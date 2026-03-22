import json
import re
import subprocess
import sys
import time
import urllib.request
from collections import Counter
from pathlib import Path

from hugo.cli import __call as _hugo_cli_entrypoint

__all__ = ["hugo_cli_entrypoint", "preview", "preview_png"]

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PUBLICATIONS_BIB = PROJECT_ROOT / "content" / "publications.bib"
GENERATED_PUBLICATIONS_JSON = PROJECT_ROOT / "data" / "generated" / "publications.json"


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


def generate_publications_data() -> None:
    if not PUBLICATIONS_BIB.exists():
        return

    entries = _parse_bibtex_entries(PUBLICATIONS_BIB.read_text())
    entries.sort(key=lambda entry: (-(int(entry.get("year", "0"))), int(entry.get("order", "0"))))

    years: list[str] = []
    for entry in entries:
        year = entry.get("year", "")
        if year and year not in years:
            years.append(year)

    topic_counts = Counter(entry.get("topic", "") for entry in entries if entry.get("topic"))
    year_counts = Counter(entry.get("year", "") for entry in entries if entry.get("year"))

    payload = {
        "entries": entries,
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
    sys.argv = sys.argv[:1] + preview_cli + [k for k in sys.argv[1:] if k not in preview_cli]
    _hugo_cli_entrypoint()


def preview_png():
    generate_publications_data()
    args = [a for a in sys.argv[1:] if a != "--"]
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

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 1440, "height": 1800})
            page.goto(url, wait_until="networkidle")
            page.screenshot(path=str(screenshot_path), full_page=True)
            browser.close()
    finally:
        server.terminate()
        server.wait(timeout=5)

    print(screenshot_path)
