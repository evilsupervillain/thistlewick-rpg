# The new world map

The 50x50 `Map008` rebuilt at **120x120**, generated with the workspace's
`tools/worldgen` and then finished by hand. It exists because the old map is
too small to hold the expansion: `COMPANIONS.md` wants eight new location
clusters and seven world-map-only sites, `BIOS.md` wants six more towns, and
the 50x50 was already crowded.

**Status: the map is built and reviewed, and is not installed.** It is
`build/worldmap/worldmap.json`, it stages cleanly, and nothing in `data/` or
`build/` points at it yet. Section 6 is the list of what a session picking this
up has to do.

    python3 build/worldmap/run_finish.py --stage 941   # rebuild and stage it
    python3 build/worldmap/review.py 941               # old map vs new, measured
    node ../tools/serve.js ../staging 8770 &           # then _probe.html?map=941

**What a session on this map needs to read, and what it does not.** The
workspace `CLAUDE.md` says to read `ROOMGEN2.md` and stop. **That instruction
is for a roomgen session and does not apply here** - this is a different effort
and reading it costs 9k tokens for nothing. Do not open `ROOMGEN2*.md`,
`MAPGEN.md`, `ROOMGEN.md` or `CHARGEN.md`; and **not `WORLDGEN.md` either**,
even though it is the document this map was made with, because the generating
is finished and the map is a file (7.6). What is wanted is the workspace
`CLAUDE.md` - its "Things that cost time to rediscover" list is the relevant
half - this game's `CLAUDE.md`, this file, and `MAPTOOLS.md` when a tool's
arguments are needed. `COMPANIONS.md` and `BIOS.md` are what the new sites are
*for* and are worth reading at section 6 item 10, not before.

---

## 1. What it is

**The old 50x50 is preserved inside it, not regenerated.** It sits at offset
**(35,35)**, so it occupies x 35..84 and y 35..84 of the new map, and every old
coordinate converts by `new = old + 35`. Its land came back byte-exact except
for two things that were changed on purpose: the one-cell ring where the old
ocean rim was erased and the new coast autotiled over it, and the two mountain
masses the World palette cannot name (section 5).

Around it, `worldgen.grow` generated new country with a **snowy far north**
(y < 32) and a **desert far south** (y > 100), which the 50x50 had no room for,
and twenty new anchored sites.

Four things were true of the specification and are worth not rediscovering:

* **Composition.** `sea 34, grass 32, snow 11, desert 11, wasteland 5, rocky 4`
  over the *filled* area. At 46% sea the new country came out as fragmented
  islands rather than a continent; 34% is what makes it read as one landmass.
* **No swamp.** `Poison Swamp` is a **damage floor**, and a 2% quota scattered
  450 cells of it wherever the allocator could fit them - including hard
  against Restwell. A swamp is a place, not a percentage. Draw one by hand.
* **The water is painted before anything is generated.** A layer-0 tile of 0
  means "generate here", so the canvas `grow2.py` builds - the old map blitted
  onto an empty 120x120 with ocean already drawn in - is itself a
  specification. This is the only way to say "there is sea *here*"; protecting
  the old map's own rim cannot do it, because the sea below Nether Sopping is
  new territory. See `PAINT_SEA` in `grow2.py`.
* **Seeds fail, loudly.** About half of any batch refuses - always a 2x2 stamp
  (a castle, a mansion, the Collegium) that cannot find four free land cells
  with its door on the right biome inside its region. That costs a re-run, not
  a bad map. `w7` is the seed that was chosen, from eight.

## 2. The files

    build/worldmap/
      grow2.py        the specification: the canvas, the painted sea, the
                      twenty new sites, the two grow passes. Produces
                      `generated.json`; re-running it re-generates the world
      generated.json  the template worldgen produced, seed `w7`. NEVER EDITED
      generated.meta.json   its sidecar: the spec it was grown from, and a
                      marker per site with the stamp and the door cell
      finish.py       the hand-pass operations: mend a coast, isolate a rock,
                      dig out a buried square, draw a range, restamp a town,
                      drown an islet. Nothing in here decides anything
      run_finish.py   the decisions. Always starts from `generated.json` and
                      writes `worldmap.json`, so every edit is a line of code
      worldmap.json   the finished map. This is what gets installed
      review.py       old map against new: which events changed access, which
                      sites are unreachable, what is stranded
      reach.py        the flood fill both of those use
      place.py        put the party and the airship somewhere they can stand

