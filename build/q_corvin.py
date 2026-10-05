"""Corvin Ash's companion quests - `COMPANIONS.md`, his section, and
`QUESTS.md` for the order they are built in.

This module imports no place module: the place modules call in here for
pages. The one map it draws is COR-2's drowned street, Map 66, which is in no
place (`QUESTS.md` 0.4); COR-1's study is in Mrs Ash's house and is drawn by
`ashcombe.py`.

COR-5, The Appraisal (`QUESTS.md` B4)
-------------------------------------
He takes the black sword to be appraised, expecting a curse. There is no
curse. It is a very good sword in poor condition with a name on the tang
nobody can say aloud, and the appraiser is enthusiastic about the tang. He
asks what a curse would cost to have put on. It is not expensive. She has a
form.

* **It is Miss Fettle's**, Map 62 event 7, below her one-self-switch ladder,
  with Corvin. Both her own pages already eye his sword and are told "No";
  this is the page where he says yes. The appraisal is once
  (`SW_COR5_DONE`); after it, the same page is the curse counter.
* **The curse is state 40**, "Cursed (Elective)": half luck, drawn fire and a
  slow bleed, which is to say a real trait and bad for him, and he takes it.
  It is optional - the form can be declined, and is offered again - and it
  is removable: Miss Fettle takes it off for nothing, and it is the economy
  curse, so it lasts until he next sleeps in a proper bed (an inn's Recover
  All clears it, which is the engine's own rule for states, stated as hers).
* **Afterwards for everybody** is her own last page and a line.

COR-1, Ashcombe (New) (`QUESTS.md` D1)
---------------------------------------
Everyone is delighted to see him. His mother is fine and has a new kitchen.
His bedroom has been rebuilt, larger, with better light, and is a study. He
is asked to speak at the Flood Dinner, and he does, and it goes well.
Nothing in this quest goes wrong for him, which is the joke and the point.

* **What sends him back is his own name.** The Roll in the museum has one
  name marked Away. (Written to.) in place of a tick, and the site left it
  unsaid whose. With Corvin the first read is the published page exactly; on
  the second he finds it is his - two hundred and six people stood on a hill
  and counted him anyway - and says "...Today, then." (`SW_COR1_ON`).
* **The door** keeps its refusal pages; with the switch he knocks, like a
  visitor, and it is always open. It sets Mrs Ash's own self switch A (her
  ladder's terminal) by script, as ALD-4 set Duchess's, because her first
  page is "my boy's away" and her boy is standing in it: the homecoming
  page carries what of that page is still true.
* **The study** is up a flight from the kitchen (a door that appears in her
  north wall once he is home): the Flood Dinner Committee's desk, Hon. Sec.
  Mrs Ash, and a pigeonhole marked C with eleven invitations in it, one a
  year, never posted - "You'd only have said not today." He takes this
  year's (item 65). And the height marks, put back from memory.
* **The Dinner** is at its notice in the street, with the invitation: he
  confirms himself, and it is Saturday. The speech goes well. On the last
  word his mother casts off: the scarf, bright yellow like the new roofs,
  the wrong colour for everything he owns (armour 44, his alone).

COR-2, Ashcombe (Old) (`QUESTS.md` D2)
--------------------------------------
The drowned one is under the lake, which is let down once a year for the
sluices; that week you can walk in. One street, a pub sign, a doorstep, and
in a strongbox in the schoolroom his own report card, which is bad. The one
moment in his story that is allowed to be simply sad, undercut at once.

* **The week is the week of the Flood Dinner**, so it needs COR-1: with
  Corvin, once he has spoken, Ashcombe Lake is down (its page below the
  lake's one-self-switch ladder) and there is a street at the bottom of the
  mud. Map 66, `drowned_street_map`.
* **The doorstep** is the sad part, and nobody says anything clever in it.
  Then the letters cut into it, the same as the tang's, and under them for
  visitors MIND THE STEP: his grandfather made the sword, and it was the
  doorstop. That is its name. One trope (the sunken ruin).
* **The strongbox** is the undercut: the schoolmistress kept everybody's
  reports, and his says he will go far, if he ever gets up. He laughs.
  Item 66, which the ending reads.
"""
import copy

import db
import mapkit as K
import rmmzdata as R
import story as S
from places import MAP_ASHCOMBE_IN, STUDY, STUDY_DESK, STUDY_DOOR, STUDY_MARKS
from places import MAP_DROWNED_STREET, MAP_WORLD, LAKE_SHORE_STEP

FEE = 30


def _cor5_state(add=True):
    """Change State on Corvin: add or remove the elective curse."""
    return {"code": 313, "indent": 0,
            "parameters": [0, db.CORVIN, 0 if add else 1, db.ST_CURSED]}


def _cor5_curse():
    c = [R.lose_gold(FEE), R.play_se("Darkness1", 70), R.wait(20),
         _cor5_state(True)]
    c += S.narrate([
        "Miss Fettle stamps the form, reads a short paragraph",
        "off the back of it in a bored voice, and blows out a",
        "candle. The black sword does not look any different."])
    c += S.say("Miss Fettle", ["There. Cursed. It's the",
                               "economy one: it lasts till you next",
                               "sleep in a proper bed."])
    c += S.narrate([
        "Corvin buckles the sword back on, and stands up a",
        "little straighter than he has stood all year."])
    return c


def _cor5_offer():
    """The form, offered: yes if the party can pay, and Corvin pleased."""
    yes = R.if_then(R.condition_script("$gameParty.gold() >= %d" % FEE),
                    _cor5_curse(),
                    S.say("Miss Fettle", ["Thirty crowns, I'm",
                                          "afraid. The form's free."]))
    no = S.say("Corvin", ["...Another time."])
    return R.choice_block(["Have it cursed (%dcr)" % FEE, "Not today"],
                          [yes, no])


