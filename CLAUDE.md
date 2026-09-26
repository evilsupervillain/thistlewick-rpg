# The Obligatory Quest

An RPG Maker MZ 1.10.0 game. The game is data, not code: everything lives in
`data/*.json`, the unmodified engine is in `js/rmmz_*.js`, and the art, audio
and effects are in `img/`, `audio/` and `effects/`.

This project is built with the harness in the parent workspace. Read
`../CLAUDE.md` and `../MZ-DATA-FORMAT.md` first; they cover the data format and
the tools. Everything below is specific to this game.

    python3 build/build_game.py                 regenerate every data file
    python3 ../tools/validate.py .              check the data after every change
    node ../tools/serve.js . 8766               serve this game (background it)
    node ../tools/shots.js /tmp/s 1:20:24       screenshot places in it

## Premise

Every hundred years the Dark Lord rises in the Obligatory Tower, and the village
of Thistlewick sends a Chosen One north to put him down. It has worked
forty-seven times. Bram, a turnip farmer, is Chosen One number forty-eight,
selected by the Prophecy Committee while he was asleep and therefore unable to
object.

The joke the game is built around is that the Prophecy is a *contract*. Grimspite
the Inevitable does not want to be the Dark Lord; he is four thousand years into
a renewable engagement he cannot get out of. Beat him and the Prophecy itself
unrolls to enforce clause twelve, and *that* is the real last boss.

Bram can take up to three of nine companions. Each is a different answer to the
same fight, so who you pick changes how combat plays:

| who | class | good at | bad at |
| --- | --- | --- | --- |
| Bram | Chosen One | everything, slightly; enormous luck | nothing, impressively |
| Merribell | Field Medic | healing, reviving, Light | hitting things |
| Hob Grumnir | Blacksmith | HP, ATK, DEF, one huge hit | speed, magic, being subtle |
| Zephyrine | Hedge Mage | elemental nukes, MAT | HP, DEF, MP economy |
| Nix | Acquisitions | speed, evasion, multi-hits, stealing | taking a hit |
| Sir Aldric | Knight Errant | DEF, covering allies, party buffs | damage, speed |
| Piper Quill | Bard | buffs, debuffs, party utility | raw numbers |
| Corvin Ash | Doomed Rival | dark damage, and more of it the worse things get | DEF, luck, being told the school is very good |
| Wren Halloway | Cataloguer | multi-hit range, poison, armour-shredding, double drops | raw damage |
| Roland Fairweather | Guest Star | everything, genuinely | being there at the end |

The last three are found in a tavern in the south, and the last of them
**leaves at the door of the Obligatory Tower**, which is deliberate. See
`EXPANSION.md` - it is the design document for the whole southern half and is
worth reading before touching any of it.

`WORLDMAP.md` is the design document for the **120x120 world map**, built with
the workspace's `tools/worldgen` around the old 50x50 and finished by hand. It
is **installed**: `Map008.json` is that map, `journey.world_map` loads
`build/worldmap/worldmap.json`, and `places.py`'s every world-map coordinate was
re-cut for it. Read it before touching Map 8, `places.py`, or anything that
walks the overworld by coordinate. Two rules in it are the ones that bite:
**a change to the map is a line in `build/worldmap/run_finish.py`** - never a
hand edit to the JSON and never an anchor added to `grow2.py`, which would
change the RNG stream and grow a different world - and **`build/worldmap/decor.py`
is the check to re-run after any such change**, because it is the only thing
that can see a decoration tile the map has quietly stopped carrying. Its
section 6 item 10, the quests behind twenty-nine placeholder doors, is all that
is left of it - and **`SITES.md` is that queue**: the ordered list of the
twenty-eight sites still to build, one step per session, with the working rules
for the effort. Penultima (Maps 29-30) is the first and is done.

`AUDIT.md` is the queue in front of `SITES.md` section 4 and of the companion
quests: Mike's list of faces and dialogue that disagree with the game, worked
through one item per session. Its section 0 is the rule that decides every
fix - **only what is on the `live-rpg` branch is protected**; everything newer
is free to change, and what is published may only be repaired where the game
contradicts itself.

`NORTH.md` is the design document for what comes next: Upper Clanging, the
airship, and a pass over the whole game adding a kind of joke it currently has
none of. Its section 1 is the specification for every line of dialogue in it,
including what is deliberately out of bounds; read that before writing any of
this game's humour, not just the north's.

## The ending

`journey.finale_event` is the longest command list in the game and most of it is
optional. It is worth knowing its shape before adding to it, because the two
halves are built differently on purpose.

**Inside the Grimspite scene**, before the fight, are two branches on
`SW_CLAUSE_SEVEN` and `SW_OTT_MATERIALS` - the two questions Ott can send the
player up here with. They are separate switches on separate branches so that
either can be asked without the other, and the finale is the only place either
is ever answered. He is never told the airship flew.

