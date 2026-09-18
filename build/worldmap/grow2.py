"""Thistlewick's 50x50, grown into a 120x120 world.

The old map is blitted onto an otherwise empty 120x120 canvas at (35,35), and
then **the water that is content is painted on before anything is generated**.
A layer-0 tile of 0 means "generate here", so a canvas with sea drawn in it is
a specification: worldgen fills the empty parts and leaves the sea alone.

That is what protecting the old map's own rim could not do. The ocean below
Nether Sopping and off the Lighthouse's headland is *new* territory - the old
map's southern shore is a dirt beach at row 46 and the map ends four rows
later - so without this the fill grows a continent across it.

Three passes:

  1. the coast: the old ocean rim is erased, except where KEEP_WATER says the
     water is content, so new land can come ashore;
  2. the country: everything still empty on the canvas is generated, with the
     new sites anchored in it;
  3. the middle: the mountain fence across rows 23-30 of the old map is a
     `MM.MM.MM` repeat with gaps on a fixed period, which reads as a fence
     rather than a range. Erased and redrawn as relief.

1 and 2 are one `grow`; 3 is a second one over its output.

    python3 grow2.py <seed>
"""
import json
import os
import sys
import time

sys.path.insert(0, 'tools')
import numpy as np                                             # noqa: E402

from worldgen import noise as nz                               # noqa: E402
from worldgen import pipeline, preserve, preview, spec         # noqa: E402

OUT = os.path.dirname(os.path.abspath(__file__))
SRC = 'thistlewick/data/Map008.json'
W = H = 120
AT = (35, 35)                       # the old map occupies 35..84 in both axes
RADIUS = 10

COMPOSE = {"sea": 34, "grass": 32, "snow": 11, "desert": 11, "wasteland": 5,
           "rocky": 4}

# --- old-map coordinates ---------------------------------------------------
# Water inside the old map that must not be grown into.
KEEP_WATER = [
    (26, 42, 49, 49),        # below Nether Sopping, round the Lighthouse
    (0, 0, 7, 9),            # Attempt 112's sea stack, near Upper Clanging
    (16, 44, 26, 49),        # the Isle of Uncertain Ownership
    (42, 26, 49, 35),        # the Hermit's middle distance
]

# The mountain fence, and the western mass beside it. Redrawn in pass 3.
REDRAW = [(24, 22, 47, 31), (4, 22, 12, 35)]

# Two walkable cells sealed inside the western mountain mass that nothing can
# reach - a fault in the hand-drawn map, which stage 4 refuses to build on.
SEALED = [((6, 27), (5, 27)), ((9, 27), (10, 27))]

# --- new-map coordinates ---------------------------------------------------
# Ocean painted onto the canvas before anything is generated.
PAINT_SEA = [
    (58, 85, 86, 101),       # the sea below Nether Sopping's shore
    (85, 66, 105, 92),       # off the Lighthouse's headland, and the Hermit's
    (46, 84, 64, 93),        # round the Isle of Uncertain Ownership
    (17, 30, 41, 49),        # the bay west of Upper Clanging, and the stack
]

NEW = [
    # the far north
    ("Coldbarrow",        "snow", "World_B/Temple A (Snow)",   (58, 12)),
    ("Hithermost",       "grass", "World_B/Village A",         (38, 20)),
    ("Sky Anvil",         "snow", "World_B/Giant Tree (Snow)", (82, 16)),
    ("Penultima",        "grass", "World_B/Town B",            (92, 40)),
    # the west
    ("Great Dunnage",    "grass", "World_B/Fortress City",     (22, 54)),
    ("Sable Hart",   "wasteland", "World_B/House (Town)",      (14, 66)),
    ("The Lay-By",       "grass", "World_B/Igloo",             (18, 78)),
    ("Olde Evermore",    "grass", "World_B/Village C",         (22, 92)),
    # the east
    ("Ashcombe",         "grass", "World_B/Village A",         (98, 46)),
    ("Collegium Arcanum", "grass", "World_B/School of Magic",  (106, 48)),
    ("Fairholme",        "grass", "World_B/Castle A",          (108, 70)),
    ("Little Gore",      "grass", "World_B/House (Village)",   (106, 100)),
    # the far south
    ("Gladhollow",       "grass", "World_B/Village B",         (28, 104)),
    ("Restwell",         "grass", "World_B/Town A",            (34, 82)),
    ("Weeping Bottom", "wasteland", "World_B/Temple B",        (48, 104)),
    ("Fenmarch Hall",    "grass", "World_B/Large Mansion",     (96, 106)),
    ("Cinder Fen",   "wasteland", "World_B/Trail",             (38, 112)),
    ("The Fair",        "desert", "World_B/Large Tent",        (62, 112)),
    ("Sump",            "desert", "World_B/House (Desert)",    (78, 110)),
    ("Wrong Dragon",    "desert", "World_B/Cave B",            (100, 114)),
]


