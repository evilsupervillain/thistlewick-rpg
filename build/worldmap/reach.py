"""Who can walk where, on a world map, using the engine's own flags.

`flags & 0x0F == 0` is the question - "open on all four sides" - not
`is_passable`, and events that block are counted as walls because a lantern in
a doorway is a sealed room.
"""
import collections
import json
import sys


def grid(project, map_id, path=None):
    """`path` overrides the map file, for a map that is no longer where it was.

    `Map008.json` used to be Thistlewick's 50x50 world and is now its 120x120
    one, so "the old map" has to be named explicitly - see
    `build/worldmap/old50.json`. Everything else still comes from the project,
    including the tileset, because the flags are the game's."""
    m = json.load(open(path or "%s/data/Map%03d.json" % (project, map_id)))
    ts = json.load(open("%s/data/Tilesets.json" % project))[m["tilesetId"]]["flags"]
    w, h, d = m["width"], m["height"], m["data"]
    blocked = set()
    for e in m["events"]:
        if e and any(p.get("priorityType") == 1 for p in e.get("pages", [])):
            blocked.add((e["x"], e["y"]))

    def openv(x, y):
        for z in (3, 2, 1, 0):
            t = d[(z * h + y) * w + x]
            if t and not (ts[t] & 0x10):
                return (ts[t] & 0x0F) == 0 and (x, y) not in blocked
        return (ts[0] & 0x0F) == 0 and (x, y) not in blocked
    return m, w, h, openv


def walk(w, h, openv, start, avoid=()):
    avoid = set(avoid)
    seen, q = {start}, collections.deque([start])
    while q:
        x, y = q.popleft()
        for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
            if (0 <= nx < w and 0 <= ny < h and (nx, ny) not in seen
                    and (nx, ny) not in avoid and openv(nx, ny)):
                seen.add((nx, ny)); q.append((nx, ny))
    return seen
