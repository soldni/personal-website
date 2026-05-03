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
        markers += "\u03b1"
    if name in core_authors:
        markers += "\u03c9"
    if markers:
        formatted += f'<sup class="author-marker">{escape(markers)}</sup>'

    return f'<span class="author-name">{formatted}</span>'


def render_authors_html(entry: dict[str, str]) -> str:
    authors = split_name_list(entry.get("author", ""))
    equal_authors = set(split_name_list(entry.get("author_equal", "")))
    core_authors = set(split_name_list(entry.get("author_core", "")))
    formatted_authors = [format_author(author, equal_authors, core_authors) for author in authors]

    team_prefix = entry.get("team_prefix", "").strip()

    if team_prefix and len(formatted_authors) >= 3:
        # Team prefix present — hide all individual authors, colon hidden with them
        hidden = ", ".join(formatted_authors)
        authors_html = f'<span class="hide-authors">: {hidden}</span>'
    elif len(formatted_authors) >= 16:
        # Pin equal/core contributors so they are never hidden
        pinned = set()
        for i, name in enumerate(authors):
            if name in equal_authors or name in core_authors:
                pinned.add(i)

        n = len(formatted_authors)

        # Collect middle section into (is_span, content) pairs
        middle: list[tuple[bool, str]] = []
        hideable_run: list[str] = []
        for i in range(4, n - 2):
            if i in pinned:
                if hideable_run:
                    middle.append((True, ", ".join(hideable_run)))
                    hideable_run = []
                middle.append((False, formatted_authors[i]))
            else:
                hideable_run.append(formatted_authors[i])
        if hideable_run:
            middle.append((True, ", ".join(hideable_run)))

        # Assemble with boundary commas tucked inside hide-spans.
        # Spans include leading ", " and trailing "," so commas vanish
        # when collapsed. Visible ↔ visible uses normal ", "; after a
        # collapsed span a space reconnects to the next visible author.
        authors_html = ", ".join(formatted_authors[:4])
        prev_was_span = False
        for is_span, content in middle:
            if is_span:
                authors_html += f'<span class="hide-authors">, {content},</span>'
                prev_was_span = True
            else:
                authors_html += f" {content}" if prev_was_span else f", {content}"
                prev_was_span = False
        trailing = ", ".join(formatted_authors[-2:])
        if trailing:
            authors_html += f" {trailing}" if prev_was_span else f", {trailing}"
    else:
        authors_html = ", ".join(formatted_authors)

    if not team_prefix:
        return authors_html

    escaped_prefix = f'<span class="author-name">{escape(team_prefix)}</span>'
    if not authors_html:
        return escaped_prefix
    return f"{escaped_prefix}{authors_html}"
