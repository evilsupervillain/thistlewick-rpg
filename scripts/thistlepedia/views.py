"""Photographs the places the Thistle-pedia describes, out of the running game.

    node ../tools/serve.js . 8766 &                       # the game, served
    .venv/bin/python scripts/thistlepedia/views.py          # every view
    .venv/bin/python scripts/thistlepedia/views.py Sump     # just these
    .venv/bin/python scripts/thistlepedia/views.py --from DIR   # finish shots already taken

`views.json` (next to this file) names each picture after the wiki page it is
for and says which map it is of. A bare `{"map": n}` is the whole map at once:
the game's screen is resized to the map before the transfer, so the camera
has nowhere to scroll and the shot is a plan of the place. A map too big for
that (the world map) gives `at` and `size` instead, a window of `size` tiles
centred on `at` - odd sizes, so the camera can centre on a tile. And
`{"picture": name}` is not a shot at all: `img/pictures/<name>.png`, copied
as it is (the great map at Coldbarrow, pins and all).

The party is made invisible, the map-name banner and the menu button are
turned off, and no event is allowed to start - Fizz meets you on arrival at
Firstfield, and a message left open there stops every transfer after it, so
the rest of the batch comes back as the same picture of Penultima. A view is
the place, and the people who are in it on a new game. The shots go through `../tools/shots.js` into a
scratch folder; here the black round an interior is cropped off and each one
is halved (24 pixels a tile) into `thistlepedia/images/views/`.

Unlike `portraits.py` this cannot say whether a copy is stale: the people in
a view walk about, so no two shots are byte for byte the same. Rerun it for a
place when its map changes.
"""
import json
import os
import subprocess
import sys
import tempfile

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.dirname(os.path.dirname(HERE))
WORKSPACE = os.path.dirname(GAME)
OUT = os.path.join(GAME, "thistlepedia", "images", "views")
MANIFEST = os.path.join(HERE, "views.json")
TILE = 48

SETUP = ("js:$gamePlayer.setTransparent(true); $gamePlayer.followers().hide();"
         " $gameSystem.disableEncounter(); $gameMap.disableNameDisplay();"
         " ConfigManager.touchUI = false;"
         " Game_Map.prototype.setupStartingEvent = function () { return false; };"
         " $gameMap._interpreter.clear();")


def shot_specs(views):
    """shots.js arguments for each view: resize the screen, then transfer."""
    specs = [SETUP]
    for name, view in views.items():
        data = json.load(open(os.path.join(GAME, "data", "Map%03d.json" % view["map"])))
        if "size" in view:
            (w, h), (x, y) = view["size"], view["at"]
            if not (w % 2 and h % 2):
                raise SystemExit(f"{name}: size {w}x{h} must be odd both ways")
        else:
            w, h = data["width"], data["height"]
            x, y = w // 2, h // 2
        specs.append(f"js:Graphics.resize({w * TILE}, {h * TILE});"
                     f" Graphics.boxWidth = {w * TILE}; Graphics.boxHeight = {h * TILE};")
        specs.append(f"{view['map']}:{x}:{y}:{name}")
    return specs


def finish(source, target):
    """Crop the black margin off, halve it, and write it into the wiki."""
    image = Image.open(source).convert("RGB")
    lit = image.point(lambda v: 255 if v > 8 else 0).convert("L")
    box = lit.getbbox()
    if box:
        image = image.crop(box)
    image = image.resize((image.width // 2, image.height // 2), Image.LANCZOS)
    image.save(target, optimize=True)
    return image.size


def finish_from(folder, names):
    """Finish shots already taken into `folder` (`--from DIR`)."""
    for name in names:
        w, h = finish(os.path.join(folder, name + ".png"), os.path.join(OUT, name + ".png"))
        print(f"{name}: {w}x{h}")


def main(argv):
    views = json.load(open(MANIFEST, encoding="utf-8"))
    views.pop("_comment", None)
    only = [a for i, a in enumerate(argv)
            if not a.startswith("-") and (i == 0 or argv[i - 1] != "--from")]
    if only:
        missing = [n for n in only if n not in views]
        if missing:
            raise SystemExit("not in views.json: " + ", ".join(missing))
        views = {n: views[n] for n in only}
    os.makedirs(OUT, exist_ok=True)
    for name in [n for n, v in views.items() if "picture" in v]:
        source = os.path.join(GAME, "img", "pictures", views.pop(name)["picture"] + ".png")
        Image.open(source).save(os.path.join(OUT, name + ".png"), optimize=True)
        print(f"{name}: {os.path.relpath(source, GAME)}")
    if not views:
        return
    if "--from" in argv:
        folder = argv[argv.index("--from") + 1]
        names = [n[:-4] for n in sorted(os.listdir(folder)) if n[:-4] in views]
        return finish_from(folder, names)
    with tempfile.TemporaryDirectory() as scratch:
        run = subprocess.run(["node", os.path.join(WORKSPACE, "tools", "shots.js"), scratch]
                             + shot_specs(views), cwd=WORKSPACE, text=True,
                             capture_output=True, timeout=1800)
        print(run.stdout.strip())
        failed = []
        for name in views:
            shot = os.path.join(scratch, name + ".png")
            if not os.path.exists(shot):
                failed.append(name)
                continue
            w, h = finish(shot, os.path.join(OUT, name + ".png"))
            print(f"{name}: {w}x{h}")
    if failed:
        raise SystemExit("no shot for: " + ", ".join(failed))


if __name__ == "__main__":
    main(sys.argv[1:])
