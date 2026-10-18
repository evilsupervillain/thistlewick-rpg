"""Maps 40-41: Gladhollow, and the mayor's room with the bookcase.

`../SITES.md` step 5. `../BIOS.md` is the bio: **Toby Wendle, aged ten**,
Official Welcomer, paid a copper a day to stand by the gate and say "Welcome to
Gladhollow!" and nothing else, per his job description, which he has read nine
times. He has fourteen ways of saying it and is working on a fifteenth, the
questioning one. He knows everything about the town - the passage behind the
mayor's bookcase, where the well key is, which barrels have a potion in them -
and is not allowed to tell you any of it, because it would be a second
sentence. He is saving up for promotion to Farewell Boy at the east gate, who
gets *two*.

One site and one module, so it exports `SITE` and `world_doors` the way
`evermore.py` does. **`Village B` is two cells**, and `world_doors` makes a
door on each.

* **No world-map coordinate is written here or in `places.py`.** The door
  cells are handed in by `journey.world_map` off the placeholders they
  replace; `places.GLADHOLLOW_STEP` is the one square this game chose, one
  south of the western cell. `../WORLDMAP.md` 7.6.
* **The fourteen are a variable and a list**, `db.VAR_TOBY` and `DELIVERIES`.
  Each time you talk to him he does the next one, and the narrator names it,
  because he cannot. The fifteenth is the one he is working on and it comes
  round once every lap: "...Welcome to Gladhollow?" and an anxious look to see
  whether a question counts as a second sentence.
* **He tells you everything anyway, by delivery.** Ask him about the town and
  the answer is always "...Welcome to Gladhollow." - with his eyes on the
  mayor's house and both hands sliding a bookcase, or on the well and then the
  pot beside it, or on his granny's barrels and then his granny. Which one is
  `VAR_TOBY` mod three, so a player who keeps asking gets all three.
* **The barrels are his granny's** and every potion in them is wrapped in a
  stocking with a label sewn in: PLEASE RETURN TO MRS WENDLE. She does not
  mind. She would like them back. You can give her one, if you have one, as
  often as you like.
* **The passage behind the bookcase is the payoff.** It goes down to a little
  room with the Council's ledger in it: Toby's copper a day in one column,
  and in the next, in the mayor's hand, a copper for every one he has saved.
  A bag of coppers, labelled FOR THE UNIFORM; a new Farewell Boy's cap on a
  stand in a very small size. DO NOT TELL TOBY, underlined twice - and under
  it, in pencil, in a much rounder hand, "I havent." He knew. It would have
  been a second sentence. After that he has one more line, once, and it is
  the bio's: "Welcome BACK to Glad- I'm not allowed that one."
* **His brother Ned is the Farewell Boy** and has two sentences, and spends
  the second one on Toby if you ask about him.
* **There is no Register A candidate here, on purpose.** `../NORTH.md` 1.6's
  line about child characters applies to Toby as written - the joke is always
  his innocence - and the site is warm rather than red. Four tropes: the
  "Welcome to Gladhollow!" villager, the hero who helps himself to a
  stranger's barrels, the key under the pot, and the passage behind a
  bookcase.
* **Tiles.** The village is `Grass (Dirt)` and a `Dirt` road, the second
  row of the sheet, so they blend. The well is `TUB`, which is `Well`, with `POT` beside it - a plain
  clay `Pot`, and the text says so. In the mayor's room the passage bookcase is `IN_BOOKSHELF`
  like its neighbours, and the event that opens it is on its lower cell. The back
  room is drawn on the same map in the black space east of the office, and
  its props are `Table A` with `Open Book A (H)` and `Sack A`, and `Hat A
  (Stand)`, a blue cap with white piping. Ned's sprite
  has no cap, so nothing says he wears one.
"""
import db
import handdrawn as HD
import mapkit as K
import rmmzdata as R

import story as S
from places import MAP_WORLD, MAP_GLADHOLLOW, MAP_MAYORS, GLADHOLLOW_STEP
import q_spare

# The name `worldmap.json`'s door events carry.
SITE = "Gladhollow"

# ------------------------------------------------------------ the village ---
VW, VH = 32, 20
ROAD_Y = 10                     # the road: rows 10 and 11, gate to gate
ARRIVE = (1, ROAD_Y)
GATES_W = [(0, ROAD_Y), (0, ROAD_Y + 1)]
GATES_E = [(VW - 1, ROAD_Y), (VW - 1, ROAD_Y + 1)]

