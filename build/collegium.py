"""Maps 58-60: the Collegium Arcanum - the Great Court, the Library, the Hall.

`../SITES.md` step 17. The source is `../COMPANIONS.md` L2 - "a university
that is entirely committee" - whose comedy is **institutional courtesy**:
nobody is ever rude, nothing is ever refused, everything is referred. The
Porter's Lodge holds the real power and knows it; the Library is where money
goes to die. Its two NPCs are **Sub-Librarian Prewitt**, immovable, courteous,
correct, who holds the largest number in the game, and **Dean Fenwold**, who
is fine, has a talk about it, and did not back her up once. This module builds
the places and the people and **not the quests**: ZEPH-1 is the fines, ZEPH-2
the duck's vote, ZEPH-3 the Dean's demonstration and WRE-1 the monograph, and
nothing here spends any of them.

* **The world-map door is claimed by name**, `journey.world_map`'s mechanism.
  The stamp is two cells of `School of Magic`, a cream-stone college of towers
  with purple spires, on open grass near the east coast with a dirt road
  ending at its door. Map 58 is the Great Court behind the gate: the Hall and
  the Library along its north side, the Porter's Lodge beside the gate, and a
  lawn in the middle that the public walks round. `places.py` has
  `COLLEGIUM_STEP`, the square south of the stamp's western cell, and no
  world coordinate.
* **Zephyrine in the party is a refusal at the world-map door.** She was
  expelled from here, and ZEPH-1 is her going back - so her walking in is the
  quest, and followers are drawn, so she cannot wait at the pond while her
  sprite follows you through the gate. There is no inner door to hang it on
  either: the Porter is standing in the gateway, and anybody who has met him
  would know her. She stops in the road, and nobody goes in. ZEPH-1 appends
  its own page after hers.
* **Wren in the Library is a reaction shot**, not WRE-1: the quest is her
  publication, and nothing has been submitted. At the shelf of the
  Collegium's monographs she finds a gap about an inch wide.
* **The duck is not here.** It is on its pond, step 7, four miles off; its
  chair at High Table is, with a cushion. Nothing mentions a vote.
* **One trope** - the ancient school of magic, whose motto is REFERATUR -
  **and no blush**: the place is courteous, not red.
"""
import os

import mapkit as K
import rmmzdata as R

import db
import q_wren
import q_zephyrine
import q_spare
import story as S
from places import (MAP_WORLD, MAP_COLLEGIUM, MAP_COLLEGIUM_LIBRARY,
                    MAP_COLLEGIUM_HALL, COLLEGIUM_STEP)

HERE = os.path.dirname(os.path.abspath(__file__))

# The name `worldmap.json`'s door events carry for this site - no "The".
SITE = "Collegium Arcanum"

# The character sheet `draw_art()` writes: Dean Fenwold's portrait, which no
# stock frame has in it. `!` - an object, no six-pixel lift.
PORTRAIT_SHEET = "!Collegium_Portrait"


def _pair(first, later):
    """A first conversation and the short one after it, on self switch A."""
    return first + [R.self_switch("A", True)], later


