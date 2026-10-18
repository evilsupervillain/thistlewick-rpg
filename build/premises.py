"""Map 42: the Former Premises - the hall with the lift.

`../SITES.md` step 6, and `../WORLDMAP.md` 7.4 is the whole design. The
floating castle the Dark Lord was raised in for two thousand years, vacated on
**accessibility grounds** - a complaint about the climb, a second complaint, a
recommendation, and the engagement renegotiated onto a ground-floor site with a
door at the bottom, which is the Obligatory Tower. The one place in the world
you cannot walk to is the one abandoned for being impossible to get to.

One site and one module, so it exports `SITE` and `world_doors` the way
`evermore.py` does. `Floating Continent (Castle)` is **two** cells, and
`world_doors` gets both and makes a door on each.

* **It is air-only, and three engine rules follow from that**, all in the
  workspace `CLAUDE.md`'s bullet on vehicles. The action button offers the
  airship before any event, and `Game_Vehicle.isLandOk` refuses a square with
  an event on it - so **nothing stands on the island's land** (Mike redrew it
  as a floating island, P2, 7 Oct 2026; `places.PREMISES_LAND` is its castle
  row). The airship sets down on either cell, and a parallel event on the row
  underneath, which is sea, asks "Go in / Not yet" once the party is standing
  there - and asks again only after they have been back in the airship, so
  "Not yet" is not asked every frame. Both site events keep **`<aironly>`**,
  so `validate.py` goes on asserting that nobody can walk here.
* **The way out carries `<airreturn>`.** It puts the party back on the cell
  the airship is standing on, beside her or under her, with the question
  already answered for this landing; without the note `validate.py` would
  seed its on-foot flood from there. The note makes it check instead that
  each square is one an airship can be standing on.
* **One man and a great deal of paperwork.** Mr Prosper Hollowell, Caretaker
  (Retained), and the rule for writing him is 7.4's: *every single thing he
  says is good news.* He is not bitter and he is not mad. Filling the hall
  with anybody else would make it a place rather than a vacancy.
* **The lift is the sight** and it is not explained. `!$Gate2` character 1 is
  a pair of engraved stone doors that slide apart, which is what a lift looks
  like when nobody has invented one yet. It goes from the hall to the
  battlements, works perfectly, and always has. The climb that was complained
  about was the four thousand feet of sky underneath.
* **The visitors' book never leaves its lectern**, because it never has, so
  what he gives you for the incumbent to sign is a slip ruled to match, to be
  pasted in. `db.SW_VISITORS_BOOK` is set when he asks, and it is a global
  because the page that reads it is Grimspite's, on Map 12 -
  `journey.finale_event` appends it, `../NORTH.md` 1.7 pattern 2.
* **No Register A here, and it must not be forced** - 7.4 is explicit. One
  trope, for the floating castle of the ancients, and no blush.
* **Tiles.** `Wall K (Stone)` and `Interior Floor I (Marble)`, white and
  kept by somebody who polishes; `Wall O (Demon Castle)` is green gemstone,
  which is not what its name suggests. The old throne is the one thing left
  of the tenant - `Throne (Demon Castle)`, black and red, facing the door; the book is `Open Book A (V)` on
  the red-draped `Table C`; the deeds are `Map A (V)`, which is a plan, on a
  `Table D`; the quarterly reports are three `Bookshelf A`; the visitors'
  waiting area is `Sofa (Castle)`. The sconces are `!Flame` character 0 facing
  up, the three-candle wall candelabrum, as events with no commands.
"""
import mapkit as K
import rmmzdata as R

import db
import story as S
from places import MAP_WORLD, MAP_PREMISES, PREMISES_LAND, PREMISES_STEP
import q_spare

# The name `worldmap.json`'s door events carry.
SITE = "The Former Premises"

