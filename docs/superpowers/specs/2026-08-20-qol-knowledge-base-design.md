# QoL Knowledge Base Design

Date: 2026-08-20

## Purpose

Create a growing, evidence-oriented knowledge base of factors, interventions, conditions, and practical changes that may affect quality of life.

The repository stores general knowledge only. It must not contain Bruno's personal audit, personal rankings, health history, medication history, work situation, or other individualized conclusions from the conversation that originated this project.

The primary unit of knowledge is a **QoL item**: one clearly stated factor or intervention paired with the evidence and references that support it.

## Design goals

1. Make the full map easy to scan.
2. Preserve the origin of factual claims and practical recommendations.
3. Support continued growth beyond the initial 100 items.
4. Allow an item to belong to multiple categories.
5. Allow new categories to appear without restructuring existing content.
6. Separate scientific evidence from practical inference.
7. Prefer primary sources and make evidence limitations visible.
8. Keep item identifiers stable even when rankings, categories, or organization change.
9. Avoid storing personalized QoL assessments in this repository.

## Repository structure

```text
qol/
├── README.md
├── catalog.md
├── topics/
│   ├── sleep.md
│   ├── physical-activity.md
│   ├── nutrition-weight.md
│   ├── mental-health.md
│   ├── attention-digital.md
│   ├── work-time.md
│   ├── environment.md
│   ├── social-relationships.md
│   └── health-checks.md
├── references.md
└── docs/
    └── superpowers/
        └── specs/
            └── 2026-08-20-qol-knowledge-base-design.md
```

The initial `topics/` files are starting points, not a closed taxonomy. New topic files may be created whenever a meaningful cluster of items becomes large enough to deserve its own page.

## Flexible taxonomy

Categories are **tags**, not exclusive containers.

A QoL item may belong to zero, one, or several categories. For example:

```text
QOL-023  Walking outdoors
Categories: physical-activity, sleep, environment, mental-health
```

The canonical identity of the item is `QOL-023`, not its category or file location.

This avoids coupling the knowledge model to the initial folder structure. If a future category such as `financial-wellbeing`, `pain`, `relationships`, `neurodiversity`, `aging`, or `work-design` becomes useful, it can be introduced without migrating existing identifiers.

Categories should be created when they improve retrieval or understanding, not merely because one item could plausibly receive another label.

## Canonical catalog

`catalog.md` is the canonical high-level index.

Each item contains at least:

| Field | Purpose |
|---|---|
| ID | Stable identifier, e.g. `QOL-001` |
| Item | Short description of the factor/intervention |
| Categories | One or more flexible category tags |
| Evidence | Evidence-strength classification |
| Applicability | Whether the item is general or conditional |
| Primary references | One or more `REF-*` identifiers |

The order of the catalog is organizational rather than permanent ranking. A future ranking or view may reorder items without changing their IDs.

## Item detail format

Detailed topic pages use the following conceptual schema:

```markdown
## QOL-XXX — Item name

**Categories:** category-a, category-b
**Evidence:** High | Moderate | Low | Inference
**Applicability:** General | Conditional

### Idea

Short, precise description of the intervention or factor.

### Why it may affect quality of life

Mechanism or causal rationale, written conservatively.

### Evidence

What the cited research actually found. Distinguish measured outcomes from interpretation.

### Practical applications

Examples of ways the evidence might be applied.

Explicitly label extrapolations when a practical example was not directly tested.

### Limitations and caveats

Population limits, study-size limitations, adherence issues, conflicting evidence, contraindications, and uncertainty.

### References

- REF-XXX
```

Not every item needs a long page. Small or well-established items may initially exist only in `catalog.md` and gain detail when useful.

## Evidence classification

Use a small, conservative vocabulary:

### High

Strong guideline support, multiple high-quality randomized trials, systematic evidence with consistent findings, or another comparably strong evidence base.

### Moderate

