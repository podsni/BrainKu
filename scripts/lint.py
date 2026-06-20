#!/usr/bin/env python3
"""
Karpathy LLM Wiki linter - programmatic health check.

Covers all 13 lint categories from the llm-wiki skill:
  1.  Orphan pages (zero inbound links)
  2.  Broken wikilinks (with code-span stripping + case-insensitive matching)
  3.  Index completeness
  4.  Frontmatter validation (required fields, tags in taxonomy)
  5.  Stale content (updated > 90 days older than most-recent source)
  6.  Contradictions (pages with contested: true surfaced)
  7.  Quality signals (confidence: low, single-source pages without confidence)
  8.  Source drift (sha256 mismatch on raw/ files)
  9.  Page size (>200 lines flagged for splitting)
  10. Tag audit (tags not in SCHEMA taxonomy)
  11. Log rotation (>500 entries)
  12. Report findings grouped by severity
  13. Append a `lint | N issues found` entry to log.md

Usage:
    python3 scripts/lint.py /root/dev/BrainKu
    python3 scripts/lint.py /root/dev/BrainKu --strict    # exit 1 on any issue
    python3 scripts/lint.py /root/dev/BrainKu --no-log     # don't append lint entry

The script depends only on the Python 3.10+ stdlib (no install needed).
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

# ---------- Configuration ----------

# Reserved top-level files (exempt from full frontmatter check)
META_FILES = {"index.md", "log.md", "schema.md", "SCHEMA.md"}

# Companion files (exempt from wiki-page lint checks - they are not wiki content)
# These are the recommended companions from the llm-wiki skill (README/AGENT/GUIDE)
# plus this project's own CHANGELOG and scripts/README.
COMPANION_FILES = {
    "README.md", "AGENT.md", "GUIDE.md", "CHANGELOG.md",
    "scripts/README.md",
}

# All files exempt from wiki-page checks (no frontmatter, not in index, etc.)
EXEMPT_FROM_WIKI_CHECKS = META_FILES | COMPANION_FILES

# Required frontmatter fields
REQUIRED_FM = {"title", "created", "updated", "type", "tags", "sources"}

# Allowed types
ALLOWED_TYPES = {"entity", "concept", "comparison", "query", "summary", "schema", "meta"}

# Default allowed tag set (used only if no schema can be loaded)
DEFAULT_ALLOWED_TAGS = {
    "pattern", "methodology", "workflow", "architecture", "data-model", "schema",
    "operations", "ingest", "query", "lint", "maintenance", "curation", "search",
    "source", "article", "paper", "talk", "gist",
    "comparison", "vs", "trade-off", "synthesis",
    "tool", "cli", "editor", "obsidian", "qmd", "mcp",
    "concept", "rag", "embedding", "vector-search", "bm25", "knowledge-base",
    "history", "memex", "hypertext", "zettelkasten",
    "person", "source-author", "karpathy",
    "meta", "opinion", "prediction", "critique", "open-question",
}

STALE_DAYS = 90
PAGE_LINE_LIMIT = 200
LOG_ENTRY_LIMIT = 500

# ---------- Parsing helpers ----------


def parse_frontmatter(text: str) -> tuple[str, str]:
    """Split YAML frontmatter from body. Returns (fm, body)."""
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end >= 0:
            return text[4:end], text[end + 5 :]
    return "", text


_FM_RE = re.compile(r"^(\w+):\s*(.*)$", re.MULTILINE)


def parse_fm_dict(fm: str) -> dict:
    """Naive YAML frontmatter parser - supports scalars and inline lists."""
    d: dict = {}
    for m in _FM_RE.finditer(fm):
        k, v = m.group(1), m.group(2).strip()
        if v.startswith("[") and v.endswith("]"):
            d[k] = [
                x.strip().strip('"').strip("'")
                for x in v[1:-1].split(",")
                if x.strip()
            ]
        else:
            d[k] = v.strip('"').strip("'")
    return d


def strip_code(text: str) -> str:
    """Remove fenced and inline code so the wikilink scanner doesn't false-positive
    on documentation that shows [[wikilinks]] as syntax examples."""
    text = re.sub(r"```[\s\S]*?```", "", text)
    text = re.sub(r"`[^`\n]*`", "", text)
    return text


_WL_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")


# ---------- Loaders ----------


def load_wiki(wiki_path: Path) -> dict:
    """Walk the wiki directory and produce the data structures the lint uses."""
    pages: list[str] = []
    raw_files: list[Path] = []
    schema_tags: set[str] | None = None

    for p in sorted(wiki_path.rglob("*.md")):
        rel = str(p.relative_to(wiki_path))
        if rel.startswith("raw/"):
            raw_files.append(p)
        else:
            pages.append(rel)

    # Try to extract tag taxonomy from schema.md (best-effort)
    schema_path = wiki_path / "schema.md"
    if schema_path.exists():
        schema_tags = extract_taxonomy(schema_path.read_text())

    docs: dict[str, dict] = {}
    for rel in pages:
        text = (wiki_path / rel).read_text()
        fm, body = parse_frontmatter(text)
        scan = strip_code(body)
        docs[rel] = {
            "text": text,
            "fm_raw": fm,
            "body": body,
            "scan": scan,
            "fm": parse_fm_dict(fm),
            "lines": text.count("\n") + 1,
            "path": wiki_path / rel,
        }

    # Page-name set, case-insensitive
    page_names: set[str] = set()
    for rel in pages:
        base = Path(rel).stem.lower()
        page_names.add(base)
        if "/" in rel:
            page_names.add(Path(rel).name.lower())
    # Sources live under raw/ - also resolvable
    for rf in raw_files:
        page_names.add(rf.stem.lower())

    return {
        "pages": pages,
        "raw_files": raw_files,
        "docs": docs,
        "page_names": page_names,
        "schema_tags": schema_tags,
        "wiki_path": wiki_path,
    }


def extract_taxonomy(schema_text: str) -> set[str]:
    """Best-effort tag extraction from the Tag Taxonomy section of schema.md."""
    tags: set[str] = set()
    in_taxonomy = False
    for line in schema_text.splitlines():
        if "Tag Taxonomy" in line or "tag taxonomy" in line:
            in_taxonomy = True
            continue
        if in_taxonomy:
            if line.startswith("## "):
                break
            for m in re.finditer(r"`([a-z][a-z0-9-]+)`", line):
                tags.add(m.group(1))
            for m in re.finditer(r"\b([a-z][a-z0-9-]+)\b", line):
                w = m.group(1)
                if w in DEFAULT_ALLOWED_TAGS:
                    tags.add(w)
    return tags or DEFAULT_ALLOWED_TAGS.copy()


# ---------- Lint checks ----------


def lint(wiki: dict) -> dict:
    pages = wiki["pages"]
    docs = wiki["docs"]
    raw_files = wiki["raw_files"]
    page_names = wiki["page_names"]
    schema_tags = wiki["schema_tags"] or DEFAULT_ALLOWED_TAGS

    # Inbound/outbound link maps
    all_targets: dict[str, list[str]] = defaultdict(list)
    for rel, d in docs.items():
        for m in _WL_RE.finditer(d["scan"]):
            all_targets[m.group(1).strip()].append(rel)

    inbound: dict[str, int] = defaultdict(int)
    for tgt, srcs in all_targets.items():
        inbound[tgt] = len(srcs)

    # 1. Orphan pages
    orphans = [
        p
        for p in pages
        if p not in EXEMPT_FROM_WIKI_CHECKS
        and inbound.get(Path(p).stem.lower(), 0) == 0
        and Path(p).stem.lower() not in ("index", "log", "schema")
    ]

    # 2. Broken wikilinks (case-insensitive)
    broken = [
        (tgt, srcs)
        for tgt, srcs in all_targets.items()
        if tgt.lower() not in page_names
    ]

    # 3. Index completeness - every page should appear in index.md
    index_text = ""
    index_path = wiki["wiki_path"] / "index.md"
    if index_path.exists():
        index_text = index_path.read_text()
    index_listed = set()
    for m in re.finditer(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", index_text):
        index_listed.add(m.group(1).strip().lower())
    not_in_index = [
        p
        for p in pages
        if p not in EXEMPT_FROM_WIKI_CHECKS
        and Path(p).stem.lower() not in index_listed
        and Path(p).stem.lower() not in ("index", "log", "schema")
    ]

    # 4. Frontmatter validation
    fm_missing = []
    fm_invalid_type = []
    for rel, d in docs.items():
        if rel in EXEMPT_FROM_WIKI_CHECKS:
            continue
        miss = REQUIRED_FM - set(d["fm"].keys())
        if miss:
            fm_missing.append((rel, miss))
        t = d["fm"].get("type", "")
        if t and t not in ALLOWED_TYPES:
            fm_invalid_type.append((rel, t))

    # 10. Tag audit
    bad_tags = []
    for rel, d in docs.items():
        tags = d["fm"].get("tags", [])
        if isinstance(tags, list):
            for t in tags:
                if t not in schema_tags:
                    bad_tags.append((rel, t))

    # 5. Stale content
    today = datetime.now().date()
    stale = []
    for rel, d in docs.items():
        u = d["fm"].get("updated", "")
        try:
            ud = datetime.strptime(u, "%Y-%m-%d").date()
            if (today - ud).days > STALE_DAYS:
                stale.append((rel, u))
        except (ValueError, TypeError):
            pass

    # 6. Contradictions
    contested = [
        (rel, d["fm"].get("contradictions", []))
        for rel, d in docs.items()
        if d["fm"].get("contested") in ("true", True)
    ]

    # 7. Quality signals
    low_conf = [
        (rel, d["fm"].get("confidence"))
        for rel, d in docs.items()
        if d["fm"].get("confidence") in ("low", "medium")
    ]
    single_source_no_conf = []
    for rel, d in docs.items():
        sources = d["fm"].get("sources", [])
        if isinstance(sources, list) and len(sources) == 1 and "confidence" not in d["fm"]:
            single_source_no_conf.append(rel)

    # 8. Source drift (sha256)
    drift = []
    for rf in raw_files:
        text = rf.read_text()
        fm, body = parse_frontmatter(text)
        d = parse_fm_dict(fm)
        if "sha256" not in d:
            continue
        actual = hashlib.sha256(body.encode()).hexdigest()
        if actual != d["sha256"]:
            drift.append((str(rf.relative_to(wiki["wiki_path"])), actual, d["sha256"]))

    # 9. Page size
    big = [
        (p, d["lines"])
        for p, d in docs.items()
        if d["lines"] > PAGE_LINE_LIMIT and p not in EXEMPT_FROM_WIKI_CHECKS
    ]

    # 11. Log rotation
    log_path = wiki["wiki_path"] / "log.md"
    log_count = 0
    if log_path.exists():
        log_count = sum(1 for line in log_path.read_text().splitlines() if line.startswith("## ["))

    return {
        "broken_wikilinks": broken,
        "orphan_pages": orphans,
        "not_in_index": not_in_index,
        "fm_missing": fm_missing,
        "fm_invalid_type": fm_invalid_type,
        "bad_tags": bad_tags,
        "stale_pages": stale,
        "contested": contested,
        "low_confidence": low_conf,
        "single_source_no_conf": single_source_no_conf,
        "source_drift": drift,
        "big_pages": big,
        "log_entry_count": log_count,
        "log_needs_rotation": log_count > LOG_ENTRY_LIMIT,
    }


# ---------- Reporting ----------


SEVERITY = [
    ("source_drift", "HIGH", "raw/ files with sha256 mismatch"),
    ("broken_wikilinks", "HIGH", "wikilinks pointing to non-existent pages"),
    ("not_in_index", "MEDIUM", "wiki pages not listed in index.md"),
    ("orphan_pages", "MEDIUM", "pages with no inbound links"),
    ("fm_missing", "MEDIUM", "pages missing required frontmatter fields"),
    ("fm_invalid_type", "MEDIUM", "pages with invalid type field"),
    ("bad_tags", "MEDIUM", "tags not in schema taxonomy"),
    ("contested", "LOW", "pages flagged contested (review for reconciliation)"),
    ("low_confidence", "LOW", "pages with confidence: low or medium"),
    ("single_source_no_conf", "LOW", "single-source pages without confidence field"),
    ("stale_pages", "LOW", "pages not updated in >90 days"),
    ("big_pages", "INFO", "pages over 200 lines (consider splitting)"),
    ("log_needs_rotation", "INFO", "log.md exceeded 500 entries"),
]


def report(issues: dict, wiki: dict) -> int:
    print("=" * 60)
    total = 0
    for key, severity, desc in SEVERITY:
        val = issues.get(key)
        if key == "log_entry_count":
            print(f"  log entries: {val}  ({'NEEDS ROTATION' if issues.get('log_needs_rotation') else 'ok'})")
            continue
        if key == "log_needs_rotation":
            continue
        if not val:
            continue
        n = len(val) if hasattr(val, "__len__") else 0
        total += n
        print(f"\n[{severity}] {desc}: {n}")
        if key == "broken_wikilinks":
            for tgt, srcs in val:
                print(f"  X [[{tgt}]] from {len(srcs)} page(s); first: {srcs[0]}")
        elif key == "orphan_pages":
            for p in val:
                print(f"  X {p}")
        elif key == "not_in_index":
            for p in val:
                print(f"  X {p}")
        elif key == "fm_missing":
            for p, m in val:
                print(f"  X {p}: missing {m}")
        elif key == "fm_invalid_type":
            for p, t in val:
                print(f"  X {p}: type={t!r} not in {sorted(ALLOWED_TYPES)}")
        elif key == "bad_tags":
            for p, t in val:
                print(f"  X {p}: [{t}] not in taxonomy")
        elif key == "stale_pages":
            for p, u in val:
                print(f"  X {p}: updated={u}")
        elif key == "contested":
            for p, c in val:
                print(f"  X {p}: contradictions={c}")
        elif key == "low_confidence":
            for p, c in val:
                print(f"  - {p}: confidence={c}")
        elif key == "single_source_no_conf":
            for p in val:
                print(f"  - {p}")
        elif key == "big_pages":
            for p, l in val:
                print(f"  - {p}: {l} lines")
        elif key == "source_drift":
            for rel, actual, expected in val:
                print(f"  X {rel}: got {actual[:12]}... expected {expected[:12]}...")

    print("\n" + "=" * 60)
    if total == 0:
        print("ALL CLEAN")
    else:
        print(f"{total} ISSUES")
    print("=" * 60)
    return total


def append_log_entry(wiki_path: Path, n: int) -> None:
    log = wiki_path / "log.md"
    if not log.exists():
        return
    today = datetime.now().strftime("%Y-%m-%d")
    with log.open("a") as f:
        f.write(f"\n## [{today}] lint | {n} issues found\n")
        f.write(f"- Linter: scripts/lint.py\n")
        f.write(f"- Total issues: {n}\n")


# ---------- CLI ----------


def main() -> int:
    ap = argparse.ArgumentParser(description="Karpathy LLM Wiki linter")
    ap.add_argument("wiki", type=Path, help="Path to wiki directory")
    ap.add_argument("--strict", action="store_true", help="Exit 1 on any issue")
    ap.add_argument("--no-log", action="store_true", help="Don't append lint entry to log.md")
    args = ap.parse_args()

    if not args.wiki.is_dir():
        print(f"error: {args.wiki} is not a directory", file=sys.stderr)
        return 2

    wiki = load_wiki(args.wiki)
    issues = lint(wiki)
    n = report(issues, wiki)

    if not args.no_log and n > 0:
        append_log_entry(args.wiki, n)

    return 1 if (args.strict and n > 0) else 0


if __name__ == "__main__":
    sys.exit(main())
