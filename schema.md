# BrainKu Schema

> Conventions, structure rules, and tag taxonomy for the BrainKu knowledge base.
> This file is **co-evolved** — edit it as the wiki grows, but always bump `updated` at the top.
> Read this file FIRST at the start of every session before doing anything else.

## Domain

**BrainKu** is a personal, compounding knowledge base. It is the LLM-owned side of the
Karpathy "LLM Wiki" pattern: the human curates sources and asks questions, the agent
summarizes, cross-references, files, and maintains consistency.

Use it for anything worth remembering across sessions: research, reading notes, projects,
ideas, decisions, references, comparisons, personal essays, technical deep-dives.

This schema is **domain-flexible** — it does not lock BrainKu into one topic. Specialize
tags and entity types below as the wiki grows.

> **Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase.**
> In practice the human runs Obsidian on one side of the screen, the LLM agent on the
> other. The LLM makes edits; the human browses the results in real time — following
> links, checking the graph view, reading updated pages. This loop is what makes the
> wiki feel alive.

> **The schema is the key configuration file.** It is what makes the LLM a
> disciplined wiki maintainer rather than a generic chatbot. It tells the agent how
> the wiki is structured, what the conventions are, and what workflows to follow
> when ingesting sources, answering questions, or maintaining the wiki.
>
> **You and the LLM co-evolve this over time as you figure out what works for your
> domain.** Every couple of weeks, ask: "What worked, what didn't, what should we
> change?" Update the schema together. The agent proposes; you decide.

## Architecture

```
BrainKu/
├── schema.md             # this file (conventions, structure, tags)
├── index.md              # catalog of every page with one-line summaries
├── log.md                # chronological action log (append-only)
├── AGENTS.md              # operational playbook for LLM agents
├── GUIDE.md              # install + usage for every audience
├── README.md             # human-facing overview
├── raw/                  # Layer 1: IMMUTABLE source material
│   ├── articles/         # web articles, clippings
│   ├── papers/           # PDFs, arxiv papers
│   ├── transcripts/      # meeting notes, interviews, podcasts
│   └── assets/           # images, diagrams referenced by sources
├── entities/             # Layer 2: one page per notable entity
├── concepts/             # Layer 2: one page per concept or topic
├── comparisons/          # Layer 2: side-by-side analyses
├── queries/              # Layer 2: filed query results worth keeping
│   ├── research/         # long-form research outputs
│   └── daily/            # daily notes, journal entries
└── _meta/                # meta-documents (topic-map, drafts, internal)
```

**Three layers:**

1. **Raw sources** — immutable. The agent reads but NEVER modifies.
2. **The wiki** — agent-owned markdown. Created, updated, cross-referenced.
3. **The schema** — this file + `AGENTS.md`. Co-evolved by human + agent.

## Conventions

- **File names:** lowercase, hyphens, no spaces. Example: `transformer-architecture.md`.
- **Frontmatter:** every wiki page starts with YAML frontmatter (see below).
- **Wikilinks:** use `[[page-name]]` to link between pages. Minimum 2 outbound links per page.
- **Updates:** when updating a page, always bump the `updated:` date in frontmatter.
- **Index:** every new or updated page must be added to `index.md` under the correct section.
- **Log:** every action must be appended to `log.md` with the action prefix.
- **Provenance markers:** on pages that synthesize 3+ sources, append `^[raw/articles/source-file.md]`
  to paragraphs whose claims trace to a specific source. Optional on single-source pages.
- **Raw is sacred:** never edit a file under `raw/`. If a source needs correcting, write
  a wiki page that supersedes it.
- **Raw body byte-exact:** the body of a raw file (everything after the second `---`) must
  be byte-exact with the original source. Compute sha256 of the body and store in frontmatter.
  See `AGENTS.md` for the full ingest procedure.

## Frontmatter (wiki pages)

```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | summary
tags: [from taxonomy below]
sources: [raw/articles/source-name.md]
# Optional quality signals:
confidence: high | medium | low        # how well-supported the claims are
contested: true                         # set when the page has unresolved contradictions
contradictions: [other-page-slug]       # pages this one conflicts with
---
```

`confidence` and `contested` are optional but recommended for opinion-heavy or fast-moving
topics. Lint surfaces `contested: true` and `confidence: low` pages for review.

### Frontmatter (raw/ files)

```yaml
---
source_url: https://example.com/article
ingested: YYYY-MM-DD
sha256: <hex digest of the raw content below the frontmatter>
---
```

The `sha256` is computed over the body only (everything after the closing `---`), not the
frontmatter itself. On re-ingest, recompute and compare — skip if identical, flag drift if not.

