"""Nether Sopping and everything in it: Maps 13-18.

    13  Nether Sopping               a wet town on the south coast
    14  The Slain Wyvern             the tavern, and the whole point of it
    15  The Adventurers' Guild       provisional, for forty years
    16  Wick & Barrow, Outfitters    there is no Wick
    17  Number Forty-Five's Cottage  a retired Chosen One, in a garden
    18  The Lighthouse of Saint Bother

None of this is on the way to the Dark Lord. It is where the forty-seven who
came back were quietly resettled, which is the answer to a question the main
quest never gets round to asking. See `EXPANSION.md`.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import db
import mapkit as K
import rmmzdata as R
import story as S
from places import (MAP_SOPPING, MAP_WYVERN, MAP_GUILD, MAP_OUTFIT,
                    MAP_COTTAGE, MAP_LIGHTHOUSE, MAP_WORLD, SOPPING_GATE,
                    WORLD_SOPPING_STEP, WORLD_LIGHTHOUSE)

TOWN_W, TOWN_H = 40, 34

# Buildings: (x, y, w, h). The door sits on the last row, as in Thistlewick.
COTTAGE = (4, 4, 7, 5)
OUTFIT = (26, 4, 8, 5)
WYVERN = (6, 11, 11, 7)
GUILD = (26, 12, 8, 6)

COTTAGE_DOOR = (7, COTTAGE[1] + COTTAGE[3] - 1)
OUTFIT_DOOR = (29, OUTFIT[1] + OUTFIT[3] - 1)
WYVERN_DOOR = (11, WYVERN[1] + WYVERN[3] - 1)
GUILD_DOOR = (29, GUILD[1] + GUILD[3] - 1)

OUT = {m: (d[0], d[1] + 1) for m, d in [
    (MAP_COTTAGE, COTTAGE_DOOR), (MAP_OUTFIT, OUTFIT_DOOR),
    (MAP_WYVERN, WYVERN_DOOR), (MAP_GUILD, GUILD_DOOR)]}

# The lighthouse has no door on the town map - it is its own landmark out on
# the headland, so it comes and goes through the world map.
LIGHTHOUSE_IN = (6, 19)

# The four sheds you cannot go into, at the top tile of their shut door. Each
# one has an event on the bottom tile saying why not.
SHED_DOORS = [(36, 14), (5, 22), (14, 7), (31, 22)]


# ---------------------------------------------------------------- helpers ---
def talker(event_id, name, x, y, speaker, first, again, sheet=None, index=None,
           direction=2, extra=(), move_type=0, pages=None):
    """Somebody with one thing to say and a shorter version of it afterwards.

    Almost every villager in the south is this shape: a set piece the first
    time, and a line that acknowledges you have already heard it. The second
    page is keyed on a self switch, so it costs no global state.

    `pages` appends further pages after those two, and is how somebody who is
    finished acquires something new to say without a syllable of what they
    already said being touched. `Game_Event.refresh` takes the **last** page
    whose conditions hold, so a page added here and guarded by a switch wins
    over both of the above once that switch is on, and is invisible until
    then. A player who never trips the condition gets today's game exactly as
    it stands - which is the whole of NORTH.md's rule 1.7, in one keyword."""
    if sheet is None:
        sheet, index = S.FACES[speaker]
    img = R.image(sheet, index, direction=direction)
    said = list(first) + list(extra) + [R.self_switch("A", True)]
    return R.event(event_id, name, x, y, [
        R.page(said, img=img, trigger=0, priority=1, move_type=move_type),
        R.page(list(again), img=img, trigger=0, priority=1, move_type=move_type,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ] + list(pages or []))


def tale(event_id, name, x, y, speaker, first, again, direction=2,
         sheet=None, index=None, extra=()):
    """One of the six first-hand accounts in the Slain Wyvern.

    Hearing one bumps `VAR_TALES`, which is what Hosea Bellwether counts, and
    `VAR_TROPES`, because every one of them is a genre cliché that happened to
    somebody who is still cross about it.

    `extra` is appended after both of those, for the one tale that something
    else in the room wants to know has been heard. Nothing already written is
    touched by it: it lands at the end of a command list, after the last thing
    the character says."""
    return talker(event_id, name, x, y, speaker, first, again,
                  sheet=sheet, index=index, direction=direction,
                  extra=[R.control_variable_add(db.VAR_TALES, 1), S.trope()]
                        + list(extra))


def travellers_count():
    """One bump for the two of them, whichever one you asked.

    `VAR_BLUSHES` counts *moments*, and NORTH.md 3.6 is one moment with two
    people in it - so the guard is a global switch and not the self switch
    every other guarded blush in the game uses. `blushes` asks both of them
    and asserts the counter moved once."""
    return R.if_then(R.condition_switch(db.SW_TRAVELLERS, False),
                     [S.blush(), R.control_switch(db.SW_TRAVELLERS, True)])


# =========================================================== Nether Sopping ==
def sopping_map():
    """One street down to a harbour. Everything faces the sea, including the
    people, which is a thing Thistlewick notices about southerners and does not
    like."""
    g = K.Canvas(TOWN_W, TOWN_H)
    g.fill(0, 0, TOWN_W - 1, TOWN_H - 1, 0, K.GRASS)
    g.fill(0, 24, TOWN_W - 1, 26, 0, K.SAND)
    g.fill(0, 27, TOWN_W - 1, TOWN_H - 1, 0, K.WATER)

    # -- the ground. A working harbour is paved right up to the water, and
    # the green only survives round the edges, which is what makes it read as
    # a town rather than four sheds on a lawn.
    g.fill(3, 9, 35, 23, 0, K.PAVING)             # the town proper
    g.fill(19, 2, 20, 25, 0, K.PAVING)            # the street, up to the gate
    g.fill(12, 20, 28, 25, 0, K.COBBLE)           # the harbour front
    # A stone jetty, not a wooden one: Outside_A2 kind 22 reads as decking but
    # is flagged impassable in every direction, so a pier built out of it is a
    # pier nobody can stand on.
    g.fill(19, 26, 20, 31, 0, K.PAVING)           # the jetty, over the water

    g.building(*COTTAGE, wall=K.WALL_PLASTER, roof=K.ROOF_BROWN)
    g.building(*OUTFIT, wall=K.WALL_PLANK_LIGHT, roof=K.ROOF_GREEN)
    g.building(*WYVERN, wall=K.WALL_TIMBER, roof=K.ROOF_BROWN, wall_rows=3)
    # Three rows of ashlar and a shallow gold roof: the Guild is the one
    # building in Nether Sopping with an opinion of itself.
    g.building(*GUILD, wall=K.WALL_STONE, roof=K.ROOF_GOLD, wall_rows=3)
    # Two sheds with no doors you can open, to fill the plots out. A town made
    # only of buildings you can enter is a town with four buildings in it.
    g.building(34, 11, 5, 5, wall=K.WALL_LOG, roof=K.ROOF_BROWN)
    g.building(3, 19, 5, 5, wall=K.WALL_PLANK, roof=K.ROOF_BROWN)
    g.building(12, 4, 6, 5, wall=K.WALL_PLASTER, roof=K.ROOF_GREEN)
    g.building(29, 19, 5, 5, wall=K.WALL_PLANK_LIGHT, roof=K.ROOF_BROWN)

    g.autotile(0)

    # -- signs and windows on the fronts. A front is laid out outward from its
    # door: sign, gap, door, gap, sign, and the windows out at the corners. The
    # windows used to be listed at the two tiles either side of the door, which
    # is where the signs are, so the outfitters' and the Guild's signs were
    # drawn and then painted over and the shops had no sign at all.
    g.set(WYVERN_DOOR[0] - 2, WYVERN_DOOR[1], 3, K.SIGN_MUG)
    g.set(WYVERN_DOOR[0] + 2, WYVERN_DOOR[1], 3, K.SIGN_INN)
    g.set(OUTFIT_DOOR[0] - 2, OUTFIT_DOOR[1], 3, K.SIGN_ARMOR)
    g.set(OUTFIT_DOOR[0] + 2, OUTFIT_DOOR[1], 3, K.SIGN_POTION)
    g.set(GUILD_DOOR[0] - 2, GUILD_DOOR[1], 3, K.SIGN_BLADE)
    g.set(GUILD_DOOR[0] + 2, GUILD_DOOR[1], 3, K.SIGN_PLATE)
    g.set(COTTAGE_DOOR[0] - 2, COTTAGE_DOOR[1], 3, K.WINDOW)
    # The four sheds get a shut door, two tiles tall, standing on the bottom
    # wall row. A bare black tile there is the inside of an opening with no
    # opening drawn round it, and reads as a hole somebody forgot to tile.
    for x, y in SHED_DOORS:
        g.column(x, y, 3, K.DOOR_SHUT)
    for x, y in [(7, 16), (8, 16), (14, 16), (15, 16), (26, 8), (33, 8),
                 (26, 17), (33, 17),
                 (5, 8), (9, 8), (35, 15), (38, 15), (4, 23), (7, 23),
                 (12, 8), (16, 8), (29, 23), (33, 23)]:
        g.set(x, y, 3, K.WINDOW)
    for x, y in [(7, 14), (15, 14), (28, 6), (28, 14), (36, 12), (5, 20),
                 (13, 5), (30, 20)]:
        g.set(x, y, 2, K.STOVEPIPE)

    # -- street furniture. Nether Sopping is a working harbour and looks it.
    for x, y in [(18, 10), (21, 10), (18, 19), (21, 19)]:
        g.column(x, y, 3, K.LAMP)

    # -- the market. It stands in the block between the street and the Guild,
    # which is the only open ground in the middle of the town; the tavern has
    # the whole of the west side and there is no room in front of it.
    g.blit(21, 12, 3, K.TENT)
    g.blit(24, 12, 3, K.STALL)
    g.blit(24, 15, 3, K.STALL_FRUIT)
    g.blit(21, 16, 3, K.STALL)
    g.blit(17, 12, 3, K.STALL_FRUIT)              # in the lane down the side
    g.set(22, 3, 3, K.SIGNPOST)                   # the town sign
    for x in (17, 18, 22, 23):                    # railings along the quay
        g.set(x, 25, 3, K.FENCE_PANEL)
    for x, y in [(4, 10), (10, 10), (24, 10), (31, 10), (3, 16), (34, 20)]:
        g.set(x, y, 3, K.FENCE_PANEL)
    g.scatter([(16, 23), (24, 23), (17, 21), (23, 21), (13, 22), (27, 22)],
              3, K.BARREL)
    g.scatter([(24, 21), (15, 24), (25, 24), (12, 21), (28, 21),
               (12, 23)], 3, K.CRATE)   # what the man on his day off leans on
    g.scatter([(22, 24), (18, 21), (14, 20), (26, 20)], 3, K.TUB)
    g.scatter([(15, 22), (25, 22), (18, 24), (21, 22)], 3, K.BUCKET)
    g.scatter([(12, 25), (29, 24), (33, 26), (6, 26), (9, 24), (31, 25)],
              3, K.LOGS)
    g.scatter([(2, 25), (37, 25), (10, 26), (30, 26), (1, 21), (38, 21)],
              3, K.ROCK2)
    g.scatter([(2, 22), (37, 22), (11, 26), (29, 27)], 3, K.REEDS)
    g.scatter([(4, 16), (34, 16), (25, 11), (30, 11), (17, 15), (22, 15)],
              3, K.POT)
    # Nothing on row 18: that is the lower street, and it is one tile deep
    # where it runs past the sheds.
    g.scatter([(17, 14), (18, 16), (35, 22)], 3, K.CRATE)
    g.scatter([(17, 16), (25, 14), (22, 19), (16, 19)], 3, K.BARREL)
    g.scatter([(3, 11), (35, 21), (11, 9), (25, 8)], 3, K.BUSH)
    g.scatter([(23, 6), (2, 12), (37, 8)], 3, K.FLOWERS3)
    g.scatter([(24, 7), (2, 6), (35, 5)], 3, K.FLOWERS2)
    # Quy's roses, such as they are: in the strip of grass beside his cottage,
    # which is the only ground he has that the harbour has not been paved over.
    g.set(11, 6, 3, K.FLOWERS)
    g.set(11, 7, 3, K.FLOWERS)
    g.scatter([(34, 4), (36, 8), (2, 4), (35, 3)], 3, K.LILYPAD)

    # -- trees along the landward sides, and a gap for the road
    for x in range(0, TOWN_W - 1, 2):
        if not (SOPPING_GATE[0] - 1 <= x <= SOPPING_GATE[0]):
            g.blit(x, 0, 3, K.TREE_DARK if x % 4 else K.TREE)
    for y in range(2, 18, 2):
        g.blit(0, y, 3, K.TREE if y % 4 else K.TREE_DARK)
        if not 10 <= y <= 14:        # the boat shed stands in the eastern trees
            g.blit(TOWN_W - 2, y, 3, K.TREE_DARK if y % 4 else K.TREE)
    for x, y in [(2, 8), (37, 4), (24, 3), (10, 2)]:
        g.blit(x, y, 3, K.TREE)

    m = K.new_map(TOWN_W, TOWN_H, K.TS_OUTSIDE, name="Nether Sopping",
                  bgm="Town6")
    m["data"] = g.data
    m["events"] = [None] + sopping_events()
    return m


def sopping_events():
    evs = []

    # -- 1: the way back out to the world map ---------------------------------
    out = S.narrate(["The road north, back towards Thistlewick.",
                     "Nobody in Nether Sopping uses it much."])
    out += R.choice_block(
        ["Go north", "Stay"],
        [[R.play_se("Move1"),
          R.transfer(MAP_WORLD, WORLD_SOPPING_STEP[0], WORLD_SOPPING_STEP[1],
                     2, 0)], []])
    evs.append(R.event(1, "North Road", *SOPPING_GATE, [R.page(
        out, img=R.image(""), trigger=1, priority=0, through=True)]))

    # -- 2-5: the four doors ---------------------------------------------------
    evs.append(S.door(2, "Cottage Door", *COTTAGE_DOOR, MAP_COTTAGE,
                      *arrival(MAP_COTTAGE)))
    evs.append(S.door(3, "Outfitters Door", *OUTFIT_DOOR, MAP_OUTFIT,
                      *arrival(MAP_OUTFIT)))
    evs.append(S.door(4, "Slain Wyvern Door", *WYVERN_DOOR, MAP_WYVERN,
                      *arrival(MAP_WYVERN)))
    evs.append(S.door(5, "Guild Door", *GUILD_DOOR, MAP_GUILD,
                      *arrival(MAP_GUILD)))

    # -- 6: the town sign ------------------------------------------------------
    evs.append(S.sign(6, "Town Sign", 22, 3, [
        "\\C[6]NETHER SOPPING\\C[0]",
        "'THE SEA IS RIGHT THERE'",
        "Underneath, in a different hand:",
        "'IT IS. WE CHECKED.'"]))

    # -- 7: the memorial, which is the quiet one ------------------------------
    memorial = S.narrate([
        "A standing stone on the harbour front, with",
        "names cut into it. Not forty-seven names.",
        "A hundred and eighty-one."])
    memorial += S.narrate([
        "The Chosen Ones are on it, but so is everyone",
        "who went with them: healers, hired swords,",
        "cousins, a cook, somebody listed only as",
        "'the lad who carried the rope'."])
    memorial += S.narrate([
        "Thistlewick's Wall of the Forty-Seven has",
        "forty-seven portraits on it.",
        "Nobody in Thistlewick has ever counted the",
        "difference."])
    memorial += [S.trope()]
    # The memorial carries its own sprite rather than sitting on a scenery
    # tile: it is the one thing on this map that has to be looked at, and an
    # invisible event on an empty flagstone is a thing nobody looks at.
    stone = R.image("!Other2", 4, direction=2, pattern=1)
    evs.append(R.event(7, "The Memorial Stone", 16, 21, [
        R.page(memorial + [R.self_switch("A", True)], img=stone,
               trigger=0, priority=1, direction_fix=True),
        R.page(S.narrate(["A hundred and eighty-one names, and room",
                          "underneath for more. There is always room",
                          "underneath for more."]),
               img=stone, trigger=0, priority=1, direction_fix=True,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ]))

    # -- 8: the ferryman, whose tide is never right ---------------------------
    ferry = S.say("Ferryman", [
        "Passage? Aye. Where to?"])
    ferry += S.narrate(["You ask what the options are."])
    ferry += S.say("Ferryman", [
        "Anywhere. Anywhere at all.",
        "Islands. The far shore. That bit on the map",
        "with the writing you can't read."])
    ferry += S.narrate(["He looks at the water for a while."])
    ferry += S.say("Ferryman", [
        "Tide's wrong today, mind.",
        "Come back tomorrow."])
    again = S.say("Ferryman", ["Tide's still wrong.",
                               "It's been wrong since I bought the boat."])
    evs.append(talker(8, "Ferryman", 20, 30, "Ferryman", ferry, again,
                      direction=4))

    # -- 9: two children, playing the only game there is ----------------------
    kids = S.narrate([
        "Two children are playing Chosen One.",
        "The rules appear to be that one of them walks",
        "north and the other one has to be the Dark",
        "Lord and lose."])
    kids += S.say("Sops", [
        "I was the Dark Lord LAST time.",
        "You be the Dark Lord."])
    kids += S.narrate(["Neither of them wants to be the Dark Lord.",
                       "They settle it, eventually, by both being",
                       "the Chosen One and agreeing that the Dark Lord",
                       "has stayed at home today."])
    kids += S.narrate(["Which, as solutions go, is well ahead of",
                       "anything the Prophecy Committee has managed."])
    again = S.say("Sops", ["The Dark Lord's stayed home again.",
                           "He does that now."])
    # Fixed, not wandering: they are one tile off the lower street and a
    # random walker there is a random blockage on the way to the Guild.
    evs.append(talker(9, "Children Playing", 24, 19, "Sops", kids, again))

    # -- 10: the fish stall ----------------------------------------------------
    stall = S.say("Merchant", [
        "Fish. Chowder. Biscuit.",
        "The biscuit's older than the fish and it'll",
        "outlive the both of us."])
    stall += R.shop([(0, db.IT_CHOWDER, 0, 0), (0, db.IT_BISCUIT, 0, 0),
                     (0, db.IT_PALE, 0, 0), (0, db.IT_POTION, 0, 0)])
    evs.append(S.npc(10, "Fish Stall", 22, 22, stall, "People2", 4,
                     direction=4))

    # -- 11: a man having a day off -------------------------------------------
    boat = S.narrate([
        "A man is asleep against a stack of crates with",
        "a very good sword across his knees."])
    boat += S.say("Regular", [
        "...Mm? No. Not today.",
        "Thirty-one years I've done this. Today I'm",
        "having a day off."])
    boat += S.narrate(["You have not asked him anything."])
    boat += S.say("Regular", [
        "You were going to. They always are.",
        "There's a lad in the Wyvern who'll go with",
        "anyone. Ask him. Let me sleep."])
    again = S.say("Regular", ["Still off. Ask in the Wyvern."])
    evs.append(talker(11, "Man Having A Day Off", 13, 23, "Regular", boat,
                      again, direction=8))

    # -- 12: the harbour notice ------------------------------------------------
    evs.append(S.sign(12, "Harbour Notice", 24, 25, [
        "\\C[6]HARBOUR RULES\\C[0]",
        "1. No adventuring on the pier.",
        "2. The crab on the west beach is nobody's",
        "   fault and is not to be provoked.",
        "3. Rule 2 is not a challenge."]))

    # -- 13-16: the four shut doors -------------------------------------------
    # A door you cannot open is a promise the town is bigger than the four
    # rooms in it. It has to answer when you try it, though, or it is just a
    # door that has stopped working.
    shut = [
        ("The Boat Shed", ["Locked. Through the window: eleven boats,",
                           "all of them upside down, all of them",
                           "belonging to somebody who went north."]),
        ("The Net Loft", ["Nets, drying. A hand-lettered card on the",
                          "door: 'IF YOU ARE HERE ABOUT THE ROPE, THE",
                          "ROPE IS SPOKEN FOR.'"]),
        ("A Front Door", ["Somebody's front door. There is a boot",
                          "scraper, and a pot with a dead thing in it,",
                          "and no answer."]),
        ("The Chandler's", ["Shut. A card in the window gives the hours,",
                            "and the hours are 'when the light is on at",
                            "the point'. The light has been out since",
                            "spring."]),
    ]
    for i, ((name, lines), (x, y)) in enumerate(zip(shut, SHED_DOORS)):
        evs.append(S.sign(13 + i, name, x, y + 1, lines))

    # -- 17: the other child. Event 9 says two children are playing, and for a
    # while there was only one of them on the map, which makes the narration
    # read like a bug rather than a scene.
    tibb = S.say("Tibb", [
        "We're both the Chosen One now.",
        "Nobody's the Dark Lord. He's at home."])
    tibb += S.narrate([
        "The arrangement has held for four days, which",
        "is longer than most treaties in the district."])
    tibb_again = S.say("Tibb", ["Still no Dark Lord.",
                                "Still working."])
    evs.append(talker(17, "The Other Child", 25, 19, "Tibb", tibb,
                      tibb_again, direction=4))
    return evs


# ================================================================ interiors ==
ROOMS = {
    #                w   h  x1  y1  x2  y2  door_x
    MAP_WYVERN:     (25, 21, 3, 4, 21, 15, 12),
    MAP_GUILD:      (19, 17, 3, 4, 15, 11, 9),
    MAP_OUTFIT:     (17, 16, 3, 4, 13, 10, 8),
    MAP_COTTAGE:    (17, 16, 3, 4, 13, 10, 8),
    MAP_LIGHTHOUSE: (13, 25, 3, 4, 9, 19, 6),
}


def arrival(map_id):
    _, _, _, _, _, y2, door_x = ROOMS[map_id]
    return door_x, y2


def threshold(map_id):
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


# ========================================================= the Slain Wyvern ==
def wyvern_map():
    """A long room with a big fire, a bar along the west wall, and eleven
    people who have all been on a quest."""
    g = room(MAP_WYVERN, floor=K.IN_WOOD_FLOOR, floor_alt=K.IN_DARK_WOOD)
    g.fill(9, 7, 13, 11, 0, K.IN_RED_RUG)         # the rug everyone stands on
    g.fill(17, 10, 20, 13, 0, K.IN_GREEN_RUG)     # the fire end, which is
    g.autotile(0)                                 # where the good chairs are

    for x, shelf in ((3, K.IN_SHELF_BOTTLES), (4, K.IN_SHELF_JARS),
                     (5, K.IN_SHELF_GOODS), (6, K.IN_SHELF_FRUIT)):
        g.column(x, 3, 2, shelf)
    # The bar. Inside_B's round table carries the counter flag (0x80), which
    # is what lets the action button reach the landlady standing behind it -
    # so the bar is built out of tables and Dorcas stands in the gap.
    for x in range(3, 7):
        g.set(x, 6, 2, K.IN_TABLE_ROUND)
    g.set(3, 6, 3, K.INC_BOTTLES)
    g.set(5, 6, 3, K.INC_GOBLET)
    g.set(6, 6, 3, K.INC_MEAL2)

    # The east end of the bar, added for NORTH.md 3.1 and 3.2: Dorcas's board
    # on the wall and the register open on the counter under it. The counter
    # tile carries the counter flag, so the action button reaches the register
    # from the customers' side; the board's event goes on the *lower* of its
    # two tiles, because the upper one is wall and nobody can stand in front
    # of a wall.
    g.column(7, 3, 2, K.IN_NOTICE_BOARD)
    g.set(7, 6, 2, K.IN_TABLE_ROUND)
    # INC_BOOK2, not INC_BOOK: the sheet's `.txt` calls them Closed Book A
    # and Open Book A, and this one is described as open on the bar with
    # forty entries down the page.
    g.set(7, 6, 3, K.INC_BOOK2)

    g.blit(8, 3, 2, K.IN_PIANO)
    g.column(12, 3, 2, K.IN_NOTICE_BOARD)
    g.column(14, 3, 2, K.IN_BOOKCASE)
    g.blit(17, 3, 2, K.IN_FIREPLACE)
    g.column(20, 3, 2, K.IN_BED_ORANGE)
    g.column(21, 3, 2, K.IN_BED_BROWN)
    g.column(10, 3, 2, K.IN_CLOCK)
    g.column(16, 3, 2, K.IN_CURTAIN_RED)

    for tx, ty in [(8, 8), (8, 11), (11, 8), (11, 12), (15, 7), (19, 8),
                   (6, 13), (16, 13), (18, 12), (5, 9)]:
        g.set(tx, ty, 2, K.IN_TABLE_ROUND)
    g.scatter([(9, 9), (12, 9), (17, 7), (20, 11), (7, 14), (15, 14)],
              2, K.IN_TABLE_SMALL)
    g.set(8, 8, 3, K.INC_GOBLET)
    g.set(11, 8, 3, K.INC_MEAL2)
    g.set(8, 11, 3, K.INC_BOTTLE)
    g.set(15, 7, 3, K.INC_MEAL)
    g.set(19, 8, 3, K.INC_BOTTLES)
    g.set(6, 13, 3, K.INC_CANDLES)
    g.set(16, 13, 3, K.INC_BOOK)
    g.set(11, 12, 3, K.INC_GOBLET)
    g.set(18, 12, 3, K.INC_CANDLES)
    g.set(5, 9, 3, K.INC_MEAL)
    g.set(3, 8, 2, K.IN_BARREL)
    g.set(3, 11, 2, K.IN_BARREL2)
    g.scatter([(21, 15), (3, 15)], 2, K.IN_CRATE)
    g.set(21, 6, 2, K.IN_POT)
    g.set(13, 15, 2, K.IN_POT)
    return finish(MAP_WYVERN, g, "The Slain Wyvern", bgm="Town5",
                  battleback=("Wood1", "Room1"), events=wyvern_events())


def wyvern_events():
    evs = [S.exit_tile(1, "Tavern Door", *threshold(MAP_WYVERN), MAP_SOPPING,
                       *OUT[MAP_WYVERN])]
    evs.append(dorcas_event(2, 4, 5))
    evs.append(hosea_event(3, 9, 6))

    # -- the six tales ---------------------------------------------------------
    evs.append(ysolde_event(4, 5, 11))

    hulda = S.narrate([
        "A woman with a ledger and a stub of pencil is",
        "totting something up and not liking it."])
    hulda += S.say("Hulda", [
        "Twelve bear pelts. That was the job.",
        "Fine. Went and got twelve bear pelts."])
    hulda += S.say("Hulda", [
        "Comes back. He says: ah, no.",
        "A DIFFERENT sort of bear."])
    hulda += S.narrate(["She turns the ledger round so you can see it.",
                        "It is nine pages long. Every line is a thing",
                        "somebody wanted fetched."])
    hulda += S.say("Hulda", [
        "Eleven years. Four hundred and six jobs.",
        "And the last one - the LAST one - I get there",
        "with the thing, and he's moved.",
        "No note. Moved."])
    hulda += S.narrate(["You ask whether she ever found out what any",
                        "of it was for."])
    hulda += S.say("Hulda", [
        "For? It wasn't FOR.",
        "That's the bit nobody tells you.",
        "It was a list. I was the legs."])
    hulda_again = S.say("Hulda", [
        "If anyone asks you to fetch twelve of",
        "anything, ask what the thirteenth is for."])
    evs.append(tale(5, "Hulda Bole (the Fetcher)", 4, 9, "Hulda",
                    hulda, hulda_again, direction=6))

    nabb = S.narrate([
        "Two people at the same table, not eating."])
    nabb += S.say("Nabb", [
        "You've been in the Gloamwood, then.",
        "Sitting on a log, is he."])
    nabb += S.narrate(["They are the rest of Chosen One #46's party.",
                       "There were five of them. There are two here."])
    nabb += S.say("Nabb", [
        "He stopped. Just - stopped, on the path,",
        "and said the woods were enough.",
        "And we looked at each other, and we said:",
        "fair."])
    nabb += S.say("Nabb", [
        "That's the whole story. Everyone wants",
        "there to be more. There isn't more.",
        "We were tired, and he said the woods were",
        "enough, and he was right, and we went home."])
    nabb += S.narrate(["You ask if they ever hear from him."])
    nabb += S.say("Nabb", [
        "We write. Every month, the both of us.",
        "He's never once written back."])
    nabb += S.say("Nabb", ["He reads them, though.",
                           "The man who collects the post says so."])
    nabb_again = S.say("Nabb", [
        "Post goes out Thursdays. Tolly does",
        "the stamps. It's something to do."])
    evs.append(tale(6, "Nabb (of the Forty-Sixth)", 7, 11, "Nabb", nabb,
                    nabb_again, direction=6))

    tolly = S.say("Tolly", [
        "She asks about the letters, does she.",
        "Nabb thinks I don't know they're",
        "unanswered. Nabb has thought that for",
        "eleven years."])
    tolly += S.narrate(["She goes back to addressing an envelope."])
    tolly_again = S.say("Tolly", [
        "Two stamps. It's a long way, and",
        "he's worth two stamps."])
    evs.append(talker(7, "Tolly (of the Forty-Sixth)", 6, 11, "Tolly", tolly,
                      tolly_again, direction=6))

    merrow = S.narrate([
        "A big man in old armour, drinking carefully."])
    merrow += S.say("Merrow", [
        "The bridge. You'll have heard about",
        "the bridge."])
    merrow += S.narrate(["You have not heard about the bridge."])
    merrow += S.say("Merrow", [
        "Twenty of us. Best-equipped party that",
        "ever went north. We fought him at the",
        "bridge and we lost."])
    merrow += S.say("Merrow", [
        "And here's the thing.",
        "We were MEANT to lose. It was written",
        "down. In advance. Clause fourteen: the",
        "first meeting shall not go well."])
    merrow += S.narrate(["He puts the cup down very precisely."])
    merrow += S.say("Merrow", [
        "Twenty of us, and a document decided",
        "how it went before we got up that morning.",
        "I've made my peace with losing.",
        "I have not made my peace with the paperwork."])
    merrow += S.narrate(["You ask what Grimspite was like."])
    merrow += S.say("Merrow", [
        "...He apologised.",
        "Halfway through, he stopped, and he",
        "apologised, and then he carried on.",
        "I think about that more than the losing."])
    merrow_again = S.say("Merrow", [
        "He apologised. Nobody ever believes",
        "me about that part."])
    evs.append(tale(8, "Merrow Halgate (the Bridge)", 15, 6, "Merrow",
                    merrow, merrow_again))

    dree = S.narrate([
        "An elderly gentleman is sitting alone with",
        "the air of a man who has been sat alone",
        "deliberately."])
    dree += S.say("Dree", [
        "I was the advisor. The kindly old",
        "advisor. You know the sort."])
    dree += S.say("Dree", [
        "Week three, they started watching me.",
        "Week five, the bard wrote a verse about",
        "how my eyes went strange at night.",
        "Week eight they searched my bags."])
    dree += S.narrate(["He refills his cup with great composure."])
    dree += S.say("Dree", [
        "Week eleven they tied me to a chair",
        "and demanded I reveal myself."])
    dree += S.narrate(["You ask what he revealed."])
    dree += S.say("Dree", [
        "That I was a kindly old advisor.",
        "That I had always been a kindly old",
        "advisor. That the strange thing about",
        "my eyes is that I need spectacles."])
    dree += S.say("Dree", [
        "They apologised. They were lovely",
        "about it. Bought me a hat.",
        "And then, for the rest of the quest,",
        "they were just a LITTLE bit careful of me."])
    dree_again = S.say("Dree", [
        "If it helps: I am not the Dark Lord.",
        "I have a certificate. I had to get one."])
    evs.append(tale(9, "Councillor Dree (the Suspect)", 20, 7, "Dree",
                    dree, dree_again, direction=4))

    perp = S.narrate([
        "A young woman with excellent posture and an",
        "expensive tiara she does not appear to have",
        "noticed she is wearing."])
    perp += S.say("Perpetua", [
        "Perpetua Small. I think.",
        "I woke up on the beach six years ago",
        "with no memory and a headache."])
    perp += S.say("Perpetua", [
        "Everyone here has been very kind.",
        "Nobody will tell me anything, but",
        "they've been very kind."])
    perp += S.narrate([
        "Behind her, the entire tavern is looking",
        "very hard at the ceiling."])
    perp += S.say("Perpetua", [
        "I can ride. I can fence. I speak four",
        "languages and I don't know why.",
        "And when I walk into a room, people",
        "stand up. They stand up! For me!"])
    perp += S.narrate(["You consider telling her.",
                       "The tavern, as one, silently begs you not to.",
                       "It has been six years. They want to see",
                       "her get there on her own."])
    perp += S.say("Perpetua", [
        "It'll come back to me.",
        "Probably something dull. Dairy, I expect."])
    perp_again = S.say("Perpetua", [
        "I've been thinking. Cheesemaking.",
        "It would explain the four languages."])
    # One command appended to the end of her list, and not one syllable of it
    # altered: Dorcas has something to say about Perpetua and cannot read
    # another event's self switch to find out whether you have met her.
    evs.append(tale(10, "Perpetua Small (the Amnesiac)", 17, 11, "Perpetua",
                    perp, perp_again, direction=4,
                    extra=[R.control_switch(db.SW_GERALD, True)]))

    # -- the three who will come with you -------------------------------------
    evs.append(corvin_event(11, 20, 14))
    evs.append(wren_event(12, 14, 13))
    evs.append(roland_event(13, 18, 9))

    # -- the wyvern ------------------------------------------------------------
    evs.append(the_wyvern(14, 18, 4))

    # -- two very ordinary travellers -----------------------------------------
    trav = S.say("Traveller", [
        "Good evening. We are peasants."])
    trav += S.narrate(["They are wearing crowns."])
    trav += S.say("Traveller", [
        "Peasant crowns. Very common where",
        "we come from. Which is a farm."])
    trav += S.say("Also A Traveller", [
        "A small farm. Beans, mostly."])
    trav += S.narrate([
        "Nether Sopping has been letting these two get",
        "away with this for four months and is starting",
        "to enjoy it."])
    trav_again = S.say("Traveller", ["Beans. As discussed."])

    # NORTH.md 3.6. They are royalty in disguise **and** newlyweds, and the
    # second only surfaces once you have found room four. Every existing line
    # - the peasant crowns, the small farm, the beans - stays exactly where it
    # is and is still what a first-time player meets.
    #
    # One joke with two mouths, and either of them can be asked first, so the
    # bump hangs off a global switch rather than a self switch: a self switch
    # is keyed on (map, event id, letter) and these are two events. Whichever
    # you ask counts; the other one does not count again.
    trav_four = S.say("Traveller", [
        "We are peasants, and we are",
        "unacquainted.",
    ])
    trav_four += S.say("Also A Traveller", ["We met on the road."])
    trav_four += S.say("Traveller", ["Yesterday."])
    trav_four += S.say("Also A Traveller", ["Yesterday."])
    trav_four += S.narrate([
        "They are holding hands.",
        "They have been holding hands the entire time.",
    ])
    trav_four += travellers_count()
    trav_four += [R.self_switch("B", True)]
    trav_four_again = S.say("Traveller", [
        "Beans.",
        "We have been discussing beans.",
    ])
    img_trav = R.image(*S.FACES["Traveller"], direction=6)
    evs.append(talker(15, "A Very Ordinary Traveller", 4, 14, "Traveller",
                      trav, trav_again, direction=6, pages=[
        R.page(trav_four, img=img_trav, trigger=0, priority=1,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_ROOM_FOUR}),
        R.page(trav_four_again, img=img_trav, trigger=0, priority=1,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_ROOM_FOUR,
                           "selfSwitchValid": True, "selfSwitchCh": "B"}),
    ]))

    trav2 = S.say("Also A Traveller", [
        "Do not curtsey. Nobody does.",
        "We are beans people."])
    trav2 += S.narrate(["You had not curtseyed."])
    trav2 += S.say("Also A Traveller", ["Well. Don't start."])
    trav2_again = S.say("Also A Traveller", ["Beans."])

    trav2_four = S.say("Also A Traveller", [
        "We are unacquainted.",
        "Do not read anything into the hand.",
    ])
    trav2_four += S.narrate(["You had not read anything into the hand."])
    trav2_four += S.say("Also A Traveller", ["Well. Don't start."])
    trav2_four += S.say("Traveller", ["We met on the road. Yesterday."])
    trav2_four += S.say("Also A Traveller", ["Yesterday."])
    trav2_four += travellers_count()
    trav2_four += [R.self_switch("B", True)]
    trav2_four_again = S.say("Also A Traveller", ["Beans. Anniversary beans."])
    img_trav2 = R.image(*S.FACES["Also A Traveller"], direction=6)
    evs.append(talker(16, "Also A Very Ordinary Traveller", 5, 14,
                      "Also A Traveller", trav2, trav2_again, direction=6,
                      pages=[
        R.page(trav2_four, img=img_trav2, trigger=0, priority=1,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_ROOM_FOUR}),
        R.page(trav2_four_again, img=img_trav2, trigger=0, priority=1,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_ROOM_FOUR,
                           "selfSwitchValid": True, "selfSwitchCh": "B"}),
    ]))

    # -- the potboy ------------------------------------------------------------
    sops = S.say("Sops", [
        "Are you a Chosen One? You look like",
        "a Chosen One. It's the standing."])
    sops += S.narrate(["You ask what the standing is."])
    sops += S.say("Sops", [
        "Like you're waiting for someone to",
        "tell you where to go. All of 'em do it.",
        "Mrs Thrupp says it's the prophecy",
        "posture and it ruins the chairs."])
    sops_again = S.say("Sops", ["You're doing the standing again."])

    # NORTH.md 3.2. A third page, on the switch room four sets, and a fourth
    # so the bit stops rather than loops - which is the shape `talker` already
    # has, one layer up. Not a syllable of the two pages above is touched, and
    # a player who never finds the board never sees either of these.
    #
    # The child asks the correct question, is answered with pastry, and is
    # entirely satisfied. He must never work it out.
    sops_four = S.say("Sops", [
        "The Forty-Second and his wife are in.",
        "They come every year for the anniversary.",
    ])
    sops_four += S.say("Sops", ["They're SIXTY."])
    sops_four += S.say("Sops", [
        "Mrs Thrupp says good for them, and I",
        "said good for what, and got a bun.",
    ])
    sops_four += [S.blush(), R.self_switch("B", True)]
    sops_four_again = S.say("Sops", [
        "Room four's still not been down.",
        "I've stopped taking the tray up.",
        "I leave it and go.",
    ])
    img_sops = R.image(*S.FACES["Sops"], direction=8)
    evs.append(talker(17, "Sops the Potboy", 9, 14, "Sops", sops, sops_again,
                      direction=8, move_type=1, pages=[
        R.page(sops_four, img=img_sops, trigger=0, priority=1, move_type=1,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_ROOM_FOUR}),
        R.page(sops_four_again, img=img_sops, trigger=0, priority=1,
               move_type=1,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_ROOM_FOUR,
                           "selfSwitchValid": True, "selfSwitchCh": "B"}),
    ]))

    # -- NORTH.md 3.1 and 3.2. Two new things to click on at the east end of
    # the bar. Both are pattern one - a new event - and neither of them
    # touches a line anybody in this room already had.
    evs.append(dorcas_board(19, 7, 4))
    evs.append(the_register(20, 7, 6))

    evs.append(S.prop(18, "The Wyvern's Plaque", 17, 4, [
        "A brass plaque under the mounted wyvern:",
        "'SLAIN BY H. VANCE, CHOSEN ONE #41,",
        "IN THE MARSHES, AFTER A LONG STRUGGLE.'",
        "Somebody has polished it recently."],
        "", 0, extra=[S.trope()]))
    return evs


