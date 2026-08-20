# Use structured per-record files as the canonical knowledge source

QoL Items and References use individual Markdown files with validated YAML front matter as their canonical records, while catalogs and other index-like views are derived from those records. We chose this over continuing with hand-maintained monolithic Markdown registries because the domain now requires machine-checkable identity, lifecycle, evidence, applicability, relationships, and reference integrity without creating multiple editable sources of truth.
