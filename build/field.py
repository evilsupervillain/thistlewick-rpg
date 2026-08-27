"""The north-west of the world map, and the two places out on it: Maps 26-27.

    26  The Long Field                     one hundred and ninety-nine wrecks
    27  The Wreck of the 199th             a crag, a dungeon, and ITEM 1

`journey.py` still owns Map 8 - it calls the five hooks at the top of this file
while it is drawing, so the world map is built in one place and the northern
content is written in one place. That is exactly the arrangement `wilds.py`
already has for the south; see `NORTH.md` sections 4.3 and 11.

The three **air-only places** of section 5.6 are here too, and they are not in
the north-west: one is in the bay off the south coast, one is a sea stack in
the north-western approaches, and one is seven squares out to sea due east of
the Hermit. They live in this file rather than a fourth module because they are
the airship's content and the airship is the north's, and because they are
three rocks and two dozen lines between them.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import db
import mapkit as K
import rmmzdata as R
import story as S
from places import (CLANGING_GATE, MAP_CLANGING, MAP_WORLD, MAP_LONG_FIELD,
                    MAP_CRAG, MAP_WORKS, WORLD_CLANGING,
                    WORLD_CLANGING_STEP, WORLD_LONG_FIELD, WORLD_CRAG,
                    WORLD_LONG_FIELD_STEP, WORLD_CRAG_STEP,
                    WORLD_JUNCTION, WORLD_ISLE, WORLD_ISLE_PAD, WORLD_STACK,
                    WORLD_STACK_PAD, WORLD_MIDDLE, WORLD_MIDDLE_PAD,
                    WORLD_TOWER, WORLD_STONES)

REG_CLANG = 4               # the north-west: whatever the works has let out


# ============================================== the north of the world map ==
def north_ground(g):
    """Layer 0. Called after the coastline blobs and before `autotile(0)`.

    The continent grows a north-west lobe for Upper Clanging to stand on. Its
    east side merges into the existing coast rather than making a bay, because
    the conifer wood `journey.py` plants at (11, 11) is eleven tiles wide and
    the old coastline only reached the eastern third of it - the other two
    thirds have been standing in open sea since the world map was drawn. The
    lobe puts ground under all of it."""
    g.blob(9, 12, 6, 7, 0, K.W_GRASS)             # the lobe itself
    g.blob(6, 9, 3, 3, 0, K.W_GRASS)              # the crag's shoulder
    g.blob(11, 17, 4, 2, 0, K.W_GRASS)            # down to the stones
    g.blob(3, 16, 2, 2, 0, K.W_SEA)               # a bite back out of it
    g.blob(13, 6, 2, 2, 0, K.W_SEA)
    _air_only_ground(g)


# ----------------------------------------------- the three air-only places --
# NORTH.md 5.6. An airship that only revisits places you have already walked to
# is a fast-travel toy, so three things go where no foot can reach them: put
# things in the sea and on top of things.
#
# The engine does all of the gating and none of it is scripted. Sea is flagged
# 0x080f, which is impassable on foot **and** sets the airship's own 0x0800, so
# a rock in open water with plain grass on top of it can only be landed on -
# and `validate.py` now asserts, out of the flags rather than by playing, that
# each of them is unreachable on the ground.
#
# Each rock keeps one square clear of events, because `Game_Vehicle.isLandOk`
# refuses to set an airship down on a square that has an event standing on it,
# and a landing site with a sheep on it is not a landing site.
ISLE = [(WORLD_ISLE[0] + i, WORLD_ISLE[1]) for i in range(4)]
STACK = [(WORLD_STACK[0] + i, WORLD_STACK[1]) for i in range(3)]
MIDDLE = [(WORLD_MIDDLE[0] + dx, WORLD_MIDDLE[1] + dy)
          for dy in range(3) for dx in range(2)]
AIR_ONLY = ISLE + STACK + MIDDLE


# `validate.py` reads this note off the finished data and asserts two things:
# that the event cannot be walked to from any transfer on the map, and that
# there is an airship on the map at all. An air-only joke that turns out to be
# walkable is a joke nobody will ever notice was one.
AIR_ONLY_NOTE = "<aironly>"


def _air_only_ground(g):
    """Layer 0: three rocks, drawn as plain world grass so that the top tile of
    each is 0x0600 - passable, and landable, and surrounded by water."""
    for x, y in AIR_ONLY:
        g.set(x, y, 0, K.W_GRASS)


def _upland(g, cx, cy, rx, ry, tile):
    """A layer-1 blob that stops at the water's edge.

    `Canvas.blob` does not know where the coast is, which is how eleven tiles
    of conifer came to be standing in the sea off this coast for the whole of
    the game so far. Anything drawn out here goes through this instead."""
    grass = R.autotile_kind(K.W_GRASS)
    for y in range(cy - ry, cy + ry + 1):
        for x in range(cx - rx, cx + rx + 1):
            if not (0 <= x < g.width and 0 <= y < g.height):
                continue
            dx, dy = (x - cx) / float(rx or 1), (y - cy) / float(ry or 1)
            if dx * dx + dy * dy > 1.0:
                continue
            under = g.get(x, y, 0)
            if R.is_autotile(under) and R.autotile_kind(under) == grass:
                g.set(x, y, 1, tile)


def north_layer1(g):
    """Layer 1: the high ground, the west road and its two spurs. Called
    before `autotile(1)`."""
    # A clearing for the town to stand in, cut out of the wood `journey.py`
    # planted here before there was any ground under it. The wood is two
    # hundred years older than the works and the works has been cutting into
    # it ever since. This goes first so the ridge can be drawn back into it.
    for y in range(9, 15):
        for x in range(7, 13):
            g.set(x, y, 1, 0)

    # High ground, and only where there is ground to put it on.
    _upland(g, 6, 7, 3, 2, K.W_MOUNTAIN)          # the crag
    _upland(g, 12, 9, 3, 2, K.W_HILLS_BROWN)      # the ridge behind the works
    _upland(g, 4, 14, 2, 3, K.W_HILLS)            # the west shoulder
    _upland(g, 7, 17, 2, 1, K.W_CONIFER)          # a copse below the town

    # The west road leaves the north road at the Gloamwood's north mouth and
    # runs along the top of the wood. It goes *past* the Standing Stones and
    # not between them: the plaque at (11, 18) is a player-touch event with no
    # self switch, so a road over it would re-read all four windows - and bump
    # the cliche counter the ending prints - every single time anybody walked
    # to Upper Clanging and back.
    track = []
    track += [(x, 20) for x in range(9, 18)]      # west, along the wood
    track += [(9, y) for y in range(WORLD_CLANGING_STEP[1], 21)]   # and north
    track += [(x, 15) for x in range(9, 13)]      # the Long Field spur
    track += [(x, 13) for x in range(6, 10)]      # the crag track
    track += [(6, y) for y in range(9, 14)]
    for x, y in track:
        g.set(x, y, 1, K.W_ROAD)

    # The Hermit's middle distance is a hill, so it gets a hill: two tiles of
    # it along the back of the rock. `W_HILLS` is flagged 0x0e0f, which is
    # impassable *and* sets 0x0800, so the hill is scenery you cannot land on
    # and the two rows of grass in front of it are where the airship goes and
    # where the bench is.
    g.set(WORLD_MIDDLE[0], WORLD_MIDDLE[1], 1, K.W_HILLS)
    g.set(WORLD_MIDDLE[0] + 1, WORLD_MIDDLE[1], 1, K.W_HILLS)


def north_layer3(g):
    """Layer 3: the three places you can walk into up here, and the things
    that are only there to be looked at."""
    g.blit(WORLD_CLANGING[0] - 1, WORLD_CLANGING[1] - 1, 3, K.WB_TOWN)
    g.set(WORLD_LONG_FIELD[0], WORLD_LONG_FIELD[1], 3, K.WB_HUT)
    g.set(WORLD_CRAG[0], WORLD_CRAG[1], 3, K.WB_CAVE_DARK)
    g.set(WORLD_JUNCTION[0], WORLD_JUNCTION[1], 3, K.WB_SIGN)
    for x, y in [(7, 15), (12, 14), (5, 11), (13, 16), (5, 17), (4, 9)]:
        g.set(x, y, 3, K.WB_TREE)
    for x, y in [(7, 7), (3, 12), (14, 13)]:
        g.set(x, y, 3, K.WB_ROCK)

    # The plaque at the west end of the Isle, and the stack Attempt 112 came
    # down on. Both `WB_SIGN` and `WB_ROCK` are flagged 0x060f - impassable,
    # and not landable either, because `isAirshipLandOk` wants 0x0f clear as
    # well as 0x0800 - so each of them is scenery that also narrows the rock
    # down to one square an airship can use.
    g.set(WORLD_ISLE[0], WORLD_ISLE[1], 3, K.WB_SIGN)
    g.set(WORLD_STACK[0], WORLD_STACK[1], 3, K.WB_ROCK)


def north_regions(g):
    """The lobe is its own encounter region. It is pointed at the same three
    troops as the rest of the north today, so nothing about a walk up here has
    changed yet - but the region exists, and `NORTH.md` section 15's northern
    encounters have somewhere to go that is not "everywhere north of the
    mountains"."""
    for y in range(21):
        for x in range(16):
            if g.get(x, y, 5):
                g.set(x, y, 5, REG_CLANG)

    # And nothing at all lives on the three rocks. `journey.py` hands every
    # square of the map a region by latitude, sea included, so without this the
    # Isle of Uncertain Ownership would have turnip encounters on it.
    for x, y in AIR_ONLY:
        g.set(x, y, 5, 0)


