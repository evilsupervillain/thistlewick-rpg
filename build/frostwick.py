"""Maps 44-47: Frostwick, the Eleven Days, the committee's room, and the
practitioner's cold room.

`../SITES.md` step 10. The source is `../WORLDMAP.md` 7.3: **the town that
voted to keep the curse.** The hundred-year winter was broken forty years ago,
the snow stopped for eleven days, and then the town held a meeting. The curse
is now maintained under an annual contract, by a retained practitioner whose
speciality is refrigeration, and the town is very proud of the arrangement.

* **Read 7.3's correction before changing a line of Perce.** He is **not** a
  Chosen One. He is one of the unnumbered who went north with everybody else,
  he never got near the Tower, and on the way he solved this town's problem
  entirely. Frostwick has called him a Chosen One for forty years because it
  is better for the Festival, and he has never corrected anybody. The
  visitors' book in the Eleven Days is where that is written down, faintly.
  He is not diminished by any of it (`../NORTH.md` 1.6): he won, he retired
  somewhere nice, and he married well.
* **Two Register A moments**, both to `../NORTH.md` 1.2. Ida's is 7.3's own
  target line, mechanism one, the innocent superlative about the ribbon. Clem's
  is mechanism two, the leaky child, reporting his nan's kitchen at the
  committee's table with the reaction shot after it. 7.3 counted only Clem's,
  and `../SITES.md` step 10 gives the site's moment to Ida. They are two
  different lines, both are compliments, and the marriage in both is plainly
  a good one, so both count. `VAR_BLUSHES` goes up by two.
* **The documents do most of the work** - mechanism four. They are the minutes
  of the working group, the asset register, the Schedule of Snowfalls and the
  visitors' book. None of them needs a face.
* **It snows on the street and nowhere else.** The weather idiom is
  `north.py`'s: an autorun that sets it and erases itself, so it comes back on
  every arrival, and a way indoors that clears it on the way through. The
  snow here is contracted, so it is gentle.
* **The door is claimed by name**, `journey.world_map`'s mechanism, and
  `places.py` has `FROSTWICK_STEP` and no world coordinate.
"""
import mapkit as K
import rmmzdata as R

import db
import story as S
import q_hob
import q_spare
from places import (MAP_WORLD, MAP_FROSTWICK, MAP_ELEVEN_DAYS,
                    MAP_WORKING_GROUP, MAP_COLD_ROOM, FROSTWICK_STEP)

# The name `worldmap.json`'s door events carry for this site.
SITE = "Frostwick"

# ----------------------------------------------------------- snow tiles ---
# None of these had a `mapkit` constant, because nothing in this game had a
# snow street before. Read off `Outside_A2.txt`, `Outside_A3.txt` and
# `Outside_B.txt`, and cropped before use.
SNOW = K.A(40)                  # A2 `Snow`
SNOW_ROAD = K.A(42)             # A2 `Road (Snow)`
WALL_SNOW_BRICK = K.A(77)       # A3 `Snow Outer Wall (Brick)`
WALL_SNOW_WOOD = K.A(78)        # A3 `Snow Outer Wall (Wood)`
# `Conifer Tree (Snow)`, 2x2. The top row is a star tile and the bottom blocks.
SNOW_TREE = ((K.b_tile(8, 8), K.b_tile(9, 8)), (K.b_tile(8, 9), K.b_tile(9, 9)))
# `Streetlight B (Snow)`: lamp, post, and a foot in a drift, which blocks.
SNOW_LAMP = (K.b_tile(0, 4), K.b_tile(0, 5), K.b_tile(0, 6))
SNOW_SIGN = K.b_tile(9, 10)     # `Sign A (Snow)`
SNOWMAN = K.b_tile(8, 11)
SNOW_BARREL = K.b_tile(13, 10)
SNOW_CRATE = K.b_tile(15, 8)    # `Crate (Snow)`

SNOW_POWER = 3


def snow(indent=0):
    return R.set_weather("snow", power=SNOW_POWER, duration=1, indent=indent)


def dry(indent=0):
    return R.set_weather("none", duration=1, indent=indent)


def weather_event(event_id):
    """Autorun, once per arrival, then erase itself - `north.py`'s idiom. An
    erased event comes back on the next load, so it snows every visit."""
    return R.event(event_id, "The Weather", 0, 0, [R.page(
        [snow(), R.erase_event()],
        img=R.image(), trigger=3, priority=0, through=True)])


def door(event_id, name, x, y, target_map, tx, ty):
    """A door indoors. The snow is cleared after the walk and before the fade,
    which is `north.door`; forgetting it once sends the weather indoors."""
    cmds = S.door_page(target_map, tx, ty, 8)
    cmds.insert(len(cmds) - 1, dry())
    return R.event(event_id, name, x, y, [R.page(
        cmds, img=R.image("!Door1", 0, direction=2), trigger=1, priority=1)])


