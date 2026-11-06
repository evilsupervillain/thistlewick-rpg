"""CURIOS.md wave C2: the south road and the south - Maps 9, 10, 13-20
and 72.

Nether Sopping is where the retired go, and its tavern is full of people
from other people's stories; the jokes there are about endings, and are
kind to everyone in the room (NORTH.md 1.6: nobody is diminished by their
own punchline, and Ysolde, Merrow and Ambrose least of all)."""

import db
import mapkit as K
from curios import curio as C

# ----------------------------------------------- Map 14, the Slain Wyvern --
WYVERN_PIANO = [
    "The Slain Wyvern's piano. Every key has a name pencilled on it: "
    "somebody who sat at this bar and swore they could play.",
    "Most of the keys have two names. Middle C has eleven.",
    "You play the one tune you know. Twenty retired adventurers turn "
    "round at once, the way people do who have heard a trap click."]

WYVERN = [
    C("The Piano", [(9, 4), (8, 4), (10, 4)], "Piano", WYVERN_PIANO,
      party=[
          (db.PIPER, [("Piper", "Budge up. They want a shanty."),
                      "Piper plays a sea shanty, and the whole room "
                      "sings the chorus, in four different versions "
                      "from four different coasts.",
                      "Nobody gives way. It is the best thing you have "
                      "ever heard."]),
          (db.CORVIN, ["Corvin sits down without a word and plays "
                       "something in a minor key. It is extremely good. "
                       "It is about ash.",
                       "Dorcas asks for something cheerful. He plays the "
                       "same thing again, faster."]),
          (db.ROLAND, ["Roland plays a fanfare. While he plays it, he is "
                       "lit very slightly better than the rest of the "
                       "room.", ("Roland", "Thank you! I'm here all "
                                 "week. Well. Until I'm not.")]),
          (db.WREN, [("Wren", "Rosewood veneer. And woodworm - "
                      "Anobium punctatum, three generations at least. "
                      "Don't play the bottom octave. They're nesting.")]),
          (db.MERRI, ["Merribell plays the one hymn the Order has. It "
                      "is called 'Sit Down', and it works: half the room "
                      "does."])],
      again=["The piano. Middle C has eleven names on it, and one of "
             "them, you now notice, is in a child's writing: SOPS."]),
    C("The Clock", (11, 3), "Clock", [
        "A wall clock, stopped at ten to twelve.",
        "Nobody winds it. Dorcas says it is right twice a day, which is "
        "more than you can say for most of the people in here."]),
    C("Notice", (12, 3), "Posted Notice", [
        "A notice under the crossed swords: NO SWORDS ON THE BAR. NO "
        "SPELLS IN THE BAR. NO DRAGONS IN THE BAR, EVEN SMALL ONES.",
        "And, added later: EVEN IF IT IS A GOOSE. - D. THRUPP."]),

    # --- behind the bar
    C("Bottles", (3, 4), "Bottle Shelf A", [
        "Bottles behind the bar, each with a label in Dorcas's hand: what "
        "it is, how much it is, and who in this room it is not to be "
        "served to.",
        "Every label has at least one name on it."]),
    C("Biscuit Shelf", (5, 4), "Bread Shelf", [
        "Sopping biscuits, by the dozen, under a card: BAKED THIS "
        "MORNING.",
        "Under that, very small: SOME MORNING."]),
    C("Jars", (6, 4), "Sundries Shelf A", [
        "Jars of pickled things. At the end of the shelf, one jar of a "
        "thing that has been pickled for so long it has turned into a "
        "different thing, and is now quite happy."]),
    C("Ship in a Bottle", (3, 6), "Bottle D", [
        "A ship in a bottle. On the deck of the ship there is a tiny "
        "bottle, and in that, if you squint, a tinier ship.",
        "Somebody in Nether Sopping has a great deal of time, and very "
        "small tweezers."]),
    C("A Bottle", (5, 6), "Bottle B", [
        "A bottle of the local cordial. The label has a picture of the "
        "sea on it, and the words THE SEA IS RIGHT THERE."]),
    C("A Tankard", (6, 6), "Pint Mug C", [
        "Somebody's tankard, with a mat on top to keep the flies off. "
        "The mat says SAVED.",
        "Judging by the dust, it has been saved since the spring."]),
    C("The Tap", (7, 6), "Beer Barrel A", [
        "A barrel with a tap in it, and a sign on the tap: HEROES WILL "
        "WAIT THEIR TURN LIKE EVERYBODY ELSE."],
      trope="containers"),
    C("A Bucket", (7, 7), "Basin", [
        "A bucket marked FOR THE GOOSE.",
        "The goose has been on the wall since 1940. The bucket is filled "
        "every morning anyway. Nobody remembers who started it."]),

    # --- at the tables
    C("Hosea's Book", (10, 6), "Open Book A (H)", [
        "Hosea's history, open on a table of its own. You read the "
        "paragraph he is writing:",
        "'Chapter Three Hundred and Twelve. The Forty-Eighth arrives, and "
        "stands about.'",
        "It is the most accurate thing anybody has written about you."],
      then=[["You turn back a page. Chapter Three Hundred and Eleven is "
             "called 'Lunch'."],
            [("Hosea", "Do you mind? I'm in the middle of you.")]],
      again=["Chapter Three Hundred and Twelve. He has got to the part "
             "where you read over his shoulder."]),
    C("Hulda's Ledger", (4, 9), "Open Book A (H)", [
        "Hulda's ledger. Three columns: BEAR. BEAR (DIFFERENT SORT). BEAR "
        "(THE FIRST SORT AFTER ALL).",
        "The third column has a great many crossings-out in it, and one "
        "very firm full stop."]),
    C("Field Kit", (6, 9), "Medicine Bottles B", [
        "Ysolde's field kit, open on the table out of habit: bottles "
        "labelled in a hand that has written on a great many "
        "bandages.",
        "One bottle is labelled FOR AFTER. It is tea."],
      party=[(db.MERRI, [("Merribell", "She's got all of them in the "
                          "order you'd reach for them. In the dark. "
                          "That's forty years, that is.")])]),
    C("The Long Table", [(9, 9), (9, 10), (13, 9), (13, 10)],
      ("Dinner Set B (Top)", "Dinner Set A (Bottom)"), [
        "The long table, where people out of eleven different stories "
        "have their dinner together.",
        "Every plate is a different meal from a different country. "
        "Nobody has eaten a thing. They are all too busy telling each "
        "other how it ended."]),
    C("A Napkin", (18, 11), "Dinner Set C (Left)", [
        "Perpetua's plate, and beside it her napkin, folded into a "
        "little crown.",
        "She folds every napkin she is given into a crown. She has no "
        "idea why. She is extremely good at it."]),
    C("A Bottle", (19, 11), "Bottle C", [
        "A bottle of very good wine with a crest on the label. "
        "Nobody at this table ordered it.",
        "Dorcas says one arrives every month from a palace somewhere, "
        "addressed to WHOM IT MAY CONCERN."]),
    C("Peasant Dinner", (4, 15), "Dinner Set B (Top)", [
        "The very ordinary travellers' table. Two plates.",
        "One is beans, untouched. The other was roast pheasant with all "
        "the trimmings, and it has been eaten down to the bone."]),
    C("Peasant Wine", (5, 15), "Bottle B", [
        "A bottle of wine with a royal crest on it, and a label stuck on "
        "over the crest in a hurry: FARM WINE."]),
    C("Peasant Luggage", (3, 15), "Crate A", [
        "A crate stencilled PEASANT LUGGAGE. It has gold corners, and a "
        "little velvet cushion on top for sitting on."]),
    C("Barrel", (21, 13), "Barrel", [
        "A barrel of salt fish. You lift the lid, and put it back. In "
        "Nether Sopping, fish is not a thing you search. It is a thing "
        "that happens to you."]),
    C("Barrel", (13, 15), "Barrel", [
        "A barrel with a brick on the lid, and a note: THE BRICK IS THERE "
        "FOR A REASON.",
        "You respect the reason."]),

    # --- the Healers' Table, behind the curtain (MER-3)
    C("The Table's Shelf", (33, 4), "Medicine Shelf", [
        "The Table's medicine shelf. Everything on it is labelled with "
        "what it is for, and then, underneath, what it was actually used "
        "for, once, in a hurry.",
        "BANDAGES. ALSO: ROPE, A FLAG, A SLING, AND A HAT."]),
    C("The Table's Books", (39, 4), "Bookshelf A", [
        "FIELD MEDICINE FOR THE CHOSEN, Third Edition. The chapter on "
        "falling off things is two hundred pages long."],
      then=[["WHAT THE BARD MEANT BY 'FLESH WOUND'. A pamphlet, much "
             "annotated."],
            ["STITCHES I HAVE PUT IN HEROES, AND WHERE. A memoir. The "
             "index is very well thumbed."]],
      party=[(db.MERRI, [("Merribell", "I've got the second edition. "
                          "The chapter on falling off things was only "
                          "a hundred and twenty. Things have got "
                          "higher.")])]),
    C("Globe", (33, 6), "Globe", [
        "A globe. Somebody has drawn little red crosses all over it, one "
        "for every place a patient of the Table's had to be carried "
        "home from.",
        "There is not much globe left."]),
    C("Tea", (35, 4), "Pint Mug D", [
        "Two mugs of tea, so strong it has gone frothy on top. Healers' tea.",
        "It is strong enough to set a bone."]),
    C("Tankard", (36, 4), "Pint Mug C", [
        "A tankard with HOBDAY on it, and a little picture of a lute "
        "with a line through it."]),
    C("Barrel", (37, 4), "Beer Barrel A", [
        "A small barrel with a tap and a label: CLEAN WATER. BOILED. "
        "BOILED AGAIN. BOILED BY GRIZEL, WHO DOES NOT TRUST HOBDAY'S "
        "BOILING."]),
    C("Potted Plant", (33, 10), "Potted Plant A", [
        "A potted plant. It has a little splint on one stem, put on by "
        "four different people, each of whom thought the last one had "
        "done it wrong."]),
    C("Potted Plant", (41, 10), "Potted Plant A", [
        "Another plant, in perfect health.",
        "Nobody at the Table trusts it."]),
]

