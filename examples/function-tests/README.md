# Functional Test Set

These fixtures test the review behavior itself, not installation or publishing.

The suite covers:

- A Chinese public-launch case that must block launch across all five gates.
- An English evidence-gap case that should stay private beta and avoid invented findings.
- An English conditional-launch case where guardrails are claimed but not fully evidenced.
- An English static-site case that should be launch-ready within the five-gate scope.
- A Chinese delivery-acceptance case for non-technical readers that explains controlled pilot scope and public-launch blockers in plain language.
- A Chinese standalone-app case that proves project type controls gate applicability, so missing community features do not become fake UGC risks.
- A Chinese AI Catalog calibration case that distinguishes a prepaid, manually operated, controlled commercial pilot from a public self-serve SaaS launch.
- A Chinese real-user request that asks for fixes but must remain review-only.

Run:

```bash
python scripts/validate_functional_outputs.py examples/function-tests/cases.json
```