def dorcas_event(event_id, x, y):
    """The landlady. Four pages, because she is also the far end of the Feud,
    and which page you get is the state of a thirty-year argument."""
    img = R.image("People4", 5, direction=2)

    def beds(lines):
        cmds = S.say("Dorcas", lines)
        cmds += R.choice_block(
            ["Take a room (25cr)", "Not tonight"],
            [R.if_then(
                R.condition_script("$gameParty.gold() >= 25"),
                [R.lose_gold(25), R.fadeout_screen(), R.play_me("Inn2"),
                 R.recover_all(), R.wait(90), R.fadein_screen()] +
                S.say("Dorcas", [
                    "Twelve hours you slept. Twelve!",
                    "And up like new. Adventurers.",
                    "It's the bedding I mind. You lot heal",
                    "in it and it never recovers."]),
                S.say("Dorcas", ["Come back with 25."]))],
            cancel=None)
        return cmds

    first = beds([
        "Dorcas Thrupp. Beds are 25.",
        "Breakfast is fish. Don't ask what fish."])

    # She is waiting for the jar and will not say so.
    takes_jar = S.say("Dorcas", [
        "That's my sister's hand on that label.",
        "Give it here."])
    takes_jar += S.narrate([
        "She takes the jar, holds it up to the light,",
        "and goes an interesting colour."])
    takes_jar += S.say("Dorcas", [
        "Thirty years. THIRTY.",
        "And she sends me THIS."])
    takes_jar += S.narrate(["You ask what it is.",
                            "She does not tell you.",
                            "She puts it on the highest shelf, where it",
                            "can be seen from every table in the room."])
    takes_jar += [R.gain_item(db.IT_JAR, -1), R.play_se("Item1"), R.wait(20)]
    takes_jar += S.say("Dorcas", [
        "Right. You'll be going back north.",
        "Wait there."])
    takes_jar += S.narrate([
        "There is a sound from the back room like",
        "someone doing carpentry to a hamper."])
    takes_jar += [R.gain_item(db.IT_REPLY, 1), R.play_me("Item")]
    takes_jar += S.narrate([
        "Got \\I[192]\\C[3]A Reply, Sealed\\C[0].",
        "It is heavier than the jar was.",
        "Considerably heavier."])
    takes_jar += S.say("Dorcas", [
        "Don't open it. Don't shake it.",
        "Don't let it near a fire.",
        "And tell her I send my love, because",
        "I do, and she knows I do, and that's her lot."])
    takes_jar += [R.control_switch(db.SW_FEUD_JAR, False),
                  R.control_switch(db.SW_FEUD_REPLY, True), S.trope()]
    takes_jar += beds(["Bed's 25 if you're stopping.",
                       "You've earned it, carrying that."])

    waiting = beds([
        "Still here? That reply doesn't",
        "walk north on its own.",
        "Bed's 25 if you're stopping."])

    done = beds([
        "She wrote. First in thirty years.",
        "Four pages, and two of them are about you.",
        "Bed's 25. For you it's still 25, don't",
        "start."])

    # NORTH.md 3.7, and the one page in the game that turns its own condition
    # off on the way out.
    #
    # `Game_Event.refresh` takes the **last** page whose conditions hold, so a
    # fifth page here wins over all four above it - including the jar handover
    # and the reply, which are a thirty-year quest and cannot be shadowed. So
    # it fires once, the next time you speak to her after hearing Perpetua's
    # tale, and then clears `SW_GERALD` and gets out of the way for good. Ask
    # again immediately and the feud is exactly where you left it.
    #
    # Nothing is explained. The ceiling does the work, which is the machinery
    # this room already built for Perpetua herself.
    gerald = S.narrate([
        "You mention that you have been talking to",
        "Perpetua Small.",
    ])
    gerald += S.say("Dorcas", ["There was a Gerald."])
    gerald += S.narrate([
        "Behind you, the entire tavern is looking very",
        "hard at the ceiling.",
    ])
    gerald += S.say("Dorcas", ["We handled it."])
    gerald += S.say("Dorcas", [
        "That is all that is being said",
        "about Gerald.",
    ])
    gerald += [S.blush(), R.control_switch(db.SW_GERALD, False)]

    return R.event(event_id, "Dorcas Thrupp", x, y, [
        R.page(first, img=img, trigger=0, priority=1),
        R.page(takes_jar, img=img, trigger=0, priority=1,
               conditions={"switch1Valid": True, "switch1Id": db.SW_FEUD_JAR}),
        R.page(waiting, img=img, trigger=0, priority=1,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_FEUD_REPLY}),
        R.page(done, img=img, trigger=0, priority=1,
               conditions={"switch1Valid": True, "switch1Id": db.SW_FEUD_DONE}),
        R.page(gerald, img=img, trigger=0, priority=1,
               conditions={"switch1Valid": True, "switch1Id": db.SW_GERALD}),
    ])


