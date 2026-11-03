"""Hob Grumnir's companion quests - `COMPANIONS.md`, his section, and
`QUESTS.md` for the order they are built in.

Nothing here draws a map, and this module imports no place module: the place
modules call in here for pages.

HOB-5, Two Smiths, One Forge (`QUESTS.md` A6)
---------------------------------------------
They went for a drink (`SW_HOB_BRYD`). This is what comes of it and no more:
a job up from the works that neither of them can do alone, done in one heat,
without either of them finishing a sentence in the same room - and Ott's
approval carried back down the hill, and nothing whatsoever said out loud.

HOB-3, The Anvil (`QUESTS.md` A8) is below it: the smithy's anvil as an
event, Beatrice while it is gone, and the three events outside the door. Then
HOB-2 (A13), the grave, and HOB-1 (B1), the Assize of Hammers, at the bottom.

* **The ask is Bryd's**, on Map 24 - three pages appended below his ladder.
  His terminal switch is `SW_SPAR_DONE`, and `SW_HOB_BRYD` is only ever set
  beside it, so requiring the drink requires the terminal. The job also
  requires `SW_OTT_MATERIALS`: it is the Two Hundred's refit, so she has to
  have flown, and a plate carried up the hill to a woman still half-way
  through her own flying chain would be heard by the chain and not by her.
* **Only the forging needs Hob.** The plate is an item and the state is two
  global switches, so a Hob dismissed with the plate in the bag leaves the
  errand where it was; anybody can carry it up.
* **Ott's approval is a page on Ott**, Map 22 event 2, below every page she
  has, on `SW_OTT_MATERIALS` and the plate. It shadows her field pages only
  while the plate is carried, and spends the plate.
* **A child says they do this every time.** He has said it since the town
  was built, from behind you, and been removed. Here he is holding the
  candle, and he is not removed.
* **Nothing is said out loud**, and that includes by the narrator.
"""
import copy

import db
import rmmzdata as R
import story as S

PLATE_ICON = 196


def _forging():
    """Hob and Bryd and a tube plate, in one heat. Nobody finishes a
    sentence; Grommet finishes the job."""
    c = S.narrate([
        "There is a drawing on the spike that came down the",
        "hill this morning. It is not a spar."])
    c += S.say("Bryd", ["Miss Hoyle. For the refit."])
    c += S.say("Hob", ["That's a tube plate. That wants -"])
    c += S.say("Bryd", ["Aye."])
    c += S.narrate([
        "It wants, you gather, four hands, one heat, and",
        "somebody small enough to go inside it afterwards."])
    c += S.narrate(["Everybody in the forge looks at Grommet."])
    c += S.say("Grommet", ["I knew it."])
    c += S.say("Bryd", ["If you take the -"])
    c += S.say("Hob", ["I've got the -"])
    c += S.narrate([
        "Hob takes his coat off. That is not a sentence",
        "either, but it is the nearest either of them comes."])
    c += [R.play_se("Fire1", pitch=80), R.wait(20),
          R.play_se("Hammer", pitch=90), R.wait(12),
          R.play_se("Hammer", pitch=110), R.wait(12),
          R.play_se("Hammer", pitch=90), R.wait(20)]
    c += S.narrate([
        "It is done in one heat, because it can only be done",
        "in one. The plate goes onto the former white and",
        "comes off it the colour of a plum, and in the whole",
        "of it their four hands are never once in the way."])
    c += S.narrate([
        "Then Grommet goes in, feet first, with a candle and",
        "a drift, and sights the holes from the inside."])
    c += S.say("Grommet", ["They're true. All of them.",
                           "Can I come out."])
    c += S.say("Bryd", ["When it's -"])
    c += S.say("Hob", ["Let the lad out."])
    c += S.narrate([
        "He comes out black to the eyebrows, looks at the",
        "two of them, and says it to you, not to them."])
    c += S.say("Grommet", ["They do this every time."])
    c += S.narrate(["For once, nobody removes him."])
    c += S.say("Bryd", ["Take it up the hill."])
    c += [R.gain_item(db.IT_TUBE_PLATE, 1), R.play_me("Item"),
          R.control_switch(db.SW_HOB5_FORGED, True)]
    c += S.got(["Got \\I[%d]\\C[3]A Boiler Tube Plate\\C[0]." % PLATE_ICON])
    return c


def _waiting():
    """The plate is made and has not gone up the hill yet."""
    c = S.say("Bryd", ["It wants to go up the hill.",
                       "It'll not get there by being looked at."])
    c += R.if_then(R.condition_actor_in_party(db.HOB), S.narrate([
        "Hob is looking at it anyway. So is Bryd."]))
    return c


def _told():
    """Ott's word, carried back down. What is said out loud: nothing."""
    told = S.narrate([
        "You tell them what Miss Hoyle said: that it will do,",
        "and that they would know what she meant by it."])
    told += [R.wait(30)]
    told += S.narrate([
        "Bryd looks at Hob. Hob looks at the anvil."])
    told += [R.wait(40)]
    told += S.narrate([
        "Nobody says anything. It is, plainly, the",
        "best afternoon either of them has had in twenty",
        "years, and neither of them is going to give the",
        "other the satisfaction of saying so."])
    told += [R.self_switch("D", True)]
    hob_again = S.say("Bryd", ["Aye."])
    hob_again += S.say("Hob", ["Aye."])
    alone = S.say("Bryd", ["She said that?"])
    alone += S.say("Bryd", ["...Aye. She would."])
    return R.if_then(
        R.condition_actor_in_party(db.HOB),
        R.if_then(R.condition_self_switch("D", False), told, hob_again),
        alone)


def bryd_pages(img):
    """Three pages for Bryd (Map 24, event 2), below his ladder. `img` is the
    image his own pages wear, so he looks the same whoever is asking."""
    drink = {"switch1Valid": True, "switch1Id": db.SW_HOB_BRYD}
    return [
        R.page(_forging(), img=img, trigger=0, priority=1,
               conditions=dict(drink, switch2Valid=True,
                               switch2Id=db.SW_OTT_MATERIALS,
                               actorValid=True, actorId=db.HOB)),
        R.page(_waiting(), img=img, trigger=0, priority=1,
               conditions=dict(drink, switch2Valid=True,
                               switch2Id=db.SW_HOB5_FORGED)),
        R.page(_told(), img=img, trigger=0, priority=1,
               conditions=dict(drink, switch2Valid=True,
                               switch2Id=db.SW_HOB5_DONE)),
    ]


