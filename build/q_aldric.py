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
from places import (MAP_DUNNAGE, COLDBARROW_MAP_AT_LARGE, FOURTH_FOLLOWS,
                    MAP_VILLAGE, MAP_SOPPING, MAP_COLDBARROW, MAP_LITTLE_GORE,
                    MAP_WEEPING_BOTTOM)

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


# ======================================================================
# ALD-5, Pemberton-Gore the Fourth (`QUESTS.md` E6)
# ----------------------------------------------------------------------
# His nephew turns up: nineteen, magnificent, courteous, found the north gate
# unassisted on the first attempt, raised on the story of the knight who went
# out and never came back, and he wants to squire for him. The comedy is
# entirely Aldric's face; the warmth is that the lad is right.
#
# * **Decided: it needs ALD-1**, as NIX-1 needs NIX-4. The Fourth cannot come
#   to Fenmarch's door to meet him - Aldric will not go in - so the news has
#   to reach the house, and it goes the way everything between Little Gore
#   and Fenmarch goes: Tom walks it every day. Once the letter is delivered,
#   the Fourth turns up at Little Gore (Map 50, a new event), having found it
#   first time.
# * **The scene is his**, with Aldric: "UNCLE." The family story, the nine
#   pins, the gate he can find. Aldric tries to tell him he has been lost
#   for six years, mostly in Thistlewick. "I know." Grandfather said the
#   Pemberton-Gores always go the long way round, and the long way round is
#   still a way - and nobody else in the family ever went OUT; they came
#   over the wall. Three paces behind, then. One trope (the prodigy
#   successor).
# * **"A page on Aldric everywhere afterwards in which somebody is following
#   him"**: the Fourth stands a few paces off the way in at six places -
#   Thistlewick, Nether Sopping, Coldbarrow, Little Gore, Weeping Bottom and
#   Great Dunnage - on a page that needs Aldric in the party and the quest
#   done, with a line each. Without Aldric he is not there; he is at home.
# * **And then Aldric can go home**: Fenmarch's world-map door, which refuses
#   him, gains a page with him and the quest done - the Fourth finds the gate
#   first time, and Sir Aldric goes in. The Third's portrait, with the
#   flowers under it, gains a page with him standing in front of it; and the
#   Fourth's own event in the gallery its afterwards page, for everybody.
ALD5_FOLLOWING = {
    # map: what the Fourth says, three paces behind his uncle
    MAP_VILLAGE: ["Uncle says the north gate's just",
                    "over there. I found it at once.",
                    "I haven't said."],
    MAP_SOPPING: ["I'm keeping three paces behind.",
                "It's how you squire. I read it.",
                "He keeps stopping, though."],
    MAP_COLDBARROW: ["Mordaunt asked where Uncle was.",
                   "I said: here. He wrote it down",
                   "and looked so pleased."],
    MAP_LITTLE_GORE: ["Mrs Vane gave me cake. She says",
                    "the invitation's on the mantel.",
                    "I've seen it. It's lovely."],
    MAP_WEEPING_BOTTOM: ["It's very damp. Uncle says it's",
                       "bracing. I think he means it's",
                       "damp, but nicely."],
    MAP_DUNNAGE: ["Duchess knew him straight off.",
                "She's never looked at me like",
                "that. I'm working on it."],
}


