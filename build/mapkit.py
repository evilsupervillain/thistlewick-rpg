"""Tile vocabulary and drawing helpers for The Obligatory Quest.

Everything here is named after what it looks like on screen, not after its tile
id, because tile ids are unreadable and the whole point of this file is that the
map scripts read like a description of the place.

The names were read off the labelled sheets that `tools/sheetgrid.py` produces
and then confirmed in a screenshot; anything unconfirmed says so.
"""
import os
import sys

WORKSPACE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(WORKSPACE, "tools"))

import rmmzdata as R

# ---------------------------------------------------------------- tilesets ---
TS_WORLD, TS_OUTSIDE, TS_INSIDE, TS_DUNGEON = 1, 2, 3, 4


def b_tile(col, row):
    """A tile on the B sheet, by its (column, row) on the 16x16 grid."""
    return (col // 8) * 128 + row * 8 + (col % 8)


def c_tile(col, row):
    return R.TILE_ID_C + b_tile(col, row)


def a5(n):
    """A plain, non-autotiling A5 tile by its index on that sheet."""
    return R.TILE_ID_A5 + n


def A(kind):
    """An autotile in its default shape; `MapGrid.autotile` fixes the shape up."""
    return R.make_autotile(kind, 0)


# ------------------------------------------------------- Outside_A2 ground ---
GRASS = A(16)
PATH = A(17)              # sandy dirt path over grass
COBBLE = A(18)            # grey cobblestone
PAVING = A(19)            # cut paving slabs
HEDGE = A(20)             # dense low shrub
DECKING = A(22)           # wooden decking
SAND = A(24)
WHEAT = A(28)             # yellow crop over grass - the turnip fields
SOIL = A(32)              # bare brown earth
DARK_GRASS = A(39)
WATER = A(1)              # Outside_A1: water with a grassy bank

# ------------------------------------------------------- Outside_A4 cliffs ---
CLIFF_TOP = A(116)        # grass plateau with a rocky rim
CLIFF_FACE = A(124)       # the earth wall below it

# -------------------------------------------------- Outside_A3 house walls ---
# A3 blocks are 16-shape wall autotiles, 8 kinds per sheet row from kind 48.
# All of these were confirmed in a rendered sampler.
WALL_SHINGLE = A(52)      # brown shingles, reads as a steep upper storey
WALL_THATCH = A(53)       # ragged dark thatch
WALL_LOG = A(54)          # stacked round logs
WALL_BLUE_TILE = A(55)
WALL_SANDBRICK = A(56)    # pale cream brick
WALL_PLASTER = A(57)      # plain tan plaster
WALL_BRICK_RED = A(58)
WALL_ICE = A(59)          # pale blue-white slabs
WALL_PLANK = A(60)        # mid-brown boards, laid horizontally
WALL_PLANK_LIGHT = A(61)  # honey-coloured boards
WALL_TIMBER = A(62)       # dark stained boards, laid vertically
WALL_BRICK_PURPLE = A(63)
WALL_BRICK_GREEN = A(64)
WALL_COLUMNS = A(65)      # white fluted columns
WALL_CONCRETE = A(66)
WALL_MOSSY = A(67)
WALL_STONE = A(72)        # grey ashlar
WALL_STONE_WHITE = A(73)
WALL_STONE_DARK = A(74)
WALL_MOSS_STONE = A(75)

# ---------------------------------------------------------- Outside_C roof ---
# Each roof is a nine-slice: (left column, top row) of a 3x3 block on Outside_C.
# There are exactly four, and they sit at columns 8-10 and 13-15 of rows 0-2 and
# 3-5. Columns 11-12 are *not* a fifth and sixth roof - they are spare hip and
# valley pieces for the green and gold blocks, with blank cells where the third
# column of a real block would be. A nine-slice anchored there straddles two
# different roofs and half of it is empty, which draws a building with a white
# band across it and a strip of somebody else's roof down one edge. Anchor a
# roof only at one of these four.
ROOF_GREEN = (8, 0)
ROOF_WHITE = (13, 0)      # snow-covered
ROOF_GOLD = (8, 3)
ROOF_BROWN = (13, 3)      # plain wooden roof - the village default
TOWER_STONE = (8, 6)      # a round stone tower, not a roof: 2 wide, 5 tall
TOWER_WHITE = (10, 6)

# ------------------------------------------------------ Outside_B scenery ----
TREE = ((b_tile(8, 6), b_tile(9, 6)), (b_tile(8, 7), b_tile(9, 7)))
TREE_DARK = ((b_tile(10, 6), b_tile(11, 6)), (b_tile(10, 7), b_tile(11, 7)))
STALL = ((b_tile(12, 6), b_tile(13, 6)), (b_tile(12, 7), b_tile(13, 7)))
STALL_FRUIT = ((b_tile(14, 6), b_tile(15, 6)), (b_tile(14, 7), b_tile(15, 7)))
# A market tent: 3 wide and 3 tall, with the awning poles down the outer
# columns. Drawn two columns wide it is a tent with one wall missing.
TENT = ((b_tile(5, 3), b_tile(6, 3), b_tile(7, 3)),
        (b_tile(5, 4), b_tile(6, 4), b_tile(7, 4)),
        (b_tile(5, 5), b_tile(6, 5), b_tile(7, 5)))
PALM = ((b_tile(12, 13),), (b_tile(12, 14),))

BUSH = b_tile(8, 3)
BUSH2 = b_tile(9, 3)
BUSH3 = b_tile(10, 3)
FLOWERS = b_tile(8, 4)            # white
FLOWERS2 = b_tile(9, 4)           # purple
FLOWERS3 = b_tile(10, 4)          # blue
ROCK = b_tile(11, 2)
ROCK2 = b_tile(12, 2)
LOGS = b_tile(12, 4)              # a stacked log pile
TUB = b_tile(11, 1)               # pale open tub
BARREL = b_tile(13, 1)
CRATE = b_tile(13, 2)
POT = b_tile(8, 2)                # round grey urn
BUCKET = b_tile(9, 2)
SIGNPOST = b_tile(9, 1)           # a fingerpost with two boards
FENCE_PANEL = b_tile(10, 1)       # a short slatted fence panel
STOVEPIPE = b_tile(8, 1)
LILYPAD = b_tile(15, 15)
MUSHROOMS = b_tile(11, 13)
BRAMBLES = b_tile(1, 6)
DEAD_BUSH = b_tile(11, 15)
DEAD_TREE = b_tile(8, 13)
DEAD_ROOTS = b_tile(8, 12)
LADDER = b_tile(2, 2)
REEDS = A(11)                     # A1 kind 11: tall green reeds

LAMP = (b_tile(0, 1), b_tile(0, 2))       # street lamp: lit head over its post

# Shop signs, hung on a wall above a door.
SIGN_BLADE = b_tile(1, 8)
SIGN_ORB = b_tile(2, 8)
SIGN_ARMOR = b_tile(3, 8)
SIGN_RING = b_tile(4, 8)
SIGN_POTION = b_tile(5, 8)
SIGN_INN = b_tile(6, 8)
SIGN_MUG = b_tile(7, 8)
SIGN_PLATE = b_tile(0, 9)
SIGN_WAND = b_tile(2, 9)
SIGN_COIN = b_tile(3, 9)
SIGN_HAMMER = b_tile(5, 9)
SIGN_SUN = b_tile(6, 9)

# On a house front, use DOOR_SHUT: a door that is closed reads as a building
# somebody lives in, and a bare black square reads as a hole the tiler left.
# DOORWAY_DARK is the inside of an opening and needs a frame drawn round it.
DOORWAY_DARK = b_tile(12, 0)      # flat black; only ever inside something
DOOR_SHUT = (b_tile(2, 14), b_tile(2, 15))       # closed boarded door, 2 tall
DOORWAY_ARCH = (b_tile(4, 14), b_tile(4, 15))    # tall arched black opening
WINDOW = b_tile(0, 12)            # window with a flower box
WINDOW_GLASS = (b_tile(3, 14), b_tile(3, 15))    # stained glass, 2 tall
DOOR_DOUBLE = (b_tile(2, 14), b_tile(2, 15))     # grand double doors, 2 tall

# ------------------------------------------------- Inside tileset (id = 3) ---
IN_WOOD_FLOOR = A(16)
IN_COBBLE = A(17)
IN_DARK_WOOD = A(24)
IN_RED_CARPET = A(26)
IN_SANDSTONE = A(37)
IN_DIAMOND_TILE = A(41)
IN_PARQUET = A(32)
IN_BRICK_FLOOR = A(25)
IN_PURPLE_RUG = A(35)
IN_GREEN_RUG = A(27)
IN_BLUE_RUG = A(34)
IN_RED_RUG = A(42)
# Wall top and wall face come in matched pairs on Inside_A4: the tops are the
# even block-rows (48-shape) and the faces the odd ones (16-shape).
IN_WALL_TOP = A(98)               # dark wood panelling, the village default
IN_WALL_FACE = A(104)
IN_WALL_TOP_PLANK, IN_WALL_FACE_PLANK = A(97), A(105)
IN_WALL_TOP_STONE, IN_WALL_FACE_STONE = A(80), A(88)
IN_WALL_TOP_TAN, IN_WALL_FACE_TAN = A(81), A(89)
IN_WALL_TOP_WHITE, IN_WALL_FACE_WHITE = A(101), A(109)
IN_WALL_TOP_RED, IN_WALL_FACE_RED = A(85), A(93)
IN_WALL_TOP_GOLD, IN_WALL_FACE_GOLD = A(86), A(94)
IN_WALL_TOP_PURPLE, IN_WALL_FACE_PURPLE = A(116), A(124)
IN_VOID = a5(0)                   # plain black

# Inside_B furniture. Vertical pairs/triples are drawn with `Canvas.column`,
# rectangular blocks with `Canvas.blit`, single tiles with `set`.
IN_BED = (b_tile(8, 5), b_tile(8, 6))          # blue blanket, 1 wide 2 tall
IN_BED_ORANGE = (b_tile(9, 5), b_tile(9, 6))
IN_BED_BROWN = (b_tile(11, 5), b_tile(11, 6))
IN_BOOKCASE = (b_tile(14, 3), b_tile(14, 4))   # shelf of books
IN_BOOKCASE2 = (b_tile(15, 3), b_tile(15, 4))
IN_CURTAIN_GREEN = (b_tile(2, 8), b_tile(2, 9))
IN_SHELF_JARS = (b_tile(9, 3), b_tile(9, 4))   # pots and crockery
IN_SHELF_BOTTLES = (b_tile(11, 3), b_tile(11, 4))
IN_SHELF_FRUIT = (b_tile(10, 3), b_tile(10, 4))
IN_SHELF_GOODS = (b_tile(8, 3), b_tile(8, 4))  # sacks and loaves
IN_CABINET = (b_tile(8, 2), b_tile(8, 3))
IN_DRESSER = (b_tile(10, 2), b_tile(10, 3))
IN_COUNTER = b_tile(9, 3)                      # a plain wooden counter top
IN_PILLAR = (b_tile(0, 3), b_tile(0, 4), b_tile(0, 5))
IN_FIREPLACE = ((b_tile(13, 7), b_tile(14, 7), b_tile(15, 7)),
                (b_tile(13, 8), b_tile(14, 8), b_tile(15, 8)))
IN_PIANO = ((b_tile(13, 9), b_tile(14, 9), b_tile(15, 9)),)
IN_ORGAN = ((b_tile(13, 10), b_tile(14, 10), b_tile(15, 10)),
            (b_tile(13, 11), b_tile(14, 11), b_tile(15, 11)),
            (b_tile(13, 12), b_tile(14, 12), b_tile(15, 12)))
IN_TABLE_ROUND = b_tile(14, 13)
IN_TABLE_SMALL = b_tile(15, 13)
IN_POT = b_tile(13, 13)
IN_CRATE = b_tile(8, 12)
IN_CRATE2 = b_tile(9, 12)
IN_BARREL = b_tile(10, 10)
IN_BARREL2 = b_tile(11, 10)
IN_SACK = b_tile(8, 10)
IN_SACK2 = b_tile(9, 10)
IN_SOFA = ((b_tile(0, 12), b_tile(1, 12), b_tile(2, 12), b_tile(3, 12)),
           (b_tile(0, 13), b_tile(1, 13), b_tile(2, 13), b_tile(3, 13)))
IN_CURTAIN_RED = (b_tile(1, 6), b_tile(1, 7))
IN_WINDOW = (b_tile(4, 8), b_tile(4, 9))
IN_STAINED_GLASS = (b_tile(7, 8), b_tile(7, 9))
IN_SWORD_RACK = (b_tile(2, 10), b_tile(2, 11))
IN_NOTICE_BOARD = (b_tile(3, 10), b_tile(3, 11))
IN_CLOCK = (b_tile(4, 14), b_tile(4, 15))
IN_MIRROR = (b_tile(6, 14), b_tile(6, 15))
IN_THRONE = (b_tile(7, 12), b_tile(7, 13))
IN_RAILING = b_tile(12, 14)
IN_STOVE = (b_tile(10, 7), b_tile(10, 8))
IN_KITCHEN = (b_tile(8, 8), b_tile(8, 9))

# Inside_C: the small things that sit on top of furniture.
INC_BOOK = c_tile(0, 8)
INC_BOOK2 = c_tile(4, 8)
INC_SCROLL = c_tile(0, 9)
INC_SCROLL2 = c_tile(5, 9)
INC_CANDLES = c_tile(2, 10)
INC_PLANT = c_tile(4, 10)
INC_PLANT2 = c_tile(6, 10)
INC_CHEST_PROP = c_tile(0, 11)
INC_POTION_BLUE = c_tile(4, 12)
INC_POTION_GREEN = c_tile(5, 12)
INC_POTION_RED = c_tile(6, 12)
INC_FRUIT = c_tile(0, 13)
INC_BASKET = c_tile(2, 13)
INC_BOTTLE = c_tile(0, 3)
INC_BOTTLES = c_tile(2, 3)
INC_GOBLET = c_tile(1, 1)
INC_MEAL = c_tile(0, 5)
INC_MEAL2 = c_tile(2, 5)
INC_ARMOR_STAND = c_tile(4, 14)
INC_LAMP = c_tile(6, 13)
INC_BELL = c_tile(0, 15)

# ------------------------------------------------ Dungeon tileset (id = 4) ---
# Read off the sample project's Cave B1, which is the reference for how a cave
# is actually tiled: solid rock is the wall *top*, and the two rows directly
# above any floor tile are the wall *face*.
DG_FLOOR = A(16)
DG_FLOOR2 = A(18)
DG_WALL_TOP = A(80)
DG_WALL_FACE = A(88)
DG_VOID = a5(0)

DGB_GATE = ((b_tile(2, 0), b_tile(3, 0)), (b_tile(2, 1), b_tile(3, 1)),
            (b_tile(2, 2), b_tile(3, 2)), (b_tile(2, 3), b_tile(3, 3)))
DGB_PORTAL = (b_tile(3, 8), b_tile(3, 9))
DGB_OBELISK = (b_tile(0, 8), b_tile(0, 9))
DGB_MONUMENT = (b_tile(1, 8), b_tile(1, 9))
DGB_STATUE_ANGEL = (b_tile(0, 10), b_tile(0, 11))
DGB_STATUE_DEMON = (b_tile(6, 10), b_tile(6, 11))
DGB_PILLAR = (b_tile(0, 12), b_tile(0, 13))
DGB_PILLAR_WHITE = (b_tile(3, 12), b_tile(3, 13))
DGB_LADDER = b_tile(4, 1)
DGB_ROCK = b_tile(0, 4)
DGB_RUBBLE = b_tile(0, 15)
DGB_BONES = b_tile(2, 15)
DGB_SKULLS = b_tile(1, 15)
DGB_CRYSTAL_PURPLE = (b_tile(5, 5), b_tile(5, 6), b_tile(5, 7))
DGB_BARRICADE = b_tile(6, 15)

# ------------------------------------------------- World tileset (id = 1) ----
# A world map is built in two layers, the way the sample's is: layer 0 carries
# the base terrain (sea, grass, sand, snow) and layer 1 carries everything that
# sits on top of it - woods, hills, mountains, and the road.
W_SEA = A(0)                      # blocks
W_GRASS = A(16)
W_GRASS_DARK = A(17)
W_SAND = A(26)
W_SNOW = A(40)
W_WASTE = A(32)

W_FOREST = A(20)                  # walkable woodland
W_CONIFER = A(21)
W_HILLS = A(22)                   # blocks
W_HILLS_BROWN = A(23)             # blocks
W_MOUNTAIN = A(38)                # blocks
W_VOLCANO = A(39)                 # blocks
W_ROAD = A(29)                    # pale sand - what the sample uses for roads
W_DUNES = A(30)                   # blocks
W_JUNGLE = A(36)

# World_B landmarks, drawn on layer 3. Everything except the cave mouths and
# the lower half of a tower is impassable, so the events that enter them are
# player-touch, which fires on an impassable tile.
WB_VILLAGE = ((b_tile(0, 12), b_tile(1, 12)), (b_tile(0, 13), b_tile(1, 13)))
WB_TOWN = ((b_tile(2, 12), b_tile(3, 12)), (b_tile(2, 13), b_tile(3, 13)))
WB_DARK_CASTLE = ((b_tile(2, 3), b_tile(3, 3)), (b_tile(2, 4), b_tile(3, 4)))
WB_STONE_CASTLE = ((b_tile(4, 3), b_tile(5, 3)), (b_tile(4, 4), b_tile(5, 4)))
WB_TOWER = ((b_tile(0, 10),), (b_tile(0, 11),))
WB_TOWER_WHITE = ((b_tile(4, 10),), (b_tile(4, 11),))
WB_CAVE = b_tile(0, 2)
WB_CAVE_DARK = b_tile(3, 2)
WB_SIGN = b_tile(1, 0)
WB_TREE = b_tile(3, 1)
WB_HUT = b_tile(0, 1)
WB_ROCK = b_tile(5, 1)


# The only things that belong on the front of a house: what is nailed to the
# wall, and the holes in it. `Canvas` uses this to tell a shop sign from a
# barrel that has been drawn halfway up a wall by accident.
WALL_MOUNTED = frozenset(
    [WINDOW, DOORWAY_DARK, SIGN_BLADE, SIGN_ORB, SIGN_ARMOR, SIGN_RING,
     SIGN_POTION, SIGN_INN, SIGN_MUG, SIGN_PLATE, SIGN_WAND, SIGN_COIN,
     SIGN_HAMMER, SIGN_SUN]
    + list(WINDOW_GLASS) + list(DOOR_DOUBLE) + list(DOOR_SHUT)
    + list(DOORWAY_ARCH))


class BuildingOverlap(Exception):
    """Something was drawn on top of a house."""


# ================================================================ drawing ====
class Canvas(R.MapGrid):
    """A MapGrid that knows how to draw the things above.

    It also remembers where it put the houses. Scenery is placed by eye from a
    list of coordinates, houses are placed by corner and size, and the two lists
    are written at opposite ends of a map function - so a barrel ends up on a
    roof, or a market stall is drawn across the front of the tavern, and the map
    still builds and still validates and looks like a bomb went off. Every write
    into a building's footprint that is not part of the building is refused at
    the point it happens, which is the only place the mistake is legible.

    Allowed inside a footprint: layer 2 anywhere (that is where chimneys go),
    anything in `WALL_MOUNTED` on the wall rows, and the shadow and region
    layers. Everything else raises."""

    def __init__(self, width, height, data=None):
        R.MapGrid.__init__(self, width, height, data)
        self.buildings = []          # (x, y, w, h, wall_rows)
        self._structural = 0         # >0 while the Canvas is drawing its own

    # -- keeping scenery off the houses -------------------------------------
    def _refuse(self, x, y, z, tile):
        for bx, by, bw, bh, wall_rows in self.buildings:
            if not (bx <= x < bx + bw and by <= y < by + bh):
                continue
            part = "roof" if y < by + bh - wall_rows else "wall"
            if z == 2 or z >= 4:
                return
            if part == "wall" and z == 3 and tile in WALL_MOUNTED:
                return
            raise BuildingOverlap(
                "tile %d drawn on layer %d at (%d,%d), which is the %s of the "
                "building at (%d,%d) %dx%d. Move it off the house."
                % (tile, z, x, y, part, bx, by, bw, bh))

    def set(self, x, y, z, tile):
        if self.buildings and not self._structural:
            self._refuse(x, y, z, tile)
        R.MapGrid.set(self, x, y, z, tile)

    def autotile(self, *args, **kwargs):
        self._structural += 1
        try:
            return R.MapGrid.autotile(self, *args, **kwargs)
        finally:
            self._structural -= 1

    def blit(self, x, y, z, block):
        """Draw a tuple-of-rows block of raw tile ids with its top-left at x,y."""
        for dy, row in enumerate(block):
            for dx, tile in enumerate(row):
                if 0 <= x + dx < self.width and 0 <= y + dy < self.height:
                    self.set(x + dx, y + dy, z, tile)

    def column(self, x, y, z, tiles):
        """Draw a vertical run of tiles - a lamp post, a window, a doorway."""
        for dy, tile in enumerate(tiles):
            if 0 <= y + dy < self.height:
                self.set(x, y + dy, z, tile)

    def scatter(self, spots, z, tile):
        for x, y in spots:
            self.set(x, y, z, tile)

    # -- buildings ----------------------------------------------------------
    def roof(self, x, y, w, h, roof, z=3):
        """Nine-slice a roof over a w x h rectangle. Needs w >= 2 and h >= 2."""
        if roof not in (ROOF_GREEN, ROOF_WHITE, ROOF_GOLD, ROOF_BROWN):
            raise ValueError(
                "%r is not one of the four roof blocks on Outside_C; a "
                "nine-slice anchored anywhere else straddles two of them"
                % (roof,))
        col, row = roof
        self._structural += 1
        try:
            for j in range(h):
                for i in range(w):
                    cx = col if i == 0 else (col + 2 if i == w - 1 else col + 1)
                    cy = row if j == 0 else (row + 2 if j == h - 1 else row + 1)
                    self.set(x + i, y + j, z, c_tile(cx, cy))
        finally:
            self._structural -= 1

    def building(self, x, y, w, h, wall=WALL_PLANK, roof=ROOF_BROWN, wall_rows=2,
                 register=True):
        """A house: `wall_rows` rows of A3 wall along the bottom on layer 0,
        with the roof nine-sliced over everything above it on layer 3.

        The footprint is remembered, so that anything drawn over it afterwards
        is refused - see the class docstring. `register=False` opts out, for the
        rare structure that is meant to be built on top of.

        Returns the y of the front wall row - where a door event goes."""
        roof_h = h - wall_rows
        if roof_h >= 2:
            self.roof(x, y, w, roof_h, roof)
        self._structural += 1
        try:
            for j in range(wall_rows):
                for i in range(w):
                    self.set(x + i, y + roof_h + j, 0, wall)
        finally:
            self._structural -= 1
        if register:
            self.buildings.append((x, y, w, h, wall_rows))
        return y + h - 1

    def dungeon_walls(self, top, face, z=0):
        """Turn solid rock into a cave wall: the two rows of rock directly
        above any floor tile become the wall *face*, everything else stays the
        wall *top*. This is how the stock cave maps are tiled, and doing it
        after carving means the carving code never has to think about it."""
        top_kind = R.autotile_kind(top)

        def is_rock(x, y):
            if not (0 <= x < self.width and 0 <= y < self.height):
                return True
            t = self.get(x, y, z)
            return R.is_autotile(t) and R.autotile_kind(t) == top_kind

        faces = []
        for y in range(self.height):
            for x in range(self.width):
                if not is_rock(x, y):
                    continue
                if not is_rock(x, y + 1):
                    faces.append((x, y))
                elif is_rock(x, y + 1) and not is_rock(x, y + 2):
                    faces.append((x, y))
        for x, y in faces:
            self.set(x, y, z, face)

    # -- ground -------------------------------------------------------------
    def path_h(self, x1, x2, y, tile=PATH, thickness=1, z=0):
        self.fill(min(x1, x2), y, max(x1, x2), y + thickness - 1, z, tile)

    def path_v(self, x, y1, y2, tile=PATH, thickness=1, z=0):
        self.fill(x, min(y1, y2), x + thickness - 1, max(y1, y2), z, tile)

    def blob(self, cx, cy, rx, ry, z, tile):
        """A rough ellipse of tiles - a pond, a copse, a patch of flowers."""
        for y in range(cy - ry, cy + ry + 1):
            for x in range(cx - rx, cx + rx + 1):
                if not (0 <= x < self.width and 0 <= y < self.height):
                    continue
                dx = (x - cx) / float(rx or 1)
                dy = (y - cy) / float(ry or 1)
                if dx * dx + dy * dy <= 1.0:
                    self.set(x, y, z, tile)


def paint_regions(g, tileset_id, value=1, layer=5):
    """Region-tag every tile the player can actually stand on.

    Encounters are filtered by region, so a map whose regions only cover the
    tiles somebody remembered to paint has random battles on some paths and
    none on others - which reads as a bug long before it reads as a design.
    `value` may be a number or a function of (x, y) returning one; returning 0
    leaves that tile alone.

    Passability is read from the tileset flags the way `Game_Map.checkPassage`
    does, upper layers first, because the stock autotiles carry per-shape
    direction flags: the middle of a rock mass is passable and only its edges
    block, so "is this tile walkable" cannot be answered from the tile alone.
    """
    flags = R.load("Tilesets.json")[tileset_id]["flags"]

    def standable(x, y):
        for bit in (0x01, 0x02, 0x04, 0x08):
            for z in (3, 2, 1, 0):
                f = flags[g.get(x, y, z)]
                if f & 0x10:            # [*] star: no effect on passage
                    continue
                if (f & bit) == 0:      # [o] passable this way
                    return True
                break                   # [x] blocked; lower layers do not matter
        return False

    pick = value if callable(value) else (lambda x, y: value)
    for y in range(g.height):
        for x in range(g.width):
            if not standable(x, y):
                continue
            v = pick(x, y)
            if v:
                g.set(x, y, layer, v)


def new_map(width, height, tileset, name="", bgm="Town1", bgm_volume=70,
            encounters=(), encounter_step=30, battleback=None, scroll_type=0,
            parallax="", disable_dashing=False):
    """A map record with everything the editor expects, and nothing surprising."""
    m = {
        "autoplayBgm": bool(bgm), "autoplayBgs": False,
        "battleback1Name": "", "battleback2Name": "",
        "bgm": {"name": bgm or "", "pan": 0, "pitch": 100, "volume": bgm_volume},
        "bgs": {"name": "", "pan": 0, "pitch": 100, "volume": 90},
        "disableDashing": disable_dashing, "displayName": name,
        "encounterList": [
            {"troopId": t, "weight": w, "regionSet": list(regions)}
            for t, w, regions in encounters],
        "encounterStep": encounter_step, "height": height, "note": "",
        "parallaxLoopX": False, "parallaxLoopY": False, "parallaxName": parallax,
        "parallaxShow": True, "parallaxSx": 0, "parallaxSy": 0,
        "scrollType": scroll_type, "specifyBattleback": battleback is not None,
        "tilesetId": tileset, "width": width, "data": [0] * (width * height * 6),
        "events": [None],
    }
    if battleback:
        m["battleback1Name"], m["battleback2Name"] = battleback
    return m


def interior(width, height, x1, y1, x2, y2, door_x=None, floor=IN_WOOD_FLOOR,
             floor_alt=None, wall_top=IN_WALL_TOP, wall_face=IN_WALL_FACE,
             void=IN_VOID, threshold=None, outside=None):
    """A room in black space, tiled the way the stock interiors are.

    Reading down the screen: one row of wall *top*, two rows of wall *face*,
    then the floor, then the same in reverse - and the reversed pair at the
    bottom is the *outside* of the south wall, which is what makes a doorway
    read as a doorway. `door_x` cuts that gap.

    `floor_alt` lays a second floor kind in a checkerboard with the first,
    which is how the stock houses get their two-tone boards.
    """
    g = Canvas(width, height)
    g.fill(0, 0, width - 1, height - 1, 0, void)

    g.fill(x1, y1, x2, y2, 0, floor)
    if floor_alt is not None:
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                if (x + y) % 2:
                    g.set(x, y, 0, floor_alt)

    g.fill(x1 - 1, y1 - 3, x2 + 1, y1 - 3, 0, wall_top)
    g.fill(x1, y1 - 2, x2, y1 - 1, 0, wall_face)
    for y in range(y1 - 2, y2 + 2):
        g.set(x1 - 1, y, 0, wall_top)
        g.set(x2 + 1, y, 0, wall_top)
    g.fill(x1 - 1, y2 + 1, x2 + 1, y2 + 1, 0, wall_top)
    g.fill(x1, y2 + 2, x2, y2 + 3, 0, wall_face)

    if door_x is not None:
        g.set(door_x, y2 + 1, 0, floor)
        g.set(door_x, y2 + 2, 0, threshold if threshold is not None else a5(91))
        g.set(door_x, y2 + 3, 0, outside if outside is not None else a5(91))
    return g


def door_animation():
    """Open a door sprite, hold, close it, then make it transparent - the
    routine the sample uses so a door looks like it was walked through."""
    return [{"code": 17}, {"code": 15, "parameters": [3]},
            {"code": 18}, {"code": 15, "parameters": [3]},
            {"code": 19}, {"code": 37}]
