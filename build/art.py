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

# Parts lent from one body type to another: (from, file stem, to[, stem]),
# the last when the part takes another id on its new body. **The male parts
# have no hood** (`../CHARGEN.md`), and the Sable Hart's five are hooded
# men, so the female `AccB p10` riding hood is lent to the male body under the
# same id, which no male part uses - a hood is a hood, and it sits on a male
# head without an offset in every view. It is done by rendering against a copy
# of the stock generator made of symlinks, so nothing in `../char-generator/`
# changes and nobody drawn before is affected. The editor itself has no male
# `AccB p10`, so a settings file that uses it loads there without the hood.
#
# **The female parts have no goggles** either, and Thistlewick's smithy
# apprentice is drawn in the brass pair she wore on the stock `People2:7`
# face. The male `AccB p06` is that pair, pushed up on the head, and it is
# lent to the female body as `AccB p11`, an id the female parts stop short
# of, because female `p06` is a crown. The editor loads her without them.
BORROWED = [("Female", "AccB_p10", "Male"),
            ("Male", "AccB_p06", "Female", "AccB_p11")]

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
        # Little Gore and Sump, `../SITES.md` step 13: one face each. Nobody
        # wrote either look down. Mrs Vane is drawn to `../COMPANIONS.md`'s
        # one line - married nine years, three children, delighted: her hair
        # up out of the way, a village dress and an open smile. The Parish
        # Clerk of Sump is drawn to MER-5's symptoms - headache, irritability,
        # poor sleep - in a waistcoat and a hat against the sun, with a frown
        # and the eyes of a man who has not slept since 1794.
        (5, "hester-vane.json"),        # Little Gore; married nine years
        (6, "parish-clerk-sump.json"),  # cannot allocate the wasps
        # Ashcombe, `../SITES.md` step 14, and the last cell of the sheet.
        # Mrs Ash is Corvin's mother, so she is drawn from his portrait
        # (`Actor1` 4): his brown hair, swept across the same way and put up
        # in a bun behind, his red-brown eyes - and a smile he has never
        # once worn - in a lilac knitted dress.
        (7, "mrs-ash.json"),            # fine; has a new kitchen; knits
    ],
    "Gen_People5": [
        # Ashcombe's other face, and the first of a new sheet. The Drainage
        # Museum's curator is `../COMPANIONS.md`'s one word - proud: grey
        # side-whiskers, round spectacles, a broad grin and the navy coat
        # with the gold frogging, which is the nearest thing in the box to
        # a parish in its best.
        (0, "hubert-weir.json"),        # the Drainage Museum; proud
        # Weeping Bottom, `../SITES.md` step 15: the Sisterhouse. Both are
        # of Merribell's world, so both wear her hood (`accb p04`) and the
        # white habit that goes with it (`clothing p04`). The white of either
        # cannot be recoloured, which suits a schism: the Prioress is in the
        # Order's blue trim, drawn, grey-haired and patient; Sister Bewick of
        # What Ought To Work is the same habit with every trim dyed black,
        # younger, dark-haired and entirely sincere.
        (1, "prioress-stope.json"),     # runs it; has begun holding symposia
        (2, "sister-bewick.json"),      # losing patients, winning arguments
        # Fenmarch Hall, `../SITES.md` step 16. The Fourth is Aldric's
        # family, so he is drawn from Aldric's portrait (`Actor3` 6): the
        # same blue-black hair, the same blue eyes, and the blue-and-gold
        # coat over silver plate - the knight Aldric was meant to look like,
        # at nineteen, open-mouthed with enthusiasm. Mr Ottershaw is the
        # oldest face, wild white hair, a pointed moustache, a sly grin and
        # green-tinted working lenses, in a craftsman's waistcoat.
        (3, "pemberton-gore-iv.json"),  # nineteen, magnificent
        (4, "mr-ottershaw.json"),       # ninety, unrepentant, an artist
        # The Collegium Arcanum, `../SITES.md` step 17, and the last three
        # cells of the sheet. The Head Porter holds the real power and is
        # dressed for it: a dark suit, a full ginger beard and a mouth that
        # has never once been surprised. Sub-Librarian Prewitt is correct in
        # every particular - a black bob, dark spectacles, a navy jacket and
        # a tie. Dean Fenwold is fine: silver hair swept back, a walrus
        # moustache, the Collegium's white-and-purple robe, and the smile of
        # a man with a talk to give.
        (5, "head-porter-gedge.json"),  # the Porter's Lodge; the real power
        (6, "sub-librarian-prewitt.json"),  # immovable, courteous, correct
        (7, "dean-fenwold.json"),       # is fine; has a talk about it
    ],
    "Gen_People6": [
        # Great Dunnage, `../SITES.md` step 18: municipal self-regard, dressed
        # for it. The Mayor in scarlet with a plumed hat, which is the most
        # hat in the game. The Prime Warden of the Company of Smiths in black
        # with gold at the collar, iron-grey and pinned up. Wharfinger Tibbs,
        # grey, bearded, in half-rims and a wharf coat, patient for eleven
        # years. Mrs Harbottle, who chairs the Bell's panel, ginger and in
        # gold lace. Appraiser Fettle, round spectacles and an orange working dress,
        # enthusiastic about the tang. The horse is a sprite, not a face.
        (0, "mayor-gristwood.json"),    # reading the preamble
        (1, "prime-warden-stannard.json"),  # has a schedule of what is a piece
        (2, "wharfinger-tibbs.json"),   # has held a coat for eleven years
        (3, "judge-harbottle.json"),    # chairs the Bell's panel
        (4, "appraiser-fettle.json"),   # enthusiastic about the tang
        # Thistlewick's gossip, Map 1 - `AUDIT.md` G3. Written as "she" and
        # drawn as the Villager boy, People1:0, since the game shipped; the
        # one unused stock woman is a child in a red riding hood. A kerchief
        # and a print dress, and a face that has heard the second vote.
        (5, "thistlewick-gossip.json"),  # the goat abstained
        # Olde Evermore's two Elders - `AUDIT.md` item 3. They were stock,
        # Actor3:0 and Nature:6, a round-eared swordsman and a spirit whose
        # hair hides her ears, and the village is written as elves. Drawn
        # with the pointed ears showing, and old: "visibly older than she
        # looks". Faelan silver, long, a gold bead; Lirien lilac, a circlet.
        (6, "elder-faelan.json"),       # sent for things on the top shelf
        (7, "elder-lirien.json"),       # translates; the pudding is urgent
    ],
    # `AUDIT.md` item 1: every human who spoke with no face gets one, face
    # and walking sprite from the one file, and the event reads both from
    # `story.FACES`. Weeping Bottom's eight first. The Sisters of Whatever
    # Works share a uniform - white kerchief cap, blue dress, white collar -
    # and are two women in it; Sir Hamo is a knight in a white surcoat.
    "Gen_People7": [
        (0, "sister-pim.json"),         # deep breaths, everybody
        (1, "sister-lamb.json"),        # leek; it works
        (2, "mrs-liddy.json"),          # never had so much of it
        (3, "mr-crouch.json"),          # lovely and bracing
        (4, "mr-oakes.json"),           # only visiting
        (5, "sir-hamo.json"),           # in the field, fourteen years
        (6, "mr-nuttall.json"),         # crossed Wednesday
        (7, "mr-dace.json"),            # day four of the correct treatment
    ],
    # Great Dunnage's eight: the gate, the yard, the Smiths' Hall, the
    # Counting House and the Bell. Mr Tweddle is the next sheet's.
    "Gen_People8": [
        (0, "watchman-dunnage.json"),   # Forty-eight what?
        (1, "mrs-poskitt.json"),        # like that, but nine times
        (2, "mr-plummer.json"),         # anything, anywhere, by Tuesday
        (3, "warden-crabbe.json"),      # reads the Schedule out
        (4, "town-clerk-dunnage.json"), # Form L, sir
        (5, "mrs-dewhirst.json"),       # you'll be judged at breakfast
        (6, "mr-ambler.json"),          # Nine!
        (7, "miss-quayle.json"),        # Two.
    ],
    # Dunnage's ninth, Little Gore and Sump, and the Sable Hart's landlady.
    # The three Vanes are drawn as the children the narration says they are.
    "Gen_People9": [
        (0, "mr-tweddle.json"),         # a thrush that's lost its keys
        (1, "dame-winifred-cope.json"), # nothing to report; lovely
        (2, "bess-vane.json"),          # I'm Mum. I mean the bride
        (3, "alfie-vane.json"),         # I'm Dad; I look pleased
        (4, "nell-vane.json"),          # I'm everybody else
        (5, "mr-gammage.json"),         # trying to get off since Tuesday
        (6, "mrs-pardew.json"),         # things used to be better
        (7, "mrs-garrow.json"),         # sit anywhere in the middle
    ],
    # The Collegium, Gladhollow, Ashcombe and the Cinder Fen. The
    # Commissioner's sprite is drawn and unused: the Fen has no event sprite.
    "Gen_People10": [
        (0, "dr-hapgood.json"),         # nearly there; never there
        (1, "collegium-reader.json"),   # asked for a book at Michaelmas
        (2, "collegium-undergraduate.json"),  # grace is at six
        (3, "ned-gladhollow.json"),     # farewell from Gladhollow!
        (4, "granny-wendle.json"),      # my knees
        (5, "wilf-ashcombe.json"),      # there's no puddles
        (6, "mrs-dimmock.json"),        # every letter answered
        (7, "drainage-commissioner.json"),  # are you a fire person?
    ],
    # The last three of item 1, then the companion quests (`QUESTS.md` 1).
    # Full.
    "Gen_People11": [
        (0, "mrs-puddifoot.json"),      # Friday to Wednesday
        (1, "tom-fenmarch.json"),       # four miles, both ways
        (2, "evermore-raker.json"),     # mind the leaves
        # HOB-3, the anvil: two of Crooke's apprentices, week four. Hodge
        # is in the syllabus bandana, as Norbert is; Ivy writes a good hand.
        (3, "ivy-scrope.json"),         # very sorry
        (4, "hodge-arkwright.json"),    # less so
        # NIX-5, half an encounter: the Works Band's first bassoon, who has
        # to be got through the Gloamwood at night without a fight.
        (5, "enoch-bagshawe.json"),     # the reed
        # WRE-3, the Gloamwood Society: the chair and the secretary.
        (6, "hester-lumb.json"),        # it's always tonight
        (7, "cyril-dunmore.json"),      # second pencil
    ],
    # The companion quests, continued.
    "Gen_People12": [
        (0, "edith-pellow.json"),       # WRE-3: I counted nine
        # ROL-3, the Fairweather alumni: six of the eleven parties.
        (1, "dame-florence-ickworth.json"),  # he was my page, at eleven
        (2, "brother-anselm.json"),     # the Seven Bells
        (3, "mags-turvey.json"),        # the siege kitchen
        (4, "pim-corrow.json"),         # the heir, found
        (5, "odile-marchbank.json"),    # the Ninth Lancers
        (6, "old-jory.json"),           # the last survey
        (7, "septimus-dray.json"),      # PIP-3: Instrumental (Other Wind)
    ],
    "Gen_People13": [
        (0, "lettice-moon.json"),       # PIP-3: Ballad (Sad)
        (1, "convenor-swale.json"),     # ROL-1: the Convenor
        (2, "registrars-clerk-pennock.json"),  # ZEPH-1: he looked her up
        # WRE-1: two of Rowbotham's three students, her reviewers again.
        (3, "professor-mott.json"),     # forty years a beetle
        (4, "doctor-furze.json"),       # it's a goose
        # MER-3, the Healers' Table: four of the five (Ysolde is the fifth).
        (5, "grizel-pennyfeather.json"),  # a femur and a church candlestick
        (6, "lucius-hobday.json"),      # a barbarian and a lute string
        (7, "nan-gilly.json"),          # a wizard and his own staff
    ],
    "Gen_People14": [
        (0, "cuthbert-spence.json"),    # MER-3: a paladin's sash
        (1, "ambrosine-quill.json"),    # PIP-1: the Authorised Version
        (2, "cobb-lorrimer.json"),      # NIX-3: steals things, and says so
        (3, "maud-penhallow.json"),     # ROL-5: the understudy, sixteen
        # Two Cotterills off the stock sheets, at Mike's request. Spare's
        # `SF_People1` 0 has no side-view battler and F1 needs one, so he is
        # redrawn whole - the same lad, blue-black hair, pale blue - and his
        # face, sprite and battler match. Cotter's `SF_Actor2` 7 read as a
        # woman; he is Rivet's brown hair and white work jacket, older.
        (4, "spare-cotterill.json"),    # F1: aged nine, a bag packed
        (5, "cotter-cotterill.json"),   # the Iron Company's gate, Saturdays
        # SPA-1: the post, the same man every time, already there. Red coat,
        # grey flat cap (male AccB p07, the bandana, reads as one in the
        # sprite); no part in the generator is a satchel.
        (6, "the-courier.json"),        # F2: on his rounds
        # SPA-4, Much Pottering: the pen pal, ginger plaits and a plaster.
        (7, "effie-gotobed.json"),      # F3: nine, and a volcano
    ],
    "Gen_People15": [
        # SPA-4: the rest of Much Pottering that speaks.
        (0, "mrs-gotobed.json"),        # Effie's mother
        (1, "mr-dibble.json"),          # wet paint, and the bonfire
        (2, "mrs-throssell.json"),      # chair of the parish council
        (3, "mr-cobley.json"),          # thirty years after one carp
        # P3, Olde Evermore's elves about doing things (`QUESTS.md`): the
        # pointed ears showing in the portrait as well as the sprite - male
        # front hair p03 hides them under a hat or a bandana, p02/p05/p12
        # do not. Thalion green robe and spectacles; Aelwen the travelling
        # cloak over the cream dress; Elowen silver, older, Lirien's mother.
        (4, "evermore-judge.json"),     # five point eight
        (5, "evermore-bard.json"),      # the Lay, three days long
        (6, "evermore-knitter.json"),   # a tea cosy
        (7, "evermore-fisher.json"),    # one fish, since the Second Age
    ],
    "Gen_People16": [
        # P3, continued. Ninian ginger under a bandana, in a teal coat; the
        # copyist bearded, in a scribe's blue.
        (0, "evermore-sweeper.json"),   # the path nobody comes in by
        (1, "evermore-copyist.json"),   # told to copy everything
        # Faces that were shared (Mike, 3 Nov). Mr Pilbeam had Hosea's,
        # spectacles and all, so he keeps the spectacles; the smithy's
        # apprentice had Ott's, so she keeps the brass goggles (`BORROWED`)
        # and nothing else. The other four each wore the face of somebody
        # Mike named to keep it: the Hermit, Mrs Barrow, Halbert Quy, Sops.
        (2, "mr-pilbeam.json"),         # only passing; there was an eagle
        (3, "smithy-apprentice.json"),  # does not talk to the hammers
        (4, "committee-clerk.json"),    # Form C-12
        (5, "mrs-budge.json"),          # the half a kingdom, in the orchard
        (6, "thistlewick-old-man.json"),  # Forty-seven was his boy
        (7, "thistlewick-child.json"),  # there's a DUNGEON
    ],
    "Gen_People17": [
        # The same, continued: Tibb's (the Hithermost villager, Ned Scarrow),
        # Number Forty-Six's (the Turnip's regular, the man having a day off,
        # Major Royce) and the Hermit's (Fellow Grice).
        (0, "hithermost-villager.json"),  # we do teas
        (1, "turnip-regular.json"),     # his cousin was the Thirty-Ninth
        (2, "man-day-off.json"),        # thirty-one years, and today off
        (3, "fellow-grice.json"),       # sends his apologies
        (4, "ned-scarrow.json"),        # the twelfth dive was Roland
        (5, "major-royce.json"),        # the Glass Fort
        # Saul Pennock, who wore the Merchant's face (Mike, 3 Nov).
        (6, "saul-pennock.json"),       # never had a better crew. Hm.
    ],
}

# battlerName -> settings file. `install.py enemy` writes a stand-in only when
# no image is there, so real art dropped in under the same name is kept.
ENEMIES = {
    "Norbert_Pelling": "norbert-pelling.json",
    "Septimus_Dray": "septimus-dray.json",          # PIP-3
    "Lettice_Moon": "lettice-moon.json",            # PIP-3
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
            if not any(body == b[2] for b in BORROWED):
                os.symlink(os.path.join(src, body), os.path.join(dst, body))
                continue
            os.mkdir(os.path.join(dst, body))
            for f in os.listdir(os.path.join(src, body)):
                os.symlink(os.path.join(src, body, f), os.path.join(dst, body, f))
            for frm, stem, to, *rename in BORROWED:
                if to != body:
                    continue
                for f in glob.glob(os.path.join(src, frm, "*_%s*" % stem)):
                    name = os.path.basename(f)
                    if rename:
                        name = name.replace(stem, rename[0])
                    os.symlink(f, os.path.join(dst, body, name))
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
