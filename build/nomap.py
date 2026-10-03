"""The seven world-map sites with no map behind them.

`../SITES.md` step 7, and `../COMPANIONS.md` section 3's "world-map-only sites":
seven places that are a single event on the world map and nothing else - no
interior, no transfer. Each is a place with its joke in it. The companion
quest that each one eventually serves (HOB-4, ZEPH-5, ZEPH-4, ALD-6, COR-4,
COR-2, ZEPH-2) is not built here; it gets **appended** to the event later, as a
page guarded by whatever that quest sets, which is `../NORTH.md` 1.7's second
pattern and is why building the place first is safe.

It is a cluster module in `hithermost.py`'s shape - `SITES`, a dict of name to
builder, merged into `journey.world_map`'s claims - with no maps, so there is
no `build()` and nothing in `MAP_NAMES`.

* **No world-map coordinate is written here.** Each builder is handed the cells
  of the placeholders it replaces. All seven are one cell, and every one is
  open ground, so each door is walked onto: player-touch, below characters,
  `through` - Olde Evermore's door, with nowhere to go.
* **Every one is two pages.** The first asks before it starts a scene, because
  a world-map cell is walked over by people on their way somewhere else; the
  scene sets self switch A at the end, and page two is the short version. A
  place that never costs the player a window they did not ask for is a place
  they will stop at again.
* **The stamps are what the text describes**, and they were looked at before
  it was written. The Sky Anvil is a `Shrine` - a little stone building with a
  domed top - which the site's heading had right and the step-6 measurement
  had as `Giant Tree (Snow)`; `World_B.txt` and a screenshot both say shrine.
  The Cinder Fen's `Trail` is a path winding off into cracked mud. Ashcombe
  Lake has no stamp: its cell is the grass on the south shore, beside the new
  village.
* **Nobody here needs a global.** Everything that happens once is a self
  switch. Mother Selvidge charges two crowns, not twopence, because the game's
  money is crowns and nothing in it has ever been priced in pence.
"""
import rmmzdata as R

import places
import q_aldric
import q_corvin
import q_hob
import q_wren
import q_zephyrine

import story as S

# The names `worldmap.json`'s door events carry - measured, not guessed, and
# three of them have no "The" in front. A claim that matches nothing fails an
# assertion in `journey.world_map`.
SKY_ANVIL = "Sky Anvil"
LAY_BY = "The Lay-By"
CINDER_FEN = "Cinder Fen"
WRONG_DRAGON = "Wrong Dragon"
FAIR = "The Fair"
ASHCOMBE_LAKE = "Ashcombe Lake"
DUCKS_POND = "The Duck's Pond"

DONE = {"selfSwitchValid": True, "selfSwitchCh": "A"}


def _site(name, stop, first, again, again_stop=None):
    """Two pages. `first` is the scene on a first stop, and it ends by
    setting A; `again` is what the square says after that. With `again_stop`
    the second page asks too, and a stop gets that; without it `again` is a
    single window, for a place with nobody in it."""
    def build(base_id, cells):
        evs = []
        for i, (x, y) in enumerate(sorted(cells)):
            page1 = stop[0] + R.choice_block(
                [stop[1], "Press on"],
                [first + [R.self_switch("A")], S.narrate(["You press on."])])
            if again_stop is None:
                page2 = again
            else:
                page2 = again + R.choice_block(
                    [stop[1], "Press on"], [again_stop, []])
            evs.append(R.event(base_id + i, name, x, y, [
                R.page(page1, img=R.image(""), trigger=1, priority=0,
                       through=True),
                R.page(page2, img=R.image(""), trigger=1, priority=0,
                       through=True, conditions=DONE)]))
        return evs
    return build


