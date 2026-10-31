# The new world map

The 50x50 `Map008` rebuilt at **120x120**, generated with the workspace's
`tools/worldgen` and then finished by hand. It exists because the old map is
too small to hold the expansion: `COMPANIONS.md` wants eight new location
clusters and seven world-map-only sites, `BIOS.md` wants six more towns, and
the 50x50 was already crowded.

**Status: the map is finished and INSTALLED.** `Map008.json` is the 120x120
map: `journey.world_map` loads `build/worldmap/worldmap.json`, puts this game's
header on it and merges this game's twenty-eight world-map events into it.
`python3 build/build_game.py` builds the game and `python3 ../tools/validate.py .`
reports no problems, which is the check that all thirteen exits back onto the
world map land on standable, reachable squares.

**Section 6 items 1-9 are done.** Items 1-5 were the map - every site placed,
the region layer painted so the encounters fire, the lost decoration back, and a
contact-sheet pass over the whole thing. Items 6-9 were the game - `places.py`
re-cut, the drawing taken out of `journey.py`, `wilds.py`, `field.py` and
`meadow.py`, the scenarios updated, and `encounterStep` measured and left alone.

**What is left is item 10, the quests**, which is what the whole thing was for
and is a larger effort than everything above it: `COMPANIONS.md` section 7
sketches nineteen maps for the eight clusters, and there are twenty-nine sites
on the map whose doors are placeholders with nothing behind them.

**One of the twenty-nine is built**, and **`SITES.md` is the queue for the
other twenty-eight** - the ordered work list, eighteen steps, what each site is
and what it is for, plus the working rules this effort runs under (nothing has
to be atomic; no full suite between sites; nothing is published until it is
pushed to `live-rpg`). Read that rather than this file to pick up the work.

**Penultima** - `BIOS.md`'s Gideon Markup, at (64,48) on the tower road - is
Maps 29 and 30, `build/penultima.py`, and its two doors are real. 7.6's last
subsection is how that was done and is the shape every other site should copy;
the placeholder count is **39** now and `placeholder_doors` is the check that
noticed. 7.3 and 7.4 have their casts written.

    python3 build/worldmap/run_finish.py --stage 941   # rebuild and stage it
    python3 build/worldmap/review.py 941               # old map vs new, measured
    python3 build/worldmap/decor.py 941                # the decoration diff; 0 casualties
    python3 build/worldmap/coords.py                   # the scenarios' world-map squares
    python3 build/worldmap/look.py 66 74 92 88         # a window of it, as text
    node ../tools/serve.js ../staging 8770 &           # then _probe.html?map=941
    RMMZ_PORT=8770 node ../tools/shots.js /tmp/s 941:79:80 941:80:88
    python3 ../tools/propsheet.py ../staging /tmp/p.png 941   # what the props *are*

and then, because the map is installed, the game has to be rebuilt to pick it up:

    python3 build/build_game.py                        # journey.py reloads worldmap.json
    python3 ../tools/validate.py .                     # no problems found
    ../tools/scenarios.sh .                            # an hour; background it

Run `decor.py` after every change - it exits non-zero on a casualty. And a
screenshot is still the only thing that catches a stamp reading as the wrong
object; **eight of section 6's nine items found something no check could see**,
and `CHARGEN.md` is not the only document here whose estimates were wrong in
the same direction. Do not trust a measurement in this file that does not say
it was measured.