def dorcas_board(event_id, x, y):
    """NORTH.md 3.1: room four. Dorcas is *delighted*; she is not being arch,
    and there is nothing in what she says that is not a landlady being pleased
    with a quiet pair of guests.

    Sets `SW_ROOM_FOUR`, which the potboy and the two travellers read."""
    board = S.narrate([
        # "board", not "slate": the tile is IN_NOTICE_BOARD, which is a
        # framed paper notice under a pair of crossed swords, and the
        # room the player is looking at should be the room the line
        # describes.
        "A board by the bar. Rooms down the left,",
        "names down the right, in a small neat hand.",
        "Room four has a line drawn through it.",
    ])
    board += S.say("Dorcas", [
        "Room four?",
        "Not been down since Tuesday.",
    ])
    board += S.say("Dorcas", [
        "Best guests I have ever had.",
        "No trouble. No noise to speak of.",
    ])
    board += S.say("Dorcas", [
        "I leave the tray on the mat.",
        "Lovely to see young people happy.",
    ])
    board += [S.blush(), R.control_switch(db.SW_ROOM_FOUR, True),
              R.self_switch("A", True)]

    again = S.narrate([
        "Room four still has a line drawn through it.",
    ])
    again += S.say("Dorcas", ["Tray's still on the mat."])
    return R.event(event_id, "Dorcas's Board", x, y, [
        R.page(board, img=R.image(""), trigger=0, priority=1,
               direction_fix=True, through=True),
        R.page(again, img=R.image(""), trigger=0, priority=1,
               direction_fix=True, through=True,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ])


def the_register(event_id, x, y):
    """NORTH.md 3.2: the accidental record. A document does not know what it
    is saying, and this one has been corrected by somebody who did."""
    look = S.narrate([
        "The house register, open on the bar.",
        "Name, town, nights - and a last column headed",
        "PURPOSE OF VISIT.",
    ])
    look += S.narrate([
        "Forty entries down the page.",
        "Thirty-nine of them say 'business'.",
    ])
    look += S.narrate([
        "The fortieth said something else. It has been",
        "crossed out - once, neatly, in a different",
        "hand - and 'business' written above it.",
    ])
    look += S.narrate([
        "The different hand is Dorcas's.",
        "She has not made a fuss about it.",
        "She has simply written 'business'.",
    ])
    look += [S.blush(), R.self_switch("A", True)]

    again = S.narrate([
        "Forty entries. Thirty-nine say 'business'.",
        "The fortieth says 'business' too, now.",
    ])
    return R.event(event_id, "The House Register", x, y, [
        R.page(look, img=R.image(""), trigger=0, priority=1,
               direction_fix=True, through=True),
        R.page(again, img=R.image(""), trigger=0, priority=1,
               direction_fix=True, through=True,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ])


def hosea_event(event_id, x, y):
    """The scribbler who is paying for the six tales. This is the quest that
    rewards the player for listening, which is the whole design of the room."""
    img = R.image("People4", 0, direction=2)

    ask = S.narrate([
        "A man with ink on both hands is writing in a",
        "book so large it has its own table."])
    ask += S.say("Hosea", [
        "Hosea Bellwether. I am compiling",
        "'A Complete And Accurate History Of",
        "The Obligatory Quest'."])
    ask += S.narrate(["You ask how it is going."])
    ask += S.say("Hosea", [
        "Complete is going well.",
        "Accurate is the problem."])
    ask += S.say("Hosea", [
        "Everyone in this room has been on one.",
        "Not one of them will tell a historian.",
        "They'll tell YOU, though. You're going",
        "north. You're in it."])
    ask += S.say("Hosea", [
        "Six first-hand accounts. Go and be",
        "told six stories properly - listen to",
        "the ends of them - and come back.",
        "I pay. Handsomely, for a man with ink hands."])
    ask += [R.control_switch(db.SW_HISTORY_ASKED, True)]

    counting = S.say("Hosea", [
        "How many so far?"])
    counting += S.narrate(["\\C[3]\\V[4]\\C[0] of the six, by his count."])
    counting += S.say("Hosea", [
        "Ysolde. Hulda. Nabb. Merrow.",
        "Dree. And the young lady with the",
        "tiara, who is going to work it out",
        "any day now and it will be marvellous."])

    payout = S.say("Hosea", [
        "Six. You actually did it.",
        "Nobody does it. They get two and",
        "go and look at a dungeon."])
    payout += S.narrate(["He writes for a long time without speaking."])
    payout += S.say("Hosea", [
        "There. It is done. It is complete.",
        "It is not accurate - Merrow's bridge",
        "and Dree's chair cannot both be true",
        "on a Tuesday - but it is COMPLETE."])
    payout += [R.gain_gold(1500), R.gain_item(db.IT_HISTORY, 1),
               R.gain_armor(db.AR_FOOTNOTE, 1), R.play_me("Fanfare3")]
    payout += S.narrate([
        "Got 1500\\G, \\I[229]\\C[3]A Complete And Accurate",
        "History\\C[0], and \\I[224]\\C[3]Footnote\\C[0]."])
    payout += S.say("Hosea", [
        "The Footnote's you. Bottom of page",
        "four hundred and one, small type.",
        "It says you listened.",
        "Nobody else has one of those."])
    payout += [R.control_switch(db.SW_HISTORY_DONE, True), S.trope()]

    done = S.say("Hosea", [
        "Off you go, then. North.",
        "I'll leave the last page blank",
        "until I hear how it went.",
        "Come back and tell me. That's the fee."])

    # Page order matters: MZ takes the last page whose conditions hold.
    return R.event(event_id, "Hosea Bellwether", x, y, [
        R.page(ask, img=img, trigger=0, priority=1),
        R.page(counting, img=img, trigger=0, priority=1,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_HISTORY_ASKED}),
        R.page(payout, img=img, trigger=0, priority=1,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_HISTORY_ASKED,
                           "variableValid": True,
                           "variableId": db.VAR_TALES, "variableValue": 6}),
        R.page(done, img=img, trigger=0, priority=1,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_HISTORY_DONE}),
    ])