**After the fight** the Prophecy's tally is fifteen appended `if_then` blocks
reading `SW_ROLAND_GONE`, `SW_SOUTH`, `VAR_BOUNTIES` (two tiers, the lower
nested in the higher's else), `SW_HISTORY_DONE`, `SW_LAMP_LIT`,
`SW_BENCH_DONE`, `SW_TWO_HUNDRED_FLEW`, `SW_84_REBUILT`, `SW_ITEM_ONE_USED`,
`SW_HOB_BRYD`, `VAR_TROPES` (40 / 20 / else), `SW_BALLAD_DONE`, `VAR_BLUSHES`,
`SW_FF_GRADUATED` and `SW_MET_QUY`. Every one is additive: a new line here is a new block, and
nothing that is already in the tally comes out or gets re-voiced.

**Two counter thresholds are cut against totals that keep moving**, so anything
that adds a `story.trope()` or a `story.blush()` site has to come back here.
`VAR_TROPES` is 40 / 20 against about eighty reachable (Firstfield added
eight; Hithermost adds four more - the sign, the villager, Sir Dunstable and
Quillon - Fairholme three, the King, Rosamund and Mrs Emberthwaite, and Olde
Evermore two, the ARRIVALS sign and Mirabel's biscuit, and Gladhollow four -
Toby, Granny Wendle's barrels, the key under the pot and the bookcase, and
the Former Premises one, Hollowell's tour - the floating castle of the
ancients - and the seven with no map five: the Sky Anvil, the hedge mages'
secret order, the Wrong Dragon, Mother Selvidge's reading and the bell under
Ashcombe Lake, and Tobias Frayne's cottage one, Tobias and his eleven, and Frostwick three,
the town sign, Pargeter and Perce, and Coldbarrow one, Mordaunt's nine files,
and the Sable Hart one, five doomed rivals being fair about seating, and
Sump one, the cursed village and its ancient affliction, and Ashcombe one,
the plaque - the hero's home village, destroyed, and fine - and Weeping Bottom
one, the founder's stone - the healing sanctuary, founded for the air - and
Fenmarch Hall one, the portraits whose eyes follow you, none of which has ever
looked at anybody, and the Collegium Arcanum one, the ancient school of magic
whose motto is REFERATUR, and Great Dunnage one, the watchman at the gate who
has never heard of you);
`VAR_BLUSHES` is 20
against **thirty-four** reachable - twenty-five measured off the data in August
2026, plus Dorothy Markup's in Penultima, which is the first from outside the
north, Walt's tune and the register in Restwell, and the Book in Hithermost's
chapel, and Rosamund's card, and Mirabel's secret, and Frostwick's two, Ida
on the ribbon and Clem at the committee's table, and Cotter Cotterill in
Great Dunnage, who is always very glad to get home - **thirty-four**. The tier
is meant to be four fifths of the true total and is now **59%**; `NORTH.md` 2.3 has the count,
why counting it by grep over-counts and is wrong, and why it is being left
alone. `SITES.md` section 4 item 5 is where it finally gets re-cut, and it is
the one thing on that list that cannot be done incrementally.

**ITEM 1 is a page, not a branch.** The crate is a whole scene rather than a
question, so page 1 of the event is `c[:split] + item_one_scene() + c[split:]`
with an `itemValid` condition, and page 0 rebuilds byte for byte. The splice is
after the Shock2 sting and before the battle, which is the only placement that
does not make him a liar: he has just said he has heard all of them, and four
windows later he says this one is new.

**The Former Premises' signature is three pages, not a branch** - 3, 4 and 5.
`journey.visitors_book_pages` splices the signing into copies of the list at
`sig`, before "Whatever you were going to say", and Hollowell's line into the
tally at `tally`, before clause twelve is struck; page 3 is that on
`SW_VISITORS_BOOK`, page 4 is that with ITEM 1's scene too, and page 5 is the
empty `SW_WON` page again, because a page appended after page 2 would
otherwise beat it and put the finale back on the throne. Pages 0-2 are byte
for byte what they were. Anything appended to Grimspite after this has the
same problem, and the same answer.

`finale_ending` covers pages 0 and 1 in eight passes; see Verifying.
`premises` runs page 3 through the same harness and asserts which page wins
in each of the four states.

## Layout

    build/
      API.md         **generated** - every signature and one-line docstring in
                     `rmmzdata`, `mapkit` and `story`, the id constants in
                     `places` and `db`, and everybody who already has a face.
                     `python3 ../tools/apidigest.py . --write`; `--check` fails
                     while it is stale. **Read it instead of opening a module
                     to find out what it does** - and grep it, do not scroll it
      TILENAMES.md   **generated** - what every `mapkit` tile constant actually
                     is, off the sheet's own `.txt`. A constant is named for
                     what the tile looked like at 48 pixels and is often
                     something else. `python3 ../tools/tileaudit.py . --write`
      mapkit.py      tile vocabulary and drawing helpers; names are what
                     things look like, and were confirmed in screenshots -
                     which is exactly why `TILENAMES.md` exists
      db.py          the whole database
      village.py     Maps 1-7: Thistlewick and its interiors
      journey.py     Maps 8-12: overworld, Gloamwood, the Obligatory Tower.
                     **Map 8 is a file, not a drawing** - `world_map()` loads
                     `build/worldmap/worldmap.json` and adds this game's
                     header and events to it
      south.py       Maps 13-18: Nether Sopping, the Slain Wyvern, the Guild,
                     the outfitters, #45's cottage, the lighthouse
      wilds.py       Maps 19-20: the Bottomless Pit and the Barrow, and the
                     events on the south of Map 8. The four hooks that used to
                     draw that half of the world map are gone
      north.py       Maps 21-25: Upper Clanging and its four interiors
      field.py       Maps 26-27: the Long Field, Attempt Eighty-Four, the
                     wreck of the 199th and ITEM 1, the events on the
                     north-west of Map 8 - its five `north_*` drawing hooks are
                     gone too - and the three places out at sea
                     that only the airship can reach. It also holds the three
                     pages `north.py` appends to Ott and the works stores
                     ledger, because those are the field's payoff and the
                     crag's
      meadow.py      Map 28: Firstfield Meadow, the optional tutorial, and
                     the event at the foot of the rainbow on Map 8. Its two
                     drawing hooks are gone; the rainbow itself is a tile on
                     the world map now
      restwell.py    Maps 31-32: Restwell and The Eight Hours, and the real
                     door events on Map 8 for that site. `SITES.md` step 1, and
                     the second site to be wired: the same shape as
                     `penultima.py` with an **inn** where the shop was, which
                     is what it was built to prove
      hithermost.py  Maps 33-34: Hithermost and the Chapel of Continuance,
                     and the real doors on Map 8 for **three** sites stacked up
                     one pass - the village, the chapel and the Door into the
                     Mountain. `SITES.md` step 2. A cluster exports `SITES`, a
                     name-to-builder dict, instead of one `SITE` string. The
                     Book on the lectern is a **save point**, and the Door
                     into the Mountain is a door that says no
      fairholme.py   Maps 35-37: the council chamber of Fairholme, Princess
                     Rosamund's tower room, and Mrs Emberthwaite's lair, and
                     the real doors on Map 8 for **two** sites - `SITES.md`
                     step 3, a `SITES` dict like `hithermost.py`. The council
                     table is three tables end to end, and the lair's dragon is
                     `$BigMonster2` with no face
      evermore.py    Maps 38-39: Olde Evermore and the Forbidden Archive, and
                     the real door on Map 8 - `SITES.md` step 4, one `SITE`
                     like `penultima.py`. **Touches the spine**: the horse in
                     the margin sits beside clause twelve, and the game never
                     says why; the docstring says what it may not contradict
      penultima.py   Maps 29-30: Penultima and Ye Final Shoppe, and the
                     **real** door events on Map 8 that replace the two
                     placeholders worldmap.json ships for that site. It is the
                     first of the new world map's twenty-nine sites to have a
                     room behind its door, and the shape every other one
                     should copy - `WORLDMAP.md` 7.6
      art.py         generated character art: which settings file is in which
                     cell of which `Gen_*` sheet. Not part of the data build;
                     run it when a look changes. See "Generated characters"
      characters/    the Character Generator settings files - the only copy
                     of each generated look, including ones not in the game yet
      places.py      map ids, the six world-map region ids, and the
                     coordinates two modules have to agree on - **every
                     world-map coordinate in it was re-cut for the 120x120
                     map**, and its docstring says which ones are not `+ (35,35)`
      story.py       shared dialogue helpers and the endgame
      build_game.py  runs all of the above, then System.json and MapInfos
      scenarios/     scripted playthroughs for `tools/scenario.js`
      balance.py     offline damage report: evaluates the real formulas
      sampler.py     throwaway tile sampler; writes Map099. `build_game.py`
                     deletes any map that is not on its own list, so the
                     sampler cannot ship by accident - run it *after* a build,
                     never before one you intend to keep

## Ids

Nothing here is ever renumbered - saves and cross-references point at ids.
Append instead.

| range | what |
| --- | --- |
| Actors 1-10 | Bram, Merribell, Hob, Zephyrine, Nix, Aldric, Piper, Corvin, Wren, Roland |
| Classes 1-10 | one per actor, same order |
| Skills 1-2 | engine-reserved Attack and Guard |
| Skills 10-19 | Bram |
| Skills 20-29 | Merribell |
| Skills 30-39 | Hob |
| Skills 40-49 | Zephyrine |
| Skills 50-59 | Nix |
| Skills 60-69 | Aldric |
| Skills 70-79 | Piper |
| Skills 90-99 | enemy and boss skills |
| Skills 100-109 | Corvin |
| Skills 110-119 | Wren |
| Skills 120-129 | Roland |
| Skills 130-139 | southern enemy and boss skills |
| Skills 140-149 | northern enemy and boss skills |
| Items 1-19 | consumables (10-12 are southern, 13-15 northern) |
| Items 20-29 | key items (23-29 are southern) |
| Items 30-32 | northern key items - the 20-29 block is full. 30 is the
  oilskin, 31 is Attempt 112's number-plate, 32 is ITEM 1. The range was
  reserved to 36 and three were enough |
| Weapons 1-33 | roughly three per class, in class order; 32-33 are the north's |
| Armors 1-26 | shared body/head/accessory; 16-22 are southern, 23-26 northern
  - Sensible Trousers, Works Cap, The Fuse (Removed) and the Governor |
| Enemies 1-19 | ordinary encounters (12-18 are southern). **Full**: northern
  ordinary encounters continue at 30 |
| Enemies 20-29 | bosses (23-26 are the optional ones, 27 is Attempt
  Eighty-Four) |
| Enemies 30-32 | northern encounters: Loose Pressure, Attempt (Unnumbered),
  Ambulant Salvage. Reserved to 35 |
| Troops 1-19 | encounter groups (11-17 are southern). **Full**: northern
  groups continue at 30 |
| Troops 20-29 | set-piece fights (24-27 are southern, 28 is Eighty-Four) |
| Troops 30-33 | northern encounter groups |
| Maps 1-7 | Thistlewick and interiors |
| Maps 8-12 | the journey |
| Maps 13-18 | Nether Sopping and its interiors, and the lighthouse |
| Maps 19-20 | the Bottomless Pit, the Barrow of the Forty-Fourth |
| Maps 21-25 | Upper Clanging and its interiors: the works, the inn, the forge,
  the Parish Rooms. `north.py` |
| Maps 26-27 | the Long Field, and the wreck of Attempt 199 on her crag.
  `field.py` |
| Map 28 | Firstfield Meadow. `meadow.py` |
| Maps 29-30 | Penultima and Ye Final Shoppe. `penultima.py`, and the first of
  the new world map's twenty-nine sites to have anything behind its door -
  `../WORLDMAP.md` item 10. **The places behind those doors start here and run
  up**, and each one is a module of its own |
| Maps 31-32 | Restwell and The Eight Hours. `restwell.py`, `SITES.md` step 1 |
| Maps 33-34 | Hithermost and the Chapel of Continuance. `hithermost.py`,
  `SITES.md` step 2. **`MAP_CONTINUANCE`, not `MAP_CHAPEL`** - that name is
  Thistlewick's chapel, Map 5 |
| Maps 35-37 | Fairholme's council chamber, Rosamund's tower, Mrs
  Emberthwaite's lair. `fairholme.py`, `SITES.md` step 3. **`MAP_ROSAMUND`,
  not `MAP_TOWER`** - that is the Obligatory Tower, Map 11 |
| Maps 38-39 | Olde Evermore and the Forbidden Archive. `evermore.py`,
  `SITES.md` step 4. `MAP_EVERMORE`, `MAP_ARCHIVE` |
| Maps 40-41 | Gladhollow and the mayor's house, whose back room is on the
  same map. `gladhollow.py`, `SITES.md` step 5. `MAP_GLADHOLLOW`,
  `MAP_MAYORS` |
| Map 42 | The Former Premises, the hall with the lift, on the floating
  continent. `premises.py`, `SITES.md` step 6. **`MAP_PREMISES`, not
  `MAP_HALL`** - that is Prophecy Hall, Map 3. Air only: its way out carries
  `<airreturn>`, see `../CLAUDE.md` on vehicles |
| Map 43 | Tobias Frayne's cottage on the coast road. `frayne.py`, `SITES.md`
  step 8. **`MAP_FRAYNE`, not `MAP_COTTAGE`** - that is Number Forty-Five's,
  Map 17 |
| Maps 44-47 | Frostwick, the Eleven Days, the Working Group and the Cold
  Room. `frostwick.py`, `SITES.md` step 10. **`MAP_WORKING_GROUP`, not
  `MAP_PARISH`** - that is Upper Clanging's Parish Rooms, Map 25. It snows on
  the street and nowhere else: `north.py`'s weather idiom, with a local
  `door()` that clears it |
| Map 48 | The Chapter House of the Order of the Errant at Coldbarrow.
  `coldbarrow.py`, `SITES.md` step 11. `MAP_COLDBARROW`. The great map is
  a **picture**, `img/pictures/Coldbarrow_Map.png`, drawn by running the
  module - not by the data build - with every pin placed by site name |
| Map 49 | The Sable Hart, the inn where every corner is taken. `sable_hart.py`,
  `SITES.md` step 12. **`MAP_SABLE_HART`, not `MAP_INN`** - that is
  Thistlewick's, Map 4. Its `journey.py` alias is `HART`: `SH` is the
  Gloamwood's height there |
| Maps 50-51 | Little Gore and Sump, two hamlets of one street each.
  `hamlets.py`, `SITES.md` step 13, a `SITES` dict like `hithermost.py`.
  `MAP_LITTLE_GORE`, `MAP_SUMP`; its `journey.py` alias is `HAM` |
| Maps 52-53 | Ashcombe, the village that is fine, and one map of two rooms
  indoors - Mrs Ash's kitchen and the Drainage Museum, side by side in the
  black like Gladhollow's back room, with no display name. `ashcombe.py`,
  `SITES.md` step 14. `MAP_ASHCOMBE`, `MAP_ASHCOMBE_IN`; its `journey.py`
  alias is `ASH` |
| Maps 54-55 | Weeping Bottom, the valley bottom with the Sisterhouse in it,
  in a drizzle, and the ward, split down the middle by a line between the two
  orders. `weeping_bottom.py`, `SITES.md` step 15. `MAP_WEEPING_BOTTOM`,
  `MAP_WARD` - **not `MAP_SISTERHOUSE`**, which is both. Its `journey.py`
  alias is `WB`. It rains on Map 54 and nowhere else: `frostwick.py`'s
  weather idiom |
| Maps 56-57 | Fenmarch Hall, the walled garden with the house in its moat,
  and the long gallery, which is most of the house - the household at one
  end, thirty-two glass cases and eight portraits going east.
  `fenmarch.py`, `SITES.md` step 16. `MAP_FENMARCH`, `MAP_GALLERY` - **not
  `MAP_HALL`**, which is Prophecy Hall. Its `journey.py` alias is `FEN`. The
  cases and portraits are character sheets drawn by **running the module**,
  not by the data build, like Coldbarrow's map |
| Maps 58-60 | The Collegium Arcanum: the Great Court behind the gate, with
  the Porter's Lodge and the Founder on the lawn, the Library and the Hall.
  `collegium.py`, `SITES.md` step 17. `MAP_COLLEGIUM`,
  `MAP_COLLEGIUM_LIBRARY`, `MAP_COLLEGIUM_HALL` - **not `MAP_HALL`**, which is
  Prophecy Hall. Its `journey.py` alias is `COL`. Dean Fenwold's portrait is
  a character sheet drawn by running the module, like Fenmarch's |
| Maps 61-65 | Great Dunnage: the town inside its wall, with the haulage yard
  in its north-west corner; the Smiths' Hall; the Counting House's lobby,
  which is mostly door; the Bonded Warehouse; and the Bell. `dunnage.py`,
  `SITES.md` step 18, the last. `MAP_DUNNAGE`, `MAP_SMITHS_HALL`,
  `MAP_COUNTING_HOUSE`, `MAP_BONDED`, `MAP_BELL` - **not `MAP_WORKS`,
  `MAP_FORGE` or `MAP_INN`**, which are Upper Clanging's and Thistlewick's.
  Its `journey.py` alias is `DUN`. Nix's refusal is on the warehouse's own
  door, not the town's |
| Map 99 | the tile sampler, not part of the game |
| **Firstfield** | fresh blocks, because `SPARE.md` has spoken for the free ends
  of the north's (Enemy 28, Troop 29, Weapon 34, Armor 27, Items 33-34, Skills
  146-155): **Armors 30-32** A Stick, A Straighter Stick, Certificate of
  Completion; **Skills 160-161** Telegraph, Enormous Swing; **Enemy 40**
  Norbert; **Troop 40** Norbert (Tutorial) |

