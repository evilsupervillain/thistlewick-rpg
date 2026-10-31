"""CURIOS.md wave C3: the Obligatory Tower (Map 11) and the north (Maps
21-27).

The Tower is Grimspite's place of work, and has been for 4,800 years: it
has barracks, a canteen, a laundry label on every banner, cells nobody has
ever been put in, and a private library that tells the player a good deal
about the man upstairs before they meet him - never the twist itself
(POSTGAME.md: the contract, the bungalow and the tea are the ending's to
say; these only point at them)."""

import db
from curios import curio as C

# ----------------------------------------------------- Map 11, the Tower --
DARK_LIBRARY = [
    ["VILLAINY FOR BEGINNERS. It has been read once, carefully, a very "
     "long time ago, and then put back with a bookmark in chapter one."],
    ["THE MONOLOGUE: A HANDBOOK. Chapter one is called 'Don't'.",
     "There are no other chapters."],
    ["THE PROPHECY OF THISTLEWICK, ANNOTATED. Every margin is full. "
     "Clause twelve has been underlined so often there is a hole in the "
     "page."],
    ["A THOUSAND AND ONE THINGS TO DO WITH A TOWER. Somebody has "
     "ticked them all, and written a thousand and two on the back: "
     "LEAVE IT."],
    ["READING A RENEWAL CLAUSE, by a firm of lawyers in Great Dunnage. "
     "It is the most worn book on the shelf. It falls open at "
     "'notice'."],
    ["BUNGALOWS OF THE COAST, with photographs. One page has been "
     "turned down at the corner. It is a small white one with a view of "
     "the sea."],
    ["TEA: A HISTORY. Volumes one to nine."],
    ["KNITTING FOR THE DARK HOURS. There is a scarf pattern in the back, "
     "with a note in the margin: AUNT M - TOO LONG?"],
]