def ysolde_event(event_id, x, y):
    """Tale one, and - much later - the last thing the expansion has to say."""
    img = R.image("People1", 7, direction=2)

    first = S.narrate([
        "An old woman with a canvas roll of field",
        "medicine open on the table in front of her,",
        "out of habit."])
    first += S.say("Ysolde", [
        "Ysolde Marrow. I kept the Forty-Fourth",
        "alive for nine years, on and off."])
    first += S.narrate(["You ask what the job was like."])
    first += S.say("Ysolde", [
        "The job was a duke's son.",
        "We were paid to walk him from the coast",
        "to the tower. For the exposure, they said.",
        "For his character."])
    first += S.say("Ysolde", [
        "He had four hit points.",
        "I counted them. Four."])
    first += S.say("Ysolde", [
        "He walked into every fight we had.",
        "Not bravely. He just walked in, the way",
        "you walk into a room. Nine weeks.",
        "Nine weeks of standing in front of a boy."])
    first += S.narrate(["You ask whether he made it."])
    first += S.say("Ysolde", [
        "He did. Runs a shipping concern now.",
        "Sent me a card once. Spelled my name",
        "with a Y in the wrong place."])
    first += S.say("Ysolde", [
        "Ambrose used to say that was the whole",
        "trade. You keep someone alive, and then",
        "they go and live, and you don't get to",
        "see much of it. He was right about most things."])

    again = S.say("Ysolde", [
        "Ambrose Fitch. The Forty-Fourth.",
        "They put him in a mound out east",
        "with a curse on it. Forty years they",
        "ignored him, and then they did THAT."])

    # After the bench: the reward for the last chain in the game.
    bench = S.narrate([
        "Ysolde Marrow looks up before you have said",
        "anything at all."])
    bench += S.say("Ysolde", [
        "You've been out to the mound."])
    bench += S.narrate(["You tell her what he asked for.",
                        "You tell her that it is there now, on the",
                        "top, facing the sea."])
    bench += S.narrate([
        "She is quiet for what feels like a long time.",
        "Nobody in the room looks over. Everybody in",
        "the room is listening."])
    bench += S.say("Ysolde", [
        "Forty years I've had that argument",
        "with a village I've never been to.",
        "They wanted a hero in a mound.",
        "He wanted somewhere to put his legs up."])
    bench += S.say("Ysolde", [
        "Take this. Don't argue with me,",
        "I'm seventy-eight and I've had a night."])
    bench += [R.gain_armor(db.AR_KIT, 1), R.play_me("Fanfare1")]
    bench += S.narrate(["Got \\I[187]\\C[3]Ysolde's Kit\\C[0].",
                        "Forty years of field medicine in a canvas",
                        "roll, and every fold of it is worn where",
                        "somebody's hand went."])
    bench += S.say("Ysolde", [
        "You're going north. They all go north.",
        "Come back, and I'll want it back,",
        "and I'll be very rude about the state",
        "you've got it into. Do you hear me? Come back."])
    bench += [S.trope(), R.self_switch("B", True)]

    thanks = S.say("Ysolde", [
        "Mind that kit. And mind yourself.",
        "In that order, if you're sensible.",
        "In the other order if you're a Chosen One,",
        "which you are, so never mind."])

    return R.event(event_id, "Ysolde Marrow (the Forty-Fourth's)", x, y, [
        R.page(first + [R.control_variable_add(db.VAR_TALES, 1), S.trope(),
                        R.self_switch("A", True)],
               img=img, trigger=0, priority=1),
        R.page(again, img=img, trigger=0, priority=1,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
        # The bench page wants her tale told first. A player can reach the
        # barrow without ever entering the tavern, and if the payoff fired on
        # a first meeting her tale would be gone and Hosea's six unreachable.
        R.page(bench, img=img, trigger=0, priority=1,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_BENCH_DONE,
                           "selfSwitchValid": True, "selfSwitchCh": "A"}),
        R.page(thanks, img=img, trigger=0, priority=1,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "B"}),
    ])


