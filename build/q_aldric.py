"""Sir Aldric's companion quests - `COMPANIONS.md`, his section, and
`QUESTS.md` for the order they are built in.

Nothing here draws a map, and this module imports no place module: the place
modules call in here for pages.

ALD-4, The Horse (`QUESTS.md` B2)
---------------------------------
He had a horse. Nobody has asked about the horse in six years, Aldric
included. The horse is fine: she walked in off the west road one winter with a
good saddle on and nobody in it, and she is a partner in a haulage business
now, and plans the Tuesdays. The reunion is a scene, and the only reward in
`COMPANIONS.md` that is a scene and nothing else. It should stay that way.

* **It is Mr Plummer's**, Map 61 event 14, a page below his ladder (one self
  switch, A) with Aldric: he has already told the party about the grey and the
  crest on her saddle, and with Aldric standing there he notices the crest on
  a tabard. Duchess cannot speak - nobody has drawn her a face - so she is
  wordless: a sound, a balloon, and the narrator.
* **Duchess's own pages** (event 15) have Aldric pat a good horse in passing
  without knowing her. After the reunion that would be wrong, so the scene
  sets her self switch A - her ladder's terminal - and her page on
  `SW_ALD4_DONE` with Aldric needs only that.
* **Afterwards is for everybody**: Plummer's last page with a line, and the
  sign under the sign.
"""
import copy

import db
import rmmzdata as R
import story as S
from places import MAP_DUNNAGE

DUCHESS_EVENT = 15              # Map 61; Plummer's scene points at her


def _ald4_reunion():
    c = S.narrate([
        "Mr Plummer looks at Sir Aldric's tabard for rather a",
        "long time: a knight on it, in a field, facing the",
        "wrong way."])
    c += S.say("Mr Plummer", ["Begging your pardon,",
                              "sir. That crest."])
    c += S.narrate([
        "He goes into the stable and comes back with a saddle,",
        "old and very well kept, and the same knight tooled into",
        "the flap of it, looking back over his shoulder."])
    c += S.say("Aldric", ["...That's my saddle."])
    c += S.say("Aldric", ["I had a horse. I had a horse! I came",
                          "into a village with a sign, and I tied",
                          "her up, and went to find the gate -"])
    c += S.narrate([
        "It occurs to you that in six years nobody has asked",
        "Sir Aldric about his horse. Including Sir Aldric."])
    c += [R.play_se("Horse", 80), R.wait(20),
          R.show_balloon(DUCHESS_EVENT, 1, True)]
    c += S.narrate([
        "Across the yard, the grey lifts her head from the road",
        "for the first time, and looks at him."])
    c += S.narrate([
        "He crosses to her, slowly, the way you would walk up to",
        "something you were not sure was there, and she puts her",
        "nose into the front of his tabard, where it always went,",
        "and breathes out."])
    c += [R.show_balloon(DUCHESS_EVENT, 4, True), R.wait(30)]
    c += S.say("Aldric", ["Hello, old girl."])
    c += [R.wait(40)]
    c += S.say("Aldric", ["I'm so sorry. I couldn't find the",
                          "gate."])
    c += S.narrate([
        "She does not seem to mind. She has found every road in",
        "the valley since."])
    c += S.say("Mr Plummer", ["What did you call",
                              "her, sir?"])
    c += S.say("Aldric", ["...Do you know, I only ever called",
                          "her Horse."])
    c += S.say("Mr Plummer", ["Duchess, then."])
    c += S.say("Aldric", ["Duchess. Yes. It suits her."])
    c += S.say("Mr Plummer", ["She'd be yours, of",
                              "course, sir. Saddle and all. Only -",
                              "she does the canal run. And the",
                              "Tuesdays. And -"])
    c += S.narrate([
        "He stops, because he is a tactful man. Duchess looks at",
        "the road, and then at Sir Aldric, and then at the cart",
        "with her name on it."])
    c += S.say("Aldric", ["Oh, no. No, no. Look at her."])
    c += [R.wait(30)]
    c += S.say("Aldric", ["She is doing so well."])
    c += S.narrate([
        "He means it. You can see that he means it, and you can",
        "see what it costs him, and he would not thank you for",
        "saying either."])
    c += S.say("Aldric", ["Might I visit? Not on a Tuesday."])
    c += S.say("Mr Plummer", ["Any day but a Tuesday,",
                              "sir. She'd like that."])
    c += [S.trope(), R.control_switch(db.SW_ALD4_DONE, True)]
    c += R.script(["$gameSelfSwitches.setValue([%d, %d, 'A'], true);"
                   % (MAP_DUNNAGE, DUCHESS_EVENT)])
    c += S.companion_story(db.ALDRIC)
    return c


def plummer_pages(last):
    """Two pages for Mr Plummer (Map 61, event 14), whose ladder is one self
    switch: the reunion, with Aldric; and afterwards, which is his own last
    page and a line, for everybody."""
    reunion = R.page(_ald4_reunion(), conditions={
        "selfSwitchValid": True, "selfSwitchCh": "A",
        "actorValid": True, "actorId": db.ALDRIC})
    after = copy.deepcopy(last)
    after["list"] = after["list"][:-1] + S.narrate([
        "Sir Aldric, he says, is welcome any day but a Tuesday.",
        "She would like that."]) + after["list"][-1:]
    after["conditions"] = R.page([], conditions={
        "selfSwitchValid": True, "selfSwitchCh": "A",
        "switch1Valid": True, "switch1Id": db.SW_ALD4_DONE})["conditions"]
    return [dict(copy.deepcopy(last), list=reunion["list"],
                 conditions=reunion["conditions"]), after]


def duchess_page(last):
    """Duchess (Map 61, event 15) after the reunion, with Aldric: she knows
    him now, and he knows her."""
    page = R.page(S.narrate([
        "Duchess puts her nose into the front of Sir Aldric's",
        "tabard, and breathes out. He tells her about his week.",
        "She is considering the Tuesdays."]), conditions={
        "selfSwitchValid": True, "selfSwitchCh": "A",
        "switch1Valid": True, "switch1Id": db.SW_ALD4_DONE,
        "actorValid": True, "actorId": db.ALDRIC})
    return dict(copy.deepcopy(last), list=page["list"],
                conditions=page["conditions"])


def sign_page(page0):
    """The yard's sign (Map 61, event 17) afterwards: as it was, and one more
    line under it, in a third paint."""
    page = copy.deepcopy(page0)
    page["list"] = page["list"][:-1] + S.narrate([
        "And under that, newer, in a third hand, very neat:",
        "(HER KNIGHT CALLS. NOT TUESDAYS.)"]) + page["list"][-1:]
    page["conditions"] = R.page([], conditions={
        "switch1Valid": True, "switch1Id": db.SW_ALD4_DONE})["conditions"]
    return page
