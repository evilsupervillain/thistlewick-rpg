"""Spare Cotterill, aged nine - `SPARE.md` for the design, `QUESTS.md` part F
for the order it is built in, `COMPANIONS.md` for his quests.

Nothing here draws a map, and this module imports no place module: `north.py`
calls in here for pages, and `db.build_spare` holds his records.

F1, Spare joins (`QUESTS.md` F1)
--------------------------------
He has asked every Chosen One who ever walked up that street, and been told
he cannot come. He can come. It takes `SPARE.md`'s four conditions, all of
them read off state the town already keeps, and then it takes getting past
his mother, who is right.

* **The gate is Gudgeon's**, Map 25 event 4, a page below her one self
  switch on `SW_SPARE_ASKED`. A page condition names two switches at most, so
  she checks the rest out loud, one section of the form at a time: Spare
  heard in full (his own last self switch), the family met (`FAMILY`, every
  one of them a `talker` whose self switch A is the meeting - **not Cotter**,
  who lives in Great Dunnage and is F4's), and the airship (`SW_AIRSHIP`,
  the day Ott hands it over) - he is nine, and he is not walking.
* **Shim's washer** is carried, never required: a page below her one self
  switch on `SW_SPARE_ASKED`. After he has joined it is his to wear at once.
* **The scene is Spare's**, Map 21 event 13, two pages below his ladder's
  terminal (C) on `SW_SPARE_FORM`: the whole of `SPARE.md` 2 the first time,
  and the short ask on D, which "Not yet", "no room" and a lost argument all
  set. Then a third page, on his recruit switch, takes him off the doorstep.
* **The argument is fought by Spare alone** (`SPARE.md` 3): the party array
  is set aside in `$gameTemp`, he is set up at a fixed level, the troop
  aborts at a quarter, and the party is put back **after** the branches, so
  it happens on every path. He is set up only here, and only until he has
  won, so `setup()` never runs on anybody who has been in the party.

F2, SPA-1 The Letters (`QUESTS.md` F2)
--------------------------------------
His mother's third term was "you write". There is no period post box on any
sheet, so the post is **the courier**: one man, red coat and flat cap, already
standing in each of eight towns when the party gets there - the Former
Premises on its rock included - and never explaining. He is there only while
Spare is in the party (he writes them); without him the event is an empty
page, and the town is today's town.

* **A letter is two halves.** The first two lines are the town's, the last
  two are `SAGA`'s, chosen by **how many he has posted so far** - so whatever
  order the player goes round in, the letters get less true one at a time and
  the dragon arrives on the third. `VAR_SPA1_POSTED` counts them; which town
  each went from is `VAR_SPA1_ORDER`, one decimal digit per town (digit *i*
  is the place in the order of `TOWNS[i]`), which is what lets the copies be
  read back in the order they went.
* **The copies** are item 73, given with the first letter, used from the
  menu: common event 5, `copies()`, one window per letter and Next.
* **The dinner hour** is Mrs Cotterill's, Map 21 event 11, on pages below her
  one self switch: a page while he is still writing, and with all eight
  posted she takes the party up to the works, where `dinner_hour` (Map 22) is
  an autorun on `SW_SPA1_DINNER` and she reads the last one out to the shift.

F3, SPA-4 The Pen Pal (`QUESTS.md` F3)
--------------------------------------
Effie Gotobed of Much Pottering (`pottering.py`, which hands in where things
are) has been his pen pal since the twinning paired them at six. She told him
about a volcano and a sea serpent; he told her he drives the Two Hundred.

* **The meeting is Effie's**, pages appended to her at the gate on actor 11;
  then she shows him round, and `VAR_SPA4_TOUR` says where she has got to.
  Each stop is an Effie of its own, there only while the tour is at it, who
  waits for him if he has been sent home.
* **The courier is here for anybody**, because her letters come here; only
  Spare is asked "Post?". At the end they each write one and he carries it
  four steps.
* **She has had his letters home too** (the courier's doing), so the dragon is
  in the conversation once three have been posted, and not before.
"""
import copy

import db
import rmmzdata as R
import story as S
from places import (MAP_CLANGING, MAP_WORKS, MAP_VALVE, MAP_FORGE, MAP_PARISH,
                    MAP_SOPPING, MAP_RESTWELL, MAP_EVERMORE, MAP_GLADHOLLOW,
                    MAP_PREMISES, MAP_FROSTWICK, MAP_ASHCOMBE, MAP_COLLEGIUM)

SPARE_EVENT = 13                # Map 21
# SPARE.md 1 B, as it listed them: the doorstep, and the four indoors. Each
# is a `talker`, whose self switch A is "has been spoken to". Checked against
# the built maps by `check_family`, because the ids are north.py's.
FAMILY = [(MAP_CLANGING, 11, "Mrs Cotterill"), (MAP_CLANGING, 12, "Mr Cotterill"),
          (MAP_CLANGING, 14, "Ferrule Cotterill"),
          (MAP_CLANGING, 15, "Clevis Cotterill"),
          (MAP_CLANGING, 16, "Shim Cotterill"), (MAP_CLANGING, 17, "Bessie Marsden"),
          (MAP_VALVE, 5, "Rivet Cotterill"), (MAP_PARISH, 4, "Gudgeon Cotterill"),
          (MAP_WORKS, 9, "Tappet Cotterill"), (MAP_FORGE, 4, "Grommet Cotterill")]

HEARD = "$gameSelfSwitches.value([%d, %d, 'C'])" % (MAP_CLANGING, SPARE_EVENT)
MET = " && ".join("$gameSelfSwitches.value([%d, %d, 'A'])" % (m, e)
                  for m, e, _ in FAMILY)


def check_family():
    """The ids in `FAMILY` are `north.py`'s; say so loudly if they move."""
    for m, e, name in FAMILY + [(MAP_CLANGING, SPARE_EVENT, "Spare Cotterill")]:
        ev = R.load("Map%03d.json" % m)["events"][e]
        assert ev and ev["name"] == name, (m, e, name, ev and ev["name"])


