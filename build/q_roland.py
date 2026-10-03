"""Roland Fairweather's companion quests - `COMPANIONS.md`, his section, and
`QUESTS.md` for the order they are built in.

Nothing here draws a map, and this module imports no place module: the place
modules call in here for pages.

ROL-4, The Maker's Mark (`QUESTS.md` A5)
----------------------------------------
The sword he leaves you at the door has a mark on it. Hob knows the mark. It
is his aunt's. It was made at the forge in Thistlewick forty years ago, and
sold, and travelled, and came back.

* **It happens at the anvil in Hob's smithy** - Map 6, event 4, the hammer
  called Beatrice. One page, no switches, so the pages below it wait on no
  ladder. The forge the sword was made at is the right place to look at it.
* **Before the door.** Roland never *equips* Fairweather's Own - he wears his
  practice sword and carries the other one, and `journey.roland_departure`
  hands it over from what he is carrying. So the look is Roland's page, with
  him taking it out to show; Hob is a branch inside it (one actor to a page).
* **Nobody explains the hammer** (`COMPANIONS.md`, twice). Hob says his aunt
  made the sword and that she did good work. Beatrice says nothing. What the
  player makes of a hammer with a name on it is theirs.
* **The refit is after he has gone**, on Hob's page: the blade on an ash
  haft, as an axe, because Hob's class takes axes and not swords, and a class
  is published. `WP_REHAFTED` is an axe nobody else can hold. The sword is
  found carried *or* equipped - Bram can wield it - so the check and the
  taking are both script, with `includeEquip`.
"""
import copy

import db
import places
import rmmzdata as R
import story as S

HAS_SWORD = "$gameParty.hasItem($dataWeapons[%d], true)" % db.WP_FAIRWEATHER


def _like(page0, cmds, conditions):
    """A page in exactly another page's dress, with its own commands and
    conditions."""
    shaped = R.page(cmds, conditions=conditions)
    page = copy.deepcopy(page0)
    page["list"] = shaped["list"]
    page["conditions"] = shaped["conditions"]
    return page


def _the_mark():
    """Roland and Hob at the anvil. The whole of ROL-4 that matters."""
    c = S.narrate([
        "Roland stops at the anvil. He has been quiet since",
        "you came in."])
    c += S.say("Roland", [
        "Hob. Would you look at something",
        "for me? Professionally."])
    c += S.narrate([
        "He unbuckles the sword he carries and never uses -",
        "not the one on his hip, the other one - and lays it",
        "across the anvil."])
    c += S.say("Roland", [
        "I leave it at a door. Every time.",
        "And every time, somehow, it finds",
        "its way back to me."])
    c += S.say("Roland", [
        "I've never known who made it.",
        "There's a mark by the hilt."])
    c += S.narrate([
        "Hob picks it up. He turns it to the light from the",
        "forge, and looks at the mark by the hilt, and does",
        "not say anything for a while."])
    c += S.narrate([
        "It is a small mark, struck with a punch: a B and a G",
        "run together, the way somebody signs a thing they",
        "are not ashamed of."])
    c += [R.wait(40)]
    c += S.say("Hob", ["That's my aunt's."])
    c += S.say("Hob", [
        "She made this here. On this.",
        "Forty years back, near enough.",
        "Sold it to a man going south."])
    c += S.narrate([
        "Roland looks at the sword, and at the forge, and at",
        "Hob, and for once he does not say anything clever."])
    c += [R.wait(30)]
    c += S.say("Hob", ["She did good work."])
    c += [R.wait(40)]
    c += S.narrate([
        "Beatrice, on the anvil, for once, says nothing at",
        "all."])
    c += S.narrate([
        "Roland buckles the sword on again, carefully, the",
        "way you would carry a thing back to where it lives."])
    c += [R.control_switch(db.SW_ROL4_SEEN, True)]
    c += S.companion_story(db.ROLAND)
    return c


