"""Maps 31-32: Restwell, and The Eight Hours.

`../SITES.md` step 1, and the second of the world map's twenty-nine sites to
get a room behind its door. `../BIOS.md` is the bio: **Mrs Hester Ashbury**,
landlady of the Eight Hours, in a crossroads town of one street and nineteen
inns.

It is step 1 because it is `penultima.py`'s shape with a **different
mechanic** - an inn rather than a shop - and building it is the cheapest way
to find out whether that template generalises. It does. The only things that
had to be thought about again were the ones below.

* **The world-map door is not written here and its coordinates are not written
  anywhere in this game.** `journey.world_map` claims the site by *name* and
  builds the real doors on whatever cells `worldmap.json` put the placeholders
  on. `places.py` therefore has a `RESTWELL_STEP` - the square the player is
  put back on coming out, which is this game's decision - and no
  `WORLD_RESTWELL`. `../WORLDMAP.md` 7.6.
* **The inn idiom is `village.py`'s Gilded Turnip**, copied rather than
  reinvented: a choice block behind a gold check, Recover All between a fadeout
  and an ME. The price is ten, which is half Prudence's twenty and is what the
  bio says, and the joke is that the famous one is the cheap one.
* **Nobody in Restwell is unhappy.** The Register A moment here is Walt's tune
  at the foot of the stairs, and `../NORTH.md` 1.2 is the rule it is written
  to: the surface reading is a compliment, the marriage is a good one, and the
  game never says the thing. The register on the bar is the second, by
  mechanism 4 - a document does not know what it is saying.
* **Four furniture constants in this room are not the obvious ones**, and
  `propsheet.py` over the finished map is the only thing that says so.
  `IN_COUNTER` is a shelf with two teddy bears on it, `IN_TABLE_ROUND` and
  `IN_TABLE_SMALL` are a broken table and a broken stool, and `INC_BELL` is a
  **`Globe`**. The last one is new here, and `INC_DESK_BELL` is it corrected.
  `IN_TABLE_ONE` is the fifth and is a trap of its own kind: it is `Table B`,
  which is sound and is *illegible* - a red cloth with no other detail in it,
  which at forty-eight pixels is a red drum. Every table in this room is
  `IN_TABLE` (`Table A`), two cells wide, which reads as a table.
"""
import handdrawn as HD
import mapkit as K
import rmmzdata as R

import db
import story as S
from places import (MAP_WORLD, MAP_RESTWELL, MAP_EIGHT_HOURS, RESTWELL_STEP)
import q_spare

# The name `worldmap.json`'s door events carry for this site. See the module
# docstring and `journey.world_map`; a re-stamp that moves Restwell moves its
# doors with it and nothing here needs editing.
SITE = "Restwell"

# ------------------------------------------------------------- the street ---
# One street east to west and one road north to south, because a crossroads
# town is a town that is four ways of passing through. All four ends of it go
# back out onto the world map: a road that runs into a hedge is the one thing
# a crossroads must not have.
RW, RH = 30, 24
STREET_Y = 14                       # the street: rows 13 and 14
CROSS_X = 15                        # the north road: columns 15 and 16

GATE_W = (0, STREET_Y)
GATE_E = (29, STREET_Y)
GATE_N = (CROSS_X, 0)
GATE_S = (CROSS_X, 23)

# Five of the nineteen are drawn. The notice on the street accounts for the
# other fourteen, which is cheaper than drawing them and is the better joke.
#
# **A building's only *face* is its south side**, so the two inns on the south
# side of the street show the player their backs and are read from a lane
# behind them - `LANE_Y`, rows 20 and 21, which the north road runs down into.
# The first draft put them against the bottom of the map with the tree line
# below them, which left their doorsteps in a sealed four-cell pocket: a sign
# nobody can stand in front of. `validate.py` said so; a screenshot did not.
EIGHT = (7, 6, 7, 6)                # the Eight Hours, north side
SEVEN = (18, 6, 6, 5)               # the one that is an hour quicker
INN_N = (25, 6, 4, 5)
LANE_Y = 20                         # the back lane: rows 20 and 21
REST = (4, 15, 6, 5)                # The Traveller's Rest, and Second Rest
INN_S = (18, 15, 6, 5)

