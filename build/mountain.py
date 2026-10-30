"""Maps 73-77: the Stair, behind the Door into the Mountain (P4d).

`../POSTGAME.md` section 9 is the design, and `../COMPANIONS.md` section 8
what the game had already fixed: the board says NO ADMITTANCE WITHOUT A LAMP,
the hook under it is empty, and Sir Dunstable borrowed the lamp ("Back
directly. - D."). Behind the Door is "a stair going down into a dark that does
not stop", and this is that stair, five maps of it. The bottom is P4e's.

* **The lamp** is the one off the hook, and after the ending Sir Dunstable
  lends it on (`dunstable_pages`): what kept the Door shut was always manners,
  and the ending is when they stop applying. The Door's published refusal is
  page 0 still; a page on the item beats it (`door_pages`).
* **Dark but for the lamp.** Every map's note carries `<lamplight>`, and
  `js/plugins/TOQ_Mountain.js` draws the dark with a small circle of light
  round the party. Everything past four cells is found by walking up to it.
* **Dunstable's chalk marks** run down the walls, D. 1 at the Door to D. 212
  on the last map, each a little further down than the last - he goes in
  every day at a quarter past four, and Brother Quillon's number "in the low
  two hundreds" is this one. Past D. 212, nobody has been. They are drawn
  (`draw_art` writes `!Chalk`, one numbered mark a frame) and read. **Nothing
  in them settles whether he is alive**: he goes in, he comes back, nothing
  happened.
* **The schedule** inside the Door lists the Stair's hazards by order of the
  parish, one to five - they are the encounters (`db.build_mountain`) - and
  item six, "anything else: NOT ANTICIPATED", which is what P4e finds.
* **Continuance.** Every map's note carries `<continuance>` too: a random
  encounter lost here sends the party back in through the chapel porch
  (`continuance`, common event 7), and so does losing to the warden, by his
  own lose branch. It is the only place in the game that happens.

Each map is a plan, built by `_plan` from boxes on solid rock, one character
a cell:

    '#'  rock; `dungeon_walls` decides which of it is face
    '.'  floor, `Ground C (Rock Cave)`;  ','  the darker floor
    '='  the treads of a flight, `Stairs B (Rock Cave)`, open only up and
         down; a run of them across a row is one flight, left to right
    '~'  water;  'o'  a hole
    'u'  the way up, a tread at the top of the map (on the first map, the
         floor inside the Door);  'd'  the way down, a tread at the bottom
    a-z  floor with an event on it, named in `SPOTS`
    A-Z  rock with an event on it: a chalk mark, a board, a hook. Always the
         cell above a floor cell, which makes it the lower row of a face, so
         it is read standing below it, facing the wall.
"""
import os
import sys

import mapkit as K
import rmmzdata as R

import db
import q_spare
import story as S
from places import MAP_STAIR, MAP_BOTTOM, MAP_HITHERMOST, MAP_CONTINUANCE

# The Stair's five maps and the bottom (P4e), which is drawn the same way and
# indexed with them: plan 5 is Map 78.
MAPS = MAP_STAIR + (MAP_BOTTOM,)
BOTTOM = len(MAP_STAIR)

# The Dungeon sheet's rock cave, all one family (`Wall B`, `Ground C`, `Dark
# Ground C`, `Stairs B`, `Hole C`, `Water D`, all "(Rock Cave)").
ROCK, FACE = K.A(81), K.A(89)
FLOOR, DARK_FLOOR = K.A(24), K.A(26)
HOLE = K.A(28)
WATER = K.A(10)
TREAD_L, TREAD_C, TREAD_R, TREAD = K.a5(44), K.a5(45), K.a5(46), K.a5(47)

GRAVEL = K.sf_tile("Dungeon_B", "Gravel B (Rock Cave)")
BOULDER = K.sf_tile("Dungeon_B", "Boulder B (Rock Cave)")
BONES = K.sf_tile("Dungeon_B", "Bones A")
CUP = K.borrowed("Inside_C", "Cup (Lower Left)")

CHALK_SHEET = "!Chalk"
HALF_WAY_SHEET = "!$Half_Way"       # three cells wide, cut into the rock
STAIR_BGM = "Dungeon3"
NOTE = "<lamplight>\n<continuance>"

# Where the Stair comes out at the top: the road under the Door, at
# Hithermost (`hithermost.MOUNTAIN_AT` is the Door's own cell, (17, 5)).
DOOR_STEP = (17, 6)
# Where the porch puts you, in the Chapel of Continuance: inside its door,
# facing the lectern (`hithermost.ROOM`).
PORCH = (7, 13)
STAIR_COURIER = (17, 3)     # SPA-3: the west end of the landing, off the way


