"""Nix's companion quests - `COMPANIONS.md`, her section, and `QUESTS.md` for
the order they are built in.

Nothing here draws a map, and this module imports no place module: the place
modules call in here for pages.

NIX-4, The Longest Loan (`QUESTS.md` A9)
----------------------------------------
Everything in the Emporium was owned by somebody Nix can name. Eleven things
have been in the ledger since the beginning with nothing in the RETURNED
column, and this is the afternoon they go back: three towns, eleven owners,
every one of them delighted and none of them aware it had gone. Two try to
pay. One gives Nix something better, and the whole thing starts again - which
is how the shop got its stock in the first place, and is stated nowhere.

* **It starts at the ledger** (Map 7, event 4), with Nix, once the party has
  been to Upper Clanging - so every owner she names is somebody the player
  has already met. She hands over the eleven as **one item, eleven of it**:
  the count in the bag is what is left to return, and `VAR_NIX4_RETURNED`
  is what has gone back.
* **Each owner gets two appended pages.** The return needs the goods and Nix,
  on top of whatever the owner's own last page needs - their terminal self
  switch A, for the ones who have a short version - so the ladder always runs
  first. Afterwards is self switch B, for everybody, and is **their own last
  page with one line added**: nobody loses a word of what they said before.
* **A dismissed Nix leaves the goods in the bag.** Nothing about the quest is
  held by a page only she can reach, so it waits, and resumes when she is back.
* **The ledger closes on the eleventh**, and opens a new page on Hulda Bole's
  parcel, which is the something better.
"""
import copy

import db
import rmmzdata as R
import story as S
from places import MAP_SOPPING

RETURNS_ICON = 209
PARCEL_ICON = 208
ELEVEN = 11


def _nix4_ask():
    """The ledger, with Nix: the eleven longest loans, and the afternoon."""
    c = S.narrate([
        "Nix takes the ledger down and turns to the front,",
        "where the hand is worst and the entries oldest."])
    c += S.say("Nix", [
        "Everything in here was owned by somebody,",
        "and I can name every one of them. Most of it",
        "I've sold on since, and written down to whom."])
    c += S.say("Nix", [
        "Eleven things I never did. They've been in",
        "the book since the first page. The longest",
        "loans I've got."])
    c += S.narrate(["You ask whether they were loans."])
    c += S.say("Nix", [
        "Everything's a loan, eventually.",
        "That's what the RETURNED column is for."])
    c += S.narrate([
        "The RETURNED column has been ruled, very neatly,",
        "down eleven years of pages. There is nothing in it."])
    c += S.say("Nix", [
        "Here: your mother's pie dish. The old",
        "man's chair. The fisher's keep net.",
        "The gate key."])
    c += S.say("Nix", [
        "Nether Sopping: the ferryman's tide table,",
        "the councillor's spectacles, Tolly's stamps",
        "and Hulda Bole's good boots."])
    c += S.say("Nix", [
        "Clanging: Old Sowerby's snap tin, a",
        "small oil can for the Hoyle Works, and a",
        "cradle for Bessie Marsden.",
        "One afternoon. Easy."])
    c += S.narrate(["It will not be one afternoon."])
    c += [S.trope(),
          R.gain_item(db.IT_RETURNS, ELEVEN), R.play_me("Item"),
          R.control_switch(db.SW_NIX4_BEGUN, True)]
    c += S.got(["Got \\I[%d]\\C[3]Previously Owned Goods\\C[0] x%d." %
                (RETURNS_ICON, ELEVEN)])
    return c


def _nix4_counting():
    """The ledger while the goods are out: how many are back."""
    c = S.say("Nix", ["\\V[%d] of eleven back." % db.VAR_NIX4_RETURNED,
                      "The column's filling up."])
    c += R.if_then(R.condition_item(db.IT_RETURNS), S.say("Nix", [
        "The rest are in the bag, labelled.",
        "Here, Nether Sopping, and up in Clanging."]))
    return c


def _nix4_closing():
    """The eleventh is back. The book is closed, and a page is opened."""
    c = S.narrate([
        "Nix opens the ledger at the last page and, with a",
        "ruler, writes RETURNED eleven times down the column."])
    c += S.say("Nix", [
        "Eleven. None of them knew it had gone,",
        "and every one of them was pleased to see",
        "it back. Two of them tried to pay."])
    c += S.say("Nix", ["That's the book closed."])
    c += S.narrate([
        "A double line under the last entry, the way it is",
        "done, and blotted. Nix sits and looks at it for a",
        "while, and you get the impression that nobody has",
        "ever seen this book finished before, Nix included."])
    c += [R.wait(30)]
    c += S.narrate([
        "Then over the page, to a clean one, and Hulda Bole's",
        "parcel out of the bag, and a line at the top, in a",
        "hand that has had eleven years of practice:"])
    c += S.narrate([
        "  ACQUIRED. One parcel, brown paper, unaddressed.",
        "  From H. Bole, the Slain Wyvern, who was the legs.",
        "  On behalf of a client not yet identified."])
    c += S.say("Nix", ["That's how it starts."])
    c += [R.gain_item(db.IT_PARCEL, -1),
          R.control_switch(db.SW_NIX4_DONE, True), R.play_me("Fanfare1")]
    c += S.companion_story(db.NIX)
    return c


def _nix4_closed():
    return S.narrate([
        "A ledger. The last page of it is ruled off: eleven",
        "lines, and RETURNED against every one of them.",
        "Over the page there is one new entry, in the same",
        "hand, for a parcel in brown paper. It begins again."])


def ledger_pages(page0):
    """Four pages for the Emporium's ledger (Map 7, event 4), which had one
    and no switches. `page0` is its own page, so it looks the same."""
    nix = {"actorValid": True, "actorId": db.NIX}

    def pg(cmds, conds):
        new = R.page(cmds, conditions=conds)
        return dict(copy.deepcopy(page0), list=new["list"],
                    conditions=new["conditions"])

    return [
        pg(_nix4_ask(), dict(nix, switch1Valid=True,
                             switch1Id=db.SW_NORTH)),
        pg(_nix4_counting(), dict(nix, switch1Valid=True,
                                  switch1Id=db.SW_NIX4_BEGUN)),
        pg(_nix4_closing(), dict(nix, switch1Valid=True,
                                 switch1Id=db.SW_NIX4_BEGUN,
                                 variableValid=True,
                                 variableId=db.VAR_NIX4_RETURNED,
                                 variableValue=ELEVEN)),
        pg(_nix4_closed(), {"switch1Valid": True,
                            "switch1Id": db.SW_NIX4_DONE}),
    ]


# -- the eleven -------------------------------------------------------------
# Each is (scene, afterwards): the scene is the return, with Nix; afterwards is
# one narrated line put on the end of the owner's own last page.

def _mother():
    c = S.narrate([
        "Nix puts a pie dish on the table: enamel, with a",
        "blue rim, and opens the ledger at a ribbon."])
    c += S.say("Nix", ["One pie dish. Off your sill, cooling.",
                       "Eleven years ago this June."])
    c += S.say("Mother", ["That's not mine."])
    c += S.say("Nix", ["Ledger says it is."])
    c += S.narrate([
        "She turns it over. Her own name is scratched into",
        "the bottom of it, in capitals, in her own hand."])
    c += S.say("Mother", ["...So it is. I never missed it."])
    c += S.say("Mother", ["Was the pie any good?"])
    c += S.say("Nix", ["The pie's not in the ledger.",
                       "The pie was a separate matter."])
    c += S.say("Mother", ["It was a good pie, that."])
    c += S.say("Nix", ["It was a very good pie."])
    return c, ["The blue-rimmed pie dish is back on the sill,",
               "with a pie in it, cooling. She is watching it."]


