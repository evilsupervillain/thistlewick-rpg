"""The faces Mike drew, which the Character Generator cannot make.

`AUDIT.md` item 1's list, "The faces Mike supplies": each came as a 144x144
portrait, kept as he gave it in `build/supplied/`, and this puts them into one
face sheet of this game's own, `img/faces/Supplied.png`, in the cells
`story.FACES` names. Not part of the data build, like `art.py`: run it when a
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


def main():
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
