"""Merribell's companion quests - `COMPANIONS.md`, her section, and
`QUESTS.md` for the order they are built in.

Nothing here draws a map, and this module imports no place module: the place
modules call in here for pages, and `db.build_common_events` for the one
common event.

MER-2, Fit To Travel (`QUESTS.md` A4)
-------------------------------------
Clause eleven: a Chosen One is certified fit before departure. It has been
done forty-seven times, and Bram's is blank, because he was asleep. She will
now do it. Properly.

* **She finds out at Upper Clanging**, from the pad of works fitness forms on
  the Parish Notices (Map 21, event 9) - a works town prints the form. The
  sign is one page with no switches, so its page 2 needs only Merribell, and
  repeats the notices before it says anything new.
* **Three fetches, all global** (`COMPANIONS.md` 1.1): the blank form
  (`SW_MER2_ASKED`, from the pad), the fish stall's stamped scales at Nether
  Sopping (`SW_MER2_SCALES`, lent to anybody once she has asked - a
  dismissed Merribell does not strand the errand), and a good light, which
  is the lighthouse lit (`SW_LAMP_LIT`), because a lamp is exactly what that
  quest already hands you.
* **The examination is wherever the party is standing**: the blank form is
  a key item used from the menu, and it runs common event 3,
  `examination()`. It needs Merribell, the three fetches and a witness, and
  says which is missing.
* **The witness is whoever is third** - the first member who is neither Bram
  nor Merribell, into `VAR_MER2_WITNESS` - and **the witness is the joke**:
  one branch per companion, each reacting to the same line of dictation.
* **Register A carries the middle, and not one line of it is improper.**
  Three blushes, each once, because the form is spent: the chest, the cough,
  and the witness writing down what they were told to.

MER-4, The Man Who Cannot Stay Down (`QUESTS.md` A7) is at the bottom: pages
for Tobias Frayne's cottage (Map 43), handed out to `frayne.py`.
"""
import copy

import db
import rmmzdata as R
import story as S


def _like(page0, cmds, conditions):
    """A page in exactly another page's dress - image, priority, movement -
    with its own commands and conditions."""
    shaped = R.page(cmds, conditions=conditions)
    page = copy.deepcopy(page0)
    page["list"] = shaped["list"]
    page["conditions"] = shaped["conditions"]
    return page


# ----------------------------------------------------------- the discovery --
def notices_pages(page0):
    """Page 2 of the Parish Notices (Map 21, event 9), for Merribell. `page0`
    is the sign's own page; its notices are read first, so nothing on the
    board changes when she is standing in front of it."""
    notices = page0["list"][:-1]

    found = S.narrate([
        "Under the notices, on a nail, a pad of printed forms:",
        "CERTIFICATE OF FITNESS (WORKS). TAKE ONE."])
    found += S.say("Merribell", [
        "Scales. A good light. A clean",
        "surface. A witness. That's all it",
        "takes, and they print the form."])
    found += S.narrate([
        "She reads it again. Then she turns and looks at you,",
        "the way she looks at a cut she has been told is",
        "nothing."])
    found += S.say("Merribell", ["Bram. Who signed you fit?"])
    found += S.narrate(["You explain that you were asleep."])
    found += S.say("Merribell", [
        "Clause eleven. A Chosen One is",
        "certified fit before departure.",
        "It's been done forty-seven times."])
    found += S.say("Merribell", [
        "I keep every ailment in",
        "Thistlewick in a book, dated.",
        "I've nothing for you. Nobody asked."])
    found += S.narrate([
        "She takes a form off the pad, and folds it once,",
        "exactly."])
    found += S.say("Merribell", [
        "Right. Properly. Scales first -",
        "the fish stall at Nether Sopping",
        "has the only stamped ones going."])
    found += S.say("Merribell", [
        "A good light: Bother's, at the",
        "lighthouse, lit. A witness: one",
        "of us. The surface I'll see to."])
    found += [R.gain_item(db.IT_FITNESS_FORM, 1),
              R.control_switch(db.SW_MER2_ASKED, True), S.trope()]
    found += S.got(["Got \\I[186]\\C[3]Certificate of Fitness (Blank)\\C[0].",
                    "Use it when she has everything. She will say."])

    again = S.narrate(["The pad of forms is one lighter."])

    return [_like(page0, notices + R.if_then(
        R.condition_switch(db.SW_MER2_ASKED), again, found),
        {"actorValid": True, "actorId": db.MERRI})]


# -------------------------------------------------------------- the scales --
def stall_pages(page0):
    """Page 2 of the fish stall (Map 13, event 10), once she has asked: the
    scales are lent, once, to whoever asks - and after that it is the stall
    it always was."""
    stall = page0["list"][:-1]

    lend = S.narrate([
        "You ask the merchant whether you could borrow the",
        "scales, for a medical examination."])
    lend += S.say("Merchant", [
        "My scales. The stamped ones.",
        "For a medical."])
    lend += S.narrate(["You explain that it is you being examined."])
    lend += S.say("Merchant", [
        "Right. They go up to twenty stone",
        "and they've never once lied, so",
        "mind what you ask them."])
    lend += S.narrate([
        "They are handed over wrapped in sacking, still",
        "faintly of haddock."])
    lend += [R.gain_item(db.IT_SCALES, 1),
             R.control_switch(db.SW_MER2_SCALES, True)]
    lend += S.got(["Got \\I[208]\\C[3]The Fishmonger's Scales\\C[0].",
                   "Stamped. Twenty stone. Haddock."])

    return [_like(page0, R.if_then(
        R.condition_switch(db.SW_MER2_SCALES), stall, lend),
        {"switch1Valid": True, "switch1Id": db.SW_MER2_ASKED})]


# --------------------------------------------------------- the examination --
WITNESS_OF = ("$gameParty.members().map(a => a.actorId())"
              ".find(i => i !== %d && i !== %d) || 0" % (db.BRAM, db.MERRI))


