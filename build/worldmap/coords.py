"""Every world-map coordinate the scenarios name, checked against the map.

The scenario suite is the ground truth and it takes **169 minutes**. This asks
the cheap half of the same question in under a second: of every coordinate the
thirty-seven scenarios name *while the player is on Map 8*, is there any that
the finished map cannot support? It would have caught fourteen of the fifteen
stale coordinates the 120x120 migration left behind (WORLDMAP.md 6.8), and it
is worth keeping because a later change to `run_finish.py` can break a
scenario's assumption about a square without anybody running the suite.

    python3 thistlewick/build/worldmap/coords.py

**The signature it looks for is "unconverted", not "wrong".** A coordinate that
is not standable *now* but would be standable at `+ (35,35)` is almost certainly
an old 50x50 coordinate somebody forgot: the old map sits inside the new one at
that offset, so the coincidence is not a coincidence. Anything else it finds is
reported as merely not standable, which is sometimes correct - a `WB_SIGN` tile
blocks its own cell and is read from beside it, and two `isAirshipLandOk` checks
*expect* false - so those are listed and not counted as failures.

Three things it has to get right, each of which was got wrong first:

  * **Track which map the scenario is on.** A coordinate is only a world-map
    coordinate if the player is on Map 8 when the step runs, which depends on
    the `query`, every `goto`, and every `mapId()` check.
  * **Coordinates hide in `eval` strings and in the `query`**, not only in
    `expect` arrays - `$gamePlayer.locate(31, 8)`,
    `$gameMap.airship().setLocation(8, 10, 13)`, `?map=8&x=21&y=39`. Two
    affected scenarios never mention Map 8 anywhere else, because they *begin*
    on it.
  * **A position check is not necessarily about the player.** `two_hundred`
    asserts where the airship is parked, and a rule that matched
    `gamePlayer.x` sailed straight past it - which is the one the suite had to
    find, after 883 seconds, as scenario thirty-six of thirty-seven.
"""
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.dirname(os.path.dirname(HERE))
WORLD_ID = 8

# `locate`, `setLocation`, `regionId`, `isAirshipLandOk`, `eventsXy` - anything
# that names a square in an expression rather than in an `expect`.
CALLS = [re.compile(p) for p in (
    r'locate\(\s*(\d+)\s*,\s*(\d+)\s*\)',
    r'setLocation\(\s*\d+\s*,\s*(\d+)\s*,\s*(\d+)\s*\)',
    r'regionId\(\s*(\d+)\s*,\s*(\d+)\s*\)',
    r'isAirshipLandOk\(\s*(\d+)\s*,\s*(\d+)\s*\)',
    r'eventsXy\(\s*(\d+)\s*,\s*(\d+)\s*\)')]
# Any check reading an x and a y together is a position check, whoever it is of.
POSITION = re.compile(r'(_x|\.x)\b.*(_y|\.y)\b')
START = re.compile(r'map=(\d+)&x=(\d+)&y=(\d+)')


def standable(m, ts, x, y):
    """Passable from at least one direction - the same question `validate.py`
    asks of a transfer destination, and the right one here: a scenario may
    legitimately name a blocked square to assert that it is blocked."""
    if not (0 <= x < m["width"] and 0 <= y < m["height"]):
        return False
    w, h, d = m["width"], m["height"], m["data"]
    flags = ts[0]
    for z in (3, 2, 1, 0):
        t = d[(z * h + y) * w + x]
        if t and not (ts[t] & 0x10):
            flags = ts[t]
            break
    return any((flags & bit) == 0 for bit in (0x01, 0x02, 0x04, 0x08))


def world_coords(path):
    """(where, (x, y), wanted) for every square this scenario names while on
    Map 8. `wanted` is False when the step is *asserting* the square is no good
    - `isAirshipLandOk(x, y)` expecting false - because then a coordinate that
    is not standable is the point rather than a mistake, and flagging it makes
    the check cry wolf about the two squares it most wants to protect."""
    doc = json.load(open(path))
    steps = doc.get("steps") or []
    out, here = [], None
    start = START.search(doc.get("query", ""))
    if start:
        here = int(start.group(1))
        if here == WORLD_ID:
            out.append(("query", (int(start.group(2)), int(start.group(3))),
                        True))
    for i, step in enumerate(steps):
        if not isinstance(step, dict):
            continue
        goto = step.get("goto")
        if isinstance(goto, list) and len(goto) == 3:
            here = goto[0]
            if here == WORLD_ID:
                out.append(("goto %d" % i, (goto[1], goto[2]), True))
        check, expect = str(step.get("check", "")), step.get("expect")
        if check == "$gameMap.mapId()" and isinstance(expect, int):
            here = expect
        if check.startswith("[$gameMap.mapId()") and isinstance(expect, list) \
                and expect:
            here = expect[0]
        if here != WORLD_ID:
            continue
        text = str(step.get("eval", "")) + " " + check
        denied = "isAirshipLandOk" in check and expect is False
        for pat in CALLS:
            for hit in pat.finditer(text):
                out.append(("step %d" % i,
                            (int(hit.group(1)), int(hit.group(2))),
                            not denied))
        if POSITION.search(check) and isinstance(expect, list):
            # One position, or a list of them - `[[name, x, y], ...]` is how a
            # site's scenario lists its door events.
            many = expect and all(isinstance(e, list) for e in expect)
            for e in (expect if many else [expect]):
                if len(e) == 2:
                    out.append(("expect %d" % i, (e[0], e[1]), True))
                elif len(e) == 3:
                    out.append(("expect %d" % i, (e[1], e[2]), True))
    return out


def main():
    m = json.load(open(os.path.join(GAME, "data", "Map%03d.json" % WORLD_ID)))
    ts = json.load(open(os.path.join(GAME, "data", "Tilesets.json")))
    ts = ts[m["tilesetId"]]["flags"]
    stale, blocked, total, files = [], [], 0, 0
    for path in sorted(glob.glob(os.path.join(
            GAME, "build", "scenarios", "*.json"))):
        coords = world_coords(path)
        if not coords:
            continue
        files += 1
        total += len(coords)
        for where, (x, y), wanted in coords:
            if standable(m, ts, x, y):
                continue
            name = os.path.basename(path)
            if wanted and x < 50 and y < 50 and standable(m, ts, x + 35, y + 35):
                stale.append((name, where, (x, y), (x + 35, y + 35)))
            else:
                blocked.append((name, where, (x, y)))
    print("%d world-map coordinates in %d of %d scenarios"
          % (total, files,
             len(glob.glob(os.path.join(GAME, "build", "scenarios", "*.json")))))
    for name, where, old, new in stale:
        print("  STALE  %-26s %-10s (%d,%d) - would be standable at (%d,%d)"
              % (name, where, old[0], old[1], new[0], new[1]))
    for name, where, c in blocked:
        print("  note   %-26s %-10s (%d,%d) is not standable, which may be the "
              "point" % (name, where, c[0], c[1]))
    return 1 if stale else 0


if __name__ == "__main__":
    sys.exit(main())
