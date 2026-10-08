"""Maps 50-51: Little Gore and Sump, two hamlets of one street each.

`../SITES.md` step 13. The source is `../COMPANIONS.md` L8 - "two hamlets, one
map each, both essentially one street and a reason" - and the three quests it
serves: ALD-1, whose letter was always going to Little Gore; MER-5, the well
at Sump; and PIP-4, whose eleven interviews either can host. This module
builds the places and the people and **not the quests**, which are appended
later as pages of their own. Nothing here spends one.

* **Both world-map doors are claimed by name**, `journey.world_map`'s
  mechanism, as a cluster: `SITES` maps each name to its builder, the way
  `hithermost.py` does. Both stamps were shot before this was written. Little
  Gore's is one cell of `House (Village)`, a wooden hut on a rocky knoll in a
  forest clearing with a sandy road ending at its door. Sump's is one cell of
  `House (Desert)`, a flat-roofed house with a palm and **a little pool of its
  own**, on a sandy spit with the sea on three sides - for a hamlet that has
  had no water since 1794. The pool is the joke rather than a problem: it is
  the sea, come in under the sand, and somebody has put a sign in it.
* **Little Gore's reason is a wedding nine years ago.** Mrs Vane - `Mrs
  Vane` in the speaker box, because the game already has a Hester at
  Restwell - married Tom from Fenmarch, and the whole hamlet walked the four
  miles over for it in the rain. The notice board still has the banns on it,
  and under them a card that says INVITATIONS TO FOLLOW. That is ALD-1's
  set-up and not its payoff: the letter, the mantelpiece and Aldric are all
  the quest's, so **there is no reaction shot with Aldric in the party** - he
  cannot stand four miles from home, carrying the letter, and have nothing
  happen, and anything that did happen would be the quest.
* **Coldbarrow has a white pin at Little Gore** - one knight of the Order in
  the field there - so she is here: Dame Winifred Cope, who has been exactly
  where the Chapter thinks she is for eleven years and finds it very
  restful. She is Coldbarrow's system working, and says nothing of Aldric.
* **Sump's reason is the wasps.** The well has a nest in it, and the parish
  cannot say whose job that is: a wasp is the Pound's, a nest is Buildings',
  and a well is Water's, and the Water Committee was wound up in 1794 on the
  grounds that there wasn't any. Everybody has a headache and nobody sleeps,
  and it is a curse. **Nobody in Sump joins those two facts up and neither
  does the game**; the minutes put them one line apart and leave it there.
  Joining them is Merribell's, in nine seconds, and that is MER-5.
* **Merribell in the party is a reaction shot and not the quest.** She looks
  at the Parish Clerk for about nine seconds and opens her mouth, and he asks
  her to speak through the chair. There is no chair. He is the chair.
* **PIP-4 is hosted by Little Gore** (`q_piper`, E12): its commission is a
  card on the back of the fingerpost, and its eleven interviews are pages on
  people in both hamlets and at Fenmarch, appended last on each.
* **One trope, the cursed village, on Sump's sign. No blush**: both places are
  warm, and neither has anybody in it for a double meaning to land on.
"""
import mapkit as K
import rmmzdata as R

import db
import story as S
import q_aldric
import q_hob
import q_merribell
import q_piper
from places import (MAP_WORLD, MAP_LITTLE_GORE, MAP_SUMP,
                    LITTLE_GORE_STEP, SUMP_STEP)

# The names `worldmap.json`'s door events carry for these two sites.
LITTLE_GORE = "Little Gore"
SUMP = "Sump"

# Sump's ground is Outside_A2's `Sand` family, and `Water D (Sand)` on A1 is
# the water that goes with it. **The `mapkit` names are the wrong way round
# here**: `K.SOIL` is the sheet's `Sand` and `K.SAND` is its `Dirt`, which is
# what the street is - `Road (Sand)` is grey cobbles, and that is a town.
SAND = K.SOIL
SAND_GRASS = K.A(33)                # `Grass (Sand)`, round the pool
SAND_ROAD = K.SAND                  # `Dirt`
SEA = K.A(10)
CACTUS = K.sf_tile("Outside_B", "Cactus")


