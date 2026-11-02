"""CURIOS.md wave C4: the sites - Maps 28-48.

Each site is one joke built into a place (SITES.md): the tutorial meadow,
the last town before the end, nineteen inns on one street, and so on. Its
curios stay inside that joke and do not explain it."""

import db
from curios import curio as C

# ----------------------------------------------- Map 28, Firstfield Meadow --
MEADOW = [
    C("Long Board", [(3, 7), (2, 7), (4, 7), (5, 7)], "Sign B", [
        "A long board: CONTROLS. UP IS UP. DOWN IS DOWN.",
        "LEFT AND RIGHT ARE ALSO AVAILABLE. THE GUILD OF GUIDES RECOMMENDS "
        "TRYING ALL FOUR."],
      trope="tutorial"),
    C("Long Board", [(17, 7), (16, 7), (18, 7), (19, 7)], "Sign B", [
        "A long board: REMEMBER - YOU MAY SAVE YOUR PROGRESS AT ANY TIME.",
        "You always could. It is a great weight off your mind anyway."]),
    C("Tutorial Barrel", (8, 14), "Barrel", [
        "A barrel with a label: BARREL (FOR PRACTICE).",
        "Inside, at the bottom, another label: WELL DONE. YOU HAVE "
        "SEARCHED A BARREL. THERE WILL BE MANY MORE."],
      trope="containers"),
    C("Resting Log", (9, 14), "Fallen Log", [
        "A log with a small sign: SIT HERE TO REST.",
        "And smaller: RESTING DOES NOTHING. IT IS FOR THE ATMOSPHERE."]),
    C("Sheep Trough", (20, 14), "Basin A", [
        "A water trough labelled SHEEP WATER. The sheep drink from it "
        "with enormous dignity, and do not look round.",
        "They are pigs."]),
    C("Log", (3, 15), "Fallen Log", [
        "A log with a label: OBSTACLE (EASY). You walk round it. A small "
        "voice somewhere in the meadow cheers."]),
]

# ------------------------------------------------------- Map 29, Penultima --
PENULTIMA = [
    C("Shoppe Sign", (9, 9), "Shop Sign (Sword)", [
        "YE FINAL SHOPPE - LAST SWORDS FOR TWO HUNDRED LEAGUES.",
        "Chalked under it: LAST POTIONS. Under that: LAST SPOONS. Under "
        "that: LAST CHANCE TO BUY A SPOON, REALLY, THINK ABOUT IT."]),
    C("Shoppe Teapot", (10, 9), "Shop Sign (Teapot)", [
        "A painted teapot. Ye Final Shoppe also does a final cup of tea, "
        "at a price which is also final."]),
    C("Shoppe Window", (12, 9), "Window A", [
        "Through the window: Gideon, polishing the sword in the window "
        "from the inside.",
        "He sees you looking. He polishes harder."]),
    C("Outfitters' Sign", (19, 9), "Shop Sign (Armor)", [
        "A painted breastplate over the boarded shop: ULTIMATE "
        "OUTFITTERS. CLOSED FOR THE SEASON.",
        "The season has been going on for some time."]),
    C("Outfitters' Window", (22, 9), "Window A", [
        "Through a crack in the boards: a shop exactly like Ye Final "
        "Shoppe, with everything in it priced at exactly one crown "
        "less."]),
    C("Barrel", (6, 13), "Barrel", [
        "A barrel with a price on it. You look inside. It is empty. The "
        "price is for the barrel."]),
    C("Well", (11, 13), "Well", [
        "A well, with a sign: LAST WELL BEFORE THE END. ONE CROWN A "
        "BUCKET.",
        "Smaller: SEASONAL."]),
    C("Well", (21, 13), "Well", [
        "Another well. Its sign says: LAST WELL BEFORE THE END (THE "
        "OTHER ONE). HALF A CROWN A BUCKET. TELL NOBODY."]),
    C("Barrel", (25, 13), "Barrel", [
        "A barrel with a card on it: THIS BARREL HAS BEEN SEARCHED BY A "
        "CHOSEN ONE.",
        "In Penultima that is a selling point, and the barrel is priced "
        "accordingly."]),
    C("House Window", (5, 18), "Window A", [
        "Through the window: a family at their supper. There is still a "
        "price tag on the teapot. They stopped noticing years ago."]),
    C("House Window", (21, 18), "Window A", [
        "Through the window: a man counting his money very slowly, for "
        "the pleasure of it, and then counting it again."]),
    C("Log", (25, 4), "Fallen Log", [
        "A log at the top of the town, with a little sign: LAST LOG. "
        "Somebody has priced it."]),
]

# ------------------------------------------------- Map 30, Ye Final Shoppe --
SHOPPE_BOOKS = [
    ["A shelf of books for sale, every one LAST BOOK BEFORE THE END. You "
     "check a title: HOW TO HAGGLE.",
     "It is marked NOT FOR SALE."],
    ["THE MARKUP ACCOUNTS, VOLUME ONE. You open it at the first page. "
     "The first entry is in Gideon's hand:",
     "DISCOUNT - ELEVEN COPPERS - WORTH IT."],
    ["A slim book, PRICING FOR BEGINNERS. Chapter one: think of a "
     "number. Chapter two: double it."],
]

