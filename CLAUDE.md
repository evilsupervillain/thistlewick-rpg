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
the Inevitable does not want to be the Dark Lord; he is four thousand eight hundred
years into a renewable engagement he cannot get out of. Beat him and the Prophecy itself
unrolls to enforce clause twelve, and *that* is the real last boss.

Bram can take up to three of nine companions - ten, counting the secret one.
Each is a different answer to the same fight, so who you pick changes how
combat plays:

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
| Spare Cotterill | The Ninth | getting in anywhere: AGI, no DEF term, not being hit, a full-party revive, double gold | HP, DEF, ATK, and getting past his mother |

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

`ART-TODO.md` lists every picture Mike still owes the game - what, where, what size, and what it has to show - and what has been put in. Keep it current: a new row whenever a map edit or a line of text asks for art that no sheet has.

`AUDIT.md` is the queue in front of `SITES.md` section 4 and of the companion
quests: Mike's list of faces and dialogue that disagree with the game, worked
through one item per session. Its section 0 is the rule that decides every
fix - **only what is on the `live-rpg` branch is protected**; everything newer
is free to change, and what is published may only be repaired where the game
contradicts itself.

`QUESTS.md` is the queue for **the companion quests** - `COMPANIONS.md`'s
forty-nine, one step per session, in the order and with the rules it gives.
It decides where their code goes (one module per companion, `build/q_<name>.py`,
hooked into place modules the way `field.ott_field_pages()` is) and holds
this effort's id blocks, which are also below. Read it and **one** character's
section of `COMPANIONS.md`, not the whole design.

`TIMELINE.md` is the world's calendar and **the reference every dated or aged
line is checked against** - write a new date into it in the same commit as the
line. Two reckonings: the calendar is the elves' Third Age (the present is
2000, Bram's year), and anything the Prophecy says is in *contract* years, because clause
two defines "a hundred years" as whatever the Committee finds convenient. That
is how the Tower is 4,800 years old and #45 is alive.

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
`SW_HOB_BRYD`, `VAR_TROPES` (60 / 20 / else), `SW_BALLAD_DONE`, `VAR_BLUSHES`,
`SW_FF_GRADUATED` and `SW_MET_QUY`. Every one is additive: a new line here is a new block, and
nothing that is already in the tally comes out or gets re-voiced.

**The finale is not the end of the game any more** (`POSTGAME.md`, P4a,
October 2026). Three things in `build/postgame.py` hang off it, each by one
line in `journey.finale_event`:

* **G1's companion lines**, `postgame.companion_lines()`, go after Firstfield's
  block and before "Thistlewick struck clause twelve". There are ten
  `if/else` chains, one per companion, each over that companion's quest
  switches with the best line first, so that exactly one line per companion
  prints. Then comes the count on `VAR_COMPANION_STORIES`: one / N / all
  ten. `postgame.rol5_line()` sits inside the `SW_ROLAND_GONE` branch, after
  "who thinks about this one".
* **After THE END comes `postgame.hand_back()`**, not Return to Title: "The
  next morning there are still turnips.", recover all, and a transfer to
  Bram's house at the new-game start (Map 2, 8,8) with no fade, because the
  screen is already black. Then the screen fades in. The map interpreter
  carries on across the transfer.
* **Page 6, `postgame.grimspite_afterwards()`**, on `SW_WON`, is Grimspite in
  his chair with a kettle. It is appended after the empty page 5 and beats
  it, so the finale cannot come back on the throne, and the empty pages 2 and 5
  are byte for byte what they were. The cup sets `SW_GRIMSPITE_TEA` (214),
  which P4c's Quy reads. A page added to Grimspite after this goes *after*
  page 6, or it has to carry it.

**P4b put Thistlewick, the pension and Roland after it**, all in
`postgame.py` again and hooked by one line each from `village.py`,
`south.py`, `dunnage.py` and `q_roland.py`. Two things in it are patterns:

* **`postgame._owing`** is how a post-game page goes on top of a ladder whose
  terminal switch the post-game cannot wait on (NIX-4's owners, NIX-3's door,
  Ysolde). The page is appended, so it wins; it asks, with the engine's own
  `meetsConditions`, which page the ladder below would have shown, and if
  that page still owes the player a beat it plays it word for word instead.
  Nothing is shadowed, and nothing is reordered.
* **Roland comes back through `story.recruit`'s own returning page**, on
  `SW_WON` and `SW_ROLAND_GONE`, with a "with you" page on `SW_RECRUIT` and
  `SW_ROLAND_BACK` after it. `SW_ROLAND_GONE` stays on for good; the tower
  door's last page is keyed on it and is the door without the departure, so
  he never leaves twice. Before the ending that page is the same door.
  `hand_back` clears `SW_ROL5_ON` for anyone who told Maud, so that her
  telling after the ending (on `SW_ROL5_ON` and `SW_WON`) is shown only while
  it is owed.

