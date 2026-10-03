"""Wren Halloway's companion quests - `COMPANIONS.md`, her section, and
`QUESTS.md` for the order they are built in.

Nothing here draws a map. Each quest is new events and pages appended to
events other modules own, and those modules call in here for them, the way
`north.py` calls `field.ott_field_pages()`. This module imports no place
module - the dependency runs one way, into it.

WRE-2, The Second Plaque (`QUESTS.md` A1)
-----------------------------------------
She was asked to leave the Slain Wyvern for saying the wyvern is a goose. It
is a goose. What she wants is a retraction, and what she gets is a second
plaque beside the first, which neither corrects it nor repeats it.

* **It hangs off the goose, not off Dorcas.** Dorcas (Map 14, event 2) is a
  five-page Feud ladder, and a page appended below it would have to wait on
  `SW_FEUD_DONE` - a thirty-year argument in another town. The goose (event
  14) is a ladder of one self switch, so its appended pages need only A, and
  Dorcas is voiced from the goose already.
* **Readmission is a line.** The goose's first page asks Wren to leave "for
  a bit, while I decide", and the game never actually removes her. So Dorcas
  decides.
* **The plate is engraved at Wick & Barrow's at a crown a letter**, which is
  what makes Wren concise: `PLATE` is what is on the brass, and its price is
  counted off it, not typed.
* **The quest giver keeps the quest** (`COMPANIONS.md` 1.1). Everything
  between the ask and the handover is global - `SW_WRE2_ASKED` and the plate
  itself - so a Wren dismissed halfway leaves the errand exactly where it
  was. Once the wording is left with Mrs Barrow the plate can be paid for
  without her; it is only put up with her standing there.

WRE-5, Bramus (`QUESTS.md` A2)
------------------------------
She names a small brown thing in Bram's own turnip field after him, and then
explains why. One scene, on one event in the field.

* **Nobody without her sees the burrow.** Its first page needs Wren, so a
  game that never recruits her has no page there at all and Map 1 is what
  it was. Once it is named there is a labelled stick beside it, and that is
  there for everybody.
* **Named is a global switch, `SW_WRE5_NAMED`, not a self switch.** Nothing
  else reads it yet; the ending will. `SW_STORY[WREN]` says only that one of
  her quests was finished, and the Bramus line in the ending is not true of
  a party that only put up a plaque.
"""
import copy

import db
import mapkit as K
import rmmzdata as R
import story as S

# The second plaque, as it is engraved. Four lines of narration, 60 wide.
PLATE = [
    "A GREYLAG GOOSE, ANSER ANSER, OF A FARM ON THIS COAST.",
    "MADE INTO A WYVERN IN 1940, IN TWO DAYS, WITH WIRE,",
    "BY H. VANCE, CHOSEN ONE #41,",
    "BECAUSE THE VILLAGE WAS WAITING ON THE QUAY.",
]
# A crown a letter, and a figure is not a letter. Said aloud below as "a
# hundred and twenty-eight", so the assert is what keeps the line honest.
PLATE_PRICE = sum(c.isalpha() for line in PLATE for c in line)
assert PLATE_PRICE == 128, PLATE_PRICE


def _goose_page(cmds, extra_conditions):
    """A page on the goose, in the goose's own dress: no image, through,
    direction fixed, action button. Every one needs its self switch A - the
    story told once - and Wren."""
    conditions = {"selfSwitchValid": True, "selfSwitchCh": "A",
                  "actorValid": True, "actorId": db.WREN}
    conditions.update(extra_conditions)
    return R.page(cmds, img=R.image(""), trigger=0, priority=1,
                  direction_fix=True, through=True, conditions=conditions)


def goose_pages():
    """Pages 3-5 of the goose (Map 14, event 14). Pages 1-2 are
    `south.the_wyvern`'s and are untouched; without Wren none of these can
    be chosen, and the goose is what it always was."""
    # -- 3: the ask. Or, once asked, where the brass is to be had.
    ask = S.narrate([
        "Wren has been standing in front of the goose for",
        "some time."])
    ask += S.say("Wren", ["Mrs Thrupp. I'd like a retraction."])
    ask += S.say("Dorcas", ["No."])
    ask += S.say("Wren", ["I haven't said of what."])
    ask += S.say("Dorcas", [
        "You've been saying of what since",
        "you walked in. No."])
    ask += S.narrate(["She comes down the bar, wiping her hands."])
    ask += S.say("Dorcas", [
        "He was a good man. He brought back",
        "what he could. That plaque stays up",
        "as long as I do, and so does he."])
    ask += S.narrate([
        "It is not said loudly. It is the tone that ends a",
        "conversation, and the whole room knows it, and",
        "nobody looks up."])
    ask += S.narrate([
        "Wren is quiet for longer than you have ever known",
        "her to be quiet."])
    ask += S.say("Wren", ["Then I don't want it down."])
    ask += S.say("Wren", [
        "I want one beside it. One that",
        "doesn't correct it and doesn't",
        "repeat it. What she is. Where she",
        "came from. Who made her, and why."])
    ask += S.narrate(["Dorcas looks at her for a while."])
    ask += S.say("Dorcas", ["Brass. Not paper. This is a house."])
    ask += S.say("Dorcas", ["And I read it first."])
    ask += [R.control_switch(db.SW_WRE2_ASKED, True), S.trope()]
    ask += S.say("Wren", [
        "Wick & Barrow's engrave. There's a",
        "card in the basket by the counter."])

    asked = S.narrate([
        "Wren looks at the goose, and then at the bare wall",
        "on the other side of the fireplace, which she has",
        "already measured."])
    asked += S.say("Wren", ["Wick & Barrow's. By the letter."])

    first = R.if_then(R.condition_switch(db.SW_WRE2_ASKED), asked, ask)

    # -- 4: the handover. She reads it twice and says nothing.
    up = S.narrate([
        "Wren holds up the plate and says nothing at all.",
        "Dorcas comes the length of the bar to take it."])
    up += S.narrate(["Dorcas reads it."])
    up += [R.wait(40)]
    up += S.narrate(["She reads it again."])
    up += [R.wait(40)]
    up += S.narrate([
        "She says nothing. She fetches a screwdriver from",
        "behind the bar, and a chair, and she puts it up",
        "herself, on the other side of the fire."])
    up += [R.gain_item(db.IT_BRASS_PLATE, -1), R.play_se("Hammer", pitch=120),
           R.wait(30), R.play_se("Hammer", pitch=120), R.wait(40)]
    up += S.narrate([
        "Two plaques, one either side of the fireplace.",
        "Neither of them mentions the other."])
    up += S.say("Dorcas", [
        "I said out. For a bit.",
        "While I decided."])
    up += S.say("Dorcas", ["Decided."])
    up += S.narrate([
        "She goes back behind the bar. That is the whole of",
        "the ceremony."])
    up += S.say("Wren", ["I hadn't noticed I was out."])
    up += S.narrate([
        "Nobody in the room believes her and nobody says so,",
        "which is the Slain Wyvern's way of letting somebody",
        "back in."])
    up += [R.control_switch(db.SW_WRE2_ASKED, False),
           R.control_switch(db.SW_WRE2_UP, True)]
    up += S.companion_story(db.WREN)

    # -- 5: afterwards, with her.
    after = S.say("Wren", [
        "Greylag. Adult female.",
        "Two days, with wire."])
    after += S.narrate([
        "She says it the way other people read a name off",
        "a memorial."])

    return [
        _goose_page(first, {}),
        _goose_page(up, {"itemValid": True, "itemId": db.IT_BRASS_PLATE}),
        _goose_page(after, {"switch1Valid": True,
                            "switch1Id": db.SW_WRE2_UP}),
    ]


