# Launch Evidence Guide

Use this guide to decide what evidence is enough for a real launch review.

Build an Evidence Ledger before the verdict when evidence freshness or launch scope could be misread. The ledger should connect each evidence item to its source, freshness, related gate, current allowed scope effect, public scope effect, and needed proof.

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

Do not say not
