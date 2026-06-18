# Public Demo Pack

This demo uses a fictional app and contains no private code or customer data.

## User Prompt

```text
Use $vibe-launch-review to review this vibe-coded app before public launch.

Product: FlashParty
Launch plan: public launch tomorrow.

Relevant notes:
- Login uses `/api/send-code` to send SMS codes. The route is public. The code sample shows no rate limit, daily cap, or provider budget alert.
- Users can post public event comments. Comments appear immediately on the public event page. There is no moderation queue or report button in the current notes.
- Users can upload event cover images. The notes mention upload to a public bucket but do not show file size, MIME checks, content review, or access separation.
- The AI event description generator is called from `/api/generate-description`. The system prompt is in frontend code and the route has no quota notes.
- Admin mode uses `?admin=true` in the frontend during the demo. There is no server-side admin check in the notes.
```

## Expected Output Shape

```md
# Vibe Launch Review

## Verdict

`BLOCK_PUBLIC_LAUNCH`

This should not launch publicly tomorrow. The reviewed notes show blocker-level risks across all five launch gates: public SMS cost exposure, unmoderated public UGC, public upload risk, exposed AI prompt/model-call risk, and demo-only admin assumptions.

## Five-Gate Summary

| Gate | Status | Notes |
| --- | --- | --- |
| SMS/email interface abuse | Issue | Public `/api/send-code` has no visible abuse limits or budget guardrail. |
| UGC moderation | Issue | Public comments appear immediately with no moderation or reporting evidence. |
| Image/file upload | Issue | Public bucket upload lacks validation and access evidence. |
| AI prompt/model-call exposure | Issue | Frontend system prompt and quota gap create exposure and spend risk. |
| Demo-to-public-product gap | Issue | `?admin=true` is a demo-only admin assumption. |

## Findings

### 1. Public SMS Code Route Has No Abuse Evidence

- Category: SMS/email interface abuse
- Severity: `BLOCKER`
- Evidence label: `confirmed`
- Evidence freshness: `Verified in this review`
- Evidence: `/api/send-code` is public and no rate limit, daily cap, provider budget, or anomaly alert is provided.
- Risk: Attackers can script SMS sends and turn a demo login flow into a direct cost sink.
- Recommendation: Do not publicly launch until send limits, budget caps, and abuse monitoring evidence are provided.
```

The full answer should continue with the remaining four findings, evidence gaps, and audit recommendations. It should not include code patches or implementation steps.

## Pass Criteria

A good review:

- Uses only the five review gates.
- Gives `BLOCK_PUBLIC_LAUNCH`.
- Includes evidence, risk, and audit-level recommendation for each issue.
- Does not implement fixes.
- Does not suggest specific package installs or code snippets.
