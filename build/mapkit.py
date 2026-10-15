"""Tile vocabulary and drawing helpers for The Obligatory Quest.

Everything here is named after what it looks like on screen, not after its tile
id, because tile ids are unreadable and the whole point of this file is that the
map scripts read like a description of the place.

The names were read off the labelled sheets that `tools/sheetgrid.py` produces
and then confirmed in a screenshot; anything unconfirmed says so.
"""
import os
import random
import sys

GAME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKSPACE = os.path.dirname(GAME)
sys.path.insert(0, os.path.join(WORKSPACE, "tools"))

import rmmzdata as R

# ---------------------------------------------------------------- tilesets ---
TS_WORLD, TS_OUTSIDE, TS_INSIDE, TS_DUNGEON = 1, 2, 3, 4
# Tileset 2 with one sheet swapped: its C sheet is `Outside_C_Collegium`, a copy
# of `Outside_C` whose green roof and green spire are purple, drawn by
# `collegium.draw_art()`. Every id means what it means on tileset 2, so the
# whole Outside vocabulary works on it; only `ROOF_PURPLE` and the spire look
# different. `build_game.build_tilesets` writes the record.
TS_COLLEGIUM = 7
# And tileset 1 with its B sheet swapped for `World_B_Fenmarch`, whose `Large
# Mansion` stamp has green roofs, drawn by `fenmarch.draw_art()`. It is the
# world map's tileset; `worldmap.json` is still drawn on tileset 1, and every
# id means the same on both.
TS_OVERWORLD = 8


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
# The ground is the sheet's second row, the kinds named "(Dirt)": each one's
# edge is a soft band of earth, so grass, a road and paving laid side by side
# blend into each other. The first row - `Meadow` and the kinds named
# "(Meadow)" - edges everything in a hard green lip, and a town drawn in it
# looks like its streets were cut out of a lawn with scissors. Mike redrew
# Nether Sopping and Much Pottering in the second row (October 2026).
GRASS = A(25)             # `Grass (Dirt)`
PATH = A(24)              # `Dirt`, a sandy track
COBBLE = A(26)            # `Road (Dirt)`, grey cobblestone
PAVING = A(27)            # `Cobblestones A (Dirt)`, cut paving slabs
MEADOW = A(16)            # `Meadow`, the green-lipped first row
HEDGE = A(20)             # dense low shrub
DECKING = A(22)           # wooden decking
SAND = A(24)              # `Dirt`, despite the name; `SOIL` is the `Sand`
WHEAT = A(28)             # yellow crop over grass - the turnip fields
SOIL = A(32)              # `Sand`
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
ROOF_PURPLE = ROOF_GREEN  # the same block, recoloured - on TS_COLLEGIUM only
TOWER_STONE = (8, 6)      # a round stone tower, not a roof: 2 wide, 5 tall
TOWER_WHITE = (10, 6)

# ------------------------------------------------------ Outside_B scenery ----
TREE = ((b_tile(8, 6), b_tile(9, 6)), (b_tile(8, 7), b_tile(9, 7)))
# TREE_DARK is not a darker tree: it is the sheet's forest canopy, a block
# that tiles with itself into one unbroken wood (the Gloamwood's Deep). Beside
# a whole TREE, or on its own on grass, it reads as four quarter-trees cut off
# square - so a ring of trees round a town is all TREE, and a solid wood is all
# TREE_DARK. The sample never lays it on Outside at all.
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
# Outside_B's `Boulder A` and `Boulder B`. These were (11, 2) and (12, 2),
# which are `Rock Fire Pit A` and `B`: campfire rings in the Gloamwood's
# undergrowth and on Thistlewick's verges. Same flags (0x60f), so nothing
# that walks past them changed (QUESTS.md A10-A11).
ROCK = b_tile(15, 3)
ROCK2 = b_tile(15, 4)
LOGS = b_tile(12, 4)              # a stacked log pile
TUB = b_tile(11, 1)               # pale open tub
BARREL = b_tile(13, 1)
CRATE = b_tile(13, 2)
POT = b_tile(8, 2)                # round grey urn
BUCKET = b_tile(9, 2)
SIGNPOST = b_tile(9, 1)           # a fingerpost with two boards
GRAVE_A = b_tile(14, 1)          # `Grave A`, a stone cross
GRAVE_B = b_tile(15, 1)          # `Grave B`, a headstone
FENCE_PANEL = b_tile(10, 1)       # a short slatted fence panel
STOVEPIPE = b_tile(8, 1)          # `Chimney`'s pipe; alone, it has no top
# `Chimney`, whole: the cap over the pipe, which bends east at the top. It
# stands *beside* a house, west of its roof's top two rows, with the bend
# reaching in over the roof - not stood in the middle of the roof, where the
# pipe alone was drawn for a year. Mike's, October 2026; `Canvas.chimney_beside`.
CHIMNEY = (b_tile(8, 0), b_tile(8, 1))
LILYPAD = b_tile(15, 15)
MUSHROOMS = b_tile(11, 13)
BURROW = b_tile(9, 5)             # a small dug hole in the earth
BRAMBLES = b_tile(1, 6)
DEAD_BUSH = b_tile(11, 15)
DEAD_TREE = b_tile(8, 13)
DEAD_ROOTS = b_tile(8, 12)
LADDER = b_tile(2, 2)

# Street lamp: lit head, post, and the foot it stands on, which is the one
# cell of the three that blocks. Two cells, without the foot, for a year; Mike
# gave Nether Sopping's and Much Pottering's theirs (October 2026).
LAMP = (b_tile(0, 1), b_tile(0, 2), b_tile(0, 3))

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
# The dark of a doorway in a north wall, for under a `!Door1` sprite on the
# lower face row: the sample's `Entrance A (Extend)`. Without it the door
# opens onto the wall it was hung on.
IN_DOOR_OPENING = b_tile(1, 2)
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
# These two are the halves of one cabinet - its frame runs across both - and
# the sheet's `.txt` hides it, calling column 9 and column 10 `Sundries Shelf
# A` and column 11 `B`. Either one alone is a cabinet cut in half down the
# middle, which is what Mike mended in the Eleven Days (October 2026): lay
# them as `IN_SUNDRIES_CABINET`, never one without the other.
IN_SHELF_BOTTLES = (b_tile(11, 3), b_tile(11, 4))
# Not fruit: two teddy bears and a pink rabbit on its top shelf.
IN_SHELF_FRUIT = (b_tile(10, 3), b_tile(10, 4))
IN_SUNDRIES_CABINET = (IN_SHELF_FRUIT, IN_SHELF_BOTTLES)  # columns, W to E
# Likewise `Bottle Shelf A` and `B`, columns 14 and 15: crockery on the west
# half, bottles on the east, one frame.
IN_BOTTLE_CABINET = ((b_tile(14, 1), b_tile(14, 2)),
                     (b_tile(15, 1), b_tile(15, 2)))
# Every two-wide piece above, for `lone_halves`.
WIDE_PIECES = (IN_SUNDRIES_CABINET, IN_BOTTLE_CABINET)
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
IN_KITCHEN_COUNTER = b_tile(10, 9)        # `Kitchen Counter A`, one cell

# Clean furniture, read off the `.txt` name tables rather than off a
# screenshot, because three of the constants above are named for what they
# looked like at 48 pixels and are something else: `IN_TABLE_ROUND` is
# **Table A (Ruins)**, `IN_TABLE_SMALL` is **Stool (Ruins)**, and `IN_COUNTER`
# is **Sundries Shelf A** - the one with two teddy bears painted on it. They
# are load-bearing in maps that already shipped and are left alone; anything
# new should use these.
IN_TABLE = ((b_tile(0, 14), b_tile(1, 14)),)   # `Table A`, two cells wide
IN_TABLE_ONE = b_tile(2, 14)               # `Table B`, a single square table
IN_STOOL = b_tile(0, 15)                   # `Stool A`, not the ruined one
IN_TABLE_PLAIN = b_tile(3, 14)             # `Table C`, a plain square one
IN_BOOKSHELF = (b_tile(13, 3), b_tile(13, 4))   # `Bookshelf A`
IN_WINE_RACK = (b_tile(13, 1), b_tile(13, 2))   # `Wine Rack`
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
INC_BELL = c_tile(0, 15)      # **`Globe`**, not a bell. Left alone: the
                             # Thistlewick store ships it. Use the next one
INC_DESK_BELL = c_tile(1, 15)  # `Bell`, which is what a counter wants
INC_SWORD_STAND = c_tile(8, 2)   # `Sword Rack A`: one sword, on a stand
INC_CASE = c_tile(0, 11)         # `Case A`: a glass display case
INC_OPEN_BOOK = c_tile(4, 8)     # `Open Book A (V)`, which is what a ledger
                                 # being written in has to be - `INC_BOOK` is
                                 # `Closed Book A (V)` and contradicts the line

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


# ============================================== SF Outside (tileset id = 5) ===
# Upper Clanging. Soot, brick and rust under a permanent chimney haze - not
# brass-and-goggles steampunk, which this library has no art for anyway.
#
# The names below come from the editor's own tile-name tables, the `.txt` files
# sitting beside each sheet in `img/tilesets/`. Those are keyed by tile id and
# are authoritative; the English half of each line is what the editor shows in
# its tile palette. They were cross-checked against the labelled sheets that
# `sheetgrid.py` draws - the ivy, Chinese and blue-tarpaulin blocks are
# unmistakable and pin the A3 rows, and Cliff A (Demonic Ground) sits at one
# odd position in the middle of the A4 walls and pins those.
#
# **The kind numbers collide with the Outside tileset and the art does not.**
# Tileset 5 uses SF_Outside_A3/A4 where tileset 2 uses Outside_A3/A4, so kind
# 116 is a grass plateau in Thistlewick (`CLIFF_TOP`) and a wooden wall in
# Upper Clanging. Nothing in the data distinguishes them. Every name in this
# section is therefore prefixed `SF_`, and an SF_ name must never be drawn on a
# map whose tileset is not TS_CLANGING - it will build, it will validate, and
# it will render as somebody else's furniture.
#
# Handily, SF Outside's A1 and A2 are the *ordinary* Outside water and grass,
# so the northern town sits on the same earth as the rest of the world and
# GRASS, WATER, PATH and the rest of the A2 vocabulary above work here
# unchanged.
TS_CLANGING, TS_CLANGING_IN = 5, 6

