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

    def put_land(self, x, y, biome='grass'):
        """Ground where there was sea, with nothing standing on it.

        The inverse of `put_sea`, and it is needed for exactly one thing a
        generator cannot be asked for after the fact: a shape. The Lighthouse's
        headland is three cells of rock reaching out past a coastline that is
        otherwise where the erosion left it, and cutting water alone can only
        ever make a coast straighter."""
        self.g.set(x, y, 0, R.make_autotile(PALETTE.biomes[biome].base.kind, 0))
        for z in (1, 2, 3):
            self.g.set(x, y, z, 0)

    def put_forest(self, x, y):
        """Trees where a road was, which is how a village stops having a road.

        Clearing layer 1 leaves bare ground, and a bare cell threading a wood
        is a path - so Olde Evermore with its road merely deleted still has a
        visible way in, which is the opposite of hidden."""
        kind = FOREST_OF.get(self.base(x, y))
        if kind is None:
            return False
        self.g.set(x, y, 1, R.make_autotile(kind, 0))
        return True

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

    def settle(self):
        """Autotile layers 0 and 1 *now*.

        Everything in here writes shape 0 and lets `save` autotile at the end,
        which is fine for tiles - but not for anything that then asks the
        engine's passability flags, because a flag belongs to a *shape* and not
        to a kind. So a pass that reads `_openness` over the whole map has to
        settle first or it is reading shapes the engine will never see. Calling
        it twice is free: a round trip through `autotile` is byte-exact."""
        for z in (0, 1):
            self.g.autotile(z)

    def save(self, path=None):
        self.settle()
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


# --------------------------------------------------------- hand-placed sites --
# WORLDMAP.md 7.6: the generated twenty-one got three things for free that a
# site put down by hand has to be given - the stamp, a door event per walkable
# cell with no destination, and a standable check on every door cell. These are
# the three, in one call, so a new site cannot be half-placed.

def add_site(world, at, stamp_name, name, kind, note=None, check=True):
    """A site: the stamp, and one player-touch door event per walkable cell.

    **Player touch, below characters**, which is worldgen's own rule and the
    engine's: an event at "same as characters" is triggered from the tile
    beside it, so a door the player is meant to walk into is walked straight
    over. The door chimes and goes nowhere, exactly like the generated
    twenty-one, until somebody builds the room behind it.

    `check` refuses to place a site whose stamp leaves no walkable cell to put
    a door on, or that lands on another stamp's footprint - the two mistakes
    arithmetic makes silently. A `Floating Continent` is all star tiles, so its
    walkable cell is decided by the ground underneath, which is why the check
    asks the finished map rather than the stamp.

    `stamp_name` may be None, for a site whose landmark is *terrain*. Ashcombe
    Lake is a body of water, and `Pond` is one small round pond drawn on a
    single tile - repeat it over eight cells and the result is eight small
    round ponds rather than a lake, which is only visible in a screenshot. The
    three air-only rocks are the same category the other way up: events on bare
    ground. So the door goes down, nothing is drawn, and the caller draws the
    landmark out of terrain."""
    stamp = _catalogue().stamp(stamp_name) if stamp_name else None
    cells = [(at[0] + dx, at[1] + dy)
             for dy in range(stamp.h) for dx in range(stamp.w)] if stamp \
        else [at]
    if check:
        for x, y in cells:
            if not (0 <= x < world.w and 0 <= y < world.h):
                raise ValueError("%s: (%d,%d) is off the map" % (name, x, y))
            if world.g.get(x, y, 2) or world.g.get(x, y, 3):
                raise ValueError("%s: (%d,%d) already carries a stamp"
                                 % (name, x, y))
    if stamp:
        restamp(world, at, stamp_name)
    flags = _openness(world)
    doors = [c for c in cells if flags[c[1]][c[0]]]
    if check and not doors:
        raise ValueError("%s at %s: no walkable cell for a door - the stamp "
                         "blocks every cell of its own footprint, or the "
                         "ground under a star stamp is not standable"
                         % (name, at))
    events = world.map.setdefault("events", [None])
    for x, y in doors:
        events.append(R.event(
            len(events), name, x, y,
            [R.page(R.comment(["hand-placed site %r" % name,
                               "%s, drawn with %s"
                               % (kind, stamp.name if stamp
                                  else "terrain, not a stamp"),
                               "no destination yet - see "
                               "worldgen.sites.transfer_page"])
                    + [R.play_se("Move1")], trigger=1, priority=0)],
            note=note or "<worldmap-site %s>" % kind))
    return doors


