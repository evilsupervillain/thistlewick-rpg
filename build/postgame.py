"""The post-game: what happens after THE END. `../POSTGAME.md` is the design.

The Prophecy's defeat stops being the end. The finale's tally plays, and then
the party wakes up in Bram's house the next morning, with every unfinished
quest still there to finish. This module holds the parts that are new;
`journey.finale_event` and the place modules call into it, one line per hook,
the way they call the `q_*` modules (`QUESTS.md` 0.4). It imports no place
module.

P4a (this step) is the hand-back and G1's ending lines:

* `companion_lines()` - one `if/else` chain per companion over that
  companion's quest switches, best line first, so each companion who has a
  story gets exactly one line in the tally; then the closing count on
  `VAR_COMPANION_STORIES`. Every line is a candidate from a Done paragraph in
  `QUESTS.md` section 3, used as written. The two exceptions are WRE-5,
  whose two candidates are stitched into one box, and SPA-4, which loses an
  "either" that leaned on SPA-1. `POSTGAME.md` 7 has the chains.
* `rol5_line()` - Maud, inside the tally's `SW_ROLAND_GONE` block, after
  "...who thinks about this one".
* `hand_back()` - what replaces Return to Title after THE END.
* `grimspite_afterwards()` - the throne's page once `SW_WON` is on. He stays,
  with a kettle, and offers the tea Halbert Quy turned down.
"""

import copy
import os
import sys

import db
import mapkit as K
import places
import rmmzdata as R
import story as S