**P4c made the tally a function**, `journey.tally(amended=False)`, which
returns `(at, commands)` from "THE OBLIGATORY QUEST" to the walk to Quy, `at`
being clause twelve, where Hollowell's line is spliced. The finale calls it
with nothing and its pages are byte for byte what they were. **Prophecy Hall's
lectern** (Map 3 event 15, `postgame.account_event`) calls it with
`amended=True`: the same account against the game as it stands, headed "as
amended", Hollowell's line read off `SW_VISITORS_BOOK` rather than a page,
ROL-5 told late and Roland back in `postgame.rol5_line(True)`, and
`postgame.amended_lines()` before clause twelve, which is **where P4d-P4e's
lamp and Stair go**. It ends "The account ends there, for the present"
rather than THE END. A new line for the tally goes in `tally()`, and both
readings get it. `SW_VISITORS_BOOK` still means "signed at the top": after
the ending Hollowell's tour stops short of the slip and gives the notice of
termination instead (`postgame.hollowell_pages`).

**P4d opened the Door into the Mountain** (`mountain.py`, Maps 73-77). After
the ending Sir Dunstable lends the lamp (item 75; his pages 2-3, Map 34 event
4, self switch B) and the Door - on Hithermost's map and on the world map -
has a page on the item after its published refusal. Behind it is the Stair,
five maps of rock cave, each a plan of boxes in `mountain.PLANS` that
`check_plans` floods before the build is allowed to write it. **Two things
are switched by tags in a map's note, not by switches**, so leaving cannot
forget to turn them off: `<lamplight>`, the dark with a circle of light round
the party, and `<continuance>`, a random encounter lost there sending the
party back in through the chapel porch instead of to Game Over. Both are
`js/plugins/TOQ_Mountain.js`, the game's own plugin, registered by
`build_game.py` with `rmmzdata.upsert_plugin`; the porch is **common event
7**, `mountain.continuance()`, which a scripted fight's lose branch calls
itself (the warden's does). Only a battle with no event behind it is
overridden. Dunstable's chalk marks are `!Chalk`, one numbered frame per mark,
and `!$Half_Way` the carving - `python3 build/mountain.py` redraws both. The
bottom of the Stair is P4e's: until then, past D. 212 the party turns back.

Anything that runs the finale's list directly must skip code **201** as well
as 354, or the run lands in Bram's house. Both harnesses (`finale_ending`'s
`SKIP_SLOW` and `premises`') do.

**Two counter thresholds are cut against totals, and were last re-cut in
September 2026** (`SITES.md` section 4), once every site on that list was built
and the totals had stopped moving. Anything that adds a `story.trope()` or a
`story.blush()` site later has to come back here; the reasoning is in the
comments above both branches in `journey.finale_event`.

`VAR_TROPES` is **60 / 20** against about ninety-two reachable - 122 code-122
writes to variable 2 across 107 events, less repeat pages and branches that
cannot both run. **The two tiers are different kinds of number, so only one
moved.** Twenty is the player who goes straight north, a fact about the
critical path, and no site is on it. Forty was two thirds of about sixty, and
at forty of ninety-two "very nearly all of them" went to a player who had not
opened one new door; sixty is two thirds again. (What the world map's sites
added: Firstfield eight; Hithermost four - the sign, the villager, Sir
Dunstable and Quillon - Fairholme three, the King, Rosamund and Mrs
Emberthwaite, Olde Evermore two, the ARRIVALS sign and Mirabel's biscuit,
Gladhollow four - Toby, Granny Wendle's barrels, the key under the pot and the
bookcase - the Former Premises one, Hollowell's tour, the seven with no map
five - the Sky Anvil, the hedge mages' secret order, the Wrong Dragon, Mother
Selvidge's reading and the bell under Ashcombe Lake - Tobias Frayne one, his
eleven, Frostwick three, the town sign, Pargeter and Perce, Coldbarrow one,
Mordaunt's nine files, the Sable Hart one, five doomed rivals being fair about
seating, Sump one, the cursed village, Ashcombe one, the plaque, Weeping Bottom
one, the founder's stone, Fenmarch Hall one, the portraits whose eyes follow
you, the Collegium Arcanum one, REFERATUR, and Great Dunnage one, the watchman
who has never heard of you.)

`VAR_BLUSHES` is **26**, four fifths of **thirty-two** reachable - thirty-four
until October 2026, when Hob and Bryd's meeting and spar afternoon stopped
being blushes (`NORTH.md` 1.6). The 34 was
proven by scenarios, each of which walks a moment and then asks again:
`blushes` 11, `clanging_cast` 8, `two_hundred` 5 and `hob_and_bryd`'s spar
afternoon 1, which are the twenty-five of August 2026; then Dorothy Markup in
Penultima, Walt's tune and the register in Restwell, the Book in Hithermost's
chapel, Rosamund's card, Mirabel's secret, Frostwick's two - Ida on the ribbon
and Clem at the committee's table - and Cotter Cotterill in Great Dunnage, who
is always very glad to get home. `NORTH.md` 2.3 says why a grep of `data/`
over-counts it.

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
                     which is exactly why `TILENAMES.md` exists. Several
                     `IN_*` names lie badly (`IN_TABLE_ROUND` is a broken
                     table, `INC_ARMOR_STAND` a doll); a room that means a
                     table, stool, barrel, clock, piano, organ or altar uses
                     the "Inside furniture, by name" block instead
      handdrawn.py   maps drawn by hand in the editor, kept: `freeze <id>`
                     copies a map's tile layers into `build/handdrawn/`, and
                     its builder loads them with `handdrawn.load()` and adds
                     its events as usual. **Maps 2, 4, 9, 10, 13, 14, 17, 18,
                     21, 23, 27, 32, 36, 41, 44, 45, 51, 65, 67, 68, 69 and 72
                     are frozen** - Bram's House, the Gilded Turnip, both
                     Gloamwood maps, Nether Sopping, the Slain Wyvern and its
                     upstairs, Number Forty-Five's cottage, the lighthouse
                     (six floors side by side, `south.LIGHTHOUSE_FLOORS` wires
                     the stairs), Upper Clanging, the Safety Valve, the Wreck,
                     the Eight Hours, Rosamund's tower, the Mayor's House,
                     Frostwick, the Eleven Days, Sump, the Bell, Under Carn
                     Drey, Much Pottering and the Gotobeds' cottage (two
                     floors side by side, `pottering.STAIRS_UP` /
                     `STAIRS_DOWN`) (Mike, October 2026). What he redrew in
                     them is the house style for every map that is still
                     generated: the ground in Outside_A2's "(Dirt)" row so it
                     blends (`mapkit.GRASS` and friends), a chimney beside a
                     house rather than in its roof (`Canvas.chimney_beside`),
                     lamps on their feet (`mapkit.LAMP` is three cells), no
                     `Waterfall D (Boulder)` scattered as "reeds", and caves
                     with ragged rooms and dark beyond the rock
                     (`mapkit.naturalise_cave`). Rooms that share a map
                     (floors side by side, a back room in the black) are far
                     enough apart that none shows from the edge of another -
                     a 17x13 screen, so about ten columns of black; Maps 3,
                     14, 18, 41, 53 and 63 were widened for it.
                     To change one: edit in the editor, `python3
                     build/handdrawn.py freeze <id>`, rebuild - a rebuild
                     without the freeze throws the edit away. `widen <id> <x>
                     <n>` inserts n black columns at x in a frozen file; move
                     the builder's width and the events east of x to match.
                     The build's post-passes skip frozen maps.
                     `handdrawn.py check` says whether data still matches
      darkwood.py    the Gloamwood's dark-forest style as a kit - `Forest A`
                     as a wall, trunks along every north edge, undergrowth,
                     dressed trunks - drawn from a character plan. Map 10,
                     the deep wood, is drawn with it (`journey.DEEP_PLAN`)
      db.py          the whole database
      village.py     Maps 1-7: Thistlewick and its interiors
      journey.py     Maps 8-12: overworld, Gloamwood, the Obligatory Tower.
                     **Map 8 is a file, not a drawing** - `world_map()` loads
                     `build/worldmap/worldmap.json` and adds this game's
                     header and events to it. It is on tileset 8,
                     `mapkit.TS_OVERWORLD` - tileset 1 with Fenmarch Hall's
                     stamp recoloured; `worldmap.json` stays on tileset 1
      tower.py       the Obligatory Tower's floors (Mike, October 2026): four
                     floors side by side on Map 11, black between them like
                     the lighthouse, each drawn from a character plan, and the
                     summit, Map 12, the fifth. A flight up comes out above
                     itself on the floor above (the plans assert it), so the
                     stairs are in a different place on every floor.
                     `journey.tower_events` asks `tower.at(floor, letter)`
                     where each event is. Maps 11 and 12 are frozen since
                     his edits of 19-20 Oct (a black border, every floor
                     rounded and walled, the barred door moved to floor 4's
                     south hall, the summit's stair to its south wall); all
                     the plans were read back off his tiles, so a frozen-map
                     edit that moves a room or a stair means updating its
                     plan to match
      south.py       Maps 13-18: Nether Sopping, the Slain Wyvern, the Guild,
                     the outfitters, #45's cottage, the lighthouse. **The
                     Wyvern's patrons sit at tables**: `WYVERN_SEATS` is who
                     sits where and faces which way, and the tables are laid
                     round it (`IN_TABLE_TOP`, the A2 table, Mike's choice);
                     the dinner's eleven use `places.WYVERN_DINNER`
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
      mountain.py    Maps 73-77: the Stair behind the Door into the Mountain
                     (P4d) - five plans of rock cave, Dunstable's chalk marks
                     and the art for them, the warden, the porch (common event
                     7), and the lamp and Door pages `hithermost.py` appends;
                     and Map 78, the bottom (P4e): the lit chamber, its
                     lamps, and Something Unscheduled
      penultima.py   Maps 29-30: Penultima and Ye Final Shoppe, and the
                     **real** door events on Map 8 that replace the two
                     placeholders worldmap.json ships for that site. It is the
                     first of the new world map's twenty-nine sites to have a
                     room behind its door, and the shape every other one
                     should copy - `WORLDMAP.md` 7.6
      supplied.py    the faces Mike drew, from `build/supplied/`, into
                     `img/faces/Supplied.png`. Not part of the data build;
                     run it when a portrait is added. Append, never move
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
      build_game.py  runs all of the above, then the post-passes over every
                     interior: `new_tables` (every `Table D`/`Table A` becomes
                     the A2 table Mike chose, joined where tables touch;
                     `KEEP_OLD_TABLES` opts a map out), `shape_wall_tops`
                     (the tops' edge shapes, and `shape_faces`, the faces'
                     trim the editor's way), `match_windows` (an
                     interior's south wall gets the windows its building
                     has on the street), `dress_shut_doors` (every event
                     `story.shut` marked gets its door sprite on every page,
                     appended ones included, and stops being Through),
                     `door_holes` (a dark doorway under every door sprite),
                     `cast_shadows`; then System.json
                     and MapInfos. A room that splits off a bedroom uses
                     `mapkit.guest_room`; stairs between floors are
                     `mapkit.stairs_up` below and `mapkit.stairwell` above
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
| Class 11 | Cataloguer (Published), Wren's upgrade from WRE-1, by Change Class |
| **Spare** | `SPARE.md`, `QUESTS.md` F1, `q_spare.py`, `db.build_spare`: **Actor 11**
  Spare, **Class 12** The Ninth, **Skills 150-155** his and **146-149** his
  mother's, **States 42-43** They Never Hit Me and Brushed Through, **Enemy 28**
  Mrs Cotterill, **Troop 29** A Discussion With Mam, **Weapon 34** A Bag, Packed,
  **Armor 27** A Washer, Off Shim, **Items 33-34** Form P-9 and the washer,
  **Common Event 4** what Temper Tantrum costs him, **weapon type 13** Bag,
  **armour type 14** Washer, **element 10** Temper - his tantrum's, which his
  mother alone is immune to. **SPA-1** (`QUESTS.md` F2): **Item 73** Spare's
  Copies and **Common Event 5** that reads them, **switches 208-209** done and
  the dinner hour, **variables 28-29** letters posted and which town each went
  from (one decimal digit per town); the courier is `Gen_People14` 6 and is
  the last event on each of Maps 13, 31, 38, 40, 42, 44, 52 and 58, and the
  dinner hour is Map 22 event 10. **SPA-4** (`QUESTS.md` F3): **switch 210**
  done and **variable 30** Effie's tour (1 the volcano, 2 the pond, 3 the
  post, 4 done), on **Maps 68-69**, Much Pottering; Effie is `Gen_People14` 7
  and the rest of the village `Gen_People15` 0-3. **SPA-2** (`QUESTS.md` F4):
  **switches 211-213** Cotter has asked, the paddle clear, done, and
  **variable 31** the party set aside while Spare is in the culvert alone
  (an array; 0 otherwise), on **Map 70**; Cotter's pages 5-6 (Map 61 event 12).
  **The post-game** (`POSTGAME.md`): **switch 214** `SW_GRIMSPITE_TEA`, Bram
  had the cup at the top (P4a); Grimspite's page 6 (Map 12 event 2). P4b:
  **switches 215-218** been in Fitch's cottage, Roland rehired after the
  ending, ROL-5 told after it, the sword out of Carn Drey handed on; **item
  76** A Key, Labelled (75 is P4d's lamp, still free); **Map 71**; the
  letter is Map 2 event 8, the frame and the minute book Map 3 events 13-14.
  P4c: the amended account is Map 3 event 15; Quy's afternoon is his pages
  3-5 (Map 17 event 2, self switch B) and Hollowell's notice his pages 2-3
  (Map 42 event 2, self switch B), with the visitors' book's page 1.
  P4d: **item 75** The Lamp (Borrowed); **switches 219-221** through the
  Door, back in through the porch, the warden told; **common event 7** the
  porch; **Enemies 60-64** the Stair's scheduled hazards, **Troops 55-60**
  (59 is the warden, met, not random; 60 runs one past the companion block),
  **Skills 185-190**; Dunstable's pages 2-3 (Map 34 event 4, self switch B),
  the Door's pages 1-2 (Map 33 event 6, and its world-map event); **Maps
  73-77**. P4e: **switches 222-223** Something Unscheduled fought, its bounty
  discharged on Form Z; **items 77-79** the bounty card, the same card
  stamped, the Guild Card (not provisional, swapped for 27); **enemy 65**,
  **troop 61**, **skills 191-194**; **Map 78**; Pell's pages 3-5 and the
  board's page 2 (Map 15 events 2-3), the schedule's page 1 (Map 73 event 9) |
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
| Maps 13-18 | Nether Sopping and its interiors, and the lighthouse. MER-3
  widened Map 14, the Slain Wyvern, from 25 to 37 columns for its back room,
  where the Healers' Table meets, in its black east; Mike made it a cellar
  in October 2026 and widened the map to 39 (`places.WYVERN_BACK_*`) |
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
  module - not by the data build - with every pin placed by site name.
  Running it also writes `Coldbarrow_Map_AtLarge.png`, the same map with
  Aldric's nine red pins out of it, which the great map shows after ALD-3 |
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
  alias is `ASH`. COR-1 widened Map 53 from 26 to 36 columns for a third room,
  Corvin's old bedroom that is a study, in its black east (`places.STUDY`) |
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
  a character sheet drawn by running the module, like Fenmarch's, and so is
  the court's tileset: Map 58 is on tileset 7, `mapkit.TS_COLLEGIUM`, whose C
  sheet has the purple roofs and spires the door describes |
| Maps 61-65 | Great Dunnage: the town inside its wall, with the haulage yard
  in its north-west corner; the Smiths' Hall; the Counting House's lobby,
  which is mostly door; the Bonded Warehouse; and the Bell. `dunnage.py`,
  `SITES.md` step 18, the last. `MAP_DUNNAGE`, `MAP_SMITHS_HALL`,
  `MAP_COUNTING_HOUSE`, `MAP_BONDED`, `MAP_BELL` - **not `MAP_WORKS`,
  `MAP_FORGE` or `MAP_INN`**, which are Upper Clanging's and Thistlewick's.
  Its `journey.py` alias is `DUN`. Nix's refusal is on the warehouse's own
  door, not the town's |
| Maps 66-79 | **companion quests** (`QUESTS.md` 0.6): new maps in no existing
  place - ROL-2's dungeon, SPA-2's tubes, COR-2's drowned street. A new room in
  a built place is drawn by that place's module, on its own map where it can be |
| Map 66 | Old Ashcombe, the drowned street under Ashcombe Lake, for the week
  it is let down (COR-2). Drawn by `q_corvin.py`; `places.MAP_DROWNED_STREET`.
  In from the lake's world-map cell, out to `places.LAKE_SHORE_STEP` |
| Map 67 | Under Carn Drey, the dirt cave under the hill east of Great Dunnage
  where Roland's prophecy puts the stone and the Worm (ROL-2). Drawn by
  `q_roland.py`; `places.MAP_CARN_DREY`. In from the cave event at
  `places.CARN_DREY`, there once the party has gone to see; out to
  `places.CARN_DREY_STEP` |
| Maps 68-69 | Much Pottering and the Gotobeds' cottage, which was worldgen's
  Village 1 - the last placeholder on the world map (SPA-4). A place, so drawn
  by its own module, `pottering.py`, with Effie's tour and the courier from
  `q_spare.py`; `places.MAP_POTTERING`, `MAP_POTTERING_IN`. In from the two
  stamped cells (60,61)-(61,61), events 68-69 on Map 8, where the placeholders
  were; out to `places.POTTERING_STEP` |
| Map 70 | The Bottom Lock: the brick culvert under the bottom gate of the
  Dunnage cut, which Spare goes into alone (SPA-2). A map in no place, drawn by
  `q_spare.py`; `places.MAP_CULVERT`. In from Cotter's page, by way of the
  basin's south end, `places.CULVERT_STEP` on Map 61, where the party waits;
  out by the ladder it arrives under, to the same cell |
| Map 71 | Ambrose Fitch's cottage in Nether Sopping, behind the shut "A Front
  Door" (Map 13 event 15), which clause nineteen's key opens after the ending
  (P4b). Drawn by `south.fitch_map`, its events from `postgame.py`;
  `places.MAP_FITCH`. Out to `places.FITCH_STEP` |
| Map 72 | The Slain Wyvern's upstairs, where the beds Dorcas sells are (October
  2026: the building is three rows of wall from the street). Drawn by hand
  by Mike and frozen; events in `south.wyvern_up_events`;
  `places.MAP_WYVERN_UP`. In and out by the stairs in the bar's north-east
  corner, `places.WYVERN_STAIRS` - Mike's, and the model for any other
  staircase (`../TILES-AND-ASSETS.md`) |
| Maps 73-77 | The Stair, behind the Door into the Mountain (P4d): `mountain.py`,
  `places.MAP_STAIR`, children of Hithermost in the tree. Rock cave on the
  Dungeon tileset, one map a few hundred feet of descent, each in by a flight
  at the top and out by one at the bottom. Their notes carry `<lamplight>` and
  `<continuance>`. In by the Door with the lamp to (19, 2) on Map 73; out at
  the top to `mountain.DOOR_STEP` on Hithermost. Map 77's way down goes on
  to Map 78 |
| Map 78 | The Bottom of the Stair (P4e): `mountain.py`, `places.MAP_BOTTOM`,
  plan 5 of `mountain.PLANS` (`mountain.MAPS` is the six), a child of Map 77.
  Lit, so its note is `<continuance>` alone; no encounters. Something
  Unscheduled is event 3; win or decline, it sends the party up to
  `mountain.DOOR_STEP` |
| Map 99 | the tile sampler, not part of the game |
| **Firstfield** | fresh blocks, because `SPARE.md` has spoken for the free ends
  of the north's (Enemy 28, Troop 29, Weapon 34, Armor 27, Items 33-34, Skills
  146-155): **Armors 30-32** A Stick, A Straighter Stick, Certificate of
  Completion; **Skills 160-161** Telegraph, Enormous Swing; **Enemy 40**
  Norbert; **Troop 40** Norbert (Tutorial) |