def _ald5_meeting():
    c = S.narrate([
        "A young man in blue and silver comes up the sandy road at",
        "a run, with a very clean helmet under his arm, and stops",
        "dead in front of Sir Aldric."])
    c += S.say("The Fourth", ["UNCLE."])
    c += S.say("Aldric", ["...Hello. Er."])
    c += S.say("The Fourth", [
        "Pemberton-Gore. The Fourth. I was",
        "ten when you went! Tom said you'd",
        "been HERE. With the letter!"])
    c += S.say("The Fourth", [
        "Grandfather's letter. The first",
        "errand! The knight who went out and",
        "never came back. It's our best one."])
    c += S.narrate([
        "Sir Aldric's face does several things at once, none of",
        "which it has had to do before."])
    c += R.if_then(R.condition_switch(db.SW_ALD3_DONE), S.say("The Fourth", [
        "And Mordaunt says you're AT LARGE.",
        "That's a RANK. They made it up for",
        "you. On a Thursday."]), S.say("The Fourth", [
        "Nine pins, Mordaunt says. Nine!",
        "Three in one week! Nobody's ever",
        "been three places in one week."]))
    c += S.say("Aldric", ["It was a busy week."])
    c += S.say("The Fourth", [
        "I want to squire for you. I can",
        "find gates. I found ours first time.",
        "I could find you all of them."])
    c += S.say("Aldric", [
        "Lad. I ought to tell you. I have",
        "not been in the field. I have been",
        "lost. For six years."])
    c += S.say("Aldric", ["In Thistlewick. Mostly."])
    c += S.say("The Fourth", ["I know."])
    c += S.narrate(["Sir Aldric looks at him."])
    c += S.say("The Fourth", [
        "Grandfather said we always go the",
        "long way round. And the long way",
        "round is still a way."])
    c += S.say("The Fourth", [
        "And nobody else in the family ever",
        "went OUT, uncle. They all came over",
        "the wall. You went OUT."])
    c += S.narrate([
        "It is not how Sir Aldric would describe the last six",
        "years. It is, he finds, standing in the road, true."])
    c += S.say("Aldric", [
        "...Three paces behind, then. And",
        "you'll tell me if I'm facing the",
        "wrong way."])
    c += S.say("The Fourth", ["You always are, uncle.",
                              "It's on the arms."])
    c += [R.play_me("Fanfare1")]
    c += S.narrate(["The Fourth takes up his place, three paces behind, and",
                    "polishes his helmet, which does not need it."])
    c += [S.trope(), R.control_switch(db.SW_ALD5_DONE, True)]
    c += S.companion_story(db.ALDRIC)
    return c


def fourth_meeting_event(event_id, x, y, follows):
    """Map 50: the Fourth, turned up at Little Gore once the letter is
    delivered. Nothing before; with Aldric, the meeting; without, waiting;
    afterwards, nothing without Aldric and following with him."""
    img = R.image(*S.FACES["The Fourth"], direction=8)
    blank = R.page([], img=R.image(""), trigger=0, priority=0, through=True)
    waiting = S.say("The Fourth", [
        "Is my uncle with you? Sir Aldric?",
        "Tom said he came HERE. Four miles!",
        "I found it first time."])
    meet = R.if_then(R.condition_actor_in_party(db.ALDRIC), _ald5_meeting(),
                     waiting)
    done = {"switch1Valid": True, "switch1Id": db.SW_ALD5_DONE}
    return R.event(event_id, "The Fourth", x, y, [
        copy.deepcopy(blank),
        R.page(meet, img=img, trigger=0, priority=1, conditions={
            "switch1Valid": True, "switch1Id": db.SW_ALD1_DONE}),
        copy.deepcopy(dict(blank, conditions=R.page([], conditions=done)[
            "conditions"])),
        R.page(_ald5_follow(follows), img=img, trigger=0, priority=1,
               conditions=dict(R.page([], conditions=done)["conditions"],
                               actorValid=True, actorId=db.ALDRIC)),
    ])


def _ald5_follow(where):
    c = S.narrate([
        "Three paces behind Sir Aldric, as near as he can manage,",
        "stands the Fourth, pretending to look at something else."])
    c += S.say("The Fourth", ALD5_FOLLOWING[where])
    return c


def following_event(event_id, x, y, where):
    """The Fourth, three paces behind his uncle, at one of the places Aldric
    goes: nothing at all unless Aldric is in the party and ALD-5 is done.
    `where` is a map id, a key of `ALD5_FOLLOWING`."""
    blank = R.page([], img=R.image(""), trigger=0, priority=0, through=True)
    page = R.page(_ald5_follow(where),
                  img=R.image(*S.FACES["The Fourth"], direction=2),
                  trigger=0, priority=1, conditions={
                      "switch1Valid": True, "switch1Id": db.SW_ALD5_DONE,
                      "actorValid": True, "actorId": db.ALDRIC})
    return R.event(event_id, "The Fourth (following)", x, y, [blank, page])