**`MapGrid.autotile` reproduces worldgen's own output byte for byte** - 0 cells
differ on a round trip, measured - which is what makes the hand pass safe.
Edit tiles, re-autotile layers 0 and 1, and nothing else moves.

## 3. Where everything is

Old-map places are at `old + (35,35)`. The doors that moved are marked.

| place | old | new | note |
| --- | --- | --- | --- |
| Thistlewick | (24,43) | **(60,79)** | moved: was astride the road |
| Nether Sopping | (36,44) | **(71,84)** | moved down onto its own shore |
| The Lighthouse | (41,44) | (76,79) | |
| Upper Clanging | (9,12) | (44,47) | |
| Gloamwood Mouth | (17,27) | (52,62) | |
| Gloamwood North Mouth | (17,20) | (52,55) | |
| Obligatory Tower | (31,8) | (66,43) | |
| everything else | | `+ (35,35)` | unchanged |

The twenty new sites, from `generated.meta.json`:

| site | at | stamp | for |
| --- | --- | --- | --- |
| Coldbarrow | (50,19) | Temple A (Snow) | ALD-3, ALD-2 |
| Hithermost | (30,23) | Village A | `BIOS.md` Brother Quillon |
| Sky Anvil | (76,26) | Giant Tree (Snow) | HOB-4 |
| Penultima | (82,48) | Town B | `BIOS.md` Gideon Markup |
| Great Dunnage | (31,52) | Fortress City | HOB-1, NIX-1/2, ALD-4, PIP-3, COR-5, ROL-1 |
| Sable Hart | (24,75) | House (Town) | COR-3, COR-4 |
| The Lay-By | (11,88) | **Igloo** | ZEPH-5 - and see section 4 |
| Olde Evermore | (30,93) | Village C | `BIOS.md` Mirabel |
| Ashcombe | (102,55) | Village A | COR-1, COR-2 |
| Collegium Arcanum | (112,38) | School of Magic | ZEPH-1/2/3, WRE-1 |
| Fairholme | (104,73) | Castle A | `BIOS.md` Princess Rosamund |
| Little Gore | (97,101) | House (Village) | ALD-1, MER-5, PIP-4 |
| Gladhollow | (33,111) | Village B | `BIOS.md` Toby Wendle |
| Restwell | (43,81) | Town A | `BIOS.md` Mrs Ashbury |
| Weeping Bottom | (58,99) | Temple B | MER-1, MER-3 |
| Fenmarch Hall | (86,114) | Large Mansion | ALD-1, ALD-5, WRE-4 |
| Cinder Fen | (47,118) | Trail | ZEPH-4 |
| The Fair | (67,115) | Large Tent | COR-4 |
| Sump | (78,102) | House (Desert) | MER-5, PIP-4 |
| Wrong Dragon | (110,114) | Cave B | ALD-6 |
| Village 1 | (60,61) | Village B | unclaimed - worldgen's own extra |

Each has a door event on it already, generated, with no destination. They are
**placeholders**: the transfer has to be written when the interior exists.

## 4. Settled, and why

**The Lay-By is an igloo on grass and that is deliberate.** It started as a
mistake - the site was drafted for the far north and then moved into temperate
country with its stamp still on it - and it is being kept, with a backstory
owed to it. ZEPH-5 is "three hedge mages, nine years, no name", which is a
better joke with an igloo in it than without. Do not tidy this away.

**The mountain fence is gone and a range is drawn in its place.** The 50x50 had
`MM.MM.MM` on a fixed period across rows 23-30, which reads as a fence. It was
erased and regenerated, and came back as **open grass with no mountains at
all** on three of four seeds - structural, not bad luck: relief follows stage
1's ridges and a 460-cell hole in the middle of a preserved continent has no
ridge in it. So the range is hand-drawn instead, along a polyline with its
thickness from a noise field, and it runs **between the Gloamwood's two
mouths** so the tunnel pierces it rather than sitting beside it.

