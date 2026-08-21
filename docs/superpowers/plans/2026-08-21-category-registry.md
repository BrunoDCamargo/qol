# Canonical Category Registry Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a canonical, validated category registry and reject unknown or deprecated category tags on Active QoL Items without coupling categories to Item identity.

**Architecture:** Store categories in one root `categories.yaml` mapping validated by a dedicated JSON Schema and semantic lifecycle checks. Add an immutable `Category` value plus `load_category_registry()` to `qol_kb.records`, then load the registry first in `validate_repository()` and validate Active Item tags against it.

**Tech Stack:** Python 3, `unittest`, PyYAML, jsonschema Draft 2020-12, YAML, JSON Schema, Markdown

**Spec:** `docs/superpowers/specs/2026-08-21-category-registry-design.md`

## Global Constraints

- The canonical source is one version-controlled root file named `categories.yaml`.
- Category names must match `^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$`.
- The initial registry contains exactly `physical-activity`, `environment`, `mental-health`, and `circadian`.
- Topic Views are non-canonical and must not be imported automatically.
- YAML mapping keys must be unique and duplicate keys must fail instead of being overwritten.
- Lifecycle values are exactly `Active` and `Deprecated`.
- A replacement, when present, points directly to a distinct Active category; replacement chains are unsupported.
- Only Active QoL Items are restricted to known Active category tags; Deprecated Items may retain historical tags.
- Categories never determine Item IDs, filenames, ownership, or placement.
- Add no runtime dependency; reuse PyYAML and jsonschema.
- Validation failures use `ValueError` and identify the source path and relevant category or item identifier.

---

### Task 1: Canonical registry schema, seed, and loader

**Files:**
- Create: `categories.yaml`
- Create: `schemas/category-registry.schema.json`
- Create: `tests/test_category_registry.py`
- Modify: `qol_kb/records.py`

**Interfaces:**
- Consumes: existing `SCHEMA_DIR`, `_validation_error_path()`, PyYAML, and `Draft202012Validator` from `qol_kb.records`.
- Produces: immutable `Category(name: str, definition: str, status: str, replaced_by: str | None = None)` and `load_category_registry(path: str | Path) -> dict[str, Category]` for Tasks 2 and 3.

- [ ] **Step 1: Add focused failing loader tests**

Create `tests/test_category_registry.py` with the shared writer and these initial cases:

```python
from pathlib import Path
import tempfile
import unittest

from qol_kb.records import load_category_registry


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class CategoryRegistryTests(unittest.TestCase):
    def _write_registry(self, root: Path, yaml_text: str) -> Path:
        path = root / "categories.yaml"
        path.write_text(yaml_text, encoding="utf-8")
        return path

    def test_seeded_registry_loads_canonical_categories(self):
        categories = load_category_registry(REPOSITORY_ROOT / "categories.yaml")
        self.assertEqual(
            set(categories),
            {"physical-activity", "environment", "mental-health", "circadian"},
        )
        self.assertEqual(categories["physical-activity"].status, "Active")
        self.assertTrue(categories["physical-activity"].definition.strip())

    def test_registry_rejects_non_kebab_case_names(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write_registry(
                Path(tmp),
                "categories:\n  Mental Health:\n    definition: Invalid name.\n    status: Active\n",
            )
            with self.assertRaisesRegex(ValueError, r"Mental Health"):
                load_category_registry(path)

    def test_registry_rejects_duplicate_category_keys(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write_registry(
                Path(tmp),
                "categories:\n"
                "  physical-activity:\n"
                "    definition: First definition.\n"
                "    status: Active\n"
                "  physical-activity:\n"
                "    definition: Second definition.\n"
                "    status: Active\n",
            )
            with self.assertRaisesRegex(ValueError, r"duplicate.*physical-activity"):
                load_category_registry(path)

    def test_registry_rejects_blank_definition_and_unknown_status(self):
        invalid_entries = (
            (
                "blank-definition",
                "categories:\n  sleep:\n    definition: '   '\n    status: Active\n",
                r"sleep.*definition|definition.*sleep",
            ),
            (
                "unknown-status",
                "categories:\n  sleep:\n    definition: Sleep timing.\n    status: Retired\n",
                r"Retired|status",
            ),
        )
        for label, yaml_text, message in invalid_entries:
            with self.subTest(label=label), tempfile.TemporaryDirectory() as tmp:
                path = self._write_registry(Path(tmp), yaml_text)
                with self.assertRaisesRegex(ValueError, message):
                    load_category_registry(path)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the new module and confirm RED**

Run: `python -m unittest tests.test_category_registry -v`

Expected: ERROR importing `load_category_registry` from `qol_kb.records`.

- [ ] **Step 3: Add the closed category-registry schema**

Create `schemas/category-registry.schema.json`:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.invalid/qol/schemas/category-registry.schema.json",
  "title": "Canonical category registry",
  "type": "object",
  "additionalProperties": false,
  "required": ["categories"],
  "properties": {
    "categories": {
      "type": "object",
      "propertyNames": {
        "pattern": "^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$"
      },
      "additionalProperties": {
        "type": "object",
        "additionalProperties": false,
        "required": ["definition", "status"],
        "properties": {
          "definition": {"type": "string", "minLength": 1},
          "status": {"type": "string", "enum": ["Active", "Deprecated"]},
          "replaced_by": {
            "type": "string",
            "pattern": "^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$"
          }
        }
      }
    }
  }
}
```

