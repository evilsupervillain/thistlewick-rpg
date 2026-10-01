"""Shared event-building helpers: how people talk, how doors work, and the
running gag that counts clichés.

The point of `say` is that dialogue in the map scripts reads as dialogue -
a speaker, a face, and the lines - instead of as a pile of command dicts.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import db
import mapkit as K
import rmmzdata as R

# Faces, by the person they belong to, so nobody has to remember that the
# blacksmith is Actor2 index 4.
FACES = {
    # Party members share their face sheet with their walking sprite - bar
    # Nix, whose face Mike drew (`supplied.py`, NORTH.md 8.1e): `Actor3` 4
    # read as a boy, and she is a woman. Her sprite is still `Actor3` 4.
    "Bram": ("Actor1", 0), "Merribell": ("Actor1", 7), "Hob": ("Actor2", 4),
    "Zephyrine": ("Actor1", 5), "Nix": ("Supplied", 0), "Aldric": ("Actor3", 6),
    "Piper": ("Actor2", 3),
    "Corvin": ("Actor1", 4), "Wren": ("Actor2", 7), "Roland": ("Actor2", 2),
    # Villagers. The stock People sheets are typecast harder than you would
    # expect - People3 is entirely royalty, so nobody in Thistlewick uses it.
    "Gatekeeper": ("People1", 2),
    "Elder Wispel": ("People1", 6),
    "Clerk": ("People2", 0),
    "Mother": ("People1", 5),
    "Villager": ("People1", 0),
    # Thistlewick's gossip is also "Villager" on screen and is not
    # Hithermost's: `say(..., face="Gossip")`. She had People1:0 too, the
    # spiky-haired boy, under "She lets that sit" - AUDIT.md G3, a repair in
    # NORTH.md 8.1c. Drawn, because the one unused stock woman is a child in
    # a red hood. Hithermost's villager is never given a pronoun and keeps it.
    "Gossip": ("Gen_People6", 5),
    "Neighbour": ("People1", 1),
    "Councillor": ("People1", 3),
    "Councillor Fenn": ("People4", 2),
    "Old Man": ("People4", 4),
    "Farmer": ("People2", 6),
    "Fisher": ("People1", 4),
    "Child": ("People2", 2),
    "Innkeeper": ("People2", 3),
    "Merchant": ("People2", 4),
    "Apprentice": ("People2", 7),
    "Shopkeeper": ("People4", 3),
    "Regular": ("People4", 6),
    # Nether Sopping. People3 is the royalty sheet, which is why the amnesiac
    # who does not know she is a princess is drawn from it, and why the two
    # "very ordinary travellers" in the corner are as well.
    "Dorcas": ("People4", 5),
    "Prudence": ("People2", 3),
    "Hosea": ("People4", 0),
    "Ysolde": ("People1", 7),
    "Hulda": ("People2", 1),
    "Nabb": ("People4", 7),
    "Tolly": ("People2", 5),
    "Merrow": ("People3", 6),
    "Dree": ("People3", 5),
    "Perpetua": ("People3", 3),
    "Pell": ("People3", 7),
    "Mrs Barrow": ("People4", 1),
    "Bother": ("People3", 4),
    # #45 is written as a man in his seventies, four stone heavier than his
    # portrait in Prophecy Hall. Every old man on the People sheets is spoken
    # for, so he shares one: People4:4, with the old man in Thistlewick square
    # forty miles north, who is the least likely of the five to be next to him
    # in a player's memory. The Hermit gave the face up to him.
    "Halbert Quy": ("People4", 4),
    "Splint": ("People2", 6),
    "Ferryman": ("People1", 4),
    "Sops": ("People2", 2),
    "Tibb": ("People1", 0),
    "Traveller": ("People3", 0),
    "Also A Traveller": ("People3", 1),
    "Hermit": ("People2", 0),
    # Meredith Crooke is drawn and fought as the same person: face
    # Actor3:1 and battler Actor3_2, which is that face in armour on the
    # side-view sheet. She used to share People2:7 with the Apprentice
    # while being fought as `Captain`, who is a man.
    "Crooke": ("Actor3", 1),
    # Ambrose Fitch and Ferrety Bother share a face: two grey-bearded old
    # men who are never in the same room, one of them being dead.
    "Ambrose": ("People3", 4),
    # Grimspite gets the horned, red-caped Dark Lord off the Evil sheet.
    # The Prophecy deliberately has no face: it is a document, not a person.
    "Grimspite": ("Evil", 6),
    # ----------------------------------------------------------- the north --
    # The People sheets are spent: People1, People2 and People4 are fully
    # allocated and People3 has one cell left. So Upper Clanging is cast out
    # of `SF_People1` and `SF_Actor3`, which between them hold thirty-two
    # faces that nothing in this game has ever used.
    #
    # Ott is the exception and is worth the share. `People2:7` has **brass
    # goggles pushed up on her head** and is the only engineer's face in the
    # entire stock library, which is not a thing you pass up for a chief
    # engineer. It is shared with the Thistlewick smithy's Apprentice, forty
    # miles and two acts away, who has one line about a hammer.
    "Ott": ("People2", 7),
    "Mrs Tunnicliffe": ("SF_People1", 7),      # white hair, spectacles, scarf
    "Mrs Cotterill": ("SF_People1", 5),        # dark braid, unbothered
    "Mr Cotterill": ("SF_People1", 4),         # moustache, work jacket
    "Spare": ("SF_People1", 0),                # a lad of nine, blue shirt
    "Sowerby": ("SF_People1", 6),              # knit cap, white beard
    "Nib": ("SF_People1", 1),                  # ponytail, red cardigan
    "Mr Kell": ("SF_People1", 2),              # black hair, blue jacket
    # The only face in either SF set with the mass to stand next to Hob.
    "Bryd": ("SF_Actor3", 0),
    # Winnie Marsden is sixty and was drawn as twenty-five. Mrs Tunnicliffe is
    # white-haired and was **born in June of the same year**, so Class of
    # 'Nineteen is sixty years back and every one of the two hundred and forty
    # is a pensioner - which is the funnier reading anyway, and the one the
    # census actually says. Nothing Winnie says implies youth, so this is a
    # recast and not a re-voicing: the lines are untouched.
    #
    # There are exactly two old women in the entire face library and both were
    # already spoken for. So she shares Ysolde's, on the Halbert Quy precedent
    # above: Nether Sopping is forty miles and an act away, and the two of them
    # will never be next to each other in a player's memory.
    "Winnie": ("People1", 7),                  # grey, and sixty, and certain
    # ---------------------------------------------------------------------
    # The Cotterills. Nine children over fifteen years and then nine years of
    # nothing, which is why the name list ran out, why the ninth is called
    # Spare, and why the tenth in the spring is a surprise. Seven of them are
    # placed around the town; Cotter, the eldest, is down the valley at the
    # big foundry and is represented here by his wife.
    #
    # `SF_People1` was spent, and Winnie's move frees exactly the face this
    # wants: Bessie is Winnie's granddaughter, so the resemblance is meant.
    # The other seven come off `SF_Actor1` and `SF_Actor2`, which nothing in
    # this game has ever used.
    "Bessie": ("SF_People1", 3),               # her grandmother, forty years on
    # Rivet was SF_Actor2:2, which is maroon hair and a soft blue shirt and
    # reads as a girl at both sizes - which makes "I have shared a bed my
    # whole life and one of them is Grommet" a different line entirely. He
    # takes SF_Actor1:0 instead: brown hair, a plain white work jacket, and
    # unmistakably a young man. It is also his brothers' and sisters' sheet,
    # so the four of them off SF_Actor1 read as related. He is the only one
    # of the nine indoors at the Safety Valve with Mr Kell, who is black hair
    # and a blue jacket, so brown-and-white is the legible choice there too.
    "Rivet": ("SF_Actor1", 0),                 # 22, day shift, Da's shadow
    "Gudgeon": ("SF_Actor1", 7),               # 20, braid and spectacles, clerk
    "Tappet": ("SF_Actor2", 3),                # 18, blue cap, drives the cart
    "Ferrule": ("SF_Actor1", 1),               # 16, long braid, in charge
    "Grommet": ("SF_Actor2", 6),               # 15, apprentice, put-upon
    "Clevis": ("SF_Actor1", 2),                # 13, red spikes, running a book
    "Shim": ("SF_Actor1", 5),                  # 11, beret and spectacles, tin
    # Firstfield Meadow. The stock sheets are spent, so these five were made
    # with the Character Generator and installed by `art.py` into a sheet of
    # the game's own. The index is the cell they were installed at.
    "Fizz": ("Gen_People1", 0),
    "Norbert": ("Gen_People1", 1),
    "Hollis": ("Gen_People1", 2),
    "Dilys": ("Gen_People1", 3),
    # Penultima. WORLDMAP.md item 10: the first of the new world
    # map's twenty-nine sites to get a room behind its door.
    "Gideon": ("Gen_People1", 4),
    "Dorothy": ("Gen_People1", 5),
    # Restwell, and the last two cells of `Gen_People1`. SITES.md step 1: the
    # Ashburys are the site, so they are the two that get drawn, and the sheet
    # is full after them - step 2 opens a `Gen_People2`.
    "Mrs Ashbury": ("Gen_People1", 6),
    "Walt": ("Gen_People1", 7),
    # Dr Pike shares a face rather than costing a new sheet on his own, on the
    # Halbert Quy and Winnie Marsden precedent above: `SF_Actor3` is the
    # north's sheet and has one face on it, Bryd's, forty miles and an act
    # away. Index 6 is black hair and a dark jacket and is the only face in
    # either SF set that reads as a professional man rather than a crew
    # member, which is what a retired country doctor in a bar needs to be.
    "Dr Pike": ("SF_Actor3", 6),
    # The guest on Restwell's street is an ordinary man and shares the
    # Merchant's face, a grin that has slept well; `Traveller` is People3:0,
    # which is the royalty sheet and is already carrying a joke of its own in
    # Nether Sopping. He was the Neighbour's face, People1:1, until AUDIT.md
    # item 4 - the girl with the pigtails, under a line that says "his pack".
    "Guest": ("People2", 4),
    # Hithermost, SITES.md step 2, and the first two cells of `Gen_People2`.
    # Quillon is BIOS.md's look to the letter - bald, the long white beard,
    # the ochre habit and the eyes shut. Sir Dunstable is the bio's joke, so
    # he is drawn rather than borrowed: an old knight with a waxed moustache,
    # a red cloak and a plume.
    "Quillon": ("Gen_People2", 0),
    "Sir Dunstable": ("Gen_People2", 1),
    # Fairholme, SITES.md step 3. Aldous is drawn - the circlet, the red robe
    # - and Rosamund is BIOS.md's look, the travelling cloak over the ball
    # gown. Mrs Emberthwaite is a dragon, `$BigMonster2`, and no face sheet
    # in the box has a dragon on it, so she spoke with no portrait until Mike
    # drew her one (`supplied.py`): kindly, spectacled, seventy.
    "King Aldous": ("Gen_People2", 2),
    "Mrs Emberthwaite": ("Supplied", 1),
    "Rosamund": ("Gen_People2", 3),
    # The shareholders round the council table all share stock faces: each is
    # one line in one room. The nine heroes take the Actor-sheet faces that no
    # companion and nobody else in the game is wearing, which is the joke - a
    # hero is a hero is a hero. The two farmers are a married couple, one
    # rescue between them; Mr Budge is the `Farmer`'s face, since he is one,
    # and Mrs Budge the bonnet. Mr Pilbeam, who was only passing, has the most
    # ordinary face in the box.
    "Tamsin": ("Actor1", 1), "Brannoc": ("Actor1", 2), "Kit": ("Actor1", 3),
    "Osric": ("Actor1", 6), "Aurel": ("Actor2", 0), "Hild": ("Actor2", 1),
    "Morwen": ("Actor2", 5), "Leof": ("Actor2", 6), "Valen": ("Actor3", 2),
    "Mr Budge": ("People2", 6), "Mrs Budge": ("People4", 1),
    "Mr Pilbeam": ("People4", 0),
    # Olde Evermore, SITES.md step 4. Mirabel is drawn, BIOS.md's look to the
    # letter. The two Elders were stock, Actor3:0 and Nature:6 - a
    # round-eared swordsman and a spirit whose hair covers her ears - in a
    # village written as elves. AUDIT.md item 3 drew them on `Gen_People6`,
    # old and with the pointed ears showing, and gave Mirabel a fringe that
    # does not hide hers (p17 -> p04): she had `ears: p02` all along.
    "Mirabel": ("Gen_People2", 4),
    "Elder Faelan": ("Gen_People6", 6),
    "Elder Lirien": ("Gen_People6", 7),
    # Gladhollow, SITES.md step 5. Toby is drawn, BIOS.md's look to the letter
    # - the saucepan, the plaster, the braces. His brother at the east gate and
    # his granny were left faceless as one short scene each, until AUDIT.md
    # item 1 drew them (`Gen_People10`, below) with his hair and eyes.
    "Toby": ("Gen_People2", 5),
    # The Former Premises, SITES.md step 6. The only person in the building,
    # drawn to WORLDMAP.md 7.4's one rule for him - every single thing he says
    # is good news - so his eyes are shut in contentment.
    "Hollowell": ("Gen_People2", 6),
    # The seven with no map, SITES.md step 7, and the last cell of
    # `Gen_People2`: Elias Meech, who is drawn, because the Sky Anvil is his
    # gatepost and HOB-4 comes back to him. The rest share faces nobody else
    # in the game is wearing. Mother Selvidge is `Evil`'s old woman in the
    # pointed hat, which is the look a fair expects of a fortune-teller and
    # is the only thing about her that is mystical. The three hedge mages at
    # the Lay-By are the pipe-smoker on the same sheet - self-taught, and it
    # shows - and the two `Actor3` women nobody has used: the white hat, and
    # the one with the staff at her shoulder. Whatever lives in the Wrong
    # Dragon's cave is a silhouette Mike drew (`supplied.py`): every line it
    # has is spoken in the dark. The Drainage Commissioner was faceless too,
    # until item 1 drew her (`Gen_People10`, below).
    "Somebody Large": ("Supplied", 2),
    "Meech": ("Gen_People2", 7),
    "Mother Selvidge": ("Evil", 2),
    "Dunnock": ("Evil", 0),
    "Miss Privet": ("Actor3", 3),
    "Mrs Quickset": ("Actor3", 7),
    # Tobias Frayne, SITES.md step 8, and the first cell of `Gen_People3`:
    # drawn, because he is the whole site. A cottager's shirt, a moustache, an
    # open grin, and one scar across the cheek, which is the only one of the
    # eleven that shows.
    "Tobias": ("Gen_People3", 0),
    # Frostwick, SITES.md step 10: all six of WORLDMAP.md 7.3's cast, drawn,
    # in `Gen_People3` 1-6. Only four have to speak to be worth building, and
    # all six do.
    "Perce": ("Gen_People3", 1),
    "Ida": ("Gen_People3", 2),
    "Clem": ("Gen_People3", 3),
    "Mrs Blagg": ("Gen_People3", 4),
    "Pargeter": ("Gen_People3", 5),
    "Mrs Marchpane": ("Gen_People3", 6),
    # Chapter Clerk Mordaunt, SITES.md step 11, drawn, and the last cell of
    # `Gen_People3`: the Order's black coat, reading glasses, a trimmed grey
    # beard. The next person drawn opens `Gen_People4`.
    "Mordaunt": ("Gen_People3", 7),
    # The Sable Hart, SITES.md step 12: five doomed rivals, drawn, in
    # `Gen_People4` 0-4 - one look five times, hooded, which is the joke.
    "Crake": ("Gen_People4", 0),
    "Morrow": ("Gen_People4", 1),
    "Rook": ("Gen_People4", 2),
    "Veyle": ("Gen_People4", 3),
    "Blackwood": ("Gen_People4", 4),
    # Little Gore and Sump, SITES.md step 13, drawn, `Gen_People4` 5 and 6.
    # **Not "Hester"**: Mrs Hester Ashbury is Restwell's, above, and a first
    # name only shows in a speaker box if it is put there. Mr Thurle is the
    # Parish Clerk of Sump, who cannot allocate the wasps.
    "Mrs Vane": ("Gen_People4", 5),
    "Mr Thurle": ("Gen_People4", 6),
    # Ashcombe, SITES.md step 14, drawn: Corvin's mother, from his portrait,
    # and the Drainage Museum's curator, `Gen_People5` 0, the first of that
    # sheet. **"Mrs Ash" is not "Mrs Ashbury"** (Restwell's, above); a
    # prefix is not a collision, but a careless grep says it is.
    "Mrs Ash": ("Gen_People4", 7),
    "Mr Weir": ("Gen_People5", 0),
    # Weeping Bottom, SITES.md step 15, drawn, `Gen_People5` 1 and 2, both in
    # Merribell's hood and habit: the Prioress in the Order's blue trim, and
    # Sister Bewick of What Ought To Work in the same habit trimmed black.
    "Prioress": ("Gen_People5", 1),
    "Sister Bewick": ("Gen_People5", 2),
    # AUDIT.md item 1, the faceless speakers, drawn - `Gen_People7`, and
    # Weeping Bottom's other eight. They walked as stock sprites, three of
    # them shared (Sister Pim and Sister Lamb were one `People4` 1, and Mr
    # Dace was Tom's old man in the headband), so each is drawn whole and
    # the event reads its sprite from this entry, like the Elders: the
    # Sisters of Whatever Works in one uniform - the white kerchief cap and
    # a blue dress with a white collar - Pim young and Lamb grey; Sir Hamo
    # the oldest face, a long white beard, in a knight's white surcoat.
    "Sister Pim": ("Gen_People7", 0),
    "Sister Lamb": ("Gen_People7", 1),
    "Mrs Liddy": ("Gen_People7", 2),
    "Mr Crouch": ("Gen_People7", 3),
    "Mr Oakes": ("Gen_People7", 4),
    "Sir Hamo": ("Gen_People7", 5),
    "Mr Nuttall": ("Gen_People7", 6),
    "Mr Dace": ("Gen_People7", 7),
    # Great Dunnage's other eight, `Gen_People8` - the "other two judges" and
    # "other Warden" the note on the Mayor's block above left faceless, and
    # the town round them. Drawn whole, like Weeping Bottom's: the Watchman
    # in the Corporation's blue coat; Mr Plummer broad, moustached, in a
    # brown coat with a fur collar; Warden Crabbe grey, goateed, in the
    # Company's dark coat and gold; the Town Clerk spectacled and in black;
    # Mr Ambler, who gives nines, grey-bearded in mustard; Miss Quayle, who
    # gives twos, severe in navy. Mr Tweddle, the ninth, is `Gen_People9`'s.
    "Watchman": ("Gen_People8", 0),
    "Mrs Poskitt": ("Gen_People8", 1),
    "Mr Plummer": ("Gen_People8", 2),
    "Warden Crabbe": ("Gen_People8", 3),
    "Town Clerk": ("Gen_People8", 4),
    "Mrs Dewhirst": ("Gen_People8", 5),
    "Mr Ambler": ("Gen_People8", 6),
    "Miss Quayle": ("Gen_People8", 7),
    # `Gen_People9`: Mr Tweddle, Dunnage's ninth - small, grey, in green, and
    # a nightingale that is a nightingale - then the rest of the hamlets and
    # the Sable Hart. Dame Winifred in armour and "a good plain helmet". The
    # three Vanes are children on the kid body, with their mother Hester's
    # brown hair and blue eyes: Bess was an adult in a headscarf and Alfie
    # and Nell shared stock children with half the game. Mr Gammage's eyes
    # are shut; he is not asleep. Mrs Garrow is the Hart's landlady and not
    # the Bell's, so she is black ringlets where Mrs Dewhirst is a red bun.
    "Mr Tweddle": ("Gen_People9", 0),
    "Dame Winifred": ("Gen_People9", 1),
    "Bess": ("Gen_People9", 2),
    "Alfie": ("Gen_People9", 3),
    "Nell": ("Gen_People9", 4),
    "Mr Gammage": ("Gen_People9", 5),
    "Mrs Pardew": ("Gen_People9", 6),
    "Mrs Garrow": ("Gen_People9", 7),
    # `Gen_People10`: the Collegium's three - Dr Hapgood, twenty-two years a
    # Junior Fellow, in the Collegium's robe; the Reader, young, in a white
    # coat; the Undergraduate, whom the text never gives a pronoun, a young
    # woman in the white-and-blue uniform - then Gladhollow's Ned, with his
    # brother Toby's hair and eyes, and their Granny Wendle in a lace bonnet;
    # Ashcombe's Wilf, small, ginger, with a paper boat nobody can sail, and
    # Mrs Dimmock of the post office in blue; and the Drainage Commissioner
    # out on the Cinder Fen, also never given a pronoun, in a yellow oilskin.
    # She is a face only - the Fen's event has no sprite.
    "Dr Hapgood": ("Gen_People10", 0),
    "Reader": ("Gen_People10", 1),
    "Undergraduate": ("Gen_People10", 2),
    "Ned": ("Gen_People10", 3),
    "Granny Wendle": ("Gen_People10", 4),
    "Wilf": ("Gen_People10", 5),
    "Mrs Dimmock": ("Gen_People10", 6),
    "Commissioner": ("Gen_People10", 7),
    # `Gen_People11`, the last of item 1: Fenmarch's Mrs Puddifoot, chestnut
    # under the white cap, in a black housekeeper's dress (Sister Lamb has
    # the same cap, grey, and they shared one stock sprite before); Tom, who walked about as the
    # old man in the headband and is about thirty (nine years married, three
    # small children), so he keeps the headband as a green bandana; and Olde
    # Evermore's raker, "Elf", which Mike asked to have drawn - an elf with
    # the ears showing, in a khaki coat the colour of the leaves.
    "Mrs Puddifoot": ("Gen_People11", 0),
    "Tom": ("Gen_People11", 1),
    "Elf": ("Gen_People11", 2),
    # HOB-3, two of Crooke's apprentices, week four (`q_hob.py`). Hodge is
    # in the syllabus bandana, as Norbert is. Their sprites are only ever
    # the knocked-down strip, `Gen_People11_Damage`, under the anvil.
    "Ivy": ("Gen_People11", 3),
    "Hodge": ("Gen_People11", 4),
    # NIX-5, the Works Band's bassoonist, through the Gloamwood at night
    # (`q_nix.py`).
    "Bagshawe": ("Gen_People11", 5),
    # WRE-3, the Gloamwood Society: its chair, its secretary, and Miss
    # Pellow, who saw it in seventy-one (`q_wren.py`).
    "Mrs Lumb": ("Gen_People11", 6),
    "Mr Dunmore": ("Gen_People11", 7),
    "Miss Pellow": ("Gen_People12", 0),
    # ROL-3, the Fairweather alumni (`q_roland.py`): six of the eleven are
    # drawn; the five with one line share stock faces nobody in the Slain
    # Wyvern wears.
    "Dame Florence": ("Gen_People12", 1),
    "Brother Anselm": ("Gen_People12", 2),
    "Mags": ("Gen_People12", 3),
    "Pim": ("Gen_People12", 4),
    "Odile": ("Gen_People12", 5),
    "Old Jory": ("Gen_People12", 6),
    "Hettie": ("People1", 1),
    "Lord Tobin": ("People3", 2),
    "Ned": ("People1", 0),
    "Saul": ("People2", 4),
    "Major Royce": ("People4", 6),
    # Fenmarch Hall, SITES.md step 16, drawn, `Gen_People5` 3 and 4. The
    # Fourth is Aldric Pemberton-Gore IV, and **"Aldric" is already Sir
    # Aldric**, so the household's name for him is the speaker. **"Mr
    # Ottershaw" is not "Ott"** (Upper Clanging's); a prefix grep says it is.
    "The Fourth": ("Gen_People5", 3),
    "Mr Ottershaw": ("Gen_People5", 4),
    # The Collegium Arcanum, SITES.md step 17, drawn, `Gen_People5` 5-7, and
    # that sheet is full. **"Mr Gedge" is not the "Clerk"** (`People2` 0, the
    # roster's); the Head Porter is the one who holds the keys.
    "Mr Gedge": ("Gen_People5", 5),
    "Prewitt": ("Gen_People5", 6),
    "Dean Fenwold": ("Gen_People5", 7),
    # Great Dunnage, SITES.md step 18, drawn, `Gen_People6` 0-4 - the sheet
    # this step opened. The horse is a sprite (`Vehicle` 4) and has no face;
    # the Bell's other two judges and the Company's other Warden speak with no
    # portrait. **"Mr Tibbs" is not "Tibb"** (Nether Sopping's, `People1` 0),
    # which a prefix grep finds first, and nobody else in the game speaks as
    # "The Mayor". Cotter Cotterill shares `SF_Actor2` 7, which
    # nothing had used: brown hair and a white work jacket, which is his
    # brother Rivet's look (`SF_Actor1` 0) four years on, and meant to be.
    "The Mayor": ("Gen_People6", 0),
    "Prime Warden": ("Gen_People6", 1),
    "Mr Tibbs": ("Gen_People6", 2),
    "Mrs Harbottle": ("Gen_People6", 3),
    "Miss Fettle": ("Gen_People6", 4),
    "Cotter": ("SF_Actor2", 7),
}


# A message window shows four lines. RPG Maker's own editor enforces that, and
# nothing enforces it here, so `say` and `narrate` do: anything longer is split
# into consecutive windows rather than being quietly drawn off the bottom.
MESSAGE_LINES = 4

CURRENCY = "cr"          # matches System.json, for the width of \G


def _pages(lines):
    lines = list(lines)
    return [lines[i:i + MESSAGE_LINES]
            for i in range(0, len(lines), MESSAGE_LINES)] or [[]]


def _check_width(line, face, speaker):
    """The window has no wrap and no ellipsis: a line too wide for it is drawn
    off the edge and the player never sees the end of the sentence. A face
    takes 164 of the 784 pixels, which is why a line that is fine over a
    narrator's window is not fine over a speaker's.

    This refuses to build rather than wrapping the line, because where a line
    of dialogue breaks is a decision about timing and belongs to whoever wrote
    it. `rmmzdata.wrap` is there for prose."""
    limit = R.message_width(bool(face))
    width = R.text_width(line, currency=CURRENCY)
    if width > limit:
        over = int((width - limit) / (R.FONT_SIZE / 2.0) + 0.999)
        raise ValueError(
            "%s's line is %d character(s) too wide for the message window "
            "(%d of %d px, and a face costs 164 of them). Break it earlier:\n"
            "  %r" % (speaker or "the narrator", over, width, limit, line))


def say(speaker, lines, *, face=True, indent=0, position=2):
    """One person saying something, over as many windows as it takes.

    `face` may name a `FACES` key other than the speaker's own, for two
    people who answer to the same label and are not the same person."""
    if speaker is None:
        return narrate(lines, indent=indent)
    key = face if isinstance(face, str) else speaker
    name, index = FACES.get(key, ("", 0)) if face else ("", 0)
    out = []
    for page in _pages(list(lines)):
        # The speaker's name leads every window, not just the first: a long
        # speech runs over several of them and the player should not have to
        # remember who started talking four windows ago.
        #
        # It leads the message rather than sitting in Show Text's `speakerName`
        # box, which would cost the line nothing. That is a decision about how
        # the game looks and not an oversight - see CLAUDE.md. When a line is
        # too wide, break the line.
        page = ["\\C[6]%s:\\C[0] %s" % (speaker, page[0])] + page[1:]
        for line in page:
            _check_width(line, name, speaker)
        out += R.text(page, face_name=name, face_index=index,
                      position=position, indent=indent)
    return out


def narrate(lines, indent=0):
    """Screen text with nobody speaking - descriptions, and the narrator."""
    out = []
    for page in _pages(lines):
        for line in page:
            _check_width(line, "", None)
        out += R.text(page, indent=indent)
    return out


def trope(indent=0):
    """Bump the cliché counter. The ending reads the total back to the player,
    so every joke that lands on a well-worn RPG convention calls this exactly
    once - and, because it usually sits behind a self switch, only once per
    playthrough."""
    return R.control_variable_add(db.VAR_TROPES, 1, indent=indent)


def blush(indent=0):
    """Bump the count of things nobody quite said.

    The companion to `trope()`, and the same discipline: bump it here and
    nowhere else, so the total can be audited with one grep. Every Register A
    moment in the game calls this exactly once, on first sight, and because it
    is a bare variable-add with no message it can be appended to any command
    list without disturbing the pacing of what is already there.

    The joke only exists in aggregate. No single line of dialogue admits to
    anything - each one is a compliment, a repair, or a census entry - and the
    ending prints the total, which is the first and only time the game lets on
    that it was counting."""
    return R.control_variable_add(db.VAR_BLUSHES, 1, indent=indent)


def companion_story(actor_id, indent=0):
    """A companion quest is finished: turn on that companion's story switch,
    and the first time it goes on, count them.

    The ending reads one line per companion off `db.SW_STORY` and one closing
    line off `db.VAR_COMPANION_STORIES` (COMPANIONS.md 1.4), so a companion
    who finishes two quests is still one companion who got something out of
    it. Call this at the end of every companion quest and set neither of the
    two anywhere else."""
    sw = db.SW_STORY[actor_id]
    return R.if_then(R.condition_switch(sw, False),
                     [R.control_switch(sw, True),
                      R.control_variable_add(db.VAR_COMPANION_STORIES, 1)],
                     indent=indent)


def got(lines, indent=0):
    """The 'you found a thing' message, in the colour things are found in."""
    return narrate(lines, indent=indent)


# ------------------------------------------------------------------ doors ---
def door_page(target_map, tx, ty, direction=2, se="Open1"):
    """The commands behind a door sprite: open it, step through, transfer."""
    cmds = [R.play_se(se)]
    cmds += R.move_route(0, K.door_animation(), repeat=False, wait_flag=True)
    cmds += R.move_route(-1, [{"code": 12}], repeat=False, skippable=True,
                         wait_flag=True)
    cmds += [R.play_se("Move1"),
             R.transfer(target_map, tx, ty, direction, 0)]
    return cmds


def door(event_id, name, x, y, target_map, tx, ty, direction=2, sheet="!Door1",
         index=0):
    """An outward-facing door on a house wall. Player-touch, because a door
    that needs a button press on an impassable tile is fiddly."""
    return R.event(event_id, name, x, y, [R.page(
        door_page(target_map, tx, ty, direction),
        img=R.image(sheet, index, direction=2), trigger=1, priority=1)])


def exit_tile(event_id, name, x, y, target_map, tx, ty, direction=2):
    """An invisible way out of an interior - stand on it and you are outside.

    Below characters, not same as characters: `checkEventTriggerHere` only
    starts events whose priority is *not* normal, so a player-touch tile at
    "same as characters" is one the player walks straight over. It would still
    answer the action button from the tile next to it, which is exactly what a
    door that has stopped working looks like."""
    return R.event(event_id, name, x, y, [R.page(
        [R.play_se("Move1"), R.transfer(target_map, tx, ty, direction, 0)],
        img=R.image(""), trigger=1, priority=0, through=True)])


def sign(event_id, name, x, y, lines, sheet="", index=0):
    """Something you read. No sprite by default - the scenery tile is the
    sign, and the event just sits on it."""
    return R.event(event_id, name, x, y, [R.page(
        narrate(lines), img=R.image(sheet, index, direction=2),
        trigger=0, priority=1, direction_fix=True, through=True)])


def npc(event_id, name, x, y, commands, sheet, index, direction=2,
        move_type=0, trigger=0, priority=1, step_anime=False, pages=None,
        move_speed=3, move_frequency=3):
    """A person who says something when you talk to them."""
    first = R.page(commands, img=R.image(sheet, index, direction=direction),
                   trigger=trigger, priority=priority, move_type=move_type,
                   step_anime=step_anime, move_speed=move_speed,
                   move_frequency=move_frequency)
    return R.event(event_id, name, x, y, [first] + list(pages or []))


def prop(event_id, name, x, y, lines, sheet, index, direction=2, pattern=1,
         extra=()):
    """A searchable object - a barrel, a bookshelf, a scarecrow."""
    return R.event(event_id, name, x, y, [R.page(
        narrate(lines) + list(extra),
        img=R.image(sheet, index, direction=direction, pattern=pattern),
        trigger=0, priority=1, direction_fix=True)])


def specimen(event_id, name, x, y, lines, wren_says, again,
             sheet="", index=0):
    """One of NORTH.md 3.4's three things on the road, for Wren to be correct
    about.

    Taxonomy is largely the study of how things reproduce, so a taxonomist
    doing her job out loud is a delivery system that needs no crudeness in it
    at all - she is describing a display structure, or a gravid female, and
    every word of it is the right word. She is never once aware. Bram is the
    one who cannot cope, and Bram does not speak: he is the narrator.

    The shape is the wyvern's, in a different room. The thing on the branch is
    the same thing either way, and the cataloguer is standing behind you or
    she is not - so a party without her loses nothing and is told nothing.
    `VAR_BLUSHES` counts moments, so the bump is behind a self switch and the
    second page is what you get afterwards."""
    look = narrate(lines)
    said = list(wren_says) + [blush(), R.self_switch("A", True)]
    page = dict(img=R.image(sheet, index, direction=2), trigger=0,
                priority=1, direction_fix=True, through=(sheet == ""))
    return R.event(event_id, name, x, y, [
        R.page(look + R.if_then(R.condition_actor_in_party(db.WREN), said),
               **page),
        R.page(narrate(again), conditions={"selfSwitchValid": True,
                                           "selfSwitchCh": "A"}, **page),
    ])


def chest(event_id, name, x, y, contents, lines):
    """A treasure chest: page one gives you the thing, page two is empty."""
    open_it = [R.play_se("Open1")] + list(contents)
    open_it += got(lines)
    open_it.append(R.self_switch("A", True))
    return R.event(event_id, name, x, y, [
        R.page(open_it, img=R.image("!Chest", 0, direction=2, pattern=1),
               trigger=0, priority=1, direction_fix=True),
        R.page(narrate(["Empty. You were thorough."]),
               img=R.image("!Chest", 0, direction=2, pattern=2),
               trigger=0, priority=1, direction_fix=True,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ])


# -------------------------------------------------------------- recruiting ---
PARTY_LIMIT = 4      # Bram plus three


def recruit(event_id, actor_id, name, x, y, sheet, index, *, pitch, accept,
            decline, full, direction=2, move_type=0, extra_pages=(), after=(),
            again=None):
    """One of the nine.

    Three pages, because there are three states and only the middle one is
    obvious: never met, met and sent home, and currently following you around.
    The last of those is keyed on a global switch rather than a self switch,
    because a form desk can amend the roster - and a self switch can only be
    set by its own event, so nothing else could ever put this person back on
    the map.

    `again` is a dict of the same four command lists - pitch, accept, decline,
    full - for somebody who has already walked north with you and is now back
    in their own kitchen explaining it to the neighbours. Any key it leaves
    out falls back to the first-meeting version."""
    sw = db.SW_RECRUIT[actor_id]
    known = db.SW_KNOWN[actor_id]

    def joining(accept_cmds, first_time):
        """The join itself.

        `initialize` is Change Party Member's flag for `Game_Actor.setup()`,
        which puts the actor back to their database level with their database
        equipment. That is right exactly once. On a rejoin it silently deletes
        every level they earned walking north with you and every piece of kit
        you ever handed them, which is why it is set on the first join and
        never again - the actor sits in `$gameActors` the whole time they are
        at home, with everything still on it."""
        cmds = list(accept_cmds)
        cmds += [R.change_party(actor_id, add=True, initialize=first_time),
                 R.control_switch(known, True)]
        if not first_time:
            # They have had a month at home, so they come back rested. A first
            # join does not need this - `setup()` has just given them full HP
            # - but a rejoin otherwise hands you back exactly the three hit
            # points they were struck off on, and a companion who has been
            # sitting in their own kitchen since Tuesday being quietly bleeding
            # is a bug the player has no way to read as anything else. Recover
            # All on one actor works whether or not they are in the party, and
            # it clears Death, so somebody struck off unconscious wakes up.
            cmds.append(R.recover_all(actor_id))
        cmds.append(R.play_me("Item"))
        cmds += R.text(["\\C[3]%s\\C[0] %s the party!"
                        % (name, "joined" if first_time else "rejoined")])
        cmds += [R.control_switch(sw, True),
                 R.control_variable_add(db.VAR_COMPANIONS, 1)]
        cmds += list(after)
        return cmds

    def conversation(pitch_cmds, accept_cmds, decline_cmds, full_cmds,
                     first_time):
        # Whether there is room changes while the player is standing here, so
        # this is a branch inside the choice rather than a condition on the
        # page.
        take_them = R.if_then(
            R.condition_script("$gameParty.size() < %d" % PARTY_LIMIT),
            joining(accept_cmds, first_time), list(full_cmds))
        yes = "Come with me" if first_time else "Come back with me"
        return list(pitch_cmds) + R.choice_block(
            [yes, "Not right now"], [take_them, list(decline_cmds)])

    look = dict(img=R.image(sheet, index, direction=direction), trigger=0,
                priority=1, move_type=move_type)
    a = dict(again or {})

    first = R.page(conversation(pitch, accept, decline, full, True), **look)
    # Struck off the roster and back home. Everything they earned is still on
    # them, and so is everything they know about you.
    returning = R.page(
        conversation(a.get("pitch", pitch), a.get("accept", accept),
                     a.get("decline", decline), a.get("full", full), False),
        conditions={"switch1Valid": True, "switch1Id": known}, **look)

    # Once they are following you around, the copy of them standing in their
    # own kitchen has to go away - invisible, and walk-through so it stops
    # being a wall in the middle of a room. It is the last page of the three,
    # because MZ takes the highest-numbered page whose conditions hold and
    # anyone who is with you has also, necessarily, been met.
    gone = R.page([], img=R.image(""), trigger=0, priority=1, through=True,
                  conditions={"switch1Valid": True, "switch1Id": sw})
    return R.event(event_id, name, x, y,
                   [first, returning, gone] + list(extra_pages))


# ------------------------------------------------------- who is with you ----
# Two lists, because Show Choices tops out at six options in the editor and
# nine companions do not fit in one form. The Committee clerk in Thistlewick
# holds Form C-12 and can only strike off Thistlewick people; Registrar Pell in
# Nether Sopping holds Form C-12(S) and can only strike off southern ones.
# This is funnier than a submenu and it is exactly how the Committee would in
# fact have arranged it.
COMPANIONS = [
    (db.MERRI, "Merribell"), (db.HOB, "Hob"), (db.ZEPH, "Zephyrine"),
    (db.NIX, "Nix"), (db.ALDRIC, "Aldric"), (db.PIPER, "Piper"),
]

COMPANIONS_SOUTH = [
    (db.CORVIN, "Corvin"), (db.WREN, "Wren"), (db.ROLAND, "Roland"),
]


def roster_amendment(companions=None, clerk="Clerk"):
    """A dismissal form. Lets the player swap a companion out without
    restarting, which matters because the whole of the first act is a choice of
    three from what is now nine."""
    branches = []
    for actor_id, nm in (companions or COMPANIONS):
        # `SW_KNOWN` is set here as well as at the join, and the redundancy is
        # the point: anybody standing at this desk to be struck off has, by
        # definition, been in the party. `story.recruit` sets it too, but a
        # save made before these switches existed has it clear for somebody who
        # is demonstrably a companion - and a clear switch sends them back to
        # page 0, which introduces them to you all over again and re-initialises
        # them down to their database level. One command here migrates every
        # such save at the only moment it matters, without a migration.
        remove = [R.control_switch(db.SW_KNOWN[actor_id], True),
                  R.change_party(actor_id, add=False),
                  R.control_switch(db.SW_RECRUIT[actor_id], False),
                  R.control_variable_add(db.VAR_COMPANIONS, -1),
                  R.play_se("Cancel1")]
        remove += R.text(["\\C[3]%s\\C[0] has been struck from the roster" % nm,
                          "and has gone home to think about it."])
        # Said out loud because the player cannot see it in the menu: a struck
        # companion keeps their level and their kit, and gets both back the
        # moment they are re-hired. Nothing is lost by trying somebody else.
        remove += say(clerk, [
            "They keep the kit and the experience.",
            "Both are theirs. It was tried the other way",
            "once. There is a form about why not."])
        not_here = say(clerk, ["%s is not on the roster." % nm,
                               "I cannot remove someone who is not on the",
                               "roster. That would create a negative person."])
        branches.append(R.if_then(R.condition_actor_in_party(actor_id),
                                  remove, not_here))
    return R.choice_block([nm for _, nm in (companions or COMPANIONS)],
                          branches,
                          cancel=say(clerk, ["Filed under 'no change'."]))