SHOPPE = [
    C("Potions", (3, 4), "Sundries Shelf A", [
        "Potions, each one labelled LAST POTION.",
        "There are forty of them."],
      trope="last_shop"),
    C("Antidotes", (4, 4), "Sundries Shelf B", [
        "Antidotes. Each price tag has been crossed out and doubled, and "
        "crossed out and doubled again. A card: SEASONAL."]),
    C("Wine Rack", (5, 4), "Wine Rack", [
        "Bottles of FINAL WINE.",
        "Underneath the card, in Dorothy's writing: (IT IS NOT. WE HAVE A "
        "CELLAR.)"]),
    C("Rope", (11, 4), "Sundries Shelf A", [
        "Rope, sold by the yard, priced by the inch."]),
    C("Books", (12, 4), "Bookshelf A", SHOPPE_BOOKS[0],
      then=SHOPPE_BOOKS[1:]),
    C("Stock", (13, 4), "Sundries Shelf A", [
        "Every item on this shelf has the same little card: WE BUY AT "
        "ONE CROWN. WE SELL AT FORTY. ASK ABOUT OUR WARRANTY.",
        "There is no warranty. Asking about it is free."]),
    C("Umbrellas", (13, 6), "Pot B", [
        "A big jar, tied shut, with a card: UMBRELLAS - THE LAST ONE. It is "
        "next to another jar with a card: UMBRELLAS - THE LAST ONE."]),
    C("The Ledger", (3, 7), "Open Book A (V)", [
        "Dorothy's ledger. Every page balances.",
        "In the margin of every page, very small: G. WAS HONEST TODAY. A "
        "few of them have a little question mark after it."]),
    C("Rings", (4, 7), "Case A", [
        "A gilt case of rings, locked, and every price tag hanging out of it "
        "reads MAKE AN OFFER.",
        "Under one, in Gideon's writing: (NOT THAT ONE). It is a plain "
        "gold band, old, and very well polished."]),
    C("Bottles", (11, 7), "Bottle D", [
        "Bottles on the counter with a card: BUY ONE, GET ONE AT THE "
        "FULL PRICE."]),
    C("The First Crown", (12, 7), "Case A", [
        "A gilt case, locked, with a card on the lid: INSIDE - THE FIRST "
        "CROWN THIS SHOPPE EVER TOOK. NOT FOR SALE.",
        "Underneath, in smaller letters: (OFFERS)."]),
    C("Stock Crate", (3, 10), "Crate B", [
        "A crate of things Gideon bought for one crown each: a boot, a "
        "slime in a jar, half a potion.",
        "He is waiting for somebody who needs exactly half a potion. He "
        "is sure they are on their way."]),
]

# -------------------------------------------------------- Map 31, Restwell --
RESTWELL = [
    C("Inn Sign", (26, 10), "Shop Sign (Inn)", [
        "THE FOUR HOURS. FOR THE BUSY HERO.",
        "A card hangs underneath: CLOSED. GONE TO BED."]),
    C("Inn Sign", (8, 11), "Shop Sign (Inn)", [
        "THE NINE HOURS. FOR THOSE WHO FIND EIGHT A LITTLE RUSHED."]),
    C("Bar Sign", (9, 11), "Shop Sign (Pub)", [
        "THE NIGHTCAP. OPEN ALL NIGHT, FOR THOSE WHO CANNOT SLEEP.",
        "In Restwell, that is nobody. The landlord has never served a "
        "single drink, and is very well rested."]),
    C("Bar Sign", (19, 19), "Shop Sign (Pub)", [
        "THE LIE-IN. BREAKFAST SERVED UNTIL FOUR."],
      trope="cheap_inn"),
    C("Window", (21, 10), "Window A", [
        "Through the window of the Seven Hours: rows of made beds, and a "
        "clock on the wall an hour fast, so the guests feel rested "
        "sooner."]),
    C("Window", (27, 10), "Window A", [
        "Through the window: somebody asleep at a breakfast table, very "
        "contentedly, still holding a spoon."]),
    C("Window", (11, 11), "Window A", [
        "Through the window: a dormitory, and a sign over the beds: "
        "SILENCE PLEASE - GUESTS SLEEPING.",
        "It is the noisiest room in Restwell. The snoring rattles the "
        "glass."]),
    C("Barrel", (2, 12), "Barrel", [
        "A barrel of pillows. Restwell orders its pillows by the "
        "barrel."]),
    C("Barrel", (24, 12), "Barrel", [
        "A barrel of spare nightcaps, sorted by inn, with a tassel in "
        "each inn's colours."]),
    C("Well", (12, 17), "Well", [
        "The town well. A sign: PLEASE DRAW WATER QUIETLY. PEOPLE ARE "
        "SLEEPING.",
        "In Restwell, people are always sleeping."]),
    C("Barrel", (12, 21), "Barrel", [
        "A water barrel with a sign: FOR WAKING GUESTS. USE SPARINGLY.",
        "Underneath, in a different hand: USE NEVER."]),
    C("Log", (12, 3), "Fallen Log", [
        "A log at the edge of town, worn into a comfortable dip by "
        "travellers who could not quite make it as far as the inns, and "
        "slept here instead, very well."]),
]