# ============================================================ the Sky Anvil ==
# HOB-4. A meteorite fell in 1749 and has been a farm gatepost ever since.
# Elias Meech will not sell it, because it is a very good gatepost, but he will
# trade it for a gate - and he is between gates, which is the whole of him.
def _sky_anvil():
    stop = (S.narrate([
        "A little stone shrine in the snow beside the road,",
        "with a round grey stone set in the top of it like",
        "an egg in an egg cup."]), "Stop a while")
    first = S.narrate([
        "A man in a brown hat is leaning on it, looking at",
        "the field the way a man looks at a field he owns."])
    first += S.say("Meech", [
        "Afternoon. You'll have come about the",
        "gatepost."])
    first += S.narrate(["You ask which gatepost."])
    first += S.say("Meech", [
        "That one. Came down out of the sky in",
        "1749, into the top field, on a Tuesday. My",
        "great-great-grandad set it up for a gatepost,",
        "because it was there."])
    first += S.say("Meech", [
        "Best gatepost in the county. It's",
        "outlasted eleven gates."])
    first += S.narrate(["You ask about the shrine."])
    first += S.say("Meech", [
        "That's the pilgrims. They call it the",
        "Sky Anvil. Built that round the foot of it",
        "in 1750, and they come up every summer to",
        "look at it. I don't mind. Keeps the frost off."])
    first += [S.trope()]
    first += R.choice_block(["Offer to buy it", "Admire it"], [
        S.say("Meech", ["It's not for sale. It's a very good",
                        "gatepost."]) +
        S.narrate(["He considers the field."]) +
        S.say("Meech", ["I'd take a gate for it, mind. The last",
                        "one went at Michaelmas. I'm between gates."]) +
        S.narrate(["You ask what he would hang a gate on, then."]) +
        S.say("Meech", ["The shrine. It's a very good shrine."]),
        S.narrate(["You admire it. It is a very good gatepost."]) +
        S.say("Meech", ["It is. Wants a gate, mind."])])
    again = S.narrate([
        "The Sky Anvil, in the snow, with no gate on it.",
        "Elias Meech is leaning on it."])
    again_stop = S.say("Meech", [
        "Still between gates. If you come across",
        "a good one, you know where I am."])
    site = _site(SKY_ANVIL, stop, first, again, again_stop)

    def build(base_id, cells):          # HOB-4's two pages, appended
        evs = site(base_id, cells)
        for ev in evs:
            ev["pages"] += q_hob.sky_anvil_pages(again)
        return evs
    return build


# ============================================================== the Lay-By ==
# ZEPH-5. Three hedge mages, an association, nine years without a name, and a
# lay-by on the west road because none of them will host. The igloo on the
# grass is `../WORLDMAP.md` 4's and is kept on purpose: it is neutral ground,
# conjured the first winter, and the one thing they have ever done together.
def _lay_by():
    stop = (S.narrate([
        "An igloo, on the grass, at the end of a lay-by on",
        "the west road. It is not melting. There are voices",
        "inside it, disagreeing politely."]), "Look in")
    first = S.narrate([
        "Three people are sitting round a folding table in",
        "the igloo, with the minutes of a meeting."])
    first += S.say("Miss Privet", [
        "Oh! A member of the public.",
        "Do come in. This is the ninth annual general",
        "meeting of the..."])
    first += S.say("Mrs Quickset", ["Of the association."])
    first += S.say("Dunnock", ["Of the association of hedge mages."])
    first += S.say("Miss Privet", ["Which is not its name."])
    first += S.say("Mrs Quickset", [
        "It hasn't got a name. That's",
        "item one."])
    first += S.narrate(["You ask how long item one has been item one."])
    first += S.say("Dunnock", ["Nine years."])
    first += S.narrate(["You ask about the igloo."])
    first += S.say("Mrs Quickset", [
        "Neutral ground. None of us",
        "would host, so I made it, the first winter.",
        "It isn't anybody's house, so nobody has to",
        "do the biscuits."])
    first += S.say("Miss Privet", [
        "It hasn't melted in nine",
        "years. It is the one thing the association",
        "has ever agreed on."])
    first += S.say("Dunnock", ["We didn't agree on it. She just",
                      "did it."])
    first += [S.trope()]
    first += S.say("Miss Privet", [
        "Would the member of the",
        "public care to propose a name? Strictly for",
        "the minutes."])
    first += R.choice_block(['"The Hedge Mages"', "Say nothing"], [
        S.say("Mrs Quickset", ["Too obvious. People would",
                               "know what we are."]) +
        S.say("Dunnock", ["Carried forward."]) +
        S.narrate(["Miss Privet writes it in the minutes, under nine",
                   "years of other things carried forward."]),
        S.say("Miss Privet", ["The member of the public",
                              "abstains. Noted."])])
    first += S.say("Dunnock", [
        "Self-taught, me. The book I",
        "learned from had four pages missing, so I",
        "worked those four out for myself. Did them",
        "better, as it turns out."])
    first += S.say("Dunnock", [
        "I'm better than the whole Collegium at",
        "exactly four things."])
    again = S.narrate([
        "The igloo in the lay-by. Item one is still under",
        "discussion."])
    again_stop = S.say("Miss Privet", [
        "Item one, carried forward.",
        "Do sit down."])
    site = _site(LAY_BY, stop, first, again, again_stop)

    def build(base_id, cells):          # ZEPH-5's two pages, appended
        evs = site(base_id, cells)
        for ev in evs:
            ev["pages"] += q_zephyrine.lay_by_pages()
        return evs
    return build