# -- SF_Outside_A3: the fronts of buildings (16-shape wall autotiles) ---------
# Row 0 (48-55) roofs A-H, row 1 (56-63) their walls, row 2 (64-71) roofs I-P,
# row 3 (72-79) their walls. As in the Outside set, the "roof" rows make good
# upper storeys, which is what they are used for here.
SF_UPPER_BRICK = A(48)            # Roof A (Brick) - dark grey ridged
SF_UPPER_FACTORY = A(49)          # Roof B (Factory) - flat pale grey
SF_UPPER_RUST = A(50)             # Roof C (Metal, Red Rust) - orange corrugated
SF_UPPER_BARRACKS = A(51)         # Roof D (Barracks) - green corrugated
SF_UPPER_IVY = A(54)              # Roof G (Ivy) - red tile gone under ivy
SF_WALL_STONE = A(56)             # Outer Wall A (Stone)
SF_WALL_FACTORY = A(57)           # Outer Wall B (Factory) - plain grey
SF_WALL_RUST = A(58)              # Outer Wall C (Metal, Red Rust) - riveted
SF_WALL_BARRACKS_A = A(59)        # Outer Wall D (Barracks)
SF_WALL_BARRACKS_B = A(60)        # Outer Wall E (Barracks)
SF_WALL_FACTORY_B = A(61)         # Outer Wall F (Factory)
SF_WALL_IVY = A(62)               # Outer Wall G (Ivy)
SF_UPPER_PATINA = A(66)           # Roof K (Metal, Patina) - green horizontal
SF_UPPER_WOOD = A(69)             # Roof N (Wood)
SF_WALL_TILE = A(72)              # Outer Wall I (Tile)
SF_WALL_BRICK_MOSSY = A(73)       # Outer Wall J (Brick) - green-brown, mossy
SF_WALL_MORTAR = A(74)            # Outer Wall K (Mortar) - salmon plaster
SF_WALL_WOOD = A(77)              # Outer Wall N (Wood) - dark brown boards
SF_WALL_BRICK = A(78)             # Outer Wall O (Brick) - the town's default
SF_WALL_WOOD_LIGHT = A(79)        # Outer Wall P (Wood)

# -- SF_Outside_A4: free-standing walls ---------------------------------------
# A4 alternates a 2x3 block-row (the top of a wall, seen from above, on the
# floor table) with a 2x2 block-row (its vertical face, on the 16-shape wall
# table). The pair for one wall is 8 kinds apart, and `MZ-DATA-FORMAT.md`'s
# "odd row is a wall" rule is what tells them apart.
SF_YARD_RUST_TOP, SF_YARD_RUST = A(86), A(94)        # Wall G (Metal, Red Rust)
SF_YARD_PATINA_TOP, SF_YARD_PATINA = A(87), A(95)    # Wall H (Metal, Patina)
SF_YARD_BARRACKS_TOP, SF_YARD_BARRACKS = A(96), A(104)   # Wall I (Barracks)
SF_YARD_BARRACKS2_TOP, SF_YARD_BARRACKS2 = A(97), A(105) # Wall J (Barracks)
SF_YARD_FACTORY_TOP, SF_YARD_FACTORY = A(98), A(106)     # Wall K (Factory)
SF_YARD_FACTORY_L_TOP, SF_YARD_FACTORY_L = A(100), A(108)  # Wall L (Factory)
SF_YARD_FACTORY_M_TOP, SF_YARD_FACTORY_M = A(101), A(109)  # Wall M (Factory)
SF_YARD_BRICK_TOP, SF_YARD_BRICK = A(103), A(111)    # Wall O (Brick) - red
SF_YARD_WOOD_TOP, SF_YARD_WOOD = A(116), A(124)      # Wall T (Wood)
SF_YARD_WOOD_DIRTY_TOP, SF_YARD_WOOD_DIRTY = A(117), A(125)  # Wall U (Wood)

# -- SF_Outside_A5: the ground of the yard ------------------------------------
SF_WASTE = a5(16)                 # Waste Land - bare grey industrial dirt
SF_METAL_FLOOR = a5(17)           # Metal Floor A (Factory) - treadplate
SF_METAL_FLOOR_RUINS = a5(23)     # the same, rusted through
SF_CONCRETE = a5(18)
SF_CONCRETE_RUINS = a5(19)
SF_GRID_FLOOR = a5(1)             # walkable grating
SF_DIRTY_FLOOR = a5(32)
SF_COBBLE_A = a5(64)
SF_COBBLE_B = a5(65)
SF_COBBLE_C = a5(66)
SF_MECHA_FLOOR = a5(27)
SF_WOOD_FLOOR = a5(38)
SF_HOLE = a5(20)
# Stairs come in left/centre/right/plain sets; the street runs up a slope and
# these are what it climbs.
SF_STAIRS_METAL = (a5(44), a5(45), a5(46), a5(47))   # left, centre, right, plain
SF_STAIRS_WOOD = (a5(60), a5(61), a5(62), a5(63))

# -- SF_Outside_B: what stands in the street ----------------------------------
SF_CHIMNEY_A = b_tile(0, 13)
SF_CHIMNEY_B = b_tile(1, 13)
SF_CHIMNEY_C = b_tile(2, 13)
SF_CRATE = b_tile(8, 0)
SF_BARREL = b_tile(11, 0)
SF_STACKED_CRATES = (b_tile(5, 12), b_tile(5, 13))   # two tiles, top then bottom
SF_MACHINE_A = b_tile(10, 4)
SF_MACHINE_B = b_tile(11, 4)
SF_MACHINE_C = b_tile(12, 4)
SF_MACHINE_DEVICE = b_tile(9, 3)
SF_AIR_VENT_A = b_tile(10, 6)
SF_AIR_VENT_B = b_tile(11, 6)
SF_VENT = b_tile(15, 8)
SF_SMALL_FUEL_TANK = b_tile(12, 7)

# -- SF_Outside_C: the bigger structures --------------------------------------
# Nine-slices, given as the (column, row) of their top-left cell, the same way
# the Outside roofs above are.
# The Clock Tower is three rows and is **not** a nine-slice, whatever its shape
# suggests. Its rows are (cap, clock face, brick shaft), so stretching it with
# `roof()` repeats the *middle* row and the town gets a tower with two clocks
# on it. `Canvas.clock_tower` repeats the shaft instead, which is what a tall
# one is made of. Found by drawing one four rows high and looking at it.
SF_CLOCK_TOWER = (12, 3)          # the one civic building in Upper Clanging
SF_ROOF = (13, 12)                # 3x3 plain pitched roof
SF_PILLAR_MACHINE = (c_tile(3, 9), c_tile(3, 10))    # Pillar C (Machine)
SF_PILLAR_METAL = (c_tile(2, 9), c_tile(2, 10))      # Pillar B (Metal)
SF_PILLAR_BRICK = (c_tile(6, 9), c_tile(6, 10))      # Pillar F (Brick)
SF_BROKEN_PILLAR_MACHINE = c_tile(3, 11)
SF_BROKEN_PILLAR_BRICK = c_tile(6, 11)
SF_IRON_FENCE_A = (c_tile(11, 9), c_tile(11, 10), c_tile(11, 11))
SF_IRON_FENCE_B = c_tile(15, 6)
SF_METAL_FENCE = (c_tile(2, 6), c_tile(3, 6), c_tile(4, 6))
SF_SPHERE_MACHINERY = ((c_tile(2, 14), c_tile(3, 14), c_tile(4, 14)),
                       (c_tile(2, 15), c_tile(3, 15), c_tile(4, 15)))
SF_WATER_TANK = (c_tile(12, 13), c_tile(12, 14))
SF_ROUND_CLOCK = c_tile(9, 10)
# What a street is furnished with, once it has stopped being a factory yard.
# All of these are from the same `.txt` table; the names in the comments are
# the editor's own. The Warning Plate comes twice, as a plate to bolt to a
# wall and as a plate on a post - the post is the only free-standing sign in
# the set, and it is what a northern town sign is nailed to.
SF_SIGN_POST = (c_tile(0, 10), c_tile(0, 11))    # Warning Plate, on a post
SF_WARNING_PLATE = c_tile(3, 7)                  # Warning Plate, on a wall
SF_CANOPY = (c_tile(6, 2), c_tile(6, 3))         # Shop Canopy
SF_PUMP = c_tile(6, 1)                           # Water Well Pump
SF_POSTBOX = c_tile(6, 7)                        # Postal Box
SF_BENCH = (c_tile(3, 2), c_tile(4, 2))          # Bench A, 2 wide
SF_BENCH_B = (c_tile(3, 3), c_tile(4, 3))        # Bench B
SF_DUMPSTER = c_tile(7, 1)                       # Garbage Dumpster
SF_WEEDS = c_tile(0, 4)                          # Grass A
SF_WEEDS_B = c_tile(1, 4)                        # Grass B
SF_RUBBLE = c_tile(3, 4)                         # Small Stones

# -- the name table, and what it rules out ------------------------------------
def tile_names(sheet):
    """`{name: [tile id, ...]}` for a B/C/D/E sheet, from the editor's own tile
    name file - the `.txt` sitting next to the `.png` in `img/tilesets/`.

    Each line is `English|Japanese` and line *n* describes tile id *n-1*, so
    the file is an exact, authoritative index of the sheet. It is what the
    editor shows in its tile palette, and it beats counting 48-pixel cells by
    eye. Names repeat where a prop is more than one tile, which is how a two-
    tile chimney or a four-tile lorry can be picked up whole."""
    path = os.path.join(GAME, "img", "tilesets", sheet + ".txt")
    out = {}
    with open(path, encoding="utf-8-sig") as fh:
        for tile_id, line in enumerate(fh):
            name = line.split("|")[0].strip()
            if name and name != "Transparent":
                out.setdefault(name, []).append(tile_id)
    return out


def _sheet_base(sheet):
    """Where a sheet's tile ids start. A `.txt` name table is indexed from the
    first tile of its own sheet, so the id it implies has to be rebased."""
    for suffix, base in (("_A5", R.TILE_ID_A5), ("_B", 0), ("_C", R.TILE_ID_C),
                         ("_D", R.TILE_ID_D), ("_E", R.TILE_ID_E)):
        if sheet.endswith(suffix):
            return base
    raise KeyError("no id base known for sheet %r" % sheet)


def sf_tile(sheet, name, index=0):
    """One tile, by the name the editor's palette gives it. Safer than counting
    48-pixel cells, and it says in the source what was meant."""
    return _sheet_base(sheet) + sorted(tile_names(sheet)[name])[index]


def sf_block(sheet, name):
    """Every tile of a multi-tile prop, in reading order - so a three-tile
    ladder or a two-tile window comes back whole, ready for `Canvas.column`."""
    base = _sheet_base(sheet)
    return tuple(base + t for t in sorted(tile_names(sheet)[name]))


# SF Inside (tileset 6) carries the stock Inside_B and Inside_C in its D and E
# slots, and Outside (tileset 2, and the Collegium's copy of it) carries
# Inside_C in E - `build_game.build_tilesets` - so the same tile has a
# different id there than on tileset 3, and `sf_tile("Inside_C", ...)` would
# be wrong.
_BORROWED_SLOTS = {"Inside_B": R.TILE_ID_D, "Inside_C": R.TILE_ID_E}


