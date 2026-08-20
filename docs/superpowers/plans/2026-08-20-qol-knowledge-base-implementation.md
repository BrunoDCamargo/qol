# QoL Knowledge Base Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Populate the repository with an extensible, evidence-oriented catalog of 100 quality-of-life items, reusable primary references, and topic pages without storing any personal audit data.

**Architecture:** `catalog.md` is the canonical item index and assigns stable `QOL-*` identities. `references.md` is the canonical bibliography and assigns stable `REF-*` identities. `topics/*.md` provides readable thematic views; categories remain flexible multi-value tags rather than exclusive folders, so new categories and mixed-category items can be added without renumbering or moving canonical items.

**Tech Stack:** Markdown, Git, primary scientific/official web sources. No runtime dependencies are required.

**Spec:** `docs/superpowers/specs/2026-08-20-qol-knowledge-base-design.md`

## Global Constraints

- Store general quality-of-life knowledge only.
- Do not store Bruno's personal audit, rankings, health history, medication history, employment situation, or individualized conclusions.
- Keep `QOL-*` item IDs stable even when categories, ordering, evidence ratings, or topic organization change.
- Treat categories as flexible tags. An item may have multiple categories, and new categories may be added without reorganizing the repository.
- Prefer primary papers, official guidelines, regulators, government agencies, standards bodies, and first-party scientific sources.
- Separate tested evidence from practical inference.
- Use only `High`, `Moderate`, `Low`, or `Inference` for evidence strength.
- Use `General` or `Conditional` for applicability unless the design is amended explicitly.
- Do not inflate an evidence rating to make an item look useful.
- Preserve deprecated or merged IDs instead of silently reusing them.
- The first 100 items are seed data, not a closed taxonomy or permanent ranking.

---

## File Structure

- Create: `README.md` — project purpose, scope boundary, contribution model, evidence vocabulary, category/tag rules, navigation.
- Create: `catalog.md` — canonical 100-item QoL catalog with stable IDs, multi-category tags, evidence rating, applicability, and `REF-*` links.
- Create: `references.md` — canonical reusable bibliography with source type, study design or guideline type, DOI/PMID when available, and primary URL.
- Create: `topics/sleep.md` — sleep duration, sleep disorders, circadian light, noise, thermal comfort, and sleep-related interventions.
- Create: `topics/physical-activity.md` — walking, aerobic activity, resistance training, sedentary behavior, active commute, and musculoskeletal items.
- Create: `topics/nutrition-weight.md` — food environment, ultraprocessed foods, hydration, caffeine, alcohol, and nutrition-related items.
- Create: `topics/mental-health.md` — anxiety, rumination, depression, mindfulness, social anxiety-adjacent mechanisms, recovery, and relationship/sexual well-being items.
- Create: `topics/attention-digital.md` — smartphone internet, notifications, multitasking, interruption control, and digital eye strain.
- Create: `topics/work-time.md` — buying time, outsourcing, work hours, hybrid work, commute, recovery, office environment, and financial time-scarcity items.
- Create: `topics/environment.md` — bedroom environment, indoor air, cooking ventilation, noise, light, plants, and recurring physical frictions.
- Create: `topics/social-relationships.md` — recurring social contact, loneliness interventions, shared experiences, prosocial spending, relationship well-being.
- Create: `topics/health-checks.md` — apnea, vision, hearing, oral health, tinnitus, nocturia, GI symptoms, medication review, rhinitis, bruxism, reflux, eczema, headache.

Topic files are views, not ownership boundaries. The same `QOL-*` item may be summarized in more than one topic file when that improves discovery.

---

### Task 1: Create repository guide and taxonomy rules

**Files:**
- Create: `README.md`

**Interfaces:**
- Consumes: the approved design spec.
- Produces: contributor-facing rules used by every later task.

- [ ] **Step 1: Write the README structure**

Use these exact sections:

