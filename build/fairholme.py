"""Maps 35-37: Fairholme, Princess Rosamund's tower, and Mrs Emberthwaite's lair.

`../SITES.md` step 3. `../BIOS.md` is the bio: **Princess Rosamund of
Fairholme-on-Ransom**, kidnapped eleven times - twelve if you count the eagle,
which the Palace does not - who keeps a packed bag by the tower window. Her
father **King Aldous** posts the traditional reward every time, her hand or
half the kingdom, and every rescuer has very sensibly taken the half. The
dragon on the hill, **Mrs Emberthwaite**, is retired and widowed and wants
somebody to play cards with.

It is **two sites and one module**, because it is one bio: `Fairholme` is a
`Castle A` stamp, two cells wide, and `Mrs Emberthwaite's lair` is a `Cave A`
a few squares north-east of it. Both claims come from `SITES` below, the way
`hithermost.py` makes three.

* **No world-map coordinate is written here or in `places.py`.** The three
  door cells are handed in by `journey.world_map` off the placeholders they
  replace. `places.FAIRHOLME_STEP` and `places.LAIR_STEP` are the two squares
  this game chose, one south of each. `../WORLDMAP.md` 7.6.
* **The council is a room, not a conversation.** The table has had to be made
  larger, so it is three tables pushed end to end - a purple one, the red
  royal one, and a plain wooden one on the end that does not match - and it
  all but touches both walls. Round it: the King, nine heroes, two farmers, a
  man who was only passing, and an empty chair with a place card on it,
  because the knight is Sir Dunstable and it is a quarter past four.
* **The arithmetic is the joke's spine.** Eleven rescues at half the kingdom
  each leaves the King one two-thousand-and-forty-eighth; the two farmers are
  one rescue between them; and Mr Pilbeam, who was only passing, rescued her
  from the eagle. The Palace does not count the eagle, so the council cannot
  decide whether he holds a share, and until it does he cannot leave.
* **Nobody is unhappy** (`../NORTH.md` 1.2). The King is resigned and fond,
  Rosamund is organised, and the Budges are a good marriage. Mrs
  Emberthwaite's widowhood is Register B and is not a joke: it is Mr
  Emberthwaite's chair at the card table, which nobody sits in, and Rosamund
  pulling up the stool instead.
* **The Register A moment is the card in the bag** (`../NORTH.md` 1.3
  mechanism four: a document does not know what it is saying). It is the
  bio's own line - her dietary requirements, headed "for whoever it is this
  time" - and every word on it is about kidnappers and tea. Nobody reacts.
* **Tiles.** The King's portrait is `Portrait B`, which is a painted king, and
  Rosamund's is `Portrait A`. The bag is `Sack A`, the card `Note A (H)`, the
  cardigan `Women's Clothing A (Hanging)`, the minutes `Note C (H)`. The lair
  is the Dungeon tileset's Dirt Cave, and its card table, chair and stool are
  `Dungeon_C`'s. Mrs Emberthwaite is `$BigMonster2`'s red dragon, which is a
  whole-sheet character and faces down on its first row; no stock face sheet
  has a dragon on it, so she speaks with her name and no portrait.
"""
import mapkit as K
import rmmzdata as R

import story as S
import q_hob
from places import (MAP_WORLD, MAP_FAIRHOLME, MAP_ROSAMUND, MAP_LAIR,
                    FAIRHOLME_STEP, LAIR_STEP)

# The names `worldmap.json`'s door events carry. Two names, two claims.
CASTLE = "Fairholme"
LAIR = "Mrs Emberthwaite's lair"

