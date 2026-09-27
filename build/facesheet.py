"""Every face beside its walking sprite and what the text says the person is.

AUDIT.md items 4, 3 and 2 all start from the same picture: a face, the sprite
the same person walks about as, and the words the game uses about them. This
builds it off the finished data rather than off the modules, so it shows what
ships:

    python3 build/facesheet.py OUT_DIR            # faces.tsv and sheet-NN.png

For each name in `story.FACES` it finds the event pages whose Show Text uses
that face with that name in the speaker label, takes the page's character
graphic as the sprite (the down-facing middle frame), and gathers the
narration in those events that reads as a description - "A woman with a slide
rule", "a small boy with a saucepan" - with a crude he/she count beside it.
The count is a hint for a person reading the sheet, not a verdict: narration
in a scene with two people in it counts both.

Needs ImageMagick (`convert`, `montage`) on the path. Not part of the build.
"""

import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import story  # noqa: E402

LABEL = re.compile(r"\\C\[6\]([^\\]+?):\\C\[0\]")
HE = re.compile(r"\b(he|him|his|himself|man|boy|lad|gentleman)\b", re.I)
SHE = re.compile(r"\b(she|her|hers|herself|woman|girl|lady)\b", re.I)
INTRO = re.compile(r"^(An? |The |On a |At the )", re.I)


def load(name):
    with open(os.path.join(ROOT, "data", name)) as f:
        return json.load(f)


def scan():
    """(face, index) -> speaker -> list of (where, sprite, intro, he, she)."""
    infos = load("MapInfos.json")
    found = {}
    for info in infos:
        if not info:
            continue
        mid = info["id"]
        path = os.path.join(ROOT, "data", "Map%03d.json" % mid)
        if not os.path.exists(path):
            continue
        for ev in load("Map%03d.json" % mid)["events"]:
            if not ev:
                continue
            for pi, page in enumerate(ev["pages"]):
                cmds = page["list"]
                texts = [c["parameters"][0] for c in cmds if c["code"] == 401]
                narr = [t for t in texts if not LABEL.search(t)]
                intro = " ".join(t for t in narr[:3] if INTRO.match(narr[0]))
                he = sum(len(HE.findall(t)) for t in narr)
                she = sum(len(SHE.findall(t)) for t in narr)
                img = page["image"]
                sprite = (img["characterName"], img["characterIndex"])
                for k, c in enumerate(cmds):
                    if c["code"] != 101 or not c["parameters"][0]:
                        continue
                    face = (c["parameters"][0], c["parameters"][1])
                    nxt = cmds[k + 1]["parameters"][0] if k + 1 < len(cmds) else ""
                    m = LABEL.search(nxt)
                    who = m.group(1) if m else "?"
                    where = "Map%03d ev%d %s p%d" % (mid, ev["id"], ev["name"], pi)
                    found.setdefault(face, {}).setdefault(who, []).append(
                        (where, sprite, intro, he, she))
    return found


def crop_face(sheet, i, out):
    x, y = (i % 4) * 144, (i // 4) * 144
    subprocess.run(["convert", os.path.join(ROOT, "img/faces", sheet + ".png"),
                    "-crop", "144x144+%d+%d" % (x, y), "+repage", out],
                   check=True)


def crop_sprite(name, i, out):
    src = os.path.join(ROOT, "img/characters", name + ".png")
    w, h = map(int, subprocess.check_output(
        ["identify", "-format", "%w %h", src]).split())
    if name.startswith("$") or name.startswith("!$"):
        cw, ch, ox, oy = w // 3, h // 4, 0, 0
    else:
        cw, ch = w // 12, h // 8
        ox, oy = (i % 4) * cw * 3, (i // 4) * ch * 4
    subprocess.run(["convert", src, "-crop",
                    "%dx%d+%d+%d" % (cw, ch, ox + cw, oy), "+repage",
                    "-filter", "point", "-resize", "96x96", out], check=True)


def main(out):
    os.makedirs(out, exist_ok=True)
    found = scan()
    actors = load("Actors.json")
    rows = []
    for name, (sheet, i) in story.FACES.items():
        uses = found.get((sheet, i), {})
        mine = uses.get(name, [])
        sprite = next((u[1] for u in mine if u[1][0]), None)
        if sprite is None:
            for a in actors:
                if a and a["faceName"] == sheet and a["faceIndex"] == i:
                    sprite = (a["characterName"], a["characterIndex"])
        intro = next((u[2] for u in mine if u[2]), "")
        he = sum(u[3] for u in mine)
        she = sum(u[4] for u in mine)
        others = sorted(k for k in uses if k != name)
        rows.append((name, sheet, i, sprite, he, she, intro, others,
                     [u[0] for u in mine]))

    with open(os.path.join(out, "faces.tsv"), "w") as f:
        f.write("name\tface\tsprite\the\tshe\tintro\tshared with\twhere\n")
        for name, sheet, i, sprite, he, she, intro, others, where in rows:
            f.write("\t".join([
                name, "%s:%d" % (sheet, i),
                "%s:%d" % sprite if sprite else "-", str(he), str(she),
                intro, ", ".join(others), "; ".join(where[:3])]) + "\n")

    tiles = []
    tmp = tempfile.mkdtemp()
    for n, (name, sheet, i, sprite, he, she, *_rest) in enumerate(rows):
        face = os.path.join(tmp, "f%03d.png" % n)
        crop_face(sheet, i, face)
        spr = os.path.join(tmp, "s%03d.png" % n)
        if sprite and sprite[0]:
            crop_sprite(sprite[0], sprite[1], spr)
        else:
            subprocess.run(["convert", "-size", "96x96", "xc:gray50", spr],
                           check=True)
        tile = os.path.join(tmp, "t%03d.png" % n)
        label = "%s\n%s:%d  %s\nhe %d / she %d" % (
            name, sheet, i, ("%s:%d" % sprite) if sprite and sprite[0] else "-",
            he, she)
        subprocess.run(["convert", face, spr, "-background", "gray50",
                        "-gravity", "center", "+append",
                        "-gravity", "south", "-splice", "0x44",
                        "-font", "DejaVu-Sans", "-pointsize", "12",
                        "-fill", "white", "-annotate", "+0+2", label, tile],
                       check=True)
        tiles.append(tile)
    for s in range(0, len(tiles), 24):
        subprocess.run(["montage"] + tiles[s:s + 24] +
                       ["-tile", "6x", "-geometry", "+4+4",
                        "-background", "gray30",
                        os.path.join(out, "sheet-%02d.png" % (s // 24))],
                       check=True)
    print("%d faces, %d sheets, in %s" % (len(rows), (len(tiles) + 23) // 24,
                                          out))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "/tmp/facesheet")
