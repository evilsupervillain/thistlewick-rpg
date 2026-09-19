# The new world map

The 50x50 `Map008` rebuilt at **120x120**, generated with the workspace's
`tools/worldgen` and then finished by hand. It exists because the old map is
too small to hold the expansion: `COMPANIONS.md` wants eight new location
clusters and seven world-map-only sites, `BIOS.md` wants six more towns, and
the 50x50 was already crowded.

**Status: the map is finished, reviewed, and not installed.** It is
`build/worldmap/worldmap.json`, it stages cleanly, and nothing in `data/` or
`build/` points at it yet. **Section 6 items 1-5 are done - all of "the map"** -
which means every site is placed, the region layer is painted so the encounters
fire, the lost decoration is back, and a contact-sheet pass has been run over
the whole thing. What is left is **section 6 items 6-10, "the game"**: rewiring
`places.py`, taking the drawing out of `journey.py`, the scenarios,
`encounterStep`, and then the quests. That is Phase B and it is much larger
than the map was; do not start it in the same session as anything else.

    python3 build/worldmap/run_finish.py --stage 941   # rebuild and stage it
    python3 build/worldmap/review.py 941               # old map vs new, measured
    python3 build/worldmap/decor.py 941                # the decoration diff; 0 casualties
    python3 build/worldmap/look.py 66 74 92 88         # a window of it, as text
    node ../tools/serve.js ../staging 8770 &           # then _probe.html?map=941
    RMMZ_PORT=8770 node ../tools/shots.js /tmp/s 941:79:80 941:80:88
    python3 ../tools/propsheet.py ../staging /tmp/p.png 941   # what the props *are*

Run `decor.py` after every change - it exits non-zero on a casualty. And a
screenshot is still the only thing that catches a stamp reading as the wrong
object; four of Phase A's five items found something no check could see.

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
      decor.py        the decoration diff: `Map008`'s layer 2-3 cells against
                      the new map at + (35,35), with deliberate losses,
                      nudges and casualties counted apart. Non-zero exit if
                      anything is a casualty, so it is a check and not a report
      look.py         the map as text, one character per cell - biome, relief,
                      stamps, roads, events. A screenshot is the only way to
                      judge whether a map *reads*, and the wrong tool for
                      asking where a coastline is; this answers "what shape is
                      this headland" for a thousandth of the cost and can be
                      diffed between runs

**`MapGrid.autotile` reproduces worldgen's own output byte for byte** - 0 cells
differ on a round trip, measured - which is what makes the hand pass safe.
Edit tiles, re-autotile layers 0 and 1, and nothing else moves.

## 3. Where everything is

Old-map places are at `old + (35,35)`. The doors that moved are marked.

| place | old | new | note |
| --- | --- | --- | --- |
| Thistlewick | (24,43) | **(60,79)** | moved: was astride the road |
| Nether Sopping | (36,44) | **(71,84)** | moved down onto its own shore |
| The Lighthouse | (41,44) | **(79,80)** | moved out onto its headland (6.1) |
| Upper Clanging | (9,12) | (44,47) | |
| Gloamwood Mouth | (17,27) | (52,62) | |
| Gloamwood North Mouth | (17,20) | (52,55) | |
| Obligatory Tower | (31,8) | (66,43) | |
| everything else | | `+ (35,35)` | unchanged |

**The twenty-one generated sites.** Two of these rows have since been changed
by hand and the sidecar does not know: **Penultima moved** and **the Sky Anvil
was restamped**, both marked below. `generated.meta.json` describes what
worldgen grew and is not editable, so from here on this table is the authority
and 7.6's rule applies - the hand-placed sites are the second table under it.

| site | at | stamp | for |
| --- | --- | --- | --- |
| Coldbarrow | (50,19) | Temple A (Snow) | ALD-3, ALD-2 |
| Hithermost | (30,23) | Village A | `BIOS.md` Brother Quillon |
| Sky Anvil | (76,26) | **Shrine** | HOB-4 - restamped; see 6.5 |
| Penultima | ~~(82,48)~~ **(64,48)** | Town B | `BIOS.md` Gideon Markup - moved onto the tower road; see 7.2 |
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

