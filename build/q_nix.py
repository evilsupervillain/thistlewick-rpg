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
    c += S.say("Bagshawe", ["Eight feet of tube. Folded.",
                            "Nobody has ever complained."])
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
    offer = ask + R.choice_block(
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