# --------------------------------------------------- Map 32, the Eight Hours --
EIGHT_HOURS = [
    C("Preserves", (3, 4), "Sundries Shelf A", [
        "Mrs Ashbury's preserves, labelled by the hour they are for: SIX "
        "O'CLOCK JAM. SEVEN O'CLOCK MARMALADE. NOON MARMALADE (FOR "
        "LATE RISERS)."]),
    C("Cocoa", (4, 4), "Sundries Shelf B", [
        "Tins of cocoa. Enough cocoa to put the whole of Restwell to "
        "sleep, which, Mrs Ashbury says, it already has."]),
    C("Jars", (5, 4), "Sundries Shelf A", [
        "Jars of honey, every one with a little woollen hat on the lid, "
        "to keep it warm, which honey does not need, but which Mrs "
        "Ashbury enjoys knitting."]),
    C("Bread", (6, 4), "Bread Shelf", [
        "Loaves for breakfast. A card: BAKED WHENEVER. SERVED WHENEVER."]),
    C("The Bell", (4, 6), "Bell", [
        "A brass bell on the bar: RING FOR SERVICE.",
        "You ring it. Upstairs, somebody turns over."]),
    C("Half a Breakfast", (6, 6), "Dinner Set C (Left)", [
        "Somebody's breakfast, half eaten, with a note on the plate: "
        "BACK AFTER A NAP."]),
    C("Candles", (3, 7), "Crate A", [
        "A crate of candles. Every one is exactly eight hours long."]),
    C("Breakfast Table", (6, 8), "Dinner Set C (Left)", [
        "A table laid for breakfast, which in Restwell is served after lunch, "
        "and is therefore a chop. The salt has a little knitted hat on. So, you"
        " notice, does the pepper."]),
    C("Tonic", (12, 8), "Bottle C", [
        "A bottle by Dr Pike's chair labelled TONIC - DR PIKE.",
        "It is cold tea. Dr Pike has never once claimed otherwise."],
      party=[(db.MERRI, [("Merribell", "Cold tea is a perfectly good "
                          "tonic. Don't tell him I said so.")])]),
    C("Lavender", (20, 7), "Pot B", [
        "A pot of lavender by the beds, for sleeping. It is strong "
        "enough to make the pot sleepy."]),
    C("Window", (8, 3), "Large Window A", [
        "A window with thick curtains, drawn at noon, as is the custom "
        "in Restwell."]),
    C("Potted Plant", (17, 4), "Potted Plant A", [
        "A potted plant, very well rested."]),
]

# -------------------------------------------------------- Map 33, Hithermost --
HITHERMOST = [
    C("Chapel Glass", (6, 12), "Stained Glass Window B", [
        "Stained glass: a saint going into a mountain.",
        "In the next panel, the same saint coming out of a chapel porch, "
        "looking puzzled."],
      trope="respawn"),
    C("Chapel Glass", (10, 12), "Stained Glass Window B", [
        "Stained glass: a saint writing her name in a book. And again. "
        "And again, smaller, to make it fit."]),
    C("Tea Room Sign", (19, 18), "Shop Sign (Eatery)", [
        "A painted plate and spoon: TEAS. HOT FOOD.",
        "A card underneath: KETTLE PERMITTING."]),
    C("Tea Room Window", (22, 18), "Window A", [
        "Through the window: the tea room's tables, all laid, and a gap "
        "on the counter exactly the shape of a kettle."]),
    C("Barrel", (21, 19), "Barrel", [
        "A barrel of tea, nearly empty. The chapel has borrowed most of "
        "it. The chapel always has."]),
    C("Window", (7, 20), "Window A", [
        "Through the window: rope, maps, boots, a kettle, all ready by "
        "the door - and a calendar with GONE UP written on every "
        "Tuesday."]),
    C("Well", (11, 20), "Well", [
        "The village well. A sign: LAST WATER BEFORE THE MOUNTAIN.",
        "And under it: FIRST WATER AFTER (SEE CHAPEL)."]),
    C("Barrel", (9, 21), "Barrel", [
        "A barrel of candles labelled FOR THE BOOK. Brother Quillon gets "
        "through a great many candles."]),
    C("Window", (22, 27), "Window A", [
        "Through the window: a hall with pots in it. A great many more "
        "pots than any hall needs.",
        "You suspect the key is not under any of these either."]),
    C("The Pots", [(21, 28), (22, 28)], "Pot", [
        "Pots by the door. You check under one, just in case. There is "
        "a note: STILL NO."],
      trope="key_under_pot"),
    C("Window", (7, 28), "Window A", [
        "Through the window: a family in their front room, braced, the "
        "way a family is that has been saved four times this year."]),
    C("Barrel", (8, 29), "Barrel", [
        "A rain barrel with a lid weighted down by a very large stone, "
        "and a card: THE BARREL HAS ALSO BEEN SAVED. PLEASE STOP."]),
]

