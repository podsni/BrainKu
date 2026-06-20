# BrainKu — Full Guide

> Install + usage for every audience: Reader, Curator, Agent, Contributor.
> New to BrainKu? Start with [README.md](README.md) and [schema.md](schema.md).

## Table of Contents

- [What is BrainKu?](#what-is-brainku)
- [Quick start (5 minutes)](#quick-start-5-minutes)
- [For Readers](#for-readers)
- [For Curators](#for-curators)
- [For Agents](#for-agents)
- [For Contributors](#for-contributors)
- [Troubleshooting](#troubleshooting)

---

## What is BrainKu?

BrainKu is a personal, compounding knowledge base built on the
[Karpathy LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

It is a directory of interlinked markdown files that an LLM agent incrementally maintains.
Unlike RAG — which rediscovers knowledge from scratch on every question — the wiki
**compiles** knowledge once. Cross-references, contradictions, and synthesis are all
already there when you ask a question.

**Three layers:**

1. **`raw/`** — immutable source material (articles, papers, transcripts).
2. **Wiki pages** — agent-owned markdown (entities, concepts, comparisons, queries).
3. **Schema + playbook** — `schema.md` + `AGENTS.md`. Co-evolved by human + agent.

---

## Quick start (5 minutes)

```bash
# 1. Clone (or create) the repo
cd /root/dev
ls BrainKu/   # already exists if you followed the setup

# 2. Open in Obsidian (optional, recommended for reading)
# File → Open vault → /root/dev/BrainKu
# The vault works out of the box — wikilinks, graph view, dataview all work.

# 3. Drop your first source into raw/articles/
# (download a webpage, save a PDF, paste a transcript)

# 4. Tell your agent to ingest it
# "Ingest /root/dev/BrainKu/raw/articles/<file>.md"
# The agent will: compute sha256, discuss takeaways, update/create wiki pages,
# add to index.md and log.md, cross-reference ≥2 other pages.

# 5. Ask questions
# "What have I learned about X?"
# The agent searches the wiki, synthesizes, cites with [[wikilinks]].

# 6. Periodically lint
# "Lint BrainKu"
# The agent health-checks: orphan pages, broken links, stale content, contradictions.
```

That's it. The wiki grows and compounds from here.

---

## For Readers

A reader is anyone who wants to **browse and learn from** the wiki without contributing.

### Option 1: Obsidian (recommended)

1. Install [Obsidian](https://obsidian.md/).
2. Open as a vault: File → Open vault → select `/root/dev/BrainKu`.
3. Done. Wikilinks, graph view, backlinks, tag pages all work.

Optional but recommended:

- **Dataview plugin** — for queries like
  `TABLE tags, updated FROM "concepts" SORT updated DESC`.
- **Tag wrangler** — for tag-based navigation.
- **Mind map** — for visualizing connections.

### Option 2: Plain markdown editor

Any editor works: VS Code, Vim, Helix, Sublime, etc. Wikilinks won't be clickable
but the markdown is readable as-is.

### Option 3: Static site (MkDocs Material)

See [Publishing as a static site](#publishing-as-a-static-site) below.

---

## For Curators

A curator is the human who **adds sources, asks questions, and shapes the wiki**.

### Adding a source

Three ways:

1. **URL** — paste the link to your agent. The agent will fetch, save to `raw/articles/`,
   compute sha256, and write the frontmatter.
2. **File** — drop a file into `raw/articles/`, `raw/papers/`, or `raw/transcripts/`.
   Then tell your agent: "Ingest /path/to/file.md".
3. **Paste** — paste the text directly to your agent. The agent will save it to the
   appropriate `raw/` subdir.

### Naming conventions

- **Raw files:** lowercase, hyphens, descriptive. Example: `karpathy-llm-wiki-2026.md`.
- **Wiki pages:** lowercase, hyphens, descriptive. Example: `transformer-architecture.md`.
- **Tags:** short, single-word or hyphenated. Example: `deep-dive`, `opinion`, `daily`.

### Asking questions

Just ask. The agent will:

1. Read `index.md` to find relevant pages.
2. Search the wiki for key terms if the wiki is large.
3. Synthesize an answer with citations.

If the answer is substantial (a comparison, deep dive, novel synthesis), the agent will
file it as a new page in `queries/` or `comparisons/`. You can also ask explicitly:
"File this as a comparison page."

### Mass updates

If you want to rewrite or reorganize a large chunk of the wiki, do it in one session
with the agent. The agent can update 10+ pages in one pass if needed — but confirm the
scope first.

---

## For Agents

If you are an LLM agent (Hermes, Codex, Claude Code, OpenCode) maintaining BrainKu:

1. **First thing: orient.**
   ```
   read_file BrainKu/schema.md
   read_file BrainKu/index.md
   read_file BrainKu/log.md offset=last 30
   ```

2. **For an ingest**, see `AGENTS.md` § Operations → 1. Ingest.

3. **For a query**, see `AGENTS.md` § Operations → 2. Query.

4. **For a lint**, see `AGENTS.md` § Operations → 3. Lint.

5. **Read `AGENTS.md` Pitfalls** before doing anything. The pitfalls section is dense
   because they're all real bugs we've hit.

6. **When in doubt, ask the user.** Mass-updates, schema changes, and tag additions
   should always be confirmed.

---

## For Contributors

Contributors add to the wiki without owning the curation loop. Common cases:

- **Filing a query** — "File this as a daily note" → creates `queries/daily/<date>.md`.
- **Adding a tag** — propose the tag in `schema.md` first, then use it.
- **Splitting a page** — when a page exceeds 200 lines, ask the agent to split.
- **Cross-referencing** — every page should link to ≥2 others. If you find an orphan,
  add links from related pages.
- **Logging actions** — every action gets a `log.md` entry. Format:
  `## [YYYY-MM-DD] action | subject`.

---

## Obsidian Headless (servers and headless machines)

On machines without a display, you can sync the BrainKu vault via Obsidian Sync
without the desktop GUI — useful when the agent writes to the wiki on a server
while Obsidian desktop reads it on another device.

```bash
# Requires Node.js 22+
npm install -g obsidian-headless

# Login (requires Obsidian account with Sync subscription)
ob login --email <email> --password '<password>'

# Create a remote vault
ob sync-create-remote --name "BrainKu"

# Connect the wiki directory
cd /root/dev/BrainKu
ob sync-setup --vault "<vault-id>"

# Initial sync
ob sync

# Continuous sync (foreground — use systemd for background)
ob sync --continuous
```

Continuous background sync via systemd:

```ini
# ~/.config/systemd/user/brainku-sync.service
[Unit]
Description=BrainKu Obsidian Sync
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/path/to/ob sync --continuous
WorkingDirectory=/root/dev/BrainKu
Restart=on-failure
RestartSec=10

[Install]
WantedBy=default.target
```

```bash
systemctl --user daemon-reload
systemctl --user enable --now brainku-sync
sudo loginctl enable-linger $USER
```

Note: this requires an active Obsidian Sync subscription. For local-only reading,
just open the directory as a vault in Obsidian desktop — no sync needed.

---

## Deployment pitfalls

These bit during the BrainKu bootstrap and are documented for the next person who
rebuilds the repo from scratch.

### `gh repo create` crashes on Unicode in non-UTF-8 locales

`gh` invokes Python internally. On systems with `LANG=C` / `POSIX` / `Latin-1`,
any non-ASCII character in `--description` (em-dash `—`, smart quote `"`, CJK)
raises `UnicodeEncodeError: 'latin-1' codec can't encode character ...` and
**the repo is not created**.

**Fix:**

```bash
# Either export UTF-8 first:
export LANG=C.UTF-8 LC_ALL=C.UTF-8
gh repo create <repo> --public \
  --description "Plain ASCII or UTF-8 description" --source=. --push

# Or write the description in plain ASCII only.
```

BrainKu's repo description uses no em-dashes for this reason.

### Older `git` doesn't accept `-b <branch>` on `init`

The `-b` flag was added in git 2.28 (July 2020). Minimal containers and older
LTS distros may ship git < 2.28.

**Fix (fallback that works on every git):**

```bash
git init
git symbolic-ref HEAD refs/heads/main
```

BrainKu's bootstrap uses this fallback explicitly.

---

## Troubleshooting

### "The agent created a duplicate page"

**Cause:** skipped orientation, didn't read `index.md` before creating.
**Fix:** read `index.md` and `search_files` for the entity/concept first. Merge duplicates
manually or via the agent.

### "The agent overwrote information"

**Cause:** silently overwrote contradicting content without flagging.
**Fix:** follow the Update Policy in `schema.md` — note both claims, mark in frontmatter
(`contradictions: [other-page]`), flag for user review.

### "The wiki has orphan pages"

**Cause:** page created without cross-references.
**Fix:** every page must link to ≥2 other pages. If you find an orphan, ask the agent
to add cross-references from related pages.

### "Wikilinks don't render on the published site"

**Cause:** default MkDocs doesn't handle `[[wikilinks]]` natively.
**Fix:** install a custom wikilinks plugin (see `mkdocs-interactive-features.md` in the
Hermes `llm-wiki` skill) or use the explicit `nav:` block in `mkdocs.yml` instead.

### "My raw file's sha256 doesn't match"

**Cause:** the body was edited or re-serialized (a trailing newline, a "fixed" typo).
**Fix:** never hand-edit a `raw/` file. Re-ingest the source if needed. If the source has
genuinely changed, update the frontmatter `sha256` and bump `ingested`.

### "log.md is huge"

**Cause:** log not rotated.
**Fix:** when `log.md` exceeds 500 entries, rename it `log-YYYY.md` and start fresh.

### "index.md is unwieldy"

**Cause:** too many pages in one section.
**Fix:** when any section exceeds 50 entries, split into sub-sections. When `index.md`
exceeds 200 entries total, create `_meta/topic-map.md`.

---

## See also

- [`README.md`](README.md) — overview and quick start
- [`schema.md`](schema.md) — conventions, structure, tag taxonomy
- [`index.md`](index.md) — the catalog
- [`log.md`](log.md) — chronological action log
- [`AGENTS.md`](AGENTS.md) — agent playbook
- [Karpathy LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — the pattern source
- Hermes `llm-wiki` skill — operational playbook + MkDocs templates