def make_doors_inert(world):
    """Strip every site door to a page with no commands, and move what the page
    said into the event's note.

    A placeholder door plays a chime and goes nowhere, which is right on a
    review map and wrong in a shipped one: 29 of them means a sound effect that
    promises a room 29 times and never delivers. An **empty page** is the
    engine's own way to say "this event exists and does nothing" - `Game_Event.
    start` requires `list().length > 1`, so a page holding only its terminator
    never runs, and `validate.py` exempts a page with no commands from every
    "can this be triggered" question. The stamp on the map already says town;
    walking over it and getting nothing reads as unfinished country.

    The record is not lost, it moves: the comment lines the page carried go into
    the note, which the editor shows, which nothing executes, and which is
    already how `<aironly>` and `<worldgen-site ...>` are carried. Writing the
    transfer later means replacing the page, and `worldgen.sites.transfer_page`
    is the shape to replace it with.

    Runs over the generated twenty-one as well as the hand-placed eight -
    `generated.json` is never edited, so this is the only place the generated
    doors can be normalised - and is idempotent."""
    done = 0
    for e in (world.map.get("events") or ()):
        if not e or "-site" not in (e.get("note") or ""):
            continue
        said = []
        for page in e["pages"]:
            said += [c["parameters"][0] for c in page["list"]
                     if c["code"] in (108, 408) and c["parameters"]]
            page["list"] = [{"code": 0, "indent": 0, "parameters": []}]
        extra = " ".join(s for s in said if not s.startswith("no destination"))
        if extra and extra not in e["note"]:
            e["note"] = "%s %s - placeholder, no destination yet; replace the " \
                        "page with worldgen.sites.transfer_page" % (e["note"],
                                                                   extra)
        done += 1
    return done


def move_site(world, name, to, stamp_name=None, radius=3):
    """Re-site a generated site: rub the building out, stamp it again, and take
    its door events with it.

    Four of the twenty-one are in the wrong place because a bio asserts a
    geography the allocator could not know about - Penultima is *The Last Town
    Before The End* and was standing on the wrong road. Moving one is three
    things that have to agree: the tiles, the events, and the hand-maintained
    site table in WORLDMAP.md. This does the first two and reports the third.

    The events move by the same offset as the stamp, so a 2x1 town's two doors
    stay one apart. Nothing is deleted: an event id is an index into the map's
    own list and a hole in it is a hole for ever, so re-siting moves events and
    never drops them."""
    evs = [e for e in (world.map.get("events") or ()) if e and e["name"] == name]
    if not evs:
        raise ValueError("no events named %r to move" % name)
    at = (min(e["x"] for e in evs), min(e["y"] for e in evs))
    stamp = _catalogue().stamp(stamp_name) if stamp_name else None
    if stamp_name:
        # The door row of a stamp is its BOTTOM row, so a 2x1 town's footprint
        # starts where its doors are and a 1x2 tower's one row above them.
        unstamp(world, at, stamp_name, radius=radius)
    dx, dy = to[0] - at[0], to[1] - at[1]
    if stamp:
        restamp(world, (at[0] + dx, at[1] + dy - (stamp.h - 1)), stamp_name)
    flags = _openness(world)
    for e in evs:
        e["x"], e["y"] = e["x"] + dx, e["y"] + dy
        if not flags[e["y"]][e["x"]]:
            raise ValueError("%s: door (%d,%d) is not standable"
                             % (name, e["x"], e["y"]))
    return [(e["x"], e["y"]) for e in evs]


def site_doors(world, name):
    return [(e["x"], e["y"]) for e in (world.map.get("events") or ())
            if e and e["name"] == name]


def put_tiles(world, cells, name, z=3):
    """One stamp's single tile, repeated - what a pier is."""
    stamp = _catalogue().stamp(name)
    for x, y in cells:
        world.g.set(x, y, z, stamp.tile(0, 0))
    return len(cells)


