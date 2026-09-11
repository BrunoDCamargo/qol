# QoL Knowledge Base

An evidence-oriented knowledge base for factors, interventions, conditions, and practical changes that may affect **quality of life**.

The project organizes research-backed claims into stable, reusable records so they can be searched, compared, updated, and connected without turning scientific evidence into generic advice or product claims.

## At a glance

Each **QoL Item** has:

- a permanent `QOL-*` identifier;
- one or more flexible category tags;
- evidence claims with explicit strength;
- an applicability label;
- a support mode that distinguishes direct support from inference;
- links to reusable `REF-*` evidence records.

Each **Implementation Option** has:

- a permanent `IMP-*` identifier;
- one or more `QOL-*` items that it implements;
- an acquisition mode: `purchase`, `service`, `subscription`, or `free`.

Implementation Options make the knowledge base concrete without claiming that a particular product, brand, supplier, material, or price has evidence that belongs to the broader QoL intervention.

## How the knowledge model fits together

```text
Primary research / official guidance
                ↓
          REF-* records
                ↓
          QOL-* items
        ↙       ↓       ↘
 categories  topic views  generated catalog
                ↓
          IMP-* options
                ↓
 products, services, subscriptions, free implementations
```

The model keeps four questions separate:

1. **What does the evidence support?**
2. **How strong is that evidence?**
3. **When is the finding applicable?**
4. **How can the proposition be implemented concretely?**

A practical proposal may apply broader evidence without having been tested as the same intervention. The QoL Item records this with `support_mode: Inferred`. An Implementation Option can then describe a concrete way to act on that proposition while preserving the evidence boundary.

## Browse

- [Generated QoL catalog](generated/catalog.md)
- [Generated references](generated/references.md)
- [Implementation Options](generated/implementation-options.md)
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

Each canonical record receives a stable identity. `QOL-*` identifies a proposition, `REF-*` identifies a source, and `IMP-*` identifies a concrete implementation option. A rank, category, filename, or evidence rating does not define the identity.

When a canonical record is deprecated, its identity remains traceable rather than being reused for a different concept.

### Flexible categories

Categories are retrieval metadata, not exclusive containers. A QoL Item may belong to several categories.

For example:

```text
QOL-034: Walk outdoors
Categories: physical-activity, environment, mental-health, circadian
```

Changing those tags does not change the identity of `QOL-034`.

### Evidence strength and support mode

Evidence Strength has three values:

- **High**: strong guideline support, multiple high-quality randomized trials, systematic evidence with consistent findings, or a comparably strong evidence base.
- **Moderate**: at least one useful randomized trial or a consistent body of evidence with meaningful limitations.
- **Low**: small studies, observational evidence, inconsistent findings, indirect evidence, or substantial uncertainty.

Evidence Strength describes confidence in an Evidence Claim. A QoL Item derives its strength from the weakest Support Claim necessary to justify its statement. It does not estimate the size of the effect for a particular person.

Support Mode records whether the evidence supports the QoL Item directly (`Direct`) or whether the item applies broader evidence by inference (`Inferred`). `Inferred` is not an Evidence Strength value.

### Applicability

The catalog distinguishes:

- **General**: the proposition can reasonably apply to broad populations, subject to normal caveats.
- **Conditional**: usefulness depends on a specific deficit, symptom, diagnosis, exposure, circumstance, or preference.

### Evidence vs. practical implementation

A time-saving purchase study can support a QoL proposition about buying back unwanted time. A cleaning service can then be an Implementation Option for outsourcing cleaning.

The service does not gain independent causal evidence merely because it implements an evidence-backed or evidence-informed QoL Item. The same rule applies to sleep masks, earplugs, meal services, devices, subscriptions, and other concrete options.

## Scope

This repository contains general knowledge, evidence summaries, and reusable implementation options. It is not intended to store personal audit answers, individualized rankings, medical histories, medication histories, employment histories, purchase histories, or conclusions about a specific person.

It should not present individualized diagnosis or treatment as a conclusion of the knowledge base. Implementation Options should describe reusable classes of solutions rather than endorsements of specific vendors unless a separate evidence and evaluation process justifies that level of specificity.

## Repository map

