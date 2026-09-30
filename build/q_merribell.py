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
