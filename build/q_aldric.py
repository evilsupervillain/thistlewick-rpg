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
from places import MAP_DUNNAGE, COLDBARROW_MAP_AT_LARGE

DUCHESS_EVENT = 15              # Map 61; Plummer's scene points at her


def _like(page0, cmds, conditions):
    """A page in exactly another page's dress - image, priority, movement -
    with its own commands and conditions (`q_merribell._like`)."""
    shaped = R.page(cmds, conditions=conditions)
    page = copy.deepcopy(page0)
    page["list"] = shaped["list"]
    page["conditions"] = shaped["conditions"]
    return page


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


# ======================================================================
# ALD-3, The Chapter House (`QUESTS.md` E4)
# ----------------------------------------------------------------------
# The Order of the Errant keeps a great map with a pin for every knight in
# the field. Aldric has nine. The Order has formed a committee and would like
# him to stay put for the duration of the review, which is the one thing he
# cannot do and the one thing he has always wanted to be asked. He is offered
# a promotion contingent on remaining in one place, and refuses it
# beautifully.
#
# * **The start is Mordaunt's second look** (Map 48 event 2: his A and
#   Aldric). His first page with Aldric is the published "The committee will
#   write." On the second it is Thursday, and the committee sits.
# * **The committee is Mordaunt**, appointed to it four times, so he sits in
#   each of the four seats in turn and is quorate. No faces.
# * **The rank is the answer to the data problem**: the knight cannot stay
#   with the pin, so the pin goes with the knight. Knight Errant, At Large -
#   Change Nickname on his actor, which is the one place a rank shows - and
#   one red pin on his tabard. The map is correct wherever he is.
# * **Afterwards for everybody**: Mordaunt, the great map (a second picture
#   with no red pins, `coldbarrow.draw_map`), and the committee's table.
ALD3_RANK = "Knight Errant, At Large"


def _ald3_picture(indent=0):
    """Show Picture 1: the great map as it is now, with no red pins in it."""
    return [{"code": 231, "indent": indent,
             "parameters": [1, COLDBARROW_MAP_AT_LARGE, 1, 0, 408, 222, 84,
                            84, 255, 0]}]


def _ald3_committee():
    c = S.narrate([
        "Mordaunt looks up from the map, sees Sir Aldric, and puts",
        "his fistful of pins down on the desk, very carefully, as",
        "if they might go off."])
    c += S.say("Mordaunt", [
        "Sir Aldric. It is Thursday.",
        "The committee will see you now."])
    c += S.narrate([
        "He crosses to the committee's table and sits in the first",
        "chair. Then he gets up and sits in the second, and then",
        "on each of the stools. Then he stands behind them all."])
    c += S.say("Aldric", ["Is it just you, Mordaunt?"])
    c += S.say("Mordaunt", [
        "It is the committee, sir. I have",
        "been appointed to it four times.",
        "We are quorate."])
    c += S.say("Mordaunt", [
        "Finding one: nine pins. Finding",
        "two: all nine are correct. Finding",
        "three: three of them are the same",
        "week."])
    c += S.say("Mordaunt", [
        "The committee has been unable to",
        "fault the pins. It has therefore",
        "had to fault the knight."])
    c += S.say("Aldric", ["Entirely fair."])
    c += S.say("Mordaunt", [
        "Recommendation: that Sir Aldric be",
        "requested to REMAIN IN ONE PLACE",
        "for the duration of the review."])
    c += S.say("Mordaunt", ["You are so requested, sir.",
                            "Informed. In ink."])
    c += S.narrate([
        "Sir Aldric goes very still. In six years of trying to",
        "leave Thistlewick, nobody has ever once asked him to",
        "stay anywhere."])
    c += S.say("Mordaunt", [
        "And the committee is empowered to",
        "offer: Knight Commander of the",
        "Chapter. A desk. Here. A pin that",
        "does not move."])
    c += S.say("Mordaunt", ["Contingent on remaining in",
                            "one place."])
    c += S.narrate([
        "It is the one thing he cannot do, and the one thing he",
        "has always wanted to be asked. Everybody in the room can",
        "see both of those at once, including the knight."])
    c += S.say("Aldric", [
        "Mordaunt. That is the finest thing",
        "I have been offered in nine years.",
        "Thank you."])
    c += S.say("Aldric", ["No."])
    c += S.say("Aldric", [
        "A knight who stays put is a post.",
        "Dame Winifred is a very fine post,",
        "and she is happy, and I honour her."])
    c += S.say("Aldric", [
        "I should be at that desk by nine",
        "every morning. And I should never",
        "once find it twice."])
    c += S.say("Aldric", [
        "But you asked. Nobody asks a man to",
        "stay. Put that in the minutes, would",
        "you? In ink."])
    c += S.narrate([
        "Mordaunt writes for some time. Then he reads it back to",
        "himself, and crosses nothing out, which the ledger on his",
        "desk would tell you is a first."])
    c += S.say("Mordaunt", [
        "Then the committee has a data",
        "problem, sir. The knight cannot",
        "stay with the pin."])
    c += S.say("Mordaunt", ["Resolved: that the pin go",
                            "with the knight."])
    c += S.narrate([
        "He goes along the great map and takes out the nine red",
        "pins one at a time, and puts eight of them in the heap on",
        "his desk. The ninth he holds out."])
    c += S.say("Mordaunt", [
        "Knight Errant, At Large. A rank of",
        "the Order, created this Thursday.",
        "The pin goes with the knight."])
    c += S.say("Mordaunt", [
        "And wherever the knight is, sir,",
        "the map is correct. That is the",
        "system now."])
    c += S.narrate([
        "Sir Aldric pins it to his tabard, over the knight who is",
        "facing the wrong way, and stands up very straight."])
    c += S.say("Aldric", ["Splendid fellow."])
    c += [{"code": 324, "indent": 0, "parameters": [db.ALDRIC, ALD3_RANK]},
          R.play_me("Fanfare1")]
    c += S.got(["Sir Aldric is now \\C[3]%s\\C[0]." % ALD3_RANK])
    c += [S.trope(), R.control_switch(db.SW_ALD3_DONE, True)]
    c += S.companion_story(db.ALDRIC)
    return c


