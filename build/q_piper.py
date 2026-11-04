"""Piper Quill's companion quests - `COMPANIONS.md`, her section, and
`QUESTS.md` for the order they are built in.

Nothing here draws a map, and this module imports no place module: the place
modules call in here for pages, as `village.py` does for the turnip.

PIP-2, A Rhyme For Turnip (`QUESTS.md` A3)
------------------------------------------
She has been looking for one since the recruit scene ("I'll get one on the
road. I always do."). The party helps, and every suggestion is worse than the
last. There is no rhyme for turnip, and any competent poet would have changed
the other line in week one - which she does, in nine seconds, and everybody
who spent the afternoon on it is furious.

* **It happens at the Gilded Turnip, at the turnip.** Map 4, event 6, the
  gilded one on its plinth: one page with no switches, so pages appended
  below it wait on no ladder. Page 1 is untouched and is all a party without
  Piper ever sees.
* **Not before the road.** The pages need `SW_LEFT_VILLAGE` as well as
  Piper, or the scene is available five minutes after she joins, in the
  room she joined in, and "since the recruit scene" is a lie.
* **One branch per companion, not one page.** A page names one actor, and
  this is one scene with whoever is standing there, so it is `if_then` on
  each of the other eight in turn. Bram always has a go, as narration.
* **A trope per suggestion** (`COMPANIONS.md`), and one for the payoff, which
  is the cliche itself. Merribell's is a blush as well.
* **Done is a global switch, `SW_PIP2_DONE`**, for the ending: `SW_STORY
  [PIPER]` will be on after any of her quests.
"""
import copy

import db
import rmmzdata as R
import story as S

# The last verse of the ballad, before and after. The draft ends its second
# line on "turnip" and needs a rhyme for the fourth; the fix moves the turnip
# down a line and ends the second on "grate", which has several.
DRAFT = [
    "'And so he came home to the fields,",
    "and sat down with a single turnip,",
    "and hung his sword above the grate,",
    "and -'",
]
VERSE = [
    "'And so he came home to the fields,",
    "and hung his sword above the grate,",
    "and sat down with a turnip, which",
    "was worth the journey, and the wait.'",
]


def _suggestion(actor_id, cmds):
    """One companion's go, if they are here - and a trope for it."""
    return R.if_then(R.condition_actor_in_party(actor_id),
                     list(cmds) + [S.trope()])


def _afternoon():
    """The suggestions, in the order they are worst. Every one is a branch;
    a party of Bram, Piper and two others hears two of these and Bram's."""
    c = []

    # Hob: "burnip", without embarrassment.
    hob = S.say("Hob", ["Burnip."])
    hob += S.say("Piper", ["That's not a word."])
    hob += S.say("Hob", [
        "It is now. I've made worse out of less.",
        "Beatrice doesn't like it."])
    hob += S.narrate(["Beatrice was always right. Hob stands by it anyway."])
    c += _suggestion(db.HOB, hob)

    # Wren: the whole class of words, inadmissible.
    wren = S.say("Wren", [
        "Before anybody says anything ending",
        "in '-nip': no. A bite, a pinch, or a",
        "catmint. Genus Nepeta. Inadmissible."])
    wren += S.say("Piper", ["Nobody's offered one yet."])
    wren += S.say("Wren", ["Pre-emptively inadmissible."])
    c += _suggestion(db.WREN, wren)

    # Corvin: it scans perfectly, and it is about drowning.
    corvin = S.narrate([
        "Corvin has been staring into the fire. He speaks",
        "without looking up."])
    corvin += S.say("Corvin", [
        "'The water came up through the lane,",
        "and closed above the chapel spire,",
        "and every bell that ever rang",
        "rang once beneath the lake, and -'"])
    corvin += S.narrate(["He stops."])
    corvin += S.say("Piper", [
        "That scans. That scans perfectly.",
        "Where's the turnip?"])
    corvin += S.say("Corvin", ["Drowned."])
    c += _suggestion(db.CORVIN, corvin)

    # Aldric: another language, and it does not rhyme in that one either.
    aldric = S.say("Aldric", [
        "In the old tongue of my house, a",
        "turnip is a 'navet'. Which rhymes,",
        "very beautifully, with -"])
    aldric += S.narrate(["There is a long pause."])
    aldric += S.say("Aldric", [
        "It doesn't. Not in ours either.",
        "I am so sorry. Carry on."])
    c += _suggestion(db.ALDRIC, aldric)

    # Nix: located, ahead of schedule, on behalf of a client.
    nix = S.narrate([
        "Nix produces a folded slip of paper from the back of",
        "the ledger and lays it on the table."])
    nix += S.say("Nix", [
        "One rhyme for 'turnip'. Located in",
        "the spring, ahead of schedule, on",
        "behalf of a client. Provenance",
        "on the back."])
    nix += S.narrate(["Piper unfolds it. It says TURNIP."])
    nix += S.say("Nix", [
        "Client didn't say it had to be a",
        "different word."])
    c += _suggestion(db.NIX, nix)

    # Merribell: the body, top to bottom, at a professional volume.
    merri = S.say("Merribell", [
        "There'll be something anatomical.",
        "There's always something anatomical."])
    merri += S.narrate([
        "She begins at the scalp and works down, aloud, in",
        "order, at the volume of somebody who has never once",
        "found any of it embarrassing."])
    merri += S.narrate([
        "The Gilded Turnip goes quiet somewhere around the",
        "pelvis. You look at the ceiling. The ceiling has",
        "never been so interesting."])
    merri += S.say("Merribell", [
        "Nothing. Not one. And I went",
        "right down to the feet."])
    merri += [S.blush()]
    c += _suggestion(db.MERRI, merri)

    # Zephyrine: a slant rhyme, defended.
    zeph = S.say("Zephyrine", [
        "Slant rhyme. 'Turnip' and 'sherbet'."])
    zeph += S.say("Piper", [
        "That isn't a slant rhyme. That's",
        "two words."])
    zeph += S.say("Zephyrine", ["The Collegium would accept it."])
    zeph += S.say("Piper", ["The Collegium set fire to a Dean."])
    zeph += S.say("Zephyrine", [
        "I set fire to a Dean. The Collegium",
        "only minuted it."])
    c += _suggestion(db.ZEPH, zeph)

    # Roland: the right answer, at a quarter past two, to nobody.
    roland = S.say("Roland", [
        "Honestly? There isn't one. Change",
        "the other line."])
    roland += S.say("Piper", [
        "Absolutely not. We're nearly there."])
    roland += S.narrate([
        "Roland nods, as if he has heard that before at a",
        "great many tables, and goes to get another round."])
    c += _suggestion(db.ROLAND, roland)

    # Bram, always. He grows them; he has a professional interest.
    bram = S.narrate([
        "You suggest 'parsnip'. It is, you point out, very",
        "nearly there."])
    bram += S.say("Piper", [
        "It is a different vegetable, Bram."])
    c += bram + [S.trope()]
    return c