def fenmarch_door_pages(page0):
    """Page 4 of Fenmarch's world-map door (two cells): with Aldric and his
    squire, the Fourth finds the gate first time, and Sir Aldric goes home.
    `page0` is the door's own first page, whose transfer is the way in."""
    home = S.narrate([
        "A grey house behind a low wall, with a moat all the way",
        "round it. Sir Aldric has stopped in the road."])
    home += S.say("The Fourth", ["Gate's just here, uncle.",
                                 "This way."])
    home += S.narrate([
        "He finds it first time. Sir Aldric looks at it for a long",
        "moment, and at the house, and at his nephew, and does not",
        "look the other way."])
    home += S.say("Aldric", ["...Shall we go in?"])
    way_in = [c for c in page0["list"] if c["code"] == 201][0]
    home += [dict(copy.deepcopy(way_in), indent=0)]
    return [_like(page0, home, {
        "switch1Valid": True, "switch1Id": db.SW_ALD5_DONE,
        "actorValid": True, "actorId": db.ALDRIC})]


def third_portrait_pages(page0):
    """Page 2 of the Third's portrait (Map 57, event 14): its own page, and
    Sir Aldric in front of it."""
    c = page0["list"][:-1] + S.narrate([
        "Sir Aldric stands in front of it for some time: himself,",
        "from behind, walking out of the picture at a good pace."])
    c += S.say("Aldric", ["I was going to come back.",
                          "...I have, rather."])
    c += S.narrate([
        "Mrs Puddifoot changes the flowers anyway, because it is",
        "the morning, and nobody tells her not to."])
    return [_like(page0, c, {
        "switch1Valid": True, "switch1Id": db.SW_ALD5_DONE,
        "actorValid": True, "actorId": db.ALDRIC})]


def fourth_pages(page0):
    """Page 3 for the Fourth at home (Map 57, event 2): his own last page and
    one line, for everybody, once he is a squire."""
    after = page0["list"][:-1] + S.narrate([
        "He is a squire now. When his uncle is out, so is he, three",
        "paces behind; when he is home, he keeps the helmet clean."])
    return [_like(page0, after, {
        "selfSwitchValid": True, "selfSwitchCh": "A",
        "switch1Valid": True, "switch1Id": db.SW_ALD5_DONE})]


def with_follower(events, map_id):
    """`events` with the Fourth appended at the next id, at
    `places.FOURTH_FOLLOWS[map_id]`: at Little Gore the event he turns up as,
    everywhere else the one that follows Aldric. One line in a place module:
    `m["events"] = [None] + q_aldric.with_follower(x_events(), MAP_X)`."""
    x, y = FOURTH_FOLLOWS[map_id]
    make = fourth_meeting_event if map_id == MAP_LITTLE_GORE else following_event
    return list(events) + [make(len(events) + 1, x, y, map_id)]


# ======================================================================
# ALD-2, The Vigil (`QUESTS.md` E7)
# ----------------------------------------------------------------------
# A knight is confirmed by keeping vigil in a chapel. He has kept eleven,
# every one in the wrong chapel, one of them a barn. The party keeps the
# twelfth with him, in the right one, and he may not move or speak until it
# is light - and things come.
#
# * **The right chapel is Weeping Bottom's**, the Order's chapel for the
#   west, which the Sisters lend it, and **Sir Hamo Tench is the sponsor**:
#   a knight of the Order, in the field in the ward for fourteen years. The
#   start is his second look with Aldric (Map 55 event 4, below his one-self-
#   switch ladder). The symposium has the chapel at three in the afternoon
#   and the vigil has it at night, so it needs nothing of MER-1.
# * **The shield has been waiting over the chapel door for thirty years**,
#   sent for his first vigil, which he kept somewhere else. The Sisters took
#   it for a pun about vigilance. Regardant means looking back, to see who is
#   behind you: that is the whole of the Order, and he has been facing his
#   friends, not the wrong way. It is his gear (`QUESTS.md` 0.5).
# * **The vigil is a fight** (`db.build_vigil`): he cannot act and draws
#   everything; the party keeps him up until dawn. Broken if he falls, and
#   lost if everybody does - either way it waits, and Sir Hamo with it.
# * **Afterwards for everybody**: Sir Hamo's last page and his letter to
#   Coldbarrow; the chapel's own page and the pale patch over its door.
ALD2_BATTLEBACK = ("Temple", "Temple")


