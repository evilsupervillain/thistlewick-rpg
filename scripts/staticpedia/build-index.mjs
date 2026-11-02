#!/usr/bin/env node
/*
 * Static-Pedia search index generator. Part of Static-Pedia:
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
 * Static-Pedia search index generator. Zero dependencies (Node.js 18+).
 *
 * Walks a wiki directory, reads every .md file and writes pages.json:
 *   [{ "path": "People/John_Doe", "title": "John Doe", "text": "plain text..." }]
 *
 * Usage:
 *   node tools/build-index.mjs [wikiRoot] [options]
 *
 * Options:
 *   --out FILE        Output file (default: <wikiRoot>/pages.json)
 *   --max-chars N     Truncate each page's text to N characters (default 20000, 0 = no limit)
 *   --exclude GLOB    Skip matching paths (repeatable). Also read from "searchExclude" in staticpedia.json
 *   --check           Don't write; exit with status 1 if pages.json is missing or out of date
 *   --quiet           Print nothing on success
 *
 * Always skipped: files and folders whose names start with "." or "_" (so
 * _Sidebar.md and _Footer.md are not indexed), and node_modules.
 */
import { readdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';

function parseArgs(argv) {
  const opts = { root: '.', out: null, maxChars: 20000, exclude: [], check: false, quiet: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--out') opts.out = argv[++i];
    else if (a === '--max-chars') opts.maxChars = Number(argv[++i]);
    else if (a === '--exclude') opts.exclude.push(argv[++i]);
    else if (a === '--check') opts.check = true;
    else if (a === '--quiet') opts.quiet = true;
    else if (a === '-h' || a === '--help') {
      console.log('Usage: node tools/build-index.mjs [wikiRoot] [--out FILE] [--max-chars N] [--exclude GLOB]... [--check] [--quiet]');
      process.exit(0);
    } else if (a.startsWith('--')) { console.error(`Unknown option: ${a}`); process.exit(2); }
    else opts.root = a;
  }
  if (!Number.isFinite(opts.maxChars) || opts.maxChars < 0) { console.error('--max-chars must be a number >= 0'); process.exit(2); }
  return opts;
}

/* "Drafts/**" -> regex. "*" stays inside one folder, "**" crosses folders. */
function globToRegExp(glob) {
  let re = '';
  for (let i = 0; i < glob.length; i++) {
    const c = glob[i];
    if (c === '*' && glob[i + 1] === '*') { re += '.*'; i++; if (glob[i + 1] === '/') i++; }
    else if (c === '*') re += '[^/]*';
    else if (c === '?') re += '[^/]';
    else re += c.replace(/[.+^${}()|[\]\\]/g, '\\$&');
  }
  return new RegExp(`^${re}$`);
}

async function walk(dir, rel = '') {
  const out = [];
  const entries = await readdir(dir, { withFileTypes: true });
  for (const e of entries) {
    if (e.name.startsWith('.') || e.name.startsWith('_') || e.name === 'node_modules') continue;
    const relPath = rel ? `${rel}/${e.name}` : e.name;
    if (e.isDirectory()) out.push(...await walk(path.join(dir, e.name), relPath));
    else if (e.isFile() && /\.md$/i.test(e.name)) out.push(relPath);
  }
  return out;
}

function splitFrontMatter(src) {
  src = src.replace(/^﻿/, '');
  const m = src.match(/^---[ \t]*\r?\n([\s\S]*?)\r?\n(?:---|\.\.\.)[ \t]*(?:\r?\n|$)/);
  if (!m) return { meta: {}, body: src };
  const meta = {};
  for (const line of m[1].split(/\r?\n/)) {
    const kv = line.match(/^([A-Za-z0-9_-]+)[ \t]*:[ \t]*(.*?)[ \t]*$/);
    if (kv) meta[kv[1].toLowerCase()] = kv[2].replace(/^(['"])(.*)\1$/, '$2');
  }
  return { meta, body: src.slice(m[0].length) };
}

// Named entities decoded in the text. Keep this list in sync with build_index.py.
const ENTITIES = {
  amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", nbsp: ' ', shy: '', copy: '©', reg: '®', trade: '™',
  mdash: '—', ndash: '–', hellip: '…', middot: '·', bull: '•', deg: '°', times: '×', divide: '÷',
  laquo: '«', raquo: '»', lsquo: '‘', rsquo: '’', ldquo: '“', rdquo: '”',
  larr: '←', rarr: '→', uarr: '↑', darr: '↓', harr: '↔', euro: '€', pound: '£', yen: '¥', cent: '¢', sect: '§', para: '¶'
};
function decodeEntities(s) {
  return s.replace(/&(#x[0-9a-f]+|#\d+|[a-z]+);/gi, (all, e) => {
    if (e[0] === '#') {
      const n = e[1].toLowerCase() === 'x' ? parseInt(e.slice(2), 16) : parseInt(e.slice(1), 10);
      try { return String.fromCodePoint(n); } catch { return all; }
    }
    return ENTITIES[e.toLowerCase()] ?? all;
  });
}

/* Inline Markdown -> plain text (links keep their text, emphasis markers go). */
function inlineToText(s) {
  // Code spans first, so their content survives tag stripping untouched.
  const code = [];
  s = s.replace(/(?<![\\`])(`+)([\s\S]*?[^`])\1(?!`)/g, (_, ticks, c) => `\u0000${code.push(c.trim()) - 1}\u0000`);
  s = s
    .replace(/!\[([^\]]*)\]\([^)]*\)/g, '$1')
    .replace(/\[\[([^\]|]+)\|([^\]]+)\]\]/g, '$2')
    .replace(/\[\[([^\]]+)\]\]/g, (_, t) => t.replace(/_/g, ' '))
    .replace(/\[\^[^\]]+\]/g, '')
    .replace(/\[([^\]]*)\]\([^)]*\)/g, '$1')
    .replace(/\[([^\]]*)\]\[[^\]]*\]/g, '$1')
    .replace(/<(https?:[^>]+|[^@>\s]+@[^>\s]+)>/g, '$1')
    .replace(/<\/?[a-zA-Z][^>]*>/g, ' ')
    .replace(/(?<!\\)(\*{1,3}|~~)(?=\S)([\s\S]*?[^\s\\])\1/g, '$2')
    .replace(/(^|[^\w\\])(_{1,3})(?=\S)([\s\S]*?[^\s\\])\2(?!\w)/g, '$1$3')
    .replace(/\\$/, '')
    .replace(/\\([!-/:-@[-`{-~])/g, '$1');
  return s.replace(/\u0000(\d+)\u0000/g, (_, n) => code[n]);
}

function markdownToText(body) {
  const lines = body.replace(/\r\n?/g, '\n').replace(/<!--[\s\S]*?-->/g, '')
    .replace(/(?<!`)<(script|style)\b[\s\S]*?<\/\1\s*>/gi, '').split('\n');
  const out = [];
  let fence = null;
  for (let line of lines) {
    const f = line.match(/^ {0,3}(`{3,}|~{3,})/);
    if (f) {
      if (!fence) fence = f[1];
      else if (f[1][0] === fence[0] && f[1].length >= fence.length) fence = null;
      continue;
    }
    if (fence) { out.push(line); continue; }
    if (/^ {0,3}\[[^\]]+\]:\s*\S+/.test(line) && !/^ {0,3}\[\^/.test(line)) continue; // link reference definition
    if (/^ {0,3}([-*_])([ \t]*\1){2,}[ \t]*$/.test(line)) continue;                  // horizontal rule
    if (/^ {0,3}(=+|-+)[ \t]*$/.test(line)) continue;                                // setext underline
    if (/^ {0,3}\|?[ \t]*:?-+:?[ \t]*(\|[ \t]*:?-+:?[ \t]*)*\|?[ \t]*$/.test(line) && line.includes('|')) continue; // table delimiter
    line = line
      .replace(/^ {0,3}#{1,6}[ \t]+/, '').replace(/[ \t]+#+[ \t]*$/, '')
      .replace(/^(\s*>)+\s?/, '')
      .replace(/^\s*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*$/i, '')
      .replace(/^\s*([-+*]|\d{1,9}[.)])\s+(\[[ xX]\]\s+)?/, '')
      .replace(/^ {0,3}\[\^[^\]]+\]:\s*/, '');
    out.push(inlineToText(line).replace(/(^|[^\\])\|/g, '$1 ').replace(/\\\|/g, '|'));
  }
  return decodeEntities(out.join('\n')).replace(/[ \t]+/g, ' ').replace(/\s*\n\s*/g, '\n').replace(/\n{2,}/g, '\n').trim()
    .replace(/\n/g, ' ');
}

function titleFor(meta, body, pagePath, siteName) {
  if (meta.title) return meta.title;
  const lines = body.split(/\r?\n/);
  let fence = null;
  for (let i = 0; i < lines.length; i++) {
    const l = lines[i];
    const f = l.match(/^ {0,3}(`{3,}|~{3,})/);
    if (f) { fence = fence ? (f[1][0] === fence[0] ? null : fence) : f[1]; continue; }
    if (fence) continue;
    const m = l.match(/^ {0,3}#[ \t]+(.+?)(?:[ \t]+#+)?[ \t]*$/);
    if (m) return inlineToText(m[1]).trim();
    if (l.trim() && /^ {0,3}=+[ \t]*$/.test(lines[i + 1] || '')) return inlineToText(l.trim());
  }
  if (pagePath === 'Index') return siteName || 'Static-Pedia';
  const leaf = pagePath.split('/').pop();
  const parent = pagePath.split('/').slice(-2, -1)[0];
  return (leaf === 'Index' && parent ? parent : leaf).replace(/_/g, ' ');
}

async function readConfig(root) {
  try { return JSON.parse(await readFile(path.join(root, 'staticpedia.json'), 'utf8')); } catch { return {}; }
}

async function main() {
  const opts = parseArgs(process.argv.slice(2));
  const root = path.resolve(opts.root);
  const outFile = path.resolve(opts.out || path.join(root, 'pages.json'));
  const config = await readConfig(root);
  const patterns = [...(Array.isArray(config.searchExclude) ? config.searchExclude : []), ...opts.exclude].map(globToRegExp);

  const files = (await walk(root)).filter(f => !patterns.some(re => re.test(f))).sort();
  const pages = [];
  for (const file of files) {
    const src = await readFile(path.join(root, file), 'utf8');
    const { meta, body } = splitFrontMatter(src);
    if (/^(true|yes)$/i.test(meta.noindex || '')) continue; // front matter "noindex: true" opts a page out
    const pagePath = file.replace(/\.md$/i, '');
    let text = markdownToText(body);
    if (opts.maxChars && text.length > opts.maxChars) text = text.slice(0, opts.maxChars).replace(/\s\S*$/, '') + ' …';
    pages.push({ path: pagePath, title: titleFor(meta, body, pagePath, config.siteName), text });
  }
  const json = JSON.stringify(pages, null, 2) + '\n';

  if (opts.check) {
    let existing = null;
    try { existing = await readFile(outFile, 'utf8'); } catch { /* missing */ }
    if (existing !== json) {
      console.error(`${path.relative(process.cwd(), outFile) || outFile} is out of date. Run: node tools/build-index.mjs ${opts.root}`);
      process.exit(1);
    }
    if (!opts.quiet) console.log(`${path.relative(process.cwd(), outFile)} is up to date (${pages.length} pages).`);
    return;
  }
  await writeFile(outFile, json);
  if (!opts.quiet) console.log(`Wrote ${pages.length} pages to ${path.relative(process.cwd(), outFile) || outFile}`);
}

main().catch(err => { console.error(err); process.exit(1); });
