from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


VERDICTS = {
    "BLOCK_PUBLIC_LAUNCH",
    "PRIVATE_BETA_ONLY",
    "CONDITIONAL_LAUNCH",
    "PUBLIC_LAUNCH_READY",
}

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

PATCH_MARKERS = [
    "diff --git",
    "\n@@ ",
    "apply_patch",
    "Replace this file",
    "I will implement",
    "我来修复",
]

ZH_STRUCTURAL_ENGLISH_PATTERNS = [
    "# Product Delivery Acceptance Report",
    "## 1. Current Decision",
    "- Current status:",
    "- Can continue:",
    "- Do not do yet:",
    "- Allowed scope:",
    "- Blocked scope:",
    "- Main reason:",
    "## 2. Context Intake:",
    "- Product type:",
    "- User exposure:",
    "- Commercial model:",
    "- Launch scope:",
    "- Operator model:",
    "- Main sensitive or costly actions:",
    "- Gates that matter most:",
    "- Gates that are not applicable:",
    "| Gate | Status | Notes |",
    "| Module | Current status | Acceptance result | Evidence | Blocks controlled pilot? | Blocks public launch? |",
    "- Blocks controlled pilot?",
    "- Blocks public launch?",
    "## Reviewed Material",
    "## Five-Gate Summary",
    "## Findings",
    "## Evidence Gaps",
    "## Audit Recommendations",
    "## Out Of Scope",
    "This report does not implement fixes",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def has_any(text: str, options: list[str]) -> bool:
    return any(option in text for option in options)


def finding_count(text: str) -> int:
    return len(re.findall(r"^###\s+\d+[\.\、]", text, flags=re.MULTILINE))


def language_errors(text: str, expect_language: str, label: str) -> list[str]:
    has_cjk = bool(re.search(r"[\u4e00-\u9fff]", text))
    if expect_language == "zh" and not has_cjk:
        return [f"{label}: expected Chinese output"]
    if expect_language == "en" and has_cjk:
        return [f"{label}: expected English output"]
    return []


def localized_label_errors(text: str, case: dict) -> list[str]:
    if case.get("expected_language") != "zh" or not case.get("strict_localized_labels"):
        return []

    case_id = case.get("id", "<missing-id>")
    errors: list[str] = []
    for pattern in ZH_STRUCTURAL_ENGLISH_PATTERNS:
        if pattern in text:
            errors.append(f"{case_id}: Chinese output contains English structural label {pattern!r}")
    return errors


def validate_case(root: Path, case: dict) -> list[str]:
    errors: list[str] = []
    case_id = case.get("id", "<missing-id>")
    input_rel = case.get("input")
    if not input_rel:
        errors.append(f"{case_id}: missing input path")
    elif not (root / input_rel).is_file():
        errors.append(f"{case_id}: missing input file {input_rel}")

    output_rel = case.get("output")
    if not output_rel:
        errors.append(f"{case_id}: missing output path")
        return errors

    output_path = root / output_rel
    if not output_path.is_file():
        errors.append(f"{case_id}: missing output file {output_rel}")
        return errors

    text = read_text(output_path)
    expected_verdict = case.get("expected_verdict")
    if expected_verdict not in VERDICTS:
        errors.append(f"{case_id}: invalid expected_verdict {expected_verdict!r}")
    elif expected_verdict not in text:
        errors.append(f"{case_id}: missing expected verdict {expected_verdict}")

    for verdict in VERDICTS:
        if verdict in text and verdict != expected_verdict and case.get("single_verdict", True):
            errors.append(f"{case_id}: contains extra verdict {verdict}")

    for aliases in GATE_ALIASES:
        if not has_any(text, aliases):
            errors.append(f"{case_id}: missing gate {aliases[0]}")

    min_findings = int(case.get("min_findings", 0))
    if min_findings > 0:
        for aliases in FIELD_ALIASES:
            if not has_any(text, aliases):
                errors.append(f"{case_id}: missing finding field {aliases[0]}")

    if not has_any(text.lower(), [item.lower() for item in NO_FIX_ALIASES]):
        errors.append(f"{case_id}: missing no-fix boundary")

    for marker in PATCH_MARKERS:
        if marker in text:
            errors.append(f"{case_id}: contains patch or implementation marker {marker.strip()}")

    count = finding_count(text)
    if count < min_findings:
        errors.append(f"{case_id}: expected at least {min_findings} findings, found {count}")

    errors.extend(language_errors(text, case.get("expected_language", "any"), case_id))
    errors.extend(localized_label_errors(text, case))

    for phrase in case.get("required_phrases", []):
        if phrase not in text:
            errors.append(f"{case_id}: missing required phrase {phrase!r}")

    for phrase in case.get("forbidden_phrases", []):
        if phrase in text:
            errors.append(f"{case_id}: contains forbidden phrase {phrase!r}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate functional Vibe Launch Review outputs.")
    parser.add_argument("manifest", help="Path to examples/function-tests/cases.json.")
    args = parser.parse_args()

    manifest = Path(args.manifest).resolve()
    root = manifest.parents[2]
    data = json.loads(read_text(manifest))
    cases = data.get("cases", [])
    errors: list[str] = []

    if len(cases) < 4:
        errors.append("manifest should include at least four functional cases")

    expected_verdicts = {case.get("expected_verdict") for case in cases}
    missing_verdicts = VERDICTS - expected_verdicts
    if missing_verdicts:
        errors.append(f"manifest missing verdict coverage: {', '.join(sorted(missing_verdicts))}")

    for case in cases:
        errors.extend(validate_case(root, case))

    if errors:
        print("FUNCTIONAL_OUTPUTS_NOT_READY")
        for error in errors:
            print(f"- {error}")
        return 1

    print("FUNCTIONAL_OUTPUTS_OK")
    print(f"cases={len(cases)}")
    print(f"manifest={manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