def the_wyvern(event_id, x, y):
    """The stuffed goose over the fireplace, and the one thing in the south
    that changes if a particular party member is standing behind you."""
    look = S.narrate([
        "Mounted over the fireplace: a wyvern.",
        "Wings out, jaws open, about the size of a",
        "large goose."])
    look += S.narrate(["It is, on any inspection at all, a goose."])

    wren_says = S.say("Wren", [
        "Anser anser. Greylag. Adult female.",
        "Somebody has wired two bats' wings to",
        "a goose and varnished the whole thing."])
    wren_says += S.narrate(["The tavern goes quiet."])
    wren_says += S.say("Dorcas", ["It is a wyvern."])
    wren_says += S.say("Wren", [
        "It is a goose. I can show you the",
        "goose parts. There are, structurally,",
        "only goose parts."])
    wren_says += S.say("Dorcas", [
        "Out. Not for good. Just out,",
        "for a bit, while I decide."])
    wren_says += S.narrate(["Wren is asked to leave the Slain Wyvern.",
                            "She is entirely right, and she is asked to",
                            "leave, and both of those are true at once."])

    others = S.narrate([
        "Nobody in the room looks at it while you are",
        "looking at it, which is its own kind of answer."])

    story = S.say("Dorcas", [
        "Ask, then. Everybody asks."])
    story += S.narrate(["You ask."])
    story += S.say("Dorcas", [
        "Number forty-one. Halloran Vance.",
        "Came back from the marshes with nothing",
        "and a whole village waiting on the quay",
        "for a monster."])
    story += S.say("Dorcas", [
        "So he brought them a monster.",
        "Took him two days with wire and a goose",
        "and he never once smiled about it."])
    story += S.narrate(["She wipes the same patch of bar twice."])
    story += S.say("Dorcas", [
        "It is a wyvern.",
        "He was a good man, and he needed it",
        "to be a wyvern, and it's been a wyvern",
        "in my house for sixty years. So."])
    story += [R.control_switch(db.SW_WYVERN, True), S.trope()]

    cmds = look + R.if_then(
        R.condition_actor_in_party(db.WREN), wren_says, others)
    cmds += story
    return R.event(event_id, "The Wyvern (A Goose)", x, y, [
        R.page(cmds + [R.self_switch("A", True)], img=R.image(""), trigger=0,
               priority=1, direction_fix=True, through=True),
        R.page(S.narrate(["The wyvern. Wings out. Jaws open.",
                          "Sixty years of everybody agreeing."]),
               img=R.image(""), trigger=0, priority=1, direction_fix=True,
               through=True,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ])


# ------------------------------------------------------- the three recruits --
def corvin_event(event_id, x, y):
    pitch = S.narrate([
        "There is a man in the darkest corner of the",
        "room, hood up, one hand on a black sword.",
        "The light does not reach him. He has chosen",
        "the table where the light does not reach."])
    pitch += S.say("Corvin", [
        "...Leave. This road ends in ash."])
    pitch += S.narrate(["You have not said anything yet."])
    pitch += S.say("Corvin", [
        "Corvin Ash.",
        "The scar? Don't ask about the scar."])
    pitch += S.narrate(["You ask about the scar."])
    pitch += S.say("Corvin", [
        "My village was destroyed."])
    pitch += S.narrate(["You say that you are sorry."])
    pitch += S.say("Corvin", [
        "Flooding. I was away.",
        "Everyone was fine. They moved eight miles",
        "inland. There's a school now."])
    pitch += S.narrate(["You wait for the rest of it.",
                        "There is no rest of it."])
    pitch += S.say("Corvin", [
        "You don't understand. NOBODY does.",
        "It's still gone. The place I was FROM",
        "is under six feet of water and everyone",
        "keeps telling me the school is very good."])
    pitch += S.narrate([
        "He has been waiting in this corner for eleven",
        "years for someone to ask him to do something."])

    accept = S.say("Corvin", [
        "...Very well. If fate demands it."])
    accept += S.narrate(["Fate did not demand it. You asked politely."])
    accept += S.say("Corvin", [
        "If FATE demands it, I said.",
        "I have a coat. I'll get the coat.",
        "Don't look pleased, it undermines the whole -",
        "just don't look pleased."])
    accept += [S.trope()]

    decline = S.say("Corvin", [
        "As I foresaw.",
        "I shall remain here. In the dark.",
        "Where the drinks are, incidentally,",
        "somewhat cheaper."])

    full = S.say("Corvin", [
        "Three already? Then my hour is",
        "not yet come.",
        "It never is. That's rather the theme."])

    return S.recruit(event_id, db.CORVIN, "Corvin", x, y, "Actor1", 4,
                     pitch=pitch, accept=accept, decline=decline, full=full,
                     direction=8)


def wren_event(event_id, x, y):
    pitch = S.narrate([
        "A woman in a green cloak has covered an entire",
        "table in specimen jars and is annoyed with one",
        "of them."])
    pitch += S.say("Wren", [
        "Don't jog the table. Nothing in here",
        "is dead enough to be casual about."])
    pitch += S.say("Wren", [
        "Wren Halloway. Cataloguer.",
        "I am four hundred pages into the only",
        "honest monograph on the monsters of this",
        "region, and every page has cost me a fight."])
    pitch += S.narrate(["You ask whether she hunts them."])
    pitch += S.say("Wren", [
        "I DOCUMENT them.",
        "The fighting is a step in the methodology",
        "and I resent it. You cannot measure a wing",
        "that is actively in use."])
    pitch += S.narrate([
        "She turns a jar so the label faces you.",
        "It reads: 'GOBLIN, DISGRUNTLED - grievance",
        "list, partial, transcribed'."])
    pitch += S.say("Wren", [
        "Everyone else names them after how they",
        "died. I name them after what they are.",
        "It's the same job done properly."])

    accept = S.say("Wren", [
        "North? Through the Gloamwood, past",
        "the wall, up an unsurveyed tower?",
        "That is four ecosystems and a boss."])
    accept += S.narrate(["She is already packing jars."])
    accept += S.say("Wren", [
        "I get first refusal on anything unusual,",
        "I write the entries, and nobody - NOBODY -",
        "says 'it's basically a dragon'."])
    accept += [S.trope()]

    decline = S.say("Wren", [
        "Fine. Bring me back a wing, then.",
        "Whole. Not 'mostly'. I have had",
        "'mostly' from better people than you."])

    full = S.say("Wren", [
        "Full party. Of course. Four is",
        "the number, always four.",
        "I have a theory about that and no",
        "funding to pursue it."])

    return S.recruit(event_id, db.WREN, "Wren", x, y, "Actor2", 7,
                     pitch=pitch, accept=accept, decline=decline, full=full,
                     direction=8)


def roland_event(event_id, x, y):
    pitch = S.narrate([
        "A man is standing by the fire in armour that",
        "has clearly never been repaired by anyone",
        "local. He is lit slightly better than the",
        "rest of the room."])
    pitch += S.say("Roland", [
        "Roland Fairweather. Well met!"])
    pitch += S.narrate(["Somewhere behind you, Dorcas says 'here we go'."])
    pitch += S.say("Roland", [
        "I have three things to tell you and",
        "you will only like two of them."])
    pitch += S.say("Roland", [
        "One: I am extremely good at this.",
        "Genuinely. Embarrassingly. I have been",
        "doing it since I was eleven and I have",
        "never lost a fight I was awake for."])
    pitch += S.say("Roland", [
        "Two: I will come with you gladly,",
        "for nothing, and I will carry more",
        "than my share, and I will like you."])
    pitch += S.narrate(["You ask about the third thing."])
    pitch += S.say("Roland", [
        "Three: I cannot be there at the end."])
    pitch += S.narrate(["The whole tavern has gone very slightly quiet",
                        "in the way of people who have watched this",
                        "conversation before."])
    pitch += S.say("Roland", [
        "It isn't cowardice. It isn't a curse.",
        "It's the shape of the thing. I turn up,",
        "I help, and before the last door I get",
        "called away. Every time. Eleven times."])
    pitch += S.say("Roland", [
        "I have tried to be there. I have tried",
        "very hard, twice.",
        "So: you'd be getting the best sword in",
        "this room, right up until you need it most."])
    pitch += [S.trope()]

    accept = S.say("Roland", [
        "Splendid! You won't regret it -",
        "and then, at one specific moment,",
        "you will, briefly."])
    accept += S.narrate(["He is already holding the door."])

    decline = S.say("Roland", [
        "Sensible. Truly.",
        "If you change your mind I'll be here,",
        "being no use to anyone at exactly",
        "the standard everyone expects."])

    full = S.say("Roland", [
        "A full party! Good. Better, honestly.",
        "Four who'll all be there at the end",
        "beats three and a rumour."])

    return S.recruit(event_id, db.ROLAND, "Roland", x, y, "Actor2", 2,
                     pitch=pitch, accept=accept, decline=decline, full=full)


# ================================================================== the Guild ==
def guild_map():
    g = room(MAP_GUILD, floor=K.IN_COBBLE,
             wall_top=K.IN_WALL_TOP_STONE, wall_face=K.IN_WALL_FACE_STONE)
    g.column(4, 3, 2, K.IN_NOTICE_BOARD)
    g.column(6, 3, 2, K.IN_BOOKCASE)
    g.column(13, 3, 2, K.IN_SWORD_RACK)
    g.column(15, 3, 2, K.IN_CABINET)
    g.set(8, 6, 2, K.IN_TABLE_SMALL)
    g.set(10, 6, 2, K.IN_TABLE_SMALL)
    g.set(8, 6, 3, K.INC_SCROLL)
    g.set(10, 6, 3, K.INC_BOOK2)
    g.scatter([(3, 10), (15, 10)], 2, K.IN_CRATE)
    g.scatter([(3, 5), (15, 6)], 2, K.INC_PLANT)
    g.set(13, 9, 2, K.IN_BARREL)
    return finish(MAP_GUILD, g, "The Adventurers' Guild (Provisional)",
                  bgm="Scene3", battleback=("Stone1", "Room1"),
                  events=guild_events())


def guild_events():
    evs = [S.exit_tile(1, "Guild Door", *threshold(MAP_GUILD), MAP_SOPPING,
                       *OUT[MAP_GUILD])]
    evs.append(pell_event(2, 9, 6))
    evs.append(bounty_board(3, 4, 4))
    evs.append(guild_mat(4, 8, 10))

    evs.append(S.sign(5, "The Charter", 6, 4, [
        "\\C[6]THE ADVENTURERS' GUILD (PROVISIONAL)\\C[0]",
        "Founded forty years ago, provisionally,",
        "pending a review.",
        "The review is scheduled.",
        "The review has been scheduled for forty years."]))

    evs.append(S.prop(6, "The Filing", 13, 4, [
        "Every party that ever went north, filed by",
        "surname of the least important member,",
        "because that was the rule when the rule was",
        "made and nobody has been able to unmake it."],
        "", 0, extra=[S.trope()]))
    return evs


def pell_event(event_id, x, y):
    """Registration, and the southern half of the roster form."""
    img = R.image("People3", 7, direction=2)

    has_hat = "$gameParty.hasItem($dataArmors[%d], true)" % db.AR_A_HAT

    intro = S.say("Pell", [
        "Registrar Pell. You'll be wanting",
        "to register."])
    intro += S.narrate(["You had not been wanting to register."])
    intro += S.say("Pell", [
        "Everyone wants to register.",
        "You cannot be an adventurer in this",
        "district unregistered. You can DO the",
        "adventuring. You just can't be one."])
    intro += S.say("Pell", [
        "Form A-1. Three requirements.",
        "One: a character reference from a",
        "recognised authority. Two: a hat.",
        "Three: Form A-1."])
    intro += S.narrate(["You ask about the hat."])
    intro += S.say("Pell", [
        "The form requires a hat.",
        "It does not say why. It does not say",
        "which. Mrs Barrow across the way sells",
        "one for thirty, and no, we are not related."])
    intro += S.narrate(["You ask about requirement three."])
    intro += S.say("Pell", [
        "Form A-1 has been mislaid.",
        "It has been mislaid for eleven years.",
        "If you find it, you may fill it in.",
        "That is the whole of the process."])
    intro += [R.control_switch(db.SW_GUILD_ASKED, True), S.trope()]

    # The check, once he has explained it.
    register = S.say("Pell", [
        "Reference. Hat. Form.",
        "In forty years nobody has brought me",
        "all three at once."])
    register += S.narrate(["He examines the reference.",
                           "He examines the hat, for some time.",
                           "He countersigns the form in four places",
                           "and stamps it twice."])
    register += [R.gain_item(db.IT_REFERENCE, -1),
                 R.gain_item(db.IT_GUILD_CARD, 1), R.play_me("Fanfare2")]
    register += S.narrate(["Got \\I[194]\\C[3]Guild Card (Provisional)\\C[0]."])
    register += S.say("Pell", [
        "You are now an adventurer.",
        "The board is open to you. So is the",
        "Barrow of the Forty-Fourth, which is a",
        "Scheduled Monument and members only."])
    register += S.narrate([
        "Somewhere out east, a mound with a curse on",
        "it becomes, administratively, accessible."])
    register += [R.control_switch(db.SW_GUILD_MEMBER, True), S.trope()]

    missing = S.say("Pell", [
        "Not yet. Let us go through it again."])
    missing += R.if_then(
        R.condition_item(db.IT_REFERENCE),
        S.say("Pell", ["Reference: acceptable."]),
        S.say("Pell", ["Reference: absent. An elder, a mayor,",
                       "a magistrate. Somebody with a chain."]))
    missing += R.if_then(
        R.condition_script(has_hat),
        S.say("Pell", ["Hat: present. Thank you."]),
        S.say("Pell", ["Hat: no hat. There must be a hat."]))
    missing += R.if_then(
        R.condition_switch(db.SW_GUILD_FORM),
        S.say("Pell", ["Form A-1: found. Astonishing."]),
        S.say("Pell", ["Form A-1: still mislaid.",
                       "Have a look about. Not in here.",
                       "I have looked in here."]))

    checking = R.if_then(
        R.condition_item(db.IT_REFERENCE),
        R.if_then(
            R.condition_script(has_hat),
            R.if_then(R.condition_switch(db.SW_GUILD_FORM),
                      register, missing),
            missing),
        missing)

    member = S.say("Pell", [
        "Registered. Provisionally.",
        "Bounties on the board. Barrow's open.",
        "And I hold Form C-12(S), if you need",
        "to let one of the southern lot go."])
    member += R.choice_block(
        ["Amend the southern roster", "Nothing today"],
        [S.roster_amendment(S.COMPANIONS_SOUTH, clerk="Pell"),
         S.say("Pell", ["Quite right. Filing is a discipline."])])

    return R.event(event_id, "Registrar Pell", x, y, [
        R.page(intro, img=img, trigger=0, priority=1),
        R.page(checking, img=img, trigger=0, priority=1,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_GUILD_ASKED}),
        R.page(member, img=img, trigger=0, priority=1,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_GUILD_MEMBER}),
    ])