- [ ] **Step 4: Seed the canonical registry**

Create root `categories.yaml` exactly as follows:

```yaml
categories:
  physical-activity:
    definition: Interventions and exposures involving bodily movement or exercise.
    status: Active
  environment:
    definition: Physical environmental conditions and exposures affecting quality of life.
    status: Active
  mental-health:
    definition: Psychological and emotional well-being, symptoms, and functioning.
    status: Active
  circadian:
    definition: Timing and regularity of sleep, wakefulness, and other circadian exposures.
    status: Active
```

- [ ] **Step 5: Implement duplicate-safe YAML loading and shared schema validation**

In `qol_kb/records.py`, add `Category` beside `Record`, then add the loader helpers before `load_record()`:

```python
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
        if key in mapping:
            raise ValueError(f"duplicate YAML key: {key}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


_UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
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
```

Replace the body of existing `_validate_front_matter()` with the shared helper so validation logic is not duplicated and existing error messages remain unchanged:

```python
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
```

Then add the category loader:

```python


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
```

- [ ] **Step 6: Run focused tests and confirm GREEN**

Run: `python -m unittest tests.test_category_registry -v`

Expected: 4 tests pass.

- [ ] **Step 7: Run the existing suite for regression safety**

Run: `python -m unittest discover -s tests -v`

Expected: 34 tests pass.

- [ ] **Step 8: Commit Task 1**

```bash
git add -- categories.yaml schemas/category-registry.schema.json qol_kb/records.py tests/test_category_registry.py
git commit -m "feat: add canonical category registry"
```

---

### Task 2: Category lifecycle and replacement validation

**Files:**
- Modify: `tests/test_category_registry.py`
- Modify: `qol_kb/records.py`

**Interfaces:**
- Consumes: `Category` and `load_category_registry(path: str | Path) -> dict[str, Category]` from Task 1.
- Produces: `load_category_registry()` guarantees that every `replaced_by` is absent or resolves directly to a distinct Active `Category`.

- [ ] **Step 1: Add failing lifecycle tests**

Append these methods to `CategoryRegistryTests`:

```python
def test_deprecated_category_allows_no_replacement_or_active_replacement(self):
    registry_variants = (
        "categories:\n  old-name:\n    definition: Historical tag.\n    status: Deprecated\n",
        "categories:\n"
        "  current-name:\n"
        "    definition: Current tag.\n"
        "    status: Active\n"
        "  old-name:\n"
        "    definition: Historical tag.\n"
        "    status: Deprecated\n"
        "    replaced_by: current-name\n",
    )
    for yaml_text in registry_variants:
        with self.subTest(yaml_text=yaml_text), tempfile.TemporaryDirectory() as tmp:
            categories = load_category_registry(
                self._write_registry(Path(tmp), yaml_text)
            )
            self.assertEqual(categories["old-name"].status, "Deprecated")

def test_active_category_rejects_replacement(self):
    with tempfile.TemporaryDirectory() as tmp:
        path = self._write_registry(
            Path(tmp),
            "categories:\n"
            "  current-name:\n"
            "    definition: Current tag.\n"
            "    status: Active\n"
            "    replaced_by: other-name\n"
            "  other-name:\n"
            "    definition: Other tag.\n"
            "    status: Active\n",
        )
        with self.assertRaisesRegex(ValueError, r"current-name.*replaced_by"):
            load_category_registry(path)

def test_deprecated_category_replacement_must_be_distinct_known_and_active(self):
    invalid_targets = (
        ("self", "old-name", "", r"old-name.*distinct"),
        ("unknown", "missing-name", "", r"missing-name.*resolve"),
        (
            "deprecated",
            "older-name",
            "  older-name:\n"
            "    definition: Older historical tag.\n"
            "    status: Deprecated\n",
            r"older-name.*Active|Active.*older-name",
        ),
    )
    for label, target, extra_entry, message in invalid_targets:
        with self.subTest(label=label), tempfile.TemporaryDirectory() as tmp:
            path = self._write_registry(
                Path(tmp),
                "categories:\n"
                f"{extra_entry}"
                "  old-name:\n"
                "    definition: Historical tag.\n"
                "    status: Deprecated\n"
                f"    replaced_by: {target}\n",
            )
            with self.assertRaisesRegex(ValueError, message):
                load_category_registry(path)
```

