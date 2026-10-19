"""The Obligatory Tower's floors, drawn as a tower (Mike, October 2026).

It was a cave: one level of rock carved into rooms with a long corridor up the
middle, which read as a dungeon underground rather than a building you climb.
Mike asked for it on the lighthouse's lines - floor above floor, the stairs on
each landing you up to the next - but much bigger, and less tidy inside, with
the way up in a different place on every floor and still consistent: a flight
climbed on one floor comes out above itself on the next.

So Map 11 is four floors side by side across one wide map, black between them
as the lighthouse has (`FLOOR_GAP` is more than half a screen, so none shows
from the edge of the next), and the summit is still Map 12, the fifth. Each
floor is a plan below, one character a cell:

    ' '  outside the tower: `Darkness`
    '#'  stone wall; `dungeon_walls` decides which of it is face
    '.'  floor
    ','  the floor, cracked
    '^'  the treads of the flight up, two wide and three deep, in the
         north wall of its room (`mapkit.stairs_up`); the plan walls the
         piers either side of it
    'v'  the top of the flight up from below, two wide and two deep
         (`mapkit.stairwell`), at the same x as that flight and two rows
         up, so its landing is over the wall the flight went into
    'x'  floor under rubble
    a-z  floor, with an event on it, named in `SPOTS`
    A-Z  wall, with an event on it

The events are `journey.tower_events`, which asks `at` where they are."""
import mapkit as K
import rmmzdata as R

FLOOR_W, FLOOR_H, FLOOR_GAP = 40, 30, 8

# Wall I (Stone) on the Dungeon sheet: grey dressed stone, which is a building
# and not a cave. The floor is `Cobblestones D`; `,` lays `Ground Cracks`
# over it.
WALL_TOP, WALL_FACE = K.A(96), K.A(104)
FLOOR = K.a5(23)
VOID = K.DG_VOID

PLANS = [
    # 1 - the hall. In by the door at the bottom, and up by the flight in the
    # north-east room, which the passage from the hall does not reach: the
    # way through it fell in, and the way round is through the east room.
    [
        "     ##############################     ",
        "    ################################    ",
        "   ##################################   ",
        "  ####################################  ",
        " #######...############################ ",
        "#####..........#########################",
        "#####..........###################N#####",
        "#####..........############...#^^#...###",
        "####...........############...#^^#...###",
        "####......................xx..#^^#...###",
        "#####.....................xx.........###",
        "#####..############..######..........###",
        "######.############..######.........####",
        "######.############..############..#####",
        "#####..############..############..#####",
        "###c.....##########..############..#####",
        "###......###...............###.......###",
        "###.....###.................##.......###",
        "##......##..................##........##",
        "##......##.................##.........##",
        "###....###...........................###",
        "###.....##...........................###",
        "###.........................##.....xx###",
        "####........................##......x###",
        "###......##.................##.......###",
        " ######.###.................##.......## ",
        "  #########......p..........##########  ",
        "   ################a#################   ",
        "    ###############e################    ",
        "     ##############################     ",
    ],
    # 2 - the guard floor: the barracks round the stairwell, three cells
    # behind bars along the corridor, a mess hall, the guard room, an armoury
    # that ends in a fall of stone, and the flight on up in the south-west
    # corner. A landing is open to the north, so the barracks has a row 3.
    [
        "     ##############################     ",
        "    ################################    ",
        "   ##################################   ",
        "  ########################........####  ",
        " ##......##...#...#...####....#..#....# ",
        "###......##...#...#...####....#vv#....##",
        "###......##===#===#===####....#vv#....##",
        "###......##===#===#===####....####....##",
        "###...........................####....##",
        "###...........................####....##",
        "###......########..#######............##",
        "###......########..########..........###",
        "###..,,..########..########..........###",
        "###.,xx,.###..............#..........###",
        "############..............#######..#####",
        "############..............#######..#####",
        "############..............#######..#####",
        "############..............###........###",
        "############..............###........###",
        "############.........................###",
        "###..#^^#..#.........................###",
        "###..#^^#..#..............###......c.###",
        "###..#^^#..#.........########........###",
        "###..................########........###",
        "###..................########........###",
        " ##........#.........########........## ",
        "  ####################################  ",
        "   ##################################   ",
        "    ################################    ",
        "     ##############################     ",
    ],
    # 3 - the chapel floor: a gallery along the north with the obelisk in
    # it, the west gallery behind it, the chapel with the basin, the crypt
    # along the south, and the flight on up in the east hall.
    [
        "     ##############################     ",
        "    ################################    ",
        "   ##################################   ",
        "  ####################################  ",
        " ##..........##......................## ",
        "###..........##......o...............###",
        "###..................................###",
        "###.c................................###",
        "###..........#####..####################",
        "###..........#####..####################",
        "##################..####################",
        "###############........#################",
        "###############........###^^#........###",
        "###..........##....b...###^^#........###",
        "###....................###^^#........###",
        "###....................##............###",
        "###..........##......................###",
        "###..#..#....##..................,,x.###",
        "###..#vv#....##........##........,xxx###",
        "###..#vv#....####################..#####",
        "###..####....####################..#####",
        "###..####....####################..#####",
        "###..####....#.......................###",
        "###..........,.......................###",
        "###..........,.......................###",
        " ##..........#.......................## ",
        "  ####################################  ",
        "   ##################################   ",
        "    ################################    ",
        "     ##############################     ",
    ],
    # 4 - the top floor: the landing, the library, the long hall along the
    # south that the roof came in on, the east gallery, and up the west
    # passage the antechamber with the barred door in its north wall.
    [
        "     ##############################     ",
        "    ################################    ",
        "   ##################################   ",
        "  ####################################  ",
        " ########D############################# ",
        "####.........k.################......###",
        "####...........###............#......###",
        "####...........###...................###",
        "####...........###...................###",
        "####...........###.......#..#.#......###",
        "####...........###.......#vv#.#......###",
        "#####..###########.......#vv#.#......###",
        "#####..#############.....####.#......###",
        "#####..#############.....####.#......###",
        "#####..#############.....####.#......###",
        "#####..#############..........#......###",
        "#####..###########............##########",
        "#####..###########............##########",
        "#####..###########............##########",
        "#####..###############..################",
        "#####..###############..################",
        "#####..###############..################",
        "###........,,,,............##........###",
        "###.......,,xx,,.....................###",
        "###........,,,,......................###",
        " ##........................##....c...## ",
        "  ####################################  ",
        "   ##################################   ",
        "    ################################    ",
        "     ##############################     ",
    ],
]