**The eight placed by hand**, which is the table 7.6 asks for. Same state as
the twenty-one: a stamp, a door event with no destination, and nothing behind
the door. Every door cell was checked with `flags & 0x0F == 0` by
`finish.add_site`, which refuses a site with no standable cell to put one on.

| site | at | stamp | for |
| --- | --- | --- | --- |
| Ashcombe Lake | (104,54) | **terrain** - inland water, no stamp | COR-2 |
| The Duck's Pond | (115,40) | Pond | ZEPH-2 |
| Mrs Emberthwaite's lair | (111,69) | Cave A, in a drawn hill | `BIOS.md` Rosamund |
| Tobias Frayne | (66,82) | House (Town) | MER-4 |
| The Door into the Mountain | (30,21) | Tunnel | `BIOS.md` Brother Quillon |
| Chapel of Continuance | (30,22) | Temple C | `BIOS.md` Brother Quillon |
| Frostwick | (61,21) (62,21) | Town B (Snow) | 7.3 - invented |
| The Former Premises | (79,88) (80,88) | Floating Continent (Castle) | 7.4 - invented, **air-only** |

Each of the twenty-nine has a door event on it, with no destination. They are
**placeholders**: the transfer has to be written when the interior exists. The
hand-placed ones are noted `<worldmap-site ...>` rather than
`<worldgen-site ...>`, which is how `review.py` tells them apart, and the
Former Premises also carries `<aironly>` so `validate.py` asserts on foot that
it cannot be reached.

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

**The road network is in pieces, and that is accepted for now** - but the
count was misleading and the reason is worth knowing. Measured on the finished
map by flooding the `Road (Dirt)` and `Road (Paved)` autotiles: **eleven**
networks of ten cells or more, the largest 148, plus eight scraps of nine cells
or fewer that were not counted. `review.py` now prints all of them, so the
number it reports is larger than the one in this paragraph and always was.

**Most of the fragmentation is diagonal joins, not gaps.** At four-connectivity
the generated map is 19 pieces; at eight it is 16. MZ has no diagonal movement,
so a road that meets the next road corner-to-corner is a road that stops - and
that is what three of the biggest "separate networks" turned out to be. Closing
one such corner at each end of the northern road merged **three** networks of
148, 47 and 109 cells into one of 306 carrying fifteen sites (7.3). Roads are
cheap and these are cheaper than that: the lever is one cell, and the thing to
measure before drawing any new road is whether the two ends are already
touching. The big one is a
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

**Half of the Lighthouse's restamp has since been reversed, and the reason is
the only thing a contact sheet can find.** Section 4 unsnowed it - "the same
tower, without the snow on it" - into `World_B/Tower A`, ids 80 and 88. That is
exactly what `journey.py` draws the **Obligatory Tower** with, at (66,42). So
the coastal landmark east of Nether Sopping and the final dungeon of the game
were the identical graphic, and nothing could see it: not `validate.py`, not
`review.py`, not a screenshot of either place, because each looks correct on
its own. Item 5's `propsheet.py` pass resolves tiles back to catalogue records
and lists them side by side, which is how two entries reading `Tower A` at two
sites turned up. It is back on `Tower A (Snow)`, whose white top is a **lamp
room** - the shipped game's own constant for it is `WB_TOWER_WHITE` - and the
whole tower field was cropped before choosing: `Tower B` is `Tower A` in
browner stone and indistinguishable at 48 pixels, `Tower C` is a pink ziggurat,
`Tower D` is one cell, and every `World_C` tower including `World_C/Lighthouse`
is a skyscraper or a modern light. **A few snow flecks in temperate country is
a smaller fault than the final dungeon having a twin**, and that is the trade
that was made.

**The 50x50 has two cells nobody can reach**, at (6,27) and (9,27): single
walkable holes sealed inside the western mountain mass. Stage 4 refuses to
build on a map with those in it, so `grow2.py` walls them up (`SEALED`). Both
are inside the band that gets redrawn, so they are gone either way.

## 5. What was found in the tools

Four faults in `tools/worldgen`, all fixed and **committed** - the workspace's
`875abe3 worldgen: four fixes found by growing a world around a real map`:

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