**The road network is in eleven pieces, and that is accepted for now.**
Measured on the finished map by flooding the `Road (Dirt)` and `Road (Paved)`
autotiles: eleven separate networks, the largest 148 cells. The big one is a
gap at y 56-61 where the old 50x50's north road used to run - the middle redraw
erased it and the hand-drawn range now stands in it - so Thistlewick's network
(57 cells, reaching Nether Sopping) does not join the Tower's (70 cells,
reaching Upper Clanging). That is mostly the intended geography rather than a
fault: the two are joined *through the Gloamwood*, whose mouths at (52,62) and
(52,55) sit either side of the gap, which is what section 4 means by the tunnel
piercing the range. **Settled: not a blocker.** Roads are cheap - `put_road` is
four lines - and the places that need joining will declare themselves while the
campaigns are written. Fix them then, not now.

**The forest corridor stays open, and so does the long way round.** You can
walk from Thistlewick to the Tower without entering the Gloamwood. That was
already true on the 50x50 - there is an open corridor at x11..24 - and it is
deliberately left alone: it makes testing easier and will be closed some other
way later. Walking all the way round the range to approach the Tower from the
north is also allowed; it is simply much further.

**Three settlements were drawn wrong in the shipped game**, and the new map
fixes all three. They were not obvious until the world had a climate:

* Thistlewick was `Fortress City` - a walled city, for a turnip village. Now
  `Town B`, and moved off the road column it was standing on, with a road spur
  along its northern edge, which is the side the gate comes out on.
* Nether Sopping was `Fortress City (Snow)` in the temperate south. Now
  `Town A` on the last row of land with **one** `Pier (V)` on the sea tile
  directly below it - which is the sample world map's own idiom, `Map001` at
  (105,121). No run of jetty, no gap of beach.
* Upper Clanging was `Fortress City (Snow)` on grass. Now `World_C/Slum`, which
  is 2x2 - the same footprint - and reads as an industrial village.

**The 50x50 has two cells nobody can reach**, at (6,27) and (9,27): single
walkable holes sealed inside the western mountain mass. Stage 4 refuses to
build on a map with those in it, so `grow2.py` walls them up (`SEALED`). Both
are inside the band that gets redrawn, so they are gone either way.

## 5. What was found in the tools

Four faults in `tools/worldgen`, all fixed, **none committed yet**:

* `climate.py`, `allocate.py`, `preserve.py`: `np.unique` on a label array
  containing `None` raises `TypeError`. It fires the moment a source map has a
  cell worldgen cannot name, which Thistlewick's `Map008` has **96** of -
  `Mountain (Rock)` over `Sea`, the Tower's massif and the western mass. Fixed
  by iterating a `set` instead.
* `spec.py`: added `Region.box(x0,y0,x1,y1)` and `Region.near(x,y,r)`. The
  existing shapes were *anywhere / edge band / centre box / one exact cell*,
  and thirty exact cells is too much precision to claim - stage 5 has to stand
  a 2x1 town on land with its door on the right biome, and one named cell is a
  coin toss. Validation refuses a box entirely off the map.
* `stamps.py`: `SLOT_BASE["World_C"]` was **512**, which is `TILE_ID_D`;
  `rmmz_core.js` says `TILE_ID_C = 256`. Every World_C stamp's tile ids and
  passability flags were read 256 too high. It had never fired because W7
  measured that the corpus uses World_B for all 31 of its stamped doors and
  made it the idiom, so Upper Clanging's Slum is the first World_C stamp ever
  placed. **The failure mode is the quiet one**: the Overworld tileset's D slot
  is empty, so the wrong id is not a wrong building, it is *no building* - a
  blank patch of grass where the town should be, and nothing reported a thing.
  `selftest.py` asserted the wrong value outright; corrected against the
  engine's own constant. Full selftest: 0 failures.

## 6. What is left to do

In order. The first five are the map; the rest is the game.

1. **The Lighthouse's own geography.** It sits on flat coast rather than a
   headland. Cosmetic, and the one piece of section 4's settlement work that
   was not finished.
