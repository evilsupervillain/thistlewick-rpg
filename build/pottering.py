"""Maps 68-69: Much Pottering, the village where nothing has happened.

`../QUESTS.md` F3 and `../COMPANIONS.md` SPA-4. This was worldgen's "Village
1", the last placeholder on the world map, which `SITES.md` step 9 and
section 4 held back - twice - for something of Spare's. It is "a nice village
with people to talk to and funny things to walk into", and it is where his pen
pal lives.

* **The joke is the plaque.** Every story starts in a quiet village and burns
  it down by the end of the first chapter; Much Pottering has never been
  burned down, overrun, foretold, cursed or chosen, and has put up a stone to
  say so. That is the site's trope, once. **No blush**: it is warm, not red.
* **It is twinned with Upper Clanging**, chosen off the map by Mrs Throssell
  as the most different place she could find, and in 1997 the twinning gave
  one child each a pen pal: Effie Gotobed here, Spare Cotterill there. Neither
  village has visited the other. Effie has told Spare that Much Pottering has
  a volcano and a sea serpent; it has Mr Dibble's bonfire, which has not gone
  out since November, and Mr Cobley's carp, which nobody has ever seen.
* **Funny things to walk into**: Mr Dibble's fence (wet paint), the pig
  asleep across the street (it has right of way), the oak by the road in (mind
  the branch) and the wishing well. Each is player-touch at "same as
  characters", so walking into it is what starts it.
* **The pen pal is `q_spare.py`'s.** This module builds Effie at her gate as
  anybody finds her, and the courier standing at the top of the road; the
  meeting, her tour, and the four Effies it moves between are appended from
  there, one line each. Without Spare the village is complete and the quest
  is invisible.
"""
import mapkit as K
import rmmzdata as R

import db
import story as S
import q_spare
from places import MAP_WORLD, MAP_POTTERING, MAP_POTTERING_IN, POTTERING_STEP

# The name `worldmap.json`'s door events carry for this site.
SITE = "Village 1"


# ================================================================ the village ==
VW, VH = 40, 28
FRONT_Y = 11                        # the bottom wall row of the north side
STREET_Y = 14                       # the street: rows 14 and 15
ROAD_X = 19                         # the road in from the south: 19 and 20

#             x  y  w  h
GOTOBED = (4, 6, 6, 6)
DIBBLE = (12, 7, 5, 5)
HALL = (22, 6, 8, 6)
THROSSELL = (32, 7, 5, 5)

GOTOBED_DOOR = (6, FRONT_Y)
DIBBLE_DOOR = (14, FRONT_Y)
HALL_DOOR = (25, FRONT_Y)
THROSSELL_DOOR = (34, FRONT_Y)

# Mr Dibble's front fence, along row 13 with a gap for his path, and the one
# post you walk into.
FENCE_Y = 13
FENCE_XS = [12, 13, 15, 16]
WET_PAINT = (13, FENCE_Y)

# The duck pond, row by row: (y, x1, x2).
POND = [(17, 6, 10), (18, 5, 11), (19, 4, 12), (20, 5, 11), (21, 6, 10)]
ALLOTMENT = (28, 18, 36, 22)        # x1, y1, x2, y2: Mr Dibble's
VOLCANO = (33, 20)                  # the ring of stones, on the allotment
MAZE = (2, 22, 12, 25)              # x1, y1, x2, y2: one hedge thick
MAZE_GAP = (12, 23)                 # the way in, on the east side
MAZE_WALLS = [(9, 24), (6, 23)]     # so that it is, technically, a maze
MAZE_CENTRE = (3, 24)
MAZE_SIGN = (13, 22)
PLAQUE = (23, 17)                   # read from below
WELL = (25, 21)
OAK = (16, 23)                      # `K.TREE`'s top-left; its trunk is row 24
BRANCH = (17, 24)                   # the trunk cell nearest the road
ROAD_SIGN = (21, 25)
LAMPS = [(3, 16), (17, 16), (28, 16), (37, 16)]