# ------------------------------------------------------------- Gudgeon ----
def _sections():
    """The three sections of Form P-9 she will not get up for. The first one
    that is not met is the one she reads out."""
    no_hearing = S.say("Gudgeon", [
        "Section one. The applicant has been",
        "heard in full.",
    ]) + S.say("Gudgeon", [
        "You have not heard him in full.",
        "He has more. He always has more.",
    ])
    no_family = S.say("Gudgeon", [
        "Section two. The applicant's family",
        "has been met. All of it.",
    ]) + S.say("Gudgeon", [
        "It is a long section.",
        "Mam has the list. So do I.",
    ])
    no_airship = S.say("Gudgeon", [
        "Section three. Means of travel.",
    ]) + S.say("Gudgeon", [
        "He is nine. He is not walking to",
        "a tower through the Gloamwood.",
    ]) + S.say("Gudgeon", [
        "If somebody had a way of getting",
        "there that was not walking, it would",
        "be different.",
    ])
    issue = S.narrate([
        "She gets up. She goes to the third drawer of the",
        "cabinet without looking, and takes out one sheet,",
        "and blows on it.",
    ]) + S.say("Gudgeon", [
        "Form P-9. Application by a Minor to",
        "Accompany a Chosen One.",
    ]) + S.say("Gudgeon", [
        "It wants a parent or a guardian.",
        "Signed. In ink.",
    ]) + S.narrate([
        "She looks at you for a moment, as if writing your",
        "name in a register.",
    ]) + S.say("Gudgeon", [
        "Good luck.",
    ]) + [R.gain_item(db.IT_FORM_P9, 1)] + S.got([
        "Got \\I[193]\\C[3]Form P-9\\C[0]."]) + [
        R.control_switch(db.SW_SPARE_FORM, True)]
    return R.if_then(R.condition_script(HEARD), R.if_then(
        R.condition_script(MET), R.if_then(
            R.condition_switch(db.SW_AIRSHIP), issue, no_airship),
        no_family), no_hearing)


def gudgeon_pages(img):
    """Pages 3-4 for Gudgeon (Map 25, event 4), below her one self switch:
    the form asked for once Spare has applied, and her own last page plus a
    line once it is issued."""
    asked = S.say("Gudgeon", [
        "Spare has applied, then.",
    ]) + S.say("Gudgeon", [
        "There is a form for it. P-9.",
        "Nobody has ever asked for one.",
    ]) + S.narrate([
        "She knows exactly where it is. She does not get up.",
    ]) + _sections()
    after = S.say("Gudgeon", [
        "Two t's and two l's.",
        "Everybody gets it wrong.",
    ]) + S.say("Gudgeon", [
        "And Mam signs it, or nobody does.",
    ])
    look = dict(img=img, trigger=0, priority=1)
    return [
        R.page(asked, conditions={"selfSwitchValid": True, "selfSwitchCh": "A",
                                  "switch1Valid": True,
                                  "switch1Id": db.SW_SPARE_ASKED}, **look),
        R.page(after, conditions={"selfSwitchValid": True, "selfSwitchCh": "A",
                                  "switch1Valid": True,
                                  "switch1Id": db.SW_SPARE_FORM}, **look),
    ]


# ---------------------------------------------------------------- Shim ----
def shim_pages(img, move_type=0):
    """Pages 3-4 for Shim (Map 21, event 16), below her one self switch: the
    washer she said he could have, and afterwards her own last line plus
    one. Carried, never required (`SPARE.md` 1 F); if he is already with
    you, he puts it on."""
    give = S.say("Shim", [
        "Is it for Spare?",
    ]) + S.narrate([
        "You say that it is.",
    ]) + S.say("Shim", [
        "I said he can have a washer.",
    ]) + S.narrate([
        "She looks in the tin for a long time. She does not",
        "offer the bearing. It is not that sort of conversation.",
    ]) + S.say("Shim", [
        "That one. It is a good one.",
        "It has been flat the whole time.",
    ])
    to_bag = [R.gain_item(db.IT_WASHER, 1)] + S.got([
        "Got \\I[145]\\C[3]A Washer, Off Shim\\C[0]."])
    to_him = [R.gain_armor(db.AR_WASHER, 1)] + S.got([
        "Got \\I[145]\\C[3]A Washer, Off Shim\\C[0]."]) + R.script([
        "$gameActors.actor(%d).changeEquipById(%d, %d);"
        % (db.SPARE, db.ET_ACCESSORY, db.AR_WASHER)]) + S.narrate([
        "Spare puts it on a bootlace, and wears it."])
    give += R.if_then(R.condition_switch(db.SW_SPARE_JOINED), to_him, to_bag)
    give += [R.self_switch("B", True)]
    after = S.say("Shim", [
        "You can hold the bearing if you like.",
    ]) + S.narrate([
        "There is one fewer washer in the tin. She has counted.",
    ])
    look = dict(img=img, trigger=0, priority=1, move_type=move_type)
    return [
        R.page(give, conditions={"selfSwitchValid": True, "selfSwitchCh": "A",
                                 "switch1Valid": True,
                                 "switch1Id": db.SW_SPARE_ASKED}, **look),
        R.page(after, conditions={"selfSwitchValid": True,
                                  "selfSwitchCh": "B"}, **look),
    ]


