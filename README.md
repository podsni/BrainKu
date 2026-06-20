# BrainKu

> A personal, compounding knowledge base — built on the
> [Karpathy LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) pattern.

BrainKu is **not** a RAG system. It is a directory of interlinked markdown files that the
LLM agent incrementally maintains. The wiki **compiles** knowledge once and keeps it current —
cross-references, contradictions, and synthesis are all already there when you ask a question.

> **Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase.**
> In practice the human runs Obsidian on one side of the screen, the LLM agent on the
> other. The LLM makes edits; the human browses the results in real time.

**Division of labor:**

- **You** — source, curate, explore, ask questions
- **Agent** — summarize, cross-references, file, lint, keep the wiki consistent
- **Obsidian** (or any markdown editor) — your IDE for reading and editing the wiki
- **The wiki** — the persistent, compounding artifact

## What you can use it for

The pattern applies to a lot of different contexts. A few from the
[source gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f):

- **Personal** — tracking your own goals, health, psychology, self-improvement. Filing
  journal entries, articles, podcast notes, and building up a structured picture of
  yourself over time.
- **Research** — going deep on a topic over weeks or months. Reading papers, articles,
  reports, and incrementally building a comprehensive wiki with an evolving thesis.
- **Reading a book** — filing each chapter as you go, building pages for characters,
  themes, plot threads, and how they connect. By the end you have a rich companion
  wiki. Think Tolkien Gateway but personalized.
- **Business / team** — an internal wiki maintained by LLMs, fed by Slack threads,
  meeting transcripts, project documents, customer calls. Possibly with humans in the
  loop reviewing updates.
- **Competitive analysis, due diligence, trip planning, course notes, hobby deep-dives**
  — anything where you're accumulating knowledge over time and want it organized rather
  than scattered.

> **Everything mentioned above is optional and modular.** Pick what's useful, ignore
> what isn't. Your sources might be text-only, so you don't need image handling. Your
> wiki might be small enough that the index file is all you need, no search engine
> required. You might not care about slide decks and just want markdown pages. BrainKu
> ships as a starting point; customize it to your domain.

## Layout

```
BrainKu/
├── schema.md          # conventions, structure, tag taxonomy
├── index.md           # catalog of every page
├── log.md             # chronological action log
├── AGENTS.md           # playbook for LLM agents
├── GUIDE.md           # full install + usage for every audience
├── README.md          # this file
├── raw/               # immutable source material
│   ├── articles/
│   ├── papers/
│   ├── transcripts/
│   └── assets/
├── entities/          # entity pages (people, orgs, products, projects)
├── concepts/          # concept pages
├── comparisons/       # side-by-side analyses
├── queries/           # filed query results
│   ├── research/
│   └── daily/         # daily notes, journal entries
└── _meta/             # meta-docs (topic-map, drafts)
```

## Quick Start

1. **Read [`schema.md`](schema.md)** — the conventions, frontmatter, tag taxonomy.
2. **Read [`index.md`](index.md)** — see what's in the wiki.
3. **Drop a source** into `raw/articles/`, `raw/papers/`, or `raw/transcripts/`.
4. **Ask the agent to ingest it** — it will:
   - Compute sha256, write raw frontmatter
   - Discuss key takeaways
   - Update or create entity/concept/comparison pages
   - Cross-reference at least 2 other pages
   - Add to `index.md` and `log.md`
5. **Ask questions** — the agent searches the wiki, synthesizes, cites with `[[wikilinks]]`.
6. **Periodically lint** — ask the agent to health-check the wiki.

See [`GUIDE.md`](GUIDE.md) for full install + usage (Reader / Curator / Agent / Contributor).

## Why this works

- **No embeddings, no vector DB, no re-derivation.** Cross-references are already there.
- **Scales to ~hundreds of pages** with just an `index.md` and the human agent loop.
- **Auditable.** Every claim has a source. Every page has provenance.
- **Obsidian-compatible.** Works as an Obsidian vault out of the box — graph view, wikilinks,
  Dataview queries all work natively.

## Pattern source

This is a direct implementation of
[Andrej Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).
The Hermes `llm-wiki` skill provides the agent-side operational playbook that this repo
follows.

## License

MIT — do whatever, just don't blame me when the wiki is empty.
