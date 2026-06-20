# scripts/

Operational scripts for BrainKu. Each script is a self-contained Python 3.10+
program with no external dependencies (stdlib only).

## `lint.py` — wiki health check

Programmatic linter covering all 13 categories from the llm-wiki skill:

1. Orphan pages (zero inbound links)
2. Broken wikilinks (with code-span stripping + case-insensitive matching)
3. Index completeness
4. Frontmatter validation
5. Stale content
6. Contradictions
7. Quality signals (confidence + single-source flags)
8. Source drift (sha256 mismatch on raw/ files)
9. Page size (>200 lines flagged)
10. Tag audit (tags not in SCHEMA taxonomy)
11. Log rotation (>500 entries)
12. Report findings grouped by severity
13. Append a `lint | N issues found` entry to log.md

### Usage

```bash
# Run lint (exits 0 always; reports findings)
python3 scripts/lint.py /root/dev/BrainKu

# Run lint in strict mode (exit 1 on any issue; useful in CI)
python3 scripts/lint.py /root/dev/BrainKu --strict

# Run lint without appending a log entry
python3 scripts/lint.py /root/dev/BrainKu --no-log
```

### Exit codes

| Code | Meaning |
|------|---------|
| 0    | Clean (or no `--strict`) |
| 1    | Issues found (only with `--strict`) |
| 2    | Bad CLI args / wiki path not a directory |
