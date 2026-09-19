"""The decoration diff: what the old 50x50 drew on layers 2-3 and the new map does not.

`Map008.json` is built output, so it contains every one of `wilds.py`'s,
`field.py`'s, `meadow.py`'s and `journey.py`'s seventy-four hand-written tile
writes - huts, signs, rocks, cave mouths, trees, tower icons. None of them is an
event, so the pass that replaces the drawn world map with a generated one
deletes all of them silently. Diffing the two maps at `+ (35,35)` finds every
casualty at once, which is why this is the check to re-run after any change to
`run_finish.py`.

    python3 thistlewick/build/worldmap/decor.py [map-id]

Reads the staged map by default so it measures what was just built. Cells whose
absence is deliberate - the three `Fortress City` restamps and the Lighthouse's
`Tower A (Snow)`, all re-sited by WORLDMAP.md section 4 - are named and counted
separately from the casualties, because otherwise the number never goes to zero
and stops being a check.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, 'tools'))

AT = (35, 35)

# The stamps section 4 deliberately rubbed out or moved. A cell that differs
# only because it held one of these is expected, not a casualty.
EXPECTED = ('World_B/Fortress City', 'World_B/Fortress City (Snow)',
            'World_B/Tower A (Snow)')


def _names():
    """tile id -> the catalogue record that owns it, for every stamp cell."""
    from worldgen import stamps as St
    cat = St.catalogue()
    out = {}
    for key, stamp in cat.stamps.items():
        for dy in range(stamp.h):
            for dx in range(stamp.w):
                out.setdefault(stamp.tile(dx, dy), key)
    return out


def cells(m, z):
    w, h, d = m["width"], m["height"], m["data"]
    return {(x, y): d[(z * h + y) * w + x]
            for y in range(h) for x in range(w) if d[(z * h + y) * w + x]}


def diff(old_path, new_path, nudge=3):
    """Every old layer-2/3 cell the new map does not carry, with how far the
    same tile had to move to survive.

    A scatter tree whose square is now under the hand-drawn range is re-placed
    a cell or two over by `finish.put_scenery`, so an exact-coordinate diff
    reports it as missing for ever and the number never reaches zero. Anything
    found within `nudge` cells counts as accounted for and is reported as a
    move rather than a loss."""
    om, nm = json.load(open(old_path)), json.load(open(new_path))
    names = _names()
    gone = []
    for z in (2, 3):
        oc, nc = cells(om, z), cells(nm, z)
        for (x, y), t in sorted(oc.items(), key=lambda kv: (kv[0][1], kv[0][0])):
            nx, ny = x + AT[0], y + AT[1]
            if nc.get((nx, ny)) == t:
                continue
            near = None
            for r in range(1, nudge + 1):
                for dy in range(-r, r + 1):
                    for dx in range(-r, r + 1):
                        if max(abs(dx), abs(dy)) == r and nc.get((nx + dx, ny + dy)) == t:
                            near = (nx + dx, ny + dy)
                            break
                    if near:
                        break
                if near:
                    break
            gone.append((z, (x, y), (nx, ny), t, names.get(t, '?'), near))
    return gone


def main(argv):
    map_id = int(argv[0]) if argv else 941
    new = os.path.join(ROOT, 'staging', 'data', 'Map%03d.json' % map_id)
    if not os.path.exists(new):
        new = os.path.join(HERE, 'worldmap.json')
    gone = diff(os.path.join(ROOT, 'thistlewick', 'data', 'Map008.json'), new)
    deliberate = [g for g in gone if g[4] in EXPECTED]
    rest = [g for g in gone if g[4] not in EXPECTED]
    moved = [g for g in rest if g[5]]
    casualties = [g for g in rest if not g[5]]
    print("decoration cells that differ: %d  (%d deliberate, %d nudged, "
          "%d casualties)" % (len(gone), len(deliberate), len(moved),
                              len(casualties)))
    for z, o, n, t, name, near in moved:
        print("  nudged    old %-9s wanted %-9s found %-9s  %s"
              % ("(%d,%d)" % o, "(%d,%d)" % n, "(%d,%d)" % near, name))
    for z, o, n, t, name, near in casualties:
        print("  LOST      layer %d  old %-9s new %-9s  id %-5d %s"
              % (z, "(%d,%d)" % o, "(%d,%d)" % n, t, name))
    return 1 if casualties else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