EIGHT_DOOR = (10, EIGHT[1] + EIGHT[3] - 1)
EIGHT_OUT = (EIGHT_DOOR[0], EIGHT_DOOR[1] + 1)
SEVEN_FRONT = (20, SEVEN[1] + SEVEN[3] - 1)
REST_FRONT = (6, REST[1] + REST[3] - 1)
SIGNPOST_AT = (3, 12)
NOTICE_AT = (13, 12)

# ------------------------------------------------------- the Eight Hours ---
#            w   h  x1  y1  x2  y2  door_x
ROOM = (24, 17, 3, 4, 20, 11, 9)
# The ground-floor room with the two beds in it, walled off the bar's
# north-east corner (`mapkit.guest_room`). Everybody else goes up the stairs.
BEDROOM = (17, 4, 20, 7, 19)                # x1, y1, x2, y2, door_x
BEDS = (18, 4)                              # the left of two, a cell apart

# The flight up to the rooms, in the north wall beside the bedroom's
# partition, drawn the way Mike drew the Slain Wyvern's (`mapkit.stairs_up`).
# There is no upstairs map, so the top tread says why not.
STAIRS_X = 14                               # the flight's west column

# Where Walt sits, which is the one thing in the room the site is about: the
# bottom step of the flight's west column, facing the room, so the east column
# is still the way up.
WALT = (14, 6)
BAR_Y = 6                                   # the bar, a row off the shelves


# =============================================================== the street ==
def restwell_map():
    w, h = RW, RH
    g = K.Canvas(w, h)
    g.fill(0, 0, w - 1, h - 1, 0, K.GRASS)

    # Both roads are cobbled the whole way through, because a crossroads town
    # is a town whose entire economy is the road surface.
    g.fill(0, STREET_Y - 1, w - 1, STREET_Y, 0, K.COBBLE)
    g.fill(CROSS_X, 0, CROSS_X + 1, h - 1, 0, K.COBBLE)
    g.fill(0, LANE_Y, w - 1, LANE_Y + 1, 0, K.PATH)
    for door in (EIGHT_DOOR, SEVEN_FRONT):
        g.fill(door[0], door[1] + 1, door[0], STREET_Y - 2, 0, K.COBBLE)

    g.building(*EIGHT, wall=K.WALL_PLASTER, roof=K.ROOF_BROWN)
    g.building(*SEVEN, wall=K.WALL_PLANK_LIGHT, roof=K.ROOF_GREEN)
    g.building(*INN_N, wall=K.WALL_PLANK, roof=K.ROOF_BROWN)
    g.building(*REST, wall=K.WALL_TIMBER, roof=K.ROOF_BROWN)
    g.building(*INN_S, wall=K.WALL_PLANK, roof=K.ROOF_GREEN)

    g.autotile(0)

    # Every front on the street carries a bed and a mug, which is the town in
    # one picture. The Eight Hours gets the inn sign itself and a window.
    g.set(EIGHT_DOOR[0] - 2, EIGHT_DOOR[1], 3, K.SIGN_INN)
    g.set(EIGHT_DOOR[0] - 1, EIGHT_DOOR[1], 3, K.SIGN_MUG)
    g.set(EIGHT_DOOR[0] + 1, EIGHT_DOOR[1], 3, K.WINDOW)
    g.set(EIGHT_DOOR[0] + 2, EIGHT_DOOR[1], 3, K.WINDOW)

    g.set(SEVEN_FRONT[0] - 1, SEVEN_FRONT[1], 3, K.SIGN_INN)
    g.set(SEVEN_FRONT[0] + 1, SEVEN_FRONT[1], 3, K.WINDOW)

    g.set(INN_N[0] + 1, INN_N[1] + INN_N[3] - 1, 3, K.SIGN_INN)
    g.set(INN_N[0] + 2, INN_N[1] + INN_N[3] - 1, 3, K.WINDOW)

    g.set(REST_FRONT[0] - 1, REST_FRONT[1], 3, K.SIGN_INN)
    g.set(REST_FRONT[0] + 2, REST_FRONT[1], 3, K.WINDOW)

    g.set(INN_S[0] + 1, INN_S[1] + INN_S[3] - 1, 3, K.SIGN_MUG)
    g.set(INN_S[0] + 4, INN_S[1] + INN_S[3] - 1, 3, K.WINDOW)

    for b in (EIGHT, SEVEN, REST, INN_S):
        g.chimney_beside(*b[:2])

    # `SIGNPOST` and `LAMP` both stand with their foot in the lower cell, so
    # the lamps are drawn from STREET_Y - 4 - a lamp is three cells, head,
    # post and foot - and their feet land beside the road rather than in it.
    g.set(*SIGNPOST_AT, 3, K.SIGNPOST)
    g.column(6, STREET_Y - 4, 3, K.LAMP)
    g.column(23, STREET_Y - 4, 3, K.LAMP)
    g.column(CROSS_X - 1, 3, 3, K.LAMP)
    # Beside the road above the lane, not in it: one standing in a two-row
    # lane cuts the lane in half. West of the road, because the east side
    # is the chimney of the inn on that corner.
    g.column(CROSS_X - 1, LANE_Y - 3, 3, K.LAMP)

    # The notice stands on a barrel, which is Penultima's idiom for a thing
    # pinned up in a street. **Not `CRATE`**, which is `Barricade (H)`, and
    # not `TUB`, which is a `Well` - both named for what they looked like at
    # forty-eight pixels and both something else. The well is worth having
    # once, at the crossroads, and is wrong as scenery in a back lane.
    g.scatter([(2, 12), (24, 12), (12, 21), (26, 21),
               (NOTICE_AT[0], NOTICE_AT[1])], 3, K.BARREL)
    g.scatter([(12, 17)], 3, K.TUB)                     # `Well`, and it is one
    g.scatter([(2, 4), (26, 3), (2, 20), (27, 20)], 3, K.BUSH)
    g.scatter([(11, 3), (20, 3), (5, 21), (21, 21)], 3, K.FLOWERS2)
    g.scatter([(5, 4), (26, 12)], 3, K.FLOWERS)
    g.scatter([(12, 3), (24, 4)], 3, K.LOGS)

    # Trees along the top and bottom and both sides, with a gap at each of the
    # four road ends. The gaps are the gates.
    for x in range(0, w - 1, 2):
        if not (CROSS_X - 1 <= x <= CROSS_X + 1):
            g.blit(x, 0, 3, K.TREE)
            g.blit(x, h - 2, 3, K.TREE)
    for y in range(2, h - 3, 2):
        if not (STREET_Y - 2 <= y <= STREET_Y):
            g.blit(0, y, 3, K.TREE)
            # The northernmost inn on the east side runs to the map edge, so
            # the tree line stops where its roof starts. `Canvas.building`
            # refuses the overlap rather than drawing a tree on a roof, which
            # is how this was found.
            if not (INN_N[1] - 1 <= y <= INN_N[1] + INN_N[3]):
                g.blit(w - 2, y, 3, K.TREE)

    m = K.new_map(w, h, K.TS_OUTSIDE, name="Restwell", bgm="Town1")
    m["data"] = g.data
    m["events"] = [None] + restwell_events()
    # Each road is two wide: the street is rows 13 and 14, the north-south
    # road columns 15 and 16.
    for event_id, (x, y) in [(1, GATE_W), (2, GATE_E)]:
        S.widen_exit(m["events"], event_id, [(x, y - 1)])
    for event_id, (x, y) in [(3, GATE_N), (4, GATE_S)]:
        S.widen_exit(m["events"], event_id, [(x + 1, y)])
    return m


