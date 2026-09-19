"""Map ids and the handful of coordinates that two maps have to agree on.

`village.py` needs to know where the world map's village tile is, and
`journey.py` needs to know where the village gate is. Putting both here keeps
the two modules from having to import each other.

**Every world-map coordinate in here was re-cut for the 120x120 map** - see
`../WORLDMAP.md`, whose section 3 is the table this file is derived from and
whose section 6 item 6 is why. Most are the old 50x50 coordinate `+ (35,35)`,
which is where the preserved old map sits; the ones that are not are marked,
and there are more of them than "+35" suggests:

  * **Thistlewick, Nether Sopping, Upper Clanging and the Lighthouse** were all
    restamped and re-sited, so their coordinates come from section 3 and not
    from arithmetic. The Lighthouse moved twice and is out on a headland now.
  * **Two `_STEP` tiles changed side.** The step is the tile the player stands
    on coming out of a town, and it is wherever the road is; `run_finish.py`
    gives Thistlewick and Nether Sopping their road spurs to the **north**,
    which is the side the gate comes out on now. A blind `+1` south puts
    Thistlewick's gate in the water.
  * **Every one was checked with `flags & 0x0F == 0` against the finished map**,
    not merely translated - the coast mend, the hand-drawn range and the islet
    drowning all changed terrain that old constants stood on. The four
    signposts read as blocked and are *supposed* to: a `WB_SIGN` tile blocks
    its own cell and is read from beside it, which is this game's idiom and was
    true on the 50x50 too.

Nothing in here is a map any more. The world map is
`build/worldmap/worldmap.json`, produced by `build/worldmap/run_finish.py`;
`journey.world_map` loads it and adds this game's events to it.
"""

MAP_VILLAGE, MAP_HOME, MAP_HALL, MAP_INN = 1, 2, 3, 4
MAP_CHAPEL, MAP_SMITHY, MAP_STORE = 5, 6, 7
MAP_WORLD, MAP_GLOAMWOOD, MAP_GLOAM_DEEP, MAP_TOWER, MAP_SUMMIT = 8, 9, 10, 11, 12

# The south: Nether Sopping and its interiors, then the three optional places
# out in the world.
MAP_SOPPING, MAP_WYVERN, MAP_GUILD = 13, 14, 15
MAP_OUTFIT, MAP_COTTAGE, MAP_LIGHTHOUSE = 16, 17, 18
MAP_PIT, MAP_BARROW = 19, 20

# The region ids the world map's encounter list filters on. Painted onto
# `worldmap.json` by `build/worldmap/finish.paint_regions`, which imports them
# from here, and named in `journey.world_map`'s `encounters=`. Five and six are
# new: a third of the 120x120's climate did not exist on the 50x50, and they are
# pointed at the north's troops until somebody writes snow and desert ones.
REG_SOUTH, REG_NORTH, REG_COAST, REG_CLANG, REG_SNOW, REG_DESERT = 1, 2, 3, 4, 5, 6

# Thistlewick's north gate, and the tile you arrive on when you step out of it.
VILLAGE_GATE = (19, 2)
WORLD_VILLAGE = (60, 79)        # was (24,43): restamped `Town B`, re-sited
WORLD_VILLAGE_STEP = (60, 78)   # was (24,45), two SOUTH; the spur is north now

# The other two places you can walk into from the world map.
WORLD_GLOAMWOOD = (52, 62)      # was (17,27)
WORLD_TOWER = (66, 43)          # was (31,8)

# --------------------------------------------------------------- the south --
# Nether Sopping's own gate, at the top of its one street, and the tiles on the
# world map that lead to it. Everything below here is optional content.
SOPPING_GATE = (20, 2)
WORLD_SOPPING = (71, 84)        # was (36,44): `Town A` on the last land row
WORLD_SOPPING_STEP = (71, 83)   # was (36,45), one SOUTH; the spur is north now

# On its own headland at last - a spit of rock three cells out into the sea,
# with the tower at the tip. It was (41,44) on the 50x50 and (76,79) for one
# build of this map, and it is neither of those: see WORLDMAP.md 6.1.
#
# **And it needed a `_STEP` of its own, which no other curiosity has.** Every
# other exit onto the world map is written "one square south of the door", and
# on a spit that runs east the square south of the door is the sea - so coming
# out of the lighthouse put the party in the water. It is a *headland* now, so
# the way out is back along the spit, westward, on the track.
WORLD_LIGHTHOUSE = (79, 80)
WORLD_LIGHTHOUSE_STEP = (78, 80)
WORLD_PIT = (43, 70)            # was (8,35); the redraw buried it and it was dug out
WORLD_BARROW = (68, 56)         # was (33,21)

