"""CURIOS.md wave C5: the coast and the east - Maps 49-67.

The Sable Hart's brooders, Little Gore's weddings, Sump's curse, Ashcombe
on its new hill, Weeping Bottom's sisters, Fenmarch and the Collegium,
Great Dunnage. Corvin's drowned Ashcombe (Map 66) and the culvert under
Carn Drey (Map 67) are his and Roland's, and are touched lightly."""

import db
from curios import curio as C

# --------------------------------------------------- Map 49, the Sable Hart --
SABLE_HART = [
    C("Black Bottles", (6, 4), "Bottle Shelf A", [
        "Bottles behind the bar, every one with a black label. Mrs Garrow buys "
        "the gloomy labels because her regulars prefer them.",
        "What is inside is elderflower cordial."]),
    C("Hooded Tankards", (7, 4), "Bottle Shelf B", [
        "A shelf of tankards, and over each one, to keep the dust off, "
        "a small knitted hood."]),
    C("Crake's Tankard", (4, 4), "Pint Mug C", [
        "Hollin Crake's tankard, on a coaster he brought from home, so "
        "as not to mark the table."]),
    C("Veyle's Pint", (16, 4), "Pint Mug C", [
        "Silas Veyle's pint, untouched. It is for atmosphere. He orders "
        "a fresh one at nine, and leaves that one too."]),
    C("The Bell", (6, 5), "Bell", [
        "A bell on the bar. You ring it.",
        "Every hooded man in the room looks up - slowly, magnificently - "
        "and then, one by one, goes back to brooding."],
      party=[(db.CORVIN, [("Corvin", "Amateurs.")])],
      trope="hooded_stranger"),
    C("Points Book", (4, 9), "Open Book A (V)", [
        "Rook's book of points. VOW - 3. SCAR - 5. DRAMATIC EXIT - 4.",
        "DRAMATIC EXIT THROUGH A DOOR THAT TURNS OUT TO BE A CUPBOARD - "
        "MINUS 2."],
      party=[(db.CORVIN, [("Corvin", "That was one time.")])]),
]

# ---------------------------------------------------- Map 50, Little Gore --
LITTLE_GORE = [
    C("Window", (7, 9), "Window A", [
        "Through the window: a wedding photograph on the mantelpiece, "
        "and beside it a child's drawing of the same wedding, with all "
        "the hats much bigger."]),
    C("Window", (15, 9), "Window A", [
        "Through the window: a neat room, a sword over the fire and a "
        "teapot on the hob, both very well looked after."]),
    C("Confetti", (13, 10), "Barrel", [
        "A barrel of confetti, labelled FOR THE NEXT ONE.",
        "The children have been at it. There is confetti on the "
        "barrel, the step, the cat, and the vicar."],
      trope="containers"),
    C("Log", (20, 13), "Fallen Log", [
        "A log with a row of daisies laid along it very carefully. They "
        "are the pews."]),
    C("Well", (19, 14), "Well", [
        "The well, tied with ribbons for a wedding. Whether it is a "
        "wedding about to happen or one forty years ago, in Little Gore "
        "it is hard to say, and nobody minds."]),
]

# ---------------------------------------------------------- Map 51, Sump --
SUMP = [
    C("Cactus", (4, 9), "Cactus", [
        "A cactus, with a card stuck on one spine: THINGS USED TO BE "
        "BETTER.",
        "The cactus is the only thing in Sump that disagrees."]),
    C("Pot", (9, 9), "Pot", [
        "A clay pot, empty, with a card: FOR RAIN.",
        "It is a very optimistic pot, and nobody in Sump has the heart "
        "to tell it."]),
    C("Hut Window", (11, 8), "Window A", [
        "Through the parish hut window: a long table, one chair at the "
        "head of it, and a great many empty chairs, kept for when things "
        "get better."]),
    C("Lidded Pot", (14, 9), "Pot", [
        "A pot with a lid, and on the lid a label: WASPS (CONTAINED). "
        "1794.",
        "You do not open it. Nobody opens it. It is minuted."]),
    C("Cactus", (18, 9), "Cactus", [
        "A cactus with a little straw hat on, to keep the sun off. It is "
        "the parish's one luxury."]),
    C("Cactus", (8, 13), "Cactus", [
        "A cactus in a pot with a brass plate: PLANTED TO CHEER THE "
        "PLACE UP. It has been trying for two hundred years."]),
]