# ============================================================= Little Gore ==
GW, GH = 24, 18
LANE_Y = 11                         # the street: rows 11 and 12
ROAD_X = 11                         # the road out: columns 11 and 12
VANES = (3, 4, 7, 6)                # the Vanes'
COPES = (12, 5, 5, 5)               # the Order's knight in the field
EAST = (18, 4, 4, 6)                # a third house, and the end of the street
VANES_DOOR = (5, VANES[1] + VANES[3] - 1)
COPES_DOOR = (14, COPES[1] + COPES[3] - 1)
EAST_DOOR = (19, EAST[1] + EAST[3] - 1)

HESTER = (8, 10)                    # in her front garden
COPE = (16, 10)                     # by her own door
# The three Vanes on the green, playing weddings: the bride, the groom and
# everybody else.
BESS, ALFIE, NELL = (4, 14), (6, 14), (5, 15)
BANNS = (16, 13)                    # the notice board, which blocks its cell
FINGERPOST = (13, 15)               # beside the road, pointing down it
WELL = (19, 14)
ARRIVE_G = (ROAD_X, GH - 2)


def gore_map():
    w, h = GW, GH
    g = K.Canvas(w, h)
    g.fill(0, 0, w - 1, h - 1, 0, K.GRASS)
    g.fill(2, LANE_Y, w - 3, LANE_Y + 1, 0, K.PATH)
    g.fill(ROAD_X, LANE_Y, ROAD_X + 1, h - 1, 0, K.PATH)

    g.building(*VANES, wall=K.WALL_PLANK_LIGHT, roof=K.ROOF_BROWN)
    g.building(*COPES, wall=K.WALL_TIMBER, roof=K.ROOF_GREEN)
    g.building(*EAST, wall=K.WALL_PLANK, roof=K.ROOF_BROWN)
    g.autotile(0)

    for x, y in (VANES_DOOR, COPES_DOOR, EAST_DOOR):
        g.column(x, y - 1, 3, K.DOOR_SHUT)
    g.set(VANES_DOOR[0] + 2, VANES_DOOR[1], 3, K.WINDOW)
    g.set(VANES_DOOR[0] + 3, VANES_DOOR[1], 3, K.WINDOW)
    g.set(COPES_DOOR[0] + 1, COPES_DOOR[1], 3, K.WINDOW)
    g.set(EAST_DOOR[0] + 1, EAST_DOOR[1], 3, K.WINDOW)
    g.set(VANES[0] + 5, VANES[1], 2, K.STOVEPIPE)
    g.set(EAST[0] + 1, EAST[1], 2, K.STOVEPIPE)

    # The Vanes' front garden, which is where Mrs Vane is.
    g.scatter([(3, 10), (4, 10), (6, 10), (7, 10), (9, 10)], 3, K.FLOWERS2)
    g.scatter([(12, 10), (20, 10)], 3, K.FLOWERS)
    g.scatter([(COPES_DOOR[0] - 1, COPES_DOOR[1] + 1)], 3, K.BARREL)

    # The green, south of the street.
    g.set(*WELL, 3, K.TUB)                              # `Well`, and it is one
    g.set(*BANNS, 3, K.FENCE_PANEL)                     # `Sign B`, a board
    g.set(*FINGERPOST, 3, K.SIGNPOST)
    g.scatter([(3, 13), (8, 15), (18, 13), (20, 15)], 3, K.FLOWERS3)
    g.scatter([(9, 13), (15, 15)], 3, K.BUSH)
    g.set(20, 13, 3, K.LOGS)

    # The wood all round, with a gap at the bottom for the road.
    for x in range(0, w, 2):
        g.blit(x, 0, 3, K.TREE)
        if not (ROAD_X - 1 <= x <= ROAD_X + 2):
            g.blit(x, h - 2, 3, K.TREE)
    for y in range(2, h - 2, 2):
        g.blit(0, y, 3, K.TREE)
        g.blit(w - 2, y, 3, K.TREE)

    m = K.new_map(w, h, K.TS_OUTSIDE, name="Little Gore", bgm="Town6")
    m["data"] = g.data
    m["events"] = [None] + q_aldric.with_follower(gore_events(), MAP_LITTLE_GORE)  # ALD-5
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


