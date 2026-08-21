# Deterministic Knowledge Views Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate byte-stable catalog and reference Markdown from one validated snapshot of canonical QoL records, with a non-writing drift check.

**Architecture:** `qol_kb.records` loads and validates one frozen `RepositorySnapshot`. Pure functions in `qol_kb.views` render the two Markdown artifacts; the same module's CLI writes them or compares their bytes in `--check` mode. Root legacy registries remain untouched during migration.

**Tech Stack:** Python 3 standard library, frozen dataclasses, pathlib, argparse, unittest, existing PyYAML and jsonschema dependencies

**Spec:** `docs/superpowers/specs/2026-08-21-deterministic-knowledge-views-design.md`

## Global Constraints

- Generated outputs are exactly `generated/catalog.md` and `generated/references.md`.
- Root `catalog.md` and `references.md` remain unchanged.
- Rendering uses UTF-8, LF line endings, no timestamps, fixed ordering, and exactly one trailing newline.
- Evidence Strength comes only from `Record.evidence_strength`, already derived from Support Claims.
- Check mode compares both outputs byte-for-byte and never writes.
- No new runtime dependency or template engine.

---

### Task 1: Validated repository snapshot

**Files:**
- Create: `tests/test_repository_snapshot.py`
- Modify: `qol_kb/records.py`

**Interfaces:**
- Consumes: existing `Category`, `Record`, `load_category_registry(path)`, and `load_record(path)`.
- Produces: frozen `RepositorySnapshot(categories: tuple[Category, ...], items: tuple[Record, ...], references: tuple[Record, ...])` and `load_repository(root: str | Path) -> RepositorySnapshot`.
- Preserves: `validate_repository(root: str | Path) -> None` and all existing validation messages.

- [ ] **Step 1: Write failing snapshot tests**

Create `tests/test_repository_snapshot.py` with a temporary canonical repository containing `QOL-999`, `QOL-1000`, `REF-999`, and `REF-1000`. Assert that `load_repository` returns a frozen snapshot, sorts categories by name and identities numerically, derives `Moderate` from one Moderate Support Claim plus one Low Constraint Claim, and that `validate_repository` still returns `None`.

```python
snapshot = records.load_repository(root)
self.assertEqual([category.name for category in snapshot.categories], ["alpha", "zeta"])
self.assertEqual([record.front_matter["id"] for record in snapshot.items], ["QOL-999", "QOL-1000"])
self.assertEqual([record.front_matter["id"] for record in snapshot.references], ["REF-999", "REF-1000"])
self.assertEqual(snapshot.items[0].evidence_strength, "Moderate")
with self.assertRaises(dataclasses.FrozenInstanceError):
    snapshot.items = ()
self.assertIsNone(records.validate_repository(root))
```

- [ ] **Step 2: Run the new tests and confirm the missing API failure**

Run:

```powershell
python -m unittest tests.test_repository_snapshot -v
```

Expected: error because `qol_kb.records` has no `load_repository` or `RepositorySnapshot`.

- [ ] **Step 3: Implement the snapshot loader**

In `qol_kb/records.py`, add:

```python
@dataclass(frozen=True)
class RepositorySnapshot:
    categories: tuple[Category, ...]
    items: tuple[Record, ...]
    references: tuple[Record, ...]


def _canonical_id_sort_key(record: Record) -> tuple[str, int]:
    prefix, number = record.front_matter["id"].split("-", maxsplit=1)
    return prefix, int(number)
```

Extract the existing cross-record checks into `_validate_repository_records(categories, records_by_id)`. Implement `load_repository` so it loads each Markdown record once, rejects duplicate IDs, runs that helper, and returns sorted tuples:

```python
def load_repository(root: str | Path) -> RepositorySnapshot:
    root_path = Path(root)
    categories = load_category_registry(root_path / "categories.yaml")
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
    _validate_repository_records(categories, records_by_id)
    return RepositorySnapshot(
        categories=tuple(sorted(categories.values(), key=lambda category: category.name)),
        items=tuple(sorted(
            (record for record in records_by_id.values() if record.record_type == "item"),
            key=_canonical_id_sort_key,
        )),
        references=tuple(sorted(
            (record for record in records_by_id.values() if record.record_type == "reference"),
            key=_canonical_id_sort_key,
        )),
    )


def validate_repository(root: str | Path) -> None:
    load_repository(root)
```

- [ ] **Step 4: Run snapshot and regression tests**

Run:

```powershell
python -m unittest tests.test_repository_snapshot tests.test_domain_invariants tests.test_category_registry tests.test_records -v
```

Expected: all tests pass with unchanged invariant error behavior.

- [ ] **Step 5: Commit the snapshot API**

```powershell
git add qol_kb/records.py tests/test_repository_snapshot.py
git commit -m "refactor: load validated repository snapshots"
```

