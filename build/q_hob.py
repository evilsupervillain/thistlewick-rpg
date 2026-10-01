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

HOB-3, The Anvil (`QUESTS.md` A8) is at the bottom: the smithy's anvil as
an event, Beatrice while it is gone, and the three events outside the door.

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
        "Nobody says anything. Nobody needs to. It is,",
        "plainly, the best afternoon either of them has",
        "had in twenty years, and neither of them is going",
        "to be so careless as to mention it."])
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
        "She tries each hole with her little finger, all",
        "forty-one of them, and nods at every one."])
    c += S.say("Ott", ["Tight. All the way round."])
    c += [S.blush()]
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
