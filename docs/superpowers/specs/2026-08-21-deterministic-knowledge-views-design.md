# Deterministic Knowledge Views Design

## Context

GitHub issue #4 introduces generated, human-readable views over canonical QoL Item, Reference, and category records. The repository is still migrating from the hand-maintained `catalog.md` and `references.md`, so this increment must establish generation and drift detection without replacing those legacy registries. The generated views must remain derived artifacts rather than editable metadata stores.

## Goals

- Load a validated repository into one immutable snapshot shared by validation and generation.
- Generate a catalog-style item view and a reusable reference view under `generated/`.
- Expose Active identities in the primary view and preserve Deprecated identities separately.
- Show item Evidence Strength only as the value derived from Support Claims.
- Produce byte-stable UTF-8 Markdown for unchanged canonical inputs.
- Provide a verification command that reports missing or stale generated files and exits unsuccessfully without writing.

## Non-goals

- Replacing the legacy root `catalog.md` or `references.md`; that cutover belongs to issue #14.
- Migrating legacy items or references into canonical per-record files.
- Generating Topic Views.
- Adding CI integration; issue #5 will invoke the verification command.
- Introducing a template engine or a new runtime dependency.

## Architecture

`qol_kb.records` gains a frozen `RepositorySnapshot` containing canonical categories, items, and references. `load_repository(root)` loads every canonical source once, applies the existing schema and cross-record invariants, sorts item and reference identities, and returns the snapshot. `validate_repository(root)` remains backward compatible by delegating to `load_repository(root)` and discarding the result.

`qol_kb.views` owns pure Markdown rendering and the filesystem boundary. `render_catalog(snapshot)` and `render_references(snapshot)` return complete strings without reading files, using the snapshot's already-derived item Evidence Strength. A small command-line entry point in the same module either writes both files or compares their expected UTF-8 bytes with the committed artifacts.

The dependency direction is one-way:

```text
canonical files -> qol_kb.records -> RepositorySnapshot -> qol_kb.views -> generated Markdown
```

Generated Markdown is never parsed back into canonical state.

## Repository snapshot

`RepositorySnapshot` contains:

- `categories: tuple[Category, ...]`
- `items: tuple[Record, ...]`
- `references: tuple[Record, ...]`

Tuples prevent callers from changing collection membership. Records and categories are already frozen dataclasses. Categories are ordered by name. Items and references are ordered by their numeric identifier suffix, so `QOL-999` precedes `QOL-1000` and the result does not depend on filesystem enumeration.

`load_repository` permits absent `items/` and `references/` directories during migration, but still requires and validates `categories.yaml`. It rejects all invalid schemas, duplicate IDs, unresolved references or relationships, illegal lifecycle links, and invalid Active-category usage before returning a snapshot.

## Generated files

Generation writes exactly two committed artifacts:

- `generated/catalog.md`
- `generated/references.md`

Each begins with an HTML comment identifying the command that generated it and warning contributors not to edit it. The files use UTF-8, LF line endings, a fixed section and field order, exactly one trailing newline, and no timestamps or environment-dependent paths.

Markdown table cells normalize embedded line breaks to spaces and escape backslashes and pipe characters. Identity links use repository-relative paths only.

### Catalog view

`generated/catalog.md` contains, in order:

1. Active categories, sorted by name, with definition.
2. Deprecated categories, sorted by name, with definition and optional Active replacement.
3. Active QoL Items, sorted by numeric ID, with ID, statement, kind, categories, derived Evidence Strength, applicability, support mode, and referenced `REF-*` identities.
4. Deprecated QoL Items, sorted by numeric ID, with ID, statement, deprecation reason, and replacement `QOL-*` identities.

Active item IDs link to their canonical `../items/QOL-*.md` files. Reference identities link to anchors in `generated/references.md`. Empty sections contain fixed explanatory text rather than disappearing.

The Evidence Strength column reads `Record.evidence_strength`, which is derived by `qol_kb.records` from the weakest Support Claim. The renderer does not inspect Constraint Claims or accept an independently stored strength.

### Reference view

`generated/references.md` contains Active and Deprecated sections, each sorted by numeric ID. Every reference has a stable standalone `REF-*` heading so catalog links resolve. Its entry renders title, authors, year, source, source type, optional design, DOI and PMID, URLs, and supported claim boundaries in a fixed order. Deprecated entries additionally render deprecation reason and optional replacement.

## Command-line interface

From the repository root:

```powershell
python -m qol_kb.views
python -m qol_kb.views --check
```

`--root PATH` overrides the repository root for tests and automation; it defaults to the current directory.

Write mode validates and renders both views, creates `generated/` if needed, and writes the expected bytes. Check mode performs the same validation and rendering entirely in memory, compares both committed files byte-for-byte, and never modifies the filesystem. It exits `0` only when both files match. Missing or different files are listed on standard error using repository-relative paths and cause exit code `1`. Invalid canonical input or filesystem errors produce a concise error on standard error and exit code `2`.

## Migration behavior

Until issue #14, root `catalog.md` and `references.md` remain untouched legacy registries. The generated views reflect only canonical records already present under `items/` and `references/`; therefore the initial generated item and reference sections are valid empty states. The category sections are populated immediately from `categories.yaml`.

README documentation distinguishes the two sets, identifies the canonical per-record sources, and gives the generation and verification commands. Editing a generated file is allowed mechanically but will be overwritten by write mode and rejected by check mode.

## Error handling

- Canonical validation errors retain their existing source path and invariant details.
- A write failure identifies the affected path and returns exit code `2` without claiming success.
- Check mode reports every missing or stale generated file in one run.
- Rendering functions rely only on validated snapshots; malformed raw dictionaries are not a supported public interface.

## Testing

Tests use temporary repositories and standard-library `unittest`:

- repository loading returns one ordered frozen snapshot while preserving every existing invariant;
- item and category lifecycle sections are separated correctly;
- displayed Evidence Strength comes from the weakest Support Claim and ignores Constraint Claims;
- reference entries expose reusable metadata and lifecycle details with stable anchors;
- Markdown escaping, numeric ID ordering, empty sections, LF endings, and repeat rendering are deterministic;
- write mode creates both expected files;
- check mode passes unchanged, reports all missing or modified outputs, performs no writes, and returns the specified exit codes;
- the full existing suite remains green.