2. **The sites still to place, and the four that are sited wrong.** Section 7
   is the list: four places the design documents ask for and the map has not
   got, four whose bios assert a geography the map does not honour, a snow
   town the far north has no substitute for, and one floating continent. All
   of it is hand-stamp work in `run_finish.py`, and it comes before the region
   layer because regions are painted over a finished map.
3. **The region layer.** A generated map has none, and `Map008`'s
   `encounterList` keys off `regionSet` 1-4 - so **the new world has no random
   encounters anywhere**. Paint regions by biome; the sidecar has every cell's
   biome. Remember that region 1 painted over a map reads back as tile 1, which
   on some sheets is a real tile.
4. **The three air-only rocks.** The Isle of Uncertain Ownership (55,83),
   Attempt 112's sea stack (37,40) and the Middle Distance (82,65) are the only
   three walkable places off the mainland, which is correct, but their events
   are not on the map. Re-place them per `places.py`'s rules: player-touch,
   below characters, one bare square each for the airship.
5. **A pass with `propsheet.py`** over the finished map, per the workspace
   `CLAUDE.md`: a map-scale screenshot does not tell you what a prop is.
6. **`places.py`**, rewritten: every constant in it moves by (35,35) except
   Thistlewick and Nether Sopping, which moved further. Section 3 is the table.
   **This is also how every exit back onto the world map gets fixed.** Measured
   on the shipped data: **thirteen `Transfer Player` commands across twelve
   maps** name Map 8 as their destination, and every one of them is a hardcoded
   old-50x50 coordinate - Thistlewick's North Gate to (24,45), both Gloamwood
   mouths, the Tower door, Nether Sopping's North Road, the Lighthouse, the
   Pit, the Barrow, Upper Clanging's South Road, the Long Field, the Crag, and
   Firstfield's Way Out twice. None of them is written out: every one is
   `R.transfer(MAP_WORLD, *WORLD_SOMETHING_STEP)` or `WORLD_SOMETHING[1] + 1`,
   so this is one file and a rebuild rather than thirteen hand edits. Three
   things stop it being a `+35` sweep:
   * **Four do not move by 35.** Thistlewick, Nether Sopping, Upper Clanging
     and the Lighthouse were all restamped and re-sited by section 4; their
     exits have to be re-derived from section 3, not offset.
   * **The `+1` convention breaks for two of them.** Several exits are written
     as "one square south of the door" - `WORLD_PIT[1] + 1`,
     `TOWER_DOOR[1] + 1`, `WOOD_MOUTH[1] + 1`. But `run_finish.py` gives
     Thistlewick and Nether Sopping road spurs to their **north**, which is the
     side the gate comes out on now, so both of those exits move to the other
     side of the building. A blind `+1` puts Thistlewick's gate in the water.
   * **Every destination needs the standable check** - `flags & 0x0F == 0`, per
     7.6 - and not merely a translated coordinate. The coast mend, the
     hand-drawn range and the islet drowning all changed terrain that old
     constants stood on.

   And one entanglement that says why item 7 has to happen alongside this one
   rather than after it: `wilds.py` has `first_coast = WORLD_VILLAGE_STEP[0] +
   2`, which is *drawing* code deriving a coastline from a place constant. The
   coordinates and the drawing are not cleanly separated.
7. **`journey.py` loses its world map.** Map 8 is currently *drawn* by code -
   roads, coastlines and scenery placed by hand-written coordinate, with hooks
   in `wilds.py`, `field.py` and `meadow.py`. All of that drawing goes; those
   modules keep only their events, placed onto the generated map. This is the
   largest single piece of work here and it is much larger than the map was.

   **"Keep only their events" is not the whole instruction, because a lot of
   the world's furniture is tiles.** Roughly **seventy-four layer-2 and
   layer-3 tile writes** across `wilds.py`, `field.py`, `meadow.py` and
   `journey.py` put down huts, signs, rocks, cave mouths, trees and tower
   icons by hand-written coordinate - `K.WB_HUT`, `K.WB_SIGN`, `K.WB_ROCK`,
   `K.WB_CAVE_DARK` and the rest. None of them is an event, so a pass that
   preserves the events and deletes the drawing deletes all of them silently.
   Each one has to be re-placed, either as a `put_tiles` line in
   `run_finish.py` or as a hook that survives.

   **The Hermit's hut is the worked example, and it is already gone.** It is
   `wilds.py` writing `K.WB_HUT` at `WORLD_HERMIT[1] - 1`, which is old
   (40,29) - and section 4's middle redraw covers old (24,22)-(47,31), so the
   hut and the Hermit's own square are both inside the band that was erased to
   kill the mountain fence. The staged map has no hut on it. The Middle
   Distance's hill, drawn by `field.py` at old (47,30), is in the same box;
   its *water* is protected by `KEEP_WATER` and `run_finish.py` re-isolates
   the rock, but the hill itself was not put back. Anything else the redraw
   box ate is found the same way: check the module's coordinate against
   `REDRAW` in `grow2.py`.
