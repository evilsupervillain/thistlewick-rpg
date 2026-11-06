"""Curios: the things on every map you can look at. `../CURIOS.md` is the
design, and its section 2 is the rules this module enforces.

A curio is an event with no sprite on the cell of a scenery tile, so the
tile is the picture and the event is the answer - the shape of
`postgame._look`. `place()` runs after every builder and after
`build_game.lay_frozen`, so it sees the tiles the player will see, and it
refuses to build when

* the tile a curio names is no longer on its cell (Mike moved it in the
  editor - move the curio), or
* nothing a player can stand on, or reach across a counter from, is next to
  any of its cells.

Ids start at `FIRST_ID` on every map and go up in list order, so a builder
that adds an event later moves none of them. Only ever append to a map's
list.

**Writing one.** `look`, `then` and `again` hold *windows*. A window is

* a string: narration, wrapped to `NARRATION_WIDTH` and at most four lines;
* a list of strings: narration, broken by hand;
* `(speaker, text)` or `(speaker, [lines])`: somebody speaking, as `S.say`;
* a dict, or a list of dicts: raw event commands, for anything else.

`look` (a list of windows) is the first time. `then` is a list of *looks* -
each a list of windows - shown one per press after that, in order: a
bookshelf's other titles. `again` (a list of windows) is every look after
those, for ever; without it the `then` looks go round again, or `look` does.
`party` is a list of `(actor_id, windows)`: the first of them who is in the
party says theirs after `look`, once. `trope` names a kind of cliche from
CURIOS.md 4, which counts once in the whole game however many barrels share
it. `loot` is commands run once, after the first look. `sprite` is a tile id
the event draws itself, nudged by `offset` pixels (`js/plugins/TOQ_Offset.js`)
- for a thing that has to sit off the grid, like a plant in a pot's mouth,
and that a map tile would make walkable (a passable tile on top of a blocked
one wins).

How many times a curio has been looked at lives in `$gameSystem._curios`,
keyed `"map:event"`, which is saved with the game; the twins of a multi-cell
curio share their first cell's key, so the object is looked at once and not
once per side."""

import db
import rmmzdata as R
import story as S

FIRST_ID = 401

# Somewhat inside the 60-character narrator limit: a curio is prose, not a
# line of dialogue, and a wrapped paragraph reads better a little short.
NARRATION_WIDTH = R.message_width(False) * 52 // 60

SPEAKERS = {db.BRAM: "Bram", db.MERRI: "Merribell", db.HOB: "Hob",
            db.ZEPH: "Zephyrine", db.NIX: "Nix", db.ALDRIC: "Aldric",
            db.PIPER: "Piper", db.CORVIN: "Corvin", db.WREN: "Wren",
            db.ROLAND: "Roland", db.SPARE: "Spare"}


class Curio:
    def __init__(self, name, cells, tile, look, then=(), again=None,
                 party=(), trope=None, loot=(), hung=0, sprite=0,
                 offset=(0, 0)):
        self.sprite, self.offset = sprite, tuple(offset)
        self.name, self.cells = name, [tuple(c) for c in cells]
        # A thing hung so high on a two-row wall face that nobody can stand
        # next to it answers from the blank face cell under it; `hung` is
        # how many cells up its tile is drawn.
        self.hung = hung
        self.tile = (tile,) if isinstance(tile, str) else tuple(tile)
        self.look, self.then, self.again = look, list(then), again
        self.party, self.trope, self.loot = list(party), trope, list(loot)


def curio(name, cells, tile, look, **kw):
    """One thing to look at. `cells` are the cells that answer, first one
    first - or one (x, y); `tile` is the `.txt` name (or names) that must be
    on each of them. See the module docstring for the rest."""
    if isinstance(cells, tuple) and len(cells) == 2 and \
            isinstance(cells[0], int):
        cells = [cells]
    return Curio(name, cells, tile, look, **kw)


# ---------------------------------------------------------------- windows --