# ------------------------------------------------------------ the street ---
# One street east to west with the road in from the world map at its east end,
# the town's four buildings along its north side facing it, and the Festival
# green south of it. A building's only face is its south side, so all four
# fronts are on the street and nothing on the green has its back to anybody.
FW, FH = 36, 22
STREET_Y = 14                       # the street: rows 13 and 14
GATE_E = [(FW - 1, STREET_Y - 1), (FW - 1, STREET_Y)]
ARRIVE = (FW - 2, STREET_Y)

STAGGS = (3, 7, 5, 5)
ELEVEN = (9, 5, 9, 7)
GROUP = (19, 6, 7, 6)
COLD = (27, 7, 5, 5)


def _front(b, dx):
    return (b[0] + dx, b[1] + b[3] - 1)


STAGGS_DOOR = _front(STAGGS, 2)
ELEVEN_DOOR = _front(ELEVEN, 4)
GROUP_DOOR = _front(GROUP, 3)
COLD_DOOR = _front(COLD, 2)

TOWN_SIGN = (FW - 4, STREET_Y - 2)
RIBBON_POST = (17, 16)
PERCE = (16, 17)
IDA = (10, 17)
SNOWMAN_AT = (25, 18)


def frostwick_map():
    w, h = FW, FH
    g = K.Canvas(w, h)
    g.fill(0, 0, w - 1, h - 1, 0, SNOW)
    g.fill(0, STREET_Y - 1, w - 1, STREET_Y, 0, SNOW_ROAD)
    for door_at in (STAGGS_DOOR, ELEVEN_DOOR, GROUP_DOOR, COLD_DOOR):
        g.set(door_at[0], door_at[1] + 1, 0, SNOW_ROAD)
    # The green: a trodden path from the street to the ribbon post.
    g.fill(RIBBON_POST[0], STREET_Y + 1, RIBBON_POST[0], RIBBON_POST[1] - 1,
           0, SNOW_ROAD)

    g.building(*STAGGS, wall=WALL_SNOW_WOOD, roof=K.ROOF_WHITE)
    g.building(*ELEVEN, wall=WALL_SNOW_BRICK, roof=K.ROOF_WHITE)
    g.building(*GROUP, wall=WALL_SNOW_BRICK, roof=K.ROOF_WHITE)
    g.building(*COLD, wall=K.WALL_ICE, roof=K.ROOF_WHITE)

    g.autotile(0)

    # Fronts. The Staggs' door is shut - they are out at the ribbon.
    g.column(STAGGS_DOOR[0], STAGGS_DOOR[1] - 1, 3, K.DOOR_SHUT)
    g.set(STAGGS_DOOR[0] + 1, STAGGS_DOOR[1], 3, K.WINDOW)
    g.set(STAGGS_DOOR[0] - 1, STAGGS_DOOR[1], 3, K.WINDOW)
    g.set(ELEVEN_DOOR[0] - 2, ELEVEN_DOOR[1], 3, K.SIGN_INN)
    g.set(ELEVEN_DOOR[0] - 1, ELEVEN_DOOR[1], 3, K.WINDOW)
    g.set(ELEVEN_DOOR[0] + 1, ELEVEN_DOOR[1], 3, K.WINDOW)
    g.set(ELEVEN_DOOR[0] + 2, ELEVEN_DOOR[1], 3, K.SIGN_MUG)
    g.set(GROUP_DOOR[0] - 1, GROUP_DOOR[1], 3, K.WINDOW)
    g.set(GROUP_DOOR[0] + 1, GROUP_DOOR[1], 3, K.WINDOW)
    g.set(COLD_DOOR[0] + 1, COLD_DOOR[1], 3, K.WINDOW)
    for x, y in [(STAGGS[0] + 1, STAGGS[1]), (ELEVEN[0] + 6, ELEVEN[1]),
                 (GROUP[0] + 1, GROUP[1])]:
        g.set(x, y, 2, K.STOVEPIPE)

    # Lamps down the street, the lantern trade being four fifths of the
    # parish income. Each is three cells and stands on its foot.
    for x in (8, 18, 26):
        g.column(x, STREET_Y - 4, 3, SNOW_LAMP)
    for x in (4, 23, 30):
        g.column(x, STREET_Y + 1, 3, SNOW_LAMP)

    g.set(*TOWN_SIGN, 3, SNOW_SIGN)
    g.set(*RIBBON_POST, 3, SNOW_SIGN)
    g.set(*SNOWMAN_AT, 3, SNOWMAN)
    g.scatter([(2, 12), (33, 11), (12, 16), (28, 16)], 3, SNOW_BARREL)
    g.scatter([(2, 16), (33, 17)], 3, SNOW_CRATE)

    # Snow conifers round the edge, with the road's gap at the east end.
    for x in range(0, w - 1, 2):
        g.blit(x, 0, 3, SNOW_TREE)
        g.blit(x, h - 2, 3, SNOW_TREE)
    for y in range(2, h - 3, 2):
        g.blit(0, y, 3, SNOW_TREE)
        if not (STREET_Y - 3 <= y <= STREET_Y):
            g.blit(w - 2, y, 3, SNOW_TREE)
    for x, y in [(12, 18), (20, 18), (29, 18), (3, 18)]:
        g.blit(x, y, 3, SNOW_TREE)

    m = K.new_map(w, h, K.TS_OUTSIDE, name="Frostwick", bgm="Town2")
    m["data"] = g.data
    m["events"] = [None] + frostwick_events()
    return m


