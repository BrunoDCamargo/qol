# Architecture

## Bounded contexts

`CONTEXT-MAP.md` defines two repository contexts:

1. **QoL Knowledge Base** — canonical general evidence and reusable implementation knowledge.
2. **Personal QoL Profile** — private application-layer observations, targets, priorities, trade-offs, and sensitive context for the repository owner.

The relationship is intentionally one-way: the personal profile may reference `QOL-*` items and Coverage Framework facets, but canonical knowledge is never derived from personal data.

## Knowledge-base source-of-truth boundary

The QoL Knowledge Base has one editable source for each kind of canonical knowledge:

- `items/QOL-*.md` stores QoL Item records;
- `references/REF-*.md` stores Reference records;
- `implementation-options/IMP-*.md` stores Implementation Options;
- `categories.yaml` stores Category definitions;
- `topic-views.yaml` stores editorial Topic View membership.

Topic Markdown contains editorial prose, but its complete `## Map` block is derived. Files under `generated/` are also derived. The retired root `catalog.md` and `references.md` registries are not part of the architecture.

Implementation Selection Guides are editorial documents outside the canonical source-of-truth boundary. They reference canonical `IMP-*` records but are not loaded into repository state.

## Personal profile boundary

Files under `personal/` are a separate application context. They may contain:

- Personal Observations;
- Personal Positions;
- Personal Targets;
- Personal Priorities;
- Accepted Trade-offs;
- Sensitive Health Context;
- references to canonical `QOL-*` identities or Coverage Framework facets.

They are not canonical evidence sources and must not be loaded into `RepositorySnapshot`, generated catalog state, Evidence Claims, Evidence Strength, Category definitions, or lifecycle resolution.

The expected flow is:

```text
canonical QoL knowledge + coverage frameworks
                 |
                 v
        personal interpretation
                 |
       +---------+----------+
       |         |          |
       v         v          v
 observations  targets   priorities/trade-offs
```

There is no reverse evidence flow from the personal profile into the canonical knowledge base.

## Validation and snapshot

`qol_kb.records` loads schema-validated canonical sources into one immutable `RepositorySnapshot`. Loading enforces identity, lifecycle, category, evidence-reference, replacement, relationship, and Implementation Option integrity before a snapshot is returned.

The validator rejects unresolved or invalid cross-record links. This means generation never needs to compensate for malformed canonical state.

Selection Guides and the Personal QoL Profile are intentionally excluded from `RepositorySnapshot` in the current implementation. Their content remains human-reviewed editorial/application guidance until enough stable examples justify dedicated schemas or validators.

## Generated views

`qol_kb.views` consumes a validated snapshot and produces deterministic Markdown:

```text
canonical records + categories.yaml
              |
              v
       qol_kb.records
              |
              v
     RepositorySnapshot
              |
       +------+------+
       |             |
       v             v
 generated/      Topic View maps
 indexes         + canonical links
```

The full QoL catalog, Reference index, and Implementation Option index are generated under `generated/`. Topic membership comes from `topic-views.yaml`; canonical row metadata comes from the snapshot; editorial prose remains in `topics/*.md`.

Generated Markdown is never parsed back into canonical state. Personal profile files are also never parsed into canonical state.

## Topic View boundary

A Topic View is a presentation, not a knowledge registry. Contributors choose which QoL identities belong in a topic and may edit explanatory prose. The generator rebuilds the complete `## Map` table from canonical records, including identity, statement, Item Kind, Categories, Evidence Strength, Applicability, Support Mode, lifecycle status, and Reference links.

Links to individual QoL Items and References resolve to the canonical record files. Retired monolithic registry links are rejected rather than silently normalized.

## Selection Guide boundary

A Selection Guide answers a narrower implementation question than an `IMP-*` record: how to compare concrete candidates inside that implementation class.

```text
QOL-* evidence proposition
          |
          v
IMP-* reusable implementation class
          |
          v
Selection Guide editorial criteria
          |
          v
optional dated market snapshot
```

The boundary is one-way. Selection Guides may use canonical records as context, but product ratings, prices, market picks, and review-site scores are never parsed back into `QOL-*`, `REF-*`, or `IMP-*` state.

Stable evaluation criteria belong in the guide. Volatile product names, prices, stock, firmware, and provider details belong only in dated market snapshots when a snapshot is useful.

## Lifecycle and identity resolution

Canonical identities remain addressable when Deprecated. Active records may only depend on lifecycle-compatible records defined by the specification and schemas. Replacement links and typed Item Relationships must resolve before generation succeeds.

Selection Guides and personal profile files do not participate in canonical lifecycle state in the current implementation. If a parent Implementation Option is Deprecated, its linked guide requires human review and should not be treated as current implementation advice without revision. If a referenced `QOL-*` changes lifecycle, personal profile interpretation also requires human review.

## Release boundary

The canonical release gate has three structural responsibilities:

1. load and validate the complete canonical knowledge base, including cross-record integrity;
2. verify deterministic generated output has no drift;
3. run the full structural test suite.

Scientific interpretation, Selection Guide methodology, and Personal QoL Profile interpretation remain human review responsibilities outside the structural gate. Personal files must remain excluded from canonical generation and validation inputs.