# A building's only face is its south side, and every front here opens onto
# the road. Granny Wendle's, the mayor's house, and one more.
GRANNY_B = (3, 4, 6, 5)
MAYOR_B = (12, 3, 8, 6)
HOUSE_B = (23, 4, 6, 5)
FRONT_Y = 8                     # the wall row every front is on
GRANNY_DOOR_X = 5
MAYOR_DOOR = (16, FRONT_Y)
MAYOR_OUT = (MAYOR_DOOR[0], FRONT_Y + 1)

TOBY_AT = (3, ROAD_Y)           # one step in from the west gate, in the way
NED_AT = (VW - 3, ROAD_Y + 1)   # and his brother, in the way at the east
GRANNY_AT = (6, FRONT_Y + 1)
BARRELS = [(3, 9), (4, 9), (7, 9), (8, 9)]
NOTICE_W = (3, 12)
NOTICE_E = (VW - 4, 12)
WELL = (9, 14)
FLOWERPOT = (10, 14)

# --------------------------------------------------------- the mayor's room ---
# 33 wide, not 26: ten columns of black between the office and the cellar,
# so neither shows from the edge of the other (Mike, October 2026).
MW, MH = 33, 13
#            x1  y1  x2  y2  door_x
OFFICE = (3, 4, 12, 8, 7)
PASSAGE_X = 9                   # the bookcase that is a door
DESK = (5, 6)                   # Table A, two cells
MAP_AT = (6, 2)                 # the World Map on the wall, two cells
#        x1  y1  x2  y2
BACK = (24, 4, 28, 6)
# The steps up out of the back room go through its north wall in the east
# corner, one step wide, the way Mike drew the Slain Wyvern's cellar stairs
# (`mapkit.stairs_up`): the way up is the top step, and you arrive at the foot.
BACK_ARRIVE = (28, 6)
STAIRS = (28, 3)
LEDGER = (24, 4)
SACK = (25, 4)
CAP = (24, 6)

# Event ids on the mayor's map, which the street's Toby reads back.
LEDGER_EVENT = 4


# ============================================================== the village ==
def gladhollow_map():
    w, h = VW, VH
    g = K.Canvas(w, h)
    g.fill(0, 0, w - 1, h - 1, 0, K.GRASS)

    # One road, gate to gate, and a doorstep off it for every front.
    g.fill(0, ROAD_Y, w - 1, ROAD_Y + 1, 0, K.PATH)
    g.fill(GRANNY_B[0], FRONT_Y + 1, GRANNY_B[0] + GRANNY_B[2] - 1,
           FRONT_Y + 1, 0, K.PATH)
    g.fill(MAYOR_DOOR[0] - 1, FRONT_Y + 1, MAYOR_DOOR[0] + 1, FRONT_Y + 1, 0,
           K.PATH)
    g.fill(HOUSE_B[0] + 2, FRONT_Y + 1, HOUSE_B[0] + 2, FRONT_Y + 1, 0,
           K.PATH)
    g.fill(WELL[0] - 1, ROAD_Y + 2, WELL[0] + 1, WELL[1] + 1, 0, K.PATH)

    g.building(*GRANNY_B, wall=K.WALL_TIMBER, roof=K.ROOF_BROWN)
    g.building(*MAYOR_B, wall=K.WALL_PLASTER, roof=K.ROOF_GREEN)
    g.building(*HOUSE_B, wall=K.WALL_PLANK_LIGHT, roof=K.ROOF_BROWN)
    g.autotile(0)

    # Fronts. The mayor's door is an event; the other two are shut.
    g.column(GRANNY_DOOR_X, FRONT_Y - 1, 3, K.DOOR_SHUT)
    g.set(GRANNY_DOOR_X + 2, FRONT_Y - 1, 3, K.WINDOW)
    g.set(MAYOR_DOOR[0] - 2, FRONT_Y, 3, K.WINDOW)
    g.set(MAYOR_DOOR[0] + 2, FRONT_Y, 3, K.WINDOW)
    g.set(MAYOR_DOOR[0] - 3, FRONT_Y - 1, 3, K.SIGN_SUN)
    g.column(HOUSE_B[0] + 2, FRONT_Y - 1, 3, K.DOOR_SHUT)
    g.set(HOUSE_B[0] + 4, FRONT_Y, 3, K.WINDOW)
    for b in (GRANNY_B, MAYOR_B, HOUSE_B):
        g.chimney_beside(*b[:2])

    # Granny Wendle's barrels, either side of her.
    g.scatter(BARRELS, 3, K.BARREL)

    # The two notices, one at each gate, and the well with its pot.
    g.set(*NOTICE_W, 3, K.SIGNPOST)
    g.set(*NOTICE_E, 3, K.SIGNPOST)
    g.set(*WELL, 3, K.TUB)
    g.set(*FLOWERPOT, 3, K.POT)

    g.scatter([(2, 2), (11, 2), (21, 2), (29, 3), (20, 16), (6, 16)], 3,
              K.BUSH)
    g.scatter([(9, 9), (10, 9), (21, 9), (22, 9), (13, 13), (14, 13),
               (24, 13), (25, 15), (5, 14), (16, 16)], 3, K.FLOWERS2)
    g.scatter([(11, 13), (18, 13), (27, 14), (7, 13), (19, 9)], 3,
              K.FLOWERS)
    g.scatter([(22, 15)], 3, K.LOGS)
    for x, y in [(14, 15), (3, 15), (25, 12)]:
        g.blit(x, y, 3, K.TREE)

    # Trees all round, with a gap for the road at each end. The gaps are the
    # gates. All `TREE`: `TREE_DARK` on open grass is a flat square of hedge.
    for x in range(0, w - 1, 2):
        g.blit(x, 0, 3, K.TREE)
        g.blit(x, h - 2, 3, K.TREE)
    for y in list(range(2, ROAD_Y, 2)) + list(range(ROAD_Y + 2, h - 2, 2)):
        g.blit(0, y, 3, K.TREE)
        g.blit(w - 2, y, 3, K.TREE)

    m = K.new_map(w, h, K.TS_OUTSIDE, name="Gladhollow", bgm="Town2")
    m["data"] = g.data
    m["events"] = [None] + gladhollow_events()
    return m


