# Security Policy

Vibe Launch Review is a review skill. It should not directly install packages, configure services, mutate source code, connect accounts, publish content, or exploit live systems.

## Report A Concern

Open a GitHub issue if you find:

- Instructions that encourage destructive or abuse-like testing.
- Prompts that produce patches while claiming to be a launch review.
- Scope drift into broad penetration testing.
- Missing boundaries around SMS/email cost abuse, UGC, uploads, AI prompts/model calls, or demo-only launch assumptions.
- Private data, credentials, cookies, tokens, or customer material in examples or evals.

## Design Boundary

The skill may identify launch blockers and recommend audit-level next actions. It must not implement the fixes.

Examples of allowed recommendations:

- Provide proof of rate limits and budget caps before public launch.
- Keep the product in private beta until UGC moderation evidence exists.
- Re-run the review after upload validation and access evidence are available.

Examples of disallowed behavior:

- Generate a code patch.
- Attempt to bypass a live rate limit.
- Upload test payloads to a production bucket.
- Extract or print secrets.
- Configure a third-party service.

