"""CURIOS.md wave C1: Thistlewick, Maps 1-7.

The village Bram has lived in all his life, so he knows what most of it is
and the joke is usually what it means now that he is the Forty-Eighth. Six
of the companions are found here and any of them may be with him on a
second visit."""

import db
from curios import curio as C

# ------------------------------------------------------------ Map 1, out --
THISTLEWICK = [
    # --- the Hall and the chapel, top of the square
    C("The Hall's Crest", (10, 10), "Shop Sign (Crest)", [
        "The crest over the Prophecy Hall door: a turnip rampant, on a "
        "field of slightly different turnips.",
        "The motto is in Old Thistlewick: NON NOBIS, NISI FORTE. "
        "Not us, unless it has to be."],
      again=["The turnip rampant. It has been repainted so often that "
             "it is now mostly paint, and slightly more rampant."]),
    C("The Hall Window", (9, 10), "Window A", [
        "Through the window: the Committee, in session. One of them "
        "sees you and holds a form up to the glass.",
        "You duck."],
      again=["The Committee is still in session. The Committee is "
             "always in session. It is how they know they exist."]),
    C("The Other Hall Window", (15, 10), "Window A", [
        "On the sill inside, a row of forty-seven little clay figures, "
        "one for each Chosen One, made by the village school.",
        "At the end, a forty-eighth has been started. So far it is "
        "mostly turnip."],
      again=["The forty-eighth figure has been given a sword since you "
             "last looked. It is holding it by the wrong end."]),
    C("The Chapel's Teapot", (26, 10), "Shop Sign (Teapot)", [
        "A teapot hangs over the chapel door on a bracket.",
        "The Order of Whatever Works never chose a symbol. It held a "
        "meeting about one, and somebody made tea, and that was the "
        "meeting."],
      party=[(db.MERRI, [("Merribell",
                          "It works. They come in for the tea and "
                          "they stay for the stitches.")])],
      again=["The teapot. On cold mornings it steams, which nobody can "
             "explain, and the Order does not try."]),
    C("Chapel Glass", (30, 10), "Stained Glass Window B", [
        "Stained glass: a saint with a bandage, a saint with a cup of "
        "water, and a saint pointing very firmly at a third saint's "
        "foot.",
        "Underneath: THE SAINTS OF WHATEVER WORKS. PATRONS OF SITTING "
        "DOWN."]),

    # --- the churchyard. Villagers, not Chosen Ones: Thistlewick does not
    # say how many came back, and the stones do not either.
    C("Headstone", (34, 4), "Grave A", [
        "HERE LIES OSWIN FARROW.",
        "HE SAID IT WAS PROBABLY FINE."],
      trope="grave_puns",
      again=["OSWIN FARROW. HE SAID IT WAS PROBABLY FINE. Somebody has "
             "left a hard hat on the stone."]),
    C("Headstone", (36, 4), "Grave B", [
        "ELSPETH MOORE, 1902 - 1994. SHE WON THE TURNIP SHOW FORTY-ONE "
        "YEARS RUNNING.",
        "Below that, in smaller and much angrier capitals: THE "
        "FORTY-SECOND WAS FIXED."],
      again=["Somebody has left a rosette on Elspeth's stone. It says "
             "SECOND. It is the most pointed rosette you have ever "
             "seen."]),
    C("A Small Stone", (34, 6), "Grave B", [
        "IN MEMORY OF COUNCILLOR (THE FIRST). A GOAT.",
        "SERVED THREE TERMS. NEVER ONCE SPOKE OUT OF TURN."],
      again=["A small stone for a goat. The present Councillor is "
             "sometimes seen standing beside it, looking thoughtful, "
             "and eating the flowers."]),
    C("Headstone", (36, 6), "Grave A", [
        "WALTER PIKE.",
        "HE KNEW A SHORTCUT."],
      again=["WALTER PIKE. HE KNEW A SHORTCUT. There is a little arrow "
             "carved under it, pointing at the hedge. Nobody has ever "
             "been brave enough."]),
    C("Headstone", (34, 8), "Grave A", [
        "MABEL THISTLE, 1890 - 1979. Your great-grandmother.",
        "SHE GREW A TURNIP AS BIG AS A CHAIR, AND SAT ON IT, AND THEN "
        "IT WAS THE CHAIR."],
      again=["Great-granny Mabel. The chair is still in the "
             "family. Your mother uses it for the good visitors."]),

    # --- the market crates
    C("Big Crate", (16, 13), "Large Crate", [
        "A big crate stencilled THIS WAY UP, with an arrow pointing at "
        "the ground."],
      trope="containers",
      again=["THIS WAY UP. The arrow still points at the ground. "
             "Whoever stacked it trusted the arrow."]),
    C("Crate", (17, 12), "Crate A", [
        "A crate stencilled TURNIPS. You lift the lid. Turnips."],
      then=[["Turnips."],
            ["You check again, in case they have turned into something "
             "else while you weren't looking.", "Turnips."]],
      again=["Turnips. You are beginning to understand the farmers."]),
    C("Crate", (17, 13), "Crate D", [
        "A crate marked FRAGILE in letters so big that they used up all "
        "the paint.",
        "The second word, which is presumably TURNIPS, is in pencil."]),
    C("Market Crate", (22, 12), "Crate B", [
        "The market's potatoes, in a crate, under a card that says "
        "FRESH."]),
    C("Market Crate", (23, 12), "Crate C", [
        "Tomatoes. The card on these says MOSTLY."]),
    C("Market Crate", (22, 13), "Crate E", [
        "Carrots. There is no card on the carrots.",
        "You decide not to ask."]),
    C("Market Crate", (23, 13), "Crate F", [
        "Fish, on ice, under a card: CAUGHT LOCALLY.",
        "The only water in Thistlewick is the pond, and there are no "
        "fish in the pond. You decide not to ask the fish, either."],
      party=[(db.NIX, [("Nix", "Locally is a very elastic word. I "
                        "respect it.")])]),

    # --- round the well
    C("Water Butt", (16, 16), "Barrel", [
        "A water butt by the well, with a notice nailed to it: THIS IS "
        "ALSO NOT A WISHING BARREL."],
      again=["There is a coin at the bottom of the water butt anyway. "
             "Thistlewick is a village of optimists, and of people who "
             "do not read notices."]),
    C("Barrel", (23, 16), "Barrel", [
        "You look in the barrel. There is a smaller barrel inside it."],
      then=[["You look in the smaller barrel. There is not a smaller "
             "barrel inside that one.",
             "You feel, obscurely, let down."]],
      again=["Barrel. Smaller barrel. You have got to the bottom of "
             "it."]),

    # --- the fields
    C("Your Turnips", [(11, 20), (11, 21), (11, 22), (11, 23)], "Crops B", [
        "Your turnips. You planted this row in the spring, and it has "
        "come up beautifully, which feels a little pointed now you are "
        "leaving."],
      again=["Your turnips. They will be fine. They are turnips. It is "
             "the one thing everybody agrees on about them."]),
    C("Turnips", [(13, 20), (13, 21), (13, 22), (13, 23)], "Crops B", [
        "Turnips. One of them has a tiny flag in it: KEPT BACK FOR THE "
        "CHOSEN ONE'S SUPPER. The flag is very, very old.",
        "They plant a fresh turnip under it every spring, just in "
        "case. It has been very good for the turnips."]),
    C("Turnips", [(15, 20), (15, 21), (15, 22), (15, 23)], "Crops B", [
        "A row of turnips, and a small, tired sign: PLEASE DO NOT PULL "
        "THE TURNIPS UP TO SEE IF ONE OF THEM IS A SWORD IN A STONE.",
        "NONE OF THEM IS. WE HAVE CHECKED. ALL OF THEM."],
      trope="sword_in_stone"),
    C("Turnips", [(17, 20), (17, 21), (17, 22), (17, 23)], "Crops B", [
        "Turnips, in a row so straight that somebody must have used "
        "string. Somebody did. The string is still there.",
        "It is the Farmer's best string, and he would like it back "
        "after the harvest."]),
    C("The Fisher's Log", (26, 24), "Fallen Log", [
        "A fallen log by the pond, worn smooth on top where the Fisher "
        "sits to eat his lunch.",
        "There is a hollow in it exactly the shape of thirty-one "
        "years."]),
    C("Another Log", (31, 25), "Fallen Log", [
        "A log. A beetle is sitting on it, looking at the pond, with "
        "the air of somebody who has also been waiting thirty-one "
        "years for a fish."]),
    C("Mushrooms", (34, 22), "Mushrooms B", [
        "Mushrooms, in a clump. Big red ones with white spots, looking "
        "very edible and slightly smug about it."],
      party=[(db.MERRI, [("Merribell", "Don't.")]),
             (db.WREN, [("Wren",
                         "Oh, lovely. Those will kill a horse. Mind "
                         "your hands.")]),
             (db.ZEPH, [("Zephyrine", "I could set fire to them. "
                         "That's a joke. Mostly.")])],
      again=["The mushrooms. You leave them alone, which is what they "
             "want you to think you decided."]),

    # --- the shops' fronts
    C("The Emporium Window", (25, 22), "Window A", [
        "In the Emporium's window: a stuffed owl, a lute with no "
        "strings, a single boot, and a card that says EVERYTHING MUST "
        "GO.",
        "Somebody has added, in a small neat hand: (BACK)."],
      party=[(db.NIX, [("Nix", "That's not mine. The card. The boot's "
                        "mine.")])]),
    C("The Emporium's Other Window", (32, 22), "Window A", [
        "A card in the window: WE BUY ANYTHING. Under it, smaller: WE "
        "ASK NOTHING.",
        "Under that, smaller still, in a different pen: PLEASE ASK "
        "SOMETHING. - YOUR NEIGHBOURS."]),
    C("Emporium Sign", (26, 22), "Shop Sign (Sword & Shield)", [
        "A painted sign: a sword crossed with a shield.",
        "The Emporium does not sell swords or shields. It has, at "
        "various times, had them in."]),
    C("Emporium Sign", (30, 22), "Shop Sign (Sack)", [
        "A painted sack, and NIX'S EMPORIUM. EST. RECENTLY. The sack is "
        "painted a little open, so you cannot see what is in it.",
        "This is, you suspect, the whole business model."]),
    C("The Tankard Sign", (3, 22), "Shop Sign (Pub)", [
        "A tin tankard hangs on a bracket over the inn and creaks when "
        "the wind blows.",
        "It creaks in exactly the rhythm of the Gilded Turnip's "
        "favourite song, and has taught it to three generations of "
        "the village."]),
    C("The Inn Sign", (7, 22), "Shop Sign (Inn)", [
        "THE GILDED TURNIP. ROOMS. Somebody has given it a star in "
        "chalk.",
        "Somebody else has added four more stars in a different chalk, "
        "in Prudence's handwriting."]),
    C("The Inn Window", (4, 22), "Window A", [
        "Through the window: the inside of the Gilded Turnip, warm and "
        "brown and loud.",
        "Somebody in there is singing about you. It is not entirely "
        "flattering, and it rhymes 'Bram' with 'jam'."],
      party=[(db.PIPER, [("Piper", "That one's mine. The jam was a "
                          "placeholder. It's tested very well.")])]),
    C("The Smithy Sign", (8, 31), "Shop Sign (Hammer)", [
        "A hammer on a bracket over the smithy door.",
        "It is just a hammer. It is not Beatrice. Beatrice would never "
        "be left out in the rain."],
      party=[(db.HOB, [("Hob", "She'd rust. She'd never say. She'd "
                        "just rust at me.")])]),
    C("The Smithy Window", (4, 31), "Window A", [
        "The smithy's window is black with soot, except for one clean "
        "circle about the size of a nose.",
        "That is where the apprentice looks out to see if it is still "
        "raining."]),
    C("Your Window", (26, 31), "Window A", [
        "Your own front window. On the sill: your mother's geraniums, "
        "and a turnip in a pot that you are growing as an experiment.",
        "It has not done anything you would call an experiment."]),
    C("Your Other Window", (31, 31), "Window A", [
        "Your window. You have looked out of it every morning of your "
        "life.",
        "It looks very odd from this side, and so, through it, does "
        "the kitchen."]),
]

