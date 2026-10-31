"""CURIOS.md 3: every decorative object on every Thistlewick map: what it is (from the
sheet's .txt), its cells, whether an event already sits on/beside it, and
whether the player can stand next to it (stationary NPCs block).

    python3 build/curio_survey.py               one line per map
    python3 build/curio_survey.py --map 4 2     every object on those maps
    python3 build/curio_survey.py out.json      the lot, as json"""
import json, os, sys
from collections import defaultdict

ROOT = "/home/mike/Projects/rpgmaker-mz/thistlewick"
D = ROOT + "/data/"
tilesets = json.load(open(D + "Tilesets.json"))
mi = json.load(open(D + "MapInfos.json"))
maps = {m["id"]: json.load(open(D + "Map%03d.json" % m["id"])) for m in mi if m}

_names = {}
def names(sheet):
    if sheet not in _names:
        p = ROOT + "/img/tilesets/%s.txt" % sheet
        if not os.path.exists(p):
            p = "/home/mike/Projects/rpgmaker-mz/reference-blank/img/tilesets/%s.txt" % sheet
        _names[sheet] = ([l.split("|")[0].strip().lstrip("﻿") for l in open(p, encoding="utf-8")]
                         if os.path.exists(p) else [])
    return _names[sheet]

def tile_name(ts, t):
    if 0 < t < 1024:
        sheet = ts["tilesetNames"][5 + t // 256]
        n = names(sheet) if sheet else []
        i = t % 256
        return (sheet, n[i] if i < len(n) else "?%d" % i)
    if 1536 <= t < 1664:
        sheet = ts["tilesetNames"][4]
        n = names(sheet) if sheet else []
        i = t - 1536
        return (sheet, n[i] if i < len(n) else "?A5-%d" % i)
    return None

def flags_at(m, x, y):
    w, h = m["width"], m["height"]
    fl = tilesets[m["tilesetId"]]["flags"]
    for z in (3, 2, 1, 0):
        t = m["data"][(z * h + y) * w + x]
        yield fl[t] if t < len(fl) else 0

def check(m, x, y, bit):
    if not (0 <= x < m["width"] and 0 <= y < m["height"]):
        return False
    for f in flags_at(m, x, y):
        if f & 0x10: continue
        if (f & bit) == 0: return True
        if (f & bit) == bit: return False
    return False

DIRS = {2: (0, 1), 4: (-1, 0), 6: (1, 0), 8: (0, -1)}
BIT = {2: 1, 4: 2, 6: 4, 8: 8}
REV = {2: 8, 4: 6, 6: 4, 8: 2}

def passable(m, x, y):
    return any(check(m, x, y, b) for b in (1, 2, 4, 8))

def flood(m, seeds, blocked):
    seen, q = set(), []
    for s in seeds:
        if passable(m, *s) and s not in seen:
            seen.add(s); q.append(s)
    while q:
        x, y = q.pop()
        for d, (dx, dy) in DIRS.items():
            n = (x + dx, y + dy)
            if n in seen or n in blocked: continue
            if not (0 <= n[0] < m["width"] and 0 <= n[1] < m["height"]): continue
            if check(m, x, y, BIT[d]) and check(m, n[0], n[1], BIT[REV[d]]):
                seen.add(n); q.append(n)
    return seen

# transfer seeds
seeds = defaultdict(set)
def walk(cmds):
    for c in cmds:
        if c["code"] == 201 and c["parameters"][0] == 0:
            seeds[c["parameters"][1]].add((c["parameters"][2], c["parameters"][3]))
for m in maps.values():
    for ev in m["events"]:
        if ev:
            for p in ev["pages"]: walk(p["list"])
for ce in json.load(open(D + "CommonEvents.json")):
    if ce: walk(ce["list"])
sysj = json.load(open(D + "System.json"))
seeds[sysj["startMapId"]].add((sysj["startX"], sysj["startY"]))

SKIP_WORDS = ("Darkness", "Wall", "Ground", "Floor", "Transparent", "Stairs",
              "Entrance", "Shadow", "Carpet", "Road", "Path", "Ladder", "Rope",
              "Hole", "Roof", "Dirt", "Grass", "Pavement", "Tile", "Brick")

import re


def skipped(name):
    """Walls, floors and roads - but not the things named after them: a
    `Wall Clock` is a curio and `Wall H (Wood)` is not."""
    if name == "Roof" or re.match(r"(Wall|Dark Wall|Roof) [A-Z]\b", name):
        return True
    return any(name.startswith(s) for s in SKIP_WORDS if s not in ("Wall", "Roof"))


out = {}
for mid, m in sorted(maps.items()):
    if mid == 8: continue
    ts = tilesets[m["tilesetId"]]
    w, h = m["width"], m["height"]
    evcells = {}
    blocked = set()
    for ev in m["events"]:
        if not ev: continue
        evcells[(ev["x"], ev["y"])] = ev["name"]
        p = ev["pages"][0]
        if p["image"]["characterName"] and p["priorityType"] == 1 and not p["through"] and p["moveType"] == 0:
            blocked.add((ev["x"], ev["y"]))
    reach = flood(m, seeds.get(mid, ()), blocked)
    cells = {}
    for y in range(h):
        for x in range(w):
            for z in (3, 2, 1):
                t = m["data"][(z * h + y) * w + x]
                r = tile_name(ts, t)
                if r and r[1] not in ("Transparent", "") and not skipped(r[1]):
                    cells[(x, y)] = r[1]
                    break
    # group same-name 4-connected cells
    seen, objs = set(), []
    for c, n in sorted(cells.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        if c in seen: continue
        comp, q = [], [c]; seen.add(c)
        while q:
            p = q.pop(); comp.append(p)
            for dx, dy in DIRS.values():
                nb = (p[0] + dx, p[1] + dy)
                if nb not in seen and cells.get(nb) == n:
                    seen.add(nb); q.append(nb)
        comp.sort(key=lambda p: (p[1], p[0]))
        ev = sorted({evcells[p] for p in comp if p in evcells})
        adj = [p for p in comp if any((p[0] + dx, p[1] + dy) in reach for dx, dy in DIRS.values())]
        objs.append(dict(name=n, cells=comp, events=ev, reachable=bool(adj),
                         on_floor=any(p in reach for p in comp)))
    out[mid] = dict(name=next(x["name"] for x in mi if x and x["id"] == mid),
                    objs=objs, events=sorted(set(evcells.values())))

if len(sys.argv) > 2 and sys.argv[1] == "--map":
    for a in sys.argv[2:]:
        v = out[int(a)]
        print("Map%03d %s - events: %s" % (int(a), v["name"], ", ".join(v["events"])))
        for o in v["objs"]:
            print("   %-30s %-34s %s%s%s" % (o["name"], " ".join("%d,%d" % tuple(c) for c in o["cells"][:4]),
                  "EV:" + "/".join(o["events"]) if o["events"] else "",
                  "" if o["reachable"] else " (unreachable)", " (floor)" if o["on_floor"] else ""))
    sys.exit()
if len(sys.argv) > 1:
    json.dump({str(k): v for k, v in out.items()}, open(sys.argv[1], "w"), indent=0)
for mid, v in out.items():
    free = [o for o in v["objs"] if not o["events"] and o["reachable"] and not o["on_floor"]]
    print("%3d %-45s objs %3d  free&reachable %3d" % (mid, v["name"][:45], len(v["objs"]), len(free)))