# ================================================================== plans ==
def _plan(w, h, *ops, seed=0):
    """A plan from boxes on solid rock: `(x1, y1, x2, y2, ch)` fills, and
    `(x, y, ch)` is one cell. `ch` "c" is a gallery: floor, with its outer
    rows and columns broken into runs of rock and floor, so it reads as a
    passage through rock and not as a room. Then the darker floor is laid in
    blobs over the floor (a few rounds of a cellular automaton), and a
    gallery's ragged edge is not allowed to cut off the foot of a flight or
    the floor under a mark."""
    import random
    rng = random.Random(seed)
    rows = [["#"] * w for _ in range(h)]
    ragged = []

    def runs(n):
        out, on = [], False
        while len(out) < n:
            out += [on] * rng.randint(2, 5)
            on = not on
        return out[:n]
    for op in ops:
        if len(op) == 3:
            x, y, ch = op
            rows[y][x] = ch
            continue
        if len(op) == 6:                    # a pool or a hole: an oval
            x1, y1, x2, y2, ch, _ = op
            cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
            rx, ry = (x2 - x1) / 2 + 0.5, (y2 - y1) / 2 + 0.5
            for y in range(y1, y2 + 1):
                for x in range(x1, x2 + 1):
                    d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
                    if d <= 1 + rng.uniform(-0.25, 0.1):
                        rows[y][x] = ch
            # no specks of rock left standing in it
            for y in range(y1, y2 + 1):
                for x in range(x1 + 1, x2):
                    if rows[y][x] != ch and rows[y][x - 1] == ch and (
                            rows[y][x + 1] == ch or rows[y][x + 2] == ch):
                        rows[y][x] = ch
            continue
        x1, y1, x2, y2, ch = op
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                rows[y][x] = "." if ch == "c" else ch
        if ch != "c":
            continue
        for y, edge in ((y1, runs(x2 - x1 + 1)), (y2, runs(x2 - x1 + 1))):
            for x, on in zip(range(x1, x2 + 1), edge):
                if not on and x in (x1, x2) or not on and rng.random() < 0.8:
                    rows[y][x] = "#"
                    ragged.append((x, y))
        for x, edge in ((x1, runs(y2 - y1 - 1)), (x2, runs(y2 - y1 - 1))):
            for y, on in zip(range(y1 + 1, y2), edge):
                if not on:
                    rows[y][x] = "#"
                    ragged.append((x, y))
    # the feet of every flight, and the floor under every mark
    for y in range(h):
        for x in range(w):
            c = rows[y][x]
            if c.isupper() and y + 1 < h and rows[y + 1][x] == "#":
                rows[y + 1][x] = "."
            if c == "=":
                for ny in (y - 1, y + 1):
                    if 0 <= ny < h and rows[ny][x] == "#":
                        rows[ny][x] = "."
    # and nothing the ragged edges cut off: put rock back to floor, nearest
    # the part that is reached first, until everything is
    def reach():
        walk = {(x, y) for y in range(h) for x in range(w)
                if rows[y][x] in ".,=ud" or rows[y][x].islower()
                and rows[y][x] != "o"}
        start = next((x, y) for y in range(h) for x in range(w)
                     if rows[y][x] == "u")
        seen, todo = {start}, [start]
        while todo:
            x, y = todo.pop()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (x + dx, y + dy)
                if n in walk and n not in seen and not (dx and (
                        rows[y][x] in "=ud" or rows[n[1]][n[0]] in "=ud")):
                    seen.add(n)
                    todo.append(n)
        return walk, seen
    def wanted(walk):
        out = {c for c in walk if rows[c[1]][c[0]] not in ".,"}
        out |= {(x, y + 1) for y in range(h - 1) for x in range(w)
                if rows[y][x].isupper()}
        return out
    while True:
        walk, seen = reach()
        if wanted(walk) <= seen:
            for x, y in walk - seen:            # pockets nobody can reach
                rows[y][x] = "#"
            break
        near = [c for c in ragged if rows[c[1]][c[0]] == "#" and any(
            (c[0] + dx, c[1] + dy) in seen
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
        bridge = [c for c in near if any(
            (c[0] + dx, c[1] + dy) in walk - seen
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
        lost = wanted(walk) - seen
        x, y = bridge[0] if bridge else min(near, key=lambda c: min(
            abs(c[0] - t[0]) + abs(c[1] - t[1]) for t in lost))
        rows[y][x] = "."
    # the darker floor: a blob round one floor cell in every forty or so
    floor = [(x, y) for y in range(h) for x in range(w) if rows[y][x] == "."]
    for x, y in rng.sample(floor, len(floor) // 40):
        r = rng.choice((1, 1, 2))
        for dy in range(-r, r + 1):
            for dx in range(-r - 1, r + 2):
                if abs(dx) + abs(dy) <= r + rng.choice((0, 0, 1)) and (
                        0 <= y + dy < h and 0 <= x + dx < w
                        and rows[y + dy][x + dx] == "."):
                    rows[y + dy][x + dx] = ","
    return ["".join(r) for r in rows]


PLANS = [
    # 73, The Stair. In at the Door, the schedule and D. 1 either side of it,
    # and the first long flight straight down into the dark. A hall, a wider
    # flight, a gallery with another hook on the wall (another lamp gone),
    # and two more switchbacks to the way on down.
    _plan(40, 48,
          (18, 2, 20, 2, "."), (17, 3, 21, 3, "."), (18, 4, 20, 4, "."),
          (19, 1, "u"), (18, 1, "S"), (20, 1, "A"),
          (19, 5, 19, 10, "="),
          (13, 11, 28, 14, "c"),
          (14, 10, "B"), (26, 10, "C"), (17, 13, "a"),
          (25, 15, 28, 19, "="),
          (25, 20, 28, 20, "."), (5, 21, 32, 23, "c"),
          (6, 20, "H"),
          (8, 24, 9, 28, "="),
          (23, 24, 25, 25, "."), (24, 25, "b"),
          (3, 29, 26, 31, "c"),
          (4, 28, "D"), (16, 28, "E"),
          (22, 32, 23, 37, "="),
          (14, 38, 35, 40, "c"), (33, 37, "F"),
          (31, 41, 31, 47, "="), (31, 46, "d"), seed=7301),

    # 74, Further Down. Along a ledge above a hole with no bottom anybody
    # has looked for, past the flat rock where he has his tea (D. 61), and
    # down three flights to a long one.
    _plan(40, 48,
          (31, 0, 31, 5, "="), (31, 1, "u"),
          (20, 6, 36, 8, "c"), (22, 5, "G"),
          (33, 9, 34, 11, "="),
          (4, 12, 35, 16, "c"), (8, 12, 27, 15, "o", "oval"),
          (6, 13, "t"), (5, 11, "H"), (30, 11, "I"),
          (5, 17, 6, 22, "="),
          (3, 23, 24, 25, "c"), (20, 22, "J"),
          (3, 25, "a"),
          (22, 26, 22, 31, "="),
          (12, 32, 30, 34, "c"), (14, 31, "K"),
          (13, 35, 13, 47, "="), (13, 46, "d"), seed=7302),

    # 75, The Half-Way Landing. A short gallery, a flight, and a great flat
    # chamber with HALF WAY cut over it and the warden of it standing at the
    # head of the only way on (D. 100 says half way; D. 101 says not).
    _plan(44, 44,
          (13, 0, 13, 5, "="), (13, 1, "u"),
          (8, 6, 18, 7, "."), (10, 5, "K"),
          (16, 8, 17, 11, "="),
          (6, 12, 37, 24, "c"),
          (20, 12, 22, 12, "."), (21, 11, "W"), (8, 11, "L"), (30, 11, "M"), (34, 11, "N"),
          (35, 24, "w"), (37, 22, "v"),
          (35, 25, 35, 30, "="),
          (20, 31, 40, 33, "c"), (39, 32, "a"),
          (22, 34, 22, 43, "="), (22, 42, "d"), seed=7303),

    # 76, Still Going. Water: the flight comes down beside a black pool, a
    # ledge along the foot of it, and on down. Wet, says D. 150; still wet,
    # says D. 177.
    _plan(40, 48,
          (22, 0, 22, 5, "="), (22, 1, "u"),
          (14, 6, 30, 8, "c"), (16, 5, "O"),
          (29, 9, 29, 15, "="),
          (3, 11, 29, 16, "~", "oval"), (3, 16, 36, 17, "."), (33, 15, "P"),
          (4, 18, 5, 23, "="),
          (3, 24, 26, 27, "c"), (10, 23, "Q"),
          (24, 27, "a"),
          (25, 28, 25, 33, "="),
          (18, 34, 38, 36, "c"), (36, 33, "R"),
          (20, 37, 20, 47, "="), (20, 46, "d"), seed=7304),

    # 77, D. 212. The marks thin out: a few days between each, then one. The
    # last is on the last landing, and past it the flight goes on down.
    _plan(40, 50,
          (20, 0, 20, 7, "="), (20, 1, "u"),
          (12, 8, 28, 10, "c"), (14, 7, "A"),
          (13, 11, 13, 17, "="),
          (5, 18, 22, 20, "c"), (20, 17, "B"),
          (7, 21, 8, 27, "="),
          (6, 28, 34, 30, "c"), (30, 27, "C"),
          (32, 27, "D"),
          (33, 31, 33, 38, "="),
          (26, 39, 36, 41, "c"), (34, 38, "E"),
          (28, 42, 28, 49, "="), (28, 48, "d"), seed=7305),

    # 78, the Bottom (P4e). One more flight, and the dark stops: a round
    # chamber, lit, with lamps on every ledge, and in the middle of it the
    # one thing on the schedule nobody anticipated, which has been getting
    # ready for company for a very long time.
    _plan(40, 30,
          (20, 0, 20, 7, "="), (20, 1, "u"),
          (18, 8, 22, 9, "."),
          (11, 9, 29, 27, ".", "oval"),
          (20, 19, "m"), seed=7306),
]

NAMES = ["The Stair", "The Stair - Further Down", "The Stair - Half Way",
         "The Stair - Still Going", "The Stair - D. 212",
         "The Bottom of the Stair"]
BOTTOM_NAME = NAMES[BOTTOM]

# What a random encounter is, map by map: the schedule's items one to four,
# deeper ones further down. The warden is not among them; there is one of
# him, and he is met.
ENCOUNTERS = [
    [(db.TR_DARK, 6), (db.TR_DRAUGHT, 4)],
    [(db.TR_DARK, 4), (db.TR_DRAUGHT, 4), (db.TR_ECHO, 3)],
    [(db.TR_ECHO, 4), (db.TR_DRAUGHT, 3), (db.TR_PASSING, 3)],
    [(db.TR_ECHO, 3), (db.TR_COMING_UP, 4), (db.TR_PASSING, 4)],
    [(db.TR_COMING_UP, 4), (db.TR_PASSING, 4), (db.TR_DRAUGHT, 3),
     (db.TR_DARK, 3)],
    [],                                 # the bottom: nothing comes down
]
ENCOUNTER_STEP = 30
BGS = ["Darkness", "Darkness", "Wind1", "Drips", "Darkness", ""]
BOTTOM_BGM = "Dungeon4"                 # Mike's choice; the lamps do the warmth
BOTTOM_BATTLE_BGM = "Battle8"           # its own fight, not the encounter music
BOTTOM_NOTE = "<continuance>"           # no <lamplight>: the dark stops

def cells(i, ch):
    """Every cell of plan `i` (0 is Map 73) holding `ch`."""
    return [(x, y) for y, row in enumerate(PLANS[i]) for x, c in enumerate(row)
            if c == ch]


def at(i, ch):
    found = cells(i, ch)
    assert len(found) == 1, (MAPS[i], ch, found)
    return found[0]


def _is_tread(i, c):
    return c in "=d" or (c == "u" and i > 0)


# ================================================================ drawing ==
def draw(i):
    plan = PLANS[i]
    h, w = len(plan), len(plan[0])
    g = K.Canvas(w, h, tileset=K.TS_DUNGEON)
    g.fill(0, 0, w - 1, h - 1, 0, ROCK)
    for y, row in enumerate(plan):
        for x, c in enumerate(row):
            if c in "#" or c.isupper():
                continue
            g.set(x, y, 0, {",": DARK_FLOOR, "~": WATER, "o": HOLE}.get(
                c, FLOOR))
    g.dungeon_walls(ROCK, FACE)
    g.autotile(0)
    for y, row in enumerate(plan):
        for x, c in enumerate(row):
            if not _is_tread(i, c):
                continue
            left = x > 0 and _is_tread(i, row[x - 1])
            right = x < w - 1 and _is_tread(i, row[x + 1])
            g.set(x, y, 0, {(False, False): TREAD, (False, True): TREAD_L,
                            (True, True): TREAD_C, (True, False): TREAD_R}[
                                (left, right)])
    for x, y, tile in props(i):
        g.set(x, y, 3, tile)
    keep = [(x, y) for y, row in enumerate(plan) for x, c in enumerate(row)
            if c.isalpha() or c == "="]
    if i == BOTTOM:
        keep += [c for group in lamps() for c in group]
    K.naturalise_cave(g, seed=7300 + i, keep=keep, top=ROCK, face=FACE)
    return g


def _reach(i, blocked=()):
    """The cells of plan `i` a player can walk to from the way in: a flight
    is walked up and down only, the rest four ways."""
    plan = PLANS[i]
    walk = {(x, y): c for y, row in enumerate(plan)
            for x, c in enumerate(row)
            if (c in ".,=ud" or c.islower() and c != "o")
            and (x, y) not in blocked}
    start = at(i, "u")
    seen, todo = {start}, [start]
    while todo:
        x, y = todo.pop()
        tread = _is_tread(i, walk[(x, y)])
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + dx, y + dy)
            if n not in walk or n in seen:
                continue
            if dx and (tread or _is_tread(i, walk[n])):
                continue
            seen.add(n)
            todo.append(n)
    return seen


def _wanted(i):
    """Everything on plan `i` that has to be reached: the way down, every
    event on the floor, and the floor under every mark."""
    plan = PLANS[i]
    out = set(cells(i, "d"))
    for y, row in enumerate(plan):
        for x, c in enumerate(row):
            if c.islower() and c not in "ou":
                out.add((x, y))
            if c.isupper():
                out.add((x, y + 1))
    return out


def props(i):
    """Gravel, which is walked over, here and there on the floor; and a few
    boulders, in the cells with the most rock round them, wherever one can
    stand without cutting anything off or sitting beside a flight or an
    event."""
    import random
    rng = random.Random(9100 + i)
    plan = PLANS[i]
    h, w = len(plan), len(plan[0])
    floor = [(x, y) for y, row in enumerate(plan) for x, c in enumerate(row)
             if c in ".,"]
    out = [(x, y, GRAVEL) for x, y in floor if rng.random() < 0.035]

    def rock(x, y):
        return not (0 <= x < w and 0 <= y < h) or plan[y][x] == "#"

    def busy(x, y):
        return any(0 <= x + dx < w and 0 <= y + dy < h
                   and plan[y + dy][x + dx] not in ".,#"
                   for dx in (-1, 0, 1) for dy in (-1, 0, 1))
    nooks = [(x, y) for x, y in floor if not busy(x, y) and sum(
        rock(x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)) >= 5]
    rng.shuffle(nooks)
    blocked, wanted = set(), _wanted(i)
    if i == BOTTOM:                     # swept, for company
        nooks = []
    for x, y in nooks:
        if len(blocked) >= 6:
            break
        if not wanted <= _reach(i, blocked | {(x, y)}):
            continue
        blocked.add((x, y))
        out = [p for p in out if p[:2] != (x, y)]
        out.append((x, y, BOULDER))
    return out


def check_plans():
    """Every wall event is the lower row of a face, and everything that has
    to be reached is reached from the way in."""
    for i, plan in enumerate(PLANS):
        assert len({len(r) for r in plan}) == 1, MAPS[i]
        h = len(plan)
        for y, row in enumerate(plan):
            for x, c in enumerate(row):
                if c.isupper():
                    assert y + 1 < h and plan[y + 1][x] in ".,", (
                        MAPS[i], c, x, y)
        missing = _wanted(i) - _reach(i)
        assert not missing, (MAPS[i], sorted(missing))
    lamps()                             # asserts the bottom's lamps block nothing


def lamps():
    """The bottom's lamps, dozens, every one lit: one on the wall over every
    other cell of the chamber's north side, where the rock has a face to
    hang it on, and a standing lamp on every other cell round the rest of
    its edge - none of them where it cuts anything off, beside the foot of
    the stair, or in the way of what lives here. Returns (wall, standing)."""
    plan = PLANS[BOTTOM]
    h, w = len(plan), len(plan[0])
    sx, _ = at(BOTTOM, "u")
    mx, my = at(BOTTOM, "m")

    def floor(x, y):
        return 0 <= x < w and 0 <= y < h and plan[y][x] in ".,"

    def rock(x, y):
        return not (0 <= x < w and 0 <= y < h) or plan[y][x] == "#"
    face = sorted((x, y) for y in range(1, h - 1) for x in range(w)
                  if rock(x, y) and rock(x, y - 1) and floor(x, y + 1)
                  and abs(x - sx) > 2)
    wall = face[::2]
    import math
    edge = [(x, y) for y in range(h) for x in range(w)
            if floor(x, y) and not rock(x, y - 1)
            and any(rock(x + dx, y + dy)
                    for dx, dy in ((1, 0), (-1, 0), (0, 1)))
            and not (abs(x - sx) <= 3 and y <= 11)
            and not (abs(x - mx) <= 2 and abs(y - my) <= 2)]
    edge.sort(key=lambda c: math.atan2(c[1] - h / 2, c[0] - w / 2))
    standing, wanted = [], _wanted(BOTTOM)
    for c in edge[::2]:
        if wanted <= _reach(BOTTOM, set(standing) | {c}):
            standing.append(c)
    assert len(wall) + len(standing) >= 24, (len(wall), len(standing))
    return wall, standing


# ===================================================================== art ==
# Chalk: a 3x5 pixel font, drawn at double size, white and patchy.
_GLYPHS = {
    "D": ["110", "101", "101", "101", "110"],
    ".": ["0", "0", "0", "0", "1"],
    " ": ["0", "0", "0", "0", "0"],
    "0": ["111", "101", "101", "101", "111"],
    "1": ["010", "110", "010", "010", "111"],
    "2": ["111", "001", "111", "100", "111"],
    "3": ["111", "001", "011", "001", "111"],
    "4": ["101", "101", "111", "001", "001"],
    "5": ["111", "100", "111", "001", "111"],
    "6": ["111", "100", "111", "101", "111"],
    "7": ["111", "001", "010", "010", "010"],
    "8": ["111", "101", "111", "101", "111"],
    "9": ["111", "101", "111", "001", "111"],
}


def chalk_slot(n):
    """Where mark number `n`'s picture is on `!Chalk`: the sheet's eight
    characters have twelve frames each, and every mark has one of its own,
    in the order `MARKS` lists them."""
    k = [m[0] for m in all_marks()].index(n)
    return k // 12, (2, 4, 6, 8)[k % 12 // 3], k % 3


def draw_art():
    """Writes `!Chalk`: one cell per chalk mark, its number in Dunstable's
    hand. Not part of the data build: run this module to redraw it."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..",
                                    "tools", "chargen"))
    import random
    import numpy as np
    import png
    rng = random.Random(212)
    sheet = np.zeros((2 * 4 * 48, 4 * 3 * 48, 4))
    for n, *_ in all_marks():
        ch, d, p = chalk_slot(n)
        cx, cy = ch % 4 * 3 * 48, ch // 4 * 4 * 48
        x0 = cx + p * 48
        y0 = cy + (d // 2 - 1) * 48
        text = "D. %d" % n
        width = sum(len(_GLYPHS[c][0]) * 2 + 2 for c in text) - 2
        x = x0 + (48 - width) // 2
        y = y0 + 16 + rng.randint(-2, 2)
        for c in text:
            glyph = _GLYPHS[c]
            lift = rng.randint(-1, 1)
            for gy, line in enumerate(glyph):
                for gx, bit in enumerate(line):
                    if bit != "1":
                        continue
                    for sy in (0, 1):
                        for sx in (0, 1):
                            if rng.random() < 0.12:
                                continue
                            a = rng.choice((150, 190, 220, 235))
                            sheet[y + lift + gy * 2 + sy,
                                  x + gx * 2 + sx] = (236, 232, 218, a)
            x += len(glyph[0]) * 2 + 2
        # the underline he puts under every one, as if it were a signature
        for ux in range(x0 + (48 - width) // 2 - 1,
                        x0 + (48 + width) // 2 + 1):
            if rng.random() < 0.8:
                sheet[y + 13 + (ux % 7 == 0), ux] = (236, 232, 218, 170)
    game = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    path = os.path.join(game, "img", "characters", CHALK_SHEET + ".png")
    png.write(path, np.clip(sheet, 0, 255).round().astype(np.uint8))
    print("wrote", os.path.normpath(path))

    # HALF WAY, cut a foot high over the landing: each stroke a groove,
    # dark, with its lower edge catching the light; and under it, in chalk,
    # NOT.
    cut = {"H": ["101", "101", "111", "101", "101"],
           "A": ["010", "101", "111", "101", "101"],
           "L": ["100", "100", "100", "100", "111"],
           "F": ["111", "100", "110", "100", "100"],
           "W": ["101", "101", "101", "111", "101"],
           "Y": ["101", "101", "010", "010", "010"],
           "N": ["101", "111", "111", "111", "101"],
           "O": ["111", "101", "101", "101", "111"],
           "T": ["111", "010", "010", "010", "010"],
           " ": ["0", "0", "0", "0", "0"], ".": ["0", "0", "0", "0", "1"]}

    def lay(frame, text, x, y, k, draw):
        for c in text:
            for gy, line in enumerate(cut[c]):
                for gx, bit in enumerate(line):
                    if bit == "1":
                        draw(frame, x + gx * k, y + gy * k, k)
            x += len(cut[c][0]) * k + k

    def groove(f, x, y, k):
        f[y:y + k, x:x + k] = (16, 15, 20, 240)
        f[y + k - 1, x:x + k] = (176, 174, 176, 220)

    def chalked(f, x, y, k):
        for sy in range(k):
            for sx in range(k):
                if rng.random() > 0.15:
                    f[y + sy, x + sx] = (236, 232, 218, rng.choice((170, 220)))
    frame = np.zeros((48, 144, 4))
    text = "HALF WAY"
    width = sum(len(cut[c][0]) * 4 + 4 for c in text) - 4
    lay(frame, text, (144 - width) // 2, 5, 4, groove)
    lay(frame, "NOT.", 92, 33, 2, chalked)
    big = np.zeros((192, 432, 4))
    for r in range(4):
        for c in range(3):
            big[r * 48:(r + 1) * 48, c * 144:(c + 1) * 144] = frame
    path = os.path.join(game, "img", "characters", HALF_WAY_SHEET + ".png")
    png.write(path, np.clip(big, 0, 255).round().astype(np.uint8))
    print("wrote", os.path.normpath(path))


# ============================================================ the marks ==
# Plan letter -> (number, what it says), map by map. Each is the cell above
# a floor cell. He writes the number, and sometimes how it went.
MARKS = [
    {"A": (1, ["D. 1. Went in. Had a look round. Grand day."]),
     "B": (2, ["D. 2. Bit further."]),
     "C": (3, ["D. 3. Bit further. Nothing happened."]),
     "D": (9, ["D. 9."]),
     "E": (14, ["D. 14. Signed the Book first. Just in case."]),
     "F": (21, ["D. 21. Somebody coming up. Charming fellow.",
                "Couldn't see him. Lovely manners."])},
    {"G": (40, ["D. 40. Nothing happened. Rather a lot of it."]),
     "I": (88, ["D. 88. Lamp went out. Lit it again. Fine."]),
     "J": (96, ["D. 96. Asked the draught to shut the door.",
                "It did not."]),
     "K": (97, ["D. 97. Bit further."])},
    {"K": (99, ["D. 99. Nearly half way, by the look of it."]),
     "L": (100, ["D. 100. HALF WAY! Tea."]),
     "M": (101, ["D. 101. Not half way."]),
     "N": (102, ["D. 102. Told the warden. He took it badly."])},
    {"O": (131, ["D. 131. The echo. Said good afternoon.",
                 "It said it back. Lovely manners."]),
     "P": (150, ["D. 150. Wet."]),
     "Q": (177, ["D. 177. Still wet. Nothing happened."]),
     "R": (190, ["D. 190. Bit further."])},
    {"A": (199, ["D. 199."]),
     "B": (203, ["D. 203. Bit further than yesterday."]),
     "C": (208, ["D. 208."]),
     "D": (211, ["D. 211. Bit further than yesterday."]),
     "E": (212, ["D. 212. Bit further than yesterday.",
                 "Back directly."])},
    {},                                 # the bottom: he never got this far
]
# D. 61 is not on a wall. It is on the flat rock where he has his tea, which
# is an event of its own on Map 74.
TEA_MARK = 61


def all_marks():
    out = [(TEA_MARK, None)]
    for marks in MARKS:
        out += sorted(marks.values())
    return sorted(out, key=lambda m: m[0])


def mark_event(event_id, i, letter):
    n, lines = MARKS[i][letter]
    x, y = at(i, letter)
    ch, d, p = chalk_slot(n)
    quoted = ["   " + l for l in lines]
    quoted[0] = "   '" + lines[0]
    quoted[-1] += "'"
    first = S.narrate(["Chalked on the rock, in a cheerful hand:", ""] +
                      quoted)
    pages = [first]
    if n == 212:
        first += S.narrate([
            "There are no marks below it. The stair goes on down",
            "past it into the dark, and nobody has written on any",
            "of that."])
        first += [S.trope(), R.self_switch("A", True)]
        pages.append(S.narrate(["   '" + lines[0], "   " + lines[1] + "'",
                                "", "Below it, nothing."]))
    img = R.image(CHALK_SHEET, ch, direction=d, pattern=p)
    kw = dict(img=img, trigger=0, priority=1, direction_fix=True,
              walk_anime=False)
    return R.event(event_id, "D. %d" % n, x, y, [
        R.page(c, conditions=({"selfSwitchValid": True, "selfSwitchCh": "A"}
                              if k else None), **kw)
        for k, c in enumerate(pages)])


# ================================================================= events ==
def _way(event_id, name, xy, to_map, to_xy, direction):
    return R.event(event_id, name, *xy, [R.page(
        [R.play_se("Move1"), R.transfer(to_map, *to_xy, direction, 0)],
        img=R.image(""), trigger=1, priority=0, through=True)])


def _ways(i):
    """Up and down. Up from the first map is out through the Door; down from
    D. 212 is one more flight, to the bottom (P4e), which has no way down."""
    evs = []
    if i == 0:
        evs.append(_way(1, "The Door", at(i, "u"), MAP_HITHERMOST, DOOR_STEP,
                        2))
    else:
        dx, dy = at(i - 1, "d")
        evs.append(_way(1, "The Stair Up", at(i, "u"), MAPS[i - 1],
                        (dx, dy - 1), 8))
    if i + 1 < len(PLANS):
        ux, uy = at(i + 1, "u")
        evs.append(_way(2, "The Stair Down", at(i, "d"), MAPS[i + 1],
                        (ux, uy + 1), 2))
    return evs


def _chest(event_id, i, ch, contents, lines):
    return S.chest(event_id, "Chest", *at(i, ch), contents, lines)


def _wall(event_id, name, i, ch, commands, img=None):
    return R.event(event_id, name, *at(i, ch), [R.page(
        commands, img=img or R.image(""), trigger=0, priority=1,
        direction_fix=True, walk_anime=False)])


def schedule(anticipated=False):
    """The board inside the Door. `anticipated` is its page once Something
    Unscheduled has been met and fought (P4e): the party's own chalk beside
    item six. Not "- D.": he never got that far."""
    c = S.narrate([
        "A board, nailed up inside the Door:",
        "",
        "   PARISH OF HITHERMOST. THE MOUNTAIN STAIR.",
        "   SCHEDULE OF HAZARDS. BY ORDER."])
    c += S.narrate([
        "   1. The dark.",
        "   2. The draught (puts lamps out).",
        "   3. The echo (do not answer it).",
        "   4. Somebody coming up."])
    c += S.narrate([
        "   5. The warden of the half-way landing.",
        "   6. Anything else: NOT ANTICIPATED."])
    if anticipated:
        c += S.narrate([
            "Chalked beside item six, in your own hand:",
            "",
            "   'Anticipated.'"])
    c += S.narrate([
        "Chalked under it, in a cheerful hand:",
        "",
        "   'All present and correct. - D.'"])
    return c


def _warden(event_id, other_id):
    """The warden of the half-way landing, at the head of the only way on;
    and, once told, the same warden out of the way, sitting down."""
    x, y = at(2, "w")
    first = S.narrate([
        "A figure in black armour stands at the head of the flight",
        "down, as still as the rock, with a hook on its belt and",
        "nothing on the hook."])
    first += S.say("The Warden", ["HALT. HALF WAY.",
                                  "NONE PASS THE HALF-WAY LANDING",
                                  "UNINSPECTED."], face=False)
    first += S.narrate(["You mention D. 101."])
    first += S.say("The Warden", ["...Not half way?"], face=False)
    first += S.narrate([
        "It looks round, down the flight behind it, into the dark,",
        "for a long time."])
    first += S.say("The Warden", ["I have been told. I have been told",
                                  "before. I did not take it well."],
                   face=False)
    first += [S.trope(), R.self_switch("A", True)]
    again = S.say("The Warden", ["HALT. HALF -", "...Oh. You again."],
                  face=False)

    def fight(opening):
        c = opening + S.say("The Warden", ["INSPECTION."], face=False)
        c += [R.battle(db.TR_WARDEN, can_escape=False, can_lose=True)]
        won = S.narrate([
            "The warden sits down on the top step, heavily. Then it",
            "gets up and moves out of the way, because it is in it."])
        won += S.narrate(["It is reconsidering a great many things."])
        won += [R.control_switch(db.SW_WARDEN, True)]
        lost = [R.call_common_event(db.CE_CONTINUANCE)]
        for code, body in [(601, won), (603, lost)]:
            c += [{"code": code, "indent": 0, "parameters": []}]
            c += R.shift(body, 1)
            c += [{"code": 0, "indent": 1, "parameters": []}]
        c += [{"code": 604, "indent": 0, "parameters": []}]
        return c

    img = R.image("Monster", 3, direction=2)
    told = {"switch1Valid": True, "switch1Id": db.SW_WARDEN}
    warden = R.event(event_id, "The Half-Way Warden", x, y, [
        R.page(fight(first), img=img, trigger=1, priority=1),
        R.page(fight(again), img=img, trigger=1, priority=1,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
        R.page([], img=R.image(""), priority=0, through=True,
               conditions=told),
    ])
    after = S.say("The Warden", ["Not half way."], face=False)
    after += S.narrate([
        "It says it to itself every so often, quietly, getting",
        "used to it."])
    sitting = R.event(other_id, "The Warden, Sitting", *at(2, "v"), [
        R.page([], img=R.image(""), priority=0, through=True),
        R.page(after, img=R.image("Monster", 3, direction=2), trigger=0,
               priority=1, conditions=told),
    ])
    return [warden, sitting]


# ============================================================= the bottom ==
UNSCHEDULED = "Something Unscheduled"
UNSCHEDULED_IMG = ("$BigMonster1", 0, 6)    # the purple one, facing you


def _it(lines):
    return S.say(UNSCHEDULED, lines, face=False)


def _arrival(event_id):
    """The first time down: the dark stops, and somebody has seen you."""
    c = S.narrate([
        "The stair ends. The dark stops all at once, like a door",
        "shutting behind you. Lamps, dozens of them, on every",
        "ledge, and every one is lit."])
    c += _it(["OH. Oh! Visitors! Come in, come in!"])
    c += [R.self_switch("A", True)]
    x, y = at(BOTTOM, "u")
    return R.event(event_id, "The Dark Stops", x, y + 1, [
        R.page(c, img=R.image(""), trigger=3, priority=0, through=True),
        R.page([], img=R.image(""), priority=0, through=True,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ])


def _see_you_up():
    """It takes the party up, every time: out under the Door at Hithermost."""
    c = S.narrate([
        "It sees you up the Stair, all of it. It takes no time at",
        "all, and afterwards none of you can say how."])
    c += [R.fadeout_screen(),
          R.transfer(MAP_HITHERMOST, *DOOR_STEP, 2, 2),
          R.wait(20), R.fadein_screen()]
    c += S.narrate([
        "You are standing under the Door into the Mountain. From",
        "somewhere a very long way down, something waves."])
    return c


SYSTEM_BATTLE_BGM = "Battle2"           # build_game's System.json battleBgm


def _battle_bgm(name, volume=85):
    """Change Battle BGM (code 132)."""
    return {"code": 132, "indent": 0, "parameters": [
        {"name": name, "pan": 0, "pitch": 100, "volume": volume}]}


def _unscheduled(event_id):
    """Item six on the schedule: anything else, not anticipated. It is on
    nothing - no prophecy, no board - so nobody has ever been obliged to fight
    it, and nobody ever has. The first win is thanked for and paid in a card
    it wrote on itself; every later visit it asks "Again?". Win or decline,
    it sees you up; lose, and it is the porch, as anywhere on the Stair."""
    x, y = at(BOTTOM, "m")

    def fight(won):
        # Change Battle BGM is saved state, so it goes back to the
        # system's on either side of the result.
        c = [_battle_bgm(BOTTOM_BATTLE_BGM),
             R.battle(db.TR_UNSCHEDULED, can_escape=False, can_lose=True)]
        won = [_battle_bgm(SYSTEM_BATTLE_BGM)] + won
        lost = [_battle_bgm(SYSTEM_BATTLE_BGM)] + _it(["Oh! Oh no. Was that too much?",
                    "I'm sorry. I don't get the practice."])
        lost += [R.call_common_event(db.CE_CONTINUANCE)]
        for code, body in [(601, won), (603, lost)]:
            c += [{"code": code, "indent": 0, "parameters": []}]
            c += R.shift(body, 1)
            c += [{"code": 0, "indent": 1, "parameters": []}]
        c += [{"code": 604, "indent": 0, "parameters": []}]
        return c

    first_win = _it(["...Thank you.",
                     "That was the best afternoon I've ever had.",
                     "Nobody made you."])
    first_win += S.narrate([
        "It rummages somewhere about itself and brings out a card,",
        "very carefully, by one corner. It has been kept ready for",
        "a very long time."])
    first_win += S.narrate([
        "   \\C[6]BOUNTY: SOMETHING UNSCHEDULED\\C[0]",
        "   Lives at the bottom of the Stair.",
        "   Would love to meet you.",
        "   Reward: on production of a witness."])
    first_win += S.narrate([
        "You point out that it said it wasn't on anything."])
    first_win += _it(["I'm not!", "Nobody would put me on anything.",
                      "So I did it myself."])
    first_win += _it(["It isn't official. It wants a stamp.",
                      "...I didn't know where you'd get one."])
    first_win += [R.play_se("Item3"), R.gain_item(db.IT_BOUNTY_CARD, 1)]
    first_win += S.got([
        "Received \\I[194]\\C[3]Bounty (Something Unscheduled)\\C[0]."])
    first_win += [R.control_switch(db.SW_UNSCHEDULED, True)]
    first_win += _see_you_up()

    again_win = _it(["...Thank you.", "Nobody made you that time either."])
    again_win += _see_you_up()

    first = _it(["I'm not on anything. I asked.",
                 "Not in the Prophecy, not on the board.",
                 "Item six."])
    first += _it(["Nobody is obliged to fight me.",
                  "So nobody ever has.",
                  "...Would you? Only if you've got the afternoon."])
    first += [S.trope(), R.self_switch("A", True)]
    not_today = _it(["Oh! No, of course. Nobody's obliged.",
                     "I'll see you up. It's a long way."]) + _see_you_up()
    first += R.choice_block(["Fight", "Not today"],
                            [fight(first_win), not_today], cancel=1)

    back = _it(["You came back!",
                "...Would you? Only if you've got the afternoon."])
    back += R.choice_block(["Fight", "Not today"],
                           [fight(first_win), not_today], cancel=1)

    again = _it(["Again?"])
    again += R.choice_block(
        ["Fight", "Not today"],
        [fight(again_win),
         _it(["Of course. Another afternoon.", "I'll see you up."]) +
         _see_you_up()], cancel=1)

    sheet, index, d = UNSCHEDULED_IMG
    kw = dict(img=R.image(sheet, index, direction=d), trigger=0, priority=1,
              step_anime=True, direction_fix=True)
    return R.event(event_id, UNSCHEDULED, x, y, [
        R.page(first, **kw),
        R.page(back, conditions={"selfSwitchValid": True,
                                 "selfSwitchCh": "A"}, **kw),
        R.page(again, conditions={"switch1Valid": True,
                                  "switch1Id": db.SW_UNSCHEDULED}, **kw),
    ])


def stair_events(i):
    evs = _ways(i)

    def nid():
        return len(evs) + 1
    for letter in sorted(MARKS[i]):
        evs.append(mark_event(nid(), i, letter))
    if i == 0:
        board = _wall(nid(), "The Schedule", i, "S", schedule())
        board["pages"].append(R.page(
            schedule(anticipated=True), trigger=0, priority=1,
            direction_fix=True, walk_anime=False,
            conditions={"switch1Valid": True,
                        "switch1Id": db.SW_UNSCHEDULED}))
        evs.append(S.pin_note(board))
        evs.append(_wall(nid(), "Another Hook", i, "H", S.narrate([
            "Another hook, with another board over it: LAMP ON HOOK.",
            "There is no lamp on this one either. Chalked beside it:",
            "",
            "   'Borrowed this one too. Back directly. - D.'"])))
        evs.append(_chest(nid(), i, "a", [R.gain_item(db.IT_HI_POTION, 3)],
                          ["Found \\I[176]\\C[3]Hi-Potion x3\\C[0]."]))
        evs.append(_chest(nid(), i, "b", [R.gain_item(db.IT_ETHER, 3)],
                          ["Found \\I[178]\\C[3]Ether x3\\C[0]."]))
        # SPA-3 (P4f): the courier, on the landing inside the Door, for
        # the ninth letter. Last on the map, so nothing above moves.
        evs.append(q_spare.stair_courier(nid(), *STAIR_COURIER))
    elif i == 1:
        tea = S.narrate([
            "A cup of tea on a saucer, set down on the floor of the",
            "ledge. Beside it, chalked on the rock:",
            "",
            "   'D. 61. TEA.'"])
        tea += S.narrate(["It is still warm. Nobody is drinking it."])
        evs.append(R.event(nid(), "D. 61", *at(i, "t"), [R.page(
            tea, img=R.image(tile_id=CUP), trigger=0, priority=1,
            direction_fix=True)]))
        evs.append(_chest(nid(), i, "a", [R.gain_item(db.IT_ELIXIR, 1)],
                          ["Found \\I[179]\\C[3]Elixir\\C[0]."]))
    elif i == 2:
        evs.append(_wall(nid(), "HALF WAY", i, "W", S.narrate([
            "Cut into the rock over the landing, in letters a foot",
            "high: HALF WAY.",
            "",
            "Under it, in chalk, much smaller: 'NOT.'"]),
            img=R.image(HALF_WAY_SHEET, 0, direction=2)))
        evs += _warden(nid(), nid() + 1)
        evs.append(_chest(nid(), i, "a", [R.gain_item(db.IT_ELIXIR, 2)],
                          ["Found \\I[179]\\C[3]Elixir x2\\C[0]."]))
    elif i == BOTTOM:
        evs.append(_arrival(nid()))
        evs.append(_unscheduled(nid()))
        wall, standing = lamps()
        for x, y in wall:
            evs.append(R.event(nid(), "Lamp (%d,%d)" % (x, y), x, y, [R.page(
                [], img=R.image("!Flame", 0, direction=2), priority=1,
                step_anime=True, direction_fix=True, walk_anime=False)]))
        for k, (x, y) in enumerate(standing):
            evs.append(R.event(nid(), "Lamp (%d,%d)" % (x, y), x, y, [R.page(
                [], img=R.image("!Flame", 1, direction=(4, 6)[k % 2]),
                priority=1, step_anime=True, direction_fix=True,
                walk_anime=False)]))
    elif i == 3:
        evs.append(_chest(nid(), i, "a",
                          [R.gain_item(db.IT_SMELLING_SALTS, 3),
                           R.gain_item(db.IT_ELIXIR, 1)],
                          ["Found \\I[181]\\C[3]Smelling Salts x3\\C[0] and",
                           "\\I[179]\\C[3]Elixir\\C[0]."]))
    return evs


# ============================================================= the porch ==
def continuance():
    """Common event 7: lost on the Stair, and back in through the chapel
    porch, restored - as at the Vigil and the Worm - with the lamp, the
    things and the gold. From a random encounter `TOQ_Mountain.js` has
    already put the party in the chapel; from the warden's lose branch this
    does it. Quillon reacts with whichever of his own pages is due, when he
    is spoken to; the one new beat is his not looking up, and only for a
    party whose name is in the Book. A party that never signed is not
    noticed coming in by the wrong door either."""
    c = R.if_then(
        R.condition_script("$gameMap.mapId() !== %d" % MAP_CONTINUANCE),
        [R.fadeout_screen(),
         R.transfer(MAP_CONTINUANCE, *PORCH, 8, 2),
         R.wait(20), R.fadein_screen()])
    c += [R.recover_all()]
    c += S.narrate(["You come back in through the porch."])
    signed = "$gameSelfSwitches.value([%d, 2, 'A'])" % MAP_CONTINUANCE
    c += R.if_then(R.condition_script(signed), S.narrate([
        "The Book is open on the lectern, where your name is.",
        "Brother Quillon looks up, and down again, and says",
        "nothing, with enormous tact."]))
    c += R.if_then(R.condition_switch(db.SW_CONTINUED, False),
                   [S.trope(), R.control_switch(db.SW_CONTINUED, True)])
    return c


# ============================================================ Hithermost ==
def lamp_offer():
    """Sir Dunstable after the ending (Map 34 event 4, page 2): the lamp.
    `hithermost.dunstable_intro()` comes first if he has not been met."""
    c = S.say("Sir Dunstable", [
        "The Forty-Eighth! Free afternoon",
        "now, I expect? Then you'll want the lamp."])
    c += S.say("Sir Dunstable", [
        "Wouldn't have dreamt of it",
        "before. Man with an appointment. Not done."])
    c += S.narrate([
        "He unhooks a lamp from his belt and hands it over,",
        "handle first."])
    c += [R.play_se("Item3"), R.gain_item(db.IT_LAMP, 1)]
    c += S.got(["Received \\I[212]\\C[3]The Lamp (Borrowed)\\C[0]."])
    c += S.say("Sir Dunstable", [
        "Back directly, there's a good",
        "fellow. I go in at a quarter past four."])
    c += S.narrate(["He does not say which quarter past four."])
    c += [R.self_switch("B", True)]
    return c


def lamp_lent():
    """Page 3: the lamp is out, and he is in no hurry for it."""
    c = S.say("Sir Dunstable", [
        "Lamp all right? Splendid.",
        "Keep it for now. I'll want it at a quarter",
        "past four."])
    c += R.if_then(R.condition_switch(db.SW_CONTINUED), S.say(
        "Sir Dunstable", ["Came in by the porch, did you?",
                          "Same as me. Nothing happened, I expect."]))
    c += S.narrate([
        "He has not looked at a clock once since you met him."])
    return c


def door_pages(first_go_in):
    """The Door into the Mountain with the lamp: a page on the item, appended
    after the published refusal, and a shorter one once the party has been
    through. The same on Hithermost's map and on the world map."""
    lamp = {"itemValid": True, "itemId": db.IT_LAMP}
    go_in = [R.play_se("Open1"), R.control_switch(db.SW_STAIR_IN, True),
             R.transfer(MAP_STAIR[0], *first_go_in, 2, 0)]
    first = S.narrate([
        "\\C[14]THE DOOR INTO THE MOUNTAIN\\C[0]. A timbered mouth",
        "in the rock, and past it a stair going down into",
        "a dark that does not stop."])
    first += S.narrate([
        "NO ADMITTANCE WITHOUT A LAMP. BY ORDER.",
        "",
        "You have a lamp."])
    first += R.choice_block(["Go in", "Not yet"],
                            [go_in, S.narrate(["Not yet."])], cancel=1)
    again = S.narrate([
        "The Door into the Mountain, and the stair going down.",
        "You have the lamp."])
    again += R.choice_block(["Go in", "Not yet"],
                            [go_in, S.narrate(["Not yet."])], cancel=1)
    been = dict(lamp, switch1Valid=True, switch1Id=db.SW_STAIR_IN)
    return [(first, lamp), (again, been)]


def door_in():
    """Where the Door puts you: inside it, facing down the stair."""
    x, y = at(0, "u")
    return (x, y + 1)


# ============================================================ the account ==
def account_lines():
    """For `postgame.amended_lines()`: what the Stair adds to the account."""
    c = R.if_then(R.condition_switch(db.SW_STAIR_IN), S.narrate([
        "Sir Dunstable lent the lamp. He has not asked for it",
        "back. The party went through the Door into the",
        "Mountain, and down."]))
    c += R.if_then(R.condition_switch(db.SW_WARDEN), S.narrate([
        "The warden of the half-way landing was told it was not",
        "half way. It is getting used to it."]))
    c += R.if_then(R.condition_switch(db.SW_CONTINUED), S.narrate([
        "They came back in through the chapel porch at least",
        "once. Brother Quillon does not remember it. The Order",
        "forbids it."]))
    c += R.if_then(R.condition_switch(db.SW_UNSCHEDULED), S.narrate([
        "Something Unscheduled was met at the bottom of the",
        "Stair, and fought, because nobody had to."]))
    c += R.if_then(R.condition_switch(db.SW_FORM_Z), S.narrate([
        "Its bounty was discharged on Form Z."]))
    return c


# ================================================================== build ==
def stair_map(i):
    g = draw(i)
    bottom = i == BOTTOM
    m = K.new_map(g.width, g.height, K.TS_DUNGEON, name=NAMES[i],
                  bgm=BOTTOM_BGM if bottom else STAIR_BGM,
                  battleback=("RockCave", "RockCave"),
                  encounters=[(t, w, []) for t, w in ENCOUNTERS[i]],
                  encounter_step=ENCOUNTER_STEP)
    m["data"] = g.data
    m["note"] = BOTTOM_NOTE if bottom else NOTE
    if BGS[i]:
        m["autoplayBgs"] = True
        m["bgs"] = {"name": BGS[i], "pan": 0, "pitch": 100, "volume": 40}
    m["events"] = [None] + stair_events(i)
    return m


def build():
    check_plans()
    for i, map_id in enumerate(MAPS):
        R.save_map(map_id, stair_map(i))


if __name__ == "__main__":
    draw_art()