# -------------------------------------------------------- Map 2, at home --
HOME = [
    C("Your Drawers", (6, 4), "Chest of Drawers", [
        "Your chest of drawers. Your mother has packed for you already: "
        "socks, more socks, a vest, and a note.",
        "The note says WEAR THE VEST."],
      then=[["WEAR THE VEST."]],
      again=["You are wearing the vest."]),
    C("Your Bedside Table", (5, 4), "Table F", [
        "Your bedside table: your mother's flowers, The Turnip Grower's Almanac"
        " (1997), and a glass of water.",
        "Your mother puts the water there every night in case you wake "
        "up Chosen. You did, in the end."]),
    C("The Rain Barrel", (12, 4), "Barrel", [
        "The rain barrel. Your mother keeps it indoors, ever since the "
        "goat."],
      again=["The rain barrel. Nobody in the family talks about the "
             "goat, and the goat has never said."]),
    C("Breakfast", (11, 6), "Dinner Set A (Bottom)", [
        "Breakfast, laid for two. Turnip. Your mother has cut yours into "
        "the shape of a sword.",
        "It is the most supportive thing anybody has done for you all "
        "day."],
      again=["The turnip sword. You will eat it later, as a sort of "
             "rehearsal."]),
    C("The Mirror", (4, 9), "Mirror", [
        "You look in the mirror. The Chosen One looks back at you.",
        "He has a bit of turnip on his chin."],
      then=[["The Chosen One still has turnip on his chin."],
            ["You wipe it off. The Chosen One looks somehow worse "
             "without it."]],
      again=["The Chosen One. He'll do. He will have to."]),
    C("The Old Crate", (13, 9), "Crate A", [
        "A crate of your old things: a wooden sword, a cardboard "
        "shield, and a paper crown with CHOSEN ONE on it in your own "
        "writing, aged six.",
        "You put the lid back on quite quickly."],
      party=[(db.PIPER, [("Piper", "Oh, no, no, no. Open it again. "
                          "That's chapter one.")]),
             (db.NIX, [("Nix", "I'll give you two crowns for the "
                        "crown.")])],
      again=["The crate of your old things. It is staying shut. It is "
             "staying shut for ever."]),
]