def _cor5_appraisal():
    c = S.narrate([
        "Corvin unbuckles the black sword and lays it on her",
        "bench, the way a man lays down a confession."])
    c += S.say("Corvin", ["Appraise it. Tell me what is on it."])
    c += S.say("Miss Fettle", ["Oh! Oh, may I - the",
                               "handle -"])
    c += S.say("Corvin", ["Yes."])
    c += S.narrate([
        "She has the handle off it in a trice. Corvin looks at",
        "the ceiling while she does, which has nothing on it."])
    c += S.say("Miss Fettle", ["Oh, look at that. Oh, the",
                               "TANG. Somebody loved this,",
                               "once."])
    c += [S.blush()]
    c += S.narrate(["She is some minutes with the tang."])
    c += S.say("Corvin", ["The curse."])
    c += S.say("Miss Fettle", ["The what? There's no",
                               "curse on this. Not a trace."])
    c += S.say("Miss Fettle", ["It's a very good sword",
                               "in very poor condition. You've been",
                               "sitting in corners with it."])
    c += S.say("Miss Fettle", ["There's a name on the",
                               "tang, in letters nobody's used for a",
                               "while. I'd not like to try it aloud."])
    c += S.narrate([
        "Corvin is quiet for a long time. Then, carefully, as if",
        "asking the price of something in a shop that might be",
        "too good for him:"])
    c += S.say("Corvin", ["How much would a curse cost? To",
                          "have one put on."])
    c += S.say("Miss Fettle", ["Oh, not much. They're",
                               "mostly paperwork. There's a form."])
    c += S.narrate([
        "From a drawer she takes FORM C-1: APPLICATION FOR A",
        "CURSE (ELECTIVE), in triplicate, and a pen."])
    c += [S.trope(), R.control_switch(db.SW_COR5_DONE, True)]
    c += S.companion_story(db.CORVIN)
    c += _cor5_offer()
    return c


def _cor5_counter():
    """After the appraisal, with Corvin: the curse on, or off."""
    cursed = S.say("Miss Fettle", ["Still cursed? Lovely.",
                                   "Want it off? No charge."])
    cursed += R.choice_block(
        ["Take it off", "Leave it"],
        [[_cor5_state(False), R.play_se("Recovery", 70)] + S.narrate([
            "She relights the candle. It comes off with no fuss at",
            "all, which Corvin finds a little disappointing."]),
         S.say("Corvin", ["Leave it."])])
    clean = S.say("Miss Fettle", ["Back for another? It",
                                  "wears off, the economy one."])
    clean += _cor5_offer()
    return R.if_then(R.condition_script(
        "$gameActors.actor(%d).isStateAffected(%d)" % (db.CORVIN,
                                                       db.ST_CURSED)),
        cursed, clean)


def fettle_pages(last):
    """Two pages for Miss Fettle (Map 62, event 7), whose ladder is one self
    switch: the appraisal and the curse counter with Corvin, and afterwards
    for everybody."""
    a_cor = {"selfSwitchValid": True, "selfSwitchCh": "A",
             "actorValid": True, "actorId": db.CORVIN}
    cmds = R.if_then(R.condition_switch(db.SW_COR5_DONE), _cor5_counter(),
                     _cor5_appraisal())
    page = R.page(cmds, conditions=a_cor)
    after = copy.deepcopy(last)
    after["list"] = after["list"][:-1] + S.narrate([
        "Pinned over her bench, a form C-1, stamped, and a",
        "drawing of a tang, very lovingly done."]) + after["list"][-1:]
    after["conditions"] = R.page([], conditions={
        "selfSwitchValid": True, "selfSwitchCh": "A",
        "switch1Valid": True, "switch1Id": db.SW_COR5_DONE})["conditions"]
    return [after, dict(copy.deepcopy(last), list=page["list"],
                        conditions=page["conditions"])]


# ============================================================== COR-1 ====

def _cor1_corvin(**more):
    return dict({"actorValid": True, "actorId": db.CORVIN}, **more)


def _cor1_plus(page, lines, conditions):
    """`page` as it was, with narration after it, on new conditions."""
    return _cor1_dressed(page, page["list"][:-1] + S.narrate(lines),
                         conditions)


def _cor1_dressed(last, commands, conditions):
    """A new page in `last`'s dress, with its own commands and conditions."""
    page = R.page(commands, conditions=conditions)
    return dict(copy.deepcopy(last), list=page["list"],
                conditions=page["conditions"])


# ------------------------------------------------------------- the Roll ----
def _cor1_found():
    c = S.narrate([
        "Corvin reads down the Roll again, slowly, the way a man",
        "reads a list of the dead. There are no dead on it. He",
        "stops at the one name without a tick."])
    c += S.say("Corvin", ["That is me."])
    c += S.narrate([
        "Two hundred and six people stood on a hill in the rain,",
        "and counted. When they got to him they wrote down where",
        "he was. And then they wrote to him."])
    c += S.say("Corvin", ["I was in a corner of the Slain",
                          "Wyvern. Being away. On purpose."])
    c += S.say("Corvin", ["They counted me anyway."])
    c += S.narrate([
        "He stands there for some time. Then he looks round at the",
        "door, as if he could see through it and up the street, to",
        "a new front door with knitting going on behind it."])
    c += S.say("Corvin", ["...Today, then."])
    c += [R.control_switch(db.SW_COR1_ON, True)]
    return c


def roll_pages(page0):
    """The Roll (Map 53, event 7), which has one page and no ladder. With
    Corvin the first read is that page exactly, and marks it read (self
    switch B, cosmetic: the quest is global); the second is his name."""
    body = page0["list"][:-1]
    first = _cor1_dressed(page0, body + [R.self_switch("B", True)],
                          _cor1_corvin())
    again = R.if_then(
        R.condition_switch(db.SW_COR1_ON), S.narrate([
            "Corvin does not read it again. He knows where he is on it."]),
        _cor1_found())
    second = _cor1_dressed(page0, body + again,
                           _cor1_corvin(selfSwitchValid=True,
                                        selfSwitchCh="B"))
    return [first, second]


# ------------------------------------------------------------- the door ----
def door_pages(page0):
    """Mrs Ash's door (Map 52, event 3), after Corvin's two refusals: with
    the Roll read, he goes in. `page0` is the door's own page, whose commands
    are the way in."""
    knock = S.narrate([
        "Corvin stops on the path, the way he always stops, and",
        "looks at the new front door for a long moment."])
    knock += S.say("Corvin", ["Not -"])
    knock += S.narrate([
        "He does not finish it. He goes up the path and knocks on",
        "his mother's door, like a visitor."])
    knock += [R.play_se("Knock"), R.wait(40)]
    knock += S.narrate([
        "From inside, over a clicking of needles:",
        "",
        "\"It's open, dear! It's always open!\""])
    knock += R.script([
        "$gameSelfSwitches.setValue([%d, 2, 'A'], true);" % MAP_ASHCOMBE_IN])
    body = R.if_then(R.condition_switch(db.SW_COR1_HOME, False), knock)
    return [_cor1_dressed(page0, body + page0["list"][:-1],
                          _cor1_corvin(switch1Valid=True,
                                       switch1Id=db.SW_COR1_ON))]