def second_plaque(event_id, x, y):
    """The plaque on the right of the fireplace (Map 14), the mirror of event
    18 on its left. Like that one it is a place to read rather than a
    sprite, and it has no page at all until it has been put up."""
    read = S.narrate(["A second brass plaque, on the other side of the",
                      "fire from the first:"])
    read += S.narrate(["'" + PLATE[0]] + PLATE[1:-1] + [PLATE[-1] + "'"])
    read += S.narrate(["Somebody has polished this one too."])
    return R.event(event_id, "The Second Plaque", x, y, [
        R.page(read, img=R.image(""), trigger=0, priority=1,
               direction_fix=True, through=True,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_WRE2_UP}),
    ])


def engraving_card(event_id, x, y):
    """A card in Mrs Barrow's basket (Map 16) - a new thing to read for
    everybody, and the engraver for WRE-2. Mrs Barrow is a page ladder of her
    own, with the forty bolts of oilskin appended to it, so the engraving is
    done from here and she only speaks.

    Page 2 is the negotiation, which needs Wren: the wording is hers. Once it
    has been settled it is left with Mrs Barrow - self switch A - and page 3
    takes the money from whoever is holding it. Page 4 is the plate, done,
    for as long as it is being carried."""
    card = S.narrate([
        "Tucked into the basket, a card in a careful hand:",
        "ENGRAVING. BRASS. A CROWN A LETTER.",
        "SPACES FREE."])

    def pay():
        done = [R.lose_gold(PLATE_PRICE)]
        done += S.narrate([
            "Mrs Barrow takes the sheet into the back. There is",
            "tapping, and then a long silence, and then more",
            "tapping."])
        done += [R.gain_item(db.IT_BRASS_PLATE, 1), R.play_me("Item")]
        done += S.got(["Got \\I[188]\\C[3]A Brass Plate\\C[0].",
                       "Four lines, no name on it, and the edges done."])
        short = S.say("Mrs Barrow", [
            "A hundred and twenty-eight. It'll",
            "keep. It's brass."])
        return R.choice_block(
            ["Pay %d crowns" % PLATE_PRICE, "Not now"],
            [R.if_then(R.condition_script(
                "$gameParty.gold() >= %d" % PLATE_PRICE), done, short),
             S.say("Mrs Barrow", ["It'll keep. It's brass."])],
            cancel=1)

    wording = S.narrate([
        "Wren reads the card. Then she takes out a sheet of",
        "paper, written on both sides and up one margin, and",
        "hands it to Mrs Barrow."])
    wording += S.say("Mrs Barrow", ["Letters, love, not words.",
                                     "Let's see."])
    wording += S.narrate(["Mrs Barrow counts with a pencil. It takes a while."])
    wording += S.say("Mrs Barrow", [
        "One thousand, four hundred and",
        "twelve crowns."])
    wording += S.narrate([
        "Wren takes the sheet back and sits down on a barrel",
        "with it. She crosses things out. Every line she",
        "crosses out, she reads aloud first, fondly."])
    wording += S.narrate(["The Latin goes last. Then it comes back."])
    wording += S.say("Wren", ["There."])
    wording += S.narrate(["Mrs Barrow counts again."])
    wording += S.say("Mrs Barrow", [
        "A hundred and twenty-eight.",
        "No name on it?"])
    wording += S.say("Wren", ["It isn't about me."])
    wording += [R.self_switch("A", True)]
    wording += pay()

    no_wren = S.narrate([
        "The card offers brass at a crown a letter. The",
        "letters are Wren's, and Wren is not here to say",
        "which ones."])

    asked = R.if_then(R.condition_actor_in_party(db.WREN), wording, no_wren)

    settled = S.say("Mrs Barrow", [
        "Your friend's plaque. I've the",
        "wording here, pinned up."])
    settled += pay()

    ready = S.say("Mrs Barrow", [
        "That's yours, done. Mind the edges,",
        "and mind whose wall it goes on."])

    img = R.image("")
    return R.event(event_id, "The Engraving Card", x, y, [
        R.page(card, img=img, trigger=0, priority=1),
        R.page(asked, img=img, trigger=0, priority=1,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_WRE2_ASKED}),
        R.page(settled, img=img, trigger=0, priority=1,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_WRE2_ASKED,
                           "selfSwitchValid": True, "selfSwitchCh": "A"}),
        R.page(ready, img=img, trigger=0, priority=1,
               conditions={"itemValid": True,
                           "itemId": db.IT_BRASS_PLATE}),
    ])


