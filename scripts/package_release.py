from __future__ import annotations

import argparse
import hashlib
import zipfile
from pathlib import Path


PACKAGE_NAME = "vibe-launch-review"
RUNTIME_DIRS = {"agents", "references"}
RUNTIME_FILES = {"SKILL.md"}
SOURCE_EXCLUDED_DIRS = {".git", "__pycache__"}
ARTIFACT_NAMES = {
    f"{PACKAGE_NAME}.skill",
    f"{PACKAGE_NAME}-github-source.zip",
    f"{PACKAGE_NAME}-SHA256SUMS.txt",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def iter_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel_parts = path.relative_to(root).parts
        if any(part in SOURCE_EXCLUDED_DIRS for part in rel_parts):
            continue
        if path.name in ARTIFACT_NAMES:
            continue
        files.append(path)
    return sorted(files, key=lambda item: item.relative_to(root).as_posix())


def runtime_files(root: Path) -> list[Path]:
    selected: list[Path] = []
    for path in iter_files(root):
        rel = path.relative_to(root)
        if rel.as_posix() in RUNTIME_FILES or rel.parts[0] in RUNTIME_DIRS:
            selected.append(path)
    return selected


def write_zip(root: Path, output: Path, files: list[Path]) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            rel = path.relative_to(root).as_posix()
            info = zipfile.ZipInfo(f"{PACKAGE_NAME}/{rel}")
            info.date_time = (1980, 1, 1, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes())


def main() -> int:
    parser = argparse.ArgumentParser(description="Build local release artifacts for vibe-launch-review.")
    parser.add_argument("root", nargs="?", default=".", help="Path to the package root.")
    parser.add_argument("--dist", default=None, help="Output directory. Defaults to ../dist from the package root.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not (root / "SKILL.md").is_file():
        print(f"NOT_READY missing SKILL.md under {root}")
        return 1

    dist = Path(args.dist).resolve() if args.dist else root.parent / "dist"
    skill_artifact = dist / f"{PACKAGE_NAME}.skill"
    source_artifact = dist / f"{PACKAGE_NAME}-github-source.zip"
    sums_artifact = dist / f"{PACKAGE_NAME}-SHA256SUMS.txt"

    runtime = runtime_files(root)
    source = iter_files(root)
    if not runtime:
        print("NOT_READY no runtime files selected")
        return 1

    write_zip(root, skill_artifact, runtime)
    write_zip(root, source_artifact, source)

    lines = [
        f"{sha256(skill_artifact)}  {skill_artifact.name}",
        f"{sha256(source_artifact)}  {source_artifact.name}",
    ]
    sums_artifact.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("READY_FOR_LOCAL_PACKAGE")
    print(f"skill_artifact={skill_artifact}")
    print(f"source_artifact={source_artifact}")
    print(f"sha256sums={sums_artifact}")
    for line in lines:
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
