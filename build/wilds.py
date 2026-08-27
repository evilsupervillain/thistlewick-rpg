"""The optional places off the road, and the half of the world map that leads
to them: Maps 19-20, plus the south of Map 8.

    19  The Bottomless Pit                 four feet deep. Admission 2cr.
    20  The Barrow of the Forty-Fourth     a hero in a mound who wanted a bench

`journey.py` still owns Map 8 - it calls the four hooks at the top of this file
while it is drawing, so the world map is built in one place and the southern
content is written in one place. See `EXPANSION.md`.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import db
import mapkit as K
import rmmzdata as R
import story as S
from places import (MAP_WORLD, MAP_SOPPING, MAP_LIGHTHOUSE, MAP_PIT,
                    MAP_BARROW, SOPPING_GATE, WORLD_SOPPING, WORLD_SOPPING_STEP,
                    WORLD_LIGHTHOUSE, WORLD_PIT, WORLD_BARROW, WORLD_STONES,
                    WORLD_HERMIT, WORLD_CRAB, WORLD_CAMP,
                    WORLD_VILLAGE_STEP)

REG_COAST = 3               # the shingle: crabs, gulls, and something in it

PIT_W, PIT_H = 26, 24
PIT_IN = (12, 20)

BARROW_W, BARROW_H = 30, 26
BARROW_IN = (14, 22)


# ================================================ the south of the world map ==
def south_ground(g):
    """Layer 0. Called after the coastline blobs and before `autotile(0)`.

    The continent grows a south-east shoulder for Nether Sopping to stand on,
    a headland for the lighthouse, and a shingle beach along the whole southern
    shore, which is its own encounter region."""
    g.blob(34, 46, 9, 4, 0, K.W_GRASS)            # the shoulder
    g.blob(41, 44, 2, 2, 0, K.W_GRASS)            # the lighthouse headland

    # The beach: the lowest two land rows of every column south of the
    # midpoint. Doing it by scan rather than by hand means the shingle follows
    # the coast wherever the coast turns out to be.
    sea = R.autotile_kind(K.W_SEA)
    for x in range(g.width):
        land = [y for y in range(34, g.height)
                if not (R.is_autotile(g.get(x, y, 0)) and
                        R.autotile_kind(g.get(x, y, 0)) == sea)]
        if not land:
            continue
        edge = max(land)
        for y in range(max(edge - 1, 34), edge + 1):
            g.set(x, y, 0, K.W_SAND)


def south_layer1(g):
    """Layer 1: the coast road east to Nether Sopping, and the two tracks that
    take you off it. Called before `autotile(1)`."""
    track = []
    track += [(24, 45), (24, 46)]                       # out of Thistlewick
    track += [(x, 46) for x in range(24, 37)]           # the coast road east
    track += [(WORLD_SOPPING[0], 45)]
    track += [(x, 45) for x in range(37, 42)]           # on to the headland
    track += [(41, 45)]
    track += [(x, 34) for x in range(8, 18)]            # west, to the Pit
    track += [(17, y) for y in range(34, 36)]
    track += [(8, y) for y in range(34, 37)]
    track += [(x, 18) for x in range(17, 34)]           # east, to the Barrow
    track += [(33, y) for y in range(18, 23)]
    for x, y in track:
        if 0 <= x < g.width and 0 <= y < g.height:
            g.set(x, y, 1, K.W_ROAD)

    g.blob(30, 42, 3, 2, 1, K.W_FOREST)
    g.blob(38, 42, 2, 2, 1, K.W_CONIFER)
    g.blob(10, 33, 2, 2, 1, K.W_FOREST)


def south_layer3(g):
    """Layer 3: the four places you can walk into down here, and the things
    that are only there to be looked at."""
    g.blit(WORLD_SOPPING[0] - 1, WORLD_SOPPING[1] - 1, 3, K.WB_TOWN)
    g.blit(WORLD_LIGHTHOUSE[0], WORLD_LIGHTHOUSE[1] - 1, 3, K.WB_TOWER_WHITE)
    g.set(WORLD_PIT[0], WORLD_PIT[1], 3, K.WB_CAVE)
    g.set(WORLD_BARROW[0], WORLD_BARROW[1], 3, K.WB_CAVE_DARK)

    for x, y in [(10, 17), (12, 17), (10, 19), (12, 19)]:
        g.set(x, y, 3, K.WB_ROCK)                 # the standing stones
    g.set(WORLD_HERMIT[0], WORLD_HERMIT[1] - 1, 3, K.WB_HUT)
    g.set(WORLD_CRAB[0] - 1, WORLD_CRAB[1], 3, K.WB_ROCK)
    g.set(WORLD_CAMP[0] - 1, WORLD_CAMP[1], 3, K.WB_HUT)
    g.set(28, 45, 3, K.WB_SIGN)   # beside the road, not on it
    for x, y in [(31, 44), (39, 43), (27, 41), (35, 47), (7, 33), (30, 19),
                 (37, 22), (14, 16)]:
        g.set(x, y, 3, K.WB_TREE)


def south_regions(g):
    """The shingle gets its own encounter list, so the walk to Nether Sopping
    is not the same three fights as the walk to the gate.

    Thistlewick sits close enough to the south coast that the beach scan runs
    right past its front door, and the tile you step onto leaving the village
    is shingle. It stays in the gentle half all the same: a level-five party
    two steps out of the gate should be meeting turnips, not crabs. The
    shingle only becomes crab country once the coast road is clear of the
    village, which is what the `x` test is - beach you can see, beach that
    bites."""
    sand = R.autotile_kind(K.W_SAND)
    first_coast = WORLD_VILLAGE_STEP[0] + 2
    for y in range(g.height):
        for x in range(first_coast, g.width):
            t = g.get(x, y, 0)
            if R.is_autotile(t) and R.autotile_kind(t) == sand:
                if g.get(x, y, 5):
                    g.set(x, y, 5, REG_COAST)


# ------------------------------------------------------ the events out there --
def south_events(next_id):
    """The world-map half of the south. `next_id` is the first free event id on
    Map 8, so the existing seven keep their numbers."""
    evs = []

    def ev(name, x, y, cmds, **kw):
        evs.append(R.event(next_id + len(evs), name, x, y, [R.page(
            cmds, img=R.image(""), trigger=1, priority=0, through=True,
            **kw)]))

    # -- Nether Sopping --------------------------------------------------------
    town = S.narrate([
        "Nether Sopping. Roofs, rigging, and a great",
        "deal of weather arriving off the sea."])
    town += R.choice_block(
        ["Go in", "Carry on"],
        [[R.play_se("Move1"), R.control_switch(db.SW_SOUTH, True),
          R.transfer(MAP_SOPPING, SOPPING_GATE[0], SOPPING_GATE[1] + 1, 2, 0)],
         []])
    ev("Nether Sopping", *WORLD_SOPPING, town)

    # -- the lighthouse --------------------------------------------------------
    light = S.narrate([
        "A lighthouse on a headland, at the end of a",
        "road that goes nowhere else.",
        "It is not lit."])
    light += R.choice_block(
        ["Go in", "Leave it"],
        [[R.play_se("Move1"),
          R.transfer(MAP_LIGHTHOUSE, 6, 19, 8, 0)], []])
    lit = S.narrate([
        "The Lighthouse of Saint Bother, burning.",
        "You can see it from the crossroads. Somebody",
        "checked, once, at midnight."])
    lit += R.choice_block(
        ["Go in", "Leave it"],
        [[R.play_se("Move1"),
          R.transfer(MAP_LIGHTHOUSE, 6, 19, 8, 0)], []])
    evs.append(R.event(next_id + len(evs), "The Lighthouse",
                       *WORLD_LIGHTHOUSE, [
        R.page(light, img=R.image(""), trigger=1, priority=0, through=True),
        R.page(lit, img=R.image(""), trigger=1, priority=0, through=True,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_LAMP_LIT})]))

    evs.append(pit_turnstile(next_id + len(evs)))
    evs.append(barrow_door(next_id + len(evs)))
    evs.append(barrow_top(next_id + len(evs)))

    # -- the standing stones ---------------------------------------------------
    stones = S.narrate([
        "Four standing stones, and a plaque."])
    stones += S.narrate([
        "\\C[6]THE STANDING STONES OF UNCERTAIN PURPOSE\\C[0]",
        "Six theories are current:",
        "1. A calendar. 2. A temple. 3. A boundary.",
        "4. A tomb. 5. An early form of the Prophecy."])
    stones += S.narrate([
        "6. That they were put up eleven years ago by",
        "   Wat Pardle of this parish, to mark where",
        "   his gate was, and that Wat Pardle is",
        "   standing over there and will say so."])
    stones += S.narrate([
        "Theory six is footnoted: 'Not favoured. The",
        "other five are more interesting and Mr Pardle",
        "has been asked to stop coming to the site.'"])
    stones += [S.trope()]
    ev("The Standing Stones", *WORLD_STONES, stones)

    # -- the hermit ------------------------------------------------------------
    hermit = S.narrate([
        "A hut, a rock, and a man looking at the",
        "middle distance with great authority."])
    hermit += S.say("Hermit", [
        "You seek wisdom."])
    hermit += S.narrate(["You had, in fact, been walking past."])
    hermit += S.say("Hermit", [
        "Then hear it, traveller.",
        "Bread. Candles. A wedge of the hard",
        "cheese, not the soft. Nails, two inch.",
        "Something for a cough."])
    hermit += S.narrate(["You point out that this is a shopping list."])
    hermit += S.say("Hermit", [
        "It is a shopping list, yes.",
        "I have been up here nineteen years",
        "and no one has ever once come up",
        "and asked me if I needed anything."])
    hermit += S.narrate([
        "You go and get his shopping. It takes an",
        "afternoon. He is so pleased that he gives you",
        "his second-best thing."])
    hermit += [R.gain_item(db.IT_ELIXIR, 1), R.gain_gold(200),
               R.play_me("Item")]
    hermit += S.narrate(["Got \\I[179]\\C[3]Elixir\\C[0] and 200\\G.",
                         "He would like it known that he did not need",
                         "the company. He needed the cheese."])
    hermit += [S.trope(), R.self_switch("A", True)]
    hermit_again = S.say("Hermit", [
        "The middle distance is very fine today.",
        "Also I am nearly out of candles again,",
        "but I shan't mention it."])
    evs.append(R.event(next_id + len(evs), "The Hermit", *WORLD_HERMIT, [
        R.page(hermit, img=R.image(""), trigger=1, priority=0, through=True),
        R.page(hermit_again, img=R.image(""), trigger=1, priority=0,
               through=True,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"})]))

    evs.append(crab_bounty(next_id + len(evs)))
    evs.append(crooke_bounty(next_id + len(evs)))

    # -- the southern signpost -------------------------------------------------
    evs.append(S.sign(next_id + len(evs), "Coast Road Signpost", 28, 45, [
        "\\C[6]EAST:\\C[0] Nether Sopping. 4 leagues.",
        "\\C[6]WEST:\\C[0] Thistlewick.",
        "Somebody from one end of this road has",
        "scratched out the other end's name.",
        "Somebody from the other end has scratched",
        "out theirs. Both are still legible. It has",
        "been like this for a hundred years."]))
    return evs


def pit_turnstile(event_id):
    """The Bottomless Pit is a paying attraction, and Fenwick Splint is at the
    gate of it, and he will take your two crowns."""
    img = R.image("")

    def gate(lines):
        cmds = S.say("Splint", lines)
        cmds += R.choice_block(
            ["Pay 2cr and go in", "Not today"],
            [R.if_then(
                R.condition_script("$gameParty.gold() >= 2"),
                [R.lose_gold(2), R.play_se("Coin"), R.play_se("Move1"),
                 R.transfer(MAP_PIT, PIT_IN[0], PIT_IN[1], 8, 0)],
                S.say("Splint", ["Two crowns. It's two crowns.",
                                 "I'd let you in for nothing but then",
                                 "it's not an attraction, is it."])), []])
        return cmds

    intro = S.narrate([
        "A hole in the hillside, a hut, a rope, and a",
        "turnstile.",
        "A board reads: \\C[6]THE BOTTOMLESS PIT\\C[0]. Admission",
        "2\\G. Children 1\\G. No refunds re: depth."])
    intro += S.say("Splint", [
        "Fenwick Splint, custodian.",
        "Two crowns and you may look into the",
        "Bottomless Pit, which is a wonder of the",
        "district and, I'll be straight with you, four"])
    intro += S.say("Splint", [
        "feet deep."])
    intro += S.narrate(["You ask why it is called the Bottomless Pit."])
    intro += S.say("Splint", [
        "Because 'the Pit' is not a wonder of",
        "the district."])
    intro += S.narrate(["He lowers his voice."])
    intro += S.say("Splint", [
        "Something's moved in, mind.",
        "Down the far end. It's been eating the",
        "lost property. Two hundred years of",
        "lost property, and it has EATEN it."])
    intro += S.say("Splint", [
        "Deal with that and there's coin in it.",
        "Also you may keep whatever's left,",
        "which by rights belongs to the parish,",
        "and the parish is me, and I say keep it."])
    intro += [R.control_switch(db.SW_PIT_ASKED, True), S.trope()]
    intro += gate(["So. Two crowns, and mind the step.",
                   "There isn't one. That's the joke."])

    entry = gate(["Two crowns. In you go.",
                  "Mind the step. There isn't one.",
                  "That's the joke, and I do it every time."])

    payout = S.say("Splint", [
        "You've done it. You actually did it."])
    payout += S.narrate(["He looks into the pit for a while."])
    payout += S.say("Splint", [
        "Forty years I've had a badger.",
        "I told the Guild. They said a badger",
        "wasn't a monster. I said come and see",
        "the badger. They never came and saw the badger."])
    payout += [R.gain_gold(700), R.gain_item(db.IT_HI_POTION, 3),
               R.play_me("Item")]
    payout += S.narrate(["Got 700\\G and \\I[176]\\C[3]Hi-Potion x3\\C[0]."])
    payout += S.say("Splint", [
        "Admission's free for you now. Forever.",
        "It's four feet deep and you're welcome",
        "in it whenever you like."])
    payout += [R.control_switch(db.SW_PIT_PAID, True), S.trope()]
    payout += R.choice_block(
        ["Go in", "Move on"],
        [[R.play_se("Move1"),
          R.transfer(MAP_PIT, PIT_IN[0], PIT_IN[1], 8, 0)], []])

    free = S.say("Splint", [
        "In you go. No charge. Never again."])
    free += R.choice_block(
        ["Go in", "Move on"],
        [[R.play_se("Move1"),
          R.transfer(MAP_PIT, PIT_IN[0], PIT_IN[1], 8, 0)], []])

    return R.event(event_id, "The Bottomless Pit", *WORLD_PIT, [
        R.page(intro, img=img, trigger=1, priority=0, through=True),
        R.page(entry, img=img, trigger=1, priority=0, through=True,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_PIT_ASKED}),
        R.page(payout, img=img, trigger=1, priority=0, through=True,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_PIT_CLEARED}),
        R.page(free, img=img, trigger=1, priority=0, through=True,
               conditions={"switch1Valid": True, "switch1Id": db.SW_PIT_PAID}),
    ])


def barrow_door(event_id):
    """A Scheduled Monument, and therefore members only, which is the pettiest
    locked door in the game and the one the player will remember."""
    img = R.image("")

    shut = S.narrate([
        "A long grass mound with a stone mouth in the",
        "side of it, and a sign."])
    shut += S.narrate([
        "\\C[6]THE BARROW OF THE FORTY-FOURTH\\C[0]",
        "A Scheduled Monument of the district.",
        "Entry restricted to registered adventurers.",
        "By order: the Adventurers' Guild (Provisional)"])
    shut += S.narrate([
        "Underneath, in chalk, in a much older hand:",
        "'THERE IS A CURSE ON IT AS WELL'."])
    shut += S.narrate([
        "The stone is not locked. There is simply a",
        "sign, and you are simply not registered.",
        "You find, to your considerable annoyance,",
        "that this is enough."])
    shut += [S.trope()]

    open_it = S.narrate([
        "The Barrow of the Forty-Fourth.",
        "You show the sign your Guild Card. The sign",
        "does not react. You go in anyway, which is",
        "the whole of what the card was for."])
    open_it += R.choice_block(
        ["Go in", "Not yet"],
        [[R.play_se("Move1"), R.control_switch(db.SW_BARROW_OPEN, True),
          R.transfer(MAP_BARROW, BARROW_IN[0], BARROW_IN[1], 8, 0)], []])

    return R.event(event_id, "The Barrow of the Forty-Fourth", *WORLD_BARROW, [
        R.page(shut, img=img, trigger=1, priority=0, through=True),
        R.page(open_it, img=img, trigger=1, priority=0, through=True,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_GUILD_MEMBER}),
    ])


def barrow_top(event_id):
    """Where the bench goes. The top of the mound, which is the only place in
    the district you can see both the sea and the north road at once."""
    img = R.image("")
    x, y = WORLD_BARROW[0] + 1, WORLD_BARROW[1] + 1

    plain = S.narrate([
        "The top of the mound. Long grass, and a view.",
        "You can see the sea from here, and the north",
        "road, and the tower at the end of it.",
        "There is nowhere at all to sit."])

    wanted = S.narrate([
        "The top of the mound. The sea one way, the",
        "tower the other.",
        "This is the spot. He was quite clear about",
        "the spot."])

    build = S.narrate([
        "The top of the mound, and a bench in eleven",
        "pieces under your arm."])
    build += R.choice_block(
        ["Put the bench together", "Not yet"],
        [[R.gain_item(db.IT_BENCH, -1), R.play_se("Hammer"), R.wait(40),
          R.play_se("Hammer"), R.wait(40), R.play_se("Hammer")] +
         S.narrate([
             "The diagram is wrong. You work it out.",
             "It takes an hour and a half and one piece",
             "is left over, which is traditional."]) +
         [R.play_me("Fanfare1"), R.wait(30)] +
         S.narrate([
             "A bench, on the top of the Barrow of the",
             "Forty-Fourth, facing the sea.",
             "Anyone may sit on it. That was the point;",
             "he was very clear that that was the point."]) +
         S.narrate([
             "Somebody should tell Ysolde Marrow.",
             "She is in the Slain Wyvern, at the table",
             "by the bar, with a kit she does not need",
             "open in front of her out of habit."]) +
         [R.control_switch(db.SW_BENCH_DONE, True), S.trope()],
         []])

    done = S.narrate([
        "The bench on the top of the mound.",
        "Somebody has already been sitting on it: the",
        "grass is flat in front of it, and there is a",
        "cup, and the cup is not yours."])

    return R.event(event_id, "The Top Of The Barrow", x, y, [
        R.page(plain, img=img, trigger=1, priority=0, through=True),
        R.page(wanted, img=img, trigger=1, priority=0, through=True,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_BENCH_ASKED}),
        R.page(build, img=img, trigger=1, priority=0, through=True,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_BENCH_ASKED,
                           "itemValid": True, "itemId": db.IT_BENCH}),
        R.page(done, img=img, trigger=1, priority=0, through=True,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_BENCH_DONE}),
    ])


def crab_bounty(event_id):
    img = R.image("")
    fight = S.narrate([
        "The west beach.",
        "Something the size of a garden shed is on it,",
        "sideways, and it has noticed you."])
    fight += S.narrate([
        "The bounty card said 'unusual'.",
        "Everyone in Nether Sopping was very careful",
        "to say 'unusual'."])
    fight += [R.play_se("Monster3"), R.wait(30),
              R.battle(db.TR_BIG_CRAB, can_escape=False, can_lose=False)]
    fight += [R.control_switch(db.SW_BOUNTY_CRAB, True)]
    fight += S.narrate([
        "The Crab Of Unusual Size stops holding the",
        "beach.",
        "Four smaller crabs immediately begin, between",
        "them, to hold the beach."])
    fight += [R.gain_gold(400), R.gain_item(db.IT_ELIXIR, 1),
              R.play_me("Victory2")]
    fight += S.narrate(["Found 400\\G and \\I[179]\\C[3]Elixir\\C[0] in the",
                        "shingle underneath it. It had been sitting on",
                        "eleven years of other people's bad afternoons."])
    fight += [S.trope()]
    return R.event(event_id, "The Crab Of Unusual Size", *WORLD_CRAB, [
        R.page(fight, img=img, trigger=1, priority=0, through=True),
        R.page(S.narrate(["The beach. Four crabs, holding it, badly."]),
               img=img, trigger=1, priority=0, through=True,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_BOUNTY_CRAB}),
    ])


def crooke_bounty(event_id):
    img = R.image("")
    camp = S.narrate([
        "A camp in the western hills: eight tents, a",
        "cook fire, and a board with a timetable on it."])
    camp += S.narrate([
        "\\C[6]WEEK 4: INTIMIDATION (PRACTICAL)\\C[0]",
        "\\C[6]WEEK 5: DEMANDS - STRUCTURE AND DELIVERY\\C[0]",
        "\\C[6]WEEK 6: ASSESSMENT AND CERTIFICATE\\C[0]"])
    camp += S.say("Crooke", [
        "You'll be the bounty, then.",
        "Meredith Crooke. Principal."])
    camp += S.narrate(["Behind her, four trainee bandits are standing",
                       "in a semicircle taking notes."])
    camp += S.say("Crooke", [
        "Don't hold back on my account.",
        "They're in week four. They need to see",
        "one of these go badly for the tutor.",
        "It's the only lesson that ever sticks."])
    camp += [R.play_me("Shock1"), R.wait(30),
             R.battle(db.TR_CROOKE, can_escape=False, can_lose=False)]
    camp += [R.control_switch(db.SW_BOUNTY_CROOKE, True)]
    camp += S.say("Crooke", [
        "Good! Did you all see the footwork?"])
    camp += S.narrate([
        "The cohort has, to a bandit, written down",
        "the footwork."])
    camp += S.say("Crooke", [
        "Take the takings. Go and claim your",
        "bounty. And tell Pell the pass rate",
        "this year is ninety per cent, which is",
        "more than his Guild can say for anything."])
    camp += [R.gain_gold(600), R.gain_item(db.IT_TONIC, 2),
             R.play_me("Victory2")]
    camp += S.narrate(["Got 600\\G and \\I[180]\\C[3]Field Tonic x2\\C[0]."])
    camp += [S.trope()]
    return R.event(event_id, "Meredith Crooke's Camp", *WORLD_CAMP, [
        R.page(camp, img=img, trigger=1, priority=0, through=True),
        R.page(S.say("Crooke", [
            "Week five. Come back Thursday and",
            "let them see it done to you properly."]),
            img=img, trigger=1, priority=0, through=True,
            conditions={"switch1Valid": True,
                        "switch1Id": db.SW_BOUNTY_CROOKE}),
    ])


# ========================================================= the Bottomless Pit ==
def pit_map():
    """Shallow, wide, and full of two hundred years of things people meant to
    come back for."""
    g = K.Canvas(PIT_W, PIT_H)
    g.fill(0, 0, PIT_W - 1, PIT_H - 1, 0, K.DG_WALL_TOP)
    for x1, y1, x2, y2 in [(9, 17, 16, 21),      # the ledge you come in on
                           (12, 11, 13, 16),     # the drop, such as it is
                           (4, 4, 21, 10)]:      # the bottom
        g.fill(x1, y1, x2, y2, 0, K.DG_FLOOR)
    g.fill(6, 5, 19, 9, 0, K.DG_FLOOR2)
    g.dungeon_walls(K.DG_WALL_TOP, K.DG_WALL_FACE)
    g.autotile(0)

    g.scatter([(5, 9), (20, 9), (7, 4), (18, 4)], 3, K.DGB_RUBBLE)
    g.scatter([(6, 10), (19, 10), (10, 4)], 3, K.DGB_ROCK)
    g.scatter([(9, 20), (16, 20)], 3, K.DGB_BARRICADE)
    g.column(4, 5, 3, K.DGB_PILLAR)
    g.column(21, 5, 3, K.DGB_PILLAR)
    K.paint_regions(g, K.TS_DUNGEON, 1)

    m = K.new_map(PIT_W, PIT_H, K.TS_DUNGEON, name="The Bottomless Pit",
                  bgm="Dungeon2", encounter_step=34,
                  battleback=("Stone1", "Ruins1"),
                  encounters=[(db.TR_PIT_MIX, 5, [1]),
                              (db.TR_GULLS, 2, [1])])
    m["data"] = g.data
    m["events"] = [None] + pit_events()
    return m


def pit_events():
    evs = []

    out = S.narrate(["Back up the rope?"])
    out += R.choice_block(
        ["Yes", "No"],
        [[R.play_se("Move1"),
          R.transfer(MAP_WORLD, WORLD_PIT[0], WORLD_PIT[1] + 1, 2, 0)], []])
    evs.append(R.event(1, "Up The Rope", PIT_IN[0], PIT_IN[1] + 1, [R.page(
        out, img=R.image(""), trigger=1, priority=0, through=True)]))

    evs.append(S.sign(2, "The Board At The Bottom", 15, 19, [
        "A painted board, at the bottom of the pit,",
        "facing up at the visitors:",
        "\\C[6]BOTTOMLESS (APPROX.)\\C[0]",
        "Somebody has added: 'YOU ARE STANDING ON IT'."]))

    # The Thing At The Bottom.
    badger = S.narrate([
        "Something enormous is asleep on a mattress of",
        "two hundred years of lost property."])
    badger += S.narrate([
        "It is a badger.",
        "It is a badger the size of a hay cart, and it",
        "has eaten every single thing that Nether",
        "Sopping has ever failed to come back for."])
    badger += S.narrate(["It opens one eye. It has a strong opinion."])
    badger += [R.play_se("Growl"), R.shake_screen(5, 5, 45, True),
               R.battle(db.TR_BADGER, can_escape=False, can_lose=False)]
    badger += [R.control_switch(db.SW_PIT_CLEARED, True)]
    badger += S.narrate([
        "The Thing At The Bottom leaves, at speed, up",
        "a slope nobody knew was there.",
        "It takes one boot with it. It has earned the",
        "boot."])
    badger += [R.gain_gold(500), R.play_me("Victory2")]
    badger += S.narrate(["Found 500\\G in the bedding.",
                         "Splint should be told. Splint has been",
                         "waiting forty years to be told."])
    badger += [S.trope(), R.self_switch("A", True)]
    evs.append(R.event(3, "The Thing At The Bottom", 12, 7, [
        R.page(badger, img=R.image("Nature", 0, direction=2), trigger=1,
               priority=1, step_anime=True),
        R.page([], img=R.image(""), trigger=0, priority=0, through=True,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ]))

    evs.append(S.chest(4, "Lost Property (West)", 6, 6,
                       [R.gain_item(db.IT_LAMP_OIL, 1),
                        R.gain_item(db.IT_ETHER, 3), R.gain_gold(150)],
                       ["Found \\I[275]\\C[3]Lamp Oil\\C[0], \\I[178]\\C[3]Ether x3\\C[0]",
                        "and 150\\G.",
                        "Somebody meant to come back for the oil.",
                        "Somebody meant to come back for all of it."]))

    evs.append(S.chest(5, "Lost Property (East)", 19, 6,
                       [R.gain_armor(db.AR_RING_SPEED, 1),
                        R.gain_item(db.IT_ELIXIR, 1)],
                       ["Found \\I[147]\\C[3]Hasty Ring\\C[0] and",
                        "\\I[179]\\C[3]Elixir\\C[0] in a hamper marked",
                        "'PROPERTY OF THE 39TH - DO NOT TOUCH'."]))

    evs.append(S.sign(6, "The Socks", 10, 9, [
        "A drift of odd socks four feet deep, which is",
        "to say: as deep as the pit.",
        "Nether Sopping has been losing one sock at a",
        "time for two hundred years and they have all",
        "come here, and none of them match."]))

    evs.append(S.prop(7, "A Hamper", 17, 9, [
        "A picnic hamper with a note in it:",
        "'BACK IN AN HOUR - H.V.'",
        "The handwriting is the same as the plaque",
        "under the wyvern in the Slain Wyvern."],
        "", 0, extra=[S.trope()]))

    # NORTH.md 3.4, three of three, and the one that needs a cave to be in.
    evs.append(S.specimen(8, "Something In The Crack", 21, 5, [
        "A crack in the wall, running back further",
        "than the lamp reaches.",
        "There is something asleep in it. It is not",
        "small, and it has not noticed you.",
    ], S.say("Wren", ["That one is gravid."]) +
       S.narrate(["You ask whether that is bad."]) +
       S.say("Wren", [
           "It is the single most normal thing",
           "in this cave.",
       ]), [
        "Still asleep. Still enormous.",
        "Still, apparently, entirely normal.",
    ]))
    return evs


# ============================================ the Barrow of the Forty-Fourth ==
def barrow_map():
    """A mound built for a man who was ignored for forty years and then given
    grave goods, a curse, and a hound, because that is what you do with a hero
    once he is safely finished."""
    g = K.Canvas(BARROW_W, BARROW_H)
    g.fill(0, 0, BARROW_W - 1, BARROW_H - 1, 0, K.DG_WALL_TOP)
    rooms = [(12, 20, 17, 23),        # the porch
             (12, 13, 17, 18),        # the antechamber
             (3, 13, 9, 18),          # west chamber
             (20, 13, 26, 18),        # east chamber
             (9, 4, 20, 11)]          # the burial chamber
    for x1, y1, x2, y2 in rooms:
        g.fill(x1, y1, x2, y2, 0, K.DG_FLOOR)
    for x1, y1, x2, y2 in [(14, 19, 14, 19), (10, 15, 11, 15),
                           (18, 15, 19, 15), (14, 12, 14, 12)]:
        g.fill(x1, y1, x2, y2, 0, K.DG_FLOOR)
    g.fill(11, 5, 18, 10, 0, K.DG_FLOOR2)
    g.dungeon_walls(K.DG_WALL_TOP, K.DG_WALL_FACE)
    g.autotile(0)

    for x, y in [(10, 8), (19, 8)]:
        g.column(x, y - 1, 3, K.DGB_PILLAR_WHITE)
    g.column(11, 4, 3, K.DGB_STATUE_ANGEL)
    g.column(18, 4, 3, K.DGB_STATUE_ANGEL)
    g.column(14, 4, 2, K.DGB_MONUMENT)
    g.scatter([(4, 17), (9, 14), (21, 14), (26, 17)], 3, K.DGB_BONES)
    g.scatter([(3, 14), (26, 14)], 3, K.DGB_SKULLS)
    g.scatter([(13, 22), (16, 22)], 3, K.DGB_RUBBLE)
    g.scatter([(12, 17), (17, 17)], 3, K.DGB_ROCK)
    K.paint_regions(g, K.TS_DUNGEON, 1)

    m = K.new_map(BARROW_W, BARROW_H, K.TS_DUNGEON,
                  name="The Barrow of the Forty-Fourth", bgm="Dungeon6",
                  encounter_step=28, battleback=("Stone1", "Ruins1"),
                  encounters=[(db.TR_BARROW_MIX, 4, [1]),
                              (db.TR_WRAITHS, 4, [1]),
                              (db.TR_GRAVE_GOODS, 3, [1])])
    m["data"] = g.data
    m["events"] = [None] + barrow_events()
    return m


def barrow_events():
    evs = []

    out = S.narrate(["Back out into the daylight?"])
    out += R.choice_block(
        ["Yes", "No"],
        [[R.play_se("Move1"),
          R.transfer(MAP_WORLD, WORLD_BARROW[0], WORLD_BARROW[1] + 1, 2, 0)],
         []])
    evs.append(R.event(1, "Barrow Mouth", BARROW_IN[0], BARROW_IN[1] + 1,
                       [R.page(out, img=R.image(""), trigger=1, priority=0,
                               through=True)]))

    evs.append(S.sign(2, "The Dedication", 16, 22, [
        "Cut into the stone of the porch, deeply, and",
        "recently, and at some expense:",
        "\\C[6]AMBROSE FITCH. CHOSEN ONE #44.\\C[0]",
        "\\C[6]THISTLEWICK REMEMBERS.\\C[0]",
        "Underneath, small, in chalk, in a woman's",
        "hand: 'thistlewick did not write once'."]))

    evs.append(S.chest(3, "West Chamber", 5, 15,
                       [R.gain_item(db.IT_ELIXIR, 1), R.gain_gold(900)],
                       ["Found \\I[179]\\C[3]Elixir\\C[0] and 900\\G,",
                        "laid out on a cloth. Grave goods. Nobody has",
                        "touched them because nobody has been in."]))

    evs.append(S.chest(4, "East Chamber", 23, 15,
                       [R.gain_armor(db.AR_CIRCLET, 1),
                        R.gain_item(db.IT_FEATHER, 2)],
                       ["Found \\I[148]\\C[3]Plain Circlet\\C[0] and",
                        "\\I[185]\\C[3]Slightly Singed Feather x2\\C[0]."]))

    evs.append(S.sign(5, "The Hound's Place", 21, 14, [
        "A stone alcove with a dish in it, and a collar,",
        "and a name: BUDGE.",
        "Something is still using the alcove.",
        "You have already met it, in the dark, twice."]))

    evs.append(forty_fourth(6, 14, 7))
    return evs


def forty_fourth(event_id, x, y):
    """The optional boss, and the only one in the game who stops when asked."""
    img = R.image("People3", 4, direction=2)

    fight = S.narrate([
        "The burial chamber.",
        "A man is standing in the middle of it, in",
        "armour, with a sword, in the exact centre of",
        "a circle somebody drew for him."])
    fight += S.say("Ambrose", [
        "You'll be a Chosen One."])
    fight += S.narrate(["You say that you are the forty-eighth."])
    fight += S.say("Ambrose", [
        "Forty-eight. Long time.",
        "Ambrose Fitch. Forty-four.",
        "I'd shake your hand but there's a way",
        "this goes and we both know it."])
    fight += S.narrate(["You ask what way that is."])
    fight += S.say("Ambrose", [
        "The dead hero in the mound fights the",
        "living one. It's what's done.",
        "It's on the sign outside. It's in the",
        "chalk. It's in the shape of the room."])
    fight += S.say("Ambrose", [
        "I didn't ask for any of it.",
        "I asked for a bench.",
        "Come on then. Let's do what's done."])
    fight += [R.play_me("Shock2"), R.wait(30),
              R.battle(db.TR_FORTY_FOURTH, can_escape=False, can_lose=False),
              R.control_switch(db.SW_BARROW_BEATEN, True)]

    fight += [R.fadeout_bgm(2), R.wait(50)]
    fight += S.narrate(["Ambrose Fitch sits down on the floor of his",
                        "own burial chamber, which is not, you notice,",
                        "something the shape of the room allows for."])
    fight += S.say("Ambrose", [
        "Well. That's that done.",
        "Forty years I've been waiting to have",
        "that fight and it took four minutes."])
    fight += S.narrate(["You ask why he did it, if he did not want to."])
    fight += S.say("Ambrose", [
        "Because it's what's done. Weren't you",
        "listening?",
        "That's the whole trouble with the lot",
        "of us. It's what's done, so we do it."])
    fight += S.narrate(["He looks up at the ceiling of the mound."])
    fight += S.say("Ambrose", [
        "They ignored me for forty years.",
        "Then I died, and within a fortnight",
        "there were masons out here. Masons!",
        "For a man they never once wrote to."])
    fight += S.say("Ambrose", [
        "Take the sword. Take the ring.",
        "They're no good to me and they were",
        "never really mine - they were what a",
        "hero is supposed to be buried with."])
    fight += S.narrate([
        "Got the Forty-Fourth's grave goods, given",
        "rather than taken, which he is extremely",
        "particular about."])
    fight += S.narrate(["You ask if there is anything he wants."])
    fight += S.say("Ambrose", [
        "A bench."])
    fight += S.narrate(["You wait. That is the whole request."])
    fight += S.say("Ambrose", [
        "Top of the mound. Facing the sea.",
        "You can see the north road from up there.",
        "People walk that road tired and there's",
        "nowhere for them to sit down for four miles."])
    fight += S.say("Ambrose", [
        "Forty years of standing in a circle",
        "and that's what I want. A bench.",
        "Anyone's bench. Not mine. Anyone's."])
    fight += [R.control_switch(db.SW_BENCH_ASKED, True), S.trope()]
    fight += S.say("Ambrose", [
        "And if you see Ysolde - and you will,",
        "she'll be in the Wyvern with that kit",
        "open in front of her - tell her I said",
        "she was right about the four hit points."])

    after = S.say("Ambrose", [
        "Still no bench.",
        "I'm not going anywhere. That's rather",
        "the difficulty."])

    seated = S.narrate([
        "The burial chamber is empty.",
        "The circle somebody drew on the floor has",
        "gone unswept for the first time in forty",
        "years, and there is nobody standing in it."])
    seated += S.narrate([
        "If you want him, he is on the top of the",
        "mound, on a bench, facing the sea."])

    return R.event(event_id, "Ambrose Fitch (#44)", x, y, [
        R.page(fight, img=img, trigger=0, priority=1, direction_fix=True),
        R.page(after, img=img, trigger=0, priority=1, direction_fix=True,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_BENCH_ASKED}),
        R.page(seated, img=R.image(""), trigger=0, priority=0, through=True,
               conditions={"switch1Valid": True,
                           "switch1Id": db.SW_BENCH_DONE}),
    ])


def build():
    R.save_map(MAP_PIT, pit_map())
    R.save_map(MAP_BARROW, barrow_map())
