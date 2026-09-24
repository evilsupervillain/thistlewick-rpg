"""Map 43: Tobias Frayne's cottage, on the coast road.

`../SITES.md` step 8. The source is `../COMPANIONS.md`'s MER-4, "The Man Who
Cannot Stay Down", and its section 4 row: **Tobias Frayne** has been revived by
passing adventurers eleven times in thirty years, on the grounds that they were
going that way anyway, and has developed a relationship with mortality. This
module builds the place and the man with that in him, and **not the quest**:
MER-4 is Merribell's, she will not raise him a twelfth time, and it gets
appended to him later as pages of its own. Nothing here spends it - he is
not cured, nobody refuses him, and the jar he pays out of is on the table and
is not opened.

* **The world-map door is claimed by name**, `journey.world_map`'s mechanism,
  and the stamp is one cell of `House (Town)` - a single green-roofed house on
  a square of grass between the coast road and the beach, shot before this
  was written. `places.py` has `FRAYNE_STEP`, the sand one square south of it,
  and no world coordinate.
* **The one bad ladder is the MER-4 entry's own prop**, `Wood Ladder` from
  `Inside_B` column 6: two cells up the wall face to a hatch and a foot on the
  floor. The two upper cells are `0x626` - a ladder, open up and down - which
  would let the player walk up the wall, so the event on the foot is "same as
  characters" and blocks it. You read the ladder from the square below.
* **The eleven add up**, because a player will count them: the ladder four,
  the well two, the bull two, the cliff one, and two he would rather not go
  into. The book on the table is the same eleven written down, which is
  `../NORTH.md` 1.3's fourth mechanism, and it has a twelfth line ruled and
  dated today.
* **Nobody in it is unhappy**, which is `../NORTH.md` 1.2 and the whole
  difficulty of the joke: he is not in danger and does not think he is. He has
  found a thing that always works out and a great many kind people, and he
  likes both.
"""
import mapkit as K
import rmmzdata as R

import story as S
from places import MAP_WORLD, MAP_FRAYNE, FRAYNE_STEP

# The name `worldmap.json`'s door events carry for this site.
SITE = "Tobias Frayne"

#            w   h  x1  y1  x2  y2  door_x
ROOM = (17, 13, 4, 4, 12, 8, 8)

# `Wood Ladder`, `Inside_B` column 6: top, middle, foot. The foot is 0x600;
# the upper two are 0x626. See the module docstring.
LADDER = (K.b_tile(6, 0), K.b_tile(6, 1), K.b_tile(6, 2))
LADDER_X = 5

# The jar is `IN_BARREL`, which is `Pot B`: a stoneware crock with its lid
# tied down, and the only thing on either sheet that reads as a jar. `Pot A`
# on the C sheet is a white milk jug and `Pot C` and `Pot D` are brass ewers,
# which `propsheet.py` said and the names did not.
JAR_AT = (12, 8)
TEAPOT = K.c_tile(0, 0)         # `Teapot A`, because he will offer you tea
# `Medicine Shelf`, `Inside_B` (12,3) over (12,4): bottles, not bandages.
MEDICINE = (K.b_tile(12, 3), K.b_tile(12, 4))
MEDICINE_X = 9

TABLE_AT = (7, 6)               # `Table A`, two cells: the book and the jar
TOBIAS = (11, 7)