def vane_pages():
    first = S.narrate([
        "A woman in the front garden of the nearest house is",
        "weeding round the flowers, and stands up, and wipes her",
        "hands, and is plainly delighted to see anybody."])
    first += S.say("Mrs Vane", [
        "Hello! You're a long way from",
        "anywhere. Well - you're four miles",
        "from Fenmarch, which round here is",
        "the same thing."])
    first += S.narrate([
        "You say that you are the Chosen One. Number forty-eight."])
    first += S.say("Mrs Vane", [
        "How lovely. Hester Vane. I've",
        "been to Fenmarch, and that's the",
        "furthest. I was married there,",
        "nine years ago this summer."])
    first += S.say("Mrs Vane", [
        "The whole of Little Gore walked",
        "over for it. All eleven of us, in",
        "our best, and it rained the whole",
        "way, and nobody minded at all."])
    first += S.say("Mrs Vane", [
        "That's our house. The three on the",
        "green are ours as well. Mind them;",
        "they'll marry you if you stand",
        "still."])
    later = S.say("Mrs Vane", [
        "Tom's in the gardens at Fenmarch.",
        "He walks it every day - four miles",
        "there and four back - and he says",
        "it's the best part."])
    return _pair(first, later)


def cope_pages():
    first = S.narrate([
        "A knight in a good plain helmet, standing outside her own",
        "front door as if it were a post."])
    first += S.say("Dame Winifred", [
        "Dame Winifred Cope, of the",
        "Order of the Errant. The Chapter's",
        "knight in the field at Little Gore."])
    first += S.say("Dame Winifred", [
        "Eleven years. There's a pin",
        "in me at Coldbarrow. Just the one."])
    first += S.narrate(["You ask what she does."])
    first += S.say("Dame Winifred", [
        "I'm here. That's the whole",
        "of it. Somebody has to be where the",
        "pin is, or what's the map for?"])
    first += S.say("Dame Winifred", [
        "I write every quarter:",
        "NOTHING TO REPORT. They write back:",
        "VERY GOOD. It's the nicest",
        "correspondence I've ever had."])
    later = S.say("Dame Winifred", [
        "Still here. Still nothing",
        "to report. Lovely."])
    return _pair(first, later)


