# Architecture

## Source-of-truth boundary

The repository has one editable source for each kind of canonical knowledge:

- `items/QOL-*.md` stores QoL Item records;
- `references/REF-*.md` stores Reference records;
- `implementation-options/IMP-*.md` stores Implementation Options;
- `categories.yaml` stores Category definitions;
- `topic-views.yaml` stores editorial Topic View membership.

Topic Markdown contains editorial prose, but its complete `## Map` block is derived. Files under `generated/` are also derived. The retired root `catalog.md` and `references.md` registries are not part of the architecture.

## Validation and snapshot

`qol_kb.records` loads schema-validated canonical sources into one immutable `RepositorySnapshot`. Loading enforces identity, lifecycle, category, evidence-reference, replacement, relationship, and Implementation Option integrity before a snapshot is returned.

The validator rejects unresolved or invalid cross-record links. This means generation never needs to compensate for malformed canonical state.

## Generated views

`qol_kb.views` consumes a validated snapshot and produces deterministic Markdown:

```text
canonical records + categories.yaml
              |
              v
       qol_kb.records
              |
              v
     RepositorySnapshot
              |
       +------+------+
       |             |
       v             v
 generated/      Topic View maps
 indexes         + canonical links
```

The full QoL catalog, Reference index, and Implementation Option index are generated under `generated/`. Topic membership comes from `topic-views.yaml`; canonical row metadata comes from the snapshot; editorial prose remains in `topics/*.md`.

Generated Markdown is never parsed back into canonical state.

## Topic View boundary

A Topic View is a presentation, not a knowledge registry. Contributors choose which QoL identities belong in a topic and may edit explanatory prose. The generator rebuilds the complete `## Map` table from canonical records, including identity, statement, Item Kind, Categories, Evidence Strength, Applicability, Support Mode, lifecycle status, and Reference links.

Links to individual QoL Items and References resolve to the canonical record files. Retired monolithic registry links are rejected rather than silently normalized.

## Lifecycle and identity resolution

Canonical identities remain addressable when Deprecated. Active records may only depend on lifecycle-compatible records defined by the specification and schemas. Replacement links and typed Item Relationships must resolve before generation succeeds.

## Release boundary

The release gate has three structural responsibilities:

1. load and validate the complete canonical repository, including cross-record integrity;
2. verify deterministic generated output has no drift;
3. run the full structural test suite.

Scientific interpretation remains a human review responsibility outside the structural gate.
