# QoL Knowledge Base

The QoL Knowledge Base organizes evidence-backed, decision-relevant propositions about changes, assessments, and guardrails that may affect quality of life.

## Items

**QoL Item**:
A stable, decision-relevant proposition about an intervention, assessment, or evidence guardrail that may affect quality of life. A `QOL-*` identifier represents one proposition, not the broader subject it concerns.
_Avoid_: concept, tip, topic, factor

**Item Statement**:
The canonical proposition identified by a QoL Item. It states the decision, assessment, or guardrail represented by the `QOL-*` identity.

**Item Kind**:
The semantic role of a QoL Item: Intervention, Assessment, or Guardrail.

**Intervention**:
A QoL Item proposing an action intended to change a behavior, exposure, environment, condition, or other quality-of-life determinant.

**Assessment**:
A QoL Item proposing measurement, evaluation, investigation, or review to inform a subsequent decision.

**Guardrail**:
A QoL Item that constrains a conclusion or practice when the available evidence does not justify a stronger claim.

**QoL Relevance**:
The defensible connection between a QoL Item and lived well-being, symptoms, function, participation, safety, or clinically relevant morbidity.

## Applicability

**Applicability**:
Whether a QoL Item is broadly relevant without a specific trigger (`General`) or depends on an explicit condition (`Conditional`). General does not mean universally appropriate.

**Applicability Condition**:
A circumstance, symptom, exposure, diagnosis, preference, or other condition that must be present for a Conditional QoL Item to be relevant.

## Evidence

**Evidence Claim**:
A narrow factual proposition supported by one or more References and used to support or constrain a QoL Item.

**Claim Role**:
The semantic role of an Evidence Claim: Support or Constraint.

**Support Claim**:
An Evidence Claim necessary to justify the material proposition of a QoL Item.

**Constraint Claim**:
An Evidence Claim that limits, qualifies, or establishes a material risk or condition without serving as the primary justification for the QoL Item.

**Evidence Strength**:
Confidence in an Evidence Claim, expressed as High, Moderate, or Low. A QoL Item's Evidence Strength is derived from the weakest Support Claim necessary to justify its statement.
_Avoid_: Inference

**Support Mode**:
Whether the evidence supports the QoL Item proposition directly or the item applies broader evidence by inference. Values are Direct and Inferred.

**Reference**:
A reusable `REF-*` identity for a citably distinct source or materially relevant version of a source. Its identity is not its URL.

## Implementation

**Implementation Option**:
A stable, concrete way to enact one or more QoL Items without carrying independent evidential authority. An `IMP-*` identifier represents the option itself, such as a product class, service arrangement, subscription, or no-cost implementation.
_Avoid_: product, purchase, tip

**Implements**:
The relationship from an Implementation Option to the QoL Item propositions it puts into practice. It does not imply that the Implementation Option itself was directly tested.

**Acquisition Mode**:
How an Implementation Option is obtained: Purchase, Service, Subscription, or Free.
_Avoid_: item type

## Classification and views

**Category**:
A canonical but extensible retrieval tag applied to QoL Items. Categories do not determine item identity or ownership.
_Avoid_: section, primary category

**Topic View**:
A non-canonical thematic presentation of related QoL Items. Topic membership and editorial prose are presentation choices; displayed item statement, kind, categories, Evidence Strength, applicability, Support Mode, lifecycle status, and canonical links are derived from the referenced QoL Items and References.
_Avoid_: category, owner, independent metadata registry

## Lifecycle

**Active QoL Item**:
A QoL Item that currently represents a canonical decision-relevant proposition.

**Deprecated QoL Item**:
A preserved `QOL-*` identity that no longer represents an active canonical proposition. It records why it was deprecated and may point to zero, one, or several replacement QoL Items.
_Avoid_: deleted item, reused ID

**Active Reference**:
A Reference that may be used as current evidential support.

**Deprecated Reference**:
A preserved `REF-*` identity that should no longer be used as current evidential support. It records why it was deprecated and may identify a replacement Reference.

**Active Implementation Option**:
An Implementation Option that currently represents a canonical way to enact one or more Active QoL Items.

**Deprecated Implementation Option**:
A preserved `IMP-*` identity that no longer represents an active canonical implementation. It records why it was deprecated and may point to zero, one, or several replacement Implementation Options.

## Relationships

**Item Relationship**:
A typed semantic relationship between distinct QoL Items that does not affect either item's identity.

**Informs**:
An Item Relationship in which one QoL Item provides information useful for deciding or applying another.
_Avoid_: requires, precedes