- [ ] **Step 2: Run lifecycle tests and confirm RED**

Run: `python -m unittest tests.test_category_registry.CategoryRegistryTests.test_active_category_rejects_replacement tests.test_category_registry.CategoryRegistryTests.test_deprecated_category_replacement_must_be_distinct_known_and_active -v`

Expected: both tests fail because Task 1 stores replacement values without semantic validation.

- [ ] **Step 3: Implement lifecycle validation**

Add this loop at the end of `load_category_registry()`, immediately before `return categories`:

```python
for name, category in categories.items():
    replacement_name = category.replaced_by
    if category.status == "Active" and replacement_name is not None:
        raise ValueError(
            f"{registry_path}: Active category {name} cannot declare replaced_by"
        )
    if replacement_name is None:
        continue
    if replacement_name == name:
        raise ValueError(
            f"{registry_path}: category {name} replacement must be distinct"
        )
    replacement = categories.get(replacement_name)
    if replacement is None:
        raise ValueError(
            f"{registry_path}: category {name} replacement does not resolve: "
            f"{replacement_name}"
        )
    if replacement.status != "Active":
        raise ValueError(
            f"{registry_path}: category {name} replacement must be Active: "
            f"{replacement_name}"
        )
```

- [ ] **Step 4: Run the category-registry module and confirm GREEN**

Run: `python -m unittest tests.test_category_registry -v`

Expected: 7 tests pass.

- [ ] **Step 5: Run the complete suite**

Run: `python -m unittest discover -s tests -v`

Expected: 37 tests pass.

- [ ] **Step 6: Commit Task 2**

```bash
git add -- qol_kb/records.py tests/test_category_registry.py
git commit -m "feat: validate category lifecycle"
```

---

### Task 3: Enforce Active Item category usage and document contributions

**Files:**
- Modify: `tests/test_domain_invariants.py`
- Modify: `qol_kb/records.py`
- Modify: `README.md`

**Interfaces:**
- Consumes: `load_category_registry(root / "categories.yaml") -> dict[str, Category]` and validated `Category.status` from Tasks 1 and 2.
- Produces: `validate_repository(root: str | Path) -> None` requires `categories.yaml` and rejects unknown or Deprecated tags on Active Items while leaving Item ID validation unchanged.

- [ ] **Step 1: Add an explicit category-registry fixture to domain tests**

Add this helper to `QoLDomainInvariantTests` in `tests/test_domain_invariants.py`:

```python
def _write_category_registry(
    self,
    root: Path,
    categories: dict | None = None,
) -> Path:
    registry_path = root / "categories.yaml"
    registry_path.write_text(
        yaml.safe_dump(
            {"categories": categories or {}},
            sort_keys=False,
            allow_unicode=True,
        ),
        encoding="utf-8",
    )
    return registry_path
```

Update the existing `_validate_repository()` test helper so old repository-level tests explicitly receive an empty registry:

```python
def _validate_repository(self, root: Path) -> None:
    validator = getattr(records, "validate_repository", None)
    self.assertIsNotNone(
        validator,
        "repository-level validation is required for cross-record invariants",
    )
    if not (root / "categories.yaml").exists():
        self._write_category_registry(root)
    validator(root)
```

- [ ] **Step 2: Add failing repository-integration tests**

Append these methods to `QoLDomainInvariantTests`:

