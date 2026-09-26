"""Maps 52-53: Ashcombe, the village that is fine.

`../SITES.md` step 14. The source is `../COMPANIONS.md` L3 - "possibly the
funniest single location in the document", and "it exists to be pleasant at
somebody" - and the two quests it serves, COR-1 (going home) and COR-2 (the
sunken ruin). The somebody is **Corvin Ash**, whose village this is: it went
under while he was away, everybody was fine, and they built it again eight
miles off, only better, and kept the name. This module builds the place and
the people and **not the quests**, which are appended later as pages of their
own. Nothing here spends either.

* **The world-map door is claimed by name**, `journey.world_map`'s mechanism.
  The stamp is two cells of `Village A` - a small fenced hamlet on open grass,
  forest to the west, a dirt road up from the south-east, and **Ashcombe Lake**
  just to its north-east. `places.py` has `ASHCOMBE_STEP`, the grass one south
  of the western cell, and no world coordinate.
* **It agrees with the lake**, `nomap.py`'s `_ashcombe_lake`, step 7: the old
  village is under the water and they took the old church bell *with them*,
  and it rings up the road calling somebody in for their dinner. So the new
  church has the old bell and a rope by the door, and ringing it gets
  somebody shouting COMING! from up the street.
* **And it agrees with Corvin**, who told the Slain Wyvern they moved "eight
  miles inland" - while the lake's own line puts the new village a few steps
  from its shore. Mr Weir reconciles them, proudly: eight miles is *by the
  road*, which goes all the way round the lake.
* **COR-1 is not spent.** Nobody is delighted to see Corvin, because he does
  not arrive: with him in the party he stops on his mother's path and says
  "Not today", and nobody goes in - `optFollowers` is on, so he cannot wait
  outside while his sprite walks into her kitchen. The plaque and the museum
  get reaction shots that cost nothing. The Flood Dinner's speaker is TO BE
  CONFIRMED, Mrs Ash is knitting something long for "somebody who feels the
  cold", and neither the invitation nor the scarf is handed over; the
  bedroom that is now a study is not built.
* **COR-2 is not spent either.** The drowned street, its doorstep and the
  report card are the lake's week, and it is not this week. The Roll in the
  museum has one name marked Away. (Written to.) in place of a tick, and does
  not say whose.
* **One trope** - the hero's home village, destroyed, turned round: the plaque
  is upbeat. **No blush**: the place is warm, not red.
"""
import mapkit as K
import rmmzdata as R

import db
import story as S
from places import MAP_WORLD, MAP_ASHCOMBE, MAP_ASHCOMBE_IN, ASHCOMBE_STEP

# The name `worldmap.json`'s door events carry for this site.
SITE = "Ashcombe"


# ================================================================ the village ==
VW, VH = 40, 26
STREET_Y = 14                       # the street: rows 14 and 15
ROAD_X = 26                         # the road in from the south: 26 and 27
FRONT_Y = 12                        # the bottom wall row of the north side
LANE_Y = 23                         # behind the post office, which faces south

#           x  y  w  h
CHURCH = (2, 4, 7, 9)
SCHOOL = (11, 7, 7, 6)
ASH_HOUSE = (20, 8, 5, 5)
MUSEUM = (27, 7, 7, 6)
POST = (17, 18, 5, 5)

CHURCH_DOOR = (5, FRONT_Y)
SCHOOL_DOOR = (14, FRONT_Y)
ASH_DOOR = (22, FRONT_Y)
MUSEUM_DOOR = (30, FRONT_Y)
POST_DOOR = (19, POST[1] + POST[3] - 1)

# The lake comes in at the north-east corner, in a rim of sand, the way the
# world map draws it.
SAND_X, WATER_X, WATER_Y = 34, 36, 13
PLAQUE = (35, 12)                   # facing the water; read from the sand below
NOTICE = (6, 16)                    # the Flood Dinner, read from the street
WILF = (10, 18)                     # a boy with a paper boat
DIMMOCK = (18, LANE_Y)              # the postmistress, at her own door
LAMPS = [(4, 16), (13, 16), (29, 16), (33, 16)]
ARRIVE = (ROAD_X, VH - 2)