# ------------------------------------------------------ Map 52, Ashcombe --
ASHCOMBE = [
    C("Church Glass", (3, 12), "Stained Glass Window B", [
        "Stained glass in the new church: a lake, very blue, and over "
        "it, very small, a man in a boat holding up a drainage plan."]),
    C("Church Glass", (7, 12), "Stained Glass Window B", [
        "Stained glass: a man building a great boat in the rain. The "
        "glazier has given him an umbrella, and the expression of a man "
        "who did say."]),
    C("School Window", (12, 12), "Window A", [
        "Through the school window: a blackboard. A HISTORY OF ASHCOMBE. "
        "1. IT WAS THERE. 2. IT WAS WET. 3. WE MOVED IT."]),
    C("School Window", (16, 12), "Window A", [
        "Through the window: rows of desks, and on every desk, a paper "
        "boat."]),
    C("Window", (24, 12), "Window A", [
        "Through the window: a front room with a line painted on the "
        "wall at knee height, a date beside it, and a smiley face."]),
    C("Window", (28, 12), "Window A", [
        "Through the window: a family at tea. Every chair stands on "
        "little stilts. Old habits."]),
    C("Vegetables", (6, 19), "Crops D", [
        "A fruit patch, every row labelled by a child: RASPBERRIES (DRY). "
        "CURRANTS (DRY). EVERYTHING HERE IS DRY NOW."]),
    C("Scarecrow", (9, 20), "Scarecrow", [
        "A scarecrow in waders, with a life ring round its middle. "
        "Ashcombe has moved up a hill, and the scarecrow is not taking "
        "any chances."],
      trope="scarecrow"),
    C("Post Office Window", (21, 22), "Window A", [
        "Through the post office window: sacks of letters, every one "
        "answered, with the answers tied on to them with ribbon."]),
]

# ---------------------------------------------- Map 53, Ashcombe, Indoors --
DRAIN_BOOKS = [
    ["DRAINS OF THE WORLD, Volume One: Ashcombe. There is no Volume "
     "Two. Nowhere else has been worth it."],
    ["WATER, AND WHERE IT OUGHT TO GO. Heavily annotated: SEE ABOVE. "
     "NO. DOWNHILL. DOWNHILL!"],
    ["THE ASHCOMBE COMMITTEE FOR DRAINAGE: MINUTES. The first meeting "
     "was held on a boat."],
]

ASHCOMBE_INDOORS = [
    C("Oven", (2, 4), "Oven", [
        "A new black oven, very proud of itself. A loaf is cooling on "
        "top with a note: NOT FOR THE COMMITTEE."]),
    C("Sink", (4, 4), "Sink", [
        "A sink under the big window. In Ashcombe everybody does the "
        "washing up looking at the lake, and nobody minds doing the "
        "washing up."]),
    C("Teapot", (6, 7), "Teapot A", [
        "A teapot, and beside it a cosy knitted in the shape of the old church,"
        " spire and all. It is too good to use."]),
    C("Kitchen Clock", (8, 3), "Clock", [
        "A kitchen clock, carried up the hill on the day of the water. "
        "It has been running ever since, and it has never once been "
        "late for anything."]),
    C("Exhibit", (21, 4), "Potted Plant A", [
        "A potted plant with a label: EXHIBIT FOURTEEN. A PLANT (DRY)."],
      trope="museum"),
    C("Exhibit", (30, 4), "Potted Plant A", [
        "A potted plant: EXHIBIT FIFTEEN. ANOTHER PLANT (ALSO DRY). The "
        "museum is very proud of everything in it that is dry."]),
    C("Study Books", (42, 4), "Bookshelf A", DRAIN_BOOKS[0],
      then=DRAIN_BOOKS[1:]),
    C("Globe", (42, 6), "Globe", [
        "A globe, with all the water on it painted a slightly "
        "disapproving shade of blue."]),
    C("Study Window", (43, 3), "Large Window A", [
        "The study window looks out over the lake, flat and bright, and "
        "exactly where the village used to be."]),
    C("Plan Drawers", (47, 4), "Chest of Drawers", [
        "A chest of drawers labelled PLANS. PLANS (OLD). PLANS (WET)."]),
    C("The Blotter", (46, 6), "Pen A", [
        "A pen and a blotter. On the blotter, backwards, the word DRAINS, "
        "a great many times, and once, very small, the word WON."]),
]

