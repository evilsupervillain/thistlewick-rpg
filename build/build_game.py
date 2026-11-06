"""Builds the whole of The Obligatory Quest from scratch.

    python3 build/build_game.py

Re-runnable: every record is written at its own id, so running it again
rewrites the game rather than piling up duplicates. This, and the modules it
calls, is the only place the game's content is authored - `data/*.json` is
output, not source.
"""
import copy
import math
import os
import re
import sys

GAME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GAME, "build"))

import mapkit  # noqa: E402  puts the workspace's tools/ on the path
import rmmzdata as R  # noqa: E402

R.use_project(GAME)

import db  # noqa: E402
import handdrawn  # noqa: E402
import curios  # noqa: E402
import field  # noqa: E402
import meadow  # noqa: E402
import journey  # noqa: E402
import north  # noqa: E402
import penultima  # noqa: E402
import restwell  # noqa: E402
import hithermost  # noqa: E402
import fairholme  # noqa: E402
import evermore  # noqa: E402
import gladhollow  # noqa: E402
import premises  # noqa: E402
import frayne  # noqa: E402
import frostwick  # noqa: E402
import coldbarrow  # noqa: E402
import sable_hart  # noqa: E402
import hamlets  # noqa: E402
import ashcombe  # noqa: E402
import weeping_bottom  # noqa: E402
import fenmarch  # noqa: E402
import collegium  # noqa: E402
import dunnage  # noqa: E402
import pottering  # noqa: E402
import mountain  # noqa: E402
import nomap  # noqa: E402,F401  world-map events only; journey reads SITES
import places  # noqa: E402
import q_corvin  # noqa: E402  draws COR-2's drowned street, Map 66
import q_roland  # noqa: E402  draws ROL-2's dungeon, Map 67
import q_spare  # noqa: E402  checks F1's gate against the built town
import quests  # noqa: E402  G0: the quest log, Quests.json and its plugin
import south  # noqa: E402
import village  # noqa: E402
import wilds  # noqa: E402


# In the editor's tree order, which is this list's order: Mike's, October 2026,
# with the places off the world map together and each town's own maps
# straight after it.
MAP_NAMES = [
    (village.MAP_VILLAGE, "Thistlewick", 0),
    (village.MAP_HOME, "Bram's House", village.MAP_VILLAGE),
    (village.MAP_HALL, "Prophecy Hall", village.MAP_VILLAGE),
    (village.MAP_INN, "The Gilded Turnip", village.MAP_VILLAGE),
    (village.MAP_CHAPEL, "Chapel of Whatever Works", village.MAP_VILLAGE),
    (village.MAP_SMITHY, "Grumnir's Smithy", village.MAP_VILLAGE),
    (village.MAP_STORE, "Nix's Emporium", village.MAP_VILLAGE),
    (journey.MAP_WORLD, "The World, Roughly", 0),
    (journey.MAP_GLOAMWOOD, "The Gloamwood", journey.MAP_WORLD),
    (journey.MAP_GLOAM_DEEP, "Gloamwood - The Bit With The Thing", journey.MAP_WORLD),
    (journey.MAP_TOWER, "The Obligatory Tower", journey.MAP_WORLD),
    (journey.MAP_SUMMIT, "The Obligatory Tower - Summit", journey.MAP_WORLD),
    (south.MAP_LIGHTHOUSE, "The Lighthouse of Saint Bother", journey.MAP_WORLD),
    (wilds.MAP_PIT, "The Bottomless Pit", journey.MAP_WORLD),
    (wilds.MAP_BARROW, "The Barrow of the Forty-Fourth", journey.MAP_WORLD),
    (field.MAP_LONG_FIELD, "The Long Field", journey.MAP_WORLD),
    (field.MAP_CRAG, "The Wreck of the One Hundred and Ninety-Ninth",
     journey.MAP_WORLD),
    (meadow.MAP_MEADOW, "Firstfield Meadow", journey.MAP_WORLD),
    (penultima.MAP_PENULTIMA, "Penultima", journey.MAP_WORLD),
    (penultima.MAP_SHOPPE, "Ye Final Shoppe",
     penultima.MAP_PENULTIMA),
    (restwell.MAP_RESTWELL, "Restwell", journey.MAP_WORLD),
    (restwell.MAP_EIGHT_HOURS, "The Eight Hours", restwell.MAP_RESTWELL),
    (hithermost.MAP_HITHERMOST, "Hithermost", journey.MAP_WORLD),
    (hithermost.MAP_CONTINUANCE, "Chapel of Continuance",
     hithermost.MAP_HITHERMOST),
    (fairholme.MAP_FAIRHOLME, "Fairholme", journey.MAP_WORLD),
    (fairholme.MAP_ROSAMUND, "Rosamund's Tower", fairholme.MAP_FAIRHOLME),
    (fairholme.MAP_LAIR, "Mrs Emberthwaite's Lair", journey.MAP_WORLD),
    (evermore.MAP_EVERMORE, "Olde Evermore", journey.MAP_WORLD),
    (evermore.MAP_ARCHIVE, "The Forbidden Archive", evermore.MAP_EVERMORE),
    (gladhollow.MAP_GLADHOLLOW, "Gladhollow", journey.MAP_WORLD),
    (gladhollow.MAP_MAYORS, "The Mayor's House", gladhollow.MAP_GLADHOLLOW),
    (premises.MAP_PREMISES, "The Former Premises", journey.MAP_WORLD),
    (frayne.MAP_FRAYNE, "Tobias Frayne's Cottage", journey.MAP_WORLD),
    (frostwick.MAP_FROSTWICK, "Frostwick", journey.MAP_WORLD),
    (frostwick.MAP_ELEVEN_DAYS, "The Eleven Days", frostwick.MAP_FROSTWICK),
    (frostwick.MAP_WORKING_GROUP, "The Working Group",
     frostwick.MAP_FROSTWICK),
    (frostwick.MAP_COLD_ROOM, "The Cold Room", frostwick.MAP_FROSTWICK),
    (coldbarrow.MAP_COLDBARROW, "The Chapter House", journey.MAP_WORLD),
    (sable_hart.MAP_SABLE_HART, "The Sable Hart", journey.MAP_WORLD),
    (hamlets.MAP_LITTLE_GORE, "Little Gore", journey.MAP_WORLD),
    (hamlets.MAP_SUMP, "Sump", journey.MAP_WORLD),
    (ashcombe.MAP_ASHCOMBE, "Ashcombe", journey.MAP_WORLD),
    (ashcombe.MAP_ASHCOMBE_IN, "Ashcombe, Indoors", ashcombe.MAP_ASHCOMBE),
    (weeping_bottom.MAP_WEEPING_BOTTOM, "Weeping Bottom", journey.MAP_WORLD),
    (weeping_bottom.MAP_WARD, "The Sisterhouse",
     weeping_bottom.MAP_WEEPING_BOTTOM),
    (fenmarch.MAP_FENMARCH, "Fenmarch Hall", journey.MAP_WORLD),
    (fenmarch.MAP_GALLERY, "The Long Gallery", fenmarch.MAP_FENMARCH),
    (collegium.MAP_COLLEGIUM, "The Great Court", journey.MAP_WORLD),
    (collegium.MAP_COLLEGIUM_LIBRARY, "The Library", collegium.MAP_COLLEGIUM),
    (collegium.MAP_COLLEGIUM_HALL, "The Hall", collegium.MAP_COLLEGIUM),
    (dunnage.MAP_DUNNAGE, "Great Dunnage", journey.MAP_WORLD),
    (dunnage.MAP_SMITHS_HALL, "The Smiths' Hall", dunnage.MAP_DUNNAGE),
    (dunnage.MAP_COUNTING_HOUSE, "The Counting House", dunnage.MAP_DUNNAGE),
    (dunnage.MAP_BONDED, "The Bonded Warehouse", dunnage.MAP_DUNNAGE),
    (dunnage.MAP_BELL, "The Bell", dunnage.MAP_DUNNAGE),
    (places.MAP_CULVERT, "The Bottom Lock", dunnage.MAP_DUNNAGE),
    (places.MAP_DROWNED_STREET, "Old Ashcombe", journey.MAP_WORLD),
    (places.MAP_CARN_DREY, "Under Carn Drey", journey.MAP_WORLD),
    ] + [(map_id, name, hithermost.MAP_HITHERMOST)
         for map_id, name in zip(places.MAP_STAIR, mountain.NAMES)] + [
    (places.MAP_BOTTOM, mountain.BOTTOM_NAME, places.MAP_STAIR[-1]),
    (places.MAP_POTTERING, "Much Pottering", journey.MAP_WORLD),
    (places.MAP_POTTERING_IN, "The Gotobeds' Cottage", places.MAP_POTTERING),
    (south.MAP_SOPPING, "Nether Sopping", 0),
    (south.MAP_WYVERN, "The Slain Wyvern", south.MAP_SOPPING),
    (places.MAP_WYVERN_UP, "The Slain Wyvern - Upstairs", south.MAP_WYVERN),
    (south.MAP_GUILD, "The Adventurers' Guild (Provisional)",
     south.MAP_SOPPING),
    (south.MAP_OUTFIT, "Wick & Barrow, Outfitters", south.MAP_SOPPING),
    (south.MAP_COTTAGE, "Number Forty-Five's Cottage", south.MAP_SOPPING),
    (places.MAP_FITCH, "Ambrose Fitch's Cottage", south.MAP_SOPPING),
    (north.MAP_CLANGING, "Upper Clanging", 0),
    (north.MAP_WORKS, "The Hoyle Works", north.MAP_CLANGING),
    (north.MAP_VALVE, "The Safety Valve", north.MAP_CLANGING),
    (north.MAP_FORGE, "Ollerenshaw's", north.MAP_CLANGING),
    (north.MAP_PARISH, "The Parish Rooms", north.MAP_CLANGING),
]