# ------------------------------------------------------------ Mrs Ash ----
def _cor1_home():
    c = S.narrate([
        "A kitchen so new that the paint still smells of it, with",
        "a big window over the lake. A woman at the table is",
        "knitting something long. She looks up, and for the first",
        "time in eleven years the needles stop."])
    c += S.say("Mrs Ash", ["Oh! There you are, love."])
    c += S.say("Mrs Ash", ["Mind the step. It's new. It's all",
                           "new. Isn't it lovely?"])
    c += S.say("Corvin", ["Mother."])
    c += S.say("Corvin", ["I have come back. To what is left."])
    c += S.say("Mrs Ash", ["Well, it's all left, love. It's",
                           "just up the hill a bit. Sit down,",
                           "I'll put the kettle on. It's a new",
                           "kettle."])
    c += S.narrate([
        "Corvin sits down at his mother's table in his black coat,",
        "with his black sword across his knees, and is given a cup",
        "of tea."])
    c += S.say("Mrs Ash", ["It was a Tuesday. We all went up",
                           "the hill with the kettles, and by",
                           "teatime we'd decided to build it",
                           "again, only better."])
    c += S.say("Mrs Ash", ["You were counted, mind. You're on",
                           "the Roll. Away. So I wrote to you."])
    c += S.say("Corvin", ["Wednesdays and Saturdays."])
    c += S.say("Mrs Ash", ["And you wrote the once. To the",
                           "Ruins of Ashcombe. Mrs Dimmock",
                           "brought it round."])
    c += S.say("Mrs Ash", ["So I wrote back. As the Ruins.",
                           "I thought you'd like that."])
    c += S.say("Corvin", ["...I did like it."])
    c += S.narrate(["He says it to his tea."])
    c += S.say("Mrs Ash", ["Your room's upstairs. It's bigger",
                           "now, and it's got the light. It's a",
                           "study at the minute. Go and look,",
                           "love."])
    c += S.narrate(["The needles start again."])
    c += [S.trope(), R.control_switch(db.SW_COR1_HOME, True)]
    return c


def _cor1_ash_after():
    """Mrs Ash with Corvin, once he is home: where the quest has got to."""
    done = S.say("Mrs Ash", ["More tea, love? It's a new pot."])
    done += S.narrate([
        "Corvin has the scarf on, in the kitchen, by the range. It",
        "is very warm in the kitchen. He keeps it on."])
    asked = S.say("Mrs Ash", ["Saturday! I'll be in the front",
                              "row. Knitting."])
    upstairs = S.say("Mrs Ash", ["Go on up, love. It's got the",
                                 "light."])
    return R.if_then(
        R.condition_switch(db.SW_COR1_DONE), done,
        R.if_then(R.condition_item(db.IT_INVITATION), asked, upstairs))


def mrs_ash_pages(last):
    """Two pages for Mrs Ash (Map 53, event 2), below her one-self-switch
    ladder: afterwards for everybody, and Corvin at home."""
    after = _cor1_plus(last, [
        "She has started another one already. It is the same",
        "colour, and it is already quite long."],
        {"selfSwitchValid": True, "selfSwitchCh": "A",
         "switch1Valid": True, "switch1Id": db.SW_COR1_DONE})
    cmds = R.if_then(R.condition_switch(db.SW_COR1_HOME), _cor1_ash_after(),
                     _cor1_home())
    home = _cor1_dressed(last, cmds, _cor1_corvin(
        selfSwitchValid=True, selfSwitchCh="A",
        switch1Valid=True, switch1Id=db.SW_COR1_ON))
    return [after, home]


# ------------------------------------------------------------ the study ----
def _cor1_desk():
    c = S.narrate([
        "A writing desk in the best of the light, with the papers",
        "of the FLOOD DINNER COMMITTEE on it in neat heaps.",
        "Hon. Sec.: Mrs Ash."])
    c += S.narrate([
        "Over it, a pigeonhole marked C. In it are eleven",
        "invitations, one for every year, in her hand, all of them",
        "addressed to the Slain Wyvern. Not one has a stamp."])
    return c


def _cor1_take():
    c = S.narrate(["Corvin takes out the top one, and reads it."])
    c += S.narrate([
        "THE FLOOD DINNER COMMITTEE requests the pleasure of",
        "MR C. ASH as Speaker. Saturday. Soup, a fish, a pudding."])
    c += S.narrate([
        "And at the bottom, in pencil:",
        "",
        "  I didn't post it, love. You'd only have said not today."])
    c += S.say("Corvin", ["...I would have."])
    c += S.narrate(["He folds it into his coat."])
    c += [R.gain_item(db.IT_INVITATION)]
    return c


def _cor1_marks():
    return S.narrate([
        "Pencil marks up the new wall by the window, with ages by",
        "them: C., 6. C., 9. C., 12. C., 16. C., 19."]) + S.narrate([
        "The old ones went under with the old wall. These have been",
        "put back from memory, and every one of them is a little",
        "taller than a boy would have been."])