def _ald2_offer():
    c = S.narrate([
        "He looks at Sir Aldric for a while, the way one knight",
        "looks at another's spurs."])
    c += S.say("Sir Hamo", ["Pemberton-Gore. Were you",
                            "ever confirmed? The vigil, and so on."])
    c += S.say("Aldric", ["Eleven times. None of them",
                          "took."])
    c += S.say("Aldric", ["Wrong chapel, every one.",
                          "Coldbarrow, twice. It says CHAPTER",
                          "HOUSE on the door. I thought it was",
                          "being modest."])
    c += S.say("Aldric", ["And one was a barn. It had",
                          "a weathercock. I was very nearly",
                          "sure."])
    c += S.say("Sir Hamo", ["The Order's chapel for the",
                            "west is across the yard. Always has",
                            "been. The Sisters lend it us."])
    c += S.say("Sir Hamo", ["There's a shield over the",
                            "door, inside. Thirty years it's hung",
                            "there. Nobody's come for it."])
    c += S.narrate([
        "A knight on it, in a field, looking back over his",
        "shoulder. The Sisters have always taken it for a pun,",
        "about vigilance."])
    c += S.say("Aldric", ["...That's mine."])
    c += S.say("Sir Hamo", ["I'll stand sponsor. Dusk",
                            "to dawn. You don't move, and you",
                            "don't speak. Your friends keep the",
                            "watch."])
    c += S.say("Sir Hamo", ["Things come, at night, at",
                            "Weeping Bottom. They always have.",
                            "Tonight?"])
    return c


def _ald2_into_battle():
    """Sir Aldric at the front, if four others are; then the chapel's
    battleback, the fight, and the map's own battleback back."""
    front = R.script([
        "const a = $gameActors.actor(%d);" % db.ALDRIC,
        "if (!$gameParty.battleMembers().includes(a)) {",
        "  const all = $gameParty.allMembers();",
        "  $gameParty.swapOrder(all.indexOf(a),",
        "    $gameParty.maxBattleMembers() - 1);",
        "}",
    ])
    return front + [{"code": 283, "indent": 0,
                     "parameters": list(ALD2_BATTLEBACK)}]


def _ald2_confirmed():
    c = S.narrate([
        "Morning. Sir Hamo gets up out of the chair at the back,",
        "a joint at a time, and takes the shield down from over",
        "the door."])
    c += S.say("Sir Hamo", ["Sir Aldric Pemberton-Gore.",
                            "Vigil kept, in the right chapel,",
                            "dusk to dawn. Confirmed."])
    c += S.say("Sir Hamo", ["Thirty years late. The",
                            "Order's never minded late. It minds",
                            "wrong chapels."])
    c += S.narrate([
        "He holds it out. Argent, a knight rampant regardant: a",
        "knight in a field, looking back over his shoulder."])
    c += S.say("Aldric", ["They told me it was a pun.",
                          "About vigilance."])
    c += S.say("Sir Hamo", ["It's not. He's looking",
                            "back to see who's behind him. That's",
                            "the whole of the Order."])
    c += S.say("Sir Hamo", ["You don't lead. You look",
                            "round, and you see who's bleeding,",
                            "and you go and stand in front of",
                            "them."])
    c += S.say("Aldric", ["...I always thought I was",
                          "facing the wrong way."])
    c += S.say("Sir Hamo", ["You were facing your",
                            "friends."])
    c += R.if_then(R.condition_switch(db.SW_ALD5_DONE), S.narrate([
        "Outside, the Fourth has kept the door all night, three",
        "paces from it. Facing the right way, he points out."]))
    c += [R.gain_armor(db.AR_REGARDANT, 1), R.play_me("Fanfare2")]
    c += S.narrate([
        "Sir Aldric takes the shield. He has not said anything",
        "for eleven hours, and he does not say anything now."])
    c += [S.trope(), R.control_switch(db.SW_ALD2_DONE, True)]
    c += S.companion_story(db.ALDRIC)
    return c


