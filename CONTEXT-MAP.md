# Context Map

This repository contains two bounded contexts with different authority and data rules.

## QoL Knowledge Base

**Context file:** `CONTEXT.md`

**Primary paths:** `items/`, `references/`, `implementation-options/`, `categories.yaml`, `topic-views.yaml`, `topics/`, `docs/`, `generated/`, `qol_kb/`.

Owns general, reusable, evidence-backed knowledge about quality of life. `QOL-*`, `REF-*`, and `IMP-*` identities belong only to this context. Scientific Evidence Claims, Evidence Strength, Support Mode, Categories, lifecycle state, and generated indexes are determined only from this context.

## Personal QoL Profile

**Context file:** `personal/CONTEXT.md`

**Primary path:** `personal/`.

Owns the repository owner's personal observations, preferences, targets, priorities, accepted trade-offs, and health or life context used to interpret applicability. It may reference `QOL-*` identities and Coverage Framework facets, but personal data never becomes Support or Constraint evidence for the QoL Knowledge Base.

## Relationship

The dependency is one-way:

```text
QoL Knowledge Base
       |
       | QOL-* references / general evidence
       v
Personal QoL Profile
```

The Personal QoL Profile may apply, prioritize, or consciously decline general propositions. The QoL Knowledge Base must not derive canonical propositions, Evidence Strength, reference metadata, or generated catalog state from the personal profile.