def bramus(event_id, x, y):
    """The burrow in the turnip rows (Map 1). The creature is never drawn:
    it is small and brown and of no consequence, and the hole is as much of
    it as anybody but Wren has ever noticed.

    Page 1 is the naming, with Wren and before it - the trope, the blush,
    and her story. Page 2 is the label she leaves, for everybody. Page 3 is
    the burrow afterwards with her there, which outranks it."""
    look = S.narrate([
        "A neat hole in the turnip row, with a rim of turned earth.",
        "Wren is down on her knees beside it before you have",
        "finished looking at it."])
    look += S.say("Wren", ["Don't move. Don't breathe on it."])
    look += S.narrate([
        "Something small and brown comes out of the hole. It",
        "looks at nothing in particular, and walks directly",
        "into the path of a wheelbarrow."])
    look += [R.play_se("Damage1", pitch=70), R.wait(30)]
    look += S.narrate([
        "The barrow goes over it. It comes out of the other",
        "side of the barrow a little flatter, shakes itself,",
        "and carries on."])
    look += [R.play_se("Crow"), R.wait(20)]
    look += S.narrate([
        "A crow drops on it from a height, misses, hits the",
        "barrel, and leaves with a great deal of dignity."])
    look += S.say("Wren", [
        "They're all over this field. Nobody",
        "has ever described one. Nobody has",
        "ever looked."])
    look += S.say("Wren", [
        "It's new. It's got no name.",
        "I'm naming it after you."])
    look += S.narrate([
        "Nobody has ever named anything after you. The last",
        "honour you were given, you were asleep for."])
    look += S.narrate([
        "You find you have had to sit down on a turnip."])
    look += S.narrate(["She has her notebook open."])
    look += [R.play_se("Book1"), R.wait(20)]
    look += S.say("Wren", [
        "Bramus agricola. Diet, turnip.",
        "Predators, everything. Of no",
        "consequence whatsoever."])
    look += S.say("Wren", [
        "Remarkable for one attribute. It",
        "survives things it has no business",
        "surviving. By luck. Repeatedly."])
    look += S.say("Wren", [
        "I shall be calling it statistically",
        "indefensible. In print."])
    look += [S.trope()]
    look += S.narrate([
        "She looks at you, and then at the hole, and then at",
        "you, with the patience of somebody waiting for a",
        "specimen to confirm a hypothesis."])
    look += S.narrate([
        "You think about the Gloamwood, and the tower, and",
        "everything since the vote, and how much of it you",
        "walked away from, and why."])
    look += S.narrate([
        "It is accurate. Nobody has ever described you",
        "accurately before. It turns out to be exactly the",
        "same feeling as being deeply touched."])
    look += S.say("Wren", [
        "Breeds March to October, and is",
        "enthusiastic about it. With its",
        "record, it can afford to be."])
    look += [S.blush()]
    look += S.narrate([
        "She writes that down, under your name. You would",
        "like to discuss which name, and cannot find a way",
        "to begin."])
    look += S.narrate([
        "She pushes a stick into the earth beside the hole",
        "and ties a label to it."])
    look += [R.control_switch(db.SW_WRE5_NAMED, True)]
    look += S.companion_story(db.WREN)

    label = S.narrate([
        "A neat hole in the turnip row. On a stick beside it is a",
        "label, in a small careful hand:"])
    label += S.narrate([
        "\\C[6]BRAMUS AGRICOLA (HALLOWAY).",
        "DO NOT PLOUGH. IT WILL NOT HELP.\\C[0]"])

    again = S.say("Wren", ["Still here."])
    again += S.narrate(["Of course it is."])

    img = R.image(tile_id=K.BURROW)
    named = {"switch1Valid": True, "switch1Id": db.SW_WRE5_NAMED}
    return R.event(event_id, "Bramus's Burrow", x, y, [
        R.page(look, img=img, trigger=0, priority=1, direction_fix=True,
               conditions={"actorValid": True, "actorId": db.WREN}),
        R.page(label, img=img, trigger=0, priority=1, direction_fix=True,
               conditions=named),
        R.page(again, img=img, trigger=0, priority=1, direction_fix=True,
               conditions=dict(named, actorValid=True, actorId=db.WREN)),
    ])


# ======================================================================
# WRE-3, The Thing In The Gloamwood (`QUESTS.md` A11)
# ----------------------------------------------------------------------
# There is a society: nine members, a newsletter, an annual walk and forty
# years of sightings. Wren proves the Thing does not exist and never did, and
# the society is delighted - they have been trying to prove it since 1960 -
# except for the one member who saw it, who is looked after by everybody
# else and is fine by the end of the walk.
#
# * **The game had already planted the answer.** The nest on the first path
#   says there are nine of them because the crest works; the shed skin says
#   everything killed that week was courting; and the Thing the party fought
#   was "difficult to say how much of it there is". It was never one thing.
#   It was nine crested grass snakes, knotted, in season, seen at dusk.
# * **The society meets in the Gilded Turnip** (Map 4), three of them at a
#   table of their own, for everybody. Wren's page is on the chair, after the
#   Thing is dealt with. While the walk is on the three are out of the inn and
#   all nine are in the deep wood's clearing (Map 10), where the Thing stood.
# * **The proof needs Wren.** The walk is a global switch, so a Wren
#   dismissed before she gets there leaves the society waiting in the clearing
#   until she comes back.
# * **Her gear is the badge** (`QUESTS.md` 0.5): an armour type nobody else
#   can wear, allowed on her actor alone.
WRE3_SPEAKERS = [            # (key, event name, speaker, the inn cell, facing)
    ("lumb", "Mrs Lumb (the Gloamwood Society)", "Mrs Lumb", (11, 11), 6),
    ("dunmore", "Mr Dunmore (the Gloamwood Society)", "Mr Dunmore",
     (13, 11), 4),
    ("pellow", "Miss Pellow (the Gloamwood Society)", "Miss Pellow",
     (12, 10), 2),
]
WRE3_TABLE = (12, 11)
# The walk, round the clearing on Map 10. The Thing stood at (15, 10) and the
# path comes up the middle, so that column is left clear.
WRE3_WALK = {"lumb": ((15, 9), 2), "dunmore": ((16, 9), 2),
             "pellow": ((13, 10), 6)}
WRE3_EXTRAS = [              # six more members, who have no lines
    ((12, 10), 6, "People2", 3), ((18, 10), 4, "People3", 2),
    ((17, 10), 4, "People1", 7), ((14, 8), 2, "People4", 0),
    ((16, 8), 2, "People2", 6), ((17, 9), 4, "People3", 4),
]
BADGE_ICON = 146


def _wre3_img(speaker, direction):
    sheet, index = S.FACES[speaker]
    return R.image(sheet, index, direction=direction)


def _wre3_ask():
    c = S.say("Mrs Lumb", ["You'll be Miss Halloway. The one",
                           "who said the goose was a goose."])
    c += S.say("Wren", ["It is a goose. I'd like to see",
                        "your sightings."])
    c += S.narrate([
        "Mr Dunmore produces forty years of The Sighting,",
        "bound by the year, from under the table. Wren reads",
        "all of it. It takes the rest of the afternoon."])
    c += S.say("Wren", ["I can prove it doesn't exist.",
                        "That it never did."])
    c += S.narrate([
        "You brace yourself. The Gloamwood Society, as one,",
        "leans forward."])
    c += S.say("Mrs Lumb", ["Can you? Oh - can you really?"])
    c += S.say("Mr Dunmore", ["We've been trying to since 1960!"])
    c += S.say("Mrs Lumb", ["The walk's tonight. It's always",
                            "tonight, when there's news. The deep",
                            "clearing, where it's seen most. Bring",
                            "whatever you've got."])
    c += S.narrate(["Only Miss Pellow, at the end of the table, does",
                    "not lean forward."])
    c += [S.trope(), R.control_switch(db.SW_WRE3_WALK, True)]
    return c