def turnip_pages(img):
    """Pages 2 and 3 of the Gilded Turnip (Map 4, event 6), in the prop's
    own dress - `img` is its first page's image, handed over by `village.py`
    so the turnip does not change what it looks like when Piper walks up.

    Page 2 is the afternoon, and can be put off; page 3 is afterwards, and
    beats it."""
    page = dict(img=img, trigger=0, priority=1, direction_fix=True)
    piper = {"actorValid": True, "actorId": db.PIPER}

    # -- 2: the afternoon.
    ask = S.narrate([
        "Piper stops in front of the gilded turnip and does",
        "not move on."])
    ask += S.say("Piper", [
        "The inn is named after the problem.",
        "I've been walking past the problem",
        "for a month. Listen to this."])
    ask += S.say("Piper", DRAFT)
    ask += S.say("Piper", [
        "And - what? And what? I need a rhyme",
        "for 'turnip'. Everybody. Sit down."])

    stay = S.narrate([
        "Everybody sits down. Prudence brings a pot of tea,",
        "reads the room, and brings a second one."])
    stay += _afternoon()
    stay += S.narrate([
        "The afternoon goes. The candles are lit. Prudence",
        "stops bringing tea, and then brings soup, out of",
        "pity."])
    stay += [R.wait(30)]
    stay += S.narrate([
        "Piper looks at the draft for a while. Then she",
        "crosses out the second line, writes a new one, and",
        "moves the turnip down one."])
    stay += S.narrate(["It takes about nine seconds."])
    stay += [R.play_se("Book1"), R.wait(20)]
    stay += S.say("Piper", VERSE)
    stay += [S.trope()]
    stay += S.narrate([
        "Everybody who spent the afternoon on this is",
        "furious. You are furious. You did not know you",
        "could be furious about a poem."])
    stay += R.if_then(
        R.condition_actor_in_party(db.ROLAND),
        S.narrate([
            "Roland, who said so at a quarter past two, is not",
            "furious. He is very gracious about it, which is",
            "worse."]))
    stay += S.say("Piper", [
        "What? It's the last verse. It was",
        "always going to be the last verse.",
        "I just had the lines the wrong",
        "way round."])
    stay += [R.control_switch(db.SW_PIP2_DONE, True)]
    stay += S.companion_story(db.PIPER)

    later = S.say("Piper", [
        "The turnip will keep.",
        "It's gold."])

    first = ask + R.choice_block(
        ["Find her a rhyme", "Not now"], [stay, later], cancel=1)

    # -- 3: afterwards.
    after = S.say("Piper", ["Nine seconds."])
    after += S.say("Piper", [
        "Put that on my headstone. Not the",
        "verse. The nine seconds."])

    return [
        R.page(first, conditions=dict(
            piper, switch1Valid=True, switch1Id=db.SW_LEFT_VILLAGE), **page),
        R.page(after, conditions=dict(
            piper, switch1Valid=True, switch1Id=db.SW_PIP2_DONE), **page),
    ]


# ======================================================================
# PIP-5, The Struck Verses (`QUESTS.md` A12)
# ----------------------------------------------------------------------
# The Committee keeps what it strikes. Of course it does. In a box, behind
# the red curtain in Prophecy Hall, and getting at it is a form, a key and
# a distraction - the last of which is what a party is for.
#
# * **What is in the box is never printed.** The player sees the count, which
#   is `VAR_BLUSHES` read back - the number the game has been keeping all
#   along - and Piper's face, and one verse: forty-one, which is about a
#   cat, and is entirely innocent, and was struck anyway.
# * **The ask is the fete minutes'** (Map 3, event 8), below their terminal
#   self switch A. The form is in the Committee Records (event 7); the
#   Councillor on the wording countersigns it (event 4); and Councillor Fenn
#   (event 5), whom nobody has ever listened to, is listened to - by whoever
#   is third in the party - while the key comes off his hook.
# * **Only the ask and the box need Piper.** The rest is global and the Clerk
#   who can strike her off the roster is in the same room, so a Piper sent
#   home half-way leaves the errand where it was.
# * **The archive is a room in the black of Map 3**, east of the hall,
#   drawn by `village.py`. The "curtain" is `Middle Window B`, a curtained
#   window on the north wall; drawn back, it is a door marked STRUCK.
VERSE_41 = [
    "  'The Elder's cat, one April, sat",
    "  upon the chapel roof till June;",
    "  the Elder climbed to fetch her - at",
    "  which point she jumped, and came down soon.'",
]


def _pip5_after(page0, conds, lines):
    """`page0` again, with one more narrated line - so nobody loses a word."""
    page = copy.deepcopy(page0)
    page["list"] = page["list"][:-1] + S.narrate(lines) + page["list"][-1:]
    page["conditions"] = R.page([], conditions=conds)["conditions"]
    return page


def _pip5_page(page0, cmds, conds):
    new = R.page(cmds, conditions=conds)
    return dict(copy.deepcopy(page0), list=new["list"],
                conditions=new["conditions"])


def minutes_pages(page0, terminal):
    """The fete minutes (Map 3, event 8): the ask, with Piper, below their
    terminal page (`terminal`, on self switch A); and afterwards."""
    ask = S.say("Piper", ["They keep what they strike. Of course",
                          "they do. It's a Committee."])
    ask += S.say("Piper", ["There'll be a box. There's always a box.",
                           "Behind the red curtain, I'd say. It's",
                           "the one thing in here that isn't on an",
                           "inventory."])
    ask += S.say("Piper", ["It'll want a form, a key and a",
                           "distraction. The distraction is what",
                           "you lot are for."])
    ask += [S.trope(), R.control_switch(db.SW_PIP5_ASKED, True)]
    again = S.say("Piper", ["A form, a key, a distraction.",
                            "In that order, ideally."])
    cmds = R.if_then(R.condition_switch(db.SW_PIP5_ASKED), again, ask)
    a = dict(terminal["conditions"])
    return [
        _pip5_page(terminal, cmds, {
            "switch1Valid": True, "switch1Id": a["switch1Id"],
            "selfSwitchValid": True, "selfSwitchCh": "A",
            "actorValid": True, "actorId": db.PIPER}),
        _pip5_after(terminal, {"switch1Valid": True,
                               "switch1Id": db.SW_PIP5_DONE},
                    ["Pinned under them, a slip: 'Struck material",
                     "consulted, Form S-7.' Initialled P.Q., in metre."]),
    ]


def records_pages(page0):
    """The Committee Records (Map 3, event 7): the form is in here, once
    Piper knows there is a box. Afterwards they are the records again."""
    find = S.narrate([
        "Behind the minutes, a pad of forms. The top one:",
        "FORM S-7. APPLICATION TO CONSULT STRUCK MATERIAL",
        "(VERSE). To be countersigned as to the wording."])
    find += [R.gain_item(db.IT_FORM_S7, 1), R.play_me("Item"),
             R.self_switch("B", True)]
    find += S.got(["Got \\I[193]\\C[3]Form S-7\\C[0]."])
    return [
        _pip5_page(page0, find, {"switch1Valid": True,
                                 "switch1Id": db.SW_PIP5_ASKED}),
        dict(copy.deepcopy(page0), conditions=R.page([], conditions={
            "selfSwitchValid": True, "selfSwitchCh": "B"})["conditions"]),
    ]