# ============================================================ the Cinder Fen ==
# ZEPH-4. Nine hundred acres that need burning, which everybody agrees about,
# and a Drainage Commissioner with the form. The quest is the fire person; the
# place is the form.
def _cinder_fen():
    stop = (S.narrate([
        "A path goes out into the Cinder Fen and gives up.",
        "Under the cracked mud on top, nine hundred acres",
        "of water are drowning a road a foot at a time."]),
        "Stop a while")
    first = S.narrate([
        "A person with a clipboard is standing where the",
        "path gives up, in wellingtons, looking at it."])
    first += S.say("Commissioner", [
        "Are you a fire person?",
        "You don't look like a fire person."])
    first += S.narrate(["You say you are a turnip person."])
    first += S.say("Commissioner", [
        "Ah. It wants burning, you see.",
        "The Fen. Nine hundred acres.",
        "Everybody agrees."])
    first += S.say("Commissioner", [
        "It's the traditional remedy,",
        "and nobody in the parish has been able",
        "to do it since Mr Tinder retired."])
    first += S.say("Commissioner", [
        "It's all approved.",
        "Here's the form. In triplicate: one for the",
        "parish, one for the county, and one to come",
        "back to me afterwards, signed."])
    first += S.narrate(["You ask who by."])
    first += S.say("Commissioner", [
        "The fire person.",
        "And countersigned by the Fen."])
    first += S.narrate(["You ask how a fen signs a form."])
    first += S.say("Commissioner", [
        "There's a box for it.",
        "I've never had one back."])
    again = S.narrate([
        "The Cinder Fen, unburnt. The Drainage Commissioner",
        "is still waiting for a fire person."])
    again_stop = S.say("Commissioner", [
        "Still wet. The form's still good.",
        "It doesn't expire. I made sure of that."])
    return _site(CINDER_FEN, stop, first, again, again_stop)