def borrowed(sheet, name):
    """Every tile of a stock Inside_B/Inside_C prop, by name, as it is
    numbered where it is borrowed (above) - one id for a 1x1 prop, a tuple
    for a column. Inside_B is on SF Inside only; Inside_C is on SF Inside,
    Outside and Dungeon."""
    base = _BORROWED_SLOTS[sheet]
    ids = tuple(base + t for t in sorted(tile_names(sheet)[name]))
    return ids[0] if len(ids) == 1 else ids


# The Dungeon tileset has Inside_C in its E slot too (`build_game.build_tilesets`,
# QUESTS.md P2): two things the Obligatory Tower and the Bottomless Pit have in
# their text that the Dungeon sheets do not have at all.
DGE_BASIN = borrowed("Inside_C", "Large Basin")    # a tub of clear water
DGE_HAMPER = borrowed("Inside_C", "Basket A")      # cloth-lined, a picnic's


# -- Inside furniture, by name ------------------------------------------------
# The honest half of the `IN_*` vocabulary. The constants above were named for
# what a tile looked like at 48 pixels, and a crop of every prop Thistlewick's
# and Nether Sopping's interiors laid down (`tools/propsheet.py`, September
# 2026) found the names wrong where it mattered most: `IN_TABLE_ROUND` is
# `Table A (Ruins)`, split in two; `IN_TABLE_SMALL` is `Stool (Ruins)`;
# `IN_POT` is `Barrel (Ruins)`, stove in; `INC_CANDLES` is `Scrolls A`;
# `INC_ARMOR_STAND` is a porcelain doll; `INC_BELL` is a globe; `IN_CLOCK` is
# two tables; `IN_PIANO` is only the lid and `IN_ORGAN` has a piano's keyboard
# on top of it; and `IN_PILLAR` stands on `Broken Stone Pillar A`. Those names
# stay, because later rooms use some of them knowingly (a `Pot B` is a good
# pot); a room that means a table uses these.
def _rows(block, width):
    return tuple(block[i:i + width] for i in range(0, len(block), width))


IN_TABLE_WOOD = sf_tile("Inside_B", "Table D")          # plain, counter-flagged
# A small table with flowers painted on: the nightstand by Halbert Quy's bed
# (Mike, October 2026). Not a `Table D`, so `new_tables` leaves it alone.
IN_NIGHTSTAND = sf_tile("Inside_B", "Table F")
IN_STOOL_SQUARE = sf_tile("Inside_B", "Stool C")        # two make a bench
IN_BARREL_WOOD = sf_tile("Inside_B", "Barrel")
IN_STONE_PILLAR = sf_block("Inside_B", "Stone Pillar A")    # capital, shaft
IN_LONGCASE_CLOCK = sf_block("Inside_B", "Clock")
IN_PIANO_WHOLE = _rows(sf_block("Inside_B", "Piano"), 3)
IN_PIPE_ORGAN = _rows(sf_block("Inside_B", "Pipe Organ"), 3)
# The tavern table Mike put in the Slain Wyvern (October 2026), and the one the
# sample's bars are built from: Inside_A2's `Table A (Wood)`, an autotile on
# layer 1, so adjacent cells join into one table of any size and whatever is
# set on it sits on the top instead of hanging off the edge of `Table D`. It
# keeps the counter flag, so a bar built of it still lets the action button
# reach across. Lay it, then `autotile(1, kinds=TABLE_KINDS)`; two tables
# meant to be separate need a cell between them or they become one.
IN_TABLE_TOP = A(23)
# Its dark twin, `Table B (Dark Wood)`, which Mike made the Safety Valve's bar
# and tables from (October 2026). Inside_A2 is the A2 of the northern tileset
# too, so it is the A2 table there as well as here; same flags, counter and all.
IN_TABLE_DARK = A(31)
TABLE_KINDS = {R.autotile_kind(IN_TABLE_TOP), R.autotile_kind(IN_TABLE_DARK)}
INC_DINNER_BELOW = sf_tile("Inside_C", "Dinner Set A (Bottom)")  # a place laid
INC_DINNER_ABOVE = sf_tile("Inside_C", "Dinner Set B (Top)")     # toward the
INC_DINNER_LEFT = sf_tile("Inside_C", "Dinner Set C (Left)")     # side its
INC_DINNER_RIGHT = sf_tile("Inside_C", "Dinner Set D (Right)")   # diner sits on
INC_ROAST = sf_tile("Inside_C", "Roast Chicken")
INC_PINT = sf_tile("Inside_C", "Pint Mug C")
INC_PINTS = sf_tile("Inside_C", "Pint Mug A (Lower Left)")
INC_ENVELOPE = sf_tile("Inside_C", "Envelope")
INC_LEDGER = sf_tile("Inside_C", "Open Book A (H)")
INC_MEDICINE = sf_tile("Inside_C", "Medicine Bottles B")
INC_MEDICINE_ONE = sf_tile("Inside_C", "Medicine Bottle A")
INC_KEG = sf_tile("Inside_C", "Beer Barrel A")              # stands on a bar
# `Bookshelf B` is two cells wide, and `IN_BOOKCASE`/`IN_BOOKCASE2` are its
# left and right halves - one alone is half a bookcase. `IN_BOOKSHELF` is the
# one-wide `Bookshelf A`.
IN_BOOKCASE_WIDE = ((IN_BOOKCASE[0], IN_BOOKCASE2[0]),
                    (IN_BOOKCASE[1], IN_BOOKCASE2[1]))
# `IN_CURTAIN_GREEN` is the left half of `Middle Window B`, a two-wide window
# with green curtains; this is all of it. It hangs on the wall's face rows.
IN_WINDOW_GREEN = _rows(sf_block("Inside_B", "Middle Window B"), 2)
INC_SCROLLS = sf_tile("Inside_C", "Scrolls A")
INC_ALTAR = _rows(sf_block("Inside_C", "Church Table"), 3)  # candles each end
INC_ARMOUR_STEEL = sf_tile("Inside_C", "Armor B (Stand)")
INC_COAT_STAND = sf_tile("Inside_C", "Women's Clothing C (Stand)")


# -- SF_Outside_B: the front of a building ------------------------------------
# The town has no trees: tileset 5's B sheet is SF_Outside_B, so none of the
# Outside_B scenery above exists up here. What a northern street front is made
# of instead is signs, windows, shutters and ventilation.
#
# The metal shop signs are the plain enamel cousins of the neon ones two rows
# above them on the sheet, and are the only signs in the set that are not lit.
SF_SIGN_BLANK = sf_tile("SF_Outside_B", "Metal Shop Sign (Blank)")
SF_SIGN_WEAPON = sf_tile("SF_Outside_B", "Metal Shop Sign (Weapon)")
SF_SIGN_ARMOR = sf_tile("SF_Outside_B", "Metal Shop Sign (Armor)")
SF_SIGN_ITEM = sf_tile("SF_Outside_B", "Metal Shop Sign (Item)")
SF_SIGN_PHARMACY = sf_tile("SF_Outside_B", "Metal Shop Sign (Pharmacy)")
SF_SIGN_CAFE = sf_tile("SF_Outside_B", "Metal Shop Sign (Cafe)")
SF_SIGN_INN = sf_tile("SF_Outside_B", "Metal Shop Sign (Inn)")

# Eight windows and eight midsize (two-tile) ones, A to H. Confirmed in the
# `sf_fronts` sampler: A is plain glass in a white frame, B frosted, C a grey
# louvre, D boarded over, E a hopper, F a louvred grid, G red-and-gold Chinese
# lattice, H white lattice. The three the town actually uses are named below.
SF_WINDOWS = tuple(sf_tile("SF_Outside_B", "Window %s" % c) for c in "ABCDEFGH")
SF_WINDOWS_TALL = tuple(sf_block("SF_Outside_B", "Midsize Window %s" % c)
                        for c in "ABCDEFGH")
SF_WINDOW = SF_WINDOWS[0]              # plain glass, white frame
SF_WINDOW_LOUVRE = SF_WINDOWS[2]       # grey slats - a works, or a shed
SF_WINDOW_TALL = SF_WINDOWS_TALL[0]    # the plain one, two tiles high

SF_ENTRANCE_A = sf_tile("SF_Outside_B", "Entrance A")
SF_ENTRANCE_B = sf_tile("SF_Outside_B", "Entrance B")
SF_SHUTTER = sf_tile("SF_Outside_B", "Shutter")
SF_EXHAUST_WALL = sf_tile("SF_Outside_B", "Exhaust Port Wall")
SF_WALL_POSTER = sf_tile("SF_Outside_B", "Wall Poster")
SF_AIR_INTAKE = sf_tile("SF_Outside_B", "Outdoor Air Intake Unit")
SF_OIL_DRUM = sf_tile("SF_Outside_B", "Oil Drum")
SF_OIL_DRUM_LEAK = sf_tile("SF_Outside_B", "Oil Drum (Leak)")
# Both of these are three tiles tall and both are **real routes**, not scenery:
# the ladder's top two tiles carry the engine's ladder bit and are flagged
# 0x626 - passable up and down, blocked left and right - and its foot is
# passable in every direction. Drawn against a retaining wall for decoration
# it is a way over the wall, and drawn on a house it is a way onto the roof.
SF_LADDER = sf_block("SF_Outside_B", "Metal Ladder")
SF_FIRE_ESCAPE = sf_block("SF_Outside_B", "Metal Stairs")


# -- the Long Field -----------------------------------------------------------
# What a works puts up round two hundred years of its own wrecks. The wrought
# iron is the whole look of the place: `Iron Fence B` tiles into a continuous
# dark-green railing on a stone plinth, `Iron Fence A` is the tall ornamental
# panel that makes a gatepost, and `Gate` is one leaf of a double gate. Rows of
# `Tombstone (Plaque)` in front of them do the rest, and nothing in the map or
# in a single line of its dialogue ever says the word the player is thinking.
SF_RAILING = SF_IRON_FENCE_B                     # one bay of railing
SF_RAILING_PIER = SF_IRON_FENCE_A                # 3 tall: a gatepost
SF_GATE_LEAF = (c_tile(15, 7), c_tile(15, 8))    # Gate, 2 tall: one leaf, open
# Named through the `.txt` tables rather than by counting cells, for the reason
# the rest of this file is: a B sheet is two blocks of eight columns, so a
# hand-counted (column, row) is off by a whole block as often as not - four of
# these were, and every one of the four resolved to a plausible-looking tile
# that happened to be somebody else's furniture.
SF_PLAQUE = sf_tile("SF_Outside_B", "Tombstone (Plaque)")
SF_SCRAP = sf_tile("SF_Outside_B", "Scrap Metal")
SF_IRONWORK = sf_tile("SF_Outside_B", "Iron Materials")
SF_SPOIL = sf_tile("SF_Outside_B", "Waste")
# Both of these carry the **ladder** bit on their upper two tiles (0x626), the
# same as `SF_LADDER` above: a rope or a net drawn down the side of anything is
# a way up it. Hang one where the top of it goes somewhere and it is a route.
SF_ROPE = sf_block("SF_Outside_B", "Rope")            # 3 tall, hook at the foot
SF_NETTING = sf_block("SF_Outside_B", "Net")          # 3 tall, rigging netting
SF_BROKEN_PILLAR_METAL = sf_tile("SF_Outside_C", "Broken Pillar B (Metal)")
SF_FISSURE = sf_block("SF_Outside_B", "Fissures A")   # 2 tall, cracked ground