# --------------------------------------------------------------- Spare ----
def _pitch():
    """`SPARE.md` 2, "He asks again, and this time he has an answer ready"."""
    c = S.say("Spare", ["Can I come yet?"])
    c += S.narrate([
        "He asks it the way he has asked it every day.",
        "Then he does something he has not done before.",
        "He puts the bag down.",
    ])
    c += S.say("Spare", [
        "I have thought about your reasons.",
        "You said I am nine. I said I am nine in a",
        "useful way. You did not ask what that means.",
    ])
    c += S.narrate(["You ask what it means."])
    c += S.say("Spare", [
        "The boiler has ninety tubes in it.",
        "They have to be brushed. A man does not fit.",
        "I fit.",
    ])
    c += S.say("Spare", [
        "I have been going in since I was six.",
        "Miss Hoyle pays me in buns.",
        "I have never once been frightened.",
    ])
    c += S.narrate(["He considers this."])
    c += S.say("Spare", [
        "I have been frightened. Not of the dark.",
        "Of coming out and nobody being there.",
        "There is always somebody there.",
    ])
    c += S.say("Spare", [
        "In the spring there will be ten of us.",
        "I will not be the littlest one any more.",
    ])
    c += S.say("Spare", [
        "I am not sad about it. I have had nine",
        "years of being the littlest and it is a",
        "very good job.",
    ])
    c += S.say("Spare", [
        "I would just like to have done one thing",
        "first.",
    ])
    # SPARE.md's optional window: the player who did not scrap Eighty-Four.
    c += R.if_then(R.condition_switch(db.SW_84_REBUILT), S.say("Spare", [
        "You mended the one in the field.",
        "Everyone said scrap her.",
        "You did not say scrap her.",
    ]))
    c += S.narrate(["You ask what is in the bag."])
    c += S.say("Spare", [
        "A jumper. A tin. A washer off Shim.",
        "There was bread. There is not now.",
    ])
    c += S.say("Spare", [
        "And a drawing of the Two Hundred.",
        "With me on it.",
    ])
    c += S.narrate([
        "He does not show you the drawing.",
        "He tells you the drawing is in there, which is",
        "not the same thing, and is worse.",
    ])
    return c


def _again():
    """The short ask, for every time after the first."""
    lost = S.say("Spare", ["Can I come yet?"]) + S.narrate([
        "He has had his tea. He has washed his hands.",
        "He has been thinking about it.",
    ]) + S.say("Spare", ["I have been thinking about Mam."])
    waiting = S.say("Spare", ["Can I come yet?"]) + S.narrate([
        "The bag is down already. He has been ready since you",
        "came up the street.",
    ])
    return R.if_then(R.condition_switch(db.SW_SPARE_REFUSED), lost, waiting)


def _mam():
    """`SPARE.md` 2, "Mam" - in full the first time, and short once she has
    already won one. The trope is the fight starting, so it is counted on the
    first argument and not again."""
    first = S.narrate([
        "Mrs Cotterill has been standing behind you.",
        "You do not know for how long.",
    ]) + S.say("Mrs Cotterill", ["No."]) + S.say("Mrs Cotterill", [
        "I have had him out of a boiler.",
        "Nine times. And out of a flue, and a",
        "culvert, and a drain we do not discuss.",
    ]) + S.say("Mrs Cotterill", [
        "Every time, he came out.",
        "Every time, I was there.",
    ]) + S.say("Mrs Cotterill", [
        "You are going to a tower that",
        "eats the people who go to it.",
        "I would not be there.",
    ]) + S.say("Spare", ["Mam."]) + S.say("Mrs Cotterill", [
        "No, love.",
    ]) + S.say("Spare", ["Then I will have to change your mind."]) + S.narrate([
        "You have seen this before. Somebody wants a",
        "thing, somebody else says no, and a fight",
        "starts. It is the only way anyone in this",
        "world has ever settled anything.",
    ]) + [S.trope()] + S.narrate([
        "Nobody raises a hand to anybody.",
        "It is an argument. It is simply that up here",
        "an argument is a serious piece of work.",
    ])
    again = S.narrate([
        "Mrs Cotterill has been standing behind you again.",
    ]) + S.say("Mrs Cotterill", ["No, love."]) + S.say("Spare", [
        "I have been practising.",
    ]) + S.say("Mrs Cotterill", ["On who?"]) + S.say("Spare", ["Shim."])
    return R.if_then(R.condition_switch(db.SW_SPARE_REFUSED), again, first)


def _argument():
    """The fight, with Spare alone (`SPARE.md` 3 and 4). The party array goes
    into `$gameTemp` and comes back after every branch; `$gameTemp` is not
    saved, and nothing can be saved while an event runs."""
    c = R.script([
        "const s = $gameActors.actor(%d);" % db.SPARE,
        "$gameTemp._spareParty = $gameParty._actors.slice();",
        "$gameTemp._spareWon = false;",
        "s.setup(%d);" % db.SPARE,
        "s.recoverAll();",
        "$gameParty._actors = [%d];" % db.SPARE,
    ])
    c += [R.battle(db.TR_MAM, can_escape=False, can_lose=True)]
    won = R.script(["$gameTemp._spareWon = true;"])
    # 601 she was somehow beaten, 602 she stopped (the troop's abort), 603
    # he lost. The first two are the same scene.
    for code, body in [(601, won), (602, won), (603, [])]:
        c += [{"code": code, "indent": 0, "parameters": []}]
        c += R.shift(body, 1)
        c += [{"code": 0, "indent": 1, "parameters": []}]
    c += [{"code": 604, "indent": 0, "parameters": []}]
    c += R.script([
        "$gameParty._actors = $gameTemp._spareParty;",
        "$gameTemp._spareParty = null;",
        "$gamePlayer.refresh();",
        "$gameMap.requestRefresh();",
    ])
    return c + R.if_then(R.condition_script("$gameTemp._spareWon"),
                         _concedes(), _does_not())