def study_events(first_id):
    """Four events for Map 53, appended after everything else so no id
    moves: the study's door in the kitchen, its stair down, the desk and the
    height marks. Each is nothing at all until Corvin has been home."""
    blank = R.page([], img=R.image(""), trigger=0, priority=0, through=True)
    home = {"switch1Valid": True, "switch1Id": db.SW_COR1_HOME}
    done = {"switch1Valid": True, "switch1Id": db.SW_COR1_DONE}
    x1, y1, x2, y2, door_x = STUDY
    wall = dict(img=R.image(""), trigger=0, priority=1, direction_fix=True)
    evs = []

    door = R.page(S.door_page(MAP_ASHCOMBE_IN, door_x, y2, 8),
                  img=R.image("!Door1", 0, direction=2), trigger=1,
                  priority=1, conditions=home)
    evs.append(R.event(first_id, "Study Door", *STUDY_DOOR,
                       [copy.deepcopy(blank), door]))

    out = S.exit_tile(first_id + 1, "Study Stair", door_x, y2 + 2,
                      MAP_ASHCOMBE_IN, STUDY_DOOR[0], STUDY_DOOR[1] + 1)
    stair = dict(out["pages"][0], conditions=R.page(
        [], conditions=home)["conditions"])
    evs.append(dict(out, pages=[copy.deepcopy(blank), stair]))

    taken = R.if_then(
        R.condition_item(db.IT_INVITATION),
        S.narrate(["The top of the pile is in Corvin's coat."]),
        _cor1_take())
    desk_done = _cor1_desk() + S.narrate([
        "Ten invitations, now. The eleventh was answered."])
    evs.append(R.event(first_id + 2, "The Committee's Desk", *STUDY_DESK, [
        copy.deepcopy(blank),
        R.page(_cor1_desk(), conditions=home, **wall),
        R.page(desk_done, conditions=done, **wall),
        R.page(_cor1_desk() + R.if_then(
            R.condition_switch(db.SW_COR1_DONE), S.narrate([
                "Ten invitations, now. Corvin looks at the gap where the",
                "eleventh was, and is pleased with it."]), taken),
            conditions=_cor1_corvin(**home), **wall)]))

    stood = S.narrate([
        "Corvin stands against the wall, under the last mark. It",
        "is exactly the top of his head. She drew where he would",
        "be."])
    evs.append(R.event(first_id + 3, "The Height Marks", *STUDY_MARKS, [
        copy.deepcopy(blank),
        R.page(_cor1_marks(), conditions=home, **wall),
        R.page(_cor1_marks() + stood, conditions=_cor1_corvin(**home),
               **wall)]))
    return evs


# ------------------------------------------------- the notice, the menus ----
def _cor1_dinner():
    c = [R.fadeout_screen(), R.play_se("Bell1"), R.wait(30)]
    c += S.narrate([
        "Saturday. The church hall, with the old bell rung for six",
        "exactly, two hundred and six people, and soup, a fish and",
        "a pudding."])
    c += S.narrate([
        "Mr Weir introduces the speaker at some length, and mostly",
        "about culverts. Then he sits down, and Corvin stands up."])
    c += S.say("Corvin", ["I was not here, on the day of the",
                          "water."])
    c += S.say("Corvin", ["I was in the corner of an inn,",
                          "eight miles off."])
    c += S.narrate(["From the back, kindly: \"By the ROAD.\""])
    c += S.say("Corvin", ["By the road."])
    c += S.narrate([
        "A laugh goes round the hall. Corvin waits for it to stop.",
        "He has a very good wait. He has been practising it for",
        "eleven years."])
    c += S.say("Corvin", ["I took the name of a place I",
                          "thought was gone, and I have carried",
                          "it about in corners."])
    c += S.say("Corvin", ["It was not gone. It went up the",
                          "hill, and built the drains, and wrote",
                          "to me."])
    c += S.say("Corvin", ["So I have brought the name back.",
                          "You may as well have it. You were",
                          "using it."])
    c += S.narrate([
        "There is a silence of exactly the right length. Then two",
        "hundred and six people stand up at once, Mr Weir is in",
        "tears, and somebody rings the bell, which is not allowed",
        "indoors."])
    c += [R.play_se("Applause1"), R.wait(60)]
    c += S.say("Corvin", ["To the water."])
    c += S.narrate(["Two hundred and six glasses go up."])
    c += S.say("Corvin", ["Which was very good about it."])
    c += S.narrate([
        "In the front row, on the last word, Mrs Ash casts off the",
        "last stitch, and stands, and holds the knitting up. It",
        "goes most of the way down the aisle."])
    c += S.say("Mrs Ash", ["There. For somebody who feels",
                           "the cold and won't say so."])
    c += S.narrate([
        "It is a scarf. It is very long, and very warm, and bright",
        "yellow, the yellow of the new roofs - which is the wrong",
        "colour for everything Corvin owns."])
    c += S.say("Corvin", ["...It is the wrong colour."])
    c += S.say("Mrs Ash", ["I know, love. If I'd done it in",
                           "black, nobody'd ever see you in it."])
    c += S.narrate([
        "He puts it on. He wears it home, and he wears it, as it",
        "turns out, everywhere."])
    c += [{"code": 126, "indent": 0,
           "parameters": [db.IT_INVITATION, 1, 0, 1]},
          R.gain_armor(db.AR_SCARF), R.control_switch(db.SW_COR1_DONE, True)]
    c += S.companion_story(db.CORVIN)
    c += [R.fadein_screen()]
    c += S.got(["Corvin's scarf - the wrong colour - is in the pack."])
    return c


def notice_pages(page0):
    """The Flood Dinner's notice (Map 52, event 9), which has one page and no
    ladder: afterwards for everybody, and with Corvin and the invitation,
    the speaker confirmed and the Dinner."""
    after = _cor1_plus(page0, [
        "Pasted over TO BE CONFIRMED, in a careful hand:",
        "C. ASH. (CONFIRMED.) And under it, in pencil: Mr Weir has",
        "kindly offered. Next year."],
        {"switch1Valid": True, "switch1Id": db.SW_COR1_DONE})
    yes = S.say("Corvin", ["Confirmed."])
    yes += S.narrate([
        "He writes it in, over TO BE CONFIRMED, in a hand that has",
        "not written its own name in a while."])
    yes += _cor1_dinner()
    no = S.say("Corvin", ["...Saturday."])
    cmds = page0["list"][:-1] + R.choice_block(
        ["Confirm the speaker", "Not yet"], [yes, no])
    return [after, _cor1_dressed(page0, cmds, _cor1_corvin(
        itemValid=True, itemId=db.IT_INVITATION))]


def menus_pages(page0):
    """The menus in the museum (Map 53, event 8) afterwards, for everybody."""
    return [_cor1_plus(page0, [
        "Pinned on top, this year's. At the foot: C. Ash, on the",
        "water. Somebody has written under it in pencil: VERY GOOD."],
        {"switch1Valid": True, "switch1Id": db.SW_COR1_DONE})]


