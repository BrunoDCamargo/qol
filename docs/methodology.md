# QoL Knowledge Base methodology

This document records methodological rules that sit above individual `QOL-*` evidence reviews and describes how the private Personal QoL Profile may apply the knowledge base without changing its evidence.

## Coverage frameworks

The repository uses external structured models to audit whether important quality-of-life domains or facets are represented. These models are **Coverage Frameworks**, not automatic causal evidence for interventions.

### Primary framework

Use **WHOQOL-100** as the primary coverage framework because its multidomain facet structure is suitable for identifying blind spots in the catalog.

Use **WHOQOL-BREF** as a compact companion when a shorter multidomain assessment view is useful.

Other frameworks may be added when they contribute nonredundant coverage insight. The repository is not ontologically bound to WHOQOL alone.

## Coverage audit

A Coverage Audit compares a Coverage Framework with the current `QOL-*` catalog and classifies each relevant domain or facet as, for example:

- strong coverage;
- partial coverage;
- weak or absent coverage.

Coverage status is editorial and should be revisited when the catalog changes.

A coverage gap is a **research trigger**, not a new QoL Item by itself.

## Separation from proposition evidence

Coverage and causal support answer different questions:

- **Coverage evidence:** what aspects of quality of life should remain visible when auditing the knowledge base?
- **Proposition evidence:** what evidence supports or constrains a particular Intervention, Assessment, or Guardrail?

A Coverage Framework may reveal that a construct such as self-esteem, leisure, access to care, or meaning is underrepresented. It does not by itself establish which intervention should be used or what Evidence Strength a future item should receive.

Do not cite a Coverage Framework as the sole Support Claim for a causal intervention unless the framework itself directly provides the evidence required for that proposition.

## Expansion workflow

Use this sequence for coverage-driven expansion:

```text
Coverage Framework
       |
       v
Coverage Audit
       |
       v
Missing or partial facet
       |
       v
Focused Research
       |
       +--> no reusable decision proposition --> document the gap
       |
       +--> reusable decision proposition
                  |
                  v
      Intervention / Assessment / Guardrail
                  |
                  v
          Evidence Claims + References
                  |
                  v
                 QOL-*
```

Before assigning a new `QOL-*` identity:

1. confirm the concept is not already represented by an existing item;
2. formulate one decision-relevant proposition rather than a broad topic;
3. gather evidence appropriate to that proposition;
4. define Applicability and Support Mode;
5. add Support and Constraint Claims no broader than the reviewed evidence;
6. use existing Categories where they fit, and create a new Category only when retrieval semantics truly require one.

## Personal application methodology

The private `personal/` bounded context applies the knowledge base to the repository owner's life. It is intentionally separate from the canonical evidence model.

A personal audit should preserve at least these distinctions when relevant:

- **Personal Observation** — current factual state;
- **subjective satisfaction** — how the current state feels to the person;
- **Personal Position** — importance, desirability, willingness, or preference;
- **Personal Target** — chosen next state and longer-term direction;
- **Personal Priority** — personal sequencing of changes;
- **Accepted Trade-off** — deliberate nonoptimization because another value or constraint takes precedence.

Do not collapse these into one score. A person can satisfy an evidence-backed behavior and still be dissatisfied, or knowingly choose not to optimize one dimension because another valued outcome matters more.

### Applying `QOL-*` items personally

Personal records may reference `QOL-*` identities and use application-layer statuses such as:

- `meets`;
- `partial`;
- `does_not_meet`;
- `not_applicable`;
- `unknown`.

These statuses describe the person's current relationship to the item. They do not alter the canonical item, Evidence Strength, Support Mode, or applicability semantics.

Conditional items should normally be opened by trigger questions rather than assumed applicable. When an item is not applicable, the profile should record that instead of treating it as a failure.

### Evidence priority versus personal priority

Keep at least two concepts distinct:

- **evidence/clinical relevance** — how strongly a proposition is supported or how important a condition may be from a health perspective;
- **personal priority** — what the person wants to address first.

A lower personal priority does not invalidate evidence relevance. Conversely, high personal importance does not strengthen scientific evidence.

### Coverage frameworks in personal audits

Coverage Frameworks may guide broad questioning so that the personal profile does not silently omit major QoL domains. WHOQOL facets can therefore be recorded as coverage observations even when no current `QOL-*` exists.

A WHOQOL facet is not automatically a personal problem. The purpose of the coverage pass is to ask whether the domain matters, not to assume a deficit.

## Sensitive personal context

Because this repository is private and personally owned, the `personal/` context may deliberately retain private health, medication, relationship, work, financial, or lifestyle information when it materially improves interpretation of applicability, targets, or trade-offs.

Guardrails:

- keep sensitive information under `personal/`;
- do not convert personal observations into Evidence Claims or general recommendations;
- do not infer treatment adequacy, diagnosis changes, or medication changes from the profile;
- remember that Git history may retain sensitive content after ordinary deletion;
- record only information the repository owner has deliberately chosen to persist.

## Scoring guardrail

Do not infer a validated WHOQOL score from unrelated interview questions or from an informal personal profile. A validated instrument score requires administration and scoring according to the applicable instrument methodology.

The personal profile may use labels such as `meets`, `partial`, or subjective satisfaction categories for internal organization, but these are not WHOQOL scores and are not universal cross-domain metrics.

## Current research and profile records

- `docs/research/whoqol-coverage-audit-2026-09-15.md` — first WHOQOL-based knowledge-base coverage audit and research questions exposed by it.
- `personal/PROFILE.md` — current human-readable personal profile snapshot.
- `personal/observations.yaml` — structured current observations.
- `personal/targets.yaml` — chosen next states and longer-term directions.
- `personal/priorities.yaml` — explicit rankings and important unranked domains.
- `personal/tradeoffs.yaml` — constraints, preferences, and accepted trade-offs.