def wording_pages(page0):
    """The Councillor on the wording (Map 3, event 4) countersigns Form S-7,
    as to the wording, which is all he does."""
    sign = S.narrate(["He reads Form S-7 twice, with a pencil."])
    sign += S.say("Councillor", ["'Consult' or 'inspect'?",
                                 "Because 'inspect' is a commitment."])
    sign += S.narrate(["He crosses out 'inspect', writes 'consult',",
                       "crosses that out too, and initials both."])
    sign += S.say("Councillor", ["Countersigned. As to the wording.",
                                 "The key is Fenn's. Good luck."])
    sign += [R.control_switch(db.SW_PIP5_SIGNED, True)]
    return [
        _pip5_page(page0, sign, {"itemValid": True,
                                 "itemId": db.IT_FORM_S7}),
        _pip5_after(page0, {"switch1Valid": True,
                            "switch1Id": db.SW_PIP5_SIGNED},
                    ["He is still thinking about 'consult'."]),
    ]


DECOY = ("$gameParty.members().map(a => a.actorId())"
         ".find(i => i !== %d && i !== %d) || 0" % (db.BRAM, db.PIPER))


def fenn_pages(page0):
    """Councillor Fenn (Map 3, event 5), whom nobody listens to. Somebody
    does, at last - whoever is third in the party - and the key comes off
    his hook while he explains."""
    listened = S.narrate([
        "There is a key on a hook on Councillor Fenn's belt,",
        "with STRUCK on its tag. He does not leave his post."])
    listened += S.narrate([
        "\\N[\\V[%d]] asks him what he means, exactly," % db.VAR_PIP5_DECOY,
        "about clause twelve."])
    listened += S.say("Councillor Fenn", ["...Nobody has ever asked."])
    listened += S.say("Councillor Fenn", ["Sit down. Sit DOWN.",
                                          "It goes back to the original",
                                          "wording, and the original wording",
                                          "goes back to a horse -"])
    listened += S.narrate([
        "He is away. He will be some time. You take the key",
        "off its hook, and he does not notice, because for",
        "the first time in forty years somebody is nodding."])
    listened += [R.gain_item(db.IT_ARCHIVE_KEY, 1), R.play_se("Key"),
                 R.control_switch(db.SW_PIP5_KEY, True)]
    listened += S.got(["Got \\I[195]\\C[3]A Key Marked STRUCK\\C[0]."])
    alone = S.narrate([
        "There is a key on a hook on Councillor Fenn's belt.",
        "Somebody would have to ask him about clause twelve,",
        "and it cannot be you: you are already Chosen, and",
        "he has explained it to you. It wants a third."])
    cmds = [R.control_variable_script(db.VAR_PIP5_DECOY, DECOY)]
    cmds += R.if_then(R.condition_variable(db.VAR_PIP5_DECOY, 0, 3),
                      listened, alone)
    return [
        _pip5_page(page0, cmds, {"switch1Valid": True,
                                 "switch1Id": db.SW_PIP5_SIGNED}),
        _pip5_after(page0, {"switch1Valid": True,
                            "switch1Id": db.SW_PIP5_KEY},
                    ["He is still explaining clause twelve, to",
                     "the room, and he looks very well on it."]),
    ]


def curtain_event(event_id, x, y, archive):
    """The red curtain in the north wall: behind it, a door. With the key,
    through it, to `archive` - (map, x, y), the archive's arrival."""
    door = S.narrate(["A window with red curtains, drawn. Behind",
                      "them there is no window: there is a door",
                      "marked STRUCK MATERIAL. NO ADMITTANCE WITHOUT",
                      "FORM S-7. It is locked."])
    go = S.narrate(["The key fits. Of course it does."])
    go += [R.play_se("Open1"), R.transfer(*archive, 8, 0)]
    blank = R.image("")
    return R.event(event_id, "Behind the Curtain", x, y, [
        R.page(door, img=blank, direction_fix=True),
        R.page(go, img=blank, direction_fix=True,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_PIP5_KEY}),
    ])


def _pip5_box():
    c = S.narrate([
        "The best box the Committee owns, gilded, with a red",
        "stone in the lid, and full to it: two hundred years of",
        "struck verses, one to a slip, each dated, and each",
        "initialled by whoever struck it."])
    c += S.say("Piper", ["They kept them. Every one."])
    c += S.narrate([
        "She does not read them aloud. She reads them to",
        "herself, one after another, and her face does a great",
        "many things, and you watch it do them."])
    c += [R.wait(40)]
    c += S.narrate([
        "In the lid there is a tally card, in the Clerk's hand:",
        "STRUCK, THERE BEING CHILDREN PRESENT. The total at",
        "the bottom is \\C[2]\\V[%d]\\C[0]." % db.VAR_BLUSHES])
    c += S.say("Piper", ["\\V[%d]." % db.VAR_BLUSHES])
    c += S.say("Piper", ["...That's about right."])
    c += S.narrate([
        "She holds up one slip, so that you can read it, and",
        "only that one. Verse forty-one. It is about a cat."])
    c += S.narrate(VERSE_41)
    c += [S.blush()]
    c += S.say("Piper", ["It scans."])
    c += S.narrate([
        "She puts it back exactly where it was, and shuts the",
        "lid, and the key goes back on Fenn's hook on the way",
        "out, while he is still explaining."])
    c += S.say("Piper", ["They were right to keep them.",
                         "Somebody should."])
    c += [R.gain_item(db.IT_ARCHIVE_KEY, -1), R.gain_item(db.IT_FORM_S7, -1),
          R.control_switch(db.SW_PIP5_DONE, True)]
    c += S.companion_story(db.PIPER)
    return c


def archive_events(base_id, box_at, door_at, back, box_tile):
    """The archive (in the black of Map 3): the box, and the way back to
    `back` - (map, x, y), in front of the curtain."""
    box_img = R.image("", 0, tile_id=box_tile)
    shut = S.narrate(["A gilded case, the best box in the building,",
                      "with a card on it in the Clerk's hand: STRUCK.",
                      "It is Piper's to open, if it is anybody's."])
    after = S.narrate(["The gilded case marked STRUCK, shut. Everything",
                       "in it is where it was, except one slip that",
                       "has been very slightly straightened."])
    return [
        R.event(base_id, "The Box", *box_at, [
            R.page(shut, img=box_img, direction_fix=True),
            R.page(_pip5_box(), img=box_img, direction_fix=True,
                   conditions={"switch1Valid": True,
                               "switch1Id": db.SW_PIP5_KEY,
                               "actorValid": True, "actorId": db.PIPER}),
            R.page(after, img=box_img, direction_fix=True,
                   conditions={"switch1Valid": True,
                               "switch1Id": db.SW_PIP5_DONE})]),
        R.event(base_id + 1, "Archive Door", *door_at, [R.page(
            [R.play_se("Close1"), R.transfer(*back, 2, 0)],
            img=R.image(""), trigger=1, priority=0, through=True)]),
    ]



