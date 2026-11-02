# Curios - things to look at

**Mike, 31 Oct 2026, before the quest log (G0):**

> Add a lot more to explore around the world in what we already have, by
> making many of the things around the maps into events which you can look at
> and sometimes interact with (similar to what we did in the summit of the
> Obligatory Tower). As you go about towns and see things which are decorating
> the maps and buildings which stand out, you can look at them and get humorous
> dialog.

His examples:
* bookshelves, with lots of book titles to find;
* shelves and cabinets, remembering that it is rude to root through other
  people's homes, especially when they are standing right there;
* crates and barrels;
* weapons and armour on display ("shiny... so is that one... but wait, this one is...");
* pianos (is Bram any good? maybe somebody in his party is better);
* shops' wares;
* signs, especially outside buildings.

He also set some limits:
* Everything must be accessible. A few things the innkeeper stands in front of
  are fine.
* There should always be a lot to explore.
* Everything should be funny and full of the tropes and clichés.
* Not too creepy; that is not the tone of this game.

This file is the plan and the live status. It goes in the order G0 waits on.
Read section 2 before writing a line. Read `NORTH.md` section 1, the humour
doctrine, too: it binds every line here, including 1.6's out-of-bounds list
and Mike's three October rules.

---

## 1. What already exists (so nothing is doubled)

* `story.prop` gives a searchable object with a sprite. `story.sign` gives
  one without a sprite, where the scenery tile is the picture. There are 17
  `prop` calls and 47 `sign` calls across the builders.
* `postgame.summit_props` / `_look` is the model Mike pointed at. One event per
  cell of the object, with no sprite (`R.image("")`), priority 1, through,
  direction fix. The tile does the blocking and the event does the answering.
* `story.pin_note` and `mapkit.E_NOTE` are Mike's note-image idiom: a `Note A (V)`
  card as the event's picture, for a thing that has no tile of its own.
* `build/curio_survey.py` is section 3's survey. Run it again before each
  wave, because the maps move.

## 2. House rules for curios

1. **Additive only.** A curio never goes on a cell that already has an event,
   and never changes an existing event. If an existing event is already the
   object (the Chapel's organ, the Turnip's washstand), the object is done.
2. **No sprite, on the tile itself, one event per answering cell.** Use the
   `_look` shape. A thing on a wall answers from the furniture cell beneath it
   (root `CLAUDE.md`: the furniture blocks the tile you would stand on). A
   counter reaches over, which is how shop wares behind a counter work.
3. **Asserted against the tile.** Each curio names the tile record it expects
   (its `.txt` name). The build refuses if the cell no longer shows it, the way
   `light_fires` refuses a hearth that has moved. Mike edits maps in the
   editor, and a curio left behind on a bare floor is the bug this prevents.
4. **Reachable.** The build checks that a walkable cell, or a counter, sits
   beside at least one cell of every curio. The flood ignores NPCs. The
   survey's NPC-blocked flag is for choosing what to write; per Mike, a thing
   behind the innkeeper is fine.
5. **Ids are 401 and up on every map**, appended in list order, with the gap
   before them padded with `null`. Nothing a builder adds later can then move
   them, and a curio's self switches survive saves. Never reorder a map's
   list; only append to it. Record the range in `CLAUDE.md`'s Ids table.
6. **How each look plays (as built).** `look` is the first time. `then` is
   a list of further looks, one per press, in order: a bookshelf's other
   titles, or the barrel with a smaller barrel in it. `again` is every look
   after those, for ever; leave it out and the `then` looks go round again.
   The count lives in `$gameSystem._curios["map:event"]`, which is saved with
   the game. No self switches are used, and the twins of a multi-cell object
   share their first cell's key, so the object is looked at once, not once
   per side.
7. **Somebody else's house.** *(Revised by Mike, 31 Oct: Bram does
   sometimes rummage.)* Heroes rummaging through people's homes is the
   trope, so Bram may open the drawer or the wardrobe and get caught. The
   homeowner's sarcastic remark is the joke ("Find anything? The socks
   are in the left one."). Mix three outcomes:
   * he rummages and the owner comments, drily, with a face (`(name,
     text)` windows);
   * he rummages and finds something absurd, or a note left for heroes;
   * occasionally, he thinks better of it. The C1-C6 drafts use only this
     outcome: Pell's drawers, Quy's wardrobe, the Gotobeds' jewellery
     box, Rosamund's wardrobe, the minions' lockers.

   **A C7 task:** rework some of those restraint curios into
   rummage-and-get-caught, and keep only a few as restraint. Open shelves
   are always fair game. All of them count as the `rummage` trope.
8. **The party joins in, sometimes.**
   * Some curios add a line when a particular companion is in the party,
     using `R.condition_actor_in_party` (the `story.specimen` shape). A party
     without them loses nothing and is told nothing.
   * The piano is the set piece. Bram plays, badly. Piper plays properly. Hob
     plays it like an anvil. Merribell knows one hymn. Zephyrine sets fire to
     middle C. Write each one into each piano's text; vary the instruments.
   * Voices are per `COMPANIONS.md` and `BIOS.md`. Read a companion's section
     before writing them.
   * Spare is nine years old, and his lines follow `NORTH.md` 1.6.