# ---------------------------------------------------- Map 3, the Hall --
HALL_TITLES = [
    ["A bound volume of minutes: THE MEETING TO DECIDE WHEN TO HOLD "
     "THE MEETING, Volume IV."],
    ["A slim book: PROPHECY - A USER'S GUIDE. Chapter One is 'Have You "
     "Tried Being Chosen Again?'"],
    ["STANDING ORDERS OF THE PROPHECY COMMITTEE, Revised. It has been "
     "revised in pencil, on every page, by somebody who was outvoted on "
     "all of them."],
    ["THE FORTY-SEVEN: A SOUVENIR. Every page has a portrait, a date, "
     "and a pressed flower. The flowers are all turnip flowers."],
    ["A dictionary. It has been opened at SLAIN and DEFEATED so often "
     "that it now falls open there by itself."],
    ["SO YOU'VE BEEN CHOSEN: A LEAFLET. It is one page long. The page "
     "says CONGRATULATIONS!",
     "And then, in very much smaller print: CLAUSE FOUR APPLIES."],
    ["The accounts of the Prophecy Fund. Income: the fete. Expenditure: "
     "swords, forty-seven. Scroll, a great deal."],
    ["WHAT TO DO IF THE CHOSEN ONE IS NOT IN. It recommends leaving a "
     "note, and choosing again if he has not replied by Thursday."],
]

