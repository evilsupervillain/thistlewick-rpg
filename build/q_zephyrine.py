"""Zephyrine Vance's companion quests - `COMPANIONS.md`, her section, and
`QUESTS.md` for the order they are built in.

Nothing here draws a map, and this module imports no place module: the place
modules call in here for pages.

ZEPH-5, The Lay-By (`QUESTS.md` A7)
-----------------------------------
Three hedge mages, nine years without a name, an igloo in a lay-by on the
west road. They are all excellent. Dunnock taught himself out of a book with
four pages missing, and is better than the Collegium at exactly those four
things; he teaches her one of them, badly, and it works.

* **It hangs off the Lay-By's world-map event** (`nomap.py`), whose two pages
  are a stop and its short version on self switch A. Page 3 needs A and
  Zephyrine, so she gets the association's first scene first, as anybody
  does; page 4 adds `SW_ZEPH5_DONE`. A party without her sees the lay-by as
  it was, forever.
* **Both pages ask before they start**, like every world-map site: a cell on
  the west road is walked over by people going somewhere else.
* **The skill is `SK_PAGE_23`**, in the free end of her block (46). It is
  Kindle worked out by a man who never saw the page: weaker, cheaper, and
  aimed at three enemies it has not been told about.
"""
import copy

import db
import mapkit as K
import rmmzdata as R
import story as S

STOP = "Look in"


def _stop(opening, scene):
    """The world map's idiom: say what is here, then ask."""
    return opening + R.choice_block(
        [STOP, "Press on"], [scene, S.narrate(["You press on."])])


def _the_page():
    """Page twenty-three. The whole of ZEPH-5."""
    c = S.narrate([
        "Three people round a folding table in the igloo,",
        "with the minutes. Miss Privet sees Zephyrine and",
        "puts her pen down."])
    c += S.say("Miss Privet", ["Oh. It's Vance."])
    c += S.say("Mrs Quickset", ["The one who set fire",
                                "to the Dean."])
    c += S.say("Dunnock", ["Collegium."])
    c += S.say("Zephyrine", ["Formerly."])
    c += S.say("Dunnock", ["We don't take Collegium."])
    c += S.say("Zephyrine", ["Neither does the Collegium."])
    c += S.narrate([
        "There is a pause, of the kind that is going into",
        "the minutes."])
    c += S.say("Miss Privet", ["Item two. Admission of a",
                               "member. Any objections?"])
    c += S.say("Dunnock", ["One."])
    c += S.say("Dunnock", ["Show us summat. Out of the",
                           "book. Not in here - it's an igloo."])
    c += S.narrate([
        "Outside, in the lay-by, Dunnock opens a book with",
        "a brown paper cover. Four pages have been torn out",
        "and replaced in pencil, in his hand."])
    c += S.say("Dunnock", ["Page twenty-three. Kindle."])
    c += S.say("Zephyrine", ["I know Kindle. I was the best",
                             "in my year at Kindle."])
    c += S.say("Dunnock", ["Not this one you weren't."])
    c += S.say("Dunnock", ["You don't aim it. You sort of",
                           "mean it, at everything, and it",
                           "sorts itself out."])
    c += S.say("Zephyrine", ["That is not how any of it works.",
                             "That is not how fire works."])
    c += S.say("Dunnock", ["Page was missing. Go on."])
    c += S.narrate([
        "Zephyrine sighs, means it at everything, and does",
        "not aim."])
    c += [R.play_se("Fire1"), R.wait(10), R.play_se("Fire2", pitch=110),
          R.wait(10), R.play_se("Fire1", pitch=90), R.wait(30)]
    c += S.narrate([
        "A gorse bush, a milestone and the lay-by's litter",
        "bin catch fire, all at once, neatly, and go out.",
        "Nobody is anywhere near any of them."])
    c += S.say("Zephyrine", ["...That should not have worked."])
    c += S.say("Dunnock", ["Page was missing."])
    c += S.say("Miss Privet", ["Objection withdrawn. Carried.",
                               "Item one?"])
    c += S.narrate([
        "Zephyrine proposes a name. It is a good name.",
        "It is carried forward, under nine years of other",
        "good names."])
    c += [R.learn_skill(db.ZEPH, db.SK_PAGE_23), R.play_me("Item")]
    c += S.got(["Zephyrine learned \\C[3]Page Twenty-Three\\C[0]."])
    c += [S.trope(), R.control_switch(db.SW_ZEPH5_DONE, True)]
    c += S.companion_story(db.ZEPH)
    return c