def _witnesses():
    """One branch per companion who can be the witness. Each is the same
    line of dictation, written down nine different ways, and each is a
    blush - once, because only one of them ever runs."""
    w = {}

    w[db.HOB] = S.narrate([
        "Hob writes it down in capitals, slowly, with his",
        "tongue out."])
    w[db.HOB] += S.say("Hob", ["How's inguinal spelled?"])
    w[db.HOB] += S.narrate(["Merribell spells it."])
    w[db.HOB] += S.say("Hob", [
        "Spell it again. It's going on a",
        "form. He's got to live with it."])

    w[db.ZEPH] = S.narrate([
        "Zephyrine writes it in a beautiful Collegium hand,",
        "and then adds something at the bottom."])
    w[db.ZEPH] += S.say("Zephyrine", [
        "A footnote. 'Both sides,'",
        "independently observed. It",
        "matters who saw what."])

    w[db.NIX] = S.narrate([
        "Nix writes it in the ledger first, from habit, and",
        "then on the form."])
    w[db.NIX] += S.say("Nix", [
        "Item: inguinal, clear. Item: the",
        "other, also clear. Provenance:",
        "Bram. Dated."])

    # COMPANIONS.md: "Sir Aldric's is the funniest thing in this document."
    # The arms are a knight rampant regardant - facing the wrong way.
    w[db.ALDRIC] = S.narrate([
        "Sir Aldric is not where you left him. At some point,",
        "without being asked, he has stepped between you and",
        "the rest of the world with his cloak held out at arm's",
        "length, like a man shielding a lady at a ford."])
    w[db.ALDRIC] += S.narrate([
        "He is facing resolutely the other way. It is the",
        "family way."])
    w[db.ALDRIC] += S.say("Merribell", ["Aldric. You're the witness."])
    w[db.ALDRIC] += S.say("Aldric", [
        "And I witness all of it. I am",
        "witnessing it very hard. From",
        "this side."])
    w[db.ALDRIC] += S.say("Merribell", ["You haven't seen any of it."])
    w[db.ALDRIC] += S.say("Aldric", [
        "Madam, no Pemberton-Gore has",
        "ever seen anything. We have been",
        "attesting to it for two hundred",
        "years."])
    w[db.ALDRIC] += S.narrate([
        "He signs the form behind his back, without turning",
        "round. It is the neatest signature on it."])

    w[db.PIPER] = S.say("Piper", [
        "'And lo, the medic bade him",
        "cough, and the Chosen One",
        "coughed, and -'"])
    w[db.PIPER] += S.say("Merribell", ["Piper."])
    w[db.PIPER] += S.say("Piper", ["It scans."])
    w[db.PIPER] += S.narrate([
        "She writes it down with the metre in. The Committee",
        "will strike it. She knows, and writes it anyway."])

    w[db.CORVIN] = S.narrate([
        "Corvin writes it down as though it were somebody's",
        "last words."])
    w[db.CORVIN] += S.say("Corvin", [
        "If he does not come back, I will",
        "remember this. Both sides. Clear."])
    w[db.CORVIN] += S.narrate([
        "You would very much prefer that he did not."])

    w[db.WREN] = S.narrate(["Wren writes it down, and then keeps writing."])
    w[db.WREN] += S.say("Wren", [
        "Adult male, well-nourished, in",
        "good condition. Entirely typical",
        "of the type. I've added a scale."])
    w[db.WREN] += S.narrate([
        "There is a small scale bar drawn in the margin. You",
        "do not ask what of."])

    w[db.ROLAND] = S.say("Roland", [
        "Clear, both sides. Genuinely",
        "well done, Bram. You should be",
        "proud of that."])
    w[db.ROLAND] += S.narrate([
        "He means it. He claps you on the shoulder. You would",
        "like to be anywhere else, including the tower."])

    c = []
    for actor_id, cmds in w.items():
        c += R.if_then(R.condition_variable(db.VAR_MER2_WITNESS, actor_id),
                       cmds + [S.blush()])
    return c


def _the_examination():
    """The middle, which is Register A from end to end and never improper:
    she is a medic, she is thorough, and she says what she is doing."""
    c = S.narrate([
        "Merribell looks round for a clean surface. There is",
        "not one, anywhere, in the whole of wherever this is."])
    c += S.narrate([
        "She makes one, with a cloth and something out of a",
        "brown bottle that takes the varnish off."])
    c += S.say("Merribell", [
        "Witness, stand there. You're",
        "signing to what you see, so see",
        "all of it. That's the job."])
    c += S.say("Merribell", ["Height."])
    c += S.narrate([
        "She stands you against the nearest upright thing",
        "and marks it with a pencil."])
    c += S.say("Merribell", ["Weight."])
    c += [R.play_se("Equip1"), R.wait(30)]
    c += S.narrate(["You stand on the fishmonger's scales. They consider",
                    "it."])
    c += S.say("Merribell", [
        "Eleven stone four. Or a large",
        "halibut and most of a cod.",
        "I'll put the stone."])
    c += S.say("Merribell", ["Eyes. Follow the light."])
    c += S.narrate([
        "She holds up a lamp lit off Bother's, and moves it",
        "left, and right, and watches you the whole time."])
    c += S.say("Merribell", ["Good. Ears. Throat. Say ah."])
    c += S.narrate(["You say ah. It goes on longer than you meant."])

    c += S.say("Merribell", ["Shirt off. Chest."])
    c += S.narrate([
        "She listens with the cold end of something, in four",
        "places, front and back, with the concentration of",
        "somebody reading a very good letter."])
    c += S.say("Merribell", ["Breathe in. Hold it. Out."])
    c += S.say("Merribell", [
        "Chest: unremarkable. That's a",
        "compliment. It's the best word",
        "we've got."])
    c += [S.blush()]

    c += S.say("Merribell", [
        "Nearly done. Last bit. Turn your",
        "head, and cough."])
    c += [R.wait(20)]
    c += S.narrate([
        "You turn your head. You cough. Nobody anywhere in",
        "the world says anything at all, for some time."])
    c += S.say("Merribell", ["Inguinal: clear. Both sides."])
    c += [S.blush()]
    c += S.say("Merribell", [
        "Witness, write that down.",
        "Exactly as I said it."])
    c += _witnesses()

    c += S.say("Merribell", ["Feet."])
    c += S.narrate([
        "Forty-seven Chosen Ones walked north, and not one of",
        "them had their feet looked at. She looks at yours for",
        "a long time."])
    c += S.say("Merribell", [
        "Socks. Two pairs, dry, and a",
        "spare. It's in the rule. It's",
        "one of the four lines."])
    c += S.narrate([
        "She signs it. The witness signs it. She blows on it",
        "and holds it up to the light, and for a moment she",
        "is completely happy."])
    c += S.say("Merribell", [
        "Fit to travel. There. Now if you",
        "fall off anything, it's on record",
        "that you were fine before."])
    c += S.narrate([
        "The scales go back to Nether Sopping by the carrier,",
        "in their sacking, with a note."])
    c += [R.gain_item(db.IT_FITNESS_FORM, -1), R.gain_item(db.IT_SCALES, -1),
          R.gain_item(db.IT_CERTIFICATE, 1), R.play_me("Item")]
    c += S.got(["Got \\I[191]\\C[3]Certificate of Fitness\\C[0].",
                "It does nothing. It is enormously official."])
    c += [R.control_switch(db.SW_MER2_DONE, True)]
    c += S.companion_story(db.MERRI)
    return c


