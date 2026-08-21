# QoL Knowledge Base

## Purpose

This repository is an extensible, evidence-oriented map of factors, interventions, conditions, and practical changes that may affect quality of life.

The core unit is a **QoL item**. Each item receives a stable `QOL-*` identifier, one or more flexible category tags, an evidence-strength label, an applicability label, and links to reusable `REF-*` records in [`references.md`](references.md).

The initial 100 items are seed data. They are neither a closed taxonomy nor a permanent ranking.

## What belongs here

- General quality-of-life factors and interventions.
- Narrow summaries of what primary research or official guidance actually supports.
- Applicability conditions and important limitations.
- Reusable references to primary papers, guidelines, regulators, government agencies, standards bodies, and other first-party scientific sources.
- Practical applications when they are clearly separated from the evidence that motivates them.
- New categories and cross-category relationships when they improve retrieval or understanding.

## What does not belong here

This repository contains general knowledge. Do not add personal audit answers, personal scores, individualized rankings, medical histories, employment histories, medication histories, or conclusions about a specific person's quality of life.

Do not present individualized diagnosis or medical treatment as a conclusion of this knowledge base. Do not inflate evidence ratings to make an item appear more useful.

## How the knowledge model works

### QoL item IDs

Each canonical item receives a permanent identifier such as `QOL-001`. The identifier represents the concept, not its current location, rank, category, or evidence rating.

IDs must not be renumbered when the catalog grows or priorities change. If an item is later merged or deprecated, retain its old ID as a retired record that points to the replacement rather than reusing that ID for a new concept.

### Categories are flexible tags

Categories are metadata, not exclusive containers. An item may have several categories. Register a new lower-case kebab-case category in `categories.yaml` before applying it to an Active QoL Item. Each registry entry requires a short definition and lifecycle status. Adding, renaming, or reorganizing categories does not change a QoL Item ID.

For example:

```text
QOL-034 — Walk outdoors
Categories: physical-activity, environment, mental-health, circadian
```

`QOL-034` remains the same item if categories are added, removed, renamed, or reorganized later. Topic pages are thematic views, not ownership boundaries.

Use lower-case kebab-case for category tags. Add a category when it improves discovery or understanding rather than merely because another label is technically possible.

### Evidence strength

The catalog uses four evidence-strength labels:

- **High**: strong guideline support, multiple high-quality randomized trials, systematic evidence with consistent findings, or a comparably strong evidence base.
- **Moderate**: at least one useful randomized trial or a consistent body of evidence with meaningful limitations in replication, population, sample size, adherence, or generalizability.
- **Low**: small studies, observational evidence, inconsistent findings, indirect evidence, or substantial uncertainty.
- **Inference**: the practical proposal follows reasonably from another established finding but has not itself been adequately tested.

Evidence strength measures confidence in a claim. It does **not** measure the expected size of the effect for a particular person.

### Applicability

The catalog uses two applicability labels:

- **General**: the intervention or factor can reasonably apply to broad populations, subject to normal caveats.
- **Conditional**: usefulness depends on a particular deficit, symptom, diagnosis, exposure, circumstance, or preference.

Regular physical activity may be broadly applicable. Treating sleep apnea is conditional on having sleep apnea or sufficient signs to justify evaluation. HEPA filtration is conditional on meaningful particulate exposure or another relevant indication.

### Evidence vs practical inference

Keep the result a study actually tested separate from a concrete way someone might apply it.

Example:

**Evidence:** a randomized crossover experiment found that a time-saving purchase reduced reported time pressure and negative affect relative to a material purchase.

**Practical inference:** hiring a cleaner, ordering groceries, or using prepared meals may apply that principle when those services actually remove unwanted tasks.

Do not write the second statement as though each service had independently demonstrated the same causal effect.

## Repository map

