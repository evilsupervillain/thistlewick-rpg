"""Map 49: the Sable Hart, the inn where every corner is taken.

`../SITES.md` step 12. The source is `../COMPANIONS.md` L7 - "an inn on a moor
where every corner is taken. A rota for the darkest one. A newsletter. Five
hooded men being scrupulously fair to each other about seating" - and COR-3,
whose rivals are "individually, lovely, and collectively a support group that
has never once used the word". This module builds the room and the five and
**not the quest**: COR-3 is Corvin's, and it is appended later as pages of its
own. Nothing here spends it. Its payoff is the league table, on which Corvin
is seventeenth, so the table on the wall stops at fourth: the rota is pinned
over the rest of it, with a fifth pin to be sure.

* **The world-map door is claimed by name**, `journey.world_map`'s mechanism.
  The stamp is one cell of `House (Town)` - a green-roofed house on a square
  of grass, two roads ending at its door, alone on dry sandy waste, shot
  before this was written - so the door's line describes the waste and not
  a moor. `places.py` has `SABLE_HART_STEP`, the sand one square south of
  it, and no world coordinate.
* **Four corners and five rivals**, which is the whole arithmetic. Crake,
  the Secretary, has the corner by the window, because somebody has to be
  able to read the rota; Veyle has the darkest, north-east, until Monday;
  Rook keeps the league table in the south-west and Morrow edits the
  newsletter in the south-east. Blackwood, the newest, is first on the
  waiting list for a corner and has the only seat left, which is by the
  fire, in the light, where he is doing his best.
* **The middle of the room is empty**: two tables and four stools that
  nobody has ever sat at. It is the room's sight gag and costs nothing.
* **Corvin in the party is a reaction shot and not the quest.** Crake has him
  down as a member, Corvin is not here, and Crake writes something very
  small in a book. The newsletter sends his apologies, "as ever", and keeps
  his chair - which is COR-3's premise, and not its payoff.
* **One trope, the dark mirror, on Crake. No blush**: the room is warm, not
  red, and there is nobody in it for a double meaning to land on.
"""
import mapkit as K
import rmmzdata as R

import db
import story as S
from places import MAP_WORLD, MAP_SABLE_HART, SABLE_HART_STEP

# The name `worldmap.json`'s door events carry for this site - no "The".
SITE = "Sable Hart"

#            w   h  x1  y1  x2  y2  door_x
ROOM = (21, 13, 3, 4, 17, 9, 10)

POSTED = K.sf_tile("Inside_B", "Posted Notice")
CURTAIN = K.sf_block("Inside_B", "Curtains B")      # 1x2, heavy, and drawn
BOTTLES = K.sf_block("Inside_B", "Bottle Shelf A")
CORNER_TABLE = K.sf_tile("Inside_B", "Table D")
MUG = K.sf_tile("Inside_C", "Pint Mug C")
NOTES = K.sf_tile("Inside_C", "Notes D")

# The four corners, and who is in each this week.
CRAKE = (3, 4)              # north-west, by the window: the Secretary's
VEYLE = (17, 4)             # north-east, the darkest, until Monday
ROOK = (3, 9)               # south-west: the league table's workings
MORROW = (17, 9)            # south-east: the newsletter
BLACKWOOD = (11, 6)         # by the fire, on a stool; first on the list
GARROW = (8, 5)             # the end of the bar
HEARTH = (11, 4)            # the fire in `Large Fireplace`'s opening
LEAGUE = (14, 3)            # a notice on the wall face, read from below
ROTA = (15, 3)              # pinned beside it, and over its bottom half
MIDDLE = [(6, 7), (13, 7)]  # `Table A`, two cells each, with a stool each end


