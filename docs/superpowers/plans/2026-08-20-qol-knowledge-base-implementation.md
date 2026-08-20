# QoL Knowledge Base Implementation Plan

**Goal:** Build and maintain an extensible, evidence-oriented catalog of quality-of-life items, reusable references, and thematic views without storing individualized audit data.

**Architecture:** `catalog.md` is the canonical item index and assigns stable `QOL-*` identities. `references.md` is the canonical bibliography and assigns stable `REF-*` identities. `topics/*.md` are readable thematic views. Categories remain flexible multi-value tags rather than ownership folders.

**Spec:** `docs/superpowers/specs/2026-08-20-qol-knowledge-base-design.md`

## Global constraints

- Store general quality-of-life knowledge only.
- Do not store personal audit answers, personal scores, individualized rankings, private health histories, employment histories, medication histories, or conclusions about a specific person's quality of life.
- Keep `QOL-*` item IDs stable even when categories, ordering, evidence ratings, or topic organization change.
- Treat categories as flexible tags. An item may have multiple categories, and new categories may be added without reorganizing the repository.
- Prefer primary papers, official guidelines, regulators, government agencies, standards bodies, and first-party scientific sources.
- Separate tested evidence from practical inference.
- Use only `High`, `Moderate`, `Low`, or `Inference` for evidence strength unless the design is explicitly revised.
- Use `General` or `Conditional` for applicability unless the design is explicitly revised.
- Do not inflate an evidence rating to make an item look useful.
- Preserve deprecated or merged IDs instead of silently reusing them.
- Treat the first 100 items as seed data, not a closed taxonomy or permanent ranking.

## File responsibilities

- `README.md`: project purpose, privacy boundary, taxonomy, evidence vocabulary, contribution rules, navigation.
- `catalog.md`: canonical QoL item registry.
- `references.md`: canonical reusable bibliography and claim boundaries.
- `topics/*.md`: overlapping thematic views of canonical items.
- `docs/superpowers/specs/*`: design rationale and long-term structural rules.
- `docs/superpowers/plans/*`: implementation and maintenance plans.

## Phase 1: Repository guide

Create or maintain `README.md` with:

- purpose and scope;
- what belongs and does not belong;
- stable item identifiers;
- flexible multi-category tags;
- evidence-strength vocabulary;
- applicability vocabulary;
- evidence-versus-inference distinction;
- repository navigation;
- instructions for adding `QOL-101` and later items;
- instructions for adding categories and references;
- deprecation/merge rules;
- evidence-update policy;
- disclaimer.

### Acceptance checks

- README states that categories are tags rather than exclusive containers.
- README demonstrates a multi-category item.
- README explains that new categories do not require renumbering or moving canonical items.
- README explicitly excludes individualized audit data.

## Phase 2: Reference registry

Create or maintain `references.md` as a reusable bibliography.

Each record should contain, when available:

```markdown
## REF-XXX

Full citation.

- Source type: ...
- Design: ...
- DOI: ...
- PMID: ...
- URL: ...
- Supports: narrow statement defining what this source can justify
```

### Reference rules

1. Prefer a primary study or official source when one is available.
2. Label systematic reviews, meta-analyses, and narrative reviews as secondary evidence.
3. Keep `Supports:` narrower than or equal to the source's actual findings.
4. Do not infer a specific practical intervention from a broad principle without labeling the intervention as an inference.
5. Reuse an existing `REF-*` when it already supports the claim.
6. Never reuse an old `REF-*` number for an unrelated source.

### Acceptance checks

- Every `REF-*` heading is unique.
- Material scientific claims in the catalog resolve to a defined reference.
- Source type is visible.
- Direct evidence and secondary synthesis are distinguishable.

## Phase 3: Canonical catalog

Maintain `catalog.md` using this schema:

```markdown
| ID | Item | Categories | Evidence | Applicability | References |
|---|---|---|---|---|---|
```

### Item rules

- IDs use `QOL-001`, `QOL-002`, and so on.
- The first release contains `QOL-001` through `QOL-100`.
- New concepts continue at `QOL-101`; existing IDs are not renumbered.
- Categories use lower-case kebab-case.
- Items may have several categories and no primary category is required.
- Evidence ratings remain conservative.
- `Conditional` should be used when usefulness depends on a symptom, diagnosis, exposure, circumstance, or preference.
- `Inference` should be used when a practical application extrapolates from broader evidence.

