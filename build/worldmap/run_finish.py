#!/usr/bin/env python3
"""The hand pass over the generated world. Re-runnable; see WORLDMAP.md.

Always starts from `generated.json` - the template worldgen produced, which is
never edited - and writes `worldmap.json`, which is what gets installed. So
every edit here is a line of code rather than a change nobody can find again.

    python3 thistlewick/build/worldmap/run_finish.py            # from the workspace root
    python3 thistlewick/build/worldmap/run_finish.py --stage 941  # and into staging

`finish.py` holds the operations; this file holds the decisions.
"""
import collections
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, 'tools'))
sys.path.insert(0, ROOT)

import finish as F                                             # noqa: E402
import rmmzdata as R                                           # noqa: E402

GENERATED = os.path.join(HERE, 'generated.json')
OUT = os.path.join(HERE, 'worldmap.json')
ROUND11 = os.path.join(HERE, 'round11.json')

# The Former Premises: the castle row of Mike's floating island, the two cells
# an airship sets down on. Named up here because `sink_islets` has to be told
# to spare it - walkable cells nobody can walk to are precisely what that pass
# is for drowning. (81,88) was the old landing pad, beside two cells of cloud.
PREMISES = [(79, 88), (80, 88)]
OLD_PAD = (81, 88)

# Mike's floating island (P2, 7 Oct 2026), drawn in the editor and diffed in
# here: `Floating Continent (Castle)`, `Floating Continent` and its `(Shadow)`,
# 2 wide and 3 deep, on layer 1 over open sea. The castle row is made open
# ground on tileset 8 (`build_game.build_tilesets`); the other two rows stay
# star tiles, so the sea under them decides and they are not land.
ISLAND = {(79, 88): 240, (80, 88): 241, (79, 89): 242, (80, 89): 243,
          (79, 90): 250, (80, 90): 251}

# Mike's mountain behind the Door into the Mountain (P2, 7 Oct 2026), drawn in
# the editor and diffed in here: two `Rock Mountain` stamps (202 203 / 210
# 211) overlapping behind the `Tunnel`, the massif (A2 kind 22) carried across
# to x=31, and the road (kind 29) moved one cell east to x=32 to go round it.
# Layers 1, 2 and 3 for every cell of the block; `A(k)` is an autotile kind,
# shaped when the map is saved.
def A(kind):
    return R.make_autotile(kind, 0)


MOUNTAIN_DOOR = {
    (29, 18): (A(29), 0, 0), (30, 18): (A(29), 0, 0),
    (31, 18): (A(29), 0, 0), (32, 18): (A(29), 0, 0),
    (29, 19): (0, 0, 0), (30, 19): (0, 0, 0),
    (31, 19): (0, 0, 0), (32, 19): (A(29), 0, 0),
    (29, 20): (A(22), 202, 0), (30, 20): (A(22), 203, 202),
    (31, 20): (A(22), 0, 203), (32, 20): (A(29), 0, 0),
    (29, 21): (A(22), 210, 0), (30, 21): (210, 211, 20),
    (31, 21): (211, 0, 0), (32, 21): (A(29), 0, 0),
    (29, 22): (0, 0, 95), (30, 22): (0, 0, 0),
    (31, 22): (0, 0, 0), (32, 22): (A(29), 0, 0),
    (29, 23): (0, 0, 116), (30, 23): (0, 0, 117),
    (31, 23): (0, 0, 0), (32, 23): (A(29), 0, 0),
    (29, 24): (A(29), 0, 0), (30, 24): (A(29), 0, 0),
    (31, 24): (A(29), 0, 0), (32, 24): (A(29), 0, 0),
}