def examination():
    """Common event 3, run from the blank form wherever the party is. Each
    missing thing is named by Merribell, in the order she would fetch it."""
    no_witness = S.say("Merribell", [
        "And a witness. Not me, and not",
        "the patient. Clause eleven is",
        "very clear."])
    no_lamp = S.say("Merribell", [
        "A good light first. Bother's, at",
        "the lighthouse. Lit."])
    no_scales = S.say("Merribell", [
        "Scales first. The fish stall at",
        "Nether Sopping. Stamped ones."])
    no_medic = S.narrate([
        "The form wants a medic. Merribell's name is already",
        "in the box at the bottom, in pencil, waiting."])

    ready = [R.control_variable_script(db.VAR_MER2_WITNESS, WITNESS_OF)]
    ready += R.if_then(R.condition_variable(db.VAR_MER2_WITNESS, 0),
                       no_witness, _the_examination())
    lit = R.if_then(R.condition_switch(db.SW_LAMP_LIT), ready, no_lamp)
    weighed = R.if_then(R.condition_item(db.IT_SCALES), lit, no_scales)
    return R.if_then(R.condition_actor_in_party(db.MERRI), weighed, no_medic)


# ======================================================================
# MER-4, The Man Who Cannot Stay Down (`QUESTS.md` A7)
# ----------------------------------------------------------------------
# Tobias Frayne (Map 43, `frayne.py`) has been revived eleven times in thirty
# years by people going that way anyway. Merribell will not raise him a
# twelfth time, and cures him of adventurers the only way it can be done,
# which is by leaving.
#
# * **The scene is Tobias's page 3**, on his own self switch A (the end of
#   his two-page pair) and Merribell. It pays out of the jar - it says FOR
#   WHOEVER IS GOING THAT WAY, and they are - and sets `SW_MER4_TOLD`.
# * **The cure is the door.** The cottage's exit tile gains a page on
#   `SW_MER4_TOLD` that finishes the quest the first time the party walks
#   out of it, and then transfers exactly as page 1 does.
# * **Afterwards is for everybody**: Tobias with the parish to tea, the rung
#   mended badly, the jar empty and **the twelfth line left empty**.
JAR_PAYOUT = 1100               # a hundred for every one of the eleven


def _tobias_told():
    c = S.say("Tobias", [
        "Visitors! And a Sister, look.",
        "I'll just pop up the ladder, shall I,",
        "while the kettle's on?"])
    c += S.say("Merribell", ["You will not."])
    c += S.narrate([
        "She has his wrist before he has reached the ladder,",
        "and is counting."])
    c += S.say("Merribell", ["Pulse, good. Colour, good.",
                             "Collarbone, set four times."])
    c += S.say("Merribell", ["Coccyx, set twice, by a paladin.",
                             "Beautifully, I'll give him that."])
    c += S.say("Tobias", ["He was ever so gentle about it."])
    c += S.narrate([
        "Bram looks at the ceiling. There is a hatch in it,",
        "and a ladder up to it, and he looks away from that",
        "too."])
    c += [S.blush()]
    c += S.say("Merribell", ["There is nothing wrong with you,",
                             "Mr Frayne. That's the trouble."])
    c += S.narrate([
        "She looks at the book, and at the shelf of tonics",
        "with other people's names on them, and at the",
        "twelfth line, ruled and dated and empty."])
    c += S.say("Merribell", ["I am not going to raise you a",
                             "twelfth time. Nobody is.",
                             "That is the treatment."])
    c += S.say("Tobias", ["But who'll come by?"])
    c += S.say("Merribell", ["The parish. Ask them to tea.",
                             "Through the door. On purpose."])
    c += S.say("Tobias", ["You can do that?"])
    c += S.say("Merribell", ["People do it every day, and",
                             "they don't fall off anything first."])
    c += S.narrate(["He thinks about this for a long time."])
    c += S.say("Tobias", ["Then you'll have the jar."])
    c += S.say("Merribell", ["I will not."])
    c += S.say("Tobias", ["It says for whoever is going",
                          "that way. You're going that way.",
                          "You said."])
    c += S.narrate([
        "He cuts the string with the bread knife and tips it",
        "out on the table: a hundred crowns for every one of",
        "the eleven, put by for thirty years for whoever",
        "would not take it."])
    c += [R.gain_gold(JAR_PAYOUT), R.play_me("Item")]
    c += S.got(["Got \\C[3]%s crowns\\C[0]." % format(JAR_PAYOUT, ",")])
    c += S.say("Merribell", ["...Thank you, Mr Frayne."])
    c += S.say("Merribell", ["Now we leave. That's the",
                             "other half of it."])
    c += [S.trope(), R.control_switch(db.SW_MER4_TOLD, True)]
    return c


def _tobias_going():
    c = S.say("Tobias", ["You're going, then."])
    c += S.say("Tobias", ["Go on. I'll not watch.",
                          "I'll put the kettle on."])
    return c


def _tobias_cured():
    c = S.say("Tobias", ["Visitors! Come in - through the",
                         "door, mind, like people."])
    c += S.say("Tobias", ["I've had the parish to tea.",
                          "Twice. Nobody fell off anything."])
    c += S.say("Tobias", ["Mended the ladder, an' all.",
                          "Not very well. It holds."])
    return c


def tobias_pages(page0):
    """Pages 3-5 for Tobias (Map 43, event 2), in his own page's dress."""
    known = {"selfSwitchValid": True, "selfSwitchCh": "A"}
    return [
        _like(page0, _tobias_told(),
              dict(known, actorValid=True, actorId=db.MERRI)),
        _like(page0, _tobias_going(),
              dict(known, switch1Valid=True, switch1Id=db.SW_MER4_TOLD)),
        _like(page0, _tobias_cured(),
              {"switch1Valid": True, "switch1Id": db.SW_MER4_DONE}),
    ]