# The room behind the Archive Door is where struck material goes.
STRUCK_TITLES = [
    ["STRUCK: A HISTORY, Volume One.", "Volume One has been struck."],
    ["VERSES STRUCK FROM THE BALLAD, by decade. The 1950s are one page, "
     "and the page is mostly crossings-out."],
    ["THE PROPHECY: EARLY DRAFTS. In the first, the Dark Lord rises "
     "'every hundred years, or so'.",
     "Somebody has crossed out OR SO. Somebody else has crossed out the "
     "crossing out."],
    ["NAMES CONSIDERED FOR THE OBLIGATORY TOWER: The Compulsory Tower. "
     "The Mandatory Tower. The Tower You Have To. The Tower (Sorry)."],
    ["A box file marked MISC (STRUCK). It is empty. Even the misc was "
     "struck."],
    ["THINGS NOT TO READ ALOUD AT THE FETE.",
     "Somebody has written inside the cover, in Mrs Wispel's hand: NOW "
     "you tell me."],
]

HALL = [
    C("Hall Window", (6, 3), "Large Window B", [
        "A tall window looking out over the square. A man with a ladder "
        "walks past with no ladder-related purpose whatsoever.",
        "The Committee pays him to look busy when visitors come. He "
        "has done it for twenty years and is extremely good at it."]),
    C("The First Window", (10, 3), "Stained Glass Window", [
        "Stained glass: the First Chosen One, slaying the Dark Lord.",
        "The glazier has given the Dark Lord a very patient expression, "
        "like a man waiting for a bus he has been told is coming."],
      trope="mural"),
    C("Pillar", (5, 4), "Stone Pillar A", [
        "A stone pillar, with a little brass plate: THIS PILLAR HOLDS UP "
        "THE HALL, BY ORDER OF THE COMMITTEE (MINUTE 4,410)."],
      again=["You wonder what the pillar was doing before minute "
             "4,410. Nobody wants to find out."]),
    C("Pillar", (15, 4), "Stone Pillar A", [
        "The other pillar. Its plate says THIS PILLAR ALSO, BY A MAJORITY "
        "OF ONE."]),
    C("Committee Shelves", [(3, 7), (4, 7)], "Bookshelf B",
      HALL_TITLES[0], then=HALL_TITLES[1:3], trope="bookshelf"),
    C("Committee Shelves", [(3, 11), (4, 11)], "Bookshelf B",
      HALL_TITLES[3], then=HALL_TITLES[4:6]),
    C("Committee Shelf", (5, 11), "Bookshelf A",
      HALL_TITLES[6], then=HALL_TITLES[7:]),
    C("Struck Shelves", [(29, 5), (30, 5)], "Bookshelf B",
      STRUCK_TITLES[0], then=STRUCK_TITLES[1:3]),
    C("Struck Shelves", [(32, 5), (33, 5)], "Bookshelf B",
      STRUCK_TITLES[3], then=STRUCK_TITLES[4:]),
    C("The Elder's Note", (9, 6), "Note A (V)", [
        "A note in Elder Wispel's hand: BUY MORE SCROLL."],
      again=["BUY MORE SCROLL. It is underlined twice. The Prophecy "
             "is very long."]),
    C("The Abridged Prophecy", (11, 6), "Closed Book A (V)", [
        "THE PROPHECY OF THISTLEWICK (ABRIDGED).",
        "It is exactly as long as the unabridged one. The abridging was "
        "done by the Committee."],
      trope="lore"),
    C("Scrolls", (29, 7), "Scrolls A", [
        "Scrolls, tied up with red tape. Actual red tape: the Committee "
        "buys it by the mile, from a man in Nether Sopping."]),
    C("Scrolls", (33, 7), "Scrolls A", [
        "A scroll labelled CLAUSE TWELVE - DO NOT LOSE. It is tied up "
        "very tight, by somebody who would quite like to lose it."]),
    C("Scrolls", (6, 11), "Scrolls A", [
        "A scroll: a petition to rename the Obligatory Tower the "
        "Optional Tower.",
        "It has one signature on it, and the signature is Councillor "
        "Fenn's."]),
    C("Potted Plant", (4, 13), "Planter A", [
        "A potted plant the Committee has been meaning to water since "
        "1987. It is in the minutes."]),
    C("Potted Plant", (16, 13), "Planter A", [
        "Another plant. This one is made of wax, and is doing very much "
        "better."]),
]