def put_scenery(world, cells, name, z=3, radius=3):
    """Scenery back onto a square, or onto the nearest square that will take it.

    `put_tiles` writes where it is told, which is right for a pier and wrong
    for the thirteen decoration cells the middle redraw ate: three of the old
    map's scatter trees now stand under the hand-drawn range and one is out at
    sea, and writing a Giant Tree onto a mountain or onto water puts the tile
    down without complaint and looks like a fault in the map. These tiles are
    *scatter* - hand-typed lists in `journey.py`, `wilds.py` and `field.py`
    with no meaning attached to any one coordinate - so nudging one to the next
    open cell keeps the dressing and costs nothing, whereas clearing a mountain
    to make room for it would hole the range for a decoration.

    Refuses sea, refuses a cell with mountain relief on it, refuses a cell that
    already carries a layer 2-3 tile (a stamp's own footprint) and refuses a
    cell an event stands on. Returns the list of (asked, placed) so the caller
    can print which ones moved; `placed` is None for one that found nowhere."""
    stamp = _catalogue().stamp(name)
    ev = {(e["x"], e["y"]) for e in (world.map.get("events") or ()) if e}
    mountains = set(MOUNTAIN_OF.values())
    taken = set()

    def ok(x, y):
        if not (0 <= x < world.w and 0 <= y < world.h) or (x, y) in taken:
            return False
        if world.base(x, y) in (None, SEA) or world.relief(x, y) in mountains:
            return False
        if world.g.get(x, y, 2) or world.g.get(x, y, 3) or (x, y) in ev:
            return False
        return True

    out = []
    for cx, cy in cells:
        found = None
        for r in range(radius + 1):
            for dy in range(-r, r + 1):
                for dx in range(-r, r + 1):
                    if max(abs(dx), abs(dy)) == r and ok(cx + dx, cy + dy):
                        found = (cx + dx, cy + dy)
                        break
                if found:
                    break
            if found:
                break
        if found:
            world.g.set(found[0], found[1], z, stamp.tile(0, 0))
            taken.add(found)
        out.append(((cx, cy), found))
    return out


def report_scenery(label, placed):
    kept = sum(1 for a, b in placed if b == a)
    moved = [(a, b) for a, b in placed if b and b != a]
    lost = [a for a, b in placed if b is None]
    print("%-22s %d as asked%s%s" % (
        label + ":", kept,
        ", %d nudged %s" % (len(moved), " ".join(
            "(%d,%d)->(%d,%d)" % (a[0], a[1], b[0], b[1]) for a, b in moved))
        if moved else "",
        ", %d LOST %s" % (len(lost), lost) if lost else ""))


ROAD = 29                                                   # Road (Dirt)


def put_road(world, cells):
    """Road on layer 1, which is where the corpus and worldgen both put it."""
    for x, y in cells:
        world.g.set(x, y, 1, R.make_autotile(ROAD, 0))
    return len(cells)


# -------------------------------------------------------------- the regions --
# `Map008`'s `encounterList` filters every random battle by region, and a
# generated map has no region layer - so the new world had **no random
# encounters anywhere**, with nine perfectly good encounter entries sitting in
# its header pointing at regions nothing was painted with. WORLDMAP.md item 3.
#
# The old 50x50's scheme, from `journey.py` and its two hooks:
#   1 SOUTH  y >= 30, the gentle half    turnips, crows, field mix
#   2 NORTH  y <= 21                     goblins, bandits, wisps
#   3 COAST  the shingle, x >= 26        crabs, gulls, coast mix
#   4 CLANG  the north-west lobe         the same three as NORTH
#   0        the mountain band, y 22-29, and the three air-only rocks
#
# Three things change, and each is a decision rather than a translation:
#
# * **The divide is the range, not a latitude.** The 50x50 split at y=21/30
#   because its mountain fence was on a fixed period across those rows; the new
#   map has a drawn range whose spine runs from y=62 in the west to y=56 in the
#   east, so the divide follows it per column. The eight-row dead band between
#   the two goes: it was the fence, the fence is gone, and "no encounters here"
#   was never the intent.
# * **Snow and desert get regions of their own** - 5 and 6 - because a third of
#   this map's climate did not exist on the 50x50 and pointing it at turnips
#   would be worse than leaving it empty. They are *pointed at* the north's
#   three troops for now, by adding them to those entries' `regionSet`, so
#   nothing is empty today; the reason they are separate ids rather than just
#   painted as 2 is so that a campaign writing real snow and desert encounters
#   has somewhere to hang them without repainting the map.
# * **The shingle has to be adjacent to sea.** `K.W_SAND` is autotile kind 26,
#   `Dirt Field A`, and on the 50x50 every cell of it was shore. On the new map
#   there are 353, including an inland basin in the far north - so a rule that
#   says "kind 26 is the coast" puts crabs and gulls in a snowfield.
#
# **The six ids come from `places.py`**, one directory up, which is this game's
# "the handful of things two modules have to agree on". They have to be the
# same numbers here and in `journey.world_map`'s `encounters=` list, and a
# region painted with a number no encounter entry names is a region with no
# battles in it - which is the whole fault item 3 existed to fix, so it is not
# a thing to keep two copies of.
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from places import (REG_SOUTH, REG_NORTH, REG_COAST,        # noqa: E402
                    REG_CLANG, REG_SNOW, REG_DESERT)
