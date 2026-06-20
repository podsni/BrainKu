# AGENTS.md — BrainKu Agent Playbook

> Operational playbook for LLM agents (Hermes, Codex, Claude Code, OpenCode, etc.) maintaining BrainKu.
> Read `schema.md` and `index.md` first, then this file.

## Orientation (do this FIRST every session)

Before any ingest, query, or lint, orient yourself. Skipping this causes duplicates and
missed cross-references.

```
1. Read schema.md       → understand domain, conventions, tag taxonomy
2. Read index.md        → see what pages exist
3. Read log.md (last 20-30 entries) → understand recent activity
4. Search the wiki if the topic has many pages
```

Only after orientation should you touch anything.

## Operations

### 1. Ingest

When the user provides a source (URL, file path, pasted text, dropped into `raw/`):

1. **Capture the raw source.**
   - URL → `web_extract` → save bytes to `raw/articles/<slug>.md` with frontmatter.
   - File path → copy as-is to appropriate `raw/` subdir.
   - Pasted text → save to appropriate `raw/` subdir.
   - **Slug naming:** lowercase, hyphens, descriptive. Example: `karpathy-llm-wiki-2026.md`.

2. **Compute sha256 of the body and write raw frontmatter.**
   ```bash
   # body = everything after the second "---"
   sha256sum /tmp/source-body.txt
   ```
   Write frontmatter with `source_url`, `ingested` (today), `sha256`. **The body must be
   byte-exact** — no extra newlines, no reformatting. After writing, re-extract the body and
   verify the sha256 matches.

3. **Discuss takeaways with the user** (skip in automated/cron contexts). What's interesting?
   What entities/concepts surfaced?

4. **Check what already exists.** Read `index.md`, then `search_files` for any entities or
   concepts the source mentions. This is the difference between a growing wiki and duplicates.

5. **Write or update wiki pages.**
   - **New entity/concept:** create only if it meets Page Thresholds in `schema.md`
     (2+ source mentions OR central to one source). Every new page must link to ≥2 others.
   - **Existing page:** add new info, bump `updated:` date. If it contradicts existing
     content, follow the Update Policy in `schema.md`.
   - **Cross-reference:** every page must link to at least 2 other pages via `[[wikilinks]]`.
   - **Tags:** only use tags from the taxonomy in `schema.md`. Add new tags to the
     schema first.
   - **Provenance:** on pages synthesizing 3+ sources, append `^[raw/articles/source.md]`
     markers to paragraphs whose claims trace to a specific source.
   - **Confidence:** set `confidence: medium` or `low` on opinion-heavy, fast-moving, or
     single-source claims.

6. **Update navigation.**
   - Add new/updated pages to `index.md` under the correct section, alphabetical.
   - Update "Total pages" count and "Last updated" date in `index.md` header.
   - Append to `log.md`: `## [YYYY-MM-DD] ingest | Source Title` with a list of every file
     created/updated.

7. **Report.** Tell the user every file created or updated.

A single source can trigger updates across 5–15 wiki pages. This is the compounding effect —
it is normal and desired.

### 2. Query

When the user asks a question about BrainKu's domain:

1. Read `index.md` to identify relevant pages.
2. For wikis with 100+ pages, also `search_files` across all `.md` for key terms.
3. Read the relevant pages.
4. Synthesize an answer from the compiled knowledge. Cite wiki pages: "Based on
   `[[page-a]]` and `[[page-b]]`..." (real wikilinks, not placeholders)
5. **File valuable answers back** — if the answer is a substantial comparison, deep dive,
   or novel synthesis, create a page in `queries/` or `comparisons/`. Don't file trivial
   lookups — only answers that would be painful to re-derive.
6. Update `log.md` with the query and whether it was filed.

#### Output formats

Answers can take different forms depending on the question. The gist's spec calls
out these output formats — pick the one that matches the question, not the default:

- **Markdown page** — the default. A wiki page synthesis, written in markdown with
  `[[wikilinks]]`. File it in `queries/research/` if it's substantial.
- **Comparison table** — when comparing 2+ entities/concepts side by side. Pipe tables
  in markdown. File as a `comparisons/` page.
- **Slide deck (Marp)** — for presentations. Use Marp frontmatter (`marp: true`) +
  `---` separators for slides. File as a `.md` page in `queries/` or `_meta/`.
- **Chart (matplotlib)** — for data-driven questions. Generate a `.png` via Python's
  matplotlib, save to `raw/assets/`, embed via `![[filename.png]]` in the wiki page.
- **Canvas** — for freeform visual explanations (diagrams, flow charts). Use a
  draw.io XML file saved to `raw/assets/canvas.drawio`, or a Mermaid block embedded
  in the wiki page directly.

When in doubt, default to markdown. The other formats are upgrades for specific
question shapes.

### 3. Lint

When the user asks to lint, health-check, or audit BrainKu:

1. **Orphan pages** — pages with no inbound `[[wikilinks]]` from other pages.
2. **Broken wikilinks** — `[[links]]` pointing to pages that don't exist.
   - **Strip code spans/blocks** before scanning (literal `[[wikilinks]]` in docs
     are not broken links).
   - **Match case-insensitively** — `[[schema]]` resolves to `schema.md`.
   - **Flag placeholder links** — `[[page-a]]`, `[[xxx]]`, `[[TODO]]` are bugs, not examples.
3. **Index completeness** — every wiki page must appear in `index.md`.
4. **Frontmatter validation** — every wiki page must have `title, created, updated, type, tags, sources`.
   Tags must be in the schema taxonomy.
5. **Stale content** — pages whose `updated:` is >90 days older than the most recent source
   mentioning the same entities.
6. **Contradictions** — pages on the same topic with conflicting claims. Surface all pages
   with `contested: true` or `contradictions:` frontmatter.
7. **Quality signals** — list pages with `confidence: low` and any page that cites only a
   single source but has no `confidence:` field set.
8. **Source drift** — for each `raw/` file, recompute sha256 and flag mismatches.
9. **Page size** — flag pages over 200 lines (candidates for splitting).
10. **Tag audit** — list all tags in use, flag any not in `schema.md` taxonomy.
11. **Log rotation** — if `log.md` exceeds 500 entries, rotate it.
12. **Report findings** grouped by severity (broken links > orphans > drift > contested > stale > style).
13. **Append to `log.md`:** `## [YYYY-MM-DD] lint | N issues found`.
14. **Suggest next actions** — from the findings, suggest:
    - **New sources to look for** — pages that have low confidence / single source / stale
      content. The agent should propose web searches to fill the gaps.
    - **New questions to investigate** — gaps in the wiki that would benefit from a
      targeted query.
    - **Promote mentioned-no-page concepts** — if a concept is referenced 2+ times but
      has no page, propose creating one.
    The linter surfaces these as a "Suggested next actions" section in its report.

## Frontmatter spec

**Wiki pages:**
```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | summary
tags: [from taxonomy]
sources: [raw/articles/source-name.md]
confidence: high | medium | low   # optional
contested: true                    # optional
contradictions: [other-page-slug]  # optional
---
```

**Raw files:**
```yaml
---
source_url: https://example.com/article
ingested: YYYY-MM-DD
sha256: <hex digest of body>
---
```

## Pitfalls (read these, save yourself pain)

- **Never modify files in `raw/`.** Sources are immutable. Corrections go in wiki pages.
- **Always orient first.** Read schema + index + recent log before any operation. Skipping
  this causes duplicates and missed cross-references.
- **Always update `index.md` and `log.md`.** Skipping this makes the wiki degrade. These
  are the navigational backbone.
- **Don't create pages for passing mentions.** Follow Page Thresholds in `schema.md`. A name
  in a footnote doesn't warrant an entity page.
- **Don't create pages without cross-references.** Isolated pages are invisible. Every page
  must link to ≥2 others.
- **Frontmatter is required.** It enables search, filtering, and staleness detection.
- **Tags must come from the taxonomy.** Freeform tags decay into noise. Add new tags to
  `schema.md` first, then use them.
- **Keep pages scannable.** A wiki page should be readable in 30 seconds. Split pages over
  200 lines.
- **Ask before mass-updating.** If an ingest would touch 10+ existing pages, confirm the
  scope with the user first.
- **Handle contradictions explicitly.** Don't silently overwrite. Note both claims with
  dates, mark in frontmatter, flag for review.
- **Raw body must be byte-exact with source.** A re-serialized body, a stripped trailing
  newline, or a "fixed" typo in the body all break the sha256. Never hand-edit a `raw/`
  file. See `GUIDE.md` for the full ingest procedure.
- **Lint: strip code spans before wikilink scan.** Otherwise literal `[[wikilinks]]` in
  backticks register as broken links.
- **Lint: case-insensitive page-name matching.** `[[schema]]` must resolve to `schema.md`.
- **Lint: placeholder links are bugs, not examples.** `[[page-a]]`, `[[xxx]]` in body text
  mean the author forgot to fill them in. Fix them; don't suppress.
- **Page name convention: lowercase-hyphen.** `schema.md`, not `SCHEMA.md`. The uppercase
  form breaks cross-platform case-insensitive matching.
- **Rotate the log when it exceeds 500 entries.** Rename to `log-YYYY.md` and start fresh.
  The linter flags this; don't wait for the wiki to slow down before rotating.
- **Meta files (`index.md`, `log.md`, `schema.md`, plus companion docs `README.md`,
  `AGENTS.md`, `GUIDE.md`, `CHANGELOG.md`, `scripts/README.md`) are not wiki content.**
  They have no `sources:` field, don't appear in `index.md`, don't count as orphans,
  and may legitimately exceed the 200-line size hint. The linter exempts them via
  `EXEMPT_FROM_WIKI_CHECKS`. Don't lint them as if they were wiki pages.