# ---------------------------------------------- Map 34, Chapel of Continuance --
CONTINUANCE = [
    C("Window", (5, 3), "Stained Glass Window", [
        "Stained glass: a saint with a candle at the door of a "
        "mountain, looking back over her shoulder, the way people do "
        "when they have done this before."]),
    C("Window", (9, 3), "Stained Glass Window", [
        "Stained glass: a monk at a lectern with a cup of tea, and a "
        "very expressive silence. The glazier has managed to get the "
        "silence in. You can see it."]),
    C("Old Volumes", (4, 7), "Closed Books C", [
        "The old volumes of the Record, stacked, every one of them "
        "full. The spine of each says CONTINUED."]),
    C("Tea", (8, 7), "Cup (Lower Left)", [
        "A cup of tea on the lectern, put out for somebody at ten past "
        "four.",
        "It is still warm. It is always still warm."]),
    C("Plant", (3, 13), "Potted Plant A", [
        "A plant in the porch. It has been knocked over and stood back "
        "up so many times that it has grown a little to one side, to be "
        "ready."]),
]

# --------------------------------------------------------- Map 35, Fairholme --
FAIRHOLME = [
    C("Window", (3, 3), "Large Window A", [
        "A tall window. From here you can see the whole of Fairholme, "
        "and every one of its eleven new fences."]),
    C("Tapestry", (6, 3), "Tapestry A", [
        "A tapestry: a hero carrying a princess down a tower.",
        "A smaller figure behind them is carrying a cake tin. The "
        "embroiderer has given the small figure the most care."]),
    C("Portrait", (10, 3), "Portrait B", [
        "A portrait of King Aldous holding the kingdom, on a map, in "
        "both hands.",
        "The map has been cut into eleven pieces since. Nobody has told "
        "the portrait."]),
    C("Portrait", (12, 3), "Portrait A", [
        "A portrait of Princess Rosamund, aged six, in a ball gown, "
        "holding a small packed bag. Already."]),
    C("Tapestry", (16, 3), "Tapestry A", [
        "A tapestry of the kingdom, sewn in eleven colours of thread, "
        "one for each share. It is mostly drainage."]),
    C("Deed", (4, 8), "Scrolls A", [
        "A deed: TO THE BEARER, ONE TWO-THOUSAND-AND-FORTY-EIGHTH PART "
        "OF THE KINGDOM OF FAIRHOLME.",
        "There is a map. The part is mostly a ditch."]),
    C("Council Teapot", (14, 8), "Teapot A", [
        "The council's teapot. It is quite small, which is why there are two of"
        " them, and why the meetings take all day."]),
    C("Teapot", (8, 9), "Teapot A", [
        "The second teapot, for item six, which is always drainage, and "
        "always takes the afternoon."]),
    C("Notices", (19, 9), "Scrolls A", [
        "Reward notices, every one for the same princess: HER HAND, OR "
        "HALF THE KINGDOM.",
        "On every one, somebody has drawn a neat circle round HALF."],
      trope="half_the_kingdom"),
    C("Potted Plant", (2, 13), "Potted Plant A", [
        "A potted plant with a little flag in it: SHARE TWELVE. It is "
        "Mr Pilbeam's, pending a decision on the eagle."]),
]

# ------------------------------------------------- Map 36, Rosamund's Tower --
ROSAMUND = [
    C("Wardrobe", (9, 4), "Closet", [
        "Rosamund's wardrobe, ajar. You open it a little further, in "
        "the spirit of adventure.",
        "Eleven sensible travelling cloaks, each with a label: 1ST, 2ND, "
        "3RD... and one at the end marked EAGLE.",
        ("Rosamund", "Do take something, if you like. Everybody who comes "
                     "up here takes something. Usually it's me.")],
      again=["Eleven cloaks, and EAGLE. You leave them be. The Princess "
             "is watching you over her book, kindly."],
      trope="rummage"),
    C("Bed", (3, 5), "Bed", [
        "A bed, very neatly made, with a rope ladder rolled up under the "
        "pillow.",
        "Rosamund has never used it. She thinks it would be unfair on "
        "the rescuers."]),
    C("Dresser", (5, 4), "Dresser", [
        "A dresser with a tiara on it and a card: FOR BALLS.",
        "Beside it, a second tiara, a good deal sturdier: FOR "
        "KIDNAPPINGS."]),
    C("Memoir", (7, 4), "Closed Book A (H)", [
        "A book: RESCUED AGAIN - A MEMOIR, VOLUME ELEVEN.",
        "Every chapter is named after a rescuer, and every one of them "
        "is written about very kindly."],
      trope="damsel"),
    C("Potted Plant", (3, 8), "Potted Plant A", [
        "A potted plant by the window, with a little label: PLEASE WATER "
        "IF I AM AWAY. I AM OFTEN AWAY. - R."]),
]