TOWER = [
    # --- the first floor
    C("Window", (7, 5), "Window (Demon Castle)", [
        "A tall arched window. The view is of more tower.",
        "Whoever built this place had a very clear idea of what a Dark "
        "Lord ought to be looking at."]),
    C("Window", (13, 5), "Window (Demon Castle)", [
        "Somebody has drawn a smiley face in the dust on the glass, from "
        "the inside, a very long time ago. It has been carefully not "
        "cleaned off."]),
    C("Spider's Web", (6, 6), "Spider Web", [
        "A spider's web, beautifully made, with a tiny card hung in the "
        "middle of it: WORK IN PROGRESS."],
      trope="cobweb"),
    C("The Night Porter's Bed", (15, 7), "Straw Bed", [
        "A straw bed with a card: NIGHT PORTER (OFF DUTY). There is a "
        "cup of cocoa beside it, quite cold, with a biscuit on the "
        "saucer."]),
    C("Card Table", [(10, 8), (11, 8)], "Table (Ruins)", [
        "A table, set for cards. Four hands dealt and never played.",
        "One of them, you can't help seeing, is a very good hand indeed. "
        "It is in front of the empty chair nearest the stairs."]),
    C("Skeleton", (6, 10), "Bones A", [
        "A skeleton slumped against the wall. Somebody has put a cushion "
        "behind it."],
      then=[["And a blanket over its knees. It is a draughty tower."]]),
    C("Pot", (14, 10), "Pot A", [
        "A pot. You look in. There is nothing in it but a note:",
        "I WOULDN'T EITHER. - G."],
      trope="pots"),
    C("Barrel", (8, 17), "Barrel A", [
        "A barrel stencilled DUNGEON SUPPLIES - GLOOM.",
        "It is empty. The gloom has got out, and is everywhere."],
      trope="containers"),
    C("Store Pot", (9, 17), "Pot B", [
        "A big lidded jar, labelled TORCHES, FLICKERING, FOR THE USE OF. "
        "There is one left. It is flickering already."]),
    C("Rocks", (3, 19), "Crate B (Stone)", [
        "A crate of rocks, labelled ROCKS (SPARE), for when a corridor "
        "has started to look too tidy."]),
    C("Broken Crate", (5, 22), "Crate C (Ruins)", [
        "A broken crate with a sign in it: DUNGEON - THIS WAY.",
        "The arrow points into the crate."]),
    C("Dragon Bones", [(32, 20), (33, 20)], "Large Bones", [
        "The skeleton of a dragon, curled round on itself like a dog "
        "asleep by a fire.",
        "Somebody has hung a little sign on the tail: PLEASE DO NOT "
        "TOUCH. It is not clear whether the sign is meant for you or for "
        "the dragon."]),
    C("Banner", (17, 16), "Tapestry A", [
        "A red banner with the Dark Lord's arms: a tower, rampant, on a "
        "field of slightly more tower."]),
    C("Banner", (24, 16), "Tapestry A", [
        "A banner. On the back, a laundry label: HAND WASH ONLY. DO NOT "
        "TUMBLE. DO NOT LET THE CHOSEN ONE SET FIRE TO IT (AGAIN)."],
      party=[(db.ZEPH, [("Zephyrine", "That wasn't me. That was one of "
                         "the others. Probably.")])]),
    C("Banner", (36, 7), "Tapestry A", [
        "A banner, slightly faded, with a darned patch in the corner, "
        "done very neatly in black thread by somebody who has had a "
        "great deal of practice."]),
    C("Mirror", (21, 4), "Mirror (Ruins)", [
        "A cracked mirror in a very fancy frame. Your reflection is in "
        "seven pieces.",
        "All seven of them look worried."]),
    C("Web", (37, 17), "Spider Web", [
        "A cobweb with a note pinned to the wall beside it: THIS COBWEB "
        "IS LISTED. DO NOT DUST. - G."]),

    # --- the second floor: armoury, cells, barracks, canteen
    C("Axes", (55, 4), "Axes", [
        "Axes on the wall, each with a little brown luggage label: "
        "PROPERTY OF THE TOWER. RETURN AFTER USE."]),
    C("Weapon Rack", (53, 5), "Sword Rack A", [
        "A rack of swords, very sharp, and labelled in order of menace. "
        "The last one is labelled FOR CUTTING CAKE."],
      trope="weapon_wall"),
    C("Spears", (55, 5), "Spears A", [
        "Spears, arranged in a fan. One is a mop, painted black, put in "
        "to make the numbers up."]),
    C("Shield", (57, 5), "Shield A", [
        "A great red shield with a fierce gold device on it. Under the device, "
        "very small, somebody has painted: HAVE A NICE DAY."]),
    C("Black Armour", (52, 7), "Armor A (Stand)", [
        "A suit of armour in gold and purple, covered in spikes, very terrible.",
        "There is a little wooden step in front of it, because whoever "
        "wears it is quite short."]),
    C("Black Armour", (52, 10), "Armor A (Stand)", [
        "More armour. A note is tucked into the gauntlet: GONE "
        "FOR TEA. BACK IN TEN. If it ever comes back, it has been ten "
        "minutes for a very long time."]),
    C("Cell", (60, 8), "Jail Bars", [
        "A cell, with a sign on the bars: FOR CHOSEN ONES WHO HAVE BEEN "
        "CAPTURED.",
        "It has never been used. In 4,800 years nobody has ever been "
        "captured. It seemed rude."],
      trope="captured"),
    C("Cell", (64, 8), "Jail Bars", [
        "Another cell. On the wall inside, a calendar, with every day "
        "crossed off very neatly for a great many years. Nobody was "
        "ever in it. It is just somebody's calendar."]),
    C("Cell", (68, 8), "Jail Bars", [
        "A cell with a straw mattress, a bucket, and a little vase of "
        "dried flowers on a shelf, in case.",
        "In case of what, the cell does not say."]),
    C("Mirror", (76, 3), "Mirror (Ruins)", [
        "A cracked mirror in the barracks, with a note tucked into the "
        "frame: PRACTISE LOOKING MENACING.",
        "Underneath, in a different hand: I AM TRYING."]),
    C("Bunk", (75, 5), "Cheap Bed", [
        "A minion's bunk, made with tight corners. A card on the pillow: "
        "SKELETON, THIRD CLASS."]),
    C("Bunk", (77, 5), "Cheap Bed", [
        "A bunk. Under the pillow, a small teddy bear wearing a helmet "
        "with horns."]),
    C("Bunk", (75, 8), "Cheap Bed", [
        "A bunk with a sign over it: DAY SHIFT. The day shift is asleep. "
        "It always is. That is what day shift means, in a dark tower."]),
    C("Lockers", [(83, 6), (84, 6)], ("Closet", "Chest of Drawers"), [
        "The minions' lockers. Names are scratched into the doors: GRUB. "
        "SNAG. GRUB (THE OTHER ONE).",
        "You open GRUB's. A packed lunch, a spare helmet, and a card: IF "
        "YOU ARE THE CHOSEN ONE, THE KEY IS NOT IN HERE. IT IS NEVER IN "
        "THE LOCKERS."],
      then=[["You open SNAG's. Clean socks, folded, and a letter from home "
             "that begins: DEAR SNAG, ARE YOU EATING."],
            ["GRUB (THE OTHER ONE)'s is locked. A card is tucked into the "
             "door: NICE TRY."]],
      again=["GRUB. SNAG. GRUB (THE OTHER ONE). NICE TRY."],
      trope="rummage"),
    C("Bunks", (76, 14), "Cheap Bed", [
        "A row of bunks. On the end of each a clipboard: SICK LEAVE. "
        "SICK LEAVE. ANNUAL LEAVE. SICK LEAVE.",
        "The Tower has very good terms and conditions."]),
    C("Canteen", [(64, 17), (65, 17)], "Table", [
        "The staff canteen. A menu is pinned to the end of the table: "
        "MONDAY - GRUEL. TUESDAY - GRUEL.",
        "WEDNESDAY - CHEF'S SPECIAL (GRUEL)."]),
    C("Brown Sauce", (66, 17), "Bottle B", [
        "A bottle of brown sauce, the canteen's one luxury, and a card: "
        "ONE SQUEEZE EACH. THAT MEANS YOU, SNAG."]),
    C("Canteen", (64, 21), "Table", [
        "A canteen table, wiped. A sign: PLEASE CLEAR YOUR OWN BONES."]),
    C("Clock", (60, 23), "Clock (Ruins)", [
        "A broken clock. It has stopped at twenty past three.",
        "A label under it, in a careful hand: SOMETIMES IT IS TWENTY "
        "PAST THREE. THEN IT IS RIGHT, AND I FEEL BETTER. - G."]),

    # --- the third floor: galleries, statues, the coffins
    C("Statue", (102, 6), "Statue B", [
        "A statue of a knight in a heroic pose. The plaque says HEROIC "
        "POSE NO. 3.",
        "Round the side of the plinth there is a little chart showing "
        "heroic poses one to twelve. Number seven is mostly pointing."]),
    C("Window", (107, 4), "Window (Demon Castle)", [
        "An arched window. Far below, very small, the road you came up, "
        "and a long way beyond it, very small indeed, the sea."]),
    C("Gargoyle", [(105, 14), (106, 14)], "Dragon Statue", [
        "A gargoyle, wings out, snarling. Somebody has hung a little "
        "bell round its neck so that it can't creep up on anybody."]),
    C("Grandfather Clock", (109, 13), "Clock", [
        "A clock that ticks in a very sinister way. You listen more "
        "closely.",
        "It ticks in a perfectly ordinary way. You were imagining it."],
      then=[["You listen again. It is definitely ordinary. Probably."]]),
    C("Wardrobe", [(100, 14), (101, 14)], ("Closet", "Chest of Drawers"), [
        "A wardrobe of black cloaks on numbered hangers. One of them is "
        "very slightly less black than the others, from being washed "
        "with something red."]),
    C("Coffin", (113, 24), "Coffin B (Top)", [
        "A coffin, standing up, with a little brass plate: RESERVED.",
        "Every coffin in this row says RESERVED. The management was told "
        "that a tower ought to have coffins, for the look of it."],
      trope="coffin"),
    C("Coffin", (116, 24), "Coffin B (Top)", [
        "A coffin. The lid is open a crack, and somebody has put a "
        "fern inside, where it is doing beautifully in the dark."]),
    C("Coffin", (119, 24), "Coffin B (Top)", [
        "A coffin with a card on it: DRY STORE. You look. It is full of "
        "spare candles, sorted by length."]),
    C("Coffin", (122, 24), "Coffin B (Top)", [
        "A coffin that smells strongly of lavender. Somebody has been "
        "putting little bags of it in, for freshness."]),
    C("Coffin", (125, 24), "Coffin B (Top)", [
        "The last coffin has a card on it: OUT OF ORDER."]),
    C("Banner", (113, 11), "Tapestry A", [
        "A banner with a stitched motto: ABANDON HOPE.",
        "Underneath, in smaller, newer stitching: (BUT DO WIPE YOUR "
        "FEET)."]),
    C("Armour", (133, 18), "Armor A (Stand)", [
        "A suit of armour with its visor up. Inside, where a face would "
        "be, there is a little hand-lettered card: NOBODY HOME."]),

    # --- the fourth floor: the library and the writing on the wall
    C("The Mural", [(165, 3), (166, 3), (167, 3), (168, 3)], "Large Mural A",
      ["A great mural in an old script that you cannot read. A card "
       "has been pinned beside it, with a translation:",
       "STAFF NOTICES. PLEASE WASH YOUR CUP."]),
    C("The Writing", [(156, 8), (157, 8)], "Hieroglyph", [
        "More of the old script, cut deep. The translation card beside it "
        "says: THE PREVIOUS MANAGEMENT REGRETS ANY INCONVENIENCE."]),
    C("Library", [(176, 6), (177, 6)], "Bookshelf A",
      DARK_LIBRARY[0], then=DARK_LIBRARY[1:4], trope="bookshelf"),
    C("Library", [(180, 6), (181, 6)], "Bookshelf A",
      DARK_LIBRARY[4], then=DARK_LIBRARY[5:]),
    C("Wine Rack", (178, 6), "Wine Rack", [
        "A wine rack, full. Every bottle in it is cold tea, corked and labelled"
        " with the year, going back further than wine could possibly keep."]),
    C("Globe", (175, 12), "Globe", [
        "A globe, with one pin in it, on a little spot by the sea.",
        "A label on the pin: ONE DAY."]),
    C("Lectern", (175, 15), "Open Book A (V)", [
        "A book open on a stand: WHAT TO SAY WHEN THEY ARRIVE. Every page "
        "is a different speech, crossed out.",
        "The last page has one word on it, and it has not been crossed "
        "out: 'Tea?'"]),
    C("Axes", (149, 22), "Axes", [
        "Crossed axes over the door, polished, with a card: DECORATIVE. "
        "THE DOOR IS THE DANGEROUS PART."]),
]