ALLOTMENTS = (6, 19, 12, 21)        # x1, y1, x2, y2
CROPS = [K.sf_tile("Outside_B", "Crops %s" % c) for c in "ABCD"]
SCARECROW = K.sf_tile("Outside_B", "Scarecrow")
SAND = K.SOIL                       # `K.SOIL` is the sheet's `Sand`: step 13
PLAQUE_TILE = K.sf_tile("Outside_C", "Monument C")


def ashcombe_map():
    w, h = VW, VH
    g = K.Canvas(w, h)
    g.fill(0, 0, w - 1, h - 1, 0, K.GRASS)

    # The lake, in the corner, and its sandy shore.
    g.fill(SAND_X, 0, w - 1, STREET_Y + 1, 0, SAND)
    g.fill(WATER_X, 0, w - 1, WATER_Y, 0, K.WATER)

    # The street, the road in, every doorstep, and the post office's lane.
    g.fill(2, STREET_Y, SAND_X + 1, STREET_Y + 1, 0, K.PATH)
    g.fill(ROAD_X, STREET_Y, ROAD_X + 1, h - 1, 0, K.PATH)
    for x, _ in (CHURCH_DOOR, SCHOOL_DOOR, ASH_DOOR, MUSEUM_DOOR):
        g.set(x, FRONT_Y + 1, 0, K.PATH)
    g.fill(POST[0], LANE_Y, ROAD_X - 1, LANE_Y, 0, K.PATH)
    # The allotments, in a square of dug earth. `K.SAND` is the sheet's
    # `Dirt`: step 13.
    g.fill(*ALLOTMENTS, 0, K.SAND)

    # Every building newer and better than what it replaced.
    g.building(*CHURCH, wall=K.WALL_STONE_WHITE, roof=K.ROOF_GREEN)
    g.building(*SCHOOL, wall=K.WALL_BRICK_RED, roof=K.ROOF_GOLD)
    g.building(*ASH_HOUSE, wall=K.WALL_PLASTER, roof=K.ROOF_GREEN)
    g.building(*MUSEUM, wall=K.WALL_STONE_WHITE, roof=K.ROOF_GOLD)
    g.building(*POST, wall=K.WALL_BRICK_RED, roof=K.ROOF_GREEN)
    g.autotile(0)

    # Fronts. Mrs Ash's door and the museum's are events; the rest are shut.
    g.column(CHURCH_DOOR[0], FRONT_Y - 1, 3, K.DOOR_DOUBLE)
    g.column(CHURCH_DOOR[0] - 2, FRONT_Y - 1, 3, K.WINDOW_GLASS)
    g.column(CHURCH_DOOR[0] + 2, FRONT_Y - 1, 3, K.WINDOW_GLASS)
    g.column(SCHOOL_DOOR[0], FRONT_Y - 1, 3, K.DOOR_SHUT)
    for x in (12, 16):
        g.set(x, FRONT_Y, 3, K.WINDOW)
    g.set(ASH_DOOR[0] + 2, FRONT_Y, 3, K.WINDOW)
    g.set(ASH_DOOR[0] - 1, FRONT_Y, 3, K.WINDOW)
    g.set(MUSEUM_DOOR[0] - 1, FRONT_Y - 1, 3, K.SIGN_SUN)
    for x in (28, 32):
        g.set(x, FRONT_Y, 3, K.WINDOW)
    g.column(POST_DOOR[0], POST_DOOR[1] - 1, 3, K.DOOR_SHUT)
    g.set(POST_DOOR[0] + 1, POST_DOOR[1] - 1, 3, K.SIGN_RING)   # the sack
    g.set(POST_DOOR[0] + 2, POST_DOOR[1], 3, K.WINDOW)
    g.set(ASH_HOUSE[0] + 1, ASH_HOUSE[1], 2, K.STOVEPIPE)
    g.set(SCHOOL[0] + 5, SCHOOL[1], 2, K.STOVEPIPE)

    # Mrs Ash's front garden, and flowers along every front.
    g.scatter([(20, 13), (21, 13), (23, 13), (24, 13)], 3, K.FLOWERS2)
    g.scatter([(3, 13), (7, 13), (11, 13), (17, 13), (28, 13), (32, 13)], 3,
              K.FLOWERS)

    # The green south of the street: the notice, the lamps, the flower beds.
    g.set(*NOTICE, 3, K.FENCE_PANEL)                    # `Sign B`, a board
    for x, y in LAMPS:
        g.column(x, y - 1, 3, K.LAMP)
    g.set(*PLAQUE, 3, PLAQUE_TILE)
    g.scatter([(3, 18), (4, 22), (15, 21), (24, 18), (33, 22)], 3,
              K.FLOWERS3)
    g.scatter([(2, 20), (14, 22), (23, 20), (31, 22)], 3, K.BUSH)
    ax1, ay1, ax2, ay2 = ALLOTMENTS
    for i, x in enumerate(range(ax1, ax2 + 1)):
        for y in (ay1, ay2):
            g.set(x, y, 3, CROPS[(i + y) % len(CROPS)])
    g.set(ax1 + 3, ay1 + 1, 3, SCARECROW)
    # The orchard, south-east of the street; and the wood behind the north
    # side, so the roofs stand against trees and not an empty field.
    for x, y in [(14, 17), (29, 17), (33, 17), (31, 20), (35, 20)]:
        g.blit(x, y, 3, K.TREE)
    for x in range(2, SAND_X - 1, 2):
        g.blit(x, 2, 3, K.TREE)
    for x in range(10, SAND_X - 1, 2):
        g.blit(x, 4, 3, K.TREE)
    for x in range(18, 26, 2):
        g.blit(x, 6, 3, K.TREE)

    # The wood to the west and along the top, and the south edge, with the
    # road's gap in it.
    for x in range(0, SAND_X, 2):
        g.blit(x, 0, 3, K.TREE)
    for x in range(0, w, 2):
        if not (ROAD_X - 1 <= x <= ROAD_X + 1):
            g.blit(x, h - 2, 3, K.TREE)
    for y in range(2, h - 2, 2):
        g.blit(0, y, 3, K.TREE)
    for y in range(STREET_Y + 3, h - 2, 2):
        g.blit(w - 2, y, 3, K.TREE)

    m = K.new_map(w, h, K.TS_OUTSIDE, name="Ashcombe", bgm="Town1")
    m["data"] = g.data
    m["events"] = [None] + ashcombe_events()
    return m