8. **The scenarios.** Anything that walks the world map by coordinate breaks.
9. **`encounterStep`.** Everything is about twice as far - Thistlewick to the
   Tower goes from ~40 steps to ~81 - so at step 36 the walk north has twice
   the battles it had. Re-cut it, or the trek stops being funny.
10. **Then the new quests**, which is what the whole thing is for.

## 7. The sites still to place

Measured by reading `COMPANIONS.md` and `BIOS.md` back against section 3's
twenty-one. The headline is that the map is in better shape than it looks:
**all eight of `COMPANIONS.md`'s L1-L8 clusters are placed, and six of
`BIOS.md`'s seven characters have a home.** Penultima, Fairholme, Gladhollow
and Olde Evermore are `BIOS.md` places, not `COMPANIONS.md` ones, and all four
are already on the map. The seventh, **Pellam Quickfoot, is correctly
placeless** - he is the merchant who is already in the deepest room of every
dungeon, so he needs no site. He needs dungeons to be in, and the game has two.

**Nothing in this section builds an interior.** A site here is a stamp, a door
event with no destination, and a line in `run_finish.py` - the same state the
twenty-one generated ones are already in. The doors chime and go nowhere until
somebody builds the room behind them, which is section 6 item 10 and is a
larger effort than this whole document: `COMPANIONS.md` section 7 sketches
**nineteen maps** for the eight clusters, and names faces as the blocker.

### 7.1 Four the design documents ask for and the map has not got

Each is one stamp, one door event and a line in `run_finish.py`. None needs an
interior to exist first; they are placeholders like the twenty.

| site | for | wants | near |
| --- | --- | --- | --- |
| **Ashcombe Lake** | COR-2, and it is in `COMPANIONS.md`'s world-map-only table | `Pond` | Ashcombe (102,55) |
| **The Duck's Pond** | ZEPH-2, same table; "four miles from the Collegium" | `Pond` | Collegium (112,38) |
| **Mrs Emberthwaite's hill** | `BIOS.md` Rosamund - the retired, widowed, card-playing dragon, and the whole point of her bio | a hill with a lair on it; `Cave A` or `Tower` | Fairholme (104,73) |
| **Tobias Frayne's cottage** | MER-4; `COMPANIONS.md` section 4 sites him on "the coast road cottage", which is a real coordinate now | `Hut` or `House (Town)` | the old coast road, `+ (35,35)` |

**Emberthwaite is not the Wrong Dragon.** ALD-6's dragon is at (110,114), forty
cells south. Two dragons is the joke working twice, not a duplicate.

### 7.2 Four whose bios assert a geography the map does not honour

These are re-sitings, and they are the same class of work as section 4's three
settlement fixes - not obvious until somebody read the bio and the map at the
same time.

* **Penultima has to be the last town before the Tower, and it is not.**
  That is its name and its entire joke - *The Last Town Before The End. Last
  Chance For Potions.* **Measured**: it is at (82,48) on the eastern road
  network, the 104-cell one it shares with the Collegium, Ashcombe and
  Fairholme. The Tower at (66,43) is on a different 70-cell network with Upper
  Clanging, and no road joins them. So Penultima is currently the last town
  before the east coast. **Settled: it moves onto the tower approach.** A shop
  that doubles its prices when a Chosen One is sighted on the road has to be on
  the road the Chosen One is on.
* **Olde Evermore is *hidden*.** `BIOS.md`: "the hidden elven village that every
  party finds eventually, by falling off the same ledge". It currently has a
  road to it like any other village. Hiddenness here is geography, not a
  switch: no road, and a ledge to fall off.
