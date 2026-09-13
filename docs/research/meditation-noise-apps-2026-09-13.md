# Meditation and sound-masking apps: Medito and Metiq

## Summary

Medito and Metiq fit the QoL repository as current examples attached to generic Implementation Options. They should not become QoL Items or vendor-specific canonical identities.

The repository already contains the decision-level propositions needed for both cases:

- [QOL-061](../../items/QOL-061.md) treats meditation or mindfulness as a conditional tool rather than a universal remedy.
- [QOL-008](../../items/QOL-008.md) warns against assuming that white or pink noise improves sleep and supports conditional testing instead.

The product sources verify access and feature characteristics. They do not establish independent causal evidence for quality-of-life or sleep outcomes. The linked QoL Items continue to carry the evidence boundary.

## Verified facts

### Medito

The Medito Foundation's repository states that Medito is free, has no ads, does not require sign-up or payment, and is available on Android and iOS. See the first-party README at commit `9e4613f3b20aa0a4555e40c6a449ca738d973fad`, [lines 5-15](https://github.com/meditohq/medito-app/blob/9e4613f3b20aa0a4555e40c6a449ca738d973fad/README.md#L5-L15).

The same README states that the app code is under the GNU Affero General Public License, while Medito content uses a separate custom license. See [lines 137-143](https://github.com/meditohq/medito-app/blob/9e4613f3b20aa0a4555e40c6a449ca738d973fad/README.md#L137-L143).

These facts support Medito as a low-friction example of a free guided-meditation app. They do not show that Medito itself improves stress, anxiety, attention, or quality of life.

### Metiq

Metiq's repository states that the Android app provides white, pink, brown, and grey noise, ambient sound mixes, a sleep timer, offline operation, and no account, cloud, tracking, or ads. The project also states that the app is free and targets Android 9 or newer. See the first-party README at commit `bc63c81f553479d4180c16a870ade21de1dd998e`, [lines 34-70](https://github.com/metiq-xyz/android-app/blob/bc63c81f553479d4180c16a870ade21de1dd998e/README.md#L34-L70).

The same README states that Metiq is licensed under GPLv3 or later. See [lines 85-88](https://github.com/metiq-xyz/android-app/blob/bc63c81f553479d4180c16a870ade21de1dd998e/README.md#L85-L88).

The repository also describes binaural-beat features. That description is a product capability claim, not evidence that binaural beats improve sleep, relaxation, focus, or quality of life. The QoL knowledge base should not promote that claim without a separate evidence review.

## Repository fit

The repository defines an Implementation Option as a concrete reusable way to enact one or more QoL Items, such as a product class or no-cost implementation. [CONTEXT.md](../../CONTEXT.md) treats the option as distinct from the evidence-bearing proposition. [CONTRIBUTING.md](../../CONTRIBUTING.md) also says that Implementation Options should describe reusable classes rather than unsupported vendor endorsements.

That structure favors two generic additions:

1. **Free guided meditation app**, implementing `QOL-061`. Medito is a current first-party-verified example.
2. **Free noise and ambient-sound generator app**, implementing `QOL-008`. Metiq is a current first-party-verified example.

Keeping the canonical identities generic avoids coupling stable `IMP-*` records to a vendor, store listing, product name, or maintenance status that can change independently of the underlying implementation class.

## Evidence boundaries and caveats

- A guided meditation app should be presented as a way to try a conditional mindfulness practice. It should not be presented as a substitute for indicated treatment or as a universally effective intervention.
- A noise generator should be presented as a way to test masking conditionally. `QOL-008` specifically prevents the repository from implying that adding continuous white or pink noise improves sleep by default.
- Product features such as privacy posture, platform support, price, and licensing may change. The first-party links above capture the state reviewed on 2026-09-13.
- Medito's app code and meditation content have different licenses. Calling the whole content catalog open source would be inaccurate.
- Metiq's binaural-beat feature should remain outside the evidence claims until the repository performs a separate review of that intervention.

## Recommendation

Add the two generic Implementation Options and mention Medito and Metiq only as current examples in their explanatory prose. Do not create new QoL Items, new References, or new evidence-strength claims for either app.

## Primary sources

- Medito Foundation. `meditohq/medito-app`, README at commit `9e4613f3b20aa0a4555e40c6a449ca738d973fad`: https://github.com/meditohq/medito-app/blob/9e4613f3b20aa0a4555e40c6a449ca738d973fad/README.md
- Metiq. `metiq-xyz/android-app`, README at commit `bc63c81f553479d4180c16a870ade21de1dd998e`: https://github.com/metiq-xyz/android-app/blob/bc63c81f553479d4180c16a870ade21de1dd998e/README.md
- QoL project domain model: [CONTEXT.md](../../CONTEXT.md)
- QoL contribution rules: [CONTRIBUTING.md](../../CONTRIBUTING.md)
- Existing meditation guardrail: [QOL-061](../../items/QOL-061.md)
- Existing white/pink-noise guardrail: [QOL-008](../../items/QOL-008.md)
