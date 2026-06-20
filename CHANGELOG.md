# Changelog

All notable changes to BrainKu are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-06-20

### Added
- Initial scaffold of the Karpathy LLM Wiki pattern.
- `schema.md` — domain-flexible conventions, frontmatter spec, tag taxonomy, page thresholds.
- `AGENT.md` — operational playbook for LLM agents (orientation, ingest/query/lint workflows, pitfalls).
- `GUIDE.md` — full install + usage for Reader, Curator, Agent, Contributor.
- `README.md` — human-facing overview, layout, quick-start.
- `index.md` — content catalog (empty).
- `log.md` — chronological action log.
- `LICENSE` — MIT.
- `scripts/lint.py` — programmatic linter covering all 13 lint categories from
  the llm-wiki skill (orphan pages, broken wikilinks, index completeness,
  frontmatter validation, stale content, contradictions, quality signals,
  source drift, page size, tag audit, log rotation).
- `.gitignore` — editor/OS, Obsidian local state, venv, build cache.
- `raw/{articles,papers,transcripts,assets}/` — immutable source directories.
- `entities/`, `concepts/`, `comparisons/` — wiki page directories.
- `queries/{research,daily}/` — filed query results.
- `_meta/` — meta-documents.

### Notes
- This is the initial public release. The wiki is empty by design — drop a
  source into `raw/` and ask the agent to ingest it to start compounding.
- MkDocs publishing is intentionally not implemented (per user request).
  See `GUIDE.md § Publishing as a static site` for the documented path
  to enable it later without restructuring.
- Pattern source: [Karpathy LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).
- Agent playbook derived from: Hermes `research/llm-wiki` skill v2.2.0.
