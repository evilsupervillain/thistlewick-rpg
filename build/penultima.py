"""Maps 29-30: Penultima, and Ye Final Shoppe.

The first of the twenty-nine sites on the new world map to get a room behind
its door. `../WORLDMAP.md` item 10 is the effort; `../BIOS.md` is the bio, and
Gideon Markup is one of the six characters in it who has both a home on the map
and a finished look in `characters/`, which is why this is the one that went
first.

**Penultima: The Last Town Before The End. Last Chance For Potions.** It stands
on the tower road at (64,48), which is not where worldgen grew it - 7.2 moved
it forty-two cells west onto the approach every player walks up, and this room
is the payoff for that. The town is one street, because a town on the last
stretch of road before a Dark Lord is a place people pass through.

Three things are worth knowing before editing this:

* **The world-map door is not written here and its coordinates are not written
  anywhere in this game.** `journey.world_map` claims the site by *name* and
  builds the real door on whatever cells `worldmap.json` put the placeholder
  on. See `WORLDMAP.md` 7.6 and `SITE` below.
* **The Sword of Ultimate Ending is not an item and must not become one.** It
  is a prop in a window with a price card. `Game_Party.maxGold` is 99,999,999,
  so the bio's "one gold more than a purse can hold" is *wrong about the
  engine* - which is the joke, because Gideon priced it thirty-one years ago
  and has never checked. Put it in the shop list and it becomes a sword a rich
  player can buy, and the gag dies the moment somebody does the arithmetic.
* **The prices in the shop are the doubled ones, and the street says so first.**
  The Sighting Bell rings when you walk in, because you are a Chosen One on the
  road, and Gideon calls that "seasonal". Every price in his list is twice the
  database price, written as a custom price so nothing else in the game is
  touched by it.
"""
import mapkit as K
import rmmzdata as R

import db
import story as S
from places import MAP_WORLD, MAP_PENULTIMA, MAP_SHOPPE, PENULTIMA_STEP

# The name `worldmap.json`'s door events carry for this site, and the only
# thing that connects this module to the world map. `journey.world_map` looks
# it up, drops the placeholders that carry it, and builds real doors on their
# cells - so a re-stamp that moves Penultima moves its door with it and
# nothing here needs editing. WORLDMAP.md 7.6.
SITE = "Penultima"

# The street. One road west to east, the gate at the western end where the
# tower road comes in, and four buildings along it.
PW, PH = 28, 22
STREET_Y = 11                       # the road row the player walks in on
GATE = (0, STREET_Y)                # the gap in the fence, and the way out

SHOPPE = (8, 4, 7, 6)               # Gideon's, north side of the street
RIVAL = (18, 4, 6, 6)               # what used to be further on
HOUSE_W = (4, 14, 6, 5)
HOUSE_E = (17, 14, 6, 5)

SHOPPE_DOOR = (11, SHOPPE[1] + SHOPPE[3] - 1)
RIVAL_DOOR = (20, RIVAL[1] + RIVAL[3] - 1)
SHOPPE_OUT = (SHOPPE_DOOR[0], SHOPPE_DOOR[1] + 1)

# Ye Final Shoppe, in the same shape every interior in this game uses.
#            w   h  x1  y1  x2  y2  door_x
ROOM = (17, 16, 3, 4, 13, 10, 8)