def _person(event_id, name, xy, img, first, later):
    return R.event(event_id, name, *xy, [
        R.page(first, img=img, trigger=0, priority=1),
        R.page(later, img=img, trigger=0, priority=1,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ])


PAGE = dict(img=R.image(""), trigger=0, priority=1, direction_fix=True)
LATER = {"selfSwitchValid": True, "selfSwitchCh": "A"}


# =========================================================== the Great Court ==
# The Hall and the Library along the north side, both facing south into the
# court, with round towers between and at either end. A paved court with a
# lawn in the middle of it. The south range faces outward on to the road -
# a building's only face is its south side - and the gate is a gap in it,
# with the Porter's Lodge the last building before it.
CW, CH = 33, 23
# `sf_grid` finds both records of that name - the 2x5 tower and, after it,
# the 2x1 piece that joins one to a wall - so only the first five rows.
TOWER = K.sf_grid("Outside_C", "Round Tower A (Castle)", 2)[:5]
# "All towers and purple spires", says the door: the sheet's green cone and
# its ring of battlements on the tower's lower three rows, six tall. It is
# purple on `TS_COLLEGIUM`, whose C sheet `draw_art()` recolours.
SPIRE = K.sf_grid("Outside_C", "Round Tower A (Castle's Spire)", 2) + TOWER[2:]
TOWER_XS = (1, 16, 30)
FOUNDER_STATUE = K.sf_block("Outside_C", "Statue B")  # 1x2, a wizard
HALL = (3, 1, 13, 7)            # x, y, w, h: front wall row is y + h - 1
LIBRARY = (18, 1, 12, 7)
HALL_DOOR = (9, 7)
LIBRARY_DOOR = (23, 7)
COURT = (1, 8, 31, 16)          # the paving, x1, y1, x2, y2
LAWN = (9, 10, 23, 14)
WEST_RANGE = (1, 17, 9, 4)
LODGE = (10, 17, 5, 4)
EAST_RANGE = (18, 17, 14, 4)
GATE_X = (15, 16, 17)
ROAD_Y = CH - 2                 # two rows of road outside the south range
ARRIVE = (16, ROAD_Y)

GEDGE = (15, 18)                # in the gateway, on the Lodge side of it
ARMS = (13, 20)                 # the crest over the Lodge window, read below
BOARD = (11, 20)                # the IN and OUT board, beside the window
LAWN_SIGN = (16, 15)            # on the paving at the south edge of the lawn
CONGREGATION = (27, 9)          # the notice board by the Library door
HAPGOOD = (5, 12)
FOUNDER = (16, 12)              # a wizard in stone, in the middle of the lawn

COURT_TREES = [(2, 9), (29, 9), (2, 15), (29, 15)]
ROAD_TREES = []


def court_map():
    w, h = CW, CH
    g = K.Canvas(w, h, tileset=K.TS_COLLEGIUM)
    g.fill(0, 0, w - 1, h - 1, 0, K.GRASS)
    x1, y1, x2, y2 = COURT
    g.fill(x1, y1, x2, y2, 0, K.PAVING)
    g.fill(*LAWN, 0, K.GRASS)
    # The gate passage, and the road outside.
    g.fill(GATE_X[0], y2 + 1, GATE_X[-1], ROAD_Y - 1, 0, K.PAVING)
    g.fill(0, ROAD_Y, w - 1, h - 1, 0, K.PATH)

    # Cream-coloured stone and purple roofs, as the door says and the stamp
    # on the world map shows.
    for b in (HALL, LIBRARY, WEST_RANGE, LODGE, EAST_RANGE):
        g.building(*b, wall=K.WALL_SANDBRICK, roof=K.ROOF_PURPLE)
    g.autotile(0)

    for x in TOWER_XS:
        g.blit(x, 2, 3, SPIRE)

    # The Hall's front: two tall stained-glass windows either side of the
    # door. The Library's: plain windows, all the way along.
    hy = HALL[1] + HALL[3] - 2
    for x in (5, 13):
        g.column(x, hy, 3, K.WINDOW_GLASS)
    for x in (7, 11):
        g.column(x, hy, 3, K.BANNER_PURPLE)
    fy = LIBRARY[1] + LIBRARY[3] - 1
    for x in (20, 26, 28):
        g.set(x, fy, 3, K.WINDOW)
    # The south range, seen from the road. The Lodge has its window and the
    # Collegium's arms over it; the ranges have windows.
    sy = LODGE[1] + LODGE[3] - 1
    for x in (3, 7, 12, 20, 24, 28):
        g.set(x, sy, 3, K.WINDOW)
    g.set(ARMS[0], sy - 1, 3, K.SIGN_SUN)

    for x, y in COURT_TREES + ROAD_TREES:
        g.blit(x, y - 1, 3, K.TREE)
    g.column(FOUNDER[0], FOUNDER[1] - 1, 3, FOUNDER_STATUE)
    g.set(*LAWN_SIGN, 3, K.FENCE_PANEL)
    g.set(*CONGREGATION, 3, K.FENCE_PANEL)
    lx1, ly1, lx2, ly2 = LAWN
    g.scatter([(lx1, ly1), (lx2, ly1), (lx1, ly2), (lx2, ly2)], 3,
              K.sf_tile("Outside_B", "Bush (Flowers)"))
    g.scatter([(4, 8), (6, 8), (12, 8), (14, 8), (19, 8), (21, 8),
               (25, 8), (29, 8)], 3, K.FLOWERS)

    m = K.new_map(w, h, K.TS_COLLEGIUM, name="The Great Court", bgm="Town2",
                  bgm_volume=60)
    m["data"] = g.data
    m["events"] = [None] + court_events()
    return m


def gedge_pages():
    first = S.narrate([
        "A large man in a dark suit and a ginger beard, standing in",
        "the gateway. He does not own it. He has the air of somebody",
        "who could, and has decided not to bother."])
    first += S.say("Mr Gedge", [
        "Afternoon. Gedge.",
        "Head Porter."])
    first += S.narrate(["You ask whether you might look round."])
    first += S.say("Mr Gedge", [
        "You'll want a",
        "visitor's pass. Issued by the Lodge, on",
        "the recommendation of a Fellow, and",
        "countersigned by the Lodge."])
    first += S.narrate(["You say that you do not know any Fellows."])
    first += S.say("Mr Gedge", [
        "Nobody does, sir.",
        "They don't come out."])
    first += S.say("Mr Gedge", [
        "I'll recommend you",
        "myself. There. And countersign it.",
        "There. And issue it. There."])
    first += S.narrate([
        "He writes on a card three times, in the same hand, and gives",
        "it to you. The whole thing has taken about four seconds."])
    first += S.say("Mr Gedge", [
        "The Master needs a",
        "meeting. The Dean needs a form. I need a",
        "pencil."])
    first += S.say("Mr Gedge", [
        "Hall's on the left,",
        "Library's on the right. Keep off the",
        "grass."])
    later = S.say("Mr Gedge", [
        "Keep to the path,",
        "sir. It goes round. Everything here",
        "does."])
    return _pair(first, later)


def arms_pages():
    first = S.narrate([
        "Over the Lodge window, the arms of the Collegium Arcanum,",
        "carved and gilded, and on a ribbon under them the motto:",
        "REFERATUR."])
    first += S.narrate([
        "Let it be referred.",
        "",
        "Six hundred years of the finest magical education in the",
        "land, and that is the part they put over the door."])
    first += [S.trope()]
    later = S.narrate(["REFERATUR. Let it be referred."])
    return _pair(first, later)


def board_pages():
    return S.narrate([
        "A board of names by the Lodge window, with a brass slide",
        "beside each one that says IN or OUT."]) + S.narrate([
        "THE MASTER: OUT. The slide has rusted there. Nobody is",
        "entirely sure who the Master is; it is thought to be a",
        "committee."]) + S.narrate([
        "THE DEAN: OUT. And under it, in the Porter's pencil,",
        "\"In Hall. Out to callers.\"",
        "THE SUB-LIBRARIAN: IN. THE HEAD PORTER: IN."])


def lawn_pages():
    return S.narrate([
        "THE GREAT COURT. The grass is reserved to Fellows of the",
        "Collegium. Members of the public are asked to keep to the",
        "path, which goes round."])


def congregation_pages():
    return S.narrate([
        "CONGREGATION. The next meeting will receive the minutes of",
        "the last meeting, which received the minutes of the one",
        "before."]) + S.narrate([
        "Item 2. That the matter of the Library roof be referred to",
        "the Committee for the Library Roof.",
        "Item 3. That the Committee for the Library Roof be referred",
        "back to Congregation, with thanks."])


def hapgood_pages():
    first = S.narrate([
        "A thin man in a gown, walking round the lawn quickly with",
        "a great many papers."])
    first += S.say("Dr Hapgood", [
        "Hapgood - Junior Fellow,",
        "twenty-two years. Can't stop, I'm taking",
        "this to the Bursar."])
    first += S.say("Dr Hapgood", [
        "The Bursar refers it",
        "to Estates, Estates refers it to the",
        "Junior Fellow, and the Junior Fellow",
        "takes it back to the Bursar."])
    first += S.narrate(["You ask what it is."])
    first += S.say("Dr Hapgood", [
        "A request for",
        "somebody to carry things. It's been",
        "going round since March."])
    later = S.say("Dr Hapgood", [
        "Once more round! Nearly",
        "there. Never there."])
    return _pair(first, later)


def founder_pages():
    first = S.narrate([
        "THE FOUNDER. A wizard in stone, in a pointed hat, holding up",
        "his staff, in the middle of the lawn. The plinth says that",
        "he founded the Collegium in one afternoon, by himself."])
    first += S.narrate([
        "Underneath, smaller, it says that everything since has been",
        "done by committee, and that a committee is considering the",
        "plinth."])
    first += S.narrate([
        "You have read it standing on the grass. Somewhere behind",
        "you, in the gateway, somebody clears his throat."])
    later = S.narrate([
        "The Founder, alone, in one afternoon. You are on the grass",
        "again. The throat, in the gateway, again."])
    return _pair(first, later)


def court_events():
    evs = []
    # 1-3: the road back out, all three cells of it, below characters.
    for i, x in enumerate(GATE_X):
        evs.append(R.event(i + 1, "The Road Out", x, CH - 1, [R.page(
            [R.play_se("Move1"), R.transfer(MAP_WORLD, *COLLEGIUM_STEP, 2, 0)],
            img=R.image(""), trigger=1, priority=0, through=True)]))

    # 4, 5: the Hall door and the Library door.
    evs.append(S.door(4, "The Hall", *HALL_DOOR, MAP_COLLEGIUM_HALL,
                      HALL_DOOR_X, HALL_ROOM[3] + 1, direction=8))
    evs.append(S.door(5, "The Library", *LIBRARY_DOOR, MAP_COLLEGIUM_LIBRARY,
                      LIBRARY_DOOR_X, LIBRARY_ROOM[3] + 1, direction=8))

    # 6: Mr Gedge, in the gateway.
    gedge = _person(6, "Mr Gedge", GEDGE,
                    R.image("Gen_People5", 5, direction=2), *gedge_pages())
    gedge["pages"].append(q_zephyrine.gedge_page(gedge["pages"][-1]))  # ZEPH-1
    evs.append(gedge)

    # 7: the arms over the Lodge window, 8: the IN and OUT board. Both are on
    # the Lodge's lower wall row and read from the road below it.
    first, later = arms_pages()
    evs.append(R.event(7, "The Arms", *ARMS, [
        R.page(first, **PAGE), R.page(later, conditions=LATER, **PAGE)]))
    board = R.event(8, "In and Out", *BOARD, [R.page(board_pages(), **PAGE)])
    board["pages"].append(q_zephyrine.board_page(board["pages"][0]))  # ZEPH-1
    evs.append(S.pin_note(board))                   # the board, on the wall

    # 9: keep off the grass, 10: Congregation's notices.
    evs.append(R.event(9, "The Lawn", *LAWN_SIGN,
                       [R.page(lawn_pages(), **PAGE)]))
    notice = R.event(10, "Congregation", *CONGREGATION,
                     [R.page(congregation_pages(), **PAGE)])
    notice["pages"] += q_zephyrine.notice_pages(notice["pages"][0])  # ZEPH-2
    evs.append(notice)

    # 11: Dr Hapgood, going round the lawn.
    hapgood = _person(11, "Dr Hapgood", HAPGOOD,
                      R.image(*S.FACES["Dr Hapgood"], direction=2), *hapgood_pages())
    last = hapgood["pages"][-1]
    hapgood["pages"].append(q_zephyrine.hapgood_page(last))  # ZEPH-3
    hapgood["pages"].append(q_zephyrine.hapgood_senior_page(last))  # ZEPH-2
    evs.append(hapgood)

    # 12: the Founder, read from the grass round him - which is the joke.
    first, later = founder_pages()
    evs.append(R.event(12, "The Founder", *FOUNDER, [
        R.page(first, **PAGE), R.page(later, conditions=LATER, **PAGE)]))
    evs.append(q_spare.courier("collegium", 12, 21))               # SPA-1
    return evs


# =============================================================== the Library ==
# A long panelled room. Sub-Librarian Prewitt's desk is just inside the door,
# with the Register on it; bookcases the whole length of the north wall, two
# rows of free-standing stacks down the middle, and a reading table in the
# west end with a reader at it who has been waiting since Michaelmas.
LW, LH = 26, 16
#               x1 y1  x2  y2
LIBRARY_ROOM = (2, 4, 23, 12)
LIBRARY_DOOR_X = 6

TABLE_A = K.sf_block("Inside_B", "Table A")          # two cells, left/right
TABLE_D = K.sf_tile("Inside_B", "Table D")
STOOL = K.sf_tile("Inside_B", "Stool A")
CHAIR = K.sf_block("Inside_B", "Chair A (Wood)")     # 1x2, faces south only
BASIN = K.sf_tile("Inside_B", "Basin")
NOTICE = K.sf_tile("Inside_B", "Posted Notice")
PORTRAIT = K.sf_tile("Inside_B", "Portrait B")      # a bearded old man
TAPESTRY = K.sf_block("Inside_B", "Tapestry A")      # 1x2, on the wall face
LEDGER = K.sf_tile("Inside_C", "Closed Books C")
OPEN_BOOK = K.sf_tile("Inside_C", "Open Book A (H)")
HOURGLASS = K.sf_tile("Inside_C", "Hourglass")
POT_PLANT = K.sf_tile("Inside_C", "Potted Plant B")  # violets; A is a cactus

DESK = [(3, 7), (4, 7), (5, 7)]
PREWITT = (4, 6)
REGISTER = (5, 7)               # the ledger on the desk, read from below
PENNOCK = (6, 7)                # ZEPH-1: the Registrar's clerk, desk's end
REVIEWERS = [(5, 10), (2, 10)]  # WRE-1: Mott and Furze, either end of the table
SUBSCRIPTION_LIST = (4, 7)      # WRE-1: on the desk, by the hourglass
APPEAL = (3, 3)                 # a notice on the wall face, read from below
APPEAL_BUCKET = (2, 4)
MONOGRAPHS = 8                  # a Bookshelf A against the north wall
NORTH_CASES = range(10, 24, 2)  # Bookshelf B, 2x2, along the north wall
STACK_XS = (10, 12, 14, 17, 19, 21)
STACK_ROWS = (7, 10)            # the top row of each run of stacks
READING = [(3, 10), (4, 10)]
READER = (3, 11)
GLOBE = (23, 12)


def library_map():
    x1, y1, x2, y2 = LIBRARY_ROOM
    g = K.interior(LW, LH, x1, y1, x2, y2, door_x=LIBRARY_DOOR_X,
                   floor=K.IN_PARQUET, wall_top=K.IN_WALL_TOP_PLANK,
                   wall_face=K.IN_WALL_FACE_PLANK)
    # A runner down the long walk behind the stacks.
    g.fill(8, 5, x2, 5, 1, K.IN_RED_CARPET)
    g.autotile(1)

    # The north wall: the monographs, then bookcases to the end.
    g.column(MONOGRAPHS, y1 - 1, 2, K.IN_BOOKSHELF)
    for x in NORTH_CASES:
        g.column(x, y1 - 1, 2, K.IN_BOOKCASE)
        g.column(x + 1, y1 - 1, 2, K.IN_BOOKCASE2)
    # The stacks: runs of 2x2 bookcases standing free, with an aisle between.
    for y in STACK_ROWS:
        for x in STACK_XS:
            g.column(x, y, 2, K.IN_BOOKCASE)
            g.column(x + 1, y, 2, K.IN_BOOKCASE2)

    # Prewitt's desk, with the Register on it, and the Appeal on the wall.
    for x, y in DESK:
        g.set(x, y, 2, TABLE_D)
    g.set(*REGISTER, 3, LEDGER)
    g.set(DESK[0][0], DESK[0][1], 3, HOURGLASS)
    g.set(*APPEAL, 2, NOTICE)
    g.set(*APPEAL_BUCKET, 3, BASIN)

    # The reading table, and the book the reader has not got.
    for (x, y), t in zip(READING, TABLE_A):
        g.set(x, y, 2, t)
    g.set(*READING[1], 3, OPEN_BOOK)
    g.set(x1 + 5, y2, 3, POT_PLANT)
    g.set(*GLOBE, 3, K.INC_BELL)                     # `INC_BELL` is a Globe

    m = K.new_map(LW, LH, K.TS_INSIDE, name="The Library", bgm="Town2",
                  bgm_volume=40, battleback=("Wood1", "Room1"))
    m["data"] = g.data
    m["events"] = [None] + library_events()
    return m


def prewitt_pages():
    first = S.narrate([
        "A woman in a navy jacket and a tie, at a desk with nothing",
        "on it but an hourglass and a very large ledger."])
    first += S.say("Prewitt", [
        "Good afternoon.",
        "Prewitt, Sub-Librarian. How may the",
        "Library help you?"])
    first += S.narrate(["You ask whether you might borrow a book."])
    first += S.say("Prewitt", [
        "Of course. You'll",
        "need a reader's ticket. The Library",
        "issues them on a letter from a Fellow."])
    first += S.narrate(["You show her Mr Gedge's card."])
    first += S.say("Prewitt", [
        "Mr Gedge is not a",
        "Fellow. Mr Gedge is a great deal more",
        "than a Fellow, and the Library cannot",
        "accept his letters on that account."])
    first += S.narrate(["You ask whether that is a no."])
    first += S.say("Prewitt", [
        "Oh, it is never a",
        "no. Nothing here is ever a no. It is",
        "\"not from this desk\"."])
    first += S.say("Prewitt", [
        "I can refer you to",
        "the Committee for Readers. It meets in",
        "the Library, so its members must all",
        "hold a reader's ticket."])
    first += S.narrate([
        "She says it kindly, and correctly, and she does not move",
        "at all."])
    later = S.say("Prewitt", [
        "Not from this desk.",
        "But I can refer you, which is very",
        "nearly the same, and takes longer."])
    return _pair(first, later)


def register_pages():
    first = S.narrate([
        "THE REGISTER OF OUTSTANDING FINES, on a pile of lesser",
        "registers. It is the size of a gravestone, and it has a",
        "brass clasp, which is locked."])
    first += S.say("Prewitt", [
        "I'm afraid the",
        "Register is confidential. It is also",
        "very heavy. Mr Gedge lifts it for me on",
        "Mondays."])
    first += S.narrate(["You ask how much is in it."])
    first += S.say("Prewitt", [
        "Most of it is in one",
        "account, and I really couldn't say",
        "whose. It is the largest number I have",
        "ever written down."])
    first += S.say("Prewitt", [
        "I write it down",
        "again every morning, with the day's",
        "interest. It has never once been wrong."])
    later = S.narrate([
        "The Register. The clasp is locked. It is probably heavier",
        "than it was this morning."])
    return _pair(first, later)


def appeal_pages():
    return S.narrate([
        "THE LIBRARY APPEAL - FOR THE ROOF.",
        "Raised this year: 1,412 crowns.",
        "Spent on the Appeal this year: 1,412 crowns.",
        "The Library thanks you for your interest."]) + S.narrate([
        "Under it, on the floor, a bucket, catching something."])


def monograph_pages():
    shelf = S.narrate([
        "MONOGRAPHS OF THE COLLEGIUM, in order of publication. On",
        "the Habits of the Lesser Wyvern. The Lesser Wyvern,",
        "Revisited. The Lesser Wyvern: A Reply To My Critics."])
    # Wren in the party is a reaction shot, not WRE-1: nothing has been
    # submitted, and nobody has asked her.
    wren = S.narrate([
        "Wren runs a finger along the shelf, and stops at a gap",
        "between two volumes. It is about an inch wide. She looks at",
        "it for some time."])
    wren += S.say("Wren", ["There's room."])
    wren += S.narrate([
        "She says nothing else, and walks on, and looks back once."])
    return shelf + R.if_then(R.condition_actor_in_party(db.WREN), wren)


def reader_pages():
    first = S.narrate([
        "A young man at the reading table, with an open book in",
        "front of him that is not the one he wants."])
    first += S.say("Reader", [
        "I asked for a book",
        "at Michaelmas. It's been referred."])
    first += S.narrate(["You ask where to."])
    first += S.say("Reader", [
        "To the shelf it's",
        "on. They say it's a very long way."])
    later = S.say("Reader", [
        "Any day now. It's",
        "been referred."])
    return _pair(first, later)


def library_events():
    x1, y1, x2, y2 = LIBRARY_ROOM
    evs = [R.event(1, "The Door", LIBRARY_DOOR_X, y2 + 2, [R.page(
        [R.play_se("Move1"),
         R.transfer(MAP_COLLEGIUM, LIBRARY_DOOR[0], LIBRARY_DOOR[1] + 1, 2,
                    0)],
        img=R.image(""), trigger=1, priority=0, through=True)])]
    prewitt = _person(2, "Prewitt", PREWITT,
                      R.image("Gen_People5", 6, direction=2), *prewitt_pages())
    prewitt["pages"] += q_zephyrine.prewitt_pages(prewitt["pages"][-1])  # ZEPH-1
    evs.append(prewitt)
    first, later = register_pages()
    register = R.event(3, "The Register", *REGISTER, [
        R.page(first, **PAGE), R.page(later, conditions=LATER, **PAGE)])
    register["pages"].append(q_zephyrine.register_page(register["pages"][-1]))  # ZEPH-1
    evs.append(register)
    appeal = R.event(4, "The Appeal", *APPEAL, [R.page(appeal_pages(), **PAGE)])
    appeal["pages"].append(q_zephyrine.appeal_page(appeal["pages"][0]))  # ZEPH-2
    evs.append(appeal)
    shelf = R.event(5, "The Monographs", MONOGRAPHS, y1,
                    [R.page(monograph_pages(), **PAGE)])
    shelf["pages"] += q_wren.shelf_pages(shelf["pages"][0])  # WRE-1
    evs.append(shelf)
    evs.append(_person(6, "Reader", READER, R.image(*S.FACES["Reader"], direction=8),
                       *reader_pages()))
    # 7: ZEPH-1's Registrar's clerk, at the east end of the desk, from the
    # Library's eleventh notice on.
    evs.append(q_zephyrine.pennock_event(7, *PENNOCK))
    # 8, 9: WRE-1's reviewers at the reading table; 10: the subscription
    # list, on Prewitt's desk by the hourglass.
    evs += q_wren.reviewer_events(8, REVIEWERS)
    evs.append(q_wren.subscription_event(10, *SUBSCRIPTION_LIST))
    return evs


# ================================================================== the Hall ==
# High Table across the north end under the portraits of the Deans, with the
# Duck's chair at the end of it; two long tables below it for everybody
# else, and an aisle down the middle from the door.
HW, HH = 24, 17
#            x1 y1  x2  y2
HALL_ROOM = (2, 4, 21, 13)
HALL_DOOR_X = 11

TABLE_E = K.sf_tile("Inside_B", "Table E")           # the purple cloth
HIGH_TABLE = range(8, 16)
HIGH_TABLE_Y = 6
DUCK_CHAIR = 16                 # its seat is (16, 6), read from below
LONG_TABLES = [(range(4, 10), 9), (range(13, 19), 9),
               (range(4, 10), 12), (range(13, 19), 12)]
FENWOLD = (6, 5)
FENWOLD_PORTRAIT = 5
FIRST_DEAN = 3
TALK_POSTER = 19
UNDERGRADUATE = (14, 10)


def hall_map():
    x1, y1, x2, y2 = HALL_ROOM
    g = K.interior(HW, HH, x1, y1, x2, y2, door_x=HALL_DOOR_X,
                   floor=K.IN_DIAMOND_TILE, wall_top=K.IN_WALL_TOP_STONE,
                   wall_face=K.IN_WALL_FACE_STONE)
    # A red runner up the aisle from the door to High Table.
    g.fill(HALL_DOOR_X, 7, HALL_DOOR_X + 1, y2, 1, K.IN_RED_CARPET)
    g.autotile(1)

    # The arms over High Table, and the Deans either side of them.
    g.column(11, y1 - 2, 2, TAPESTRY)
    g.column(12, y1 - 2, 2, TAPESTRY)
    for x in (FIRST_DEAN, 18):
        g.set(x, y1 - 1, 2, PORTRAIT)
    g.set(TALK_POSTER, y1 - 1, 2, NOTICE)
    g.set(20, y1 - 1, 2, PORTRAIT)

    # High Table, with its chairs behind it, and the Duck's at the end.
    for x in HIGH_TABLE:
        g.set(x, HIGH_TABLE_Y, 2, TABLE_E)
        g.column(x, y1, 2, CHAIR)
    g.column(DUCK_CHAIR, HIGH_TABLE_Y - 1, 2, CHAIR)
    # The long tables, stools on the north side of each.
    for xs, y in LONG_TABLES:
        for x in xs:
            g.set(x, y, 2, TABLE_A[(x - xs[0]) % 2])
            if (x - xs[0]) % 2 == 0:
                g.set(x, y - 1, 2, STOOL)
    g.set(x1, y2, 3, POT_PLANT)
    g.set(x2, y2, 3, POT_PLANT)

    m = K.new_map(HW, HH, K.TS_INSIDE, name="The Hall", bgm="Town2",
                  bgm_volume=50, battleback=("Wood1", "Room1"))
    m["data"] = g.data
    m["events"] = [None] + hall_events()
    return m


def fenwold_pages():
    first = S.narrate([
        "A tall man in the Collegium's white-and-purple robe, with a",
        "magnificent moustache, standing under a portrait of",
        "himself and looking at it with approval."])
    first += S.say("Dean Fenwold", [
        "Ah! Visitors.",
        "Fenwold. Dean. I'm fine, thank you."])
    first += S.narrate(["You had not asked."])
    first += S.say("Dean Fenwold", [
        "People do. They've",
        "been asking for eleven years. I do a",
        "talk about it now."])
    first += S.say("Dean Fenwold", [
        "\"The Man Who Was",
        "Fine.\" Forty-one engagements. They",
        "laugh in all the right places."])
    first += S.narrate(["You ask what happened."])
    first += S.say("Dean Fenwold", [
        "An incident. A",
        "very gifted young woman, a very small",
        "room, and rather more fire than the",
        "room had been told about."])
    first += S.say("Dean Fenwold", [
        "The eyebrows grew",
        "back. Magnificently, I'm told."])
    first += S.narrate(["He smooths one."])
    first += S.say("Dean Fenwold", [
        "She said the room",
        "was wrong, you know. At the time. I",
        "remember thinking she was very",
        "probably right."])
    first += S.narrate([
        "There is a short pause. It has been in the talk forty-one",
        "times, and it has never once been there on purpose."])
    first += S.say("Dean Fenwold", [
        "Well! It's a very",
        "good talk. Thursday week, in Hall."])
    later = S.say("Dean Fenwold", [
        "Fine! Still fine.",
        "Thursday week, if you're about."])
    return _pair(first, later)


def portrait_pages(x):
    if x == FENWOLD_PORTRAIT:
        return S.narrate([
            "DEAN FENWOLD. Painted after the incident. The painter was",
            "asked to be accurate about the eyebrows, and then, on",
            "reflection, to be a little less accurate."])
    return S.narrate([
        "THE FIRST DEAN. A card tucked into the frame says that the",
        "portrait is hung pending the approval of the Hanging",
        "Committee. It has been pending for five hundred years."])


def duck_chair_pages():
    first = S.narrate([
        "At the end of High Table, set a little apart from the",
        "others, a chair with a cushion on it."])
    first += S.narrate([
        "A card in front of it says: RESERVED. HONORARY FELLOW.",
        "There is a dent in the cushion, and in the dent, a",
        "feather."])
    later = S.narrate([
        "The Honorary Fellow's chair. The feather is still there.",
        "Nobody would dream of moving it."])
    return _pair(first, later)


def poster_pages():
    return S.narrate([
        "THURSDAY WEEK, IN HALL.",
        "\"THE MAN WHO WAS FINE\" - an evening with the Dean.",
        "Light refreshments. Questions afterwards, if nice.",
        "Tickets from the Lodge."])


def undergraduate_pages():
    first = S.say("Undergraduate", [
        "Dinner's at seven.",
        "Grace is at six. It's a long grace."])
    first += S.say("Undergraduate", [
        "It's been referred",
        "to a committee for shortening. Since",
        "before I came up."])
    later = S.say("Undergraduate", [
        "Six to seven. Every",
        "night. Still referred."])
    return _pair(first, later)


def hall_events():
    x1, y1, x2, y2 = HALL_ROOM
    evs = [R.event(1, "The Door", HALL_DOOR_X, y2 + 2, [R.page(
        [R.play_se("Move1"),
         R.transfer(MAP_COLLEGIUM, HALL_DOOR[0], HALL_DOOR[1] + 1, 2, 0)],
        img=R.image(""), trigger=1, priority=0, through=True)])]
    dean = _person(2, "Dean Fenwold", FENWOLD,
                   R.image("Gen_People5", 7, direction=8), *fenwold_pages())
    dean["pages"] += q_zephyrine.fenwold_pages(dean["pages"][-1])  # ZEPH-3
    evs.append(dean)
    # 3, 4: the portraits, on the lower row of the wall face, read from the
    # floor below them - like the Talk's poster, 6.
    evs.append(R.event(3, "The First Dean", FIRST_DEAN, y1 - 1,
                       [R.page(portrait_pages(FIRST_DEAN), **PAGE)]))
    # Dean Fenwold's is drawn, so it is an event on the wall face itself,
    # read from the floor below it like Fenmarch's.
    portrait = R.event(4, "Dean Fenwold's Portrait", FENWOLD_PORTRAIT, y1 - 1,
                       [R.page(portrait_pages(FENWOLD_PORTRAIT),
                               img=R.image(PORTRAIT_SHEET, 0, direction=2),
                               trigger=0, priority=1, direction_fix=True)])
    portrait["pages"].append(q_zephyrine.portrait_page(portrait["pages"][0]))  # ZEPH-3
    evs.append(portrait)
    first, later = duck_chair_pages()
    chair = R.event(5, "The Honorary Fellow's Chair", DUCK_CHAIR,
                    HIGH_TABLE_Y, [R.page(first, **PAGE),
                                   R.page(later, conditions=LATER, **PAGE)])
    chair["pages"] += q_zephyrine.chair_pages(chair["pages"][-1])  # ZEPH-2
    evs.append(chair)
    evs.append(R.event(6, "The Talk", TALK_POSTER, y1 - 1,
                       [R.page(poster_pages(), **PAGE)]))
    lad = _person(7, "Undergraduate", UNDERGRADUATE,
                  R.image(*S.FACES["Undergraduate"], direction=2),
                  *undergraduate_pages())
    lad["pages"].append(q_zephyrine.undergraduate_page(lad["pages"][-1]))  # ZEPH-3
    assert lad["id"] == q_zephyrine.UNDERGRADUATE_EVENT
    evs.append(lad)
    return evs


# ================================================================== the art ==
def draw_art():
    """Writes `PORTRAIT_SHEET`: Dean Fenwold, painted after the incident.

    Not part of the data build, like `fenmarch.draw_art()`, whose idiom this
    is: run this module to redraw it. The frame is `Inside_B`'s `Portrait B`
    with its sitter painted out, and the Dean is his own walking sprite,
    facing out, on the Collegium's purple."""
    import sys
    sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "chargen"))
    import numpy as np
    import png
    game = os.path.join(HERE, "..")

    tid = PORTRAIT_B
    sheet = png.read(os.path.join(game, "img", "tilesets", "Inside_B.png"))
    x = ((tid // 128) % 2 * 8 + tid % 8) * 48
    y = ((tid % 256) // 8 % 16) * 48
    f = sheet[y:y + 48, x:x + 48].astype(float)
    x0, y0, x1, y1 = 11, 9, 37, 40
    f[y0:y1, x0:x1] = (70, 40, 96, 255)

    chars = png.read(os.path.join(game, "img", "characters",
                                  "Gen_People5.png"))
    i = 7                                   # Dean Fenwold, facing down
    bx, by = (i % 4) * 144, (i // 4) * 192
    fig = chars[by + 4:by + 40, bx + 48 + 6:bx + 48 + 42].astype(float)
    # Nearest-neighbour up to the canvas, the top of him only: a portrait.
    h, w = y1 - y0, x1 - x0
    ys = (np.arange(h + 4) * fig.shape[0] / (h + 4)).astype(int)[:h]
    xs = (np.arange(w) * fig.shape[1] / w).astype(int)
    fig = fig[ys][:, xs]
    al = fig[..., 3:4] / 255
    d = f[y0:y1, x0:x1]
    d[..., :3] = fig[..., :3] * al + d[..., :3] * (1 - al)

    out = np.zeros((384, 576, 4))
    for r in range(4):
        for c in range(3):
            out[r * 48:(r + 1) * 48, c * 48:(c + 1) * 48] = f
    path = os.path.join(game, "img", "characters", PORTRAIT_SHEET + ".png")
    png.write(path, np.clip(out, 0, 255).round().astype(np.uint8))
    print("wrote", os.path.normpath(path))
    draw_tileset()


# The Collegium's C sheet: `Outside_C` with the green roof, its hip and valley
# pieces, its roof detail, and the green `Castle's Spire` turned purple. Only
# the green in those cells moves - the spire's stone ring stays stone.
PURPLE_HUE = 272        # degrees: the lavender of the world-map stamp's roofs
PURPLE_SAT = 0.55       # of the green's saturation - the full value is magenta
PURPLE_CELLS = ([(c, r) for r in (0, 1) for c in range(8, 13)]
                + [(c, 2) for c in range(8, 11)] + [(12, 6)]
                + [(c, r) for r in (8, 9, 10) for c in (12, 13)])


def draw_tileset():
    """Writes `img/tilesets/Outside_C_Collegium.png`, and its `.txt` with the
    recoloured records renamed, for `mapkit.TS_COLLEGIUM`. Not part of the
    data build: run this module to redraw it."""
    K.recolour_sheet("Outside_C", "Outside_C_Collegium", PURPLE_CELLS,
                     (55, 185), PURPLE_HUE, PURPLE_SAT,
                     [("Green Tile", "Purple Tile"), ("緑瓦", "紫瓦"),
                      ("Castle's Spire", "Castle's Purple Spire")])


# `Inside_B`'s `Portrait B`, the gilt frame, by its index on the sheet.
PORTRAIT_B = 133


# ================================================================== the door ==
def world_doors(base_id, cells):
    """The real door into the Collegium Arcanum, on the world map.

    `cells` is the two squares `worldmap.json` put placeholders on for this
    site - the lower half of the `School of Magic` stamp - handed in by
    `journey.world_map`. Player-touch and below characters, the world map's
    idiom for a place you walk into.

    **With Zephyrine in the party it is a refusal.** She was expelled from
    here, and ZEPH-1 is her going back, so her walking in is the quest; and
    followers are drawn, so she cannot wait outside. She stops in the road,
    and nobody goes in. ZEPH-1 appends its own page after these three."""
    zeph = {"actorValid": True, "actorId": db.ZEPH}
    evs = []
    for i, (x, y) in enumerate(sorted(cells)):
        arrive = S.narrate([
            "A college of cream-coloured stone, all towers and purple",
            "spires, with a gate in the middle of it and a large man",
            "standing in the gate."])
        arrive += R.choice_block(
            ["Go in at the gate", "Press on"],
            [[R.transfer(MAP_COLLEGIUM, *ARRIVE, 8, 0)],
             S.narrate(["You press on. Somewhere inside, a bell rings",
                        "for something, and then for something else."])])
        stop = S.narrate([
            "A college of cream-coloured stone, all towers and purple",
            "spires. Zephyrine has stopped in the road."])
        stop += S.say("Zephyrine", ["No."])
        stop += S.narrate(["You have not said anything yet."])
        stop += S.say("Zephyrine", [
            "I was expelled.",
            "From there. By them. They were very",
            "clear about it. Everybody in there is",
            "FINE, and they can stay fine."])
        stop += S.narrate([
            "Nobody argues. She walks the next mile with her hat pulled",
            "down, and does not once look back at the towers, which",
            "takes some doing: they are visible for most of it."])
        stop += [R.self_switch("A", True)]
        again = S.say("Zephyrine", ["Still no."])
        touch = dict(img=R.image(""), trigger=1, priority=0, through=True)
        evs.append(R.event(base_id + i, SITE, x, y, [
            R.page(arrive, **touch),
            R.page(stop, conditions=zeph, **touch),
            R.page(again, conditions=dict(zeph, selfSwitchValid=True,
                                          selfSwitchCh="A"), **touch),
        ] + q_zephyrine.door_pages(                                # ZEPH-1
            [R.transfer(MAP_COLLEGIUM, *ARRIVE, 8, 0)]) + [
            q_zephyrine.duck_door_page(                             # ZEPH-2
                [R.transfer(MAP_COLLEGIUM, *ARRIVE, 8, 0)])]))
    return evs


def build():
    R.save_map(MAP_COLLEGIUM, court_map())
    R.save_map(MAP_COLLEGIUM_LIBRARY, library_map())
    R.save_map(MAP_COLLEGIUM_HALL, hall_map())


if __name__ == "__main__":
    draw_art()