def grommet_pages(img):
    """One page for Grommet (Map 24, event 4), after the boiler. He was told
    he has the makings, slowly; now he is told again, and it is quicker.
    It needs his own self switch A, the end of his ladder."""
    c = S.say("Grommet", ["I've been inside a tube plate.",
                          "Mr Ollerenshaw says I did it right."])
    c += S.say("Grommet", ["He said it quick, an' all."])
    return [R.page(c, img=img, trigger=0, priority=1,
                   conditions={"switch1Valid": True,
                               "switch1Id": db.SW_HOB5_FORGED,
                               "selfSwitchValid": True,
                               "selfSwitchCh": "A"})]


def ott_pages(img):
    """Ott's approval (Map 22, event 2), below every page she has. Her pages
    all require self switch D and everything appended to her requires
    `SW_OTT_MATERIALS`, the switch that means she has nothing left owing
    (this game's `CLAUDE.md`); this does both, and the plate."""
    c = S.narrate([
        "You put the plate down on the drawing office table."])
    c += S.say("Ott", ["Ollerenshaw's."])
    c += S.narrate([
        "She holds it up to the window and sights down every",
        "hole in it, one at a time, and does not hurry."])
    c += S.say("Ott", ["One heat. Four hands."])
    c += S.say("Ott", ["And somebody went in to true",
                       "the holes. Who went in?"])
    c += S.narrate(["You say Grommet went in."])
    c += S.say("Ott", ["Good lad."])
    c += S.narrate([
        "She tries each hole with a gauge pin, all",
        "forty-one of them, and nods at every one."])
    c += S.say("Ott", ["True. Every one."])
    c += S.say("Ott", ["That will do."])
    c += S.narrate([
        "In the Hoyle Works, you are given to understand,",
        "'that will do' is framed."])
    c += S.say("Ott", ["Tell them."])
    c += S.narrate(["You ask what you are to tell them."])
    c += S.say("Ott", ["That it will do.",
                       "They will know what I mean by it."])
    c += [R.gain_item(db.IT_TUBE_PLATE, -1),
          R.control_switch(db.SW_HOB5_DONE, True), R.play_me("Fanfare1")]
    c += S.companion_story(db.HOB)
    return [R.page(c, img=img, trigger=0, priority=1,
                   conditions={"selfSwitchValid": True, "selfSwitchCh": "D",
                               "switch1Valid": True,
                               "switch1Id": db.SW_OTT_MATERIALS,
                               "itemValid": True,
                               "itemId": db.IT_TUBE_PLATE})]


# ======================================================================
# HOB-3, The Anvil (`QUESTS.md` A8)
# ----------------------------------------------------------------------
# The anvil has been stolen. It weighs three hundredweight. Hob is
# incandescent for nine seconds and then thoughtful, because they cannot have
# got far. They did not: they are eleven feet outside the door, under it, and
# are two of Meredith Crooke's apprentices, week four. Rescue your own
# burglars; Crooke collects them and marks the module a fail.
#
# * **The anvil is an event now** (Map 6, `village.SMITHY_ANVIL`), not a
#   tile, so it can be gone: page 1 is the anvil, page 2 the theft - an
#   autorun, the first time Hob walks in after the village has been left -
#   page 3 nothing, and page 4 the anvil back. Beatrice's event stays on the
#   same cell, invisible as it always was, and blocks it.
# * **`SW_HOB3_GONE` goes off again when it comes back**, so "gone" is one
#   switch: Beatrice's page for it and the three events outside all read it
#   and nothing else, and `SW_HOB3_DONE` is what stays.
# * **Outside** (Map 1, `village.ANVIL_OUTSIDE`) the anvil lies on the grass
#   with Ivy and Hodge flat on either side of it - the generator's
#   knocked-down strip. Lifting it needs Hob; without him they wait.
# * **Crooke's line branches on her bounty**: she runs the course either way
#   (`wilds.crooke_bounty`), and she remembers a party that beat her.
FAR = "eleven feet"


def anvil_event(event_id, x, y, tile):
    """The smithy's anvil (Map 6), as an event so it can be stolen."""
    theft = S.narrate(["The anvil is gone."])
    theft += S.narrate([
        "Where it stood there is a square of clean floor,",
        "and Beatrice, lying beside it, on her side."])
    theft += [R.wait(20)]
    theft += S.narrate([
        "Hob Grumnir is incandescent for nine seconds.",
        "It is very loud and entirely technical, and a",
        "good deal of it is about the horn."])
    theft += S.narrate(["Then he stops, and is thoughtful."])
    theft += S.say("Hob", ["Three hundredweight, that."])
    theft += S.say("Hob", ["They'll not have got far."])
    theft += [S.trope(), R.control_switch(db.SW_HOB3_GONE, True)]
    anvil = R.image("", 0, tile_id=tile)
    none = R.image("")
    kw = dict(priority=0, direction_fix=True, through=True)
    return R.event(event_id, "The Anvil", x, y, [
        R.page([], img=anvil, trigger=0, **kw),
        R.page(theft, img=none, trigger=3,
               conditions={"actorValid": True, "actorId": db.HOB,
                           "switch1Valid": True,
                           "switch1Id": db.SW_LEFT_VILLAGE}, **kw),
        R.page([], img=none, trigger=0,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_HOB3_GONE}, **kw),
        R.page([], img=anvil, trigger=0,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_HOB3_DONE}, **kw),
    ])


def beatrice_pages(page0):
    """Beatrice (Map 6, event 4) while the anvil is out on the grass. It
    shadows her ROL-4 pages only for as long as that lasts, which is right:
    Roland lays the sword across the anvil."""
    shaped = R.page(S.narrate([
        "A hammer, lying on the floor where the anvil was.",
        "Somebody has scratched BEATRICE into the haft.",
        "She is not saying anything. Pointedly."]),
        conditions={"switch1Valid": True, "switch1Id": db.SW_HOB3_GONE})
    page = dict(page0, list=shaped["list"], conditions=shaped["conditions"])
    return [page]


def _crooke():
    c = S.narrate(["Somebody is coming down the lane with a clipboard."])
    c += R.if_then(
        R.condition_switch(db.SW_BOUNTY_CROOKE),
        S.say("Crooke", ["You. The footwork."]) +
        S.say("Crooke", ["I'll have my apprentices back,",
                         "if you've finished with them."]),
        S.say("Crooke", ["Meredith Crooke. Principal.",
                         "I believe you have two of mine."]))
    c += S.say("Crooke", ["Week four. Module seven.",
                          "Acquisition of a heavy object."])
    c += S.narrate([
        "She looks at the anvil, and at the door, and at the",
        "%s between them, and writes something down." % FAR])
    c += S.say("Crooke", ["Fail. Both of you."])
    c += S.say("Hodge", ["It's three hundredweight!"])
    c += S.say("Crooke", ["It says so on the side.",
                          "Reading was week one."])
    return c