# ================================================================== G1 ==
# One chain per companion, in actor order. Each entry is (switch, boxes):
# the first switch that is on prints its boxes and the rest are skipped.
# A box is up to four lines, broken by hand, because where a line breaks
# is the timing.
CHAINS = [
    ("Merribell", [
        (db.SW_MER1_DONE, [[
            "The Order of Whatever Works won the Sisterhouse",
            "on points, nineteen to one, in an afternoon.",
            "Sister Bewick has been examined on its doctrine,",
            "and passed. It is four lines long."]]),
        (db.SW_MER4_DONE, [[
            "Tobias Frayne has not died since.",
            "He has the parish to tea."]]),
        (db.SW_MER5_DONE, [[
            "The curse of Sump was lifted in the year 2000 by",
            "the Water Committee, one member, with a glass of",
            "water. The minutes record an item three."]]),
        (db.SW_MER3_DONE, [[
            "Sister Merribell is to speak at the Healers'",
            "Table next year. She has nothing to tell them",
            "yet. She is writing it down."]]),
        (db.SW_MER2_DONE, [[
            "Sister Merribell certified the party fit to",
            "travel, which makes this the first properly",
            "documented attempt in four thousand years."]]),
    ]),
    ("Hob", [
        (db.SW_HOB1_DONE, [[
            "The Worshipful Company of Smiths disqualified a",
            "hammer called Beatrice under clause one. The",
            "Wardens' notes say she is right about everything."]]),
        (db.SW_HOB4_DONE, [[
            "The Sky Anvil has a gate on it, out of eleven",
            "gates, with a spring on the latch. The star-iron",
            "made one sword. Hob Grumnir has not said who it",
            "is for."]]),
        (db.SW_HOB2_DONE, [[
            "Thistlewick churchyard has a new gate, with a",
            "good latch. Somebody says the latch wants a",
            "spring."]]),
        (db.SW_HOB5_DONE, [[
            "The Two Hundred's tube plate was made at",
            "Ollerenshaw's in one heat, by four hands. Neither",
            "of them has mentioned it since. Ott Hoyle says",
            "it will do."]]),
        (db.SW_HOB3_DONE, [[
            "Two apprentices failed module seven, acquisition",
            "of a heavy object, by eleven feet. The apology is",
            "framed in the smithy, next to nothing Hob made."]]),
    ]),
    ("Zephyrine", [
        (db.SW_ZEPH2_DONE, [[
            "The Collegium Arcanum has been quorate since the",
            "duck came back. Its vote is held by proxy,",
            "permanently, by Zephyrine Vance.",
            "She has not yet used it. She is saving it."]]),
        (db.SW_ZEPH1_PAID, [[
            "Zephyrine Vance is a member of the Collegium",
            "Arcanum in good standing. Her library fines were",
            "paid in good faith, out of a purse, on the",
            "Library desk."]]),
        (db.SW_ZEPH1_EXPELLED, [[
            "Zephyrine Vance was expelled from the Collegium",
            "Arcanum eleven years after the event, at her own",
            "request. She filed it herself."]]),
        (db.SW_ZEPH4_DONE, [[
            "The Cinder Fen was burnt in the year 2000 by",
            "Zephyrine Vance, fire person, sanctioned, in",
            "triplicate. The road to Great Dunnage is dry,",
            "and the form came back countersigned."]]),
        (db.SW_ZEPH3_DONE, [[
            "Dean Fenwold is fine. His talk now ends with the",
            "room being wrong, and Dr Hapgood's paper has",
            "Dr Hapgood's name on it."]]),
        (db.SW_ZEPH5_DONE, [[
            "The association of hedge mages has four members",
            "and no name. Item one is carried forward."]]),
    ]),
    ("Nix", [
        (db.SW_NIX1_DONE, [[
            "The client has been identified. The first line",
            "of Nix's ledger has a provenance now, and the",
            "coat fits."]]),
        (db.SW_NIX4_DONE, [[
            "Nix's ledger has a RETURNED column now, with",
            "eleven lines in it. Over the page there is a",
            "parcel, for a client not yet identified."]]),
        (db.SW_NIX3_DONE, [[
            "Cobb Lorrimer, thief, lost a contest to Nix on",
            "paperwork. He is the Dark Lord in Nether Sopping",
            "now, afternoons, signed for, and he loses."]]),
        (db.SW_NIX5_DONE, [[
            "Enoch Bagshawe crossed the Gloamwood by night",
            "without a single encounter, or half of one.",
            "The Works Band has a bassoon."]]),
        (db.SW_NIX2_DONE, [[
            "The Counting House at Great Dunnage has been",
            "opened, informally. It held a chair.",
            "Form L remains blank."]]),
    ]),
    ("Aldric", [
        (db.SW_ALD2_DONE, [[
            "Sir Aldric Pemberton-Gore the Third kept his",
            "vigil in the right chapel, thirty years late,",
            "and did not move until it was light."], [
            "The knight on his shield is looking back, to see",
            "who is behind him. Somebody always is."]]),
        (db.SW_ALD5_DONE, [[
            "Sir Aldric Pemberton-Gore the Third has a squire,",
            "who finds the gates. He has been home. He went",
            "the long way round, and it was still a way."]]),
        (db.SW_ALD4_DONE, [[
            "Duchess, a grey mare, is a partner in Plummer &",
            "Partner, haulage, of Great Dunnage. Her knight",
            "calls on her. Not on Tuesdays."]]),
        (db.SW_ALD3_DONE, [[
            "Sir Aldric Pemberton-Gore the Third has been",
            "promoted, to Knight Errant, At Large. He carries",
            "his own pin. Wherever he is, the map is correct."]]),
        (db.SW_ALD1_DONE, [[
            "Sir Aldric Pemberton-Gore delivered his first",
            "errand, nine years late, by a route of a hundred",
            "and ten miles. It is on a mantelpiece in Little",
            "Gore."]]),
        (db.SW_ALD6_DONE, [[
            "Somewhere in the rocks above the water there is",
            "the only dragon in the valley, uneaten. A knight",
            "reads it the Odes, when he can find the way."]]),
    ]),
    ("Piper", [
        (db.SW_PIP4_DONE, [[
            "On the back of the fingerpost at Little Gore",
            "there are nine lines by Piper Quill, which she",
            "has never performed. The road is four miles",
            "long. He walks it still."]]),
        (db.SW_PIP1_GOOD, [[
            "The official account of the Forty-Eighth is by",
            "Ambrosine Quill, and it is very good. Bram is an",
            "orphan in it, and there is a wolf. It has one",
            "footnote, by P. Quill: none of this happened."]]),
        (db.SW_PIP1_FIXED, [[
            "The official account of the Forty-Eighth is by",
            "A. and P. Quill. It is true, and it scans, and",
            "where the wolf was there is a goat, which is in",
            "the minutes."]]),
        (db.SW_PIP3_DONE, [[
            "Piper Quill came second at the Contest at the",
            "Sign of the Bell, by one point, to a thrush."], [
            "The certificate is framed. It is the first prize",
            "a Quill has won for writing down what actually",
            "happened."]]),
        (db.SW_PIP2_DONE, [[
            "The ballad's last verse took an afternoon and",
            "nine seconds, and the turnip is in the middle of",
            "a line, where nothing has to rhyme with it."]]),
        # Last, because the tally has already printed \V[7] two blocks up.
        (db.SW_PIP5_DONE, [[
            "The Committee's box of struck verses holds"
            " \\C[3]\\V[7]\\C[0].",
            "Piper Quill has read every one of them, and",
            "printed none."]]),
    ]),
    ("Corvin", [
        (db.SW_COR1_DONE, [[
            "Corvin Ash spoke at the Ashcombe Flood Dinner,",
            "and it went well. He gave the village its name",
            "back. His mother knitted him a scarf in the",
            "wrong colour, and he wears it."]]),
        (db.SW_COR2_DONE, [[
            "Corvin Ash's sword is called Mind The Step. His",
            "grandfather made it for a doorstop. His school",
            "report says he will go far, if he ever gets up.",
            "He is up."]]),
        (db.SW_COR4_DONE, [[
            "Mother Selvidge has read Corvin Ash three times.",
            "A long life, a useful trade, no destiny",
            "whatsoever. She has never once been wrong."]]),
        (db.SW_COR3_DONE, [[
            "Corvin Ash is second on the league table at the",
            "Sable Hart, behind a scar. He has a chair there,",
            "in the middle of the room, in the light.",
            "He attends."]]),
        (db.SW_COR5_DONE, [[
            "There is no curse on Corvin Ash's sword. He has",
            "the form, if he wants one. It is not expensive."]]),
    ]),
    ("Wren", [
        (db.SW_WRE1_DONE, [[
            "The Fauna of the Valley, by What They Are, by",
            "W. Halloway, is on the shelf of the Collegium",
            "Arcanum, in a gap exactly an inch wide."], [
            "It has eleven type specimens and three",
            "reviewers, one of them a duck.",
            "Page four hundred says goose."]]),
        (db.SW_WRE5_NAMED, [[
            "The thing in the turnips is in W. Halloway's",
            "journal: Bramus agricola, statistically",
            "indefensible. The Prophecy does not read",
            "journals. It has read one."]]),
        (db.SW_WRE3_DONE, [[
            "The Gloamwood Society has proved there is",
            "nothing in the Gloamwood. Next year's walk is",
            "expected to be very well attended."]]),
        (db.SW_WRE4_DONE, [[
            "The Fenmarch Collection has been authenticated",
            "by W. Halloway: seventy-nine composed, the",
            "finest joins she has seen. The family has never",
            "been prouder. Case forty was not examined."]]),
    ]),
    ("Roland", [
        (db.SW_ROL2_DONE, [[
            "Roland Fairweather's prophecy was discharged in",
            "an afternoon, under Carn Drey, with help.",
            "He asked to be surprised. Everybody was."]]),
        (db.SW_ROL4_REFIT, [[
            "Roland said his sword had never been in a last",
            "room. It went into one after all, on a",
            "Thistlewick haft, in a Thistlewick hand."]]),
        (db.SW_ROL3_DONE, [[
            "Eleven parties finished their quests without",
            "Roland Fairweather. They drank to him anyway:",
            "to the man who got them all to the door."]]),
        (db.SW_ROL1_DONE, [[
            "Somewhere there are minutes of a hundred and",
            "forty-one meetings, at which Roland Fairweather",
            "was present and available, and was thanked for",
            "his patience."]]),
    ]),
    ("Spare", [
        (db.SW_SPA2_DONE, [[
            "Spare Cotterill went into the Dunnage bottom",
            "lock alone, in the dark. Somebody was there",
            "when he came out."]]),
        (db.SW_SPA4_DONE, [[
            "Spare Cotterill met his pen pal at last, in Much",
            "Pottering. There was no volcano.",
            "They are still writing."]]),
        (db.SW_SPA1_DONE, [[
            "Spare Cotterill wrote home from eight towns.",
            "There was no dragon. His mother did more",
            "potatoes anyway."]]),
    ]),
]


