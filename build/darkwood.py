"""The Gloamwood's dark-forest style, as a drawing kit for a map in it.

Mike redrew the Gloamwood by hand in October 2026 (`handdrawn.py`), and this
is how it is built, read back off his tiles so that a second map can be drawn
the same way - the deep wood, Map 10, is the first:

* **The forest is a wall, not a scattering of trees.** `Forest A` is an A4
  autotile pair on Outside: kind 114 is the canopy, seen from above, black
  inside a leafy edge; kind 122 is the trunks. Lay canopy everywhere the wood
  is solid, carve the ground out of it, and `Canvas.dungeon_walls` makes the
  two rows of canopy over any ground into trunks - so every clearing has a
  wall of trees along its north side and a leafy edge on the other three,
  exactly as a room has a north wall face. The interior of the canopy is
  passable (its shape 0 is `0xe00`); nobody can reach it.
* **The ground is meadow with a dirt path through it**, `Meadow` and `Dirt
  (Meadow)`, autotiled, so the path's edges are soft.
* **Layer 1 is undergrowth**: `Bush` (A2 kind 20) in clumps, mostly along the
  foot of the trees, and `Moss` (kind 39), a darker grass in strips beside the
  canopy edge.
* **The trunks are dressed**: vines over both trunk rows (`Wall Vines A-C`,
  `Vines A`), a fern on the upper row (`Wall Fern`), moss on the lower (`Wall
  Moss`). Mike's map dresses about a third of its trunk columns. Never two
  dressed columns side by side, so the trunks still read as trees.
* **Shadows** fall as they do indoors: the left half of a ground cell whose
  west and north-west neighbours are both forest.

A map is a plan - one string per row, one character per cell - plus props
placed by hand. `draw()` does the rest, deterministically, from a seed.
"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mapkit as K
import rmmzdata as R

CANOPY = K.A(114)                 # Forest A, the top
TRUNKS = K.A(122)                 # Forest A, the face
MEADOW = K.A(16)
DIRT = K.A(17)                    # Dirt (Meadow)
WATER = K.A(0)                    # Water A (Meadow)
BUSH = K.A(20)                    # layer 1
MOSS = K.A(39)                    # layer 1
REEDS = K.A(3)                    # Swamp Grass B, layer 1 over water

# Props, by the cells Mike's map used - several of the sheet's names cover
# more than one prop, so these are ids, top row first.
VINES = [(49, 57), (50, 58), (51, 59), (20, 28)]   # Wall Vines A-C, Vines A
FERN = 64                         # Wall Fern, the upper trunk row
TRUNK_MOSS = 56                   # Wall Moss, the lower trunk row
TREE = (157, 165)                 # a small conifer, 1x2
LARGE_TREE = ((176, 177), (184, 185))
DEAD_TREE = (232, 240)            # 1x2
DEAD_SHRUB = 241
STUMP = 156
LOG = 164                         # Fallen Log
BOULDER = 159
MUSHROOMS = 235                   # Mushrooms B, red caps
MUSHROOMS_PALE = 234
GRASS = (152, 153, 154)           # tufts
SUSUKI = 251
FERN_PLANT = 246
DEAD_BEANSTALK = 224
BONES = K.c_tile(0, 3)            # Outside_C `Bones A`

LEGEND = {
    "#": (CANOPY, 0),
    ".": (MEADOW, 0),
    ",": (DIRT, 0),
    "~": (WATER, 0),
    "b": (MEADOW, BUSH),
    "m": (MEADOW, MOSS),
    "r": (WATER, REEDS),
}
SHADOW_LEFT = 1 | 4


def _forest(t):
    return R.is_autotile(t) and R.autotile_kind(t) in (114, 122)


def shape_trunks(g):
    """Re-decide where a run of trunks starts and stops, the way the editor
    does it on Mike's Gloamwood rather than the way `MapGrid.autotile` does.

    A face cell's left and right edges: none beside canopy (the top and face
    of `Forest A` are one wall), none beside trunks in the same row of the
    face, an edge on the *upper* face row beside a face that started a row
    higher, and an edge beside anything that is not forest. That is 151 of
    the 156 sides on his map that have a canopy or trunk beside them; the
    other five go both ways under identical neighbours, which is the order
    he painted them in. Up and down stay as autotiled."""
    def kind(x, y):
        if not (0 <= x < g.width and 0 <= y < g.height):
            return None
        t = g.get(x, y, 0)
        return R.autotile_kind(t) if R.is_autotile(t) else None

    def upper(x, y):
        return kind(x, y + 1) == 122
    for y in range(g.height):
        for x in range(g.width):
            t = g.get(x, y, 0)
            if kind(x, y) != 122:
                continue
            shape = R.autotile_shape(t) & ~(1 | 4)
            for dx, bit in ((-1, 1), (1, 4)):
                n = kind(x + dx, y)
                if n == 114:
                    continue
                if n == 122 and (upper(x + dx, y) == upper(x, y)
                                 or not upper(x, y)):
                    continue
                if n is None and not (0 <= x + dx < g.width):
                    continue                     # the map's edge is forest
                shape |= bit
            g.set(x, y, 0, R.make_autotile(122, shape))


def draw(plan, seed, dress=0.4):
    """A Canvas of the plan, its trunks found, everything autotiled, the
    trunks dressed with probability `dress` per eligible column, and the
    shadows cast. Props are the caller's, after."""
    h, w = len(plan), len(plan[0])
    assert all(len(row) == w for row in plan), "ragged plan"
    g = K.Canvas(w, h)
    for y, row in enumerate(plan):
        for x, ch in enumerate(row):
            ground, under = LEGEND[ch]
            g.set(x, y, 0, ground)
            if under:
                g.set(x, y, 1, under)
    g.dungeon_walls(CANOPY, TRUNKS)
    g.autotile(0)
    shape_trunks(g)
    g.autotile(1)

    rng = random.Random(seed)
    last = -2
    for y in range(h - 1):
        for x in range(w):
            top, below = g.get(x, y, 0), g.get(x, y + 1, 0)
            if not (_forest(top) and R.autotile_kind(top) == 122
                    and R.autotile_kind(below) == 122):
                continue
            if x == last + 1 or rng.random() >= dress:
                continue
            last = x
            pick = rng.random()
            if pick < 0.6:
                upper, lower = rng.choice(VINES)
                g.set(x, y, 3, upper)
                g.set(x, y + 1, 3, lower)
            elif pick < 0.85:
                g.set(x, y, 3, FERN)
            else:
                g.set(x, y + 1, 3, TRUNK_MOSS)

    for y in range(h):
        for x in range(w):
            if _forest(g.get(x, y, 0)):
                continue
            if x > 0 and y > 0 and _forest(g.get(x - 1, y, 0)) \
                    and _forest(g.get(x - 1, y - 1, 0)):
                g.set(x, y, 4, SHADOW_LEFT)
    return g


def tall(g, x, y, prop, z=3):
    """A 1x2 prop standing on (x, y): its top drawn in the cell above."""
    top, base = prop
    g.set(x, y - 1, z, top)
    g.set(x, y, z, base)


def large_tree(g, x, y, z=3):
    """The 2x2 `Large Tree`, standing on (x, y) and (x + 1, y)."""
    (a, b), (c, d) = LARGE_TREE
    g.set(x, y - 1, z, a)
    g.set(x + 1, y - 1, z, b)
    g.set(x, y, z, c)
    g.set(x + 1, y, z, d)
