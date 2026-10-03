"""Maps 56-57: Fenmarch Hall, and its long gallery.

`../SITES.md` step 16. The source is `../COMPANIONS.md` L5 - the
Pemberton-Gore seat, "moated, damp, and hung with eighty impossible animals in
glass cases ... Small household, enormous portrait gallery, all of them facing
the wrong way" - and its two NPCs, **Mr Ottershaw**, ninety, unrepentant, an
artist, who will show you the joins, and **Pemberton-Gore IV**, nineteen,
magnificent, who found the gate first time. This module builds the place and
the people and **not the quests**: ALD-1 departs from here, ALD-5 is the
Fourth and WRE-4 is the animals, and nothing here spends any of them.

* **The world-map door is claimed by name**, `journey.world_map`'s mechanism.
  The stamp is two cells of `Large Mansion`, a grey house with blue roofs in a
  low walled garden, on a green headland with the sea on both sides. The moat
  is inside the walls: Map 56 is the garden, the moat all the way round the
  house and one bridge over it. `places.py` has `FENMARCH_STEP`, the square
  south of the stamp's western cell, and no world coordinate.
* **The house is small and the gallery is enormous**, so Map 57 is both: one
  long room, the household at the west end of it round the fire, and forty
  cells of glass cases and portraits going east. The cases and the portraits
  are character sheets **drawn by running this module** - no tile on any
  sheet is a glass case, and none of the stock portraits faces away - see
  `draw_art()`. Every animal in a case is two stock creatures sewn together,
  which is what WRE-4 says they are.
* **Sir Aldric in the party is a refusal at the world-map door.** He is the
  quest here twice over - ALD-1 sets out from this house and ALD-5 is his
  nephew in it - and followers are drawn, so he cannot wait outside while his
  sprite walks in behind you. He looks at the house, and then very carefully
  the other way, and nobody goes in. ALD-1 and ALD-5 append their own pages.
* **Wren in the gallery is a reaction shot**, not WRE-4: the quest is her
  being engaged to authenticate the animals, and nobody has engaged her. She
  opens her notebook in front of the first case and closes it again.
* **One trope** - the portraits whose eyes follow you round the room, none of
  which has ever looked at anybody - **and no blush**: the house is damp, not
  red.
"""
import os

import mapkit as K
import rmmzdata as R

import db
import story as S
import q_aldric
import q_wren
from places import MAP_WORLD, MAP_FENMARCH, MAP_GALLERY, FENMARCH_STEP

HERE = os.path.dirname(os.path.abspath(__file__))

# The name `worldmap.json`'s door events carry for this site.
SITE = "Fenmarch Hall"

# The character sheets `draw_art()` writes. `!` - objects, no six-pixel lift.
CASES = ("!Fenmarch_Cases1", "!Fenmarch_Cases2")    # 48x64 frames, 8 each
PORTRAITS = "!Fenmarch_Portraits"                   # 48x48 frames


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


# ================================================================ the garden ==
# A low stone wall round the whole map with a gate in the south; the house in
# the middle of the north half, standing in its moat, with one bridge over.
# Tom's flowerbeds to the east, the damp to the west.
GW, GH = 33, 27
WALL = K.A(38)                  # A2 `Fencepost C (Stone)`: the garden wall
GARDEN_BED = K.a5(91)           # A5 `Garden A`, a flowerbed
BRIDGE = (K.a5(5), K.a5(6), K.a5(7))    # `Large Bridge (V, Left/Center/Right)`
WALL_Y = GH - 3                 # the wall's south run; the gate is a gap in it
GATE_X = (15, 16, 17)
MOAT = (7, 2, 25, 13)           # outer x1, y1, x2, y2
ISLAND = (9, 4, 23, 11)         # the dry inside of it
HOUSE = (9, 4, 15, 7)           # x, y, w, h - front wall row is y + h - 1
HOUSE_DOOR = (16, 10)
ARRIVE = (16, GH - 2)

GATEPOST = (GATE_X[0] - 1, WALL_Y)
MOAT_SIGN = (12, MOAT[3])       # a water cell, read from the bank below it
TOM = (28, 18)
BEDS = [(26, 15, 30, 16), (26, 20, 30, 21)]

MUSHROOMS = K.sf_tile("Outside_B", "Mushrooms A")
GATEPOST_PILLAR = K.sf_block("Outside_C", "Stone Pillar B (Moss)")  # 1x2