#            w   h  x1  y1  x2  y2  door_x
ROOM = (21, 15, 3, 4, 17, 11, 10)
THRONE_AT = (10, 4)             # 1x2; its lower cell is the event's
HOLLOWELL_AT = (10, 9)
LECTERN = (9, 9)
DEEDS = (14, 8)
SHELVES_X = (3, 4, 5)           # the quarterly reports, against the north wall
LIFT_AT = (16, 3)               # !$Gate2 is 3x2 cells, drawn up from here
SCONCES = [(8, 3), (12, 3)]
WINDOWS_X = (7, 13)
SOFA = (3, 9)                   # 5x2, top-left; a row of floor in front
PILLARS = [(8, 7), (12, 7), (8, 10), (12, 10)]     # base cells, down the aisle
DESK = (15, 10)                 # this quarter's report, begun this morning

WALL_TOP, WALL_FACE = K.IN_WALL_TOP_WHITE, K.IN_WALL_FACE_WHITE  # Wall K
FLOOR = K.sf_tile("Inside_A5", "Interior Floor I (Marble)")
THRONE = K.sf_block("Inside_B", "Throne (Demon Castle)")
WINDOW = K.sf_block("Inside_B", "Window (Demon Castle)")
TAPESTRY = K.sf_block("Inside_B", "Tapestry A")
BOOKSHELF = K.sf_block("Inside_B", "Bookshelf A")
SOFA_GRID = K.sf_grid("Inside_B", "Sofa (Castle)", 5)
TABLE_C = K.sf_tile("Inside_B", "Table C")
TABLE_D = K.sf_tile("Inside_B", "Table D")
OPEN_BOOK = K.sf_tile("Inside_C", "Open Book A (V)")
PLAN = K.sf_tile("Inside_C", "Map A (V)")
ARMOUR = K.sf_tile("Inside_C", "Armor A (Stand)")
PILLAR = K.sf_block("Inside_B", "Stone Pillar B")
REPORT = K.sf_tile("Inside_C", "Closed Books C")

LIFT_IMG = ("!$Gate2", 1)
SCONCE_IMG = ("!Flame", 0)


# ================================================================ the hall ==
def hall_map():
    w, h, x1, y1, x2, y2, door_x = ROOM
    g = K.interior(w, h, x1, y1, x2, y2, door_x=door_x, floor=FLOOR,
                   wall_top=WALL_TOP, wall_face=WALL_FACE)

    # A red runner from the door to the old throne. Layer 1 is floor art.
    g.fill(door_x, THRONE_AT[1] + 2, door_x, y2 + 1, 1, K.IN_RED_CARPET)
    g.autotile(1)

    # The north wall: the old throne under a tapestry, a window either side
    # of it onto nothing but sky, the reports on their shelves to the west
    # and the lift to the east.
    g.column(THRONE_AT[0], y1 - 2, 3, TAPESTRY)
    g.column(*THRONE_AT, 3, THRONE)
    for x in WINDOWS_X:
        g.column(x, y1 - 2, 3, WINDOW)
    for x in SHELVES_X:
        g.column(x, y1 - 1, 3, BOOKSHELF)

    # The lectern with the book on it, and the deeds on a table of their own.
    g.set(*LECTERN, 2, TABLE_C)
    g.set(*LECTERN, 3, OPEN_BOOK)
    g.set(*DEEDS, 2, TABLE_D)
    g.set(*DEEDS, 3, PLAN)
    g.set(*DESK, 2, TABLE_D)
    g.set(*DESK, 3, REPORT)

    # Pillars down the aisle, two either side of the runner.
    for x, y in PILLARS:
        g.column(x, y - 1, 3, PILLAR)

    # The visitors' waiting area. There has never been a wait.
    g.blit(*SOFA, 3, SOFA_GRID)

    # Armour down both sides, polished, on duty for nobody.
    for y in (6, 8):
        g.set(x1, y, 3, ARMOUR)
        g.set(x2, y, 3, ARMOUR)
    g.set(x2, y2, 3, K.INC_PLANT2)

    m = K.new_map(w, h, K.TS_INSIDE, name="The Former Premises",
                  bgm="Castle1")
    m["data"] = g.data
    m["events"] = [None] + hall_events()
    return m


