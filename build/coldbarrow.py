"""Map 48: the Chapter House of the Order of the Errant, at Coldbarrow.

`../SITES.md` step 11. The source is `../COMPANIONS.md` L6 - "one room, one
enormous map of the island with pins in it, one clerk" - and its section 4
row: **Chapter Clerk Mordaunt**, nine pins, one knight, a committee, a
review. This module builds the room and the man and **not the quest**:
ALD-3 is Aldric's, and it is appended to Mordaunt later as pages of its own.
Nothing here spends it - nobody is offered a promotion, nobody is asked to
stay put to his face, and nobody refuses anything. ALD-2's vigil may want a
chapel here too; this room is not one, and does not pretend to be.

* **The world-map door is claimed by name**, `journey.world_map`'s mechanism.
  The stamp is one cell of `Temple A (Snow)` - a small white columned temple
  with a snowy pediment, on open snow, with the northern road running south
  from its door - shot before this was written. `places.py` has
  `COLDBARROW_STEP`, the snow one square south of it, and no world
  coordinate.
* **The sight gag is a picture, not a tile.** The stock `World Map` on
  `Inside_B` is a small poster, so the wall carries four of them end to end
  as the great map, and reading it shows `img/pictures/Coldbarrow_Map.png`:
  this game's own world, off `build/worldmap/generated.png`, in sepia, with a
  white pin for every knight in the field and **nine red ones for Aldric**.
  `draw_map()` makes it - run this module to redraw it; the data build does
  not - and it reads every pin's position off `build/worldmap/worldmap.json`
  **by site name**, so no world coordinate is copied in here either.
* **Six of the nine are right on different dates, and three are the same
  week**: Frostwick, Fenmarch Hall and the Lay-By, which are the north coast,
  the south coast and the far west. The six include Thistlewick, which is
  where he actually is, and has been, for six years.
* **The cliche is the guild that has lost your file, and it is turned
  round**: the Order has not lost Sir Aldric's file. It has nine of them.
  One trope, on Mordaunt. No blush; a clerk is not a Register A delivery
  system, and this one would not approve.
"""
import json
import os

import mapkit as K
import rmmzdata as R

import db
import story as S
import q_aldric
from places import (MAP_WORLD, MAP_COLDBARROW, COLDBARROW_STEP,
                    WORLD_VILLAGE, COLDBARROW_MAP_AT_LARGE)

# The name `worldmap.json`'s door events carry for this site.
SITE = "Coldbarrow"

HERE = os.path.dirname(os.path.abspath(__file__))
PICTURE = "Coldbarrow_Map"

#            w   h  x1  y1  x2  y2  door_x
ROOM = (19, 12, 3, 4, 15, 8, 9)

FLOOR = K.IN_DIAMOND_TILE                        # `Ground L (Stone Floor X Tile)`
WALL_TOP, WALL_FACE = K.IN_WALL_TOP_STONE, K.IN_WALL_FACE_STONE   # `Wall A (Stone)`

GREAT_MAP = K.sf_block("Inside_B", "World Map")  # a 2x1 poster, four abreast
MAP_X = range(5, 13)                             # the eight cells it covers
WINDOW = K.sf_block("Inside_B", "Stained Glass Window")
WINDOWS_X = (3, 15)
BOOKSHELF = K.sf_block("Inside_B", "Bookshelf A")
ARMOUR = K.sf_tile("Inside_C", "Armor A (Stand)")
TABLE_A = K.sf_block("Inside_B", "Table A")
CHAIR = K.sf_block("Inside_B", "Chair A (Wood)")   # back over seat, 1x2
NOTES = K.sf_tile("Inside_C", "Notes B (V)")
PEN = K.sf_tile("Inside_C", "Pen A")
BOOKS = K.sf_tile("Inside_C", "Closed Books C")
OPEN_BOOK = K.sf_tile("Inside_C", "Open Book A (V)")

MORDAUNT = (13, 4)          # at the east end of the map, with the pins
DESK = (13, 6)              # `Table A`, two cells: the spare pins and the ledger
COMMITTEE = (5, 7)          # `Table A`, two chairs and two stools, all empty
FILES_X = (14, 15)          # the bookshelves along the east wall

# The pins, by the names `worldmap.json`'s site doors carry, plus Thistlewick.
# Aldric's nine; the last three are the same week.
ALDRIC_PINS = ["Thistlewick", "Hithermost", "Great Dunnage", "Restwell",
               "Weeping Bottom", "Sky Anvil",
               "Frostwick", "Fenmarch Hall", "The Lay-By"]