# ======================================================================
# PIP-3, The Contest at the Sign of the Bell (`QUESTS.md` B3)
# ----------------------------------------------------------------------
# A bardic competition at Great Dunnage with categories nobody can defend,
# judged by a panel that includes a man who cannot hear and a woman who gives
# everything a two. The damage type is heckling. She loses to a man who does
# birdcalls, and the birdcalls are, in fairness, extraordinary.
#
# * **The entry is Mrs Harbottle's** (Map 65 event 3), below her one-self-
#   switch ladder, with Piper. Ballad (Not Sad) - the category she wrote
#   something about in the back of her book at the poster. It turns
#   `SW_PIP3_ON` on, which brings two rival acts into the Bell (events 9 and
#   10, empty until then and empty again after).
# * **The contest is Mrs Harbottle's next page**, with Piper and the switch:
#   three acts are scored, then Piper's set is a fight - troop 41, the two
#   rival acts and the back table, whose hit points are the room's patience
#   (`db.build_contest`), and she fights it alone - the rest of the party
#   is shown to the bench by the door (P1, `QUESTS.md` Part G; the swap in
#   `_pip3_battle`). It can be lost; she finishes anyway. Either way the
#   scores are the scores: eighteen against Mr Tweddle's nineteen, by one
#   point, Miss Quayle's - the thrush got a three.
# * **Her gear is the rosette** (`QUESTS.md` 0.5): armour 41, an accessory of
#   armour type 8, which no class can wear and Piper's actor can. She frames
#   the certificate and wears the rosette.
# * **Afterwards is for everybody**: Mrs Harbottle, Mr Tweddle and Miss
#   Quayle each get their own last page and a line, and the poster its
#   results.
PIP3_RIVALS = [(9, "Mr Dray", (19, 6)), (10, "Miss Moon", (19, 8))]
ROSETTE_ICON = 149


def _pip3_battle(won, lost):
    """Battle Processing with If Win and If Lose bodies, and no escape -
    fought by Piper alone (P1, `QUESTS.md` Part G), with `SPARE.md` 3's swap:
    the party into `$gameTemp`, which is safe because nothing can be saved
    while an event runs, and back after both branches. She goes on rested."""
    out = R.script([
        "$gameTemp._pip3Party = $gameParty._actors.slice();",
        "$gameParty._actors = [%d];" % db.PIPER,
        "$gameActors.actor(%d).recoverAll();" % db.PIPER,
        "$gamePlayer.refresh();",
        "$gameMap.requestRefresh();",
    ])
    out += [R.battle(db.TR_CONTEST, can_escape=False, can_lose=True)]
    for code, body in [(601, won), (603, lost)]:
        out += [{"code": code, "indent": 0, "parameters": []}]
        out += R.shift(body, 1)
        out += [{"code": 0, "indent": 1, "parameters": []}]
    out += [{"code": 604, "indent": 0, "parameters": []}]
    out += R.script([
        "$gameParty._actors = $gameTemp._pip3Party;",
        "$gameTemp._pip3Party = null;",
        "$gamePlayer.refresh();",
        "$gameMap.requestRefresh();",
    ])
    return out


def _pip3_entry():
    c = S.narrate([
        "Piper puts her book down on the judges' table, open,",
        "and stands up very straight."])
    c += S.say("Piper", ["Piper Quill, of Thistlewick,",
                         "wishes to enter."])
    c += S.say("Mrs Harbottle", ["Category?"])
    c += S.say("Piper", ["Ballad (Not Sad)."])
    c += S.say("Mrs Harbottle", ["Nobody has ever",
                                 "entered Ballad (Not Sad)."])
    c += S.say("Piper", ["Piper Quill is aware of that."])
    c += S.say("Mrs Harbottle", ["Then the Contest is",
                                 "tonight. It is always tonight. We",
                                 "have simply not had the entries."])
    c += [R.play_se("Open1"), R.wait(20)]
    c += S.narrate([
        "As if they had been waiting outside, which they had,",
        "two more entrants come in out of the street: a man",
        "with a serpent, and a woman in black with a sheaf of",
        "verses and her handkerchief already out."])
    c += S.say("Mrs Harbottle", ["Come to the panel",
                                 "when you are ready, Miss Quill."])
    c += [S.trope(), R.control_switch(db.SW_PIP3_ON, True)]
    return c


def _pip3_waiting():
    return S.say("Mrs Harbottle", ["Miss Quill. When you",
                                   "are ready. The panel is always ready."])


def _pip3_scores(ambler, quayle, harbottle):
    c = S.say("Mr Ambler", ["%s!" % ambler])
    c += S.say("Miss Quayle", ["%s." % quayle])
    c += S.say("Mrs Harbottle", ["%s." % harbottle])
    return c


def _pip3_contest():
    c = [R.play_se("Bell1", 70), R.wait(30)]
    c += S.narrate([
        "The room fills, the way a room does when word has got",
        "round that there are entries. Mrs Harbottle rings the",
        "little bell on the judges' table."])
    c += S.say("Mrs Harbottle", ["Instrumental (Other",
                                 "Wind). Mr Septimus Dray."])
    c += S.narrate([
        "Mr Dray plays the serpent, which is a sort of bassoon",
        "that has given up, for eleven minutes. It is very like",
        "listening to a drain that has had bad news."])
    c += _pip3_scores("Nine", "Two", "Six")
    c += S.say("Mrs Harbottle", ["Ballad (Sad). Miss",
                                 "Lettice Moon."])
    c += S.narrate([
        "Fourteen verses. Everybody in it dies, including the",
        "narrator, who comes back for the chorus. Several of",
        "the back table are visibly moved, and say so, loudly."])
    c += _pip3_scores("Nine", "Two", "Five")
    c += S.say("Mrs Harbottle", ["Birdsong (Open).",
                                 "Mr Tweddle."])
    c += [R.wait(40)]
    c += S.narrate([
        "A nightingale. A curlew. And then the thrush that has",
        "lost its keys, which goes looking for them all round",
        "the room, under the tables and up the chimney, and",
        "finds them, and the room very nearly stands up."])
    c += S.say("Mr Ambler", ["Nine!"])
    c += [R.wait(40)]
    c += S.narrate([
        "Miss Quayle's pencil hovers over her card for a long",
        "time."])
    c += S.say("Miss Quayle", ["...Three."])
    c += S.narrate([
        "The room gasps. Miss Quayle looks at her pencil as if",
        "it had done it by itself."])
    c += S.say("Mrs Harbottle", ["Seven. Nineteen."])
    c += S.say("Mrs Harbottle", ["Ballad (Not Sad).",
                                 "Miss Piper Quill."])
    c += S.say("Piper", ["Piper Quill takes the stage. Piper",
                         "Quill is not nervous. Piper Quill has",
                         "done this on tables."])
    c += S.narrate([
        "The rest of you are shown to the bench by the door,",
        "and told, kindly, that it is Piper's set."])
    c += S.narrate([
        "The back table has views. So, from the floor, do the",
        "other two acts."])
    won = S.narrate([
        "Somewhere in the fourth verse the back table runs out",
        "of things to shout, and Mr Dray and Miss Moon sit down,",
        "to a smattering, and the rest of it is heard."])
    lost = S.narrate([
        "The room runs out of patience somewhere in verse three.",
        "Piper finishes anyway, in the third person, over the",
        "top of all of it, and the last verse is so loud that",
        "it is, technically, heard."])
    lost += [R.recover_all(0)]
    c += _pip3_battle(won, lost)
    c += S.narrate([
        "It is a ballad about a farm boy who walked north, and",
        "nobody dies in it, and it is all true. Nobody in Great",
        "Dunnage has ever heard one like it."])
    c += _pip3_scores("Nine", "Two", "Seven")
    c += S.narrate([
        "Eighteen. Mr Tweddle: nineteen. Second place, by one",
        "point, and the point is Miss Quayle's."])
    c += S.say("Piper", ["Piper Quill will say this once. The",
                         "birdcalls were, in fairness,",
                         "extraordinary."])
    c += S.say("Mr Tweddle", ["Thank you. The thrush has been",
                              "practising since Easter."])
    c += S.narrate([
        "Mrs Harbottle presents a certificate, SECOND PLACE,",
        "BALLAD (NOT SAD), and a rosette in blue silk. It is the",
        "first prize anybody in Piper's family has won for",
        "writing down what actually happened."])
    c += S.narrate([
        "She has the certificate framed before breakfast. Mrs",
        "Dewhirst lends her the nail. She wears the rosette."])
    c += [R.gain_armor(db.AR_ROSETTE, 1), R.play_me("Fanfare1"),
          R.control_switch(db.SW_PIP3_ON, False),
          R.control_switch(db.SW_PIP3_DONE, True)]
    c += S.got(["Got \\I[%d]\\C[3]Rosette, Second Place\\C[0]." %
                ROSETTE_ICON])
    c += S.companion_story(db.PIPER)
    return c