def anvil_pages(page0):
    """Pages 2 and 3 of Beatrice (Map 6, event 4). `page0` is the prop's own
    page: a party without Roland or Hob sees only that, and either of them
    alone still reads it first where nothing else is happening."""
    looked = page0["list"][:-1]

    # -- 2: Roland, before the door. Hob is a branch.
    alone = looked + S.narrate([
        "Roland looks at the anvil for a moment, the way a",
        "swordsman looks at any forge he is standing in, and",
        "his hand goes to the sword he never uses."])
    again = S.say("Hob", [
        "Mind the edge on that. She'd",
        "want it minded."])
    with_hob = R.if_then(R.condition_switch(db.SW_ROL4_SEEN), again,
                         _the_mark())
    roland = R.if_then(R.condition_actor_in_party(db.HOB), with_hob, alone)

    # -- 3: Hob, after the door, with the sword.
    refit = S.narrate([
        "He takes the grip off. He fits the tang to a long",
        "ash haft out of the rack, and wedges it, and pins it.",
        "It takes the whole of an afternoon, and he does not",
        "talk to anybody, including the hammers."])
    refit += [R.play_se("Hammer"), R.wait(30), R.play_se("Hammer"),
              R.wait(30), R.play_se("Hammer", pitch=90), R.wait(40)]
    refit += R.script(["$gameParty.loseItem($dataWeapons[%d], 1, true);"
                       % db.WP_FAIRWEATHER])
    refit += [R.gain_weapon(db.WP_REHAFTED, 1), R.play_me("Item"),
              R.control_switch(db.SW_ROL4_REFIT, True)]
    refit += S.got(["Got \\I[99]\\C[3]Fairweather's Own, Rehafted\\C[0].",
                    "Her blade. His haft. Hob's to swing."])
    refit += S.say("Hob", ["There. Still hers. Handle's mine."])
    keep = S.say("Hob", [
        "Fair enough. It's a good sword",
        "as it is. She'd say so."])

    ask = S.narrate([
        "Hob stands at the anvil with Roland's sword across",
        "his two hands, which is where it started."])
    ask += S.say("Hob", [
        "He said take it up there. It's",
        "never been in a last room."])
    ask += S.say("Hob", [
        "I'm not a sword man. But it's",
        "hers, and it should go up with",
        "one of us."])
    ask += R.choice_block(["Let Hob refit it", "Leave it a sword"],
                          [refit, keep], cancel=1)

    swung = S.say("Hob", [
        "It swings right. She always made",
        "them to swing right."])
    no_sword = looked + S.say("Hob", [
        "He'll have left you that sword.",
        "Bring it here when you're ready."])

    hob = R.if_then(
        R.condition_switch(db.SW_ROL4_REFIT), swung,
        R.if_then(R.condition_script(HAS_SWORD), ask, no_sword))

    return [
        _like(page0, roland, {"actorValid": True, "actorId": db.ROLAND}),
        _like(page0, hob, {"actorValid": True, "actorId": db.HOB,
                           "switch1Valid": True,
                           "switch1Id": db.SW_ROLAND_GONE,
                           "switch2Valid": True,
                           "switch2Id": db.SW_ROL4_SEEN}),
    ]