# ----------------------------------------------- Map 13, Nether Sopping --
SOPPING = [
    # --- the boards on legs round the town
    C("Board", (4, 10), "Sign B", [
        "A board: NETHER SOPPING IN BLOOM - HIGHLY COMMENDED.",
        "In smaller letters: DAMP CATEGORY."]),
    C("Board", (10, 10), "Sign B", [
        "A board: SPEED LIMIT - A BRISK WALK.",
        "Underneath: ADVENTURERS ARE NOT TO RUN THROUGH THE TOWN, HOWEVER "
        "URGENT THE PROPHECY. YES, YOU. WE CAN SEE YOU."],
      trope="dash"),
    C("Board", (24, 10), "Sign B", [
        "A board: WICK & BARROW, OUTFITTERS. EVERYTHING FOR THE ROAD "
        "NORTH.",
        "Chalked under it: ALSO THE ROAD BACK (ASK)."]),
    C("Board", (31, 10), "Sign B", [
        "A board: TODAY'S WEATHER - RAIN.",
        "It is not chalked. It is painted on."]),
    C("Board", (3, 16), "Sign B", [
        "A board: THE SLAIN WYVERN. ROOMS. HOT FOOD. ONE WYVERN (SLAIN).",
        "Very small, at the bottom, where the paint has been scratched "
        "off and done again: (GOOSE)."]),
    C("Board", (34, 20), "Sign B", [
        "A board: THE ADVENTURERS' GUILD (PROVISIONAL). FOUNDED 1960, "
        "PROVISIONALLY. MEMBERSHIP OPEN.",
        "Somebody has added: STILL PROVISIONAL. Somebody else has "
        "added: PROVISIONALLY."]),
    C("Board", [(17, 25), (18, 25)], "Sign B", [
        "A board on the harbour: TIDES. HIGH - WHEN IT FEELS LIKE IT. "
        "LOW - SEE ABOVE."]),

    # --- the shop fronts
    C("Outfitters' Sign", (27, 8), "Shop Sign (Armor)", [
        "A painted breastplate: W & B. A little plate screwed on below "
        "it: ARMOUR REPAIRED. DRAGONS QUOTED FOR."]),
    C("Outfitters' Teapot", (31, 8), "Shop Sign (Teapot)", [
        "A painted teapot. Wick & Barrow sell tea for the road as well, "
        "and there is a card about it in the window:",
        "A HERO RUNS ON TEA AND BOOTS. MOSTLY BOOTS."]),
    C("Outfitters' Window", (26, 8), "Window A", [
        "Boots in the window, on a card: WALKED NORTH AND BACK. ONE "
        "CAREFUL OWNER.",
        "The boots look as though they would rather not talk about "
        "it."]),
    C("Outfitters' Window", (33, 8), "Window A", [
        "A window display: a rucksack, a rope, a lantern, a tin of "
        "biscuits, and a little painted card: YOU WILL NEED A BIGGER "
        "RUCKSACK."]),
    C("The Wyvern's Sign", (9, 17), "Shop Sign (Pub)", [
        "A painted tankard, dented, with a bite out of one side.",
        "The bite is about the size and shape of a goose."]),
    C("The Inn Sign", (13, 17), "Shop Sign (Inn)", [
        "THE SLAIN WYVERN. ROOMS 25.",
        "The 25 has been painted over a 20, which was painted over a "
        "15. Underneath it all, if you look closely, a very faint 2."]),
    C("Guild Sign", (27, 17), "Shop Sign (Sword)", [
        "A sword on a painted board, held on with six bolts.",
        "The last sign had one bolt, and was taken by somebody who "
        "needed a sword more than the Guild did."]),
    C("Guild Crest", (31, 17), "Shop Sign (Crest)", [
        "The Guild's crest: a sword, a scroll, and a small question "
        "mark.",
        "The question mark is the provisional part."]),
    C("Guild Window", (26, 17), "Window A", [
        "Through the window: a long table, a very large ledger, and "
        "nobody at all. The Guild is open, provisionally."]),

    # --- the market
    C("Market Crate", (24, 15), "Crate B", [
        "Potatoes, under a card: SEA POTATOES.",
        "They are potatoes. In Nether Sopping, everything is sea "
        "something. They have a sea cat."]),
    C("Market Crate", (24, 16), "Crate E", [
        "Carrots, under a card: SEA CARROTS. They are, as far as you "
        "can tell, carrots."]),
    C("Market Crate", (25, 16), "Crate F", [
        "Fish, under a card: FISH.",
        "It is the only thing on the market that is exactly what it "
        "says it is, and the stallholder is very proud of it."]),
    C("Big Crate", (21, 17), "Large Crate", [
        "A big crate stencilled RETURN TO SENDER. Then, in another hand: "
        "SENDER UNKNOWN. Then, in a third: RETURN.",
        "It has been standing on the market waiting to be returned for "
        "some years."],
      trope="containers"),
    C("Barrel", (22, 19), "Barrel", [
        "A barrel of rainwater, with a notice: IF YOU WANT RAIN, HELP "
        "YOURSELF. WE HAVE PLENTY."]),
    C("Barrel", (17, 21), "Barrel", [
        "A barrel of salt. It is for the fish, and for the steps in "
        "winter, and for the occasional sea monster, which hates it."]),
    C("Well", (14, 20), "Well", [
        "A well. You look down it. A crab looks up.",
        "Harbour Rules, rule two: the crab is nobody's fault and is not "
        "to be provoked. You back away, politely."],
      trope="well"),
    C("Well", (26, 20), "Well", [
        "A well, with a bucket on a rope, and a sign: SEA WATER. DO NOT "
        "DRINK.",
        "You look over the edge. It is a long way down, and it smells "
        "of the beach. The sea, apparently, is also right there."]),
    C("Tub", (15, 22), "Basin A", [
        "A tub of eels, sold by the yard.",
        "You do not ask how they measure them. The eels would rather "
        "you didn't."]),
    C("Tub", (21, 22), "Basin A", [
        "A tub with an octopus in it. It is very relaxed, and has "
        "arranged itself so as to be holding the fishmonger's pencil."]),

    # --- the shore
    C("Net Rack", (2, 24), "Net Drying Rack (Left)", [
        "Nets on a drying rack, with a card tied to them: IF YOU ARE "
        "HERE ABOUT THE NET, THE NET IS ALSO SPOKEN FOR."]),
    C("Driftwood", (9, 24), "Fallen Log", [
        "Driftwood, bleached silver. Somebody has carved into it: K + M, "
        "WED 1972, and a small heart.",
        "Under it, in newer, deeper letters: STILL."]),
    C("Driftwood", (29, 24), "Fallen Log", [
        "A log on the beach. A gull is standing on it with the air of a "
        "gull that owns the log, and the beach, and has opinions about "
        "you."]),
    C("Bollard", (19, 29), "Mooring Bollard A", [
        "A mooring bollard, worn smooth by a hundred years of rope, and "
        "a hundred years of people sitting on it to look at the sea."]),
    C("Bollard", (21, 29), "Mooring Bollard A", [
        "Another bollard. There is a little brass plate on the top: "
        "THIS BOLLARD IS FOR BOATS. Under that, worn almost away: AND "
        "FOR GRANDAD."]),

    # --- the front door nobody answers (Ambrose Fitch's, `south.py` 15),
    # whose own page mentions "a pot with a dead thing in it". The dead
    # thing was a `Dead Grass A` tile on layer 3, which is passable and
    # made the pot walkable; it is the event's own sprite now, raised into
    # the pot's mouth (Mike, 5 Nov 2026).
    C("Pot", (15, 9), "Pot", [
        ["A pot by the front door, and in it something that",
         "was a plant once. A card in the soil says:",
         "PLEASE WATER."],
        ["It stands under the eaves, where the rain cannot",
         "reach it. In Nether Sopping, that makes it the only",
         "plant in town to have died of thirst."]],
      sprite=K.sf_tile("Outside_B", "Dead Grass A"), offset=(-1, -14)),
]