# ================================================ SF Inside (tileset id = 6) ==
# Tileset 6 is a mongrel, and usefully so: its A1 and A2 are the *ordinary*
# Inside water and floors and its A5 is SF_Outside_A5 - the same ground the
# town outside is paved with. Only A4, B and C are SF Inside's own. So every
# `IN_` floor above works in a northern interior, and so does every `SF_` A5
# name, and only the walls have to be learned.
#
# A4 is arranged exactly as SF Outside's: a 2x3 block-row of wall *top* on the
# 48-shape floor table, then a 2x2 block-row of its vertical *face* on the
# 16-shape wall table, and **the face of a wall is its top plus 8**. Names are
# from `SF_Inside_A4.txt`, which for an A-sheet is one line per *kind*, so
# line n is kind 79 + n.
#
# Wall F is the one to leave alone: its top is called "Metal, Patina" and its
# face is called "Tent, Camouflage", which is either a mislabel or two
# different walls sharing a slot, and the editor's own table cannot say which.
SF_IN_WALL_CONCRETE, SF_IN_FACE_CONCRETE = A(80), A(88)      # Wall A
SF_IN_WALL_HOUSE, SF_IN_FACE_HOUSE = A(82), A(90)            # Wall C (House)
SF_IN_WALL_METAL, SF_IN_FACE_METAL = A(83), A(91)            # Wall D (Metal)
SF_IN_WALL_RUST, SF_IN_FACE_RUST = A(84), A(92)              # Wall E (Red Rust)
SF_IN_WALL_BARRACKS, SF_IN_FACE_BARRACKS = A(86), A(94)      # Wall G
SF_IN_WALL_FACTORY, SF_IN_FACE_FACTORY = A(96), A(104)       # Wall I (Factory)
SF_IN_WALL_FACTORY_B, SF_IN_FACE_FACTORY_B = A(97), A(105)   # Wall J (Factory)
SF_IN_WALL_PATTERN, SF_IN_FACE_PATTERN = A(98), A(106)       # Interior Wall A
SF_IN_WALL_PATTERN_B, SF_IN_FACE_PATTERN_B = A(99), A(107)   # Interior Wall B
SF_IN_WALL_BRICK, SF_IN_FACE_BRICK = A(103), A(111)          # Wall K (Brick)
SF_IN_WALL_WOOD, SF_IN_FACE_WOOD = A(112), A(120)            # Wall L (Wood)

# A5, shared with the street outside. `interior()`'s default threshold tile is
# Inside_A5's wooden step, which on this sheet is a slab of demonic ground, so
# a northern room has to be given one: the plain metal stair is flagged 0x606,
# blocked left and right, which is exactly what a doorway wants.
SF_FLOOR_RESIN = a5(48)           # Interior Floor A (Green Resin)
SF_FLOOR_TILE = a5(49)            # Interior Floor B (Tile)
SF_FLOOR_DECO = a5(51)            # Interior Floor C (Decoration)
SF_FLOOR_WOOD = a5(54)            # Wood Floor B
SF_FLOOR_CARPET = a5(89)          # Interior Floor F (Tile Carpet)
SF_FLOOR_MARBLE = a5(96)
SF_FLOOR_LINO = a5(97)            # Interior Floor G (Linoleum)
SF_THRESHOLD = SF_STAIRS_METAL[3]


# -- SF_Inside_B and SF_Inside_C: what stands in a northern room --------------
# Named through the `.txt` tables for the same reason the street is, and
# confirmed in `sampler.py sf_inside` / `sf_parlour`. Tileset 6's B and C are
# its own, so *none* of the `IN_` furniture above exists indoors up here - no
# beds with blankets, no bookcases, no round tables, no fireplace. Only the
# floors and the water carry over.
#
# The convention on this sheet is the same as everywhere else: a two-tile prop
# has the **star** flag on its upper tile (0x610) so it draws over the party,
# and its lower tile solid (0x60f). Both go on an upper layer.
def sf_grid(sheet, name, w):
    """A rectangular prop as a tuple of rows, ready for `Canvas.blit`.

    `sf_block` returns a flat run in id order, which for anything inside one
    half of a sheet is reading order - so it only wants folding into rows."""
    flat = sf_block(sheet, name)
    if len(flat) % w:
        raise ValueError("%s is %d tiles, which is not %d wide"
                         % (name, len(flat), w))
    return tuple(flat[i:i + w] for i in range(0, len(flat), w))


def recolour_sheet(sheet, out, cells, hues, hue, sat, renames=()):
    """Writes `img/tilesets/<out>.png`, a copy of `<sheet>.png` with some cells
    recoloured, and the `.txt` beside it with some names changed.

    For a colour no sheet has: the Collegium's purple roofs, Fenmarch's green
    ones. In each (column, row) of `cells`, every pixel whose hue is inside
    `hues` (lo, hi degrees) and which has any colour in it is moved to `hue`,
    with its saturation scaled by `sat` and its value kept - so the shading
    survives and grey stone in the same cell is left alone. `renames` is
    (old, new) pairs applied to those cells' names, so `contact.py` and
    `tileaudit.py` read the copy truthfully. Not part of the data build: the
    modules that need one run it from their `draw_art()`."""
    sys.path.insert(0, os.path.join(WORKSPACE, "tools", "chargen"))
    import numpy as np
    import png
    tiles = os.path.join(GAME, "img", "tilesets")
    a = png.read(os.path.join(tiles, sheet + ".png")).astype(float)
    lo, hi = hues
    for c, r in cells:
        cell = a[r * 48:(r + 1) * 48, c * 48:(c + 1) * 48]
        rgb = cell[..., :3] / 255
        v, mn = rgb.max(-1), rgb.min(-1)
        d = v - mn
        q = np.where(d > 0, d, 1)
        red, grn, blu = rgb[..., 0], rgb[..., 1], rgb[..., 2]
        h = np.where(v == red, ((grn - blu) / q) % 6,
                     np.where(v == grn, (blu - red) / q + 2,
                              (red - grn) / q + 4)) * 60
        s = np.where(v > 0, d / np.where(v > 0, v, 1), 0)
        pick = (d > 0) & (h > lo) & (h < hi) & (s > 0.15) & (cell[..., 3] > 0)
        s = s * sat
        k = (np.array([5, 3, 1]) + hue / 60) % 6
        k = k[None, None, :]
        new = v[..., None] - (v * s)[..., None] * np.clip(
            np.minimum(k, 4 - k), 0, 1)
        cell[..., :3] = np.where(pick[..., None], new * 255, cell[..., :3])
    path = os.path.join(tiles, out + ".png")
    png.write(path, np.clip(a, 0, 255).round().astype(np.uint8))
    print("wrote", os.path.normpath(path))
    with open(os.path.join(tiles, sheet + ".txt"), encoding="utf-8",
              newline="") as fh:
        names = fh.read().split("\n")
    for c, r in cells:
        i = b_tile(c, r)
        for old, new_name in renames:
            names[i] = names[i].replace(old, new_name)
    path = os.path.join(tiles, out + ".txt")
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write("\n".join(names))
    print("wrote", os.path.normpath(path))


# The works, the forge, and anything with pressure in it. `NORTH.md` 4.4 names
# the ones to use; the screens and the server are on the forbidden list.
SF_IN_MACHINE_C = sf_tile("SF_Inside_C", "Machine C")
SF_IN_AIR_VENT = sf_tile("SF_Inside_C", "Air Vent A")   # a louvred grille
SF_IN_RUBBLE = sf_tile("SF_Inside_C", "Rubble")         # masonry, not litter
SF_IN_PIPE_H = sf_tile("SF_Inside_C", "Pipe (H)")
SF_IN_PIPE_V = sf_block("SF_Inside_C", "Pipe (V)")
# "Plumbing" is eleven tiles, not a rectangle: a two-tile cap over a 3x3 run
# of pipework. Only the square part tiles, so that is what the name means.
SF_IN_PLUMBING = tuple(sf_block("SF_Inside_C", "Plumbing")[i:i + 3]
                       for i in range(2, 11, 3))          # 3 wide, 3 tall
SF_IN_VALVE = sf_tile("SF_Inside_C", "Valve")
SF_IN_DUCT = sf_block("SF_Inside_C", "Duct")             # 1 wide, 3 tall
SF_IN_MECH_DEVICE = sf_block("SF_Inside_C", "Mechanical Device")
SF_IN_BELT_H = sf_block("SF_Inside_C", "Belt Conveyor (H)")
SF_IN_BELT_V = sf_block("SF_Inside_C", "Belt Conveyor (V)")
SF_IN_AIR_VENT_A = sf_tile("SF_Inside_C", "Air Vent A")
SF_IN_AIR_VENT_B = sf_tile("SF_Inside_C", "Air Vent B")
SF_IN_VENT = sf_tile("SF_Inside_C", "Vent")
SF_IN_DRAIN = sf_tile("SF_Inside_C", "Drain")
SF_IN_PAPERS = sf_tile("SF_Inside_C", "Scattered Papers")
SF_IN_RUBBLE = sf_tile("SF_Inside_C", "Rubble")
SF_IN_RUBBLE_PILE = sf_grid("SF_Inside_C", "Pile of Rubble", 2)
SF_IN_HANDRAIL = sf_block("SF_Inside_C", "Handrail")[:3]
SF_IN_GIRDER = sf_block("SF_Inside_B", "Girder B (Metal, Left)") \
    + sf_block("SF_Inside_B", "Girder B (Metal, Center)") \
    + sf_block("SF_Inside_B", "Girder B (Metal, Right)")
# Plate *B* is the plain black-and-yellow striped plate, which is the same
# object as the street's `SF_WARNING_PLATE`. A is the ISO warning triangle
# and C is a radiation trefoil; both are twentieth-century safety design and
# both are on the forbidden list below.
SF_IN_WARNING = sf_tile("SF_Inside_B", "Warning Plate B")
SF_IN_METAL_RUBBLE = sf_tile("SF_Inside_B", "Rubble B (Metal)")

