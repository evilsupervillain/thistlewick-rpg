"""Map ids and the handful of coordinates that two maps have to agree on.

`village.py` needs to know where the world map's village tile is, and
`journey.py` needs to know where the village gate is. Putting both here keeps
the two modules from having to import each other.
"""

MAP_VILLAGE, MAP_HOME, MAP_HALL, MAP_INN = 1, 2, 3, 4
MAP_CHAPEL, MAP_SMITHY, MAP_STORE = 5, 6, 7
MAP_WORLD, MAP_GLOAMWOOD, MAP_GLOAM_DEEP, MAP_TOWER, MAP_SUMMIT = 8, 9, 10, 11, 12

# The south: Nether Sopping and its interiors, then the three optional places
# out in the world.
MAP_SOPPING, MAP_WYVERN, MAP_GUILD = 13, 14, 15
MAP_OUTFIT, MAP_COTTAGE, MAP_LIGHTHOUSE = 16, 17, 18
MAP_PIT, MAP_BARROW = 19, 20

# Thistlewick's north gate, and the tile you arrive on when you step out of it.
VILLAGE_GATE = (19, 2)
WORLD_VILLAGE = (24, 43)        # the village icon on the world map
WORLD_VILLAGE_STEP = (24, 45)   # two tiles south of it, on the road

# The other two places you can walk into from the world map.
WORLD_GLOAMWOOD = (17, 27)
WORLD_TOWER = (31, 8)

# --------------------------------------------------------------- the south --
# Nether Sopping's own gate, at the top of its one street, and the tiles on the
# world map that lead to it. Everything below here is optional content.
SOPPING_GATE = (20, 2)
WORLD_SOPPING = (36, 44)        # the town icon, at the end of the coast road
WORLD_SOPPING_STEP = (36, 45)   # the tile you stand on to walk into it

WORLD_LIGHTHOUSE = (41, 44)     # on its own headland, east along the shore
WORLD_PIT = (8, 35)             # the Bottomless Pit, west, under the hills
WORLD_BARROW = (33, 21)         # the Barrow of the Forty-Fourth, north-east

# World-map curiosities: things to look at rather than places to go into.
WORLD_STONES = (11, 18)         # the Standing Stones of Uncertain Purpose
WORLD_HERMIT = (40, 30)         # the Hermit of the Middle Distance
WORLD_CRAB = (20, 46)           # where the bounty crab holds the beach
WORLD_CAMP = (12, 32)           # Meredith Crooke's banditry apprenticeship

# --------------------------------------------------------------- the north --
# Upper Clanging and its interiors, then the two places out on the north-west
# lobe of the world map. See `NORTH.md` section 4.3 for the coordinates.
MAP_CLANGING, MAP_WORKS, MAP_VALVE = 21, 22, 23
MAP_FORGE, MAP_PARISH = 24, 25
MAP_LONG_FIELD, MAP_CRAG = 26, 27

CLANGING_GATE = (17, 42)        # the foot of the street, where the road leaves
WORLD_CLANGING = (9, 12)        # the town icon, at the top of the west road
WORLD_CLANGING_STEP = (9, 13)   # the tile you stand on to walk into it
WORLD_LONG_FIELD = (12, 15)     # the wrecks, on a spur off the town road
WORLD_LONG_FIELD_STEP = (11, 15)   # back onto the spur, one west of the gate
WORLD_CRAG = (6, 8)             # Attempt 199, on the rocks north-west
WORLD_CRAG_STEP = (6, 9)        # back onto the track, one south of the mouth
WORLD_JUNCTION = (14, 19)       # the signpost where the west road leaves

# Where the Two Hundred is parked the day she is handed over: plain world
# grass beside the town's door, because the road itself is not airship-
# landable - road tile 3008 already carries 0x0800. See NORTH.md 5.2.
WORLD_AIRSHIP = (10, 13)

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
WORLD_ISLE = (20, 48)           # the Isle of Uncertain Ownership: 4 tiles east
WORLD_ISLE_PAD = (22, 48)       # the one square with nothing standing on it
WORLD_STACK = (2, 5)            # Attempt 112, on its sea stack: 3 tiles east
WORLD_STACK_PAD = (4, 5)
WORLD_MIDDLE = (47, 30)         # the Hermit's middle distance: 2 by 3
WORLD_MIDDLE_PAD = (48, 31)