# --------------------------------------------- Map 37, Mrs Emberthwaite's --
LAIR_BOOKS = [
    ["CARD GAMES FOR TWO. Somebody has crossed out TWO and written AND "
     "ON THURSDAYS, THREE."],
    ["HOARDING: A SENSIBLE APPROACH. Chapter one: dust it."],
    ["LETTERS FROM KNIGHTS, bound in one volume. Every letter begins "
     "FOUL BEAST and ends YOURS FAITHFULLY."],
]

LAIR = [
    C("The Hoard", [(4, 4), (5, 4)], "Large Gold Mound", [
        "A dragon's hoard: a great heap of gold, dusted every morning, very "
        "gently, with a feather.",
        "You could take a coin. Mrs Emberthwaite looks at you over her "
        "spectacles. You could not."],
      trope="dragon_hoard"),
    C("Coins", (7, 4), "Mound of Gold Coins", [
        "Coins, swept into a heap for the card games. "
        "Thursday stakes are a copper a hand, and Rosamund is "
        "ruthless."]),
    C("Coins", (3, 5), "Mound of Gold Coins", [
        "A smaller heap of coins with a little flag stuck in the top: "
        "RAINY DAY."]),
    C("Tapestry", (9, 3), "Tapestry A", [
        "A tapestry of two dragons asleep in the sun on a hillside. It "
        "has been hung where the light catches it in the afternoon."]),
    C("China", (14, 4), "Dish Cabinet", [
        "The best china. Every cup has a small scorch mark on the rim, "
        "from being drunk out of by a dragon with a cold."]),
    C("Cuckoo Clock", (15, 3), "Clock", [
        "A cuckoo clock. The cuckoo is a very small dragon. It comes out "
        "on the hour, and sneezes."]),
    C("Books", (16, 4), "Bookshelf A", LAIR_BOOKS[0], then=LAIR_BOOKS[1:]),
    C("Card Table", (12, 7), "Table", [
        "The card table, with a game laid out: hands dealt, a pot of "
        "matchsticks, and a score pad.",
        "On the score pad, Rosamund is winning by a mile."]),
    C("Umbrella Pot", (17, 10), "Pot A", [
        "A pot of umbrellas, for the knights who come up the hill in the "
        "rain meaning to slay her, so that they at least go home "
        "dry."]),
    C("Pot", (4, 11), "Pot A", [
        "A pot of dried flowers, every one picked by a different "
        "princess, every one labelled with a date and a very polite "
        "thank-you."]),
]

# ---------------------------------------------------- Map 38, Olde Evermore --
EVERMORE = [
    C("Elven Window", (7, 12), "Window A", [
        "Through an elven window: a room in which everything has been "
        "carved, beautifully, including, as far as you can tell, the "
        "soap."]),
    C("Mushrooms", (9, 12), "Mushrooms B", [
        "Mushrooms growing in a perfect spiral, which in Olde Evermore "
        "counts as untidy. Somebody has already been told."]),
    C("Mushrooms", (3, 13), "Mushrooms B", [
        "Mushrooms, each one with a tiny name tag in the Old Tongue. They "
        "have been here since the First Age, and they are on first-name "
        "terms with everybody."]),
    C("Elven Glass", (17, 13), "Stained Glass Window B", [
        "Stained glass: an elf falling off a ledge, gracefully.",
        "Below, a second elf holds up a small card that says 6.0. Nobody "
        "has ever been given a 6.0. It is a very old window, and a very "
        "hopeful one."]),
    C("Lily Pads", (23, 16), "Lotus Pads C", [
        "Lily pads. Under them, if you wait - and Calder has waited a "
        "very long time - there is the one fish.",
        "It is not there. Then it is. Then it is not."]),
    C("Window", (7, 20), "Window A", [
        "Through the window: a tidy elven room, with a ladder-shaped "
        "space by the wall where a ladder usually stands."]),
]

# ----------------------------------------------- Map 39, the Forbidden Archive --
FORBIDDEN = [
    ["A book stamped FORBIDDEN in four languages. You open it. It is a "
     "book of very good biscuit recipes.",
     "The Elders forbade it after what happened the last time."],
    ["THE CHRONICLE OF THE SECOND AGE, Volume One of Nine Hundred.",
     "Small handwriting in every margin: BORING. BORING. TRUE. BORING."],
    ["A picture book of a horse. Every page is the same horse. On the "
     "cover, in the Old Tongue: THE VILLAIN."],
    ["A shelf labelled THINGS GRANDMOTHER FORESAW. The first volume is "
     "THE FALL OF EMPIRES. The last is WHERE SHE LEFT HER SLIPPER."],
    ["PROPHECIES (DISCARDED). The top one reads: AND THE ONE WHO WAS NOT "
     "CHOSEN SHALL - and then there is a jam stain."],
    ["Elven poetry, in sixty volumes. The bookmark in volume one has not "
     "moved since the First Age."],
]

