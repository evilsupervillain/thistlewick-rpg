# The places behind the doors

`WORLDMAP.md` section 6 item 10. The 120x120 world map carries **29 sites whose
doors were placeholders**; one of them - Penultima - is built, and this document
is the ordered work list for the other twenty-eight.

It exists because item 10 is larger than the whole of the map work that produced
it, and because it is a *queue* rather than a design: the design for each site
is already written down somewhere else, and the job here is to say what, where,
in what order, and how to know when one is finished.

---

## 0. How to work on this

**These are the rules for this effort specifically.** They are deliberately
looser than the ones the map work ran under, because the map was one artefact
that had to be right all at once and this is twenty-eight independent rooms.

* **Nothing here has to be atomic.** A site can be built while the thing it
  eventually pays off does not exist yet. If Mrs Ashbury's inn is built before
  Merribell's quest that sends you there, the inn is simply an inn for a while.
  Partially done is a legitimate state to leave a site in, and to leave the
  *list* in. Say so in the step's line when you do.
* **Do not run the full scenario suite between sites.** It is about 170 minutes
  and it is the wrong check for this work. Run it **once, at the end**, when the
  pieces are in place. The exception is narrow and real: run it early if there
  is a **specific** reason to think something has broken in a way that gets more
  expensive to find later - a change to `journey.world_map`, `story.py`,
  `places.py`, `db.py` or the ending, rather than a new module of a site's own.
* **What to run per site instead**, cheapest first, and it is enough:

      python3 build/build_game.py
      python3 ../tools/validate.py .
      python3 build/worldmap/coords.py                  # ~1s
      python3 ../tools/propsheet.py . /tmp/p.png <new map ids>
      node ../tools/shots.js /tmp/s <map>:<x>:<y> ...
      node ../tools/scenario.js build/scenarios/<site>.json

  The site's own scenario, and only it. `propsheet.py` over any new interior is
  not optional - see 3.
* **Commit per site, freely.** A commit is not a publication. **Nothing is
  published until it is pushed to the `live-rpg` branch** of
  `github:evilsupervillain/thistlewick-rpg`, which is the branch the playable
  game is served from. `master` can be as far ahead of it as it likes; as of
  this writing it is six commits ahead. Push to `live-rpg` at the end, after the
  suite.
* **Speed is the priority.** Prefer the shape that already works over the shape
  that would be nicer. `build/penultima.py` is the reference and copying it is
  the right instinct.

## 1. What building a site actually is

Penultima is the worked example and `build/penultima.py` is the template.
`WORLDMAP.md` 7.6's last subsection is the reasoning; this is the checklist.

1. **A module per site or cluster**, `build/<name>.py`, with a `build()` that
   saves its maps. Import it in `build_game.py`, add its maps to `MAP_NAMES`.
2. **Map ids continue upward from 38.** Penultima took 29 and 30, Restwell
   31 and 32, Hithermost 33 and 34, Fairholme 35 to 37. Never renumber.
3. **The door is claimed by name, not by coordinate.** The module exports
   `SITE = "<the name worldmap.json's door events carry>"` and
   `world_doors(base_id, cells)`; `journey.world_map` drops the placeholders
   carrying that name and hands the module *their* cells. **Never copy a site's
   world-map coordinate into `places.py`** - only the square the player is put
   back on coming out.
4. **`placeholder_doors.json`'s count goes down by the number of cells you
   claimed**, and you edit that number on purpose. It is 30 now. That scenario
   is the check that notices a half-wired site.
5. **A scenario that walks in from the world map and back out.** Not
   `$gameMap.event(n).start()` - walking is the only thing that proves the door
   swap landed on the right squares.
6. **Faces.** `build/art.py`. **`Gen_People1` is full** - Restwell took the
   last two cells - so the next site that needs a generated face adds a
   `Gen_People2` to `SHEETS`, which is one line. A face can also be *shared*
   rather than drawn, which is what Dr Pike does; `story.FACES` records every
   such share and why. Six `BIOS.md` characters already have settings files in
   `build/characters/`; everybody else has to be drawn with `tools/chargen`,
   which is about fifteen minutes per person including looking at the result.

**Two traps that are specific to this work:**

* **A real door replacing an air-only placeholder must keep `<aironly>` in its
  note.** `validate.py` reads that note to assert on foot that the place cannot
  be walked to. Drop it and the assertion silently stops being made. This
  applies to exactly one site, **The Former Premises**, and to nothing else.
* **A site that is `<noairship>` or on a stamp with only one standable cell has
  the airship rules of `WORLDMAP.md` 6.4 on it.** Again, only the Former
  Premises.

## 2. The order

Cheapest and most certain first. The two principles are **the face bill decides
the cost** - a site whose cast is already drawn is a fraction of the work of one
that is not - and **one module per session**, so a step is a session.

| # | step | sites | maps | new faces | source |
| --- | --- | --- | --- | --- | --- |
| — | ~~Penultima~~ | 1 | 2 | 0 | **done** |
| — | ~~Restwell~~ | 1 | 2 | 1 | **done** |
| — | ~~Hithermost cluster~~ | **3** | 2 | 1 | **done** |
| — | ~~Fairholme and the lair~~ | **2** | 3 | 1 | **done** |
| — | ~~Olde Evermore~~ | 1 | 2 | 1 | **done** |
| — | ~~Gladhollow~~ | 1 | 2 | 1 | **done** |
| — | ~~The Former Premises~~ | 1 | 1 | 1 | **done** |
| — | ~~The seven with no map~~ | **7** | **0** | 1 | **done** |
| — | ~~Tobias Frayne~~ | 1 | 1 | 1 | **done** |
| — | ~~Village 1~~ | 1 | 0 | 0 | **deferred to section 4** |
| — | ~~Frostwick~~ | 1 | 4 | 6 | **done** |
| — | ~~Coldbarrow~~ | 1 | 1 | 1 | **done** |
| — | ~~The Sable Hart~~ | 1 | 1 | 5 | **done** |
| — | ~~Little Gore and Sump~~ | **2** | 2 | 2 | **done** |
| 14 | Ashcombe | 1 | 2 | 2 | `COMPANIONS.md` L3 |
| 15 | Weeping Bottom | 1 | 2 | 2 | `COMPANIONS.md` L4 |
| 16 | Fenmarch Hall | 1 | 2 | 2 | `COMPANIONS.md` L5 |
| 17 | The Collegium Arcanum | 1 | 3 | 3 | `COMPANIONS.md` L2 |
| 18 | Great Dunnage | 1 | 5 | 6 | `COMPANIONS.md` L1 |

**Twenty-eight sites, eighteen steps, about thirty-three maps.**

**`COMPANIONS.md` section 6 disagrees with this order and is worth reading
before overruling it.** It says build Great Dunnage second and the Collegium
third, because between them they unlock seven of the nine companions. That is
the right order if only *some* of this gets built. This list assumes all of it
gets built, so it optimises for momentum and for the face bill instead, and puts
the two big ones last - where their cost is known and the pattern has been
exercised sixteen times. If the schedule collapses, swap steps 17 and 18 forward.

**And the thing `COMPANIONS.md` 6 puts first is not on this list at all**, on
purpose: **sixteen of its forty-nine quests need no new map and no new site** -
they are appended pages on people who already exist. That is a separate,
cheaper effort with no doors in it, and four of the best jokes in the document
(MER-2, PIP-2, ROL-4, WRE-2) are in it. Do not let this list crowd it out.

---

## 3. The steps

Coordinates and stamps are `WORLDMAP.md` section 3, which is the authority.
Everything under "build" is sourced, not invented; where a source is thin, the
step says so.

### 1. Restwell — (43,81), `Town A`

`BIOS.md`: **Mrs Hester Ashbury**, landlady of **The Eight Hours**. A crossroads
town of one street and nineteen inns; hers is the one the songs are about. A
night restores everything and cures poison, blindness, curses and frogs, and on
one occasion death. Nobody has ever been seen asleep in the beds - guests go up
at noon, come straight back down fully restored, and insist it is morning, so
she serves breakfast at all hours. Her husband **Walt** plays a little tune on
the fiddle at the foot of the stairs every time somebody goes up, and after
twenty-six years she is no longer sure it isn't the tune that does it.

* **Build:** the street (1), the Eight Hours (1). An **inn** - Recover All
  behind a fee - which is why this is first: it is Penultima's shape with a
  different mechanic, and it proves the template generalises.
