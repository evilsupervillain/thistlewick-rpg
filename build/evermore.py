"""Maps 38-39: Olde Evermore, and the Forbidden Archive.

`../SITES.md` step 4. `../BIOS.md` is the bio: **Mirabel**, aged 4,112 (eight
and a quarter), Last Oracle of the hidden elven village that every party finds
eventually, by falling off the same ledge. Her prophecies are in the Old Tongue,
flawless and terrible, and delivered from a stepstool; she has to be in bed by
half past seven. The Elders call her Grandmother and are sent up the ladder for
things on the top shelf of the Forbidden Archive.

One site and one module, so it exports `SITE` and `world_doors` the way
`penultima.py` and `restwell.py` do. `Village C` is one cell.

* **No world-map coordinate is written here or in `places.py`.** The door cell
  is handed in by `journey.world_map` off the placeholder it replaces;
  `places.EVERMORE_STEP` is the one square this game chose, one south of it.
  `../WORLDMAP.md` 7.6.
* **Everybody arrives by falling off the ledge**, so the world-map door is a
  choice to look over the edge, and the village's way in is a heap of leaves
  under the cliff with a sign on it that says ARRIVALS. Its way out is a
  perfectly good path, which nobody has ever come in by.
* **This site touches the spine**, and nothing in it may contradict the
  finale. The Prophecy there is a scroll, clause twelve is the clause that
  renews the Dark Lord, and Grimspite calls it a renewal notice. So: Mirabel
  was at the signing and was bored, and drew a horse in the margin; the
  Archive keeps a fair copy made at the signing, by a copyist who copied
  everything, and the horse is in the margin **beside clause twelve**. Asked
  who the villain really is, she draws it, and it is a horse - "I'm only very
  good at horses." The game never connects the two horses and never says what
  the villain is. A player who has read the Prophecy's own item description
  (clause twelve "underlined by somebody worried") and then reaches the top of
  the Tower can do it for themselves. Nothing here says where the original is,
  who signed it, or when, so nothing here can disagree with the Tower.
* **The Register A candidate is mechanism two, the leaky child** (`../NORTH.md`
  1.3). An oracle is a child who can leak news nobody has told her yet: Elder
  Lirien is going to have a baby, Mirabel foresaw it and told them at
  breakfast, and she has known "since the ninth of March." Every word is
  literal - an oracle being precise about when she foresaw something - and the
  line is funny without its second reading, because the baby is going to be
  called Biscuit. 1.6's rule about child characters applies to her exactly as
  written: she is the reporter, the secret she thinks she is telling is the
  name, and the joke is her innocence. The Elders go red and cannot stop
  smiling, which is making the red worse. Nobody is unhappy.
* **She has to be in bed by half past seven**, and the Archive's clock says a
  quarter past, and has for some time, because its pendulum is tied up with a
  hair ribbon. A child who is four thousand years old has had a very long
  time to work out how to stay up.
* **Tiles.** The stepstool is `Stool A`, under her on layer 2. The top shelf
  is `Wood Ladder`, three cells up the north wall against the bookcases, with
  Elder Faelan at its foot. The Archive's copy of the Prophecy is `Scrolls B`
  on a `Table D`; the bed is `Bed`, in the corner. The village's cliffs are
  `Ledge A (Meadow)` over `Meadow` and `Dirt (Meadow)`, one family, and the
  landing is `Outside_B`'s `Fallen Leaves`, which is open.
"""
import mapkit as K
import rmmzdata as R

import story as S
from places import MAP_WORLD, MAP_EVERMORE, MAP_ARCHIVE, EVERMORE_STEP

# The name `worldmap.json`'s door event carries.
SITE = "Olde Evermore"

# ------------------------------------------------------------ the village ---
VW, VH = 26, 24
MASS = K.CLIFF_TOP              # Ledge A (Meadow)
FACE = K.CLIFF_FACE             # and its face
GROUND = K.GRASS                # Meadow: the same family as the ledge
PATH = K.PATH                   # Dirt (Meadow)
PATH_X = 12                     # the path: columns 12 and 13

