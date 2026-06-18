from __future__ import annotations

import json
import re
import sys
from pathlib import Path


REQUIRED_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
    "README.md",
    "LICENSE",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "GITHUB_RELEASE.md",
    "evals/evals.json",
    "examples/function-tests/README.md",
    "examples/function-tests/cases.json",
    "examples/function-tests/conditional-launch-input.md",
    "examples/function-tests/conditional-launch-output.md",
    "examples/function-tests/evidence-gap-input.md",
    "examples/function-tests/evidence-gap-output.md",
    "examples/function-tests/static-ready-input.md",
    "examples/function-tests/static-ready-output.md",
    "examples/function-tests/delivery-acceptance-input.md",
    "examples/function-tests/delivery-acceptance-output.md",
    "examples/function-tests/standalone-app-applicability-input.md",
    "examples/function-tests/standalone-app-applicability-output.md",
    "examples/function-tests/ai-catalog-controlled-pilot-input.md",
    "examples/function-tests/ai-catalog-controlled-pilot-output.md",
    "examples/function-tests/zh-fix-request-input.md",
    "examples/function-tests/zh-fix-request-output.md",
    "examples/public-demo-pack.md",
    "examples/smoke-review-output.md",
    "examples/zh-realistic-vibe-app/README.md",
    "examples/zh-realistic-vibe-app/launch-notes.md",
    "examples/zh-realistic-vibe-app/review-output.md",
    "examples/zh-realistic-vibe-app/src/api/comments.ts",
    "examples/zh-realistic-vibe-app/src/api/generate-description.ts",
    "examples/zh-realistic-vibe-app/src/api/send-code.ts",
    "examples/zh-realistic-vibe-app/src/api/upload-cover.ts",
    "examples/zh-realistic-vibe-app/src/app/admin-panel.tsx",
    "references/risk-taxonomy.md",
    "references/launch-evidence.md",
    "references/report-template.md",
    "references/delivery-acceptance-template.md",
    "scripts/package_release.py",
    "scripts/preflight_check.py",
    "scripts/validate_functional_outputs.py",
    "scripts/validate_smoke_outputs.py",
]

FORBIDDEN_PATTERNS = [
    r"C:\\Users\\",
    r"agent_memory",
    r"Obsidian Vault",
    r"CoCreationOS\\data",
    r"BEGIN .*PRIVATE",
    r"API[_-]?KEY\s*=",
    r"token\s*=",
    r"cookie\s*=",
    r"password\s*=",
]

SKIP_DIRS = {".git", "__pycache__"}

FIVE_GATES = [
    "SMS/email interface abuse",
    "UGC moderation",
    "Image/file upload",
    "AI prompt/model-call exposure",
    "Demo-to-public-product gap",
]

GATE_PATTERNS = {
    "SMS/email interface abuse": [r"SMS", r"email", r"interface abuse"],
    "UGC moderation": [r"UGC", r"moderation"],
    "Image/file upload": [r"Image", r"file upload"],
    "AI prompt/model-call exposure": [r"AI prompt", r"model-call"],
    "Demo-to-public-product gap": [r"Demo", r"public-product"],
}

REQUIRED_SKILL_PHRASES = [
    "Act as the final pre-launch safety gate",
    "Do not modify files",
    "Do not broaden the review into general security audit topics",
    "BLOCK_PUBLIC_LAUNCH",
    "PRIVATE_BETA_ONLY",
    "CONDITIONAL_LAUNCH",
    "PUBLIC_LAUNCH_READY",
    "Delivery Acceptance",
    "plain language",
    "Context Intake",
    "Product type",
    "gate applicability",
    "Evidence freshness",
]