```markdown
# QoL Knowledge Base

## Purpose
## What belongs here
## What does not belong here
## How the knowledge model works
### QoL item IDs
### Categories are flexible tags
### Evidence strength
### Applicability
### Evidence vs practical inference
## Repository map
## How to add an item
## How to add a category
## How to add or revise a reference
## Deprecating or merging an item
## Evidence update policy
## Disclaimer
```

- [ ] **Step 2: State the privacy boundary explicitly**

Include this rule in `## What does not belong here`:

```markdown
This repository contains general knowledge. Do not add personal audit answers, personal scores, individualized rankings, medical histories, employment histories, medication histories, or conclusions about a specific person's quality of life.
```

- [ ] **Step 3: State the category model explicitly**

Include this example in `### Categories are flexible tags`:

```text
QOL-034 — Walk outdoors
Categories: physical-activity, environment, mental-health, sleep
```

Explain that `QOL-034` remains the same item if categories are added, removed, renamed, or reorganized later.

- [ ] **Step 4: Document the evidence vocabulary**

Use the four definitions from the design spec: `High`, `Moderate`, `Low`, `Inference`. State that evidence strength measures confidence in the claim, not expected effect size.

- [ ] **Step 5: Document applicability**

Use `General` and `Conditional`. Include examples that regular physical activity may be broadly applicable while sleep-apnea treatment and HEPA filtration are conditional on a relevant condition or exposure.

- [ ] **Step 6: Document growth rules**

State that contributors may add `QOL-101`, create new categories, assign several categories to one item, split broad items, or merge duplicates while preserving retired IDs.

- [ ] **Step 7: Review for accidental personalization**

Run:

```bash
grep -Ein 'Bruno|personal audit|my medication|my job|my score' README.md
```

Expected: only the generic phrase `personal audit` may appear in the repository-wide exclusion rule; no personal facts appear.

- [ ] **Step 8: Commit**

```bash
git add README.md
git commit -m "docs: add QoL knowledge base guide"
```

---

### Task 2: Build the canonical reference registry

**Files:**
- Create: `references.md`

**Interfaces:**
- Consumes: primary research and official sources listed below.
- Produces: stable `REF-*` identifiers used by `catalog.md` and topic pages.

- [ ] **Step 1: Create the reference record schema**

Start `references.md` with:

```markdown
# References

Each `REF-*` record is reusable. Prefer the primary paper, official guideline, regulator, government publication, or first-party scientific source. Secondary sources may be used only when adequate primary evidence is unavailable and must be labeled as secondary.

Each record should contain:

- full citation;
- source type;
- study/guideline design when relevant;
- DOI when available;
- PMID when available;
- primary URL;
- short note describing which claim the source can support.
```

- [ ] **Step 2: Verify and register the initial primary-source pool**

Assign sequential `REF-*` IDs after verifying title, authors/organization, year, DOI/PMID where available, and the primary URL. Use at least the following source pool because these sources already support the seed catalog:

1. AASM/Sleep Research Society adult sleep-duration consensus: `https://aasm.org/resources/pdf/sleepdurationrecommendations.pdf` or the current AASM canonical equivalent.
2. NHLBI sleep-wake cycle: `https://www.nhlbi.nih.gov/health/sleep/sleep-wake-cycle`.
3. NHLBI sleep apnea symptoms: `https://www.nhlbi.nih.gov/health/sleep-apnea/symptoms`.
4. CBT-I randomized evidence, PubMed 40220528: `https://pubmed.ncbi.nlm.nih.gov/40220528/`.
5. Caffeine and sleep timing, PMID 24235903: `https://pubmed.ncbi.nlm.nih.gov/24235903/`.
6. WHO environmental noise compendium: `https://www.who.int/tools/compendium-on-health-and-environment/environmental-noise`.
7. Sleep mask trial in *Sleep*: `https://academic.oup.com/sleep/article/46/12/zsad196/7227835`.
8. Mobile-internet blocking RCT, *PNAS Nexus* 2025: `https://academic.oup.com/pnasnexus/article/4/2/pgaf017/8016017`.
9. Notification interruption field experiment, PMID 37280752: `https://pubmed.ncbi.nlm.nih.gov/37280752/`.
10. Multitasking/interruption experiment, PMID 37542740: `https://pubmed.ncbi.nlm.nih.gov/37542740/`.
11. Work-disconnection intervention, PMID 41545795: `https://pubmed.ncbi.nlm.nih.gov/41545795/`.
12. Whillans et al., *Buying time promotes happiness*, PMCID PMC5559044: `https://pmc.ncbi.nlm.nih.gov/articles/PMC5559044/`.
13. Hybrid-work randomized trial in *Nature*: `https://www.nature.com/articles/s41586-024-07500-2`.
14. HHS/ODPHP physical-activity guidelines summary: `https://odphp.health.gov/our-work/nutrition-physical-activity/physical-activity-guidelines/current-guidelines/top-10-things-know`.
15. WHO physical-activity guidelines: `https://www.who.int/publications/i/item/9789240015128` or current canonical WHO page.
16. CDC adult physical-activity recommendations: `https://www.cdc.gov/physical-activity-basics/guidelines/adults.html`.
17. Neck-pain office-worker trial, PMID 36167936: `https://pubmed.ncbi.nlm.nih.gov/36167936/`.
18. Ergonomic intervention evidence, PMID 30132008: `https://pubmed.ncbi.nlm.nih.gov/30132008/`.
19. Sit-stand intervention trial, PMID 26584856: `https://pubmed.ncbi.nlm.nih.gov/26584856/`.
20. Myofascial-pain massage trial, PMID 36645811: `https://pubmed.ncbi.nlm.nih.gov/36645811/`.
21. EPA indoor particulate matter: `https://www.epa.gov/indoor-air-quality-iaq/indoor-particulate-matter`.
22. EPA air cleaners/home filters: `https://www.epa.gov/indoor-air-quality-iaq/air-cleaners-and-air-filters-home`.
23. Refractive correction quality-of-life trial, PMID 16776781: `https://pubmed.ncbi.nlm.nih.gov/16776781/`.
24. WHO oral health: `https://www.who.int/health-topics/oral-health`.
25. WHO hearing/rehabilitation source appropriate to functional hearing loss and participation.
26. Hall et al. ultraprocessed-diet inpatient RCT, PMID 31105044: `https://pubmed.ncbi.nlm.nih.gov/31105044/`.
27. CDC alcohol use: `https://www.cdc.gov/alcohol/about-alcohol-use/index.html`.
28. WHO tobacco source appropriate to cessation/health burden.
29. WHO mhGAP guideline for anxiety interventions: current official WHO mhGAP guideline PDF/page.
30. WHO social connection report: current official WHO Commission on Social Connection report/page.
31. Community social-connection pragmatic trial, PMID 41982893: `https://pubmed.ncbi.nlm.nih.gov/41982893/`.
32. Kindness/loneliness randomized evidence, PMID 40847560: `https://pubmed.ncbi.nlm.nih.gov/40847560/`.
33. USPSTF vitamin supplementation recommendation: `https://www.uspreventiveservicestaskforce.org/uspstf/recommendation/vitamin-supplementation-to-prevent-cvd-and-cancer-preventive-medication`.
34. USPSTF vitamin-D deficiency screening: `https://www.uspreventiveservicestaskforce.org/uspstf/recommendation/vitamin-d-deficiency-screening`.
35. NCCIH dietary supplements: `https://www.nccih.nih.gov/health/using-dietary-supplements-wisely`.
36. Sleep regularity consensus, PMID 37684151: `https://pubmed.ncbi.nlm.nih.gov/37684151/`.
37. AASM restless-legs guideline, PMID 39324694: `https://pubmed.ncbi.nlm.nih.gov/39324694/`.
38. Rhinitis/sleep randomized evidence, PMID 12797340: `https://pubmed.ncbi.nlm.nih.gov/12797340/`.
39. NIDCR bruxism: `https://www.nidcr.nih.gov/health-info/bruxism`.
40. Digital-eye-strain breaks experiment, PMID 40466853: `https://pubmed.ncbi.nlm.nih.gov/40466853/`.
41. Behavioral activation depression evidence, PMID 42492146: `https://pubmed.ncbi.nlm.nih.gov/42492146/`.
42. WHO/ILO long working hours: `https://www.who.int/news/item/17-05-2021-long-working-hours-increasing-deaths-from-heart-disease-and-stroke-who-ilo` plus the underlying WHO/ILO paper if accessible.
43. Psychological detachment RCT, PMID 39101888: `https://pubmed.ncbi.nlm.nih.gov/39101888/`.
44. Recovery training RCT, PMID 38023967: `https://pubmed.ncbi.nlm.nih.gov/38023967/`.
45. Self-monitoring activity trial, PMID 33028335: `https://pubmed.ncbi.nlm.nih.gov/33028335/`.
46. Microbreak meta-analysis, PMID 36044424: `https://pubmed.ncbi.nlm.nih.gov/36044424/`; label as secondary evidence because it is a meta-analysis rather than primary research.
47. Tinnitus guideline/paper, PMID 40111327: `https://pubmed.ncbi.nlm.nih.gov/40111327/`.
48. NIDDK IBS: `https://www.niddk.nih.gov/health-information/digestive-diseases/irritable-bowel-syndrome`.
49. FDA adverse-reaction guidance: `https://www.fda.gov/drugs/find-information-about-drug/finding-and-learning-about-side-effects-adverse-reactions`.
50. NIDDK constipation pages appropriate to definition, causes, diet, and treatment.
51. NIDDK lactose intolerance treatment: `https://www.niddk.nih.gov/health-information/digestive-diseases/lactose-intolerance/treatment`.