def cottage_map():
    w, h, x1, y1, x2, y2, door_x = ROOM
    g = K.interior(w, h, x1, y1, x2, y2, door_x=door_x,
                   floor=K.IN_WOOD_FLOOR,
                   wall_top=K.IN_WALL_TOP_PLANK, wall_face=K.IN_WALL_FACE_PLANK)

    # The ladder, up the north wall to a hatch in the loft.
    for dy, tile in enumerate(LADDER):
        g.set(LADDER_X, y1 - 2 + dy, 2, tile)

    # A window on to the road, the stove and the one shelf.
    g.column(7, y1 - 2, 3, K.IN_WINDOW)
    g.column(10, y1 - 1, 2, K.IN_STOVE)
    g.set(11, y1, 2, K.IN_KITCHEN_COUNTER)
    g.column(4, y1 - 1, 2, K.IN_SHELF_BOTTLES)
    g.column(MEDICINE_X, y1 - 1, 2, MEDICINE)

    # The bed, in the corner, made. He has spent a good deal of time lying
    # down and none of it in it.
    g.column(12, y1, 2, K.IN_BED_BROWN)

    # The table: the book, open, and the jar.
    g.blit(TABLE_AT[0], TABLE_AT[1], 2, K.IN_TABLE)
    g.set(TABLE_AT[0] - 1, TABLE_AT[1], 2, K.IN_STOOL)
    g.set(TABLE_AT[0] + 2, TABLE_AT[1], 2, K.IN_STOOL)
    g.set(TABLE_AT[0], TABLE_AT[1], 3, K.INC_OPEN_BOOK)
    g.set(TABLE_AT[0] + 1, TABLE_AT[1], 3, TEAPOT)

    g.set(4, y2, 2, K.IN_CRATE)
    g.set(*JAR_AT, 2, K.IN_BARREL)      # the jar

    m = K.new_map(w, h, K.TS_INSIDE, name="Tobias Frayne's Cottage",
                  bgm="Town2", battleback=("Wood1", "Room1"))
    m["data"] = g.data
    m["events"] = [None] + cottage_events()
    return m