# The fourteen, in order: what he does, and what he says while he does it.
# The narrator names each one, because Toby is not allowed to.
DELIVERIES = [
    ("one", "the Standard",
     ["Both arms out, both feet together, and a smile",
      "you could read by."],
     ["Welcome to Gladhollow!"]),
    ("two", "the Formal",
     ["A bow so low the saucepan falls off. He catches",
      "it on the way down without looking."],
     ["Welcome to Gladhollow!"]),
    ("three", "the Whisper",
     ["Very softly, for people who look tired. You had",
      "not realised that you did."],
     ["welcome to gladhollow"]),
    ("four", "the Song",
     ["Sung, on three notes, going up. The last note is",
      "a little beyond him and he goes anyway."],
     ["Welcome to Glad-hol-LOOOW!"]),
    ("five", "the Salute",
     ["Heels together, chin up, and a salute with the",
      "handle of the saucepan."],
     ["Welcome to Gladhollow!"]),
    ("six", "the Surprised",
     ["As if you are the first visitor Gladhollow has",
      "ever had. He has welcomed you before. He is",
      "still amazed."],
     ["Welcome to Gladhollow!"]),
    ("seven", "the Slow One",
     ["One word at a time, very clearly, for anybody",
      "from abroad. The job description says nothing",
      "about abroad. He checked."],
     ["Wel. Come. To. Glad. Hol. Low."]),
    ("eight", "the Dramatic Pause",
     ["He says the first word, and then waits so long",
      "that you start to answer, and he has to hold up",
      "one hand until you stop."],
     ["Welcome...", "...to Gladhollow!"]),
    ("nine", "the Rainy Day",
     ["He holds the saucepan up over your head, although",
      "it is not raining. He is practising for when it",
      "is."],
     ["Welcome to Gladhollow!"]),
    ("ten", "the Very Loud",
     ["Hands cupped, full volume, for people on horses.",
      "A pigeon leaves the roof of the mayor's house."],
     ["WELCOME TO GLADHOLLOW!"]),
    ("eleven", "the Sorry",
     ["For people who have walked into him. He touches",
      "the plaster on his cheek, bravely, and forgives",
      "you."],
     ["Welcome to Gladhollow."]),
    ("twelve", "the Tour",
     ["He turns slowly on the spot while he says it,",
      "pointing at every building in Gladhollow in",
      "turn. He points at the mayor's house for rather",
      "longer than the others."],
     ["Welcome to Gladhollow!"]),
    ("thirteen", "the Evening",
     ["Hushed and golden, for the end of a long day. It",
      "is not the end of the day. He could not wait."],
     ["Welcome to Gladhollow."]),
    ("fourteen", "the Classic",
     ["Both arms out, both feet together, and a smile",
      "you could read by. It is exactly the same as",
      "number one. He is extremely pleased with it."],
     ["Welcome to Gladhollow!"]),
]

