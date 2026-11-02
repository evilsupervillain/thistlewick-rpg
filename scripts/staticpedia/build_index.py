#!/usr/bin/env python3
# Static-Pedia search index generator. Part of Static-Pedia:
# https://github.com/evilsupervillain/staticpedia
#
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 evilsupervillain
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Static-Pedia search index generator: Python equivalent of build-index.mjs.

Zero dependencies (Python 3.8+). Walks a wiki directory, reads every .md file
and writes pages.json:  [{"path": "People/John_Doe", "title": "...", "text": "..."}]

Usage:
    python3 tools/build_index.py [wikiRoot] [--out FILE] [--max-chars N]
                                 [--exclude GLOB]... [--check] [--quiet]

Files and folders whose names start with "." or "_" are always skipped, as is
node_modules. "searchExclude" globs in staticpedia.json are honoured. A page
whose front matter says "noindex: true" is left out.
"""
import argparse
import json
import os
import re
import sys


def glob_to_regex(glob):
    out, i = '', 0
    while i < len(glob):
        c = glob[i]
        if glob.startswith('**', i):
            out += '.*'
            i += 2
            if i < len(glob) and glob[i] == '/':
                i += 1
            continue
        out += '[^/]*' if c == '*' else '[^/]' if c == '?' else re.escape(c)
        i += 1
    return re.compile('^' + out + '$')


def walk(root, rel=''):
    found = []
    for name in sorted(os.listdir(os.path.join(root, rel))):
        if name.startswith(('.', '_')) or name == 'node_modules':
            continue
        rel_path = f'{rel}/{name}' if rel else name
        full = os.path.join(root, rel_path)
        if os.path.isdir(full):
            found.extend(walk(root, rel_path))
        elif os.path.isfile(full) and name.lower().endswith('.md'):
            found.append(rel_path)
    return found


FRONT_RE = re.compile(r'^---[ \t]*\r?\n([\s\S]*?)\r?\n(?:---|\.\.\.)[ \t]*(?:\r?\n|$)')


def split_front_matter(src):
    src = src.lstrip('\ufeff')
    m = FRONT_RE.match(src)
    if not m:
        return {}, src
    meta = {}
    for line in m.group(1).splitlines():
        kv = re.match(r'^([A-Za-z0-9_-]+)[ \t]*:[ \t]*(.*?)[ \t]*$', line)
        if kv:
            meta[kv.group(1).lower()] = re.sub(r'^([\'"])(.*)\1$', r'\2', kv.group(2))
    return meta, src[m.end():]


# Named entities decoded in the text. Keep this list in sync with build-index.mjs.
ENTITIES = {
    'amp': '&', 'lt': '<', 'gt': '>', 'quot': '"', 'apos': "'", 'nbsp': ' ', 'shy': '', 'copy': '©', 'reg': '®',
    'trade': '™', 'mdash': '—', 'ndash': '–', 'hellip': '…', 'middot': '·', 'bull': '•', 'deg': '°', 'times': '×',
    'divide': '÷', 'laquo': '«', 'raquo': '»', 'lsquo': '‘', 'rsquo': '’', 'ldquo': '“', 'rdquo': '”',
    'larr': '←', 'rarr': '→', 'uarr': '↑', 'darr': '↓', 'harr': '↔', 'euro': '€', 'pound': '£', 'yen': '¥',
    'cent': '¢', 'sect': '§', 'para': '¶',
}


def decode_entities(s):
    def repl(m):
        e = m.group(1)
        if e[0] == '#':
            try:
                return chr(int(e[2:], 16) if e[1] in 'xX' else int(e[1:]))
            except (ValueError, OverflowError):
                return m.group(0)
        return ENTITIES.get(e.lower(), m.group(0))
    return re.sub(r'&(#[xX][0-9a-fA-F]+|#\d+|[a-zA-Z]+);', repl, s)


def inline_to_text(s):
    # Code spans first, so their content survives tag stripping untouched.
    code = []

    def keep(m):
        code.append(m.group(2).strip())
        return f'\0{len(code) - 1}\0'
    s = re.sub(r'(?<![\\`])(`+)([\s\S]*?[^`])\1(?!`)', keep, s)
    s = re.sub(r'!\[([^\]]*)\]\([^)]*\)', r'\1', s)
    s = re.sub(r'\[\[([^\]|]+)\|([^\]]+)\]\]', r'\2', s)
    s = re.sub(r'\[\[([^\]]+)\]\]', lambda m: m.group(1).replace('_', ' '), s)
    s = re.sub(r'\[\^[^\]]+\]', '', s)
    s = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', s)
    s = re.sub(r'\[([^\]]*)\]\[[^\]]*\]', r'\1', s)
    s = re.sub(r'<(https?:[^>]+|[^@>\s]+@[^>\s]+)>', r'\1', s)
    s = re.sub(r'</?[a-zA-Z][^>]*>', ' ', s)
    s = re.sub(r'(?<!\\)(\*{1,3}|~~)(?=\S)([\s\S]*?[^\s\\])\1', r'\2', s)
    s = re.sub(r'(^|[^\w\\])(_{1,3})(?=\S)([\s\S]*?[^\s\\])\2(?!\w)', r'\1\3', s)
    s = re.sub(r'\\$', '', s)
    s = re.sub(r'\\([!-/:-@\[-`{-~])', r'\1', s)
    return re.sub('\0(\\d+)\0', lambda m: code[int(m.group(1))], s)


def markdown_to_text(body):
    body = re.sub(r'<!--[\s\S]*?-->', '', body.replace('\r\n', '\n').replace('\r', '\n'))
    body = re.sub(r'(?<!`)<(script|style)\b[\s\S]*?</\1\s*>', '', body, flags=re.I)
    out, fence = [], None
    for line in body.split('\n'):
        f = re.match(r'^ {0,3}(`{3,}|~{3,})', line)
        if f:
            if not fence:
                fence = f.group(1)
            elif f.group(1)[0] == fence[0] and len(f.group(1)) >= len(fence):
                fence = None
            continue
        if fence:
            out.append(line)
            continue
        if re.match(r'^ {0,3}\[[^\]]+\]:\s*\S+', line) and not re.match(r'^ {0,3}\[\^', line):
            continue
        if re.match(r'^ {0,3}([-*_])([ \t]*\1){2,}[ \t]*$', line) or re.match(r'^ {0,3}(=+|-+)[ \t]*$', line):
            continue
        if '|' in line and re.match(r'^ {0,3}\|?[ \t]*:?-+:?[ \t]*(\|[ \t]*:?-+:?[ \t]*)*\|?[ \t]*$', line):
            continue
        line = re.sub(r'^ {0,3}#{1,6}[ \t]+', '', line)
        line = re.sub(r'[ \t]+#+[ \t]*$', '', line)
        line = re.sub(r'^(\s*>)+\s?', '', line)
        line = re.sub(r'^\s*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*$', '', line, flags=re.I)
        line = re.sub(r'^\s*([-+*]|\d{1,9}[.)])\s+(\[[ xX]\]\s+)?', '', line)
        line = re.sub(r'^ {0,3}\[\^[^\]]+\]:\s*', '', line)
        line = re.sub(r'(^|[^\\])\|', r'\1 ', inline_to_text(line))
        out.append(line.replace('\\|', '|'))
    text = decode_entities('\n'.join(out))
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\s*\n\s*', '\n', text)
    return re.sub(r'\n+', ' ', text).strip()


def title_for(meta, body, page_path, site_name):
    if meta.get('title'):
        return meta['title']
    lines = body.splitlines()
    fence = None
    for i, line in enumerate(lines):
        f = re.match(r'^ {0,3}(`{3,}|~{3,})', line)
        if f:
            fence = (None if f.group(1)[0] == fence[0] else fence) if fence else f.group(1)
            continue
        if fence:
            continue
        m = re.match(r'^ {0,3}#[ \t]+(.+?)(?:[ \t]+#+)?[ \t]*$', line)
        if m:
            return inline_to_text(m.group(1)).strip()
        nxt = lines[i + 1] if i + 1 < len(lines) else ''
        if line.strip() and re.match(r'^ {0,3}=+[ \t]*$', nxt):
            return inline_to_text(line.strip())
    if page_path == 'Index':
        return site_name or 'Static-Pedia'
    parts = page_path.split('/')
    leaf = parts[-1]
    return (parts[-2] if leaf == 'Index' and len(parts) > 1 else leaf).replace('_', ' ')


def main():
    ap = argparse.ArgumentParser(description='Build pages.json for Static-Pedia search.')
    ap.add_argument('root', nargs='?', default='.')
    ap.add_argument('--out')
    ap.add_argument('--max-chars', type=int, default=20000)
    ap.add_argument('--exclude', action='append', default=[])
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--quiet', action='store_true')
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    out_file = os.path.abspath(args.out or os.path.join(root, 'pages.json'))
    try:
        with open(os.path.join(root, 'staticpedia.json'), encoding='utf-8') as fh:
            config = json.load(fh)
    except (OSError, ValueError):
        config = {}
    globs = (config.get('searchExclude') if isinstance(config.get('searchExclude'), list) else []) + args.exclude
    patterns = [glob_to_regex(g) for g in globs]

    files = sorted(f for f in walk(root) if not any(p.match(f) for p in patterns))
    pages = []
    for rel in files:
        with open(os.path.join(root, rel), encoding='utf-8') as fh:
            meta, body = split_front_matter(fh.read())
        if str(meta.get('noindex', '')).lower() in ('true', 'yes'):
            continue
        page_path = rel[:-3]
        text = markdown_to_text(body)
        if args.max_chars and len(text) > args.max_chars:
            text = re.sub(r'\s\S*$', '', text[:args.max_chars]) + ' …'
        pages.append({'path': page_path, 'title': title_for(meta, body, page_path, config.get('siteName')), 'text': text})

    data = json.dumps(pages, indent=2, ensure_ascii=False) + '\n'
    if args.check:
        try:
            with open(out_file, encoding='utf-8') as fh:
                current = fh.read()
        except OSError:
            current = None
        if current != data:
            print(f'{out_file} is out of date. Run: python3 tools/build_index.py {args.root}', file=sys.stderr)
            sys.exit(1)
        if not args.quiet:
            print(f'{out_file} is up to date ({len(pages)} pages).')
        return
    with open(out_file, 'w', encoding='utf-8') as fh:
        fh.write(data)
    if not args.quiet:
        print(f'Wrote {len(pages)} pages to {os.path.relpath(out_file)}')


if __name__ == '__main__':
    main()
