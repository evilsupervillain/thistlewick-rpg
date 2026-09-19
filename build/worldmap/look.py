"""The map as text: biome, relief, stamps, roads and events in one window.

A screenshot is the only way to judge whether a map *reads* well, and it is the
wrong tool for asking where the coastline is. This prints a rectangle of the
staged map as one character per cell, which answers "is this square land",
"what is the shape of this headland" and "does that road reach the town" for
about a thousandth of the cost of rendering it - and unlike a screenshot it can
be diffed between runs.

    python3 thistlewick/build/worldmap/look.py x0 y0 x1 y1 [map-id]

    ~ sea      . grass     s snow      d desert    w wasteland   r rocky
    f dirtfield p swamp     c cloud
    M mountain T forest    = road      # a stamp or scenery tile on layer 2-3
    E an event standing on the cell    ! land with no biome worldgen can name

Uppercase wins over lowercase: a cell with anything on layers 2-3 shows `#`
whatever the ground under it is, and an event shows `E` over that, because what
is being looked for is usually a building or a door rather than the dirt.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, 'tools'))

import finish as F                                             # noqa: E402

BIOME = {'sea': '~', 'grass': '.', 'snow': 's', 'desert': 'd',
         'wasteland': 'w', 'rocky': 'r', 'dirtfield': 'f', 'swamp': 'p',
         'cloud': 'c'}


def chars():
    """autotile kind -> one character, for every record the palette names."""
    out = {}
    for name, b in F.PALETTE.biomes.items():
        out[b.base.kind] = BIOME.get(name, '?')
        for r in b.mountains:
            out[r.kind] = 'M'
        for r in b.forests:
            out[r.kind] = 'T'
    out[F.ROAD] = '='
    return out


def window(world, x0, y0, x1, y1):
    ch = chars()
    ev = {(e["x"], e["y"]) for e in (world.map.get("events") or ()) if e}
    xs = range(max(0, x0), min(world.w, x1 + 1))
    lines = ["    " + "".join(str(x // 10 % 10) for x in xs),
             "    " + "".join(str(x % 10) for x in xs)]
    for y in range(max(0, y0), min(world.h, y1 + 1)):
        row = ""
        for x in xs:
            base, relief = world.base(x, y), world.relief(x, y)
            c = ch.get(relief) if ch.get(relief) in ('M', 'T', '=') \
                else ch.get(base, '!' if base is None else '?')
            if world.g.get(x, y, 2) or world.g.get(x, y, 3):
                c = '#'
            if (x, y) in ev:
                c = 'E'
            row += c
        lines.append("%3d %s" % (y, row))
    return "\n".join(lines)


def main(argv):
    x0, y0, x1, y1 = (int(a) for a in argv[:4])
    map_id = int(argv[4]) if len(argv) > 4 else 941
    path = os.path.join(ROOT, 'staging', 'data', 'Map%03d.json' % map_id)
    if not os.path.exists(path):
        path = os.path.join(HERE, 'worldmap.json')
    print(window(F.World(path), x0, y0, x1, y1))


if __name__ == '__main__':
    main(sys.argv[1:])