def _pair(first, later):
    """A first conversation and the short one after it, on self switch A."""
    return first + [R.self_switch("A", True)], later


def _person(event_id, name, xy, img, first, later):
    return R.event(event_id, name, *xy, [
        R.page(first, img=img, trigger=0, priority=1),
        R.page(later, img=img, trigger=0, priority=1,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ])


def ash_door():
    """Mrs Ash's front door, which Corvin does not go through.

    COR-1 is him going home, so with him in the party the door is a refusal
    and not a transfer: he stops on the path, and you do not go in without
    him. Followers are drawn, so he cannot wait at the gate while his sprite
    follows you into her kitchen. COR-1 appends its own page after these."""
    img = R.image("!Door1", 0, direction=2)
    tx, ty = KITCHEN[4], KITCHEN[3]
    corvin = {"actorValid": True, "actorId": db.CORVIN}
    stop = S.narrate([
        "Corvin stops on the path. He looks at the new front",
        "door, and the new window, and at somebody's knitting",
        "going on behind it."])
    stop += S.say("Corvin", ["...Not today."])
    stop += S.narrate([
        "He says it like a man who has been saying it for eleven",
        "years and has got good at it. You do not go in either.",
        "It would not be kind."])
    stop += [R.self_switch("A", True)]
    again = S.say("Corvin", ["Not today."])
    return R.event(3, "Mrs Ash's Door", *ASH_DOOR, [
        R.page(S.door_page(MAP_ASHCOMBE_IN, tx, ty, 8), img=img, trigger=1,
               priority=1),
        R.page(stop, img=img, trigger=1, priority=1, conditions=corvin),
        R.page(again, img=img, trigger=1, priority=1,
               conditions=dict(corvin, selfSwitchValid=True,
                               selfSwitchCh="A")),
    ])


def plaque_pages():
    first = S.narrate([
        "A plaque of polished stone, set up facing the lake, with",
        "the gilt still bright in the letters:"])
    first += S.narrate([
        "HERE, ON THE DAY OF THE WATER, EVERY SOUL IN OLD",
        "ASHCOMBE CAME SAFE UP THE HILL, AND WAS DRY BY TEATIME.",
        "",
        "WE BUILT IT AGAIN, ONLY BETTER."])
    first += S.narrate([
        "And under that, smaller:",
        "",
        "Mind the drains. They are very good.",
        "Visit the Museum! (Free.)"])
    first += [S.trope()]
    # Corvin in the party is a reaction shot, not COR-1.
    corvin = S.narrate([
        "Corvin reads the plaque. Then he reads it again, slower,",
        "as if it might say something else the second time."])
    corvin += S.say("Corvin", ["'Visit the Museum.'"])
    corvin += S.narrate([
        "He says nothing else. The lake laps at the sand,",
        "cheerfully."])
    first += R.if_then(R.condition_actor_in_party(db.CORVIN), corvin)
    later = S.narrate([
        "WE BUILT IT AGAIN, ONLY BETTER.",
        "Mind the drains. They are very good."])
    return _pair(first, later)


def church_pages():
    look = S.narrate([
        "The new church, in pale stone, with a green roof and",
        "coloured glass in every window."])
    look += S.narrate([
        "A rope hangs by the door, for the bell. The bell is the",
        "old one: they brought it up the hill on a cart on the day",
        "of the water, and did not see why they shouldn't."])
    ring = [R.play_se("Bell1", volume=80), R.wait(40),
            R.play_se("Bell1", volume=60), R.wait(40)]
    ring += S.narrate([
        "Up the street a door flies open, and somebody shouts",
        "COMING! - and then, a moment later, rather put out:",
        "\"Oh. It isn't six.\""])
    look += R.choice_block(["Ring the bell", "Leave it be"], [
        ring, S.narrate(["You leave it be. It is nearly six anyway."])])
    return look


def dimmock_pages():
    first = S.say("Mrs Dimmock", [
        "Hello, dear! Anything",
        "to post? Everything that comes to",
        "Ashcombe gets answered. It's policy."], face=False)
    first += S.say("Mrs Dimmock", [
        "We had one, years back,",
        "addressed to THE RUINS OF ASHCOMBE."], face=False)
    first += S.say("Mrs Dimmock", [
        "So the Ruins wrote back.",
        "Lovely long letter. Hoped he was",
        "keeping warm."], face=False)
    later = S.say("Mrs Dimmock", [
        "Nothing for you today,",
        "dear. Every letter answered!"], face=False)
    return _pair(first, later)


def ashcombe_events():
    evs = []
    # 1-2: the road out, both cells of it, below characters.
    for i in range(2):
        evs.append(S.exit_tile(i + 1, "The Road Out", ROAD_X + i, VH - 1,
                               MAP_WORLD, *ASHCOMBE_STEP))

    # 3: Mrs Ash's door; 4: the museum's.
    evs.append(ash_door())
    evs.append(S.door(4, "The Drainage Museum", *MUSEUM_DOOR,
                      MAP_ASHCOMBE_IN, MUSEUM_ROOM[4], MUSEUM_ROOM[3],
                      direction=8))

    page = dict(img=R.image(""), trigger=0, priority=1, direction_fix=True)

    # 5: the plaque, and the site's trope.
    first, later = plaque_pages()
    evs.append(R.event(5, "The Plaque", *PLAQUE, [
        R.page(first, **page),
        R.page(later, conditions={"selfSwitchValid": True,
                                  "selfSwitchCh": "A"}, **page)]))

    # 6: the church door, and the bell the lake says they took with them.
    evs.append(R.event(6, "The Church", *CHURCH_DOOR,
                       [R.page(church_pages(), **page)]))

    # 7: the school, which is very good.
    school = S.narrate([
        "ASHCOMBE SCHOOL, on a brass plate, polished. Under it, on",
        "a smaller brass plate, also polished:",
        "",
        "       'Very Good.'  - H.M. Inspector of Schools"])
    school += S.narrate([
        "Through the window: rows of new desks, a globe, and a map",
        "of the world on the wall with Ashcombe marked on it twice."])
    evs.append(R.event(7, "The School", *SCHOOL_DOOR, [R.page(school, **page)]))

    # 8: the post office, which answers its correspondence.
    post = S.narrate([
        "POST OFFICE. A card in the window says ALL LETTERS",
        "ANSWERED, and under it, in the same hand, WE MEAN IT."])
    evs.append(R.event(8, "The Post Office", *POST_DOOR,
                       [R.page(post, **page)]))

    # 9: the Flood Dinner. The speaker is COR-1's, and is not confirmed.
    notice = S.narrate([
        "THE ANNUAL FLOOD DINNER",
        "Saturday, at the church hall. Soup, a fish, a pudding,",
        "and speeches."])
    notice += S.narrate([
        "Speaker: TO BE CONFIRMED.",
        "",
        "And under that, in pencil: Mr Weir has kindly offered.",
        "Again."])
    evs.append(R.event(9, "The Flood Dinner", *NOTICE,
                       [R.page(notice, **page)]))

    # 10: a boy with a paper boat and nowhere to sail it.
    wilf = S.narrate([
        "A small boy with a paper boat, looking for somewhere to",
        "sail it."])
    wilf += S.say("Wilf", [
        "There's no puddles. Mr Weir",
        "says there won't ever be a puddle",
        "again. He says it like it's good."], face=False)
    wilf += S.narrate([
        "You look. There are no puddles. There is not so much as a",
        "damp patch."])
    evs.append(S.npc(10, "Wilf", *WILF, wilf, "People1", 2, direction=2))

    # 11: the postmistress, at her own door on the lane.
    evs.append(_person(11, "Mrs Dimmock", DIMMOCK,
                       R.image("People1", 5, direction=2), *dimmock_pages()))
    return evs


# ================================================================== indoors ==
# One map, two rooms in the black: Mrs Ash's kitchen to the west and the
# Drainage Museum to the east. The map shows no name on arrival, because it is
# two places.
IW, IH = 26, 13
#            x1  y1  x2  y2  door_x
KITCHEN = (2, 4, 9, 8, 5)
MUSEUM_ROOM = (14, 4, 23, 8, 18)

OVEN = K.sf_tile("Inside_B", "Oven")
SINK = K.sf_tile("Inside_B", "Sink")
COUNTER_A = K.sf_tile("Inside_B", "Kitchen Counter A")
COUNTER_B = K.sf_tile("Inside_B", "Kitchen Counter B")
DRESSER = K.sf_block("Inside_B", "Dish Cabinet")        # 1x2, on its base
CLOCK = K.sf_block("Inside_B", "Clock")                 # 1x2
TABLE_D = K.sf_tile("Inside_B", "Table D")
CHAIR = K.sf_block("Inside_B", "Chair A (Wood)")        # 1x2, faces south
TEAPOT = K.sf_tile("Inside_C", "Teapot A")
UTENSILS = K.sf_tile("Inside_C", "Cooking Utensils")
LAKE_PAINTING = K.sf_block("Inside_B", "Painting")      # 2x1: a lake
NOTICE_IN = K.sf_tile("Inside_B", "Posted Notice")
PLAN = K.sf_tile("Inside_C", "Map B (H)")
PLINTH = K.sf_tile("Inside_C", "Dais")
BASKET = K.sf_tile("Inside_C", "Basket A")             # empty, cloth-lined
STOOL = K.sf_tile("Inside_B", "Stool A")
OLD_DRAIN = K.sf_tile("Inside_B", "Stone Tablet")

DRESSER_X = 9
MRS_ASH = (7, 7)
KITCHEN_TABLE = (5, 7)              # two cells of `Table D`
PAINTING_AT = (15, 3)               # two cells, on the wall face
ROLL_X, MENUS_X = 19, 21
PLAN_AT = (16, 6)                   # two cells of `Table D`, the plan on them
PLINTH_AT = (21, 6)
OLD_DRAIN_AT = (19, 5)
BASKET_AT = (8, 8)
WEIR = (19, 7)


def _room(g, x1, y1, x2, y2, door_x, floor, top, face):
    """`mapkit.interior`'s walls and doorway, for a second room on the same
    canvas - `gladhollow._room`, with the door cut the way `interior` cuts
    it."""
    g.fill(x1, y1, x2, y2, 0, floor)
    g.fill(x1 - 1, y1 - 3, x2 + 1, y1 - 3, 0, top)
    g.fill(x1, y1 - 2, x2, y1 - 1, 0, face)
    for y in range(y1 - 2, y2 + 2):
        g.set(x1 - 1, y, 0, top)
        g.set(x2 + 1, y, 0, top)
    g.fill(x1 - 1, y2 + 1, x2 + 1, y2 + 1, 0, top)
    g.fill(x1, y2 + 2, x2, y2 + 3, 0, face)
    g.set(door_x, y2 + 1, 0, floor)
    g.set(door_x, y2 + 2, 0, K.a5(91))
    g.set(door_x, y2 + 3, 0, K.a5(91))


def indoors_map():
    x1, y1, x2, y2, door_x = KITCHEN
    g = K.interior(IW, IH, x1, y1, x2, y2, door_x=door_x,
                   floor=K.IN_WOOD_FLOOR, wall_top=K.IN_WALL_TOP_WHITE,
                   wall_face=K.IN_WALL_FACE_WHITE)
    _room(g, *MUSEUM_ROOM, K.IN_DIAMOND_TILE, K.IN_WALL_TOP_RED,
          K.IN_WALL_FACE_RED)

    # Rugs. Layer 1 is floor art.
    g.fill(4, 6, 7, 8, 1, K.IN_GREEN_RUG)
    g.fill(16, 7, 21, 8, 1, K.IN_RED_CARPET)
    g.autotile(1)

    # -- the kitchen: all new. The range, the sink and the counters along
    # the north wall, a big window over the lake, the dresser and the clock.
    for x, tile in [(2, OVEN), (3, COUNTER_B), (4, SINK), (5, COUNTER_A)]:
        g.set(x, y1, 2, tile)
    g.set(3, y1 - 1, 3, UTENSILS)
    g.column(7, y1 - 2, 3, K.IN_WINDOW)
    g.column(8, y1 - 1, 2, CLOCK)
    g.column(DRESSER_X, y1 - 1, 2, DRESSER)
    g.set(KITCHEN_TABLE[0], KITCHEN_TABLE[1], 2, TABLE_D)
    g.set(KITCHEN_TABLE[0] + 1, KITCHEN_TABLE[1], 2, TABLE_D)
    g.column(KITCHEN_TABLE[0], KITCHEN_TABLE[1] - 2, 2, CHAIR)
    g.set(KITCHEN_TABLE[0] + 1, KITCHEN_TABLE[1], 3, TEAPOT)
    g.set(KITCHEN_TABLE[0] - 1, KITCHEN_TABLE[1], 2, STOOL)
    g.set(*BASKET_AT, 3, BASKET)
    g.set(x1, y2, 3, K.INC_PLANT2)
    g.set(x2, y2, 3, K.INC_PLANT2)

    # -- the museum. The lake on the wall, the Roll and the menus framed
    # beside it, the plan of the drains on a table, and the plinth.
    mx1, my1, mx2, my2, _ = MUSEUM_ROOM
    g.set(PAINTING_AT[0], PAINTING_AT[1], 3, LAKE_PAINTING[0])
    g.set(PAINTING_AT[0] + 1, PAINTING_AT[1], 3, LAKE_PAINTING[1])
    g.set(ROLL_X, my1 - 1, 3, NOTICE_IN)
    g.set(MENUS_X, my1 - 1, 3, NOTICE_IN)
    g.set(PLAN_AT[0], PLAN_AT[1], 2, TABLE_D)
    g.set(PLAN_AT[0] + 1, PLAN_AT[1], 2, TABLE_D)
    g.set(PLAN_AT[0], PLAN_AT[1], 3, PLAN)
    g.set(*PLINTH_AT, 2, PLINTH)
    g.set(*OLD_DRAIN_AT, 2, OLD_DRAIN)
    for x, y in [(mx1, my1), (mx2, my1), (mx1, my2), (mx2, my2)]:
        g.set(x, y, 3, K.INC_PLANT2)

    m = K.new_map(IW, IH, K.TS_INSIDE, name="Ashcombe, Indoors", bgm="Town1",
                  battleback=("Wood1", "Room1"))
    m["displayName"] = ""
    m["data"] = g.data
    m["events"] = [None] + indoors_events()
    return m


def ash_pages():
    first = S.narrate([
        "A kitchen so new that the paint still smells of it, with",
        "a big window over the lake. A woman at the table is",
        "knitting something long, and does not stop."])
    first += S.say("Mrs Ash", [
        "Hello, dear! Come in, come in.",
        "Mind the step. It's new. It's all new.",
        "Isn't it lovely?"])
    first += S.narrate([
        "You say that you are the Chosen One. Number forty-eight."])
    first += S.say("Mrs Ash", [
        "How nice. Sit down, I'll put",
        "the kettle on. It's a new kettle."])
    first += S.narrate(["You ask, carefully, about the flood."])
    first += S.say("Mrs Ash", [
        "Oh, the flood. It was a Tuesday.",
        "We all went up the hill with the kettles,",
        "and by teatime we'd decided to build it",
        "again, only better."])
    first += S.say("Mrs Ash", [
        "The old kitchen was DARK. You",
        "couldn't see your potatoes. Look at the",
        "light in here. I can see every potato",
        "I own."])
    first += S.narrate(["You ask whether she has family."])
    first += S.say("Mrs Ash", [
        "My boy's away. He wrote to say",
        "he'd taken the name Ash, after the",
        "village, in its memory. Well, I thought,",
        "that's nice."])
    first += S.say("Mrs Ash", [
        "So I took it as well, to save",
        "the postman. Now we're all Ashes, and",
        "the post comes lovely. He's very deep,",
        "my boy."])
    first += S.narrate([
        "The knitting has got longer while she talks. You ask who",
        "it is for."])
    first += S.say("Mrs Ash", [
        "Somebody who feels the cold",
        "and won't say so."])
    later = S.say("Mrs Ash", [
        "More tea, dear? It's a new pot.",
        "Everything's new. Isn't it lovely?"])
    later += S.narrate(["The knitting is longer again."])
    return _pair(first, later)


def weir_pages():
    first = S.narrate([
        "A man in a coat with gold frogging stands in the middle of",
        "the room with his hands behind his back, the way a man",
        "stands in a room he is proud of."])
    first += S.say("Mr Weir", [
        "Welcome to the Ashcombe",
        "Drainage Museum! Hubert Weir, Curator.",
        "Admission is free. So is the enthusiasm."])
    first += S.narrate([
        "You say that you are the Chosen One. Number forty-eight."])
    first += S.say("Mr Weir", ["Splendid! Then you'll want the drains."])
    first += S.say("Mr Weir", [
        "Fourteen hundred yards of culvert,",
        "a fall of one in two hundred, and not one",
        "puddle in Ashcombe since the day they",
        "went in."])
    first += S.narrate(["You ask about the flood."])
    first += S.say("Mr Weir", [
        "A tremendous success. Everybody",
        "out by dinner, everybody dry by tea, and",
        "not so much as a hen lost. We have the",
        "Roll."])
    first += S.narrate([
        "You mention that you had heard the new village was eight",
        "miles inland."])
    first += S.say("Mr Weir", [
        "By the ROAD, sir. The road goes",
        "all the way round the lake. As the crow",
        "flies, you could skim a stone on to the",
        "old church roof."])
    # Corvin in the party is a reaction shot, not COR-1: nobody knows him.
    corvin = S.narrate([
        "Mr Weir's eye passes over the hooded man behind you, and",
        "moves on without stopping."])
    corvin += S.narrate([
        "Corvin is looking at the plan of the drains. After a",
        "while, very quietly:"])
    corvin += S.say("Corvin", ["...They are good drains."])
    first += R.if_then(R.condition_actor_in_party(db.CORVIN), corvin)
    later = S.say("Mr Weir", [
        "Have you seen the plan? Grown",
        "men have stood in front of that plan and",
        "gone quite quiet."])
    return _pair(first, later)


def indoors_events():
    x1, y1, x2, y2, door_x = KITCHEN
    mx1, my1, mx2, my2, mdoor_x = MUSEUM_ROOM
    evs = [S.exit_tile(1, "Kitchen Door", door_x, y2 + 2, MAP_ASHCOMBE,
                       ASH_DOOR[0], ASH_DOOR[1] + 1)]
    evs.append(_person(2, "Mrs Ash", MRS_ASH,
                       R.image("Gen_People4", 7, direction=4), *ash_pages()))

    page = dict(img=R.image(""), trigger=0, priority=1, direction_fix=True)

    # 3: the dresser, and the one letter on it.
    letter = S.narrate([
        "A dresser of the best plates. Propped against the middle",
        "one, ironed flat and read soft, a letter of one line:"])
    letter += S.narrate([
        "     Mother -  I have taken the name Ash.",
        "     Do not look for me.        C."])
    letter += S.narrate([
        "On the back, in pencil, in her hand:",
        "",
        "     The Slain Wyvern. Post Wednesdays and Saturdays."])
    evs.append(R.event(3, "The Dresser", DRESSER_X, y1,
                       [R.page(letter, **page)]))

    # 4: the museum's way out.
    evs.append(S.exit_tile(4, "Museum Door", mdoor_x, my2 + 2, MAP_ASHCOMBE,
                           MUSEUM_DOOR[0], MUSEUM_DOOR[1] + 1))

    # 5: the curator.
    evs.append(_person(5, "Hubert Weir", WEIR,
                       R.image("Gen_People5", 0, direction=2), *weir_pages()))

    # 6: the plan of the drains.
    plan = S.narrate([
        "THE DRAINS OF ASHCOMBE: a plan of every one of them, on a",
        "great sheet of parchment, drawn very carefully. Every",
        "culvert has a name, in copperplate. The longest is called",
        "Hubert."])
    evs.append(R.event(6, "The Plan", *PLAN_AT, [R.page(plan, **page)]))

    # 7: the Roll. COR-2's schoolmistress kept everybody's report card; this
    # is her hand too, and it does not say whose name is Away.
    roll = S.narrate([
        "THE ROLL, taken on the hill on the day of the water, in",
        "the schoolmistress's hand. Every name in the old village,",
        "a tick by each one, and after every tick one word: DRY."])
    roll += S.narrate([
        "Two hundred and six ticks. Beside one name, in place of a",
        "tick, in the same careful hand:",
        "",
        "     Away.  (Written to.)"])
    evs.append(R.event(7, "The Roll", ROLL_X, my1 - 1, [R.page(roll, **page)]))

    # 8: the menus.
    menus = S.narrate([
        "The menus of the Flood Dinner, pinned up one on another,",
        "one for every year. Soup, a fish, a pudding, and a toast:",
        "TO THE WATER, WHICH WAS VERY GOOD ABOUT IT."])
    menus += S.narrate([
        "At the foot of each, the speaker. The Curator. The",
        "Curator. Mrs Ash, on knitting. The Curator. The Curator."])
    evs.append(R.event(8, "The Menus", MENUS_X, my1 - 1,
                       [R.page(menus, **page)]))

    # 9: the lake, in oils.
    painting = S.narrate([
        "THE LAKE, AT EVENING. Painted for the Flood Dinner, and",
        "hung where the light falls best."])
    painting += S.narrate([
        "Under the water, very small, somebody has painted in the",
        "old church spire. It is the best bit of the picture, and",
        "they know it."])
    evs.append(R.event(9, "The Painting", PAINTING_AT[0], PAINTING_AT[1],
                       [R.page(painting, **page)]))

    # 10: the plinth.
    plinth = S.narrate([
        "An empty plinth, beautifully polished. The card on it",
        "reads:",
        "",
        "     THE FLOOD.  (On loan to the lake.)"])
    evs.append(R.event(10, "The Plinth", *PLINTH_AT, [R.page(plinth, **page)]))

    # 11: exhibit one, which was not up to it.
    drain = S.narrate([
        "EXHIBIT ONE. The stone that was set in the old high street",
        "over the only drain old Ashcombe had, lifted when the water",
        "went down. It is carved, in capitals: DRAIN."])
    drain += S.narrate([
        "The card beside it says, kindly: It was not up to it."])
    evs.append(R.event(11, "The Old Drain", *OLD_DRAIN_AT,
                       [R.page(drain, **page)]))

    # 12: her work basket.
    basket = S.narrate([
        "Her work basket. It is empty: whatever was in it is now",
        "the knitting, and the knitting is still going."])
    evs.append(R.event(12, "The Work Basket", *BASKET_AT,
                       [R.page(basket, **page)]))
    return evs


# ================================================================ the doors ==
def world_doors(base_id, cells):
    """The real door into Ashcombe, on the world map.

    `cells` is the two squares `worldmap.json` put placeholders on for this
    site, handed in by `journey.world_map`. Player-touch and below
    characters, the world map's idiom for a place you walk into."""
    evs = []
    for i, (x, y) in enumerate(sorted(cells)):
        arrive = S.narrate([
            "A village above a lake, with its roofs all new and its",
            "windows all clean, and a smell of somebody's dinner",
            "coming down the road."])
        arrive += R.choice_block(
            ["Go in", "Press on"],
            [[R.transfer(MAP_ASHCOMBE, *ARRIVE, 8, 0)],
             S.narrate(["You press on. Behind you a bell rings, and",
                        "somebody shouts COMING!"])])
        evs.append(R.event(base_id + i, SITE, x, y, [R.page(
            arrive, img=R.image(""), trigger=1, priority=0, through=True)]))
    return evs


def build():
    R.save_map(MAP_ASHCOMBE, ashcombe_map())
    R.save_map(MAP_ASHCOMBE_IN, indoors_map())