# ----------------------------------------------- Map 4, the Gilded Turnip --
PIANO = [
    "An upright piano, with a sign on the lid: PLEASE DO NOT PLAY THE "
    "PIANO. Under it, smaller: THIS MEANS YOU, BRAM.",
    "You lift the lid anyway, and play the one tune you know - 'Turnips "
    "in the Morning' - with one finger.",
    "The whole inn goes quiet. Then it goes back to being loud, slightly "
    "faster than before."]

TURNIP = [
    C("The Piano", [(4, 4), (3, 4), (5, 4)], ("Piano", "Stool A"), PIANO,
      party=[
          (db.PIPER, [("Piper", "Shove up."),
                      "Piper sits down and plays something so lovely "
                      "that the Regular puts his drink down and looks at "
                      "the wall for a while.",
                      "Then she plays 'Turnips in the Morning', properly, "
                      "and it turns out it was a good tune all along."]),
          (db.HOB, ["Hob has a go. He plays the piano the way he shoes a "
                    "horse: hard, in time, and quite sure it will thank "
                    "him later.", "Two keys come off. He puts them back "
                    "on better than they were."]),
          (db.ALDRIC, [("Aldric", "Allow me. I had lessons, as a boy, "
                        "at Pemberton Hall."),
                       "Sir Aldric plays a stirring march. Halfway "
                       "through, it turns into a different stirring "
                       "march, and then back. He looks very pleased."]),
          (db.ZEPH, [("Zephyrine", "I can play. Middle C is a bit "
                      "warm. That's me, I'm afraid."),
                     "She plays a scale. The piano smells faintly of "
                     "toast for the rest of the evening."])],
      then=[["You play a few notes in the order a secret door would "
             "want, in a book. No secret door opens.",
             "The Regular claps, slowly, for exactly as long as it is "
             "funny."]],
      again=["The piano. PLEASE DO NOT PLAY THE PIANO. You have been "
             "told twice now, once in writing."],
      trope="piano"),
    C("Turnip Shelf", (7, 4), "Sundries Shelf A", [
        "The inn's shelves: sacks and boxes of turnip, labelled by year like "
        "wine.",
        "The '87 is said to be very good. The '91 is not spoken of."]),
    C("Mug Shelf", (8, 4), "Sundries Shelf B", [
        "Jars and bottles, each with a name painted on it: REGULAR, REGULAR, "
        "REGULAR, REGULAR.",
        "And one at the end: PIPER (NOT ON THE TABLE)."]),
    C("Inn Window", (6, 3), "Large Window B", [
        "A window onto the square. From here you can see the well, the "
        "Hall, and Sir Aldric, walking very purposefully south."]),
    C("Bedside Table", (13, 4), "Table F", [
        "A card on the bedside table: PLEASE LEAVE THE ROOM AS YOU "
        "WOULD WISH TO FIND IT.",
        "Underneath somebody has written ON FIRE?, and it has been "
        "initialled, Z.V."],
      party=[(db.ZEPH, [("Zephyrine", "It was a question. It was a "
                         "genuine question.")])]),
    C("The Big Bed", [(14, 5)], "Large Bed", [
        "A big bed, made up very tightly. In stories, heroes lie down "
        "on any bed they find, and wake up feeling much better.",
        "Prudence is watching you. You do not lie down."],
      trope="strangers_bed",
      again=["It is twenty crowns. Prudence would like you to know "
             "that it is still twenty crowns."]),
    C("The Register", (8, 6), "Pen A", [
        "The inn's register. The most recent entry: SIR A. "
        "PEMBERTON-GORE. ONE NIGHT.",
        "It is dated six years ago. Every night since then, he has "
        "written DITTO."],
      party=[(db.ALDRIC, [("Aldric", "One keeps records, sir. One "
                           "never knows where the gate will be in the "
                           "morning.")])]),
    C("A Note on the Counter", (9, 6), "Note C (V)", [
        "A note pinned to the counter: NO CREDIT. NO SINGING ON TABLES. "
        "NO CHOSEN ONES ON CREDIT EITHER. THAT MEANS YOU, BRAM."],
      again=["There is a lot in this inn that means you, Bram."]),
    C("A Big Pot", (15, 6), "Pot B", [
        "A big lidded pot, with a label on it that says POT, so that "
        "everybody knows."],
      then=[["You lift the lid. There is another label inside. It says "
             "INSIDE OF POT."]],
      trope="containers"),
    C("Cordial", (4, 7), "Bottle B", [
        "A bottle of Prudence's own cordial: elderflower and turnip.",
        "It is better than it sounds. It would more or less have to "
        "be."]),
]