| **Companion quests** | reserved by `QUESTS.md` 0.6, taken in queue order and
  written down here as they are: **Items 40-79**, **Weapons 40-54**, **Armors
  40-59**, **Enemies 41-69**, **Troops 41-59**, **Skills 170-189** (their
  enemies'), **States 40-44**, **Common Events 3-10**. A skill a quest teaches
  goes in the free end of that companion's own block. Spare keeps `SPARE.md`'s
  Enemy 28, Troop 29, Weapon 34, Armor 27, Items 33-34 and Skills 146-155 |
| **Mothballs** | the playtest round's P1 (`QUESTS.md` Part G), `db.build_mothballs`:
  **Item 74** Mothballs, 30 gold, at the Emporium, the Chandler's, Wick &
  Barrow and the Parish Rooms; **State 44** Mothballs, Encounter None until
  it is walked off after 50 steps; **Common Event 6** using one, and
  **variable 32** when one was last used - 25 steps of airing after it wears
  off before another will take. A Repel: it is a state because a transfer
  re-rolls the encounter count, and it stacks with Nix's half |

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
| 89-92 | **Spare** (`QUESTS.md` F1): 89 `SW_SPARE_FORM` Gudgeon has issued Form
  P-9, 90 `SW_SPARE_JOINED` (also `SW_RECRUIT[SPARE]`), 91 `SW_SPARE_REFUSED`
  the argument lost at least once, 92 `SW_SPARE_KNOWN` (also `SW_KNOWN[SPARE]`).
  `SPARE.md` says 72-74, which are `SW_KNOWN`'s. He is in those dicts and
  **not** in `story.COMPANIONS`: no form desk can strike him off |
| 93-100 | unallocated |
| 101-109 | `SW_<NAME>_STORY`: Merribell, Hob, Zephyrine, Nix, Aldric, Piper,
  Corvin, Wren, Roland have had a companion quest of their own finished - same
  last digit as 11-19 and 72-80. Set only by `story.companion_story`, which also
  counts variable 15. The ending reads one block per companion off these
  (`COMPANIONS.md` 1.4), not one per quest. 110 is Spare's |
| 111-250 | companion quests, taken in `QUESTS.md` order; each step's Done
  paragraph names its own |

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
| 15 | **companions who got a story of their own** - how many of the
     `SW_<NAME>_STORY` switches are on. Bumped only by `story.companion_story`,
     the first time each one goes on; the ending's closing line reads it |
| 16-30 | companion quests, reserved, taken in `QUESTS.md` order |
| 31 | SPA-2: the party, set aside while Spare is in the culvert |
| 32 | **`$gameParty.steps()` when a twist of Mothballs was last used** - the
     airing: another is given back until 75 steps after (`db.build_mothballs`) |

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
| `tower_climb` | every flight in the tower climbed with the arrow keys and come
  back down, each landing above itself; through the barred door to the head
  of the summit's stairs, and back down in front of the door |
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
| `p3_evermore_elves` | `QUESTS.md` P3: Olde Evermore's six elves about
  doing things, each walked to and talked to twice with its face asserted off
  the message - Thalion, Ninian's route asserted to move and to keep to the
  west path, Aelwen (the trope, counted once), Elowen's tea cosy before
  Mirabel's secret and after it, Calder, and the copyist, asserted to say
  nothing about the horse |
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
| `audit_fixes` | `AUDIT.md`'s fixes to published places, off the live game:
  **Thistlewick's gossip walks and talks as `Gen_People6` 5** under her old
  "Villager:" label (G3, `NORTH.md` 8.1c), and **the Chandler's in Nether
  Sopping is shut with the lamp out and a shop with it lit** (D3) |
| `wall_ring` | a room's walls are wall: at every wall of the Gilded Turnip and
  the Bell, and either side of each doorway, a step along the wall and then a
  push into it, asserted by position *and* facing so a dropped press cannot
  pass for a wall; the Turnip's washstand, walked to and pressed; and out
  through both doors. Fourteen of its checks fail on the data from before
  `shape_wall_tops` (`NORTH.md` 8.1f) |
| `supplied_faces` | the three faces Mike drew, `img/faces/Supplied.png`, read
  off the live message window: Nix in the back room, Mrs Emberthwaite and
  Somebody Large in the dark of the Wrong Dragon's cave - and Nix's actor,
  with the new face over her unchanged sprite (`NORTH.md` 8.1e) |
| `coldbarrow` | `SITES.md` step 11, walked: onto Coldbarrow's door off the
  world map, **the great map, which puts `Coldbarrow_Map` up as picture 1 and
  takes it down after**, Mordaunt and the nine pins (the trope, counted once),
  Mordaunt again, Mordaunt with Sir Aldric in the party - the reaction shot,
  asserted to offer nobody a promotion - the desk, the files, the committee's
  table, and back out onto `places.COLDBARROW_STEP` |
| `placeholder_doors` | that the world map has **no placeholder doors left**.
  It was 41 on 29 sites; the last two, Village 1's, became Much Pottering in
  `QUESTS.md` F3, and the walk onto them moved to `q_spa4_penpal`. What is left
  is the count at nought, and the six `<aironly>` assertions |
| `pg_home` | `POSTGAME.md` P4b, the morning after: the letter on the mat
  walked onto and read (the pension once, the key), Mother before and after
  it, the five villagers, Elder Wispel, the forty-eighth frame and the Wall
  walked to, the minute book's SEE BRAM, the Regular, the front door into
  Ambrose Fitch's cottage and everything in it walked to, and Ysolde - with
  NIX-4's, NIX-3's and Ysolde's owed beats each asserted to play first |
| `pg_account` | `POSTGAME.md` P4c: the lectern absent before the ending and
  there after it; every line of the finale's tally, read out of Map 12's data,
  in the amended account; walked to and read bare, then with each switched
  line, in order; Quy's afternoon both ways in, with and without the cup, and
  the pot next door; Hollowell's notice both ways in, and the signed book; and (P4d) the
  Stair's three lines, absent bare and between the tea and clause twelve,
  and (P4e) the bottom's two after them |
| `pg_mountain` | `POSTGAME.md` P4d: Sir Dunstable before and after the ending,
  never met (introduced, the trope, the lamp) and again; the Door with the
  lamp, in, in the dark but for it; the schedule; the first flight on foot,
  D. 2, down one map and back up; **the warden lost**, which is back through
  the porch restored with the lamp and no Quillon beat unsigned, and
  Dunstable knowing it; the warden won and out of the way; **a random
  encounter lost on the Stair** with the Book signed; D. 212 and past it;
  and **a battle lost on the world map still Game Over**. Its message window
  auto-advances (`_auto`) through speeches that end in a battle, which
  `advance` cannot do without playing the battle |
| `pg_bottom` | `POSTGAME.md` P4e: down past D. 212 to Map 78, lit and
  without encounters; Something Unscheduled met (the trope), "Not today" and
  seen up to the Door; back, fought and won (the card, the ride up); the
  schedule's "Anticipated."; a rematch with no second card; a loss to the
  porch; Pell refusing a non-member the card, then stamping it on Form Z and
  swapping both cards; the not-provisional page and its roster amendment; the
  board's third card; the account's two lines |
| `pg_roland` | `POSTGAME.md` P4b, Roland: he leaves at the door with nothing
  on and the door is then its own page; after the ending, rehired at his
  table in his own shield and shirt, struck off and back, up the tower and
  not called away, the drawn sword kept at the door, ROL-3 started, ROL-5
  told after the ending, his pitch with Maud's news, and ROL-4's mark with
  the sword handed back |
| `shut_doors` | **a door that does not open is a door** (Mike, October
  2026). Every one used to be Outside_B's `Large Window C`, which is shutters
  and read as a window, so `mapkit.DOOR_SHUT` is not a door and a new one is
  `story.shut_door`. Walked up to one of each kind - a push that does not go
  through, the action button, and the reason it gives - then every page of
  all twenty-nine, appended pages included, is a `!Door1` and solid |
| `blushes` | the whole of `NORTH.md` section 3, in one walk: room four, the
  house register, Sops, both travellers, Perpetua and Gerald, the fete
  minutes, the washstand, Wren's three specimens and the second notice at the
  Standing Stones. Every one of them is asked a second time and `VAR_BLUSHES`
  asserted not to have moved, and the last check is that the retrofit came to
  eleven - the number 2.3 asked for |

| `q_wre2` | `QUESTS.md` A1, WRE-2 The Second Plaque: the goose unchanged without
  Wren and the second plaque absent; with her, the ask (a trope, once), the
  engraving card at Wick & Barrow's without her and with her, too little money
  and then enough **paid without her** - the wording is left with Mrs Barrow -
  the plate carried past the goose without her and nothing happening, then the
  handover: `SW_WRE2_UP`, `SW_STORY[WREN]` and `VAR_COMPANION_STORIES` once,
  both plaques read, the goose again with and without her. The first companion
  quest, and the pattern for the rest |
| `q_wre5` | `QUESTS.md` A2, WRE-5 Bramus: the burrow in the turnip field absent
  without Wren - walked onto - and with her the naming (a trope and a blush,
  once each), `SW_WRE5_NAMED`, `SW_STORY[WREN]` and `VAR_COMPANION_STORIES`;
  then "Still here." with her and the label without her |
| `q_pip2` | `QUESTS.md` A3, PIP-2 A Rhyme For Turnip: the gilded turnip unchanged
  without Piper and before the road, her afternoon put off once, then two
  parties so each of the eight suggestion branches runs exactly once - a trope
  each, Bram's parsnip and the payoff, Merribell's blush - `SW_PIP2_DONE`, and
  `SW_STORY[PIPER]` counted once |
| `q_mer2` | `QUESTS.md` A4, MER-2 Fit To Travel: the Parish Notices unchanged
  without Merribell and clause eleven with her; the blank form used from the
  **real Key Items menu**, naming what is missing in order; the fish stall
  lending its scales without her and a shop again after; the examination
  played through with Sir Aldric as witness - three blushes, the certificate,
  `SW_STORY[MERRI]` - and the other seven witnesses through the common event's
  own list, fast. Long: run it in the background |
| `q_rol4` | `QUESTS.md` A5, ROL-4 The Maker's Mark: Beatrice unchanged without
  Roland or Hob, Roland alone at the forge, then both - the mark, "She did good
  work", Beatrice silent, **no line mentioning the hammer**, `SW_STORY[ROLAND]`
  once; then after the door, the sword **equipped on Bram**, the refit turned
  down and then done: the sword gone off his hands, the axe Hob's and nobody
  else's |
| `q_spa0_joins` | `QUESTS.md` F1, Spare's gate: his beats played, Shim's
  washer, **Gudgeon reading the three sections of Form P-9 one at a time** -
  heard in full, the family met (not Cotter), the airship - the form, the whole conversation with "Not
  yet", no room in his voice, and the Eighty-Four window; faces off the live
  window |
| `q_spa0_argument` | `QUESTS.md` F1, the argument fought for real with **Spare
  alone** on auto-battle: lost - no Game Over, the party put back, the trope
  once - then she stops at a quarter, she concedes and he joins, levelled to
  the party with The Drawing and the washer on him; the same face, sprite and
  battler as the doorstep; the bag sealed in his hand; a shot of the fight |
| `q_spa4_penpal` | `QUESTS.md` F3, Much Pottering and SPA-4: in by the world
  door that was Village 1; without Spare, Effie at her gate and nobody on the
  tour, the plaque's trope once, and the four things you walk into (the wet
  fence, the pig, the oak, the well); with Spare, the courier's "she is right
  there", the meeting and its trope, a dismissal mid-tour that she waits
  through, the volcano, the sea serpent and the post, done; the afterwards
  pages, the second wish, the cottage, and out by the road |