def frostwick_events():
    evs = [weather_event(1)]

    # 2-3: the road east, back out onto the world map.
    for i, cell in enumerate(GATE_E):
        evs.append(R.event(2 + i, "The Road East", *cell, [R.page(
            [dry(), R.play_se("Move1"),
             R.transfer(MAP_WORLD, *FROSTWICK_STEP, 2, 0)],
            img=R.image(""), trigger=1, priority=0, through=True)]))

    # 4: the sign at the town end of the road. The eternal winter, and the
    # footnote that is the whole town.
    sign = S.narrate([
        "\\C[14]FROSTWICK\\C[0]",
        "Home of the Winter Festival.",
        "SNOW GUARANTEED*"])
    sign += S.narrate([
        "Along the bottom, much smaller:",
        "*Under contract. Schedule of snowfalls available",
        "on request from the parish."])
    sign += [S.trope()]
    evs.append(R.event(4, "The Town Sign", *TOWN_SIGN, [R.page(
        sign, img=R.image(""), trigger=0, priority=1, through=True,
        direction_fix=True)]))

    evs.append(door(5, "The Eleven Days", *ELEVEN_DOOR, MAP_ELEVEN_DAYS,
                    ELEVEN_ROOM[6], ELEVEN_ROOM[5]))
    evs.append(door(6, "The Working Group", *GROUP_DOOR, MAP_WORKING_GROUP,
                    GROUP_ROOM[6], GROUP_ROOM[5]))
    evs.append(door(7, "The Cold Room", *COLD_DOOR, MAP_COLD_ROOM,
                    COLD_ROOM_[6], COLD_ROOM_[5]))

    # 8: the Staggs' house, which is shut because they are out at the ribbon.
    staggs = S.narrate([
        "A neat house with its door shut and",
        "a card in the window, in two hands:",
        "   AT THE RIBBON. - P.",
        "   BACK FOR TEA. - I."])
    evs.append(R.event(8, "The Staggs' House", *STAGGS_DOOR, [R.page(
        staggs, img=R.image(""), trigger=0, priority=1,
        direction_fix=True)]))

    # 9: Perce, who broke it. 7.3's correction is the scene: Bram is a real
    # Chosen One, and Perce tells him quietly, and only him, that he is not.
    first = S.narrate([
        "An old man in a red coat with a white fur collar,",
        "standing beside the ribbon post as though it",
        "might need him."])
    first += S.say("Perce", [
        "Hello! You've come for the Festival?",
        "It's not till the twelfth.",
        "Everybody comes early."])
    first += S.narrate(["You ask whether he is the man who broke the winter."])
    first += S.say("Perce", [
        "I am. Percival Stagg. Perce.",
        "Forty years ago this spring."])
    first += S.narrate([
        "A lady with a basket goes by and says 'Our Chosen",
        "One!' He does a face: warm, modest, and very",
        "well practised."])
    first += S.narrate([
        "You mention, as one professional to another,",
        "that you are a Chosen One yourself.",
        "Number forty-eight."])
    first += S.say("Perce", [
        "Are you! Well. Good for you.",
        "I wasn't, you know. Chosen.",
        "Nobody chose me."])
    first += S.say("Perce", [
        "Everybody went north, that year.",
        "Farmers, tinkers, a man with a goat.",
        "I got as far as here, and the winter",
        "was in the way, so I saw to it."])
    first += S.narrate(["You ask why he has never said so."])
    first += S.say("Perce", [
        "Nobody's ever asked.",
        "They were all so pleased.",
        "And it's a lovely Festival."])
    first += [S.trope(), R.self_switch("A", True)]

    later = S.say("Perce", [
        "The twelfth. Ribbon at noon.",
        "I'll do the face. You'll see."])
    img = R.image("Gen_People3", 1, direction=2)
    evs.append(q_hob.owned("perce", R.event(9, "Perce Stagg", *PERCE, [  # HOB-1
        R.page(first, img=img, trigger=0, priority=1),
        R.page(later, img=img, trigger=0, priority=1,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ])))

    # 10: Ida, and 7.3's line for her - mechanism one, the innocent
    # superlative, offered as praise. It is literally about deeds, and it is
    # a compliment, and he goes pink across the green.
    ida = S.say("Ida", [
        "You've met Perce. Everybody meets Perce."])
    ida += S.narrate(["You ask whether she minds the Festival."])
    ida += S.say("Ida", [
        "Mind it? I love it. Forty years of it.",
        "He cuts the ribbon, the whole town",
        "cheers, and he goes pink."])
    ida += S.narrate([
        "You say that it must be nice, to have done",
        "one great thing."])
    ida += S.say("Ida", [
        "He did one great thing forty years ago.",
        "And a great many things since.",
        "None of THOSE ever got a ribbon."])
    ida += S.narrate([
        "Across the green, Mr Stagg has gone a little pink,",
        "and is examining the ribbon post with enormous",
        "care."])
    ida += [S.blush(), R.self_switch("A", True)]
    ida_again = S.say("Ida", [
        "Don't tell him I said so.",
        "He'll only go pink again."])
    img = R.image("Gen_People3", 2, direction=2)
    evs.append(R.event(10, "Ida Stagg", *IDA, [
        R.page(ida, img=img, trigger=0, priority=1),
        R.page(ida_again, img=img, trigger=0, priority=1,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ]))

    # 11: the ribbon post, and the programme pinned to it.
    post = S.narrate([
        "\\C[14]THE WINTER FESTIVAL\\C[0] - the twelfth.",
        "  Noon: the Ribbon. Mr P. Stagg.",
        "  Two o'clock: carols. Four: lanterns.",
        "  Throughout: a light dusting."])
    evs.append(R.event(11, "The Ribbon Post", *RIBBON_POST, [R.page(
        post, img=R.image(""), trigger=0, priority=1, through=True,
        direction_fix=True)]))

    # 12: the snowman, which the committee has judged.
    man = S.narrate([
        "A snowman wearing a Festival rosette.",
        "The rosette says: \\C[14]JUDGED - SNOW, ADEQUATE\\C[0]."])
    evs.append(R.event(12, "The Snowman", *SNOWMAN_AT, [R.page(
        man, img=R.image(""), trigger=0, priority=1, through=True,
        direction_fix=True)]))
    evs.append(q_spare.courier("frostwick", 27, 15))               # SPA-1
    return evs


# ========================================================= The Eleven Days ==
#            w   h  x1  y1  x2  y2  door_x
ELEVEN_ROOM = (19, 14, 3, 4, 15, 10, 9)
MARCHPANE = (8, 5)
VISITORS_BOOK = (5, 5)
SNOW_MARK = (13, 3)             # the plate, on the wall face, read from below


def eleven_days_map():
    w, h, x1, y1, x2, y2, door_x = ELEVEN_ROOM
    g = K.interior(w, h, x1, y1, x2, y2, door_x=door_x,
                   floor=K.IN_WOOD_FLOOR, floor_alt=K.IN_DARK_WOOD)

    # Behind the bar, and the bar. `IN_TABLE` is `Table A`, two cells wide,
    # and is Restwell's corrected bar - `IN_COUNTER` is the teddy-bear shelf.
    g.column(4, y1 - 1, 2, K.IN_SHELF_BOTTLES)
    g.column(6, y1 - 1, 2, K.IN_WINE_RACK)
    g.blit(4, 5, 1, K.IN_TABLE)
    g.blit(6, 5, 1, K.IN_TABLE)
    g.set(VISITORS_BOOK[0], VISITORS_BOOK[1], 3, K.INC_OPEN_BOOK)
    g.set(4, 5, 3, K.INC_DESK_BELL)
    g.set(7, 5, 3, K.INC_GOBLET)

    # The fire, the windows onto the snow, and the plate beside the fire.
    g.blit(9, y1 - 1, 2, K.IN_FIREPLACE)
    g.column(12, y1 - 2, 3, K.IN_WINDOW)
    g.column(15, y1 - 2, 3, K.IN_WINDOW)

    # Tables, with supper on them.
    for tx, ty, dish in [(5, 8, K.INC_MEAL), (11, 7, K.INC_MEAL2),
                         (11, 9, K.INC_BOTTLE)]:
        g.blit(tx, ty, 2, K.IN_TABLE)
        g.set(tx - 1, ty, 2, K.IN_STOOL)
        g.set(tx + 2, ty, 2, K.IN_STOOL)
        g.set(tx, ty, 3, dish)

    # Two beds by the east wall, and a rug in front of the fire.
    g.column(14, 6, 2, K.IN_BED)
    g.column(15, 6, 2, K.IN_BED_ORANGE)
    for x in range(9, 12):
        g.set(x, 5, 1, K.IN_RED_RUG)
    g.autotile(1)
    g.set(3, 10, 2, K.IN_CRATE)
    g.set(15, 10, 2, K.IN_BARREL)

    m = K.new_map(w, h, K.TS_INSIDE, name="The Eleven Days", bgm="Town3",
                  battleback=("Wood1", "Room1"))
    m["data"] = g.data
    m["events"] = [None] + eleven_days_events()
    return m


def eleven_days_events():
    evs = [S.exit_tile(1, "Inn Door", ELEVEN_ROOM[6], ELEVEN_ROOM[5] + 2,
                       MAP_FROSTWICK, ELEVEN_DOOR[0], ELEVEN_DOOR[1] + 1)]

    # 2: Mrs Marchpane, and a bed - `restwell.py`'s idiom, at eleven crowns.
    def beds(lines):
        stay = [R.lose_gold(11), R.fadeout_screen(), R.play_me("Inn1"),
                R.recover_all(), R.wait(90), R.fadein_screen()]
        stay += S.narrate([
            "You sleep under three quilts. In the morning",
            "it has snowed four inches, exactly, and not",
            "on the path."])
        cmds = S.say("Mrs Marchpane", lines)
        cmds += R.choice_block(
            ["Take a room (11cr)", "Not just now"],
            [R.if_then(R.condition_script("$gameParty.gold() >= 11"), stay,
                       S.say("Mrs Marchpane",
                             ["Eleven crowns, dear. It's",
                              "the name of the place."]))],
            cancel=None)
        return cmds

    first = S.say("Mrs Marchpane", [
        "Welcome, dears. The Eleven Days.",
        "Named for the thaw.",
        "Eleven days, it lasted."])
    first += S.narrate(["You ask what happened on the twelfth."])
    first += S.say("Mrs Marchpane", ["The meeting."])
    first += [R.self_switch("A", True)]
    first += beds(["Room's eleven crowns.",
                   "Snow's included."])
    later = beds(["Eleven crowns, dears.",
                  "Three quilts and a hot brick."])
    img = R.image("Gen_People3", 6, direction=2)
    evs.append(R.event(2, "Mrs Tibby Marchpane", *MARCHPANE, [
        R.page(first, img=img, trigger=0, priority=1),
        R.page(later, img=img, trigger=0, priority=1,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ]))

    # 3: the visitors' book signed by three Chosen Ones - mechanism four -
    # and the third signature, which is the one worth reading twice. The two
    # old ones are a century apart and too faded to have names, which is what
    # keeps them from disagreeing with anybody the game has numbered.
    book = S.narrate([
        "The visitors' book, open on the bar under a card:",
        "\\C[14]SIGNED BY THREE CHOSEN ONES. PLEASE ASK.\\C[0]"])
    book += S.narrate([
        "It is ruled NAME, FROM, WHITHER, and a fourth",
        "column in a newer hand: CHOSEN ONE (Y/N)."])
    book += S.narrate([
        "Two very old entries, a century apart, both",
        "bound north, both marked Y, the names faded out.",
        "One says 'Lovely weather.' The other says 'Cold.'"])
    book += S.narrate([
        "The third is forty years old: P. Stagg, of nowhere",
        "in particular, bound north. In the last column,",
        "in Mrs Marchpane's hand, a firm Y."])
    book += S.narrate([
        "Under the Y, rubbed out but not quite, smaller,",
        "and in his own hand: N."])
    book += [R.self_switch("A", True)]
    book_again = S.narrate([
        "SIGNED BY THREE CHOSEN ONES.",
        "You look at the third again. It is still, very",
        "faintly, an N."])
    page = dict(img=R.image(""), trigger=0, priority=1, direction_fix=True,
                through=True)
    evs.append(R.event(3, "The Visitors' Book", *VISITORS_BOOK, [
        R.page(book, **page),
        R.page(book_again, conditions={"selfSwitchValid": True,
                                       "selfSwitchCh": "A"}, **page),
    ]))

    # 4: the eleven days, commemorated - 7.3's mark on the wall at the height
    # the snow reached during them, which is the floor. It is the whole town
    # in one object and needs nobody to explain it.
    mark = S.narrate([
        "A brass plate beside the fire, polished to a",
        "shine, over a line painted along the skirting:",
        "",
        "   THE ELEVEN DAYS. SNOW DEPTH DURING: THIS HIGH."])
    mark += S.narrate(["The line is on the floor."])
    evs.append(R.event(4, "The Eleven Days (Plate)", *SNOW_MARK, [R.page(
        mark, img=R.image(""), trigger=0, priority=1, direction_fix=True)]))
    return evs


# ============================================== the room the committee meets in
#            w   h  x1  y1  x2  y2  door_x
GROUP_ROOM = (17, 13, 3, 4, 13, 9, 8)
TABLE_Y = 6
BLAGG = (5, 6)                  # at the head of the table
CLEM = (7, 7)
MEMBERS = [(7, 5), (9, 5), (10, 7)]
MINUTES = (8, 6)
REGISTER_X = 12                 # the bookcase, read from its foot
RIBBON_CASE = (4, 9)


def working_group_map():
    w, h, x1, y1, x2, y2, door_x = GROUP_ROOM
    g = K.interior(w, h, x1, y1, x2, y2, door_x=door_x,
                   floor=K.IN_PARQUET,
                   wall_top=K.IN_WALL_TOP_RED, wall_face=K.IN_WALL_FACE_RED)

    # The committee's table: two `Table A`s end to end, which seats six.
    g.blit(6, TABLE_Y, 2, K.IN_TABLE)
    g.blit(8, TABLE_Y, 2, K.IN_TABLE)
    g.set(MINUTES[0], MINUTES[1], 3, K.INC_SCROLL)
    g.set(6, TABLE_Y, 3, K.INC_BOOK)
    g.set(9, TABLE_Y, 3, K.INC_GOBLET)

    g.column(REGISTER_X, y1 - 1, 2, K.IN_BOOKSHELF)
    g.column(REGISTER_X + 1, y1 - 1, 2, K.IN_BOOKCASE)
    g.column(5, y1 - 2, 3, K.IN_WINDOW)
    g.column(9, y1 - 2, 3, K.IN_WINDOW)

    # The ribbon, in its case, on a table of its own.
    g.blit(RIBBON_CASE[0], RIBBON_CASE[1], 2, K.IN_TABLE)
    g.set(RIBBON_CASE[0], RIBBON_CASE[1], 3, K.INC_CASE)
    g.set(13, 9, 2, K.IN_CRATE)
    g.set(12, 9, 2, K.IN_CRATE2)

    m = K.new_map(w, h, K.TS_INSIDE, name="The Working Group", bgm="Town3",
                  battleback=("Wood1", "Room1"))
    m["data"] = g.data
    m["events"] = [None] + working_group_events()
    return m


def working_group_events():
    y1 = GROUP_ROOM[3]
    evs = [S.exit_tile(1, "Parish Door", GROUP_ROOM[6], GROUP_ROOM[5] + 2,
                       MAP_FROSTWICK, GROUP_DOOR[0], GROUP_DOOR[1] + 1)]

    # 2: Mrs Blagg, the premise made flesh - parish bureaucracy played
    # entirely straight. The curse is an asset.
    first = S.say("Mrs Blagg", [
        "Wilhelmina Blagg. Chair, Festival",
        "committee. You'll be here for the Festival."])
    first += S.narrate(["You ask, carefully, about the winter."])
    first += S.say("Mrs Blagg", [
        "The curse? It's an asset.",
        "Page one of the register.",
        "Depreciating at four per cent a year."])
    first += S.narrate(["You ask what it is depreciating towards."])
    first += S.say("Mrs Blagg", [
        "Spring, eventually.",
        "We've budgeted for it.",
        "The auditor called it forward-looking.",
        "He came in August. It was snowing.",
        "He was very impressed."])
    first += [R.self_switch("A", True)]
    later = S.say("Mrs Blagg", [
        "The minutes are on the table.",
        "Do read them. Clem has.",
        "Clem has read everything."])
    img = R.image("Gen_People3", 4, direction=6)
    evs.append(R.event(2, "Mrs Wilhelmina Blagg", *BLAGG, [
        R.page(first, img=img, trigger=0, priority=1),
        R.page(later, img=img, trigger=0, priority=1,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ]))

    # 3: Clem, aged seven - mechanism two, the leaky child, in company, at
    # volume. He thinks the subject is the lanterns. The room does the rest:
    # 1.3 item 6, the reaction shot, which is Perpetua's machinery.
    clem = S.say("Clem", [
        "Are you here for the lanterns?",
        "I do the lanterns. I'm seven."])
    clem += S.say("Clem", [
        "Nan says Mrs Stagg's never once been",
        "cold. Not in forty winters. Not once.",
        "And that's Mr Stagg, that is."])
    clem += S.say("Clem", [
        "I think it's his lanterns.",
        "He does ever such good lanterns."])
    clem += S.narrate([
        "Round the table, the committee finds the ceiling",
        "very interesting. Mrs Blagg finds it most",
        "interesting of all."])
    clem += [S.blush(), R.self_switch("A", True)]
    clem_again = S.say("Clem", [
        "I know all the minutes off by heart.",
        "Item three. The winter. CARRIED."])
    img = R.image("Gen_People3", 3, direction=8)
    evs.append(R.event(3, "Clem Blagg", *CLEM, [
        R.page(clem, img=img, trigger=0, priority=1),
        R.page(clem_again, img=img, trigger=0, priority=1,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ]))

    # 4: the minutes - mechanism four. A vote, a division, an abstention.
    minutes = S.narrate([
        "MINUTES OF THE WORKING GROUP ON THE WINTER.",
        "Extraordinary meeting, the twelfth day."])
    minutes += S.narrate([
        "Item 1. That the winter has stopped. Noted.",
        "Item 2. Takings, carols and lanterns, since:",
        "nil. Noted, with concern."])
    minutes += S.narrate([
        "Item 3. That a practitioner be retained to put it",
        "back, on a sensible footing.",
        "For, 41. Against, 3, who had planted peas.",
        "Carried."])
    minutes += S.narrate([
        "Item 4. That Mr Stagg be asked to open the first",
        "Festival. Carried unanimously, with one",
        "abstention: Mr Stagg."])
    minutes += [R.self_switch("A", True)]
    minutes_again = S.narrate([
        "Item 5. Any other business. The peas.",
        "Deferred."])
    page = dict(img=R.image(""), trigger=0, priority=1, direction_fix=True,
                through=True)
    evs.append(R.event(4, "The Minutes", *MINUTES, [
        R.page(minutes, **page),
        R.page(minutes_again, conditions={"selfSwitchValid": True,
                                          "selfSwitchCh": "A"}, **page),
    ]))

    # 5: the asset register. The fourth line is the committee's, and the
    # margin is Mrs Blagg's, and it is the kindest thing in the room.
    register = S.narrate([
        "THE PARISH OF FROSTWICK - REGISTER OF ASSETS.",
        "1. The Winter (maintained). Value: considerable.",
        "   Depreciation: four per cent.",
        "2. The Ribbon (one). 3. The Lanterns (212)."])
    register += S.narrate([
        "4. Mr Stagg - struck through, and in the margin:",
        "   'NOT AN ASSET. A PERSON. - W.B.'"])
    evs.append(R.event(5, "The Asset Register", REGISTER_X, y1, [R.page(
        register, img=R.image(""), trigger=0, priority=1,
        direction_fix=True)]))

    # 6: the ribbon. Forty Festivals and one ribbon.
    ribbon = S.narrate([
        "A gilt case on a table of its own, and in it a red",
        "ribbon, cut and tied again so often it is mostly",
        "knots. A card:",
        "   THE RIBBON. 40 FESTIVALS. 1 RIBBON."])
    evs.append(R.event(6, "The Ribbon", *RIBBON_CASE, [R.page(
        ribbon, **page)]))

    # 7-9: the committee, who are the reaction shot and say nothing else.
    for i, ((x, y), (sheet, index, facing)) in enumerate(zip(MEMBERS, [
            ("People1", 5, 2), ("People2", 1, 2), ("People3", 4, 4)])):
        says = S.narrate([
            "A member of the committee. They are reading",
            "the agenda with great attention, and do not",
            "look up."])
        evs.append(S.npc(7 + i, "Committee Member %d" % (i + 1), x, y, says,
                         sheet, index, direction=facing))
    return evs


# ============================================================ the cold room ==
#            w   h  x1  y1  x2  y2  door_x
COLD_ROOM_ = (15, 12, 3, 4, 11, 8, 7)
PARGETER = (8, 5)
SCHEDULE = (5, 6)
LARDER_X = 10


def cold_room_map():
    w, h, x1, y1, x2, y2, door_x = COLD_ROOM_
    g = K.interior(w, h, x1, y1, x2, y2, door_x=door_x,
                   floor=K.IN_COBBLE,
                   wall_top=K.IN_WALL_TOP_WHITE,
                   wall_face=K.IN_WALL_FACE_WHITE)

    # Her desk, and the schedule on it.
    g.blit(SCHEDULE[0], SCHEDULE[1], 2, K.IN_TABLE)
    g.set(SCHEDULE[0] - 1, SCHEDULE[1], 2, K.IN_STOOL)
    g.set(SCHEDULE[0], SCHEDULE[1], 3, K.INC_SCROLL)
    g.set(SCHEDULE[0] + 1, SCHEDULE[1], 3, K.INC_BOOK)

    # The larder, which is next January, and the rest of the trade.
    g.column(LARDER_X, y1 - 1, 2, K.IN_SHELF_BOTTLES)
    g.column(LARDER_X + 1, y1 - 1, 2, K.IN_BOOKSHELF)
    g.column(4, y1 - 2, 3, K.IN_WINDOW)
    g.set(3, y2, 2, K.IN_CRATE)
    g.set(4, y2, 2, K.IN_CRATE2)
    g.set(11, y2, 2, K.IN_BARREL2)
    for x in range(6, 9):
        g.set(x, 8, 1, K.IN_BLUE_RUG)
    g.autotile(1)

    m = K.new_map(w, h, K.TS_INSIDE, name="The Cold Room", bgm="Town3",
                  battleback=("Wood1", "Room1"))
    m["data"] = g.data
    m["events"] = [None] + cold_room_events()
    return m


def cold_room_events():
    y1 = COLD_ROOM_[3]
    evs = [S.exit_tile(1, "Cold Room Door", COLD_ROOM_[6], COLD_ROOM_[5] + 2,
                       MAP_FROSTWICK, COLD_DOOR[0], COLD_DOOR[1] + 1)]

    # 2: Eudora Pargeter, the retained practitioner. Not an ice witch. The
    # only person in the story who has read the contract, and the only one
    # with no feelings about the curse whatsoever - and so the one person in
    # this game who reads the Prophecy as a contract and says so.
    first = S.narrate([
        "A woman in pale blue and sensible spectacles,",
        "with her gloves on indoors, as a matter of course."])
    first += S.say("Pargeter", [
        "Pargeter. Retained practitioner.",
        "Before you ask: not an ice witch."])
    first += S.say("Pargeter", [
        "Refrigeration. Larders, dairies,",
        "the fishmonger's. The winter is one",
        "client. A good one."])
    first += S.narrate(["You ask how one makes a winter."])
    first += S.say("Pargeter", [
        "Same as a larder, only bigger, and",
        "with the door open. I do January in",
        "an afternoon. Home by four."])
    first += S.narrate([
        "You ask whether she minds keeping a town under",
        "a curse."])
    first += S.say("Pargeter", [
        "It isn't a curse, it's a contract.",
        "Nine years, renewed on time.",
        "I'd sign it again tomorrow."])
    prophecy = S.narrate([
        "You show her the Prophecy. She reads it all the",
        "way through, which nobody ever has."])
    prophecy += S.say("Pargeter", [
        "No break clause. No notice period.",
        "And clause twelve renews itself."])
    prophecy += S.say("Pargeter", [
        "I'd never sign a thing like that.",
        "Somebody's underlined it, I see.",
        "Somebody's worried."])
    # AUDIT.md item 6, C1, and TIMELINE.md: the one line in the game that
    # says what "every hundred years" means, which is how the published
    # south's Chosen Ones can be alive and the Tower 4,800 years old at once.
    # It is read, not explained - nobody here counts the south's ages for you.
    prophecy += S.narrate(["She turns back to clause two."])
    prophecy += S.say("Pargeter", [
        "'A hundred years' is a defined term.",
        "'Such period as the Committee shall",
        "find convenient.'"])
    first += R.if_then(R.condition_item(db.IT_PROPHECY), prophecy)
    first += [S.trope(), R.self_switch("A", True)]

    later = S.say("Pargeter", [
        "Light dusting Tuesday. For the look",
        "of the thing. It's in the schedule."])
    img = R.image("Gen_People3", 5, direction=2)
    evs.append(R.event(2, "Eudora Pargeter", *PARGETER, [
        R.page(first, img=img, trigger=0, priority=1),
        R.page(later, img=img, trigger=0, priority=1,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ]))

    # 3: the Schedule of Snowfalls - mechanism four, and 7.3's own list:
    # depth, duration, and a light dusting for the ribbon.
    sched = S.narrate([
        "CONTRACT FOR THE MAINTENANCE OF A WINTER.",
        "Appendix C: Schedule of Snowfalls."])
    sched += S.narrate([
        "Ordinary: four inches, overnight, not on market",
        "days. Blizzard: at the committee's request, in",
        "writing, one week's notice. Not during carols."])
    sched += S.narrate([
        "Festival Day: a light dusting, commencing at the",
        "ribbon, to settle on Mr Stagg's hat.",
        "Tolerance: plus or minus one flake."])
    page = dict(img=R.image(""), trigger=0, priority=1, direction_fix=True,
                through=True)
    evs.append(R.event(3, "The Schedule Of Snowfalls", *SCHEDULE, [R.page(
        sched, **page)]))

    # 4: the larder, which is where next winter is kept until it is wanted.
    larder = S.narrate([
        "Jars on a shelf, frosted over, in neat rows.",
        "The labels say JANUARY, and which week."])
    evs.append(R.event(4, "The Larder", LARDER_X, y1, [R.page(
        larder, img=R.image(""), trigger=0, priority=1,
        direction_fix=True)]))
    return evs


# ================================================================ the doors ==
def world_doors(base_id, cells):
    """The real doors into Frostwick, on the world map.

    `cells` is both squares `worldmap.json` put a placeholder on for this
    site - `Town B (Snow)` is two cells - handed in by `journey.world_map`.
    Player-touch and below characters, the world map's idiom."""
    evs = []
    for i, (x, y) in enumerate(sorted(cells)):
        arrive = S.narrate([
            "Frostwick. Snow on every roof, a lamp in every",
            "window, and a banner over the road:",
            "\\C[14]WINTER FESTIVAL - THE TWELFTH\\C[0]."])
        arrive += R.choice_block(
            ["Go in", "Press on"],
            [[R.play_se("Move1"),
              R.transfer(MAP_FROSTWICK, *ARRIVE, 4, 0)],
             S.narrate(["You press on. It begins, very precisely,",
                        "to snow."])])
        evs.append(R.event(base_id + i, SITE, x, y, [R.page(
            arrive, img=R.image(""), trigger=1, priority=0, through=True)]))
    return evs


def build():
    R.save_map(MAP_FROSTWICK, frostwick_map())
    R.save_map(MAP_ELEVEN_DAYS, eleven_days_map())
    R.save_map(MAP_WORKING_GROUP, working_group_map())
    R.save_map(MAP_COLD_ROOM, cold_room_map())