def _rescue():
    c = S.narrate([
        "The anvil is face down on the grass %s from" % FAR,
        "the smithy door. Under it, as far as can be told",
        "from a head at either end, are two people."])
    c += S.say("Ivy", ["Hello. Sorry. Hello."])
    c += S.say("Hodge", ["Don't say sorry. We don't say",
                         "sorry. It's in the syllabus."])
    c += S.say("Ivy", ["We've been here since before it",
                       "got light. We're ever so sorry."])
    c += S.narrate([
        "Hob Grumnir looks at the anvil, and at the heads,",
        "and at the door, and does the arithmetic."])
    c += S.say("Hob", ["Three hundredweight. Two of you.",
                       "Eleven foot, in the dark."])
    c += S.say("Hob", ["That's not bad, that."])
    c += S.say("Hodge", ["Is it?"])
    c += S.say("Hob", ["No."])
    c += S.narrate([
        "He gets his hands under the horn and lifts it off",
        "them as if it were a loaf. They lie there a moment,",
        "flatter than they were, looking at the sky."])
    c += [R.play_se("Equip1", pitch=70), R.wait(20)]
    c += _crooke()
    c += S.say("Ivy", ["Please, miss. Might I write",
                       "to him first?"])
    c += S.narrate([
        "Ivy Scrope writes an apology on the back of her",
        "syllabus, in a very good hand, and gives it to Hob.",
        "He reads it twice."])
    c += [R.gain_item(db.IT_APOLOGY, 1), R.play_me("Item")]
    c += S.got(["Got \\I[%d]\\C[3]A Written Apology\\C[0]." % APOLOGY_ICON])
    c += S.say("Hob", ["...Nice hand, that."])
    c += S.say("Crooke", ["Week one. It's all week one."])
    c += S.narrate([
        "Crooke takes them off up the lane, one ear each.",
        "Hob carries the anvil back in under one arm and",
        "sets it down where it was, to the inch, with",
        "Beatrice on top of it."])
    c += [R.control_switch(db.SW_HOB3_GONE, False),
          R.control_switch(db.SW_HOB3_DONE, True)]
    c += S.companion_story(db.HOB)
    return c


def _burglars_waiting():
    c = S.narrate([
        "The smithy's anvil, face down on the grass %s" % FAR,
        "from the door. There is a head at either end."])
    c += S.say("Ivy", ["Is he coming? The smith?",
                       "Only we can't lift it."])
    c += S.say("Hodge", ["We lifted it once."])
    return c


APOLOGY_ICON = 193


def outside_events(base_id, anvil_at, tile):
    """The anvil and its two burglars, on the grass outside the smithy
    (Map 1). Each has one page, on `SW_HOB3_GONE`, so before and after they
    are not there at all."""
    x, y = anvil_at
    gone = {"switch1Valid": True, "switch1Id": db.SW_HOB3_GONE}
    anvil = R.page(
        R.if_then(R.condition_actor_in_party(db.HOB), _rescue(), _burglars_waiting()),
        img=R.image("", 0, tile_id=tile), trigger=0, priority=1,
        direction_fix=True, conditions=gone)

    def flat(event_id, name, dx, speaker, lines):
        sheet, index = S.FACES[speaker]
        return R.event(event_id, name, x + dx, y, [R.page(
            S.say(speaker, lines),
            img=R.image(sheet + "_Damage", index, direction=2, pattern=2),
            trigger=0, priority=1, direction_fix=True, walk_anime=False,
            conditions=gone)])

    return [
        R.event(base_id, "The Anvil (Outside)", x, y, [anvil]),
        flat(base_id + 1, "Ivy Scrope", -1, "Ivy",
             ["Sorry. We're under the anvil.",
              "Well - near it. Mostly under it."]),
        flat(base_id + 2, "Hodge Arkwright", 1, "Hodge",
             ["We're not stuck. We're resting.",
              "Between modules."]),
    ]


# ======================================================================
# HOB-2, The Grave He Has Not Made (`QUESTS.md` A13)
# ----------------------------------------------------------------------
# Beatrice goes quiet. Not broken - quiet. Hob is bereft and unbearable, and
# admits in the end what she told him to do eleven years ago: make her a
# marker. He has never started it. The quest is four attempts: three
# magnificent things he carries down to the churchyard and will not put up,
# and a gate with a good latch, because the gate sticks and she would have
# hated the fuss. She starts talking again on the walk home, about the latch.
#
# * **Nobody in it says she is the hammer**, including the narrator. The
#   headstone has her name on it, and that is all.
# * **The churchyard is new tiles in an empty corner of Map 1**, east of the
#   chapel, drawn by `village.py` - `QUESTS.md` A13 has the argument. It is
#   there for everybody, from the start; only the gate changes.
# * **The attempts are made at the forge** (Map 6, a new event on it) and
#   carried to her grave (Map 1). `SW_HOB2_CARRYING` is one attempt on its
#   way, `VAR_HOB2_TRY` which; the fourth is hung, not put up. Every piece of
#   it is a global, so a Hob sent home leaves it where it was.
# * **His weapon is the three he would not put up**, melted, and made badly
#   on purpose so that she would have something to say. It is his best.
HOB2_ICON = 99


def _hob2_quiet():
    c = S.narrate([
        "Hob stops in the doorway of his own smithy, with his",
        "hand on Beatrice at his belt, and listens."])
    c += S.say("Hob", ["...Beatrice?"])
    c += [R.wait(40)]
    c += S.narrate(["Nothing."])
    c += S.say("Hob", ["She's not sulking. Hammers don't sulk."])
    c += S.narrate([
        "He says this four times in the next hour - to the",
        "anvil, to the forge, to the quench and to you - and",
        "is unbearable in between. Nobody has ever seen Hob",
        "Grumnir at a loss, and he turns out to be very large",
        "at it."])
    c += S.say("Hob", ["Eleven years back, she told me to",
                       "make her a marker. For the churchyard."])
    c += S.say("Hob", ["Make it right, she said, and don't",
                       "make a fuss. I've not started it.",
                       "I can't get it right in my head."])
    c += S.narrate(["He looks at the forge for a long time."])
    c += S.say("Hob", ["She'll not say anything till I do.",
                       "That'll be it."])
    c += [S.trope(), R.control_switch(db.SW_HOB2_ON, True)]
    return c


_HOB2_MADE = {
    1: ["Hob makes a headstone of wrought iron, with roses on",
        "it that open as you watch, and her name in letters",
        "you could hang a door on. It takes him all night. It",
        "is magnificent."],
    2: ["A cross of forged steel, eight feet high, with a",
        "flame worked into the heart of it that is somehow",
        "made of iron. It is the best thing you have ever",
        "seen made by hand, until the next one."],
    3: ["Something small this time: a plate, her name, and a",
        "B and a G run together by the hilt of a little",
        "sword. It is perfect. He looks at it as if it had",
        "said something rude."],
    4: ["A gate. A plain churchyard gate in good iron, true",
        "on its hangings, with a latch that drops shut under",
        "its own weight and stays shut."],
}