def in_any(x, y, boxes):
    return any(x0 <= x <= x1 and y0 <= y <= y1 for x0, y0, x1, y1 in boxes)


def sea_mask(seed):
    """The painted ocean, with an edge worth looking at.

    A rectangle of preserved sea meets the generated coast in a straight line,
    which is exactly what it looks like. So the rectangle is eroded by a noise
    field: the requirement is "there is ocean here", and a wobbly blob answers
    it as well as a box does and does not read as a box."""
    n = nz.Noise(("coast", seed))
    field = n.perlin(W, H, (16, 16)) + 0.5 * n.perlin(W, H, (31, 31), salt=1)
    field = (field - field.min()) / max(1e-9, float(np.ptp(field)))
    mask = np.zeros((H, W), dtype=bool)
    for x0, y0, x1, y1 in PAINT_SEA:
        ys, xs = np.mgrid[0:H, 0:W]
        # How far inside the rectangle a cell is, in cells, capped at 6.
        inside = np.minimum.reduce([xs - x0, x1 - xs, ys - y0, y1 - ys])
        mask |= inside > (field * 4.0 - 1.0)
    return mask


def canvas(seed):
    """The old map on a 120x120 of nothing, with the kept water painted in.

    Returns the `Source` and the list of old-map sea cells to erase, in new
    coordinates."""
    old = json.load(open(SRC))
    ow, oh, od = old["width"], old["height"], old["data"]
    for (hx, hy), (fx, fy) in SEALED:            # the two sealed pockets
        for z in range(4):
            od[(z * oh + hy) * ow + hx] = od[(z * oh + fy) * ow + fx]
    sea_tile = od[0]                             # the old map's own open sea

    new = dict(old)
    new["width"], new["height"] = W, H
    new["data"] = [0] * (W * H * 6)
    new["events"] = [None]
    for z in range(4):
        for y in range(oh):
            for x in range(ow):
                new["data"][(z * H + y + AT[1]) * W + x + AT[0]] = \
                    od[(z * oh + y) * ow + x]
    mask = sea_mask(seed)
    for y in range(H):
        for x in range(W):
            if mask[y][x] and new["data"][y * W + x] == 0:   # never over the old map
                new["data"][y * W + x] = sea_tile
    path = os.path.join(OUT, "canvas.json")
    json.dump(new, open(path, "w"), ensure_ascii=False)
    src = preserve.read(path)

    protect = set()
    for (px, py) in src.unreadable():
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                protect.add((px + dx, py + dy))
    erase = []
    for y in range(AT[1], AT[1] + oh):
        for x in range(AT[0], AT[0] + ow):
            if src.labels[y][x] != 'sea' or (x, y) in protect:
                continue
            if in_any(x - AT[0], y - AT[1], KEEP_WATER):
                continue
            erase.append((x, y))
    return src, erase


def country(seed):
    src, erase = canvas(seed)
    anchors = [spec.Anchor(n, b, stamp=s,
                           at=spec.Region.near(a[0], a[1], RADIUS))
               for n, b, s, a in NEW]
    req = spec.WorldRequest(
        seed=seed, width=W, height=H, loop="none", compose=COMPOSE,
        exclude=["cloud", "volcanic"], anchors=anchors,
        name="The Obligatory Quest, world map")
    world = pipeline.grow(req, source=src, at=(0, 0), fill=erase)
    print("  erased %d of the old map's sea cells" % len(erase))
    return world


def middle(seed, path):
    src = preserve.read(path)
    fill = [(x, y) for y in range(H) for x in range(W)
            if in_any(x - AT[0], y - AT[1], REDRAW)
            or src.labels[y][x] == preserve.UNREADABLE]
    req = spec.WorldRequest(
        seed=seed + "-relief", width=W, height=H, loop="none",
        compose={"grass": 55, "rocky": 30, "wasteland": 15},
        exclude=["cloud", "volcanic"],
        name="The Obligatory Quest, world map")
    world = pipeline.grow(req, source=src, at=(0, 0), fill=fill)
    print("  redrew %d cells of the middle" % len(fill))
    return world


def main(argv):
    seed = argv[0] if argv else "w1"
    t = time.time()
    one = country(seed)
    one.save(OUT + "/step1-%s.json" % seed)
    two = middle(seed, OUT + "/step1-%s.json" % seed)
    two.save(OUT + "/world-%s.json" % seed)
    print("%s: %.1fs" % (seed, time.time() - t))
    preview.render(OUT + "/world-%s.png" % seed, scale=4, land=two.land,
                   plan=two.plan, hills=two.hills, world=two.world)
    print(two.report().text())


if __name__ == "__main__":
    main(sys.argv[1:])