* **Hithermost's chapel stands beside the only door into the mountain**, at the
  top of the pass above the village. The Chapel of Continuance is *for* that
  door - travellers write their names in the Book and then go through it. There
  is a `Tunnel` stamp for exactly this and the site is built around it.
* **Restwell is a crossroads town** - "one street and nineteen inns". It wants
  roads that actually cross at (43,81).

### 7.3 A snow town, which is new

**The far north has no settlement at all.** Coldbarrow is a one-room chapter
house, the Sky Anvil is a meteorite used as a gatepost, and Hithermost is a
pass village whose reason for existing is a chapel. A third of the map's
climate has no town in it, and a world map with a snow region and no snow town
reads as unfinished.

There is no spare `BIOS.md` character to fill it - Pellam is the only unplaced
one and he is deliberately placeless - so this one is invented. Enough of it is
settled below to choose a stamp and a square; the rest is written later,
alongside 7.4, as a stage between the map work and the `COMPANIONS.md` /
`BIOS.md` build-out.

**Frostwick - the town that voted to keep the curse.**

*(cliche: the eternal winter, and the hero who broke it)*

Every world has the town under the hundred-year winter, and every one of them
is waiting for somebody to go and kill the thing that did it. Frostwick's was
broken. Forty years ago, by a Chosen One two or three numbers back, exactly as
advertised, and the snow stopped for eleven days.

Then the town held a meeting.

The Winter Festival is the only reason anybody comes to Frostwick, the
carol-and-lantern trade is four fifths of the parish income, and a working
group was convened to look into it. The curse is now **maintained** - by a
retained practitioner, under an annual contract, with a renewal clause and a
schedule of what constitutes a snowfall - and the town is very proud of the
arrangement, which it regards as forward-looking. The practitioner, who is not
an ice witch and would like that on the record, is a perfectly ordinary mage
whose speciality is refrigeration and who has never been happier. She does the
whole of January in an afternoon.

The hero who broke it **still lives there**. He is gracious about it. He opens
the Festival every year, cuts the ribbon, and does the face he has been doing
for forty years, and the town loves him, and nobody has ever once said the
quiet thing out loud. His wife thinks it is very funny and has said so only to
him. *That* is the joke: not a man robbed of his victory, a man who won,
retired somewhere nice, and married well, and whose one great deed is now a
line item in the events budget.

It connects to the spine of the game the way everything else here does. The
Prophecy is a contract; **Frostwick has one too**, and theirs is shorter,
better drafted, and renewed on time. Grimspite is four thousand years into an
engagement he cannot get out of. Frostwick's practitioner is nine years into
one she would renew tomorrow. The same joke, from the other end, in a town that
is pleased with itself - which is the register Great Dunnage is also written
in, and it travels.

Things to see, enough to know the place is worth a map: the Festival committee
and its minutes; the retained practitioner and her schedule of snowfalls; the
hero, and the ribbon; the visitors' book that has been signed by three Chosen
Ones; and the eleven days, which are commemorated. What the interiors actually
are is a later decision.

**What that means for the stamp.** A town, not a village: it has a committee, a
festival, an inn and a contract. **`Town B (Snow)`**, which is 2x2 and is the
snowed twin of Thistlewick's own `Town B` - deliberately, because Frostwick is
what Thistlewick would be if one of the forty-seven had come home and stayed.
Somewhere around **(62,22)**, subject to the land and standable checks: it
fills the gap between Coldbarrow (50,19) and the Sky Anvil (76,26), and it can
sit on the 44-cell northern road network that already joins those two, which
gives the far north one road with three things on it instead of three errands.

`COMPANIONS.md` section 7 names faces as **the** blocker, so this cast is a
bill as well as a joke - see `../CHARGEN.md`, which is now the answer to that.

### 7.4 One floating continent

**`Floating Continent (Castle)`**, settled. This is the answer to section 8's
question about the sea: **the airship currently earns three rocks**, and
`COMPANIONS.md` says the airship is the delivery mechanism for everything. A
place that can only be reached by flying, and that is visibly *up*, is what
makes the Two Hundred worth having flown.

**The Former Premises.**

