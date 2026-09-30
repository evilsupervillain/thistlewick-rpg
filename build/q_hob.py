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