MAP_W = len(PLANS) * FLOOR_W + (len(PLANS) - 1) * FLOOR_GAP
MAP_H = FLOOR_H


def origin(floor):
    """Where floor `floor` (1 is the ground) starts on the map."""
    return (floor - 1) * (FLOOR_W + FLOOR_GAP)


def _cells(floor, ch):
    ox = origin(floor)
    return [(ox + x, y) for y, row in enumerate(PLANS[floor - 1])
            for x, c in enumerate(row) if c == ch]


def at(floor, ch):
    """The one cell on `floor` marked `ch` in its plan, in map coordinates."""
    cells = _cells(floor, ch)
    if len(cells) != 1:
        raise ValueError("floor %d has %d cells marked %r"
                         % (floor, len(cells), ch))
    return cells[0]


def _corner(floor, ch):
    cells = _cells(floor, ch)
    return min(cells, key=lambda c: (c[1], c[0])) if cells else None


def flight_up(floor):
    """(x, top tread) of the flight up from `floor`, or None on the top."""
    return _corner(floor, "^")


def well(floor):
    """(x, top tread) of the flight down from `floor`, or None on the
    ground. Its landing, where the stairs up from below put you, is the
    row above."""
    return _corner(floor, "v")


for _f in range(1, len(PLANS)):
    _up, _down = flight_up(_f), well(_f + 1)
    assert _down == (_up[0] + FLOOR_W + FLOOR_GAP, _up[1] - 2), (
        "floor %d's flight does not come out above itself" % _f)