# --------------------------------------------------- Map 5, the Chapel --
CHAPEL = [
    C("Chapel Glass", (9, 3), "Stained Glass Window", [
        "Stained glass: Saint Ebba of Whatever Works, setting a bone.",
        "The glazier went to a great deal of trouble to get the bone "
        "right. You can tell. You can tell which bone."],
      party=[(db.MERRI, [("Merribell", "Tibia. Clean break. Look at "
                          "that splint - that's how you do it. "
                          "Somebody went to the trouble.")])]),
    C("The Altar", [(9, 5), (8, 5), (10, 5)], "Church Table", [
        "The altar. On it: a candle, a bowl of clean bandages, and a "
        "copy of the Creed with rule three crossed out so hard that the "
        "pen went through."]),
    C("Pew", (6, 7), "Stool C", [
        "A pew, with a brass plate on the end: RESERVED FOR THE TIRED.",
        "Everybody who comes in qualifies. That is rather the point."],
      party=[(db.MERRI, [("Merribell", "Sit. You're tired. I can see "
                          "it from here. It's in your ankles.")])]),
    C("Potted Plant", (4, 12), "Potted Plant A", [
        "A potted plant, very green and very well. The Order waters it "
        "the way it waters everyone: firmly, and whether it likes it or "
        "not."]),
    C("Potted Plant", (15, 12), "Potted Plant A", [
        "Another plant. It has a little bandage tied round one stem, "
        "neatly, with a bow.",
        "It is doing much better, thank you."]),
]

