#!/usr/bin/env node
/*
 * Static-Pedia link checker. Part of Static-Pedia:
 * https://github.com/evilsupervillain/staticpedia
 *
 * SPDX-License-Identifier: MIT
 * Copyright (c) 2026 evilsupervillain
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

/*
 * Static-Pedia link checker. Zero dependencies (Node.js 18+).
 *
 * Finds broken page links, wiki links, image/media/file references and
 * #anchors in a wiki, resolving them exactly the way index.html does:
 *   - relative links resolve from the linking page's folder
 *   - a leading "/" and every [[wiki link]] resolve from the wiki root
 *   - "Page", "Page.md" -> Page.md; "Folder/" -> Folder/Index.md
 *   - a name whose extension contains a letter (report.pdf) is a file
 *
 * Usage:
 *   node tools/check-links.mjs [wikiRoot] [--no-anchors] [--quiet]
 *
 * Skipped: external links (any scheme or //), ?query links, code blocks and
 * inline code, <a class="new"> (intentional red links), and any line that
 * contains <!-- check-links: ignore -->.
 * Exit status: 0 when everything resolves, 1 when something is broken.
 */
import { readdir, readFile, stat } from 'node:fs/promises';
import path from 'node:path';

const args = process.argv.slice(2);
const opts = { root: '.', anchors: true, quiet: false };
for (const a of args) {
  if (a === '--no-anchors') opts.anchors = false;
  else if (a === '--quiet') opts.quiet = true;
  else if (a === '-h' || a === '--help') {
    console.log('Usage: node tools/check-links.mjs [wikiRoot] [--no-anchors] [--quiet]');
    process.exit(0);
  } else if (a.startsWith('--')) { console.error(`Unknown option: ${a}`); process.exit(2); }
  else opts.root = a;
}
const ROOT = path.resolve(opts.root);

/* Same slug rule as index.html: lowercase, keep letters/digits/space/_/-, spaces -> "-". */
function slugify(text) {
  const s = String(text).trim().toLowerCase().replace(/[^\p{L}\p{N}\s_-]/gu, '').trim().replace(/\s+/g, '-');
  return s || 'section';
}

/* Rendered text of inline Markdown, close enough for heading slugs. */
function inlineText(s) {
  return s
    .replace(/`+([^`]*)`+/g, '$1')
    .replace(/!\[([^\]]*)\]\([^)]*\)/g, '$1')
    .replace(/\[\[([^\]|]+)\|([^\]]+)\]\]/g, '$2')
    .replace(/\[\[([^\]]+)\]\]/g, '$1')
    .replace(/\[\^[^\]]+\]/g, '')
    .replace(/\[([^\]]*)\]\([^)]*\)/g, '$1')
    .replace(/<[^>]+>/g, '')
    .replace(/(\*{1,3}|_{1,3}|~~)(?=\S)(.*?\S)\1/g, '$2')
    .replace(/\\([!-/:-@[-`{-~])/g, '$1');
}

async function walk(dir, rel = '') {
  const out = [];
  for (const e of await readdir(dir, { withFileTypes: true })) {
    if (e.name.startsWith('.') || e.name === 'node_modules') continue;
    const r = rel ? `${rel}/${e.name}` : e.name;
    if (e.isDirectory()) out.push(...await walk(path.join(dir, e.name), r));
    else if (e.isFile() && /\.md$/i.test(e.name)) out.push(r);
  }
  return out;
}

const existsCache = new Map();
async function exists(rel) {
  if (!existsCache.has(rel)) {
    existsCache.set(rel, stat(path.join(ROOT, rel)).then(s => s.isFile(), () => false));
  }
  return existsCache.get(rel);
}

