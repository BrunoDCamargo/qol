# R&D Career Radar focus

The Career Radar maps places where someone living in Curitiba can build a sustained career in Research and Development (R&D), not just find an isolated technical vacancy.

## Core question

For each candidate, ask: **is this a place where a professional can plausibly build an R&D career while continuing to live in Curitiba?**

A strong candidate combines:

1. meaningful and recurring R&D, research, product-development, engineering-development or scientific activity;
2. practical viability from Curitiba, through Curitiba/RMC presence, compatible hybrid work, or current remote-Brazil work;
3. a recurring institutional path to employment, fellowship, selection or other sustained professional participation.

## Priority order

### Priority 1: Curitiba and RMC with own R&D

Highest priority. Favor organizations that maintain laboratories, research groups, engineering development, product development, clinical research, applied research or formal PD&I in Curitiba or the Região Metropolitana de Curitiba.

This group best matches the purpose of the radar because it combines geographic viability with a stable R&D environment.

### Priority 2: Brazil organizations with remote R&D careers

Include Brazilian ICTs, companies and research organizations that maintain their own R&D or research activity and currently allow professionals to work remotely from Brazil.

Remote eligibility must have current evidence. Historical remote policies alone do not establish present viability.

### Priority 3: research-intensive service organizations

CROs, engineering consultancies, quantitative-research firms and similar organizations can remain in the radar when research is a durable part of the work and they offer recurring employment compatible with Curitiba.

They rank below organizations with their own local or remote R&D programs because the work can depend more strongly on client projects, service contracts or specific assignments.

### Opportunity sources

Funding portals, scholarship programs, job aggregators, contractor marketplaces and assignment platforms belong to the opportunity-source layer. They can be useful for finding work without representing a long-term R&D environment themselves.

## Inclusion rule

Promote a candidate into the career radar only when all three conditions have adequate evidence:

- **R&D relevance:** the organization performs meaningful research, PD&I, scientific work, engineering development or product-development activity;
- **Curitiba viability:** the opportunity can realistically be pursued while living in Curitiba;
- **recurring path:** a stable careers, jobs, fellowship, selection or opportunity channel exists.

One isolated vacancy does not establish a recurring career path.

## Boundary cases

Product development alone does not automatically qualify as R&D. The evidence should show research, experimentation, engineering development, scientific work or a formal innovation function strong enough to support an R&D career.

A remote job does not automatically qualify an organization. The work itself must still fit the R&D scope.

A contractor or freelancer marketplace can provide valuable research work, but it should not receive the same priority as an employer or research organization with a stable internal R&D environment.

CROs and clinical-development organizations qualify when research is their core business and current remote-Brazil employment is verified, but they remain a secondary track relative to direct R&D employers and ICTs.

## Repository roles

- [`organizations.yaml`](organizations.yaml) stores verified organizations and their evidence. It is an evidence registry, not a ranking.
- [`sources.yaml`](sources.yaml) stores recurring opportunity and discovery sources.
- [`README.md`](README.md) is the decision-oriented view and presents organizations by career priority.
- `docs/research/` preserves the evidence and reasoning behind additions, exclusions and reclassifications.

Research can preserve a lower-priority entity in `organizations.yaml` even when the README does not surface it as a primary career target. The README controls the practical career view; the YAML preserves the verified research record.