def draw():
    """All four floors, walled, stepped and dressed, as a Canvas."""
    g = K.Canvas(MAP_W, MAP_H, tileset=K.TS_DUNGEON)
    g.fill(0, 0, MAP_W - 1, MAP_H - 1, 0, WALL_TOP)
    for f, plan in enumerate(PLANS, 1):
        ox = origin(f)
        for y, row in enumerate(plan):
            for x, c in enumerate(row):
                if c not in " #" and not c.isupper():
                    g.set(ox + x, y, 0, FLOOR)
    # Outside the tower is wall while the faces are worked out, so that the
    # tower's outer wall is all top: a wall shows a face only to the floor
    # below it, and the dark is not floor.
    g.dungeon_walls(WALL_TOP, WALL_FACE)
    outside = {(x, y) for x in range(MAP_W) for y in range(MAP_H)}
    for f, plan in enumerate(PLANS, 1):
        ox = origin(f)
        outside -= {(ox + x, y) for y, row in enumerate(plan)
                    for x, c in enumerate(row) if c != " "}
    for x, y in outside:
        g.set(x, y, 0, VOID)
    for f in range(1, len(PLANS) + 1):
        if flight_up(f):
            K.stairs_up(g, *flight_up(f), flight=K.DG_FLIGHT, step=K.DG_STEP)
        if well(f):
            K.stairwell(g, *well(f), wall_top=WALL_TOP, wall_face=WALL_FACE,
                        flight=K.DG_FLIGHT, step=K.DG_STEP)
    g.autotile(0)
    for f in range(1, len(PLANS) + 1):
        for x, y in _cells(f, ","):
            g.set(x, y, 1, CRACKS)
        for x1, y1, x2, y2 in RUGS.get(f, ()):
            g.fill(origin(f) + x1, y1, origin(f) + x2, y2, 1, RUG)
    g.autotile(1)
    for f in range(1, len(PLANS) + 1):
        for x, y in _cells(f, "x"):
            g.set(x, y, 3, RUBBLE[(x + y) % len(RUBBLE)])
        dress(g, f)
    return g


RUBBLE = (K.sf_tile("Dungeon_B", "Rubble"),
          K.sf_tile("Dungeon_B", "Rubble (Dirt)"))


def dress(g, floor):
    """The furniture of one floor, from `PROPS`, in plan coordinates."""
    ox = origin(floor)
    for x, y, z, piece in PROPS.get(floor, ()):
        if isinstance(piece, int):
            g.set(ox + x, y, z, piece)
        elif isinstance(piece[0], int):
            g.column(ox + x, y, z, piece)
        else:
            g.blit(ox + x, y, z, piece)


def _b(name):
    return K.sf_block("Dungeon_B", name)


def _c(name):
    return K.sf_block("Dungeon_C", name)


def _grid(block, w):
    return tuple(block[i:i + w] for i in range(0, len(block), w))


PILLAR = _b("Stone Pillar A")                   # two tall
PILLAR_BROKEN = _b("Broken Stone Pillar A")[0]
STATUE = _b("Statue")
DEMON = _b("Demon Statue")
OBELISK = _b("Obelisk")                         # three tall
MONUMENT = _b("Monument A")
BONES, BONES_B = _b("Bones A")[0], _b("Bones B")[0]
SKELETON = _grid(_b("Large Bones"), 2)
CRATE, BARREL = _b("Crate B (Stone)")[0], _b("Barrel A")[0]
POT, POT_B = _b("Pot A")[0], _b("Pot B")[0]
TABLE_RUIN, STOOL_RUIN = _b("Table (Ruins)")[0], _b("Stool (Ruins)")[0]
WEB = _b("Spider Web")[0]
DOORWAY = K.sf_tile("Dungeon_B", "Entrance C")  # behind the barred door
_BARS = _b("Jail Bars")
TAPESTRY = _c("Tapestry A")
WINDOW = _c("Window (Demon Castle)")
SHELF = _c("Bookshelf A")
SHELF_WIDE = _grid(_c("Bookshelf B"), 2)
BED, STRAW_BED = _c("Cheap Bed"), _c("Straw Bed")
TABLE, STOOL = _c("Table")[0], _c("Stool")[0]
HEXAGRAM = _grid(_c("Hexagram (Lit)"), 3)
COFFIN = _c("Coffin B (Top)")
CLOSET, DRAWERS = _c("Closet"), _c("Chest of Drawers")
CLOCK = _c("Clock")
SWORD_RACK = K.borrowed("Inside_C", "Sword Rack A")
SPEARS = K.borrowed("Inside_C", "Spears A")
SHIELD = K.borrowed("Inside_C", "Shield A")
ARMOUR = K.borrowed("Inside_C", "Armor A (Stand)")
SWORDS = K.borrowed("Inside_C", "Repository of Swords")
SCROLLS = K.borrowed("Inside_C", "Scrolls A")
BOOKS = K.borrowed("Inside_C", "Closed Books C")
OPEN_BOOK = K.borrowed("Inside_C", "Open Book A (V)")
HOURGLASS = K.borrowed("Inside_C", "Hourglass")
GLOBE = K.borrowed("Inside_C", "Globe")

