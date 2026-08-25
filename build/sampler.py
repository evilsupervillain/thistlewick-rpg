"""Throwaway: paint candidate tiles onto Map099 so a screenshot can settle what
they look like. Not part of the game; run it, look, then move on.

    python3 build/sampler.py walls | roofs | scenery | ground | world
    python3 build/sampler.py sf_walls | sf_yard | sf_ground | sf_props
    python3 build/sampler.py sf_fronts | sf_inside | sf_parlour
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mapkit as K
import rmmzdata as R

GAME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R.use_project(GAME)

MAP = 99


def grid(g, items, draw, cols=5, cell_w=6, cell_h=7, x0=1, y0=1):
    for n, item in enumerate(items):
        draw(g, x0 + (n % cols) * cell_w, y0 + (n // cols) * cell_h, item)


def walls():
    kinds = [52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63,
             64, 65, 66, 67, 70, 71, 72, 73, 74, 75, 76, 79]
    g = K.Canvas(32, 30)
    g.fill(0, 0, 31, 29, 0, K.GRASS)

    def draw(g, x, y, kind):
        g.building(x, y, 4, 5, wall=K.A(kind), roof=K.ROOF_BROWN)
    grid(g, kinds, draw, cols=6, cell_w=5, cell_h=6)
    g.autotile(0)
    return g, "A3 wall kinds 52..79, six per row"


def roofs():
    """Nine-slice whatever anchor you point at, including ones that are not
    real roofs - that is the point of a sampler. `Canvas.roof` refuses anything
    but the four proper anchors, so this draws the slice itself."""
    roofs_ = [K.ROOF_GREEN, K.ROOF_WHITE, K.ROOF_GOLD, K.ROOF_BROWN,
              (11, 0), (11, 3),
              (8, 6), (10, 6), (13, 6), (11, 6), (8, 9), (13, 9)]
    g = K.Canvas(32, 30)
    g.fill(0, 0, 31, 29, 0, K.GRASS)

    def draw(g, x, y, roof):
        col, row = roof
        for j in range(4):
            for i in range(4):
                cx = col if i == 0 else (col + 2 if i == 3 else col + 1)
                cy = row if j == 0 else (row + 2 if j == 3 else row + 1)
                g.set(x + i, y + j, 3, K.c_tile(cx, cy))
        g.fill(x, y + 4, x + 3, y + 5, 0, K.WALL_PLANK)
    grid(g, roofs_, draw, cols=6, cell_w=5, cell_h=7)
    g.autotile(0)
    return g, "Outside_C roof nine-slices"


def scenery():
    g = K.Canvas(34, 20)
    g.fill(0, 0, 33, 19, 0, K.GRASS)
    blocks = [K.TREE, K.TREE2, K.STALL, K.STALL2, K.TENT, K.PALM, K.DEAD_TREE]
    for n, b in enumerate(blocks):
        g.blit(1 + n * 4, 1, 3, b)
    singles = [K.BUSH, K.BUSH2, K.BUSH3, K.FLOWERS, K.FLOWERS2, K.FLOWERS3,
               K.ROCK, K.ROCK2, K.LOGS, K.BARREL, K.BARREL2, K.CRATE, K.POT,
               K.BUCKET, K.SIGNPOST, K.SIGNPOST2, K.CHIMNEY, K.PEBBLES,
               K.LILYPAD, K.MUSHROOMS, K.VINES, K.LADDER,
               K.DOORWAY_DARK, K.FENCE_RAIL]
    for n, t in enumerate(singles):
        g.set(1 + (n % 16) * 2, 5 + (n // 16) * 2, 3, t)
    pairs = [K.LAMP, K.STATUE_POST, K.WINDOW_FLOWERS, K.WINDOW_ARCH,
             K.WINDOW_GLASS, K.DOOR_WOOD, K.DOOR_DOUBLE]
    for n, p in enumerate(pairs):
        g.column(1 + n * 3, 10, 3, p)
    signs = [K.SIGN_BLADE, K.SIGN_ORB, K.SIGN_ARMOR, K.SIGN_RING, K.SIGN_POTION,
             K.SIGN_INN, K.SIGN_MUG, K.SIGN_PLATE, K.SIGN_WAND, K.SIGN_COIN,
             K.SIGN_HAMMER, K.SIGN_SUN]
    for n, s in enumerate(signs):
        g.set(1 + n * 2, 14, 3, s)
    g.autotile(0)
    return g, "scenery blocks, singles, pairs, shop signs"


def ground():
    g = K.Canvas(34, 20)
    tiles = [K.GRASS, K.PATH, K.COBBLE, K.PAVING, K.HEDGE, K.DECKING, K.SAND,
             K.WHEAT, K.SOIL, K.DARK_GRASS, K.WATER, K.CLIFF_TOP, K.REEDS]
    g.fill(0, 0, 33, 19, 0, K.GRASS)
    for n, t in enumerate(tiles):
        cx = 3 + (n % 5) * 7
        cy = 3 + (n // 5) * 7
        g.fill(cx - 2, cy - 2, cx + 2, cy + 2, 0, t)
    g.autotile(0)
    return g, "ground autotiles"


def world():
    """Candidate overworld landmarks from World_B, two tiles wide by three
    tall, laid on grass so the transparent parts read correctly."""
    g = K.Canvas(34, 26)
    g.fill(0, 0, 33, 25, 0, K.W_GRASS)
    picks = [(0, 10), (2, 10), (4, 10), (6, 10),
             (0, 12), (2, 12), (4, 12), (6, 12),
             (0, 14), (2, 14), (4, 14), (6, 14),
             (8, 0), (10, 0), (12, 0), (14, 0),
             (8, 2), (11, 2), (13, 2), (15, 2),
             (0, 3), (2, 3), (4, 3), (6, 3),
             (0, 0), (1, 0), (3, 0), (5, 1)]
    for n, (col, row) in enumerate(picks):
        cx = 1 + (n % 8) * 4
        cy = 1 + (n // 8) * 6
        for dy in range(3):
            for dx in range(2):
                g.set(cx + dx, cy + dy, 3, K.b_tile(col + dx, row + dy))
    g.autotile(0)
    return g, "World_B landmark blocks"


def sf_walls():
    """Every SF_Outside_A3 wall the north has a name for, drawn as a building
    so the wall autotile shapes and the roof over them both get exercised."""
    named = [(n, v) for n, v in sorted(vars(K).items())
             if n.startswith(("SF_WALL_", "SF_UPPER_"))]
    g = K.Canvas(32, 30, tileset=K.TS_CLANGING)
    g.fill(0, 0, 31, 29, 0, K.GRASS)

    def draw(g, x, y, item):
        g.building(x, y, 4, 5, wall=item[1], roof=K.SF_ROOF)
    grid(g, named, draw, cols=6, cell_w=5, cell_h=6)
    g.autotile(0)
    return g, "SF_Outside_A3: " + ", ".join(n for n, _ in named)


def sf_yard():
    """The A4 free-standing walls, each drawn as its top row plus two rows of
    face - which is the only way to tell whether the pair is really a pair."""
    pairs = [(n, v) for n, v in sorted(vars(K).items())
             if n.startswith("SF_YARD_") and not n.endswith("_TOP")]
    g = K.Canvas(34, 28, tileset=K.TS_CLANGING)
    g.fill(0, 0, 33, 27, 0, K.SF_WASTE)

    def draw(g, x, y, item):
        name, face = item
        top = getattr(K, name + "_TOP")
        g.fill(x, y, x + 2, y, 0, top)
        g.fill(x, y + 1, x + 2, y + 2, 0, face)
    grid(g, pairs, draw, cols=8, cell_w=4, cell_h=5)
    g.autotile(0)
    return g, "SF_Outside_A4: " + ", ".join(n for n, _ in pairs)


def sf_ground():
    named = [(n, v) for n, v in sorted(vars(K).items())
             if n.startswith(("SF_WASTE", "SF_METAL_FLOOR", "SF_CONCRETE",
                              "SF_GRID_FLOOR", "SF_DIRTY_FLOOR", "SF_COBBLE",
                              "SF_MECHA_FLOOR", "SF_WOOD_FLOOR", "SF_HOLE"))]
    g = K.Canvas(34, 20, tileset=K.TS_CLANGING)
    g.fill(0, 0, 33, 19, 0, K.GRASS)
    for n, (name, t) in enumerate(named):
        cx, cy = 3 + (n % 5) * 7, 3 + (n // 5) * 7
        g.fill(cx - 2, cy - 2, cx + 2, cy + 2, 0, t)
    g.autotile(0)
    return g, "SF_Outside_A5: " + ", ".join(n for n, _ in named)


def sf_props():
    """The street furniture, plus the two big C-sheet structures. Laid on
    Waste Land because that is what they will stand on in the town."""
    g = K.Canvas(34, 24, tileset=K.TS_CLANGING)
    g.fill(0, 0, 33, 23, 0, K.SF_WASTE)
    singles = [(n, v) for n, v in sorted(vars(K).items())
               if n.startswith(("SF_CHIMNEY", "SF_CRATE", "SF_BARREL",
                                "SF_MACHINE", "SF_AIR_VENT", "SF_VENT",
                                "SF_SMALL_FUEL", "SF_BROKEN_PILLAR",
                                "SF_IRON_FENCE_B", "SF_ROUND_CLOCK"))]
    for n, (name, t) in enumerate(singles):
        g.set(1 + (n % 16) * 2, 1, 3, t)
    columns = [K.SF_STACKED_CRATES, K.SF_PILLAR_MACHINE, K.SF_PILLAR_METAL,
               K.SF_PILLAR_BRICK, K.SF_IRON_FENCE_A, K.SF_WATER_TANK]
    for n, col in enumerate(columns):
        g.column(1 + n * 3, 4, 3, col)
    for n, t in enumerate(K.SF_METAL_FENCE):
        g.set(20 + n, 4, 3, t)
    # Sphere Machinery used to be sampled here and is now on the forbidden
    # list - it has a cyan console bolted to its right-hand cell. The water
    # tank in `columns` above is the boiler shape that survives the rule.
    # The Clock Tower at three rows and at six, to prove the shaft repeats and
    # the clock does not, and the plain roof as a nine-slice beside them.
    g.clock_tower(8, 12, h=3)
    g.clock_tower(12, 9, h=6)
    g.roof(16, 11, 4, 4, K.SF_ROOF)
    g.autotile(0)
    return g, "SF props: " + ", ".join(n for n, _ in singles)


def sf_fronts():
    """What goes on the front of a northern building.

    Tileset 5's B sheet is SF_Outside_B, so none of the Outside_B scenery
    exists up here and a street front has to be built out of signs, windows,
    shutters and ventilation instead. Four brick walls, eight candidates on
    each, drawn where they will actually live."""
    groups = [
        ("windows", list(K.SF_WINDOWS)),
        ("midsize windows", list(K.SF_WINDOWS_TALL)),
        ("signs", [K.SF_SIGN_WEAPON, K.SF_SIGN_ARMOR, K.SF_SIGN_ITEM,
                   K.SF_SIGN_PHARMACY, K.SF_SIGN_CAFE, K.SF_SIGN_INN,
                   K.SF_SIGN_BLANK, K.SF_WARNING_PLATE]),
        ("openings and fittings",
         [K.SF_ENTRANCE_A, K.SF_ENTRANCE_B, K.SF_SHUTTER, K.SF_EXHAUST_WALL,
          K.SF_WALL_POSTER, K.SF_AIR_INTAKE, K.SF_CANOPY, K.SF_WARNING_PLATE]),
    ]
    g = K.Canvas(34, 30, tileset=K.TS_CLANGING)
    g.fill(0, 0, 33, 29, 0, K.SF_WASTE)
    for gi, (_, items) in enumerate(groups):
        top = 1 + gi * 7
        g.crest(1, top, 32, K.SF_WALL_BRICK)
        g.building(1, top, 32, 5, wall=K.SF_WALL_BRICK, roof=K.SF_ROOF,
                   wall_rows=3)
        for n, item in enumerate(items):
            x = 2 + n * 4
            if isinstance(item, tuple):
                g.column(x, top + 2, 3, item)
            else:
                g.set(x, top + 3, 3, item)
    # The free-standing furniture, out in front of the walls where it goes.
    for n, item in enumerate([K.SF_SIGN_POST, K.SF_BENCH, K.SF_BENCH_B,
                              K.SF_PUMP, K.SF_POSTBOX, K.SF_DUMPSTER,
                              K.SF_WEEDS, K.SF_RUBBLE, K.SF_OIL_DRUM,
                              K.SF_OIL_DRUM_LEAK, K.SF_LADDER,
                              K.SF_FIRE_ESCAPE]):
        x = 2 + n * 2
        if isinstance(item, tuple) and len(item) == 2 and item == K.SF_BENCH:
            g.blit(x, 28, 3, (item,))
        elif isinstance(item, tuple) and item in (K.SF_BENCH_B,):
            g.blit(x, 28, 3, (item,))
        elif isinstance(item, tuple):
            g.column(x, 29 - len(item), 3, item)
        else:
            g.set(x, 28, 3, item)
    g.autotile(0)
    return g, "SF fronts: " + ", ".join(n for n, _ in groups)


def _inside_room(names, note, floor=None, wall=None, face=None):
    """Lay a list of `SF_IN_` props out on the floor of a real northern room,
    which is the only place their star flags and their two-tile shapes read
    correctly. Singles on one row, columns on the next, blocks below that."""
    g = K.interior(34, 26, 2, 4, 31, 22, door_x=16, tileset=K.TS_CLANGING_IN,
                   floor=floor or K.SF_CONCRETE,
                   wall_top=wall or K.SF_IN_WALL_FACTORY,
                   wall_face=face or K.SF_IN_FACE_FACTORY,
                   threshold=K.SF_THRESHOLD, outside=K.SF_THRESHOLD)
    g.autotile(0)
    # Which way a flat run of tiles goes is in the ids: neighbours on a sheet
    # differ by 1 across and by 8 down. Drawing a horizontal prop vertically
    # stacks three copies of the left-hand end of it, which is a misreading
    # that costs a screenshot to spot and looks deliberate.
    singles, runs, blocks = [], [], []
    for n in names:
        v = getattr(K, n)
        if isinstance(v, int):
            singles.append((n, v))
        elif any(isinstance(t, tuple) for t in v):
            blocks.append((n, v))
        elif len(v) > 1 and v[1] - v[0] == 1:
            blocks.append((n, (v,)))            # a horizontal run is one row
        else:
            runs.append((n, v))
    for i, (_, t) in enumerate(singles):
        g.set(3 + (i % 15) * 2, 5 + (i // 15) * 2, 2, t)
    for i, (_, col) in enumerate(runs):
        g.column(3 + (i % 15) * 2, 11 + (i // 15) * 3, 2, col)
    x = 3
    for _, block in blocks:
        if x + len(block[0]) > g.width - 3:
            x = 3
        g.blit(x, 18, 2, block)
        x += len(block[0]) + 1
    return g, note + ": " + ", ".join(n for n, _ in singles + runs + blocks)


def sf_in_walls():
    """Every SF_Inside_A4 wall pair the north has a name for, drawn as a real
    little room - a top row, two face rows, a floor and two side columns.

    Which is the only honest way to look at one: what you actually see of an
    interior wall is mostly the *top* autotile, in the side columns and along
    the horizontal runs, and a pair whose face is a fine warm rusted plate can
    still have a top like a public lavatory."""
    # `SF_IN_WALL_CLOCK` is a clock on a wall, not a wall - so the test is
    # whether the name has a matching `_FACE_`, not what it starts with.
    pairs = [(n, getattr(K, n)) for n in sorted(vars(K))
             if n.startswith("SF_IN_WALL_")
             and hasattr(K, n.replace("_WALL_", "_FACE_"))]
    g = K.Canvas(34, 28, tileset=K.TS_CLANGING_IN)
    g.fill(0, 0, 33, 27, 0, K.IN_VOID)

    def draw(g, x, y, item):
        name, top = item
        face = getattr(K, name.replace("_WALL_", "_FACE_"))
        g.fill(x, y, x + 4, y, 0, top)            # wall top, across
        g.fill(x + 1, y + 1, x + 3, y + 2, 0, face)
        g.fill(x + 1, y + 3, x + 3, y + 4, 0, K.SF_CONCRETE)
        for j in range(1, 5):                     # the side columns
            g.set(x, y + j, 0, top)
            g.set(x + 4, y + j, 0, top)
        g.fill(x, y + 5, x + 4, y + 5, 0, top)
    grid(g, pairs, draw, cols=6, cell_w=5, cell_h=7, x0=1, y0=1)
    g.autotile(0)
    return g, "SF_Inside_A4: " + ", ".join(n for n, _ in pairs)


def sf_floors():
    """The A5 interior floors, in patches, inside a room - because an interior
    floor is judged at room size and against a wall, not as a swatch."""
    names = ["SF_FLOOR_RESIN", "SF_FLOOR_TILE", "SF_FLOOR_DECO",
             "SF_FLOOR_WOOD", "SF_FLOOR_CARPET", "SF_FLOOR_MARBLE",
             "SF_FLOOR_LINO", "SF_CONCRETE", "SF_METAL_FLOOR",
             "IN_WOOD_FLOOR", "IN_COBBLE", "SF_DIRTY_FLOOR"]
    g = K.interior(34, 26, 2, 4, 31, 22, door_x=16, tileset=K.TS_CLANGING_IN,
                   floor=K.SF_CONCRETE, wall_top=K.SF_IN_WALL_PATTERN,
                   wall_face=K.SF_IN_FACE_PATTERN,
                   threshold=K.SF_THRESHOLD, outside=K.SF_THRESHOLD)
    for n, name in enumerate(names):
        cx, cy = 4 + (n % 6) * 5, 5 + (n // 6) * 8
        g.fill(cx, cy, cx + 4, cy + 6, 0, getattr(K, name))
    g.autotile(0)
    return g, "SF interior floors: " + ", ".join(names)


def sf_inside():
    """The works and the forge: everything with pressure in it."""
    names = ["SF_IN_MACHINE_C", "SF_IN_AIR_VENT", "SF_IN_RUBBLE",
             "SF_IN_PIPE_H", "SF_IN_VALVE",
             "SF_IN_AIR_VENT_A", "SF_IN_AIR_VENT_B", "SF_IN_VENT",
             "SF_IN_DRAIN", "SF_IN_PAPERS",
             "SF_IN_RUBBLE", "SF_IN_METAL_RUBBLE",
             "SF_IN_WARNING", "SF_IN_CHEST_WOOD",
             "SF_IN_CHEST_METAL", "SF_IN_DESK", "SF_IN_SIDE_DESK",
             "SF_IN_SIDE_DESK_METAL", "SF_IN_PIPE_V", "SF_IN_DUCT", "SF_IN_MECH_DEVICE",
             "SF_IN_BELT_H", "SF_IN_BELT_V", "SF_IN_GIRDER", "SF_IN_HANDRAIL",
             "SF_IN_STEEL_SHELF", "SF_IN_LOCKER", "SF_IN_STACKED_CRATES",
             "SF_IN_DESK_LARGE",
             "SF_IN_PLUMBING",
             "SF_IN_RUBBLE_PILE"]
    return _inside_room(names, "SF Inside: the works")


def sf_parlour():
    """The inn and the Parish Rooms: the two rooms up here with people in."""
    names = ["SF_IN_STOOL", "SF_IN_TABLE", "SF_IN_LAMP", "SF_IN_PICTURE", "SF_IN_PAINTING_A",
             "SF_IN_PAINTING_B", "SF_IN_POTTED_PLANT", "SF_IN_BULLETIN",
             "SF_IN_BOOK_STAND",
             "SF_IN_DOCUMENT", "SF_IN_MUG",
             "SF_IN_WINE", "SF_IN_BREAD", "SF_IN_MEAT", "SF_IN_CHICKEN",
             "SF_IN_PLATE", "SF_IN_PLATE_B", "SF_IN_TEAPOT", "SF_IN_FRUIT",
             "SF_IN_BOOK", "SF_IN_VASE", "SF_IN_SPIDER_WEB",
             "SF_IN_DRIPPING",
             "SF_IN_ARMCHAIR", "SF_IN_BED", "SF_IN_BED_IRON", "SF_IN_CURTAINS",
             "SF_IN_CURTAINS_B", "SF_IN_WINDOW", "SF_IN_WALL_CLOCK", "SF_IN_PLANT", "SF_IN_PARTITION",
             "SF_IN_BOOKSHELF", "SF_IN_DOC_SHELF", "SF_IN_DRAWERS",
             "SF_IN_ODDMENTS", "SF_IN_MEDICINE_SHELF", "SF_IN_DESK_LARGE_B",
             "SF_IN_FIREPLACE"]
    return _inside_room(names, "SF Inside: the parlour",
                        floor=K.IN_WOOD_FLOOR, wall=K.SF_IN_WALL_WOOD,
                        face=K.SF_IN_FACE_WOOD)


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "walls"
    g, note = {"walls": walls, "roofs": roofs, "scenery": scenery,
               "ground": ground, "world": world, "sf_walls": sf_walls,
               "sf_yard": sf_yard, "sf_ground": sf_ground,
               "sf_props": sf_props, "sf_fronts": sf_fronts,
               "sf_inside": sf_inside, "sf_parlour": sf_parlour,
               "sf_floors": sf_floors, "sf_in_walls": sf_in_walls}[which]()
    tileset = (K.TS_WORLD if which == "world" else
               K.TS_CLANGING_IN if which in ("sf_inside", "sf_parlour", "sf_floors", "sf_in_walls")
               else
               K.TS_CLANGING if which.startswith("sf_") else K.TS_OUTSIDE)
    m = K.new_map(g.width, g.height, tileset, name=note, bgm="")
    m["data"] = g.data
    R.save_map(MAP, m)
    infos = R.load("MapInfos.json")
    while len(infos) <= MAP:
        infos.append(None)
    infos[MAP] = {"id": MAP, "expanded": False, "name": "Sampler",
                  "order": MAP, "parentId": 0, "scrollX": 0, "scrollY": 0}
    R.save_list("MapInfos.json", infos)
    print("Map%03d: %s  (%dx%d)" % (MAP, note, g.width, g.height))


if __name__ == "__main__":
    main()