Icon indices in `db.py` and in the `\I[n]` codes in dialogue were re-checked
against `img/system/IconSet.png` cell by cell when the south was added; several
of the original ones pointed at the wrong cell (rings that were orbs, a
prophecy that was a glove). The sheet is 16 icons to a row: row 6 is weapons in
`wtypeId` order from 96, row 8 is armour from 128, row 11 is consumables from
176, row 12 is tools and instruments from 192, and the food is at 256-280.

## Switches and variables

| id | switch |
| --- | --- |
| 1 | quest accepted (the Elder has said the words) |
| 2 | the party has left the village |
| 3 | Gloamwood cleared |
| 4 | Grimspite defeated |
| 5 | the Prophecy annulled - the game is won |
| 6 | the tower door is unbarred |
| 11-19 | recruited: Merribell, Hob, Zephyrine, Nix, Aldric, Piper, Corvin, Wren, Roland |
| 20 | the mimic has been met |
| 21 | Roland has left at the tower door |
| 22-24 | the Feud: jar going south, reply going north, done |
| 25-27 | the Guild: asked, Form A-1 found, registered |
| 28-31 | bounties: crab beaten, Crooke beaten, and each one paid |
| 32-33 | the lighthouse: asked for oil, lit |
| 34-36 | the Pit: asked, badger gone, Splint has paid |
| 37-38 | the Barrow: entered, the Forty-Fourth has stopped |
| 39-40 | the bench: asked for, built |
| 41-42 | Hosea's history: asked, complete |
| 43 | #45 told Bram what to ask Grimspite - this changes the finale |
| 44 | met #46 on his log |
| 45 | has been to Nether Sopping |
| 46 | knows the wyvern is a goose |
| 47-67 | the north. Named in `db.py` and specified in `NORTH.md` section 10:
  47 been to Upper Clanging, 48 Ott has explained what she needs, 49-50 the
  oilskin, 51-52 the spar, 53 the airship flies, 54-55 ITEM 1, 56-57 Attempt
  Eighty-Four, 58 Hob and Bryd went for a drink, 59-60 the ballad, 61 the
  Cold Winter, 62 met the Cotterills, 63 the nine-year-old has applied,
  64 walked the Long Field, 65 clause seven, 66 room four, 67 Gerald,
  68 the Two Hundred set down beside the tower, 69 the two travellers
  have been asked how long, exactly - the retrofit's one global switch,
  because the joke is one moment across two events and a self switch is
  keyed on (map, event id, letter), 70 Ott asked you to ask what the tower
  is made of, which is also the last thing her flying chain sets and so the
  one switch that means "Ott has nothing left owing", 71 the crate was set
  down in front of the throne. **59 is reserved and unused** - it was
  drafted as the ask half of an ask-then-done pair and the fete minutes
  turned out to be a board rather than a conversation. It is never set and
  never read, and `System.json` names it as unused so nobody goes looking
  for the event |
