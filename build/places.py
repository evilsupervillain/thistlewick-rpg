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

# ----------------------------------------- the places behind the new doors --
# `../WORLDMAP.md` item 10. The 120x120 arrived carrying twenty-nine sites
# whose doors go nowhere; these are the ones that have a room behind them now.
# **There is no `WORLD_PENULTIMA` constant and that is deliberate** - see
# `WORLDMAP.md` 7.6. Every other world-map coordinate in this file is written
# down here because two modules have to agree on it; a site door's cell is
# written down in `worldmap.json`, which is the one file that knows where the
# stamp is, and `journey.world_map` reads it off the placeholder it replaces.
# A constant here would be a second copy of a number that has already moved
# once - 7.2 shifted Penultima forty-two cells west - and would have gone
# stale in silence.
#
# What a site *does* need here is the square the player is put back on coming
# out, because that is this game's own decision and not the map's.
MAP_PENULTIMA, MAP_SHOPPE = 29, 30
PENULTIMA_STEP = (63, 48)       # the tower road, one west of the western door

MAP_RESTWELL, MAP_EIGHT_HOURS = 31, 32
# One west of the western of Restwell's two `Town A` cells, and checked open
# (`flags & 0x0F == 0`) against the finished `data/Map008.json` rather than
# merely passable - a tile can be passable and still be blocked on three
# sides. All four of Restwell's roads come back out here, which is a
# simplification the map can afford: the crossroads is the town's joke and
# not a junction of the world's.
RESTWELL_STEP = (42, 81)

MAP_HITHERMOST, MAP_CONTINUANCE = 33, 34
# One south of the western of Hithermost's two `Village A` cells, which is the
# bottom of a stack of three sites - the village, the Chapel of Continuance
# above it and the Door into the Mountain above that, all in column 30 - so it
# is the one square below all of them. Checked open four ways
# (`flags & 0x0F == 0`) against the finished `data/Map008.json`, region 2, and
# nothing else standing on it. The village's road and the chapel's porch both
# come back out here; the Door into the Mountain does not go anywhere yet.
HITHERMOST_STEP = (30, 24)

MAP_FAIRHOLME, MAP_ROSAMUND, MAP_LAIR = 35, 36, 37
# Fairholme is the council chamber, Rosamund's tower room is up its stairs,
# and the lair is Mrs Emberthwaite's, on the hill to the north-east. Not
# `MAP_TOWER`, which is the Obligatory Tower, Map 11. Both steps were checked
# open four ways (`flags & 0x0F == 0`) against the finished `data/Map008.json`,
# in region 1 and with nothing standing on them: one south of the western of
# the castle's two `Castle A` cells, and one south of the cave mouth.
FAIRHOLME_STEP = (104, 74)
LAIR_STEP = (111, 70)

MAP_EVERMORE, MAP_ARCHIVE = 38, 39
# Olde Evermore and its Forbidden Archive. One south of the village's one
# `Village C` cell, checked open four ways (`flags & 0x0F == 0`, it is 0xe00)
# against the finished `data/Map008.json`, region 1, nothing standing on it.
# Everybody arrives by falling off the ledge; this is where the path out ends.
EVERMORE_STEP = (30, 94)

MAP_GLADHOLLOW, MAP_MAYORS = 40, 41
# Gladhollow, and the mayor's room with the bookcase. One south of the western
# of the village's two `Village B` cells, checked open four ways (`flags &
# 0x0F == 0`, it is 0x600) against the finished `data/Map008.json`, region 1,
# nothing standing on it. Both gates come back out here.
GLADHOLLOW_STEP = (33, 112)

MAP_PREMISES = 42
# The Former Premises: the hall with the lift, on the floating continent. Air
# only, so this is not "one south of the door": it is the one square of the
# three `Clouds` cells with no door on it, east of the two, checked open four
# ways and airship-landable (0x600, the 0x800 bit clear) against the finished
# `data/Map008.json`, with sea (0x80f) on every other side. It is where the
# airship is standing, because it is the only place she can have landed.
# `MAP_PREMISES`, not `MAP_HALL` - that is Prophecy Hall, Map 3.
PREMISES_STEP = (81, 88)