# ------------------------------------------------ Map 15, the Guild --
GUILD = [
    C("The Guild's Map", [(8, 3), (9, 3)], "World Map", [
        "A map of the world, as far as the Guild has got. North of the "
        "Tower it says HERE BE DRAGONS.",
        "Somebody has corrected that to HERE BE ONE DRAGON. Somebody "
        "else has added: RETIRED. SHE IS VERY NICE. TAKE A CAKE."],
      trope="world_map"),
    C("Drawers", (15, 4), "Chest of Drawers", [
        "A chest of drawers, labelled IN, OUT, PENDING and PROVISIONAL.",
        "You open PENDING. It is full of forms, every one of them waiting "
        "for another form.",
        ("Pell", "Do help yourself. There is a form for that as well. "
                 "It is in PENDING.")],
      then=[["You try OUT. It is empty. Everything in it has gone out.",
             ("Pell", "Splendid. Now you have looked in two drawers, and "
                      "we are both a little older.")]],
      again=["IN, OUT, PENDING, PROVISIONAL. Registrar Pell does not look "
             "up, which is somehow worse."],
      trope="rummage"),
    C("Planter", (3, 4), "Planter A", [
        "A box of petunias, flowering provisionally."]),
    C("Pell's Note", (8, 6), "Note A (V)", [
        "A note on the Registrar's desk: FORM 7B REQUIRES FORM 7A. FORM "
        "7A HAS BEEN MISLAID. SEE FORM 7B."]),
    C("The Members' Book", (10, 6), "Open Book A (V)", [
        "The register of members. Under MEMBERS: Pell (Registrar).",
        "Under PROVISIONAL MEMBERS, everybody who has ever come in "
        "through that door - including, you notice, you, as of a "
        "minute ago."]),
    C("Old Quests", (11, 9), "Scrolls A", [
        "Quests nobody took. RESCUE CAT FROM TREE (CAT CAME DOWN). CLEAR "
        "THE CELLAR OF RATS (THEY'RE FINE, LEAVE THEM).",
        "TAKE THIS LETTER TO THE NEXT TOWN (IT IS FOR US. WE ARE THE "
        "NEXT TOWN)."],
      trope="rat_cellar"),
    C("A Note", (12, 9), "Note A (V)", [
        "A note: THE GUILD WILL BE CLOSED ON TUESDAY FOR THE REVIEW.",
        "It is very yellow. It is not saying which Tuesday."]),
    C("Barrel", (15, 10), "Barrel", [
        "A barrel of wooden practice swords marked FOR INDUCTIONS. "
        "There have been no inductions. The swords are as good as "
        "new."]),
    C("Guild Swords", (15, 11), "Sword Rack A", [
        "The Guild's swords, for issue to members. Each one was signed "
        "out on a little card.",
        "Every card says RETURNED: PENDING."]),
]