def _pip3_go():
    return S.narrate(["The panel is ready. The room is filling up."]) + \
        R.choice_block(["Begin", "Not yet"],
                       [_pip3_contest(), _pip3_waiting()])


def _after(last, conds, lines):
    """A person's own last page with one narrated line put on the end."""
    page = copy.deepcopy(last)
    page["list"] = page["list"][:-1] + S.narrate(lines) + page["list"][-1:]
    page["conditions"] = R.page([], conditions=conds)["conditions"]
    return page


def harbottle_pages(last):
    """Three pages for Mrs Harbottle (Map 65, event 3), whose ladder is one
    self switch: the entry, the contest, and afterwards."""
    a_piper = {"selfSwitchValid": True, "selfSwitchCh": "A",
               "actorValid": True, "actorId": db.PIPER}

    def pg(cmds, conds):
        new = R.page(cmds, conditions=conds)
        return dict(copy.deepcopy(last), list=new["list"],
                    conditions=new["conditions"])

    return [
        pg(_pip3_entry(), a_piper),
        pg(_pip3_go(), dict(a_piper, switch1Valid=True,
                            switch1Id=db.SW_PIP3_ON)),
        _after(last, {"selfSwitchValid": True, "selfSwitchCh": "A",
                      "switch1Valid": True, "switch1Id": db.SW_PIP3_DONE},
               ["Pinned on the wall behind her: SECOND, MISS P.",
                "QUILL, BALLAD (NOT SAD), 18. A very creditable 18."]),
    ]


_DONE_A = {"selfSwitchValid": True, "selfSwitchCh": "A",
           "switch1Valid": True, "switch1Id": db.SW_PIP3_DONE}


def tweddle_page(last):
    return _after(last, _DONE_A, [
        "He has a rosette on, in red silk, and keeps forgetting,",
        "and being startled by it."])


def quayle_page(last):
    return _after(last, _DONE_A, [
        "She gave the thrush a three. She has not got over it."])


def poster_page(page0):
    return _after(page0, {"switch1Valid": True,
                          "switch1Id": db.SW_PIP3_DONE}, [
        "RESULTS, pinned under it: 1st, Mr Tweddle, Birdsong",
        "(Open), 19. 2nd, Miss Quill, Ballad (Not Sad), 18."])


_RIVAL_LINES = {
    "Mr Dray": (["Dray. Instrumental (Other Wind).",
                 "Second place, twice. There were two",
                 "entries, both times."],
                ["It's a serpent. It's meant to sound",
                 "like that. Mostly."]),
    "Miss Moon": (["Moon. Ballad (Sad). Fourteen verses.",
                   "Nobody survives."],
                  ["I've changed the ending. Somebody",
                   "survives verse three. Briefly."]),
}


def rival_events():
    """The two other entrants (Map 65, events 9 and 10): there only while the
    Contest is on. Empty before, and empty again after - they go home."""
    evs = []
    for eid, name, (x, y) in PIP3_RIVALS:
        img = R.image(*S.sprite(name), direction=4)
        first, again = _RIVAL_LINES[name]
        on = {"switch1Valid": True, "switch1Id": db.SW_PIP3_ON}
        evs.append(R.event(eid, name, x, y, [
            R.page([], img=R.image(""), priority=0, through=True),
            R.page(S.say(name, first) + [R.self_switch("A", True)], img=img,
                   conditions=on),
            R.page(S.say(name, again), img=img,
                   conditions=dict(on, selfSwitchValid=True,
                                   selfSwitchCh="A")),
            R.page([], img=R.image(""), priority=0, through=True,
                   conditions={"switch1Valid": True,
                               "switch1Id": db.SW_PIP3_DONE}),
        ]))
    return evs


# ================================================================ PIP-4 ==
# The Elegy (`QUESTS.md` E12). She is commissioned to write an elegy for a
# man she never met, by a village that loved him, and the only way to do it
# is to interview eleven people who all describe somebody different. She
# writes it out of the contradictions, it is nine lines long, and she does
# not perform it. **Register B: no punchline at anybody's expense.** The
# joke is that the village had asked for a bit more of a tune.
#
# * **The man is Abel Thrush**, the carrier, who walked Little Gore -
#   Fenmarch - Sump with the post for fifty years and died in the spring of
#   1991; Tom walks the Fenmarch half now. The commission is a card nailed to
#   the back of Little Gore's fingerpost, where nobody reads but a
#   chronicler: its own page, and with Piper, the card.
# * **The eleven are other quests' owners**, in three places, so each
#   interview page has to carry whatever page would otherwise have shown:
#   `_pip4_carry` rebuilds `Game_Event.refresh`'s choice as a chain of
#   script conditions over the event's own pages, then the interview. The
#   page needs Piper and `SW_PIP4_ON`, which goes off when the elegy is
#   written, so nothing is shadowed afterwards. Heard is the owner's self
#   switch D (free on all four maps), counted in `VAR_PIP4_HEARD`.
# * **Afterwards for everybody**: the fingerpost, with the nine lines under
#   the Fenmarch arm.
PIP4_ELEGY = [
    "ABEL THRUSH, CARRIER. LITTLE GORE - FENMARCH - SUMP.",
    "He never spoke a word. He never stopped.",
    "He came in at the gate. He climbed the wall.",
    "He read no letter, and he knew them all.",
    "He carried a cow, and wept over a bird.",
    "He brought the water nobody would drink,",
    "and stopped for tea, and was at eight each day",
    "where somebody looked up to see him wave.",
    "Eleven people knew him. All are true.",
    "The road is four miles long. He walks it still.",
]