def restwell_events():
    evs = []

    # 1-4: the four ways out, all onto the same square of the world map. All
    # of them are "below characters": an exit tile at "same as characters" is
    # one the player walks straight over.
    for i, (name, cell, facing) in enumerate([
            ("The Road West", GATE_W, 4), ("The Road East", GATE_E, 6),
            ("The Road North", GATE_N, 8), ("The Road South", GATE_S, 2)]):
        evs.append(S.exit_tile(i + 1, name, *cell, MAP_WORLD,
                               *RESTWELL_STEP, direction=facing))

    # 5: the fingerpost, which is the town's whole premise in four boards.
    # Read from the tile beside it - a `SIGNPOST` tile blocks its own cell.
    sign = S.narrate([
        "A fingerpost with four boards on it.",
        "Three of them say \\C[14]RESTWELL\\C[0]."])
    sign += S.narrate([
        "The fourth says \\C[14]RESTWELL (CONT.)\\C[0] and points",
        "back the way you have just come."])
    sign += S.narrate([
        "Under them, smaller:",
        "",
        "   NINETEEN INNS. ONE STREET.",
        "   PLEASE DO NOT SLEEP IN THE ROAD."])
    sign += [S.trope()]
    evs.append(R.event(5, "The Crossroads Sign", *SIGNPOST_AT, [R.page(
        sign, img=R.image(""), trigger=0, priority=1, through=True,
        direction_fix=True)]))

    # 6: the Eight Hours.
    evs.append(S.door(6, "The Eight Hours", *EIGHT_DOOR, MAP_EIGHT_HOURS,
                      ROOM[6], ROOM[5]))

    # 7: the other eighteen, and the reason nobody in this town is a rival.
    notice = S.narrate([
        "A painted list under glass, nailed to a",
        "barrel, headed \\C[14]THE INNS OF RESTWELL\\C[0], with",
        "nineteen names on it. Eleven have been",
        "crossed out and written in again."])
    notice += S.narrate([
        "At the bottom, firmly:",
        "'THE EIGHT HOURS IS THE ONE IN THE SONGS.",
        "THE OTHERS ARE ALSO VERY GOOD.'"])
    notice += S.narrate([
        "Under that, in eighteen other hands,",
        "the word 'YES.'"])
    evs.append(S.pin_note(R.event(7, "The Inns Of Restwell", *NOTICE_AT, [R.page(
        notice, img=R.image(""), trigger=0, priority=1, through=True,
        direction_fix=True)])))

    # 8: the one next door, which is an hour quicker.
    seven = S.narrate([
        "\\C[14]THE SEVEN HOURS\\C[0]. A good front, freshly",
        "painted, and a card in the window:",
        "'JUST AS RESTFUL. ONE HOUR QUICKER.'"])
    seven += S.narrate([
        "The door is shut. A second card, older,",
        "hangs under the first:",
        "",
        "        'BACK IN EIGHT HOURS.'"])
    evs.append(S.shut(R.event(8, "The Seven Hours", *SEVEN_FRONT, [R.page(
        seven, img=R.image(""), trigger=0, priority=1, through=True,
        direction_fix=True)])))

    # 9: and the one on the south side, which has solved expansion.
    rest = S.narrate([
        "\\C[14]THE TRAVELLER'S REST\\C[0], and beneath it",
        "\\C[14]THE TRAVELLER'S SECOND REST\\C[0], and beneath",
        "that a hand-lettered strip reading",
        "\\C[14]THE TRAVELLER'S REST (ANNEXE)\\C[0]."])
    rest += S.narrate([
        "All three of them are over the same door,",
        "and it is the only door there is."])
    evs.append(S.shut(R.event(9, "The Traveller's Rest", *REST_FRONT, [R.page(
        rest, img=R.image(""), trigger=0, priority=1, through=True,
        direction_fix=True)])))

    # 10: a guest, on his way out, at four in the afternoon. This is the
    # premise stated once on the street so that the inn does not have to.
    guest = S.say("Guest", ["Morning!"])
    guest += S.narrate(["It is four in the afternoon."])
    guest += S.say("Guest", [
        "Slept like the dead.",
        "Eight hours, easy. Best night in years."])
    guest += S.narrate(["You ask when he went up."])
    guest += S.say("Guest", ["Noon."])
    guest += S.narrate([
        "He says it without the slightest difficulty,",
        "shoulders his pack, and walks off whistling",
        "eight bars of something."])
    guest += [S.trope()]
    evs.append(S.npc(10, "A Satisfied Guest", 12, 12, guest,
                     "People2", 4, direction=2))
    evs.append(q_spare.courier("restwell", 5, 12))                 # SPA-1
    return evs