# =============================================================== the street ==
def penultima_map():
    w, h = PW, PH
    g = K.Canvas(w, h)
    g.fill(0, 0, w - 1, h - 1, 0, K.GRASS)

    # The tower road comes in at the gate and becomes the street, which is
    # cobbled because Penultima is a town that thinks well of itself.
    # The street stops at x=24, because there is nothing further on - which
    # is what the boarded shop at the east end of it is about.
    g.fill(0, STREET_Y - 1, 6, STREET_Y, 0, K.PATH)
    g.fill(6, STREET_Y - 1, 24, STREET_Y, 0, K.COBBLE)
    g.fill(SHOPPE_DOOR[0], SHOPPE_DOOR[1] + 1, SHOPPE_DOOR[0],
           STREET_Y - 2, 0, K.COBBLE)
    g.fill(RIVAL_DOOR[0], RIVAL_DOOR[1] + 1, RIVAL_DOOR[0],
           STREET_Y - 2, 0, K.COBBLE)

    g.building(*SHOPPE, wall=K.WALL_PLANK_LIGHT, roof=K.ROOF_GREEN)
    g.building(*RIVAL, wall=K.WALL_PLASTER, roof=K.ROOF_BROWN)
    g.building(*HOUSE_W, wall=K.WALL_PLANK, roof=K.ROOF_BROWN)
    g.building(*HOUSE_E, wall=K.WALL_PLANK, roof=K.ROOF_BROWN)

    g.autotile(0)

    # Gideon's window is the whole point of Gideon's shop, so it is the thing
    # on the front wall, and the signs are the other side of the door.
    # **Not `WINDOW_GLASS`**, which is stained glass and put a chapel window on
    # a sword shop - it is what the chapel in Thistlewick is drawn with.
    g.set(SHOPPE_DOOR[0] + 1, SHOPPE_DOOR[1], 3, K.WINDOW)
    g.set(SHOPPE_DOOR[0] - 2, SHOPPE_DOOR[1], 3, K.SIGN_BLADE)
    g.set(SHOPPE_DOOR[0] - 1, SHOPPE_DOOR[1], 3, K.SIGN_POTION)

    # The rival's door is shut and has been for some time.
    g.set(RIVAL_DOOR[0] - 1, RIVAL_DOOR[1], 3, K.SIGN_ARMOR)
    # And a window, for the card in it that the door reads out (Mike, 30 Oct).
    g.set(RIVAL_DOOR[0] + 2, RIVAL_DOOR[1], 3, K.WINDOW)

    g.set(HOUSE_W[0] + 1, HOUSE_W[1] + HOUSE_W[3] - 1, 3, K.WINDOW)
    g.set(HOUSE_E[0] + 4, HOUSE_E[1] + HOUSE_E[3] - 1, 3, K.WINDOW)
    for b in (HOUSE_W, HOUSE_E):
        g.chimney_beside(*b[:2])

    # `LAMP` is head, post and foot, and the foot is the cell that blocks: a
    # lamp drawn from STREET_Y - 3 stands with its foot in the road.
    g.set(3, STREET_Y - 2, 3, K.SIGNPOST)          # the town's own sign
    g.column(7, STREET_Y - 4, 3, K.LAMP)
    g.column(16, STREET_Y - 4, 3, K.LAMP)
    g.scatter([(6, 13), (25, 13), (15, 14)], 3, K.BARREL)
    g.scatter([(24, 9), (5, 9), (13, 13)], 3, K.CRATE)
    g.scatter([(11, 13), (21, 13)], 3, K.TUB)
    g.scatter([(26, 15), (2, 17), (10, 19)], 3, K.BUSH)
    g.scatter([(3, 8), (26, 7), (24, 18)], 3, K.FLOWERS2)
    g.scatter([(2, 13), (26, 19)], 3, K.FLOWERS)
    g.scatter([(1, 6), (25, 4)], 3, K.LOGS)

    # Trees round three sides. The western side is left open: that is the road
    # in, and the gate is the gap.
    for x in range(0, w - 1, 2):
        g.blit(x, 0, 3, K.TREE)
        g.blit(x, h - 2, 3, K.TREE)
    for y in range(2, h - 2, 2):
        if not (STREET_Y - 2 <= y <= STREET_Y):
            g.blit(0, y, 3, K.TREE)
        g.blit(w - 2, y, 3, K.TREE)

    m = K.new_map(w, h, K.TS_OUTSIDE, name="Penultima", bgm="Town2")
    m["data"] = g.data
    m["events"] = [None] + penultima_events()
    S.widen_exit(m["events"], 1, [(GATE[0], GATE[1] - 1)])    # rows 10 and 11
    return m


