"""Thistlewick and everything inside it: Maps 1-7.

Map 1 is the village; Maps 2-7 are the six doors off it. Four of the six
companions are recruited indoors, one is in the square, and one is in a field,
so that finding all of them means actually walking around the place.

The layout is a cross: one road north-south from the gate, one east-west
through the market square, and a building in each quadrant.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import db
import mapkit as K
import rmmzdata as R
import story as S
from places import (MAP_VILLAGE, MAP_HOME, MAP_HALL, MAP_INN, MAP_CHAPEL,
                    MAP_SMITHY, MAP_STORE, MAP_WORLD, VILLAGE_GATE,
                    WORLD_VILLAGE_STEP)

VW, VH = 40, 36    # two rows deeper than the buildings need, so that
                   # stepping out of the smithy or Bram's front door
                   # lands on grass rather than inside the tree line

# Buildings: (x, y, w, h). The door always sits on the front wall row, which is
# the last row of the building, and `building()` returns that y.
HALL = (8, 4, 9, 7)
CHAPEL = (24, 4, 8, 7)
INN = (3, 18, 8, 6)
SMITHY = (3, 27, 7, 5)
STORE = (25, 18, 8, 5)
HOME = (25, 27, 7, 5)

HALL_DOOR = (12, HALL[1] + HALL[3] - 1)
CHAPEL_DOOR = (28, CHAPEL[1] + CHAPEL[3] - 1)
INN_DOOR = (6, INN[1] + INN[3] - 1)
SMITHY_DOOR = (6, SMITHY[1] + SMITHY[3] - 1)
STORE_DOOR = (28, STORE[1] + STORE[3] - 1)
HOME_DOOR = (28, HOME[1] + HOME[3] - 1)

GATE = VILLAGE_GATE            # the one gap in the tree line, and the way out
SQUARE = (15, 11, 24, 17)      # x1, y1, x2, y2 of the cobbled market square

# Where the player lands coming back out of each door.
OUT = {m: (d[0], d[1] + 1) for m, d in [
    (MAP_HALL, HALL_DOOR), (MAP_CHAPEL, CHAPEL_DOOR), (MAP_INN, INN_DOOR),
    (MAP_SMITHY, SMITHY_DOOR), (MAP_STORE, STORE_DOOR), (MAP_HOME, HOME_DOOR)]}

HOME_START = (8, 8)            # Bram's bed-side, where a new game begins


# ============================================================== the village ==
def village_map():
    g = K.Canvas(VW, VH)
    g.fill(0, 0, VW - 1, VH - 1, 0, K.GRASS)

    # -- roads. Drawn before the square so the square's cobbles win in the
    # middle and the dirt roads run out of it in four directions.
    g.fill(19, 2, 20, 26, 0, K.PATH)              # the main road, north-south
    g.fill(3, 14, 36, 15, 0, K.PATH)              # the cross road
    g.fill(6, 15, 6, 33, 0, K.PATH)               # west lane: inn, smithy
    g.fill(28, 15, 28, 33, 0, K.PATH)             # east lane: store, home
    g.fill(12, 11, 12, 15, 0, K.PATH)             # up to Prophecy Hall
    g.fill(28, 11, 28, 15, 0, K.PATH)             # up to the chapel
    g.fill(33, 14, 36, 15, 0, K.PATH)             # out to the pond
    g.fill(SQUARE[0], SQUARE[1], SQUARE[2], SQUARE[3], 0, K.COBBLE)

    # -- the turnip fields, which is what Thistlewick is for
    g.fill(10, 20, 17, 30, 0, K.SOIL)
    for y in range(20, 31, 2):
        g.fill(10, y, 17, y, 0, K.WHEAT)

    # -- the pond, with reeds on the near bank
    g.blob(35, 25, 3, 3, 0, K.WATER)
    g.scatter([(32, 27), (38, 23)], 0, K.REEDS)   # (32,24) is the Fisher's bank

    # -- buildings
    g.building(*HALL, wall=K.WALL_SANDBRICK, roof=K.ROOF_GOLD, wall_rows=3)
    g.building(*CHAPEL, wall=K.WALL_STONE_WHITE, roof=K.ROOF_WHITE, wall_rows=3)
    g.building(*INN, wall=K.WALL_PLANK, roof=K.ROOF_BROWN)
    g.building(*SMITHY, wall=K.WALL_STONE, roof=K.ROOF_BROWN)
    g.building(*STORE, wall=K.WALL_PLANK_LIGHT, roof=K.ROOF_GREEN)
    g.building(*HOME, wall=K.WALL_PLANK, roof=K.ROOF_BROWN)

    g.autotile(0)

    # -- shop signs and windows, hung on the front wall next to each door
    g.set(HALL_DOOR[0] - 2, HALL_DOOR[1], 3, K.SIGN_SUN)
    g.set(HALL_DOOR[0] + 2, HALL_DOOR[1], 3, K.SIGN_COIN)
    g.set(CHAPEL_DOOR[0] - 2, CHAPEL_DOOR[1], 3, K.SIGN_POTION)
    g.column(CHAPEL_DOOR[0] + 2, CHAPEL_DOOR[1] - 1, 3, K.WINDOW_GLASS)
    g.set(INN_DOOR[0] + 2, INN_DOOR[1], 3, K.SIGN_INN)
    g.set(INN_DOOR[0] - 2, INN_DOOR[1], 3, K.SIGN_MUG)
    g.set(SMITHY_DOOR[0] + 2, SMITHY_DOOR[1], 3, K.SIGN_HAMMER)
    g.set(STORE_DOOR[0] - 2, STORE_DOOR[1], 3, K.SIGN_ORB)
    g.set(STORE_DOOR[0] + 2, STORE_DOOR[1], 3, K.SIGN_RING)
    g.set(HOME_DOOR[0] - 2, HOME_DOOR[1], 3, K.WINDOW)
    for x, y in [(9, 10), (15, 10), (5, 23), (9, 23), (32, 22),
                 (26, 31), (31, 31), (4, 31), (25, 22)]:
        g.set(x, y, 3, K.WINDOW)
    for x, y in [(5, 20), (27, 20), (27, 29), (5, 29)]:
        g.set(x, y, 2, K.STOVEPIPE)

    # -- the market square
    g.blit(16, 12, 3, K.STALL)
    g.blit(22, 12, 3, K.STALL_FRUIT)
    g.column(15, 16, 3, K.LAMP)
    g.column(24, 16, 3, K.LAMP)
    g.set(18, 11, 3, K.SIGNPOST)
    g.set(14, 11, 3, K.SIGNPOST)                  # the notice board
    g.set(21, 4, 3, K.SIGNPOST)                   # the ominous sign
    g.scatter([(16, 16), (23, 16)], 3, K.BARREL)
    g.set(17, 17, 3, K.CRATE)

    # -- odds and ends around the place
    g.scatter([(11, 22), (12, 22)], 3, K.BARREL)
    g.scatter([(4, 25), (9, 25)], 3, K.CRATE)
    g.scatter([(26, 24), (31, 25)], 3, K.LOGS)
    g.scatter([(3, 33), (36, 33), (2, 16), (37, 17)], 3, K.ROCK)
    g.scatter([(13, 18), (22, 20), (33, 20), (14, 32), (24, 25)], 3, K.BUSH)
    g.scatter([(12, 19), (23, 19), (32, 21), (21, 32)], 3, K.BUSH2)
    g.scatter([(9, 16), (25, 16), (18, 19), (34, 17)], 3, K.FLOWERS)
    g.scatter([(10, 17), (26, 17), (21, 18), (35, 18)], 3, K.FLOWERS2)
    g.scatter([(11, 18), (30, 16), (17, 19)], 3, K.FLOWERS3)
    g.scatter([(34, 22), (37, 27), (33, 29)], 3, K.MUSHROOMS)
    g.set(18, 24, 3, K.SIGNPOST)                  # the scarecrow's pole

    # -- trees. Two rows deep all the way round, with one gap for the gate.
    for x in range(0, VW - 1, 2):
        if not (GATE[0] - 1 <= x <= GATE[0]):
            g.blit(x, 0, 3, K.TREE)
        g.blit(x, VH - 2, 3, K.TREE_DARK if x % 4 else K.TREE)
    for y in range(2, VH - 2, 2):
        g.blit(0, y, 3, K.TREE if y % 4 else K.TREE_DARK)
        g.blit(VW - 2, y, 3, K.TREE_DARK if y % 4 else K.TREE)
    # a couple of trees inside the village, so it is not all lawn
    for x, y in [(21, 3), (2, 11), (36, 11), (21, 22), (11, 33), (31, 33)]:
        g.blit(x, y, 3, K.TREE)

    m = K.new_map(VW, VH, K.TS_OUTSIDE, name="Thistlewick", bgm="Town1")
    m["data"] = g.data
    m["events"] = [None] + village_events()
    return m


def village_events():
    evs = []

    def add(ev):
        evs.append(ev)
        return ev

    # -- 1: the way out, and the whole first-act gate --------------------------
    leave = S.say("Gatekeeper", [
        "Right then. North road. Obligatory Tower.",
        "You'll want to be sure - it's a long walk",
        "and the scenery repeats."])
    leave += R.choice_block(
        ["Go north", "Not yet"],
        [[R.play_se("Move1"), R.control_switch(db.SW_LEFT_VILLAGE, True),
          R.transfer(MAP_WORLD, WORLD_VILLAGE_STEP[0],
                     WORLD_VILLAGE_STEP[1], 2, 0)],
         S.say("Gatekeeper", ["Very sensible. Nobody ever went north",
                              "and came back saying it was fine."])])

    too_few = S.say("Gatekeeper", [
        "Hold up. You're alone.",
        "Prophecy, section four, subsection b: a Chosen",
        "One travels with a Party. Minimum one other",
        "person. It's about the optics."])
    too_few += S.narrate(["Somebody in Thistlewick will come with you.",
                          "Probably. Ask around."])

    no_quest = S.say("Gatekeeper", [
        "Can't let you north, I'm afraid.",
        "You've not been Chosen yet. Officially.",
        "Prophecy Hall's up the road - the gold one."])

    gate_cmds = R.if_then(
        R.condition_switch(db.SW_QUEST),
        R.if_then(R.condition_script("$gameParty.size() > 1"), leave, too_few),
        no_quest)
    add(R.event(1, "North Gate", GATE[0], GATE[1], [R.page(
        gate_cmds, img=R.image(""), trigger=1, priority=0, through=True)]))

    # -- 2: the gatekeeper himself ---------------------------------------------
    keeper = S.say("Gatekeeper", [
        "Forty-seven Chosen Ones I've waved off through",
        "that gate."])
    keeper += S.narrate(["He looks north for a while."])
    keeper += S.say("Gatekeeper", ["Forty-seven."])
    keeper += S.narrate(["He does not say how many came back.",
                         "You decide not to make him."])
    add(S.npc(2, "Gatekeeper", 17, 4, keeper, "People1", 2, direction=6))

    # -- 3-8: the doors ---------------------------------------------------------
    add(S.door(3, "Prophecy Hall Door", *HALL_DOOR, MAP_HALL, *arrival(MAP_HALL)))
    add(S.door(4, "Chapel Door", *CHAPEL_DOOR, MAP_CHAPEL, *arrival(MAP_CHAPEL)))
    add(S.door(5, "Inn Door", *INN_DOOR, MAP_INN, *arrival(MAP_INN)))
    add(S.door(6, "Smithy Door", *SMITHY_DOOR, MAP_SMITHY, *arrival(MAP_SMITHY)))
    add(S.door(7, "Emporium Door", *STORE_DOOR, MAP_STORE, *arrival(MAP_STORE)))
    add(S.door(8, "Bram's Front Door", *HOME_DOOR, MAP_HOME, *arrival(MAP_HOME)))

    # -- 9: Sir Aldric, lost in the square -------------------------------------
    add(aldric_event(9, 22, 16))

    # -- 10: the fingerpost ----------------------------------------------------
    add(S.sign(10, "Fingerpost", 18, 11, [
        "\\C[6]NORTH:\\C[0] The Obligatory Tower. 200 leagues.",
        "\\C[6]SOUTH:\\C[0] The turnip fields. 40 paces.",
        "\\C[6]EAST:\\C[0] The pond. There are no fish in it.",
        "\\C[6]WEST:\\C[0] Also the turnip fields.",
        "Somebody has scratched out '200' and written",
        "'FEELS LIKE MORE'."]))

    # -- 11: the notice board --------------------------------------------------
    board = S.narrate([
        "\\C[6]THISTLEWICK NOTICE BOARD\\C[0]",
        "- LOST: one goat. Answers to Councillor.",
        "- WANTED: Chosen One. Position filled.",
        "- The well is not a wishing well. Stop it."])
    board += S.narrate([
        "- MISSING: Sir A. Pemberton-Gore, six years.",
        "  If found, point him at the north gate.",
        "  He will not go. Point anyway."])
    board += [R.self_switch("A", True)] + [S.trope()]
    add(R.event(11, "Notice Board", 14, 11, [
        R.page(board, img=R.image(""), trigger=0, priority=1,
               direction_fix=True, through=True),
        R.page(S.narrate(["Nothing new. There is never anything new."]),
               img=R.image(""), trigger=0, priority=1,
               direction_fix=True, through=True,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ]))

    # -- 12: the child who has heard about the dungeon -------------------------
    kid = S.say("Child", ["Have you HEARD? There's a DUNGEON!",
                          "To the NORTH!"])
    kid += S.narrate(["You have heard.",
                      "You will hear again."])
    kid += [S.trope(), R.self_switch("A", True)]
    add(R.event(12, "Child (dungeon rumour)", 21, 17, [
        R.page(kid, img=R.image("People2", 2, direction=2), trigger=0,
               priority=1, move_type=1, move_speed=5, move_frequency=5),
        R.page(S.say("Child", ["There's a DUNGEON! To the NORTH!"]),
               img=R.image("People2", 2, direction=2), trigger=0, priority=1,
               move_type=1, move_speed=5, move_frequency=5,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ]))

    # -- 13: the father of Chosen One #47 --------------------------------------
    old = S.say("Old Man", ["Forty-seven was my boy."])
    old += S.narrate(["He is quiet for a moment."])
    old += S.say("Old Man", [
        "Everyone tells you it's an honour.",
        "Nobody tells you it's a rota.",
        "Come back, lad. That's all. Come back."])
    old += [S.trope()]
    add(S.npc(13, "Old Man", 11, 17, old, "People4", 4))

    # -- 14/15: the dog, and the man who speaks for him ------------------------
    add(S.npc(14, "Dog", 8, 27,
              S.narrate(["\\C[6]Dog:\\C[0] Woof."]),
              "Nature", 0, move_type=1, move_frequency=2))
    interp = S.say("Neighbour", [
        "He says the north road is dangerous and you",
        "should take a coat."])
    interp += S.narrate(["The dog has not made a sound."])
    interp += S.say("Neighbour", ["He says it again. Louder."])
    add(S.npc(15, "Dog Interpreter", 9, 27, interp, "People1", 1))

    # -- 16: the farmer, who is Bram's actual boss -----------------------------
    farmer = S.say("Farmer", [
        "So you're Chosen. Marvellous. Wonderful.",
        "Who's doing the west field, then?"])
    farmer += S.narrate(["You explain about the Dark Lord."])
    farmer += S.say("Farmer", [
        "Aye, well. The west field's got weevils and",
        "the Dark Lord's got a tower. Only one of those",
        "is going to spoil my supper."])
    add(S.npc(16, "Farmer", 13, 19, farmer, "People2", 6))

    # -- 17: the scarecrow -----------------------------------------------------
    add(S.sign(17, "Scarecrow", 18, 24, [
        "A pole, a crossbeam, and Bram's old coat.",
        "Somebody has pinned a note to it reading",
        "\\C[2]CHOSEN ONE (RESERVE)\\C[0].",
        "It is, you have to admit, a contingency."]))

    # -- 18: the fisher --------------------------------------------------------
    fish = S.say("Fisher", ["Thirty-one years I've fished this pond."])
    fish += S.narrate(["There are no fish in the pond."])
    fish += S.say("Fisher", [
        "Thirty-one years.",
        "You know what keeps a man going, lad?",
        "Not catching anything, and coming back anyway."])
    fish += S.narrate(["It is, unexpectedly, the best advice",
                       "anyone gives you today."])
    # On the west bank looking out over the water. The pond itself is
    # impassable, so a Fisher standing in it is a Fisher nobody can talk to.
    add(S.npc(18, "Fisher", 32, 24, fish, "People1", 4, direction=6))

    # -- 19/20: two barrels, because someone has to say it ---------------------
    loot = S.narrate(["You look in the barrel.",
                      "You take three Potions out of the barrel.",
                      "The barrel belongs to the innkeeper."])
    loot += [R.play_se("Item1"), R.gain_item(db.IT_POTION, 3), S.trope(),
             R.self_switch("A", True)]
    add(R.event(19, "Innkeeper's Barrel", 11, 22, [
        R.page(loot, img=R.image(""), trigger=0, priority=1,
               direction_fix=True, through=True),
        R.page(S.narrate(["You have already robbed this barrel."]),
               img=R.image(""), trigger=0, priority=1, direction_fix=True,
               through=True,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ]))
    add(S.sign(20, "The Other Barrel", 12, 22, [
        "Rainwater. Half a boot.",
        "Nothing a hero could use."]))

    # -- 21: the gossip --------------------------------------------------------
    gossip = S.say("Villager", [
        "They chose you at the meeting, you know.",
        "Second vote. First vote was the goat."])
    gossip += S.narrate(["She lets that sit."])
    gossip += S.say("Villager", [
        "Goat abstained. Very dignified about it."])
    add(S.npc(21, "Gossip", 24, 16, gossip, "People1", 0, direction=4))

    # -- 22: the market stall --------------------------------------------------
    stall = S.say("Merchant", ["Fresh! Mostly!"])
    stall += R.shop([(0, db.IT_POTION, 0, 0), (0, db.IT_ANTIDOTE, 0, 0),
                     (0, db.IT_SMELLING_SALTS, 0, 0), (0, db.IT_TURNIP, 0, 0)])
    add(S.npc(22, "Market Stall", 23, 14, stall, "People2", 4, direction=8))

    # -- 23: point of no return ------------------------------------------------
    add(S.sign(23, "Ominous Sign", 21, 4, [
        "\\C[2]POINT OF NO RETURN\\C[0]",
        "Somebody has added, in smaller letters:",
        "'not really, you can come back whenever,",
        "we just like the sign'."]))

    # -- 24: the well that is not a wishing well -------------------------------
    well = S.narrate(["A well. A sign says NOT A WISHING WELL."])
    well += R.choice_block(
        ["Make a wish", "Respect the sign"],
        [S.narrate(["You wish for the Dark Lord to be dealt with",
                    "by somebody else.",
                    "Nothing happens.",
                    "The sign was right."]) + [S.trope()],
         S.narrate(["You respect the sign.",
                    "The sign does not acknowledge this."])])
    add(R.event(24, "Fountain", 17, 16, [R.page(
        well, img=R.image("!Other2", 2, direction=2), trigger=0, priority=1,
        direction_fix=True, step_anime=True, walk_anime=False)]))
    return evs


def aldric_event(event_id, x, y):
    """Sir Aldric has been circling the square for six years. He is the one
    companion you meet before you have any reason to want one."""
    pitch = S.say("Aldric", [
        "Ho there, good citizen! Sir Aldric",
        "Pemberton-Gore the Third, knight errant.",
        "I am passing through."])
    pitch += S.narrate(["He has been passing through for six years."])
    pitch += S.say("Aldric", [
        "I seek only the north gate. It moves, you see.",
        "A cunning enchantment. I shall find it."])
    pitch += S.narrate(["The north gate is forty paces north.",
                        "It has never moved."])
    pitch += S.say("Aldric", ["...Unless. Do YOU know the way?"])

    accept = S.say("Aldric", [
        "At LAST! A guide! Providence!",
        "Sir Aldric Pemberton-Gore the Third, at your",
        "service, and slightly behind you at all times."])
    accept += [S.trope()]

    decline = S.say("Aldric", [
        "Quite right. A knight does not impose.",
        "I shall continue my search.",
        "I have narrowed it down to the village."])

    full = S.say("Aldric", [
        "A full company already! Splendid discipline.",
        "I shall wait here. As I have. For six years."])

    return S.recruit(event_id, db.ALDRIC, "Aldric", x, y, "Actor3", 6,
                     pitch=pitch, accept=accept, decline=decline, full=full,
                     move_type=1)


# ================================================================ interiors ==
# Every interior is the same shape: a room in black space with a doorway cut
# through the bottom wall. Keeping the geometry in one table means the map, the
# door on the village side, and the exit event can never disagree about where
# the door is.
ROOMS = {
    #          w   h  x1  y1  x2  y2  door_x
    MAP_HOME:   (17, 15, 3, 4, 13, 10, 8),
    MAP_HALL:   (21, 18, 3, 4, 17, 13, 10),
    MAP_INN:    (19, 16, 3, 4, 15, 11, 9),
    MAP_CHAPEL: (19, 18, 3, 4, 15, 13, 9),
    MAP_SMITHY: (17, 15, 3, 4, 13, 10, 8),
    MAP_STORE:  (17, 15, 3, 4, 13, 10, 8),
}


def arrival(map_id):
    """Where the player lands coming in: just inside, on the bottom floor row."""
    _, _, _, _, _, y2, door_x = ROOMS[map_id]
    return door_x, y2


def threshold(map_id):
    """The tile in the doorway that takes you back outside - two steps down
    from the arrival tile, so entering never bounces you straight out."""
    _, _, _, _, _, y2, door_x = ROOMS[map_id]
    return door_x, y2 + 2


def room(map_id, **kw):
    w, h, x1, y1, x2, y2, door_x = ROOMS[map_id]
    return K.interior(w, h, x1, y1, x2, y2, door_x=door_x, **kw)


def finish(map_id, g, name, bgm, battleback, events):
    w, h = ROOMS[map_id][0], ROOMS[map_id][1]
    m = K.new_map(w, h, K.TS_INSIDE, name=name, bgm=bgm, battleback=battleback)
    m["data"] = g.data
    m["events"] = [None] + events
    return m

def home_map():
    """Where a new game starts: Bram's one room, his bed, and his mother."""
    g = room(MAP_HOME, floor=K.IN_WOOD_FLOOR, floor_alt=K.IN_DARK_WOOD)
    g.column(4, 4, 2, K.IN_BED)                     # Bram's bed
    g.column(6, 3, 2, K.IN_CABINET)
    g.column(13, 3, 2, K.IN_SHELF_JARS)             # the pantry
    g.blit(9, 3, 2, K.IN_FIREPLACE)
    g.set(12, 4, 2, K.IN_POT)
    g.scatter([(4, 9), (5, 9)], 2, K.IN_SACK)
    g.set(12, 9, 2, K.IN_CRATE)
    g.set(11, 6, 2, K.IN_TABLE_ROUND)
    g.set(11, 6, 3, K.INC_MEAL)
    g.set(12, 6, 2, K.IN_TABLE_SMALL)
    g.set(7, 6, 2, K.IN_TABLE_SMALL)
    g.set(7, 6, 3, K.INC_CANDLES)
    return finish(MAP_HOME, g, "Bram's House", bgm="Town2",
                  battleback=("Wood1", "Room1"), events=home_events())