# ======================================================================
# ROL-3, The Alumni (`QUESTS.md` A14)
# ----------------------------------------------------------------------
# Eleven parties. Every one of them finished its quest without him, all of
# them say so warmly, and every one of them thinks of him as *their* Roland
# and is slightly hurt to find that there are ten others. It is a wholly
# happy room full of people quietly working the same thing out, and it
# resolves into a toast.
#
# * **The dinner is a state of the Slain Wyvern** (Map 14): eleven new
#   events, shown only while `SW_ROL3_DINNER` is on, stood about the room at
#   capacity. None of them is an existing NPC - the room's own regulars keep
#   their ladders - and none of them can be: Roland has been at this "since
#   I was eleven" (his recruit page) and he is thirty-four, so his first
#   party is 1977, after the Forty-Fourth and the Forty-Sixth.
# * **It starts on Dorcas's Board** (event 19), below its terminal self
#   switch A, with Roland: a card for tonight. Before the tower door,
#   necessarily - he has to be in the party.
# * **Each of the eleven counts once** into `VAR_ROL3_HEARD`, on a self switch
#   of their own; the toast is Dame Florence's, with Roland, once all eleven
#   have been heard. A Roland sent home leaves the dinner waiting.
ALUMNI = [
    # (key, event name, speaker, (sheet, index) or None, cell, facing, lines)
    ("florence", "Dame Florence Ickworth (the Wyrm of Ickworth)",
     "Dame Florence", None, (11, 10), 2, [
         ["The Wyrm of Ickworth,",
          "'seventy-seven. He was my page. Eleven",
          "years old, and he could already disarm",
          "me."],
         ["He left at the wyrm's door.",
          "They'd sent for him. We did the wyrm",
          "ourselves. I organised this. I thought",
          "there might be three of us."]]),
    ("anselm", "Brother Anselm (the Seven Bells)", "Brother Anselm", None,
     (3, 10), 6, [
         ["The Pilgrimage of the Seven",
          "Bells. He rang the first six with us.",
          "We rang the seventh without him."],
         ["I had thought we were his only",
          "pilgrimage. He has been very discreet."]]),
    ("mags", "Mags Turvey (the Second Siege of Wenlow)", "Mags", None,
     (6, 5), 2, [
         ["Second Siege of Wenlow. I fed him a",
          "fortnight on the walls. Best appetite I",
          "ever cooked for. Our Roland."],
         ["...That one over there's calling him",
          "'our Roland' and all. Cheek."]]),
    ("pim", "Pim Corrow (the Lost Heir of Corrow)", "Pim", None,
     (15, 10), 4, [
         ["I'm the Lost Heir of Corrow. He found",
          "me. Then he had to go, and I found",
          "the rest of it myself."],
         ["He said I was the bravest boy he'd",
          "ever met. ...Did he say that to him?"]]),
    ("odile", "Captain Odile Marchbank (the Ninth Lancers)", "Odile", None,
     (22, 10), 4, [
         ["The Ninth Lancers. He had the left at",
          "Haddow Ford, and drilled us, and went.",
          "We took the Ford without him."],
         ["He gave me his whetstone when he left.",
          "The man by the door has one exactly",
          "like it."]]),
    ("jory", "Old Jory (the Last Survey)", "Old Jory", None,
     (5, 12), 6, [
         ["The Cartographers' Last Survey. He",
          "walked every mile of it but the last.",
          "I drew that one in from his say-so."],
         ["I've a map of him going. Eleven of",
          "them, it turns out. Same road."]]),
    ("hettie", "Hettie Brack (the Goblin King's Riddles)", "Hettie",
     ("People1", 1), (10, 5), 2, [
         ["The Goblin King's Riddles. He got",
          "every one bar the last. I got the last.",
          "The answer was 'a door'."]]),
    ("tobin", "Lord Tobin Fairley-Vane (the Usurper of Hask)", "Lord Tobin",
     ("People3", 2), (22, 5), 4, [
         ["He held the gate at Hask. Then a",
          "letter came. We took the throne room",
          "without him. It was very good of us."]]),
    ("ned", "Ned Scarrow (the Drowned Bell)", "Ned", ("People1", 0),
     (7, 16), 6, [
         ["The Drowned Bell. He dived for it",
          "eleven times. The twelfth was me.",
          "Our Roland, the whole crew calls him."]]),
    ("saul", "Saul Pennock (the Reckoning at Pennock's Cove)", "Saul",
     ("People2", 4), (17, 16), 4, [
         ["He settled the Reckoning at Pennock's",
          "Cove, all but the last of it. Said",
          "he'd never had a better crew. Hm."]]),
    ("royce", "Major Royce (the Glass Fort)", "Major Royce",
     ("People4", 6), (20, 12), 4, [
         ["The Glass Fort. He walked us",
          "up to the last gate, and shook every",
          "hand, and went. We were his best, he",
          "said."]]),
]
ROL3_FACES = {"florence": ("Gen_People12", 1), "anselm": ("Gen_People12", 2),
              "mags": ("Gen_People12", 3), "pim": ("Gen_People12", 4),
              "odile": ("Gen_People12", 5), "jory": ("Gen_People12", 6)}
ROL3_GIFTS = [(db.IT_POTION, 2), (db.IT_HI_POTION, 2), (db.IT_TONIC, 2),
              (db.IT_ETHER, 2), (db.IT_FEATHER, 1), (db.IT_ANTIDOTE, 1),
              (db.IT_SMELLING_SALTS, 1)]
assert sum(n for _, n in ROL3_GIFTS) == len(ALUMNI) == 11


def _rol3_card():
    c = S.narrate([
        "Pinned to the board, over the room list, a card in a",
        "good square hand:"])
    c += S.narrate([
        "  THE FAIRWEATHER ALUMNI. DINNER, TONIGHT,",
        "  THE SLAIN WYVERN. ALL PARTIES WELCOME.",
        "  - F. ICKWORTH (DAME), WHO WAS FIRST."])
    c += S.say("Roland", ["Oh no."])
    c += S.say("Roland", ["...Oh, how lovely. Oh no."])
    c += [S.trope(), R.control_switch(db.SW_ROL3_DINNER, True)]
    return c