* **Faces:** Ashbury has one. Walt and the **town doctor**, who has no patients
  left and has taken a room himself for the rest, are new.
* Walt's tune is the site's Register A candidate and the marriage is a good one,
  which is the rule - `NORTH.md` 1.2.

**Done.** `build/restwell.py`, Maps 31 and 32, `build/scenarios/restwell.json`.
The template generalises: the module is `penultima.py` with the shop swapped
for `village.py`'s Gilded Turnip beds, and nothing about the door mechanism
needed a second thought. `placeholder_doors` is **37**. Four things are worth
carrying forward:

* **The face bill came out at one new drawing, not two.** `Gen_People1` had two
  cells and Restwell had three people in it, so the **Ashburys** took 6 and 7 -
  she was already drawn, he was made here - and **Dr Pike shares `SF_Actor3:6`**
  on the Halbert Quy and Winnie Marsden precedent. `Gen_People1` is now full and
  **step 2 opens a `Gen_People2`**, which is a line in `art.py` and not a
  problem.
* **Two blushes, not one**, so `VAR_BLUSHES` is now 28 reachable against a tier
  of 20 - 71%, under `NORTH.md` 2.3's four fifths. Section 4 item 5 is where
  that gets cut and it is still the right place for it.
* **A building's only face is its south side**, which decides the shape of a
  street with buildings on both sides of it: the south row has to be read from
  a lane *behind* it. The first draft put that row against the tree line and
  left its doorsteps in a sealed four-cell pocket. `validate.py` found it; four
  screenshots did not.
* **`INC_BELL` is a `Globe`**, found by `propsheet.py` over the finished inn and
  now recorded in `../TILES-AND-ASSETS.md` with the other five. `INC_DESK_BELL`
  is it corrected. `IN_TABLE_ONE` is a sixth of a different kind - it is the
  right object and is *illegible*, a red drape with no other detail, which at
  forty-eight pixels is a red drum.

### 2. The Hithermost cluster — (30,23)-(31,23), (30,22), (30,21)

**Three sites, four door cells, one module, one face**, which is the best ratio
on the list. **Hithermost** `Village A` at (30,23) *and* (31,23), **Chapel of
Continuance** `Temple C` at (30,22), and **The Door into the Mountain** `Tunnel`
at (30,21), stacked up the pass.

The names in bold are the `SITE` strings, read off `worldmap.json`'s door events
and not invented here - a claim that matches nothing is not a no-op, it leaves a
real door and an inert one on the same square. **`Village A` is two cells wide**,
which this heading said otherwise until somebody counted, so
`placeholder_doors.json` goes **37 → 33** and not 34. Count the cells of any
stamp before writing its number down; `SITES.md` section 1 item 4 is the rule and
this is the first step where it would have bitten.

`BIOS.md`: **Brother Quillon**, Keeper of the Record. A lectern, and on it the
Book, which glows. Travellers write their names in it "in case of misfortune",
go through the door, and quite often come back in through the porch and write
their names again. **Sir Dunstable of the Vale** has come in at a quarter past
four two hundred and twelve times, always says "Just in case", and always
explains afterwards, with some warmth, that nothing happened; Quillon now leaves
a cup of tea on the lectern for him at ten past. The Order's vows forbid exactly
one thing: saying that he remembers.

* **Build:** the pass village (1), the chapel (1). **The Door into the Mountain
  is a door and should stay one for now** - a refusal, or a dark tunnel with a
  reason not to go in yet. It is the obvious future dungeon and nothing here
  needs it to be one.
* **The Book is a save point.** That is what it is for and it costs almost
  nothing; the joke and the mechanic are the same object.
* **Faces:** Quillon has one. Sir Dunstable is new.

**Done.** `build/hithermost.py`, Maps 33 and 34, `build/scenarios/hithermost.json`.
`placeholder_doors` is **33**. What is worth carrying forward:

* **A cluster exports `SITES`, a dict of name to builder**, and
  `journey.world_map` merges it into `claims` with `**HM.SITES`. Three names,
  three claims, one module, and nothing else about the mechanism changed. The
  Door into the Mountain's world-map door is a *claimed* door that transfers
  nowhere - a refusal - which is legal: a claim replaces the placeholder, it
  does not have to go anywhere.
* **The Book is a save point**, `R.open_save_screen()` behind a choice, and a
  scenario cannot catch `Scene_Save` in the act: `advance` goes on pressing
  Enter inside it, which saves. `hithermost.json` counts openings with a spy on
  `Scene_Save.prototype.start` and asserts `DataManager.savefileInfo(1)`.
* **`places.py` already had a `MAP_CHAPEL`** - Thistlewick's, Map 5 - and
  defining a second one silently re-pointed `village.py` at Map 34; the build
  printed `dropped stray Map005.json` and that line was the only symptom.
  Grep `places.py` for a constant's name before adding it. This one is
  `MAP_CONTINUANCE`.
* **Pick the ground from the cliff's family.** `Ledge B (Dirt)` over `Meadow`
  grass is two materials; over `Grass (Dirt)` and `Road (Dirt)` it is one
  place. `A(25)`/`A(26)` have no `mapkit` constant and are local to the
  module. And `TREE_DARK` drawn free-standing on grass is a flat square of
  hedge, not a tree - `TREE` is the one that reads.
* **`Gen_People2` is open**: Quillon at 0, Sir Dunstable at 1. The Tolleys'
  entry in the Book is the blush, so `VAR_BLUSHES` is **29** reachable against
  a tier of 20 - 69%, and still section 4 item 5's problem.
* **`serve.js` needs an absolute root.** `node ../tools/serve.js . 8766` serves
  404 for everything - its prefix check compares a joined relative path
  against `"."` - and `shots.js` then times out on a probe that never loads.
  Pass `$(pwd)`.

### 3. Fairholme and Mrs Emberthwaite's lair — (104,73)-(105,73) `Castle A`, (111,69) `Cave A`

**Two sites, three door cells, one module**: they are one bio. **`Castle A` is
two cells wide** - measured off `worldmap.json`, which names them `Fairholme`
and `Mrs Emberthwaite's lair` - so `placeholder_doors.json` goes **33 → 30**.

`BIOS.md`: **Princess Rosamund**, kidnapped eleven times - twelve if you count
the eagle, which the Palace does not. She keeps a packed bag by the tower
window: a book, a cardigan, sandwiches, and a card listing her dietary
requirements "for whoever it is this time". Her father **King Aldous** posts the
traditional reward every time - her hand, or half the kingdom - and every
rescuer has very sensibly taken the half, so Fairholme is held in shares by nine
heroes, a knight, two farmers and a man who was only passing, and council
meetings now take all day and need a larger table. **Mrs Emberthwaite**, the
dragon on the hill, is retired, widowed and mostly wants someone to play cards
with; Rosamund has started going round on Thursdays without being carried, and
the rescue economy of three kingdoms is in uproar.

* **Build:** the council chamber with the larger table (1), her tower room with
  the packed bag (1), the lair (1).
* **Faces:** Rosamund has one. Aldous is new. **Mrs Emberthwaite is a dragon** -
  a sprite or a battler, not a generated face; `install.py artsheet` is the
  route if she needs drawing.
* The shareholders' council is the best sight gag here and it is a room, not a
  conversation.

**Done.** `build/fairholme.py`, Maps 35-37, `build/scenarios/fairholme.json`.
`placeholder_doors` is **30**. What is worth carrying forward:

* **The face bill came out at one drawing.** King Aldous is `Gen_People2` 2,
  drawn here (acca `p02` is the gold circlet, clothing `p14` the red robe,
  cloak `p02`, beard `p11`); Rosamund, whose settings were already written,
  is 3. `Gen_People2` has **four cells left**. The twelve shareholders round
  the table all **share** stock faces, and the nine heroes are the Actor-sheet
  faces nobody else in the game wears - `story.FACES` says which.
* **A dragon is `$BigMonster2`, character 0, facing down** - a whole-sheet
  character whose four direction rows are four different monsters, so
  `direction_fix` is not optional. No stock face sheet has a dragon on it, so
  Mrs Emberthwaite has **no `FACES` entry on purpose**: `say()` then prints
  her name with no portrait, and her lines get 60 characters instead of 47.
