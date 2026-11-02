---
name: staticpedia
description: Add a Static-Pedia wiki to a project and write its content. Static-Pedia is a single self-contained index.html that renders a folder of Markdown files as a Wikipedia-style site on any static host (GitHub Pages, S3, nginx, python -m http.server), at the domain root or under a sub-path. Use when asked to create project documentation, a docs site, a knowledge base, a wiki or an encyclopedia made of Markdown that must work without a server or a build step.
license: MIT (see the notice below)
---

<!--
Static-Pedia skill: https://github.com/evilsupervillain/staticpedia

SPDX-License-Identifier: MIT
Copyright (c) 2026 evilsupervillain

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
-->

# Static-Pedia: install it, configure it, write the wiki

Source repository: `https://github.com/evilsupervillain/staticpedia` (branch `master`).
Raw files: `https://raw.githubusercontent.com/evilsupervillain/staticpedia/master/<path>`.

## Mental model

- **The whole program is `index.html`.** It is copied verbatim into a folder (the *wiki root*). Every `.md` file under that folder becomes a page.
- The page is chosen by the query string: no `p` → `Index.md`; `?p=Guides/Setup` → `Guides/Setup.md`; `?p=Guides/` → `Guides/Index.md`. The `.md` is optional in `p`.
- In the browser, `index.html` fetches the `.md`, renders Markdown to HTML, sanitizes it, and rewrites links and media relative to the page's folder. **There is no build step.** The only generated file is the optional search index `pages.json`.
- Customization never requires editing `index.html`. Use `staticpedia.json` (config), `style.css` (CSS variables), `_Sidebar.md` and `_Footer.md`.

## Hard rules