def gore_events():
    evs = []
    # 1-2: the road out, both cells of it. Below characters: an exit tile at
    # "same as characters" is one the player walks straight over.
    for i in range(2):
        evs.append(S.exit_tile(i + 1, "The Road Out", ROAD_X + i, GH - 1,
                               MAP_WORLD, *LITTLE_GORE_STEP))

    evs.append(_person(3, "Hester Vane", HESTER,
                       R.image("Gen_People4", 5, direction=2), *vane_pages()))
    evs[-1]["pages"] += q_aldric.vane_pages(evs[-1]["pages"][-1])  # ALD-1
    evs[-1]["pages"] += q_piper.interview_pages("vane", evs[-1]["pages"])  # PIP-4
    evs.append(q_hob.owned("winifred", _person(                    # HOB-1
        4, "Dame Winifred Cope", COPE,
        R.image(*S.FACES["Dame Winifred"], direction=2), *cope_pages())))
    evs[-1]["pages"] += q_piper.interview_pages("winifred", evs[-1]["pages"])  # PIP-4

    # 5-7: the three Vanes on the green, playing weddings; the narration says
    # how small they are. Nell was the spiky-haired boy, People1:0, under a
    # line that says "She is, too", until AUDIT.md item 4, and Bess an adult
    # in a headscarf; item 1 drew all three, faces and sprites, as children.
    bess = S.narrate([
        "A small girl with a daisy chain on her head, standing",
        "very straight."])
    bess += S.say("Bess", ["I'm Mum. I mean I'm the bride.",
                           "It's the same thing."])
    alfie = S.narrate([
        "A smaller boy with his hair wetted flat, standing next to",
        "the bride and looking pleased."])
    alfie += S.say("Alfie", ["I'm Dad. I have to stand here and",
                             "look pleased. Dad says that's the",
                             "whole job."])
    nell = S.say("Nell", ["I'm everybody else."])
    nell += S.narrate([
        "She is, too. She has been the whole of Little Gore, half",
        "of Fenmarch, the vicar, the rain and the cake."])
    for eid, name, xy, (sheet, idx), cmds, facing in [
            (5, "Bess", BESS, S.FACES["Bess"], bess, 6),
            (6, "Alfie", ALFIE, S.FACES["Alfie"], alfie, 4),
            (7, "Nell", NELL, S.FACES["Nell"], nell, 8)]:
        evs.append(S.npc(eid, name, *xy, cmds, sheet, idx, direction=facing))
        evs[-1]["pages"] += q_piper.interview_pages(name.lower(), evs[-1]["pages"])  # PIP-4

    page = dict(img=R.image(""), trigger=0, priority=1, direction_fix=True)

    # 8: the notice board, which is ALD-1's set-up and none of its payoff.
    banns = S.narrate([
        "A notice board on a post. One notice on it is older than",
        "all the others and has been very carefully kept out of",
        "the rain."])
    banns += S.narrate([
        "BANNS OF MARRIAGE",
        "between HESTER PLUMB, of this parish, and THOMAS VANE,",
        "of the parish of Fenmarch. Third time of asking."])
    banns += S.narrate([
        "Pinned under it, in another hand, on a card gone brown at",
        "the edges:",
        "",
        "        INVITATIONS TO FOLLOW."])
    banns += S.narrate([
        "Round the both of them, newer, three notices of births,",
        "a year or two apart, each with a drawing of a very round",
        "baby in the corner."])
    evs.append(R.event(8, "The Banns", *BANNS, [R.page(banns, **page)]))
    evs[-1]["pages"] += q_aldric.banns_pages(evs[-1]["pages"][0])  # ALD-1

    # 9: the fingerpost, which is Little Gore's whole geography.
    post = S.narrate([
        "A fingerpost. One arm points at the houses and says",
        "LITTLE GORE. The other points back down the road:",
        "",
        "        FENMARCH  4 MILES"])
    post += S.narrate([
        "Somebody has carved a great many initials into the post,",
        "and a heart round two of them, nine years deep."])
    evs.append(R.event(9, "The Fingerpost", *FINGERPOST,
                       [R.page(post, **page)]))
    evs[-1]["pages"] += q_piper.fingerpost_pages(evs[-1]["pages"][0])  # PIP-4
    return evs


# ==================================================================== Sump ==
SW_, SH_ = 22, 16
STREET_Y = 10                       # the street: rows 10 and 11
ROAD_S = 10                         # the road out: columns 10 and 11
WEST = (4, 4, 4, 5)
HUT = (9, 5, 4, 4)                  # the parish hut
EASTH = (14, 4, 4, 5)
WEST_DOOR = (5, WEST[1] + WEST[3] - 1)
HUT_DOOR = (10, HUT[1] + HUT[3] - 1)
EAST_DOOR_S = (15, EASTH[1] + EASTH[3] - 1)

THURLE = (12, 9)                    # in front of the parish hut
BOARD = (13, 9)                     # the minutes, as posted
GAMMAGE = (7, 9)
PARDEW = (17, 9)
WELL_S = (14, 13)
POOL = (5, 13)                      # 3x2 of the sea, come in under the sand
TOWN_SIGN = (12, 14)
ARRIVE_S = (ROAD_S, SH_ - 2)


