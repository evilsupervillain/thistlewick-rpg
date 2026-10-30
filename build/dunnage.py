"""Maps 61-65: Great Dunnage - the town, the Company of Smiths' hall, the
Sealed Counting House, the Bonded Warehouse and the Bell.

`../SITES.md` step 18. The source is `../COMPANIONS.md` L1, "the big one":
down the valley from Upper Clanging, where Cotter Cotterill already works.
Upper Clanging is a works with a town round it; **Great Dunnage is a town
with nine works in it**, and it is to Upper Clanging what Upper Clanging is
to Thistlewick - bigger, richer, louder, and completely uninterested in the
Prophecy. The joke of the place is **municipal self-regard**: a Corporation,
a Mayor, a motto, a crest, an anthem, and a counting house it cannot open. It
considers Upper Clanging charming. **Nobody in it has ever heard of Bram.**

This module builds the places and the people and **not the quests**. Six
companions have quests here, and each one is decided below - a refusal, a
reaction shot, or nothing:

* **Nix at the Bonded Warehouse is a refusal, on its door.** NIX-1 is going
  in there after eleven years of not, so walking in is the quest. It is an
  inner door, not the world-map one: a refusal at the gate would lock the
  whole town, and five other companions' places with it. Nix at the
  Counting House's door is a **reaction shot** - NIX-2 is opening it, and
  looking at it is not.
* **Hob at the Schedule is a reaction shot.** HOB-1 is a retrieval tour and a
  submission; walking into the Company's hall is neither. He reads clause
  two twice and says nothing.
* **Aldric and the horse is a reaction shot.** ALD-4 is the reunion, and it
  does not happen: he pats a good grey mare in passing, and she goes on
  looking at the road. Neither of them looks at the other.
* **Piper at the Contest's poster is a reaction shot.** PIP-3 is entering it,
  and she does not.
* **Corvin and Appraiser Fettle is a reaction shot.** COR-5 is the appraisal,
  and he will not hand the sword over. Nothing in this module mentions a
  curse; the form for one is COR-5's.
* **Roland: nothing.** ROL-1 is a summons, and nothing has summoned him. The
  review meeting needs a Convenor and a room, and a line about either would
  be the quest's set-up done by somebody else.
* HOB-4's "approach" is the west road, which is already there.

**One trope** - the watchman at the gate who has never heard of you - **and
one blush**, Cotter's, which is his mother's line about his father, in his
own mouth, meant exactly as said.
"""
import handdrawn as HD
import mapkit as K
import rmmzdata as R

import db
import story as S
import q_aldric
import q_corvin
import q_nix
import q_piper
import q_roland
import q_hob
import q_spare
from places import (MAP_WORLD, MAP_DUNNAGE, MAP_SMITHS_HALL,
                    MAP_COUNTING_HOUSE, MAP_BONDED, MAP_BELL, DUNNAGE_STEP,
                    VAULT, VAULT_CHAIR, COUNTING_BEFORE_DOOR, CULVERT_STEP)

# The name `worldmap.json`'s door events carry for this site.
SITE = "Great Dunnage"


def _pair(first, later):
    """A first conversation and the short one after it, on self switch A."""
    return first + [R.self_switch("A", True)], later


def _person(event_id, name, xy, img, first, later, **kw):
    return R.event(event_id, name, *xy, [
        R.page(first, img=img, trigger=0, priority=1, **kw),
        R.page(later, img=img, trigger=0, priority=1,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"},
               **kw),
    ])


def _thing(event_id, name, xy, first, later=None):
    """Something read with the action button, with no sprite of its own."""
    if later is None:
        return R.event(event_id, name, *xy, [R.page(first, **PAGE)])
    return R.event(event_id, name, *xy, [
        R.page(first, **PAGE), R.page(later, conditions=LATER, **PAGE)])


def _exit(event_id, x, y, target_map, tx, ty):
    return R.event(event_id, "The Door", x, y, [R.page(
        [R.play_se("Move1"), R.transfer(target_map, tx, ty, 2, 0)],
        img=R.image(""), trigger=1, priority=0, through=True)])


PAGE = dict(img=R.image(""), trigger=0, priority=1, direction_fix=True)
LATER = {"selfSwitchValid": True, "selfSwitchCh": "A"}

STACKED = K.sf_grid("Inside_B", "Stacked Crates", 2)
LARGE_CRATE = K.sf_block("Inside_B", "Large Crate")   # 1x2: lid over crate
CRATE_A = K.sf_tile("Inside_B", "Crate A")
CRATE_B = K.sf_tile("Inside_B", "Crate B")
IN_BARREL = K.sf_tile("Inside_B", "Barrel")
CLOSET = K.sf_block("Inside_B", "Closet")             # 1x2, a wardrobe
TABLE_C = K.sf_tile("Inside_B", "Table C")            # the red cloth
TABLE_D = K.sf_tile("Inside_B", "Table D")            # a plain desk
TAPESTRY = K.sf_block("Inside_B", "Tapestry A")       # 1x2, red and gold
NOTICE = K.sf_tile("Inside_B", "Posted Notice")
ANVIL = (K.sf_tile("Inside_C", "Blacksmith's Table A"),
         K.sf_tile("Inside_C", "Blacksmith's Table B"))
HAMMERS = K.sf_tile("Inside_C", "Hammers")
SWORD = K.sf_tile("Inside_C", "Sword A")
ARMOUR = K.sf_tile("Inside_C", "Armor A (Stand)")
LEDGER = K.sf_tile("Inside_C", "Closed Books C")
OPEN_BOOK = K.sf_tile("Inside_C", "Open Book A (H)")
HAY = K.sf_tile("Outside_B", "Hay")
GRATE = K.sf_tile("Outside_B", "Window F")             # laid flat: the culvert
BOLLARD = K.sf_tile("Outside_B", "Mooring Bollard A")
BOLLARD_ROPE = K.sf_tile("Outside_B", "Mooring Bollard B (Rope)")
CRATE_OUT = K.sf_tile("Outside_B", "Crate A")
CRATE_OUT_D = K.sf_tile("Outside_B", "Crate D")
STATUE = K.sf_block("Outside_C", "Statue A")          # 1x2, a knight
PORT = K.A(12)                  # Outside_A1 `Water E (Port)`: a stone quay


# ================================================================ the town ==
# Inside the wall. The works along the north side, with their chimneys; the
# haulage yard in the north-west corner; the Counting House and the Bell on
# the square; the Bonded Warehouse on the canal basin to the east; and the
# south range facing out on to the road, with the gate a gap in it - a
# building's only face is its south side, so the range is read from outside.
TW, TH = 36, 28
# The works stand shoulder to shoulder, so there is no alley between them
# running off the top of the map.
IRONWORKS = (0, 0, 12, 7)       # x, y, w, h: front wall row is y + h - 1
SMITHS = (12, 0, 11, 7)
FOUNDRY = (23, 0, 13, 7)
STABLE = (0, 10, 5, 5)
COUNTING = (11, 10, 7, 5)
BELL = (19, 10, 7, 5)
WAREHOUSE = (27, 10, 6, 6)
WEST_RANGE = (0, 22, 16, 4)
EAST_RANGE = (19, 22, 17, 4)
YARD = (0, 10, 9, 19)           # x1, y1, x2, y2: the fence runs round it
YARD_GAP = (15, 16)             # the gate in its east fence
SQUARE = (11, 15, 26, 19)
CANAL = (33, 10, 35, 19)
WHARF = (27, 16, 32, 19)
GATE_X = (16, 17, 18)
ROAD_Y = TH - 2
ARRIVE = (17, ROAD_Y)

SMITHS_DOOR = (17, 6)
COUNTING_DOOR = (14, 14)
BELL_DOOR = (22, 14)
WAREHOUSE_DOOR = (29, 15)