# ------------------------------------------------ Map 21, Upper Clanging --
CLANGING = [
    C("Crate", (11, 3), "Crate", [
        "A crate stencilled HOYLE WORKS - RIVETS - HANDLE WITH CARE. "
        "Rivets do not need handling with care. Somebody at the works "
        "is fond of them."]),
    C("Barrel", (18, 3), "Barrel", [
        "A barrel of rainwater, which in Upper Clanging comes down "
        "already a pale shade of grey."],
      trope="containers"),
    C("Crate", (20, 3), "Crate", [
        "A crate addressed to THE PARISH, UPPER CLANGING, with "
        "FRAGILE - HYMN BOOKS on the side. It clanks."]),
    C("Leaking Drum", (3, 10), "Oil Drum (Leak)", [
        "An oil drum on its side, leaking very slowly into a little "
        "gutter somebody has dug for it.",
        "The gutter runs to a bucket. The bucket is full, and has a "
        "little gutter of its own, to the next bucket."]),
    C("Oil Drum", (5, 10), "Oil Drum", [
        "An oil drum with a hand-painted label: NOT FOR LAMPS. NOT FOR "
        "HAIR. NOT FOR CAKE. The list goes round the back."]),
    C("Window", (2, 8), "Window C", [
        "A window with a little box of geraniums on the sill. They are "
        "grey, like everything else in Clanging, but they are trying."]),
    C("Window", (26, 9), "Window C", [
        "Through the window: a front room with every ornament on every "
        "shelf turned round to face the works, out of loyalty."]),
    C("Vent", (12, 13), "Exhaust Port Wall", [
        "A vent in the wall, breathing out warm air every few seconds.",
        "The cat from next door has arranged its whole life round it."]),
    C("Works Sign", (14, 13), "Metal Shop Sign (Blank)", [
        "A metal sign with nothing on it. The works has never needed a "
        "sign. Everybody knows where the works is: it is where the noise "
        "is."]),
    C("Warning Plate", (20, 13), "Warning Plate", [
        "An enamel plate: DANGER. HOT. LOUD. EARLY.",
        "All four are true. Upper Clanging is four minutes early for "
        "everything."]),
    C("Fuel Tank", (27, 14), "Small Fuel Tank", [
        "A tank marked COAL OIL. Somebody has chalked underneath it: NO "
        "WIZARDS WITHIN TEN YARDS."],
      party=[(db.ZEPH, [("Zephyrine", "I'm offended. I'm not wrong to "
                         "be offended. But I am.")])]),
    C("Pump", (11, 15), "Water Well Pump", [
        "A hand pump with a sign: DRINKING WATER. Under it, smaller: "
        "SORT OF."],
      trope="well"),
    C("Skip", (28, 15), "Garbage Dumpster", [
        "A skip full of scrap metal, and every piece has a little paper "
        "tag tied on it in a child's writing:",
        "NOT A WASHER. NOT A WASHER. NOT A WASHER. MAYBE."]),
    C("Skip", (30, 30), "Garbage Dumpster", [
        "A skip with the boiler of an airship in it. A plate on the "
        "boiler says No. 147.",
        "Somebody has chalked on it, very small: ALMOST."]),
    C("Leaking Drum", (32, 15), "Oil Drum (Leak)", [
        "A leaking drum with a cup under the leak, and a label on the "
        "cup: TEA (DO NOT)."]),
    C("Barrel", (24, 15), "Barrel", [
        "A barrel of washers, unsorted. A note is pinned to it: SHIM - "
        "PLEASE. JUST THIS ONCE. NOT ALL OF THEM."]),
    C("Inn Sign", (23, 26), "Metal Shop Sign (Inn)", [
        "THE SAFETY VALVE. BEDS. A smaller plate screwed on underneath: "
        "IN THE EVENT OF PRESSURE, GO TO BED."]),
    C("Cafe Sign", (27, 26), "Metal Shop Sign (Cafe)", [
        "A painted cup and saucer, steaming. It is the only steam in "
        "Upper Clanging that anybody is pleased to see."]),
    C("Forge Sign", (5, 27), "Metal Shop Sign (Weapon)", [
        "A painted sword. Under it: BRYD - SMITH. Under that, smaller, "
        "freshly painted: THE BEST IN THE NORTH.",
        "Under that, in a different paint: SAYS WHO."],
      party=[(db.HOB, [("Hob", "Says me. I did that one. Don't tell "
                        "him.")])]),
    C("Forge Sign", (9, 27), "Metal Shop Sign (Armor)", [
        "A painted breastplate, very finely done, with every rivet "
        "showing. It is an advertisement and also, quite clearly, "
        "showing off."]),
    C("Pillar Box", (12, 28), "Postal Box", [
        "A red pillar box. COLLECTIONS: 9, 12 AND 5.",
        "The slot has a little step built in front of it, worn smooth, "
        "for somebody quite small who posts a great many letters."]),
    C("Bench", (21, 29), "Bench A", [
        "A bench with a brass plate: FOR SOWERBY. SIXTY YEARS ON THE "
        "RIVETS.",
        "Sowerby sits on the other bench. He says this one is for "
        "visitors."]),
    C("Bench", (31, 39), "Bench A", [
        "A bench by the parish rooms with a little plate: IN MEMORY OF "
        "THE QUIET.",
        "Somebody has scratched under it: IT WILL BE BACK SOON."]),
    C("Parish Sign", (26, 39), "Metal Shop Sign (Item)", [
        "A painted bag on a hook. PARISH ROOMS - TEAS - JUMBLE - "
        "WEDDINGS - FUNERALS - FETE. Every one of them is on Saturday."]),
    C("Cotterill Window", (7, 39), "Window C", [
        "Through the window: washing on a line across the kitchen, nine "
        "vests in a row in order of size.",
        "There is a peg on the end with nothing on it yet. It has been "
        "put there in hope, and labelled."]),
    C("Cotterill Window", (3, 39), "Window C", [
        "Through the window: a chart on the kitchen wall headed WHOSE "
        "TURN FOR THE BATH. It goes round twice and the last name is "
        "always SPARE (TRY)."]),
    C("Barrel", (4, 40), "Barrel", [
        "A rain barrel with nine little tin cups hung round the rim on "
        "nails, each with a name scratched in. One more nail, no cup."]),
]