**`build/worldmap/old50.json` is the old 50x50 and must not be deleted.**
`data/Map008.json` is the *new* map now, so four things - `grow2.py`,
`finish.old_events`, `decor.py` and `review.py` - would otherwise be reading
this map as their own input. See section 6 item 7.

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
      old50.json      the 50x50 `Map008` as it was before this map replaced
                      it. **NEVER EDITED**, and load-bearing: `data/Map008.json`
                      is the new map now, so this is the only copy of the input
                      outside git history. `grow2.py` reads it, `finish.
                      old_events` reads it to decide where the range is drawn
                      around the old events, and `decor.py` and `review.py`
                      both diff against it
      generated.json  the template worldgen produced, seed `w7`. NEVER EDITED
      generated.meta.json   its sidecar: the spec it was grown from, and a
                      marker per site with the stamp and the door cell
      finish.py       the hand-pass operations: mend a coast, isolate a rock,
                      dig out a buried square, draw a range, restamp a town,
                      drown an islet. Nothing in here decides anything
      run_finish.py   the decisions. Always starts from `generated.json` and
                      writes `worldmap.json`, so every edit is a line of code
      round11.json    Mike's editor pass of 22 Oct 2026, every cell he changed
                      on all four tile layers; `run_finish.py` lays it after
                      `settle`, so his autotile shapes are kept as drawn
      round12.json    his pass of 27 Oct 2026, laid the same way after it: the
                      Barrow moved east to (76,54), the sea and the Middle
                      Distance reshaped, the road to the Crag taken up
      round13.json    his pass of 30 Oct 2026, laid after that: the forests
                      and ranges near the middle made less symmetrical
                      (layer 1 only, 77 cells)
      worldmap.json   the finished map. **This is Map 8**: `journey.world_map`
                      loads it, so a rebuild of the game picks up whatever
                      `run_finish.py` last wrote. Never edited by hand
      review.py       old map against new: which events changed access, which
                      sites are unreachable, what is stranded
      reach.py        the flood fill both of those use
      place.py        put the party and the airship somewhere they can stand
      coords.py       every world-map coordinate the 37 scenarios name,
                      checked against the finished map in under a second.
                      The suite is the ground truth and takes 169 minutes;
                      this asks the cheap half of the same question, and the
                      signature it hunts is "unconverted" - not standable now,
                      standable at `+ (35,35)`. Non-zero exit on a stale one
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
| Penultima | ~~(82,48)~~ **(64,48)** | Town B | `BIOS.md` Gideon Markup - moved onto the tower road (7.2), and **built**: Maps 29-30, `build/penultima.py` |
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

**The forest corridor stays open, and the range has quietly dealt with it.**
You can still walk from Thistlewick to the Tower without entering the
Gloamwood, and that is deliberately left alone. But it is no longer a *short
cut*: measured on the finished map it is **177 steps against 48 on the 50x50**,
where the route through the wood is 50 either way. The hand-drawn range stands
where the old corridor at x11..24 ran, so this paragraph's own "will be closed
some other way later" has happened by accident - what is left is the long way
round, which is what it was always supposed to be.

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

## 6. What was left to do - items 1-9 done, item 10 left

**Items 1-9 are done.** Items 1-5 were the map and items 6-9 the game, and
what each of them turned out to be is below - because **eight of the nine found
something the plan had not predicted**, which is the single most useful fact
about this list. Two of those were faults the plan would have shipped (a trunk
road cut by accident, a lighthouse door opening into the sea), two were claims
in this document that measurement disproved (the northern road's connectivity,
and everything being twice as far), and two were wrong objects that only a
contact sheet of tile ids could see. **Item 10, the quests, is what is left**,
and it is larger than everything above it.

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

6. ~~**`places.py`**, rewritten~~ **Done.** Every world-map coordinate in it was
   re-cut, and with it **every exit back onto the world map**: thirteen
   `Transfer Player` commands across twelve maps name Map 8, and not one of
   them was written out - each is `R.transfer(MAP_WORLD, *WORLD_SOMETHING_STEP)`
   - so it was one file and a rebuild. `validate.py` floods each map from its
   transfer destinations, so **"no problems found" on the whole game is the
   check** that all thirteen land on standable, reachable squares.

   **There are fourteen, not thirteen.** The count in this item was of
   `Transfer Player` commands and missed a **`Set Vehicle Location`** - the one
   in the works on Map 22 that parks the Two Hundred on the world map when Ott
   hands her over, which is `WORLD_AIRSHIP` and is now (45,48). It is the only
   world-map coordinate in the data that is not a transfer, and it moved with
   the rest because it was written as a constant too.

   The three things that stopped it being a `+35` sweep, and what they came to:

   * **Four did not move by 35 and one of those moved twice.** Thistlewick
     (60,79), Nether Sopping (71,84), Upper Clanging (44,47) and the
     Lighthouse - which is **(79,80)**, not (76,79) and not `+35`, because item
     1 moved it out onto its headland.
   * **The `+1` convention broke for two of them, in the direction predicted.**
     `run_finish.py` gives Thistlewick and Nether Sopping road spurs to their
     **north**, so `WORLD_VILLAGE_STEP` went from two rows *south* of the icon
     to one row *north* of it, (60,78), and `WORLD_SOPPING_STEP` likewise to
     (71,83). Both are on road.
   * **Every destination was checked with `flags & 0x0F == 0`** against the
     finished map before it went in the file, and the four world-map signposts
     read as *blocked* - correctly, because a `WB_SIGN` tile blocks its own cell
     and is read from beside it, which was true on the 50x50 too.

   And two things the plan had not predicted:

   * **Three of the four signposts were hand-written coordinates, not
     constants**, buried in `journey.py` and `wilds.py`. They were the only
     world-map events this rewrite could have silently missed, and they are
     `WORLD_SIGN_SOUTH`, `WORLD_SIGN_NORTH` and `WORLD_SIGN_COAST` now.
   * **The `wilds.py` entanglement dissolved.** `first_coast =
     WORLD_VILLAGE_STEP[0] + 2` was drawing code deriving a coastline from a
     place constant, and it lived in `south_ground`, which item 7 deleted. The
     coordinates and the drawing are cleanly separated because the drawing is
     gone.

   **And one of the thirteen was wrong, and the tool that should have caught it
   was looking the other way.** The Lighthouse's way out is written "one square
   south of the door", and item 1 had just moved the Lighthouse onto a spit of
   rock that runs east - so one square south of the door is **the sea**, and
   coming out of the lighthouse put the party in the water. `validate.py` said
   no problems: it floods each map from its transfer destinations, and a flood
   *filters* its seeds, so a seed in the sea contributes nothing to the flood
   and is never mentioned while the other twelve entrances cover the map. Three
   lines above that filter sits a function whose whole docstring is about this
   fault. It is an assertion now, not a filter, and the check found one further
   true positive on the engine's own BasicSample. The Lighthouse has a
   `WORLD_LIGHTHOUSE_STEP` of its own - (78,80), back along the spit - which is
   the only curiosity on the map that needs one. **A check that silently skips
   what it cannot handle is not a check.**

   `places.py` also now holds the **six region ids**, which
   `finish.paint_regions` imports and `journey.world_map`'s `encounters=` names.
   A region painted with a number no encounter entry names is a region with no
   battles in it, which is the fault item 3 existed to fix, so it is not a
   thing to keep two copies of.