def hollowell_pages():
    """The tour, and what he says every time after it."""
    t = S.narrate([
        "A man in a pressed suit is standing in the middle",
        "of the hall with a feather duster. He sees you,",
        "and his whole face lights up."])
    t += S.say("Hollowell", [
        "Visitors! Oh, VISITORS.",
        "Come in, come in, mind the step - no,",
        "there isn't one. Force of habit."])
    t += S.say("Hollowell", [
        "Prosper Hollowell. Caretaker.",
        "Retained. Welcome to the Former",
        "Premises!"])
    t += S.narrate([
        "He shakes your hand. He shakes everybody's hand.",
        "He comes back and shakes yours again, in case it",
        "did not take."])
    t += S.say("Hollowell", [
        "You came by AIR. Of course you did.",
        "It's the only way. That was rather",
        "the whole point of the place."])
    t += S.say("Hollowell", [
        "The tour starts here. It also ends",
        "here. It's one hall. I've been",
        "working on it."])
    t += S.narrate(["You ask what this place was."])
    t += S.say("Hollowell", [
        "The venue! Two thousand years of",
        "Dark Lords, raised up here by",
        "somebody's grandfather so that no",
        "hero could ever reach it."])
    t += S.say("Hollowell", [
        "And no hero ever did.",
        "It worked perfectly. Not one."])
    t += S.narrate([
        "He beams, as if this is the best news he has had",
        "in years. It may be."])
    t += S.say("Hollowell", [
        "Then there was a complaint, about",
        "the climb. Then a second one. Then",
        "a recommendation."])
    t += S.say("Hollowell", [
        "So they moved it all into a tower,",
        "with a door at the bottom. Ground",
        "floor. Very sensible. The heroes",
        "have to be able to ARRIVE, you see."])
    t += S.say("Hollowell", [
        "That was four thousand eight hundred",
        "years ago. I was retained. I've kept",
        "it ready ever since, in case it's",
        "re-let."])
    t += S.say("Hollowell", [
        "And the complaint was upheld! They",
        "put in a lift. Courtyard to the",
        "battlements. It works beautifully.",
        "It always has."])
    t += S.narrate([
        "You ask whether anybody has visited, in four",
        "thousand eight hundred years."])
    t += S.say("Hollowell", [
        "Not a soul! Everything's in perfect",
        "working order. Which brings me to",
        "the visitors' book."])
    t += S.say("Hollowell", [
        "Four thousand eight hundred years,",
        "and nobody in it. It's the one gap in",
        "the record. And you're going up the",
        "tower, aren't you? You've the look."])
    t += S.say("Hollowell", [
        "Would you ask the current incumbent",
        "to sign it? For the file?"])
    t += S.narrate(["You say that you will ask."])
    t += S.say("Hollowell", [
        "Splendid. SPLENDID. The book doesn't",
        "leave the lectern - it never has -",
        "but here's a slip, ruled to match.",
        "I'll paste it in."])
    t += S.narrate([
        "He gives you a slip of good paper, ruled into three",
        "columns: NAME, FROM and REMARKS."])
    t += [S.trope(), R.control_switch(db.SW_VISITORS_BOOK, True),
          R.self_switch("A", True)]

    again = S.say("Hollowell", [
        "Take the lift! Any time you like.",
        "It's always running. Beautifully."])
    return t, again