def garden_map():
    w, h = GW, GH
    g = K.Canvas(w, h)
    g.fill(0, 0, w - 1, h - 1, 0, K.GRASS)

    # The wall, and the gate in it. A2's fenceposts are an overlay: laid on
    # layer 0 they draw over black, so they go on layer 1 over the grass.
    g.fill(0, 0, w - 1, 0, 1, WALL)
    g.fill(0, 0, 0, WALL_Y, 1, WALL)
    g.fill(w - 1, 0, w - 1, WALL_Y, 1, WALL)
    g.fill(0, WALL_Y, GATE_X[0] - 1, WALL_Y, 1, WALL)
    g.fill(GATE_X[-1] + 1, WALL_Y, w - 1, WALL_Y, 1, WALL)

    # The moat, all the way round, and the bridge over its south side.
    mx1, my1, mx2, my2 = MOAT
    g.fill(mx1, my1, mx2, my2, 0, K.WATER)
    ix1, iy1, ix2, iy2 = ISLAND
    g.fill(ix1, iy1, ix2, iy2, 0, K.GRASS)

    # The drive, from the gate to the bridge, and on to the road outside.
    g.fill(GATE_X[0], iy2 + 1, GATE_X[-1], h - 1, 0, K.PATH)
    g.fill(HOUSE_DOOR[0] - 1, iy2, HOUSE_DOOR[0] + 1, iy2, 0, K.PATH)

    g.building(*HOUSE, wall=K.WALL_MOSS_STONE, roof=K.ROOF_GREEN)
    g.autotile(0)
    g.autotile(1)

    # The bridge is A5 and does not autotile, so it goes on after.
    for y in (my2 - 1, my2):
        for x, t in zip(GATE_X, BRIDGE):
            g.set(x, y, 0, t)
    for x1, y1, x2, y2 in BEDS:
        g.fill(x1, y1, x2, y2, 0, GARDEN_BED)
    # "Two stone gateposts, green with damp", says the gate: one at each end
    # of the wall, over its last fencepost.
    for x in (GATE_X[0] - 1, GATE_X[-1] + 1):
        g.column(x, WALL_Y - 1, 3, GATEPOST_PILLAR)

    fy = HOUSE[1] + HOUSE[3] - 1
    for x in (11, 13, 19, 21):
        g.set(x, fy, 3, K.WINDOW)
    # Two tall stacks on the roof - `Outside_C`'s `Chimney` is 2x2.
    for cx in (11, 20):
        for i, t in enumerate(K.CHIMNEY_STACK):
            g.chimney(cx + i % 2, 5 + i // 2, t)

    # Trees down both sides inside the wall, and outside it by the road.
    for x, y in [(2, 2), (2, 6), (2, 10), (29, 2), (29, 6), (29, 10),
                 (4, 14), (6, 21), (22, 21), (19, 16)]:
        g.blit(x, y, 3, K.TREE)
    for x, y in [(3, 25), (9, 25), (21, 25), (27, 25)]:
        g.blit(x, y, 3, K.TREE)
    g.scatter([(5, 17), (2, 20), (12, 18), (8, 22), (24, 18), (13, 15)], 3,
              MUSHROOMS)
    g.scatter([(26, 17), (30, 17), (26, 19), (30, 19)], 3, K.FLOWERS)

    m = K.new_map(w, h, K.TS_OUTSIDE, name="Fenmarch Hall", bgm="Town2",
                  bgm_volume=60)
    m["data"] = g.data
    m["events"] = [None] + garden_events()
    return m


def gate_pages():
    first = S.narrate([
        "Two stone gateposts, green with damp. On each of them, the",
        "family arms: a knight in armour, rearing up, looking back",
        "over his shoulder at something behind him."])
    first += S.narrate([
        "Under the arms, the motto: RESPICE.",
        "",
        "Look behind you."])
    first += S.narrate([
        "On the inside of the left-hand post, at about the height",
        "of a boy of ten, somebody has scratched: FOUND IT."])
    later = S.narrate([
        "RESPICE. And lower down, in a boy's hand: FOUND IT."])
    return _pair(first, later)


def moat_pages():
    return S.narrate([
        "The moat. It goes all the way round the house, and in",
        "places it goes a little further than that: the lawn is wet",
        "for twenty yards in every direction, and so is the house."])


def tom_pages():
    first = S.narrate([
        "A gardener in a headband, on his knees in a flowerbed,",
        "planting something that will not mind the wet."])
    first += S.say("Tom", [
        "Morning! Tom. I do the",
        "gardens. Walk over from Little Gore",
        "every day. Four miles, both ways."])
    first += S.narrate(["You say that is a long way."])
    first += S.say("Tom", [
        "Not when you've somebody",
        "at the other end of it. Nine years",
        "married this summer. Married here, as",
        "it happens. It rained."])
    first += S.say("Tom", [
        "It always rains at",
        "Fenmarch. The whole of Little Gore",
        "walked over in it and didn't mind."])
    later = S.say("Tom", [
        "Can't stop. Five o'clock,",
        "I'm off home. Always am."])
    return _pair(first, later)


def garden_events():
    evs = []
    # 1-3: the road back out, all three cells of it, below characters.
    for i, x in enumerate(GATE_X):
        evs.append(R.event(i + 1, "The Road Out", x, GH - 1, [R.page(
            [R.play_se("Move1"), R.transfer(MAP_WORLD, *FENMARCH_STEP, 2, 0)],
            img=R.image(""), trigger=1, priority=0, through=True)]))

    # 4: the front door.
    evs.append(S.door(4, "The Front Door", *HOUSE_DOOR, MAP_GALLERY,
                      GALLERY_DOOR_X, GALLERY[3] + 1, direction=8))

    # 5: the gateposts, and the arms.
    first, later = gate_pages()
    evs.append(R.event(5, "The Gate", *GATEPOST, [
        R.page(first, **PAGE), R.page(later, conditions=LATER, **PAGE)]))

    # 6: the moat.
    evs.append(R.event(6, "The Moat", *MOAT_SIGN,
                       [R.page(moat_pages(), **PAGE)]))

    # 7: Tom, from Little Gore.
    evs.append(_person(7, "Tom", TOM, R.image(*S.FACES["Tom"], direction=2),
                       *tom_pages()))
    return evs


# =============================================================== the gallery ==
# One long room. The west end is where the household lives - the fire, the
# table, the clock - and everything east of it is the gallery: portraits all
# along the north wall, a double row of glass cases down the middle, and a
# walk either side of them. Mr Ottershaw's bench is two thirds of the way down.
IW, IH = 48, 12
#          x1  y1  x2  y2
GALLERY = (2, 4, 45, 8)
GALLERY_DOOR_X = 6
HOME_X2 = 10                    # the household's end runs x1..HOME_X2

TABLE_C = K.sf_tile("Inside_B", "Table C")          # the red cloth
TABLE_D = K.sf_tile("Inside_B", "Table D")
CHAIR = K.sf_block("Inside_B", "Chair A (Wood)")    # 1x2, faces south only
STOOL = K.sf_tile("Inside_B", "Stool A")
CLOCK = K.sf_block("Inside_B", "Clock")             # 1x2
PLANTER = K.sf_tile("Inside_C", "Planter A")        # a box of fresh flowers
POT_PLANT = K.sf_tile("Inside_C", "Potted Plant B")  # violets; A is a cactus
SOUP = K.sf_tile("Inside_C", "Soup Bowl")

FIRE_X = 3                      # the fireplace is three cells, x..x+2
FAMILY_TABLE = [(6, 6), (7, 6)]
FOURTH = (8, 5)
PUDDIFOOT = (4, 7)
CASE_XS = list(range(12, 44, 2))                    # 16 a row
CASE_ROWS = (5, 7)
BENCH = [(31, 8), (32, 8)]      # Mr Ottershaw's, in the south walk
OTTERSHAW = (33, 8)
PORTRAIT_XS = list(range(13, 44, 4))                # 8, on the lower face row
THIRD = PORTRAIT_XS[3]          # Sir Aldric III's portrait, over the planter

# Portraits by x, west to east, oldest first; the Fourth's is the newest and
# the last, and the only one facing out. Index into `PORTRAIT_LOOKS`.
PORTRAIT_AT = dict(zip(PORTRAIT_XS, range(8)))


def gallery_map():
    x1, y1, x2, y2 = GALLERY
    g = K.interior(IW, IH, x1, y1, x2, y2, door_x=GALLERY_DOOR_X,
                   floor=K.IN_WOOD_FLOOR, wall_top=K.IN_WALL_TOP_STONE,
                   wall_face=K.IN_WALL_FACE_STONE)
    # The household's end has a rug; the gallery a long red runner down the
    # aisle between the cases. Layer 1 is floor art.
    g.fill(x1 + 1, y1 + 1, HOME_X2 - 1, y2 - 1, 1, K.IN_BLUE_RUG)
    g.fill(CASE_XS[0] - 1, 6, x2, 6, 1, K.IN_RED_CARPET)
    g.autotile(1)

    # The west end: the fire, the table, the clock.
    g.blit(FIRE_X, y1 - 1, 2, K.IN_FIREPLACE)
    g.column(HOME_X2 - 1, y1 - 1, 2, CLOCK)
    for x, y in FAMILY_TABLE:
        g.set(x, y, 2, TABLE_C)
    g.set(*FAMILY_TABLE[0], 3, SOUP)
    g.column(FAMILY_TABLE[0][0], y1, 2, CHAIR)
    g.column(FAMILY_TABLE[1][0], y1, 2, CHAIR)
    g.set(FAMILY_TABLE[0][0], y2 - 1, 2, STOOL)
    g.set(FAMILY_TABLE[1][0], y2 - 1, 2, STOOL)
    g.set(x1, y2, 3, POT_PLANT)

    # The gallery: Mr Ottershaw's bench, and fresh flowers under the Third.
    for x, y in BENCH:
        g.set(x, y, 2, TABLE_D)
    g.set(THIRD, y1, 2, PLANTER)
    g.set(x2, y2, 3, POT_PLANT)

    m = K.new_map(IW, IH, K.TS_INSIDE, name="The Long Gallery", bgm="Town2",
                  bgm_volume=50, battleback=("Wood1", "Room1"))
    m["data"] = g.data
    m["events"] = [None] + gallery_events()
    return m


def fourth_pages():
    first = S.narrate([
        "A young man in blue and silver, polishing a helmet that",
        "does not need it. He stands up to greet you as if you were",
        "the King."])
    first += S.say("The Fourth", [
        "Pemberton-Gore. The",
        "Fourth. Welcome to Fenmarch! Mind the",
        "moat. It's everywhere."])
    first += S.narrate(["You say that you found the house easily."])
    first += S.say("The Fourth", [
        "Did you? So did I!",
        "I found the gate first time, when I",
        "was ten. First of the family who ever",
        "has. Grandfather came over the wall."])
    first += S.say("The Fourth", [
        "Until he was eighty. He",
        "said it was quicker. It wasn't. He",
        "just couldn't find the gate."])
    first += S.narrate(["You ask about the family."])
    first += S.say("The Fourth", [
        "Oh, you'll want the",
        "gallery. That's everybody. And my",
        "uncle - Sir Aldric, the Third."])
    first += S.say("The Fourth", [
        "He went out errant nine",
        "years ago and never came back. It's",
        "the best story we've got."])
    first += S.narrate([
        "You open your mouth. He is already on to the next part."])
    first += S.say("The Fourth", [
        "Imagine being that busy.",
        "I'm going out myself, one day.",
        "Somebody ought to tell him how proud",
        "we all are."])
    first += S.narrate([
        "He means every word of it, magnificently. The helmet has",
        "never been so clean."])
    later = S.say("The Fourth", [
        "Mind the moat! It's",
        "everywhere. Even in here, a bit."])
    return _pair(first, later)


def puddifoot_pages():
    first = S.narrate([
        "A housekeeper in a white cap, with a duster in one hand",
        "and a second duster in the other."])
    first += S.say("Mrs Puddifoot", [
        "Mrs Puddifoot. I keep",
        "house. What there is of it. It's",
        "mostly gallery."])
    first += S.say("Mrs Puddifoot", [
        "Everything in this house",
        "is damp except the animals. Mr",
        "Ottershaw won't have it."])
    first += S.say("Mrs Puddifoot", [
        "Eighty of them. I start",
        "dusting on a Friday and I'm done",
        "by the Wednesday after."])
    first += S.narrate(["You count the cases. There are not eighty."])
    first += S.say("Mrs Puddifoot", [
        "The rest are upstairs.",
        "There's one in every bedroom. You",
        "get used to it."])
    later = S.say("Mrs Puddifoot", [
        "Friday to Wednesday.",
        "Then it's Friday again."])
    return _pair(first, later)


def ottershaw_pages():
    first = S.narrate([
        "A very old man at a workbench among the cases, in green",
        "lenses, with a needle in his hand and a great deal of",
        "thread."])
    first += S.say("Mr Ottershaw", [
        "Ottershaw. Ninety in",
        "March. I did the animals."])
    first += S.narrate(["You ask whether he preserved them."])
    first += S.say("Mr Ottershaw", [
        "Preserved? Anybody can",
        "preserve. A cook can preserve.",
        "I COMPOSED them."])
    first += S.say("Mr Ottershaw", [
        "Seventy years. Three",
        "generations. The family'll tell you",
        "every one of them's rare. The family",
        "are right. There's one of each."])
    first += S.narrate(["He beckons you over to the nearest case."])
    first += S.say("Mr Ottershaw", [
        "Look at the shoulder.",
        "Now tell me where it stops."])
    first += S.narrate([
        "You look for a long time. Feathers, and then scales, and",
        "nowhere at all where the one becomes the other."])
    first += S.say("Mr Ottershaw", [
        "Seventy years, and",
        "nobody's found a join. Not one of",
        "them ever looked."])
    first += S.narrate([
        "He is not sorry. He is delighted. He goes back to his",
        "needle, humming."])
    later = S.say("Mr Ottershaw", [
        "Still looking for the",
        "join? Take your time. Everybody does."])
    return _pair(first, later)


# The cases with a brass plate worth reading, by (row, x), and what the plate
# says in the family's hand. Every other case is dressing and says nothing.
# A case shows `SEWN[case_look(row, x)]` - the south row is the north row
# turned on by eight, so the two rows never match across the runner - and
# each plate is on the case whose animal it describes: the bear on a crab is
# the Marsh Bear.
CASE_PLATES = {
    (5, 12): [
        "THE MARSH BEAR (Ursus fenmarchensis). Taken in the moat",
        "by Sir Aldric the Second. It had come for the",
        "crayfish, and had been at them some time."],
    (7, 30): [
        "A UNICORN, of the Home Farm. Bred at Fenmarch.",
        "Not a success as a unicorn. It kept the foxes down."],
    (5, 16): [
        "THE FENMARCH PHOENIX. Rose from the kitchen fire, and was",
        "put out by Cook."],
    (7, 34): [
        "THE GREATER MOAT BEAR. Larger than the Marsh Bear, and",
        "wetter."],
    (5, 20): [
        "A ROOK (Scaled). Shot on the lawn by Sir Aldric the",
        "First, who had been looking for the gate at the time."],
    (7, 38): [
        "A HORSE. The plate says nothing else. There is room left",
        "on it where somebody meant to, and did not like to ask."],
}


def case_look(row, x):
    """Which of `SEWN`'s sixteen animals is in the case at (x, row)."""
    return ((x - CASE_XS[0]) // 2 + 8 * CASE_ROWS.index(row)) % 16


def case_pages(row, x):
    plate = S.narrate(CASE_PLATES[(row, x)])
    if (row, x) != FIRST_CASE:
        return plate
    # Wren in the party is a reaction shot, not WRE-4: nobody has asked her.
    wren = S.narrate([
        "Wren stops in front of the case. She looks at it for a long",
        "time, and then at the shoulder, and then at the case again."])
    wren += S.narrate([
        "She takes out her notebook, and opens it, and closes it",
        "again."])
    wren += S.say("Wren", ["Not unless I'm asked."])
    return plate + R.if_then(R.condition_actor_in_party(db.WREN), wren)


FIRST_CASE = (5, 12)


# The portraits with something to say, by x. The rest hang there.
def portrait_pages(x):
    i = PORTRAIT_AT[x]
    if i == 0:
        first = S.narrate([
            "SIR ALDRIC PEMBERTON-GORE, THE FIRST. In armour, painted",
            "from behind, looking back over his shoulder at something",
            "outside the frame."])
        first += S.narrate([
            "They are all like that. Every portrait down the gallery",
            "is of somebody's back. Not one of them has ever followed",
            "anybody round a room with its eyes."])
        first += [S.trope()]
        later = S.narrate([
            "The First, from behind, looking the other way. The",
            "family has always faced the wrong way. It is on the arms."])
        return first, later
    if i == 2:
        return S.narrate([
            "DAME HONORIA PEMBERTON-GORE, 1811. From behind, looking",
            "out of a window. The painter was paid for a front, and",
            "waited three weeks for one."]), None
    if i == 3:
        first = S.narrate([
            "SIR ALDRIC PEMBERTON-GORE, THE THIRD. From behind, in",
            "armour, walking out of the picture at a good pace."])
        first += S.narrate([
            "There are fresh flowers in a box under it. They were",
            "changed this morning. They have been changed every morning",
            "for nine years."])
        return first, None
    if i == 5:
        return S.narrate([
            "ROLLO, a dog, 1840. From behind. She was the only one",
            "of the family who could find her way home, and she did",
            "it facing the right way."]), None
    if i == 7:
        return S.narrate([
            "THE FOURTH. Painted last spring. The only portrait in the",
            "gallery facing out, and he is pointing, confidently, at",
            "the gate."]), None
    return None, None


def gallery_events():
    x1, y1, x2, y2 = GALLERY
    evs = [R.event(1, "The Front Door", GALLERY_DOOR_X, y2 + 2, [R.page(
        [R.play_se("Move1"),
         R.transfer(MAP_FENMARCH, HOUSE_DOOR[0], HOUSE_DOOR[1] + 1, 2, 0)],
        img=R.image(""), trigger=1, priority=0, through=True)])]
    evs.append(_person(2, "The Fourth", FOURTH,
                       R.image("Gen_People5", 3, direction=2),
                       *fourth_pages()))
    evs[-1]["pages"] += q_aldric.fourth_pages(evs[-1]["pages"][-1])  # ALD-5
    evs.append(_person(3, "Mrs Puddifoot", PUDDIFOOT,
                       R.image(*S.FACES["Mrs Puddifoot"], direction=6), *puddifoot_pages()))
    evs[-1]["pages"] += q_wren.puddifoot_pages(evs[-1]["pages"][-1])  # WRE-4
    evs.append(_person(4, "Mr Ottershaw", OTTERSHAW,
                       R.image("Gen_People5", 4, direction=4),
                       *ottershaw_pages()))
    evs[-1]["pages"] += q_wren.ottershaw_pages(evs[-1]["pages"][-1])  # WRE-4

    # 5: the fire, which the stock fireplace does not have - step 12.
    evs.append(R.event(5, "The Fire", FIRE_X + 1, y1, [R.page(
        [], img=R.image("!Flame", 3, direction=4), trigger=0, priority=0,
        step_anime=True, direction_fix=True)]))

    # 6-13: the portraits, on the lower row of the north wall's face, read
    # from the walk below them. The Third's is read from the planter under
    # it, which blocks the square you would have stood on.
    eid = 6
    for x in PORTRAIT_XS:
        i = PORTRAIT_AT[x]
        img = R.image(PORTRAITS, i, direction=2)
        first, later = portrait_pages(x)
        if first is None or x == THIRD:
            pages = [R.page([], img=img, trigger=0, priority=1,
                            direction_fix=True)]
        elif later is None:
            pages = [R.page(first, img=img, trigger=0, priority=1,
                            direction_fix=True)]
        else:
            pages = [R.page(first + [R.self_switch("A", True)], img=img,
                            trigger=0, priority=1, direction_fix=True),
                     R.page(later, img=img, trigger=0, priority=1,
                            direction_fix=True, conditions=LATER)]
        evs.append(R.event(eid, "Portrait", x, y1 - 1, pages))
        eid += 1

    # 14: the flowers under the Third, which is how his portrait is read.
    evs.append(R.event(eid, "The Third", THIRD, y1,
                       [R.page(portrait_pages(THIRD)[0], **PAGE)]))
    evs[-1]["pages"] += q_aldric.third_portrait_pages(evs[-1]["pages"][0])  # ALD-5
    eid += 1

    # 15-: the cases, two rows of sixteen. Sixteen animals, two sheets.
    for row in CASE_ROWS:
        for x in CASE_XS:
            look = case_look(row, x)
            img = R.image(CASES[look // 8], look % 8, direction=2)
            cmds = case_pages(row, x) if (row, x) in CASE_PLATES else []
            evs.append(R.event(eid, "Case", x, row, [R.page(
                cmds, img=img, trigger=0, priority=1, direction_fix=True)]))
            eid += 1
    return evs


# ================================================================== the art ==
# (enemy image, flip it, enemy image, flip it, how): "v" sews the first one's
# top half on to the second one's bottom half; "h" the first one's left half
# on to the second one's right. Side-on creatures face left unless flipped.
SEWN = [
    ("SF_Brownbear", False, "Crab", False, "v"),
    ("SF_Wolf", False, "Unicorn", False, "h"),
    ("SF_Phoenix", False, "Salamander", False, "v"),
    ("Kraken", False, "SF_Brownbear", False, "v"),
    ("Crow", False, "Frilledlizard", False, "v"),
    ("Crab", False, "Unicorn", False, "v"),
    ("SF_Whitewolf", True, "Hydra", True, "h"),
    ("Tigerbunny", False, "SF_Anaconda", False, "v"),
    ("Unicorn", True, "Kraken", False, "h"),
    ("SF_Kamaitachi", False, "SF_Whitewolf", False, "v"),
    ("Crow", False, "SF_Brownbear", False, "v"),
    ("Hakutaku", False, "Crab", False, "h"),
    ("Frilledlizard", False, "Unicorn", False, "v"),
    ("Ketos", False, "SF_Wolf", True, "h"),
    ("Salamander", False, "SF_Wolf", False, "v"),
    ("Hydra", False, "Tigerbunny", False, "v"),
]

# (sheet, index, facing, backdrop): 2 is facing out, 8 is from behind.
PORTRAIT_LOOKS = [
    ("Actor3", 6, 8, (92, 30, 30)),         # the First
    ("People2", 0, 8, (40, 70, 44)),        # the Second
    ("People1", 1, 8, (70, 50, 90)),        # Dame Honoria
    ("Actor3", 6, 8, (36, 48, 90)),         # the Third
    ("People1", 3, 8, (90, 60, 40)),        # a lady
    ("Nature", 0, 8, (80, 70, 50)),         # Rollo, a dog
    ("People2", 3, 8, (60, 44, 30)),        # a gentleman
    ("Gen_People5", 3, 2, (150, 120, 70)),  # the Fourth, facing out
]


def draw_art():
    """Writes the three character sheets the gallery hangs and shows.

    Not part of the data build, like `art.py` and Coldbarrow's map: run this
    module to redraw them. **No tile on any sheet is a glass case**, and the
    stock portraits face out, so both are drawn here. A case is a wooden
    plinth and a glass box with the shine on it, and in the box two stock
    creatures from `img/enemies`, sewn together - Ottershaw's work. A
    portrait is `Inside_B`'s `Portrait B` frame with its sitter painted out
    and a character sprite put in, from behind."""
    import sys
    sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "chargen"))
    import numpy as np
    import png
    game = os.path.join(HERE, "..")

    def load(name, flip):
        a = png.read(os.path.join(game, "img", "enemies", name + ".png"))
        a = a.copy()
        a[a[..., 3] < 200] = 0          # the drop shadow is half alpha
        ys, xs = np.nonzero(a[..., 3])
        a = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
        return a[:, ::-1] if flip else a

    def resize(a, w, h):
        a = a.astype(float)
        pm = a.copy()
        pm[..., :3] *= a[..., 3:4] / 255
        ys = np.linspace(0, a.shape[0], h + 1).astype(int)
        xs = np.linspace(0, a.shape[1], w + 1).astype(int)
        out = np.zeros((h, w, 4))
        for j in range(h):
            for i in range(w):
                b = pm[ys[j]:max(ys[j + 1], ys[j] + 1),
                       xs[i]:max(xs[i + 1], xs[i] + 1)]
                out[j, i] = b.reshape(-1, 4).mean(0)
        al = out[..., 3:4]
        rgb = np.where(al > 0, out[..., :3] * 255 / np.maximum(al, 1), 0)
        return np.dstack([rgb, np.where(al[..., 0] > 110, 255, 0)])

    def fit(a, bw, bh):
        k = min(bw / a.shape[1], bh / a.shape[0])
        w, h = max(1, round(a.shape[1] * k)), max(1, round(a.shape[0] * k))
        c = np.zeros((bh, bw, 4))
        x0 = (bw - w) // 2
        c[bh - h:, x0:x0 + w] = resize(a, w, h)
        return c

    def sew(a, b, how, bw=36, bh=38):
        A, B = fit(a, bw, bh), fit(b, bw, bh)
        if how == "h":
            out = B.copy()
            out[:, :bw // 2] = A[:, :bw // 2]
            return out
        ya = np.nonzero(A[..., 3].any(1))[0]
        yb = np.nonzero(B[..., 3].any(1))[0]
        top = A[ya.min():(ya.min() + ya.max()) // 2]
        bot = B[(yb.min() + yb.max()) // 2:]
        out = np.zeros_like(B)
        out[bh - len(bot):] = bot
        y0 = max(0, bh - len(bot) - len(top))
        out[y0:bh - len(bot)] = top[len(top) - (bh - len(bot) - y0):]
        return out

    def over(dst, src, x, y):
        h, w = src.shape[:2]
        d = dst[y:y + h, x:x + w]
        al = src[..., 3:4] / 255
        d[..., :3] = src[..., :3] * al + d[..., :3] * (1 - al)
        d[..., 3:4] = np.maximum(d[..., 3:4], src[..., 3:4])

    def case(animal):
        f = np.zeros((64, 48, 4))
        wood, dark, gold = (96, 60, 34, 255), (60, 36, 20, 255), (206, 168,
                                                                  72, 255)
        f[50:62, 4:44] = wood
        f[60:62, 4:44] = dark
        f[50, 4:44] = gold
        f[53, 6:42] = dark
        glass = np.zeros((44, 38, 4))
        glass[...] = (190, 222, 232, 70)
        over(f, glass, 5, 6)
        over(f, animal, 6, 11)
        edge = (226, 244, 250, 200)
        f[6:50, 5] = edge
        f[6:50, 42] = edge
        f[4:7, 4:44] = wood
        f[4, 4:44] = gold
        white = np.array([255, 255, 255, 255])
        for k in range(12):             # the shine on the glass
            y, x = 12 + k, 32 - k // 2
            f[y, x] = f[y, x] * 0.5 + white * 0.5
            f[y, x - 1] = f[y, x - 1] * 0.7 + white * 0.3
        return f

    def tile(sheet, tid):
        a = png.read(os.path.join(game, "img", "tilesets", sheet + ".png"))
        x = ((tid // 128) % 2 * 8 + tid % 8) * 48
        y = ((tid % 256) // 8 % 16) * 48
        return a[y:y + 48, x:x + 48].astype(float)

    def figure(sheet, i, facing):
        a = png.read(os.path.join(game, "img", "characters", sheet + ".png"))
        row = {2: 0, 4: 1, 6: 2, 8: 3}[facing]
        bx, by = (i % 4) * 144, (i // 4) * 192
        return a[by + row * 48:by + row * 48 + 48,
                 bx + 48:bx + 96].astype(float)

    def portrait(sheet, i, facing, backdrop):
        f = tile("Inside_B", PORTRAIT_B)
        x0, y0, x1, y1 = 11, 9, 37, 40
        f[y0:y1, x0:x1] = backdrop + (255,)
        fig = resize(figure(sheet, i, facing)[4:40, 6:42], x1 - x0,
                     y1 - y0 + 4)[:y1 - y0]
        over(f, fig, x0, y0)
        return f

    def sheet(frames, fw, fh):
        """Eight characters, each standing still in all twelve frames."""
        out = np.zeros((fh * 8, fw * 12, 4))
        for n, f in enumerate(frames):
            bx, by = (n % 4) * 3 * fw, (n // 4) * 4 * fh
            for r in range(4):
                for c in range(3):
                    out[by + r * fh:by + (r + 1) * fh,
                        bx + c * fw:bx + (c + 1) * fw] = f
        return np.clip(out, 0, 255).round().astype(np.uint8)

    def write(name, img):
        path = os.path.join(game, "img", "characters", name + ".png")
        png.write(path, img)
        print("wrote", os.path.normpath(path))

    cases = [case(sew(load(a, fa), load(b, fb), how))
             for a, fa, b, fb, how in SEWN]
    write(CASES[0], sheet(cases[:8], 48, 64))
    write(CASES[1], sheet(cases[8:], 48, 64))
    write(PORTRAITS, sheet([portrait(*p) for p in PORTRAIT_LOOKS], 48, 48))
    draw_stamp()


# The house's stamp on the world map, `World_B`'s `Large Mansion` (2x2 at
# columns 4-5, rows 12-13), has blue roofs; the door says "its roofs gone
# green" and Map 56's are. `World_B_Fenmarch` is the sheet with that one stamp
# gone the green of old copper, and `mapkit.TS_OVERWORLD` the tileset that
# carries it. Nothing else on the world map uses the stamp.
STAMP_CELLS = [(4, 12), (5, 12), (4, 13), (5, 13)]


def draw_stamp():
    """Writes `img/tilesets/World_B_Fenmarch.png` and its `.txt`. Not part of
    the data build: run this module to redraw it."""
    K.recolour_sheet("World_B", "World_B_Fenmarch", STAMP_CELLS, (170, 250),
                     140, 0.5, [("Large Mansion", "Large Mansion (Green)")])


# `Inside_B`'s `Portrait B`, the gilt frame, by its index on the sheet: the
# engine's tile maths reads it straight out of the png.
PORTRAIT_B = 133


# ================================================================== the door ==
def world_doors(base_id, cells):
    """The real door into Fenmarch Hall, on the world map.

    `cells` is the two squares `worldmap.json` put placeholders on for this
    site - the lower half of the `Large Mansion` stamp - handed in by
    `journey.world_map`. Player-touch and below characters, the world map's
    idiom for a place you walk into.

    **With Sir Aldric in the party it is a refusal.** ALD-1 sets out from this
    house and ALD-5 is his nephew in it, so his walking in is the quest, and
    followers are drawn, so he cannot wait at the gate. He looks at the house
    and then the other way, and you press on. ALD-5 appends the fourth page,
    on which his squire finds the gate; ALD-1 turned out to need none."""
    aldric = {"actorValid": True, "actorId": db.ALDRIC}
    evs = []
    for i, (x, y) in enumerate(sorted(cells)):
        arrive = S.narrate([
            "A grey house behind a low wall, with its roofs gone green",
            "and a moat all the way round it, on a headland with the",
            "sea on both sides. Everything about it is slightly wet."])
        arrive += R.choice_block(
            ["Go in at the gate", "Press on"],
            [[R.transfer(MAP_FENMARCH, *ARRIVE, 8, 0)],
             S.narrate(["You press on. Somewhere behind the wall, a",
                        "clock strikes, damply."])])
        stop = S.narrate([
            "A grey house behind a low wall, with a moat all the way",
            "round it. Sir Aldric has stopped in the road."])
        stop += S.narrate([
            "He looks at the house for a long moment. Then, very",
            "carefully, he looks the other way."])
        stop += S.say("Aldric", [
            "Fine old place. Damp, I",
            "should think. ...Shall we press on?"])
        stop += S.narrate([
            "Nobody asks. He walks a little ahead of you for the next",
            "mile, which is unusual, and in the right direction, which",
            "is more so."])
        stop += [R.self_switch("A", True)]
        again = S.say("Aldric", ["Damp. Shall we press on?"])
        touch = dict(img=R.image(""), trigger=1, priority=0, through=True)
        evs.append(R.event(base_id + i, SITE, x, y, [
            R.page(arrive, **touch),
            R.page(stop, conditions=aldric, **touch),
            R.page(again, conditions=dict(aldric, selfSwitchValid=True,
                                          selfSwitchCh="A"), **touch),
        ]))
        evs[-1]["pages"] += q_aldric.fenmarch_door_pages(evs[-1]["pages"][0])  # ALD-5
    return evs


def build():
    R.save_map(MAP_FENMARCH, garden_map())
    R.save_map(MAP_GALLERY, gallery_map())


if __name__ == "__main__":
    draw_art()