MAP_FRAYNE = 43
# Tobias Frayne's cottage on the coast road, `../SITES.md` step 8. One south
# of the `House (Town)` stamp's one cell, on the sand between the grass it
# stands on and the sea: checked open four ways (0x600) against the finished
# `data/Map008.json`, with nothing standing on it. `MAP_FRAYNE`, not
# `MAP_COTTAGE` - that is Number Forty-Five's, Map 17.
FRAYNE_STEP = (66, 83)

MAP_FROSTWICK, MAP_ELEVEN_DAYS, MAP_WORKING_GROUP, MAP_COLD_ROOM = 44, 45, 46, 47
# Frostwick, `../SITES.md` step 10: the street, the inn, the room the committee
# meets in, and the practitioner's. One south of the western of the `Town B
# (Snow)` stamp's two cells, on snow, checked open four ways (0x600) against
# the finished `data/Map008.json`, with nothing standing on it. **Not
# `MAP_PARISH`** - that is Upper Clanging's Parish Rooms, Map 25 - so the room
# is named for the thing that meets in it.
FROSTWICK_STEP = (61, 22)

MAP_COLDBARROW = 48
# The Chapter House of the Order of the Errant at Coldbarrow, `../SITES.md`
# step 11. One south of the `Temple A (Snow)` stamp's one cell, on snow,
# checked open four ways (0x600) against the finished `data/Map008.json`, with
# nothing standing on it. `MAP_COLDBARROW`, not `MAP_CHAPTER` or `MAP_CHAPEL` -
# the second of those is Thistlewick's chapel, Map 5.
COLDBARROW_STEP = (50, 20)

MAP_SABLE_HART = 49
# The Sable Hart, `../SITES.md` step 12: an inn where every corner is taken.
# One south of the `House (Town)` stamp's one cell, on the sandy waste, checked
# open four ways (0x600) against the finished `data/Map008.json`, with nothing
# standing on it. **Not `MAP_INN`** - that is Thistlewick's, Map 4.
SABLE_HART_STEP = (24, 76)

MAP_LITTLE_GORE, MAP_SUMP = 50, 51
# Little Gore and Sump, `../SITES.md` step 13: two hamlets, one street each,
# one module (`hamlets.py`). Each step is one south of its stamp's one cell -
# `House (Village)` and `House (Desert)` - checked open four ways (0x600)
# against the finished `data/Map008.json`, with nothing standing on it.
# Sump's door has the sea west of it and north of it, so south is the only
# side of it there is to come back out on.
LITTLE_GORE_STEP = (97, 102)
SUMP_STEP = (78, 103)

MAP_ASHCOMBE, MAP_ASHCOMBE_IN = 52, 53
# Ashcombe, `../SITES.md` step 14: the village that is fine (52), and one map
# of two rooms indoors (53) - Mrs Ash's kitchen and the Drainage Museum, drawn
# side by side in the black the way Gladhollow's mayor's back room is. **Not
# `MAP_KITCHEN` or `MAP_MUSEUM`** - the second map is both. One south of the
# western of the `Village A` stamp's two cells, on grass, checked open four
# ways (0x600) against the finished `data/Map008.json`, with nothing standing
# on it.
ASHCOMBE_STEP = (102, 56)

MAP_WEEPING_BOTTOM, MAP_WARD = 54, 55
# Weeping Bottom, `../SITES.md` step 15: the valley bottom with the
# Sisterhouse in it (54), and the ward, split down the middle (55). **Not
# `MAP_SISTERHOUSE`** - the house is both maps. One south of the `Temple B`
# stamp's one cell, on the track, checked open four ways (0x600) against the
# finished `data/Map008.json`, with nothing standing on it.
WEEPING_BOTTOM_STEP = (58, 100)

