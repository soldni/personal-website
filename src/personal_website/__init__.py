import json
import re
import subprocess
import sys
import time
import urllib.request
from collections import Counter
from html import escape
from pathlib import Path

from hugo.cli import __call as _hugo_cli_entrypoint

__all__ = ["hugo_cli_entrypoint", "preview", "preview_png"]

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PUBLICATIONS_BIB = PROJECT_ROOT / "content" / "publications.bib"
GENERATED_PUBLICATIONS_JSON = PROJECT_ROOT / "data" / "generated" / "publications.json"
HIGHLIGHT_AUTHOR = "Luca Soldaini"

VENUE_SHORT_NAMES = {
    "AAAI Conference on Artificial Intelligence": "AAAI",
    "AAAI/ACM Conference on AI, Ethics, and Society": "AIES",
    "ACM Conference on Bioinformatics, Computational Biology, and Health Informatics": "ACM-BCB",
    "ACM International Conference on Information and Knowledge Management": "CIKM",
    "Annual Conference of the North American Chapter of the Association for Computational Linguistics": "NAACL",
    "Annual Meeting of the Association for Computational Linguistics": "ACL",
    "Conference of the Asia-Pacific Chapter of the Association for Computational Linguistics": "AACL",
    "Conference of the European Chapter of the Association for Computational Linguistics": "EACL",
    "Conference on Computer Vision and Pattern Recognition": "CVPR",
    "Conference on Empirical Methods in Natural Language Processing": "EMNLP",
    "Conference on Fairness, Accountability, and Transparency": "FAccT",
    "Conference on Language Modeling": "COLM",
    "Conference on Neural Information Processing Systems": "NeurIPS",
    "European Conference on Information Retrieval": "ECIR",
    "International ACM SIGIR Conference on Research and Development in Information Retrieval": "SIGIR",
    "International Conference on Computational Linguistics": "COLING",
    "International Conference on Intelligent User Interfaces": "IUI",
    "International Conference on Learning Representations": "ICLR",
    "International Conference on Machine Learning": "ICML",
    "Journal of the Association for Information Science and Technology": "JASIST",
    "Nature": "Nature",
    "SIAM International Conference on Data Mining": "SDM",
    "Text REtrieval Conference": "TREC",
    "The Web Conference": "WWW",
    "Transactions on Machine Learning Research": "TMLR",
}


def _unescape_bibtex(value: str) -> str:
    return value.replace("\\{", "{").replace("\\}", "}").replace("\\\\", "\\")


def _parse_bibtex_value(text: str, index: int) -> tuple[str, int]:
    if text[index] == "{":
        index += 1
        depth = 0
        chars = []
        while index < len(text):
            char = text[index]
            if char == "\\" and index + 1 < len(text):
                chars.append(char)
                chars.append(text[index + 1])
                index += 2
                continue
            if char == "{":
                depth += 1
                chars.append(char)
                index += 1
                continue
            if char == "}":
                if depth == 0:
                    return _unescape_bibtex("".join(chars)).strip(), index + 1
                depth -= 1
                chars.append(char)
                index += 1
                continue
            chars.append(char)
            index += 1
        raise ValueError("Unterminated braced BibTeX value")

    if text[index] == '"':
        index += 1
        chars = []
        while index < len(text):
            char = text[index]
            if char == "\\" and index + 1 < len(text):
                chars.append(text[index + 1])
                index += 2
                continue
            if char == '"':
                return "".join(chars).strip(), index + 1
            chars.append(char)
            index += 1
        raise ValueError("Unterminated quoted BibTeX value")

    start = index
    while index < len(text) and text[index] not in ",}\n":
        index += 1
    return text[start:index].strip(), index


def _parse_bibtex_entries(text: str) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    index = 0
    while index < len(text):
        if text[index] != "@":
            index += 1
            continue

        entry_match = re.match(r"@([A-Za-z]+)\s*\{\s*([^,]+)\s*,", text[index:])
        if entry_match is None:
            raise ValueError(f"Could not parse BibTeX entry near index {index}")

        entry_type, entry_key = entry_match.groups()
        index += entry_match.end()
        entry: dict[str, str] = {"entry_type": entry_type.lower(), "key": entry_key.strip()}

        while index < len(text):
            while index < len(text) and text[index] in " \t\r\n,":
                index += 1

            if index >= len(text):
                break

            if text[index] == "}":
                index += 1
                break

            field_match = re.match(r"([A-Za-z_][A-Za-z0-9_]*)\s*=", text[index:])
            if field_match is None:
                raise ValueError(f"Could not parse BibTeX field near index {index}")

            field_name = field_match.group(1).lower()
            index += field_match.end()
            while index < len(text) and text[index].isspace():
                index += 1

            field_value, index = _parse_bibtex_value(text, index)
            entry[field_name] = field_value

            while index < len(text) and text[index].isspace():
                index += 1
            if index < len(text) and text[index] == ",":
                index += 1

        entries.append(entry)

    return entries


def _split_bibtex_name_list(value: str) -> list[str]:
    if not value:
        return []
    return [part.strip() for part in re.split(r"\s+and\s+", value) if part.strip()]


def _format_author(name: str, equal_authors: set[str], core_authors: set[str]) -> str:
    formatted = escape(name)
    if name == HIGHLIGHT_AUTHOR:
        formatted = f"<strong>{formatted}</strong>"

    markers = ""
    if name in equal_authors:
        markers += "*"
    if name in core_authors:
        markers += "†"
    if markers:
        formatted += f"<sup>{escape(markers)}</sup>"

    return formatted