def _chain(links):
    """The first link whose switch is on prints; the rest are its else."""
    sw, boxes = links[0]
    body = []
    for box in boxes:
        body += S.narrate(box)
    rest = _chain(links[1:]) if len(links) > 1 else None
    return R.if_then(R.condition_switch(sw), body, rest)


def companion_lines():
    """G1: one line per companion with a story, then how many had one.

    Goes in the tally after Firstfield and before clause twelve is struck, so
    that clause twelve and the walk to Halbert Quy stay the last words."""
    c = []
    for _who, links in CHAINS:
        c += _chain(links)
    n = db.VAR_COMPANION_STORIES
    c += R.if_then(
        R.condition_variable(n, 10, 1),
        S.narrate(["All ten of them got something out of it as well."]),
        R.if_then(
            R.condition_variable(n, 2, 1),
            S.narrate(["\\C[3]\\V[%d]\\C[0] of them got something out of it"
                       " as well." % n]),
            R.if_then(
                R.condition_variable(n, 1, 0),
                S.narrate(["One of them got something out of it as well."]))))
    return c


def rol5_line(amended=False):
    """ROL-5's candidate, after "...who thinks about this one". Inside the
    `SW_ROLAND_GONE` branch, so it is never read without the line it follows.

    `amended` is the lectern's reading (P4c). Maud told after the ending
    (`SW_ROL5_LATE`) did not wait at the door - nobody did - so she gets the
    line for what she did instead, which is go and see the bit after. And a
    Roland engaged again since (`SW_ROLAND_BACK`) is not only being
    marvellous in somebody else's story, and would like that noted."""
    told = S.narrate([
        "Somebody saw the end of this one. She is sixteen,",
        "and she waited at the door, and she has gone to",
        "tell him how it ends."])
    if not amended:
        return R.if_then(R.condition_switch(db.SW_ROL5_DONE), told)
    late = S.narrate([
        "Somebody was told the end of this one afterwards,",
        "over a pie. She is sixteen, and she has gone to see",
        "one for herself. Not the end: the bit after."])
    back = S.narrate([
        "He has since been engaged again, between",
        "engagements, and has asked that the account say so."])
    return (R.if_then(R.condition_switch(db.SW_ROL5_LATE), late,
                      R.if_then(R.condition_switch(db.SW_ROL5_DONE), told))
            + R.if_then(R.condition_switch(db.SW_ROLAND_BACK), back))


def amended_lines():
    """What only the post-game can add to the account, read at the lectern
    before clause twelve is struck (`journey.tally`). P4d-P4e's lamp and
    Stair go here."""
    c = R.if_then(R.condition_switch(db.SW_GRIMSPITE_TEA), S.narrate([
        "Grimspite the Inevitable has retired, and stays on",
        "in the tower with a kettle. One Chosen One has had a",
        "cup. It was just tea."]))
    import mountain
    return c + mountain.account_lines()


# ============================================================ the hand-back ==
HOME_X, HOME_Y = 8, 8       # where a new game starts, in Bram's house


def hand_back():
    """After THE END, in place of Return to Title: the next morning.

    The screen is already black (the tally plays over the fade), so the
    transfer takes no fade of its own and the house fades in after it. The
    party is rested, because it is the next morning; the house's own music
    takes over on arrival."""
    c = [R.fadeout_bgm(2), R.wait(60)]
    c += S.narrate(["The next morning there are still turnips."])
    # P4b: Maud's "to tell her?" is settled for anyone who told her, so
    # her page for a telling after the ending (`q_roland`) can key on it.
    c += R.if_then(R.condition_switch(db.SW_ROL5_DONE),
                   [R.control_switch(db.SW_ROL5_ON, False)])
    c += [R.recover_all(),
          R.transfer(places.MAP_HOME, HOME_X, HOME_Y, direction=2, fade=2),
          R.wait(30), R.fadein_screen()]
    return c


# =============================================================== the tower ==
def grimspite_afterwards():
    """The throne once the Prophecy is gone: he stays, with a kettle.

    The page after the empty `SW_WON` pages, so it beats all of them. The tea
    is the one Halbert Quy turned down thirty years ago; `SW_GRIMSPITE_TEA`
    is global because P4c's Quy asks what it was like."""
    first = S.narrate([
        "Grimspite is in his chair, with the book open at",
        "the bookmark."])
    first += S.narrate([
        "On the wall behind you, forty-seven carvings.",
        "There is room for a forty-eighth.",
        "Nobody is going to need it."])
    first += S.say("Grimspite", [
        "Forty-eight.",
        "Nobody's ever come back up.",
        "There's a kettle on, if you want one."])
    have = S.narrate(["It is just tea."])
    have += S.say("Grimspite", ["There. Now somebody has."])
    have += [R.control_switch(db.SW_GRIMSPITE_TEA, True)]
    later = S.say("Grimspite", [
        "Halbert said no as well.",
        "It's all right. The kettle's always on now."])
    first += R.choice_block(["Have a cup", "Not just now"], [have, later],
                            cancel=1)

    again = S.narrate(["Grimspite looks up from his book."])
    again += S.say("Grimspite", [
        "Forty-eight. Kettle's on.",
        "It's still just tea."])

    c = R.if_then(R.condition_switch(db.SW_GRIMSPITE_TEA), again, first)
    return R.page(c, img=R.image("Evil", 6, direction=2), trigger=0,
                  priority=1, direction_fix=True,
                  conditions={"switch1Valid": True, "switch1Id": db.SW_WON})


# ===================================================================== P4b ==
# Thistlewick, the pension, and Roland (POSTGAME.md 3a-5). Thistlewick is
# delighted, proud, and very keen that Bram should enjoy the coast, and
# never notices the calendar (TIMELINE.md 1).
WON = {"switch1Valid": True, "switch1Id": db.SW_WON}


