# WHOQOL coverage audit for the QoL Knowledge Base

## Summary

This note records the decision to use WHOQOL as a coverage framework for the QoL Knowledge Base.

The repository stores evidence-backed, decision-relevant propositions (`QOL-*`), not a complete ontology of human experience. WHOQOL therefore should not be used as causal support for arbitrary interventions. Its role is different: it provides a structured external model for auditing whether important quality-of-life domains and facets are represented strongly, partially, or not at all.

Decision:

- use **WHOQOL-100** as the primary coverage framework because its facet structure is granular enough to expose blind spots;
- use **WHOQOL-BREF** as a compact assessment-oriented companion where a shorter multidomain view is useful;
- treat WHOQOL as **coverage/construct evidence**, not as automatic causal Support Claims for interventions;
- when WHOQOL reveals a gap, run focused research before proposing a new `QOL-*`;
- do not infer a WHOQOL score from unrelated interview questions or informal profile data.

No personal audit answers, diagnoses, medication histories, or individualized rankings belong in this repository.

## Findings

### 1. WHOQOL and the current repository answer different questions

WHOQOL is a multidomain quality-of-life assessment framework developed by the World Health Organization. The repository's canonical `QOL-*` records instead represent reusable decision propositions of kind Intervention, Assessment, or Guardrail.

The two models are complementary:

- **WHOQOL question:** which aspects of lived quality of life should be visible in a broad assessment?
- **QoL Knowledge Base question:** which concrete decisions, assessments, or evidence guardrails are defensible from the available evidence?

A WHOQOL facet can therefore identify a research gap without itself justifying an intervention.

### 2. Provisional coverage audit

The table below is an editorial audit of the current catalog against the WHOQOL facet model. `Strong`, `Partial`, and `Weak/absent` describe repository coverage, not evidence quality for any one item.

| WHOQOL facet / area | Current coverage | Notes |
| --- | --- | --- |
| Pain and discomfort | Strong | Multiple pain and symptom-management items exist. |
| Energy and fatigue | Partial | Sleep, activity, work recovery, and microbreaks touch the area, but broad fatigue assessment is not represented directly. |
| Sleep and rest | Strong | One of the best-covered areas. |
| Positive feelings / enjoyment | Weak/absent | Catalog is stronger on symptoms and risk reduction than positive psychological experience. |
| Thinking, learning, memory, concentration | Partial | Attention and concentration are represented; learning and memory are much less explicit. |
| Self-esteem | Weak/absent | No dedicated decision proposition currently represents this construct. |
| Body image and appearance | Weak/absent | Weight-related health is not the same construct as body image. |
| Negative feelings | Strong | Anxiety, depression, rumination, and recovery are represented. |
| Mobility | Partial | Physical activity is strong, but mobility as functional capacity is less explicit. |
| Activities of daily living | Weak/absent | No broad functional assessment item exists. |
| Dependence on medicines or treatment | Partial | Medication review exists, but treatment dependence as a lived QoL construct is broader. |
| Work capacity | Partial | Work hours and work design are represented more strongly than functional work capacity. |
| Personal relationships | Strong | Recurring contact and relationship distress are represented. |
| Social support | Partial | Social contact is present; perceived availability and adequacy of support are less explicit. |
| Sexual activity / sexual well-being | Present | Covered conditionally through sexual-health assessment. |
| Physical safety and security | Weak/absent | No broad safety-oriented QoL assessment is represented. |
| Home environment | Partial | Noise, light, thermal comfort, air, and friction are represented, but not a broad home-suitability assessment. |
| Financial resources | Moderate | Financial safety margin, spending trade-offs, and time-buying are represented. |
| Health and social care: accessibility and quality | Weak/absent | No general access-to-care assessment is represented. |
| Opportunities for acquiring information and skills | Weak/absent | Not represented in the core QoL catalog. |
| Recreation and leisure | Weak/partial | Time recovery is represented, but meaningful leisure is not directly represented as a QoL construct. |
| Physical environment | Strong | Indoor air, noise, light, temperature, and related exposures are represented. |
| Transport | Moderate/strong | Commute cost, faster transport, and proximity are represented. |
| Spirituality / religion / personal beliefs / meaning | Weak/absent | No general meaning, belief, or purpose-oriented proposition exists. |

### 3. A coverage gap is not automatically a new QoL Item

The correct expansion path is:

```text
Coverage Framework
       |
       v
Coverage Audit
       |
       v
Missing or partial facet
       |
       v
Focused Research
       |
       +--> no reusable decision proposition --> document the gap
       |
       +--> reusable decision proposition
                  |
                  v
      Intervention / Assessment / Guardrail
                  |
                  v
          Evidence Claims + References
                  |
                  v
                 QOL-*
```

Examples:

- `Self-esteem is a WHOQOL facet` is a coverage fact.
- `Increase self-esteem` is **not** yet a valid `QOL-*` statement because it does not specify a defensible intervention, assessment, or guardrail and WHOQOL alone does not establish causal effectiveness.

### 4. Candidate research questions exposed by the audit

These should be researched individually rather than bulk-added:

1. Should the catalog include an Assessment for broad multidomain quality-of-life baseline/follow-up using a validated instrument?
2. Is a Guardrail warranted against inferring overall quality of life from a single behavior, symptom, or domain?
3. Which evidence-backed assessments or interventions are appropriate for clinically meaningful self-esteem or body-image problems?
4. Is perceived social support sufficiently distinct from recurring social contact to justify a separate Assessment or Intervention?
5. Which reusable propositions belong under access to health care, functional activities of daily living, leisure, safety, and meaning/purpose?

### 5. Relationship to existing gap-discovery work

The existing preventive-health gap scan already notes that candidate discovery should continue by looking for under-covered domains. WHOQOL provides a repeatable structure for that step rather than relying only on opportunistic discovery.

## Gaps and caveats

- WHOQOL is an assessment/construct framework, not an intervention guideline.
- WHOQOL facet coverage does not determine causal Evidence Strength.
- A facet can be relevant to human quality of life without yielding a stable reusable `QOL-*` proposition.
- Topic Views are editorial presentations and should not be mistaken for the coverage framework itself.
- The current coverage ratings are an editorial first pass and should be revised as the catalog changes.
- WHOQOL should not become the only possible coverage framework. Additional frameworks may be used when they add nonredundant coverage insight.
- Do not copy instrument questions into the repository unless licensing and use terms are explicitly satisfied. Prefer recording the conceptual structure and links to official sources.

## Sources

### Primary / authoritative sources

- World Health Organization. **WHOQOL: Measuring Quality of Life**. https://www.who.int/tools/whoqol
- World Health Organization. **WHOQOL-BREF**. https://www.who.int/publications/i/item/WHOQOL-BREF
- World Health Organization. **WHOQOL user guidance / instrument materials**. https://www.who.int/publications/i/item/WHO-HIS-HSI-Rev.2012.03

### Repository sources reviewed

- `CONTEXT.md`
- `docs/specification.md`
- `docs/architecture.md`
- `topic-views.yaml`
- `generated/catalog.md`
- `docs/research/open-qol-gap-scan-2026-09-11.md`