# -------------------------------------------------- Map 16, Wick & Barrow --
OUTFITTERS = [
    C("Rations", [(4, 4), (3, 4), (5, 4)], "Bread Shelf", [
        "Rations for the road: hard tack, harder tack, and a tin marked "
        "HARDEST TACK (FOR TEETHING DRAGONS)."]),
    C("Chalk and Rope", (6, 4), "Sundries Shelf A", [
        "Rope, lanterns, and chalk, for marking the walls of a dungeon "
        "so you can find your way out.",
        "A card: CHALK - ONE CROWN. FINDING YOUR WAY OUT - NOT "
        "INCLUDED."]),
    C("Tailor's Dummy", (8, 4), "Women's Clothing C (Stand)", [
        "A tailor's dummy in a blue travelling coat, with a card: AS "
        "WORN BY A CHOSEN ONE.",
        "Smaller: WHICH ONE IS NOT SPECIFIED. ALL OF THEM, PROBABLY."]),
    C("Ten-Foot Poles", [(11, 4), (12, 4)], "Sundries Shelf A", [
        "A card on the shelf: EVERY ADVENTURER NEEDS A TEN-FOOT POLE. The poles"
        " are round the back. They would not fit on the shelf.",
        "It does not say what for. Nobody has ever said what for. "
        "Everybody buys one."],
      trope="ten_foot_pole"),
    C("Camping", (13, 4), "Sundries Shelf B", [
        "Bedrolls, a tent, and one very optimistic deckchair."]),
    C("Lamp Oil", (11, 6), "Bottle D", [
        "Bottles of lamp oil, and one labelled DRAGON REPELLENT.",
        "The small print says: IT IS LAMP OIL. THROW IT HARD."]),
    C("Boot Polish", (12, 8), "Basin", [
        "A tub that used to hold boot polish. It is empty, and still the "
        "strongest smell in Nether Sopping, which is saying something."]),
    C("Boots", [(3, 9), (4, 9)], "Crate B", [
        "Crates of boots, sorted by size, and then by how far north they "
        "have been."]),
    C("Returns", (13, 9), "Crate B", [
        "A crate marked RETURNS: compasses, every one of them pointing "
        "at the Gilded Turnip in Thistlewick.",
        "Nobody knows why. Mrs Barrow says it is a known fault."]),
]