9. **Tropes.**
   * Each *kind* of cliché counts once in the whole game, not once per
     barrel. A trope bump sits behind
     `!$gameSelfSwitches.value([0, 0, 'T:kind:<name>'])` and sets the key
     after bumping. The key holds `'T:'`, so `build_game.once_tropes` already
     reads it as guarded.
   * There are about 25-30 kinds, listed in section 4 as they are written.
   * A completionist can reach about 92 now. The ending's top tier is 60
     (`journey.py` around line 1237, two-thirds of about 92). These kinds push
     the total towards 120.
   * **Ask Mike** whether to re-cut the tier to about 80, keeping two thirds,
     or to leave it at 60. Until he answers, leave it at 60.
   * **Answered 31 Oct: raise it.** The top tier is **90**, two thirds of
     the reachable total of about 140; twenty stays.
10. **No blushes.** `VAR_BLUSHES` is Mike's audited count, and curios add
    none. A curio can still be gently Register A if it passes all four tone
    tests in 1.5, but it is not counted.
11. **A little loot, and rarely.** The barrel-with-a-potion-in-it is the
    oldest trope there is, so a few curios give something once, and the
    second page is empty.
    * At most about one per town: a single herb, a few gold, or a joke item
      that does nothing.
    * Never anything that moves `balance.py`.
    * Gladhollow's barrels are Toby's granny's and she wants her potions back
      (`BIOS.md`). Check what `gladhollow.py` already does with that before
      building on it.
12. **Not creepy.**
    * Bones, coffins and crypts are played for admin and anticlimax, never
      dread. The plaster skeletons at the summit are the register.
    * Sad is allowed where it is earned (Ysolde, Ambrose). Horror is not.
13. **Text discipline.**
    * Messages are four lines: 47 characters with a face, 60 without.
      `S.say` and `S.narrate` refuse anything longer.
    * Run `python3 build/audit_text.py` and `validate.py` after each wave.
    * Never reuse a joke. The book titles in particular go in section 5 as
      they are used, and each title is used once in the game.

## 3. The survey (31 Oct 2026)

`python3 build/curio_survey.py` gives one line per map.
`python3 build/curio_survey.py --map N` lists every object on map N. It groups
same-named, adjacent B-E/A5 cells into objects, skips walls and floors, marks
any that already have an event on them, and floods reachability from every
transfer and the start (stationary NPCs block).

Free, reachable objects by map: about 1,700 in total, but most outdoor ones
are trees, boulders and rubble.

| map | free | | map | free | | map | free |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 Thistlewick | 46 | | 26 Long Field | 181 | | 51 Sump | 9 |
| 2 Bram's House | 6 | | 27 Wreck | 28 | | 52 Ashcombe | 24 |
| 3 Prophecy Hall | 13 | | 28 Firstfield | 8 | | 53 Ashcombe Indoors | 21 |
| 4 Gilded Turnip | 11 | | 29 Penultima | 15 | | 54 Weeping Bottom | 20 |
| 5 Chapel | 3 | | 30 Ye Final Shoppe | 16 | | 55 Sisterhouse | 24 |
| 6 Smithy | 10 | | 31 Restwell | 18 | | 56 Fenmarch Hall | 8 |
| 7 Nix's Emporium | 11 | | 32 Eight Hours | 20 | | 57 Long Gallery | 4 |
| 9 Gloamwood | 33 | | 33 Hithermost | 31 | | 58 Great Court | 20 |
| 10 The Bit With The Thing | 21 | | 34 Chapel of Continuance | 6 | | 59 Library | 6 |
| 11 Obligatory Tower | 174 | | 35 Fairholme | 12 | | 60 The Hall | 4 |
| 12 Summit | 10 | | 36 Rosamund's Tower | 5 | | 61 Great Dunnage | 8 |
| 13 Nether Sopping | 91 | | 37 Emberthwaite's Lair | 11 | | 62 Smiths' Hall | 9 |
| 14 Slain Wyvern | 47 | | 38 Olde Evermore | 13 | | 63 Counting House | 1 |
| 15 Adventurers' Guild | 9 | | 39 Forbidden Archive | 13 | | 64 Bonded Warehouse | 26 |
| 16 Wick & Barrow | 10 | | 40 Gladhollow | 5 | | 65 The Bell | 7 |
| 17 Forty-Five's | 9 | | 41 Mayor's House | 5 | | 66 Old Ashcombe | 31 |
| 18 Lighthouse | 59 | | 42 Former Premises | 8 | | 67 Under Carn Drey | 6 |
| 19 Bottomless Pit | 8 | | 43 Frayne's | 9 | | 68 Much Pottering | 25 |
| 20 Barrow | 9 | | 44 Frostwick | 30 | | 69 Gotobeds' | 18 |
| 21 Upper Clanging | 83 | | 45 Eleven Days | 19 | | 70 Bottom Lock | 0 |
| 22 Hoyle Works | 26 | | 46 Working Group | 8 | | 71 Fitch's | 1 |
| 23 Safety Valve | 24 | | 47 Cold Room | 6 | | 72 Wyvern Upstairs | 28 |
| 24 Ollerenshaw's | 17 | | 48 Chapter House | 4 | | 73-78 the Stair | 27 |
| 25 Parish Rooms | 10 | | 49 Sable Hart | 7 | | 8 world map | (sites, not curios) |

Most common free objects across the game:

| object | count |
| --- | --- |
| Window A | 80 |
| Barrel | 75 |
| Scrap Metal | 62 |
| Crate (all kinds) | about 100 |
| Bed | 35 |
| Potted Plant | 32 |
| Large Window | 31 |
| Tapestry | 28 |
| Tombstone (Plaque) | 15 |
| Sundries Shelf | 20 |
| Basin | 13 |
| Bookshelf A/B | 21 |
| Armor (Stand) | 14 |
| Chest of Drawers | 13 |
| Clock | 9 |
| Sign B | 9 |
| Shop Sign (all kinds) | about 25 |
| Wine Rack | 5 |
| Swords, shields, spears and axes on racks | about 15 |
| Piano | 2 |
| Globe | 4 |
| Crystal Ball | 1 |
| World Map | 2 |
| Wells | 10 |
| Graves | 5 |
| Scarecrows | 2 |