def _wre3_inn(key):
    """The three at their table in the Gilded Turnip, for everybody: before,
    while they are out, and after."""
    if key == "lumb":
        before = S.say("Mrs Lumb", ["The Gloamwood Society. Thursdays.",
                                    "Nine members, forty years, and a",
                                    "walk once a year."])
        before += S.say("Mrs Lumb", ["Any sightings? We take anything.",
                                     "A shape. A smell. A feeling."])
        before += R.if_then(R.condition_switch(db.SW_GLOAMWOOD), S.narrate([
            "You have been in the clearing. Thistlewick will",
            "never believe you, and you are not going to tell",
            "them anyway."]))
        after = S.say("Mrs Lumb", ["Forty years, and proved. Next year's",
                                   "walk is going to be marvellous.",
                                   "There's nothing there."])
    elif key == "dunmore":
        before = S.say("Mr Dunmore", ["Dunmore. Secretary. I edit The",
                                      "Sighting. Forty years and nothing,",
                                      "so far, that would stand up."])
        after = S.say("Mr Dunmore", ["Issue one hundred and sixty. Proof,",
                                     "in writing, by a professional. Our",
                                     "best ever. We've printed extra."])
    else:
        before = S.say("Miss Pellow", ["I saw it, you know. Once. In",
                                       "seventy-one. Nobody's seen it",
                                       "since. I don't mind. I saw it."])
        after = S.say("Miss Pellow", ["Nine. I counted nine.",
                                      "I was the only one who got it right."])
    return before, after


def _wre3_proof():
    c = S.narrate([
        "Nine lanterns in the clearing where the Thing stood,",
        "and nine members of the Gloamwood Society round them,",
        "in good boots, with flasks."])
    c += S.say("Mrs Lumb", ["Here's where it's seen most.",
                            "Miss Halloway. In your own time."])
    c += S.say("Wren", ["Every sighting in forty years has",
                        "between one and nine heads. Mostly",
                        "in late spring. Always at dusk."])
    c += S.say("Wren", ["There's a nest in the fork of a tree",
                        "on the first path, with a crest feather",
                        "in it, and a shed skin on a branch",
                        "near here. Both are one animal."])
    c += S.say("Wren", ["The crested grass snake. Common.",
                        "In spring they gather to court. Nine",
                        "is usual. They knot together."])
    c += S.say("Wren", ["From the path, at dusk, it looks like",
                        "one large thing with a great many heads."])
    c += S.say("Wren", ["It isn't a Thing.",
                        "It's nine of them. Courting."])
    c += [R.wait(30)]
    c += S.say("Mrs Lumb", ["...All at once?"])
    c += S.say("Wren", ["It's the only way they know how."])
    c += [S.blush()]
    c += S.narrate(["Then the Gloamwood Society, as one, cheers."])
    c += [R.play_se("Applause1", volume=70)]
    c += S.say("Mr Dunmore", ["Forty years! Proved! I'll want it",
                              "in writing, Miss Halloway. Best",
                              "issue we've ever had."])
    c += S.narrate([
        "Everybody is delighted, except Miss Pellow, who is",
        "standing a little apart with her lantern, looking",
        "at the place where it was."])
    c += [R.wait(30)]
    c += S.narrate([
        "Nobody says anything to her. Mrs Lumb takes her",
        "lantern, and Mr Dunmore her arm, and on the walk",
        "home the whole society contrives, without anybody",
        "arranging it, to be on either side of her."])
    c += S.say("Miss Pellow", ["I saw it, you know.",
                               "In seventy-one. I wrote it up."])
    c += S.say("Wren", ["I read it. Issue forty-four. 'A great",
                        "many heads, and all of them busy.'"])
    c += S.say("Wren", ["Of forty years of sightings, yours",
                        "is the only accurate one. You counted",
                        "nine. You were right."])
    c += S.say("Miss Pellow", ["...I did count nine."])
    c += S.narrate([
        "By the edge of the wood Miss Pellow is telling",
        "everybody about the nine, and has been for some",
        "time, and nobody minds in the least."])
    c += S.say("Mrs Lumb", ["Honorary membership, Miss Halloway.",
                            "And the badge. We've never given",
                            "one away before."])
    c += [R.gain_armor(db.AR_SOCIETY_BADGE, 1), R.play_me("Item")]
    c += S.got(["Got \\I[%d]\\C[3]Gloamwood Society Badge\\C[0]." %
                BADGE_ICON])
    c += S.say("Wren", ["...It goes on the cloak, I suppose."])
    c += [R.control_switch(db.SW_WRE3_WALK, False),
          R.control_switch(db.SW_WRE3_DONE, True)]
    c += S.companion_story(db.WREN)
    return c


def society_events(base_id):
    """The Gloamwood Society's three, at their table in the Gilded Turnip
    (Map 4). Out of the inn while the walk is on."""
    walk = {"switch1Valid": True, "switch1Id": db.SW_WRE3_WALK}
    done = {"switch1Valid": True, "switch1Id": db.SW_WRE3_DONE}
    evs = []
    for n, (key, name, speaker, (x, y), d) in enumerate(WRE3_SPEAKERS):
        img = _wre3_img(speaker, d)
        before, after = _wre3_inn(key)
        pages = [R.page(before, img=img, direction_fix=True)]
        if key == "lumb":
            pages.append(R.page(_wre3_ask(), img=img, direction_fix=True,
                                conditions={"switch1Valid": True,
                                            "switch1Id": db.SW_GLOAMWOOD,
                                            "actorValid": True,
                                            "actorId": db.WREN}))
        pages.append(R.page([], img=R.image(""), priority=0, through=True,
                            conditions=walk))
        pages.append(R.page(after, img=img, direction_fix=True,
                            conditions=done))
        evs.append(R.event(base_id + n, name, x, y, pages))
    return evs


def walk_events(base_id):
    """All nine on the walk, round the clearing in the deep wood (Map 10),
    only while it is on. Mrs Lumb has the proof, with Wren."""
    walk = {"switch1Valid": True, "switch1Id": db.SW_WRE3_WALK}
    nothing = R.page([], img=R.image(""), priority=0, through=True)
    evs = []
    eid = base_id
    for key, name, speaker, _, _ in WRE3_SPEAKERS:
        (x, y), d = WRE3_WALK[key]
        img = _wre3_img(speaker, d)
        if key == "lumb":
            wait = S.say("Mrs Lumb", ["We'll wait for Miss Halloway.",
                                      "We've waited forty years."])
        elif key == "dunmore":
            wait = S.say("Mr Dunmore", ["Notebook. Pencil. Second pencil."])
        else:
            wait = S.say("Miss Pellow", ["It was just there. Where you're",
                                         "standing. In seventy-one."])
        pages = [nothing, R.page(wait, img=img, direction_fix=True,
                                 conditions=walk)]
        if key == "lumb":
            pages.append(R.page(_wre3_proof(), img=img, direction_fix=True,
                                conditions=dict(walk, actorValid=True,
                                                actorId=db.WREN)))
        evs.append(R.event(eid, name + " (on the walk)", x, y, pages))
        eid += 1
    for (x, y), d, sheet, index in WRE3_EXTRAS:
        evs.append(R.event(eid, "A Member of the Gloamwood Society", x, y, [
            nothing,
            R.page(S.narrate(["A member of the Gloamwood Society, with",
                              "a lantern and a flask, keeping watch on",
                              "a clearing with nothing in it."]),
                   img=R.image(sheet, index, direction=d),
                   direction_fix=True, conditions=walk)]))
        eid += 1
    return evs