def build_map_infos():
    """Writes the map list, and drops anything not on it.

    Throwaway maps - the tile sampler, mostly - are written straight into
    `data/` while working, and would otherwise ship with the game. The build
    owns the map list, so it deletes any map it did not author."""
    infos = R.load("MapInfos.json")
    for order, (map_id, name, parent) in enumerate(MAP_NAMES, start=1):
        while len(infos) <= map_id:
            infos.append(None)
        infos[map_id] = {"id": map_id, "expanded": True, "name": name,
                         "order": order, "parentId": parent,
                         "scrollX": 0, "scrollY": 0}

    ours = {map_id for map_id, _, _ in MAP_NAMES}
    for map_id, info in enumerate(infos):
        if not info or map_id in ours:
            continue
        infos[map_id] = None
        stray = os.path.join(GAME, "data", "Map%03d.json" % map_id)
        if os.path.exists(stray):
            os.remove(stray)
            print("  dropped stray %s (%s)" % (os.path.basename(stray),
                                               info["name"]))
    while len(infos) > 1 and infos[-1] is None:
        infos.pop()
    R.save_list("MapInfos.json", infos)


# The one number that makes clause seven a rule of the engine rather than a
# line of dialogue. See NORTH.md 5.2, which was verified against the built
# data before this was written.
#
# `Game_Map.isAirshipLandOk` is `checkPassage(x, y, 0x0800) && checkPassage(x,
# y, 0x0f)`, and `checkPassage` reads the layers top down, skips star tiles,
# and **returns on the first tile it does not skip**. The Obligatory Tower's
# door is a B-sheet tile on layer 3 of Map 8 at (31, 8): tile 88, flagged
# 0x0600, which does not set 0x0800 - so it is consulted before the impassable
# castle wall underneath it, and it says yes. As the blank project ships it,
# **the airship can land on the front step of the tower.**
#
# Tile 88 is used exactly once in the whole 50x50 world map and Map 8 is the
# only map on tileset 1, so this is surgical. The approach tiles cannot be
# done and do not need doing: they are plain world grass, which is *the*
# landable ground for the entire island, and the road beside them already
# carries 0x0800 in its own flags. So the Two Hundred sets down on the grass
# two squares short and the party walks in, which is clause seven, enforced by
# the collision map.
TILESET_FLAGS = {
    1: {88: 0x0800},            # Overworld: the Obligatory Tower's door tile
}


# The tilesets whose A4 sheet is the walls of a room. On the outdoor ones A4
# is roofs and town walls, placed with deliberate shapes, so they are left out.
INTERIOR_TILESETS = {mapkit.TS_INSIDE, mapkit.TS_DUNGEON, mapkit.TS_CLANGING_IN}


def lay_frozen():
    """Every frozen map's tiles over whatever its builder drew. Runs after
    every module and before the passes that skip frozen maps.

    A builder that was rewritten round its frozen file (`HD.load`, "only the
    events are built here") comes out unchanged by this. Round seven (15 Oct
    2026) froze thirty maps at once, most of them still drawn by their
    generator, and this is how those are kept: the generator still runs, its
    tiles are replaced here, and its events - which are what the rest of the
    game points at - stand. Regions are derived, so a map that had them is
    repainted from the frozen tiles."""
    for map_id in sorted(handdrawn.frozen()):
        m = R.load_map(map_id)
        w, h = m["width"], m["height"]
        data = handdrawn.load(map_id, w, h, m["tilesetId"])
        if data[:w * h * handdrawn.LAYERS] == m["data"][:w * h * handdrawn.LAYERS]:
            continue
        regions = any(m["data"][w * h * 5:])
        g = R.MapGrid(w, h, data)
        if regions:
            mapkit.paint_regions(g, m["tilesetId"], 1)
        m["data"] = g.data
        R.save_map(map_id, m)


def shape_wall_tops():
    """Gives every interior's wall tops their edge shapes. Runs after every
    module, so it is the one place it happens.

    `mapkit.interior()` writes the ring round a room as `A(98)` - the A4
    wall-top autotile in shape 0, the middle of a solid block of wall - and
    no room builder re-shapes layer 0, because autotiling all of it would
    outline every square of a two-tone floor. Shape 0 is `0xe00` and blocks
    nothing; it is the edge shapes that carry the direction bit for their
    edge, so a ring left in shape 0 is a ring the player can walk round the
    top of. Only the A4 kinds are re-shaped, and the floor is not touched.
    Maps built another way are unchanged by it, because their walls are
    already in the shapes this computes.

    **The faces too** (October 2026). They were written in shape 0 as well,
    which on a face is a plank wall with no trim at all - no rail along its
    top, none along its foot - and nothing shaped them; Mike found it
    redrawing the Gilded Turnip in the editor. `shape_faces` is the editor's
    rule, which reproduces his walls there cell for cell."""
    for map_id, _, _ in MAP_NAMES:
        if map_id in handdrawn.frozen():
            continue                    # drawn by hand, walls and all
        m = R.load_map(map_id)
        if m["tilesetId"] not in INTERIOR_TILESETS:
            continue
        w, h = m["width"], m["height"]
        kinds = {R.autotile_kind(t) for t in m["data"][:w * h]
                 if t >= R.TILE_ID_A4 and not R.is_wall_autotile(t)}
        if not kinds:
            continue
        g = R.MapGrid(w, h, list(m["data"]))
        g.autotile(0, kinds=kinds)
        shape_faces(g)
        if g.data != m["data"]:
            m["data"] = g.data
            R.save_map(map_id, m)


def shape_faces(g):
    """Shape every A4 wall face on layer 0 the way the editor does: a rail
    along the top and foot wherever the face ends, and a post at a side only
    where the face stops against something that is not wall - so the north
    wall of a room runs into its side walls with no post, and the outside of
    the south wall has one either side of the doorway."""
    def wall(x, y):
        if not (0 <= x < g.width and 0 <= y < g.height):
            return True
        return R.TILE_ID_A4 <= g.get(x, y, 0) < R.TILE_ID_MAX
    faces = {R.autotile_kind(t) for t in g.data[:g.width * g.height]
             if R.TILE_ID_A4 <= t < R.TILE_ID_MAX and R.is_wall_autotile(t)}
    if not faces:
        return
    g.autotile(0, kinds=faces)
    for y in range(g.height):
        for x in range(g.width):
            t = g.get(x, y, 0)
            if not (R.is_autotile(t) and R.autotile_kind(t) in faces):
                continue
            shape = R.autotile_shape(t)
            for dx, bit in ((-1, 1), (1, 4)):
                if wall(x + dx, y):
                    shape &= ~bit
            g.set(x, y, 0, R.make_autotile(R.autotile_kind(t), shape))


# The plain tables of Inside_B - `Table D` (one cell) and `Table A` (two) -
# and what Mike put in their place in the Slain Wyvern (October 2026).
OLD_TABLES = {mapkit.IN_TABLE_WOOD, *mapkit.IN_TABLE[0]}
# Maps that keep the old tables: none yet. A map goes here when its tables
# are not tables - a counter, a desk - and look wrong joined up.
KEEP_OLD_TABLES = set()