def _wrap(text, width):
    return R.wrap(text, width, currency=S.CURRENCY)


def window(w):
    """One window, or a run of raw commands, as event commands."""
    if isinstance(w, dict):
        return [w]
    if isinstance(w, list) and w and isinstance(w[0], dict):
        return list(w)
    if isinstance(w, tuple):
        speaker, text = w
        if isinstance(text, str):
            name = S.FACES.get(speaker, ("", 0))[0]
            limit = R.message_width(bool(name))
            # say() puts "Speaker: " in front of the first line.
            lead = R.text_width("%s: " % speaker, currency=S.CURRENCY)
            first = _wrap(text, limit - lead)
            rest = _wrap(text[len(first[0]):].strip(), limit) if first else []
            lines = first[:1] + rest
        else:
            lines = list(text)
        assert len(lines) <= 4, "%s's window is %d lines: %r" % (
            speaker, len(lines), text)
        return S.say(speaker, lines)
    lines = _wrap(w, NARRATION_WIDTH) if isinstance(w, str) else list(w)
    assert len(lines) <= 4, "window is %d lines: %r" % (len(lines), w)
    return S.narrate(lines)


def windows(ws):
    out = []
    for w in ws or []:
        out += window(w)
    return out


# ------------------------------------------------------------------ pages --

def _count(primary, cap, wrap=False):
    """Look this curio up, and count this look - up to `cap`, so the number
    saved with the game stops growing once it has stopped mattering; or, with
    `wrap`, back round to 1 after `cap`."""
    step = ("this._curioN >= %d ? 1 : this._curioN + 1" % cap if wrap
            else "Math.min(this._curioN + 1, %d)" % cap)
    return R.script([
        "const c = ($gameSystem._curios = $gameSystem._curios || {});",
        "const k = this._mapId + ':' + %d;" % primary,
        "this._curioN = c[k] || 0;",
        "c[k] = %s;" % step])


def _nth(n):
    return R.condition_script("this._curioN === %d" % n)


def trope_once(kind):
    """`story.trope()`, once per kind of cliche in the whole game: map 0,
    event 0 is nobody's, so the key is the game's and not an event's. The
    key holds `T:`, which is how `build_game.once_tropes` knows it is
    guarded."""
    key = "[0, 0, 'T:kind:%s']" % kind
    return R.if_then(
        R.condition_script("!$gameSelfSwitches.value(%s)" % key),
        [S.trope()] + R.script(["$gameSelfSwitches.setValue(%s, true);"
                                % key]))


def party_lines(party):
    """The first of `party` who is with Bram has their say; nobody else."""
    out = []
    for actor_id, ws in reversed(party):
        out = R.if_then(R.condition_actor_in_party(actor_id), windows(ws),
                        out if out else None)
    return out


def commands(c, primary):
    """The page: count the look, then the first look, the `then` looks in
    order, and `again` for ever."""
    first = windows(c.look) + party_lines(c.party)
    if c.trope:
        first += trope_once(c.trope)
    first += list(c.loot)
    looks = [first] + [windows(t) for t in c.then]
    if c.again is not None:
        last, cap = windows(c.again), len(looks)
    elif c.then:
        # Round the `then` looks again: n counts 1..len(then) for ever.
        tail = [windows(t) for t in c.then]
        body = tail[-1]
        for i in range(len(tail) - 2, -1, -1):
            body = R.if_then(R.condition_script(
                "(this._curioN - 1) %% %d === %d" % (len(tail), i)),
                tail[i], body)
        return _count(primary, len(tail), wrap=True) + R.if_then(
            _nth(0), first, body)
    else:
        last, cap = windows(c.look), 1
    body = last
    for n in range(len(looks) - 1, -1, -1):
        body = R.if_then(_nth(n), looks[n], body)
    return _count(primary, cap) + body