7. ~~**`journey.py` loses its world map.**~~ **Done, and it was smaller than
   feared for one reason worth knowing.** `world_map()` is now forty lines that
   load `build/worldmap/worldmap.json`, put this game's header on it and merge
   this game's events into it. The nine drawing hooks - `south_ground`,
   `south_layer1`, `south_layer3`, `south_regions`, `north_ground`,
   `north_layer1`, `north_layer3`, `north_regions`, and the meadow's two - are
   deleted, with everything that only they used: `_upland`, `_air_only_ground`,
   `AIR_ONLY`, `RAINBOW`, and `wilds.REG_COAST` / `field.REG_CLANG`, which
   `places.py` owns now.

   **And installing the map made the generator's own input become its output.**
   `data/Map008.json` *was* the old 50x50; the moment `journey.world_map` began
   loading `worldmap.json`, that file became the 120x120 map - and **four things
   were still reading it as "the old map"**:

   | reads it as the old 50x50 | what went wrong |
   | --- | --- |
   | `grow2.py`'s `SRC` | would blit a 120x120 map into a 120x120 canvas at an offset of 35, so `generated.json` stops being reproducible from it - which 7.6 promises it is |
   | `finish.old_events` | feeds `draw_range`'s `keep=`, so **the range moved**: re-running `run_finish.py` produced a world **106 layer-1 cells different** from the committed one |
   | `decor.py`'s baseline | diffed the new world against itself and reported **107 casualties** that were not there |
   | `review.py`'s old half | reported "old 1 walkable" and **48 events as having changed access** when none had |

   Only the second of those changed anything, and it changed the map. So the
   50x50 is frozen as **`build/worldmap/old50.json`**, committed beside
   `generated.json` and never edited, and all four point at it; `run_finish.py`
   now reproduces `worldmap.json` byte for byte again, which is the proof the
   snapshot is the right file. `old_events` asserts its input is 50x50 so this
   cannot happen quietly a second time.

   **The general shape is worth more than the incident.** A build that replaces
   a file with something derived from that file has a window in which every
   reader of it is reading the wrong generation, and nothing in the data says
   so - two of these four were *checks*, which is the worst place for it. If a
   pipeline's output can land where its input used to live, freeze the input.

   **The seventy-four hand-written tile writes were mostly not lost, because
   `grow2.py` preserved layers 0-3 of the old 50x50 and not just its terrain.**
   Every `_STEP` cell still has its road under it; the coast road at y=81 is
   walkable end to end; the rainbow, the wayshrine's hut, the Isle's sign,
   Attempt 112's rock and the four standing stones are all still there. So
   deleting the drawing deleted tiles only where the *middle redraw* had already
   taken them - which is the thirteen `decor.py` counts, all of which are back -
   and under the hand-drawn range. That is why this item cost a morning and not
   a week, and it is the single most useful thing to know before touching it.

   Two decisions about the merge:

   * **This game's events keep their ids and the placeholders are renumbered
     after them.** `worldmap.json` arrives with **41 placeholder door events**
     on its 29 sites, and an event id is an index into the map's own list, so
     one set has to move. Moving the placeholders is strictly safer: their pages
     have no commands, so nothing can refer to them, whereas a scenario or a
     move route naming an event id on Map 8 refers to one of ours. It paid off
     immediately - `airship_lands` asserts `eventId()` is 4, 20, 21, 22 and 23,
     and all five still are. Map 8 is 28 game events (ids 1-28) then 41
     placeholders (29-69).
   * **The placeholder doors are inert.** A door that chimes and goes nowhere is
     right on a review map and wrong in a shipped one; 41 of them is a sound
     effect that promises a room and never delivers. `finish.make_doors_inert`
     strips each page to its terminator - `Game_Event.start` needs
     `list().length > 1`, so it never runs, and `validate.py` exempts a page
     with no commands - and folds what the page said into the **note**, which
     the editor shows and nothing executes. Writing the transfer later means
     replacing the page with `worldgen.sites.transfer_page`. It is done in
     `run_finish.py` rather than in `journey.py` so the staged map and the
     installed map behave the same.

   **The record of what the thirteen casualties were, and the four nudges, is
   below and is still the check to re-run.**

   | what | old | new | outcome |
   | --- | --- | --- | --- |
   | The Hermit's hut (`WB_HUT`, a `Tent`) | (40,29) | (75,64) | restored |
   | Meredith Crooke's camp tent (`WB_HUT`) | (11,32) | (46,67) | restored |
   | **The Bottomless Pit's cave mouth** (`WB_CAVE`, `Cave A`) | (8,35) | (43,70) | restored |
   | Giant Tree scenery (`WB_TREE`), 7 cells | (40,21) (37,22) (9,25) (34,29) (7,33) (44,33) (12,35) | `+35` | 3 as asked, **4 nudged** |
   | Rock scenery (`WB_ROCK`, `Dirt`), 3 cells | (36,13) (7,22) (31,31) | `+35` | restored |