# ------------------------------------------------- Map 54, Weeping Bottom --
WEEPING = [
    C("Window", (11, 11), "Window A", [
        "Through the window: patients in rows, in blankets, all looking "
        "at the sea with the faces of people being told it is good for "
        "them."]),
    C("Window", (19, 11), "Window A", [
        "Through the window: a Sister hanging washing up indoors. It is "
        "the only way anything in Weeping Bottom ever gets dry, and it "
        "does not."]),
    C("Mushrooms", (8, 7), "Mushrooms A", [
        "Mushrooms, on the path, on the wall, and on a bench. The "
        "Sisters stopped trying in about 1750."]),
    C("Mushroom", (21, 12), "Mushrooms A", [
        "A mushroom with a very small bandage on it. Nobody goes "
        "untreated in Weeping Bottom."]),
    C("Chapel Glass", (8, 17), "Stained Glass Window B", [
        "Stained glass: Mother Ursula Pym, the founder, holding up a pair "
        "of socks like a holy relic.",
        "They are dry. It is the only dry thing in any window in the "
        "Order."]),
]

# ---------------------------------------------------- Map 55, the Sisterhouse --
SISTERHOUSE = [
    C("Window", (5, 3), "Large Window A", [
        "A window onto the sea, with a sign: FRESH AIR - TEN MINUTES. NO "
        "MORE. IT IS VERY STRONG HERE."]),
    C("Bed", (4, 5), "Bed", [
        "A bed on the left side of the ward, under a card: WHATEVER "
        "WORKS. The patient in it is eating toast."]),
    C("Bed", (20, 5), "Bed", [
        "A bed on the right side, under a card: CORRECT TREATMENT, STAGE "
        "SIX.",
        "Toast is permitted at stage nine. The patient is looking across "
        "the line at the toast."]),
    C("Soup", (4, 7), "Soup Bowl", [
        "A bowl of soup, ready for anybody.",
        "It is the same soup on both sides of the line. Both sides know "
        "it. Nobody says."]),
    C("Leeches", (19, 7), "Pot A", [
        "A jar of leeches, labelled HISTORICAL. They are retired, and "
        "they are treated with great respect."]),
    C("Stage Notes", (20, 7), "Closed Books C", [
        "Sister Bewick's notes, in eleven volumes: one for each stage of "
        "the correct treatment. Volume eleven is very thin. Nobody has "
        "got that far."]),
    C("Hourglass", (21, 7), "Hourglass", [
        "Sister Bewick's hourglass, for timing pulses, stages, and how "
        "long a patient has been allowed to sit up."]),
    C("Bed", (13, 10), "Bed", [
        "A bed exactly on the line down the middle of the ward. It is "
        "the most argued-about bed in the Order."]),
    C("Potted Plant", (24, 11), "Potted Plant A", [
        "A potted plant on the right side of the ward. It has its own "
        "chart, and it is at stage four."]),
]

# ------------------------------------------------------ Map 56, Fenmarch Hall --
FENMARCH = [
    C("Mushrooms", (13, 15), "Mushrooms A", [
        "Mushrooms on the lawn, which is also, in places, the moat."]),
    C("Mushrooms", (24, 18), "Mushrooms A", [
        "Mushrooms in a neat ring. The gardener has put a little "
        "border of stones round them, as if they were meant."]),
]

# ----------------------------------------------------- Map 57, the Long Gallery --
GALLERY = [
    C("Clock", (11, 3), "Clock", [
        "A clock with a card on top: ROBIN (STUFFED) - AWAY FOR CLEANING. The "
        "clock looks a little lonely without it."]),
    C("Soup", (6, 6), "Soup Bowl", [
        "A bowl of soup on a tray, left for Mr Ottershaw, with a note "
        "from Mrs Puddifoot: EAT IT WHILE IT IS HOT. NOT LIKE LAST "
        "TIME."]),
    C("Fern", (2, 8), "Potted Plant B", [
        "A potted fern, labelled as carefully as everything else in the "
        "gallery: FERN (LIVING). DO NOT STUFF."]),
    C("Plant", (45, 8), "Potted Plant B", [
        "A potted plant at the far end of the gallery, with a label: "
        "PLANT (ALSO LIVING). PLEASE TELL MR OTTERSHAW."]),
]