| 72-80 | **has been in the party before**: Merribell, Hob, Zephyrine, Nix,
  Aldric, Piper, Corvin, Wren, Roland. 11-19 mean "is walking behind you right
  now" and go *off* when a form desk strikes somebody off; these go on at the
  first join and never go off again. They pay for three things. Change Party
  Member's *initialise* flag calls `Game_Actor.setup()`, which resets the actor
  to their database level and database equipment - correct exactly once, and on
  a rejoin it silently deletes every level they earned with you and every piece
  of kit you gave them, so `story.recruit` initialises only when the switch is
  clear. The switch is also page 1 of all nine recruit events: somebody you have
  already walked north with does not introduce themselves again. And it is why
  the "gone" page is page 2 of 3 - `Game_Event.refresh` takes the last page
  whose conditions hold, and anyone with you has necessarily also been met |
| 81-87 | Firstfield Meadow: 81 Fizz has said HEY, 82 Old Hollis's stick,
  83-84 Dilys's sheep asked and found, 85 the chest, 86 Norbert has lost,
  87 graduated. **`SPARE.md` proposes 72-74 for itself**, which `SW_KNOWN`
  took after it was written - it needs new numbers before it is built |
| 88 | the Former Premises: Hollowell has given you the slip for the visitors'
  book. Set on Map 42 and read by a page on Grimspite on Map 12, which is why
  it is a global - a page condition cannot name another event's self switch.
  The first new switch of the world-map sites |

| id | variable |
| --- | --- |
| 1 | companions recruited |
| 2 | **tropes encountered** - the running gag. Every cliche the player walks
     into bumps it, and the ending reads the total back to them. Bump it with
     `story.trope()` and nowhere else. |
