"""Everything north of the gate: Maps 8-12.

    8   The World, Roughly            the overworld, with encounters
    9   The Gloamwood                 a forest maze
    10  The Bit With The Thing        the wood's far half, and its boss
    11  The Obligatory Tower          the dungeon
    12  The Obligatory Tower, Summit  Grimspite, and then the real last boss

The route is a straight line with one fork: the mountains only have one gap in
them, and the gap is full of trees, so the Gloamwood is not optional. Everything
else - chests, the mimic, the shrine - is off to the side.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import db
import mapkit as K
import rmmzdata as R
import story as S
import wilds as W
import field as F
from places import (MAP_VILLAGE, MAP_WORLD, MAP_GLOAMWOOD, MAP_GLOAM_DEEP,
                    MAP_TOWER, MAP_SUMMIT, VILLAGE_GATE, WORLD_VILLAGE,
                    WORLD_VILLAGE_STEP, WORLD_GLOAMWOOD, WORLD_TOWER)

WW, WH = 50, 50

# The three places on the world map you can walk into, and the tiles beside
# them that the player actually stands on.
WOOD_MOUTH = WORLD_GLOAMWOOD                 # south end of the Gloamwood
WOOD_NORTH = (17, 20)                        # where the wood spits you out
TOWER_DOOR = WORLD_TOWER
SHRINE = (28, 15)

# Region ids drive which encounters happen where. Region 3 is the shingle
# along the south coast, and belongs to `wilds.py`.
REG_SOUTH, REG_NORTH = 1, 2
REG_COAST = W.REG_COAST
REG_CLANG = F.REG_CLANG

# Gloamwood
GW, GH = 34, 40
GW_IN = (17, 37)                             # arriving from the world map
GW_OUT = (17, 2)                             # on to the deep wood

# The deep wood
DW, DH = 30, 30
DW_IN = (15, 27)
DW_OUT = (15, 2)

# The tower
TW, TH = 33, 34
TOWER_IN = (16, 30)
TOWER_STAIR = (16, 5)

# The summit
SW_, SH = 25, 23
SUMMIT_IN = (12, 19)


def tint(tone, duration=30):
    return [R.tint_screen(tone, duration, True)]


GLOOM = [-68, -50, -20, 40]
TOWER_GLOOM = [-40, -50, -10, 60]
CLEAR = [0, 0, 0, 0]


# ============================================================ the overworld ==
def world_map():
    """Layer 0 is the base terrain, layer 1 is everything that grows or piles
    up on it, layer 3 is the landmarks. That split is what the sample's world
    map does, and it is the only way the forest and mountain autotiles blend
    into their surroundings instead of cutting holes in them."""
    g = K.Canvas(WW, WH)
    g.fill(0, 0, WW - 1, WH - 1, 0, K.W_SEA)

    # One continent, roughly oval, with a bite out of each coast.
    g.blob(25, 26, 21, 21, 0, K.W_GRASS)
    g.blob(46, 36, 5, 5, 0, K.W_SEA)
    g.blob(5, 13, 4, 5, 0, K.W_SEA)
    g.blob(9, 44, 4, 4, 0, K.W_SEA)
    W.south_ground(g)                             # the south-east shoulder,
    F.north_ground(g)                             # the headland and the beach,
    g.autotile(0)                                 # and the north-west lobe

    # -- layer 1: the shape of the journey --------------------------------
    # A mountain wall across the middle. Its one gap is full of trees, which
    # is why the Gloamwood is not optional.
    for x in range(5, 46):
        if 14 <= x <= 21:
            continue
        top = 23 + (x * 7 % 3)
        g.fill(x, top, x, top + 3, 1, K.W_MOUNTAIN)
    g.blob(17, 25, 7, 6, 1, K.W_FOREST)           # the Gloamwood itself
    g.fill(13, 20, 22, 30, 1, K.W_FOREST)

    g.blob(35, 34, 6, 3, 1, K.W_HILLS)
    g.blob(12, 39, 4, 3, 1, K.W_CONIFER)
    g.blob(38, 16, 4, 4, 1, K.W_HILLS_BROWN)
    g.blob(11, 11, 5, 3, 1, K.W_CONIFER)
    g.blob(33, 42, 3, 3, 1, K.W_FOREST)
    g.blob(8, 30, 3, 3, 1, K.W_HILLS)
    g.blob(43, 26, 2, 4, 1, K.W_MOUNTAIN)
    g.blob(35, 8, 4, 3, 1, K.W_MOUNTAIN)

    # The road, cut through whatever it crosses so it is always walkable.
    road = []
    road += [(24, y) for y in range(33, 45)]      # village to the crossroads
    road += [(x, 33) for x in range(17, 25)]      # west along the foothills
    road += [(17, y) for y in range(28, 34)]      # up to the wood
    road += [(17, y) for y in range(15, 21)]      # out of the wood, northward
    road += [(x, 15) for x in range(17, 29)]      # east past the wayshrine
    road += [(28, y) for y in range(9, 16)]       # north to the tower
    road += [(x, 9) for x in range(28, 32)]
    for x, y in road:
        g.set(x, y, 1, K.W_ROAD)
    W.south_layer1(g)                             # the coast road and the
    F.north_layer1(g)                             # two tracks off it, and the
    g.autotile(1)                                 # west road to Upper Clanging

    # -- layer 3: the places you can walk into -----------------------------
    g.blit(WORLD_VILLAGE[0] - 1, WORLD_VILLAGE[1] - 1, 3, K.WB_VILLAGE)
    g.blit(TOWER_DOOR[0], TOWER_DOOR[1] - 1, 3, K.WB_TOWER)
    g.set(WOOD_MOUTH[0], WOOD_MOUTH[1], 3, K.WB_CAVE_DARK)
    g.set(WOOD_NORTH[0], WOOD_NORTH[1], 3, K.WB_CAVE_DARK)
    g.set(SHRINE[0], SHRINE[1], 3, K.WB_HUT)
    g.set(23, 38, 3, K.WB_SIGN)
    g.set(29, 11, 3, K.WB_SIGN)
    for x, y in [(20, 41), (28, 38), (12, 35), (34, 29), (40, 21), (21, 12),
                 (33, 46), (9, 25), (44, 33)]:
        g.set(x, y, 3, K.WB_TREE)
    for x, y in [(31, 31), (14, 44), (36, 13), (7, 22)]:
        g.set(x, y, 3, K.WB_ROCK)
    W.south_layer3(g)
    F.north_layer3(g)

    # Regions decide which encounters happen where: the south half of the
    # continent is a gentler place than the north half.
    for y in range(WH):
        for x in range(WW):
            if g.get(x, y, 0) == 0:
                continue
            g.set(x, y, 5, REG_SOUTH if y >= 30 else
                  (REG_NORTH if y <= 21 else 0))
    W.south_regions(g)
    F.north_regions(g)

    m = K.new_map(WW, WH, K.TS_WORLD, name="", bgm="Field1",
                  encounter_step=36, scroll_type=0,
                  battleback=("Grassland", "Grassland"),
                  encounters=[
                      (db.TR_TURNIPS, 6, [REG_SOUTH]),
                      (db.TR_CROWS, 5, [REG_SOUTH]),
                      (db.TR_FIELD_MIX, 4, [REG_SOUTH]),
                      (db.TR_GOBLINS, 5, [REG_NORTH, REG_CLANG]),
                      (db.TR_BANDITS, 4, [REG_NORTH, REG_CLANG]),
                      (db.TR_WISPS, 3, [REG_NORTH, REG_CLANG]),
                      (db.TR_CRABS, 5, [REG_COAST]),
                      (db.TR_GULLS, 5, [REG_COAST]),
                      (db.TR_COAST_MIX, 3, [REG_COAST]),
                  ])
    m["data"] = g.data
    evs = world_events()
    south = W.south_events(len(evs) + 1)
    m["events"] = ([None] + evs + south +
                   F.north_events(len(evs) + len(south) + 1))
    return m


def world_events():
    evs = []

    # 1: back into Thistlewick
    home = S.narrate(["Thistlewick. Still there. Still turnips."])
    home += R.choice_block(
        ["Go in", "Carry on"],
        [[R.play_se("Move1"), R.transfer(MAP_VILLAGE, VILLAGE_GATE[0],
                                         VILLAGE_GATE[1] + 1, 2, 0)],
         []])
    evs.append(R.event(1, "Thistlewick", *WORLD_VILLAGE, [R.page(
        home, img=R.image(""), trigger=1, priority=0, through=True)]))

    # 2: into the Gloamwood
    wood = S.narrate([
        "The road ends at a wall of trees.",
        "There is a gap. The gap is the road now."])
    wood += R.choice_block(
        ["Go in", "Think about it"],
        [[R.play_se("Move1")] + tint(GLOOM, 1) +
         [R.transfer(MAP_GLOAMWOOD, *GW_IN, 8, 0)],
         S.narrate(["You think about it.",
                    "It does not improve."])])
    evs.append(R.event(2, "Gloamwood Mouth", *WOOD_MOUTH, [R.page(
        wood, img=R.image(""), trigger=1, priority=0, through=True)]))

    # 3: the far side of the wood, once it has been crossed
    back = S.narrate(["The north end of the Gloamwood.",
                      "You have been in there. You remember."])
    back += R.choice_block(
        ["Go back in", "Leave it"],
        [[R.play_se("Move1")] + tint(GLOOM, 1) +
         [R.transfer(MAP_GLOAM_DEEP, DW_OUT[0], DW_OUT[1] + 1, 2, 0)],
         []])
    evs.append(R.event(3, "Gloamwood North Mouth", *WOOD_NORTH, [
        R.page([], img=R.image(""), trigger=0, priority=0, through=True),
        R.page(back, img=R.image(""), trigger=1, priority=0, through=True,
               conditions={"switch1Valid": True, "switch1Id": db.SW_GLOAMWOOD}),
    ]))

    # 4: the tower - and the door at which the guest star always leaves
    door = roland_departure()
    door += S.narrate([
        "The Obligatory Tower.",
        "It is exactly as tall as everyone said, which",
        "is somehow the most unsettling thing about it."])
    door += R.choice_block(
        ["Go in", "Not yet"],
        [[R.play_se("Move1")] + tint(TOWER_GLOOM, 1) +
         [R.transfer(MAP_TOWER, *TOWER_IN, 8, 0)],
         S.narrate(["Not yet."])])
    # `<noairship>` is an assertion, not behaviour: `validate.py` reads it and
    # checks the tileset flags say an airship cannot set down on this square.
    # Clause seven of the Prophecy specifies on foot, and the tile the door is
    # drawn on carries 0x0800 so that the engine agrees - see NORTH.md 5.2 and
    # `build_game.TILESET_FLAGS`. Not one of Roland's or the door's own lines
    # is touched by it.
    evs.append(R.event(4, "Tower Door", TOWER_DOOR[0], TOWER_DOOR[1],
                       [R.page(door, img=R.image(""), trigger=1, priority=0,
                               through=True)], note="<noairship>"))

    # 5: the wayshrine - the one safe place on the road
    shrine = S.narrate([
        "A wayshrine. A roof, a bench, and a box of",
        "supplies with a note: 'FOR CHOSEN ONES.",
        "PLEASE REPLACE WHAT YOU TAKE. NOBODY EVER",
        "REPLACES WHAT THEY TAKE.'"])
    shrine += R.choice_block(
        ["Rest", "Read the visitors' book", "Move on"],
        [[R.fadeout_screen(), R.play_me("Inn2"), R.recover_all(), R.wait(60),
          R.fadein_screen()] + S.narrate(["The party rests. Nothing eats them.",
                                          "A small mercy, well taken."]),
         S.narrate(["Forty-seven names.",
                    "The last entry reads: 'Feeling good about",
                    "this one!' and is dated a hundred years ago.",
                    "You add your name. You do not add a comment."]) +
         [S.trope()],
         []])
    evs.append(R.event(5, "Wayshrine", *SHRINE, [R.page(
        shrine, img=R.image(""), trigger=1, priority=0, through=True)]))

    # 6/7: signposts, because the road is long
    evs.append(S.sign(6, "Southern Signpost", 23, 38, [
        "\\C[6]NORTH:\\C[0] The Obligatory Tower.",
        "\\C[6]SOUTH:\\C[0] Thistlewick, and then the coast road",
        "       east to Nether Sopping.",
        "Under that, freshly carved:",
        "'HE IS NOT THAT BAD ACTUALLY' - and someone",
        "else has carved 'YES HE IS' underneath it."]))
    evs.append(S.sign(7, "Northern Signpost", 29, 11, [
        "\\C[6]THE OBLIGATORY TOWER\\C[0]",
        "VISITORS: 47",
        "SURVIVORS: [the number has been scratched off]",
        "PLEASE WIPE YOUR FEET"]))
    return evs


def roland_departure():
    """Roland Fairweather is contractually unavailable for the final dungeon.

    This runs at the tower door on the world map rather than inside the tower,
    so a party that has just lost a member can walk back and get another one.
    He empties his pockets first: an actor removed from the party keeps
    whatever is equipped on him, and a guest star who walks off wearing the
    best armour the player owns is a joke that stops being funny immediately."""
    leave = [R.save_bgm(), R.fadeout_bgm(1), R.wait(20),
             R.play_bgm("Theme4", 75)]
    leave += S.narrate([
        "At the foot of the tower, Roland Fairweather",
        "stops walking.",
        "He does not look surprised. He looks like a",
        "man who has been checking the time all week."])
    leave += S.say("Roland", [
        "Ah.",
        "Yes. There it is."])
    leave += S.narrate(["You ask what it is."])
    leave += S.say("Roland", [
        "I have to be somewhere.",
        "I don't know where. I never know where.",
        "I only ever know that it is not here,",
        "and that it is now, and that I am going."])
    leave += S.narrate([
        "He tries, visibly, to stay.",
        "It is not a curse and it is not cowardice and",
        "it does not look like either. It looks like a",
        "man being gently and firmly asked to leave."])
    leave += S.say("Roland", [
        "Eleven times. This is the eleventh.",
        "I have never once seen the end of one."])
    leave += R.script(["$gameActors.actor(%d).clearEquipments();" % db.ROLAND])
    leave += S.narrate([
        "He puts everything he is carrying on the",
        "grass, which takes a while, and includes",
        "several things you had lent him and one you",
        "had not."])
    leave += [R.gain_weapon(db.WP_FAIRWEATHER, 1),
              R.gain_item(db.IT_ELIXIR, 2), R.play_me("Fanfare2")]
    leave += S.narrate([
        "Got \\I[113]\\C[3]Fairweather's Own\\C[0] and",
        "\\I[179]\\C[3]Elixir x2\\C[0]."])
    leave += S.say("Roland", [
        "Take it up there. It is a very good",
        "sword and it has never been in a last",
        "room. Neither have I. One of us should",
        "manage it."])
    leave += S.narrate(["He shakes hands with everyone, including,",
                        "carefully, anyone who is not looking."])
    leave += S.say("Roland", [
        "Right. Well.",
        "Go on, then. You'll be marvellous.",
        "I'd stay to watch, but - "])
    leave += S.narrate(["He is already forty paces away."])
    # His recruit switch stays on: it is what keeps the "gone" page showing in
    # the Slain Wyvern, and a guest star you can re-hire after he has made his
    # exit is not a guest star.
    leave += [R.change_party(db.ROLAND, add=False),
              R.control_switch(db.SW_ROLAND_GONE, True),
              S.trope(), R.fadeout_bgm(2), R.wait(40), R.replay_bgm()]
    leave += S.narrate([
        "The party is one smaller.",
        "It is the shape of the thing. Everybody told",
        "you it was the shape of the thing."])
    return R.if_then(R.condition_actor_in_party(db.ROLAND), leave)


# ============================================================== the Gloamwood ==
def gloamwood_map():
    """Dark grass, a lot of trees, and one path that only looks like a maze.

    The trees are stepped two apart because a tree block is 2x2 and only its
    lower row blocks - so the whole wood tiles solid with no gaps to slip
    through, and the path is genuinely the only way across."""
    g = K.Canvas(GW, GH)
    g.fill(0, 0, GW - 1, GH - 1, 0, K.DARK_GRASS)

    # A switchback, so crossing the wood takes a minute.
    path = []
    path += [(17, y) for y in range(30, 39)]
    path += [(x, 30) for x in range(6, 18)]
    path += [(6, y) for y in range(22, 31)]
    path += [(x, 22) for x in range(6, 27)]
    path += [(26, y) for y in range(13, 23)]
    path += [(x, 13) for x in range(9, 27)]
    path += [(9, y) for y in range(7, 14)]
    path += [(x, 7) for x in range(9, 18)]
    path += [(17, y) for y in range(1, 8)]

    # Two clearings off the path, which is where the chest and the mimic sit.
    clearings = [(x, y) for y in range(11, 16) for x in range(11, 15)]
    clearings += [(x, y) for y in range(24, 28) for x in range(23, 27)]
    for x, y in path + clearings:
        g.set(x, y, 0, K.PATH if (x, y) in set(path) else K.SOIL)
    g.autotile(0)

    open_ground = set(path) | set(clearings)
    for y in range(0, GH - 1, 2):
        for x in range(0, GW - 1, 2):
            block = {(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)}
            if block & open_ground:
                continue
            # Vary the trees so the wood does not read as wallpaper.
            g.blit(x, y, 3, K.TREE if (x * 5 + y * 3) % 7 < 3 else K.TREE_DARK)

    # Undergrowth along the path and in the clearings.
    for n, (x, y) in enumerate(path):
        if n % 7 == 0:
            g.set(x + 1, y, 3, [K.MUSHROOMS, K.BUSH, K.DEAD_BUSH][n % 3])
        if n % 11 == 0:
            g.set(x - 1, y, 3, [K.LOGS, K.ROCK, K.DEAD_ROOTS][n % 3])
    g.scatter([(11, 11), (14, 15), (23, 27), (26, 24)], 3, K.DEAD_TREE)
    g.scatter([(12, 15), (25, 26)], 3, K.MUSHROOMS)

    m = K.new_map(GW, GH, K.TS_OUTSIDE, name="The Gloamwood", bgm="Dungeon1",
                  encounter_step=26, battleback=("GrassMaze", "Forest"),
                  encounters=[(db.TR_WISPS, 5, [1]),
                              (db.TR_CROWS, 4, [1]),
                              (db.TR_GOBLINS, 4, [1]),
                              (db.TR_WOOD_MIX, 3, [1])])
    K.paint_regions(g, K.TS_OUTSIDE, 1)
    m["data"] = g.data
    m["events"] = [None] + gloamwood_events()
    return m


def gloamwood_events():
    evs = []

    out = S.narrate(["Back out into the daylight?"])
    out += R.choice_block(
        ["Yes", "No"],
        [[R.play_se("Move1")] + tint(CLEAR, 1) +
         [R.transfer(MAP_WORLD, WOOD_MOUTH[0], WOOD_MOUTH[1] + 1, 2, 0)], []])
    evs.append(R.event(1, "Way Out (south)", GW_IN[0], GW_IN[1] + 1, [R.page(
        out, img=R.image(""), trigger=1, priority=0, through=True)]))

    evs.append(R.event(2, "Deeper In (north)", GW_OUT[0], GW_OUT[1] - 1, [
        R.page([R.play_se("Move1"), R.transfer(MAP_GLOAM_DEEP, *DW_IN, 8, 0)],
               img=R.image(""), trigger=1, priority=0, through=True)]))

    # NORTH.md 3.4, one of three. New props in existing dungeons; nobody's
    # existing lines are touched and a party without Wren in it is told
    # nothing at all.
    evs.append(S.specimen(8, "A Nest", 13, 7, [
        "A nest wedged into the fork of a tree, at",
        "head height. Big, untidy, recently used.",
        "Caught in the rim of it: one long banded",
        "crest feather, the colour of a boiled sweet.",
    ], S.say("Wren", [
        "The crest isn't for fighting.",
        "It's a display structure.",
    ]) + S.say("Wren", [
        "It is for attracting a mate. It works.",
        "That is why there are nine of them.",
    ]), [
        "The nest, and the feather, where you put",
        "them back.",
    ]))

    # A lost adventurer, still going.
    lost = S.narrate([
        "A man in very good armour is sitting on a log."])
    lost += S.say("Regular", [
        "Don't tell me. North, is it? Tower?",
        "I'm number forty-six."])
    lost += S.narrate(["You point out that forty-seven came after him."])
    lost += S.say("Regular", [
        "Did he? Good for him.",
        "Did he come back?"])
    lost += S.narrate(["You do not answer."])
    lost += S.say("Regular", [
        "Right. Well. I got as far as the woods",
        "and decided the woods were enough.",
        "Nobody writes songs about that. But I'm",
        "here, and I'm forty-six, and I'm sitting down."])
    lost += S.narrate([
        "There is a sack beside the log with letters",
        "in it. A great many letters, in two hands,",
        "one round and one narrow, going back years."])
    lost += S.say("Regular", [
        "Nabb and Tolly. They write.",
        "Every month, the both of them."])
    lost += S.narrate(["You ask whether he writes back."])
    lost += S.say("Regular", [
        "I read them.",
        "Reading them's the answer. They know",
        "that. Nabb doesn't, but Tolly does,",
        "and Tolly does the stamps."])
    lost += [R.control_switch(db.SW_MET_46, True), S.trope()]
    evs.append(S.npc(3, "Number Forty-Six", 7, 26, lost, "People4", 6,
                     direction=6))

    evs.append(S.chest(4, "Wood Chest", 25, 25,
                       [R.gain_item(db.IT_HI_POTION, 2),
                        R.gain_item(db.IT_ETHER, 2), R.gain_gold(300)],
                       ["Found \\I[176]\\C[3]Hi-Potion x2\\C[0],",
                        "\\I[178]\\C[3]Ether x2\\C[0] and 300\\G."]))

    # The mimic, which is obviously a mimic, and the game says so.
    mimic = S.narrate([
        "A treasure chest, alone, in the middle of a",
        "wood, on a path, in perfect condition."])
    mimic += R.choice_block(
        ["Open it", "Absolutely not"],
        [S.narrate(["You knew. You knew and you did it anyway."]) +
         [R.control_switch(db.SW_MIMIC, True), S.trope(),
          R.play_se("Monster1"),
          R.battle(db.TR_MIMIC, can_escape=False, can_lose=False)] +
         S.narrate(["It was a mimic.",
                    "Somewhere, a Dungeon Design Committee is",
                    "having a very good day."]) +
         [R.gain_item(db.IT_ELIXIR, 1), R.play_me("Item"),
          R.self_switch("A", True)] +
         S.narrate(["Found \\I[179]\\C[3]Elixir\\C[0] in the mimic.",
                    "It had been carrying it around as bait,",
                    "which is either clever or very sad."]),
         S.narrate(["You walk past the obvious mimic.",
                    "It is, briefly, insulted."]) + [S.trope()]])
    evs.append(R.event(5, "Chest (Definitely A Chest)", 12, 12, [
        R.page(mimic, img=R.image("!Chest", 0, direction=2, pattern=1),
               trigger=0, priority=1, direction_fix=True),
        R.page(S.narrate(["Just splinters now."]), img=R.image(""),
               trigger=0, priority=1, through=True,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ]))

    evs.append(S.sign(6, "Carved Tree", 6, 24, [
        "Somebody has carved an arrow into the bark,",
        "pointing north.",
        "Underneath it, in a shakier hand, a second",
        "arrow points back the way you came."]))

    evs.append(S.sign(7, "Bones", 10, 9, [
        "A helmet, a boot, and a note in a jar:",
        "'IF FOUND, I WAS RIGHT ABOUT THE MIMIC'."]))
    return evs


# ======================================================= the deep Gloamwood ==
def deep_map():
    g = K.Canvas(DW, DH)
    g.fill(0, 0, DW - 1, DH - 1, 0, K.DARK_GRASS)

    path = []
    path += [(15, y) for y in range(12, 29)]
    path += [(x, 20) for x in range(8, 16)]
    path += [(x, 16) for x in range(15, 23)]
    path += [(15, y) for y in range(1, 12)]
    clearing = [(x, y) for y in range(8, 13) for x in range(11, 20)]
    for x, y in path + clearing:
        g.set(x, y, 0, K.SOIL)
    g.autotile(0)

    on_path = set(path) | set(clearing)
    for y in range(0, DH - 1, 2):
        for x in range(0, DW - 1, 2):
            block = {(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)}
            if block & on_path:
                continue
            g.blit(x, y, 3, K.TREE_DARK)

    # The clearing itself: dead things in a circle, because of course.
    for x, y in [(11, 8), (19, 8), (11, 12), (19, 12)]:
        g.set(x, y, 3, K.DEAD_TREE)
    g.scatter([(13, 11), (17, 11), (12, 9), (18, 9)], 3, K.MUSHROOMS)
    g.scatter([(14, 12), (16, 12)], 3, K.DEAD_ROOTS)

    m = K.new_map(DW, DH, K.TS_OUTSIDE, name="The Gloamwood", bgm="Dungeon1",
                  encounter_step=26, battleback=("GrassMaze", "Forest"),
                  encounters=[(db.TR_WOOD_MIX, 5, [1]),
                              (db.TR_WISPS, 4, [1]),
                              (db.TR_BANDITS, 3, [1])])
    K.paint_regions(g, K.TS_OUTSIDE, 1)
    m["data"] = g.data
    m["events"] = [None] + deep_events()
    return m


def deep_events():
    evs = [R.event(1, "Back South", DW_IN[0], DW_IN[1] + 1, [R.page(
        [R.play_se("Move1"), R.transfer(MAP_GLOAMWOOD, GW_OUT[0],
                                        GW_OUT[1] + 1, 2, 0)],
        img=R.image(""), trigger=1, priority=0, through=True)])]

    # The way north, which only opens once the Thing is dealt with.
    out = S.narrate(["Out of the trees, and north."])
    out += [R.play_se("Move1")] + tint(CLEAR, 1)
    out += [R.transfer(MAP_WORLD, WOOD_NORTH[0], WOOD_NORTH[1] + 1, 2, 0)]
    evs.append(R.event(2, "North Out Of The Wood", DW_OUT[0], DW_OUT[1] - 1, [
        R.page(S.narrate(["Something enormous is in the way."]),
               img=R.image(""), trigger=1, priority=0, through=True),
        R.page(out, img=R.image(""), trigger=1, priority=0, through=True,
               conditions={"switch1Valid": True, "switch1Id": db.SW_GLOAMWOOD}),
    ]))

    # NORTH.md 3.4, two of three.
    evs.append(S.specimen(6, "A Shed Skin", 19, 13, [
        "A shed skin, whole, hooked over a branch and",
        "left inside out. Four feet of it, and the",
        "head end is still the right way round.",
    ], S.say("Wren", [
        "Everything we have killed this week",
        "was in the middle of courting.",
    ]) + S.say("Wren", [
        "I don't say that to upset you.",
        "I say it because it goes in the monograph.",
    ]), [
        "Four feet of skin, inside out, on a branch.",
        "Somebody has straightened it since.",
    ]))

    # The Thing In The Woods.
    fight = S.narrate(["Something moves in the clearing.",
                       "It is difficult to say how much of it there is."])
    fight += [R.play_me("Shock1"), R.shake_screen(6, 6, 60, True)]
    fight += S.narrate([
        "Thistlewick has argued about this for two",
        "hundred years. Is it a bear? Is it several",
        "bears? Is it a bear-shaped hole in the idea",
        "of a wood?",
        "Nobody has ever got close enough to settle it."])
    fight += S.narrate(["You are now close enough."])
    fight += [R.battle(db.TR_THING, can_escape=False, can_lose=False),
              R.control_switch(db.SW_GLOAMWOOD, True)]
    fight += S.narrate([
        "The Thing In The Woods stops being in the woods.",
        "Thistlewick will never believe you.",
        "You are not going to tell them anyway."])
    fight += [R.gain_item(db.IT_ELIXIR, 1), R.gain_gold(800),
              R.play_me("Victory2")]
    fight += S.narrate(["Found \\I[179]\\C[3]Elixir\\C[0] and 800\\G."])
    fight += [S.trope(), R.self_switch("A", True)]
    evs.append(R.event(3, "The Thing In The Woods", 15, 10, [
        R.page(fight, img=R.image("Monster", 1, direction=2), trigger=1,
               priority=1, step_anime=True),
        R.page([], img=R.image(""), trigger=0, priority=0, through=True,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ]))

    evs.append(S.chest(4, "Deep Wood Chest", 9, 20,
                       [R.gain_armor(db.AR_AMULET, 1),
                        R.gain_item(db.IT_FEATHER, 2)],
                       ["Found \\I[146]\\C[3]Amulet of the Committee\\C[0]",
                        "and \\I[185]\\C[3]Slightly Singed Feather x2\\C[0]."]))

    evs.append(S.chest(5, "Hollow Log", 22, 16,
                       [R.gain_weapon(db.WP_DIRK, 1), R.gain_gold(250)],
                       ["Found \\I[96]\\C[3]Quiet Dirk\\C[0] and 250\\G",
                        "inside a hollow log.",
                        "Somebody hid these. Somebody did not come back",
                        "for them."]))
    return evs


# ======================================================= the Obligatory Tower ==
def tower_map():
    """Solid rock, carved into rooms. `dungeon_walls` handles the wall faces
    afterwards, so the carving below only has to describe the shape.

    Rooms are kept at least two tiles apart: a one-tile wall between two rooms
    renders as a pillar rather than a wall, and the whole floor then reads as
    one big room with columns in it."""
    g = K.Canvas(TW, TH)
    g.fill(0, 0, TW - 1, TH - 1, 0, K.DG_WALL_TOP)

    rooms = [
        (12, 26, 20, 31),      # entrance hall
        (14, 5, 18, 24),       # the long climb, all the way up
        (3, 18, 10, 24),       # west store room
        (22, 18, 29, 24),      # east guard room
        (3, 7, 10, 13),        # west gallery
        (22, 7, 29, 13),       # east gallery
    ]
    for x1, y1, x2, y2 in rooms:
        g.fill(x1, y1, x2, y2, 0, K.DG_FLOOR)
    corridors = [
        (16, 24, 16, 27),      # entrance up into the climb
        (11, 21, 13, 21), (19, 21, 21, 21),
        (11, 10, 13, 10), (19, 10, 21, 10),
    ]
    for x1, y1, x2, y2 in corridors:
        g.fill(min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2), 0,
               K.DG_FLOOR)
    # A landing halfway up and another at the top, in different flagstones,
    # so the climb has a middle and an end you can see coming.
    g.fill(14, 15, 18, 18, 0, K.DG_FLOOR2)
    g.fill(14, 5, 18, 8, 0, K.DG_FLOOR2)

    g.dungeon_walls(K.DG_WALL_TOP, K.DG_WALL_FACE)
    g.autotile(0)

    for x, y in [(13, 28), (19, 28), (13, 17), (19, 17)]:
        g.column(x, y - 1, 3, K.DGB_PILLAR)
    g.scatter([(4, 19), (9, 23), (23, 23), (28, 19)], 3, K.DGB_RUBBLE)
    g.scatter([(6, 23), (26, 23), (4, 12), (29, 12)], 3, K.DGB_BONES)
    g.scatter([(8, 19), (24, 19)], 3, K.DGB_SKULLS)
    g.column(4, 8, 3, K.DGB_STATUE_ANGEL)
    g.column(29, 8, 3, K.DGB_STATUE_DEMON)
    g.column(15, 12, 3, K.DGB_OBELISK)
    g.scatter([(17, 20), (15, 23)], 3, K.DGB_ROCK)

    K.paint_regions(g, K.TS_DUNGEON, 1)

    m = K.new_map(TW, TH, K.TS_DUNGEON, name="The Obligatory Tower",
                  bgm="Dungeon5", encounter_step=30,
                  battleback=("Stone1", "Ruins1"),
                  encounters=[(db.TR_SKELETONS, 5, [1]),
                              (db.TR_TOWER_MIX, 4, [1]),
                              (db.TR_GARGOYLES, 3, [1])])
    m["data"] = g.data
    m["events"] = [None] + tower_events()
    return m


def tower_events():
    evs = []

    leave = S.narrate(["Leave the tower?"])
    leave += R.choice_block(
        ["Yes", "No"],
        [[R.play_se("Move1")] + tint(CLEAR, 1) +
         [R.transfer(MAP_WORLD, TOWER_DOOR[0], TOWER_DOOR[1] + 1, 2, 0)], []])
    evs.append(R.event(1, "Tower Door", TOWER_IN[0], TOWER_IN[1] + 1, [R.page(
        leave, img=R.image(""), trigger=1, priority=0, through=True)]))

    # The barred door. Two ways through it, so no party can be locked out.
    nix_picks = S.say("Nix", [
        "Bar's on the inside. Classic.",
        "Which means there's a gap, and a gap is just",
        "a door that hasn't been asked properly."])
    nix_picks += [R.play_se("Key"), R.wait(30)]
    nix_picks += S.narrate(["The bar lifts."])

    the_mat = S.narrate([
        "There is a mat in front of the door.",
        "It says WELCOME, which for a Dark Lord's tower",
        "raises a number of questions."])
    the_mat += R.choice_block(
        ["Look under the mat", "Do not look under the mat"],
        [S.narrate(["There is a key under the mat."]) +
         [R.play_se("Key"), R.gain_item(db.IT_TOWER_KEY, 1), S.trope()] +
         S.narrate(["Got \\I[195]\\C[3]Tower Key\\C[0].",
                    "It is labelled 'SPARE - DO NOT LOSE AGAIN'.",
                    "Four thousand years of this and the answer",
                    "was the mat."]),
         S.narrate(["You maintain your dignity.",
                    "The door remains barred.",
                    "Dignity is not a key."])])

    barred = S.narrate([
        "A heavy door, barred from the other side.",
        "Beyond it, stairs."])
    barred += R.if_then(
        R.condition_actor_in_party(db.NIX),
        nix_picks + [R.control_switch(db.SW_TOWER_OPEN, True), S.trope()],
        R.if_then(R.condition_item(db.IT_TOWER_KEY),
                  S.narrate(["The spare key turns. Of course it does."]) +
                  [R.play_se("Key"),
                   R.control_switch(db.SW_TOWER_OPEN, True)],
                  the_mat))
    evs.append(R.event(2, "Barred Door", 16, 9, [
        R.page(barred, img=R.image("!Door2", 0, direction=2), trigger=0,
               priority=1, direction_fix=True),
        R.page([R.play_se("Move1"), R.transfer(MAP_SUMMIT, *SUMMIT_IN, 8, 0)],
               img=R.image("!Door2", 0, direction=2, pattern=2), trigger=1,
               priority=1, direction_fix=True,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_TOWER_OPEN}),
    ]))

    # A shrine that heals, because the run up to a two-phase boss is long.
    shrine = S.narrate([
        "A basin of clear water in a tower with no",
        "plumbing.",
        "Scratched into the rim: 'HE LEAVES IT OUT FOR",
        "US. NOBODY KNOWS WHY.'"])
    shrine += R.choice_block(
        ["Drink", "Leave it"],
        [[R.play_me("Refresh"), R.recover_all()] +
         S.narrate(["The party is fully restored.",
                    "Somewhere upstairs, someone is being",
                    "unaccountably thoughtful."]),
         []])
    evs.append(R.event(3, "Basin", 16, 16, [R.page(
        shrine, img=R.image(""), trigger=0, priority=1, direction_fix=True)]))

    evs.append(S.chest(4, "West Store Room", 5, 21,
                       [R.gain_weapon(db.WP_BROADSWORD, 1),
                        R.gain_item(db.IT_HI_POTION, 3)],
                       ["Found \\I[123]\\C[3]Broadsword\\C[0] and",
                        "\\I[176]\\C[3]Hi-Potion x3\\C[0]."]))
    evs.append(S.chest(5, "East Guard Room", 27, 21,
                       [R.gain_armor(db.AR_PLATE, 1), R.gain_gold(600)],
                       ["Found \\I[137]\\C[3]Family Plate\\C[0] and 600\\G."]))
    evs.append(S.chest(6, "West Gallery", 5, 10,
                       [R.gain_weapon(db.WP_STARFALL, 1)],
                       ["Found \\I[118]\\C[3]Unlicensed Starfall\\C[0].",
                        "The College would like a word."]))
    evs.append(S.chest(7, "East Gallery", 27, 10,
                       [R.gain_weapon(db.WP_WORLDBREAKER, 1),
                        R.gain_item(db.IT_ELIXIR, 1)],
                       ["Found \\I[99]\\C[3]Beatrice II\\C[0] and",
                        "\\I[179]\\C[3]Elixir\\C[0]."]))

    evs.append(S.sign(8, "Plaque By The Door", 14, 29, [
        "\\C[6]THE OBLIGATORY TOWER\\C[0]",
        "Est. approx. 4,800 years ago",
        "'UNDER THE SAME MANAGEMENT'"]))

    evs.append(S.sign(9, "The Obelisk", 15, 13, [
        "An obelisk, covered in very small writing.",
        "It is a list. Forty-seven entries. Each one is",
        "a date and a name and the word RENEWED.",
        "There is room for a forty-eighth."]))

    # Every character's best weapon lives in one cupboard, because the party
    # is four of seven and there is no way to know which four in advance.
    cache = [R.play_se("Chest1")]
    cache += S.narrate([
        "A cupboard. Inside, nine hooks, each with a",
        "small brass label.",
        "The labels read: CHOSEN ONE. HEALER. SMITH.",
        "MAGE. SPECIALIST. KNIGHT. MUSICIAN."])
    cache += S.narrate([
        "Two more have been added later, in a different",
        "hand and a cheaper brass: RIVAL. CATALOGUER.",
        "Somebody has been keeping this list up to date",
        "for four thousand years, which is unnerving."])
    cache += S.narrate([
        "The ninth hook is empty. Its label reads",
        "\\C[2]GUEST\\C[0], and underneath, in pencil:",
        "'HE WON'T BE HERE. HE NEVER IS. I LEAVE IT",
        "OUT ANYWAY.'"])
    cache += [R.gain_weapon(db.WP_DESTINY, 1), R.gain_weapon(db.WP_HOLY_ROD, 1),
              R.gain_weapon(db.WP_WORLDBREAKER, 1),
              R.gain_weapon(db.WP_STARFALL, 1), R.gain_weapon(db.WP_LAST_WORD, 1),
              R.gain_weapon(db.WP_OATHKEEPER, 1), R.gain_weapon(db.WP_LEGEND, 1),
              R.gain_weapon(db.WP_FORETOLD, 1), R.gain_weapon(db.WP_CITATION, 1),
              R.gain_item(db.IT_ELIXIR, 2), R.play_me("Fanfare2")]
    cache += S.narrate([
        "Got the \\C[3]Contingency Cache\\C[0]: one legendary",
        "weapon for every kind of Chosen One there has",
        "ever been, and two \\I[179]\\C[3]Elixirs\\C[0]."])
    cache += S.narrate([
        "A note on the inside of the door:",
        "'RESTOCKED EVERY CENTURY. NOBODY HAS EVER",
        "OPENED THIS CUPBOARD. IT IS SIX FEET FROM",
        "THE STAIRS. I DO NOT UNDERSTAND ANY OF YOU.'"])
    cache += [S.trope(), R.self_switch("A", True)]
    evs.append(R.event(11, "Contingency Cache", 14, 7, [
        R.page(cache, img=R.image("!Chest", 0, direction=2, pattern=1),
               trigger=0, priority=1, direction_fix=True),
        R.page(S.narrate(["Seven empty hooks and a very smug note."]),
               img=R.image("!Chest", 0, direction=2, pattern=2), trigger=0,
               priority=1, direction_fix=True,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ]))

    evs.append(S.sign(10, "Notice In The Stairwell", 18, 6, [
        "A notice, nailed up at eye level:",
        "'MIND THE STEP. I MEAN IT. THE STEP HAS",
        "TAKEN MORE OF YOU THAN I HAVE.' - G."]))
    return evs


# ================================================================== the end ==
def summit_map():
    """The top of the tower: a round chamber with a dais, and a portal at the
    back that has been renewing the same contract for four thousand years."""
    g = K.Canvas(SW_, SH)
    g.fill(0, 0, SW_ - 1, SH - 1, 0, K.DG_WALL_TOP)
    g.blob(12, 10, 9, 7, 0, K.DG_FLOOR)
    g.fill(10, 16, 14, 21, 0, K.DG_FLOOR)         # the stair up from below
    g.fill(8, 6, 16, 12, 0, K.DG_FLOOR2)          # the dais
    g.dungeon_walls(K.DG_WALL_TOP, K.DG_WALL_FACE)
    g.autotile(0)

    for x in (6, 18):
        g.column(x, 7, 3, K.DGB_PILLAR_WHITE)
        g.column(x, 12, 3, K.DGB_PILLAR_WHITE)
    g.column(12, 3, 2, K.DGB_PORTAL)              # where clause twelve lives
    g.column(9, 4, 3, K.DGB_STATUE_DEMON)
    g.column(15, 4, 3, K.DGB_STATUE_DEMON)
    g.scatter([(8, 14), (16, 14)], 3, K.DGB_SKULLS)
    g.scatter([(7, 16), (17, 16)], 3, K.DGB_BONES)
    g.scatter([(10, 15), (14, 15)], 3, K.DGB_RUBBLE)

    m = K.new_map(SW_, SH, K.TS_DUNGEON,
                  name="The Obligatory Tower - Summit", bgm="Dungeon7",
                  battleback=("DemonCastle1", "DemonCastle1"))
    m["data"] = g.data
    m["events"] = [None] + summit_events()
    return m


def summit_events():
    """The two-phase finale. Everything here runs off one long event so the
    beats stay in order: Grimspite, the relief, the Prophecy, the annulment."""
    evs = [R.event(1, "Back Down", SUMMIT_IN[0], SUMMIT_IN[1] + 1, [R.page(
        [R.play_se("Move1"), R.transfer(MAP_TOWER, 16, 10, 2, 0)],
        img=R.image(""), trigger=1, priority=0, through=True)])]

    evs.append(finale_event(2, 12, 8))
    return evs


def finale_event(event_id, x, y):
    c = []
    c += [R.play_bgm("Scene6", 80)]
    c += S.narrate([
        "The top of the Obligatory Tower.",
        "There is a throne. There is a Dark Lord on it.",
        "He is reading."])
    c += S.say("Grimspite", [
        "Forty-eight. Right on time.",
        "Sit down. No? Fine. Standing is traditional."])
    c += S.narrate(["He puts a bookmark in. He is careful about it."])
    c += S.say("Grimspite", [
        "Grimspite the Inevitable. Dark Lord.",
        "Four thousand eight hundred years, this job.",
        "Do you know how many times I have said the",
        "words 'so, you have come at last'?"])
    c += S.narrate(["You say you do not."])
    c += S.say("Grimspite", [
        "Forty-seven.",
        "And I meant it the first time."])
    quy = R.if_then(
        R.condition_switch(db.SW_MET_QUY),
        S.narrate(["Grimspite the Inevitable stops."]) +
        S.say("Grimspite", [
            "...Somebody told you to ask that.",
            "Nobody asks that. Forty-seven of them",
            "and not one. Who told you to ask?"]) +
        S.narrate(["You tell him: the forty-fifth.",
                   "A man in a garden, forty miles south,",
                   "who has thought about a cup of tea for",
                   "thirty years."]) +
        S.say("Grimspite", [
            "Halbert.",
            "He said no to the tea. I've wondered.",
            "You go back and you tell him the tea",
            "was just tea. Will you tell him that?"]) +
        S.narrate(["You say that you will."]) +
        S.say("Grimspite", [
            "Then listen to all of it. He'll ask",
            "you what I said, and I would like,",
            "once, for somebody to have listened",
            "to the whole of it."]))
    c += R.choice_block(
        ["Why don't you stop?", "Draw your weapon"],
        [S.say("Grimspite", [
            "Ah. The clever one.",
            "They're rarer than you'd",
            "think.",
            "I can't. Look at the wall behind you."]) + quy +
         S.narrate(["You look.",
                    "The wall is covered in the same sentence,",
                    "carved forty-seven times:",
                    "\\C[2]THE DARK LORD SHALL RISE AGAIN.\\C[0]"]) +
         S.say("Grimspite", [
             "Clause twelve. It isn't a threat.",
             "It's a renewal notice."]),
         S.say("Grimspite", [
             "Yes. Good.",
             "Let's do the part we're for."])])

    # -- clause seven, and the question Ott sent you up here with -----------
    # NORTH.md 8.2. Two appended branches, and the whole point of them is that
    # they do not know about each other. He explains why the Prophecy sends
    # its Chosen One on foot, and in explaining it he is wrong: the Two
    # Hundred did get off the ground in sight of this place, is parked outside
    # it, and got there because it had a Chosen One aboard. Nobody in the game
    # ever notices. It is for the player.
    #
    # Then, if she asked, he answers the only question anybody has ever put to
    # him that was not about the person putting it - and thanks her for it,
    # four lines after writing her off. Neither end of that ever refers to the
    # other: she is not told what he said, and he is not told what she built.
    c += R.if_then(
        R.condition_switch(db.SW_CLAUSE_SEVEN),
        S.narrate(["You ask him about clause seven."]) +
        S.say("Grimspite", [
            "Clause seven. On foot.",
            "Do you know why?"]) +
        S.narrate(["You say that you do not."]) +
        S.say("Grimspite", [
            "Because a thing that flies over",
            "and drops something is not a story.",
            "It is a Tuesday."]) +
        S.say("Grimspite", [
            "She will never get one",
            "off the ground in sight of this place, and",
            "it has nothing whatever to do with her",
            "spars."]))
    c += R.if_then(
        R.condition_switch(db.SW_OTT_MATERIALS),
        S.narrate(["You ask him what the tower is made of."]) +
        S.say("Grimspite", ["...Nobody has ever asked me that."]) +
        S.narrate(["He looks at the wall behind you as though",
                   "it has just arrived."]) +
        S.say("Grimspite", [
            "I don't know.",
            "It was here when I got here, and I have",
            "leaned on that wall every day of four",
            "thousand years and never once wondered."]) +
        S.say("Grimspite", ["Tell her the work was good."]) +
        S.say("Grimspite", [
            "Four thousand years, and she is the",
            "only one who ever came at me with a",
            "question about materials."]))

    c += S.say("Grimspite", [
        "Whatever you were going to say -",
        "and I have heard all of them - say it",
        "while we fight. It goes faster that way."])
    c += [R.play_me("Shock2"), R.wait(30)]
    # NORTH.md 7, the stretch goal, and the reason this is an index and not
    # another `if_then`: ITEM 1 is a whole scene rather than a question, and it
    # belongs to a *page*, not to a branch. The page below is built as
    # `c[:split] + bomb + c[split:]`, so page 1 stays the identical list it has
    # always been - the existing finale rebuilds byte for byte - and the crate
    # page is the same finale with one scene spliced into it. Splicing here,
    # after the sting and before the battle, is also the only placement that
    # does not make him a liar: he has just said he has heard all of them, and
    # four windows later he says this one is new, so the crate has to land
    # after the line, not before it.
    split = len(c)
    c += [R.battle(db.TR_GRIMSPITE, can_escape=False, can_lose=False),
          R.control_switch(db.SW_GRIMSPITE, True)]

    # -- the turn -----------------------------------------------------------
    c += [R.fadeout_bgm(2), R.wait(60)]
    c += S.narrate(["Grimspite the Inevitable goes down on one knee",
                    "and stays there, breathing."])
    c += S.say("Grimspite", ["...Thank you."])
    c += S.narrate(["That is not one of the forty-seven things",
                    "you were expecting."])
    c += S.say("Grimspite", [
        "You don't understand yet. You will.",
        "It takes about four seconds."])
    c += [R.play_se("Bell3"), R.wait(45), R.shake_screen(4, 4, 40, True)]
    c += S.narrate(["Something unrolls."])
    c += [R.tint_screen([-40, -40, 34, 60], 40, True), R.play_me("Curse1"),
          R.wait(30)]
    c += S.narrate([
        "It comes down from the ceiling and keeps",
        "coming: a scroll the width of the room, dense",
        "with clauses, moving like something with an",
        "opinion."])
    c += S.say("The Prophecy", [
        "CLAUSE TWELVE.",
        "THE DARK LORD SHALL RISE AGAIN."])
    c += S.say("Grimspite", [
        "It renews me. It has renewed me",
        "forty-seven times. It will do it before",
        "you reach the stairs. That is the whole of",
        "it. That is the whole of my life."])
    c += S.narrate(["The Prophecy turns, very slowly, to face you.",
                    "It has found a party of the correct size,",
                    "at the correct place, on the correct date."])
    c += S.say("The Prophecy", [
        "THE CHOSEN ONE SHALL BE CHOSEN.",
        "A NEW DARK LORD SHALL BE APPOINTED.",
        "THE ROLE IS VACANT.",
        "\\C[2]CONGRATULATIONS.\\C[0]"])
    c += S.narrate(["Ah."])
    c += S.say("Grimspite", ["Yes. That's how I got the job."])
    c += S.say("Grimspite", [
        "Forty-eight - don't kill it.",
        "Read it. Out loud. All of it.",
        "A contract that has been read in full has",
        "never once survived the experience."])
    c += [R.play_bgm("Battle7", 85), R.wait(20)]
    c += [R.battle(db.TR_PROPHECY, can_escape=False, can_lose=False)]

    # -- the ending ---------------------------------------------------------
    c += [R.fadeout_bgm(3), R.tint_screen(CLEAR, 60, True), R.wait(40),
          R.control_switch(db.SW_WON, True)]
    c += S.narrate([
        "The Prophecy comes apart in the middle of a",
        "sentence.",
        "It does not burn or explode. It simply stops",
        "being binding, which for a contract is the",
        "same as dying."])
    c += [R.play_me("Fanfare1"), R.wait(60)]
    c += S.narrate([
        "Grimspite the Inevitable stands up.",
        "Nothing renews him.",
        "He waits, to be sure. Nothing keeps happening."])
    c += S.say("Grimspite", [
        "Huh.",
        "Four thousand eight hundred years and it was",
        "an admin problem."])
    c += [R.gain_item(db.IT_RECEIPT, 1), R.play_se("Item1")]
    c += S.narrate(["Got \\I[188]\\C[3]A Receipt\\C[0].",
                    "Grimspite has signed it over to you.",
                    "'Proof of purchase,' he says. 'In case",
                    "anyone asks whose fault this was.'"])
    c += S.say("Grimspite", [
        "Go home, forty-eight.",
        "Grow your turnips. There isn't a forty-nine.",
        "Say that to them, when you get in.",
        "Say: there isn't a forty-nine."])
    c += [R.fadeout_screen(), R.wait(60), R.play_bgm("Theme6", 80)]

    # The trope counter, cashed in.
    c += S.narrate([
        "\\}\\C[6]THE OBLIGATORY QUEST\\C[0]",
        "Bram Thistle, Chosen One #48, went north",
        "with \\C[3]\\V[1]\\C[0] companions."])
    c += R.if_then(
        R.condition_switch(db.SW_ROLAND_GONE),
        S.narrate([
            "He came back with all of them but one, who",
            "had somewhere to be, and who is at this",
            "moment being marvellous in somebody else's",
            "story, and who thinks about this one."]),
        S.narrate(["He came back with all of them."]))
    c += S.narrate([
        "Along the way he walked into \\C[3]\\V[2]\\C[0] well-worn",
        "adventuring conventions and ate \\C[3]\\V[3]\\C[0] turnips."])
    c += R.if_then(
        R.condition_switch(db.SW_SOUTH),
        S.narrate([
            "He also went south, which no Chosen One had",
            "thought to do, and found forty-seven of them",
            "in a tavern, and sat down, and listened."]))
    c += R.if_then(
        R.condition_variable(db.VAR_BOUNTIES, 2, 1),
        S.narrate([
            "Both cards came off the Guild's board while",
            "he was down there, and Registrar Pell has",
            "written the year up as an unusually good one",
            "and does not intend to explain how."]),
        R.if_then(
            R.condition_variable(db.VAR_BOUNTIES, 1, 1),
            S.narrate([
                "One card came off the Guild's board while he",
                "was down there. There are usually two cards.",
                "There are, at the moment, rather fewer."])))
    c += R.if_then(
        R.condition_switch(db.SW_HISTORY_DONE),
        S.narrate([
            "There is a song about it now. Hosea",
            "Bellwether wrote it from first-hand accounts",
            "and it is, therefore, complete.",
            "It is not remotely accurate."]))
    c += R.if_then(
        R.condition_switch(db.SW_LAMP_LIT),
        S.narrate([
            "The Lighthouse of Saint Bother is lit again.",
            "You can see it from the crossroads, which is",
            "the whole of what it is for."]))
    c += R.if_then(
        R.condition_switch(db.SW_BENCH_DONE),
        S.narrate([
            "And on the top of a mound in the eastern",
            "hills there is a bench, facing the sea,",
            "which anybody may sit on, and which is what",
            "Ambrose Fitch asked for and did not get."]))
    # NORTH.md 2.2 and 8.2: three switches the ending did not know about.
    # Appended in the shape the lighthouse and the bench already have -
    # one thing that is different about the world, told flatly, no summary.
    c += R.if_then(
        R.condition_switch(db.SW_TWO_HUNDRED_FLEW),
        S.narrate([
            "There is a two hundredth entry in the Hoyle",
            "Works' attempt log. REACHED THE TOWER.",
            "LANDED ADJACENT. And under it, in the same",
            "hand as the hundred and ninety-nine above,"]) +
        S.narrate([
            "CAUSE: UNDER REVIEW.",
            "Two hundred years, and the only thing in that",
            "building Miss Hoyle will not write down is",
            "the reason it worked."]))
    c += R.if_then(
        R.condition_switch(db.SW_84_REBUILT),
        S.narrate([
            "In the works shed there is a bay with the",
            "number eighty-four over it, and for the",
            "first time in a hundred and forty years",
            "there is something under it."]) +
        S.narrate([
            "It will take years and nobody has costed it",
            "and nobody has asked to.",
            "Miss Hoyle had told a great many people that",
            "there would not be a two hundred and one."]))
    # The other half of the stretch goal. The crate is the one thing in the
    # game that can be spent two ways and this is the only place that ever
    # says which way it went - and it says it the way the works says
    # everything, which is in a ledger, in a column, without adjectives.
    c += R.if_then(
        R.condition_switch(db.SW_ITEM_ONE_USED),
        S.narrate([
            "There is a line through ITEM 1 in the Hoyle",
            "Works' stores book at last, dated, and",
            "initialled O.H., a hundred and ninety-eight",
            "years after it was written in."]) +
        S.narrate([
            "Miss Hoyle asked one question about it, which",
            "was whether it had worked, and was told that",
            "it had worked perfectly, and ruled the line",
            "through, and has not asked a second."]))
    c += R.if_then(
        R.condition_switch(db.SW_HOB_BRYD),
        S.narrate([
            "Bryd Ollerenshaw has been down the hill to",
            "the house that does a pale more times this",
            "year than in the twenty before it, and not",
            "once on his own."]) +
        S.narrate([
            "Half of Upper Clanging watches them go.",
            "The other half is told about it inside the",
            "hour."]))
    # The thresholds are set against the number of `story.trope()` sites in
    # the build, which the south roughly doubled. A completionist can reach
    # about sixty; a player who goes straight north will see twenty.
    c += R.if_then(
        R.condition_variable(db.VAR_TROPES, 40, 1),
        S.narrate(["Very nearly all of them. He read the notice",
                   "board, he searched the barrels, he opened",
                   "things that were obviously not chests, and",
                   "he went south, which nobody does."]),
        R.if_then(
            R.condition_variable(db.VAR_TROPES, 20, 1),
            S.narrate(["A respectable haul of cliches, honestly",
                       "encountered."]),
            S.narrate(["Remarkably few cliches, which the Prophecy",
                       "Committee will record as a procedural",
                       "irregularity."])))
    # NORTH.md 2.3, and the reason VAR_BLUSHES exists at all. The joke only
    # works in aggregate - which is exactly what keeps every one of the
    # twenty instances individually deniable - so this is the one place in
    # the game that admits there was a pattern, and it still does not say
    # what the pattern was.
    c += R.if_then(
        R.condition_switch(db.SW_BALLAD_DONE),
        S.narrate([
            "Verses struck by the Committee: \\C[3]\\V[7]\\C[0].",
            "Piper had every one of them down. The",
            "Committee read the fair copy through twice",
            "and took a pencil to the lot, without comment."]),
        S.narrate([
            "Things nobody quite said: \\C[3]\\V[7]\\C[0].",
            "Nobody wrote them down either. They are only",
            "the reason certain people in this account",
            "still do not quite look at one another."]))
    # One tier and no else, rather than the three-way shape the cliche block
    # above already uses: doing that twice running reads as a form being
    # filled in.
    #
    # **Twenty-five is every blush moment in the finished build**, measured
    # 2026-08-26 off the data rather than off the source, because NORTH.md 2.3
    # is right that a grep over-counts: 28 code-122 writes to variable 7, less
    # the two travellers (one joke, two events, one `SW_TRAVELLERS`), less Mrs
    # Tunnicliffe's census (first-visit page and repeat page, both guarded on
    # `SW_CENSUS` being false), less Bryd's spar page (the with-Hob and the
    # without-Hob branch cannot both run). The threshold was 16 when the total
    # was 20 - the town's nine and the retrofit's eleven - and the total has
    # since grown by Ott's three flying-chain beats, Bessie and Gudgeon. Keep
    # it at four fifths of whatever the total is, or the line congratulates a
    # player who missed nine of them.
    c += R.if_then(
        R.condition_variable(db.VAR_BLUSHES, 20, 1),
        S.narrate([
            "Very nearly all of them, which means he was",
            "in the room for very nearly all of them,",
            "which is the part nobody has yet worked out",
            "how to raise with him."]))
    c += S.narrate([
        "Thistlewick struck clause twelve from the",
        "records and replaced it with a note reading",
        "'SEE BRAM'.",
        "Nobody has needed to yet."])
    c += R.if_then(
        R.condition_switch(db.SW_MET_QUY),
        S.narrate([
            "It struck clause nineteen out as well, six",
            "months later, after a very long meeting.",
            "Forty miles south, a man in a garden read",
            "the notice twice and then went indoors."]) +
        S.narrate([
            "Bram had already been. He had walked down",
            "and told him what Grimspite said, all of it,",
            "in order, including the part about the tea.",
            "It took most of an afternoon."]))
    c += S.narrate(["\\}\\C[6]THE END\\C[0]"])
    c += [R.wait(90), R.return_to_title()]

    return R.event(event_id, "Grimspite", x, y, [
        R.page(c, img=R.image("Evil", 6, direction=2), trigger=0, priority=1,
               direction_fix=True),
        # Carrying the crate. Last page wins, so this beats the finale above
        # for as long as ITEM 1 is in the party's hands, and the SW_WON page
        # below beats both afterwards.
        R.page(c[:split] + item_one_scene() + c[split:],
               img=R.image("Evil", 6, direction=2), trigger=0, priority=1,
               direction_fix=True,
               conditions={"itemValid": True, "itemId": db.IT_ITEM_ONE}),
        R.page([], img=R.image(""), trigger=0, priority=0, through=True,
               conditions={"switch1Valid": True, "switch1Id": db.SW_WON}),
    ])


def item_one_scene():
    """ITEM 1, carried up the tower and used on the Dark Lord - NORTH.md 7.

    The funniest failure in the game, and it is funny because the bomb works.
    The Hoyle Works has spent two hundred years and a hundred and ninety-nine
    attempts failing to do one thing; the single object in that building that
    performs exactly as specified, first time, at the first asking, is the one
    nobody ever wanted to find out about. It goes off perfectly and it changes
    nothing, because the thing in this room is not a person who can be killed,
    it is a contract that has to be read.

    It is offered rather than triggered. A player can reach the summit with
    the crate on the way to Ott - the stores ledger sends you to the crag, not
    to the tower - and a page that lit it unasked would cost them Number One
    and the Fuse without ever putting the question. `Draw your weapon` is
    option zero, so a confirm pressed out of habit keeps the crate.

    And he sends the compliment south a second time without knowing it is the
    same woman, the same works or the same argument. Nobody at either end ever
    finds out, which is the arrangement everything else in section 8.2 is
    built on."""
    d = S.narrate([
        "You do not draw your weapon.",
        "Two of you set the crate down in front of the",
        "throne. It goes down like an anvil."])
    d += S.say("Grimspite", ["What is that."])
    d += S.narrate(["You tell him what is stencilled on it."])
    d += S.say("Grimspite", [
        "That is not a name. That is a line",
        "in somebody's ledger."])
    d += S.narrate([
        "You agree that it is.",
        "Then you light it."])
    d += S.say("Grimspite", ["...Ah."])
    d += S.narrate([
        "He does not get up, and he does not stop you.",
        "He puts the book down on the arm of the throne",
        "with the bookmark still in it, and watches the",
        "crate with real interest."])
    d += [R.fadeout_bgm(1), R.wait(40)]
    d += [R.play_se("Explosion2", 100),
          R.flash_screen([255, 255, 255, 255], 30, True),
          R.shake_screen(9, 9, 120, False),
          R.tint_screen([-90, -90, -90, 0], 20, True),
          R.wait(60)]
    d += S.narrate([
        "The Hoyle Works built it in 1802, to a",
        "specification of which no copy has been kept,",
        "and it has spent a hundred and ninety-eight",
        "years strapped down, waiting to be asked."])
    d += S.narrate([
        "It does not fail.",
        "It does precisely what it was built to do, at",
        "a range of four feet, in a stone room with the",
        "door shut."])
    d += [R.tint_screen(CLEAR, 90, True), R.wait(30)]
    d += S.narrate([
        "When the smoke goes, the throne is where the",
        "throne was. The wall is where the wall was.",
        "All forty-seven sentences carved into it are",
        "still legible."])
    d += S.narrate([
        "Grimspite the Inevitable is sitting exactly as",
        "he was sitting."])
    d += S.narrate(["His bookmark is on the floor."])
    d += S.say("Grimspite", [
        "Clause thirty-one.",
        "\\C[2]THE DARK LORD SHALL NOT BE CONCLUDED\\C[0]",
        "\\C[2]BY MECHANISM.\\C[0]"])
    d += S.say("Grimspite", [
        "Ordnance is not provided for.",
        "Nothing is provided for. That is what a",
        "renewal notice is."])
    d += S.narrate([
        "He leans forward. It is the first time he has",
        "moved like a man and not like a fixture."])
    d += S.say("Grimspite", [
        "Forty-seven of you.",
        "Swords, mostly. A spear, once.",
        "A very great deal of fire.",
        "Nobody has ever brought a bomb."])
    d += S.say("Grimspite", ["Do you know what that is?"])
    d += S.narrate(["You say that you do not."])
    d += S.say("Grimspite", [
        "That is new.",
        "That is the first new thing in four thousand",
        "eight hundred years, and I would like a",
        "moment with it."])
    d += S.narrate([
        "He takes one.",
        "Nobody says anything. Somewhere behind you a",
        "piece of the ceiling that has been thinking",
        "about it for a long time comes down."])
    d += S.say("Grimspite", [
        "Whoever made that has never once",
        "been told that it was any good."])
    d += S.narrate([
        "You think about that, and find that he is not",
        "wrong, and that you are not going to be the",
        "one to tell her either, because you would have",
        "to explain what you did with it."])
    d += S.narrate([
        "Then he leans down and picks the bookmark up,",
        "and puts it back in the book, and puts the",
        "book on the seat of the throne, and stands."])
    d += S.say("Grimspite", [
        "Right.",
        "Thank you for that. Genuinely.",
        "Now hit me with something."])
    d += [S.trope(), R.gain_item(db.IT_ITEM_ONE, -1),
          R.control_switch(db.SW_ITEM_ONE_USED, True)]
    d += [R.play_me("Shock2"), R.wait(30)]

    ask = S.narrate([
        "You are carrying a crate that is stencilled on",
        "all six faces, and it is not for carrying."])
    return ask + R.choice_block(
        ["Draw your weapon", "Set the crate down"], [[], d])


def build():
    R.save_map(MAP_WORLD, world_map())
    R.save_map(MAP_GLOAMWOOD, gloamwood_map())
    R.save_map(MAP_GLOAM_DEEP, deep_map())
    R.save_map(MAP_TOWER, tower_map())
    R.save_map(MAP_SUMMIT, summit_map())