def cottage_door_pages(page0):
    """Page 2 of the cottage's exit tile (Map 43, event 1): the first time
    out after the talk is the cure. Then the same way out as page 1."""
    leave = S.narrate([
        "You leave. Behind you the door shuts, and the",
        "kettle goes on, and nobody goes up the ladder."])
    leave += R.if_then(R.condition_actor_in_party(db.MERRI), S.say(
        "Merribell", ["Don't look back. It's part of it."]))
    leave += [R.control_switch(db.SW_MER4_DONE, True)]
    leave += S.companion_story(db.MERRI)
    out = R.if_then(R.condition_switch(db.SW_MER4_DONE, False), leave)
    return [_like(page0, out + page0["list"][:-1],
                  {"switch1Valid": True, "switch1Id": db.SW_MER4_TOLD})]


def jar_pages(page0):
    """Page 2 of the jar (Map 43, event 5), once it has been paid out."""
    return [_like(page0, S.narrate([
        "The jar, empty, the string cut. The label still",
        "says FOR WHOEVER IS GOING THAT WAY."]),
        {"switch1Valid": True, "switch1Id": db.SW_MER4_TOLD})]


def book_pages(page0):
    """Page 3 of the book (Map 43, event 4). The twelfth line stays empty."""
    return [_like(page0, S.narrate([
        "WHEN, WHAT, WHO, REMARKS.",
        "The twelfth line is still empty. The pen has been",
        "capped, and put away in the drawer."]),
        {"switch1Valid": True, "switch1Id": db.SW_MER4_DONE})]


def ladder_pages(page0):
    """Page 2 of the ladder (Map 43, event 3): he mended it himself."""
    return [_like(page0, S.narrate([
        "The ladder up to the hatch. The third rung is new,",
        "fitted by somebody who has never fitted a rung",
        "before, and it holds."]),
        {"switch1Valid": True, "switch1Id": db.SW_MER4_DONE})]


# ======================================================================
# MER-5, The Well at Sump (`QUESTS.md` E1)
# ----------------------------------------------------------------------
# Sump (Map 51, `hamlets.py`) has been cursed since 1794: headaches, short
# tempers, no sleep, and a general sense that things used to be better. The
# well has had a wasps' nest in it for as long, and nobody can say whose job
# the wasps are. Merribell diagnoses it in nine seconds.
#
# * **The start is Mr Thurle's second look.** His first page with Merribell
#   is the published reaction shot - she opens her mouth and is asked to
#   speak through the chair - so the quest is his page 3, on his own self
#   switch A and Merribell: she asks for an item three. The diagnosis is
#   thirst, and the Water Committee is re-formed, one member, with you
#   seconding. `SW_MER5_ON`.
# * **The cure is the obvious thing** (the Creed's rule one): wasps want
#   water and something sweet, and have had the water for two hundred
#   years, so give them something sweet somewhere else. Mrs Pardew has her
#   gran's last jar of jam, 1931, which she will hand to whoever asks once
#   the Committee has sat - Merribell need not be there for that, so a
#   dismissed Merribell does not strand the errand. The jam is an item.
# * **The well is where it is lifted**, with Merribell and the jam, under the
#   parish's Standing Orders for the Lifting of the Curse - drafted 1795 and
#   never used - whose six clauses are every cliche of the cursed village in
#   a row, each met by something smaller. That is the "biggest trope payload
#   in the document": in the telling, and counted **once**.
# * **The rule made literal**: item three is the Order's Rule of Life, four
#   lines, adopted as a by-law, and the parish does it in order.
# * **Afterwards is for everybody**: Mr Thurle, Mr Gammage (asleep), Mrs
#   Pardew, the well, the minutes with an item three, and the sign.
_MER5_RULE = [
    "I.   Drink a glass of water.",
    "II.  Sit down.",
    "III. Dry socks: two pairs, and a spare.",
    "IV.  Then see how you feel."]


def _mer5_agenda():
    c = S.narrate([
        "Merribell plants herself in front of Mr Thurle, exactly",
        "where a chair would be if there were one."])
    c += S.say("Merribell", ["Mr Thurle. Is there an item three?"])
    c += S.say("Mr Thurle", ["There is never an item three.",
                             "There's never time."])
    c += S.say("Merribell", ["There is now. I'll be quick."])
    c += S.narrate([
        "She is. Headaches: everybody. Sleep: nobody. Tempers:",
        "short. A general sense that things used to be better.",
        "Skin like a letter that has been left in a window."])
    c += S.say("Merribell", [
        "Lips cracked. Eyes sunk. I don't",
        "need to ask anybody about their",
        "water. I can tell from here what",
        "colour all of your -"])
    c += S.say("Mr Thurle", ["THROUGH the chair. Please."])
    c += [S.blush()]
    c += S.narrate([
        "There is a short silence in the parish of Sump. Somebody",
        "in the end house closes a window."])
    c += S.say("Mr Thurle", ["...The chair recognises the Sister."])
    c += S.say("Merribell", [
        "When did anybody in Sump last",
        "drink a glass of water?"])
    c += S.narrate([
        "He opens the ledger, and goes back, and goes on going",
        "back, a page at a time, for some while."])
    c += S.say("Mr Thurle", ["...1794."])
    c += S.say("Merribell", [
        "That's not a curse, Mr Thurle.",
        "That's thirst. Six generations",
        "of it."])
    c += S.narrate([
        "He takes his two fingers away from the side of his",
        "head, and looks at them."])
    c += S.say("Mr Thurle", ["It's a very thorough curse."])
    c += S.say("Merribell", ["It's a very thorough thirst."])
    c += S.say("Mr Thurle", [
        "But the wasps. A wasp is the Pound.",
        "A nest is Buildings. And the Water",
        "Committee was wound up -"])
    c += S.say("Merribell", [
        "Then I move that the Water",
        "Committee be re-formed. Have I a",
        "seconder?"])
    c += S.narrate([
        "Everybody looks at you. You second it. It is the first",
        "motion seconded in Sump since 1794, and Mr Thurle has",
        "to look up how it is written down."])
    c += S.say("Mr Thurle", [
        "Carried. The Water Committee of",
        "Sump: one member. Its first",
        "business?"])
    c += S.say("Merribell", ["Wasps."])
    c += S.narrate([
        "He writes WASPS. His pen hovers over the word after it,",
        "the one it has always been, for a long moment."])
    c += S.say("Mr Thurle", ["...Not deferred."])
    c += S.say("Merribell", [
        "Wasps want two things. Water, and",
        "something sweet. They've had the",
        "water for two hundred years."])
    c += S.say("Merribell", [
        "So we give them something sweet,",
        "somewhere else. Has anybody in",
        "Sump got anything sweet?"])
    c += S.say("Mr Thurle", [
        "Mrs Pardew has jam. Her gran's.",
        "She won't open it. She says things",
        "were better when it was made."])
    c += [R.control_switch(db.SW_MER5_ON, True)]
    return c