| 3 | turnips eaten |
| 4 | tales heard in the Slain Wyvern - Hosea pays out at six |
| 5 | bounties claimed |
| 6 | wreck plaques read - Ott opens up at twelve. The thirteenth plaque
     deliberately does not count: there are twelve readable plates in the
     Long Field and the thirteenth is one you make |
| 7 | **things nobody quite said** - the north's running gag, and the
     companion to variable 2. Every Register A moment bumps it once, on first
     sight, and the ending prints the total. Bump it with `story.blush()` and
     nowhere else. `NORTH.md` 2.3 is the specification and it matters: the
     joke exists only in aggregate, which is exactly what keeps every
     individual instance deniable. **Twenty-five reachable moments**; a grep
     of `data/` says 28 and over-counts, for the three reasons in 2.3 |
| 8 | Ott's beat while the oilskin-and-spar order is outstanding - a nine-beat
     chain. A variable and not a run of self switches because a page
     condition can name exactly one self switch, and four letters do not
     reach nine |
| 9 | the same for the seven beats after the Two Hundred flies. Its last write
     is the one that sets switch 70, which is what makes that switch usable as
     "Ott has nothing left owing" - and anything appended to Ott below her
     ladders has to require it, or it shadows them. `NORTH.md` 16 step 6 is
     the write-up of the lockout that taught us so |
| 10 | scratch, owned by `build_game.py` - Nix's reallocated gold |
| 11 | Firstfield stations done, of four. Fizz's graduation page needs all four,
     and a page condition can name two switches at most |
| 12 | Firstfield sheep found, of three |
| 13 | Firstfield signs read - which of her three spare lines Fizz uses |
| 14 | Toby's delivery: which of his fourteen he did last, 15 being the one he
     is still working on, and round to 1 again. A variable because the joke
     is a list of fifteen and a page condition can name one self switch.
     Gladhollow's hint is this mod three. The first new global of the
     world-map sites |

## Verifying

Nothing here is judged by reading the data back. Maps are judged from
screenshots, fights from numbers, and events from a scripted playthrough.

    node ../tools/serve.js . 8766                # background it, then
    node ../tools/scenario.js build/scenarios/opening.json
    ../tools/scenarios.sh .                      # or all thirty-six

The whole suite is a little over an hour, so background it and read
`build/scenarios/logs/` afterwards rather than watching it. `scenarios.sh`
checks before it starts that 8766 is serving *this* game and that no Chromium
has been orphaned by an earlier killed run, because both of those turn an hour
of machine time into an hour of confusing output.

Headless runs at about twelve frames a second on a map and three in a battle,
so playing a boss fight through a scenario takes the better part of an hour and
mostly tests the renderer. `finale_ending` sidesteps that: it feeds the finale's
own command list straight to the interpreter with Battle Processing filtered
out, so every switch, item and screen effect still runs, with no key presses at
all. Use the same trick for any long cutscene.

**Filtering the Show Texts out as well is the version of that trick to avoid,
and it is what this scenario used to do.** An optional ending is *made of*
Show Text inside a Conditional Branch, so a scenario that deletes the messages
before running the list can assert nothing whatever about which branch it took
- and four shipped endings sat behind checks that would have passed with every
one of them deleted. The fix is to take the blocking out of the messages
instead of taking the messages out of the list:

    Game_Message.prototype.add = function (t) { window._lines.push(t); };
    Game_Message.prototype.isBusy = function () { return false; };

The interpreter then runs the whole cutscene without ever opening a window -
`hasText()` is false, so `Window_Message` does not try - and what comes back is
every line the player would have read, in order, ready to assert against. Two
things go with it. A choice must be answered by a shim on `setupChoices`,
because a choice left unanswered takes *neither* branch: `command402` compares
against a `_branch` entry nothing ever wrote, and the run silently loses
everything under both halves. And if the pass is only about what was printed,
filter the waits and screen effects (`230`, `221`, `222`, `223`, `225`) as
well - the interpreter will run a hundred thousand commands in a frame before
it decides it has frozen, so the entire finale executes in one. That is what
makes eight passes over it cost less than the single pass did before.

| scenario | what it proves |
| --- | --- |
| `opening` | the house scene, the sword, the turnips, walking out the door |
| `village` | the gate refuses a Chosen One with no quest; the Elder gives it; Merribell joins |
| `gate` | a lone hero is still turned back; two of them get onto the world map |
| `journey` | Gloamwood, the Thing that blocks the way, and the tower door |
| `tower_door` | a party without Nix finds the key under the mat; the Cache arms all seven |
| `nix_door` | Nix opens the same door without it |
| `battle_mook` | a random encounter at level 6 is a fight, not a formality |
| `finale` | the throne-room scene runs and the Grimspite fight starts |
| `finale_ending` | the ending, in eight passes over the same command list.
  Seven fast ones capture the narration and assert which optional endings
  printed: clause seven and the materials question independently and together,
  the two `VAR_BOUNTIES` tiers each with the other's line asserted *absent*,
  and the ITEM 1 stores-book line. Pass D is the one worth having - it is the
  only state in which Grimspite saying she will never get one off the ground
  and the attempt log reporting that she did are both on screen, which is the
  game's central joke and had nothing standing behind it. The eighth runs at
  full length with the waits intact for the switches, the receipt and the
  return to the title |
| `reachable_home` | the bed, the sword and the front door of Bram's house,
  walked to with the arrow keys and triggered with the action button |
| `reachable_village` | the Fisher on the pond bank, Prophecy Hall's door, the
  Wall of the Forty-Seven, the Creed and the Organ, the same way |
| `south_road` | the coast road east is walkable end to end, the shingle is
  its own encounter region, and the town door opens |
| `north_road` | the west road is walked end to end with the arrow keys, from
  the Gloamwood's north mouth to the door of Upper Clanging, plus both spurs;
  and the Standing Stones are proved to be *beside* the road rather than on it |
| `reachable_sopping` | all four doors of Nether Sopping, walked to with the
  arrow keys from the north road |
| `reachable_clanging` | walking into Upper Clanging off the world map, up the
  whole street and both flights of steps, and through all four doors - and
  that the rain stops indoors and does not follow the player home |
| `clanging_cast` | the town's dialogue: Ott's four steam beats arrive one per
  conversation and then stop, Spare's three, the whole Cotterill doorstep, the
  Cold Winter, Gudgeon over the parish ledger, the Parish Rooms counter opening
  as a real shop, and Hob and Bryd - with `VAR_BLUSHES` asserted after every one
  of them, because a counter nobody checks is a counter that silently reads zero
  in the ending. It is also where Ott's first rung is proved **with** Merribell
  in the party: that moment is a conditional branch, and a conditional blush
  that has only ever been run one way is indistinguishable from one somebody
  deleted. `two_hundred` runs the same four rungs without her and asserts the
  counter does not move |