def _hob2_forge():
    made = []
    for n in (1, 2, 3, 4):
        body = S.narrate(_HOB2_MADE[n])
        if n == 4:
            body += S.say("Hob", ["She'd have hated the fuss."])
        made += R.if_then(R.condition_variable(db.VAR_HOB2_TRY, n), body)
    make = [R.control_variable_add(db.VAR_HOB2_TRY, 1),
            R.play_se("Fire1", pitch=80), R.wait(20),
            R.play_se("Hammer", pitch=90), R.wait(12),
            R.play_se("Hammer", pitch=100), R.wait(20)]
    make += made + [R.control_switch(db.SW_HOB2_CARRYING, True)]
    make += S.say("Hob", ["Right. Down to her with it."])
    wait = S.say("Hob", ["Down to her with it first.",
                         "Then we'll see."])
    return R.if_then(R.condition_switch(db.SW_HOB2_CARRYING), wait, make)


def forge_event(event_id, x, y):
    """The forge on the smithy's back wall (Map 6): the quiet, as an autorun
    the first time Hob walks in after the anvil is back, and then the four
    attempts, one at a time."""
    blank = R.image("")
    kw = dict(direction_fix=True)
    return R.event(event_id, "The Forge", x, y, [
        R.page(S.narrate(["The forge, banked down. It is never quite out."]),
               img=blank, **kw),
        R.page(_hob2_quiet(), img=blank, trigger=3,
               conditions={"actorValid": True, "actorId": db.HOB,
                           "switch1Valid": True,
                           "switch1Id": db.SW_HOB3_DONE}, **kw),
        R.page(_hob2_forge(), img=blank,
               conditions={"actorValid": True, "actorId": db.HOB,
                           "switch1Valid": True,
                           "switch1Id": db.SW_HOB2_ON}, **kw),
        R.page(S.narrate([
            "The forge. Chalked on the wall beside it, a drawing",
            "of a latch, and under it, in another hand entirely,",
            "'TOO HEAVY'."]), img=blank,
            conditions={"switch1Valid": True,
                        "switch1Id": db.SW_HOB2_DONE}, **kw),
    ])


def _hob2_grave():
    no = {
        1: S.narrate(["Hob sets the iron headstone up beside the parish",
                      "one. The roses catch the light."]) +
        S.say("Hob", ["No."]) +
        S.narrate(["He does not say why. He takes it back up the lane",
                   "under one arm."]),
        2: S.narrate(["He stands the cross up. It is eight feet high. It",
                      "can be seen from the road."]) +
        S.say("Hob", ["She'd say it was showing off."]) +
        S.narrate(["It is, a bit. It goes back up the lane."]),
        3: S.narrate(["He props the little plate against the headstone.",
                      "It is exactly right, and small, and he looks at",
                      "it for a long time."]) +
        S.say("Hob", ["It's right. It's not her."]) +
        S.narrate(["On the way out the gate sticks, as it always has,",
                   "and you all have to lift it to make it move. Hob",
                   "stops with his hand on it."]) +
        S.say("Hob", ["...Hang on."]),
    }
    c = []
    for n in (1, 2, 3):
        c += R.if_then(R.condition_variable(db.VAR_HOB2_TRY, n),
                       no[n] + [R.control_switch(db.SW_HOB2_CARRYING, False)])
    c += R.if_then(R.condition_variable(db.VAR_HOB2_TRY, 4), S.say("Hob", [
        "Not this one. This one's for the gate."]))
    return c


def grave_event(event_id, x, y, tile):
    """Beatrice Grumnir's grave (Map 1), the parish's plain headstone, for
    everybody; with Hob and an attempt in hand, where each one is refused."""
    stone = S.narrate([
        "A plain headstone, the parish's own:",
        "  BEATRICE GRUMNIR. SMITH. 1919 - 1989.",
        "The grass round it has been cut. Somebody cuts it",
        "every week, and nobody says who."])
    img = R.image("", 0, tile_id=tile)
    kw = dict(direction_fix=True)
    return R.event(event_id, "Beatrice Grumnir's Grave", x, y, [
        R.page(stone, img=img, **kw),
        R.page(_hob2_grave(), img=img,
               conditions={"actorValid": True, "actorId": db.HOB,
                           "switch1Valid": True,
                           "switch1Id": db.SW_HOB2_CARRYING}, **kw),
    ])


def _hob2_hung():
    c = S.narrate([
        "Hob lifts the old gate off what is left of its",
        "hinge and hangs the new one. It takes him ten",
        "minutes, and he does not hurry one of them."])
    c += [R.play_se("Hammer", pitch=100), R.wait(15),
          R.play_se("Hammer", pitch=110), R.wait(30),
          R.play_se("Open1", pitch=80), R.wait(20),
          R.play_se("Switch1", pitch=70), R.wait(30)]
    c += S.narrate(["It swings shut under its own weight.",
                    "The latch drops. Click."])
    c += S.say("Hob", ["There."])
    c += [R.wait(40)]
    c += S.narrate([
        "Nobody says anything. Half-way up the lane Hob stops,",
        "and puts his hand to his belt, and listens."])
    c += S.say("Hob", ["...She says the latch wants a spring."])
    c += S.say("Hob", ["She says it's hung a quarter-inch proud",
                       "on the low side, and the sneck's too",
                       "heavy, and who was it taught me to use",
                       "a sneck that heavy."])
    c += S.say("Hob", ["She's right."])
    c += S.narrate([
        "He walks the rest of the way home a good deal faster",
        "than he came, talking the whole way, and so, you",
        "gather, does she."])
    c += S.say("Hob", ["Them three I made for her. I'll melt",
                       "them for a hammer. Make it badly, a",
                       "bit. Give her something to say."])
    c += [R.play_se("Fire1", pitch=80), R.wait(20),
          R.gain_weapon(db.WP_SOMETHING_TO_SAY, 1), R.play_me("Item")]
    c += S.got(["Got \\I[%d]\\C[3]Something To Say\\C[0]." % HOB2_ICON])
    c += [R.control_switch(db.SW_HOB2_CARRYING, False),
          R.control_switch(db.SW_HOB2_ON, False),
          R.control_switch(db.SW_HOB2_DONE, True)]
    c += S.companion_story(db.HOB)
    return c