Where the existing source pool does not support a seed item closely enough, find and register a better primary source before giving that item an evidence rating above `Low` or `Inference`.

- [ ] **Step 3: Keep claims narrow**

For every `REF-*`, write one sentence beginning `Supports:` that states the narrow claim the source can justify. Example:

```markdown
Supports: In the randomized crossover experiment, spending money on a time-saving purchase reduced reported time pressure and negative affect relative to a material purchase.
```

Do not write `Supports: hiring a cleaner improves happiness` unless that specific intervention was directly tested.

- [ ] **Step 4: Verify no duplicate reference IDs**

Run:

```bash
grep '^## REF-' references.md | sort | uniq -d
```

Expected: no output.

- [ ] **Step 5: Commit**

```bash
git add references.md
git commit -m "docs: add QoL reference registry"
```

---

### Task 3: Create the canonical 100-item catalog

**Files:**
- Create: `catalog.md`

**Interfaces:**
- Consumes: `REF-*` IDs from `references.md`.
- Produces: stable `QOL-001` through `QOL-100`, used by all topic views.

- [ ] **Step 1: Create the catalog schema**

Use this table header:

```markdown
# QoL Catalog

The catalog is an extensible map, not a permanent ranking. IDs are stable. Categories are flexible tags and may be combined freely.

| ID | Item | Categories | Evidence | Applicability | References |
|---|---|---|---|---|---|
```

- [ ] **Step 2: Seed these exact stable IDs**

Use the following item identity map. Wording may be tightened for scientific precision, but do not renumber IDs:

```text
QOL-001  Maintain sufficient sleep duration
QOL-002  Evaluate possible sleep apnea when signs are present
QOL-003  Use CBT-I for chronic insomnia when indicated
QOL-004  Test caffeine timing when sleep may be affected
QOL-005  Increase useful daytime light exposure
QOL-006  Reduce bright light late at night when circadian delay is a concern
QOL-007  Reduce meaningful nighttime environmental noise
QOL-008  Do not assume white/pink noise improves sleep; test conditionally
QOL-009  Improve thermal comfort during sleep
QOL-010  Use blackout or a sleep mask when bedroom light is disruptive
QOL-011  Consider weighted blankets only for relevant sleep/anxiety contexts
QOL-012  Trial reduced or blocked mobile internet on smartphones
QOL-013  Disable nonessential notifications
QOL-014  Remove nonessential badges, banners, and vibrations
QOL-015  Move discretionary social-media use to less interruptive devices
QOL-016  Reduce work-app intrusion into off-hours when feasible
QOL-017  Create periods of monotasking
QOL-018  Batch asynchronous communication when immediate response is unnecessary
QOL-019  Keep the phone physically out of reach during focus activities
QOL-020  Treat generic social-media detox claims cautiously
QOL-021  Spend money to buy back unwanted time when worthwhile
QOL-022  Outsource cleaning when it meaningfully saves unwanted time
QOL-023  Use grocery delivery when it meaningfully saves unwanted time
QOL-024  Outsource laundry/ironing when it meaningfully saves unwanted time
QOL-025  Use prepared meals or meal services when they meaningfully save unwanted time
QOL-026  Outsource recurring maintenance when it meaningfully saves unwanted time
QOL-027  Pay for faster transport selectively when time savings justify it
QOL-028  Automate recurring bills and administrative chores
QOL-029  Use hybrid work when role and circumstances support it
QOL-030  Quantify the annual time cost of commuting
QOL-031  Consider living closer to recurring destinations when commute dominates life
QOL-032  Protect meeting-free or interruption-free focus blocks
QOL-033  Add regular walking
QOL-034  Walk outdoors when feasible
QOL-035  Treat sub-guideline amounts of physical activity as useful, not worthless
QOL-036  Perform resistance training at least twice weekly when able
QOL-037  Break up long periods of sitting
QOL-038  Treat recurrent neck pain rather than normalizing it
QOL-039  Combine ergonomics with movement/exercise rather than relying only on gadgets
QOL-040  Consider sit-stand workstations conditionally
QOL-041  Use massage as a conditional adjunct for relevant musculoskeletal pain
QOL-042  Reduce bedroom noise when it disrupts sleep
QOL-043  Make the bedroom sufficiently dark for sleep
QOL-044  Get adequate light during the day
QOL-045  Keep the bedroom thermally comfortable
QOL-046  Use source control/exhaust ventilation while cooking
QOL-047  Use HEPA filtration when particulate exposure or another indication justifies it
QOL-048  Avoid treating consumer CO2 sensing as a guaranteed cognitive-performance hack
QOL-049  Correct meaningful refractive error and reassess vision when symptomatic
QOL-050  Treat oral-health problems rather than normalizing pain or dysfunction
QOL-051  Evaluate hearing when functional difficulty is present
QOL-052  Reduce reliance on ultraprocessed foods
QOL-053  Design the food environment so preferred choices are easy defaults
QOL-054  Use water/unsweetened drinks as default hydration
QOL-055  Maintain adequate hydration when intake is insufficient
QOL-056  Adjust caffeine timing before assuming total abstinence is necessary
QOL-057  Trial lower alcohol exposure when alcohol may affect sleep, mood, or health
QOL-058  Stop nicotine/tobacco use when applicable
QOL-059  Use evidence-based psychological treatment for clinically significant anxiety
QOL-060  Address persistent rumination when it consumes attention or recovery
QOL-061  Treat meditation/mindfulness as a conditional tool rather than a universal remedy
QOL-062  Maintain recurring contact with people one values
QOL-063  Prefer reliable recurring social contact over relying only on occasional large events
QOL-064  Do not assume more social activities alone will resolve loneliness
QOL-065  Do not assume prosocial acts are a universal treatment for loneliness
QOL-066  Avoid assuming generic multivitamins will transform health or QoL
QOL-067  Avoid indiscriminate vitamin-D screening in asymptomatic adults without indication
QOL-068  Use supplements for a defined need, deficiency, or evidence-based indication
QOL-069  Keep sleep/wake timing reasonably regular
QOL-070  Evaluate restless-legs symptoms when present
QOL-071  Treat persistent rhinitis/congestion when it affects sleep or daytime function
QOL-072  Treat recurrent headache/migraine when it meaningfully affects function
QOL-073  Evaluate symptomatic bruxism/TMD rather than normalizing it
QOL-074  Treat clinically relevant nocturnal reflux
QOL-075  Address digital eye strain when screen work causes symptoms
QOL-076  Treat recurrent low-back pain rather than normalizing it
QOL-077  Evaluate and treat persistent loss of interest/pleasure or depression when present
QOL-078  Treat persistent relationship distress when it is a major QoL driver
QOL-079  Include sexual health in quality-of-life assessment when relevant
QOL-080  Measure actual weekly work hours when workload is uncertain
QOL-081  Improve psychological detachment from work
QOL-082  Build deliberate recovery skills after work
QOL-083  Reduce office noise when concentration demands and noise exposure justify it
QOL-084  Consider modest workplace greening/vegetation as a low-stakes environmental intervention
QOL-085  Spend some discretionary money on meaningful shared experiences when valued
QOL-086  Treat prosocial spending as potentially beneficial, not universally effective
QOL-087  Increase financial safety margin when financial insecurity drives stress
QOL-088  Automate recurring financial obligations where automation removes cognitive load
QOL-089  Use activity self-monitoring when it helps sustain movement
QOL-090  Use microbreaks to manage fatigue during long cognitive work
QOL-091  Use active commuting when safe and practical
QOL-092  Schedule rewarding activities when low activation or avoidance is a problem
QOL-093  Treat bothersome tinnitus rather than assuming nothing can help
QOL-094  Evaluate recurrent nocturia when it disrupts sleep
QOL-095  Investigate chronic GI symptoms that meaningfully affect QoL
QOL-096  Treat eczema/pruritus when it disrupts comfort or sleep
QOL-097  Review medications when symptoms plausibly track medication initiation or dose changes
QOL-098  Repair or replace recurring physical irritants in the environment
QOL-099  Duplicate inexpensive frequently transported items when it removes repeated friction
QOL-100  Audit recurring commitments and remove those no longer worth their cost
```