### Task 2: Pure deterministic Markdown renderers

**Files:**
- Create: `qol_kb/views.py`
- Create: `tests/test_views.py`

**Interfaces:**
- Consumes: `RepositorySnapshot`, `Category`, and `Record` from `qol_kb.records`.
- Produces: `render_catalog(snapshot: RepositorySnapshot) -> str` and `render_references(snapshot: RepositorySnapshot) -> str`.
- Produces internally: `_markdown_cell(value: object) -> str`, `_item_reference_ids(record: Record) -> tuple[str, ...]`, and lifecycle partition helpers.

- [ ] **Step 1: Write failing catalog rendering tests**

Build `RepositorySnapshot` values directly from frozen `Category` and `Record` instances. Test that the catalog:

- starts with `<!-- Generated by python -m qol_kb.views. Do not edit. -->`;
- lists Active categories and items before Deprecated categories and items;
- sorts supplied identities numerically even if the input tuple is reversed;
- links item IDs to `../items/QOL-*.md` and references to `references.md#ref-*`;
- displays `Record.evidence_strength` exactly;
- escapes `|`, backslashes, and embedded newlines inside table cells;
- emits fixed empty-state text;
- is identical across repeated calls and ends with one `\n`.

Core assertions:

```python
rendered = views.render_catalog(snapshot)
self.assertLess(rendered.index("QOL-999"), rendered.index("QOL-1000"))
self.assertIn("[QOL-999](../items/QOL-999.md)", rendered)
self.assertIn("[REF-999](references.md#ref-999)", rendered)
self.assertIn("| Moderate |", rendered)
self.assertNotIn("Low", rendered)
self.assertEqual(rendered, views.render_catalog(snapshot))
self.assertTrue(rendered.endswith("\n"))
self.assertFalse(rendered.endswith("\n\n"))
```

- [ ] **Step 2: Run the catalog tests and confirm the missing module failure**

Run:

```powershell
python -m unittest tests.test_views.DeterministicViewTests.test_catalog_view -v
```

Expected: import error because `qol_kb.views` does not exist.

- [ ] **Step 3: Implement the catalog renderer**

Create `qol_kb/views.py` with fixed section builders joined using `"\n"`. Escape table content with:

```python
def _markdown_cell(value: object) -> str:
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\r", " ").replace("\n", " ")
```

Partition by `front_matter["status"]`, sort categories by `name`, sort records with a local numeric ID key, deduplicate and numerically sort all Support and Constraint Claim reference identities, and render the columns specified by the design. Do not recalculate Evidence Strength.

- [ ] **Step 4: Write failing reference rendering tests**

Test stable standalone headings, fixed metadata order, repeated URL and Supports bullet order, omitted optional fields when null, and lifecycle separation:

```python
rendered = views.render_references(snapshot)
self.assertIn("### REF-999", rendered)
self.assertIn("[Canonical record](../references/REF-999.md)", rendered)
self.assertLess(rendered.index("- **Source:**"), rendered.index("- **Source type:**"))
self.assertLess(rendered.index("## Active References"), rendered.index("## Deprecated References"))
self.assertIn("- **Deprecation reason:** Superseded", rendered)
self.assertIn("- **Replaced by:** [REF-1000](#ref-1000)", rendered)
```

- [ ] **Step 5: Implement the reference renderer and run renderer tests**

Render each reference with `### REF-*` as its own heading, then the canonical link, title, authors, year, source, source type, optional design/DOI/PMID, URLs, Supports, and lifecycle metadata. Run:

```powershell
python -m unittest tests.test_views -v
```

Expected: all renderer tests pass.

- [ ] **Step 6: Commit the pure renderers**

```powershell
git add qol_kb/views.py tests/test_views.py
git commit -m "feat: render deterministic knowledge views"
```

### Task 3: Write and drift-check command

**Files:**
- Modify: `qol_kb/views.py`
- Modify: `tests/test_views.py`

**Interfaces:**
- Consumes: `load_repository(root)` plus both render functions.
- Produces: `generate_views(root: str | Path) -> dict[Path, bytes]`, `write_views(root: str | Path) -> None`, `check_views(root: str | Path) -> tuple[Path, ...]`, and `main(argv: list[str] | None = None) -> int`.
- CLI: `python -m qol_kb.views [--root PATH] [--check]`.

- [ ] **Step 1: Write failing filesystem and CLI tests**

Use a temporary repository with a valid `categories.yaml` and no record directories. Assert:

```python
self.assertEqual(views.main(["--root", str(root)]), 0)
self.assertTrue((root / "generated" / "catalog.md").is_file())
self.assertTrue((root / "generated" / "references.md").is_file())
self.assertEqual(views.main(["--root", str(root), "--check"]), 0)
```