| `clanging_faces` | each of the eighteen northern faces read off the **live
  message window** rather than off the data, and screenshotted. It is the check
  that catches an off-by-one between `story.FACES` (0-based, like MZ's
  `faceIndex`) and `img/pictures/` (1-based), which is a mistake that builds,
  validates and looks like somebody else answering - and the only thing standing
  behind two casting decisions with reasons: Winnie on `People1` 7 because she
  is sixty, and Rivet off `SF_Actor2` 2 because that face reads as a girl at
  both sizes |
| `two_hundred` | Ott's quest end to end without Hob: the ask amidships, the
  spar in a day, forty bolts of oilskin on account, and the airship placed on
  the world map at (10, 13). It also walks **both of Ott's beat chains** - five
  conversations of the order chain and all seven of the flying chain - because
  five of her six Register A moments live in them and nothing else in the suite
  executes one. The last beat of the flying chain is what sets
  `SW_OTT_MATERIALS`, so this is also the check that the ladders can be finished
  at all |
| `hob_and_bryd` | the same spar with Hob in the party - forged in an
  afternoon, and then they go for a drink, and `SW_HOB_BRYD` |
| `airship_lands` | the one that protects the joke. It asserts
  `isAirshipLandOk` out of the flags, then **flies over the tower door and
  presses the button**, and the engine refuses; then lands on the grass beside
  it and walks in. Then all three of the air-only rocks |
| `tavern` | all six tales count, and each one counts as a cliche |
| `tavern_history` | Hosea asks for six, pays out at six, and the wyvern turns
  out to be a goose |
| `recruit_south` | Corvin and Wren join; a full party is turned down |
| `guest_leaves` | Roland joins over-levelled and is gone - with his gear
  handed back - by the time the party reaches the tower door |
| `feud` | the jar goes south, the reply comes north, the locket arrives |
| `guild` | reference plus hat plus the mat equals a Guild Card |
| `barrow` | the card opens the mound, the Forty-Fourth stops and asks for a
  bench, the bench is built, and Ysolde answers |
| `lighthouse` | Mrs Barrow's shelf is stocked and Lamp Oil can be *bought*
  through the shop windows, not granted - then Bother, the climb and the lamp |
| `long_field` | the gate off the spur road, the twelve plaques counting once
  each, `VAR_PLAQUES` landing on twelve, clause seven out of Ott, and the
  thirteenth plaque made out of Attempt 112's number-plate - which does *not*
  count, because twelve is twelve. Also the guard: twelve plaques on their own
  must **not** change which page Ott is on, because those pages sit below both
  of her beat chains and would delete them |
| `eighty_four` | the furrow is walkable from her empty plot to the top of the
  field, the action button reaches her, "Stop her" starts the right fight
  against the right enemy, and the stop, the rebuild and the governor |
| `item_one` | the stores ledger, the crag, the log with seven minutes missing
  out of it, ITEM 1 off the crag for the first time since 1802, and Ott
  rendering it down into a weapon and an accessory |
| `item_one_throne` | the stretch goal: carrying ITEM 1 to the throne room
  instead. Both branches of the choice - "Draw your weapon" keeps the crate
  and sets nothing, "Set the crate down" lights it - plus the page mechanism
  itself, which is that `findProperPageIndex()` returns the crate page while
  the crate is held and drops back to the ordinary finale the moment it is
  spent. The crate block is found in the command list **by its label**: the
  finale opens with a choice of its own, and slicing from the first code 102
  on the page runs the whole introduction and takes the wrong branch while
  reporting a pass |
| `restwell` | `SITES.md` step 1, walked: onto Restwell's door off the world
  map, in at the west gate, the fingerpost, in at the Eight Hours, Walt's tune
  and the register (a blush each), **a night in a bed that actually restores
  the party** - which is the mechanic the site exists to prove - Dr Pike, and
  back out onto `places.RESTWELL_STEP` |
| `hithermost` | `SITES.md` step 2, walked: onto Hithermost's door off the world
  map, the sign and the villager, in at the chapel, Sir Dunstable, **the Book,
  which is the save screen** - counted with a spy on `Scene_Save.start`, since
  `advance` presses Enter inside it and saves - and signing it a second time
  for "Again? Of course", Quillon, out through the porch, the Door into the
  Mountain refusing, back out onto `places.HITHERMOST_STEP`, and then the
  chapel's and the mountain's own world-map doors |
| `fairholme` | `SITES.md` step 3, walked: onto Fairholme's door off the world
  map, the minutes, round the end of the table to King Aldous, up to Rosamund,
  **the card in her bag, which is the blush**, the bag, back down, Sir
  Dunstable's empty chair and its place card, Mr Pilbeam, out onto
  `places.FAIRHOLME_STEP`; then the lair's door, the tablet, Mrs Emberthwaite
  and a hand of whist, Mr Emberthwaite's chair, and out onto `places.LAIR_STEP` |
| `evermore` | `SITES.md` step 4, walked: onto Olde Evermore's door off the world
  map, over the edge and into the leaves, the ARRIVALS sign, the raker, into
  the Archive, Mirabel four times - the biscuit, the horse, **the secret, which
  is the blush**, and bedtime - the Archive's copy of the Prophecy, and back
  out down the path onto `places.EVERMORE_STEP` |
| `frayne` | `SITES.md` step 8, walked: onto Tobias Frayne's door off the world
  map, a knock, Tobias and the eleven (the trope, counted once), the jar he
  pays out of and does not open here, the medicine shelf, **the foot of the
  ladder, which blocks** - the upper cells are ladder tiles over a wall face -
  the book, and back out onto `places.FRAYNE_STEP` |
| `frostwick` | `SITES.md` step 10, walked: onto Frostwick's door off the world
  map, the town sign, the Cold Room and Pargeter (with the Prophecy in the bag,
  so her branch runs), the Schedule of Snowfalls and the larder, the Working
  Group - Clem's blush, Mrs Blagg, the minutes, the asset register, the
  ribbon - the Eleven Days, **a room that restores a party at 1 HP** for
  eleven crowns, the visitors' book and the plate, then Ida's blush and Perce
  on the green, the ribbon post, the Staggs' shut door, and out onto
  `places.FROSTWICK_STEP`. The weather is asserted at every door: snow on the
  street, none indoors, none on the world map |
| `sable_hart` | `SITES.md` step 12, walked: onto the Sable Hart's door off
  the world map, Crake (the trope, counted once), Crake again, Crake with
  Corvin in the party - the reaction shot, asserted to say nothing of the
  league table or where he is on it - Rook, Mrs Garrow, Blackwood by the fire,
  **the league table, asserted to stop at fourth**, the rota, Veyle twice, the
  empty table, Morrow, the newsletter with Corvin's apologies, and back out
  onto `places.SABLE_HART_STEP` |
