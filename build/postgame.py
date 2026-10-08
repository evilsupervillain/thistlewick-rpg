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

import db
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


def rol5_line():
    """ROL-5's candidate, after "...who thinks about this one". Inside the
    `SW_ROLAND_GONE` branch, so it is never read without the line it follows."""
    return R.if_then(R.condition_switch(db.SW_ROL5_DONE), S.narrate([
        "Somebody saw the end of this one. She is sixteen,",
        "and she waited at the door, and she has gone to",
        "tell him how it ends."]))


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
