"""Keeps the Thistle-pedia's red links honest.

    python3 scripts/thistlepedia/redlinks.py          # rewrite, then list red links
    python3 scripts/thistlepedia/redlinks.py --list   # list red links only

An encyclopedia written a volume at a time links to articles that do not exist
yet. Static-Pedia's answer is the red link, `<a class="new" href="...">`, which
the link checker skips; the danger is that a red link outlives its excuse, or
an ordinary link quietly points at nothing. This makes the state of every link
a fact about the files rather than something to remember:

* an ordinary Markdown link `[text](Page)` to a page that does not exist
  becomes `<a class="new" href="Page">text</a>`;
* so does a plain `<a href="Page">text</a>`, which is how a link is written
  inside a raw HTML block, where Markdown links do not render;
* a red link to a page that now exists becomes `<a href="Page">text</a>`,
  which works both in Markdown and inside HTML.

Only page links are touched (no extension, or `.md`, or a trailing `/`), and
only in prose - fenced code is left alone. It resolves links the way
Static-Pedia does: relative to the page's folder, or to the wiki root when
they start with `/`. Then it prints every red link left, grouped by target,
which is the list of articles still owed.
"""
import os
import re
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
WIKI = os.path.join(os.path.dirname(os.path.dirname(HERE)), "thistlepedia")

MD_LINK = re.compile(r"(?<!!)\[([^\]\n]+)\]\(([^)\s]+)\)")
RED_LINK = re.compile(r'<a class="new" href="([^"]+)">([^<]+)</a>')
HTML_LINK = re.compile(r'<a href="([^"]+)">([^<]+)</a>')


def is_page(target):
    if re.match(r"^[a-z]+:", target) or target.startswith(("#", "?")):
        return False
    path = target.split("#", 1)[0]
    if not path or path.endswith((".md", "/")):
        return bool(path)
    last = path.rsplit("/", 1)[-1]
    ext = last.rsplit(".", 1)[1] if "." in last else ""
    return not re.search(r"[A-Za-z]", ext)


def resolve(page_dir, target):
    """The .md file a page link names, relative to the wiki root."""
    path = target.split("#", 1)[0]
    base = "" if path.startswith("/") else page_dir
    path = os.path.normpath(os.path.join(base, path.lstrip("/")))
    if target.split("#", 1)[0].endswith("/"):
        return os.path.join(path, "Index.md")
    return path if path.endswith(".md") else path + ".md"


def exists(rel):
    return os.path.isfile(os.path.join(WIKI, rel))


def rewrite(text, page_dir, red):
    out, fenced = [], False
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            fenced = not fenced
        if not fenced:
            def to_red(m):
                label, target = m.group(1), m.group(2)
                if is_page(target) and not exists(resolve(page_dir, target)):
                    return f'<a class="new" href="{target}">{label}</a>'
                return m.group(0)

            def html_to_red(m):
                target, label = m.group(1), m.group(2)
                if is_page(target) and not exists(resolve(page_dir, target)):
                    return f'<a class="new" href="{target}">{label}</a>'
                return m.group(0)

            def to_blue(m):
                target, label = m.group(1), m.group(2)
                if is_page(target) and exists(resolve(page_dir, target)):
                    return f'<a href="{target}">{label}</a>'
                red[resolve(page_dir, target)].append(page_dir or ".")
                return m.group(0)
            line = MD_LINK.sub(to_red, line)
            line = HTML_LINK.sub(html_to_red, line)
            line = RED_LINK.sub(to_blue, line)
        out.append(line)
    return "\n".join(out)


def main(argv):
    listing = "--list" in argv
    red, changed = defaultdict(list), []
    for root, dirs, files in os.walk(WIKI):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for name in files:
            if not name.endswith(".md"):
                continue
            path = os.path.join(root, name)
            page_dir = os.path.relpath(root, WIKI)
            page_dir = "" if page_dir == "." else page_dir
            text = open(path, encoding="utf-8").read()
            new = rewrite(text, page_dir, red)
            if new != text and not listing:
                open(path, "w", encoding="utf-8").write(new)
                changed.append(os.path.relpath(path, WIKI))
    for path in changed:
        print(f"rewrote {path}")
    print(f"{len(red)} articles still owed (red links):")
    for target in sorted(red):
        print(f"  {target[:-3]}  <- {len(red[target])} link(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