def guild_mat(event_id, x, y):
    """Form A-1 is under the mat. The tower has already done this joke, which
    is exactly why it is funny here and exactly why Pell does not think so."""
    plain = S.narrate([
        "A doormat. It says WELCOME.",
        "It has said WELCOME through eleven years of",
        "a mislaid form."])

    search = S.narrate(["A doormat. It says WELCOME."])
    search += R.choice_block(
        ["Look under the mat", "Leave the mat alone"],
        [S.narrate(["Form A-1 is under the mat."]) +
         [R.play_se("Key"), R.control_switch(db.SW_GUILD_FORM, True),
          S.trope()] +
         S.narrate([
             "It has been under the mat for eleven years,",
             "six feet from the man looking for it."]) +
         S.say("Pell", [
             "...Do not say it.",
             "I am aware of the tower. I am aware",
             "that the key was under the mat.",
             "I do not find the pattern amusing."]),
         S.narrate(["You leave the mat alone.",
                    "It continues to say WELCOME."])])

    found = S.narrate(["The mat, with nothing under it any more.",
                       "It looks smaller."])

    return R.event(event_id, "The Mat", x, y, [
        R.page(plain, img=R.image(""), trigger=0, priority=1,
               direction_fix=True),
        R.page(search, img=R.image(""), trigger=0, priority=1,
               direction_fix=True,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_GUILD_ASKED}),
        R.page(found, img=R.image(""), trigger=0, priority=1,
               direction_fix=True,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_GUILD_FORM}),
    ])


