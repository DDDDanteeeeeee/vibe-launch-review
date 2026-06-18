# Vibe Launch Review

## Verdict

`BLOCK_PUBLIC_LAUNCH`

FlashParty should not launch publicly tomorrow. The supplied notes show blocker-level exposure across all five Vibe Launch Review gates: public SMS cost exposure, unmoderated public UGC, public image upload risk, exposed AI prompt/model-call risk, and demo-only admin behavior.

This review does not implement fixes. It identifies launch risk and names the guardrail evidence needed before another review.

## Five-Gate Summary

| Gate | Status | Evidence |
| --- | --- | --- |
| SMS/email interface abuse | Issue | Public `/api/send-code` has no visible rate limit, daily cap, provider budget, or anomaly alert. |
| UGC moderation | Issue | Public comments appear immediately and no moderation queue, report flow, or takedown process is shown. |
| Image/file upload | Issue | Event cover uploads go to a public bucket without visible size, type, content, storage, or access controls. |
| AI prompt/model-call exposure | Issue | `/api/generate-description` uses a frontend system prompt and no quota evidence is provided. |
| Demo-to-public-product gap | Issue | Admin mode depends on `?admin=true` in the frontend notes. |

## Findings

### 1. Public SMS Code Route Has No Abuse Evidence

- Category: SMS/email interface abuse
- Severity: `BLOCKER`
- Evidence label: `confirmed`
- Evidence freshness: `Verified in this review`
- Evidence: `/api/send-code` is public, and the review notes do not show rate limits, daily caps, provider budget alerts, or anomaly monitoring.
- Risk: Attackers can script sends and turn the login flow into a direct cost sink or spam channel after launch.
- Recommendation: Block public launch until abuse limits, spending guardrails, and operational monitoring evidence are available for review.

### 2. Public Comments Have No Moderation Evidence

- Category: UGC moderation
- Severity: `BLOCKER`
- Evidence label: `confirmed`
- Evidence freshness: `Verified in this review`
- Evidence: Event comments appear immediately on public event pages. No moderation queue, report button, takedown process, or accountability trail is provided.
- Risk: Public users can post abusive, illegal, scam, or brand-damaging content before the team has a reliable review path.
- Recommendation: Keep the product private or beta-only until public UGC review, reporting, removal, and escalation evidence can be reviewed.

### 3. Event Cover Uploads Lack File Safety Evidence

- Category: Image/file upload
- Severity: `HIGH`
- Evidence label: `confirmed`
- Evidence freshness: `Verified in this review`
- Evidence: Users can upload event cover images to a public bucket. The notes do not show file size limits, MIME validation, content checks, storage separation, or access rules.
- Risk: A public upload surface can host unsafe or unwanted files, create storage cost exposure, and leak files through public object access.
- Recommendation: Do not open this upload path publicly until validation, storage, content review, and access-control evidence are documented.

### 4. AI Generation Path Exposes Prompt And Quota Risk

- Category: AI prompt/model-call exposure
- Severity: `HIGH`
- Evidence label: `confirmed`
- Evidence freshness: `Verified in this review`
- Evidence: The AI event description generator is called from `/api/generate-description`; the system prompt is in frontend code, and no quota or abuse-control notes are provided.
- Risk: Users can inspect prompt behavior, trigger unwanted generations, and drive model spend or unsafe output without visible launch controls.
- Recommendation: Treat this as not launch-ready until prompt placement, model access, quota limits, output review expectations, and spend controls are documented.

### 5. Admin Mode Is A Demo Assumption

- Category: Demo-to-public-product gap
- Severity: `BLOCKER`
- Evidence label: `confirmed`
- Evidence freshness: `Verified in this review`
- Evidence: Admin mode uses `?admin=true` in the frontend during the demo. No server-side admin authorization evidence is supplied.
- Risk: A demo-only admin switch can become a public privilege bypass if shipped as-is.
- Recommendation: Block public launch until the team provides server-side authorization evidence and removes demo-only access assumptions from the public path.

## Evidence Gaps

- No operational evidence for SMS/email rate limits, budget caps, or provider-side alerting.
- No UGC moderation policy, queue, reporting, takedown, or audit trail evidence.
- No upload validation, content review, storage isolation, or object access evidence.
- No AI quota, prompt placement, model route control, or output review evidence.
- No public-launch authorization evidence for admin behavior.

## Audit Recommendations

- Change the launch decision to `BLOCK_PUBLIC_LAUNCH`.
- Use private beta only if access is constrained and costly/public surfaces are disabled or manually monitored.
- Re-run Vibe Launch Review when each of the five gates has visible guardrail evidence.
- Keep this review limited to the five video-derived gates; a separate security review can cover broader attack classes later.
