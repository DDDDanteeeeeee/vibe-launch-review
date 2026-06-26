# Vibe Launch Review

## Verdict

`BLOCK_PUBLIC_LAUNCH`

PromptShelf AI should not open as a public self-serve launch yet. The product is a public AI SaaS with unknown users, self-serve access, email flows, and a paid model route. The provided packet does not show the rate limit, budget cap, alerting, queue control, or circuit breaker evidence needed before public traffic.

- Allowed scope: limited private testing with known users and operator monitoring.
- Blocked scope: public self-serve launch / large-scale public release.
- Why: working UI evidence is not enough when unknown users can trigger paid model calls and email sends.

This review follows the four-stage workflow and does not implement fixes, generate patches, configure services, or replace a broader security audit.

## Reviewed Material

- `examples/function-tests/public-self-serve-ai-saas-input.md`
- Evidence limits: product notes only; no route code, quota config, rate-limit config, provider budget cap, monitoring screenshot, alert policy, or circuit-breaker evidence was provided.

## Context Intake And Review Focus

- Product type: public self-serve AI SaaS.
- User exposure: unknown public users.
- Commercial model: free trial plus self-serve paid upgrade.
- Launch scope: public self-serve launch.
- Operator model: mostly self-serve after signup.
- Costly or sensitive actions: email sends and LLM calls through `/api/generate`.
- Content surface: private generated drafts, not public UGC.
- Gates that matter most: AI prompt/model-call exposure, SMS/email interface abuse, and demo-to-public-product gap.

This is not a controlled paid pilot. Because unknown users can create accounts and trigger paid model calls, missing public-scale cost controls are public-launch blockers.

## Data And Privacy Handling Feedback

- What data or files are involved: user prompts, generated drafts, account email addresses, and likely request logs for `/api/generate`.
- Where they go: user prompts and generation context go from the public web app to the backend route and then to the model provider. The packet does not show whether logs store full prompts or generated output.
- Log, access, retention, or deletion evidence: not provided. There is no proof for prompt log redaction, operator access limits, retention duration, or user deletion behavior.
- Impact on current allowed scope: this does not block limited private testing with known users if operators explain the data handling limits and watch usage manually.
- Impact on public launch: this blocks public self-serve launch until prompt/log handling, access, retention, deletion, and model-call cost controls have visible proof.

## Gate Applicability

| Gate | Applicability | Reason |
| --- | --- | --- |
| SMS/email interface abuse | Primary | Email verification and password reset can create provider cost or spam risk. |
| UGC moderation | Not applicable | The launch packet shows no comments, public posts, public profiles, shared gallery, marketplace listing, or public user submissions. |
| Image/file upload | Not applicable | The launch packet states no file upload is included. |
| AI prompt/model-call exposure | Primary | `/api/generate` calls an LLM for public self-serve users. |
| Demo-to-public-product gap | Primary | The launch depends on public signup, self-serve payment, and production traffic assumptions. |

## Five-Gate Summary

| Gate | Status | Notes |
| --- | --- | --- |
| SMS/email interface abuse | Evidence gap | Email verification and password reset exist, but send-rate limit and provider budget cap proof is missing. |
| UGC moderation | Not applicable | No public user content surface is described. |
| Image/file upload | Not applicable | No image or file upload path is described. |
| AI prompt/model-call exposure | Issue | The public model route lacks visible quota, rate limit, budget cap, alerting, queue control, and circuit breaker proof. |
| Demo-to-public-product gap | Issue | Staging UI proof does not prove public self-serve launch readiness. |

## Evidence Ledger

| Evidence item | Source | Evidence freshness | Related gate | Current allowed scope effect | Public scope effect | Needed proof |
| --- | --- | --- | --- | --- | --- | --- |
| `/api/generate` calls an LLM for public users | Launch packet | Verified in this review | AI prompt/model-call exposure | Does not block limited private testing with known users if monitored manually. | Blocks public self-serve launch because quota, rate limit, budget cap, queue control, alerting, and circuit breaker proof is missing. | Route boundary, quota, rate-limit, provider spend cap, monitoring, alert, queue, and circuit-breaker evidence. |
| Email verification and password reset exist | Launch packet | Verified in this review | SMS/email interface abuse | Does not block limited private testing with known users. | Blocks public self-serve launch until send-rate and provider budget evidence exists. | Send-rate limit, abuse monitoring, and provider budget cap proof. |
| No public UGC or file upload is included | Launch packet | Verified in this review | UGC moderation / Image/file upload | Does not block current limited testing. | Does not block public launch for these gates unless those surfaces are added. | Re-review if public posts, shared drafts, profiles, comments, media upload, or file upload are added. |

## Findings

### 1. Public Model Route Lacks Public-Scale Cost Controls

- Category: AI prompt/model-call exposure
- Severity: `BLOCKER`
- Evidence label: `evidence_gap`
- Evidence freshness: `Not verified`
- Evidence: The packet says `/api/generate` calls an LLM for public self-serve users, but no quota, rate limit, budget cap, queue, alert, or circuit breaker evidence is included.
- Risk: Unknown users can create model spend, overload the queue, or exhaust provider budget before an operator notices.
- Blocks current allowed scope? No. Limited private testing with known users can continue if the operator monitors use manually.
- Blocks public self-serve launch or large-scale release? Yes. Public AI traffic needs visible rate limit, budget cap, alerting, queue control, and circuit breaker evidence before launch.
- Recommendation: Do not publicly launch until public-scale model-call protection and proof are provided.

### 2. Email Send Paths Lack Abuse And Budget Evidence

- Category: SMS/email interface abuse
- Severity: `HIGH`
- Evidence label: `evidence_gap`
- Evidence freshness: `Not verified`
- Evidence: Email verification and password reset exist, but the packet does not include send-rate limits, provider budget caps, or anomaly alert evidence.
- Risk: Public signup can turn email sends into a spam, cost, or deliverability problem.
- Blocks current allowed scope? No. Known-user testing can stay limited and manually watched.
- Blocks public self-serve launch or large-scale release? Yes. Public self-serve launch needs send abuse limits and cost evidence.
- Recommendation: Provide email send-rate, provider budget, and abuse monitoring proof before public release.

### 3. Staging UI Proof Does Not Prove Public SaaS Readiness

- Category: Demo-to-public-product gap
- Severity: `BLOCKER`
- Evidence label: `confirmed`
- Evidence freshness: `Verified in this review`
- Evidence: The packet only says the UI works in staging while the launch plan is public signup, free trial, paid upgrade, and paid model calls.
- Risk: A working demo can fail under unknown users, public traffic, abuse attempts, and unattended cost growth.
- Blocks current allowed scope? No. The product can remain in limited private testing while evidence is collected.
- Blocks public self-serve launch or large-scale release? Yes. The public launch scope is blocked until production guardrail evidence exists.
- Recommendation: Keep the product out of public self-serve release until the missing launch evidence is supplied and reviewed.

## Evidence Gaps

- Verified in this review: public self-serve launch plan, `/api/generate` model route, email verification and password reset, no public UGC, and no file upload.
- Previously verified, not rerun: none provided.
- Not verified: model quota, rate limit, budget cap, queue control, alerting, circuit breaker, email send limits, provider budget cap, and production traffic readiness.

## Audit Recommendations

- Blocks public self-serve launch now.
- Keep only a limited private test or operator-watched pilot until public-scale evidence exists.
- Re-review after model-call protection, email-send protection, budget cap, alerting, and circuit breaker proof is available.

## Out Of Scope

This review is limited to the five Vibe Launch Review gates and does not implement fixes, generate patches, perform penetration testing, or validate production infrastructure.