ARRIVE = (PATH_X, 6)            # under the ledge, in the leaves
GATE = [(PATH_X, VH - 1), (PATH_X + 1, VH - 1)]

# The Forbidden Archive, and three houses. A building's only face is its
# south side, and every front here opens onto the hollow's floor.
ARCHIVE_B = (15, 8, 9, 6)
ARCHIVE_DOOR = (19, ARCHIVE_B[1] + ARCHIVE_B[3] - 1)
ARCHIVE_OUT = (ARCHIVE_DOOR[0], ARCHIVE_DOOR[1] + 1)
HOUSES = [(3, 8, 6, 5), (3, 17, 5, 4), (15, 17, 5, 4)]

ARRIVALS_AT = (11, 7)
SIGN_AT = (11, 20)
NOTICE_AT = (21, 14)
RAKER_AT = (15, 6)

LEAVES = K.sf_tile("Outside_B", "Fallen Leaves")

# ------------------------------------------------------------ the archive ---
#            w   h  x1  y1  x2  y2  door_x
ROOM = (19, 15, 3, 4, 15, 11, 9)
STOOL = (9, 7)                  # Mirabel, on her stepstool
LIRIEN = (11, 7)
LADDER_X = 5                    # Elder Faelan, at the foot of the ladder
COPY = (4, 9)                   # the Archive's copy of the Prophecy
CLOCK_X = 12
BED = (15, 10)                  # its lower cell is the event's

TABLE_D = K.sf_tile("Inside_B", "Table D")
STEPSTOOL = K.sf_tile("Inside_B", "Stool A")
LADDER = K.sf_block("Inside_B", "Wood Ladder")
CLOCK = K.sf_block("Inside_B", "Clock")
BEDSTEAD = K.sf_block("Inside_B", "Bed")
SCROLLS = K.sf_tile("Inside_C", "Scrolls B")
SCROLLS2 = K.sf_tile("Inside_C", "Scrolls A")
CRYSTAL = K.sf_tile("Inside_C", "Crystal Ball")
BOOKS = K.sf_tile("Inside_C", "Closed Books C")


