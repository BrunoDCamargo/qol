from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class Record:
    record_type: str
    front_matter: dict[str, Any]
    body: str


def load_record(path: str | Path) -> Record:
    record_path = Path(path)
    lines = record_path.read_text(encoding="utf-8").splitlines(keepends=True)

    if not lines or lines[0].strip() != "---":
        raise ValueError(f"{record_path} does not start with YAML front matter")

    closing_index = next(
        (index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---"),
        None,
    )
    if closing_index is None:
        raise ValueError(f"{record_path} has unterminated YAML front matter")

    front_matter = yaml.safe_load("".join(lines[1:closing_index])) or {}
    if not isinstance(front_matter, dict):
        raise ValueError(f"{record_path} front matter must be a mapping")

    record_id = front_matter.get("id", "")
    if record_id.startswith("QOL-"):
        record_type = "item"
    elif record_id.startswith("REF-"):
        record_type = "reference"
    else:
        raise ValueError(f"{record_path} has an unsupported record id: {record_id!r}")

    body = "".join(lines[closing_index + 1 :])
    return Record(record_type=record_type, front_matter=front_matter, body=body)