def _ald2_again():
    return S.say("Sir Hamo", ["Twelfth's not done, then.",
                              "Took me four goes. When you're",
                              "ready. The chapel's not going",
                              "anywhere. Nor am I."])


def _ald2_broken():
    return S.narrate([
        "Sir Hamo helps him up. Nobody says anything about it,",
        "least of all Sir Aldric."]) + _ald2_again()


def _ald2_lost():
    return S.narrate([
        "The Sisters find the lot of you on the chapel floor at",
        "six, and put you to bed on the line, so that both halves",
        "can treat you."]) + _ald2_again()


def _ald2_vigil():
    c = [R.fadeout_screen()]
    c += S.narrate([
        "Dusk. Leek soup first, from both halves of the ward; it",
        "is the rule. Then Sir Hamo unlocks the chapel with a key",
        "he keeps on a string, under the nightshirt."])
    c += [R.recover_all(0)]
    c += S.narrate([
        "The symposium's chairs stand in their two rows, facing",
        "one another, and watch. Over the door hangs the shield,",
        "the knight on it looking back."])
    c += S.say("Sir Hamo", ["From now. Not a word,",
                            "Pemberton-Gore."])
    c += S.narrate([
        "He does not say one. Sir Hamo sits down at the back and",
        "coughs, very quietly, until midnight. Then something",
        "comes in under the door."])
    c += _ald2_into_battle()
    c += [R.battle(db.TR_VIGIL, can_escape=False, can_lose=True)]
    bodies = [(601, _ald2_confirmed()),
              (602, _ald2_broken() + [R.recover_all(0)]),
              (603, _ald2_lost() + [R.recover_all(0)])]
    for code, body in bodies:
        c += [{"code": code, "indent": 0, "parameters": []}]
        c += R.shift(body, 1)
        c += [{"code": 0, "indent": 1, "parameters": []}]
    c += [{"code": 604, "indent": 0, "parameters": []}]
    c += [{"code": 283, "indent": 0, "parameters": ["", ""]},
          R.fadein_screen()]
    return c


def hamo_pages(last):
    """Pages 3-4 for Sir Hamo (Map 55, event 4), in his own last page's
    dress: with Aldric, his last page and then the vigil, below his ladder;
    afterwards, his last page and the letter to Coldbarrow, for everybody."""
    known = {"selfSwitchValid": True, "selfSwitchCh": "A"}
    own = last["list"][:-1]
    later = S.say("Sir Hamo", ["Thirty years. It'll keep",
                               "till you're ready. So will I."])
    ask = own + _ald2_offer() + R.choice_block(
        ["Tonight", "Not yet"], [_ald2_vigil(), later])
    after = own + S.narrate([
        "On the blanket, a letter to Coldbarrow, nearly done:",
        "   IN THE FIELD. CONFIRMED: ONE. (PEMBERTON-GORE.)",
        "   FIRST IN THIRTY YEARS."])
    after += R.if_then(R.condition_actor_in_party(db.ALDRIC),
                       S.say("Sir Hamo", ["Anybody behind you, Sir",
                                          "Aldric?"]) +
                       S.say("Aldric", ["Always."]))
    return [
        _like(last, ask, dict(known, actorValid=True, actorId=db.ALDRIC)),
        _like(last, after,
              dict(known, switch1Valid=True, switch1Id=db.SW_ALD2_DONE)),
    ]


def chapel_pages(page0):
    """Page 2 of Weeping Bottom's chapel (Map 54, event 5), which has no
    ladder: its own page, and the patch over the door, for everybody."""
    after = page0["list"][:-1] + S.narrate([
        "Over the door inside, a paler patch on the wall, the",
        "shape of a shield, where one hung for thirty years."])
    return [_like(page0, after, {"switch1Valid": True,
                                 "switch1Id": db.SW_ALD2_DONE})]