def _mer5_sitting():
    return S.say("Mr Thurle", [
        "The Water Committee has the floor.",
        "Item: wasps. Not deferred. I keep",
        "writing that, to see how it looks."])


def thurle_pages(page0):
    """Pages 3-4 for Mr Thurle (Map 51, event 3), in his own page's dress:
    the agenda with Merribell, below his ladder; afterwards for everybody."""
    known = {"selfSwitchValid": True, "selfSwitchCh": "A"}
    ask = R.if_then(R.condition_switch(db.SW_MER5_ON), _mer5_sitting(),
                    _mer5_agenda())
    after = S.say("Mr Thurle", [
        "Item one, the curse: lifted. Item",
        "two, the wasps: removed, to the end",
        "of the spit. Item three: the Rule."])
    after += S.narrate([
        "He has his hat off, and both hands free, and no fingers",
        "pressed to anything. There was time."])
    return [
        _like(page0, ask, dict(known, actorValid=True, actorId=db.MERRI)),
        _like(page0, after,
              dict(known, switch1Valid=True, switch1Id=db.SW_MER5_DONE)),
    ]


def pardew_pages(page0):
    """Pages 3-4 for Mrs Pardew (Map 51, event 5). `page0` is her own last
    page, which page 3 carries whole: the jam is handed to whoever asks once
    the Committee has sat, Merribell or not."""
    known = {"selfSwitchValid": True, "selfSwitchCh": "A"}
    own = page0["list"][:-1]
    jam = S.narrate([
        "You tell her the Water Committee would like something",
        "sweet. She looks at you for a long time."])
    jam += S.say("Mrs Pardew", [
        "It's my gran's. Gooseberry. 1931.",
        "Things were better when it was",
        "made. It says so on the label."])
    jam += S.narrate([
        "It does. In a careful hand under GOOSEBERRY 1931 it says",
        "(BETTER). She gives it to you with both hands."])
    jam += [R.gain_item(db.IT_JAM, 1), R.play_me("Item")]
    jam += S.got(["Got \\I[179]\\C[3]Mrs Pardew's Jam\\C[0]."])
    give = own + R.if_then(
        R.condition_switch(db.SW_MER5_DONE, False),
        R.if_then(R.condition_item(db.IT_JAM), [], jam))
    after = S.say("Mrs Pardew", [
        "You can talk to me before noon now.",
        "Not after. That's just me."])
    after += S.say("Mrs Pardew", ["Things are better.",
                                  "It's in the minutes."])
    return [
        _like(page0, give,
              dict(known, switch1Valid=True, switch1Id=db.SW_MER5_ON)),
        _like(page0, after,
              dict(known, switch1Valid=True, switch1Id=db.SW_MER5_DONE)),
    ]


def gammage_pages(page0):
    """Page 3 for Mr Gammage (Map 51, event 4): his own last page, and then
    he is."""
    after = page0["list"][:-1] + S.narrate([
        "And then, quite suddenly, he is. He snores like a man",
        "making up for six generations."])
    return [_like(page0, after, {
        "selfSwitchValid": True, "selfSwitchCh": "A",
        "switch1Valid": True, "switch1Id": db.SW_MER5_DONE})]


def _mer5_orders():
    """The Standing Orders for the Lifting of the Curse, 1795, never used:
    every cliche of the cursed village, one clause each."""
    c = S.say("Mr Thurle", [
        "Before the Committee proceeds. The",
        "Standing Orders for the Lifting of",
        "the Curse. Drafted 1795. Never yet",
        "used."])
    c += [R.play_me("Curse1")]
    c += S.say("Mr Thurle", ["One. A Chosen One shall be present."])
    c += S.narrate(["You are. He writes PRESENT, and underlines it."])
    c += S.say("Mr Thurle", ["Two. The guardian of the well",
                             "shall be overcome."])
    c += [R.play_se("Wind7", 60, 150)]
    c += S.narrate([
        "The hum in the well changes key. Something small and",
        "striped comes up, tastes the air, and sets off down the",
        "spit towards the jam. Then all of them do."])
    c += S.narrate([
        "It takes about four minutes and it is extremely loud.",
        "Nobody is stung. Nobody had ever asked them to leave."])
    c += S.say("Mr Thurle", ["Three. An ancient relic shall",
                             "be given up."])
    c += S.say("Mrs Pardew", ["Gooseberry. 1931."])
    c += S.narrate(["It is being very well received at the end of the spit."])
    c += S.say("Mr Thurle", ["Four. A price shall be paid, in",
                             "sorrow."])
    c += S.say("Mrs Pardew", ["...It was the last jar."])
    c += S.narrate(["Everybody is quiet, respectfully, for about a second."])
    c += S.say("Mr Thurle", ["Five. The eldest shall speak",
                             "the riddle."])
    c += S.narrate(["Mr Gammage opens one eye."])
    c += S.say("Mr Gammage", [
        "What's wet, and in the middle of",
        "the village, and we've not had any",
        "since 1794?"])
    c += S.say("Merribell", ["Water."])
    c += S.say("Mr Gammage", ["Took us six generations, that one."])
    c += S.say("Mr Thurle", ["Six. The curse shall be called by",
                             "its true name."])
    c += S.say("Merribell", ["Thirst."])
    c += S.narrate([
        "He writes it down. The pen does not go through the",
        "paper."])
    return c