* **`IN_DRESSER` is the teddy-bear shelf** - its lower cell is `Sundries
  Shelf A`, which `../CLAUDE.md` already warns about - and it went into a
  princess's bedroom without anybody noticing until the first screenshot.
  `Inside_B`'s `Closet` and `Dresser` (a vanity, with a mirror) are the
  bedroom furniture.
* **The sight gag is three tables, not one long one.** `Table E` (purple),
  eleven cells of `Table C` (the red royal cloth) and two `Table A`s (plain
  kitchen wood) end to end, in a room one cell wider than the table at each
  end. Chairs down the north side, **stools** down the south - there were not
  enough chairs - and Sir Dunstable's chair empty, with a place card; his seat
  is open, so the card is read by sitting in it.
* **The arithmetic carries the council**: eleven halves leave the King a
  two-thousand-and-forty-eighth, the two farmers are one rescue between them
  (Mr and Mrs Budge, a good marriage), and Mr Pilbeam, who was only passing,
  rescued her from **the eagle** - which the Palace does not count, so the
  council cannot settle his share and he cannot leave. That is the bio's
  "a man who was only passing" and its "twelve if you count the eagle" as one
  joke.
* **The blush is the card in her bag**, headed FOR WHOEVER IT IS THIS TIME -
  mechanism four, the bio's own line, and nobody reacts. Three tropes: the
  King's reward, Rosamund's eleven kidnappings, and the dragon on the hill.
  So `VAR_BLUSHES` is **30** reachable against a tier of 20 (67%), and
  `VAR_TROPES` is three higher than it was. Still section 4 item 5's problem.
* **The widowhood is a chair.** Mr Emberthwaite's, at the card table, with a
  pipe on the seat. Rosamund has never sat in it; she pulls up the stool.
  Register B, and no joke is made of it.

### 4. Olde Evermore — (30,93), `Village C`

`BIOS.md`: **Mirabel**, aged 4,112 (eight and a quarter), Last Oracle of the
hidden elven village that every party finds eventually, by falling off the same
ledge. Her prophecies are in the Old Tongue, flawless and terrible, and
delivered from a stepstool; she has to be in bed by half past seven. The
Elders - every one of them visibly older than she looks and four thousand years
younger than she is - call her Grandmother and are sent to fetch things down
from the top shelf of the **Forbidden Archive**. She was there when the Prophecy
of Thistlewick was signed and the doodle in its margin is hers. She knows who
the villain really is and will tell you, but only as a drawing, and the drawing
is a horse.

* **Build:** the village (1), the Forbidden Archive (1).
* **Faces:** Mirabel has one. One or two Elders are new.
* **This one touches the spine**, so it is the one on this list to be careful
  with: the margin doodle and the drawing are statements about the Prophecy, and
  the Prophecy is the last boss. Nothing here should contradict the finale.

**Done.** `build/evermore.py`, Maps 38 and 39, `build/scenarios/evermore.json`.
`placeholder_doors` is **29**. What is worth carrying forward:

* **The spine is handled by placing the horse, not by explaining it.** Mirabel
  drew a horse in the margin at the signing because it was very long and she
  was bored; the Archive keeps a fair copy made there and then, by a copyist
  who was told to copy everything, and the horse is in its margin **beside
  clause twelve**. Asked who the villain really is, she draws it, and it is a
  horse - "I'm only very good at horses." Nothing connects the two horses and
  nothing says what the villain is. The finale's Prophecy is a scroll whose
  twelfth clause renews the Dark Lord, and the player's own copy (`db`'s key
  item) already has clause twelve "underlined by somebody worried", so a player
  can join it up at the top of the Tower and the game never does. The module
  says nothing about who signed it, when, or where the original is, which is
  what keeps it from disagreeing with anything. `CLAUDE.md`'s "The ending"
  summary was not quite enough for this: it says what the tally reads and not
  what the Prophecy *is*, so twenty lines of `journey.finale_event` (the scroll
  unrolling, "CLAUSE TWELVE") were read to check it. Worth adding one line to
  that summary if another site touches the spine.
* **The Register A candidate is mechanism two, and the blush is Mirabel's
  secret**: Elder Lirien is going to have a baby, Mirabel foresaw it and told
  them at breakfast, she has known "since the ninth of March", and it is going
  to be called Biscuit. The secret she thinks she is telling is the name. The
  Elders go red and cannot stop smiling. `VAR_BLUSHES` is **31** reachable
  against a tier of 20 (65%); two tropes (the ARRIVALS sign, the biscuit).
* **The face bill was one install and no drawing.** Mirabel's settings were
  written; she is `Gen_People2` 4. The Elders share faces nobody else wears:
  Faelan `Actor3:0`, Lirien `Nature:6`, the one face in the box that already
  looks as if she lives in a hidden elven village. The raker has no `FACES`
  entry and speaks as "Elf", with no portrait. `Gen_People2` has **three cells
  left**.
* **`build/worldmap/coords.py` was broken by step 3 and nobody noticed**:
  `fairholme.json` checks its door events as a list of `[name, x, y]`, which
  matches the position pattern, and the tool crashed on a list of lists. It
  reads a list of positions now. The per-site check list says to run it; it
  had not been run since step 2.
* **Everybody arrives by falling**, so the world-map door's first option is
  "Look over the edge", with the `Fall` sound effect, and the landing is
  `Outside_B`'s `Fallen Leaves` under a `Ledge A (Meadow)` cliff. `blob()` for a
  three-cell pond comes out as a sand-edged speck with the lily pads on the
  grass; a filled rectangle of `WATER` autotiles into a proper pond.

### 5. Gladhollow — (33,111)-(34,111), `Village B`

**`Village B` is two cells** - `worldmap.json` names both `Gladhollow` - so
`placeholder_doors.json` goes **29 → 27**, not 28. Measured at the end of step
4. Toby's settings are already written, as `build/characters/toby-gladhollow.json`,
and he is not in `story.FACES` yet: he is an install into `Gen_People2` 5, not
a drawing.

`BIOS.md`: **Toby Wendle, aged ten**, Official Welcomer, paid a copper a day to
stand by the gate and say "Welcome to Gladhollow!" and nothing else, per his job
description, which he has read nine times. He has fourteen ways of saying it and
is working on a fifteenth, the questioning one. He knows everything about the
town - the passage behind the mayor's bookcase, where the well key is, which
barrels have a potion in them - and is not allowed to tell you any of it,
because it would be a second sentence. He is saving up for promotion to Farewell
Boy at the east gate, who gets *two*.

* **Build:** the street with both gates (1). Optionally the mayor's room with
  the bookcase (1) - the passage is the payoff for the thing he cannot say.
* **Faces:** Toby has one. **This step needs no new art at all** if the mayor's
  room is skipped, which makes it the cheapest of the five `BIOS.md` sites.
* His fourteen deliveries are a variable and a list, and they are the whole
  joke. The barrels are his granny's and she would like her potions back.

**Done.** `build/gladhollow.py`, Maps 40 and 41, `build/scenarios/gladhollow.json`.
`placeholder_doors` is **27**. What is worth carrying forward:

* **The fourteen took the first new global of the world-map sites**,
  `db.VAR_TOBY`, variable 14. A self switch cannot count to fifteen and a page
  condition can name only one, so Toby is two pages - walking into him, and
  the cycle - and the cycle is fifteen `if_then` blocks on the variable. The
  narrator names each delivery ("Number seven: the Slow One") because Toby is
  not allowed to. The fifteenth is "...Welcome to Gladhollow?", once a lap.
* **He tells you everything by delivery.** Asked about the town he says
  "...Welcome to Gladhollow." and his hands slide a bookcase aside, or his eyes
  go well, pot, well, pot - `VAR_TOBY` mod three, so asking again gets another.
  No global switch was needed for the rest: the bio's "Welcome BACK to Glad- I'm
  not allowed that one" is a `condition_script` at the top of the cycle page,
  reading the ledger's self switch on the other map and his own B.
* **The mayor's room is two rooms on one map.** The office is
  `K.interior`; the back room is the same wall recipe copied into
  `gladhollow._room` and drawn in the black space to its east, and the
  bookcase is an ordinary shelf with a transfer behind a choice. No sliding
  furniture, no second map id. The payoff is the Council's ledger - a copper
  matched for every copper Toby has saved, a bag FOR THE UNIFORM, a Farewell
  Boy's cap in his size - and DO NOT TELL TOBY, and under it in pencil, "I
  havent." He knew; it would have been a second sentence.