# ------------------------------------- Map 17, Number Forty-Five's Cottage --
QUY = [
    C("Crates", [(5, 4), (6, 4)], "Stacked Crates", [
        "Crates, stacked squarely and labelled in a careful hand: SEEDS. "
        "MORE SEEDS. SEEDS (ROSES).",
        "SEEDS (NOT TURNIPS)."]),
    C("Supper", (8, 4), "Dinner Set A (Bottom)", [
        "A small supper for one, laid properly, with a napkin, because "
        "that is how it is done."]),
    C("Water Butt", (12, 4), "Barrel", [
        "A water butt for the roses. It is the best-kept barrel in the "
        "south, and somebody has painted it green to match."]),
    C("Wardrobe", (3, 9), "Closet", [
        "A wardrobe. In stories, a wardrobe is a way into another "
        "world, and you put your hand on the handle.",
        "You open it. Coats, and behind the coats more coats, and behind "
        "those the back of the wardrobe, which you knock on, twice, to be "
        "sure.",
        ("Halbert Quy", "It is a wardrobe, young man. If you want another "
                        "world, the back door is through there. It is the "
                        "garden.")],
      again=["Coats. Mr Quy's, all brushed, all for later."],
      trope="wardrobe"),
    C("Bedside Table", (5, 9), "Table F", [
        "Roses in a bowl, a pair of reading glasses, and a seed catalogue, open"
        " at ROSES and underlined in three colours."]),
    C("Tea", (10, 9), "Cup (Upper Right)", [
        "A cup of tea with the saucer on top to keep it warm.",
        "Halbert Quy is a man who keeps things for later."]),
    C("A Rose", (13, 11), "Potted Plant A", [
        "A rose in a pot, flowering in quite the wrong season, because "
        "it has been looked after so well that it does not know any "
        "better."]),
]

# ------------------------------------------- Map 72, the Wyvern upstairs --
GUEST_BOOKS = [
    ["Books left behind by guests. ESCAPING FROM DUNGEONS FOR "
     "BEGINNERS, by somebody who left without paying."],
    ["A COMPLETE AND ACCURATE HISTORY OF THE OBLIGATORY QUEST, Volume "
     "One, by Hosea Bellwether. It is a pamphlet.",
     "Volume Two is downstairs, and is the size of a door."],
    ["WYVERNS OF THE COAST: A GUIDE. Somebody has stuck a picture of a "
     "goose in the front."],
    ["THE CHOSEN ONE'S COOKBOOK. Every recipe begins: 'First, be "
     "chosen.'"],
    ["A romance, THE KNIGHT WHO CAME HOME. The last chapter has been "
     "read so often that it has come loose, and somebody has tied it "
     "back in with a ribbon."],
    ["A HUNDRED THINGS TO DO IN NETHER SOPPING. Ninety-nine of them "
     "are 'look at the sea'."],
]