def bounty_board(event_id, x, y):
    """Two bounties, posted and paid. The board is only readable to members,
    because of course it is."""
    closed = S.narrate([
        "A cork board, behind a small rope.",
        "A card on the rope reads: MEMBERS ONLY.",
        "The rope is eleven inches high and could be",
        "stepped over by a determined duck."])

    crab = S.narrate([
        "\\C[6]BOUNTY: THE CRAB OF UNUSUAL SIZE\\C[0]",
        "Holds the west beach. Will not be reasoned",
        "with. Has been there longer than the town.",
        "Reward: 900\\G on production of a witness."])
    crooke = S.narrate([
        "\\C[6]BOUNTY: M. CROOKE, BANDIT CHIEF\\C[0]",
        "Camp in the western hills. Runs a six-week",
        "banditry apprenticeship with a syllabus.",
        "Reward: 1200\\G and the Guild's quiet relief."])

    claim_crab = R.if_then(
        R.condition_switch(db.SW_BOUNTY_CRAB),
        R.if_then(
            R.condition_switch(db.SW_CRAB_PAID),
            S.narrate(["Paid. The card has DISCHARGED across it",
                       "in Pell's handwriting."]),
            [R.gain_gold(900), R.gain_item(db.IT_CHOWDER, 2),
             R.play_me("Item"), R.control_switch(db.SW_CRAB_PAID, True),
             R.control_variable_add(db.VAR_BOUNTIES, 1)] +
            S.narrate(["Claimed: 900\\G and \\I[236]\\C[3]Sopping Chowder x2\\C[0].",
                       "The chowder is from the fish stall, who are",
                       "extremely pleased about the beach."])),
        crab)

    claim_crooke = R.if_then(
        R.condition_switch(db.SW_BOUNTY_CROOKE),
        R.if_then(
            R.condition_switch(db.SW_CROOKE_PAID),
            S.narrate(["Paid. Somebody has pinned the syllabus",
                       "up next to it as a curiosity."]),
            [R.gain_gold(1200), R.gain_armor(db.AR_OILSKIN, 1),
             R.play_me("Item"), R.control_switch(db.SW_CROOKE_PAID, True),
             R.control_variable_add(db.VAR_BOUNTIES, 1)] +
            S.narrate(["Claimed: 1200\\G and \\I[153]\\C[3]Oilskin Coat\\C[0]."])),
        crooke)

    board = S.narrate(["\\C[6]THE BOARD\\C[0]",
                       "Two cards. There are usually two cards."])
    board += R.choice_block(
        ["The crab", "The bandit chief", "Step away from the board"],
        [claim_crab, claim_crooke, []])

    return R.event(event_id, "Bounty Board", x, y, [
        R.page(closed, img=R.image(""), trigger=0, priority=1,
               direction_fix=True, through=True),
        R.page(board, img=R.image(""), trigger=0, priority=1,
               direction_fix=True, through=True,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_GUILD_MEMBER}),
    ])


# ============================================================ the outfitters ==
def outfit_map():
    g = room(MAP_OUTFIT, floor=K.IN_WOOD_FLOOR, floor_alt=K.IN_DARK_WOOD)
    for x in (3, 4, 5):
        g.column(x, 3, 2, K.IN_SHELF_GOODS)
    g.column(6, 3, 2, K.IN_SHELF_JARS)
    g.column(10, 3, 2, K.IN_SWORD_RACK)
    for x in (11, 12, 13):
        g.column(x, 3, 2, K.IN_SHELF_BOTTLES)
    g.scatter([(3, 9), (4, 9), (13, 9)], 2, K.IN_CRATE2)
    g.scatter([(3, 7), (12, 8)], 2, K.IN_BARREL2)
    g.set(4, 6, 2, K.IN_TABLE_SMALL)
    g.set(4, 6, 3, K.INC_BASKET)
    g.set(11, 6, 2, K.IN_TABLE_SMALL)
    g.set(11, 6, 3, K.INC_BOTTLES)
    g.set(8, 4, 2, K.INC_ARMOR_STAND)
    return finish(MAP_OUTFIT, g, "Wick & Barrow, Outfitters", bgm="Town7",
                  battleback=("Wood1", "Room1"), events=outfit_events())


def forty_bolts(shop):
    """The largest order Mrs Barrow has ever taken, on a page appended to her.

    `NORTH.md` 5.1 ties the two expansions together here on purpose: the north
    cannot be finished until the south is open, and the reason is forty bolts
    of oilskin. This is rule 1.7 pattern two - her shop, her lines and her
    peg are untouched, and a player who never goes north never sees any of it.

    She invoices the works rather than taking the party's money. That is what
    a works order is, it means nobody can arrive here too poor to finish the
    airship, and 'on account' is a better joke than a price.

    `shop` is her own first page, handed in so that from the second
    conversation onwards she is exactly the shopkeeper she was before."""
    forty = S.narrate([
        "You ask whether Wick and Barrow can do forty",
        "bolts of oilskin."])
    forty += S.say("Mrs Barrow", [
        "Forty.",
    ]) + S.narrate([
        "You say it again. You say the word 'bolts'",
        "as well, in case that was the trouble."])
    forty += S.say("Mrs Barrow", [
        "I heard you the first time.",
        "I was enjoying it."])
    forty += S.narrate([
        "You explain that it is for the Hoyle Works at",
        "Upper Clanging, and that they will settle."])
    forty += S.say("Mrs Barrow", [
        "On account.",
    ]) + S.say("Mrs Barrow", [
        "Thirty-nine years in this",
        "trade, and I have never once had cause",
        "to write 'on account'."])
    forty += S.narrate([
        "She writes it. She writes it in the day book,",
        "and then in the ledger, and then a third time",
        "on a card, which she props against the till",
        "where it can be seen from the door."])
    forty += S.narrate([
        "The oilskin comes down off the top shelf.",
        "It takes both of you and most of the morning."])
    forty += [R.gain_item(db.IT_OILSKIN_BOLTS, 1), R.play_me("Item")]
    forty += S.narrate([
        "Got \\I[227]\\C[3]Forty Bolts of Oilskin\\C[0]."])
    forty += S.narrate([
        "You mention that it is going north."])
    forty += S.say("Mrs Barrow", [
        "North.",
    ]) + S.say("Mrs Barrow", [
        "Well. Something's going",
        "the right way up that road for once."])
    forty += [R.self_switch("B", True)]

    return [R.page(
        R.if_then(R.condition_self_switch("B", False), forty, list(shop)),
        img=R.image("People4", 1, direction=6), trigger=0, priority=1,
        conditions={"switch1Valid": True, "switch1Id": db.SW_OILSKIN_ASKED})]


def outfit_events():
    evs = [S.exit_tile(1, "Outfitters Door", *threshold(MAP_OUTFIT),
                       MAP_SOPPING, *OUT[MAP_OUTFIT])]

    shop = S.say("Mrs Barrow", [
        "Outfitting. Everything an",
        "adventurer needs, and four things nobody does."])
    shop += R.shop([
        (0, db.IT_POTION, 0, 0), (0, db.IT_HI_POTION, 0, 0),
        (0, db.IT_BISCUIT, 0, 0), (0, db.IT_CHOWDER, 0, 0),
        (0, db.IT_PALE, 0, 0), (0, db.IT_ANTIDOTE, 0, 0),
        (0, db.IT_LAMP_OIL, 0, 0), (0, db.IT_BENCH, 0, 0),
        (1, db.WP_GRUDGE, 0, 0), (1, db.WP_CROSSBOW, 0, 0),
        (1, db.WP_RECURVE, 0, 0),
        (2, db.AR_A_HAT, 0, 0), (2, db.AR_OILSKIN, 0, 0),
        (2, db.AR_LEATHER, 0, 0), (2, db.AR_BOOTS, 0, 0),
    ])
    evs.append(S.npc(2, "Mrs Barrow", 5, 6, shop, "People4", 1, direction=6,
                     pages=forty_bolts(shop)))

    wick = S.narrate([
        "A peg on the wall, at the end of a row of",
        "pegs, with nothing on it."])
    wick += S.say("Mrs Barrow", [
        "Wick's peg."])
    wick += S.narrate(["You ask where Wick is."])
    wick += S.say("Mrs Barrow", [
        "Went north. Same as they all do.",
        "Forty-one years ago this spring."])
    wick += S.narrate(["You ask whether the sign should be changed."])
    wick += S.say("Mrs Barrow", [
        "The sign says Wick and Barrow.",
        "That's two names, and one of them's",
        "still walking about, and the other one",
        "went north, and both belong on a sign."])
    wick += [S.trope()]
    evs.append(talker(3, "Wick's Peg", 10, 4, "Mrs Barrow", wick,
                      S.narrate(["Wick's peg. Empty, and dusted."]),
                      sheet="", index=0))

    evs.append(S.prop(4, "The Bench, Flat-Packed", 12, 4, [
        "A bench, in eleven pieces, leaning against",
        "the wall under a hand-lettered card:",
        "'BENCH. 400. NOBODY HAS EVER BOUGHT THIS.'",
        "The card is not wrong and knows it."], "", 0))
    return evs


# ================================================== Number Forty-Five's house ==
def cottage_map():
    g = room(MAP_COTTAGE, floor=K.IN_WOOD_FLOOR, floor_alt=K.IN_PARQUET)
    g.blit(9, 3, 2, K.IN_FIREPLACE)
    g.column(3, 3, 2, K.IN_BOOKCASE)
    g.column(4, 3, 2, K.IN_BOOKCASE2)
    g.column(13, 3, 2, K.IN_SHELF_JARS)
    g.column(6, 3, 2, K.IN_CURTAIN_GREEN)
    g.blit(3, 8, 2, K.IN_SOFA)
    g.set(8, 6, 2, K.IN_TABLE_ROUND)
    g.set(8, 6, 3, K.INC_PLANT2)
    g.set(12, 6, 2, K.IN_TABLE_SMALL)
    g.set(12, 6, 3, K.INC_MEAL)
    g.scatter([(13, 9), (12, 9)], 2, K.IN_POT)
    g.set(5, 5, 2, K.IN_CRATE)
    return finish(MAP_COTTAGE, g, "Number Forty-Five's Cottage", bgm="Theme2",
                  battleback=("Wood1", "Room1"), events=cottage_events())