def _like(dress, cmds, conditions):
    """A page in exactly another page's dress, with its own commands and
    conditions."""
    shaped = R.page(cmds, conditions=conditions)
    page = copy.deepcopy(dress)
    page["list"] = shaped["list"]
    page["conditions"] = shaped["conditions"]
    return page


def _shows(n, i):
    """A script condition: of this event's first `n` pages, the ladder would
    show page `i`. Found the way `Game_Event.refresh` finds it - the last
    page whose conditions hold - so a page appended above a ladder can still
    hand over to a page under it that owes the player a beat."""
    return ("(e => { const p = e.event().pages; for (let i = %d; i >= 0; i--)"
            " if (e.meetsConditions(p[i])) return i; return -1; })"
            "($gameMap.event(this._eventId)) === %d" % (n - 1, i))


def _owing(ev, owed, body):
    """`body`, unless the ladder below would show one of the `owed` pages,
    which then runs instead, word for word. `owed` is (index, extra js or
    None) pairs; the js narrows when a page still owes its beat.

    This is how a post-game page goes on somebody whose ladder ends in a
    switch the post-game cannot wait on (`QUESTS.md` 0.2): NIX-4's owners,
    NIX-3's door, Ysolde. The page does not shadow the beat it sits on top
    of; it plays it."""
    n = len(ev["pages"])
    c = list(body)
    for i, js in reversed(owed):
        test = _shows(n, i) + (" && " + js if js else "")
        c = R.if_then(R.condition_script(test), ev["pages"][i]["list"][:-1],
                      c)
    return c


# ------------------------------------------------------- the letter, Map 2 --
def letter_event(event_id, x, y):
    """The letter on the mat, just inside Bram's front door (Map 2): nothing
    before the ending; the Committee's envelope after it; and nothing once
    it has been picked up. Below characters, on a square the player stands
    on, so it is read from the mat.

    The envelope is a character sprite (`LETTER_SHEET`), **not** a tile
    picture: `Game_Map.allTiles` counts the tile of every tile-picture event
    on a square, through or not, and `Envelope` is flagged blocked, so as a
    tile it sealed the mat and the doorway with it."""
    read = S.narrate([
        "A letter on the mat, in the Committee's envelope, with",
        "the Committee's seal. Somebody has polished the seal."])
    read += S.narrate([
        "\\C[6]PROPHECY OF THISTLEWICK - CLAUSE NINETEEN\\C[0]",
        "With the Committee's congratulations on your return.",
        "Enclosed: your pension, and the key to a cottage at",
        "Nether Sopping, at such distance as is mutually agreeable."])
    read += S.narrate(["We trust Friday will suit."])
    read += [R.gain_gold(db.PENSION), R.gain_item(db.IT_COTTAGE_KEY, 1),
             R.play_me("Item")]
    read += S.got(["Got %d\\G and \\I[195]\\C[3]A Key, Labelled\\C[0]."
                   % db.PENSION])
    read += S.narrate(["The pension is one quarter, in advance.",
                       "There is no mention of the next one."])
    read += [R.self_switch("A", True)]
    blank = dict(img=R.image(""), trigger=0, priority=0, through=True)
    return R.event(event_id, "The Letter on the Mat", x, y, [
        R.page([], **blank),
        R.page(read, img=R.image(LETTER_SHEET, 0, direction=2), trigger=0,
               priority=0, direction_fix=True, conditions=WON),
        R.page([], conditions=dict(WON, selfSwitchValid=True,
                                   selfSwitchCh="A"), **blank),
    ])


def mother(ev):
    """Mother (Map 2, event 3), afterwards. Her ladder ends in NIX-4's self
    switch, so NIX-4's page plays when it is still owed (`_owing`)."""
    before = S.say("Mother", [
        "Morning, love. There's a letter come.",
        "It's on the mat. It's from the Committee.",
        "I haven't opened it. I've looked at it."])
    after = S.say("Mother", [
        "A cottage! By the sea!"])
    after += S.narrate(["She is very proud. She has her hands together."])
    after += S.say("Mother", [
        "You'll want your good shirt.",
        "I ironed it Tuesday."])
    body = R.if_then(R.condition_item(db.IT_COTTAGE_KEY), after, before)
    ev["pages"].append(_like(ev["pages"][0], _owing(ev, [(1, None)], body),
                             WON))
    return ev


# ------------------------------------------------------- Thistlewick, Map 1 --
def old_man(ev):
    """The Old Man (Map 1, event 13), whose boy was the Forty-Seventh: short,
    and the one villager not in on the coast (Mike, 8 Oct 2026). NIX-4's
    page plays when it is still owed."""
    body = S.say("Old Man", ["You came back."])
    body += S.narrate(["He takes your hand, and holds on to it for a while."])
    body += S.say("Old Man", ["Good lad. That's all. Good lad."])
    ev["pages"].append(_like(ev["pages"][0], _owing(ev, [(1, None)], body),
                             WON))
    return ev


def child_page(dress):
    """The child who heard about the dungeon (Map 1, event 12), on the
    terminal self switch A: the news, at volume, again."""
    c = S.say("Child", ["Have you HEARD?",
                        "You're going to the SEASIDE!"])
    c += S.say("Child", ["My mum says it's LOVELY and you'll",
                         "NEVER want to come BACK!"])
    c += S.narrate(["You have heard.",
                    "You will hear again."])
    return _like(dress, c, dict(WON, selfSwitchValid=True, selfSwitchCh="A"))


def board_page(dress):
    """The notice board (Map 1, event 11), on its terminal self switch A."""
    c = S.narrate([
        "\\C[6]THISTLEWICK NOTICE BOARD\\C[0]",
        "- FAREWELL TEA for B. Thistle, the Forty-Eighth.",
        "  Friday. Bring a plate.",
        "- LOST: one goat. Answers to Councillor. Still."])
    return _like(dress, c, dict(WON, selfSwitchValid=True, selfSwitchCh="A"))


