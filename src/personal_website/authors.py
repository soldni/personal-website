import re
from html import escape

HIGHLIGHT_AUTHOR = "Luca Soldaini"


def split_name_list(value: str) -> list[str]:
    if not value:
        return []
    return [part.strip() for part in re.split(r"\s+and\s+", value) if part.strip()]


def format_author(name: str, equal_authors: set[str], core_authors: set[str]) -> str:
    formatted = escape(name)
    if name == HIGHLIGHT_AUTHOR:
        formatted = f"<strong>{formatted}</strong>"

    markers = ""
    if name in equal_authors:
        markers += "*"
    if name in core_authors:
        markers += "\u2020"
    if markers:
        formatted += f"<sup>{escape(markers)}</sup>"

    return formatted


def render_authors_html(entry: dict[str, str]) -> str:
    authors = split_name_list(entry.get("author", ""))
    equal_authors = set(split_name_list(entry.get("author_equal", "")))
    core_authors = set(split_name_list(entry.get("author_core", "")))
    formatted_authors = [format_author(author, equal_authors, core_authors) for author in authors]

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