# Who said what. Keyed by owner; each is (speaker, lines, Piper's note).
PIP4_HEARD = {
    "vane": ("Mrs Vane", [
        "Abel? He brought Tom's letters",
        "a whole year, every day, and never",
        "once read one. He knew, mind."],
        "He read no letter, and knew them all."),
    "tom": ("Tom", [
        "Never stopped talking. Four",
        "miles each way, about everything.",
        "I talk the whole way now. Somebody",
        "has to."], "He never stopped."),
    "winifred": ("Dame Winifred", [
        "Waved every morning,",
        "eight o'clock, two years. Never",
        "said one word. Shy, I thought."],
        "He never spoke a word."),
    "bess": ("Bess", [
        "Gran says he was a giant. He",
        "carried a cow to Fenmarch once,",
        "because it wouldn't walk."], "He carried a cow."),
    "alfie": ("Alfie", [
        "He could whistle with two",
        "fingers. You could hear it at Sump.",
        "Dad can't. I'm learning."], "A whistle you could hear at Sump."),
    "nell": ("Nell", [
        "When we play weddings I'm him,",
        "sometimes. He brings the letter.",
        "You go round the green and say POST."],
        "He brings the letter. Round the green."),
    "puddifoot": ("Mrs Puddifoot", [
        "Over the wall, every",
        "day, fifty years. Never used the",
        "gate once. Like family."], "He climbed the wall."),
    "ottershaw": ("Mr Ottershaw", [
        "He brought me every",
        "heron he found dead on the road.",
        "Wept over each one. Four miles."],
        "He wept over a bird."),
    "fourth": ("The Fourth", [
        "I asked him the way to",
        "the gate, when I was ten. He said",
        "he came in by it every day."],
        "He came in at the gate."),
    "gammage": ("Mr Gammage", [
        "Every Tuesday, forty",
        "years, a bottle of Fenmarch water",
        "on our well. Nobody drank it."],
        "The water nobody would drink."),
    "pardew": ("Mrs Pardew", [
        "Terrible man for his tea.",
        "Stopped anywhere for it. Took him",
        "all day to do four miles."], "He stopped for tea."),
}


def _pip4_test(conditions):
    """A JavaScript expression that is true when a page's conditions hold,
    evaluated by a Conditional Branch inside the same event."""
    c, out = conditions, []
    if c["switch1Valid"]:
        out.append("$gameSwitches.value(%d)" % c["switch1Id"])
    if c["switch2Valid"]:
        out.append("$gameSwitches.value(%d)" % c["switch2Id"])
    if c["variableValid"]:
        out.append("$gameVariables.value(%d) >= %d"
                   % (c["variableId"], c["variableValue"]))
    if c["selfSwitchValid"]:
        out.append("$gameSelfSwitches.value([this._mapId, this._eventId, "
                   "'%s'])" % c["selfSwitchCh"])
    if c["itemValid"]:
        out.append("$gameParty.hasItem($dataItems[%d])" % c["itemId"])
    if c["actorValid"]:
        out.append("$gameParty.members().includes($gameActors.actor(%d))"
                   % c["actorId"])
    return " && ".join(out) or "true"


def _pip4_carry(pages):
    """The commands of whichever of `pages` the engine would show, as a
    chain of Conditional Branches: the last page whose conditions hold, as
    `Game_Event.refresh` decides it."""
    shown = pages[0]["list"][:-1]
    for page in pages[1:]:
        shown = R.if_then(
            R.condition_script(_pip4_test(page["conditions"])),
            page["list"][:-1], shown)
    return shown


def _pip4_interview(key):
    speaker, lines, note = PIP4_HEARD[key]
    c = S.narrate([
        "Piper asks about Abel Thrush, the carrier, and gets out",
        "her notebook."])
    c += S.say(speaker, lines)
    c += S.narrate([
        "Piper writes it down: %s" % note,
        "It does not agree with anything else in the book. She",
        "underlines it."])
    c += [R.self_switch("D"), R.control_variable_add(db.VAR_PIP4_HEARD)]
    return c


def interview_pages(key, pages):
    """One page appended to an owner's event: with Piper while the elegy is
    being written, the page that would have shown, and then their account
    of Abel Thrush - once. `pages` is the event's whole list so far."""
    heard = S.narrate(["Piper has this one already. She nods, and does not",
                       "write it down twice."])
    cmds = _pip4_carry(pages) + R.if_then(
        R.condition_self_switch("D"), heard, _pip4_interview(key))
    conds = {"actorValid": True, "actorId": db.PIPER,
             "switch1Valid": True, "switch1Id": db.SW_PIP4_ON}
    # Below a ladder the page needs its terminal (0.2): the owner's A, where
    # the owner's first page sets one.
    if any(p["conditions"]["selfSwitchValid"] and
           p["conditions"]["selfSwitchCh"] == "A" for p in pages):
        conds.update(selfSwitchValid=True, selfSwitchCh="A")
    return [_pip5_page(pages[-1], cmds, conds)]


def _pip4_commission():
    c = S.narrate([
        "Piper goes round the back of the post, the way a chronicler",
        "reads the back of everything. There is a card nailed there,",
        "gone soft with weather:"])
    c += S.narrate([
        "WANTED: AN ELEGY. For ABEL THRUSH, carrier, who walked",
        "this road fifty years and never had one. Something with a",
        "bit of a tune. The parish will pay. Ask anybody."])
    c += S.say("Piper", ["Piper Quill has never met",
                         "Abel Thrush. Piper Quill will have",
                         "to ask anybody."])
    c += S.narrate([
        "She takes the card down, and puts it in her book, and",
        "looks up the road towards Fenmarch, and down it, towards",
        "Sump. It is a long road for a short poem."])
    c += [S.trope(), R.control_switch(db.SW_PIP4_ON, True)]
    return c


def _pip4_count():
    return S.narrate([
        "Piper's notebook: \\V[%d] of eleven, and not one of them"
        % db.VAR_PIP4_HEARD,
        "the same man. Little Gore, Fenmarch, and Sump."])


def _pip4_write():
    c = S.narrate([
        "Piper sits down at the foot of the fingerpost with her",
        "book open on her knee, and reads all eleven, and does not",
        "try to make them agree."])
    c += S.narrate([
        "She writes for a long time, and crosses most of it out,",
        "and what is left is nine lines."])
    c += [R.wait(30)]
    c += S.narrate(PIP4_ELEGY[:4])
    c += S.narrate(PIP4_ELEGY[4:7])
    c += S.narrate(PIP4_ELEGY[7:])
    c += [R.wait(40)]
    c += S.narrate([
        "She does not stand on anything. She does not read it out.",
        "She pins it to the post, under the Fenmarch arm, and",
        "steps back."])
    c += S.narrate([
        "Little Gore comes out to read it, one at a time, all",
        "afternoon. Mrs Vane reads it twice."])
    c += S.say("Mrs Vane", ["It's him. All of him. Every",
                            "one of us is in it."])
    c += S.say("Mrs Vane", ["...We did wonder whether it",
                            "might have a bit more of a tune."])
    c += S.narrate([
        "Piper laughs - properly, out loud, about her own work,",
        "which nobody has heard her do before."])
    c += S.say("Piper", ["Next time."])
    c += [R.gain_item(db.IT_ELEGY, 1)]
    c += R.text(["Got \\I[193]\\C[3]Elegy (Nine Lines)\\C[0]."])
    c += [R.control_switch(db.SW_PIP4_ON, False),
          R.control_switch(db.SW_PIP4_DONE, True)]
    c += S.companion_story(db.PIPER)
    return c