# World-map curiosities: things to look at rather than places to go into.
WORLD_STONES = (46, 53)         # was (11,18); the plaque, between the four rocks
WORLD_HERMIT = (75, 65)         # was (40,30); his hut is one row north of it
WORLD_CRAB = (55, 81)           # was (20,46)
WORLD_CAMP = (47, 67)           # was (12,32); Crooke's tent is one column west

# --------------------------------------------------------------- the north --
# Upper Clanging and its interiors, then the two places out on the north-west
# lobe of the world map. `NORTH.md` section 4.3 explains what each of them is
# for; its **coordinates are the 50x50's** and are superseded by the ones here.
MAP_CLANGING, MAP_WORKS, MAP_VALVE = 21, 22, 23
MAP_FORGE, MAP_PARISH = 24, 25
MAP_LONG_FIELD, MAP_CRAG = 26, 27

CLANGING_GATE = (17, 42)        # the foot of the street, where the road leaves
WORLD_CLANGING = (44, 47)       # was (9,12): restamped `World_C/Slum`, same cell
WORLD_CLANGING_STEP = (44, 48)  # was (9,13); still one south, still on the road
WORLD_LONG_FIELD = (47, 50)     # was (12,15)
WORLD_LONG_FIELD_STEP = (46, 50)   # was (11,15)
WORLD_CRAG = (41, 43)           # was (6,8)
WORLD_CRAG_STEP = (41, 44)      # was (6,9)
WORLD_JUNCTION = (49, 54)       # was (14,19); the signpost, blocked, read from beside

# Where the Two Hundred is parked the day she is handed over: plain world
# grass beside the town's door, because the road itself is not airship-
# landable - road tile 3008 already carries 0x0800. See NORTH.md 5.2.
WORLD_AIRSHIP = (45, 48)        # was (10,13)

# ------------------------------------------------ the three air-only places --
# NORTH.md 5.6. Each is a rock in the sea with impassable water all round it,
# so the only way onto any of them is to land on it, and `validate.py` asserts
# on foot that none of them can be reached. An air-only joke that turns out to
# be walkable is a joke nobody will ever notice was one.
#
# Each is laid out around two rules that only bite when an airship is the only
# way in, and which cost an afternoon to find:
#
#  * `Game_Vehicle.isLandOk` refuses to set an airship down on a square that
#    has an event on it, so every rock needs a square with nothing on it or
#    there is no way to arrive; and
#  * `Game_Player.triggerButtonAction` offers the vehicle **before** it offers
#    the event in front of you, so the action button pressed while standing on
#    a landed airship always takes off again. On a rock with one square to
#    stand on, that makes every "same as characters" event on it unusable.
#
# So the props out here are **player-touch, below characters**, which is the
# idiom this world map already uses for the Standing Stones and the Hermit -
# you walk onto the thing and it speaks - and each rock keeps exactly one bare
# square in the middle for the airship.
# All three are `+ (35,35)`, and `review.py` checks all of them by name on
# every build - cell count, walkable count, landable count and region - because
# the Middle Distance quietly lost one of its two hill cells to the middle
# redraw and had five walkable squares instead of four. There is a fourth rock
# now, the Former Premises at (79,88), which is `worldmap.json`'s own and has no
# constant here because nothing in this game's code goes there yet.
WORLD_ISLE = (55, 83)           # the Isle of Uncertain Ownership: 4 tiles east
WORLD_ISLE_PAD = (57, 83)       # the one square with nothing standing on it
WORLD_STACK = (37, 40)          # Attempt 112, on its sea stack: 3 tiles east
WORLD_STACK_PAD = (39, 40)
WORLD_MIDDLE = (82, 65)         # the Hermit's middle distance: 2 by 3
WORLD_MIDDLE_PAD = (83, 66)

# ------------------------------------------------------ Firstfield Meadow --
# The optional tutorial, `meadow.py`. The rainbow stands on the grass west of
# the village's north road; its foot is the way in, and a two-tile spur of
# road joins it to the road.
MAP_MEADOW = 28
WORLD_MEADOW = (55, 74)         # was (20,39); the foot of the rainbow
WORLD_MEADOW_STEP = (56, 74)    # was (21,39); on the spur, one east of it

# ------------------------------------------------------------ the signposts --
# Four world-map signposts were hand-written coordinates inside `journey.py`,
# `wilds.py` and `field.py` rather than constants, which is why they were the
# only world-map events this rewrite could have missed. They are here now.
# Each is `+ (35,35)`; each sits on a `WB_SIGN` tile that blocks its own cell
# and is read from the tile beside it, which is the idiom and not a fault.
WORLD_SIGN_SOUTH = (58, 73)     # was (23,38): north for the Tower, south for home
WORLD_SIGN_NORTH = (64, 46)     # was (29,11): visitors 47, survivors scratched off
WORLD_SIGN_COAST = (63, 80)     # was (28,45): the two ends of the coast road
# and the west road's own is `WORLD_JUNCTION`, which always was a constant.