### What gets a curio

| always | most | some (one or two per map, chosen for the joke) | never |
| --- | --- | --- | --- |
| every bookshelf | barrels | windows (the view: say what is outside, specific to the place) | trees, boulders and rubble, unless one is a landmark |
| every shop's wares | crates | beds (the strangers'-beds trope, once a town) | floor tiles |
| every weapon or armour display | wardrobes and drawers (rule 7) | potted plants | chimneys |
| every piano or organ | tables with something on them | tapestries | fences |
| every sign without an event | wells | | |
| every grave or tombstone | clocks | | |
| statues | mirrors | | |
| globes, maps, crystal balls | | | |

**Target:**
* about 8-15 per interior and 10-25 per town;
* fewer in the dungeons and the Stair, where a curio is a reward rather
  than furniture;
* about 600-700 in all.

## 4. Trope kinds (rule 9) - claimed as written

**In use (C1):**
* `containers` (barrels, crates, a shelf of MISC);
* `grave_puns`;
* `sword_in_stone`;
* `bookshelf`;
* `lore`;
* `mural` (stained glass that tells the backstory);
* `piano`;
* `strangers_bed`;
* `weapon_wall`;
* `suit_of_armour`;
* `potion_colours`.

**In use (C2):**
* `dash` (Sopping's speed limit);
* `well` (the crab);
* `world_map` (HERE BE ONE DRAGON, RETIRED);
* `rat_cellar` (the Guild's untaken quests);
* `ten_foot_pole`;
* `wardrobe` (Quy's);
* `cheap_inn` (bedding that never heals);
* `message_bottle`;
* `beanstalk`;
* `hollow_log` (SEARCHED);
* `fairy_ring`.

**In use (C3):**
* `cobweb`;
* `pots` (I WOULDN'T EITHER - G.);
* `captured` (the cell nobody was ever put in);
* `coffin`;
* `scrap_heap`.

**In use (C4):**
* `tutorial`;
* `last_shop` (forty LAST POTIONs);
* `respawn` (the saint coming out of the chapel porch);
* `key_under_pot` (STILL NO);
* `half_the_kingdom`;
* `damsel` (RESCUED AGAIN, Vol. Eleven);
* `dragon_hoard` (the doily);
* `forbidden_book` (biscuit recipes);
* `crystal_ball`.

**In use (C7, at Mike's suggestion):**
* `retired_hero` (Mr Gotobed's swords: he came to rescue a lady, knocked
  on the wrong door, and it was Mrs Gotobed's).

**Candidates still unclaimed:** the rest of this table.

| key | the cliché |
| --- | --- |
| `barrel` | heroes search every barrel |
| `pots` | ... and break the pots |
| `bookshelf` | every bookshelf holds exactly one relevant book |
| `lore` | a book that is the exposition |
| `rummage` | heroes walk into houses and take things (Bram declines) |
| `strangers_bed` | sleeping in any bed you find |
| `well` | the well holds a secret |
| `piano` | the puzzle piano |
| `weapon_wall` | the weapon on display that is the legendary one |
| `suit_of_armour` | the empty armour that moves |
| `portrait_eyes` | the portrait whose eyes follow you |
| `wardrobe` | a wardrobe that is a door to somewhere |
| `false_wall` | the suspicious wall |
| `locked_chest` | the chest that needs the key from three towns away |
| `notice_board` | the quest board |
| `shop_sign` | the shop that sells only exactly what you need |
| `cheap_inn` | the inn that heals you overnight for five gold |
| `grave_puns` | jokes on gravestones |
| `crystal_ball` | the fortune teller's vagueness |
| `world_map_x` | X marks the spot |
| `mysterious_crate` | an unlabelled crate the plot will need later |
| `scrap_heap` | the junk heap that has a part in it |
| `talking_statue` | the statue with a riddle |
| `clock` | the clock puzzle |
| `diary` | the convenient diary |
| `kitchen` | food that heals more than potions |
| `scarecrow` | the scarecrow that is obviously a monster |
| `mirror` | the reflection that does not match |

## 5. Registry of used jokes

Add every book title, epitaph, shop sign and named object here as it goes in,
so nothing is said twice.

### Book titles
* Prophecy Hall (Map 3): THE MEETING TO DECIDE WHEN TO HOLD THE MEETING
  Vol. IV; PROPHECY - A USER'S GUIDE; THE FORTY-SEVEN: A SOUVENIR;
  STANDING ORDERS OF THE PROPHECY COMMITTEE, Revised; a dictionary that
  falls open at SLAIN and DEFEATED; THE PROPHECY OF THISTLEWICK
  (ABRIDGED); SO YOU'VE BEEN CHOSEN: A LEAFLET; the Prophecy Fund's
  accounts; WHAT TO DO IF THE CHOSEN ONE IS NOT IN.
* The Hall's struck archive: STRUCK: A HISTORY Vol. One (struck); VERSES
  STRUCK FROM THE BALLAD by decade; THE PROPHECY: EARLY DRAFTS (OR SO);
  NAMES CONSIDERED FOR THE OBLIGATORY TOWER; MISC (STRUCK); THINGS NOT TO
  READ ALOUD AT THE FETE.
* Bram's house: The Turnip Grower's Almanac (1997).

* The south (C2):
  * the Wyvern's guests' books:
    * ESCAPING FROM DUNGEONS FOR BEGINNERS;
    * Hosea's HISTORY Vol. One (a pamphlet);
    * WYVERNS OF THE COAST (with a goose);
    * THE CHOSEN ONE'S COOKBOOK;
    * THE KNIGHT WHO CAME HOME;
    * A HUNDRED THINGS TO DO IN NETHER SOPPING.
  * The Healers' Table's books: FIELD MEDICINE FOR THE CHOSEN; WHAT THE
    BARD MEANT BY 'FLESH WOUND'; STITCHES I HAVE PUT IN HEROES, AND WHERE.
  * The lighthouse:
    * THE KEEPER'S HANDBOOK (no rule two);
    * LIGHTHOUSES I HAVE KNOWN;
    * KNITTING FOR KEEPERS;
    * the gull book;
    * THE TIDES, AND WHY;
    * keepers' ghost stories;
    * SHIPS OF THE COAST.

* The Tower's private library:
  * VILLAINY FOR BEGINNERS;
  * THE MONOLOGUE: A HANDBOOK ('Don't');
  * THE PROPHECY ANNOTATED (a hole at clause twelve);
  * A THOUSAND AND ONE THINGS TO DO WITH A TOWER (+ LEAVE IT);
  * READING A RENEWAL CLAUSE (falls open at 'notice');
  * BUNGALOWS OF THE COAST;
  * TEA: A HISTORY, vols 1-9;
  * KNITTING FOR THE DARK HOURS (AUNT M - TOO LONG?).
  These point at the ending and never say it.
* The Safety Valve: BOILERS, AND HOW TO TALK TO THEM; A HISTORY OF THE
  HOYLE WORKS in 199 chapters; SIXTY-THREE THINGS: A COMMENTARY; THE
  HOOTER.

* The sites (C4):
  * Ye Final Shoppe: HOW TO HAGGLE (not for sale); THE MARKUP ACCOUNTS
    (DISCOUNT - ELEVEN COPPERS - WORTH IT); PRICING FOR BEGINNERS.
  * The Lair: CARD GAMES FOR TWO (AND ON THURSDAYS, THREE); HOARDING: A
    SENSIBLE APPROACH; LETTERS FROM KNIGHTS.
  * The Forbidden Archive:
    * the FORBIDDEN biscuit book;
    * THE CHRONICLE OF THE SECOND AGE (BORING. TRUE.);
    * the horse picture book THE VILLAIN;
    * THINGS GRANDMOTHER FORESAW (to her slipper);
    * PROPHECIES (DISCARDED) with jam;
    * sixty volumes of poetry;
    * the overdue books with the Second Age date.
  * The Mayor's: council minutes (T. WENDLE, AGED SEVEN, abstaining);
    CIVIC DUTY, CIVIC PRIDE, CIVIC HATS.
  * The Cold Room: CONTRACT boxes (and COMPLIMENTS); MAINTAINING A WINTER.

### Epitaphs
* Thistlewick (Map 1):
  * OSWIN FARROW - HE SAID IT WAS PROBABLY FINE;
  * ELSPETH MOORE, forty-one turnip shows, the forty-second fixed;
  * COUNCILLOR (THE FIRST), A GOAT, never spoke out of turn;
  * WALTER PIKE - HE KNEW A SHORTCUT;
  * MABEL THISTLE, the turnip that became the chair.

### Other
* Thistlewick:
  * the crest NON NOBIS, NISI FORTE;
  * the forty-seven clay figures;
  * THIS WAY UP pointing at the ground;
  * the barrel inside a barrel;
  * the market's FRESH potatoes, MOSTLY tomatoes, carrots with no card, and
    the fish CAUGHT LOCALLY;
  * the turnip kept back for the Chosen One's supper;
  * the sword-in-stone turnip sign;
  * EVERYTHING MUST GO (BACK);
  * WE BUY ANYTHING / PLEASE ASK SOMETHING;
  * EST. RECENTLY;
  * the creaking tankard that taught the song;
  * the five chalk stars;
  * 'Bram' rhymed with 'jam';
  * "it is not Beatrice";
  * the nose-sized clean circle on the smithy window.
* Home: WEAR THE VEST; the turnip cut into a sword; turnip on the chin; the
  CHOSEN ONE paper crown, aged six.
* The Hall: the man paid to look busy; the Dark Lord waiting for a bus;
  pillar minute 4,410; BUY MORE SCROLL; red tape by the mile; the Optional
  Tower petition; the plant since 1987, and the wax one.
* The Turnip: the piano (PLEASE DO NOT PLAY, THIS MEANS YOU, BRAM;
  'Turnips in the Morning'); pickled turnip by vintage; the REGULAR
  tankards; Aldric walking south; ON FIRE? Z.V.; the bed and the trope;
  Aldric's register DITTO; the POT that says INSIDE OF POT; elderflower and turnip cordial.
* The Chapel: Saint Ebba's tibia; rule three crossed out through the
  paper; the pew RESERVED FOR THE TIRED; the plant with a bandage.
* The smithy: the spear rack with a broom; the wooden SWORD; DO NOT DRINK,
  MERRIBELL HAS BEEN TOLD; only one hammer has a name; horseshoes sorted
  LEFT and RIGHT; the armour that does not come to life; THE DENT IS
  STRUCTURAL.
* The Emporium:
  * bread from A BAKERY;
  * MISC (DO NOT ASK);
  * RETURNED TO OWNER, WHO WAS VERY UNDERSTANDING;
  * the purple NOT POISON, blue MANA and green ANTIDOTE potions' small
    print;
  * the apples ONE PER CUSTOMER, PER VISIT, PER HAND;
  * the two basins;
  * PROPERTY;
  * the crate of LIVE houseplants.
* The south (C2):
  * The Wyvern:
    * the piano's pencilled names, Middle C eleven, SOPS;
    * the clock at ten to twelve;
    * NO DRAGONS IN THE BAR, EVEN IF IT IS A GOOSE;
    * bottles with names not to serve;
    * BAKED SOME MORNING;
    * the ship in a bottle in a ship;
    * the SAVED tankard;
    * HEROES WILL WAIT THEIR TURN;
    * the bucket FOR THE GOOSE;
    * Hosea's chapter 312 ("stands about") and 311 ("Lunch");
    * Hulda's three BEAR columns;
    * Ysolde's FOR AFTER;
    * the long table of eleven endings;
    * Perpetua's crown napkins;
    * the crested wine TO WHOM IT MAY CONCERN;
    * beans and pheasant, FARM WINE, PEASANT LUGGAGE;
    * fish is not searched;
    * the brick on the lid;
    * the Healers' Table (BANDAGES ALSO ROPE..., the globe of crosses, tea
      strong enough to set a bone, HOBDAY with no lute, boiled by Grizel,
      the splinted plant, the plant nobody trusts).
  * Upstairs: A CHOSEN ONE SLEPT HERE; the armour-shaped dip; Sops's
    dandelions; fishy fresh water; the LOST PROPERTY castle keys; the
    bedding; the tired mirror; no chime between three and four; STOOLS
    STOOD ON BY BARDS - 41.
  * Nether Sopping:
    * IN BLOOM (DAMP CATEGORY);
    * SPEED LIMIT A BRISK WALK;
    * ALSO THE ROAD BACK;
    * the painted-on rain;
    * ONE WYVERN (SLAIN) (GOOSE);
    * PROVISIONALLY;
    * the TIDES board;
    * DRAGONS QUOTED FOR;
    * A HERO RUNS ON TEA AND BOOTS;
    * the WALKED NORTH AND BACK boots;
    * YOU WILL NEED A BIGGER RUCKSACK;
    * the goose bite in the sign;
    * ROOMS 25 over 20 over 15;
    * the six bolts;
    * the provisional question mark;
    * the empty Guild window;
    * SEA POTATOES and SEA CARROTS, and FISH;
    * RETURN TO SENDER;
    * the rain barrel;
    * salt for sea monsters;
    * the crab in the well;
    * the sea-water well;
    * eels by the yard;
    * the octopus with the pencil;
    * the net also spoken for;
    * K + M WED 1972 STILL;
    * the gull;
    * the bollards (AND FOR GRANDAD).
  * The Guild:
    * HERE BE ONE DRAGON, RETIRED;
    * drawers IN/OUT/PENDING/PROVISIONAL;
    * petunias, provisionally;
    * FORM 7A/7B;
    * provisional members;
    * the cat that came down;
    * the letter for the next town;
    * closed Tuesday for the review;
    * practice swords never used;
    * RETURNED: PENDING.
  * Wick & Barrow:
    * HARDEST TACK;
    * chalk, FINDING YOUR WAY OUT NOT INCLUDED;
    * the dummy, which Chosen One not specified;
    * ten-foot poles;
    * the optimistic deckchair;
    * DRAGON REPELLENT (lamp oil, throw hard);
    * boot polish;
    * boots by how far north;
    * compasses that point at the Turnip.
  * Quy's: SEEDS (NOT TURNIPS); supper for one; the green water butt; the
    wardrobe and the throat-clearing; the rose catalogue; the tea under a
    saucer; the rose out of season.
  * The lighthouse:
    * the hollow oil barrels;
    * Saint Bother's three tapestries;
    * the bottled ships and then one lit lighthouse a year;
    * plates for thirty;
    * the vinegar;
    * the chained ladle;
    * the message in a bottle in the lighthouse;
    * the wick jar;
    * the lens crates;
    * the 1908 biscuit;
    * sand for the lamp's ideas;
    * the mouse in the flour;
    * the jumpers;
    * the clock;
    * the nightcap;
    * supper and the ship that waved;
    * the crossroads window;
    * EMERGENCIES ONLY biscuits;
    * the unnameable pickle;
    * salt;
    * the coast chart green and red;
    * the old logs (GOT HER IN);
    * the LIGHT LIT nib;
    * the sky almanacs.
  * The Gloamwood:
    * GIANT NOT IN, THIS MEANS YOU JACK;
    * Wren's delicious row;
    * the gnome's dent;
    * the SEARCHED log;
    * two dead beanstalks;
    * the troll boulder;
    * RESERVED - NUMBER FORTY-SIX;
    * ARE YOU SURE?;
    * the painted mushroom door;
    * OTHER WAY.
  * The Bit With The Thing: the roped fairy ring; MUSHROOM 14 OF 31; the
    back-scratching beanstalk; the old, happy sheep; the Society's picnic
    log; the mushroom called Norman (Wren says Cyril).
  * The Pit: the pickaxe that found the bottom; one sock. The Barrow: the
    hound's leaning place.
* The Tower (C3):
  * the view of more tower;
  * the dust smiley;
  * WORK IN PROGRESS;
  * the night porter's cocoa;
  * the unplayed good hand;
  * the cushioned skeleton (and blanket);
  * I WOULDN'T EITHER - G.;
  * GLOOM;
  * the last torch;
  * ROCKS (SPARE);
  * DUNGEON THIS WAY into the crate;
  * the dragon's DO NOT TOUCH;
  * a tower rampant;
  * DO NOT LET THE CHOSEN ONE SET FIRE TO IT (AGAIN);
  * the darned banner;
  * seven worried reflections;
  * THIS COBWEB IS LISTED;
  * PROPERTY OF THE TOWER;
  * FOR CUTTING CAKE;
  * the mop among the spears;
  * the eye with eyelashes;
  * the step for the short armour;
  * GONE FOR TEA;
  * three cells (never captured, the calendar, the flowers in case);
  * PRACTISE LOOKING MENACING / I AM TRYING;
  * SKELETON, THIRD CLASS;
  * the horned teddy;
  * the day shift asleep;
  * GRUB, SNAG, GRUB (THE OTHER ONE);
  * sick leave;
  * GRUEL;
  * ONE SQUEEZE EACH, SNAG;
  * CLEAR YOUR OWN BONES;
  * twenty past three;
  * HEROIC POSE NO. 3;
  * the bell on the gargoyle;
  * the ordinary-sinister clock;
  * the pink-tinged cloak;
  * five coffins (RESERVED, the fern, DRY STORE, lavender, OUT OF ORDER);
  * ABANDON HOPE (BUT DO WIPE YOUR FEET);
  * NOBODY HOME;
  * the mural PLEASE WASH YOUR CUP;
  * THE PREVIOUS MANAGEMENT REGRETS;
  * tea tins in the wine rack;
  * the globe pin ONE DAY;
  * WHAT TO SAY WHEN THEY ARRIVE ('Tea?');
  * DECORATIVE - THE DOOR IS THE DANGEROUS PART.
* Upper Clanging:
  * rivets handled with care;
  * grey rain;
  * hymn books that clank;
  * the gutter of buckets;
  * NOT FOR CAKE;
  * grey geraniums;
  * ornaments facing the works;
  * the cat and the vent;
  * the works needs no sign;
  * HOT. LOUD. EARLY.;
  * NO WIZARDS WITHIN TEN YARDS;
  * SORT OF;
  * NOT A WASHER;
  * boiler No. 147 ALMOST;
  * TEA (DO NOT);
  * SHIM - NOT ALL OF THEM;
  * IN THE EVENT OF PRESSURE, GO TO BED;
  * the welcome steam;
  * BEST IN THE NORTH / SAYS WHO;
  * the rivet-perfect breastplate;
  * the pillar box with a step;
  * FOR SOWERBY;
  * IN MEMORY OF THE QUIET;
  * parish Saturdays;
  * nine vests and a labelled peg;
  * WHOSE TURN FOR THE BATH (SPARE (TRY));
  * nine cups and a nail.
* The Hoyle Works:
  * SAFETY FIRST... LIFT ALWAYS / SEE OTT;
  * THE HOOTER IS NOT A SUGGESTION;
  * Ott's camp bed crease;
  * NIB'S rivets;
  * CONTENTS UNDER PRESSURE;
  * ALWAYS IN THE RED;
  * locker 40 EAT YOUR CRUSTS;
  * LIFT, DRAG, WEIGHT, NERVE and the birds;
  * NOT A KIT, A PROBLEM;
  * SPARE PARTS 1-199;
  * the careful scrap;
  * castings four minutes early.
* The Safety Valve: the china FOR WHEN SHE FLIES; EVERYWHERE ELSE IS LATE;
  the snake plant; IN CASE OF EMERGENCY, LIE DOWN; the boiler tea cosy;
  rivet-hard rolls; hissing sausages; CLASS OF '19 doily; Rivet's plate;
  THE SECRETARY; Kell polishes when worried.
* Ollerenshaw's: I SAID DO NOT - B.O.; BEST SMITH awarded to himself; the
  tub that hisses at 'Thistlewick'; sorted coal; hammers all named BRYD;
  the nail-bending machine; RIVETS (GRUMNIR'S - DO NOT USE).
* The Parish Rooms: the rota of Mrs Tunnicliffe; COTTERILL (CONT.); the
  carriage clock photograph; the added chimney; three urns; the brass pot;
  the hooter minutes; the boy with a packed bag, RETURNED.
* The sites (C4), in brief:
  * Firstfield: the CONTROLS and SAVE boards; BARREL (FOR PRACTICE); the
    log that rests for atmosphere; SHEEP WATER; OBSTACLE (EASY).
  * Penultima:
    * last swords / spoons;
    * the final tea;
    * Gideon polishing harder;
    * CLOSED FOR THE SEASON;
    * the one-gold-cheaper shop;
    * the priced barrel;
    * the two LAST WELLs;
    * the searched barrel as a selling point;
    * the priced teapot;
    * the man counting twice;
    * LAST LOG.
  * Ye Final Shoppe:
    * forty LAST POTIONs;
    * doubled SEASONAL antidotes;
    * FINAL WINE (WE HAVE A CELLAR);
    * rope priced by the inch;
    * WE BUY AT ONE, SELL AT FORTY, the warranty;
    * the two LAST UMBRELLAs;
    * G. WAS HONEST TODAY (?);
    * the ring NOT THAT ONE;
    * BUY ONE GET ONE AT FULL PRICE;
    * THE FIRST GOLD (OFFERS);
    * half a potion.
  * Restwell:
    * THE FOUR HOURS (gone to bed);
    * THE NINE HOURS;
    * THE NIGHTCAP;
    * THE LIE-IN;
    * the clock an hour fast;
    * the spoon sleeper;
    * the loud SILENCE dormitory;
    * pillows by the barrel;
    * nightcaps by inn;
    * the quiet well;
    * FOR WAKING GUESTS / USE NEVER;
    * the sleepers' log.
  * The Eight Hours:
    * jam by the hour;
    * cocoa;
    * honey in woollen hats;
    * BAKED WHENEVER;
    * the bell and the one who turns over;
    * BACK AFTER A NAP;
    * eight-hour candles;
    * knitted egg hats;
    * Dr Pike's cold-tea TONIC;
    * the sleepy lavender pot;
    * curtains at noon;
    * the well-rested plant.
  * Hithermost:
    * the saint out of the porch;
    * the saint signing smaller;
    * KETTLE PERMITTING;
    * the kettle-shaped gap;
    * the borrowed tea;
    * GONE UP every Tuesday;
    * FIRST WATER AFTER (SEE CHAPEL);
    * FOR THE BOOK candles;
    * the hall of pots;
    * STILL NO;
    * the braced family;
    * THE BARREL HAS ALSO BEEN SAVED.
  * The Chapel of Continuance: the saint looking back; the glazed silence;
    CONTINUED; the tea at ten past four, still warm; the leaning plant.
  * Fairholme:
    * eleven fences;
    * the cake-tin figure;
    * the uncut portrait map;
    * Rosamund, six, with a bag;
    * the kingdom in eleven threads (drainage);
    * the 1/2048 deed (a ditch);
    * the barrel teapot;
    * item six's teapot;
    * HALF circled;
    * SHARE ELEVEN pending the eagle.
  * Rosamund's Tower: eleven cloaks and EAGLE; the ladder she won't use;
    the tiaras FOR BALLS and FOR KIDNAPPINGS; RESCUED AGAIN; PLEASE WATER
    IF I AM AWAY.
  * The Lair:
    * the hoard's doily;
    * Thursday stakes;
    * RAINY DAY;
    * two dragons in the sun;
    * scorched cups;
    * the sneezing cuckoo;
    * Rosamund winning;
    * umbrellas for knights;
    * princesses' flowers.
  * Olde Evermore: the carved soap; the untidy spiral; first-name
    mushrooms; the 6.0 window; the one fish; the ladder-shaped space.
  * The Archive: the biscuit glass; the crystal ball with Mirabel waving;
    the first beautiful word; MINE. DO NOT WATER.
  * Gladhollow: FIFTEEN WAYS (fourteen and a question mark); HERO PASSES
    THROUGH; NOTHING HERE cupboards; the WELCOME/FAREWELL log.
  * The Mayor's: the (WELCOME) sun shield; BEST KEPT PLANT, the only
    entrant.
  * The Former Premises: sky and more sky; the ignored cloud; four suits
    of armour (DISPLAY ONLY, FOR THE LOOK, the duster, the one facing the
    door); the plant watered from below.
  * Frayne's: ONE EACH on the bird table; honey FOR VISITORS; the worn
    breadboard; the shirt quilt; the third cup; small firewood.
  * Frostwick:
    * four contracted inches;
    * the lamplighter of seven;
    * slippers toes touching;
    * ASK MRS MARCHPANE;
    * Reginald the icicle;
    * snowflakes checked against the contract;
    * SPARE SNOW;
    * grit not to be used;
    * lanterns in straw;
    * the crossed-out carol verse;
    * the right carrots.
  * The Eleven Days:
    * eleven circled days;
    * hot-water bottles by room;
    * WARM BEFORE SERVING;
    * ring for service or the thaw;
    * FOR THE RIBBON - MR STAGG;
    * the frost face with a scarf;
    * IT IS IN THE CONTRACT;
    * syrup-face porridge;
    * logs for THE TWELFTH.
  * The Working Group:
    * snow timed;
    * THE WINTER (CONT., CONT.);
    * numbered drifts;
    * eleven drafts, Ribbon at noon;
    * no apologies ever;
    * ink on 'winter';
    * BUNTING (CONTESTED).
  * The Cold Room: frost on the inside; COMPLIMENTS; ICICLES, ASSORTED;
    washing with gloves on.
  * The Chapter House: the motto too long to fit; CEREMONIAL armour; SIZES
    RUN SMALL; PINS REVIEWED (WITH TEA).

## 6. The waves, in the player's order

Each wave works like this:
1. Run the survey and look at the map with `shots.js` on port 8772.
2. Crop anything ambiguous with `propsheet.py`.
3. Write the map's curio list in `build/curios.py`.
4. Build, then run `validate`, `audit_text` and a curio scenario.
5. Mark the wave done here.

| wave | maps | status |
| --- | --- | --- |
| C0 | the mechanism: `build/curios.py` (`curio()`, the cell and tile assertion, ids 401+, shared twins, trope kinds, companion lines), wired into `build_game.main` after `light_fires`; `python3 build/curios.py` checks without writing | **done 31 Oct**: wired into `build_game.main` after `light_fires` and before `once_tropes`; the reach check is per cell (every twin must be answerable, which is `validate.py`'s rule) |
| C1 | Thistlewick: 1-7, `build/curios_c1.py`, scenario `curios_c1` | **drafted 31 Oct**: 113 events, and the dry run passes. **Built 31 Oct.** |
| C2 | the south road and the south: 9, 10, 13-20, and 72, in `build/curios_c2.py` | **drafted 31 Oct**: 9, 10, 13, 14, 15, 16, 17, 18, 19, 20 and 72 all have curios, 168 events, and the dry run passes. The Barrow has only one, out of respect for Ambrose. **Built 31 Oct.** |
| C3 | the tower (11-12, beyond the summit props) and the north (21-27), in `build/curios_c3.py` | **drafted 31 Oct**: 11, 21, 22, 23, 24 and 25 have curios, 138 events, and the dry run passes. **The Long Field (26) and the Wreck (27) are left alone on purpose**: they are the north's two solemn set pieces (the plaques, the empty ship), and a joke on them would cost more than it adds. Map 12, the summit, already has `postgame.summit_props`. **Built 31 Oct.** |
| C4 | the sites: 28-48, in `build/curios_c4.py` | **drafted 31 Oct**: every map from 28 to 48 has curios, 182 events, and the dry run passes. 28-31 were written from tile names and the event text, with no screenshots (see C7). **Built 31 Oct.** |
| C5 | the coast and the east: 49-67, in `build/curios_c5.py` | **drafted 31 Oct**: 49-65, 104 events, and the dry run passes. **Old Ashcombe (66) and Under Carn Drey (67) are left alone on purpose**, because they are Corvin's and Roland's stories. **Built 31 Oct.** |
| C6 | Pottering, the Stair, the rest: 68-78, in `build/curios_c6.py` | **drafted 31 Oct**: 68 and 69, 15 events. **Left alone on purpose:** the Bottom Lock (70); Fitch's cottage (71), which is Ambrose; and the Stair (73-78), which is the post-game, with Dunstable's markers (never settle him). **Built 31 Oct.** |
| C6b | quiet curios for the maps the jokes were kept out of (Mike, 31 Oct): the Long Field (26), the Wreck (27), Old Ashcombe (66), Under Carn Drey (67), Fitch's (71) and the Stair (73-77), in `build/curios_c6b.py` | **drafted 31 Oct**: 27 events, and the dry run passes; **built 31 Oct**. They are observations in each map's own voice, with no jokes: the plaques, the log, the chalk. Dunstable's boulders are in his cheerful hand with no D. numbers, so nothing is settled. The Bottom Lock (70) and the Bottom of the Stair (78) stay bare: 70 by agreement, and 78 has nothing that is not already an event |
| C7 | whole-game pass: re-run the survey, the reachability check, `audit_text`, every curio scenario; **a contact sheet of every curio's tile** (`tools/propsheet.py`, or a crop per curio), checked against what its text says the thing is - C4's maps 28-31 were written from the tile names without screenshots; Mike's trope tier answer | **in progress 31 Oct**: contact sheet done, rummage rework done, TIMELINE rows done, `curios_rummage` written; trope tier answered (90); Mr Gotobed's swords and map added |

**Done notes go here, one paragraph per wave.**

### Where things stand (31 Oct, after the build)

**Built.** The trope fix went in on its own as db7f7e3. Then the curios
were built: 753 events on 74 maps. `validate.py` and `audit_text.py` are
clean, and `curios_c1` passes (15 checks). Two twin cells nobody could
stand next to were dropped (the Big Bed's (15,5), the Lens Crates'
(32,4)), and `curios.place` now asserts reach per cell, so that cannot
come back. A curio's saved count stops at the number of distinct looks
(look + `then`), so look + one `then` + `again` saturates at 2.

**The contact sheet (C7) was run**: 586 crops, one per curio's tile,
captioned with its first line (a scratch script; the crop maths is
`../CLAUDE.md`'s). 41 lines named something the tile does not show and
were rewritten to the picture, keeping the joke: wine racks called empty
that are full, gold armour called black (Maps 11, 42, 48), "glass cases"
that are gilt boxes, dinner sets that are chop and soup, tea cosies and
a stuffed robin that are not drawn, the Smiths' arms (crossed swords,
not hammers), Map 52's raspberry canes, and more. "Photograph" is in
period (Clanging, 1997 almanacs) and was left.

**The rummage rework (rule 7) is done.** Pell's drawers (Map 15), Quy's
wardrobe (17), Rosamund's wardrobe (36) - each owner answers in their
own window - and the minions' lockers (11), which are rummaged with an
absurd find each and NICE TRY. Kept as restraint: the Gotobeds'
jewellery box and STAMPS drawer (69), locker 40 (22), the wasps (51).
`build/scenarios/curios_rummage.json` covers all four.

**TIMELINE**: 1802 (Bond No. 40, the cabbage) and 1987 (Bryd
Ollerenshaw's BEST IN HALL; Hob had a cold) are in.

**Mr Gotobed (Map 69), at Mike's suggestion.** The crossed swords in
the upstairs alcove and the world map over the bedroom drawers were the
two props on the map with no curio. They are now Mr Gotobed's youth:
ADVENTURER (RETIRED), who came through on a quest to rescue a lady,
knocked on the wrong door, and it was Mrs Gotobed's; and a red line to
every edge of the map and back to Much Pottering, circled: FOUND IT.
The necklace on its stand at the far end of the dresser (2 Nov, at
Mike's suggestion) closes it: the reward, sent on by the lady who got
herself out, GIVE IT TO THE ONE YOU DID RESCUE. I DID. A new kind, `retired_hero`.

**The trope tier** is 90 (rule 9, `journey.py`).

**Still open:**
* Per-wave walk-up scenarios are not written; `validate.py`'s flood is
  the reachability check for all 753.
* Nothing is committed. The curio commit is `build/curios*.py`,
  `build/curio_survey.py`, the two curio scenarios, `build_game.py`,
  `CURIOS.md`, `TIMELINE.md` and the 74 maps - never `Animations.json`,
  `System.json`, `package.json`, `.DS_Store` or `transfers.json`.
