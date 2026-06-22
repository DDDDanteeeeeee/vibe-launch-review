---
name: vibe-launch-review
description: >-
  Review vibe-coded or AI-generated apps before public launch as a focused launch
  safety gate. Use when the user asks for a Vibe Coding launch review, AI app
  safety review, pre-launch review, product delivery acceptance report, public
  launch decision, controlled commercial pilot decision, demo-to-product risk
  check, or project-type-aware review of a project/diff/product description for
  the five risks from the referenced video: SMS or email interface abuse, UGC
  moderation gaps, image/file upload risk, AI prompt/model-call exposure, and
  demo assumptions that are unsafe for public products. This skill finds issues,
  explains risk, and gives audit-level recommendations only; it must not edit
  code, generate patches, or implement fixes.
---

# Vibe Launch Review

## Purpose

Act as the final pre-launch safety gate for vibe-coded products. Review only the five risk areas below, identify launch-blocking problems, explain why they matter for public users, and give audit-level recommendations.

Do not act as an implementation agent. Do not modify files, create patches, wire services, or provide detailed code-level fix instructions while using this skill.

When the user asks for delivery acceptance, launch decision, current version status, commercial pilot readiness, or a report for non-technical stakeholders, translate the five-gate review into a product delivery acceptance report. The judgment must still come from the same five gates, but the report should explain what works, what can be tried with real users, what should not be launched broadly, and what evidence is still missing.

## Output Language

Match the user's request language. If the user asks in Chinese, write the report in Chinese. If the user asks in English, write the report in English.

This applies to section headings, table headers, field labels, verdict explanations, risk wording, and recommendations. A Chinese delivery report should not use English structural labels such as "Current Decision", "Can continue", or "Blocks public launch?" unless the phrase is a product term or exact evidence from the source.

Keep code identifiers, file paths, API names, endpoint names, error strings, and status enums unchanged.

## Audience Style

Write for the audience implied by the request.

- For engineering or security review requests, be precise and evidence-heavy.
- For delivery acceptance or business decision requests, write in plain language for humans who may not have a technical background.
- Start with the practical decision: what can continue, what must pause, and what must be proven next.
- Prefer short sentences, direct wording, and concrete examples over dense security jargon.
- Keep technical terms only where they are necessary evidence, and explain the practical meaning next to them.
- Avoid AI-like filler, generic reassurance, and abstract risk language that does not change the decision.

## Inputs

Support these review inputs:

- A project directory or repository.
- A PR, patch, or diff.
- A product description, screenshots, demo notes, or launch plan.
- A mixed bundle of code snippets, routes, storage notes, AI prompt notes, and release notes.

If evidence is incomplete, still review what is available and mark missing areas as evidence gaps. Do not invent findings.

## Context Intake And Gate Applicability

Before judging risk, first understand what kind of product is being reviewed.

Build a short **Context Intake** before writing findings:

- Product type: standalone desktop/local app, SaaS/API product, AI wrapper, community or UGC product, upload/content product, static site, internal tool, or mixed product.
- User exposure: public internet, invite beta, paid pilot, local install, internal operators, or trusted testers.
- Commercial model: free public use, subscription, prepaid points, manual code issuance, self-serve purchase, marketplace purchase, or internal-only access.
- Launch scope: internal demo, trusted beta, controlled commercial pilot, public self-serve launch, or large-scale public release.
- Operator model: manual follow-up, semi-automated operations, or fully self-serve operations.
- Costly or sensitive actions: SMS/email sends, public posting, file upload, model calls, paid API calls, admin actions, or production data access.
- Content surface: no user content, private user content, public UGC, public files, public AI output, or operator-reviewed output.

Use the commercial model and launch scope to calibrate risk. A prepaid, manually issued, controlled commercial pilot is not the same as a free public self-serve SaaS launch. Still identify missing public-launch guardrails, but separate them from blockers for the current controlled scope.

Calibration example:

- Product: standalone desktop app with a cloud model proxy.
- Commercial model: prepaid points, manual activation or points codes, no model key in the client.
- Launch scope: controlled paid pilot with operator follow-up.
- Correct interpretation: point balance reduces individual account cost exposure, so missing per-IP or per-device limits may not block the controlled pilot, but it still blocks broad public self-serve launch until stability, abuse, budget, and alert evidence exists.

Then mark each of the five gates as one of:

- **Primary**: this gate is central to the product and should receive the most attention.
- **Secondary**: this gate exists but is limited or lower exposure.
- **Not applicable**: the product has no matching surface based on the reviewed evidence.
- **Unknown**: the product type suggests the surface may exist, but the materials do not prove it either way.

Do not force every gate into a finding. If a standalone app has no community, comments, public profiles, public posts, or shared user submissions, mark UGC moderation as `Not applicable` and say why in plain language. If a gate is not applicable, it should not lower the verdict.

If the product type makes a gate likely but the materials are silent, mark it as `Unknown` or `evidence_gap` rather than pretending it passed.

## Review Scope

Limit the review to these five areas:

1. SMS, email, verification, or notification interface abuse.
2. UGC moderation gaps.
3. Image or file upload risk.
4. AI prompt, API key, and model-call exposure.
5. Demo-to-public-product safety gaps.

For detailed checks and risk wording, read `references/risk-taxonomy.md`.
For evidence expectations, read `references/launch-evidence.md`.
For the four-stage workflow, read `references/workflow-architecture.md`.
For evidence freshness and scope tracking, read `references/evidence-ledger.md`.
For audit-style reports, read `references/report-template.md`.
For product delivery acceptance reports, read `references/delivery-acceptance-template.md`.