def fingerpost_pages(page0):
    """Pages 2-3 of Little Gore's fingerpost (Map 50, event 9), which has no
    ladder: with Piper, its own page and the commission, the count or the
    writing; afterwards, its own page and the nine lines, for everybody."""
    own = page0["list"][:-1]
    working = R.if_then(
        R.condition_variable(db.VAR_PIP4_HEARD, 11, 1), _pip4_write(),
        _pip4_count())
    piper = own + R.if_then(R.condition_switch(db.SW_PIP4_ON), working,
                            _pip4_commission())
    after = own + S.narrate([
        "Under the Fenmarch arm, under a little roof somebody has",
        "made for it, nine lines in Piper's hand: ABEL THRUSH,",
        "CARRIER. People stop and read it on their way past."])
    after += R.if_then(R.condition_actor_in_party(db.PIPER), S.narrate([
        "Piper does not read it again. She does not need to."]))
    return [
        _pip5_page(page0, piper, {"actorValid": True, "actorId": db.PIPER}),
        _pip5_page(page0, after, {"switch1Valid": True,
                                  "switch1Id": db.SW_PIP4_DONE}),
    ]


# ================================================================ PIP-1 ==
# The Authorised Version (`QUESTS.md` E13). Her aunt Ambrosine is writing
# the official account of Bram's quest and has already finished it, having
# started before he left, because the shape is known. It is better than what
# happened. Bram is an orphan in it, Merribell dies in it, and there is a bit
# with a wolf. The Committee has approved it.
#
# * **Ambrosine is a new event in Prophecy Hall** (Map 3 event 12), at the
#   Committee's paperwork by the door: empty until Piper is in the party and
#   the road has been walked - it is finished while you were away - and then
#   there, and she reads it to you. `SW_PIP1_ON` keeps her there for
#   everybody, so a dismissed Piper's errand waits ("Where is my niece?").
# * **Three answers, two endings.** "It's very good" is the one worth
#   building (`COMPANIONS.md`): it stands, with one footnote by P. Quill.
#   "Fix it" is the two of them putting the truth into metre - and the wolf
#   becomes the goat that sent its apologies to the meeting at which Bram
#   was Chosen, which is in the minutes. "Fight it" is a letter to the
#   Committee, which approved it, and which files it under 'no change': it
#   ends nothing and the choice is put again.
# * **Afterwards for everybody**: Ambrosine on her ending, and the Wall of
#   the Forty-Seven's card for the Forty-Eighth, one `if_then` on the ending.
AUTH_CANTO_1 = [
    "  'An orphan boy of humble birth,",
    "  who never knew a mother's care,",
    "  went northward, out across the earth,",
    "  with nothing but a sword, and prayer.'",
]
AUTH_CANTO_4 = [
    "  'And in the Gloamwood, grey and old,",
    "  a wolf came padding from the wood,",
    "  and spoke, and what the grey wolf told",
    "  he kept, and kept it for his good.'",
]
AUTH_CANTO_6 = [
    "  'And on the mountain, in the night,",
    "  he doubted, on a single stone,",
    "  and forty-seven, robed in light,",
    "  stood round, and he was not alone.'",
]
AUTH_CANTO_9 = [
    "  'And Merribell, the healer, fell,",
    "  and with her last breath bade him go;",
    "  he laid her by a holy well,",
    "  and wept, and went on through the snow.'",
]
# The fixed version: the same four cantos, in metre, and true.
FIXED_CANTOS = [
    ["  'A farmer's boy, whose mother still",
     "  was in the kitchen, with a pie,",
     "  took down the sword against his will,",
     "  and went, and did not ask her why.'"],
    ["  'There was no wolf. There was a goat,",
     "  which sent apologies, and stayed",
     "  away; the Clerk took careful note,",
     "  and that is how a record's made.'"],
    ["  'And in the middle, it was wet,",
     "  and they walked on, and on, and on,",
     "  and argued for a week, and yet",
     "  found no rhyme for turnip. None.'"],
    ["  'And Merribell, who did not fall,",
     "  sat everybody down instead,",
     "  and gave them water, first of all,",
     "  and socks, and saw that they were fed.'"],
]
AUTH_NO_TURNIP = "There is not a turnip in it anywhere."


def _pip1_reading():
    """Ambrosine reads it to you - four of its twelve cantos, and the good
    middle, and who is in the room decides who minds what."""
    c = S.narrate([
        "THE LAY OF THE FORTY-EIGHTH. Being the Authorised",
        "Account of the Chosen One, Bram Thistle. By A. Quill,",
        "Chronicler to the Committee. APPROVED."])
    c += S.narrate(AUTH_CANTO_1)
    c += S.narrate([
        "Bram has a mother. She is at home, as far as he knows,",
        "and was making a pie when he last saw her."])
    c += S.say("Ambrosine", ["It's an orphan's road, dear.",
                             "It always is. Nobody goes north",
                             "with a mother. It doesn't scan."])
    c += S.narrate(AUTH_CANTO_4)
    c += S.say("Piper", ["There was no wolf."])
    c += S.say("Ambrosine", ["There is always a wolf.",
                             "Your grandmother had a wolf in",
                             "numbers forty-one, forty-two and",
                             "forty-three. The same wolf. A good wolf."])
    c += S.narrate(AUTH_CANTO_6)
    c += S.say("Ambrosine", ["That's the middle. Nobody",
                             "does the middle. Everybody has a",
                             "beginning and an end, and in between",
                             "they walk. That is a good middle."])
    c += S.narrate(["Piper does not say anything for a moment."])
    c += S.say("Piper", ["...It is a good middle."])
    c += S.narrate(AUTH_CANTO_9)
    merri = S.narrate(["Merribell reads canto nine with professional",
                       "interest, and then again."])
    merri += S.say("Merribell", ["What did I die of?"])
    merri += S.say("Ambrosine", ["It doesn't say, dear. It",
                                 "scans."])
    merri += S.say("Merribell", ["I'd have had a glass of",
                                 "water and sat down."])
    no_merri = S.say("Piper", ["Sister Merribell is alive,",
                               "and well, and would want it noted",
                               "that she is."])
    c += R.if_then(R.condition_actor_in_party(db.MERRI), merri, no_merri)
    c += S.narrate([
        "Twelve cantos. He slays the Dark Lord at the top of a",
        "tower in a thunderstorm, in a rhyme on 'tower' that was",
        "never going to be anything but 'hour', and comes home."])
    c += S.narrate([
        "Bram reads all twelve again, looking for a turnip.",
        AUTH_NO_TURNIP])
    c += [R.wait(30)]
    c += S.say("Ambrosine", ["Well, Piper? You have",
                             "a face. Your mother had that face."])
    return c


def _pip1_good():
    """The ending worth building: you read it, and it is very good, and you
    say so."""
    c = S.narrate([
        "You tell her it is very good. It is. It is properly",
        "metred, and it has a good middle, and none of it",
        "happened."])
    c += S.narrate(["Piper looks at you as if you had hit her."])
    c += [R.wait(30)]
    c += S.narrate([
        "Then she takes the manuscript back off the table and",
        "reads canto six again, to herself, and her mouth goes",
        "on moving after the last line."])
    c += S.say("Piper", ["...It's very good."])
    c += S.say("Ambrosine", ["Thank you."])
    c += S.narrate([
        "Ambrosine Quill takes her spectacles off, and holds",
        "them, and does not put them back on for a while."])
    c += S.say("Ambrosine", ["Four generations. The",
                             "Committee approves. It doesn't read.",
                             "Nobody has ever said that before."])
    c += S.narrate([
        "Bram says he would like a copy, for his mother. Ambrosine",
        "points out, gently, that his mother is in it, briefly,",
        "in the past tense. He would still like a copy."])
    c += S.say("Piper", ["Piper Quill has a professional",
                         "objection. She will put it in a",
                         "footnote."])
    c += S.say("Ambrosine", ["One footnote."])
    c += S.say("Piper", ["One."])
    c += S.narrate([
        "At the foot of canto twelve, in small type: 'None of",
        "this happened. It is very good. - P.Q.' Ambrosine reads",
        "it twice, and initials it, as to the wording."])
    c += [R.control_switch(db.SW_PIP1_GOOD, True)]
    return c