def _member():
    """Once she is a member. The minutes, as ever."""
    c = S.say("Miss Privet", ["Vance. Sit down, dear.",
                              "Item one, carried forward."])
    c += S.say("Dunnock", ["Page twenty-three holding up?"])
    c += S.say("Zephyrine", ["It should not be.",
                             "It is."])
    c += S.say("Dunnock", ["Aye. They do that."])
    return c


def lay_by_pages():
    """Pages 3 and 4 of the Lay-By's world-map event, in its dress:
    player-touch, below characters, walked through."""
    opening = S.narrate([
        "The igloo in the lay-by. Somebody inside says",
        "'Collegium' in the voice people use for weather."])
    again = S.narrate([
        "The igloo in the lay-by. There is a chair at the",
        "folding table now with nobody's coat on it."])
    seen = {"selfSwitchValid": True, "selfSwitchCh": "A",
            "actorValid": True, "actorId": db.ZEPH}
    kw = dict(img=R.image(""), trigger=1, priority=0, through=True)
    return [
        R.page(_stop(opening, _the_page()), conditions=seen, **kw),
        R.page(_stop(again, _member()),
               conditions=dict(seen, switch1Valid=True,
                               switch1Id=db.SW_ZEPH5_DONE), **kw),
    ]


# =============================================================== ZEPH-1 ==
# The Fines (`QUESTS.md` C1).
#
# She goes back to appeal, and there is no appeal, because there was no
# expulsion: it was drafted, initialled by the Dean and referred to the
# Registrar, who referred it to a committee that has not met since. So she has
# been on unpaid study leave for eleven years, in good standing, and owes
# eleven years of library fines - the largest number in the game.
#
# * **The occasion is a letter**, because she "drinks at the Gilded Turnip in
#   the manner of a person waiting for a letter" and her refusal at the
#   world-map door is a refusal nobody can talk her out of. The Library's
#   eleventh notice has come to her old table at the Turnip (Map 4, a new
#   event on the table, (12, 6), read from where she used to sit): the first
#   ten went to her pigeonhole at the Collegium, which was her last address;
#   the new Registrar's clerk looked her up. `SW_ZEPH1_ON`, and the notice is
#   item 53.
# * **The world-map doors** keep their three pages; page 4 (Zephyrine and the
#   notice) is her going in to appeal, and page 5 (Zephyrine, done) goes in
#   either way, with a line for each branch.
# * **The scene is Mr Pennock's**, the Registrar's clerk, a new event at the
#   east end of Prewitt's desk in the Library (Map 59, event 7), there from
#   the notice on - so nothing in the Library changes for a party without
#   her. All its state is global: a dismissed Zephyrine's file waits on the
#   desk.
# * **The choice is real, and both ends are respected.** Turn out the purse on
#   the Library desk - every crown the party has, which statute nine deems
#   paid in full, the only gold sink the design ever had that is funny - and
#   she is a member in good standing, with her robe and her name on the IN
#   and OUT board. Or file the draft, which only ever wanted filing, and be
#   expelled at last, properly, at her own request, for nothing: members of
#   the public are not fined. "Not today" keeps the file on the desk.
# * **Afterwards** is Pennock, Prewitt, the Register and the board, for
#   everybody; Gedge, with her, knows her and always did.

def _z1_paid_or_expelled(paid, expelled, indent=0):
    """Two bodies, chosen by which end of ZEPH-1 she took."""
    return R.if_then(R.condition_switch(db.SW_ZEPH1_PAID), paid, expelled,
                     indent=indent)


