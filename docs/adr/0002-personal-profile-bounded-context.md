# ADR 0002: Keep the personal QoL profile in a separate bounded context inside the private repository

## Status

Accepted

## Decision

The private repository will contain both the general QoL Knowledge Base and a Personal QoL Profile under `personal/`. Personal records may reference canonical `QOL-*` items and Coverage Framework facets, but personal observations, diagnoses, medications, priorities, and trade-offs never become canonical evidence or generated knowledge-base state.

## Rationale

Keeping the profile beside the evidence preserves continuity between general recommendations and their personal application without requiring a second repository. The trade-off is that sensitive information committed to Git can remain in history even after ordinary deletion; the repository owner explicitly accepts this persistence risk for information deliberately recorded in the personal context.

## Consequences

`CONTEXT-MAP.md` routes the two contexts. `personal/` stays outside `RepositorySnapshot`, Evidence Claims, Evidence Strength, generated indexes, and the canonical schema/release gate. Any future automation must preserve this one-way boundary, and removing sensitive history may require Git history rewriting rather than ordinary file deletion.