def events(curios, first_id=FIRST_ID):
    """Every curio's events, numbered from `first_id`: one per answering
    cell, all with the first cell's commands."""
    out, eid = [], first_id
    for c in curios:
        cmds = commands(c, eid)
        for i, (x, y) in enumerate(c.cells):
            name = c.name if i == 0 else "%s (%d)" % (c.name, i + 1)
            note = "<curio>"
            if c.offset != (0, 0):
                note += "<offset:%d,%d>" % c.offset
            out.append(R.event(eid + i, name, x, y, [R.page(
                cmds, img=R.image(tile_id=c.sprite), trigger=0, priority=1,
                direction_fix=True, through=True)], note=note))
        eid += len(c.cells)
    return out


# ------------------------------------------------------------ the checks --

_names = {}


def _sheet_names(sheet):
    if sheet not in _names:
        import os
        p = os.path.join(os.path.dirname(R._data_dir()), "img", "tilesets",
                         sheet + ".txt")
        with open(p, encoding="utf-8") as fh:
            _names[sheet] = [l.split("|")[0].strip().lstrip("﻿")
                             for l in fh]
    return _names[sheet]


def tile_names(m, ts, x, y):
    """What is drawn on (x,y), by the sheets' own names: B-E on layers 1-3,
    and A5 on any layer."""
    w, h = m["width"], m["height"]
    found = set()
    for z in (0, 1, 2, 3):
        t = m["data"][(z * h + y) * w + x]
        if 0 < t < 1024 and z:
            sheet = ts["tilesetNames"][5 + t // 256]
        elif 1536 <= t < 1664:
            sheet, t = ts["tilesetNames"][4], t - 1536
        else:
            continue
        if sheet:
            names = _sheet_names(sheet)
            if t % 256 < len(names):
                found.add(names[t % 256])
    return found


def _flags(m, fl, x, y):
    w, h = m["width"], m["height"]
    for z in (3, 2, 1, 0):
        t = m["data"][(z * h + y) * w + x]
        yield fl[t] if t < len(fl) else 0


def _check(m, fl, x, y, bit):
    if not (0 <= x < m["width"] and 0 <= y < m["height"]):
        return False
    for f in _flags(m, fl, x, y):
        if f & 0x10:
            continue
        if (f & bit) == 0:
            return True
        if (f & bit) == bit:
            return False
    return False


DIRS = {2: (0, 1), 4: (-1, 0), 6: (1, 0), 8: (0, -1)}
BIT = {2: 1, 4: 2, 6: 4, 8: 8}
REV = {2: 8, 4: 6, 6: 4, 8: 2}


def walkable(m, fl, seeds):
    """Every cell the player can walk to from `seeds`, events ignored."""
    seen, todo = set(), []
    for s in seeds:
        if any(_check(m, fl, s[0], s[1], b) for b in (1, 2, 4, 8)):
            seen.add(s)
            todo.append(s)
    while todo:
        x, y = todo.pop()
        for d, (dx, dy) in DIRS.items():
            n = (x + dx, y + dy)
            if n not in seen and _check(m, fl, x, y, BIT[d]) and \
                    _check(m, fl, n[0], n[1], BIT[REV[d]]):
                seen.add(n)
                todo.append(n)
    return seen


def answerable(m, fl, reach, x, y):
    """Can the player press the action button at (x,y) from somewhere? From
    the next cell, or from the far side of a counter, which the button reaches
    over."""
    for dx, dy in DIRS.values():
        if (x + dx, y + dy) in reach:
            return True
        cx, cy = x + dx, y + dy
        if 0 <= cx < m["width"] and 0 <= cy < m["height"] and \
                next(_flags(m, fl, cx, cy)) & 0x80 and \
                (x + 2 * dx, y + 2 * dy) in reach:
            return True
    return False


def entrances():
    """(map id -> cells) every Transfer Player lands on, plus the start."""
    import json
    import os
    seeds = {}

    def scan(cmds):
        for c in cmds:
            if c["code"] == 201 and c["parameters"][0] == 0:
                p = c["parameters"]
                seeds.setdefault(p[1], set()).add((p[2], p[3]))
    for m in R.load("MapInfos.json"):
        if m:
            for ev in R.load_map(m["id"])["events"]:
                for page in (ev or {}).get("pages", []):
                    scan(page["list"])
    for ce in R.load("CommonEvents.json"):
        if ce:
            scan(ce["list"])
    system = R.load("System.json")
    seeds.setdefault(system["startMapId"], set()).add(
        (system["startX"], system["startY"]))
    return seeds


# ----------------------------------------------------------------- place --

def place(by_map, save=True):
    """Put `by_map` (map id -> list of curios) on the maps, checked. With
    `save=False`, only check, and leave `data/` alone."""
    tilesets = R.load("Tilesets.json")
    seeds = entrances()
    total = 0
    for map_id, curios in sorted(by_map.items()):
        m = R.load_map(map_id)
        ts = tilesets[m["tilesetId"]]
        taken = {(e["x"], e["y"]): e["name"] for e in m["events"] if e}
        assert max([e["id"] for e in m["events"] if e] + [0]) < FIRST_ID, \
            "Map%03d has events at %d or above" % (map_id, FIRST_ID)
        reach = walkable(m, ts["flags"], seeds.get(map_id, ()))
        mine = set()
        for c in curios:
            where = "Map%03d curio %r" % (map_id, c.name)
            for x, y in c.cells:
                assert (x, y) not in taken, "%s: (%d,%d) is already %r" % (
                    where, x, y, taken[(x, y)])
                assert (x, y) not in mine, "%s: (%d,%d) is two curios" % (
                    where, x, y)
                mine.add((x, y))
                drawn = tile_names(m, ts, x, y - c.hung)
                assert drawn & set(c.tile), \
                    "%s: (%d,%d) shows %s, not %s" % (
                        where, x, y - c.hung, sorted(drawn), list(c.tile))
            dead = [xy for xy in c.cells
                    if not answerable(m, ts["flags"], reach, *xy)]
            assert not dead, "%s: nobody can stand next to %s" % (
                where, dead)
        m["events"] = [e for e in m["events"] if e] + events(curios)
        if save:
            R.save_map(map_id, m)
        total += sum(len(c.cells) for c in curios)
    print("curios: %d events on %d maps" % (total, len(by_map)))


WAVES = ("curios_c1", "curios_c2", "curios_c3", "curios_c4",
         "curios_c5", "curios_c6", "curios_c6b")


def everything():
    """Every wave's curios, by map, in wave order."""
    import importlib
    by_map = {}
    for name in WAVES:
        for map_id, curios in importlib.import_module(name).ALL.items():
            by_map.setdefault(map_id, []).extend(curios)
    return by_map


def build(save=True):
    place(everything(), save=save)


def where(map_id, name):
    """Every cell on `map_id` showing tile `name`, and whether the player
    can answer it - for choosing a curio's cells. `python3 curios.py where
    22 Plumbing`."""
    tilesets = R.load("Tilesets.json")
    m = R.load_map(map_id)
    ts = tilesets[m["tilesetId"]]
    reach = walkable(m, ts["flags"], entrances().get(map_id, ()))
    for y in range(m["height"]):
        for x in range(m["width"]):
            if name in tile_names(m, ts, x, y):
                print("(%d, %d)%s" % (x, y, "  answerable" if answerable(
                    m, ts["flags"], reach, x, y) else ""))


if __name__ == "__main__":
    # python3 build/curios.py: check every curio against data/, write nothing.
    # python3 build/curios.py where MAP "Tile Name": cells and reach.
    import os
    import sys
    R.use_project(os.path.dirname(os.path.dirname(os.path.abspath(
        __file__))))
    if sys.argv[1:2] == ["where"]:
        where(int(sys.argv[2]), sys.argv[3])
    else:
        build(save=False)
