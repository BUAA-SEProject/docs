"""Package the current course documents using only the Python standard library."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
MATERIALS = ROOT / "研讨课材料包"
OUTPUT = ROOT / "dist"
PREFIX = "01组-自定义名称8"
CATEGORIES = ("作业1-需求调研成果", "作业2-需求建模成果")
SHARED = ("通用材料", "汇报PPT", "课程参考原文")
EXTENSIONS = {".md", ".docx", ".pptx", ".pdf", ".puml", ".png", ".json"}


def source_files() -> list[Path]:
    for category in CATEGORIES + SHARED:
        if not (MATERIALS / category).is_dir():
            raise FileNotFoundError(f"Missing material directory: {category}")
    files = sorted(
        path for path in MATERIALS.rglob("*")
        if path.is_file()
        and not path.is_symlink()
        and path.suffix.lower() in EXTENSIONS
        and not any(
            part.startswith((".", "~$"))
            for part in path.relative_to(MATERIALS).parts
        )
    )
    for category in CATEGORIES + SHARED:
        if not any(path.relative_to(MATERIALS).parts[0] == category for path in files):
            raise ValueError(f"Empty material directory: {category}")
    for path in files:
        if path.suffix.lower() in {".docx", ".pptx"}:
            with ZipFile(path) as document:
                bad = document.testzip()
                if bad:
                    raise ValueError(f"Damaged Office document: {path.name}: {bad}")
    return files


def write_archive(
    filename: str, files: list[Path], *, full: bool = False, label: str = ""
) -> dict:
    target = OUTPUT / filename
    temporary = target.with_suffix(".zip.tmp")
    try:
        with ZipFile(temporary, "w", ZIP_DEFLATED) as archive:
            for path in files:
                relative = path.relative_to(MATERIALS).as_posix()
                archive.write(path, f"研讨课材料包/{relative}" if full else relative)
            if not full:
                archive.writestr(
                    "00-提交说明.md",
                    f"# {PREFIX} {label}\n\n"
                    "本包包含对应作业、通用材料、综合汇报与课程原文。"
                    "Markdown 为可阅读源稿，Word 与 PPT 为交付文件。\n\n"
                    "综合 PPT 还引用另一作业；查阅全部来源时，请使用完整材料包。"
                    "打包不代表文档已同步或已通过课程验收。\n",
                )
        with ZipFile(temporary) as archive:
            bad = archive.testzip()
            if bad:
                raise ValueError(f"Damaged archive: {filename}: {bad}")
            for path in files:
                relative = path.relative_to(MATERIALS).as_posix()
                member = f"研讨课材料包/{relative}" if full else relative
                if archive.read(member) != path.read_bytes():
                    raise ValueError(f"Archive content mismatch: {member}")
            count = len(archive.namelist())
        temporary.replace(target)
    finally:
        temporary.unlink(missing_ok=True)
    return {
        "file": filename,
        "files": count,
        "bytes": target.stat().st_size,
        "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
    }


def main() -> None:
    files = source_files()
    OUTPUT.mkdir(exist_ok=True)
    checksums = []
    for category, label in zip(CATEGORIES, ("需求调研成果", "需求建模成果")):
        selected = [
            path for path in files
            if path.relative_to(MATERIALS).parts[0] in (category,) + SHARED
        ]
        checksums.append(write_archive(f"{PREFIX}-{label}.zip", selected, label=label))
    checksums.append(write_archive(f"{PREFIX}-研讨课完整材料.zip", files, full=True))
    (OUTPUT / "checksums.json").write_text(
        json.dumps(checksums, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    for item in checksums:
        print(f"dist/{item['file']} ({item['files']} files, {item['bytes']} bytes)")


if __name__ == "__main__":
    main()
