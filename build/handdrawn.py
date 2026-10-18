"""Maps whose tiles were drawn by hand in the editor, kept as committed files.

    python3 build/handdrawn.py freeze 9        data/Map009.json -> build/handdrawn/Map009.json
    python3 build/handdrawn.py check           every frozen map still matches its data file
    python3 build/handdrawn.py widen 18 16 3   three more columns of black at x 16
    python3 build/handdrawn.py set 20 16 22 3 177   one tile, one layer

The build writes `data/*.json`, so anything painted in the editor is gone the
next time it runs. A map that is better drawn than generated - the Gloamwood,
from 8 October 2026 - is frozen instead: `freeze` copies its tile layers out of
the data file into `build/handdrawn/`, and the map's builder loads them from
there with `load()`. Its events stay in code, where they always were, so a
frozen map still gets every quest's pages.

What is frozen is layers 0-4, the tiles and the shadows. Layer 5, the regions,
is not: it is derived from passability by `mapkit.paint_regions`, and an
editor session that moves a wall leaves the old regions behind it.

To change a frozen map: edit it in the editor, `freeze` it, rebuild. The file
is one row per line so the diff of an edit is the rows it touched.

`widen` is the one change made to a frozen file outside the editor: it copies
an all-black column in place to push everything east of it further east, so
two rooms drawn side by side on one map are far enough apart that neither
shows from the edge of the other. The builder's width and every event east
of the column move by the same amount, by hand.

`set` is the other: one tile on one layer, for a prop that contradicts the
line the player reads when they examine it (October 2026) - `Rubble` under
words cut into stone, a teddy-bear shelf under jars of cuttings. Mike rsyncs
`data/` back to his editor, so the change reaches the editor on his next
pull; whatever he paints after that is frozen over it as usual.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
import rmmzdata as R

FROZEN = os.path.join(HERE, "handdrawn")
LAYERS = 5          # tiles 0-3 and the shadow layer; regions are derived


def frozen():
    """The ids of every frozen map. The build's post-passes leave these
    alone: their walls and shadows are as they were drawn."""
    if not os.path.isdir(FROZEN):
        return set()
    return {int(n[3:6]) for n in os.listdir(FROZEN) if n.startswith("Map")}


def path(map_id):
    return os.path.join(FROZEN, "Map%03d.json" % map_id)


def load(map_id, width, height, tileset):
    """The frozen tiles of `map_id` as a full six-layer data list, with an
    empty region layer. Asserts the shape it was frozen at, so a builder whose
    idea of the map has changed - a new size, another tileset - fails here
    rather than drawing one map's tiles over the other's grid."""
    with open(path(map_id)) as f:
        frozen = json.load(f)
    got = (frozen["width"], frozen["height"], frozen["tilesetId"])
    if got != (width, height, tileset):
        raise ValueError(
            "build/handdrawn/Map%03d.json is %dx%d on tileset %d; the builder "
            "wants %dx%d on tileset %d. Re-freeze it or fix the builder."
            % ((map_id,) + got + (width, height, tileset)))
    data = []
    for layer in frozen["layers"]:
        assert len(layer) == height and all(len(r) == width for r in layer)
        for row in layer:
            data += row
    return data + [0] * (width * height * (6 - LAYERS))


def freeze(map_id):
    m = R.load_map(map_id)
    w, h = m["width"], m["height"]
    d = m["data"]
    layers = [[d[(z * h + y) * w:(z * h + y + 1) * w] for y in range(h)]
              for z in range(LAYERS)]
    _write(map_id, w, h, m["tilesetId"], layers)
    print("froze Map%03d (%dx%d) into %s" % (map_id, w, h,
                                              os.path.relpath(path(map_id))))


def widen(map_id, x, count):
    """Insert `count` copies of column `x` of a frozen map at `x`. The column
    has to be the same tile all the way down on every layer - black between
    two rooms - or this refuses, because copying a column through a room
    would stretch the room."""
    with open(path(map_id)) as f:
        frozen = json.load(f)
    w, h = frozen["width"], frozen["height"]
    for z, layer in enumerate(frozen["layers"]):
        if len({row[x] for row in layer}) != 1:
            raise ValueError("Map%03d column %d is not uniform on layer %d"
                             % (map_id, x, z))
    layers = [[row[:x] + [row[x]] * count + row[x:] for row in layer]
              for layer in frozen["layers"]]
    _write(map_id, w + count, h, frozen["tilesetId"], layers)
    print("widened Map%03d at x %d by %d: %dx%d" % (map_id, x, count,
                                                    w + count, h))


def set_tile(map_id, x, y, z, tile):
    with open(path(map_id)) as f:
        frozen = json.load(f)
    old = frozen["layers"][z][y][x]
    frozen["layers"][z][y][x] = tile
    _write(map_id, frozen["width"], frozen["height"], frozen["tilesetId"],
           frozen["layers"])
    print("Map%03d (%d,%d) layer %d: %d -> %d" % (map_id, x, y, z, old, tile))


def _write(map_id, w, h, tileset, layers):
    os.makedirs(FROZEN, exist_ok=True)
    with open(path(map_id), "w") as f:
        f.write('{"width": %d, "height": %d, "tilesetId": %d,\n'
                % (w, h, tileset))
        f.write(' "layers": [\n')
        f.write(",\n".join(
            "  [\n" + ",\n".join("   " + json.dumps(r) for r in layer) + "\n  ]"
            for layer in layers))
        f.write("\n ]}\n")


def check():
    """Every frozen map's tiles against its data file. Non-zero if any differ,
    which after a build means a builder is not loading its frozen file, and
    before one means somebody has been in the editor."""
    bad = 0
    for name in sorted(os.listdir(FROZEN)):
        map_id = int(name[3:6])
        m = R.load_map(map_id)
        w, h = m["width"], m["height"]
        want = load(map_id, w, h, m["tilesetId"])[:w * h * LAYERS]
        diff = sum(a != b for a, b in zip(want, m["data"][:w * h * LAYERS]))
        print("Map%03d: %s" % (map_id, "matches" if not diff else
                               "%d cells differ" % diff))
        bad += bool(diff)
    return bad


if __name__ == "__main__":
    R.use_project(os.path.join(HERE, ".."))
    if sys.argv[1:2] == ["freeze"] and len(sys.argv) == 3:
        freeze(int(sys.argv[2]))
    elif sys.argv[1:2] == ["widen"] and len(sys.argv) == 5:
        widen(*map(int, sys.argv[2:]))
    elif sys.argv[1:2] == ["set"] and len(sys.argv) == 7:
        set_tile(*map(int, sys.argv[2:]))
    elif sys.argv[1:] == ["check"]:
        sys.exit(1 if check() else 0)
    else:
        sys.exit(__doc__)
