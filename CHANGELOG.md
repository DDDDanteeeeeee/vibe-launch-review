# Changelog

## 0.2.1

- Added a data and privacy handling view inside the existing five-gate review flow, without turning the skill into a legal-compliance audit.
- Updated delivery acceptance outputs to include a short, reader-friendly data/privacy feedback block when user files, AI inputs, AI outputs, or logs matter.
- Tightened functional validation so selected cases must prove data/privacy feedback coverage before packaging.

## 0.2.0

- Added a four-stage review workflow: Context Intake and Applicability, Five-Gate Review, Evidence Ledger, and Delivery Decision.
- Added `references/workflow-architecture.md` and `references/evidence-ledger.md`.
- Updated report templates to include scoped verdicts, evidence freshness, and current-scope versus public-scope impact.
- Added a public self-serve AI SaaS functional case to contrast with the AI Catalog controlled paid pilot calibration case.
- Tightened functional and preflight validation so workflow and Evidence Ledger structure are checked before packaging.

## 0.1.0

- Initial public-ready package.
- Added the five-gate Vibe Launch Review workflow.
- Added risk taxonomy, launch evidence guide, report template, public demo, evals, and preflight checks.
- Added repeatable local packaging and smoke-output validation scripts.
- Added a Chinese realistic local trial fixture and review output to validate language matching.
- Added functional output tests for blocker, evidence-gap, and launch-ready behaviors.
- Added explicit evidence labels to finding format and functional coverage for `CONDITIONAL_LAUNCH`.
- Tightened functional validation so each case must keep both its input fixture and output report.
- Added a Chinese real-user acceptance case that asks for fixes but must remain review-only.