# Storage, and the things an office is made of.
SF_IN_STEEL_SHELF = sf_block("SF_Inside_B", "Steel Shelf")
SF_IN_DOC_SHELF = sf_block("SF_Inside_B", "Document Shelf")
SF_IN_BOOKSHELF = sf_block("SF_Inside_B", "Bookshelf A")
SF_IN_DRAWERS = sf_block("SF_Inside_B", "Chest of Drawers A")
SF_IN_ODDMENTS = sf_block("SF_Inside_B", "Miscellaneous Item Shelf")
SF_IN_LOCKER = sf_block("SF_Inside_B", "Locker A")
SF_IN_MEDICINE_SHELF = sf_block("SF_Inside_B", "Medicine Shelf")
SF_IN_STACKED_CRATES = sf_block("SF_Inside_B", "Stacked Crates")
SF_IN_CHEST_WOOD = sf_tile("SF_Inside_B", "Chest A (Wood)")
SF_IN_CHEST_METAL = sf_tile("SF_Inside_B", "Chest B (Metal)")
# Both desks carry the counter flag (0x80) as well as being solid, so the
# action button reaches across one - which is what a shop counter wants, and
# is better than the Wyvern's trick of building a bar out of round tables.
SF_IN_DESK_LARGE = sf_block("SF_Inside_B", "Large Desk A")     # 2 wide
SF_IN_DESK_LARGE_B = sf_block("SF_Inside_B", "Large Desk B")
SF_IN_DESK = sf_tile("SF_Inside_B", "Desk")
SF_IN_SIDE_DESK = sf_tile("SF_Inside_B", "Side Desk A (Wood)")
SF_IN_SIDE_DESK_METAL = sf_tile("SF_Inside_B", "Side Desk B (Metal)")
SF_IN_BOOK_STAND = sf_tile("SF_Inside_B", "Book Stand")
SF_IN_DOCUMENT = sf_tile("SF_Inside_B", "Document")
SF_IN_BULLETIN = sf_tile("SF_Inside_C", "Bulletin Board")
SF_IN_WALL_CLOCK = sf_block("SF_Inside_C", "Wall Clock")
SF_IN_PARTITION = sf_block("SF_Inside_C", "Partition A")

# The inn, which is the only room up here with soft furnishings in it.
SF_IN_FIREPLACE = sf_grid("SF_Inside_C", "Fireplace", 3)       # 3 wide, 2 tall
SF_IN_ARMCHAIR = sf_block("SF_Inside_C", "Armchair")
SF_IN_STOOL = sf_tile("SF_Inside_C", "Stool")
SF_IN_TABLE = sf_tile("SF_Inside_C", "Side Table")             # also a counter
SF_IN_BED = sf_block("SF_Inside_B", "Bed")
SF_IN_BED_IRON = sf_block("SF_Inside_B", "Pipe Frame Bed")
SF_IN_CURTAINS = sf_block("SF_Inside_C", "Curtains A")
SF_IN_CURTAINS_B = sf_block("SF_Inside_C", "Curtains B")
SF_IN_WINDOW = sf_block("SF_Inside_B", "Midsize Window A")
SF_IN_LAMP = sf_tile("SF_Inside_C", "Lamp")
SF_IN_PICTURE = sf_tile("SF_Inside_C", "Picture Frame")
SF_IN_PAINTING_A = sf_tile("SF_Inside_C", "Painting A")
SF_IN_PAINTING_B = sf_tile("SF_Inside_C", "Painting B")
SF_IN_PLANT = sf_block("SF_Inside_C", "Plant A")
SF_IN_POTTED_PLANT = sf_tile("SF_Inside_C", "Potted Plant")
# No `Kitchen Counter` name: it is on the forbidden list below, and a name
# that always raises when it is drawn is a trap rather than a vocabulary.
SF_IN_SINK = sf_tile("SF_Inside_B", "Sink")
SF_IN_MATTRESS = sf_tile("SF_Inside_B", "Mattress")
SF_IN_SPIDER_WEB = sf_tile("SF_Inside_C", "Spider Web")
SF_IN_DRIPPING = sf_tile("SF_Inside_C", "Dripping")

# On the table. Every one of these is a single tile that goes on top of one.
SF_IN_MUG = sf_tile("SF_Inside_C", "Beer Mug")
SF_IN_WINE = sf_tile("SF_Inside_C", "Wine & Glass")
SF_IN_BREAD = sf_tile("SF_Inside_C", "Bread")
SF_IN_MEAT = sf_tile("SF_Inside_C", "Meat Dish")
SF_IN_CHICKEN = sf_tile("SF_Inside_C", "Roast Chicken")
SF_IN_PLATE = sf_tile("SF_Inside_C", "Plate A")
SF_IN_PLATE_B = sf_tile("SF_Inside_C", "Plate B")
SF_IN_TEAPOT = sf_tile("SF_Inside_C", "Teapot & Cup")
SF_IN_FRUIT = sf_tile("SF_Inside_C", "Fruit Bowl")
SF_IN_BOOK = sf_tile("SF_Inside_C", "Book A")
SF_IN_VASE = sf_tile("SF_Inside_C", "Vase")


# Two thirds of the SF set is a modern city and the rest is a cyberpunk one,
# and both are the wrong century for this game. The rule that sorts them is
# **anything that implies electricity is out; anything that implies pressure is
# in** - a boiler, a vent and a rivet belong in Upper Clanging, a neon sign and
# a pedestrian crossing do not.
#
# So the list is written as names and resolved through the table above, which
# means it cannot drift from the sheet and it can be read by somebody who has
# never seen the art. A `Canvas(tileset=TS_CLANGING)` refuses every one of them
# at the point of drawing.
#
# Two entries are worth knowing about specifically. **"Tank" is not a fuel
# tank** - it is 戦車, a tracked military tank with a turret, and it sits two
# cells from the water tank, which is fine and is not on this list. And the
# vending machine has a twin: the cell beside it is an **ATM**, which is not
# called a vending machine and would have been missed by eye.
SF_FORBIDDEN_NAMES = {
    "SF_Outside_B": [
        # electricity
        "Neon Shop Sign (Weapon)", "Neon Shop Sign (Armor)",
        "Neon Shop Sign (Item)", "Neon Shop Sign (Pharmacy)",
        "Neon Shop Sign (Cafe)", "Neon Shop Sign (Inn)",
        "Neon Shop Sign (Market)", "Neon Shop Sign (CASINO)",
        "Neon Shop Sign (H)", "Neon Shop Sign (V)", "Neon Tube",
        "Traffic Lights (Car)", "Traffic Lights (Pedestrian)",
        "Vending Machine", "ATM", "Metal Shop Sign (Firearm)",
        "Utility Pole",
        # tarmac
        "White Line", "White Line (Crosswalk)", "Red & Black Line",
        "Traffic Cone", "Asphalt Bridge (H)", "Asphalt Bridge (V)",
        "Bridge Spar A (Asphalt, Left)", "Bridge Spar A (Asphalt, Right)",
        "Bridge Spar A (Asphalt, Center A)", "Bridge Spar A (Asphalt, Center B)",
        # the internal combustion engine
        "Car (Red)", "Car (Black)", "Car (Blue)", "Wrecked Car", "Truck", "Bus",
    ],
    "SF_Outside_C": [
        "Tank", "Bus Waiting Area", "Food Cart",
        "Rooftop Billboard A", "Rooftop Billboard B",
        # `NORTH.md` 4.4 recommends Sphere Machinery and 4.4 is wrong about
        # it. Cropped out of the sheet a cell at a time it is a white riveted
        # sphere in a cradle - which is exactly the boiler the town wants -
        # with **coloured wiring loomed out of the side of it and a console
        # lit cyan bolted to its right-hand cell**. The 3x2 block cannot be
        # used without the console and a 2x2 crop of it is a sphere with cut
        # wires hanging off. Same rule as everything else on this list:
        # anything that implies electricity is out.
        "Sphere Machinery",
    ],
    # The tarmac is not only in B. A5 interleaves asphalt floors and asphalt
    # stairs with the ones the town is actually paved with - "Asphalt Floor
    # (Ruins)" sits one cell from the rusted metal floor that Waste Land and
    # Metal Floor A live on - so the ground is as easy to get wrong by eye as
    # the street furniture is. A5 is shared with SF Inside, so this list does
    # duty in both directions.
    "SF_Outside_A5": [
        "Asphalt Bridge (H, Top)", "Asphalt Bridge (H, Center)",
        "Asphalt Bridge (H, Bottom)", "Asphalt Bridge (V, Left)",
        "Asphalt Bridge (V, Center)", "Asphalt Bridge (V, Right)",
        "Asphalt Floor (Ruins)", "Asphalt Floor (Dirty)",
        "Asphalt Floor (Dirty, Ruins)",
        "Stairs A (Asphalt, Left)", "Stairs A (Asphalt, Center)",
        "Stairs A (Asphalt, Right)", "Stairs A (Asphalt)",
        "Neon Floor", "Bumpy Tile A", "Bumpy Tile B", "Bumpy Tile C",
        "Bumpy Tile C (Ruins)",
    ],
}

