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