Then modify catalog output and remove reference output. Capture stderr, run `--check`, assert exit `1`, both relative paths reported, the modified catalog remains byte-for-byte unchanged, and the missing reference file remains absent. Add an invalid-root case expecting exit `2` and an `error:` prefix.

- [ ] **Step 2: Run CLI tests and confirm missing functions**

Run:

```powershell
python -m unittest tests.test_views.DeterministicViewTests.test_cli_write_and_check -v
```

Expected: failure because the write/check API does not exist.

- [ ] **Step 3: Implement generation, writing, checking, and CLI exit codes**

Use repository-relative output paths and bytes:

```python
OUTPUT_PATHS = {
    Path("generated/catalog.md"): render_catalog,
    Path("generated/references.md"): render_references,
}


def generate_views(root: str | Path) -> dict[Path, bytes]:
    snapshot = load_repository(root)
    return {
        relative_path: renderer(snapshot).encode("utf-8")
        for relative_path, renderer in OUTPUT_PATHS.items()
    }


def check_views(root: str | Path) -> tuple[Path, ...]:
    root_path = Path(root)
    expected = generate_views(root_path)
    return tuple(
        relative_path
        for relative_path, expected_bytes in expected.items()
        if not (root_path / relative_path).is_file()
        or (root_path / relative_path).read_bytes() != expected_bytes
    )
```

`write_views` creates parent directories and writes expected bytes. `main` parses arguments, catches `OSError` and `ValueError` as exit `2`, prints all drift paths and returns `1`, otherwise returns `0`. End the module with `raise SystemExit(main())`.

- [ ] **Step 4: Run CLI and full unit tests**

Run:

```powershell
python -m unittest tests.test_views -v
python -m unittest discover -s tests -v
```

Expected: all tests pass.

- [ ] **Step 5: Commit drift detection**

```powershell
git add qol_kb/views.py tests/test_views.py
git commit -m "feat: detect generated view drift"
```

### Task 4: Commit initial generated views and contributor documentation

**Files:**
- Create: `generated/catalog.md`
- Create: `generated/references.md`
- Modify: `README.md`
- Modify: `tests/test_views.py`

**Interfaces:**
- Consumes: `python -m qol_kb.views` and `python -m qol_kb.views --check`.
- Produces: committed baseline artifacts and documented contributor commands.

- [ ] **Step 1: Add a failing repository-output integration test**

Add a test that identifies the repository root from `tests/test_views.py`, calls `check_views(root)`, and expects no drift:

```python
def test_committed_repository_views_have_no_drift(self) -> None:
    root = Path(__file__).resolve().parents[1]
    self.assertEqual(views.check_views(root), ())
```

- [ ] **Step 2: Run it and confirm both generated outputs are missing**

Run:

```powershell
python -m unittest tests.test_views.DeterministicViewTests.test_committed_repository_views_have_no_drift -v
```

Expected: failure listing `generated/catalog.md` and `generated/references.md`.

- [ ] **Step 3: Generate the committed baseline**

Run:

```powershell
python -m qol_kb.views
```

Inspect both outputs. `generated/catalog.md` must contain the four Active categories from `categories.yaml` and fixed empty states for Active and Deprecated items. `generated/references.md` must contain fixed empty states for both lifecycle sections.

- [ ] **Step 4: Document transitional ownership and commands**

Update `README.md` so the repository map labels root `catalog.md` and `references.md` as legacy during migration, adds the two generated views as derived previews, identifies `categories.yaml`, `items/*.md`, and `references/*.md` as canonical structured sources as they are migrated, and documents:

```powershell
python -m qol_kb.views
python -m qol_kb.views --check
```

State explicitly that files under `generated/` must not be edited manually.

- [ ] **Step 5: Verify determinism and the complete suite**

Run write mode twice and verify Git reports no generated-file changes after the second run. Then run:

```powershell
python -m qol_kb.views --check
python -m unittest discover -s tests -v
git diff --check
```

Expected: check exits `0`, all tests pass, and `git diff --check` emits no errors.

- [ ] **Step 6: Commit the integration**

```powershell
git add README.md generated/catalog.md generated/references.md tests/test_views.py
git commit -m "docs: publish generated knowledge views"
```

### Task 5: Final acceptance verification

**Files:**
- Verify only.

**Interfaces:**
- Verifies all issue #4 acceptance criteria against committed state.

- [ ] **Step 1: Run final acceptance commands**

```powershell
python -m qol_kb.views --check
python -m unittest discover -s tests -v
git diff --check
git status --short
```

Expected: check exits `0`, all tests pass, no whitespace errors, and the worktree is clean.

- [ ] **Step 2: Review the branch diff**

```powershell
git diff --stat domain-model-context...HEAD
git diff domain-model-context...HEAD
```

Confirm that root legacy registries are unchanged, no generated metadata is parsed as input, output ordering has no timestamps or environment state, and every acceptance criterion has direct test coverage.