8. ~~**The scenarios.**~~ **Done.** **Fifteen** of the thirty-six touch the
   world map - one more than anybody had counted - and every one of them is
   updated and passing, plus a new sixteenth. Most were a `+35` sweep on
   a `goto`, a `query` string or an `expect`; three needed thought:
   * **`airship_lands` is the one that mattered**, and it came through on `+35`
     alone - every `isAirshipLandOk` assertion in it still holds, including the
     two that are the joke (the tower door refuses her, the grass beside it does
     not) and the Middle Distance's hill, which only holds because item 4 put
     that hill back. Its five `eventId()` assertions still hold too, because
     item 7 renumbered the placeholders rather than our events.
   * **`south_road`'s shingle check was wrong rather than stale**, and it is the
     one place the new geography changed what is true. On the 50x50 the beach
     was a two-row scan of every southern column and the coast road ran *on* the
     sand, so the walk east was crab country; the 120x120's shore falls away to
     the south-east and the road stays inland of it, so only two of its thirteen
     cells are shingle. The check now asserts the pair - the road is region 1
     and the beach three rows below it is region 3 - which is a stronger check
     than the old one and says the true thing: **you step down onto the beach to
     meet the crabs.**
   * **`gate`'s position check moved to the other side of the town**, per item
     6's `_STEP` change, and its `regionId` check passes unaltered.

   **The coordinates hide in three places and two of them are not obvious.**
   A first pass over the `"expect"` arrays and the `"goto"` steps looked
   complete and was not: `airship_lands` then failed with no useful output,
   because a scenario's coordinates also live
   * **inside `eval` strings** - `$gamePlayer.locate(31, 8)`,
     `$gameMap.airship().setLocation(8, 10, 13)`, `$gameMap.regionId(9, 16)`,
     `$gameMap.isAirshipLandOk(22, 48)` - which no amount of looking at
     `expect` will find; and
   * **in the `"query"` string**, the `?map=8&x=..&y=..` that says where the
     scenario starts. Six were still on old coordinates, two of them in
     scenarios (`long_field`, `battle_mook`) that no search for `goto` or
     `mapId` had turned up at all, because they *begin* on the world map and
     never mention it again.

   So the sweep was done properly the second time, by walking each scenario's
   steps, tracking which map it is on through its query, its `goto`s and its
   `mapId()` checks, extracting every coordinate-bearing construct while that
   map is 8, and flagging any that is **not standable now but would be at
   `+ (35,35)`** - which is a near-perfect signature for "unconverted".

   **And the sweep still missed one, for a reason worth stating.** It matched a
   position check by looking for `gamePlayer.x`, and `two_hundred` asserts where
   the **airship** is parked - `[$gameMap.airship()._x, $gameMap.airship()._y]`.
   A position check is not necessarily about the player. The full suite caught
   it (36 of 37, one failure, fixed) and the sweep now matches any check that
   reads an `_x`/`.x` and an `_y`/`.y` together, whoever it is about, which
   takes it from 51 world-map coordinates to **64**. Fifteen scenarios carry
   them; one flag remains and it is a true negative -
   `isAirshipLandOk(37, 40)` expecting **false**, which is Attempt 112's rock
   and is supposed to be unstandable.

   The suite is the ground truth and there was no substitute for running it:
   **37 of 37 passing, 498 checks, 169 minutes** - and the one failure was
   scenario thirty-six of thirty-seven, which is what three hours buys that a
   second-long check does not. `coords.py` is that second-long check, written
   afterwards so the next map change gets the cheap answer first.
   One new scenario, **`placeholder_doors`**, because item 7's inertness is the
   kind of thing that stops being true the day somebody wires the first real
   transfer and nothing else would say so. It asserts out of the live game that
   there are 41 site doors, that every page of every one of them has no
   commands, that the note carries what the page used to say, and then walks
   onto two of them - Frostwick's and Village 1's - and checks the interpreter
   does not start. Six `<aironly>` events are counted off the data in the same
   pass.