def cottage_events():
    evs = [S.exit_tile(1, "Cottage Door", *threshold(MAP_COTTAGE), MAP_SOPPING,
                       *OUT[MAP_COTTAGE])]
    evs.append(quy_event(2, 7, 6))

    evs.append(S.prop(3, "A Sword Over The Fire", 10, 4, [
        "A sword on two hooks above the fireplace,",
        "exactly like the one that was over yours.",
        "There is dust on the upper edge, which takes",
        "a long time and a great deal of not looking."],
        "", 0, extra=[S.trope()]))

    evs.append(S.prop(4, "The Commendation", 3, 4, [
        "A framed commendation from the Prophecy",
        "Committee of Thistlewick, thanking Halbert",
        "Quy for his service.",
        "It is face down on the shelf, and the frame",
        "has been dusted around rather than moved."],
        "", 0, extra=[]))

    evs.append(S.prop(5, "Roses", 13, 4, [
        "Cuttings in jars along the windowsill, all",
        "of them labelled in a careful hand.",
        "Not one turnip in the house.",
        "You get the feeling that is a policy."], "", 0))
    return evs


def quy_event(event_id, x, y):
    """Chosen One #45, and the single most load-bearing conversation in the
    expansion: it changes what Grimspite says at the top of the tower."""
    img = R.image(*S.FACES["Halbert Quy"], direction=2)

    first = S.narrate([
        "A man in his seventies is potting something",
        "on the kitchen table. He is exactly as tall",
        "as the portraits in Prophecy Hall and about",
        "four stone heavier."])
    first += S.say("Halbert Quy", [
        "Thistlewick.",
        "I can tell from the standing."])
    first += S.narrate(["You say who you are."])
    first += S.say("Halbert Quy", [
        "Forty-eight. Well.",
        "Halbert Quy. Forty-five.",
        "Sit down, you're blocking the light."])
    first += S.narrate(["You ask why nobody in Thistlewick has ever",
                        "mentioned that he is alive."])
    first += S.say("Halbert Quy", [
        "Clause nineteen. The Resettlement",
        "Clause. You come back, they give you a",
        "pension and a cottage and 'such distance",
        "from the village as is mutually agreeable'."])
    first += S.say("Halbert Quy", [
        "Turned out to be forty miles.",
        "They're not cruel. They're embarrassed.",
        "A hero who came back asks questions."])
    first += S.narrate(["He turns the pot a quarter turn and looks",
                        "at it."])
    first += S.say("Halbert Quy", [
        "I asked one at the next meeting.",
        "I said: if it works every hundred years,",
        "why is there always a next one?",
        "Cottage was ready by the Friday."])
    first += [R.control_switch(db.SW_SOUTH, True), S.trope()]

    # The line the finale reads back.
    ask = S.say("Halbert Quy", [
        "You want to know what he's like."])
    ask += S.narrate(["You do."])
    ask += S.say("Halbert Quy", [
        "Polite. Tired. Very well read.",
        "He offered me tea and I said no because",
        "I thought it was a trick, and it wasn't,",
        "and I've thought about that tea ever since."])
    ask += S.narrate(["He puts the trowel down."])
    ask += S.say("Halbert Quy", [
        "Here's the thing I came home with,",
        "forty-eight, and it's the only thing",
        "I've got that's worth the trip."])
    ask += S.say("Halbert Quy", [
        "Nobody asks him why.",
        "Forty-seven of us. Forty-seven.",
        "We all did the sword. Not one of us",
        "ever asked the man why he doesn't stop."])
    ask += S.narrate(["He looks at you for a while."])
    ask += S.say("Halbert Quy", [
        "Ask him. That's all. Ask him why.",
        "And then listen to the whole answer,",
        "because it's long, and because I didn't."])
    ask += [R.control_switch(db.SW_MET_QUY, True), S.trope()]

    after = S.say("Halbert Quy", [
        "Still here? Go on, then. North.",
        "Ask him. And come back and tell me",
        "what he said, because I've been",
        "waiting thirty years to hear it."])

    return R.event(event_id, "Halbert Quy (#45)", x, y, [
        R.page(first + [R.self_switch("A", True)], img=img, trigger=0,
               priority=1),
        R.page(ask, img=img, trigger=0, priority=1,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
        R.page(after, img=img, trigger=0, priority=1,
               conditions={"switch1Valid": True, "switch1Id": db.SW_MET_QUY}),
    ])


# =============================================================== the lighthouse ==
def lighthouse_map():
    """Tall and thin, the way a lighthouse ought to be: the keeper at the
    bottom, the lamp nineteen rows up, and nothing much in between except the
    climb."""
    g = room(MAP_LIGHTHOUSE, floor=K.IN_SANDSTONE,
             wall_top=K.IN_WALL_TOP_STONE, wall_face=K.IN_WALL_FACE_STONE)
    g.fill(5, 4, 7, 6, 0, K.IN_DIAMOND_TILE)      # the lamp floor at the top
    g.autotile(0)
    g.column(3, 3, 2, K.IN_SHELF_BOTTLES)
    g.column(9, 3, 2, K.IN_CABINET)
    g.column(3, 16, 2, K.IN_BED_BROWN)
    g.column(9, 16, 2, K.IN_BOOKCASE)
    g.set(4, 18, 2, K.IN_TABLE_ROUND)
    g.set(4, 18, 3, K.INC_MEAL)
    g.set(8, 18, 2, K.IN_TABLE_SMALL)
    g.set(8, 18, 3, K.INC_BOOK)
    g.scatter([(3, 12), (9, 12)], 2, K.IN_BARREL)
    g.scatter([(3, 9), (9, 9)], 2, K.IN_CRATE)
    g.scatter([(4, 8), (8, 8)], 2, K.INC_CANDLES)
    g.column(6, 4, 2, K.IN_STOVE)                 # the lamp itself, brass and
                                                  # the size of a cart
    return finish(MAP_LIGHTHOUSE, g, "The Lighthouse of Saint Bother",
                  bgm="Ship2", battleback=("Stone1", "Room1"),
                  events=lighthouse_events())


def lighthouse_events():
    evs = [S.exit_tile(1, "Lighthouse Door", *threshold(MAP_LIGHTHOUSE),
                       MAP_WORLD, WORLD_LIGHTHOUSE[0],
                       WORLD_LIGHTHOUSE[1] + 1)]
    evs.append(bother_event(2, 6, 17))
    evs.append(the_lamp(3, 6, 5))

    evs.append(S.prop(4, "The Ships Book", 8, 17, [
        "A ledger of every ship that has passed the",
        "point. The last entry is ninety-one years old.",
        "Under it, in the same hand, again and again",
        "down four hundred pages: 'no ship. light lit.'"],
        "", 0, extra=[S.trope()]))
    return evs


def bother_event(event_id, x, y):
    img = R.image("People3", 4, direction=2)

    first = S.narrate([
        "A man is sitting at the bottom of a lighthouse",
        "in the dark, which is a thing you notice about",
        "a lighthouse immediately."])
    first += S.say("Bother", [
        "Ferrety Bother. It's a family name.",
        "The saint was my great-grandmother",
        "and she'd have hated the fuss."])
    first += S.narrate(["You ask why the light is out."])
    first += S.say("Bother", [
        "Out of oil since the spring.",
        "Mrs Barrow has oil. Mrs Barrow also",
        "has a price, and the Guild stopped my",
        "stipend when the shipping stopped."])
    first += S.narrate(["You ask when the shipping stopped."])
    first += S.say("Bother", [
        "Ninety-one years ago."])
    first += S.narrate(["You point out, carefully, that a lighthouse",
                        "with no ships is a lamp on a rock."])
    first += S.say("Bother", [
        "It isn't for the ships. Hasn't been",
        "for four generations."])
    first += S.say("Bother", [
        "It's for the ones coming back down",
        "the north road at night. You can see",
        "this light from the crossroads.",
        "It's what you walk home by."])
    first += S.narrate([
        "Forty-seven times this light has been lit for",
        "somebody. It has been lit for nobody a great",
        "deal more often than that."])
    first += [R.control_switch(db.SW_LAMP_ASKED, True), S.trope()]

    waiting = S.say("Bother", [
        "One gallon. That's all it takes.",
        "Mrs Barrow, across from the Guild.",
        "Tell her it's for the light. She'll",
        "still charge you. Tell her anyway."])

    lit = S.say("Bother", [
        "You'll be wanting to go up, then."])
    lit += S.narrate(["He does not get up. He has been up those",
                      "stairs eleven thousand times and he would",
                      "like somebody else to do it once."])

    burning = S.say("Bother", [
        "You can see it from the crossroads.",
        "I checked. I walked out to the",
        "crossroads at midnight to check,",
        "and I stood there, and I looked back."])

    return R.event(event_id, "Ferrety Bother", x, y, [
        R.page(first, img=img, trigger=0, priority=1),
        R.page(waiting, img=img, trigger=0, priority=1,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_LAMP_ASKED}),
        R.page(lit, img=img, trigger=0, priority=1,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_LAMP_ASKED,
                           "itemValid": True, "itemId": db.IT_LAMP_OIL}),
        R.page(burning, img=img, trigger=0, priority=1,
               conditions={"switch1Valid": True, "switch1Id": db.SW_LAMP_LIT}),
    ])


def the_lamp(event_id, x, y):
    cold = S.narrate([
        "The lamp. Brass, enormous, and cold.",
        "The wick has been trimmed square by somebody",
        "who trims it square every week regardless."])

    fill = S.narrate([
        "The lamp. You have a gallon of oil."])
    fill += R.choice_block(
        ["Fill it and light it", "Not yet"],
        [[R.gain_item(db.IT_LAMP_OIL, -1), R.play_se("Fire1"), R.wait(30),
          R.flash_screen([255, 255, 200, 170], 60, True)] +
         S.narrate([
             "The wick takes. The brass goes from cold to",
             "warm to something you have to look away from.",
             "Out through the glass, the whole south coast",
             "gets an edge on it."]) +
         [R.play_me("Fanfare1"), R.gain_armor(db.AR_LAMP, 1)] +
         S.narrate(["Got \\I[212]\\C[3]Keeper's Lamp\\C[0].",
                    "Bother pressed it on you at the bottom of",
                    "the stairs without a word, which from him",
                    "is a speech."]) +
         S.narrate([
             "Somewhere out on the north road, at the",
             "crossroads, there is now a light in the",
             "south when you turn round.",
             "It has been dark there since the spring."]) +
         [R.control_switch(db.SW_LAMP_LIT, True), S.trope()],
         []])

    lit = S.narrate([
        "The lamp is lit.",
        "It will need oil again in the spring, and",
        "somebody will get it, now that somebody has."])

    # Once it is burning the event carries the flame sprite, so the top of the
    # lighthouse looks different from the bottom of the stairs.
    flame = R.image("!Flame", 0, direction=2)
    return R.event(event_id, "The Lamp", x, y, [
        R.page(cold, img=R.image(""), trigger=0, priority=1,
               direction_fix=True),
        R.page(fill, img=R.image(""), trigger=0, priority=1,
               direction_fix=True,
               conditions={"itemValid": True, "itemId": db.IT_LAMP_OIL}),
        R.page(lit, img=flame, trigger=0, priority=1, direction_fix=True,
               step_anime=True, walk_anime=False,
               conditions={"switch1Valid": True, "switch1Id": db.SW_LAMP_LIT}),
    ])


def build():
    R.save_map(MAP_SOPPING, sopping_map())
    R.save_map(MAP_WYVERN, wyvern_map())
    R.save_map(MAP_GUILD, guild_map())
    R.save_map(MAP_OUTFIT, outfit_map())
    R.save_map(MAP_COTTAGE, cottage_map())
    R.save_map(MAP_LIGHTHOUSE, lighthouse_map())
