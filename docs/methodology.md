# QoL Knowledge Base methodology

This document records methodological rules that sit above individual `QOL-*` evidence reviews.

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

## Personal audits

Personal profiles may use the catalog and Coverage Frameworks to guide questioning, but personal answers are outside repository scope.

Do not store in this repository:

- personal audit responses;
- individualized priority rankings;
- diagnoses or private health histories;
- medication histories;
- employment or purchase histories;
- individualized treatment conclusions.

A personal audit may reference stable `QOL-*` identities externally, but the canonical knowledge base remains general and reusable.

## Scoring guardrail

Do not infer a validated WHOQOL score from unrelated interview questions or from an informal personal profile. A validated instrument score requires administration and scoring according to the applicable instrument methodology.

## Current research record

See `docs/research/whoqol-coverage-audit-2026-09-15.md` for the first WHOQOL-based coverage audit and research questions exposed by it.
