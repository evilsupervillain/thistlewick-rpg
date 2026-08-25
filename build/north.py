"""Upper Clanging and its four interiors: Maps 21-25.

    21  Upper Clanging          one street up a hill, in the rain
    22  The Hoyle Works         the shed, the drawing office, and the Two Hundred
    23  The Safety Valve        the inn
    24  Ollerenshaw's           the forge
    25  The Parish Rooms        the register, the census, and the counter

The third answer to the Prophecy and the only cheerful one. Thistlewick
believes it, Nether Sopping has been discarded by it, and Upper Clanging
intends to *solve* it - with infrastructure, on an industrial scale, at the
fourth generation of trying. `NORTH.md` sections 4 and 5 are the design and
section 1 is the specification for every line anybody up here says.

The town is furnished and cast. What is *not* here is the Two Hundred itself
(section 5), the Long Field and the crag (`field.py`, section 6), and the
retrofit (section 3) - and none of them needs a line of this file rewritten,
because everything anybody says here is either a new event or a page that a
later switch can be appended after. That is rule 1.7 and it is the reason Ott
has five pages and a spare condition rather than one page that will have to be
edited when the airship quest arrives.

On the humour: section 1 of `NORTH.md` is the specification, not the flavour
text. The short version is that the comedy is embarrassment and never
resentment, that every line has to be defensible as literal, and that the game
never says the thing - the player's head says it. `story.blush()` counts the
moments where it does, and the count is the joke.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import db
import mapkit as K
import rmmzdata as R
import story as S
from places import (MAP_CLANGING, MAP_WORKS, MAP_VALVE, MAP_FORGE, MAP_PARISH,
                    MAP_WORLD, CLANGING_GATE, WORLD_CLANGING_STEP,
                    WORLD_AIRSHIP)
# Not forked: `talker` builds the two-pages-and-a-free-third shape that most of
# this town wants, and its third page is what NORTH.md 1.7 calls pattern two.
from south import talker
# The Long Field's payoff and the crag's are written where the Long Field and
# the crag are (`NORTH.md` 11), and appended here: three further pages on Ott
# and one new readable thing in the works. Nothing below is edited to take
# them - that is what `ladder(..., pages=)` is for.
import field

TOWN_W, TOWN_H = 34, 44

# The street runs straight up the hill, and the hill is the point: three
# terraces, each one a two-row brick retaining wall above the last, with a
# flight of iron steps cut through it where the road goes. The bands are given
# as the first of their two face rows.
HILL_WALL = 1                       # the hillside the town is cut into
STEP_UPPER, STEP_LOWER = 17, 32     # the two retaining walls in the street

STREET_X1, STREET_X2 = 15, 19       # the road, five tiles across
STAIR_X = 16                        # the flights are three of those five

# Buildings: (x, y, w, h), and how many of those rows are wall rather than
# roof. `Canvas.building` puts the wall rows along the bottom and returns the
# row the door goes on.
#
# Wall rows are worth having. An SF roof is a flat pale grey slab with an
# orange lip round it, so a building with more roof than wall reads as a car
# park seen from above; the walls are brick and corrugated iron and carry all
# the texture there is. Everything up here is therefore drawn shallow - three
# rows of roof at most - and given its height in storeys of wall instead.
WORKS, WORKS_ROWS = (12, 6, 12, 8), 5          # the Hoyle Works, across the top
TOWER = (7, 7, 3, 7)                           # the Clock Tower, beside it
BOILER_HOUSE, BOILER_ROWS = (25, 4, 7, 6), 3   # no door: the works' own boiler
FORGE, FORGE_ROWS = (3, 21, 9, 7), 4           # Ollerenshaw's
VALVE, VALVE_ROWS = (21, 20, 10, 7), 4         # the Safety Valve
PARISH, PARISH_ROWS = (20, 34, 10, 6), 3       # the Parish Rooms
SHED_WEST, SHED_WEST_ROWS = (3, 35, 7, 5), 2   # no door
SHED_EAST, SHED_EAST_ROWS = (10, 36, 5, 4), 2  # no door
STORES, STORES_ROWS = (1, 4, 5, 5), 2          # no door: the works' stores

# The works stands across the head of the street with its door on the centre
# line of it, so that what you see coming up the hill is the thing the town is
# for, with the clock standing beside it.
WORKS_DOOR = (17, WORKS[1] + WORKS[3] - 1)
FORGE_DOOR = (7, FORGE[1] + FORGE[3] - 1)
VALVE_DOOR = (25, VALVE[1] + VALVE[3] - 1)
PARISH_DOOR = (24, PARISH[1] + PARISH[3] - 1)

# The tile you are put back on when you come out of each door.
OUT = {m: (d[0], d[1] + 1) for m, d in [
    (MAP_WORKS, WORKS_DOOR), (MAP_FORGE, FORGE_DOOR),
    (MAP_VALVE, VALVE_DOOR), (MAP_PARISH, PARISH_DOOR)]}

# The three doors nobody can get through, on the bottom row of their building.
SHUT_DOORS = [(6, SHED_WEST[1] + SHED_WEST[3] - 1),
              (12, SHED_EAST[1] + SHED_EAST[3] - 1),
              (28, BOILER_HOUSE[1] + BOILER_HOUSE[3] - 1)]


# ------------------------------------------------------------------ rain ----
# `NORTH.md` 14: Upper Clanging has rain, and rain is one event command.
#
# The bookkeeping is the cost, not the weather. Weather lives on `$gameScreen`,
# which is cleared on a new game and *nowhere else*, so it survives a transfer:
# rain started up here is still falling in Thistlewick, and indoors, until
# something turns it off. So there is exactly one place it goes on - the map's
# own autorun, which also means a screenshot warped straight in gets the
# weather - and every way out of the town turns it off again.
RAIN_POWER = 4


def rain(indent=0):
    return R.set_weather("rain", power=RAIN_POWER, duration=1, indent=indent)


def dry(indent=0):
    return R.set_weather("none", duration=1, indent=indent)


def weather_event(event_id):
    """Autorun, once per arrival, then erase itself.

    Erasing rather than latching a self switch is deliberate: an erased event
    comes back the next time the map is loaded and a self switch would not, so
    with a switch it would rain on the first visit only."""
    return R.event(event_id, "The Weather", 0, 0, [R.page(
        [rain(), R.erase_event()],
        img=R.image(), trigger=3, priority=0, through=True)])


def door(event_id, name, x, y, target_map, tx, ty, direction=2):
    """A door into somewhere with a roof on it - so it stops raining.

    The drying is in the helper rather than in each event because forgetting
    it once is enough to send the player home with the weather still running,
    and nothing in the data would show it."""
    cmds = S.door_page(target_map, tx, ty, direction)
    cmds.insert(len(cmds) - 1, dry())       # after the walk, before the fade
    return R.event(event_id, name, x, y, [R.page(
        cmds, img=R.image("!Door1", 0, direction=2), trigger=1, priority=1)])


def ladder(event_id, name, x, y, speaker, beats, sheet=None, index=None,
           direction=2, move_type=0, pages=None):
    """Somebody with several things to say, one per conversation, in order.

    A page condition can name exactly **one** self switch, so "A and B" is not
    expressible - but `Game_Event.refresh` takes the *last* page whose
    condition holds, so a chain works instead: page one is unconditional and
    sets A, page two needs A and sets B, page three needs B and sets C. With A
    and B both on, pages one, two and three all qualify and three wins.

    Four self switches means five beats, and the last one repeats for the rest
    of the game - so write the last beat as something worth hearing twice.

    This exists for `NORTH.md` 4.7: Ott's steam vocabulary has to land **at
    intervals**, because the moment it becomes The Bit it stops being a repair
    and starts being a routine. One beat per visit is the interval."""
    if len(beats) > 5:
        raise ValueError("%s has %d beats and there are only four self "
                         "switches to chain them with" % (name, len(beats)))
    if sheet is None:
        sheet, index = S.FACES[speaker]
    img = R.image(sheet, index, direction=direction)
    out = []
    for i, beat in enumerate(beats):
        cmds = list(beat)
        if i + 1 < len(beats):
            cmds.append(R.self_switch("ABCD"[i], True))
        out.append(R.page(
            cmds, img=img, trigger=0, priority=1, move_type=move_type,
            conditions=None if i == 0 else
            {"selfSwitchValid": True, "selfSwitchCh": "ABCD"[i - 1]}))
    return R.event(event_id, name, x, y, out + list(pages or []))


def archway(event_id, name, x, y, target_map, tx, ty, direction=2):
    """A way in with no door on it - the works, whose opening is sized for an
    airship and would look silly with a cottage door leaf across it.

    The arch is drawn on the wall as scenery; the event carries no sprite of
    its own, because a door sprite is an event image and would simply be drawn
    over the hole. "Same as characters" is what makes it work: the arch tile is
    passable, so the event is the only thing stopping the player walking into
    the building, and player-touch fires on the bump."""
    return R.event(event_id, name, x, y, [R.page(
        [R.play_se("Move1"), dry(),
         R.transfer(target_map, tx, ty, direction, 0)],
        img=R.image(""), trigger=1, priority=1)])


# ============================================================ Upper Clanging ==
def clanging_map():
    """One street, three terraces, and a clock tower closing the top of it.

    Drawn from the bottom up: ground, then the retaining walls the town is cut
    into, then the buildings, then everything that stands in the street.
    Buildings go on before `autotile(0)` so that their A3 walls take their
    shapes in the same pass as the retaining walls do."""
    g = K.Canvas(TOWN_W, TOWN_H, tileset=K.TS_CLANGING)
    g.fill(0, 0, TOWN_W - 1, TOWN_H - 1, 0, K.GRASS)

    # -- the ground. One paving for the whole town and cobbles for the road,
    # and that is the lot: the SF A5 set has a dozen surfaces and putting four
    # of them in one view turns a street into a swatch card. Grass survives
    # round the edges, which is what stops the place reading as a car park.
    g.fill(1, 3, 32, 16, 0, K.SF_CONCRETE)        # the works terrace
    g.fill(2, 19, 31, 31, 0, K.SF_CONCRETE)       # the town proper
    g.fill(3, 34, 30, 41, 0, K.SF_CONCRETE)       # the bottom of the hill
    # The street stops at the works' front door, which is where it is going,
    # and runs off the bottom of the map, which is where it came from. The
    # paving stops a row short of the edge so that the town ends in a road
    # through grass rather than in a straight line ruled across a lawn.
    g.fill(STREET_X1, WORKS_DOOR[1] + 1, STREET_X2, TOWN_H - 1, 0, K.SF_COBBLE_A)

    # -- the hill. Two rows of brick, three times: once for the hillside the
    # town is cut into, and once under each of the two upper terraces. The
    # street climbs each of them by a three-tile flight of iron steps, and the
    # stair tiles are flagged 0x602 / 0x604 - blocked left, blocked right - so
    # a flight is a channel and nobody walks off the side of it.
    for band in (HILL_WALL, STEP_UPPER, STEP_LOWER):
        g.fill(0, band, TOWN_W - 1, band + 1, 0, K.SF_WALL_BRICK)
    for band in (STEP_UPPER, STEP_LOWER):
        for row in (band, band + 1):
            for i in range(3):
                g.set(STAIR_X + i, row, 0, K.SF_STAIRS_METAL[i])

    # -- the buildings. `crest` first, every time: the top row of an SF roof is
    # a star tile, drawn over the player and ignored for collision, so without
    # something solid underneath it the ridge of every building in town is a
    # tile you can stand on and disappear behind.
    def put(box, rows, wall):
        x, y, w, h = box
        g.crest(x, y, w, wall)
        return g.building(x, y, w, h, wall=wall, roof=K.SF_ROOF, wall_rows=rows)

    put(WORKS, WORKS_ROWS, K.SF_WALL_BRICK)
    put(BOILER_HOUSE, BOILER_ROWS, K.SF_WALL_FACTORY)
    put(STORES, STORES_ROWS, K.SF_WALL_RUST)
    put(FORGE, FORGE_ROWS, K.SF_WALL_RUST)
    put(VALVE, VALVE_ROWS, K.SF_WALL_MORTAR)
    put(PARISH, PARISH_ROWS, K.SF_WALL_STONE)
    put(SHED_WEST, SHED_WEST_ROWS, K.SF_WALL_WOOD)
    put(SHED_EAST, SHED_EAST_ROWS, K.SF_WALL_BARRACKS_A)

    # The Clock Tower is the one civic building, and is not a nine-slice: cap,
    # clock face, then as much brick shaft as the street needs.
    g.clock_tower(TOWER[0], TOWER[1], h=TOWER[3])

    g.autotile(0)

    # -- chimneys, along every ridge. On this sheet they are not star tiles, so
    # they go on layer 3 and push the roof tile they stand on down to layer 2;
    # `Canvas.chimney` does that. The boiler house gets the tall pair.
    for x, y, stack in [(14, 7, K.SF_CHIMNEY_A), (17, 7, K.SF_CHIMNEY_C),
                        (20, 7, K.SF_CHIMNEY_A), (22, 8, K.SF_CHIMNEY_B),
                        (27, 5, K.SF_CHIMNEY_C), (29, 5, K.SF_CHIMNEY_C),
                        (3, 5, K.SF_CHIMNEY_B),
                        (5, 22, K.SF_CHIMNEY_C), (9, 22, K.SF_CHIMNEY_A),
                        (23, 21, K.SF_CHIMNEY_B), (28, 21, K.SF_CHIMNEY_A),
                        (22, 35, K.SF_CHIMNEY_B), (27, 35, K.SF_CHIMNEY_A),
                        (5, 36, K.SF_CHIMNEY_A), (12, 37, K.SF_CHIMNEY_B)]:
        g.chimney(x, y, stack)

    # -- the fronts. A door in the middle, a plate either side of it, windows
    # out towards the corners and along the upper storey. The works gets an
    # arch rather than a door leaf, because what is meant to go in and out of
    # it is an airship.
    g.set(WORKS_DOOR[0], WORKS_DOOR[1], 3, K.SF_ENTRANCE_B)
    g.set(WORKS_DOOR[0] - 3, WORKS_DOOR[1], 3, K.SF_SIGN_BLANK)
    g.set(WORKS_DOOR[0] + 3, WORKS_DOOR[1], 3, K.SF_WARNING_PLATE)
    for x in (13, 15, 19, 22):
        g.column(x, WORKS[1] + 3, 3, K.SF_WINDOW_TALL)
    for x in (13, 22):
        g.set(x, WORKS_DOOR[1] - 1, 3, K.SF_WINDOW)
    g.set(12, WORKS_DOOR[1], 3, K.SF_EXHAUST_WALL)
    g.set(23, WORKS_DOOR[1], 3, K.SF_EXHAUST_WALL)

    g.set(FORGE_DOOR[0] - 2, FORGE_DOOR[1], 3, K.SF_SIGN_WEAPON)
    g.set(FORGE_DOOR[0] + 2, FORGE_DOOR[1], 3, K.SF_SIGN_ARMOR)
    for x in (4, 10):
        g.column(x, FORGE[1] + 3, 3, K.SF_WINDOW_TALL)
    g.set(3, FORGE_DOOR[1], 3, K.SF_EXHAUST_WALL)
    g.set(11, FORGE_DOOR[1], 3, K.SF_EXHAUST_WALL)

    g.column(VALVE_DOOR[0], VALVE_DOOR[1] - 1, 3, K.SF_CANOPY)
    g.set(VALVE_DOOR[0] - 2, VALVE_DOOR[1], 3, K.SF_SIGN_INN)
    g.set(VALVE_DOOR[0] + 2, VALVE_DOOR[1], 3, K.SF_SIGN_CAFE)
    for x in (22, 24, 27, 29):
        g.column(x, VALVE[1] + 3, 3, K.SF_WINDOW_TALL)

    g.set(PARISH_DOOR[0] - 2, PARISH_DOOR[1], 3, K.SF_SIGN_BLANK)
    g.set(PARISH_DOOR[0] + 2, PARISH_DOOR[1], 3, K.SF_SIGN_ITEM)
    g.set(PARISH_DOOR[0] - 3, PARISH_DOOR[1], 3, K.SF_WALL_POSTER)
    for x in (21, 27, 28):
        g.set(x, PARISH_DOOR[1] - 1, 3, K.SF_WINDOW)

    # The three doors that do not open get a shutter rather than a black
    # rectangle: a bare dark tile on a wall reads as a hole the tiler forgot.
    for x, y in SHUT_DOORS:
        g.set(x, y, 3, K.SF_SHUTTER)
    for x, y in [(4, 39), (8, 39), (10, 39), (14, 39), (26, 9), (30, 9),
                 (2, 8), (4, 8)]:
        g.set(x, y, 3, K.SF_WINDOW_LOUVRE)

    # -- the works yard: east of the building, and the strip behind it that
    # runs up against the hill.
    g.column(26, 10, 3, K.SF_WATER_TANK)
    g.column(29, 10, 3, K.SF_WATER_TANK)
    g.column(33, 10, 3, K.SF_PILLAR_BRICK)
    g.blit(30, 13, 3, (K.SF_METAL_FENCE,))
    g.column(25, 14, 3, K.SF_STACKED_CRATES)
    g.scatter([(25, 12), (27, 12), (31, 12), (24, 16), (33, 15)], 3, K.SF_OIL_DRUM)
    g.scatter([(28, 12), (32, 12), (30, 16), (24, 4)], 3, K.SF_CRATE)
    g.set(27, 15, 3, K.SF_SMALL_FUEL_TANK)
    g.set(32, 15, 3, K.SF_OIL_DRUM_LEAK)
    g.set(28, 16, 3, K.SF_DUMPSTER)
    g.scatter([(15, 3), (20, 3), (11, 3)], 3, K.SF_CRATE)
    g.scatter([(18, 3), (23, 3)], 3, K.SF_BARREL)

    # -- west of the clock tower, where the works keeps what it is not using.
    g.column(2, 11, 3, K.SF_STACKED_CRATES)
    g.scatter([(4, 13), (1, 15), (5, 10)], 3, K.SF_OIL_DRUM)
    g.scatter([(5, 13), (1, 10), (6, 15)], 3, K.SF_CRATE)
    g.set(3, 10, 3, K.SF_OIL_DRUM_LEAK)
    g.set(11, 15, 3, K.SF_PUMP)
    g.set(24, 15, 3, K.SF_BARREL)

    # -- the street. Furniture on the flat bits, nothing in the flights.
    g.blit(13, 29, 3, (K.SF_BENCH,))
    g.blit(21, 29, 3, (K.SF_BENCH,))
    g.set(12, 28, 3, K.SF_POSTBOX)
    g.scatter([(13, 20), (14, 24), (20, 22), (31, 28), (2, 28)], 3, K.SF_BARREL)
    g.scatter([(12, 21), (20, 25), (31, 21), (2, 21)], 3, K.SF_CRATE)
    g.column(13, 24, 3, K.SF_STACKED_CRATES)
    g.set(31, 19, 3, K.SF_OIL_DRUM)
    g.set(2, 31, 3, K.SF_OIL_DRUM_LEAK)
    g.set(30, 31, 3, K.SF_DUMPSTER)

    g.column(CLANGING_GATE[0] - 1, 40, 3, K.SF_SIGN_POST)   # the town sign
    g.scatter([(20, 41), (13, 41), (31, 38), (2, 38)], 3, K.SF_BARREL)
    g.scatter([(30, 34), (31, 41), (2, 34)], 3, K.SF_CRATE)
    g.set(30, 36, 3, K.SF_DUMPSTER)
    g.blit(31, 39, 3, (K.SF_BENCH,))

    # -- the weeds. Nothing grows in Upper Clanging on purpose, which is the
    # only reason anything grows in it at all.
    g.scatter([(1, 20), (32, 24), (1, 30), (32, 34), (1, 41), (32, 20),
               (2, 16), (33, 16), (11, 31), (22, 31)], 3, K.SF_WEEDS)
    g.scatter([(1, 25), (32, 30), (1, 35), (32, 42), (10, 3), (33, 3)],
              3, K.SF_WEEDS_B)
    g.scatter([(0, 19), (33, 19), (0, 34), (33, 31), (0, 3), (6, 16),
               (26, 19), (9, 34), (12, 42), (23, 42), (8, 42), (27, 42)],
              3, K.SF_RUBBLE)
    g.scatter([(10, 42), (25, 42), (5, 42), (30, 42), (14, 43), (20, 43)],
              3, K.SF_WEEDS)

    m = K.new_map(TOWN_W, TOWN_H, K.TS_CLANGING, name="Upper Clanging",
                  bgm="Town8")
    m["data"] = g.data
    m["events"] = [None] + clanging_events()
    return m


def clanging_events():
    evs = [weather_event(1)]

    # -- 2: the road south, and the only place the rain is turned off outdoors
    out = S.narrate([
        "The road south, off the hill and out from",
        "under the chimneys. It is drier down there,",
        "and everybody up here knows it, and nobody",
        "up here has ever mentioned it."])
    out += R.choice_block(
        ["Go on", "Stay"],
        [[dry(), R.play_se("Move1"),
          R.transfer(MAP_WORLD, WORLD_CLANGING_STEP[0],
                     WORLD_CLANGING_STEP[1], 2, 0)], []])
    evs.append(R.event(2, "South Road", CLANGING_GATE[0], CLANGING_GATE[1],
                       [R.page(out, img=R.image(""), trigger=1, priority=0,
                               through=True)]))

    # -- 3: the sign. The format is Nether Sopping's; the post it is on is a
    # works hazard plate, because it is the only free-standing sign the north
    # owns and repurposing one is exactly what this town would do.
    evs.append(S.sign(3, "Town Sign", CLANGING_GATE[0] - 1, 41, [
        "A works hazard plate on a post, repainted:",
        "\\C[6]UPPER CLANGING\\C[0]",
        "'IT WILL BE QUIETER SOON'"]))

    # -- 4-7: the four doors
    evs.append(archway(4, "Works Door", WORKS_DOOR[0], WORKS_DOOR[1],
                       MAP_WORKS, *arrival(MAP_WORKS)))
    evs.append(door(5, "Forge Door", FORGE_DOOR[0], FORGE_DOOR[1],
                    MAP_FORGE, *arrival(MAP_FORGE)))
    evs.append(door(6, "Safety Valve Door", VALVE_DOOR[0], VALVE_DOOR[1],
                    MAP_VALVE, *arrival(MAP_VALVE)))
    evs.append(door(7, "Parish Rooms Door", PARISH_DOOR[0], PARISH_DOOR[1],
                    MAP_PARISH, *arrival(MAP_PARISH)))

    # -- 8: the clock. Upper Clanging's one civic building, and its temperament
    # in four lines: a fault everybody knows about, nobody corrects, and the
    # town has organised itself around instead.
    evs.append(S.sign(8, "The Clock", TOWER[0] + 1, TOWER[1] + TOWER[3], [
        "The clock has been four minutes fast since",
        "eighteen forty-one.",
        "The town sets its watches by it and is",
        "therefore four minutes early for everything,",
        "and has been for sixty years, and gets a",
        "great deal done."]))

    # -- 9: the parish notices, on the poster beside the Parish Rooms door
    evs.append(S.sign(9, "Parish Notices", PARISH_DOOR[0] - 3,
                      PARISH_DOOR[1], [
        "\\C[6]UPPER CLANGING PARISH NOTICES\\C[0]",
        "The hooter will sound at six, as usual.",
        "The hooter will sound at six on Sunday",
        "as well.",
        "The parish has been asked about this.",
        "The parish has considered it."]))

    # -- 10: Old Sowerby, on the bench. He is the town's memory and he is
    # entirely cheerful about what he remembers, which is the north in one
    # man - see 4.1. No blush: this is the other register and it is doing
    # different work.
    evs.append(talker(
        10, "Old Sowerby", 14, 30, "Sowerby",
        S.say("Sowerby", [
            "Sixty years I gave that works.",
            "Started on the rivets.",
            "Finished on the rivets.",
        ]) + S.say("Sowerby", [
            "I have seen a hundred and ninety-nine",
            "of them go up.",
            "I have seen the same number come down.",
        ]) + S.say("Sowerby", [
            "Never in a hurry about it, mind.",
            "They come down like a man sitting.",
        ]) + S.say("Sowerby", [
            "It is the coming down that wants the",
            "work. She will get to it.",
        ]),
        S.say("Sowerby", [
            "Rivets. You cannot beat a rivet.",
        ]), direction=2))

    # -- 11-13: the Cotterills. A foundry family, every child named after a
    # fastener, and the joke is never the family - it is Bram's face, and the
    # player's. Mrs Cotterill is **proud**. She is not complaining and she is
    # not confessing; she is answering a polite question from a polite young
    # man, which is 1.4 exactly.
    evs.append(talker(
        11, "Mrs Cotterill", 12, 40, "Mrs Cotterill",
        S.say("Mrs Cotterill", [
            "These are ours.",
        ]) + S.narrate([
            "You ask whether all of them are.",
        ]) + S.say("Mrs Cotterill", [
            "Nine. And one in the oven.",
        ]) + S.say("Mrs Cotterill", [
            "Mr Cotterill is on nights.",
            "He is always very glad to get home.",
        ]) + [S.blush()] + S.narrate([
            "You ask about the names instead.",
        ]) + S.say("Mrs Cotterill", [
            "Cotter, Rivet, Gudgeon, Tappet,",
            "Ferrule, Grommet, Clevis, Shim.",
        ]) + S.say("Mrs Cotterill", [
            "And Spare.",
        ]) + S.say("Mrs Cotterill", [
            "We had run out.",
            "He said call it Spare, and I was tired.",
        ]),
        S.say("Mrs Cotterill", [
            "Ten in the spring.",
            "Mr Cotterill is very pleased.",
        ]),
        extra=[R.control_switch(db.SW_COTTERILL, True)], direction=4))

    # Mr Cotterill is the reaction shot and deliberately does **not** bump the
    # counter: it is one joke, told three times by three people, and counting
    # it three times would be the game explaining it. See 1.5's fourth test.
    evs.append(talker(
        12, "Mr Cotterill", 10, 41, "Mr Cotterill",
        S.say("Mr Cotterill", [
            "Nights.",
            "Twelve on, twelve off, six days.",
        ]) + S.say("Mr Cotterill", [
            "It is not the work I mind.",
            "It is the walk home in the dark.",
        ]) + S.narrate([
            "He thinks about that for a moment.",
        ]) + S.say("Mr Cotterill", [
            "Mind, I have never once minded",
            "the walk home.",
        ]),
        S.say("Mr Cotterill", [
            "Six o'clock. Every day.",
            "Sunday and all.",
        ]), direction=8))

    # Spare Cotterill, aged nine, with a packed bag. Four beats, in this order
    # on purpose: the last one is the one that repeats for the rest of the
    # game, and it should be the running gag rather than either of the two
    # things he reports without understanding them. **Never let him work it
    # out** - he asks the correct question, is answered with a bun, and is
    # entirely satisfied.
    evs.append(ladder(13, "Spare Cotterill", 14, 40, "Spare", [
        S.say("Spare", [
            "Are you the Chosen One?",
        ]) + S.narrate([
            "You admit that you are.",
        ]) + S.say("Spare", [
            "I have a bag. It is packed.",
            "It has been packed for two years.",
        ]) + S.say("Spare", [
            "I am nine. I am nine in a useful way.",
        ]) + S.narrate([
            "You explain that he cannot come.",
            "He takes it extremely well.",
            "He does not put the bag down.",
        ]) + [R.control_switch(db.SW_SPARE_ASKED, True)],

        S.say("Spare", [
            "We are not to knock on Sunday mornings.",
        ]) + S.say("Spare", [
            "Da says Sunday mornings is why",
            "there is ten of us.",
        ]) + S.narrate([
            "Mrs Cotterill has gone the colour of the forge.",
        ]) + [S.blush()],

        S.say("Spare", [
            "Da calls Mam the Two Hundred.",
        ]) + S.narrate([
            "You ask whether that is the airship.",
        ]) + S.say("Spare", [
            "No. He says she is the one that is",
            "finally going to work.",
        ]) + S.narrate([
            "Mr Cotterill has remembered an errand",
            "at the other end of the street.",
        ]) + [S.blush()],

        S.say("Spare", [
            "Can I come yet?",
        ]) + S.narrate([
            "The bag is still packed.",
        ]),
    ], direction=8))
    return evs


# ================================================================ interiors ==
ROOMS = {
    #                w   h  x1  y1  x2  y2  door_x
    MAP_WORKS:      (25, 22, 3, 4, 21, 16, 12),
    MAP_VALVE:      (21, 18, 3, 4, 17, 12, 10),
    MAP_FORGE:      (19, 17, 3, 4, 15, 11, 9),
    MAP_PARISH:     (19, 16, 3, 4, 15, 10, 9),
}


def arrival(map_id):
    _, _, _, _, _, y2, door_x = ROOMS[map_id]
    return door_x, y2


def threshold(map_id):
    _, _, _, _, _, y2, door_x = ROOMS[map_id]
    return door_x, y2 + 2


def room(map_id, **kw):
    """A northern room. Tileset 6's A1 and A2 are the ordinary Inside ones and
    its A5 is the street's own, so only the walls are new - and the doorstep
    has to be given, because `interior`'s default is Inside_A5's wooden step
    and on this sheet that cell is a slab of demonic ground."""
    w, h, x1, y1, x2, y2, door_x = ROOMS[map_id]
    kw.setdefault("threshold", K.SF_THRESHOLD)
    kw.setdefault("outside", K.SF_THRESHOLD)
    return K.interior(w, h, x1, y1, x2, y2, door_x=door_x,
                      tileset=K.TS_CLANGING_IN, **kw)


def finish(map_id, g, name, bgm, battleback, events):
    w, h = ROOMS[map_id][0], ROOMS[map_id][1]
    m = K.new_map(w, h, K.TS_CLANGING_IN, name=name, bgm=bgm,
                  battleback=battleback)
    m["data"] = g.data
    m["events"] = [None] + events
    return m


def way_out(map_id, name):
    """Back into the weather. The town's own autorun starts the rain again, so
    this only has to be a door."""
    return S.exit_tile(1, name, threshold(map_id)[0], threshold(map_id)[1],
                       MAP_CLANGING, OUT[map_id][0], OUT[map_id][1])


def _girder(g, x1, x2, y, z=2):
    """A run of roof girder overhead. Every tile of it is a star tile, so the
    party walks underneath it, which is the only reason a shed reads as tall
    when it is drawn from directly above."""
    left, centre, right = K.SF_IN_GIRDER
    g.set(x1, y, z, left)
    for x in range(x1 + 1, x2):
        g.set(x, y, z, centre)
    g.set(x2, y, z, right)


# ============================================================== the works ====
def works_map():
    """The shed, the drawing office, and the frame of the Two Hundred.

    The drawing office is the west end and the shed is everything else, and
    the two are told apart by what is standing in them rather than by a wall,
    because Ott does not believe in the wall."""
    # One floor, not two. `interior`'s checkerboard is for the stock houses'
    # two tones of the same board; laid with two textures as unalike as
    # treadplate and concrete it comes out as a chessboard forty feet across.
    g = room(MAP_WORKS, floor=K.SF_METAL_FLOOR,
             wall_top=K.SF_IN_WALL_FACTORY, wall_face=K.SF_IN_FACE_FACTORY)
    g.autotile(0)

    # -- along the back wall. Two-tile props stand at y=3, which puts their
    # star-flagged top on the lower wall row and their solid foot on the first
    # row of floor.
    g.column(4, 3, 2, K.SF_IN_DRAWERS)      # a deed press, not a display case
    g.column(5, 3, 2, K.SF_IN_BOOKSHELF)
    g.set(7, 3, 2, K.SF_IN_BULLETIN)              # the drawings
    g.column(9, 3, 2, K.SF_IN_WALL_CLOCK)      # the shed runs on the hour
    g.column(10, 3, 2, K.SF_IN_DUCT)
    g.column(14, 3, 2, K.SF_IN_STEEL_SHELF)
    g.set(15, 3, 2, K.SF_IN_WARNING)
    g.column(16, 3, 2, K.SF_IN_PIPE_V)
    g.blit(18, 3, 2, K.SF_IN_PLUMBING)

    # -- the drawing office
    g.blit(4, 6, 2, (K.SF_IN_DESK_LARGE_B,))
    g.set(6, 6, 2, K.SF_IN_SIDE_DESK)             # the attempt log lives here
    g.set(4, 7, 2, K.SF_IN_STOOL)
    g.set(3, 9, 2, K.SF_IN_METAL_RUBBLE)
    g.set(4, 10, 2, K.SF_IN_PAPERS)

    # -- the shed. One run of girder overhead - two read as a fence rather
    # than as a roof, which is what happens when a star tile is the widest
    # thing in the room.
    _girder(g, 5, 20, 7)

    # The Two Hundred, in frame: two runs of heavy pipe on the shed floor with
    # a gap amidships to walk through, which is also how you get up the shed.
    # `Pipe (H)` is solid, so the frame is a thing you go round rather than a
    # pattern on the floor - and the airship herself is section 5.
    for x in list(range(6, 12)) + list(range(14, 20)):
        g.set(x, 11, 2, K.SF_IN_PIPE_H)

    # the shed furnace. `Large Machine` stood here and is a console bank
    # lit cyan; a works and a smithy both having a fire in them is not a
    # repetition, it is what the two trades have in common.
    g.blit(17, 13, 2, K.SF_IN_FIREPLACE)
    g.blit(7, 14, 2, K.SF_IN_PLUMBING)
    g.set(4, 13, 2, K.SF_IN_MACHINE_C)
    g.set(5, 13, 2, K.SF_IN_MACHINE_C)
    g.set(3, 15, 2, K.SF_IN_VALVE)
    g.column(21, 5, 2, K.SF_IN_STACKED_CRATES)
    g.column(21, 9, 2, K.SF_IN_STACKED_CRATES)
    g.column(21, 15, 2, K.SF_IN_STACKED_CRATES)
    g.column(20, 15, 2, K.SF_IN_BOOKSHELF)
    g.set(19, 9, 2, K.SF_IN_RUBBLE)
    g.set(6, 9, 2, K.SF_IN_MACHINE_C)
    g.column(4, 8, 2, K.SF_IN_STACKED_CRATES)
    g.set(18, 8, 2, K.SF_IN_VALVE)
    g.set(3, 12, 2, K.SF_IN_RUBBLE)
    g.set(18, 16, 2, K.SF_IN_DRAIN)      # not (12, 15): that is straight in front of the door
    g.set(15, 15, 2, K.SF_IN_MACHINE_C)
    g.set(4, 16, 2, K.SF_IN_METAL_RUBBLE)
    return finish(MAP_WORKS, g, "The Hoyle Works", bgm="Ship1",
                  battleback=("Stone1", "Room1"), events=works_events())


# =========================================== 5: the Two Hundred, and the ask ==
# NORTH.md 5.1-5.4. Everything below is an addition under 1.7: four pages
# appended to Ott's `ladder`, one new event on the shed floor, one page
# appended to the attempt log, and three pages appended to Bryd. Not a
# syllable of what any of them already said is touched.
#
# **Why the ask is not one of Ott's pages.** A page condition is a set of ANDs
# with no NOT in it, so there is no way to write "she has finished the steam
# ladder and has *not* yet asked" as a page: it is the same condition as the
# last rung of the ladder, and a page with the same condition wins and deletes
# the rung. So the ask is pattern one - a new event - and it goes on the chalk
# line amidships, which is where the player is standing when they are inside
# the thing she wants them to fly.
#
# That makes the quest open on the fourth conversation rather than the first,
# and that is the right answer rather than a compromise: 5.6's timing joke is
# that you are handed the airship once the map is already walked, and four
# conversations with the chief engineer is the cheapest honest way to spend
# that time. She does not hand the fourth generation of the experiment to
# somebody who has said hello.
CHALK_LINE = (12, 11)           # the gap amidships, between the two runs of
                                # frame; the player walks up the shed through it


def _still_wants(indent=0):
    """What is outstanding, asked and answered in Ott's own register, which is
    as few words as will do the job."""
    out = R.if_then(R.condition_switch(db.SW_OILSKIN_GOT, False), S.say("Ott", [
        "Fabric. Forty bolts of oilskin.",
        "Mrs Barrow, Nether Sopping.",
    ]) + S.say("Ott", [
        "She will not have forty.",
        "Make her find forty.",
    ]), indent=indent)
    out += R.if_then(R.condition_switch(db.SW_SPAR_DONE, False), S.say("Ott", [
        "Spar. Ollerenshaw's, bottom of the hill.",
    ]) + S.say("Ott", [
        "Tell him this one has to hold.",
        "He will say we shall see. He always does.",
    ]), indent=indent)
    return out


def ott_the_two_hundred():
    """The four pages appended to Ott, in the order the quest goes through them.

    `Game_Event.refresh` takes the **last** page whose conditions hold, and a
    page's conditions are ANDed, so the state machine is written by making each
    page's condition strictly harder than the one before it: the standing
    order, then the same thing with forty bolts of oilskin in the party's
    hands, then both parts in and the handover, then afterwards. All four also
    require self switch D, which is the last rung of the ladder above, so
    nothing here can fire before she has finished saying what she has to say
    about the drain cock."""
    order = S.say("Ott", ["Well?"]) + _still_wants() + S.say("Ott", [
        "Off you go, then.",
    ])

    # The fabric, arriving. She counts it. Everybody in this town counts
    # things, and this is the largest order of Mrs Barrow's life going the
    # other way, which is 5.1's reason for tying the two expansions together.
    fabric = S.say("Ott", ["Is that it?"]) + S.narrate([
        "She counts them. She counts all forty, out loud,",
        "in front of you, and does not hurry any of it.",
    ]) + S.say("Ott", [
        "Forty.",
    ]) + S.say("Ott", [
        "Nobody has ever brought me forty",
        "of anything.",
    ]) + [R.gain_item(db.IT_OILSKIN_BOLTS, -1),
          R.control_switch(db.SW_OILSKIN_GOT, True), R.play_me("Item")]
    fabric += R.if_then(R.condition_switch(db.SW_SPAR_DONE, False),
                        S.say("Ott", [
                            "Spar next. Ollerenshaw's.",
                        ]),
                        S.say("Ott", [
                            "That is the pair of them.",
                            "Come back in the morning.",
                        ]))

    # 5.3. The handover, and then the engine is left to deliver the punchline
    # unassisted: it will fly the party over the Obligatory Tower all day and
    # set them down beside it, on the grass, on foot.
    handover = S.narrate([
        "The shed doors are open. There is a great deal",
        "of daylight in here that was not here before.",
    ]) + S.say("Ott", [
        "She is yours.",
        "Where will you take her first?",
    ]) + S.narrate([
        "You think about it.",
    ]) + S.narrate([
        "You have been everywhere.",
    ]) + S.say("Ott", [
        "Ah. Yes.",
    ]) + S.say("Ott", [
        "I am told that is traditional.",
        "I did ask.",
    ]) + S.narrate([
        "The Two Hundred goes down the yard on ropes, at",
        "the speed of the slowest person holding one.",
        "That is everybody in the town who is not at work",
        "and several who are.",
    ]) + [R.play_me("Fanfare1"), R.wait(30),
          R.set_vehicle_location(R.AIRSHIP, MAP_WORLD, *WORLD_AIRSHIP),
          R.control_switch(db.SW_AIRSHIP, True), S.trope()] + S.narrate([
        "The Two Hundred is standing on the grass outside",
        "the town gate.",
    ])

    after = S.say("Ott", [
        "She is outside the gate.",
    ]) + S.say("Ott", [
        "Do not set her down on anything",
        "with a roof on it. You would be astonished",
        "how often that has been the finding.",
    ])

    return [
        R.page(order, img=_ott_face(), trigger=0, priority=1,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "D",
                           "switch1Valid": True,
                           "switch1Id": db.SW_TWO_HUNDRED_ASKED}),
        R.page(fabric, img=_ott_face(), trigger=0, priority=1,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "D",
                           "switch1Valid": True,
                           "switch1Id": db.SW_TWO_HUNDRED_ASKED,
                           "itemValid": True, "itemId": db.IT_OILSKIN_BOLTS}),
        R.page(handover, img=_ott_face(), trigger=0, priority=1,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "D",
                           "switch1Valid": True,
                           "switch1Id": db.SW_OILSKIN_GOT,
                           "switch2Valid": True,
                           "switch2Id": db.SW_SPAR_DONE}),
        R.page(after, img=_ott_face(), trigger=0, priority=1,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "D",
                           "switch1Valid": True, "switch1Id": db.SW_AIRSHIP}),
    ]


def _ott_face():
    sheet, index = S.FACES["Ott"]
    return R.image(sheet, index, direction=2)


def chalk_line(event_id):
    """The ask, delivered from inside the machine.

    5.1's speech, and the best beat in the north: she has considered the
    Prophecy, privately, for years; she will not say so; she has designed the
    experiment anyway; and the missing part walked in this morning and asked
    whether they had a gift shop. It inverts 'they have sent a lad', which is
    the first thing she ever says to Bram, and neither line mentions the other.

    Player touch, below characters, and it speaks exactly twice in a whole
    playthrough - once for the chalk line and once for the ask - because
    something that talks every time you walk up your own shed is a fault."""
    ask = S.narrate([
        "Somebody has stopped work behind you.",
    ]) + S.say("Ott", [
        "Lift has never been the problem.",
        "I want you clear on that.",
    ]) + S.say("Ott", [
        "We can get anything off the ground.",
        "We have had a shed off the ground.",
    ]) + S.say("Ott", [
        "They come down. That is all they do.",
        "They come down in sight of the tower.",
    ]) + S.say("Ott", [
        "And I have one variable left that I have",
        "never once been able to get hold of.",
    ]) + S.narrate([
        "She looks at you for slightly too long.",
    ]) + S.say("Ott", [
        "And it walked into my works this morning",
        "and asked whether we had a gift shop.",
    ]) + S.say("Ott", [
        "Three things, then.",
    ]) + _still_wants() + S.say("Ott", [
        "And a pilot who has been to the tower",
        "and come back.",
    ]) + S.narrate([
        "She goes back to the drawing. That appears to",
        "be the whole of the interview.",
    ]) + [R.control_switch(db.SW_TWO_HUNDRED_ASKED, True),
          R.control_switch(db.SW_OILSKIN_ASKED, True),
          R.control_switch(db.SW_SPAR_ASKED, True),
          R.self_switch("A", True)]

    chalk = S.narrate([
        "You are standing amidships, in the middle of",
        "something that is mostly not there yet.",
    ]) + S.narrate([
        "From the far end of the shed, without looking up:",
    ]) + S.say("Ott", [
        "That side is HERE. The other side is NO.",
    ]) + [R.self_switch("B", True)]

    # The event cannot read another event's self switch as a page condition,
    # and Ott's D is the only marker of "she has finished". A script branch
    # can, and this is what a script branch is for.
    ready = "$gameSelfSwitches.value([%d, 2, 'D'])" % MAP_WORKS
    cmds = R.if_then(R.condition_script(ready), ask,
                     R.if_then(R.condition_self_switch("B", False), chalk))
    return R.event(event_id, "The Chalk Line", *CHALK_LINE, [
        R.page(cmds, img=R.image(""), trigger=1, priority=0, through=True),
        R.page([], img=R.image(""), trigger=1, priority=0, through=True,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ])


def attempt_200():
    """5.4, appended to the attempt log as a further page. The same object,
    with one more entry in it, and the same three words as 199.

    It is guarded by `SW_TWO_HUNDRED_FLEW` rather than by the handover,
    because the second line of it is a claim about something that has to have
    happened - see the Clause Seven event in `field.py`."""
    return [R.page(S.narrate([
        "\\C[6]THE HOYLE WORKS - ATTEMPT LOG\\C[0]",
        "",
        "200. REACHED THE TOWER.",
        "     LANDED ADJACENT.",
    ]) + S.narrate([
        "     CAUSE: UNDER REVIEW.",
    ]) + S.narrate([
        "Three words, in a fresh hand, at the bottom of a",
        "page that has said them once already.",
        "Two hundred years, and the only thing in this",
        "building she will not write down is the reason.",
    ]), img=R.image(""), trigger=0, priority=1,
        conditions={"switch1Valid": True,
                    "switch1Id": db.SW_TWO_HUNDRED_FLEW})]


def works_events():
    evs = [way_out(MAP_WORKS, "Works Door")]

    # -- 2: Ottoline Hoyle -------------------------------------------------
    # Chief engineer, fourth generation, deadpan, precise, and with no
    # capacity for embarrassment whatsoever. She is not a fool and must never
    # be played as one: she has looked at a four-thousand-year-old curse and
    # seen a load case.
    #
    # Her four steam-vocabulary beats are on a `ladder`, one per visit, for
    # the reason in NORTH.md 4.7 - the moment it becomes The Bit it stops
    # being a repair. Every one of them is a real term. Nobody has written a
    # dirty line; somebody has written a repair, accurately, and the
    # authenticity is the whole defence.
    #
    # The Two Hundred quest (section 5) is a **page appended after these**,
    # guarded by its own switch: 1.7 pattern two, and the reason this event
    # will not have to be edited when it arrives.
    evs.append(ladder(2, "Ott", 13, 9, "Ott", [
        S.narrate([
            "A woman with a slide rule, and goggles pushed",
            "up into her hair, does not look up.",
        ]) + S.say("Ott", [
            "Two hundred years I have been at this.",
            "Four generations of us.",
        ]) + S.narrate([
            "Now she looks up.",
        ]) + S.say("Ott", [
            "And they have sent a lad.",
        ]) + S.say("Ott", [
            "No offence intended. Some given,",
            "I will grant you. But none intended.",
        ]) + S.narrate([
            "You ask, politely, how the work is going.",
        ]) + S.say("Ott", [
            "She's blowing off at the drain cock,",
            "the gland has gone on the big end,",
            "and she primes if you heat her too fast.",
        ]) + S.say("Ott", [
            "Otherwise she is sound.",
        ]) + R.if_then(
            R.condition_actor_in_party(db.MERRI),
            S.narrate([
                "Merribell nods along. Merribell is a field",
                "medic and this is a Tuesday.",
            ]),
            S.narrate([
                "You have found something to look at.",
            ])) + [S.blush()],

        S.say("Ott", [
            "Get on the stuffing box with the packing,",
            "and do not be shy with it.",
        ]) + S.narrate([
            "You do not say anything for a moment.",
        ]) + S.say("Ott", [
            "It is a box. You stuff it.",
            "That is what it is called.",
        ]) + [S.blush()],

        S.say("Ott", [
            "Nipples want doing every forty hours.",
        ]) + S.say("Ott", [
            "There are thirty-one of them.",
            "You will want the small can.",
        ]) + S.narrate([
            "Nib, without being asked, hands you the",
            "small can.",
        ]) + [S.blush()],

        S.say("Ott", [
            "That is a male thread, that is a female,",
            "and they do not go together.",
        ]) + S.say("Ott", [
            "I have had this conversation with every",
            "apprentice I have ever had, and every one",
            "of them does the face.",
        ]) + S.say("Ott", [
            "You are doing the face.",
        ]) + S.narrate([
            "Nib has stopped work to watch this happen",
            "to somebody else for once.",
        ]) + [S.blush()],

        S.say("Ott", [
            "Mind the swarf.",
        ]) + S.say("Ott", [
            "And do not touch anything with a handle",
            "on it. Or a wheel. Or a lever.",
        ]) + S.say("Ott", [
            "Or, on reflection, anything.",
        ]),
    ], direction=2,
        pages=ott_the_two_hundred() + field.ott_field_pages()))

    # -- 3: Nib, the fortieth apprentice
    evs.append(talker(
        3, "Nib", 16, 10, "Nib",
        S.say("Nib", [
            "I am the apprentice.",
            "There has been an apprentice here",
            "since eighteen oh four.",
        ]) + S.say("Nib", [
            "We are numbered. I am the fortieth.",
        ]) + S.say("Nib", [
            "Miss Hoyle says the numbering is not a",
            "joke, and I have decided to believe her.",
        ]),
        S.say("Nib", [
            "She will want the small can.",
            "She always wants the small can.",
        ]), direction=4))

    # -- 4: the Two Hundred, in frame. The airship itself is section 5; what
    # is here is the shape of it and the chalk line, which is the town.
    evs.append(S.sign(4, "The Two Hundred", 11, 11, [
        "The Two Hundred, in frame.",
        "There is a great deal of her, and most of it",
        "is air, and the air is not in anything yet.",
        "Somebody has chalked a line across the shed",
        "floor and written HERE on one side of it",
        "and NO on the other."]))

    # -- 5: the attempt log, on the drawing office desk. Section 5.4 appends a
    # further page to it rather than editing this one, so the log a player has
    # already read stays exactly as they read it and simply acquires a line.
    log = S.sign(5, "The Attempt Log", 6, 6, [
        "\\C[6]THE HOYLE WORKS - ATTEMPT LOG\\C[0]",
        "",
        "197. LOST OVER THE LONG FIELD.",
        "     CAUSE: ENVELOPE, SEAM.",
        "198. LOST OVER THE LONG FIELD.",
        "     CAUSE: ENVELOPE, THE OTHER SEAM.",
        "199. LOST IN SIGHT OF THE TOWER.",
        "     CAUSE: UNDER REVIEW.",
        "That entry was made eleven years ago.",
        "The ink is the same age as the rest of the",
        "page: it was written on the day, in one",
        "sitting, and nobody has been back to it."])
    log["pages"] += attempt_200()
    evs.append(log)

    # -- 6: the drawings
    evs.append(S.sign(6, "The Drawings", 7, 3, [
        "Drawings, pinned four deep.",
        "The one on top is this spring's main spar.",
        "The one under it is last spring's main spar,",
        "with one dimension crossed out and redrawn."]))

    # -- 7: the chalk line amidships, which is where the quest is asked for
    evs.append(chalk_line(7))

    # -- 8: the stores book, which is the only thing in the game that will
    # tell you what is still aboard Attempt 199, and does it by arithmetic.
    # Appended, never inserted: a self switch is keyed on the event id.
    evs.append(field.stores_ledger(8, 5, 4))
    return evs


# ========================================================= the Safety Valve ==
def valve_map():
    """The inn. Named for the one part of a boiler whose entire job is to give
    up before anything else does."""
    g = room(MAP_VALVE, floor=K.IN_WOOD_FLOOR, floor_alt=K.IN_DARK_WOOD,
             wall_top=K.SF_IN_WALL_WOOD, wall_face=K.SF_IN_FACE_WOOD,
             threshold=K.SF_STAIRS_WOOD[3], outside=K.SF_STAIRS_WOOD[3])
    g.autotile(0)

    # -- the back wall: the shelves behind the bar, the framed list, the clock
    g.column(3, 3, 2, K.SF_IN_ODDMENTS)
    g.column(4, 3, 2, K.SF_IN_DRAWERS)
    # THINGS THAT ARE NOT TO HAPPEN AGAIN. `Black Board` was tried here,
    # three tiles of chalked board being the right shape for a list of
    # sixty-three: it is chalked with a bar chart, a graph and a line of
    # katakana, and reads as a lecture theatre. The blank board it is.
    g.set(7, 3, 2, K.SF_IN_BULLETIN)
    g.column(12, 3, 2, K.SF_IN_WALL_CLOCK)
    g.blit(14, 3, 2, K.SF_IN_FIREPLACE)
    g.column(17, 3, 2, K.SF_IN_PLANT)

    # -- the bar. `Large Desk B` is a two-tile counter with a dark top, and
    # it carries the counter flag (0x80) as well as being solid, so the
    # action button reaches across it and Mr Kell stands behind his own bar
    # instead of beside it. Two of them make one unbroken four-tile run;
    # a row of `Side Table` here read as four little round tables in a line,
    # which is the Slain Wyvern's mistake and this town is not that town.
    g.blit(3, 6, 2, (K.SF_IN_DESK_LARGE_B,))
    g.blit(5, 6, 2, (K.SF_IN_DESK_LARGE_B,))
    g.set(3, 6, 3, K.SF_IN_MUG)
    g.set(5, 6, 3, K.SF_IN_TEAPOT)
    g.set(6, 6, 3, K.SF_IN_BREAD)

    # -- the room. Stools are passable, so they go anywhere; tables are not.
    for tx, ty in [(9, 7), (13, 7), (9, 10), (14, 10)]:
        g.set(tx, ty, 2, K.SF_IN_TABLE)
    g.set(9, 7, 3, K.SF_IN_MEAT)
    g.set(13, 7, 3, K.SF_IN_MUG)
    g.set(9, 10, 3, K.SF_IN_PLATE)
    g.set(14, 10, 3, K.SF_IN_WINE)
    g.scatter([(8, 7), (10, 7), (12, 7), (8, 10), (10, 10), (15, 10),
               (13, 10)], 2, K.SF_IN_STOOL)
    g.set(15, 6, 2, K.SF_IN_TABLE)                # the fireside table
    g.set(15, 6, 3, K.SF_IN_MUG)
    g.scatter([(14, 6), (16, 6)], 2, K.SF_IN_STOOL)
    g.column(3, 10, 2, K.SF_IN_BOOKSHELF)
    g.set(17, 12, 2, K.SF_IN_LAMP)
    g.set(3, 12, 2, K.SF_IN_LAMP)
    return finish(MAP_VALVE, g, "The Safety Valve", bgm="Town5",
                  battleback=("Wood1", "Room1"), events=valve_events())


BED_PRICE = 30


def valve_events():
    evs = [way_out(MAP_VALVE, "Safety Valve Door")]

    beds = S.say("Mr Kell", [
        "Beds are %d. You will be dry." % BED_PRICE,
        "That is worth %d up here." % BED_PRICE,
    ])
    beds += R.choice_block(
        ["Take a room (%dcr)" % BED_PRICE, "Not tonight"],
        [R.if_then(
            R.condition_script("$gameParty.gold() >= %d" % BED_PRICE),
            [R.lose_gold(BED_PRICE), R.fadeout_screen(), R.play_me("Inn2"),
             R.recover_all(), R.wait(90), R.fadein_screen()] +
            S.say("Mr Kell", [
                "You slept through the six o'clock",
                "hooter. Nobody does that.",
            ]),
            S.say("Mr Kell", ["Come back with %d." % BED_PRICE]))],
        cancel=None)

    evs.append(talker(
        2, "Mr Kell", 5, 5, "Mr Kell",
        S.say("Mr Kell", [
            "The Safety Valve.",
        ]) + S.say("Mr Kell", [
            "Named for the one part of a boiler",
            "whose entire job is to give up before",
            "anything else does.",
        ]) + S.say("Mr Kell", [
            "We are very proud of it.",
        ]) + beds,
        list(beds), direction=2))

    # -- 3: the framed list. The accidental record, mechanism four: a document
    # does not know what it is saying, and this one has been redacted by
    # somebody who very much does.
    evs.append(S.sign(3, "Things That Are Not To Happen Again", 7, 3, [
        "A framed list on the wall, in a very good",
        "hand, numbered to sixty-three. Most of the",
        "entries have been reduced to a single word.",
        "",
        "     7.  THE GEESE",
        "    19.  NOT LIKE THAT",
        "    31.  HOT",
        "    44.  MR PADGETT'S HAT (AND MR PADGETT)",
        "    58.  ANY OF IT",
        "    61.  OLLERENSHAW",
        "",
        "Number sixty-three is one very long word.",
        "Nobody in the room will say it aloud."]))

    # -- 4: Winnie Marsden. The other half of Mrs Tunnicliffe's census, said
    # by somebody with no idea what she is telling you - which is why she
    # does **not** bump the counter. It is one joke. Counting it twice would
    # be the game explaining it, and 1.5's fourth test forbids that.
    evs.append(talker(
        4, "Winnie Marsden", 13, 8, "Winnie",
        S.say("Winnie", [
            "Class of 'Nineteen.",
        ]) + S.say("Winnie", [
            "We have a dinner. I do not suppose",
            "you would know about the dinner.",
        ]) + S.say("Winnie", [
            "There is a seating plan. There has",
            "been a seating plan since we were four.",
        ]) + S.say("Winnie", [
            "You cannot get in. I am not being",
            "unkind about it. You had to be born",
            "in it.",
        ]),
        S.say("Winnie", [
            "Second Saturday. As ever.",
        ]), direction=4))
    return evs


# ============================================================ Ollerenshaw's ==
def forge_map():
    """Ollerenshaw's. It shares its music with Grumnir's Smithy, which is not
    an accident and is not to be pointed at."""
    # Wall J (Factory) is dark brown brick, which is the only warm masonry on
    # SF Inside's A4. Wall K (Brick) and Wall E (Metal, Red Rust) both sound
    # right and both come out pale grey - their *tops* do, which is nearly all
    # of what you see of an interior wall, and the sampler draws the top and
    # the face together for exactly that reason. Both made the forge read as
    # a cold cellar.
    g = room(MAP_FORGE, floor=K.SF_CONCRETE,
             wall_top=K.SF_IN_WALL_FACTORY_B, wall_face=K.SF_IN_FACE_FACTORY_B)
    g.autotile(0)

    g.blit(4, 3, 2, K.SF_IN_FIREPLACE)            # the hearth
    g.column(8, 3, 2, K.SF_IN_PIPE_V)
    g.column(11, 3, 2, K.SF_IN_ODDMENTS)
    g.set(12, 3, 2, K.SF_IN_WARNING)
    g.set(13, 3, 2, K.SF_IN_BULLETIN)         # orders, on a spike
    g.column(15, 3, 2, K.SF_IN_DRAWERS)       # the tool press

    g.set(7, 7, 2, K.SF_IN_MACHINE_C)             # the drop hammer
    g.set(6, 5, 2, K.SF_IN_VALVE)
    g.column(3, 6, 2, K.SF_IN_STEEL_SHELF)
    g.set(13, 7, 2, K.SF_IN_CHEST_METAL)
    g.column(14, 5, 2, K.SF_IN_STACKED_CRATES)
    g.set(14, 10, 2, K.SF_IN_METAL_RUBBLE)
    g.set(3, 10, 2, K.SF_IN_METAL_RUBBLE)
    g.blit(4, 10, 2, K.SF_IN_RUBBLE_PILE)
    g.set(6, 11, 2, K.SF_IN_RUBBLE)       # not (9, 11): that is the doorway
    g.set(13, 11, 2, K.SF_IN_RUBBLE)
    g.set(5, 8, 2, K.SF_IN_DRAIN)

    # The spar, on trestles. A run of `Pipe (H)`: the belt conveyor was tried
    # first and reads as exactly what it is, which is a conveyor belt.
    for x in range(9, 14):
        g.set(x, 9, 2, K.SF_IN_PIPE_H)
    return finish(MAP_FORGE, g, "Ollerenshaw's", bgm="Town4",
                  battleback=("Stone1", "Room1"), events=forge_events())


def forge_events():
    evs = [way_out(MAP_FORGE, "Forge Door")]

    # -- 2: Bryd Ollerenshaw, and twenty years, and nothing said -----------
    #
    # NORTH.md 4.6, and section 14 confirms it. **The game never says the
    # thing.** Nobody announces anything, nobody has a Moment, the two of them
    # cannot finish a sentence in the same room, a child says "they do this
    # every time", and the payoff - which belongs with the spar in section 5 -
    # is that they go for a drink. A child reads two grown-ups being strange
    # at each other. An adult reads twenty years. A coming-out scene, a
    # declaration or a kiss would be a misreading of the entire document, and
    # so would any line in which either of them is unhappy about it.
    #
    # All of the state is in one page rather than in page conditions, because
    # the meeting has to fire the moment Hob walks in - including on a second
    # visit, when Bryd has already introduced himself to a Hobless party.
    plain = S.say("Bryd", [
        "Ollerenshaw's.",
        "Mine, my father's, and his mother's",
        "before that.",
    ]) + S.say("Bryd", [
        "If it is iron and it has to hold,",
        "it comes to me.",
    ]) + S.say("Bryd", [
        "Miss Hoyle sends me a drawing every",
        "spring. Every spring it is a spar.",
    ]) + S.say("Bryd", [
        "One of these springs I will get it right.",
    ])
    plain_again = S.say("Bryd", [
        "Spar's not ready.",
        "It will not get ready by being asked.",
    ])

    meeting = S.say("Hob", [
        "...Ollerenshaw.",
    ]) + S.say("Bryd", [
        "...Grumnir.",
    ]) + S.narrate([
        "Neither of them says anything else.",
    ]) + S.narrate([
        "The forge is very warm.",
    ]) + S.narrate([
        "Somewhere behind you a child says 'they do",
        "this every time', and is removed.",
    ]) + S.say("Hob", [
        "You kept the place on, then.",
    ]) + S.say("Bryd", [
        "I kept the place on.",
    ]) + S.say("Hob", [
        "Aye.",
    ]) + S.narrate([
        "That appears to be the whole of it.",
        "They are both entirely satisfied.",
    ]) + [S.blush()]
    hob_again = S.narrate([
        "They have not moved.",
    ]) + S.say("Bryd", [
        "Aye.",
    ])

    sheet, index = S.FACES["Bryd"]
    img = R.image(sheet, index, direction=6)
    evs.append(R.event(2, "Bryd Ollerenshaw", 6, 7, [R.page(
        R.if_then(
            R.condition_actor_in_party(db.HOB),
            R.if_then(R.condition_self_switch("B", False),
                      meeting + [R.self_switch("B", True)],
                      hob_again),
            R.if_then(R.condition_self_switch("A", False),
                      plain + [R.self_switch("A", True)],
                      plain_again)),
        img=img, trigger=0, priority=1)]
        + bryd_and_the_spar(img, meeting, plain)))

    # -- 3: the spar
    evs.append(S.sign(3, "The Spar", 11, 9, [
        "A bar of iron on trestles, longer than the",
        "room and straight enough to sight along.",
        "",
        "Chalked on it, in a hand that is not Bryd's:",
        "THIS ONE.",
        "",
        "Underneath, in a hand that is:",
        "WE SHALL SEE."]))
    return evs


def bryd_and_the_spar(img, meeting, plain):
    """Three pages appended to Bryd: the forging, the day it takes, and after.

    NORTH.md 5.1 puts the drink here, with the spar, and 4.6 and section 14
    say what it is and what it must never become. If Hob is in the party the
    two of them do it together in an afternoon and then go out, and nobody
    says anything about anything. If he is not, Bryd does it alone and it
    takes a day, and you get the shorter version of the same scene - which is
    also the only version in which Grumnir is mentioned by name and not
    present, and it costs Bryd nothing to be glad about that.

    `SW_HOB_BRYD` is set on the first path only. They cannot go for a drink if
    one of them is four days' walk south.

    `meeting` and `plain` are page one's own two openings, handed in so that a
    party who reaches the spar without ever having spoken to him gets the
    introduction first rather than instead. They are the same lists page one
    builds - nothing is rewritten, and the self switches page one latches are
    the ones this checks."""
    together = S.say("Bryd", [
        "Miss Hoyle's spar.",
    ]) + S.say("Bryd", [
        "It wants two.",
        "It has always wanted two.",
    ]) + S.narrate([
        "Hob Grumnir takes his coat off without being",
        "asked and without saying anything at all.",
    ]) + S.narrate([
        "It takes them the afternoon. Neither of them",
        "speaks once. They do not need to; they were",
        "apprenticed together, and a hammer is a",
        "conversation if you have had twenty years of it.",
    ]) + S.say("Bryd", [
        "That will hold.",
    ]) + S.say("Hob", [
        "Aye.",
    ]) + S.narrate([
        "They stand and look at it for a while.",
    ]) + S.say("Bryd", [
        "There is a house at the bottom",
        "of the hill that does a pale.",
    ]) + S.say("Hob", [
        "Aye.",
    ]) + S.narrate([
        "They go.",
        "Half of Upper Clanging watches them go and the",
        "other half is told about it within the hour.",
    ]) + [S.blush(), R.control_switch(db.SW_HOB_BRYD, True),
          R.control_switch(db.SW_SPAR_DONE, True), R.play_me("Fanfare1")]

    alone = S.say("Bryd", [
        "Miss Hoyle's spar. Aye.",
    ]) + S.say("Bryd", [
        "It wants two, that job.",
        "It has always wanted two.",
    ]) + S.narrate([
        "You ask whether there is anybody who could",
        "stand the other end of it."]) + S.say("Bryd", [
        "There was.",
        "He went south twenty year ago come spring.",
    ]) + S.say("Bryd", [
        "Grumnir. You will not know him.",
    ]) + S.narrate([
        "He says the name the way a man reads a",
        "dimension off a drawing he has known by heart",
        "for a very long time.",
    ]) + S.say("Bryd", [
        "It will take me a day on my own.",
        "Go and get her fabric. It will be here.",
    ]) + [R.self_switch("C", True)]

    ready = S.narrate([
        "The spar is off the trestles and up on the",
        "wall, where the finished ones go.",
    ]) + S.say("Bryd", [
        "Done. On my own, and it will hold.",
    ]) + S.say("Bryd", [
        "Tell her I said we shall see.",
        "She will know what I mean by it.",
    ]) + [R.control_switch(db.SW_SPAR_DONE, True), R.play_me("Fanfare1")]

    after = R.if_then(
        R.condition_switch(db.SW_HOB_BRYD),
        S.say("Bryd", [
            "That is a good spar.",
        ]) + S.say("Bryd", [
            "It was a good afternoon, an' all.",
        ]),
        S.say("Bryd", [
            "That is a good spar.",
        ]) + S.say("Bryd", [
            "It would have been a better one",
            "with somebody on the far end.",
        ]))

    # Somebody who is handed the spar errand before they have ever said hello
    # to him would otherwise skip the introduction - and, with Hob along, skip
    # the meeting, which is one of the town's nine blushes. So page one's
    # openings run first if their self switch is still down.
    asked = R.if_then(
        R.condition_actor_in_party(db.HOB),
        R.if_then(R.condition_self_switch("B", False),
                  list(meeting) + [R.self_switch("B", True)]) + together,
        R.if_then(R.condition_self_switch("A", False),
                  list(plain) + [R.self_switch("A", True)]) + alone)
    return [
        R.page(asked, img=img, trigger=0, priority=1,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_SPAR_ASKED}),
        R.page(ready, img=img, trigger=0, priority=1,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_SPAR_ASKED,
                           "selfSwitchValid": True, "selfSwitchCh": "C"}),
        R.page(after, img=img, trigger=0, priority=1,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_SPAR_DONE}),
    ]


# ========================================================= the Parish Rooms ==
def parish_map():
    """The Parish Rooms: the register, the census, and - because in a town this
    size the registrar also sells things - the counter."""
    # One floor, and a warm one. Tile-and-lino chequered came out as a public
    # convenience forty feet across - the trap `interior`'s `floor_alt` is
    # written up for. `SF_FLOOR_CARPET` is a plain green office carpet, which
    # is what you put under a register.
    g = room(MAP_PARISH, floor=K.SF_FLOOR_CARPET,
             wall_top=K.SF_IN_WALL_PATTERN, wall_face=K.SF_IN_FACE_PATTERN)
    g.autotile(0)

    g.column(4, 3, 2, K.SF_IN_DRAWERS)      # a deed press, not a display case
    g.column(5, 3, 2, K.SF_IN_BOOKSHELF)
    g.column(6, 3, 2, K.SF_IN_ODDMENTS)
    g.set(8, 3, 2, K.SF_IN_BULLETIN)
    g.set(10, 3, 2, K.SF_IN_PAINTING_A)     # a framed landscape
    g.column(12, 3, 2, K.SF_IN_WALL_CLOCK)
    g.column(14, 3, 2, K.SF_IN_STEEL_SHELF)       # what there is, is behind me
    g.column(15, 3, 2, K.SF_IN_PLANT)

    # The counter, which is also the shop. Two Large Desks side by side: the
    # tile is solid *and* carries the counter flag, so nobody walks on it and
    # the action button reaches over it.
    g.blit(5, 7, 2, (K.SF_IN_DESK_LARGE_B,))
    g.blit(7, 7, 2, (K.SF_IN_DESK_LARGE_B,))
    g.set(5, 7, 3, K.SF_IN_DOCUMENT)
    g.set(8, 7, 3, K.SF_IN_BOOK)

    g.set(12, 6, 2, K.SF_IN_SIDE_DESK)            # the register lives here
    g.set(12, 6, 3, K.SF_IN_BOOK_STAND)
    g.set(11, 9, 2, K.SF_IN_STOOL)
    g.set(3, 9, 2, K.SF_IN_STOOL)              # somewhere to wait
    g.set(14, 9, 2, K.SF_IN_POTTED_PLANT)
    return finish(MAP_PARISH, g, "The Parish Rooms", bgm="Scene3",
                  battleback=("Wood1", "Room1"), events=parish_events())


# The counter. Consumables the town makes, the two garments nobody in this
# story owns, and one piece of works property that should not be for sale.
PARISH_STOCK = [
    (0, db.IT_POTION, 0, 0), (0, db.IT_HI_POTION, 0, 0),
    (0, db.IT_DRIPPING, 0, 0), (0, db.IT_STEWED_TEA, 0, 0),
    (0, db.IT_LINIMENT, 0, 0),
    (2, db.AR_TROUSERS, 0, 0), (2, db.AR_WORKS_CAP, 0, 0),
    (2, db.AR_OILSKIN, 0, 0),
    (1, db.WP_WRENCH, 0, 0),
]


def parish_events():
    evs = [way_out(MAP_PARISH, "Parish Rooms Door")]

    # -- 2: Mrs Tunnicliffe ------------------------------------------------
    # The registrar, and the accidental record in person. The census is the
    # one to fight hardest for: it is the most innocent object imaginable and
    # it does the whole job by itself. The punchline for a child is a woman
    # being sulky about a dinner. The punchline for an adult is the
    # arithmetic. Nothing has been said, and nothing may be added that says
    # it.
    census = S.say("Mrs Tunnicliffe", [
        "Class of 'Nineteen.",
        "The Cold Winter lot.",
    ]) + S.say("Mrs Tunnicliffe", [
        "Foundry was banked down",
        "six weeks that January. No work.",
        "No heat in the whole town but what",
        "was in the houses.",
    ]) + S.say("Mrs Tunnicliffe", [
        "Two hundred and forty of them.",
        "All born the same autumn,",
        "near enough.",
    ]) + S.say("Mrs Tunnicliffe", [
        "They have a dinner every year.",
        "I am not invited.",
        "I was born in June.",
    ])
    # She will tell it again to anybody who asks, and a player should be able
    # to hear it twice - but `VAR_BLUSHES` counts *moments*, not tellings, so
    # the bump is guarded rather than the speech. This is the one place in the
    # town where the beat is not already behind a self switch, and it counted
    # twice until `clanging_cast` was made to ask her twice.
    census += R.if_then(R.condition_switch(db.SW_CENSUS, False),
                        [S.blush(), R.control_switch(db.SW_CENSUS, True)])

    counter = S.say("Mrs Tunnicliffe", [
        "What there is, is behind me.",
    ]) + R.shop(PARISH_STOCK)

    desk = R.choice_block(
        ["The census", "The counter", "Nothing, thank you"],
        [census, counter, S.say("Mrs Tunnicliffe", [
            "Then you are the first today.",
        ])])

    evs.append(talker(
        2, "Mrs Tunnicliffe", 6, 6, "Mrs Tunnicliffe",
        S.say("Mrs Tunnicliffe", [
            "Parish Rooms.",
            "Births, deaths, and whatever else",
            "nobody else will take on.",
        ]) + S.say("Mrs Tunnicliffe", [
            "I have the register,",
            "the census, and the counter.",
        ]) + list(desk),
        list(desk), direction=2))

    # -- 3: the register. A document that does not know what it is saying,
    # and the one line in it that does.
    evs.append(S.sign(3, "The Register", 12, 6, [
        "The parish register, lying open at OCCUPATION.",
        "",
        "Every line reads AT THE WORKS. Page after page",
        "of it, in one hand, for eighty years.",
        "One entry, dated eighteen oh two, reads",
        "AT THE WORKS (THINKING).",
        "",
        "Somebody has pencilled HOYLE in the margin",
        "beside it and then rubbed it out, because the",
        "register does not take marginal notes."]))
    return evs


def build():
    R.save_map(MAP_CLANGING, clanging_map())
    R.save_map(MAP_WORKS, works_map())
    R.save_map(MAP_VALVE, valve_map())
    R.save_map(MAP_FORGE, forge_map())
    R.save_map(MAP_PARISH, parish_map())