def _old_man():
    c = S.narrate(["Nix sets down a kitchen chair with a rush seat."])
    c += S.say("Nix", ["One chair. From outside your door.",
                       "Eleven years."])
    c += S.say("Old Man", ["I don't sit. I stand here."])
    c += S.say("Nix", ["You stand here because I had the chair."])
    c += S.narrate([
        "He considers this for a long time. Then he sits",
        "down on it, very slowly, and shuts his eyes."])
    c += S.say("Old Man", ["Oh, that's better."])
    c += S.say("Old Man", ["I'll wait sat down, then.",
                           "For the lad. That's better."])
    return c, ["He is sitting down now, on a kitchen chair.",
               "It is better for waiting."]


def _fisher():
    c = S.say("Nix", ["One keep net. Yours. Off this bank."])
    c += S.say("Fisher", ["A keep net."])
    c += S.narrate(["He looks at the pond, which has no fish in it."])
    c += S.say("Fisher", ["Never needed one."])
    c += S.say("Nix", ["That's why I located it.",
                       "Nobody was using it."])
    c += S.say("Fisher", ["...I'll need it now, though.",
                          "Man with a keep net's got to catch",
                          "something. Stands to reason."])
    c += S.narrate([
        "He puts it in the water with enormous ceremony. It",
        "is the most optimistic thing you have ever seen."])
    return c, ["The keep net is in the water, and empty. It is",
               "somehow less empty than the pond was."]


def _gatekeeper():
    c = S.say("Nix", ["One key. Iron. Large. The gate's."])
    c += S.say("Gatekeeper", ["The gate's got a key?"])
    c += S.say("Nix", ["It had. It was in the lock.",
                       "I've had it eleven years."])
    c += S.narrate([
        "He looks at the gate, which has stood open for as",
        "long as anybody can remember, and then at the key."])
    c += S.say("Gatekeeper", ["Forty-seven of them through there,",
                              "and not one ever had to knock."])
    c += S.narrate([
        "He hangs the key on a nail beside the gate, where",
        "it will be very safe."])
    return c, ["The key hangs on its nail by the gate.",
               "The gate is open."]


def _ferryman():
    c = S.say("Nix", ["One tide table. Printed. Yours -",
                      "your boat's drawn in the margin."])
    c += S.say("Ferryman", ["Never had a tide table."])
    c += S.say("Nix", ["You had one the week you bought the",
                       "boat. I've had it since the week after."])
    c += S.narrate([
        "He reads it. He looks at the water.",
        "He reads it again."])
    c += S.say("Ferryman", ["Tide's right today."])
    c += S.narrate(["He looks at the water again, for some time."])
    c += S.say("Ferryman", ["...Says here."])
    c += S.narrate(["He holds out a penny: the fare."])
    c += S.say("Ferryman", ["What do I owe you?"])
    c += S.say("Nix", ["It's yours. You can't pay me for your",
                       "own tide table. There isn't a column."])
    return c, ["He has the tide table open on his knee, and is",
               "giving it a few more days."]


def _dree():
    c = S.say("Nix", ["Spectacles. Reading. Left on this bar,",
                      "and nobody came for them all week."])
    c += S.say("Dree", ["I have never owned spectacles.",
                        "That was rather the point of the",
                        "whole business."])
    c += S.narrate([
        "He puts them on anyway, and looks round the Slain",
        "Wyvern properly, possibly for the first time."])
    c += S.say("Dree", ["Good heavens. Is that what",
                        "everybody looks like?"])
    c += S.narrate([
        "At the next table, somebody who has been watching",
        "his eyes for eleven years stops, very slightly."])
    c += S.say("Dree", ["My eyes are entirely ordinary now.",
                        "I shall miss being suspected.",
                        "Nobody has ever watched me so closely."])
    return c, ["He is wearing spectacles. His eyes are entirely",
               "ordinary, which nobody here has quite accepted."]


def _tolly():
    c = S.say("Nix", ["Stamps. A sheet of forty, off",
                      "the Wyvern's counter. The old rate."])
    c += S.say("Tolly", ["We don't buy them by the sheet.",
                         "We buy them in twos."])
    c += S.say("Nix", ["You bought a sheet once. Eleven years",
                       "ago. I've had it ever since."])
    c += S.narrate(["She counts them. There are forty."])
    c += S.say("Tolly", ["Twenty letters, then. He's worth two."])
    c += S.narrate(["She goes back to her envelope, and it has",
                    "two stamps on it before she has finished."])
    return c, ["She is working through a sheet of forty stamps,",
               "two at a time."]


def _hulda():
    c = S.say("Nix", ["One pair of boots, walking. Your good",
                      "ones. Left outside to air, eleven years",
                      "ago, and I aired them for you."])
    c += S.say("Hulda", ["My good boots?"])
    c += S.say("Hulda", ["I've done four hundred and six jobs",
                         "in the other pair."])
    c += S.say("Nix", ["I know. I wrote them down."])
    c += S.narrate([
        "Hulda Bole looks at Nix's ledger, and Nix looks at",
        "hers. Give or take the handwriting, it is the same",
        "book."])
    c += S.say("Hulda", ["Here, then. You're the legs now."])
    c += S.narrate([
        "From under the bench she gets a parcel in brown",
        "paper and string: the last job, the one where he",
        "had moved, with no note."])
    c += S.say("Hulda", ["No name on it. No address.",
                         "I've had it eleven years, an' all."])
    c += S.say("Nix", ["Client?"])
    c += S.say("Hulda", ["Not identified."])
    c += S.narrate([
        "Nix takes it in both hands, and you can see the",
        "whole thing start again."])
    c += S.say("Nix", ["...That's better than boots."])
    c += [R.gain_item(db.IT_PARCEL, 1), R.play_me("Item")]
    c += S.got(["Got \\I[%d]\\C[3]A Parcel, Unaddressed\\C[0]." % PARCEL_ICON])
    return c, ["She is wearing her good boots. She keeps looking",
               "at them."]


def _sowerby():
    c = S.say("Nix", ["One snap tin. Yours. Came south in a",
                      "carrier's crate nobody claimed, which",
                      "makes it a return and not a location."])
    c += S.say("Sowerby", ["My snap tin."])
    c += S.narrate([
        "He opens it. There is a sandwich in it, eleven",
        "years old, and he regards it with respect."])
    c += S.say("Sowerby", ["Dripping. She always did me dripping."])
    c += S.narrate(["He holds out a rivet."])
    c += S.say("Sowerby", ["For your trouble."])
    c += S.say("Nix", ["Can't. It's yours. It goes in the",
                       "book as returned, not as sold."])
    c += S.say("Sowerby", ["It's a rivet.",
                           "You cannot beat a rivet."])
    c += S.narrate([
        "Nix does not take the rivet. It is the hardest thing",
        "you have seen anybody do all afternoon."])
    return c, ["He has his snap tin on his knee. He has not",
               "opened it again. He knows what is in it."]


