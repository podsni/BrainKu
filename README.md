# BrainKu

> **A personal, compounding knowledge base — built on the
> [Karpathy LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) pattern.**
>
> Compiled markdown over RAG. Cross-references already there when you ask.

> **Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase.**
> You run Obsidian on one side of the screen, the LLM agent on the other. The LLM
> makes edits; you browse the results in real time — following links, checking the
> graph view, reading updated pages. This loop is what makes the wiki feel alive.

---

## Table of contents

- [What is BrainKu?](#what-is-brainku)
- [Why this works](#why-this-works)
- [Division of labor](#division-of-labor)
- [What you can use it for](#what-you-can-use-it-for)
- [Optional and modular](#optional-and-modular)
- [Architecture: three layers](#architecture-three-layers)
- [Layout](#layout)
- [The seven page types](#the-seven-page-types)
- [How it works: three workflows](#how-it-works-three-workflows)
- [The linter: 15 categories](#the-linter-15-categories)
- [Quick start](#quick-start)
- [The schema is the key configuration file](#the-schema-is-the-key-configuration-file)
- [Obsidian integration](#obsidian-integration)
- [Optional tools](#optional-tools)
- [Companion docs](#companion-docs)
- [Customizing BrainKu](#customizing-brainku)
- [Requirements](#requirements)
- [Pattern source](#pattern-source)
- [License](#license)

---

## What is BrainKu?

BrainKu is **not** a RAG system. It is a directory of interlinked markdown files
that an LLM agent incrementally maintains. The wiki **compiles** knowledge once and
keeps it current — cross-references, contradictions, and synthesis are all already
there when you ask a question.

RAG rediscovers knowledge from scratch on every query. The embedding search finds
the right chunks, the LLM re-derives the synthesis, the user gets an answer that
isn't quite the same as last time. The wiki inverts that: every insight is written
down, cross-linked, and updated. When you ask a question, the LLM doesn't rediscover
— it reads what you and previous agents already wrote.

The result: knowledge compounds. A wiki with 200 pages answers a question in
seconds by reading 5 already-linked pages, not by re-deriving 5 pages of synthesis
from raw sources. A wiki with 1000 pages is faster than a fresh RAG query on
10GB of source material, because the compilation has already happened.

You and the LLM co-evolve the schema, the tag taxonomy, the page-type conventions
over time. BrainKu is a starting point — the project is what you make of it.

## Why this works

- **No embeddings, no vector DB, no re-derivation.** Cross-references are already
  there. The LLM doesn't compute similarity; it follows `[[wikilinks]]` you and
  previous agents wrote.
- **Scales to ~hundreds of pages** with just an `index.md` and the human-agent
  loop. Thousands of pages with a local search engine like [qmd](https://github.com/tobi/qmd).
- **Auditable.** Every claim has a source. Every page has provenance. You can
  trace any statement back to the `raw/` file it came from.
- **Compounding.** A wiki with 200 pages answers new questions in 30 seconds
  because the synthesis has already happened. A wiki with 1000 pages is faster
  than a fresh RAG query on 10GB of source material.
- **Obsidian-compatible.** Works as an Obsidian vault out of the box — graph view,
  wikilinks, Dataview queries, daily notes, all native.
- **The maintenance problem disappears.** The tedious part of a wiki — updating
  cross-references, keeping summaries current, noting when new data contradicts
  old claims — is the LLM's job. Humans abandon wikis because maintenance grows
  faster than value. LLMs don't get bored and can touch 15 files in one pass.

## Division of labor

- **You** — source, curate, ask questions, set the direction. Drop articles into
  `raw/`, ask "what do I know about X", review the LLM's edits in Obsidian.
- **Agent** — summarize, cross-reference, file, lint, keep the wiki consistent.
  Reads `schema.md` and `AGENTS.md` at the start of every session. Writes wiki
  pages, updates `index.md` and `log.md`, never modifies `raw/`.
- **Obsidian** (or any markdown editor) — your IDE for reading and editing.
  The graph view shows the shape of the wiki; backlinks show what's connected.
  Dataview plugin runs queries over page frontmatter.
- **The wiki** — the persistent, compounding artifact. A directory of markdown
  files in git, with version history and a public URL if you want one.

## What you can use it for

The pattern applies to a lot of different contexts. A few from the
[source gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f):

- **Personal** — tracking your own goals, health, psychology, self-improvement.
  Filing journal entries, articles, podcast notes, and building up a structured
  picture of yourself over time.
- **Research** — going deep on a topic over weeks or months. Reading papers,
  articles, reports, and incrementally building a comprehensive wiki with an
  evolving thesis.
- **Reading a book** — filing each chapter as you go, building pages for
  characters, themes, plot threads, and how they connect. By the end you have
  a rich companion wiki. Think Tolkien Gateway but personalized.
- **Business / team** — an internal wiki maintained by LLMs, fed by Slack threads,
  meeting transcripts, project documents, customer calls. Possibly with humans
  in the loop reviewing updates.
- **Competitive analysis, due diligence, trip planning, course notes, hobby
  deep-dives** — anything where you're accumulating knowledge over time and want
  it organized rather than scattered.

## Optional and modular

**Everything mentioned above is optional and modular.** Pick what's useful, ignore
what isn't:

- Your sources might be text-only, so you don't need image handling.
- Your wiki might be small enough that `index.md` is all you need, no search
  engine required.
- You might not care about slide decks and just want markdown pages.
- You might never use Obsidian and just read the wiki in `cat` and `grep`.

BrainKu ships as a starting point; customize it to your domain. The schema is
co-evolved, the page types are extensible, the linter is configurable. There is
no "right way" — there is only what works for you.

---

## Architecture: three layers

```
Layer 3 ─── schema.md + AGENTS.md    (the key configuration file; co-evolved)
   │
Layer 2 ─── entities/, concepts/, comparisons/, queries/,
            overviews/, syntheses/, summaries/   (the wiki; agent-owned)
   │
Layer 1 ─── raw/                       (immutable source material)
```

**Layer 1 — Raw sources.** The agent reads but **never modifies**. A dropped-in
web article, a PDF, a meeting transcript, a podcast note. Each has YAML
frontmatter with `source_url`, `ingested` date, and `sha256` of the body.
The body is byte-exact with the source.

**Layer 2 — The wiki.** Agent-owned markdown. Created, updated, cross-referenced.
Seven page types: entity, concept, comparison, query, summary, synthesis, overview.
Frontmatter powers filtering and the linter. Wikilinks make the graph.

**Layer 3 — The schema.** `schema.md` (conventions, frontmatter, tag taxonomy,
page thresholds) + `AGENTS.md` (operational playbook: orientation, ingest,
query, lint, pitfalls). Both are co-evolved by you and the agent over time.

## Layout

```
BrainKu/
├── README.md           this file
├── schema.md           conventions, structure, tag taxonomy, page thresholds
├── index.md            content catalog (one entry per page)
├── log.md              chronological action log (append-only)
├── AGENTS.md           operational playbook for LLM agents
├── GUIDE.md            full install + usage for every audience
├── CHANGELOG.md        release history
├── LICENSE             MIT
├── .gitignore          editor/OS, Obsidian local state, venv, build cache
│
├── raw/                LAYER 1: immutable source material
│   ├── articles/       web articles, clippings
│   ├── papers/         PDFs, arxiv papers
│   ├── transcripts/    meeting notes, interviews, podcasts
│   └── assets/         images, diagrams referenced by sources
│
├── entities/           LAYER 2: one page per notable entity (people, orgs, products, models, projects)
├── concepts/           one page per concept or topic
├── comparisons/        side-by-side analyses
├── queries/            filed query results
│   ├── research/       long-form research outputs
│   └── daily/          daily notes, journal entries
├── overviews/          higher-level framing pages for sub-areas
├── syntheses/          novel cross-cutting analyses (most valuable)
├── summaries/          per-source summary pages (one per raw file)
│
├── _meta/              meta-documents (topic-map, drafts, internal)
└── scripts/
    ├── lint.py         the wiki linter (15 categories, stdlib-only)
    └── README.md       linter usage
```

The directories under `Layer 2` are recommendations, not laws. The agent
co-evolves the layout with you. If your domain favors `people/`, `projects/`,
`papers/` instead of `entities/` + `concepts/`, change the schema and update
the linter.

## The seven page types

BrainKu has seven page types. Each has a distinct role and shape. Pick the type
that best matches the page's role, not what's easy.

- **entity** — a notable entity (person, org, product, model, project). Facts,
  dates, relationships, sources.
- **concept** — an abstract topic or idea. Definition, current state, open
  questions, related concepts.
- **comparison** — a side-by-side analysis of 2+ entities or concepts.
  Dimensions, verdicts, sources.
- **query** — a filed query result worth keeping. Question, synthesis, pages
  drawn from, caveats.
- **summary** — a per-source summary page (one per raw file). The first thing
  the agent creates during an ingest. Acts as the source's entry point in the
  wiki and the anchor for downstream entity/concept updates.
- **overview** — a higher-level page that frames a sub-area. "AI research
  overview", "My health overview". Synthesizes summaries and entity pages
  into a navigable landing page.
- **synthesis** — a novel cross-cutting analysis that goes beyond what any
  individual source says. "Why every 2024 model converged on MoE". The most
  valuable page type — these are the insights you couldn't derive from any
  one source.

The frontmatter `type:` field must be one of these seven values (plus `schema`
and `meta` for system pages). The linter enforces this.

## How it works: three workflows

The agent follows three workflows. All are documented in detail in `AGENTS.md`.

### 1. Ingest

When you provide a source (URL, file path, pasted text, or a file already in
`raw/`):

1. **Capture the raw source** to `raw/articles/`, `raw/papers/`, or
   `raw/transcripts/`. Compute sha256 of the body. Write frontmatter.
2. **Read the source** and identify entities, concepts, claims.
3. **Check what already exists** in `index.md` (and search the wiki for 100+
   pages). This is the difference between a growing wiki and duplicates.
4. **Write a per-source summary page** first — the source's entry point in
   the wiki.
5. **Update or create entity/concept/comparison pages** with new info.
   Cross-reference to ≥2 other pages. Tags from the schema taxonomy only.
6. **Update navigation**: add to `index.md` (with date + source count
   metadata), append to `log.md`.

A single source can trigger updates across 5–15 wiki pages. This is the
compounding effect — it is normal and desired.

### 2. Query

When you ask a question about BrainKu's domain:

1. Read `index.md` to find relevant pages (or run `qmd search` for 100+ pages).
2. Read the relevant pages.
3. Synthesize an answer. Cite wiki pages with `[[wikilinks]]`.
4. File the answer back if it's a substantial comparison, deep dive, or novel
   synthesis. Don't file trivial lookups.
5. Update `log.md` with the query.

Output formats beyond markdown: comparison tables, Marp slide decks, matplotlib
charts, drawio/Mermaid canvases. Pick the format that matches the question.

### 3. Lint

Run `python3 scripts/lint.py .` to health-check the wiki. The linter covers 15
categories (see below). For 100+ pages, run weekly. For small wikis, monthly is
fine. The linter is stdlib-only Python 3.10+ — no install.

```bash
python3 scripts/lint.py .                # standard
python3 scripts/lint.py . --strict       # exit 1 on any issue (for CI)
python3 scripts/lint.py . --no-log       # don't append lint entry to log.md
```

## The linter: 15 categories

The linter surfaces issues grouped by severity. See `scripts/README.md` for
full details on each.

| Sev | Category | What it catches |
|-----|----------|-----------------|
| HIGH | `source_drift` | `raw/` files whose sha256 doesn't match frontmatter |
| HIGH | `broken_wikilinks` | `[[links]]` pointing to non-existent pages |
| MEDIUM | `mentioned_no_page` | concepts referenced 2+ times but with no page |
| MEDIUM | `missing_xrefs` | pages with <2 outbound `[[wikilinks]]` |
| MEDIUM | `not_in_index` | wiki pages not listed in `index.md` |
| MEDIUM | `orphan_pages` | pages with no inbound links |
| MEDIUM | `fm_missing` | pages missing required frontmatter fields |
| MEDIUM | `fm_invalid_type` | pages with invalid `type` field |
| MEDIUM | `bad_tags` | tags not in the schema taxonomy |
| LOW | `contested` | pages flagged `contested: true` |
| LOW | `low_confidence` | pages with `confidence: low` or `medium` |
| LOW | `single_source_no_conf` | single-source pages missing `confidence:` field |
| LOW | `stale_pages` | pages not updated in >90 days |
| INFO | `big_pages` | pages over 200 lines (consider splitting) |
| INFO | `log_needs_rotation` | `log.md` exceeded 500 entries |

The linter also outputs a "Suggested next actions" section: pages to create,
sources to look for, cross-references to add, contradictions to reconcile.

---

## Quick start

```bash
# 1. Clone or create the repo (you already have it at /root/dev/BrainKu)
cd /root/dev/BrainKu

# 2. (Optional) Open in Obsidian as a vault
#    File > Open vault > /root/dev/BrainKu
#    Wikilinks, graph view, Dataview all work out of the box.

# 3. Drop your first source into raw/articles/
curl -fsSL "https://example.com/article" -o raw/articles/my-first-source.md
# or: copy a PDF, paste a transcript, drop a file in.

# 4. Tell your agent to ingest it
#    "Ingest /root/dev/BrainKu/raw/articles/my-first-source.md"
#    The agent will: compute sha256, discuss takeaways, write a per-source
#    summary page, update or create entity/concept pages, add to index.md
#    and log.md, cross-reference ≥2 other pages.

# 5. Ask questions
#    "What have I learned about X?"
#    The agent reads the wiki, synthesizes, cites with [[wikilinks]].

# 6. Periodically lint
python3 scripts/lint.py .
# ALL CLEAN means the wiki is structurally healthy.
```

**First sources to consider (personal knowledge base starter pack):**

1. A book or paper you just read → `raw/articles/` or `raw/papers/`
2. A recent article worth remembering → `raw/articles/`
3. A meeting transcript or interview → `raw/transcripts/`
4. A research question you're working on → `queries/research/`

## The schema is the key configuration file

`schema.md` is what makes the LLM a disciplined wiki maintainer rather than a
generic chatbot. It tells the agent how the wiki is structured, what the
conventions are, and what workflows to follow when ingesting sources,
answering questions, or maintaining the wiki.

**You and the LLM co-evolve this over time as you figure out what works for
your domain.** Every couple of weeks, ask: "What worked, what didn't, what
should we change?" Update the schema together. The agent proposes; you decide.

`schema.md` covers:

- **Domain** — what the wiki is for, what's in scope, what's optional
- **Architecture** — the three layers, with the file tree
- **Conventions** — file names, frontmatter, wikilinks, update dates, index, log,
  provenance markers
- **Frontmatter spec** — wiki pages (title/created/updated/type/tags/sources +
  confidence/contested/contradictions) and raw files (source_url/ingested/sha256)
- **Page thresholds** — when to create, add, or split a page
- **Page types** — the seven types and what each looks like
- **Tag taxonomy** — domain buckets, type markers, quality, status
- **Update policy** — how to handle contradictions
- **Log rotation** — at 500 entries
- **Index scaling** — split at 50/section, topic-map at 200 total
- **Workflow preferences** — your own knobs (source granularity, discussion
  depth, stale threshold, tag density)

A clear schema saves endless re-derivation. Bump the `updated:` date at the top
when you change it.

## Obsidian integration

BrainKu works as an Obsidian vault out of the box. The wikilinks, frontmatter,
and directory structure are all Obsidian-native.

**For the desktop editor:**

- **Set the attachment folder to `raw/assets/`** (Settings → Files and links).
- **Enable Wikilinks** in settings (default on).
- **Install Dataview plugin** for queries like
  `TABLE tags, updated FROM "concepts" SORT updated DESC`.
- **Install Obsidian Web Clipper** (browser extension) to drop new sources
  directly into `raw/articles/`.
- **Use the graph view** to see the shape of the wiki — what's connected to
  what, which pages are hubs, which are orphans.
- **Install Marp plugin** if you want query answers as slide decks.

**For headless servers (no display):**

Sync the vault via Obsidian Sync without the desktop GUI. Requires Node.js 22+
and an Obsidian Sync subscription. See `GUIDE.md § Obsidian Headless` for full
setup, including a systemd unit for continuous background sync.

**The Obsidian Web Clipper + image-download workflow:**

1. Clip an article in the browser.
2. In Obsidian, hit the hotkey for "Download attachments for current file"
   (e.g. Ctrl+Shift+D, after binding it in settings).
3. All images get downloaded to `raw/assets/`.
4. Tell the agent to ingest the file. The LLM can read the text first, then
   view some/all of the referenced images separately to gain additional context.

## Optional tools

These aren't required but are useful at scale.

- **[qmd](https://github.com/tobi/qmd)** — a local search engine for markdown
  files with hybrid BM25 + vector search + LLM re-ranking, all on-device.
  Both a CLI (`qmd search "transformer architecture"`) and an MCP server
  (so the agent can use it as a native tool). When the wiki grows past
  ~hundreds of pages, install qmd and use it in the Query workflow step 1.
  Doesn't want to install qmd? The LLM can help you vibe-code a one-off
  search script as the need arises.
- **Obsidian Web Clipper** — browser extension that converts web articles to
  clean markdown. Drop new sources directly into `raw/articles/`.
- **Marp** — markdown-based slide deck format. Obsidian has a plugin for it.
  Useful when a query answer should be a presentation.
- **Dataview** — Obsidian plugin that runs queries over page frontmatter.
  Dynamic tables and lists. The LLM doesn't run Dataview, but you can.
- **obsidian-headless** — sync the vault on a headless server via Obsidian
  Sync. See `GUIDE.md § Obsidian Headless` for setup.

## Companion docs

BrainKu ships with five companion files. Read in this order:

1. **[`schema.md`](schema.md)** — conventions, structure, tag taxonomy, page
   thresholds, page types, workflow preferences. **Read first** at the start
   of every agent session.
2. **[`AGENTS.md`](AGENTS.md)** — operational playbook for LLM agents.
   Orientation, Ingest/Query/Lint workflows, pitfalls, Obsidian integration,
   qmd, Tips and tricks, why this works, historical context (Memex 1945).
3. **[`GUIDE.md`](GUIDE.md)** — full install + usage for Reader, Curator,
   Agent, Contributor. Obsidian Headless, Deployment pitfalls, Troubleshooting.
4. **[`CHANGELOG.md`](CHANGELOG.md)** — release history. Currently at 0.3.0.
5. **[`scripts/README.md`](scripts/README.md)** — linter usage.

## Customizing BrainKu

BrainKu is a starting point. Customize it to your domain.

- **Specialize the domain** — edit `schema.md` to lock the scope. "BrainKu is
  for AI research", "BrainKu is for tracking my health", "BrainKu is for book
  notes". Update the schema's Domain section to make this explicit.
- **Specialize the tag taxonomy** — replace the general tags in `schema.md §
  Tag Taxonomy` with domain-specific ones. The rule is: add new tags to the
  schema first, then use them.
- **Add or remove page types** — if `synthesis` and `overview` don't fit your
  use case, remove them from `ALLOWED_TYPES` in `scripts/lint.py`. If you
  need a new type (`quote`, `bookmark`, `event`), add it everywhere.
- **Add sub-directories** — e.g. `entities/people/`, `entities/organizations/`,
  `concepts/tech/`, `concepts/science/`. Update the linter's
  `EXEMPT_FROM_WIKI_CHECKS` set if you need new meta-files.
- **Tune the linter** — change `STALE_DAYS`, `PAGE_LINE_LIMIT`,
  `LOG_ENTRY_LIMIT`, `MIN_OUTBOUND_WIKILINKS` at the top of `scripts/lint.py`.
- **Add scripts** — `scripts/` is a stdlib-only home for any custom tooling
  (deploy, generate stats, etc.).

The principle: **the schema is a contract.** Whatever you put in the schema
governs the linter and the agent. Keep them in sync.

## Requirements

- **Python 3.10+** — for `scripts/lint.py` (uses `list[str]`, `dict | None`
  type hints). No external dependencies.
- **Git** — for version control. The wiki is a git repo.
- **An LLM agent** — Hermes, Codex, Claude Code, OpenCode, or any other that
  reads `AGENTS.md` at the start of a session.
- **Obsidian** (optional, recommended) — for reading and editing. The wiki
  works without it, but Obsidian's graph view and Dataview queries are the
  canonical way to navigate.
- **Bun** (optional) — only if you install qmd.

## Pattern source

BrainKu is a direct implementation of
[Andrej Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
(75 lines). The historical context is Vannevar Bush's
[Memex (1945)](https://www.theatlantic.com/magazine/archive/1945/07/as-we-may-think/303881/)
— a personal, curated knowledge store with associative trails between
documents. Bush's vision was closer to this pattern than to what the web
became: private, actively curated, with the connections between documents as
valuable as the documents themselves. The part he couldn't solve was who does
the maintenance. The LLM handles that.

## License

MIT — do whatever, just don't blame me when the wiki is empty.