def _rug_down(g, x, y):
    """A rug on layer 1 under a table that is moving onto layer 1: the whole
    rug - every cell of its kind joined to this one - goes down to layer 0,
    over the boards, which is where an A2 carpet can lie as well as on 1.
    Moving only the cell under the table would cut the rug's border in two.
    False when layer 1 holds something that is not an A2 floor."""
    t = g.get(x, y, 1)
    if not (R.TILE_ID_A2 <= t < R.TILE_ID_A3):
        return False
    kind = R.autotile_kind(t)
    todo, seen = [(x, y)], set()
    while todo:
        cx, cy = todo.pop()
        if (cx, cy) in seen or not (0 <= cx < g.width and 0 <= cy < g.height):
            continue
        c = g.get(cx, cy, 1)
        if not (R.is_autotile(c) and R.autotile_kind(c) == kind):
            continue
        seen.add((cx, cy))
        todo += [(cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)]
    for cx, cy in seen:
        g.set(cx, cy, 0, g.get(cx, cy, 1))
        g.set(cx, cy, 1, 0)
    g.moved_rugs = getattr(g, "moved_rugs", set()) | {kind}
    return True


def moved_rugs(g):
    return getattr(g, "moved_rugs", set())


def new_tables():
    """Every `Table D` and `Table A` on an Inside map becomes the A2 table,
    `mapkit.IN_TABLE_TOP`, which is what Mike chose for the Slain Wyvern:
    bigger, so what stands on it sits on the top instead of hanging off the
    edge, and an autotile, so tables side by side are one table. It goes on
    layer 1, where the sample's tables are, and what was on the table stays
    where it was. Runs after every module, so a table any room lays gets it;
    a cell whose layer 1 is already taken - a rug - keeps its old table and
    is reported, because a table cannot be laid on a rug that is on the
    same layer."""
    for map_id, _, _ in MAP_NAMES:
        if map_id in handdrawn.frozen() or map_id in KEEP_OLD_TABLES:
            continue
        m = R.load_map(map_id)
        if m["tilesetId"] != mapkit.TS_INSIDE:
            continue
        w, h = m["width"], m["height"]
        g = R.MapGrid(w, h, list(m["data"]))
        for y in range(h):
            for x in range(w):
                if g.get(x, y, 1) in OLD_TABLES:         # laid on layer 1
                    g.set(x, y, 1, mapkit.IN_TABLE_TOP)
                for z in (2, 3):
                    if g.get(x, y, z) not in OLD_TABLES:
                        continue
                    if g.get(x, y, 1) and not _rug_down(g, x, y):
                        print("  Map%03d (%d,%d): a table on something that "
                              "is not a rug, left as it was" % (map_id, x, y))
                        continue
                    g.set(x, y, z, 0)
                    g.set(x, y, 1, mapkit.IN_TABLE_TOP)
        g.autotile(0, kinds=moved_rugs(g))
        g.autotile(1, kinds=mapkit.TABLE_KINDS)
        if g.data != m["data"]:
            m["data"] = g.data
            R.save_map(map_id, m)


# The shadow layer's value for the left half of a cell: quarter bits 1 2 / 4 8.
SHADOW_LEFT = 1 | 4


def check_wide_pieces():
    """No two-wide cabinet cut in half (`mapkit.WIDE_PIECES`). The sheet's
    `.txt` names the halves as if they were whole shelves, so half of one is
    an easy thing to lay and looks, at map scale, like a shelf with its frame
    sawn through. Mike mended one in the Eleven Days (October 2026) and there
    were nine more. Frozen maps are checked too: a new half there is worth
    asking him about."""
    tilesets = R.load("Tilesets.json")
    bad = []
    for map_id, _, _ in MAP_NAMES:
        m = R.load_map(map_id)
        if tilesets[m["tilesetId"]]["tilesetNames"][5] != "Inside_B":
            continue
        bad += [(map_id,) + c for c in mapkit.lone_halves(m)]
    if bad:
        raise ValueError("half a two-wide cabinet (map, x, y, tile): %s"
                         % bad)


def cast_shadows():
    """Shadows every interior the way the sample's are: the left half of a
    cell whose west and north-west neighbours are both wall, if it is not wall
    itself. A wall is drawn seen from in front, so it darkens the floor below
    and to the right of it, and the top course casts nothing - which is why
    north-west is asked as well as west. That rule reproduces 83 of the
    sample's 99 interiors cell for cell (`../ROOMGEN2-CORPUS.md` 1.20); the
    rest are an author's hand. Runs after every module, like
    `shape_wall_tops`. Wall is any A4 tile on layer 0, top or face."""
    def is_wall(t):
        return R.TILE_ID_A4 <= t < R.TILE_ID_MAX
    for map_id, _, _ in MAP_NAMES:
        if map_id in handdrawn.frozen():
            continue                    # drawn by hand, walls and all
        m = R.load_map(map_id)
        if m["tilesetId"] not in INTERIOR_TILESETS:
            continue
        w, h = m["width"], m["height"]
        data = list(m["data"])

        def wall(x, y):
            return 0 <= x < w and 0 <= y < h and is_wall(data[y * w + x])
        for y in range(h):
            for x in range(w):
                cell = 4 * w * h + y * w + x
                if (data[cell] == 0 and not wall(x, y)
                        and wall(x - 1, y) and wall(x - 1, y - 1)):
                    data[cell] = SHADOW_LEFT
        if data != m["data"]:
            m["data"] = data
            R.save_map(map_id, m)


# The black opening a town door swings away from, by tileset. A `!Door1`
# sprite's open frames are see-through, so with nothing under it an opened
# door showed the wall it was painted on. The Outside sheet's is the tile the
# sample lays on layer 3 under every one of its `!Door1` events; SF Outside
# has its own.
DOORWAY = {
    mapkit.TS_OUTSIDE: mapkit.DOORWAY_DARK,
    mapkit.TS_COLLEGIUM: mapkit.DOORWAY_DARK,
    mapkit.TS_CLANGING: mapkit.sf_tile("SF_Outside_B", "Entrance A"),
    mapkit.TS_INSIDE: mapkit.IN_DOOR_OPENING,
}
# Doorways Mike draws himself, which `door_holes` leaves alone: Outside_B's
# `Entrance A`, the id before `DOORWAY_DARK` (`Entrance A (Extend)`) - the
# church door in Ashcombe, 23 October 2026.
DOORWAY_BY_HAND = {
    mapkit.TS_OUTSIDE: {mapkit.DOORWAY_DARK - 1},
    mapkit.TS_COLLEGIUM: {mapkit.DOORWAY_DARK - 1},
}


def dress_shut_doors():
    """Every event `story.shut` marked gets its door sprite on every page,
    and stops being Through. Runs after every module, so pages appended to
    a shut door from anywhere - NIX-3's on the Nether Sopping doors, ALD-2's
    on Weeping Bottom's chapel, the post-game's - are dressed too, and before
    `door_holes`, which then sees a door and lays the doorway under it. The
    doorway is open ground, so a door left Through would be walked into."""
    mark = re.compile(r"<shutdoor (\S+) (\d+) (\d+)>")
    for map_id, _, _ in MAP_NAMES:
        m = R.load_map(map_id)
        changed = False
        for ev in m["events"]:
            found = ev and mark.search(ev.get("note", ""))
            if not found:
                continue
            sheet, index, pattern = found.group(1), *map(int, found.groups()[1:])
            for p in ev["pages"]:
                p["image"] = R.image(sheet, index, direction=2, pattern=pattern)
                p["through"] = False
                p["directionFix"] = True
            changed = True
        if changed:
            R.save_map(map_id, m)


# The hearths with a fire in them (Mike, 31 Oct 2026): the firebox cell of each
# stock fireplace - the lower one, the middle of a three-wide - where somebody
# is at home, open or working. Not Ashcombe's oven, which shows no flame, and
# not Tobias Frayne's grate: he has been revived eleven times and he does not
# light fires. The Sable Hart and the Long Gallery build their own.
FIRES = {
    2: (10, 3),         # Bram's House
    4: (9, 3),          # the Gilded Turnip
    6: (11, 3),         # Grumnir's forge
    14: (14, 3),        # the Slain Wyvern
    17: (10, 3),        # Number Forty-Five's, by his sofa
    23: (15, 3),        # the Safety Valve
    24: (6, 3),         # Ollerenshaw's forge
    32: (11, 3),        # the Eight Hours
    45: (10, 3),        # the Eleven Days
    69: (5, 3),         # the Gotobeds'
}
FIREBOXES = {("Inside_B", n) for n in range(194, 200)} | \
    {("SF_Inside_C", n) for n in (179, 180, 181)}