```text
items/                   Canonical structured QoL Items
references/              Canonical structured evidence records
implementation-options/  Canonical concrete implementation options
categories.yaml          Category registry
topics/                  Editorial topic views with generated canonical maps
generated/               Derived catalog, reference, and implementation views
schemas/                 Structured-data schemas
qol_kb/                  Generation and validation code
tests/                   Regression tests
CONTEXT.md                Domain glossary
catalog.md                Generated compatibility pointer
references.md             Generated compatibility pointer
```

### Canonical cutover

The migration from the original monolithic `catalog.md` and `references.md` registries is complete. Those root paths are now generated compatibility pointers; they are no longer editable knowledge registries.

QoL Item metadata is edited in `items/`, reference metadata in `references/`, Implementation Options in `implementation-options/`, and category definitions in `categories.yaml`. The complete catalog and reference indexes are derived under `generated/`.

Topic pages remain editorial documents. Their prose and choice of which `QOL-*` identities belong in a topic are maintained in `topics/`, while the `## Map` table is rebuilt from canonical records. The displayed statement, kind, categories, Evidence Strength, applicability, Support Mode, lifecycle status, and reference links are therefore derived rather than independently maintained.

## Generated views

The generator owns:

- `catalog.md` and `references.md` compatibility pointers;
- files under `generated/`;
- canonical metadata inside each topic page's `## Map` table and canonical record links in topic prose.

After changing canonical structured sources or topic composition:

```powershell
python -m qol_kb.views
python -m qol_kb.views --check
```

`--check` compares the expected bytes with committed output. CI rejects drift in generated indexes, compatibility pointers, and Topic View metadata. Editorial prose remains editable because the generator preserves it.

## Adding or revising knowledge

### Add a QoL Item

1. Check that the proposition is not already represented.
2. Assign the next unused permanent `QOL-*` ID.
3. State the proposition narrowly enough that its evidence can be evaluated.
4. Apply all useful registered category tags.
5. Set applicability and Support Mode conservatively.
6. Add explicit Support and Constraint Claims as needed and link reusable `REF-*` records.
7. Add the identity to relevant topic `## Map` selections when that improves discovery; the generator will populate the canonical row metadata.
8. Run the view generator rather than editing generated metadata by hand.
9. Keep claims no broader than their sources support.

### Add an Implementation Option

1. Start from an existing Active QoL Item. Do not create a free-floating product or service record.
2. Check that the concrete implementation is not already represented.
3. Assign the next unused permanent `IMP-*` ID.
4. Link every QoL Item that the option implements.
5. Set `acquisition` to `purchase`, `service`, `subscription`, or `free`.
6. Describe the option as a reusable class, not an unsupported brand recommendation.
7. State important evidence boundaries in the record body when readers could mistake the QoL evidence for product-level evidence.

### Add a category

1. Check `categories.yaml` for an existing retrieval dimension.
2. If needed, add a unique lower-case kebab-case entry with a short definition and `status: Active`.
3. Apply the registered tag to relevant active items.
4. When replacing a category, retain the old entry as `Deprecated` and point to a direct replacement when appropriate.

Category changes do not require a new QoL Item ID.

### Add or revise a reference

1. Prefer primary studies, current official guidelines, regulators, government publications, standards bodies, or other first-party scientific sources.
2. Reuse an existing `REF-*` record when it already supports the claim.
3. Otherwise assign the next unused permanent `REF-*` ID.
4. Record the citation, source type, study or guideline design when relevant, DOI and PMID when available, primary URL, and a narrow `Supports:` statement.
5. Label secondary evidence explicitly when primary evidence is unavailable.
6. Update interpretations and evidence ratings when stronger or newer evidence changes the picture.

## Evidence update policy

Evidence ratings can change when new randomized trials, systematic reviews, guidelines, safety findings, or failures to replicate change confidence in a claim.

When revising an item:

- preserve its stable ID unless the proposition itself changes;
- prefer current primary or official sources;
- distinguish measured outcomes from interpretation;
- record major limitations and applicability conditions;
- use `support_mode: Inferred` when a practical proposition applies broader evidence by inference.

## Disclaimer

This repository is an evidence map for learning and decision support. It is not a diagnostic system and does not replace individualized medical, psychological, nutritional, legal, or financial advice.