# ================================================================ WRE-1 ==
# The Monograph (`QUESTS.md` C4).
#
# Publication at the Collegium requires a type specimen for every entry, three
# Fellows to review it, and a list of subscribers. Rowbotham named three
# hundred species after himself, his subscribers and his dogs, and never had a
# type specimen for one of them; she will measure all eleven of hers, in eleven
# fights she objects to, and the specimens are what make the work unanswerable.
#
# * **The start is the monographs' shelf**, Map 59 event 5, whose one page
#   already has her reaction shot to the inch-wide gap. Page 2 is hers: the
#   gap, and tucked into it the Library's card of rules. `SW_WRE1_ON`.
# * **The specimens are on the world map**, one each by eleven places, as
#   tracks (`!Other1` 5) that are there only while the monograph is on. With
#   Wren they are a fight (troops 42-52, no escape: a type specimen will not
#   wait) and the specimen is **measured, not killed**; without her they are
#   tracks. Collected is the specimen's own self switch and the count is
#   global, `VAR_WRE1_SPECIMENS`, so a dismissed Wren's count waits.
#   Appended after every other event on Map 8, so no existing id moves.
# * **The reviewers** are two of Rowbotham's three students, who reviewed her
#   first paper at twenty-three: Professor Mott, who has been a beetle for
#   forty years, and Dr Furze, who was at the Slain Wyvern the night they
#   asked Wren to leave. They sit at the Library's reading table from the
#   start. The third is the Honorary Fellow, on its pond (`SW_WRE1_DUCK_DUE`,
#   which ends).
# * **The subscription list** is a shop with names in it, on Prewitt's desk:
#   eight subscriptions, six needed, and the party pays for them, because that
#   is how a list works when you are the one holding it.
# * **The upgrade** is a class change with her experience kept, to
#   `db.CL_WREN_PUBLISHED`: her own class with two more party abilities - no
#   surprise attacks, and more first strikes. Her double drops are untouched.

# (world cell, the place it is by, what she says about it)
WRE1_SPECIMENS = [
    ((52, 74), ["An egg. It has legs. It is not",
                "a breakfast, whatever he says."]),
    ((40, 81), ["A lizard with a frill. He said it",
                "was magnificent. It is a lizard."]),
    ((44, 118), ["It lives in hearths. It is warm,",
                 "and it is not a comfort to anyone."]),
    ((57, 79), ["A gnome that lives in turnips.",
                "He named it after his wife. She knew."]),
    ((105, 76), ["A cat. He named it after his dog.",
                 "I have never forgiven him that."]),
    ((21, 75), ["A hare with stripes. Not a tiger.",
                "It has never once been a tiger."]),
    ((30, 111), ["A fox that walks upright. A",
                 "subscriber paid to have it named."]),
    ((58, 21), ["It grazes, and it has a great many",
                "eyes. It is not, in any sense, an ox."]),
    ((73, 26), ["A sylph that lives in draughts.",
                "Named for a lady who had a cold."]),
    ((56, 98), ["A wader. He called it his",
                "self-portrait. It does look like him."]),
    ((103, 56), ["A kappa, in a lake. He called it",
                 "Captain. Captain was a spaniel."]),
]
TRACKS = ("!Other1", 5)


def specimen_events(base_id):
    """WRE-1's eleven specimens, as world-map events from `base_id` on:
    nothing until the monograph is on, then tracks, and nothing again once
    the specimen is measured."""
    assert len(WRE1_SPECIMENS) == len(db.SPECIMENS) == 11
    evs = []
    for i, ((x, y), remark) in enumerate(WRE1_SPECIMENS):
        name, his = db.SPECIMENS[i][0], db.SPECIMENS[i][7]
        troop = db.TR_SPECIMENS[i]
        measured = [R.battle(troop, can_escape=False, can_lose=False)]
        measured += S.narrate([
            "It is not dead. It has been measured, which it minds a",
            "great deal more. Wren writes for some time, and then",
            "she lets it go."])
        measured += [R.control_variable_add(db.VAR_WRE1_SPECIMENS),
                     R.play_se("Book1"), R.self_switch("A", True)]
        measured += S.got(["Type specimens measured: \\V[%d] of eleven."
                           % db.VAR_WRE1_SPECIMENS])
        wren = S.say("Wren", ["Rowbotham's name for it:"])
        wren += S.narrate([his + "."])
        wren += S.say("Wren", remark)
        wren += S.say("Wren", ["%s. I need it intact." % name])
        wren += R.choice_block(
            ["Measure it", "Leave it"],
            [measured, S.say("Wren", ["It'll be back. They always are."])])
        c = S.narrate(["Tracks, in the soft ground, going somewhere in",
                       "a hurry."])
        c += R.if_then(R.condition_actor_in_party(db.WREN), wren,
                       S.narrate(["Wren would know what made them."]))
        nothing = dict(img=R.image(""), trigger=1, priority=0, through=True)
        evs.append(R.event(base_id + i, "Type Specimen: " + name, x, y, [
            R.page([], **nothing),
            R.page(c, img=R.image(*TRACKS, direction=2), trigger=1,
                   priority=0, through=True, direction_fix=True,
                   conditions={"switch1Valid": True,
                               "switch1Id": db.SW_WRE1_ON}),
            R.page([], conditions={"selfSwitchValid": True,
                                   "selfSwitchCh": "A"}, **nothing),
        ]))
    return evs


def _wre1_complete():
    subs = " + ".join("($gameParty.hasItem($dataItems[%d]) ? 1 : 0)" % i
                      for i in db.IT_SUBSCRIPTIONS)
    return R.condition_script(
        "$gameVariables.value(%d) >= 11 && $gameSwitches.value(%d) && "
        "$gameSwitches.value(%d) && $gameSwitches.value(%d) && (%s) >= %d"
        % (db.VAR_WRE1_SPECIMENS, db.SW_WRE1_MOTT, db.SW_WRE1_FURZE,
           db.SW_WRE1_DUCK, subs, db.SUBSCRIBERS_NEEDED))


