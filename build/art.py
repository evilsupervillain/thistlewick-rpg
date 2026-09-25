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
import glob
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.dirname(HERE)
INSTALL = os.path.join(os.path.dirname(GAME), "tools", "chargen", "install.py")
STOCK = os.path.join(os.path.dirname(GAME), "char-generator", "stock", "generator")

# Parts lent from one body type to another: (from, file stem, to). **The male
# parts have no hood** (`../CHARGEN.md`), and the Sable Hart's five are hooded
# men, so the female `AccB p10` riding hood is lent to the male body under the
# same id, which no male part uses - a hood is a hood, and it sits on a male
# head without an offset in every view. It is done by rendering against a copy
# of the stock generator made of symlinks, so nothing in `../char-generator/`
# changes and nobody drawn before is affected. The editor itself has no male
# `AccB p10`, so a settings file that uses it loads there without the hood.
BORROWED = [("Female", "AccB_p10", "Male")]

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
        # The Former Premises, `../SITES.md` step 6. Nobody wrote Hollowell's
        # look down, so he is drawn to `../WORLDMAP.md` 7.4's one rule - every
        # single thing he says is good news: a pressed suit and a tie, the
        # spectacles, and his eyes shut in contentment.
        (6, "prosper-hollowell.json"),  # Caretaker (Retained); delighted
        # The seven with no map, `../SITES.md` step 7, and the last cell of
        # the sheet. Elias Meech is the one of them drawn: a hill farmer in
        # the snow, the olive work coat, a brown hat with a grey band and a
        # grey beard. Everybody else at those seven shares a stock face, or
        # has none.
        (7, "elias-meech.json"),        # the Sky Anvil; between gates
    ],
    "Gen_People3": [
        # Tobias Frayne, `../SITES.md` step 8, and the first of a new sheet.
        # Nobody wrote his look down, so he is drawn to `../COMPANIONS.md`'s
        # one line - revived eleven times and delighted about it: the shirt
        # of a man who lives on the coast road, a moustache, an open grin,
        # and a scar on the cheek.
        (0, "tobias-frayne.json"),      # the coast road; eleven times
        # Frostwick, `../SITES.md` step 10: all six of `../WORLDMAP.md`
        # 7.3's cast, drawn to its lines. Perce in a red coat with a white
        # fur collar, which is the Festival's; Ida in a shawl, amused; Clem
        # in a winter coat; Mrs Blagg in spectacles and the committee's
        # navy and gold; Miss Pargeter in pale ice-blue and practical
        # spectacles, and no pointed hat; Mrs Marchpane in the inn's cap.
        (1, "perce-stagg.json"),        # Frostwick: broke it; opens it
        (2, "ida-stagg.json"),          # thinks it is very funny
        (3, "clem-blagg.json"),         # aged seven; has read the minutes
        (4, "wilhelmina-blagg.json"),   # chair of the Festival committee
        (5, "eudora-pargeter.json"),    # retained; refrigeration
        (6, "tibby-marchpane.json"),    # the Eleven Days
        # Chapter Clerk Mordaunt, `../SITES.md` step 11, and the last cell
        # of the sheet. Nobody wrote his look down, so he is drawn to
        # `../COMPANIONS.md` L6's one line - nine pins, one knight, a
        # committee, a review: grey, the oldest face, a trimmed beard,
        # half-rim reading glasses, and the Order's black coat with the
        # purple lining. The next person drawn opens `Gen_People4`.
        (7, "mordaunt.json"),           # Coldbarrow; the great map
    ],
    "Gen_People4": [
        # The Sable Hart, `../SITES.md` step 12: five doomed rivals, which is
        # the whole joke, drawn as five variations on one look - `BORROWED`'s
        # hood over cloak `p03` and clothing `p25`, all three in one colour -
        # and told apart at sprite size by the colour of the hood, the hair
        # under it and one thing each: the Secretary's moustache, the
        # editor's spectacles, the statistician's beard, the scar, the grin.
        (0, "hollin-crake.json"),       # Secretary; keeps the rota
        (1, "lucan-morrow.json"),       # edits the newsletter
        (2, "thaddeus-rook.json"),      # keeps the league table
        (3, "silas-veyle.json"),        # has the darkest corner this week
        (4, "kit-blackwood.json"),      # newest; on the waiting list
    ],
}

# battlerName -> settings file. `install.py enemy` writes a stand-in only when
# no image is there, so real art dropped in under the same name is kept.
ENEMIES = {
    "Norbert_Pelling": "norbert-pelling.json",
}


def generator(tmp):
    """The stock generator with `BORROWED` added, as a tree of symlinks."""
    for view in os.listdir(STOCK):
        src = os.path.join(STOCK, view)
        dst = os.path.join(tmp, view)
        if not os.path.isdir(src):
            os.symlink(src, dst)
            continue
        os.mkdir(dst)
        for body in os.listdir(src):
            if not any(body == to for _, _, to in BORROWED):
                os.symlink(os.path.join(src, body), os.path.join(dst, body))
                continue
            os.mkdir(os.path.join(dst, body))
            for f in os.listdir(os.path.join(src, body)):
                os.symlink(os.path.join(src, body, f), os.path.join(dst, body, f))
            for frm, stem, to in BORROWED:
                if to != body:
                    continue
                for f in glob.glob(os.path.join(src, frm, "*_%s*" % stem)):
                    os.symlink(f, os.path.join(dst, body, os.path.basename(f)))
    return tmp


def main(argv):
    with tempfile.TemporaryDirectory() as tmp:
        run(argv, generator(tmp))


def run(argv, gen):
    extra = argv[1:] + ["--generator", gen]
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