# SF Inside is the same problem indoors, and `NORTH.md` 4.4 names the screens.
# The vending machine and the ATM have followed the street inside.
#
# The inside sheets need a longer list than the street did, because a modern
# *room* is much easier to build by accident than a modern street: an office
# chair and a shipping container are the same shape as a stool and a crate,
# and they sit next to each other in the palette. Everything here was looked
# at in `sampler.py sf_inside` / `sf_parlour` before being ruled out.
SF_INSIDE_FORBIDDEN_NAMES = {
    "SF_Inside_B": [
        # electricity
        "TV", "Computer", "Laptop", "Printer", "Telephone", "Tablet Device",
        "Intercom (Hanging)", "Table Clock", "Air Conditioner", "Exhaust Fan",
        "Vending Machine", "ATM", "Slot Machine",
        # safety signage, which is a design language of about 1970. The plain
        # striped Plate B is the one this town paints on a wall.
        "Warning Plate A", "Warning Plate C",
        "Warning Plate (Biohazard Mark)",
        # a teal plastic bin, and a low black three-seater that from above
        # is two dark boxes and reads as loudspeakers
        "Wastebasket", "Sofa (Down)", "Sofa (Up)",
        "Sofa (Left)", "Sofa (Right)",
        # a plastic swivel chair is not a stool, however like one it looks
        # from above
        "Office Chair (Bottom)", "Office Chair (Top)",
        "Office Chair (Left)", "Office Chair (Right)",
        # modern retail and logistics
        "Shipping Container", "Stacked Cardboard Boxes",
        "Convenience Store Shelf A", "Convenience Store Shelf B",
        "Display Shelf A", "Display Shelf B",
        # Three cupboards that pass at map scale and do not survive a cell
        # crop, and all three had shipped: "Document Shelf" is a steel case
        # whose upper half is a **backlit teal glass display** with a pink
        # stripe in it, "Medicine Shelf" is a white **pharmacy fridge** of lit
        # bottles over a bank of flat drawers, and "Locker A" has a **green
        # LCD readout and a card reader** on the door. What does all three
        # jobs is "Chest of Drawers A" - a wooden press - with "Miscellaneous
        # Item Shelf" and "Steel Shelf" for the ones that wanted open storage.
        "Document Shelf", "Medicine Shelf", "Locker A",
        # plumbed-in bathrooms and white goods. "Kitchen Counter" sounds
        # like a bench and is a four-ring **electric hob** with a control
        # panel on the front, which is the one a map-scale screenshot of a
        # galley will never show you.
        "Washing Machine", "Western Style Toilet", "Urinal", "Bathroom Sink",
        "Wash Basin", "Bathtub (V)", "Bathtub (H)", "Refrigerator",
        "Gas Stove", "Glass Table (V)", "Glass Table (H)", "Kitchen Counter",
        # the school, the hospital and the laboratory
        "School Desk (V)", "School Desk (H)", "School Chair (Bottom)",
        "School Chair (Top)", "School Chair (Left)", "School Chair (Right)",
        "Locker B (School)", "Lab Equipment", "Operating Table",
        "Hospital Bed", "Pipe Frame Bed (Ruins)",
        "Wheelchair (Left)", "Wheelchair (Right)", "Wheelchair (Bottom)",
        "Wheelchair (Fallen)", "Laser Barrier",
        # the casino
        "Poker Table", "Roulette Table",
        # tarmac, again
        "Asphalt Bridge (V)", "Asphalt Bridge (H)",
        "Bridge Spar A (Asphalt, Left)", "Bridge Spar A (Asphalt, Right)",
        "Bridge Spar A (Asphalt, Center A)", "Bridge Spar A (Asphalt, Center B)",
    ],
    "SF_Inside_C": [
        "Monitor A", "Monitor B", "Large Monitor", "ECG Monitor",
        "Server Machine", "Neon Tube", "Fluorescent Light", "Wall Speaker",
        "Emergency Alarm", "Huge Display", "Robot Arm", "IV Stand",
        "Operation Board A", "Operation Board B", "Operation Board C",
        "Operation Board D",
        # signage in a language and a century this game does not have. The
        # Room Plate is lettered, and what it is lettered in is katakana.
        "Room Plate", "EXIT Sign", "Restroom Mark (Men)",
        "Restroom Mark (Women)", "Line A", "Line B", "Road Closed",
        # the specimen cabinet. "Sphere Machinery" on this sheet is not the
        # street's boiler sphere at all - it is a dome with something pink
        # and organic under it, next to a screen.
        "Sphere Machinery", "Skeleton Model", "Biological Specimen",
        # the rest of the sheet's machinery, looked at one tile at a time on
        # a contact sheet of everything the four interiors had laid down.
        # "Meters" is an LED rack with a digital readout, "Machine A" and
        # "Broken Machine" are circuit boards in a hole, the Control Panels
        # are screens, and "Large Machine" is a console bank lit cyan. What
        # survives the rule is "Machine C" - brass, gears and pipework.
        "Meters", "Machine A", "Machine B", "Broken Machine",
        "Control Panel A", "Control Panel B", "Control Panel C",
        "Control Panel", "Large Machine", "Fan",
        # chalked, but chalked with a bar chart, a graph and a line of
        # katakana - a lecture theatre, not a notice board
        "Black Board", "White Board",
        "Outdoor Air Intake Unit", "Shutter",
        # heaps with a blue jerrycan and a yellow plastic case in them.
        # "Rubble" and "Rubble B (Metal)" are masonry and twisted iron.
        "Waste", "Scrap Metal",
        "Insect Specimen", "Anatomical Chart", "Vision Test Chart",
        "Ration",
        # a red cylinder with a flame pictogram and a moulded black hose
        "Fire Extinguisher",
        # a wall planner, gridded and lettered in katakana. A parish room
        # hangs a picture; `Painting A`-`C` are all in period.
        "Calendar", "Painting D",
        # bright magenta, and it is not damp - it reads as slime
        "Dripping",
    ],
    "SF_Outside_A5": SF_FORBIDDEN_NAMES["SF_Outside_A5"],
}


def _forbidden(table_of_names):
    out = set()
    for sheet, names in table_of_names.items():
        table = tile_names(sheet)
        base = _sheet_base(sheet)
        for name in names:
            if name not in table:
                raise KeyError("%s has no tile called %r" % (sheet, name))
            out.update(base + t for t in table[name])
    return frozenset(out)


SF_FORBIDDEN = _forbidden(SF_FORBIDDEN_NAMES)
SF_INSIDE_FORBIDDEN = _forbidden(SF_INSIDE_FORBIDDEN_NAMES)


class ForbiddenTile(Exception):
    """A tile from the wrong century was drawn on a northern map."""


# What each tileset allows, so that a `Canvas` told which tileset it is for
# can enforce both rules by itself.
#
# The roof entry is the reason this table exists. A roof is a nine-slice
# anchored at a (column, row) on the *C* sheet, and tilesets 2 and 5 have
# different C sheets - so `ROOF_BROWN`, which is (13, 3) and a plain wooden
# roof in Thistlewick, is the middle of the **Clock Tower** in Upper Clanging.
# Drawing an Outside roof on a northern map builds, validates, and puts a
# three-storey clock face on top of a cottage. It was found by doing it.
TILESET_ROOFS = {
    TS_OUTSIDE: (ROOF_GREEN, ROOF_WHITE, ROOF_GOLD, ROOF_BROWN),
    TS_COLLEGIUM: (ROOF_PURPLE, ROOF_WHITE, ROOF_GOLD, ROOF_BROWN),
    TS_CLANGING: (SF_ROOF,),
}
TILESET_FORBIDDEN = {
    TS_CLANGING: SF_FORBIDDEN,
    TS_CLANGING_IN: SF_INSIDE_FORBIDDEN,
}


# The only things that belong on the front of a house: what is nailed to the
# wall, and the holes in it. `Canvas` uses this to tell a shop sign from a
# barrel that has been drawn halfway up a wall by accident.
# `Outside_C`'s `Tapestry B`, a purple banner with a gold border, 1x2, hung
# from a rod: made to go down the face of a building's wall.
BANNER_PURPLE = sf_block("Outside_C", "Tapestry B")

WALL_MOUNTED = frozenset(
    [WINDOW, DOORWAY_DARK, SIGN_BLADE, SIGN_ORB, SIGN_ARMOR, SIGN_RING,
     SIGN_POTION, SIGN_INN, SIGN_MUG, SIGN_PLATE, SIGN_WAND, SIGN_COIN,
     SIGN_HAMMER, SIGN_SUN]
    + list(WINDOW_GLASS) + list(DOOR_DOUBLE) + list(DOOR_SHUT)
    + list(DOORWAY_ARCH)
    # Upper Clanging bolts its ventilation to the outside of the building, so
    # these are as much a part of a northern wall as a shop sign is of a
    # southern one - and so are its windows, its signs, its shutters and the
    # ladder up to its roof.
    + [SF_AIR_VENT_A, SF_AIR_VENT_B, SF_VENT, SF_MACHINE_DEVICE,
       SF_EXHAUST_WALL, SF_WALL_POSTER, SF_AIR_INTAKE, SF_SHUTTER,
       SF_ENTRANCE_A, SF_ENTRANCE_B, SF_SIGN_BLANK, SF_SIGN_WEAPON,
       SF_SIGN_ARMOR, SF_SIGN_ITEM, SF_SIGN_PHARMACY, SF_SIGN_CAFE,
       SF_SIGN_INN, SF_WARNING_PLATE]
    + list(SF_CANOPY)
    + list(SF_WINDOWS) + [t for pair in SF_WINDOWS_TALL for t in pair]
    + list(SF_LADDER) + list(SF_FIRE_ESCAPE)
    # The Collegium Arcanum hangs its colours down the front of the Hall.
    + list(BANNER_PURPLE))