# Mike's seventh round in the editor (15 Oct 2026), diffed in here: every cell
# of all four tile layers as he left it. The lake west of Upper Clanging grown
# down into the hills, the Mountain (Rock) shoulder at (41,70), Thistlewick's
# shore at (49,79) given back as dirt, and four road ends straightened (23,75),
# (32,111) and (47,117), and the inlet under Hithermost's new road filled
# in. The village's own move is in `MOUNTAIN_DOOR` above.
# Autotiles are re-shaped by `settle`, which reproduces his shapes.
ROUND7 = {
    (30, 24): (2816, 3473, 0, 0),
    (31, 24): (2816, 3473, 0, 0),
    (32, 24): (2816, 3479, 0, 0),
    (30, 25): (2844, 0, 0, 0),
    (31, 25): (2844, 0, 0, 0),
    (32, 25): (2844, 0, 0, 0),
    (31, 26): (2069, 0, 0, 0),
    (35, 46): (2856, 0, 0, 0),
    (36, 46): (2824, 0, 0, 0),
    (32, 47): (2056, 0, 0, 0),
    (33, 47): (2048, 0, 0, 0),
    (34, 47): (2050, 0, 0, 0),
    (35, 47): (2084, 0, 0, 0),
    (36, 47): (2832, 0, 0, 0),
    (31, 48): (2852, 0, 0, 0),
    (32, 48): (2088, 0, 0, 0),
    (33, 48): (2056, 0, 0, 0),
    (34, 48): (2052, 0, 0, 0),
    (35, 48): (2086, 0, 0, 0),
    (36, 48): (2832, 0, 0, 0),
    (31, 49): (2818, 3149, 0, 0),
    (32, 49): (2852, 0, 0, 0),
    (33, 49): (2088, 0, 0, 0),
    (34, 49): (2073, 0, 0, 0),
    (35, 49): (2850, 3138, 0, 0),
    (36, 49): (2817, 3124, 0, 0),
    (32, 50): (2818, 0, 0, 0),
    (33, 50): (2852, 0, 0, 0),
    (34, 50): (2080, 0, 0, 0),
    (35, 50): (2832, 3120, 0, 0),
    (32, 51): (2820, 0, 0, 97),
    (33, 51): (2854, 0, 0, 0),
    (34, 51): (2080, 0, 0, 0),
    (35, 51): (2832, 3120, 0, 0),
    (32, 52): (2840, 0, 0, 105),
    (33, 52): (2091, 0, 0, 0),
    (34, 52): (2087, 0, 0, 0),
    (35, 52): (2832, 3120, 0, 0),
    (32, 53): (2818, 0, 0, 0),
    (33, 53): (2836, 0, 0, 0),
    (34, 53): (2836, 3147, 0, 0),
    (35, 53): (2817, 3133, 0, 0),
    (40, 70): (3708, 3902, 0, 0),
    (41, 70): (3692, 3909, 0, 0),
    (40, 71): (2852, 3477, 0, 0),
    (41, 71): (3724, 3916, 0, 0),
    (23, 75): (3200, 3477, 0, 0),
    (25, 75): (3200, 0, 0, 0),
    (26, 75): (3200, 0, 0, 0),
    (23, 76): (3200, 3481, 0, 0),
    (24, 76): (3200, 3473, 0, 0),
    (25, 76): (3200, 3473, 0, 0),
    (26, 76): (3200, 3463, 0, 0),
    (49, 78): (3306, 0, 0, 0),
    (50, 78): (3316, 0, 0, 0),
    (48, 79): (2093, 0, 0, 0),
    (49, 79): (3336, 0, 0, 13),
    (50, 79): (3324, 0, 0, 13),
    (32, 111): (2816, 3472, 0, 0),
    (35, 111): (2816, 0, 0, 0),
    (36, 111): (2816, 0, 0, 0),
    (32, 112): (2816, 3481, 0, 0),
    (33, 112): (2816, 3473, 0, 0),
    (34, 112): (2816, 3473, 0, 0),
    (35, 112): (2816, 3473, 0, 0),
    (36, 112): (2816, 3473, 0, 0),
    (47, 117): (3216, 0, 0, 0),
    (48, 117): (3204, 3472, 0, 0),
    (48, 118): (3225, 3472, 0, 0),
    (47, 119): (3716, 3460, 0, 0),
    (48, 119): (3232, 3466, 0, 0),
    (49, 119): (3712, 0, 0, 0),
}