- [ ] **Step 3: Assign multi-category tags**

Use lower-case kebab-case tags. Start with these suggested tags, but add new tags when they improve retrieval:

```text
sleep
circadian
physical-activity
strength
sedentary-behavior
nutrition
weight
hydration
substances
mental-health
attention
technology
work-design
time
financial-wellbeing
environment
indoor-air
pain
vision
hearing
oral-health
gastrointestinal
social
relationships
sexual-health
preventive-health
medications
friction-reduction
```

Do not force one primary category. Example:

```text
QOL-034 categories: physical-activity, environment, mental-health, circadian
QOL-081 categories: work-design, mental-health, time
QOL-097 categories: medications, preventive-health
```

- [ ] **Step 4: Assign evidence and applicability conservatively**

Examples:

```text
QOL-002  High / Conditional
QOL-012  Moderate / General
QOL-022  Inference / Conditional
QOL-036  High / General
QOL-047  Moderate / Conditional
QOL-066  High / General
QOL-099  Inference / Conditional
```

If evidence only supports a broader principle, mark the concrete application `Inference` and link the broader principle's reference.

- [ ] **Step 5: Attach at least one supporting reference to every non-Inference scientific claim**

For `Inference` items, cite the reference that supports the upstream principle and make the inference status explicit.

- [ ] **Step 6: Validate ID count and uniqueness**

Run:

```bash
python - <<'PY'
import re
from pathlib import Path
text = Path('catalog.md').read_text()
ids = re.findall(r'QOL-\d{3}', text)
unique = sorted(set(ids))
expected = [f'QOL-{i:03d}' for i in range(1, 101)]
assert unique == expected, (len(unique), set(expected)-set(unique), set(unique)-set(expected))
print('100 canonical QoL IDs present')
PY
```