# ---------------------------------------------- Map 22, the Hoyle Works --
WORKS = [
    C("Notices", (10, 3), "Bulletin Board", [
        "A board of works notices: SAFETY FIRST. SAFETY SECOND. LIFT "
        "THIRD.",
        "Somebody has crossed out THIRD and written ALWAYS, and "
        "somebody else has crossed that out and written SEE OTT."]),
    C("Works Clock", (11, 3), "Wall Clock", [
        "The works clock, four minutes fast like every clock in Upper "
        "Clanging. A plate underneath: THE HOOTER IS NOT A "
        "SUGGESTION."]),
    C("Camp Bed", (11, 5), "Pipe Frame Bed", [
        "A camp bed against the wall, with the blanket folded square. "
        "Ott sleeps here when an attempt is close.",
        "The blanket has been folded so many times there is a crease in "
        "it you could cut bread with."]),
    C("Rivet Rack", (14, 4), "Steel Shelf", [
        "A steel rack of rivets in drawers, labelled by size: SMALL. "
        "SMALLER. SMALLEST. NIB'S."]),
    C("Hazard Plate", (15, 3), "Warning Plate A", [
        "A yellow plate: CAUTION - CONTENTS UNDER PRESSURE.",
        "Nib says it refers to everybody who works here."]),
    C("Plumbing", [(19, 5), (18, 5), (20, 5)], "Plumbing", [
        "A knot of pipes with a gauge in the middle of it. The needle is "
        "in the red.",
        "A label beside the gauge: IT IS ALWAYS IN THE RED. THAT IS WHERE "
        "IT LIVES. LEAVE IT."]),
    C("Locker", (6, 4), "Locker B (School)", [
        "A steel locker with a number painted on: 40. You leave it shut.",
        "Taped to the outside, in a mother's handwriting: EAT YOUR "
        "CRUSTS. YOU ARE AN ENGINEER NOW."]),
    C("Calculations", [(4, 6), (5, 6)], ("Large Desk B", "Document"), [
        "Papers covered in sums: ATTEMPT 200 - LIFT, DRAG, WEIGHT, NERVE.",
        "Every page ends with a tiny drawing of a bird, flying."]),
    C("Engine", (6, 9), "Machine C", [
        "A small steam engine on the bench, in pieces, with a card: DO "
        "NOT TOUCH. THIS IS NOT A KIT. THIS IS A PROBLEM."]),
    C("Parts Chest", (4, 12), "Chest B (Metal)", [
        "A steel chest labelled SPARE PARTS - ATTEMPTS 1 TO 199. It is "
        "extremely full, and it is extremely tidy."]),
    C("Scrap", (3, 16), "Rubble B (Metal)", [
        "A heap of scrap from the last attempt, swept into the corner "
        "very carefully, as though one of the pieces might still turn "
        "out to be the important one."],
      trope="scrap_heap"),
    C("Crates", (21, 6), "Stacked Crates", [
        "Crates of castings from the foundry down the valley, stencilled "
        "with the date. They are four minutes early."]),
]