1. **Do not modify `index.html`.** Copy it byte-for-byte, including the MIT license notice at its top. The tools carry the same notice; keeping these notices is the only condition of the license, and it needs no other attribution in the project. All customization goes in the special files below. The only exception is the user explicitly asking for a new feature; then say so and keep the changes minimal.
2. **Home page is `Index.md`** with a capital `I`. `index.md` does not work on case-sensitive hosts such as GitHub Pages and Linux servers, which are the common case.
3. **Use relative links only** (rules in [Links](#links-the-rules-that-matter-most)). Never write host-absolute URLs to your own pages and never hard-code the deploy path, such as `/my-repo/`.
4. **GitHub Pages needs an empty `.nojekyll`** at the published root. Without it, `_Sidebar.md` and `_Footer.md` are not published and `.md` files with front matter get converted to HTML (every such page then 404s).
5. **Never invent facts.** When documenting a project, derive every statement from its code, configs, README, issues or the user. Mark genuine unknowns with a `> [!NOTE]` callout instead of guessing.
6. **Verify before reporting done:** run the link checker and the index generator, and serve the wiki once (see [Verify](#step-7-verify)).
7. **No third-party assets.** No CDN scripts, no web fonts from Google Fonts or similar, no hot-linked images unless the user wants them. The wiki must work offline.

## Step 1: Decide the layout

Pick the wiki root:

| Situation | Wiki root | Notes |
|---|---|---|
| Project repo, docs alongside code (most common) | `docs/` | GitHub Pages → Settings → Pages → Deploy from branch → `/docs`. |
| Dedicated wiki/encyclopedia repo | repo root | Add `README.md` etc. to `searchExclude`. |
| Site already has an `index.html` at the root | a sub-folder, e.g. `wiki/` | Never overwrite an existing site's `index.html`. |
| Existing folder of Markdown docs | that folder | Keep files; add `index.html` + `Index.md`; existing relative `.md` links keep working. |

Put helper scripts **outside** the wiki root when it is a sub-folder (for example `scripts/staticpedia/`). When the wiki root is the repo root, use `tools/`.

If the hosting target or wiki root is unclear and cannot be inferred from the repo (an existing `docs/`, a Pages workflow, a `gh-pages` branch), ask the user once. Otherwise default to `docs/` + GitHub Pages.

## Step 2: Fetch the files

```sh
WIKI=docs                       # wiki root (use . for repo root)
TOOLS=scripts/staticpedia       # helper scripts (use tools if WIKI=.)
SP=https://raw.githubusercontent.com/evilsupervillain/staticpedia/master
mkdir -p "$WIKI" "$TOOLS"
curl -fsSL "$SP/index.html"            -o "$WIKI/index.html"
curl -fsSL "$SP/tools/build-index.mjs" -o "$TOOLS/build-index.mjs"   # pages.json generator (Node 18+)
curl -fsSL "$SP/tools/check-links.mjs" -o "$TOOLS/check-links.mjs"   # link/anchor checker (Node 18+)
# optional, for machines without Node:
curl -fsSL "$SP/tools/build_index.py"  -o "$TOOLS/build_index.py"
touch "$WIKI/.nojekyll"
```

If raw downloads fail (network policy, private mirror), use `git clone --depth 1 https://github.com/evilsupervillain/staticpedia /tmp/staticpedia` and copy the same files. For reproducible installs, record the commit (`git ls-remote https://github.com/evilsupervillain/staticpedia master`) in the commit message. To upgrade later, replace `index.html` only.

Sanity check: `head -c 15 "$WIKI/index.html"` prints `<!doctype html>` and `grep -c 'name="generator" content="Static-Pedia"' "$WIKI/index.html"` prints `1`. A failed download often saves an HTML error page instead.

## Step 3: Special files (all at the wiki root)

| File | Required | Purpose |
|---|---|---|
| `index.html` | yes | The program. |
| `Index.md` | yes | Home page. |
| `.nojekyll` | GitHub Pages only | Empty file; disables Jekyll. |
| `staticpedia.json` | recommended | Site name, logo, defaults. |
| `_Sidebar.md` | recommended | Left navigation on every page. Links in it resolve from the wiki root. |
| `_Footer.md` | optional | Footer on every page. Links resolve from the wiki root. |
| `style.css` | optional | Loaded after built-in styles; override CSS variables here. |
| `pages.json` | optional (generated) | Enables the search box, `?special=AllPages`, `?special=Random`. |

### `staticpedia.json`

Every key is optional. Unknown keys are ignored. Paths are relative to the wiki root.

```json
{
  "siteName": "Acme Docs",
  "tagline": "Everything about Acme",
  "logo": "images/logo.svg",
  "favicon": "images/logo.svg",
  "lang": "en",
  "defaultTheme": "system",
  "defaults": { "fontSize": "medium", "width": "narrow", "toc": true, "sidebar": true },
  "tocMinHeadings": 3,
  "showSourceLink": true,
  "showLastModified": true,
  "iframeHosts": [],
  "stylesheets": [],
  "themeStylesheets": {},
  "footerText": "Powered by Static-Pedia.",
  "searchExclude": ["README.md"]
}
```

| Key | Values / default |
|---|---|
| `siteName` | header text and tab-title suffix; default `"Static-Pedia"` |
| `tagline` | small text under the name; default none |
| `logo`, `favicon` | image paths; default built-in icon / no logo |
| `lang` | `<html lang>`; default `"en"` |
| `defaultTheme` | `"system"` \| `"light"` \| `"dark"` |
| `defaults` | `fontSize`: small\|medium\|large\|xlarge; `width`: narrow\|wide; `toc`, `sidebar`: booleans |
| `titleSeparator` | default `" — "` |
| `tocMinHeadings` | headings needed for a contents box; default `3` |
| `showSourceLink`, `showLastModified` | booleans, default `true` |
| `iframeHosts` | exact hostnames allowed in `<iframe src="https://…">`; default `[]` (all iframes removed) |
| `stylesheets` | extra CSS files loaded after `style.css` |
| `themeStylesheets` | `{"light": "…css", "dark": "…css"}` loaded for the active theme only |
| `footerText` | footer when there is no `_Footer.md`; `""` hides it |
| `searchExclude` | globs skipped by the index generator (`*` within a folder, `**` across folders) |

### `_Sidebar.md` template

Short lists under `###` headings, which render as small section labels. Lists render without bullets.

```markdown
- [Main page](Index)
- [All pages](?special=AllPages)

### Getting started
- [Installation](Installation)
- [Quick start](Quick_Start)

### Reference
- [Configuration](Reference/Configuration)
- [CLI](Reference/CLI)
```

Keep it under about 25 links. Link a folder's `Index.md` rather than listing every page in large sections. `?special=AllPages` and `?special=Random` only work when `pages.json` exists.

### `_Footer.md` template

```markdown
© 2026 Acme Corp. Documentation licensed under CC BY 4.0. · [Source](https://github.com/acme/acme)
```

### `Index.md` template

```markdown
---
title: Acme Docs
---

# Acme

**Acme** is <one-sentence description derived from the project>. <Second sentence: who it is for.>

## Start here

| Page | What it covers |
|---|---|
| [Installation](Installation) | … |
| [Configuration](Reference/Configuration) | … |
```

A front matter `title` equal to `siteName` makes the home tab show just the site name.

## Step 4: Write the pages

### Files and names

- One topic per file. **Use `Underscores_Not_Spaces.md`**: underscores display as spaces in derived titles. Be consistent with case (`Title_Case.md` recommended).
- Group with folders. Give a folder an `Index.md` as its overview; `[x](Folder/)` and `?p=Folder/` open it.
- Names starting with `_` or `.` are excluded from search (use them for drafts). `_Sidebar.md` and `_Footer.md` are reserved.
- Front matter, optional and only simple `key: value` lines: `title:` (tab title and search title; used as the heading if there is no `# H1`), `toc: false` (no contents box), `noindex: true` (excluded from `pages.json`).

### Page anatomy (encyclopedia style)

```markdown
# Exact Page Title

<p class="hatnote">For the command-line tool, see <a href="CLI">CLI</a>.</p>

<table class="infobox">
<caption>Widget Service</caption>
<tr><td colspan="2" class="infobox-image"><img src="images/widget.svg" alt="Widget logo" width="160"><span class="infobox-caption">Logo</span></td></tr>
<tr><th>Language</th><td>Go</td></tr>
<tr><th>Repository</th><td><code>services/widget</code></td></tr>
<tr><th colspan="2" class="infobox-header">Dependencies</th></tr>
<tr><td colspan="2">PostgreSQL, Redis</td></tr>
</table>

**Widget Service** is … (lead paragraph: what it is, why it matters, in 2–4 sentences).

## Overview
## Usage
### Example
## Internals
## See also
- [Related page](Related_Page)

## Notes
[^1]: Footnote text, referenced in prose as text[^1].
```

- Exactly **one `# H1` per page**, first. Sections use `##`, sub-sections `###`. Three or more headings produce a Wikipedia-style Contents box before the first `##`.
- The lead paragraph comes before the first `##`. Bold the subject's name in its first mention.
- Infobox, hatnote and figure markup is raw HTML: **a raw HTML block ends at the first blank line**, so keep an HTML table without blank lines inside it. To use Markdown inside an HTML element, put blank lines after the opening tag and before the closing tag.

### Markdown supported

CommonMark plus: tables (`|`, alignment `:--:`, escape a literal pipe as `\|`, including inside code in tables), task lists `- [ ]` / `- [x]`, `~~strike~~`, bare-URL autolinks, footnotes `[^id]`, reference links, `[[wiki links]]`, and callouts:

```markdown
> [!NOTE]
> Also TIP, IMPORTANT, WARNING, CAUTION.
```

Fenced code with a language (```` ```js ````) gets class `language-js`. There is no syntax highlighting.

### Links: the rules that matter most

| Written in `Guides/Setup.md` | Resolves to |
|---|---|
| `[x](Install)` or `[x](Install.md)` | `Guides/Install.md` (relative to the **page's folder**) |
| `[x](../Index.md)` | `Index.md` |
| `[x](/Reference/CLI)` | `Reference/CLI.md` (leading `/` = **wiki root**, not the host root) |
| `[x](Reference/)` | `Guides/Reference/Index.md` |
| `[x](Install#first-run)` | `Guides/Install.md`, at heading "First run" |
| `[x](#options)` | heading on the same page |
| `[[Reference/CLI]]`, `[[Reference/CLI\|the CLI]]`, `[[CLI#Global flags]]` | from the **wiki root**, spaces → `_`, `#Heading text` is slugified for you |
| `[x](files/spec.pdf)`, `![](images/a.png)` | files relative to the page's folder |
| `[x](https://…)` | external; gets an arrow marker and `rel="noopener"` |
| `[x](?search=term)`, `[x](?special=AllPages)` | built-in pages |

- A link is a **page** if it ends in `.md`, ends in `/`, or its last segment has no extension containing a letter (`Version_2.0` is a page; `notes.txt` is a file). When in doubt, add `.md`.
- `_Sidebar.md` and `_Footer.md` links always resolve from the wiki root.
- **Anchor slugs:** the heading's rendered text, lowercased, with every character that is not a letter, digit, space, `_` or `-` deleted, then spaces → `-`. Examples: `## Early life` → `#early-life`; ``## Why `.nojekyll` matters`` → `#why-nojekyll-matters`; `## Works (1990–2001)` → `#works-19902001`. Duplicates get `-1`, `-2`.
- Images and media in a sub-folder next to the page are fine: in `People/Ada.md`, `![](images/ada.png)` loads `People/images/ada.png`.

### Media and layout snippets

```html
<figure class="thumb right">
  <img src="images/diagram.svg" alt="Describe the image" width="220">
  <figcaption>Caption text.</figcaption>
</figure>

<video controls width="480" poster="media/poster.jpg"><source src="media/clip.mp4" type="video/mp4"></video>
<audio controls src="media/sound.wav"></audio>
```

Content classes styled by default: `infobox` (with `infobox-header`, `infobox-image`, `infobox-caption`, `infobox-title`), `thumb`, `right`, `left`, `center` (on `figure`), `float-right`, `float-left`, `center`, `clear`, `hatnote`, `notice`, `plain` (borderless table), `new` (red link), `no-toc` (exclude contained headings from the contents box). Markdown tables automatically get bordered "wikitable" styling and scroll sideways on phones.

For diagrams, write an `.svg` file and embed it with `<img src="images/x.svg">`. **Inline `<svg>` is removed.** Give SVGs their own background so they read in dark mode.

### What the sanitizer removes (don't rely on these)

`<script>`, `<style>`, `<iframe>` (unless the host is in `iframeHosts`), `<object>`, `<embed>`, `<form>` and form controls (except disabled checkboxes), inline `<svg>` and `<math>`, `<link>`, `<meta>`, `<base>`, all `on*` attributes, the `name` attribute, `javascript:`, `vbscript:` and non-image `data:` URLs, and `id`s starting with `sp-` (reserved). Unknown tags are unwrapped (their text stays). Allowed: normal text and table elements, `div`, `span`, `details`/`summary`, `figure`, `img`, `picture`, `video`, `audio`, `source`, `track`, `kbd`, `mark`, `abbr`, `sub`, `sup`, `dl`, plus attributes `id`, `class`, `title`, `style`, `lang`, `dir`, `role`, `aria-*`, `data-*`, `width`, `height`, `colspan`, `rowspan`.

## Step 5: Styling (only if the user wants a custom look)

Create `style.css` at the wiki root and **override variables** rather than rewriting rules. Theme selectors live on `<html>`:

```css
/* both themes */
:root, :root[data-theme="dark"] { --sp-accent: #0b7a75; --sp-focus: #0b7a75; }
/* one theme (needed to beat the built-in dark values) */
:root[data-theme="light"] { --sp-link: #0b7a75; }
:root[data-theme="dark"]  { --sp-link: #5fd3cc; }
```

Variables: colors `--sp-bg`, `--sp-surface`, `--sp-surface-2`, `--sp-surface-3`, `--sp-text`, `--sp-text-muted`, `--sp-border`, `--sp-border-light`, `--sp-link`, `--sp-link-visited`, `--sp-link-hover`, `--sp-link-new`, `--sp-accent`, `--sp-accent-text`, `--sp-focus`, `--sp-header-bg`, `--sp-sidebar-bg`, `--sp-input-bg`, `--sp-code-bg`, `--sp-code-text`, `--sp-mark-bg`, `--sp-note`, `--sp-tip`, `--sp-important`, `--sp-warning`, `--sp-caution`, `--sp-shadow`. Type and layout: `--sp-font-body`, `--sp-font-heading`, `--sp-font-mono`, `--sp-line-height`, `--sp-page-max`, `--sp-sidebar-width`, `--sp-content-max`, `--sp-radius`.

Settings attributes on `<html>`: `data-theme` (`light`|`dark`, resolved), `data-theme-pref`, `data-font-size`, `data-width`, `data-toc`, `data-sidebar` (`on`|`off`). Interface classes start with `sp-` (`.sp-header`, `.sp-sidebar`, `.sp-main`, `.sp-content`, `.sp-footer`). Scope custom content classes under `.sp-content`. Fonts must be self-hosted (`@font-face` with a `url()` inside the wiki). Check both themes after any color change.

## Step 6: Search index

```sh
node "$TOOLS/build-index.mjs" "$WIKI"          # writes $WIKI/pages.json
node "$TOOLS/build-index.mjs" "$WIKI" --check  # exit 1 if pages.json is stale (for CI)
# no Node: python3 "$TOOLS/build_index.py" "$WIKI"   (same output)
```

Options: `--exclude GLOB` (repeatable), `--max-chars N` (default 20000 per page), `--out FILE`, `--quiet`. It also reads `searchExclude` from `staticpedia.json`. Commit `pages.json`, and **regenerate it after every content change.**

Optional GitHub Action (`.github/workflows/search-index.yml`) that keeps it fresh:

```yaml
name: Update search index
on:
  push:
    branches: [main]
    paths: ['docs/**.md', 'docs/staticpedia.json']
  workflow_dispatch:
permissions:
  contents: write
jobs:
  index:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20 }
      - run: node scripts/staticpedia/build-index.mjs docs
      - run: |
          if ! git diff --quiet -- docs/pages.json; then
            git config user.name "github-actions[bot]"
            git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
            git add docs/pages.json && git commit -m "Update search index" && git push
          fi
```

Adjust the branch and paths to the project. Only add a workflow if the user wants CI changes.

## Step 7: Verify

Run all of these and fix every problem before reporting:

```sh
node "$TOOLS/check-links.mjs" "$WIKI"          # broken pages, files, images, #anchors; exit 1 on problems
node "$TOOLS/build-index.mjs" "$WIKI" --check  # pages.json up to date
cd "$WIKI" && python3 -m http.server 8000      # then open http://localhost:8000/
```

`check-links.mjs` resolves links exactly as `index.html` does and suggests near-miss anchors. It skips external links, code, `<a class="new">` red links, and lines containing `<!-- check-links: ignore -->` (use that only for deliberate examples of broken links).

If a headless browser is available (for example Playwright), also load every page and confirm it renders with no JavaScript errors:

```js
// node verify.mjs  (with a server running on :8000 in the wiki root)
import { chromium } from 'playwright';
import { readFileSync } from 'node:fs';
const pages = JSON.parse(readFileSync('docs/pages.json', 'utf8'));
const browser = await chromium.launch(), page = await browser.newPage();
const errors = []; page.on('pageerror', e => errors.push(e.message));
for (const { path } of pages) {
  await page.goto(`http://localhost:8000/?p=${path}`);
  await page.waitForFunction(() => !document.querySelector('#sp-main').hasAttribute('aria-busy') && document.querySelector('#sp-content h1'));
  const h1 = await page.locator('#sp-content h1').first().innerText();
  if (h1 === 'Page not found' || h1 === 'Could not load page') errors.push(`${path}: ${h1}`);
}
console.log(errors.length ? errors.join('\n') : `All ${pages.length} pages render.`);
await browser.close();
```

To prove sub-path hosting works (as on GitHub Pages project sites), serve the **parent** folder and open `http://localhost:8000/<wiki-folder>/`.

## Writing a project's documentation

1. **Survey first:** README, package manifests, entry points, CLI definitions, config schemas, public APIs, existing `docs/`, examples and tests. List the concepts, components and tasks a reader needs.
2. **Plan the page tree** before writing, and put it in `_Sidebar.md`. A typical set: `Index.md` (what and why, quick links), `Installation.md`, `Quick_Start.md`, `Guides/…` (task-oriented how-tos), `Concepts/…` or `Architecture.md` (how it works), `Reference/…` (CLI, config, API: exhaustive, table-heavy), `FAQ.md`, `Glossary.md`.
3. **Write each page** from the sources: a lead paragraph, then `##` sections, then runnable examples in fenced code with a language, and tables for options (name | type | default | description). Cross-link generously with relative links; link each glossary term the first time it appears on a page.
4. Use an **infobox** for entities with stable facts (a service, package, module, person, place). Use **callouts** for warnings and prerequisites. Use **figures** for diagrams.
5. Keep reference pages in sync with the code: copy option names, defaults and flags exactly.

## Writing an encyclopedia (worlds, organizations, knowledge bases)

- **Folders are categories:** `People/`, `Places/`, `Events/`, `Organizations/`. Each has an `Index.md` with a table of its articles (name | summary | key date).
- **One article per entity,** named by its common name: `People/Ada_Lovelace.md`. Disambiguate with a parenthetical in front matter `title:` (for example `title: Mercury (planet)`) and a `hatnote`.
- **Every article:** an H1, a bold-name lead, an infobox of key facts, `##` sections (History, Description, Relationships…), `## See also`, and `## Notes` with footnotes for sources. Facts in the infobox must match the prose.
- **Use wiki links `[[People/Ada Lovelace]]` between articles.** They resolve from the root, so they read the same on every page. When an article that should exist hasn't been written yet, link it with `<a class="new" href="…">` (red link) and list it for the user. Never leave silent broken links.
- Keep a `Timeline.md` or `Glossary.md` for cross-cutting facts, and re-run the link checker after every batch of articles.

## Pitfalls checklist

- [ ] `Index.md` (capital I) exists at the wiki root
- [ ] `.nojekyll` exists (GitHub Pages)
- [ ] No link starts with the deploy path or the domain; root-relative links start with `/` and mean the wiki root
- [ ] Wiki links are written from the root (`[[Guides/Setup]]`, not `[[Setup]]` from inside `Guides/`)
- [ ] Anchors match slugs (punctuation removed: `#whats-new` for "What's new?")
- [ ] HTML blocks (infoboxes, tables) contain no blank lines unless Markdown inside is intended
- [ ] No inline `<svg>`, `<script>`, `<style>`, `<iframe>` (unless allowed), or `on*=` attributes
- [ ] Images have `alt` text and live inside the wiki root
- [ ] `pages.json` regenerated; `check-links.mjs` exits 0
- [ ] `searchExclude` covers non-wiki Markdown in the wiki root (README.md, CHANGELOG.md, CLAUDE.md…)
- [ ] The site is never opened via `file://`; a local server is used for previews

## Deeper reference

The full human manual lives in the source repository and can be fetched raw when a detail is missing here: `Writing_Pages.md`, `Links_and_Media.md`, `Special_Files.md`, `Configuration.md`, `Theming.md`, `Settings.md`, `Search.md`, `GitHub_Pages.md`, `Installation.md`, `FAQ.md` (for example `curl -fsSL https://raw.githubusercontent.com/evilsupervillain/staticpedia/master/Links_and_Media.md`).

## Report back

When done, tell the user:
- the wiki root and how to preview it (`cd <wiki> && python3 -m http.server 8000`);
- the publishing steps (for example GitHub Pages → Deploy from branch → `/docs`);
- the pages created, as a tree;
- the verification results (link checker, index check, browser check if run);
- any facts you could not confirm, and any red links left for future articles.