def cottage_events():
    x1, y1, y2, door_x = ROOM[2], ROOM[3], ROOM[5], ROOM[6]
    evs = [S.exit_tile(1, "Cottage Door", door_x, y2 + 2,
                       MAP_WORLD, *FRAYNE_STEP)]

    # 2: Tobias. The count is the joke and it is given as a list, the way a
    # man gives the number of times he has been to the seaside.
    first = S.say("Tobias", [
        "Visitors! Come in, come in.",
        "Mind the ladder. Well - don't mind it.",
        "Stand wherever you like."])
    first += S.narrate(["You ask what is wrong with the ladder."])
    first += S.say("Tobias", [
        "Third rung. Goes like a biscuit.",
        "Thirty years I've meant to mend it,",
        "and it's never quite been the moment."])
    first += S.narrate(["You ask how many times it has gone."])
    first += S.say("Tobias", [
        "The ladder? Four. The well's two,",
        "the bull's two, the cliff's one, and",
        "two I'd sooner not go into, because",
        "I was in a hurry and it was silly."])
    first += S.narrate([
        "You add them up, and ask whether he means",
        "he has died eleven times."])
    first += S.say("Tobias", [
        "Oh, nobody DIES on the coast road.",
        "Somebody always comes by. Adventurers.",
        "They're going that way anyway, they say."])
    first += S.say("Tobias", [
        "And they're ever so kind about it.",
        "Kneel down. Hold your hand.",
        "Ask your name. Ask it twice, sometimes.",
        "You don't get that from the parish."])
    first += S.narrate([
        "He glances at the ladder. Then at you.",
        "Then, quite fondly, at the ladder."])
    first += [S.trope(), R.self_switch("A", True)]

    later = S.say("Tobias", [
        "Staying for tea? I might just pop up",
        "the ladder while the kettle's on."])
    later += S.narrate([
        "He does not go up the ladder. He only",
        "wants you to know that he could."])

    img = R.image("Gen_People3", 0, direction=2)
    evs.append(R.event(2, "Tobias Frayne", *TOBIAS, [
        R.page(first, img=img, trigger=0, priority=1),
        R.page(later, img=img, trigger=0, priority=1,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ]))

    # 3: the ladder. The foot blocks, so nobody climbs the wall; it is read
    # from the square below it. The new rung is the whole of the prop.
    ladder = S.narrate([
        "A ladder up to a hatch in the ceiling.",
        "The third rung is cracked clean through."])
    ladder += S.narrate([
        "A new rung leans against the wall beside it,",
        "planed, sound, and still in its paper.",
        "The paper has gone yellow."])
    evs.append(R.event(3, "The Ladder", LADDER_X, y1, [R.page(
        ladder, img=R.image(""), trigger=0, priority=1,
        direction_fix=True)]))

    # 4: the book. `../NORTH.md` 1.3 mechanism four. Seven of the eleven are
    # written out and the other four are summed; they agree with what he
    # says, because a player will count.
    book = S.narrate([
        "A book, open on the table and ruled in",
        "four columns: WHEN, WHAT, WHO, REMARKS.",
        "Eleven entries, in thirty years."])
    book += S.narrate([
        "  Ladder. A paladin. Very kind.",
        "  Well. Two elves. Sang to me.",
        "  Bull. A cleric. Cried a bit.",
        "  Ladder. Same paladin. Less kind."])
    book += S.narrate([
        "  Cliff. Four of them. Carried me up.",
        "  Ladder. A wizard. Did it from the gate.",
        "  Bull. Same cleric. Laughed this time.",
        "and four more in the same hand."])
    book += S.narrate([
        "Every remark in the last column is some",
        "way of saying 'lovely'.",
        "The twelfth line is ruled, and dated",
        "today, and has nothing in it yet."])
    book += [R.self_switch("A", True)]
    book_again = S.narrate([
        "WHEN, WHAT, WHO, REMARKS.",
        "The twelfth line is still empty. He has",
        "left the pen beside it, uncapped."])

    # 5: the jar, which is MER-4's payment and is not paid here.
    jar = S.narrate([
        "A stoneware jar, the lid tied down with",
        "string, heavy with crowns. The label is in",
        "the book's hand:",
        "   FOR WHOEVER IS GOING THAT WAY."])

    page = dict(img=R.image(""), trigger=0, priority=1, direction_fix=True,
                through=True)
    evs.append(R.event(4, "The Book", TABLE_AT[0], TABLE_AT[1], [
        R.page(book, **page),
        R.page(book_again, conditions={"selfSwitchValid": True,
                                       "selfSwitchCh": "A"}, **page),
    ]))
    evs.append(R.event(5, "The Jar", *JAR_AT, [R.page(jar, **page)]))

    # 6: the shelf, which is where the eleven went afterwards.
    shelf = S.narrate([
        "Tonics, liniments and smelling salts, a",
        "shelf of them, and hardly any in his hand.",
        "Each label has a date on it, and a name,",
        "and 'in case'."])
    evs.append(R.event(6, "The Medicine Shelf", MEDICINE_X, y1,
                       [R.page(shelf, **page)]))
    return evs


# ================================================================ the doors ==
def world_doors(base_id, cells):
    """The real door into the cottage, on the world map.

    `cells` is the one square `worldmap.json` put a placeholder on for this
    site, handed in by `journey.world_map`. Player-touch and below characters,
    the world map's idiom for a place you walk into."""
    w, h, x1, y1, x2, y2, door_x = ROOM
    evs = []
    for i, (x, y) in enumerate(sorted(cells)):
        arrive = S.narrate([
            "A cottage on the coast road, with a",
            "square of grass and a gate that has been",
            "mended more often than it has been shut."])
        arrive += R.choice_block(
            ["Knock", "Press on"],
            [[R.play_se("Knock"),
              R.transfer(MAP_FRAYNE, door_x, y2, 8, 0)],
             S.narrate(["You press on. Somebody inside waves",
                        "through the window, hopefully."])])
        evs.append(R.event(base_id + i, SITE, x, y, [R.page(
            arrive, img=R.image(""), trigger=1, priority=0, through=True)]))
    return evs


def build():
    R.save_map(MAP_FRAYNE, cottage_map())