def _nib():
    c = S.say("Nix", ["One oil can. The small one."])
    c += S.narrate(["Nib goes very still."])
    c += S.say("Nib", ["There is only one can. There has only",
                       "ever been the big can."])
    c += S.say("Nix", ["There were two. I had the small one."])
    c += S.say("Nib", ["She wants the small can every day.",
                       "I give her the big can every day.",
                       "I thought it was part of the numbering."])
    c += S.say("Nix", ["Was it?"])
    c += S.say("Nib", ["I have decided to believe so."])
    return c, ["The small can is on the bench now, where Miss",
               "Hoyle can reach it without asking."]


def _bessie():
    c = S.say("Nix", ["One cradle. Oak, on rockers. Your",
                      "gran's. You'll have been in it."])
    c += S.say("Bessie", ["Gran's cradle? It went years ago."])
    c += S.say("Nix", ["It went south in a crate. I've been",
                       "keeping it for when it was wanted."])
    c += S.narrate([
        "Bessie looks at the cradle, and then at Nix, and",
        "goes slowly and completely red."])
    c += S.say("Bessie", ["Nobody has said anything."])
    c += S.say("Nix", ["Nobody has."])
    c += S.say("Nix", ["Ahead of schedule. It's what I do."])
    c += [S.blush()]
    return c, ["There is a cradle by the range. Nobody has",
               "mentioned it. Everybody has looked at it."]


OWNERS = {
    "mother": _mother, "old_man": _old_man, "fisher": _fisher,
    "gatekeeper": _gatekeeper, "ferryman": _ferryman, "dree": _dree,
    "tolly": _tolly, "hulda": _hulda, "sowerby": _sowerby, "nib": _nib,
    "bessie": _bessie,
}
assert len(OWNERS) == ELEVEN


def _nix4_back(scene):
    """The end of every return: the goods out of the bag, counted, and a
    word when it is the last of them."""
    return scene + [
        R.gain_item(db.IT_RETURNS, -1),
        R.control_variable_add(db.VAR_NIX4_RETURNED, 1),
        R.self_switch("B", True),
    ] + R.if_then(
        R.condition_variable(db.VAR_NIX4_RETURNED, ELEVEN, 1),
        S.narrate(["That is the eleventh. Nix would like to get",
                   "back to the ledger before it gets dark."]))


def returned(key, ev):
    """Append NIX-4's two pages to an owner's event and hand it back, so a
    place module's hook is one line round the event it already builds."""
    pages = ev["pages"]
    last = pages[-1]
    conds = last["conditions"]
    # The owner's own last page may need self switch A (the short version
    # after the set piece) and nothing else; B is ours.
    assert not (conds["switch1Valid"] or conds["switch2Valid"] or
                conds["variableValid"] or conds["itemValid"] or
                conds["actorValid"]), (key, conds)
    assert conds["selfSwitchCh"] == "A" or not conds["selfSwitchValid"], key
    for p in pages:
        for c in p["list"]:
            assert not (c["code"] == 123 and c["parameters"][0] == "B"), key
    scene, after = OWNERS[key]()
    back = R.page(_nix4_back(scene), conditions=dict(
        {k: v for k, v in conds.items() if k.startswith("selfSwitch")},
        itemValid=True, itemId=db.IT_RETURNS, actorValid=True,
        actorId=db.NIX))
    again = copy.deepcopy(last)
    again["list"] = again["list"][:-1] + S.narrate(after) + again["list"][-1:]
    again["conditions"] = R.page([], conditions={
        "selfSwitchValid": True, "selfSwitchCh": "B"})["conditions"]
    pages.append(dict(copy.deepcopy(last), list=back["list"],
                      conditions=back["conditions"]))
    pages.append(again)
    return ev


# ======================================================================
# NIX-5, Half An Encounter (`QUESTS.md` A10)
# ----------------------------------------------------------------------
# Nix's party ability halves encounters. Enoch Bagshawe has an engagement
# with the Upper Clanging Works Band tonight - their first bassoon - and one
# reed, which took three weeks, and which goes the moment anything so much as
# looks at him. So he has to be got through the Gloamwood at night without a
# single fight, and half an encounter is still an encounter.
#
# * **It starts at the Gloamwood's mouth** (the world map's event there), on a
#   page that needs Nix and the wood cleared - the way out at the north end
#   only opens then. The rest of the page is the mouth's own, so a party that
#   says "not tonight" still gets its "Go in / Think about it".
# * **A fight is detected without touching a troop**: `$gameSystem.
#   battleCount()` goes into `VAR_NIX5_BATTLES` at the mouth, and a parallel
#   event on each of the two wood maps fails the escort the moment the count
#   moves - fleeing counts, since a fight has been had. The far end checks it
#   again, as `QUESTS.md` says it should.
# * **Night is a tint** in place of the wood's usual gloom, for as long as
#   `SW_NIX5_ON` is. Walking back out of the south end abandons it; either way
#   he goes home, and is at the mouth again another night.
NIGHT = [-120, -100, -30, 90]
GLOOM = [-68, -50, -20, 40]       # journey.GLOOM, the wood by day
CLEAR = [0, 0, 0, 0]
FEE = 300


def _nix5_first(page0, code):
    """The first command with `code` in one of journey's own pages, lifted
    out at indent 0 - so a transfer here goes exactly where the page's own
    does, without this module knowing where that is."""
    for c in page0["list"]:
        if c["code"] == code:
            return dict(copy.deepcopy(c), indent=0)
    raise KeyError(code)


def _nix5_ask():
    c = S.narrate([
        "Somebody is sitting on the milestone at the mouth of",
        "the wood, in a good coat, holding a long case upright",
        "between his knees like a man holding a small tree."])
    c += S.say("Bagshawe", ["Enoch Bagshawe. First bassoon.",
                            "The Works Band, at Upper Clanging.",
                            "Tonight. They've never had one."])
    c += S.say("Bagshawe", ["It's a brass band. I'm aware.",
                            "They asked. Nobody asks."])
    c += S.narrate([
        "It is getting dark. The only road north is through",
        "the Gloamwood, and he has been sitting at the edge",
        "of it for some time."])
    c += S.say("Bagshawe", ["The reed took three weeks. If",
                            "anything so much as looks at me, I drop",
                            "the case, and that's the reed, and",
                            "that's that."])
    c += S.narrate(["You ask whether it is heavy."])
    c += S.say("Bagshawe", ["Eight feet of tube. Folded."])
    c += S.say("Bagshawe", ["Mrs Bagshawe says I carry it",
                            "more carefully than I carried her",
                            "over the doorstep. She says it",
                            "every anniversary. She's right."])
    c += S.narrate(["He has gone a little pink."])
    c += S.narrate(["Nix looks at the trees for a while."])
    c += [S.blush()]
    c += S.say("Nix", ["I halve them. Encounters. It's a",
                       "knack. I don't stop them - I halve them."])
    c += S.say("Bagshawe", ["What's half an encounter?"])
    c += S.say("Nix", ["Still an encounter."])
    return c


def _nix5_go(transfer):
    c = S.narrate([
        "Mr Bagshawe stands up, and holds the case against his",
        "chest, and looks at the wood as if it had been rude."])
    c += [R.control_variable_script(db.VAR_NIX5_BATTLES,
                                    "$gameSystem.battleCount()"),
          R.control_switch(db.SW_NIX5_ON, True),
          R.play_se("Move1"), R.tint_screen(NIGHT, 30, True), transfer]
    return c