def _wre1_rules():
    c = S.narrate([
        "Tucked into it, as if it had been waiting, is one of the",
        "Library's cards."])
    c += S.narrate([
        "A MONOGRAPH OF THE COLLEGIUM REQUIRES: (I) A TYPE",
        "SPECIMEN FOR EVERY ENTRY; (II) THREE FELLOWS TO REVIEW",
        "IT; (III) A LIST OF SUBSCRIBERS."])
    c += S.say("Wren", ["Eleven entries. Eleven type specimens."])
    c += S.say("Wren", ["Rowbotham named three hundred species",
                        "and never had a type specimen for one",
                        "of them. He named them after his dogs."])
    c += S.say("Wren", ["I am going to find all eleven, and",
                        "measure them, and fight every one of",
                        "them, and I am going to hate it."])
    c += [S.trope(), R.control_switch(db.SW_WRE1_ON, True)]
    return c


def _wre1_publish():
    c = S.narrate([
        "Prewitt binds it herself, which she has not done for",
        "anybody in eleven years, and brings it to the shelf."])
    c += S.narrate([
        "THE FAUNA OF THE VALLEY, BY WHAT THEY ARE.",
        "W. HALLOWAY. Eleven type specimens, three reviewers,",
        "and a list of subscribers, bound in at the back."])
    c += [R.play_se("Book2"), R.wait(30)]
    c += S.narrate(["It goes into the gap. It is exactly an inch wide."])
    c += S.say("Wren", ["There was room."])
    c += S.narrate([
        "She says nothing else. She stands with one finger on its",
        "spine for some time, the way you would keep your place",
        "in a book."])
    # Change Class, experience kept (code 321): her own class, plus the
    # monograph. See db.CL_WREN_PUBLISHED.
    c += [{"code": 321, "indent": 0,
           "parameters": [db.WREN, db.CL_WREN_PUBLISHED, True]},
          R.gain_item(db.IT_MONOGRAPH), R.play_me("Fanfare1")]
    c += S.got(["Wren is a \\C[3]Cataloguer (Published)\\C[0]. Nothing the",
                "monograph describes takes the party by surprise,",
                "and the party tends to see it first."])
    c += [R.control_switch(db.SW_WRE1_DONE, True)]
    c += S.companion_story(db.WREN)
    return c


def shelf_pages(page0):
    """The monographs (Map 59, event 5), which have one page with her
    reaction shot in it. Page 2 is that page exactly, for her, and it marks
    the gap seen (self switch B, which is cosmetic - the quest is global);
    page 3 is her second look, which finds the card and starts the
    monograph, and after that counts it and publishes it; then afterwards,
    for everybody, and afterwards with her."""
    status = S.narrate([
        "The inch-wide gap. Type specimens measured: \\V[%d]"
        % db.VAR_WRE1_SPECIMENS, "of eleven."])
    status += S.say("Wren", ["Not yet. Specimens, three reviewers,",
                             "six subscribers. Then there's room."])
    # The shelf's own narration, before its Wren branch.
    first_branch = next(i for i, cmd in enumerate(page0["list"])
                        if cmd["code"] == 111)
    narration = page0["list"][:first_branch]
    first_look = page0["list"][:-1] + [R.self_switch("B", True)]
    second_look = narration + R.if_then(
        R.condition_switch(db.SW_WRE1_ON),
        R.if_then(_wre1_complete(), _wre1_publish(), status),
        S.narrate(["Wren goes back to the gap, as if it might have moved."])
        + _wre1_rules())
    shelf = [
        "And in what was an inch-wide gap: THE FAUNA OF THE VALLEY,",
        "BY WHAT THEY ARE. W. HALLOWAY. It fits exactly."]
    # Afterwards the reaction shot to the gap would be wrong: keep the
    # shelf's own narration, drop the Wren branch, and say what is there.
    after = copy.deepcopy(narration) + S.narrate(shelf) + [page0["list"][-1]]
    with_her = after[:-1] + S.narrate([
        "Wren does not look at it. Then she does."]) + [after[-1]]
    wren = {"actorValid": True, "actorId": db.WREN}
    done = {"switch1Valid": True, "switch1Id": db.SW_WRE1_DONE}
    return [
        _dressed(page0, first_look, wren),
        _dressed(page0, second_look, dict(wren, selfSwitchValid=True,
                                          selfSwitchCh="B")),
        _dressed(page0, after, done),
        _dressed(page0, with_her, dict(done, **wren)),
    ]


def _dressed(page0, commands, conditions):
    """A new page in `page0`'s dress with its own list and conditions;
    `commands` already ends with the terminator or is given one."""
    if not commands or commands[-1]["code"] != 0:
        commands = commands + [{"code": 0, "indent": 0, "parameters": []}]
    page = R.page([], conditions=conditions)
    return dict(copy.deepcopy(page0), list=commands,
                conditions=page["conditions"])


def _review(key, other):
    """The review scene for one student, with Wren: after the specimens,
    once; and the duck named when it is the second review in."""
    me = {"mott": db.SW_WRE1_MOTT, "furze": db.SW_WRE1_FURZE}[key]
    them = {"mott": db.SW_WRE1_MOTT, "furze": db.SW_WRE1_FURZE}[other]
    who = {"mott": "Professor Mott", "furze": "Dr Furze"}[key]
    if key == "mott":
        scene = S.say(who, ["Miss Halloway. I",
                            "reviewed your first, at twenty-three.",
                            "I said it lacked respect."])
        scene += S.say("Wren", ["It did."])
        scene += S.narrate([
            "He reads, for a long time, and stops at the eleventh",
            "type specimen, and takes his spectacles off."])
        scene += S.say(who, ["He never measured",
                             "anything. He named it after whoever",
                             "was at dinner. He named a beetle",
                             "after me."])
        scene += S.say(who, ["I have been a beetle",
                             "for forty years. I should like, before",
                             "I die, to be a person. Accepted."])
    else:
        scene = S.say(who, ["I reviewed your first",
                            "as well. 'Too many footnotes.'"])
        scene += S.say("Wren", ["There were exactly enough footnotes."])
        scene += S.narrate([
            "Dr Furze turns the pages without hurrying, and stops at",
            "page four hundred, the Lesser Wyvern, and reads one word",
            "of it several times."])
        scene += S.say(who, ["You've written",
                             "'goose'."])
        scene += S.say("Wren", ["It is a goose."])
        scene += S.say(who, ["I know. I was in the",
                             "Slain Wyvern the night they asked you",
                             "to leave. I have always known."])
        scene += S.say(who, ["Accepted. With no",
                             "corrections, which I have never",
                             "written before."])
    scene += [R.control_switch(me, True), R.play_se("Book1")]
    scene += R.if_then(R.condition_switch(them), S.say(who, [
        "That's two. The rules",
        "say three Fellows. The third is the",
        "Honorary Fellow. It lives on a pond."]) + [
        R.control_switch(db.SW_WRE1_DUCK_DUE, True)])
    early = S.say(who, ["Specimens first, Miss",
                        "Halloway. All eleven. He never kept",
                        "that rule. You will have to."])
    done = S.say(who, {"mott": ["Accepted. I said so.",
                                "I am a person now."],
                       "furze": ["Accepted. It is still",
                                 "a goose."]}[key])
    return R.if_then(
        R.condition_switch(me), done,
        R.if_then(R.condition_variable(db.VAR_WRE1_SPECIMENS, 11, 1),
                  scene, early))