**See [`GUIDE.md` § Deployment pitfalls](GUIDE.md#deployment-pitfalls) for the two
git/Unicode pitfalls that hit when bootstrapping the repo.**

## Bulk ingest

When ingesting multiple sources at once, batch the updates:

1. Read all sources first.
2. Identify all entities and concepts across all sources.
3. Check existing pages for all of them (one search pass, not N).
4. Create/update pages in one pass (avoids redundant updates).
5. Update `index.md` once at the end.
6. Write a single log entry covering the batch.

## Archiving

When content is fully superseded or domain scope changes:

1. Create `_archive/` if it doesn't exist.
2. Move the page to `_archive/` with its original path
   (e.g., `_archive/entities/old-page.md`).
3. Remove from `index.md`.
4. Update any pages that linked to it — replace wikilink with plain text + "(archived)".
5. Log the archive action.

## Obsidian integration

BrainKu works as an Obsidian vault out of the box:

- `[[wikilinks]]` render as clickable links.
- Graph View visualizes the knowledge network.
- YAML frontmatter powers Dataview queries.
- The `raw/assets/` folder holds images referenced via `![[image.png]]`.

For best results:

- Set Obsidian's attachment folder to `raw/assets/`.
- Enable "Wikilinks" in Obsidian settings (default on).
- Install Dataview plugin for queries like
  `TABLE tags FROM "entities" WHERE contains(tags, "entity")`.

## qmd (recommended search tool)

When the wiki grows past ~hundreds of pages, the `index.md` catalog alone is no
longer enough. The gist recommends **[qmd](https://github.com/tobi/qmd)** — a
local search engine for markdown files with hybrid BM25 + vector search + LLM
re-ranking, all on-device.

- **CLI** — so the agent can shell out: `qmd search "transformer architecture"`
- **MCP server** — so the agent can use it as a native tool (preferred when
  running in Hermes or Claude Code)
- **All on-device** — no cloud, no API keys, no embeddings database to manage

Install:

```bash
# qmd requires Bun
curl -fsSL https://bun.sh/install | bash
bun install -g https://github.com/tobi/qmd
```

Use qmd as the search step in the Query workflow (step 2) and as an alternative
to `search_files` in larger wikis. Fall back to the `index.md` catalog for small
wikis where qmd is overkill.

## Tips and tricks (from the gist)

These are workflow tips from the source spec that the agent should know about.
The first three are user-facing; the rest are mostly agent-facing.

- **Obsidian Web Clipper** is a browser extension that converts web articles to
  clean markdown. Use it to drop new sources directly into `raw/articles/`. The
  agent then ingests from there.
- **Download images locally.** In Obsidian Settings → Files and links, set
  "Attachment folder path" to `raw/assets/`. Bind "Download attachments for
  current file" to a hotkey (e.g. Ctrl+Shift+D). After clipping an article, hit
  the hotkey and all images get downloaded to local disk. The LLM can then read
  the text first, then view some/all of the referenced images separately to
  gain additional context. It's a bit clunky but works well enough.
- **Obsidian's graph view** is the best way to see the shape of the wiki —
  what's connected to what, which pages are hubs, which are orphans.
- **Marp** is a markdown-based slide deck format. Obsidian has a plugin for it.
  Useful when a query answer should be a presentation rather than a wiki page.
- **Dataview** is an Obsidian plugin that runs queries over page frontmatter. If
  the agent adds YAML frontmatter consistently (tags, dates, source counts),
  Dataview can generate dynamic tables and lists. The LLM doesn't run Dataview,
  but the human can.
- **The wiki is just a git repo.** You get version history, branching, and
  collaboration for free. The agent should commit after every meaningful batch
  of changes.
- **`grep '^## \[' log.md | tail -5`** gives you the last 5 log entries with
  simple unix tools. The `## [YYYY-MM-DD] action | subject` prefix is
  intentionally parseable so the log is greppable without a custom parser.

## Why this works (and a historical note)

From the gist's closing section, with the historical context preserved.

The tedious part of maintaining a knowledge base is not the reading or the
thinking — it's the bookkeeping. Updating cross-references, keeping summaries
current, noting when new data contradicts old claims, maintaining consistency
across dozens of pages. Humans abandon wikis because the maintenance burden
grows faster than the value. LLMs don't get bored, don't forget to update a
cross-reference, and can touch 15 files in one pass. The wiki stays maintained
because the cost of maintenance is near zero.

The human's job is to curate sources, direct the analysis, ask good questions,
and think about what it all means. The LLM's job is everything else.

**Historical context — Vannevar Bush's Memex (1945).** The idea is related in
spirit to Bush's Memex — a personal, curated knowledge store with associative
trails between documents. Bush's vision was closer to this pattern than to
what the web became: private, actively curated, with the connections between
documents as valuable as the documents themselves. The part he couldn't solve
was who does the maintenance. The LLM handles that.

Consider creating a `concepts/memex.md` page if your domain intersects with
knowledge-management history.