# ============================================================== COR-2 ====
DROWNED_W, DROWNED_H = 22, 15
MUD = K.SAND                        # `K.SAND` is Outside_A2's `Dirt`
WET = K.A(31)                       # `Soil`, an overlay: Dirt under it is mud
MOSS = K.A(39)                      # `Moss`, an overlay, on the old floors
LAKEWATER = K.A(8)                  # Outside_A1 `Water C (Dirt)`
OLD_STREET = K.a5(28)               # `Cobblestones A (Ruins)`
OLD_FLOOR = K.a5(38)                # `Cobblestones G (Ruins)`
DOORSTEP = K.a5(71)                 # `Stairs (Ruins)`: one step, on its own
PUB_SIGN = K.sf_tile("Outside_B", "Shop Sign (Pub)")
RUBBLE_MOSS = K.sf_tile("Outside_C", "Rubble B (Moss)")
RUBBLE = K.sf_tile("Outside_C", "Rubble")
STUMP_WALL = K.sf_tile("Outside_C", "Broken Stone Pillar B (Moss)")
WEEDS = [K.sf_tile("Outside_B", n) for n in
         ("Dead Grass B", "Fern", "Stump (Moss)", "Rocks", "Fallen Log")]
LILY = K.sf_tile("Outside_B", "Lotus Pads A")

STREET_ROWS = (7, 8)
#              x1 y1 x2 y2: the floor of what each was
ANCHOR_PLOT = (3, 3, 6, 5)
ASH_PLOT = (9, 3, 11, 5)
SCHOOL_PLOT = (14, 3, 18, 5)
ANCHOR_SIGN = (5, 6)
STEP_AT = (10, 6)
STRONGBOX = (16, 4)
CHURCH_WATER = (20, 7)              # the street runs on into the lake
DROWNED_ARRIVE = (10, 13)


def drowned_street_map():
    """Old Ashcombe, with the lake let down off it for sluice week: one
    street of cobbles in a bed of mud, the lake still standing round three
    sides, and three plots where the Anchor, the Ashes' house and the
    schoolroom were - a sign, a doorstep and a strongbox. The slope at the
    south is the way back up to the shore."""
    w, h = DROWNED_W, DROWNED_H
    g = K.Canvas(w, h)
    g.fill(0, 0, w - 1, h - 1, 0, MUD)
    g.fill(0, 0, w - 1, 1, 0, LAKEWATER)
    g.fill(0, 0, 1, 10, 0, LAKEWATER)
    g.fill(w - 2, 0, w - 1, 10, 0, LAKEWATER)
    for x, y in [(2, 10), (3, 2), (19, 2), (19, 10), (4, 11), (5, 11),
                 (15, 11), (16, 11), (16, 12)]:
        g.set(x, y, 0, LAKEWATER)
    g.fill(2, STREET_ROWS[0], w - 3, STREET_ROWS[1], 0, OLD_STREET)
    for x1, y1, x2, y2 in (ANCHOR_PLOT, ASH_PLOT, SCHOOL_PLOT):
        g.fill(x1, y1, x2, y2, 0, OLD_FLOOR)
    g.set(*STEP_AT, 0, DOORSTEP)
    # Layer 1 is the lake's leavings: the bed wet through, and moss on the
    # floors it lay longest over.
    for y in range(h):
        for x in range(w):
            if g.get(x, y, 0) == MUD:
                g.set(x, y, 1, WET)
    for x, y in [(4, 3), (5, 4), (10, 4), (15, 3), (16, 5), (17, 4)]:
        g.set(x, y, 1, MOSS)
    g.autotile(0)
    g.autotile(1)

    # What is left of the walls, at the corners and along the backs.
    for x, y in [(2, 3), (2, 5), (7, 3), (7, 5), (4, 2), (8, 4), (12, 3),
                 (12, 5), (13, 4), (15, 2), (17, 2), (19, 3), (19, 5)]:
        g.set(x, y, 2, STUMP_WALL)
    for x, y in [(3, 6), (6, 6), (9, 6), (11, 6), (14, 6), (18, 6), (5, 2),
                 (10, 2)]:
        g.set(x, y, 2, RUBBLE_MOSS if (x + y) % 2 else RUBBLE)
    g.set(*ANCHOR_SIGN, 3, PUB_SIGN)

    # The lake bed south of the street, and its puddles.
    for i, (x, y) in enumerate([(3, 10), (7, 12), (13, 10), (18, 12),
                                (6, 9), (15, 9), (2, 12), (19, 13),
                                (13, 13), (8, 10)]):
        g.set(x, y, 3, WEEDS[i % len(WEEDS)])
    for x, y in [(4, 11), (16, 12)]:
        g.set(x, y, 3, LILY)

    m = K.new_map(w, h, K.TS_OUTSIDE, name="Old Ashcombe", bgm="")
    m["bgs"] = {"name": "Drips", "pan": 0, "pitch": 100, "volume": 60}
    m["data"] = g.data
    m["events"] = [None] + _cor2_events()
    return m


def _cor2_sign():
    c = S.narrate([
        "A pub sign, face up in the mud and propped against what is",
        "left of a wall: THE ANCHOR, with an anchor on it."])
    c += S.narrate([
        "It hung over a pub for a hundred years. It has been under",
        "a lake for eleven. It is the first time it has been any",
        "use."])
    return c


def _cor2_step():
    c = S.narrate([
        "A doorstep. Only the step, at the edge of the old street,",
        "with nothing behind it now but mud and a square of stones",
        "where a house was."])
    c += S.narrate([
        "Corvin sits down on it. He does not say anything for a",
        "long time, and nor does anybody else."])
    c += S.say("Corvin", ["I used to sit here. Waiting for",
                          "something to happen."])
    c += S.say("Corvin", ["Then it did. And I was in the",
                          "Slain Wyvern, waiting."])
    c += [R.wait(60)]
    c += S.narrate([
        "The lake drips off the stones. Up the hill, a long way",
        "off, a bell rings for somebody's dinner."])
    c += [R.play_se("Bell1", volume=40), R.wait(90)]
    c += S.narrate([
        "When at last he gets up, there are letters cut into the",
        "step where he was sitting: the old letters, the ones on",
        "the tang of his sword. And under them, in plain capitals,",
        "for visitors:"])
    c += S.narrate(["", "                  MIND THE STEP"])
    c += S.say("Corvin", ["My grandfather cut that. He made",
                          "the sword as well."])
    c += S.say("Corvin", ["It stood here forty years, holding",
                          "the door open. That is its name."])
    c += S.narrate([
        "He puts his hand on the hilt, very lightly, the way you",
        "would introduce yourself to somebody you had known all",
        "your life."])
    c += [S.trope(), R.control_switch(db.SW_COR2_STEP, True)]
    c += S.narrate([
        "Next door, in what was the schoolroom, something square",
        "and iron is sitting in the mud."])
    return c