def gate_event(event_id, x, y):
    """The churchyard gate (Map 1), in the gap in the south wall: the old one,
    stuck, which you lift every time; the new one being hung; and the new
    one, which clicks. Below characters, walked through."""
    old = R.image("!Door2", 2, direction=6, pattern=2)
    new = R.image("!Door2", 3, direction=8, pattern=0)
    kw = dict(trigger=1, priority=0, direction_fix=True, walk_anime=False)
    return R.event(event_id, "The Churchyard Gate", x, y, [
        R.page(S.narrate(["The gate sticks. You lift it, and shove, and it",
                          "scrapes, and you are through."]), img=old, **kw),
        R.page(_hob2_hung(), img=old,
               conditions={"actorValid": True, "actorId": db.HOB,
                           "switch1Valid": True,
                           "switch1Id": db.SW_HOB2_CARRYING,
                           "variableValid": True,
                           "variableId": db.VAR_HOB2_TRY,
                           "variableValue": 4}, **kw),
        R.page([R.play_se("Switch1", pitch=70)], img=new,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_HOB2_DONE}, **kw),
    ])


# ======================================================================
# HOB-1, The Assize of Hammers (`QUESTS.md` B1)
# ----------------------------------------------------------------------
# The Worshipful Company of Smiths judges work every three years at Great
# Dunnage, and Hob has never entered: a piece has to be the entrant's own
# work *and* the entrant's own property (the Schedule, clauses one and two),
# and he does not own anything he has made. So it is a retrieval tour - eleven
# things in eleven hands, every owner glad to see him and none of them giving
# it back - and in the end he submits Beatrice, which is not his work, and is
# disqualified, and is entirely satisfied.
#
# * **The ask is the Prime Warden's**, Map 62 event 2, below her ladder (one
#   self switch, A), with Hob. The tally is a page above it on `SW_HOB1_ON`,
#   the submission a page above that on `VAR_HOB1_ASKED` 11, and afterwards
#   is her own last page on `SW_HOB1_DONE`, for everybody.
# * **Ten owners, each two appended pages**, `q_nix.returned`'s pattern: the
#   ask on the owner's own last-page conditions plus Hob plus `SW_HOB1_ON`, so
#   a ladder's set piece runs first; afterwards on self switch B, their own
#   last page with one narrated line added. `owned()` asserts nothing of
#   theirs uses B and their last page needs no more than A.
# * **The eleventh is Nix's lockpicks**, and Nix is in the party, not on a
#   map. They are asked at the Company's table: the ask and the tally pages
#   both carry the exchange behind "Nix is here and has not been asked", so a
#   party with both of them settles it in front of the Prime Warden, and one
#   without Nix is told who is missing when the other ten are done.
# * **A dismissed Hob leaves the tour where it is.** It is two switches and a
#   variable, all global.
ELEVEN = 11
NOTES_ICON = 191


def _hob1_nix():
    """The lockpicks, asked of Nix wherever Hob reports to the Prime Warden
    with Nix in the party; once."""
    c = S.say("Hob", ["And them picks. I made you them picks."])
    c += S.say("Nix", ["You did. Best set I've had."])
    c += S.say("Hob", ["Could I have them back? For the spring."])
    c += S.say("Nix", ["No."])
    c += S.narrate(["Hob waits. Nix gets out the ledger."])
    c += S.say("Nix", ["ACQUIRED: one set of picks, from",
                       "H. Grumnir, Thistlewick. Column: GIVEN."])
    c += S.say("Nix", ["Nothing comes out of GIVEN. Not even",
                       "for you. That's what it's for."])
    c += S.say("Hob", ["...That's a better reason than mine."])
    c += [R.control_switch(db.SW_HOB1_PICKS, True),
          R.control_variable_add(db.VAR_HOB1_ASKED, 1)]
    return R.if_then(R.condition_actor_in_party(db.NIX),
                     R.if_then(R.condition_switch(db.SW_HOB1_PICKS, False),
                               c))


def _hob1_ask():
    c = S.narrate([
        "Hob stands in front of the Company's table with his",
        "cap in both hands, which you have never seen."])
    c += S.say("Hob", ["Grumnir. Thistlewick. I'm a smith."])
    c += S.say("Prime Warden", [
        "Then you may submit.",
        "One piece. Your own work, from the ore",
        "up, and your own property."])
    c += S.say("Hob", ["Aye. That's where it comes unstuck."])
    c += S.narrate(["You ask why."])
    c += S.say("Hob", ["I don't own anything I've made. Never",
                       "have. Somebody wants a thing, I say",
                       "take it."])
    c += S.say("Prime Warden", ["And the invoicing?"])
    c += S.say("Hob", ["There's a shelf."])
    c += S.narrate([
        "The Prime Warden looks at him the way a toll-keeper",
        "looks at a bridge with nobody on it."])
    c += S.say("Prime Warden", ["Then you have never",
                                "entered."])
    c += S.say("Hob", ["Never once. I could get one back,",
                       "though. Just the one. For this, they'd",
                       "not mind."])
    c += S.narrate(["He counts on his fingers, and then on yours."])
    c += S.say("Hob", ["A share in the west field at home.",
                       "The goat's bell. A sword at Nether",
                       "Sopping. A trivet up at Hithermost."])
    c += S.say("Hob", ["The crown on the ribbon post at",
                       "Frostwick. Some hinges at Fairholme.",
                       "The post box at Ashcombe."])
    c += S.say("Hob", ["A helmet at Little Gore. Cotter's",
                       "heel-irons. Them tongs."])
    c += S.narrate([
        "Across the hall, Warden Crabbe goes very still, and",
        "puts a hand over his belt."])
    c += S.say("Hob", ["Eleven. One of them'll give it back.",
                       "Stands to reason."])
    c += S.narrate(["Nobody ever gives anything back."])
    c += [S.trope(), R.control_switch(db.SW_HOB1_ON, True)]
    return c + _hob1_nix()


def _hob1_tally():
    c = S.say("Prime Warden", ["Your piece, Mr",
                               "Grumnir?"])
    c += S.say("Hob", ["\\V[%d] of eleven asked. Not one of" %
                       db.VAR_HOB1_ASKED,
                       "them'll part with it. All very nice",
                       "about it."])
    c += _hob1_nix()
    c += R.if_then(R.condition_variable(db.VAR_HOB1_ASKED, ELEVEN - 1),
                   R.if_then(R.condition_switch(db.SW_HOB1_PICKS, False),
                             S.say("Hob", ["Just the picks to ask.",
                                           "Nix has them."])))
    return c