def interpreter_page(dress):
    """The man who speaks for the dog (Map 1, event 15): one page, no ladder."""
    c = S.say("Neighbour", [
        "He says well done.",
        "He says the coast is very windy and",
        "you should take a coat."])
    c += S.narrate(["The dog has not made a sound."])
    c += S.say("Neighbour", ["He says it again. Louder."])
    return _like(dress, c, WON)


# ------------------------------------------------------ Prophecy Hall, Map 3 --
def wispel_page(dress):
    """Elder Wispel (Map 3, event 2), who chairs the Committee, on his
    terminal `SW_QUEST`: the hero back, the Receipt, and the sea air."""
    c = S.say("Elder Wispel", ["Bram Thistle! The Forty-Eighth!",
                               "Back!"])
    c += S.narrate(["He shakes your hand with both of his."])
    c += S.say("Elder Wispel", ["And that's the receipt? May I?"])
    c += S.narrate(["He holds the Receipt up to the window, the way you",
                    "would a banknote."])
    c += S.say("Elder Wispel", ["Renewable. What a lovely hand."])
    c += R.if_then(
        R.condition_item(db.IT_COTTAGE_KEY),
        S.say("Elder Wispel", [
            "You'll have had the letter.",
            "Clause nineteen. Sea air, Bram. Sea air",
            "is the thing. You've earned it. It's a",
            "long way, and you've earned that as well."]),
        S.say("Elder Wispel", [
            "There's a letter at home for you.",
            "Clause nineteen. Sea air, Bram. Sea air",
            "is the thing."]))
    return _like(dress, c, dict(WON, switch2Valid=True,
                                switch2Id=db.SW_QUEST))


def frame_event(event_id, x, y, pip1_done):
    """The forty-eighth frame on the Wall of the Forty-Seven (Map 3): a bare
    space under the forty-seventh until the ending, then an empty frame with
    a card in it. PIP-1's card was pinned in the space; it is still there."""
    c = S.narrate([
        "At the end of the forty-seven, a forty-eighth frame,",
        "new, and empty. A card is pinned in it:",
        "PORTRAIT TO FOLLOW. SITTER AT THE COAST."])
    c += R.if_then(R.condition_switch(pip1_done), S.narrate([
        "The Quills' card is tucked into the corner of the",
        "frame, to make room."]))
    return R.event(event_id, "The Forty-Eighth Frame", x, y, [
        R.page([], img=R.image(""), trigger=0, priority=0, through=True),
        R.page(c, img=R.image(FRAME_SHEET, 0, direction=2), trigger=0,
               priority=1, direction_fix=True, conditions=WON),
    ])


def minute_book(event_id, x, y, book_tile):
    """The Committee's minute book (Map 3), open on the table by the door
    once the ending has been minuted. Clause twelve's note, as the tally
    has it; clause nineteen, which still applies."""
    c = S.narrate(["The Committee's minute book, open at this week."])
    c += S.narrate([
        "ITEM 3. Clause twelve. Struck, nem. con. In its",
        "place, a note: SEE BRAM.",
        "ITEM 4. Clause nineteen. Applies. Letter sent,",
        "cottage aired. Friday suggested."])
    c += S.narrate([
        "ITEM 5. Councillor Fenn wished it minuted that he",
        "had been saying so. Minuted."])
    return R.event(event_id, "The Minute Book", x, y, [
        R.page([], img=R.image(""), trigger=0, priority=0, through=True),
        R.page(c, img=R.image(tile_id=book_tile), trigger=0, priority=1,
               direction_fix=True, conditions=WON),
    ])


# ------------------------------------------------------ the Gilded Turnip --
def regular_page(dress):
    """The Regular (Map 4, event 5), whose cousin was the Thirty-Ninth: one
    page, no ladder. He drinks, as before."""
    c = S.say("Regular", ["Here he is! The Forty-Eighth!"])
    c += S.narrate(["He drinks."])
    c += S.say("Regular", ["Coast, is it? Sea air."])
    c += S.narrate(["He drinks again."])
    c += S.say("Regular", ["Lovely coast, apparently."])
    return _like(dress, c, WON)


# --------------------------------------------- Nether Sopping and the cottage --
# Not "next door": next door, to the west, is Number Forty-Five's.
FITCH_NEIGHBOUR = "MRS PIMM, WHO HAS THE OTHER KEY"


def fitch_door(ev, arrive):
    """Nether Sopping's shut "A Front Door" (Map 13, event 15) with the key.
    The published page stays first. NIX-3's page plays when Nix still owes
    it the pot (its self switch A is the pot located)."""
    first = S.narrate([
        "The Committee's key goes into somebody's front door, and",
        "turns, after some thought."])
    first += [R.control_switch(db.SW_COTTAGE_SEEN, True)]
    go = R.if_then(R.condition_switch(db.SW_COTTAGE_SEEN, False), first)
    # The shut page is direction-fixed, being a sign, and the door's opening
    # is a turn through its four rows, so the fix comes off first.
    go += [R.play_se("Open1")]
    go += R.move_route(0, [{"code": 36}] + K.door_animation(), repeat=False,
                       wait_flag=True)
    go += [R.play_se("Move1"),
           R.transfer(places.MAP_FITCH, *arrive, 8, 0)]
    owed = [(1, "!$gameSelfSwitches.value([this._mapId, this._eventId,"
                " 'A'])")]
    ev["pages"].append(_like(ev["pages"][0], _owing(ev, owed, go),
                             {"itemValid": True,
                              "itemId": db.IT_COTTAGE_KEY}))
    return ev