def board_pages(terminal):
    """Dorcas's Board (Map 14, event 19), below its terminal self switch A:
    the card, with Roland; and afterwards, for everybody."""
    card = R.page(R.if_then(R.condition_switch(db.SW_ROL3_DINNER),
                            S.narrate(["The card for tonight. They are",
                                       "all here."]),
                            _rol3_card()),
                  conditions={"selfSwitchValid": True, "selfSwitchCh": "A",
                              "actorValid": True, "actorId": db.ROLAND})
    after = copy.deepcopy(terminal)
    after["list"] = after["list"][:-1] + S.narrate([
        "Pinned beside it, a dinner card signed eleven times,",
        "with a ring on it from somebody's glass."]) + after["list"][-1:]
    after["conditions"] = R.page([], conditions={
        "switch1Valid": True, "switch1Id": db.SW_ROL3_DONE})["conditions"]
    return [dict(copy.deepcopy(terminal), list=card["list"],
                 conditions=card["conditions"]), after]


def _rol3_toast():
    c = S.narrate([
        "By the end of the evening the whole room has worked",
        "it out, one table at a time, and has not said so."])
    c += S.narrate([
        "Eleven parties. Eleven last doors. Every one of them",
        "finished without him, and every one of them thought,",
        "until about an hour ago, that he was theirs."])
    c += S.narrate(["Dame Florence stands up."])
    c += S.say("Dame Florence", ["Roland. We finished. Every",
                                 "one of us in this room finished."])
    c += S.say("Dame Florence", ["We finished because you got",
                                 "us to the door, and taught us what",
                                 "to do on the other side of it."])
    c += S.say("Roland", ["I'm sorry I was never -"])
    c += S.say("Dame Florence", ["Don't."])
    c += S.narrate(["She raises her glass. The room raises eleven."])
    c += S.say("Dame Florence", ["To Roland Fairweather.",
                                 "Who got us all to the door."])
    c += [R.play_se("Applause1", volume=60)]
    c += S.narrate(["'To Roland,' says the Slain Wyvern, at capacity,",
                    "and nobody says anything else at all."])
    c += [R.wait(40)]
    c += S.say("Roland", ["...Thank you. All of you.",
                          "Every one."])
    c += S.narrate([
        "Then there are presents: eleven small things, pressed",
        "into the party's hands on the way out, because a party",
        "that is still going needs things. A whetstone. A twist",
        "of tea. A pot of dripping. A map with one mile in pencil."])
    for item, n in ROL3_GIFTS:
        c += [R.gain_item(item, n)]
    c += [R.play_me("Item")]
    c += S.got(["Got eleven small gifts: Potions, Hi-Potions, Tonics,",
                "Ethers, a Feather, an Antidote and Smelling Salts."])
    c += [R.control_switch(db.SW_ROL3_DINNER, False),
          R.control_switch(db.SW_ROL3_DONE, True)]
    c += S.companion_story(db.ROLAND)
    return c


def alumni_events(base_id):
    """The eleven, about the Slain Wyvern (Map 14), while the dinner is on.
    Each counts once into `VAR_ROL3_HEARD`; Dame Florence has the toast."""
    dinner = {"switch1Valid": True, "switch1Id": db.SW_ROL3_DINNER}
    nothing = R.page([], img=R.image(""), priority=0, through=True)
    evs = []
    for n, (key, name, speaker, stock, (x, y), d, lines) in enumerate(ALUMNI):
        sheet, index = stock or ROL3_FACES[key]
        img = R.image(sheet, index, direction=d)
        talk = []
        for window in lines:
            talk += S.say(speaker, window)
        talk += R.if_then(R.condition_self_switch("A", False), [
            R.control_variable_add(db.VAR_ROL3_HEARD, 1),
            R.self_switch("A", True)])
        pages = [nothing, R.page(talk, img=img, direction_fix=True,
                                 conditions=dinner)]
        if key == "florence":
            go_round = talk + R.if_then(
                R.condition_variable(db.VAR_ROL3_HEARD, len(ALUMNI), 4),
                S.say(speaker, ["Go round. Say hello.",
                                "Everybody's here."]))
            pages[1] = R.page(go_round, img=img, direction_fix=True,
                              conditions=dinner)
            pages.append(R.page(_rol3_toast(), img=img, direction_fix=True,
                                conditions=dict(
                                    dinner, variableValid=True,
                                    variableId=db.VAR_ROL3_HEARD,
                                    variableValue=len(ALUMNI),
                                    actorValid=True, actorId=db.ROLAND)))
        evs.append(R.event(base_id + n, name, x, y, pages))
    return evs


