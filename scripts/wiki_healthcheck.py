#!/usr/bin/env python3
"""Fast, dependency-free integrity checks for the ai-lab wiki."""
from __future__ import annotations

import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "wiki"
CONTENT_DIRS = ("entities", "concepts", "comparisons", "queries")
REQUIRED_FRONTMATTER = ("title:", "created:", "updated:", "type:", "tags:", "sources:")
STALE_AFTER_DAYS = 45


def markdown_files(directory: Path) -> list[Path]:
    return sorted(p for p in directory.rglob("*.md") if p.is_file())


def frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        return ""
    end = text.find("\n---", 4)
    return text[:end + 4] if end != -1 else ""


def main() -> int:
    pages = [p for name in CONTENT_DIRS for p in markdown_files(ROOT / name)]
    index = (ROOT / "index.md").read_text(encoding="utf-8")
    names_in_index = set(re.findall(r"\[\[([^\]|]+)", index))
    errors: list[str] = []
    warnings: list[str] = []
    today = date.today()

    for page in pages:
        text = page.read_text(encoding="utf-8")
        fm = frontmatter(text)
        if not fm:
            errors.append(f"no frontmatter: {page.relative_to(ROOT)}")
            continue
        missing = [field for field in REQUIRED_FRONTMATTER if field not in fm]
        if missing:
            errors.append(f"missing {', '.join(missing)}: {page.relative_to(ROOT)}")
        if page.stem not in names_in_index:
            errors.append(f"not indexed: {page.relative_to(ROOT)}")
        updated = re.search(r"^updated:\s*(\d{4}-\d{2}-\d{2})\s*$", fm, re.M)
        if updated:
            try:
                age = (today - date.fromisoformat(updated.group(1))).days
                if age > STALE_AFTER_DAYS:
                    warnings.append(f"stale {age}d: {page.relative_to(ROOT)}")
            except ValueError:
                errors.append(f"invalid updated date: {page.relative_to(ROOT)}")

    raw_files = [p for kind in ("articles", "papers", "transcripts") for p in markdown_files(ROOT / "raw" / kind)]
    print(f"Wiki root: {ROOT}")
    print(f"Content pages: {len(pages)} | Raw markdown sources: {len(raw_files)}")
    print(f"Index links: {len(names_in_index)}")
    print(f"Errors: {len(errors)} | Warnings: {len(warnings)}")
    for item in errors:
        print(f"ERROR  {item}")
    for item in warnings:
        print(f"WARN   {item}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
