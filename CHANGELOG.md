# Changelog

All notable changes to BrainKu are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2026-06-20

### Added
- **Output formats** for query answers (markdown, comparison table, Marp slide deck,
  matplotlib chart, drawio/Mermaid canvas) in `AGENTS.md § Query`.
- **qmd** as the recommended search tool for large wikis (BM25 + vector + LLM
  re-ranking, on-device) in `AGENTS.md § qmd`.
- **Tips and tricks** section consolidating Karpathy's tips (Obsidian Web Clipper,
  image downloads, graph view, Marp, Dataview, grep log tip) in `AGENTS.md`.
- **Why this works + Memex (1945)** historical context section in `AGENTS.md`.
- **Lint category 14: concepts mentioned but lacking their own page** — surfaces
  wikilink targets that are referenced 2+ times but have no page. Helps the agent
  decide which missing concepts to create.
- **Lint category 14: Suggested next actions** — output section in `scripts/lint.py`
  report. Proposes page creation, source searches, page refreshes, contested-page
  reconciliation based on findings.

### Changed
- **Renamed `AGENT.md` → `AGENTS.md`** to match Karpathy's pattern (the gist says
  "AGENTS.md for Codex"). All references updated across `README.md`, `schema.md`,
  `log.md`, `index.md`, `GUIDE.md`, `CHANGELOG.md`, and `scripts/lint.py`.

### Notes
- This round was triggered by a request to re-read the source gist (Karpathy's
  75-line original) and find anything missed. Six gaps identified and fixed.
- The wiki is still empty (no sources ingested). All changes are documentation
  and tooling only.

## [0.1.0] - 2026-06-20

### Added
- Initial scaffold of the Karpathy LLM Wiki pattern.
- `schema.md` — domain-flexible conventions, frontmatter spec, tag taxonomy, page thresholds.
- `AGENTS.md` — operational playbook for LLM agents (orientation, ingest/query/lint workflows, pitfalls).
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