MAP_FENMARCH, MAP_GALLERY = 56, 57
# Fenmarch Hall, `../SITES.md` step 16: the walled garden with the house in
# its moat (56), and the long gallery, which is most of the house and has the
# household at one end of it (57). **Not `MAP_HALL`** - that is Prophecy
# Hall, Map 3. One south of the western of the `Large Mansion` stamp's two
# door cells, on grass, checked open four ways (0x600) against the finished
# `data/Map008.json`, with nothing standing on it.
FENMARCH_STEP = (86, 115)

MAP_COLLEGIUM, MAP_COLLEGIUM_LIBRARY, MAP_COLLEGIUM_HALL = 58, 59, 60
# The Collegium Arcanum, `../SITES.md` step 17: the Great Court behind the
# gate (58), the Library (59) and the Hall (60). **Not `MAP_HALL`** - that is
# Prophecy Hall, Map 3 - and not `MAP_LIBRARY` or `MAP_COURT`, which say
# nothing about whose. One south of the western of the `School of Magic`
# stamp's two door cells, on the dirt road that ends at it, checked open four
# ways (0x600) against the finished `data/Map008.json`, with nothing on it.
COLLEGIUM_STEP = (112, 39)

(MAP_DUNNAGE, MAP_SMITHS_HALL, MAP_COUNTING_HOUSE, MAP_BONDED,
 MAP_BELL) = 61, 62, 63, 64, 65
# Great Dunnage, `../SITES.md` step 18: the town inside its wall, with the
# haulage yard in its north-west corner (61), the hall of the Worshipful
# Company of Smiths (62), the lobby of the Sealed Counting House, which is
# mostly door (63), the Bonded Warehouse on the canal (64) and the Bell (65).
# **Not `MAP_WORKS` or `MAP_FORGE`** - those are Upper Clanging's, Maps 22
# and 24 - **and not `MAP_INN`**, which is Thistlewick's, Map 4. One south of
# the western of the `Fortress City` stamp's two door cells, on grass, checked
# open four ways (0x600) against the finished `data/Map008.json`, with
# nothing standing on it.
DUNNAGE_STEP = (31, 53)

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

# NIX-2's room behind the Door (`../QUESTS.md` B6): drawn by `dunnage.py` in
# the black east of Map 63, which was widened for it from 18 to 30 columns -
# the lobby is tile for tile what it was - and furnished by `q_nix.py`. The
# Door is at (8, 4) and the lobby's square in front of it is (8, 5).
#           x1 y1  x2  y2 door_x
VAULT = (23, 5, 25, 7, 24)
VAULT_CHAIR = (24, 5)           # Chair A (Wood), 1x2: back, then the seat
COUNTING_BEFORE_DOOR = (8, 5)

# COR-1's study (`../QUESTS.md` D1), Corvin's old bedroom: drawn by
# `ashcombe.py` in the black east of Map 53, which was widened for it from 26
# to 36 columns - the kitchen and the museum are tile for tile what they were.
# Its door is an event in the kitchen's north wall, up from (6, 4), and its
# way out is the foot of its stairs; both are `q_corvin.py`'s.
#           x1 y1  x2  y2 door_x
STUDY = (28, 4, 33, 8, 30)
STUDY_DOOR = (6, 3)             # on the kitchen's north wall face
STUDY_DESK = (31, 6)            # Table A, two cells, the committee's papers
STUDY_MARKS = (30, 3)           # the height marks, on the north wall face

# COR-2's drowned street (`../QUESTS.md` D2): old Ashcombe, under the lake,
# for the week it is let down. A map in no place, drawn by `q_corvin.py`.
# The way in is Ashcombe Lake's world-map cell, which `worldmap.json` puts at
# (104, 54) and `nomap.py` asserts; the way out is one south of it, checked
# open four ways (0x600) against the finished `data/Map008.json` with nothing
# standing on it.
MAP_DROWNED_STREET = 66
ASHCOMBE_LAKE = (104, 54)
LAKE_SHORE_STEP = (104, 55)