# ------------------------------------------------ Map 23, the Safety Valve --
VALVE_BOOKS = [
    ["BOILERS, AND HOW TO TALK TO THEM. Chapter one: quietly."],
    ["A HISTORY OF THE HOYLE WORKS, in a hundred and ninety-nine short "
     "chapters. Most of them end over the Long Field."],
    ["SIXTY-THREE THINGS: A COMMENTARY. A companion to the framed list "
     "on the wall. It is much longer, and is not allowed out of the "
     "inn."],
    ["THE HOOTER: ITS HISTORY, ITS USES, ITS CRITICS."],
]

SAFETY_VALVE = [
    C("Best China", (4, 4), "Chest of Drawers A", [
        "A dresser full of the inn's best china, with a card on top: FOR WHEN "
        "SHE FLIES.",
        "It has never been used. It is dusted every week."]),
    C("Books", [(9, 4), (10, 4)], "Bookshelf A",
      VALVE_BOOKS[0], then=VALVE_BOOKS[1:]),
    C("Clock", (12, 3), "Wall Clock", [
        "A clock, four minutes fast, with a card under it: THIS CLOCK IS "
        "RIGHT. EVERYWHERE ELSE IS LATE."]),
    C("Plant", (17, 4), "Plant A", [
        "A snake plant in a pot, grey with soot and thriving. It is the "
        "only thing in Upper Clanging that actually likes the air."]),
    C("Bed", (19, 5), "Bed", [
        "A bed with a little brass plate on the foot: IN CASE OF "
        "EMERGENCY, LIE DOWN.",
        "It is the whole philosophy of the Safety Valve, on one plate."],
      trope="strangers_bed"),
    C("Teapot", (5, 6), "Teapot & Cup", [
        "Mr Kell's teapot, and folded beside it a cosy knitted like a small "
        "boiler, with a little knitted gauge on the front, in the red."]),
    C("Bread Rolls", (6, 6), "Bread", [
        "A basket of loaves. They are hard enough to "
        "rivet with, and in Upper Clanging that is a compliment."]),
    C("Sausages", (9, 7), "Meat Dish", [
        "A dish of sausages, done the Clanging way: until they hiss."]),
    C("Winnie's Glass", (14, 7), "Beer Mug", [
        "Winnie's half of shandy, on a doily. The doily is embroidered "
        "CLASS OF '19."]),
    C("Plate", (9, 10), "Plate A", [
        "An empty plate, very clean. It is Rivet Cotterill's, and he is "
        "growing."]),
    C("Water Jug", (14, 10), "Wine & Glass", [
        "A jug of water and a glass, with a place card: THE SECRETARY. "
        "It has been laid for the Class of 'Nineteen dinner."]),
    C("Lamp", (3, 8), "Lamp", [
        "A brass lamp, polished until it hurts to look at. Mr Kell "
        "polishes things when he is worried, and he has been worried "
        "for about two hundred years."]),
]