def _cor2_card():
    c = [R.play_se("Chest1")]
    c += S.narrate([
        "The strongbox is rusted shut. Corvin opens it with the",
        "black sword, which turns out to be very good at it."])
    c += S.narrate([
        "Inside, dry, wrapped in oilcloth: a report for every",
        "child old Ashcombe ever had, in the schoolmistress's",
        "careful hand. She kept everybody's."])
    c += S.narrate([
        "Corvin's is near the top. It was the last year.",
        "",
        "ASHCOMBE SCHOOL. Pupil: Corvin - the surname has run."])
    c += S.narrate([
        "Arithmetic: looks out of the window at it.",
        "Composition: writes, darkly. Will not read it out.",
        "Conduct: sits in the corner. Asked to sit elsewhere,",
        "sits in a different corner."])
    c += S.narrate([
        "General: Corvin could do anything he put his mind to,",
        "and has put it to waiting. He will go far, if he ever",
        "gets up."])
    c += S.narrate([
        "It is very quiet in the drowned street. Then Corvin",
        "laughs - once, out loud. Nobody in the party has heard",
        "him do it before."])
    c += S.say("Corvin", ["It is a fair report."])
    c += S.narrate(["He puts it in his coat, next to the scarf."])
    c += [R.gain_item(db.IT_REPORT_CARD),
          R.control_switch(db.SW_COR2_DONE, True)]
    c += S.companion_story(db.CORVIN)
    return c


def _cor2_events():
    corvin = _cor1_corvin()
    wall = dict(img=R.image(""), trigger=0, priority=1, direction_fix=True)
    evs = []
    for i in range(2):
        evs.append(S.exit_tile(i + 1, "The Way Up", DROWNED_ARRIVE[0] + i,
                               DROWNED_H - 1, MAP_WORLD, *LAKE_SHORE_STEP))

    sign = _cor2_sign()
    evs.append(R.event(3, "The Anchor", *ANCHOR_SIGN, [
        R.page(sign, **wall),
        R.page(sign + S.say("Corvin", ["I was not allowed in. I sat",
                                       "outside it and waited."]),
               conditions=corvin, **wall)]))

    step = S.narrate([
        "A doorstep, at the edge of the old street, with nothing",
        "behind it."])
    named = S.narrate([
        "The doorstep. Cut into it, in the old letters and then in",
        "plain capitals: MIND THE STEP."])
    evs.append(R.event(4, "The Doorstep", *STEP_AT, [
        R.page(step, **wall),
        R.page(R.if_then(R.condition_switch(db.SW_COR2_STEP), named,
                         _cor2_step()), conditions=corvin, **wall)]))

    box = dict(wall, img=R.image("!Chest", 5, direction=2))   # the iron one
    shut = S.narrate([
        "A strongbox, in the mud of what was the schoolroom, rusted",
        "shut."])
    waiting = shut + S.narrate([
        "Corvin does not look at it. He is looking along the street",
        "for something else."])
    opened = S.narrate([
        "The strongbox, open: everybody's reports, back in their",
        "oilcloth. One fewer than there were."])
    evs.append(R.event(5, "The Strongbox", *STRONGBOX, [
        R.page(shut, **box),
        R.page(R.if_then(R.condition_switch(db.SW_COR2_DONE), opened,
                         R.if_then(R.condition_switch(db.SW_COR2_STEP),
                                   _cor2_card(), waiting)),
               conditions=corvin, **box)]))

    church = S.narrate([
        "The street goes on into the water. Just under the surface,",
        "a green roof: the old church, up to its eaves. You could",
        "skim a stone on to it."])
    evs.append(R.event(6, "The Street's End", *CHURCH_WATER,
                       [R.page(church, **wall)]))
    return evs


def lake_pages(last):
    """Two pages for Ashcombe Lake (Map 8, event 55), below its one-self-
    switch ladder: afterwards for everybody, and with Corvin, once COR-1 is
    done, sluice week - the lake is let down in the week of the Flood Dinner,
    and old Ashcombe is up for air."""
    after = _cor1_plus(last, [
        "Somewhere under it there is a doorstep with a sword's",
        "name cut into it, and a strongbox one report lighter."],
        {"selfSwitchValid": True, "selfSwitchCh": "A",
         "switch1Valid": True, "switch1Id": db.SW_COR2_DONE})
    week = S.narrate([
        "Ashcombe Lake - and it is not well up. It is the week.",
        "The sluices are open for the culverts, as they are every",
        "year in the week of the Flood Dinner, and the water has",
        "gone down off the old street like a tide that is bored."])
    week += S.narrate([
        "At the bottom of a slope of wet mud below the shore,",
        "there is a street."])
    week += S.narrate(["Corvin looks at it for a long time."])
    week += R.choice_block(["Walk down", "Not now"], [
        [R.transfer(MAP_DROWNED_STREET, *DROWNED_ARRIVE, 8, 0)],
        S.say("Corvin", ["...In a minute."])])
    cmds = R.if_then(R.condition_switch(db.SW_COR2_DONE),
                     after["list"][:-1], week)
    return [after, _cor1_dressed(last, cmds, _cor1_corvin(
        selfSwitchValid=True, selfSwitchCh="A",
        switch1Valid=True, switch1Id=db.SW_COR1_DONE))]


def weir_pages(last):
    """Mr Weir (Map 53, event 5) afterwards, below his one-self-switch
    ladder, for everybody."""
    return [_cor1_plus(last, [
        "Sluice week went off splendidly, he tells you. Somebody",
        "sat on a doorstep down there for an hour, and the",
        "culverts did not mind in the least."],
        {"selfSwitchValid": True, "selfSwitchCh": "A",
         "switch1Valid": True, "switch1Id": db.SW_COR2_DONE})]


def build():
    R.save_map(MAP_DROWNED_STREET, drowned_street_map())


