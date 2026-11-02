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
import handdrawn as HD
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
ROAD_X = 19                         # the road in from the south: 19 and 20
GOTOBED_DOOR = (6, FRONT_Y)

# Mr Dibble's front fence, along row 13 with a gap for his path, and the one
# post you walk into.
FENCE_Y = 13
WET_PAINT = (13, FENCE_Y)

VOLCANO = (33, 20)                  # the ring of stones, on the allotment
MAZE_CENTRE = (3, 24)
MAZE_SIGN = (13, 22)
PLAQUE = (23, 17)                   # read from below
WELL = (25, 21)
BRANCH = (17, 24)                   # the oak's trunk cell nearest the road
ROAD_SIGN = (21, 25)

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


def pottering_map():
    """A village of four houses on a green, with a duck pond, a hedge maze one
    hedge thick and Mr Dibble's allotment. Drawn by hand in the editor and
    kept by `handdrawn.py` (Mike, October 2026), from the generated village:
    the ground in the Dirt-edged kinds so the street blends into the green,
    the street and the doorsteps two wide, lamps with their feet, and the
    Gotobeds' cottage a storey taller, which is where its upstairs is. Only
    the events are built here."""
    w, h = VW, VH
    data = HD.load(MAP_POTTERING, w, h, K.TS_OUTSIDE)
    m = K.new_map(w, h, K.TS_OUTSIDE, name="Much Pottering", bgm="Town1")
    m["data"] = data
    m["events"] = [None] + pottering_events()
    m["events"] += shut_doors(len(m["events"]))
    return m


def shut_doors(first_id):
    """Three of the four front doors, which do not open, and say why. They
    were shutters until October 2026, and read as windows (`story.shut`);
    appended after the volcano, so no id above moved."""
    dibble = S.narrate([
        "Mr Dibble's front door. A card on it says WET PAINT, and",
        "the door is locked as well, which in Much Pottering is",
        "very nearly an event."])
    dibble += S.narrate([
        "Nothing has ever happened here. Mr Dibble would like it",
        "to stay that way, and so would his hall carpet."])
    motto = S.narrate([
        "Locked. A card in the window, done in poker-work:",
        "'NOBODY HOME. NOTHING HAPPENING. NO QUESTS.'"])
    motto += S.narrate([
        "It is the village motto, more or less. Heroes knock",
        "anyway, in case. Heroes always knock in case."])
    pig = S.narrate([
        "Shut. A sign on it says the pig has right of way.",
        "It does not say you have."])
    pig += S.narrate([
        "Somebody inside is having a quiet afternoon. You can",
        "hear it from here: a clock, a kettle, and nothing",
        "whatever happening."])
    return [S.shut_door(first_id + i, name, x, FRONT_Y, cmds)
            for i, (name, x, cmds) in enumerate([
                ("Mr Dibble's Door", 14, dibble),
                ("A Door With a Motto", 25, motto),
                ("The Pig's Door", 34, pig)])]


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
# The Gotobeds' cottage: the kitchen that is also the parlour, and since Mike
# put a storey on it (October 2026) the bedrooms over it, drawn beside it on
# the same map. Drawn by hand in the editor and kept by `handdrawn.py`.
IW, IH = 36, 16
#           x1 y1 x2 y2 door_x
PARLOUR = (2, 4, 9, 9, 5)
# The flight up in the parlour's north-west corner, and the one step down at
# the head of it upstairs: (x, top tread, bottom tread).
STAIRS_UP = (2, 4, 5)
STAIRS_DOWN = (26, 4, 5)            # (26, 4) is the landing, (26, 5) the step

PAINTING_AT = (4, 3)
CABINET_AT = (9, 4)
MRS_GOTOBED = (7, 7)


def parlour_map():
    data = HD.load(MAP_POTTERING_IN, IW, IH, K.TS_INSIDE)
    m = K.new_map(IW, IH, K.TS_INSIDE, name="", bgm="Town1",
                  battleback=("Wood1", "Room1"))
    m["displayName"] = ""
    m["data"] = data
    m["events"] = [None] + parlour_events()
    return m


def parlour_stairs(first_id):
    """Up is the top tread of the parlour's flight, to the landing upstairs,
    facing up; down is the step at the head of the stairs, back to the bottom
    tread of the parlour's flight, facing down. Turning round on the stairs
    takes you straight back, as in the Lighthouse."""
    x, top, foot = STAIRS_UP
    ux, landing, step = STAIRS_DOWN
    go = dict(img=R.image(""), trigger=1, priority=0, through=True)
    return [
        R.event(first_id, "The Stairs Up", x, top, [R.page(
            [R.play_se("Move1"),
             R.transfer(MAP_POTTERING_IN, ux, landing, 8, 0)], **go)]),
        R.event(first_id + 1, "The Stairs Down", ux, step, [R.page(
            [R.play_se("Move1"),
             R.transfer(MAP_POTTERING_IN, x, foot, 2, 0)], **go)]),
    ]


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
        "A painting of a mountain, by the fireplace. Somebody has",
        "added, in crayon, on the glass, a good deal of smoke",
        "coming out of the top.",
    ])
    evs.append(R.event(4, "The Painting", *PAINTING_AT,
                       [R.page(painting, **page)]))
    evs += parlour_stairs(5)
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