def mordaunt_pages(page0):
    """Pages 3-4 for Mordaunt (Map 48, event 2), in his own page's dress: the
    committee with Aldric, below his ladder; afterwards, for everybody."""
    known = {"selfSwitchValid": True, "selfSwitchCh": "A"}
    after = S.say("Mordaunt", [
        "Sir Aldric is wherever he is. He",
        "has the pin. The map is correct.",
        "That is the system."])
    after += S.narrate([
        "He has very few red pins left to move, and does not seem",
        "to know what to do with his hands."])
    return [
        _like(page0, _ald3_committee(),
              dict(known, actorValid=True, actorId=db.ALDRIC)),
        _like(page0, after,
              dict(known, switch1Valid=True, switch1Id=db.SW_ALD3_DONE)),
    ]


def great_map_pages(page0):
    """Page 2 of each cell of the great map (Map 48, events 3-10): the
    picture without the red pins, and the card where they were."""
    look = _ald3_picture() + [R.wait(20)] + S.narrate([
        "The island, in the Order's own survey, four sheets",
        "wide, with a pin for every knight in the field."])
    look += S.narrate([
        "One pin, one knight: a white head for each of them,",
        "spread thin, standing where they were put. No red ones."])
    look += S.narrate([
        "In the margin, a small card in Mordaunt's hand:",
        "   PEMBERTON-GORE. AT LARGE. PIN CARRIED."])
    look += [{"code": 235, "indent": 0, "parameters": [1]}]
    return [_like(page0, look, {"switch1Valid": True,
                                "switch1Id": db.SW_ALD3_DONE})]


def committee_pages(page0):
    """Page 2 of the committee's table (Map 48, events 11-12)."""
    card = S.narrate([
        "Two chairs and two stools, all empty, and a card",
        "on the table:",
        "   REVIEW OF PINS (PEMBERTON-GORE): CONCLUDED.",
        "   Sir A. informed. Offered the Chapter. Declined."])
    card += S.narrate([
        "Beneath it, in a smaller hand, in ink:",
        "   Beautifully. (Minuted at his request.)"])
    return [_like(page0, card, {"switch1Valid": True,
                                "switch1Id": db.SW_ALD3_DONE})]
