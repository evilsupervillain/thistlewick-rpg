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