# ---------------------------------------------------- Map 24, Ollerenshaw's --
BRYDS = [
    C("Valve", (8, 3), "Valve", [
        "A valve on the pipe, painted red, with a tag: DO NOT TURN.",
        "Under it, on a second tag: I SAID DO NOT. - B.O."]),
    C("Shelf", (11, 4), "Miscellaneous Item Shelf", [
        "A shelf: a pot plant, a clock, and a framed certificate - BEST "
        "SMITH IN THE NORTH.",
        "It was awarded by B. Ollerenshaw, to B. Ollerenshaw."],
      party=[(db.HOB, [("Hob", "Hah! ...Is that real gold leaf on "
                        "that? ...It's not bad, the lettering.")])]),
    C("Quenching Tub", (5, 4), "Large Basin", [
        "A quenching tub. The water hisses faintly, every time anybody "
        "in the room says the word 'Thistlewick'."],
      party=[(db.HOB, [("Hob", "Thistlewick.")]),
             (db.MERRI, [("Merribell", "That's steam. That's just "
                          "steam. Don't encourage him.")])]),
    C("Coal", (7, 4), "Scrap Metal", [
        "A crate of coal, every lump the same size. Bryd sorts it. "
        "Nobody has ever seen him do it."]),
    C("Hammers", (7, 6), "Hammers", [
        "Bryd's hammers, hung by size, every one with a name scratched "
        "on the handle.",
        "The names are all BRYD."]),
    C("Contraption", (10, 6), "Machine C", [
        "A machine of cogs and springs. Grommet says it is for "
        "straightening nails.",
        "It has not straightened any yet, but it has bent some very "
        "interestingly."]),
    C("Steel Cabinet", (13, 7), "Chest B (Metal)", [
        "A steel cabinet with three drawers: RIVETS. OTHER RIVETS. "
        "RIVETS (GRUMNIR'S - DO NOT USE)."],
      party=[(db.HOB, [("Hob", "Do not use. Hah. Because they're "
                        "better than his. ...They are, mind.")])]),
]

