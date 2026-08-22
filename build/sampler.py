"""Throwaway: paint candidate tiles onto Map099 so a screenshot can settle what
they look like. Not part of the game; run it, look, then move on.

    python3 build/sampler.py walls | roofs | scenery | ground
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
    roofs_ = [K.ROOF_GREEN, K.ROOF_WHITE, K.ROOF_GOLD, K.ROOF_BROWN,
              K.ROOF_YELLOW_BRICK, K.ROOF_GREEN_FLAT,
              (8, 6), (10, 6), (13, 6), (11, 6), (8, 9), (13, 9)]
    g = K.Canvas(32, 30)
    g.fill(0, 0, 31, 29, 0, K.GRASS)

    def draw(g, x, y, roof):
        g.building(x, y, 4, 6, wall=K.WALL_PLANK, roof=roof)
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


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "walls"
    g, note = {"walls": walls, "roofs": roofs, "scenery": scenery,
               "ground": ground, "world": world}[which]()
    tileset = K.TS_WORLD if which == "world" else K.TS_OUTSIDE
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