def _hob1_submit():
    c = S.say("Hob", ["Eleven asked. Eleven said no.",
                      "Every one of them had a better",
                      "reason than I had."])
    c += S.narrate([
        "He stands a while. Then he takes Beatrice off his",
        "belt and lays her on the Company's table, very",
        "gently, the way you would put down a sleeping cat."])
    c += S.say("Prime Warden", ["This is your piece?"])
    c += S.say("Hob", ["She's not mine to call a piece. I'd",
                       "like her looked at, proper. Once."])
    c += S.say("Prime Warden", [
        "Clause thirty-nine.",
        "A piece is examined on receipt against",
        "clauses one and two, so that nobody",
        "waits three years to be told."])
    c += S.narrate([
        "Warden Crabbe reads clause one out, and then clause",
        "two, which takes him rather less than the day. Miss",
        "Fettle comes from her bench without being asked, and",
        "turns Beatrice over in her hands for a long time."])
    c += S.say("Miss Fettle", ["Who made this?"])
    c += S.say("Hob", ["Not me. I'd never have got the",
                       "balance."])
    c += S.say("Prime Warden", [
        "Clause two: the",
        "entrant's property. Satisfied.",
        "Clause one: the entrant's own work."])
    c += S.say("Prime Warden", ["Not satisfied.",
                                "Disqualified."])
    c += [R.wait(30)]
    c += S.narrate([
        "Hob beams. You have never seen him so pleased about",
        "anything, and you have seen him given a pie."])
    c += S.say("Hob", ["Aye. She would be."])
    c += S.narrate([
        "The Prime Warden writes the notes on a card, and",
        "Warden Crabbe strikes the Company's mark on it, as is",
        "done for every piece examined. She hands it to Hob,",
        "and Beatrice back with it."])
    c += S.narrate([
        "  BEATRICE. A hammer. From H. Grumnir, Thistlewick.",
        "  Clause one: not satisfied. Two to forty-one:",
        "  satisfied. DISQUALIFIED. Remarks: in the",
        "  Wardens' opinion, right about everything."])
    c += S.say("Hob", ["...She'll be unbearable."])
    c += S.say("Hob", ["Every three years, is it? I'll not",
                       "bother. I've had what I came for."])
    c += [R.gain_item(db.IT_WARDENS_NOTES, 1), R.play_me("Fanfare1"),
          R.control_switch(db.SW_HOB1_DONE, True)]
    c += S.got(["Got \\I[%d]\\C[3]The Wardens' Notes\\C[0]." % NOTES_ICON])
    c += S.companion_story(db.HOB)
    return c


def warden_pages(page0):
    """Four pages for the Prime Warden (Map 62, event 2), whose ladder is one
    self switch: the ask, the tally, the submission, and afterwards - which is
    her own last page and a line, for everybody."""
    a_hob = {"selfSwitchValid": True, "selfSwitchCh": "A",
             "actorValid": True, "actorId": db.HOB}

    def pg(cmds, conds):
        new = R.page(cmds, conditions=conds)
        return dict(copy.deepcopy(page0), list=new["list"],
                    conditions=new["conditions"])

    return [
        pg(_hob1_ask(), a_hob),
        pg(_hob1_tally(), dict(a_hob, switch1Valid=True,
                               switch1Id=db.SW_HOB1_ON)),
        pg(_hob1_submit(), dict(a_hob, variableValid=True,
                                variableId=db.VAR_HOB1_ASKED,
                                variableValue=ELEVEN)),
    ]


def warden_after(last):
    """The Prime Warden once Beatrice has been examined: her own last page,
    and the card, for everybody. Appended after `warden_pages`."""
    page = copy.deepcopy(last)
    page["list"] = page["list"][:-1] + S.narrate([
        "Behind her, beside the prize hinge, a second card is",
        "pinned up, with the Company's mark on it."]) + page["list"][-1:]
    page["conditions"] = R.page([], conditions={
        "selfSwitchValid": True, "selfSwitchCh": "A",
        "switch1Valid": True, "switch1Id": db.SW_HOB1_DONE})["conditions"]
    return page


def prize_after(page0):
    """The Prize (Map 62, event 5) once Beatrice has been examined: the hinge
    as it always was, and her card beside it."""
    page = copy.deepcopy(page0)
    page["list"] = page["list"][:-1] + S.narrate([
        "Pinned beside it, a second card, with the same mark:",
        "BEATRICE. A hammer. DISQUALIFIED (clause one).",
        "Remarks: in the Wardens' opinion, right about",
        "everything."]) + page["list"][-1:]
    page["conditions"] = R.page([], conditions={
        "switch1Valid": True, "switch1Id": db.SW_HOB1_DONE})["conditions"]
    return page


# -- the ten ----------------------------------------------------------------
# Each is (scene, afterwards): the scene is Hob asking, and the owner saying
# no, nicely, with a reason; afterwards is one narrated line put on the end
# of the owner's own last page.

def _farmer():
    c = S.narrate([
        "Hob leans on the gate and looks at the west field,",
        "where a ploughshare is lying at the end of a furrow."])
    c += S.say("Hob", ["That's my share. Could I have it back?",
                       "Just till the spring."])
    c += S.say("Farmer", ["Spring? Spring's when I plough."])
    c += S.say("Farmer", ["And the weevils have had a good look",
                          "at that share, and they don't like it.",
                          "First year in ten."])
    c += S.say("Hob", ["...Fair."])
    return c, ["There is a ploughshare at the end of the west",
               "field. The weevils are keeping their distance."]


def _gossip():
    c = S.say("Hob", ["The goat's bell. I made that. Could",
                      "I have it back a while?"])
    c += S.say("Villager", ["Off the goat?"], face="Gossip")
    c += S.say("Villager", ["He'll not wear another. We tried him",
                            "in a brass one."], face="Gossip")
    c += S.say("Villager", ["He abstained from it."], face="Gossip")
    c += S.narrate([
        "Somewhere behind the cottages a good iron bell goes",
        "once, as if it has heard."])
    c += S.say("Hob", ["...He's got taste."])
    return c, ["Somewhere behind the cottages, a good iron bell.",
               "The goat is wearing it with dignity."]


def _regular():
    c = S.narrate([
        "Hob looks at the very good sword across the man's",
        "knees for a long time."])
    c += S.say("Hob", ["That's one of mine."])
    c += S.say("Regular", ["...Is it? Never once let me down."],
               face="Day Off")
    c += S.say("Hob", ["It wouldn't. Could I borrow it back?",
                       "For the spring."])
    c += S.say("Regular", ["It's having a day off."], face="Day Off")
    c += S.narrate([
        "He shuts his eyes again. So, in a manner of speaking,",
        "does the sword."])
    return c, ["The sword is across his knees. Neither of them",
               "is working today."]