WRE1_REVIEWERS = [   # (key, speaker, the other one, facing)
    ("mott", "Professor Mott", "furze", 4),
    ("furze", "Dr Furze", "mott", 6),
]


def reviewer_events(base_id, cells):
    """Professor Mott and Dr Furze at the Library's reading table (Map 59),
    `cells` theirs in that order: there from the start of the monograph,
    waiting for the specimens without her, reviewing with her, and pleased
    with themselves afterwards."""
    evs = []
    for i, ((key, who, other, facing), (x, y)) in enumerate(
            zip(WRE1_REVIEWERS, cells)):
        img = R.image(*S.FACES[who], direction=facing)
        on = {"switch1Valid": True, "switch1Id": db.SW_WRE1_ON}
        waiting = S.say(who, {
            "mott": ["Mott. Rowbotham's",
                     "student. Reviewing Miss Halloway.",
                     "Again. When she is ready."],
            "furze": ["Furze. I am waiting",
                      "for eleven type specimens. He never",
                      "had one. Nobody has ever had one."]}[key])
        after = S.say(who, {
            "mott": ["A person. Not a",
                     "beetle. You would be surprised what",
                     "a difference it makes."],
            "furze": ["It is a goose. I",
                      "have it in writing now, and so does",
                      "the Library."]}[key])
        evs.append(R.event(base_id + i, who, x, y, [
            R.page([], img=R.image(""), priority=0, through=True),
            R.page(waiting, img=img, conditions=on),
            R.page(_review(key, other), img=img,
                   conditions=dict(on, actorValid=True, actorId=db.WREN)),
            R.page(after, img=img, conditions={
                "switch1Valid": True, "switch1Id": db.SW_WRE1_DONE}),
        ]))
    return evs


def subscription_event(event_id, x, y):
    """The subscription list (Map 59), on Prewitt's desk: a shop with names
    in it while the monograph is on; bound in at the back afterwards."""
    c = S.narrate([
        "Wren's subscription list, on the Library desk, with the",
        "Library's pen. SUBSCRIBERS, it says, and a long space."])
    c += S.narrate([
        "A subscription is a bound copy, paid for. Nobody in the",
        "valley has ever been asked to subscribe, so you will be",
        "doing the paying."])
    c += R.shop([(0, iid, 0, 0) for iid in db.IT_SUBSCRIPTIONS],
                purchase_only=True)
    nothing = dict(img=R.image(""), trigger=0, priority=0, through=True)
    return R.event(event_id, "The Subscription List", x, y, [
        R.page([], **nothing),
        R.page(c, img=R.image(""), trigger=0, priority=1, direction_fix=True,
               conditions={"switch1Valid": True, "switch1Id": db.SW_WRE1_ON}),
        R.page(S.narrate(["The subscription list is closed, and bound in at",
                          "the back of the monograph."]),
               img=R.image(""), trigger=0, priority=1, direction_fix=True,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_WRE1_DONE}),
    ])


def pond_page():
    """The Duck's Pond (Map 8), after its own pages and ZEPH-2's: with Wren,
    once two reviews are in, the third. The duck reviews by walking on to the
    manuscript and sitting on it."""
    review = R.if_then(
        R.condition_switch(db.SW_ZEPH2_WALKING),
        S.narrate(["The duck's pond, without the duck: GONE TO",
                   "CONGREGATION."])
        + S.say("Wren", ["We'll come back when it's home."]),
        S.narrate([
            "Wren lays the manuscript on the bank. The duck walks",
            "into it, then on to it, reads - apparently - page four",
            "hundred, and sits down on it."])
        + S.say("Wren", ["That is acceptance."])
        + S.narrate(["It is. It is the warmest review she has ever had."])
        + [R.play_se("Chicken", 70, 90),
           R.control_switch(db.SW_WRE1_DUCK, True),
           R.control_switch(db.SW_WRE1_DUCK_DUE, False)])
    stop = S.narrate(["A small pond, four miles from the Collegium, with",
                      "a reviewer on it."])
    return R.page(stop + R.choice_block(
        ["Stop a while", "Press on"],
        [review, S.narrate(["You press on."])]),
        img=R.image(""), trigger=1, priority=0, through=True,
        conditions={"selfSwitchValid": True, "selfSwitchCh": "A",
                    "switch1Valid": True, "switch1Id": db.SW_WRE1_DUCK_DUE,
                    "actorValid": True, "actorId": db.WREN})


# ================================================================ WRE-4 ==
# The Cabinet (`QUESTS.md` E9). A manor holds eighty impossible animals in
# glass cases, and she is engaged to authenticate them. All eighty are two
# animals sewn together; the taxidermist is ninety and unrepentant and an
# artist, and the joins are magnificent. She writes it up honestly, which
# means saying the workmanship is the finest she has seen, which she means.
#
# * **The manor is Fenmarch**, Map 57 (`COMPANIONS.md` says reuse it), and
#   the Marsh Bear's case already has her "Not unless I'm asked." **Mrs
#   Puddifoot asks** - her second look with Wren, below her one-self-switch
#   ladder - because she dusts all eighty and the family has always wanted
#   them looked at properly. The Fourth is the family, and speaks in the
#   scene from where he stands, but he is not the owner: ALD-5's afterwards
#   page is on him.
# * **Mr Ottershaw shows her the joins** (his second look, with Wren and the
#   engagement): nobody in seventy years has asked. He walks her down the
#   gallery case by case, and past case forty, the Home Farm's unicorn,
#   without looking at it. She looks. There is no join. She writes nothing.
# * **The write-up** goes back to Mrs Puddifoot, read out: seventy-nine
#   composed, the finest joins she has seen, and case forty "not examined" -
#   the composite that is real, which she does not mention. The Fourth is
#   prouder than ever: nobody else in the county has a composer. The fee is
#   `db.WRE4_FEE`.
# * **Afterwards for everybody**: Mrs Puddifoot and the framed write-up; Mr
#   Ottershaw, who has been asked.
def _wre4_engage():
    c = S.narrate([
        "Mrs Puddifoot looks at Wren's jars, and her notebook, and",
        "the way she has been looking at the cases."])
    c += S.say("Mrs Puddifoot", ["You're a naturalist.",
                                 "A proper one. With the jars."])
    c += S.say("Mrs Puddifoot", ["The family's always",
                                 "wanted them looked at. Properly.",
                                 "By somebody who knows."])
    c += S.narrate([
        "The Fourth is across the gallery before she has finished,",
        "helmet under his arm."])
    c += S.say("The Fourth", ["A NATURALIST? Would you?",
                              "Three generations we've been proud",
                              "of them. Dr Rowbotham named the",
                              "bear!"])
    c += S.say("Wren", ["He named everything. That was",
                        "the problem."])
    c += S.say("Wren", ["I'll tell you what they are. All",
                        "eighty. You may not like it."])
    c += S.say("The Fourth", ["We'll love it. We love",
                              "everything. Ask anybody."])
    c += S.say("Mrs Puddifoot", ["There's a fee. The",
                                 "rest are upstairs, one in every",
                                 "bedroom. Mind the moat."])
    c += [R.control_switch(db.SW_WRE4_ON, True)]
    c += S.narrate([
        "Wren opens her notebook, and this time she does not",
        "close it again."])
    return c