# Every other knight in the field: one each, which is the system. Sir
# Dunstable's is the Chapel of Continuance, and it is right.
OTHER_PINS = ["Chapel of Continuance", "Penultima", "Olde Evermore",
              "Gladhollow", "Ashcombe", "Collegium Arcanum", "Little Gore",
              "Fairholme", "Weeping Bottom"]


def chapter_map():
    w, h, x1, y1, x2, y2, door_x = ROOM
    g = K.interior(w, h, x1, y1, x2, y2, door_x=door_x, floor=FLOOR,
                   wall_top=WALL_TOP, wall_face=WALL_FACE)

    # A red runner from the door to the map. Layer 1 is floor art.
    g.fill(door_x, y1 + 1, door_x, y2 + 1, 1, K.IN_RED_CARPET)
    g.autotile(1)

    # The north wall: the great map, and a window either side of it.
    for x in MAP_X[::2]:
        g.blit(x, y1 - 1, 3, (GREAT_MAP,))
    for x in WINDOWS_X:
        g.column(x, y1 - 2, 3, WINDOW)

    # The files, along the east wall: shelf on shelf of them.
    for x in FILES_X:
        g.column(x, y2 - 1, 3, BOOKSHELF)

    # Mordaunt's desk: the spare pins on a sheet, and the ledger.
    g.blit(*DESK, 2, (TABLE_A,))
    g.set(DESK[0], DESK[1], 3, NOTES)
    g.set(DESK[0] + 1, DESK[1], 3, OPEN_BOOK)

    # The committee's table: two chairs and two stools, all empty. The
    # stock chair is a tall back over a seat and only faces south, so the
    # south side gets stools, which is how Fairholme's council is seated too.
    cx, cy = COMMITTEE
    g.blit(cx, cy, 2, (TABLE_A,))
    g.set(cx, cy, 3, BOOKS)
    g.set(cx + 1, cy, 3, PEN)
    for x in (cx, cx + 1):
        g.column(x, cy - 2, 3, CHAIR)
        g.set(x, cy + 1, 3, K.IN_STOOL)

    # Armour down the west wall: knights in the field, standing still.
    for y in (y1, y2):
        g.set(x1, y, 3, ARMOUR)

    m = K.new_map(w, h, K.TS_INSIDE, name="The Chapter House",
                  bgm="Castle2", battleback=("Castle1", "Castle1"))
    m["data"] = g.data
    m["events"] = [None] + q_aldric.with_follower(chapter_events(), MAP_COLDBARROW)  # ALD-5
    return m


def _picture(indent=0):
    """Show Picture 1: the great map, centred over the upper screen."""
    return [{"code": 231, "indent": indent,
             "parameters": [1, PICTURE, 1, 0, 408, 222, 84, 84, 255, 0]}]


def _erase(indent=0):
    return [{"code": 235, "indent": indent, "parameters": [1]}]