EFFIE_GATE = (7, 13)
COURIER = (18, 17)
EFFIE_VOLCANO = (32, 20)
EFFIE_POND = (12, 18)
EFFIE_POST = (17, 17)
DIBBLE_AT = (17, 13)
THROSSELL_AT = (24, 18)
COBLEY_AT = (13, 19)
PIG = (36, 15)
ARRIVE = (ROAD_X, VH - 2)

CROPS = [K.sf_tile("Outside_B", "Crops %s" % c) for c in "ABCD"]
SCARECROW = K.sf_tile("Outside_B", "Scarecrow")
FIRE_PIT = K.sf_tile("Outside_B", "Rock Fire Pit B")
STUMP = K.sf_tile("Outside_B", "Stump")
PLAQUE_TILE = K.sf_tile("Outside_C", "Monument C")
HAY = K.sf_tile("Outside_B", "Hay")


def pottering_map():
    w, h = VW, VH
    g = K.Canvas(w, h)
    g.fill(0, 0, w - 1, h - 1, 0, K.GRASS)

    # The street, the road in, every doorstep.
    g.fill(2, STREET_Y, w - 3, STREET_Y + 1, 0, K.PATH)
    g.fill(ROAD_X, STREET_Y, ROAD_X + 1, h - 1, 0, K.PATH)
    for x, _ in (GOTOBED_DOOR, DIBBLE_DOOR, HALL_DOOR, THROSSELL_DOOR):
        g.fill(x, FRONT_Y + 1, x, STREET_Y - 1, 0, K.PATH)

    # The duck pond, and the allotment in a square of dug earth (`K.SAND` is
    # the sheet's `Dirt`).
    for y, px1, px2 in POND:
        g.fill(px1, y, px2, y, 0, K.WATER)
    g.fill(*ALLOTMENT, 0, K.SAND)

    # The maze: a ring of hedge one thick, and two walls inside it. `HEDGE`
    # is an overlay, so it goes on layer 1 over the grass.
    mx1, my1, mx2, my2 = MAZE
    for x in range(mx1, mx2 + 1):
        g.set(x, my1, 1, K.HEDGE)
        g.set(x, my2, 1, K.HEDGE)
    for y in range(my1, my2 + 1):
        g.set(mx1, y, 1, K.HEDGE)
        if (mx2, y) != MAZE_GAP:
            g.set(mx2, y, 1, K.HEDGE)
    for xy in MAZE_WALLS:
        g.set(*xy, 1, K.HEDGE)

    for b, wall, roof in [(GOTOBED, K.WALL_PLASTER, K.ROOF_BROWN),
                          (DIBBLE, K.WALL_PLANK, K.ROOF_GREEN),
                          (HALL, K.WALL_BRICK_RED, K.ROOF_GOLD),
                          (THROSSELL, K.WALL_STONE_WHITE, K.ROOF_GREEN)]:
        g.building(*b, wall=wall, roof=roof)

    # Mr Dibble's fence, a wooden overlay on layer 1.
    for x in FENCE_XS:
        g.set(x, FENCE_Y, 1, K.DECKING)
    g.autotile(0)
    g.autotile(1)

    # Fronts. The Gotobeds' door is an event; the rest are shut.
    g.column(DIBBLE_DOOR[0], FRONT_Y - 1, 3, K.DOOR_SHUT)
    g.column(HALL_DOOR[0], FRONT_Y - 1, 3, K.DOOR_DOUBLE)
    g.column(THROSSELL_DOOR[0], FRONT_Y - 1, 3, K.DOOR_SHUT)
    for x in (4, 8, 13, 16, 23, 27, 28, 33, 36):
        g.set(x, FRONT_Y, 3, K.WINDOW)
    g.set(HALL_DOOR[0] - 2, FRONT_Y - 1, 3, K.SIGN_SUN)
    g.set(GOTOBED[0] + 1, GOTOBED[1], 2, K.STOVEPIPE)
    g.set(THROSSELL[0] + 3, THROSSELL[1], 2, K.STOVEPIPE)

    # Front gardens: hollyhocks along every front, Mrs Throssell's best.
    g.scatter([(4, 12), (5, 12), (8, 12), (9, 12), (4, 13), (9, 13)], 3,
              K.FLOWERS2)
    g.scatter([(22, 12), (23, 12), (28, 12), (29, 12)], 3, K.FLOWERS)
    g.scatter([(32, 12), (33, 12), (35, 12), (36, 12), (32, 13), (36, 13)],
              3, K.FLOWERS3)

    # The green: lamps, the plaque, the well, lily pads, flowers, bushes.
    for x, y in LAMPS:
        g.column(x, y - 1, 3, K.LAMP)
    g.set(*PLAQUE, 3, PLAQUE_TILE)
    g.set(*WELL, 3, K.TUB)
    g.set(*ROAD_SIGN, 3, K.SIGNPOST)
    g.set(*MAZE_SIGN, 3, K.FENCE_PANEL)
    g.set(*MAZE_CENTRE, 3, STUMP)
    g.scatter([(6, 18), (9, 20), (10, 18)], 3, K.LILYPAD)
    g.scatter([(15, 18), (26, 17), (16, 21), (22, 22), (27, 24), (14, 17)],
              3, K.FLOWERS3)
    g.scatter([(2, 18), (24, 23), (30, 24), (14, 22)], 3, K.BUSH)

    # The allotment: crops round the edge, the scarecrow, a stook of hay, and
    # the ring of stones in which the volcano has been smouldering since
    # November.
    ax1, ay1, ax2, ay2 = ALLOTMENT
    for i, x in enumerate(range(ax1, ax2 + 1)):
        g.set(x, ay1, 3, CROPS[i % len(CROPS)])
    for i, x in enumerate(range(ax1 + 3, ax2 + 1)):
        g.set(x, ay2, 3, CROPS[(i + 2) % len(CROPS)])
    g.set(ax1 + 1, ay1 + 2, 3, SCARECROW)
    g.set(ax2, ay1 + 2, 3, HAY)
    g.set(*VOLCANO, 3, FIRE_PIT)

    # The oak by the road in, and the wood round everything else.
    g.blit(*OAK, 3, K.TREE)
    for x in range(0, w, 2):
        g.blit(x, 0, 3, K.TREE)
        if not (ROAD_X - 1 <= x <= ROAD_X + 1):
            g.blit(x, h - 2, 3, K.TREE)
    for y in range(2, h - 2, 2):
        if y < FRONT_Y or y > STREET_Y + 2:
            g.blit(0, y, 3, K.TREE)
            g.blit(w - 2, y, 3, K.TREE)
    for x in range(2, w - 2, 2):
        if not any(b[0] - 1 <= x <= b[0] + b[2] for b in
                   (GOTOBED, DIBBLE, HALL, THROSSELL)):
            g.blit(x, 2, 3, K.TREE)
            g.blit(x, 4, 3, K.TREE)
    g.blit(30, 9, 3, K.TREE)
    g.blit(18, 9, 3, K.TREE)

    m = K.new_map(w, h, K.TS_OUTSIDE, name="Much Pottering", bgm="Town1")
    m["data"] = g.data
    m["events"] = [None] + pottering_events()
    return m


