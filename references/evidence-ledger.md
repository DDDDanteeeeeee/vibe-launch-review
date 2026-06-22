# Evidence Ledger

Use the Evidence Ledger to stop launch decisions from being based on vague confidence.

The ledger is a compact proof table created before the final verdict. It should be clear enough for an engineer to audit, but short enough that a founder or operator can still understand what matters.

## Required Fields

| Field | Purpose |
| --- | --- |
| Evidence item | The route, feature, behavior, file, screenshot, test, note, or missing proof being judged. |
| Source | Where the evidence came from: current review, earlier smoke test, release note, screenshot, user note, or missing material. |
| Evidence freshness | `Verified in this review`, `Previously verified, not rerun`, or `Not verified`. |
| Related gate | One of the five Vibe Launch Review gates. |
| Current allowed scope effect | Whether this item blocks the current allowed scope. |
| Public scope effect | Whether this item blocks public self-serve launch or large-scale release. |
| Needed proof | What proof is needed before a stronger decision. |

## Freshness Labels

- `Verified in this review`: checked directly during this review.
- `Previously verified, not rerun`: credible prior evidence exists, but the current review did not rerun it.
- `Not verified`: evidence is missing, claimed without proof, or outside the reviewed material.

Do not collapse these labels. The distinction matters because a path can support a controlled pilot based on earlier proof while still needing fresh release evidence before public launch.

## Scope Effect Labels

Use direct language:

- Blocks current allowed scope: Yes / No. Why:
- Blocks public self-serve launch or large-scale release: Yes / No. Why:

Do not write only "launch risk". Say which launch scope is affected.

## Report Usage

For audit reports, include an `Evidence Ledger` section when it helps show why the verdict is scoped.

For product delivery acceptance reports, do not dump a long raw ledger by default. Instead, fold the ledger into:

- Verified Paths
- Module Acceptance Table
- Current Risks And Blockers
- Must-Have Before Public Launch

If the user asks for the raw review record, include the full ledger.

## AI Catalog Calibration

AI Catalog is the controlled paid pilot calibration case:

- Real DeepSeek smoke and point deduction were previously verified.
- Real `.ai` file smoke was previously verified.
- If the current review lacks `ADMIN_TOKEN`, those paths are `Previously verified, not rerun`, not `Not verified`.
- Missing per-IP, per-device, or per-license limits do not directly block the controlled paid pilot because prepaid points limit one account's cost.
- The same missing protections still block public self-serve launch or large-scale public release.

Correct interpretation: `CONDITIONAL_LAUNCH` with allowed scope `controlled paid pilot` and blocked scope `public self-serve launch / large-scale public release`.

## Public Self-Serve AI SaaS Contrast

A public AI SaaS is different:

- Unknown users can sign up or use the product without operator review.
- Model calls can create direct provider cost.
- Abuse can scale before an operator notices.

For this context, missing quota, rate limits, budget caps, alerts, queue controls, or circuit breakers should normally block public self-serve launch until evidence is provided.