def _mer5_cure():
    c = S.narrate([
        "Merribell takes the jar to the very end of the spit,",
        "past the sign, where the sand runs down to the sea. She",
        "opens it, and leaves it in the sun, and comes back."])
    c += S.narrate([
        "Mr Thurle comes over with the ledger. Mrs Pardew comes",
        "out to see what is being done with her jam. Mr Gammage",
        "does not come over, but he is listening."])
    c += _mer5_orders()
    c += [R.gain_item(db.IT_JAM, -1)]
    c += S.narrate([
        "The well is quiet. Merribell takes a coil of rope and a",
        "tin cup out of her bag, because of course she has a coil",
        "of rope and a tin cup in her bag, and lets it down."])
    c += [R.play_se("Water1"), R.wait(30)]
    c += S.narrate([
        "It comes up full: clear and cold, and only very slightly",
        "wasp-flavoured."])
    c += S.say("Merribell", ["Item three. Through the chair."])
    c += S.say("Mr Thurle", ["...The chair recognises the Sister."])
    c += S.say("Merribell", [
        "The Rule of Life of my order.",
        "Mother Ursula Pym, 1702. Four",
        "lines. Adopt it as a by-law."])
    c += S.narrate(_MER5_RULE)
    c += S.say("Mr Thurle", ["Seconded?"])
    c += S.narrate(["You second it. You are getting good at this."])
    c += S.say("Mr Thurle", ["Carried."])
    c += S.narrate([
        "So the parish of Sump does it, by law, in order. It",
        "drinks a glass of water, one cup at a time, down the",
        "street and back. It sits down, in the street."])
    c += S.narrate([
        "It looks to its socks, which in Sump are dry, and always",
        "have been: the one line of the four nobody here has ever",
        "had any trouble with. Then it sees how it feels."])
    c += [R.tint_screen([17, 17, 0, 0], 60), R.play_me("Inn1")]
    c += S.narrate([
        "Mr Thurle takes his hat off. Mrs Pardew says \"Oh.\"",
        "Mr Gammage is asleep, sitting up against the wall,",
        "properly, for the first time since Tuesday."])
    c += [R.tint_screen([0, 0, 0, 0], 60)]
    c += S.say("Merribell", [
        "That's the whole of my order.",
        "Four lines. One's about socks.",
        "It works."])
    c += S.say("Mr Thurle", [
        "Item one. The curse. Lifted, 2000.",
        "There's time for an item four, if",
        "anybody has one."])
    c += S.narrate(["Nobody has. It is wonderful."])
    c += [S.trope(), R.control_switch(db.SW_MER5_DONE, True)]
    c += S.companion_story(db.MERRI)
    return c


def well_pages(page0):
    """Pages 2-3 of the well (Map 51, event 6), which has no ladder: the
    Committee at work while it sits, and the well afterwards, for everybody.
    The cure needs Merribell and the jam, and says which is missing."""
    absent = page0["list"][:-1] + S.narrate([
        "The Water Committee is not present. The wasps carry on,",
        "unminuted."])
    no_jam = S.say("Merribell", [
        "Water, and something sweet. They",
        "have the water. Somebody in Sump",
        "has something sweet."])
    work = R.if_then(R.condition_actor_in_party(db.MERRI),
                     R.if_then(R.condition_item(db.IT_JAM), _mer5_cure(),
                               no_jam),
                     absent)
    after = S.narrate([
        "The parish well: a good round stone head, with a rope on",
        "it now, and a tin cup on the rope."])
    after += S.narrate([
        "Down the spit, in the sun, a great many wasps are being",
        "extremely happy about a jam jar."])
    return [
        _like(page0, work, {"switch1Valid": True,
                            "switch1Id": db.SW_MER5_ON}),
        _like(page0, after, {"switch1Valid": True,
                             "switch1Id": db.SW_MER5_DONE}),
    ]


def minutes_pages(page0):
    """Page 2 of the minutes (Map 51, event 7): there is an item three."""
    after = page0["list"][:-1] + S.narrate(
        ["2000. Item 3: The Rule. Carried, and done, in order:"] +
        _MER5_RULE[:3])
    after += S.narrate([_MER5_RULE[3], "",
                        "Under it, in the same hand: Felt better."])
    return [_like(page0, after, {"switch1Valid": True,
                                 "switch1Id": db.SW_MER5_DONE})]


def sign_pages(page0):
    """Page 2 of the fingerpost (Map 51, event 8): its own page, and a new
    line painted under the old one."""
    after = page0["list"][:-1] + S.narrate([
        "Under it, in fresh paint: Lifted 2000.   Please Mind",
        "The Well. (Rule Of Life Applies.)"])
    return [_like(page0, after, {"switch1Valid": True,
                                 "switch1Id": db.SW_MER5_DONE})]


# ======================================================================
# MER-1, The Sisterhouse (`QUESTS.md` E2)
# ----------------------------------------------------------------------
# The mother house has split. Whatever Works has the west half of the ward
# and soup; What Ought To Work has the east half, a doctrine and the correct
# treatment in eleven stages. The Prioress holds symposia, and knows what
# that means. It is settled the way this world settles things: a queue.
#
# * **The start is the Prioress's second look.** Her first page with
#   Merribell is the published "We'll talk. Not today." - so the talk is her
#   page 3, on her own self switch A and Merribell. The disappointment is
#   the other way round: she stayed for the symposia. Merribell proposes the
#   queue instead of the eleventh symposium; Sister Bewick agrees, in
#   writing, off the page. `SW_MER1_ON`.
# * **The queue is outside**, in the drizzle, up the track: six of the forty
#   are events on Map 54 (13-18), empty before and after, while it waits.
# * **The contest is the same page**, "Begin / Not yet", with Merribell and
#   the queue waiting. Sir Hamo keeps the score from the bed on the line,
#   because both orders treat him and he is very fair. Four patients come to
#   Merribell with a choice each - the Rule's four lines plus the question
#   she always asks - and a point each for the obvious thing
#   (`VAR_MER1_POINTS`); sixteen more go through in a paragraph. Sister
#   Bewick gets through one, and he really has the Weeping Bottom ague, and
#   stage eleven works: one point, honestly given. **Whatever Works wins on
#   points.** One blush, in the paragraph; one trope.
# * **The Pamphlet** is the Order's founding document, Mother Ursula Pym's,
#   four pages; Sister Bewick asks to be examined on it, which is how a
#   doctrine is settled, and passes. The Prioress gives Merribell the
#   founder's own copy: her gear (`QUESTS.md` 0.5), armour 45 of a new type.
# * **Afterwards for everybody**: the Prioress, Sister Bewick and the line.
#   The chapel is left alone for ALD-2.
_MER1_PATIENTS = [
    # (who, complaint lines, the right answer's index, right, wrong)
    ("A carter", [
        "A carter, grey in the face, holding his head as if it",
        "might come off. He has driven since five this morning,",
        "with the window down, in the rain, and nothing to drink."],
     0, ["She hands him her flask. He drinks the lot, and",
         "blinks, and his face comes back to the right colour."],
     ["He looks at her. He holds his head a little tighter. She",
      "gives him her flask anyway, and he drinks the lot."]),
    ("A shepherdess", [
        "A shepherdess who has walked in from the hill, through",
        "the bog, and stands in the queue squelching. She has a",
        "cough and two blisters and a very cross expression."],
     2, ["Merribell takes a pair out of her bag. The shepherdess",
         "changes them on the spot, and the cross expression goes."],
     ["The shepherdess squelches. Merribell looks down, sighs at",
      "herself, and gets a dry pair out of her bag."]),
    ("A clerk", [
        "A thin clerk who has stood in the queue since before it",
        "was a queue, four hours, and is now quietly going the",
        "colour of his paper, and leaning."],
     1, ["She puts a stool under him just as his knees go. He sits.",
         "He is fine. He says he has never been better."],
     ["He leans further. Merribell catches him on the way down",
      "and sits him on a stool, where he is fine."]),
    ("A small boy", [
        "A small boy, with his mother, who says he has been",
        "impossible since ten o'clock and something must be wrong",
        "with him. He is crying about a sock."],
     3, ["The answer is no, not since breakfast. Sister Lamb brings",
         "soup. The boy stops crying about the sock in mid-word."],
     ["The boy cries louder. Merribell asks whether he has eaten,",
      "which is what she should have asked, and he has not."]),
]
_MER1_CHOICES = ["Drink some water", "Sit down", "Dry socks",
                 "Have you eaten?"]