def fitch_events(threshold, bed, chair, pot, note, cupboard):
    """Ambrose Fitch's cottage, Map 71: one room. A bed that rests the party
    for nothing, his chair turned to the window, a dead thing in a pot, and
    a note from the neighbour who has kept the key since he died. The
    neighbour is the old woman NIX-3 met at this door (Mike, 8 Oct 2026);
    she never appears."""
    evs = [S.exit_tile(1, "Front Door", *threshold, places.MAP_SOPPING,
                       *places.FITCH_STEP)]

    sleep = S.narrate(["A bed, made up, with the covers turned down.",
                       "Somebody has aired it."])
    sleep += R.choice_block(
        ["Sleep", "Not now"],
        [[R.fadeout_screen(), R.play_me("Inn1"), R.recover_all(),
          R.wait(60), R.fadein_screen()] +
         S.narrate(["You wake up. You can hear the sea."]) +
         [R.call_common_event(db.CE_MORNING)],                         # SPA-3
         []], cancel=1)
    evs.append(R.event(2, "The Bed", *bed, [R.page(
        sleep, img=R.image(""), trigger=0, priority=1, direction_fix=True,
        through=True)]))

    sat = S.narrate([
        "Ambrose Fitch's chair, turned to face the window.",
        "From it you can see the sea."])
    sat += S.narrate(["Nobody has sat in it since. You don't either."])
    evs.append(R.event(3, "Fitch's Chair", *chair, [R.page(
        sat, img=R.image(CHAIR_SHEET, 0, direction=2), trigger=0,
        priority=1, direction_fix=True)]))

    water = [R.play_se("Water1", 70), R.wait(40)]
    water += S.narrate(["You water it. It goes on being dead, but it has",
                        "been watered."])
    look = S.narrate(["A pot by the window, with a dead thing in it."])
    look += R.choice_block(["Water it", "Leave it"], [water, []], cancel=1)
    evs.append(R.event(4, "The Pot by the Window", *pot, [R.page(
        look, img=R.image(""), trigger=0, priority=1, direction_fix=True,
        through=True)]))

    evs.append(S.sign(5, "A Note on the Table", *note, [
        "A note on the table, in pencil, in a careful hand:",
        "AIRED TUESDAYS. KETTLE IN THE CUPBOARD.",
        "PLEASE DON'T MOVE HIS CHAIR.",
        "- " + FITCH_NEIGHBOUR]))
    evs.append(S.sign(6, "The Cupboard", *cupboard, [
        "A kettle, a caddy of tea, and one cup."]))
    return evs


def ysolde(ev):
    """Ysolde Marrow (Map 14, event 4) once Bram has been in the cottage:
    whichever of her pages is due, and then the pot. Her tale (page 0) and
    the bench (page 2) still owe the player their beat, so they play
    instead, and the line waits for the next time."""
    pot = S.narrate(["You tell her you have been in Ambrose's cottage."])
    pot += S.say("Ysolde", ["Did you water that thing in the pot?"])
    pot += S.say("Ysolde", ["He watered it every morning for forty",
                            "years. It was dead when he bought it.",
                            "He said it was the principle."])
    pages = ev["pages"]
    body = R.if_then(R.condition_script(_shows(len(pages), 3)),
                     pages[3]["list"][:-1] + pot,
                     pages[1]["list"][:-1] + pot)
    pages.append(_like(pages[0], _owing(ev, [(0, None), (2, None)], body),
                       {"switch1Valid": True,
                        "switch1Id": db.SW_COTTAGE_SEEN}))
    return ev


# ------------------------------------------------- Roland, the Slain Wyvern --
def roland_pages(sheet, index):
    """Roland at his table after the ending (Map 14, event 13), between
    engagements: two pages after `story.recruit`'s three (POSTGAME.md 3a).

    * **At his table**, on `SW_WON` and `SW_ROLAND_GONE`: his departure left
      `SW_RECRUIT` on to keep the "gone" page showing, so this has to come
      after it. It is `story.recruit`'s own returning page - the same join,
      on `SW_KNOWN`, with no second initialise - with a new pitch.
    * **With you**, on `SW_RECRUIT` and `SW_ROLAND_BACK`: walk-through and
      empty, as `recruit`'s own. A roster desk turns `SW_RECRUIT` off and
      he is back at his table.

    He comes back with nothing on: the departure cleared his equipment onto
    the grass. So the join puts his own shield and shirt back on him, from
    the bag if the party has them and new if it has not, into any slot he
    has empty; the swords stay with whoever has them now, and he says so.
    The first rehire also notes whether the sword out of Carn Drey was
    already handed over at the door (`q_roland._after_the_door`)."""
    first = S.narrate([
        "Roland is at his table by the fire, in his shirtsleeves,",
        "with nothing to polish."])
    first += S.say("Roland", ["Finished? Marvellous.",
                              "I've never been in the bit after.",
                              "Is it nice?"])
    first += R.if_then(R.condition_switch(db.SW_ROL5_DONE),
                       S.say("Roland", [
                           "Miss Penhallow walked all this way",
                           "to tell me how it ends. She told me",
                           "all of it, in order."]) +
                       S.say("Roland", ["Then she asked me again whose",
                                        "prophecy it was."]) +
                       S.narrate(["He still does not know."]))
    first += S.say("Roland", ["If you're going on, I'd come.",
                              "I'll want a sword. I left both of",
                              "mine with you, if you remember."])
    again = S.say("Roland", ["Back again? Marvellous.",
                             "Still between engagements.",
                             "I'm no good at it."])
    pitch = R.if_then(R.condition_switch(db.SW_ROLAND_BACK), again, first)
    accept = S.say("Roland", ["Splendid. I'll fetch the armour."])
    accept += S.narrate(["It is still polished."])
    decline = S.say("Roland", ["Quite right. I'll be here,",
                               "between engagements. I'm told",
                               "it's restful."])
    full = S.say("Roland", ["Full! Good. I'll be here,",
                            "between engagements."])
    dress = [
        "const a = $gameActors.actor(%d);" % db.ROLAND,
        "for (const id of [%d, %d]) {" % (db.AR_KITE_SHIELD, db.AR_CHAIN),
        "  const it = $dataArmors[id], s = a.equipSlots().indexOf(it.etypeId);",
        "  if (s < 0 || a.equips()[s]) continue;",
        "  if ($gameParty.hasItem(it)) a.changeEquip(s, it);",
        "  else a.forceChangeEquip(s, it);",
        "}"]
    after = R.if_then(R.condition_switch(db.SW_ROLAND_BACK, False),
                      R.if_then(R.condition_switch(db.SW_ROL2_DONE),
                                [R.control_switch(db.SW_DRAWN_LEFT, True)]))
    after += R.script(dress)
    after += [R.control_switch(db.SW_ROLAND_BACK, True)]
    built = S.recruit(0, db.ROLAND, "Roland", 0, 0, sheet, index,
                      pitch=[], accept=[], decline=[], full=[], after=after,
                      again=dict(pitch=pitch, accept=accept, decline=decline,
                                 full=full))
    table = built["pages"][1]
    table["conditions"] = R.page([], conditions=dict(
        WON, switch2Valid=True, switch2Id=db.SW_ROLAND_GONE))["conditions"]
    with_you = R.page([], img=R.image(""), trigger=0, priority=1,
                      through=True,
                      conditions={"switch1Valid": True,
                                  "switch1Id": db.SW_RECRUIT[db.ROLAND],
                                  "switch2Valid": True,
                                  "switch2Id": db.SW_ROLAND_BACK})
    return [table, with_you]


