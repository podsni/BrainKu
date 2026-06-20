# BrainKu Index

> Content catalog. Every wiki page listed under its type with a one-line summary
> and metadata (date, source count).
> Read this first to find relevant pages for any query.
> Last updated: 2026-06-20 | Total pages: 0

## Entry format

```markdown
- [[page-name]] — one-line summary _(updated YYYY-MM-DD, N sources)_
```

The metadata after the summary is optional but recommended. The linter uses
`sources:` from frontmatter to derive the source count. `updated:` comes from
the page's frontmatter too. When a page has `confidence: low` or
`contested: true`, append a marker:

```markdown
- [[risky-page]] — claim with weak support _(updated 2026-06-20, 1 source) [low conf]_
- [[contradicted-page]] — has open contradiction _(updated 2026-06-20, 3 sources) [contested]_
```

## Entities
<!-- Alphabetical within section. Use page type "entity" for notable people, orgs, products, models, projects. -->
_(none yet — start ingesting sources to populate)_

## Concepts

<!-- Use page type "concept" for abstract topics and ideas. -->
_(none yet)_

## Comparisons

<!-- Use page type "comparison" for side-by-side analyses. -->
_(none yet)_

## Overviews

<!-- Use page type "overview" for higher-level framing pages that synthesize summaries + entities into a navigable landing for a sub-area. -->
_(none yet)_

## Syntheses

<!-- Use page type "synthesis" for novel cross-cutting analyses that go beyond any individual source. These are the most valuable pages. -->
_(none yet)_

## Queries

<!-- Use page type "query" for filed query results worth keeping. -->
_(none yet)_

## Daily Notes

<!-- Use page type "query" (subtype) or no-frontmatter .md for daily journal entries. -->
_(none yet)_

## Sources

<!-- Per-source summary pages (page type "summary") + raw/ file index.
     One entry per ingested source. The summary page is the first thing the agent
     creates during an ingest; it acts as the source's entry point in the wiki. -->
_(none yet)_

---

## Quick Start

BrainKu is empty. To populate it, ingest a source. Drop the raw file into
`raw/articles/`, `raw/papers/`, or `raw/transcripts/`, then ask the agent to
process it. See `AGENTS.md` for the full ingest procedure.

First sources to consider (personal knowledge base starter pack):

1. A book or paper you just read → `raw/articles/` or `raw/papers/`
2. A recent article worth remembering → `raw/articles/`
3. A meeting transcript or interview → `raw/transcripts/`
4. A research question you're working on → `queries/research/`