9. ~~**`encounterStep`.**~~ **Nothing to do, and the premise was wrong.** This
   item said everything is about twice as far - "Thistlewick to the Tower goes
   from ~40 steps to ~81" - and that step 36 would therefore double the battles
   on the trek north. **Measured on the finished data, by flood fill, it is not
   true.** The old 50x50 is preserved inside the new map at an offset, so the
   *relative* geography of everything this game already has is identical, and
   every leg is the length it was. From the Gloamwood's north mouth: the tower
   door 26 steps against 26, Upper Clanging 15 against 15, the crag 22 against
   22, the Long Field 10 against 10, the Standing Stones 8 against 8, the
   wayshrine 16 against 16, the Barrow 19 against 17. The world-map half of the
   quest is **50 steps against 51**. `encounterStep` stays at 36.

   It was briefly changed to 72 on the strength of this item before anybody
   measured, which would have quietly **halved** the encounter rate of the
   shipped game on a route that had not changed length - so the note is worth
   keeping: *the map got bigger and the game did not get further apart.*

   What did get longer is the **short cut**. Walking to the tower without
   entering the Gloamwood was 48 steps on the 50x50 and is **177** now, and the
   Barrow the same way went from 37 to 192, because the hand-drawn range stands
   where the old forest corridor was. Section 4 wanted that corridor closed
   "some other way later"; the range has effectively done it, and what is left
   is a long way round rather than a shortcut. Nothing is tuned for it and
   nothing needs to be.
10. **Then the new quests**, which is what the whole thing is for.
    **Penultima is the first and is finished**: Maps 29-30
    (`build/penultima.py`), Gideon and Dorothy Markup rendered with
    `tools/chargen` into `Gen_People1` 4 and 5, a scenario that walks the
    whole way in from the world map and back out (39 checks), and 7.6's
    settled answer to how a placeholder becomes a door. Three things it found
    that the next site will hit too:
    * **Five `mapkit` furniture constants are named for what they looked like
      at forty-eight pixels and are something else** - `IN_COUNTER` is the
      shelf with teddy bears on it, `IN_TABLE_SMALL` is a broken stool,
      `INC_BOOK` is a *closed* book under a line about writing in a ledger.
      `tools/propsheet.py` over the new room found all five in one look, and
      the workspace's `TILES-AND-ASSETS.md` now lists them with what to use
      instead. **Run it over any new interior before believing the room.**
    * **A display that is legible in the catalogue can be illegible on the
      map.** `Sword Rack A` on a red-draped plinth is exactly what the bio
      describes and reads as a red drum at map scale, because the swords lie
      flat and the cloth is the only thing with area. Only a screenshot finds
      that, and the fix was a wall mount.
    * **A player-touch event on the route home eats the walk.** Penultima's
      Sighting Bell is on the lower row of the street, so a scenario walking
      back to the gate along it stops dead and every arrow press after that
      goes into a message window. It reads exactly like a dropped press and is
      not one; the route goes along the other row.

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