WATCHMAN = (16, 23)             # in the gate passage, on its west side
ARMS = (14, 25)                 # on the range's front, read from the road
ANTHEM = (12, 17)
NINE_WORKS = (23, 17)
FIRST_MAYOR = (18, 17)          # `Statue A`, 1x2, a knight on a plinth
COTTER = (6, 7)                 # at the Iron Company's gate, beside it
POSKITT = (20, 18)
PLUMMER = (6, 14)
DUCHESS = (2, 15)               # at her stable door
CART = (6, 17)
PARTNER_SIGN = (8, 17)          # inside the yard gate, read from above


def town_map():
    w, h = TW, TH
    g = K.Canvas(w, h)
    # One paving everywhere inside the wall: two kinds side by side draw a
    # grass seam between them, which is a village, not a town.
    g.fill(0, 0, w - 1, h - 1, 0, K.PAVING)
    g.fill(0, ROAD_Y, w - 1, h - 1, 0, K.PATH)
    # The gate's paving runs on across the verge to the map edge, so the way
    # out is a road the player can see and not a strip of open sand (Mike,
    # October 2026: an open edge's exit is on the road, and the road reaches
    # the edge).
    g.fill(GATE_X[0], ROAD_Y, GATE_X[-1], h - 1, 0, K.PAVING)
    x1, y1, x2, y2 = YARD
    g.fill(x1, y1, x2, y2, 0, K.PATH)
    g.fill(*CANAL, 0, PORT)

    # Along the north side the fence runs on behind the stable (Mike, October
    # 2026), where the ridge of its roof lets it show - laid before the
    # stable is, since nothing is drawn on a house once it is up.
    for x in range(x1, x1 + 5):
        g.set(x, y1, 1, K.DECKING)
    for b, wall, roof in [
            (IRONWORKS, K.WALL_BRICK_RED, K.ROOF_BROWN),
            (SMITHS, K.WALL_STONE, K.ROOF_GREEN),
            (FOUNDRY, K.WALL_BRICK_RED, K.ROOF_BROWN),
            (STABLE, K.WALL_PLANK, K.ROOF_GOLD),
            (COUNTING, K.WALL_STONE_WHITE, K.ROOF_GREEN),
            (BELL, K.WALL_TIMBER, K.ROOF_BROWN),
            (WAREHOUSE, K.WALL_BRICK_RED, K.ROOF_BROWN),
            (WEST_RANGE, K.WALL_STONE, K.ROOF_GREEN),
            (EAST_RANGE, K.WALL_STONE, K.ROOF_GREEN)]:
        g.building(*b, wall=wall, roof=roof)

    # The yard's fence, a wooden overlay on layer 1, with a gap for the gate.
    for x in range(x1 + 5, x2 + 1):
        g.set(x, y1, 1, K.DECKING)
    for y in range(y1, y2 + 1):
        if y not in YARD_GAP:
            g.set(x2, y, 1, K.DECKING)
    for x in range(x1, x2 + 1):
        g.set(x, y2, 1, K.DECKING)
    g.autotile(0)
    g.autotile(1)

    # The works: shut gates and chimneys, two stacks apiece.
    for b, gate_x, stacks in [(IRONWORKS, 5, (2, 7)), (FOUNDRY, 29, (26, 32))]:
        fy = b[1] + b[3] - 1
        for x in (gate_x - 2, gate_x + 2):
            g.set(x, fy - 1, 3, K.WINDOW)
        for cx in stacks:
            for i, t in enumerate(K.CHIMNEY_STACK):
                g.chimney(cx + i % 2, 2 + i // 2, t)

    # The Company's hall: windows either side of its door, and its sign.
    fy = SMITHS[1] + SMITHS[3] - 1
    for x in (14, 15, 19, 20):
        g.set(x, fy - 1, 3, K.WINDOW)
    g.set(SMITHS_DOOR[0], fy - 1, 3, K.SIGN_HAMMER)
    # The Counting House: the Corporation's crest and a coin, and no windows,
    # since there is nothing in it to look at.
    fy = COUNTING[1] + COUNTING[3] - 1
    g.set(12, fy - 1, 3, K.SIGN_COIN)
    g.set(COUNTING_DOOR[0], fy - 1, 3, K.SIGN_SUN)
    g.set(16, fy - 1, 3, K.SIGN_COIN)
    # The Bell: a window and its sign.
    fy = BELL[1] + BELL[3] - 1
    for x in (20, 25):
        g.set(x, fy - 1, 3, K.WINDOW)
    g.set(BELL_DOOR[0] + 1, fy - 1, 3, K.SIGN_MUG)
    # The warehouse: one high window.
    fy = WAREHOUSE[1] + WAREHOUSE[3] - 1
    g.set(31, fy - 1, 3, K.WINDOW)
    # The south range, seen from the road, and the arms over the gate.
    fy = WEST_RANGE[1] + WEST_RANGE[3] - 1
    for x in (2, 6, 10, 21, 25, 29, 33):
        g.set(x, fy - 1, 3, K.WINDOW)
    g.set(ARMS[0], fy - 1, 3, K.SIGN_SUN)

    # The square: two lamps, the anthem and the nine works.
    for x in (13, 24):
        g.column(x, 15, 3, K.LAMP)
    g.set(*ANTHEM, 3, K.FENCE_PANEL)
    g.set(*NINE_WORKS, 3, K.FENCE_PANEL)
    g.column(FIRST_MAYOR[0], FIRST_MAYOR[1] - 1, 3, STATUE)

    # The yard: hay by the stable, a barrel, and the partner's sign.
    g.scatter([(0, 15), (0, 16), (1, 17)], 3, HAY)
    g.set(8, 11, 3, K.BARREL)
    g.set(*PARTNER_SIGN, 3, K.FENCE_PANEL)

    # The wharf: crates in bond waiting to go in, and the bollards.
    g.scatter([(27, 17), (28, 17), (27, 18)], 3, CRATE_OUT)
    g.set(28, 19, 3, CRATE_OUT_D)
    g.set(32, 17, 3, BOLLARD_ROPE)
    g.set(32, 19, 3, BOLLARD)
    g.scatter([(26, 13), (26, 14)], 3, K.BARREL)

    m = K.new_map(w, h, K.TS_OUTSIDE, name="Great Dunnage", bgm="Town3",
                  bgm_volume=70)
    m["data"] = g.data
    m["events"] = [None] + q_aldric.with_follower(town_events(), MAP_DUNNAGE)  # ALD-5
    # 20, after the Fourth's 19: the grate over the bottom lock, where
    # Cotter's errand stands the party before Spare goes down (SPA-2), so the
    # culvert has a way in that can be seen. Mike's, from the editor (October
    # 2026): `Window F` laid flat in the street, as an event so that it is
    # drawn over the paving and stood on.
    m["events"].append(R.event(len(m["events"]), "The Bottom Lock Grate",
                               *CULVERT_STEP, [R.page(
        [], img=R.image(tile_id=GRATE, pattern=0), priority=0, through=True)]))
    assert m["events"][-1]["id"] == 20
    m["events"] += works_gates(len(m["events"]))
    return m


def works_gates(first_id):
    """The Iron Company's gate and the foundry's, which do not open, and
    say why: iron doors, `!Door1` pattern 2. They were shutters until
    October 2026, and read as windows (`story.shut`); appended after the
    grate, so no id above moved."""
    company = S.narrate([
        "THE IRON COMPANY. The gate is barred, and a brass plate",
        "on it says NO ADMITTANCE EXCEPT ON BUSINESS."])
    company += S.narrate([
        "A smaller plate under it, newer, says HEROES ARE NOT",
        "BUSINESS. Somebody has had a hero in, once."])
    foundry = S.narrate([
        "The foundry gate, shut, with a board wired to it:",
        "'NO VISITORS. THE CRUCIBLES ARE NOT MIMICS. THE MOULDS",
        "ARE NOT MIMICS. NOTHING IN HERE IS A MIMIC.'"])
    foundry += S.narrate(["'PLEASE STOP HITTING THINGS TO CHECK.'"])
    return [S.shut_door(first_id + i, name, x, b[1] + b[3] - 1, cmds,
                        pattern=2)
            for i, (name, b, x, cmds) in enumerate([
                ("The Iron Company's Gate", IRONWORKS, 5, company),
                ("The Foundry Gate", FOUNDRY, 29, foundry)])]


def watchman_pages():
    first = S.narrate([
        "A watchman in the gateway, in the Corporation's blue coat,",
        "with the air of a man who has been asked to be impressive",
        "and is doing his best."])
    first += S.say("Watchman", [
        "Halt. Name and",
        "business."])
    first += S.narrate([
        "You say that you are Bram, of Thistlewick, Chosen One",
        "number forty-eight."])
    first += S.say("Watchman", [
        "Forty-eight what?"])
    first += S.narrate(["You explain about the Prophecy."])
    first += S.say("Watchman", [
        "Thistlewick.",
        "That's the Prophecy people, down south.",
        "Charming."])
    first += S.say("Watchman", [
        "Business?"])
    first += S.narrate(["You say that you are passing through."])
    first += S.say("Watchman", [
        "Everybody is, sir.",
        "Nobody's too busy for Great Dunnage.",
        "They only think they are."])
    first += S.narrate([
        "He takes out a ledger, writes BRAM (THISTLEWICK) - PROPHECY,",
        "SOME SORT in it, and lets you in."])
    first += [S.trope()]
    later = S.say("Watchman", [
        "Carry on, sir. Mind",
        "the carts. Mind the canal. Mind the",
        "Mayor."])
    return _pair(first, later)


def arms_pages():
    first = S.narrate([
        "Over the gate, on a gilded board, the arms of the",
        "Corporation of Great Dunnage: an anvil, a bell and a key,",
        "done so small and so gold that from the road they look like",
        "a flourish."])
    first += S.narrate([
        "Under them, the motto: QUIS SIMILIS NOBIS?",
        "",
        "Who is like unto us?",
        "The Corporation has looked into it."])
    first += S.narrate([
        "The key is the key to the Counting House. It is the only",
        "one the town still has, and it is painted on a board."])
    later = S.narrate(["QUIS SIMILIS NOBIS? The Corporation has looked into it."])
    return _pair(first, later)


def anthem_pages():
    return S.narrate([
        "THE ANTHEM OF GREAT DUNNAGE. To be sung standing, all nine",
        "verses, on the Mayor's Day."]) + S.narrate([
        "Great Dunnage! Great Dunnage!",
        "Nine chimneys, and more!",
        "We make what they make up at Clanging,",
        "but more."]) + S.narrate([
        "Verse two is the same, but more."])


def nine_works_pages():
    return S.narrate([
        "THE NINE WORKS OF THE CORPORATION OF GREAT DUNNAGE:"]) + S.narrate([
        "The Dunnage Iron Company. The Bell Foundry. The Nail Works.",
        "The Chain Works. The Wire Works. The Anchor Works.",
        "The Screw Works. The Brass Works. The Other Nail Works."]) + \
        S.narrate([
            "And along the bottom, in smaller letters:",
            "See also UPPER CLANGING - a works, up the valley.",
            "Charming."])


def first_mayor_pages():
    first = S.narrate([
        "A statue on a plinth, in the middle of the square: a knight",
        "in full armour, with a sword and a shield."])
    first += S.narrate([
        "ALDERMAN JOSIAH DUNNAGE, FIRST MAYOR. Erected by the",
        "Corporation, to the Corporation's own design, at the",
        "Corporation's expense, in honour of the Corporation."])
    first += S.narrate([
        "Under it, smaller: The armour is allegorical. Alderman",
        "Dunnage sold nails."])
    later = S.narrate([
        "The First Mayor, in allegorical armour. He sold nails."])
    return _pair(first, later)


def cotter_pages():
    first = S.narrate([
        "A young man in a white work jacket, at the gate of the Iron",
        "Company. The shift bell has just gone."])
    first += S.say("Cotter", [
        "Cotter Cotterill.",
        "Upper Clanging, originally. Eldest of",
        "nine."])
    first += S.narrate([
        "You say that Great Dunnage seems a very big place."])
    first += S.say("Cotter", [
        "Nine works. I'm on",
        "the big furnace at the Iron Company",
        "till the spring. Then home for good."])
    first += S.narrate([
        "You ask whether he gets home at all before then."])
    first += S.say("Cotter", [
        "Every Saturday.",
        "Off at six, eleven miles up the valley,",
        "and back down for the Monday."])
    first += S.narrate([
        "You say that it is twenty-two miles, for one night."])
    first += S.say("Cotter", [
        "I'm always very",
        "glad to get home."])
    first += S.narrate([
        "He says it with great simplicity, as a fact about the",
        "weather."])
    first += [S.blush()]
    # If you have met the family, he has a message. It is not a secret.
    first += R.if_then(
        R.condition_switch(db.SW_COTTERILL),
        S.narrate(["You say that you have met his family."])
        + S.say("Cotter", [
            "All of them? Then",
            "you've met Bessie. Tell her Saturday."]))
    later = S.say("Cotter", [
        "Saturday. Six",
        "o'clock. Eleven miles."])
    return _pair(first, later)


def poskitt_pages():
    first = S.say("Mrs Poskitt", [
        "Visitors! Not from",
        "up the valley? Oh, you'd love Upper",
        "Clanging. We went up for the day."])
    first += S.say("Mrs Poskitt", [
        "Only the one works!",
        "And they all know each other! We",
        "thought it was ever so sweet."])
    first += S.narrate(["You ask what Great Dunnage is like."])
    first += S.say("Mrs Poskitt", [
        "Oh, like that. But",
        "nine times."])
    later = S.say("Mrs Poskitt", [
        "Nine times! Mind",
        "you, they've a very nice sign."])
    return _pair(first, later)


def plummer_pages():
    first = S.narrate([
        "A broad man in a brown coat, with a moustache, keeping an",
        "eye on the yard."])
    first += S.say("Mr Plummer", [
        "Plummer. Haulage.",
        "Anything, anywhere, by Tuesday."])
    first += S.narrate(["You ask who the partner is."])
    first += S.say("Mr Plummer", [
        "Her. The grey."])
    first += S.say("Mr Plummer", [
        "Walked in off the",
        "west road one winter, on her own, with",
        "a good saddle on and nobody in it."])
    first += S.say("Mr Plummer", [
        "Nobody came for her.",
        "So she stayed. Best worker in the yard.",
        "Knows every road in the valley."])
    first += S.say("Mr Plummer", [
        "She has a stall",
        "with her name on it and a say in the",
        "routes. It seemed only fair."])
    first += S.narrate(["You ask what her name is."])
    first += S.say("Mr Plummer", [
        "Duchess. There was",
        "a crest on the saddle. It seemed to",
        "suit her."])
    later = S.say("Mr Plummer", [
        "Anything, anywhere,",
        "by Tuesday. She plans the Tuesdays."])
    return _pair(first, later)


def duchess_pages():
    """The horse. ALD-4 is the reunion, and with Sir Aldric in the party it
    does not happen: he pats a good horse in passing, and she goes on looking
    at the road. Neither of them looks at the other. Her direction is fixed,
    so she does not turn to the player either."""
    first = [R.play_se("Horse", 70)]
    first += S.narrate([
        "A grey mare in harness, standing at her stable door as if",
        "she is waiting for the Tuesday. She considers you with great",
        "calm, the way a partner in a business considers a customer."])
    aldric = S.narrate([
        "Sir Aldric gives the grey a pat on the neck in passing, the",
        "way he would any good horse."])
    aldric += S.say("Aldric", ["Good girl."])
    aldric += S.narrate([
        "She flicks an ear. She goes on looking at the road, and he",
        "goes on looking at the cart."])
    first += R.if_then(R.condition_actor_in_party(db.ALDRIC), aldric)
    later = S.narrate(["Duchess. She is considering the Tuesdays."])
    later += R.if_then(R.condition_actor_in_party(db.ALDRIC), S.narrate([
        "Sir Aldric has found something to admire about the cart."]))
    return first + [R.self_switch("A", True)], later


def cart_pages():
    return S.narrate([
        "A haulage cart, empty and swept. On the tailboard, in good",
        "paint: PLUMMER & PARTNER."])


def partner_sign_pages():
    return S.narrate([
        "PLUMMER & PARTNER. HAULAGE.",
        "Anything, anywhere, by Tuesday."]) + S.narrate([
        "And under it, in a different paint and a different hand:",
        "(THE PARTNER IS THE GREY.)"])


def warehouse_door():
    """The Bonded Warehouse's door, which Nix does not go through.

    NIX-1 is going in there after eleven years of not, so with Nix in the
    party the door is a refusal. Followers are drawn, so Nix cannot wait on
    the wharf while their sprite follows you in. It is the warehouse's door
    and not the town's: the town has five other companions' business in it.
    NIX-1 appends its own page after these."""
    img = R.image("!Door1", 0, direction=2)
    x1, y1, x2, y2, door_x = BONDED_ROOM
    nix = {"actorValid": True, "actorId": db.NIX}
    stop = S.narrate([
        "Nix stops a yard short of the warehouse door, and looks at",
        "it."])
    stop += S.say("Nix", ["Not that one."])
    stop += S.narrate([
        "You have seen Nix go through a great many doors, several of",
        "them locked. You have never before seen Nix walk away from",
        "one, and Nix walks away from this one quite fast."])
    stop += [R.self_switch("A", True)]
    again = S.say("Nix", ["Still not that one."])
    return R.event(7, "The Bonded Warehouse", *WAREHOUSE_DOOR, [
        R.page(S.door_page(MAP_BONDED, door_x, y2 + 1, 8), img=img,
               trigger=1, priority=1),
        R.page(stop, img=img, trigger=1, priority=1, conditions=nix),
        R.page(again, img=img, trigger=1, priority=1,
               conditions=dict(nix, selfSwitchValid=True, selfSwitchCh="A")),
    ])


def town_events():
    evs = []
    # 1-3: the road back out, all three cells of the gate, below characters.
    for i, x in enumerate(GATE_X):
        evs.append(R.event(i + 1, "The Road Out", x, TH - 1, [R.page(
            [R.play_se("Move1"), R.transfer(MAP_WORLD, *DUNNAGE_STEP, 2, 0)],
            img=R.image(""), trigger=1, priority=0, through=True)]))

    # 4-6: the Company's hall, the Counting House and the Bell. 7 is the
    # warehouse, whose door says no to Nix.
    evs.append(S.door(4, "The Smiths' Hall", *SMITHS_DOOR, MAP_SMITHS_HALL,
                      SMITHS_ROOM[4], SMITHS_ROOM[3] + 1, direction=8))
    evs.append(S.door(5, "The Counting House", *COUNTING_DOOR,
                      MAP_COUNTING_HOUSE, COUNTING_ROOM[4],
                      COUNTING_ROOM[3] + 1, direction=8))
    evs.append(S.door(6, "The Bell", *BELL_DOOR, MAP_BELL, BELL_ROOM[4],
                      BELL_ROOM[3] + 1, direction=8))
    evs.append(q_nix.warehouse_door_pages(warehouse_door()))       # NIX-1

    # 8: the watchman in the gate passage. 9: the arms over the gate, on the
    # range's front wall and read from the road below it.
    evs.append(_person(8, "Watchman", WATCHMAN,
                       R.image(*S.FACES["Watchman"], direction=6), *watchman_pages()))
    evs.append(_thing(9, "The Arms", ARMS, *arms_pages()))
    # 10, 11: the anthem and the nine works, on the square.
    evs.append(_thing(10, "The Anthem", ANTHEM, anthem_pages()))
    evs.append(_thing(11, "The Nine Works", NINE_WORKS, nine_works_pages()))
    # 12: Cotter, at the Iron Company's gate.
    evs.append(q_spare.cotter(q_hob.owned("cotter", _person(  # HOB-1, SPA-2
        12, "Cotter", COTTER,
        R.image(*S.FACES["Cotter"], direction=2), *cotter_pages()))))
    # 13: Mrs Poskitt, on the square.
    evs.append(_person(13, "Mrs Poskitt", POSKITT,
                       R.image(*S.FACES["Mrs Poskitt"], direction=2), *poskitt_pages()))
    # 14-17: the haulage yard - Mr Plummer, Duchess, the cart and the sign.
    plummer = _person(14, "Mr Plummer", PLUMMER,
                      R.image(*S.FACES["Mr Plummer"], direction=4), *plummer_pages())
    plummer["pages"] += q_aldric.plummer_pages(plummer["pages"][-1])  # ALD-4
    evs.append(plummer)
    first, later = duchess_pages()
    duchess = _person(15, "Duchess", DUCHESS,
                      R.image("Vehicle", 4, direction=2), first, later,
                      direction_fix=True)
    duchess["pages"].append(q_aldric.duchess_page(duchess["pages"][-1]))  # ALD-4
    assert duchess["id"] == q_aldric.DUCHESS_EVENT
    evs.append(duchess)
    evs.append(R.event(16, "The Cart", *CART, [R.page(
        cart_pages(), img=R.image("Vehicle", 6, direction=2), trigger=0,
        priority=1, direction_fix=True)]))
    sign = _thing(17, "Plummer & Partner", PARTNER_SIGN, partner_sign_pages())
    sign["pages"].append(q_aldric.sign_page(sign["pages"][0]))    # ALD-4
    evs.append(sign)
    # 18: the First Mayor, in the middle of the square.
    evs.append(_thing(18, "The First Mayor", FIRST_MAYOR,
                      *first_mayor_pages()))
    return evs


# ======================================================== the Smiths' Hall ==
# The hall of the Worshipful Company of Smiths. The Company's banners on the
# north wall, the Schedule beside them, and the Wardens' table under them;
# the last Assize's prize on the Company's anvil in the west end, and the
# appraiser's bench in the east.
#               x1 y1  x2  y2 door_x
SMITHS_ROOM = (2, 4, 19, 9, 10)
SW, SH = 22, 14
SCHEDULE = (6, 3)               # on the wall face, read from below
STANNARD = (10, 6)
CRABBE = (13, 6)
WARDENS_TABLE = range(8, 15)
PRIZE = (4, 8)                  # the anvil, with the hinge on it
FETTLE = (15, 8)
BENCH = [(16, 8), (17, 8)]


def smiths_map():
    x1, y1, x2, y2, door_x = SMITHS_ROOM
    g = K.interior(SW, SH, x1, y1, x2, y2, door_x=door_x,
                   floor=K.IN_BRICK_FLOOR, wall_top=K.IN_WALL_TOP_STONE,
                   wall_face=K.IN_WALL_FACE_STONE)
    # A red runner from the door to the Wardens' table.
    g.fill(door_x, 7, door_x + 1, y2, 1, K.IN_RED_CARPET)
    g.autotile(1)

    # The north wall: the Company's banners over the table, sword racks at
    # either end, and the Schedule.
    for x in (10, 11):
        g.column(x, y1 - 2, 2, TAPESTRY)
    for x in (4, 17):
        g.column(x, y1 - 2, 2, K.IN_SWORD_RACK)
    g.set(*SCHEDULE, 2, NOTICE)

    # The Wardens' table, in the red cloth, with the Company's hammers on it.
    for x in WARDENS_TABLE:
        g.set(x, 5, 2, TABLE_C)
    g.set(12, 5, 3, HAMMERS)
    g.set(9, 5, 3, LEDGER)

    # The west end: the last prize on the Company's anvil, and armour.
    g.set(PRIZE[0], PRIZE[1], 2, ANVIL[0])
    g.set(PRIZE[0] + 1, PRIZE[1], 2, ANVIL[1])
    for y in (5, y2):
        g.set(x1, y, 2, ARMOUR)
    # The east end: the appraiser's bench, with a sword on it.
    for x, y in BENCH:
        g.set(x, y, 2, TABLE_D)
    g.set(*BENCH[1], 3, SWORD)
    g.set(*BENCH[0], 3, OPEN_BOOK)

    m = K.new_map(SW, SH, K.TS_INSIDE, name="The Smiths' Hall", bgm="Town3",
                  bgm_volume=50, battleback=("Wood1", "Room1"))
    m["data"] = g.data
    m["events"] = [None] + smiths_events()
    return m


def stannard_pages():
    first = S.narrate([
        "A tall woman in black, with iron-grey hair pinned up and",
        "gold at her collar, standing at the Company's table as if",
        "it might try something."])
    first += S.say("Prime Warden", [
        "Stannard. Prime",
        "Warden of the Worshipful Company of",
        "Smiths of Great Dunnage."])
    first += S.say("Prime Warden", ["Are you a smith?"])
    first += S.narrate(["You say that you are a turnip farmer."])
    first += S.say("Prime Warden", [
        "Then you may look.",
        "Do not touch. The Assize is in the",
        "spring. It is every three years."])
    first += S.narrate(["You ask what the Assize is."])
    first += S.say("Prime Warden", [
        "Every smith in the",
        "land may submit one piece, to be",
        "judged by the Wardens against the",
        "Schedule."])
    first += S.say("Prime Warden", [
        "Very few manage to",
        "submit one. It is a very good",
        "Schedule."])
    later = S.say("Prime Warden", [
        "Look. Do not",
        "touch. The Schedule is on the wall."])
    return _pair(first, later)


def crabbe_pages():
    first = S.say("Warden Crabbe", [
        "Crabbe. Junior",
        "Warden. I read the Schedule out, at",
        "the Assize. It takes most of the day."])
    first += S.say("Warden Crabbe", [
        "People ask why we",
        "don't just pin it up. We do. I read",
        "it out as well. It's a very good",
        "Schedule."])
    later = S.say("Warden Crabbe", [
        "Clause forty. A",
        "pair of tongs is one piece. A tong is",
        "not a piece. Nobody has ever tried."])
    return _pair(first, later)


def schedule_pages():
    """The Schedule of What Constitutes a Piece. With Hob in the party it is a
    reaction shot, not HOB-1: he reads clause two twice, and says nothing."""
    cmds = S.narrate([
        "THE SCHEDULE OF WHAT CONSTITUTES A PIECE, being the rules of",
        "the Assize of Hammers, in forty-one clauses, of which:"])
    cmds += S.narrate([
        "1. A piece shall be the entrant's own work, from the ore up.",
        "2. A piece shall be the entrant's own property.",
        "3. A hinge is a piece. Half a hinge is not a piece. A pair",
        "of hinges is two pieces, unless submitted as a door."])
    cmds += S.narrate([
        "41. The decision of the Wardens is final, and so is the",
        "Schedule."])
    hob = S.narrate([
        "Hob reads it all the way down, slowly, with one finger, and",
        "then goes back up to clause two and reads that again."])
    hob += S.narrate([
        "He says nothing at all. On the way past the door he looks",
        "at its hinges, for a while."])
    return cmds + R.if_then(R.condition_actor_in_party(db.HOB), hob)


def prize_pages():
    return S.narrate([
        "THE ASSIZE OF HAMMERS. The prize piece of the last Assize,",
        "on the Company's own anvil: a hinge."]) + S.narrate([
        "It is a very good hinge. A card beside it says: Clauses one",
        "to forty-one, satisfied. The Company's mark, awarded."])


def banners_pages():
    return S.narrate([
        "The Company's banners, red and gold, and worked along the",
        "bottom of each, the Company's motto: BY HAMMER AND HAND.",
        "Under that, in chalk, in a smaller hand: AND BY SCHEDULE."])


def fettle_pages():
    """Appraiser Fettle. With Corvin in the party it is a reaction shot, not
    COR-5: she sees the black sword, and he will not hand it over. Nothing
    here mentions a curse, and the form for one is COR-5's."""
    corvin = S.narrate([
        "Her eyes go straight past you to the black sword at Corvin's",
        "side, and stay there."])
    corvin += S.say("Miss Fettle", [
        "Oh. Oh, may I -",
        "just the handle -"])
    corvin += S.say("Corvin", ["No."])
    corvin += S.say("Miss Fettle", [
        "Quite right. Quite",
        "right. Another time."])
    corvin += S.narrate([
        "She gives him a card. He puts it away without reading it,",
        "and then, when he thinks nobody is looking, reads it."])
    corvin = R.if_then(R.condition_actor_in_party(db.CORVIN), corvin)

    first = S.narrate([
        "A young woman in round spectacles, at a bench with a sword",
        "on it, looking at the sword the way other people look at a",
        "sunset."])
    first += S.say("Miss Fettle", [
        "Look at that. No,",
        "LOOK at it. Fettle. Appraiser to the",
        "Company. Do you see the tang?"])
    first += S.narrate([
        "You say that you cannot see the tang. It is inside the",
        "handle."])
    first += S.say("Miss Fettle", [
        "Exactly! You can't",
        "see it! It's the most important part",
        "of the whole sword, and it's hidden!"])
    first += S.say("Miss Fettle", [
        "Everybody looks at",
        "the blade. Nobody ever asks after the",
        "tang. I always ask after the tang."])
    first += S.narrate(["She wipes her spectacles, overcome."])
    first += S.say("Miss Fettle", [
        "Anything you want",
        "valued, bring it in. Weapons, plate,",
        "heirlooms. I don't charge for tangs."])
    later = S.say("Miss Fettle", [
        "Bring it in! I'll",
        "have the handle off it in a trice."])
    return first + corvin + [R.self_switch("A", True)], later + corvin


def smiths_events():
    x1, y1, x2, y2, door_x = SMITHS_ROOM
    evs = [_exit(1, door_x, y2 + 2, MAP_DUNNAGE, SMITHS_DOOR[0],
                 SMITHS_DOOR[1] + 1)]
    warden = _person(2, "Prime Warden", STANNARD,
                     R.image("Gen_People6", 1, direction=2),
                     *stannard_pages())
    last = warden["pages"][-1]                                    # HOB-1
    warden["pages"] += q_hob.warden_pages(last)
    warden["pages"].append(q_hob.warden_after(last))
    evs.append(warden)
    evs.append(q_hob.owned("crabbe", _person(                      # HOB-1
        3, "Warden Crabbe", CRABBE,
        R.image(*S.FACES["Warden Crabbe"], direction=2), *crabbe_pages())))
    evs.append(_thing(4, "The Schedule", SCHEDULE, schedule_pages()))
    prize = _thing(5, "The Prize", PRIZE, prize_pages())
    prize["pages"].append(q_hob.prize_after(prize["pages"][0]))   # HOB-1
    evs.append(prize)
    evs.append(_thing(6, "The Banners", (10, y1 - 1), banners_pages()))
    fettle = _person(7, "Miss Fettle", FETTLE,
                     R.image("Gen_People6", 4, direction=2),
                     *fettle_pages())
    fettle["pages"] += q_corvin.fettle_pages(fettle["pages"][-1])  # COR-5
    evs.append(fettle)
    return evs


# ==================================================== the Counting House ==
# The lobby, which is what there is of the Counting House that anybody can
# get into: the Door across the north wall, two rows of benches set out for
# the Opening, the Mayor in the aisle, practising, and the Town Clerk at a
# desk with the form. What is behind the Door is NIX-2's, and is not built.
#                 x1 y1  x2  y2 door_x
COUNTING_ROOM = (3, 5, 14, 9, 8)
# At least a screen in each direction: a map smaller than the screen is drawn
# wrapped, and its own south wall turns up again along the top.
CW, CH = 34, 14                 # 18 until NIX-2's room went in the black east
THE_DOOR = (8, 4)               # `!$Gate2`, 3x2, drawn up over the wall face
MAYOR = (7, 6)
MEMORANDUM = (4, 4)
CLERK = (14, 6)
CLERK_DESK = (13, 6)
BENCHES = [(x, y) for y in (7, 8) for x in (4, 5, 6, 10, 11, 12)]
DOOR_IMG = ("!$Gate2", 0)       # pattern 2: the round bronze one


def counting_map():
    x1, y1, x2, y2, door_x = COUNTING_ROOM
    g = K.interior(CW, CH, x1, y1, x2, y2, door_x=door_x,
                   floor=K.IN_DIAMOND_TILE, wall_top=K.IN_WALL_TOP_GOLD,
                   wall_face=K.IN_WALL_FACE_GOLD)
    # A red runner up the aisle to the Door, for the Opening.
    g.fill(door_x - 1, y1, door_x + 1, y2, 1, K.IN_RED_CARPET)
    g.autotile(1)
    g.set(*MEMORANDUM, 2, NOTICE)
    for x, y in BENCHES:
        g.set(x, y, 2, TABLE_D)
    g.set(*CLERK_DESK, 2, TABLE_D)
    g.set(*CLERK_DESK, 3, OPEN_BOOK)
    vault_room(g)                                               # NIX-2
    m = K.new_map(CW, CH, K.TS_INSIDE, name="The Counting House",
                  bgm="Town3", bgm_volume=40, battleback=("Wood1", "Room1"))
    m["data"] = g.data
    m["events"] = [None] + counting_events()
    return m


CHAIR_WOOD = K.sf_block("Inside_B", "Chair A (Wood)")   # 1x2: back, seat


def vault_room(g):
    """NIX-2's room behind the Door, in the lobby's black east: what there is
    of the Counting House past its door. Gold walls like the lobby's, bare
    floor, one chair against the north wall, and nothing else whatever.
    `village.archive_room`'s idiom - `mapkit.interior`'s walls on a second
    room of the same canvas, the doorway cut into the south wall, and the way
    out an event on it, back to the lobby in front of the Door."""
    x1, y1, x2, y2, door_x = VAULT
    top, face = K.IN_WALL_TOP_GOLD, K.IN_WALL_FACE_GOLD
    g.fill(x1, y1, x2, y2, 0, K.IN_DIAMOND_TILE)
    g.fill(x1 - 1, y1 - 3, x2 + 1, y1 - 3, 0, top)
    g.fill(x1, y1 - 2, x2, y1 - 1, 0, face)
    for y in range(y1 - 2, y2 + 2):
        g.set(x1 - 1, y, 0, top)
        g.set(x2 + 1, y, 0, top)
    g.fill(x1 - 1, y2 + 1, x2 + 1, y2 + 1, 0, top)
    g.set(door_x, y2 + 1, 0, K.IN_DIAMOND_TILE)
    g.column(*VAULT_CHAIR, 3, CHAIR_WOOD)


def mayor_pages():
    first = S.narrate([
        "A man in scarlet, wearing the most hat you have ever seen,",
        "standing in front of an enormous door and reading to it from",
        "a long roll of paper."])
    first += S.say("The Mayor", [
        "...AND WHEREAS the",
        "Corporation of Great Dunnage, being",
        "in Council assembled, and mindful -"])
    first += S.narrate([
        "He sees you, and stops, and rolls a very small amount of the",
        "paper back up."])
    first += S.say("The Mayor", [
        "Gristwood. Mayor.",
        "Forgive me. I'm practising the",
        "preamble, for the Opening."])
    first += S.narrate(["You ask what is being opened."])
    first += S.say("The Mayor", [
        "The Counting House!",
        "Sealed in 1788, when the key was lost.",
        "We've run the town on a memorandum."])
    first += S.say("The Mayor", [
        "It is to be opened",
        "formally, by a licensed person, with",
        "the preamble read in full."])
    first += S.narrate(["You ask when."])
    first += S.say("The Mayor", [
        "When there is a",
        "licensed person. The licence is a form.",
        "Nobody has ever filled it in."])
    first += S.say("The Mayor", [
        "But the preamble is",
        "ready. It takes forty minutes. I'm",
        "down to thirty-eight."])
    later = S.say("The Mayor", [
        "...AND WHEREAS -",
        "Oh, hello again. Thirty-seven and a",
        "half."])
    return _pair(first, later)


def door_pages():
    """The Door. With Nix in the party it is a reaction shot, not NIX-2."""
    cmds = S.narrate([
        "The door of the Counting House, which is most of the",
        "Counting House: bronze, a good deal taller than you, with a",
        "lock in the middle of it the size of a cartwheel."])
    cmds += S.narrate([
        "It has not been opened since 1788. Everybody who comes in",
        "looks at it for a while, and then at the Mayor."])
    nix = S.narrate([
        "Nix looks at the Door for rather longer than anybody looks",
        "at a door, and then puts both hands in both pockets, on",
        "purpose."])
    return cmds + R.if_then(R.condition_actor_in_party(db.NIX), nix)


def memorandum_pages():
    return S.narrate([
        "A memorandum in a frame, in a clerk's hand, dated 1788:"]) + \
        S.narrate([
            "THAT, the Counting House being sealed, the accounts of the",
            "Corporation be taken as read;",
            "and THAT the Corporation be assumed to have enough."]) + \
        S.narrate(["Carried unanimously."])


def clerk_pages():
    first = S.say("Town Clerk", [
        "Form L, sir. An",
        "Application by a Licensed Person to",
        "Open the Counting House."])
    first += S.say("Town Clerk", [
        "To be completed by",
        "the licensed person, and countersigned",
        "by a licensed person."])
    first += S.narrate(["You ask how many licensed persons there are."])
    first += S.say("Town Clerk", [
        "None, sir. A",
        "licence is issued on completion of",
        "Form L."])
    later = S.say("Town Clerk", [
        "Form L, sir. Any",
        "time. We live in hope, and a",
        "memorandum."])
    return _pair(first, later)


def counting_events():
    x1, y1, x2, y2, door_x = COUNTING_ROOM
    evs = [_exit(1, door_x, y2 + 2, MAP_DUNNAGE, COUNTING_DOOR[0],
                 COUNTING_DOOR[1] + 1)]
    mayor = _person(2, "The Mayor", MAYOR,
                    R.image("Gen_People6", 0, direction=8), *mayor_pages())
    mayor["pages"] += q_nix.mayor_pages(mayor["pages"][-1])         # NIX-2
    evs.append(mayor)
    door = R.event(3, "The Door", *THE_DOOR, [R.page(
        door_pages(), img=R.image(*DOOR_IMG, direction=2, pattern=2),
        trigger=0, priority=1, direction_fix=True)])
    door["pages"].append(q_nix.door_page(                            # NIX-2
        door["pages"][0], (MAP_COUNTING_HOUSE, VAULT[4], VAULT[3])))
    evs.append(door)
    evs.append(_thing(4, "The Memorandum", MEMORANDUM, memorandum_pages()))
    clerk = _person(5, "Town Clerk", CLERK,
                    R.image(*S.FACES["Town Clerk"], direction=2), *clerk_pages())
    clerk["pages"].append(q_nix.clerk_page(clerk["pages"][-1]))     # NIX-2
    evs.append(clerk)
    evs += q_nix.vault_events(6, VAULT, VAULT_CHAIR,                 # NIX-2
                              (MAP_COUNTING_HOUSE, *COUNTING_BEFORE_DOOR))
    return evs


# =================================================== the Bonded Warehouse ==
# Goods in bond, in rows, with an aisle between; the wharfinger's desk just
# inside the door, and the wardrobe with bond number one in it, standing by
# itself against the wall.
#               x1 y1  x2  y2 door_x
BONDED_ROOM = (2, 4, 21, 10, 5)
BW, BH = 24, 14
TIBBS = (4, 5)
TIBBS_DESK = [(3, 4), (4, 4)]
WARDROBE = 7                    # its base is on the floor's first row
PIANO = (12, 6)
RACK_ROWS = (6, 9)
RACK_XS = [x for x in range(9, 21) if x != 15]


def bonded_map():
    x1, y1, x2, y2, door_x = BONDED_ROOM
    g = K.interior(BW, BH, x1, y1, x2, y2, door_x=door_x,
                   floor=K.IN_DARK_WOOD, wall_top=K.IN_WALL_TOP_PLANK,
                   wall_face=K.IN_WALL_FACE_PLANK)
    for x, y in TIBBS_DESK:
        g.set(x, y, 2, TABLE_D)
    g.set(*TIBBS_DESK[0], 3, LEDGER)
    g.column(WARDROBE, y1 - 1, 2, CLOSET)
    # Big crates along the north wall, and two racks of goods in bond.
    for x in range(10, 21, 2):
        g.column(x, y1 - 1, 2, LARGE_CRATE)
    goods = [CRATE_A, IN_BARREL, CRATE_B, LARGE_CRATE[1], IN_BARREL,
             CRATE_A, CRATE_B]
    for j, y in enumerate(RACK_ROWS):
        for i, x in enumerate(RACK_XS):
            g.set(x, y, 2, goods[(i + j * 3) % len(goods)])
    g.set(*PIANO, 2, LARGE_CRATE[1])
    m = K.new_map(BW, BH, K.TS_INSIDE, name="The Bonded Warehouse",
                  bgm="Town3", bgm_volume=40, battleback=("Wood1", "Room1"))
    m["data"] = g.data
    m["events"] = [None] + bonded_events()
    return m


def tibbs_pages():
    first = S.narrate([
        "An old man in half-rimmed spectacles and a wharf coat, at a",
        "desk by the door, with a ledger that has every single thing",
        "in the warehouse in it."])
    first += S.say("Mr Tibbs", [
        "Tibbs. Wharfinger.",
        "Goods in bond. Nothing out without",
        "the ticket, and the duty, and me."])
    first += S.narrate(["You ask what is in bond."])
    first += S.say("Mr Tibbs", [
        "Everything, sir.",
        "Brandy, iron, cloth, and a piano from",
        "abroad nobody will pay the duty on."])
    first += S.narrate(["You ask what has been here longest."])
    first += S.say("Mr Tibbs", [
        "A coat.",
        "Bond number one. Eleven years."])
    first += S.say("Mr Tibbs", [
        "Rent comes by post",
        "every quarter, never late. No name.",
        "Just the money, and \"Bond No. 1\"."])
    first += S.narrate(["You ask whose coat it is."])
    first += S.say("Mr Tibbs", [
        "Never asked, sir.",
        "Not my place. It's in bond. It's",
        "safe. That's all a thing wants."])
    later = S.say("Mr Tibbs", [
        "Nothing out without",
        "the ticket, sir. Not even the coat."])
    return _pair(first, later)


def wardrobe_pages():
    return S.narrate([
        "A tall wardrobe, by itself against the wall, with a luggage",
        "ticket tied to the handle:"]) + S.narrate([
        "BOND No. 1. ONE COAT. HELD.",
        "Rent paid to date."]) + S.narrate([
        "It is locked. It is the only thing in the warehouse that is."])


def bond_book_pages():
    return S.narrate([
        "The Bond Book. Every entry has a name, a date, a description",
        "and a duty - except the first, which has a date, and the",
        "word \"coat\"."])


def piano_pages():
    return S.narrate([
        "A crate stencilled FRAGILE and THIS WAY UP, the wrong way",
        "up. There is a piano in it. The duty on it is more than the",
        "piano."])


def bonded_events():
    x1, y1, x2, y2, door_x = BONDED_ROOM
    evs = [_exit(1, door_x, y2 + 2, MAP_DUNNAGE, WAREHOUSE_DOOR[0],
                 WAREHOUSE_DOOR[1] + 1)]
    tibbs = _person(2, "Mr Tibbs", TIBBS,
                    R.image("Gen_People6", 2, direction=2), *tibbs_pages())
    tibbs["pages"] += q_nix.tibbs_pages(tibbs["pages"][-1])         # NIX-1
    evs.append(tibbs)
    wardrobe = _thing(3, "Bond No. 1", (WARDROBE, y1), wardrobe_pages())
    wardrobe["pages"].append(q_nix.wardrobe_page(wardrobe["pages"][0]))
    evs.append(wardrobe)
    book = _thing(4, "The Bond Book", TIBBS_DESK[0], bond_book_pages())
    book["pages"].append(q_nix.bond_book_page(book["pages"][0]))
    evs.append(book)
    evs.append(_thing(5, "The Piano", PIANO, piano_pages()))
    return evs


# ================================================================ the Bell ==
# The inn. The bar in the west end, with the bell on it; the judges' table
# facing the little stage in the east end, where Mr Tweddle is practising;
# the Contest's poster on the north wall; and two tables for everybody else.
#            x1 y1  x2  y2 door_x
BELL_ROOM = (2, 4, 19, 10, 10)
LW, LH = 22, 14
DEWHIRST = (7, 5)
THE_BELL = (6, 5)
POSTER = (8, 3)
# The judges' table is a column across from the stage, where Mike moved it
# (October 2026), and they sit along its west side facing the stage.
HARBOTTLE = (13, 7)
AMBLER = (13, 6)
QUAYLE = (13, 8)
TWEDDLE = (16, 6)
BELL_STAIRS = 10                    # the flight's west column


def bell_map():
    """Drawn by hand in the editor and kept by `handdrawn.py` (Mike, October
    2026), from the generated inn: the bar and its two cabinets, the bell on
    the counter, the poster, the stage on its rug, the judges' table across
    from it, and the stairs up through the north wall ("You go up"). Only
    the events are built here."""
    data = HD.load(MAP_BELL, LW, LH, K.TS_INSIDE)
    m = K.new_map(LW, LH, K.TS_INSIDE, name="The Bell", bgm="Town5",
                  battleback=("Wood1", "Room1"))
    m["data"] = data
    m["events"] = [None] + bell_events()
    return m


PRICE = 15


def dewhirst_pages():
    def rooms(lines):
        stay = [R.lose_gold(PRICE), R.fadeout_screen(), R.play_me("Inn1"),
                R.recover_all(), R.wait(90), R.fadein_screen()]
        stay += S.narrate([
            "You go up. Somebody downstairs is doing a curlew, and it is",
            "so good that you do not mind."])
        stay += S.narrate([
            "In the morning everybody is whole, and warm, and rested.",
            "The panel has marked breakfast. Breakfast got a seven."])
        stay += [R.call_common_event(db.CE_MORNING)]               # SPA-3: is it spring yet
        cmds = S.say("Mrs Dewhirst", lines)
        cmds += R.choice_block(
            ["Take a room (%dcr)" % PRICE, "Not just now"],
            [R.if_then(R.condition_script("$gameParty.gold() >= %d" % PRICE),
                       stay,
                       S.say("Mrs Dewhirst", [
                           "Fifteen crowns, love.",
                           "The panel's very strict."]))],
            cancel=None)
        return cmds

    first = S.say("Mrs Dewhirst", [
        "Welcome to the Bell!",
        "A room's fifteen crowns, and you'll be",
        "judged at breakfast."])
    first += S.narrate(["You ask what she means."])
    first += rooms([
        "The panel eat here.",
        "They can't help it. They mark the",
        "soup. Will you stop?"])
    later = rooms([
        "Fifteen crowns, love.",
        "Will you stop?"])
    return _pair(first, later)


def harbottle_pages():
    first = S.narrate([
        "A formidable woman in gold lace, at the judges' table, with",
        "a pencil, a score card, and nothing yet to score."])
    first += S.say("Mrs Harbottle", [
        "Harbottle. I chair",
        "the panel for the Contest at the Sign",
        "of the Bell. We are practising."])
    first += S.narrate(["You ask what they practise on, between contests."])
    first += S.say("Mrs Harbottle", [
        "Everything. The",
        "fire was a six. The door was a four; it",
        "creaks in the wrong key."])
    first += S.say("Mrs Harbottle", [
        "Mr Ambler gives",
        "everything a nine. Mr Ambler cannot",
        "hear. We have never had the heart."])
    first += S.narrate(["You ask whether that is fair."])
    first += S.say("Mrs Harbottle", [
        "It averages out.",
        "Miss Quayle gives everything a two."])
    later = S.say("Mrs Harbottle", [
        "Your entrance was a",
        "five. Your second entrance, a five."])
    return _pair(first, later)


def ambler_pages():
    first = S.say("Mr Ambler", ["Nine!"])
    first += S.narrate(["You have not done anything yet."])
    first += S.say("Mr Ambler", ["What?"])
    first += S.narrate(["You say that you have not done anything yet."])
    first += S.say("Mr Ambler", ["Nine!"])
    later = S.say("Mr Ambler", ["Beautiful. Nine."])
    return _pair(first, later)


def quayle_pages():
    first = S.say("Miss Quayle", ["Two."])
    first += S.narrate(["She does not look up."])
    first += S.say("Miss Quayle", [
        "It isn't personal.",
        "Everything is a two. The birdcalls",
        "were a two."])
    first += S.narrate([
        "She says it the way people say something they have not",
        "quite managed to believe."])
    later = S.say("Miss Quayle", ["Still two."])
    return _pair(first, later)


def tweddle_pages():
    first = S.narrate([
        "A small man in green on the little stage, practising. He",
        "puts two fingers to his mouth, and a nightingale comes out."])
    first += S.narrate([
        "It is not like a nightingale. It is a nightingale. At the",
        "judges' table, a pencil goes down."])
    first += S.say("Mr Tweddle", [
        "Tweddle. Birdcalls.",
        "I've been practising since Easter."])
    first += S.say("Mr Tweddle", [
        "I do a nightingale,",
        "a curlew, and a thrush that's lost its",
        "keys. The thrush goes down very well."])
    later = S.narrate([
        "A blackbird, and then, for no reason, an owl. The room goes",
        "quiet for both of them."])
    return _pair(first, later)


def poster_pages():
    """The Contest's poster. With Piper in the party it is a reaction shot,
    not PIP-3: she reads the categories and does not enter."""
    cmds = S.narrate([
        "THE CONTEST AT THE SIGN OF THE BELL. Open to all.",
        "Categories:"])
    cmds += S.narrate([
        "Ballad (Sad). Ballad (Not Sad). Ballad (Other).",
        "Instrumental (Wind). Instrumental (Other Wind).",
        "Recitation, Comic. Recitation, Not Comic But Funny.",
        "Birdsong (Open)."])
    cmds += S.narrate([
        "Entries to the bar. The decision of the panel is final, and",
        "has been explained to Mr Ambler."])
    piper = S.narrate(["Piper reads the categories twice."])
    piper += S.say("Piper", [
        "You can't defend",
        "half of these."])
    piper += S.narrate(["Then, more quietly, to nobody:"])
    piper += S.say("Piper", ["...Ballad (Not Sad)."])
    piper += S.narrate([
        "She writes something small in the back of her book, and does",
        "not show anybody."])
    return cmds + R.if_then(R.condition_actor_in_party(db.PIPER), piper)


def bell_pages():
    return S.narrate([
        "THE BELL. A small brass bell on the bar, for service, and",
        "the inn is named after it. The Bell Foundry next door casts",
        "bells the size of a cart. This is the one the landlady will",
        "have in the house."])


def bell_events():
    x1, y1, x2, y2, door_x = BELL_ROOM
    evs = [_exit(1, door_x, y2 + 2, MAP_DUNNAGE, BELL_DOOR[0],
                 BELL_DOOR[1] + 1)]
    dewhirst = _person(2, "Mrs Dewhirst", DEWHIRST,
                       R.image(*S.FACES["Mrs Dewhirst"], direction=2),
                       *dewhirst_pages())
    dewhirst["pages"].append(q_roland.dewhirst_page(dewhirst["pages"][-1]))  # ROL-1
    dewhirst["pages"].append(q_roland.dewhirst_after(dewhirst["pages"][1]))  # ROL-5
    dewhirst["pages"].append(q_roland.dewhirst_late(dewhirst["pages"][1]))   # P4b
    evs.append(dewhirst)
    harbottle = _person(3, "Mrs Harbottle", HARBOTTLE,
                        R.image("Gen_People6", 3, direction=6),
                        *harbottle_pages())
    harbottle["pages"] += q_piper.harbottle_pages(harbottle["pages"][-1])  # PIP-3
    evs.append(harbottle)
    evs.append(_person(4, "Mr Ambler", AMBLER,
                       R.image(*S.FACES["Mr Ambler"], direction=6), *ambler_pages()))
    quayle = _person(5, "Miss Quayle", QUAYLE,
                     R.image(*S.FACES["Miss Quayle"], direction=6), *quayle_pages())
    quayle["pages"].append(q_piper.quayle_page(quayle["pages"][-1]))  # PIP-3
    evs.append(quayle)
    tweddle = _person(6, "Mr Tweddle", TWEDDLE,
                      R.image(*S.FACES["Mr Tweddle"], direction=2), *tweddle_pages())
    tweddle["pages"].append(q_piper.tweddle_page(tweddle["pages"][-1]))  # PIP-3
    evs.append(tweddle)
    poster = _thing(7, "The Contest", POSTER, poster_pages())
    poster["pages"].append(q_piper.poster_page(poster["pages"][0]))   # PIP-3
    evs.append(poster)
    evs.append(_thing(8, "The Bell", THE_BELL, bell_pages()))
    evs += q_piper.rival_events()                                     # PIP-3
    evs += q_roland.meeting_events()                                  # ROL-1
    evs.append(q_roland.understudy_event(len(evs) + 1))               # ROL-5
    evs.append(q_roland.snug_card_event(len(evs) + 1))                # ROL-2
    # The top tread of each column: the rooms are Mrs Dewhirst's to give.
    stairs = S.narrate([
        "The stairs up to the rooms. A sign on the newel post",
        "says RESIDENTS, and under it, smaller, AND JUDGES."])
    for i in range(2):
        evs.append(R.event(len(evs) + 1, "The Stairs Up", BELL_STAIRS + i,
                           y1, [R.page(stairs, img=R.image(""), trigger=1,
                                       priority=1, direction_fix=True)]))
    return evs


# ================================================================ the door ==
def world_doors(base_id, cells):
    """The real door into Great Dunnage, on the world map.

    `cells` is the two squares `worldmap.json` put placeholders on for this
    site - the lower half of the `Fortress City` stamp - handed in by
    `journey.world_map`. Player-touch and below characters, the world map's
    idiom for a place you walk into. **No refusal here**: six companions
    have business in this town, and a refusal at the gate would lock all of
    it. Nix's is on the Bonded Warehouse's own door."""
    evs = []
    for i, (x, y) in enumerate(sorted(cells)):
        arrive = S.narrate([
            "A walled town of brick and stone, with smoke going up over",
            "the wall from somewhere inside it, and a gate in the middle",
            "of its south side. A board by the gate says CORPORATE TOWN."])
        arrive += R.choice_block(
            ["Go in at the gate", "Press on"],
            [[R.transfer(MAP_DUNNAGE, *ARRIVE, 8, 0)],
             S.narrate(["You press on. Behind you, somewhere inside the",
                        "wall, several things are being hit with hammers."])])
        evs.append(R.event(base_id + i, SITE, x, y, [R.page(
            arrive, img=R.image(""), trigger=1, priority=0, through=True)]))
    return evs


def build():
    R.save_map(MAP_DUNNAGE, town_map())
    R.save_map(MAP_SMITHS_HALL, smiths_map())
    R.save_map(MAP_COUNTING_HOUSE, counting_map())
    R.save_map(MAP_BONDED, bonded_map())
    R.save_map(MAP_BELL, bell_map())