def light_fires():
    """A fire in every hearth `FIRES` names: `!Flame` 3 facing up, the
    middle-sized fire set on the bottom of its cell, so it stands on the
    hearth instead of hanging 10px above it (Mike, 31 Oct 2026) - below
    characters, animated, no commands, so it neither blocks nor
    answers. Appended after every other event, so no id moves, and refused
    if the cell is not a fireplace, so a hearth moved in the editor is a
    failed build rather than a fire burning on the floor."""
    tilesets = R.load("Tilesets.json")
    for map_id, (x, y) in sorted(FIRES.items()):
        m = R.load_map(map_id)
        w, h = m["width"], m["height"]
        names = tilesets[m["tilesetId"]]["tilesetNames"]
        found = set()
        for z in (1, 2, 3):
            t = m["data"][(z * h + y) * w + x]
            if 0 < t < R.TILE_ID_E + 256:             # B-E only
                found.add((names[5 + t // 256], t % 256))
        assert found & FIREBOXES, "Map%03d (%d,%d) is not a hearth: %s" % (
            map_id, x, y, sorted(found))
        m["events"].append(R.event(len(m["events"]), "The Fire", x, y, [
            R.page([], img=R.image("!Flame", 3, direction=8), trigger=0,
                   priority=0, step_anime=True, direction_fix=True)]))
        R.save_map(map_id, m)


def _trope_guarded(page, later, i):
    """Whether the trope bump at `page["list"][i]` can only ever run once:
    the list turns on a switch or self switch that a later page is conditioned
    on, or the bump sits in a branch on a switch the list itself turns on
    (taken while it is off), or in one of `once_tropes`' own guards."""
    lst = page["list"]
    ss = {c["parameters"][0] for c in lst
          if c["code"] == 123 and c["parameters"][1] == 0}
    sw = set()
    for c in lst:
        if c["code"] == 121 and c["parameters"][2] == 0:
            sw.update(range(c["parameters"][0], c["parameters"][1] + 1))
    for q in later:
        k = q["conditions"]
        if (k["selfSwitchValid"] and k["selfSwitchCh"] in ss) or \
                (k["switch1Valid"] and k["switch1Id"] in sw) or \
                (k["switch2Valid"] and k["switch2Id"] in sw):
            return True
    ind = lst[i]["indent"]
    for j in range(i - 1, -1, -1):
        c = lst[j]
        if c["indent"] >= ind:
            continue
        ind, taken_if_on = c["indent"], True
        if c["code"] == 411:                    # the else of the 111 above it
            k = j - 1
            while not (lst[k]["code"] == 111 and lst[k]["indent"] == c["indent"]):
                k -= 1
            c, taken_if_on = lst[k], False
        if c["code"] != 111:
            continue
        p = c["parameters"]
        if p[0] == 12 and "'T:" in p[1]:
            return True
        if p[0] in (0, 2) and (p[1] in sw if p[0] == 0 else p[1] in ss) and \
                (p[2] == 0) != taken_if_on:     # the branch runs while it is off
            return True
    return False


def once_tropes():
    """`VAR_TROPES` counts jokes, once each, and the ending reads it back - but
    a prop's narration with `S.trope()` on the end, an inn's morning line, a
    sign, bumped it on every reading (found 31 Oct 2026; 46 of them). Every
    bump on a map that `_trope_guarded` cannot show runs once is wrapped in a
    self switch of its own, keyed on the text of the message just before it,
    so a joke told on two pages of one event is still one joke. No line of
    text changes, and a bump that was already once is left alone."""
    import hashlib
    wrapped = 0
    for map_id, *_ in MAP_NAMES:
        m = R.load_map(map_id)
        changed = False
        for e in m["events"]:
            if not e:
                continue
            for pi, page in enumerate(e["pages"]):
                lst = page["list"]
                bumps = [i for i, c in enumerate(lst) if c["code"] == 122 and
                         c["parameters"][:2] == [db.VAR_TROPES, db.VAR_TROPES]]
                for n, i in reversed(list(enumerate(bumps))):
                    if _trope_guarded(page, e["pages"][pi + 1:], i):
                        continue
                    text = []
                    for j in range(i - 1, -1, -1):
                        if lst[j]["code"] == 401:
                            text.insert(0, lst[j]["parameters"][0])
                        elif lst[j]["code"] == 101 and text:
                            break
                    seed = "\n".join(text) or "%d.%d" % (pi, n)
                    key = "T:" + hashlib.md5(seed.encode()).hexdigest()[:8]
                    sw = "[this._mapId, this._eventId, '%s']" % key
                    bump = dict(lst[i], indent=0)
                    lst[i:i + 1] = R.if_then(
                        R.condition_script("!$gameSelfSwitches.value(%s)" % sw),
                        [bump] + R.script(["$gameSelfSwitches.setValue(%s, true);" % sw]),
                        indent=lst[i]["indent"])
                    wrapped += 1
                    changed = True
        if changed:
            R.save_map(map_id, m)
    print("  once_tropes: %d trope bumps given a guard" % wrapped)


def door_holes():
    """Puts a dark doorway under every door sprite set in a town wall. Runs
    after every module, like `shape_wall_tops`, so a door added anywhere gets
    one.

    Only doors in a wall - A3 outside, A4 in: a gate in a fence opens onto
    grass, which is right. A door in a room's north wall is the Slain
    Wyvern's back door (Mike, October 2026: "should have a door opening
    behind it"), and its first page is the curtain over it, so every page is
    asked whether it is a door. The doorway goes on layer 3, as the sample's do, or on the highest
    layer still free - the Safety Valve has a canopy over its door on 3, and a
    star tile draws over the doorway whichever layer that is on. The tile is
    open (`0x600`), so the step through the opened door now really is a step
    into the doorway; the closed door still blocks the cell, being an event at
    "same as characters"."""
    for map_id, _, _ in MAP_NAMES:
        m = R.load_map(map_id)
        hole = DOORWAY.get(m["tilesetId"])
        if hole is None:
            continue
        w, h = m["width"], m["height"]
        data = list(m["data"])
        for ev in m["events"]:
            if not ev or not any(p["image"]["characterName"].startswith(
                    "!Door") for p in ev["pages"]):
                continue
            cell = ev["y"] * w + ev["x"]
            if not R.TILE_ID_A3 <= data[cell] < R.TILE_ID_MAX:
                continue
            if {hole, *DOORWAY_BY_HAND.get(m["tilesetId"], ())} & {
                    data[z * w * h + cell] for z in (1, 2, 3)}:
                continue                # drawn by hand already
            free = [z for z in (3, 2, 1) if data[z * w * h + cell] == 0]
            if not free:
                raise ValueError("Map%03d %s: no free layer for a doorway"
                                 % (map_id, ev["name"]))
            data[free[0] * w * h + cell] = hole
        if data != m["data"]:
            m["data"] = data
            R.save_map(map_id, m)


# The window drawn on the outside of an interior's south wall, by tileset:
# Inside_B's `Large Window A`, and on SF Inside the `Midsize Window A` Mike
# gave the Safety Valve.
# Frozen maps whose windows are Mike's and stay as drawn although the street
# disagrees: the Safety Valve's front has none, the Eleven Days' right-hand
# window is a cell nearer the door than the rule would put it, and the
# Gotobeds' front is a storey taller than the rule's rows. Frayne's Cottage
# (43) was a single tile outside that Mike drew a room for with liberties, and
# the Long Gallery (57) has its door at the left inside and in the middle
# outside, so he drew it as one end of a larger castle the player never sees.
WINDOWS_AS_DRAWN = {23, 43, 45, 57, 69}

OUTSIDE_WINDOW = {
    mapkit.TS_INSIDE: mapkit.IN_WINDOW,
    mapkit.TS_CLANGING_IN: (mapkit.b_tile(0, 2), mapkit.b_tile(0, 3)),
}


def _sheet_names(tileset):
    """{tile id: name} over a tileset's B-E sheets."""
    names = {}
    for slot, sheet in enumerate(R.load("Tilesets.json")[tileset]["tilesetNames"]):
        if slot >= 5 and sheet:
            for name, ids in mapkit.tile_names(sheet).items():
                for i in ids:
                    names[(slot - 5) * 256 + i] = name
    return names


def _street_windows(town, door, names):
    """The building a town door is in - the run of the same wall along the
    door's row, since a terrace is several houses in different walls - as
    (west end, east end), and the columns along it that have a window in
    either of its two rows. A window over the door itself is a fanlight and
    is not one of them."""
    w, h, d = town["width"], town["height"], town["data"]
    dx, dy = door
    kinds = {R.autotile_kind(d[dy * w + x]) for x in (dx - 1, dx + 1)
             if 0 <= x < w and R.TILE_ID_A3 <= d[dy * w + x] < R.TILE_ID_MAX}

    def wall(x):
        return (0 <= x < w and R.TILE_ID_A3 <= d[dy * w + x] < R.TILE_ID_MAX
                and R.autotile_kind(d[dy * w + x]) in kinds)
    x1 = x2 = dx
    while wall(x1 - 1):
        x1 -= 1
    while wall(x2 + 1):
        x2 += 1
    found = set()
    for x in range(x1, x2 + 1):
        for y in (dy - 1, dy):
            for z in (1, 2, 3):
                t = d[(z * h + y) * w + x]
                if 0 < t < R.TILE_ID_A5 and "window" in names.get(t, "").lower():
                    found.add(x)
    found.discard(dx)
    return x1, x2, sorted(found)


def _inside_windows(span, door, street, room):
    """Where the street's windows go on the inside of the south wall: each
    side of the door has the same windows the street front has on that side,
    each the same fraction of the way from the door to its end of the
    building, rounded towards the corner. That is Mike's own placing on
    Bram's House, the Gilded Turnip and Forty-Five's, all six windows of
    them. Windows side by side outside stay side by side, laid from the one
    nearest the corner."""
    (bx1, bx2), dx, (rx1, ix, rx2) = span, door, room
    out = set()
    runs = []
    for x in street:
        if runs and x == runs[-1][-1] + 1 and (x < dx) == (runs[-1][0] < dx):
            runs[-1].append(x)
        else:
            runs.append([x])
    for run in runs:
        if run[0] < dx:
            frac = (dx - run[0]) / float(dx - bx1)
            at = math.floor(ix - frac * (ix - rx1) + 1e-9)
            at = max(rx1, min(at, ix - len(run)))
            xs = range(at, at + len(run))
        else:
            frac = (run[-1] - dx) / float(bx2 - dx)
            at = math.ceil(ix + frac * (rx2 - ix) - 1e-9)
            at = min(rx2, max(at, ix + len(run)))
            xs = range(at - len(run) + 1, at + 1)
        out.update(xs)
    return sorted(out)


def match_windows():
    """Gives every interior's south wall the windows its building has on the
    street: Mike, October 2026, added Bram's House's "to match what is
    outside". The outside face of the south wall is the two face rows under
    the ring, which is the front of the building seen from the street.
    Frozen maps are drawn by hand and are left alone; what this would do to
    one is printed, for drawing in the editor."""
    town_cache = {}
    for map_id, _, _ in MAP_NAMES:
        m = R.load_map(map_id)
        window = OUTSIDE_WINDOW.get(m["tilesetId"])
        if window is None:
            continue
        w, h, d = m["width"], m["height"], m["data"]
        exits = []
        for ev in m["events"]:
            for page in (ev or {}).get("pages", [])[:1]:
                for c in page["list"]:
                    if c["code"] == 201 and c["parameters"][0] == 0:
                        exits.append((ev, c["parameters"][1:4]))
        for ev, (town_id, tx, ty) in exits:
            if town_id == map_id:
                continue
            if town_id not in town_cache:
                town_cache[town_id] = R.load_map(town_id)
            town = town_cache[town_id]
            if town["tilesetId"] in OUTSIDE_WINDOW:
                continue                # a stair or a back door, not the street
            doors = [(e["x"], e["y"]) for e in town["events"] if e and any(
                c["code"] == 201 and c["parameters"][:2] == [0, map_id]
                for p in e["pages"] for c in p["list"])]
            if not doors:
                continue
            door = min(doors, key=lambda c: abs(c[0] - tx) + abs(c[1] - ty))
            bx1, bx2, street = _street_windows(
                town, door, _sheet_names(town["tilesetId"]))
            ix, y2 = ev["x"], ev["y"] - 2

            def floor(x):
                t = d[y2 * w + x]
                return t and t != mapkit.IN_VOID and not (
                    R.TILE_ID_A4 <= t < R.TILE_ID_MAX)

            def face(x):
                return all(R.TILE_ID_A4 <= d[y * w + x] < R.TILE_ID_MAX
                           for y in (y2 + 2, y2 + 3))
            if not (0 <= y2 and y2 + 3 < h and floor(ix)):
                continue
            # The room's width is the south wall's, inside its corners: a
            # bedroom partitioned off the bar is still behind the same front.
            rx1 = rx2 = ix
            while rx1 > 1 and face(rx1 - 2):
                rx1 -= 1
            while rx2 < w - 2 and face(rx2 + 2):
                rx2 += 1
            want = [x for x in _inside_windows((bx1, bx2), door[0], street,
                                               (rx1, ix, rx2)) if face(x)]
            if map_id in handdrawn.frozen():
                have = [x for x in range(w) if d[(3 * h + y2 + 2) * w + x]
                        == window[0]]
                if have != want and map_id not in WINDOWS_AS_DRAWN:
                    print("  Map%03d is frozen; the street says windows at "
                          "x %s, row %d (it has %s)" % (map_id, want,
                                                        y2 + 2, have))
                break
            data = list(d)
            for x in range(rx1 - 1, rx2 + 2):
                for y, t in zip((y2 + 2, y2 + 3), window):
                    cell = (3 * h + y) * w + x
                    if data[cell] in window:
                        data[cell] = 0
                    if x in want:
                        data[cell] = t
            if data != d:
                m["data"] = data
                R.save_map(map_id, m)
            break


def build_tilesets():
    """`Tilesets.json` is the one data file this game inherits rather than
    authors, so the edits it needs are written here, by id, and OR-ed in - the
    build stays re-runnable and the diff stays one number wide."""
    tilesets = R.load("Tilesets.json")
    for tid, flags in TILESET_FLAGS.items():
        for tile_id, bits in flags.items():
            tilesets[tid]["flags"][tile_id] |= bits
    # SF Inside has no D or E sheet, and no anvil, hearth or coal anywhere on
    # the two it has - so Ollerenshaw's was a forge with a marble mantelpiece
    # in it. The stock Inside_B and Inside_C go into those empty slots with
    # tileset 3's flags for them, which changes nothing any existing map has
    # drawn; `mapkit.borrowed` names a tile on them.
    # Outside (tileset 2) takes `Inside_C` into its E slot the same way, for
    # the smithy's anvil out on the grass (HOB-3), so an `Inside_C` tile has
    # the same E id on both and `mapkit.borrowed` serves either. Dungeon
    # (tileset 4) takes it too, for the Obligatory Tower's basin and the
    # Pit's hamper, which had text and no tile (P2). This runs
    # before the copies below, so the Collegium's copy of 2 has it too, on
    # the first build as on every other.
    inside = tilesets[mapkit.TS_INSIDE]
    for tid, slot, sheet, src, dst in (
            (mapkit.TS_CLANGING_IN, 7, "Inside_B", R.TILE_ID_B, R.TILE_ID_D),
            (mapkit.TS_CLANGING_IN, 8, "Inside_C", R.TILE_ID_C, R.TILE_ID_E),
            (mapkit.TS_OUTSIDE, 8, "Inside_C", R.TILE_ID_C, R.TILE_ID_E),
            (mapkit.TS_DUNGEON, 8, "Inside_C", R.TILE_ID_C, R.TILE_ID_E)):
        tilesets[tid]["tilesetNames"][slot] = sheet
        tilesets[tid]["flags"][dst:dst + 256] = inside["flags"][src:src + 256]
    # This game's own D sheet (`tiles_d.py`, 30 Oct 2026): a doormat and a
    # crab's tracks and nets, which nothing in the box has. Outside's D
    # slot and World's were empty; all under characters, all open but the
    # nets (`mapkit.D_BLOCKED`).
    for tid in (mapkit.TS_OUTSIDE, mapkit.TS_WORLD):
        tilesets[tid]["tilesetNames"][7] = mapkit.SHEET_D
        tilesets[tid]["flags"][R.TILE_ID_D:R.TILE_ID_D + 256] = [0] * 256
        for t in mapkit.D_BLOCKED:
            tilesets[tid]["flags"][t] = 0x0F
    # Two copies of stock tilesets with one sheet swapped for a recoloured
    # one, rewritten whole each build after the flags above, so the flags
    # follow: the Collegium's purple roofs (`mapkit.TS_COLLEGIUM`) and the
    # world map with Fenmarch Hall's green ones (`mapkit.TS_OVERWORLD`).
    for tid, base, name, slot, sheet in [
            (mapkit.TS_COLLEGIUM, mapkit.TS_OUTSIDE, "Outside (Collegium)",
             6, "Outside_C_Collegium"),
            (mapkit.TS_OVERWORLD, mapkit.TS_WORLD, "Overworld (Thistlewick)",
             5, "World_B_Fenmarch")]:
        ts = copy.deepcopy(tilesets[base])
        ts.update(id=tid, name=name)
        ts["tilesetNames"][slot] = sheet
        tilesets[tid:tid + 1] = [ts]
    # Mike's floating island (P2; `worldmap/run_finish.ISLAND`), on the world
    # map's own copy only, so after the copy. The castle row, 240-241, is
    # ground: open and not a star, so the party stands on it and an airship
    # lands on it. The shadow row, 250-251, is drawn on the sea and was open
    # and not a star on the stock sheet - two cells of water a party could
    # set down on and walk about - so it becomes a star, and the sea decides.
    flags = tilesets[mapkit.TS_OVERWORLD]["flags"]
    for tile_id in (240, 241):
        flags[tile_id] &= ~0x10
    for tile_id in (250, 251):
        flags[tile_id] |= 0x10
    # The crest of a roof - the top row of its nine-slice - is a star tile on
    # every stock roof, so the engine ignores it for passage, the ground
    # under it decides, and a player on the street north of a house walks up
    # behind the ridge. From round 3 until October 2026 this made the crest
    # solid and not a star, which stopped that; Mike wants it back (October
    # 2026: "the top panel of the roofs cannot be walked behind anymore"),
    # so the crest is put back to the stock flags - a star, with the Outside
    # sheets' down bit, 0x611, and SF Outside's none, 0x610. Tilesets.json is
    # read back from data/, so it has to be written, not just left alone.
    # The street still goes under the crest, which is what the player stands
    # on there; a chimney on the crest is refused by `Canvas.chimney`, since
    # a star is drawn over it.
    for tid, roofs in mapkit.TILESET_ROOFS.items():
        flags = tilesets[tid]["flags"]
        crest = 0x610 if tid == mapkit.TS_CLANGING else 0x611
        for col, row in roofs:
            for i in range(3):
                flags[mapkit.c_tile(col + i, row)] = crest
    R.save_list("Tilesets.json", tilesets)


def build_system():
    system = R.load("System.json")

    # 251: QUESTS.md 0.6 reserves up to 250 for the companion quests.
    switches = [""] * 251
    for sid, name in [
            (db.SW_QUEST, "quest accepted"),
            (db.SW_LEFT_VILLAGE, "left the village"),
            (db.SW_GLOAMWOOD, "Gloamwood cleared"),
            (db.SW_GRIMSPITE, "Grimspite defeated"),
            (db.SW_WON, "the Prophecy annulled"),
            (db.SW_TOWER_OPEN, "tower door unbarred"),
            (db.SW_MIMIC, "met the mimic"),
            (db.SW_ROLAND_GONE, "the guest star had a prior engagement"),
            (db.SW_FEUD_JAR, "carrying the jar south"),
            (db.SW_FEUD_REPLY, "carrying the reply north"),
            (db.SW_FEUD_DONE, "the Thrupp sisters are speaking"),
            (db.SW_GUILD_ASKED, "Pell has explained Form A-1"),
            (db.SW_GUILD_FORM, "Form A-1 was under the mat"),
            (db.SW_GUILD_MEMBER, "registered adventurer"),
            (db.SW_BOUNTY_CRAB, "the crab is dealt with"),
            (db.SW_BOUNTY_CROOKE, "Crooke is dealt with"),
            (db.SW_CRAB_PAID, "crab bounty claimed"),
            (db.SW_CROOKE_PAID, "Crooke bounty claimed"),
            (db.SW_LAMP_ASKED, "Bother has asked for oil"),
            (db.SW_LAMP_LIT, "the lighthouse is lit"),
            (db.SW_PIT_ASKED, "Splint has explained the badger"),
            (db.SW_PIT_CLEARED, "the badger has left"),
            (db.SW_PIT_PAID, "Splint has paid up"),
            (db.SW_BARROW_OPEN, "the barrow has been entered"),
            (db.SW_BARROW_BEATEN, "the Forty-Fourth has stopped"),
            (db.SW_BENCH_ASKED, "he asked for a bench"),
            (db.SW_BENCH_DONE, "there is a bench on the mound"),
            (db.SW_HISTORY_ASKED, "Hosea wants six tales"),
            (db.SW_HISTORY_DONE, "the history is complete"),
            (db.SW_MET_QUY, "#45 said what to ask"),
            (db.SW_MET_46, "met #46 on his log"),
            (db.SW_SOUTH, "has been to Nether Sopping"),
            (db.SW_WYVERN, "knows about the goose"),
            (db.SW_NORTH, "has been to Upper Clanging"),
            (db.SW_TWO_HUNDRED_ASKED, "Ott has said what she needs"),
            (db.SW_OILSKIN_ASKED, "Ott wants forty bolts of oilskin"),
            (db.SW_OILSKIN_GOT, "the oilskin is bought"),
            (db.SW_SPAR_ASKED, "the main spar wants forging"),
            (db.SW_SPAR_DONE, "the main spar is forged"),
            (db.SW_AIRSHIP, "the Two Hundred flies"),
            (db.SW_ITEM_ONE_ASKED, "Ott has mentioned ITEM 1"),
            (db.SW_ITEM_ONE_DOWN, "ITEM 1 is off the crag"),
            (db.SW_84_BEATEN, "Attempt Eighty-Four has stopped"),
            (db.SW_84_REBUILT, "Attempt Eighty-Four is being rebuilt"),
            (db.SW_HOB_BRYD, "they went for a drink"),
            (db.SW_BALLAD_ASKED, "(unused - reserved, see NORTH.md 10)"),
            (db.SW_BALLAD_DONE, "verse seven was struck"),
            (db.SW_CENSUS, "heard about the Cold Winter"),
            (db.SW_COTTERILL, "met the Cotterills"),
            (db.SW_SPARE_ASKED, "Spare has applied to come along"),
            (db.SW_LONG_FIELD, "walked the Long Field"),
            (db.SW_CLAUSE_SEVEN, "Ott showed you clause seven"),
            (db.SW_ROOM_FOUR, "room four has not been down since Tuesday"),
            (db.SW_GERALD, "there was a Gerald"),
            (db.SW_TWO_HUNDRED_FLEW, "the Two Hundred set down by the tower"),
            (db.SW_TRAVELLERS, "the travellers said how long, exactly"),
            (db.SW_OTT_MATERIALS, "Ott asked you to ask about materials"),
            (db.SW_ITEM_ONE_USED, "ITEM 1 was used on the Dark Lord"),
            (db.SW_FF_ARRIVED, "Fizz has said HEY"),
            (db.SW_FF_STICK, "Firstfield: got a stick"),
            (db.SW_FF_SHEEP_ASKED, "Firstfield: the sheep are lost"),
            (db.SW_FF_SHEEP_DONE, "Firstfield: the sheep are found"),
            (db.SW_FF_CHEST, "Firstfield: opened the chest"),
            (db.SW_FF_NORBERT, "Firstfield: Norbert has lost"),
            (db.SW_FF_GRADUATED, "Firstfield: tutorial completed"),
            (db.SW_VISITORS_BOOK, "Hollowell wants the visitors' book signed"),
            (db.SW_SPARE_FORM, "Gudgeon has issued Form P-9"),
            (db.SW_SPARE_REFUSED, "Spare has lost the argument at least once")]:
        switches[sid] = name
    for actor_id, sid in db.SW_RECRUIT.items():
        switches[sid] = "recruited actor %d" % actor_id
    for actor_id, sid in db.SW_KNOWN.items():
        switches[sid] = "actor %d has been in the party before" % actor_id
    for actor_id, sid in db.SW_STORY.items():
        switches[sid] = "actor %d has had a story of their own" % actor_id
    for sid, name in [
            (db.SW_WRE2_ASKED, "WRE-2: Dorcas will read a second plaque"),
            (db.SW_WRE2_UP, "WRE-2: the second plaque is up"),
            (db.SW_WRE5_NAMED, "WRE-5: Bramus is named"),
            (db.SW_PIP2_DONE, "PIP-2: the ballad has its last verse"),
            (db.SW_MER2_ASKED, "MER-2: clause eleven, the blank form"),
            (db.SW_MER2_SCALES, "MER-2: the fish stall's scales lent"),
            (db.SW_MER2_DONE, "MER-2: Bram certified fit to travel"),
            (db.SW_ROL4_SEEN, "ROL-4: Hob has seen the maker's mark"),
            (db.SW_ROL4_REFIT, "ROL-4: the sword rehafted for Hob"),
            (db.SW_HOB5_FORGED, "HOB-5: the tube plate is made"),
            (db.SW_HOB5_DONE, "HOB-5: Ott says it will do"),
            (db.SW_ZEPH5_DONE, "ZEPH-5: page twenty-three"),
            (db.SW_MER4_TOLD, "MER-4: no twelfth time; the jar paid"),
            (db.SW_MER4_DONE, "MER-4: left, which is the cure"),
            (db.SW_HOB3_GONE, "HOB-3: the anvil is outside"),
            (db.SW_HOB3_DONE, "HOB-3: the anvil is back"),
            (db.SW_NIX4_BEGUN, "NIX-4: the eleven are out"),
            (db.SW_NIX4_DONE, "NIX-4: the ledger is ruled off"),
            (db.SW_NIX5_ON, "NIX-5: the escort is on (ends)"),
            (db.SW_NIX5_DONE, "NIX-5: through without a fight"),
            (db.SW_WRE3_WALK, "WRE-3: the society's walk is on (ends)"),
            (db.SW_WRE3_DONE, "WRE-3: the Thing proved not to exist"),
            (db.SW_PIP5_ASKED, "PIP-5: there is a box"),
            (db.SW_PIP5_SIGNED, "PIP-5: Form S-7 countersigned"),
            (db.SW_PIP5_KEY, "PIP-5: the key, while Fenn was listened to"),
            (db.SW_PIP5_DONE, "PIP-5: the box opened and shut"),
            (db.SW_HOB2_ON, "HOB-2: Beatrice is quiet (ends)"),
            (db.SW_HOB2_CARRYING, "HOB-2: an attempt is being carried (ends)"),
            (db.SW_HOB2_DONE, "HOB-2: the gate is hung"),
            (db.SW_ROL3_DINNER, "ROL-3: the alumni dinner is on (ends)"),
            (db.SW_ROL3_DONE, "ROL-3: the toast"),
            (db.SW_HOB1_ON, "HOB-1: the retrieval tour is on"),
            (db.SW_HOB1_PICKS, "HOB-1: Nix asked for the picks"),
            (db.SW_HOB1_DONE, "HOB-1: Beatrice disqualified"),
            (db.SW_ALD4_DONE, "ALD-4: Duchess found, and stays"),
            (db.SW_PIP3_ON, "PIP-3: the contest is on (ends)"),
            (db.SW_PIP3_DONE, "PIP-3: second place"),
            (db.SW_COR5_DONE, "COR-5: appraised; no curse"),
            (db.SW_NIX1_LETTER, "NIX-1: the client's letter opened"),
            (db.SW_NIX1_DONE, "NIX-1: the coat collected"),
            (db.SW_NIX2_OPEN, "NIX-2: the Door open, informally"),
            (db.SW_NIX2_DONE, "NIX-2: we spent it"),
            (db.SW_ROL1_ON, "ROL-1: the review meeting is on (ends)"),
            (db.SW_ROL1_DONE, "ROL-1: the minutes"),
            (db.SW_ZEPH1_ON, "ZEPH-1: the eleventh notice read"),
            (db.SW_ZEPH1_TOLD, "ZEPH-1: no expulsion; purse or draft"),
            (db.SW_ZEPH1_PAID, "ZEPH-1: the purse turned out"),
            (db.SW_ZEPH1_EXPELLED, "ZEPH-1: expelled, at her own request"),
            (db.SW_ZEPH1_DONE, "ZEPH-1: decided, either way"),
            (db.SW_ZEPH3_DONE, "ZEPH-3: the demonstration; everyone fine"),
            (db.SW_ZEPH2_ON, "ZEPH-2: inquorate; fetch the duck"),
            (db.SW_ZEPH2_WALKING, "ZEPH-2: the duck is walking (ends)"),
            (db.SW_ZEPH2_DONE, "ZEPH-2: quorate; the proxy"),
            (db.SW_WRE1_ON, "WRE-1: the monograph is on"),
            (db.SW_WRE1_MOTT, "WRE-1: reviewed by Mott"),
            (db.SW_WRE1_FURZE, "WRE-1: reviewed by Furze"),
            (db.SW_WRE1_DUCK_DUE, "WRE-1: the duck's review is due (ends)"),
            (db.SW_WRE1_DUCK, "WRE-1: reviewed by the duck"),
            (db.SW_WRE1_DONE, "WRE-1: published"),
            (db.SW_COR1_ON, "COR-1: on the Roll; today, then"),
            (db.SW_COR1_HOME, "COR-1: home, and the tea"),
            (db.SW_COR1_DONE, "COR-1: the speech; the scarf"),
            (db.SW_COR2_STEP, "COR-2: the doorstep; the sword's name"),
            (db.SW_COR2_DONE, "COR-2: the report card"),
            (db.SW_MER5_ON, "MER-5: the Water Committee re-formed"),
            (db.SW_MER5_DONE, "MER-5: the curse lifted; item three"),
            (db.SW_MER1_ON, "MER-1: the queue instead of the symposium"),
            (db.SW_MER1_DONE, "MER-1: on points; the Pamphlet"),
            (db.SW_MER3_ON, "MER-3: the Table is sitting"),
            (db.SW_MER3_DONE, "MER-3: write it down; the Table's Kit"),
            (db.SW_ALD3_DONE, "ALD-3: Knight Errant, At Large"),
            (db.SW_ALD1_DONE, "ALD-1: the letter delivered"),
            (db.SW_ALD5_DONE, "ALD-5: the Fourth squires for him"),
            (db.SW_ALD2_DONE, "ALD-2: the vigil kept; confirmed"),
            (db.SW_ALD6_DONE, "ALD-6: the Wrong Dragon, read to"),
            (db.SW_WRE4_ON, "WRE-4: engaged to authenticate"),
            (db.SW_WRE4_JOINS, "WRE-4: shown every join"),
            (db.SW_WRE4_DONE, "WRE-4: written up; the fee"),
            (db.SW_COR3_ON, "COR-3: seventeenth"),
            (db.SW_COR3_DONE, "COR-3: the meeting; his chair kept"),
            (db.SW_COR4_DONE, "COR-4: the third reading"),
            (db.SW_PIP4_ON, "PIP-4: the interviews (ends)"),
            (db.SW_PIP4_DONE, "PIP-4: the elegy, nine lines"),
            (db.SW_PIP1_ON, "PIP-1: the Authorised Version, read"),
            (db.SW_PIP1_GOOD, "PIP-1: very good; one footnote"),
            (db.SW_PIP1_FIXED, "PIP-1: fixed, A. & P. Quill"),
            (db.SW_PIP1_DONE, "PIP-1: the official account settled"),
            (db.SW_NIX3_ON, "NIX-3: Lorrimer's list (ends)"),
            (db.SW_NIX3_DONE, "NIX-3: won on paperwork"),
            (db.SW_HOB4_TRADED, "HOB-4: a gate for the gatepost"),
            (db.SW_HOB4_DONE, "HOB-4: one sword, not for Hob"),
            (db.SW_ZEPH4_DONE, "ZEPH-4: the Fen burnt; the road open"),
            (db.SW_ROL5_ON, "ROL-5: met the understudy; to tell her?"),
            (db.SW_ROL5_DONE, "ROL-5: told; she is at the tower door"),
            (db.SW_ROL2_ON, "ROL-2: gone to see, under Carn Drey"),
            (db.SW_ROL2_DRAWN, "ROL-2: the sword out of the stone"),
            (db.SW_ROL2_DONE, "ROL-2: the Worm ended; discharged"),
            (db.SW_SPA1_DONE, "SPA-1: read out at the dinner hour"),
            (db.SW_SPA1_DINNER, "SPA-1: the dinner hour (scene)"),
            (db.SW_SPA4_DONE, "SPA-4: met, and written to by hand"),
            (db.SW_SPA2_ASKED, "SPA-2: Cotter has asked"),
            (db.SW_SPA2_CLEARED, "SPA-2: the paddle is clear"),
            (db.SW_SPA2_DONE, "SPA-2: out, and everybody there"),
            (db.SW_GRIMSPITE_TEA, "P4: had the tea at the top"),
            (db.SW_COTTAGE_SEEN, "P4: been in Ambrose Fitch's cottage"),
            (db.SW_ROLAND_BACK, "P4: Roland rehired after the ending"),
            (db.SW_ROL5_LATE, "ROL-5: told after the ending"),
            (db.SW_DRAWN_LEFT, "ROL-2: the drawn sword handed on"),
            (db.SW_STAIR_IN, "P4d: through the Door into the Mountain"),
            (db.SW_CONTINUED, "P4d: back in through the chapel porch"),
            (db.SW_WARDEN, "P4d: the warden told it is not half way"),
            (db.SW_UNSCHEDULED, "P4e: Something Unscheduled, fought"),
            (db.SW_FORM_Z, "P4e: its bounty discharged on Form Z"),
            (db.SW_SPA3_LETTER, "SPA-3: the ninth letter, from the Stair"),
            (db.SW_SPA3_SPRING, "SPA-3: it is spring; all indoors"),
            (db.SW_SPA3_INSIDE, "SPA-3: Spare gone in with Bessie"),
            (db.SW_SPA3_DONE, "SPA-3: Washer; everybody back out"),
            (db.SW_SPA3_STEP, "SPA-3: Spare has told you on the step")]:
        switches[sid] = name

    variables = [""] * 40
    variables[db.VAR_COMPANIONS] = "companions recruited"
    variables[db.VAR_TROPES] = "tropes encountered"
    variables[db.VAR_TURNIPS] = "turnips eaten"
    variables[db.VAR_TALES] = "tales heard in the Slain Wyvern"
    variables[db.VAR_BOUNTIES] = "bounties claimed"
    variables[db.VAR_PLAQUES] = "wreck plaques read"
    variables[db.VAR_BLUSHES] = "things nobody quite said"
    variables[db.VAR_OTT_ORDER] = "Ott's beat, while the order is outstanding"
    variables[db.VAR_OTT_FLYING] = "Ott's beat, once the Two Hundred flies"
    variables[10] = "scratch: gold reallocated"
    variables[db.VAR_FF_STATIONS] = "Firstfield stations done"
    variables[db.VAR_FF_SHEEP] = "Firstfield sheep found"
    variables[db.VAR_FF_SIGNS] = "Firstfield signs read"
    variables[db.VAR_TOBY] = "Toby's delivery"
    variables[db.VAR_COMPANION_STORIES] = "companions with a story of their own"
    variables[db.VAR_MER2_WITNESS] = "MER-2: who witnessed it"
    variables[db.VAR_NIX4_RETURNED] = "NIX-4: returned, of eleven"
    variables[db.VAR_NIX5_BATTLES] = "NIX-5: battles when the escort set out"
    variables[db.VAR_PIP5_DECOY] = "PIP-5: who asked Fenn about clause twelve"
    variables[db.VAR_HOB2_TRY] = "HOB-2: attempts, of four"
    variables[db.VAR_ROL3_HEARD] = "ROL-3: alumni spoken to, of eleven"
    variables[db.VAR_HOB1_ASKED] = "HOB-1: owners asked, of eleven"
    variables[db.VAR_ZEPH1_PAID] = "ZEPH-1: crowns turned out in the Library"
    variables[db.VAR_WRE1_SPECIMENS] = "WRE-1: type specimens, of eleven"
    variables[db.VAR_MER1_POINTS] = "MER-1: Whatever Works' points"
    variables[db.VAR_PIP4_HEARD] = "PIP-4: accounts of Abel Thrush, of eleven"
    variables[db.VAR_NIX3_LOCATED] = "NIX-3: located with receipts, of three"
    variables[db.VAR_SPA1_POSTED] = "SPA-1: letters posted, of eight"
    variables[db.VAR_SPA1_ORDER] = "SPA-1: which went from where (digits)"
    variables[db.VAR_SPA4_TOUR] = "SPA-4: Effie's tour (4 is done)"
    variables[db.VAR_SPA2_PARTY] = "SPA-2: the party, set aside"
    variables[db.VAR_MOTHBALLS] = "P1: party steps when mothballs last used"
    variables[db.VAR_SPA3_ASKS] = "SPA-3: mornings he has asked"

    system.update({
        "gameTitle": "The Obligatory Quest",
        "startMapId": village.MAP_HOME,
        "startX": village.HOME_START[0], "startY": village.HOME_START[1],
        "editMapId": village.MAP_VILLAGE,
        "partyMembers": [db.BRAM],
        "testBattlers": [], "testTroopId": db.TR_TURNIPS,
        "optFollowers": True, "optSideView": True, "optDisplayTp": True,
        "optAutosave": False,
        # The title is lettered into the picture (Mike's, 5 Nov 2026), so the
        # engine must not draw it again over the top.
        "optDrawTitle": False,
        "switches": switches, "variables": variables,
        # WRE-3's badge is Wren's alone: a type of its own (QUESTS.md 0.5).
        "armorTypes": system["armorTypes"][:db.AT_BADGE] + ["Badge", "Rosette", "Coat", "Robe", "Scarf", "Pamphlet", "Escutcheon", "Washer"],
        # Spare's bag is a weapon type of its own, and his tantrum an element
        # his mother is immune to (QUESTS.md F1).
        "weaponTypes": system["weaponTypes"][:db.WT_BAG] + ["Bag"],
        "elements": system["elements"][:db.EL_TEMPER] + ["Temper"],
        # The blank project ships all three vehicles parked on map 1 at
        # coordinates from a tutorial map that is not in this game - the
        # airship at (154, 70), which is a hundred tiles off the east edge of
        # Thistlewick. That is inherited junk, not setup. The Two Hundred is
        # earned, so it starts on map 0, which is nowhere, and an event puts
        # it on the world map the day Ott hands it over.
        #
        # The *ship* carries the same junk (map 1, 142x69) and is left alone:
        # it is unreachable, unreferenced and invisible, and NORTH.md 8.2
        # sanctions the airship only.
        "airship": {"bgm": {"name": "Ship3", "pan": 0, "pitch": 100,
                            "volume": 90},
                    "characterName": "Vehicle", "characterIndex": 3,
                    "startMapId": 0, "startX": 0, "startY": 0},
        "title1Name": "Obligatory_Quest", "title2Name": "",
        # The menu goes down on the grass to the lower left, off Bram's face.
        "titleCommandWindow": {"background": 0, "offsetX": -270,
                               "offsetY": 70},
        "titleBgm": {"name": "Theme3", "pan": 0, "pitch": 100, "volume": 80},
        "battleBgm": {"name": "Battle2", "pan": 0, "pitch": 100, "volume": 85},
        "victoryMe": {"name": "Victory1", "pan": 0, "pitch": 100, "volume": 85},
        "defeatMe": {"name": "Defeat1", "pan": 0, "pitch": 100, "volume": 85},
        "gameoverMe": {"name": "Gameover1", "pan": 0, "pitch": 100, "volume": 85},
        "battleback1Name": "Grassland", "battleback2Name": "Grassland",
        "currencyUnit": "cr",
    })
    system["terms"]["basic"][8] = "EXP"
    R.save_object("System.json", system)


def main():
    # First, because `mapkit.paint_regions` reads passage off the tileset
    # flags on disk: run last, a change to them took two builds to settle.
    build_tilesets()
    db.build()
    village.build()
    journey.build()
    south.build()
    wilds.build()
    north.build()
    q_spare.check_family()             # F1's gate names north.py's ids
    field.build()
    meadow.build()
    penultima.build()
    restwell.build()
    hithermost.build()
    fairholme.build()
    evermore.build()
    gladhollow.build()
    premises.build()
    frayne.build()
    frostwick.build()
    coldbarrow.build()
    sable_hart.build()
    hamlets.build()
    ashcombe.build()
    weeping_bottom.build()
    fenmarch.build()
    collegium.build()
    dunnage.build()
    q_corvin.build()                    # COR-2's drowned street
    q_roland.build()                    # ROL-2's dungeon under Carn Drey
    pottering.build()                   # SPA-4's village, Maps 68-69
    q_spare.build()                     # SPA-2's culvert, Map 70
    mountain.build()                    # P4d: the Stair, Maps 73-77
    q_spare.check_couriers()            # F2's courier ids are the towns'
    lay_frozen()
    new_tables()
    shape_wall_tops()
    match_windows()
    dress_shut_doors()
    light_fires()
    curios.build()                      # CURIOS.md: things to look at
    once_tropes()
    door_holes()
    cast_shadows()
    check_wide_pieces()
    build_map_infos()
    build_system()
    q_spare.check_mornings()            # P4f: every bed calls the morning
    # P4d: the Stair's lamplight and continuance (POSTGAME.md 9).
    R.upsert_plugin(GAME, "TOQ_Mountain",
                    "The Stair under the mountain: a circle of lamplight, "
                    "and no Game Over.",
                    {"commonEvent": str(db.CE_CONTINUANCE),
                     "mapId": str(places.MAP_CONTINUANCE),
                     "x": str(mountain.PORCH[0]), "y": str(mountain.PORCH[1])})
    # The world map's biomes and the Tower's guard floor: `<battleback>` tags.
    R.upsert_plugin(GAME, "TOQ_Battlebacks",
                    "A battle background chosen by region, terrain or "
                    "column, from tags in a map's note.")
    quests.build(GAME)                  # G0: the quest log (QUESTS.md)

    print("built The Obligatory Quest")
    print("  %d maps, %d playable characters, %d skills"
          % (len(MAP_NAMES), len(db.CLASSES), len(R.load("Skills.json")) - 1))
    print("  start: Map%03d '%s' at %s"
          % (village.MAP_HOME, "Bram's House", village.HOME_START))


if __name__ == "__main__":
    main()