# What he says when he is asked a question, which is the same thing every
# time, and what he does while he says it, which is not.
HINTS = [
    ["He says it with his eyes on the mayor's house,",
     "and both hands flat beside him, pushing, like",
     "somebody sliding a very heavy bookcase aside."],
    ["His eyes go to the well. Then to the pot beside",
     "the well. Then to the well. Then to the pot.",
     "Then, very innocently, to the sky."],
    ["He points at his granny's barrels, and then at",
     "his granny, and then puts one hand on his heart,",
     "like somebody who would very much like you to",
     "put things back."],
]


def toby_pages():
    """Two pages. The first is walking into him. The second is the
    fourteen, one per conversation, then the fifteenth, then round again -
    and, once, after the back room, the one he is not allowed."""
    first = S.narrate([
        "You walk straight into a small boy with a saucepan",
        "on his head. It rings like a bell."])
    first += S.narrate([
        "He does not fall over. He has had a great deal of",
        "practice. He straightens the saucepan, takes a",
        "deep breath, and beams at you."])
    first += S.say("Toby", ["Welcome to Gladhollow!"])
    first += S.narrate([
        "You wait for the rest of it. There is no rest of",
        "it. That was all of it, and he is delighted."])
    first += [S.trope(), R.control_variable(db.VAR_TOBY, 1),
              R.self_switch("A", True)]

    # Once, after the ledger: the one he is not allowed.
    back = S.narrate([
        "Toby sees you coming, and something is happening",
        "to his face. He knows where you have been."])
    back += S.say("Toby", ["Welcome BACK to Glad-"])
    back += S.narrate(["He claps both hands over his mouth."])
    back += S.say("Toby", ["...I'm not allowed that one."])
    back += S.narrate([
        "He looks at you over his hands, enormously, and",
        "goes pink with not saying anything at all."])
    back += [R.self_switch("B", True), R.exit_event()]
    found = "$gameSelfSwitches.value([%d, %d, 'A']) && " \
            "!$gameSelfSwitches.value([%d, %d, 'B'])" % (
                MAP_MAYORS, LEDGER_EVENT, MAP_GLADHOLLOW, 1)

    ask = []
    for n, lines in enumerate(HINTS):
        body = S.narrate(["You ask him what there is to know about the town."])
        body += S.say("Toby", ["...Welcome to Gladhollow."])
        body += S.narrate(lines)
        ask += R.if_then(R.condition_script(
            "$gameVariables.value(%d) %% 3 === %d" % (db.VAR_TOBY, n)), body)
    thank = S.narrate(["You thank him. He beams so hard the saucepan moves."])
    after = R.choice_block(["Ask him about the town", "Thank him"],
                           [ask, thank], cancel=1)

    cycle = [R.control_variable_add(db.VAR_TOBY, 1)]
    cycle += R.if_then(R.condition_variable(db.VAR_TOBY, 16, 1),
                       [R.control_variable(db.VAR_TOBY, 1)])
    for i, (word, name, how, said) in enumerate(DELIVERIES):
        body = S.narrate(["\\C[14]Number %s:\\C[0] %s." % (word, name)])
        body += S.narrate(how)
        for line in said:
            body += S.say("Toby", [line])
        body += after
        cycle += R.if_then(R.condition_variable(db.VAR_TOBY, i + 1), body)
    fifteen = S.narrate([
        "\\C[14]Number fifteen.\\C[0] It is not finished yet."])
    fifteen += S.narrate([
        "He takes a breath, looks worried, and tries it",
        "anyway, going up at the end:"])
    fifteen += S.say("Toby", ["...Welcome to Gladhollow?"])
    fifteen += S.narrate([
        "He looks at you anxiously, to see whether a",
        "question counts as a second sentence. You decide",
        "it does not. He writes something on the back of",
        "his hand."])
    cycle += R.if_then(R.condition_variable(db.VAR_TOBY, 15), fifteen)

    second = R.if_then(R.condition_script(found), back) + cycle
    return first, second