# ------------------------------------------------------ the events out there --
def north_events(next_id):
    """The world-map half of the north. `next_id` is the first free event id on
    Map 8, so everything already out there keeps its number.

    A destination event arrives with its map: a Transfer Player pointed at a
    map that does not exist is not a thing to leave lying about. Upper
    Clanging exists now, so its door is here. The Long Field's and the crag's
    still are not, and come with step 6."""
    evs = []
    evs.append(S.sign(next_id + len(evs), "West Road Signpost",
                      *WORLD_JUNCTION, [
        "\\C[6]UPPER CLANGING\\C[0] .......... 9 miles",
        "\\C[6]THE OBLIGATORY TOWER\\C[0] .... 14 miles",
        "",
        "The second figure has been crossed out and",
        "rewritten four times, in four hands, each",
        "more confident than the last."]))

    # -- the town itself, at the top of the road. The shape is Nether
    # Sopping's: look at it, decide, and mark that you have been. Coming out
    # again puts you back on the road at `WORLD_CLANGING_STEP`, and the
    # town's own gate event is what turns the rain off on the way.
    town = S.narrate([
        "Upper Clanging. Chimneys, and a clock, and a",
        "very great deal of rain falling on both."])
    town += R.choice_block(
        ["Go in", "Carry on"],
        [[R.play_se("Move1"), R.control_switch(db.SW_NORTH, True),
          R.transfer(MAP_CLANGING, CLANGING_GATE[0], CLANGING_GATE[1] - 1,
                     8, 0)], []])
    evs.append(R.event(next_id + len(evs), "Upper Clanging",
                       WORLD_CLANGING[0], WORLD_CLANGING[1], [R.page(
                           town, img=R.image(""), trigger=1, priority=0,
                           through=True)]))

    # -- the Long Field and the crag. Appended after everything step 5 wrote,
    # never inserted among it: a self switch is keyed on (map, event id,
    # letter), so putting a new event in the middle of this list would move
    # every id after it and silently reset the Isle, the sheep, Attempt 112,
    # the bench and Clause Seven in every existing save.
    evs.append(isle_plaque(next_id + len(evs)))
    evs.append(isle_sheep(next_id + len(evs)))
    evs.append(attempt_112(next_id + len(evs)))
    evs.append(the_bench(next_id + len(evs)))
    evs.append(clause_seven(next_id + len(evs)))
    evs.append(long_field_door(next_id + len(evs)))
    evs.append(crag_door(next_id + len(evs)))
    # NORTH.md 3.8. It belongs beside the Standing Stones, which are event 13,
    # and it is here at the end of the list instead for the reason above: a
    # self switch is keyed on (map, event id, letter), and an event inserted
    # next to its own subject would move every id after it.
    evs.append(stones_correction(next_id + len(evs)))
    return evs


def stones_correction(event_id):
    """NORTH.md 3.8: a second, newer, smaller notice beside the plaque.

    **The plaque is not edited.** A seventh theory added to the sign would be
    a longer sign; the parish correcting its own sign, on a separate board,
    six inches away, is funnier and it is an addition.

    It also does a job. The stones are the turn onto the west road, so this is
    the last thing a player reads before a whole town of people who will not
    accept the obvious explanation. Player-touch and below characters, which
    is the idiom every curiosity on this world map already uses - walk onto
    the thing and it speaks."""
    notice = S.narrate([
        "A second board beside the plaque. Newer,",
        "smaller, and screwed down much harder.",
    ])
    notice += S.narrate([
        "\\C[6]THEORY SEVEN HAS BEEN REMOVED AT THE\\C[0]",
        "\\C[6]REQUEST OF THE PARISH AND THE FAMILY.\\C[0]",
    ])
    notice += [S.blush(), R.self_switch("A", True)]

    again = S.narrate([
        "\\C[6]THEORY SEVEN HAS BEEN REMOVED AT THE\\C[0]",
        "\\C[6]REQUEST OF THE PARISH AND THE FAMILY.\\C[0]",
    ])
    page = dict(img=R.image(""), trigger=1, priority=0, through=True)
    return R.event(event_id, "Theory Seven",
                   WORLD_STONES[0], WORLD_STONES[1] + 1, [
        R.page(notice, **page),
        R.page(again, conditions={"selfSwitchValid": True,
                                  "selfSwitchCh": "A"}, **page),
    ])


def long_field_door(event_id):
    """The gate of the Long Field, on a spur off the town road.

    The shape is the town's and Nether Sopping's: look at it, decide, and mark
    that you have been. `SW_LONG_FIELD` is *not* set here - it is set by
    standing in the field, because "walked the Long Field" should mean that."""
    look = S.narrate([
        "A field below the town, on the slope, behind a",
        "hundred yards of good wrought-iron railing that",
        "stops abruptly at both ends.",
        "Rows of something, going away over the rise."])
    look += R.choice_block(
        ["Go in", "Carry on"],
        [[R.play_se("Move1"),
          R.transfer(MAP_LONG_FIELD, FIELD_IN[0], FIELD_IN[1], 8, 0)], []])
    return R.event(event_id, "The Long Field",
                   WORLD_LONG_FIELD[0], WORLD_LONG_FIELD[1], [R.page(
                       look, img=R.image(""), trigger=1, priority=0,
                       through=True)])


def crag_door(event_id):
    """The crag at the north-west corner of the island, and the thing on it.

    Attempt 199 came down here eleven years ago, right way up, and is still
    right way up. The way in is the rent she made in her own flank on the way
    down, which is the only thing about her that is broken."""
    look = S.narrate([
        "A crag, at the end of a track the works keeps",
        "cut and nobody uses.",
        "There is an airship on top of it, the right way",
        "up, eleven years dead."])
    look += R.choice_block(
        ["Climb up", "Carry on"],
        [[R.play_se("Move1"),
          R.transfer(MAP_CRAG, CRAG_IN[0], CRAG_IN[1], 8, 0)], []])
    return R.event(event_id, "The Wreck Of The 199th",
                   WORLD_CRAG[0], WORLD_CRAG[1], [R.page(
                       look, img=R.image(""), trigger=1, priority=0,
                       through=True)])