/* Strip front matter; return lines with fenced code blanked out (line numbers kept). */
function proseLines(src) {
  let body = src.replace(/^﻿/, '');
  const fm = body.match(/^---[ \t]*\r?\n[\s\S]*?\r?\n(?:---|\.\.\.)[ \t]*(?:\r?\n|$)/);
  const fmLines = fm ? fm[0].split('\n').length - 1 : 0;
  if (fm) body = body.slice(fm[0].length);
  const lines = body.split(/\r?\n/);
  let fence = null;
  const out = lines.map(l => {
    const f = l.match(/^ {0,3}(`{3,}|~{3,})/);
    if (f) {
      if (!fence) fence = f[1];
      else if (f[1][0] === fence[0] && f[1].length >= fence.length) fence = null;
      return '';
    }
    if (fence) return '';
    return l;
  });
  return { lines: out, offset: fmLines };
}

/* Anchor ids a page will have once rendered. */
const anchorCache = new Map();
async function anchorsOf(rel) {
  if (anchorCache.has(rel)) return anchorCache.get(rel);
  const ids = new Set();
  try {
    const { lines } = proseLines(await readFile(path.join(ROOT, rel), 'utf8'));
    for (let i = 0; i < lines.length; i++) {
      const l = lines[i];
      let text = null;
      const atx = l.match(/^ {0,3}#{1,6}[ \t]+(.+?)(?:[ \t]+#+)?[ \t]*$/);
      if (atx) text = atx[1];
      else if (l.trim() && /^ {0,3}(=+|-+)[ \t]*$/.test(lines[i + 1] || '') && !/^ {0,3}([-*_])([ \t]*\1){2,}/.test(l) && !/^\s*[-+*]\s/.test(l)) text = l.trim();
      const htmlHeading = l.match(/<h[1-6][^>]*>(.*?)<\/h[1-6]>/i);
      if (htmlHeading && !/\bid\s*=/.test(htmlHeading[0])) text = htmlHeading[1];
      if (text !== null) {
        const base = slugify(inlineText(text));
        let id = base, n = 1;
        while (ids.has(id)) id = `${base}-${n++}`;
        ids.add(id);
      }
      for (const m of l.matchAll(/\bid\s*=\s*["']([^"']+)["']/g)) ids.add(m[1]);
      const fn = l.match(/^ {0,3}\[\^([^\]\s]+)\]:/);
      if (fn) ids.add('fn-' + slugify(fn[1]));
    }
  } catch { /* unreadable: no anchors */ }
  anchorCache.set(rel, ids);
  return ids;
}

const SCHEME = /^[a-z][a-z0-9+.-]*:/i;

/* Resolve a reference to { kind: 'page'|'file', rel, hash } or null (skip). */
function resolve(ref, pageDir, { wiki = false, media = false } = {}) {
  let v = ref.trim().replace(/^<|>$/g, '');
  if (!v || SCHEME.test(v) || v.startsWith('//') || v.startsWith('?')) return null;
  let hash = '';
  const hi = v.indexOf('#');
  if (hi >= 0) { hash = v.slice(hi + 1); v = v.slice(0, hi); }
  const qi = v.indexOf('?');
  if (qi >= 0) v = v.slice(0, qi);
  try { v = decodeURIComponent(v); } catch { /* keep as-is */ }
  try { hash = decodeURIComponent(hash); } catch { /* keep */ }
  if (!v) return { kind: 'self', hash };
  const fromRoot = wiki || v.startsWith('/');
  const joined = path.posix.normalize(path.posix.join(fromRoot ? '' : pageDir, v.replace(/^\/+/, '')) + (v.endsWith('/') ? '/' : ''));
  if (joined.startsWith('../') || joined === '..') return { kind: 'outside', rel: joined, hash };
  const rel = joined === './' || joined === '.' ? '' : joined.replace(/^\.\//, '');
  const leaf = rel.split('/').pop();
  if (media) return { kind: 'file', rel, hash };
  if (wiki) return { kind: 'page', rel: rel.replace(/\s+/g, '_').replace(/\.md$/i, '') + '.md', hash };
  if (leaf === '') return { kind: 'page', rel: rel + 'Index.md', hash };
  if (/\.md$/i.test(leaf)) return { kind: 'page', rel, hash };
  if (/\.[a-z0-9]*[a-z][a-z0-9]*$/i.test(leaf)) return { kind: 'file', rel, hash };
  return { kind: 'page', rel: rel.replace(/\s+/g, '_') + '.md', hash };
}

/* Every link-like reference on a line: [text](dest), [ref]: dest, [[wiki]], href/src/poster/srcset. */
function referencesIn(line) {
  const refs = [];
  let at = 0;
  while ((at = line.indexOf('](', at)) !== -1) {
    const isImage = (() => { // find the matching "[" to see if it is "!["
      let depth = 0;
      for (let k = at; k >= 0; k--) {
        if (line[k] === ']') depth++;
        else if (line[k] === '[' && --depth === 0) return line[k - 1] === '!';
      }
      return false;
    })();
    const m = line.slice(at + 2).match(/^\s*(<[^>]*>|(?:[^\s()\\]|\\.|\((?:[^\s()\\]|\\.)*\))*)/);
    if (m && m[1]) refs.push({ ref: m[1], media: isImage });
    at += 2;
  }
  const def = line.match(/^ {0,3}\[(?!\^)[^\]]+\]:\s*(<[^>]*>|\S+)/);
  if (def) refs.push({ ref: def[1] });
  for (const m of line.matchAll(/\[\[([^\]\n]+)\]\]/g)) {
    const target = m[1].split('|')[0].replace(/\\$/, '').trim();
    refs.push({ ref: target, wiki: !target.startsWith('#'), wikiHash: true });
  }
  for (const m of line.matchAll(/<a\b([^>]*)>/gi)) {
    if (/\bclass\s*=\s*["'][^"']*\bnew\b/i.test(m[1])) continue; // intentional red link
    const h = m[1].match(/\bhref\s*=\s*["']([^"']*)["']/i);
    if (h) refs.push({ ref: h[1] });
  }
  for (const m of line.matchAll(/<(?:img|video|audio|source|track)\b[^>]*?\b(src|poster)\s*=\s*["']([^"']*)["']/gi)) refs.push({ ref: m[2], media: true });
  for (const m of line.matchAll(/<video\b[^>]*?\bposter\s*=\s*["']([^"']*)["']/gi)) refs.push({ ref: m[1], media: true });
  for (const m of line.matchAll(/\bsrcset\s*=\s*["']([^"']*)["']/gi)) {
    for (const part of m[1].split(',')) { const u = part.trim().split(/\s+/)[0]; if (u) refs.push({ ref: u, media: true }); }
  }
  return refs;
}

async function main() {
  const files = (await walk(ROOT)).sort();
  if (!await exists('Index.md')) console.log('warning: no Index.md at the wiki root (it is the home page)');
  let problems = 0, checked = 0;
  for (const file of files) {
    const pageDir = file.includes('/') ? file.slice(0, file.lastIndexOf('/') + 1) : '';
    // _Sidebar.md and _Footer.md are rendered with links relative to the wiki root
    const dir = /^_(Sidebar|Footer)\.md$/.test(file) ? '' : pageDir;
    const { lines, offset } = proseLines(await readFile(path.join(ROOT, file), 'utf8'));
    for (let i = 0; i < lines.length; i++) {
      if (lines[i].includes('<!-- check-links: ignore -->')) continue;
      // Inline code (Markdown or <code>) is literal text, never a link.
      const prose = lines[i].replace(/(`+)[^`]*?\1/g, '').replace(/<code\b[^>]*>[\s\S]*?<\/code>/gi, '');
      for (const r of referencesIn(prose)) {
        let ref = r.ref;
        if (r.wikiHash) { // [[Page#Heading text]] -> slugified anchor
          const hi = ref.indexOf('#');
          if (hi >= 0) ref = ref.slice(0, hi) + '#' + slugify(ref.slice(hi + 1));
        }
        const res = resolve(ref, dir, r);
        if (!res) continue;
        checked++;
        const where = `${file}:${i + 1 + offset}`;
        if (res.kind === 'outside') { problems++; console.log(`${where}: "${r.ref}" points outside the wiki root (${res.rel})`); continue; }
        const target = res.kind === 'self' ? file : res.rel;
        if (res.kind !== 'self' && !await exists(target)) {
          problems++;
          console.log(`${where}: broken ${res.kind === 'file' ? 'file' : 'page'} link "${r.ref}" -> ${target} does not exist`);
          continue;
        }
        if (opts.anchors && res.hash && /\.md$/i.test(target) && !/^_(Sidebar|Footer)\.md$/.test(target)) {
          const ids = await anchorsOf(target);
          if (!ids.has(res.hash)) {
            problems++;
            const near = [...ids].filter(id => id.includes(res.hash.split('-')[0])).slice(0, 3);
            console.log(`${where}: missing anchor "#${res.hash}" in ${target}${near.length ? ` (did you mean ${near.map(n => '#' + n).join(', ')}?)` : ''}`);
          }
        }
      }
    }
  }
  if (problems) { console.log(`\n${problems} problem(s) in ${checked} references across ${files.length} files.`); process.exit(1); }
  if (!opts.quiet) console.log(`All ${checked} references in ${files.length} files resolve.`);
}

main().catch(err => { console.error(err); process.exit(1); });