# ========================================================== the Wrong Dragon ==
# ALD-6. Eight years ago a young knight was sent to slay a dragon and arrived
# at a different one. The different one is delightful, elderly and well read,
# and is not remotely a dragon in the sense the commission meant. What it *is*
# is a closed subject - `../NORTH.md` 1.3's fifth mechanism - so it speaks as
# "Somebody Large" and nothing on the page says more. Mrs Emberthwaite is a
# dragon in every sense and is on her hill in `fairholme.py`; this is not her.
def _wrong_dragon():
    stop = (S.narrate([
        "A cave in the rocks above the water. Something",
        "very large is breathing inside it, slowly, the way",
        "people breathe when they are reading."]), "Call in")
    first = S.say("Somebody Large", [
        "Come in, come in.",
        "Mind the books. They're in the order",
        "I read them, which is nobody else's."])
    first += S.narrate([
        "It is dark inside, and warm, and full of books.",
        "Something enormous is in an armchair at the back,",
        "with a blanket over what you think are its knees."])
    first += S.say("Somebody Large", [
        "Is it about the dragon?",
        "It's usually about the dragon."])
    first += S.narrate(["You ask whether it is the dragon."])
    first += S.say("Somebody Large", [
        "I'm a dragon, dear,",
        "in the sense that the map says so.",
        "I'm not a dragon in the sense anybody means."])
    first += S.say("Somebody Large", [
        "People are generally relieved,",
        "and then a little disappointed,",
        "and then they stay for tea."])
    first += S.say("Somebody Large", [
        "There was a young knight,",
        "oh, eight years ago. Very correct."])
    first += S.say("Somebody Large", [
        "He had a commission with",
        "'dragon' on it and a great deal of armour,",
        "and we talked about Horace until it got dark."])
    first += S.say("Somebody Large", [
        "I do hope he found his dragon.",
        "He was so looking forward to it."])
    first += [S.trope()]
    again = S.narrate([
        "The Wrong Dragon's cave. Somebody inside turns a",
        "page."])
    again_stop = S.say("Somebody Large", [
        "Come in, dear. I've just got",
        "to the good bit. You can have it after me."])
    site = _site(WRONG_DRAGON, stop, first, again, again_stop)

    def build(base_id, cells):          # ALD-6's two pages, appended
        evs = site(base_id, cells)
        for ev in evs:
            ev["pages"] += q_aldric.dragon_pages(ev["pages"][-1])
        return evs
    return build


# ================================================================= the Fair ==
# COR-4. Mother Selvidge, who remembers nothing, is never wrong, and says the
# rival thing to four young men a year. That last is Corvin's quest and is not
# spent here; what she tells Bram is what she tells everybody, and it is true.
def _fair():
    stop = (S.narrate([
        "A big tent in the sand, with a fair in it, a long",
        "way from anywhere, the way fairs always are."]),
        "Go to the fair")
    reading = [R.lose_gold(2), R.play_se("Coin")]
    reading += S.narrate([
        "She takes your hand and looks at it for a long",
        "time, and then at you, for longer."])
    reading += S.say("Mother Selvidge", [
        "You're going to go a long",
        "way, and meet a great many people, and at",
        "the end of it somebody is going to be very",
        "surprised to see you."])
    reading += S.say("Mother Selvidge", [
        "And you'll eat a turnip.",
        "That one's free."])
    reading += S.narrate(["You ask whether she is ever wrong."])
    reading += S.say("Mother Selvidge", [
        "Not once, dear. Ask",
        "anybody I've read."])
    reading += [S.trope()]
    reading += [R.self_switch("A")]
    first = S.narrate([
        "Swingboats, a coconut shy with no coconuts, and at",
        "the back of the tent a little striped booth:",
        "MOTHER SELVIDGE. NEVER WRONG. TWO CROWNS."])
    first += S.say("Mother Selvidge", [
        "Cross my palm, dear. Two",
        "crowns."])
    first += R.choice_block(["Pay 2cr", "Not today"], [
        R.if_then(R.condition_script("$gameParty.gold() >= 2"), reading,
                  S.say("Mother Selvidge", [
                      "Two crowns, dear. The",
                      "cards don't do credit."])),
        S.say("Mother Selvidge", [
            "Suit yourself. You'll be",
            "back. I know you will."])])

    def build(base_id, cells):
        # Not `_site`: the scene only counts as having happened if she was
        # paid, so the self switch is set inside the branch that pays her.
        evs = []
        for i, (x, y) in enumerate(sorted(cells)):
            page1 = stop[0] + R.choice_block(
                [stop[1], "Press on"], [first, S.narrate(["You press on."])])
            again = S.narrate([
                "The fair in the big tent. Mother Selvidge is at",
                "the back, shuffling."])
            again += R.choice_block([stop[1], "Press on"], [S.say(
                "Mother Selvidge", [
                    "Same again? It'll be the",
                    "same again, dear. Keep your money."]), []])
            evs.append(R.event(base_id + i, FAIR, x, y, [
                R.page(page1, img=R.image(""), trigger=1, priority=0,
                       through=True),
                R.page(again, img=R.image(""), trigger=1, priority=0,
                       through=True, conditions=DONE)]))
            evs[-1]["pages"] += q_corvin.fair_pages(evs[-1]["pages"][-1])  # COR-4
        return evs
    return build


