"""The hand pass over the chosen generated world.

Four things a generator got wrong or could not know, applied to the finished
map rather than to the specification, because the map is the one that was
chosen by looking at it. `MapGrid.autotile` reproduces worldgen's own output
byte for byte - measured, 0 cells differ on a round trip - so editing tiles
and re-autotiling is safe.

  1. the coast below Nether Sopping and off the Lighthouse, which the noise
     erosion ate back into a straight shelf and a one-cell land seam;
  2. the Hermit's Middle Distance, which is meant to be air-only and had
     become walkable;
  3. the Bottomless Pit, which the middle redraw buried under a mountain;
  4. the mountain range across the middle, drawn as a range rather than as the
     `MM.MM.MM` fence the 50x50 had.

Everything is in NEW map coordinates; `old(x, y)` converts.
"""
import json
import os
import sys

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))), 'tools'))
import rmmzdata as R                                          # noqa: E402
from worldgen import biomes as B                              # noqa: E402
from worldgen import noise as nz                              # noqa: E402

# The game's own tileset, which is where the passability flags come from - not
# the directory the map happens to be sitting in.
TILESETS = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "data", "Tilesets.json")

AT = (35, 35)
SEA, GRASS = 0, 16
PALETTE = B.palette()
# base autotile kind -> the mountain that belongs over it, by family.
MOUNTAIN_OF = {b.base.kind: b.mountains[0].kind
               for b in PALETTE.biomes.values() if b.mountains}
# Every relief record, so "is there anything on layer 1 here" can be answered.
FOREST_OF = {b.base.kind: (b.forests[0].kind if b.forests else None)
             for b in PALETTE.biomes.values()}


def old(x, y):
    return x + AT[0], y + AT[1]


class World:
    def __init__(self, path):
        self.path = path
        self.map = json.load(open(path))
        self.w, self.h = self.map["width"], self.map["height"]
        self.g = R.MapGrid(self.w, self.h, self.map["data"])

    def base(self, x, y):
        t = self.g.get(x, y, 0)
        return R.autotile_kind(t) if R.is_autotile(t) else None

    def relief(self, x, y):
        t = self.g.get(x, y, 1)
        return R.autotile_kind(t) if R.is_autotile(t) else None

    def put_sea(self, x, y):
        self.g.set(x, y, 0, R.make_autotile(SEA, 0))
        for z in (1, 2, 3):
            self.g.set(x, y, z, 0)

    def put_mountain(self, x, y):
        kind = MOUNTAIN_OF.get(self.base(x, y))
        if kind is None:
            return False
        self.g.set(x, y, 1, R.make_autotile(kind, 0))
        for z in (2, 3):
            self.g.set(x, y, z, 0)
        return True

    def clear_relief(self, x, y):
        self.g.set(x, y, 1, 0)

    def save(self, path=None):
        for z in (0, 1):
            self.g.autotile(z)
        self.map["data"] = self.g.data
        json.dump(self.map, open(path or self.path, "w"), ensure_ascii=False)


# ---------------------------------------------------------------- the coast --
def mend_coast(world):
    """Sea where the painted ocean should have met the old map's shore.

    The erosion that gave the ocean an organic edge was applied to every side
    of the rectangle, including the side that abuts the preserved map - so the
    old map's straight southern edge grew a straight two-row shelf, and a
    one-cell column of land ran up its eastern side."""
    n = nz.Noise("mend")
    field = n.perlin(world.w, world.h, (22, 22))
    field = (field - field.min()) / max(1e-9, float(field.max() - field.min()))
    cut = 0
    # Below the old map's southern shore, and east of the Lighthouse.
    for x in range(58, 88):
        for y in range(85, 90):
            depth = 4.0 - 2.5 * field[y][x]          # a wobbly shoreline
            if y - 84 <= depth and world.base(x, y) not in (None, SEA):
                world.put_sea(x, y); cut += 1
    for x in range(85, 88):
        for y in range(66, 86):
            depth = 2.5 - 1.5 * field[y][x]
            if x - 84 <= depth and world.base(x, y) not in (None, SEA):
                world.put_sea(x, y); cut += 1
    return cut