def hall_events():
    w, h, x1, y1, x2, y2, door_x = ROOM

    # 1: the way out, onto the island cell the airship is standing on, with
    # this landing's question already answered (`world_doors`).
    out = S.exit_tile(1, "The Door", door_x, y2 + 2, MAP_WORLD,
                      *PREMISES_STEP)
    (x0, y0), _ = PREMISES_LAND
    out["pages"][0]["list"] = [
        R.play_se("Move1"),
        R.script(["$gamePlayer._premisesAsked = true;"])[0]] + R.if_then(
        # x and y, not `pos()`: a vehicle's `pos` is false off its own
        # map, and the party is in the hall when this is asked.
        R.condition_script("$gameMap.airship()._mapId === %d && "
                           "$gameMap.airship().x === %d && "
                           "$gameMap.airship().y === %d"
                           % (MAP_WORLD, x0, y0)),
        [R.transfer(MAP_WORLD, x0, y0, 2, 0)],
        [R.transfer(MAP_WORLD, *PREMISES_STEP, 2, 0)]) + [
        {"code": 0, "indent": 0, "parameters": []}]
    out["note"] = "<airreturn>"
    evs = [out]

    # 2: Mr Prosper Hollowell, facing the door, as he has been for some time.
    tour, again = hollowell_pages()
    img = R.image("Gen_People2", 6, direction=2)
    evs.append(R.event(2, "Hollowell", *HOLLOWELL_AT, [
        R.page(tour, img=img, trigger=0, priority=1),
        R.page(again, img=img, trigger=0, priority=1,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ]))

    page = dict(img=R.image(""), trigger=0, priority=1, direction_fix=True)

    # 3: the visitors' book, and the one thing in the hall he is not pleased
    # about, which is never said - it is on the lectern face down.
    book = S.narrate([
        "The visitors' book, open on the lectern. It is",
        "ruled into three columns - NAME, FROM, REMARKS -",
        "and there is nothing in any of them, on any page,",
        "for four thousand eight hundred years."])
    book += S.narrate([
        "Beside it, face down, is a letter. It has been",
        "unfolded and folded again a great many times."])
    book += S.narrate([
        "\\C[14]NOTIFICATION OF CHANGE OF ADDRESS\\C[0]",
        "The Engagement has removed to: The Obligatory",
        "Tower. Ground floor. Door at the bottom.",
        "Please amend your records."])
    book += S.narrate([
        "It is dated this spring. It is from the Prophecy",
        "Committee, and it has been sent to him as a matter",
        "of course."])
    evs.append(R.event(3, "The Visitors' Book", *LECTERN,
                       [R.page(book, **page)]))

    # 4: the deeds.
    deeds = S.narrate([
        "The deeds of the Premises, with a plan. The builder",
        "is given as MALAGANT THE PROVISIONAL. The site is",
        "given as the sky, above the southern sea."])
    deeds += S.narrate([
        "Ott will want to know what holds it up, so you",
        "find the clause. Means of support:"])
    deeds += S.narrate(["\"As before.\""])
    deeds += S.narrate([
        "You read the deeds through twice, looking for the",
        "before. There isn't one."])
    evs.append(R.event(4, "The Deeds", *DEEDS, [R.page(deeds, **page)]))

    # 5: the quarterly reports, on the middle shelf's base cell.
    reports = S.narrate([
        "Quarterly reports, bound, one for every quarter",
        "since the lease lapsed: nineteen thousand two hundred",
        "of them. These are the copies. The originals were",
        "filed."])
    reports += S.narrate([
        "Tucked into each one is the reply. It is the same",
        "form letter every time:",
        "",
        "   THANK YOU FOR YOUR REPORT, WHICH HAS BEEN FILED."])
    reports += S.narrate([
        "The most recent runs to eleven pages, and it is",
        "mostly about the lift."])
    evs.append(R.event(5, "The Quarterly Reports", SHELVES_X[1], y1,
                       [R.page(reports, **page)]))

    # 6: the old throne. The lower cell, because the throne blocks both.
    throne = S.narrate([
        "The old throne, facing the door, black and red and",
        "polished to a shine. A dust sheet is folded on the",
        "seat, ready to go back over it the moment you",
        "leave."])
    evs.append(R.event(6, "The Old Throne", THRONE_AT[0], THRONE_AT[1] + 1,
                       [R.page(throne, **page)]))

    # 7: the lift. Its doors slide apart, and that is route codes 17, 18 and
    # 19 - turn left, right, up - walking the four rows of the sheet, so the
    # page must not fix its direction.
    def doors(codes):
        steps = []
        for c in codes:
            steps += [{"code": c, "parameters": []},
                      {"code": 15, "parameters": [4]}]
        return R.move_route(0, steps, repeat=False, wait_flag=True)
    ride = S.narrate([
        "\\C[14]LIFT\\C[0]  -  COURTYARD - BATTLEMENTS",
        "Commissioned following a complaint (upheld)."])
    ride += R.choice_block(
        ["Go up", "Leave it"],
        [[R.play_se("Open3")] + doors([17, 18, 19]) +
         [R.fadeout_screen(), R.play_se("Move1"), R.wait(30)] +
         S.narrate([
             "The lift goes up, smoothly and in perfect silence,",
             "to the battlements."]) +
         S.narrate([
             "From the battlements you can see four thousand",
             "feet of sky, straight down, all the way to the",
             "sea."]) +
         S.narrate([
             "The lift comes back down, smoothly and in perfect",
             "silence, to the hall. It does not go any further",
             "than that. Nobody asked it to."]) +
         [R.wait(20), R.fadein_screen(), R.play_se("Close1")] +
         doors([18, 17, 16]),
         []])
    evs.append(R.event(7, "The Lift", *LIFT_AT, [R.page(
        ride, img=R.image(*LIFT_IMG, direction=2), trigger=0, priority=1,
        walk_anime=False)]))

    # 8-9: the sconces, lit. Decoration: no commands at all.
    for i, (x, y) in enumerate(SCONCES):
        evs.append(R.event(8 + i, "Sconce", x, y, [R.page(
            [], img=R.image(*SCONCE_IMG, direction=8), trigger=0, priority=1,
            direction_fix=True, step_anime=True, walk_anime=False)]))

    # 10: the waiting area.
    sofa = S.narrate([
        "A sofa for visitors, in case of a wait. There has",
        "never been a wait. The cushions are plumped anyway,",
        "every morning."])
    evs.append(R.event(10, "The Waiting Area", SOFA[0] + 2, SOFA[1] + 1,
                       [R.page(sofa, **page)]))

    # 11: this quarter's report, which has news in it for the first time.
    report = S.narrate([
        "This quarter's report, begun this morning in a very",
        "neat hand. ITEM ONE: THE LIFT. It runs to four",
        "pages already."])
    report += S.narrate([
        "Under ITEM TWO: VISITORS, where every other report",
        "on the shelf says NONE, he has written \"Yes!\"",
        "and underlined it twice."])
    evs.append(R.event(11, "This Quarter's Report", *DESK,
                       [R.page(report, **page)]))
    evs.append(q_spare.courier("premises", 8, 11))                 # SPA-1
    return evs


# ================================================================ the door ==
def world_doors(base_id, cells):
    """The site's two events on Map 8, on the row under the castle - sea under
    a star tile, which nobody stands on - because the castle row itself has to
    stay bare for the airship. The first is the door: a parallel event that
    asks once the party is standing on the island, and again only after they
    have been back in the airship (`$gamePlayer._premisesAsked`, which the
    save keeps). The second does nothing and keeps the id the second door
    had, so that no event after it on Map 8 moves."""
    (door, spare) = sorted(cells)
    on_island = " || ".join("$gamePlayer.pos(%d, %d)" % c
                            for c in PREMISES_LAND)
    arrive = R.script(["$gamePlayer._premisesAsked = true;"])
    arrive += S.narrate([
        "A castle on a cloud, four thousand feet up, with",
        "nothing under it but the sea."])
    arrive += S.narrate([
        "The front door is open and the step has been",
        "swept. The mat says WELCOME. It has never been",
        "stood on."])
    arrive += R.choice_block(
        ["Go in", "Not yet"],
        [[R.play_se("Open1"),
          R.transfer(MAP_PREMISES, ROOM[6], ROOM[5], 8, 0)],
         []])
    watch = R.script([
        "if ($gamePlayer.isInAirship()) $gamePlayer._premisesAsked = false;"])
    watch += R.if_then(R.condition_script(
        "$gamePlayer.isNormal() && !$gamePlayer.isMoving() && "
        "!$gamePlayer._premisesAsked && (%s)" % on_island), arrive)
    return [
        R.event(base_id, SITE, *door, [R.page(
            watch, img=R.image(""), trigger=4, priority=0, through=True)],
            note="<aironly>"),
        R.event(base_id + 1, SITE + " (the second door, retired)", *spare,
                [R.page([], img=R.image(""), trigger=0, priority=0,
                        through=True)], note="<aironly>")]


def build():
    R.save_map(MAP_PREMISES, hall_map())