UPSTAIRS = [
    C("Bed", (3, 5), "Bed", [
        "A bed, with a card on the pillow: A CHOSEN ONE SLEPT HERE.",
        "Underneath: SO DID ALL THE OTHERS. IT IS THAT SORT OF INN."]),
    C("Bed", (8, 5), "Bed", [
        "A bed with a dip in the middle exactly the shape of a man in "
        "full plate armour.",
        "Dorcas has tried everything. The bed remembers him."]),
    C("Bedside Flowers", (5, 4), "Table F", [
        "Flowers on the bedside table, and a card: PICKED BY SOPS.",
        "They are mostly dandelions. They have been arranged with "
        "enormous care."]),
    C("Washstand", (11, 9), "Basin", [
        "A washtub and a jug. The water is cold, a little salty and "
        "faintly fishy, which in Nether Sopping is what fresh means."]),
    C("Lost Property", (19, 11), "Chest of Drawers", [
        "Drawers marked LOST PROPERTY. Gloves, a single boot, a monocle, "
        "and a ring of keys to a castle in some other story, labelled "
        "PLEASE RETURN."]),
    C("More Lost Property", [(20, 11), (21, 11)], ("Sundries Shelf A",
                                                   "Sundries Shelf B"), [
        "What the drawers would not hold: jars, a pink rabbit, and a teddy "
        "with one ear mended and mended again. The heroes heal overnight in "
        "the beds here, and the teddy never does."],
      trope="cheap_inn"),
    C("Mirror", (7, 12), "Mirror", [
        "A long mirror on the landing. You look tired. It is a long way "
        "from Thistlewick, and the mirror is in no mood to pretend "
        "otherwise."]),
    C("Clock", (16, 12), "Clock", [
        "A tall clock that chimes the quarters. Somebody has stopped "
        "the chime between three and four in the morning, which is when "
        "the adventurers get in."]),
    C("Crates", [(3, 13), (4, 13)], "Stacked Crates", [
        "Crates of spare stools, all mended. A tally chalked on the lid: "
        "STOOLS STOOD ON BY BARDS - 41."],
      party=[(db.PIPER, [("Piper", "Forty-one? Somebody's been standing "
                          "on stools in my name.")])]),
    C("Guests' Books", [(10, 13), (11, 13)], "Bookshelf B",
      GUEST_BOOKS[0], then=GUEST_BOOKS[1:3]),
    C("Guests' Books", [(12, 13), (13, 13)], "Bookshelf B",
      GUEST_BOOKS[3], then=GUEST_BOOKS[4:]),
    C("Potted Plant", (3, 15), "Potted Plant A", [
        "A potted plant on the landing, watered every morning by Sops, "
        "whether it needs it or not. It is the wettest plant in the "
        "wettest town on the coast."]),
]

# ------------------------------------------- Map 18, Saint Bother's light --
# Six floors side by side. Ferrety Bother keeps it for the people coming
# home down the north road; the jokes are the family's, and fond.
KEEPERS_BOOKS = [
    ["THE KEEPER'S HANDBOOK. Rule one: keep the light lit.",
     "There is no rule two. There has never been any need for one."],
    ["LIGHTHOUSES I HAVE KNOWN, by S. Bother. It is a very short book. "
     "She only knew the one, and she did not think much of the others "
     "anyway."],
    ["KNITTING FOR KEEPERS, with a pattern for a jumper with a "
     "lighthouse on it, and a pattern for a lighthouse with a jumper on "
     "it, for the winter."],
    ["A BOOK OF COAST BIRDS, kept by four generations of Bothers. Every "
     "entry says GULL.",
     "One says NOT A GULL (?). The next one says GULL."],
    ["THE TIDES, AND WHY. Somebody has written in the margin: THEY "
     "DON'T SAY."],
    ["A book of ghost stories for keepers on long nights. Every story "
     "ends with the keeper lighting the lamp and the ghost going home, "
     "satisfied."],
]