# ------------------------------------------------------- the air-only rocks --
def isolate(world, cells, ring=1):
    """Water all round a rock, so the only way onto it is to land on it."""
    keep = set(cells)
    cut = 0
    xs = [c[0] for c in cells]
    ys = [c[1] for c in cells]
    for y in range(min(ys) - ring, max(ys) + ring + 1):
        for x in range(min(xs) - ring, max(xs) + ring + 1):
            if (x, y) in keep or not (0 <= x < world.w and 0 <= y < world.h):
                continue
            if world.base(x, y) not in (None, SEA):
                world.put_sea(x, y); cut += 1
    return cut


# ------------------------------------------------------------------ the Pit --
def dig_out(world, cells):
    """Take the relief back off a square the redraw buried."""
    freed = 0
    for x, y in cells:
        if world.relief(x, y) is not None:
            world.clear_relief(x, y); freed += 1
    return freed


def sink_islets(world, mainland, keep, smaller_than=12):
    """Drown the scraps of beach the coast mend left standing in the water.

    A one-tile sandbar reads as a mistake rather than as an island, and the
    ones worth keeping are the ones somebody meant: the three rocks the
    airship exists to reach. Everything else under `smaller_than` cells that
    the player cannot walk to goes back to sea."""
    import collections
    spared = {c for cell in keep for c in _ring(cell, 1)}
    flags = _openness(world)
    seen, sunk, islets = set(), 0, 0
    for sy in range(world.h):
        for sx in range(world.w):
            if (sx, sy) in seen or not flags[sy][sx] or (sx, sy) in mainland:
                continue
            group, q = {(sx, sy)}, collections.deque([(sx, sy)])
            while q:
                x, y = q.popleft()
                for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                    if (0 <= nx < world.w and 0 <= ny < world.h
                            and (nx, ny) not in group and flags[ny][nx]):
                        group.add((nx, ny)); q.append((nx, ny))
            seen |= group
            if len(group) >= smaller_than or group & spared:
                continue
            islets += 1
            for x, y in group:
                world.put_sea(x, y); sunk += 1
    return islets, sunk


def _ring(cell, r):
    x, y = cell
    return {(x + dx, y + dy) for dy in range(-r, r + 1)
            for dx in range(-r, r + 1)}


def _openness(world):
    """`flags & 0x0F == 0` per cell - open on all four sides, not merely
    passable, which is the wrong question for ground you stand on."""
    ts = json.load(open(TILESETS))[world.map["tilesetId"]]["flags"]
    out = []
    for y in range(world.h):
        row = []
        for x in range(world.w):
            f = ts[0]
            for z in (3, 2, 1, 0):
                t = world.g.get(x, y, z)
                if t and not (ts[t] & 0x10):
                    f = ts[t]; break
            row.append((f & 0x0F) == 0)
        out.append(row)
    return out


# ----------------------------------------------------------- the settlements --
CATALOGUE = None


def _catalogue():
    global CATALOGUE
    if CATALOGUE is None:
        from worldgen import stamps as St
        CATALOGUE = St.catalogue()
    return CATALOGUE


def unstamp(world, near, name, radius=3):
    """Rub out one named building, found by its own tile ids near a point.

    Hand-counted rectangles get this wrong: a 2x2 stamp's door cells are its
    *bottom* row, so the footprint of Nether Sopping's `Fortress City (Snow)`
    starts one column and one row up from the door the event stands on, and a
    clear written from the door leaves two cells of city behind. The ids are
    the stamp's own, so this cannot be off by one - and it is kept to a radius
    because `Fortress City` is also what Great Dunnage is made of."""
    stamp = _catalogue().stamp(name)
    ids = {stamp.tile(dx, dy) for dy in range(stamp.h) for dx in range(stamp.w)}
    gone = 0
    for y in range(near[1] - radius, near[1] + radius + 1):
        for x in range(near[0] - radius, near[0] + radius + 1):
            if not (0 <= x < world.w and 0 <= y < world.h):
                continue
            for z in (2, 3):
                if world.g.get(x, y, z) in ids and world.g.get(x, y, z):
                    world.g.set(x, y, z, 0); gone += 1
    return gone