# --------------------------------------------------- Map 6, the smithy --
SMITHY = [
    C("Spears", (8, 4), "Repository of Spears", [
        "A rack of spears. Shiny. That one is shiny. So is that one.",
        "This one is a broom."],
      party=[(db.HOB, [("Hob", "That's for sweeping. You keep it with "
                        "the spears or it gets ideas.")])],
      again=["The spears, and the broom. The broom is the one that "
             "gets used."],
      trope="weapon_wall"),
    C("Swords", (13, 4), "Repository of Swords", [
        "Swords, racked by length. Shiny. Very shiny. Extremely shiny.",
        "And one on the end that is a sword-shaped bit of wood with "
        "SWORD painted on it, for the apprentice to practise with."],
      party=[(db.HOB, [("Hob", "That's not the apprentice's. That's "
                        "mine. Beatrice made me learn on it. You "
                        "don't throw out your first sword.")])],
      again=["The apprentice would like you to know she has not needed "
             "the wooden one for years."]),
    C("Quenching Tub", (12, 4), "Tub A", [
        "The quenching tub. The water still hisses faintly when it is "
        "cold.",
        "A sign: DO NOT DRINK. MERRIBELL HAS BEEN TOLD."],
      party=[(db.MERRI, [("Merribell", "It's quite clean. It's mostly "
                          "iron. Iron is good for you.")])]),
    C("Hammers", (11, 5), "Hammers", [
        "Hammers, hung up by size. Not one of them has a name scratched "
        "on it.",
        "Only one hammer in here has a name."]),
    C("Horseshoes", [(4, 9), (5, 9)], "Crate A", [
        "A crate of horseshoes sorted into LEFT and RIGHT.",
        "Horseshoes do not have a left and a right. Hob sorts them "
        "anyway, for the horses' sake."],
      trope="containers"),
    C("Water Barrel", [(12, 9), (13, 9)], "Barrel", [
        "A barrel of water for the forge, with a ladle. You have a "
        "drink. It tastes of iron and effort."]),
    C("Shield", (4, 3), "Shield", [
        "A shield on the wall, polished until you can see yourself in "
        "it. You look slightly heroic, and very slightly bent."]),
    C("Shield", (6, 3), "Shield", [
        "Another shield. This one has a dent in the middle, and a label: "
        "THE DENT IS STRUCTURAL. DO NOT ASK FOR ONE WITHOUT."]),
    C("Armour Stand", (4, 5), "Armor B (Stand)", [
        "A suit of armour on a stand. In stories, it comes to life the "
        "moment your back is turned.",
        "You turn your back on it. It does not. You feel faintly let "
        "down, and very slightly relieved."],
      trope="suit_of_armour"),
    C("Armour Stand", (6, 5), "Armor B (Stand)", [
        "More armour. A label says MADE TO MEASURE.",
        "It has been made, measuring by eye, for somebody about the "
        "size of a wardrobe."],
      party=[(db.HOB, [("Hob", "That's mine. For best.")])]),
]