def letter_event(event_id, x, y):
    """Map 4, on Zephyrine's old table in the Turnip, read from where she
    used to sit. Nothing at all without her; the notice with her; and nothing
    again once it is read, because it is in her hat."""
    c = S.narrate([
        "Zephyrine's old table. Propped against the glass is a",
        "letter on thick cream paper, with a purple seal."])
    c += S.say("Zephyrine", ["...That's the Collegium's crest."])
    c += S.narrate([
        "Prudence calls over from the bar that it came on Tuesday,",
        "and she put it where Zephyrine would see it, and it has",
        "been a long time since anybody wrote to that table."])
    c += S.narrate([
        "COLLEGIUM ARCANUM. THE LIBRARY.",
        "NOTICE OF OUTSTANDING FINES (ELEVENTH).",
        "Miss Z. Vance, on study leave."])
    c += S.narrate([
        "The Library would be grateful for a convenient moment.",
        "P. Pennock, Registrar's clerk, encloses directions to",
        "Thistlewick, in case."])
    c += S.say("Zephyrine", ["Study leave."])
    c += S.say("Zephyrine", ["STUDY leave. I was EXPELLED.",
                             "There was an ENQUIRY. It used the",
                             "phrase TWICE."])
    c += S.narrate([
        "She reads it three more times. Then she folds it very",
        "small, and puts it in her hat."])
    c += S.say("Zephyrine", ["We're going to the Collegium.",
                             "I am going to appeal.",
                             "I don't know against what."])
    c += [R.gain_item(db.IT_FINES_NOTICE), R.play_se("Book1")]
    c += S.got(["You have the \\C[3]Notice of Fines (Eleventh)\\C[0]."])
    c += [S.trope(), R.control_switch(db.SW_ZEPH1_ON, True)]
    img = R.image("", tile_id=K_ENVELOPE)
    nothing = dict(img=R.image(""), trigger=0, priority=0, through=True)
    return R.event(event_id, "Zephyrine's Letter", x, y, [
        R.page([], **nothing),
        R.page(c, img=img, trigger=0, priority=1, direction_fix=True,
               conditions={"actorValid": True, "actorId": db.ZEPH}),
        R.page([], conditions={"switch1Valid": True,
                               "switch1Id": db.SW_ZEPH1_ON}, **nothing),
    ])


# `Envelope` on Inside_C, which the Turnip's tileset has: a letter on the
# table, drawn over her glass.
K_ENVELOPE = K.sf_tile("Inside_C", "Envelope")


def door_pages(go_in):
    """Pages 4 and 5 of each of the Collegium's world-map door events, after
    the three of `collegium.world_doors`. `go_in` is the transfer through the
    gate, which only the place module knows."""
    zeph = {"actorValid": True, "actorId": db.ZEPH}
    touch = dict(img=R.image(""), trigger=1, priority=0, through=True)
    appeal = S.narrate([
        "A college of cream-coloured stone, all towers and purple",
        "spires. Zephyrine has stopped in the road again. She takes",
        "the notice out of her hat and reads it, again."])
    appeal += S.say("Zephyrine", ["Study leave."])
    appeal += S.say("Zephyrine", ["I am going in there to appeal, and",
                                  "I want it on the record that I am",
                                  "FINE."])
    appeal += R.choice_block(
        ["Go in at the gate", "Press on"],
        [list(go_in),
         S.say("Zephyrine", ["...Tomorrow. I'll be fine tomorrow."])])
    after = S.narrate([
        "A college of cream-coloured stone, all towers and purple",
        "spires, with a gate in the middle of it and a large man",
        "standing in the gate."])
    after += _z1_paid_or_expelled(
        S.narrate(["Zephyrine walks towards it as if she had been out",
                   "for a newspaper."]),
        S.say("Zephyrine", ["Member of the public.",
                            "I'll keep to the path. Mostly."]))
    after += R.choice_block(
        ["Go in at the gate", "Press on"],
        [list(go_in),
         S.narrate(["You press on. Somewhere inside, a bell rings",
                    "for something, and then for something else."])])
    return [
        R.page(appeal, conditions=dict(zeph, switch1Valid=True,
                                       switch1Id=db.SW_ZEPH1_ON), **touch),
        R.page(after, conditions=dict(zeph, switch1Valid=True,
                                      switch1Id=db.SW_ZEPH1_DONE), **touch),
    ]