# ========================================================= The Eight Hours ==
def eight_hours_map():
    """Drawn by hand in the editor and kept by `handdrawn.py` (Mike, October
    2026), from the generated inn: the bar a row out from the shelves, the
    stairs up through the wall beside the bedroom, and the two beds stood
    apart. Only the events are built here."""
    w, h = ROOM[0], ROOM[1]
    data = HD.load(MAP_EIGHT_HOURS, w, h, K.TS_INSIDE)
    m = K.new_map(w, h, K.TS_INSIDE, name="The Eight Hours", bgm="Town3",
                  battleback=("Wood1", "Room1"))
    m["data"] = data
    m["events"] = [None] + eight_hours_events()
    return m


def eight_hours_events():
    evs = [S.exit_tile(1, "Inn Door", ROOM[6], ROOM[5] + 2,
                       MAP_RESTWELL, *EIGHT_OUT)]

    # 2: Mrs Ashbury, and the bed. `village.py`'s Gilded Turnip is the idiom
    # and this is it with the numbers changed: a choice block behind a gold
    # check, Recover All between a fadeout and an ME.
    def beds(lines):
        stay = [R.lose_gold(10), R.fadeout_screen(), R.play_me("Inn1"),
                R.recover_all(), R.wait(90), R.fadein_screen()]
        stay += S.narrate([
            "You go up. There is a little tune behind you",
            "on the way, eight bars of it, and then it",
            "stops."])
        stay += S.narrate([
            "You come down. Everyone is whole, and warm,",
            "and unpoisoned, and agrees without discussing",
            "it that it is morning."])
        stay += S.narrate([
            "Breakfast is on the bar. It is always on the",
            "bar."])
        stay += [S.trope()]
        stay += [R.call_common_event(db.CE_MORNING)]               # SPA-3: is it spring yet
        cmds = S.say("Mrs Ashbury", lines)
        cmds += R.choice_block(
            ["Take a room (10cr)", "Not just now"],
            [R.if_then(R.condition_script("$gameParty.gold() >= 10"), stay,
                       S.say("Mrs Ashbury",
                             ["Come back when you have got ten."]))],
            cancel=None)
        return cmds

    first = S.say("Mrs Ashbury", [
        "Ten crowns a night, love.",
        "Breakfast included."])
    first += S.narrate(["You ask when breakfast is."])
    first += S.say("Mrs Ashbury", [
        "Whenever you come down.",
        "I argued about that for a year.",
        "Now I just cook."])
    first += S.narrate(["You ask about the songs."])
    first += S.say("Mrs Ashbury", [
        "Resurrection's extra.",
        "And I'll want the room back by noon."])
    first += S.narrate(["It is already twenty past two."])
    first += S.say("Mrs Ashbury", ["Then you had better get up there."])
    first += [R.self_switch("A", True)]
    first += beds(["Ten crowns, love.",
                   "Walt will play you up."])

    later = beds([
        "Back again. Ten crowns.",
        "Walt is by the stairs. He always is."])

    img = R.image("Gen_People1", 6, direction=2)
    evs.append(R.event(2, "Mrs Hester Ashbury", 8, 5, [
        R.page(first, img=img, trigger=0, priority=1),
        R.page(later, img=img, trigger=0, priority=1,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ]))

    # 3: Walt, and the tune. `../SITES.md` step 1 calls this the site's
    # Register A candidate and it is written to `../NORTH.md` 1.2: mechanism
    # one, the innocent superlative, offered as praise. Every line of it is
    # literally about a fiddle. The marriage is a good one, nobody is unhappy
    # in it, and the game never lets on.
    tune = S.narrate([
        "A man with a fiddle, sitting on the bottom",
        "step where he can see the whole room."])
    tune += S.say("Walt", [
        "Going up? Say the word.",
        "I'll play you up."])
    tune += S.narrate(["You ask whether he plays for everybody."])
    tune += S.say("Walt", [
        "Everybody. Twenty-six years.",
        "Same eight bars, every time."])
    tune += S.narrate(["You ask whether it has to be that one."])
    tune += S.say("Walt", [
        "It has to be that one.",
        "I tried a different one, once.",
        "They came down tired."])
    tune += S.narrate([
        "Behind the bar, Mrs Ashbury does not look up."])
    tune += S.say("Mrs Ashbury", ["He is very good at it."])
    tune += S.narrate([
        "She has listened to those eight bars for",
        "twenty-six years and has never once asked",
        "him to stop."])
    tune += [S.blush(), R.self_switch("A", True)]

    again = S.narrate([
        "Walt is tuning. It does not need tuning.",
        "He is going to tune it anyway."])
    walt_img = R.image("Gen_People1", 7, direction=2)
    evs.append(R.event(3, "Walt Ashbury", *WALT, [
        R.page(tune, img=walt_img, trigger=0, priority=1),
        R.page(again, img=walt_img, trigger=0, priority=1,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ]))

    # 4: the register, open on the bar. `../NORTH.md` 1.3 mechanism four - a
    # document does not know what it is saying - and the second of this site's
    # two blushes. The party of six is first on purpose: the entry the page
    # opens on has to be a crowd, or the joke is about couples and is a
    # different joke that this game does not make.
    book = S.narrate([
        "The register, open on the bar, ruled in a",
        "firm hand. The last two entries:"])
    book += S.narrate([
        "  Party of six. Up 12.02. Down 12.09.",
        "  Slept: eight hours. Remarks: lovely.",
        "  Mr & Mrs Tolley. Up 12.11. Down 12.19.",
        "  Slept: eight hours. Remarks: LOVELY."])
    book += S.narrate([
        "Every entry on the page says eight hours.",
        "Every entry is in a different hand.",
        "Nobody has ever written anything else."])
    book += [S.blush(), R.self_switch("A", True)]
    book_again = S.narrate([
        "Eight hours, eight hours, eight hours,",
        "eight hours, and one 'eight hrs' where",
        "somebody was in a hurry."])
    page = dict(img=R.image(""), trigger=0, priority=1, direction_fix=True,
                through=True)
    evs.append(R.event(4, "The Register", 5, BAR_Y, [
        R.page(book, **page),
        R.page(book_again, conditions={"selfSwitchValid": True,
                                       "selfSwitchCh": "A"}, **page),
    ]))

    # 5: the town doctor, who has no patients left and took a room for a
    # fortnight eleven years ago. He is the only person in Restwell who has
    # noticed, and he is not unhappy about it either.
    doc = S.say("Dr Pike", [
        "Pike. Doctor. Retired in the practical",
        "sense, which is to say nobody comes."])
    doc += S.narrate(["You ask how long he has been retired."])
    doc += S.say("Dr Pike", [
        "Eleven years. I took a room for a",
        "fortnight, to think about it."])
    doc += S.narrate(["You ask what he does instead."])
    doc += S.say("Dr Pike", [
        "I watch.",
        "Twelve hundred guests a year go up that",
        "staircase, and every one of them comes",
        "down better, and nobody can tell me why."])
    doc += S.narrate([
        "He looks at the fiddle player for slightly",
        "too long, and then back at his breakfast."])
    doc += S.say("Dr Pike", ["I have theories. I do not like them."])
    doc += [S.trope()]
    evs.append(S.npc(5, "Dr Pike", 11, 7, doc, "SF_Actor3", 6, direction=2))

    # 6: the beds, which is the bio's one flat impossibility stated flatly.
    beds_look = S.narrate([
        "Two beds, made up, with the corners folded",
        "by somebody who has folded ten thousand of",
        "them."])
    beds_look += S.narrate([
        "They have not been slept in.",
        "They have also, plainly, been slept in."])
    evs.append(R.event(6, "The Beds", BEDS[0], BEDS[1] + 1, [R.page(
        beds_look, img=R.image(""), trigger=0, priority=1, through=True,
        direction_fix=True)]))

    # 7, 8: the top tread of each column of the stairs. The rooms are
    # upstairs and there is no upstairs, so this is as far as anybody goes
    # who has not taken one.
    stairs = S.narrate([
        "The stairs up to the rooms. Somebody up there is",
        "asleep, audibly, and has been since noon."])
    for i in range(2):
        evs.append(R.event(7 + i, "The Stairs Up", STAIRS_X + i, ROOM[3], [
            R.page(stairs, img=R.image(""), trigger=1, priority=1,
                   direction_fix=True)]))
    return evs


# ================================================================ the doors ==
def world_doors(base_id, cells):
    """The real doors into Restwell, on the world map.

    `cells` is every square `worldmap.json` put a placeholder door on for this
    site, handed in by `journey.world_map` - so the geometry stays the world
    map's and only the destination is ours. `Town A` is two cells and both of
    them get a door.

    Player-touch and below characters, which is the world map's own idiom for
    a place you walk into, and what `finish.add_site` wrote the placeholders
    as."""
    evs = []
    for i, (x, y) in enumerate(sorted(cells)):
        arrive = S.narrate([
            "Restwell. One street, four roads into it,",
            "and nineteen inns along the one street."])
        arrive += R.choice_block(
            ["Go in", "Press on"],
            [[R.play_se("Move1"),
              R.transfer(MAP_RESTWELL, GATE_W[0] + 2, GATE_W[1], 6, 0)],
             S.narrate(["You press on. There will be another one.",
                        "There are eighteen more in this one."])])
        evs.append(R.event(base_id + i, "Restwell", x, y, [R.page(
            arrive, img=R.image(""), trigger=1, priority=0, through=True)]))
    return evs


def build():
    R.save_map(MAP_RESTWELL, restwell_map())
    R.save_map(MAP_EIGHT_HOURS, eight_hours_map())
