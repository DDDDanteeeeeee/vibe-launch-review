# Product Delivery Acceptance Template

Use this template when the user asks for product delivery acceptance, current version acceptance, launch decision, controlled pilot readiness, commercial trial readiness, or a report for non-technical stakeholders.

The review scope is still limited to the five Vibe Launch Review gates. This template changes the communication shape, not the risk scope.

## Style Rules

- Write in plain language. Assume some readers are product, sales, operations, or founders rather than engineers.
- Start with the decision before details.
- Use short paragraphs and concrete labels such as "Can continue", "Pause for now", and "Must prove before public launch".
- Match the user's language for section headings, table headers, and field labels, not only the paragraph text. For Chinese output, use labels such as `当前结论`, `可以继续`, `暂缓事项`, `允许范围`, `暂缓范围`, `证据标签`, `证据新鲜度`, `是否阻塞受控试点`, and `是否阻塞公开发布`.
- Explain technical evidence by its product meaning.
- First explain what type of product is being reviewed, then focus the report on the gates that actually apply to that product.
- Mark gates as "Not applicable" when the product truly has no matching surface. Give a short reason instead of inventing a risk.
- Do not hide evidence gaps, but do not bury the reader in raw audit wording.
- Use the Evidence Ledger as a behind-the-scenes proof check. In the final report, usually compress it into verified paths, module acceptance, current risks, and must-have proof before public launch.
- Do not include implementation code, patches, package recommendations, or step-by-step service configuration.
- Calibrate the report by business model and launch scope before judging blockers. A controlled paid pilot with manual code issuance should not be judged as if it were a large-scale public self-serve SaaS launch.
- Separate "blocks current controlled scope" from "blocks public launch". Missing public-scale guardrails can block public launch without blocking a small manually operated pilot.

```md
# Product Delivery Acceptance Report

## 1. Current Decision

- Current status:
- Can continue:
- Do not do yet:
- Allowed scope:
- Blocked scope:
- Why:
- Main reason:

Use one stable launch verdict:
`BLOCK_PUBLIC_LAUNCH` / `PRIVATE_BETA_ONLY` / `CONDITIONAL_LAUNCH` / `PUBLIC_LAUNCH_READY`

Explain the verdict in one plain paragraph.

## 2. Context Intake: Product Type And Review Focus

- Product type:
- User exposure:
- Commercial model:
- Launch scope:
- Operator model:
- Main sensitive or costly actions:
- Gates that matter most:
- Gates that are not applicable:

Explain this in plain language. Example: if the product is a standalone desktop app with no comments, posts, profiles, or shared user submissions, say that UGC moderation is not applicable instead of treating it as a risk.

For prepaid or manually operated products, explain what the prepaid balance or operator control already limits, and what it does not limit. Example: prepaid points can limit one account's model spend, but they do not prove public-scale rate limiting, queue protection, alerts, or provider budget caps.

| Gate | Applicability | Plain-language reason |
| --- | --- | --- |
| SMS/email interface abuse | Primary / Secondary / Not applicable / Unknown | |
| UGC moderation | Primary / Secondary / Not applicable / Unknown | |
| Image/file upload | Primary / Secondary / Not applicable / Unknown | |
| AI prompt/model-call exposure | Primary / Secondary / Not applicable / Unknown | |
| Demo-to-public-product gap | Primary / Secondary / Not applicable / Unknown | |

## 3. Current Business Flow

- How the user gets access:
- How the user pays or receives quota:
- What the product does for the user:
- Where the costly or sensitive operation happens:
- What happens when the operation fails:

## 4. Completed Capabilities

- Capability:
- Current status:
- Product meaning:
- Evidence:

## 5. Verified Paths

| Path | Result | Evidence | Meaning |
| --- | --- | --- | --- |
|  | Pass / Partial / Not verified |  |  |

Separate old evidence from this-turn evidence. If something was verified earlier but not rerun in this review, say that clearly.

Use these freshness labels:

- Verified in this review:
- Previously verified, not rerun:
- Not verified:

Evidence Ledger checkpoint:

| Evidence item | Evidence freshness | Current allowed scope effect | Public scope effect | Needed proof |
| --- | --- | --- | --- | --- |
|  | Verified in this review / Previously verified, not rerun / Not verified | Blocks current scope? Yes / No. Why: | Blocks public launch? Yes / No. Why: |  |

For non-technical readers, this table can be shortened or folded into the next module and risk tables.

## 6. Module Acceptance Table

| Module | Current status | Acceptance result | Evidence | Blocks controlled pilot? | Blocks public launch? |
| --- | --- | --- | --- | --- | --- |
|  |  | Pass / Partial / Blocked / Not verified |  | Yes / No | Yes / No |

## 7. Current Risks And Blockers

Use practical wording:

- Risk:
- Why it matters:
- Evidence label:
- Evidence freshness:
- Impact on current allowed scope:
- Impact on blocked/public scope:
- Blocks controlled pilot? Yes / No. Why:
- Blocks public launch? Yes / No. Why:
- What proof is needed:

Keep findings tied to the five gates. Use evidence labels where useful:
`confirmed` / `suspected` / `evidence_gap`

## 8. Controlled Pilot Scope

- Allowed:
- Not allowed:
- Operator responsibility:
- User type:
- Review point:

## 9. Must-Have Before Public Launch

- Required proof:
- Why it matters:
- Gate:

## 10. Next Work

- Task:
- Goal:
- Owner or role:
- Validation:

Do not write code or implementation patches.

## 11. Five-Gate Summary

| Gate | Status | Plain-language meaning |
| --- | --- | --- |
| SMS/email interface abuse | Pass / Issue / Evidence gap / Not applicable | |
| UGC moderation | Pass / Issue / Evidence gap / Not applicable | |
| Image/file upload | Pass / Issue / Evidence gap / Not applicable | |
| AI prompt/model-call exposure | Pass / Issue / Evidence gap / Not applicable | |
| Demo-to-public-product gap | Pass / Issue / Evidence gap / Not applicable | |

## Out Of Scope

This report does not implement fixes, generate patches, replace penetration testing, or validate production infrastructure.
```