def _render_authors_html(entry: dict[str, str]) -> str:
    authors = _split_bibtex_name_list(entry.get("author", ""))
    equal_authors = set(_split_bibtex_name_list(entry.get("author_equal", "")))
    core_authors = set(_split_bibtex_name_list(entry.get("author_core", "")))
    formatted_authors = [_format_author(author, equal_authors, core_authors) for author in authors]

    if len(formatted_authors) >= 16:
        leading = ", ".join(formatted_authors[:4])
        hidden = ", ".join(formatted_authors[4:-2])
        trailing = ", ".join(formatted_authors[-2:])
        authors_html = leading
        if hidden:
            authors_html += f'<span class="hide-authors">, {hidden},</span>'
        if trailing:
            authors_html += f" {trailing}"
    else:
        authors_html = ", ".join(formatted_authors)

    prefix = entry.get("author_prefix", "").strip()
    if not prefix:
        return authors_html

    escaped_prefix = escape(prefix)
    if not authors_html:
        return escaped_prefix
    if prefix.endswith(":"):
        return f"{escaped_prefix} {authors_html}"
    return f"{escaped_prefix}, {authors_html}"


def _venue_short_name(name: str) -> str:
    return VENUE_SHORT_NAMES.get(name, name)


def _render_venue_text(entry: dict[str, str]) -> str:
    archiveprefix = entry.get("archiveprefix", "")
    eprint = entry.get("eprint", "")
    if archiveprefix and eprint:
        return f"arXiv {eprint}"

    if entry.get("journal"):
        parts = [_venue_short_name(entry["journal"]), entry.get("year", "")]
        return " ".join(part for part in parts if part)

    if entry.get("school"):
        parts = [_venue_short_name(entry["school"]), entry.get("year", ""), "PhD Thesis"]
        return " ".join(part for part in parts if part)

    if entry.get("booktitle"):
        parts = [_venue_short_name(entry["booktitle"]), entry.get("year", ""), entry.get("venue_note", "")]
        return " ".join(part for part in parts if part)

    return ""


def _derive_badge_style(badge: str) -> str:
    if not badge:
        return ""
    if badge in {"preprint", "technical report"}:
        return "call-in"
    return "call-out"


def _validate_entry(entry: dict[str, str]) -> None:
    required_fields = ["title", "author", "year", "order", "url", "topic"]
    missing = [field for field in required_fields if not entry.get(field)]
    if missing:
        raise ValueError(f"Missing required fields for {entry.get('key', '<unknown>')}: {', '.join(missing)}")


def _prepare_entry(entry: dict[str, str]) -> dict[str, str]:
    _validate_entry(entry)
    prepared = dict(entry)
    prepared["authors_html"] = _render_authors_html(entry)
    prepared["venue_text"] = _render_venue_text(entry)
    prepared["badge_style"] = _derive_badge_style(entry.get("badge", ""))
    return prepared


def generate_publications_data() -> None:
    if not PUBLICATIONS_BIB.exists():
        return

    entries = _parse_bibtex_entries(PUBLICATIONS_BIB.read_text())
    entries.sort(key=lambda entry: (-(int(entry.get("year", "0"))), int(entry.get("order", "0"))))
    prepared_entries = [_prepare_entry(entry) for entry in entries]

    years: list[str] = []
    for entry in prepared_entries:
        year = entry.get("year", "")
        if year and year not in years:
            years.append(year)

    topic_counts = Counter(entry.get("topic", "") for entry in prepared_entries if entry.get("topic"))
    year_counts = Counter(entry.get("year", "") for entry in prepared_entries if entry.get("year"))

    payload = {
        "entries": prepared_entries,
        "years": years,
        "topic_counts": dict(topic_counts),
        "year_counts": dict(year_counts),
    }

    GENERATED_PUBLICATIONS_JSON.parent.mkdir(parents=True, exist_ok=True)
    GENERATED_PUBLICATIONS_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def hugo_cli_entrypoint() -> None:
    generate_publications_data()
    _hugo_cli_entrypoint()


def preview():
    generate_publications_data()
    preview_cli = ["server", "--disableFastRender"]
    sys.argv = sys.argv[:1] + preview_cli + [arg for arg in sys.argv[1:] if arg not in preview_cli]
    _hugo_cli_entrypoint()


def preview_png():
    generate_publications_data()
    args = [arg for arg in sys.argv[1:] if arg != "--"]
    if len(args) != 1:
        print("Usage: uv run preview-png -- <page path>", file=sys.stderr)
        raise SystemExit(2)

    page_path = args[0].strip()
    normalized = "/" + page_path.strip("/")

    output_dir = Path(".artifacts")
    output_dir.mkdir(parents=True, exist_ok=True)

    slug = normalized.strip("/").replace("/", "-") or "home"
    screenshot_path = output_dir / f"preview-{slug}.png"

    server_cmd = ["hugo", "server", "--disableFastRender", "-D", "--bind", "127.0.0.1", "--port", "1313"]
    server = subprocess.Popen(server_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    try:
        url = f"http://127.0.0.1:1313{normalized}"
        for _ in range(30):
            try:
                urllib.request.urlopen(url, timeout=1)
                break
            except Exception:
                time.sleep(0.5)

        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)

        from playwright.sync_api import sync_playwright

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            page = browser.new_page(viewport={"width": 1440, "height": 1800})
            page.goto(url, wait_until="networkidle")
            page.screenshot(path=str(screenshot_path), full_page=True)
            browser.close()
    finally:
        server.terminate()
        server.wait(timeout=5)

    print(screenshot_path)