def _wre4_waiting():
    return S.say("Mrs Puddifoot", ["Mr Ottershaw's at the",
                                   "far end. He'll want to show you.",
                                   "He's never been asked."])


def _wre4_writeup():
    c = S.narrate([
        "Wren has been through the gallery and every bedroom, and",
        "under one bed. She reads it out to the household, standing,",
        "the way you would read a will."])
    c += S.narrate([
        "THE FENMARCH COLLECTION. EIGHTY CASES.",
        "Seventy-nine composed, each of two animals, by Mr J.",
        "Ottershaw, 1930 to the present. None is what its plate",
        "says. Not one of them ever lived."])
    c += S.narrate([
        "The joins are the finest work I have seen. I have looked",
        "for joins all my life. I could not find these without",
        "being shown, and then I could not stop looking at them.",
        "Case forty: not examined. W. Halloway."])
    c += S.say("The Fourth", ["...None of them?"])
    c += S.say("Wren", ["None of them. I'm sorry."])
    c += [R.wait(30)]
    c += S.say("The Fourth", ["COMPOSED. By Mr",
                              "Ottershaw. Nobody else in the",
                              "county has a COMPOSER."])
    c += S.say("The Fourth", ["That's better than",
                              "real. Anybody can have real."])
    c += S.narrate([
        "He means it, magnificently. Mrs Puddifoot counts out the",
        "fee from a tin on the mantelpiece, and has the write-up",
        "framed before Wren has her coat on."])
    c += [R.gain_gold(db.WRE4_FEE)]
    c += R.text(["Got \\C[3]%d\\G\\C[0]." % db.WRE4_FEE])
    c += S.say("Wren", ["Nobody has ever been pleased",
                        "with a write-up of mine."])
    c += S.say("Wren", ["...I'm not sure what to do with",
                        "my face."])
    c += [S.trope(), R.control_switch(db.SW_WRE4_DONE, True)]
    c += S.companion_story(db.WREN)
    return c


def puddifoot_pages(last):
    """Pages 3-4 for Mrs Puddifoot (Fenmarch's gallery, event 3), in her own
    last page's dress: with Wren, below her ladder, the engagement, the wait
    and the write-up; afterwards, her last page and the frame."""
    known = {"selfSwitchValid": True, "selfSwitchCh": "A"}
    own = last["list"][:-1]
    ask = own + R.if_then(
        R.condition_switch(db.SW_WRE4_JOINS), _wre4_writeup(),
        R.if_then(R.condition_switch(db.SW_WRE4_ON), _wre4_waiting(),
                  _wre4_engage()))
    after = own + S.narrate([
        "Over the fire, framed: SEVENTY-NINE COMPOSED. THE FINEST",
        "WORK I HAVE SEEN. She dusts it first, before the cases."])
    return [
        _dressed(last, ask, dict(known, actorValid=True, actorId=db.WREN)),
        _dressed(last, after, dict(known, switch1Valid=True,
                                   switch1Id=db.SW_WRE4_DONE)),
    ]


def _wre4_joins():
    c = S.say("Wren", ["Mr Ottershaw. I've been engaged",
                       "to authenticate them."])
    c += S.narrate([
        "He puts down the needle. He takes off the green lenses, and",
        "puts them on again, to see her better."])
    c += S.say("Mr Ottershaw", ["Seventy years. Nobody",
                                "has ever ASKED."])
    c += S.narrate([
        "He takes her down the gallery at a pace you would not",
        "expect of a man of ninety, one case at a time."])
    c += S.say("Mr Ottershaw", ["The Marsh Bear. Bear",
                                "to the waist, crab below. The crab",
                                "end came for the crayfish."])
    c += S.say("Mr Ottershaw", ["The Phoenix. A",
                                "salamander, and the top of something",
                                "that fell in Cook's fire."])
    c += S.say("Mr Ottershaw", ["The Horse. Crab and",
                                "unicorn. The plate's blank because",
                                "nobody liked to ask what it was."])
    c += S.narrate([
        "At every case he shows her the join, and she finds it",
        "only once he has put his finger on it. She writes each",
        "one down. Her hand is not quite steady."])
    c += S.narrate([
        "He goes past case forty, the Home Farm's unicorn, without",
        "looking at it, the way you go past a door you don't open."])
    c += S.narrate([
        "Wren stops. She looks at the shoulder, and the horn, and",
        "the shoulder again, for a long time. There is no join."])
    c += S.narrate([
        "She looks at Mr Ottershaw. He is threading a needle. She",
        "closes her notebook, and writes nothing, and walks on."])
    c += S.say("Wren", ["They're magnificent."])
    c += S.say("Mr Ottershaw", ["I know. Put it in",
                                "writing. Nobody ever has."])
    c += [R.control_switch(db.SW_WRE4_JOINS, True)]
    return c


def ottershaw_pages(last):
    """Pages 3-4 for Mr Ottershaw (Fenmarch's gallery, event 4), in his own
    last page's dress: with Wren and the engagement, the joins, below his
    ladder; afterwards, his last page and the write-up over his bench."""
    known = {"selfSwitchValid": True, "selfSwitchCh": "A"}
    own = last["list"][:-1]
    shown = S.say("Mr Ottershaw", ["Every join. Go and",
                                   "write it down, Miss Halloway."])
    joins = own + R.if_then(R.condition_switch(db.SW_WRE4_JOINS), shown,
                            _wre4_joins())
    after = own + S.narrate([
        "Pinned over his bench, a copy of the write-up. He has",
        "underlined 'finest' twice, and hums louder."])
    return [
        _dressed(last, joins, dict(known, actorValid=True, actorId=db.WREN,
                                   switch1Valid=True,
                                   switch1Id=db.SW_WRE4_ON)),
        _dressed(last, after, dict(known, switch1Valid=True,
                                   switch1Id=db.SW_WRE4_DONE)),
    ]