def sump_map():
    w, h = SW_, SH_
    g = K.Canvas(w, h)
    # The spit: sea on three sides, and the road out to the south.
    g.fill(0, 0, w - 1, h - 1, 0, SEA)
    g.fill(3, 3, w - 4, h - 1, 0, SAND)
    g.fill(2, 10, 2, h - 1, 0, SAND)
    g.fill(w - 3, 12, w - 3, h - 1, 0, SAND)

    g.fill(3, STREET_Y, w - 4, STREET_Y + 1, 0, SAND_ROAD)
    g.fill(ROAD_S, STREET_Y, ROAD_S + 1, h - 1, 0, SAND_ROAD)
    # A little green round the pool, which is what it looks like from the road.
    x0, y0 = POOL
    g.fill(x0 - 1, y0 - 1, x0 + 3, y0 + 2, 0, SAND_GRASS)
    for cx, cy in [(x0 - 1, y0 - 1), (x0 + 3, y0 - 1),
                   (x0 - 1, y0 + 2), (x0 + 3, y0 + 2)]:
        g.set(cx, cy, 0, SAND)
    g.fill(POOL[0], POOL[1], POOL[0] + 2, POOL[1] + 1, 0, SEA)

    g.building(*WEST, wall=K.WALL_SANDBRICK, roof=K.ROOF_GOLD)
    g.building(*HUT, wall=K.WALL_SANDBRICK, roof=K.ROOF_GOLD)
    g.building(*EASTH, wall=K.WALL_SANDBRICK, roof=K.ROOF_GOLD)
    g.autotile(0)

    for x, y in (WEST_DOOR, HUT_DOOR, EAST_DOOR_S):
        g.column(x, y - 1, 3, K.DOOR_SHUT)
    g.set(WEST_DOOR[0] + 1, WEST_DOOR[1], 3, K.WINDOW)
    g.set(HUT_DOOR[0] + 1, HUT_DOOR[1], 3, K.WINDOW)
    g.set(EAST_DOOR_S[0] + 1, EAST_DOOR_S[1], 3, K.WINDOW)

    g.set(*WELL_S, 3, K.TUB)                            # `Well`, and it is one
    g.set(*BOARD, 3, K.FENCE_PANEL)                     # `Sign B`, a board
    g.set(*TOWN_SIGN, 3, K.SIGNPOST)

    g.blit(POOL[0] - 1, POOL[1] - 1, 3, K.PALM)
    g.blit(3, 4, 3, K.PALM)
    g.blit(18, 4, 3, K.PALM)
    g.blit(17, 12, 3, K.PALM)
    g.scatter([(8, 13), (16, 14), (4, 9), (18, 9)], 3, CACTUS)
    g.scatter([(9, 9), (14, 9)], 3, K.POT)

    m = K.new_map(w, h, K.TS_OUTSIDE, name="Sump", bgm="Town8")
    m["bgs"] = {"name": "Sea", "pan": 0, "pitch": 100, "volume": 40}
    m["autoplayBgs"] = True
    m["data"] = g.data
    m["events"] = [None] + sump_events()
    return m


def thurle_pages():
    first = S.narrate([
        "A man in a wide hat in front of the parish hut, with a",
        "ledger under one arm, pressing two fingers very hard to",
        "the side of his head."])
    first += S.say("Mr Thurle", [
        "Absalom Thurle. Parish Clerk.",
        "If it's about the curse, it's on",
        "the agenda. If it's about the",
        "wasps, it is not."])
    first += S.narrate(["You ask why not."])
    first += S.say("Mr Thurle", [
        "Because nobody can say whose they",
        "are. A wasp is an animal, which is",
        "the Pound. A nest is a structure,",
        "which is Buildings."])
    first += S.say("Mr Thurle", [
        "And a well is Water, and the Water",
        "Committee was wound up in 1794, on",
        "the grounds that there wasn't any."])
    first += S.narrate([
        "He says it without the slightest sign of having heard it."])
    first += S.say("Mr Thurle", [
        "Forgive me. I've a head like a",
        "drum. We all have. It's the curse.",
        "Nobody in Sump has had a decent",
        "night's sleep in six generations."])

    # Merribell in the party is a reaction shot, not MER-5.
    merri = S.narrate([
        "Merribell has been looking at him for about nine seconds.",
        "She opens her mouth."])
    merri += S.say("Mr Thurle", ["Through the chair, please."])
    merri += S.narrate([
        "There is no chair. He is the chair. Merribell closes her",
        "mouth again, with some difficulty, and writes something",
        "on the back of her hand."])
    first += R.if_then(R.condition_actor_in_party(db.MERRI), merri)

    later = S.say("Mr Thurle", [
        "Item one, the curse. Item two, the",
        "wasps: deferred. There is never an",
        "item three. There's never time."])
    return _pair(first, later)