ARCHIVE = [
    C("Forbidden Shelf", [(3, 4), (4, 4)], "Bookshelf B",
      FORBIDDEN[0], then=FORBIDDEN[1:3], trope="forbidden_book"),
    C("Prophecy Shelf", (6, 4), "Bookshelf A", FORBIDDEN[4]),
    C("Foreseen Shelf", [(7, 4), (8, 4)], "Bookshelf B", FORBIDDEN[3]),
    C("Poetry Shelf", [(14, 4), (15, 4)], "Bookshelf B", FORBIDDEN[5]),
    C("Archive Glass", (10, 3), "Stained Glass Window", [
        "Stained glass: a very small figure on a stepstool, prophesying, "
        "and a crowd of tall elves leaning down to listen. One of them "
        "is holding a biscuit."]),
    C("Crystal Ball", (13, 8), "Crystal Ball", [
        "A crystal ball. You look into it, and see yourself, bent over a "
        "crystal ball.",
        "Behind you, in the ball, a very small girl on a stepstool is "
        "waving."],
      trope="crystal_ball"),
    C("Overdue", (14, 8), "Closed Books C", [
        "A stack of library books, very overdue. The date stamped in "
        "them is in the Second Age.",
        "The fine is written on a separate sheet, and the sheet is "
        "rolled up, and quite long."]),
    C("The Copying", (6, 10), "Open Book A (H)", [
        "The book being copied. The copyist has got as far as the first "
        "word.",
        "It is a very beautiful first word."]),
    C("Potted Plant", (11, 11), "Potted Plant A", [
        "A potted plant, ancient and very small, labelled in Mirabel's "
        "hand: MINE. DO NOT WATER. I DO IT."]),
]

# ------------------------------------------------------- Map 40, Gladhollow --
GLADHOLLOW = [
    C("Window", (14, 8), "Window A", [
        "Through the window: a kitchen table, and on it a list in "
        "large, careful letters headed FIFTEEN WAYS.",
        "There are fourteen of them, and a question mark."]),
    C("Window", (18, 8), "Window A", [
        "Through the window: an old man asleep in a chair with a "
        "newspaper over his face. The headline says HERO PASSES THROUGH. "
        "It has been the headline for some time."]),
    C("End House Window", (27, 8), "Window A", [
        "Through the window of the end house: every cupboard is open, "
        "and every one has a card in it saying NOTHING HERE.",
        "They have planned for you."],
      trope="rummage"),
    C("Log", (22, 15), "Fallen Log", [
        "A log by the road, with WELCOME carved into one end and "
        "FAREWELL into the other, by two boys with one penknife."]),
]

# -------------------------------------------------- Map 41, the Mayor's House --
MAYORS = [
    C("Council Minutes", (3, 4), "Bookshelf A", [
        "Council minutes: THE WELCOMER IS TO SAY 'WELCOME TO GLADHOLLOW' "
        "AND NOTHING ELSE. Carried, nine to nil.",
        "One abstention, in pencil: T. WENDLE (AGED SEVEN)."]),
    C("The Mayor's Books", [(11, 4), (12, 4)], "Bookshelf B", [
        "The Mayor's own books: CIVIC DUTY. CIVIC PRIDE. CIVIC HATS: A "
        "HISTORY, in three volumes."]),
    C("Town Shield", (27, 4), "Shield", [
        "A shield on the wall with the town's arms: two crossed swords.",
        "Under the swords, in tiny letters: (WELCOME)."]),
    C("Potted Plant", (12, 8), "Potted Plant A", [
        "A potted plant with a ribbon round the pot: BEST KEPT PLANT, "
        "GLADHOLLOW. It is the only entrant. It has won eleven years "
        "running, and is very modest about it."]),
]

# ------------------------------------------------- Map 42, the Former Premises --
PREMISES = [
    C("Window", (7, 3), "Window (Demon Castle)", [
        "A tall window. Through it: sky, and under the sky, more sky, "
        "and a very long way down, the sea."]),
    C("Window", (13, 3), "Window (Demon Castle)", [
        "Through the window a cloud drifts by at eye level, and is "
        "politely ignored."]),
    C("Armour", (3, 6), "Armor A (Stand)", [
        "A suit of armour, dusted this morning. A label: DISPLAY "
        "ONLY - NO LONGER IN SERVICE."]),
    C("Armour", (17, 6), "Armor A (Stand)", [
        "Armour, with a little tag on one finger: KEPT FOR THE LOOK "
        "OF THE THING. - H."]),
    C("Armour", (3, 8), "Armor A (Stand)", [
        "Armour, with a feather duster tucked under one arm, as if "
        "it has been helping."]),
    C("Armour", (17, 8), "Armor A (Stand)", [
        "The last suit of armour stands slightly apart from the others, "
        "facing the door, in case anybody ever comes. It has been "
        "polished more than the rest."]),
    C("Potted Plant", (3, 11), "Potted Plant A", [
        "A potted plant on a castle on a cloud. It is watered by the "
        "rain, from underneath, and is the best-watered plant in the "
        "world."]),
]