# ------------------------------------------------ Map 25, the Parish Rooms --
PARISH = [
    C("Parish Board", (8, 3), "Bulletin Board", [
        "The parish rota. TEA - MRS TUNNICLIFFE. URN - MRS TUNNICLIFFE. "
        "HYMN BOARD - MRS TUNNICLIFFE.",
        "EVERYTHING ELSE - SEE ABOVE."]),
    C("Registers", (5, 4), "Bookshelf A", [
        "Parish registers, one a year for eighty years, each one fatter "
        "than the last. The fattest is labelled COTTERILL (CONT.)."]),
    C("The Clock Shelf", (6, 4), "Miscellaneous Item Shelf", [
        "A shelf with a pot plant and a carriage clock: PRESENTED TO MR "
        "TUNNICLIFFE, FORTY YEARS AT THE WORKS.",
        "Beside it, a photograph of Mr Tunnicliffe holding the clock, "
        "looking delighted, and of Mrs Tunnicliffe holding Mr "
        "Tunnicliffe."]),
    C("Painting", (10, 3), "Painting A", [
        "A painting of the valley before the works: green, quiet, with a "
        "river.",
        "Somebody has added a very small chimney in the corner, in "
        "different paint, so it would feel like home."]),
    C("Urns", (14, 4), "Steel Shelf", [
        "The rack where the three tea urns live, for the three sizes of parish "
        "emergency: a funeral, a wedding, and the fete. All three are out."]),
    C("Brass Pot", (15, 4), "Plant A", [
        "A tall plant in a brass pot. The Sunday school polishes the pot "
        "every week. It is the shiniest thing north of the Tower."]),
    C("Minutes", (5, 7), "Document", [
        "The minutes of the parish council. Item one: the hooter. Item "
        "two: the hooter, again.",
        "Any other business: the hooter."]),
    C("Lost and Found", (8, 7), "Book A", [
        "The parish lost-and-found book. FOUND: ONE BOY, NINE, WITH A "
        "PACKED BAG, ON THE SOUTH ROAD. RETURNED.",
        "FOUND: THE SAME. RETURNED. It goes on like that for two "
        "pages."]),
]

ALL = {11: TOWER, 21: CLANGING, 22: WORKS, 23: SAFETY_VALVE, 24: BRYDS,
       25: PARISH}