def _concedes():
    """`SPARE.md` 2, "She concedes" - on the map, where the faces are - and
    then he joins: late, levelled to the party, permanent."""
    c = S.narrate([
        "She stops. Not because she is tired.",
        "Because he has not.",
    ]) + S.say("Mrs Cotterill", [
        "Nine years, and you have never",
        "once let a thing go.",
        "I do not know where you get it.",
    ]) + S.say("Mr Cotterill", ["Mam."]) + S.say("Mrs Cotterill", [
        "I know.",
    ]) + S.narrate([
        "She picks the bag up and looks in it.",
        "She takes out the drawing and looks at that,",
        "for rather longer, and puts it back.",
    ]) + S.say("Mrs Cotterill", ["Right. Terms."]) + S.say("Mrs Cotterill", [
        "Jumper on.",
        "You do not go in first.",
        "You write. It does not have to be long,",
        "and it does not have to be true.",
    ]) + S.say("Spare", ["Yes, Mam."]) + S.say("Mrs Cotterill", [
        "And you.",
    ]) + S.narrate(["She hands you the bag."]) + S.say("Mrs Cotterill", [
        "Bring him back.",
    ])
    # Shim's washer, if it was carried here, goes on him.
    c += R.if_then(R.condition_item(db.IT_WASHER),
                   [R.gain_item(db.IT_WASHER, -1),
                    R.gain_armor(db.AR_WASHER, 1)])
    c += [R.change_party(db.SPARE, add=True, initialize=False)]
    c += R.script([
        "const s = $gameActors.actor(%d);" % db.SPARE,
        "const lv = Math.max(s.level, $gameParty.highestLevel());",
        "if (lv > s.level) s.changeLevel(lv, false);",
        "if ($gameParty.hasItem($dataArmors[%d])) s.changeEquipById(%d, %d);"
        % (db.AR_WASHER, db.ET_ACCESSORY, db.AR_WASHER),
        "s.recoverAll();",
    ])
    c += [R.learn_skill(db.SPARE, db.SK_THE_DRAWING),
          R.gain_item(db.IT_FORM_P9, -1), R.play_me("Item")]
    c += R.text(["\\C[3]Spare\\C[0] joined the party!"])
    # The second trope is the secret tenth companion himself (SPARE.md 7).
    c += [R.control_switch(db.SW_SPARE_JOINED, True),
          R.control_switch(db.SW_SPARE_KNOWN, True),
          R.control_variable_add(db.VAR_COMPANIONS, 1), S.trope()]
    return c


def _does_not():
    """`SPARE.md` 2, "She does not". Nothing is lost but the argument; he can
    come back and try again tomorrow, which is what a nine-year-old would do."""
    return S.narrate(["It is not close."]) + S.say("Spare", [
        "I nearly had you.",
    ]) + S.say("Mrs Cotterill", ["You did not."]) + S.say("Mrs Cotterill", [
        "Tea is at six. Wash your hands.",
    ]) + S.narrate([
        "He takes it extremely well.",
        "He does not put the bag down.",
    ]) + [R.control_switch(db.SW_SPARE_REFUSED, True), R.self_switch("D", True)]


def _choice():
    """Come with me, or not yet - and no room is his line, not the game's."""
    not_yet = S.say("Spare", ["Right."]) + S.narrate([
        "He takes it extremely well.",
        "He picks the bag back up.",
    ]) + [R.self_switch("D", True)]
    full = S.say("Spare", ["You have got three already."]) + S.say("Spare", [
        "I will wait. I am extremely good at it.",
    ]) + [R.self_switch("D", True)]
    come = R.if_then(
        R.condition_script("$gameParty.size() < %d" % S.PARTY_LIMIT),
        _mam() + _argument(), full)
    return R.choice_block(["Come with me", "Not yet"], [come, not_yet])


def spare_pages(img):
    """Pages 5-7 for Spare (Map 21, event 13), below his ladder's terminal,
    C: the whole conversation on the form, the short ask on D, and gone once
    he is coming - walk-through, so the doorstep is not a wall."""
    look = dict(img=img, trigger=0, priority=1)
    return [
        R.page(_pitch() + _choice(),
               conditions={"selfSwitchValid": True, "selfSwitchCh": "C",
                           "switch1Valid": True, "switch1Id": db.SW_SPARE_FORM},
               **look),
        R.page(_again() + _choice(),
               conditions={"selfSwitchValid": True, "selfSwitchCh": "D",
                           "switch1Valid": True, "switch1Id": db.SW_SPARE_FORM},
               **look),
        R.page([], img=R.image(""), trigger=0, priority=1, through=True,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_SPARE_JOINED}),
    ]


# ======================================================= SPA-1, The Letters ==
COURIER = "Courier"

# The eight towns: key, map, the courier's event id there (appended by that
# town's own module, after everything it had), the town's half of the letter,
# and anything the town adds to finding him there.
TOWNS = [
    ("sopping", MAP_SOPPING, 20, [
        "Dear Mam, I am at the seaside. The sea is right there.",
        "I have checked. It goes out and then it comes back.",
    ], []),
    ("restwell", MAP_RESTWELL, 11, [
        "Dear Mam, Restwell has nineteen inns and one street.",
        "You are not allowed to sleep in the road. I asked.",
    ], []),
    ("evermore", MAP_EVERMORE, 8, [
        "Dear Mam, the elves have no way in. You jump off a ledge",
        "into some leaves. A man rakes them. It is his whole job.",
    ], []),
    ("gladhollow", MAP_GLADHOLLOW, 16, [
        "Dear Mam, here they pay a boy a copper and a half to say",
        "goodbye to you. There is a vacancy. I have applied.",
    ], []),
    ("premises", MAP_PREMISES, 12, [
        "Dear Mam, I am on a rock in the sky. There is a throne",
        "and a waiting area. I waited. Only the post came.",
    ], [
        "There is no road up here. There is nothing up here",
        "at all, except sky, and a lift, and now him.",
    ]),
    ("frostwick", MAP_FROSTWICK, 13, [
        "Dear Mam, it snows here because they pay it to. There is",
        "a schedule. I have made a snowman. He is under contract.",
    ], []),
    ("ashcombe", MAP_ASHCOMBE, 12, [
        "Dear Mam, Ashcombe has a post office. The window says ALL",
        "LETTERS ANSWERED. I did not risk it. I gave it to the man.",
    ], []),
    ("collegium", MAP_COLLEGIUM, 13, [
        "Dear Mam, I am at a college for wizards. I have been made",
        "a Fellow. There is a duck who is a Fellow too. We get on.",
    ], []),
]
TOWN = {key: i for i, (key, *_rest) in enumerate(TOWNS)}

