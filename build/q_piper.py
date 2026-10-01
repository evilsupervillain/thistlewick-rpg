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
# the green curtain in Prophecy Hall, and getting at it is a form, a key and
# a distraction - the last of which is what a party is for.
#
# * **What is in the box is never printed.** The player sees the count, which
#   is `VAR_BLUSHES` read back - the number the game has been keeping all
#   along - and Piper's face, and one verse: forty-one, which is about a
#   hedge, and is entirely innocent, and was struck anyway.
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
    "  'The Elder's hedge, one summer, grew",
    "  much higher than the chapel wall;",
    "  he trimmed it every Tuesday, through",
    "  to autumn, and he trimmed it all.'",
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
                           "Behind the green curtain, I'd say. It's",
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
    """The green curtain in the north wall: behind it, a door. With the key,
    through it, to `archive` - (map, x, y), the archive's arrival."""
    door = S.narrate(["A window with green curtains, drawn. Behind",
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
        "only that one. Verse forty-one. It is about a hedge."])
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