```python
def test_repository_requires_category_registry(self):
    with tempfile.TemporaryDirectory() as tmp:
        with self.assertRaisesRegex(ValueError, r"categories.yaml.*required"):
            records.validate_repository(Path(tmp))

def test_active_item_accepts_only_known_active_categories(self):
    cases = (
        (
            "active",
            {"sleep": {"definition": "Sleep timing.", "status": "Active"}},
            None,
        ),
        ("unknown", {}, r"QOL-950.*unknown category.*sleep"),
        (
            "deprecated",
            {"sleep": {"definition": "Historical sleep tag.", "status": "Deprecated"}},
            r"QOL-950.*Deprecated category.*sleep",
        ),
    )
    for label, category_entries, message in cases:
        with self.subTest(label=label), tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_category_registry(root, category_entries)
            self._write_record(root, "references", self._reference())
            self._write_record(root, "items", self._item(categories=["sleep"]))
            if message is None:
                self._validate_repository(root)
            else:
                with self.assertRaisesRegex(ValueError, message):
                    self._validate_repository(root)

def test_deprecated_item_may_retain_historical_category(self):
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        self._write_category_registry(root)
        self._write_record(
            root,
            "items",
            self._item(
                status="Deprecated",
                categories=["historical-category"],
                evidence_claims=[],
                deprecation_reason="Historical fixture.",
                replaced_by=[],
            ),
        )
        self._validate_repository(root)

def test_category_rename_does_not_change_item_id(self):
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        self._write_record(root, "references", self._reference())
        item_path = self._write_record(
            root,
            "items",
            self._item(categories=["old-name"]),
        )
        self._write_category_registry(
            root,
            {"old-name": {"definition": "Old tag.", "status": "Active"}},
        )
        self._validate_repository(root)

        item_path = self._write_record(
            root,
            "items",
            self._item(categories=["new-name"]),
        )
        self._write_category_registry(
            root,
            {"new-name": {"definition": "New tag.", "status": "Active"}},
        )
        self._validate_repository(root)
        self.assertEqual(load_record(item_path).front_matter["id"], "QOL-950")
```

- [ ] **Step 3: Run the new integration tests and confirm RED**

Run: `python -m unittest tests.test_domain_invariants.QoLDomainInvariantTests.test_repository_requires_category_registry tests.test_domain_invariants.QoLDomainInvariantTests.test_active_item_accepts_only_known_active_categories -v`

Expected: the missing-registry test fails because `validate_repository()` does not load `categories.yaml`, and the item-category test fails because Active Item tags are not checked.

- [ ] **Step 4: Integrate the registry into repository validation**

At the start of `validate_repository()` in `qol_kb/records.py`, load the required registry:

```python
def validate_repository(root: str | Path) -> None:
    root_path = Path(root)
    categories = load_category_registry(root_path / "categories.yaml")
    records_by_id: dict[str, Record] = {}
```

Inside the existing loop over `records_by_id.items()`, after confirming the record is an Item and before evidence-claim validation, add:

```python
if record.front_matter["status"] == "Active":
    for category_name in record.front_matter["categories"]:
        category = categories.get(category_name)
        if category is None:
            raise ValueError(
                f"{record_id}: unknown category does not resolve: {category_name}"
            )
        if category.status != "Active":
            raise ValueError(
                f"{record_id}: Active item cannot use Deprecated category "
                f"{category_name}"
            )
```

- [ ] **Step 5: Run domain and category tests and confirm GREEN**

Run: `python -m unittest tests.test_category_registry tests.test_domain_invariants -v`

Expected: all category-registry and domain-invariant tests pass.

- [ ] **Step 6: Update the category contribution documentation**

In `README.md`, replace the statement that contributors may introduce categories directly on Items with this workflow while preserving the surrounding explanation that categories are flexible tags:

```markdown
Register a new lower-case kebab-case category in `categories.yaml` before applying it to an Active QoL Item. Each registry entry requires a short definition and lifecycle status. Adding, renaming, or reorganizing categories does not change a QoL Item ID.
```

In `README.md` under `## How to add a category`, make the sequence explicit:

```markdown
1. Check `categories.yaml` for an existing tag that represents the retrieval dimension.
2. If none exists, add a unique lower-case kebab-case entry with a short definition and `status: Active`.
3. Apply the registered tag to relevant Active QoL Items.
4. When replacing a category, retain the old entry as `Deprecated` and optionally point `replaced_by` to its direct Active replacement.

Category changes never require a folder move, file migration, or QoL Item ID change. Topic pages remain optional thematic views rather than canonical category definitions.
```

- [ ] **Step 7: Run the complete suite and repository hygiene check**

Run: `python -m unittest discover -s tests -v`

Expected: 41 tests pass.

Run: `git diff --check`

Expected: no output and exit code 0.

- [ ] **Step 8: Commit Task 3**

```bash
git add -- qol_kb/records.py tests/test_domain_invariants.py README.md
git commit -m "feat: enforce canonical item categories"
```

---

## Final verification

- [ ] Run the focused category suite: `python -m unittest tests.test_category_registry tests.test_domain_invariants -v`.
- [ ] Run the complete suite: `python -m unittest discover -s tests -v` and confirm 41 tests pass.
- [ ] Run `git diff --check 31f412f..HEAD` and confirm no output.
- [ ] Review `31f412f..HEAD` independently against both Standards and GitHub issue #3.
- [ ] Leave issue #3, branch publication, PR creation, and merging unchanged unless explicitly authorized.