Expected: `100 canonical QoL IDs present`.

- [ ] **Step 7: Validate reference tokens**

Run:

```bash
python - <<'PY'
import re
from pathlib import Path
catalog = Path('catalog.md').read_text()
refs = Path('references.md').read_text()
used = set(re.findall(r'REF-\d{3}', catalog))
defined = set(re.findall(r'^## (REF-\d{3})', refs, re.M))
missing = sorted(used - defined)
assert not missing, missing
print(f'{len(used)} referenced REF IDs resolve')
PY
```

Expected: no missing references.

- [ ] **Step 8: Commit**

```bash
git add catalog.md
git commit -m "docs: add initial 100-item QoL catalog"
```

---

### Task 4: Create thematic topic views

**Files:**
- Create: `topics/sleep.md`
- Create: `topics/physical-activity.md`
- Create: `topics/nutrition-weight.md`
- Create: `topics/mental-health.md`
- Create: `topics/attention-digital.md`
- Create: `topics/work-time.md`
- Create: `topics/environment.md`
- Create: `topics/social-relationships.md`
- Create: `topics/health-checks.md`

**Interfaces:**
- Consumes: canonical `QOL-*` IDs and `REF-*` IDs.
- Produces: readable thematic explanations without redefining item identity.

- [ ] **Step 1: Add a standard preamble to every topic file**

Use:

```markdown
> This is a thematic view of the canonical QoL catalog. Categories overlap by design. An item may appear in several topic pages; its canonical identity remains its `QOL-*` ID in `catalog.md`.
```

- [ ] **Step 2: Use the detail schema consistently**

For items that merit explanation, use:

```markdown
## QOL-XXX — Item name

**Categories:** category-a, category-b
**Evidence:** High | Moderate | Low | Inference
**Applicability:** General | Conditional

### Idea
### Why it may affect quality of life
### Evidence
### Practical applications
### Limitations and caveats
### References
```

- [ ] **Step 3: Populate `topics/sleep.md`**

Cover at minimum `QOL-001` through `QOL-011`, plus `QOL-042` through `QOL-045`, `QOL-069` through `QOL-074`, and `QOL-094` where sleep disruption is relevant.

- [ ] **Step 4: Populate `topics/physical-activity.md`**

Cover at minimum `QOL-033` through `QOL-041`, `QOL-076`, `QOL-089`, `QOL-090`, and `QOL-091`.

- [ ] **Step 5: Populate `topics/nutrition-weight.md`**

Cover at minimum `QOL-004`, `QOL-052` through `QOL-058`, `QOL-066` through `QOL-068`, and cross-link `QOL-095` when diet-related GI investigation is relevant.

- [ ] **Step 6: Populate `topics/mental-health.md`**

Cover at minimum `QOL-059` through `QOL-065`, `QOL-077` through `QOL-082`, `QOL-092`, and relevant cross-links to `QOL-017`, `QOL-021`, and `QOL-085`.

- [ ] **Step 7: Populate `topics/attention-digital.md`**

Cover `QOL-012` through `QOL-020`, `QOL-032`, `QOL-075`, and `QOL-090`.

- [ ] **Step 8: Populate `topics/work-time.md`**

Cover `QOL-021` through `QOL-032`, `QOL-080` through `QOL-090`, and `QOL-100`.

- [ ] **Step 9: Populate `topics/environment.md`**

Cover `QOL-007` through `QOL-010`, `QOL-042` through `QOL-048`, `QOL-083`, `QOL-084`, `QOL-098`, and `QOL-099`.

- [ ] **Step 10: Populate `topics/social-relationships.md`**

Cover `QOL-062` through `QOL-065`, `QOL-078`, `QOL-079`, `QOL-085`, and `QOL-086`.

- [ ] **Step 11: Populate `topics/health-checks.md`**

Cover `QOL-002`, `QOL-038`, `QOL-049` through `QOL-051`, `QOL-070` through `QOL-079`, and `QOL-093` through `QOL-097`.

