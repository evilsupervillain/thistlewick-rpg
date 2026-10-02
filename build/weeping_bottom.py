"""Maps 54-55: Weeping Bottom, and the Sisterhouse ward.

`../SITES.md` step 15. The source is `../COMPANIONS.md` L4 - the Order of
Whatever Works' mother house, "in a damp valley chosen on medical grounds that
were wrong. Half hospital, half argument." - and its two NPCs, **Prioress
Aveline Stope**, who has begun holding symposia and knows that is a bad sign,
and **Sister Bewick** of the Order of What Ought To Work, who is losing
patients, winning arguments, and entirely sincere. This module builds the
place and the people and **not the quests** - MER-1, MER-3 and ALD-2 are
appended later as pages of their own, and nothing here spends any of them.

* **The world-map door is claimed by name**, `journey.world_map`'s mechanism.
  The stamp is one cell of `Temple B`, a small white pillared temple on a
  shelf of sandy cobbles with grey rock close to the west and **the sea right
  up against it to the east**. So the valley is the hollow between the rock
  and the sea, and **the medical grounds were the sea air**: the founder chose
  it in 1702 because every physician she asked recommended it, none of whom
  had been, and the fog comes in off the water and settles in the bottom and
  does not leave. It drizzles on Map 54 and nowhere else - `frostwick.py`'s
  weather idiom, with a local `door()` that clears it. `places.py` has
  `WEEPING_BOTTOM_STEP`, the square south of the stamp, and no world
  coordinate.
* **The schism is a line down the middle of the ward.** Whatever Works has
  the west half, in wood, with soup; What Ought To Work has the east half,
  re-floored in tile, with a doctrine, the correct treatment in eleven stages
  and a great many empty beds. Sister Bewick **loses patients to the other
  half of the ward** - they walk across in the night, because there is soup -
  which is COMPANIONS' line taken literally and nobody dies. The symposium is
  in the chapel, which is locked and set out for it; ALD-2's vigil is at night
  and can have the chapel later.
* **MER-1 is not spent.** No queue, no forty patients, no contest, no
  Pamphlet. With Merribell in the party the Prioress says "We'll talk. Not
  today." and Merribell fills Sister Bewick's empty water jug without a word -
  two reaction shots, and the quest still has everything it needs.
* **Coldbarrow's white pin here is Sir Hamo Tench**, of the Order of the
  Errant, "in the field" at Weeping Bottom for fourteen years with a cough he
  came for the sea air to cure. His bed is exactly on the line, so both orders
  treat him. With Sir Aldric in the party he tells him the Chapter House has a
  red pin in him here too - "Then for once I'm where it says." - which is a
  reaction shot, and spends nothing of ALD-2 or ALD-3.
* **One trope** - the founder's stone, the healing sanctuary in its place of
  power - **and no blush**: the place is damp, not red.
"""
import mapkit as K
import rmmzdata as R

import db
import story as S
import q_aldric
import q_merribell
from places import MAP_WORLD, MAP_WEEPING_BOTTOM, MAP_WARD, WEEPING_BOTTOM_STEP

# The name `worldmap.json`'s door event carries for this site.
SITE = "Weeping Bottom"


# ================================================================ the weather ==
DRIZZLE_POWER = 3


def drizzle(indent=0):
    return R.set_weather("rain", power=DRIZZLE_POWER, duration=1,
                         indent=indent)


def dry(indent=0):
    return R.set_weather("none", duration=1, indent=indent)


def weather_event(event_id):
    """Autorun, once per arrival, then erase itself - `north.py`'s idiom. An
    erased event comes back on the next load, so it drizzles every visit."""
    return R.event(event_id, "The Weather", 0, 0, [R.page(
        [drizzle(), R.erase_event()],
        img=R.image(), trigger=3, priority=0, through=True)])


def door(event_id, name, x, y, target_map, tx, ty):
    """A door indoors. The drizzle is cleared after the walk and before the
    fade, which is `frostwick.door`."""
    cmds = S.door_page(target_map, tx, ty, 8)
    cmds.insert(len(cmds) - 1, dry())
    return R.event(event_id, name, x, y, [R.page(
        cmds, img=R.image("!Door1", 0, direction=2), trigger=1, priority=1)])