# On layer 1, autotiled: the cracks in a ruined floor, and the runners.
CRACKS = K.A(23)                                # `Ground Cracks`
RUG = K.A(35)                                   # `Rug A`, red

# The runners, (x1, y1, x2, y2) in plan coordinates: up the hall from the
# door, and from the barred door down the antechamber.
RUGS = {
    1: [(18, 17, 20, 26)],
    4: [(8, 5, 10, 9)],
}


def bars(x, y, width):
    """A run of cell bars `width` wide from (x, y), two rows tall: the frame
    at each end, bars between."""
    top = (_BARS[0],) + (_BARS[1],) * (width - 2) + (_BARS[3],)
    foot = (_BARS[4],) + (_BARS[5],) * (width - 2) + (_BARS[7],)
    return (x, y, 3, (top, foot))


def _row(xs, y, z, piece):
    return [(x, y, z, piece) for x in xs]


# (x, y, layer, piece) in plan coordinates: a tile, a column (drawn down from
# y) or a block of rows (from its top-left). Walls hold windows only where
# the wall is the tower's own, on the north, with the sky behind it.
PROPS = {
    1: (
        # the NW room, the porter's: his table, his bed, his visitors
        [(6, 3, 3, WINDOW), (12, 3, 3, WINDOW), (9, 2, 3, TAPESTRY),
         (9, 7, 3, TABLE_RUIN), (10, 7, 3, TABLE_RUIN),
         (8, 7, 3, STOOL_RUIN), (11, 7, 3, STOOL_RUIN),
         (14, 5, 3, STRAW_BED), (5, 9, 3, BONES), (5, 5, 3, WEB),
         (13, 9, 3, POT)]
        # the crossroads, and the way through to the stairs that fell in
        + [(25, 10, 3, BONES_B), (16, 9, 3, PILLAR_BROKEN)]
        # the stair room
        + [(28, 5, 3, WINDOW), (35, 5, 3, TAPESTRY),
           (28, 10, 3, STATUE), (36, 10, 3, STATUE)]
        # the store room
        + [(4, 22, 3, CRATE), (5, 22, 3, CRATE), (4, 23, 3, CRATE),
           (3, 24, 3, BARREL), (4, 24, 3, BARREL), (8, 24, 3, POT),
           (7, 16, 3, BARREL), (8, 16, 3, POT_B), (2, 18, 3, CRATE),
           (2, 19, 3, POT)]
        # the hall: pillars, one of them down, the runner up from the door,
        # and the obelisks either side of the door
        + [(13, 18, 3, PILLAR), (25, 18, 3, PILLAR), (25, 22, 3, PILLAR),
           (13, 23, 3, PILLAR_BROKEN), (12, 24, 3, BONES_B),
           (16, 14, 3, TAPESTRY), (23, 14, 3, TAPESTRY),
           (17, 24, 3, OBELISK), (21, 24, 3, OBELISK)]
        # the east room, where the roof came in
        + [(31, 18, 3, SKELETON), (34, 24, 3, BONES), (32, 25, 3, PILLAR_BROKEN),
           (36, 16, 3, WEB)]
    ),
    2: (
        # the cells: somebody in each, still
        [bars(11, 6, 3), bars(15, 6, 3), bars(19, 6, 3),
         (12, 4, 3, BONES), (16, 4, 3, STRAW_BED), (19, 5, 3, BONES_B),
         (21, 4, 3, POT)]
        # the armoury, cleared out long ago, and its far end fallen in
        + [(4, 3, 3, SWORD_RACK), (6, 3, 3, SPEARS), (8, 3, 3, SHIELD),
           (3, 6, 3, ARMOUR), (3, 9, 3, ARMOUR), (8, 6, 3, SWORDS),
           (8, 10, 3, CRATE), (7, 12, 3, BONES_B)]
        # the barracks round the stairwell
        + _row((26, 28, 35, 37), 4, 3, BED)
        + _row((28, 30, 34, 36), 11, 3, BED)
        + [(27, 8, 3, DRAWERS), (37, 8, 3, CLOSET)]
        # the mess hall: two long tables, and benches of stools
        + _row(range(15, 23), 16, 3, TABLE) + _row(range(15, 23), 15, 3, STOOL)
        + _row(range(15, 23), 17, 3, STOOL)
        + _row(range(15, 22), 21, 3, TABLE_RUIN)
        + _row((15, 17, 18, 20), 20, 3, STOOL_RUIN)
        + _row((16, 19, 21), 22, 3, STOOL_RUIN)
        + [(13, 13, 3, BARREL), (14, 13, 3, BARREL), (25, 13, 3, CRATE),
           (14, 11, 3, TAPESTRY), (21, 11, 3, TAPESTRY)]
        # the guard room: lockers, a table, the rack
        + [(29, 17, 3, CLOSET), (30, 17, 3, CLOSET), (36, 17, 3, CLOCK),
           (32, 21, 3, TABLE), (33, 21, 3, TABLE), (31, 21, 3, STOOL),
           (34, 21, 3, STOOL), (36, 24, 3, SWORDS), (29, 25, 3, CRATE)]
        # the stair room
        + [(3, 20, 3, CRATE), (10, 20, 3, POT), (3, 25, 3, BARREL),
           (4, 25, 3, CRATE)]
    ),
    3: (
        # the west gallery: three statues and a window between each
        [(5, 4, 3, STATUE), (8, 4, 3, STATUE), (11, 4, 3, STATUE),
         (6, 2, 3, WINDOW), (10, 2, 3, WINDOW), (3, 9, 3, BONES)]
        # the long gallery: pillars down it, the obelisk of the forty-seven
        + _row((17, 25, 29, 33), 4, 3, PILLAR)
        + [(19, 2, 3, WINDOW), (27, 2, 3, WINDOW), (35, 2, 3, WINDOW),
           (21, 4, 3, MONUMENT), (23, 2, 3, TAPESTRY), (31, 2, 3, TAPESTRY)]
        # the chapel: a circle on the floor and the basin in the middle of it
        + [(18, 12, 1, HEXAGRAM), (15, 11, 3, DEMON), (22, 11, 3, DEMON),
           (16, 9, 3, TAPESTRY), (21, 9, 3, TAPESTRY)]
        # the vestry round the stairs
        + [(3, 13, 3, CLOSET), (4, 13, 3, DRAWERS), (12, 13, 3, CLOCK),
           (10, 25, 3, POT), (3, 23, 3, CRATE)]
        # the east hall: swords nobody came back for
        + [(30, 12, 3, SWORDS), (32, 12, 3, SWORDS), (34, 12, 3, SWORDS),
           (36, 15, 3, ARMOUR), (36, 17, 3, ARMOUR), (29, 17, 3, PILLAR)]
        # the crypt
        + _row((16, 19, 22, 25, 28, 31, 36), 22, 3, COFFIN)
        + [(17, 25, 3, BONES), (24, 25, 3, BONES_B), (30, 24, 3, SKELETON),
           (14, 22, 3, WEB)]
    ),
    4: (
        # the antechamber: the door up, a statue either side of it
        [(9, 4, 3, DOORWAY), (7, 5, 3, DEMON), (11, 5, 3, DEMON),
         (5, 3, 3, TAPESTRY),
         (13, 3, 3, TAPESTRY), (14, 9, 3, BONES)]
        # the landing
        + [(19, 6, 3, PILLAR), (24, 6, 3, PILLAR), (19, 16, 3, PILLAR),
           (28, 16, 3, PILLAR_BROKEN), (21, 4, 3, WINDOW), (26, 4, 3, WINDOW)]
        # the library
        + _row((31, 32, 33, 35, 36), 5, 3, SHELF)
        + [(32, 9, 3, SHELF_WIDE), (35, 9, 3, SHELF_WIDE),
           (32, 12, 3, SHELF_WIDE), (35, 12, 3, SHELF_WIDE),
           (34, 3, 3, WINDOW), (31, 14, 2, TABLE), (31, 15, 3, STOOL),
           (31, 14, 3, OPEN_BOOK), (36, 15, 3, GLOBE)]
        # the long hall, where the roof came in
        + [(7, 22, 3, PILLAR_BROKEN), (18, 23, 3, PILLAR_BROKEN),
           (3, 25, 3, BONES), (24, 25, 3, BONES_B), (20, 25, 3, PILLAR_BROKEN)]
        # the east gallery
        + [(30, 22, 3, STATUE), (36, 22, 3, STATUE), (30, 25, 3, POT)]
    ),
}