*(cliche: the floating castle of the ancients, seat of the true final boss)*

The Dark Lord has not always risen in the Obligatory Tower. For the first two
thousand years of the engagement the venue was a castle in the sky, raised up
there by somebody's grandfather so that no hero could ever reach it, and it
worked exactly as intended: **nobody could ever reach it.**

It was vacated on **accessibility grounds.** The Prophecy Committee's minutes
record a complaint about the climb, then a second complaint, then a
recommendation, and the engagement was renegotiated onto a ground-floor site
with a door at the bottom - which is the Obligatory Tower, and is why it is a
tower with stairs in it rather than a castle on a cloud. An unreachable lair
turns out to be a poor lair. The business needs the heroes to arrive.

So the one place in the world you cannot walk to is the one place that was
abandoned *for being impossible to get to*, and the airship is what makes the
complaint moot four hundred years late. That is the whole joke and it lands the
moment the player sets down on it.

**Somebody is still up there.** The caretaker has kept the place ready since
the lease lapsed: the hall is swept, the sconces are lit, the visitors' book is
open on the lectern with nobody in it, and he has been doing the rounds against
the day the venue is re-let. He is not bitter and he is not mad. He is
*delighted*. A Chosen One has finally arrived and he starts the tour
immediately, and it is a very good tour, and he has been working on it.

It hangs off the spine exactly where Frostwick does. **The Prophecy is a
contract**, and this is its estate management: a decommissioned property, a
caretaker still on the books, and a change of premises minuted by a committee.
Ott gets to ask what it is made of. Grimspite has never seen it and has opinions
about the old place he has inherited entirely from paperwork.

**What that means for the stamp.** `Floating Continent (Castle)`, out over
water, far enough from any coast that it reads as *out there* rather than as an
offshore rock. Built to section 6 item 4's rules - player-touch events, below
characters, one bare square kept clear for the airship, `<aironly>` on the
events so `validate.py` asserts on foot that it cannot be reached. The square
it stands over must be checked with `flags & 0x0F == 0` like any other, because
a floating castle that the player can walk to is the one thing this joke cannot
survive.

It is air-only, so it is built to section 6 item 4's rules: player-touch
events, below characters, one bare square kept clear for the airship to land
on, and `<aironly>` on the events so `validate.py` asserts it cannot be walked
to.

### 7.5 Deferred, on purpose

A pass over the whole 207-stamp catalogue turned up ten more location types a
self-respecting RPG has and this map does not. **None of them is being built
now** - there is enough in section 6 already - but they are written down here
so the next person does not have to do the audit again, and in the order they
would be worth doing:

1. **A graveyard** (`Cemetery A/B`). The best of them: the premise is
   forty-seven dead Chosen Ones, the Wall of the Forty-Seven is already an
   event in Prophecy Hall, and a field of forty-seven headstones with the
   forty-eighth plot dug and waiting is one stamp.
2. **A mine** (`Mine`). Great Dunnage is nine works and no ore, and there are
   exactly two dungeons between the Gloamwood and the Tower - which is also
   Pellam's problem.
3. **Ruins** (`Town A (Ruins)`, `Castle (Ruins)`, `Fort (Ruins)`,
   `Village A (Ruins)`). There are none anywhere, in a world with forty-seven
   previous attempts on a Dark Lord.
4. **A port with a ship** (`Port`). Nether Sopping has one pier; this much sea
   wants a harbour, and it is the rung before the airship.
5. **Islands** (`Island A/B/C`), for the same reason as 7.4.
6. **A volcano and an ice cave** (`Volcano`, `Volcano Crater (Lava)`,
   `Cave A` on snow, `Pond (Ice)`). Zephyrine is the elemental specialist and
   there is no fire place and no ice place.
7. **Desert furniture** (`Oasis`, `Pyramid`, `Town D/E/F (Desert)`) - section
   8's other open question, four sites holding down the whole far south.
8. **A broken bridge** (`Broken Bridge A/B`, `Collapsed Bridge`) - the classic
   "you must go the long way", and the map already has a deliberate long way
   round the range.
9. **Signposts** (`Signboard A-D`, `Sign`). Everything is twice as far now, and
   a sign is a joke vehicle this game already owns: Fizz appears in front of
   every one you try to read.