def _nix5_mothballs():
    """P1 (`QUESTS.md` Part G): the Repel, mentioned every night - a new
    line after either telling, so nothing he said before is changed."""
    assert db.MOTHBALL_STEPS == 50, "he says fifty"
    c = S.say("Bagshawe", ["Mothballs, mind. The Band keeps the",
                           "uniforms in them, and nothing has come",
                           "near the Band in years."])
    c += S.say("Bagshawe", ["Any shop has them. Fifty steps a",
                            "twist, and then you want another twist -",
                            "not straight off. They want airing."])
    c += S.say("Nix", ["Halved and mothballed. Belt and braces."])
    return c


def mouth(ev):
    """NIX-5's page on the Gloamwood's mouth (the world map's event 2), and
    hand the event back. `ev`'s own page is the rest of ours."""
    page0 = ev["pages"][0]
    own = page0["list"][:-1]
    go = _nix5_go(_nix5_first(page0, 201))
    again = S.narrate(["Mr Bagshawe is on the milestone, with the case."])
    again += S.say("Bagshawe", ["Another night. Same reed.",
                                "I've had words with it."])
    again += S.say("Nix", ["Still halving."])
    ask = R.if_then(R.condition_self_switch("A"), again,
                    _nix5_ask() + [R.self_switch("A", True)])
    offer = ask + _nix5_mothballs() + R.choice_block(
        ["Take him through", "Not tonight"],
        [go, S.say("Bagshawe", ["Another night, then.",
                                "They'll start without me. They always",
                                "have. It's a brass band."]) + own])
    cmds = R.if_then(R.condition_switch(db.SW_NIX5_DONE), own, offer)
    new = R.page(cmds, conditions={
        "switch1Valid": True, "switch1Id": db.SW_GLOAMWOOD,
        "actorValid": True, "actorId": db.NIX})
    ev["pages"].append(dict(copy.deepcopy(page0), list=new["list"],
                            conditions=new["conditions"]))
    return ev


def _nix5_failed():
    c = [R.play_se("Break", volume=40, pitch=150), R.wait(20)]
    c += S.narrate([
        "Somewhere behind you there is a small, final sound,",
        "like a very polite sneeze."])
    c += S.say("Bagshawe", ["That's the reed."])
    c += S.say("Bagshawe", ["I'll go back. I know the way back.",
                            "It's forwards I'm no good at."])
    c += S.narrate([
        "He goes, at a brisk walk, into the dark, humming the",
        "second bassoon part of something to keep his spirits",
        "up, and there being no first."])
    c += S.say("Nix", ["...Another night. He'll be on the",
                       "milestone. They always are."])
    c += [R.control_switch(db.SW_NIX5_ON, False),
          R.tint_screen(GLOOM, 30, True)]
    return c


def _nix5_fought():
    return R.condition_script("$gameSystem.battleCount() > "
                              "$gameVariables.value(%d)" % db.VAR_NIX5_BATTLES)


def reed_event(event_id):
    """A parallel event for each of the Gloamwood's two maps: while the
    escort is on, a fight - any fight, won, lost or run from - ends it."""
    return R.event(event_id, "Mr Bagshawe's Reed", 0, 0, [
        R.page([], img=R.image(""), trigger=0, priority=0, through=True),
        R.page(R.if_then(_nix5_fought(), _nix5_failed()), img=R.image(""),
               trigger=4, priority=0, through=True,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_NIX5_ON})])


def way_out(ev):
    """The Gloamwood's south end (Map 9, event 1) while he is with you:
    going back out is going home, and he says so first."""
    page0 = ev["pages"][0]
    back = S.say("Bagshawe", ["Back? Well - it's the way I know."])
    back += [R.control_switch(db.SW_NIX5_ON, False), R.play_se("Move1"),
             R.tint_screen(CLEAR, 30, True), _nix5_first(page0, 201)]
    cmds = S.narrate(["Back out, and take Mr Bagshawe home?"])
    cmds += R.choice_block(["Yes", "No"], [back, []])
    new = R.page(cmds, conditions={"switch1Valid": True,
                                   "switch1Id": db.SW_NIX5_ON})
    ev["pages"].append(dict(copy.deepcopy(page0), list=new["list"],
                            conditions=new["conditions"]))
    return ev


def _nix5_through():
    c = S.narrate([
        "The trees stop. There is a road, and a moon on it,",
        "and a long way off, up the valley, the lights of a",
        "works town."])
    c += S.narrate([
        "Mr Bagshawe stands in the road and looks back at the",
        "Gloamwood, which has not so much as looked at him."])
    c += S.say("Bagshawe", ["Nothing. Not one thing.",
                            "Did you see anything?"])
    c += S.say("Nix", ["Didn't see a thing. That's the knack."])
    c += S.narrate([
        "He opens the case, there in the road, and checks the",
        "reed by moonlight, and plays one long low note on it",
        "for no reason but that he can."])
    c += [R.play_se("Horn", pitch=50, volume=70), R.wait(40)]
    c += S.say("Bagshawe", ["There. Your fee. Three hundred,",
                            "in the envelope, exact."])
    c += S.say("Nix", ["Receipt."])
    c += S.narrate([
        "He writes one on his knee. Nix reads it twice, and",
        "files it, and he goes off up the valley at a pace",
        "that suggests the Works Band has started without him."])
    c += [R.gain_gold(FEE), S.trope(),
          R.control_switch(db.SW_NIX5_ON, False),
          R.control_switch(db.SW_NIX5_DONE, True), R.play_me("Fanfare1")]
    c += S.companion_story(db.NIX)
    return c


def north_out(ev):
    """The Gloamwood's north end (Map 10, event 2) while he is with you: the
    far end, and the check `QUESTS.md` asks for. The rest is the exit's own
    open page, so the party goes out exactly as it always does."""
    open_page = ev["pages"][1]
    own = open_page["list"][:-1]
    cmds = R.if_then(_nix5_fought(), _nix5_failed(), _nix5_through()) + own
    new = R.page(cmds, conditions={
        "switch1Valid": True, "switch1Id": db.SW_GLOAMWOOD,
        "switch2Valid": True, "switch2Id": db.SW_NIX5_ON})
    ev["pages"].append(dict(copy.deepcopy(open_page), list=new["list"],
                            conditions=new["conditions"]))
    return ev


# ======================================================================
# NIX-1, The Client Identifies Themselves (`QUESTS.md` B5)
# ----------------------------------------------------------------------
# A letter, correctly addressed, in Nix's own hand: written at fifteen, to be
# opened at twenty-six, and Nix has been beaten to the joke by a teenager. The
# client wants one item - the ledger's one entry with no provenance - and it
# is a coat, in bond at Great Dunnage, where Nix has not set foot for eleven
# years, for a reason that turns out to be embarrassment rather than crime.
#
# * **NIX-4's parcel is the letter.** Hulda Bole's last job, the one where
#   "he's moved" (her tale in the Slain Wyvern, `south.py`), was also her
#   first: Nix gave it her in 1989, to be delivered at twenty-six to the
#   address given, which Nix had long since left for the Emporium. Hulda
#   assumed a "he"; nobody corrects her. So NIX-1 needs `SW_NIX4_DONE`, the
#   way HOB-4 needs HOB-2: the parcel is opened at the ledger (Map 7 event 4)
#   with Nix, on a page above NIX-4's closed book.
# * **The warehouse door** (Map 61 event 7) refuses Nix twice already; with
#   the ticket it is "...Fine." and the door's own page. Once the coat is out
#   it is just a door.
# * **Mr Tibbs** (Map 64 event 2), below his ladder, with Nix and the ticket:
#   the party of the second part, a speech made from a crate, and eleven years
#   of rent by post sooner than come in and face him. The coat comes out of
#   the wardrobe and it fits. **Nix's gear** (`QUESTS.md` 0.5): body armour
#   of an armour type only Nix's actor can wear, as Wren's badge is.
COAT_ICON = 152
TICKET_ICON = 195


