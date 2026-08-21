# Canonical Category Registry Design

## Context

QoL Items already carry flexible category tags, but the repository has no machine-readable source of truth for category names, definitions, or lifecycle. GitHub issue #3 requires a canonical registry, validation of active item usage, and an initial seed based on categories already used in the repository.

`CONTEXT.md` distinguishes canonical categories from non-canonical Topic Views. Therefore, topic-page names are not imported automatically. The initial registry contains only the four category tags explicitly used in `README.md`.

## Goals

- Define canonical category names, short definitions, and lifecycle in one version-controlled file.
- Enforce lower-case kebab-case names and unique YAML keys.
- Allow deprecated categories to identify an optional active replacement.
- Reject unknown or deprecated categories on Active QoL Items.
- Preserve QoL Item identity when categories are added or renamed.
- Document and test the contribution workflow.

## Non-goals

- Turning Topic Views into canonical categories.
- Making categories determine item identity, ownership, or file placement.
- Creating one file per category.
- Requiring historical Deprecated QoL Items to use only currently active categories.
- Supporting replacement chains between deprecated categories.

## Canonical representation

The repository root contains one `categories.yaml` file. Categories are a mapping keyed by canonical name, so the name is the stable lookup key rather than a duplicated field.

```yaml
categories:
  physical-activity:
    definition: Interventions and exposures involving bodily movement or exercise.
    status: Active
  environment:
    definition: Physical environmental conditions and exposures affecting quality of life.
    status: Active
  mental-health:
    definition: Psychological and emotional well-being, symptoms, and functioning.
    status: Active
  circadian:
    definition: Timing and regularity of sleep, wakefulness, and other circadian exposures.
    status: Active
```

A deprecated entry may identify one direct replacement:

```yaml
  former-name:
    definition: Historical category retained for traceability.
    status: Deprecated
    replaced_by: current-name
```

## Schema and semantic rules

`schemas/category-registry.schema.json` uses JSON Schema Draft 2020-12 and defines a closed top-level object containing the required `categories` mapping.

Category keys must match:

```text
^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$
```

Each value is a closed object with:

- required non-empty string `definition`;
- required `status`, either `Active` or `Deprecated`;
- optional `replaced_by`, which must use the category-name pattern.

Semantic validation supplements JSON Schema:

- YAML mapping keys must be unique; duplicate keys are rejected while parsing rather than silently overwritten by PyYAML;
- definitions containing only whitespace are rejected;
- Active categories cannot declare `replaced_by`;
- Deprecated categories may omit `replaced_by`;
- when present, `replaced_by` must resolve to a distinct Active category;
- self-references, unknown targets, and deprecated targets are rejected.

Direct replacement-to-Active semantics avoid replacement chains and give contributors one current tag to use.

## Runtime design

`qol_kb.records` gains an immutable `Category` value and a focused `load_category_registry()` function. The loader:

1. reads `categories.yaml` with duplicate-key detection;
2. validates its shape against `schemas/category-registry.schema.json`;
3. constructs categories keyed by canonical name;
4. validates definitions and lifecycle relationships;
5. returns the validated category mapping.

`validate_repository()` requires the registry and loads it before canonical records. During repository-level validation:

- every category tag on an Active QoL Item must resolve in the registry;
- the resolved category must have status `Active`;
- Deprecated QoL Items may retain historical tags without this active-category restriction.

Category changes never participate in filename or `QOL-*` validation. Adding a tag or replacing a category name therefore does not change item identity.

## Error handling

Validation raises `ValueError`, consistent with the existing record pipeline. Messages identify `categories.yaml`, the relevant category name when available, and the failed rule. Expected failures include duplicate keys, malformed names, blank definitions, invalid lifecycle states, invalid replacements, unknown item tags, and deprecated tags used by Active items.

No new runtime dependency is required; the design reuses PyYAML and jsonschema.

## Documentation and migration

The initial `categories.yaml` is seeded with:

- `physical-activity`
- `environment`
- `mental-health`
- `circadian`

`README.md` is updated so contributors register a category before applying it to an Active item. It continues to state that categories are flexible metadata and do not affect item identity. Topic Views remain independent, non-canonical presentations.

## Testing

New category-registry tests cover:

- loading the seeded valid registry;
- invalid category names;
- duplicate YAML keys;
- blank definitions and invalid lifecycle values;
- Deprecated categories with no replacement or a valid active replacement;
- unknown, deprecated, or self-referential replacement targets;
- Active items using valid, unknown, or Deprecated category tags;
- historical category tags on Deprecated items;
- adding or renaming a category without changing the item's `QOL-*` ID.

Existing repository-validation tests receive an explicit minimal registry fixture. The complete test suite remains the final regression gate.

## Acceptance mapping

- Existing usage is represented by the four seeded entries.
- Mapping keys plus duplicate-key parsing enforce unique names.
- The key pattern enforces lower-case kebab-case.
- Schema and semantic validation enforce Active/Deprecated lifecycle and optional replacement.
- Repository validation rejects unknown or Deprecated tags on Active items.
- Category data is independent of Item IDs and filenames.
- Automated tests cover valid, unknown, duplicate, deprecated, replacement, and identity-preservation cases.