def stairs_events(first_id, map_id):
    """Up from each floor and down from the one above, both columns of each
    flight. Up is the top tread, to the landing above the well upstairs,
    facing on up; down is the well's top tread, to the bottom tread of the
    flight it came up, facing down - so turning round on the stairs takes you
    straight back."""
    evs = []

    def ev(name, x, y, to, d):
        evs.append(R.event(first_id + len(evs), name, x, y, [R.page(
            [R.play_se("Move1"), R.transfer(map_id, to[0], to[1], d, 0)],
            img=R.image(""), trigger=1, priority=0, through=True)]))
    for f in range(1, len(PLANS)):
        (x, y1), (wx, wy) = flight_up(f), well(f + 1)
        for i in (0, 1):
            ev("Stairs Up (%d)" % f, x + i, y1, (wx + i, wy - 1), 8)
        for i in (0, 1):
            ev("Stairs Down (%d)" % (f + 1), wx + i, wy, (x + i, y1 + 2), 2)
    return evs


# ================================================================ the summit ==
# Map 12, the fifth floor and the top of the stairs behind the barred door:
# one room, roofed - the Prophecy comes down out of its ceiling, and the
# bomb brings a piece of that ceiling down - with the throne on a dais at the
# north end and the stairs up from below arriving at the south, one wide.
SUMMIT_PLAN = [
    "    #################    ",
    "  #####################  ",
    " ####################### ",
    "#########################",
    "#####...............#####",
    "####.................####",
    "###...................###",
    "###...................###",
    "###...................###",
    "###...................###",
    "###...................###",
    "###...................###",
    "###...................###",
    "###...................###",
    "####.................####",
    "#####...............#####",
    "######.....#.#.....######",
    "############v############",
    "############v############",
    "#########################",
    " ####################### ",
    "  #####################  ",
    "    #################    ",
]
SUMMIT_W, SUMMIT_H = len(SUMMIT_PLAN[0]), len(SUMMIT_PLAN)
SUMMIT_WELL = min((x, y) for y, row in enumerate(SUMMIT_PLAN)
                  for x, c in enumerate(row) if c == "v")
