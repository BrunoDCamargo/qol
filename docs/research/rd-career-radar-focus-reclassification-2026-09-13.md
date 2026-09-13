# R&D Career Radar focus reclassification

## Summary

The Career Radar scope was tightened from a broad catalog of R&D-related opportunities to a career-oriented radar: prioritize organizations where a professional can plausibly build a sustained R&D career while continuing to live in Curitiba.

The evidence registry remains broad, but the decision view now distinguishes direct R&D career environments from research-intensive service organizations and opportunity providers.

## Scope decision

The priority order is now:

1. Curitiba and RMC organizations with their own R&D, research, engineering-development, product-development or scientific structures;
2. organizations with sustained internal R&D and current remote-Brazil career paths;
3. research-intensive service organizations such as CROs and quantitative-research firms;
4. contractor marketplaces, assignment platforms, funding portals and other recurring opportunity sources.

This is a project-scoping decision rather than an empirical claim. The durable rule is recorded in `career-radar/FOCUS.md`.

## Verified facts relevant to the reclassification

### Turing

Turing does conduct original frontier-AI research. Its Frontier Research Lab publishes original benchmarks and experimental datasets for evaluating and improving frontier AI agents and language models. [Turing Research](https://www.turing.com/research)

Turing also describes its broader Frontier AI work as a combination of datasets, reinforcement-learning environments, experts and original research. [Turing Frontier AI](https://www.turing.com/frontier-ai)

However, current research opportunities available to candidates in Brazil are explicitly presented as contractor or freelancer assignments rather than standard employment. Current examples include:

- `AI Researcher`, available in Brazil with `Engagement Type: Contractor assignment`. [AI Researcher](https://work.turing.com/r/OkhbSWeMyt)
- `AI Benchmark Engineer — Knowledge / Research`, available in Brazil with `Engagement type: Contractor assignment/freelancer`. [AI Benchmark Engineer — Knowledge / Research](https://work.turing.com/r/8FqO7Lxyme)
- `Research Quality Specialist - Computational Biology`, available in Brazil as a contractor/freelancer engagement. [Computational Biology](https://work.turing.com/r/xpJ4m8DFBx)

Turing's own jobs page also describes the platform as matching professionals with remote work at global companies. [Turing Jobs](https://www.turing.com/jobs)

## Decision

Keep Turing in `organizations.yaml` because the organization itself performs verifiable research and the evidence remains useful. Do not surface it as a primary R&D employer target in the README. Also register Turing in `sources.yaml` as `contract-research-opportunities`, because its current Brazil-accessible research path is primarily an assignment marketplace / contractor channel.

This dual representation is intentional:

- `organizations.yaml` answers whether the organization itself has verified R&D relevance;
- `sources.yaml` answers whether a recurring channel can be monitored for opportunities;
- `README.md` answers which targets deserve career priority.

### CROs and other research-intensive services

CROs and similar service organizations remain legitimate career targets when research is their core business and current remote-Brazil employment is verified. They are placed below direct R&D employers and ICTs in the decision view because their work is more dependent on clinical programs, clients or contracts. This is a prioritization rule, not a claim that CRO work is less technically demanding or less scientific.

## Repository changes

- Added `career-radar/FOCUS.md` as the durable scope and inclusion rule.
- Reworked `career-radar/README.md` into a priority-based decision view.
- Preserved the broader verified evidence registry in `career-radar/organizations.yaml`.
- Added `Turing - Research and AI Assignments` to `career-radar/sources.yaml`.
- Kept unresolved candidates under `To investigate` rather than lowering the evidence threshold.