### 7.2 Four whose bios asserted a geography the map did not honour - **all four re-sited**

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

### 7.3 A snow town, which is new - **placed at (61,21)**

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

**The cast.** Six people, written to `NORTH.md` section 1, which this game's
`CLAUDE.md` calls the law for every line of its humour and not only the
north's. Nothing below is built; this is the stage the synopsis above said was
owed, and it is what a `frostwick.py` would be written from.

**First, a correction the synopsis needs, because the fix is one word.** 7.3
says the curse was broken "by a Chosen One two or three numbers back". That
cannot be true and it is worth saying why rather than quietly editing it: the
Dark Lord rises **every hundred years**, Bram is forty-eight, so two or three
numbers back is two or three *centuries* back and not forty years. The hero
who broke Frostwick's winter is therefore **not a Chosen One at all**, and the
version that is both true and funnier is already established elsewhere in the
game - `EXPANSION.md` is explicit that **everybody** went north, not just the
Chosen Ones, and the Sopping harbour memorial has a hundred and eighty-one
names against the Wall's forty-seven portraits. He is one of the unnumbered.
He went north with everyone else, he never got anywhere near the Tower, and on
the way he solved somebody else's problem entirely and has been a hero of that
town ever since. Frostwick has spent forty years calling him a Chosen One
because it is better for the Festival, and he has spent forty years not
correcting anybody, which is a smaller and more embarrassing thing to be
gracious about than a victory. **This also pays off the 181-against-47 count
that 7.5 leans on**, from the other end: Thistlewick cannot account for the
difference, and here is one of the difference, opening a fete.

* **Percival Stagg**, who broke it. Everybody calls him Perce. He opens the
  Festival, cuts the ribbon, and does the face he has been doing for forty
  years - which the town can describe precisely, because it is the same face.
  He is not diminished by any of this and must not be written as though he
  were (1.6): he won, he retired somewhere nice, and he married well. The
  ribbon is the same ribbon, re-tied annually, and kept in a case. There have
  been forty of them and there has been one.
* **Ida Stagg**, his wife, who thinks the whole arrangement is very funny and
  has said so to exactly one person. She is **the Register A carrier of the
  town**, by mechanism 1 - the innocent superlative offered as praise. The
  line to aim at is her, mildly, on the subject of the ribbon: that he did one
  great thing forty years ago and has done a great many things since, and
  none of *those* ever got a ribbon. It is a compliment, it is defensible as
  literal, the game never says anything, and the marriage is plainly a good
  one, which is 1.2 exactly.
* **Clem Blagg, aged seven**, the leaky child (mechanism 2), and the reason
  the town can be funny without anybody in it saying anything. The committee
  minutes live on his nan's table, so he has read them, and he reports at
  volume, in company, in the wrong order. He thinks the subject is the
  lanterns. He is the one who says the thing about Mr Stagg that his nan said
  in the kitchen, and the room looks at the ceiling - which is the machinery
  the tavern already has for Perpetua and which 1.3 item 6 says to reuse.
* **Mrs Wilhelmina Blagg**, chair of the Festival committee, his grandmother,
  and the town's pride in the arrangement made flesh. Her register is parish
  bureaucracy played entirely straight: the curse is **an asset**, it is on
  the asset register, and there is a depreciation schedule. She is the reason
  Frostwick is written in Great Dunnage's register rather than Thistlewick's -
  a place that is pleased with itself.
* **Eudora Pargeter**, the retained practitioner, nine years into a contract
  she would renew tomorrow. She is not an ice witch and would like that on the
  record; her speciality is **refrigeration**, which is a trade with
  customers, a season, and a great deal of paperwork. She does the whole of
  January in an afternoon and is home by four. Her half of the joke is that
  she is the only person in the story who has read the contract, and the only
  one with no feelings about the curse whatsoever.
* **Mrs Tibby Marchpane**, of the **Eleven Days** - the inn, named for the
  thaw, which is a thing you can only name an inn after in a town that took
  the other decision. She keeps the **visitors' book that has been signed by
  three Chosen Ones**, and will show it to you, and the third signature is the
  one worth reading twice.

**The accidental record** (mechanism 4) is where most of this should actually
land, because it is the cheapest thing on the list to build and the hardest to
get wrong: the **schedule of snowfalls**, an appendix to the contract,
specifying depth, duration, and a light dusting for the ribbon; and the
**minutes** of the working group, which record a vote, a division, and an
abstention. A document does not know what it is saying, and neither of these
needs a face.