# What belongs on a roof, and may therefore be drawn on layer 3 inside a
# building's footprint.
#
# On the Outside sheet this set would be empty: `STOVEPIPE` is a **star** tile,
# and `Tilemap._addSpotTile` sorts tiles into the upper or lower rendering
# layer by that flag alone rather than by which map layer they are on - so a
# star tile on layer 2 is drawn over a non-star roof on layer 3, and a
# Thistlewick chimney sits happily under the roof it comes out of.
#
# The SF chimneys are not star tiles. On layer 2 they are drawn *before* the
# roof and vanish underneath it. So a northern chimney takes layer 3, and the
# roof tile it stands on moves down to layer 2 to keep drawing behind it -
# which is what `Canvas.chimney` does.
#
# `Outside_C`'s `Chimney` is the one Outside exception: a 2x2 stone stack
# whose top row is star and whose bottom row is not, so the bottom row has the
# SF chimneys' problem and goes in through `Canvas.chimney` too. Fenmarch
# Hall's roof has two.
CHIMNEY_STACK = sf_block("Outside_C", "Chimney")          # 2x2, reading order
ROOF_MOUNTED = frozenset([SF_CHIMNEY_A, SF_CHIMNEY_B, SF_CHIMNEY_C,
                          SF_AIR_VENT_A, SF_AIR_VENT_B, SF_VENT,
                          *CHIMNEY_STACK])


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

    def __init__(self, width, height, data=None, tileset=TS_OUTSIDE):
        R.MapGrid.__init__(self, width, height, data)
        self.buildings = []          # (x, y, w, h, wall_rows)
        self._structural = 0         # >0 while the Canvas is drawing its own
        self.tileset = tileset
        self.forbidden = TILESET_FORBIDDEN.get(tileset, frozenset())
        self.roofs = TILESET_ROOFS.get(tileset, ())

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
            if part == "roof" and z == 3 and tile in ROOF_MOUNTED:
                return
            raise BuildingOverlap(
                "tile %d drawn on layer %d at (%d,%d), which is the %s of the "
                "building at (%d,%d) %dx%d. Move it off the house."
                % (tile, z, x, y, part, bx, by, bw, bh))

    def set(self, x, y, z, tile):
        # Layers 4 and 5 are the shadow bits and the region ids, not tiles, so
        # the forbidden set has no business looking at them: region 1 is the
        # number 1, and tile 1 on SF_Outside_B is a neon shop sign. Every SF
        # map that wants encounters goes through `paint_regions`, and this is
        # what stopped the first one that did.
        if z < 4 and tile in self.forbidden:
            raise ForbiddenTile(
                "tile %d at (%d,%d) is on this map's forbidden list - see "
                "SF_FORBIDDEN. It is the right sheet and the wrong century."
                % (tile, x, y))
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
        if roof not in self.roofs:
            raise ValueError(
                "%r is not a roof block on tileset %d's C sheet (it has %s); "
                "a nine-slice anchored anywhere else straddles two blocks, "
                "and an anchor borrowed from another tileset draws whatever "
                "happens to be at those cells on this one"
                % (roof, self.tileset, ", ".join(map(str, self.roofs))))
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

    def chimney(self, x, y, tile):
        """A chimney on a roof, drawn so that it is actually visible.

        Neither an SF chimney nor an SF roof is a star tile, so both are drawn
        on the lower rendering layer in map-layer order and whichever is on
        layer 3 wins. The chimney takes layer 3 and the roof tile underneath it
        drops to layer 2, which is empty on a roof and draws first.

        Both tiles block, so the roof stays as impassable as it was.

        Not on the crest, though. The top row of the nine-slice was a star
        tile, drawn on the upper rendering layer after everything on the lower
        one, so a chimney there was simply not drawn. `build_tilesets` has
        since made the crest solid and not a star, but the ridge is no place
        for a chimney anyway."""
        if tile not in ROOF_MOUNTED:
            raise ValueError("%d is not a roof fitting; see ROOF_MOUNTED" % tile)
        for bx, by, bw, bh, _ in self.buildings:
            if bx <= x < bx + bw and by <= y < by + bh and y == by:
                raise ValueError(
                    "a chimney at (%d,%d) is on the crest of the building at "
                    "(%d,%d) %dx%d. Put it a row further down the roof."
                    % (x, y, bx, by, bw, bh))
        self.set(x, y, 2, self.get(x, y, 3))
        self.set(x, y, 3, tile)

    def chimney_beside(self, x, y):
        """A chimney up the west side of the house whose top-left corner is
        (x, y): `CHIMNEY` in the cell west of the roof's top two rows, its cap
        level with the crest and its pipe bending in over the roof. Mike's
        rule from Nether Sopping and Frostwick (October 2026).

        Both cells are star tiles, so the ground under them still decides
        passage and the player walks behind the stack. The west cell has to be
        clear: another house there is refused by `set`, and anything already
        on layer 3 - a tree, a sign - raises here, since a chimney with no
        room for it is a house that should not have one."""
        if self.tileset not in (TS_OUTSIDE, TS_COLLEGIUM):
            raise ValueError("`CHIMNEY` is an Outside_B tile; tileset %d has "
                             "its own chimneys" % self.tileset)
        if not any(b[:2] == (x, y) for b in self.buildings):
            raise ValueError("no building has its corner at (%d,%d)" % (x, y))
        for dy, tile in enumerate(CHIMNEY):
            if self.get(x - 1, y + dy, 3):
                raise ValueError(
                    "the chimney beside the house at (%d,%d) would go over "
                    "tile %d at (%d,%d)" % (x, y, self.get(x - 1, y + dy, 3),
                                            x - 1, y + dy))
            self.set(x - 1, y + dy, 3, tile)

    def clock_tower(self, x, y, h=5, z=3):
        """The Clock Tower, three tiles wide and `h` tall, with its base at
        `y + h - 1`. The top two rows are fixed - the cap and the clock face -
        and the brick shaft below them repeats, so it can stand as tall as the
        street needs without growing a second clock."""
        if h < 3:
            raise ValueError("the clock tower needs at least 3 rows, got %d" % h)
        col, row = SF_CLOCK_TOWER
        self._structural += 1
        try:
            for i in range(3):
                self.set(x + i, y, z, c_tile(col + i, row))
                self.set(x + i, y + 1, z, c_tile(col + i, row + 1))
                for j in range(2, h):
                    self.set(x + i, y + j, z, c_tile(col + i, row + 2))
        finally:
            self._structural -= 1
        self.buildings.append((x, y, 3, h, 0))
        return y + h - 1

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
             void=IN_VOID, threshold=None, outside=None, tileset=TS_INSIDE):
    """A room in black space, tiled the way the stock interiors are.

    Reading down the screen: one row of wall *top*, two rows of wall *face*,
    then the floor, then the same in reverse - and the reversed pair at the
    bottom is the *outside* of the south wall, which is what makes a doorway
    read as a doorway. `door_x` cuts that gap.

    `floor_alt` lays a second floor kind in a checkerboard with the first,
    which is how the stock houses get their two-tone boards.

    `threshold` defaults to Inside_A5's wooden step, which is right for
    tileset 3 and is a slab of demonic ground on tileset 6 - a northern room
    wants `SF_THRESHOLD`.
    """
    g = Canvas(width, height, tileset=tileset)
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
    # Under the corners as well: the ring's corner tops stand over the
    # street like the rest of the south wall, so they show a face too
    # (Mike, October 2026 - it was missing at both ends of every room).
    g.fill(x1 - 1, y2 + 2, x2 + 1, y2 + 3, 0, wall_face)

    if door_x is not None:
        g.set(door_x, y2 + 1, 0, floor)
        g.set(door_x, y2 + 2, 0, threshold if threshold is not None else a5(91))
        g.set(door_x, y2 + 3, 0, outside if outside is not None else a5(91))
    return g


# The wooden flight on Inside_A5 (`Stairs A (Wood, Left)` and the right-hand
# piece; 89 is a centre for a wider one), and the standalone step, which is
# the one a one-wide flight is made of. All flagged up-and-down only.
IN_FLIGHT = (a5(88), a5(90))
IN_STEP = a5(91)

# Shadow-layer bits: a cell's four quarters, top-left 1, top-right 2,
# bottom-left 4, bottom-right 8.
SHADOW_FULL, SHADOW_LEFT = 15, 5


def _kind_of(g, x, y):
    return A(R.autotile_kind(g.get(x, y, 0)))


def _floor_like(g, cx, cy, from_y):
    """The room's floor for cell (cx, cy), read off the floor from row
    `from_y` down: the nearest floor cell an even step away, so a two-tone
    floor carries its checkerboard into a cell that was wall."""
    def floor(t):
        return (R.TILE_ID_A1 <= t < R.TILE_ID_A4
                or (R.TILE_ID_A5 < t < R.TILE_ID_A1
                    and t not in IN_FLIGHT and t != IN_STEP))
    best = None
    for r in range(from_y, min(from_y + 4, g.height)):
        for c in range(max(cx - 3, 0), min(cx + 4, g.width)):
            t = g.get(c, r, 0)
            if (c + r - cx - cy) % 2 or not floor(t):
                continue
            d = abs(c - cx) + abs(r - from_y)
            if best is None or d < best[0]:
                best = (d, t)
    if best is None:
        raise ValueError("no floor below (%d,%d) to carry up the stairwell"
                         % (cx, cy))
    return best[1]


def stairs_up(g, x, y1, rows=3, width=2, piers=(True, True)):
    """A flight going up through a room's north wall, the way Mike drew the
    Slain Wyvern's (Map 14, October 2026) and its cellar's - the single
    `Stairs A (Up)` tile laid over the boards "does not work visually".

    The treads are on layer 0, `width` wide at x and `rows` tall from y1, the
    room's first floor row, down. The two face rows above them are not wall
    but the floor upstairs seen up the stairwell, under the full shadow,
    which steps down the flight's left-hand side. Each side with a pier gets
    a column of wall round the stairwell: wall top through the face rows
    and on down beside the flight, and a face over the last two treads, so
    the pier is flush with the foot of the stairs. A side that is already
    the room's own wall wants `piers` False there.

    The floor in the stairwell is copied from the room below the flight, so
    a two-tone floor keeps its checkerboard. The way up - a transfer, or
    something that says why not - is the caller's event: nothing here stops
    the player walking up the flight into the stairwell."""
    top, face = _kind_of(g, x, y1 - 3), _kind_of(g, x, y1 - 2)
    treads = IN_FLIGHT if width == 2 else (IN_STEP,) * width
    for i in range(width):
        for y in range(y1 - 2, y1 + rows):
            for z in (1, 2, 3):
                g.set(x + i, y, z, 0)
            if y >= y1:
                g.set(x + i, y, 0, treads[i])
            else:
                g.set(x + i, y, 0, _floor_like(g, x + i, y, y1 + rows))
                g.set(x + i, y, 4, SHADOW_FULL)
        g.set(x + i, y1, 4, 7 if i == 0 else 3)
    for y in range(y1 + 1, y1 + rows):
        g.set(x, y, 4, SHADOW_LEFT)
    for side, wanted in zip((x - 1, x + width), piers):
        if not wanted:
            continue
        for y in range(y1 - 2, y1 + rows):
            for z in (1, 2, 3):
                g.set(side, y, z, 0)
            g.set(side, y, 0, top if y < y1 + rows - 2 else face)


def stairwell(g, x, y, width=2, wall_top=IN_WALL_TOP,
              wall_face=IN_WALL_FACE, sides=(True, True)):
    """The top of a flight that `stairs_up` drew on the floor below: the
    Slain Wyvern's upstairs (Map 72, Mike, October 2026). The treads, two
    rows from y, sit in a well walled off the floor round three sides and
    open on the north, where the landing is; the wall under the well shows
    its two face rows to the floor south of it, so the map wants floor at
    y + 3 and y + 4 beside the well, or the room's south wall. The wall
    beside the treads starts a row above them, alongside the landing.

    The way down is the caller's event on the well's top row; arrival from
    below is the landing above it, y - 1. A side that is already the room's
    wall wants `sides` False there."""
    def wall(c, r):
        return R.autotile_kind(g.get(c, r, 0)) in (
            R.autotile_kind(wall_top), R.autotile_kind(wall_face))
    for i in range(width):
        for r in (y, y + 1):
            for z in (1, 2, 3):
                g.set(x + i, r, z, 0)
            g.set(x + i, r, 0, IN_FLIGHT[i] if width == 2 else IN_STEP)
    g.set(x, y, 4, SHADOW_LEFT)
    g.set(x, y + 1, 4, SHADOW_LEFT)
    for side, wanted in zip((x - 1, x + width), sides):
        if wanted:
            for r in range(y - 1, y + 3):
                g.set(side, r, 0, wall_top)
    for c in range(x - 1, x + width + 1):
        g.set(c, y + 2, 0, wall_top)
        for r in (y + 3, y + 4):
            if not wall(c, r):
                g.set(c, r, 0, wall_face)


# What Mike lays over the rock beyond a cave (Under Carn Drey, October 2026):
# `Ground D (Black Floor)` on layer 1, black inside a ragged rim of rock.
DG_BLACK = A(22)


