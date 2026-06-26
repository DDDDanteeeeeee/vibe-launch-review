# Vibe Launch Review Workflow Architecture

Use this reference to run the review as a deliverable workflow, not as a loose list of security concerns.

The workflow has four stages:

1. Context Intake and Applicability
2. Five-Gate Review
3. Evidence Ledger
4. Delivery Decision

This is still one skill with one review boundary. Do not turn it into a broad security audit, do not call unrelated security skills by default, and do not implement fixes.

## Stage 1: Context Intake And Applicability

Goal: understand the product before judging it.

Collect:

- Product type
- User exposure
- Commercial model
- Launch scope
- Operator model
- Costly or sensitive actions
- Content surface
- Data/privacy surface when relevant

Then produce a gate applicability map:

- `Primary`: central to this product's user flow, cost surface, or content exposure.
- `Secondary`: present, but limited or lower exposure.
- `Not applicable`: no matching surface exists in the reviewed evidence.
- `Unknown`: the product type suggests the surface may exist, but the evidence does not prove it.

Stop condition: do not write findings until the product type, launch scope, and applicable gates are clear enough to avoid fake risks.

User-experience rule: collect only the minimum information needed. If a user does not know an answer, mark it as unknown and let the review identify the evidence gap.

## Stage 2: Five-Gate Review

Goal: inspect only the five Vibe Launch Review gates.

Review:

1. SMS/email interface abuse
2. UGC moderation
3. Image/file upload risk
4. AI prompt/model-call exposure
5. Demo-to-public-product gap

For each relevant gate, record:

- Evidence label: `confirmed`, `suspected`, or `evidence_gap`
- Evidence freshness: `Verified in this review`, `Previously verified, not rerun`, or `Not verified`
- Current allowed scope impact
- Public self-serve or large-scale release impact
- Audit-level recommendation

When a gate involves user data, uploaded files, model context, stored output, or logs, include the data and privacy handling view in the same finding: what data exists, where it goes, whether sensitive content is logged, and what proof is missing. Do not create a separate privacy-compliance gate.

Stop condition: if a gate is not applicable, state why and move on. Do not create a finding just to fill all five categories.

## Stage 3: Evidence Ledger

Goal: make the proof chain explicit before deciding launch status.

Build a compact Evidence Ledger that separates:

- What was verified in this review
- What was previously verified but not rerun
- What was not verified
- Which allowed or blocked scope each evidence item affects

The Evidence Ledger is an intermediate control, not a requirement to overwhelm every final report. In delivery acceptance reports, compress it into human-readable Verified
