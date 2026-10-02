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


# ======================================================================
# ALD-1, The Errand (`QUESTS.md` E5)
# ----------------------------------------------------------------------
# He still has the letter. It has been in his tabard for nine years and is
# soft at the folds. It must go to the next village, four miles off, and he
# insists on leading, by a route of a hundred and ten miles that passes a
# coast he has been told about. The party may correct him at any point and
# should not. It is an invitation to a wedding nine years ago, which
# everybody attended anyway.
#
# * **The start is the banns** (Map 50 event 8), which have no ladder: with
#   Aldric, its own page and then INVITATIONS TO FOLLOW read over your
#   shoulder - "...I am the invitations." Out of the tabard comes the letter,
#   TO THE PARISH OF LITTLE GORE. BY HAND., his first errand, the morning he
#   rode out. It is a key item from here, so a dismissed Aldric's errand
#   waits on whoever is carrying it.
# * **The route is a choice**: follow him - the coast, the Lay-By in the
#   west, Frostwick, the Fenmarch road twice, three days, and over a rise, a
#   sandy road and a wooden house on a knoll - or tell him this is Little
#   Gore, which is shorter and a little sad. Both arrive.
# * **The delivery is Mrs Vane's** (event 3, page 3: her A, Aldric and the
#   letter). She opens an invitation to her own wedding, is delighted, and
#   puts it on the mantelpiece. The first thing he has carried in six years
#   that has got where it was going.
# * **Afterwards for everybody**: Mrs Vane's own last page plus the
#   mantelpiece, and the banns plus FOLLOWED. (P-G.)
ALD1_LETTER_ICON = 192          # the envelope


def _ald1_route():
    c = [R.fadeout_screen()]
    c += S.narrate([
        "You follow him. Down to the coast, which is lovely, and",
        "along it, which takes a day. Through a lay-by in the far",
        "west, where he is fairly sure he has been before."])
    c += S.narrate([
        "Up to Frostwick, which is cold, and down the Fenmarch road,",
        "twice, in different directions, both times on purpose.",
        "He carries the letter the whole way, in his hand."])
    c += S.narrate([
        "On the third evening you come over a rise, and there is a",
        "clearing, and a sandy road, and a wooden house on a knoll",
        "with smoke going up from it. A painted board: LITTLE GORE."])
    c += [R.fadein_screen()]
    c += S.say("Aldric", [
        "THERE. Little Gore. Told you I",
        "knew the way."])
    c += S.narrate(["It is a very good way. You would not change a mile of it."])
    return c


def _ald1_corrected():
    c = S.narrate([
        "You point at the fingerpost, which says LITTLE GORE, and",
        "at the houses, and at the banns, which say so as well."])
    c += S.say("Aldric", [
        "...Is it? Oh. Oh, good. That is a",
        "great deal shorter."])
    c += S.narrate(["He looks, for a moment, at the road to the coast."])
    c += S.say("Aldric", ["I should have liked to see",
                          "the coast."])
    return c


def _ald1_letter():
    c = S.narrate([
        "Sir Aldric reads the banns over your shoulder, and then",
        "the card under them, and goes a colour."])
    c += S.say("Aldric", ["Invitations to follow."])
    c += S.say("Aldric", ["...I am the invitations."])
    c += S.narrate([
        "He puts a hand into his tabard and brings out a letter,",
        "soft at the folds and nine years old. TO THE PARISH OF",
        "LITTLE GORE. BY HAND. P-G."])
    c += S.say("Aldric", [
        "My father gave me this the morning",
        "I rode out. Four miles to Little",
        "Gore, he said. Your first errand."])
    c += S.say("Aldric", [
        "Deliver it, and then you may go",
        "errant. I have been errant for nine",
        "years. I never delivered it."])
    c += S.say("Aldric", [
        "Little Gore! Four miles. I know the",
        "way. Down to the coast, along it,",
        "the west road, Frostwick -"])
    c += S.narrate([
        "It is about a hundred and ten miles. He has been told",
        "about the coast. You are standing in Little Gore."])
    c += [R.gain_item(db.IT_ALD1_LETTER, 1)]
    c += R.choice_block(["Follow him", "Aldric, this is Little Gore"],
                        [_ald1_route(), _ald1_corrected()])
    c += S.say("Aldric", [
        "Well. Mrs Vane's, then. The first",
        "house. One knocks, I believe."])
    return c


