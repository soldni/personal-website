import json
from collections import Counter
from pathlib import Path

from .authors import render_authors_html
from .bibtex import parse_bib_file
from .venues import render_venue_text

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PUBLICATIONS_BIB = PROJECT_ROOT / "content" / "publications.bib"
GENERATED_PUBLICATIONS_JSON = PROJECT_ROOT / "data" / "generated" / "publications.json"


def validate_entry(entry: dict[str, str]) -> None:
    required_fields = ["title", "author", "year", "order", "url", "topic"]
    missing = [field for field in required_fields if not entry.get(field)]
    if missing:
        raise ValueError(f"Missing required fields for {entry.get('key', '<unknown>')}: {', '.join(missing)}")


def derive_badge_style(badge: str) -> str:
    if not badge:
        return ""
    if badge in {"preprint", "tech report"}:
        return "call-in"
    return "call-out"


def is_preprint(entry: dict[str, str]) -> bool:
    return entry.get("badge", "").strip().lower() == "preprint"


def prepare_entry(entry: dict[str, str]) -> dict[str, str]:
    validate_entry(entry)
    prepared = dict(entry)
    prepared["authors_html"] = render_authors_html(entry)
    prepared["venue_text"] = render_venue_text(entry)
    if is_preprint(prepared) and (
        prepared["venue_text"] == "preprint" or entry.get("booktitle") or entry.get("journal") or entry.get("school")
    ):
        prepared["venue_text"] = ""
    prepared["badge_style"] = derive_badge_style(prepared.get("badge", ""))
    return prepared


def _safe_int(value: str, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def generate_publications_data() -> None:
    if not PUBLICATIONS_BIB.exists():
        return

    entries = parse_bib_file(PUBLICATIONS_BIB)
    entries.sort(
        key=lambda entry: (
            -_safe_int(entry.get("year", "0")),
            -_safe_int(entry.get("order", "0")),
        )
    )
    prepared_entries = [prepare_entry(entry) for entry in entries]

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