def _hithermost():
    c = S.narrate([
        "The Hithermost teapot comes out, in its cosy, and is",
        "stood on an iron trivet worked like a sprig of holly."])
    c += S.say("Hob", ["That trivet's mine. Could I have it",
                       "back, for a bit?"])
    c += S.say("Villager", ["And stand the pot where? On the",
                            "cloth?"])
    c += S.say("Villager", ["They come down off that mountain",
                            "cold to the bone, every one of them,",
                            "and the first thing they get is a",
                            "pot of tea off that trivet."])
    c += S.say("Hob", ["...Aye. Keep it."])
    return c, ["The teapot is in its cosy, on its holly trivet.",
               "They do teas."]


def _perce():
    c = S.narrate([
        "The ribbon post has an iron crown on top of it,",
        "worked like frost on a window."])
    c += S.say("Hob", ["I did that crown. Could I have it",
                       "for the spring?"])
    c += S.say("Perce", ["The spring? The Festival's",
                         "on the twelfth."])
    c += S.say("Perce", ["Everybody ties a ribbon to that",
                         "crown. You can't tie a ribbon to a",
                         "bare post, you know. It slides down."])
    c += S.say("Hob", ["...It does, aye."])
    return c, ["The ribbon post has its iron crown. Ribbons",
               "do not slide off it."]


def _aldous():
    c = S.say("Hob", ["The hinges on the tower door.",
                      "Them's mine. Could I have them back?"])
    c += S.say("King Aldous", ["Your hinges? Oh dear.",
                               "They're the only part that's held."])
    c += S.say("King Aldous", ["We're on the fourteenth door.",
                               "Every rescuer kicks it in, and the",
                               "door goes, and the hinges are fine."])
    c += S.say("King Aldous", ["Take the hinges and there's only",
                               "so much door."])
    c += S.say("Hob", ["...Fourteen doors."])
    return c, ["There is a drawing of a door on the table. It is",
               "marked FIFTEENTH. The hinges are not drawn."]


def _dimmock():
    c = S.narrate([
        "The Ashcombe post box is iron, painted red, with a",
        "slot in it like a polite smile."])
    c += S.say("Hob", ["That box is mine. Could I have it",
                       "back a while?"])
    c += S.say("Mrs Dimmock", ["And where would the",
                               "letters go, dear?"])
    c += S.say("Mrs Dimmock", ["That box has had a",
                               "letter from the Ruins of Ashcombe",
                               "in it. You can't take a box back",
                               "after that."])
    c += S.say("Hob", ["...No. You can't."])
    return c, ["The red box is by the door, with a letter in it.",
               "It will be answered."]


def _winifred():
    c = S.narrate([
        "Dame Winifred wears her good plain helmet pushed back,",
        "and there is a small G stamped inside the brim."])
    c += S.say("Hob", ["That helmet's one of mine. Could I",
                       "borrow it back? For the spring."])
    c += S.say("Dame Winifred", ["I'm in it."])
    c += S.narrate([
        "That turns out to be the whole of her reason, and it",
        "is a very good one."])
    c += S.say("Dame Winifred", ["Not a dent in it. Nothing",
                                 "to report. That's your helmet."])
    return c, ["She is in her helmet. There is still nothing to",
               "report."]


def _cotter():
    c = S.narrate([
        "Cotter's boots are shod with iron at heel and toe,",
        "worn bright."])
    c += S.say("Hob", ["Them's my heel-irons. Could I have",
                       "them back, till the spring?"])
    c += S.say("Cotter", ["Till the spring?",
                          "I'm home in the spring. For good."])
    c += S.say("Cotter", ["Eleven miles up every Saturday,",
                          "and eleven back. I'd not get home",
                          "without them."])
    c += S.say("Hob", ["...Aye. Get home."])
    return c, ["His boots are shod with iron, worn bright.",
               "Saturday. Six o'clock."]


def _crabbe():
    c = S.narrate([
        "Warden Crabbe has a pair of tongs at his belt, and is",
        "standing in front of them as hard as he can."])
    c += S.say("Hob", ["Them tongs are mine."])
    c += S.say("Warden Crabbe", ["These are the",
                                 "Company's tongs. Every piece at the",
                                 "Assize goes onto the table in them."])
    c += S.say("Warden Crabbe", ["A pair of tongs is",
                                 "a piece. Clause forty. But not your",
                                 "property. Clause two."])
    c += S.say("Warden Crabbe", ["You would be",
                                 "disqualified by your own tongs."])
    c += S.say("Hob", ["...It's a very good Schedule."])
    return c, ["He has the tongs at his belt, and is standing",
               "in front of them."]


OWNERS = {
    "farmer": _farmer, "gossip": _gossip, "regular": _regular,
    "hithermost": _hithermost, "perce": _perce, "aldous": _aldous,
    "dimmock": _dimmock, "winifred": _winifred, "cotter": _cotter,
    "crabbe": _crabbe,
}
assert len(OWNERS) == ELEVEN - 1        # and Nix's picks


def _hob1_asked(scene):
    return scene + [
        R.control_variable_add(db.VAR_HOB1_ASKED, 1),
        R.self_switch("B", True),
    ] + R.if_then(
        R.condition_variable(db.VAR_HOB1_ASKED, ELEVEN, 1),
        S.narrate(["That is the eleventh. Hob would like to go back",
                   "to Great Dunnage, and he has a look about him."]))


def owned(key, ev):
    """Append HOB-1's two pages to an owner's event and hand it back, so a
    place module's hook is one line round the event it already builds."""
    pages = ev["pages"]
    last = pages[-1]
    conds = last["conditions"]
    assert not (conds["switch1Valid"] or conds["switch2Valid"] or
                conds["variableValid"] or conds["itemValid"] or
                conds["actorValid"]), (key, conds)
    assert conds["selfSwitchCh"] == "A" or not conds["selfSwitchValid"], key
    for p in pages:
        for c in p["list"]:
            assert not (c["code"] == 123 and c["parameters"][0] == "B"), key
    scene, after = OWNERS[key]()
    ask = R.page(_hob1_asked(scene), conditions=dict(
        {k: v for k, v in conds.items() if k.startswith("selfSwitch")},
        switch1Valid=True, switch1Id=db.SW_HOB1_ON,
        actorValid=True, actorId=db.HOB))
    again = copy.deepcopy(last)
    again["list"] = again["list"][:-1] + S.narrate(after) + again["list"][-1:]
    again["conditions"] = R.page([], conditions={
        "selfSwitchValid": True, "selfSwitchCh": "B"})["conditions"]
    pages.append(dict(copy.deepcopy(last), list=ask["list"],
                      conditions=ask["conditions"]))
    pages.append(again)
    return ev


