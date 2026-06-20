# Changelog

All notable changes to BrainKu are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- **Removed the `Publishing as a static site` section from `GUIDE.md`** per user
  request. BrainKu ships as a local vault + GitHub repo only; the MkDocs/Material
  publishing path is intentionally not part of this project. The 108-line section
  covered MkDocs setup, GitHub Pages workflow, Obsidian-like UI plugins, and
  mkdocs.yml examples. All removed; the deployment pitfalls section (Unicode gh
  CLI, older git) is preserved as it's independent of MkDocs.

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

## [0.3.0] - 2026-06-20

### Added
- **Lint category 15: Missing cross-references** — pages with <2 outbound
  `[[wikilinks]]`. Per `schema.md`, every page must link to at least 2
  others. Different from `orphan_pages` (which is the inbound direction).
  MEDIUM severity. Configurable via `MIN_OUTBOUND_WIKILINKS` constant.
- **Page types `synthesis` and `overview`** — added to `ALLOWED_TYPES` in
  `scripts/lint.py`, to `schema.md § Page Types`, and to the frontmatter
  spec in `AGENTS.md`. `synthesis` is a novel cross-cutting analysis that
  goes beyond any individual source (the most valuable page type).
  `overview` is a higher-level landing page that frames a sub-area.
- **`Sources` section in `index.md`** — Karpathy's example categorizes the
  index as "entities, concepts, sources, etc.". The new section lists
  per-source summary pages and acts as a navigable entry point to the
  raw/ collection.
- **Index entry format with metadata** — `_(updated YYYY-MM-DD, N sources)_`
  appended to each entry, plus optional `[low conf]` / `[contested]` markers.
  Matches the gist's "a link, a one-line summary, and optionally metadata
  like date or source count".
- **`Overviews` and `Syntheses` sections in `index.md`** — separate from
  generic `Comparisons` and `Queries` to match the new page types.
- **"What you can use it for" section in `README.md`** — 5 example use
  cases from the gist (Personal, Research, Reading a book, Business/team,
  Competitive analysis etc.).
- **"Obsidian is the IDE" quote** in `README.md` and `schema.md` —
  the human-loop framing from the gist's intro.
- **"Everything mentioned above is optional and modular" note** in
  `README.md` — the closing principle from the gist's Note section.
- **"Schema is the key configuration file" + co-evolution framing** in
  `schema.md` — the gist emphasizes both: schema makes the LLM a
  disciplined maintainer, and it co-evolves with the user over time.
- **`Workflow preferences` section in `schema.md`** — the gist says "It's
  up to you to develop the workflow that fits your style and document it
  in the schema for future sessions." The new section gives concrete
  examples (source granularity, discussion depth, stale threshold, tag
  density).
- **First-action summary page in Ingest** — the gist's example flow leads
  with "writes a summary page in the wiki". The Ingest workflow now
  makes this explicit: every source gets a per-source summary page
  before entity/concept updates.
- **Vibe-code-a-search-script note in qmd section** — the gist explicitly
  offers this as an alternative to qmd for users who want something
  simpler. The qmd section in `AGENTS.md` now links to it.
- **`suggested_actions` enhanced** — surfaces two new action types:
  "Add cross-references to `[[page]]`" (from missing_xrefs) and
  "Either set confidence on `[[page]]` or find a second source" (from
  single_source_no_conf).

### Notes
- This round was triggered by a request to re-read the source gist (75 lines,
  12KB) line-by-line, not just trust the skill distillation. 8 distinct
  gaps identified from the gist that weren't captured previously.
- BrainKu is still empty (no sources ingested). All changes are docs +
  tooling only.