- [`catalog.md`](catalog.md): legacy high-level map of QoL items during migration.
- [`references.md`](references.md): legacy reusable evidence registry during migration.
- [`generated/catalog.md`](generated/catalog.md): derived preview of the catalog; do not edit it manually.
- [`generated/references.md`](generated/references.md): derived preview of the references; do not edit it manually.
- [`categories.yaml`](categories.yaml): canonical structured category registry.
- [`items/*.md`](items): canonical structured QoL item sources as they are migrated.
- [`references/*.md`](references): canonical structured reference sources as they are migrated.
- [`topics/sleep.md`](topics/sleep.md): sleep, circadian factors, bedroom conditions, and sleep disorders.
- [`topics/physical-activity.md`](topics/physical-activity.md): aerobic activity, strength, sedentary behavior, active commuting, and musculoskeletal factors.
- [`topics/nutrition-weight.md`](topics/nutrition-weight.md): food environment, dietary quality, hydration, caffeine, alcohol, weight, and nutrition-related factors.
- [`topics/mental-health.md`](topics/mental-health.md): anxiety, rumination, depression, recovery, relationships, and related psychological mechanisms.
- [`topics/attention-digital.md`](topics/attention-digital.md): smartphone access, notifications, interruptions, multitasking, and digital eye strain.
- [`topics/work-time.md`](topics/work-time.md): buying time, outsourcing, work design, commuting, recovery, and financial time scarcity.
- [`topics/environment.md`](topics/environment.md): light, noise, thermal comfort, indoor air, cooking ventilation, and recurring physical frictions.
- [`topics/social-relationships.md`](topics/social-relationships.md): recurring social contact, loneliness, shared experiences, relationship well-being, and prosocial spending.
- [`topics/health-checks.md`](topics/health-checks.md): conditional health problems and evaluations that may substantially affect quality of life.
- [`topics/reproductive-health.md`](topics/reproductive-health.md): pelvic health, urinary incontinence, menopause, heavy menstrual bleeding, endometriosis, and related reproductive-health factors.
- [`docs/superpowers/specs/2026-08-20-qol-knowledge-base-design.md`](docs/superpowers/specs/2026-08-20-qol-knowledge-base-design.md): design principles and long-term structural rules.
- [`docs/superpowers/plans/2026-08-20-qol-knowledge-base-implementation.md`](docs/superpowers/plans/2026-08-20-qol-knowledge-base-implementation.md): implementation and maintenance workflow.

## Generated views

The files under `generated/` are derived previews and must not be edited manually. Regenerate them after changing canonical structured sources, then confirm that the committed previews have no drift:

```powershell
python -m qol_kb.views
python -m qol_kb.views --check
```

## How to add an item

1. Read the existing catalog to confirm that the concept is not already represented.
2. Assign the next unused permanent ID. After the current expansion, the next ID is `QOL-119`.
3. State the item narrowly enough that its evidence can be evaluated.
4. Assign all useful category tags. There is no primary-category requirement.
5. Assign evidence strength and applicability conservatively.
6. Add or reuse the necessary `REF-*` records.
7. Add the item to any topic views where it improves discovery.
8. Keep evidence statements narrower than or equal to what the sources actually support.

Adding `QOL-119` must not require renumbering `QOL-001` through `QOL-118`.

## How to add a category

1. Check `categories.yaml` for an existing tag that represents the retrieval dimension.
2. If none exists, add a unique lower-case kebab-case entry with a short definition and `status: Active`.
3. Apply the registered tag to relevant Active QoL Items.
4. When replacing a category, retain the old entry as `Deprecated` and optionally point `replaced_by` to its direct Active replacement.

Category changes never require a folder move, file migration, or QoL Item ID change. Topic pages remain optional thematic views rather than canonical category definitions.

## How to add or revise a reference

1. Prefer the primary study, current official guideline, regulator, government publication, standards body, or first-party scientific source.
2. Reuse an existing `REF-*` record when it already supports the claim.
3. Otherwise assign the next unused permanent `REF-*` ID.
4. Record the citation, source type, study or guideline design when relevant, DOI and PMID when available, primary URL, and a narrow `Supports:` statement.
5. If only secondary evidence is available, label it explicitly as secondary.
6. When a stronger or newer source changes the interpretation, update the evidence summary and rating rather than silently retaining obsolete certainty.

## Deprecating or merging an item

Do not delete an old identity and reuse its number.

If two items are true duplicates, select the clearer canonical item and retain the other ID as a deprecated record pointing to it. If one broad item is split into several precise items, retain the original ID with a note describing the replacement items when necessary for traceability.

## Evidence update policy

Evidence ratings are revisable. New randomized trials, systematic reviews, guidelines, safety findings, or failures to replicate may strengthen or weaken an item.

When revising an item:

- preserve its stable ID unless the concept itself changes;
- prefer current primary or official sources;
- distinguish outcomes measured by the research from interpretation;
- record major limitations and applicability conditions;
- keep practical extrapolations labeled as inference;
- avoid certainty words such as "guarantees" or "always" unless the evidence genuinely warrants them.

## Disclaimer

This repository is an evidence map for learning and decision support. It is not a diagnostic system and does not replace individualized medical, psychological, nutritional, legal, or financial advice. Many high-impact interventions are conditional: an intervention can have a large effect for people with a relevant problem and little or no value for people without it.
