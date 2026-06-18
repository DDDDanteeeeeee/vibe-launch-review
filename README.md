# Vibe Launch Review

**A final launch safety gate for vibe-coded apps.**

Vibe Launch Review helps builders review AI-generated or vibe-coded products before public launch. It checks the five risk areas from the source video logic: SMS/email abuse, UGC moderation, image/file upload risk, AI prompt/model-call exposure, and demo assumptions that break in public.

It is project-type-aware. The review first asks what kind of product this is, then weights the five gates accordingly. A standalone desktop app with no comments, posts, community, profiles, or shared submissions should not be punished for missing UGC moderation. An AI app with paid model calls should instead receive heavier attention on model-call exposure, budget, quota, monitoring, and demo-to-public readiness.

It is also launch-scope-aware. A controlled paid pilot with prepaid points and manual code issuance should not be judged as if it were a free public self-serve SaaS launch. The report should say what scope is allowed, what scope is blocked, and which gaps matter only before public-scale release.

It does not fix code. It finds launch risks, explains why they matter, and tells the builder what evidence or guardrail class is needed before launch.

It can produce two report styles:

- An audit record for engineers who need raw five-gate evidence.
- A product delivery acceptance report for founders, product owners, sales, operations, or other non-technical readers who need a clear launch decision.

## Why This Exists

Vibe-coded products can look complete while still being unsafe for real users. The common failure is not that the app cannot run. The failure is that nobody reviews the public abuse surfaces before launch.

This skill is built for that last checkpoint.

## What It Reviews

| Gate | What It Catches |
| --- | --- |
| SMS/email interface abuse | Paid or spam-capable sends without limits, budget caps, or anomaly monitoring. |
| UGC moderation | Public user content without review, reporting, takedown, or accountability evidence. |
| Image/file upload | Upload paths without size/type/content/access/storage controls. |
| AI prompt/model-call exposure | Prompts, keys, public model routes, quota gaps, and unreviewed model output. |
| Demo-to-public-product gap | Mock auth, debug routes, default accounts, frontend-only permissions, and demo assumptions. |

## What It Produces

- A launch verdict: `BLOCK_PUBLIC_LAUNCH`, `PRIVATE_BETA_ONLY`, `CONDITIONAL_LAUNCH`, or `PUBLIC_LAUNCH_READY`.
- A project profile and gate applicability table.
- A five-gate summary table.
- Findings with evidence label, evidence, risk, severity, and audit-level recommendations.
- Evidence gaps that must be resolved before a stronger launch decision.
- When requested, a plain-language delivery acceptance report covering current status, business flow, verified paths, controlled pilot scope, public-launch blockers, and next work.

## What It Does Not Do

- It does not modify source code.
- It does not generate patches.
- It does not configure services.
- It does not perform penetration testing.
- It does not replace a full security audit.

## Install

Copy this folder into your local Codex skills directory, or install the packaged `vibe-launch-review.skill` artifact if your environment supports `.skill` files.

Expected installable layout:

```text
vibe-launch-review/
  SKILL.md
  agents/openai.yaml
  references/
```

## Usage

Ask in the language you want the report in:

```text
Use $vibe-launch-review to review this app before public launch.
```

For a stakeholder-facing delivery report, ask:

```text
Use $vibe-launch-review to produce a product delivery acceptance report and launch decision for this version.
```

You can provide:

- A project directory or repository.
- A PR, patch, or diff.
- Product notes, screenshots, routes, storage notes, AI prompt notes, or launch notes.

The report language follows your input language. Code identifiers and status enums stay unchanged.

## Demo And Evals

See:

- `examples/function-tests/`
- `examples/public-demo-pack.md`
- `examples/smoke-review-output.md`
- `examples/zh-realistic-vibe-app/`
- `evals/evals.json`

`examples/function-tests/ai-catalog-controlled-pilot-*.md` is the calibration case for a desktop app with a cloud model proxy, prepaid points, manual code issuance, and controlled commercial pilot scope.

## Preflight

Run this before local packaging or publishing:

```bash
python scripts/preflight_check.py .
python scripts/validate_functional_outputs.py examples/function-tests/cases.json
python scripts/validate_smoke_outputs.py examples/smoke-review-output.md
python scripts/validate_smoke_outputs.py examples/zh-realistic-vibe-app/review-output.md --expect-language zh
```

Expected result:

```text
READY_FOR_LOCAL_PACKAGE
FUNCTIONAL_OUTPUTS_OK
SMOKE_OUTPUT_OK
SMOKE_OUTPUT_OK
```

Build local artifacts:

```bash
python scripts/package_release.py . --dist ../dist
```

## License

MIT.