LIGHTHOUSE = [
    # --- the mess, on the ground floor
    C("Oil Barrel", (3, 4), "Barrel", [
        "A barrel marked LAMP OIL. You knock on it. It is hollow all the "
        "way down."]),
    C("Tapestry", (6, 3), "Tapestry A", [
        "A tapestry: Saint Bother, with a lantern, glaring at a ship.",
        "The ship looks very sorry."]),
    C("Tapestry", (9, 3), "Tapestry A", [
        "Saint Bother again, telling off a storm.",
        "The storm is leaving."]),
    C("Tapestry", (13, 3), "Tapestry A", [
        "Saint Bother in a deckchair with her feet up and the lamp lit, "
        "and, embroidered underneath by a great-grandson: SHE'D HAVE "
        "HATED THE FUSS."]),
    C("Ship Bottles", (7, 4), "Bottle Shelf A", [
        "A shelf of bottles with little ships inside. The keepers made "
        "one for every ship that passed the point.",
        "The last is from 1909. After that the ships stop, and the "
        "bottles go on: one a year, each with a tiny lighthouse in it, "
        "lit."]),
    C("Plates", (11, 4), "Dish Cabinet", [
        "Plates for thirty, from when the light had a crew.",
        "Ferrety uses one plate and washes it, and dusts the other "
        "twenty-nine on Sundays."]),
    C("Wine Rack", (12, 4), "Wine Rack", [
        "A wine rack, full. Every bottle in it is vinegar that used to be wine,"
        " a long time ago, and has made its peace with it."]),
    C("Water Barrel", (13, 5), "Basin", [
        "A rain tub, with a ladle chained to it. The chain is older "
        "than the ladle, and the ladle is older than Ferrety."]),
    C("A Bottle", (7, 10), "Bottle B", [
        "A bottle with a message in it, and you can read it through the "
        "glass: IF FOUND, PLEASE RETURN TO THE LIGHTHOUSE.",
        "It is in the lighthouse. Somebody has, technically, returned "
        "it."],
      trope="message_bottle"),

    # --- the store, second floor
    C("Oil Barrels", [(29, 5), (29, 4)], "Barrel", [
        "Barrels marked OIL, OIL, OIL and OIL. You knock on each.",
        "Hollow, hollow, hollow and hollow."]),
    C("Wick Jar", (30, 5), "Pot B", [
        "A jar of old wicks, trimmed square, each tagged with its year. "
        "The jar is very full and the years go back a very long way."]),
    C("Lens Crates", [(33, 4)], "Stacked Crates", [
        "Crates of spare lenses, packed in straw, for a lamp that has "
        "had the same lens since it was built and is not about to "
        "change now."],
      trope="containers"),
    C("Biscuit Crate", (32, 8), "Crate D", [
        "Ship's biscuit, in a crate stencilled 1908.",
        "It is the same biscuit they sell in Nether Sopping. You suspect "
        "it is from the same batch."]),
    C("Sandbags", [(32, 11), (33, 11)], "Sacks C", [
        "Sacks of sand, for the steps in winter, and for putting out the "
        "lamp if it ever gets ideas above its station."]),
    C("Flour", (31, 11), "Sack B", [
        "A sack of flour with a scoop in it, and one very contented "
        "mouse, who has been told, and has not listened."]),

    # --- the keeper's room, third floor
    C("Wardrobe", (49, 4), "Closet", [
        "Ferrety's wardrobe. You open it, remember whose it is, and shut "
        "it again.",
        "You saw a very large number of identical jumpers. All of them "
        "have a lighthouse on."]),
    C("Clock", (48, 6), "Clock", [
        "A clock, wound every evening at lighting-up time. It is very "
        "punctual. It has not had much to be punctual for, lately."]),
    C("Bedside Table", (52, 4), "Table D", [
        "A bedside table, and on it a nightcap with a little lighthouse "
        "embroidered on the bobble."]),
    C("Supper", (53, 8), "Dinner Set C (Left)", [
        "Supper: a chop, a bowl of soup, and a book propped against the glass, "
        "open at the same page as yesterday.",
        "It is SHIPS OF THE COAST. The page is about a ship that "
        "waved."]),
    C("Window", (47, 3), "Large Window D", [
        "A window looking inland. On a clear night you could see the "
        "crossroads from here, where the north road comes down.",
        "You could see a light from there, too, if there was one."]),

    # --- the pantry and the books, fourth floor
    C("Bread", (69, 4), "Bread Shelf", [
        "Loaves, wrapped in cloth, and a tin of the Sopping biscuit for "
        "emergencies. The tin says EMERGENCIES ONLY. It is nearly "
        "empty."]),
    C("Bottles", (72, 4), "Bottle Shelf A", [
        "Jars of pickled samphire, pickled cockles, and pickled something "
        "that Ferrety's grandmother found on the rocks and was never "
        "able to name."]),
    C("Keepers' Books", [(71, 7), (72, 7)], "Bookshelf B",
      KEEPERS_BOOKS[0], then=KEEPERS_BOOKS[1:3]),
    C("Keepers' Books", (73, 7), "Bookshelf A",
      KEEPERS_BOOKS[3], then=KEEPERS_BOOKS[4:]),
    C("Barrels", (69, 11), "Barrel", [
        "Barrels of salt, stacked three deep. A lighthouse on a rock "
        "keeps a great deal of salt for no reason anybody can give, and "
        "the sea brings more."]),

    # --- the watch room, fifth floor
    C("Map of the Coast", [(89, 2), (90, 2)], "World Map", [
        "A chart of the coast, with every rock and wreck marked in red "
        "ink and every ship that ever got past in green.",
        "There is a great deal more green than red. Somebody was very "
        "good at this."]),
    C("Old Logs", (90, 4), "Closed Books C", [
        "The old logbooks, before the one that is open. NO SHIP. LIGHT "
        "LIT. Before that: SHIP. LIGHT LIT. SHIP WAVED. Before that, in "
        "a much older hand: GOT HER IN."]),
    C("Pen", (92, 4), "Pen A", [
        "A pen and a pot of ink. The nib is worn into the shape of the "
        "words LIGHT LIT."]),
    C("Watch Shelf", (93, 4), "Bookshelf A", [
        "Almanacs of the sky, one a year, for working out when it will be "
        "dark enough to bother with the light.",
        "In this lighthouse, that is the family joke, and they have made "
        "it every year for a hundred years."]),
]