# ============================================================== COR-3 ====
# The Rivals' Retreat (`QUESTS.md` E10). An inn on a moor where doomed rivals
# brood professionally; a rota for the darkest corner; a newsletter; a league
# table on which Corvin, a member who has never attended, is seventeenth.
#
# * **The start is the league table** (Map 49 event 8), which has no ladder
#   and no published reaction shot: with Corvin, its own page, and then he
#   takes out the fifth pin and reads the rest. Seventeenth, of seventeen,
#   behind Blackwood, who is new. He takes it very hard, and sits down.
# * **The fix is a meeting**, because points are only scored at meetings and
#   he has sent apologies to a hundred and twelve of them. Crake convenes it
#   on his second look with Corvin (event 2, below his one-self-switch
#   ladder), Rook reviews the points, and everybody is lovely about it
#   without once using the word. Eleven years in one corner of the Slain
#   Wyvern is not a category. It is now. Second, behind the scar.
# * **His chair is kept**, the newsletter has always said - and it is not a
#   corner. It is a stool at the empty table in the middle of the room, in
#   the light, which nobody but a tinker has ever sat at. He sits at it, and
#   stays for his pie.
# * **Afterwards for everybody**: Crake, the table re-ruled, the newsletter's
#   next issue, and the stool with no dust on it.
def _cor3_seventeenth():
    c = S.narrate([
        "Corvin looks at the fifth pin for a long moment. Then he",
        "takes it out, and lifts the rota, and reads down."])
    c += S.narrate([
        "   5. K. BLACKWOOD ... 12   (keen)",
        "   6-16. members by post, in order of their last letter",
        "   17. C. ASH ............ 0   (no meetings attended)"])
    c += S.say("Corvin", ["Seventeenth."])
    c += S.say("Corvin", ["Of seventeen. Behind",
                          "Blackwood. Blackwood is NEW."])
    c += S.narrate([
        "He puts the pin back, very carefully, and sits down at",
        "the nearest table, which is the one in the middle of the",
        "room, in the light. Nobody in the Sable Hart says a word.",
        "Across the room, Crake opens his book."])
    c += [S.trope(), R.control_switch(db.SW_COR3_ON, True)]
    return c


def league_pages(page0):
    """Pages 2-3 of the league table (Map 49, event 8), which has no ladder:
    with Corvin, its own page and then the rest of it; afterwards, its own
    page and the table re-ruled, for everybody."""
    own = page0["list"][:-1]
    again = S.narrate(["Corvin does not look at the bottom of it again."])
    corvin = own + R.if_then(R.condition_switch(db.SW_COR3_ON), again,
                             _cor3_seventeenth())
    after = own + S.narrate([
        "The rota has been moved up an inch. Under it, new, in red:",
        "   2. C. ASH ............ 39   (one corner, eleven years)",
        "   5. T. ROOK ........... 35   (by his own request)"])
    return [
        _cor1_dressed(page0, corvin, _cor1_corvin()),
        _cor1_dressed(page0, after, {"switch1Valid": True,
                                     "switch1Id": db.SW_COR3_DONE}),
    ]


def _cor3_meeting():
    c = S.say("Crake", ["Mr Ash. You've seen the",
                        "table."])
    c += S.say("Corvin", ["Seventeenth."])
    c += S.say("Crake", ["Points are scored at",
                         "meetings, I'm afraid, and you have",
                         "sent apologies to a hundred and",
                         "twelve of them. Beautifully."])
    c += S.say("Crake", ["Shall we have one? Now.",
                         "Quorum is two. We are five, and",
                         "a member."])
    c += [R.play_se("Bell1", 70)]
    c += S.narrate([
        "He rings a little bell. The four corners and the fire",
        "come into the middle of the room, which none of them has",
        "stood in for years, and stand round Corvin's table."])
    c += S.say("Rook", ["Review of points. Ash, C.",
                        "A vow?"])
    c += S.say("Corvin", ["A fortune-teller said I was",
                          "the rival of a great hero. I paid",
                          "twopence."])
    c += S.say("Rook", ["A vow you paid for. That's",
                        "binding. Two points."])
    c += S.say("Rook", ["A scar?"])
    c += S.say("Corvin", ["No."])
    c += S.say("Veyle", ["Don't ask about the scar."])
    c += S.narrate([
        "Nobody asks about the scar. Veyle looks, very briefly,",
        "disappointed."])
    c += S.say("Rook", ["Standing in the rain?"])
    c += S.say("Corvin", ["I sat in the corner of the",
                          "Slain Wyvern. For eleven years."])
    c += [R.wait(40)]
    c += S.say("Rook", ["...In ONE corner?"])
    c += S.say("Veyle", ["Out of turn?"])
    c += S.say("Corvin", ["There wasn't a rota."])
    c += S.say("Crake", ["Nobody has ever sat in one",
                         "corner for eleven years. Mr Rook,",
                         "is there a category?"])
    c += S.say("Rook", ["There is now."])
    c += S.say("Morrow", ["Front page."])
    c += S.say("Blackwood", ["Could I have that",
                             "category, one day? When I've got",
                             "a corner?"])
    c += S.narrate([
        "Rook does the sum twice, in the margin, and rules a new",
        "line in red. C. ASH, thirty-nine. Second, behind the",
        "scar. He moves himself down to fifth, and is visibly",
        "happier there."])
    c += S.say("Veyle", ["Have the dark corner. Go on.",
                         "Monday's only four days."])
    c += S.say("Crake", ["NOBODY out of turn,",
                         "however rainy."])
    c += S.say("Crake", ["Besides, his chair is kept.",
                         "It always has been."])
    c += S.narrate([
        "It is the stool he is sitting on: in the middle of the",
        "room, in the light, where nobody broods. Somebody has",
        "dusted it. It does not look as if it has been easy."])
    c += S.say("Corvin", ["...It's a very good chair."])
    c += S.narrate([
        "Mrs Garrow brings him a pie. He stays for it. Nobody uses",
        "the word for what this is, and nobody needs to."])
    c += [R.control_switch(db.SW_COR3_DONE, True)]
    c += S.companion_story(db.CORVIN)
    return c


