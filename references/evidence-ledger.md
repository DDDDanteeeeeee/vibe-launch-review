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

When user data, uploaded files, model calls, logs, or stored outputs are involved, add one short data/privacy note:

- What data is involved, where it goes, what log/access/retention/deletion proof exists, and whether this affects current scope or public launch.

Do not turn this into a separate legal compliance section.

## Freshness Labels

- `Verified in this review`: checked directly during this review.
- `Previously verified, not rerun`: credible prior evidence exists, but the current review did not rerun it.
- `Not verified`: evidence is missing, claimed without proof, or outside the reviewed material.

Do not collapse these labels. The distinction matters because a path can support a controlled pilot based on earlier proof while still needing fresh release evidence before public launch.

## Scope Effect Labels

Use direct language:

- Blocks current allowed scope: Yes / No. Why:
- Blocks public self-serve launch or large-scale release: Yes / No. Why:

Do not write only launch