# ------------------------------------------ Map 43, Tobias Frayne's Cottage --
FRAYNE = [
    C("Window", (7, 3), "Large Window A", [
        "Through the window: the road, and a bird table piled with "
        "crumbs, and a very small sign on the bird table, at bird "
        "height: ONE EACH."]),
    C("Honey", (4, 4), "Sundries Shelf A", [
        "Jars of honey, labelled by the year, and one labelled FOR "
        "VISITORS.",
        "It is full. It is always full. Tobias Frayne is always ready "
        "for visitors."]),
    C("Breadboard", (11, 4), "Kitchen Counter A", [
        "A loaf and a breadboard, worn into a dip in the middle by a "
        "great many very thin slices."]),
    C("Bed", (12, 5), "Cheap Bed A", [
        "A narrow bed with a patchwork quilt. Every patch is a "
        "different shirt, and every one of them was worn out "
        "properly."]),
    C("Teapot", (8, 6), "Teapot A", [
        "A teapot with two cups set out beside it, and a third, just in "
        "case."]),
    C("Firewood", (4, 8), "Crate A", [
        "A crate of firewood, split very small and stacked very neatly, "
        "by a man with time on his hands and a good axe."],
      trope="containers"),
]

# --------------------------------------------------------- Map 44, Frostwick --
FROSTWICK = [
    C("Street Lamp", (8, 12), "Streetlight B (Snow)", [
        "A street lamp with a little hat of snow on top. The snow is "
        "exactly the contracted four inches. Somebody has measured "
        "it."]),
    C("Street Lamp", (26, 12), "Streetlight B (Snow)", [
        "A street lamp, tied with a festival ribbon. It is lit at four "
        "sharp, for the lanterns, by a boy of seven with a very long "
        "pole."]),
    C("Staggs' Window", (4, 11), "Window A", [
        "Through the window: two armchairs pulled up very close to the "
        "fire, and two pairs of slippers warming on the fender, toes "
        "touching."]),
    C("Inn Sign", (11, 11), "Shop Sign (Inn)", [
        "THE ELEVEN DAYS. ROOMS.",
        "A card underneath: NAMED FOR THE THAW. ASK MRS MARCHPANE. SHE "
        "WILL TELL YOU ANYWAY."]),
    C("Tavern Sign", (15, 11), "Shop Sign (Pub)", [
        "A tankard sign with an icicle hanging off it. The icicle has "
        "been there so long it has a name. It is called Reginald."]),
    C("Window", (21, 11), "Window A", [
        "Through the window: a front room hung with paper snowflakes. "
        "Every one of them is a slightly different shape, and every one "
        "has been checked against the contract."]),
    C("Barrel", (33, 11), "Barrel (Snow)", [
        "A barrel labelled SPARE SNOW (CONTRACT). It is full. You "
        "suspect it is not, strictly, allowed."]),
    C("Barrel", (2, 12), "Barrel (Snow)", [
        "A barrel of grit for the paths, with a sign: NOT TO BE USED "
        "DURING THE FESTIVAL. THE SNOW HAS BEEN PAID FOR."]),
    C("Crate", (2, 16), "Crate (Snow)", [
        "A crate of paper lanterns, for four o'clock, packed in straw so "
        "they will not crease, and in snow so they will feel at home."]),
    C("Crate", (33, 17), "Crate (Snow)", [
        "A crate of carol sheets. Every one has a verse crossed out by "
        "the Working Group, on the grounds that it promised snow on the "
        "twelfth without consulting them."]),
    C("Barrel", (12, 16), "Barrel (Snow)", [
        "A barrel of carrots for snowmen. Each carrot has been chosen, "
        "and is very much the right carrot."]),
]

# ---------------------------------------------------- Map 45, the Eleven Days --
ELEVEN_DAYS = [
    C("Shelf", (3, 4), "Sundries Shelf A", [
        "Jars of preserves, with a little calendar pinned on the end of "
        "the shelf. Eleven days on it have been circled, a long time "
        "ago, in red."]),
    C("Shelf", (4, 4), "Sundries Shelf B", [
        "Hot-water bottles, a great many of them, each in a knitted "
        "cover, and each knitted cover with the name of a room on "
        "it."]),
    C("Wine Rack", (6, 4), "Wine Rack", [
        "A wine rack holding mulled wine for the festival, and a card: "
        "WARM BEFORE SERVING. THE WINTER WILL NOT DO IT FOR YOU."]),
    C("The Bell", (4, 6), "Bell", [
        "A bell on the bar. A little card: RING FOR SERVICE, OR FOR THE "
        "STORY OF THE THAW. They are, in practice, the same thing."]),
    C("Hot Drink", (7, 6), "Bottle B", [
        "A bottle of something hot, wrapped in a tea towel to keep it "
        "that way, and labelled FOR THE RIBBON - MR STAGG."]),
    C("Window", (12, 3), "Large Window A", [
        "A frosted window. Somebody has drawn a face in the frost from "
        "the inside, and somebody else has drawn a scarf on it."]),
    C("Bedside Table", (18, 4), "Table F", [
        "A bedside table with flowers, a hot-water bottle, and a card: "
        "IF COLD, RING. IF STILL COLD, RING AGAIN. IF STILL COLD, IT IS "
        "IN THE CONTRACT."]),
    C("Breakfast", (5, 8), "Dinner Set C (Left)", [
        "Breakfast: a chop, and porridge with a little face drawn on it in "
        "golden syrup, as Mrs Marchpane does for every guest regardless of age."]),
    C("Crate", (3, 11), "Crate A", [
        "A crate of logs, cut for the fire, labelled THE TWELFTH. It is "
        "being saved for the festival."]),
]