**Items 1-5 are done** - the whole of Phase A - and what each of them turned
out to be is below, because four of the five found something the plan had not
predicted. Items 6 onwards are untouched and are Phase B.

1. ~~**The Lighthouse's own geography.**~~ **Done.** It is a spit: three cells
   of `Rocky Land A` reaching east out of the coast at x=76, two deep, water cut
   either side of the neck, the track running out along it, and the tower at the
   tip - so the Lighthouse **moves to (79,80)**, which item 6 has to re-derive
   its exit from rather than offsetting. `EXPANSION.md` always called it "a
   world-map landmark east of Sopping **on a spit of rock**" and `places.py`'s
   own constant has read `# on its own headland` the whole time; the generated
   coast left it two cells inland of a blunt corner, which is a lighthouse
   standing in a field. `finish.put_land` exists for this and only this:
   cutting water can only ever make a coast *straighter*, so a shape that
   reaches out has to be drawn. The stamp changed too, and that was item 5's
   find - see section 4.
2. ~~**The sites still to place, and the four that are sited wrong.**~~
   **Done, all nine.** Section 7 has each one; section 3's second table is the
   hand-maintained list 7.6 asked for. Two things learned that generalise:
   * **A stamp's own cell has to be *open*, because the door stands on it.**
     Every site door is a player-touch, below-characters event on the stamp
     cell, so `World_C/Hut` (0x60f) cannot carry one and `House (Town)` can -
     which is why 7.1 offered both for Frayne. It is also the constraint that
     produced the Sky Anvil's wrong stamp, and why a rock is hard to draw: every
     rock in the catalogue is blocked. `finish.add_site` refuses a site whose
     footprint leaves no standable cell, and refuses one that lands on another
     stamp - the two mistakes arithmetic makes in silence.
   * **A stamp repeated is not a bigger thing, it is more things.** Ashcombe
     Lake was placed as `Pond`, which is one small round pond drawn on a single
     tile, and read as a puddle with a drowned village allegedly under it. Seven
     of them would have read as seven puddles. It is inland **water** now, the
     sea autotile with a sand shore, and the door is a square of shoreline -
     which is also the better joke, because COR-2's lake is drawn down for the
     sluices and "if you are there that week you can walk in". Only a
     screenshot finds this.
3. ~~**The region layer.**~~ **Done, and the encounters work.** `generated.json`
   already carried `Map008`'s nine `encounterList` entries and `encounterStep`
   36 - `grow2.py` copied the map header - so the only thing missing was the
   layer, and nine good encounter entries were pointing at regions nothing was
   painted with. Three decisions, in `finish.paint_regions`:
   * **The divide is the range, not a latitude.** The 50x50 split at y<=21 /
     y>=30 with a dead band between, because its mountain fence stood in those
     rows. The new map has a drawn range whose spine runs y=62 in the west to
     y=56 in the east, so the divide is interpolated per column. The dead band
     is gone: it was the fence, and "no encounters here" was never the point.
   * **Snow and desert get regions 5 and 6.** A third of this map's climate did
     not exist on the 50x50, and pointing it at turnips would be worse than
     leaving it empty. They are *widened into* the north's three troops for now
     by adding 5 and 6 to those entries' `regionSet` - so nothing is empty
     today, and a campaign writing real snow and desert encounters has
     somewhere to hang them without repainting the map. `finish.point_at` does
     that without touching the database: the troop ids came across in the
     header, so the encounter *list* stays `journey.py`'s to own.
   * **The shingle has to be next to the sea.** `K.W_SAND` is autotile kind 26,
     `Dirt Field A`, and on the 50x50 every cell of it was shore. The new map
     has 353 including an inland basin in the far north, so "kind 26 is the
     coast" puts crabs and gulls in a snowfield. 58 cells qualify.

   Painted: south 2786, north 2310, coast 58, clanging 193, snow 1251, desert
   669, and 12 quiet. **It has to run after `World.settle`**, which is new: a
   passability flag belongs to an autotile *shape* and not to a kind, and
   everything in `finish.py` writes shape 0 and lets `save` autotile at the end
   - so a pass that asks "can the player stand here" of every cell has to
   settle first or it is reading shapes the engine will never see.