# ---------------------------------------------------- Map 58, the Great Court --
GREAT_COURT = [
    C("Tapestry", (7, 7), "Tapestry B", [
        "A tapestry of the Founder founding the Collegium, in one "
        "afternoon. In the corner, very small, the Founder's tea, going "
        "cold."]),
    C("Tapestry", (11, 7), "Tapestry B", [
        "The Collegium's arms, and the motto in Old Arcane: FLAMMA NON "
        "CORRUMPIT.",
        "Under it, much later, in a different thread: (MOSTLY)."],
      party=[(db.ZEPH, [("Zephyrine", "That 'mostly' is about me. I'm "
                         "very proud of it.")])]),
    C("Glass", (5, 7), "Stained Glass Window B", [
        "Stained glass: a wizard reading a book.",
        "In the next panel, the same wizard, singed."]),
    C("Glass", (13, 7), "Stained Glass Window B", [
        "Stained glass: a Dean in full robes, presenting a scroll. The "
        "scroll says ENQUIRY."]),
    C("Window", (20, 7), "Window A", [
        "Through the window: a lecture room, a lecturer, and one "
        "student, asleep. The lecturer is also asleep."]),
    C("Window", (26, 7), "Window A", [
        "Through the window: a laboratory where every surface is "
        "scorched, and there is a fire bucket on every surface."],
      trope="wizard_school"),
    C("Window", (3, 20), "Window A", [
        "Through the window: a student's room, a pointed hat on a peg, "
        "and a card on the inside of the door: DO NOT ENTER - "
        "PRACTISING."]),
    C("Window", (20, 20), "Window A", [
        "Through the window: a desk piled with books, and a student "
        "asleep on the pile, with a quill still in his hand and a word "
        "half-finished."]),
]

# ------------------------------------------------------- Map 59, the Library --
LIBRARY_BOOKS = [
    ["MAGIC: AN INTRODUCTION, Forty-First Edition. Each edition says in "
     "its preface that all the others were wrong."],
    ["ON THE QUANTITY OF FIRE APPROPRIATE TO A LECTURE, by the Dean. A "
     "pamphlet. It is mostly the word NONE."],
    ["THE COLLEGIUM: A HISTORY IN ONE AFTERNOON. It is six hundred "
     "pages long."],
    ["A DICTIONARY OF SPELLS, with SPELLS spelt wrong on the spine. "
     "Nobody has ever said."],
    ["ADVANCED LEVITATION, on the very top shelf, out of reach, where "
     "it has always been. The students say that is the point."],
]

LIBRARY = [
    C("Stacks", [(10, 4), (11, 4)], "Bookshelf B", LIBRARY_BOOKS[0],
      then=LIBRARY_BOOKS[1:3]),
    C("Stacks", [(12, 4), (13, 4)], "Bookshelf B", LIBRARY_BOOKS[3],
      then=LIBRARY_BOOKS[4:]),
    C("Basin", (2, 4), "Basin", [
        "A basin for washing the ink off. The water in it has been "
        "permanently blue since the Collegium was founded."]),
    C("Hourglass", (3, 7), "Hourglass", [
        "An hourglass on the librarian's desk, for timing how long you "
        "have had a book. The sand in it is from the First Dean's "
        "holiday."]),
    C("A Reader's Book", (4, 10), "Open Book A (H)", [
        "A book left open at a chapter on fire safety. The bookmark in "
        "it has been very slightly singed."]),
    C("Star Globe", (23, 12), "Globe", [
        "A globe of the stars. A great many of the stars have been "
        "labelled MINE, in different hands, by students."]),
]