# ------------------------------------------------- Map 7, the Emporium --
EMPORIUM = [
    C("Bread", [(5, 4), (4, 4), (6, 4)], "Bread Shelf", [
        "Loaves, each with a label saying where it was ACQUIRED. Most "
        "of them say A BAKERY.",
        "One says THE BAKERY, and has been corrected to A BAKERY."]),
    C("Odds and Ends", (7, 4), "Sundries Shelf A", [
        "Odds and ends: one glove, a teapot lid, a key to something, "
        "and a jar marked MISC (DO NOT ASK)."],
      trope="containers"),
    C("Returns", (10, 4), "Sundries Shelf A", [
        "A shelf of things that were returned, each with a tag: "
        "RETURNED TO OWNER. RETURNED TO OWNER.",
        "And one, very small: RETURNED TO OWNER, WHO WAS VERY "
        "UNDERSTANDING ABOUT IT."]),
    C("A Purple Potion", (6, 6), "Potion B", [
        "A purple potion. Label: NOT POISON.",
        "Small print: THIS LABEL IS PROVIDED FOR REASSURANCE ONLY."]),
    C("A Blue Potion", (9, 6), "Potion A", [
        "A blue potion. Label: MANA. Blue is always mana. Everybody "
        "knows that, and nobody knows how.",
        "Small print: OR IT IS BLUE WATER. ONE OF THOSE."],
      trope="potion_colours"),
    C("A Green Potion", (12, 6), "Potion C", [
        "A green potion. Label: ANTIDOTE.",
        "Small print: TO WHAT IS NOT STATED. WE ARE NOT IN A POSITION "
        "TO SAY."]),
    C("Apples", (4, 6), "Basket C", [
        "A basket of green apples, and a card: ONE PER CUSTOMER.",
        "Under that, in a different hand: PER VISIT. Under that: PER "
        "HAND. Somebody has been arguing with the card."]),
    C("Basin", (13, 6), "Basin", [
        "A basin of water so customers can wash their hands, in case "
        "they have touched anything they are not going to buy."]),
    C("Basin", (13, 8), "Basin", [
        "Another basin, for customers who have touched something they "
        "are not going to buy and feel bad about it."]),
    C("Crate", [(4, 9), (5, 9)], "Crate B", [
        "A crate stencilled PROPERTY OF THE ROYAL MAIL. That has been "
        "painted over: PROPERTY OF THE EMPORIUM.",
        "That has been painted over too, and now it just says "
        "PROPERTY."],
      party=[(db.NIX, [("Nix", "It's honest. You can't say it isn't "
                        "honest.")])]),
    C("Crate", (12, 9), "Crate B", [
        "A crate with holes in the lid, and a label: LIVE.",
        "You look in. It is a crate of houseplants. They are, "
        "technically, alive."]),
]

ALL = {1: THISTLEWICK, 2: HOME, 3: HALL, 4: TURNIP, 5: CHAPEL, 6: SMITHY,
       7: EMPORIUM}
