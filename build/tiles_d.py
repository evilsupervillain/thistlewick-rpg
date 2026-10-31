"""`img/tilesets/Thistlewick_D.png`: the few tiles no stock sheet has.

    python3 build/tiles_d.py

Drawn here, a pixel at a time, because nothing in the box is a doormat or a
crab's footprint (30 Oct 2026, Mike). The sheet goes in the empty **D** slot
of Outside (tileset 2) and World (tileset 1) - and so of their copies, the
Collegium's and the Overworld - by `build_game.build_tilesets`, which also
gives every tile on it flags 0: open, under characters, nothing blocked.

Like `art.py` this is not part of the build. The image and its name table are
committed; run this again only to change a tile. It is deterministic - the
fibres and the scuffing come from a seeded generator - so a re-run with no
change writes the same bytes.

The cells are local ids on the D sheet, so the tile id is `TILE_ID_D + n`;
cell 0 is left empty, the way every stock B sheet leaves it.
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(os.path.dirname(GAME), "tools", "chargen"))
import png                                  # noqa: E402

SHEET = "Thistlewick_D"
OUT = os.path.join(GAME, "img", "tilesets", SHEET + ".png")
TS = 48

DOORMAT, CRAB_H, CRAB_HOLLOW, CRAB_V = 1, 2, 3, 4
NAMES = {
    DOORMAT: "Doormat",
    CRAB_H: "Crab Tracks (H)",
    CRAB_HOLLOW: "Crab Tracks (Hollow)",
    CRAB_V: "Crab Tracks (V)",
}


def origin(n):
    """The engine's own arithmetic: a B-E sheet is two blocks of eight."""
    return (((n // 128) % 2 * 8 + n % 8) * TS, ((n % 256) // 8 % 16) * TS)


def blend(cell, x, y, rgb, a):
    """Lay `rgb` at alpha `a` (0-255) over whatever is in the cell."""
    if not (0 <= x < TS and 0 <= y < TS):
        return
    src = np.array(list(rgb) + [a], dtype=float) / 255
    dst = cell[y, x].astype(float) / 255
    out_a = src[3] + dst[3] * (1 - src[3])
    if out_a == 0:
        return
    out = (src[:3] * src[3] + dst[:3] * dst[3] * (1 - src[3])) / out_a
    cell[y, x] = np.round(np.append(out, out_a) * 255)


def doormat(rng):
    """Coir, seen from above, lying in front of a door: woven rows, a darker
    bound edge, a dark outline like every RTP prop, and a soft shadow."""
    c = np.zeros((TS, TS, 4), dtype=np.uint8)
    x0, y0, x1, y1 = 6, 4, 41, 22
    for x in range(x0 + 1, x1 + 2):                         # shadow
        blend(c, x, y1 + 1, (0, 0, 0), 70)
    for y in range(y0 + 1, y1 + 2):
        blend(c, x1 + 1, y, (0, 0, 0), 50)
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            edge = x in (x0, x1) or y in (y0, y1)
            bound = x in (x0 + 1, x0 + 2, x1 - 1, x1 - 2) or \
                y in (y0 + 1, y0 + 2, y1 - 1, y1 - 2)
            if edge:
                rgb = (74, 46, 22)
            elif bound:
                rgb = (128, 84, 40)
            else:
                base = 182 if (y - y0) % 2 else 170           # woven rows
                n = int(rng.integers(-14, 15))
                rgb = (base + n, int((base + n) * 0.74), int((base + n) * 0.42))
            c[y, x] = rgb + (255,)
    for x in range(x0 + 5, x1 - 4):                         # a pale stripe
        if x % 3:
            for y in (y0 + 5, y1 - 5):
                blend(c, x, y, (226, 196, 140), 150)
    return c


def _mark(c, x, y, rng, up):
    """One leg's stab in sand: a dark pit, with the sand it threw up as a
    paler lip on the side away from the body."""
    out = -1 if up else 1                   # away from the body
    for dx in (0, 1):
        for dy in (0, 1):
            blend(c, x + dx, y + dy * -out, (104, 76, 32), 235)
    blend(c, x + 2, y + out, (104, 76, 32), 200)        # the tip, raked out
    for dx in (-1, 0, 1, 2):
        blend(c, x + dx, y + 2 * -out, (246, 228, 166), 130)


def crab_h(rng, x_from=0, x_to=TS):
    """A crab going sideways, left to right: four legs a side, so two rows of
    stabs in fours, and between them the broad faint smear of a crab that is
    the size of a garden shed and is not lifting itself very far."""
    c = np.zeros((TS, TS, 4), dtype=np.uint8)
    for x in range(x_from, x_to):
        for y in range(20, 29):
            a = 34 if 21 <= y <= 27 else 18
            blend(c, x, y, (150, 118, 56), a)
    for step in range(x_from, x_to, 12):
        for i in range(4):
            x = step + 1 + i * 3 + int(rng.integers(0, 2))
            if x >= x_to - 1:
                continue
            _mark(c, x, 12 + int(rng.integers(-1, 2)) + (i % 2), rng, True)
            _mark(c, x, 35 + int(rng.integers(-1, 2)) - (i % 2), rng, False)
    return c


def crab_hollow(rng):
    """Where it sits: an oval scooped out of the beach, darker in the bottom
    and lipped with thrown sand, and the trail coming in from the right."""
    c = crab_h(rng, x_from=36)
    cx, cy, rx, ry = 20, 24, 16, 11
    for y in range(TS):
        for x in range(TS):
            d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
            if d <= 1:
                blend(c, x, y, (150, 118, 56), int(60 + 90 * (1 - d)))
            elif d <= 1.35 and y >= cy - 2:
                blend(c, x, y, (246, 228, 166), 140)
            elif d <= 1.25:
                blend(c, x, y, (120, 90, 40), 70)
    for k in range(10):                                     # legs, round it
        t = np.pi * (0.15 + 0.7 * (k % 5) / 4) + (np.pi if k >= 5 else 0)
        x = int(round(cx + np.cos(t) * (rx + 4)))
        y = int(round(cy - np.sin(t) * (ry + 4)))
        _mark(c, x, y, rng, y < cy)
    return c


def build():
    rng = np.random.default_rng(30_10_2026)
    sheet = np.zeros((TS * 16, TS * 16, 4), dtype=np.uint8)
    tiles = {
        DOORMAT: doormat(rng),
        CRAB_H: crab_h(rng),
        CRAB_HOLLOW: crab_hollow(rng),
    }
    tiles[CRAB_V] = np.transpose(crab_h(rng), (1, 0, 2))
    for n, cell in tiles.items():
        x, y = origin(n)
        sheet[y:y + TS, x:x + TS] = cell
    png.write(OUT, sheet)
    with open(OUT[:-4] + ".txt", "w", encoding="utf-8-sig") as f:
        for n in range(256):
            f.write("%s|\n" % NAMES.get(n, "Transparent"))
    print("wrote %s (%d tiles)" % (OUT, len(tiles)))


if __name__ == "__main__":
    build()