# ---------------------------------------------------- the council chamber ---
#            w   h  x1  y1  x2  y2  door_x
ROOM = (23, 17, 2, 4, 20, 13, 11)
TABLE_Y = (8, 9)                # the table's two rows
NORTH_Y, SOUTH_Y = 7, 10        # the seats either side of it
SEATS = (5, 7, 9, 11, 13, 15, 17)
# The flight up to the tower, in the north-east corner, and the well it comes
# up into: Mike's Slain Wyvern stairs (`mapkit.stairs_up`, `stairwell`). Each
# column's middle tread goes up to the landing above the well's same column,
# and the well's top row comes down to the foot of the flight.
STAIRS_X = 19                   # the flight's west column; the east wall is 21
STAIRS_UP = 5                   # the middle tread
STAIRS_FOOT = 7
MINUTES = (10, 9)               # on the table, in front of the King
PLACE_CARD = (17, 8)            # in front of the empty chair

TABLE_A = K.sf_grid("Inside_B", "Table A", 2)
TABLE_C = K.sf_tile("Inside_B", "Table C")
TABLE_E = K.sf_tile("Inside_B", "Table E")
CHAIR = K.sf_block("Inside_B", "Chair A (Wood)")
CHAIR_STONE = K.sf_block("Inside_B", "Chair B (Stone)")
STOOL = K.sf_tile("Inside_B", "Stool B")
TAPESTRY = K.sf_block("Inside_B", "Tapestry A")
PORTRAIT_KING = K.sf_tile("Inside_B", "Portrait B")
PORTRAIT_GIRL = K.sf_tile("Inside_B", "Portrait A")
PLATE = K.sf_tile("Inside_C", "Plate A")
MUG = K.sf_tile("Inside_C", "Cup (Lower Left)")
TEAPOT = K.sf_tile("Inside_C", "Teapot A")
NOTE = K.sf_tile("Inside_C", "Note A (H)")
MINUTES_TILE = K.sf_tile("Inside_C", "Note C (H)")
SCROLLS = K.sf_tile("Inside_C", "Scrolls A")

# ------------------------------------------------------ Rosamund's tower ---
TOWER = (13, 13, 3, 4, 9, 8)    # w, h, x1, y1, x2, y2: no south door
TOWER_WELL = (8, 7)             # the well's west column and top row
TOWER_ARRIVE = 6                # the landing, above the well
BAG = (6, 4)                    # under the window
CARD = (8, 4)                   # on the table beside it
ROSAMUND_AT = (5, 6)
SACK = K.sf_tile("Inside_C", "Sack A")
BOOK = K.sf_tile("Inside_C", "Closed Book A (H)")
CARDIGAN = K.sf_tile("Inside_C", "Women's Clothing A (Hanging)")
WINDOW = K.sf_block("Inside_B", "Large Window B")
# Not `IN_DRESSER`, whose lower cell is `Sundries Shelf A` with the teddy
# bears painted on it. `Dresser` is a vanity with a mirror.
CLOSET = K.sf_block("Inside_B", "Closet")
DRESSER = K.sf_tile("Inside_B", "Dresser")

# --------------------------------------------------------------- the lair ---
LW, LH = 21, 17
MOUTH = [(9, LH - 1), (10, LH - 1), (11, LH - 1)]
LAIR_ARRIVE = (10, LH - 2)
DRAGON = (10, 7)
CARD_TABLE = (12, 7)
HIS_CHAIR = (12, 5)             # the back; the seat is (12, 6)
TABLET = (8, 13)

D_TABLE = K.sf_tile("Dungeon_C", "Table")
D_STOOL = K.sf_tile("Dungeon_C", "Stool")
D_CHAIR = K.sf_block("Dungeon_C", "Chair A (Wood)")
D_CLOCK = K.sf_block("Dungeon_C", "Clock")
D_CABINET = K.sf_block("Dungeon_C", "Dish Cabinet")
D_BOOKS = K.sf_block("Dungeon_C", "Bookshelf A")
D_TAPESTRY = K.sf_block("Dungeon_C", "Tapestry A")
GOLD_BIG = K.sf_grid("Dungeon_B", "Large Gold Mound", 2)
GOLD = K.sf_tile("Dungeon_B", "Gold Mound")
COINS = K.sf_tile("Dungeon_B", "Mound of Gold Coins")
POT = K.sf_tile("Dungeon_B", "Pot A")
STONE_TABLET = K.sf_tile("Dungeon_B", "Stone Tablet")
DAYLIGHT = K.sf_tile("Dungeon_B", "Light From Exit B (Bottom)")


