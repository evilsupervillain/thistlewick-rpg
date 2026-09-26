"""Grep the game's player-visible text, marking each line Published or Free.

`AUDIT.md` item 6's tool. Every Show Text line, choice list and database
description in `data/` is dumped with where it is - map, event, page and the
speaker - and the same is dumped off the `live-rpg` branch, so a line is **P**
only if the identical line is in the published game and **F** otherwise
(`AUDIT.md` section 0). It reads the built data, not the source, so run it
after a build.

    python3 build/audit_text.py 'thousand|hundred years'     # P/F, where, line
    python3 build/audit_text.py --event 'Map042 ev2 '         # one event's text
    python3 build/audit_text.py --free 'crowns?'              # Free lines only

The regex is case-insensitive and matched against the text with its colour
codes left in. Not part of the data build.
"""
import argparse
import glob
import json
import os
import re
import subprocess

GAME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = "live-rpg"


def _files(ref):
    if ref is None:
        return sorted("data/" + os.path.basename(p)
                      for p in glob.glob(os.path.join(GAME, "data", "*.json")))
    out = subprocess.run(["git", "-C", GAME, "ls-tree", "--name-only", ref,
                          "data/"], capture_output=True, text=True, check=True)
    return sorted(out.stdout.split())


def _load(ref, path):
    if ref is None:
        with open(os.path.join(GAME, path)) as f:
            return json.load(f)
    out = subprocess.run(["git", "-C", GAME, "show", "%s:%s" % (ref, path)],
                         capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def _commands(lst, where, out):
    speaker = ""
    for c in lst or []:
        code, p = c["code"], c["parameters"]
        if code == 101:
            speaker = p[4] if len(p) > 4 else ""
        elif code in (401, 405):
            out.append((where + (" [%s]" % speaker if speaker else ""), p[0]))
        elif code == 102:
            out.append((where + " choice", " / ".join(p[0])))


def dump(ref=None):
    """[(where, line)] for every line of text in `data/` at `ref`, or on disk
    when `ref` is None."""
    out = []
    for path in _files(ref):
        if not path.endswith(".json"):
            continue
        d = _load(ref, path)
        base = path[5:-5]
        if base.startswith("Map") and base != "MapInfos":
            out.append((base + " name", d.get("displayName", "")))
            for e in d.get("events") or []:
                if e:
                    for i, pg in enumerate(e["pages"]):
                        _commands(pg["list"], "%s ev%d %s p%d"
                                  % (base, e["id"], e["name"], i), out)
        elif base == "CommonEvents":
            for e in d:
                if e:
                    _commands(e["list"], "CE%d %s" % (e["id"], e["name"]), out)
        elif base == "Troops":
            for t in d:
                if t:
                    for i, pg in enumerate(t["pages"]):
                        _commands(pg["list"], "Troop%d %s p%d"
                                  % (t["id"], t["name"], i), out)
        elif isinstance(d, list):
            for r in d:
                if isinstance(r, dict):
                    for k in ("description", "note", "profile", "nickname",
                              "message1", "message2", "message3", "message4"):
                        for line in str(r.get(k) or "").split("\n"):
                            if line:
                                out.append(("%s#%d %s %s" % (
                                    base, r["id"], r.get("name", ""), k), line))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("pattern", nargs="?", default="")
    ap.add_argument("--event", help="print every line whose location starts "
                    "with this, e.g. 'Map042 ev2 '")
    ap.add_argument("--free", action="store_true", help="Free lines only")
    ap.add_argument("--published", action="store_true",
                    help="Published lines only")
    a = ap.parse_args()
    live = {t for _, t in dump(REF)}
    pat = re.compile(a.pattern, re.I)
    for where, t in dump():
        if a.event and not where.startswith(a.event):
            continue
        if not pat.search(t):
            continue
        pub = t in live
        if (a.free and pub) or (a.published and not pub):
            continue
        print("%s %-55s | %s" % ("P" if pub else "F", where[:55], t))


if __name__ == "__main__":
    main()
