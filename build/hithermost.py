"""Maps 33-34: Hithermost, and the Chapel of Continuance.

`../SITES.md` step 2, and the third of the world map's sites to get something
behind its doors. `../BIOS.md` is the bio: **Brother Quillon**, Keeper of the
Record, and the Book on his lectern that travellers sign "in case of
misfortune" before they go through the door into the mountain - and then,
quite often, come back in through the porch and sign again.

It is **three sites and one module**. The world map stacks them up the pass in
column 30 - Hithermost at the bottom, the chapel above it, the Door into the
Mountain at the top - and each carries its own name, so `journey.world_map`
has three claims to make. It takes them from `SITES` below, a name-to-builder
dict, rather than from a single `SITE` string as `penultima.py` and
`restwell.py` export.

* **No world-map coordinate is written here or in `places.py`.** The four
  door cells - `Village A` is two wide - are handed in by `journey.world_map`
  off the placeholders they replace. `places.HITHERMOST_STEP` is the one square
  this game chose: under all three, where the village road and the chapel
  porch both come back out. `../WORLDMAP.md` 7.6.
* **The Book is a save point**, which is the whole of the chapel: the joke and
  the mechanic are the same object. Travellers sign it in case of misfortune;
  so does the player, and the player also comes back in through the porch and
  signs it again. Its third page is the bio's own line, "Again? Of course."
* **The Door into the Mountain stays a door.** It is the obvious future
  dungeon, so it is a refusal with a reason - no lamp, because Sir Dunstable
  has it - and nothing here assumes what is behind it. On the world map it
  says the same thing and does not transfer anywhere. Its "Not yet." is a
  promise Mike chose to keep (`../AUDIT.md` D6), and `../COMPANIONS.md`
  section 8 is where it is owed.
* **The Register A moment is the Book** (`../NORTH.md` 1.3 mechanism four: a
  document does not know what it is saying). The page opens on a crowd of one
  - Sir Dunstable, all the way down - and the newly-married Tolleys are further
  down it, apologising. Every word of it is about people dying in a mountain
  and being very polite about it. Quillon does not react, because not reacting
  is the whole of his character.
* **Tiles.** There is no lectern, candle or pew on the Inside sheets by those
  names. The altar is `Church Table`, which has its candles painted on; the
  pews are `Table A`, two cells of low plain wood that reads as a bench; the
  lectern is `Table D` with the Book open on it. The Door into the Mountain is
  `Outside_C`'s `Mine Entrance`, a timbered mouth set into the cliff face, and
  the cliffs are `Ledge B (Dirt)` - rock, not the meadow ledge `CLIFF_TOP` is.
"""
import mapkit as K
import rmmzdata as R

import story as S
import q_hob
from places import MAP_WORLD, MAP_HITHERMOST, MAP_CONTINUANCE, HITHERMOST_STEP

# The names `worldmap.json`'s door events carry. Three names, three claims.
VILLAGE = "Hithermost"
CHAPEL = "Chapel of Continuance"
MOUNTAIN = "The Door into the Mountain"

# ------------------------------------------------------------ the village ---
HW, HH = 26, 34
MASS = K.A(117)                 # Ledge B (Dirt): the top of the rock
FACE = K.A(125)                 # and its face, which `dungeon_walls` finds
GROUND = K.A(25)                # Grass (Dirt): the same family as the rock
ROAD = K.A(26)                  # Road (Dirt)
ROAD_X = 14                     # the road up the pass: columns 14 and 15

GATE = [(ROAD_X, HH - 1), (ROAD_X + 1, HH - 1)]
ARRIVE = (ROAD_X, HH - 2)

# The chapel, on the terrace at the top of the pass. A building's only face is
# its south side, and every front below opens onto the one open slope, so no
# doorstep here is in a pocket.
CHAPEL_B = (4, 7, 9, 6)
CHAPEL_DOOR = (8, CHAPEL_B[1] + CHAPEL_B[3] - 1)
CHAPEL_OUT = (CHAPEL_DOOR[0], CHAPEL_DOOR[1] + 1)
HOUSES = [(3, 16, 6, 5), (3, 24, 7, 5), (18, 14, 6, 5), (18, 23, 5, 5)]