# ================================================================ Fairholme ==
def council_map():
    w, h, x1, y1, x2, y2, door_x = ROOM
    g = K.interior(w, h, x1, y1, x2, y2, door_x=door_x,
                   floor=K.IN_DIAMOND_TILE,
                   wall_top=K.IN_WALL_TOP_GOLD,
                   wall_face=K.IN_WALL_FACE_GOLD)

    # The runner, from the door to the foot of the table.
    g.fill(door_x, SOUTH_Y + 1, door_x, y2 + 1, 1, K.IN_RED_CARPET)
    g.autotile(1)

    # The table, made larger: three tables end to end, none of them a match.
    # The purple one at the west end, the red royal one, and a plain wooden
    # one on the east end that was somebody's kitchen table last year.
    ty1, ty2 = TABLE_Y
    for y in (ty1, ty2):
        for x in (3, 4):
            g.set(x, y, 2, TABLE_E)
        for x in range(5, 16):
            g.set(x, y, 2, TABLE_C)
        g.blit(16, y, 2, TABLE_A)
        g.blit(18, y, 2, TABLE_A)

    # The chairs along the north side, the King's the stone one, and stools
    # along the south side, because there were not enough chairs.
    for x in SEATS:
        g.column(x, NORTH_Y - 1, 3, CHAIR_STONE if x == 11 else CHAIR)
        g.set(x, SOUTH_Y, 3, STOOL)

    # On the table: a place at every seat, and the minutes.
    for x in SEATS:
        g.set(x, ty1, 3, PLATE if x % 4 == 1 else MUG)
        g.set(x, ty2, 3, MUG if x % 4 == 1 else PLATE)
    g.set(*MINUTES, 3, MINUTES_TILE)
    g.set(*PLACE_CARD, 3, NOTE)
    g.set(8, ty2, 3, TEAPOT)
    g.set(14, ty1, 3, TEAPOT)
    g.set(4, ty1, 3, SCROLLS)
    g.set(19, ty2, 3, SCROLLS)

    # The north wall: the King and his daughter, two tapestries, and the
    # stairs up to the tower in the corner.
    g.set(10, y1 - 1, 3, PORTRAIT_KING)
    g.set(12, y1 - 1, 3, PORTRAIT_GIRL)
    g.column(6, y1 - 2, 3, TAPESTRY)
    g.column(16, y1 - 2, 3, TAPESTRY)
    g.column(3, y1 - 2, 3, K.IN_WINDOW)
    g.column(14, y1 - 2, 3, K.IN_WINDOW)
    K.stairs_up(g, STAIRS_X, y1, piers=(True, False))

    g.set(x1, y2, 3, K.INC_PLANT2)
    g.set(x2, y2, 3, K.INC_PLANT2)

    m = K.new_map(w, h, K.TS_INSIDE, name="Fairholme", bgm="Castle1")
    m["data"] = g.data
    m["events"] = [None] + council_events()
    return m


