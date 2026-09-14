# QoL Knowledge Base

An evidence-oriented knowledge base for reusable propositions, evidence records, and concrete implementation options that may affect quality of life.

## Browse

- [Generated QoL catalog](generated/catalog.md)
- [Generated reference index](generated/references.md)
- [Implementation Options](generated/implementation-options.md)
- [Implementation Selection Guides](docs/selection-guides/README.md)
- [R&D Career Radar](career-radar/README.md)
- [Sleep](topics/sleep.md)
- [Physical activity](topics/physical-activity.md)
- [Nutrition and weight](topics/nutrition-weight.md)
- [Mental health](topics/mental-health.md)
- [Attention and digital environment](topics/attention-digital.md)
- [Work and time](topics/work-time.md)
- [Physical environment](topics/environment.md)
- [Social relationships](topics/social-relationships.md)
- [Health checks](topics/health-checks.md)
- [Reproductive health](topics/reproductive-health.md)

## Project documentation

The current project contract is split by responsibility:

- [Domain glossary](CONTEXT.md): canonical domain terms and distinctions.
- [Architecture](docs/architecture.md): source-of-truth boundaries, validation, and generated-view flow.
- [Specification](docs/specification.md): normative repository behavior and invariants.
- [Contribution rules](CONTRIBUTING.md): how to add or revise knowledge and pass the release gate.
- [ADR 0001](docs/adr/0001-structured-canonical-records.md): why structured per-record files replaced monolithic registries.

Canonical knowledge is edited in structured records and registries described by the specification. Generated indexes and generated portions of Topic Views are derived output and must not be edited as independent knowledge sources. Implementation Selection Guides are non-canonical editorial aids for choosing concrete products or providers inside an existing `IMP-*` class.

## Scope

This repository contains general knowledge and reusable implementation options. It does not store personal audit answers, individualized rankings, private health or medication histories, employment histories, purchase histories, or individualized diagnosis or treatment conclusions.

## Disclaimer

This repository is an evidence map for learning and decision support. It is not a diagnostic system and does not replace individualized medical, psychological, nutritional, legal, or financial advice.