| `hamlets` | `SITES.md` step 13, walked: onto Little Gore's door off the
  world map, the three Vanes playing weddings on the green, Mrs Vane twice -
  asserted to say nothing of a letter, a mantelpiece or Aldric - Dame Winifred
  Cope, **the banns, with INVITATIONS TO FOLLOW under them**, the fingerpost
  and out onto `places.LITTLE_GORE_STEP`; then onto Sump's door, the sign (the
  trope, counted once), the well, the pool that is the sea, Mr Gammage twice,
  the Parish Clerk, the Parish Clerk with Merribell in the party - the reaction
  shot, asserted to say nothing of what the curse is - the minutes, Mrs Pardew,
  and out onto `places.SUMP_STEP` |
| `ashcombe` | `SITES.md` step 14, walked: onto Ashcombe's door off the
  world map, in at Mrs Ash's door - Mrs Ash twice, asserted to hand over no
  scarf and mention no study or invitation, her basket, the letter on the
  dresser - the Drainage Museum, Mr Weir twice (**eight miles is by the
  road**, which is what reconciles Corvin's line with the lake's), and its
  six exhibits, the plaque (the trope, counted once), the school, the church
  and the bell the lake says they took with them, the Flood Dinner's notice
  with its speaker TO BE CONFIRMED, Wilf, Mrs Dimmock, the post office; then
  **Corvin at his mother's door, which does not open**, twice, the plaque and
  Mr Weir with him in the party - reaction shots, not COR-1 - and back out
  onto `places.ASHCOMBE_STEP` |
| `weeping_bottom` | `SITES.md` step 15, walked: onto Weeping Bottom's door off
  the world map, down into the drizzle, the board, the founder's stone (the
  trope, counted once), Sister Pim and Mr Crouch on the shore, in at the
  Sisterhouse - where it stops raining - the whole ward from both halves of
  the line: Sister Lamb, Mr Nuttall, the Prioress twice, the minutes, Mr Dace,
  the correct treatment, an empty bed, Sister Bewick twice, the doctrine, Sir
  Hamo and the medicine shelf; out, the locked chapel and the physic garden;
  then Merribell and Sir Aldric in the party - three reaction shots, asserted
  to say nothing of a queue, a contest, a Pamphlet, a vigil or a promotion -
  and back out onto `places.WEEPING_BOTTOM_STEP`, dry |
| `fenmarch` | `SITES.md` step 16, walked: onto Fenmarch Hall's door off the
  world map, in at the gate - RESPICE, and FOUND IT scratched at a ten-year-
  old's height - the moat, Tom from Little Gore, over the bridge and in; Mrs
  Puddifoot, the Fourth, the Marsh Bear's case, the First's portrait (the
  trope, counted once), the flowers under the Third, the Scaled Rook, Mr
  Ottershaw, the unicorn of the Home Farm and the Fourth's portrait, the only
  one facing out; then **Wren at the first case**, a reaction shot asserted to
  say nothing of a fee or an engagement; out onto `places.FENMARCH_STEP`; then
  **Sir Aldric at the world-map door, which refuses**, twice, asserted to say
  nothing of a letter, an errand or a nephew |
| `collegium` | `SITES.md` step 17, walked: onto the Collegium Arcanum's
  door off the world map, the arms over the Lodge window (REFERATUR - the
  trope, counted once), the IN and OUT board, Mr Gedge twice, keep off the
  grass, **the Founder, read from the grass**, Dr Hapgood; the Hall - the
  undergraduate, the Honorary Fellow's chair, the talk, Dean Fenwold twice,
  his portrait and the First Dean's; Congregation's notices; the Library -
  Prewitt twice, **the Register, asserted to name nobody**, the Appeal, the
  monographs, the reader; then **Wren at the monographs**, a reaction shot
  asserted to say nothing of reviewers or specimens; out onto
  `places.COLLEGIUM_STEP`; then **Zephyrine at the world-map door, which
  refuses**, twice, asserted to say nothing of fines, paperwork or the duck |
| `dunnage` | `SITES.md` step 18, walked: onto Great Dunnage's door off the
  world map, the arms over the gate, **the watchman who has never heard of
  Bram** (the trope, counted once), the First Mayor, the anthem, the nine
  works and Mrs Poskitt; the Bell - the Contest's poster, **a night's room
  for fifteen crowns**, the bell, three judges and Mr Tweddle; the Counting
  House - the Mayor at the preamble twice, the Door, the memorandum, the Town
  Clerk; the Smiths' Hall - the Prime Warden twice, Warden Crabbe, Miss
  Fettle, the Schedule, the banners and the prize; **Cotter at the Iron
  Company's gate** (the blush, counted once); the haulage yard and Duchess;
  the Bonded Warehouse - Mr Tibbs twice, the Bond Book, Bond No. 1 and the
  piano; and out onto `places.DUNNAGE_STEP`. Every reaction shot is asserted
  absent with nobody in the party |
| `dunnage_company` | the same town with Hob, Nix, Aldric, Piper and Corvin
  in the party: **the gate lets everybody in**; Nix at the Counting House's
  Door, Piper at the poster, Hob at the Schedule, Corvin at Miss Fettle's
  bench and Aldric at Duchess are reaction shots, each asserted to say
  nothing of its quest; and **the Bonded Warehouse's door refuses Nix**,
  twice |
| `coldbarrow` | `SITES.md` step 11, walked: onto Coldbarrow's door off the
  world map, **the great map, which puts `Coldbarrow_Map` up as picture 1 and
  takes it down after**, Mordaunt and the nine pins (the trope, counted once),
  Mordaunt again, Mordaunt with Sir Aldric in the party - the reaction shot,
  asserted to offer nobody a promotion - the desk, the files, the committee's
  table, and back out onto `places.COLDBARROW_STEP` |
| `placeholder_doors` | that the world map's **remaining site doors do nothing**.
  It was 41 on 29 sites and is **2** now: every site but Village 1 has become
  a real door. Every page of the two left has no commands, which is how an
  event says "this exists and is not finished" - and it is asserted out of the
  live game rather than off the data, because the day somebody wires the first
  real transfer is the day it stops being true for one of them. It walks onto
  both of Village 1's cells, (61,61) and (60,61), and checks the interpreter
  does not start. `SITES.md` section 4 decides Village 1, and this walk moves
  or goes with it |
| `blushes` | the whole of `NORTH.md` section 3, in one walk: room four, the
  house register, Sops, both travellers, Perpetua and Gerald, the fete
  minutes, the washstand, Wren's three specimens and the second notice at the
  Standing Stones. Every one of them is asked a second time and `VAR_BLUSHES`
  asserted not to have moved, and the last check is that the retrofit came to
  eleven - the number 2.3 asked for |

| `firstfield` | Firstfield Meadow walked with the arrow keys: in off the rainbow,
  Fizz in front of you before a step and in front of the sign you try to read,
  Old Hollis's stick and giving it back, the chest, Dilys's "But thou must"
  loop taken once, and three sheep that are pigs - with the trope count
  asserted at each station |
