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
7. **`journey.py` loses its world map.** Map 8 is currently *drawn* by code -
   roads, coastlines and scenery placed by hand-written coordinate, with hooks
   in `wilds.py`, `field.py` and `meadow.py`. All of that drawing goes; those
   modules keep only their events, placed onto the generated map. This is the
   largest single piece of work here and it is much larger than the map was.
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

* **Penultima has to be the last town before the Tower.** That is its name and
  its entire joke - *The Last Town Before The End. Last Chance For Potions.* It
  is at (82,48) and the Tower is at (66,43). Whether it stands on the tower
  approach has not been checked; if it does not, it moves onto it. A shop that
  doubles its prices when a Chosen One is sighted on the road needs to be on
  the road.
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
one and he is deliberately placeless - so **this one is new, and it is owed a
backstory, a reason to go, and people to meet**, in that order and before any
stamp goes down. A stamp without a reason is the Lay-By without its backstory.
The vocabulary is there when the decision is made: `Town A/B/C (Snow)`,
`Village A/B/C (Snow)`, `Large Town A`, `Castle A,B (Snow)`, `Fort (Snow)`.

Three things it should probably be doing, given what the north already is:
it is far from Upper Clanging and owes it nothing; it is the only reason to go
above y=32 other than three errands; and `COMPANIONS.md` section 7 names faces
as **the** blocker, so its cast is a bill as well as a joke - see
`../CHARGEN.md`, which is now the answer to that.

### 7.4 One floating continent

`Floating Continent`, and its `(Castle)`, `(Temple)`, `(Giant Tree)`,
`(Cloud)` and `(Shadow)` variants. This is the answer to section 8's question
about the sea: **the airship currently earns three rocks**, and
`COMPANIONS.md` says the airship is the delivery mechanism for everything. A
place that can only be reached by flying, and that is visibly *up*, is what
makes the Two Hundred worth having flown.

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
  **Still open.** It is the obvious home for 7.5's graveyard of the
  Forty-Seven if that ever gets built, being a short walk from Thistlewick.
* **Does the far south want more than four sites?** Sump, the Fair, the Wrong
  Dragon and the Cinder Fen are what hold the desert down. It is a large
  landmass for four things.
  7.5 item 7 is the cheap version of an answer and is deferred.
* **Nothing has been said about the sea.** There is a lot of it and only three
  rocks in it. `COMPANIONS.md` says the airship is the delivery mechanism for
  everything; a few more islands would earn it. **Half-answered**: 7.4 adds one
  floating continent, which is the part of this that was worth doing first.
  Islands are 7.5 item 5 and are deferred.