# (name, sheet, index, x, y, lines) for everybody round the table but the
# King. North side faces down, south side faces up. x=17 north is the empty
# chair and is not in this list.
SHAREHOLDERS = [
    ("Tamsin", "Actor1", 1, 5, NORTH_Y, [
        "Rescued her from a sorcerer,",
        "year before last. Lovely girl.",
        "Took the half, obviously."]),
    ("Brannoc", "Actor1", 2, 7, NORTH_Y, [
        "Item six is drainage.",
        "It is always drainage.",
        "I rescued her from a wyrm for",
        "the eastern marshes."]),
    ("Osric", "Actor1", 6, 9, NORTH_Y, [
        "Eleven rescues at half the",
        "kingdom each. The King's down",
        "to a two-thousand-and-",
        "forty-eighth."]),
    ("Aurel", "Actor2", 0, 13, NORTH_Y, [
        "I had a sorcerer.",
        "Everybody had a sorcerer.",
        "She'd packed a cardigan for",
        "the tower. It was a cold tower."]),
    ("Hild", "Actor2", 1, 15, NORTH_Y, [
        "I got a turnip field and the",
        "north bridge. The bridge is",
        "the troll's. We take turns."]),
    ("Morwen", "Actor2", 5, 5, SOUTH_Y, [
        "She met me at the door with",
        "her bag packed and a card.",
        "Nobody has ever been so",
        "pleased to see me. Or so ready."]),
    ("Kit", "Actor1", 3, 7, SOUTH_Y, [
        "I got the bit with the orchard.",
        "Worth it. She'd brought",
        "sandwiches, you know.",
        "For both of us."]),
    ("Leof", "Actor2", 6, 9, SOUTH_Y, [
        "My half came with a duck pond.",
        "The ducks have been very good",
        "about it."]),
    ("Valen", "Actor3", 2, 11, SOUTH_Y, [
        "The Guild's written to complain",
        "about Thursdays. If a princess",
        "won't be carried, what is a",
        "hero for? We're a bit lost."]),
    ("Mr Budge", "People2", 6, 13, SOUTH_Y, [
        "We were only mucking out.",
        "She come down the hill with a",
        "tin of cake, and we walked",
        "her home. That was all."]),
    ("Mrs Budge", "People4", 1, 15, SOUTH_Y, [
        "We got the half between us.",
        "Didn't know what to do with",
        "it. Put most of it back",
        "into the orchard."]),
]


def _tower_stairs(event_id, i):
    """Column i of the flight up: its middle tread, to the landing above the
    tower's well, facing up."""
    return R.event(event_id, "The Tower Stairs", STAIRS_X + i, STAIRS_UP, [
        R.page([R.play_se("Move1"),
                R.transfer(MAP_ROSAMUND, TOWER_WELL[0] + i, TOWER_ARRIVE, 8,
                           0)],
               img=R.image(""), trigger=1, priority=0, through=True)])


def _stairs_down(event_id, i):
    """Column i of the tower's well: its top row, to the foot of the flight
    in the council chamber, facing down."""
    return R.event(event_id, "The Stairs Down", TOWER_WELL[0] + i,
                   TOWER_WELL[1], [R.page(
                       [R.play_se("Move1"),
                        R.transfer(MAP_FAIRHOLME, STAIRS_X + i, STAIRS_FOOT,
                                   2, 0)],
                       img=R.image(""), trigger=1, priority=0, through=True)])