At least one useful randomized trial or a consistent body of evidence with meaningful limitations in replication, population, size, adherence, or generalizability.

### Low

Small studies, observational evidence, inconsistent findings, indirect evidence, or substantial uncertainty.

### Inference

The practical proposal follows reasonably from another established finding but has not itself been adequately tested.

Evidence strength describes confidence in the claim, not expected effect size.

## Applicability classification

Use at least two applicability labels:

- **General**: can reasonably apply to broad populations, subject to normal caveats.
- **Conditional**: potentially useful only when a specific deficit, symptom, exposure, diagnosis, or circumstance exists.

Examples:

- Regular physical activity can be broadly applicable.
- Treating sleep apnea is conditional on having sleep apnea.
- HEPA filtration is conditional on meaningful particulate exposure or another relevant indication.

This prevents large conditional effects from being presented as universal recommendations.

## References

`references.md` stores reusable bibliographic records with stable IDs.

Example:

```markdown
## REF-001

Whillans AV, Dunn EW, Smeets P, Bekkers R, Norton MI.
Buying time promotes happiness.
Proceedings of the National Academy of Sciences. 2017.

- Type: primary research
- Design: observational studies + randomized crossover experiment
- DOI: ...
- PMID: ...
- URL: ...
```

An item may cite several references, and a reference may support several items.

When possible, references should point to the primary paper, official guideline, government publication, regulator, standards body, or first-party scientific source rather than a secondary article describing it.

## Evidence versus practical inference

The repository must explicitly distinguish what was tested from how someone might use the finding.

Example:

**Evidence:** participants randomized to spend money on a time-saving purchase reported less time pressure and better affect than when spending the same amount on a material purchase.

**Practical inference:** hiring a cleaner, ordering groceries, or buying prepared meals may be ways to apply that principle when those activities actually save unwanted time.

The second statement must not be written as though each concrete service had independently demonstrated the same causal effect.

## Growth model

The initial 100 QoL items are a seed dataset, not a target size or closed list.

Future work may:

- add new QoL items;
- add new references;
- split broad items into more precise items;
- merge true duplicates while preserving redirects or notes for retired IDs;
- add or remove category tags;
- create new topic pages;
- add alternate views such as evidence strength, intervention cost, time-to-effect, or life domain;
- revise evidence classifications when stronger research becomes available.

Item IDs should not be renumbered when the catalog grows or priorities change.

If an item is deprecated or merged, keep a short record of the old ID and point it to the replacement rather than silently reusing that ID.

## Scope boundaries

The repository should contain:

- QoL interventions and factors;
- evidence summaries;
- applicability conditions;
- limitations;
- primary references;
- clearly labeled practical inferences.

The repository should not contain:

- Bruno's personal QoL scores;
- personalized rankings;
- personal health or medication history;
- personal employment details;
- private audit answers;
- individualized medical diagnosis;
- recommendations presented as personal medical care.

A separate private system could use the public QoL map later, but that would be a different project and data boundary.

## Initial implementation

After this design is approved, populate:

1. `README.md` with project purpose, evidence principles, taxonomy rules, and navigation.
2. `catalog.md` with the initial QoL item map and stable `QOL-*` IDs.
3. `references.md` with the source records supporting those items.
4. `topics/*.md` with grouped explanatory material for items that benefit from more context.

The first pass should prioritize correctness of claim-to-source mapping over prose volume. An item with insufficient evidence should be labeled accordingly rather than padded with weak references.

## Success criteria

The design succeeds if a future contributor can:

1. add `QOL-101` without reorganizing the repository;
2. assign that item to several existing categories;
3. introduce a new category without moving or renumbering existing items;
4. trace a material factual claim to its source;
5. tell whether a statement is evidence or extrapolation;
6. understand whether an intervention is broadly applicable or conditional;
7. revise the taxonomy without breaking stable item identities;
8. browse the repository without encountering personal audit information.