def penultima_events():
    evs = []

    # 1: back out onto the tower road. Below characters, because an exit at
    # "same as characters" is one the player walks straight over.
    evs.append(S.exit_tile(1, "The Road North", *GATE, MAP_WORLD,
                           *PENULTIMA_STEP, direction=4))

    # 2: the town sign, which is the premise, and the cliche it is made of.
    sign = S.narrate([
        "A board, repainted often, in gold:",
        "",
        "        \\C[14]PENULTIMA\\C[0]",
        "  The Last Town Before The End"])
    sign += S.narrate([
        "Underneath, smaller, and newer:",
        "",
        "   LAST CHANCE FOR POTIONS"])
    sign += S.narrate([
        "Underneath that, smaller again, and newest:",
        "",
        "      (WE MEAN IT)"])
    sign += [S.trope()]
    # Read from the tile beside it, not by standing on it: a `SIGNPOST` tile
    # blocks its own cell, which is this game's idiom and the reason every
    # other sign in it is "same as characters" rather than "below".
    evs.append(R.event(2, "The Town Sign", 3, STREET_Y - 2, [R.page(
        sign, img=R.image(""), trigger=0, priority=1, through=True,
        direction_fix=True)]))

    # 3: the Sighting Bell. It is heard and never seen, which is cheaper than
    # drawing a bell tower and funnier than standing under one. Player-touch
    # and below characters, two squares inside the gate, so it goes off before
    # the player reaches the shop and explains the prices in advance.
    first = S.narrate([
        "Somewhere behind you a bell rings once,",
        "briskly, the way a shop bell rings."])
    first += S.narrate([
        "Along the street, unhurried, several",
        "shopkeepers turn over several small cards.",
        "Nobody looks at you while they do it."])
    first += S.narrate([
        "A man on a ladder hangs a fresh board over",
        "the old one. The old one said SUMMER RATES.",
        "The new one says SEASONAL RATES.",
        "It is the twelfth of November."])
    first += [S.trope(), R.self_switch("A", True)]
    again = S.narrate(["The bell does not ring twice for the same",
                       "customer. There would be no point."])
    evs.append(R.event(3, "The Sighting Bell", 5, STREET_Y, [
        R.page(first, img=R.image(""), trigger=1, priority=0, through=True),
        R.page(again, img=R.image(""), trigger=1, priority=0, through=True,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ]))

    # 4: Ye Final Shoppe.
    evs.append(S.door(4, "Ye Final Shoppe", *SHOPPE_DOOR, MAP_SHOPPE,
                      ROOM[6], ROOM[5]))

    # 5: the shop that used to be further on. Penultima means second to last,
    # and somebody once took that personally.
    rival = S.narrate([
        "A good shop front, boarded, with the paint",
        "still sound. The sign over the door reads:",
        "",
        "  \\C[14]ULTIMATE OUTFITTERS\\C[0] - The Actual Last Shop"])
    rival += S.narrate([
        "A hand points confidently up the road.",
        "Under it: 'TWO HUNDRED YARDS FURTHER ON.'"])
    rival += S.narrate([
        "Two hundred yards further on there is the",
        "road, and then the hills, and then the Tower.",
        "There has never been anything else."])
    rival += S.narrate([
        "A card in the window, in a different hand:",
        "'THANK YOU PENULTIMA FOR NINE WONDERFUL",
        "MONTHS.' It has been there some years."])
    evs.append(S.shut(R.event(5, "Ultimate Outfitters", *RIVAL_DOOR, [R.page(
        rival, img=R.image(""), trigger=0, priority=1, through=True,
        direction_fix=True)])))

    # 6: the notice a town like this puts up about itself, on the barrel at
    # (15, 14) it says it is pinned to - it was on the grass above it (P2).
    evs.append(S.pin_note(S.prop(6, "The Parish Notice", 15, 14, [
        "Pinned to a barrel, under glass:",
        "'PENULTIMA IS TWINNED WITH NOWHERE. THERE",
        "IS NOTHING TO BE TWINNED WITH. WE HAVE",
        "WRITTEN TO THE TOWER TWICE.'"], "", 0)))
    return evs


# ========================================================= Ye Final Shoppe ==
def shoppe_map():
    w, h, x1, y1, x2, y2, door_x = ROOM
    g = K.interior(w, h, x1, y1, x2, y2, door_x=door_x,
                   floor=K.IN_WOOD_FLOOR, floor_alt=K.IN_DARK_WOOD)

    # The window, from the inside: two of them, and between them the stand,
    # which is the only thing in the shop anybody remembers. `INC_SWORD_STAND`
    # is `Sword Rack A` - one sword, upright, on a stand, which is what the
    # line of dialogue says it is. The first draft of this room used
    # `IN_SWORD_RACK`, which is a sword and a shield mounted on a wall.
    g.column(7, 2, 3, K.IN_WINDOW)
    g.column(9, 2, 3, K.IN_WINDOW)
    # `IN_SWORD_RACK` is `Swords A` over `Shield`, mounted, two cells tall.
    # The plinth this was first drawn on - `Table B`, a red-draped round
    # table, with `Sword Rack A` laid on it - is a better description of the
    # bio and is **illegible at forty-eight pixels**: the swords lie flat, the
    # cloth is the only thing with any area, and the whole display reads as a
    # red drum. A screenshot is the only thing that finds that.
    g.column(8, 2, 2, K.IN_SWORD_RACK)        # on the wall's face rows

    K.wide(g, 3, 3, 2, K.IN_SUNDRIES_CABINET)     # whole: it was two halves
    g.column(5, 3, 2, K.IN_WINE_RACK)
    g.column(11, 3, 2, K.IN_SHELF_JARS)
    g.column(12, 3, 2, K.IN_BOOKSHELF)
    g.column(13, 3, 2, K.IN_SHELF_JARS)

    # The counter, across the west end, with the ledger open on it. Layer 1 is
    # floor art in the corpus and layer 3 the props, which is why the counter
    # and the book it carries are two cells deep rather than two tiles in one.
    g.blit(3, 7, 1, K.IN_TABLE)
    g.set(3, 7, 3, K.INC_OPEN_BOOK)
    g.set(4, 7, 3, K.INC_CASE)

    g.blit(11, 7, 1, K.IN_TABLE)        # `Table C` is draped in red too
    g.set(11, 7, 3, K.INC_BOTTLES)
    g.set(12, 7, 3, K.INC_CASE)
    g.set(12, 9, 2, K.IN_CRATE)
    g.set(13, 9, 2, K.IN_CRATE2)
    g.set(3, 10, 2, K.IN_CRATE2)
    g.set(13, 6, 2, K.IN_BARREL)   # `Pot B`, a ceramic pot

    m = K.new_map(ROOM[0], ROOM[1], K.TS_INSIDE, name="Ye Final Shoppe",
                  bgm="Town7", battleback=("Wood1", "Room1"))
    m["data"] = g.data
    m["events"] = [None] + shoppe_events()
    return m


def shoppe_events():
    evs = [S.exit_tile(1, "Shoppe Door", ROOM[6], ROOM[5] + 2,
                       MAP_PENULTIMA, *SHOPPE_OUT)]

    # 2: Gideon. Every price is twice the database price, which is what the
    # bell on the street was about, and which is done with custom prices so
    # that nothing outside this shop is affected by it.
    def seasonal(item_id, price):
        return (0, item_id, 1, price * 2)

    greet = S.say("Gideon", [
        "Welcome! What are you buying?"])
    shop = R.shop([
        seasonal(db.IT_POTION, 60), seasonal(db.IT_HI_POTION, 280),
        seasonal(db.IT_ETHER, 200), seasonal(db.IT_TONIC, 420),
        seasonal(db.IT_ANTIDOTE, 40), seasonal(db.IT_SMELLING_SALTS, 80),
        seasonal(db.IT_FEATHER, 500), seasonal(db.IT_ELIXIR, 1500),
    ])
    part = S.say("Gideon", [
        "Come again!"])

    # First time through he does the whole thing. Afterwards he is exactly the
    # shopkeeper he was, which is what a shop has to be.
    opening = S.say("Gideon", [
        "Welcome! What are you buying?"])
    opening += S.narrate([
        "You say you have only just come in."])
    opening += S.say("Gideon", [
        "Of course, of course. Take your time.",
        "Everything is priced.",
        "Everything has always been priced."])
    opening += S.narrate([
        "You ask about the prices, which seem high."])
    opening += S.say("Gideon", [
        "Seasonal.",
    ]) + S.say("Gideon", [
        "Thirty-one years in this trade",
        "and it has been seasonal every one of them.",
        "It is a very reliable season."])
    opening += [R.self_switch("A", True)]
    opening += shop + part

    # He stands at the window, not behind the counter, because Dorothy's
    # first line is that he is in the window again and the room has to agree
    # with her.
    evs.append(S.npc(2, "Gideon Markup", 7, 5,
                     R.if_then(R.condition_self_switch("A", False), opening,
                               list(greet) + list(shop) + list(part)),
                     "Gen_People1", 4, direction=8))

    # 3: the window, from the inside. The Sword is a prop with a price card
    # and is deliberately not stock - see the module docstring.
    sword = S.narrate([
        "A sword and a shield, mounted in the window,",
        "with a velvet rope in front of them. The sword",
        "has been polished this morning, and every",
        "morning."])
    sword += S.narrate([
        "The card beside it reads:",
        "",
        "  \\C[14]THE SWORD OF ULTIMATE ENDING\\C[0]",
        "        9,999,999 crowns"])
    sword += S.say("Gideon", [
        "Ah. The Sword of Ultimate Ending.",
        "Would sir like to hold it?"])
    sword += S.narrate(["You would."])
    sword += S.say("Gideon", [
        "Sir cannot afford to hold it."])
    sword += S.narrate([
        "He says it warmly. He has said it to everyone",
        "who has ever come through that door, and he",
        "is not going to stop now."])
    sword += [S.trope(), R.self_switch("A", True)]
    again = S.narrate([
        "The Sword of Ultimate Ending, in the window,",
        "behind its rope, and priced beyond the reach",
        "of anybody who has ever walked up this road."])
    # On the rack itself, the lower of its two cells on the wall - it was two
    # squares out on the bare floor, where nothing is drawn.
    evs.append(R.event(3, "The Window", 8, 3, [
        R.page(sword, img=R.image(""), trigger=0, priority=1, through=True,
               direction_fix=True),
        R.page(again, img=R.image(""), trigger=0, priority=1, through=True,
               direction_fix=True,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ]))

    # 4: Dorothy, and the ledger, and the eleven coppers. Register A, by the
    # innocent superlative - NORTH.md 1.3 item 1. Nothing improper is said by
    # anybody, the marriage is plainly a good one, and the game never lets on.
    first = S.say("Dorothy", [
        "He is in the window again.",
        "He is always in the window."])
    first += S.narrate([
        "You say that the window is very well kept."])
    first += S.say("Dorothy", [
        "He brings me my tea every morning,",
        "and then he does the window.",
        "Thirty-one years, and never once",
        "has he had to be asked."])
    first += S.narrate([
        "She writes a line in the ledger and rules",
        "it off, and does not look up."])
    first += S.say("Dorothy", [
        "Mind you, he has never sold the sword."])
    first += [S.blush(), R.self_switch("A", True)]
    later = S.say("Dorothy", [
        "A boot came in this morning.",
        "One crown. It will go out at forty.",
        "That is the trade, and I write down",
        "both of them."])
    later += S.narrate([
        "You ask whether he has ever given a discount."])
    later += S.say("Dorothy", [
        "Once.",
    ]) + S.say("Dorothy", [
        "Eleven coppers, off a lamp, to a",
        "girl who would not stop haggling."])
    later += S.narrate([
        "She taps the front of the ledger, where an",
        "old entry has been ruled round twice."])
    later += S.say("Dorothy", [
        "I have still got them."])
    evs.append(S.npc(4, "Dorothy Markup", 3, 6, first, "Gen_People1", 5,
                     direction=2, pages=[
                         R.page(later,
                                img=R.image("Gen_People1", 5, direction=2),
                                trigger=0, priority=1,
                                conditions={"selfSwitchValid": True,
                                            "selfSwitchCh": "A"})]))
    return evs


# ================================================================ the doors ==
def world_doors(base_id, cells):
    """The real doors into Penultima, on the world map.

    `cells` is every square `worldmap.json` put a placeholder door on for this
    site, handed in by `journey.world_map` - so the geometry stays the world
    map's and only the destination is ours. Both cells of the stamp get a
    door, because a player walking up the road can arrive at either.

    Player-touch and below characters, which is the world map's own idiom for
    a place you walk into, and what `finish.add_site` wrote the placeholders
    as."""
    evs = []
    for i, (x, y) in enumerate(sorted(cells)):
        arrive = S.narrate([
            "Penultima. One street, and every window on",
            "it has a sword in it."])
        arrive += R.choice_block(
            ["Go in", "Press on"],
            [[R.play_se("Move1"),
              R.transfer(MAP_PENULTIMA, GATE[0] + 2, GATE[1], 6, 0)],
             S.narrate(["You press on. It is the last town before",
                        "the end. It will keep."])])
        evs.append(R.event(base_id + i, "Penultima", x, y, [R.page(
            arrive, img=R.image(""), trigger=1, priority=0, through=True)]))
    return evs


def build():
    R.save_map(MAP_PENULTIMA, penultima_map())
    R.save_map(MAP_SHOPPE, shoppe_map())