# ===================================================================== P4c ==
# The amended account, Quy and Hollowell (POSTGAME.md 6 and 8).
WON_B = dict(WON, selfSwitchValid=True, selfSwitchCh="B")


def account_event(event_id, x, y, account):
    """The lectern in Prophecy Hall (Map 3): nothing before the ending; after
    it, "THE OBLIGATORY QUEST, as amended". `account` is
    `journey.tally(amended=True)`, the finale's own tally read against the
    game as it stands, so a quest finished in the post-game shows up here
    and nowhere else, and so do its tropes and blushes."""
    c = S.narrate([
        "A lectern by the door, which was not there last week.",
        "On it, a ledger in the Committee's best hand, open at",
        "the first page, with a pen on a chain beside it."])
    c += account
    return R.event(event_id, "The Amended Account", x, y, [
        R.page([], img=R.image(""), trigger=0, priority=0, through=True),
        R.page(c, img=R.image(LECTERN_SHEET, 0, direction=2), trigger=0,
               priority=1, direction_fix=True, conditions=WON),
    ])


# ------------------------------------------------------------ Halbert Quy --
def _afternoon(intro):
    """Telling Quy what Grimspite said. The tally has already narrated this
    ("all of it, in order, including the part about the tea. It took most of
    an afternoon."), so the scene says what the tally says, and no more."""
    c = list(intro)
    c += S.narrate([
        "You tell him what Grimspite said, all of it, in order,",
        "including the part about the tea."])
    c += [R.fadeout_screen(), R.wait(60), R.fadein_screen()]
    c += S.narrate(["It takes most of an afternoon."])
    cup = S.say("Halbert Quy", ["What was it like?"])
    cup += S.narrate(["You tell him that it was just tea."])
    cup += S.say("Halbert Quy", ["Just tea.", "Thirty years."])
    cup += S.narrate(["He fills the kettle and puts it on, and gets down",
                      "two cups."])
    none = S.narrate(["When you have finished, he sits for a while with",
                      "his hands flat on the table."])
    none += S.say("Halbert Quy", [
        "Thank you. Somebody had to listen",
        "to the whole of it.",
        "I'm glad it was one of us."])
    c += R.if_then(R.condition_switch(db.SW_GRIMSPITE_TEA), cup, none)
    c += [R.control_switch(db.SW_MET_QUY, True), R.self_switch("B", True)]
    return c


def quy_pages(dress):
    """Halbert Quy's pages after the ending (`south.quy_event`), appended
    over his three: met and sent north (`SW_MET_QUY`), the afternoon the
    tally promised; met only after the ending, the same afternoon from his
    "You want to know what he's like", because Bram has already met him; and
    then his own line from the first visit, and the cottage next door.

    `SW_MET_QUY` is set by the afternoon either way, so the amended account
    prints Quy's paragraph for anybody who has sat through it."""
    sent = S.narrate([
        "Halbert Quy looks up from the kitchen table, sees who",
        "it is, and puts the trowel down."])
    sent += S.say("Halbert Quy", ["Forty-eight. You went up.",
                                  "Well. Sit down. Tell me."])
    unsent = S.say("Halbert Quy", ["You want to know what he's like."])
    unsent += S.narrate(["You have met him. You say so."])
    unsent += S.say("Halbert Quy", ["...Have you, now. Sit down.",
                                    "Tell me."])
    after = S.say("Halbert Quy", ["Forty-eight. Sit down, you're",
                                  "blocking the light."])
    after += R.if_then(R.condition_switch(db.SW_COTTAGE_SEEN), S.say(
        "Halbert Quy", [
            "You've been in Ambrose's, then.",
            "Next door. He watered that pot every",
            "morning for as long as I knew him.",
            "Nothing grew then, either."]))
    return [
        _like(dress, _afternoon(unsent),
              dict(WON, selfSwitchValid=True, selfSwitchCh="A")),
        _like(dress, _afternoon(sent),
              dict(WON, switch2Valid=True, switch2Id=db.SW_MET_QUY)),
        _like(dress, after, WON_B),
    ]


# ----------------------------------- Hollowell, the Former Premises (Map 42) --
NOTICE = [
    "\\C[14]NOTICE OF TERMINATION\\C[0]",
    "The Engagement is concluded. The Premises are",
    "released from retention. No further action is",
    "required."]


def hollowell_pages(dress, tour, upto):
    """Mr Hollowell after the ending (`premises.hall_events`): the notice of
    termination has come in the post, and he has filed it, and he has nothing
    else to file. A party that has never been gets the tour as far as the
    visitors' book and the notice in place of the rest - the incumbent it
    would have asked them to find is gone, so the slip is never handed over
    and `SW_VISITORS_BOOK` still means the book was signed at the top of the
    tower."""
    met = S.narrate([
        "Mr Hollowell is at the lectern with a letter. It has",
        "been read a great many times since breakfast."])
    met += S.say("Hollowell", ["Visitors! Oh, it's you. Come and",
                               "look at this. It came in the post."])
    new = list(tour[:upto]) + [S.trope()]
    new += S.say("Hollowell", ["And THIS came in the post, this",
                               "very morning. Come and look."])
    notice = S.narrate(NOTICE)
    notice += S.say("Hollowell", [
        "No further action. I've filed it.",
        "Under N, for Notice, and under T,",
        "and under C, in case. That took me",
        "until about half past nine."])
    notice += S.narrate(["He looks round the hall. It is very clean."])
    notice += S.say("Hollowell", [
        "I've nothing else to file.",
        "Four thousand eight hundred years,",
        "and that's the file."])
    notice += R.if_then(R.condition_switch(db.SW_VISITORS_BOOK), S.say(
        "Hollowell", [
            "But the book's got one in it now.",
            "One! It's in the record, and nobody",
            "can take it out of the record."]))
    first = R.if_then(R.condition_self_switch("A"), met, new) + notice
    first += [R.self_switch("A", True), R.self_switch("B", True)]
    again = S.say("Hollowell", [
        "Take the lift! Any time you like.",
        "It's still running. I can't think",
        "who would stop it."])
    return [_like(dress, first, WON), _like(dress, again, WON_B)]