4. ~~**The three air-only rocks.**~~ **The map half is done; the events are
   item 6's.** Their events live in `field.py` and arrive with it, so what was
   checkable here was the geometry, and item 7's suspicion was right:
   **the Middle Distance had lost one of its two hill cells.** `field.py` puts
   `W_HILLS` on the back row - 0x0e0f, impassable *and* carrying 0x0800, so it
   is scenery an airship cannot set down on and the two rows in front are where
   the airship goes and where the bench is - and the middle redraw took (82,65),
   which came back **open**. The rock had five walkable cells instead of four
   and the Hermit had a hill with a hole in it. Restored.

   **`decor.py` cannot see a fault like that and is not going to be made to.**
   It diffs layers 2 and 3, where a decoration is a tile that is either there or
   not; layer 1 is autotiled terrain that differs almost everywhere on purpose,
   so a diff of it reports the whole new world. The four places off the mainland
   are checked **by name** in `review.py` instead, which prints each one's cell
   count, walkable count, landable count and region, and says so out loud if any
   of them becomes walkable from the mainland. All four are region 0: nothing
   lives out there, and a party that has just set down on the Isle of Uncertain
   Ownership should not be met by turnips.
5. ~~**A pass with `propsheet.py`**~~ **Done, and it earned its place twice.**
   Sixty distinct prop tiles over the finished map. Two findings, neither of
   which any other check could have produced:
   * **The Lighthouse was the Obligatory Tower.** Section 4 has the write-up.
   * **The Sky Anvil was a tree.** "A meteorite used as a gatepost since 1749",
     HOB-4's whole joke, stamped `Giant Tree (Snow)` by worldgen - a snowy tree
     standing in for a rock, which at 48 pixels is a plausible landmark that
     contradicts the only line of dialogue about it. This is exactly the
     workspace `CLAUDE.md`'s "a prop that was the wrong *object*". It is
     `Shrine` now: a stone trilithon with a boulder resting across the top, a
     gatepost with a rock on it, and open, so the door event did not move. The
     **unsnowed** variant, which is the opposite call to the Lighthouse's and
     for the opposite reason - both were rendered in place, and `Shrine (Snow)`
     is white stone under white snow on a white snowfield and vanishes. A
     landmark you cannot see is not a landmark.

   Two things worth not rediscovering from the same sheet. `Mine` is the
   catalogue's name for `WB_CAVE_DARK`, which is already the tile for both
   Gloamwood mouths, the Barrow and the Crag - so 7.5 item 2's mine would look
   like the Barrow, and needs a different stamp or a reason. And the `Rainbow`
   at (55,73) and the `Bridge (H)` at (72,109) are `meadow.py`'s and
   worldgen's respectively, both correct, both surprising in a list.

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
   * **Four do not move by 35, and one of those moved twice.** Thistlewick,
     Nether Sopping, Upper Clanging and the Lighthouse were all restamped and
     re-sited by section 4; their exits have to be re-derived from section 3,
     not offset. The Lighthouse has since moved again, out onto its headland:
     it is **(79,80)**, not (76,79) and certainly not `+35`. Penultima moved
     too - to (64,48) - and while it has no exit of its own yet, anything that
     learns its coordinate has to learn it from section 3 and not the sidecar.
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

   **Thirteen of them were already gone; all thirteen are back.** `decor.py`
   is that diff, and it is the check to re-run after any change to
   `run_finish.py`: it compares `Map008`'s layer-2 and layer-3 cells against the
   new map at `+ (35,35)`, and it exits non-zero on a casualty so it is a check
   rather than a report. Twenty-seven cells differed. **Fourteen are
   deliberate** - the three `Fortress City` stamps at Thistlewick, Nether
   Sopping and Upper Clanging, and the Lighthouse's `Tower A (Snow)`, all
   restamped by section 4. The other thirteen were casualties:

   | what | old | new | outcome |
   | --- | --- | --- | --- |
   | The Hermit's hut (`WB_HUT`, a `Tent`) | (40,29) | (75,64) | restored |
   | Meredith Crooke's camp tent (`WB_HUT`) | (11,32) | (46,67) | restored |
   | **The Bottomless Pit's cave mouth** (`WB_CAVE`, `Cave A`) | (8,35) | (43,70) | restored |
   | Giant Tree scenery (`WB_TREE`), 7 cells | (40,21) (37,22) (9,25) (34,29) (7,33) (44,33) (12,35) | `+35` | 3 as asked, **4 nudged** |
   | Rock scenery (`WB_ROCK`, `Dirt`), 3 cells | (36,13) (7,22) (31,31) | `+35` | restored |

   **The Pit was the one that mattered** and it is a cave mouth again -
   `run_finish.py` already dug its terrain back out of the mountain the redraw
   buried it under, but the mouth is a *decoration tile* and nothing had put
   that back, so the Pit was an invisible hole in open ground with a transfer
   event on it. The two tents were the same fault one step down: the Hermit and
   Crooke both had their events and their squares and nothing to look at.

   **Four of the seven trees moved a cell or two, and that is the right
   answer.** Three of them now stand under the hand-drawn range and one is out
   past the mended coast, and `put_tiles` writes where it is told - so a Giant
   Tree goes onto a mountain, or into the sea, without complaint, and looks like
   a fault in the map. These tiles are *scatter*: hand-typed coordinate lists in
   `journey.py`, `wilds.py` and `field.py` with no meaning attached to any one
   cell. So `finish.put_scenery` refuses sea, mountain relief, an existing
   stamp footprint and an event's square, and nudges to the nearest cell that
   will take one - which keeps the dressing and costs nothing, where clearing a
   mountain to make room would hole the range for a decoration. `decor.py`
   counts a nudge as accounted for and a loss as a casualty, so the number can
   reach zero and stay a check. **It is 0 casualties, 4 nudged.**

   **The events themselves are all fine**, which is worth knowing because it is
   the half that could have been much worse: all twenty-eight of `Map008`'s
   events land on a square exactly as standable as the one they left. Four
   signposts report as blocked, and were blocked on the 50x50 too - a
   `WB_SIGN` tile blocks its own cell and is read from beside it - so that is
   the idiom, not a regression.

   One that was confirmed and fixed: **the Middle Distance's anchor cell had
   gone from blocked to open.** `field.py` drew a hill there at old (47,30) and
   the redraw took it. Item 4 above has the write-up and `review.py` now checks
   all four sea places by name.