10. **Gates and watchtowers** (`Gate A-D`, `Watchtower`, `Lookout Post`) -
    border checkpoints, which is Aldric's entire comic register.

Arena, casino and hot spring came up in the same audit and are **not** world
sites: they are interiors of Great Dunnage and Restwell, and PIP-3 and HOB-1
are already contests held there.

### 7.6 How any of it gets placed

**worldgen is finished as a generator and retained as a stamp library.** The
pipeline has run: `generated.json` is seed `w7`'s output, it is frozen, and
nothing on this list needs it re-run - the only thing that would is a decision
to regenerate the world, which means a different map and the review thrown
away. But `finish.py` calls `worldgen.stamps.catalogue()` on every `restamp`,
`unstamp` and `put_tiles`, for the footprints and the tile ids, and it is how
`unstamp` finds a building by its own ids rather than by a hand-counted
rectangle. So `tools/worldgen` is still imported on every hand pass, and
section 5's `TILE_ID_C` fix is load-bearing for **any** World_C stamp placed
from now on, not only for the Slum that found it. That is also why those six
files commit with the map: not because more generating is planned, but because
`run_finish.py` imports them every run, and because without them
`generated.json` is not reproducible from `grow2.py`.

Two things stopped being automatic when the generator stopped:

* **Roads are hand-drawn now.** Stage 5 joined the generated sites with 654
  cells of road; a site stamped by hand gets none unless `put_road` draws it.
  That is most of the work in Restwell's crossroads and in moving Penultima
  onto the tower approach.
* **The sidecar stops being the site list.** `generated.meta.json` will
  describe twenty-one sites for ever. The moment the first hand-placed site
  goes down, the authority for "where are the places" is the hand-maintained
  table below, and the sidecar is a record of how the map was grown.

**Not by adding anchors to `grow2.py`.** Changing the specification changes the
RNG stream, so re-running produces a *different world* and throws away the
reviewed map. New sites go in as `F.restamp()` / `F.put_road()` /
`F.put_tiles()` lines in `run_finish.py`, which is exactly how Thistlewick,
Nether Sopping, Upper Clanging and the Lighthouse were re-sited.

A hand-placed site does not get three things the generated twenty got for free,
and all three have to be supplied:

* **a door event**, written by hand, with no destination, like the others;
* **a check that the door cell is standable** - `flags & 0x0F == 0`, not
  `is_passable`, and not on another stamp's footprint. `place.py` does this
  properly and is the thing to copy; two squares picked by arithmetic instead
  were both mountains, and neither the build nor `validate.py` said so;
* **an entry in a site table that is maintained by hand**, because
  `generated.meta.json` is worldgen's output and is no more editable than
  `generated.json`. Section 6 item 6 wants one source for `places.py` and the
  door events both; this is where it comes from.

## 8. Open questions

* **Is `Village 1` at (60,61) wanted?** worldgen placed it itself, as an extra
  settlement beyond the anchors. It is in the middle of the old map's country,
  between the range and Thistlewick. Name it or remove it.
  **Still open, and it has no backstory anywhere** - "Village 1" appears in
  this file and in no other document or module in the game, so nothing is owed
  to it and nothing breaks if it goes. Looked at (staged as Map 941, probe at
  x=60 y=61): one building on the western edge of the redrawn middle, forest
  on two sides, wasteland and mountains immediately east, and a **six-cell
  road stub that joins nothing** - the smallest of the map's eleven road
  networks. It is the obvious home for 7.5's graveyard of the Forty-Seven if
  that is ever built, being a short walk from Thistlewick.
* **Does the far south want more than four sites?** Sump, the Fair, the Wrong
  Dragon and the Cinder Fen are what hold the desert down. It is a large
  landmass for four things.
  7.5 item 7 is the cheap version of an answer and is deferred.
* **Nothing has been said about the sea.** There is a lot of it and only three
  rocks in it. `COMPANIONS.md` says the airship is the delivery mechanism for
  everything; a few more islands would earn it. **Half-answered**: 7.4 adds one
  floating continent, which is the part of this that was worth doing first.
  Islands are 7.5 item 5 and are deferred.