def visitors_book_page(dress):
    """The visitors' book (`premises.hall_events`) once Grimspite's slip is
    pasted in: after the ending, with the book asked for. Its own page
    rather than a branch, so the published page stays as it is."""
    c = S.narrate([
        "The visitors' book, open on the lectern. On the first",
        "page, pasted in square and ruled to match, one entry."])
    c += S.narrate([
        "NAME: GRIMSPITE THE INEVITABLE. FROM: HERE.",
        "REMARKS: Never been. Heard marvellous things",
        "about the lift."])
    c += S.narrate([
        "Beside it, face up, the notice of termination, in a",
        "folder of its own."])
    return _like(dress, c, dict(WON, switch2Valid=True,
                                switch2Id=db.SW_VISITORS_BOOK))


# =================================================================== art ==
# The two character sheets `draw_art()` writes. `!$`: an object, one to a
# sheet, so the frame can be any size.
FRAME_SHEET = "!$Hall_Frame"        # 48x48: the forty-eighth frame, empty
LETTER_SHEET = "!$Mat_Letter"       # 48x48: `Inside_C`'s Envelope, on the mat
CHAIR_SHEET = "!$Fitch_Chair"       # 48x96: a chair, from behind
LECTERN_SHEET = "!$Hall_Lectern"    # 48x48: `Table E` with an open book
PORTRAIT_B = 133                    # `Inside_B`'s gilt frame
CHAIR_A = (101, 109)                # `Inside_B`'s `Chair A (Wood)`, 1x2
ENVELOPE = 81                       # `Inside_C`'s `Envelope`
TABLE_E = 123                       # `Inside_B`'s, with the purple cloth
OPEN_BOOK = 324                     # `Inside_C`'s `Open Book A (V)`


def draw_art():
    """Writes `FRAME_SHEET`, `CHAIR_SHEET`, `LETTER_SHEET` and
    `LECTERN_SHEET`. Not part of the data build,
    like `fenmarch.draw_art()`: run this module to redraw them.

    * The frame is `Portrait B`'s gilt frame with nothing in it - the
      canvas painted out to plain board - and a small white card.
    * The lectern (P4c) is `Table E` with `Open Book A` laid on it, the way
      the hall's own tables carry their books on layer 3.
    * The letter is `Inside_C`'s `Envelope`, as it is: a sprite, so that it
      does not lend the mat its blocked passage (`letter_event`).
    * The stock `Chair A` only faces south. Seen from behind, a high-backed
      chair is its back all the way down to the seat rail and then four
      legs, so the planks are carried down over the seat, the front's
      handle slot is painted out, and the whole is put in its own shadow."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..",
                                    "tools", "chargen"))
    import numpy as np
    import png
    game = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    sheet = png.read(os.path.join(game, "img", "tilesets", "Inside_B.png"))
    sheet_c = png.read(os.path.join(game, "img", "tilesets", "Inside_C.png"))

    def tile(tid, sheet=sheet):
        x = ((tid // 128) % 2 * 8 + tid % 8) * 48
        y = ((tid % 256) // 8 % 16) * 48
        return sheet[y:y + 48, x:x + 48].astype(float)

    frame = tile(PORTRAIT_B)
    frame[9:40, 11:37] = (108, 92, 70, 255)          # bare board
    frame[9:11, 11:37] = (84, 70, 52, 255)           # the frame's shadow on it
    frame[26:35, 17:31] = (240, 236, 222, 255)       # the card
    frame[28, 19:29] = (90, 84, 76, 255)
    frame[31, 19:27] = (90, 84, 76, 255)

    front = np.concatenate([tile(CHAIR_A[0]), tile(CHAIR_A[1])])
    chair = np.zeros_like(front)
    chair[0:22] = front[0:22]                   # the crest and the posts
    chair[13:18, 14:34] = front[11, 14:34]      # no handle slot at the back
    chair[22:56] = front[22:56]                 # the planks, carried down
    chair[56:70] = front[36:50]                 # over where the seat was
    chair[70:76] = front[56:62]                 # to the seat rail
    for x0, x1 in [(0, 7), (41, 48)]:           # and then only the legs
        chair[76:88, x0:x1] = front[62:74, x0:x1]
    lit = chair[..., 3] > 0
    chair[lit, :3] *= 0.82

    def one(f, fw, fh):
        out = np.zeros((fh * 4, fw * 3, 4))
        for r in range(4):
            for c in range(3):
                out[r * fh:(r + 1) * fh, c * fw:(c + 1) * fw] = f
        return np.clip(out, 0, 255).round().astype(np.uint8)

    letter = tile(ENVELOPE, sheet_c)
    lectern = tile(TABLE_E)
    book = tile(OPEN_BOOK, sheet_c)
    a = book[..., 3:] / 255.0
    lectern[..., :3] = book[..., :3] * a + lectern[..., :3] * (1 - a)
    lectern[..., 3] = np.maximum(lectern[..., 3], book[..., 3])
    for name, img in [(FRAME_SHEET, one(frame, 48, 48)),
                      (LETTER_SHEET, one(letter, 48, 48)),
                      (CHAIR_SHEET, one(chair, 48, 96)),
                      (LECTERN_SHEET, one(lectern, 48, 48))]:
        path = os.path.join(game, "img", "characters", name + ".png")
        png.write(path, img)
        print("wrote", os.path.normpath(path))


if __name__ == "__main__":
    draw_art()