def mordaunt_pages():
    first = S.narrate([
        "A thin grey man in the Order's black coat is",
        "standing at the great map with a fistful of pins,",
        "reading it the way other people read a will."])
    first += S.say("Mordaunt", [
        "Chapter House of the Order of",
        "the Errant. Mordaunt, clerk.",
        "Are you a knight?"])
    first += S.narrate(["You say that you grow turnips."])
    first += S.say("Mordaunt", [
        "Then you are not on the map.",
        "Good. One knight, one pin.",
        "That is the system."])
    first += S.narrate([
        "You look at the map. There are a great many",
        "white pins in it, one to a knight, and nine red."])
    first += S.say("Mordaunt", [
        "Sir Aldric Pemberton-Gore.",
        "The Third. Nine pins."])
    first += S.say("Mordaunt", [
        "Six of them are correct,",
        "on different dates. Three of",
        "them are the same week."])
    first += S.narrate([
        "You ask how a man can be in three places in",
        "one week."])
    first += S.say("Mordaunt", [
        "That is a question for the",
        "committee. The committee has",
        "been formed. It is reviewing",
        "the map, the pins and the week."])
    first += S.say("Mordaunt", [
        "People say the Order has lost",
        "his file. The Order has not",
        "lost his file."])
    first += S.say("Mordaunt", ["The Order has nine of them."])
    first += S.narrate([
        "He takes a tenth pin from his fist. He holds",
        "it over the island for a long moment, and then",
        "he puts it back."])
    first += [S.trope()]

    # Aldric in the party is a reaction shot and not the quest: ALD-3's
    # review, its request and its promotion are appended later.
    aldric = S.narrate([
        "Mordaunt looks up from the map, at the knight",
        "behind you, and back at the map."])
    aldric += S.say("Aldric", [
        "Mordaunt! Splendid fellow.",
        "Where am I?"])
    aldric += S.say("Mordaunt", [
        "Frostwick, sir. And Fenmarch.",
        "And a lay-by in the west."])
    aldric += S.say("Aldric", ["Busy week."])
    aldric += S.say("Mordaunt", ["The committee will write."])
    first += R.if_then(R.condition_actor_in_party(db.ALDRIC), aldric)
    first += [R.self_switch("A", True)]

    later = S.say("Mordaunt", [
        "If you should see Sir Aldric,",
        "note the place, the date and",
        "the time. In ink. Not pencil.",
        "Pencil is how we got here."])

    img = R.image("Gen_People3", 7, direction=2)
    return [
        R.page(first, img=img, trigger=0, priority=1),
        R.page(later, img=img, trigger=0, priority=1,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ]


def chapter_events():
    x1, y1, y2, door_x = ROOM[2], ROOM[3], ROOM[5], ROOM[6]
    evs = [S.exit_tile(1, "Chapter House Door", door_x, y2 + 2,
                       MAP_WORLD, *COLDBARROW_STEP)]
    evs.append(R.event(2, "Mordaunt", *MORDAUNT, mordaunt_pages()))
    evs[-1]["pages"] += q_aldric.mordaunt_pages(evs[-1]["pages"][-1])  # ALD-3

    page = dict(img=R.image(""), trigger=0, priority=1, direction_fix=True)

    # 3-10: the great map, one event on each cell of the wall it covers,
    # read from the floor below it. The picture is the sight gag.
    look = S.narrate([
        "The island, in the Order's own survey, four sheets",
        "wide, with a pin for every knight in the field."])
    look = _picture() + [R.wait(20)] + look
    look += S.narrate([
        "One pin, one knight: a white head for each of",
        "them, spread thin, standing where they were put."])
    look += S.narrate([
        "And nine red ones, all over it, for one knight,",
        "three of which have a label in the same hand:",
        "   SAME WEEK. SEE COMMITTEE."])
    look += _erase()
    for i, x in enumerate(MAP_X):
        evs.append(R.event(3 + i, "The Great Map", x, y1 - 1,
                           [R.page(look, **page)]))
        evs[-1]["pages"] += q_aldric.great_map_pages(evs[-1]["pages"][0])  # ALD-3
    n = 3 + len(MAP_X)

    # The committee's table. It is not sitting.
    table = S.narrate([
        "Two chairs and two stools, all empty, and a card",
        "on the table:",
        "   REVIEW OF PINS (PEMBERTON-GORE)",
        "   The committee sits on Thursdays."])
    table += S.narrate([
        "Beneath it, in a smaller hand:",
        "   Sir A. requested to REMAIN IN ONE PLACE",
        "   for the duration. Not yet informed."])
    cx, cy = COMMITTEE
    for i in range(2):
        evs.append(R.event(n + i, "The Committee's Table", cx + i, cy,
                           [R.page(table, **page)]))
        evs[-1]["pages"] += q_aldric.committee_pages(evs[-1]["pages"][0])  # ALD-3

    # The files: every other knight is a thin one. His are the shelf.
    files = S.narrate([
        "The files of the Order, bound, a knight to a",
        "volume, each one thin and neat and in its place."])
    files += S.narrate([
        "Except the bottom shelf, which is nine fat",
        "volumes, each labelled PEMBERTON-GORE, and each",
        "one certain that it is the real one."])
    for i, x in enumerate(FILES_X):
        evs.append(R.event(n + 2 + i, "The Files", x, y2,
                           [R.page(files, **page)]))

    # The desk: the spare pins, and the ledger.
    desk = S.narrate([
        "A sheet of paper with pins laid out on it, sorted",
        "by colour: a great many white, and a small heap",
        "of red, kept apart."])
    desk += S.narrate([
        "The ledger beside it is open at P. Every entry",
        "on the page has been crossed out and written",
        "in again somewhere else."])
    evs.append(R.event(n + 4, "Mordaunt's Desk", *DESK,
                       [R.page(desk, **page)]))
    return evs


# ============================================================= the picture ==
def draw_map(aldric=True):
    """Writes `img/pictures/Coldbarrow_Map.png` - the great map, with pins.

    With `aldric` False it writes `COLDBARROW_MAP_AT_LARGE` instead: the
    same map after ALD-3, when the nine red pins have come out and the one
    that is left goes about on his tabard. The white pins that stood aside
    for a red one keep their places, so the two pictures differ only there.

    Not part of the data build, like `art.py`: run this module to redraw it.
    The world is `build/worldmap/generated.png` at four pixels a cell, toned
    to sepia, in a dark wooden frame. Every pin is placed by the name of the
    site it is at, read off `worldmap.json`'s door events."""
    import sys
    sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "chargen"))
    import numpy as np
    import png

    world = png.read(os.path.join(HERE, "worldmap", "generated.png"))
    rgb = world[..., :3].astype(float)
    grey = rgb @ [0.3, 0.59, 0.11]
    sepia = np.stack([grey * 1.07 + 30, grey * 0.9 + 22, grey * 0.66 + 8], -1)
    rgb = np.clip(rgb * 0.45 + sepia * 0.55, 0, 255)

    cell = world.shape[0] // 120
    border = 14
    size = world.shape[0] + 2 * border
    out = np.zeros((size, size, 4), dtype=float)
    out[..., :3] = (74, 46, 26)
    out[3:-3, 3:-3, :3] = (110, 72, 40)
    out[..., 3] = 255
    out[border:-border, border:-border, :3] = rgb

    sites = {"Thistlewick": WORLD_VILLAGE}
    doors = json.load(open(os.path.join(HERE, "worldmap", "worldmap.json")))
    for e in doors["events"]:
        if e and "-site" in (e.get("note") or ""):
            sites.setdefault(e["name"], (e["x"], e["y"]))

    def pin(name, colour, dx=0):
        x, y = sites[name]
        px = border + x * cell + cell // 2 + dx
        py = border + y * cell + cell // 2
        # a shaft, then a round head above it with a dark rim
        out[py - 6:py + 1, px:px + 2, :3] = (40, 36, 34)
        for yy in range(-5, 6):
            for xx in range(-5, 6):
                d = xx * xx + yy * yy
                if d <= 25:
                    out[py - 9 + yy, px + 1 + xx, :3] = (
                        (30, 20, 20) if d > 13 else colour)
        out[py - 11, px - 1:px + 1, :3] = (255, 255, 255)

    for name in OTHER_PINS:
        pin(name, (236, 232, 220), dx=-6 if name in ALDRIC_PINS else 0)
    if aldric:
        for name in ALDRIC_PINS:
            pin(name, (214, 32, 28))

    name = PICTURE if aldric else COLDBARROW_MAP_AT_LARGE
    path = os.path.join(HERE, "..", "img", "pictures", name + ".png")
    png.write(path, np.clip(out, 0, 255).astype(np.uint8))
    print("wrote", os.path.normpath(path))


# ================================================================ the doors ==
def world_doors(base_id, cells):
    """The real door into the Chapter House, on the world map.

    `cells` is the one square `worldmap.json` put a placeholder on for this
    site, handed in by `journey.world_map`. Player-touch and below characters,
    the world map's idiom for a place you walk into."""
    w, h, x1, y1, x2, y2, door_x = ROOM
    evs = []
    for i, (x, y) in enumerate(sorted(cells)):
        arrive = S.narrate([
            "A small white temple in the snow, with a brass",
            "plate by the door:",
            "   THE ORDER OF THE ERRANT - CHAPTER HOUSE",
            "   Knights in the field, please report."])
        arrive += R.choice_block(
            ["Go in", "Press on"],
            [[R.transfer(MAP_COLDBARROW, door_x, y2, 8, 0)],
             S.narrate(["You press on. Somewhere inside, a pin",
                        "is moved."])])
        evs.append(R.event(base_id + i, SITE, x, y, [R.page(
            arrive, img=R.image(""), trigger=1, priority=0, through=True)]))
    return evs


def build():
    R.save_map(MAP_COLDBARROW, chapter_map())


if __name__ == "__main__":
    draw_map()
    draw_map(aldric=False)                                          # ALD-3