def exit_tile(event_id, name, x, y):
    """The track back up to the world map, where it is not raining."""
    return R.event(event_id, name, x, y, [R.page(
        [R.play_se("Move1"), dry(),
         R.transfer(MAP_WORLD, *WEEPING_BOTTOM_STEP, 2, 0)],
        img=R.image(""), trigger=1, priority=0, through=True)])


def _pair(first, later):
    """A first conversation and the short one after it, on self switch A."""
    return first + [R.self_switch("A", True)], later


def _person(event_id, name, xy, img, first, later):
    return R.event(event_id, name, *xy, [
        R.page(first, img=img, trigger=0, priority=1),
        R.page(later, img=img, trigger=0, priority=1,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ])


PAGE = dict(img=R.image(""), trigger=0, priority=1, direction_fix=True)


# ========================================================== the valley bottom ==
# The hollow between the rock and the sea. Rock round three sides, with a gap
# at the south for the track down; sand and the sea along the east. The
# Sisterhouse stands against the rock at the top, the chapel to the west of
# the track, and the patients are out on the sand for the air.
VW, VH = 36, 26
MASS = K.A(117)                 # Ledge B (Dirt): the rock
FACE = K.A(125)                 # and its face, which `dungeon_walls` finds
GROUND = K.A(25)                # Grass (Dirt): the same family as the rock
ROAD = K.A(26)                  # Road (Dirt)
SEA = K.A(10)                   # A1 `Water D (Sand)`
SAND = K.SOIL                   # `K.SOIL` is the sheet's `Sand`: step 13

TRACK_X = 15                    # the track down: columns 15 and 16
SAND_X, SEA_X = 27, 31

#            x   y   w   h
HOUSE = (10, 4, 13, 8)
CHAPEL = (4, 13, 6, 5)
HOUSE_DOOR = (16, HOUSE[1] + HOUSE[3] - 1)
CHAPEL_DOOR = (6, CHAPEL[1] + CHAPEL[3] - 1)
ARRIVE = (TRACK_X, VH - 2)

STONE = (20, 15)                # the founder's stone, on its base
SIGN = (18, 20)                 # the board by the track
PIM = (26, 13)
SHORE = [(28, 11), (28, 14), (28, 17)]
GARDEN = (4, 20, 10, 21)        # x1, y1, x2, y2: the physic garden
QUEUE = [(TRACK_X + 1, y) for y in range(14, 20)]     # MER-1's last six

STONE_TILE = K.sf_block("Outside_C", "Monument A")      # 1x2, on its base
WALL_MOSS = K.sf_tile("Outside_B", "Wall Moss")
WALL_FERN = K.sf_tile("Outside_B", "Wall Fern")
FERN = K.sf_tile("Outside_B", "Fern")
MUSHROOMS = K.sf_tile("Outside_B", "Mushrooms A")
BOULDER = K.sf_tile("Outside_B", "Boulder A")
PEBBLES = K.sf_tile("Outside_B", "Rocks")


def valley_map():
    w, h = VW, VH
    g = K.Canvas(w, h)
    g.fill(0, 0, w - 1, h - 1, 0, GROUND)

    # The sand and the sea, the whole length of the east side.
    g.fill(SAND_X, 0, w - 1, h - 1, 0, SAND)
    g.fill(SEA_X, 0, w - 1, h - 1, 0, SEA)

    # The rock: the top, the west, and the south either side of the track.
    g.fill(0, 0, SAND_X - 1, 3, 0, MASS)
    g.fill(0, 4, 2, h - 1, 0, MASS)
    g.fill(3, h - 3, TRACK_X - 2, h - 1, 0, MASS)
    g.fill(TRACK_X + 3, h - 3, SAND_X - 1, h - 1, 0, MASS)
    g.dungeon_walls(MASS, FACE)

    # The bottom is wet: standing water in the low places. A2 `Moss` would
    # have been the obvious ground and draws as a sunken black-rimmed pit, and
    # A1 `Swamp Grass A` is lily pads on black; a rectangle of `WATER`
    # autotiles into a proper pond.
    for x1, y1, x2, y2 in [(4, 7, 6, 9), (22, 18, 24, 20), (11, 21, 12, 22)]:
        g.fill(x1, y1, x2, y2, 0, K.WATER)

    # The track down, and the path to each door.
    g.fill(TRACK_X, 14, TRACK_X + 1, h - 1, 0, ROAD)
    g.fill(HOUSE_DOOR[0], HOUSE_DOOR[1] + 1, HOUSE_DOOR[0], 14, 0, ROAD)
    g.fill(CHAPEL_DOOR[0], CHAPEL_DOOR[1] + 1, TRACK_X - 1,
           CHAPEL_DOOR[1] + 1, 0, ROAD)
    g.fill(TRACK_X + 2, 14, SAND_X - 1, 14, 0, ROAD)

    g.building(*HOUSE, wall=K.WALL_STONE_WHITE, roof=K.ROOF_GREEN)
    g.building(*CHAPEL, wall=K.WALL_STONE_WHITE, roof=K.ROOF_GREEN)
    g.autotile(0)

    # Fronts. The Sisterhouse door is an event; the chapel's is locked.
    fy = HOUSE_DOOR[1]
    for x in (11, 13, 19, 21):
        g.set(x, fy, 3, K.WINDOW)
    g.column(CHAPEL_DOOR[0], CHAPEL_DOOR[1] - 1, 3, K.DOOR_DOUBLE)
    g.column(CHAPEL_DOOR[0] + 2, CHAPEL_DOOR[1] - 1, 3, K.WINDOW_GLASS)

    # The rock weeps: moss and fern down every face of it.
    for x in range(3, SAND_X, 3):
        if not HOUSE[0] - 1 <= x <= HOUSE[0] + HOUSE[2]:
            g.set(x, 3, 3, WALL_MOSS if x % 2 else WALL_FERN)
    for x in (HOUSE[0] - 1, HOUSE[0] + HOUSE[2] + 1):
        g.set(x, 2, 3, WALL_MOSS)

    # The founder's stone, the board by the track, the physic garden.
    g.column(STONE[0], STONE[1] - 1, 3, STONE_TILE)
    g.set(*SIGN, 3, K.FENCE_PANEL)                      # `Sign B`, a board
    gx1, gy1, gx2, gy2 = GARDEN
    for x in range(gx1, gx2 + 1):
        for y in (gy1, gy2):
            g.set(x, y, 3, FERN)
    g.scatter([(8, 7), (26, 22), (10, 22), (3, 12), (21, 12)], 3, MUSHROOMS)

    # Boulders across the top of the rock, which is otherwise bare dirt and
    # reads as dunes.
    rock = [(x, y) for y in (0, 1) for x in range(1, SAND_X - 1, 4)]
    rock += [(x, y) for x in (0, 1) for y in range(5, h - 3, 4)]
    rock += [(x, h - 2) for x in list(range(4, TRACK_X - 2, 3))
             + list(range(TRACK_X + 4, SAND_X - 1, 3))]
    g.scatter([(x + (y % 2), y) for x, y in rock], 3, BOULDER)

    # The shore: boulders and pebbles on the sand.
    g.scatter([(29, 3), (30, 8), (29, 21), (30, 23)], 3, BOULDER)
    g.scatter([(27, 6), (29, 15), (27, 20), (28, 24)], 3, PEBBLES)

    m = K.new_map(w, h, K.TS_OUTSIDE, name="Weeping Bottom", bgm="Town2",
                  bgm_volume=60)
    m["data"] = g.data
    m["events"] = [None] + q_aldric.with_follower(valley_events(), MAP_WEEPING_BOTTOM)  # ALD-5
    return m


def stone_pages():
    first = S.narrate([
        "A stone, beaded all over with the damp. The letters are cut",
        "deep, which is as well:"])
    first += S.narrate([
        "THE SISTERHOUSE OF THE ORDER OF WHATEVER WORKS.",
        "FOUNDED 1702 BY MOTHER URSULA PYM, IN THIS VALLEY,",
        "FOR THE AIR."])
    first += S.narrate([
        "And under that, smaller: The sea air being the finest cure",
        "for the chest, in the opinion of every physician consulted.",
        "",
        "And under that, in a newer hand: None of whom had been."])
    first += [S.trope()]
    later = S.narrate([
        "FOR THE AIR. The air comes in off the sea, settles in the",
        "bottom of the valley, and stays. It is very loyal."])
    return _pair(first, later)


def chapel_pages():
    look = S.narrate([
        "The chapel. A notice is pinned to its door, and has been",
        "rained on:"])
    look += S.narrate([
        "SYMPOSIUM THE ELEVENTH",
        "'Whether Anything Works'",
        "Three o'clock. The Prioress in the chair."])
    look += S.narrate([
        "The door is locked. Through the keyhole: two rows of",
        "chairs set out facing one another, like a wedding where",
        "the families have not been introduced."])
    return look


def sign_pages():
    board = S.narrate([
        "WEEPING BOTTOM",
        "THE SISTERHOUSE OF THE ORDER OF WHATEVER WORKS",
        "Visitors welcome. Mind the step; it is wet."])
    board += S.narrate([
        "Painted in underneath, in black, more recently and very",
        "neatly: AND OF THE ORDER OF WHAT OUGHT TO WORK. (EAST DOOR.)",
        "",
        "There is one door."])
    return board


def pim_pages():
    first = S.narrate([
        "A Sister of Whatever Works in a white cap and apron, with",
        "three patients lined up along the shore."])
    first += S.say("Sister Pim", [
        "Deep breaths, everybody! In",
        "through the nose. It's prescribed."])
    first += S.narrate([
        "The patients breathe in the sea air, obediently. The fog",
        "breathes back."])
    first += S.say("Sister Pim", [
        "Twice a day. Founder's orders.",
        "Nobody's ever countermanded them. It",
        "seemed rude, with her on the stone."])
    later = S.say("Sister Pim", [
        "And OUT. Lovely. And in",
        "again. Nobody cough."])
    later += S.narrate(["Somebody coughs."])
    return _pair(first, later)


def valley_events():
    evs = [weather_event(1)]
    # 2-3: the track back up, both cells of it, below characters.
    for i in range(2):
        evs.append(exit_tile(i + 2, "The Track Up", TRACK_X + i, VH - 1))

    # 4: the Sisterhouse door; the drizzle stops at it.
    evs.append(door(4, "The Sisterhouse", *HOUSE_DOOR, MAP_WARD,
                    WARD_DOOR_X, WARD[3] + 1))

    # 5: the chapel, locked, and set out for the symposium.
    evs.append(R.event(5, "The Chapel", *CHAPEL_DOOR,
                       [R.page(chapel_pages(), **PAGE)]))

    # 6: the founder's stone, and the site's trope.
    first, later = stone_pages()
    evs.append(R.event(6, "The Founder's Stone", *STONE, [
        R.page(first, **PAGE),
        R.page(later, conditions={"selfSwitchValid": True,
                                  "selfSwitchCh": "A"}, **PAGE)]))

    # 7: the board by the track.
    evs.append(R.event(7, "The Board", *SIGN, [R.page(sign_pages(), **PAGE)]))

    # 8: Sister Pim, taking the patients out for the air.
    evs.append(_person(8, "Sister Pim", PIM,
                       R.image(*S.FACES["Sister Pim"], direction=6), *pim_pages()))

    # 9-11: the patients, facing the sea.
    crouch = S.say("Mr Crouch", [
        "Lovely and bracing, the sea",
        "air. Lovely and bracing."])
    crouch += S.narrate(["He coughs, bracingly."])
    evs.append(S.npc(9, "Mr Crouch", *SHORE[0], crouch, *S.FACES["Mr Crouch"],
                     direction=6))
    liddy = S.say("Mrs Liddy", [
        "I came for the damp on my",
        "chest. It's doing wonderfully. I've",
        "never had so much of it."])
    evs.append(S.npc(10, "Mrs Liddy", *SHORE[1], liddy, *S.FACES["Mrs Liddy"],
                     direction=6))
    oakes = S.say("Mr Oakes", [
        "I'm only visiting. My brother",
        "came in with a cough."])
    oakes += S.say("Mr Oakes", [
        "That was in the spring. He's",
        "gone home now. I've got it instead."])
    evs.append(S.npc(11, "Mr Oakes", *SHORE[2], oakes, *S.FACES["Mr Oakes"],
                     direction=6))

    # 12: the physic garden.
    garden = S.narrate([
        "THE PHYSIC GARDEN, says a slate. The Order planted",
        "feverfew here, and sage, and rosemary, and comfrey."])
    garden += S.narrate([
        "The valley grew ferns. Every plant in the garden is a",
        "fern, and they are doing splendidly."])
    evs.append(R.event(12, "The Physic Garden", GARDEN[0], GARDEN[1],
                       [R.page(garden, **PAGE)]))

    # 13-18: the last six of MER-1's queue of forty, up the track.
    evs += q_merribell.queue_events(13, QUEUE, q_merribell.MER1_QUEUE)  # MER-1
    return evs


# ================================================================== the ward ==
# One long room, split down the middle by a strip of red carpet nailed to the
# floor. West of it, in wood, is Whatever Works; east of it, re-floored in
# tile, is What Ought To Work. The Prioress stands at the line.
IW, IH = 27, 15
#       x1  y1  x2  y2
WARD = (2, 4, 24, 11)
WARD_DOOR_X = 7
LINE_X = 13

BED = K.sf_block("Inside_B", "Bed")                     # 1x2, head at the top
TABLE_D = K.sf_tile("Inside_B", "Table D")
MEDICINE = K.sf_block("Inside_B", "Medicine Shelf")     # 1x2, on its base
BOOKSHELF = K.sf_block("Inside_B", "Bookshelf A")       # 1x2, on its base
NOTICE = K.sf_tile("Inside_B", "Posted Notice")
STOOL = K.sf_tile("Inside_B", "Stool A")
STEW = K.sf_tile("Inside_C", "Stew")
BOWL = K.sf_tile("Inside_C", "Soup Bowl")
JUG = K.sf_tile("Inside_C", "Pot A")                    # a white jug
OPEN_BOOK = K.sf_tile("Inside_C", "Open Book A (V)")
BOOKS = K.sf_tile("Inside_C", "Closed Books C")
HOURGLASS = K.sf_tile("Inside_C", "Hourglass")

WEST_BEDS = [(4, 4), (6, 4), (8, 4), (10, 4), (3, 9), (5, 9), (9, 9), (11, 9)]
EAST_BEDS = [(16, 4), (18, 4), (20, 4), (15, 9), (17, 9), (19, 9), (21, 9),
             (23, 9)]
HAMO_BED = (LINE_X, 9)
MEDICINE_X = 2
SHELVES_X = (22, 23, 24)
MINUTES = (LINE_X, 4)                   # the table on the line, and the book
STOPE = (LINE_X - 1, 5)
SOUP = (5, 7)                           # `Table D`, the pot on it
LAMB = (6, 7)
NUTTALL = (9, 6)
DESK = (19, 7)                          # `Table D`, two cells
BEWICK = (18, 7)
DACE = (16, 6)
HAMO = (LINE_X, 11)
TREATMENT = (15, 3)                     # the notice on the east wall face
EMPTY_BED = (18, 5)                     # the lower cell of an east bed


def ward_map():
    x1, y1, x2, y2 = WARD
    g = K.interior(IW, IH, x1, y1, x2, y2, door_x=WARD_DOOR_X,
                   floor=K.IN_WOOD_FLOOR, wall_top=K.IN_WALL_TOP_WHITE,
                   wall_face=K.IN_WALL_FACE_WHITE)
    # What Ought To Work has re-floored its half, in tile.
    g.fill(LINE_X + 1, y1, x2, y2, 0, K.IN_DIAMOND_TILE)
    # The line: a strip of red carpet, nailed down. Layer 1 is floor art.
    g.fill(LINE_X, y1, LINE_X, y2, 1, K.IN_RED_CARPET)
    g.autotile(1)

    for x, y in WEST_BEDS + EAST_BEDS + [HAMO_BED]:
        g.column(x, y, 2, BED)

    # West: the Order's whole pharmacy, the windows, the soup.
    g.column(MEDICINE_X, y1 - 1, 2, MEDICINE)
    for x in (5, 9):
        g.column(x, y1 - 2, 3, K.IN_WINDOW)
    g.set(*SOUP, 2, TABLE_D)
    g.set(*SOUP, 3, STEW)
    g.set(SOUP[0] - 1, SOUP[1], 2, TABLE_D)
    g.set(SOUP[0] - 1, SOUP[1], 3, BOWL)
    for x, _ in WEST_BEDS[:4]:
        g.set(x, 6, 2, STOOL)

    # The line: the minutes on a table, and the notice above it.
    g.set(*MINUTES, 2, TABLE_D)
    g.set(*MINUTES, 3, OPEN_BOOK)
    g.set(LINE_X, y1 - 1, 3, NOTICE)

    # East: the doctrine, in writing.
    for x in SHELVES_X:
        g.column(x, y1 - 1, 2, BOOKSHELF)
    g.set(*TREATMENT, 3, NOTICE)
    g.set(20, y1 - 1, 3, NOTICE)
    g.set(DESK[0], DESK[1], 2, TABLE_D)
    g.set(DESK[0] + 1, DESK[1], 2, TABLE_D)
    g.set(DESK[0], DESK[1], 3, JUG)
    g.set(DESK[0] + 1, DESK[1], 3, BOOKS)
    g.set(DESK[0] + 2, DESK[1], 2, TABLE_D)
    g.set(DESK[0] + 2, DESK[1], 3, HOURGLASS)
    for x, y in [(x1, y2), (x2, y2)]:
        g.set(x, y, 3, K.INC_PLANT2)

    m = K.new_map(IW, IH, K.TS_INSIDE, name="The Sisterhouse", bgm="Town2",
                  bgm_volume=50, battleback=("Wood1", "Room1"))
    m["data"] = g.data
    m["events"] = [None] + ward_events()
    return m


def stope_pages():
    first = S.narrate([
        "A woman in the Order's white and blue stands at the line",
        "down the middle of the ward, looking at both halves of it."])
    first += S.say("Prioress", [
        "Aveline Stope. Prioress.",
        "Welcome to Weeping Bottom. Mind the",
        "floor; it's damp. Everything is damp."])
    first += S.narrate(["You ask about the line."])
    first += S.say("Prioress", [
        "Sister Bewick's order has the",
        "east half. Mine has the west. We had",
        "the whole of it once. It was simpler."])
    first += S.say("Prioress", [
        "They are What Ought To Work.",
        "They have a doctrine. We never had a",
        "doctrine. We had soup."])
    first += S.say("Prioress", [
        "So now we hold symposia. This",
        "is the eleventh. An order that holds",
        "one symposium is thinking. An order",
        "that holds eleven has stopped."])
    first += S.narrate([
        "She says it the way a physician names a symptom she has",
        "seen before, in other people."])
    first += S.say("Prioress", [
        "Sister Bewick is right about",
        "everything. I have read her paper. It",
        "is a very good paper. Nobody who has",
        "read it is any better."])

    # Merribell in the party is a reaction shot, not MER-1.
    merri = S.narrate([
        "The Prioress's eyes find Merribell, and stop there."])
    merri += S.say("Prioress", ["Sister."])
    merri += S.say("Merribell", ["Prioress."])
    merri += S.say("Prioress", [
        "You look well. You look",
        "hydrated."])
    merri += S.say("Merribell", ["I am."])
    merri += S.say("Prioress", [
        "Good. We'll talk. Not today.",
        "Today there's a symposium, and I know",
        "what that means."])
    merri += S.narrate([
        "Merribell nods. Neither of them says anything else, very",
        "professionally."])
    first += R.if_then(R.condition_actor_in_party(db.MERRI), merri)

    later = S.say("Prioress", [
        "The symposium's at three, in",
        "the chapel. Bring a chair. There's a",
        "shortage, owing to the symposium."])
    return _pair(first, later)


def bewick_pages():
    first = S.narrate([
        "A young Sister in the same white habit, with every trim",
        "on it dyed black, stands very straight at a desk with",
        "her books on it."])
    first += S.say("Sister Bewick", [
        "Sister Bewick, of the",
        "Order of What Ought To Work. You will",
        "want to know the difference."])
    first += S.narrate(["You had not been going to ask."])
    first += S.say("Sister Bewick", [
        "Whatever Works has no",
        "doctrine. It cannot be examined on it.",
        "We can. We have been. We passed."])
    first += S.narrate(["You ask how her patients are getting on."])
    first += S.say("Sister Bewick", [
        "I have lost eleven",
        "this month."])
    first += S.narrate(["You say that you are very sorry."])
    first += S.say("Sister Bewick", [
        "To the other half of",
        "the ward. They walk across in the",
        "night. They say there is soup."])
    first += S.say("Sister Bewick", [
        "Soup is not the correct",
        "treatment. I have the correct treatment",
        "here, in writing. Volume three."])
    first += S.narrate([
        "She means every word of it, and she is winning every",
        "argument in the building. You find that you like her."])

    # Merribell in the party is a reaction shot, not MER-1.
    merri = S.narrate([
        "Merribell's eye has gone to the jug on Sister Bewick's",
        "desk. It is empty, and has been for some time."])
    merri += S.narrate([
        "She fills it from her own flask, without a word, and puts",
        "it back."])
    merri += S.narrate([
        "Sister Bewick looks at the jug. Then she opens a notebook",
        "and writes, very neatly: Intervention. Unsupported."])
    first += R.if_then(R.condition_actor_in_party(db.MERRI), merri)

    later = S.say("Sister Bewick", [
        "Volume three, chapter",
        "nine. The correct treatment, set out in",
        "full. Nobody has ever needed it yet."])
    return _pair(first, later)


def hamo_pages():
    first = S.narrate([
        "An old man in a nightshirt, with a knight's surcoat over",
        "it, stands at the foot of the bed that is exactly on the",
        "line."])
    first += S.say("Sir Hamo", [
        "Sir Hamo Tench, of the",
        "Order of the Errant. In the field."])
    first += S.narrate(["You look at the bed."])
    first += S.say("Sir Hamo", [
        "Fourteen years. Came in",
        "with a cough. The sea air, you see.",
        "Came here specially."])
    first += S.say("Sir Hamo", [
        "Bed's on the line, so",
        "both lots treat me. Soup at noon,",
        "correct treatment at four. Cough's",
        "exactly the same. Very fair."])
    first += S.say("Sir Hamo", [
        "Write to Coldbarrow every",
        "quarter: IN THE FIELD. True, too.",
        "They've a pin in me."])

    # Sir Aldric in the party is a reaction shot, not ALD-2 or ALD-3.
    aldric = S.narrate([
        "He sees Sir Aldric, and straightens up out of the cough",
        "like a younger man."])
    aldric += S.say("Sir Hamo", [
        "Pemberton-Gore! They've",
        "got you here too, you know. On the",
        "great map. Red pin."])
    aldric += S.say("Aldric", [
        "Have they? Then for once",
        "I'm where it says."])
    aldric += S.narrate([
        "They salute one another, one of them in a nightshirt,",
        "entirely seriously."])
    first += R.if_then(R.condition_actor_in_party(db.ALDRIC), aldric)

    later = S.say("Sir Hamo", [
        "Still in the field. Cough's",
        "holding up. Soup at noon."])
    return _pair(first, later)


def lamb_pages():
    first = S.narrate([
        "A Sister of Whatever Works is ladling soup out of a pot",
        "the size of a bath, for anybody who holds out a bowl."])
    first += S.say("Sister Lamb", [
        "Soup? It's leek. It's always",
        "leek. It works."])
    first += S.narrate(["You ask what it is for."])
    first += S.say("Sister Lamb", [
        "Everything, dear. Colds,",
        "falls, fevers. Mr Nuttall came in with",
        "his arm. He's had the soup."])
    first += S.narrate([
        "You look at Mr Nuttall. He is eating his soup with his",
        "good arm, very happily."])
    later = S.say("Sister Lamb", ["Leek. It works."])
    return _pair(first, later)


def ward_events():
    x1, y1, x2, y2 = WARD
    evs = [exit_tile_in(1)]
    evs.append(_person(2, "Prioress Stope", STOPE,
                       R.image("Gen_People5", 1, direction=2), *stope_pages()))
    evs[-1]["pages"] += q_merribell.stope_pages(evs[-1]["pages"][-1])   # MER-1
    evs.append(_person(3, "Sister Bewick", BEWICK,
                       R.image("Gen_People5", 2, direction=4),
                       *bewick_pages()))
    evs[-1]["pages"] += q_merribell.bewick_pages(evs[-1]["pages"][-1])  # MER-1
    evs.append(_person(4, "Sir Hamo Tench", HAMO,
                       R.image(*S.FACES["Sir Hamo"], direction=8), *hamo_pages()))
    evs.append(_person(5, "Sister Lamb", LAMB,
                       R.image(*S.FACES["Sister Lamb"], direction=4), *lamb_pages()))

    # 6: Mr Nuttall, who crossed.
    nuttall = S.say("Mr Nuttall", [
        "Came in Tuesday. Started",
        "over that side. Crossed Wednesday."])
    nuttall += S.say("Mr Nuttall", [
        "Much better this side.",
        "Nobody asks you anything this side",
        "except whether you're warm."])
    evs.append(S.npc(6, "Mr Nuttall", *NUTTALL, nuttall, *S.FACES["Mr Nuttall"],
                     direction=2))

    # 7: Mr Dace, on the correct treatment.
    dace = S.narrate([
        "A patient stands by a very tidy bed, holding up one",
        "finger."])
    dace += S.say("Mr Dace", [
        "It's a splinter. Sister",
        "Bewick says a splinter is how the ague",
        "starts. She's got it in writing."])
    dace += S.say("Mr Dace", [
        "I'm on the correct",
        "treatment. Day four. It's very",
        "thorough."])
    dace += S.narrate([
        "He looks, briefly and wistfully, across the line at the",
        "soup."])
    evs.append(S.npc(7, "Mr Dace", *DACE, dace, *S.FACES["Mr Dace"], direction=2))

    # 8: the line, the notice over it, and the minutes on the table.
    line = S.narrate([
        "A notice, pinned to the wall above the line:",
        "",
        "PATIENTS WILL KINDLY REMAIN IN THE HALF OF THE WARD TO",
        "WHICH THEY WERE ADMITTED."])
    line += S.narrate([
        "On the table under it, the minutes of the symposia, open.",
        "Ten of them, and every one ends the same way: Resolved,",
        "that the matter be referred to the next symposium."])
    evs.append(R.event(8, "The Line", *MINUTES, [R.page(line, **PAGE)]))
    evs[-1]["pages"] += q_merribell.line_pages(evs[-1]["pages"][0])    # MER-1

    # 9: the correct treatment, in eleven stages.
    treatment = S.narrate([
        "THE CORRECT TREATMENT OF THE WEEPING BOTTOM AGUE, in",
        "Sister Bewick's hand, in eleven stages, each with its",
        "authority."])
    treatment += S.narrate([
        "Stage eleven reads: The patient will now feel better.",
        "It is underlined twice."])
    evs.append(R.event(9, "The Correct Treatment", *TREATMENT,
                       [R.page(treatment, **PAGE)]))

    # 10: an empty bed on the east side.
    bed = S.narrate([
        "A bed made up so tightly you could bounce a coin off it.",
        "Somebody has: the coin is on the pillow. Nobody has been",
        "in it since Monday. There are slipper prints in the dust,",
        "going west."])
    evs.append(R.event(10, "An Empty Bed", *EMPTY_BED, [R.page(bed, **PAGE)]))

    # 11: the medicine shelf.
    shelf = S.narrate([
        "The Order's pharmacy: jars of honey and of salt, a brown",
        "tonic, and one large jar labelled, in a firm hand,",
        "SOUP (CONCENTRATED)."])
    evs.append(R.event(11, "The Medicine Shelf", MEDICINE_X, y1,
                       [R.page(shelf, **PAGE)]))

    # 12: the east wall's books.
    books = S.narrate([
        "DISEASES PROPERLY SO CALLED, in nine volumes, and the",
        "Order's commentaries on it, in fourteen. Volume three is",
        "missing. It is on Sister Bewick's desk, open."])
    evs.append(R.event(12, "The Doctrine", SHELVES_X[0], y1,
                       [R.page(books, **PAGE)]))
    return evs


def exit_tile_in(event_id):
    """The ward's door, back out into the drizzle."""
    x1, y1, x2, y2 = WARD
    return R.event(event_id, "Ward Door", WARD_DOOR_X, y2 + 2, [R.page(
        [R.play_se("Move1"),
         R.transfer(MAP_WEEPING_BOTTOM, HOUSE_DOOR[0], HOUSE_DOOR[1] + 1,
                    2, 0)],
        img=R.image(""), trigger=1, priority=0, through=True)])


# ================================================================= the door ==
def world_doors(base_id, cells):
    """The real door into Weeping Bottom, on the world map.

    `cells` is the one square `worldmap.json` put a placeholder on for this
    site, handed in by `journey.world_map`. Player-touch and below
    characters, the world map's idiom for a place you walk into."""
    evs = []
    for i, (x, y) in enumerate(sorted(cells)):
        arrive = S.narrate([
            "The track goes down between the rock and the sea, into a",
            "hollow where the fog off the water has come to rest and",
            "not left. At the bottom, a white house, and every wall of",
            "it wet."])
        arrive += R.choice_block(
            ["Go down", "Press on"],
            [[R.transfer(MAP_WEEPING_BOTTOM, *ARRIVE, 8, 0)],
             S.narrate(["You press on. Somebody down in the fog",
                        "coughs, politely."])])
        evs.append(R.event(base_id + i, SITE, x, y, [R.page(
            arrive, img=R.image(""), trigger=1, priority=0, through=True)]))
    return evs


def build():
    R.save_map(MAP_WEEPING_BOTTOM, valley_map())
    R.save_map(MAP_WARD, ward_map())