8. **The scenarios.** Anything that walks the world map by coordinate breaks.
9. **`encounterStep`.** Everything is about twice as far - Thistlewick to the
   Tower goes from ~40 steps to ~81 - so at step 36 the walk north has twice
   the battles it had. Re-cut it, or the trek stops being funny.
10. **Then the new quests**, which is what the whole thing is for.

## 7. The sites still to place - **placed**

**All nine are on the map**: 7.1's four, 7.2's four re-sitings, 7.3's snow town
and 7.4's floating continent. Each subsection below keeps the design reasoning,
which is the half worth re-reading, and records under it what was actually done
and what it cost. Section 3's second table is the coordinates.

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

### 7.1 Four the design documents ask for - **all four placed**

Each is one stamp, one door event and a line in `run_finish.py`. None needs an
interior to exist first; they are placeholders like the twenty-one. Where each
one went, and what each cost beyond a line, is below the table; section 3's
second table is the authority for the coordinates.

| site | for | wants | near |
| --- | --- | --- | --- |
| **Ashcombe Lake** | COR-2 | **inland water**, not `Pond` - see below | (104,54), two cells from Ashcombe's east door |
| **The Duck's Pond** | ZEPH-2, "four miles from the Collegium" | `Pond`, one cell, which is right for one duck | (115,40), with the Collegium in shot |
| **Mrs Emberthwaite's hill** | `BIOS.md` Rosamund | `Cave A` in a **drawn** hill - the palette has no hill | (111,69), seven cells from Fairholme |
| **Tobias Frayne's cottage** | MER-4, "the coast road cottage" | `House (Town)`; `World_C/Hut` is blocked | (66,82), on the old coast road, now y=81 |