def _pair(first, later):
    """A first conversation and the short one after it, on self switch A."""
    return first + [R.self_switch("A", True)], later


def _person(event_id, name, xy, img, first, later, extra=()):
    return R.event(event_id, name, *xy, [
        R.page(first, img=img, trigger=0, priority=1),
        R.page(later, img=img, trigger=0, priority=1,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ] + list(extra))


def _bump(event_id, name, xy, first, later, img=None):
    """A thing you walk into: player-touch at "same as characters", which is
    what makes walking into it, and not standing on it, start it."""
    look = dict(img=img or R.image(""), trigger=1, priority=1,
                direction_fix=True)
    return R.event(event_id, name, *xy, [
        R.page(first + [R.self_switch("A", True)], **look),
        R.page(later, conditions={"selfSwitchValid": True,
                                  "selfSwitchCh": "A"}, **look),
    ])


def effie_pages():
    """Effie at her gate, as anybody finds her: waiting for the post."""
    first = S.say("Effie", ["Are you the post?"])
    first += S.say("Effie", ["You're not the post."])
    first += S.say("Effie", [
        "I'm waiting for a letter from Upper",
        "Clanging. From my pen pal. He's six foot.",
    ])
    first += S.say("Effie", [
        "He drives an airship called the Two",
        "Hundred, and he's the foreman at the works.",
        "He's nine.",
    ])
    first += R.if_then(R.condition_variable(db.VAR_SPA1_POSTED, 3, 1), S.say(
        "Effie", [
            "He's got a dragon now. It's called",
            "Ferrule. It's quite big.",
        ]))
    first += S.say("Effie", [
        "I've told him we've got a volcano.",
        "And a sea serpent, in the pond.",
    ])
    first += S.narrate(["She looks at the pond, and lowers her voice."])
    first += S.say("Effie", ["Don't tell him."])
    later = S.say("Effie", [
        "Still not the post.",
    ]) + S.say("Effie", [
        "He comes about now. The man in the red",
        "coat. He always comes about now.",
    ])
    return _pair(first, later)


def throssell_pages():
    first = S.say("Mrs Throssell", [
        "Good morning! Agatha Throssell,",
        "chair of the parish council. Do mind",
        "the plaque. It's been done.",
    ])
    first += S.say("Mrs Throssell", [
        "We had a Chosen One through,",
        "once. He asked the way to somewhere",
        "else.",
    ])
    first += S.say("Mrs Throssell", [
        "We're twinned with Upper",
        "Clanging. I chose it off the map. As",
        "different as possible, I said, and",
        "there it was.",
    ])
    first += S.say("Mrs Throssell", [
        "Neither of us has ever visited.",
        "It's going beautifully.",
    ])
    first += S.say("Mrs Throssell", [
        "And the children write. One",
        "each. That was my idea as well.",
    ])
    # Spare in the party is a reaction shot, not SPA-4.
    spare = S.narrate([
        "Her eye falls on Spare, and on the bag, and stays there.",
    ]) + S.say("Mrs Throssell", [
        "Is that a Cotterill? From Upper",
        "Clanging? Our first visitor!",
    ]) + S.say("Mrs Throssell", [
        "I shall have to minute it.",
        "'Something arising.'",
    ])
    first += R.if_then(R.condition_actor_in_party(db.SPARE), spare)
    later = S.say("Mrs Throssell", [
        "The minutes of the last meeting:",
        "'Nothing arising.' I wrote that.",
        "I'm rather proud of it.",
    ])
    return _pair(first, later)


def dibble_pages():
    first = S.say("Mr Dibble", [
        "Mind the fence. Wet paint.",
    ])
    first += S.say("Mr Dibble", [
        "I paint it every spring. And every",
        "summer. It is a very good fence.",
    ])
    first += S.say("Mr Dibble", [
        "Young Effie tells everybody my",
        "bonfire is a volcano. It's leaves.",
    ])
    first += S.say("Mr Dibble", [
        "I lit it in November. It's never",
        "gone out. I'm quite proud of that,",
        "if I'm honest.",
    ])
    later = S.say("Mr Dibble", ["Wet paint. Still."])
    return _pair(first, later)


def cobley_pages():
    first = S.say("Mr Cobley", [
        "Morning. Don't splash.",
        "Old Tom's about.",
    ])
    first += S.say("Mr Cobley", [
        "Thirty years I've fished for him.",
        "Biggest carp in the county.",
    ])
    first += S.say("Mr Cobley", [
        "Nobody's ever seen him.",
        "That's how you know he's big.",
    ])
    first += S.say("Mr Cobley", [
        "Young Effie writes to her pen pal",
        "there's a sea serpent in here.",
        "I've never once contradicted her.",
    ])
    first += S.say("Mr Cobley", ["I don't know he isn't."])
    later = S.say("Mr Cobley", ["Not today. He knows I'm here."])
    return _pair(first, later)


def plaque_pages():
    first = S.narrate([
        "A stone on the green, with the lettering picked out in",
        "gold, and polished this morning:",
    ])
    first += S.narrate([
        "THE PARISH OF MUCH POTTERING HAS NEVER BEEN",
        "BURNED DOWN, OVERRUN, FORETOLD, CURSED, CHOSEN,",
        "OR SET UPON BY ANYTHING.",
        "    Erected by the Parish Council, which was not busy.",
    ])
    first += S.narrate([
        "You know the kind of village a story starts in. The",
        "quiet one, the nice one - the one that is on fire by",
        "the end of the first chapter. This one has put up a",
        "stone about it.",
    ]) + [S.trope()]
    later = S.narrate([
        "NEVER BURNED DOWN. Somebody has been at it with a cloth",
        "again.",
    ])
    return _pair(first, later)


def wet_paint():
    first = S.narrate([
        "You walk into Mr Dibble's fence. WET PAINT, says a card",
        "on the post, a moment too late. You are now partly green.",
    ]) + S.say("Mr Dibble", ["That's four today."])
    later = S.narrate([
        "You walk into the fence again. It is still wet. You are",
        "now more green.",
    ]) + S.narrate([
        "Mr Dibble has stopped counting. He has not stopped",
        "painting.",
    ])
    return first, later


def pottering_events():
    evs = []
    # 1-2: the road out, both cells of it, below characters.
    for i in range(2):
        evs.append(S.exit_tile(i + 1, "The Road Out", ROAD_X + i, VH - 1,
                               MAP_WORLD, *POTTERING_STEP))
    # 3: the Gotobeds' front door.
    x1, y1, x2, y2, door_x = PARLOUR
    evs.append(S.door(3, "The Gotobeds' Door", *GOTOBED_DOOR,
                      MAP_POTTERING_IN, door_x, y2 + 1, direction=8))

    # 4: Effie at her gate, and SPA-4's meeting appended to her.
    img = R.image(*S.FACES["Effie"], direction=2)
    evs.append(_person(4, "Effie Gotobed", EFFIE_GATE, img, *effie_pages()))
    evs[-1]["pages"] += q_spare.effie_pages(evs[-1]["pages"][1])    # SPA-4
    # 5-7: where she takes him, and 8: the courier, on his round.
    evs += q_spare.tour_events(5, EFFIE_VOLCANO, EFFIE_POND, EFFIE_POST)
    evs.append(q_spare.pottering_courier(8, *COURIER))              # SPA-4

    # 9-10: Mr Dibble, and his fence.
    evs.append(_person(9, "Mr Dibble", DIBBLE_AT,
                       R.image(*S.FACES["Mr Dibble"], direction=4),
                       *dibble_pages()))
    evs.append(_bump(10, "Wet Paint", WET_PAINT, *wet_paint()))
    # 11-12: Mrs Throssell, and her plaque - the site's trope.
    evs.append(_person(11, "Mrs Throssell", THROSSELL_AT,
                       R.image(*S.FACES["Mrs Throssell"], direction=4),
                       *throssell_pages()))
    page = dict(img=R.image(""), trigger=0, priority=1, direction_fix=True)
    first, later = plaque_pages()
    evs.append(R.event(12, "The Plaque", *PLAQUE, [
        R.page(first, **page),
        R.page(later, conditions={"selfSwitchValid": True,
                                  "selfSwitchCh": "A"}, **page)]))
    # 13: Mr Cobley, at the pond, after one carp.
    evs.append(_person(13, "Mr Cobley", COBLEY_AT,
                       R.image(*S.FACES["Mr Cobley"], direction=4),
                       *cobley_pages()))

    # 14: the pig, asleep across the street.
    evs.append(_bump(14, "The Pig", PIG, S.narrate([
        "There is a pig asleep across the street. You walk into",
        "it. It does not wake up.",
    ]) + S.narrate([
        "Somebody has chalked on the cobbles beside it, neatly:",
        "PIG HAS RIGHT OF WAY.",
    ]), S.narrate([
        "You walk into the pig. The pig has right of way.",
    ]), img=R.image("Nature", 2, direction=4)))
    # 15: the oak by the road in.
    evs.append(_bump(15, "The Oak", BRANCH, S.narrate([
        "There is a sign nailed to the oak at head height. You",
        "read it as you walk into the branch:",
        "",
        "                 MIND THE BRANCH",
    ]), S.narrate([
        "MIND THE BRANCH. You mind it, this time, and walk into",
        "the trunk instead.",
    ])))
    # 16: the wishing well, and two wishes on it once they have met.
    well = S.narrate([
        "A wishing well. You walk into it, which is not how wishes",
        "work.",
    ]) + S.narrate([
        "Tied to the windlass with string is a label, in a child's",
        "capitals: I WISH FOR A VOLCANO. A PROPER ONE. E.G.",
    ])
    evs.append(R.event(16, "The Wishing Well", *WELL, [
        R.page(well, img=R.image(""), trigger=1, priority=1,
               direction_fix=True)]))
    evs[-1]["pages"] += q_spare.well_pages(evs[-1]["pages"][0])     # SPA-4
    # 17-18: the maze.
    evs.append(S.sign(17, "The Maze", *MAZE_SIGN, [
        "THE MUCH POTTERING MAZE.",
        "Planted Tuesday. Please do not step over it.",
    ]))
    centre = S.narrate([
        "The centre of the Much Pottering Maze. There is a stump",
        "to sit on, and a visitors' book in a tin.",
    ]) + S.narrate([
        "Every entry in it is Mr Dibble's. The most recent one",
        "says: Found it again.",
    ])
    evs.append(R.event(18, "The Middle of the Maze", *MAZE_CENTRE,
                       [R.page(centre, **page)]))
    # 19: the sign on the road in.
    evs.append(S.sign(19, "The Road Sign", *ROAD_SIGN, [
        "MUCH POTTERING.  Twinned with Upper Clanging.",
        "Please go slowly. There is no hurry, and there never",
        "has been.",
    ]))
    # 20: the volcano.
    fire = S.narrate([
        "A ring of stones on Mr Dibble's allotment, with a heap of",
        "leaves in it, smouldering gently, the way it has since",
        "November.",
    ])
    evs.append(R.event(20, "The Volcano", *VOLCANO, [R.page(
        fire, img=R.image("!Flame", 0, direction=2), trigger=0, priority=1,
        step_anime=True, direction_fix=True)]))
    return evs


# ================================================================== indoors ==
# The Gotobeds' cottage: one room, the kitchen that is also the parlour.
IW, IH = 12, 12
#           x1 y1 x2 y2 door_x
PARLOUR = (2, 4, 9, 8, 5)

FIREPLACE = K.sf_block("Inside_B", "Fireplace B (Brick)")       # 1x2
DRESSER = K.sf_block("Inside_B", "Dish Cabinet")                # 1x2, on its base
CLOCK = K.sf_block("Inside_B", "Clock")                         # 1x2
CABINET = K.sf_tile("Inside_B", "Cabinet")
TABLE_D = K.sf_tile("Inside_B", "Table D")
CHAIR = K.sf_block("Inside_B", "Chair A (Wood)")                # 1x2, faces south
TEAPOT = K.sf_tile("Inside_C", "Teapot A")
LETTERS = K.sf_tile("Inside_C", "Small Box C")                  # envelopes, sealed
MOUNTAIN = K.sf_tile("Inside_B", "Painting B")                  # a mountain

PAINTING_AT = (4, 3)
CABINET_AT = (9, 4)
TABLE_AT = (5, 6)                   # two cells of `Table D`
MRS_GOTOBED = (7, 6)


def parlour_map():
    x1, y1, x2, y2, door_x = PARLOUR
    g = K.interior(IW, IH, x1, y1, x2, y2, door_x=door_x,
                   floor=K.IN_WOOD_FLOOR, wall_top=K.IN_WALL_TOP_WHITE,
                   wall_face=K.IN_WALL_FACE_WHITE)
    g.fill(4, 6, 7, 8, 1, K.IN_GREEN_RUG)
    g.autotile(1)

    g.column(x1 + 1, y1 - 1, 2, FIREPLACE)
    g.set(*PAINTING_AT, 3, MOUNTAIN)
    g.column(6, y1 - 2, 3, K.IN_WINDOW)
    g.column(7, y1 - 2, 2, CLOCK)             # hung on the wall, not stood
    g.column(8, y1 - 1, 2, DRESSER)
    g.set(*CABINET_AT, 2, CABINET)
    g.set(*CABINET_AT, 3, LETTERS)
    tx, ty = TABLE_AT
    g.set(tx, ty, 2, TABLE_D)
    g.set(tx + 1, ty, 2, TABLE_D)
    g.column(tx, ty - 2, 2, CHAIR)
    g.set(tx + 1, ty, 3, TEAPOT)
    g.set(x1, y2, 3, K.INC_PLANT2)
    g.set(x2, y2, 3, K.INC_PLANT2)

    m = K.new_map(IW, IH, K.TS_INSIDE, name="", bgm="Town1",
                  battleback=("Wood1", "Room1"))
    m["displayName"] = ""
    m["data"] = g.data
    m["events"] = [None] + parlour_events()
    return m


def gotobed_pages():
    first = S.say("Mrs Gotobed", [
        "Hello! You'll be wanting Effie.",
        "She's at the gate. She's always at the",
        "gate, about this time.",
    ])
    first += S.say("Mrs Gotobed", [
        "Waiting for the post. Her pen pal",
        "writes from Upper Clanging. They've",
        "been at it since they were six.",
    ])
    first += S.say("Mrs Gotobed", [
        "He says he drives an airship.",
        "I've never had the heart.",
    ])
    later = S.say("Mrs Gotobed", [
        "She keeps every one of his, on the",
        "cabinet. Don't tell her I said.",
    ])
    return _pair(first, later)


def parlour_events():
    x1, y1, x2, y2, door_x = PARLOUR
    evs = [S.exit_tile(1, "The Front Door", door_x, y2 + 2, MAP_POTTERING,
                       GOTOBED_DOOR[0], GOTOBED_DOOR[1] + 1)]
    evs.append(_person(2, "Mrs Gotobed", MRS_GOTOBED,
                       R.image(*S.FACES["Mrs Gotobed"], direction=4),
                       *gotobed_pages()))
    page = dict(img=R.image(""), trigger=0, priority=1, direction_fix=True)
    box = S.narrate([
        "A box on the cabinet, full of letters, tied up by the year",
        "in string. The writing on the envelopes gets bigger and",
        "worse the further down you go.",
    ])
    box += R.if_then(
        R.condition_variable(db.VAR_SPA1_POSTED, 3, 1),
        S.narrate(["The one on top is fat, and recent, and has a dragon",
                   "drawn on the back."]),
        S.narrate(["The one on top has an airship drawn on the back, with",
                   "somebody very tall at the wheel."]))
    evs.append(R.event(3, "The Letters", *CABINET_AT, [R.page(box, **page)]))
    painting = S.narrate([
        "A painting of a mountain, over the fireplace. Somebody has",
        "added, in crayon, on the glass, a good deal of smoke",
        "coming out of the top.",
    ])
    evs.append(R.event(4, "The Painting", *PAINTING_AT,
                       [R.page(painting, **page)]))
    return evs


# ================================================================ the doors ==
def world_doors(base_id, cells):
    """The real door into Much Pottering, on the world map.

    `cells` is the two squares `worldmap.json` put placeholders on for this
    site, handed in by `journey.world_map`. Player-touch and below
    characters, the world map's idiom for a place you walk into."""
    evs = []
    for i, (x, y) in enumerate(sorted(cells)):
        arrive = S.narrate([
            "A village of thatch and hollyhocks, with a duck pond and a",
            "parish hall and a smell of somebody's bonfire. Nothing",
            "appears to be happening in it, very contentedly.",
        ])
        arrive += R.choice_block(
            ["Go in", "Press on"],
            [[R.transfer(MAP_POTTERING, *ARRIVE, 8, 0)],
             S.narrate(["You press on. Behind you, a pig turns over in its",
                        "sleep."])])
        evs.append(R.event(base_id + i, "Much Pottering", x, y, [R.page(
            arrive, img=R.image(""), trigger=1, priority=0, through=True)]))
    return evs


def build():
    R.save_map(MAP_POTTERING, pottering_map())
    R.save_map(MAP_POTTERING_IN, parlour_map())