* **No Register A candidate, on purpose**; the site is warm, not red. Four
  tropes: Toby, Granny Wendle's barrels, the key under the pot, the bookcase.
  `VAR_TROPES` is about seventy-four reachable; `VAR_BLUSHES` is unchanged.
* **Nobody but Toby has a face.** Granny Wendle (`People1:7`, the old woman
  Ysolde's face already belongs to) and Ned the Farewell Boy (`People1:0`) speak
  with their names and no portrait, the raker's precedent. `Gen_People2` has
  **two cells left**.
* **Two props did not match their text until they were cropped.** The
  well's "flowerpot with a geranium in it" is `Pot`, a plain clay jar, so it is
  a pot now; and Ned's line gave him a blue cap his sprite does not have.
  Neither shows at map scale and both are the thing the player reads.
* **`journey.py` already has a `GH`** - the Gloamwood's height - and
  `import gladhollow as GH` shadowed it; the build died on `'int' object has
  no attribute 'SITE'`. It is `GLAD`. Grep the importing module for an alias
  before picking one, the same lesson as `MAP_CHAPEL` one layer up.
* **`TREE_DARK` down a map edge is the flat hedge square** step 2 warned about
  on open grass; the edges here are all `TREE`.

**Steps 1-5 finish `BIOS.md` entirely** except Pellam Quickfoot, who is
correctly placeless - he is already in the deepest room of every dungeon, so he
needs dungeons rather than a site.

### 6. The Former Premises — (79,88)-(80,88), `Floating Continent (Castle)`, **air-only**

`WORLDMAP.md` 7.4, whose cast is written. The floating castle the Dark Lord was
raised in for two thousand years, **vacated on accessibility grounds** - a
complaint about the climb, then a second, then a recommendation, and the
engagement renegotiated onto a ground-floor site with a door at the bottom,
which is the Obligatory Tower. The one place in the world you cannot walk to is
the one that was abandoned for being impossible to get to, and the airship makes
the complaint moot four hundred years late.

**Mr Prosper Hollowell, Caretaker (Retained)**, is still up there and is
*delighted*. The lift - commissioned after the complaint was upheld, installed
inside the castle from the courtyard to the battlements, where it works
perfectly and always has - is the sight the place is for. The visitors' book has
nobody in it and he would like the current incumbent to sign it.

* **Build:** the hall (1). One face. One **appended page on Grimspite** at the
  finale for the signature - `NORTH.md` 1.7 pattern 2, and additive.
* **The three air-only rules apply and nothing else on this list has them:**
  player-touch and below characters, one bare square kept clear for the airship,
  and **`<aironly>` carried through onto the real door events**.
* Cheapest whole site on the list by payoff, and it is what makes the Two
  Hundred worth having flown.

**Done.** `build/premises.py`, Map 42, `build/scenarios/premises.json`.
`placeholder_doors` is **25**, and every placeholder left is on the ground.
What is worth carrying forward:

* **The way out of an air-only place needed a fourth note in `validate.py`.**
  The hall's exit puts the party back on (81,88), where the airship is, and a
  transfer destination is an on-foot entrance - so the flood walked straight
  onto both `<aironly>` doors and reported them. `<airreturn>` on the exit
  event keeps its destinations out of the on-foot flood and asserts instead
  that they are airship-landable. Both halves were proved on a throwaway copy
  (drop the note: the doors are reported; move the destination into the sea:
  the landing is). It is in the workspace `CLAUDE.md`'s vehicle bullet, and
  it is the only change this step made outside the game.
* **An appended page on Grimspite is three pages, because of the two already
  there.** Last page wins, so a signing page added on its own beats the ITEM 1
  page whenever both hold, and beats the empty `SW_WON` page after the win,
  which would put the finale back on the throne. So page 3 is the book, page
  4 is the book and the crate, and page 5 is the `SW_WON` page again, the
  same bytes. Pages 0-2 are byte for byte what they were, checked against
  `HEAD`. `journey.visitors_book_pages` splices at two new indices, `sig` and
  `tally`, the way ITEM 1 does at `split`; `CLAUDE.md`'s "The ending" has it.
  **Anybody appending to Grimspite after this has the same problem**, and
  `premises.json` asserts which page wins in each of the four states.
* **The first new switch of the sites**, `db.SW_VISITORS_BOOK`, 88. The
  book never leaves its lectern, so Hollowell gives you a slip ruled to match
  - which is also why no item was needed. He signs it before the fight:
  "Never been. Heard marvellous things about the lift." The tally reads it
  back before clause twelve is struck.
* **Hollowell is `Gen_People2` 6**, drawn here: suit and tie, spectacles,
  waxed moustache, and eyes shut in contentment (`eyes p25`), because 7.4's
  rule for him is that every single thing he says is good news. `Gen_People2`
  has **one cell left**.
* **The lift is `!$Gate2` character 1**, a pair of engraved stone doors that
  slide apart; the four rows of the sheet are the frames, walked with route
  codes 17-19, so the page must not fix its direction. It goes up to the
  battlements and back and "does not go any further than that. Nobody asked
  it to." No stock tile is a lift and nothing on the Inside sheets is a
  sconce; the sconces are `!Flame` 0 facing up, the wall candelabrum.
* **`Wall O (Demon Castle)` is green gemstone**, which is not what its name
  says - the first screenshot was a hall walled in emerald. The hall is
  `Wall K (Stone)` over `Interior Floor I (Marble)`, white and polished, and
  the old black-and-red throne is the one thing left of the tenant.
* **The first draft was a row too tall and half-empty**; four pillars down
  the aisle and this quarter's report on a desk (VISITORS: "Yes!", underlined
  twice) filled it. One trope, for the floating castle, and no blush, as 7.4
  insists. `VAR_TROPES` is about seventy-five reachable.

### 7. The seven that need no map at all

`COMPANIONS.md` 3's "world-map-only sites (no maps, one event each)". **Seven
doors, no interiors, one module, one session.** Each is a real event on the
stamp cell instead of a placeholder - a place with its joke in it. The quest
each one eventually serves gets **appended** later, which is the additive rule
and is why building them now is safe.

| site | at | stamp | what it is | for |
| --- | --- | --- | --- | --- |
| **The Sky Anvil** | (76,26) | Shrine | a meteorite used as a gatepost since 1749. **Elias Meech** will not sell a very good gatepost, but will trade for a gate | HOB-4 |
| **The Lay-By** | (11,88) | Igloo | three hedge mages, nine years, no name. **The igloo on grass is deliberate** - `WORLDMAP.md` 4 - and is a better joke than tidying it | ZEPH-5 |
| **The Cinder Fen** | (47,118) | Trail | nine hundred acres that need burning. The **Drainage Commissioner** wants it in triplicate | ZEPH-4 |
| **The Wrong Dragon** | (110,114) | Cave B | elderly, well read, delightful, and not a dragon | ALD-6 |
| **The Fair** | (67,115) | Large Tent | **Mother Selvidge**, twopence, four young men a year, never wrong | COR-4 |
| **Ashcombe Lake** | (104,54) | terrain, no stamp | drawn down one week a year; if you are there that week you can walk in | COR-2 |
| **The Duck's Pond** | (115,40) | Pond | four miles from the Collegium. The Duck is an honorary Fellow, holds a chair, votes, and has four hit points | ZEPH-2 |

* **Faces:** three to five, and some of these want no face at all - Ashcombe
  Lake and the Duck's Pond can be narration, the way the Standing Stones and
  the Hermit already are.
* **Measured at the end of step 6, and three of the names above are wrong as
  `SITE` strings**: `worldmap.json` calls them `Sky Anvil`, `Cinder Fen` and
  `Wrong Dragon`, with no "The". The Sky Anvil is stamped `Giant Tree (Snow)`,
  not a shrine. All seven are one cell, so `placeholder_doors` goes 25 → 18,
  and the Wrong Dragon's cave is open only from the north.
* **`COMPANIONS.md` contradicts itself about Ashcombe Lake** - it is in this
  table as one event and in L3 as "the drawn-down street (1 small map)". Build
  the event here; the small map, if it is ever wanted, belongs to step 14.

