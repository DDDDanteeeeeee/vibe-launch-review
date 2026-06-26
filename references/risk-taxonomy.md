# Vibe Launch Review Risk Taxonomy

Use this reference only for the five review areas. The goal is to identify public-launch risk and give audit-level recommendations, not to design or implement fixes.

## Evidence Labels

- `confirmed`: The issue is visible in code, diff, UI, docs, config, screenshot, or user-provided material.
- `suspected`: The materials suggest a risk, but the evidence is incomplete.
- `evidence_gap`: The review cannot determine whether the required guardrail exists.

## Severity Labels

- `BLOCKER`: Do not recommend public launch until this is addressed or disproven.
- `HIGH`: Risk is material for public launch and should be resolved before broad release.
- `MEDIUM`: Risk matters but may be acceptable for controlled beta.
- `LOW`: Useful improvement or documentation gap.

## Project-Type Weighting

Do not treat the five gates as a checklist that must produce five findings. First classify the product, then decide which gates actually apply.

Use these applicability labels:

- `Primary`: central to this product's real user flow or cost surface.
- `Secondary`: present but limited, private, or lower exposure.
- `Not applicable`: no matching surface exists in the reviewed materials.
- `Unknown`: the product type suggests the surface may exist, but the materials do not prove it.

Common weighting patterns:

| Product type | Usually primary | Often not applicable |
| --- | --- | --- |
| Standalone desktop or local utility | AI prompt/model-call exposure if it calls a model; demo-to-public-product gap; file handling if files leave the device | UGC moderation, SMS/email abuse, public upload risk when there is no cloud upload |
| AI SaaS or API product | AI prompt/model-call exposure, demo-to-public-product gap, SMS/email if account flows send codes | UGC moderation if there is no public user content |
| Community, social, marketplace, forum, or review product | UGC moderation, demo-to-public-product gap, SMS/email if account flows send codes | Image/file upload only if uploads exist |
| Image, media, document, or import product | Image/file upload risk, demo-to-public-product gap, AI exposure if model calls exist | UGC moderation if content is never public or shared |
| Static site or read-only marketing page | Demo-to-public-product gap only if hidden admin/demo features exist | SMS/email, UGC, upload, AI model-call gates when no matching surface exists |

If a gate is `Not applicable`, explain the reason and do not lower the verdict for it. If the reviewed materials are silent but the product type makes the gate plausible, use `Unknown` or `evidence_gap`.

## Business Model And Scope Calibration

Do not judge every product as a public, free, self-serve SaaS. First classify the current launch scope and commercial model:

- `internal_demo`: trusted operators only.
- `trusted_beta`: invited testers, limited access.
- `controlled_paid_pilot`: real users, paid or quota-based access, manual follow-up, limited distribution.
- `public_self_serve`: unknown users can sign up, pay, or use without operator review.
- `large_scale_public_release`: public promotion, high traffic, or mostly unattended operations.

For a `controlled_paid_pilot`, missing public-scale protection can justify `CONDITIONAL_LAUNCH` instead of `BLOCK_PUBLIC_LAUNCH` when the core business loop is proven and operator follow-up is explicit. For `public_self_serve` or `large_scale_public_release`, the same missing protection can block launch.

Use the four-stage workflow and Evidence Ledger to make this distinction explicit. The review should show what evidence supports the current allowed scope, what proof is stale, and what missing evidence blocks public self-serve launch.

## Data And Privacy Handling View

Data and privacy handling does not create a sixth gate. Use it only when it affects one of the five existing gates.

For AI, upload, UGC, or demo-to-product findings, ask the simple user-facing questions:

- What data or files does the product collect?
- Is that data necessary for the task?
- Does the product send only necessary context to the cloud or model provider?
- Who can access user data, uploaded files, prompts, model outputs, and logs?
- How long is the data or log kept?
- Is there a visible cleanup or deletion path?
- Can the reviewed evidence prove these controls exist?

Risk wording:

- Public users may submit personal, customer, or business-sensitive data without knowing where it goes or how long it stays.
- Logs, model calls, or storage can turn a working demo into a privacy or confidentiality risk.
- Missing data-handling proof can be acceptable for a tightly controlled manual pilot, but it should block public self-serve launch when sensitive data, files, or AI context are involved.

Audit-level recommendations:

- Recommend re-review with evidence for data path, model context, log redaction, access, retention, and deletion.
- Do not claim legal compliance. State the visible evidence gap and its effect on launch scope.

Calibration pattern:

| Pattern | Correct weighting |
| --- | --- |
| Standalone desktop app + cloud model proxy + prepaid points + manual code issuance | Treat model-call exposure and demo-to-public gap as primary. Treat prepaid balance as partial cost-control evidence. Require public-scale queue, rate, budget, alert, and resilience evidence before broad release. |
| Free public AI route without quota or account binding | Treat as blocker-level model-call exposure for public launch. |
| Manual operator service with no public self-serve route | Separate operator-process risk from public abuse risk. Do not invent public-route findings without evidence. |

Public self-serve AI SaaS contrast:

- Unknown users can access the model route without operator review.
- A free trial, public signup, or self-serve purchase flow can scale cost quickly.
- Missing per-user/per-IP limits, provider budget caps, alerts, queue controls, or circuit breakers should block public self-serve launch until evidence exists.

## Scope Impact For Each Risk

Every risk should say which launch scope it affects:

- Blocks current controlled scope? Use this when the risk can hurt a small paid pilot even with manual follow-up.
- Blocks public self-serve or large-scale release? Use this when the risk becomes unacceptable once unknown users can use the product at scale.
- Why? Explain the practical reason in one sentence.

Do not collapse these into one generic launch