def _pip1_fix():
    """The other ending: the two of them put what happened into metre."""
    c = S.narrate([
        "You say it could be fixed. Piper has her book open",
        "before you have finished, at the first page, where",
        "Bram is asleep and eleven people are outside."])
    c += S.say("Ambrosine", ["It has to scan, Piper.",
                             "I won't have it not scanning."])
    c += S.say("Piper", ["It will scan."])
    c += S.narrate([
        "It takes the afternoon. Ambrosine gives up the orphan",
        "for a mother in a kitchen, and Merribell for a glass of",
        "water, and fights for the wolf for an hour."])
    c += S.say("Ambrosine", ["There is always a wolf."])
    c += S.say("Piper", ["There was a goat. It sent its",
                         "apologies to the meeting. It is in",
                         "the minutes."])
    c += S.narrate(["Ambrosine looks at the Committee Records for a long",
                    "time, and then at her niece."])
    c += S.say("Ambrosine", ["...A goat is a sort of",
                             "wolf. If you squint."])
    for canto in FIXED_CANTOS:
        c += S.narrate(canto)
    c += S.say("Ambrosine", ["The middle is worse."])
    c += S.say("Piper", ["The middle is true."])
    c += S.say("Ambrosine", ["...It scans. Just."])
    c += S.narrate([
        "She signs the fair copy A. QUILL, and hands Piper the",
        "pen, and Piper signs under her, and it is the first",
        "account in four generations with two Quills on it."])
    c += S.narrate([
        "Across the hall the Clerk stamps it AMENDED, which he",
        "has not had cause to do before, and looks pleased."])
    c += [R.control_switch(db.SW_PIP1_FIXED, True)]
    return c


def _pip1_fight():
    """Fight it: a letter to the Committee, which approved it. Nothing ends,
    and the choice is put again on the next visit."""
    c = S.say("Piper", ["Piper Quill will fight it."])
    c += S.say("Ambrosine", ["With what, dear?"])
    c += S.say("Piper", ["A letter. To the Committee."])
    c += S.say("Ambrosine", ["The Committee approved it.",
                             "You'd be writing to tell them they",
                             "had approved it. They know. They",
                             "were there."])
    c += S.narrate([
        "Piper writes it anyway, three sides, in the third",
        "person, and carries it across the hall to the Clerk,",
        "who reads it, and stamps it, and files it."])
    c += S.say("Clerk", ["Filed under 'no change'."])
    c += S.say("Piper", ["...Piper Quill will think of",
                         "something else."])
    return c


def _pip1_end():
    c = [R.gain_item(db.IT_AUTHORISED, 1), R.play_me("Item")]
    c += S.got(["Got \\I[189]\\C[3]The Authorised Version\\C[0]."])
    c += [R.control_switch(db.SW_PIP1_DONE, True)]
    c += S.companion_story(db.PIPER)
    return c


def _pip1_choice():
    return R.choice_block(
        ["It's very good", "Fix it", "Fight it"],
        [_pip1_good() + _pip1_end(), _pip1_fix() + _pip1_end(),
         _pip1_fight()], cancel=2)


def _pip1_meet():
    c = S.narrate([
        "A woman in the Quills' crimson is at the Committee's",
        "table with a stack of manuscript squared off in front",
        "of her and a pen she is no longer using."])
    c += S.say("Piper", ["Aunt Ambrosine."])
    c += S.say("Ambrosine", ["Piper. And this is the",
                             "Forty-Eighth. You're shorter."])
    c += S.say("Ambrosine", ["It's done. The official",
                             "account. I started the morning they",
                             "voted. One knows the shape."])
    c += S.say("Piper", ["He hasn't finished yet."])
    c += S.say("Ambrosine", ["The shape has, dear.",
                             "The Committee approved it on Tuesday.",
                             "Sit down. I'll read you the best bits."])
    c += [S.trope(), R.control_switch(db.SW_PIP1_ON, True)]
    c += _pip1_reading()
    c += _pip1_choice()
    return c


def _pip1_again():
    c = S.say("Ambrosine", ["Well? It's still very",
                            "good. It was very good on Tuesday."])
    c += S.narrate([
        "The manuscript is squared off on the table, twelve",
        "cantos, APPROVED, with a wolf in it."])
    c += _pip1_choice()
    return c


def _pip1_alone():
    return S.say("Ambrosine", ["Where is my niece? I",
                               "have a question about a rhyme, and",
                               "she will have an answer, and it will",
                               "be the wrong one."])


def _pip1_after():
    good = S.say("Ambrosine", ["It is a very good",
                               "middle. I read it again most",
                               "mornings. And the footnote."])
    fixed = S.say("Ambrosine", ["A. and P. Quill. It has",
                                "a goat in it now. The goat is in the",
                                "minutes, so I can't object."])
    c = R.if_then(R.condition_switch(db.SW_PIP1_GOOD), good, fixed)
    c += R.if_then(R.condition_actor_in_party(db.PIPER), S.narrate([
        "Piper and her aunt nod to one another, as one",
        "professional to another, which is new."]))
    return c


def ambrosine_event(event_id, x, y):
    """Ambrosine Quill (Map 3), at the Committee's paperwork by the door:
    empty until Piper has been on the road; then the reading and the choice;
    then, for everybody, the account settled."""
    img = R.image(*S.sprite("Ambrosine"), direction=4)
    return R.event(event_id, "Ambrosine Quill", x, y, [
        R.page([], img=R.image(""), priority=0, through=True),
        R.page(_pip1_meet(), img=img, conditions={
            "actorValid": True, "actorId": db.PIPER,
            "switch1Valid": True, "switch1Id": db.SW_LEFT_VILLAGE}),
        R.page(R.if_then(R.condition_actor_in_party(db.PIPER),
                         _pip1_again(), _pip1_alone()), img=img,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_PIP1_ON}),
        R.page(_pip1_after(), img=img, conditions={
            "switch1Valid": True, "switch1Id": db.SW_PIP1_DONE}),
    ])


def wall_page(page0):
    """The Wall of the Forty-Seven (Map 3, event 6), which has no ladder:
    its own page, and the card in the space left for the Forty-Eighth."""
    good = S.narrate([
        "Under the forty-seventh, a space, and a card pinned in",
        "it: THE FORTY-EIGHTH. ACCOUNT BY A. QUILL. APPROVED.",
        "And under that, in small type, one footnote."])
    fixed = S.narrate([
        "Under the forty-seventh, a space, and a card pinned in",
        "it: THE FORTY-EIGHTH. ACCOUNT BY A. AND P. QUILL.",
        "AMENDED. There is a goat in the margin."])
    cmds = page0["list"][:-1] + R.if_then(
        R.condition_switch(db.SW_PIP1_GOOD), good, fixed)
    return [_pip5_page(page0, cmds, {"switch1Valid": True,
                                     "switch1Id": db.SW_PIP1_DONE})]