# ------------------------------------- 5.6: the last three jokes in the game --
def isle_plaque(event_id):
    """The Isle of Uncertain Ownership. Two parish councils, two hundred years
    of correspondence, and not one landing.

    The plaque is the accidental record again - mechanism four in NORTH.md 1.3 -
    and it does the whole job by not finishing its own sentence."""
    plaque = S.narrate([
        "A plaque, bolted to the rock, weathered",
        "almost smooth."])
    plaque += S.narrate([
        "\\C[6]THIS ISLAND IS THE PROPERTY OF\\C[0]",
        "",
        "and then a very great deal of scratching out."])
    plaque += S.narrate([
        "Above it, a flagpole, with two flags on it,",
        "one above the other.",
        "The order has been reversed nine times, by",
        "parties who could not get ashore and were",
        "shouting from boats."])
    again = S.narrate([
        "The plaque. Still nobody's."])
    return R.event(event_id, "The Isle Of Uncertain Ownership",
                   WORLD_ISLE[0] + 1, WORLD_ISLE[1], [
        R.page(plaque + [R.self_switch("A", True)], img=R.image(""),
               trigger=1, priority=0, through=True),
        R.page(again, img=R.image(""), trigger=1, priority=0, through=True,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ], note=AIR_ONLY_NOTE)


def isle_sheep(event_id):
    """The sheep, which is the joke.

    Never sheared, because shearing it would be an act of ownership and nobody
    has been able to establish ownership. It is the only party to the dispute
    that has done well out of it. `!Other1` index 2 is the stock white boulder,
    which at world-map scale is a sphere of wool with feet, and it is the best
    sheep in the library by a wide margin."""
    sheep = S.narrate([
        "A sheep.",
        "It has never been sheared. Shearing it would",
        "be an act of ownership, and ownership is the",
        "one thing nobody has managed to establish."])
    sheep += S.narrate([
        "It is, by now, very nearly a sphere.",
        "It looks at you with the calm of an animal",
        "that has never once been asked to do",
        "anything."])
    again = S.narrate([
        "The sheep has moved about a foot.",
        "It took a while."])
    return R.event(event_id, "The Sheep", WORLD_ISLE[0] + 3, WORLD_ISLE[1], [
        R.page(sheep + [R.self_switch("A", True)],
               img=R.image("!Other1", 2), trigger=1, priority=0),
        R.page(again, img=R.image("!Other1", 2), trigger=1, priority=0,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ], note=AIR_ONLY_NOTE)


def attempt_112(event_id):
    """Attempt 112, and the only gap in a hundred and ninety-nine plaques.

    It is not in the Long Field because it came down here and nobody could get
    to it, so its plaque was never written. Ott would rather have an unwritten
    plaque than a wrong one, which is the most engineer thing about her."""
    wreck = S.narrate([
        "An airship, on a rock, a hundred years dead.",
        "The envelope went long ago. The frame is",
        "still bolted to the stone it came down on."])
    wreck += S.narrate([
        "Nobody has ever been able to get out here to",
        "unbolt it, which is also why there is no",
        "plaque, and why there is a gap in a row of",
        "plaques forty miles inland."])
    wreck += S.narrate([
        "The number-plate comes off in one turn of a",
        "spanner."])
    wreck += [R.gain_item(db.IT_PLATE, 1), R.play_me("Item")]
    wreck += S.narrate([
        "Got \\I[188]\\C[3]Number-Plate, 112\\C[0]."])
    again = S.narrate([
        "Attempt 112. Everything else on her is",
        "bolted to the rock and staying there."])
    return R.event(event_id, "Attempt One Hundred And Twelve",
                   WORLD_STACK[0] + 1, WORLD_STACK[1], [
        R.page(wreck + [R.self_switch("A", True)],
               img=R.image("Vehicle", 3), trigger=1, priority=0),
        R.page(again, img=R.image("Vehicle", 3), trigger=1, priority=0,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ], note=AIR_ONLY_NOTE)


def the_bench(event_id):
    """The thing the Hermit of the Middle Distance has been looking at for
    nineteen years, with great authority, from a rock seven squares west.

    It is a hill. There is a bench on it. You sit on it and nothing happens,
    and that is the entire event, and it should be the last thing in the game
    anybody finds. NORTH.md 5.6 allows exactly one extra line if the bench on
    the mound in the east got built, and one is what it gets."""
    sit = S.narrate([
        "You sit on it.",
        "Nothing happens.",
        "The sea does what the sea does."])
    sit += R.if_then(
        R.condition_switch(db.SW_BENCH_DONE),
        S.narrate([
            "There is another one of these a long way",
            "south, facing the same water."]))

    look = S.narrate([
        "The middle distance.",
        "It is a hill. Grass, a view of the sea, and",
        "nothing else of any description whatever."])
    look += S.narrate([
        "There is a bench on it.",
        "It is older than the one on the mound in the",
        "east. It has no plaque. Nobody remembers who",
        "put it up."])
    look += R.choice_block(["Sit on it", "Stand about"], [sit, []])
    return R.event(event_id, "The Middle Distance",
                   WORLD_MIDDLE[0], WORLD_MIDDLE[1] + 2, [
        R.page(look, img=R.image(""), trigger=1, priority=0, through=True)],
        note=AIR_ONLY_NOTE)


def clause_seven(event_id):
    """Clause seven, arriving on its own, with nobody to introduce it.

    The engine does the whole joke: `Tilesets.json` refuses to let the Two
    Hundred land on the tower's step (see `build_game.TILESET_FLAGS`), so a
    party that flies here sets down on the grass and walks the last two
    squares, exactly as the Prophecy specifies and for reasons that have
    nothing to do with the Prophecy. Nothing here explains that, because 1.5's
    fourth test says an explained joke is a deleted joke.

    It is a parallel process because there is no tile to hang it on: the
    airship keeps the party on its own square when it lands, so a player-touch
    event beside the door is missed by anybody who sets down on it. The script
    condition asks the two questions that matter - is the party on foot, and is
    the Two Hundred parked within sight - so walking here overland says
    nothing, which is correct."""
    near = ("!$gamePlayer.isInVehicle() && $gameMap.airship()._mapId === %d"
            " && Math.abs($gameMap.airship().x - %d)"
            " + Math.abs($gameMap.airship().y - %d) <= 4"
            " && Math.abs($gamePlayer.x - %d)"
            " + Math.abs($gamePlayer.y - %d) <= 2"
            % (MAP_WORLD, WORLD_TOWER[0], WORLD_TOWER[1],
               WORLD_TOWER[0], WORLD_TOWER[1]))
    arrive = R.if_then(R.condition_script(near),
                       S.narrate([
                           "The Two Hundred is on the grass behind you,",
                           "ticking as she cools.",
                           "The door is two squares away.",
                           "You walk them."]) +
                       [R.control_switch(db.SW_TWO_HUNDRED_FLEW, True),
                        R.self_switch("A", True)])
    return R.event(event_id, "Clause Seven",
                   WORLD_TOWER[0] - 2, WORLD_TOWER[1] - 1, [
        R.page(arrive, img=R.image(""), trigger=4, priority=0, through=True,
               conditions={"switch1Valid": True, "switch1Id": db.SW_AIRSHIP}),
        R.page([], img=R.image(""), trigger=0, priority=0, through=True,
               conditions={"switch1Valid": True, "switch1Id": db.SW_AIRSHIP,
                           "selfSwitchValid": True, "selfSwitchCh": "A"}),
    ])


# ============================================================ the Long Field ==
# NORTH.md 5.5 and 6. One hundred and ninety-nine wrecks in rows, twelve of
# them with readable plaques, and a machine at the top of the field that has
# not been told it stopped.
#
# **What the map is, and why nothing in it says so.** The town has built a war
# cemetery for machines: wrought-iron railings on a stone plinth, a double gate
# with the works' name on it, rows in numerical order, and a plaque on each one
# saying where it was lost and what it was that failed. Not one line of
# dialogue in this file uses the word, and not one character remarks on it. It
# is a works disposal ground and everybody up here would tell you so.
#
# The rows age as you walk them, which is free: the oldest row at the gate is
# wood and ivy, the middle rows are riveted rust and corrugated iron, and the
# newest row at the top of the field is plain factory grey. Two hundred years
# of trying, told in four A3 wall autotiles.
FIELD_W, FIELD_H = 34, 32

FIELD_IN = (16, 29)             # inside the gate, where you arrive
FIELD_OUT = (16, 30)            # one south of it: the way back to the road

# The rows, oldest first, given as the y of the upper of their two wall rows.
# The plaque row is always the row directly south of the band, which is where
# a plaque is bolted and where the player stands to read it.
ROW_Y = [23, 18, 13, 8, 3]
PLAQUE_Y = [y + 2 for y in ROW_Y]

# What a wreck is made of. Two hundred years of iron under grass does not look
# like a machine from directly overhead - it looks like a heap - so that is
# what it is drawn as: a bare plot with a mound of scrap on it and one
# recognisable part standing up out of the middle, which is the thing that
# tells you the heap used to fly.
#
# Two other ways of drawing one were built and looked at first, and both were
# wrong in a way no amount of reasoning would have shown. Two rows of A3 outer
# wall - the town's retaining wall - is a **garden wall**, five to a row. Two
# rows of SF roof over one of A3 wall is a **shed**: pale slab, orange rim, a
# row of little cabins with a graveyard in front of them. The A4 free-standing
# pairs, which sound like exactly the right tool, put a *gravel* top on the
# mass, and the wood one is cream flecked with colour and reads as a flower
# bed. Screenshots, three times, and each time the answer was somewhere else.
#
# The part that stands up out of the mound is the same part every time, and
# that is not laziness: two hundred years of one works building one machine
# means a hundred and ninety-nine identical tanks in a hundred and ninety-nine
# rows, which is a better joke than variety would have been. The other pillars
# were tried and are worse in every way - `Pillar C (Machine)` on this sheet is
# a decorative column with a *figure painted on it*, which a map-scale
# screenshot renders as a pastel poster in the middle of a scrapheap.
ROW_PART = K.SF_WATER_TANK

# What the mound is made of.
#
# No `SF_IRONWORK`: Iron Materials is a stack of bright red painted girders and
# six of them to a screen is the only thing anybody looks at. And no
# `SF_BROKEN_PILLAR_METAL`, which is the one the contact sheet caught: cropped
# out of the sheet on its own, "Broken Pillar B (Metal)" is a heap of **gold
# blocks on a purple base** and at map scale it reads as treasure. It was in
# every wreck in the field.
MOUND = [K.SF_SCRAP, K.SF_SPOIL, K.SF_CRATE, K.SF_OIL_DRUM,
         K.SF_SCRAP, K.SF_SPOIL, K.SF_BARREL, K.SF_SCRAP]

# Plots, west to east, as (x, width). The gap columns between them are the
# cross-aisles, and the central pair - 16 and 17 - is the path up the field.
WEST_PLOTS = [(1, 3), (5, 4), (10, 4)]
EAST_PLOTS = [(19, 4), (24, 3), (28, 4)]

# Attempt Eighty-Four broke her moorings in the eighteen-eighties and has been
# going north ever since, at a foot or so a year, straight through four rows of
# her own kind. So the west plot of every row except the oldest is *gone*, and
# what is there instead is a hundred and forty years of gouge in the ground.
# The empty plot in row two is hers; the plaque in front of it is the only one
# in the field whose cause line was never filled in.
FURROW_X = (1, 3)
EIGHTY_FOUR = (2, 1)


def _plots(row):
    """The plots that actually have a wreck standing on them in `row`."""
    west = WEST_PLOTS if row == 0 else WEST_PLOTS[1:]
    return west + EAST_PLOTS


def _wreck(g, x, y, w, row, n):
    """One wreck: a bare plot `w` across and two rows deep, with a mound on it.

    The whole plot is registered with the Canvas as a footprint, so nothing
    written afterwards can land on one. That is not fussiness - the aisles and
    the plots are two lists a hundred lines apart, and moving the rows down by
    a single row put four heaps of weeds on four wrecks, which the Canvas
    named, at the point it happened, one by one."""
    g.fill(x, y, x + w - 1, y + 1, 0, K.SF_WASTE)
    px = x + 1 + (n % 2)
    seed = row * 7 + n * 3
    for i in range(w):
        cx = x + i
        if cx == px:
            continue
        g.set(cx, y, 3, MOUND[(seed + i) % len(MOUND)])
        g.set(cx, y + 1, 3, MOUND[(seed + i + 2) % len(MOUND)])
    g.column(px, y, 3, ROW_PART)
    g.buildings.append((x, y, w, 2, 2))


def long_field_map():
    g = K.Canvas(FIELD_W, FIELD_H, tileset=K.TS_CLANGING)
    g.fill(0, 0, FIELD_W - 1, FIELD_H - 1, 0, K.GRASS)

    # -- the ground. A cinder path up the middle from the gate, and the furrow,
    # which is not a path and has never been made into one.
    g.fill(16, 1, 17, 28, 0, K.SF_WASTE)
    g.fill(FURROW_X[0], 1, FURROW_X[1], ROW_Y[1] + 1, 0, K.SF_WASTE)

    # -- the wrecks. Bare ground first, then `autotile(0)` so the plots take
    # their edges against the grass, then the mounds on top of them.
    for row, y in enumerate(ROW_Y):
        for x, w in _plots(row):
            g.fill(x, y, x + w - 1, y + 1, 0, K.SF_WASTE)
    g.autotile(0)
    for row, y in enumerate(ROW_Y):
        for n, (x, w) in enumerate(_plots(row)):
            _wreck(g, x, y, w, row, n)

    # -- the railings, and the gate. They run about six bays either side of the
    # gate and then they stop, because a works will pay for a good gate and a
    # bit of railing where the road can see it and not for four hundred yards
    # of wrought iron round a field nobody visits.
    for x in list(range(9, 15)) + list(range(19, 25)):
        g.set(x, 28, 3, K.SF_RAILING)
    g.column(15, 26, 3, K.SF_RAILING_PIER)
    g.column(18, 26, 3, K.SF_RAILING_PIER)
    g.column(14, 27, 3, K.SF_GATE_LEAF)        # both leaves, standing open
    g.column(19, 27, 3, K.SF_GATE_LEAF)
    for x in (8, 25):                          # where the railing gives up
        g.set(x, 28, 3, K.SF_SCRAP)

    # The far boundary, which the works stopped maintaining about ninety years
    # ago and which is the same railing as the gate's, minus most of it. The
    # gap at the head of the furrow is where Attempt Eighty-Four went through.
    for x in range(FIELD_W):
        if FURROW_X[0] <= x <= FURROW_X[1]:
            g.set(x, 0, 3, K.SF_SCRAP)
        elif x % 5 != 4:
            g.set(x, 0, 3, K.SF_RAILING)

    # -- what is lying about between the rows. Plaques first, one to every
    # plot: the twelve with readable events on them are drawn no differently
    # from the rest, because a field where the readable ones look readable is a
    # field with twelve things in it rather than a hundred and ninety-nine.
    for row, y in enumerate(PLAQUE_Y):
        for x, w in _plots(row):
            g.set(x + 1, y, 3, K.SF_PLAQUE)
    g.set(2, PLAQUE_Y[1], 3, K.SF_PLAQUE)      # Eighty-Four's, on an empty plot
    g.set(9, PLAQUE_Y[1], 3, K.SF_PLAQUE)      # and the bracket with nothing in

    # Everything else goes in the aisles. The Canvas refuses anything written
    # into a wreck's footprint, which is how the first pass of this list was
    # found: moving the rows down one row moved four heaps of weeds onto four
    # envelopes, and it said so, by name, at the point it happened.
    g.scatter([(4, 22), (23, 27), (27, 17), (32, 12),
               (4, 12), (23, 7), (32, 27)], 3, K.SF_SCRAP)
    g.scatter([(9, 17), (18, 22), (27, 21), (14, 6), (23, 16), (4, 7)],
              3, K.SF_SPOIL)
    # Two stacks of new girder, both of them near the gate, because they are
    # the only things in the field that arrived rather than were left. Iron
    # Materials is painted bright red and any more of it is the only thing
    # anybody looks at.
    g.scatter([(9, 26), (23, 26)], 3, K.SF_IRONWORK)
    g.scatter([(23, 21), (14, 11), (4, 17), (32, 6), (18, 27), (27, 27)],
              3, K.SF_OIL_DRUM)
    g.scatter([(9, 6), (18, 16), (32, 16), (4, 27)], 3, K.SF_BARREL)
    g.set(27, 11, 3, K.SF_OIL_DRUM_LEAK)
    # One crate, not `SF_STACKED_CRATES`. Every two-tile prop on this
    # sheet is a *column* - a flat top cell over a crated face cell - and
    # it is drawn to stand against a wall. Free-standing in grass the
    # face cell is a wooden panel on end, and what it reads as from
    # directly above is a door somebody has left in a field.
    g.set(9, 12, 3, K.SF_CRATE)

    # -- the weeds. Nothing in here is cut and nothing in here is tidied.
    g.scatter([(0, 22), (0, 17), (0, 7), (33, 27), (33, 17), (33, 7),
               (8, 22), (13, 27), (22, 12), (26, 22), (31, 7), (5, 27),
               (20, 27), (12, 22), (26, 12), (7, 12), (21, 17)],
              3, K.SF_WEEDS)
    g.scatter([(0, 27), (33, 22), (33, 12), (0, 12), (8, 17), (26, 17),
               (13, 7), (21, 7), (12, 12), (30, 27), (3, 27)],
              3, K.SF_WEEDS_B)
    g.scatter([(8, 1), (26, 1), (13, 1), (21, 1), (30, 1), (5, 1)],
              3, K.SF_RUBBLE)

    # The head of the furrow, which is where she got to and where she is.
    g.scatter([(0, 6), (4, 6), (0, 11), (4, 11)], 3, K.SF_SCRAP)

    K.paint_regions(g, K.TS_CLANGING, 1)
    m = K.new_map(FIELD_W, FIELD_H, K.TS_CLANGING, name="The Long Field",
                  bgm="Field4", encounter_step=42,
                  # Not "Wasteland", which is a desert with cacti in it, and
                  # not "Ruins2", which is white classical colonnades under
                  # ivy. Patchy grass over bare dirt, and the hillside the
                  # town is up.
                  battleback=("Ground1", "Cliff"),
                  encounters=[(db.TR_UNNUMBERED, 5, [1]),
                              (db.TR_PRESSURE, 4, [1]),
                              (db.TR_SALVAGE, 3, [1])])
    m["data"] = g.data
    m["events"] = [None] + long_field_events()
    return m


# --------------------------------------------------------------- the plaques --
# NORTH.md 5.5. Twelve readable ones, counted in `VAR_PLAQUES`, and every cause
# mechanical, specific and plausible. Not one of them says "the Prophecy".
#
# The joke is the sequence and nothing else, so it is written into the order
# the player walks them in: the gate end of the field is 1802 and names a
# broken part every time, and by the top of the field every plate says IN
# SIGHT OF THE TOWER and every cause says UNDER REVIEW. Nobody in the game
# remarks on that. Ott will, once, and only if you have read all twelve.
def plaque(event_id, name, x, y, lines, again, count=True):
    """One plate, read once for the counter and re-readable afterwards.

    The counting page is guarded by a self switch rather than by anything
    global, so a plate cannot be read twice for two - which is the same
    discipline `story.trope()` needs and for the same reason: `VAR_PLAQUES` is
    a gate at twelve and a gate that can be walked through twice is not one."""
    first = S.narrate(lines)
    if count:
        first += [R.control_variable_add(db.VAR_PLAQUES, 1)]
    first += [R.self_switch("A", True)]
    return R.event(event_id, name, x, y, [
        R.page(first, img=R.image(""), trigger=0, priority=1,
               direction_fix=True, through=True),
        R.page(S.narrate(again), img=R.image(""), trigger=0, priority=1,
               direction_fix=True, through=True,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ])


# (x, y, name, first reading, re-reading). Twelve, in the order the field is
# walked, which is the order they were lost in.
PLAQUES = [
    (2, PLAQUE_Y[0], "Attempt Three", [
        "A brass plate, green with two hundred years of",
        "weather, on a wreck that is mostly ivy.",
        "\\C[6]ATTEMPT 3. LOST IN THIS FIELD.\\C[0]",
        "\\C[6]CAUSE: NEVER LEFT IT.\\C[0]",
        "",
        "It is the oldest plate here and the only one",
        "that gives a distance.",
        "The distance is eleven feet."],
     ["Attempt 3. Eleven feet, and then the ivy."]),

    (6, PLAQUE_Y[0], "Attempt Forty-One", [
        "\\C[6]ATTEMPT 41. LOST OVER THE WEST ROAD.\\C[0]",
        "\\C[6]CAUSE: ENVELOPE, SEAM.\\C[0]",
        "",
        "Somebody has scratched underneath it, in a",
        "different hand and a much better mood:",
        "'the seam was fine. so was he. he walked home.'"],
     ["Attempt 41. The seam was fine."]),

    (11, PLAQUE_Y[0], "Attempt Sixty", [
        "\\C[6]ATTEMPT 60. LOST OVER THE GLOAMWOOD.\\C[0]",
        "\\C[6]CAUSE: BALLAST, RELEASED IN ERROR.\\C[0]",
        "",
        "Underneath, on a plate of its own, smaller:",
        "\\C[6]ALL HANDS RECOVERED. ONE ANNOYED.\\C[0]"],
     ["Attempt 60. One annoyed."]),

    (2, PLAQUE_Y[1], "Attempt Eighty-Four's Plate", [
        "\\C[6]ATTEMPT 84. LOST OVER THE LONG FIELD.\\C[0]",
        "\\C[6]CAUSE:\\C[0]",
        "",
        "The cause line is blank.",
        "It is the only blank one in the field.",
        "",
        "The plot behind it is empty, and out of the",
        "back of it, going north, is a gouge in the",
        "ground about three feet deep and as wide as",
        "the plot."],
     ["Attempt 84. The cause line is still blank."]),

    (6, PLAQUE_Y[1], "Attempt One Hundred And One", [
        "\\C[6]ATTEMPT 101. LOST OVER THE SEA.\\C[0]",
        "\\C[6]CAUSE: FIRE, WHICH WAS EXPECTED.\\C[0]",
        "",
        "The works wrote the word FIRE on her flight",
        "plan before she left the shed, in the box",
        "headed ANTICIPATED DIFFICULTIES."],
     ["Attempt 101. Anticipated."]),

    (11, PLAQUE_Y[1], "Attempt One Hundred And Twenty-Three", [
        "\\C[6]ATTEMPT 123. LOST OVER THE STANDING STONES.\\C[0]",
        "\\C[6]CAUSE: FIRE, WHICH WAS NOT.\\C[0]"],
     ["Attempt 123. Not anticipated."]),

    (6, PLAQUE_Y[2], "Attempt One Hundred And Thirty-Seven", [
        "\\C[6]ATTEMPT 137. LOST OVER THE GLOAMWOOD.\\C[0]",
        "\\C[6]CAUSE: FRACTURE, MAIN SPAR.\\C[0]"],
     ["Attempt 137. Main spar."]),

    (11, PLAQUE_Y[2], "Attempt One Hundred And Thirty-Eight", [
        "\\C[6]ATTEMPT 138. LOST OVER THE GLOAMWOOD.\\C[0]",
        "\\C[6]CAUSE: FRACTURE, MAIN SPAR\\C[0]",
        "\\C[6]       (DIFFERENT SPAR).\\C[0]",
        "",
        "The two plates are eleven months apart."],
     ["Attempt 138. The other spar."]),

    (20, PLAQUE_Y[2], "Attempt One Hundred And Fifty-Five", [
        "\\C[6]ATTEMPT 155. LOST IN SIGHT OF THE TOWER.\\C[0]",
        "\\C[6]CAUSE: WIND.\\C[0]",
        "",
        "Somebody has underlined CAUSE: WIND twice.",
        "Somebody else, in a much later ink, has put a",
        "small question mark beside it and left it",
        "there."],
     ["Attempt 155. Wind, with a question mark."]),

    (6, PLAQUE_Y[3], "Attempt One Hundred And Seventy-Six", [
        "\\C[6]ATTEMPT 176. LOST IN SIGHT OF THE TOWER.\\C[0]",
        "\\C[6]CAUSE: NO FAULT FOUND.\\C[0]",
        "",
        "Every system was recovered, stripped and",
        "tested. Every system passed."],
     ["Attempt 176. No fault found."]),

    (11, PLAQUE_Y[3], "Attempt One Hundred And Eighty-Four", [
        "\\C[6]ATTEMPT 184. LOST IN SIGHT OF THE TOWER.\\C[0]",
        "\\C[6]CAUSE: UNDER REVIEW.\\C[0]",
        "",
        "It is the first plate in this field to say it."],
     ["Attempt 184. Under review."]),

    (6, PLAQUE_Y[4], "Attempt One Hundred And Ninety-Nine", [
        "\\C[6]ATTEMPT 199. LOST IN SIGHT OF THE TOWER.\\C[0]",
        "\\C[6]CAUSE: UNDER REVIEW.\\C[0]",
        "",
        "This plate has said UNDER REVIEW for eleven",
        "years.",
        "",
        "The plot behind it is empty. She is on a crag",
        "in the north-west, right way up, and every",
        "system aboard her still works."],
     ["Attempt 199. Eleven years of under review."]),
]


def thirteenth_plaque(event_id, x, y):
    """The gap in a hundred and ninety-nine, and what fills it.

    Attempt 112 came down on a sea stack, nobody could get out to her, and her
    plate was therefore never written - which is the point, because every other
    plate in this field names the part that failed and Ott will not guess one.
    Bring the number-plate back off the stack and it bolts straight on.

    Her reaction is written here rather than in the works, and she is not in
    it: the card behind the plate has been ready for years. She wrote out the
    entry correctly, in about eleven words, the day she gave up on getting
    anybody out there, and then had nowhere to put it."""
    empty = S.narrate([
        "Between Attempt 101 and Attempt 123 there is a",
        "gap, and standing in the gap there is a post.",
        "",
        "On the post are two brass bolts, four inches",
        "apart, with nothing between them."])
    empty += S.narrate([
        "The rows either side of it are unbroken.",
        "Whoever keeps this field has left the space."])

    fit = S.narrate([
        "The number-plate off the wreck on the sea stack",
        "goes onto the two bolts.",
        "",
        "It fits. Of course it fits."])
    fit += [R.gain_item(db.IT_PLATE, -1), R.play_me("Item"), R.wait(30)]
    fit += S.narrate([
        "There is a card behind it.",
        "It has been behind it for some years - the",
        "paper has gone the colour of the post."])
    fit += S.narrate([
        "\\C[6]ATTEMPT 112. LOST.\\C[0]",
        "\\C[6]CAUSE: LOST.\\C[0]"])
    fit += S.narrate([
        "Every other plate in this field names a part",
        "that failed.",
        "This one does not, because nobody ever got out",
        "to her to find out which part it was."])
    fit += S.narrate([
        "Somebody wrote it out, correctly, in five",
        "words, and then had nowhere to put it, and",
        "would not put up a wrong one instead."])
    fit += [R.self_switch("A", True)]

    done = S.narrate([
        "\\C[6]ATTEMPT 112. LOST.\\C[0]",
        "\\C[6]CAUSE: LOST.\\C[0]",
        "",
        "The plate is a hundred years older than the",
        "card behind it and they are the same colour",
        "now."])
    img = R.image("")
    return R.event(event_id, "The Empty Bracket", x, y, [
        R.page(empty, img=img, trigger=0, priority=1, direction_fix=True,
               through=True),
        # A page condition can hold an item, which is how the Barrow already
        # reads the flat-packed bench, and it is why Attempt 112's number-plate
        # is a key item the party keeps rather than a switch.
        R.page(fit, img=img, trigger=0, priority=1, direction_fix=True,
               through=True,
               conditions={"itemValid": True, "itemId": db.IT_PLATE}),
        R.page(done, img=img, trigger=0, priority=1, direction_fix=True,
               through=True,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ])


# ------------------------------------------------------ 6: Attempt Eighty-Four --
# NORTH.md 6. The structural rhyme with the Barrow of the Forty-Fourth, in a
# different key, and the difference is the whole reason she exists: **Ambrose
# Fitch could ask for what he wanted. Eighty-Four cannot.** She can only keep
# trying. So there is no request, no bench and no conversation, and the player
# has to decide for her with nothing to go on - which is why stopping her is a
# choice and the Forty-Fourth's fight is not.
#
# Her sprite is the airship off `Vehicle`, the same one Attempt 112 wears on
# her sea stack, because that is what she is: a flying machine, on the ground,
# pointing north.
def eighty_four(event_id):
    img = R.image("Vehicle", 3, direction=8)

    look = S.narrate([
        "The furrow ends at the top of the field, at a",
        "boundary the works stopped maintaining about",
        "ninety years ago."])
    look += S.narrate([
        "There is a machine at the end of it.",
        "Fifteen feet of iron, facing north, with a",
        "great deal of pressure in it."])
    look += S.narrate([
        "There is a number on her flank under four",
        "coats of somebody else's paint.",
        "It is eighty-four."])
    look += S.narrate([
        "She has been making herself good out of the",
        "rows either side of her since eighteen eighty-",
        "six. Nobody taught her that.",
        "Nobody could have."])
    look += S.narrate([
        "She gets a foot off the ground.",
        "Then she does not.",
        "Then she tries it again."])

    fight = [R.play_me("Shock2"), R.wait(30),
             R.battle(db.TR_84, can_escape=False, can_lose=False),
             R.control_switch(db.SW_84_BEATEN, True),
             R.fadeout_bgm(2), R.wait(60)]
    fight += S.narrate([
        "She stops.",
        "Not at once. There is a long time between the",
        "last thing that moves and the last thing that",
        "makes a noise."])
    fight += S.narrate([
        "Then the field is quiet, and it turns out it",
        "has not been quiet since before anybody now",
        "alive was born."])
    fight += S.narrate([
        "Somebody has come down from the works.",
        "She does not say anything for a while."])
    fight += S.say("Ott", [
        "She got further than any of them."])
    fight += S.say("Ott", [
        "Nobody has ever been able to work out",
        "how she was still doing it."])
    fight += S.say("Ott", [
        "I have not tried very hard."])
    fight += S.narrate([
        "You ask what happens to her now."])
    fight += S.say("Ott", [
        "She comes up the hill.",
        "There is a bay in the shed with her",
        "number over it and nothing under it, and",
        "there has been for a hundred and forty years."])
    fight += S.say("Ott", [
        "Two hundred and one.",
        "I had decided there would not be one.",
        "I had told people."])
    fight += [R.control_switch(db.SW_84_REBUILT, True)]
    fight += S.narrate([
        "She takes something off the flank with two",
        "turns of a spanner and puts it in your hand."])
    fight += [R.gain_armor(db.AR_GOVERNOR, 1), R.play_me("Item")]
    fight += S.narrate([
        "Got \\I[163]\\C[3]Governor\\C[0], given rather than taken."])
    fight += S.say("Ott", [
        "That was coming off her anyway.",
        "She never needed it."])
    fight += S.say("Ott", [
        "A hundred and forty years and she has",
        "not once run away with herself.",
        "I have a field to prove it."])
    fight += [R.self_switch("A", True)]

    cmds = look + R.choice_block(
        ["Stop her", "Leave her to it"],
        [fight,
         S.narrate([
             "You leave her to it.",
             "She gets a foot off the ground."])])

    after = S.narrate([
        "The end of the furrow.",
        "There is a rectangle of ground here that had",
        "not seen daylight since the eighteen-eighties",
        "and is not sure what to do about it."])
    return R.event(event_id, "Attempt Eighty-Four", *EIGHTY_FOUR, pages=[
        R.page(cmds, img=img, trigger=0, priority=1, direction_fix=True),
        R.page(after, img=R.image(""), trigger=0, priority=1,
               direction_fix=True, through=True,
               conditions={"switch1Valid": True, "switch1Id": db.SW_84_BEATEN}),
    ])


def long_field_events():
    evs = []

    # -- 1: the way back out to the spur road.
    out = S.narrate(["Back out to the road?"])
    out += R.choice_block(
        ["Yes", "No"],
        [[R.play_se("Move1"),
          R.transfer(MAP_WORLD, WORLD_LONG_FIELD_STEP[0],
                     WORLD_LONG_FIELD_STEP[1], 4, 0)], []])
    evs.append(R.event(1, "The Gate", FIELD_OUT[0], FIELD_OUT[1], [R.page(
        out, img=R.image(""), trigger=1, priority=0, through=True)]))

    # -- 2: the gatepost. The second number is the joke and it is exact:
    # a hundred and ninety-nine attempts, less 112 on her sea stack and 199 on
    # her crag, is a hundred and ninety-seven. Somebody keeps it up to date.
    evs.append(S.sign(2, "The Gatepost", 15, 27, [
        "Bolted to the gatepost, in letters a foot high:",
        "\\C[6]THE HOYLE WORKS\\C[0]",
        "",
        "and underneath, on a smaller plate:",
        "\\C[6]ONE HUNDRED AND NINETY-NINE ATTEMPTS.\\C[0]",
        "\\C[6]ONE HUNDRED AND NINETY-SEVEN ARE HERE.\\C[0]",
        "",
        "The second number has been re-cut four times.",
        "Somebody keeps it right."]))

    for n, (x, y, name, lines, again) in enumerate(PLAQUES):
        evs.append(plaque(3 + n, name, x, y, lines, again))

    evs.append(thirteenth_plaque(3 + len(PLAQUES), 9, PLAQUE_Y[1]))
    evs.append(eighty_four(4 + len(PLAQUES)))

    # -- the last one: `SW_LONG_FIELD`. An autorun that erases itself, in the
    # corner, exactly like Upper Clanging's weather - **not** a player-touch
    # tile inside the gate, because the path up the field is two tiles wide
    # and a player who walks up the other one never touches it.
    evs.append(R.event(5 + len(PLAQUES), "Been To The Long Field", 0, 0, [
        R.page([R.control_switch(db.SW_LONG_FIELD, True), R.erase_event()],
               img=R.image(), trigger=3, priority=0, through=True)]))
    return evs


def build():
    R.save_map(MAP_LONG_FIELD, long_field_map())
    R.save_map(MAP_CRAG, crag_map())


# =========================================== 7: the wreck of the 199th (Map 27) ==
# NORTH.md 7. Attempt 199 came down eleven years ago on a crag in the north-
# west. Everything aboard is intact. Every system is sound. She came down
# because she **stopped flying**, in sight of the tower, and started again
# about four hundred feet lower, and the crew walked home, and none of them
# will discuss it.
#
# So the dungeon is not a ruin. It is a working airship with nobody on it: the
# lamps are out, the mugs are on the mess table where they were put down, and
# the only thing broken on the whole ship is the hole the crew came out of.
# Everything the player fights in here is a system doing its job.
#
# Still aboard is the thing they meant to drop on the tower. On the works
# inventory since 1802 it is ITEM 1, and nobody has ever ticked it off.
CRAG_W, CRAG_H = 27, 26
CRAG_IN = (13, 22)              # inside the rent in her flank
CRAG_OUT = (13, 23)

CRAG_ROOMS = [(10, 3, 16, 7),        # the control car, in the bow
              (12, 8, 14, 20),       # the keel corridor, her whole length
              (3, 9, 9, 14),         # the gas cell space, and the hold
              (17, 9, 23, 14),       # the engine room
              (3, 16, 9, 20),        # the crew's quarters
              (17, 16, 23, 20),      # the mess
              (11, 21, 15, 23)]      # the rent, which is the way in
CRAG_DOORS = [(10, 11, 11, 11), (15, 11, 16, 11),
              (10, 18, 11, 18), (15, 18, 16, 18)]


def crag_map():
    g = K.Canvas(CRAG_W, CRAG_H, tileset=K.TS_CLANGING_IN)
    # Wall G (Barracks): its top is grey **corrugated** sheet, which is what
    # an airship hull looks like from directly above and is the whole reason
    # the map reads as being inside something.
    #
    # Two others were drawn and looked at first, and on a carved map the wall
    # *top* is not trim - it is the two thirds of the screen that is not room,
    # so it is the single biggest decision on the map. Wall D is called Metal
    # and its top is a green-grey mould: the hull came out as a flooded
    # cellar. Wall E (Metal, Red Rust) has the grey plate top `north.py`
    # recommends, and at hull scale the plate reads as a wall of lockers.
    g.fill(0, 0, CRAG_W - 1, CRAG_H - 1, 0, K.SF_IN_WALL_BARRACKS)
    for x1, y1, x2, y2 in CRAG_ROOMS + CRAG_DOORS:
        g.fill(x1, y1, x2, y2, 0, K.SF_METAL_FLOOR)
    # Treadplate, not `SF_GRID_FLOOR`. "Walkable grating" sounds like the
    # right floor for a keel and draws as a green-edged cage grid that is the
    # loudest thing on the map.
    #
    # The control car is the one part of her with a floor anybody sat on.
    g.fill(11, 4, 15, 6, 0, K.SF_FLOOR_WOOD)
    g.dungeon_walls(K.SF_IN_WALL_BARRACKS, K.SF_IN_FACE_BARRACKS)
    g.autotile(0)

    # -- the keel. Girders the whole length of her, which is the only reason a
    # corridor drawn from directly overhead reads as being inside anything.
    for y in (9, 13, 17):
        left, centre, right = K.SF_IN_GIRDER
        g.set(12, y, 2, left)
        g.set(13, y, 2, centre)
        g.set(14, y, 2, right)
    g.set(13, 12, 2, K.SF_IN_DRAIN)
    g.set(12, 15, 2, K.SF_IN_PIPE_V[0])
    g.set(14, 20, 2, K.SF_IN_RUBBLE)

    # -- the control car. Her instruments, her chart table, and the log.
    g.blit(11, 3, 2, (K.SF_IN_DESK_LARGE,))          # the chart table
    g.set(13, 3, 2, K.SF_IN_BULLETIN)                # the charts, pinned
    g.column(15, 3, 2, K.SF_IN_WALL_CLOCK)           # stopped at 0940
    g.set(10, 4, 2, K.SF_IN_MACHINE_C)
    g.set(16, 4, 2, K.SF_IN_VALVE)
    # The helm. "Mechanical Device" was here first and is a rack of coloured
    # somethings that reads as a bookshelf; `Machine C` is brass gears and
    # pipework, which is what a wheel is attached to.
    g.set(13, 6, 2, K.SF_IN_MACHINE_C)               # the wheel and its gearing
    g.set(11, 6, 2, K.SF_IN_STOOL)
    g.set(15, 6, 2, K.SF_IN_STOOL)
    g.set(10, 7, 2, K.SF_IN_PAPERS)
    g.set(16, 7, 2, K.SF_IN_BOOK)                    # the ship's rules, shut

    # -- the engine room. Nothing here is broken and nothing here has stopped.
    g.blit(18, 8, 2, K.SF_IN_PLUMBING)
    g.column(22, 8, 2, K.SF_IN_DUCT)
    g.set(17, 9, 2, K.SF_IN_MACHINE_C)
    g.set(23, 9, 2, K.SF_IN_MACHINE_C)
    for x in range(18, 23):
        g.set(x, 12, 2, K.SF_IN_PIPE_H)
    g.set(17, 14, 2, K.SF_IN_VALVE)
    g.set(23, 14, 2, K.SF_IN_VALVE)
    g.set(21, 14, 2, K.SF_IN_METAL_RUBBLE)
    g.set(19, 14, 2, K.SF_IN_AIR_VENT_A)

    # -- the hold, forward and to port. The gas cell space above it is empty
    # and has been since she was gassed down; what is left is the stowage.
    g.column(3, 8, 2, K.SF_IN_STEEL_SHELF)
    g.column(4, 8, 2, K.SF_IN_STEEL_SHELF)
    g.column(8, 8, 2, K.SF_IN_STEEL_SHELF)
    g.column(3, 12, 2, K.SF_IN_STACKED_CRATES)
    g.column(9, 12, 2, K.SF_IN_STACKED_CRATES)
    g.set(7, 14, 2, K.SF_IN_RUBBLE)
    g.set(4, 14, 2, K.SF_IN_PAPERS)

    # -- the crew's quarters. Four berths and a locker, along the forward
    # bulkhead. Every two-tile prop on this sheet is a *column* - star top,
    # solid foot - so it stands at the last wall row and its foot lands on the
    # first row of floor. Laid sideways instead, four berths reach across the
    # room and seal the only doorway into it, which is what happened first.
    for x in (3, 4, 8, 9):
        g.column(x, 15, 2, K.SF_IN_BED_IRON)
    g.column(6, 15, 2, K.SF_IN_DRAWERS)
    g.set(5, 20, 2, K.SF_IN_SPIDER_WEB)
    g.set(7, 20, 2, K.SF_IN_MATTRESS)
    g.set(3, 19, 2, K.SF_IN_SIDE_DESK_METAL)
    g.set(9, 19, 2, K.SF_IN_STOOL)

    # -- the mess. The mugs are still out. Nobody cleared up, because nobody
    # was doing anything wrong when they left. Table things go on layer 3, on
    # top of the table's own tile on layer 2.
    g.blit(19, 17, 2, (K.SF_IN_DESK_LARGE_B,))
    g.set(19, 17, 3, K.SF_IN_MUG)
    g.set(20, 17, 3, K.SF_IN_TEAPOT)
    g.set(21, 18, 2, K.SF_IN_TABLE)
    g.set(21, 18, 3, K.SF_IN_MUG)
    g.set(18, 19, 2, K.SF_IN_STOOL)
    g.set(22, 19, 2, K.SF_IN_STOOL)
    # The galley bench. `Kitchen Counter` was here and is a modern **electric
    # hob**, four rings and a control panel, which no map-scale screenshot was
    # ever going to show.
    g.blit(17, 16, 2, (K.SF_IN_DESK_LARGE,))
    # The galley dresser. Not `SF_IN_ODDMENTS`, which has a **living pot
    # plant** and a wound wall clock painted into its top cell: both are
    # right in a parish room and neither survives two hundred years on a
    # crag with nobody aboard.
    g.column(23, 15, 2, K.SF_IN_DRAWERS)
    # Not `SF_IN_DRIPPING`: it is bright magenta and reads as slime.
    g.set(23, 20, 2, K.SF_IN_SPIDER_WEB)

    # -- the rent. The only thing broken on the whole ship.
    g.set(11, 21, 2, K.SF_IN_METAL_RUBBLE)
    g.set(15, 21, 2, K.SF_IN_METAL_RUBBLE)
    g.set(11, 23, 2, K.SF_IN_RUBBLE)
    g.set(15, 23, 2, K.SF_IN_RUBBLE)

    K.paint_regions(g, K.TS_CLANGING_IN, 1)
    m = K.new_map(CRAG_W, CRAG_H, K.TS_CLANGING_IN,
                  name="The Wreck of the One Hundred and Ninety-Ninth",
                  bgm="Ship2", encounter_step=34,
                  # Not "Ship", which is the deck of a wooden sailing ship.
                  # Plating, in a dark battered interior.
                  battleback=("Cobblestones3", "Ruins3"),
                  encounters=[(db.TR_CRAG_MIX, 4, [1]),
                              (db.TR_SALVAGE, 4, [1]),
                              (db.TR_PRESSURE, 3, [1])])
    m["data"] = g.data
    m["events"] = [None] + crag_events()
    return m


def crag_events():
    evs = []

    out = S.narrate([
        "Out through the hole, and back down the crag?"])
    out += R.choice_block(
        ["Yes", "No"],
        [[R.play_se("Move1"),
          R.transfer(MAP_WORLD, WORLD_CRAG_STEP[0], WORLD_CRAG_STEP[1], 2, 0)],
         []])
    evs.append(R.event(1, "The Rent", CRAG_OUT[0], CRAG_OUT[1], [R.page(
        out, img=R.image(""), trigger=1, priority=0, through=True)]))

    # -- the log. The best thing on the ship, and it is seven minutes long.
    evs.append(S.sign(2, "The Log", 11, 3, [
        "The ship's log, open, on the chart table.",
        "The last page is in two hands.",
        "",
        "\\C[6]0938. TOWER IN SIGHT. ALL WELL.\\C[0]",
        "\\C[6]0939. ALL WELL.\\C[0]",
        "\\C[6]0940.\\C[0]",
        "",
        "\\C[6]0947. ON THE CRAG. ALL HANDS. NO INJURIES.\\C[0]",
        "\\C[6]0947. NOTHING TO REPORT BETWEEN 0940 AND\\C[0]",
        "\\C[6]      0947.\\C[0]",
        "",
        "Everything from the crag onwards is in the",
        "other hand, and it is the steadier of the two.",
        "Underneath it, and this is the whole of it:",
        "\\C[6]WE ARE WALKING HOME.\\C[0]"]))

    evs.append(S.sign(3, "The Charts", 13, 3, [
        "Charts, pinned four deep, all of them of the",
        "same fourteen miles.",
        "The top one has a line ruled on it from the",
        "works to the tower, and a small cross on the",
        "line, and nothing after the cross."]))

    evs.append(S.sign(4, "The Clock", 15, 3, [
        "A brass clock, screwed to the bulkhead.",
        "It is stopped at nine forty.",
        "",
        "It is a good clock. It was serviced that",
        "spring. Somebody walks out here twice a year",
        "and winds it, and it runs, and it keeps",
        "perfect time.",
        "",
        "It has been set right eleven times.",
        "It is at nine forty again."]))

    evs.append(S.sign(5, "The Wheel", 13, 6, [
        "The wheel. It turns.",
        "The linkage behind it moves the surfaces at",
        "the stern exactly as it should, eleven years",
        "after the last hand came off it."]))

    evs.append(S.sign(6, "The Engine Room", 20, 12, [
        "The engine room.",
        "There is pressure in her. There is water in",
        "the glass. The lubricators are full and the",
        "bearings are cool.",
        "",
        "Nothing in this room has failed and nothing",
        "in this room is going to."]))

    evs.append(S.sign(7, "The Berths", 4, 16, [
        "Four berths, made up.",
        "Nobody packed. There is a shirt over the end",
        "of one of them and a book face down on",
        "another, still holding its place."]))

    evs.append(S.chest(8, "The Locker", 6, 16,
                       [R.gain_item(db.IT_ELIXIR, 1),
                        R.gain_item(db.IT_LINIMENT, 3)],
                       ["The crew's locker. \\I[179]\\C[3]Elixir\\C[0] and",
                        "\\I[194]\\C[3]Works Liniment x3\\C[0], and a note",
                        "saying PUT IT BACK, which somebody did."]))

    evs.append(S.sign(9, "The Mess Table", 20, 17, [
        "The mess table. Four mugs, put down rather",
        "than emptied. A teapot with the lid off.",
        "",
        "The tea went eleven years ago. The ring it",
        "left is still exactly where the mug is."]))

    evs.append(S.chest(10, "The Stowage", 4, 12,
                       [R.gain_armor(db.AR_TROUSERS, 1),
                        R.gain_item(db.IT_HI_POTION, 3)],
                       ["Ship's stores. \\I[152]\\C[3]Sensible Trousers\\C[0]",
                        "and \\I[177]\\C[3]Strong Potion x3\\C[0].",
                        "Everything is where the manifest says."]))

    evs.append(item_one(11, 8, 12))
    return evs


def item_one(event_id, x, y):
    """The thing they meant to drop on the tower.

    Nothing in the game says what it is. The ledger will not, the crate will
    not, and Ott says the least of anybody. The icon says it plainly, which is
    the whole arrangement: the accidental record, and then the refusal."""
    crate = S.narrate([
        "Forward of the stowage, on its own, chocked,",
        "and strapped down four ways.",
        "One crate."])
    crate += S.narrate([
        "It is stencilled on all six faces.",
        "It says \\C[6]ITEM 1\\C[0]."])
    crate += S.narrate([
        "It is a good deal heavier than a crate that",
        "size has any business being."])
    take = [R.play_se("Open1"), R.gain_item(db.IT_ITEM_ONE, 1),
            R.play_me("Item")]
    take += S.narrate([
        "Got \\I[218]\\C[3]ITEM 1\\C[0].",
        "",
        "Two of you carry it. It is that sort of crate."])
    take += [R.control_switch(db.SW_ITEM_ONE_DOWN, True),
             R.self_switch("A", True)]
    crate += R.choice_block(["Take it", "Leave it strapped down"],
                            [take, S.narrate([
                                "You leave it strapped down.",
                                "It has been strapped down for eleven years",
                                "and it is very good at it."])])
    gone = S.narrate([
        "Four straps and a set of chocks, with nothing",
        "in them."])
    return R.event(event_id, "ITEM 1", x, y, [
        # `!Chest` index 6 is the plain banded wooden crate, not one of the
        # ornate treasure chests - the same sheet `story.chest` uses and the
        # same closed/open patterns, because that is what the idiom is for.
        # `!Other1` index 6 was here first and is a rack of coloured orbs on
        # pedestals; a map-scale screenshot showed a red dome in the hold and
        # nothing else about it.
        R.page(crate, img=R.image("!Chest", 6, direction=2, pattern=1),
               trigger=0, priority=1, direction_fix=True),
        R.page(gone, img=R.image("!Chest", 6, direction=2, pattern=2),
               trigger=0, priority=1, direction_fix=True,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ])


# ================================== what the field is worth, back in the works ==
# NORTH.md 5.5 and 7. Both of these are 1.7's patterns rather than edits: the
# stores ledger is a **new event** in a room that already exists, and Ott's
# three are **appended pages** on the event `north.py` already built with a
# `pages=` argument for exactly this. Not a syllable of what she already says
# is touched, and her five ladder pages and her four Two Hundred pages are all
# still reachable.
#
# They live in this file rather than in `north.py` because they are the Long
# Field's payoff and the crag's, and `NORTH.md` 11 puts the Long Field and the
# crag here. `north.py` imports them and appends them.
#
# **Page order matters and it is not obvious.** `Game_Event.refresh` takes the
# *last* page whose conditions hold and a page's conditions are ANDed with no
# NOT available, so the only way to say "and now this instead" is to make each
# page's condition strictly harder than the one before it. Ott's own self
# switches are all four spent on the ladder, so:
#
#   ... D + SW_OTT_MATERIALS    clause seven, which sets SW_CLAUSE_SEVEN
#       + VAR_PLAQUES >= 12
#   ... D + SW_CLAUSE_SEVEN     what she says afterwards - and it has to win,
#       + SW_OTT_MATERIALS      or clause seven runs every time you say hello
#   ... D + SW_OTT_MATERIALS    last, so it beats both of those while the crate
#       + holding ITEM 1        is in the party's hands, and stops beating them
#                               the moment she takes it
#
# **Being appended last is not the same as being conditioned last, and the
# difference was a content lockout.** These three sit below every page
# `north.py` built, so a condition that can hold while one of those pages still
# has something to say does not "come next" - it deletes it. Twelve plaques is
# reachable on foot before the works is even asked for a ship, so the first
# build of this section shadowed the fabric page, the handover page, the nine
# beats of the order chain and the seven of the flying chain, and reading the
# field early made SW_OTT_MATERIALS - and therefore the airship, and therefore
# the whole works questline - permanently unreachable, with no symptom beyond
# Ott saying the wrong thing forever. Reordering does not fix it; it only
# chooses which ladder gets deleted.
#
# So each of the three requires SW_OTT_MATERIALS, the last switch the flying
# chain sets and thus the one that means "Ott has nothing left owing". Order
# stops mattering: read the field first and she simply holds clause seven until
# the ship is done. The rule for anything appended here later is the same one -
# **a page appended below a ladder must require that ladder's terminal switch.**
def stores_ledger(event_id, x, y):
    """The works stores book: mechanism four, the accidental record.

    A document does not know what it is saying. This one has been ruled in
    columns and kept honestly since 1802 and it is the only thing in the game
    that will tell you what is on the crag, and it does it by arithmetic."""
    return R.event(event_id, "The Stores Book", x, y, [
        R.page(S.narrate([
            "\\C[6]THE HOYLE WORKS - STORES\\C[0]",
            "A ledger, ruled in columns, kept since 1802.",
            "",
            "Everything ever issued has a line through it."]) + S.narrate([
            "One line has no line through it.",
            "",
            "\\C[6]ITEM 1 . . . . . . . 1 OFF . . . . . 1802\\C[0]",
            "\\C[6]ISSUED 199 TIMES. RETURNED 198.\\C[0]"]) + S.narrate([
            "In the column headed DESCRIPTION, somebody",
            "wrote one thing in 1802, and four generations",
            "of this works have not improved on it.",
            "",
            "It says \\C[6]ITEM 1\\C[0]."]) +
            [R.control_switch(db.SW_ITEM_ONE_ASKED, True),
             R.self_switch("A", True)],
            img=R.image(""), trigger=0, priority=1, direction_fix=True,
            through=True),
        R.page(S.narrate([
            "\\C[6]ITEM 1 . . . . . . . 1 OFF . . . . . 1802\\C[0]",
            "Still not ticked off."]),
            img=R.image(""), trigger=0, priority=1, direction_fix=True,
            through=True,
            conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ])


def _ott(img=None):
    sheet, index = S.FACES["Ott"]
    return R.image(sheet, index, direction=2)


def ott_field_pages():
    """Clause seven, what she says afterwards, and ITEM 1 rendered down."""
    # -- 5.5. Read all twelve and she stops working. The reward is deliberately
    # not gold: Hosea already does gold-for-collectibles in the south and doing
    # it again up here would be the laziest thing in the expansion.
    clause = S.say("Ott", [
        "Twelve of them you have read."])
    clause += S.say("Ott", [
        "Go on, then. Ask me."])
    clause += S.narrate([
        "You ask why the last four all say the same",
        "three words."])
    clause += S.narrate([
        "She gets a ledger out of the drawing office",
        "that is older than the building it is in."])
    clause += S.narrate([
        "Copied onto the flyleaf, in a hand a hundred",
        "and sixty years dead, is one sentence out of a",
        "document nobody in this town has any business",
        "owning a copy of."])
    clause += S.say("Ott", [
        "\"AND THE CHOSEN ONE SHALL COME UNTO",
        "THE TOWER UPON HIS OWN TWO FEET.\""])
    clause += S.say("Ott", [
        "Clause seven."])
    clause += S.narrate([
        "Underneath it, four hands, in four inks."])
    clause += S.narrate([
        "\\C[6]does this apply to us\\C[0]",
        "\\C[6]it does not say it applies to us\\C[0]",
        "\\C[6]it does not say it does not\\C[0]"])
    clause += S.narrate([
        "The fourth is one word, in pencil, and recent.",
        "",
        "\\C[6]quite.\\C[0]"])
    clause += S.say("Ott", [
        "Great-grandmother started it to stop",
        "the Dark Lord."])
    clause += S.say("Ott", [
        "Grandmother kept it on because the town",
        "needed the work."])
    clause += S.say("Ott", [
        "Mother kept it on out of spite."])
    clause += S.say("Ott", [
        "I keep it on because I like it.",
        "I would rather be honest with you."])
    clause += S.say("Ott", [
        "Two hundred years, and we have got to",
        "\"I like it\", and I think that is fine."])
    clause += [R.control_switch(db.SW_CLAUSE_SEVEN, True)]

    # -- what she says for the rest of the game once she has. It has to be a
    # page of its own and it has to come *after* clause seven, or twelve
    # plaques means the whole speech again every time anybody says hello.
    settled = S.say("Ott", [
        "You read the field. All of it."])
    settled += S.say("Ott", [
        "Nobody reads the field.",
        "The field is for us."])
    settled += R.if_then(
        R.condition_switch(db.SW_AIRSHIP),
        S.say("Ott", ["She is outside the gate. Go on."]),
        S.say("Ott", ["Get on, then. I have a shed to fill."]))

    # -- 7. ITEM 1, rendered down. She takes the fuse out first, before
    # anything else is touched, which is the whole of what she thinks about it.
    render = S.narrate([
        "You put the crate down on the drawing office",
        "floor. It goes down like an anvil."])
    render += S.say("Ott", [
        "...",
        "Where did you get that."])
    render += S.narrate([
        "You say where."])
    render += S.say("Ott", [
        "Nobody has ever got out there."])
    render += S.narrate([
        "She looks at it for a while without touching",
        "it, which nobody has ever seen her do."])
    render += S.say("Ott", [
        "Eighteen oh two. One off.",
        "I have signed for that eleven times and",
        "never once seen it."])
    render += S.narrate([
        "She takes the fuse out of it first, before",
        "anything else on it is touched, and puts it in",
        "your hand, and does not let go of it for a",
        "moment."])
    render += [R.gain_item(db.IT_ITEM_ONE, -1),
               R.gain_armor(db.AR_FUSE, 1), R.play_me("Item")]
    render += S.narrate([
        "Got \\I[215]\\C[3]The Fuse (Removed)\\C[0]."])
    render += S.say("Ott", [
        "Right."])
    render += S.narrate([
        "The rest of it goes down the hill to",
        "Ollerenshaw's and comes back in the afternoon",
        "as eighteen pounds of casing on a shaft."])
    render += [R.gain_weapon(db.WP_NUMBER_ONE, 1), R.play_me("Item")]
    render += S.narrate([
        "Got \\I[117]\\C[3]Number One\\C[0]."])
    render += S.narrate([
        "She stamps a 1 into the head of it, out of",
        "habit, and then is quiet for a bit."])
    render += S.say("Ott", [
        "Two hundred years of this works and I",
        "have never once had that out of a field."])
    render += S.say("Ott", [
        "Take it. Please."])

    # Every one of the three carries SW_OTT_MATERIALS, and the reason is at the
    # top of this section: these pages are appended *below* the two chains
    # `north.py` built, so without it they shadow them. SW_OTT_MATERIALS is the
    # last thing the flying chain sets, which makes it the one switch that means
    # "Ott has nothing left owing" - it implies the airship, which implies the
    # handover, which implies the fabric and supersedes the order chain. On
    # `settled` it is redundant, because SW_CLAUSE_SEVEN can only be set by the
    # page above; it is written out anyway so that the rule is legible on all
    # three rather than inferable from two.
    done = {"selfSwitchValid": True, "selfSwitchCh": "D",
            "switch1Valid": True, "switch1Id": db.SW_OTT_MATERIALS}
    return [
        R.page(clause, img=_ott(), trigger=0, priority=1,
               conditions=dict(done, variableValid=True,
                               variableId=db.VAR_PLAQUES, variableValue=12)),
        R.page(settled, img=_ott(), trigger=0, priority=1,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "D",
                           "switch1Valid": True,
                           "switch1Id": db.SW_CLAUSE_SEVEN,
                           "switch2Valid": True,
                           "switch2Id": db.SW_OTT_MATERIALS}),
        R.page(render, img=_ott(), trigger=0, priority=1,
               conditions=dict(done, itemValid=True, itemId=db.IT_ITEM_ONE)),
    ]