# ---------------------------------------------------------- Map 60, the Hall --
HALL_PORTRAITS = [
    C("Portrait", (18, 3), "Portrait B", [
        "A portrait of a Dean, painted with his eyebrows raised. They "
        "were always raised. The painter just painted what was "
        "there."]),
    C("Portrait", (20, 3), "Portrait B", [
        "A portrait of another Dean. There is a small scorch mark on "
        "the corner of the frame, at about the height of a hedge "
        "mage."],
      party=[(db.ZEPH, [("Zephyrine", "Allegedly.")])]),
    C("Potted Plant", (2, 13), "Potted Plant B", [
        "A potted plant, with a label: FELLOW OF THE COLLEGIUM "
        "(HONORARY). It was elected by a margin of one, after a long "
        "evening."]),
]

# -------------------------------------------------------- Map 61, Great Dunnage --
DUNNAGE = [
    C("Barrel", (8, 11), "Barrel", [
        "A barrel with the Corporation's seal on it, the date 1788, and "
        "the word EMPTY.",
        "Like everything else in Great Dunnage that was sealed in 1788, "
        "it is empty."]),
    C("Barrel", (26, 14), "Barrel", [
        "A barrel of nails on the quay, stencilled BONDED. A watchman has "
        "chalked a tally beside it, and keeps glancing at you."]),
    C("Hay", (0, 16), "Hay", [
        "Hay for the cart horses. A cat is asleep in it, very "
        "officially, with a little brass tag on: WAREHOUSE CAT."]),
    C("Crates", (27, 18), "Crate A", [
        "Crates on the quay stencilled GREAT DUNNAGE - TO ALL PARTS.",
        "Smaller: (MOSTLY SUMP)."],
      trope="containers"),
    C("Bollard", (32, 19), "Mooring Bollard A", [
        "A bollard. A boatman has left his pipe on it, and the pipe is "
        "still warm, and the boatman is nowhere to be seen."]),
]

# -------------------------------------------------- Map 62, the Smiths' Hall --
SMITHS_HALL = [
    C("Shield", (4, 3), "Shield", [
        "A shield with the Smiths' arms: two swords crossed, and the "
        "motto STRIKE WHILE IT IS HOT.",
        "Smaller, underneath: AND THEN LET IT COOL. WE ARE NOT ANIMALS."]),
    C("Prize Shield", (17, 3), "Shield", [
        "A prize shield, every rivet perfect, with a card: BEST IN HALL, "
        "1987 - B. OLLERENSHAW."],
      party=[(db.HOB, [("Hob", "I didn't enter in eighty-seven. I had "
                        "a cold. ...I'd have won.")])]),
    C("Armour", (2, 5), "Armor A (Stand)", [
        "A suit of armour made by an apprentice for his examination. The "
        "examiners' note is pinned to it: PASSED. ONE ELBOW "
        "BACKWARDS."]),
    C("Records", (9, 5), "Closed Books C", [
        "The Hall's records: every masterpiece ever submitted, marked "
        "out of ten.",
        "Nobody has ever been given ten. Two smiths have been given "
        "eleven, and the Hall is still arguing about it."]),
    C("Ceremonial Hammers", (12, 5), "Hammers", [
        "Ceremonial hammers, much too big to use, polished every day by "
        "the newest apprentice, who is not yet allowed to touch the "
        "real ones."]),
    C("Visitors' Book", (16, 8), "Open Book A (H)", [
        "The visitors' book: SMITHS, TRAVELLING. Every entry says which "
        "forge the smith came from, and how much better it is."]),
    C("Prize Sword", (17, 8), "Sword A", [
        "Last year's prize sword, on a stand. The card says it is the "
        "finest sword in the island. It is very fine. It is also, "
        "somehow, smug."],
      party=[(db.HOB, [("Hob", "The balance is off. Half an ounce. "
                        "...It's lovely, mind.")])]),
    C("Armour", (2, 9), "Armor A (Stand)", [
        "A suit of armour with a card on it: ENTERED FOR THE PRIZE BY A "
        "SMITH WHO WISHES TO REMAIN ANONYMOUS. The card is in Warden "
        "Crabbe's handwriting."]),
]