def hart_map():
    w, h, x1, y1, x2, y2, door_x = ROOM
    g = K.interior(w, h, x1, y1, x2, y2, door_x=door_x,
                   floor=K.IN_WOOD_FLOOR, floor_alt=K.IN_DARK_WOOD)

    # A rug in front of the fire, for the one seat that is not in a corner.
    # Layer 1 is floor art.
    g.fill(10, y1 + 1, 12, y1 + 1, 1, K.IN_RED_RUG)
    g.autotile(1)

    # The north wall: the window over the Secretary's corner, the bar, the
    # fire, the two notices, and a curtain drawn over the darkest corner,
    # where there is no window.
    g.column(x1, y1 - 2, 3, K.IN_WINDOW)
    g.column(6, y1 - 1, 2, BOTTLES)
    g.column(7, y1 - 1, 2, K.IN_WINE_RACK)
    g.blit(6, y1 + 1, 1, K.IN_TABLE)
    g.set(6, y1 + 1, 3, K.INC_DESK_BELL)
    g.set(7, y1 + 1, 3, MUG)
    g.blit(10, y1 - 1, 2, K.IN_FIREPLACE)
    g.set(*LEAGUE, 3, POSTED)
    g.set(*ROTA, 3, POSTED)
    g.column(x2, y1 - 2, 3, CURTAIN)

    # A small table beside each corner, with a pint on it; Rook's has his
    # workings and Morrow's the next issue.
    for (cx, cy), thing in [(CRAKE, MUG), (VEYLE, MUG),
                            (ROOK, K.INC_OPEN_BOOK), (MORROW, NOTES)]:
        tx = cx + 1 if cx == x1 else cx - 1
        g.set(tx, cy, 2, CORNER_TABLE)
        g.set(tx, cy, 3, thing)

    # Blackwood's stool, by the fire.
    g.set(*BLACKWOOD, 2, K.IN_STOOL)

    # The middle of the room, where nobody sits.
    for tx, ty in MIDDLE:
        g.blit(tx, ty, 2, K.IN_TABLE)
        g.set(tx - 1, ty, 2, K.IN_STOOL)
        g.set(tx + 2, ty, 2, K.IN_STOOL)

    m = K.new_map(w, h, K.TS_INSIDE, name="The Sable Hart", bgm="Town5",
                  battleback=("Wood1", "Room1"))
    m["data"] = g.data
    m["events"] = [None] + hart_events()
    return m


def _pair(first, later):
    """A first conversation and the short one after it, on self switch A."""
    return first + [R.self_switch("A", True)], later


