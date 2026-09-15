# Personal QoL Profile

The Personal QoL Profile records how the repository owner's life relates to the general QoL Knowledge Base without changing the evidence or meaning of canonical `QOL-*` records.

## Profile model

**Personal QoL Profile**:
A structured record of current observations, subjective satisfaction, preferences, targets, priorities, and trade-offs for one person. It may reference `QOL-*` items but does not provide scientific evidence for them.
_Avoid_: QoL Knowledge Base, clinical record

**Personal Observation**:
A dated factual description of the person's current state relevant to a `QOL-*` item or coverage domain. Observation status may be `meets`, `partial`, `does_not_meet`, `not_applicable`, or `unknown` when that classification is useful.
_Avoid_: diagnosis, evidence claim

**Personal Position**:
The person's expressed importance, desirability, preference, or willingness concerning a QoL domain or possible change. It is independent of Evidence Strength.
_Avoid_: recommendation strength

**Personal Target**:
A chosen next state or longer-term direction. A target can intentionally be less ambitious than a general evidence-backed target when that is the person's realistic next step.
_Avoid_: evidence-based recommendation

**Personal Priority**:
The person's ordering of changes or domains for attention. It records preference and sequencing, not clinical urgency or Evidence Strength.
_Avoid_: evidence priority, risk ranking

**Accepted Trade-off**:
A deliberate choice not to optimize an evidence-favored dimension because another valued outcome, constraint, cost, or preference takes precedence.
_Avoid_: failure, nonadherence

**Sensitive Health Context**:
Personal diagnosis, treatment, medication, symptom, or care information retained because it materially affects applicability or interpretation of the profile. It remains personal context and never becomes a canonical Evidence Claim.

## Boundaries

- `personal/` may contain private health, medication, relationship, work, financial, and lifestyle information because this repository is private and personally owned.
- Personal information must remain under the `personal/` bounded context.
- `QOL-*`, `REF-*`, `IMP-*`, Categories, Evidence Claims, Evidence Strength, and generated knowledge-base views must not be derived from personal records.
- A Personal Observation may link to a `QOL-*`, but that link means "applied to this person", not "evidence for this item".
- A WHOQOL or other Coverage Framework may guide personal questioning, but informal answers do not constitute a validated instrument score.
- Git history may retain sensitive information after ordinary file deletion; recording Sensitive Health Context is therefore a deliberate persistence decision.