def banns_pages(page0):
    """Pages 2-3 of the banns (Map 50, event 8), which have no ladder: with
    Aldric, its own page and then the letter out of his tabard; afterwards,
    its own page and one line, for everybody."""
    own = page0["list"][:-1]
    nearly = S.say("Aldric", [
        "Mrs Vane's, the first house. I have",
        "it here. Nearly there."])
    aldric = own + R.if_then(R.condition_item(db.IT_ALD1_LETTER), nearly,
                             _ald1_letter())
    after = own + S.narrate([
        "Under INVITATIONS TO FOLLOW, in a fresh hand, very neat:",
        "        FOLLOWED. (P-G.)"])
    return [
        _like(page0, aldric, {"actorValid": True, "actorId": db.ALDRIC}),
        _like(page0, after, {"switch1Valid": True,
                             "switch1Id": db.SW_ALD1_DONE}),
    ]


def _ald1_delivery():
    c = S.narrate([
        "Sir Aldric takes off his helmet, which nobody has seen him",
        "do, and holds out the letter in both hands."])
    c += S.say("Aldric", [
        "Mrs Vane. For the parish of Little",
        "Gore, by hand. With the compliments",
        "of Fenmarch Hall. I am late."])
    c += S.narrate([
        "She opens it on the doorstep. Bess and Alfie and Nell",
        "come and stand round her to see."])
    c += S.narrate([
        "SIR ALDRIC PEMBERTON-GORE THE SECOND REQUESTS THE PLEASURE",
        "OF THE PARISH OF LITTLE GORE AT THE WEDDING OF HESTER",
        "PLUMB AND THOMAS VANE, AT FENMARCH."])
    c += S.say("Mrs Vane", ["...It's my wedding."])
    c += S.say("Aldric", ["It is. I do apologise. It was",
                          "my first errand."])
    c += S.say("Mrs Vane", [
        "Oh, but we all came anyway! All",
        "eleven of us. In the rain. Nobody",
        "had told us not to."])
    c += S.say("Mrs Vane", [
        "And now we're invited. Properly.",
        "It's going on the mantelpiece.",
        "Bess, fetch the good pin."])
    c += S.narrate([
        "It goes on the mantelpiece, propped against the clock,",
        "where you can see it through the window from the road."])
    c += S.narrate([
        "Sir Aldric stands on the path with his hands empty, and",
        "looks at them. It is the first thing he has carried in",
        "six years that has got where it was going."])
    c += S.say("Mrs Vane", ["You'll stop for tea."])
    c += S.say("Aldric", [
        "I should like that very much. I may",
        "not find my way out afterwards."])
    c += S.say("Mrs Vane", ["Then you'll stop for supper."])
    c += [R.gain_item(db.IT_ALD1_LETTER, -1), R.play_me("Fanfare2")]
    c += [S.trope(), R.control_switch(db.SW_ALD1_DONE, True)]
    c += S.companion_story(db.ALDRIC)
    return c


def vane_pages(page0):
    """Pages 3-4 for Mrs Vane (Map 50, event 3), in her own page's dress:
    the delivery, with Aldric and the letter, below her ladder; afterwards,
    her own last page and the mantelpiece, for everybody."""
    known = {"selfSwitchValid": True, "selfSwitchCh": "A"}
    after = page0["list"][:-1] + S.narrate([
        "Through the window behind her, on the mantelpiece, an",
        "invitation nine years late, propped against the clock."])
    return [
        _like(page0, _ald1_delivery(),
              dict(known, actorValid=True, actorId=db.ALDRIC,
                   itemValid=True, itemId=db.IT_ALD1_LETTER)),
        _like(page0, after,
              dict(known, switch1Valid=True, switch1Id=db.SW_ALD1_DONE)),
    ]