def gammage_pages():
    first = S.narrate([
        "An old man sitting with his back to the wall and his eyes",
        "shut. He is not asleep. He opens one."])
    first += [R.show_balloon(0, 5)]
    first += S.say("Mr Gammage", [
        "Don't. I've been trying to get off",
        "since Tuesday."])
    first += S.say("Mr Gammage", [
        "My father never slept. Nor his.",
        "It's the curse. You get used to it.",
        "You don't, but you say you do."])
    later = [R.show_balloon(0, 10)]
    later += S.narrate([
        "His eyes are shut. He is not asleep, and would like you",
        "to know it."])
    return _pair(first, later)


def pardew_pages():
    first = S.say("Mrs Pardew", [
        "Things used to be better. My gran",
        "said so, and her gran said so. It's",
        "in the minutes."])
    first += S.narrate(["You ask what they used to be better at."])
    first += S.say("Mrs Pardew", [
        "It doesn't say.",
        "That's the worst of it."])
    later = S.say("Mrs Pardew", [
        "Don't talk to me before noon.",
        "Or after.",
        "It isn't you, love. It's the curse."])
    return _pair(first, later)


def sump_events():
    evs = []
    for i in range(2):
        evs.append(S.exit_tile(i + 1, "The Road Out", ROAD_S + i, SH_ - 1,
                               MAP_WORLD, *SUMP_STEP))

    evs.append(_person(3, "Absalom Thurle", THURLE,
                       R.image("Gen_People4", 6, direction=2),
                       *thurle_pages()))
    evs[-1]["pages"] += q_merribell.thurle_pages(evs[-1]["pages"][-1])   # MER-5
    evs.append(_person(4, "Mr Gammage", GAMMAGE,
                       R.image(*S.FACES["Mr Gammage"], direction=2), *gammage_pages()))
    evs[-1]["pages"] += q_merribell.gammage_pages(evs[-1]["pages"][-1])  # MER-5
    evs[-1]["pages"] += q_piper.interview_pages("gammage", evs[-1]["pages"])  # PIP-4
    evs.append(_person(5, "Mrs Pardew", PARDEW,
                       R.image(*S.FACES["Mrs Pardew"], direction=2), *pardew_pages()))
    evs[-1]["pages"] += q_merribell.pardew_pages(evs[-1]["pages"][-1])   # MER-5
    evs[-1]["pages"] += q_piper.interview_pages("pardew", evs[-1]["pages"])  # PIP-4

    page = dict(img=R.image(""), trigger=0, priority=1, direction_fix=True)

    # 6: the well, and the wasps, which no sprite in the box can draw.
    well = S.narrate([
        "The parish well: a good round stone head, no rope and no",
        "bucket."])
    well += S.narrate([
        "A deep, steady hum comes up out of it, like a choir that",
        "has been given one note and is not going to let go of it."])
    well += S.narrate([
        "Something small and striped comes up, looks at you, and",
        "goes back down to report."])
    evs.append(R.event(6, "The Well", *WELL_S, [R.page(well, **page)]))
    evs[-1]["pages"] += q_merribell.well_pages(evs[-1]["pages"][0])  # MER-5

    # 7: the minutes, which put the two facts one line apart and leave them
    # there. Joining them is MER-5's.
    minutes = S.narrate([
        "THE PARISH OF SUMP. Minutes, as posted.",
        "",
        "1794. Item 1: Wasps, in the well. Whose? Deferred."])
    minutes += S.narrate([
        "1794. Item 2: The Water Committee to be wound up, there",
        "being no water. Carried."])
    minutes += S.narrate([
        "1795. Item 1: Wasps. Deferred.",
        "1795. Item 2: A general sense that things used to be",
        "better. Noted. Suspected curse."])
    minutes += S.narrate([
        "And so on, every year, in six different hands. The last",
        "is this year's: WASPS - DEFERRED. It is underlined, and",
        "the pen has gone through the paper."])
    evs.append(R.event(7, "The Minutes", *BOARD, [R.page(minutes, **page)]))
    evs[-1]["pages"] += q_merribell.minutes_pages(evs[-1]["pages"][0])  # MER-5

    # 8: the sign on the road in, and the site's trope.
    sign = S.narrate([
        "A fingerpost, bleached almost white by the sun. One arm",
        "points up the street and says SUMP. The other points at",
        "the sea, and says:",
        "        Cursed 1794.   Please Mind The Wasps."])
    sign += [S.trope()]
    evs.append(R.event(8, "The Sign", *TOWN_SIGN, [R.page(sign, **page)]))
    evs[-1]["pages"] += q_merribell.sign_pages(evs[-1]["pages"][0])  # MER-5

    # 9: the pool the world map shows, which is the sea.
    pool = S.narrate([
        "A pool with a palm tree leaning over it, blue and clear,",
        "which is the first thing anybody sees of Sump."])
    pool += S.narrate([
        "It is salt. It is the sea, which comes in under the sand",
        "at high tide and goes out again at low. Somebody has",
        "stuck a little sign in the middle of it that says NO."])
    evs.append(R.event(9, "The Pool", POOL[0] + 1, POOL[1],
                       [R.page(pool, **page)]))
    return evs