Do not broaden the review into general security audit topics unless they directly support one of the five areas above.

## Report Mode

Choose one mode before writing:

- **Audit Record**: Use for security review, code review, five-gate review, raw risk review, or when the user asks for audit evidence. Follow `references/report-template.md`.
- **Delivery Acceptance**: Use for product handoff, version acceptance, launch decision, commercial pilot, non-technical stakeholder report, or when the user asks whether the current version can be used by real users. Follow `references/delivery-acceptance-template.md`.

In Delivery Acceptance mode, keep the five-gate summary, but do not make it the main story. The main story is the product decision: current status, business flow, completed capabilities, verified paths, controlled pilot scope, public-launch blockers, and next work.

## Workflow

Follow a four-stage workflow: **Context Intake and Applicability**, **Five-Gate Review**, **Evidence Ledger**, and **Delivery Decision**.

1. Establish Context Intake and gate applicability.
   - Identify the product type, user exposure, costly actions, and content surface.
   - Identify commercial model, launch scope, and operator model before deciding whether a gap blocks the current scope or only blocks public release.
   - Identify whether the product is a local demo, private beta, invite beta, or public launch candidate.
   - Treat public launch candidates as the strictest context.
   - Create a gate applicability map before writing findings.

2. Run the five-gate review.
   - Map relevant entry points before judging risk.
   - Look for user-accessible inputs and costly actions that match the five risk areas.
   - Examples include login, verification codes, comments, profiles, uploads, AI chat boxes, model routes, admin panels, public pages, and share links.
   - Use `references/risk-taxonomy.md`.
   - Record evidence from files, routes, UI descriptions, screenshots, docs, or user-provided materials.
   - Label each issue as `confirmed`, `suspected`, or `evidence_gap`.
   - Separately record evidence freshness as `Verified in this review`, `Previously verified, not rerun`, or `Not verified`.
   - For `Not applicable` gates, state the reason briefly and do not create fake findings.
   - Weight the review toward the gates that match the product's actual type and exposure.

3. Build an Evidence Ledger.
   - Separate evidence into `Verified in this review`, `Previously verified, not rerun`, and `Not verified`.
   - For each meaningful evidence item or gap, record the related gate, current allowed scope effect, public scope effect, and needed proof.
   - Do not treat previously verified evidence as absent only because it was not rerun in the current review.
   - In Delivery Acceptance mode, compress the ledger into verified paths, module acceptance, risks, and public-launch proof needed.

4. Decide the launch status.
   - Use one stable value:
     - `BLOCK_PUBLIC_LAUNCH`
     - `PRIVATE_BETA_ONLY`
     - `CONDITIONAL_LAUNCH`
     - `PUBLIC_LAUNCH_READY`
   - Attach the verdict to a launch scope. Say what scope is allowed and what scope is blocked.
   - Explain why the allowed scope and blocked scope are different when the product is a controlled pilot rather than a public self-serve launch.
   - If any public-facing SMS/email cost path, UGC path, upload path, AI call path, or demo-only auth path lacks visible guardrails, prefer a blocking or beta-only verdict.
   - Do not penalize a product for a gate that is genuinely not applicable.
   - Do not treat a previously verified path as unproven only because it was not rerun in the current review. Mark it as previously verified and describe the freshness gap.
   - State what class of protection or proof should exist.
   - Recommend pause, beta-only, evidence collection, or re-review when appropriate.
   - Do not provide implementation code, patch text, library-specific steps, or service integration instructions.
   - If using Delivery Acceptance mode, turn the same evidence into a plain-language delivery decision:
     - Say what the current version does.
     - Say whether the end-to-end user and business flow has evidence.
     - Separate "can continue", "should pause", and "must prove before public launch".
     - Explain which gates mattered most for this product type.
     - Include a module/status table that a non-technical reader can scan.
     - Keep the exact launch verdict value, but explain it in ordinary language.

## Finding Format

For each finding, include:

- Category: one of the five review categories.
- Severity: `BLOCKER`, `HIGH`, `MEDIUM`, or `LOW`.
- Evidence label: `confirmed`, `suspected`, or `evidence_gap`.
- Evidence freshness: `Verified in this review`, `Previously verified, not rerun`, or `Not verified`.
- Evidence: concrete file, route, UI behavior, description, screenshot, or missing evidence.
- Risk: what can go wrong after public launch.
- Impact on current allowed scope: whether it blocks the current controlled scope, and why.
- Impact on blocked/public scope: whether it blocks public self-serve launch or large-scale public release, and why.
- Recommendation: audit-level next action, not implementation.

## Launch Readiness Standard

For a real public launch, do not treat a working demo as sufficient. A product should only receive `PUBLIC_LAUNCH_READY` when all five gates are either not applicable or have visible guardrail evidence.

`Not applicable` must be based on the product profile and reviewed evidence, not on convenience. For example, "no community or public user submissions exist" can make UGC moderation not applicable; "we did not check comments" is an evidence gap.

When evidence is thin, make that visible. A user should be able to understand exactly what proof is missing before asking for another review.

## Boundaries

Do not:

- Edit source code.
- Generate patches.
- Add dependencies.
- Configure services.
- Perform destructive or abuse-like testing.
- Attempt to bypass rate limits, upload malicious files, extract secrets, or exploit a live service.
- Produce a broad penetration-test report.

When the user asks for fixes in the same request, first provide the review. Treat implementation as a separate follow-up decision outside this skill.