# The second half, by how many have gone before it - so the first letter is
# nearly true wherever it is posted, and the eighth is never true anywhere.
SAGA = [
    ["I have my jumper on and I did not go in first. Nobody",
     "has hit me. There is no dragon. Love, Spare."],
    ["There is probably no dragon. Bram says there is not.",
     "I am keeping an eye out anyway. Love, Spare."],
    ["There is a dragon. It is only small. It has followed us",
     "since breakfast. I have called it Ferrule. Love, Spare."],
    ["The dragon is the size of the Two Hundred now. Bram has",
     "asked it to stop following us. It said no. Love, Spare."],
    ["I have spoken to the dragon. It knows where we live.",
     "It says hello to the shift. Say hello back. Love, Spare."],
    ["Me and the dragon have had a fight. I won. I did not go in",
     "first. It went in first. It said sorry. Love, Spare."],
    ["The dragon would like a job at the works. I said ask Ott.",
     "It is practising its chalk line. Love, Spare."],
    ["The dragon is coming home with us for its tea. Please do",
     "more potatoes. It has never had a potato. Love, Spare."],
]
LETTERS = len(SAGA)
assert len(TOWNS) == LETTERS

# Finding him there, by how many have gone before: he is always already here.
ARRIVES = [
    ["A man in a red coat and a flat cap, with a satchel on",
     "a strap, is standing here as if he has been here all",
     "morning."],
    ["The man in the red coat is here. You left him in another",
     "town entirely. He does not look as if he hurried."],
    ["The man in the red coat. He got here first.",
     "His boots are dry."],
    ["The courier is here. Nobody asks him how any more."],
    ["The courier is here. He touches his cap to Spare,",
     "and not to you."],
    ["The courier is here. You did not pass him on the road.",
     "There was only the one road."],
    ["The courier is here, eating an apple.",
     "He has nearly finished it."],
    ["The courier is here. Of course he is here."],
]


def letter(town, k):
    """The four lines that went from `TOWNS[town]` as letter `k` (from 0)."""
    return TOWNS[town][3] + SAGA[k]


def _digit(town):
    return ("Math.floor($gameVariables.value(%d) / %d) %% 10"
            % (db.VAR_SPA1_ORDER, 10 ** town))


def check_couriers():
    """The ids in `TOWNS` are the towns' own appended events: say so loudly if
    a town gains an event in front of its courier."""
    for key, m, e, _, _ in TOWNS:
        ev = R.load("Map%03d.json" % m)["events"][e]
        assert ev and ev["name"] == "The Courier", (key, m, e, ev and ev["name"])


def _post(town):
    """Spare writes one, on his knee, and hands it over."""
    _, _, _, _, extra = TOWNS[town]
    c = []
    for k in range(LETTERS):
        c += R.if_then(R.condition_variable(db.VAR_SPA1_POSTED, k),
                       S.narrate(ARRIVES[k]))
    if extra:
        c += S.narrate(extra)
    c += S.say(COURIER, ["Post?"])
    c += S.say("Spare", ["One for Upper Clanging.",
                         "Mrs Cotterill. It is quite urgent."])
    c += S.narrate(["He writes it on his knee, with his tongue out,",
                    "and lets you read it first."])
    for k in range(LETTERS):
        c += R.if_then(R.condition_variable(db.VAR_SPA1_POSTED, k),
                       S.narrate(letter(town, k)))
    c += R.script([
        "const v = $gameVariables;",
        "v.setValue(%d, v.value(%d) + (v.value(%d) + 1) * %d);"
        % (db.VAR_SPA1_ORDER, db.VAR_SPA1_ORDER, db.VAR_SPA1_POSTED,
           10 ** town),
    ])
    c += [R.control_variable_add(db.VAR_SPA1_POSTED, 1), R.self_switch("A")]
    c += S.narrate(["He licks it shut and hands it over."])
    c += S.say(COURIER, ["Upper Clanging. Dinner hour."])
    # The first one: the copies, and the cliche, which is that there will be
    # one of these in every town.
    c += R.if_then(R.condition_variable(db.VAR_SPA1_POSTED, 1), S.narrate([
        "Spare has kept a copy, in pencil, in case.",
    ]) + [R.gain_item(db.IT_SPA1_COPIES, 1)] + S.got([
        "Got \\I[192]\\C[3]Spare's Copies\\C[0]."]) + S.narrate([
        "You have a feeling there is going to be one of these",
        "in every town, and that you will be asked to find",
        "all of them.",
    ]) + [S.trope()])
    c += R.if_then(R.condition_variable(db.VAR_SPA1_POSTED, LETTERS), S.narrate([
        "That is eight. Spare puts the pencil away.",
    ]) + S.say("Spare", ["That is all of it.",
                         "I have told her everything."]) + S.narrate([
        "Somewhere up the valley, it is nearly the dinner hour.",
    ]))
    return c


def courier(key, x, y):
    """The courier in one of `TOWNS`, for that town's module to append: an
    empty page, and himself only while Spare is in the party."""
    town = TOWN[key]
    _, _, event_id, _, _ = TOWNS[town]
    img = R.image(*S.FACES[COURIER], direction=2)
    spare = {"actorValid": True, "actorId": db.SPARE}
    rounds = S.say(COURIER, ["On my rounds."]) + S.narrate([
        "He does not say whose."])
    return R.event(event_id, "The Courier", x, y, [
        R.page([], img=R.image(""), trigger=0, priority=0),
        R.page(_post(town), img=img, trigger=0, priority=1, conditions=spare),
        R.page(rounds, img=img, trigger=0, priority=1,
               conditions=dict(spare, selfSwitchValid=True, selfSwitchCh="A")),
    ])