def gedge_page(last):
    """Mr Gedge (Map 58, event 6), below his one-self-switch ladder, with
    Zephyrine once the notice is read. The Lodge knew her all along."""
    c = R.if_then(
        R.condition_switch(db.SW_ZEPH1_DONE),
        _z1_paid_or_expelled(
            S.say("Mr Gedge", ["Afternoon, Miss Vance.",
                               "Your slide's up. I painted it myself."]),
            S.say("Mr Gedge", ["Member of the public,",
                               "is it, Miss Vance? Keep to the path.",
                               "Lovely to see you."])),
        S.say("Mr Gedge", ["Miss Vance. Afternoon.",
                           "Your pigeonhole's full. Eleven years",
                           "of it. Library first, I should think."])
        + S.say("Zephyrine", ["You KNEW. You knew I'd never been",
                              "expelled."])
        + S.say("Mr Gedge", ["The Lodge knows",
                             "everything, miss. The Lodge is never",
                             "asked."]))
    return _dressed(last, c, {
        "selfSwitchValid": True, "selfSwitchCh": "A",
        "switch1Valid": True, "switch1Id": db.SW_ZEPH1_ON,
        "actorValid": True, "actorId": db.ZEPH})


def _dressed(last, commands, conditions):
    """A new page in `last`'s dress - its image, trigger and priority - with
    its own commands and conditions."""
    page = R.page(commands, conditions=conditions)
    return dict(copy.deepcopy(last), list=page["list"],
                conditions=page["conditions"])


def _afterwards(last, conditions, paid, expelled):
    """`last`, somebody's own last page, with a line after it for whichever
    end of ZEPH-1 she took."""
    body = last["list"][:-1] + _z1_paid_or_expelled(
        S.narrate(paid), S.narrate(expelled))
    return _dressed(last, body, conditions)


def _z1_reveal():
    """There is no appeal, because there was no expulsion. Once."""
    c = S.narrate([
        "A young man in a gown at the end of the desk, with a file",
        "under his arm, who goes pink when he sees Zephyrine."])
    c += S.say("Mr Pennock", ["Miss Vance! You came.",
                              "Pennock - Registrar's clerk. I wrote",
                              "to you."])
    c += S.say("Zephyrine", ["You wrote to me at a public house."])
    c += S.say("Mr Pennock", ["Your file gave your",
                              "address as 'passing through",
                              "Thistlewick'. The Turnip seemed the",
                              "likeliest place to pass."])
    c += S.say("Zephyrine", ["I am here to appeal my expulsion.",
                             "I've had eleven years to prepare it.",
                             "It is forty pages, and most of it is",
                             "about the room."])
    c += S.say("Mr Pennock", ["Ah. Yes. That's the",
                              "thing. You can't. There isn't one."])
    c += S.narrate([
        "He opens the file. In it is one sheet: drafted, initialled",
        "by the Dean, and stamped REFERRED TO THE REGISTRAR FOR",
        "FILING."])
    c += S.say("Mr Pennock", ["The Registrar referred",
                              "it to the Committee for Expulsions.",
                              "Which hasn't met since. It's never",
                              "had to."])
    c += S.say("Mr Pennock", ["So in law you went on",
                              "study leave. Unpaid. You're a member",
                              "of this Collegium in good standing,",
                              "Miss Vance, and you always were."])
    c += S.narrate([
        "Zephyrine sits down on the edge of the Sub-Librarian's",
        "desk, which nobody has ever done."])
    c += S.say("Zephyrine", ["I have been passing through",
                             "Thistlewick for eleven years because",
                             "of a FILING ERROR."])
    c += S.say("Prewitt", ["Not an error, Miss",
                           "Vance. A referral."])
    c += S.say("Prewitt", ["Which brings us, I'm",
                           "afraid, to the Register."])
    c += S.narrate([
        "Mr Gedge is sent for to lift it, although it is not a",
        "Monday. Prewitt unlocks the clasp and opens it at the",
        "large account. It is Zephyrine's. It always was."])
    c += S.say("Prewitt", ["Three books, borrowed",
                           "in the spring of 1989. A penny a day,",
                           "with the day's interest, every day,",
                           "for eleven years."])
    c += [R.play_se("Book1"), R.wait(20)]
    c += S.narrate([
        "The number runs across both pages and on to a third:",
        "4,117,206 crowns and ninepence. It is the largest number",
        "anybody has ever written down, and it is correct."])
    c += S.say("Zephyrine", ["I have the books. One of them is",
                             "holding my door shut."])
    c += S.say("Prewitt", ["Returning them stops",
                           "the fine. It does not pay it."])
    c += S.say("Mr Pennock", ["But! Statute nine.",
                              "A member who turns out her purse on",
                              "the Library desk, in good faith, on",
                              "the day, is deemed to have paid."])
    c += S.say("Prewitt", ["It has never been",
                           "invoked. Nobody has ever had the nerve",
                           "to turn out a purse in the Library."])
    c += S.say("Mr Pennock", ["Or - the draft only",
                              "wants filing. It's initialled. If",
                              "you'd rather be expelled, I could",
                              "file it this afternoon."])
    c += S.narrate([
        "Zephyrine looks at the Register, and at the draft, and",
        "then, for some time, at you."])
    c += [R.control_switch(db.SW_ZEPH1_TOLD, True)]
    return c