MER1_REST = 16                  # the sixteen who go through in a paragraph


def _mer1_talk():
    c = S.say("Prioress", [
        "Sister. We'll talk. It's today,",
        "now, and I know it is."])
    c += S.narrate([
        "She takes Merribell to the window on the west side, out",
        "of the way of the line."])
    c += S.say("Prioress", [
        "You left at twenty-two. You said",
        "we'd started holding symposia, and",
        "you'd come to look after people."])
    c += S.say("Merribell", [
        "I'm sorry, Prioress. I know you",
        "were disappointed."])
    c += S.say("Prioress", [
        "I was. Not in you. I stayed for the",
        "symposia. Eleven of them. I chair",
        "them very well."])
    c += S.narrate([
        "Merribell does not say anything. It is the kindest thing",
        "she could have said."])
    c += S.say("Prioress", [
        "The eleventh is at three. Whether",
        "Anything Works. It will be referred",
        "to the twelfth."])
    c += S.say("Merribell", [
        "There's a queue at the gate. I",
        "saw it coming down. Forty, and more",
        "coming up the track."])
    c += S.say("Merribell", [
        "Don't hold the symposium. Open the",
        "door. Twenty patients each half,",
        "and whoever's through first is right."])
    c += S.narrate([
        "The Prioress looks at her for a long time. Then she",
        "laughs, once, which nobody on either side of the ward",
        "has heard her do."])
    c += S.say("Prioress", [
        "Sister Bewick will want it in",
        "writing. Sister Bewick will want",
        "it in writing IMMEDIATELY."])
    c += S.narrate([
        "She does. She writes it, in eleven clauses, and signs it,",
        "and puts it in volume three. Somebody unlocks the gate."])
    c += [R.control_switch(db.SW_MER1_ON, True)]
    return c


def _mer1_patient(n, who, lines, right, yes, no):
    """One of the four: their complaint, Merribell's choice, a point for the
    obvious thing."""
    c = S.narrate(lines)
    c += S.narrate(["%s. Merribell looks at them for about a second." % (
        ["The first", "The second", "The third", "The fourth"][n])])
    branches = []
    for i in range(len(_MER1_CHOICES)):
        if i == right:
            b = S.narrate(yes) + [R.control_variable_add(db.VAR_MER1_POINTS, 1)]
            b += S.say("Sir Hamo", ["Point to the west!"])
        else:
            b = S.narrate(no)
            b += S.say("Sir Hamo", ["...Point withheld. Very fair."])
        branches.append(b)
    c += R.choice_block(_MER1_CHOICES, branches)
    return c