def _nix1_letter():
    c = S.narrate([
        "Nix takes Hulda Bole's parcel down off the shelf, and",
        "turns it over, and goes very still."])
    c += S.say("Nix", ["That's my hand."])
    c += S.narrate([
        "Brown paper, and string, and on the back, small, in a",
        "hand that has not had eleven years of practice yet:",
        "NOT TO BE OPENED UNTIL I AM TWENTY-SIX."])
    c += S.say("Nix", ["...I'm twenty-six."])
    c += S.narrate([
        "Tucked under the string, a docket in Hulda Bole's hand:",
        "JOB 1. ACCEPTED 1989. TO BE DELIVERED WHEN THE CLIENT",
        "IS 26, TO THE ADDRESS GIVEN. And under that, eleven",
        "years later, in capitals: MOVED."])
    c += S.say("Nix", ["Her first job and her last.",
                       "I gave it her. I'd forgotten."])
    c += S.narrate(["Inside there is a letter, and a luggage ticket."])
    c += S.narrate([
        "  Dear Nix. This is the client. You have been wondering.",
        "  I want one thing. It is the first entry in the book,",
        "  the one with no provenance. It is in bond at Great",
        "  Dunnage. The ticket is enclosed. You will have been"])
    c += S.narrate([
        "  avoiding it. Stop it.",
        "  Yours, the party of the second part",
        "  (N., aged fifteen)"])
    c += [R.wait(40)]
    c += S.say("Nix", ["Ahead of schedule. Of me."])
    c += S.narrate([
        "Nix reads it again, and then puts the ledger under one",
        "arm and the ticket in an inside pocket, and does not",
        "say anything else for some time."])
    c += [S.trope(), R.gain_item(db.IT_BOND_TICKET, 1), R.play_me("Item"),
          R.control_switch(db.SW_NIX1_LETTER, True)]
    c += S.got(["Got \\I[%d]\\C[3]Bond No. 1 (Ticket)\\C[0]." % TICKET_ICON])
    return c


def _nix1_ledger():
    """The ledger after the letter, for everybody."""
    done = S.narrate([
        "A ledger, ruled off, and a new page begun. Its first",
        "line has a provenance now, in the same hand: one coat,",
        "COLLECTED, on behalf of the party of the second part."])
    waiting = S.narrate([
        "A ledger, ruled off, and a new page begun. Folded into",
        "the back of it, a letter in a fifteen-year-old's hand."])
    return R.if_then(R.condition_switch(db.SW_NIX1_DONE), done, waiting)


def nix1_ledger_pages(page0):
    """Two pages for the Emporium's ledger, after NIX-4's four: the parcel
    opened, with Nix; and the ledger afterwards, for everybody."""
    def pg(cmds, conds):
        new = R.page(cmds, conditions=conds)
        return dict(copy.deepcopy(page0), list=new["list"],
                    conditions=new["conditions"])
    return [
        pg(_nix1_letter(), {"switch1Valid": True,
                            "switch1Id": db.SW_NIX4_DONE,
                            "actorValid": True, "actorId": db.NIX}),
        pg(_nix1_ledger(), {"switch1Valid": True,
                            "switch1Id": db.SW_NIX1_LETTER}),
    ]


def warehouse_door_pages(ev):
    """The Bonded Warehouse's door (Map 61, event 7), after its own three:
    with the ticket, Nix goes in; once the coat is out, it is a door."""
    pages = ev["pages"]
    own = pages[0]["list"]
    fine = S.say("Nix", ["...Fine."]) + own
    pages.append(dict(copy.deepcopy(pages[2]), list=fine, conditions=R.page(
        [], conditions={"selfSwitchValid": True, "selfSwitchCh": "A",
                        "itemValid": True, "itemId": db.IT_BOND_TICKET,
                        "actorValid": True, "actorId": db.NIX})["conditions"]))
    pages.append(dict(copy.deepcopy(pages[2]), list=copy.deepcopy(own),
                      conditions=R.page([], conditions={
                          "selfSwitchValid": True, "selfSwitchCh": "A",
                          "switch1Valid": True, "switch1Id": db.SW_NIX1_DONE,
                          "actorValid": True, "actorId": db.NIX})["conditions"]))
    return ev


def _nix1_collect():
    c = S.narrate([
        "Mr Tibbs looks up from the Bond Book, and over his",
        "spectacles at Nix, for a long moment."])
    c += S.say("Mr Tibbs", ["Ah. The party of the",
                            "second part."])
    c += S.narrate(["Nix puts the ticket on the desk, face down."])
    c += S.say("Mr Tibbs", ["Eleven years. You stood",
                            "on that crate, there, and made a",
                            "speech."])
    c += S.say("Nix", ["I was fifteen."])
    c += S.say("Mr Tibbs", ["'I shall return for it",
                            "when I am somebody.' I wrote it in",
                            "the margin. It was a good speech."])
    c += S.say("Mr Tibbs", ["And then the rent came by",
                            "post every quarter for eleven years,",
                            "never late, no name."])
    c += S.say("Nix", ["Couldn't come in. Not after the",
                       "speech. You'd have remembered it."])
    c += S.say("Mr Tibbs", ["I did remember it."])
    c += S.narrate([
        "He takes a key off his chain, unlocks the wardrobe,",
        "and lifts out a long coat, dark, well made and much",
        "mended, the best coat a village ever had."])
    c += S.say("Mr Tibbs", ["Whose was it?"])
    c += S.say("Nix", ["My gran's. Left me it. It went down",
                       "to my ankles. I wasn't going to wear it",
                       "till it fit, and I wasn't going to sell",
                       "it, so."])
    c += S.narrate(["Nix puts it on. It fits."])
    c += [R.wait(30)]
    c += S.narrate([
        "Nix opens the ledger at the very first page and, under",
        "the one line in eleven years with no provenance,",
        "writes one, slowly, and blots it."])
    c += S.say("Mr Tibbs", ["No duty owing. Rent paid",
                            "to date. Always was."])
    c += [R.gain_item(db.IT_BOND_TICKET, -1),
          R.gain_armor(db.AR_GRANS_COAT, 1), R.play_me("Fanfare1"),
          R.control_switch(db.SW_NIX1_DONE, True)]
    c += S.got(["Got \\I[%d]\\C[3]Gran's Coat\\C[0]." % COAT_ICON])
    c += S.companion_story(db.NIX)
    return c


def tibbs_pages(last):
    """Two pages for Mr Tibbs (Map 64, event 2), whose ladder is one self
    switch: the collection, with Nix and the ticket; and afterwards, for
    everybody, which is his own last page and a line."""
    collect = R.page(_nix1_collect(), conditions={
        "selfSwitchValid": True, "selfSwitchCh": "A",
        "itemValid": True, "itemId": db.IT_BOND_TICKET,
        "actorValid": True, "actorId": db.NIX})
    after = copy.deepcopy(last)
    after["list"] = after["list"][:-1] + S.narrate([
        "The rent has stopped coming by post. He says he misses",
        "it, a little, every quarter day."]) + after["list"][-1:]
    after["conditions"] = R.page([], conditions={
        "selfSwitchValid": True, "selfSwitchCh": "A",
        "switch1Valid": True, "switch1Id": db.SW_NIX1_DONE})["conditions"]
    return [after, dict(copy.deepcopy(last), list=collect["list"],
                        conditions=collect["conditions"])]