# ================================================================ HOB-4 ==
# The Sky Anvil (`QUESTS.md` E15). A meteorite fell in 1749 and has been a
# farm gatepost ever since. Elias Meech will not sell his gatepost, because it
# is a very good gatepost, but he will trade it for a gate - and Hob has
# lately become quite good at gates, so it needs HOB-2 (`COMPANIONS.md`: the
# one place a chain earns the dependency).
#
# * **The trade is at the Sky Anvil** (`nomap.py`'s world-map cell), below
#   its ladder (self switch A) with Hob and `SW_HOB2_DONE`. The gate is made
#   there and then, cold, out of the eleven gates the gatepost has outlasted,
#   which Meech has never thrown out - and the spring Hob has carried since
#   the churchyard goes on the latch. The star-iron is a key item, so a
#   dismissed Hob's errand is in the bag, waiting.
# * **The sword is made at Hob's forge** (Map 6 event 6), below HOB-2's
#   afterwards page and carrying it: exactly one thing, a sword, which his
#   class cannot hold. He will not say who it is for.
# * **Afterwards for everybody**: the Sky Anvil with a gate on it.
STAR_ICON = 313
STAR_SWORD_ICON = 119


def _hob4_trade():
    c = S.say("Meech", ["Still between gates. If you come across",
                        "a good one, you know where I am."])
    c += S.narrate([
        "Hob puts his hand flat on the grey stone in the top of",
        "the shrine, the way you would put it on a horse."])
    c += S.say("Hob", ["That's star-iron. That's come down",
                       "out of the sky, that has."])
    c += S.say("Meech", ["On a Tuesday."])
    c += S.say("Hob", ["I'll make you a gate for it."])
    c += S.say("Meech", ["Out of what? I've no iron.",
                         "Never thrown a gate out, mind."])
    c += S.narrate([
        "He has not. All eleven are in the hedge-bottom along the",
        "top field, where each was put when it went, rusting",
        "quietly in order."])
    c += S.narrate([
        "Hob has them out one after another and sorts them on the",
        "snow into what will do and what won't, and works the",
        "afternoon through, cold, with what he carries in his pack."])
    c += [R.play_se("Hammer", 70), R.wait(30), R.play_se("Hammer", 70),
          R.wait(30)]
    c += S.narrate([
        "A gate, out of eleven gates, true on its hangings. Then he",
        "takes a spring out of his pocket, where it has been since a",
        "churchyard in Thistlewick, and fits it to the latch."])
    c += S.say("Hob", ["Latch wanted a spring."])
    c += S.narrate([
        "Meech hangs it on the shrine himself. It swings to, and",
        "the latch drops, and stays."])
    c += [R.play_se("Door1", 80)]
    c += S.say("Meech", ["...That's a very good gate."])
    c += S.say("Meech", ["Go on, then. Take it. Mind",
                         "your back."])
    c += S.narrate([
        "Hob lifts the Sky Anvil out of the top of the shrine like",
        "an egg out of an egg cup, and puts it under one arm. It is",
        "very heavy. He does not mention this."])
    c += [R.gain_item(db.IT_STAR_IRON, 1), R.play_me("Item")]
    c += S.got(["Got \\I[%d]\\C[3]Star-Iron\\C[0]." % STAR_ICON])
    c += S.say("Meech", ["Pilgrims'll miss it."])
    c += S.say("Hob", ["They've a gate to open now."])
    c += [S.trope(), R.control_switch(db.SW_HOB4_TRADED, True)]
    return c


def sky_anvil_pages(again):
    """Two pages for the Sky Anvil (Map 8), whose ladder is self switch A:
    with Hob, once HOB-2 is done, the trade; and afterwards, for everybody,
    a gate on the shrine. `again` is the site's own second-visit narration."""
    stop = ["Stop a while", "Press on"]
    trade = list(again) + R.choice_block(stop, [_hob4_trade(), []])
    after = S.narrate([
        "The Sky Anvil, in the snow, with a gate hung on it now",
        "and nothing in the top. Elias Meech is leaning on the",
        "gate."]) + R.choice_block(stop, [S.say("Meech", [
            "Best gate in the county. Pilgrims",
            "come up and open it and shut it all",
            "afternoon. Nobody's ever given them",
            "anything to open before."]), []])
    a = {"selfSwitchValid": True, "selfSwitchCh": "A"}
    page = dict(trigger=1, priority=0, through=True, img=R.image(""))
    return [
        R.page(trade, conditions=dict(a, actorValid=True, actorId=db.HOB,
                                      switch1Valid=True,
                                      switch1Id=db.SW_HOB2_DONE), **page),
        R.page(after, conditions=dict(a, switch1Valid=True,
                                      switch1Id=db.SW_HOB4_TRADED), **page),
    ]


def _hob4_sword():
    c = S.narrate([
        "Hob puts the star-iron in the fire and says nothing for a",
        "long time, which for Hob is about a minute."])
    c += [R.play_se("Fire1", 70), R.wait(30)]
    c += S.narrate([
        "It makes exactly one thing. He knew it would. He makes a",
        "sword - plain, long in the blade, that takes the light",
        "like frost on a window."])
    c += [R.play_se("Hammer", 80), R.wait(20), R.play_se("Hammer", 80),
          R.wait(40)]
    c += S.narrate([
        "Hob cannot use a sword. Everybody in the smithy knows it,",
        "and nobody says so. You ask who it is for."])
    c += S.say("Hob", ["Nobody. It's a sword. Swords are",
                       "for whoever."])
    c += S.narrate(["He listens to the hammer at his belt for a while."])
    c += S.say("Hob", ["She says a sword's no use on its own."])
    c += S.say("Hob", ["It's not on its own."])
    c += S.narrate([
        "He wraps it in sacking and puts it in your pack, and does",
        "not look at anybody, and goes to see about the fire."])
    lose = R.gain_item(db.IT_STAR_IRON)
    lose["parameters"] = [db.IT_STAR_IRON, 1, 0, 1]     # operation 1: decrease
    c += [lose, R.gain_weapon(db.WP_STAR_IRON, 1), R.play_me("Item")]
    c += S.got(["Got \\I[%d]\\C[3]Star-Iron Sword\\C[0]." % STAR_SWORD_ICON])
    c += [R.control_switch(db.SW_HOB4_DONE, True)]
    c += S.companion_story(db.HOB)
    return c


def star_iron_page(last):
    """The forge (Map 6 event 6), below HOB-2's afterwards page and carrying
    it: with Hob and the star-iron, the sword."""
    page = copy.deepcopy(last)
    page["list"] = R.page(last["list"][:-1] + _hob4_sword())["list"]
    page["conditions"] = R.page([], conditions={
        "switch1Valid": True, "switch1Id": db.SW_HOB2_DONE,
        "itemValid": True, "itemId": db.IT_STAR_IRON,
        "actorValid": True, "actorId": db.HOB})["conditions"]
    return [page]