**Done.** `build/nomap.py`, no maps, `build/scenarios/nomap.json`.
`placeholder_doors` is **18**. What is worth carrying forward:

* **The Sky Anvil is a `Shrine` after all.** Its cell's layer-3 tile is
  `World_B` 22, which `World_B.txt` calls `Shrine` and a screenshot shows as a
  little stone building with a domed top - this heading had it right and the
  step-6 measurement, which said `Giant Tree (Snow)`, did not. So the text is
  about a shrine: the pilgrims call the stone the Sky Anvil and built the shrine
  round its foot in 1750, and Elias Meech hangs his gates off it. **Shoot the
  stamp before believing any measurement of it**, including the one in the
  prompt you were given.
* **A world-map scene asks first.** Each event is two pages: the first is a
  line of narration and a Stop / Press on choice, so a player crossing the cell
  on the way somewhere else loses one window and not a scene; the scene sets
  self switch A, and page two is the short version (with a second choice where
  somebody lives there, one window where nobody does). Mother Selvidge's A is
  set inside the branch that pays her, so walking off without paying leaves
  her first page standing.
* **The money is crowns.** `COMPANIONS.md` says twopence and nothing in the
  game is priced in pence; `System.json`'s unit is `cr` and Splint charges two
  crowns for the pit. Mother Selvidge charges two crowns.
* **One drawing: Elias Meech is `Gen_People2` 7**, and that sheet is full; the
  next site to draw anybody opens `Gen_People3`. Mother Selvidge is `Evil` 2,
  the old woman in the pointed hat, which is the look a fair expects and the
  only mystical thing about her. The three hedge mages are `Evil` 0 (Dunnock,
  the pipe-smoker, self-taught) and the two `Actor3` women nobody had used,
  3 and 7 (Miss Privet and Mrs Quickset). The Commissioner and "Somebody Large"
  in the Wrong Dragon's cave have no face on purpose.
* **What the Wrong Dragon is stays a closed subject** - `NORTH.md` 1.3's fifth
  mechanism - because Mrs Emberthwaite is already a dragon in every sense and
  a second kindly one would be a repeat. It is "a dragon in the sense that the
  map says so", has a blanket over what you think are its knees, and
  remembers a very correct young knight twelve years ago who talked about
  Horace until dark. ALD-6 can decide the rest.
* **Nothing here spends a quest's payoff.** Mother Selvidge tells Bram what is
  true of him - a long walk, a lot of company, and somebody very surprised to
  see him at the end - and not the four young men a year, which is Corvin's
  third reading. The Fen has its form and no fire person; the duck has its
  medal and walks into the bank twice, and nobody escorts it.
* **Five tropes, no blush**: the Sky Anvil, the hedge mages' secret order, the
  dragon's lair, the fortune-teller and the bell under the lake (which rings -
  up the road in the new Ashcombe, which took it with them). `VAR_TROPES` is
  about eighty reachable; `VAR_BLUSHES` is unchanged.
* **Step 8's door is measured**: `Tobias Frayne` at (66,82), `House (Town)`,
  one cell, open all four ways, so `placeholder_doors` goes 18 → 17. And
  **Village 1 is two cells**, (60,61) and (61,61), which step 9 should count
  before it writes its number down.

### 8. Tobias Frayne — (66,82), `House (Town)`

`COMPANIONS.md` 4: a cottage on the coast road, four cells from Thistlewick.
**Revived eleven times, and has developed a relationship with mortality.**
Merribell's MER-4.

* **Build:** the cottage (1). One face.
* Cheap, close to country the player already walks, and it is a good one to do
  while the pattern is fresh.

**Done.** `build/frayne.py`, Map 43, `build/scenarios/frayne.json`.
`placeholder_doors` is **17**. What is worth carrying forward:

* **`COMPANIONS.md` disagrees with this step, and this step won.** Its section
  5 files MER-4 under "no new map at all", and its own entry says *Needs: one
  world-map cottage, one bad ladder* - which reads as a world-map event, like
  step 7's seven. This list said one map, and a bad ladder has to lean against
  something, so it is a room: one 9x5 cottage behind the one-cell `House
  (Town)` stamp. Same shape of disagreement as Ashcombe Lake in step 7, and the
  same answer - `SITES.md` is the queue. **What MER-4 inherits**: Tobias is
  event 2 on Map 43 with a two-page self-switch pair, the ladder is event 3,
  the book event 4, the jar event 5 - **sealed and unpaid**, labelled FOR
  WHOEVER IS GOING THAT WAY - and the shelf event 6. The book's twelfth line
  is ruled and dated today and left empty, which is the quest's ending if
  Merribell's cure is leaving: it stays empty.
* **The stamp was what its name said** - shot this time, per step 7: a single
  green-roofed house on a square of grass between the coast road and the
  beach. `FRAYNE_STEP` is the sand below it.
* **Gen_People3 is open**, and Tobias is 0: face `p11`, fronthair `p03`, hair
  swatch 3 (brown), a moustache (`beard p01`), an open grin (`mouth p05`), the
  cottager's shirt (`clothing p22`) and **`facialmark p03`, the scar across
  the cheek** - the one of the eleven that shows. Seven cells left.
* **Three props were not what they were called, and `propsheet.py` found all
  three.** The jar was going to be `Pot A` on `Inside_C`, which is a white milk
  jug; `Pot C` and `Pot D` are brass ewers. The only thing on either sheet that
  reads as a jar is `Pot B` on `Inside_B` - `IN_BARREL`, a stoneware crock with
  the lid tied down with string - so the jar is that, on the floor, and the
  line says so. And `Medicine Shelf` is bottles, not bandages; its line was
  written to the crop ("tonics, liniments and smelling salts").
* **A ladder over a wall face makes the wall walkable.** `Wood Ladder` is
  `Inside_B` column 6, three cells; the foot is `0x600` and the two upper
  cells are **`0x626`** - the ladder bit, open up and down - and since the
  topmost non-star tile decides passage, laying them over the wall face opens
  a staircase up the wall. The ladder's event stands on the foot at "same as
  characters", which blocks it, and it is read from the square below; the
  scenario asserts the player stops there.