def _mer1_contest():
    c = [R.fadeout_screen()]
    c += S.narrate([
        "The gate is opened. The queue comes in out of the",
        "drizzle, steaming, and divides at the line: twenty to the",
        "west, twenty to the east, by the toss of a bedpan."])
    c += [R.fadein_screen()]
    c += S.narrate([
        "Sir Hamo keeps the score from the bed on the line,",
        "since both orders treat him and he is very fair. He has",
        "a slate, and a cough, and he is having a wonderful time."])
    c += S.say("Sister Bewick", [
        "Patient one. Stage one: the",
        "history. Begin with the",
        "grandparents."])
    c += S.say("Merribell", ["Next!"])
    c += [R.control_variable(db.VAR_MER1_POINTS, 0)]
    for n, (who, lines, right, yes, no) in enumerate(_MER1_PATIENTS):
        c += _mer1_patient(n, who, lines, right, yes, no)
    c += S.narrate([
        "Then the next sixteen, at a pace: a sprain, a fright, a",
        "wasp sting, a man who has been told he is dying and has",
        "only been reading the wrong almanac."])
    c += S.narrate([
        "She tells a farmer, at full volume, across the whole",
        "ward, exactly where his hernia is and what he is to stop",
        "lifting. He thanks her. So does the ward."])
    c += [S.blush()]
    c += [R.control_variable_add(db.VAR_MER1_POINTS, MER1_REST)]
    c += S.say("Sir Hamo", [
        "That's the west half through!",
        "Twenty! Somebody find out how",
        "the east is getting on."])
    c += S.narrate([
        "The east is on patient one, stage eleven. Every bed but",
        "one has nineteen patients sitting on it, waiting, very",
        "politely, with the history of their grandparents taken."])
    c += S.say("Sister Bewick", [
        "Stage eleven. The patient",
        "will now feel better."])
    c += S.narrate([
        "Patient one is a fisherman called Mr Grebe, who has the",
        "Weeping Bottom ague, properly, the first case anybody",
        "has seen in nine years. He sits up. He feels better."])
    c += S.say("Sister Bewick", ["...It worked."])
    c += S.say("Merribell", [
        "Of course it worked. He had it.",
        "That's a point to the east, Sir",
        "Hamo. Fair's fair."])
    c += S.say("Sir Hamo", [
        "Whatever Works, \\V[%d]. What" % db.VAR_MER1_POINTS,
        "Ought To Work, one. On points!",
        "Very fair."])
    c += S.narrate([
        "Nineteen patients get up off the east beds and walk",
        "across the line, the way they always do at night, except",
        "that it is the afternoon, and nobody minds."])
    c += S.say("Sister Bewick", [
        "Then it is settled. I should",
        "like to be examined on your",
        "doctrine. That is how a doctrine",
        "is settled."])
    c += S.say("Merribell", ["We haven't got one. We've got",
                             "a pamphlet."])
    c += S.say("Prioress", [
        "We have got one. Mother Ursula's",
        "own. It's been in the drawer since",
        "the first symposium."])
    c += S.narrate([
        "Four pages, stitched, damp at the corners. The Rule of",
        "Life is on the first page. Sister Bewick reads it, all",
        "four lines, twice, and is examined on it, and passes."])
    c += S.say("Sister Bewick", [
        "It is very short.",
        "I can find nothing wrong with it.",
        "That is very annoying."])
    c += S.say("Prioress", [
        "Keep it, Sister. It works better",
        "out of a drawer. Everything does."])
    c += [R.gain_armor(db.AR_PAMPHLET, 1), R.play_me("Item")]
    c += S.got(["Got \\C[3]The Pamphlet\\C[0]."])
    c += S.narrate([
        "There is no symposium at three. There is soup, on both",
        "sides of the line. Sister Bewick has some. She writes in",
        "her notebook: Intervention. Supported."])
    c += [S.trope(), R.control_switch(db.SW_MER1_DONE, True)]
    c += S.companion_story(db.MERRI)
    return c


def _mer1_waiting():
    c = S.say("Prioress", [
        "The queue's in. Sister Bewick has",
        "her history forms out. Are you",
        "ready, Sister?"])
    c += R.choice_block(["Begin", "Not yet"], [
        _mer1_contest(),
        S.say("Merribell", ["A minute. I want to wash",
                            "my hands. Twice."])])
    return c


def stope_pages(page0):
    """Pages 3-4 for the Prioress (Map 55, event 2), in her own page's
    dress: the talk and the contest with Merribell, below her ladder; and
    afterwards, for everybody."""
    known = {"selfSwitchValid": True, "selfSwitchCh": "A"}
    ask = R.if_then(R.condition_switch(db.SW_MER1_ON), _mer1_waiting(),
                    _mer1_talk())
    after = S.say("Prioress", [
        "No symposium at three. Soup at",
        "noon, and the queue at two. Bring a",
        "chair. People sit down now."])
    after += S.say("Prioress", ["It's in the rule."])
    return [
        _like(page0, ask, dict(known, actorValid=True, actorId=db.MERRI)),
        _like(page0, after,
              dict(known, switch1Valid=True, switch1Id=db.SW_MER1_DONE)),
    ]


def bewick_pages(page0):
    """Page 3 for Sister Bewick (Map 55, event 3): her own last page, plus
    the pamphlet she keeps in volume three."""
    after = page0["list"][:-1] + S.narrate([
        "There is a pamphlet in volume three now, as a bookmark,",
        "at chapter nine. She has read it eleven times."])
    return [_like(page0, after, {
        "selfSwitchValid": True, "selfSwitchCh": "A",
        "switch1Valid": True, "switch1Id": db.SW_MER1_DONE})]


def line_pages(page0):
    """Page 2 of the line (Map 55, event 8): its own page, and the minutes
    of a symposium that was not held."""
    after = page0["list"][:-1] + S.narrate([
        "The eleventh has been added, in the Prioress's hand: Not",
        "held. A queue instead. Whatever Works, on points. Soup."])
    return [_like(page0, after, {"switch1Valid": True,
                                 "switch1Id": db.SW_MER1_DONE})]


# The last six of the forty, who are on Map 54, in the drizzle, up the track:
# (name, (sheet, index), what they say). Strangers, so stock sprites.
MER1_QUEUE = [
    ("Number Thirty-Five", ("People1", 4), [
        "Thirty-five. Chest. It's the air.",
        "I came for the air."]),
    ("Number Thirty-Six", ("People2", 3), [
        "Thirty-six! I'm not ill. Mum said",
        "to queue, so I'm queueing."]),
    ("Number Thirty-Seven", ("People1", 6), [
        "Thirty-seven. Knee. It'll keep.",
        "It's kept since Michaelmas."]),
    ("Number Thirty-Eight", ("People4", 1), [
        "Thirty-eight. They say there's soup",
        "on the one side and a book on the",
        "other. I'm hoping for soup."]),
    ("Number Thirty-Nine", ("People4", 4), [
        "Thirty-nine. Don't know what I've",
        "got. That's why I'm in a queue."]),
    ("Number Forty", ("People1", 2), [
        "Forty. Last. Somebody's always",
        "last. Wet, an' all."]),
]


def queue_events(base_id, cells, people):
    """Events `base_id`.. on Map 54: the end of the queue, standing in the
    drizzle while `SW_MER1_ON` and gone home once it is done. `people` is
    [(name, (sheet, index), lines)], one per cell."""
    evs = []
    for i, ((x, y), (name, img, lines)) in enumerate(zip(cells, people)):
        waiting = S.say(name, lines, face=False)
        waiting += R.if_then(R.condition_actor_in_party(db.MERRI), S.narrate([
            "Merribell looks along the queue the way a general looks",
            "along a line, and very nearly smiles."]))
        evs.append(R.event(base_id + i, name, x, y, [
            R.page([], img=R.image(""), trigger=0, priority=0, through=True),
            R.page(waiting, img=R.image(img[0], img[1], direction=8),
                   trigger=0, priority=1,
                   conditions={"switch1Valid": True,
                               "switch1Id": db.SW_MER1_ON}),
            R.page([], img=R.image(""), trigger=0, priority=0, through=True,
                   conditions={"switch1Valid": True,
                               "switch1Id": db.SW_MER1_DONE}),
        ]))
    return evs
