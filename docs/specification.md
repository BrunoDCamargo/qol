# Repository Specification

This document defines the normative repository contract. Domain terms are defined in `CONTEXT.md`; schemas provide machine-checkable field constraints.

## Canonical identities

The canonical record families are:

- `QOL-*`: one QoL Item proposition;
- `REF-*`: one citably distinct Reference or materially relevant source version;
- `IMP-*`: one concrete reusable Implementation Option.

Identities are stable and must not be reassigned to different concepts.

## QoL Items

A QoL Item represents one decision-relevant proposition. Its Item Kind is Intervention, Assessment, or Guardrail.

Every Active QoL Item must have the Support Claims required by the schema. Conditional items must state the condition that makes them relevant. Categories are retrieval metadata and must resolve through the Category registry.

Evidence Claims have a role of Support or Constraint. Evidence Strength is `High`, `Moderate`, or `Low`. Item-level displayed strength is derived from the weakest Support Claim needed to justify the proposition.

Support Mode is independent of Evidence Strength. `Direct` means the cited evidence supports the proposition directly; `Inferred` means the proposition applies broader evidence by inference.

## References

A Reference is reusable evidence metadata with a stable `REF-*` identity. Evidence Claims may cite only resolvable References. Active QoL Items must not depend on Deprecated References as current support.

Reference lifecycle transitions preserve identity. A Deprecated Reference records its reason and may identify a valid Active replacement when the schema permits one.

## Implementation Options

An Implementation Option is a concrete reusable way to enact one or more QoL Items. It has a stable `IMP-*` identity and an acquisition mode allowed by its schema.

An Active Implementation Option must implement at least one resolvable Active QoL Item. The option does not acquire independent causal evidence merely because the parent QoL Item is evidence-backed. Deprecated options preserve identity and may link to valid Active replacements.

## Implementation Selection Guides

An Implementation Selection Guide is a non-canonical editorial aid for comparing concrete products or providers inside one existing Implementation Option class.

A Selection Guide does not receive a stable identity, does not alter the parent `IMP-*` record, and does not contribute Evidence Claims or Evidence Strength to a `QOL-*` item. Product-testing sources cited by a guide support product-selection judgments only unless they separately satisfy the evidence requirements for a canonical QoL claim.

Selection Guides may describe context modifiers, must-have criteria, performance criteria, safety or disqualifying conditions, usability, reliability, maintenance, recurring costs, privacy, connectivity, and other category-specific trade-offs.

Stable selection criteria must remain distinct from volatile market data. Named products, providers, prices, stock, firmware, and similar market details may appear in optional dated and region-specific market snapshots. These snapshots are editorial content rather than canonical identities.

The repository does not define a universal score across unrelated Implementation Options. Any future numeric scoring must be category-specific, method-versioned, and reproducible.

## Categories

Categories are canonical retrieval tags, not exclusive ownership containers. Active QoL Items may use only Active registered Categories. Category lifecycle changes do not change QoL Item identities.

## Item Relationships

Item Relationships are typed directed edges between distinct resolvable QoL Items. `informs` means the source item provides information useful for deciding or applying the target item. Relationship direction must be semantically defensible and does not change either identity.

## Topic Views

Topic Views are non-canonical presentations. `topic-views.yaml` defines editorial membership. Topic Markdown contains editorial prose.

The complete `## Map` block of every Topic View is generated from canonical records. Generated rows include canonical identity, statement, Item Kind, Categories, Evidence Strength, Applicability, Support Mode, lifecycle status, and Reference links. Direct edits to generated map metadata must be detected as drift.

Topic links to individual QoL Items and References resolve directly to canonical record files. Retired monolithic `catalog.md` and `references.md` paths are not supported.

## Generated indexes

`generated/catalog.md`, `generated/references.md`, and `generated/implementation-options.md` are deterministic derived views. They are not editable knowledge sources. A generated view must be reproducible byte-for-byte from the same validated canonical inputs.

## Lifecycle

Canonical records use Active and Deprecated lifecycle states. Deprecation preserves the old identity rather than deleting it or reusing it for another concept. Replacement links must resolve according to the applicable schema and repository invariants.

Every `QOL-*` and `REF-*` identity emitted by current generated or Topic View output must resolve to its canonical record under this lifecycle model.

## Repository scope

The repository stores general knowledge and reusable implementation classes. It must not store personal audit answers, individualized rankings, private health or medication histories, employment histories, purchase histories, or conclusions about a specific person's diagnosis, treatment, or quality of life.

## Release requirements

A releasable revision must satisfy all of the following:

1. every canonical file validates against its schema and semantic invariants;
2. all category, evidence, replacement, Implementation Option, and Item Relationship links resolve with valid lifecycle states;
3. all emitted `QOL-*` and `REF-*` identities remain resolvable;
4. deterministic generated output matches the committed output with no drift;
5. the complete structural test suite passes.

These checks establish structural correctness. They do not substitute for human review of scientific claims, evidence interpretation, Selection Guide methodology, or editorial quality.