* **The eleven add up**, because a player will count: the ladder four, the
  well two, the bull two, the cliff one, and two he would sooner not go into.
  The book writes seven of them out and sums the rest. **One trope** (Tobias,
  the healer as a vending machine, seen from the patient's side), **no
  blush** - he is fond of kneeling adventurers holding his hand, and it is
  meant exactly as said. `VAR_TROPES` is about eighty-one reachable.
* **Nobody in it is unhappy**, and that was the only hard part: a man who
  keeps falling off a ladder on purpose is a sad story unless he is not in
  danger in his own mind. "Oh, nobody DIES on the coast road. Somebody always
  comes by." The new rung is leaning beside the old one, planed and sound,
  and still in its paper, which has gone yellow.

### 9. Village 1 — (60,61), `Village B` - **deferred**

**A decision, not a build.** `WORLDMAP.md` 8: worldgen placed it itself as an
extra beyond the anchors, it has no backstory in any document, and two
candidates were measured against it and both refused. It is being kept surplus
on purpose rather than filled with the first idea that fits.

* **Name it or remove it**, and either is a few lines. If it is removed, the
  placeholder count drops by two and `placeholder_doors` needs editing; if it is
  named, it joins this list as a step of its own.
* It is here at number nine so that the decision is taken while the list is
  still short, not left to the end.

**Done - deferred, by Mike's decision.** Neither named nor removed: Village 1
stays standing as an inert placeholder, and the decision moves to section 4,
where it is taken with the whole map built round it. Nothing was built, the map
is unchanged, and `placeholder_doors` is still **17**. What is worth carrying
forward:

* **Why not remove it now, although that is the cheapest line.** `WORLDMAP.md`
  8 left the site standing on purpose, twice, and the reason was to keep a
  spare settlement rather than fill it with the first thing that fits. Taking
  it out settles that question for good, and the list still has nine sites to
  build, any of which might turn up a use for it. So it waits until they are
  built.
* **Why not name it: nothing written supplies a name.** `WORLDMAP.md` 8's sweep
  of `COMPANIONS.md` found nothing unplaced that wants a settlement at (60,61),
  and Corvin's resettled Ashcombe is pinned beside its lake at (102,55). A
  name made up in this session would be exactly the filling that section warns
  against.
* **What a later removal costs, measured now so it need not be measured again.**
  Two cells, (60,61) and (61,61), which are events **66 and 67** on
  `data/Map008.json` as of this step. It takes an `F.unstamp` line in
  `build/worldmap/run_finish.py`, which already has several, followed by
  `build/worldmap/decor.py`. `placeholder_doors` then goes **17 -> 15**, and its
  walk onto (60,61) - one of its two proofs that a placeholder starts nothing -
  has to be re-pointed at a placeholder that still exists. No other scenario
  names either square.

### 10. Frostwick — (61,21)-(62,21), `Town B (Snow)`

`WORLDMAP.md` 7.3, whose cast is written. **The town that voted to keep the
curse.** The hundred-year winter was broken forty years ago; the town held a
meeting, and the curse is now *maintained*, under an annual contract with a
renewal clause and a schedule of what constitutes a snowfall. The town is very
proud of the arrangement, which it regards as forward-looking.

Six people: **Percival "Perce" Stagg**, who broke it and who opens the Festival
every year; **Ida Stagg**, his wife, who thinks it is very funny and has said so
to exactly one person, and who carries the site's Register A moment; **Clem
Blagg, aged seven**, the leaky child; **Mrs Wilhelmina Blagg**, chair of the
Festival committee; **Eudora Pargeter**, the retained practitioner, whose
speciality is refrigeration and who would like it on the record that she is not
an ice witch; and **Mrs Tibby Marchpane** of **the Eleven Days**.

* **Build:** the street, the Eleven Days (inn, and the visitors' book signed by
  three Chosen Ones), the parish room (the minutes, the asset register), the
  practitioner's cold room. The Staggs' house if there is time. **Four maps.**
* **Six new faces - the largest art bill on this list before Great Dunnage.**
  Only four have to speak to be worth building; 7.3 says which.
* Read 7.3's correction before writing a line of it: the hero is **not** a
  Chosen One, he is one of the unnumbered who went north with everybody else,
  and that is load-bearing.

**Done.** `build/frostwick.py`, Maps 44-47, `build/scenarios/frostwick.json`.
`placeholder_doors` is **15**. What is worth carrying forward:

* **All six faces were drawn**, not four: `Gen_People3` 1-6 are Perce, Ida,
  Clem, Mrs Blagg, Pargeter and Mrs Marchpane. That took about an hour
  including the lineups, which is cheaper than 7.3 feared. `Gen_People3` has
  **one cell left**, so the next site to draw anybody opens `Gen_People4`.
  Perce is male clothing `p26`, the red coat with the white fur collar, which
  is exactly the Festival. Clem is kid clothing `p12`, recoloured blue.
* **Two blushes, not one.** 7.3 counts only Clem's, and this list gave the
  site's moment to Ida. They are different lines and both pass 1.5, so both
  are in. Ida's is 7.3's own target: one great thing forty years ago, a great
  many since, none of which got a ribbon. Mr Stagg goes pink across the
  green. Clem's is his nan's kitchen at the committee's table: Mrs Stagg has
  not been cold in forty winters, "and that's Mr Stagg, that is". He thinks
  it is the lanterns, and the committee finds the ceiling interesting.
  `VAR_BLUSHES` is **33** reachable against a tier of 20, which is 61%.
  Three tropes: the town sign, Pargeter and Perce.
* **7.3's correction is the Perce scene, and the visitors' book is its
  record.** Bram is a real Chosen One, and Perce tells him and nobody else
  that he never was one. In the book, the third of the "three Chosen Ones"
  is P. Stagg, marked Y in Mrs Marchpane's hand over a rubbed-out N in his.
  The two older entries are a century apart and too faded to have names,
  which keeps them from disagreeing with anybody the game has numbered. The
  minutes carry the rest: Item 4, Mr Stagg to open the Festival, carried
  unanimously with one abstention, Mr Stagg.
* **Pargeter reads the Prophecy as a contract**, if it is in the bag: no
  break clause, no notice period, "and clause twelve renews itself...
  Somebody's underlined it, I see. Somebody's worried." That is the item's
  own description and step 4's clause twelve, read by the one person in the
  game with no feelings about contracts. It says nothing about who signed it.
* **It snows on the street and nowhere else**, with `north.py`'s idiom: an
  autorun that erases itself, and a local `door()` that clears the weather
  after the walk and before the fade. The scenario asserts it at every door.
  **A `shots.js` batch carries weather across its teleports**, so an
  interior shot straight after a street shot shows snow indoors. That is the
  tool, not the map.
* **Snow tiles had no `mapkit` constants**, so they are local to the module:
  A2 `Snow` 40 and `Road (Snow)` 42, A3 `Snow Outer Wall` 77 and 78, and on
  `Outside_B` the 2x2 snow conifer, the three-cell snow streetlight (its foot
  blocks), `Sign A (Snow)`, the snowman, and the snow barrel and crate.
  `ROOF_WHITE` was already the snow roof. `MAP_PARISH` was taken (Upper
  Clanging, Map 25), so the committee's room is `MAP_WORKING_GROUP`.
* **The Staggs' house is a shut door** with a card in two hands, AT THE
  RIBBON - P. / BACK FOR TEA - I. That was cheaper than a fifth map and says
  more. `propsheet.py` found `DOOR_SHUT` is `Large Window C`. It reads as a
  door at map scale, but there is no wreath on it, so the line lost its
  wreath.
* **`placeholder_doors` now walks onto Great Dunnage** at (31,52), from
  (31,53), because Frostwick's cell is a real door now. Great Dunnage is the
  last step on this list.

### 11. Coldbarrow — (50,19), `Temple A (Snow)`

`COMPANIONS.md` L6, "the single cheapest location here and the one with the best
sight gag". One room, one enormous map of the island with pins in it, one
clerk - **Chapter Clerk Mordaunt**. Nine pins, one knight, a committee, a
review. Serves ALD-3, and ALD-2 if the chapel is here rather than at the
Sisterhouse.

* **Build:** 1 map, 1 face.

**Done.** `build/coldbarrow.py`, Map 48, `build/scenarios/coldbarrow.json`.
`placeholder_doors` is **14**. What is worth carrying forward:

* **The sight gag is a picture, and that is the one new mechanism.** The
  stock `World Map` on `Inside_B` is a small 2x1 poster, so no tile can be
  "one enormous map". The wall carries four of them abreast as set dressing,
  and reading any of its eight cells puts `img/pictures/Coldbarrow_Map.png`
  up as picture 1 - this game's own world off `build/worldmap/generated.png`,
  toned sepia, in a wooden frame, a white pin for every other knight and
  **nine red for Aldric** - and erases it after the last window. Show and
  Erase Picture are raw commands 231/235, since `rmmzdata` has no helper;
  the scenario asserts both. **The picture is drawn by running the module**
  (`python3 build/coldbarrow.py`), like `art.py`, not by the data build, and
  every pin is placed **by site name** off `worldmap.json`, so no world
  coordinate was copied anywhere. PIL is not installed; `tools/chargen/png.py`
  and numpy did it.
* **Six right on different dates, three the same week**: Frostwick, Fenmarch
  Hall and the Lay-By - north coast, south coast, far west. Thistlewick is
  one of the six, because it is where he is.
* **Nothing of ALD-3 is spent.** Mordaunt says the committee is reviewing the
  pins and the card on its table says Sir A. is to be asked to remain in one
  place, "Not yet informed". Nobody asks him and nobody offers a promotion.
  With Aldric in the party, the first page runs a reaction shot - "Where am
  I?" / "Frostwick, sir. And Fenmarch." / "Busy week." - and the scenario
  asserts no line mentions a promotion. **What ALD-3 inherits**: Mordaunt is
  event 2 on Map 48 with a two-page self-switch pair; the committee's table is
  events 11-12, the files 13-14, the desk 15.
* **One trope, no blush**: the guild that has lost your file, turned round -
  the Order has not lost it, it has nine of them. `VAR_TROPES` is about
  eighty-five reachable.
* **Mordaunt is `Gen_People3` 7, and that sheet is full.** Face `p12`, grey
  hair (swatch 19) in `fronthair p16` / `rearhair p08`, a trimmed beard
  (`p10`), half-rim reading glasses (`glasses p01`) and the black coat with the
  purple lining (`clothing p09`). **Skin swatch 0 leaves a red smear round the
  sprite's eyes** under grey hair; swatch 2, which everybody else uses, does
  not. The next site to draw anybody adds `Gen_People4` to `art.py`.
* **`Chair A (Wood)` is a 1x2 chair** - tall back over an open seat, facing
  south only. Laid as one tile it is a back with nothing under it, and it
  cannot sit on the north side of a table facing up; that side gets stools.
  `propsheet.py` agreed with every other prop, but two lines had to follow
  it: the desk holds a sheet of paper, not a tray, and the shelves are bound
  volumes, not folders.
* **Step 12's door is measured**: `Sable Hart` - no "The" - at (24,75), event
  **58** now, layer 3 `World_B` 121, `House (Town)`, and (24,76) is `0x600`.
  Shot: one green-roofed house on a square of grass, with two roads ending at
  its door, on dry sandy waste rather than anything that reads as moor, with
  mountains to the north-east and rock to the south.

### 12. The Sable Hart — (24,75), `House (Town)`

`COMPANIONS.md` L7. An inn on a moor where every corner is taken: **five hooded
men being scrupulously fair to each other about seating**, with a rota for the
darkest corner, a newsletter and a league table. Corvin's COR-3, and where
COR-4's fair should be pitched if the fair does not get its own map — it does,
at step 7.

* **Build:** 1 map. **Five faces**, which is the whole joke and is why a cheap
  map is not a cheap step. They can be five variations on one look; doubling up
  is established practice.

**Done.** `build/sable_hart.py`, Map 49, `build/scenarios/sable_hart.json`.
`placeholder_doors` is **13**. What is worth carrying forward:

* **The five are hooded after all, on a borrowed hood.** The male body has
  none (`../CHARGEN.md`), but the female `AccB p10` riding hood sits on a male
  head without an offset in all four views and recolours down to black.
  `art.py`'s `BORROWED` lends it by rendering against a symlinked copy of the
  stock generator with those files added to `Male`; no male part used the
  id, so a dry run left all twenty-four people already drawn `unchanged`.
  The look is one hood over cloak `p03` and clothing `p25`, all in one
  colour, and the five are told apart by that colour (teal, grey,
  mauve-grey, black, brown), the hair under it, the eyes and one thing each:
  Crake's moustache, Morrow's spectacles, Rook's beard, Veyle's scar,
  Blackwood's grin. **`Gen_People4` is open**, 0-4, three cells left. The
  editor has no male `AccB p10`, so those settings files load there hoodless.
* **Four corners, five rivals** is the room's arithmetic, and it is drawn
  rather than said: Crake the Secretary by the window, "because somebody has
  to be able to read the rota"; Veyle in the darkest, north-east, until
  Monday; Rook, who keeps the league table, south-west; Morrow, who edits
  OVERSHADOWED, south-east; and Blackwood, first on the waiting list for any
  corner since March, on a stool **by the fire**, brooding as hard as he can
  in the brightest seat in the inn. The middle of the room is two tables and
  four stools with dust on them. Mrs Garrow at the bar has no face and says
  they tip beautifully.
* **Nothing of COR-3 is spent.** Its payoff is the league table, on which
  Corvin is seventeenth, so **the table on the wall stops at fourth**: the
  rota is pinned over the rest with four pins, "and somebody has put in a
  fifth, to be sure". The newsletter sends C. Ash's apologies "(as ever)" and
  keeps his chair, which is COR-3's premise. With Corvin in the party, Crake
  has him down as a member, Corvin is not here, and Crake writes something
  very small in a book; the scenario asserts no line in that branch mentions
  a league, a rank or seventeen. **What COR-3 inherits**: Crake is event 2
  with a two-page self-switch pair, Veyle 3, Rook 4, Morrow 5, Blackwood 6,
  Mrs Garrow 7, the league table 8, the rota 9, the newsletter 10.
* **Veyle says Corvin's line.** "Don't ask about the scar" is Corvin's, word
  for word, in the Slain Wyvern; here the player does not ask, and Veyle is
  briefly disappointed. It is the dark mirror, which is the room's one trope.
  **No blush**: the room is warm, not red. `VAR_TROPES` is about eighty-six
  reachable.
* **Two props were wrong in the first screenshot, and neither was a
  misnamed tile.** `Curtains A` is a pale sheer that made the darkest corner
  the brightest thing on the wall; `Curtains B` is the heavy drawn one. And
  A2 `Ground D (Black Floor)` laid on layer 1 to darken the corner autotiles
  into what reads as rubble, so the darkness is the curtain and the text.
  The stock `Large Fireplace` is **unlit** - an empty black grate, which
  contradicts "by the fire" - so the fire is an event, `!Flame` 3 facing
  left, on the grate's middle cell. And **an event list's index is its
  id**: appending the fire as event 12 before 8-11 in the list is a map
  whose ids do not match their slots, so append in id order.
* **Step 13's doors are measured and shot** - see its restart prompt. Sump's
  stamp is a desert house with **its own oasis pool**, on a spit with the sea
  on three sides, for a hamlet with no water since 1794. And the game already
  has a **Hester**: Mrs Hester Ashbury, Restwell's innkeeper.

### 13. Little Gore and Sump — (97,101) `House (Village)`, (78,102) `House (Desert)`

`COMPANIONS.md` L8. Two hamlets, one map each, both essentially one street and a
reason. **Little Gore** is four miles from Fenmarch and is where the letter was
always going - **Hester Vane**, married nine years ago, keeps the invitation.
**Sump** has not had any water since 1794 and has a wasp problem the parish
cannot allocate. Either can host PIP-4's eleven interviews. Serves ALD-1,
MER-5, PIP-4.

* **Build:** 2 maps, 2 faces, one module.

**Done.** `build/hamlets.py`, Maps 50 and 51, `build/scenarios/hamlets.json`.
`placeholder_doors` is **11**. What is worth carrying forward:

* **A cluster of two**, `SITES = {"Little Gore": ..., "Sump": ...}`, merged
  into `journey.world_map`'s claims as `**HAM.SITES` - Hithermost's shape, and
  nothing else about the mechanism changed. `HAM` was free in `journey.py`;
  `LG` and `SU` were never needed. Both doors were measured again and both
  stamps shot: nothing on the map had moved since step 12.
* **Little Gore's reason is the wedding, and ALD-1's letter is untouched.**
  Mrs Vane married Tom from Fenmarch at Fenmarch nine years ago this summer,
  and the whole hamlet - eleven of them - walked the four miles over in the
  rain. Tom works in the gardens at Fenmarch and walks it daily, which is new
  and which step 16 is free to use or ignore. The notice board still carries
  the banns, and pinned under them a brown card: **INVITATIONS TO FOLLOW**.
  That is the set-up for ALD-1 and none of its payoff - no letter, no
  mantelpiece - and the scenario asserts she mentions neither. **There is no
  reaction shot with Aldric**, unlike Coldbarrow and the Sable Hart, on
  purpose: he cannot stand four miles from home with the letter in his tabard
  and have nothing happen, and anything that happened would be the quest. So
  ALD-1 inherits a Little Gore where Aldric walks in and nobody notices, and
  should deal with that however it likes.
* **Coldbarrow's white pin at Little Gore is Dame Winifred Cope**, the
  Order's knight in the field there for eleven years - "There's a pin in me at
  Coldbarrow. Just the one." - who writes NOTHING TO REPORT every quarter and
  treasures the replies. She has no face (`Actor2` 1). **`Actor3` 6 is
  Aldric's own sprite**, and was the first armoured sprite reached for.
* **Sump puts the two facts one line apart and never joins them.** The
  minutes: 1794, wasps in the well, deferred; 1794, the Water Committee wound
  up, there being no water; 1795, a general sense that things used to be
  better, suspected curse. The Clerk, Mr Thurle, explains that a wasp is the
  Pound's, a nest is Buildings', and a well is Water's, "and the Water
  Committee was wound up in 1794, on the grounds that there wasn't any." With
  Merribell in the party she looks at him for about nine seconds and opens her
  mouth, and he asks her to speak through the chair; there is no chair, he is
  the chair. The scenario asserts nobody says thirst, drink or dehydration.
  **What MER-5 inherits**: Thurle is event 3 on Map 51 with a two-page
  self-switch pair, Gammage 4, Mrs Pardew 5, the well 6, the minutes 7, the
  sign 8, the pool 9.
* **The stamp's oasis is the sea**, come in under the sand, with a sign in
  it that says NO. It is drawn as three by two of A1 `Water D (Sand)` - the
  same kind as the sea round the spit - in a rim of `Grass (Sand)`, drawn by
  hand: `blob()` left a detached green speck.
* **Four tile traps, all cheap.** `K.PALM` is a block for `blit`, not a
  column - `column` put a list into the map data, and `validate.py` died on it
  rather than reporting it. `K.SOIL` is the sheet's `Sand` and `K.SAND` its
  `Dirt`; `Road (Sand)` is grey cobbles, which is a town, so Sump's street is
  `Dirt`. `SIGNPOST` (`Sign A`) is a two-armed fingerpost and `FENCE_PANEL`
  (`Sign B`) is a notice board between two posts - the banns and the minutes
  are on `Sign B`, and both fingerposts' text says two arms. And `Well` is an
  open stone ring: `propsheet.py` found the line that gave it a winch.
* **No wasps in the box.** Nothing on `Monster`, `Nature` or `!Other1` is an
  insect (`!Other1` 4 is spike traps), so the nest is a hum and "something
  small and striped" that comes up, looks at you and goes back down to report.
* **Two faces, `Gen_People4` 5 and 6**: Mrs Vane (face `p05`, `fronthair p07`
  over a bun, `rearhair p18`, the village dress `clothing p09`, and an open
  smile, `mouth p21`) and Mr Thurle (face `p10`, a frown `p16`, shadowed eyes
  `p19`, a waistcoat `p10` and a wide hat `accb p03` whose lime band is
  recoloured black through `accessory 1 sub 2`). `Gen_People4` has **one
  cell left**. The children, Mr Gammage, Mrs Pardew and Dame Winifred share
  stock sprites and speak without portraits - and **a faceless speaker's name
  goes inside the line**, so their lines are ~45 characters, not 60.
* **PIP-4 is not here.** Little Gore has more people in it who liked each
  other, which is what an elegy wants; nobody in either hamlet has died.
* **One trope** - Sump's sign, the cursed village - **and no blush**: both
  places are warm. `VAR_TROPES` is about eighty-seven reachable.
* **Step 14's door is measured and shot.** `Ashcombe` is **two cells**,
  `Village A` at (102,55) and (103,55) - events **61 and 62** now, layer 3
  `World_B` 116 and 117 - so `placeholder_doors` goes 11 -> 9. (102,56) is
  `0x600` with nothing on it. Shot: a small fenced hamlet of two wooden huts
  and a garden on open grass, forest to the west, a dirt road coming up from
  the south-east, and Ashcombe Lake - step 7's event, at (104,54) - a large
  square pond with sandy banks just to its north-east.

### 14. Ashcombe — (102,55), `Village A`

`COMPANIONS.md` L3, "possibly the funniest single location in the document".
**The village that is fine.** Prosperous, cheerful, superbly drained, with a
small museum about the flood and an annual dinner; every building is newer and
better than what it replaced and the plaque is upbeat. It exists to be pleasant
at Corvin Ash, whose village it is. **Mrs Ash** is fine, has a new kitchen, and
knits. Serves COR-1, COR-2.

* **Build:** the village (1), Mrs Ash's kitchen (1). Two faces - Mrs Ash and the
  Drainage Museum curator, who is proud.
* Ashcombe Lake's world-map event is step 7; only build the drawn-down street
  here if COR-2 turns out to need it.

### 15. Weeping Bottom — (58,99), `Temple B`

`COMPANIONS.md` L4, the Sisterhouse: the Order of Whatever Works' mother house,
in a damp valley chosen on medical grounds that were wrong. Half hospital, half
argument. **Prioress Aveline Stope** runs it and has begun holding symposia and
knows that is a bad sign; **Sister Bewick** of the Order of What Ought To Work
is losing patients, winning arguments, and entirely sincere. Serves MER-1,
MER-3, and ALD-2 if the chapel is here rather than at Coldbarrow.

* **Build:** the Sisterhouse (1), the ward (1). Two faces.
* Merribell is a party member, so her own pages are appended rather than
  written fresh - `NORTH.md` 1.7 pattern 2.

### 16. Fenmarch Hall — (86,114), `Large Mansion`

`COMPANIONS.md` L5, the Pemberton-Gore seat. Moated, damp, and hung with
**eighty impossible animals in glass cases**, which is how Aldric's family home
also becomes Wren's cabinet of curiosities and saves a map. Small household,
enormous portrait gallery, all of them facing the wrong way. **Mr Ottershaw**,
ninety, unrepentant, an artist, will show you the joins.
**Pemberton-Gore IV**, nineteen, magnificent, found the gate first time.
Serves ALD-1, ALD-5, WRE-4.

* **Build:** the hall (1), the long gallery (1). Two faces.

### 17. The Collegium Arcanum — (112,38), `School of Magic`

`COMPANIONS.md` L2, "the second big one" and "the best value in the document" -
three companions' worth of quest on one set of maps. A university that is
entirely committee; its comedy is **institutional courtesy**, where nobody is
ever rude, nothing is ever refused, and everything is referred. The Porter's
Lodge holds the real power and knows it; the Library is where money goes to die.
**Sub-Librarian Prewitt** is immovable, courteous, correct, and holds the
largest number in the game. **Dean Fenwold** is fine, has a talk about it, and
did not back her up once. Serves ZEPH-1, ZEPH-2, ZEPH-3, WRE-1.

* **Build:** the Great Court (1), the Library (1), the Hall (1). Three faces.
* The pond is step 7's Duck's Pond and is already done by the time you get here.

### 18. Great Dunnage — (31,52), `Fortress City`

`COMPANIONS.md` L1, "the big one", and last on this list because it is the most
expensive thing in it. Down the valley from Upper Clanging where Cotter
Cotterill already works - `NORTH.md` 4.6 says so in a table and this is the town
collecting on it. Upper Clanging is a works with a town round it; **Great
Dunnage is a town with nine works in it**. The joke is **municipal
self-regard**: a Corporation, a Mayor, a motto, a crest, an anthem, and a
counting house it cannot open. It has opinions about Upper Clanging, which it
considers charming. Nobody in Great Dunnage has ever heard of Bram.

Serves HOB-1, HOB-4 (approach), NIX-1, NIX-2, ALD-4, PIP-3, COR-5, ROL-1 -
**six companions off one town.**

* **Build:** the town (1), the Company of Smiths' hall (1), the Sealed Counting
  House (1, mostly door), the Bonded Warehouse (1), the Bell inn (1). **Five
  maps**, and the haulage yard can be a corner of the town map.
* **Six faces:** the Wardens of the Company of Smiths, **Wharfinger Tibbs** (has
  held a coat for eleven years and never asked why), the Mayor (reading the
  preamble), the Bell's judges (one of them cannot hear; the birdcall man wins),
  the horse (fine, doing well, effectively a partner), and **Appraiser Fettle**,
  who is enthusiastic about the tang and has a form for curses.

---

## 4. When it is all in place

Only then, and in this order:

1. `python3 build/build_game.py` and `python3 ../tools/validate.py .`
2. `python3 build/worldmap/coords.py`
3. `python3 ../tools/propsheet.py . /tmp/all.png <every new map id>` - one look
   at every prop the expansion laid down. It found eight wrong-century props in
   four rooms the last time it was run over work that had already been reviewed.
4. `../tools/scenarios.sh .` in the background. It is about 170 minutes for the
   suite as it stands and will be longer with a scenario per site.
5. Re-cut the two counter thresholds in `journey.finale_event`. `VAR_TROPES` is
   40/20 and `VAR_BLUSHES` is 20; both are cut against totals this work moves,
   and `NORTH.md` 2.3 says to keep the blush tier at four fifths of the true
   total. It is at **71%** after Penultima's one moment and Restwell's two -
   twenty-eight reachable - and every site from here makes it worse. **This is the one
   thing on this list that genuinely cannot be done incrementally**, because it
   is a judgement about a total that is not known until the total stops moving.
6. **Decide Village 1** (step 9, deferred). Name it if a finished site has
   turned up a use for a spare settlement at (60,61); otherwise remove it,
   which step 9's last bullet has already costed. Either way, do it before the
   push. An inert door on a published map is a promise that nothing keeps.
7. Then, and only then, push `master` to **`live-rpg`**.