# ======================================================================
# ROL-1, The Appointment (`QUESTS.md` B7)
# ----------------------------------------------------------------------
# Follow him. He is embarrassed, and permits it. The appointment is a review
# meeting, in a room, with an agenda, at which four people confirm that his
# prophecy is still not ready, note his continued availability, and thank him
# for his patience. It takes eleven minutes. He has attended a hundred and
# forty of them. Nobody remarks on what it resembles, and nor does this file.
#
# * **The summons is Mrs Dewhirst's** (Map 65 event 2), below her ladder, with
#   Roland: the snug is booked in his name, the usual. The page is her own
#   last page with the summons in front of it, so the inn is still the inn.
#   It turns `SW_ROL1_ON` (ends) on, which seats the Convenor and three
#   fellows at the Bell's west table (events 11-14), empty before and after.
# * **The meeting is the Convenor's**, with Roland. The minutes are a key
#   item, and Roland hands them over: he has a drawer of them.
# * **Before the tower door**, necessarily: everything needs Roland, and he
#   leaves at the door. Nothing here keeps him.
MINUTES_ICON = 193
# Where they sit, round the table at (4, 8) and its two stools.
ROL1_SEATS = [(11, "The Convenor", (4, 7), 2), (12, "Fellow Grice", (5, 7), 2),
              (13, "Fellow Amory", (3, 8), 6), (14, "Fellow Blunt", (6, 8), 4)]


def _rol1_summons():
    c = S.say("Mrs Dewhirst", ["Mr Fairweather! The",
                               "snug's booked in your name, love. The",
                               "usual. They're just sitting down."])
    c += S.narrate([
        "Roland goes, very slightly, pink, which you would not",
        "have thought was possible."])
    c += S.say("Roland", ["Ah. Yes. Thank you, Mrs Dewhirst."])
    c += S.say("Roland", ["It's nothing. A standing appointment.",
                          "Eleven minutes. You needn't -"])
    c += S.narrate(["You say that you will come."])
    c += S.say("Roland", ["...Yes. All right. I suppose you'd",
                          "better. Don't say anything."])
    c += [R.control_switch(db.SW_ROL1_ON, True)]
    return c


def dewhirst_page(last):
    """Mrs Dewhirst (Map 65, event 2) with Roland: the summons, once, in
    front of her own last page."""
    first = R.if_then(R.condition_switch(db.SW_ROL1_ON), [],
                      R.if_then(R.condition_switch(db.SW_ROL1_DONE), [],
                                _rol1_summons()))
    page = copy.deepcopy(last)
    page["list"] = first + page["list"]
    page["conditions"] = R.page([], conditions={
        "selfSwitchValid": True, "selfSwitchCh": "A",
        "actorValid": True, "actorId": db.ROLAND})["conditions"]
    return page