| `firstfield_graduation` | Norbert in the gap in the fence, the battle against
  the generated enemy, his knocked-down sprite off the generated damage sheet,
  the gap opening, the graduation with the lore loop taken once, and the way
  out back onto the spur |

The two `reachable` scenarios exist because every other scenario here starts
its events with `$gameMap.event(n).start()`, which proves what an event does
and nothing at all about whether the player can get to it. They walk instead,
and check `$gameMap._interpreter.eventId()` to see which event the button
press actually reached. `validate.py` catches the same class of bug statically
now, so these are the confirmation rather than the search.

    python3 build/worldmap/coords.py

checks every world-map coordinate the scenarios name against the finished
Map 8, in under a second. The suite is the ground truth and takes nearly three
hours; this is the cheap half of it, and it exists because the 120x120
migration left fifteen stale coordinates behind and the suite found the last
one as scenario thirty-six of thirty-seven.

    python3 build/balance.py 8

prints, for every enemy, what each character's best hit does to it and what its
best hit does to the squishiest party member. Use it before touching a stat: the
fights were tuned so a four-person party kills a mook in two or three turns and
survives five or six of its turns.

## Generated characters

The stock face and walking sheets are exhausted (`NORTH.md` 4.6), so new people
are made with the Character Generator, headless - `../CHARGEN.md` - and
installed into sheets of this game's own, named `Gen_*`:

    python3 build/art.py        # after adding a character to it, or changing a look

`art.py` lists each sheet's slots and hands them to
`../tools/chargen/install.py`, which writes the face, walking sprite, damage
strip, side-view battler and a split face into `img/`, and refuses any cell that
already holds somebody else. **Append to its lists; never move anybody**, for
the same reason ids are not renumbered. The images are committed like the rest
of the art, so the data build never needs the untracked stock generator parts.

| sheet | 0 | 1 | 2 | 3 | 4 | 5 | 6-7 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `Gen_People1` | Fizz | Norbert | Old Hollis | Dilys | Gideon | Dorothy | Mrs Ashbury, Walt |
| `Gen_People2` | Brother Quillon | Sir Dunstable | King Aldous | Rosamund | Mirabel | Toby | Hollowell, Meech |
| `Gen_People3` | Tobias Frayne | Perce Stagg | Ida Stagg | Clem Blagg | Mrs Blagg | Pargeter | Mrs Marchpane, Mordaunt |
| `Gen_People4` | Hollin Crake | Lucan Morrow | Thaddeus Rook | Silas Veyle | Kit Blackwood | Hester Vane | Mr Thurle, Mrs Ash |
| `Gen_People5` | Hubert Weir | Prioress Stope | Sister Bewick | Pemberton-Gore IV | Mr Ottershaw | Mr Gedge | Prewitt, Dean Fenwold |
| `Gen_People6` | the Mayor | Prime Warden Stannard | Mr Tibbs | Mrs Harbottle | Miss Fettle | - | - |

**The Sable Hart's five wear a borrowed hood.** The male body has no hood
among its parts, so `art.py`'s `BORROWED` lends the female `AccB p10` riding
hood to it under the same id, by rendering against a symlinked copy of the
stock generator with those files added. No male part used that id, so
nobody drawn before changed - `art.py --dry-run` said `unchanged` for all
twenty-four - and the editor, which has no male `AccB p10`, loads those five
settings files without the hood.

**`Gen_People1` is full**, and `Gen_People2` was opened by Hithermost; Fairholme
took 2 and 3, and the twelve shareholders round its table share stock faces;
Olde Evermore's Mirabel is 4, and its two Elders share `Actor3:0` and
`Nature:6`. Restwell's third speaking part, Dr Pike,
**shares `SF_Actor3:6`** instead - `story.FACES` records every such share and
the reasoning, and sharing is the cheaper answer whenever a character is a
single scene in one room.

A generated person who has to be *fought* needs an `img/sv_enemies/` image,
which the generator cannot make. `art.py`'s `ENEMIES` writes a stand-in cut
from the battler, and only if the file is not already there - so the real
art goes in under the same name and stays. `install.py artsheet` makes the
reference to draw it from, and Norbert's was drawn from one - so
`img/sv_enemies/Norbert_Pelling.png` is real art now, and a rebuild leaves it
alone.

The rest of `BIOS.md`'s cast have settings in `build/characters/` and are not
installed, because nowhere they live is built yet.

**Dorothy Markup is the first look drawn for this game rather than taken from
`BIOS.md`.** The bio gives Gideon a look and not his wife, so hers was built
the way `CHARGEN.md` says to - `swatches.py` for the two colours that mattered,
then `lineup.py`, then a screenshot of the room she stands in. Iron-grey hair
up, a plain dark dress, and **the same gold wire spectacles Gideon wears**,
which is the one deliberate thing in it.

## Conventions

* Every event is named for what it is, and the recruitable six are named after
  the character so `Merribell` is findable by grep.
* **A page appended below a ladder must require that ladder's terminal
  switch.** `Game_Event.refresh` takes the *last* page whose conditions hold,
  so appending is not the same as sequencing: a new page whose condition can be
  true while a page above it still owes the player a beat does not follow that
  page, it deletes it - silently, permanently, with no symptom but the
  character saying the wrong thing forever. Ott's three field pages were
  appended on a plaque count that is reachable on foot long before the works is
  asked for an airship, which shadowed her fabric page, her handover page and
  both of her beat chains and made the whole questline unreachable for anyone
  who read the field first. The fix is to name the switch that means "this
  character has nothing left owing" - for Ott, `SW_OTT_MATERIALS`, the last
  thing the flying chain sets - and require it on every appended page.
  Reordering is not a fix; it only chooses which ladder dies.
* Dialogue lives in `village.py` / `journey.py` next to the event that says it,
  not in a strings table - it is read far more often than it is reused.
* Colour codes in text: `\C[6]` for a speaker's name, `\C[3]` for a thing you
  just got, `\C[2]` for something ominous.
* **The speaker's name goes inside the message, not in a name box.** MZ's Show
  Text has a fifth parameter, `speakerName`, which draws the name in its own
  little window above the message and costs the line nothing - it is the
  engine's own answer to the width problem, and it is deliberately not used
  here. `\C[6]Speaker:\C[0] ` in front of the first line of each window is the
  look this game has settled on, and the eight-to-seventeen characters it costs
  are a price worth paying. Do not "fix" a long line by moving the name out of
  it; break the line.
* A line of dialogue is at most **47 characters** including the `Speaker: `
  that `say()` puts in front of the first line of every window - so a line by
  Councillor Fenn has thirty characters to play with and one by Hob has
  forty-two. Narration, which has no face beside it, gets 60. `say()` and
  `narrate()` measure every line and refuse to build one that would be drawn
  off the edge of the window, naming the speaker and how much is over; break
  it earlier rather than letting anything wrap it, because where a line breaks
  is the joke landing or not. Item and skill descriptions are prose, so
  `db.described()` wraps those onto the two lines the help window shows.
