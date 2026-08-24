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
