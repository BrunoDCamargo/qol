# Open QoL gap scan: preventive-health candidates

## Summary

The current catalog already covers sleep, physical activity, nutrition, work/time, mental health, social relationships, common symptoms, sensory health, and several preventive-health decisions. This scan looked for high-confidence additions that are decision-relevant, broadly reusable, and can fit the current taxonomy without creating new categories.

Three candidates survived the first pass:

1. **Brush teeth twice daily with fluoride toothpaste.** Strong candidate for a new general Intervention using the existing `oral-health` and `preventive-health` categories.
2. **Use sun protection when ultraviolet exposure is substantial.** Strong candidate for a conditional Intervention using the existing `environment` and `preventive-health` categories.
3. **Keep routine immunization appropriate to age, risk, and the applicable schedule up to date.** Strong preventive-health candidate, but the canonical wording needs to avoid embedding one jurisdiction's changing schedule.

These are candidates, not yet canonical QoL Items. Each should receive a focused evidence review and duplicate check before a `QOL-*` identity is assigned.

## Findings

### 1. Twice-daily brushing with fluoride toothpaste

**Verified fact.** WHO states that oral diseases can cause pain, discomfort, tooth loss, functional impairment, and psychosocial harm, and identifies inadequate fluoride exposure and poor plaque removal as modifiable contributors. WHO recommends twice-daily toothbrushing with fluoride toothpaste containing 1000 to 1500 ppm fluoride.

**Supporting synthesis.** A 2019 Cochrane systematic review of 96 studies found that fluoride toothpaste prevents dental caries compared with non-fluoride toothpaste. The evidence base is strongest in children and adolescents, with more limited direct evidence for mature permanent dentition in adults.

**Repository inference.** The current catalog contains treatment of symptomatic oral-health problems and reduction of free sugars, but this proposition is distinct: it is a routine preventive behavior. It can use existing categories and does not need a new taxonomy concept.

**Provisional disposition:** add after focused review. Likely `Intervention`, `General`, `Direct`.

### 2. Protection from excessive ultraviolet radiation

**Verified fact.** WHO identifies ultraviolet radiation as a major cause of skin cancer and contributor to eye damage. WHO recommends sun-protection measures when the UV Index reaches 3 or above, prioritizing shade and protective clothing and using broad-spectrum sunscreen for exposed skin. WHO also recommends avoiding artificial tanning devices.

**Repository inference.** A decision-level proposition should focus on reducing excessive UV exposure rather than on sunscreen alone. Sunscreen, protective clothing, hats, and UV-protective sunglasses can then be considered Implementation Options where appropriate.

**Provisional disposition:** add after focused review. Likely `Intervention`, `Conditional`, `Direct`.

### 3. Routine immunization across the life course

**Verified fact.** WHO's routine-immunization summary tables include recommendations across the lifespan, including adults, and distinguish primary series, booster doses, age groups, and risk groups. National schedules translate these recommendations into jurisdiction-specific practice.

**Repository inference.** A reusable QoL Item should not hard-code one country's vaccine schedule. A safer proposition is to keep recommended immunizations current according to age, risk, contraindications, and the applicable national or local schedule.

**Provisional disposition:** research further before adding. Likely `Intervention`, `Conditional` or `General` with explicit schedule constraints. This item will require more maintenance than the other two because recommendations change over time and by jurisdiction.

## Gaps and caveats

- This was a gap-discovery pass, not a complete re-review of all existing `QOL-*` records.
- The toothbrushing recommendation is well established, but evidence for exact fluoride concentrations and effect sizes varies by age and dentition. The canonical claim should stay no broader than the evidence needed for the decision.
- UV protection should not be reduced to a product recommendation. WHO treats clothing, shade, timing, sunglasses, sunscreen, and avoidance of sunbeds as complementary controls.
- Immunization guidance changes with epidemiology, products, age, risk, and jurisdiction. Any canonical item needs wording that remains stable while References can be updated or deprecated.
- Candidate discovery should continue by looking for under-covered domains and by revisiting existing Low-strength or Inferred items when new evidence appears.

## Sources

### Primary / authoritative sources

- World Health Organization. **Oral health**. 17 March 2025. https://www.who.int/news-room/fact-sheets/detail/oral-health
- World Health Organization. **Oral health: questions and answers**. https://www.who.int/news-room/questions-and-answers/item/oral-health
- World Health Organization. **Ultraviolet radiation**. 21 June 2022. https://www.who.int/news-room/fact-sheets/detail/ultraviolet-radiation
- World Health Organization. **Radiation: Protecting against skin cancer**. https://www.who.int/news-room/questions-and-answers/item/radiation-protecting-against-skin-cancer
- World Health Organization. **Table 1: Summary of WHO Position Papers - Recommendations for Routine Immunization**. 1 December 2025. https://www.who.int/publications/m/item/table1-summary-of-who-position-papers-recommendations-for-routine-immunization

### Secondary evidence explicitly used for synthesis

- Walsh T, Worthington HV, Glenny AM, Marinho VCC, Jeroncic A. **Fluoride toothpastes of different concentrations for preventing dental caries**. Cochrane Database of Systematic Reviews. 2019;3:CD007868. PMID 30829399. https://pubmed.ncbi.nlm.nih.gov/30829399/