# ================================================================ the doors ==
def _gore_doors(base_id, cells):
    """The real door into Little Gore, on the world map.

    Player-touch and below characters, the world map's idiom for a place you
    walk into."""
    evs = []
    for i, (x, y) in enumerate(sorted(cells)):
        arrive = S.narrate([
            "A clearing in the wood, and a sandy road that ends at a",
            "wooden house on a rocky knoll, with smoke going up from",
            "a few more chimneys somewhere behind it."])
        arrive += R.choice_block(
            ["Go in", "Press on"],
            [[R.transfer(MAP_LITTLE_GORE, *ARRIVE_G, 8, 0)],
             S.narrate(["You press on. Somewhere behind the trees, children",
                        "are singing something with a great many verses."])])
        evs.append(R.event(base_id + i, LITTLE_GORE, x, y, [R.page(
            arrive, img=R.image(""), trigger=1, priority=0, through=True)]))
    return evs


def _sump_doors(base_id, cells):
    """The real door into Sump, on the world map."""
    evs = []
    for i, (x, y) in enumerate(sorted(cells)):
        arrive = S.narrate([
            "A flat-roofed house on a spit of sand, with the sea on",
            "three sides of it, a palm tree, and a little blue pool of",
            "its own. A painted board says SUMP."])
        arrive += R.choice_block(
            ["Go in", "Press on"],
            [[R.transfer(MAP_SUMP, *ARRIVE_S, 8, 0)],
             S.narrate(["You press on. Behind you, somebody shouts WHAT at",
                        "nobody in particular, and then apologises."])])
        evs.append(R.event(base_id + i, SUMP, x, y, [R.page(
            arrive, img=R.image(""), trigger=1, priority=0, through=True)]))
    return evs


# One claim per name the world map carries - `journey.world_map` merges this
# into its `claims` dict. Two names, two entries, one module.
SITES = {
    LITTLE_GORE: _gore_doors,
    SUMP: _sump_doors,
}


def build():
    R.save_map(MAP_LITTLE_GORE, gore_map())
    R.save_map(MAP_SUMP, sump_map())