SUMMIT_IN = (SUMMIT_WELL[0], SUMMIT_WELL[1] - 1)    # the landing, facing up
DAIS = K.a5(37)                                     # `Ground G (Demon Castle)`
THRONE = _grid(_c("Throne B (Demon Castle)"), 3)
PORTAL = _grid(_b("Large Monument")[:6], 3)         # where clause twelve lives


def summit_draw():
    g = K.Canvas(SUMMIT_W, SUMMIT_H, tileset=K.TS_DUNGEON)
    for y, row in enumerate(SUMMIT_PLAN):
        for x, c in enumerate(row):
            g.set(x, y, 0, WALL_TOP if c in " #" else FLOOR)
    g.fill(8, 4, 16, 8, 0, DAIS)
    g.dungeon_walls(WALL_TOP, WALL_FACE)
    for y, row in enumerate(SUMMIT_PLAN):
        for x, c in enumerate(row):
            if c == " ":
                g.set(x, y, 0, VOID)
    K.stairwell(g, *SUMMIT_WELL, width=1, wall_top=WALL_TOP,
                wall_face=WALL_FACE, flight=K.DG_FLIGHT, step=K.DG_STEP)
    g.autotile(0)
    g.fill(11, 9, 13, 15, 1, RUG)
    g.autotile(1)
    g.blit(11, 4, 3, PORTAL)
    g.blit(11, 7, 3, THRONE)
    for x, y, piece in [(9, 5, DEMON), (15, 5, DEMON),
                        (6, 6, PILLAR), (18, 6, PILLAR),
                        (6, 11, PILLAR), (18, 11, PILLAR),
                        (7, 2, WINDOW), (17, 2, WINDOW),
                        (9, 2, TAPESTRY), (15, 2, TAPESTRY)]:
        g.column(x, y, 3, piece)
    g.scatter([(5, 13), (19, 13)], 3, BONES)
    g.scatter([(4, 9), (20, 10)], 3, BONES_B)
    g.scatter([(8, 14), (16, 14)], 3, PILLAR_BROKEN)
    return g