def copies():
    """Common event 5, from the menu: every letter posted, in the order it
    went, one window each, with Next."""
    c = S.narrate(["Spare's copies, in pencil, in the order they went.",
                   "He keeps one of everything, in case."])
    c += R.script(["$gameTemp._spaLetter = 1;"])
    c += [R.label("letter")]
    for k in range(1, LETTERS + 1):
        body = []
        for town in range(LETTERS):
            body += R.if_then(R.condition_script("%s === %d" % (_digit(town), k)),
                              S.narrate(letter(town, k - 1)))
        body += R.if_then(
            R.condition_variable(db.VAR_SPA1_POSTED, k, 3),
            R.choice_block(["Next", "Put them away"], [
                R.script(["$gameTemp._spaLetter = %d;" % (k + 1)])
                + [R.jump_to_label("letter")], []], cancel=1))
        c += R.if_then(R.condition_script("$gameTemp._spaLetter === %d" % k),
                       body)
    return c


def mam_pages(img):
    """Pages 3-5 for Mrs Cotterill (Map 21, event 11), below her one self
    switch: while he is writing, the dinner hour once all eight are in, and
    afterwards her own last page plus a line."""
    writing = S.say("Mrs Cotterill", [
        "You have been writing.",
    ]) + S.say("Spare", ["It does not have to be true."]) + S.say(
        "Mrs Cotterill", ["It does not."]) + S.say("Mrs Cotterill", [
            "Keep them coming, love.",
        ])
    dinner = S.say("Mrs Cotterill", [
        "That is the eighth. It came this",
        "morning, with the milk.",
    ]) + S.say("Mrs Cotterill", [
        "It is the dinner hour.",
        "I am wanted up at the works.",
    ]) + S.say("Spare", ["What for?"]) + S.say("Mrs Cotterill", [
        "Come and see.",
    ]) + [R.control_switch(db.SW_SPA1_DINNER, True),
          # Indoors, so it stops raining: north.door's dry(), which this
          # module cannot import.
          R.set_weather("none", duration=1),
          R.transfer(MAP_WORKS, 12, 16, direction=8)]
    after = S.say("Mrs Cotterill", [
        "Ten in the spring.",
        "Mr Cotterill is very pleased.",
    ]) + S.say("Mrs Cotterill", [
        "There was no dragon. I have kept",
        "them all anyway.",
    ])
    look = dict(img=img, trigger=0, priority=1)
    spare = {"actorValid": True, "actorId": db.SPARE,
             "selfSwitchValid": True, "selfSwitchCh": "A",
             "variableValid": True, "variableId": db.VAR_SPA1_POSTED}
    return [
        R.page(writing, conditions=dict(spare, variableValue=1), **look),
        R.page(dinner, conditions=dict(spare, variableValue=LETTERS), **look),
        R.page(after, conditions={"selfSwitchValid": True, "selfSwitchCh": "A",
                                  "switch1Valid": True,
                                  "switch1Id": db.SW_SPA1_DONE}, **look),
    ]


def _reading():
    """`COMPANIONS.md`'s payoff: the whole shift knows about the dragon."""
    c = S.narrate([
        "It is the dinner hour at the Hoyle Works. The shift has",
        "its tins out: Ott, and Nib, and Tappet, which at the",
        "Hoyle Works is all of it.",
    ]) + S.narrate([
        "Mrs Cotterill has a bundle of letters tied up in",
        "string, and her reading glasses on.",
    ]) + S.say("Tappet", ["Is it the dragon one?"]) + S.say("Mrs Cotterill", [
        "It is the last one.",
    ]) + S.say("Nib", ["Read the dragon one."]) + S.narrate([
        "She reads it out, all four lines, the way she has read",
        "out the other seven: slowly, with the punctuation in.",
    ]) + S.say("Mrs Cotterill", [
        "'The dragon is coming home",
        "with us for its tea. Please do more",
        "potatoes. It has never had a potato.'",
    ]) + S.narrate([
        "There is a silence along the gantry.",
    ]) + S.say("Ott", ["It'll want the big table."]) + S.say("Nib", [
        "We've had a sweep on it all month.",
        "I had Thursday.",
    ]) + S.say("Spare", ["There is not a dragon."]) + S.narrate([
        "Everybody looks at him.",
    ]) + S.say("Spare", [
        "There was never a dragon. I made it",
        "up. Mam said it did not have to be",
        "true.",
    ]) + S.say("Mrs Cotterill", ["I know, love."]) + S.say("Mrs Cotterill", [
        "I did more potatoes anyway.",
    ]) + S.say("Tappet", [
        "I had 'there is no dragon'.",
    ]) + S.narrate([
        "Nib pays her. He is not happy about it.",
    ]) + S.say("Mrs Cotterill", [
        "Right. Back to work,",
        "the lot of you.",
    ]) + S.say("Mrs Cotterill", ["And you. Same terms."]) + S.say("Spare", [
        "Jumper on. Do not go in first.",
        "Write.",
    ]) + S.say("Mrs Cotterill", [
        "It does not have to be long.",
    ])
    c += [R.fadeout_screen(), R.control_switch(db.SW_SPA1_DINNER, False),
          R.control_switch(db.SW_SPA1_DONE, True)]
    c += S.companion_story(db.SPARE)
    c += [R.wait(30), R.fadein_screen()]
    return c


def dinner_hour(event_id, x, y):
    """Map 22: Mrs Cotterill in the works, only for the dinner hour - an empty
    page, and an autorun on `SW_SPA1_DINNER` that ends by turning it off."""
    img = R.image(*S.FACES["Mrs Cotterill"], direction=2)
    return R.event(event_id, "The Dinner Hour", x, y, [
        R.page([], img=R.image(""), trigger=0, priority=0),
        R.page(_reading(), img=img, trigger=3, priority=1,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_SPA1_DINNER}),
    ])