# --------------------------------------------------- Map 63, the Counting House --
COUNTING_HOUSE = [
    C("Applications", (13, 6), "Open Book A (H)", [
        "The Town Clerk's book of applications to open the Counting "
        "House. Two hundred and twelve years of them.",
        "Every one is marked DECLINED - FORM L INCOMPLETE. The clerk who "
        "wrote the first one also designed Form L."]),
]

# -------------------------------------------------- Map 64, the Bonded Warehouse --
WAREHOUSE = [
    C("Large Crate", (10, 4), "Large Crate", [
        "A tag: BOND No. 2 - ONE STATUE OF THE FIRST MAYOR, ACTUAL SIZE.",
        "DUTY: ON THE HAT."],
      trope="containers"),
    C("Large Crate", (14, 4), "Large Crate", [
        "BOND No. 7 - TEN THOUSAND BUTTONS, ALL DIFFERENT. DECLARED AS ONE "
        "BUTTON, REPEATED."]),
    C("Large Crate", (16, 4), "Large Crate", [
        "BOND No. 9 - A SHIP IN A BOTTLE. THE SHIP IS FULL SIZE. THE "
        "BOTTLE IS NOT DESCRIBED."]),
    C("Large Crate", (18, 4), "Large Crate", [
        "BOND No. 11 - FOG, ONE BARREL, FROM NETHER SOPPING. DUTY PAID IN "
        "ADVANCE, BY NETHER SOPPING, TO BE RID OF IT."]),
    C("Crate", (9, 6), "Crate A", [
        "BOND No. 23 - SPARE KEYS, FOR THE COUNTING HOUSE.",
        "The crate is empty. That explains a great deal."]),
    C("Barrel", (13, 6), "Barrel", [
        "BOND No. 31 - RAIN, ONE BARREL, RETURNED BY UPPER CLANGING AS "
        "SECOND-HAND."]),
    C("Large Crate", (9, 9), "Large Crate", [
        "BOND No. 40 - ONE CABBAGE, VERY LARGE, 'FOR THE SHOW'.",
        "The show was in 1802. Nobody has been brave enough to check on "
        "the cabbage."]),
    C("Barrel", (18, 9), "Barrel", [
        "BOND No. 58 - ONE TONGUE-TWISTER (UNSOLVED). A label on the lid: "
        "PLEASE DO NOT READ ALOUD."]),
    C("Crate", (19, 9), "Crate A", [
        "BOND No. 52 - THE CONTENTS OF THIS CRATE.",
        "DUTY: ON THE CRATE."]),
]

# ------------------------------------------------------------ Map 65, the Bell --
THE_BELL = [
    C("Scored Bottles", (3, 4), "Bottle Shelf A", [
        "Bottles behind the bar, each with a score card tucked behind "
        "it: SHERRY - 7. PORT - 8.",
        "GINGER WINE - 2. IT ISN'T PERSONAL."]),
    C("Trophies", (6, 4), "Bottle Shelf B", [
        "Bottles, and among them the trophies, which are bottles too, with "
        "ribbons on: BEST BALLAD (SAD). BEST BALLAD (NOT SAD).",
        "And a very small one at the end: BEST BALLAD (UNDECIDED)."],
      party=[(db.PIPER, [("Piper", "I want the little one. The little "
                          "one's the hardest to win.")])]),
    C("Tankard", (4, 5), "Pint Mug C", [
        "A tankard with a score card propped against it: 6.",
        "Nobody knows what the tankard did."]),
    C("Judges' Table", (14, 7), "Table C", [
        "The judges' table: pencils, score cards, and a little silver "
        "bell for when time is up. It has been rung a great deal, and "
        "is slightly bent."]),
    C("Tankard", (7, 10), "Pint Mug C", [
        "A tankard with a card under it: RESERVED FOR THE WINNER. It "
        "has been reserved since the spring."]),
]

ALL = {49: SABLE_HART, 50: LITTLE_GORE, 51: SUMP, 52: ASHCOMBE,
       53: ASHCOMBE_INDOORS, 54: WEEPING, 55: SISTERHOUSE, 56: FENMARCH,
       57: GALLERY, 58: GREAT_COURT, 59: LIBRARY, 60: HALL_PORTRAITS,
       61: DUNNAGE, 62: SMITHS_HALL, 63: COUNTING_HOUSE, 64: WAREHOUSE,
       65: THE_BELL}
