# Vibe Launch Review Audit Report Template

Match the user's language. Keep identifiers and status enums unchanged. Localize section headings, table headers, and field labels too. For Chinese output, use labels such as `当前结论`, `允许范围`, `暂缓范围`, `证据标签`, `证据新鲜度`, `是否阻塞当前允许范围`, and `是否阻塞公开发布`.

Use this audit template for security review, code review, raw five-gate review, or when the user asks for an evidence-heavy audit record.

If the user asks for product delivery acceptance, current version acceptance, launch decision, controlled commercial pilot readiness, or a report for non-technical stakeholders, use `delivery-acceptance-template.md` instead. Keep the same five-gate risk scope, but present the result as a product decision.

```md
# Vibe Launch Review

## Verdict

`BLOCK_PUBLIC_LAUNCH` / `PRIVATE_BETA_ONLY` / `CONDITIONAL_LAUNCH` / `PUBLIC_LAUNCH_READY`

One short paragraph explaining the launch decision.

- Allowed scope:
- Blocked scope:
- Why:

## Reviewed Material

- Project, diff, URL, screenshot, or product description reviewed:
- Evidence limits:

## Context Intake And Review Focus

- Product type:
- User exposure:
- Commercial model:
- Launch scope:
- Operator model:
- Costly or sensitive actions:
- Content surface:
- Gates that matter most:

Explain in one short paragraph why the review is weighted this way. If a gate is not applicable, say why. Do not turn an absent product feature into a fake risk.

For paid or quota-based products, explain which risks are limited by the business model and which are not. Example: prepaid points may limit one account's model spend, but do not prove public-scale rate limiting, queue protection, provider budget caps, or anomaly alerting.

## Gate Applicability

| Gate | Applicability | Reason |
| --- | --- | --- |
| SMS/email interface abuse | Primary / Secondary / Not applicable / Unknown | |
| UGC moderation | Primary / Secondary / Not applicable / Unknown | |
| Image/file upload | Primary / Secondary / Not applicable / Unknown | |
| AI prompt/model-call exposure | Primary / Secondary / Not applicable / Unknown | |
| Demo-to-public-product gap | Primary / Secondary / Not applicable / Unknown | |

## Five-Gate Summary

| Gate | Status | Notes |
| --- | --- | --- |
| SMS/email interface abuse | Pass / Issue / Evidence gap / Not applicable | |
| UGC moderation | Pass / Issue / Evidence gap / Not applicable | |
| Image/file upload | Pass / Issue / Evidence gap / Not applicable | |
| AI prompt/model-call exposure | Pass / Issue / Evidence gap / Not applicable | |
| Demo-to-public-product gap | Pass / Issue / Evidence gap / Not applicable | |

## Findings

### 1. Finding Title

- Category:
- Severity: `BLOCKER` / `HIGH` / `MEDIUM` / `LOW`
- Evidence label: `confirmed` / `suspected` / `evidence_gap`
- Evidence freshness: `Verified in this review` / `Previously verified, not rerun` / `Not verified`
- Evidence:
- Risk:
- Blocks current allowed scope? Yes / No. Why:
- Blocks public self-serve launch or large-scale release? Yes / No. Why:
- Recommendation:

## Evidence Gaps

- Missing material or proof that prevents a final judgment.
- Separate evidence into:
  - Verified in this review:
  - Previously verified, not rerun:
  - Not verified:

## Audit Recommendations

- Launch decision recommendation.
- Whether the issue blocks the current controlled scope, the public launch scope, or both.
- Evidence to provide before re-review.
- Risk areas that should be checked again after changes.

## Out Of Scope

This review does not implement fixes, generate patches, replace penetration testing, or validate production infrastructure.
```

## Recommendation Style

Use recommendations like:

- "Do not publicly launch until this risk is addressed or disproven."
- "Keep this as private beta until evidence is provided."
- "Provide proof of rate limits, budget caps, or moderation workflow for re-review."
- "Confirm that this route is server-side protected before public launch."

Avoid recommendations like:

- "Install package X and add this code."
- "Replace this file with the following patch."
- "I will implement the fix now."