def gladhollow_events():
    evs = []

    # 1: Toby, one step in from the west gate and in the way, as he is about
    # forty times a day. Event 1 on purpose: his own page reads its B switch.
    first, second = toby_pages()
    img = R.image("Gen_People2", 5, direction=4)
    evs.append(R.event(1, "Toby", *TOBY_AT, [
        R.page(first, img=img, trigger=0, priority=1),
        R.page(second, img=img, trigger=0, priority=1,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ]))

    # 2-5: both gates, both lanes of the road, all onto the same square.
    gates = [("The West Gate", c, 4) for c in GATES_W] + \
            [("The East Gate", c, 6) for c in GATES_E]
    for i, (name, cell, facing) in enumerate(gates):
        evs.append(S.exit_tile(2 + i, name, *cell, MAP_WORLD,
                               *GLADHOLLOW_STEP, direction=facing))

    # 6: the mayor's house.
    evs.append(S.door(6, "The Mayor's House", *MAYOR_DOOR, MAP_MAYORS,
                      OFFICE[4], OFFICE[3], direction=8))

    page = dict(img=R.image(""), trigger=0, priority=1, through=True,
                direction_fix=True)

    # 7: Toby's job description, at his gate.
    west = S.narrate([
        "\\C[14]GLADHOLLOW TOWN COUNCIL\\C[0]",
        "OFFICIAL WELCOMER (WEST GATE). One copper a day.",
        "Duties: to say \"Welcome to Gladhollow!\"",
        "AND NOTHING ELSE."])
    west += S.narrate([
        "The paper has been read so often it has gone soft",
        "as cloth. In the margin, in pencil, somebody has",
        "been keeping count. They have got to nine."])
    evs.append(R.event(7, "The Welcomer's Notice", *NOTICE_W,
                       [R.page(west, **page)]))

    # 8: and the one he is saving up for, at the other.
    east = S.narrate([
        "\\C[14]GLADHOLLOW TOWN COUNCIL\\C[0]",
        "FAREWELL BOY (EAST GATE). A copper and a half.",
        "Duties: to say \"Farewell from Gladhollow!\" and",
        "\"Mind how you go.\""])
    east += S.narrate([
        "Pinned underneath: VACANCY SHORTLY. APPLICATIONS",
        "TO THE MAYOR."])
    east += S.narrate([
        "Somebody has applied already. The application is",
        "pinned up too, so that everybody can see it. It",
        "is one sentence long."])
    evs.append(R.event(8, "The Farewell Boy's Notice", *NOTICE_E,
                       [R.page(east, **page)]))

    # 9: Ned, the Farewell Boy, who has two sentences and uses both.
    def ned_body(intro):
        body = []
        if intro:
            body += S.narrate([
                "A slightly bigger boy, with his hair brushed very",
                "flat for the job. He has clearly been waiting for",
                "somebody to leave."])
        body += S.say("Ned", ["Farewell from Gladhollow! Mind how you go!"])
        about = S.narrate(["You ask about the boy at the west gate."])
        about += S.say("Ned", ["Farewell from Gladhollow! That's our Toby."])
        about += S.narrate([
            "He has spent his second sentence on his brother,",
            "and he does not look as if he minds at all."])
        bye = S.narrate(["You say goodbye. He looks very satisfied."])
        body += R.choice_block(["Ask about the boy at the west gate",
                                "Say goodbye"], [about, bye], cancel=1)
        return body
    nimg = R.image(*S.FACES["Ned"], direction=4)
    evs.append(R.event(9, "Ned", *NED_AT, [
        R.page(ned_body(True) + [R.self_switch("A", True)], img=nimg,
               trigger=0, priority=1),
        R.page(ned_body(False), img=nimg, trigger=0, priority=1,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ]))

    # 10: Granny Wendle, between her barrels, who would like her potions back.
    give = S.narrate(["You give her back a Potion."])
    give += [{"code": 126, "indent": 0,
              "parameters": [db.IT_POTION, 1, 0, 1]}]
    give += S.say("Granny Wendle", [
        "Thank you, dear.", "That's Tuesday's knee sorted."])
    keep = S.say("Granny Wendle", ["Another time, dear.",
                                   "I'm not going anywhere."])
    returns = R.if_then(R.condition_item(db.IT_POTION), R.choice_block(
        ["Give her a Potion back", "Not just now"], [give, keep], cancel=1))
    granny = S.say("Granny Wendle", [
        "Those are my barrels, dear.",
        "Every hero who comes through has the potions",
        "out of them."])
    granny += S.say("Granny Wendle", [
        "I don't mind.",
        "They're very good potions.",
        "I'd like them back, though."])
    granny += S.narrate(["You ask what they are for."])
    granny += S.say("Granny Wendle", ["My knees."])
    granny += [S.trope(), R.self_switch("A", True)] + returns
    again = S.say("Granny Wendle", ["Hello again, dear."]) + returns
    gimg = R.image(*S.FACES["Granny Wendle"], direction=2)
    evs.append(R.event(10, "Granny Wendle", *GRANNY_AT, [
        R.page(granny, img=gimg, trigger=0, priority=1),
        R.page(again, img=gimg, trigger=0, priority=1,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ]))

    # 11-14: the barrels. All of them have a potion in them.
    for i, cell in enumerate(BARRELS):
        take = S.narrate([
            "One of Granny Wendle's barrels. In the straw at the",
            "bottom, rolled up in a stocking, is a Potion."])
        take += [R.gain_item(db.IT_POTION, 1)]
        take += S.got(["You found a Potion."])
        take += S.narrate([
            "The stocking has a label sewn into it:",
            "PLEASE RETURN TO MRS WENDLE, GLADHOLLOW."])
        take += [R.self_switch("A", True)]
        empty = S.narrate([
            "Straw, and a stocking with a label sewn into it."])
        evs.append(R.event(11 + i, "Granny's Barrel", *cell, [
            R.page(take, **page),
            R.page(empty, conditions={"selfSwitchValid": True,
                                      "selfSwitchCh": "A"}, **page)]))

    # 15: the well, and the pot beside it.
    drink = S.narrate([
        "You wind up a bucket. The water is cold and clear",
        "and tastes faintly of stone, and you feel very",
        "much better for it."])
    drink += [R.play_se("Recovery"), R.recover_all()]
    lift = S.narrate([
        "You tip up the pot. Under it is a key.",
        "Of course it is."])
    lift += [S.trope(), R.play_se("Open1")]
    lift += S.narrate(["The padlock opens. You put the key back."])
    lift += drink + [R.self_switch("A", True)]
    well = S.narrate([
        "The Gladhollow well. The lid is padlocked shut.",
        "Beside it stands an old clay pot."])
    well += R.choice_block(["Look under the pot", "Leave it"],
                           [lift, []], cancel=1)
    evs.append(R.event(15, "The Well", *WELL, [
        R.page(well, **page),
        R.page(drink, conditions={"selfSwitchValid": True,
                                  "selfSwitchCh": "A"}, **page)]))
    evs.append(q_spare.courier("gladhollow", 6, 12))                # SPA-1
    return evs


# ========================================================= the mayor's room ==
def mayors_map():
    """Drawn by hand in the editor and kept by `handdrawn.py` (Mike, October
    2026), from the generated house: the office with the Council Minutes
    along its north wall - one bookcase of them a door - the desk on its rug,
    and the cellar behind, now in stone. Only the events are built here."""
    data = HD.load(MAP_MAYORS, MW, MH, K.TS_INSIDE)
    m = K.new_map(MW, MH, K.TS_INSIDE, name="The Mayor's House",
                  bgm="Town2")
    m["data"] = data
    m["events"] = [None] + mayors_events()
    return m


def mayors_events():
    x1, y1, x2, y2, door_x = OFFICE
    evs = [S.exit_tile(1, "The Door", door_x, y2 + 2, MAP_GLADHOLLOW,
                       *MAYOR_OUT)]
    page = dict(img=R.image(""), trigger=0, priority=1, direction_fix=True)
    to_back = [R.play_se("Move1"),
               R.transfer(MAP_MAYORS, BACK_ARRIVE[0], BACK_ARRIVE[1], 2, 0)]

    # 2: the bookcase. Its lower cell, which is the one you can face.
    shelf = S.narrate([
        "A bookcase full of the Gladhollow Town Council",
        "Minutes, in order, going back a very long way.",
        "One volume is sticking out further than the rest."])
    pull = S.narrate([
        "You pull it. Somewhere inside the wall, something",
        "goes clunk, and the whole bookcase swings out on",
        "a hinge. Behind it, steps go down."])
    pull += [S.trope(), R.self_switch("A", True)] + to_back
    shelf += R.choice_block(["Pull the book", "Leave it"], [pull, []],
                            cancel=1)
    open_ = S.narrate(["The bookcase stands open on its hinge."])
    open_ += R.choice_block(["Go down the steps", "Leave it"],
                            [to_back, []], cancel=1)
    evs.append(R.event(2, "The Bookcase", PASSAGE_X, y1, [
        R.page(shelf, **page),
        R.page(open_, conditions={"selfSwitchValid": True,
                                  "selfSwitchCh": "A"}, **page)]))

    # 3: the stairs back up, which put you in front of the bookcase.
    evs.append(R.event(3, "The Steps Up", *STAIRS, [R.page(
        [R.play_se("Move1"),
         R.transfer(MAP_MAYORS, PASSAGE_X, y1 + 1, 2, 0)],
        img=R.image(""), trigger=1, priority=0, through=True)]))

    # 4: the ledger. Its A switch is what Toby's B page is waiting for, so
    # its id is `LEDGER_EVENT` and must not move.
    ledger = S.narrate([
        "An open ledger, headed \\C[14]T. WENDLE, WELCOMER\\C[0].",
        "A copper a day, in one column, going back years."])
    ledger += S.narrate([
        "In the next column, in the mayor's hand: another",
        "copper, from the Council, for every one he has",
        "saved. He has saved every one."])
    ledger += S.narrate([
        "At the bottom of the page, underlined twice:",
        "",
        "   DO NOT TELL TOBY."])
    ledger += S.narrate([
        "Under that, in pencil, in a much rounder hand:",
        "",
        "   I havent."])
    ledger += [R.self_switch("A", True)]
    assert len(evs) + 1 == LEDGER_EVENT
    evs.append(R.event(LEDGER_EVENT, "The Ledger", *LEDGER,
                       [R.page(ledger, **page)]))

    # 5: the coppers.
    sack = S.narrate([
        "A bag of coppers, tied at the neck, with a label:",
        "FOR THE UNIFORM. It is a good deal heavier than a",
        "copper a day."])
    evs.append(R.event(5, "The Coppers", *SACK, [R.page(sack, **page)]))

    # 6: the cap.
    cap = S.narrate([
        "A cap on a stand: blue, with white piping, brand",
        "new, and much too small for anybody but one",
        "person."])
    cap += S.narrate([
        "The label inside says FAREWELL BOY. Somebody has",
        "written TOBY under it, and somebody else has",
        "crossed that out, because it is not official yet,",
        "and then written it in again, smaller."])
    evs.append(R.event(6, "The Cap", *CAP, [R.page(cap, **page)]))

    # 7: the note on the desk.
    note = S.narrate([
        "A note on the desk, in the mayor's hand:",
        "",
        "   GONE TO SEE ABOUT A FITTING.",
        "   BACK AT FOUR. - A. PODMORE, MAYOR"])
    evs.append(R.event(7, "The Mayor's Note", DESK[0] + 1, DESK[1],
                       [R.page(note, **page)]))

    # 8: the map of the town on the wall, read from the floor below it.
    town = S.narrate([
        "A map of Gladhollow, drawn by the Council. The west",
        "gate is marked WELCOME and the east gate FAREWELL,",
        "and at each, in pencil, somebody has drawn a very",
        "small boy."])
    evs.append(R.event(8, "The Town Map", MAP_AT[0], y1 - 1,
                       [R.page(town, **page)]))
    return evs


# ================================================================ the door ==
def world_doors(base_id, cells):
    """The real doors on Map 8, one on each of `Village B`'s two cells."""
    evs = []
    for i, (x, y) in enumerate(sorted(cells)):
        arrive = S.narrate([
            "A little village behind a low hedge, one road",
            "through it, and at the gate a small figure with",
            "something shiny on its head, waiting."])
        arrive += R.choice_block(
            ["Go in", "Press on"],
            [[R.play_se("Move1"),
              R.transfer(MAP_GLADHOLLOW, ARRIVE[0], ARRIVE[1], 6, 0)],
             S.narrate(["You press on. Behind you, faintly, somebody",
                        "says \"Welcome to Gladhollow!\" to nobody."])])
        evs.append(R.event(base_id + i, SITE, x, y, [R.page(
            arrive, img=R.image(""), trigger=1, priority=0, through=True)]))
    return evs


def build():
    R.save_map(MAP_GLADHOLLOW, gladhollow_map())
    R.save_map(MAP_MAYORS, mayors_map())