## Page Thresholds

- **Create a page** when an entity/concept appears in **2+ sources** OR is **central to one source**
- **Add to existing page** when a source mentions something already covered
- **DON'T create a page** for passing mentions, minor details, or things outside the domain
- **Split a page** when it exceeds ~200 lines — break into sub-topics with cross-links
- **Archive a page** when its content is fully superseded — move to `_archive/`, remove from index

## Entity Pages

One page per notable entity (person, org, product, model, project). Include:
- Overview / what it is
- Key facts and dates
- Relationships to other entities (use `[[wikilinks]]`)
- Source references

## Concept Pages

One page per concept or topic. Include:
- Definition / explanation
- Current state of knowledge
- Open questions or debates
- Related concepts (use `[[wikilinks]]`)

## Comparison Pages

Side-by-side analyses. Include:
- What is being compared and why
- Dimensions of comparison (table format preferred)
- Verdict or synthesis
- Sources

## Query Pages

Filed query results worth keeping. Include:
- Original question
- Synthesis / answer
- Pages drawn from (with `[[wikilinks]]`)
- Confidence / caveats

## Tag Taxonomy

Start with a small, focused set. Add new tags here BEFORE using them.

- **Domain buckets:** `tech`, `science`, `business`, `personal`, `project`, `reference`
- **Type markers:** `entity`, `concept`, `comparison`, `query`, `summary`, `daily`
- **Quality:** `tutorial`, `deep-dive`, `opinion`, `controversy`, `prediction`, `list`, `snippet`
- **Status:** `draft`, `wip`, `done`, `archived`, `stale`

**Rule:** every tag on a page must appear in this taxonomy. If a new tag is needed,
add it here first, then use it. This prevents tag sprawl.

## Page Types

BrainKu has seven wiki page types. Each has a distinct role and shape. Pick the
type that best matches the page's role, not what's easy.

- **entity** — a notable entity (person, org, product, model, project).
  Facts, dates, relationships, sources.
- **concept** — an abstract topic or idea. Definition, current state, open
  questions, related concepts.
- **comparison** — a side-by-side analysis of 2+ entities or concepts.
  Dimensions, verdicts, sources.
- **query** — a filed query result worth keeping. Question, synthesis,
  pages drawn from, caveats.
- **summary** — a per-source summary page (one per raw file). The first thing
  the agent creates during an ingest. Acts as the source's entry point in the
  wiki and the anchor for downstream entity/concept updates.
- **overview** — a higher-level page that frames a domain. "My health
  overview", "AI research overview". Synthesizes summaries and entity pages
  into a navigable landing page for a sub-area.
- **synthesis** — a novel cross-cutting analysis that goes beyond what any
  individual source says. "Why every 2024 model converged on MoE",
  "Cross-reading Karpathy + Chollet on AGI timelines". The most valuable
  page type — these are the insights you couldn't derive from any one source.

## Update Policy

When new information conflicts with existing content:

1. Check the dates — newer sources generally supersede older ones.
2. If genuinely contradictory, note both positions with dates and sources.
3. Mark the contradiction in frontmatter: `contradictions: [page-name]`.
4. Flag for user review in the lint report.

## Log Rotation

When `log.md` exceeds 500 entries, rename it `log-YYYY.md` and start fresh. The agent
should check log size during lint.

## Workflow preferences

BrainKu's ingest/query/lint workflows are templates, not laws. After using the
wiki for a while, you'll develop preferences — for example:

- **Source granularity** — do you prefer one summary per file, or one per chapter
  / section? "Personally I prefer to ingest sources one at a time and stay involved"
  vs "I batch-ingest many sources at once with less supervision" are both fine.
- **Discussion depth** — should the agent pause after each ingest to discuss
  takeaways, or just write the pages and let you review?
- **Stale threshold** — 90 days is the default. Your domain may move faster
  (finance, news) or slower (philosophy) and warrant different thresholds.
- **Tag density** — do you want every page to have 3-5 tags, or are 1-2 enough?

**Document your preferences in this file.** Future agents (and future you) will
read the schema before doing anything; a clear "this is how I work" section saves
endless re-derivation. Bump the `updated:` date at the top when you change this.

## Index Scaling

- When any section of `index.md` exceeds 50 entries, split into sub-sections by first letter
  or sub-domain.
- When `index.md` exceeds 200 entries total, create `_meta/topic-map.md` that groups pages
  by theme for faster navigation.

---

**Last updated:** 2026-06-20
**Version:** 1.0
**Domain scope:** general (personal knowledge base — no specialization yet)
