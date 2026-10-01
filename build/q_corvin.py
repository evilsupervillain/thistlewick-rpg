"""Corvin Ash's companion quests - `COMPANIONS.md`, his section, and
`QUESTS.md` for the order they are built in.

Nothing here draws a map, and this module imports no place module: the place
modules call in here for pages.

COR-5, The Appraisal (`QUESTS.md` B4)
-------------------------------------
He takes the black sword to be appraised, expecting a curse. There is no
curse. It is a very good sword in poor condition with a name on the tang
nobody can say aloud, and the appraiser is enthusiastic about the tang. He
asks what a curse would cost to have put on. It is not expensive. She has a
form.

* **It is Miss Fettle's**, Map 62 event 7, below her one-self-switch ladder,
  with Corvin. Both her own pages already eye his sword and are told "No";
  this is the page where he says yes. The appraisal is once
  (`SW_COR5_DONE`); after it, the same page is the curse counter.
* **The curse is state 40**, "Cursed (Elective)": half luck, drawn fire and a
  slow bleed, which is to say a real trait and bad for him, and he takes it.
  It is optional - the form can be declined, and is offered again - and it
  is removable: Miss Fettle takes it off for nothing, and it is the economy
  curse, so it lasts until he next sleeps in a proper bed (an inn's Recover
  All clears it, which is the engine's own rule for states, stated as hers).
* **Afterwards for everybody** is her own last page and a line.
"""
import copy

import db
import rmmzdata as R
import story as S

FEE = 30


def _cor5_state(add=True):
    """Change State on Corvin: add or remove the elective curse."""
    return {"code": 313, "indent": 0,
            "parameters": [0, db.CORVIN, 0 if add else 1, db.ST_CURSED]}


def _cor5_curse():
    c = [R.lose_gold(FEE), R.play_se("Darkness1", 70), R.wait(20),
         _cor5_state(True)]
    c += S.narrate([
        "Miss Fettle stamps the form, reads a short paragraph",
        "off the back of it in a bored voice, and blows out a",
        "candle. The black sword does not look any different."])
    c += S.say("Miss Fettle", ["There. Cursed. It's the",
                               "economy one: it lasts till you next",
                               "sleep in a proper bed."])
    c += S.narrate([
        "Corvin buckles the sword back on, and stands up a",
        "little straighter than he has stood all year."])
    return c


def _cor5_offer():
    """The form, offered: yes if the party can pay, and Corvin pleased."""
    yes = R.if_then(R.condition_script("$gameParty.gold() >= %d" % FEE),
                    _cor5_curse(),
                    S.say("Miss Fettle", ["Thirty crowns, I'm",
                                          "afraid. The form's free."]))
    no = S.say("Corvin", ["...Another time."])
    return R.choice_block(["Have it cursed (%dcr)" % FEE, "Not today"],
                          [yes, no])


def _cor5_appraisal():
    c = S.narrate([
        "Corvin unbuckles the black sword and lays it on her",
        "bench, the way a man lays down a confession."])
    c += S.say("Corvin", ["Appraise it. Tell me what is on it."])
    c += S.say("Miss Fettle", ["Oh! Oh, may I - the",
                               "handle -"])
    c += S.say("Corvin", ["Yes."])
    c += S.narrate([
        "She has the handle off it in a trice. Corvin looks at",
        "the ceiling while she does, which has nothing on it."])
    c += S.say("Miss Fettle", ["Oh, look at that. Nobody's",
                               "had that out in years. Oh, the",
                               "TANG."])
    c += [S.blush()]
    c += S.narrate(["She is some minutes with the tang."])
    c += S.say("Corvin", ["The curse."])
    c += S.say("Miss Fettle", ["The what? There's no",
                               "curse on this. Not a trace."])
    c += S.say("Miss Fettle", ["It's a very good sword",
                               "in very poor condition. You've been",
                               "sitting in corners with it."])
    c += S.say("Miss Fettle", ["There's a name on the",
                               "tang, in letters nobody's used for a",
                               "while. I'd not like to try it aloud."])
    c += S.narrate([
        "Corvin is quiet for a long time. Then, carefully, as if",
        "asking the price of something in a shop that might be",
        "too good for him:"])
    c += S.say("Corvin", ["How much would a curse cost? To",
                          "have one put on."])
    c += S.say("Miss Fettle", ["Oh, not much. They're",
                               "mostly paperwork. There's a form."])
    c += S.narrate([
        "From a drawer she takes FORM C-1: APPLICATION FOR A",
        "CURSE (ELECTIVE), in triplicate, and a pen."])
    c += [S.trope(), R.control_switch(db.SW_COR5_DONE, True)]
    c += S.companion_story(db.CORVIN)
    c += _cor5_offer()
    return c


def _cor5_counter():
    """After the appraisal, with Corvin: the curse on, or off."""
    cursed = S.say("Miss Fettle", ["Still cursed? Lovely.",
                                   "Want it off? No charge."])
    cursed += R.choice_block(
        ["Take it off", "Leave it"],
        [[_cor5_state(False), R.play_se("Recovery", 70)] + S.narrate([
            "She relights the candle. It comes off with no fuss at",
            "all, which Corvin finds a little disappointing."]),
         S.say("Corvin", ["Leave it."])])
    clean = S.say("Miss Fettle", ["Back for another? It",
                                  "wears off, the economy one."])
    clean += _cor5_offer()
    return R.if_then(R.condition_script(
        "$gameActors.actor(%d).isStateAffected(%d)" % (db.CORVIN,
                                                       db.ST_CURSED)),
        cursed, clean)


def fettle_pages(last):
    """Two pages for Miss Fettle (Map 62, event 7), whose ladder is one self
    switch: the appraisal and the curse counter with Corvin, and afterwards
    for everybody."""
    a_cor = {"selfSwitchValid": True, "selfSwitchCh": "A",
             "actorValid": True, "actorId": db.CORVIN}
    cmds = R.if_then(R.condition_switch(db.SW_COR5_DONE), _cor5_counter(),
                     _cor5_appraisal())
    page = R.page(cmds, conditions=a_cor)
    after = copy.deepcopy(last)
    after["list"] = after["list"][:-1] + S.narrate([
        "Pinned over her bench, a form C-1, stamped, and a",
        "drawing of a tang, very lovingly done."]) + after["list"][-1:]
    after["conditions"] = R.page([], conditions={
        "selfSwitchValid": True, "selfSwitchCh": "A",
        "switch1Valid": True, "switch1Id": db.SW_COR5_DONE})["conditions"]
    return [after, dict(copy.deepcopy(last), list=page["list"],
                        conditions=page["conditions"])]