def home_events():
    evs = [S.exit_tile(1, "Front Door", *threshold(MAP_HOME), MAP_VILLAGE, *OUT[MAP_HOME])]

    # The bed you woke up in, which is also the game's save point and its inn.
    bed = S.narrate(["Your bed. Still warm.",
                     "You were in it when they voted."])
    bed += R.choice_block(
        ["Sleep", "Get on with it"],
        [[R.fadeout_screen(), R.play_me("Inn1"), R.recover_all(), R.wait(60),
          R.fadein_screen()] + S.narrate(["You wake up.",
                                          "You are still the Chosen One."]),
         S.narrate(["You get on with it."])])
    # Same as characters, not below: the bed tiles block, so nobody can ever
    # stand on this one, and an action-button event is only triggered from the
    # tile it is standing on unless its priority is normal.
    evs.append(R.event(2, "Bram's Bed", 4, 5, [R.page(
        bed, img=R.image(""), trigger=0, priority=1, direction_fix=True,
        through=True)]))

    # Mother, who has the sword above the fireplace and the whole opening beat.
    intro = S.say("Mother", [
        "Bram. There are eleven people outside and",
        "one of them has a scroll."])
    intro += S.say("Mother", ["You've been Chosen."])
    intro += S.narrate([
        "You point out that you were asleep.",
        "You point out that you grow turnips.",
        "You point out several things."])
    intro += S.say("Mother", [
        "I know, love.",
        "Go and see the Elder. Then take the sword",
        "off the wall. It's been up there a hundred",
        "years waiting for exactly this, and frankly",
        "it has been unbearable about it."])
    evs.append(S.npc(3, "Mother", 10, 8, intro, "People1", 5, direction=8))

    # The sword over the fireplace: available once the Elder has said the words.
    take = S.narrate([
        "The sword comes off the wall with a sound",
        "you can only describe as smug."])
    take += [R.play_me("Item"), R.gain_weapon(db.WP_SWORD, 1)]
    take += S.narrate(["Got \\I[98]\\C[3]Village Sword\\C[0]!",
                       "Equip it. It has waited a century",
                       "and it will not be gracious about waiting longer."])
    take += [S.trope(), R.self_switch("A", True)]
    # The sword hangs on the wall at (10,3), but the fireplace fills (9-11,
    # 3-4) and blocks, so nobody can stand next to the wall tile. The event
    # goes on the fireplace's lower half instead - the tile the player faces
    # when they walk up to the hearth.
    evs.append(R.event(4, "Sword Over The Fireplace", 10, 4, [
        R.page(take, img=R.image(""), trigger=0, priority=1,
               direction_fix=True, through=True),
        R.page(S.narrate(["A clean rectangle of wall where a sword",
                          "used to be."]),
               img=R.image(""), trigger=0, priority=1, direction_fix=True,
               through=True,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ]))

    evs.append(S.prop(5, "Pantry Shelf", 13, 4, [
        "Jars. Preserves. Four kinds of turnip.",
        "You take some turnips, because they are yours."],
        "", 0, extra=[R.gain_item(db.IT_TURNIP, 5), R.play_se("Item1")]))

    evs.append(S.sign(6, "Family Portrait", 8, 3, [
        "Six generations of Thistles, all holding",
        "turnips.",
        "Not one of them is holding a sword.",
        "You are going to be the odd one out."]))
    return evs


def hall_map():
    """Prophecy Hall: the Committee, the Elder, and the paperwork that turns
    out to be the actual antagonist."""
    g = room(MAP_HALL, floor=K.IN_SANDSTONE,
             wall_top=K.IN_WALL_TOP_TAN, wall_face=K.IN_WALL_FACE_TAN)
    g.fill(8, 5, 12, 12, 0, K.IN_RED_CARPET)
    g.autotile(0)
    for x in (5, 15):
        g.column(x, 3, 2, K.IN_PILLAR)
        g.column(x, 8, 2, K.IN_PILLAR)
    g.column(10, 2, 2, K.IN_STAINED_GLASS)
    g.column(7, 3, 2, K.IN_BOOKCASE)
    g.column(13, 3, 2, K.IN_BOOKCASE2)
    g.column(4, 3, 2, K.IN_NOTICE_BOARD)
    g.column(16, 3, 2, K.IN_CURTAIN_GREEN)
    g.set(9, 6, 2, K.IN_TABLE_ROUND)
    g.set(9, 6, 3, K.INC_SCROLL)
    g.set(11, 6, 2, K.IN_TABLE_ROUND)
    g.set(11, 6, 3, K.INC_BOOK)
    g.scatter([(6, 12), (14, 12)], 2, K.INC_CANDLES)
    g.scatter([(4, 13), (16, 13)], 2, K.INC_PLANT)
    return finish(MAP_HALL, g, "Prophecy Hall", bgm="Scene2",
                  battleback=("Stone1", "Castle1"), events=hall_events())
def hall_events():
    evs = [S.exit_tile(1, "Hall Door", *threshold(MAP_HALL), MAP_VILLAGE, *OUT[MAP_HALL])]

    # -- the Elder: the quest-giver, and the one who explains the rules --------
    first = S.say("Elder Wispel", [
        "Bram Thistle. The Forty-Eighth."])
    first += S.narrate([
        "Elder Wispel unrolls a scroll. It keeps",
        "unrolling. It reaches the far wall."])
    first += S.say("Elder Wispel", [
        "The Prophecy of Thistlewick. Every hundred",
        "years the Dark Lord rises in the Obligatory",
        "Tower. Every hundred years we send someone.",
        "It has worked forty-seven times."])
    first += S.narrate(["You ask what happened the other times."])
    first += S.say("Elder Wispel", [
        "It has worked forty-seven times."])
    first += S.narrate([
        "He rolls the scroll back up. It takes a while.",
        "Nobody helps."])
    first += S.say("Elder Wispel", [
        "Take companions. Up to three - that is the",
        "clause, not my preference. Then go north.",
        "Kill the Dark Lord. Come home.",
        "In that order, ideally."])
    first += [R.play_me("Mystery"), R.control_switch(db.SW_QUEST, True),
              R.gain_item(db.IT_PROPHECY, 1), R.gain_gold(500),
              R.gain_item(db.IT_POTION, 3)]
    first += S.narrate([
        "Got \\I[143]\\C[3]The Prophecy\\C[0], 500\\G,",
        "and \\I[176]\\C[3]Potion x3\\C[0]."])
    first += S.say("Elder Wispel", [
        "The gold is from the parish fund.",
        "The potions are from the parish fund.",
        "The prophecy is, regrettably, free."])
    first += [S.trope()]

    again = S.say("Elder Wispel", [
        "Still here? Take up to three companions and",
        "go north. The gate is where it has always been,",
        "whatever Sir Aldric tells you."])

    evs.append(R.event(2, "Elder Wispel", 10, 5, [
        R.page(first, img=R.image("People1", 6, direction=2), trigger=0,
               priority=1),
        R.page(again, img=R.image("People1", 6, direction=2), trigger=0,
               priority=1,
               conditions={"switch1Valid": True, "switch1Id": db.SW_QUEST}),
    ]))

    # -- the clerk: roster amendments, i.e. swapping a companion out ----------
    clerk = S.say("Clerk", [
        "Roster amendments. Form C-12.",
        "You may strike one companion from the",
        "roster. They will go home. They will not",
        "hold it against you. Much."])
    clerk += S.roster_amendment()
    evs.append(S.npc(3, "Committee Clerk", 7, 8, clerk, "People2", 0,
                     direction=6))

    # -- the Committee, still arguing about the wording -----------------------
    arg1 = S.say("Councillor", [
        "'Shall be slain' or 'shall be defeated'?",
        "Because 'slain' is a commitment."])
    evs.append(S.npc(4, "Committee Member (Wording)", 13, 8, arg1,
                     "People1", 3, direction=4))

    arg2 = S.say("Councillor Fenn", [
        "I keep saying it. Clause twelve is the problem.",
        "'THE DARK LORD SHALL RISE AGAIN.'",
        "That's not a warning. That's a subscription."])
    arg2 += S.narrate(["Nobody is listening to him.",
                       "Remember him."])
    arg2 += [S.trope()]
    evs.append(S.npc(5, "Committee Member (Clause Twelve)", 14, 11, arg2,
                     "People4", 2, direction=4))

    evs.append(S.sign(6, "The Wall of the Forty-Seven", 4, 4, [
        "Forty-seven portraits.",
        "Forty-six of them are looking at the viewer.",
        "One of them is looking at the door."]))

    evs.append(S.prop(7, "Committee Records", 7, 4, [
        "Minutes of the meeting at which you were",
        "Chosen. Under 'apologies for absence':",
        "your name, and one goat."], "", 0, extra=[S.trope()]))
    return evs


def inn_map():
    """The Gilded Turnip. Zephyrine drinks here; Piper performs here, at
    everyone."""
    g = room(MAP_INN, floor=K.IN_WOOD_FLOOR, floor_alt=K.IN_DARK_WOOD)
    g.blit(12, 3, 2, K.IN_FIREPLACE)
    g.column(4, 3, 2, K.IN_SHELF_BOTTLES)
    g.column(5, 3, 2, K.IN_CABINET)
    g.column(6, 3, 2, K.IN_SHELF_FRUIT)
    g.blit(8, 3, 2, K.IN_PIANO)
    g.column(7, 3, 2, K.IN_SHELF_JARS)
    g.set(4, 5, 3, K.INC_BOTTLES)
    g.set(5, 5, 3, K.INC_GOBLET)
    for tx, ty in [(6, 9), (12, 9), (12, 6)]:
        g.set(tx, ty, 2, K.IN_TABLE_ROUND)
    g.set(5, 9, 2, K.IN_TABLE_SMALL)
    g.set(13, 9, 2, K.IN_TABLE_SMALL)
    g.set(12, 9, 3, K.INC_MEAL2)
    g.set(12, 6, 3, K.INC_GOBLET)
    g.set(6, 9, 3, K.INC_BOTTLE)
    g.column(14, 4, 2, K.IN_BED_ORANGE)
    g.column(15, 4, 2, K.IN_BED_BROWN)
    g.set(4, 10, 2, K.IN_BARREL)
    g.set(4, 11, 2, K.IN_BARREL2)
    return finish(MAP_INN, g, "The Gilded Turnip", bgm="Town3",
                  battleback=("Wood1", "Room1"), events=inn_events())
def inn_events():
    evs = [S.exit_tile(1, "Inn Door", *threshold(MAP_INN), MAP_VILLAGE, *OUT[MAP_INN])]

    rest = S.say("Innkeeper", [
        "Bed's 20 crowns. Includes breakfast.",
        "Breakfast is turnip."])
    rest += R.choice_block(
        ["Stay the night (20cr)", "No thanks"],
        [R.if_then(
            R.condition_script("$gameParty.gold() >= 20"),
            [R.lose_gold(20), R.fadeout_screen(), R.play_me("Inn1"),
             R.recover_all(), R.wait(90), R.fadein_screen()] +
            S.narrate(["The party wakes restored.",
                       "Breakfast was turnip."]) + [S.trope()],
            S.say("Innkeeper", ["Come back when you've got 20."]))],
        cancel=None)
    evs.append(S.npc(2, "Innkeeper", 5, 7, rest, "People2", 3, direction=2))

    evs.append(zephyrine_event(3, 12, 7))
    evs.append(piper_event(4, 9, 6))

    drunk = S.say("Regular", [
        "Chosen One, eh? My cousin was a Chosen One."])
    drunk += S.narrate(["He drinks."])
    drunk += S.say("Regular", ["Number thirty-nine."])
    drunk += S.narrate(["He drinks again."])
    drunk += S.say("Regular", ["Lovely tower, apparently."])
    evs.append(S.npc(5, "Regular", 6, 10, drunk, "People4", 6, direction=8))

    evs.append(S.prop(6, "The Turnip", 13, 9, [
        "A single turnip on a plinth, painted gold.",
        "A small plaque reads: THE GILDED TURNIP.",
        "It is not a metaphor. It is just a turnip",
        "somebody painted."], "", 0, extra=[S.trope()]))
    return evs


def zephyrine_event(event_id, x, y):
    pitch = S.say("Zephyrine", [
        "Don't. Whatever it is, don't."])
    pitch += S.narrate([
        "Zephyrine Vance has been 'just passing through'",
        "Thistlewick for eleven years."])
    pitch += S.say("Zephyrine", [
        "I was expelled from the Collegium Arcanum.",
        "The enquiry used the phrase 'an unsanctioned",
        "quantity of fire'. Twice."])
    pitch += S.narrate(["You ask what happened to the Dean."])
    pitch += S.say("Zephyrine", [
        "The Dean is FINE. The DUCK is fine.",
        "Everyone is FINE."])
    pitch += S.narrate(["She drinks."])
    pitch += S.say("Zephyrine", ["...What sort of quest?"])

    accept = S.say("Zephyrine", [
        "A tower. With a Dark Lord in it.",
        "That's the most fire-adjacent thing anyone",
        "has said to me in eleven years.",
        "Give me my hat."])
    accept += [S.trope()]

    decline = S.say("Zephyrine", [
        "Fine. Wonderful. I'll be here.",
        "I'm always here. That's the whole problem."])

    full = S.say("Zephyrine", [
        "You've got three already? And none of them",
        "can set anything on fire?",
        "Bold. Genuinely bold."])
    return S.recruit(event_id, db.ZEPH, "Zephyrine", x, y, "Actor1", 5,
                     pitch=pitch, accept=accept, decline=decline, full=full)


def piper_event(event_id, x, y):
    pitch = S.narrate([
        "A bard is standing on a table.",
        "She is describing you, out loud, in the third",
        "person, as you approach."])
    pitch += S.say("Piper", [
        "'And lo, the Chosen One drew near, smelling",
        "faintly of turnip, and the tavern fell silent -'"])
    pitch += S.narrate(["The tavern has not fallen silent.",
                        "The tavern is ignoring her."])
    pitch += S.say("Piper", [
        "Piper Quill. Chronicler. I do the songs.",
        "You do the sword bit. It's a good system."])

    accept = S.say("Piper", [
        "'And she went WITH him, and it was...'",
        "Hold on. I need a rhyme for 'turnip'.",
        "I'll get one on the road. I always do."])
    accept += [S.trope()]

    decline = S.say("Piper", [
        "Unchronicled, then. Very brave.",
        "Nobody will ever know how brave."])

    full = S.say("Piper", [
        "Four's a crowd, chronicle-wise.",
        "Hard to rhyme four names. Ask anyone."])
    return S.recruit(event_id, db.PIPER, "Piper", x, y, "Actor2", 3,
                     pitch=pitch, accept=accept, decline=decline, full=full)


def chapel_map():
    """The Chapel of Whatever Works. Merribell's, and the only place in the
    village with an organ and a strong opinion about water."""
    g = room(MAP_CHAPEL, floor=K.IN_DIAMOND_TILE,
             wall_top=K.IN_WALL_TOP_WHITE, wall_face=K.IN_WALL_FACE_WHITE)
    g.fill(8, 4, 10, 12, 0, K.IN_RED_CARPET)
    g.autotile(0)
    g.blit(12, 3, 2, K.IN_ORGAN)
    g.column(9, 2, 2, K.IN_STAINED_GLASS)
    g.column(4, 3, 2, K.IN_BOOKCASE)
    g.column(14, 7, 2, K.IN_SHELF_JARS)
    for y in (7, 9, 11):
        for x in (5, 6, 12, 13):
            g.set(x, y, 2, K.IN_TABLE_SMALL)
    g.scatter([(5, 4), (13, 4)], 2, K.INC_CANDLES)
    g.scatter([(4, 12), (15, 12)], 2, K.INC_PLANT2)
    g.set(9, 5, 2, K.IN_TABLE_ROUND)
    g.set(9, 5, 3, K.INC_BELL)
    return finish(MAP_CHAPEL, g, "Chapel of Whatever Works", bgm="Scene4",
                  battleback=("Stone1", "Castle1"), events=chapel_events())
def chapel_events():
    evs = [S.exit_tile(1, "Chapel Door", *threshold(MAP_CHAPEL), MAP_VILLAGE, *OUT[MAP_CHAPEL])]
    evs.append(merribell_event(2, 9, 6))

    heal = S.narrate([
        "A basin of clean water and a hand-lettered sign:",
        "'FREE. DRINK IT. YOU ARE DEHYDRATED. YES YOU.'"])
    heal += [R.play_me("Refresh"), R.recover_all()]
    heal += S.narrate(["The party is restored.",
                       "You feel obscurely told off."])
    heal += [S.trope()]
    evs.append(R.event(3, "Basin", 14, 8, [R.page(
        heal, img=R.image(""), trigger=0, priority=1, direction_fix=True)]))

    evs.append(S.sign(4, "The Creed", 4, 4, [
        "\\C[6]THE CREED OF WHATEVER WORKS\\C[0]",
        "1. Try the obvious thing.",
        "2. If the obvious thing works, it was correct.",
        "3. There is no rule three. Rule three was",
        "   getting in the way."]))

    evs.append(S.prop(5, "The Organ", 13, 5, [
        "A pipe organ. Sister Merribell plays it",
        "at people who look tired.",
        "You press one key. The note goes on for",
        "considerably longer than you expected."],
        "", 0, extra=[R.play_me("Organ")]))
    return evs


def merribell_event(event_id, x, y):
    pitch = S.say("Merribell", [
        "Sit down. When did you last drink water?"])
    pitch += S.narrate(["You try to explain about the prophecy."])
    pitch += S.say("Merribell", [
        "That wasn't the question. Water. When."])
    pitch += S.narrate([
        "Sister Merribell of the Order of Whatever Works.",
        "The Order holds that theology is a distraction",
        "from the actual problem, and that the actual",
        "problem is usually simpler than you want it",
        "to be."])
    pitch += S.say("Merribell", [
        "Right. A tower, a Dark Lord, and a boy who",
        "hasn't had a glass of water since Tuesday.",
        "Someone should go with you."])

    accept = S.say("Merribell", [
        "I'm bringing the basin. Don't argue.",
        "Nobody has ever won an argument with me",
        "about hydration and I am not starting a",
        "losing streak on a Thursday."])
    accept += [S.trope()]

    decline = S.say("Merribell", [
        "Then take this, and drink it before the gate.",
        "I will know if you don't."])
    decline += [R.gain_item(db.IT_POTION, 1), R.play_se("Item1")]
    decline += S.narrate(["Got \\I[176]\\C[3]Potion\\C[0]."])

    full = S.say("Merribell", [
        "Three already. Good. One of them had better",
        "know first aid.",
        "...None of them know first aid, do they."])
    return S.recruit(event_id, db.MERRI, "Merribell", x, y, "Actor1", 7,
                     pitch=pitch, accept=accept, decline=decline, full=full)


def smithy_map():
    """Grumnir's Smithy: weapons, armour, and a man who talks to hammers."""
    g = room(MAP_SMITHY, floor=K.IN_COBBLE,
             wall_top=K.IN_WALL_TOP_STONE, wall_face=K.IN_WALL_FACE_STONE)
    g.blit(10, 3, 2, K.IN_FIREPLACE)
    g.column(4, 3, 2, K.IN_SWORD_RACK)
    g.column(6, 3, 2, K.IN_SWORD_RACK)
    g.column(13, 3, 2, K.IN_CABINET)
    g.scatter([(4, 9), (5, 9)], 2, K.IN_CRATE)
    g.scatter([(12, 9), (13, 9)], 2, K.IN_BARREL)
    g.scatter([(11, 6), (12, 6)], 2, K.INC_ARMOR_STAND)
    g.column(8, 3, 2, K.IN_SHELF_BOTTLES)
    g.set(5, 5, 2, K.IN_TABLE_ROUND)
    g.set(5, 5, 3, K.INC_CANDLES)
    return finish(MAP_SMITHY, g, "Grumnir's Smithy", bgm="Town4",
                  battleback=("Stone1", "Room1"), events=smithy_events())
def smithy_events():
    evs = [S.exit_tile(1, "Smithy Door", *threshold(MAP_SMITHY), MAP_VILLAGE, *OUT[MAP_SMITHY])]
    evs.append(hob_event(2, 8, 5))

    shop = S.narrate(["Hob's apprentice minds the counter.",
                      "She does not talk to the hammers.",
                      "She says this often, and with feeling."])
    shop += R.shop([
        (1, db.WP_SWORD, 0, 0), (1, db.WP_BROADSWORD, 0, 0),
        (1, db.WP_STAFF, 0, 0), (1, db.WP_SLEDGE, 0, 0),
        (1, db.WP_WAND, 0, 0), (1, db.WP_DIRK, 0, 0),
        (1, db.WP_HALBERD, 0, 0), (1, db.WP_FIDDLE, 0, 0),
        (2, db.AR_LEATHER, 0, 0), (2, db.AR_CHAIN, 0, 0),
        (2, db.AR_ROBE, 0, 0), (2, db.AR_SILK, 0, 0),
        (2, db.AR_BUCKLER, 0, 0), (2, db.AR_KITE_SHIELD, 0, 0),
        (2, db.AR_HAT, 0, 0), (2, db.AR_HELM, 0, 0),
    ])
    evs.append(S.npc(3, "Apprentice", 11, 8, shop, "People2", 7, direction=4))

    evs.append(S.prop(4, "Beatrice", 5, 5, [
        "A hammer, resting on the anvil.",
        "Somebody has scratched BEATRICE into the haft.",
        "You are almost certain it did not just move."],
        "", 0, extra=[S.trope()]))
    return evs


def hob_event(event_id, x, y):
    pitch = S.say("Hob", [
        "Hold on. Beatrice is talking."])
    pitch += S.narrate([
        "Hob Grumnir holds a hammer to his ear.",
        "The hammer does not talk. Hammers do not talk."])
    pitch += S.say("Hob", [
        "She says you're the forty-eighth.",
        "She says the last one came in here for a",
        "sword and I gave him a good one and it",
        "didn't help."])
    pitch += S.narrate(["He puts the hammer down carefully."])
    pitch += S.say("Hob", [
        "She says a sword's no good on its own.",
        "She says somebody's got to swing it who",
        "knows what breaks."])

    accept = S.say("Hob", [
        "Right. Beatrice comes. I come with Beatrice.",
        "That's the arrangement and it's not up for",
        "discussion, mainly because she'd win."])
    accept += [R.gain_weapon(db.WP_HAMMER, 1), R.play_se("Item1")]
    accept += S.narrate(["Got \\I[113]\\C[3]Shop Hammer\\C[0]."])
    accept += [S.trope()]

    decline = S.say("Hob", [
        "Suit yourself. Mind the anvil on the way out.",
        "Not for your sake. For the anvil's."])

    full = S.say("Hob", [
        "Full up. Beatrice says that's a shame.",
        "Beatrice says a lot of things."])
    return S.recruit(event_id, db.HOB, "Hob", x, y, "Actor2", 4,
                     pitch=pitch, accept=accept, decline=decline, full=full)


def store_map():
    """Nix's Emporium of Previously Owned Goods."""
    g = room(MAP_STORE, floor=K.IN_WOOD_FLOOR, floor_alt=K.IN_DARK_WOOD)
    for x in (4, 5, 6):
        g.column(x, 3, 2, K.IN_SHELF_GOODS)
    for x in (10, 11, 12):
        g.column(x, 3, 2, K.IN_SHELF_BOTTLES)
    g.column(7, 3, 2, K.IN_SHELF_FRUIT)
    g.column(8, 3, 2, K.IN_SHELF_JARS)
    g.scatter([(4, 9), (5, 9), (12, 9)], 2, K.IN_CRATE2)
    g.scatter([(13, 5), (13, 8)], 2, K.IN_BARREL2)
    g.set(4, 6, 2, K.IN_TABLE_SMALL)
    g.set(4, 6, 3, K.INC_BASKET)
    g.set(12, 6, 2, K.IN_TABLE_SMALL)
    g.set(12, 6, 3, K.INC_POTION_RED)
    g.set(9, 5, 2, K.INC_POTION_BLUE)
    g.set(6, 5, 2, K.INC_POTION_GREEN)
    return finish(MAP_STORE, g, "Nix's Emporium", bgm="Town2",
                  battleback=("Wood1", "Room1"), events=store_events())
def store_events():
    evs = [S.exit_tile(1, "Emporium Door", *threshold(MAP_STORE), MAP_VILLAGE, *OUT[MAP_STORE])]

    shop = S.say("Shopkeeper", [
        "Everything here is previously owned.",
        "By whom, we don't ask. That's the arrangement."])
    shop += R.shop([
        (0, db.IT_POTION, 0, 0), (0, db.IT_HI_POTION, 0, 0),
        (0, db.IT_TONIC, 0, 0), (0, db.IT_ETHER, 0, 0),
        (0, db.IT_FEATHER, 0, 0), (0, db.IT_ANTIDOTE, 0, 0),
        (0, db.IT_SMELLING_SALTS, 0, 0),
        (2, db.AR_BOOTS, 0, 0), (2, db.AR_RING_LUCK, 0, 0),
        (2, db.AR_RING_SPEED, 0, 0), (2, db.AR_AMULET, 0, 0),
        (2, db.AR_CIRCLET, 0, 0),
    ])
    evs.append(S.npc(2, "Shopkeeper", 5, 8, shop, "People4", 3, direction=6))

    evs.append(nix_event(3, 11, 5))

    evs.append(S.prop(4, "The Ledger", 8, 4, [
        "A ledger. Every entry reads 'ACQUIRED'.",
        "None of them say from where.",
        "One entry, in a different hand, reads",
        "'PLEASE STOP WRITING ACQUIRED'."],
        "", 0, extra=[S.trope()]))
    return evs


def nix_event(event_id, x, y):
    pitch = S.narrate([
        "Somebody is in the back room, doing an",
        "inventory of things that are not on the",
        "inventory."])
    pitch += S.say("Nix", [
        "Nix. Acquisitions.",
        "Before you ask: no. I locate things.",
        "Ahead of schedule. On behalf of a client",
        "who has not yet been identified."])
    pitch += S.narrate(["You did not ask."])
    pitch += S.say("Nix", [
        "Everyone asks eventually. I like to get ahead",
        "of it. Same as everything else."])

    accept = S.say("Nix", [
        "A tower nobody's been inside for a hundred",
        "years, full of things nobody's counted.",
        "Say no more. Genuinely, say no more, I've",
        "already got my coat."])
    accept += [S.trope()]

    decline = S.say("Nix", [
        "Fair. Check your pockets before you go.",
        "Not accusing. Just a good habit."])

    full = S.say("Nix", [
        "Three's a good number. Small, quiet, splits",
        "four ways.",
        "...Four ways?"])
    return S.recruit(event_id, db.NIX, "Nix", x, y, "Actor3", 4,
                     pitch=pitch, accept=accept, decline=decline, full=full)


def build():
    R.save_map(MAP_VILLAGE, village_map())
    R.save_map(MAP_HOME, home_map())
    R.save_map(MAP_HALL, hall_map())
    R.save_map(MAP_INN, inn_map())
    R.save_map(MAP_CHAPEL, chapel_map())
    R.save_map(MAP_SMITHY, smithy_map())
    R.save_map(MAP_STORE, store_map())
