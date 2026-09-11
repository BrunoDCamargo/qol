# ADR 0001: Use structured records as the canonical knowledge source

## Status

Accepted

## Decision

QoL Items, References, and Implementation Options use individual Markdown files with validated YAML front matter as canonical records. Categories use `categories.yaml`, and editorial Topic View membership uses `topic-views.yaml`.

Catalogs, reference indexes, implementation indexes, and Topic View `## Map` blocks are derived from validated canonical state. Generated Markdown is never an editable source of canonical metadata.

The former monolithic root `catalog.md` and `references.md` registries have been retired.

## Rationale

The domain requires machine-checkable identity, lifecycle, evidence, applicability, relationships, implementation links, and reference integrity without multiple editable sources of truth. Stable per-record identities allow records to evolve or be Deprecated while remaining resolvable, and deterministic views provide human-readable navigation without duplicating authority.

## Consequences

Contributors edit canonical records or registries and regenerate views. Topic prose may remain editorial, but canonical map metadata is generated. Repository validation must resolve cross-record links and lifecycle rules before generated output is accepted.
