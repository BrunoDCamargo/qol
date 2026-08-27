# QoL Knowledge Base

An evidence-oriented knowledge base for factors, interventions, conditions, and practical changes that may affect **quality of life**.

The project organizes research-backed claims into stable, reusable records so they can be searched, compared, updated, and connected without collapsing scientific evidence into generic advice.

## At a glance

Each **QoL item** has:

- a permanent `QOL-*` identifier;
- one or more flexible category tags;
- an evidence-strength label;
- an applicability label;
- links to reusable `REF-*` evidence records.

The repository began with 100 seed items and is designed to expand without renumbering existing concepts or forcing them into a fixed taxonomy.

## How the knowledge model fits together

```text
Primary research / official guidance
                ↓
          REF-* records
                ↓
          QOL-* items
        ↙       ↓       ↘
 categories  topic views  generated catalog
```

The model separates three questions that are easy to mix together:

1. **What does the evidence support?**
2. **How strong is that evidence?**
3. **When is the finding applicable?**

A practical suggestion may be useful without having been directly tested. Those cases are labeled as inference rather than presented as if the intervention itself had established evidence.

## Browse by topic

- [Sleep and circadian factors](topics/sleep.md)
- [Physical activity](topics/physical-activity.md)
- [Nutrition and weight](topics/nutrition-weight.md)
- [Mental health](topics/mental-health.md)
- [Attention and digital environment](topics/attention-digital.md)
- [Work and time](topics/work-time.md)
- [Physical environment](topics/environment.md)
- [Social relationships](topics/social-relationships.md)
- [Health checks](topics/health-checks.md)
- [Reproductive health](topics/reproductive-health.md)

## Core design principles

### Stable identities

Each canonical item receives a permanent identifier such as `QOL-001`. The identifier represents the concept, not its current rank, category, filename, or evidence rating.

If an item is merged, split, or deprecated, its old identity remains traceable rather than being reused for a different concept.

### Flexible categories

Categories are retrieval metadata, not exclusive containers. A QoL item may belong to several categories.

For example:

```text
QOL-034 — Walk outdoors
Categories: physical-activity, environment, mental-health, circadian
```

Changing those tags does not change the identity of `QOL-034`.

### Evidence strength

The catalog uses four evidence-strength labels:

- **High**: strong guideline support, multiple high-quality randomized trials, systematic evidence with consistent findings, or a comparably strong evidence base.
- **Moderate**: at least one useful randomized trial or a consistent body of evidence with meaningful limitations.
- **Low**: small studies, observational evidence, inconsistent findings, indirect evidence, or substantial uncertainty.
- **Inference**: the practical proposal follows reasonably from another established finding but has not itself been adequately tested.

Evidence strength describes confidence in a claim. It does not estimate the size of the effect for a particular person.

### Applicability

The catalog distinguishes:

- **General**: the factor or intervention can reasonably apply to broad populations, subject to normal caveats.
- **Conditional**: usefulness depends on a specific deficit, symptom, diagnosis, exposure, circumstance, or preference.

### Evidence vs. practical inference

The project keeps a study result separate from a concrete way someone might apply it.

**Evidence:** a randomized crossover experiment found that a time-saving purchase reduced reported time pressure and negative affect relative to a material purchase.

**Practical inference:** hiring a cleaner, ordering groceries, or using prepared meals may apply that principle when those services actually remove unwanted tasks.

The second statement should not be written as though each service had independently demonstrated the same causal effect.

## Scope

This repository contains general knowledge and evidence summaries. It is not intended to store personal audit answers, individualized rankings, medical histories, medication histories, employment histories, or conclusions about a specific person.

It should not present individualized diagnosis or treatment as a conclusion of the knowledge base.

## Repository map

```text
items/               Canonical structured QoL items
references/          Canonical structured evidence records
categories.yaml      Category registry
topics/              Human-readable thematic views
generated/           Derived catalog and reference views
schemas/             Structured-data schemas
qol_kb/              Generation and validation code
tests/               Regression tests
CONTEXT.md            Domain model and project context
```

Legacy migration views remain available in [`catalog.md`](catalog.md) and [`references.md`](references.md).

The design rationale and implementation records live under [`docs/superpowers/`](docs/superpowers/).

## Generated views

Files under `generated/` are derived previews and should not be edited manually.

After changing canonical structured sources:

```powershell
python -m qol_kb.views
python -m qol_kb.views --check
```

## Adding or revising knowledge

### Add a QoL item

1. Check that the concept is not already represented.
2. Assign the next unused permanent `QOL-*` ID.
3. State the item narrowly enough that its evidence can be evaluated.
4. Apply all useful registered category tags.
5. Assign evidence strength and applicability conservatively.
6. Add or reuse the necessary `REF-*` records.
7. Add the item to relevant topic views when that improves discovery.
8. Keep evidence statements no broader than the sources support.

### Add a category

1. Check `categories.yaml` for an existing retrieval dimension.
2. If needed, add a unique lower-case kebab-case entry with a short definition and `status: Active`.
3. Apply the registered tag to relevant active items.
4. When replacing a category, retain the old entry as `Deprecated` and point to a direct replacement when appropriate.

Category changes do not require a new QoL item ID.

### Add or revise a reference

1. Prefer primary studies, current official guidelines, regulators, government publications, standards bodies, or other first-party scientific sources.
2. Reuse an existing `REF-*` record when it already supports the claim.
3. Otherwise assign the next unused permanent `REF-*` ID.
4. Record the citation, source type, study or guideline design when relevant, DOI and PMID when available, primary URL, and a narrow `Supports:` statement.
5. Label secondary evidence explicitly when primary evidence is unavailable.
6. Update interpretations and evidence ratings when stronger or newer evidence changes the picture.

## Evidence update policy

Evidence ratings are revisable. New randomized trials, systematic reviews, guidelines, safety findings, or failures to replicate may strengthen or weaken an item.

When revising an item:

- preserve its stable ID unless the concept itself changes;
- prefer current primary or official sources;
- distinguish measured outcomes from interpretation;
- record major limitations and applicability conditions;
- keep practical extrapolations labeled as inference.

## Disclaimer

This repository is an evidence map for learning and decision support. It is not a diagnostic system and does not replace individualized medical, psychological, nutritional, legal, or financial advice.