def _z1_pay():
    c = [R.control_variable_script(db.VAR_ZEPH1_PAID, "$gameParty.gold()")]
    c += R.script(["$gameParty.loseGold($gameParty.gold());"])
    c += [R.play_se("Coin"), R.wait(10), R.play_se("Coin", pitch=90),
          R.wait(10), R.play_se("Coin", pitch=110), R.wait(20)]
    c += S.narrate([
        "You turn out the purse on the Library desk: every crown",
        "the party has, \\V[%d] of them, and some buttons."
        % db.VAR_ZEPH1_PAID])
    c += S.narrate([
        "Prewitt counts it, all of it, buttons separately. Then",
        "she rules a line under the largest number she has ever",
        "written down, and writes beneath it: PAID IN GOOD FAITH."])
    c += S.say("Prewitt", ["It has never been",
                           "paid before. I find I want to sit",
                           "down."])
    c += S.narrate([
        "Mr Pennock goes into the Registrar's cupboard and comes",
        "out with a robe, white and purple, folded the way they",
        "were folded eleven years ago. Her name is in the collar."])
    c += S.say("Mr Pennock", ["Z. Vance, of this",
                              "Collegium. On study leave. In good",
                              "standing."])
    c += S.say("Zephyrine", ["Say it again."])
    c += S.say("Mr Pennock", ["In good standing,",
                              "Miss Vance."])
    c += [R.gain_armor(db.AR_COLLEGIUM_ROBE), R.play_me("Fanfare1")]
    c += S.got(["You have the \\C[3]Collegium Robe (Vance)\\C[0]."])
    c += S.say("Zephyrine", ["I am still not casting anything",
                             "indoors."])
    c += [R.control_switch(db.SW_ZEPH1_PAID, True)]
    return c


def _z1_file():
    c = S.say("Zephyrine", ["No. I'd like to be expelled, please.",
                            "Properly. In writing."])
    c += S.say("Zephyrine", ["It's the only thing anybody here",
                             "ever did about it, and it wasn't even",
                             "done."])
    c += S.narrate([
        "She signs the draft under the Dean's initials. Mr Pennock",
        "stamps it FILED, and files it, in the pigeonhole marked",
        "FILED, which is empty, and which he dusts first."])
    c += S.say("Prewitt", ["Members of the public",
                           "are not fined, Miss Vance. The account",
                           "is closed."])
    c += S.narrate([
        "She rules a line under the largest number she has ever",
        "written down, and writes CLOSED, and looks at it for some",
        "time, as you might look at a view."])
    c += S.say("Zephyrine", ["Expelled. At last."])
    c += S.narrate(["She is smiling, which nobody had expected."])
    c += [R.control_switch(db.SW_ZEPH1_EXPELLED, True)]
    return c