# ====================================================== SPA-4, The Pen Pal ==
# Much Pottering is `pottering.py`'s, and it hands its coordinates in: this
# module imports no place module. Effie's tour is `VAR_SPA4_TOUR`, global, so
# a dismissed Spare's errand waits wherever she was standing: 1 the volcano,
# 2 the sea serpent, 3 the post, 4 done.
EFFIE = "Effie"
_SPA4_SPARE = {"actorValid": True, "actorId": db.SPARE}
_SPA4_EMPTY = dict(img=R.image(""), trigger=0, priority=0)


def _spa4_dragon():
    """A script condition: the dragon has got into the letters by now. She
    has had every one he posted (the courier brings her his letters home as
    well, which he is probably not meant to do)."""
    return R.condition_variable(db.VAR_SPA1_POSTED, 3, 1)


def _spa4_move_on(stage):
    """She runs on ahead to the next place on the tour."""
    return [R.fadeout_screen(), R.control_variable(db.VAR_SPA4_TOUR, stage),
            R.wait(20), R.fadein_screen()]


def _spa4_meeting():
    """Effie at her gate, with Spare in the party: the childhood friend from
    the letters, met at last. Neither of them is what they said."""
    c = S.narrate([
        "The girl at the gate looks at Spare. Spare looks at the",
        "girl at the gate. Neither of them says anything for",
        "some time.",
    ])
    c += S.say(EFFIE, ["You're not six foot."])
    c += S.say("Spare", ["You're not a princess."])
    c += S.say(EFFIE, [
        "I never said I was a princess.",
        "I said I was nearly a princess.",
        "It's different.",
    ])
    c += S.say("Spare", ["How is it different?"])
    c += S.say(EFFIE, ["It's nearly."])
    c += S.narrate([
        "You gather that this is Effie Gotobed, of Much Pottering,",
        "and that the parish councils paired the two of them off",
        "for the twinning when they were six, and that this is the",
        "first time either of them has seen the other.",
    ])
    c += S.narrate([
        "You know this one: the friend from the letters, met at",
        "last, and they know each other at once.",
    ]) + [S.trope()] + S.narrate([
        "They knew each other at once. They are both furious",
        "about it.",
    ])
    c += S.say(EFFIE, ["Where's the Two Hundred?"])
    c += S.say("Spare", ["Parked."])
    c += R.if_then(_spa4_dragon(), S.say(EFFIE, [
        "And where's the dragon?",
    ]) + S.say("Spare", ["...It's out."]) + S.say(EFFIE, [
        "Out where?",
    ]) + S.say("Spare", ["Just out."]))
    c += S.say(EFFIE, ["Do you want to see the volcano?"])
    c += S.say("Spare", ["Yes."])
    c += S.narrate([
        "He says it the way you say yes to a dare. She is off down",
        "the street before he has finished saying it.",
    ])
    return c + _spa4_move_on(1)


def _spa4_volcano():
    c = S.narrate([
        "Effie is standing beside a ring of stones on Mr Dibble's",
        "allotment, in which a heap of leaves is smouldering.",
    ])
    c += S.say(EFFIE, ["That's the volcano."])
    c += S.say("Spare", ["It's a bonfire."])
    c += S.say(EFFIE, [
        "It's a dormant volcano. You can tell",
        "because it's smoking.",
    ])
    c += S.narrate(["Spare looks at it for a long time."])
    c += S.say("Spare", ["It is a very good bonfire."])
    c += S.say(EFFIE, [
        "Mr Dibble lit it in November.",
        "It's never gone out.",
    ])
    c += S.say("Spare", [
        "Our boiler's never gone out.",
        "Not since before Mam.",
    ])
    c += S.say(EFFIE, ["...Is it big?"])
    c += S.say("Spare", ["It has ninety tubes. I brush them."])
    c += S.narrate([
        "It is the first true thing either of them has said all",
        "morning, and they both notice.",
    ])
    c += S.say(EFFIE, ["Come and see the sea serpent."])
    return c + _spa4_move_on(2)


def _spa4_serpent():
    c = S.narrate([
        "Effie and Mr Cobley are looking at the duck pond. The duck",
        "pond is looking back, with nothing on it but one duck.",
    ])
    c += S.say(EFFIE, ["There's a sea serpent in there."])
    c += S.say("Mr Cobley", ["Old Tom. Carp."])
    c += S.say(EFFIE, ["Serpent."])
    c += S.say("Mr Cobley", ["Carp."])
    c += S.say("Spare", ["How big?"])
    c += S.say("Mr Cobley", ["Nobody knows. Nobody's seen him."])
    c += S.narrate(["You all look at the pond for a while."])
    c += [R.play_se("Water1", volume=70, pitch=60), R.wait(30)]
    c += S.narrate([
        "Something under the water, very large and very slow, turns",
        "over. The duck goes up in the air, and comes down somewhere",
        "else, and says so.",
    ])
    c += S.say("Mr Cobley", ["...Thirty years."])
    c += S.say("Spare", ["That was quite big."])
    c += S.say(EFFIE, ["I TOLD you."])
    c += S.say("Spare", ["You said it had a head like a horse."])
    c += S.say(EFFIE, ["It might have."])
    c += S.narrate([
        "Effie says there is one more thing, and it is at the top",
        "of the road, where the man in the red coat is.",
    ])
    return c + _spa4_move_on(3)


