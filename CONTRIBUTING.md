# Contributing

This file defines the contributor workflow for the current canonical architecture.

## Authority hierarchy

Use these sources for different questions:

1. `CONTEXT.md` defines canonical domain language.
2. `docs/specification.md` defines normative repository behavior and invariants.
3. `docs/architecture.md` describes the current technical arrangement and data flow.
4. `CONTRIBUTING.md` defines the contribution and release procedure.
5. `docs/adr/` records architectural decisions and their rationale.

The README is an entry point, not a second normative specification.

## Editable sources

Edit knowledge only at its authoritative source:

- `items/` for `QOL-*` Item records;
- `references/` for `REF-*` Reference records;
- `implementation-options/` for `IMP-*` Implementation Options;
- `categories.yaml` for Category definitions;
- `topic-views.yaml` for editorial Topic View membership;
- prose outside the generated `## Map` block in `topics/` for editorial explanation;
- `docs/selection-guides/` for non-canonical product or provider selection guidance linked to an Implementation Option.

Files under `generated/` and the `## Map` blocks inside Topic Views are derived output. Do not maintain canonical metadata there.

## Evidence vocabulary

Evidence Strength expresses confidence in an Evidence Claim and has exactly three values: `High`, `Moderate`, and `Low`.

Support Mode records whether a QoL Item is supported `Direct`ly or applies broader evidence by inference with `Inferred`. `Inferred` is a Support Mode, not an Evidence Strength.

Keep claims no broader than their References support. Prefer primary research, current official guidance, regulators, standards bodies, or other first-party scientific sources when available. Reuse an existing `REF-*` record when it already identifies the relevant source.

## Stable identities and lifecycle

`QOL-*`, `REF-*`, and `IMP-*` identities are stable. Do not renumber or reuse an identity because ordering, categories, evidence, or presentation changes.

Canonical records are `Active` or `Deprecated`. Preserve Deprecated identities so historical references remain resolvable. When a replacement exists, use the lifecycle fields permitted by the relevant schema and ensure the replacement resolves to the appropriate Active record.

Active QoL Items may use only Active Categories and Active References. Active Implementation Options must implement Active QoL Items. Item relationships must target existing distinct QoL Items.

Implementation Selection Guides are not canonical identities and do not use the Active/Deprecated lifecycle in the first implementation.

## Adding or revising a QoL Item

1. Check whether the proposition already exists.
2. Assign the next unused `QOL-*` identity only for a genuinely new proposition.
3. Choose the correct Item Kind: Intervention, Assessment, or Guardrail.
4. State applicability and any required condition explicitly.
5. Add narrow Support and Constraint Claims with appropriate References.
6. Set Evidence Strength on claims conservatively and set Support Mode separately.
7. Apply registered Categories that improve retrieval.
8. Add or revise typed Item Relationships only when their direction is defensible.
9. Add the item to `topic-views.yaml` when it belongs in an editorial Topic View.

## Adding or revising a Reference

Create or reuse a `REF-*` record for a citably distinct source or materially relevant version. Record the narrow boundaries of what the source supports. Keep lifecycle changes explicit instead of deleting or silently replacing an identity.

## Adding or revising an Implementation Option

An Implementation Option is a concrete reusable way to enact one or more existing QoL Items. It does not inherit product-level causal evidence merely by implementing an evidence-backed proposition.

Use a stable `IMP-*` identity, link the Active QoL Items it implements, choose the permitted acquisition mode, and describe a reusable class of solution rather than an unsupported vendor endorsement.

## Adding or revising an Implementation Selection Guide

Use a Selection Guide when concrete products or providers inside an `IMP-*` class differ enough that selection criteria affect real-world usefulness, safety, maintenance burden, cost, or reliability.

1. Link the guide to one existing Active Implementation Option.
2. Keep the parent `IMP-*` record vendor-neutral and reusable.
3. Start with authoritative standards, regulators, certification programs, or first-party technical sources for criteria they define.
4. Use transparent independent product-testing methods to supplement those sources with comparative performance, usability, and reliability information.
5. Keep product-selection evidence separate from `QOL-*` causal evidence.
6. State context modifiers and disqualifying conditions before secondary feature preferences.
7. Separate stable criteria from market-specific recommendations.
8. Date and region-label any market snapshot that names products, providers, or prices.
9. Record the guide's last-review date and revisit it when the parent `IMP-*`, testing method, safety guidance, or market changes materially.

Do not create a universal score across unrelated Implementation Options. Avoid using isolated customer reviews as if they were controlled evidence or representative reliability data.

## Topic Views

`topic-views.yaml` owns Topic View membership. Topic Markdown owns editorial prose. The generator owns each complete `## Map` block. Links to individual `QOL-*` and `REF-*` records must resolve directly to canonical files; retired monolithic registry paths are not supported.

After changing canonical records, topic membership, or Topic View prose, regenerate views before committing.

Selection Guide edits do not require generated-view changes unless a canonical record or Topic View also changed.

## Release gate

From the repository root, run:

```powershell
python -c "from qol_kb.records import validate_repository; validate_repository('.')"
python -c "from qol_kb.career_radar import validate_career_radar; validate_career_radar('.')"
python -m qol_kb.views
python -m qol_kb.views --check
python -m unittest discover -s tests
```

Career Radar validation is structural and offline. Contributors verify link freshness and any `remote-brazil` eligibility against institutional sources during curation.

The repository is releasable only when canonical validation succeeds, every cross-reference and lifecycle invariant resolves, generated output has no drift, and the full test suite passes. Structural automation does not replace human review of scientific claims or Selection Guide methodology.
