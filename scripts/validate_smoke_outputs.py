from __future__ import annotations

import argparse
import re
from pathlib import Path


CORE_REQUIRED_PHRASES = [
    "# Vibe Launch Review",
    "BLOCK_PUBLIC_LAUNCH",
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

FORBIDDEN_PATCH_MARKERS = [
    "diff --git",
    "\n@@ ",
    "apply_patch",
    "Replace this file",
]


def contains_any(text: str, options: list[str]) -> bool:
    return any(option in text for option in options)


def validate_text(text: str, expect_language: str = "any") -> list[str]:
    errors: list[str] = []
    for phrase in CORE_REQUIRED_PHRASES:
        if phrase not in text:
            errors.append(f"missing required phrase: {phrase}")
    for aliases in GATE_ALIASES:
        if not contains_any(text, aliases):
            errors.append(f"missing review gate: {aliases[0]}")
    for aliases in FIELD_ALIASES:
        if not contains_any(text, aliases):
            errors.append(f"missing finding field: {aliases[0]}")
    if not contains_any(text.lower(), [item.lower() for item in NO_FIX_ALIASES]):
        errors.append("missing no-fix boundary")
    for marker in FORBIDDEN_PATCH_MARKERS:
        if marker in text:
            errors.append(f"contains patch-like marker: {marker.strip()}")
    if len(re.findall(r"^###\s+\d+[\.\、]", text, flags=re.MULTILINE)) < 5:
        errors.append("expected at least five numbered findings")
    has_cjk = bool(re.search(r"[\u4e00-\u9fff]", text))
    if expect_language == "zh" and not has_cjk:
        errors.append("expected Chinese-language output")
    if expect_language == "en" and has_cjk:
        errors.append("expected English-language output")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Vibe Launch Review example outputs.")
    parser.add_argument("path", help="Path to a review output markdown file.")
    parser.add_argument("--expect-language", choices=["any", "en", "zh"], default="any")
    args = parser.parse_args()

    path = Path(args.path).resolve()
    text = path.read_text(encoding="utf-8")
    errors = validate_text(text, expect_language=args.expect_language)
    if errors:
        print("SMOKE_OUTPUT_NOT_READY")
        for error in errors:
            print(f"- {error}")
        return 1
    print("SMOKE_OUTPUT_OK")
    print(f"file={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