def _person(event_id, name, xy, img, first, later):
    return R.event(event_id, name, *xy, [
        R.page(first, img=img, trigger=0, priority=1),
        R.page(later, img=img, trigger=0, priority=1,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ])


def crake_pages():
    first = S.narrate([
        "A hooded man in the corner by the window stands up as",
        "you come in, which nobody brooding in a corner has ever",
        "done."])
    first += S.say("Crake", [
        "Good evening. Hollin Crake,",
        "Secretary. Are you anybody's",
        "rival at all?"])
    first += S.narrate([
        "You say that you are the Chosen One. Number forty-eight."])
    first += S.say("Crake", [
        "Ah. Then you're on the other",
        "side, as it were. That's quite",
        "all right. We're very fair."])
    first += S.say("Crake", [
        "Every corner is taken, I'm",
        "afraid. There are four corners",
        "and five of us. You can see",
        "the difficulty."])
    first += S.narrate(["You can see the difficulty."])
    first += S.say("Crake", [
        "Hence the rota. The darkest",
        "corner changes hands on a",
        "Monday. Nobody broods in it",
        "out of turn, however rainy."])
    first += S.say("Crake", [
        "This is the Secretary's corner.",
        "It is by the window, because",
        "somebody has to be able to",
        "read the rota."])
    first += [S.trope()]

    # Corvin in the party is a reaction shot, not COR-3.
    corvin = S.narrate([
        "Crake looks past you, at the man in the black coat, for",
        "rather a long moment."])
    corvin += S.say("Crake", [
        "Mr Ash. We have you down",
        "as a member."])
    corvin += S.say("Corvin", ["I'm not here."])
    corvin += S.say("Crake", ["Of course."])
    corvin += S.narrate([
        "He writes something very small in a book, and closes it,",
        "and does not mention it again."])
    first += R.if_then(R.condition_actor_in_party(db.CORVIN), corvin)

    later = S.say("Crake", [
        "Veyle has the dark corner",
        "until Monday. Then Rook. Then",
        "me, though I shall very likely",
        "give mine to Blackwood."])
    return _pair(first, later)


def veyle_pages():
    first = S.narrate([
        "The darkest corner of the room. A hooded man sits in it",
        "as if he were part of it, with a scar and a pint."])
    first += S.say("Veyle", [
        "...Leave me.",
        "The shadows are mine."])
    first += S.narrate([
        "He glances at the rota on the wall, and back at you."])
    first += S.say("Veyle", ["Until Monday."])
    first += S.say("Veyle", [
        "Sorry. That came out very",
        "possessive. They're mine until",
        "Monday, and then they're Rook's,",
        "and he's earned them."])
    first += S.say("Veyle", [
        "Silas Veyle. And the scar?",
        "Don't ask about the scar."])
    first += S.narrate([
        "You don't ask about the scar. He looks, very briefly,",
        "disappointed."])
    later = S.say("Veyle", [
        "The curtain's drawn. There's",
        "no window behind it. It makes",
        "a real difference."])
    return _pair(first, later)


def rook_pages():
    first = S.say("Rook", [
        "Thaddeus Rook. I keep the",
        "table. Points for a vow, a",
        "scar, a dramatic exit, and",
        "standing about in the rain."])
    first += S.narrate(["You ask who is top."])
    first += S.say("Rook", [
        "Veyle. The scar, mostly.",
        "He was very good about it."])
    first += S.narrate(["You ask where he is himself."])
    first += S.say("Rook", [
        "Fourth. I never give myself",
        "the benefit of the doubt.",
        "That's the whole point of",
        "keeping the table."])
    first += S.say("Rook", [
        "I'm rival to a very great",
        "archer on the east coast.",
        "He's ninety-one. I'm giving",
        "him every chance."])
    later = S.say("Rook", [
        "Standing in the rain is two",
        "points. Standing in the rain",
        "on purpose is one. We're",
        "quite strict."])
    return _pair(first, later)


def morrow_pages():
    first = S.say("Morrow", [
        "Lucan Morrow. I edit the",
        "newsletter. There's one on the",
        "table. It's free. It's always",
        "been free."])
    first += S.say("Morrow", [
        "I'm rival to a Mr Pennock,",
        "who is a very great wizard.",
        "He doesn't know. I write to",
        "him at Christmas."])
    first += S.narrate(["You ask whether he writes back."])
    first += S.say("Morrow", [
        "Every year. A lovely card.",
        "He thinks I'm his cousin."])
    later = S.say("Morrow", [
        "Next issue's the Midsummer",
        "meeting. Rook was silent for",
        "an hour. Some of us thought",
        "it was the meeting."])
    return _pair(first, later)


def blackwood_pages():
    first = S.narrate([
        "A young man in a brown hood, on a stool by the fire, in",
        "the warmest and brightest seat in the inn, brooding as",
        "hard as he possibly can."])
    first += S.say("Blackwood", [
        "Hello! Kit Blackwood.",
        "I'm new. I'm first on the",
        "waiting list for a corner."])
    first += S.say("Blackwood", [
        "Any corner. I've been first",
        "on it since March."])
    first += S.say("Blackwood", [
        "It's quite hard to brood by",
        "a fire. I'm getting better.",
        "Mr Crake says I have a gift",
        "for a long silence."])
    first += S.narrate(["You ask whose rival he is."])
    first += S.say("Blackwood", [
        "Nobody's yet. There's a",
        "list for that, too."])
    later = S.say("Blackwood", [
        "Still first!",
        "Any day now."])
    return _pair(first, later)


def garrow_pages():
    first = S.say("Mrs Garrow", [
        "They're no trouble, love. They tip",
        "beautifully, and they put the chairs back."], face=False)
    first += S.say("Mrs Garrow", [
        "Four in the corners and the young one by",
        "the fire, every night of the year, and the",
        "middle of the room empty as a church."], face=False)
    first += S.narrate(["You ask whether anybody ever sits in the middle."])
    first += S.say("Mrs Garrow", [
        "Once. A tinker, in the rain. They were",
        "ever so nice to him. He left before his",
        "pie came."], face=False)
    later = S.say("Mrs Garrow", [
        "Sit anywhere you like, love.",
        "Anywhere in the middle."], face=False)
    return _pair(first, later)


def hart_events():
    w, h, x1, y1, x2, y2, door_x = ROOM
    evs = [S.exit_tile(1, "Sable Hart Door", door_x, y2 + 2,
                       MAP_WORLD, *SABLE_HART_STEP)]
    people = [
        (2, "Hollin Crake", CRAKE, 0, crake_pages),
        (3, "Silas Veyle", VEYLE, 3, veyle_pages),
        (4, "Thaddeus Rook", ROOK, 2, rook_pages),
        (5, "Lucan Morrow", MORROW, 1, morrow_pages),
        (6, "Kit Blackwood", BLACKWOOD, 4, blackwood_pages),
    ]
    for eid, name, xy, cell, pages in people:
        evs.append(_person(eid, name, xy, R.image("Gen_People4", cell,
                                                  direction=2), *pages()))
    evs.append(_person(7, "Mrs Garrow", GARROW,
                       R.image("People4", 5, direction=2), *garrow_pages()))

    page = dict(img=R.image(""), trigger=0, priority=1, direction_fix=True)

    # 8: the league table, which stops at fourth, because the rota is pinned
    # over the rest of it. COR-3's payoff is further down.
    league = S.narrate([
        "THE LEAGUE TABLE, in a careful hand and ruled in red:",
        "   1. S. VEYLE ......... 41   (the scar)",
        "   2. L. MORROW ....... 37   (a vow, in the rain)",
        "   3. H. CRAKE ......... 36"])
    league += S.narrate([
        "   4. T. ROOK ........... 35   (under review, by himself)"])
    league += S.narrate([
        "The rest of it is under the rota, which is pinned over the",
        "bottom half with four pins. It goes on for some way.",
        "Somebody has put in a fifth pin, to be sure."])
    evs.append(R.event(8, "The League Table", *LEAGUE,
                       [R.page(league, **page)]))

    # 9: the rota.
    rota = S.narrate([
        "THE CORNER ROTA - the darkest one (north-east).",
        "   This week: Mr Veyle.  Then Mr Rook.  Then Mr Crake.",
        "   Then Mr Morrow.  Then Mr Veyle again, which is fair."])
    rota += S.narrate([
        "   WAITING LIST FOR A CORNER: Mr Blackwood (1st).",
        "",
        "Underneath, in capitals: NOBODY TO BROOD IN IT OUT OF",
        "TURN, HOWEVER RAINY."])
    evs.append(R.event(9, "The Corner Rota", *ROTA, [R.page(rota, **page)]))

    # 10: the newsletter, on Morrow's table.
    news = S.narrate([
        "OVERSHADOWED. The newsletter of the Sable Hart. Issue",
        "one hundred and twelve. Very nicely done."])
    news += S.narrate([
        "Congratulations to Mr Veyle on his scar. Mr Blackwood's",
        "first dramatic exit is postponed until the door is",
        "planed; it sticks."])
    news += S.narrate([
        "Apologies for absence: C. Ash (as ever). Mr Ash remains",
        "a member in good standing, and his chair is kept."])
    evs.append(R.event(10, "The Newsletter", MORROW[0] - 1, MORROW[1],
                       [R.page(news, **page)]))

    # 11: the middle of the room.
    empty = S.narrate([
        "A table in the middle of the room, in the light, with a",
        "stool at each end. There is dust on both stools."])
    evs.append(R.event(11, "An Empty Table", *MIDDLE[1],
                       [R.page(empty, **page)]))

    # 12: the fire, which the stock fireplace does not have. `!Flame` 3
    # facing left is the middle-sized one of its four rows.
    evs.append(R.event(12, "The Fire", *HEARTH, [R.page(
        [], img=R.image("!Flame", 3, direction=4), trigger=0, priority=0,
        step_anime=True, direction_fix=True)]))
    return evs


# ================================================================ the doors ==
def world_doors(base_id, cells):
    """The real door into the Sable Hart, on the world map.

    `cells` is the one square `worldmap.json` put a placeholder on for this
    site, handed in by `journey.world_map`. Player-touch and below characters,
    the world map's idiom for a place you walk into."""
    w, h, x1, y1, x2, y2, door_x = ROOM
    evs = []
    for i, (x, y) in enumerate(sorted(cells)):
        arrive = S.narrate([
            "A house with a green roof, alone on the waste, with a",
            "painted sign over the door: a black stag, and THE SABLE",
            "HART. Every curtain in it is drawn."])
        arrive += R.choice_block(
            ["Go in", "Press on"],
            [[R.transfer(MAP_SABLE_HART, door_x, y2, 8, 0)],
             S.narrate(["You press on. Behind you a curtain moves, and is",
                        "put back exactly as it was."])])
        evs.append(R.event(base_id + i, SITE, x, y, [R.page(
            arrive, img=R.image(""), trigger=1, priority=0, through=True)]))
    return evs


def build():
    R.save_map(MAP_SABLE_HART, hart_map())
