"""Copies the character portraits the Thistle-pedia uses into the wiki.

    .venv/bin/python scripts/thistlepedia/portraits.py          # copy what changed
    .venv/bin/python scripts/thistlepedia/portraits.py --check  # exit 1 if any is stale
    .venv/bin/python scripts/thistlepedia/portraits.py --list   # who comes from where

The wiki has to be servable on its own, apart from the game, so it cannot link
into `img/` - it keeps its own copies in `thistlepedia/images/portraits/`.
This script is the only thing that writes them, and it is re-runnable: run it
again whenever a face or a picture changes and every copy is refreshed.

Who looks like whom is not decided here. `portraits.json` (next to this file)
names each portrait after the wiki page it is for and says which speaker in
`build/story.py`'s `FACES` it is - so the casting is read from the game itself,
and recasting somebody there recasts them here on the next run. An entry can
instead give an explicit `[sheet, index]` for somebody who has no line of
dialogue and so no entry in `FACES`, or `null` for somebody who is never in
the game at all and has only a portrait drawn for the wiki (Mother Ursula
Pym, dead since 1744) - which must then be in `art/`.

For each portrait the first of these that exists wins:

1. `scripts/thistlepedia/art/<Name>.png` - a portrait drawn for the wiki, if
   one is ever wanted that is not the in-game art;
2. `img/pictures/<sheet>_<index + 1>.png` - the full bust the game ships for
   that face (1-based, where `FACES` and MZ's `faceIndex` are 0-based);
3. the 144x144 cell cut out of `img/faces/<sheet>.png`, for the faces that
   have no bust yet (Nix's, which Mike drew, is one).

So when the finished pictures go into `img/pictures/` under the same names,
a rerun is the whole of the update.
"""
import ast
import json
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(GAME, "thistlepedia", "images", "portraits")
MANIFEST = os.path.join(HERE, "portraits.json")
ART = os.path.join(HERE, "art")

FACE_W = FACE_H = 144   # MZ's face cell; a face sheet is 4 across, 2 down


def story_faces():
    """`FACES` out of build/story.py, without importing it - the build needs
    the parent workspace's tools, and this script must not."""
    path = os.path.join(GAME, "build", "story.py")
    tree = ast.parse(open(path, encoding="utf-8").read(), path)
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "FACES" for t in node.targets):
            return ast.literal_eval(node.value)
    raise SystemExit("no FACES in build/story.py")


def resolve(name, entry, faces):
    """(sheet, index) for one manifest entry; (None, None) for wiki-only art."""
    if entry is None:
        return None, None
    if isinstance(entry, list):
        return entry[0], int(entry[1])
    if entry not in faces:
        raise SystemExit(f"{name}: '{entry}' is not a speaker in story.FACES")
    sheet, index = faces[entry]
    return sheet, int(index)


def render(name, sheet, index):
    """The portrait as a PIL image, and where it came from."""
    drawn = os.path.join(ART, name + ".png")
    if os.path.exists(drawn):
        return Image.open(drawn).convert("RGBA"), os.path.relpath(drawn, GAME)
    if sheet is None:
        raise SystemExit(f"{name}: no game face, and no art/{name}.png")
    bust = os.path.join(GAME, "img", "pictures", f"{sheet}_{index + 1}.png")
    if os.path.exists(bust):
        return Image.open(bust).convert("RGBA"), os.path.relpath(bust, GAME)
    sheet_path = os.path.join(GAME, "img", "faces", sheet + ".png")
    if not os.path.exists(sheet_path):
        raise SystemExit(f"{name}: no img/faces/{sheet}.png")
    x, y = (index % 4) * FACE_W, (index // 4) * FACE_H
    cell = Image.open(sheet_path).convert("RGBA").crop((x, y, x + FACE_W, y + FACE_H))
    return cell, os.path.relpath(sheet_path, GAME) + f" cell {index}"


def same(path, image):
    if not os.path.exists(path):
        return False
    old = Image.open(path).convert("RGBA")
    return old.size == image.size and old.tobytes() == image.tobytes()


def main(argv):
    check, listing = "--check" in argv, "--list" in argv
    faces = story_faces()
    manifest = json.load(open(MANIFEST, encoding="utf-8"))
    os.makedirs(OUT, exist_ok=True)
    wanted, stale = set(), []
    for name, entry in sorted(manifest.items()):
        if name.startswith("_"):
            continue
        sheet, index = resolve(name, entry, faces)
        image, source = render(name, sheet, index)
        target = os.path.join(OUT, name + ".png")
        wanted.add(name + ".png")
        if listing:
            print(f"{name:32} {source}")
        if not same(target, image):
            stale.append(name)
            if not check:
                image.save(target, optimize=True)
    orphans = sorted(f for f in os.listdir(OUT)
                     if f.endswith(".png") and f not in wanted)
    if check:
        for name in stale:
            print(f"stale: {name}.png")
        for f in orphans:
            print(f"not in portraits.json: {f}")
        return 1 if stale or orphans else 0
    for f in orphans:
        os.remove(os.path.join(OUT, f))
    print(f"{len(wanted)} portraits; {len(stale)} written, {len(orphans)} removed")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