def _spa4_post():
    """The end of the tour: the truth, both ways, and then a letter each,
    delivered by hand, which is the courier's shortest round."""
    c = S.say(EFFIE, ["That's the post."])
    c += S.say("Spare", ["I know. He does ours."])
    c += S.say(COURIER, ["Post?"])
    c += S.narrate(["Nobody answers him. Effie is looking at her shoes."])
    c += S.say(EFFIE, ["You don't drive the Two Hundred."])
    c += S.say("Spare", [
        "No. Ott does. I'm not allowed to",
        "touch the wheel.",
    ])
    c += S.say("Spare", ["You're not nearly a princess."])
    c += S.say(EFFIE, ["No."])
    c += R.if_then(_spa4_dragon(), S.say(EFFIE, [
        "And there's no dragon.",
    ]) + S.say("Spare", ["And there's no volcano."]), S.say(EFFIE, [
        "And you're not the foreman.",
    ]) + S.say("Spare", ["And there's no volcano."]))
    c += S.narrate([
        "They consider this, each of them, for a while.",
    ])
    c += S.say(EFFIE, ["Will you still write?"])
    c += S.say("Spare", [
        "Mam says it does not have to be true.",
    ])
    c += S.say(EFFIE, ["Good. Make the dragon bigger."])
    c += S.say("Spare", ["Make the volcano go off."])
    c += S.narrate([
        "They each write one there and then, on their knees, with",
        "their tongues out, and hand it to the courier. He takes",
        "them both, walks the four steps from one of them to the",
        "other, and hands them over.",
    ])
    c += S.say(COURIER, ["Much Pottering."])
    c += S.say(COURIER, ["Upper Clanging."])
    c += S.narrate([
        "They read them at once, in front of each other, which you",
        "are not supposed to do. Spare's says the volcano has gone",
        "off and buried Mr Dibble, who is fine. Effie's says the",
        "dragon is back, and is the size of the parish hall.",
    ])
    c += S.say(EFFIE, ["Is it?"])
    c += S.say("Spare", ["Bigger."])
    c += [R.fadeout_screen(), R.control_variable(db.VAR_SPA4_TOUR, 4),
          R.control_switch(db.SW_SPA4_DONE, True)]
    c += S.companion_story(db.SPARE)
    c += [R.wait(30), R.fadein_screen()]
    return c


def effie_pages(later):
    """Pages 3-5 for Effie at her gate (Much Pottering, event 4): the meeting
    with Spare there; nobody at the gate while she is showing him round; and
    afterwards, her own last page plus a line. `later` is that last page."""
    img = later["image"]
    look = dict(img=img, trigger=0, priority=1)
    after = copy.deepcopy(later["list"][:-1]) + S.say(EFFIE, [
        "He wrote. The dragon's learned to swim.",
        "It's in our pond. Mr Cobley's furious.",
    ])
    return [
        R.page(_spa4_meeting(), conditions=dict(_SPA4_SPARE), **look),
        R.page([], conditions={"variableValid": True,
                               "variableId": db.VAR_SPA4_TOUR,
                               "variableValue": 1}, **_SPA4_EMPTY),
        R.page(after, conditions={"switch1Valid": True,
                                  "switch1Id": db.SW_SPA4_DONE}, **look),
    ]


def tour_events(base_id, volcano, pond, post):
    """Events `base_id` to `base_id + 2`: Effie at each stop of her tour, there
    only while the tour is at that stop. Without Spare she waits for him."""
    img = R.image(*S.FACES[EFFIE], direction=2)
    look = dict(img=img, trigger=0, priority=1)
    stops = [("Effie (at the volcano)", volcano, 1, _spa4_volcano(),
              "the volcano"),
             ("Effie (at the pond)", pond, 2, _spa4_serpent(),
              "the sea serpent"),
             ("Effie (at the post)", post, 3, _spa4_post(), "the post")]
    evs = []
    for i, (name, (x, y), stage, scene, what) in enumerate(stops):
        at = {"variableValid": True, "variableId": db.VAR_SPA4_TOUR,
              "variableValue": stage}
        wait = S.say(EFFIE, [
            "Where's Spare gone? I'm showing him",
            "%s." % what,
        ]) + S.say(EFFIE, ["I'll wait. I'm good at it."])
        evs.append(R.event(base_id + i, name, x, y, [
            R.page([], **_SPA4_EMPTY),
            R.page(wait, conditions=dict(at), **look),
            R.page(scene, conditions=dict(at, **_SPA4_SPARE), **look),
            R.page([], conditions=dict(at, variableValue=stage + 1),
                   **_SPA4_EMPTY),
        ]))
    return evs


def pottering_courier(event_id, x, y):
    """The courier in Much Pottering. Not a ninth posting town: he is here
    because her letters come here, so he is here for anybody, and only Spare
    gets asked "Post?"."""
    img = R.image(*S.FACES[COURIER], direction=2)
    rounds = S.say(COURIER, ["On my rounds."]) + S.narrate([
        "He has a letter in his hand for Miss E. Gotobed, Much",
        "Pottering. Somebody has drawn on the envelope.",
    ])
    spare = S.say(COURIER, ["Post?"]) + S.narrate([
        "Spare looks past him, at the girl with the plaits by the",
        "gate up the street.",
    ]) + S.say("Spare", ["Not today. She is right there."]) + S.narrate([
        "The courier nods, as if that is often the case.",
    ])
    done = S.say(COURIER, ["On my rounds."])
    look = dict(img=img, trigger=0, priority=1)
    return R.event(event_id, "The Courier", x, y, [
        R.page(rounds, **look),
        R.page(spare, conditions=dict(_SPA4_SPARE), **look),
        R.page(done, conditions={"switch1Valid": True,
                                 "switch1Id": db.SW_SPA4_DONE}, **look),
    ])


def well_pages(page):
    """The wishing well (Much Pottering, event 16), afterwards: its own page,
    and a second wish under the first."""
    return [R.page(copy.deepcopy(page["list"][:-1]) + S.narrate([
        "And under it, on the same string, in different pencil:",
        "A DRAGON. S.C.",
    ]), img=page["image"], trigger=1, priority=1, direction_fix=True,
        conditions={"switch1Valid": True, "switch1Id": db.SW_SPA4_DONE})]
