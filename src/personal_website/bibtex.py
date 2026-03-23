from pathlib import Path

import bibtexparser


def parse_bib_file(path: Path) -> list[dict[str, str]]:
    library = bibtexparser.parse_string(path.read_text())

    if library.failed_blocks:
        messages = [str(block) for block in library.failed_blocks]
        raise ValueError(f"Failed to parse BibTeX blocks:\n" + "\n".join(messages))

    entries: list[dict[str, str]] = []
    for entry in library.entries:
        record: dict[str, str] = {
            "entry_type": entry.entry_type.lower(),
            "key": entry.key,
        }
        for field_key, field_value in entry.fields_dict.items():
            record[field_key.lower()] = field_value.value
        entries.append(record)

    return entries