**Ashcombe Lake is water, and `Pond` was the wrong tool.** `Pond` is one small
round pond drawn on a single tile - correct for the Duck's, and a puddle for the
lake a village is supposed to be under. Repeating it would have given seven
puddles, not a lake. It is the sea autotile inland now, seven cells with a sand
shore in the valley north-east of the village, and the door is a square of
*shoreline* - which is the better joke anyway, because COR-2's lake is drawn
down one week a year for the sluices and "if you are there that week you can
walk in". Only a screenshot finds a fault like this; the text view and every
check said it was fine.

**The lair is a hill drawn by hand, and a cave mouth over mountain relief reads
back as open.** Eleven cells of `Mountain (Grass)` in a three-five-three
diamond - a 3x3 block reads as a plantation - with `Cave A` on layer 3 in the
middle of the southern face. The topmost non-star tile decides passage, so the
cave cell is standable inside a mountain, which is exactly how the Bottomless
Pit and the Barrow have always worked. It also gets a **five-cell track** off
the Fairholme road, and it is the only road on the map that goes to a dragon:
Rosamund "has started going round on Thursdays **without being carried**", and
a lair somebody visits weekly has a path to it.

**Emberthwaite is not the Wrong Dragon.** ALD-6's dragon is at (110,114), forty
cells south. Two dragons is the joke working twice, not a duplicate.

### 7.2 Four whose bios assert a geography the map does not honour

These are re-sitings, and they are the same class of work as section 4's three
settlement fixes - not obvious until somebody read the bio and the map at the
same time.

**All four are done.** Each is written up below as the problem it was; what
was actually done is the line after it.

* **Penultima has to be the last town before the Tower, and it was not.**
  That is its name and its entire joke - *The Last Town Before The End. Last
  Chance For Potions.* **Measured**: it is at (82,48) on the eastern road
  network, the 104-cell one it shares with the Collegium, Ashcombe and
  Fairholme. The Tower at (66,43) is on a different 70-cell network with Upper
  Clanging, and no road joins them. So Penultima was the last town before the
  east coast. A shop that doubles its prices when a Chosen One is sighted on the
  road has to be on the road the Chosen One is on.
  **Done: (64,48)**, five cells south of the tower door with its two doors
  against the approach road at x=63, and no spur needed. Measured after:
  Penultima is now the only site on that 70-cell network, which is the whole
  point - it is alone on the road to the end of the world. `finish.move_site`
  is the operation: it rubs the building out by its own ids, restamps it, and
  carries its door events with it by the same offset. **Nothing is deleted** -
  an event id is an index into the map's own list and a hole in it is a hole
  for ever - so re-siting moves events and never drops them.
* **Olde Evermore is *hidden*.** `BIOS.md`: "the hidden elven village that every
  party finds eventually, by falling off the same ledge". It had a road to its
  door like any other village. Hiddenness here is geography, not a switch: no
  road, and a ledge to fall off.
  **Done**, and it very nearly broke the south-west. The road past it is the
  **trunk**, not a spur: it comes down x=28, doglegs east to x=29 for three rows
  straight past the village door, and carries on south to Gladhollow. Deleting
  those cells dropped Gladhollow's road network from 79 cells to 21 - a change
  nothing on the map says out loud and no screenshot shows. So the trunk is
  *re-routed* straight down x=28 first, and only then does the dogleg go back to
  trees: `finish.put_forest`, not a clear, because a cleared cell threading a
  wood is a path. The village is now a pocket with mountain closed round its
  north and east - the ledge - forest on its western approach, and no road to
  its door. **If any road is ever removed again, measure every site's network
  before and after**; `review.py` prints the pieces for exactly this.
* **Hithermost's chapel stands beside the only door into the mountain**, at the
  top of the pass above the village. The Chapel of Continuance is *for* that
  door - travellers write their names in the Book and then go through it. There
  is a `Tunnel` stamp for exactly this and the site is built around it.
  **Done, as two sites.** The pass is the neck at y=21 where the western massif
  reaches the road at x=31, two cells above the village; the `Tunnel` is set into
  that face at **(30,21)** and the **Chapel of Continuance** stands below it at
  **(30,22)**, so the Book is the last thing on the near side. Village, chapel,
  door into the mountain, stacked up the pass in that order. `Temple C` for the
  chapel, because Coldbarrow has `Temple A (Snow)` and Weeping Bottom has
  `Temple B`.
