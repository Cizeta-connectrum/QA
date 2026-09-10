#!/usr/bin/env python3
"""faq.md / glossary.md / sources.yaml を QA ボット取り込み用 JSONL に変換する。

使い方:
    python3 scripts/build_qa_dataset.py            # 全製品
    python3 scripts/build_qa_dataset.py landmarker # 指定製品のみ

出力: dist/<product_id>.qa.jsonl
    1 行 1 レコード。type は "faq" または "glossary"。
    {"id", "product_id", "type", "category", "question", "answer", "tags", "sources": [{id,title,drive_file_id}]}
標準ライブラリのみで動作する（PyYAML 不要）。
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS = ROOT / "products"
DIST = ROOT / "dist"

SRC_LABEL = re.compile(r"\[(S\d+)\]")


def parse_sources(path: Path) -> dict[str, dict]:
    """sources.yaml の最小パーサ。`- id:` で始まるブロックから id/title/drive_file_id を拾う。"""
    out: dict[str, dict] = {}
    cur: dict | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\s*-\s+id:\s*(\S+)", line)
        if m:
            cur = {"id": m.group(1)}
            out[cur["id"]] = cur
            continue
        if cur is None:
            continue
        m = re.match(r"\s+(title|drive_file_id):\s*(.+)", line)
        if m:
            cur[m.group(1)] = m.group(2).strip()
    return out


def split_sources(text: str, sources: dict[str, dict]) -> tuple[str, list[dict]]:
    ids = sorted(set(SRC_LABEL.findall(text)))
    clean = SRC_LABEL.sub("", text).strip()
    clean = re.sub(r"[ \t]+$", "", clean, flags=re.M)
    refs = [sources[i] for i in ids if i in sources]
    missing = [i for i in ids if i not in sources]
    if missing:
        print(f"  warn: 未定義の出典ラベル {missing}", file=sys.stderr)
    return clean, refs


def parse_faq(path: Path, product_id: str, sources: dict[str, dict]) -> list[dict]:
    records: list[dict] = []
    category = ""
    question: str | None = None
    answer_lines: list[str] = []
    tags: list[str] = []
    n = 0

    def flush() -> None:
        nonlocal question, answer_lines, tags, n
        if question is None:
            return
        n += 1
        answer, refs = split_sources("\n".join(answer_lines), sources)
        records.append(
            {
                "id": f"{product_id}-faq-{n:03d}",
                "product_id": product_id,
                "type": "faq",
                "category": category,
                "question": question,
                "answer": answer,
                "tags": tags,
                "sources": refs,
            }
        )
        question, answer_lines, tags = None, [], []

    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            flush()
            category = line[3:].strip()
        elif line.startswith("### Q:"):
            flush()
            question = line[6:].strip()
        elif line.startswith("A:") and question is not None:
            answer_lines.append(line[2:].strip())
        elif line.startswith("tags:") and question is not None:
            tags = [t.strip() for t in line[5:].split(",") if t.strip()]
        elif question is not None and line.strip() and not line.startswith("#"):
            answer_lines.append(line.strip())
    flush()
    return records


def parse_glossary(path: Path, product_id: str, sources: dict[str, dict]) -> list[dict]:
    records: list[dict] = []
    n = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"-\s+\*\*(.+?)\*\*:\s*(.+)", line)
        if not m:
            continue
        n += 1
        term, desc = m.group(1), m.group(2)
        answer, refs = split_sources(desc, sources)
        records.append(
            {
                "id": f"{product_id}-glossary-{n:03d}",
                "product_id": product_id,
                "type": "glossary",
                "category": "用語集",
                "question": f"{term}とは何ですか？",
                "answer": answer,
                "tags": ["用語"],
                "sources": refs,
            }
        )
    return records


def build(product_dir: Path) -> int:
    product_id = product_dir.name
    sources = parse_sources(product_dir / "sources.yaml")
    records: list[dict] = []
    faq = product_dir / "faq.md"
    glossary = product_dir / "glossary.md"
    if faq.exists():
        records += parse_faq(faq, product_id, sources)
    if glossary.exists():
        records += parse_glossary(glossary, product_id, sources)
    DIST.mkdir(exist_ok=True)
    out = DIST / f"{product_id}.qa.jsonl"
    with out.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"{product_id}: {len(records)} records -> {out.relative_to(ROOT)}")
    return len(records)


def main(argv: list[str]) -> int:
    targets = [PRODUCTS / a for a in argv] if argv else sorted(p for p in PRODUCTS.iterdir() if p.is_dir())
    total = 0
    for d in targets:
        if not d.is_dir():
            print(f"error: {d} が見つかりません", file=sys.stderr)
            return 1
        total += build(d)
    return 0 if total else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
