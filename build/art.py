"""Generated character art: which character is in which cell of which sheet.

The stock face and walking sheets are all spoken for (`NORTH.md` 4.6), so new
people are made with the Character Generator - headless, by `tools/chargen` in
the workspace - and installed into sheets of this game's own, named `Gen_*`
so a filename says it did not come in the box.

This is **not** part of `build_game.py`. The images it writes are committed
like any other art, and rendering them needs the editor's stock generator
parts, which live untracked in `../char-generator/stock/` - so the data build
stays runnable on a machine that has never seen them. Run this when a
character is added or their look changes:

    python3 build/art.py

Every settings file a character is rendered from is kept in `characters/`,
because it is the only copy of that look; `../char-generator/characters/`
holds the renders and is not tracked. Installing is additive: a cell that
holds someone else is refused, so a slot below is never reused. To change a
look on purpose, edit the settings and pass the slot with `--replace`.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.dirname(HERE)
INSTALL = os.path.join(os.path.dirname(GAME), "tools", "chargen", "install.py")

# sheet -> [(slot, settings file)]. Slots are the 0-based faceIndex /
# characterIndex the data uses. Append; never move anybody.
SHEETS = {
    "Gen_People1": [
        (0, "fizz.json"),               # Firstfield Meadow: Tutorial Sprite
        (1, "norbert-pelling.json"),    # the tutorial bandit
        (2, "old-hollis.json"),         # it's dangerous to go alone
        (3, "dilys-fenwick.json"),      # the sheep are not lost
        (4, "gideon-markup.json"),      # Penultima: Ye Final Shoppe
        (5, "dorothy-markup.json"),     # and the ledger
        # Restwell, and the last two cells of the sheet. `../SITES.md` step 1:
        # the Ashburys are the site, so they are the two that get drawn, and
        # step 2 opens a `Gen_People2`. Dr Pike shares `SF_Actor3:6` rather
        # than costing a sheet of his own - see `story.FACES`.
        (6, "mrs-ashbury.json"),        # Restwell: The Eight Hours
        (7, "walt-ashbury.json"),       # and the tune at the foot of the stairs
    ],
    "Gen_People2": [
        # Hithermost, `../SITES.md` step 2. Quillon's look is `../BIOS.md`'s
        # to the letter; Sir Dunstable is drawn here, an old knight with a
        # plume, because he is the bio's joke and a borrowed face would be
        # somebody else coming in at a quarter past four.
        (0, "brother-quillon.json"),    # Chapel of Continuance: the Book
        (1, "sir-dunstable.json"),      # two hundred and twelve times
        # Fairholme, `../SITES.md` step 3. Aldous is drawn here - the gold
        # circlet, the red robe and cape, a long white beard - because he
        # is the one who keeps posting the reward. Rosamund is `../BIOS.md`'s
        # look: the travelling cloak over the ball gown, because she has
        # learned.
        (2, "king-aldous.json"),        # half the kingdom, every time
        (3, "princess-rosamund.json"),  # the packed bag by the window
        # Olde Evermore, `../SITES.md` step 4. Mirabel's look is
        # `../BIOS.md`'s: silver hair and fringe, the circlet with the blue
        # stone, the purple and gold robe. The Elders share stock faces.
        (4, "mirabel.json"),            # Last Oracle; in bed by half seven
        # Gladhollow, `../SITES.md` step 5. Toby's look is `../BIOS.md`'s:
        # shirt and braces, the saucepan, the plaster from a paladin, and
        # enormous, eager eyes. Nobody else on that street needs a face.
        (5, "toby-gladhollow.json"),    # Official Welcomer; one sentence
    ],
}

# battlerName -> settings file. `install.py enemy` writes a stand-in only when
# no image is there, so real art dropped in under the same name is kept.
ENEMIES = {
    "Norbert_Pelling": "norbert-pelling.json",
}


def main(argv):
    extra = argv[1:]
    for sheet, slots in SHEETS.items():
        placements = ["%d=%s" % (slot, os.path.join(HERE, "characters", name))
                      for slot, name in slots]
        subprocess.run([sys.executable, INSTALL, "sheet", GAME, sheet]
                       + placements + extra, check=True)
    for battler, name in ENEMIES.items():
        subprocess.run([sys.executable, INSTALL, "enemy", GAME, battler,
                        os.path.join(HERE, "characters", name)], check=True)


if __name__ == "__main__":
    main(sys.argv)