SHINGLE, SNOW, DESERT = 26, 40, 32
# The old north-west lobe, translated: `field.py` painted x < 16, y < 21.
CLANG_LOBE = (AT[0], AT[1], AT[0] + 16, AT[1] + 21)


def paint_regions(world, spine, quiet=(), start=None):
    """Region-tag every cell the player can stand on.

    `quiet` is the cells that get region 0 - the air-only rocks, because nothing
    lives out there and a party that has just landed on the Isle of Uncertain
    Ownership should not be met by turnips. Everything else standable gets a
    region, sea excluded by construction: `_openness` reads the engine's own
    flags, so a cell is tagged exactly when it could have been walked on."""
    flags = _openness(world)
    quiet = set(quiet)
    divide = _divide(world.w, spine)
    x0, y0, x1, y1 = CLANG_LOBE
    counts = {}
    for y in range(world.h):
        for x in range(world.w):
            if not flags[y][x]:
                world.g.set(x, y, 5, 0)
                continue
            if (x, y) in quiet:
                r = 0
            else:
                base = world.base(x, y)
                if base == SHINGLE and _by_sea(world, x, y):
                    r = REG_COAST
                elif base == SNOW:
                    r = REG_SNOW
                elif base == DESERT:
                    r = REG_DESERT
                elif y >= divide[x]:
                    r = REG_SOUTH
                elif x0 <= x < x1 and y0 <= y < y1:
                    r = REG_CLANG
                else:
                    r = REG_NORTH
            world.g.set(x, y, 5, r)
            counts[r] = counts.get(r, 0) + 1
    return counts


def _divide(width, spine):
    """The range's own latitude per column, so "north of the mountains" means
    north of *these* mountains rather than north of a number."""
    out = [spine[0][1]] * width
    for (ax, ay), (bx, by) in zip(spine, spine[1:]):
        for x in range(ax, min(bx, width - 1) + 1):
            out[x] = ay + (by - ay) * (x - ax) / max(1, bx - ax)
    for x in range(spine[-1][0], width):
        out[x] = spine[-1][1]
    return [int(round(v)) for v in out]


def _by_sea(world, x, y):
    for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1),
                   (x+1, y+1), (x-1, y-1), (x+1, y-1), (x-1, y+1)):
        if 0 <= nx < world.w and 0 <= ny < world.h and world.base(nx, ny) == SEA:
            return True
    return False


def point_at(world, have, also):
    """Add regions to the `regionSet` of every encounter entry that already
    names `have`, so a newly painted region is not an empty one.

    The nine entries came across from `Map008` in the map header `grow2.py`
    copied, troop ids and all, so this needs no access to the game's database -
    which is the point: the encounter *list* is `journey.py`'s to own and this
    only widens where its existing entries apply."""
    n = 0
    for e in world.map.get("encounterList") or ():
        if have in e["regionSet"]:
            e["regionSet"] = sorted(set(e["regionSet"]) | set(also))
            n += 1
    return n


# ---------------------------------------------------------------- the range --
# The 50x50 `Map008` as it was before this map replaced it. **Frozen, like
# `generated.json`, and for a sharper reason**: `Map008.json` in `data/` used to
# be the old world and is now the new one, so every reference to it as "the old
# map" silently started pointing at the output instead of the input the moment
# `journey.py` began loading `worldmap.json`. Two things read it that way -
# `old_events` below, whose result decides which squares the range is drawn
# around, and `decor.py`'s whole diff - and re-running `run_finish.py` after the
# install grew a range **106 cells different** from the committed one before
# anybody noticed. There is nowhere else this map exists now except git history.
OLD50 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "old50.json")


def old_events(path=None):
    """Every square the 50x50's own events stand on, on the new map.

    The generated world carries worldgen's door events and nothing else - the
    game's events were in `Map008.json` and arrive when the build script places
    them - so protecting `world.map["events"]` protects the wrong list, which is
    how the first draft buried the Barrow. It reads `old50.json` and not
    `data/Map008.json`; see `OLD50`."""
    m = json.load(open(path or OLD50))
    assert (m["width"], m["height"]) == (50, 50), \
        "%s is not the old 50x50" % (path or OLD50)
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
