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

Calibration pattern:

| Pattern | Correct weighting |
| --- | --- |
| Standalone desktop app + cloud model proxy + prepaid points + manual code issuance | Treat model-call exposure and demo-to-public gap as primary. Treat prepaid balance as partial cost-control evidence. Require public-scale queue, rate, budget, alert, and resilience evidence before broad release. |
| Free public AI route without quota or account binding | Treat as blocker-level model-call exposure for public launch. |
| Manual operator service with no public self-serve route | Separate operator-process risk from public abuse risk. Do not invent public-route findings without evidence. |

## Scope Impact For Each Risk

Every risk should say which launch scope it affects:

- Blocks current controlled scope? Use this when the risk can hurt a small paid pilot even with manual follow-up.
- Blocks public self-serve or large-scale release? Use this when the risk becomes unacceptable once unknown users can use the product at scale.
- Why? Explain the practical reason in one sentence.

Do not collapse these into one generic "launch risk" statement. The same evidence gap can be acceptable for a manually operated pilot and still block public launch.

## Fixed Calibration Case: AI Catalog

Use AI Catalog as a standing calibration case for controlled paid pilots:

- Product type: Windows Electron desktop app that processes Illustrator `.ai` files locally.
- Cloud boundary: the client calls `/api/translate/batch`; the client does not include the DeepSeek key and users do not configure a model key.
- Commercial model: users buy outside the app, then an operator manually issues activation or points codes.
- Cost control: users redeem points before tasks run; the cloud charges by `taskId`; model failure refunds points.
- Prior evidence: a real DeepSeek smoke previously translated a short sentence and charged 1 point; a real `.ai` smoke previously hit 22 text boxes with 0 errors.
- Freshness rule: if the current review lacks `ADMIN_TOKEN`, mark the DeepSeek and charge path as `Previously verified, not rerun`, not as "not working" or "never proven".
- Delivery quality gap: if Illustrator is not reopened to inspect the final `.ai` layout, mark that as a delivery-quality evidence gap.
- Current-scope interpretation: missing per-IP, per-device, or per-license limits should not directly block a controlled paid pilot because prepaid points limit one account's cost.
- Public-scope interpretation: the same missing limits still block public self-serve launch or large-scale release until rate, queue, budget, alert, circuit-breaker, production env/log, and clean Windows profile install evidence exists.

Correct verdict for this case: `CONDITIONAL_LAUNCH`.

Allowed scope: controlled paid pilot.

Blocked scope: public self-serve launch / large-scale public release.

## 1. SMS Or Email Interface Abuse

Review any user-triggered cost path such as SMS code, email code, invite email, notification send, password reset, or magic link.

Look for:

- No visible per-user, per-IP, per-device, or global send limits.
- No daily budget or provider-spend guardrail.
- No anomaly alerting or abuse monitoring evidence.
- Public route that triggers paid sends without authentication or challenge.
- Repeated send endpoint that can be scripted cheaply.

Risk wording:

- Attackers can burn provider spend, degrade service, or use the product as a spam relay.
- Public launch can convert a small demo endpoint into a direct cost sink.

Audit-level recommendations:

- Recommend blocking public launch until abuse limits and budget evidence are provided.
- Recommend beta-only launch if limits are claimed but not evidenced.
- Recommend re-review with rate-limit, budget, and alerting proof.

## 2. UGC Moderation Gaps

Review user-generated content such as comments, posts, messages, profile text, nicknames, avatars, reviews, shared pages, and public submissions.

Look for:

- UGC appears publicly without prior review, filtering, queueing, reporting, or takedown evidence.
- User text is rendered directly into public pages.
- No visible moderation workflow for illegal, abusive, spam, adult, violent, or brand-damaging content.
- No evidence of audit trail or author accountability for public UGC.

Risk wording:

- Public users can publish harmful or illegal content through the product.
- The product owner may inherit platform, brand, or legal risk from user content.

Audit-level recommendations:

- Recommend blocking public launch for public UGC with no moderation evidence.
- Recommend private beta if content visibility is limited and moderation responsibility is still unresolved.
- Recommend re-review with moderation flow, reporting, and takedown evidence.

## 3. Image Or File Upload Risk

Review avatar upload, image upload, document upload, media upload, import flows, and object storage access.

Look for:

- No visible file size limit.
- No visible file type or MIME validation.
- No content review for public images.
- Public object URLs that appear enumerable or unrestricted.
- Uploads stored in a shared public bucket without access separation evidence.
- No evidence of storage cost limits, hotlink protection, or cleanup.

Risk wording:

- Attackers can upload harmful files, consume storage or bandwidth, expose private files, or turn storage into a public hosting surface.
- Image upload is a public attack and cost surface, not just a UI feature.

Audit-level recommendations:

- Recommend blocking public launch for public upload flows without validation and access evidence.
- Recommend re-review with upload limits, access model, public/private storage evidence, and content review evidence.

## 4. AI Prompt And Model-Call Exposure

Review AI chat, generation, summarization, translation, classification, agents, model routes, and frontend prompt logic.

Look for:

- System prompts, hidden policy prompts, provider keys, model tokens, or privileged instructions exposed in frontend code or client config.
- Model routes callable by unauthenticated or unlimited users.
- No visible quota, rate limit, or budget protection for model calls.
- No input or output review evidence for public AI features.
- Model output displayed, executed, emailed, posted, or stored without review in sensitive contexts.

Risk wording:

- Attackers can steal prompts or keys, burn model spend, coerce unsafe outputs, or make the AI feature a public abuse surface.
- Public AI features combine cost risk, content risk, and data leakage risk.

Audit-level recommendations:

- Recommend blocking public launch if keys or system prompts are exposed.
- Recommend blocking or beta-only status if public model calls lack visible quota or moderation evidence.
- Recommend re-review with server-side prompt/key boundary and model input/output review evidence.

## 5. Demo-To-Public-Product Gap

Review whether the product still assumes trusted demo users rather than unknown public users.

Look for:

- Mock authentication, hardcoded admin users, test passwords, demo tokens, or default accounts.
- Frontend-only permission checks or hidden buttons without server-side enforcement evidence.
- Debug pages, seed routes, test routes, admin routes, or development panels reachable in launch builds.
- Logs, errors, or UI messages that expose internals or secrets.
- Public routes that assume low traffic, trusted users, or manual operator cleanup.

Risk wording:

- The product may function as a demo but fail as a public service.
- Unknown users can exploit assumptions that were harmless during local testing.

Audit-level recommendations:

- Recommend blocking public launch for mock auth, exposed admin paths, or frontend-only enforcement.
- Recommend private beta if the app has a controlled-user assumption that is not yet removed.
- Recommend re-review with production-auth, route-access, and demo-removal evidence.

## Verdict Guidance

Use `BLOCK_PUBLIC_LAUNCH` when a confirmed or strongly suspected `BLOCKER` exists.

Use `PRIVATE_BETA_ONLY` when the product may be safe for trusted testers but lacks evidence for public exposure.

Use `CONDITIONAL_LAUNCH` when no blocker is found, but high-risk evidence gaps remain.

Use `PUBLIC_LAUNCH_READY` only when the five review areas are either not applicable or have sufficient visible guardrail evidence.
