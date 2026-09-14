# Implementation Selection Guides

Implementation Selection Guides help readers compare concrete products or providers inside an existing `IMP-*` class.

They are editorial decision aids, not canonical knowledge records. A guide does not create a new identity, change the evidence strength of a `QOL-*` item, or turn a product review into evidence that an intervention improves quality of life.

## Boundary

The repository uses three distinct layers:

1. `QOL-*` records answer whether an intervention, assessment, or guardrail has defensible QoL relevance.
2. `IMP-*` records identify reusable implementation classes such as a portable HEPA air purifier or sleep mask.
3. Selection Guides explain how to evaluate concrete candidates within one `IMP-*` class.

Product models, providers, prices, stock, firmware, and subscription terms change faster than the first two layers. Keep those details out of canonical `IMP-*` metadata.

## Guide structure

A mature guide should cover the sections that matter for its category:

- Decision this guide supports
- Context modifiers
- Must-have criteria
- Performance criteria
- Safety / disqualifiers
- Usability and friction
- Reliability and durability
- Maintenance and consumables
- Total cost of ownership
- Privacy / connectivity, when relevant
- How to compare candidates
- Current market snapshot, when useful
- Sources and methodology
- Last reviewed

Do not invent a universal score across unrelated Implementation Options. If a category later uses numeric scoring, document the category-specific method and version it when the method changes.

## Market snapshots

A market snapshot is optional. When included, state the review date and relevant region or market. Treat model recommendations as replaceable editorial content rather than stable identities.

Prefer a durable guide that remains useful after its named products disappear from sale.

## Current guides

- [IMP-017 - Portable HEPA air purifier](IMP-017.md)