# The Door into the Mountain: `Mine Entrance`, two cells, set into the two
# rows of cliff face above the top of the road.
MINE = K.sf_block("Outside_C", "Mine Entrance")
MOUNTAIN_AT = (17, 5)           # the lower, open cell of the entrance

SIGN_AT = (13, 30)
NOTICE_AT = (11, 14)            # the chapel's board, below the path to its door

# ------------------------------------------------------------- the chapel ---
#            w   h  x1  y1  x2  y2  door_x
ROOM = (15, 17, 3, 4, 11, 13, 7)
LECTERN = (7, 7)
QUILLON = (7, 6)
DUNSTABLE = (5, 12)

TABLE_D = K.sf_tile("Inside_B", "Table D")
CUP = K.sf_tile("Inside_C", "Cup (Lower Left)")
RECORDS = K.sf_tile("Inside_C", "Closed Books C")
ALTAR = K.sf_grid("Inside_C", "Church Table", 3)
STATUE = K.sf_block("Inside_C", "Goddess Statue")
SYMBOL = K.sf_block("Inside_C", "Church Symbol")


# ============================================================== the village ==
def hithermost_map():
    w, h = HW, HH
    g = K.Canvas(w, h)
    g.fill(0, 0, w - 1, h - 1, 0, GROUND)

    # The pass: rock across the top, rock down both sides, a shoulder of it
    # into the top right and the bottom two corners, and the road the only
    # way through the bottom.
    g.fill(0, 0, w - 1, 5, 0, MASS)
    g.fill(0, 6, 1, h - 1, 0, MASS)
    g.fill(w - 2, 6, w - 1, h - 1, 0, MASS)
    g.fill(21, 6, 23, 8, 0, MASS)
    g.fill(2, h - 3, 5, h - 1, 0, MASS)
    g.fill(20, h - 3, 23, h - 1, 0, MASS)
    g.fill(6, h - 2, ROAD_X - 1, h - 1, 0, MASS)
    g.fill(ROAD_X + 2, h - 2, 19, h - 1, 0, MASS)

    g.fill(ROAD_X, 6, ROAD_X + 1, h - 1, 0, ROAD)
    g.fill(ROAD_X + 2, 6, MOUNTAIN_AT[0], 6, 0, ROAD)
    g.fill(CHAPEL_OUT[0], CHAPEL_OUT[1], ROAD_X - 1, CHAPEL_OUT[1], 0, ROAD)
    g.fill(10, 21, ROAD_X - 1, 21, 0, ROAD)

    g.dungeon_walls(MASS, FACE)

    g.building(*CHAPEL_B, wall=K.WALL_STONE_WHITE, roof=K.ROOF_GREEN)
    walls = [K.WALL_TIMBER, K.WALL_PLASTER, K.WALL_PLANK, K.WALL_STONE]
    for (x, y, bw, bh), wall in zip(HOUSES, walls):
        g.building(x, y, bw, bh, wall=wall, roof=K.ROOF_BROWN)
    g.autotile(0)

    # Trees along the tops of the rock, so the heights either side of the
    # pass read as wooded ridges rather than as a flat plain of dirt. Only
    # where a whole two-by-two is rock top - never on a face.
    def top(x, y):
        return R.autotile_kind(g.get(x, y, 0)) == R.autotile_kind(MASS)
    for y in range(0, h - 1, 2):
        for x in range(y // 2 % 2, w - 1, 2):
            if all(top(x + dx, y + dy) for dx in (0, 1) for dy in (0, 1)):
                g.blit(x, y, 3, K.TREE)

    # The door into the mountain, in the cliff face at the top of the road.
    g.column(MOUNTAIN_AT[0], MOUNTAIN_AT[1] - 1, 3, MINE)

    # The chapel: two tall stained windows either side of the door, and a
    # chimney, because Brother Quillon makes a great deal of tea.
    g.column(CHAPEL_DOOR[0] - 2, CHAPEL_DOOR[1] - 1, 3, K.WINDOW_GLASS)
    g.column(CHAPEL_DOOR[0] + 2, CHAPEL_DOOR[1] - 1, 3, K.WINDOW_GLASS)
    g.set(CHAPEL_B[0] + 6, CHAPEL_B[1], 2, K.STOVEPIPE)

    # The houses: a shut door and a window on each, and one sign - Hithermost
    # does teas, because people keep coming back down.
    for i, (x, y, bw, bh) in enumerate(HOUSES):
        fy = y + bh - 1
        g.column(x + 2, fy - 1, 3, K.DOOR_SHUT)
        g.set(x + 4, fy, 3, K.WINDOW)
        g.set(x + 1, y, 2, K.STOVEPIPE)
    g.set(HOUSES[2][0] + 1, HOUSES[2][1] + HOUSES[2][3] - 1, 3, K.SIGN_PLATE)

    boulder = K.sf_tile("Outside_B", "Boulder A")
    rocks = K.sf_tile("Outside_B", "Rocks")
    g.set(*SIGN_AT, 3, K.SIGNPOST)
    g.set(*NOTICE_AT, 3, K.SIGNPOST)
    g.scatter([(11, 20)], 3, K.TUB)                     # `Well`, and it is one
    g.scatter([(2, 7), (3, 13), (22, 10), (9, 30), (19, 29), (3, 22)],
              3, boulder)
    g.scatter([(16, 9), (12, 16), (7, 22), (17, 31), (20, 20), (10, 26)],
              3, rocks)
    g.scatter([(9, 21), (21, 19), (8, 29)], 3, K.BARREL)
    g.scatter([(2, 15), (23, 21), (12, 28)], 3, K.BUSH)
    g.scatter([(5, 14), (9, 14), (20, 28), (16, 21)], 3, K.FLOWERS2)
    g.scatter([(19, 11), (7, 30)], 3, K.LOGS)
    for x, y in [(2, 9), (22, 12), (10, 23), (16, 25)]:
        g.blit(x, y, 3, K.TREE)

    m = K.new_map(w, h, K.TS_OUTSIDE, name="Hithermost", bgm="Town2")
    m["data"] = g.data
    m["events"] = [None] + hithermost_events()
    return m


def door_into_the_mountain():
    """What the Door into the Mountain says, here and on the world map."""
    cmds = S.narrate([
        "\\C[14]THE DOOR INTO THE MOUNTAIN\\C[0]. A timbered mouth",
        "in the rock, and past it a stair going down into",
        "a dark that does not stop."])
    cmds += S.narrate([
        "A board is nailed to the frame:",
        "",
        "   NO ADMITTANCE WITHOUT A LAMP. BY ORDER.",
        "   LAMP ON HOOK."])
    cmds += S.narrate([
        "There is a hook under the board. There is no lamp",
        "on the hook. Chalked beside it, in a cheerful hand:",
        "",
        "   'Borrowed lamp. Back directly. - D.'"])
    cmds += S.narrate(["You have no lamp. You do not go in. Not yet."])
    return cmds


def hithermost_events():
    evs = []

    # 1-2: the road back down, both columns of it.
    for i, cell in enumerate(GATE):
        evs.append(S.exit_tile(i + 1, "The Road Down", *cell, MAP_WORLD,
                               *HITHERMOST_STEP))

    # 3: the sign at the foot of the village.
    sign = S.narrate([
        "\\C[14]HITHERMOST\\C[0]",
        "The last village before the mountain."])
    sign += S.narrate([
        "Underneath, added later and in smaller letters:",
        "",
        "   AND, FOR SOME, THE FIRST ONE AFTER IT."])
    sign += [S.trope()]
    evs.append(R.event(3, "The Village Sign", *SIGN_AT, [R.page(
        sign, img=R.image(""), trigger=0, priority=1, through=True,
        direction_fix=True)]))

    # 4: the chapel.
    evs.append(S.door(4, "Chapel of Continuance", *CHAPEL_DOOR,
                      MAP_CONTINUANCE, ROOM[6], ROOM[5]))

    # 5: the chapel's board.
    notice = S.narrate([
        "\\C[14]CHAPEL OF CONTINUANCE\\C[0]",
        "Keeper of the Record: Br. Quillon",
        "",
        "SERVICES: CONTINUOUS"])
    notice += S.narrate([
        "Travellers are asked to sign the Book before",
        "proceeding into the mountain, and again on the",
        "way back, if applicable, and again after that."])
    evs.append(R.event(5, "The Chapel Board", *NOTICE_AT, [R.page(
        notice, img=R.image(""), trigger=0, priority=1, through=True,
        direction_fix=True)]))

    # 6: the Door into the Mountain. Same as characters and player-touch, so
    # walking into it is what reads it and nobody ends up standing in it.
    evs.append(R.event(6, "The Door into the Mountain", *MOUNTAIN_AT, [R.page(
        door_into_the_mountain(), img=R.image(""), trigger=1, priority=1,
        direction_fix=True)]))

    # 7: somebody who lives here, by the well.
    local = S.say("Villager", [
        "Hithermost. Last village before",
        "the mountain."])
    local += S.narrate(["You ask what is after the mountain."])
    local += S.say("Villager", [
        "Hithermost, mostly.",
        "They come back down, you see.",
        "We do teas."])
    local += S.narrate(["You ask who comes back down."])
    local += S.say("Villager", [
        "Most of them. The knight, every day.",
        "Quarter past four, regular as a clock.",
        "Lovely manners. Has our lamp."])
    local += [S.trope(), R.self_switch("A", True)]
    again = S.say("Villager", [
        "If you're going up, sign the Book.",
        "Everybody does. Some of them twice."])
    evs.append(q_hob.owned("hithermost", S.npc(                    # HOB-1
        7, "A Villager", 12, 21, local, "People1", 0,
        direction=2, pages=[R.page(
            again, img=R.image("People1", 0, direction=2),
            trigger=0, priority=1,
            conditions={"selfSwitchValid": True,
                        "selfSwitchCh": "A"})])))
    return evs


# ============================================================== the chapel ==
def chapel_map():
    w, h, x1, y1, x2, y2, door_x = ROOM
    g = K.interior(w, h, x1, y1, x2, y2, door_x=door_x,
                   floor=K.IN_COBBLE, floor_alt=K.IN_DIAMOND_TILE,
                   wall_top=K.IN_WALL_TOP_WHITE,
                   wall_face=K.IN_WALL_FACE_WHITE)

    # The aisle, from the porch to the lectern. Layer 1 is the corpus's
    # floor-art layer, which is where a runner goes.
    g.fill(door_x, LECTERN[1] + 1, door_x, y2 + 1, 1, K.IN_RED_CARPET)
    g.autotile(1)

    # The altar, with its candles painted on, the symbol and two statues,
    # and two tall windows in the north wall.
    g.blit(6, y1, 3, ALTAR)
    g.column(4, y1, 3, STATUE)
    g.column(10, y1, 3, STATUE)
    g.column(5, y1 - 2, 3, K.IN_STAINED_GLASS)
    g.column(9, y1 - 2, 3, K.IN_STAINED_GLASS)

    # The lectern and the Book on it; beside it, the tea. Two cells, a table
    # each on layer 2 and the thing on it on layer 3.
    g.set(LECTERN[0], LECTERN[1], 2, TABLE_D)
    g.set(LECTERN[0], LECTERN[1], 3, K.INC_OPEN_BOOK)
    g.set(LECTERN[0] + 1, LECTERN[1], 2, TABLE_D)
    g.set(LECTERN[0] + 1, LECTERN[1], 3, CUP)

    # The Record: every Book before this one, which is forty years of it.
    # Two one-wide shelves down each side wall. They were the two halves of
    # one `Bookshelf B`, stood one above the other.
    for x in (x1, x2):
        g.column(x, 6, 3, K.IN_BOOKSHELF)
        g.column(x, 8, 3, K.IN_BOOKSHELF)
    g.set(4, 7, 2, TABLE_D)
    g.set(4, 7, 3, RECORDS)

    # Two rows of pews each side of the aisle.
    for y in (9, 11):
        g.blit(4, y, 2, K.IN_TABLE)
        g.blit(9, y, 2, K.IN_TABLE)

    g.set(x1, y2, 3, K.INC_PLANT2)
    g.set(x2, y2, 3, K.INC_PLANT2)

    m = K.new_map(w, h, K.TS_INSIDE, name="Chapel of Continuance",
                  bgm="Scene4", battleback=("Temple", "Temple"))
    m["data"] = g.data
    m["events"] = [None] + chapel_events()
    return m


def chapel_events():
    evs = [S.exit_tile(1, "The Porch", ROOM[6], ROOM[5] + 2,
                       MAP_HITHERMOST, *CHAPEL_OUT)]

    # 2: the Book. Three pages: the first time, when it is read and signed;
    # after it has been read and not signed; and after it has been signed,
    # when Quillon says the bio's line. Signing is the save screen.
    def sign(opening):
        write = S.narrate(["You write your name in the Book."])
        write += [R.open_save_screen(), R.self_switch("A", True)]
        cmds = opening
        cmds += R.choice_block(
            ["Write your name", "Not just now"],
            [write, S.say("Quillon", ["Of course. It will be here."])],
            cancel=1)
        return cmds

    read = S.narrate([
        "The Book lies open on the lectern, and it glows:",
        "a soft, even light with nothing to account for it."])
    read += S.narrate([
        "The page is in a great many hands. Most of them",
        "are the same hand."])
    read += S.narrate([
        "  Sir Dunstable of the Vale. Just in case.",
        "  Sir Dunstable of the Vale. Just in case.",
        "  Sir Dunstable of the Vale. Just in case.",
        "  Sir Dunstable of the Vale. Just in case."])
    read += S.narrate([
        "  Mr & Mrs Tolley, just married. In case.",
        "  Mr & Mrs Tolley. Again. So sorry, Brother.",
        "  Mr & Mrs Tolley. Again!",
        "  Sir Dunstable of the Vale. Just in case."])
    read += S.narrate([
        "Brother Quillon's smile does not change. It is the",
        "smile of a man not reacting to anything."])
    read += [S.blush(), R.self_switch("B", True)]
    read += S.say("Quillon", [
        "Welcome, traveller.",
        "Will you write your name in the Book?",
        "In case of misfortune."])

    unsigned = S.say("Quillon", [
        "Welcome, traveller.",
        "Will you write your name in the Book?"])

    signed = S.say("Quillon", [
        "Welcome, traveller.",
        "Will you write your name in the Book?"])
    signed += S.narrate([
        "He looks down at the page, where your name",
        "already is."])
    signed += S.say("Quillon", ["...Again? Of course."])
    signed += S.say("Quillon", ["Of course you will."])

    page = dict(img=R.image(""), trigger=0, priority=1, direction_fix=True)
    evs.append(R.event(2, "The Book", *LECTERN, [
        R.page(sign(read), **page),
        R.page(sign(unsigned), conditions={"selfSwitchValid": True,
                                           "selfSwitchCh": "B"}, **page),
        R.page(sign(signed), conditions={"selfSwitchValid": True,
                                         "selfSwitchCh": "A"}, **page),
    ]))

    # 3: Brother Quillon, behind the lectern. The vows forbid exactly one
    # thing, and he has built the most expressive silence in the Church out
    # of not doing it.
    keeper = S.say("Quillon", [
        "Welcome, traveller.",
        "Brother Quillon. I keep the Record."])
    keeper += S.narrate(["You ask what the Record is for."])
    keeper += S.say("Quillon", [
        "Those going into the mountain",
        "write their names in the Book.",
        "In case of misfortune."])
    keeper += S.narrate(["You ask what happens in case of misfortune."])
    keeper += S.say("Quillon", [
        "They come back in through the porch,",
        "and write their names again."])
    keeper += S.narrate(["You ask whether he remembers them."])
    keeper += S.say("Quillon", [
        "The Order forbids it, traveller.",
        "It is the only thing the Order forbids."])
    keeper += S.narrate([
        "He smiles, serenely, with his eyes shut. It is a",
        "very expressive smile. It has had forty years."])
    keeper += [S.trope(), R.self_switch("A", True)]

    again = S.say("Quillon", [
        "Every soul deserves a second chance."])
    again += S.narrate([
        "He does not look at Sir Dunstable. He does not",
        "look at him very clearly indeed."])
    again += S.narrate([
        "He adds something under his breath that sounds",
        "like a number in the low two hundreds."])
    img = R.image("Gen_People2", 0, direction=2)
    evs.append(R.event(3, "Brother Quillon", *QUILLON, [
        R.page(keeper, img=img, trigger=0, priority=1),
        R.page(again, img=img, trigger=0, priority=1,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ]))

    # 4: Sir Dunstable of the Vale, just in from the porch. It is a quarter
    # past four. His tea was poured at ten past.
    knight = S.narrate([
        "A knight, in armour that has been polished a great",
        "many times and scorched very slightly more."])
    knight += S.say("Sir Dunstable", [
        "Dunstable. Sir. Of the Vale.",
        "Just signed the Book.",
        "Just in case."])
    knight += S.narrate(["You ask whether he has been through before."])
    knight += S.say("Sir Dunstable", [
        "Oh, once or twice.",
        "Nothing happened, mind. Nothing at",
        "all. Went in, had a look round,",
        "came out. Grand day."])
    knight += S.narrate([
        "There is a cup of tea waiting for him on the lectern.",
        "It is a quarter past four. It was poured at ten past."])
    knight += S.say("Sir Dunstable", [
        "Oh, how kind. Every time!",
        "The fellow's a mind-reader."])
    knight += S.narrate(["Brother Quillon says nothing, with enormous tact."])
    knight += [S.trope(), R.self_switch("A", True)]

    back = S.narrate([
        "Sir Dunstable has just come in through the porch.",
        "He is very slightly more singed than he was."])
    back += S.say("Sir Dunstable", [
        "Just signing in.",
        "Just in case."])
    back += S.narrate([
        "He explains, with some warmth, that nothing",
        "happened."])
    dimg = R.image("Gen_People2", 1, direction=8)
    evs.append(R.event(4, "Sir Dunstable of the Vale", *DUNSTABLE, [
        R.page(knight, img=dimg, trigger=0, priority=1),
        R.page(back, img=dimg, trigger=0, priority=1,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ]))
    return evs


# ================================================================ the doors ==
def _village_doors(base_id, cells):
    """The real doors into Hithermost. `Village A` is two cells; both are
    doors onto the foot of the road."""
    evs = []
    for i, (x, y) in enumerate(sorted(cells)):
        arrive = S.narrate([
            "Hithermost. The last village before the mountain,",
            "climbing the pass in a hurry to get there."])
        arrive += R.choice_block(
            ["Go in", "Press on"],
            [[R.play_se("Move1"),
              R.transfer(MAP_HITHERMOST, ARRIVE[0], ARRIVE[1], 8, 0)],
             S.narrate(["You press on. The mountain will keep."])])
        evs.append(R.event(base_id + i, VILLAGE, x, y, [R.page(
            arrive, img=R.image(""), trigger=1, priority=0, through=True)]))
    return evs


def _chapel_doors(base_id, cells):
    """The chapel's porch, straight off the pass."""
    evs = []
    for i, (x, y) in enumerate(sorted(cells)):
        arrive = S.narrate([
            "The Chapel of Continuance, at the top of the pass.",
            "A light is on inside. It is always on."])
        arrive += R.choice_block(
            ["Go in", "Press on"],
            [[R.play_se("Move1"),
              R.transfer(MAP_CONTINUANCE, ROOM[6], ROOM[5], 8, 0)],
             S.narrate(["You press on."])])
        evs.append(R.event(base_id + i, CHAPEL, x, y, [R.page(
            arrive, img=R.image(""), trigger=1, priority=0, through=True)]))
    return evs


def _mountain_doors(base_id, cells):
    """The Door into the Mountain says no, and does not go anywhere yet."""
    return [R.event(base_id + i, MOUNTAIN, x, y, [R.page(
        door_into_the_mountain(), img=R.image(""), trigger=1, priority=0,
        through=True)]) for i, (x, y) in enumerate(sorted(cells))]


# One claim per name the world map carries - `journey.world_map` merges this
# into its `claims` dict. Three names, three entries, one module.
SITES = {
    VILLAGE: _village_doors,
    CHAPEL: _chapel_doors,
    MOUNTAIN: _mountain_doors,
}


def build():
    R.save_map(MAP_HITHERMOST, hithermost_map())
    R.save_map(MAP_CONTINUANCE, chapel_map())
