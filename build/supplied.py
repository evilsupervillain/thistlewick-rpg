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

# (sheet, cell, file). Nix replaces the face of `Actor3` 4 - her walking
# sprite and battler stay - so she matches them: masked, hooded, the same
# colours. The eight from 3 November replace generated or stock faces the same
# way, walking sprites and battlers unchanged; they came at 133 pixels and are
# scaled to the cell. `Supplied` was full at eight, so `Supplied2` follows it.
# Winnie's face and picture were replaced on 4 November with Mike's second
# go, closer to how the game describes her; same cell, so no data changed.
PORTRAITS = [
    (SHEET, 0, "nix_portrait.png"),                # Nix
    (SHEET, 1, "mrs_emberthwaite_portrait.png"),   # Mrs Emberthwaite
    (SHEET, 2, "wrong_dragon_portrait.png"),       # the Wrong Dragon, in the dark
    (SHEET, 3, "courier_portrait.png"),            # the Courier (3 Nov)
    (SHEET, 4, "winnie_marsden_portrait.png"),     # Winnie Marsden
    (SHEET, 5, "fizz_portrait.png"),               # Fizz
    (SHEET, 6, "ferrety_bother_portrait.png"),     # Ferrety Bother
    (SHEET, 7, "miss_moon_portrait.png"),          # Miss Moon
    ("Supplied2", 0, "mr_dray_portrait.png"),      # Mr Dray
    ("Supplied2", 1, "spare_cotterill_portrait.png"),   # Spare
    ("Supplied2", 2, "cotter_cotterill_portrait.png"),  # Cotter
]

# The whole portrait each face was cut from, 330x350 like the stock busts,
# copied into `img/pictures/` as the stock folder names them (the first three
# delivered later the same day):
# `<face sheet>_<cell + 1>.png`. Nothing in the game shows them.
PICTURES = {
    "nix_portrait.png": "nix_picture.png",
    "mrs_emberthwaite_portrait.png": "mrs_emberthwaite_picture.png",
    "wrong_dragon_portrait.png": "wrong_dragon_picture.png",
    "courier_portrait.png": "courier_picture.png",
    "winnie_marsden_portrait.png": "winnie_marsden_picture.png",
    "fizz_portrait.png": "fizz_picture.png",
    "ferrety_bother_portrait.png": "ferrety_bother_picture.png",
    "miss_moon_portrait.png": "miss_moon_picture.png",
    "mr_dray_portrait.png": "mr_dray_picture.png",
    "spare_cotterill_portrait.png": "spare_cotterill_picture.png",
    "cotter_cotterill_portrait.png": "cotter_cotterill_picture.png",
}


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
    # shadow round them; the earlier goes are beside them, unused. The
    # `_wall` files are those plates moved to the far side of their cells
    # (30 Oct), on the wall beside the fireplace rather than on its pillars.
    ("!$ThistlePortrait", "thistle_portrait_small.png", 48, False),  # village.py
    # The goose's body is rows 17-30 of its cell; 72 sets it on the mantel
    # shelf, which is the top 4 pixels of the fireplace's upper row; Mike
    # asked for it 3 pixels lower (29 Oct), so it sits just into the shelf.
    ("!$GooseTrophy", "goose_trophy.png", 69, False),          # south.py
    ("!$PlaqueLeft", "plaque_left_wall.png", 0, False),         # south.py
    ("!$PlaqueRight", "plaque_right_wall.png", 0, False),       # q_wren.py
    ("!$BottomlessBoard", "bottomless_board.png", 0, False),   # wilds.py
    ("!$SocksPlain", "socks_plain.png", 0, False),             # (the other)
    ("!$SocksOutlined", "socks_outlined.png", 0, False),       # wilds.py
    ("!$BarrowBench", "barrow_bench.png", 0, True),            # wilds.py
    ("!$MiddleBench", "middle_distance_bench.png", 0, True),   # field.py
    ("!$HeightMarks", "height_marks.png", 0, False),           # q_corvin.py
    # 4 November: the badger asleep in the pit, in place of `Nature` 0's
    # small black dog, and Washer on the end of Mrs Cotterill's bench.
    ("!$BadgerAsleep", "badger_sprite.png", 0, False),         # wilds.py
    ("!$Washer", "washer_sprite.png", 0, False),               # north.py
]


# Battlers, copied into `img/sv_enemies/` (the game is side view) as they came: (battler name, file).
BATTLERS = [
    ("Grimspite", "grimspite_battler.png"),  # db.EN_GRIMSPITE (29 Oct)
    ("Prophecy", "prophecy_battler.png"),    # db.EN_PROPHECY (29 Oct)
    # 4 November, each in place of a stock battler and its hue
    ("MilitantTurnip", "militant_turnip_battler.png"),  # db.EN_TURNIP
    ("TurnipGnome", "turnip_gnome_battler.png"),        # db.SPECIMENS
    ("SkeletonIntern", "skeleton_intern_battler.png"),  # db.EN_SKELETON
    ("TowerBat", "tower_bat_battler.png"),              # db.EN_BAT
    ("Badger", "badger_battler.png"),                   # db.EN_BADGER
    ("SmallHours", "small_hours_battler.png"),          # db.EN_SMALL_HOURS
    ("Echo", "echo_battler.png"),                       # db.EN_ECHO, Bram
    ("BarnCait", "barn_cait_battler.png"),              # db.SPECIMENS
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


def pictures():
    for sheet, cell, name in PORTRAITS:
        if name not in PICTURES:
            continue
        path = os.path.join(HERE, "..", "img", "pictures",
                            "%s_%d.png" % (sheet, cell + 1))
        subprocess.run(["convert", os.path.join(HERE, "supplied",
                                                PICTURES[name]),
                        "PNG32:" + path], check=True)
        print("wrote", os.path.normpath(path))


def main():
    sprites()
    battlers()
    pictures()
    for sheet in dict.fromkeys(s for s, _, _ in PORTRAITS):
        args = ["convert", "-size", "576x288", "xc:none"]
        for _, cell, name in (p for p in PORTRAITS if p[0] == sheet):
            x, y = cell % 4 * 144, cell // 4 * 144
            args += ["(", os.path.join(HERE, "supplied", name), "-filter",
                     "Lanczos", "-resize", "144x144!", ")", "-geometry",
                     "+%d+%d" % (x, y), "-composite"]
        path = os.path.join(HERE, "..", "img", "faces", sheet + ".png")
        subprocess.run(args + ["PNG32:" + path], check=True)
        print("wrote", os.path.normpath(path))


if __name__ == "__main__":
    main()