def _rol1_meeting():
    c = S.narrate([
        "The snug is the corner table, with a card on it that",
        "says RESERVED. Four people sit round it, with papers,",
        "and stand up when Roland arrives, and sit down again."])
    c += S.say("The Convenor", ["Mr Fairweather. Good.",
                                "We're quorate. The hundred and",
                                "forty-first meeting."])
    c += S.say("The Convenor", ["Item one. Apologies."])
    c += S.say("Fellow Grice", ["The sorcerer sends his",
                                "apologies."])
    c += S.say("The Convenor", ["Noted. Item two. The",
                                "minutes of the hundred and fortieth."])
    c += S.say("Fellow Amory", ["Agreed."])
    c += S.say("The Convenor", ["Item three. Readiness.",
                                "The stone?"])
    c += S.say("Fellow Blunt", ["Not ready."])
    c += S.say("The Convenor", ["The sword?"])
    c += S.say("Fellow Blunt", ["In the stone."])
    c += S.say("The Convenor", ["The sorcerer?"])
    c += S.say("Fellow Grice", ["Sends his apologies."])
    c += S.say("The Convenor", ["The lineage?"])
    c += S.say("Roland", ["Present."])
    c += S.narrate([
        "Fellow Amory writes PRESENT in the minutes, and underlines",
        "it, and then, after some thought, underlines it again."])
    c += S.say("The Convenor", ["Item four. The",
                                "continued availability of the asset."])
    c += S.say("Roland", ["Available."])
    c += S.say("The Convenor", ["Noted, with thanks.",
                                "Item five. Any other business?"])
    c += [R.wait(60)]
    c += S.say("The Convenor", ["Then thank you, Mr",
                                "Fairweather, for your continued",
                                "patience. Until the next door."])
    c += S.narrate([
        "They gather their papers, and shake his hand, all four,",
        "and go out into the street together. It has taken",
        "eleven minutes. Roland sits on at the table a while."])
    c += S.say("Roland", ["A hundred and forty-one."])
    c += S.narrate([
        "He folds the minutes once, neatly, and holds them out",
        "to you."])
    c += S.say("Roland", ["You may as well have these. I've a",
                          "drawer of them."])
    c += [S.trope(), R.gain_item(db.IT_MINUTES, 1), R.play_me("Item"),
          R.control_switch(db.SW_ROL1_ON, False),
          R.control_switch(db.SW_ROL1_DONE, True)]
    c += S.got(["Got \\I[%d]\\C[3]The Minutes (141st)\\C[0]." % MINUTES_ICON])
    c += S.companion_story(db.ROLAND)
    return c


_ROL1_WAIT = {
    "The Convenor": ["Mr Fairweather is expected.",
                     "We can't start without the asset."],
    "Fellow Grice": ["The sorcerer is not coming.",
                     "He never comes. It's minuted."],
    "Fellow Amory": ["I take the minutes. I have taken",
                     "all of them."],
    "Fellow Blunt": ["The stone is not ready. I check",
                     "the stone."],
}


def meeting_events():
    """The Convenor and three fellows (Map 65, events 11-14): at the Bell's
    west table while the meeting is on, and nowhere before or after. The
    Convenor holds the meeting, with Roland; without him, everybody waits."""
    on = {"switch1Valid": True, "switch1Id": db.SW_ROL1_ON}
    gone = {"switch1Valid": True, "switch1Id": db.SW_ROL1_DONE}
    evs = []
    for eid, name, (x, y), d in ROL1_SEATS:
        img = R.image(*S.FACES[name], direction=d)
        pages = [R.page([], img=R.image(""), priority=0, through=True),
                 R.page(S.say(name, _ROL1_WAIT[name]), img=img,
                        direction_fix=True, conditions=on)]
        if name == "The Convenor":
            pages.append(R.page(_rol1_meeting(), img=img, direction_fix=True,
                                conditions=dict(on, actorValid=True,
                                                actorId=db.ROLAND)))
        pages.append(R.page([], img=R.image(""), priority=0, through=True,
                            conditions=gone))
        evs.append(R.event(eid, name, x, y, pages))
    return evs


# ======================================================================
# ROL-5, The Understudy (`QUESTS.md` E17)
# ----------------------------------------------------------------------
# Somebody is being trained to replace him against the day the prophecy is
# ready. She is sixteen, she is extraordinary, and she has been told nothing
# about the review meetings. His whole moral position, for the length of the
# quest, is whether to tell her. He tells her. She takes it well, and asks the
# question nobody has asked in twenty-two years - whose prophecy is it,
# exactly? - and it is dropped, and never answered.
#
# * **It needs ROL-1**: the meetings are what there is to tell, and the minutes
#   are in the party's bag. Maud Penhallow sits at the Bell's snug table once
#   the hundred and forty-first has sat (Map 65, the last event), where the
#   meetings are held and she is not allowed to go.
# * **Two looks, both Roland's**: the first, he looks at her guard for an hour
#   and does not tell her (`SW_ROL5_ON`); the second, he has thought about it.
#   Without him she waits, and says so. Global switches, so a dismissed
#   Roland's errand waits.
# * **Nothing keeps him at the door.** What changes is that somebody is at the
#   tower door after all, and it is not him: she goes north to see the end of
#   one, since he never has. The door (Map 8, event 4) gains a page on
#   `SW_ROL5_DONE` that is its own page with her scene spliced in after his
#   departure, once (the door's self switch A); and she stands beside it.
UNDERSTUDY_EVENT_DOOR = "Maud (at the door)"


