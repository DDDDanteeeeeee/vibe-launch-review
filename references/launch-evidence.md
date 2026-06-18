# Launch Evidence Guide

Use this guide to decide what evidence is enough for a real launch review.

## Evidence Quality

Prefer evidence in this order:

1. Code, routes, configuration, policy, or tests visible in the reviewed materials.
2. Screenshots or product notes that show the guardrail and its user-visible behavior.
3. Explicit user-provided release notes or architecture notes.
4. Claims without supporting material.

Claims without proof should usually become `evidence_gap`, not `Pass`.

## Applicability Evidence

Evidence can also prove that a gate is not applicable. Useful proof includes product notes, routes, UI screenshots, release notes, or code showing that the product has no matching surface.

Examples:

- No comments, posts, profiles, public submissions, shared pages, or public user text can make UGC moderation `Not applicable`.
- No SMS, email, magic-link, invite, notification, or password-reset send path can make SMS/email interface abuse `Not applicable`.
- Local-only file selection can make public upload risk `Not applicable`, but only if the reviewed material shows files are not uploaded to public storage or a shared cloud bucket.
- No AI feature or model route can make AI prompt/model-call exposure `Not applicable`.

Do not use `Not applicable` when the materials simply omit evidence for a likely surface. In that case, use `Unknown` or `evidence_gap`.

## Evidence Freshness

Separate evidence by freshness:

- **Verified in this review**: evidence checked or rerun during the current review.
- **Previously verified, not rerun**: credible earlier smoke tests, build records, release notes, screenshots, or logs that were not rerun in the current review.
- **Not verified**: claims, assumptions, missing screenshots, missing configs, or environments not inspected.

Do not say "not verified" when there is credible previous evidence. Instead, say what was previously verified and what was not rerun this time.

For delivery acceptance reports, turn freshness into plain language. Example: "This path has passed a previous smoke test, but we did not rerun it in this review."

## Business Model And Launch Scope Evidence

Before deciding whether a missing guardrail blocks launch, collect evidence for:

- How users receive access: manual activation code, invite, self-serve signup, or public anonymous use.
- How users pay or receive quota: prepaid points, subscription, manual invoice, marketplace purchase, free public quota, or internal budget.
- Where costly actions happen: client device, cloud proxy, third-party provider, or operator workstation.
- What stops cost: point balance, subscription quota, provider cap, queue limit, rate limit, operator approval, or manual shutdown.
- What scope is being reviewed: internal demo, controlled commercial pilot, public self-serve launch, or large-scale public release.

Use this evidence to separate current-scope blockers from public-launch blockers.

Example: in a desktop app that uses a server-side model proxy and prepaid points, the point balance is evidence that one account cannot spend beyond its balance. That reduces controlled-pilot cost risk. It does not prove public-scale rate limits, queue protection, provider spend caps, anomaly alerts, or resilience under many unknown users.

AI Catalog calibration:

- Previously verified, not rerun: real DeepSeek smoke translated a short sentence and charged 1 point; real `.ai` smoke hit 22 text boxes with 0 errors, when the current review did not rerun them.
- Not verified: final Illustrator layout inspection, clean Windows profile install, production server env permission review, log redaction review, public-scale per-IP/per-device/per-license limits, budget caps, alerts, and circuit breakers when those were not inspected in this review.
- Scope effect: the previous smoke evidence can support a controlled paid pilot, but the missing public-scale evidence should still block public self-serve launch or large-scale public release.

## Minimum Evidence By Gate

### SMS Or Email Interface Abuse

Useful evidence:

- Send-rate limits by user, IP, device, or account.
- Daily budget caps or provider spend limits.
- Monitoring or anomaly alert notes.
- Authentication or challenge boundary for public send routes.

Missing evidence should block or restrict public launch when paid sends are public-facing.

### UGC Moderation

Useful evidence:

- Pre-publication review, queueing, filtering, reporting, or takedown flow.
- Public/private visibility rules.
- Author accountability or audit trail.
- Moderation ownership for private beta or public launch.

Public UGC without visible moderation is a launch risk even when the app works.

### Image Or File Upload

Useful evidence:

- File size limit.
- File type and MIME validation.
- Public/private access model.
- Storage bucket separation.
- Bandwidth, hotlink, cleanup, or retention guardrails.
- Content review when uploads become public.

Upload flows should be treated as attack and cost surfaces.

### AI Prompt And Model-Call Exposure

Useful evidence:

- Prompts and keys stay server-side.
- Public model calls have quota, rate limit, or budget controls.
- AI inputs and outputs have review boundaries for public display, posting, emailing, or storage.
- Logs do not expose sensitive prompts, keys, or user data.

Client-exposed prompts or keys are blocker-level findings.

### Demo-To-Public-Product Gap

Useful evidence:

- Production auth replaces mock auth.
- Admin and debug routes are absent or protected in launch builds.
- Server-side authorization protects sensitive actions.
- Default accounts, seed routes, and test tokens are removed.
- Errors and logs do not expose internals to users.

If a product still relies on trusted demo assumptions, use `PRIVATE_BETA_ONLY` or `BLOCK_PUBLIC_LAUNCH`.

## Recommendation Boundary

Recommendations should say what class of proof or protection is needed. Do not give implementation code, patches, package names, or service-specific integration steps.
