#!/usr/bin/env python3
"""Fast, dependency-free integrity checks for the ai-lab wiki."""
from __future__ import annotations

import re
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "wiki"
CONTENT_DIRS = ("entities", "concepts", "comparisons")
REQUIRED_FRONTMATTER = ("title:", "created:", "updated:", "type:", "tags:", "sources:")
STALE_AFTER_DAYS = 45
# 想法层适应度（借自进化式笔记）：只对 concepts/notes 计分，事实层不参与竞争
FITNESS_DIRS = ("concepts", "notes")
FRESHNESS_HALF_LIFE_DAYS = 180
FOCUS_CONFIRM_AFTER_DAYS = 21


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

    # 伴读推送停摆检测：companion-log 最新条目距今 >2 天即报错
    log_file = ROOT / "queries" / "companion-log.md"
    if log_file.exists():
        dates = re.findall(r"^## (\d{4}-\d{2}-\d{2})", log_file.read_text(encoding="utf-8"), re.M)
        if dates:
            silent = (today - date.fromisoformat(max(dates))).days
            if silent > 2:
                errors.append(f"companion-log silent for {silent}d — run `hermes cron status`")
        else:
            warnings.append("companion-log has no entries yet")

    # 薄弱点半衰期：current-focus 里每条薄弱点带「最后确认」日期，超期即提醒
    focus_file = ROOT / "queries" / "current-focus.md"
    if focus_file.exists():
        for match in re.finditer(
            r"^-\s+\*\*([^*]+)\*\*.*?最后确认[：:]\s*(\d{4}-\d{2}-\d{2})",
            focus_file.read_text(encoding="utf-8"), re.M,
        ):
            age = (today - date.fromisoformat(match.group(2))).days
            if age > FOCUS_CONFIRM_AFTER_DAYS:
                warnings.append(f"薄弱点 {age}d 未确认（反馈/链接均无支持，考虑降权或移除）: {match.group(1)}")

    # 适应度榜：连接度 + 新鲜度 + companion-log 提及，供挖掘提炼与季度清理参考
    # ponytail: 反馈热度只按文件名提及计数，不做反馈归因；不够用再升级
    log_text = log_file.read_text(encoding="utf-8") if log_file.exists() else ""
    incoming: Counter[str] = Counter()
    for page in markdown_files(ROOT):
        text = page.read_text(encoding="utf-8")
        for target in re.findall(r"\[\[([^\]|#]+)", text):
            stem = target.strip().split("/")[-1].removesuffix(".md")
            if stem != page.stem:
                incoming[stem] += 1
    scores: list[tuple[float, str]] = []
    for page in (p for name in FITNESS_DIRS for p in markdown_files(ROOT / name)):
        fm = frontmatter(page.read_text(encoding="utf-8"))
        # 日期来源：frontmatter 的 updated/date，缺失时兜底用文件名前缀（伴读笔记无 frontmatter）
        stamp = re.search(r"^(?:updated|date):\s*(\d{4}-\d{2}-\d{2})", fm, re.M) or re.match(r"(\d{4}-\d{2}-\d{2})", page.stem)
        freshness = 0.5 ** ((today - date.fromisoformat(stamp.group(1))).days / FRESHNESS_HALF_LIFE_DAYS) if stamp else 0.0
        links = min(1.0, incoming[page.stem] / 5)
        mentions = min(1.0, log_text.count(page.stem) / 3)
        scores.append((0.4 * links + 0.3 * freshness + 0.3 * mentions, str(page.relative_to(ROOT))))
    scores.sort(reverse=True)

    raw_files = [p for kind in ("articles", "papers", "transcripts") for p in markdown_files(ROOT / "raw" / kind)]
    print(f"Wiki root: {ROOT}")
    print(f"Content pages: {len(pages)} | Raw markdown sources: {len(raw_files)}")
    print(f"Index links: {len(names_in_index)}")
    print(f"Errors: {len(errors)} | Warnings: {len(warnings)}")
    for item in errors:
        print(f"ERROR  {item}")
    for item in warnings:
        print(f"WARN   {item}")
    if scores:
        print("Fitness top 5（提炼/交叉候选）:")
        for score, name in scores[:5]:
            print(f"  {score:.2f}  {name}")
        print("Fitness bottom 5（沉底/清理候选）:")
        for score, name in scores[-5:]:
            print(f"  {score:.2f}  {name}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