| `q_spa2_tubes` | `QUESTS.md` F4, SPA-2 Ninety Tubes: Cotter without Spare
  is today's pages; with Spare and Hob, HOB-1's heel-irons carried first; the
  meeting and not now; the short ask and down, `SPARE.md` 3's swap into Map
  70, the dark and the drips; up early with the party put back; down again and
  walked by key presses - the counting, a crown, Mr Pocock, the paddle; out,
  everybody there, the trope and the fee; afterwards with and without him |

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
| `Gen_People6` | the Mayor | Prime Warden Stannard | Mr Tibbs | Mrs Harbottle | Miss Fettle | Thistlewick's gossip | Elder Faelan, Elder Lirien |
| `Gen_People7` | Sister Pim | Sister Lamb | Mrs Liddy | Mr Crouch | Mr Oakes | Sir Hamo | Mr Nuttall, Mr Dace |
| `Gen_People8` | Watchman | Mrs Poskitt | Mr Plummer | Warden Crabbe | Town Clerk | Mrs Dewhirst | Mr Ambler, Miss Quayle |
| `Gen_People9` | Mr Tweddle | Dame Winifred | Bess | Alfie | Nell | Mr Gammage | Mrs Pardew, Mrs Garrow |
| `Gen_People10` | Dr Hapgood | Reader | Undergraduate | Ned | Granny Wendle | Wilf | Mrs Dimmock, the Commissioner |
| `Gen_People11` | Mrs Puddifoot | Tom | the raker (`Elf`) | Ivy | Hodge | Bagshawe | Mrs Lumb, Mr Dunmore |
| `Gen_People12` | Miss Pellow | Dame Florence | Brother Anselm | Mags | Pim | Odile | Old Jory, Septimus Dray |
| `Gen_People13` | Lettice Moon | Convenor Swale | Pennock | Professor Mott | Doctor Furze | Grizel Pennyfeather | Lucius Hobday, Nan Gilly |
| `Gen_People14` | Cuthbert Spence | Ambrosine Quill | Lorrimer | Maud | Spare | Cotter | the Courier, Effie |
| `Gen_People15` | Mrs Gotobed | Mr Dibble | Mrs Throssell | Mr Cobley | Thalion | Aelwen | Elowen, Calder |
| `Gen_People16` | Ninian | the Copyist | *free* | *free* | *free* | *free* | *free* |

