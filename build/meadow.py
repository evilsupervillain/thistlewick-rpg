"""Firstfield Meadow: Map 28, and its rainbow on the world map.

Every Chosen One's journey begins in Firstfield, where the Guild of Guides has
laid on a tutorial and assigned it Fizz, Tutorial Sprite, Third Class. Bram's
began in a turnip field three miles away, and he arrives at this one having
already walked out of the village, down a road and past a turnip with
opinions - which is the joke, and nobody in the meadow will hear of it.

It is optional, it is west of the village gate, and it is four stations and
a graduation:

    ONE    Old Hollis, and a stick (items)         SW_FF_STICK
    TWO    a chest the Guild restocks at nine      SW_FF_CHEST
    THREE  Dilys Fenwick's sheep, which are not    SW_FF_SHEEP_ASKED / _DONE
           lost (quests)
    FOUR   Norbert, who loses for a living         SW_FF_NORBERT
           (combat)

Each station bumps `VAR_FF_STATIONS` once, and Fizz graduates you when it
reaches four - a variable rather than four switches because a page condition
can name two switches at most. Norbert stands in the one gap in the fence
across the top of the meadow, so the graduation lawn behind him is reached by
beating him, which is what a tutorial boss is for.

Every one of the five speaking characters here was made with the Character
Generator and installed by `art.py` into `Gen_People1`; Norbert's battler is
`img/sv_enemies/Norbert_Pelling.png`, a stand-in until real art replaces it.

**Fizz is one event that moves.** She lives on the graduation lawn, and any
event in the meadow that needs her calls `fizz_in()`, which puts her beside the
player - or, for a sign, directly in front of it, which is the whole bit - and
`fizz_out()`, which sends her home. `Game_Event` positions are not saved
across a map load, so if anything ever strands her she is back on her lawn the
next time the map is entered.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import db
import mapkit as K
import rmmzdata as R
import story as S
from places import MAP_WORLD, MAP_MEADOW, WORLD_MEADOW, WORLD_MEADOW_STEP

MW, MH = 30, 24
ARRIVE = (14, 21)                   # just inside the gap in the trees
EXITS = [(14, 23), (15, 23)]
FIZZ_HOME = (15, 3)

# Event ids. Appended to, never reordered: a self switch is keyed on
# (map, event id, letter), so moving an id resets somebody in every save.
EV_ARRIVAL, EV_FIZZ = 1, 2
EV_EXIT_W, EV_EXIT_E = 3, 4
EV_SIGN_GATE, EV_SIGN_ONE, EV_SIGN_TWO = 5, 6, 7
EV_SIGN_THREE, EV_SIGN_FOUR, EV_SIGN_GRAD = 8, 9, 10
EV_HOLLIS, EV_CHEST, EV_DILYS = 11, 12, 13
EV_SHEEP = (14, 15, 16)
EV_NORBERT, EV_NORBERT_DOWN = 17, 18

GEN = "Gen_People1"                 # see art.py for who is in which cell
FIZZ_IMG = R.image(GEN, 0, direction=2)
# There is no sheep anywhere in the stock library, and `!Other1` 2 - the
# snowball that is a perfectly good sheep from the air in `field.isle_sheep` -
# is a boulder at this scale. So the Guild ordered sheep and was sent pigs,
# and the form says sheep, and they are doing their best.
SHEEP_IMG = R.image("Nature", 2)

# The four stations' spots. Everything else on the map is drawn around them.
HOLLIS = (7, 15)
TENT = (4, 12)                      # 3x3; its doorway is the bottom middle
CHEST = (6, 10)
DILYS = (23, 12)                    # at the open gate of an empty pen
SHEEP = [(22, 12), (24, 12), (23, 14)]
FENCE_Y = 7
GAP = (15, FENCE_Y)                 # Norbert stands in it
NORBERT_DOWN = (16, 8)              # and lies down beside it afterwards


# ================================================================== Fizz ====
def fizz(lines):
    return S.say("Fizz", lines)


def fizz_in(front=False):
    """Fizz arrives. In front of the player for a sign, which is the bit;
    otherwise at their side, so she is not drawn on top of whoever they were
    talking to. Falls back to behind them if both sides are taken."""
    if front:
        place = [
            "const p = $gamePlayer, d = p.direction();",
            "const x = $gameMap.roundXWithDirection(p.x, d);",
            "const y = $gameMap.roundYWithDirection(p.y, d);",
        ]
    else:
        place = [
            "const p = $gamePlayer, d = p.direction();",
            "const tries = (d === 2 || d === 8) ? [4, 6, 10 - d] : [2, 8, 10 - d];",
            "let x = p.x, y = p.y;",
            "for (const s of tries) {",
            "  const tx = $gameMap.roundXWithDirection(p.x, s);",
            "  const ty = $gameMap.roundYWithDirection(p.y, s);",
            "  if ($gameMap.isValid(tx, ty) && p.isMapPassable(p.x, p.y, s) &&",
            "      $gameMap.eventsXyNt(tx, ty).length === 0) { x = tx; y = ty; break; }",
            "}",
        ]
    place += [
        "const f = $gameMap.event(%d);" % EV_FIZZ,
        "f.locate(x, y);",
        "f.turnTowardCharacter(p);",
    ]
    return [R.play_se("Chime2", pitch=130)] + R.script(place) + [
        R.show_balloon(EV_FIZZ, 1, wait_flag=True)]


def fizz_out():
    return [R.play_se("Chime2", pitch=150)] + R.script([
        "const f = $gameMap.event(%d);" % EV_FIZZ,
        "f.locate(%d, %d);" % FIZZ_HOME,
        "f.setDirection(2);",
    ])


def station_done(switch_id):
    return [R.control_switch(switch_id, True),
            R.control_variable_add(db.VAR_FF_STATIONS, 1), S.trope()]


# ============================================================== the map =====
def meadow_map():
    g = K.Canvas(MW, MH)
    g.fill(0, 0, MW - 1, MH - 1, 0, K.GRASS)

    # -- paths. A spine up from the gap in the trees, and three branches off
    # it to the stations, each a little tidier than a meadow strictly needs.
    g.fill(14, 8, 15, MH - 1, 0, K.PATH)
    g.fill(FIZZ_HOME[0], FIZZ_HOME[1] + 1, FIZZ_HOME[0], FENCE_Y, 0, K.PATH)
    g.fill(4, 16, 13, 16, 0, K.PATH)              # west to Hollis
    g.fill(5, 15, 5, 15, 0, K.PATH)               # and up to the tent door
    g.fill(7, 10, 13, 10, 0, K.PATH)              # west to the chest
    g.fill(16, 13, 25, 13, 0, K.PATH)             # east to the sheep
    g.autotile(0)

    # -- the fence across the top of the meadow, and its one gap
    for x in range(2, MW - 2):
        if x != GAP[0]:
            g.set(x, FENCE_Y, 3, K.FENCE_PANEL)

    # -- station one: a tent, and a great many sticks
    g.blit(TENT[0], TENT[1], 3, K.TENT)
    g.set(8, 14, 3, K.BARREL)
    g.set(9, 14, 3, K.LOGS)
    g.set(3, 15, 3, K.LOGS)

    # -- station two: the chest, in a ring of flowers, as chests are
    g.scatter([(5, 9), (7, 9), (5, 11), (7, 11)], 3, K.FLOWERS)
    g.scatter([(6, 9), (6, 11)], 3, K.FLOWERS2)

    # -- station three: a sheep pen with nothing in it, because the sheep are
    # lost, officially
    for x in range(19, 26):
        g.set(x, 9, 3, K.FENCE_PANEL)
    g.scatter([(19, 10), (25, 10), (19, 11), (20, 11), (21, 11), (24, 11),
               (25, 11)], 3, K.FENCE_PANEL)
    g.set(20, 14, 3, K.BUCKET)

    # -- signposts. Every one of them has an event on it, and every event on
    # one of them has Fizz in it.
    for x, y in SIGNS.values():
        g.set(x, y, 3, K.SIGNPOST)

    # -- the graduation lawn: flowers, because it is a ceremony
    g.scatter([(11, 3), (19, 3), (12, 2), (18, 2), (12, 5), (18, 5)],
              3, K.FLOWERS)
    g.scatter([(11, 4), (19, 4), (14, 2), (16, 2)], 3, K.FLOWERS3)

    # -- the rest of it, so it is a meadow and not a syllabus
    g.scatter([(10, 19), (19, 18), (24, 20), (4, 20), (22, 16), (9, 5),
               (24, 4), (3, 9)], 3, K.BUSH)
    g.scatter([(18, 21), (11, 13), (25, 17), (6, 19)], 3, K.BUSH2)
    g.scatter([(17, 17), (12, 21), (21, 19), (8, 18), (26, 15), (3, 18),
               (23, 5), (7, 4)], 3, K.FLOWERS)
    g.scatter([(18, 19), (9, 20), (25, 19), (4, 5)], 3, K.FLOWERS2)
    g.scatter([(16, 16), (11, 17), (22, 21)], 3, K.FLOWERS3)
    g.scatter([(26, 21), (3, 12)], 3, K.ROCK)

    # -- trees, two deep all round, with the gap at the bottom for the way in
    for x in range(0, MW, 2):
        g.blit(x, 0, 3, K.TREE)
        if x != EXITS[0][0]:
            g.blit(x, MH - 2, 3, K.TREE_DARK if x % 4 else K.TREE)
    for y in range(2, MH - 2, 2):
        g.blit(0, y, 3, K.TREE if y % 4 else K.TREE_DARK)
        g.blit(MW - 2, y, 3, K.TREE_DARK if y % 4 else K.TREE)
    for x, y in [(26, 2), (2, 2), (26, 5)]:
        g.blit(x, y, 3, K.TREE)

    m = K.new_map(MW, MH, K.TS_OUTSIDE, name="Firstfield Meadow",
                  bgm="Town2", battleback=("Grassland", "Grassland"))
    m["data"] = g.data
    m["events"] = [None] + meadow_events()
    return m


# ================================================================ signs =====
SIGNS = {
    EV_SIGN_GATE: (13, 20),
    EV_SIGN_ONE: (12, 15),
    EV_SIGN_TWO: (12, 11),
    EV_SIGN_THREE: (17, 14),
    EV_SIGN_FOUR: (13, 8),
    EV_SIGN_GRAD: (13, 3),
}


def sign(event_id, name, lines, first, *, trope=False, extra=None):
    """A signpost Fizz gets to first. Her opening line on each sign is its
    own; after that she draws on three she keeps for any sign, in turn, off
    `VAR_FF_SIGNS`, so reading the same one twice does not repeat itself."""
    again = []
    for n, said in enumerate([
            ["That's a SIGN!",
             "...Still a sign! Signs don't change!",
             "That's what's GOOD about them!"],
            ["SIGN! Sign sign sign!",
             "Press the button to READ it!",
             "...You already did. I know. I know."],
            ["Oh! Oh! Do you know what THAT is?"]]):
        body = fizz(said)
        if n == 2:
            body += S.narrate(["You say that it is a sign."])
            body += fizz(["It IS! You're doing SO well!"])
        again += R.if_then(R.condition_script(
            "$gameVariables.value(%d) %% 3 === %d" % (db.VAR_FF_SIGNS, n)), body)
    once = fizz(first) + ([S.trope()] if trope else []) + [R.self_switch("A")]
    cmds = fizz_in(front=True)
    cmds += R.if_then(R.condition_self_switch("A"), again, once)
    cmds += fizz_out()
    cmds += [R.control_variable_add(db.VAR_FF_SIGNS, 1)]
    cmds += S.narrate(lines)
    if extra:
        cmds += extra
    x, y = SIGNS[event_id]
    return R.event(event_id, name, x, y, [R.page(
        cmds, img=R.image(""), trigger=0, priority=1, direction_fix=True,
        through=True)])


def signs():
    return [
        sign(EV_SIGN_GATE, "Sign: Firstfield Meadow", [
            "\\C[6]FIRSTFIELD MEADOW\\C[0]",
            "Where Every Journey Begins*",
            "",
            "*Journeys already in progress also welcome."], [
            "That's a SIGN!",
            "Signs are for READING!",
            "Press the BUTTON to READ it!"], trope=True,
            extra=None),
        sign(EV_SIGN_ONE, "Sign: Station One", [
            "\\C[6]STATION ONE: ITEMS\\C[0]",
            "Please speak to the old man.",
            "He has been expecting you.",
            "He has been expecting everybody."], [
            "ANOTHER sign!",
            "You're really getting the hang of these!"]),
        sign(EV_SIGN_TWO, "Sign: Station Two", [
            "\\C[6]STATION TWO: TREASURE\\C[0]",
            "Please close the chest after use.",
            "The Guild of Guides restocks it at nine."], [
            "A SIGN! And it's about a CHEST!",
            "A sign about a chest! Two for one!"]),
        sign(EV_SIGN_THREE, "Sign: Station Three", [
            "\\C[6]STATION THREE: QUESTS\\C[0]",
            "Mrs Fenwick's sheep are lost.",
            "(They are not lost.)",
            "(They are not sheep.)"], [
            "A SIGN! This one's got BRACKETS!",
            "Don't read the brackets!"]),
        sign(EV_SIGN_FOUR, "Sign: Station Four", [
            "\\C[6]STATION FOUR: COMBAT\\C[0]",
            "Ambush in progress. Please queue.",
            "The ambush is contracted to lose.",
            "The ambush would like you to know he tries."], [
            "A sign! And past it is an ENEMY!",
            "Ooh! Hold on to your STICK!"]),
        sign(EV_SIGN_GRAD, "Sign: Graduation", [
            "\\C[6]GRADUATION\\C[0]",
            "Tutorials completed in this meadow:"], [
            "SIGN! This is the BEST sign!",
            "It's where you GRADUATE!",
            "Nobody's ever READ it before!"],
            extra=R.if_then(
                R.condition_switch(db.SW_FF_GRADUATED),
                S.narrate([
                    "One.",
                    "The one has been painted on over a nought,",
                    "very carefully, by somebody with small hands",
                    "and no experience of paint."]),
                S.narrate(["None."]))),
    ]


# =============================================================== arrival ====
def arrival():
    hello = fizz_in(front=True)
    hello += fizz(["HEY! LISTEN!"])
    hello += fizz(["Welcome to Firstfield Meadow,",
                   "where EVERY Chosen One's",
                   "journey BEGINS!"])
    hello += S.narrate([
        "You point out that yours began some time ago,",
        "in a turnip field, and that since then you",
        "have walked out of a village, down a road,",
        "and past a turnip with opinions."])
    hello += fizz(["Every. Journey. Begins. HERE."])
    hello += fizz(["I'm Fizz! Tutorial Sprite, Third Class!",
                   "I'll be explaining EVERYTHING!",
                   "Once! The Guild is very firm on once!"])
    hello += fizz(["That thing you just did, to get here?",
                   "That was WALKING!",
                   "You press the ARROWS and you WALK!"])
    hello += fizz(["You're doing SO well."])
    hello += fizz_out()
    hello += S.narrate([
        "She zips off up the meadow towards a small",
        "sign that says GRADUATION, trailing sparkles",
        "and the word 'SIGNS!' over her shoulder."])
    hello += [S.trope(), R.control_switch(db.SW_FF_ARRIVED, True)]
    x, y = ARRIVE[0], ARRIVE[1] + 1
    return R.event(EV_ARRIVAL, "Fizz Says Hey", x, y, [
        R.page(hello, img=R.image(""), trigger=3, priority=0, through=True),
        R.page([], img=R.image(""), trigger=0, priority=0, through=True,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_FF_ARRIVED}),
    ])


# ============================================== Fizz, and the graduation ====
def fizz_event():
    todo = fizz(["You're doing SO well!"])
    for switch_id, lines in [
            (db.SW_FF_STICK, ["Old Hollis has an ITEM for you!",
                              "By the TENT! It's a stick!"]),
            (db.SW_FF_CHEST, ["There's a CHEST in the flowers!",
                              "Chests are for OPENING!"]),
            (db.SW_FF_SHEEP_DONE, ["Mrs Fenwick has lost her SHEEP!",
                                   "They're right next to her! They're",
                                   "the pink ones!"]),
            (db.SW_FF_NORBERT, ["And Norbert wants FIGHTING!",
                                "He's in the gap in the fence!"])]:
        todo += R.if_then(R.condition_switch(switch_id, False), fizz(lines))

    grad = [R.play_me("Fanfare1"), R.wait(30)]
    grad += fizz(["You DID it!",
                  "You've finished the TUTORIAL!"])
    grad += fizz(["Nobody has EVER finished the tutorial!",
                  "Forty-seven Chosen Ones, and every",
                  "single one of them SKIPPED it!"])
    grad += S.narrate(["You ask how they skipped it."])
    grad += fizz(["They pressed the button REALLY FAST."])
    grad += fizz(["So by the power vested in me by the",
                  "Guild of Guides, Firstfield Chapter,",
                  "I present you with..."])
    grad += [R.gain_armor(db.AR_CERTIFICATE, 1), R.play_me("Item")]
    grad += S.got(["Got \\I[191]\\C[3]Certificate of Completion\\C[0]."])
    grad += fizz(["It goes in the ACCESSORY slot!",
                  "Next to your STICK!"])
    grad += [R.control_switch(db.SW_FF_GRADUATED, True)]
    grad += fizz(["Any questions? Ask me ANYTHING!"])
    grad += [R.label("questions")]
    grad += R.choice_block(
        ["What is the Dark Lord's weakness?", "Where is the Sacred Key?",
         "What does the lever do?", "No questions"],
        [fizz(["That's LORE!",
               "The Guild doesn't cover LORE!"]) +
         fizz(["Anything else? ANYTHING!"]) + [R.jump_to_label("questions")],
         fizz(["LORE!"]) +
         S.narrate(["You ask whether there is a Sacred Key."]) +
         fizz(["...That's also lore."]) + [R.jump_to_label("questions")],
         fizz(["What lever?"]) +
         S.narrate(["You say that there is always a lever."]) +
         fizz(["...LORE."]) + [R.jump_to_label("questions")],
         fizz(["Nobody EVER has questions!"])])
    grad += fizz(["One day I'm going to be a BOSS WARNING",
                  "SPRITE, First Class! I'll wait outside",
                  "the last door and shout IT'S WEAK TO FIRE!"])
    grad += S.narrate(["You ask whether he is weak to fire."])
    grad += fizz(["...That's LORE."])
    grad += [S.trope()]

    after = fizz(["IT'S WEAK TO FIRE!"])
    after += fizz(["Sorry! Practising!",
                   "I practise on the sheep."])
    after += fizz(["The sheep isn't weak to fire.",
                   "Please don't check."])

    common = dict(img=FIZZ_IMG, trigger=0, priority=1, step_anime=True)
    return R.event(EV_FIZZ, "Fizz", *FIZZ_HOME, [
        R.page(todo, **common),
        R.page(grad, conditions={"variableValid": True,
                                 "variableId": db.VAR_FF_STATIONS,
                                 "variableValue": 4}, **common),
        R.page(after, conditions={"switch1Valid": True,
                                  "switch1Id": db.SW_FF_GRADUATED}, **common),
    ])


# ======================================================= station one ========
def hollis_event():
    def stick(where):
        return S.say("Hollis", ["It's dangerous to go %s!" % where,
                                "Take this."])

    give = S.say("Hollis", ["Ah. There you are."])
    give += R.if_then(
        R.condition_script("$gameParty.size() <= 1"), stick("alone"),
        S.say("Hollis", ["It's dangerous to go-",
                         "...there's a few of you, isn't there."]) +
        R.if_then(R.condition_script("$gameParty.size() === 2"),
                  stick("as a pair"),
                  R.if_then(R.condition_script("$gameParty.size() === 3"),
                            stick("as a three"), stick("as four"))))
    give += [R.gain_armor(db.AR_STICK, 1), R.play_me("Item")]
    give += S.got(["Got \\I[292]\\C[3]A Stick\\C[0]."])
    give += S.narrate(["It is a stick."])
    give += S.say("Hollis", ["Forty-one years I've stood here.",
                             "Eleven thousand, two hundred and six",
                             "sticks. And not one has come back."])
    give += S.narrate(["You ask where they all go."])
    give += S.say("Hollis", ["Cupboards. Every hero's mother has a",
                             "cupboard, and in it is a stick.",
                             "I've seen them. Hundreds."])
    give += S.say("Hollis", ["My Nell cuts them. Every evening, by",
                             "the fire, forty-one years. She picks",
                             "out the straight ones. She says a hero",
                             "deserves a straight stick."])
    give += S.narrate(["You say that is very kind of her."])
    give += S.say("Hollis", ["She is. It's why I married her.",
                             "Well. That and the sticks."])
    give += fizz_in()
    give += fizz(["That's an ITEM!",
                  "Open the MENU and EQUIP it!",
                  "It goes in the ACCESSORY slot!"])
    give += fizz(["Nobody knows why!"])
    give += fizz_out()
    give += station_done(db.SW_FF_STICK)
    give += [R.self_switch("A")]

    returned = S.say("Hollis", ["You're... you're bringing it BACK?"])
    returned += S.narrate(["He turns and shouts at the tent."])
    returned += S.say("Hollis", ["NELL! NELL! ONE'S COME BACK!"])
    returned += S.narrate([
        "There is a clatter from the tent, and then",
        "a great deal of hurrying. A small, round,",
        "delighted woman comes out, takes the stick,",
        "inspects it, and goes back in."])
    returned += S.narrate(["She comes out with another one."])
    returned += S.say("Hollis", ["She says you're to have this one.",
                                 "It's straighter."])
    returned += [R.gain_armor(db.AR_STRAIGHTER_STICK, 1), R.play_me("Item")]
    returned += S.got(["Got \\I[292]\\C[3]A Straighter Stick\\C[0]."])
    returned += S.say("Hollis", ["She's putting yours on the mantelpiece."])
    returned += [R.self_switch("B")]

    rules = S.say("Hollis", ["Just the one stick, lad. Nell's rules."])
    rules += R.if_then(
        R.condition_script("$gameParty.hasItem($dataArmors[%d], false)"
                           % db.AR_STICK),
        R.choice_block(["Give the stick back", "Keep it"],
                       [[R.gain_armor(db.AR_STICK, -1)] + returned, []]))

    proud = S.say("Hollis", ["Nell's dusted it twice today.",
                             "First thing on that mantelpiece in",
                             "forty-one years that isn't me."])

    img = R.image(GEN, 2, direction=2)
    return R.event(EV_HOLLIS, "Old Hollis", *HOLLIS, [
        R.page(give, img=img),
        R.page(rules, img=img,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
        R.page(proud, img=img,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "B"}),
    ])


# ======================================================= station two ========
def chest_event():
    open_it = fizz_in()
    open_it += fizz(["That's a CHEST!",
                     "Chests are for OPENING!",
                     "Press the button to OPEN it!"])
    open_it += fizz_out()
    open_it += [R.play_se("Open1")]
    open_it += S.narrate(["Inside is a Potion, and a note."])
    open_it += [R.gain_item(db.IT_POTION, 1)]
    open_it += S.got(["Got \\I[176]\\C[3]Potion\\C[0]."])
    open_it += S.narrate([
        "The note says: WELL DONE FOR OPENING THE CHEST.",
        "PLEASE CLOSE THE CHEST.",
        "- The Guild of Guides"])
    open_it += R.if_then(
        R.condition_actor_in_party(db.NIX),
        S.narrate([
            "Nix checks the chest for a false bottom.",
            "There is a false bottom. Under it is a",
            "second note, which says WELL DONE, NIX."]) +
        S.say("Nix", ["They've met me, then."]))
    open_it += station_done(db.SW_FF_CHEST)
    open_it += [R.self_switch("A")]

    empty = S.narrate([
        "Empty. The Guild restocks it at nine.",
        "It is the most-opened chest in the world, and",
        "the only one that has ever been expecting you."])
    return R.event(EV_CHEST, "The Tutorial Chest", *CHEST, [
        R.page(open_it, img=R.image("!Chest", 0, direction=2, pattern=1),
               trigger=0, priority=1, direction_fix=True),
        R.page(empty, img=R.image("!Chest", 0, direction=2, pattern=2),
               trigger=0, priority=1, direction_fix=True,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ])


# ===================================================== station three ========
def dilys_event():
    ask = S.say("Dilys", ["Oh, thank goodness. A hero!"])
    ask += S.say("Dilys", ["My sheep are lost! All three of them!",
                           "Will you find them for me?"])
    ask += [R.label("ask")]
    yes = S.say("Dilys", ["Oh, thank you!"])
    yes += S.say("Dilys", ["They're, um.",
                           "They're just there."])
    yes += S.narrate(["There are three animals standing next to her.",
                      "One of them is leaning on her.",
                      "They are pigs."])
    yes += S.narrate(["You mention that they are pigs."])
    yes += S.say("Dilys", ["The Guild ordered sheep. The Guild",
                           "sent these. The form says sheep.",
                           "So they're sheep."])
    yes += S.say("Dilys", ["The Guild says a meadow has to have a",
                           "fetch quest. I said my sheep aren't",
                           "lost. They said, well, lose them a bit."])
    yes += S.say("Dilys", ["So they're lost. A bit. They're very",
                           "good about it. They've been practising",
                           "their baa."])
    yes += fizz_in()
    yes += fizz(["That's a QUEST!",
                 "QUESTS go in your QUEST LOG!"])
    yes += fizz(["...We haven't got a quest log.",
                 "Just remember it! Really hard!"])
    yes += fizz_out()
    yes += [R.control_switch(db.SW_FF_SHEEP_ASKED, True)]
    no = S.say("Dilys", ["But thou must!"])
    no += R.if_then(R.condition_self_switch("C", False),
                    [S.trope(), R.self_switch("C")])
    no += S.say("Dilys", ["Sorry. The Guild gave me that line.",
                          "Will you find them?"])
    no += [R.jump_to_label("ask")]
    ask += R.choice_block(["Yes", "No"], [yes, no])

    waiting = S.say("Dilys", ["Any luck? They're just there.",
                              "About where you'd leave a sheep."])

    found = S.say("Dilys", ["You found them! All three!"])
    found += S.narrate(["The sheep have not moved.",
                        "They look extremely found."])
    found += S.say("Dilys", ["This is for you. It's the reward.",
                             "It's out of my own cupboard, so don't",
                             "tell the Guild it's not a proper one."])
    found += [R.gain_item(db.IT_HI_POTION, 1), R.play_me("Item")]
    found += S.got(["Got \\I[176]\\C[3]Hi-Potion\\C[0]."])
    found += station_done(db.SW_FF_SHEEP_DONE)

    married = S.say("Dilys", ["Tam and I were married in this meadow.",
                              "Fizz explained the vows to us first.",
                              "Twice. In capitals."])
    married += S.say("Dilys", ["Tam cried at the second one. He says",
                               "it was the capitals. He cries at the",
                               "harvest supper as well, bless him."])

    img = R.image(GEN, 3, direction=2)
    return R.event(EV_DILYS, "Dilys Fenwick", *DILYS, [
        R.page(ask, img=img),
        R.page(waiting, img=img,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_FF_SHEEP_ASKED}),
        R.page(found, img=img,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_FF_SHEEP_ASKED,
                           "variableValid": True,
                           "variableId": db.VAR_FF_SHEEP,
                           "variableValue": 3}),
        R.page(married, img=img,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_FF_SHEEP_DONE}),
    ])


def sheep_event(event_id, x, y, n):
    idle = S.narrate(["A sheep, according to the Guild of Guides.",
                      "It is a pig."])
    idle += [R.play_se("Sheep")]
    idle += S.narrate(["It says baa. It has been practising, and",
                       "it would like that noted."])

    find = [R.play_se("Sheep"), R.control_variable_add(db.VAR_FF_SHEEP, 1)]
    find += S.narrate(["You have found a sheep!"])
    find += R.if_then(
        R.condition_variable(db.VAR_FF_SHEEP, 1),
        fizz_in() + fizz(["You FOUND one! That's a SHEEP!"]) +
        S.narrate(["It is a pig."]) +
        fizz(["A QUEST SHEEP!",
              "Two more! You can DO this!"]) + fizz_out())
    find += R.if_then(
        R.condition_variable(db.VAR_FF_SHEEP, 3),
        S.narrate(["That is all three.",
                   "Mrs Fenwick is watching you with enormous,",
                   "and slightly embarrassed, gratitude."]))
    find += [R.self_switch("A")]

    found = S.narrate(["This sheep has been found.",
                       "It seems pleased about it, as a sheep."])
    return R.event(event_id, "Sheep %d (Lost)" % n, x, y, [
        R.page(idle, img=SHEEP_IMG),
        R.page(find, img=SHEEP_IMG,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_FF_SHEEP_ASKED}),
        R.page(found, img=SHEEP_IMG,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ])


# ====================================================== station four ========
def fight_with_branches(troop_id, won, escaped, lost):
    """Battle Processing with its If Win / If Escape / If Lose bodies. `R.battle`
    alone writes no branches, and every other battle in this game is one that
    cannot be lost, so this is the first place that needs them."""
    out = [R.battle(troop_id, can_escape=True, can_lose=True)]
    for code, body in [(601, won), (602, escaped), (603, lost)]:
        out += [{"code": code, "indent": 0, "parameters": []}]
        out += R.shift(body, 1)
        out += [{"code": 0, "indent": 1, "parameters": []}]
    out += [{"code": 604, "indent": 0, "parameters": []}]
    return out


def norbert_event():
    cmds = S.say("Norbert", ["Oh! Hello! Right. Hang on."])
    cmds += S.narrate(["He puts down a sandwich, wipes his hands on",
                       "his trousers, and adopts a stance."])
    cmds += S.say("Norbert", ["STAND AND DELIVER!"])
    cmds += S.say("Norbert", ["...your best attack, if you'd be so",
                              "kind. I'm the tutorial ambush.",
                              "Norbert. Pleased to meet you."])
    cmds += R.if_then(
        R.condition_actor_in_party(db.CORVIN),
        S.say("Corvin", ["Are you my rival?"]) +
        S.say("Norbert", ["Oh, sorry, no. I'm booked up",
                          "through the spring."]))
    cmds += fizz_in()
    cmds += fizz(["That's an ENEMY!",
                  "Enemies are for FIGHTING!"])
    cmds += S.say("Norbert", ["Afternoon, Fizz."])
    cmds += fizz(["Afternoon, Norbert!"])
    cmds += fizz_out()
    won = S.narrate(["Norbert falls over, quite convincingly."])
    won += S.say("Norbert", ["Oh! Ooh. You've got me.",
                             "Down I go. Lovely. Lovely stuff."])
    won += station_done(db.SW_FF_NORBERT)
    escaped = S.say("Norbert", ["Very sensible. Most heroes never",
                                "think of running. Come back when",
                                "you're ready. I'm on till four."])
    lost = [R.recover_all()]
    lost += S.say("Norbert", ["Oh. Oh dear. No, that's not how",
                              "it goes."])
    lost += S.say("Norbert", ["Tell you what, we'll call that one a",
                              "practice. Nobody saw. I won't put it",
                              "on the form."])
    cmds += fight_with_branches(db.TR_NORBERT, won, escaped, lost)

    return R.event(EV_NORBERT, "Norbert (Ambush)", *GAP, [
        R.page(cmds, img=R.image(GEN, 1, direction=2)),
        R.page([], img=R.image(""), priority=0, through=True,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_FF_NORBERT}),
    ])


def norbert_down_event():
    first = S.say("Norbert", ["Lovely fight. Textbook.",
                              "I have a lie down after. It's in",
                              "the contract. Best part of the job."])
    first += S.say("Norbert", ["That's three thousand, one hundred",
                               "and five losses, now. Maud's had",
                               "the first one framed."])
    first += S.narrate(["You ask who Maud is."])
    first += S.say("Norbert", ["The wife. She packs my lunch.",
                               "There's a note in it every day."])
    first += S.narrate(["He fishes the note out of a pocket without",
                        "getting up. It says: LOSE WELL, LOVE."])
    first += S.say("Norbert", ["She says I'm the best loser in the",
                               "county. She means it nicely.",
                               "I asked."])
    first += [R.self_switch("A")]
    again = S.say("Norbert", ["Twenty minutes, then I'm up for the",
                              "next one. Mind the sandwich."])

    img = R.image(GEN + "_Damage", 1, direction=2, pattern=1)
    return R.event(EV_NORBERT_DOWN, "Norbert (Lying Down)", *NORBERT_DOWN, [
        R.page([], img=R.image(""), priority=0, through=True),
        R.page(first, img=img, direction_fix=True,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_FF_NORBERT}),
        R.page(again, img=img, direction_fix=True,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_FF_NORBERT,
                           "selfSwitchValid": True, "selfSwitchCh": "A"}),
    ])


# ================================================================ events ====
def meadow_events():
    evs = [arrival(), fizz_event()]
    for event_id, (x, y) in zip((EV_EXIT_W, EV_EXIT_E), EXITS):
        evs.append(S.exit_tile(event_id, "Way Out", x, y, MAP_WORLD,
                               *WORLD_MEADOW_STEP, direction=6))
    evs += signs()
    evs += [hollis_event(), chest_event(), dilys_event()]
    evs += [sheep_event(event_id, x, y, n + 1)
            for n, (event_id, (x, y)) in enumerate(zip(EV_SHEEP, SHEEP))]
    evs += [norbert_event(), norbert_down_event()]
    evs.sort(key=lambda e: e["id"])
    assert [e["id"] for e in evs] == list(range(1, len(evs) + 1)), \
        "meadow event ids must be dense"
    return evs


# ====================================================== on the world map ====
# The rainbow's two cells: B-sheet 7 is its blocked top and 15 its open foot,
# and the foot is the door. A short spur of road runs to it off the village's
# north road.
RAINBOW = (K.b_tile(7, 0), K.b_tile(7, 1))


def world_layer1(g):
    for x in range(WORLD_MEADOW[0] + 1, 24):
        g.set(x, WORLD_MEADOW[1], 1, K.W_ROAD)


def world_layer3(g):
    g.column(WORLD_MEADOW[0], WORLD_MEADOW[1] - 1, 3, RAINBOW)


def world_events(next_id):
    """`next_id` is the first free event id on Map 8. Appended after every
    event the other modules put there, for the self-switch reason above."""
    look = S.narrate([
        "The end of a rainbow.",
        "Under it is a meadow, a small sign, and the",
        "sound of somebody getting ready to say HEY."])
    look += R.choice_block(
        ["Go in", "Carry on"],
        [[R.play_se("Move1"), R.transfer(MAP_MEADOW, *ARRIVE, 8, 0)], []])
    return [R.event(next_id, "Firstfield Meadow", *WORLD_MEADOW, [R.page(
        look, img=R.image(""), trigger=1, priority=0, through=True)])]


def build():
    R.save_map(MAP_MEADOW, meadow_map())