* **Restwell is a crossroads town** - "one street and nineteen inns" - and the
  road merely arrived from the north-west and stopped.
  **Done: eighteen cells.** Road on all four sides of the town block and four
  arms leaving it - the existing one north-west, a street west and a lane east,
  and a southern arm down the one-cell corridor at x=46 that the mountains leave
  open, which is a piece of the map that had no road on it at all.

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
festival, an inn and a contract. **`Town B (Snow)`**, which is 2x1 - not 2x2 -
and is the snowed twin of Thistlewick's own `Town B`, deliberately, because
Frostwick is what Thistlewick would be if one of the forty-seven had come home
and stayed.

**Placed at (61,21)-(62,21)**, all snow, no relief under it, with a three-cell
road spur east along y=22 to meet the northern road at (65,22).

**And the reason this square was chosen was not true, which is worth recording
because the fix was two cells.** 7.3 said the site "can sit on the 44-cell
northern road network that already joins" Coldbarrow and the Sky Anvil. Measured:
that network joined **neither**. It ran between the two and touched them only
*diagonally* - (50,20) beside (49,19) at Coldbarrow, (76,25) beside (77,26) at
the Anvil - and MZ has no diagonal movement, so a diagonal join is a road that
stops. Frostwick would have been alone on a 47-cell road going nowhere.
**One cell at each end** - (49,20) and (77,25) - closed both corners and merged
three networks of 148, 47 and 109 into **one of 306 carrying fifteen sites**:
Coldbarrow, Frostwick, the Sky Anvil, Hithermost, Great Dunnage, Sable Hart,
the Lay-By, Ashcombe, Ashcombe Lake, the Collegium, Fairholme, Emberthwaite's
lair, the Duck's Pond, the Chapel and the Door into the Mountain. So the far
north is one road from the chapter house to the gatepost with a town on it,
which is what this section asked for and thought it already had. Section 4 has
the general lesson.

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

**What that means for the stamp, and what it turned out to need.**
`Floating Continent (Castle)` is two **star** tiles (0x610), so the stamp
decides *nothing* about passage and the ground underneath decides everything -
which is the whole difference between this and a stamp on the water. A star
stamp over sea is a castle nobody can stand on, and the check that catches it
is `finish.add_site`'s: it asks the finished map for a standable cell rather
than asking the stamp, and refuses a site that has none.

So it is **three cells of `Clouds`** - autotile kind 42, which is open at 0x600,
and which is plainly what the palette carries a cloud biome *for* - out in the
middle of the southern sea at **(79,88)-(81,88)**, with six cells of open water
on every side, which is what makes it read as *out there* rather than as an
offshore rock. Two cells carry the castle and its doors and **the third is left
bare**, because `Game_Vehicle.isLandOk` refuses a square with an event on it:
a castle with a door on every cell is a castle with no way in. The events carry
`<aironly>`, `review.py` confirms none of the three is walkable from the
mainland, and they are region 0 like the other three rocks.

One thing it had to be told: **`sink_islets` would have drowned it.** Three
walkable cells nobody can walk to is precisely what that pass exists to drown,
so the Premises is in `run_finish.py`'s `rocks` list beside the other three.

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