# -------------------------------------------------- Map 9, the Gloamwood --
GLOAMWOOD = [
    C("Beanstalk", (8, 7), "Beanstalk", [
        "A beanstalk, going straight up into the canopy, where it stops, "
        "as though it had thought better of it.",
        "There is a little card nailed to the bottom: GIANT NOT IN. "
        "PLEASE DO NOT CLIMB. THIS MEANS YOU, JACK."],
      trope="beanstalk"),
    C("Mushrooms", (8, 11), "Mushrooms A", [
        "Pale mushrooms in a neat little row, as though somebody had "
        "planted them, which in the Gloamwood is not out of the "
        "question."],
      party=[(db.WREN, [("Wren", "Edible. Delicious, actually. Tell "
                         "nobody, or there'll be a society.")]),
             (db.MERRI, [("Merribell", "Don't. Not even if Wren says. "
                          "Especially if Wren says.")])]),
    C("Mushrooms", (10, 12), "Mushrooms B", [
        "Red mushrooms with white spots, the kind in every picture book "
        "with a gnome sitting on top.",
        "There is no gnome. There is a very small dent in the top of the "
        "biggest one, as if one had just left."]),
    C("Log", (13, 13), "Fallen Log", [
        "A fallen log, hollow, with a hand-lettered sign at one end: "
        "SEARCHED.",
        "Somebody has been along the whole path with these. It saves "
        "everybody a great deal of time."],
      trope="hollow_log"),
    C("Dead Beanstalk", (24, 13), "Dead Beanstalk", [
        "A dead beanstalk. Somebody had a go. Somebody else, by the look "
        "of the footprints, had a go at climbing it anyway."]),
    C("Boulder", (27, 16), "Boulder A", [
        "A boulder, hunched over in exactly the shape of a sleeping "
        "troll.",
        "You check. It is a boulder. You check again from the other side, "
        "to be sure. Still a boulder."],
      then=[["You check a third time. It is a boulder, and you are "
             "beginning to feel that it knows."]],
      again=["The boulder. Still a boulder. Probably."]),
    C("Log", (8, 22), "Fallen Log", [
        "A log across the path, with a cushion on it, and a little card "
        "on the cushion: RESERVED - NUMBER FORTY-SIX."]),
    C("Dead Beanstalk", (19, 22), "Dead Beanstalk", [
        "Another dead beanstalk, with a little wooden marker in front of "
        "it like a gravestone: HERE LIES A MAGIC BEAN. IT WAS NOT."]),
    C("Boulder", (5, 23), "Boulder A", [
        "A boulder with an arrow chalked on it pointing north, and under "
        "it, chalked by a different hand: ARE YOU SURE?"]),
    C("Mushrooms", (25, 26), "Mushrooms B", [
        "More red mushrooms. One of them has a tiny door painted on the "
        "stalk, very carefully, by somebody with a very fine brush and "
        "a great deal of hope."]),
    C("Log", (16, 30), "Fallen Log", [
        "A mossy log. The moss grows on the north side, as the books "
        "say it should. Somebody has nailed a small sign to the south "
        "side: OTHER WAY."]),
]

# ------------------------------------- Map 10, the Bit With The Thing --
THE_BIT = [
    C("Mushroom Ring", (12, 9), "Mushrooms B", [
        "A ring of mushrooms round the clearing, very large, very "
        "even, and very obviously magic.",
        "The Gloamwood Society has put a little rope round it, and a "
        "sign: SITE OF SPECIAL INTEREST. DO NOT DANCE IN."],
      trope="fairy_ring"),
    C("Mushrooms", (18, 9), "Mushrooms B", [
        "Part of the ring. A small label on a stick: MUSHROOM 14 OF 31. "
        "THE SOCIETY COUNTS THEM EVERY YEAR.",
        "There were thirty-one last year as well. It is the most "
        "exciting thing that has happened to the Society."]),
    C("Dead Beanstalk", (14, 12), "Dead Beanstalk", [
        "A beanstalk, dead, with a scratching post's worth of claw marks "
        "on it, at about the height of something very big that likes to "
        "scratch its back."]),
    C("Bones", (6, 18), "Bones A", [
        "Bones, and a little sign beside them in the Society's "
        "handwriting:",
        "THESE ARE A SHEEP'S. THE SOCIETY HAS CHECKED. IT WAS A VERY OLD "
        "SHEEP AND IT DIED HAPPY. PLEASE STOP REPORTING IT."]),
    C("Log", (19, 19), "Fallen Log", [
        "A log with a flask, a sandwich box, and a notebook on it, all "
        "labelled G.S. - the Society's picnic spot, forty years in the "
        "same place."]),
    C("Mushrooms", (7, 20), "Mushrooms A", [
        "Pale mushrooms. The Society has given each one a name. This one "
        "is called Norman."],
      party=[(db.WREN, [("Wren", "That's not a Norman. That's a Cyril "
                         "if ever I saw one. I'll write to them.")])]),
]

# ------------------------------------------ Map 19, the Bottomless Pit --
PIT = [
    C("Pickaxe", (10, 17), "Pickax", [
        "A pickaxe, left by somebody who came down to dig for the bottom "
        "of the pit.",
        "They found it almost straight away, and left in a hurry, "
        "embarrassed."]),
    C("Broken Pot", (15, 22), "Pot A (Ruins)", [
        "A broken pot. In it, one sock."]),
]

# ------------------------------------ Map 20, the Barrow of the 44th --
BARROW = [
    C("Pillar", (19, 4), "Stone Pillar B (Moss)", [
        "A mossy pillar. Low down on it, at about the height of a big "
        "dog's shoulder, the moss has been worn smooth by something "
        "leaning there for a very long time, every day, very "
        "contentedly."]),
]

ALL = {9: GLOAMWOOD, 10: THE_BIT, 13: SOPPING, 14: WYVERN, 15: GUILD,
       16: OUTFITTERS, 17: QUY, 18: LIGHTHOUSE, 19: PIT, 20: BARROW,
       72: UPSTAIRS}