- [ ] **Step 12: Keep practical inference labeled**

If a topic page says `hire a cleaner`, `order prepared meals`, `duplicate a charger`, or another concrete application not directly tested, prefix the paragraph or sentence with `Practical inference:`.

- [ ] **Step 13: Commit**

```bash
git add topics
git commit -m "docs: add thematic QoL topic views"
```

---

### Task 5: Cross-reference and quality audit

**Files:**
- Modify if needed: `README.md`
- Modify if needed: `catalog.md`
- Modify if needed: `references.md`
- Modify if needed: `topics/*.md`

**Interfaces:**
- Consumes: all knowledge-base files.
- Produces: a coherent first release with traceable claims and no personal data.

- [ ] **Step 1: Verify all catalog reference IDs resolve**

Run the reference-resolution script from Task 3 again.

Expected: zero missing `REF-*` IDs.

- [ ] **Step 2: Verify every canonical item exists exactly once in the catalog**

Run the ID-validation script from Task 3 again.

Expected: exactly `QOL-001` through `QOL-100`.

- [ ] **Step 3: Verify the repository can grow beyond 100 items**

Read `README.md` and confirm it explicitly explains how to add `QOL-101`, a new category, and a multi-category item without renumbering existing IDs.

- [ ] **Step 4: Verify flexible categories are visible in real data**

Confirm at least ten catalog entries have two or more category tags and at least one has four or more category tags.

- [ ] **Step 5: Search for personalized content**

Run:

```bash
grep -RniE 'Bruno|103 kg|1\.85|escitalopram|pregabalina|IBMP|demit|sal[aá]rio|qualidade de vida.*6\.5' README.md catalog.md references.md topics || true
```

Expected: no matches.

- [ ] **Step 6: Search for unsupported certainty language**

Review uses of words equivalent to `proves`, `guarantees`, `will improve`, and `always`. Replace with study-specific language unless the statement is genuinely established at that strength.

- [ ] **Step 7: Verify primary-source preference**

For each material evidence claim, confirm the linked `REF-*` points to the primary study or official source when one is available. Keep any necessary secondary source explicitly labeled.

- [ ] **Step 8: Verify inference labeling**

Review `QOL-022` through `QOL-028`, `QOL-053`, `QOL-088`, `QOL-098`, `QOL-099`, and `QOL-100` closely. Any concrete application extrapolated from broader evidence must remain `Inference` or be backed by its own direct evidence.

- [ ] **Step 9: Verify Markdown navigation**

Confirm README links to `catalog.md`, `references.md`, and every `topics/*.md` file. Confirm every topic file points back to the catalog and references registry.

- [ ] **Step 10: Commit audit fixes**

```bash
git add README.md catalog.md references.md topics
git commit -m "docs: audit QoL catalog evidence and cross-references"
```

---

## Plan Self-Review

### Spec coverage

- Canonical scan-friendly map: Task 3.
- Stable item IDs: Task 3 and Task 5.
- Multi-category items: Tasks 1, 3, and 5.
- New categories without restructuring: Tasks 1 and 5.
- Evidence vs inference: Tasks 1, 2, 3, 4, and 5.
- Primary-source preference: Tasks 2 and 5.
- Evidence limitations visible: Tasks 2, 3, and 4.
- Reusable references: Task 2.
- Topic pages: Task 4.
- Growth beyond 100: Tasks 1 and 5.
- No personal audit data: Global Constraints, Task 1, Task 5.

### Placeholder scan

The plan contains no `TBD`, `TODO`, `implement later`, or unspecified test steps. Source verification is explicit because bibliographic metadata must be checked against the primary source at implementation time rather than guessed in the plan.

### Consistency

- Canonical item identity is always `QOL-*`.
- Canonical bibliography identity is always `REF-*`.
- Topic files are non-owning views.
- Category values are lower-case kebab-case tags and may be multi-valued.
- Evidence and applicability vocabularies match the approved design.