def restamp(world, at, name, clear=()):
    """Put a different building on a square, and rub out the old one.

    The 50x50 draws Thistlewick as `Fortress City` and Nether Sopping as
    `Fortress City (Snow)` - a walled city for a turnip village, and a snowed
    one in the temperate south. Both are older than this world map; they were
    simply not obvious until the map had a climate."""
    stamp = _catalogue().stamp(name)
    for x, y in clear:
        for z in (2, 3):
            world.g.set(x, y, z, 0)
    for dy in range(stamp.h):
        for dx in range(stamp.w):
            world.g.set(at[0] + dx, at[1] + dy, 3, stamp.tile(dx, dy))
            world.g.set(at[0] + dx, at[1] + dy, 2, 0)
    return stamp


def put_tiles(world, cells, name, z=3):
    """One stamp's single tile, repeated - what a pier is."""
    stamp = _catalogue().stamp(name)
    for x, y in cells:
        world.g.set(x, y, z, stamp.tile(0, 0))
    return len(cells)


ROAD = 29                                                   # Road (Dirt)


def put_road(world, cells):
    """Road on layer 1, which is where the corpus and worldgen both put it."""
    for x, y in cells:
        world.g.set(x, y, 1, R.make_autotile(ROAD, 0))
    return len(cells)


# ---------------------------------------------------------------- the range --
def old_events(path='thistlewick/data/Map008.json'):
    """Every square the 50x50's own events stand on, on the new map.

    The generated world carries worldgen's door events and nothing else - the
    game's events are still in `Map008.json` and arrive when the build script
    places them - so protecting `world.map["events"]` protects the wrong list,
    which is how the first draft buried the Barrow."""
    m = json.load(open(path))
    return [old(e["x"], e["y"]) for e in m["events"] if e]


def draw_range(world, spine, thickness, passes, keep=(), seed="range"):
    """A range along a polyline, with named gaps left open as passes.

    Thickness varies along the spine from a noise field, which is the whole
    difference between a range and a fence: the 50x50's version was a fixed
    period of two mountains and a gap, repeated, and it read as one."""
    n = nz.Noise(seed)
    field = n.perlin(world.w, world.h, (11, 11))
    field = (field - field.min()) / max(1e-9, float(field.max() - field.min()))
    wobble = n.derive("wobble").perlin(world.w, world.h, (5, 5))

    points = []
    for (x0, y0), (x1, y1) in zip(spine, spine[1:]):
        steps = max(abs(x1 - x0), abs(y1 - y0))
        for i in range(steps + 1):
            points.append((x0 + (x1 - x0) * i / steps,
                           y0 + (y1 - y0) * i / steps))

    # Never over an event, nor the ring round it: a door has to be walked to,
    # and every world-map curiosity is an event standing on open ground. The
    # first draft of this buried the Barrow and Meredith Crooke's camp, which
    # is exactly the mistake a hand-typed list of exceptions makes again later.
    open_cells = set()
    for px, py in passes:
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                open_cells.add((px + dx, py + dy))
    for ex, ey in list(keep) + [(e["x"], e["y"])
                                for e in (world.map.get("events") or ()) if e]:
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                open_cells.add((ex + dx, ey + dy))

    drawn = 0
    for px, py in points:
        cx = int(round(px))
        cy = int(round(py + 1.5 * wobble[int(py) % world.h][cx % world.w]))
        half = thickness * (0.55 + 0.9 * field[cy % world.h][cx % world.w])
        for dy in range(-int(half) - 1, int(half) + 2):
            y = cy + dy
            if not (0 <= y < world.h) or abs(dy) > half:
                continue
            if (cx, y) in open_cells:
                continue
            if world.put_mountain(cx, y):
                drawn += 1
    return drawn
