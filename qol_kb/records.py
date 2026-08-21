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
EVIDENCE_STRENGTH_ORDER = {
    "Low": 0,
    "Moderate": 1,
    "High": 2,
}


@dataclass(frozen=True)
class Record:
    record_type: str
    front_matter: dict[str, Any]
    body: str
    evidence_strength: str | None = None


@dataclass(frozen=True)
class Category:
    name: str
    definition: str
    status: str
    replaced_by: str | None = None


class _UniqueKeyLoader(yaml.SafeLoader):
    pass


def _construct_unique_mapping(
    loader: _UniqueKeyLoader,
    node: yaml.MappingNode,
    deep: bool = False,
) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            if key in mapping:
                raise ValueError(f"duplicate YAML key: {key}")
            mapping[key] = loader.construct_object(value_node, deep=deep)
        except TypeError as error:
            raise ValueError(f"unhashable YAML key: {key}") from error
    return mapping


_UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


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
    _validate_schema_data(
        record_path,
        SCHEMA_FILES[record_type],
        front_matter,
    )


def _validate_schema_data(
    source_path: Path,
    schema_filename: str,
    data: dict[str, Any],
) -> None:
    schema_path = SCHEMA_DIR / schema_filename
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    errors = sorted(
        validator.iter_errors(data),
        key=lambda error: (str(list(error.absolute_path)), error.message),
    )
    if errors:
        details = []
        for error in errors:
            error_path = _validation_error_path(error)
            details.append(
                f"{error_path}: {error.message}" if error_path else error.message
            )
        raise ValueError(f"{source_path}: {'; '.join(details)}")


def load_category_registry(path: str | Path) -> dict[str, Category]:
    registry_path = Path(path)
    if not registry_path.is_file():
        raise ValueError(f"{registry_path}: canonical category registry is required")

    try:
        registry_data = yaml.load(
            registry_path.read_text(encoding="utf-8"),
            Loader=_UniqueKeyLoader,
        )
    except (ValueError, yaml.YAMLError) as error:
        raise ValueError(f"{registry_path}: {error}") from error

    if not isinstance(registry_data, dict):
        raise ValueError(f"{registry_path}: category registry must be a mapping")

    _validate_schema_data(
        registry_path,
        "category-registry.schema.json",
        registry_data,
    )
    categories: dict[str, Category] = {}
    for name, data in registry_data["categories"].items():
        definition = data["definition"]
        if not definition.strip():
            raise ValueError(f"{registry_path}: {name} definition must not be blank")
        categories[name] = Category(
            name=name,
            definition=definition,
            status=data["status"],
            replaced_by=data.get("replaced_by"),
        )
    return categories


def _support_claims(front_matter: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        claim
        for claim in front_matter["evidence_claims"]
        if claim["role"] == "Support"
    ]


def _derived_evidence_strength(front_matter: dict[str, Any]) -> str | None:
    support_claims = _support_claims(front_matter)
    if not support_claims:
        return None
    return min(
        (claim["strength"] for claim in support_claims),
        key=EVIDENCE_STRENGTH_ORDER.__getitem__,
    )


def _validate_item_semantics(record_path: Path, front_matter: dict[str, Any]) -> None:
    if front_matter["applicability"] == "Conditional":
        condition = front_matter.get("condition")
        if not isinstance(condition, str) or not condition.strip():
            raise ValueError(f"{record_path}: condition is required for Conditional items")

    if front_matter["status"] == "Active" and not _support_claims(front_matter):
        raise ValueError(f"{record_path}: Active items require at least one Support Claim")

    if front_matter["status"] == "Deprecated":
        reason = front_matter.get("deprecation_reason")
        if not isinstance(reason, str) or not reason.strip():
            raise ValueError(f"{record_path}: deprecation_reason is required for Deprecated items")


def _validate_reference_semantics(
    record_path: Path,
    front_matter: dict[str, Any],
) -> None:
    if front_matter["status"] == "Deprecated":
        reason = front_matter.get("deprecation_reason")
        if not isinstance(reason, str) or not reason.strip():
            raise ValueError(
                f"{record_path}: deprecation_reason is required for Deprecated references"
            )


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

    if record_type == "item":
        _validate_item_semantics(record_path, front_matter)
        evidence_strength = _derived_evidence_strength(front_matter)
    else:
        _validate_reference_semantics(record_path, front_matter)
        evidence_strength = None

    body = "".join(lines[closing_index + 1 :])
    return Record(
        record_type=record_type,
        front_matter=front_matter,
        body=body,
        evidence_strength=evidence_strength,
    )


def validate_repository(root: str | Path) -> None:
    root_path = Path(root)
    records_by_id: dict[str, Record] = {}

    for folder in ("references", "items"):
        directory = root_path / folder
        if not directory.exists():
            continue
        for path in sorted(directory.glob("*.md")):
            record = load_record(path)
            record_id = record.front_matter["id"]
            if record_id in records_by_id:
                raise ValueError(f"duplicate canonical record id: {record_id}")
            records_by_id[record_id] = record

    for record_id, record in records_by_id.items():
        if record.record_type != "item":
            continue

        for claim in record.front_matter["evidence_claims"]:
            for reference_id in claim["references"]:
                reference = records_by_id.get(reference_id)
                if reference is None or reference.record_type != "reference":
                    raise ValueError(
                        f"{record_id}: evidence claim reference does not resolve: {reference_id}"
                    )
                if (
                    record.front_matter["status"] == "Active"
                    and reference.front_matter["status"] == "Deprecated"
                ):
                    raise ValueError(
                        f"{record_id}: active item cannot use Deprecated reference {reference_id}"
                    )

        for replacement_id in record.front_matter.get("replaced_by", []):
            replacement = records_by_id.get(replacement_id)
            if replacement is None or replacement.record_type != "item":
                raise ValueError(
                    f"{record_id}: replacement item does not resolve: {replacement_id}"
                )

        for relationship in record.front_matter["relationships"]:
            target_id = relationship["target"]
            if target_id == record_id:
                raise ValueError(
                    f"{record_id}: relationship target must be a distinct item: {target_id}"
                )
            target = records_by_id.get(target_id)
            if target is None or target.record_type != "item":
                raise ValueError(
                    f"{record_id}: relationship target does not resolve: {target_id}"
                )