def _done_page(page0, lines):
    page = copy.deepcopy(page0)
    page["list"] = S.narrate(lines) + page["list"][-1:]
    page["conditions"] = R.page([], conditions={
        "switch1Valid": True, "switch1Id": db.SW_NIX1_DONE})["conditions"]
    return page


def wardrobe_page(page0):
    """Bond No. 1 (Map 64, event 3) with the coat collected."""
    return _done_page(page0, [
        "A tall wardrobe, unlocked, and empty. The ticket on the",
        "handle has been crossed through: BOND No. 1. COLLECTED."])


def bond_book_page(page0):
    """The Bond Book (Map 64, event 4) with the coat collected."""
    return _done_page(page0, [
        "The Bond Book. Every entry has a name, a date, a",
        "description and a duty. The first has a name now, in",
        "Mr Tibbs's hand: the party of the second part."])


# ======================================================================
# NIX-2, The Sealed Counting House (`QUESTS.md` B6)
# ----------------------------------------------------------------------
# Great Dunnage sealed its Counting House in 1788 when the key was lost, and
# has run on faith and a memorandum since. It is to be opened formally, by a
# licensed person, with the preamble read in full, and the licence is a form
# nobody has filled in. Nix opens it in nine seconds while the Mayor is still
# reading the preamble. Inside: one chair, and a note in a clerk's hand -
# *we spent it* - and the change, which the Corporation insists you keep,
# because it is not theirs, because apparently nothing is.
#
# * **The opening is the Mayor's** (Map 63 event 2), below his ladder, with
#   Nix. `SW_NIX2_OPEN` turns the Door (event 3) open and walkable for
#   everybody, and puts the Mayor inside, where he goes at once.
# * **The room** is `dunnage.vault_room`, in the lobby's black east
#   (`places.VAULT`): events 6 (the way out), 7 (the Mayor, while he is in
#   there) and 8 (the chair). Only the opening needs Nix; the chair does not.
# * **Form L is never completed.** In law the Counting House is still sealed,
#   and the Town Clerk says so afterwards.
CHANGE = 1788                   # the change, when counted; nobody can explain


def _nix2_opening():
    c = S.narrate([
        "The Mayor looks up from the preamble, and at Nix, and at",
        "Nix's hands, which are out of Nix's pockets."])
    c += S.say("The Mayor", ["Are you, by any",
                             "chance, a licensed person?"])
    c += S.say("Nix", ["I locate things. Doors are things."])
    c += S.say("Town Clerk", ["Form L, sir. Not",
                              "completed."])
    c += S.say("The Mayor", ["Then we shall have",
                             "the preamble while it is. It's ready.",
                             "Thirty-seven and a half minutes."])
    c += S.say("The Mayor", ["AND WHEREAS the",
                             "Corporation of Great Dunnage, being in",
                             "Council assembled, and mindful -"])
    c += S.narrate([
        "Nix walks up to the Door, puts an ear to the lock the",
        "size of a cartwheel, and does something small with two",
        "fingers."])
    c += [R.play_se("Key", 80), R.wait(60), R.play_se("Key", 80, 80),
          R.wait(60)]
    c += S.narrate(["Nine seconds."])
    c += [R.play_se("Open3", 90, 70), R.control_switch(db.SW_NIX2_OPEN,
                                                       True), R.wait(40)]
    c += S.say("The Mayor", ["- mindful of its",
                             "ancient and -"])
    c += S.narrate([
        "The Door of the Counting House stands open for the first",
        "time since 1788. The Mayor looks at it, and then at the",
        "preamble, of which there are thirty-seven minutes left."])
    c += S.say("The Mayor", ["...That was not the",
                             "Opening."])
    c += S.say("Town Clerk", ["No, sir. Form L."])
    c += S.say("The Mayor", ["The Counting House is",
                             "opened informally. The Opening proper",
                             "will follow on completion of Form L."])
    c += S.narrate(["And he goes in, at something close to a run."])
    c += [S.trope()]
    return c


def _nix2_chair():
    c = S.narrate([
        "The room behind the Door is not large. There is one",
        "chair in it, and on the chair a note, and under the",
        "note, very neatly stacked, a little money."])
    c += S.narrate([
        "  WE SPENT IT.",
        "  J. Pocklington, Clerk to the Corporation. 1788."])
    c += S.say("The Mayor", ["...Ah."])
    c += S.say("The Mayor", ["Two hundred and twelve",
                             "years we've been assumed to have",
                             "enough. On the strength of a chair."])
    c += S.narrate([
        "It is, to be fair, a very good chair. He sits down on",
        "it, carefully, as the first Mayor to do so."])
    c += S.narrate([
        "The change comes, when it is counted, to one thousand",
        "seven hundred and eighty-eight crowns, which nobody",
        "can explain."])
    c += S.say("The Mayor", ["Keep it. It isn't",
                             "the Corporation's. The memorandum",
                             "says we have enough."])
    c += R.if_then(R.condition_actor_in_party(db.NIX),
                   S.say("Nix", ["Provenance?"]) +
                   S.say("The Mayor", ["None whatever."]) +
                   S.say("Nix", ["...I'll write it down."]))
    c += S.say("The Mayor", ["I shall read the",
                             "preamble anyway. In full. To the",
                             "chair."])
    c += [R.gain_gold(CHANGE), R.play_me("Fanfare1"),
          R.control_switch(db.SW_NIX2_DONE, True)]
    c += S.got(["Got \\C[3]%d crowns\\C[0], which are nobody's." % CHANGE])
    c += S.companion_story(db.NIX)
    return c


def mayor_pages(last):
    """Three pages for the Mayor (Map 63, event 2), whose ladder is one self
    switch: the opening, with Nix; gone inside while the Door is open and the
    chair not yet found; and afterwards, his own last page and a line."""
    opening = R.page(_nix2_opening(), conditions={
        "selfSwitchValid": True, "selfSwitchCh": "A",
        "actorValid": True, "actorId": db.NIX})
    inside = R.page([], img=R.image(""), priority=0, through=True,
                    conditions={"switch1Valid": True,
                                "switch1Id": db.SW_NIX2_OPEN})
    after = copy.deepcopy(last)
    after["list"] = after["list"][:-1] + S.narrate([
        "He has read the preamble to the chair, in full, twice.",
        "He is down to thirty-six minutes."]) + after["list"][-1:]
    after["conditions"] = R.page([], conditions={
        "selfSwitchValid": True, "selfSwitchCh": "A",
        "switch1Valid": True, "switch1Id": db.SW_NIX2_DONE})["conditions"]
    return [dict(copy.deepcopy(last), list=opening["list"],
                 conditions=opening["conditions"]), inside, after]


def door_page(page0, inside_at):
    """The Door (Map 63, event 3) once it has been opened: open, and the
    way in, for everybody. `inside_at` is (map, x, y)."""
    page = copy.deepcopy(page0)
    page["image"] = dict(page["image"], direction=8)
    new = R.page([R.play_se("Move1"),
                  R.transfer(*inside_at, 8, 0)], conditions={
        "switch1Valid": True, "switch1Id": db.SW_NIX2_OPEN})
    page["list"], page["conditions"] = new["list"], new["conditions"]
    return page


