# Implementation Selection Guides

## Problem Statement

Implementation Options identify reusable classes of products, services, subscriptions, or free approaches that can enact an evidence-backed QoL Item. They intentionally stop before endorsing a specific vendor or model.

That boundary leaves a practical decision unresolved. Two products can belong to the same Implementation Option while differing materially in performance, noise, maintenance burden, reliability, safety, recurring cost, or fit for a particular context. The repository currently has no standard place to describe how to evaluate those differences without mixing product-review evidence into the causal evidence for a `QOL-*` proposition.

## Solution

Add a non-canonical editorial layer called an **Implementation Selection Guide**. Each guide is attached to one Implementation Option and explains how to compare concrete candidates within that class.

A guide records stable decision criteria, context modifiers, disqualifying failure modes, usability and maintenance factors, reliability considerations, and total cost of ownership. It may cite product-testing organizations, standards bodies, regulators, or other sources relevant to product selection.

Concrete product or provider recommendations remain optional, dated market snapshots. They are not canonical identities and do not alter the evidential authority of the parent QoL Item or Implementation Option.

## User Stories

1. As a reader, I want to know which product characteristics matter inside an Implementation Option, so that I can choose a concrete implementation without treating a brand recommendation as scientific evidence.
2. As a reader, I want context modifiers to be explicit, so that I can see why the best choice may differ by room size, noise tolerance, maintenance capacity, intended use, or other relevant conditions.
3. As a reader, I want clear disqualifiers, so that I can eliminate unsafe, misleading, or impractical options before comparing minor features.
4. As a maintainer, I want stable selection criteria separated from volatile model and price data, so that routine market churn does not force changes to canonical records.
5. As a maintainer, I want product-test sources kept separate from QoL causal evidence, so that a strong product review cannot be mistaken for evidence that the intervention itself improves quality of life.
6. As a maintainer, I want a consistent guide structure, so that different Implementation Options can be compared and maintained without inventing a new format for each category.
7. As a maintainer, I want market snapshots to be dated and region-specific when used, so that recommendations expose their freshness and availability limits.
8. As a future automation author, I want the guide-to-Implementation Option relationship to be simple and explicit, so that link and freshness checks can be added later without changing canonical identities.

## Implementation Decisions

- Implementation Selection Guides are non-canonical editorial documents. They do not receive a new stable identity family.
- Each guide is associated with exactly one existing `IMP-*` identity for navigation and scope.
- The parent `IMP-*` record continues to describe a reusable implementation class rather than a vendor, SKU, or provider recommendation.
- A guide must keep product-selection evidence separate from `QOL-*` Evidence Claims. Product-test sources do not gain causal authority by appearing in a Selection Guide.
- The initial guide structure includes: decision supported, context modifiers, must-have criteria, performance criteria, safety or disqualifiers, usability and friction, reliability and durability, maintenance and consumables, total cost of ownership, privacy or connectivity when relevant, comparison method, optional market snapshot, sources, and review date.
- Stable criteria and volatile market data are separate concerns. A market snapshot, when present, must identify its review date and relevant market or region.
- The repository will not introduce a universal Implementation Option score. Numeric scoring, if added later, must be category-specific, method-versioned, and reproducible.
- The first pilot uses the portable HEPA air purifier Implementation Option because its existing description already identifies unresolved product-level factors and mature external testing methods exist for the category.
- The pilot does not change schemas, canonical identities, repository snapshot loading, or generated indexes.

## Testing Decisions

The initial increment is documentation-only and does not introduce a new automated behavior seam. Verification therefore consists of:

- confirming every guide points to an existing active Implementation Option;
- confirming links between the parent Implementation Option and its guide resolve;
- checking that the guide does not make or alter a `QOL-*` Evidence Claim;
- checking that product-level claims are traceable to the cited testing method, regulator, standard, or first-party source;
- running the repository's existing release gate before merge to confirm the documentation change did not disturb canonical validation, generated output, or structural tests.

If Selection Guides later become schema-backed or generated, automated tests should validate guide ownership, required metadata, market-snapshot dates, and stale or unresolved links at the repository-loading or release-gate seam rather than through a separate parallel validator.

## Out of Scope

- A database of individual SKUs or service providers.
- Automatic scraping of Wirecutter, RTINGS, Consumer Reports, Which?, retailers, or manufacturers.
- A cross-category product score.
- Affiliate links, monetization, deal tracking, or price alerts.
- Personalized rankings based on a specific person's private history.
- Replacing scientific, regulatory, or standards evidence with consumer-review ratings.
- Product-level lifecycle identities in the first pilot.

## Further Notes

The Selection Guide layer should borrow methods rather than verdicts from consumer-review organizations. Wirecutter is useful for decision structure and explicit trade-offs. RTINGS is useful for repeatable test benches and methodology versioning. Consumer Reports and Which? add long-term reliability and owner-experience patterns. Sleep Foundation demonstrates context-sensitive testing. Regulators and standards bodies remain preferable when a criterion has an authoritative definition or safety implication.

Market recommendations age faster than the parent Implementation Option. A guide should remain useful after every named product in a market snapshot has disappeared.