def naturalise_cave(g, seed, keep=(), rough=True, top=DG_WALL_TOP,
                    face=DG_WALL_FACE, dark=DG_BLACK):
    """Make a carved cave read as rock rather than as boxes, the way Mike
    redrew Under Carn Drey (October 2026). Two things, on a Canvas whose rooms
    are carved, walled with `dungeon_walls` and dressed:

    * `rough`: the rooms' outlines broken up - a corner cell knocked back into
      the rock here, a cell of rock opened into the room there - and the walls
      re-faced to match. Nothing is touched within a cell of a prop or an
      event (`keep` is the events' cells), nor the top row of a room whose
      face has anything hung on it, and every change is undone that would
      join two passages or part one: the cave goes where it went.
    * then the rock itself given an edge. One or two cells of it are kept
      round every room and passage, and everything beyond is `dark` on layer
      1, so the hill ends in the dark instead of filling the map.

    `seed` makes it the same cave on every build."""
    rng = random.Random(seed)
    w, h = g.width, g.height
    walls = (R.autotile_kind(top), R.autotile_kind(face))

    def rock(x, y):
        if not (0 <= x < w and 0 <= y < h):
            return True
        t = g.get(x, y, 0)
        return R.is_autotile(t) and R.autotile_kind(t) in walls

    def dressed(x, y):
        return any(g.get(x, y, z) for z in (1, 2, 3))

    near = set()
    for x, y in keep:
        near.update((x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1))
    for y in range(h):
        for x in range(w):
            if dressed(x, y) and not rock(x, y):
                near.update((x + dx, y + dy)
                            for dx in (-1, 0, 1) for dy in (-1, 0, 1))

    def floor_cells():
        return {(x, y) for y in range(h) for x in range(w) if not rock(x, y)}

    def parts(cells):
        seen, out = set(), []
        for c in sorted(cells):
            if c in seen:
                continue
            stack, part = [c], set()
            while stack:
                x, y = stack.pop()
                if (x, y) in seen or (x, y) not in cells:
                    continue
                seen.add((x, y))
                part.add((x, y))
                stack += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            out.append(part)
        return out

    def steps(cells, start, limit):
        """Walking distance from `start` to each cell, up to `limit`."""
        dist, todo = {start: 0}, [start]
        for cx, cy in todo:
            if dist[(cx, cy)] >= limit:
                continue
            for n in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                if n in cells and n not in dist:
                    dist[n] = dist[(cx, cy)] + 1
                    todo.append(n)
        return dist

    floors = floor_cells()
    count = len(parts(floors))
    if rough:
        changed = []
        candidates = []
        for x, y in sorted(floors):
            if (x, y) in near or x < 2 or y < 3 or x > w - 3 or y > h - 2:
                continue
            if g.get(x, y, 0) >= R.TILE_ID_A5 and g.get(x, y, 0) < R.TILE_ID_A1:
                continue                # stairs and the like, laid by id
            sides = [rock(x - 1, y), rock(x + 1, y), rock(x, y - 1),
                     rock(x, y + 1)]
            if rock(x, y - 1) and any(dressed(x, y - d) for d in (1, 2, 3)):
                continue                # something hangs on the face above
            if sum(sides) >= 2 and not (sides[0] and sides[1]) \
                    and not (sides[2] and sides[3]):
                candidates.append(("notch", x, y))
        for y in range(3, h - 1):
            for x in range(2, w - 2):
                if not rock(x, y) or (x, y) in near or dressed(x, y):
                    continue
                if any(dressed(x, y - d) for d in (1, 2)):
                    continue
                into = [(x - 1, y), (x + 1, y), (x, y - 1)]
                if sum((c in floors) for c in into) == 1 and \
                        (x, y + 1) not in floors:
                    candidates.append(("bulge", x, y))
        rng.shuffle(candidates)
        budget = max(2, len(candidates) // 5)
        for kind, x, y in candidates:
            if len(changed) >= budget:
                break
            # Two cells apart, or two changes make a zigzag of loose faces.
            if any(abs(cx - x) <= 2 and abs(cy - y) <= 2
                   for _, cx, cy in changed):
                continue
            if kind == "notch":
                if (x, y) not in floors:
                    continue
                trial = floors - {(x, y)}
                if len(parts(trial)) != count:
                    continue
                g.set(x, y, 0, top)
            else:
                if (x, y) in floors:
                    continue
                trial = floors | {(x, y)}
                if len(parts(trial)) != count:
                    continue
                # No short cut: everything within two cells of the new floor
                # must already be a short walk from the room it opens off.
                door = next(c for c in [(x - 1, y), (x + 1, y), (x, y - 1)]
                            if c in floors)
                # Off a room, not a passage: three cells of floor straight
                # on from the opening.
                ox, oy = door[0] - x, door[1] - y
                if (door[0] + 2 * ox, door[1] + 2 * oy) not in floors:
                    continue
                close = steps(floors, door, 6)
                if any(c not in close for c in floors
                       if abs(c[0] - x) <= 2 and abs(c[1] - y) <= 2):
                    continue
                g.set(x, y, 0, g.get(door[0], door[1], 0))
            floors = trial
            changed.append((kind, x, y))
        # Re-wall: rock over a floor is face for two rows, the rest is top.
        for y in range(h):
            for x in range(w):
                if rock(x, y):
                    g.set(x, y, 0, top)
        g.dungeon_walls(top, face)
        g.autotile(0)

    # -- the edge of the rock --------------------------------------------
    cave = {(x, y) for y in range(h) for x in range(w)
            if not (rock(x, y) and R.autotile_kind(g.get(x, y, 0)) == walls[0])}
    rim = {}
    step = 3
    for gy in range(-step, h + 2 * step, step):
        for gx in range(-step, w + 2 * step, step):
            rim[(gx, gy)] = rng.choice((1, 1, 2))

    def width_at(x, y):
        gx, gy = x - x % step, y - y % step
        return rim[(gx, gy)]

    void = set()
    for y in range(h):
        for x in range(w):
            if (x, y) in cave or dressed(x, y):
                continue
            r = width_at(x, y)
            if not any((x + dx, y + dy) in cave
                       for dx in range(-r, r + 1) for dy in range(-r, r + 1)):
                void.add((x, y))
    # No single cells of rock left standing in the dark, nor single cells of
    # dark in the rock: both read as a mistake.
    for _ in range(2):
        for y in range(h):
            for x in range(w):
                n = sum((x + dx, y + dy) in void or not (0 <= x + dx < w and
                                                         0 <= y + dy < h)
                        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                if (x, y) in void and n <= 1:
                    void.discard((x, y))
                elif (x, y) not in void and (x, y) not in cave \
                        and not dressed(x, y) and n >= 3:
                    void.add((x, y))
    for x, y in void:
        g.set(x, y, 1, dark)
    g.autotile(1, kinds={R.autotile_kind(dark)})
    return void


def guest_room(g, x1, y1, x2, y2, door_x, wall_top=IN_WALL_TOP,
               wall_face=IN_WALL_FACE, floor=None):
    """Wall off a room inside an interior that `interior()` has drawn: the
    way Mike split the Gilded Turnip (October 2026) into the bar, where
    everybody is, and a bedroom for the guests - nobody sleeps in the middle
    of the pub.

    The room is x1..x2, y1..y2 of floor in a corner of the bigger one, sharing
    its north wall (y1 is the big room's first floor row) and one side wall.
    A partition goes round its open sides - a wall-top column one cell
    outside whichever of x1 and x2 is not on the big room's ring, and a
    wall-top row under y2 - and the partition shows a face to the room below
    it, two rows, like any south wall seen from the north. `door_x` cuts the
    doorway through the partition and its face. So the big room needs at
    least one row of floor below y2 + 3, which is where you walk to the door.

    Shapes are left to the build's `shape_wall_tops`, which turns the joins
    into T-pieces and trims the faces the editor's way."""
    west = g.get(x1 - 1, y1, 0) != wall_top     # which side is open
    side = x1 - 1 if west else x2 + 1
    xa, xb = (x1 - 1, x2) if west else (x1, x2 + 1)
    for y in range(y1 - 2, y2 + 2):
        g.set(side, y, 0, wall_top)
    for x in range(xa, xb + 1):
        g.set(x, y2 + 1, 0, wall_top)
        g.set(x, y2 + 2, 0, wall_face)
        g.set(x, y2 + 3, 0, wall_face)
    under = floor if floor is not None else g.get(door_x, y2 + 4, 0)
    for y in (y2 + 1, y2 + 2, y2 + 3):
        g.set(door_x, y, 0, under)


def wide(g, x, y, z, piece):
    """Lay a piece that is several columns wide - `IN_SUNDRIES_CABINET` - with
    its west column at x."""
    for i, col in enumerate(piece):
        g.column(x + i, y, z, col)


def lone_halves(m):
    """Cells of map `m` holding one column of a `WIDE_PIECES` piece without
    the column that belongs beside it, as (x, y, tile). Inside_B only."""
    w, h, d = m["width"], m["height"], m["data"]

    def cell(x, y):
        return ({d[(z * h + y) * w + x] for z in range(4)}
                if 0 <= x < w else set())
    out = []
    for piece in WIDE_PIECES:
        for i, col in enumerate(piece):
            for row, tile in enumerate(col):
                for y in range(h):
                    for x in range(w):
                        if tile not in cell(x, y):
                            continue
                        for j, other in enumerate(piece):
                            if j != i and other[row] not in cell(x + j - i, y):
                                out.append((x, y, tile))
    return out


def four_beds(g, x1, y1, x2, door_x, bed=None, nightstand=None):
    """Four beds in a guest room the way Mike laid out the Safety Valve's
    (October 2026): two and two, against the side walls, with an aisle up the
    middle from the door. The top pair stands under the north wall at y1 and
    the bottom pair one clear row below it, at y1 + 3, so the room wants five
    rows of floor, y1..y1 + 4, and at least two columns of aisle between
    x1 and x2. A nightstand goes between the top pair, in the door's column,
    at the far end of the aisle - not in the doorway's line of sight, since
    the aisle is two wide and the door is in one of them. Four in a row along
    the back wall is a dormitory; this is an inn."""
    bed = bed or IN_BED
    if x2 - x1 < 3:
        raise ValueError("four_beds needs two columns of aisle: x %d..%d"
                         % (x1, x2))
    for x in (x1, x2):
        for y in (y1, y1 + 3):
            g.column(x, y, 2, bed)
    if nightstand is not None:
        g.set(door_x, y1, 2, nightstand)


def door_animation():
    """Open a door sprite, hold, close it, then make it transparent - the
    routine the sample uses so a door looks like it was walked through."""
    return [{"code": 17}, {"code": 15, "parameters": [3]},
            {"code": 18}, {"code": 15, "parameters": [3]},
            {"code": 19}, {"code": 37}]