def main(argv):
    shutil.copy(GENERATED, OUT)
    w = F.World(OUT)
    o = F.old

    print("coast mended:   %d cells" % F.mend_coast(w))

    # The Hermit's Middle Distance: 2 by 3 at old (47,30). Air-only, so water
    # all round it - `validate.py` asserts on foot that it cannot be reached.
    rock = [o(x, y) for y in range(30, 33) for x in range(47, 49)]
    rock = [(x, y) for x, y in rock if w.base(x, y) not in (None, F.SEA)]
    print("Middle Distance isolated: %d cells of water cut" % F.isolate(w, rock))

    # The Bottomless Pit, which the middle redraw had buried under a mountain.
    print("Bottomless Pit dug out: %d cells" % F.dig_out(
        w, [o(x, y) for y in range(33, 38) for x in range(6, 11)]))

    # The range, between the Gloamwood's two mouths - (52,62) south and (52,55)
    # north, which Mike's round eleven moved to (52,57) - so the tunnel pierces it instead of sitting beside it. The 50x50's
    # version was `MM.MM.MM` on a fixed period and read as a fence.
    spine = [(40, 62), (46, 60), (52, 58), (64, 57), (74, 59), (86, 56)]
    print("range drawn:    %d cells" % F.draw_range(
        w, spine, thickness=2.4, passes=[], keep=F.old_events()))

    # --- the settlements ----------------------------------------------------
    # The sample world map's own coastal town, `Map001` at (105,121), is the
    # idiom: `Town A` on the LAST row of land, ONE `Pier (V)` on the sea tile
    # directly below it, road arriving from the north. No run of jetty, no gap
    # of beach between the town and the water.

    # Thistlewick: a town, beside the road rather than astride it. The 50x50
    # drew it as `Fortress City` - a walled city, for a turnip village - and
    # stood it on the road column at x=59.
    print("Thistlewick: %d city tile(s) rubbed out" % F.unstamp(
        w, o(24, 43), 'World_B/Fortress City'))
    F.put_road(w, [(60, 78), (61, 78)])
    F.restamp(w, (60, 79), 'World_B/Town B')

    # The Lighthouse: the same tower, without the snow on it, and on a
    # headland instead of on flat coast. `EXPANSION.md` calls it "a world-map
    # landmark east of Sopping **on a spit of rock**", and the generated coast
    # left it two cells inland of a blunt corner - a lighthouse standing in a
    # field, which is the one thing a lighthouse cannot be.
    #
    # So: a spit, three cells long and two deep, of Rocky Land A - the bracket
    # in the design document is "rock" and the palette has one - reaching east
    # out of the coast at x=76, water cut on both sides of it, and the tower
    # moved to its tip. The door is the stamp's lower cell and `Tower A`'s is
    # walkable, exactly as `Tower A (Snow)`'s was, so the transfer event still
    # stands on open ground. **The Lighthouse therefore moves to (79,80)**, and
    # section 6 item 6 has to re-derive its exit from that and not from +35.
    F.unstamp(w, o(41, 44), 'World_B/Tower A (Snow)')
    for y in (79, 80):
        for x in (77, 78, 79):
            w.put_land(x, y, 'rocky')
    for x, y in [(77, 78), (77, 81), (78, 81), (77, 82)]:
        w.put_sea(x, y)                     # the water either side of the neck
    F.put_road(w, [(77, 80), (78, 80)])     # the track out to the light
    #
    # **And the tower keeps its snow, which reverses half of section 4.** The
    # `propsheet.py` pass of item 5 found that section 4's "the same tower,
    # without the snow on it" made the Lighthouse `Tower A` - ids 80 and 88 -
    # which is exactly what `journey.py` draws the **Obligatory Tower** with, at
    # (66,42). So the landmark east of Nether Sopping and the final dungeon were
    # the identical graphic, which no reachability check, no validator and no
    # single screenshot can see; it takes a contact sheet of the ids.
    #
    # The whole field was cropped and looked at. `Tower B` is `Tower A` in
    # browner stone and indistinguishable at 48 pixels. `Tower C` is a pink
    # ziggurat. `Tower D` is one cell, so the spit loses its vertical landmark.
    # Every `World_C` tower - including `World_C/Lighthouse` - is a skyscraper,
    # a steel mast or a modern light, which is the wrong century for a keeper
    # whose great-grandmother kept the same lamp. `Tower A (Snow)`'s white top
    # is a **lamp room**, which is why the shipped game's own constant for it is
    # `WB_TOWER_WHITE`. A few snow flecks on the stonework in temperate country
    # is a far smaller fault than the final dungeon having a twin.
    #
    # **And then `Tower B` after all** (Mike, in the editor, October 2026):
    # brown stone, no snow. It is the one he looked at in place and chose, and
    # it is a different enough tower from the Obligatory one at 48 pixels that
    # the twin above is no longer the question.
    F.restamp(w, (79, 79), 'World_B/Tower B')

    # The Sky Anvil: a meteorite used as a gatepost since 1749, and HOB-4's
    # whole joke - Elias Meech will not sell a very good gatepost and will trade
    # for a gate. worldgen drew it with `Giant Tree (Snow)`, so it was a snowy
    # tree standing in for a rock, which the item 5 contact sheet found and no
    # screenshot of the map would have: at 48 pixels it is a plausible landmark
    # that contradicts the only line of dialogue about it.
    #
    # The constraint that produced the tree is real and worth writing down: a
    # site's door is a **player-touch, below-characters** event standing on the
    # stamp's own cell, so the stamp has to be *open*, and every rock in the
    # catalogue is blocked - `Dirt` (which is what this game's own Standing
    # Stones are drawn with) is 0x60f, and so is every `Rocky Mountain` and both
    # `Statue`s. Of the 74 open one-cell stamps, `Shrine` is a stone trilithon
    # with a boulder resting across the top - a gatepost with a rock on it - and
    # it is open, so the door does not move.
    #
    # **The unsnowed one, even though this is snow country**, which is the
    # opposite call to the Lighthouse's two paragraphs up and for the opposite
    # reason. Both variants were rendered in place and looked at: `Shrine (Snow)`
    # is white stone under white snow on a white snowfield and disappears, and a
    # landmark you cannot see is not a landmark. Grey stone reads at 48 pixels.
    # People keep the snow off a gatepost.
    F.unstamp(w, (76, 26), 'World_B/Giant Tree (Snow)')
    F.restamp(w, (76, 26), 'World_B/Shrine')

    # Nether Sopping: unsnowed, down on the last land row, road spur to its
    # north, one pier below it.
    print("Nether Sopping: %d snow-city tile(s) rubbed out" % F.unstamp(
        w, o(36, 44), 'World_B/Fortress City (Snow)'))
    F.put_road(w, [(71, 82), (71, 83)])
    F.restamp(w, (71, 84), 'World_B/Town A')
    F.put_tiles(w, [(72, 85)], 'World_B/Pier (V)')

    # Upper Clanging: an industrial village, not a snowbound castle.
    # `World_C/Slum` is 2x2 - the same footprint - and tileset 1 carries
    # World_C. This is the stamp that found the TILE_ID_C bug; see WORLDMAP.md.
    print("Upper Clanging: %d snow-city tile(s) rubbed out" % F.unstamp(
        w, o(9, 12), 'World_B/Fortress City (Snow)'))
    F.restamp(w, o(8, 11), 'World_C/Slum')

    # --- the sites the design documents ask for (WORLDMAP.md 7.1) -----------
    # Each is one stamp and one player-touch door event per walkable cell, with
    # no destination - the same state the generated twenty-one are in. None of
    # them needs an interior to exist first. `F.add_site` refuses a stamp that
    # lands on another footprint or that leaves no standable cell to put a door
    # on, which is the check 7.6 asks for and arithmetic does not do.

    # Ashcombe Lake, for COR-2: the drowned Ashcombe (Old) is under it, and it
    # is drawn down one week a year for the sluices. It has to be a *walk* from
    # Ashcombe (102,55) so that the draw-down week is a walk from COR-1's
    # drainage dinner, and Ashcombe sits in a mountain valley, which is where a
    # reservoir belongs. Two cells, north-east of the village, against the
    # massif; the door is the southern one, which is the shore you arrive on.
    # **The lake is water, not a `Pond`.** `Pond` is one small round pond drawn
    # on a single tile, which is right for the Duck's below and wrong here: laid
    # over seven cells it is seven small round ponds, and the thing that has to
    # read is a lake with a village underneath it. So the sea autotile, inland -
    # the same way the water below the Bottomless Pit is drawn - and the door on
    # the southern shore. Which is also the better joke: COR-2 says the lake is
    # drawn down for the sluices and "if you are there that week you can walk
    # in", so the way into Ashcombe (Old) is a square of shoreline.
    for c in [(105, 51), (104, 52), (105, 52), (106, 52),
              (104, 53), (105, 53), (106, 53)]:
        w.put_sea(*c)
    #
    # Mike's round eleven (22 Oct 2026) reshaped the lake and moved the door
    # one east and one south, to (105,55) on the shore the road comes up to.
    # That cell is still water until `ROUND11` is laid below, so the door goes
    # down unchecked here; `nomap.py` and `places.LAKE_SHORE_STEP` check it
    # against the finished map instead.
    print("Ashcombe Lake:  door at %s" % F.add_site(
        w, (105, 55), None, 'Ashcombe Lake', 'lake', check=False))

    # The Duck's Pond, for ZEPH-2. `COMPANIONS.md` puts it "four miles from the
    # Collegium" (112,38) and the Duck is an honorary Fellow who holds a chair
    # and votes, so it is close enough to commute from.
    print("The Duck's Pond: door at %s" % F.add_site(
        w, (115, 40), 'World_B/Pond', "The Duck's Pond", 'pond'))

    # Mrs Emberthwaite's hill, for `BIOS.md` Rosamund. The dragon is retired,
    # widowed and wants somebody to play cards with, and the whole point of the
    # bio is that Rosamund "has started going round on Thursdays **without
    # being carried**" - so it has to be a walk from Fairholme (104,73), not a
    # flight. A hill is drawn rather than stamped, because the palette has no
    # hill: nine cells of mountain, with the lair as a `Cave A` on layer 3 in
    # the middle of its southern face. A cave mouth over mountain relief reads
    # back as *open* - the topmost non-star tile decides - which is exactly how
    # the Bottomless Pit and the Barrow have always worked.
    # Shaped by hand rather than as a 3x3 block, because a square of nine
    # identical peaks reads as a plantation. Three, five, three - wider in the
    # middle - with the lair in the centre of the southern face.
    hill = ([(x, 67) for x in range(110, 113)]
            + [(x, 68) for x in range(109, 114)]
            + [(x, 69) for x in range(110, 113)])
    print("Emberthwaite's hill: %d cells of mountain"
          % sum(1 for c in hill if w.put_mountain(*c)))
    # And a track to it, off the Fairholme road - five cells, and the only road
    # on the map that goes to a dragon. Rosamund goes round on Thursdays and
    # carries the cake tin herself; a lair nobody visits has no path to it, and
    # this one is visited weekly.
    F.put_road(w, [(x, 70) for x in range(107, 112)])
    print("the lair:       door at %s" % F.add_site(
        w, (111, 69), 'World_B/Cave A', "Mrs Emberthwaite's lair", 'lair'))

    # Tobias Frayne's cottage, for MER-4 - revived eleven times, and has
    # developed a relationship with mortality. `COMPANIONS.md` sites him on
    # "the coast road cottage", which is a real coordinate now: the old map's
    # coast road is y=45 from Thistlewick to Nether Sopping, which is **y=81**
    # here, and this is the south side of it, half way along. `World_C/Hut` is
    # blocked on its own cell and so cannot carry a door the player walks into;
    # `House (Town)` is open, which is why 7.1 offered both.
    print("Frayne's cottage: door at %s" % F.add_site(
        w, (66, 82), 'World_B/House (Town)', 'Tobias Frayne', 'cottage'))

    # --- the four sited wrong (WORLDMAP.md 7.2) -----------------------------
    # Penultima is *The Last Town Before The End. Last Chance For Potions*, and
    # it was standing on the eastern road network with the Collegium, Ashcombe
    # and Fairholme - the last town before the east coast. The Tower (66,43) is
    # on a different network, whose approach runs south from the tower door
    # along x=63. Gideon Markup's prices double whenever a Chosen One is
    # sighted on the road, so he has to be on the road the Chosen One is on.
    # Five cells south of the tower, with its doors against that road.
    print("Penultima ->    %s" % F.move_site(
        w, 'Penultima', (64, 48), 'World_B/Town B'))

    # Olde Evermore is *hidden* - `BIOS.md`: "the hidden elven village that
    # every party finds eventually, by falling off the same ledge" - and it had
    # a road to its door like any other village. Hiddenness is geography here,
    # so: the spur goes, and it goes back to **forest** rather than to bare
    # ground, because a cleared cell threading a wood is a path. And a ledge to
    # fall off, which is the mountain shoulder closed round its north and east,
    # leaving the village a pocket in the trees reachable only on foot.
    #
    # **The road past it is the trunk, not a spur, and deleting it cut the
    # south-west off.** The road comes down x=28, doglegs east to x=29 for
    # three rows - right past the village door - and carries on south to
    # Gladhollow; taking those cells out dropped Gladhollow's road network from
    # 79 cells to 21, which nothing on the map says out loud and no screenshot
    # shows. So the trunk is *re-routed* straight down x=28 first, and only then
    # does the dogleg go back to trees.
    F.put_road(w, [(28, 94), (28, 95), (28, 96)])
    for x, y in [(29, 93), (29, 94), (29, 95), (30, 94)]:
        w.put_forest(x, y)
    print("Evermore's ledge: %d cells of mountain" % sum(
        1 for c in [(29, 92), (30, 92), (31, 92), (31, 93), (31, 94)]
        if w.put_mountain(*c)))

    # Hithermost's chapel "stands at the top of the pass above Hithermost,
    # beside the only door into the mountain" - and the Chapel of Continuance
    # is *for* that door: travellers write their names in the Book and then go
    # through it. Both halves were missing. The pass is the neck at y=21 where
    # the western massif reaches the road at x=31, two cells above the village;
    # the `Tunnel` is set into that face and the chapel stands below it, so the
    # Book is the last thing on the near side. `Temple C` because Coldbarrow
    # already has `Temple A (Snow)` and Weeping Bottom has `Temple B`.
    print("the mountain door: %s" % F.add_site(
        w, (30, 21), 'World_B/Tunnel', 'The Door into the Mountain', 'tunnel'))
    print("Chapel of Continuance: %s" % F.add_site(
        w, (29, 22), 'World_B/Temple C', 'Chapel of Continuance', 'chapel'))
    for (x, y), tiles in MOUNTAIN_DOOR.items():
        for z, t in zip((1, 2, 3), tiles):
            w.g.set(x, y, z, t)
    # Mike moved the village and the chapel one west, off the column the
    # tunnel is in, and ran a road under them (October 2026).
    print("Hithermost: doors at %s" % (F.move_site(w, 'Hithermost', (29, 23)),))

    # Restwell is "a crossroads town of one street and nineteen inns", and the
    # road merely arrived at it from the north-west and stopped. So: road on all
    # four sides of the town block, and four arms leaving it - the existing one
    # north-west, a street west and east, and a southern arm down the corridor
    # at x=46 that the mountains leave open, which is a piece of the map that
    # had no road on it at all.
    print("Restwell crossroads: %d cells of road" % F.put_road(w, (
        [(44, 80)]                                       # north, beside (43,80)
        + [(42, 81), (41, 81), (40, 81)]                 # west, to the old road
        + [(45, 81), (46, 81), (47, 81)]                 # east, the lane
        + [(43, 82), (44, 82), (45, 82), (46, 82)]        # south, out of town
        + [(46, y) for y in range(83, 90)])))            # and down the corridor

    # --- Frostwick (WORLDMAP.md 7.3) ----------------------------------------
    # The town that voted to keep the curse. A third of the map's climate had no
    # town in it: Coldbarrow is a chapter house, the Sky Anvil is a gatepost and
    # Hithermost is a pass village. `Town B (Snow)` because it has a committee,
    # a festival, an inn and a contract - and because it is the snowed twin of
    # Thistlewick's own `Town B`, which is the joke: Frostwick is what
    # Thistlewick would be if one of the forty-seven had come home and stayed.
    #
    # Between Coldbarrow (50,19) and the Sky Anvil (76,26), on the 44-cell
    # northern road network that already joins those two, with a three-cell spur
    # east to meet it - so the far north has one road with three things on it
    # instead of three errands.
    #
    # **The northern road did not actually join Coldbarrow to the Sky Anvil**,
    # which is the reason 7.3 gave for this square. Measured: it is its own
    # network of 44 cells that ran between the two and touched neither, because
    # at each end it meets the next network *diagonally* - (50,20) beside
    # (49,19) at Coldbarrow, (76,25) beside (77,26) at the Anvil - and MZ has no
    # diagonal movement, so a diagonal join is a road that stops. That is also
    # most of what the eleven pieces of section 4 are: 20 networks at
    # four-connectivity and 16 at eight. Two cells close both corners, and the
    # far north becomes one road from the chapter house to the gatepost with a
    # town on it, which is what 7.3 asked for and thought it already had.
    F.put_road(w, [(49, 20), (77, 25)])
    F.put_road(w, [(62, 22), (63, 22), (64, 22)])
    print("Frostwick:      doors at %s" % F.add_site(
        w, (61, 21), 'World_B/Town B (Snow)', 'Frostwick', 'town'))

    # --- The Former Premises (WORLDMAP.md 7.4) ------------------------------
    # The floating castle the engagement was vacated from, on accessibility
    # grounds, because nobody could ever reach it. The airship makes the
    # complaint moot four hundred years late, which is the whole joke and lands
    # the moment the player sets down on it.
    #
    # It was three cells of `Clouds` with the castle stamp on two and a bare
    # pad for the airship on the third. Mike redrew it in the editor as a
    # floating island over open sea (`ISLAND`), and the castle row is the land:
    # open ground on tileset 8, which is where the airship sets down.
    #
    # **Nothing may stand on the castle row**, because `Game_Vehicle.isLandOk`
    # refuses a square with an event on it - a door on each cell was a castle
    # with no way in. So the site's two events go on the row *under* it, which
    # is sea under a star tile and nobody's square, and `premises.world_doors`
    # makes one of them a watcher: land on either cell and it asks.
    for c in PREMISES + [OLD_PAD]:
        w.put_sea(*c)
    for (x, y), t in ISLAND.items():
        w.g.set(x, y, 1, t)
    events = w.map.setdefault("events", [None])
    for x, y in [(79, 89), (80, 89)]:
        events.append(R.event(
            len(events), 'The Former Premises', x, y,
            [R.page(R.comment(["hand-placed site 'The Former Premises'",
                               "castle, Mike's floating island; the events",
                               "sit under the castle row, which is the land"])
                    + [R.play_se("Move1")], trigger=1, priority=0)],
            note='<worldmap-site castle> <aironly>'))
    print("Former Premises: events at (79,89) (80,89)   lands on %s"
          % (PREMISES,))

    # --- the decoration the middle redraw ate -------------------------------
    # Thirteen layer-3 cells the 50x50 drew by hand and the generated map has
    # not got. They are not events, so the pass that replaced a drawn world map
    # with a generated one deleted them in silence; `decor.py` is the diff that
    # finds them and is the check to re-run after any change here.
    #
    # The Pit is the one that matters: it is a real destination with a transfer
    # event on it, `dig_out` above already takes it back out of the mountain the
    # redraw buried it under, and without this line it is an invisible hole in
    # open ground. The two tents are the same fault one step down - the Hermit
    # and Meredith Crooke both kept their events and their squares and had
    # nothing to look at.
    F.report_scenery("Pit's cave mouth", F.put_scenery(w, [o(8, 35)], 'World_B/Cave A'))
    F.report_scenery("the two tents", F.put_scenery(
        w, [o(40, 29), o(11, 32)], 'World_B/Tent'))          # Hermit, Crooke
    # Scatter, from the hand-typed lists in `journey.py`, `wilds.py` and
    # `field.py`. Three of the seven trees now stand under the hand-drawn range
    # and one is out past the mended coast, so those nudge rather than hole the
    # range for a decoration; see `put_scenery`.
    F.report_scenery("scatter trees", F.put_scenery(
        w, [o(40, 21), o(37, 22), o(9, 25), o(34, 29), o(7, 33), o(44, 33),
            o(12, 35)], 'World_B/Giant Tree'))
    F.report_scenery("scatter rocks", F.put_scenery(
        w, [o(36, 13), o(7, 22), o(31, 31)], 'World_B/Dirt'))

    # --- the tidy-up --------------------------------------------------------
    # Scraps of beach the coast mend left standing go back to sea, except the
    # three rocks only the airship can reach.
    # The floating island's shadow row reads as two cells of land here, on
    # tileset 1's flags; it is a star on the world map's own tileset 8, where
    # the sea decides. Spared, or it is drowned as a two-cell islet.
    rocks = [o(21, 48), o(3, 5), o(47, 31), PREMISES[1], (79, 90)]
    flags = F._openness(w)
    start, main_land = o(24, 45), None
    main_land, q = {start}, collections.deque([start])
    while q:
        x, y = q.popleft()
        for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
            if (0 <= nx < w.w and 0 <= ny < w.h
                    and (nx, ny) not in main_land and flags[ny][nx]):
                main_land.add((nx, ny)); q.append((nx, ny))
    islets, sunk = F.sink_islets(w, main_land, rocks)
    print("islets drowned: %d (%d cells)" % (islets, sunk))

    # --- the three air-only rocks (WORLDMAP.md item 4) ----------------------
    # The Middle Distance's back row is a **hill** - `field.py`'s `W_HILLS`, on
    # layer 1, flagged 0x0e0f, which is impassable and carries 0x0800 as well,
    # so it is scenery an airship cannot set down on and the two rows of grass
    # in front of it are where the airship goes and where the bench is. The
    # middle redraw took one of the two cells and nothing reported it: item 7
    # suspected as much, and it is confirmed - (82,65) came back **open**, so
    # the rock had five walkable cells instead of four and the Hermit had a
    # hill with a hole in it.
    #
    # `decor.py` cannot see this and is not going to be made to. It diffs
    # layers 2 and 3, where a decoration is a tile that is either there or not;
    # layer 1 is autotiled terrain that differs almost everywhere on purpose,
    # so a diff of it reports the whole new world. The rocks are checked by
    # name in `review.py` instead.
    for c in [o(47, 30), o(48, 30)]:
        if w.relief(*c) is None:
            print("Middle Distance: hill restored at %s" % (c,))
            w.put_mountain(*c)

    # --- the region layer (WORLDMAP.md item 3) ------------------------------
    # Last, because regions are painted over a *finished* map - and after
    # `settle`, because a passability flag belongs to an autotile shape rather
    # than to a kind, so a pass that asks "can the player stand here" over
    # every cell has to be looking at the shapes the engine will see.
    # --- the placeholder doors ----------------------------------------------
    # Twenty-nine doors with nothing behind them. On a review map a chime is
    # useful; in the shipped game it is a sound effect that promises a room
    # twenty-nine times and never delivers, so they are made **inert** - a page
    # with no commands, which the engine never starts and `validate.py` exempts
    # from every "can this be triggered" question - and what the page said moves
    # into the note. Normalised here rather than in `journey.py` so the staged
    # map and the installed map behave the same; `generated.json` is never
    # edited, so this is the only place the generated twenty-one can be reached.
    print("placeholder doors made inert: %d" % F.make_doors_inert(w))

    for (x, y), tiles in ROUND7.items():
        for z, t in enumerate(tiles):
            w.g.set(x, y, z, t)
    print("Mike's round seven: %d cells" % len(ROUND7))


    w.settle()

    # Mike's round eleven (22 Oct 2026), the same thing again and larger: road
    # changes all over, tiles made truer to what stands there (the Wreck and
    # the Barrow lose their `Cave (Collapsed)`, as do both Gloamwood mouths),
    # Ashcombe Lake redrawn round its new door. Every cell he changed, all
    # four tile layers as he left it; too long to read as code, so it is data.
    # Laid *after* `settle`, unlike round seven: along the bottom edge the
    # editor shapes autotiles differently from `settle`, and his shapes win.
    with open(ROUND11) as f:
        round11 = json.load(f)
    for x, y, tiles in round11:
        for z, t in enumerate(tiles):
            w.g.set(x, y, z, t)
    print("Mike's round eleven: %d cells" % len(round11))

    quiet = ([(55 + i, 83) for i in range(4)]            # the Isle
             + [(37 + i, 40) for i in range(3)]          # Attempt 112's stack
             + [(82 + dx, 65 + dy) for dy in range(3) for dx in range(2)]
             + sorted(ISLAND))                           # and the castle in the sky
    counts = F.paint_regions(w, spine, quiet=quiet)
    print("regions painted: %s" % ", ".join(
        "%s %d" % (n, counts.get(r, 0)) for n, r in
        [("south", 1), ("north", 2), ("coast", 3), ("clanging", 4),
         ("snow", 5), ("desert", 6), ("quiet", 0)]))
    print("encounter entries widened to snow and desert: %d"
          % F.point_at(w, F.REG_NORTH, (F.REG_SNOW, F.REG_DESERT)))

    w.save(settle=False)                # keeps round eleven's shapes
    print("wrote %s" % OUT)

    if '--stage' in argv:
        map_id = argv[argv.index('--stage') + 1]
        dest = os.path.join(ROOT, 'staging', 'data', 'Map%03d.json' % int(map_id))
        shutil.copy(OUT, dest)
        print("staged as %s" % dest)


if __name__ == '__main__':
    main(sys.argv[1:])