**The Sable Hart's five wear a borrowed hood.** The male body has no hood
among its parts, so `art.py`'s `BORROWED` lends the female `AccB p10` riding
hood to it under the same id, by rendering against a symlinked copy of the
stock generator with those files added. No male part used that id, so
nobody drawn before changed - `art.py --dry-run` said `unchanged` for all
twenty-four - and the editor, which has no male `AccB p10`, loads those five
settings files without the hood.

**`Gen_People1` is full**, and `Gen_People2` was opened by Hithermost; Fairholme
took 2 and 3, and the twelve shareholders round its table share stock faces;
Olde Evermore's Mirabel is 4, and its two Elders were stock until
`AUDIT.md` item 3 drew them as elves on `Gen_People6`, which is now full;
`Gen_People7` to `Gen_People11` are `AUDIT.md` item 1's - a face, and a
sprite from the same file, for every human who spoke without one;
`Gen_People11`'s last five and `Gen_People12` to `Gen_People15` are the
companion quests'; Olde Evermore's six elves of the playtest round's P3 are
`Gen_People15` 4-7 and `Gen_People16` 0-1, and **the next face goes in
`Gen_People16` 2**. Restwell's third speaking part, Dr Pike,
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
* **A tile picture on an event is a tile for passage.** `Game_Map.allTiles`
  counts the tile of every event whose picture is a tile, through or not and
  whatever its priority, so a "below characters" letter drawn as `Envelope`
  (flagged blocked) sealed Bram's doormat. Something meant to be walked onto
  is a character sprite (`postgame.draw_art` cuts one from the tile).
  `validate.py` does not see it on a page that only exists later.
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