**And the eleven days are commemorated**, on the wall of the Eleven Days: a
mark at the height the snow reached during them, which is the floor, under a
brass plate giving the year. It is a sight, not a person, and it is the whole
town in one object.

**What this costs.** Six faces - and only four of them have to speak to be
worth building, because Perce, Ida and the child carry the register and Mrs
Blagg carries the premise, while Pargeter and Marchpane can be a shop and a
bed with two conversations on them. The interiors it implies are the inn, the
parish room (minutes, asset register, chair), the practitioner's cold room and
the Staggs' house, which is four and is one more than Upper Clanging needed.
**Register A count: one moment**, the child's, which bumps variable 7 like
every other and adds nothing to the ending's nine blocks - a new town feeds
the counter, it does not earn a block (`COMPANIONS.md` 7's first risk).

### 7.4 One floating continent - **placed at (79,88)**

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
complaint moot four thousand eight hundred years late. That is the whole joke and it lands the
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

**The cast, and it is one man and a great deal of paperwork.** The synopsis
above says "somebody is still up there", singular, and the singular is the
joke: a castle with a staff of one, kept ready for a tenant who left four
thousand eight hundred years ago. Filling it with people would make it a place rather than a
**vacancy**, which is the thing the player is supposed to be standing in.

* **Mr Prosper Hollowell, Caretaker (Retained).** He has kept the place ready
  since the lease lapsed: the hall swept, the sconces lit, the book open on
  the lectern. He is not bitter and he is not mad - both are specified in 1.6
  and in the synopsis, and both would be easy to drift into, so the rule for
  writing him is that **every single thing he says is good news**. A Chosen
  One has arrived. He begins the tour immediately. It is a very good tour and
  he has been working on it, and the correct player experience is to be
  slightly unable to leave.
* His title is the rhyme, and it is deliberate: Frostwick has a **retained
  practitioner** and the Premises has a **retained caretaker**, and they are
  the same joke from the two ends the spine already runs between. The Prophecy
  is a contract; this is its estate management and its facilities budget.
* **The quarterly reports.** He writes them. They are filed. The replies are
  form letters, and one of them - recent, on the lectern, and the only thing
  in the room he is not pleased about - is a **change of address notification**
  for the Obligatory Tower, sent to him as a matter of course by a committee
  that has not thought about this building in four thousand eight hundred
  years.
* **The visitors' book, open, with nobody in it.** Not a single name in four
  thousand eight hundred years, because nobody could get here, which is the complaint that
  closed the place. And it is the one gap in his record, so he has an **ask**:
  when the party reaches the current incumbent, would they have him sign it.
  That costs one item, one page on Grimspite, and it lands at the finale -
  a four-thousand-eight-hundred-year-old contractor being asked to sign a
  guest book for a building he has never seen and has inherited opinions about
  entirely from paperwork.
* **The lift.** This is the sight the whole place is for. The accessibility
  complaint was upheld, a recommendation was made, and a lift was duly
  commissioned and installed - **inside the castle**, from the courtyard to
  the battlements, where it works perfectly and always has. The climb that was
  complained about was the one from the ground, which is four thousand feet of
  sky and was never what the works order said. Nobody noticed, because by the
  time it was finished the engagement had been renegotiated onto a ground-floor
  site. It is a committee solving the wrong climb, minuted, and it is funny
  without a word of dialogue.
* **The deeds**, which name the builder - **Malagant the Provisional** - and
  which are **Ott's payoff**. She gets to ask what holds it up. The deeds say
  "as before". There is no before.

**No Register A here, and it must not be forced.** There is one man in the
building and he is delighted; there is no couple, no household news and no
leaky child, so mechanisms 1, 2 and 6 have nothing to work with, and reaching
for the second reading with a lone caretaker would be a wink, which 1.2's
corollary puts out of bounds. The Premises is **Register B and contract
comedy** - which is the register the game is already very good at - and the
right thing is to let it be. It bumps variable 2 (`story.trope`) for the
floating castle of the ancients and variable 7 not at all.

**What this costs.** One face, one interior, and the finale page. That is the
cheapest site in this document by a wide margin, which is worth knowing when
the build-out is prioritised: it is the only air-only destination in the game,
it is the thing that makes the Two Hundred worth having flown, and it needs
less work than any of the six `BIOS.md` towns.

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
9. **Signposts** (`Signboard A-D`, `Sign`). There are five on the map and the
   world is much wider than they cover - **not** "everything is twice as far",
   which section 6 item 9 measured and disproved, but the *unvisited* country
   genuinely is all new and unmarked. A sign is a joke vehicle this game already
   owns: Fizz appears in front of every one you try to read.
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

### How a placeholder door becomes a real one - **settled**

The constraint is a pincer and is worth stating before the answer. The doors
live in `worldmap.json`, which `run_finish.py` owns and which has to stay free
of game content - a transfer names a map id and a square inside a room this
map knows nothing about, and putting one there would make the world map a file
that cannot be regenerated without the game. But `journey.world_map` only
*merges* what it finds. So **the transfer cannot be written where the door
is**, and something has to bridge the two.

**Settled: the game claims a site by name, and the placeholder is dropped
rather than rewritten.** A module that builds a site exports two things - a
`SITE` string, which is the name `finish.add_site` gave that site's door
events, and a `world_doors(base_id, cells)` function. `journey.world_map`
collects the cells of every placeholder carrying a claimed name, drops those
placeholders, and calls the module to build real doors on **exactly those
cells**, inside this game's own block of events. Penultima is the first, and
`build/penultima.py` is the shape to copy.

Four things fall out of it, and three of them are the reason it was chosen
over the alternatives:

* **The world map keeps the geometry and the game keeps the destination.**
  The module is *handed* the squares; it does not know them and must not write
  them down. 7.2 moved Penultima forty-two cells west after the map was
  reviewed, and a coordinate copied into `places.py` would have gone stale in
  silence - which is section 6 item 7's lesson in a new place. `places.py`
  therefore has **no `WORLD_PENULTIMA`**, only the square the player is put
  back on coming out, which is the game's own decision.
* **A real door is one of ours, so it gets a stable id and the game's own
  idiom.** It sits in the block before the placeholders, numbered like
  Thistlewick's and the Gloamwood's, and it is written the way this game
  writes a door - narration, then a Go in / Press on choice - rather than as
  `worldgen.sites.transfer_page`, which is a bare transfer and reads nothing
  like the rest of the map.
* **The placeholder count goes down, and `placeholder_doors` is the check that
  notices.** It was 41 and is 39, because a `Town B` stamp is two cells and
  both of them became doors. That scenario asserts the count, and asserts that
  every *remaining* placeholder still has no commands on any page - so the day
  somebody half-wires a site, it says so. Adjusting the number is part of
  wiring a door, deliberately: a check nobody has to touch is a check that
  stopped meaning anything.
* **A claim that matches nothing is an assertion, not a no-op.** If the name
  is misspelled or the site is renamed, the filter drops nothing, the module
  still builds its doors, and the map ends up with a real door and an inert
  one on the same square - which builds, validates and looks correct.
  `world_map` asserts that every claimed name matched at least one
  placeholder. Section 6 item 7's general shape again: *a check that silently
  skips what it cannot handle is not a check.*

**Two alternatives, and why not.** Rewriting the placeholder's page in place
leaves a real door sitting in the renumbered tail with a `<worldgen-site ...>`
note still on it, so `placeholder_doors` needs a per-event exemption and the
event's id moves whenever a site ahead of it is wired - both of which make the
next wiring harder than this one. Writing the transfer into `run_finish.py`
puts game content in the map file and is what 7.6 exists to forbid.

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
  **Deferred a third time, on purpose** - `SITES.md` step 9 put the question
  to Mike, and he chose to keep it standing until every other site is built.
  It is now `SITES.md` section 4 item 6, to be decided before the push to
  `live-rpg`.
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
* **The Cinder Fen's tile (47,118).** Mike placed `House (Desert)`, layer 3
  (`round11.json`, `[47,118,[3240,0,0,142]]`), on a one-cell strip of cracked
  mud between rock, two roads and the lake. **Kept as it is (28 Oct 2026);
  Mike may experiment with it later.** What was tried, on a scratch copy only:
  * A1 kind 4, `Poison Swamp`, on layer 0 at (47,116)-(47,118), with layers 1
    and 3 cleared on those cells and `autotile(0, kinds=[4])`, reads as a fen
    strip. The best of three mockups added `Forest (Dead Trees)` (A2 kind 12,
    id kind 28) on layer 1 at (45,117), (46,117) and (46,118), with
    `autotile(1, kinds=[28])`: three dead trees on the rock beside it. Both are
    walkable.
  * **What does not work.** A1 kind 5, `Dead Trees`, is waterfall-format, so
    it draws as a hard purple square unless it sits inside a swamp at least
    3x3, and there is no room for one here. A wider swamp (2x3, or an L)
    shows sand-coloured edge rims against the Rocky Land.
  * To apply it, edit the cells in `build/worldmap/round11.json` (replace
    (47,118), add the others) and rebuild.