# ---------------------------------------------------- Map 46, the Working Group --
WORKING_GROUP = [
    C("Window", (9, 3), "Large Window A", [
        "A window, and through it, snow falling at exactly the "
        "contracted rate. A member of the committee is timing it."]),
    C("Scrolls", (3, 4), "Scrolls A", [
        "Scrolls of minutes, tied up in festival ribbon. ITEM: THE "
        "WINTER. ITEM: THE WINTER (CONT.). ITEM: THE WINTER (CONT., "
        "CONT.)."]),
    C("Map", (4, 4), "Map A (V)", [
        "A map of Frostwick with every snowdrift drawn in, numbered, and "
        "cross-referenced to a schedule."]),
    C("Scrolls", (5, 4), "Scrolls B", [
        "The festival programme in draft, in eleven drafts. Every draft "
        "has the Ribbon at noon. Nobody has ever suggested changing "
        "it."]),
    C("Agenda", (6, 6), "Closed Book A (V)", [
        "The agenda. Item one is APOLOGIES. There are none. Nobody in "
        "Frostwick has ever missed a meeting of the Working Group."]),
    C("Ink", (9, 6), "Bottle B", [
        "A bottle of ink, nearly empty. The Working Group gets through a "
        "great deal of ink, most of it on the word 'winter'."]),
    C("Crates", [(12, 9), (13, 9)], ("Crate B", "Crate A"), [
        "Crates of bunting, sorted by colour, and one crate labelled "
        "BUNTING (CONTESTED)."]),
]

# ------------------------------------------------------- Map 47, the Cold Room --
COLD_ROOM = [
    C("Window", (4, 3), "Large Window A", [
        "A window, frosted on the inside. In this room the frost is "
        "always on the inside."]),
    C("Files", (11, 4), "Bookshelf A", [
        "Box files: CONTRACT. CONTRACT (AMENDMENTS). CONTRACT (AMENDMENTS "
        "TO THE AMENDMENTS). A slim one: COMPLIMENTS."]),
    C("Handbook", (6, 6), "Closed Book A (V)", [
        "A handbook, MAINTAINING A WINTER: GOOD PRACTICE. It is bound "
        "in purple, and very cold to the touch."]),
    C("Crates", [(3, 8), (4, 8)], ("Crate A", "Crate B"), [
        "Crates stencilled ICICLES, ASSORTED, packed in straw, for "
        "dressing the eaves on the twelfth."]),
    C("Basin", (11, 8), "Basin", [
        "A basin of water with a skin of ice on it. Somebody washes "
        "here every morning, gloves on."]),
]

# ------------------------------------------------- Map 48, the Chapter House --
CHAPTER_HOUSE = [
    C("Window", (15, 3), "Stained Glass Window", [
        "Stained glass: a knight kneeling, and above him a scroll with "
        "the Order's motto, which is too small to read from here, and "
        "was, you suspect, too long to fit."]),
    C("Armour", (3, 4), "Armor A (Stand)", [
        "A suit of armour on a stand, very bright, very polished, with a "
        "card: CEREMONIAL. DO NOT GO ON A QUEST IN."]),
    C("Armour", (3, 8), "Armor A (Stand)", [
        "Another suit, with a label: ISSUE PATTERN, KNIGHTS ERRANT, ONE. "
        "Underneath, in pencil: SIZES RUN SMALL."]),
    C("Register", (14, 6), "Open Book A (V)", [
        "The Order's daybook, open. Today: PINS REVIEWED. Yesterday: "
        "PINS REVIEWED. The day before: PINS REVIEWED (WITH TEA)."]),
]

ALL = {28: MEADOW, 29: PENULTIMA, 30: SHOPPE, 31: RESTWELL,
       32: EIGHT_HOURS, 33: HITHERMOST, 34: CONTINUANCE, 35: FAIRHOLME,
       36: ROSAMUND, 37: LAIR, 38: EVERMORE, 39: ARCHIVE, 40: GLADHOLLOW,
       41: MAYORS, 42: PREMISES, 43: FRAYNE, 44: FROSTWICK,
       45: ELEVEN_DAYS, 46: WORKING_GROUP, 47: COLD_ROOM,
       48: CHAPTER_HOUSE}