### Acceptance checks

- Canonical IDs are unique.
- `QOL-001` through `QOL-100` all exist in the seed release.
- Every reference token used by the catalog resolves in `references.md`.
- At least several items demonstrate genuine multi-category tagging.
- The catalog states that its order is not a permanent ranking.

## Phase 4: Thematic views

Maintain these initial topic pages:

```text
topics/sleep.md
topics/physical-activity.md
topics/nutrition-weight.md
topics/mental-health.md
topics/attention-digital.md
topics/work-time.md
topics/environment.md
topics/social-relationships.md
topics/health-checks.md
```

These files are views, not ownership boundaries. The same item may appear in several topic pages when that improves discovery.

Use a common preamble:

```markdown
> This is a thematic view of the canonical QoL catalog. Categories overlap by design. An item may appear in several topic pages; its canonical identity remains its `QOL-*` ID in `catalog.md`.
```

For detailed entries, prefer:

```markdown
## QOL-XXX — Item name

**Categories:** category-a, category-b
**Evidence:** High | Moderate | Low | Inference
**Applicability:** General | Conditional

### Idea
### Why it may affect quality of life
### Evidence
### Practical applications
### Limitations and caveats
### References
```

### Topic rules

- Link back to `catalog.md` and `references.md`.
- Do not redefine the canonical identity of an item.
- Keep claims consistent with the catalog and reference registry.
- Prefix extrapolated concrete advice with `Practical inference:` when needed.
- Create new topic files when a category or cross-cutting domain becomes large enough to justify a dedicated view.

## Phase 5: Quality audit

Before a release or large merge, verify all of the following.

### ID integrity

- `QOL-001` through `QOL-100` exist in the seed catalog.
- No canonical QoL ID appears as two separate catalog rows.
- New items continue with the next unused ID.

### Reference integrity

- Every `REF-*` used in `catalog.md` exists in `references.md`.
- Reference headings are unique.
- Each material claim remains within the source's `Supports:` boundary.

### Taxonomy integrity

- Multi-category examples exist in real catalog data.
- New categories can be added without moving canonical items.
- Topic pages do not become ownership silos.

### Privacy integrity

Review repository content for names, personal measurements, medication lists, employer-specific history, salaries, personal QoL scores, private audit answers, or individualized conclusions. Remove such data from the general knowledge base.

### Evidence integrity

Review claims containing certainty language such as `proves`, `guarantees`, `always`, or `will improve`. Replace them with study-specific wording unless the evidence genuinely supports that strength.

Review inference-heavy items, especially outsourcing, automation, friction reduction, and environment-design examples. Keep them labeled `Inference` unless direct evidence exists for the exact intervention.

### Navigation integrity

- README links to the catalog, reference registry, and initial topic pages.
- Topic pages link back to canonical resources.
- Design and maintenance documents remain discoverable under `docs/`.

## Maintenance workflow

When adding an item:

1. Check for an existing item covering the concept.
2. Assign the next unused `QOL-*` ID.
3. State the item narrowly.
4. Assign all useful categories.
5. Add or reuse references.
6. Set evidence and applicability conservatively.
7. Add the item to relevant topic views.
8. Verify claim-to-source mapping.

When adding a category:

1. Use lower-case kebab-case.
2. Add it where it improves retrieval.
3. Do not move or renumber items because of the category.
4. Create a topic page only when the category merits a dedicated view.

When evidence changes:

1. Keep the canonical item ID if the concept remains the same.
2. Add or update references.
3. Revise the evidence rating and wording.
4. Record important limitations.
5. Avoid preserving old certainty for historical consistency.

When merging or splitting items:

- Never recycle an old ID.
- Preserve a deprecated ID with a pointer or note when necessary for traceability.

## Release definition

A release is ready when:

- the catalog is structurally valid;
- references resolve;
- privacy boundaries hold;
- practical inference is labeled;
- categories remain flexible and overlapping;
- navigation is coherent;
- material claims can be traced to appropriate evidence.
