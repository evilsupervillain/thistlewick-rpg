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
"""
import db
import rmmzdata as R
import story as S
from places import MAP_CLANGING, MAP_WORKS, MAP_VALVE, MAP_FORGE, MAP_PARISH

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
