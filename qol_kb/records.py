import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
import yaml


SCHEMA_DIR = Path(__file__).resolve().parents[1] / "schemas"
SCHEMA_FILES = {
    "item": "qol-item.schema.json",
    "reference": "reference.schema.json",
}


@dataclass(frozen=True)
class Record:
    record_type: str
    front_matter: dict[str, Any]
    body: str


def _record_type_for_path(record_path: Path) -> str:
    if record_path.suffix != ".md":
        raise ValueError(f"{record_path.name} must use the .md extension")
    if record_path.stem.startswith("QOL-"):
        return "item"
    if record_path.stem.startswith("REF-"):
        return "reference"
    raise ValueError(f"{record_path.name} is not a supported canonical record filename")


def _validation_error_path(error: Any) -> str:
    path = ""
    for part in error.absolute_path:
        if isinstance(part, int):
            path += f"[{part}]"
        else:
            path += f".{part}" if path else str(part)
    return path


def _validate_front_matter(
    record_path: Path,
    record_type: str,
    front_matter: dict[str, Any],
) -> None:
    schema_path = SCHEMA_DIR / SCHEMA_FILES[record_type]
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    errors = sorted(
        validator.iter_errors(front_matter),
        key=lambda error: (str(list(error.absolute_path)), error.message),
    )
    if errors:
        details = []
        for error in errors:
            path = _validation_error_path(error)
            details.append(f"{path}: {error.message}" if path else error.message)
        raise ValueError(f"{record_path}: {'; '.join(details)}")


def load_record(path: str | Path) -> Record:
    record_path = Path(path)
    record_type = _record_type_for_path(record_path)
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

    _validate_front_matter(record_path, record_type, front_matter)

    record_id = front_matter["id"]
    if record_path.stem != record_id:
        raise ValueError(f"{record_path.name} does not match record id {record_id}")

    body = "".join(lines[closing_index + 1 :])
    return Record(record_type=record_type, front_matter=front_matter, body=body)