def _rol5_meet():
    c = S.narrate([
        "A girl of about sixteen sits at the snug table in a practice",
        "jacket, with a wooden sword across her knees and a pie she",
        "has forgotten about. She sees Roland, and stands up so fast",
        "that the pie goes over."])
    c += S.say("Maud", ["You're him. You're Roland",
                        "Fairweather."])
    c += S.say("Roland", ["...Guilty."])
    c += S.say("Maud", ["Maud Penhallow. I'm your understudy."])
    c += S.narrate(["Roland's face does something very careful."])
    c += S.say("Maud", ["Fellow Blunt's had me in his yard",
                        "since I was nine. Sword, horse,",
                        "lineage, the lot. In case."])
    c += S.say("Roland", ["In case of what?"])
    c += S.say("Maud", ["In case it's ready and you're -",
                        "you know."])
    c += S.say("Roland", ["Old."])
    c += S.say("Maud", ["They said 'unavailable'."])
    c += S.say("Maud", ["They say it's nearly ready. It's",
                        "been nearly ready since I was nine.",
                        "Is it nearly ready?"])
    c += S.narrate(["There is a pause, of the kind that has eleven",
                    "minutes in it."])
    c += S.say("Roland", ["They'd know better than I would."])
    c += S.say("Maud", ["They won't let me come to the",
                        "meetings. I'm not on the agenda.",
                        "What are they like?"])
    c += S.say("Roland", ["...Short."])
    c += S.narrate([
        "She asks him to look at her guard. He does, for an hour,",
        "in the yard behind the Bell, and says almost nothing, which",
        "from Roland is a great deal. She is extraordinary: she finds",
        "a gap in his that nobody has found in fifteen years."])
    c += S.narrate(["Outside, Roland is quiet for most of a street."])
    c += S.say("Roland", ["She's been told it's nearly ready.",
                          "I was told that when I was twelve."])
    c += S.say("Roland", ["I don't know whether to tell her.",
                          "I'm going to think about it. You'll",
                          "have noticed I'm not very good at it."])
    c += [R.control_switch(db.SW_ROL5_ON, True)]
    return c


def _rol5_tell():
    c = S.narrate([
        "Maud is at the snug table again, with a new pie, which",
        "she is guarding."])
    c += S.say("Roland", ["I've thought about it."])
    c += S.narrate([
        "He sits down across from her, which he has never done at",
        "that table, because at that table he is the asset."])
    c += S.say("Roland", ["Miss Penhallow. The meetings.",
                          "I'll tell you what they're like."])
    c += S.narrate([
        "He tells her. Apologies: the sorcerer. The minutes of the",
        "last. Readiness: the stone, not ready; the sword, in the",
        "stone; the lineage, present. The asset: available.",
        "Thanked. Eleven minutes, a hundred and forty-one times."])
    c += S.say("Roland", ["May I have those back a moment?"])
    c += S.narrate([
        "You give him the minutes, and he lays them on the table in",
        "front of her. She reads them twice, and then she eats some",
        "of the pie, and thinks, the way a person thinks who has been",
        "told to wait for seven years and is good at it."])
    c += S.say("Maud", ["Eleven minutes."])
    c += S.say("Roland", ["Eleven. I'm sorry. Somebody should",
                          "have told you at nine. Somebody",
                          "should have told me at twelve."])
    c += S.say("Maud", ["Can I ask something?"])
    c += S.say("Roland", ["Anything."])
    c += S.say("Maud", ["Whose prophecy is it?",
                        "Exactly?"])
    c += S.narrate([
        "Roland opens his mouth, and then he closes it. In twenty-two",
        "years of meetings, nobody has asked."])
    c += S.say("Roland", ["It's - it names a lineage. Mine.",
                          "It's -"])
    c += S.narrate([
        "Mrs Dewhirst comes over to ask whether anybody wants",
        "pudding, and the question stays where it is, on the table",
        "among the plates, and nobody picks it up."])
    c += S.say("Maud", ["Then I'm not waiting either."])
    c += S.say("Maud", ["You've never seen the end of one.",
                        "Eleven doors, you said. Where does",
                        "this one end?"])
    c += S.say("Roland", ["At a tower, in the north. I leave",
                          "at the door."])
    c += S.say("Maud", ["Then I'll be at the door. Somebody",
                        "ought to see the end of one. I'll",
                        "tell you how it ends."])
    c += S.narrate([
        "Roland laughs - properly, out loud, which nobody at the",
        "Bell has heard him do. Then he gives you back the minutes."])
    c += S.say("Roland", ["...Yes. All right. Do."])
    c += [S.trope(), R.control_switch(db.SW_ROL5_DONE, True)]
    c += S.companion_story(db.ROLAND)
    return c


