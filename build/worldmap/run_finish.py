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

GENERATED = os.path.join(HERE, 'generated.json')
OUT = os.path.join(HERE, 'worldmap.json')


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
    # north - so the tunnel pierces it instead of sitting beside it. The 50x50's
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

    # The Lighthouse: the same tower, without the snow on it.
    F.unstamp(w, o(41, 44), 'World_B/Tower A (Snow)')
    F.restamp(w, o(41, 43), 'World_B/Tower A')

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

    # --- the tidy-up --------------------------------------------------------
    # Scraps of beach the coast mend left standing go back to sea, except the
    # three rocks only the airship can reach.
    rocks = [o(21, 48), o(3, 5), o(47, 31)]
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

    w.save()
    print("wrote %s" % OUT)

    if '--stage' in argv:
        map_id = argv[argv.index('--stage') + 1]
        dest = os.path.join(ROOT, 'staging', 'data', 'Map%03d.json' % int(map_id))
        shutil.copy(OUT, dest)
        print("staged as %s" % dest)


if __name__ == '__main__':
    main(sys.argv[1:])