def clerk_page(last):
    """The Town Clerk (Map 63, event 5) afterwards: Form L is still blank."""
    page = copy.deepcopy(last)
    page["list"] = page["list"][:-1] + S.narrate([
        "Form L is still blank. In law, the Counting House has",
        "never been opened."]) + page["list"][-1:]
    page["conditions"] = R.page([], conditions={
        "selfSwitchValid": True, "selfSwitchCh": "A",
        "switch1Valid": True, "switch1Id": db.SW_NIX2_DONE})["conditions"]
    return page


def vault_events(base_id, vault, chair, back_to):
    """The room behind the Door: the way out on its doorway, the Mayor while
    he is in there, and the chair. `back_to` is (map, x, y) in the lobby."""
    x1, y1, x2, y2, door_x = vault
    cx, cy = chair
    out = R.event(base_id, "The Way Out", door_x, y2 + 1, [R.page(
        [R.play_se("Move1"), R.transfer(*back_to, 2, 0)],
        img=R.image(""), trigger=1, priority=0, through=True)])
    mayor_img = R.image("Gen_People6", 0, direction=6)
    mayor = R.event(base_id + 1, "The Mayor (Inside)", cx - 1, cy + 2, [
        R.page([], img=R.image(""), priority=0, through=True),
        R.page(S.say("The Mayor", ["Do look. I'm",
                                   "composing a shorter preamble."]),
               img=mayor_img, conditions={"switch1Valid": True,
                                          "switch1Id": db.SW_NIX2_OPEN}),
        R.page([], img=R.image(""), priority=0, through=True,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_NIX2_DONE}),
    ])
    chair_ev = R.event(base_id + 2, "The Chair", cx, cy + 1, [
        R.page(_nix2_chair(), img=R.image(""), direction_fix=True),
        R.page(S.narrate([
            "One very good chair. On it, a note, in a clerk's hand:",
            "WE SPENT IT. 1788."]), img=R.image(""), direction_fix=True,
            conditions={"switch1Valid": True,
                        "switch1Id": db.SW_NIX2_DONE}),
    ])
    return [out, mayor, chair_ev]


# ================================================================ NIX-3 ==
# Professional Courtesy (`QUESTS.md` E14). Cobb Lorrimer steals things, says
# so, and finds Nix's whole vocabulary - "locates", "ahead of schedule",
# "the client" - insulting. The contest is not a fight: a client, a list and
# an afternoon, and Nix wins on paperwork.
#
# * **Lorrimer is at the Adventurers' Guild** (Map 15 event 7), registered,
#   under T. With Nix he challenges; then he is gone to the front.
# * **The client is Sops and Tibb**, the two children who cannot play Chosen
#   One properly because nobody will be the Dark Lord. Their list: a rope, a
#   helmet, a sword and a Dark Lord (who loses).
# * **Nix locates three with permission**, at three of Nether Sopping's shut
#   doors - the Net Loft's rope, asked for properly at last; the pot at the
#   front door nobody answers, waited for; an oar off one of the eleven
#   boats, offered by the Ferryman, who keeps the key. Each is a page on the
#   door, with Nix and `SW_NIX3_ON`, carrying the door's own page; located
#   is the door's self switch A, counted in `VAR_NIX3_LOCATED`, so a
#   dismissed Nix's count waits.
# * **The judging** is Lorrimer's, by the children (Map 13 event 19): his
#   three are stolen and go back to their owners; Nix's three have receipts.
#   The fourth thing cannot be stolen, so Nix locates it: Lorrimer signs on
#   as Dark Lord, afternoons, and reads (WHO LOSES) a moment too late. He
#   leaves his tools on a barrel, in a huff, which means they were located.
# * **Afterwards for everybody**: Lorrimer on the front, losing better; Sops,
#   her own last page and the Dark Lord who comes in the afternoons now.
TOOLS_ICON = 208


def _nix3_challenge():
    c = S.narrate([
        "A man in a teal hood is leaning on the Guild's wall with",
        "his arms folded, the way a man leans who would like to",
        "be asked what he does."])
    c += S.say("Lorrimer", ["Cobb Lorrimer. Thief.",
                            "Registered. Pell's got me down under T."])
    c += S.say("Lorrimer", ["And you'll be the one",
                            "who LOCATES."])
    c += S.say("Nix", ["I locate things. Ahead of schedule.",
                       "On behalf of a client."])
    c += S.say("Lorrimer", ["LOCATES. AHEAD OF",
                            "SCHEDULE. THE CLIENT. It's stealing",
                            "with a waistcoat on. It's a job you've",
                            "failed to apply for."])
    c += S.say("Nix", ["Nothing in my shop was stolen. I can",
                       "tell you how I got every piece of it."])
    c += S.say("Lorrimer", ["Prove it. There's two",
                            "kids on the front playing Chosen One",
                            "with no kit. I said I'd get it them.",
                            "You get it too. First back with the lot."])
    c += S.narrate([
        "He produces the list, in a child's hand: ONE ROPE. ONE",
        "HELMIT. ONE SWORD. ONE DARK LORD (WHO LOSES)."])
    c += S.say("Lorrimer", ["A client, a list and",
                            "an afternoon. No fighting. I don't",
                            "fight. I'm a professional."])
    c += S.say("Nix", ["So am I."])
    c += S.narrate(["He is out of the door before Nix has finished",
                    "saying it."])
    c += [S.trope(), R.control_switch(db.SW_NIX3_ON, True)]
    return c


def lorrimer_guild(event_id, x, y):
    """Lorrimer at the Guild (Map 15): there with Nix until he has made his
    challenge; then gone to the front, and gone for good afterwards."""
    img = R.image(*S.sprite("Lorrimer"), direction=4)
    blank = R.image("")
    return R.event(event_id, "Cobb Lorrimer (Guild)", x, y, [
        R.page([], img=blank, priority=0, through=True),
        R.page(_nix3_challenge(), img=img,
               conditions={"actorValid": True, "actorId": db.NIX}),
        R.page([], img=blank, priority=0, through=True,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_NIX3_ON}),
        R.page([], img=blank, priority=0, through=True,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_NIX3_DONE}),
    ])


def _nix3_rope():
    c = S.narrate([
        "Nix knocks. A voice from inside, over the nets: 'The",
        "rope is spoken for.'"])
    c += S.say("Nix", ["Who for?"])
    c += S.narrate([
        "'Whoever asks properly. Nobody ever has. They read the",
        "card and go off.'"])
    c += S.say("Nix", ["May I borrow the rope, please, until",
                       "sundown, for two children playing",
                       "Chosen One? I'll write you a receipt."])
    c += S.narrate([
        "A long pause. Then a coil of rope comes out of the",
        "window and lands at Nix's feet, and the voice says,",
        "'Properly.'"])
    c += S.narrate([
        "Nix writes a receipt - ONE ROPE, LENT, UNTIL SUNDOWN -",
        "and pins it under the card."])
    return c


def _nix3_pot():
    c = S.narrate([
        "Nix knocks, and there is no answer, and Nix waits. Nix",
        "is very good at waiting. It is most of locating."])
    c += S.narrate([
        "After about an hour the door opens an inch, on an old",
        "woman who has not been asked anything in years and is",
        "not sure she likes it."])
    c += S.say("Nix", ["The pot. For a helmet. For a child,",
                       "until sundown. I'll take the dead thing",
                       "out of it first."])
    c += S.narrate([
        "'...Keep it,' she says. 'Keep the dead thing an' all.'",
        "Nix takes the pot, leaves the dead thing, and writes a",
        "receipt for both."])
    return c