def understudy_event(event_id):
    """Maud Penhallow at the Bell's snug table (Map 65, the last event):
    nobody before the hundred and forty-first meeting; then waiting for the
    asset; met, with Roland; told, with him on a second look; and gone north
    once she has asked whose prophecy it is."""
    img = R.image(*S.FACES["Maud"], direction=8)
    met = {"switch1Valid": True, "switch1Id": db.SW_ROL1_DONE}
    on = {"switch1Valid": True, "switch1Id": db.SW_ROL5_ON}
    roland = {"actorValid": True, "actorId": db.ROLAND}
    blank = dict(img=R.image(""), priority=0, through=True)
    return R.event(event_id, "Maud Penhallow", *places.UNDERSTUDY_BELL, [
        R.page([], **blank),
        R.page(S.narrate([
            "A girl of about sixteen in a practice jacket, at the snug",
            "table, with a wooden sword across her knees, watching the",
            "door."]) + S.say("Maud", ["Is Mr Fairweather with you? I'm",
                                       "meant to study how he stands."]),
            img=img, direction_fix=True, conditions=met),
        R.page(_rol5_meet(), img=img, direction_fix=True,
               conditions=dict(met, **roland)),
        R.page(S.say("Maud", ["Is he coming back? He went off",
                              "thinking. You can tell. He stands",
                              "differently when he's thinking."]),
               img=img, direction_fix=True, conditions=on),
        R.page(_rol5_tell(), img=img, direction_fix=True,
               conditions=dict(on, **roland)),
        R.page([], conditions={"switch1Valid": True,
                               "switch1Id": db.SW_ROL5_DONE}, **blank),
    ])


def dewhirst_after(own):
    """Mrs Dewhirst (Map 65, event 2) afterwards, below her ladder: her own
    last page for everybody, and a line about the snug."""
    page = copy.deepcopy(own)
    page["list"] = own["list"][:-1] + S.say("Mrs Dewhirst", [
        "Snug's empty, love. Miss",
        "Penhallow's gone north. Said to tell",
        "Mr Fairweather she'd be at the door."])
    page["list"] += R.page([])["list"][-1:]
    page["conditions"] = R.page([], conditions={
        "selfSwitchValid": True, "selfSwitchCh": "A",
        "switch1Valid": True, "switch1Id": db.SW_ROL5_DONE})["conditions"]
    return page


def _rol5_at_door():
    """Spliced into the tower door's page after his departure, once."""
    c = R.if_then(R.condition_switch(db.SW_ROLAND_GONE), S.narrate([
        "Forty paces off, he stops, and looks back once, at the girl",
        "standing beside the door with a practice sword. She raises",
        "it to him, the way you are taught to at nine. He raises a",
        "hand, and goes."]))
    c += S.narrate(["Somebody is at the tower door after all.",
                    "It is not him."])
    c += S.say("Maud", ["He said somebody ought to see the",
                        "end of one."])
    c += S.say("Maud", ["I'm the understudy. I'll wait here.",
                        "When you come out, I'll go and tell",
                        "him how it ends."])
    return R.if_then(R.condition_self_switch("A", False),
                     c + [R.self_switch("A", True)])


def door_pages(door, split):
    """The Obligatory Tower's door (Map 8, event 4) once she has gone north:
    its own page, `door`, with her scene after the first `split` commands -
    his departure, which still happens - and nothing else changed."""
    return [R.page(door[:split] + _rol5_at_door() + door[split:],
                   img=R.image(""), trigger=1, priority=0, through=True,
                   conditions={"switch1Valid": True,
                               "switch1Id": db.SW_ROL5_DONE})]


def understudy_at_door(event_id):
    """Maud beside the tower door (Map 8, the last event), once she has gone
    north: nobody before."""
    return R.event(event_id, UNDERSTUDY_EVENT_DOOR, *places.UNDERSTUDY_DOOR, [
        R.page([], img=R.image(""), priority=0, through=True),
        R.page(S.say("Maud", ["Go on. I'll be here. Somebody",
                              "ought to see the end of one."]),
               img=R.image(*S.FACES["Maud"], direction=2),
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_ROL5_DONE}),
    ])
