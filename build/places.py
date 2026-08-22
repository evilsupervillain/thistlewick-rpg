"""Map ids and the handful of coordinates that two maps have to agree on.

`village.py` needs to know where the world map's village tile is, and
`journey.py` needs to know where the village gate is. Putting both here keeps
the two modules from having to import each other.
"""

MAP_VILLAGE, MAP_HOME, MAP_HALL, MAP_INN = 1, 2, 3, 4
MAP_CHAPEL, MAP_SMITHY, MAP_STORE = 5, 6, 7
MAP_WORLD, MAP_GLOAMWOOD, MAP_GLOAM_DEEP, MAP_TOWER, MAP_SUMMIT = 8, 9, 10, 11, 12

# Thistlewick's north gate, and the tile you arrive on when you step out of it.
VILLAGE_GATE = (19, 2)
WORLD_VILLAGE = (24, 43)        # the village icon on the world map
WORLD_VILLAGE_STEP = (24, 45)   # two tiles south of it, on the road

# The other two places you can walk into from the world map.
WORLD_GLOAMWOOD = (17, 27)
WORLD_TOWER = (31, 8)