1. **A graveyard** (`Cemetery A/B`). One stamp, and the premise as first
   written here was **wrong** - do not build it as stated. "Forty-seven dead
   Chosen Ones" contradicts the spine of `EXPANSION.md`, which asks "forty-seven
   went north; where are they?" and answers **Nether Sopping**: they came back,
   they were quietly resettled, and they are all alive in the Slain Wyvern.
   Exactly one is buried, and elsewhere - Ambrose Fitch, #44, in the Barrow of
   the Forty-Fourth in the eastern hills, who is not even dead in the useful
   sense because he stands up and fights you. The dead are already counted, and
   not by Thistlewick: the Sopping harbour memorial has a hundred and
   eighty-one names against the Wall's forty-seven portraits, and nobody in
   Thistlewick has counted the difference. There is also already a Thistlewick
   churchyard in the lore - Beatrice Grumnir's headstone, `COMPANIONS.md` - and
   it is inside the village.

   A graveyard is still available, and the version that *pays off* the
   181-against-47 count instead of breaking it is **the stones being wrong, not
   the people**: Thistlewick built the Forty-Fourth a heroic barrow forty years
   late because that is what you do with a hero, and the same instinct at scale
   is forty-seven memorial stones, voted and paid for and unveiled, for
   forty-seven people who are alive eleven cells south and have written in to
   ask that they come down. The parish will not, because the stones are paid for
   and the unveiling is minuted. The forty-eighth plot is dug and waiting,
   because nobody has learned anything. **Offered and not taken** (section 8);
   written down so the audit is not repeated and the wrong version is not built.
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

A hand-placed site does not get three things the generated twenty got for free.
All three are now supplied by **`finish.add_site`**, in one call, so a site
cannot be half-placed:

* **a door event**, written by hand, with no destination, like the others -
  player-touch and below characters, which is worldgen's rule and the engine's;
* **a check that the door cell is standable** - `flags & 0x0F == 0`, not
  `is_passable`, and not on another stamp's footprint. `place.py` does this
  properly and was the thing copied; two squares picked by arithmetic instead
  were both mountains, and neither the build nor `validate.py` said so. It asks
  the **finished map** rather than the stamp, which is what makes it work for a
  star stamp like the Floating Continent, where the ground underneath decides;
* **an entry in the hand-maintained site table**, which is now section 3's
  second table. Section 6 item 6 wants one source for `places.py` and the door
  events both; that is where it comes from.

Two more things a hand pass has to know, both learned the hard way in 7.1-7.4:

* **The stamp's own cell has to be open, because the door stands on it.** That
  rules out every rock in the catalogue (`Dirt`, every `Rocky Mountain`, both
  `Statue`s - all 0x60f) and `World_C/Hut`, and it is why worldgen drew a
  meteorite as a tree. `add_site` takes `stamp_name=None` for a site whose
  landmark is *terrain* instead - Ashcombe Lake's water, and the three air-only
  rocks are the same category the other way up.
* **A stamp repeated is more things, not a bigger thing.** See Ashcombe Lake in
  7.1. A `Pond` laid over seven cells is seven ponds.

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
  networks.

  **Still open after a second look, and deliberately left standing.** Two
  candidates were measured against it and both were refused. It is *not* a home
  for Corvin Ash's resettled village, which is a question worth recording
  because it is the one thing on the map that sounds like it wants a spare
  settlement: Ashcombe (New) is already stamped at (102,55) and **Ashcombe
  Lake** - the drowned Ashcombe (Old), 7.1's first item - has to be adjacent to
  it, so that COR-2's draw-down week is a walk from COR-1's dinner. Moving
  either forty-two cells west across the range breaks that adjacency, and there
  is nothing else at (60,61) to gain by it. A sweep of `COMPANIONS.md`'s
  seven world-map-only sites and its new-NPC table found **no unplaced thing
  that wants a settlement here**: five of the seven are stamped, and the other
  two plus Mrs Emberthwaite's hill and Tobias Frayne's cottage are each pinned
  to somewhere else by their own bio. And it is not 7.5's graveyard either,
  whose premise was wrong - see that entry. So the site is surplus and is being
  kept surplus rather than filled with the first idea that fits.
* **Does the far south want more than four sites?** Sump, the Fair, the Wrong
  Dragon and the Cinder Fen are what hold the desert down. It is a large
  landmass for four things.
  7.5 item 7 is the cheap version of an answer and is deferred.
* **Nothing has been said about the sea.** There is a lot of it and only three
  rocks in it. `COMPANIONS.md` says the airship is the delivery mechanism for
  everything; a few more islands would earn it. **Half-answered and half-done**:
  7.4's floating continent is **placed**, at (79,88), which was the part of this
  worth doing first - the airship now earns a destination that is visibly *up*
  and that was abandoned for being impossible to reach. Islands are 7.5 item 5
  and remain deferred. The sea is still mostly empty and that is still an open
  question, just a smaller one.