def council_events():
    w, h, x1, y1, x2, y2, door_x = ROOM
    evs = [S.exit_tile(1, "The Great Door", door_x, y2 + 2, MAP_WORLD,
                       *FAIRHOLME_STEP)]

    # 2: King Aldous, at the head of the table, which is the middle of it.
    king = S.say("King Aldous", [
        "Welcome to Fairholme.",
        "Are you here about the rescue?"])
    king += S.narrate(["You say you are only passing."])
    king += S.say("King Aldous", [
        "Only passing. Oh dear.",
        "That's how Mr Pilbeam started."])
    king += S.narrate([
        "At the far end of the table, a small man in a red robe",
        "and a crown waves, weakly."])
    king += S.say("King Aldous", [
        "Every time she's taken, I post",
        "the traditional reward.",
        "Her hand, or half the kingdom."])
    king += S.say("King Aldous", [
        "They all take the half.",
        "Every one. Very sensible.",
        "Nobody's fault.",
        "But there's only so much kingdom."])
    king += [S.trope(), R.self_switch("A", True)]
    again = S.say("King Aldous", [
        "If you do rescue her, take the",
        "half. Everybody does.",
        "We've a form."])
    img = R.image("Gen_People2", 2, direction=2)
    evs.append(q_hob.owned("aldous", R.event(2, "King Aldous", 11, NORTH_Y, [  # HOB-1
        R.page(king, img=img, trigger=0, priority=1),
        R.page(again, img=img, trigger=0, priority=1,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ])))

    # 3: the minutes, on the table in front of him, read from the south side.
    minutes = S.narrate([
        "\\C[14]MINUTES OF THE COUNCIL OF FAIRHOLME\\C[0]",
        "Present: HM the King; nine heroes; Mr & Mrs Budge;",
        "Mr Pilbeam (passing). Apologies: Sir Dunstable",
        "(in a mountain)."])
    minutes += S.narrate([
        "1. The table. To be lengthened again. Carried.",
        "2. Drainage.",
        "3. Drainage, continued.",
        "4. Drainage, continued."])
    minutes += S.narrate([
        "5. The eagle. The Palace does not count the eagle.",
        "   Whether Mr Pilbeam, who rescued Her Highness from",
        "   the eagle, therefore holds a share. Deferred.",
        "   Mr Pilbeam asks whether he may go. Deferred."])
    minutes += S.narrate([
        "6. Thursdays. Her Highness has been walking up the",
        "   hill on Thursdays, unaccompanied, and coming back.",
        "   The Heroes' Guild has written to complain. Noted.",
        "7. Drainage."])
    evs.append(R.event(3, "The Minutes", *MINUTES, [R.page(
        minutes, img=R.image(""), trigger=0, priority=1,
        direction_fix=True)]))

    # 4: the empty chair's place card, read from the empty chair.
    card = S.narrate([
        "A place card, in front of the one empty chair:",
        "",
        "   SIR DUNSTABLE OF THE VALE",
        "   One share. Back directly. - D."])
    evs.append(R.event(4, "Sir Dunstable's Place", *PLACE_CARD, [R.page(
        card, img=R.image(""), trigger=0, priority=1, direction_fix=True)]))

    # 5: the stairs up to the tower.
    # (the east column's is appended last, so no id moves).
    evs.append(_tower_stairs(5, 0))

    # 6: Mr Pilbeam, at the far end, on the table that does not match.
    pilbeam = S.say("Mr Pilbeam", [
        "I was only passing.",
        "There was an eagle.",
        "That was four years ago."])
    pilbeam += S.say("Mr Pilbeam", [
        "They haven't decided if the",
        "eagle counts. I can't go till",
        "they decide if the eagle counts."])
    pilbeam += S.narrate([
        "He looks at the door the way a man looks at a",
        "door he has been looking at for four years."])
    evs.append(S.npc(6, "Mr Pilbeam", 17, SOUTH_Y, pilbeam, "People4", 0,
                     direction=8))

    # 7-17: the rest of the shareholders.
    for i, (name, sheet, index, x, y, lines) in enumerate(SHAREHOLDERS):
        facing = 2 if y == NORTH_Y else 8
        evs.append(S.npc(7 + i, name, x, y, S.say(name, lines), sheet, index,
                         direction=facing))
    evs.append(_tower_stairs(len(evs) + 1, 1))
    return evs


# ========================================================= Rosamund's tower ==
def tower_map():
    w, h, x1, y1, x2, y2 = TOWER
    g = K.interior(w, h, x1, y1, x2, y2, floor=K.IN_WOOD_FLOOR,
                   wall_top=K.IN_WALL_TOP_STONE,
                   wall_face=K.IN_WALL_FACE_STONE)
    g.fill(4, 6, 6, 7, 1, K.IN_PURPLE_RUG)
    g.autotile(1)

    # The window, and under it the bag. Beside it, on the table, the book
    # and the card; the cardigan is hanging up ready on the wall above.
    g.column(BAG[0], y1 - 2, 3, WINDOW)
    g.set(*BAG, 3, SACK)
    g.blit(7, y1, 2, TABLE_A)
    g.set(7, y1, 3, BOOK)
    g.set(*CARD, 3, NOTE)
    g.set(8, y1 - 1, 3, CARDIGAN)

    g.column(x1, y1, 3, K.IN_BED)
    g.set(4, y1 - 1, 3, PORTRAIT_KING)
    g.column(x2, y1 - 1, 3, CLOSET)
    g.set(x2, 5, 3, DRESSER)
    K.stairwell(g, *TOWER_WELL, wall_top=K.IN_WALL_TOP_STONE,
                wall_face=K.IN_WALL_FACE_STONE, sides=(True, False))
    g.set(x1, y2, 3, K.INC_PLANT2)

    m = K.new_map(w, h, K.TS_INSIDE, name="Rosamund's Tower", bgm="Town3")
    m["data"] = g.data
    m["events"] = [None] + tower_events()
    return m


def tower_events():
    evs = [_stairs_down(1, 0)]

    # 2: Rosamund. The bio's own line first, then the Thursdays.
    rosa = S.say("Rosamund", [
        "Oh, are you the rescue? Lovely.",
        "Could you carry the cake tin?",
        "Mind the seventh stair,",
        "it's a trap."])
    rosa += S.say("Rosamund", [
        "The eighth is also a trap.",
        "The ninth is fine."])
    rosa += S.narrate(["You say you are not the rescue. You are only passing."])
    rosa += S.say("Rosamund", [
        "Oh! Well, that's a relief,",
        "honestly. It's Thursday."])
    rosa += S.say("Rosamund", [
        "I go up the hill on Thursdays.",
        "Mrs Emberthwaite does a lovely",
        "sponge, and she cheats at whist."])
    rosa += S.narrate(["You ask whether she is not afraid of the dragon."])
    rosa += S.say("Rosamund", [
        "Of Mrs Emberthwaite? She's",
        "seventy. The first time I was",
        "carried up there, she made up",
        "the spare room."])
    rosa += S.say("Rosamund", [
        "She said she hadn't had anybody",
        "to talk to since Mr Emberthwaite.",
        "So now I walk. It's quicker."])
    rosa += S.narrate([
        "Eleven times, she says, she has been kidnapped.",
        "Twelve, if you count the eagle, which the Palace",
        "does not."])
    rosa += [S.trope(), R.self_switch("A", True)]
    again = S.say("Rosamund", [
        "It's the bag by the window,",
        "if anybody asks. It is always",
        "the bag by the window."])
    img = R.image("Gen_People2", 3, direction=2)
    evs.append(R.event(2, "Princess Rosamund", *ROSAMUND_AT, [
        R.page(rosa, img=img, trigger=0, priority=1),
        R.page(again, img=img, trigger=0, priority=1,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ]))

    # 3: the bag.
    bag = S.narrate([
        "A travelling bag, packed and buckled, by the window.",
        "It has been packed for some time. It has the look of",
        "a bag that is never quite unpacked."])
    bag += S.narrate([
        "A book. A cardigan. Sandwiches, in greaseproof paper,",
        "made this morning. A second round of sandwiches,",
        "labelled OTHERS."])
    evs.append(R.event(3, "The Packed Bag", *BAG, [R.page(
        bag, img=R.image(""), trigger=0, priority=1, direction_fix=True)]))

    # 4: the card. Mechanism four: a document does not know what it is
    # saying, and nobody reacts to it.
    card = S.narrate([
        "A card on the table beside the bag, in a round,",
        "firm hand:"])
    card += S.narrate([
        "   \\C[14]FOR WHOEVER IT IS THIS TIME\\C[0]",
        "   No eels. No mushrooms. Nothing in aspic.",
        "   Tea at four, and not stewed."])
    card += S.narrate([
        "   I will not be carried unless there are stairs.",
        "   I would like to be home by Thursday.",
        "   Thank you so much for having me."])
    card += [S.blush()]
    evs.append(R.event(4, "The Card", *CARD, [
        R.page(card + [R.self_switch("A", True)], img=R.image(""), trigger=0,
               priority=1, direction_fix=True),
        R.page(card[:-1], img=R.image(""), trigger=0, priority=1,
               direction_fix=True,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ]))
    evs.append(_stairs_down(len(evs) + 1, 1))
    return evs


# ================================================================= the lair ==
def lair_map():
    w, h = LW, LH
    g = K.Canvas(w, h, tileset=K.TS_DUNGEON)
    g.fill(0, 0, w - 1, h - 1, 0, K.DG_WALL_TOP)
    g.fill(3, 4, 17, 11, 0, K.DG_FLOOR)         # the parlour
    g.fill(8, 12, 12, h - 1, 0, K.DG_FLOOR)     # the way in, to the mouth
    g.dungeon_walls(K.DG_WALL_TOP, K.DG_WALL_FACE)
    g.autotile(0)

    # The hoard, which is where she sleeps, at the back.
    g.blit(4, 4, 3, GOLD_BIG)
    g.set(6, 4, 3, GOLD)
    g.set(3, 6, 3, COINS)
    g.set(7, 5, 3, COINS)

    # The card table, with his chair drawn up to it and her visitor's stool.
    g.set(*CARD_TABLE, 3, D_TABLE)
    g.column(*HIS_CHAIR, 3, D_CHAIR)
    g.set(CARD_TABLE[0], CARD_TABLE[1] + 1, 3, D_STOOL)

    # The parlour: a dish cabinet, a clock, a shelf of books, a tapestry.
    g.column(14, 3, 3, D_CABINET)
    g.column(15, 3, 3, D_CLOCK)
    g.column(16, 3, 3, D_BOOKS)
    g.column(9, 2, 3, D_TAPESTRY)
    g.set(17, 11, 3, POT)
    g.set(3, 11, 3, POT)

    g.set(*TABLET, 3, STONE_TABLET)
    for x, y in MOUTH:
        g.set(x, y, 3, DAYLIGHT)

    m = K.new_map(w, h, K.TS_DUNGEON, name="Mrs Emberthwaite's Lair",
                  bgm="Town5", battleback=("Cave1", "Cave1"))
    m["data"] = g.data
    m["events"] = [None] + lair_events()
    return m


def lair_events():
    evs = []
    for i, cell in enumerate(MOUTH):
        evs.append(S.exit_tile(i + 1, "The Cave Mouth", *cell, MAP_WORLD,
                               *LAIR_STEP))

    # 4: the tablet at the door.
    tablet = S.narrate([
        "A stone tablet, carved deep, by the way in:",
        "",
        "   PLEASE WIPE YOUR FEET",
        "   NO RESCUES"])
    tablet += S.narrate([
        "Underneath, in chalk, more recently:",
        "",
        "   WHIST THURSDAYS. ALL WELCOME."])
    evs.append(R.event(4, "The Tablet", *TABLET, [R.page(
        tablet, img=R.image(""), trigger=0, priority=1, direction_fix=True)]))

    # 5: Mrs Emberthwaite.
    first = S.narrate([
        "A dragon, very large and very red, with a pair of",
        "reading spectacles on a chain round her neck."])
    first += S.say("Mrs Emberthwaite", [
        "Oh! A visitor. Come in,",
        "come in, mind the gold, it gets everywhere."])
    first += S.say("Mrs Emberthwaite", [
        "You're not a hero,",
        "are you, dear? Only I'm retired.",
        "I've had a letter."])
    first += S.narrate(["You say you are only passing."])
    first += S.say("Mrs Emberthwaite", [
        "Passing! Lovely.",
        "Do you play whist?"])
    play = S.narrate([
        "You play a hand of whist with a dragon. She wins it,",
        "by a margin that makes you check the deck.",
        "The deck is fine. It is you."])
    play += S.say("Mrs Emberthwaite", [
        "Don't feel bad, dear.",
        "Rosamund hasn't beaten me yet either."])
    teach = S.say("Mrs Emberthwaite", [
        "Oh, that's all right.",
        "I'll teach you. Rosamund didn't know either,",
        "the first time."])
    first += R.choice_block(["Deal me in", "I don't play"], [play, teach],
                            cancel=1)
    first += S.say("Mrs Emberthwaite", [
        "The first time they brought",
        "her up here, she had a bag packed and a card",
        "about her diet. I made up the spare room.",
        "I'd not had company in years."])
    first += S.say("Mrs Emberthwaite", [
        "Now she walks up",
        "on Thursdays, on her own two feet,",
        "with a cake tin.",
        "The heroes are furious."])
    first += [S.trope(), R.self_switch("A", True)]
    again = S.say("Mrs Emberthwaite", [
        "Thursdays, dear.",
        "Bring a cake tin, if you're coming."])
    img = R.image("$BigMonster2", 0, direction=2)
    page = dict(img=img, trigger=0, priority=1, direction_fix=True,
                step_anime=True)
    evs.append(R.event(5, "Mrs Emberthwaite", *DRAGON, [
        R.page(first, **page),
        R.page(again, conditions={"selfSwitchValid": True,
                                  "selfSwitchCh": "A"}, **page),
    ]))

    # 6: his chair. Register B, and not a joke: read from the seat's side.
    chair = S.narrate([
        "A big wooden chair drawn up to the card table,",
        "much sat in, once. There is a pipe on the seat."])
    chair += S.say("Mrs Emberthwaite", [
        "That's Mr Emberthwaite's.",
        "He did the roaring, mostly.",
        "I was always more of an indoor dragon."])
    chair += S.say("Mrs Emberthwaite", [
        "Rosamund asked whose it was,",
        "the first Thursday. She's never",
        "sat in it. She pulls up the stool."])
    evs.append(R.event(6, "Mr Emberthwaite's Chair", HIS_CHAIR[0],
                       HIS_CHAIR[1] + 1, [R.page(
                           chair, img=R.image(""), trigger=0, priority=1,
                           direction_fix=True)]))
    return evs


# ================================================================ the doors ==
def _castle_doors(base_id, cells):
    """The real doors into Fairholme. `Castle A` is two cells; both open onto
    the council chamber's great door."""
    evs = []
    for i, (x, y) in enumerate(sorted(cells)):
        arrive = S.narrate([
            "Fairholme-on-Ransom. A castle with a great many",
            "flags on it, no two of them the same."])
        arrive += R.choice_block(
            ["Go in", "Press on"],
            [[R.play_se("Move1"),
              R.transfer(MAP_FAIRHOLME, ROOM[6], ROOM[5], 8, 0)],
             S.narrate(["You press on. Somebody else will rescue her."])])
        evs.append(R.event(base_id + i, CASTLE, x, y, [R.page(
            arrive, img=R.image(""), trigger=1, priority=0, through=True)]))
    return evs


def _lair_doors(base_id, cells):
    """The cave on the hill, which has a doormat."""
    evs = []
    for i, (x, y) in enumerate(sorted(cells)):
        arrive = S.narrate([
            "A cave in the hillside, with smoke coming out of it",
            "the way smoke comes out of a kitchen.",
            "There is a doormat."])
        arrive += R.choice_block(
            ["Go in", "Press on"],
            [[R.play_se("Move1"),
              R.transfer(MAP_LAIR, LAIR_ARRIVE[0], LAIR_ARRIVE[1], 8, 0)],
             S.narrate(["You press on. It is not Thursday."])])
        evs.append(R.event(base_id + i, LAIR, x, y, [R.page(
            arrive, img=R.image(""), trigger=1, priority=0, through=True)]))
    return evs


# One claim per name the world map carries - `journey.world_map` merges this
# into its `claims` dict.
SITES = {
    CASTLE: _castle_doors,
    LAIR: _lair_doors,
}


def build():
    R.save_map(MAP_FAIRHOLME, council_map())
    R.save_map(MAP_ROSAMUND, tower_map())
    R.save_map(MAP_LAIR, lair_map())
