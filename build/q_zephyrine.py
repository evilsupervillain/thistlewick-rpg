"""Zephyrine Vance's companion quests - `COMPANIONS.md`, her section, and
`QUESTS.md` for the order they are built in.

Nothing here draws a map, and this module imports no place module: the place
modules call in here for pages.

ZEPH-5, The Lay-By (`QUESTS.md` A7)
-----------------------------------
Three hedge mages, nine years without a name, an igloo in a lay-by on the
west road. They are all excellent. Dunnock taught himself out of a book with
four pages missing, and is better than the Collegium at exactly those four
things; he teaches her one of them, badly, and it works.

* **It hangs off the Lay-By's world-map event** (`nomap.py`), whose two pages
  are a stop and its short version on self switch A. Page 3 needs A and
  Zephyrine, so she gets the association's first scene first, as anybody
  does; page 4 adds `SW_ZEPH5_DONE`. A party without her sees the lay-by as
  it was, forever.
* **Both pages ask before they start**, like every world-map site: a cell on
  the west road is walked over by people going somewhere else.
* **The skill is `SK_PAGE_23`**, in the free end of her block (46). It is
  Kindle worked out by a man who never saw the page: weaker, cheaper, and
  aimed at three enemies it has not been told about.
"""
import db
import rmmzdata as R
import story as S

STOP = "Look in"


def _stop(opening, scene):
    """The world map's idiom: say what is here, then ask."""
    return opening + R.choice_block(
        [STOP, "Press on"], [scene, S.narrate(["You press on."])])


def _the_page():
    """Page twenty-three. The whole of ZEPH-5."""
    c = S.narrate([
        "Three people round a folding table in the igloo,",
        "with the minutes. Miss Privet sees Zephyrine and",
        "puts her pen down."])
    c += S.say("Miss Privet", ["Oh. It's Vance."])
    c += S.say("Mrs Quickset", ["The one who set fire",
                                "to the Dean."])
    c += S.say("Dunnock", ["Collegium."])
    c += S.say("Zephyrine", ["Formerly."])
    c += S.say("Dunnock", ["We don't take Collegium."])
    c += S.say("Zephyrine", ["Neither does the Collegium."])
    c += S.narrate([
        "There is a pause, of the kind that is going into",
        "the minutes."])
    c += S.say("Miss Privet", ["Item two. Admission of a",
                               "member. Any objections?"])
    c += S.say("Dunnock", ["One."])
    c += S.say("Dunnock", ["Show us summat. Out of the",
                           "book. Not in here - it's an igloo."])
    c += S.narrate([
        "Outside, in the lay-by, Dunnock opens a book with",
        "a brown paper cover. Four pages have been torn out",
        "and replaced in pencil, in his hand."])
    c += S.say("Dunnock", ["Page twenty-three. Kindle."])
    c += S.say("Zephyrine", ["I know Kindle. I was the best",
                             "in my year at Kindle."])
    c += S.say("Dunnock", ["Not this one you weren't."])
    c += S.say("Dunnock", ["You don't aim it. You sort of",
                           "mean it, at everything, and it",
                           "sorts itself out."])
    c += S.say("Zephyrine", ["That is not how any of it works.",
                             "That is not how fire works."])
    c += S.say("Dunnock", ["Page was missing. Go on."])
    c += S.narrate([
        "Zephyrine sighs, means it at everything, and does",
        "not aim."])
    c += [R.play_se("Fire1"), R.wait(10), R.play_se("Fire2", pitch=110),
          R.wait(10), R.play_se("Fire1", pitch=90), R.wait(30)]
    c += S.narrate([
        "A gorse bush, a milestone and the lay-by's litter",
        "bin catch fire, all at once, neatly, and go out.",
        "Nobody is anywhere near any of them."])
    c += S.say("Zephyrine", ["...That should not have worked."])
    c += S.say("Dunnock", ["Page was missing."])
    c += S.say("Miss Privet", ["Objection withdrawn. Carried.",
                               "Item one?"])
    c += S.narrate([
        "Zephyrine proposes a name. It is a good name.",
        "It is carried forward, under nine years of other",
        "good names."])
    c += [R.learn_skill(db.ZEPH, db.SK_PAGE_23), R.play_me("Item")]
    c += S.got(["Zephyrine learned \\C[3]Page Twenty-Three\\C[0]."])
    c += [S.trope(), R.control_switch(db.SW_ZEPH5_DONE, True)]
    c += S.companion_story(db.ZEPH)
    return c


def _member():
    """Once she is a member. The minutes, as ever."""
    c = S.say("Miss Privet", ["Vance. Sit down, dear.",
                              "Item one, carried forward."])
    c += S.say("Dunnock", ["Page twenty-three holding up?"])
    c += S.say("Zephyrine", ["It should not be.",
                             "It is."])
    c += S.say("Dunnock", ["Aye. They do that."])
    return c


def lay_by_pages():
    """Pages 3 and 4 of the Lay-By's world-map event, in its dress:
    player-touch, below characters, walked through."""
    opening = S.narrate([
        "The igloo in the lay-by. Somebody inside says",
        "'Collegium' in the voice people use for weather."])
    again = S.narrate([
        "The igloo in the lay-by. There is a chair at the",
        "folding table now with nobody's coat on it."])
    seen = {"selfSwitchValid": True, "selfSwitchCh": "A",
            "actorValid": True, "actorId": db.ZEPH}
    kw = dict(img=R.image(""), trigger=1, priority=0, through=True)
    return [
        R.page(_stop(opening, _the_page()), conditions=seen, **kw),
        R.page(_stop(again, _member()),
               conditions=dict(seen, switch1Valid=True,
                               switch1Id=db.SW_ZEPH5_DONE), **kw),
    ]