GATE_ALIASES = [
    ["SMS/email interface abuse", "短信/邮件接口滥用", "短信接口滥用", "邮件接口滥用"],
    ["UGC moderation", "UGC 审核", "用户生成内容审核"],
    ["Image/file upload", "图片/文件上传", "图片上传", "文件上传"],
    ["AI prompt/model-call exposure", "AI 提示词/模型调用暴露", "AI 提示词", "模型调用暴露"],
    ["Demo-to-public-product gap", "Demo 到公开产品差距", "Demo 与公开产品差距"],
]

FIELD_ALIASES = [
    ["Evidence label", "证据标签"],
    ["Evidence freshness", "证据新鲜度"],
    ["Evidence", "证据"],
    ["Risk", "风险"],
    ["Recommendation", "建议"],
]

NO_FIX_ALIASES = [
    "does not implement fixes",
    "不实施修复",
    "不直接修复",
    "不生成 patch",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def check_required_files(root: Path) -> list[str]:
    errors: list[str] = []
    for rel in REQUIRED_FILES:
        if not (root / rel).is_file():
            errors.append(f"missing required file: {rel}")
    return errors


def extract_frontmatter(text: str) -> str | None:
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    return match.group(1) if match else None


def check_skill(root: Path) -> list[str]:
    errors: list[str] = []
    text = read_text(root / "SKILL.md")
    frontmatter = extract_frontmatter(text)
    if frontmatter is None:
        errors.append("SKILL.md must start with YAML frontmatter")
        return errors
    if not re.search(r"^name:\s*vibe-launch-review\s*$", frontmatter, re.MULTILINE):
        errors.append("SKILL.md frontmatter must include name: vibe-launch-review")
    if "description:" not in frontmatter:
        errors.append("SKILL.md frontmatter missing description")
    if len(frontmatter) > 1400:
        errors.append("SKILL.md frontmatter is unexpectedly long")
    for phrase in REQUIRED_SKILL_PHRASES:
        if phrase not in text:
            errors.append(f"SKILL.md missing required phrase: {phrase}")
    for gate, patterns in GATE_PATTERNS.items():
        if not all(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns):
            errors.append(f"SKILL.md missing review gate: {gate}")
    return errors


def check_openai_yaml(root: Path) -> list[str]:
    errors: list[str] = []
    text = read_text(root / "agents" / "openai.yaml")
    for key in ["display_name", "short_description", "default_prompt"]:
        if key not in text:
            errors.append(f"agents/openai.yaml missing {key}")
    if "$vibe-launch-review" not in text:
        errors.append("agents/openai.yaml default_prompt should mention $vibe-launch-review")
    return errors


def check_references(root: Path) -> list[str]:
    errors: list[str] = []
    risk = read_text(root / "references" / "risk-taxonomy.md")
    evidence = read_text(root / "references" / "launch-evidence.md")
    template = read_text(root / "references" / "report-template.md")
    delivery_template = read_text(root / "references" / "delivery-acceptance-template.md")
    for label in ["confirmed", "suspected", "evidence_gap"]:
        if label not in risk:
            errors.append(f"risk taxonomy missing evidence label: {label}")
    for status in ["BLOCKER", "HIGH", "MEDIUM", "LOW"]:
        if status not in risk:
            errors.append(f"risk taxonomy missing severity label: {status}")
    for gate, patterns in GATE_PATTERNS.items():
        if not all(re.search(pattern, evidence, flags=re.IGNORECASE) for pattern in patterns):
            errors.append(f"launch evidence missing gate: {gate}")
    for verdict in ["BLOCK_PUBLIC_LAUNCH", "PRIVATE_BETA_ONLY", "CONDITIONAL_LAUNCH", "PUBLIC_LAUNCH_READY"]:
        if verdict not in template:
            errors.append(f"report template missing verdict: {verdict}")
    if "This review does not implement fixes" not in template:
        errors.append("report template missing no-fix boundary")
    for phrase in [
        "Product Delivery Acceptance Report",
        "Context Intake",
        "Product Type And Review Focus",
        "Current Business Flow",
        "Module Acceptance Table",
        "Controlled Pilot Scope",
        "plain language",
        "证据新鲜度",
        "Not applicable",
        "Previously verified, not rerun",
        "Evidence freshness",
        "Blocks controlled pilot?",
        "Blocks public launch?",
    ]:
        if phrase not in delivery_template:
            errors.append(f"delivery acceptance template missing phrase: {phrase}")
    for phrase in ["Context Intake", "Gate Applicability", "fake risk", "Evidence freshness", "Blocks current allowed scope?", "Blocks public self-serve launch"]:
        if phrase not in template:
            errors.append(f"audit report template missing project applicability phrase: {phrase}")
    if "delivery-acceptance-template.md" not in template:
        errors.append("audit report template should route delivery acceptance requests to delivery-acceptance-template.md")
    for phrase in ["Fixed Calibration Case: AI Catalog", "controlled paid pilot", "public self-serve launch"]:
        if phrase not in risk:
            errors.append(f"risk taxonomy missing scope calibration phrase: {phrase}")
    for phrase in ["Previously verified, not rerun", "AI Catalog calibration", "Not verified"]:
        if phrase not in evidence:
            errors.append(f"launch evidence missing freshness phrase: {phrase}")
    return errors


def check_evals(root: Path) -> list[str]:
    errors: list[str] = []
    data = json.loads(read_text(root / "evals" / "evals.json"))
    evals = data.get("evals", [])
    if data.get("skill_name") != "vibe-launch-review":
        errors.append("evals.json skill_name must be vibe-launch-review")
    if len(evals) < 5:
        errors.append("evals.json should include at least 5 evals")
    all_assertions = " ".join(" ".join(item.get("assertions", [])) for item in evals)
    for required in ["does not include code patches", "report language is Chinese", "evidence_gap"]:
        if required not in all_assertions:
            errors.append(f"eval assertions missing coverage: {required}")
    for item in evals:
        if not item.get("prompt") or not item.get("expected_output"):
            errors.append(f"eval {item.get('id')} missing prompt or expected_output")
        if not item.get("assertions"):
            errors.append(f"eval {item.get('id')} missing assertions")
    return errors


def has_any(text: str, options: list[str]) -> bool:
    return any(option in text for option in options)


def validate_review_output(text: str, label: str, expect_language: str) -> list[str]:
    errors: list[str] = []
    required = [
        "# Vibe Launch Review",
        "BLOCK_PUBLIC_LAUNCH",
    ]
    for phrase in required:
        if phrase not in text:
            errors.append(f"{label} missing phrase: {phrase}")
    for aliases in GATE_ALIASES:
        if not has_any(text, aliases):
            errors.append(f"{label} missing review gate: {aliases[0]}")
    for aliases in FIELD_ALIASES:
        if not has_any(text, aliases):
            errors.append(f"{label} missing finding field: {aliases[0]}")
    if not has_any(text.lower(), [item.lower() for item in NO_FIX_ALIASES]):
        errors.append(f"{label} missing no-fix boundary")
    for forbidden in ["diff --git", "\n@@ ", "apply_patch", "Replace this file"]:
        if forbidden in text:
            errors.append(f"{label} contains patch-like marker: {forbidden.strip()}")
    if len(re.findall(r"^###\s+\d+[\.\、]", text, flags=re.MULTILINE)) < 5:
        errors.append(f"{label} should include at least five numbered findings")
    has_cjk = bool(re.search(r"[\u4e00-\u9fff]", text))
    if expect_language == "zh" and not has_cjk:
        errors.append(f"{label} should be Chinese-language output")
    if expect_language == "en" and has_cjk:
        errors.append(f"{label} should be English-language output")
    return errors


def check_smoke_output(root: Path) -> list[str]:
    errors: list[str] = []
    smoke = read_text(root / "examples" / "smoke-review-output.md")
    zh_trial = read_text(root / "examples" / "zh-realistic-vibe-app" / "review-output.md")
    errors.extend(validate_review_output(smoke, "smoke output", "en"))
    errors.extend(validate_review_output(zh_trial, "zh realistic output", "zh"))
    return errors


def check_functional_cases(root: Path) -> list[str]:
    errors: list[str] = []
    data = json.loads(read_text(root / "examples" / "function-tests" / "cases.json"))
    cases = data.get("cases", [])
    case_ids = {item.get("id") for item in cases}
    expected = {
        "zh-blocks-all-five-public-launch-risks",
        "en-private-beta-for-evidence-gaps",
        "en-public-ready-for-static-no-surface-case",
        "en-conditional-launch-for-claimed-controls-with-proof-gaps",
        "zh-delivery-acceptance-for-nontechnical-reader",
        "zh-standalone-app-project-type-applicability",
        "zh-ai-catalog-controlled-paid-pilot-calibration",
        "zh-fix-request-still-review-only",
    }
    if not expected.issubset(case_ids):
        errors.append("functional cases missing required behavior coverage")
    verdicts = {item.get("expected_verdict") for item in cases}
    required_verdicts = {"BLOCK_PUBLIC_LAUNCH", "PRIVATE_BETA_ONLY", "CONDITIONAL_LAUNCH", "PUBLIC_LAUNCH_READY"}
    if not required_verdicts.issubset(verdicts):
        errors.append("functional cases must cover all four launch verdicts")
    for item in cases:
        input_path = item.get("input")
        output = item.get("output")
        verdict = item.get("expected_verdict")
        language = item.get("expected_language")
        if verdict not in {"BLOCK_PUBLIC_LAUNCH", "PRIVATE_BETA_ONLY", "CONDITIONAL_LAUNCH", "PUBLIC_LAUNCH_READY"}:
            errors.append(f"functional case {item.get('id')} has invalid expected_verdict")
        if language not in {"en", "zh", "any"}:
            errors.append(f"functional case {item.get('id')} has invalid expected_language")
        if not input_path or not (root / input_path).is_file():
            errors.append(f"functional case {item.get('id')} missing input file")
        if not output or not (root / output).is_file():
            errors.append(f"functional case {item.get('id')} missing output file")
    return errors


def check_public_only(root: Path) -> list[str]:
    errors: list[str] = []
    forbidden_dirs = {"runs", "agent_memory", ".tmp", ".codex-tmp"}
    for name in forbidden_dirs:
        if (root / name).exists():
            errors.append(f"public package must not include {name} directory")
    for path in root.rglob("*"):
        rel_parts = path.relative_to(root).parts
        if any(part in SKIP_DIRS for part in rel_parts):
            continue
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if rel.as_posix() == "scripts/preflight_check.py":
            continue
        if path.suffix.lower() in {".skill", ".zip", ".png", ".jpg", ".jpeg", ".gif"}:
            continue
        try:
            text = read_text(path)
        except UnicodeDecodeError:
            continue
        for pattern in FORBIDDEN_PATTERNS:
            if re.search(pattern, text, flags=re.IGNORECASE):
                errors.append(f"forbidden private or secret-like pattern in {rel}: {pattern}")
    return errors


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    errors: list[str] = []
    errors.extend(check_required_files(root))
    if not errors:
        errors.extend(check_skill(root))
        errors.extend(check_openai_yaml(root))
        errors.extend(check_references(root))
        errors.extend(check_evals(root))
        errors.extend(check_smoke_output(root))
        errors.extend(check_functional_cases(root))
        errors.extend(check_public_only(root))

    if errors:
        print("NOT_READY")
        for error in errors:
            print(f"- {error}")
        return 1

    print("READY_FOR_LOCAL_PACKAGE")
    print(f"skill_dir={root}")
    print("checks=required_files,skill,openai_yaml,references,evals,localized_outputs,functional_cases,public_only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
