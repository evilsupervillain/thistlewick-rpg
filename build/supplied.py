"""The faces (and pictures, and battlers) Mike drew, which the Character Generator cannot make.

`AUDIT.md` item 1's list, "The faces Mike supplies": each came as a 144x144
portrait, kept as he gave it in `build/supplied/`, and this puts them into one
face sheet of this game's own, `img/faces/Supplied.png`, in the cells
`story.FACES` names - and the whole pictures in `SPRITES` into character
sheets of their own. Not part of the data build, like `art.py`: run it when a
portrait is added or replaced. **Append; never move anybody** - the index is
what the data points at.
"""

import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
SHEET = "Supplied"

# (cell, file). Nix replaces the face of `Actor3` 4 - her walking sprite and
# battler stay - so she matches them: masked, hooded, the same colours.
PORTRAITS = [
    (0, "nix_portrait.png"),                # Nix
    (1, "mrs_emberthwaite_portrait.png"),   # Mrs Emberthwaite
    (2, "wrong_dragon_portrait.png"),       # the Wrong Dragon, in the dark
]


# Whole pictures that become an event's sprite: (sheet, file, lift, clean).
# Each is a `!$` sheet, so its one frame is repeated in all twelve cells and
# the event looks the same whichever way it faces. The frame is the picture at
# its own size - the engine draws an event's frame at whatever size the sheet
# divides into, so a screen-sized picture is a screen-sized event - with
# `lift` pixels of nothing under it: a frame stands on the bottom of its
# event's cell, so that is how a picture on a wall hangs above the cell the
# player reads it from. `clean` drops pixels below a fifth opaque, for a
# drawing delivered with a faint frame round the edge of its cell.
SPRITES = [
    ("!$AirshipShadow", "airship_shadow.png", 0, False),  # the Hoyle Works
    # ART-TODO.md, delivered 28 October. The portrait and the plates are
    # Mike's smaller second goes (29 Oct), and the plates his third, with a
    # shadow round them; the earlier goes are beside them, unused.
    ("!$ThistlePortrait", "thistle_portrait_small.png", 48, False),  # village.py
    # The goose's body is rows 17-30 of its cell; 72 sets it on the mantel
    # shelf, which is the top 4 pixels of the fireplace's upper row; Mike
    # asked for it 3 pixels lower (29 Oct), so it sits just into the shelf.
    ("!$GooseTrophy", "goose_trophy.png", 69, False),          # south.py
    ("!$PlaqueLeft", "plaque_left_shadow2.png", 0, False),        # south.py
    ("!$PlaqueRight", "plaque_right_shadow.png", 0, False),       # q_wren.py
    ("!$BottomlessBoard", "bottomless_board.png", 0, False),   # wilds.py
    ("!$SocksPlain", "socks_plain.png", 0, False),             # (the other)
    ("!$SocksOutlined", "socks_outlined.png", 0, False),       # wilds.py
    ("!$BarrowBench", "barrow_bench.png", 0, True),            # wilds.py
    ("!$MiddleBench", "middle_distance_bench.png", 0, True),   # field.py
    ("!$HeightMarks", "height_marks.png", 0, False),           # q_corvin.py
]


# Battlers, copied into `img/sv_enemies/` (the game is side view) as they came: (battler name, file).
BATTLERS = [
    ("Grimspite", "grimspite_battler.png"),  # db.EN_GRIMSPITE (29 Oct)
    ("Prophecy", "prophecy_battler.png"),    # db.EN_PROPHECY (29 Oct)
]


def battlers():
    for battler, name in BATTLERS:
        path = os.path.join(HERE, "..", "img", "sv_enemies", battler + ".png")
        subprocess.run(["convert", os.path.join(HERE, "supplied", name),
                        "PNG32:" + path], check=True)
        print("wrote", os.path.normpath(path))


def sprites():
    for sheet, name, lift, clean in SPRITES:
        src = os.path.join(HERE, "supplied", name)
        frame = ["(", src]
        if clean:
            frame += ["-channel", "A", "-fx", "u<0.2?0:u", "+channel"]
        if lift:
            frame += ["-gravity", "south", "-splice", "0x%d" % lift,
                      "+gravity"]
        frame += [")"]
        row = ["("] + frame * 3 + ["+append", ")"]
        path = os.path.join(HERE, "..", "img", "characters", sheet + ".png")
        subprocess.run(["convert", "-background", "none"] + row * 4
                       + ["-append", "+repage", "PNG32:" + path], check=True,
                       stdout=subprocess.DEVNULL)  # -fx says "list"
        print("wrote", os.path.normpath(path))


def main():
    sprites()
    battlers()
    args = ["convert", "-size", "576x288", "xc:none"]
    for cell, name in PORTRAITS:
        x, y = cell % 4 * 144, cell // 4 * 144
        args += [os.path.join(HERE, "supplied", name), "-geometry",
                 "+%d+%d" % (x, y), "-composite"]
    path = os.path.join(HERE, "..", "img", "faces", SHEET + ".png")
    subprocess.run(args + ["PNG32:" + path], check=True)
    print("wrote", os.path.normpath(path))


if __name__ == "__main__":
    main()