def crake_pages(last):
    """Pages 3-4 for Crake (Map 49, event 2), in his own last page's dress:
    the meeting, with Corvin once he has read the table, below his ladder;
    afterwards, his last page and one line, for everybody."""
    known = {"selfSwitchValid": True, "selfSwitchCh": "A"}
    own = last["list"][:-1]
    after = own + S.say("Crake", ["Mr Ash attends now. Not",
                                  "every week. He sends apologies",
                                  "when he doesn't. We find it very",
                                  "reassuring."])
    return [
        _cor1_dressed(last, own + _cor3_meeting(), _cor1_corvin(
            switch1Valid=True, switch1Id=db.SW_COR3_ON, **known)),
        _cor1_dressed(last, after, dict(known, switch1Valid=True,
                                        switch1Id=db.SW_COR3_DONE)),
    ]


def newsletter_pages(page0):
    """Page 2 of the newsletter (Map 49, event 10): its own page and the
    next issue, for everybody."""
    return [_cor1_plus(page0, [
        "Issue one hundred and thirteen, stop press: PRESENT: C.",
        "ASH. A new category (one corner, eleven years). One",
        "stool dusted."], {"switch1Valid": True,
                           "switch1Id": db.SW_COR3_DONE})]


def middle_pages(page0):
    """Page 2 of the empty table (Map 49, event 11): one stool dusted, and
    with Corvin, him at it."""
    c = S.narrate([
        "A table in the middle of the room, in the light, with a",
        "stool at each end. One of them has been dusted, and has a",
        "card on it: KEPT. (C. ASH.)"])
    c += R.if_then(R.condition_actor_in_party(db.CORVIN), S.narrate([
        "Corvin sits on it for a minute, in the light, and does",
        "not brood at all."]))
    return [_cor1_dressed(page0, c, {"switch1Valid": True,
                                     "switch1Id": db.SW_COR3_DONE})]


# ============================================================== COR-4 ====
# Mother Selvidge (`QUESTS.md` E11). The fortune-teller who told him at
# nineteen that he was the rival of a great hero is still working the fairs,
# remembers nothing, and reads him again: a long life, a useful trade, and
# no destiny whatsoever. Again: the same. The third reading is the quest.
#
# * **It is the Fair's second look with Corvin** (Map 8 event 54, below its
#   one-self-switch ladder), and that switch is set only when she is paid -
#   so a party that never crossed her palm has never been to her booth, and
#   this waits until they have. Two crowns for the first reading, as for
#   anybody; the second and third are free, because her own second page
#   says "Same again? Keep your money."
# * **The third reading has no mysticism in it**: she says the rival thing
#   to about four young men a year, because it is the reading that makes
#   them stand up straight, and it has never once been wrong, in the sense
#   that they all went and did something. Nobody tells him he is nothing.
# * **Gives nothing.** He keeps the coat.
# * **Afterwards for everybody**: the fair's own second page, with a young
#   man in the queue standing up very straight.
def _cor4_readings():
    c = S.narrate([
        "Corvin stops in front of the little striped booth, and",
        "reads the sign, and stands there for some time."])
    c += S.say("Corvin", ["Eleven years ago. Two crowns.",
                          "You told me I was the rival of a",
                          "great hero."])
    c += S.say("Mother Selvidge", ["Did I, dear? I",
                                   "dare say I did. Cross my palm."])
    c += [R.lose_gold(2), R.play_se("Coin")]
    c += S.narrate([
        "She takes his hand, and looks at it for a long time, and",
        "then at him, for longer."])
    c += S.say("Mother Selvidge", ["A long life. A",
                                   "useful trade. Something with your",
                                   "hands. No destiny whatsoever."])
    c += S.say("Corvin", ["...Again."])
    c += S.narrate([
        "She shuffles, and cuts, and lays them out again, and does",
        "not charge him, and looks."])
    c += S.say("Mother Selvidge", ["A long life. A",
                                   "useful trade. No destiny. Same",
                                   "again, dear. Keep your money."])
    c += S.say("Corvin", ["Again."])
    c += [R.wait(40)]
    c += S.narrate([
        "This time she does not shuffle. She puts the cards down,",
        "and folds her hands on them, and looks at him the way",
        "your aunt would."])
    c += S.say("Mother Selvidge", ["Shall I tell you a",
                                   "thing, dear? The rival of a great",
                                   "hero. I say that to about four",
                                   "young men a year."])
    c += S.say("Mother Selvidge", ["Lads like you, at",
                                   "nineteen, sat in a heap. It's the",
                                   "reading that makes them stand up",
                                   "straight."])
    c += S.say("Mother Selvidge", ["And it has never once",
                                   "been wrong. They all went and did",
                                   "something."])
    c += S.say("Corvin", ["I sat in a corner. For eleven",
                          "years."])
    c += S.say("Mother Selvidge", ["And then you got up.",
                                   "Look at you. You're stood in a",
                                   "fair a long way from anywhere with",
                                   "your friends."])
    c += S.say("Mother Selvidge", ["Never wrong, dear.",
                                   "Ask anybody I've read."])
    c += S.narrate([
        "Corvin looks at the cards, and at the party, and at his",
        "long black coat. He thinks about taking it off."])
    c += S.narrate(["He keeps the coat. It is a very good coat."])
    c += [S.trope(), R.control_switch(db.SW_COR4_DONE, True)]
    c += S.companion_story(db.CORVIN)
    return c


def fair_pages(last):
    """Pages 3-4 of the Fair (Map 8, event 54), in its second page's dress:
    with Corvin, the tent and then the three readings, below its ladder;
    afterwards, the tent and a young man in the queue, for everybody."""
    known = {"selfSwitchValid": True, "selfSwitchCh": "A"}
    tent = S.narrate([
        "The fair in the big tent. Mother Selvidge is at",
        "the back, shuffling."])
    pay = R.if_then(R.condition_script("$gameParty.gold() >= 2"),
                    _cor4_readings(),
                    S.say("Mother Selvidge", ["Two crowns, dear. The",
                                              "cards don't do credit."]))
    visit = tent + R.choice_block(["Go to the fair", "Press on"], [pay, []])
    queue = tent + S.narrate([
        "In front of her booth a young man in a hat has just been",
        "told something, and is standing up very straight."])
    same = S.say("Mother Selvidge", ["Same again? It'll be the",
                                     "same again, dear. Keep your money."])
    after = queue + R.choice_block(["Go to the fair", "Press on"],
                                   [same, []])
    return [
        _cor1_dressed(last, visit, _cor1_corvin(**known)),
        _cor1_dressed(last, after, dict(known, switch1Valid=True,
                                        switch1Id=db.SW_COR4_DONE)),
    ]