def _nix3_oar():
    c = S.narrate([
        "Nix does not open the lock, though Nix could, in about",
        "four seconds. The Ferryman, who keeps the key, is",
        "fetched instead, and comes up from the pier."])
    c += S.narrate([
        "He lets them choose an oar off one of the eleven boats.",
        "'Nobody's rowed her since. She'd like being a sword.'"])
    c += S.narrate([
        "Nix writes a receipt - ONE OAR (SWORD), LENT, WITH",
        "THANKS - and the Ferryman folds it into his hat."])
    return c


_NIX3_DOORS = {"rope": _nix3_rope, "pot": _nix3_pot, "oar": _nix3_oar}


def _nix3_count():
    return S.narrate([
        "Nix's list: \\V[%d] of three, with receipts. And one Dark"
        % db.VAR_NIX3_LOCATED,
        "Lord (who loses), still to find."])


def located_page(key, page0):
    """One page on a shut door (Map 13, events 13-15): with Nix while the
    list is out, the door's own page, and then the thing located, once."""
    done = S.narrate(["Nix's receipt is pinned to the door."])
    get = _NIX3_DOORS[key]() + [R.self_switch("A"),
                                R.control_variable_add(db.VAR_NIX3_LOCATED)]
    cmds = page0["list"][:-1] + R.if_then(
        R.condition_self_switch("A"), done, get) + _nix3_count()
    page = copy.deepcopy(page0)
    page["list"] = R.page(cmds)["list"]
    page["conditions"] = R.page([], conditions={
        "actorValid": True, "actorId": db.NIX,
        "switch1Valid": True, "switch1Id": db.SW_NIX3_ON})["conditions"]
    return [page]


def _nix3_judging():
    c = S.narrate([
        "Sops and Tibb sit on a barrel each, as judges. Lorrimer",
        "lays his out first, with a flourish."])
    c += S.say("Lorrimer", ["One rope. Off the ferry.",
                            "One helmet, out of the outfitters'",
                            "window. One sword."])
    c += S.narrate([
        "The sword is the very good one off the knees of the man",
        "having a day off. He has come up the street after it in",
        "his socks, and stands there, still having a day off."])
    c += S.say("Sops", ["Where'd you get them?"])
    c += S.say("Lorrimer", ["I STOLE them. I'm a",
                            "thief. It's the whole point of me."])
    c += S.say("Tibb", ["Mum says we're not to have stolen",
                        "things. She says it twice."])
    c += S.narrate([
        "Nix lays out a coil of rope, a pot and an oar, and on",
        "top of each, a receipt."])
    c += S.say("Sops", ["...This one's got PAPERWORK."])
    c += S.say("Nix", ["Lent until sundown, and signed for.",
                       "The rope was asked for properly. The",
                       "pot was waited for. The oar was offered."])
    c += S.narrate([
        "The ferry, the outfitters and the man in his socks take",
        "their things back off Lorrimer, one at a time, politely.",
        "He watches them go."])
    c += S.say("Lorrimer", ["...You can't win a",
                            "THIEVING contest on PAPERWORK."])
    c += S.say("Nix", ["It wasn't a thieving contest.",
                       "It was a list."])
    c += S.say("Tibb", ["There's one more thing on it."])
    c += S.narrate([
        "ONE DARK LORD (WHO LOSES). Neither child will be it.",
        "Nobody in Nether Sopping will be it. Lorrimer has not",
        "got one. You cannot steal a Dark Lord."])
    c += S.narrate(["Nix takes out a form, and a pen, and turns to",
                    "Lorrimer."])
    c += S.say("Nix", ["Position available. Dark Lord,",
                       "afternoons. Villainous. A proper",
                       "criminal post. You'd be good at it."])
    c += S.say("Lorrimer", ["...Villainous?"])
    c += S.say("Nix", ["Very. Sign here."])
    c += S.narrate([
        "He signs. He reads what he has signed - (WHO LOSES) - a",
        "moment too late, and the children are already running",
        "at him with an oar and a pot on."])
    c += S.narrate([
        "He loses magnificently, three times before sundown,",
        "storms off up the street in a huff, and leaves his",
        "tools on the barrel."])
    c += S.say("Nix", ["Unattended property. Located.",
                       "I'll write him a receipt."])
    c += [R.gain_armor(db.AR_LORRIMER_TOOLS, 1), R.play_me("Item")]
    c += S.got(["Got \\I[%d]\\C[3]Lorrimer's Tools\\C[0]." % TOOLS_ICON])
    # The children's own first pages say nobody will be the Dark Lord, which
    # stopped being true just now: their terminal self switches, by script.
    c += R.script([
        "$gameSelfSwitches.setValue([%d, 9, 'A'], true);" % MAP_SOPPING,
        "$gameSelfSwitches.setValue([%d, 17, 'A'], true);" % MAP_SOPPING])
    c += [R.control_switch(db.SW_NIX3_ON, False),
          R.control_switch(db.SW_NIX3_DONE, True)]
    c += S.companion_story(db.NIX)
    return c


def _nix3_waiting():
    c = S.narrate([
        "Lorrimer is on the front with a rope, a real helmet and",
        "a very good sword at his feet, looking over his",
        "shoulder."])
    c += S.say("Lorrimer", ["Had mine before dinner.",
                            "Where's yours?"])
    return c


def _nix3_front():
    with_nix = R.if_then(R.condition_variable(db.VAR_NIX3_LOCATED, 3, 1),
                         _nix3_judging(), _nix3_waiting())
    without = S.say("Lorrimer", ["Where's your clerk?",
                                 "The one who LOCATES. I'm not doing",
                                 "this twice."])
    return R.if_then(R.condition_actor_in_party(db.NIX), with_nix, without)


def _nix3_after():
    c = S.say("Lorrimer", ["Don't. I signed it. I",
                           "read it after. It's afternoons."])
    c += S.narrate([
        "Cobb Lorrimer, Dark Lord (afternoons), signed for. He has",
        "come back every day since, under protest, and is",
        "getting very good at losing."])
    c += R.if_then(R.condition_actor_in_party(db.NIX), S.say("Lorrimer", [
        "And I want a receipt for my tools."]))
    return c


def lorrimer_front(event_id, x, y):
    """Lorrimer on the front (Map 13), by the children: there while the list
    is out, with the judging; and afterwards, for everybody."""
    img = R.image(*S.sprite("Lorrimer"), direction=4)
    return R.event(event_id, "Cobb Lorrimer", x, y, [
        R.page([], img=R.image(""), priority=0, through=True),
        R.page(_nix3_front(), img=img, conditions={
            "switch1Valid": True, "switch1Id": db.SW_NIX3_ON}),
        R.page(_nix3_after(), img=img, conditions={
            "switch1Valid": True, "switch1Id": db.SW_NIX3_DONE}),
    ])


def sops_page(last):
    """Sops (Map 13 event 9), whose ladder is one self switch: afterwards,
    her own last page and the Dark Lord who comes in the afternoons."""
    page = copy.deepcopy(last)
    page["list"] = page["list"][:-1] + S.narrate([
        "Except in the afternoons, now, when he comes down the",
        "street in a teal hood, under protest, and loses."]) + \
        page["list"][-1:]
    page["conditions"] = R.page([], conditions={
        "selfSwitchValid": True, "selfSwitchCh": "A",
        "switch1Valid": True, "switch1Id": db.SW_NIX3_DONE})["conditions"]
    return [page]