# ============================================================ Ashcombe Lake ==
# COR-2. The old Ashcombe is under the lake, and the lake is drawn down one
# week a year for the sluices; if you are there that week you can walk in.
# This is not that week, and the drowned street is step 14's if it is ever
# wanted. Nobody here: the Standing Stones' precedent.
def _ashcombe_lake():
    stop = (S.narrate([
        "Ashcombe Lake, deep and still, with the new",
        "Ashcombe a few steps from its shore."]), "Stop a while")
    first = S.narrate([
        "The old Ashcombe is down there. Once a year they",
        "let the lake down for the sluices, for a week, and",
        "the old street comes up for air. Not this week."])
    first += S.narrate([
        "They say that on a still day you can hear the old",
        "church bell ringing under the water."])
    first += [S.trope()]
    first += S.narrate(["It is a still day. You listen."])
    first += [R.wait(60), R.play_se("Bell1", volume=60), R.wait(60)]
    first += S.narrate([
        "A bell rings. It is up the road in the new",
        "Ashcombe, calling somebody in for their dinner.",
        "They took it with them."])
    again = S.narrate([
        "Ashcombe Lake, well up over the old street. Not",
        "this week."])
    site = _site(ASHCOMBE_LAKE, stop, first, again)

    def build(base_id, cells):          # COR-2's two pages, appended
        assert sorted(cells) == [places.ASHCOMBE_LAKE], cells
        evs = site(base_id, cells)
        for ev in evs:
            ev["pages"] += q_corvin.lake_pages(ev["pages"][-1])
        return evs
    return build


# ========================================================== the Duck's Pond ==
# ZEPH-2. Four miles from the Collegium, a duck that is an honorary Fellow,
# holds a chair, votes in Congregation, and has four hit points. The escort
# is the quest; the pond is the duck.
def _ducks_pond():
    stop = (S.narrate([
        "A small pond, four miles from the Collegium, with",
        "a duck on it."]), "Stop a while")
    first = S.narrate([
        "Round the duck's neck, on a ribbon, is the little",
        "silver medal the Collegium gives its Fellows."])
    first += S.narrate([
        "It sets off across the pond to get a better look",
        "at you, and walks into the bank. Then, with great",
        "dignity, into the bank again."])
    first += R.choice_block(["Bow", "Leave it be"], [
        S.narrate(["You bow. The duck inclines its head, as one",
                   "Fellow to a member of the public."]),
        S.narrate(["You leave it be. It looks as if it has a great",
                   "deal on."])])
    again = S.narrate([
        "The duck's pond. The Fellow is in residence."])
    site = _site(DUCKS_POND, stop, first, again)

    def build(base_id, cells):          # ZEPH-2's three pages, appended
        evs = site(base_id, cells)
        for ev in evs:
            ev["pages"] += q_zephyrine.pond_pages()
            ev["pages"].append(q_wren.pond_page())          # WRE-1
        return evs
    return build


# One claim per name the world map carries - `journey.world_map` merges this
# into its `claims` dict. Seven names, seven cells, no maps.
SITES = {
    SKY_ANVIL: _sky_anvil(),
    LAY_BY: _lay_by(),
    CINDER_FEN: _cinder_fen(),
    WRONG_DRAGON: _wrong_dragon(),
    FAIR: _fair(),
    ASHCOMBE_LAKE: _ashcombe_lake(),
    DUCKS_POND: _ducks_pond(),
}