# ============================================================== the village ==
def evermore_map():
    w, h = VW, VH
    g = K.Canvas(w, h)
    g.fill(0, 0, w - 1, h - 1, 0, GROUND)

    # The hollow: the ledge everybody falls off across the top, ledge down
    # both sides and along the bottom, and the path the only way through it.
    g.fill(0, 0, w - 1, 5, 0, MASS)
    g.fill(0, 6, 1, h - 1, 0, MASS)
    g.fill(w - 2, 6, w - 1, h - 1, 0, MASS)
    g.fill(2, h - 2, PATH_X - 1, h - 1, 0, MASS)
    g.fill(PATH_X + 2, h - 2, w - 3, h - 1, 0, MASS)
    g.fill(2, 6, 3, 7, 0, MASS)
    g.fill(22, 6, 23, 7, 0, MASS)

    g.fill(PATH_X, 6, PATH_X + 1, h - 1, 0, PATH)
    g.fill(PATH_X + 2, ARCHIVE_OUT[1], ARCHIVE_OUT[0], ARCHIVE_OUT[1], 0, PATH)
    g.fill(5, 13, PATH_X - 1, 13, 0, PATH)
    g.fill(5, 21, PATH_X - 1, 21, 0, PATH)
    g.fill(PATH_X + 2, 21, 17, 21, 0, PATH)
    g.fill(21, 16, 23, 18, 0, K.WATER)            # a pond, by the ledge

    g.dungeon_walls(MASS, FACE)

    g.building(*ARCHIVE_B, wall=K.WALL_MOSS_STONE, roof=K.ROOF_GREEN)
    walls = [K.WALL_LOG, K.WALL_PLANK_LIGHT, K.WALL_TIMBER]
    for (x, y, bw, bh), wall in zip(HOUSES, walls):
        g.building(x, y, bw, bh, wall=wall, roof=K.ROOF_GREEN)
    g.autotile(0)

    # Trees along the tops of the ledge, so the hollow reads as a hollow in a
    # forest rather than a hole in a lawn. Only where a whole two-by-two is
    # ledge top - never on a face.
    def top(x, y):
        return R.autotile_kind(g.get(x, y, 0)) == R.autotile_kind(MASS)
    for y in range(0, h - 1, 2):
        for x in range(y // 2 % 2, w - 1, 2):
            if all(top(x + dx, y + dy) for dx in (0, 1) for dy in (0, 1)):
                g.blit(x, y, 3, K.TREE)

    # The landing: leaves, raked into a heap under the ledge every morning.
    for x, y in [(12, 6), (13, 6), (12, 7), (13, 7), (11, 6), (14, 6),
                 (12, 8), (13, 8)]:
        g.set(x, y, 2, LEAVES)

    # The Archive: two tall stained windows either side of its door.
    g.column(ARCHIVE_DOOR[0] - 2, ARCHIVE_DOOR[1] - 1, 3, K.WINDOW_GLASS)
    g.column(ARCHIVE_DOOR[0] + 2, ARCHIVE_DOOR[1] - 1, 3, K.WINDOW_GLASS)

    for x, y, bw, bh in HOUSES:
        fy = y + bh - 1
        g.column(x + 2, fy - 1, 3, K.DOOR_SHUT)
        g.set(x + 4, fy, 3, K.WINDOW)
        g.set(x + 1, y, 2, K.STOVEPIPE)

    g.set(*ARRIVALS_AT, 3, K.SIGNPOST)
    g.set(*SIGN_AT, 3, K.SIGNPOST)
    g.set(*NOTICE_AT, 3, K.SIGNPOST)
    g.scatter([(10, 16)], 3, K.TUB)                     # the well
    g.scatter([(22, 17), (23, 16)], 3, K.LILYPAD)
    g.scatter([(9, 9), (20, 15), (4, 14), (22, 20), (9, 18)], 3, K.BUSH)
    g.scatter([(10, 10), (14, 11), (8, 15), (19, 21), (15, 15), (5, 15),
               (10, 19), (16, 15), (21, 21)], 3, K.FLOWERS2)
    g.scatter([(10, 8), (14, 16), (17, 7), (20, 7)], 3, K.FLOWERS)
    g.scatter([(3, 13), (9, 12)], 3, K.MUSHROOMS)
    for x, y in [(9, 6), (6, 15), (20, 19), (8, 19)]:
        g.blit(x, y, 3, K.TREE)

    m = K.new_map(w, h, K.TS_OUTSIDE, name="Olde Evermore", bgm="Town4")
    m["data"] = g.data
    m["events"] = [None] + evermore_events()
    return m


def evermore_events():
    evs = []

    # 1-2: the path out, both columns of it.
    for i, cell in enumerate(GATE):
        evs.append(S.exit_tile(i + 1, "The Path Out", *cell, MAP_WORLD,
                               *EVERMORE_STEP))

    # 3: the sign by the leaves.
    arrivals = S.narrate(["\\C[14]ARRIVALS\\C[0]"])
    arrivals += S.narrate([
        "The leaves under the ledge are raked into a deep,",
        "soft heap every morning, and fluffed up again after",
        "each arrival. It is somebody's whole job."])
    arrivals += [S.trope()]
    evs.append(R.event(3, "The Arrivals Sign", *ARRIVALS_AT, [R.page(
        arrivals, img=R.image(""), trigger=0, priority=1, through=True,
        direction_fix=True)]))

    # 4: the Archive.
    evs.append(S.door(4, "The Forbidden Archive", *ARCHIVE_DOOR, MAP_ARCHIVE,
                      ROOM[6], ROOM[5]))

    # 5: the Archive's notice.
    notice = S.narrate([
        "\\C[14]THE FORBIDDEN ARCHIVE\\C[0]",
        "",
        "The Oracle receives visitors until a quarter past",
        "seven. Bedtime is half past. This is not a prophecy."])
    notice += S.narrate([
        "Underneath, in a very careful hand, somebody small",
        "has added:",
        "",
        "   IT IS NOT HALF PAST YET."])
    evs.append(R.event(5, "The Archive Notice", *NOTICE_AT, [R.page(
        notice, img=R.image(""), trigger=0, priority=1, through=True,
        direction_fix=True)]))

    # 6: the village sign, by the path out.
    sign = S.narrate([
        "\\C[14]OLDE EVERMORE\\C[0]",
        "Hidden Village of the Elves. Since the First Age."])
    sign += S.narrate([
        "Underneath, smaller:",
        "",
        "   VISITORS ARE ASKED TO ARRIVE BY THE LEDGE,",
        "   AS IS TRADITIONAL."])
    evs.append(R.event(6, "The Village Sign", *SIGN_AT, [R.page(
        sign, img=R.image(""), trigger=0, priority=1, through=True,
        direction_fix=True)]))

    # 7: whoever's job it is.
    raker = S.say("Elf", [
        "You'll have come off the ledge.",
        "Everybody does. It's the only way in."])
    raker += S.narrate(["You ask whether there is a way out."])
    raker += S.say("Elf", [
        "Down the path, past the well.",
        "Nobody's ever come in by it. We did ask."])
    raker += [R.self_switch("A", True)]
    again = S.say("Elf", ["Mind the leaves. I've just done them."])
    img = R.image("People2", 1, direction=4)
    evs.append(S.npc(7, "The Raker", *RAKER_AT, raker, "People2", 1,
                     direction=4, pages=[R.page(
                         again, img=img, trigger=0, priority=1,
                         conditions={"selfSwitchValid": True,
                                     "selfSwitchCh": "A"})]))
    return evs


# ============================================================= the archive ==
def archive_map():
    w, h, x1, y1, x2, y2, door_x = ROOM
    g = K.interior(w, h, x1, y1, x2, y2, door_x=door_x,
                   floor=K.IN_PARQUET, wall_top=K.IN_WALL_TOP_GOLD,
                   wall_face=K.IN_WALL_FACE_GOLD)

    # A red runner from the door to the stepstool. Layer 1 is floor art.
    g.fill(door_x, STOOL[1] + 1, door_x, y2 + 1, 1, K.IN_RED_CARPET)
    g.autotile(1)

    # The north wall is shelves, floor to ceiling, and the ladder up to the
    # top shelf is three cells tall against them. The clock stands between.
    shelves = [K.IN_BOOKCASE, K.IN_BOOKCASE2, K.IN_BOOKSHELF]
    for i, x in enumerate([3, 4, 6, 7, 8, 14, 15]):
        g.column(x, y1 - 1, 3, shelves[i % 3])
    g.column(LADDER_X, y1 - 2, 3, LADDER)
    g.column(CLOCK_X, y1 - 1, 3, CLOCK)
    g.column(10, y1 - 2, 3, K.IN_STAINED_GLASS)

    # Shelves down the west wall too.
    g.column(x1, 6, 3, K.IN_BOOKCASE)

    # The stepstool, under her.
    g.set(STOOL[0], STOOL[1], 2, STEPSTOOL)

    # The reading table: the Archive's copy of the Prophecy, and the rest of
    # the reading beside it.
    g.set(COPY[0], COPY[1], 2, TABLE_D)
    g.set(COPY[0], COPY[1], 3, SCROLLS)
    g.set(COPY[0] + 1, COPY[1], 2, TABLE_D)
    g.set(COPY[0] + 1, COPY[1], 3, SCROLLS2)
    g.set(13, 8, 2, TABLE_D)
    g.set(13, 8, 3, CRYSTAL)
    g.set(14, 8, 2, TABLE_D)
    g.set(14, 8, 3, BOOKS)

    # Her bed, in the corner, turned down.
    g.column(BED[0], BED[1], 3, BEDSTEAD)

    g.set(x1, y2, 3, K.INC_PLANT2)
    g.set(7, y2, 3, K.INC_PLANT2)
    g.set(11, y2, 3, K.INC_PLANT2)

    m = K.new_map(w, h, K.TS_INSIDE, name="The Forbidden Archive",
                  bgm="Scene2")
    m["data"] = g.data
    m["events"] = [None] + archive_events()
    return m


def mirabel_pages():
    """Four pages, one after another: the prophecy and the biscuit; the
    Prophecy of Thistlewick and the horse; the secret; bedtime."""
    first = S.narrate([
        "On a stepstool in the middle of the Archive stands",
        "a very small girl with long silver hair, a silver",
        "circlet, and the look of somebody who has seen all",
        "of this before."])
    first += S.narrate([
        "She has. She is the Last Oracle of Olde Evermore,",
        "and she is four thousand one hundred and twelve."])
    first += S.say("Elder Lirien", [
        "And a quarter.",
        "She likes the quarter mentioned."])
    first += S.say("Mirabel", ["Eight and a QUARTER."])
    first += S.narrate([
        "She lifts her hands. Every candle in the Archive",
        "leans towards her. She speaks in the Old Tongue,",
        "and it is flawless, and it is terrible."])
    first += S.say("Elder Lirien", [
        "\"When the moon devours the sun,",
        "and the last bell falls silent,",
        "the one who was not chosen shall...\""])
    first += S.say("Mirabel", ["...is that a biscuit?"])
    first += S.narrate([
        "It is. It is in your pocket. You had forgotten it",
        "was there. She had not."])
    first += S.narrate([
        "You give her the biscuit. The prophecy does not",
        "get finished, and nobody seems to mind."])
    first += S.say("Elder Lirien", [
        "It never does. She's been doing",
        "that one since the Second Age.",
        "It's always a biscuit."])
    first += [S.trope(), R.self_switch("A", True)]

    horse = S.narrate(["You ask about the Prophecy of Thistlewick."])
    horse += S.say("Mirabel", [
        "I was there when they signed it.",
        "It was ever so long. Everybody had",
        "to sign it three times."])
    horse += S.say("Mirabel", ["So I drew a horse on it."])
    horse += S.say("Elder Faelan", [
        "In the margin. Of a sacred and",
        "binding instrument. Grandmother."])
    horse += S.say("Mirabel", ["It's a good horse."])
    horse += S.narrate(["You ask her who the villain really is."])
    horse += S.say("Mirabel", [
        "I know. I'm not allowed to SAY.",
        "I'll draw it."])
    horse += S.narrate([
        "She draws for a long time, with her tongue out of",
        "the corner of her mouth, and then she shows you."])
    horse += S.narrate(["It is a horse."])
    horse += S.narrate([
        "You say, carefully, that it is a very good horse."])
    horse += S.say("Mirabel", [
        "It's not a horse. It's the villain.",
        "I'm only very good at horses."])
    horse += [R.self_switch("B", True)]

    secret = S.say("Mirabel", [
        "Do you want to know a secret?",
        "A real one. Not a prophecy."])
    secret += S.say("Mirabel", [
        "Elder Lirien is going to have",
        "a baby."])
    secret += S.narrate([
        "Across the Archive, Elder Lirien drops a scroll.",
        "At the foot of the ladder, Elder Faelan stops",
        "moving altogether."])
    secret += S.say("Mirabel", [
        "I foresaw it. I told them at",
        "breakfast. They didn't know yet."])
    secret += S.say("Mirabel", ["I've known since the ninth of March."])
    secret += S.narrate([
        "Elder Lirien picks up the scroll. It takes her a",
        "long time. Elder Faelan has gone the colour of the",
        "carpet. Neither of them can stop smiling, which is",
        "making the colour worse."])
    secret += S.say("Mirabel", [
        "It's a girl. She's going to be",
        "called Biscuit."])
    secret += S.say("Elder Faelan", [
        "She is not going to be called",
        "Biscuit."])
    secret += S.say("Mirabel", ["She is, though."])
    secret += [S.blush(), R.self_switch("C", True)]

    bedtime = S.say("Mirabel", [
        "It's nearly half past seven.",
        "I'm not tired."])
    bedtime += S.narrate(["She yawns, enormously, on the stepstool."])
    bedtime += S.say("Mirabel", [
        "I have seen the fall of empires.",
        "I can see the clock. It says",
        "a quarter past."])
    return first, horse, secret, bedtime


def archive_events():
    w, h, x1, y1, x2, y2, door_x = ROOM
    evs = [S.exit_tile(1, "The Door", door_x, y2 + 2, MAP_EVERMORE,
                       *ARCHIVE_OUT)]

    # 2: Mirabel, on her stepstool, facing the door. Each page sets the self
    # switch the next one waits on, and the engine takes the last page whose
    # condition holds.
    first, horse, secret, bedtime = mirabel_pages()
    img = R.image("Gen_People2", 4, direction=2)

    def after(ch):
        return {"selfSwitchValid": True, "selfSwitchCh": ch}
    evs.append(R.event(2, "Mirabel", *STOOL, [
        R.page(first, img=img, trigger=0, priority=1),
        R.page(horse, img=img, trigger=0, priority=1, conditions=after("A")),
        R.page(secret, img=img, trigger=0, priority=1, conditions=after("B")),
        R.page(bedtime, img=img, trigger=0, priority=1,
               conditions=after("C")),
    ]))

    # 3: Elder Lirien, who translates.
    lirien = S.say("Elder Lirien", [
        "Elder Lirien. I translate for",
        "Grandmother, when she prophesies,",
        "and when she asks for pudding."])
    lirien += S.narrate(["You ask how you tell the difference."])
    lirien += S.say("Elder Lirien", ["The pudding is more urgent."])
    lirien += S.say("Elder Lirien", [
        "She has to be in bed by half past",
        "seven. We tried eight, once."])
    lirien += S.narrate(["You ask what happened."])
    lirien += S.say("Elder Lirien", [
        "She foresaw the fall of an empire",
        "in the middle of supper, out of",
        "sheer tiredness. It was only a",
        "small empire. Still."])
    lirien += [R.self_switch("A", True)]
    lirien_again = S.say("Elder Lirien", [
        "Half past seven.",
        "Not a minute after."])
    limg = R.image("Nature", 6, direction=4)
    evs.append(R.event(3, "Elder Lirien", *LIRIEN, [
        R.page(lirien, img=limg, trigger=0, priority=1),
        R.page(lirien_again, img=limg, trigger=0, priority=1,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ]))

    # 4: Elder Faelan, at the foot of the ladder, fetching something down.
    faelan = S.say("Elder Faelan", [
        "Elder Faelan. Forgive me - I am",
        "fetching the Chronicle of the Second",
        "Age for Grandmother."])
    faelan += S.narrate(["You ask why he calls her Grandmother."])
    faelan += S.say("Elder Faelan", [
        "Everybody does. She was old when",
        "my grandmother was a girl, and my",
        "grandmother was a girl for a long",
        "time."])
    faelan += S.narrate(["You ask why the Chronicle is on the top shelf."])
    faelan += S.say("Elder Faelan", [
        "So that she can't reach it.",
        "She reads the endings first."])
    # TIMELINE.md section 1, "Who notices": the further from Thistlewick's
    # committees, the more plainly the clock is seen, and the elves simply say
    # it. The Forty-Seventh came through in 1990; the Age is not Thistlewick's.
    faelan += S.narrate(["You mention that you are the Forty-Eighth."])
    faelan += S.say("Elder Faelan", [
        "Are you! The Forty-Seventh came",
        "off the ledge ten years ago. A",
        "lovely boy. Landed on his feet."])
    faelan += S.say("Elder Faelan", [
        "Your Committee will have told",
        "you it was a hundred years. It",
        "counts the way the Prophecy does.",
        "We count the way the sun does."])
    faelan += S.narrate(["You say that the Age began with the Prophecy."])
    faelan += S.say("Elder Faelan", [
        "The Age began with a great many",
        "things. The Prophecy was the one",
        "with a clerk present."])
    faelan += [R.self_switch("A", True)]
    faelan_again = S.say("Elder Faelan", [
        "The top shelf. It is always the",
        "top shelf."])
    fimg = R.image("Actor3", 0, direction=8)
    evs.append(R.event(4, "Elder Faelan", LADDER_X, y1, [
        R.page(faelan, img=fimg, trigger=0, priority=1),
        R.page(faelan_again, img=fimg, trigger=0, priority=1,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ]))

    # 5: the Archive's copy of the Prophecy of Thistlewick. What is in its
    # margin, and beside which clause, is the whole of this site's statement
    # about the spine - see the docstring.
    copy = S.narrate([
        "On the reading table, under a sign that says",
        "FORBIDDEN in four languages: the Archive's copy of",
        "the Prophecy of Thistlewick, made at the signing."])
    copy += S.narrate([
        "It is very long and dense with clauses, and signed",
        "by everybody three times. The copyist was told to",
        "copy everything. The copyist copied everything."])
    copy += S.narrate([
        "In the margin beside clause twelve, very small and",
        "in wax crayon, somebody has drawn a horse."])
    copy += S.narrate(["It is quite a good horse."])
    page = dict(img=R.image(""), trigger=0, priority=1, direction_fix=True)
    evs.append(R.event(5, "The Archive Copy", *COPY, [R.page(copy, **page)]))

    # 6: the clock, which says a quarter past seven.
    clock = S.narrate([
        "A tall clock, beautifully kept. It says a quarter",
        "past seven."])
    clock += S.narrate([
        "The pendulum is not moving. It has been tied to",
        "the side of the case with a hair ribbon, in a",
        "very neat bow."])
    evs.append(R.event(6, "The Clock", CLOCK_X, y1, [R.page(clock, **page)]))

    # 7: her bed. The lower cell, because the bed blocks both.
    bed = S.narrate([
        "A small bed in the corner, turned down, with a",
        "stone hot-water bottle already in it."])
    bed += S.narrate([
        "On the pillow is a note in the Old Tongue. It is",
        "flawless, and it is terrible, and Elder Lirien",
        "translates it without looking up."])
    bed += S.say("Elder Lirien", ["\"Not tired.\""])
    evs.append(R.event(7, "Mirabel's Bed", BED[0], BED[1] + 1,
                       [R.page(bed, **page)]))
    return evs


# ================================================================ the door ==
def world_doors(base_id, cells):
    """The real door on Map 8. Everybody finds Olde Evermore by falling off
    the same ledge, so the door is a choice to look over it."""
    evs = []
    for i, (x, y) in enumerate(sorted(cells)):
        arrive = S.narrate([
            "A ledge, and below it, through the trees, the",
            "glint of rooftops that are not on any map."])
        arrive += R.choice_block(
            ["Look over the edge", "Press on"],
            [S.narrate(["You lean out to look. A little further than you",
                        "meant to."]) +
             [R.play_se("Fall"),
              R.transfer(MAP_EVERMORE, ARRIVE[0], ARRIVE[1], 2, 0)],
             S.narrate(["You press on, keeping well back from the edge."])])
        evs.append(R.event(base_id + i, SITE, x, y, [R.page(
            arrive, img=R.image(""), trigger=1, priority=0, through=True)]))
    return evs


def build():
    R.save_map(MAP_EVERMORE, evermore_map())
    R.save_map(MAP_ARCHIVE, archive_map())