def _z1_scene():
    """Mr Pennock's page with Zephyrine and the notice: the reveal once, then
    the decision, which "Not today" leaves on the desk."""
    c = R.if_then(R.condition_switch(db.SW_ZEPH1_TOLD),
                  S.say("Mr Pennock", ["Miss Vance. The file's",
                                       "on the desk, and the Register's",
                                       "open. Purse, or draft?"]),
                  _z1_reveal())
    done = [S.trope(), R.control_switch(db.SW_ZEPH1_DONE, True)]
    done += S.companion_story(db.ZEPH)
    c += R.choice_block(
        ["Turn out the purse", "File the expulsion", "Not today"],
        [_z1_pay() + done, _z1_file() + done,
         S.say("Mr Pennock", ["It'll keep, Miss Vance.",
                              "Everything here does."])])
    return c


PENNOCK_IMG = ("Gen_People13", 2)


def pennock_event(event_id, x, y):
    """The Registrar's clerk (Map 59), at the east end of Prewitt's desk: not
    there until the notice is read, waiting for her if she is not in the
    party, the scene if she is, and afterwards for everybody."""
    img = R.image(*PENNOCK_IMG, direction=2)
    on = {"switch1Valid": True, "switch1Id": db.SW_ZEPH1_ON}
    waiting = S.say("Mr Pennock", ["Miss Vance's file. I keep",
                                   "it on the desk. She'll come."])
    after = _z1_paid_or_expelled(
        S.say("Mr Pennock", ["Miss Vance's is the",
                             "tidiest file in the building. I keep",
                             "it on top."]),
        S.say("Mr Pennock", ["Miss Vance's expulsion",
                             "is the only thing I've ever actually",
                             "filed. It was very satisfying."]))
    return R.event(event_id, "Mr Pennock", x, y, [
        R.page([], img=R.image(""), priority=0, through=True),
        R.page(waiting, img=img, conditions=on),
        R.page(_z1_scene(), img=img,
               conditions=dict(on, actorValid=True, actorId=db.ZEPH)),
        R.page(after, img=img, conditions={"switch1Valid": True,
                                           "switch1Id": db.SW_ZEPH1_DONE}),
    ])


def prewitt_pages(last):
    """Prewitt (Map 59, event 2), below her one-self-switch ladder: with
    Zephyrine and the notice, a referral; and afterwards, for everybody."""
    seen = {"selfSwitchValid": True, "selfSwitchCh": "A"}
    with_her = S.say("Prewitt", ["Miss Vance. Good",
                                 "afternoon. Mr Pennock has your file.",
                                 "He has kept it on top since March."])
    return [
        _dressed(last, with_her, dict(
            seen, switch1Valid=True, switch1Id=db.SW_ZEPH1_ON,
            actorValid=True, actorId=db.ZEPH)),
        _afterwards(last, dict(seen, switch1Valid=True,
                               switch1Id=db.SW_ZEPH1_DONE),
                    ["She has a ruled line in the Register, and under it",
                     "PAID IN GOOD FAITH, and she looks at it sometimes."],
                    ["The large account is ruled off: CLOSED. She looks",
                     "at it sometimes, as you might look at a view."]),
    ]


def register_page(last):
    """The Register (Map 59, event 3) afterwards, for everybody."""
    return _afterwards(
        last, {"selfSwitchValid": True, "selfSwitchCh": "A",
               "switch1Valid": True, "switch1Id": db.SW_ZEPH1_DONE},
        ["It is a little lighter than it was. Only a little."],
        ["It is a little lighter than it was. Only a little."])


def board_page(page0):
    """The IN and OUT board (Map 58, event 8), once the purse is turned out:
    as it was, and one new slide at the bottom."""
    body = page0["list"][:-1] + S.narrate([
        "At the bottom, newly painted, Z. VANCE: OUT. And under",
        "it, in the Porter's pencil, \"Study leave. Good standing.\""])
    return _dressed(page0, body, {"switch1Valid": True,
                                  "switch1Id": db.SW_ZEPH1_PAID})
