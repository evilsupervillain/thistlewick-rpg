# The companion quests - the queue

`COMPANIONS.md` is the design for the fourth quarter: nine companions, forty-nine
quests that exist only when one of them is in the party. This is its **work
list**, the way `SITES.md` was the work list for the world map's doors: what,
in what order, what each step inherits, and how to know it is finished.

**Why a file of its own and not a new section of `COMPANIONS.md`.** That
document is a proposal written before any of its places existed, and parts of
it are now wrong (see 0.3). A queue is read every session and a design is read
once per quest; keeping them apart means a session reads this, then **one**
character's section, and nothing else - the same split `SITES.md` made, and
the same reason it worked.

---

## 0. How to work on this

### 0.1 The rules for this effort

* **One step per session**, in order. A step is one quest, or two when both
  are small and share a place. Partially done is a legitimate state; say so in
  the step's Done paragraph.
* **Per step, and only this:**

      python3 build/build_game.py                       # byte-stable: any
      git diff --stat data/                             # diff outside the step
      python3 ../tools/validate.py .                    # is a mistake
      python3 ../tools/apidigest.py . --write           # if a signature moved
      node ../tools/shots.js /tmp/s <map>:<x>:<y> ...   # anything drawn
      node ../tools/scenario.js build/scenarios/<step>.json

  **No full suite between steps.** Once, in step G1, budgeted at eight hours
  (the last run was 484 minutes). The narrow exception is `SITES.md`'s: a
  change to `story.py`, `db.py`, `places.py` or the ending is a reason to run
  the scenarios that touch it, not the suite.
* **Commit per step, freely. Nothing is pushed.** `live-rpg` is pushed once,
  after all of this and its scenarios are done **and Mike has played through
  everything himself**. Do not push and do not offer to.
* **When a session ends early**, write the state into the step's Done
  paragraph and leave a restart prompt at the bottom of this file, the way
  this one was left.
* **Fix the room you are standing in.** When a step puts pages into an old
  room and the room itself is wrong - a prop that is not what its constant
  says, a thing on the floor that belongs on a table, furniture a row out -
  fix that room in the same step (Mike, 30 Sep 2026). Hob's anvil was a pile
  of scrolls on a broken table. "Additive only" protects the storyline, not
  bugs: no line of dialogue changes, but tiles and an event's cell may.
  Crop before judging (`python3 ../tools/propsheet.py . out.png <map>`, and
  `build/TILENAMES.md`); draw with mapkit's "Inside furniture, by name" or
  `K.sf_tile` by the sheet's own name; screenshot before and after; and run
  every scenario that walks the room, because a moved prop can block a
  scripted walk (find them by parsing the scenarios' `query` and `goto` map
  ids). Say what was fixed in the step's Done paragraph. Thistlewick's and
  Nether Sopping's ten interiors were swept on 30 Sep (commit 8d35f6b); the
  north and the world-map sites have not been.

### 0.2 The rules for every quest (`COMPANIONS.md` 1, restated where it bites)

* **The gate is `actorValid` on a page.** One actor per page, so "X or Y" is
  two pages and "X and Y" is `R.if_then(R.condition_actor_in_party(...))`
  inside one. A player without the companion sees today's game byte for byte.
* **The quest giver keeps the quest.** A roster desk can dismiss anybody
  mid-quest. Every piece of quest state is a **global** switch, variable or
  item - never a self switch that only a page gated on the companion can
  spend, never anything carried by the actor. A dismissed companion's errand
  waits, and resumes when they are back.
* **A page appended below a ladder requires that ladder's terminal switch**
  (this game's `CLAUDE.md`, Conventions). Every existing NPC a quest touches
  gets its ladder read first. Where the terminal switch is not something a
  quest can reasonably wait on - Dorcas's is the thirty-year Feud - **put the
  quest on a new event, or on an event whose ladder is one self switch**,
  rather than on the NPC.
* **Additive only** (`NORTH.md` 1.7): new events, appended pages, and - for
  the ending only - appended `if_then` blocks. Nothing published is re-voiced.
* **A companion's Change Party Member initialises once**, in `story.recruit`
  on `SW_KNOWN`. No quest adds another initialise anywhere.
* **Lines**: 47 characters with a face, 60 without; `say()` refuses longer.
  Every new date goes into `TIMELINE.md` in the same commit.
* **Every quest bumps `story.trope()` for its cliché**, once, and counts any
  Register A moment with `story.blush()`, once. **Do not re-cut either
  threshold per quest** - both are re-cut once, in step G1, against the
  finished totals. Keep a running tally in each Done paragraph.
* **Finishing a quest calls `story.companion_story(actor)`** (built in step
  A1): it turns that companion's `SW_<NAME>_STORY` on and, the first time only,
  adds one to `VAR_COMPANION_STORIES`. The ending reads one block per
  companion, not per quest (1.4), so a quest that `COMPANIONS.md` says "gives
  a line in the ending" gives a **candidate** line: write it into the step's
  Done paragraph and step G1 chooses one per companion.
* **One piece of gear only they can wear, per companion** (1.2), not per
  quest. The first quest of theirs that `COMPANIONS.md` gives gear to takes
  it; the table in 0.5 tracks who has had theirs.

### 0.3 What `COMPANIONS.md` gets wrong now

* **1.4's thresholds**: `VAR_TROPES` is **60 / 20** and `VAR_BLUSHES` **27 of
  34**, both re-cut in `SITES.md` section 4. Re-cut once more in G1.
* **Section 3's locations are built**, some under other names; the Ids table in
  `CLAUDE.md` is the authority, and each step below names its maps.
* **Section 7's module plan is superseded** by 0.4.
* **`SPARE.md`'s switches 72-74 are `SW_KNOWN`'s.** Spare's are 89-92 now
  (0.6).
* **SPA-1 is in section 5's "no map" row but needs Spare**, who is not built.
  It moves to part F with him, so the no-map row here is fifteen.
* **MER-4, ZEPH-5, HOB-4, ZEPH-4, ALD-6, COR-4 and COR-2** each had a
  world-map site built for them by `SITES.md` - Tobias Frayne's cottage, and
  `nomap.py`'s Lay-By, Sky Anvil, Cinder Fen, Wrong Dragon, Fair and Ashcombe
  Lake. What was a new place is now an appended page.

### 0.4 Where the code goes - decided once

**One module per companion, `build/q_<name>.py`** - `q_merribell.py`,
`q_hob.py`, `q_zephyrine.py`, `q_nix.py`, `q_aldric.py`, `q_piper.py`,
`q_corvin.py`, `q_wren.py`, `q_roland.py`, and `q_spare.py`. Each is created
by the first step that needs it.

* **Why by companion and not by place.** A quest is the unit a session builds,
  reviews and tests, and most of them span places: MER-2 fetches from three
  towns, NIX-4 has eleven owners over three, PIP-2 has a page per companion.
  Filed by place, one quest would be scattered over five finished modules,
  each of which is two thousand lines of somebody else's room.
* **How a page gets onto an event another module builds**: the place module
  calls the quest module, exactly as `north.py` calls
  `field.ott_field_pages()` - `pages=[...] + q_wren.goose_pages()`, or
  `evs.append(q_wren.second_plaque(21, ...))`. The place module gains one line
  per hook and nothing else. The quest module must **not** import a place
  module (they import it; the other way is a cycle) - so coordinates two
  modules share go in `places.py`, which is what it is for.
* **A new map a quest needs belongs to the place it is in** - drawn in that
  place's module (NIX-2's room behind the Door is `dunnage.py`, in the black
  north of Map 63, `ashcombe._room`'s idiom), with its events from the quest
  module. A new map in no existing place (ROL-2's dungeon, SPA-2's tubes, the
  drowned street) is drawn in the quest module and takes an id from 0.6.
* **Scenarios** are `build/scenarios/q_<quest>.json` - `q_wre2.json` - and a
  step with two quests may share one.

### 0.5 Gear, and who has had theirs

| companion | gear | from | step |
| --- | --- | --- | --- |
| Merribell | the Pamphlet (accessory) | MER-1 | E2 |
| Hob | the best weapon for him, forged badly on purpose - **done**: weapon 41, "Something To Say", an axe (axes are his alone) | HOB-2 | A13 |
| Zephyrine | a robe with a stat line | ZEPH-1 | C1 |
| Nix | the coat (armour, and it fits) | NIX-1 | B5 |
| Aldric | the shield | ALD-2 | E7 |
| Piper | the rosette for second place (accessory) - she frames the certificate and wears the rosette; decided in A3 | PIP-3 | B3 |
| Corvin | the scarf, the wrong colour (accessory) | COR-1 | D1 |
| Wren | **the Gloamwood Society badge** - decided in A11: armour 40, an accessory of a new armour type (7, "Badge") that only her actor can wear | WRE-3 | A11 |
| Roland | the better sword he leaves at the door - **done**: weapon 43, The Drawn Sword, out of the stone under Carn Drey, laid on the grass at the tower door beside Fairweather's Own | ROL-2 | E18 |

### 0.6 Ids reserved for this effort

Also in `CLAUDE.md`'s Ids and Switches tables, which are the authority. Take
the next free id in a block and write it into the step's Done paragraph and
`CLAUDE.md` in the same commit.

| block | what |
| --- | --- |
| Switches 89-92 | **Spare** (was 72-74 in `SPARE.md`): 89 `SW_SPARE_FORM`, 90 his recruit switch (`SW_RECRUIT[SPARE]`, `SPARE.md`'s `SW_SPARE_JOINED`), 91 `SW_SPARE_REFUSED`, 92 his `SW_KNOWN` |
| Switches 93-100 | unallocated, left free |
| Switches 101-109 | `SW_<NAME>_STORY`, Merribell to Roland in actor order - the same last digit as 11-19 and 72-80 |
| Switch 110 | `SW_SPARE_STORY` |
| Switches 111-250 | per-quest switches, taken in queue order |
| Variable 15 | `VAR_COMPANION_STORIES` |
| Variables 16-30 | per-quest variables, taken in queue order |
| Items 33-34 | Spare's, as `SPARE.md` has them |
| Items 40-79 | companion-quest items, key and otherwise |
| Weapons 34 | Spare's |
| Weapons 40-54 | companion-quest weapons |
| Armors 27 | Spare's |
| Armors 40-59 | companion-quest armours |
| Skills 146-155 | Spare's and Mrs Cotterill's, as `SPARE.md` has them |
| Skills - | a skill a quest *teaches* goes in the free end of that companion's own block (Zephyrine's is 46-49) |
| Skills 170-189 | companion-quest enemy skills |
| States 40-44 | companion-quest states (COR-5's curse) |
| Enemies 28 | Mrs Cotterill |
| Enemies 41-69 | companion-quest enemies (WRE-1's eleven specimens are the bulk) |
| Troops 29 | A Discussion With Mam |
| Troops 41-59 | companion-quest troops |
| Common Events 3-10 | companion-quest common events |
| Maps 66-79 | new maps in no existing place (ROL-2, SPA-2, COR-2's street, and anything a step finds it needs) |

`build_game.py` sizes System.json's switch list at 101; the first step past
switch 100 grows it.

---

## 1. Faces - the audit, before a line is written

`COMPANIONS.md` 7 called faces the blocker. **They no longer are, for
humans**: `tools/chargen` makes a face and a matching sprite for anybody who
can be described, `art.py` installs them into this game's `Gen_*` sheets, and
the next free cell is **`Gen_People11` 3**, with 3-7 free and `Gen_People12`
onwards to be opened as needed. What the generator cannot make is anything
that is not a person - and **the sv battlers** a party member or a fought
human needs. Those go to Mike, at the end (`AUDIT.md` item 1).

**Speaking parts the queue needs that have no face** (existing speakers,
companions included, already have one - `build/API.md`'s `FACES` list):

| step | who | count | answer |
| --- | --- | --- | --- |
| A8 HOB-3 | two apprentice bandits | 2 | generate |
| A10 NIX-5 | the person got through the Gloamwood (witness, bailiff or bassoonist) | 1 | generate |
| A11 WRE-3 | the society: chair, secretary, the one who is devastated; six more members as extras with no lines | 3 | generate |
| A14 ROL-3 | the eleven parties' cameos - several exist (the Forty-Fourth's Ysolde, the Forty-Sixth's Nabb and Tolly); say six new | ~6 | generate; share stock faces for any with one line |
| B3 PIP-3 | two rival acts (Mr Tweddle is the third) | 2 | generate |
| B5 NIX-1 | the client, if they are not somebody already drawn | 0-1 | decide in the step |
| B7 ROL-1 | the Convenor and three fellows | 4 | generate; the fellows "of no importance" may share |
| C1 ZEPH-1 | the Registrar's clerk - `SITES.md` 17 designed him and did not draw him | 1 | generate |
| C4 WRE-1 | Rowbotham's students (the three reviewers are two students and the duck) | 2 | generate |
| D2 COR-2 | the schoolmistress, if she speaks | 0-1 | generate |
| E3 MER-3 | four visiting healers (Ysolde is the fifth) | 4 | generate |
| E13 PIP-1 | Ambrosine, Piper's aunt | 1 | generate |
| E14 NIX-3 | Cobb Lorrimer | 1 | generate |
| E17 ROL-5 | the understudy | 1 | generate |
| | | **~30** | `Gen_People11` 3-7, then `Gen_People12`-`15` |

**Things only Mike can supply**, added to `AUDIT.md` item 1's list as
provisional rows - they become real only if the step gives them lines or a
fight:

* **The Duck** (ZEPH-2, WRE-1): a face if it speaks. It is a reviewer and a
  voting Fellow; it probably does.
* **Duchess** (ALD-4): only if the reunion gives her a line. `COMPANIONS.md`
  says the reward is a scene; a scene can be wordless.
* **The Wrong Dragon in the light** (ALD-6): `AUDIT.md` already says so.
* **Spare's side-view battler** and **Mrs Cotterill's enemy image** (part F):
  `SPARE.md` 6. Both are stock-face characters (`SF_People1`), so the
  generator cannot draw a match. **This is the one hard blocker in the queue**:
  `validate.py` fails a side-view actor with no battler.
* **Enemy art** for ALD-2's vigil, PIP-3's hecklers, WRE-1's eleven specimens
  and ROL-2's thing: stock monster art first; anything that is a generated
  person gets `art.py`'s stand-in and goes on the list for real art.

---

## 2. The queue

Order: `COMPANIONS.md` 6. **Part A is the no-map row**, cheapest and most
certain first; then Great Dunnage's seven (B), the Collegium's four (C),
Ashcombe's two (D), everything else (E), Spare (F), and the ending (G).
Forty-nine quests: A 15, B 7, C 4, D 2, E 18, F 3.

Each step: **quests**, **exists** (the "inherits" notes from `SITES.md`, and
what was checked), **new**, **scenario**.

### Part A - no new map

**A1. WRE-2 The Second Plaque** - and the effort's plumbing.
* *Exists:* Map 14. The goose is event 14 at (18,4), two pages, its first
  page with a Wren branch in which Dorcas asks her to leave "for a bit, while
  I decide" - she is never actually removed, so "readmission" is a line, not
  a mechanic. The first plaque is event 18 at (17,4). Dorcas is event 2 with
  **a five-page Feud ladder** - so WRE-2 does not go on Dorcas (0.2); it goes
  on the goose, whose ladder is one self switch, A.
* *New:* `SW_WREN_STORY` .. `SW_ROLAND_STORY` (101-109) and
  `VAR_COMPANION_STORIES` (15) in `db.py` and System.json;
  `story.companion_story(actor)`; `q_wren.py`. Two pages appended to the goose
  (A + Wren: the ask; A + Wren + the plate: the handover), the brass plate (an
  item), wherever it is got, and the second plaque as a new event beside the
  first, shown once it is up. One trope (the retcon). `TIMELINE.md` if the
  plate carries a date (#41 is 1940).
* *Scenario:* `q_wre2` - the goose with and without Wren, the plate, the
  handover, the second plaque, both plaques read, `SW_WREN_STORY` and the
  counter; and the goose without Wren asserted unchanged.

**A2. WRE-5 Bramus.** *Exists:* nothing named - "nothing new". A small brown
thing in a turnip field: Thistlewick's fields (Map 1) or Firstfield. *New:*
one event (pattern 1) where it lives; Bram's reaction. Candidate ending line:
the Prophecy has read the journal. *Scenario:* `q_wre5`.

**A3. PIP-2 A Rhyme For Turnip.** *Exists:* the ballad (`SW_BALLAD_DONE`,
verse seven struck - read `CLAUDE.md`'s switches 59-60 and the ballad's
event before choosing a venue). *New:* one scene with one branch per
companion in the party (Hob, Wren, Corvin, Aldric, Nix at least - "X and Y"
is branches, not pages), the ballad's last verse, a trope per suggestion.
Decide Piper's gear here or record that she has none. *Scenario:* `q_pip2`,
run with two parties so every branch is taken once.

**A4. MER-2 Fit To Travel.** *Exists:* Nether Sopping's scales (find the
event), the lighthouse's lamp (Map 18, `SW_LAMP_LIT`). *New:* Certificate of
Fitness (key item), the fetch chain as global switches, the examination
(wherever the party is standing - probably a common event run from the
certificate or from Merribell's page), **one witness branch per companion**,
eight of them, and several blushes. Candidate ending line: the first properly
documented attempt. *Scenario:* `q_mer2`, and each blush asked twice.

**A5. ROL-4 The Maker's Mark.** *Exists:* Roland leaves at the tower door
with his gear handed back (`guest_leaves`, `SW_ROLAND_GONE`); Hob's aunt's
name is on his hammer (Beatrice, `db.py` ~1374). *New:* the look at the mark,
Roland **and** Hob (a branch inside one page), and a refit after Roland has
gone that makes his sword Hob's. The moment must be reachable *before* the
tower door. *Scenario:* `q_rol4`.

**A6. HOB-5 Two Smiths, One Forge.** *Exists:* Map 24 (Ollerenshaw's), Bryd,
Grommet, `SW_HOB_BRYD`. *New:* appended pages requiring `SW_HOB_BRYD` and
Bryd's own terminal switch; the boiler tube plate (key item); Ott's approval
as a page on Ott **below her ladders**, so it requires `SW_OTT_MATERIALS`.
*Scenario:* `q_hob5`.

**A7. ZEPH-5 The Lay-By, and MER-4 The Man Who Cannot Stay Down.** Two small
ones on built one-scene sites. *Exists:* `nomap.py`'s Lay-By at (11,88) -
Dunnock, Miss Privet, Mrs Quickset, two pages; Tobias Frayne on Map 43 -
event 2 with a two-page pair, the ladder 3, the book 4, **the jar 5, sealed
and unpaid**, the shelf 6, and the book's twelfth line ruled, dated today and
empty. *New:* a quest page on each; a skill for Zephyrine in 46-49, "taught
badly, that works"; Tobias's jar opened and paid out; the twelfth line left
empty. *Scenario:* `q_zeph5_mer4`.

**A8. HOB-3 The Anvil.** *Exists:* Hob's smithy (Map 6), Crooke (enemy 25,
troop 26, camp at `places.WORLD_CAMP`), the bandit syllabus. Check what state
Crooke is in after his bounty before writing her line. *New:* the anvil
gone and found eleven feet outside the door; two apprentice bandits (2 faces);
the apology (key item). *Scenario:* `q_hob3`.

**A9. NIX-4 The Longest Loan.** *Exists:* Nix's Emporium (Map 7). *New:*
eleven returns to eleven existing people across three towns - each one an
appended page, so **each owner's ladder is read first** - a variable counting
them, and the ledger's last page. *Scenario:* `q_nix4`, which is long; split
it by town if it outruns a timeout.

**A10. NIX-5 Half An Encounter.** *Exists:* the Gloamwood (Maps 9-10). *New:*
the person to be got through (1 face); night on the Gloamwood as a tint while
the escort is on; **a fight fails it**, detected without touching a troop by
storing `$gameSystem.battleCount()` in a variable at the start and comparing
at the far end. *Scenario:* `q_nix5`, with encounters **on** for once, and a
forced battle to prove the failure.

**A11. WRE-3 The Thing In The Gloamwood.** *Exists:* the Gloamwood; "an
existing inn" - the Gilded Turnip (Map 4) or the Slain Wyvern (Map 14).
*New:* the society (3 faces, six extras), the walk, the badge (accessory -
possibly Wren's gear, 0.5). *Scenario:* `q_wre3`.

**A12. PIP-5 The Struck Verses.** *Exists:* Prophecy Hall (Map 3), verse
seven (`SW_BALLAD_DONE`). *New:* the box, "a form, a key and a distraction";
the archive room - **find out first whether Map 3 has room for it**, and if
not, it is a room in the black of Map 3 rather than a new map. The count shown
is `VAR_BLUSHES`, read back. *Scenario:* `q_pip5`.

**A13. HOB-2 The Grave He Has Not Made.** *Exists:* Beatrice (weapon, and a
prop in the smithy, `village.py` ~1326). **Thistlewick has no churchyard**,
and `COMPANIONS.md` says "one appended corner of Map 1". Drawing on a
published map is new tiles on a published map, which 1.7 does not name either
way: **argue it in writing in the step** (an empty corner, nothing moved) or
put the gate somewhere that already exists (behind the chapel, Map 5). *New:*
the four attempts, the gate, Hob's weapon (0.5). *Scenario:* `q_hob2`.

**A14. ROL-3 The Alumni.** *Exists:* the Slain Wyvern, and several of the
eleven parties' people are in it already. *New:* the dinner as a separate
state of the room - probably extra events shown only while a switch is on -
~6 faces, the toast, the small gifts. Must be before the tower door.
Candidate ending line. *Scenario:* `q_rol3`.

### Part B - Great Dunnage (Maps 61-65, `dunnage.py`)

**B1. HOB-1 The Assize of Hammers.** *Exists:* Prime Warden (event 2, Map 62),
Warden Crabbe (3), the Schedule (4), the last prize, a hinge (5), the Assize
"in the spring, every three years". *New:* the retrieval tour - eleven
appended pages on existing people, which is "the cheapest big quest"; the
submission; a Company mark. Candidate ending line: the judges' notes.
*Scenario:* `q_hob1`.

**B2. ALD-4 The Horse.** *Exists:* Duchess, event 15 on Map 61 (`Vehicle` 4,
direction fixed), Mr Plummer (14) and the saddle with a crest; PLUMMER &
PARTNER. *New:* the reunion - a scene, no mechanical reward. *Scenario:*
`q_ald4`.

**B3. PIP-3 The Contest at the Sign of the Bell.** *Exists:* Mrs Harbottle
(event 3, Map 65), Mr Ambler (4, gives nines), Miss Quayle (5, gives twos),
Mr Tweddle (6, a nightingale). *New:* the heckling troop and its enemies, two
rival acts (2 faces), second place, framed. *Scenario:* `q_pip3`.

**B4. COR-5 The Appraisal.** *Exists:* Miss Fettle, event 7 on Map 62, who
always asks after the tang. *New:* the form for a curse, the optional curse
as a state (40-44) with a real trait. *Scenario:* `q_cor5`.

**B5. NIX-1 The Client Identifies Themselves.** *Exists:* the warehouse door,
event 7 on Map 61, pages 1-2, a quest page after them; Mr Tibbs event 2 on Map
64 with a two-page pair; the wardrobe (3), locked; the Bond Book (4), "coat".
*New:* the client, the coat (Nix's armour). *Scenario:* `q_nix1`.

**B6. NIX-2 The Sealed Counting House.** *Exists:* Map 63's lobby, the Door
(event 3, `!$Gate2` 2), the Mayor (2), the memorandum of 1788 (4), the Town
Clerk and Form L (5), the painted key on the crest. **The room behind the Door
is not built**: it goes in the black north of Map 63, drawn in `dunnage.py`.
*New:* the room, the gold the Corporation insists you keep. *Scenario:*
`q_nix2`.

**B7. ROL-1 The Appointment.** *Exists:* the Bell or the Smiths' Hall for the
room. *New:* the Convenor and three fellows (4 faces), the minutes (key item).
Before the tower door. *Scenario:* `q_rol1`.

### Part C - The Collegium (Maps 58-60, `collegium.py`)

**C1. ZEPH-1 The Fines.** *Exists:* the world-map doors carry her refusal at
pages 1 and 2, a quest page after them; Prewitt event 2 on Map 59, two-page
pair; **the Register of Outstanding Fines, event 3**. *New:* the Registrar's
clerk (1 face), her name back, the robe (0.5), and the real choice to refuse
and stay expelled. *Scenario:* `q_zeph1`.

**C2. ZEPH-3 Dean Fenwold Is Fine.** *Exists:* the Hall (Map 60), Dean Fenwold
and his portrait. *New:* the biggest fire in the game, no consequences.
*Scenario:* `q_zeph3`.

**C3. ZEPH-2 The Duck**, and **C4. WRE-1 The Monograph** - `COMPANIONS.md` says
build these together; two sessions, one after the other. *Exists:* the Duck's
Pond (`nomap.py`, (115,40)) with the medal; the monographs, event 5 on Map 59,
with the inch-wide gap. *New:* the duck as an escortable event; the eleven
type specimens (enemies 41+, troops 41+) and their fights; the three reviewers,
one of them the duck; the subscription list as a shop; Wren's party ability
upgrade. The Duck's face if it speaks. *Scenarios:* `q_zeph2`, `q_wre1`.

### Part D - Ashcombe (Maps 52-53, `ashcombe.py`)

**D1. COR-1 Ashcombe (New).** *Exists:* her door, event 3 on Map 52, with
Corvin's refusal at pages 1-2 - its own page goes after them; the Flood
Dinner's speaker TO BE CONFIRMED (event 9); Mrs Ash, event 2 on Map 53,
knitting something long; the bedroom that is a study was **not built**.
*New:* the study, the invitation, the scarf (Corvin's accessory). *Scenario:*
`q_cor1`.

**D2. COR-2 Ashcombe (Old).** *Exists:* Ashcombe Lake on the world map
(`nomap.py`), the Roll in the museum with one name "Away. (Written to.)".
*New:* the drowned street (a small map, 66+), the doorstep, the sword's name.
*Scenario:* `q_cor2`.

### Part E - the rest, in built places

Order within E is cheapest first; reorder freely.

| step | quest | exists | new |
| --- | --- | --- | --- |
| E1 | MER-5 The Well at Sump | Thurle event 3 on Map 51 (two-page pair), Gammage 4, Mrs Pardew 5, the well 6, the minutes 7, the sign 8, the pool 9 | the biggest trope payload in the document |
| E2 | MER-1 The Sisterhouse | Map 55: the Prioress 2 (two-page pair), Bewick 3, Sir Hamo 4, Lamb 5, Nuttall 6, Dace 7, the line and minutes 8, the correct treatment 9, the empty bed 10, the shelf 11, the doctrine 12; Map 54 chapel 5, founder's stone 6 | the queue of forty; the Pamphlet (Merribell's gear) |
| E3 | MER-3 The Healers' Table | the Slain Wyvern | four visiting healers (4 faces), Ysolde's line, the Table's Kit |
| E4 | ALD-3 The Chapter House | Mordaunt event 2 on Map 48 (two-page pair), the committee's table 11-12, files 13-14, desk 15 | a proper rank |
| E5 | ALD-1 The Errand | Little Gore (Map 50), where Aldric walks in and nobody notices; Hester Vane; the banns | the letter delivered |
| E6 | ALD-5 Pemberton-Gore the Fourth | the Fourth is drawn (`Gen_People5` 3) and at Fenmarch | a page on Aldric everywhere afterwards |
| E7 | ALD-2 The Vigil | the chapel at Weeping Bottom (Map 54, event 5) or Coldbarrow | the vigil troop (turn-count victory), the shield (Aldric's gear) |
| E8 | ALD-6 The Wrong Dragon | `nomap.py`'s cave, Somebody Large, Horace | the scene in the light (Mike's art) |
| E9 | WRE-4 The Cabinet | Mr Ottershaw event 4 on Map 57 (two-page pair), the Marsh Bear's case 15, the joins | the write-up, the fee |
| E10 | COR-3 The Rivals' Retreat | Crake event 2 on Map 49 (two-page pair), Veyle 3, Rook 4, Morrow 5, Blackwood 6, Mrs Garrow 7, the league table 8, rota 9, newsletter 10 | seventeenth, and fixing it |
| E11 | COR-4 Mother Selvidge | `nomap.py`'s Fair, two crowns, her third reading unsaid | the reading about four young men a year |
| E12 | PIP-4 The Elegy | Little Gore or Sump | eleven appended pages, the song |
| E13 | PIP-1 The Authorised Version | Prophecy Hall | Ambrosine (1 face), the document |
| E14 | NIX-3 Professional Courtesy | an existing town | Cobb Lorrimer (1 face), his tools |
| E15 | HOB-4 The Sky Anvil | `nomap.py`, Elias Meech, a gate for a gatepost; the west road | star-iron, one weapon, not for Hob |
| E16 | ZEPH-4 The Cinder Fen | `nomap.py`, the Commissioner (faceless on purpose), the triplicate | the burning, the road it opens |
| E17 | ROL-5 The Understudy | the finale's pages - **read `CLAUDE.md` "The ending" and the Former Premises' pages 3-5 first** | the understudy (1 face), a page at the tower door |
| E18 | ROL-2 Roland's Own Quest | nothing | a small dungeon (67+; COR-2 took 66), the thing, the better sword |

### Part F - Spare (`SPARE.md`, `q_spare.py`)

Re-planned with Mike, 5 Oct 2026: four steps, not three. SPA-3 leaves this
effort (see "Owed"), a new quest takes Village 1, and SPA-2 is reached through
Cotter. `COMPANIONS.md`'s Spare section has the same changes.

**F1. Spare joins.** `SPARE.md` whole, with its switches renumbered to 89-92
first. **Unblocked, 5 Oct 2026.** At Mike's word Spare was redrawn whole with
the generator, `Gen_People14` 4 (`build/characters/spare-cotterill.json`):
face, sprite and battler `Gen_People14_5` all match, and `FACES["Spare"]`
points there. Mike supplied `img/sv_enemies/Mrs_Cotterill.png`. Both images
are in. Decided before it was built, keeping to `SPARE.md` wherever the game
still allows:
* *The gate* is `SPARE.md`'s A + B + C + D. B is `SPARE.md`'s own list of the
  family - Mr and Mrs Cotterill, Ferrule, Clevis, Shim and Bessie on the
  street, Rivet, Gudgeon, Tappet and Grommet indoors - and **not Cotter**, who
  was drawn later in Great Dunnage and is F4's way in. C is `SW_AIRSHIP`
  (53), the day Ott hands the Two Hundred over. (F1 first built it on
  `SW_TWO_HUNDRED_FLEW`, 68, taking `SPARE.md`'s "has flown somewhere real"
  at the switch it named - but 68 means *set down beside the tower*, a
  narrow and arbitrary thing to require; Mike, 6 Oct 2026.)
  A, B and C are script reads inside Gudgeon's page (a page condition names
  two switches at most).
* *Class 12*, not 11 - WRE-1 took 11. *Weapon type 13 "Bag"* and *armour type
  14 "Washer"*, his alone. *States 42-43*: They Never Hit Me, and Ninety
  Tubes' DEF break. Every other id is `SPARE.md`'s.
* *The bag is the joke*: every skill's battle message is a thing he takes out
  of it, and all but Temper Tantrum (he puts the bag down) need it equipped.
* *The ending block is G1's*, with everybody else's.

**F2. SPA-1 The Letters - the courier.** There is no period post box in any
sheet (`SF_Outside_C`'s `Postal Box` has a lit button panel and is on a
tileset no town uses), so the post is a **courier: the same man, every time**,
one generated character with one look - cap, satchel, red coat - who is
somehow already standing in every town Spare writes from, including the ones
only the airship reaches. He never explains; he is on his rounds. Spare hands
him a letter per town, four lines each, increasingly untrue; the set is
readable from the menu; the payoff is `COMPANIONS.md`'s, at the works, at the
dinner hour, with the dragon. **Done, 6 Oct 2026** (section 3).

**F3. SPA-4 The Pen Pal - Village 1.** Village 1, (60,61)-(61,61), deferred by
`SITES.md` step 9 and section 4 for exactly this. A nice village with people to
talk to and funny things to walk into, and **a girl of about Spare's age who
has been his pen pal**, whom he finally meets. The courier has been carrying
their letters for years, so she has had every untrue letter he ever wrote -
she knows about the dragon - and hers back were exactly as untrue. After F2,
so the letters exist. It retires the last placeholder door, so
`placeholder_doors` changes with it; new faces are generated. **Done, 6 Oct
2026** (section 3): Much Pottering, Maps 68-69.

**F4. SPA-2 Ninety Tubes - through Cotter.** Cotter works the Iron Company's
gate in Great Dunnage (`dunnage.py`). With Spare in the party he knows his
brother, and he has a job a man does not fit: the jammed lock gate on the
Dunnage cut. The party waits outside and Spare goes in alone, with
`SPARE.md` 3's party swap, on a confined map (68+). Cotter's published scene
stays as it is; the new page requires his ladder's terminal. **Done, 6 Oct
2026** (section 3): the bottom lock, Map 70.

### Part G - the ending, last

**Before G: the playtest round** (Mike, 7 Oct 2026). Mike's first
playthrough of the earlier content turned up the list below, and it goes
in before the ending, in this order. One step per session, as before.

* **P1. Playtest fixes.**
  * **NIX-5's escort is luck, not care.** The Gloamwood rolls an encounter
    about every 26 steps, Nix's half-encounters makes that about 52, and the
    walk through Maps 9-10 is long against that. An accessory cannot help:
    Encounter Half does not stack with Nix's, and Encounter None trivialises
    the quest. Add a cheap consumable sold in shops that pushes the next
    encounter back a fixed number of steps (a Repel), which stacks with Nix
    and is useful anywhere, and have Bagshawe mention it at the mouth.
    Measure the walk first, so the odds come out at "a careful player
    usually makes it".
  * **PIP-3's contest is Piper alone.** She is the one performing, so the
    party watches from the floor. Use `SPARE.md` 3's swap, as Spare's
    argument and the culvert do, and retune troop 41 for one performer with
    `balance.py`. Losing costs nothing: she finishes anyway, and the scores
    are fixed.
* **P2. The early maps** (fix-on-sight; "additive only" protects the
  storyline, not bugs). The changes that touch every map go first:
  * A dark doorway tile under every town door event, so an opened door
    leaves a hole, not a wall.
  * Shadows in building interiors.
  * The forest ring that alternates whole trees with four quarter-trees.
  * A `validate.py` check for events that block without being drawn, then
    every one it finds: the Obligatory Tower and elsewhere.
  * The Adventurers' Guild (Provisional): the invisible door mat, a
    scattered layout, and a shield standing in for a sign.
  * A sword on the mantel in Bram's house that is gone once he has it.
  * The Door into the Mountain and the floating island: Mike draws them in
    the editor, commits the edited `data/` maps without rebuilding, and the
    step diffs his tiles into the build script.
* **P3. Olde Evermore** needs more elves about doing things.
* **P4. The post-game.** The Prophecy's defeat stops being the end: the
  finale's tally plays, then the party is back in the world, open, with
  unfinished quests still finishable. It starts as a short design doc agreed
  with Mike: the tower's state; Thistlewick's lines; whether the pension and
  the place in Nether Sopping still happen; whether the Prophecy is really
  over; and whether an ending tally still makes sense when the game goes on.
  **The Door into the Mountain is post-ending content** (Mike, 7 Oct 2026):
  Sir Dunstable's lamp at a quarter past four, and what is behind the door.
  G1's ending lines are written in the same pass, because they live in the
  finale event that now hands back to the world.
* **The quest log (G0)** has no dependency on P1-P4. The plugin (Q0-Q7) can
  be built in a parallel session at any time, and adoption follows it.
  Post-game quests are added to `quests.py` when they are built.
* **Then G1's counter re-cuts, the one full suite, Mike's playthrough, and
  the push**, in that order. The re-cuts come last because P4 adds tropes.

**G0. The quest log** (added 7 Oct 2026). Install the workspace's generic
quest-log plugin (`../QUESTLOG.md`) once its milestones Q0-Q6 are done. It goes
**before G1** so that G1's one full suite and Mike's playtest cover it too;
putting it after the release would mean a second suite, a second playtest and
a second push. The plugin is generic. Everything below is this game's side of
it, and none of it belongs in `tools/questlog/`.

* **Inventory.** Every quest this game has, with its start, done and fail
  state: the main line (switches 1-5), the side quests in `CLAUDE.md`'s
  switch table (the Feud, the Guild, bounties, lighthouse, the Pit, the
  Barrow, the bench, Hosea's history), the north (47-71, `NORTH.md` 10),
  Firstfield Meadow (81-87), the world-map sites (`SITES.md`), and the
  companion quests (111-250, each step's Done paragraph). Most are already
  ask/done switch pairs, so a binding is two constants from `db.py`.
  Anything kept in a **self switch** or only in a counter variable gets
  listed, because those are the bindings `check.py` cannot fully check.
* **Bind to the quest's own switches, never to `SW_RECRUIT` (11-19)**,
  which go off when a form desk strikes somebody off. The plugin latches
  completion, but a quest bound to a recruit switch would still drop out of
  Active mid-quest. `SW_KNOWN` (72-80) and `SW_<NAME>_STORY` (101-110) are
  safe.
* **`build/quests.py`** writes `data/Quests.json` through `questlog.py` and
  is called from `build_game.py`, which also calls `questlog.install()`. No
  database ids are spent, and no existing event changes: the log reads
  state that is already set. Nothing in this step needs a plugin command.
* **Text.** Titles and objectives are plain and short, because they are
  instructions. Descriptions can carry the game's voice, but they are new
  writing and get Mike's eye, the way every published line does. A quest
  that is finished gets a closing description, keyed on its done switch.
* **Spoilers.** An objective that names a twist is `"hidden": "omit"` until
  its `visible` switch is on. SPA-3 is past the ending and does not appear.
* **The menu entry is there from the start** (Mike, 7 Oct 2026): Bram has
  the log from the first screen, so no `menuSwitch`. There are no spoilers,
  because a quest is not listed until it is started. The only care needed is
  in the objective text of a quest that has already started.
* **Fizz's line stays, and gets an answer** (Mike, 7 Oct 2026). This is a
  splice inside Dilys's published "Yes" branch (`meadow.dilys_event`),
  agreed because nothing is lost and it is only improved. After "...We
  haven't got a quest log. / Just remember it! Really hard!":
  `You point out that you do have a quest log, and that this quest has just
  appeared in it.`, then Fizz with Mike's choice of option b - "...Oh." /
  "Remember it anyway. Really hard. Just in case." - optionally preceded by
  "...WHO GAVE YOU THAT?" / "Nobody tells ME anything." He was happy with
  either. `SW_FF_SHEEP_ASKED` moves up to just before the narration, so the
  quest really is in the log when the line says so. If the plugin only
  shows a banner when the screen is idle, the timing is adjusted so the
  banner and the line agree.
* **Two Firstfield quests**: the sheep (which are pigs), started on
  `SW_FF_SHEEP_ASKED` and done on `SW_FF_SHEEP_DONE`; and **"We haven't got
  a quest log."**, started and done on `SW_FF_SHEEP_ASKED`, so it arrives
  Completed. Its description is "Check your quest log so that you don't have
  to remember really hard." Old saves past the meadow file both under
  Completed, silently.
* **Old saves.** `live-rpg` players have saves from before the log. The
  plugin's silent first snapshot (`QUESTLOG.md` 2.5) is the whole answer, and
  a scenario asserts it: load a mid-game state, delete `_questLog`, and assert
  that nothing is announced and the finished quests are under Completed.
* **Checks.** `validate.py` (which runs `check.py`), one scenario
  `ql_log.json` sampling one quest per part through each status with
  screenshots of the scene, and the old-save scenario. The full suite is
  G1's.
* **Done paragraph** names the quest count, every self-switch binding, and
  what Mike decided for the menu switch and Fizz's line.

**G1.** One `if_then` block per companion on `SW_<NAME>_STORY` (and Spare's),
each choosing one line from its quests' candidates, and one closing line on
`VAR_COMPANION_STORIES` (1.4), appended to `journey.finale_event`'s tally
before THE END; `finale_ending` extended to assert them. Then **both counters
re-cut** against the new totals, the comments above both branches updated,
and `CLAUDE.md` "The ending" amended. Then the **full suite**, once, eight
hours, in the background. Then Mike plays it. Then, and only then, `live-rpg`.

### Owed, and not in this effort

`COMPANIONS.md` 8's hook - **the Door into the Mountain**, the lamp from Sir
Dunstable at a quarter past four - is not a companion quest. It stays owed.

**SPA-3 The Tenth** moves to the extension past the current ending (Mike, 5 Oct
2026): spring comes *after* the Prophecy is beaten, and the party takes Spare
home for it. Nothing in this effort may settle the baby - G1's line for Spare
included.

---

## 3. Done

*(one paragraph per step, as `SITES.md` 3 has them: what was built, where, the
ids taken, the tropes and blushes added, and what the next step inherits)*

**A1, WRE-2 The Second Plaque - done.** `build/q_wren.py`, hooked from
`south.py` in three places; `build/scenarios/q_wre2.json`. What is worth
carrying forward:

* **The plumbing is in.** `db.SW_STORY` (101-109), `db.VAR_COMPANION_STORIES`
  (15) and `story.companion_story(actor)`, which turns the switch on and
  counts it the first time only. System.json's switch list is 251 long now.
* **Ids taken:** switches **111** `SW_WRE2_ASKED` and **112** `SW_WRE2_UP`;
  item **40** `IT_BRASS_PLATE`. Next free: switch 113, item 41.
* **It hangs off the goose, not Dorcas** - Map 14 event 14's pages 3-5, all
  on its self switch A and `actorValid` Wren; page 3 is the ask (or, once
  asked, "By the letter"), page 4 the handover on the plate as an `itemValid`,
  page 5 afterwards. Dorcas's Feud ladder is untouched, which is the pattern
  for any NPC whose terminal switch is somebody else's quest.
* **The plate is engraved at Wick & Barrow's** - a new event, **The Engraving
  Card**, event 5 on Map 16, in the basket at (4,6) beside Mrs Barrow, and a
  new thing to read for everybody. A crown a letter: `q_wren.PLATE_PRICE` is
  counted off the four lines on the brass and asserted to be the 128 she says
  aloud. The negotiation needs Wren; the wording is then left with Mrs Barrow
  (the card's self switch A), and anybody can pay. So a Wren dismissed at any
  point leaves the errand where it was, and only the handover needs her.
* **The second plaque is event 21 on Map 14 at (19,4)**, the right of the
  fireplace, mirroring the first (event 18, (17,4), the left). Neither is a
  sprite - the fireplace is the picture, as it always was. It has no page
  until `SW_WRE2_UP`, then one, for everybody.
* **Readmission is a line**: the goose's first page asks her to leave "while
  I decide", so Dorcas says "Decided."
* **One trope** (the retcon), at the ask. **No blush.** Running tally for the
  effort: tropes +1, blushes +0.
* **Candidate ending line** (G1 chooses): none - WRE-2's reward is the room.
  WRE-5's is Wren's likelier one.
* **Wren's gear**: not from WRE-2. Still open - WRE-3's badge is the
  candidate (0.5).
* `TIMELINE.md`: the plate says 1940, #41's year, and the row names it.

**A2, WRE-5 Bramus - done.** `q_wren.bramus`, hooked from `village.py` in one
line; `build/scenarios/q_wre5.json`. What is worth carrying forward:

* **It is Bram's own field, Map 1** - event 25, **Bramus's Burrow**, at
  (15,27) in the fourth soil row. The creature is never drawn - the stock
  character sheets have nothing small and brown, and it is of no consequence
  - so the event is a tile: `mapkit.BURROW`, Outside_B 169, the sheet's own
  `Hole`. It blocks its cell; the crop rows are walkable, so nothing is sealed.
* **Without Wren there is no page at all** until it is named, so a game that
  never recruits her has Map 1 exactly as it was (the scenario walks onto the
  cell). Page 1 (Wren) is the naming; page 2 (`SW_WRE5_NAMED`) is the label
  on its stick, for everybody; page 3 (named + Wren) is "Still here."
* **Ids taken:** switch **113** `SW_WRE5_NAMED`. A global rather than a self
  switch for the ending's sake: `SW_STORY[WREN]` is on after *either* of her
  quests, and the Bramus line is not true of a party that only put up a
  plaque, so **G1 reads 113 for this line, not 108**. Next free: switch 114,
  item 41.
* **Bram's reaction is narration**, as he always is: touched, then the
  rationale ("statistically indefensible"), then touched anyway, because it
  is accurate.
* **One trope** (the honour that is an insult), at "In print". **One blush**:
  "Distinguishing features: none. Goes pink when it is looked at", written
  down under Bram's name (rewritten October 2026, NORTH.md 1.6). Running tally for the effort: **tropes +2, blushes +1**.
* **Candidate ending line** (G1 chooses; read `SW_WRE5_NAMED`):
  "The Prophecy does not read journals. It has read one." /
  "Bramus agricola: statistically indefensible."
* Wren's gear: still open - WRE-3's badge.
* `TIMELINE.md`: nothing dated.

**A3, PIP-2 A Rhyme For Turnip - done.** `build/q_piper.py`, hooked from
`village.py` in two lines; `build/scenarios/q_pip2.json`. What is worth
carrying forward:

* **The venue is the gilded turnip itself** - Map 4, event 6, on its plinth
  in the Gilded Turnip. It was one page with no switches, so pages 2 and 3
  are appended with no ladder to wait on; page 1 is byte for byte (checked
  against HEAD), and is all a party without Piper sees. `village.py` hands
  the prop's own image to `q_piper.turnip_pages`, so the turnip looks the
  same whoever is standing there.
* **Page 2 needs Piper and `SW_LEFT_VILLAGE`** - not before the road, or the
  quest is five minutes after she joins, in the same room - and opens with a
  "Not now". Page 3 (Piper + `SW_PIP2_DONE`) is "Nine seconds." afterwards.
* **One `if_then` per companion**, eight of them - everybody but Bram and
  Piper, the five `COMPANIONS.md` names plus Merribell (the body, top to
  bottom, at volume: **a blush**), Zephyrine ("sherbet", and who set fire to
  the Dean) and Roland (the right answer at a quarter past two, ignored, and
  gracious about it afterwards, which is worse). Bram always has a go:
  "parsnip". The scenario takes every branch exactly once over two parties.
* **The verse** is `q_piper.VERSE`, and the fix is the joke: the draft ends
  its second line on "turnip"; she ends it on "grate" and moves the turnip
  down a line, where nothing has to rhyme with it.
* **Ids taken:** switch **114** `SW_PIP2_DONE`, for the ending, as 113 is.
  Next free: switch 115, item 41.
* **Tropes: one per suggestion made plus one for the payoff** - 2 to 9 in a
  play, 4 for a party of three companions. **Blushes: +1** if Merribell is
  there. Running tally for the effort: **tropes +2 fixed and 2-9 here,
  blushes +1 fixed and 0-1 here** - G1 counts the reachable maximum as 9 and
  1.
* **Piper's gear is decided: PIP-3's rosette for second place** (0.5). PIP-2
  gives none.
* **Candidate ending line** (G1 chooses; read `SW_PIP2_DONE`): "The ballad's
  last verse took an afternoon and nine seconds, and the turnip is in the
  middle of a line, where nothing has to rhyme with it."
* `TIMELINE.md`: nothing dated.

**A4, MER-2 Fit To Travel - done.** `build/q_merribell.py`, hooked from
`north.py` and `south.py` in two lines each and from `db.build_common_events`
(an import inside the function - `q_merribell` imports `db`);
`build/scenarios/q_mer2.json`. What is worth carrying forward:

* **Clause eleven is found on Upper Clanging's Parish Notices** (Map 21,
  event 9): a works town prints fitness forms, and there is a pad of them.
  Page 2, for Merribell, reads the notices first and then finds the pad; it
  gives the blank form, **item 41**, and `SW_MER2_ASKED` **115**. One trope
  (the prologue medical), there.
* **The three fetches are the form, the scales and the lighthouse.** The fish
  stall at Nether Sopping (Map 13, event 10) lends its stamped scales,
  **item 42**, `SW_MER2_SCALES` **116**, on a page gated only on 115, so a
  dismissed Merribell does not strand the errand; after that it is the shop
  it always was. The light is `SW_LAMP_LIT` - the lighthouse quest already
  ends with a lamp in your hands. Both events' first pages are byte for byte.
* **The examination is common event 3**, `CE_FIT_TO_TRAVEL`, run by using the
  blank form from the Key Items menu (occasion menu, scope none - scope none
  goes straight to `useItem`, and the common event sends the scene back to the
  map). It is therefore wherever the party is standing. It needs Merribell,
  the scales, the light and a witness, and says which is missing, in order.
  **This is the pattern for any quest that happens "wherever you are".**
* **The witness is whoever is third**: the first member who is neither Bram
  nor Merribell, written into **variable 16** `VAR_MER2_WITNESS` - so the
  ending, or anything else, can say who. One branch per companion, eight,
  each reacting to the same line of dictation ("Inguinal: clear. Both
  sides."). Sir Aldric shields Bram at arm's length with his cloak, facing
  the wrong way, and attests to all of it.
* **Blushes: three, each once** - the chest, the cough, and the witness
  writing it down - because the form is spent and nothing can run the common
  event again. **Tropes: one.** Running tally for the effort: **tropes +3
  fixed and 2-9 from PIP-2; blushes +4 fixed and 0-1 from PIP-2.**
* **Done:** `SW_MER2_DONE` **117**; the form and scales spent; the
  Certificate of Fitness, **item 43**, which does nothing. Next free: switch
  118, variable 17, item 44, common event 4.
* **The scenario plays one examination through** (Aldric) and runs the other
  seven witnesses through the common event's own list with the messages made
  non-blocking, the finale's trick - a full examination is about forty
  windows and **outlasts a ten-minute timeout at headless speed**, so run
  `q_mer2` in the background.
* **Candidate ending line** (G1 chooses; read `SW_MER2_DONE`): the Prophecy
  notes that this is the first properly documented attempt in four thousand
  years - and, if G1 wants it, `\\N[\\V[16]]` names the witness.
* `TIMELINE.md`: nothing dated.

**A5, ROL-4 The Maker's Mark - done.** `build/q_roland.py`, hooked from
`village.py` in two lines; `build/scenarios/q_rol4.json`. What is worth
carrying forward:

* **It is at the anvil in Hob's smithy** - Map 6, event 4, Beatrice, one page
  and no switches; the forge the sword was made at. Page 1 is byte for byte.
* **Before the door: Roland's page, Hob a branch in it.** Roland never
  *equips* Fairweather's Own - he wears the practice sword and carries the
  other, and `roland_departure` hands it over from his pack - so he takes it
  out to show. Hob: "That's my aunt's." ... "She did good work." Beatrice,
  for once, says nothing. **Nobody explains the hammer**, and the scenario
  asserts that no line of the scene says "hammer" at all. Roland alone gets a
  look at the forge and nothing more.
* **The refit is Hob's page, after `SW_ROLAND_GONE` and the mark seen**: the
  blade on an ash haft, **weapon 40** `WP_REHAFTED`, an **axe** - Hob's class
  takes axes and nobody else's does, so it is his without a published class
  being edited. It can be turned down. The sword is found carried **or
  equipped** (Bram wields swords), by script with `includeEquip`, since
  `rmmzdata` has no weapon condition - worth adding if a later step needs one
  twice. Stats sit under Beatrice II and Number One (ATK 66, Light), so HOB-2's
  weapon is still his best (0.5).
* **Ids taken:** switches **118** `SW_ROL4_SEEN` and **119** `SW_ROL4_REFIT`;
  weapon **40**. Weapons.json is padded 34-39 with blank records (34 is
  Spare's). Next free: switch 120, weapon 41.
* **`SW_STORY[ROLAND]`** goes on at the mark - it is filed as his quest -
  and not Hob's; G1 may want Hob's block to read `SW_ROL4_SEEN` as well.
* **No trope** (it is the one quest in the document with no cliché) **and no
  blush.** Running tally unchanged: tropes +3 fixed and 2-9 from PIP-2;
  blushes +4 fixed and 0-1 from PIP-2.
* **Candidate ending line** (G1; read `SW_ROL4_REFIT`): Roland said the sword
  had never been in a last room. "It went into one after all, on a
  Thistlewick haft, in a Thistlewick hand."
* **The smithy was redrawn after this step**, at Mike's word that wrong tiles
  in the early maps are to be fixed on sight: the "anvil" was `Table A
  (Ruins)` under `Scrolls A`. It is a real anvil now, at **(10,5)** beside
  Hob, with the forge on the wall behind it, and Beatrice's event moved onto
  it; `q_rol4` stands at (10,6). Nothing she says changed. The same sweep
  fixed the other Thistlewick and Nether Sopping interiors - see the commit
  and mapkit's "Inside furniture, by name".
* `TIMELINE.md`: 1960, Beatrice Grumnir makes the sword and sells it south.

**A6, HOB-5 Two Smiths, One Forge - done.** `build/q_hob.py`, hooked from
`north.py` in three places; `build/scenarios/q_hob5.json`. What is worth
carrying forward:

* **The ask is Bryd's** - Map 24 event 2, pages 5-7, below his ladder. His
  terminal is `SW_SPAR_DONE`, and `SW_HOB_BRYD` is only ever set beside it,
  so a page on the drink is a page on the terminal. The job **also needs
  `SW_OTT_MATERIALS`**: it is the Two Hundred's refit, so she has flown, and
  a plate carried to a woman half-way through her flying chain would be
  heard by the chain. Page 5 (Hob + both) is the forging; page 6
  (`SW_HOB5_FORGED`) Bryd waiting for it to go up the hill; page 7
  (`SW_HOB5_DONE`) the telling, with Hob once (Bryd's self switch D) and
  "Aye." / "Aye." after, and "She would." without him.
* **Only the forging needs Hob.** The plate is an item and the state is two
  globals; the scenario dismisses him with the plate in the bag and carries
  it up without him.
* **Ott's approval is her 28th page**, Map 22 event 2, below everything, on
  self switch D, `SW_OTT_MATERIALS` and the plate. It shadows her field pages
  only while the plate is carried, and spends it. "That will do. They will
  know what I mean by it" - Bryd's "we shall see", going the other way.
* **Nobody finishes a sentence** ("If you take the -" / "I've got the -"),
  and the telling has no line from either of them at all; the scenario
  asserts no Hob or Bryd window in it. **Grommet** says "They do this every
  time" to you, holding the candle, and is not removed; his own new page
  (event 4, page 4, `SW_HOB5_FORGED` + his A) is "He said it quick, an' all",
  against "He says it slowly".
* **Ids taken:** switches **120** `SW_HOB5_FORGED`, **121** `SW_HOB5_DONE`;
  item **44** `IT_TUBE_PLATE`. Next free: switch 122, variable 17, item 45,
  weapon 41, common event 4.
* **No trope** (the quest has no cliche, like ROL-4). **No blush** since
  October 2026 (NORTH.md 1.6): Ott tries each of the forty-one holes with a
  gauge pin - "True. Every one." Running tally for the effort: **tropes +3 fixed and 2-9 from
  PIP-2; blushes +5 fixed and 0-1 from PIP-2.**
* `SW_STORY[HOB]` goes on at Ott's approval - his first.
* **Candidate ending line** (G1; read `SW_HOB5_DONE`): "The Two Hundred's
  tube plate was made at Ollerenshaw's in one heat, by four hands. Neither
  of them has mentioned it since. Ott Hoyle says it will do."
* **The rooms were fixed (0.1).** Ollerenshaw's was a forge with SF Inside's
  carved `Fireplace` for a hearth, a brass console for an anvil, a valve lying
  on the floor and a 2x2 heap of fallen masonry by the door. SF Inside has no
  anvil, hearth or coal, so **tileset 6 now carries the stock `Inside_B` and
  `Inside_C` in its empty D and E slots**, with tileset 3's flags for them
  (`build_game.build_tilesets`); `mapkit.borrowed(sheet, name)` (was `clanging_in`) names a
  tile there - **not** `sf_tile`, whose id would be tileset 3's. The forge
  has Grumnir's brick hearth, a quench basin, a coal box (`Inside_C`'s
  `Scrap Metal` is coal - `TILES-AND-ASSETS.md`), an anvil and hammers at
  `north.FORGE_ANVIL` (6,6), and Bryd faces it; the drop hammer moved to
  (10,6). The Works' two floor valves went onto its pipe junctions. No event
  moved and no line changed. Every scenario that walks Maps 22 or 24 was
  rerun and passes: `clanging_cast`, `clanging_faces`, `hob_and_bryd`,
  `item_one`, `long_field`, `two_hundred` and `reachable_clanging`.
* `TIMELINE.md`: nothing dated.

**A7, ZEPH-5 The Lay-By and MER-4 The Man Who Cannot Stay Down - done.**
`build/q_zephyrine.py` (new), hooked from `nomap.py` in one wrapper, and a
MER-4 section at the bottom of `q_merribell.py`, hooked from `frayne.py` in
five lines; one scenario for both, `build/scenarios/q_zeph5_mer4.json`. What
is worth carrying forward:

* **ZEPH-5 hangs off the Lay-By's world-map event** (Map 8, (11,88)), pages 3
  and 4. Its two pages are a stop and a short version on self switch A, so
  page 3 needs **A and Zephyrine** - she gets the association's first scene
  first, as anybody does - and page 4 adds `SW_ZEPH5_DONE`. Both ask "Look
  in / Press on" first, the world map's idiom.
* **The skill is skill 46, `SK_PAGE_23`, "Page Twenty-Three"**: Kindle as
  Dunnock worked it out with the page missing - you don't aim it, you mean
  it at everything. Fire, `a.mat * 3 - b.mdf * 2`, three random enemies,
  5 MP (Kindle is one enemy, `* 4`, 6 MP). Taught with a gorse bush, a
  milestone and the litter bin, all at once, nobody near any of them.
  `rmmzdata.learn_skill(actor, skill)` is new (Change Skill, code 318).
* **MER-4 is Tobias's pages 3-5** (Map 43, event 2) and one page each on the
  door, ladder, book and jar, all in their own page's dress. Page 3 (his A +
  Merribell) is the refusal: nothing wrong with him, which is the trouble;
  no twelfth time; the parish to tea, through the door, on purpose; and the
  jar, which says FOR WHOEVER IS GOING THAT WAY, paid out: **1,100 crowns**,
  a hundred for each of the eleven (`q_merribell.JAR_PAYOUT`).
  `SW_MER4_TOLD`.
* **The cure is leaving.** The exit tile's page 2 (on `SW_MER4_TOLD`) sets
  `SW_MER4_DONE` and her story the first time the party walks out, then
  transfers exactly as page 1 does. A Merribell dismissed in between cannot
  happen - the roster desk is not in the cottage.
* **Afterwards is for everybody**: Tobias has had the parish to tea, twice,
  and nobody fell off anything; he mended the rung himself, badly, and it
  holds; the jar is empty; and **the twelfth line is left empty**, the pen
  capped and put in the drawer.
* **Ids taken:** switches **122** `SW_ZEPH5_DONE`, **123** `SW_MER4_TOLD`,
  **124** `SW_MER4_DONE`; skill **46**. Next free: switch 125, variable 17,
  item 45, weapon 41, common event 4, Zephyrine's skills 47-49.
* **Tropes: two** - ZEPH-5's is the eccentric master's secret technique (the
  site already counted the secret order itself), MER-4's the healer as a
  vending machine. **Blushes: one**, the coccyx, set twice by a paladin,
  beautifully; Bram looks at the ceiling, which has a hatch in it. Running
  tally for the effort: **tropes +5 fixed and 2-9 from PIP-2; blushes +6
  fixed and 0-1 from PIP-2.**
* `SW_STORY[ZEPH]` and `SW_STORY[MERRI]` - Merribell's was already on from
  MER-2, so VAR_COMPANION_STORIES counts only Zephyrine's here in a game that
  did MER-2 first. The scenario runs MER-4 on a fresh file, so it counts.
* **Candidate ending lines** (G1): read `SW_ZEPH5_DONE` - "The association
  of hedge mages has four members and no name. Item one is carried
  forward."; read `SW_MER4_DONE` - "Tobias Frayne has not died since. He has
  the parish to tea."
* **The rooms (0.1):** Tobias's cottage was cropped and screenshotted and is
  what it says - the ladder, the jar (`Pot B`), the book, the stove - so
  nothing was changed. The Lay-By is a world-map cell with its igloo stamp
  on it (`B1,1` on layer 3), deliberate by `WORLDMAP.md` 4; the party
  stands on it and hides it in the scene's shot, which is not a fault.
  `frayne` and `nomap`, which walk these events, were rerun and pass.
* `TIMELINE.md`: nothing dated.

**A8, HOB-3 The Anvil - done.** HOB-3's section at the bottom of
`build/q_hob.py`, hooked from `village.py` in four places;
`build/scenarios/q_hob3.json`. What is worth carrying forward:

* **The smithy's anvil is an event now** - Map 6 event 5, **The Anvil**, on
  `village.SMITHY_ANVIL` (10,5) with Beatrice's event on the same cell, as
  she always was (invisible, blocking it). The tile came out of layer 2.
  Page 1 is the anvil (a tile image, below characters); page 2 is **the
  theft, an autorun**, on Hob in the party and `SW_LEFT_VILLAGE` - the
  first time he walks into his own smithy after the road; page 3
  (`SW_HOB3_GONE`) is nothing; page 4 (`SW_HOB3_DONE`) is the anvil back.
  Nine seconds of incandescence, "mostly about the horn", then "They'll not
  have got far." **One trope** (the stolen sacred object), there.
* **`SW_HOB3_GONE` goes off again when the anvil comes back**, so one
  switch means "it is outside" and every page that shows the theft reads it
  alone. It is the pattern for a quest state that has to *end*, since a
  page condition has no NOT.
* **Beatrice's page 4** (`SW_HOB3_GONE`): on the floor where the anvil was,
  saying nothing, pointedly. It shadows her ROL-4 pages while the anvil is
  out, which is right - Roland lays the sword across the anvil - so **a
  party with Roland and Hob that comes home after the road gets the theft
  first, and ROL-4 after the rescue.** `q_rol4` does not set the road
  switch and still passes.
* **Outside, Map 1 events 26-28**, at `village.ANVIL_OUTSIDE` (9,33), three
  squares south-east of the door: the anvil, face down on the grass, with
  **Ivy Scrope** (8,33) and **Hodge Arkwright** (10,33) flat on either side
  of it - a head at each end, which is what the text says. Each has one
  page, on `SW_HOB3_GONE`, so before and after the grass is empty and the
  cells block nothing. The anvil needs Hob; without him, "Is he coming? The
  smith? Only we can't lift it."
* **The two apprentices are generated**: `Gen_People11` **3** (Ivy, the
  sorry one, in a striped top) and **4** (Hodge, in the syllabus bandana, as
  Norbert is), settings in `build/characters/`, installed by `art.py`.
  Their sprites are only ever the knocked-down strip,
  `Gen_People11_Damage`, pattern 2. `Gen_People11` 5-7 are free. They have
  no battlers in use, so nothing goes on `AUDIT.md`'s list.
* **Crooke's line branches on her bounty** (`SW_BOUNTY_CROOKE`): she runs
  the course either way, so a party that beat her gets "You. The footwork."
  and one that did not gets her introduction. Either way: week four, module
  seven, acquisition of a heavy object - fail, both of you; "It says so on
  the side. Reading was week one." The scenario takes both branches.
* **The apology is item 45**, `IT_APOLOGY`, on the back of a syllabus, in a
  very good hand. Hob: "...Nice hand, that." Crooke: "Week one. It's all
  week one."
* **Outside's tileset (2, and the Collegium's copy, 7) now carries
  `Inside_C` in its E slot**, as SF Inside does since A6 - the first anvil
  drawn on the grass came out as a white square, because tile 404 on
  Outside is something else. `mapkit.clanging_in` is renamed
  **`mapkit.borrowed`**, since an `Inside_C` tile now has the same E id on
  every tileset that borrows it. The borrow runs before the copies in
  `build_tilesets`, so the build is byte-stable from the first run.
* **Ids taken:** switches **125** `SW_HOB3_GONE`, **126** `SW_HOB3_DONE`;
  item **45**. Next free: switch 127, variable 17, item 46, weapon 41,
  common event 4, `Gen_People11` 5.
* **One trope, no blush.** Running tally for the effort: **tropes +6 fixed
  and 2-9 from PIP-2; blushes +6 fixed and 0-1 from PIP-2.**
* `SW_STORY[HOB]` at the rescue (already on after HOB-5 in a game that did
  that first).
* **Candidate ending line** (G1; read `SW_HOB3_DONE`): "Two apprentices
  failed module seven, acquisition of a heavy object, by eleven feet. The
  apology is framed in the smithy, next to nothing Hob made."
* **The rooms (0.1):** the smithy was swept on 30 Sep and still reads right;
  the grass outside the door is open ground. `q_rol4`, the only other
  scenario that enters Map 6, was rerun and passes; nothing else walks the
  new cells, which have no page until the theft.
* `TIMELINE.md`: nothing dated.

**A9-A14 were built in one session (30 Sep 2026) and share one commit**,
against 0.1. Each step after A9 was written while the steps before it were
still in their scenarios, so the six are interleaved through `db.py`,
`build_game.py`, `story.py`, `art.py`, `village.py`, `journey.py`, Maps 1,
10 and 14 and the database files; splitting the hunks by hand risked a
commit that does not build. Each step is complete and has its own scenario,
and the paragraphs below are per step as usual.

**A9, NIX-4 The Longest Loan - done.** `build/q_nix.py` (new), hooked from
`village.py` (five), `south.py` (four) and `north.py` (three), one line round
each owner's event; `build/scenarios/q_nix4.json`. What is worth carrying
forward:

* **It starts at the Emporium's ledger** (Map 7, event 4), pages 2-5, with
  Nix and `SW_NORTH` - so every owner she names is somebody already met.
  Page 2 is the ask: eleven of **one item**, `IT_RETURNS` "Previously Owned
  Goods", so the count in the bag is what is left; page 3 is the tally
  (`\V[17]` of eleven); page 4 (`VAR_NIX4_RETURNED` 11) rules the book off
  and opens a new page on the parcel; page 5 (`SW_NIX4_DONE`) is the closed
  book, for everybody. One trope (the fetch chain), at the ask.
* **The eleven, and the ladder rule.** `q_nix.returned(key, ev)` appends two
  pages to an owner's event: the return, on `IT_RETURNS` + Nix + whatever
  the owner's own last page needs (self switch A, for the seven with a short
  version), and afterwards on self switch B - **their own last page with one
  narrated line added**, so nobody loses a word. It asserts the owner's last
  page needs nothing but A and that nothing of theirs uses B. Thistlewick:
  Bram's mother (pie dish; the pie was a separate matter), the Old Man (a
  chair: he can wait sat down), the Fisher (a keep net, for a pond with no
  fish), the Gatekeeper (the key to a gate that has never been shut). Nether
  Sopping: the Ferryman (a tide table; **pays**, a penny), Councillor Dree
  (spectacles: his eyes are entirely ordinary now, and he will miss being
  suspected), Tolly (a sheet of forty stamps, the old rate), **Hulda Bole**
  (her good boots - and she gives Nix the last job's parcel, `IT_PARCEL`,
  client not identified: **the something better**). Upper Clanging: Old
  Sowerby (his snap tin, a sandwich eleven years old; **pays**, a rivet, and
  Nix does not take it), Nib (the small can - there were always two), Bessie
  Marsden (her gran's cradle, ahead of schedule: **one blush**). The Elder,
  Mr Kell and Mrs Tunnicliffe were passed over because their last pages do
  something (the guild reference, a room, the census) that a page on top
  would shadow.
* **A ladder's set piece runs first**: an owner never spoken to gives their
  own scene, then the return. The scenario shows it on Tolly.
* **Ids taken:** switches **127** `SW_NIX4_BEGUN`, **128** `SW_NIX4_DONE`;
  variable **17** `VAR_NIX4_RETURNED`; items **46** `IT_RETURNS`, **47**
  `IT_PARCEL`.
* Tropes +1, blushes +1. Running tally for the effort: **tropes +7 fixed and
  2-9 from PIP-2; blushes +7 fixed and 0-1 from PIP-2.**
* `SW_STORY[NIX]` at the ruling-off. **The parcel is on the Emporium's
  shelf, unopened**, a line in the new page - NIX-1 (B5) may want it.
* **Candidate ending line** (G1; read `SW_NIX4_DONE`): "Nix's ledger has a
  RETURNED column now, with eleven lines in it. Over the page there is a
  parcel, for a client not yet identified."
* **The rooms (0.1):** the Emporium was swept on 30 Sep and reads right (the
  toy shelf is stock, there). Upper Clanging, never swept, was cropped: its
  "dumpsters" are plain lidded bins and its two posters printed bills, both
  right for a works town, so nothing was changed. The two inns' toy shelves
  were fixed in A11, below.
* **Scenario** `q_nix4`: the whole round, about 25 minutes; passes. It
  clears Clanging's rain after its last `goto`, which teleports past the
  South Road that clears it in play.
* `TIMELINE.md`: 1989, Nix starts the ledger at fifteen.

**A10, NIX-5 Half An Encounter - done.** NIX-5's section of `q_nix.py`,
hooked from `journey.py` in five places; `build/scenarios/q_nix5.json`.

* **Enoch Bagshawe**, first bassoon engaged by the Upper Clanging Works Band
  (a brass band; they asked), with one reed that took three weeks and goes
  the moment anything looks at him. He is on the milestone at the
  **Gloamwood's mouth** - the world map's event 2 gets a page on
  `SW_GLOAMWOOD` + Nix whose tail is the mouth's own "Go in / Think about
  it", so saying "not tonight" loses nothing. The first telling sets the
  mouth's self switch A and later nights are the short version, so the
  **one blush** ("eight feet of tube, folded; nobody has ever complained")
  counts once. Nix: "I halve them. What's half an encounter? Still an
  encounter."
* **A fight is detected without touching a troop**: `battleCount()` into
  `VAR_NIX5_BATTLES` at the mouth; a new parallel event on each wood map,
  **Mr Bagshawe's Reed** (Map 9 event 9, Map 10 event 7), fails it the
  moment the count moves - running away counts - and the north exit (Map 10
  event 2, page 3) checks again, as A10 says. Walking out of the south end
  (Map 9 event 1, page 2) abandons it. Either way he goes home and is on
  the milestone another night.
* **Night** is a tint (`q_nix.NIGHT`) instead of the wood's gloom for as
  long as `SW_NIX5_ON` is; a failure puts the gloom back.
* **Through**: the moon on the road, one low note (`Horn` at pitch 50), the
  fee, 300, and a receipt. **One trope** (the stealth section).
* **Ids taken:** switches **129** `SW_NIX5_ON` (ends), **130**
  `SW_NIX5_DONE`; variable **18** `VAR_NIX5_BATTLES`; face `Gen_People11`
  **5**, Bagshawe.
* Running tally: **tropes +8 fixed and 2-9; blushes +8 fixed and 0-1.**
* **Candidate ending line** (G1; read `SW_NIX5_DONE`): "Enoch Bagshawe
  crossed the Gloamwood by night without a single encounter, or half of
  one. The Works Band has a bassoon."
* **The rooms (0.1):** the Gloamwood was cropped, and **`mapkit.ROCK` and
  `ROCK2` were `Rock Fire Pit A` and `B`** - campfire rings standing in the
  wood's undergrowth, on Thistlewick's verges, on Nether Sopping's shore and
  in Firstfield. They are `Boulder A` and `B` now, with the same flags
  (0x60f), so nothing anybody walks changed; screenshots before and after.
* **Scenario** `q_nix5`, encounters left on: three nights - abandoned at
  the south end, failed by a forced battle (the parallel event fires as
  the battle ends), and through to the north exit. Passes.
* `TIMELINE.md`: nothing dated.

**A11, WRE-3 The Thing In The Gloamwood - done.** WRE-3's section of
`q_wren.py`, hooked from `village.py` and `journey.py`;
`build/scenarios/q_wre3.json`.

* **The answer was already in the game**: the nest on the first path ("that
  is why there are nine of them"), the shed skin ("everything we have
  killed this week was in the middle of courting"), and a Thing "difficult
  to say how much of it there is". It was never one thing: nine crested
  grass snakes, knotted, in season, seen at dusk. "It's nine of them.
  Courting." / "...Forty years. With lanterns. We've been chaperoning snakes." / "Very
  conscientiously. Nobody got up to anything."
  **One blush.**
* **The Gloamwood Society** - nine members, The Sighting four times a year
  since 1960, a walk once a year - meets in the **Gilded Turnip** (Map 4,
  events 8-10, at a new table at (12,11)): Mrs Lumb the chair, Mr Dunmore
  the secretary, Miss Pellow who saw it in 1971. They are there for
  everybody; once the Thing is dealt with Mrs Lumb's first page adds the
  game's own "you are not going to tell them anyway". Wren's ask is her page
  2 (`SW_GLOAMWOOD` + Wren). **One trope** (the cryptid).
* **The walk** (`SW_WRE3_WALK`, ends): the three leave the inn and all nine
  stand round the deep clearing (Map 10, events 8-16; six extras on stock
  sprites, no lines). The proof is Mrs Lumb's page there with Wren; without
  her they wait. **Miss Pellow is looked after** by everybody without
  anybody arranging it, and is fine by the edge of the wood: hers, issue
  forty-four, is the only accurate sighting in forty years - she counted
  nine.
* **Wren's gear is decided: the badge** (0.5), armour **40** "Gloamwood
  Society Badge", an accessory of a new armour type **7, "Badge"**, which no
  class can wear and **Wren's actor** has a trait for - on the actor, not
  the Cataloguer class, so no published class changed. That is the pattern
  for any later accessory that must be one companion's alone. LUK +12, AGI
  +4, hit +5%.
* **Ids taken:** switches **131** `SW_WRE3_WALK` (ends), **132**
  `SW_WRE3_DONE`; armour **40**, armour type **7**; faces `Gen_People11`
  **6** (Lumb), **7** (Dunmore) and `Gen_People12` **0** (Pellow) - the
  first cell of the new sheet.
* Running tally: **tropes +9 fixed and 2-9; blushes +9 fixed and 0-1.**
* **Candidate ending line** (G1; read `SW_WRE3_DONE`): "The Gloamwood
  Society has proved there is nothing in the Gloamwood. Next year's walk is
  expected to be very well attended."
* **The rooms (0.1):** both inns had `IN_SHELF_FRUIT` behind the bar, which
  is `Sundries Shelf A` - **two teddy bears and a pink rabbit**. The Turnip's
  is a bottle shelf now and the Wyvern's a jar shelf, same flags; the
  Emporium keeps its toys, and the constant has a comment. (`IN_CABINET`
  was tried for the Wyvern and refused: its lower cell is a star tile and
  would have opened a cell of the bar.) The clearing needed nothing.
* **Scenario** `q_wre3`; passes.
* `TIMELINE.md`: 1960 the society; 1971 Miss Pellow counts nine.

**A12, PIP-5 The Struck Verses - done.** PIP-5's section of `q_piper.py`,
hooked from `village.py`; `build/scenarios/q_pip5.json`.

* **Map 3 had no room**: the hall fills x 3-17 and its margins are two
  tiles. So **Map 3 is 31 wide now** and the archive is a room in its black
  east (x 23-27, y 5-8), `village.archive_room`; the hall is tile for tile
  what it was in its old 21 columns (checked). The way in is the curtained
  window on the north wall (`Middle Window B`, (16,4)): drawn back, there
  is no window, there is a door marked STRUCK (event 9). Out is the
  archive's doorway (event 11).
* **A form, a key and a distraction.** The ask is the fete minutes' page 3
  (Map 3 event 8, below its terminal A, with Piper): **one trope** (the
  redacted archive). Form S-7 is in the Committee Records (event 7, which
  are the records again afterwards, on its B); the Councillor on the wording
  countersigns it (event 4: "'consult' or 'inspect'?"). And **Councillor
  Fenn** (event 5) - "Nobody is listening to him. Remember him." - is
  listened to, by whoever is third in the party (`VAR_PIP5_DECOY`, named by
  `\N[\V[19]]`), and the key comes off his hook. Bram and Piper alone
  cannot: "It wants a third."
* **The box** (event 10, `Case A`, the Committee's best box): never
  printed. The tally card in the lid is **`VAR_BLUSHES` read back**, Piper
  says the number and "...That's about right", and one slip is shown:
  verse forty-one, about a hedge, entirely innocent, struck anyway. "It
  scans." **One blush.** The key goes back on Fenn's hook on the way out.
* Only the ask and the box need Piper; the Clerk who can strike her off is
  in the same room, and the scenario does that with the key in hand.
* **Ids taken:** switches **133** `SW_PIP5_ASKED`, **134**
  `SW_PIP5_SIGNED`, **135** `SW_PIP5_KEY`, **136** `SW_PIP5_DONE`; variable
  **19** `VAR_PIP5_DECOY`; items **48** Form S-7, **49** the key.
* Running tally: **tropes +10 fixed and 2-9; blushes +10 fixed and 0-1.**
  `COMPANIONS.md` says this quest "requires the threshold in `journey.py`
  to be recut" - **not done here**, by 0.2; G1 re-cuts once.
* **Candidate ending line** (G1; read `SW_PIP5_DONE`): "The Committee's box
  of struck verses holds \V[7]. Piper Quill has read every one of them,
  and printed none."
* **The rooms (0.1):** Prophecy Hall cropped; it reads right. The archive
  is new.
* **Scenario** `q_pip5`; passes.
* `TIMELINE.md`: nothing dated.

**A13, HOB-2 The Grave He Has Not Made - done.** HOB-2's section of
`q_hob.py`, hooked from `village.py`; `build/scenarios/q_hob2.json`.

* **The churchyard is on Map 1** - the call A13 asked to be argued. The
  argument: `NORTH.md` 1.7's never-list is lines, faces, deleting events and
  renumbering, and new tiles on empty grass move nothing and silence nobody
  (A2 and A8 already drew on Map 1); a churchyard is outdoors beside its
  chapel, where "behind the chapel" on Map 5 would be a graveyard inside a
  building map; and `COMPANIONS.md` already treats the headstone as being
  in Thistlewick churchyard, so this fills a gap rather than changing
  anything. It is the empty strip east of the chapel, `village.CHURCHYARD`
  (33,2)-(37,9): a low wall of `Fencepost C (Stone)` (Fenmarch's), four
  parish graves, and **Beatrice Grumnir's**, event 29 at (35,4) - "BEATRICE
  GRUMNIR. SMITH. 1919 - 1989", the grass cut every week by nobody who says
  who. There for everybody from the start, like the gate that sticks
  (event 30, `!Door2` 2, pattern 2: you lift it, every time).
* **Beatrice goes quiet** the first time Hob walks into the smithy after the
  anvil is back (`SW_HOB3_DONE`): a new event on the forge, **The Forge**,
  Map 6 event 6 at (11,3), page 2 (autorun). Hob is very large at being at
  a loss, and admits the marker. **One trope** (the smith's masterwork).
  `SW_HOB2_ON` (ends).
* **Four attempts**, each made at the forge (page 3) and carried to the
  grave (event 29, page 2): a wrought-iron headstone with roses ("No."), an
  eight-foot steel cross ("She'd say it was showing off."), a small perfect
  plate ("It's right. It's not her." - and the gate sticks on the way
  out); and the fourth is **a gate**, hung as you walk through with it
  (event 30, page 2). "She says the latch wants a spring." **Nobody says
  she is the hammer**; the scenario asserts that no line says "hammer is",
  "a hammer" made of the markers, and that nobody says "aunt".
* **Hob's gear, and his best weapon** (0.5): weapon **41** "Something To
  Say", a flail made of the three markers he would not put up, made badly
  on purpose so she would have something to say: ATK 78 (Number One is
  68), AGI -6, crit +15%. An **axe**, as Beatrice II is - flails are
  Bram's and Merribell's too, and axes are Hob's alone.
* **Afterwards**: the new gate (`!Door2` 3) clicks as you go through, and
  the forge has a latch chalked beside it with "TOO HEAVY" under it in
  another hand. **HOB-4 (E-part) requires `SW_HOB2_DONE`**, as
  `COMPANIONS.md` says - Hob is good at gates now.
* **Ids taken:** switches **137** `SW_HOB2_ON` (ends), **138**
  `SW_HOB2_CARRYING` (ends), **139** `SW_HOB2_DONE`; variable **20**
  `VAR_HOB2_TRY`; weapon **41**. No faces.
* No blush. Running tally: **tropes +11 fixed and 2-9 from PIP-2; blushes
  +10 fixed and 0-1 from PIP-2.**
* **Candidate ending line** (G1; read `SW_HOB2_DONE`): "Thistlewick
  churchyard has a new gate, with a good latch. Somebody says the latch
  wants a spring."
* **The rooms (0.1):** the smithy was swept on 30 Sep and reads right; the
  churchyard is new.
* **Scenario** `q_hob2`: passes.
* `TIMELINE.md`: 1919 and 1989, Beatrice Grumnir.

**A14, ROL-3 The Alumni - done.** ROL-3's section of `q_roland.py`, hooked
from `south.py` in two places; `build/scenarios/q_rol3.json`.

* **None of the eleven parties is an existing NPC, and none can be.** The
  game's Roland has been at this "since I was eleven" and is thirty-four,
  so his first party is 1977 - after the Forty-Fourth (1960) and the
  Forty-Sixth (1980) that `QUESTS.md` had guessed at. The Wyvern's
  regulars keep their ladders untouched.
* **The card is on Dorcas's Board** (Map 14 event 19, page 3, below its
  terminal A, with Roland): THE FAIRWEATHER ALUMNI, from F. Ickworth (Dame),
  who was first. "...Oh, how lovely. Oh no." **One trope** (the party
  reunion). `SW_ROL3_DINNER` (ends) puts **eleven guests** about the room
  at capacity, events 22-32, each with their party and their line, each
  counted once into `VAR_ROL3_HEARD` on their own A: Dame Florence (the
  Wyrm of Ickworth - he was her page, at eleven), Brother Anselm (the Seven
  Bells), Mags Turvey (the Second Siege of Wenlow), Pim (the Lost Heir of
  Corrow, found), Captain Odile Marchbank (the Ninth Lancers), Old Jory (the
  Last Survey), Hettie Brack (the Goblin King's Riddles - the last answer
  was "a door"), Lord Tobin (the Usurper of Hask), Ned Scarrow (the Drowned
  Bell), Saul Pennock (Pennock's Cove), Major Royce (the Glass Fort). Every
  one says "our Roland", and notices the others.
* **The toast** is Dame Florence's (page 3: dinner, all eleven heard,
  Roland): "To Roland Fairweather. Who got us all to the door." Nobody
  says anything else. Then **the small gifts**: eleven consumables
  (`q_roland.ROL3_GIFTS`) and their real names in a line - a whetstone, a
  twist of tea, a pot of dripping, a map with one mile in pencil.
  `SW_STORY[ROLAND]`. The board afterwards, for everybody: the card, signed
  eleven times, with a ring from a glass.
* **Before the tower door**, necessarily: the card needs Roland.
* **Ids taken:** switches **140** `SW_ROL3_DINNER` (ends), **141**
  `SW_ROL3_DONE`; variable **21** `VAR_ROL3_HEARD`; faces `Gen_People12`
  **1-6** (Florence, Anselm, Mags, Pim, Odile, Jory); five one-liners share
  stock faces nobody in the Wyvern wears.
* No blush. Running tally at the end of Part A: **tropes +12 fixed and 2-9
  from PIP-2; blushes +10 fixed and 0-1 from PIP-2.** Next free: switch
  142, variable 22, item 50, weapon 42, armour 41, common event 4,
  `Gen_People12` 7 (then `Gen_People13`).
* **Candidate ending line** (G1; read `SW_ROL3_DONE`): "Eleven parties
  finished their quests without Roland Fairweather. They drank to him
  anyway: to the man who got them all to the door."
* **The rooms (0.1):** the Slain Wyvern's bar had the teddy-bear shelf too
  (A11, above); fixed. Two guests were moved off the bottom row when
  `validate.py` found nothing beside them could be reached.
* **Scenario** `q_rol3`: passes.
* `TIMELINE.md`: 1977, Roland's first party.

**Rerun for the rooms changed in A9-A14** (0.1): every scenario that walks
Maps 3 or 4 - `village`, `reachable_village`, `guild`, `q_pip2`, `feud`,
`wall_ring`, `blushes`. The rock and shelf swaps kept their flags, so no
walk anywhere else changed.

**B1, HOB-1 The Assize of Hammers - done.** HOB-1's section at the bottom of
`q_hob.py`, hooked from `dunnage.py` (four), `village.py` (two) and one line
each in `south.py`, `hithermost.py`, `frostwick.py`, `fairholme.py`,
`ashcombe.py` and `hamlets.py`; `build/scenarios/q_hob1.json`.

* **The ask is the Prime Warden's** (Map 62 event 2, pages 3-5, below her
  one-self-switch ladder, with Hob): clauses one and two, "There's a shelf",
  and the eleven counted on his fingers and then on yours. **One trope**
  (the tournament arc). Page 4 is the tally on `SW_HOB1_ON`, page 5 the
  submission on `VAR_HOB1_ASKED` 11, and page 6 is her own last page plus
  "a second card is pinned up" on `SW_HOB1_DONE`, for everybody.
* **The ten** take `q_nix.returned`'s pattern as `q_hob.owned(key, ev)`: the
  ask on the owner's own last-page conditions plus Hob plus `SW_HOB1_ON`, and
  afterwards on their self switch B - their own last page plus one line. It
  asserts the same two things. Nobody gives anything back, and each has a
  reason: **the Farmer** (the share - the weevils don't like it), **the
  Gossip** (the goat's bell - he abstained from a brass one), **the Man
  Having A Day Off** in Nether Sopping (the sword on his knees - it is having
  a day off), **Hithermost's villager** (the holly trivet under the
  teapot - they do teas), **Perce Stagg** (the crown on the ribbon post - a
  ribbon slides down a bare post), **King Aldous** (Rosamund's tower hinges -
  fourteen doors, and the hinges are fine), **Mrs Dimmock** (the post box,
  which has had a letter from the Ruins of Ashcombe in it), **Dame
  Winifred** ("I'm in it"), **Cotter** (his heel-irons - he'd not get home)
  and **Warden Crabbe** (the Company's tongs: a piece by clause forty, not
  Hob's property by clause two - "You would be disqualified by your own
  tongs"). The NIX-4 owners were avoided, since two quests' "afterwards"
  pages on one event would shadow each other.
* **Nix's lockpicks are asked at the Company's table**, since Nix is in the
  party and on no map: the ask and the tally pages both carry the exchange
  behind "Nix is here and `SW_HOB1_PICKS` is off". Nix's reason is the
  ledger: ACQUIRED from H. Grumnir, column GIVEN, and nothing comes out of
  GIVEN. With the other ten done and no Nix, the tally says "Just the picks
  to ask. Nix has them."
* **The submission**: Beatrice laid on the table "the way you would put down
  a sleeping cat"; clause thirty-nine, examined on receipt "so that nobody
  waits three years to be told"; Miss Fettle asks who made it ("Not me. I'd
  never have got the balance"); clause two satisfied, clause one not,
  **disqualified**, and Hob beams. The Company's mark is struck on the
  Wardens' notes, which are **item 50**: "Remarks: in the Wardens' opinion,
  right about everything." Nobody says what she is; the scenario asserts no
  line says "aunt", "hammer is" or "she made". **The Prize** (event 5) gets a
  second page on `SW_HOB1_DONE` with her card pinned beside the hinge.
* **Ids taken:** switches **142** `SW_HOB1_ON`, **143** `SW_HOB1_PICKS`,
  **144** `SW_HOB1_DONE`; variable **22** `VAR_HOB1_ASKED`; item **50**
  `IT_WARDENS_NOTES`. No faces.
* One trope, no blush. Running tally: **tropes +13 fixed and 2-9 from PIP-2;
  blushes +10 fixed and 0-1 from PIP-2.**
* **Candidate ending line** (G1; read `SW_HOB1_DONE`): "The Worshipful
  Company of Smiths disqualified a hammer called Beatrice under clause one.
  The Wardens' notes say she is right about everything."
* **The rooms (0.1):** Great Dunnage had never been swept. All five of its
  maps were cropped with `propsheet.py` (79 tiles) and screenshotted: the
  Smiths' Hall's two `Blacksmith's Table`s are the two anvils, the Bell's
  shelves are bottles and wine, the warehouse is crates and barrels, and the
  town's signs are what their shops are. Nothing needed fixing. The owners'
  own places (Hithermost, Fairholme, Frostwick, Little Gore, Ashcombe) were
  cropped too (110 tiles) and read right.
* **Scenario** `q_hob1`: passes (81 checks, about fifteen minutes).
* `TIMELINE.md`: nothing dated.

**B2, ALD-4 The Horse - done.** `build/q_aldric.py` (new), hooked from
`dunnage.py` in three places; `build/scenarios/q_ald4.json`.

* **The reunion is Mr Plummer's** (Map 61 event 14, page 3, below his
  one-self-switch ladder, with Aldric): he has already told the party about
  the grey and the crest on her saddle, and with Aldric standing there he
  looks at the tabard - a knight facing the wrong way - and brings the
  saddle out. "...That's my saddle." Nobody has asked Sir Aldric about his
  horse in six years, including Sir Aldric. Duchess lifts her head from the
  road (the `Horse` sound and a balloon on her event), puts her nose into
  his tabard, and he says "Hello, old girl" and that he could not find the
  gate. He only ever called her Horse; Duchess suits her. Plummer offers her
  back and stops, being tactful; **"She is doing so well,"** and he means it.
  He may visit, any day but a Tuesday. **One trope** (the loyal steed).
* **Duchess is wordless** - Mike has not drawn her a face (`QUESTS.md` 1), so
  the decision was made for the scene: a sound, two balloons and the
  narrator. **No reward at all**: the scenario asserts no item, no gold and
  no change to the party.
* **Her own pages** had Aldric pat a good horse in passing without knowing
  her, which would be wrong afterwards. The reunion sets her self switch A
  (her ladder's terminal) by script, and her new page (`SW_ALD4_DONE`, A,
  Aldric) is the two of them: he tells her about his week. **Afterwards for
  everybody**: Plummer's own last page plus "welcome any day but a Tuesday",
  and the yard sign's third line, in a third hand: (HER KNIGHT CALLS. NOT
  TUESDAYS.)
* **Ids taken:** switch **145** `SW_ALD4_DONE`. No faces, no items.
* One trope, no blush. Running tally: **tropes +14 fixed and 2-9 from PIP-2;
  blushes +10 fixed and 0-1 from PIP-2.**
* `SW_STORY[ALDRIC]` - his first.
* **Candidate ending line** (G1; read `SW_ALD4_DONE`): "Duchess, a grey mare,
  is a partner in Plummer & Partner, haulage, of Great Dunnage. Her knight
  calls on her. Not on Tuesdays."
* **The rooms (0.1):** the yard was cropped with the rest of Great Dunnage in
  B1. `Vehicle` 4 is the harness horse `TILES-AND-ASSETS.md` names, and reads
  as a grey at map scale. Nothing changed.
* **Scenario** `q_ald4`: passes.
* `TIMELINE.md`: 1994, the horse walks into Plummer's yard that winter.

**B3, PIP-3 The Contest at the Sign of the Bell - done.** PIP-3's section at
the bottom of `q_piper.py`, hooked from `dunnage.py`'s Bell (five places);
the fight in `db.build_contest`; `build/scenarios/q_pip3.json`.

* **The entry is Mrs Harbottle's** (Map 65 event 3, page 3, below her
  one-self-switch ladder, with Piper): Ballad (Not Sad), the category she
  wrote something about in the back of her book at the poster. "Nobody has
  ever entered Ballad (Not Sad)." / "Piper Quill is aware of that." The
  Contest is always tonight; they have simply not had the entries. **One
  trope** (the tournament, again). `SW_PIP3_ON` (ends) brings **Mr Septimus
  Dray** (Instrumental, Other Wind - the serpent; second place twice, of two
  entries) and **Miss Lettice Moon** (Ballad, Sad - fourteen verses, nobody
  survives) into the Bell, events 9 and 10, empty before and after.
* **The contest is her page 4** (Piper and the switch, "Begin / Not yet"):
  Dray 17, Moon 16, and Mr Tweddle's thrush that has lost its keys gets
  **Miss Quayle's first three** - nineteen. Then Piper's set, which is the
  fight: **troop 41**, Mr Dray (enemy 41), Miss Moon (42) and **the Back
  Table** (43, the stock `Sailor`), whose hit points are the room's patience,
  sized to the party as Norbert's are. The damage type is heckling - skills
  **170-174**: Heckle, Talks Through It (a MAT debuff), Serpent Solo (all),
  A Very Sad Verse (MP, all) and Encore (self-heal under half). Piper's own
  kit is already buffs and debuffs. It can be lost; she finishes anyway, "so
  loud that it is, technically, heard". Either way: 9, 2, 7 - eighteen.
  **Second place, by one point, and the point is Miss Quayle's.** "The
  birdcalls were, in fairness, extraordinary."
* **Piper's gear is the rosette** (0.5): armour **41** "Rosette, Second
  Place", an accessory of a new armour type **8, "Rosette"**, which Piper's
  actor has a trait for - Wren's badge pattern. MMP +20, MAT +8, MDF +4, LUK
  +6, MP regen 5%. She has the certificate framed before breakfast; Mrs
  Dewhirst lends her the nail.
* **Afterwards for everybody**: Mrs Harbottle's own last page plus SECOND,
  MISS P. QUILL, 18; Mr Tweddle in a red rosette he keeps being startled by;
  Miss Quayle, who gave the thrush a three and has not got over it; the
  poster's results.
* **Ids taken:** switches **146** `SW_PIP3_ON` (ends), **147**
  `SW_PIP3_DONE`; armour **41**, armour type **8**; enemies **41-43**; troop
  **41**; skills **170-174**; faces `Gen_People12` **7** (Dray) and
  `Gen_People13` **0** (Moon, the first cell of a new sheet), with
  `art.py`'s stand-in battlers `Septimus_Dray` and `Lettice_Moon` - both on
  `AUDIT.md` item 1's list for real art.
* One trope, no blush. Running tally: **tropes +15 fixed and 2-9 from PIP-2;
  blushes +10 fixed and 0-1 from PIP-2.**
* **Candidate ending line** (G1; read `SW_PIP3_DONE`): "Piper Quill came
  second at the Contest at the Sign of the Bell, by one point, to a thrush.
  The certificate is framed. It is the first prize a Quill has won for
  writing down what actually happened."
* **The rooms (0.1):** the Bell was cropped with Great Dunnage in B1 and
  reads right. Nothing changed.
* **Scenario** `q_pip3`: passes. It wins the fight by fiat (a death state on
  each act once the battle is up) - the lost branch is the same scores.
* `TIMELINE.md`: nothing dated.

**B4, COR-5 The Appraisal - done.** `build/q_corvin.py` (new), hooked from
`dunnage.py` in one place; the state in `db.build_states`;
`build/scenarios/q_cor5.json`.

* **It is Miss Fettle's** (Map 62 event 7, page 4, below her one-self-switch
  ladder, with Corvin). Both her own pages eye the black sword and are told
  "No."; this is the page where he lays it on her bench "the way a man lays
  down a confession" and says yes. She has the handle off in a trice - "Oh,
  the TANG. Somebody loved this, once." - and Corvin looks at the ceiling (**one blush**). **No curse**:
  a very good sword in very poor condition, he has been sitting in corners
  with it, and there is a name on the tang in letters nobody has used for a
  while, which she would not like to try aloud (COR-2 keeps the real name,
  off the doorstep). He asks what a curse would cost. They are mostly
  paperwork; there is a form, FORM C-1: APPLICATION FOR A CURSE (ELECTIVE).
  **One trope** (the cursed blade). `SW_COR5_DONE` and his story are set at
  the appraisal, whatever he chooses.
* **The curse is state 40, "Cursed (Elective)"** - LUK x0.5, target rate
  x1.5 (his 0.9 becomes 1.35), HP regen -3%: real, and bad for him, and he stands up straighter for
  it. **Optional**: thirty crowns, "Have it cursed / Not today", offered again
  every visit. **Removable**: she takes it off for nothing ("which Corvin
  finds a little disappointing"), and it is "the economy one: it lasts till
  you next sleep in a proper bed" - an inn's Recover All clears states, which
  is the engine's rule stated as hers. Out of battle it stays: no auto
  removal, not removed at battle end.
* **Afterwards for everybody**: her own last page plus a stamped C-1 and "a
  drawing of a tang, very lovingly done" pinned over the bench.
* **Ids taken:** switch **148** `SW_COR5_DONE`; state **40** `ST_CURSED`.
* One trope, one blush. Running tally: **tropes +16 fixed and 2-9 from
  PIP-2; blushes +11 fixed and 0-1 from PIP-2.**
* `SW_STORY[CORVIN]` - his first.
* **Candidate ending line** (G1; read `SW_COR5_DONE`): "There is no curse on
  Corvin Ash's sword. He has the form, if he wants one. It is not
  expensive."
* **The rooms (0.1):** the Smiths' Hall was cropped in B1; nothing changed.
* **Scenario** `q_cor5`: passes.
* `TIMELINE.md`: nothing dated.

**B5, NIX-1 The Client Identifies Themselves - done.** NIX-1's section at
the bottom of `q_nix.py`, hooked from `village.py` (the ledger) and
`dunnage.py` (the warehouse door, Mr Tibbs, the wardrobe and the Bond Book);
`build/scenarios/q_nix1.json`.

* **Decided: NIX-4's parcel is the letter's occasion**, so NIX-1 needs
  `SW_NIX4_DONE`, as HOB-4 needs HOB-2. Hulda Bole's tale (published, in the
  Slain Wyvern) has her last job end "he's moved"; it was also her **first**,
  JOB 1, accepted 1989, "to be delivered when the client is 26, to the
  address given" - and Nix had long since moved out to the Emporium. Hulda
  assumed a "he", and nothing corrects her. In NIX-4 she handed the parcel to
  its own addressee and said "You're the legs now".
* **The letter is the ledger's page 6** (Map 7 event 4, `SW_NIX4_DONE` and
  Nix): "That's my hand." NOT TO BE OPENED UNTIL I AM TWENTY-SIX. "Dear Nix.
  This is the client... You will have been avoiding it. Stop it. Yours, the
  party of the second part (N., aged fifteen)." "Ahead of schedule. Of me."
  **One trope** (the mysterious patron); item **51**, the Bond No. 1 ticket.
  Page 7 is the ledger afterwards, for everybody.
* **The warehouse door** (Map 61 event 7) keeps its two refusals; page 4
  (its A, Nix, the ticket) is "...Fine." and the door's own page; page 5
  (`SW_NIX1_DONE`) is the door's own page with Nix, no comment.
* **Mr Tibbs** (Map 64 event 2, page 4, below his ladder, with Nix and the
  ticket): "Ah. The party of the second part." The reason was embarrassment:
  a fifteen-year-old's speech from a crate - "I shall return for it when I am
  somebody", which he wrote in the margin - and eleven years of rent by post,
  never late, no name, sooner than come in and face him. "I did remember
  it." The coat was **Nix's gran's**, down to the ankles at fifteen, not to
  be worn till it fit and not to be sold. It fits. Nix writes the first
  entry's provenance at last. Rent paid to date; always was.
* **Nix's gear** (0.5): armour **42** "Gran's Coat", body armour of a new
  armour type **9, "Coat"**, which Nix's actor has a trait for - the badge
  pattern again. DEF +30, MDF +18, AGI +10, LUK +8, crit evasion +5%.
* **Afterwards**: Tibbs's own last page plus the rent that has stopped coming
  ("he misses it, a little, every quarter day"); the wardrobe, unlocked and
  empty, BOND No. 1. COLLECTED; the Bond Book's first entry, named now, the
  party of the second part.
* **Ids taken:** switches **149** `SW_NIX1_LETTER`, **150** `SW_NIX1_DONE`;
  item **51** `IT_BOND_TICKET`; armour **42** `AR_GRANS_COAT`, armour type
  **9** `AT_COAT`. No faces (the client is Nix).
* One trope, no blush. Running tally: **tropes +17 fixed and 2-9 from PIP-2;
  blushes +11 fixed and 0-1 from PIP-2.**
* `SW_STORY[NIX]` (already on after NIX-4 or NIX-5 in a game that did those).
* **Candidate ending line** (G1; read `SW_NIX1_DONE`): "The client has been
  identified. The first line of Nix's ledger has a provenance now, and the
  coat fits."
* **The rooms (0.1):** the warehouse was cropped with Great Dunnage in B1:
  crates, barrels, a closet for the wardrobe. Nothing changed.
* **Scenario** `q_nix1`: passes. It sets `SW_NIX4_DONE` rather than doing
  NIX-4, which `q_nix4` covers.
* `TIMELINE.md`: 1989, the coat into bond, the speech, and Hulda's job 1.

**B6, NIX-2 The Sealed Counting House - done.** NIX-2's section at the bottom
of `q_nix.py`, hooked from `dunnage.py`'s Counting House (four places); the
room drawn by `dunnage.vault_room`; `build/scenarios/q_nix2.json`.

* **The room behind the Door is in the black east, not the north** - the
  lobby fills Map 63 to two rows from the top, so the map was widened from
  18 to 30 columns, `village.archive_room`'s way, and the lobby is tile for
  tile what it was (checked). `places.VAULT` (23,5)-(25,7), gold walls like
  the lobby's, the doorway cut in the south wall, and **one chair**, `Chair A
  (Wood)`, a tall plain one, against the north wall. It was drawn 5x4 first
  and looked like an unfurnished room rather than a joke about one; 3x3 is
  the size of the punchline.
* **The opening is the Mayor's** (Map 63 event 2, page 3, below his ladder,
  with Nix): "Are you, by any chance, a licensed person?" / "I locate
  things. Doors are things." Form L is not completed, so he starts the
  preamble while it is, and Nix opens the Door with two fingers - the `Key`
  sound twice - in nine seconds. "- mindful of its ancient and -". "That was
  not the Opening." The Counting House is **opened informally**; the Opening
  proper will follow on completion of Form L, which never happens. **One
  trope** (the vault nobody can open). `SW_NIX2_OPEN`: the Door (event 3,
  page 2) is open, drawn open, and the way in, **for everybody**; the
  Mayor's page 4 is empty because he has gone in "at something close to a
  run" (events 7, inside, while the switch is on).
* **The chair** (event 8): WE SPENT IT. J. Pocklington, Clerk to the
  Corporation. 1788. "Two hundred and twelve years we've been assumed to
  have enough. On the strength of a chair." It is a very good chair. The
  change counts to **1,788 crowns**, which nobody can explain, and the Mayor
  insists: it isn't the Corporation's, the memorandum says they have
  enough. With Nix: "Provenance?" / "None whatever." / "...I'll write it
  down." Only the opening needs Nix; the chair does not.
* **Afterwards for everybody**: the Mayor's own last page plus the preamble,
  read to the chair, in full, twice; the Town Clerk's plus "Form L is still
  blank. In law, the Counting House has never been opened."
* **Ids taken:** switches **151** `SW_NIX2_OPEN`, **152** `SW_NIX2_DONE`;
  Map 63 events 6-8; `places.VAULT`, `VAULT_CHAIR`, `COUNTING_BEFORE_DOOR`.
* One trope, no blush. Running tally: **tropes +18 fixed and 2-9 from PIP-2;
  blushes +11 fixed and 0-1 from PIP-2.**
* **Candidate ending line** (G1; read `SW_NIX2_DONE`): "The Counting House at
  Great Dunnage has been opened, informally. It held a chair. Form L remains
  blank."
* **The rooms (0.1):** the lobby was cropped with Great Dunnage in B1 and is
  unchanged; the vault is new, screenshotted at both sizes.
* **Scenario** `q_nix2`: passes.
* `TIMELINE.md`: 1788, the clerk's note.

**B7, ROL-1 The Appointment - done.** ROL-1's section at the bottom of
`q_roland.py`, hooked from `dunnage.py`'s Bell (two places);
`build/scenarios/q_rol1.json`.

* **At the Bell, not the Smiths' Hall** - the snug is the Bell's west table
  at (4,8) and its two stools, which was already furniture, so nothing was
  drawn. The Hall is the Company's, and the joke wants a booked table in a
  pub rather than a chamber.
* **The summons is Mrs Dewhirst's** (Map 65 event 2, page 3, below her
  one-self-switch ladder, with Roland): "The snug's booked in your name,
  love. The usual." Roland goes slightly pink, which you would not have
  thought possible, and permits it: "Don't say anything." The page is her own
  last page with the summons in front of it, once (it skips while
  `SW_ROL1_ON` or `SW_ROL1_DONE` is on), so with Roland the inn is still the
  inn.
* **The meeting** - `SW_ROL1_ON` (ends) seats **the Convenor** and **Fellows
  Grice, Amory and Blunt** at the table (events 11-14, empty before and
  after; without Roland they wait for the asset). With Roland, the
  Convenor's page is the hundred and forty-first meeting: apologies (the
  sorcerer), the minutes of the hundred and fortieth, readiness - the stone
  not ready, the sword in the stone, the sorcerer sends his apologies, the
  lineage "Present." (underlined twice) - the continued availability of the
  asset ("Available." / "Noted, with thanks."), any other business (a
  minute's silence), and "thank you, Mr Fairweather, for your continued
  patience. Until the next door." Eleven minutes. "A hundred and
  forty-one." **One trope** (the summons that takes the ally away). Nobody
  says what it resembles; the scenario asserts no line names Grimspite or
  "the other end".
* **The minutes are item 52**, "The Minutes (141st)": "Apologies: the
  sorcerer. Readiness: not. Lineage: present. Asset: available. Thanked.
  Eleven minutes." Roland hands them over: he has a drawer of them. He is
  still in the party, and still leaves at the door.
* **Ids taken:** switches **153** `SW_ROL1_ON` (ends), **154**
  `SW_ROL1_DONE`; item **52** `IT_MINUTES`; face `Gen_People13` **1** (the
  Convenor, generated); the three fellows share stock faces nobody in the
  Bell wears - `People2` 0 and 4 and `People1` 3. `People3` 0 and 1 were
  tried first and were a crown and a pair of wings, which are of some
  importance.
* One trope, no blush. **Running tally at the end of Part B: tropes +19
  fixed and 2-9 from PIP-2; blushes +11 fixed and 0-1 from PIP-2.**
* `SW_STORY[ROLAND]` (on already after ROL-3 or ROL-4 in a game that did
  those).
* **Candidate ending line** (G1; read `SW_ROL1_DONE`): "Somewhere there are
  minutes of a hundred and forty-one meetings, at which Roland Fairweather
  was present and available, and was thanked for his patience."
* **The rooms (0.1):** the Bell was cropped in B1; nothing changed.
* **Scenario** `q_rol1`: passes.
* `TIMELINE.md`: nothing dated (a hundred and forty-one meetings are a count,
  not a span).

**Rerun for Part B** (0.1): every step appended pages to Great Dunnage, so
once B7 was committed `dunnage` and `dunnage_company` were run again, alone
and with no timeout - **both pass**. (After B1 `dunnage_company` had passed
and `dunnage` had been killed by an hour's timeout beside another browser,
with no failures as far as it got.) Nothing is owed.

**C1, ZEPH-1 The Fines - done.** ZEPH-1's section at the bottom of
`q_zephyrine.py`, hooked from `village.py` (the letter) and `collegium.py`
(the world-map doors, Mr Gedge, the IN and OUT board, Prewitt, the Register
and the clerk); `build/scenarios/q_zeph1.json`.

* **Decided: the occasion is a letter.** Her refusal at the world-map door is
  one nobody can argue with, and she "drinks at the Gilded Turnip in the
  manner of a person waiting for a letter" - so one comes. A new event on her
  old table at the Turnip (Map 4 event 11, (12,6), an `Envelope` drawn over
  her glass, read from where she used to sit), nothing at all without her:
  NOTICE OF OUTSTANDING FINES (ELEVENTH), Miss Z. Vance, on study leave. The
  first ten went to her pigeonhole, her last address; the new Registrar's
  clerk looked her up. "STUDY leave. I was EXPELLED." She folds it into her
  hat - **item 53** - and `SW_ZEPH1_ON`. **One trope** (the return to the
  wizard school).
* **The world-map doors** (Map 8 events 64-65) keep pages 1-3; page 4
  (Zephyrine and `SW_ZEPH1_ON`) is "I want it on the record that I am FINE"
  and in at the gate; page 5 (Zephyrine and done) goes in either way, with
  a line for each end.
* **The scene is Mr Pennock's**, the Registrar's clerk, a new event at the
  east end of Prewitt's desk (Map 59 event 7, `collegium.PENNOCK` (6,7)):
  empty until the notice is read, then waiting with her file if she is not
  in the party, so a dismissed Zephyrine's errand waits. With her: there is
  no appeal because there was no expulsion - a draft, initialled by the Dean,
  referred to the Registrar, who referred it to the Committee for
  Expulsions, which has never had to meet. Eleven years of unpaid study
  leave, in good standing. "Not an error, Miss Vance. A referral." Mr Gedge
  is sent for to lift the Register although it is not a Monday, and the
  large account is hers: three books, spring 1989, a penny a day with the
  day's interest - **4,117,206 crowns and ninepence**, the largest number in
  the game. One of the books is holding her door shut.
* **The real choice, three ways**, after the reveal (once, `SW_ZEPH1_TOLD`):
  **turn out the purse** - statute nine, a member who turns out her purse on
  the Library desk in good faith on the day is deemed to have paid, never
  invoked because nobody has had the nerve - which takes **every crown the
  party has** (`VAR_ZEPH1_PAID` keeps the figure; it is the gold sink
  `COMPANIONS.md` wanted, and it is the whole purse, whatever is in it), and
  gives her name back, the robe and a slide on the IN and OUT board; or **file
  the expulsion** herself - "Properly. In writing. It's the only thing
  anybody here ever did about it, and it wasn't even done" - which costs
  nothing, because members of the public are not fined, and she smiles; or
  **not today**, which keeps the file on the desk. Either end sets
  `SW_ZEPH1_DONE`, one trope and her story. C2 and C3 must work for both.
* **Zephyrine's gear** (0.5): armour **43** "Collegium Robe (Vance)", body
  armour of a new armour type **10, "Robe"**, which her actor has a trait for
  - the badge pattern. MMP +60, DEF +20, MAT +30, MDF +40, AGI +4, and MP cost
  x0.9: the right equipment, at last. Only on the paid end.
* **Mr Gedge** (Map 58 event 6, page 3: his A, Zephyrine, the notice): "Your
  pigeonhole's full. Eleven years of it." / "You KNEW." / "The Lodge knows
  everything, miss. The Lodge is never asked." Afterwards with her: her
  slide is up, he painted it himself; or "Member of the public, is it, Miss
  Vance? Keep to the path. Lovely to see you."
* **Afterwards for everybody**: Pennock (the tidiest file in the building, or
  the only thing he has ever actually filed); Prewitt's own last page plus
  PAID IN GOOD FAITH, or CLOSED, which she looks at "as you might look at a
  view"; the Register's, a little lighter; and, paid only, the IN and OUT
  board's new slide, Z. VANCE: OUT, "Study leave. Good standing." in the
  Porter's pencil. Prewitt with Zephyrine before it is decided refers her to
  Pennock, who has kept the file on top since March.
* **Ids taken:** switches **155** `SW_ZEPH1_ON`, **156** `SW_ZEPH1_TOLD`,
  **157** `SW_ZEPH1_PAID`, **158** `SW_ZEPH1_EXPELLED`, **159**
  `SW_ZEPH1_DONE`; variable **23** `VAR_ZEPH1_PAID`; item **53**
  `IT_FINES_NOTICE`; armour **43** `AR_COLLEGIUM_ROBE`, armour type **10**
  `AT_ROBE`; Map 4 event 11, Map 59 event 7; face `Gen_People13` **2** (Mr
  Pennock, generated: young, neat, chestnut, the Collegium's purple and
  white).
* Two tropes, no blush. Running tally: **tropes +21 fixed and 2-9 from
  PIP-2; blushes +11 fixed and 0-1 from PIP-2.**
* `SW_STORY[ZEPH]` (on already after ZEPH-5 in a game that did it).
* **Candidate ending lines** (G1; read `SW_ZEPH1_PAID` / `SW_ZEPH1_EXPELLED`):
  paid - "Zephyrine Vance is a member of the Collegium Arcanum in good
  standing. Her library fines were paid in good faith, out of a purse, on
  the Library desk."; expelled - "Zephyrine Vance was expelled from the
  Collegium Arcanum eleven years after the event, at her own request. She
  filed it herself."
* **The rooms (0.1):** the Collegium had never been swept. Maps 58-60 were
  cropped with `propsheet.py` (59 tiles) and screenshotted: the purple roofs
  and spires, `Statue B` the Founder, `Tapestry B` the banner, the
  stained glass, the Library's bookcases, `Table D` with the hourglass and
  `Closed Books C` (the Register), `Basin` the Appeal's bucket, High Table's
  `Table E` and the two portraits. Everything is what its event says.
  Nothing needed fixing. The Turnip was swept on 30 Sep.
* **Scenario** `q_zeph1`: passes (38 checks). It walks both ends - the
  purse with 1,234 crowns, then the switches put back and the draft filed -
  and asserts the robe is Zephyrine's alone.
* `TIMELINE.md`: 1989, the incident, the three books and the draft.

**C2, ZEPH-3 Dean Fenwold Is Fine - done.** ZEPH-3's section of
`q_zephyrine.py`, hooked from `collegium.py` in four places (the Dean, his
portrait, the undergraduate, Dr Hapgood); `build/scenarios/q_zeph3.json`.

* **Decided: the why is Hapgood's footnote.** `COMPANIONS.md` says she did it
  over a junior fellow's paper attributed to somebody senior; the court
  already had the junior fellow - Dr Hapgood, Junior Fellow, twenty-two
  years, going round - and the IN and OUT board already had the senior: the
  Master, "thought to be a committee". So: On the Kindling of Damp Materials,
  by Hapgood, went out under the Master's name, "and the Master is a
  committee"; she said so at High Table and the Dean told her to let it go.
  Nobody senior is a villain, because nobody senior is a person.
* **It is the Dean's page 3** (Map 60 event 2: his A, Zephyrine,
  `SW_ZEPH1_DONE`), which also knows how ZEPH-1 ended - "Pennock says you
  paid... Prewitt had to sit down" or "you filed it. Yourself. I initialled
  that, you know." The talk wants a demonstration, small, controlled, with
  buckets. "No." Then "...On terms": one, the room is wrong and he will say
  so in the talk; two, Hapgood's paper, under his name - "I'll write the
  note" - and "I should have backed you, Vance. At the time." / "I was
  right." / "You were right." It is the best apology he has, and it is going
  in the talk. **He is not a villain**: the scene never makes him one.
* **The fire**, a rehearsal now "before either of us thinks better of it":
  the undergraduate brings one bucket, the Library's, still catching
  something; "The room is wrong. Stand by the door." / "Noted!" - he does not
  move, as he did not in 1989; Kindle; and the Hall draws, chimney to door,
  down the Hall, past eleven Deans and into the twelfth. Drawn, not tiled:
  animations 66, 68, 69 and 70 on the Dean, the undergraduate and the party,
  a tint to orange and then red, two flashes, two shakes, five sounds, and
  the tint back to normal. **No consequences**, asserted: no gold, no items,
  no hit points, no tile. Eyebrows gone; "I'm fine!"; "We heard her, sir.";
  "EXACTLY the same reason. I SAID." She has cast something indoors for the
  first time in eleven years. **One trope** (the mentor who was secretly the
  villain - denied). PIP-2's "I set fire to a Dean. The Collegium only
  minuted it." agrees.
* **Afterwards**: the Dean's own last page plus the talk's new ending (she
  said the room was wrong, and it was; twice; the eyebrows are coming back);
  with her, "Fine. Both times." / "Stand by the door." / "Noted!"; his
  portrait's second card, "And again, 2000. The painter has been asked
  back."; Dr Hapgood with an offprint in his own name, going round "slightly
  taller"; the undergraduate, who has kept the bucket.
* **Ids taken:** switch **160** `SW_ZEPH3_DONE`. No faces, no items.
* One trope, no blush. Running tally: **tropes +22 fixed and 2-9 from
  PIP-2; blushes +11 fixed and 0-1 from PIP-2.**
* **Candidate ending line** (G1; read `SW_ZEPH3_DONE`): "Dean Fenwold is
  fine. His talk now ends with the room being wrong, and Dr Hapgood's paper
  has Dr Hapgood's name on it."
* **The rooms (0.1):** the Hall was cropped in C1; nothing changed - the fire
  touches no tile.
* **Scenario** `q_zeph3`: passes (17 checks), on ZEPH-1's expelled end; the
  fire is redrawn for one shot and looked at.
* `TIMELINE.md`: C1's 1989 row gains Hapgood's paper.

**C3, ZEPH-2 The Duck - done.** ZEPH-2's section at the bottom of
`q_zephyrine.py`, hooked from `nomap.py` (the pond, in a wrapper like the
Lay-By's) and `collegium.py` (the world-map doors, Congregation's notice, Dr
Hapgood, the Appeal and the chair); `build/scenarios/q_zeph2.json`.

* **Decided: Congregation is quorate at twelve** - eleven Fellows who come to
  things, and one who is a duck - **so every meeting since the incident has
  been inquorate, and that is why everything at the Collegium has been
  referred for eleven years.** The place's whole joke turns out to have a
  cause, and the cause is on a pond.
* **Decided: it needs ZEPH-3.** Hapgood's paper is out under his own name, so
  Congregation at last has something it wants to decide - his Senior
  Fellowship - and its notice (Map 58 event 10, which has no ladder) says so,
  for everybody, with INQUORATE (eleven present; twelve required). With
  Zephyrine she reads it, counts, and knows: "And one who is a duck." /
  "We are going to fetch a duck." `SW_ZEPH2_ON`. **One trope** (the escort
  mission).
* **Decided: the duck is a key item, not a follower event** - item **54**,
  "The Honorary Fellow" (a feather icon). An event cannot leave its map, so
  a duck walking behind the party would be left at the pond by the first
  transfer and lost to the airship for good; the item survives both, and
  the escort is in the telling. It is wordless - a quack in narration, the
  `Chicken` sound - so **it needs no face** and nothing goes on `AUDIT.md`.
* **The pond** (Map 8 event 56) keeps its two pages; page 3 (its A,
  Zephyrine, `SW_ZEPH2_ON`) is the two of them, both at the enquiry; it
  walks into a reed and stands ready. "Four hit points. Walks into
  everything. Ysolde did nine weeks of this." - the duke's son of her tale in
  the Slain Wyvern. `SW_ZEPH2_WALKING` (ends). Page 4 is the pond without
  it, GONE TO CONGREGATION; page 5 the Fellow home, proxy given, "and does
  not intend to be walked again".
* **The world-map doors' page 6** (Zephyrine and the duck): it walks into a
  milestone, the gatepost and Mr Gedge, in that order, and Mr Gedge touches
  his hat to it.
* **The vote is at its chair** (Map 60 event 5, below its one-self-switch
  ladder): without Zephyrine it will not sit; with her, it fits the dent and
  puts the feather back. Eleven Fellows, the Dean in the chair, Pennock with
  the minutes: "We are QUORATE." Hapgood, five-five, the chair abstaining;
  the duck walks into the Dean's water jug and says, once, quack. Carried -
  and outside a thin man stops going round the lawn for the first time in
  twenty-two years. The roof, carried; items three to four hundred and six,
  carried; through by half past six. The duck names its proxy by walking
  into Zephyrine: PROXY - Z. VANCE. PERMANENTLY. (On the expelled end:
  "Nobody ever said a proxy had to be a member. Nobody thought to.") "It's
  the only vote I've ever had in this place." Mr Gedge takes it home in the
  Lodge's handcart. **Item 55**, "The Duck's Proxy", replaces the duck.
* **Afterwards for everybody**: the notice, CARRIED, the Honorary Fellow
  voting, and the roof; the chair's second card, PROXY - Z. VANCE.; the
  Appeal, THE ROOF - CARRIED, the bucket staying until it is mended; and
  **Senior Fellow Hapgood**, who has stopped going round and stands in the
  middle of the path while people go round him (his page 4, above ZEPH-3's
  offprint page).
* **Fixed on the way:** the Notice of Fines (item 53, C1) had the key icon,
  195; it is the envelope, 192, now. The proxy is 193, the minutes' scroll.
* **Ids taken:** switches **161** `SW_ZEPH2_ON`, **162** `SW_ZEPH2_WALKING`
  (ends), **163** `SW_ZEPH2_DONE`; items **54** `IT_DUCK`, **55**
  `IT_PROXY`. No faces.
* One trope, no blush. Running tally: **tropes +23 fixed and 2-9 from
  PIP-2; blushes +11 fixed and 0-1 from PIP-2.**
* **Candidate ending line** (G1; read `SW_ZEPH2_DONE`) - the one joke the
  proxy is worth: "The Collegium Arcanum has been quorate since the duck came
  back. Its vote is held by proxy, permanently, by Zephyrine Vance. She has
  not yet used it. She is saving it."
* **The rooms (0.1):** the Hall, the court and the Library were cropped in
  C1; nothing changed. The pond is a world-map cell.
* **Scenario** `q_zeph2`: passes (25 checks), on ZEPH-1's paid end.
* `TIMELINE.md`: nothing dated ("eleven years" is C1's 1989).

**C4, WRE-1 The Monograph - done.** WRE-1's section at the bottom of
`q_wren.py`, hooked from `collegium.py` (the shelf, the reviewers, the list),
`nomap.py` (the pond) and `journey.py` (the eleven specimens); the records in
`db.build_monograph`; `build/scenarios/q_wre1.json`.

* **The start is the shelf's second look** (Map 59 event 5, which has one
  page with her reaction shot in it). Page 2 is that page exactly, for her,
  and marks the gap seen (its self switch B - cosmetic; the quest is
  global); so her first visit is the published scene, word for word, which
  `collegium` asserts. Page 3, her second look, finds one of the Library's
  cards tucked into the gap: A MONOGRAPH OF THE COLLEGIUM REQUIRES (I) A
  TYPE SPECIMEN FOR EVERY ENTRY; (II) THREE FELLOWS TO REVIEW IT; (III) A
  LIST OF SUBSCRIBERS. "Rowbotham named three hundred species and never had
  a type specimen for one of them. He named them after his dogs."
  `SW_WRE1_ON`. **One trope** (the collect-them-all). The same page then
  counts what is left (`\V[24]` of eleven, three reviewers, six
  subscribers) and publishes when it is all there.
* **Decided: the specimens are on the world map**, one by each of eleven
  places, as tracks (`!Other1` 5, the footprints) that are there only while
  the monograph is on - Map 8 events **70-80**, appended after every other
  event so no existing id moves. With Wren: Rowbotham's name for it, what it
  actually is, "Measure it / Leave it", and a fight with no escape (a type
  specimen will not wait); the specimen is **measured, not killed** - "which
  it minds a great deal more" - and let go. Without her: "Wren would know
  what made them." Collected is the event's self switch; the count is global,
  `VAR_WRE1_SPECIMENS`, so a dismissed Wren's count waits. The eleven, Wren's
  name / Rowbotham's / where: Common Hedge Egg / Rowbotham's Breakfast /
  Firstfield; Frilled Wall Lizard / Rowbotham's Magnificent / Restwell;
  Hearth Salamander / Rowbotham's Comfort / the Cinder Fen; Turnip Gnome /
  Mrs Rowbotham ("She knew.") / Thistlewick; Barn Cait / Biscuit, his dog /
  Fairholme; Striped Warren Hare / Rowbotham's Tiger / the Sable Hart;
  Upright Fox / Pelham-Rudd's Fox, a subscriber / Gladhollow; Many-Eyed
  Grazer / Rowbotham's Ox / Frostwick; Draught Sylph / Lady Amberley, a
  subscriber "who had a cold" / the Sky Anvil; Tall Marsh Wader /
  Rowbotham's Self-Portrait ("It does look like him.") / Weeping Bottom; Pond
  Kappa / Captain, his other dog, a spaniel / Ashcombe Lake. Each cell is
  three or four steps off its place, open ground, reached on foot from
  Thistlewick (checked by a flood over Map 8's passability).
* **The fights**: enemies **44-54**, troops **42-52**, one specimen each,
  stock art (`Oddegg`, `Frilledlizard`, `Salamander`, `Gnome`, `Caitsith`,
  `Tigerbunny`, `Foxman`, `Hakutaku`, `Sylph`, `Birdman`, `SF_Kappa` - none
  used by any other enemy), 1,500-2,400 hit points, 340 experience, **no
  gold** - she will not sell them. Skills **175-178**: Startle (an attack
  debuff), Bolts For Cover (agility, self), Bites The Note-Taker, and Is Not
  Where You Measured It (all). No generated people fight, so nothing goes on
  `AUDIT.md`.
* **The reviewers are two of Rowbotham's three students**, who reviewed her
  first paper at twenty-three, at the Library's reading table from the start
  (Map 59 events **8-9**, empty until then): **Professor Mott** (face
  `Gen_People13` **3**: white hair and beard, round spectacles, the gown) -
  "I said it lacked respect." / "It did." - who has been a beetle for forty
  years and "should like, before I die, to be a person"; and **Dr Furze**
  (`Gen_People13` **4**: a silver bun, spectacles, the jacket and tie) - "Too
  many footnotes." / "There were exactly enough footnotes." - who stops at
  page four hundred, the Lesser Wyvern: "You've written 'goose'." She was in
  the Slain Wyvern the night they asked Wren to leave, "and I have always
  known". Accepted, with no corrections, which she has never written before.
  Both want the eleven specimens first. Whichever is second names the third
  reviewer, **the Honorary Fellow** (`SW_WRE1_DUCK_DUE`, ends): at its pond
  (Map 8 event 56, page 6) it walks on to the manuscript, reads page four
  hundred, and sits down on it. "That is acceptance." It is wordless, as in
  C3. If ZEPH-2 has the duck out walking, the pond says GONE TO CONGREGATION
  and Wren comes back later.
* **The subscription list is a shop with names in it** (Map 59 event **10**,
  on Prewitt's desk by the hourglass): eight subscriptions, items **56-63** -
  Dorcas Thrupp, the Gloamwood Society, Mr Ottershaw, Bram, Dr Hapgood, Mr
  Gedge, Prewitt, Edith Pellow - at **150** each, purchase only, and **six**
  are needed (`db.SUBSCRIBERS_NEEDED`). The party pays, "because nobody in the
  valley has ever been asked to subscribe".
* **Publication**: Prewitt binds it herself; THE FAUNA OF THE VALLEY, BY WHAT
  THEY ARE. W. HALLOWAY goes into the gap, and it is exactly an inch wide.
  "There was room." Item **64**, The Monograph.
* **Wren's party ability upgrade, additively.** Her ability was one trait on
  the Cataloguer class, party ability 5, double drops ("she is collecting
  specimens"). Publication is **Change Class, experience kept, to class
  11, "Cataloguer (Published)"**: her class record copied whole, plus party
  abilities 2 (cancel surprise - nothing the monograph describes takes the
  party by surprise) and 3 (raise preemptive - the party tends to see it
  first). The Cataloguer record and every other actor are untouched; the
  scenario asserts her level and experience are kept and double drops still
  hold.
* **Afterwards for everybody**: the shelf, with the monograph where the gap
  was (and without the reaction shot); with her, "Wren does not look at it.
  Then she does."; Mott ("A person. Not a beetle."), Furze ("It is a goose. I
  have it in writing now"), and the list, closed and bound in at the back.
* **Ids taken:** switches **164** `SW_WRE1_ON`, **165** `SW_WRE1_MOTT`,
  **166** `SW_WRE1_FURZE`, **167** `SW_WRE1_DUCK_DUE` (ends), **168**
  `SW_WRE1_DUCK`, **169** `SW_WRE1_DONE`; variable **24**
  `VAR_WRE1_SPECIMENS`; items **56-63** `IT_SUBSCRIPTIONS`, **64**
  `IT_MONOGRAPH`; class **11** `CL_WREN_PUBLISHED`; enemies **44-54**; troops
  **42-52**; skills **175-178**; Map 8 events 70-80, Map 59 events 8-10;
  faces `Gen_People13` **3-4**.
* One trope, no blush. **Running tally at the end of Part C: tropes +24
  fixed and 2-9 from PIP-2; blushes +11 fixed and 0-1 from PIP-2.**
* `SW_STORY[WREN]` (on already after WRE-2, -3 or -5 in a game that did one).
* **Candidate ending line** (G1; read `SW_WRE1_DONE`): "The Fauna of the
  Valley, by What They Are, by W. Halloway, is on the shelf of the Collegium
  Arcanum, in a gap exactly an inch wide. It has eleven type specimens and
  three reviewers, one of them a duck. Page four hundred says goose."
* **The rooms (0.1):** the Library was cropped in C1; nothing changed - the
  reviewers stand on open floor at either end of the reading table, and the
  list is on the desk.
* **Scenario** `q_wre1`: passes (47 checks): two specimens fought (one
  walked on to, one started where it stands), nine set by script; the list
  opened as a shop and one subscription bought through it; Mott, Furze and
  the duck; publication; and the upgrade asserted present with her and gone
  without her. The first run failed at the pond, and it was the page, not
  the scenario: with Wren, every visit to the shelf replayed her whole
  reaction shot before the count, so `advance` ran out of presses and the
  next `goto` never arrived. A second visit is now the shelf's narration and
  the count only, asserted.
* `TIMELINE.md`: nothing dated (Rowbotham's "forty years" and Wren's first
  paper are not new dates).

**Rerun for Part C** (0.1): after C4, every scenario that walks Maps 58-60
was run again, alone and with no timeout - `collegium`, `q_zeph1`,
`q_zeph3`, `q_zeph2`, `q_wre1` - and `nomap`, because the Duck's Pond had
pages added twice. **The first `collegium` run failed, and it found a real
fault**: C4 had put the card that starts WRE-1 on Wren's *first* visit to
the shelf, straight after the published reaction shot - so the site step's
assertion that her shelf says nothing of reviewers or specimens broke, the
scene ran on past "She says nothing else, and walks on", and the walk after
it never left the Library. Fixed in C4's own pages rather than in the
assertion: her first visit is the published page exactly, and the card is
her second look. The other `collegium` failure was its own count of the
world-map doors' pages, which C1 and C3 took from three to six by design;
the check now says six and why. **All six pass**: `collegium` 101 checks,
`q_zeph1` 38, `q_zeph3` 17, `q_zeph2` 25, `q_wre1` 47, `nomap` 44. Nothing
is owed.

**D1, COR-1 Ashcombe (New) - done.** COR-1's section of `q_corvin.py`,
hooked from `ashcombe.py` in seven places (the door, the notice, Mrs Ash, the
Roll, the menus, the study's four events, and the study drawn by
`ashcombe.study_room`); `build/scenarios/q_cor1.json`.

* **Decided: what sends him back is his own name**, not a letter (ZEPH-1 had
  the letter). The museum's Roll has one name marked "Away. (Written to.)"
  and the site left it unsaid whose. With Corvin the first read is the
  published page exactly (it marks its self switch B, cosmetic); the second
  is his: two hundred and six people stood on a hill in the rain and counted
  him anyway. "I was in a corner of the Slain Wyvern. Being away. On
  purpose." / "They counted me anyway." / "...Today, then." `SW_COR1_ON`.
* **The door** (Map 52 event 3) keeps both refusal pages; page 4 (Corvin and
  the switch) is "Not -", and he knocks on his mother's door like a visitor,
  and it is always open - then the door's own page. **It sets Mrs Ash's self
  switch A by script**, ALD-4's way with Duchess: her ladder's terminal,
  because her first page is "My boy's away" and her boy is in the kitchen.
* **Home is Mrs Ash's page 4** (Map 53 event 2: her A, Corvin, the switch),
  carrying what of her first page is still true - the new step, the new
  kettle, the Tuesday and the kettles up the hill - and for the first time in
  eleven years the needles stop. "I have come back. To what is left." /
  "Well, it's all left, love. It's just up the hill a bit." She wrote
  Wednesdays and Saturdays; he wrote once, to THE RUINS OF ASHCOMBE (Mrs
  Dimmock's published letter), **and the Ruins' answer was hers**: "I
  thought you'd like that." / "...I did like it." **One trope** (going
  home), `SW_COR1_HOME`. Nothing in it goes wrong for him.
* **The study** - the bedroom, rebuilt larger with better light - **is Map
  53's black east**: the map widened from 26 to 36 columns, the kitchen and
  museum tile for tile what they were (checked). `places.STUDY` (28,4)-(33,8),
  the kitchen's white walls, two tall windows, a bookshelf, a globe, a blue
  rug, a chest of drawers for pigeonholes, and `Table A` with `Notes D` and
  `Pen A`. Up a flight: its door (event 13) appears in the kitchen's north
  wall at (6,3) once he is home, for everybody, and its way out (event 14)
  is the foot of its stair. **The Committee's desk** (event 15): Hon. Sec.
  Mrs Ash, and a pigeonhole marked C with eleven invitations, one a year, to
  the Slain Wyvern, none stamped - "I didn't post it, love. You'd only have
  said not today." / "...I would have." He takes this year's, **item 65**.
  **The height marks** (event 16), put back from memory, each a little
  taller than a boy would have been; with Corvin, the last is exactly the top
  of his head. "She drew where he would be."
* **The Dinner is at its notice** (Map 52 event 9, which has no ladder), with
  Corvin and the invitation: "Confirm the speaker / Not yet". Faded out, the
  church hall, Mr Weir on culverts, and the speech: he was not here, he was
  in an inn eight miles off ("By the ROAD."), he carried the name about in
  corners, it was not gone, it went up the hill and built the drains and
  wrote to him - "So I have brought the name back. You may as well have it.
  You were using it." It goes well. "To the water." / "Which was very good
  about it." On the last word Mrs Ash casts off.
* **Corvin's gear** (0.5): armour **44** "Scarf (Wrong Colour)", an accessory
  of a new armour type **11, "Scarf"**, which his actor has a trait for - the
  badge pattern. MHP +80, DEF +8, MDF +12, LUK +6, ice x0.5 and HP regen +3%,
  which about cancels the elective curse's bleed; nobody planned it. Bright
  yellow, the yellow of the new roofs, the wrong colour for everything he
  owns. "If I'd done it in black, nobody'd ever see you in it." The
  invitation is handed in.
* **Afterwards for everybody**: Mrs Ash's own last page plus another one
  started, the same colour; the notice, C. ASH. (CONFIRMED.), and Mr Weir
  has kindly offered next year; the museum's menus, this year's on top,
  VERY GOOD in pencil; the desk, ten invitations and the eleventh answered.
  With Corvin, Mrs Ash's kitchen: he keeps the scarf on by the range. Mr
  Weir was left alone, for COR-2.
* **Ids taken:** switches **170** `SW_COR1_ON`, **171** `SW_COR1_HOME`,
  **172** `SW_COR1_DONE`; item **65** `IT_INVITATION`; armour **44**
  `AR_SCARF`, armour type **11** `AT_SCARF`; Map 53 events 13-16;
  `places.STUDY`, `STUDY_DOOR`, `STUDY_DESK`, `STUDY_MARKS`. No faces: nobody
  new speaks.
* One trope, no blush. Running tally: **tropes +25 fixed and 2-9 from PIP-2;
  blushes +11 fixed and 0-1 from PIP-2.**
* `SW_STORY[CORVIN]` (on already after COR-5 in a game that did it).
* **Candidate ending line** (G1; read `SW_COR1_DONE`): "Corvin Ash spoke at
  the Ashcombe Flood Dinner, and it went well. He gave the village its name
  back. His mother knitted him a scarf in the wrong colour, and he wears it."
* **The rooms (0.1):** Ashcombe had never been swept. Maps 52-53 were
  cropped with `propsheet.py` (67 tiles) and screenshotted: the green and
  yellow roofs, the church's stained glass, the allotments and the
  scarecrow, `Monument C` the plaque, `Sign B` the Flood Dinner; in the
  kitchen the range, sink, counters, dresser, clock and the empty `Basket
  A`; in the museum `Stone Tablet` the old drain, `Map B (H)` the plan,
  `Dais` the plinth, `Posted Notice` the Roll and the menus, and the lake in
  oils. Every event sits on what it says. Nothing needed fixing. The study is
  new, screenshotted.
* **Scenario** `q_cor1`: passes (71 checks). Its first run found a real
  fault: the door's script was handed to `R.script` as a string rather than
  a list of lines, so it was split a character a line and the door never
  opened. Both of the Dinner's choices are walked, "Not yet" first.
* `TIMELINE.md`: nothing dated (eleven invitations are 1989's eleven years).

**D2, COR-2 Ashcombe (Old) - done.** COR-2's section at the bottom of
`q_corvin.py`, which draws Map 66 (`q_corvin.build`, called from
`build_game`), hooked from `nomap.py` (the lake, in a wrapper like the
Lay-By's) and `ashcombe.py` (Mr Weir); `build/scenarios/q_cor2.json`.

* **Decided: the week is the week of the Flood Dinner**, so COR-2 needs
  COR-1, as NIX-1 needs NIX-4. The lake says the sluices are opened "once a
  year, for a week"; the Dinner is annual and its committee's speaker is
  Mr Weir, whose whole life is the culverts. So with Corvin, once he has
  spoken, **Ashcombe Lake** (Map 8 event 55, page 4: its A, Corvin,
  `SW_COR1_DONE`) is down, "like a tide that is bored", with a street at the
  bottom of the mud: "Walk down / Not now" ("...In a minute."). The week
  lasts until he has been, since nothing in the game keeps a calendar.
  Below the lake's ladder, so a player who always pressed on stops once
  first; `nomap.py` asserts the lake's cell is `places.ASHCOMBE_LAKE`.
* **The drowned street is Map 66, "Old Ashcombe"**, 22x15 on the Outside
  tileset, drawn in `q_corvin.py` since it is in no place (0.4): the lake
  still standing round three sides (`Water C (Dirt)`), the bed `Dirt` with
  `Soil` laid over it on layer 1 so it reads wet and grey, dry at the
  margins, one street of `Cobblestones A (Ruins)`, and three plots of
  `Cobblestones G (Ruins)` with moss on them where the Anchor, the Ashes'
  house and the schoolroom were, outlined by `Broken Stone Pillar B (Moss)`
  and rubble. Silent, with the `Drips` background sound. The first draw was
  pale beach sand and a red-and-gold treasure chest; the strongbox is
  `!Chest` 5, the iron one. The way out is the foot of the slope, to
  `places.LAKE_SHORE_STEP` (104,55), checked open four ways.
* **The doorstep** (event 4, `Stairs (Ruins)`, one step on its own) **is the
  one moment allowed to be simply sad**, and nothing in it is a joke: he
  sits on it, as he did, "waiting for something to happen. Then it did. And
  I was in the Slain Wyvern, waiting." A bell, up the hill, a long way off.
  Then the letters cut where he sat: the old ones, as on the tang, and under
  them for visitors, **MIND THE STEP**. His grandfather made the sword, and
  it stood on the step forty years holding the door open. "That is its
  name." - **the name COR-5 left on the tang unread, and his mother's "Mind
  the step. It's new." from COR-1**, which nobody points out. **One trope**
  (the sunken ruin), `SW_COR2_STEP`. The weapon record is not renamed: a
  database name is not part of a save, and the name is better said once.
* **The strongbox** (event 5) waits for the doorstep - before it, Corvin "is
  looking along the street for something else". After, it is the undercut:
  he opens it with the black sword, "which turns out to be very good at it";
  the schoolmistress kept everybody's reports, dry in oilcloth; his surname
  has run. Arithmetic, looks out of the window at it; Composition, writes
  darkly; Conduct, sits in the corner, and asked to sit elsewhere sits in a
  different corner; "He will go far, if he ever gets up." Corvin laughs, out
  loud, which nobody in the party has heard before. "It is a fair report."
  **Item 66**, the report card, which the ending reads. `SW_COR2_DONE` and
  his story. The schoolmistress does not speak, so **no face**.
* **The Anchor** (event 3): the pub sign face up in the mud, a hundred years
  over a pub and eleven under a lake, "the first time it has been any use";
  with Corvin, he was not allowed in, so he sat outside and waited. **The
  street's end** (event 6): the old church, up to its eaves - you could skim
  a stone on to it, which is Mr Weir's line in the museum, true.
* **Afterwards for everybody**: the lake's own last page plus a doorstep
  with a sword's name cut into it and a strongbox one report lighter; **Mr
  Weir** (Map 53 event 5, below his ladder, left free by D1), his own last
  page plus sluice week going off splendidly - "Somebody sat on a doorstep
  down there for an hour, and the culverts did not mind in the least."
* **Ids taken:** switches **173** `SW_COR2_STEP`, **174** `SW_COR2_DONE`;
  item **66** `IT_REPORT_CARD`; **Map 66** `MAP_DROWNED_STREET`, events 1-6;
  `places.ASHCOMBE_LAKE`, `LAKE_SHORE_STEP`. No faces.
* One trope, no blush. **Running tally at the end of Part D: tropes +26
  fixed and 2-9 from PIP-2; blushes +11 fixed and 0-1 from PIP-2.**
* `SW_STORY[CORVIN]` (on already after COR-5 or COR-1).
* **Candidate ending line** (G1; read `SW_COR2_DONE`): "Corvin Ash's sword is
  called Mind The Step. His grandfather made it for a doorstop. His school
  report says he will go far, if he ever gets up. He is up."
* **The rooms (0.1):** Map 66 is new and was screenshotted twice (the sand
  and the treasure chest, then the mud and the strongbox). Maps 52-53 were
  swept in D1; Mr Weir's room is unchanged.
* **Scenario** `q_cor2`: passes (37 checks), first run - "Not now" and then
  in, the strongbox before the doorstep and after, the Anchor, out by the
  slope, and afterwards with and without Corvin.
* `TIMELINE.md`: 1949, the grandfather makes the sword and cuts its name
  into the step ("forty years" before the water).

**Rerun for Part D** (0.1): after D2, every scenario that walks Maps 52-53,
Map 66 or the lake was run again, alone and with no timeout - `ashcombe`
(97 checks), `q_cor1` (71), `q_cor2` (37), `q_hob1` (81, Mrs Dimmock's post
box is on Map 52), `nomap` (44, Ashcombe Lake had pages appended),
`placeholder_doors` (12, it counts Ashcombe's world-map door cells) and
`q_wre1` (47, the Pond Kappa is three steps off the lake). They were found
by parsing every scenario's `query` and `goto` map ids and grepping for
Ashcombe and the lake's cells. **All seven pass**, with no check changed:
`ashcombe` asserts that the door refuses with Corvin and that Mrs Ash and
Mr Weir say nothing of COR-1, and both still hold, because every COR-1 page
waits on `SW_COR1_ON`, which only his own second look at the Roll sets.
Nothing is owed.

**E1, MER-5 The Well at Sump - done.** MER-5's section at the bottom of
`q_merribell.py`, hooked from `hamlets.py` in six places (Mr Thurle, Mr
Gammage, Mrs Pardew, the well, the minutes, the sign);
`build/scenarios/q_mer5.json`.

* **The start is Mr Thurle's second look** (Map 51 event 3, page 3: his A
  and Merribell). His first page with her is the published reaction shot -
  "Through the chair, please." - and stays the first visit word for word.
  On the second she plants herself where a chair would be and asks for an
  item three. The diagnosis takes a paragraph; the ledger says nobody has
  drunk a glass of water since 1794. "That's not a curse, Mr Thurle. That's
  thirst. Six generations of it." / "It's a very thorough curse." / "It's a
  very thorough thirst." **Decided: the wasps are made Water's business by
  re-forming the Water Committee** - one member, Merribell, seconded by you,
  the first motion seconded in Sump since 1794 - so nobody has to settle
  whose they were. WASPS, and for the first time, "...Not deferred."
  `SW_MER5_ON`. **One blush**: "I can tell from here what colour all of
  your -" / "THROUGH the chair. Please."
* **Decided: the cure is the Creed's rule one, the obvious thing** - wasps
  want water and something sweet, have had the water for two hundred years,
  so give them something sweet somewhere else. No fight: there is no wasp in
  the stock enemy art (only `Machinerybee`, which is used and is a machine),
  and the site already said "the wasps, which no sprite in the box can
  draw". **Mrs Pardew's jam** is item **67**, her gran's last jar,
  GOOSEBERRY 1931 (BETTER); her page 3 is her own last page plus the jam,
  once, to whoever asks once the Committee sits - **Merribell need not be
  there**, so a dismissed Merribell's errand waits on the well, not on her.
* **The well** (event 6, no ladder): page 2 while the Committee sits -
  without Merribell, its own page plus "The Water Committee is not present";
  with her and no jam, what is missing; with both, the cure. **The trope
  payload is the parish's Standing Orders for the Lifting of the Curse**,
  drafted 1795 and never used, read by Mr Thurle clause by clause, each one
  a cliche of the cursed village met by something smaller: a Chosen One
  present (PRESENT, underlined); the guardian of the well overcome (they go
  down the spit to the jam, four minutes, extremely loud, nobody stung -
  "Nobody had ever asked them to leave"); an ancient relic given up
  (gooseberry, 1931); a price paid in sorrow ("...It was the last jar", and
  a respectful second); the eldest's riddle (Mr Gammage: "What's wet, and in
  the middle of the village, and we've not had any since 1794?" - "Water." -
  "Took us six generations, that one."); and the curse called by its true
  name, Thirst. **Counted once**, as 0.2 says, however many it turns over.
* **The rule made literal**: Merribell's rope and tin cup (of course she has
  them), and item three - the Order's Rule of Life, Mother Ursula Pym, 1702,
  four lines, adopted as a by-law: I. Drink a glass of water. II. Sit down.
  III. Dry socks: two pairs, and a spare. IV. Then see how you feel. The
  parish does it in order, and in Sump the socks were always dry - "the one
  line of the four nobody here has ever had any trouble with". Mr Gammage
  falls asleep sitting up. "Four lines. One's about socks. It works." The
  curse, lifted, 2000, and time for an item four, which nobody has. The four
  lines were written here, since `COMPANIONS.md` names them and nothing in
  the game had yet; MER-2's socks line agrees, and E2's Pamphlet carries
  them.
* **Afterwards for everybody**: Mr Thurle (his hat off, both hands free -
  "There was time"); Mr Gammage's own last page plus "And then, quite
  suddenly, he is"; Mrs Pardew, who may be spoken to before noon now; the
  well with a rope and a cup on it and the wasps happy down the spit; the
  minutes' own page plus 2000, Item 3, the Rule, "Felt better."; and the
  sign's own page (its trope included, as before) plus "Lifted 2000. Please
  Mind The Well. (Rule Of Life Applies.)" Every Sump owner is now taken:
  **PIP-4 (E12) should be Little Gore's**, and ALD-1 (E5) is there too.
* **Ids taken:** switches **175** `SW_MER5_ON`, **176** `SW_MER5_DONE`; item
  **67** `IT_JAM`. No faces, no new events.
* One trope, one blush. Running tally: **tropes +27 fixed and 2-9 from
  PIP-2; blushes +12 fixed and 0-1 from PIP-2.**
* `SW_STORY[MERRI]` (on already after MER-2 or MER-4 in a game that did one).
* **Candidate ending line** (G1; read `SW_MER5_DONE`): "The curse of Sump was
  lifted in the year 2000 by the Water Committee, one member, with a glass
  of water. The minutes record an item three."
* **The rooms (0.1):** Sump had never been swept. Map 51 was cropped with
  `propsheet.py` (19 tiles) and screenshotted: the sandbrick houses and gold
  roofs, `Large Window C` as the doors, `Well` the well, `Sign B` the minutes'
  board, `Sign A` the fingerpost, `Pot`, palms and cacti. Everything is what
  its event says. Nothing needed fixing.
* **Scenario** `q_mer5`: passes (74 checks). Its first run ran out of
  `advance` presses in the agenda and the minutes (still busy, then a `goto`
  that never arrived) - budgets, not pages; the cure takes 120.
* `TIMELINE.md`: 1795 gains the Standing Orders, 1931 the jam, 1702 the Rule
  of Life.

**E2, MER-1 The Sisterhouse - done.** MER-1's section at the bottom of
`q_merribell.py`, hooked from `weeping_bottom.py` in four places (the
Prioress, Sister Bewick, the line, the queue); `build/scenarios/q_mer1.json`.

* **The start is the Prioress's second look** (Map 55 event 2, page 3: her
  A and Merribell). Her first page with Merribell is the published "We'll
  talk. Not today." and stays the first visit. On the second, it is today.
  **Decided: the master's disappointment runs the other way** - "I was. Not
  in you. I stayed for the symposia. Eleven of them. I chair them very
  well." - and Merribell says nothing, which is the kindest thing she could
  have said. Instead of the eleventh symposium (Whether Anything Works, at
  three), Merribell proposes the queue at the gate: twenty patients each
  half, and whoever is through first is right. The Prioress laughs, once;
  Sister Bewick wants it in writing IMMEDIATELY, and writes it, in eleven
  clauses, into volume three. `SW_MER1_ON`.
* **The queue is outside**, in the drizzle, on the track up to the door:
  the last six of the forty, Numbers Thirty-Five to Forty, Map 54 events
  **13-18** at (16,14)-(16,19), stock sprites (strangers), each with a line
  and, with Merribell, her looking along them "the way a general looks along
  a line". Empty before, and gone home after.
* **The contest is the Prioress's same page**, "Begin / Not yet" ("A minute.
  I want to wash my hands. Twice."). Sir Hamo keeps the score from the bed
  on the line, since both orders treat him and he is very fair. **Decided:
  the four answers are the Rule's** - Drink some water, Sit down, Dry socks,
  and the question she always asks, Have you eaten? - and four patients each
  want one of them: a carter who has driven since five with nothing to
  drink, a shepherdess squelching from the bog, a clerk who has stood in the
  queue four hours, and a small boy crying about a sock. The obvious thing is
  a point ("Point to the west!"); anything else, she gets there anyway and the
  point is withheld ("Very fair."). Sixteen more go through in a paragraph,
  including the farmer told at full volume across the ward exactly where his
  hernia is - **one blush**. `VAR_MER1_POINTS` keeps the score and Sir Hamo
  reads it off `\V[25]`.
* **Sister Bewick is not a villain**: she gets through one patient in the
  time, stage eleven, and Mr Grebe the fisherman really has the Weeping
  Bottom ague, the first case in nine years. "...It worked." Merribell gives
  her the point. **Whatever Works wins on points** - nineteen or twenty to
  one. Then Bewick asks to be examined on Whatever Works' doctrine, which is
  how a doctrine is settled; the Prioress has Mother Ursula's own pamphlet in
  the drawer since the first symposium, the Rule is on its first page, and
  Bewick is examined on it and passes: "It is very short. I can find nothing
  wrong with it. That is very annoying." No symposium at three; soup, on
  both sides. Her notebook: Intervention. Supported. (D1's was
  Unsupported.) **One trope** (the return to the monastery).
* **Merribell's gear** (0.5): armour **45** "The Pamphlet", an accessory of
  a new armour type **12, "Pamphlet"**, which her actor has a trait for - the
  badge pattern. MMP +20, MAT +12, MDF +8, and pharmacology x1.25 - healing
  +, as `COMPANIONS.md` has it: what she gives out does a quarter more.
* **Afterwards for everybody**: the Prioress (no symposium; soup at noon,
  the queue at two; bring a chair, people sit down now, "It's in the
  rule."); Sister Bewick's own last page plus the pamphlet in volume three as
  a bookmark, read eleven times; the line's own page plus the eleventh
  minute, Not held. The chapel (ALD-2's) and Sir Hamo (on the line, ALD-3's
  neighbour) were left alone.
* **Ids taken:** switches **177** `SW_MER1_ON`, **178** `SW_MER1_DONE`;
  variable **25** `VAR_MER1_POINTS`; armour **45** `AR_PAMPHLET`, armour type
  **12** `AT_PAMPHLET`; Map 54 events 13-18. No faces.
* One trope, one blush. Running tally: **tropes +28 fixed and 2-9 from
  PIP-2; blushes +13 fixed and 0-1 from PIP-2.**
* `SW_STORY[MERRI]` (on already after MER-2, -4 or -5 in a game that did
  one).
* **Candidate ending line** (G1; read `SW_MER1_DONE`): "The Order of
  Whatever Works won the Sisterhouse on points, nineteen to one, in an
  afternoon. Sister Bewick has been examined on its doctrine, and passed. It
  is four lines long."
* **The rooms (0.1):** Weeping Bottom had never been swept. Maps 54-55 were
  cropped with `propsheet.py` (41 tiles) and screenshotted: the green roofs,
  the chapel's stained glass, `Monument A` the founder's stone, ferns and
  mushrooms; in the ward the beds, `Medicine Shelf`s, `Bookshelf A`, the
  stew pot and soup bowl, `Pot A` the jug on Bewick's desk, the open book on
  the line and `Closed Books C`. Every event sits on what it says. Nothing
  needed fixing. (A batch of shots carried Map 54's drizzle into the ward's
  shot; the door clears it in play, and `weeping_bottom` asserts the ward
  dry.)
* **Scenario** `q_mer1`: passes (52 checks), first run - three answers right
  and one wrong (the boy, asked for water), 19 points, the score read off
  the variable, the Pamphlet Merribell's and nobody else's, and the queue
  shot in the rain.
* `TIMELINE.md`: 1991 gains the last ague case before Mr Grebe's, 1996
  Merribell leaving at twenty-two, and her age, twenty-six.

**E3, MER-3 The Healers' Table - done.** MER-3's section at the bottom of
`q_merribell.py`; the back room drawn by `south.back_room`, its events
appended by `south.wyvern_events` in one line; `build/scenarios/q_mer3.json`.

* **Decided: the Table meets in a back room that is really there.**
  `COMPANIONS.md` says "a back room of the Slain Wyvern", and the bar is full
  - ROL-3's dinner, six tales, three recruits and Dorcas. So Map 14 was
  widened from 25 to 37 columns, `village.archive_room`'s way, and the bar is
  tile for tile what it was (checked): `places.WYVERN_BACK` (28,4)-(34,9), in
  the bar's own wood, one long table of five `Table D`s with a bottle, the
  Table's minutes open, and bottles; a `Medicine Shelf`, a `Bookshelf A`, two
  plants. Its door is on the bar's north wall face at (15,3), between the
  bookcase and the red curtain, and is drawn only for the Table; its way out
  is the foot of the room, back to (15,4). (The crates at (3,15) and (21,15)
  looked like back stairs in a screenshot and are crates.)
* **Ysolde's own event is left alone**: its ladder ends on self switch B,
  behind the bench at the Barrow, and the quest cannot reasonably wait on
  that (0.2). So the Table is new events - **Map 14 events 33-40**: the
  door, the way out, "Ysolde (in the chair)", the four, and a card - and
  while the Table sits Ysolde is in the chair and also at her own table in
  the bar, which nobody in a pub would remark on.
* **The door appears for Merribell** (page 2, her actor): THE TABLE. MEDICS
  ONLY., and Ysolde from across the bar - "Sister! You. Yes, you, with the
  flask. You're a medic, aren't you? Then you're on the list. In."
  `SW_MER3_ON`. While it sits, without her: "Merribell is on the list. You
  are not, and somebody inside says so." Afterwards, a door anybody may
  use, to an empty room.
* **The round** (Ysolde's chair page): **Mother Grizel Pennyfeather** (81),
  a femur set with a church candlestick during the service ("The vicar
  carried on."); **Dr Lucius Hobday** (70), a barbarian stitched with a lute
  string ("The bard wanted it back. He got it back. Eventually."); **Nan
  Gilly** (88), a wizard's leg splinted with his own staff ("He walks with it
  now. Never said thank you. Sends a card."); **Mr Cuthbert Spence** (64),
  a tourniquet out of a paladin's sash ("He minded about the sash."); and
  Ysolde, the duke's son, four hit points, nine weeks - "You've heard it."
  Then Merribell, the youngest by thirty-eight years: water, sitting down
  and socks always work; "I've never lost anybody. I know what that means.
  It isn't a virtue. It's an average." **Nobody consoles her and nobody
  mocks her**: they look at Ysolde, "which is what the chair is for".
  "Then write it down. All of it. Every cup of water and every pair of
  socks. Now, tonight. While you still think it's boring. Because one day it
  won't be, and you'll want to know what you did on all the days it
  worked." And the day it doesn't, come down and tell them. "...Yes, Mrs
  Marrow." **No blush** - this is the Register B moment `COMPANIONS.md`
  asked for, Ysolde's second; **one trope** (the veterans' reunion). She
  starts writing down today in the book with every ailment in Thistlewick
  in it.
* **The Table's Kit** is armour **46**, an accessory of the general type -
  anybody's, since it "goes to the youngest" and the Pamphlet is already
  hers alone: a candle-end, a coil of gut string, a splint and a very good
  sash, rolled in canvas. MHP +60, MMP +10, DEF +10, MDF +10, recovery
  effect x1.15, HP regen 4%. Price 0.
* **Afterwards for everybody**: the four and the chair gone home; the card
  on the table - NEXT YEAR. SISTER M. (THISTLEWICK) TO SPEAK. "Bring the
  book. All of it." With the four asides while it sits (Grizel's candlestick
  is on her mantelpiece; the wizard is ninety and still cross; Mr Spence was
  the youngest "until about four minutes ago. It was lovely.").
* **Ids taken:** switches **179** `SW_MER3_ON`, **180** `SW_MER3_DONE`;
  armour **46** `AR_TABLE_KIT`; Map 14 events 33-40; `places.WYVERN_BACK`,
  `WYVERN_BACK_DOOR`, `WYVERN_BACK_TABLE`; faces `Gen_People13` **5-7**
  (Mother Grizel, Dr Hobday, Nan Gilly) and `Gen_People14` **0** (Mr Spence,
  the first cell of a new sheet), generated, settings in `build/characters/`.
  Nobody fights, so nothing goes on `AUDIT.md`.
* One trope, no blush. Running tally: **tropes +29 fixed and 2-9 from
  PIP-2; blushes +13 fixed and 0-1 from PIP-2.**
* `SW_STORY[MERRI]` (on already after any other of hers).
* **Candidate ending line** (G1; read `SW_MER3_DONE`): "Sister Merribell is
  to speak at the Healers' Table next year. She has nothing to tell them yet.
  She is writing it down."
* **The rooms (0.1):** the Wyvern was swept on 30 Sep and is unchanged
  inside its old bounds. The back room is new, screenshotted empty and with
  the Table sitting.
* **Scenario** `q_mer3`: passes (36 checks). The first run failed one check
  of its own - a last "nothing moved" delta measured from before the scene -
  and passes with a mark after it.
* `TIMELINE.md`: the four healers' ages.

**E4, ALD-3 The Chapter House - done.** ALD-3's section at the bottom of
`q_aldric.py`, hooked from `coldbarrow.py` in three places (Mordaunt, the
eight cells of the great map, the committee's two); the second picture drawn
by `coldbarrow.draw_map(aldric=False)`; `build/scenarios/q_ald3.json`.

* **The start is Mordaunt's second look** (Map 48 event 2, page 3: his A and
  Aldric). His first page with Aldric is the published "Where am I?" /
  "Frostwick, sir. And Fenmarch. And a lay-by in the west." / "The
  committee will write." On the second it is Thursday, and the committee
  will see him now.
* **Decided: the committee is Mordaunt**, "appointed to it four times", who
  sits in each of the four seats in turn and is quorate - so the empty
  chairs and stools of the site were never empty, and nobody new needs a
  face. Findings: nine pins; all nine correct; three the same week. "The
  committee has been unable to fault the pins. It has therefore had to
  fault the knight." / "Entirely fair." The request to REMAIN IN ONE PLACE,
  "Informed. In ink." - in six years of trying to leave Thistlewick nobody
  has once asked him to stay anywhere - and the offer: Knight Commander of
  the Chapter, a desk, here, a pin that does not move, contingent on
  remaining in one place.
* **The refusal**: "That is the finest thing I have been offered in nine
  years. Thank you." / "No." A knight who stays put is a post; Dame Winifred
  (Little Gore's white pin) is a very fine post, and happy, and he honours
  her; he would be at that desk by nine every morning "and I should never
  once find it twice". "But you asked. Nobody asks a man to stay. Put that
  in the minutes, would you? In ink." **One trope** (the guild that has lost
  your file - which has nine).
* **Decided: the rank is the answer to the data problem.** The knight cannot
  stay with the pin, so "Resolved: that the pin go with the knight." The
  nine red pins come out of the map, eight into the heap on the desk, and the
  ninth goes on his tabard: **Knight Errant, At Large**, a rank of the Order
  created this Thursday, and "wherever the knight is, sir, the map is
  correct. That is the system now." It is **Change Nickname** (code 324) on
  his actor, `Pemberton-Gore III` to `Knight Errant, At Large`, because the
  status screen's nickname is the one place a rank shows - what
  `COMPANIONS.md` calls "a proper rank", and what the ending's "somebody in
  this party finally got promoted" can read.
* **Afterwards for everybody**: Mordaunt ("Sir Aldric is wherever he is. He
  has the pin. The map is correct. That is the system." - with very few red
  pins left to move); the great map's eight cells, which show
  `Coldbarrow_Map_AtLarge` - the same map with the red pins out and the
  white ones where they were - and a card in the margin, PEMBERTON-GORE. AT
  LARGE. PIN CARRIED.; and the committee's table, CONCLUDED. Sir A.
  informed. Offered the Chapter. Declined. "Beautifully. (Minuted at his
  request.)"
* **Ids taken:** switch **181** `SW_ALD3_DONE`; `places.
  COLDBARROW_MAP_AT_LARGE`, `img/pictures/Coldbarrow_Map_AtLarge.png`. No
  faces, no items.
* One trope, no blush. Running tally: **tropes +30 fixed and 2-9 from
  PIP-2; blushes +13 fixed and 0-1 from PIP-2.**
* `SW_STORY[ALDRIC]` (on already after ALD-4 in a game that did it).
* **Candidate ending line** (G1; read `SW_ALD3_DONE`) - the Prophecy
  noticing a promotion: "Sir Aldric Pemberton-Gore the Third has been
  promoted, to Knight Errant, At Large. He carries his own pin. Wherever he
  is, the map is correct."
* **The rooms (0.1):** Coldbarrow had never been swept. Map 48 was cropped
  with `propsheet.py` (16 tiles) and screenshotted: `World Map` four abreast
  as the great map, the stained glass, `Armor A (Stand)` twice, the
  committee's `Table A` with two `Chair A (Wood)` and two stools, the desk
  with `Notes B` and the ledger, `Bookshelf A` the files. Everything is what
  its event says. Nothing needed fixing. `Coldbarrow_Map.png` was redrawn by
  the same run and is byte for byte what it was.
* **Scenario** `q_ald3`: passes (33 checks), the picture asserted by name
  through a spy on `showPicture`. Two earlier runs failed on the scenario,
  not the pages: twenty presses were too few for Mordaunt's published
  first page, and the great map's cell at x 7 is event 5.
* `TIMELINE.md`: nothing dated ("this Thursday" is not a year).

**E5, ALD-1 The Errand - done.** ALD-1's section of `q_aldric.py`, hooked
from `hamlets.py` in two places (Mrs Vane, the banns);
`build/scenarios/q_ald1.json`.

* **The start is the banns** (Map 50 event 8), which have no ladder and were
  built as this quest's set-up: with Aldric, their own page whole, and then
  INVITATIONS TO FOLLOW read over your shoulder. "...I am the invitations."
  Out of the tabard comes a letter, soft at the folds, nine years old: TO
  THE PARISH OF LITTLE GORE. BY HAND. P-G. His father gave it him the morning
  he rode out - four miles, your first errand, deliver it and then you may go
  errant. "I have been errant for nine years. I never delivered it." **The
  letter is item 68**, a key item, so the errand belongs to whoever carries
  it and a dismissed Aldric's waits.
* **The route is a choice, and the party should not correct him**: "Follow
  him" is the hundred and ten miles in three windows - the coast, which is
  lovely, a lay-by in the far west where he is fairly sure he has been
  before, Frostwick, the Fenmarch road twice in different directions both on
  purpose, and on the third evening over a rise a wooden house on a knoll -
  "THERE. Little Gore. Told you I knew the way." "Aldric, this is Little
  Gore" is shorter and a little sad: "...Is it? Oh. Oh, good. That is a
  great deal shorter." / "I should have liked to see the coast." Both end at
  "Mrs Vane's, then. The first house. One knocks, I believe." The lay-by and
  Frostwick are two of Mordaunt's three same-week pins, which nobody points
  out.
* **The delivery is Mrs Vane's** (event 3, page 3: her A, Aldric and the
  letter). He takes his helmet off, which nobody has seen him do. It is SIR
  ALDRIC PEMBERTON-GORE THE SECOND requesting the pleasure of the parish at
  the wedding of HESTER PLUMB AND THOMAS VANE, at Fenmarch. "...It's my
  wedding." All eleven came anyway, in the rain, because nobody had told
  them not to; now they are invited, properly, and it goes on the
  mantelpiece against the clock, with the good pin. He stands on the path
  with his hands empty: the first thing he has carried in six years that
  has got where it was going. Tea, and supper, since he may not find his way
  out. **One trope** (the quest that started it all). Mrs Vane's first page
  stays the published one, with Aldric or without - the site said "there is
  no reaction shot with Aldric in the party", and there still is not.
* **Afterwards for everybody**: Mrs Vane's own last page plus the invitation
  on the mantelpiece through the window; the banns' own page plus, under
  INVITATIONS TO FOLLOW, in a fresh hand, FOLLOWED. (P-G.)
* **Ids taken:** switch **182** `SW_ALD1_DONE`; item **68**
  `IT_ALD1_LETTER`. No faces, no new events.
* One trope, no blush. Running tally: **tropes +31 fixed and 2-9 from
  PIP-2; blushes +13 fixed and 0-1 from PIP-2.**
* `SW_STORY[ALDRIC]` (on already after ALD-3 or ALD-4).
* **Candidate ending line** (G1; read `SW_ALD1_DONE`): "Sir Aldric
  Pemberton-Gore delivered his first errand, nine years late, by a route of
  a hundred and ten miles. It is on a mantelpiece in Little Gore."
* **The rooms (0.1):** Little Gore had never been swept. Map 50 was cropped
  with `propsheet.py` (39 tiles) and screenshotted: the three houses, wood
  and green roofs, `Sign B` the banns' board, `Sign A` the fingerpost, the
  well, a barrel, a fallen log, flowers and trees. Everything is what its
  event says. Nothing needed fixing.
* **Scenario** `q_ald1`: passes (40 checks), first run - both routes (the
  letter taken back between them), the letter waiting without Aldric, the
  delivery, and afterwards without him.
* `TIMELINE.md`: 1991 gains the letter, his first errand, given the morning
  he rode out.

**E6, ALD-5 Pemberton-Gore the Fourth - done.** ALD-5's section at the
bottom of `q_aldric.py`; hooked from six place modules in one line each
(`q_aldric.with_follower` round the events list of Maps 1, 13, 48, 50, 54
and 61) and from `fenmarch.py` in three places (the world-map door, the
Fourth at home, the Third's portrait); `build/scenarios/q_ald5.json`.

* **Decided: it needs ALD-1**, as NIX-1 needs NIX-4. `COMPANIONS.md` says
  "placeable anywhere", and Fenmarch is the one place it cannot be: the
  world-map door refuses Aldric, so the Fourth has to come to him. The news
  goes the way everything between Little Gore and Fenmarch goes - Tom walks
  it every day - so once the letter is delivered the Fourth turns up at
  Little Gore (Map 50 event **10**, at (14,16) by the road), having found it
  first time. Without Aldric: "Is my uncle with you? Tom said he came HERE.
  Four miles! I found it first time."
* **The meeting** (with Aldric): "UNCLE." He was ten when his uncle went;
  the knight who went out and never came back is "our best one"; nine pins,
  Mordaunt says, three in one week (or, after ALD-3, "you're AT LARGE. That's
  a RANK. They made it up for you. On a Thursday."). He wants to squire: he
  can find gates. Aldric's face does several things at once, none of which
  it has had to do before, and he tells him: lost, for six years. "In
  Thistlewick. Mostly." / "I know." Grandfather said the Pemberton-Gores
  always go the long way round, and the long way round is still a way; and
  nobody else in the family ever went OUT - "They all came over the wall.
  You went OUT." It is not how Sir Aldric would describe the last six
  years; it is, he finds, true. "...Three paces behind, then. And you'll
  tell me if I'm facing the wrong way." / "You always are, uncle. It's on
  the arms." **One trope** (the prodigy successor).
* **"An appended page on Aldric everywhere afterwards in which somebody is
  following him"** (`COMPANIONS.md`). Aldric is not an event while he is in
  the party, so **decided: the Fourth is**, a few paces off the way in at six
  places Aldric goes - Thistlewick (17,3), Nether Sopping (18,3), the
  Chapter House (11,8), Little Gore (14,16, the same event he turned up as),
  Weeping Bottom (17,22) and Great Dunnage (19,26), `places.FOURTH_FOLLOWS` -
  on a page that needs ALD-5 done and Aldric in the party, with a line each
  ("Uncle says the north gate's just over there. I found it at once. I
  haven't said."; Mordaunt wrote down "here" and looked so pleased; Duchess
  knew him straight off, "I'm working on it"). Without Aldric each is a
  blank page, through and below characters, so nothing in any existing walk
  can touch it. **Map 1 event 31, Map 13 event 18, Map 48 event 16, Map 54
  event 19, Map 61 event 19**, each appended after every other event.
* **And Aldric can go home.** Fenmarch's world-map door (Map 8 events 62-63)
  keeps its three pages and gains a fourth, with Aldric and ALD-5 done: "Gate's
  just here, uncle. This way." He finds it first time, and Sir Aldric looks
  at the house, and at his nephew, "and does not look the other way" -
  "...Shall we go in?" - and the door's own transfer. In the gallery, the
  Third's portrait (Map 57 event 14) is its own page and then him in front
  of it: "I was going to come back. ...I have, rather." Mrs Puddifoot changes
  the flowers anyway. `fenmarch.py`'s docstring expected ALD-1 to append a
  page to the door as well; it turned out not to need one, and now says so.
* **Afterwards for everybody**: the Fourth at home (Map 57 event 2) - his own
  last page plus "He is a squire now. When his uncle is out, so is he, three
  paces behind; when he is home, he keeps the helmet clean."
* **Ids taken:** switch **183** `SW_ALD5_DONE`; the events above;
  `places.FOURTH_FOLLOWS`. No new faces - the Fourth was drawn for the site
  (`Gen_People5` 3).
* One trope, no blush. **Running tally at the end of E6: tropes +32 fixed
  and 2-9 from PIP-2; blushes +13 fixed and 0-1 from PIP-2.**
* `SW_STORY[ALDRIC]` (on already after ALD-1, which this needs).
* **Candidate ending line** (G1; read `SW_ALD5_DONE`): "Sir Aldric
  Pemberton-Gore the Third has a squire, who finds the gates. He has been
  home. He went the long way round, and it was still a way."
* **The rooms (0.1):** Fenmarch had never been swept. Maps 56-57 were
  cropped with `propsheet.py` (38 tiles) and screenshotted: the green roofs
  and chimneys, `Stone Pillar B (Moss)` the gateposts, the trees and
  mushrooms; in the gallery the cases and portraits (character sheets),
  `Planter A` the flowers under the Third, the clock, `Large Fireplace`,
  `Table C` and `Table D`, chairs and a stool. Everything is what its event
  says. Nothing needed fixing. The six followers stand on cells checked
  open on each map's passability, beside and not on the way in.
* **Scenario** `q_ald5`: passes (50 checks): the Fourth nothing before the
  letter and waiting without Aldric, the meeting, the five other followers
  present with Aldric and absent without, in at Fenmarch's gate, the
  portrait and the Fourth at home. Its first run failed one fragment of its
  own that spanned a line break. Two followers were also screenshotted
  (Thistlewick, and outside Great Dunnage's gate).
* `TIMELINE.md`: nothing new (the Fourth was ten in 1991 and is nineteen,
  which the ages table has).

**Rerun for E1-E6** (0.1): parsing every scenario's `query` and `goto` map
ids and grepping for the places' names finds **67** that walk a map this
part changed - because E3 widened Map 14, E6 put an event on Maps 1, 13 and
61, and E6 appended a page to Fenmarch's door on Map 8, and almost every
scenario walks one of those. That is the full suite, which waits for G1. So
the rerun was chosen by what each change can reach, and the reasoning is
here to be checked:
* **every site scenario for a map whose pages changed** - `hamlets` (Sump,
  Little Gore), `weeping_bottom` (the Sisterhouse, the queue), `coldbarrow`,
  `fenmarch` (the gallery and the world-map door) and `placeholder_doors`
  (it counts site door cells);
* **a sample of the Slain Wyvern**, for the widening and its eight new
  events: `tavern`, `reachable_sopping` (walks in with the arrow keys) and
  `q_rol3` (whose dinner events, 22-32, are the ones immediately before
  MER-3's);
* **each step scenario whose map a later step changed again**: `q_mer1`
  (Map 54, the Fourth in E6), `q_ald3` (Map 48, the same) and `q_ald1` (Map
  50, the same). `q_mer5`, `q_mer3` and `q_ald5` ran on their maps' final
  state.
* **Not rerun, and why**: the Fourth's events on Maps 1, 13 and 61 are a
  blank first page, through and below characters, until ALD-5 is done and
  Aldric is in the party, which no other scenario sets - nothing can walk
  into, collide with or trigger them. Fenmarch's door gains a page only on
  the same condition. Map 14's new events are blank and through except the
  back-room door, which is on a wall face and needs Merribell. Every old
  page on every map was compared byte for byte at each step.

**Ten of eleven passed first time** - `hamlets` 72, `weeping_bottom` 101,
`coldbarrow` 32, `placeholder_doors` 12, `tavern` 3, `reachable_sopping` 7,
`q_rol3` 18, `q_mer1` 52, `q_ald3` 33, `q_ald1` 40. **`fenmarch` failed one
check, and it was a count changed by design**: it asserts the world-map
door's page count, which ALD-5 took from three to four. The check now says
four, and its label says whose the fourth is. `fenmarch` then passed (76 checks).
The `weeping_bottom`, `hamlets` and `coldbarrow` reaction-shot assertions
(no queue, no diagnosis, no promotion) all still hold, because each of
those scenarios resets the owner's self switch before its companion pass,
and every quest page waits on the second look. Nothing is owed.


**E7, ALD-2 The Vigil - done.** ALD-2's section at the bottom of
`q_aldric.py`, hooked from `weeping_bottom.py` in two places (Sir Hamo, the
chapel); the fight in `db.build_vigil`; `build/scenarios/q_ald2.json`.

* **Decided: Weeping Bottom's chapel, not Coldbarrow.** It is the Order's
  chapel for the west, which the Sisters lend it, and the symposium has it
  at three in the afternoon while a vigil has it at night - so it needs
  nothing of MER-1, and the published locked door and the chairs set out
  facing one another are still true on the night. Coldbarrow's Chapter House
  "is not one", so it became two of his eleven wrong chapels ("It says
  CHAPTER HOUSE on the door. I thought it was being modest."), with a barn
  that had a weathercock.
* **The sponsor is Sir Hamo Tench**, the Order's knight in the field in the
  ward for fourteen years, and the start is his second look with Aldric (Map
  55 event 4, page 3: his A and Aldric), carrying his own last page; his
  first page with Aldric is the published salute and stays the first visit.
  **Decided: the shield has been over the chapel door for thirty years**,
  hung for the vigil Aldric was due at sixteen and kept somewhere else; the
  Sisters took the knight on it for a pun about vigilance. "...That's mine."
  "Tonight / Not yet" ("Thirty years. It'll keep till you're ready. So will
  I.").
* **The vigil** is leek soup from both halves (Recover All), Sir Hamo's key
  on a string under the nightshirt, the symposium's chairs watching, "From
  now. Not a word, Pemberton-Gore." - and **troop 53**, a defence battle in
  the chapel (battleback `Temple`, put back to the map's own after):
  * **Aldric keeps vigil**, state **41**: restriction 4, so he never gets a
    turn and cannot be commanded, and target rate x10, so he draws nearly
    everything aimed at the party. Substitute was the literal reading, and
    the engine only lets a battler who can move substitute, so the cover is
    the targeting. The scenario counts the hits: he took at least 70% of
    them. If he is fifth in the party he is brought to the front first.
  * **The things that come** hit for a share of the target's hit points, so
    it is the same fight at any level: **the Damp** (two, `Undine`, Seeps
    In, 8%), **the Small Hours** (`Siren`, 999,999 hit points - "cannot be
    fought, only got through" - humming How Late It Is, a sleep), **a Small
    Temptation** (`Petitdevil`, from turn 2, Suggests Sitting Down, 6%) and
    **a Light Going Away** (`SF_Will_o_the_wisp`, from turn 3, THIS WAY,
    12%: "Sir Aldric has followed every light in the valley. He does not
    follow this one."). None was used by any enemy before. The killable
    three are sized to the party, as the contest's acts are.
  * **The only win is the dawn**: a troop page at the end of turn
    `VIGIL_DAWN` (5) kills whatever is still in the chapel. **If he falls,
    the vigil is broken** - a troop page aborts, which Battle Processing
    reports as an escape, and the party cannot run; if everybody falls it is
    lost, and the Sisters put you to bed on the line so both halves can
    treat you. Either way, Recover All, and Sir Hamo: "Took me four goes...
    The chapel's not going anywhere. Nor am I." It waits.
* **Confirmed**: "Thirty years late. The Order's never minded late. It minds
  wrong chapels." Regardant is looking back, to see who is behind him -
  "That's the whole of the Order. You don't lead. You look round, and you
  see who's bleeding, and you go and stand in front of them." / "...I always
  thought I was facing the wrong way." / "You were facing your friends." -
  which is the family arms, ALD-4's saddle, ALD-5's squire and his class, said
  once. With ALD-5 done, the Fourth has kept the door all night, facing the
  right way. He has not said anything for eleven hours, and does not now.
  **One trope** (the night watch).
* **Aldric's gear** (0.5): armour **47** "Shield (Regardant)", a shield of a
  new armour type **13, "Escutcheon"**, which his actor has a trait for -
  the badge pattern, in the shield slot. MHP +60, DEF +40, MDF +24, LUK +6,
  guard x1.3, and **substitute**: he covers whoever is bleeding without
  being asked, now always and not only while Interposing.
* **Afterwards for everybody**: Sir Hamo's own last page plus a letter to
  Coldbarrow on the blanket, IN THE FIELD. CONFIRMED: ONE. (PEMBERTON-GORE.)
  FIRST IN THIRTY YEARS. - and with Aldric, "Anybody behind you, Sir
  Aldric?" / "Always."; the chapel's own page plus the paler patch over its
  door, the shape of a shield.
* **Ids taken:** switch **184** `SW_ALD2_DONE`; armour **47**
  `AR_REGARDANT`, armour type **13** `AT_ESCUTCHEON`; state **41**
  `ST_VIGIL`; enemies **55-58**; troop **53**; skills **179-182**. No
  faces, no new events, nothing for `AUDIT.md` (stock art). **Fixed on the
  way:** two of the first names chosen, `EN_WISP` and `SK_LULLABY`, were
  already `db` constants (the Gloamwood's wisp, Piper's lullaby) and
  rebinding them moved two old troops and a learning - the data diff showed
  it, and they are `EN_LIGHT` and `SK_HOW_LATE`.
* One trope, no blush. Running tally: **tropes +33 fixed and 2-9 from PIP-2;
  blushes +13 fixed and 0-1 from PIP-2.**
* `SW_STORY[ALDRIC]` (on already after ALD-1, -3, -4 or -5 in a game that
  did one).
* **Candidate ending line** (G1; read `SW_ALD2_DONE`): "Sir Aldric
  Pemberton-Gore the Third kept his vigil in the right chapel, thirty years
  late, and did not move until it was light. The knight on his shield is
  looking back, to see who is behind him. Somebody always is."
* **The rooms (0.1):** Weeping Bottom was swept in E2; nothing drawn, and the
  fight was screenshotted in the chapel.
* **Scenario** `q_ald2`: passes (30 checks), fought for real on
  auto-battle, three times: broken (Aldric felled at frame 300), lost
  (everybody felled) and kept to dawn - won at the end of turn five and not
  before, the temptation and the light both came in, and he took 15 of the
  16 hits aimed at the party. Its first run failed only its own last step,
  a look at the fight that killed the party for the shot and never pressed
  through the defeat; the shot is now taken first.
* `TIMELINE.md`: 1970, the shield over the door and the first wrong chapel;
  Aldric's age, forty-six.


**E8, ALD-6 The Wrong Dragon - done.** ALD-6's section at the bottom of
`q_aldric.py`, hooked from `nomap.py` (the cave, in a wrapper like the
lake's); `build/scenarios/q_ald6.json`.

* **The start is the cave's second look with Aldric** (Map 8 event 53, page
  3: its A and Aldric), with the site's own "Call in / Press on". The
  published first stop says "a young knight, oh, eight years ago. Very
  correct." with Aldric standing in the cave or not, and stays the first
  visit word for word - which is a better joke than anything a reaction
  shot could add, and the scenario asserts it.
* **Decided: Horace was the horse.** He only ever called her Horse (ALD-4),
  so eight years ago one of them talked about a grey mare for four hours and
  the other about the Odes, and both had a lovely time. "And how is
  Horace?" - with ALD-4 done, "She's a partner in a haulage firm, at Great
  Dunnage. Not Tuesdays"; without, "I lost her, I'm afraid" - "...Horace is
  a poet, dear. Roman. The Odes." / "I thought we were talking about my
  horse." / "For four hours?" / "She's a very good horse." / "I did wonder
  why the Odes had so much in them about oats."
* **The right dragon was slain by somebody else, offstage**, as
  `COMPANIONS.md` has it - "He drinks in the Slain Wyvern. He's insufferable
  about it, I hear." Nobody new was drawn for him: the Wyvern is full, and a
  bore is funnier described than met. So the commission, out of the tabard
  (DRAGON, ONE. TO BE SLAIN.), has nothing left to slay: "You've a dragon. In
  the sense that the map says so." / "I couldn't. You lent me a book." - which
  he has not finished, because he keeps losing his place.
* **The scene in the light keeps the subject closed** - decided against
  asking Mike for a lit image. It wants reading to ("My eyes aren't what they
  were. It's why I talk so much."); Aldric lights the lamp (a warm tint, put
  back after); the light shows books to the roof, a blanket with ducks on it
  and reading spectacles the size of cartwheels, "and the rest of it, which
  you look at for a long moment, and decide you will not describe to
  anybody. Sir Aldric does not describe it either." `SITES.md` and
  `NORTH.md` 1.3 closed what it is, and a picture would open it; its face
  stays Mike's silhouette. `AUDIT.md`'s "Wrong Dragon, lit" row is answered
  so. The Odes are not about oats. **His report**, on the back of the
  commission, the first in eight years: DRAGON: FOUND. NOT SLAIN. READ TO.
  P-G. "Come again, dear. Bring the horse." **One trope** (the dragon). No
  item: `COMPANIONS.md` gives "the game's only dragon, uneaten", and that is
  the reward.
* **Afterwards for everybody**: the cave with a lamp lit in it now; "It's
  the Odes. A young knight reads them to me, when he can find the way" -
  "He usually can't. I keep the lamp lit."; with Aldric, he finds the way,
  first time, and takes the book down, and nobody remarks on it.
* **Ids taken:** switch **185** `SW_ALD6_DONE`. No faces, no items, no new
  events.
* One trope, no blush. Running tally: **tropes +34 fixed and 2-9 from PIP-2;
  blushes +13 fixed and 0-1 from PIP-2.**
* `SW_STORY[ALDRIC]` (on already after any other of his).
* **Candidate ending line** (G1; read `SW_ALD6_DONE`): "Somewhere in the
  rocks above the water there is the only dragon in the valley, uneaten. A
  knight reads it the Odes, when he can find the way."
* **The rooms (0.1):** the cave is a world-map cell (Cave B, open from the
  north) and nothing was drawn.
* **Scenario** `q_ald6`: passes (15 checks), first run - walked onto the
  cell for the published first stop with Aldric, Press on, the visit with
  ALD-4 undone and then done (the switch put back between), the tint put
  back, and afterwards with and without him.
* `TIMELINE.md`: 1993, the right dragon slain by somebody else.


**E9, WRE-4 The Cabinet - done.** WRE-4's section at the bottom of
`q_wren.py`, hooked from `fenmarch.py` in two places (Mrs Puddifoot, Mr
Ottershaw); `build/scenarios/q_wre4.json`.

* **Decided: Mrs Puddifoot asks.** The Marsh Bear's case has Wren's
  published "Not unless I'm asked.", and somebody had to. The family is the
  Fourth, but ALD-5's afterwards page is on him, so the owner is the
  housekeeper who dusts all eighty, Friday to Wednesday: her second look with
  Wren (Map 57 event 3, page 3: her A and Wren), carrying her own last page.
  "You're a naturalist. A proper one. With the jars." The Fourth is across
  the gallery before she has finished, and speaks from where he stands: "Three
  generations we've been proud of them. Dr Rowbotham named the bear!" / "He
  named everything. That was the problem." `SW_WRE4_ON`.
* **Mr Ottershaw shows her the joins** (event 4, page 3: his A, Wren and the
  engagement): "Seventy years. Nobody has ever ASKED." The Marsh Bear (bear
  to the waist, crab below - the crab end came for the crayfish), the
  Phoenix (a salamander, and the top of something that fell in Cook's fire),
  the Horse (crab and unicorn: the plate is blank because nobody liked to ask
  what it was) - each one what `fenmarch.SEWN` actually drew. She finds each
  join only once he has put his finger on it. `SW_WRE4_JOINS`.
* **Decided: the composite that is real is case forty**, the Home Farm's
  unicorn that "kept the foxes down" - drawn as a wolf and a unicorn, and
  the one case whose plate already says it was bred at Fenmarch. He walks
  past it "the way you go past a door you don't open"; she looks at the
  shoulder and the horn for a long time; there is no join; she writes
  nothing. Nobody says it is real.
* **The write-up**, read back at Mrs Puddifoot's: eighty cases, seventy-nine
  composed by Mr J. Ottershaw, none what its plate says, not one ever lived;
  "The joins are the finest work I have seen... I could not find these
  without being shown, and then I could not stop looking at them. Case
  forty: not examined." - honest, and silent on the one thing. "...None of
  them?" / "None of them. I'm sorry." Then: "COMPOSED. By Mr Ottershaw.
  Nobody else in the county has a COMPOSER... That's better than real.
  Anybody can have real." The fee, **600 crowns**, from a tin on the
  mantelpiece (`db.WRE4_FEE`); "Nobody has ever been pleased with a write-up
  of mine... I'm not sure what to do with my face." **One trope** (the
  nobleman's collection). No gear - Wren has her badge.
* **Afterwards for everybody**: Mrs Puddifoot's own last page plus the
  write-up framed over the fire, dusted first, before the cases; Mr
  Ottershaw's plus a copy pinned over his bench with "finest" underlined
  twice.
* **Ids taken:** switches **186** `SW_WRE4_ON`, **187** `SW_WRE4_JOINS`,
  **188** `SW_WRE4_DONE`; `db.WRE4_FEE`. No faces, no items, no new events.
* One trope, no blush. Running tally: **tropes +35 fixed and 2-9 from PIP-2;
  blushes +13 fixed and 0-1 from PIP-2.**
* `SW_STORY[WREN]` (on already after WRE-1, -2, -3 or -5 in a game that did
  one).
* **Candidate ending line** (G1; read `SW_WRE4_DONE`): "The Fenmarch
  Collection has been authenticated by W. Halloway: seventy-nine composed,
  the finest joins she has seen. The family has never been prouder. Case
  forty was not examined."
* **The rooms (0.1):** the gallery was swept in E6 and is unchanged.
* **Scenario** `q_wre4`: passes (24 checks), first run - both owners'
  published first visits with Wren, the engagement, the wait, a dismissed
  Wren's errand waiting at Mr Ottershaw, the joins and case forty, the
  write-up and the fee, and afterwards with and without her.
* `TIMELINE.md`: nothing new (Ottershaw's 1930 is already there).


**E10, COR-3 The Rivals' Retreat - done.** COR-3's section at the bottom of
`q_corvin.py`, hooked from `sable_hart.py` in four places (Crake, the
league table, the newsletter, the empty table);
`build/scenarios/q_cor3.json`.

* **The start is the league table** (Map 49 event 8), which has no ladder
  and no published reaction shot, and which the site built to stop at fourth
  for this: with Corvin, its own page, and then he takes out the fifth pin
  and reads the rest - 5. K. BLACKWOOD 12 (keen), 6-16 members by post,
  **17. C. ASH 0 (no meetings attended)**. "Seventeenth. Of seventeen.
  Behind Blackwood. Blackwood is NEW." He takes it very hard, and sits down
  at the nearest table, which is the empty one in the middle, in the light.
  Across the room Crake opens his book. **One trope** (the dark mirror,
  again - the site's was Crake's). `SW_COR3_ON`.
* **Decided: the fix is a meeting**, because points are scored at meetings
  and he has sent apologies to a hundred and twelve (the newsletter's issue
  number). Crake convenes it on his second look with Corvin and the switch
  (event 2, page 3: his A, Corvin, `SW_COR3_ON`), carrying his own last
  page; his first page with Corvin is the published "I'm not here." and
  stays the first visit. "Quorum is two. We are five, and a member." Rook
  reviews: a vow (a fortune-teller, twopence - "A vow you paid for. That's
  binding. Two points."); a scar (no - "Don't ask about the scar", and
  Veyle looks very briefly disappointed); standing in the rain - "I sat in
  the corner of the Slain Wyvern. For eleven years." / "...In ONE corner?" /
  "Out of turn?" / "There wasn't a rota." Nobody has ever sat in one corner
  for eleven years; is there a category? "There is now." "Front page."
  Blackwood would like that category one day, when he has a corner.
  **Second, thirty-nine, behind the scar**; Rook moves himself down to
  fifth and is visibly happier there. Veyle offers the dark corner out of
  turn; NOBODY out of turn, however rainy.
* **Decided: the chair the newsletter keeps is not a corner.** It is the
  stool he sat down on, in the middle of the room, in the light, where
  nobody broods - somebody has dusted it, "and it does not look as if it
  has been easy". "...It's a very good chair." Mrs Garrow brings him a pie
  and he stays for it (the tinker, in her own page, left before his came).
  Nobody uses the word for what this is. No gear, no item: Corvin has his
  scarf.
* **Afterwards for everybody**: Crake's own last page plus "Mr Ash attends
  now. Not every week. He sends apologies when he doesn't. We find it very
  reassuring."; the table's own page plus the rota moved up an inch and two
  new lines in red, 2. C. ASH 39 (one corner, eleven years) and 5. T. ROOK
  35 (by his own request); the newsletter's own page plus issue one hundred
  and thirteen, PRESENT: C. ASH; the empty table, one stool dusted, KEPT.
  (C. ASH.) - and with Corvin, he sits on it for a minute and does not brood
  at all.
* **Ids taken:** switches **189** `SW_COR3_ON`, **190** `SW_COR3_DONE`. No
  faces, no items, no new events.
* One trope, no blush. Running tally: **tropes +36 fixed and 2-9 from PIP-2;
  blushes +13 fixed and 0-1 from PIP-2.**
* `SW_STORY[CORVIN]` (on already after COR-1, -2 or -5 in a game that did
  one).
* **Candidate ending line** (G1; read `SW_COR3_DONE`): "Corvin Ash is second
  on the league table at the Sable Hart, behind a scar. He has a chair there,
  in the middle of the room, in the light. He attends."
* **The rooms (0.1):** the Sable Hart had never been swept. Map 49 was
  cropped with `propsheet.py` (23 tiles) and screenshotted: `Large Window A`
  over Crake's corner, `Curtains B` over Veyle's (no window behind it, as he
  says), `Open Book A` on Rook's table and `Notes D` on Morrow's, two
  `Posted Notice`s for the table and the rota, the `Large Fireplace`, the bar
  with `Bottle Shelf A`, `Wine Rack` and the `Bell`, `Pint Mug C`s in the
  corners, and the middle's two `Table A`s and four `Stool A`s. Everything
  is what its event says. Nothing needed fixing.
* **Scenario** `q_cor3`: passes (24 checks), first run - Crake's published
  reaction shot, the table as published without Corvin and still stopping
  at fourth, then his seventeenth (and not twice), a dismissed Corvin's
  errand waiting at Crake, the meeting, and afterwards with and without
  him.
* `TIMELINE.md`: nothing dated (eleven years is 1989's).


**E11, COR-4 Mother Selvidge - done.** COR-4's section at the bottom of
`q_corvin.py`, hooked from `nomap.py` (the Fair, one line in its own
builder); `build/scenarios/q_cor4.json`.

* **The start is the Fair's second look with Corvin** (Map 8 event 54, page
  3: its A and Corvin), with its own "Go to the fair / Press on". Its A is
  set only when Mother Selvidge is paid, so a party that never crossed her
  palm has never sat at her booth and this waits until they have - the
  ladder's terminal, as 0.2 says. The published reading ("somebody is going
  to be very surprised to see you"), with Corvin standing in the tent or
  not, stays the first visit word for word.
* **Three readings, two crowns.** "Eleven years ago. Two crowns. You told me
  I was the rival of a great hero." / "Did I, dear? I dare say I did." The
  first is paid, as for anybody, and refused on credit ("The cards don't do
  credit"); the second and third are free, because her own second page says
  "Same again? ... Keep your money." A long life, a useful trade, something
  with his hands, no destiny whatsoever. "...Again." The same. "Again."
* **The third reading has no mysticism in it**: she puts the cards down and
  folds her hands on them "the way your aunt would" - she says the rival
  thing to about four young men a year, lads at nineteen sat in a heap,
  because it is the reading that makes them stand up straight, "and it has
  never once been wrong. They all went and did something." / "I sat in a
  corner. For eleven years." / "And then you got up. Look at you. You're
  stood in a fair a long way from anywhere with your friends." Nobody tells
  him he is nothing. **One trope** (the prophecy that made him).
* **Gives nothing** (`COMPANIONS.md`): he thinks about taking the long black
  coat off, and keeps it. "It is a very good coat." The scenario asserts no
  item and two crowns, once.
* **Afterwards for everybody**: the tent, and in front of her booth a young
  man in a hat who has just been told something and is standing up very
  straight; her own "Same again? ... Keep your money." if you go in.
* **Ids taken:** switch **191** `SW_COR4_DONE`. No faces, no items, no new
  events.
* One trope, no blush. Running tally: **tropes +37 fixed and 2-9 from PIP-2;
  blushes +13 fixed and 0-1 from PIP-2.**
* `SW_STORY[CORVIN]` (on already after any other of his).
* **Candidate ending line** (G1; read `SW_COR4_DONE`): "Mother Selvidge has
  read Corvin Ash three times. A long life, a useful trade, no destiny
  whatsoever. She has never once been wrong."
* **The rooms (0.1):** the Fair is a world-map cell; nothing drawn.
* **Scenario** `q_cor4`: passes (13 checks), first run - walked onto the
  cell for the published reading with Corvin there, Press on, one crown and
  no credit, then the three readings for two crowns, and afterwards with
  and without him.
* `TIMELINE.md`: nothing new (nineteen and eleven years are 1989's).


**E12, PIP-4 The Elegy - done.** PIP-4's section at the bottom of
`q_piper.py`, hooked from `hamlets.py` (the fingerpost, and seven owners in
Little Gore and Sump) and `fenmarch.py` (four owners), one line each;
`build/scenarios/q_pip4.json`.

* **Decided: Little Gore, and the man is Abel Thrush**, the carrier, who
  walked Little Gore - Fenmarch - Sump with the post every day for fifty
  years and died in the spring of 1991; Tom walks the Fenmarch half now. E1
  had already said PIP-4 should be Little Gore's - every Sump owner was
  MER-5's - and a carrier is the one man all three places would each have
  known differently. Nobody had to be dead recently: Mrs Vane's published
  pages are cheerful, and stay so.
* **The commission is a card nailed to the back of the fingerpost** (Map 50
  event 9, which has no ladder), "where nobody reads but a chronicler":
  with Piper, its own page and then WANTED: AN ELEGY. For ABEL THRUSH,
  carrier, who walked this road fifty years and never had one. Something
  with a bit of a tune. The parish will pay. Ask anybody. "Piper Quill has
  never met Abel Thrush. Piper Quill will have to ask anybody." **One
  trope** (the tragic backstory of the NPC you never met). `SW_PIP4_ON`
  (ends). After that the post shows the count, `\V[26]` of eleven.
* **The eleven, and none of them the same man**: Mrs Vane (a year of Tom's
  letters, never once read one, knew); Tom (never stopped talking, four
  miles each way - "I talk the whole way now. Somebody has to."); Dame
  Winifred (waved at eight every morning for two years, never said one
  word); Bess (Gran says he was a giant, carried a cow to Fenmarch); Alfie (a
  two-finger whistle you could hear at Sump); Nell (in weddings she is him
  sometimes - round the green, and say POST); Mrs Puddifoot (over the wall
  every day for fifty years, never used the gate, like family); Mr Ottershaw
  (every heron he found dead on the road, wept over each); the Fourth (he
  said he came in by the gate every day); Mr Gammage (a bottle of Fenmarch
  water on Sump's well every Tuesday for forty years, and nobody drank it);
  Mrs Pardew (a terrible man for his tea, all day to do four miles). Piper
  writes each one down; it does not agree with anything else in the book;
  she underlines it.
* **Decided: the interview pages carry whatever would have shown.** Five of
  the eleven already have other quests' pages - Mrs Vane ALD-1's, Dame
  Winifred HOB-1's, the Fourth ALD-5's, Mrs Puddifoot and Mr Ottershaw
  WRE-4's - and an appended page beats them all. So `q_piper._pip4_carry`
  rebuilds `Game_Event.refresh`'s choice inside the page, as a chain of
  Conditional Branch scripts over that event's own pages (switches, self
  switches, variable, item, actor), and then the interview. The page needs
  Piper and `SW_PIP4_ON`, and the owner's A where the owner has a ladder;
  `SW_PIP4_ON` goes off when the elegy is written, so nothing is shadowed
  afterwards. Heard is the owner's self switch **D** (free on Maps 50, 51,
  56 and 57), counted in `VAR_PIP4_HEARD`, so a dismissed Piper's count
  waits. The scenario checks ALD-1's and HOB-1's afterwards pages are carried
  through.
* **The elegy is nine lines**, written at the foot of the post out of the
  contradictions rather than resolving them, and not performed: "She does
  not stand on anything. She does not read it out." She pins it under the
  Fenmarch arm.

      He never spoke a word. He never stopped.
      He came in at the gate. He climbed the wall.
      He read no letter, and he knew them all.
      He carried a cow, and wept over a bird.
      He brought the water nobody would drink,
      and stopped for tea, and was at eight each day
      where somebody looked up to see him wave.
      Eleven people knew him. All are true.
      The road is four miles long. He walks it still.

  Little Gore reads it one at a time all afternoon. "It's him. All of him.
  Every one of us is in it." / "...We did wonder whether it might have a bit
  more of a tune." Piper laughs, out loud, about her own work, which nobody
  has heard her do: "Next time." **No blush** - this is the Register B one,
  and nothing in it is at anybody's expense. **Item 69**, Elegy (Nine
  Lines), her copy.
* **Afterwards for everybody**: the fingerpost's own page plus the nine lines
  under a little roof somebody has made for them, which people stop and read
  on their way past; with Piper, she does not read it again.
* **Ids taken:** switches **192** `SW_PIP4_ON` (ends), **193**
  `SW_PIP4_DONE`; variable **26** `VAR_PIP4_HEARD`; item **69**
  `IT_ELEGY`. No faces, no new events.
* One trope, no blush. **Running tally at the end of E12: tropes +38 fixed
  and 2-9 from PIP-2; blushes +13 fixed and 0-1 from PIP-2.**
* `SW_STORY[PIPER]` (on already after PIP-2, -3 or -5 in a game that did
  one).
* **Candidate ending line** (G1; read `SW_PIP4_DONE`) - one of the game's
  two best lines is the elegy's last, so the ending can quote it: "On the
  back of the fingerpost at Little Gore there are nine lines by Piper Quill,
  which she has never performed. The road is four miles long. He walks it
  still."
* **The rooms (0.1):** Little Gore was swept in E5, Sump in E1 and Fenmarch
  in E6; nothing drawn.
* **Scenario** `q_pip4`: passes (42 checks), first run - the card with
  Piper and the post without her, the count, all eleven across four maps
  with Mrs Vane carrying ALD-1's afterwards and Dame Winifred HOB-1's,
  not twice, a dismissed Piper's errand waiting at Mr Ottershaw, the nine
  lines, and afterwards for everybody with every owner back on their own
  page.
* `TIMELINE.md`: 1941, Abel Thrush starts the round; 1991, he dies, and the
  card goes up.


**Rerun for E7-E12** (0.1): parsing every scenario's `query` and `goto` map
ids and grepping for the places' names finds eighteen that walk a map this
part changed (Maps 8, 49, 50, 51, 54, 55, 56 and 57). Four of them are this
part's own and ran on their maps' final state (`q_ald2`, `q_cor3`, `q_cor4`,
`q_pip4`). The other fourteen were run again, alone and with no timeout:
* **every site scenario for a map whose pages changed** - `weeping_bottom`
  (Sir Hamo's first visit with Aldric is still the published salute, and its
  companion pass still asserts nothing of a vigil), `fenmarch`, `sable_hart`
  (Crake's reaction shot, and the table stopping at fourth without Corvin),
  `hamlets`, `nomap` (the cave and the Fair), `supplied_faces` (Somebody
  Large in the cave) and `placeholder_doors` (it counts the world map's
  site doors);
* **each step scenario whose map a later step changed again** - `q_ald1`
  and `q_hob1` (Map 50, where PIP-4 appended to Mrs Vane and Dame
  Winifred), `q_mer5` (Map 51, Mr Gammage and Mrs Pardew), `q_ald5` (Maps 50
  and 57), `q_mer1` (Map 54, E7's chapel), `q_wre4` (Map 57, PIP-4's three)
  and `q_ald6` (Map 8, the Fair in E11).
* **Not rerun, and why**: the rest of Map 8's scenarios walk the world map
  past two events whose new pages need Aldric or Corvin and their quest's
  own switches, which no other scenario sets; and every old page on every
  map was compared byte for byte at each step.

**All fourteen passed first time**, with no check changed: `weeping_bottom`
101, `fenmarch` 76, `sable_hart` 45, `hamlets` 72, `nomap` 44,
`supplied_faces` 6, `placeholder_doors` 12, `q_ald1` 40, `q_mer5` 74,
`q_ald5` 50, `q_mer1` 52, `q_wre4` 24, `q_ald6` 15, `q_hob1` 81. Every
reaction-shot assertion still holds because every new page waits on a second
look, a quest switch, or both. Nothing is owed.

**E13, PIP-1 The Authorised Version - done.** PIP-1's section at the bottom
of `q_piper.py`, hooked from `village.py` in two places (Ambrosine, the Wall
of the Forty-Seven); `build/scenarios/q_pip1.json`.

* **Ambrosine Quill is a new event in Prophecy Hall** (Map 3 event **12**,
  `village.AMBROSINE` (7,12)), at the Committee's paperwork table by the
  door, in the Quills' crimson. Empty first page; there **with Piper once the
  road has been walked** (`SW_LEFT_VILLAGE`, as PIP-2) - she started "the
  morning they voted", and it is finished while you are away. The Committee
  approved it on Tuesday. "He hasn't finished yet." / "The shape has, dear."
  **One trope** (the rival chronicler). `SW_PIP1_ON` keeps her there for
  everybody, so a dismissed Piper's errand waits: "Where is my niece? I have
  a question about a rhyme."
* **The document**, read in four cantos of twelve: THE LAY OF THE
  FORTY-EIGHTH, by A. Quill, Chronicler to the Committee, APPROVED. Canto one,
  an orphan boy "who never knew a mother's care" (his mother is at home,
  making a pie - "Nobody goes north with a mother. It doesn't scan."); canto
  four, the wolf ("Your grandmother had a wolf in numbers forty-one,
  forty-two and forty-three. The same wolf."); **canto six, the good middle**
  - "Nobody does the middle" - and Piper, after a moment: "...It is a good
  middle."; canto nine, Merribell dies by a holy well. With Merribell in the
  party she asks what she died of ("It doesn't say, dear. It scans." / "I'd
  have had a glass of water and sat down."); without, Piper has it noted she
  is alive. Bram reads all twelve again looking for a turnip. There is not one.
* **Decided: three answers, two endings** (`COMPANIONS.md`: "fight it, or fix
  it, or - the choice worth building - read it, and find it very good").
  **Fight it** ends nothing: a letter to the Committee, which approved it,
  carried across the hall to the Clerk, who files it under 'no change' - his
  own published line - and the choice is put again next visit. **It's very
  good** (`SW_PIP1_GOOD`): Piper looks at you as if you had hit her, reads
  canto six again, and agrees; Ambrosine takes her spectacles off - "Four
  generations. The Committee approves. It doesn't read. Nobody has ever said
  that before." Bram would like a copy for his mother, who is in it, briefly,
  in the past tense. One footnote, in small type: "None of this happened. It
  is very good. - P.Q." **Fix it** (`SW_PIP1_FIXED`): the afternoon, in metre,
  and Ambrosine fights for the wolf for an hour; **the wolf becomes the goat
  that sent its apologies to the meeting at which Bram was Chosen** (the
  Committee Records' published line) - "A goat is a sort of wolf. If you
  squint." Four fixed cantos (a mother with a pie; the goat, "and that is how
  a record's made"; the middle, wet, and no rhyme for turnip; Merribell, who
  did not fall, and socks); "The middle is worse." / "The middle is true." /
  "...It scans. Just." Signed A. QUILL and P. QUILL, the first account with
  two Quills on it, and the Clerk stamps it AMENDED. Both ends give **item
  70**, The Authorised Version, set `SW_PIP1_DONE` and her story.
* **No gear** (Piper has the rosette) and **no blush**: nothing in it is a
  Register A moment.
* **Afterwards for everybody**: Ambrosine on her ending - the good middle
  read most mornings, and the footnote; or A. and P. Quill, with a goat in it
  that is in the minutes - and with Piper, the two nod "as one professional
  to another, which is new". **The Wall of the Forty-Seven** (event 6, one
  page, no ladder, nobody else's afterwards) gets its own page plus a card in
  the space under the forty-seventh: ACCOUNT BY A. QUILL. APPROVED., and a
  footnote; or A. AND P. QUILL. AMENDED., and a goat in the margin.
* **Ids taken:** switches **194** `SW_PIP1_ON`, **195** `SW_PIP1_GOOD`, **196**
  `SW_PIP1_FIXED`, **197** `SW_PIP1_DONE`; item **70** `IT_AUTHORISED` (icon
  189, the open book); Map 3 event 12; `village.AMBROSINE`; face
  `Gen_People14` **1** (Ambrosine, generated: Piper's purple, up in a bun,
  spectacles, the crimson high collar; `build/characters/ambrosine-quill.json`).
  She does not fight, so nothing goes on `AUDIT.md`.
* One trope, no blush. Running tally: **tropes +39 fixed and 2-9 from PIP-2;
  blushes +13 fixed and 0-1 from PIP-2.**
* `SW_STORY[PIPER]` (on already after PIP-2, -3, -4 or -5 in a game that did
  one).
* **Candidate ending lines** (G1; read `SW_PIP1_GOOD` / `SW_PIP1_FIXED`):
  good - "The official account of the Forty-Eighth is by Ambrosine Quill, and
  it is very good. Bram is an orphan in it, and there is a wolf. It has one
  footnote, by P. Quill: none of this happened."; fixed - "The official
  account of the Forty-Eighth is by A. and P. Quill. It is true, and it
  scans, and where the wolf was there is a goat, which is in the minutes."
* **The rooms (0.1):** Prophecy Hall was swept on 30 Sep; cropped again with
  `propsheet.py` (17 tiles) and screenshotted, and it reads right - nothing
  changed. Ambrosine was screenshotted at the table by the scenario.
* **Scenario** `q_pip1`: passes (24 checks): absent alone and before the
  road, the reading with Merribell, Fight it (filed, nothing ends), the wait
  without Piper, It's very good, the switches put back, Fix it, and
  afterwards with and without Piper on both endings, with the Wall. Its first
  run failed only its own screenshot path.
* `TIMELINE.md`: nothing dated ("forty-one, forty-two and forty-three" are
  portrait numbers, already the grandmother's; Tuesday is not a year).


**E14, NIX-3 Professional Courtesy - done.** NIX-3's section at the bottom
of `q_nix.py`, hooked from `south.py` in four places (Lorrimer at the Guild,
Lorrimer on the front, three shut doors, Sops); `build/scenarios/q_nix3.json`.

* **Decided: Nether Sopping, and the Adventurers' Guild.** `COMPANIONS.md`
  wants "a room in an existing town"; Lorrimer's complaint is that Nix's
  words make thieving sound "like a job somebody has failed to apply for",
  so he is at the one place in the valley where you apply for jobs -
  registered, "Pell's got me down under T." **Cobb Lorrimer** is a new event
  (Map 15 event **7**, `south.LORRIMER_GUILD` (14,8)), empty except with
  Nix: LOCATES. AHEAD OF SCHEDULE. THE CLIENT. "It's stealing with a
  waistcoat on." **One trope** (the rival thief). `SW_NIX3_ON` (ends).
* **Decided: the client is Sops and Tibb**, the two children on the front
  who play Chosen One and cannot find anybody to be the Dark Lord (their
  published pages). Their list, in a child's hand: ONE ROPE. ONE HELMIT.
  ONE SWORD. ONE DARK LORD (WHO LOSES). A client, a list and an afternoon;
  no fighting - "I'm a professional." / "So am I."
* **Nix locates three, with permission, at three of the town's shut doors**
  (Map 13 events 13-15, one page each, no ladder), each a page with Nix and
  the switch carrying the door's own page: **the Net Loft**, whose card has
  said THE ROPE IS SPOKEN FOR since the game was built - spoken for by
  whoever asks properly, and nobody ever had; **the front door nobody
  answers**, waited at for an hour ("It is most of locating") for the pot
  with a dead thing in it, which is a helmet - "Keep the dead thing an'
  all"; and **the boat shed**, which Nix could open in four seconds and does
  not: the Ferryman, who keeps the key, offers an oar off one of the eleven
  boats - "She'd like being a sword." Located is each door's self switch A,
  counted in `VAR_NIX3_LOCATED`, so a dismissed Nix's list waits.
* **The judging is on the front** (Map 13 event **19**, `south.
  LORRIMER_FRONT` (26,19), beside the children; ahead of Nix he "had mine
  before dinner"). His three are a rope off the ferry, a helmet out of the
  outfitters' window and the very good sword off the knees of the man
  having a day off, who has come up the street after it in his socks. "Mum
  says we're not to have stolen things." Nix's three have receipts - "This
  one's got PAPERWORK" - and his go back to their owners, politely. "You
  can't win a THIEVING contest on PAPERWORK." / "It wasn't a thieving
  contest. It was a list." **The fourth cannot be stolen, so Nix locates
  it**: Dark Lord, afternoons, "a proper criminal post" - "...Villainous?" /
  "Very. Sign here." He reads (WHO LOSES) a moment too late, loses
  magnificently three times before sundown, and leaves his tools on the
  barrel in a huff: "Unattended property. Located." **Armour 48**,
  Lorrimer's Tools, an accessory of the general type (Nix has the coat):
  ATK +6, AGI +14, LUK +10, critical +5%, evasion +3%. The children's own
  first pages say nobody will be the Dark Lord, so the judging sets both
  their self switches A by script (ALD-4's way).
* **Afterwards for everybody**: Lorrimer on the front, "Don't. I signed it.
  I read it after. It's afternoons." - getting very good at losing - and
  with Nix, he wants a receipt for his tools; **Sops**, her own last page
  ("The Dark Lord's stayed home again. He does that now.") plus "Except in
  the afternoons, now, when he comes down the street in a teal hood, under
  protest, and loses." The doors go back to their own pages; the Guild's
  Lorrimer is gone for good.
* **Ids taken:** switches **198** `SW_NIX3_ON` (ends), **199** `SW_NIX3_DONE`;
  variable **27** `VAR_NIX3_LOCATED`; armour **48** `AR_LORRIMER_TOOLS`;
  Map 15 event 7, Map 13 event 19; face `Gen_People14` **2** (Lorrimer,
  generated in the borrowed hood, teal, with a waxed moustache;
  `build/characters/cobb-lorrimer.json`). He does not fight: nothing for
  `AUDIT.md`.
* One trope, no blush. Running tally: **tropes +40 fixed and 2-9 from PIP-2;
  blushes +13 fixed and 0-1 from PIP-2.**
* `SW_STORY[NIX]` (on already after NIX-1, -2, -4 or -5 in a game that did
  one).
* **Candidate ending line** (G1; read `SW_NIX3_DONE`): "Cobb Lorrimer, thief,
  lost a contest to Nix on paperwork. He is the Dark Lord in Nether Sopping
  now, afternoons, signed for, and he loses."
* **The rooms (0.1):** Nether Sopping and the Guild were swept on 30 Sep;
  cropped again (92 tiles) and screenshotted with Lorrimer in both places.
  Nothing changed.
* **Scenario** `q_nix3`: passes (22 checks). Its first run failed two of its
  own checks - a fragment spanning a line break, and `numArmors`, which is
  not an engine method (`numItems` takes an armour).
* `TIMELINE.md`: nothing dated.


**E15, HOB-4 The Sky Anvil - done.** HOB-4's section at the bottom of
`q_hob.py`, hooked from `nomap.py` (the Sky Anvil, in a wrapper like the
pond's) and `village.py` (the forge); `build/scenarios/q_hob4.json`.

* **The trade is at the Sky Anvil** (Map 8 event 50, (76,26)), page 3, below
  its ladder (self switch A) with Hob and **`SW_HOB2_DONE`** - `COMPANIONS.md`
  makes HOB-2 the one dependency a chain earns: Hob is good at gates now.
  The site's own second-visit narration and "Stop a while / Press on", then
  Meech's own "Still between gates", then Hob's hand flat on the stone "the
  way you would put it on a horse": "That's star-iron." / "On a Tuesday." /
  "I'll make you a gate for it." / "Out of what? I've no iron. Never thrown a
  gate out, mind." The published first stop stays the first visit, with Hob
  in it or not, word for word.
* **Decided: the gate is made there, out of the eleven gates.** The site
  says the gatepost "outlasted eleven gates"; a farmer never throws one out,
  so they are in the hedge-bottom, rusting in order, and Hob sorts them on
  the snow and works the afternoon cold with what is in his pack. That keeps
  the quest to one trip out and one home. Then **the spring**: HOB-2 ended
  with Beatrice saying the churchyard latch wanted a spring, and he has
  carried one in his pocket since - "Latch wanted a spring." Nobody asks who
  said so. Meech hangs it on the shrine (his own published answer to where a
  gate would go), it swings to and stays, "...That's a very good gate", and
  Hob lifts the Sky Anvil out of the top of the shrine "like an egg out of an
  egg cup" - very heavy, not mentioned. **Item 71**, Star-Iron, a key item,
  so a dismissed Hob's errand waits in the bag. "Pilgrims'll miss it." /
  "They've a gate to open now." **One trope** (the star-metal blade).
  `SW_HOB4_TRADED`.
* **The sword is made at his forge** (Map 6 event 6, page 5): below HOB-2's
  afterwards page (`SW_HOB2_DONE`, its terminal) with Hob and the star-iron,
  and carrying that page - the chalked latch, TOO HEAVY - first. It makes
  exactly one thing, and he knew it would: a sword, plain, long in the blade,
  "that takes the light like frost on a window". **Decided: a sword, because
  Hob cannot hold one** - his class takes flails, axes and gloves - so "not
  for Hob" is a fact of the data, not a line. "Nobody. It's a sword. Swords
  are for whoever." / "She says a sword's no use on its own." / "It's not on
  its own." He wraps it in sacking, puts it in your pack and does not look at
  anybody. **He does not say who it is for**, and the scene names nobody; the
  player can guess (four of the party carry swords, and one of them was
  Chosen with one off a wall). **Weapon 42**, Star-Iron Sword: ATK 66, DEF
  +6, MAT +8, MDF +8, AGI +6, LUK +14, critical +6%; price 0. No gear: Hob
  has his axe.
* **Afterwards for everybody**: the Sky Anvil, "with a gate hung on it now
  and nothing in the top", Meech leaning on the gate, and if you stop: "Best
  gate in the county. Pilgrims come up and open it and shut it all
  afternoon. Nobody's ever given them anything to open before." (His own
  last page was "Still between gates", which is no longer true, so it is not
  carried.) The forge goes back to HOB-2's afterwards once the star-iron is
  spent.
* **Ids taken:** switches **200** `SW_HOB4_TRADED`, **201** `SW_HOB4_DONE`;
  item **71** `IT_STAR_IRON` (icon 313, the bright ingot); weapon **42**
  `WP_STAR_IRON` (icon 119). No faces (Meech is `Gen_People2` 7), no new
  events.
* One trope, no blush. **Running tally at the end of E15: tropes +41 fixed
  and 2-9 from PIP-2; blushes +13 fixed and 0-1 from PIP-2.**
* `SW_STORY[HOB]` (on already after HOB-1, -2, -3 or -5 in a game that did
  one).
* **Candidate ending line** (G1; read `SW_HOB4_DONE`): "The Sky Anvil has a
  gate on it, out of eleven gates, with a spring on the latch. The star-iron
  made one sword. Hob Grumnir has not said who it is for."
* **The rooms (0.1):** the Sky Anvil is a world-map cell and the gate is in
  the telling; the smithy was swept on 30 Sep. Nothing drawn.
* **Scenario** `q_hob4`: passes (21 checks), first run - the published
  first stop with Hob in it, nothing before HOB-2, Press on, the trade, the
  gate for everybody, the star-iron waiting without Hob, the sword carrying
  HOB-2's page, and the sword asserted unequippable by Hob and equippable by
  Bram.
* `TIMELINE.md`: nothing new (1749 and 1750 are the site's).


**Rerun for E13-E15** (0.1): parsing every scenario's `query` and `goto` map
ids and grepping for the places' names finds 63 that touch Maps 3, 6, 8, 13
or 15 - nearly all of them for Map 8. So the rerun was chosen by what each
change can reach, as for E1-E6:
* **Map 3** (Ambrosine stands at (7,12) and blocks it, with Piper in the
  party after the road; the Wall gains a page on `SW_PIP1_DONE`): `village`,
  `reachable_village` (walks to the Wall), `q_pip5`, `guild` (the Elder's
  reference) and `blushes` (the fete minutes).
* **Map 6** (the forge's new page needs the star-iron): `q_hob2`, `q_hob3`,
  `q_rol4`.
* **Map 8** (only the Sky Anvil's event, whose new pages need its A and Hob
  and HOB-2 or HOB-4's switch): `nomap`, which walks onto it. The rest of
  Map 8's scenarios walk past an event they cannot change.
* **Maps 13 and 15** (Lorrimer's two events, blank and through until
  `SW_NIX3_ON`; three shut doors with a page needing Nix and the switch;
  Sops's page on `SW_NIX3_DONE`): `roster` (Pell's desk), `reachable_sopping`,
  `audit_fixes`, `south_road`, `feud`, `q_ald5`, `q_hob1`, `q_mer2`, `q_nix4`.

**Seventeen of eighteen passed first time**, with no check changed:
`village` 12, `reachable_village` 6, `q_pip5` 33, `guild` 7, `blushes` 36,
`q_hob2` 46, `q_rol4` 31, `nomap` 44, `roster` 19, `reachable_sopping` 7,
`audit_fixes` 10, `south_road` 4, `feud` 8, `q_ald5` 50, `q_hob1` 81,
`q_mer2` 52, `q_nix4` 60. **`q_hob3` failed one check, and it was not this
part**: it was written in A8 and asserted that nothing runs when Hob walks
back into the smithy with the anvil returned - and A13 (HOB-2) made exactly
that moment the autorun where Beatrice goes quiet, by design. It had not been
run since. The forge's E15 page needs the star-iron, which `q_hob3` never
holds. The check now asserts the interpreter is running the Forge (event 6),
and its label says why; `q_hob3` then passed (30 checks). Nothing is owed.


**E16, ZEPH-4 The Cinder Fen - done.** ZEPH-4's section at the bottom of
`q_zephyrine.py`, hooked from `nomap.py` (the Fen, in a wrapper like the
Lay-By's) and `journey.py` (the Fen Road's sign, after WRE-1's specimens);
`build/scenarios/q_zeph4.json`.

* **The start is the Fen's second stop with Zephyrine** (Map 8 event 52, page
  3: its A and Zephyrine), below its one-self-switch ladder, with the site's
  own "Stop a while / Press on". The published "Are you a fire person? You
  don't look like a fire person." stays the first visit word for word with
  her standing in it - which is the set-up, since her answer is the second
  stop: "I'm a fire person." / "You don't look like a fire person." The page
  carries the Commissioner's own last line ("Still wet. The form's still
  good.") first. "Press on" with her: she looks back at the Fen twice.
* **Decided: the form is the joke and the payoff**, since `COMPANIONS.md`
  makes it "an unsanctioned quantity of fire, sanctioned". She was expelled
  for one; "Oh, that's only the form. We can sanction anything. That's what
  it's FOR." She reads all three sheets, which nobody has ever done - NAME OF
  FIRE PERSON. QUANTITY OF FIRE. COUNTERSIGNATURE OF FEN (WHERE APPLICABLE) -
  asks what to put for quantity ("Nine hundred acres") and writes it in "in
  the hand of a person who has been told for eleven years that hers was the
  wrong amount". SANCTIONED, three times. "...Say that again."
* **The fire** reuses ZEPH-3's effects on the player (animations 66, 68, 70,
  two tints, two flashes, two shakes), all put back. It reads ZEPH-5: with
  it done she does not aim, "the way Dunnock's missing page says to";
  without, she aims properly, from the shoulder, the Collegium's way. It
  burns all afternoon and all night; nobody in the parish goes to bed;
  somebody brings out chairs. **No fight** - the Fen is the hazard, and the
  quest is the one ability nobody else has.
* **Decided: the Fen's countersignature is a scorch.** The published first
  stop has "There's a box for it. I've never had one back." She held the third
  copy out over the edge all night; it comes back scorched in one corner,
  exactly in the box. "Thirty years in this job. I've never had one back." The
  certificate, filled in thirty years ago and waiting for a name, is **item
  72**, Certificate of Burning (icon 193). "It's the first piece of paper about
  me and fire that I've liked." / "Same again in thirty years?" / "Write to
  me. In triplicate." **One trope** (the elemental hazard only one member can
  solve). No gear - she has the robe (or chose not to).
* **Decided: the road is a real two-way causeway to Great Dunnage**, since
  the Fen was drowning "the road to Great Dunnage". The world map is a file,
  not a drawing, and a page cannot repaint tiles, so the road is travelled in
  a window: the Fen's afterwards page asks "Take the causeway / Stop a while /
  Press on" and the causeway is a long day's walk on dry stone to
  `places.DUNNAGE_STEP`; and **a new signpost by Great Dunnage's gate** (Map 8
  event **81**, `places.FEN_ROAD_SIGN` (33,53), south-east of the step, a
  `WB_SIGN` that blocks its cell and is read from beside like the other four)
  reads THE FEN ROAD. CINDER FEN. (BURNT. SANCTIONED.) and goes south to
  `places.FEN_ROAD_END` (47,117), the cell north of the Fen. Before the burning
  the sign is a blank page, through and below characters, so nothing in any
  existing walk can touch it. On foot it is 91 steps from Great Dunnage to the
  Fen, so the reward is one long walk, both ways, into the far south (Sump,
  the Fair, the Wrong Dragon) - modest, and real.
* **Afterwards for everybody**: the Fen burnt, black and dry, a causeway north
  past a milestone; "Stop a while" is the Commissioner - "The third copy's in.
  Countersigned. First I've had back in thirty years." - and with Zephyrine,
  "Miss Vance. Still sanctioned." / "I know. I keep checking." **The Fen's
  own last page is not carried**: "still wet" and "still waiting for a fire
  person" are no longer true, HOB-4's Meech's way. The Commissioner keeps no
  pronoun.
* **Ids taken:** switch **202** `SW_ZEPH4_DONE`; item **72**
  `IT_FEN_CERTIFICATE`; Map 8 event **81**; `places.FEN_ROAD_SIGN`,
  `FEN_ROAD_END`. No faces (the Commissioner is `Gen_People10` 7, a face with
  no sprite, as the site drew), no variables.
* One trope, no blush. Running tally: **tropes +42 fixed and 2-9 from PIP-2;
  blushes +13 fixed and 0-1 from PIP-2.**
* `SW_STORY[ZEPH]` (on already after ZEPH-1, -2, -3 or -5 in a game that did
  one).
* **Candidate ending line** (G1; read `SW_ZEPH4_DONE`): "The Cinder Fen was
  burnt in the year 2000 by Zephyrine Vance, fire person, sanctioned, in
  triplicate. The road to Great Dunnage is dry, and the form came back
  countersigned."
* **The rooms (0.1):** the Fen is a world-map cell (the `Trail` stamp) and
  nothing was drawn on it; the sign is the stock `WB_SIGN`, screenshotted by
  the gate.
* **Scenario** `q_zeph4`: passes (19 checks), first run - walked onto the
  Fen for the published first stop with Zephyrine, the site's own second page
  without her, Press on, the burning (the Collegium's way, ZEPH-5 undone), the
  tint put back, the certificate and no gold, afterwards with and without her,
  the causeway north to Great Dunnage's step, the sign blocking its cell and
  read from beside, Not now, and the fen road back south.
* `TIMELINE.md`: 1970, Mr Tinder retires and the Fen goes unburnt ("thirty
  years").

**E17, ROL-5 The Understudy - done.** ROL-5's section at the bottom of
`q_roland.py`, hooked from `dunnage.py`'s Bell (Mrs Dewhirst, the understudy)
and `journey.py` (the tower door's page, and her event beside it);
`build/scenarios/q_rol5.json`.

* **Decided: it needs ROL-1**, as NIX-1 needs NIX-4: the meetings are what
  there is to tell, and the minutes are in the party's bag. The 141st meeting
  never mentioned an understudy (item five, any other business, was silence),
  and that is the point - she is not on the agenda.
* **Maud Penhallow, sixteen, is at the Bell's snug table** once the meeting
  has sat (Map 65 event **15**, `places.UNDERSTUDY_BELL` (4,9), facing the
  table), for everybody: without Roland, "Is Mr Fairweather with you? I'm
  meant to study how he stands." In Fellow Blunt's yard since she was nine -
  sword, horse, lineage, the lot, "in case it's ready and you're - you know."
  / "Old." / "They said 'unavailable'." She has been told it is nearly ready
  since she was nine; they will not let her come to the meetings, because she
  is not on the agenda. "What are they like?" / "...Short."
* **His moral position, in two looks, both his.** The first (Roland): an hour
  on her guard in the yard behind the Bell, almost nothing said, and she finds
  a gap in his nobody has found in fifteen years; outside, "She's been told
  it's nearly ready. I was told that when I was twelve... I don't know whether
  to tell her." `SW_ROL5_ON`. Without him, she waits: "He stands differently
  when he's thinking." The second (Roland and the switch): "I've thought about
  it." He sits on the other side of that table, where he is never the asset,
  and tells her - apologies, the sorcerer; readiness, not; the lineage,
  present; the asset, available; thanked; eleven minutes, a hundred and
  forty-one times - and lays the minutes in front of her. She reads them
  twice, eats some pie, and thinks. "Eleven minutes." / "Somebody should have
  told you at nine. Somebody should have told me at twelve."
* **The question is dropped**: "Whose prophecy is it? Exactly?" Roland opens
  his mouth and closes it; "It's - it names a lineage. Mine. It's -"; and Mrs
  Dewhirst comes over to ask about pudding, and the question stays on the
  table among the plates, and nobody picks it up. The scenario asserts no line
  answers it. **One trope** (the successor). No item: the minutes go back in
  the bag.
* **Decided: what she does with it is go and see the end of one.** "You've
  never seen the end of one. Eleven doors... Then I'll be at the door. I'll
  tell you how it ends." He laughs, properly, which nobody at the Bell has
  heard. `SW_ROL5_DONE` and his story; she is gone from the snug.
* **The tower door is `COMPANIONS.md`'s "somebody at the tower door after
  all"**, and nothing keeps him: the Tower Door (Map 8 event 4) gains page 2
  on `SW_ROL5_DONE`, which is page 1 exactly with her scene spliced in after
  `roland_departure` (`journey.py` passes the split; the check is that page 2
  minus the splice is page 1, command for command). Once, on the door's self
  switch A: if he has just gone, forty paces off he looks back at the girl
  beside the door with a practice sword, she raises it the way you are taught
  at nine, and he raises a hand and goes; then, either way, "Somebody is at the
  tower door after all. It is not him." / "I'm the understudy. I'll wait here.
  When you come out, I'll go and tell him how it ends." She stands beside the
  door (Map 8 event **82**, `places.UNDERSTUDY_DOOR` (65,43), west of it on the
  grass, the door's cell and the way up left clear): "Go on. I'll be here.
  Somebody ought to see the end of one." His departure, its lines and its
  sword are untouched.
* **Afterwards for everybody**: Mrs Dewhirst's own last page (Map 65 event 2,
  page 4, on her A and `SW_ROL5_DONE`) plus "Snug's empty, love. Miss
  Penhallow's gone north. Said to tell Mr Fairweather she'd be at the door."
  With Roland it beats ROL-1's page, which after the meeting is her own page
  anyway.
* **Ids taken:** switches **203** `SW_ROL5_ON`, **204** `SW_ROL5_DONE`; Map 65
  event 15, Map 8 event 82; `places.UNDERSTUDY_BELL`, `UNDERSTUDY_DOOR`; face
  `Gen_People14` **3** (Maud, generated: brown ponytail with a ribbon, the
  silver practice jacket; `build/characters/maud-penhallow.json`). She does not
  fight: nothing for `AUDIT.md`.
* One trope, no blush. Running tally: **tropes +43 fixed and 2-9 from PIP-2;
  blushes +13 fixed and 0-1 from PIP-2.**
* `SW_STORY[ROLAND]` (on already after ROL-1, which this needs).
* **Candidate ending line** (G1; read `SW_ROL5_DONE`) - after "who thinks
  about this one": "Somebody saw the end of this one. She is sixteen, and
  she waited at the door, and she has gone to tell him how it ends." Her
  question is not in it.
* **The rooms (0.1):** the Bell was swept in B1 and is unchanged; Maud was
  screenshotted at the snug and beside the tower door.
* **Scenario** `q_rol5`: passes (26 checks), first run - nobody before ROL-1,
  waiting without Roland, walked to and met, a dismissed Roland's errand
  waiting, the telling (never answered), Mrs Dewhirst with and without him,
  and the tower door walked onto: he leaves as published, her scene once, the
  door's own page after, her line from beside, and the scene again with the
  switches put back and Roland not there to leave.
* `TIMELINE.md`: 1978, Roland at twelve told it is nearly ready
  ("twenty-two years"); 1993, Maud into Fellow Blunt's yard at nine; her age,
  sixteen.

**E18, ROL-2 Roland's Own Quest - done.** ROL-2's section at the bottom of
`q_roland.py`, which draws Map 67 (`q_roland.build`, called from
`build_game`), hooked from `dunnage.py`'s Bell (the card) and `journey.py`
(the cave, and the tower door's pages through `q_roland.door_pages`); the
records in `db.build_worm`; `build/scenarios/q_rol2.json`.

* **Decided: it needs ROL-1**, like ROL-5: the prophecy lives at the
  meetings. The start is **the card on the snug table** (Map 65 event **16**,
  `places.SNUG_CARD`, the table cell, read from beside), which ROL-1's
  narration already put there: RESERVED. R. FAIRWEATHER. With Roland he turns
  it over without looking, and on the back, in Fellow Amory's hand, is the
  prophecy as minuted - WHEN THE STONE IS READY, ONE OF THE LINE SHALL DRAW THE
  SWORD THEREFROM, AND GO DOWN UNDER CARN DREY, AND THE WORM THAT SLEEPS THERE
  SHALL BE ENDED, AND THE LAND SHALL BE GLAD. "I know it by heart. I was
  twelve." Carn Drey is an afternoon east; he has never been; it isn't ready;
  **Fellow Blunt checks the stone - from the gate, quarterly, and has never
  gone down: the stairs are not his department; it's minuted.** You suggest
  somebody go down the stairs and look. "...Today?" "Today / Not today"
  ("It isn't ready."). Today: GONE TO SEE, in pencil, propped against the salt
  (`SW_ROL2_ON`).
* **The place is Map 67, "Under Carn Drey"**, 21x21 on the Dungeon tileset,
  Dirt Cave throughout (one family), drawn in `q_roland.py` since it is in no
  place (0.4): stairs down into the stone's room, the stone in the middle with
  `!Weapon` 0 standing in it, two tall rocks, a short passage, and the Worm's
  room at the bottom of the hill. **The way in is a `WB_CAVE` event in the
  hill's south face** (Map 8 event **83**, `places.CARN_DREY` (39,55)), there
  only once the party has gone to see - a gate and a plate, THE WORM. NOT
  READY. (FELLOW BLUNT, QUARTERLY.) "The gate is not locked. Nobody ever tried
  it." - "Go down / Not yet", with Roland; without him it waits. Down is the
  tower's gloom idiom (a tint), lifted on the way out, which comes up at
  `places.CARN_DREY_STEP` (40,55), the road's side (the cell south of the cave
  is hill). The Worm's room was drawn 15x8 first and was too big and too bright
  for "asleep in the dark"; it is 11x6, dimmed. No random encounters.
* **The stone** (event 2): twenty-two years of dust on the hilt and none on
  the stone. "Readiness. The stone?" You say it looks ready to you; nobody has
  ever said that to him. His hand on the hilt "the way you might put a hand on
  a horse you were not sure of", and it comes out "as if it had only been
  waiting to be asked". "...Oh." / "It's ready." `SW_ROL2_DRAWN`. Nobody draws
  the moral.
* **Decided: the Worm is never drawn on the map.** It is coiled three times
  round the room in the dark - "You have, you realise, been walking beside it
  since the stairs" - so the room is its body and the fight shows it: **enemy
  59**, the Worm of Carn Drey, stock `SF_Anaconda` (unused, and a worm, not a
  dragon - ALD-6's is the valley's only dragon, and stays so), fixed numbers
  "scaled for a hero of nineteen" (1,600 hit points), skills **183** Coils and
  **184** Looks At Roland ("It was expecting somebody younger."); **troop 54**,
  no escape. Before the sword: "Not yet. The sword first. It's in the
  prophecy, and the order matters to the committee." "I'm thirty-four. I'm
  sorry. I did mean to come sooner." It can be lost ("Again, after tea?",
  Recover All, and it waits).
* **Won**: over before Piper has got to the end of the first line of a verse
  (or "in about the time it takes to say so" without her); the land - the
  top of the hill, a field with sheep in it - is presumably glad. "That's it.
  That was it. Twenty-two years." / "Would you - I know it's a great deal to
  ask. Would you mind being surprised? Only a little." **You are. Everybody
  is** - at Roland Fairweather, who has finished something. He laughs till he
  has to wipe his eyes, and thanks each of you by name. **Played straight, and
  not sad; nobody says whose prophecy it is** (asserted). **One trope** (the
  epic). `SW_ROL2_DONE` and his story.
* **Roland's gear (0.5) is the sword out of the stone**: **weapon 43**, The
  Drawn Sword, strictly better than Fairweather's Own in every parameter (ATK
  72, DEF +14, MAT +12, MDF +12, AGI +10, LUK +16, Light, critical +15%, hit
  +6%; asserted). **He keeps it till the door** - "It's had one afternoon. It
  ought to have another." - so nothing goes in the bag at Carn Drey, and
  **nothing keeps him at the door**: the tower door gains pages 3 and 4 (on
  `SW_ROL2_DONE`, and on it and `SW_ROL5_DONE` together), each its own page
  with the hand-over spliced **inside** his departure, after Fairweather's Own
  and before "Take it up there" - he unbuckles the sword out of Carn Drey and
  lays it on top; "And that one." The splice is found by that line and asserts
  it is still there. His departure, his lines and the first sword are
  untouched, and ROL-4's refit still reads `WP_FAIRWEATHER`.
* **Afterwards for everybody**: the card - under GONE TO SEE, in the same
  pencil, DONE. (R.F.) It took an afternoon.; and the plate on the cave - under
  NOT READY, READY. DONE. (R.F.) The Worm's room is empty and walkable.
* **Ids taken:** switches **205** `SW_ROL2_ON`, **206** `SW_ROL2_DRAWN`,
  **207** `SW_ROL2_DONE`; weapon **43** `WP_DRAWN` (icon 120); enemy **59**
  `EN_WORM`; troop **54** `TR_WORM`; skills **183-184**; **Map 67**
  `MAP_CARN_DREY`, events 1-3; Map 65 event 16, Map 8 event 83;
  `places.CARN_DREY`, `CARN_DREY_STEP`, `SNUG_CARD`. No faces; stock art, so
  nothing for `AUDIT.md`.
* One trope, no blush. **Running tally at the end of Part E: tropes +44 fixed
  and 2-9 from PIP-2; blushes +13 fixed and 0-1 from PIP-2.**
* `SW_STORY[ROLAND]` (on already after ROL-1, which this needs).
* **Candidate ending line** (G1; read `SW_ROL2_DONE`): "Roland Fairweather's
  prophecy was discharged in an afternoon, under Carn Drey, with help. He
  asked to be surprised. Everybody was."
* **The rooms (0.1):** Map 67 is new, screenshotted lit and in its gloom, and
  the fight once; the Bell was swept in B1 and is unchanged; the cave was
  screenshotted in the hill.
* **Scenario** `q_rol2`: passes (31 checks): the card before ROL-1, without
  and with Roland, Not today and Today; the cave walked onto, waiting without
  him, Not yet, Go down; the Worm before the sword; the stone walked to and
  drawn; the Worm without him; a look at the fight; lost, then won with
  Piper; out by the stairs with the gloom lifted; both afterwards; and the
  tower door walked onto, both swords on the grass, and both switches' page.
  Its first run gave the fight sixty presses and checked while the battle was
  still up; the fight's kill now comes sooner and `advance` has 250.
* `TIMELINE.md`: the 1978 row gains Fellow Blunt's quarterly look from the
  gate and the Worm ended in 2000.

**Rerun for E16-E18** (0.1): parsing every scenario's `query` and `goto` map
ids and grepping for the places' names finds the usual near-whole suite for
Map 8, so the rerun was chosen by what each change can reach:
* **Map 65, the Bell** (Mrs Dewhirst's afterwards page on `SW_ROL5_DONE`;
  Maud at (4,9) and the card on the snug table, both blank and through until
  `SW_ROL1_DONE`): every scenario that walks it - `dunnage` (the Bell's site
  scenario), `dunnage_company`, `q_pip3`, `wall_ring`, and `q_rol1`, the one
  that sets `SW_ROL1_DONE` and so walks the Bell with Maud standing in it.
* **The world-map sites whose pages this part appended to**: the Cinder Fen
  (`nomap`, which walks onto it) and the Tower Door, whose three new pages
  need `SW_ROL5_DONE` or `SW_ROL2_DONE` and carry splices inside Roland's
  departure - `guest_leaves` and `q_rol4` (the departure, walked, and the
  sword it leaves), `tower_door`; and `q_rol5`, which ran before E18 added
  the door's pages 3-4 and the snug card.
* **Not rerun, and why**: Map 8's events 81-83 (the Fen Road sign, Maud by the
  door, the cave in Carn Drey) are a blank first page, through and below
  characters, until switches only this part's scenarios set; `q_zeph4` and
  `q_rol2` ran on the maps' final state; `journey`, `airship_lands`,
  `nix_door` and the rest of Map 8's walk past the tower door on its page 1,
  which is byte for byte what it was. Map 67 is new and only `q_rol2` enters it.

**All ten passed first time**, with no check changed: `nomap` 44, `q_rol1`
31, `q_rol5` 26, `q_pip3` 38, `wall_ring` 35, `guest_leaves` 7, `q_rol4` 31,
`tower_door` 6, `dunnage_company` 54, `dunnage` 153. Nothing is owed. **Part E
is done.**

**F1, Spare joins - done** (5 Oct 2026). `q_spare.py` (new), hooked from
`north.py` (Spare, Shim, Gudgeon: one line each); his records in
`db.build_spare`; `build/scenarios/q_spa0_joins.json` and
`q_spa0_argument.json`. Every page on Maps 21 and 25 that existed is byte for
byte what it was; the data diff is Spare's ids and nothing else.

* **The gate is `SPARE.md`'s A + B + C + D**, read out by **Gudgeon** (Map 25
  event 4, pages 3-4 below her one self switch on `SW_SPARE_ASKED`): she knows
  where Form P-9 is and does not get up, and reads the first unmet section of
  it - *one*, the applicant heard in full (Spare's own self switch C); *two*,
  the family met, all of it ("It is a long section. Mam has the list. So do
  I."), which is `q_spare.FAMILY`, `SPARE.md`'s ten - **not Cotter**;
  *three*, means of travel ("He is nine. He is not walking to a tower through
  the Gloamwood"), which is `SW_AIRSHIP` - having the Two Hundred at all.
  (Built first on `SW_TWO_HUNDRED_FLEW`, set down by the tower, which
  `SPARE.md` never asked for; changed at Mike's word, 6 Oct 2026.) Then the third drawer, one sheet, blown on: the form
  (item 33, `SW_SPARE_FORM`), "Good luck." Afterwards: her own last line,
  and "And Mam signs it, or nobody does." `q_spare.check_family`, called from
  `build_game`, fails the build if north.py's event ids ever move under it.
* **Shim** (Map 21 event 16, pages 3-4 below her self switch on
  `SW_SPARE_ASKED`): "I said he can have a washer." She does not offer the
  bearing. Not the bearing. Carried as item 34 - or, if he has already
  joined, straight onto him (armour 27).
* **Spare** (Map 21 event 13, pages 5-7, below his ladder's terminal C):
  page 5 on the form is `SPARE.md` 2 whole, the Eighty-Four window inside it
  on `SW_84_REBUILT`; page 6 on self switch **D** is the short ask, which "Not
  yet", no room and a lost argument all set - "The bag is down already", or,
  after a loss, "I have been thinking about Mam."; page 7 on
  `SW_SPARE_JOINED` is blank and walk-through. No room is his line: "You have
  got three already. I will wait. I am extremely good at it."
* **The argument** is fought by Spare alone, exactly as `SPARE.md` 3 says: the
  party array to `$gameTemp`, `setup(11)` at level 12, troop 29, can lose and
  cannot escape, a troop page that says "Mrs Cotterill stops." and aborts at a
  quarter, and the party put back after all three branches. Lost: "Tea is at
  six. Wash your hands." (`SW_SPARE_REFUSED`); the retry's Mam is short
  ("On who?" "Shim."). Won: the concession, word for word, then he joins -
  levelled to the party's highest, rested, Shim's washer on him if it was
  carried, **The Drawing learned** because it is what she found in the bag,
  the form handed over, `SW_SPARE_JOINED`, `SW_SPARE_KNOWN`, `VAR_COMPANIONS`.
* **The records** (`db.build_spare`): Actor 11 on **Class 12**, The Ninth -
  tgr 0.45, evasion 0.25, double gold, special skills only, AGI the best in
  the game and HP, DEF and ATK the worst. **Weapon type 13, Bag**, his alone,
  locked in his hand (Lock Equip, 53 - *not* Seal Equip, 54, which deletes the
  slot; the first run of `q_spa0_argument` caught exactly that). Every skill
  but one is something out of the bag and needs it: Small Enough (a candle
  end, `a.agi * 2`), I Have A Bag (plasters, a hanky and a boiled sweet each),
  They Never Hit Me (the jumper, state 42; icon 135, a pullover - 154 is a dress), Ninety Tubes (a flue brush longer
  than the bag; state 43, DEF to 60% for the fight), The Drawing (scope 13:
  revives, heals, ATK and AGI up, full TP; costs 100). **Temper Tantrum** is
  the one where he puts the bag down: 20 TP, `a.agi * 4.5 - b.def`, common
  event 4 takes a fifth of his HP (never the last point), and its element is
  **10, Temper**, which Mrs Cotterill alone is immune to - it has never once
  worked on her. **Armour type 14, Washer.** Mrs Cotterill is enemy 28 on
  Mike's art: You Are Nine (a third of his HP, her opener), Ask Your Father
  (a heal; "Mr Cotterill looks at the sky."), That Is Not The Point (every
  buff and the jumper off him; "He was doing so well."), I Have Said No
  (below half: less damage, all his TP; "It is not louder. It is quieter.").
  Tuned by simulation at level 12: about six in seven for a player who heals
  and spends TP well, eleven turns or so; 2,600 HP. `balance.py` at 14: his
  best hit 555 against Hob's 760 and Nix's 276, no sweep, 559 HP.
* **Not in `story.COMPANIONS`**, so no form desk can strike him off; he is in
  `SW_RECRUIT`, `SW_KNOWN` and `SW_STORY` (110) for their names and for
  `companion_story`. He does not leave at the tower door.
* **Tropes +2** (the fight starting, once; the secret companion, at the
  join): running tally **+46 fixed**, and 2-9 from PIP-2. **Blushes +0**:
  +13 fixed. Ending block: G1's, as decided - candidate line for Spare,
  "Spare Cotterill, aged nine, Form P-9, countersigned by his mother. He
  wrote." Nothing may settle the baby (SPA-3 is the extension's).
* `NORTH.md` 9's "Actors / Classes: none" is amended, not deleted; enemy 28 is
  written into its table. `TIMELINE.md` has his six and his two years.
* **Scenarios**: `q_spa0_joins` 19 checks, `q_spa0_argument` 17 checks - all
  pass, the argument fought for real on auto-battle, a loss and then a win,
  with a screenshot of the fight (`spa0_argument.png`). **Rerun**, because they stand on Maps 21
  or 25 (found by parsing every scenario's `query` and `goto`): `clanging_cast`
  38, `q_mer2` 52, `q_nix4` 60 - all passed - and `clanging_faces` 18 after
  one fix that was **not** F1's: it still expected Spare's stock face,
  `SF_People1` 0, which the redraw (a0cf092) replaced with `Gen_People14` 4
  without updating the check. Its expectation and label are corrected, and
  `face_spare.png` shows the new face.


**F2, SPA-1 The Letters - done** (6 Oct 2026). `q_spare.py` (the second
quest in it), hooked from the eight towns' own modules and `north.py` (one
line each); `build/scenarios/q_spa1_letters.json`. Every page that existed is
byte for byte what it was: the data diff is a new last event on each of Maps
13, 31, 38, 40, 42, 44, 52 and 58, three pages appended to Mrs Cotterill
(Map 21 event 11), a new Map 22 event 10, item 73, common event 5 and four
switch and variable names.

* **The courier** is `Gen_People14` 6 (`build/characters/the-courier.json`,
  `FACES["Courier"]`): red coat (male clothing p25), grey flat cap (male AccB
  p07, the bandana, which reads as a cap in the sprite and a little less so
  in the portrait). **No generator part is a satchel**; the narration carries
  it. He is the last event in eight towns - **Nether Sopping, Restwell, Olde
  Evermore, Gladhollow, the Former Premises (the airship's rock, in the
  waiting area by the sofa, "There is no road up here"), Frostwick, Ashcombe
  (beside the post office, whose window says ALL LETTERS ANSWERED) and the
  Collegium** - Great Dunnage left out on purpose, as F4's and Cotter's.
  Page 1 is empty and below characters, so **without Spare the town is
  today's town**; page 2 on actor 11 is him; page 3 on A is "On my rounds."
  Spare writes them, so posting needs Spare.
* **A letter is two halves**: two lines for the town (`TOWNS`), two for the
  saga (`SAGA`), chosen by **how many have gone before** - so in any order
  the first letter is nearly true ("There is no dragon"), the dragon arrives
  on the third, is called Ferrule, grows to the size of the Two Hundred,
  asks for a job at the works, and on the eighth is coming home for its tea
  ("Please do more potatoes. It has never had a potato."). `ARRIVES` is the
  same by order: he is always already there, and on the eighth "Of course he
  is here." He only ever says "Post?" and "Upper Clanging. Dinner hour."
* **State is global**: `VAR_SPA1_POSTED` (28) counts; `VAR_SPA1_ORDER` (29)
  holds one decimal digit per town, its place in the order, which is how
  **Spare's Copies** (item 73, given with the first letter, used from the
  menu) read back through common event 5 in posting order, one window each
  with Next. The courier's own A is only "posted here".
* **Mrs Cotterill**, below her one self switch: page 3 on actor 11 and one
  letter ("It does not have to be true." "It does not."); page 4 on all
  eight, the dinner hour - she dries the weather (the town door's `dry()`; the
  first screenshot had it raining indoors) and takes the party up to the
  works, where `dinner_hour` (Map 22 event 10, autorun on `SW_SPA1_DINNER`,
  209) reads the last one out to the shift - which at the Hoyle Works is
  Ott, Nib and Tappet. Nib had Thursday in the sweep; Tappet had "there is
  no dragon". "I did more potatoes anyway." Then `SW_SPA1_DONE` (208) and
  `companion_story(SPARE)`. Page 5 on 208 is her own last page plus "There was
  no dragon. I have kept them all anyway."
* **Tropes +1** (the collectible, at the first letter: "one of these in every
  town"): running tally **+47 fixed**, and 2-9 from PIP-2. **Blushes +0**: +13
  fixed. **Candidate ending line**: "Spare Cotterill wrote home from eight
  towns. There was no dragon. His mother did more potatoes anyway." No date
  is new, so `TIMELINE.md` is unchanged; nothing settles the baby (her
  "Ten in the spring" is her own published line, repeated).
* **The works, looked at** (0.1): `propsheet.py` over Map 22 - `Machine C` has
  a small blue readout in the corner of a brass machine; it is the north's
  steam look on purpose, used in the forge too, and was kept.
* **Scenarios**: `q_spa1_letters` 27 checks, all pass - posted out of
  `TOWNS` order, Restwell's walked to, the copies read back in order, the
  dinner hour with a screenshot (`spa1_dinner.png`) and dry indoors.
  **Rerun**: only `q_spa0_joins` and `q_spa0_argument`, because they are the
  only scenarios that ever put Spare in the party, and without him every
  courier is an empty below-characters page that blocks nothing and Mrs
  Cotterill's new pages need him or switch 208. The twenty scenarios that
  stand on the touched maps (parsed from `query` and `goto`) can see no
  difference, and were not rerun.
---

**F3, SPA-4 The Pen Pal - done** (6 Oct 2026). Village 1 is **Much
Pottering**, Maps 68-69, drawn by a place module of its own, `pottering.py`,
with the quest's pages from `q_spare.py` hooked one line each - not drawn in
the quest module as 0.4 says for "a map in no place", because it is a place:
a site on the world map with five residents, like Ashcombe, which nobody needs
Spare to visit. `build/scenarios/q_spa4_penpal.json`. The data diff is Map 8
events 68 and 69 (the placeholders, now its doors, on the same cells, at the
same ids, every tile unchanged), Maps 68-69, switch 210 and variable 30.

* **The place.** The village where nothing has happened: a stone on the green
  says it has never been burned down, overrun, foretold, cursed or chosen -
  the starting village that is on fire by chapter one, turned round, **one
  trope**. Twinned with Upper Clanging, which Mrs Throssell chose off the map
  as the most different place she could find; neither has visited. Four
  things to walk into, player-touch at "same as characters": Mr Dibble's
  fence (WET PAINT, "That's four today"), a pig asleep across the street (PIG
  HAS RIGHT OF WAY), the oak by the road in (MIND THE BRANCH, read while
  walking into it) and the wishing well (I WISH FOR A VOLCANO. A PROPER ONE.
  E.G.). A hedge maze of two rows - the hedge is the knee-high overlay you can
  wade through, which is what its sign asks you not to do - with only Mr
  Dibble's name in its visitors' book. The Gotobeds' cottage: Mrs Gotobed,
  the box of Spare's letters on the cabinet (`Small Box C`, which is
  envelopes), and a mountain over the fire with crayon smoke on the glass.
* **New faces**, all generated: Effie `Gen_People14` 7 (ginger plaits, a
  sticking plaster), and `Gen_People15` opened for Mrs Gotobed 0, Mr Dibble 1,
  Mrs Throssell 2 (bonnet and spectacles) and Mr Cobley 3 (the angler's hat).
* **The quest.** Effie at her gate, without Spare: waiting for the post; her
  pen pal is six foot and drives the Two Hundred, and has a dragon once three
  letters are posted (the courier brings her his letters home as well);
  "Don't tell him" about the volcano. **With Spare**: "You're not six foot."
  "You're not a princess." - "nearly", and the **childhood-friend trope**
  ("They knew each other at once. They are both furious about it."). Then her
  tour, `VAR_SPA4_TOUR` (30): the volcano (Mr Dibble's bonfire, lit in
  November, never out - and Spare's first true thing, the ninety tubes), the
  sea serpent (Mr Cobley's carp, Old Tom, who turns over once and launches
  the duck), and the post, where both confess and each writes one on the spot
  and **the courier carries them four steps**. `SW_SPA4_DONE` (210) and
  `companion_story(SPARE)` (already on after F2, so the count does not move).
  Each stop is an Effie event of its own; a dismissed Spare's tour waits.
* **The courier** is here for anybody, because her letters come here, and is
  **not** a ninth posting town: with Spare he asks "Post?" and Spare says
  "Not today. She is right there."
* **Afterwards**: Effie's own last page plus "The dragon's learned to swim.
  It's in our pond. Mr Cobley's furious." The well gains A DRAGON. S.C.
* **Tropes +2** (the plaque, the childhood friend): running tally **+49
  fixed**, and 2-9 from PIP-2. **Blushes +0**: +13 fixed. **Candidate ending
  line**: "Spare Cotterill met his pen pal at last, in Much Pottering. There
  was no volcano either. They are still writing." `TIMELINE.md`: 1970 Mr
  Cobley and Old Tom, 1997 the twinning and the pen pals, Effie nine. Nothing
  settles the baby.
* **Looked at** (0.1): `propsheet.py` over Maps 68-69, 71 tiles, all period and
  all what the text calls them. The first draw had a plus-shaped pond, a
  hedge in black (an A2 overlay drawn on layer 0) and a maze whose one
  corridor was walled across, so the centre could not be reached -
  `validate.py` was clean, because the centre is read from beside. Found by
  screenshot and a flood, fixed, shot again.
* **`placeholder_doors`** now asserts none are left, and nothing is called
  Village 1, and keeps its six `<aironly>` checks; the walk moved to
  `q_spa4_penpal`.
* **Scenarios**: `q_spa4_penpal` 36 checks, all pass, and
  `placeholder_doors`. **Rerun**: nothing else. No other scenario stands on
  (60,61)-(61,61) or names Map 8's events 68-69 (grepped), and the
  village is new.

---

**F4, SPA-2 Ninety Tubes - done** (6 Oct 2026). `q_spare.py` (the fourth
quest in it), with Cotter's pages hooked by wrapping his event in
`dunnage.py` (`q_spare.cotter(q_hob.owned(...))`, one hook, three lines) and
Map 70 drawn in the quest module (`build()`, called from `build_game.py`, a
map in no place, child of Great Dunnage in the map tree);
`build/scenarios/q_spa2_tubes.json`. The data diff is Cotter's two appended
pages (his four pages byte for byte what they were), Map 70, MapInfos, and
three switch and one variable names.

* **Cotter, Map 61 event 12**, pages 5-6, below his terminal A. HOB-1 had
  already put a quest page (Hob, A, switch 142) and an afterwards page (B)
  there, so both new pages **play HOB-1's quest page instead** whenever it
  is the one the engine would have shown (`q_piper._pip4_test`, imported:
  its page's conditions and not B's), and the afterwards page carries his
  B page or his A page by B. Without Spare and before `SW_SPA2_DONE`, the
  town is today's town.
* **The quest page**, on Spare: Cotter looks down, properly - he has just
  introduced himself to the party over his brother's head, which is the
  published first page kept as the reaction shot. "Does Mam know?" Mam's
  terms were his too, at sixteen; "Is any of it true?" "No." "Good lad."
  The bottom lock is jammed, thirty of the Company's boats are sat on the
  cut, and the Canal Company's smallest man went in at eleven and has not
  come out. "A man does not fit." "I fit." And Mam's second term, kept to
  the letter: **"I would not be first. The man is first."** Not now sets
  `SW_SPA2_ASKED` (211) and the short ask from then on.
* **Down**: the party walks to the south end of the basin
  (`places.CULVERT_STEP`, (33,20), open), Spare checks his jumper is on,
  gives you the bag, and asks "You will be here?" Then `SPARE.md` 3's swap -
  **into `VAR_SPA2_PARTY` (31), not `$gameTemp`**, because the menu is open
  in the culvert and a save made there has to come back up with the party;
  it never overwrites a party already set aside. The town's BGM fades, the
  screen is tinted `[-119,-119,-102,119]` (darker than Carn Drey's), and Map
  70 autoplays the Drips BGS.
* **Map 70, The Bottom Lock**: a brick culvert (Dungeon `Wall J (Brick)`,
  `Cobblestones A`), one man wide, standing in A5 `Darkness` past one ring
  of wall top - solid brick read as a brick yard from above. The ladder
  (`Metal Ladder`) on the face over the arrival, read from below; a drop
  where he counts the bricks out loud "the way he counts tubes"; a dead end
  with a crown in it ("There is always something down the back of
  something", 1 crown); **Mr Pocock**, stuck at the narrow bit - a voice
  in the dark, **no face and no sprite**, which is why "A Voice" becomes
  "Mr Pocock" in the speaker name. He is frightened of the dark; Spare says
  what he *is* frightened of, `SPARE.md` 2's line, to the one person in the
  game who needed to hear it, and talks him out backwards by the boots. Then
  the paddle (`Jail Bars` on the face): the Mayor's ceremonial scissors, a
  yard long, ribbon on, jammed across the bars since the lock was opened -
  worked out "the way you get a brush back out of a tube with a bend in it".
  "Ninety-one." `SW_SPA2_CLEARED` (212); the BGS turns to River.
* **The ladder** takes him up at any time: before the paddle, the party is put
  back and the errand waits on Cotter's short ask. After it: **everybody is
  there.** "There is always somebody there." Cotter comes down at a run; the
  Mayor has had to open two things with a knife; Mr Pocock has gone home for
  a lie down and says Spare is to have his job ("I have got a job."); thirty
  boats go down the cut and every steersman lifts his hat; the Canal
  Company's fee (`SPA2_FEE`, 300 crowns) and a bun from Cotter; "Tell her I
  did not go in first." "Did you?" "Mr Pocock went in first."
  `SW_SPA2_DONE` (213) and `companion_story(SPARE)` (already on).
* **Afterwards**, for everybody: his own last page plus "Thirty boats down,
  and the Mayor's had his scissors back. He's cut the ribbon again."
* **Tropes +1** (the solo section): running tally **+50 fixed**, and 2-9
  from PIP-2. **Blushes +0**: +13 fixed. **Candidate ending line**: "Spare
  Cotterill went into the Dunnage bottom lock alone, in the dark. Somebody
  was there when he came out." No date is new, so `TIMELINE.md` is
  unchanged; nothing settles the baby.
* **Looked at** (0.1): `propsheet.py` over Map 70 - the three cells of the
  `Metal Ladder` and `Jail Bars`, all what the text calls them. The first draw
  had brick to the map edge and `Wall Moss`, which is a green fern and read
  as a bush in a drain; both gone. Shots: undarkened (layout), the dark
  (`spa2_dark.png` - readable, Spare alone), the paddle, and out at the
  basin in daylight (`spa2_out.png`). Cotter's corner of the town was not
  touched and needed nothing.
* **Scenarios**: `q_spa2_tubes` 35 checks, all pass - walked by key presses
  from the ladder to the paddle and back, with the early climb-out. **Rerun**:
  nothing. `dunnage` and `q_hob1` talk to Cotter, but never with Spare, and
  the new pages need actor 11 or switch 213, which nothing else sets; no
  other scenario stands on Map 70 or (33,20).

**P1, the playtest fixes - done** (Part G, "Before G"): NIX-5's Repel and
PIP-3 fought by Piper alone. `db.build_mothballs` (new), `q_nix._nix5_mothballs`
(new), `q_piper._pip3_battle`, `db.build_contest`, and one goods line in each
of four shops. Built in two commits: the first had no cooldown, and Mike
asked the right question of it (below, "And then it wants airing").

* **The walk, measured** (a shortest path over Maps 9-10 with the engine's
  own passage rules and the first-page blockers): **92 steps on Map 9 and 28
  on Map 10**, every one of them in region 1, which is the only region the
  wood's encounters are listed for, and none on a bush. The count is
  `randomInt(26) + randomInt(26) + 1`, halved per step by Nix, and **re-rolled
  on every transfer** (`Game_Player.locate`), so the two maps are two
  independent draws: with Nix alone the escort gets through about **one night
  in fifty** (1.9%). Mike's "luck" was generous.
* **That last fact decided the mechanism.** A Repel that adds to
  `_encounterCount` would be thrown away at the map change. So the Repel is a
  **state**: **State 44, Mothballs** - Party Ability Encounter None, removed
  by walking after **50 steps**, with a message ("Bram no longer smells of
  mothballs."). While it is on the count does not move, so the next encounter
  is pushed back exactly that far, and Nix's half applies to every step after:
  the two stack, which an Encounter Half trait would not. It survives the
  transfer, and the inn (Recover All) takes it off.
* **And then it wants airing** (Mike, 7 Oct 2026: "does that not negate the
  need for Nix?"). It did: a twist used every time the last wore off covered
  any walk, with Nix or without. So the item runs **Common Event 6**, which
  stamps `$gameParty.steps()` into **variable 32** (`build_game.py`'s list
  grown to 33): inside 75 steps of the last twist - 50 worn, 25 airing - the
  new one goes back in the bag, "The last lot is still airing. Give it a
  while.", and nothing is spent; otherwise the state goes on the first
  living battle member, "The smell is extraordinary." Party steps, so
  another member's coat is no way round it. The cost is that it closes the
  menu, as Spare's Copies does.
* **Item 74, Mothballs**: 30 gold, menu only, no target (the common event
  picks), icon 208 (the tied pouch). "A twist of paper, very strong. Nothing
  will come near you for 50 steps. Then it wants airing." Sold at **Nix's Emporium** (Map 7), **the Chandler's**
  (Map 13), **Wick & Barrow** (Map 16, both of Mrs Barrow's pages) and **the
  Parish Rooms** (Map 25, `PARISH_STOCK`), after each one's last consumable.
  Not at Gideon's (his list is his own joke) or the market stalls.
* **The odds, per night** (exact, over both draws): a twist covers 49 steps
  outright, because the fiftieth walks it off in `onPlayerWalk` before
  `updateEncounterCount` counts it at Nix's half. One twist at the mouth,
  **56%**. Twisted at the mouth and again the moment the airing allows -
  which leaves 26 steps of Map 9 bare - **87% with Nix** (85% for a party
  that wanders a tenth further) and **48% without**. So a careful player
  usually makes it, and Nix is what makes it usually. A longer airing was
  costed and rejected: 40 steps is 69% / 8%, 50 is 65% / 5%.
* **Bagshawe mentions it** at the mouth, every night - a new block after
  either telling and before "Take him through / Not tonight", so nothing he
  said is changed: "Mothballs, mind. The Band keeps the uniforms in them, and
  nothing has come near the Band in years." / "Any shop has them. Fifty steps
  a twist, and then you want another twist - not straight off. They want
  airing." / Nix: "Halved and mothballed. Belt and braces." (The second box
  was reworded in the airing commit; it had never been played.) (`_nix5_mothballs` asserts `MOTHBALL_STEPS == 50`,
  because he says fifty.)
* **PIP-3 is Piper alone.** `_pip3_battle` sets the party aside in
  `$gameTemp` (safe: nothing can be saved while an event runs, as in
  `q_spare._argument`), makes it `[PIPER]`, rests her, fights, and puts the
  party back **after the 604**, so both branches restore it. The lose
  branch's `Recover All` now recovers only her, which is all it needs to.
  One new narrated line before her set, a continuation: "The rest of you are
  shown to the bench by the door, / and told, kindly, that it is Piper's
  set." Scores, lines and the rosette are untouched.
* **Troop 41, retuned for one performer.** Everything is read off Piper at
  the start of the battle, in the troop's turn-0 script that already sized
  the room's patience, so it is the same fight at any level or kit: patience
  is **3.5 Epic Finales** each for the back table and Miss Moon and **4** for
  Mr Dray (`4 * mat + 2 * agi`); the back table's ATK and Mr Dray's MAT are
  set so a Heckle or a Serpent Solo is **14% of her HP**; Miss Moon's MAT so
  a Sad Verse takes **6% of her MP**. No skill or enemy record changed.
  `balance.py` showed the old numbers doing nothing to her at all (Heckle
  `48 - 87`, zero, at level 15) and its four-person ceiling is the wrong
  question for one, so the tune is a Monte Carlo of the engine's rules
  (speed order, variance, Encore below half, the MAT debuff, MP damage, TP
  by damage): **never heals, 61-90%** from level 9 to 15 in about seven
  turns; **a potion or two at a third of her HP, 93-99%** in nine or ten.
  Epic Finale's flat 30 MP is why a higher-level Piper finds it easier.
  Losing still costs nothing.
* **Found, not fixed - Mike's call.** Every buff and debuff in `db.py` is
  written `effect(31 or 32, param, 0 or a rate, turns)`, but the engine
  reads a buff's **turns from value1** (`itemEffectAddBuff`), not value2. A
  0-turn buff is removed at the end of its holder's next action
  (`onAllActionsEnd` -> `removeBuffsAuto`), so it never reaches the caster's
  next action at all, and lasts an ally one action - Piper's Ballad of
  Adequacy and Foreshadowing do nothing for her alone. A debuff with 0.6 or
  0.5 in value1 (Portentous Shriek and Doom Monologue) goes negative at
  the first turn end, is never "expired", and lasts the battle. Talks
  Through It (`effect(32, 4, 3)`) is the only one written the engine's way.
  It is game-wide - fixing it moves every fight - so it is not in this step;
  PIP-3 was tuned with the buffs doing nothing, and would get a little
  easier.
* Tropes **+0**, blushes **+0**: still **+50 fixed** and 2-9 from PIP-2,
  **+13 fixed** and 0-1. Nothing dated; `TIMELINE.md` unchanged. No ending
  line: these are mechanics.
* **Looked at**: nothing drawn changed. The solo battle's screenshot
  (`q_pip3_battle.png`) and the night shot (`q_nix5_night.png`) from the
  scenarios.
* **Scenarios**: `q_nix5` **42 checks, all pass**: Bagshawe's new lines
  both nights (the first night's `advance` had to go from 30 to 45 presses
  for them), and on night three a twist used the way the menu uses it
  (`useItem`, then `applyGlobal` reserving common event 6) - fifty steps on
  the state, the step stamped; a second straight away given back, still
  airing; four steps walked on an encounter count of one with no fight; the
  wear-off message, and the step it wore off on counted at Nix's half (40 to
  39.5); refused at 74 steps after the stamp and taken at 75; then through
  as before. `q_pip3` **48, all pass**:
  troop 41 fought by `[7]` alone, rested from 1 HP, sized exactly as the
  script says, the bench line, the party back; then a **second contest lost
  on purpose** - she finishes anyway, the same scores, the party back, her on
  her feet, Bram never in it. (Killing the only actor while her command
  window is open does not end a battle; the scenario calls
  `BattleManager.checkBattleEnd()` after it.) **Rerun because a shop's
  stock count is asserted**: `audit_fixes` (the Chandler's, 4 to 5),
  `lighthouse` (Wick & Barrow, 15 to 16), `clanging_cast` (the Parish Rooms,
  9 to 10) - all pass; the airing commit changed no shop. **Not rerun**: `q_mer2` and `two_hundred` open
  Mrs Barrow's shop and close it without counting; `journey`, `q_cor1`,
  `q_wre1` and `q_zeph4` pass the mouth without both Nix and switch 3, so
  they see the page they always did; `blushes` and `q_wre3` are in the wood
  but never at the mouth or with the escort on; the `q_rol*`, `wall_ring` and
  `dunnage` runs stand in the Bell but never start Mrs Harbottle's contest
  page, which needs `SW_PIP3_ON`; troop 41 is fought nowhere else.

**P2, part one - Mike's Door and island, done first** (7 Oct 2026). Mike drew
P2's last item in the editor before the step began, so it went in first:
the mountain behind the Door into the Mountain, and the Former Premises as a
floating island. **P2's other six items are still to do.**

* **His edits, carried into the build.** The editor saved ten files; the
  real changes were Map 8's tiles, two flags on tileset 8, and
  `package.json`'s name (the editor's own "rmmz-game", put back). The rest
  was `2.0` written as `2`, and event 44's name mangled to "¿"; the build
  writes those as they were. Map 8 is `worldmap.json`, written only by
  `build/worldmap/run_finish.py`, which was checked to reproduce it byte for
  byte before it was touched. His tiles are two literal tables there:
  `MOUNTAIN_DOOR` (two overlapping `Rock Mountain` stamps behind the
  `Tunnel`, the massif carried to x=31, the road moved east to x=32) and
  `ISLAND` (`Floating Continent (Castle)`, `Floating Continent` and its
  `(Shadow)`, 2x3 on layer 1 over open sea). The built Map 8 equals his
  file on every tile layer; the region layer differs on three cells that
  are mountain now and on the island, which is region 0 as before.
* **The flags** are set in `build_game.build_tilesets` after tileset 1 is
  copied to 8, or every build would undo them: the castle row (240-241)
  loses its star, as Mike did, so it is ground; **the shadow row (250-251)
  gains one** - stock, it is open and not a star, which made two cells of
  sea a party could land on and walk about. The middle row is a star
  already, so the sea decides. In `run_finish`, which reads tileset 1, the
  shadow reads as land, so `sink_islets` is told to spare it.
* **Getting in** (Mike chose "land, then prompt"): nothing may stand on the
  castle row, because `Game_Vehicle.isLandOk` refuses a square with an
  event on it - with a door on each cell there was no way in at all. So the
  site's two events moved to the row underneath: **Map 8 event 43** is a
  parallel watcher, which asks "Go in / Not yet" (the old door's text,
  unchanged) once the party is standing on either cell, and asks again
  only after they have been back in the airship -
  `$gamePlayer._premisesAsked`, which a save keeps; **event 44** is empty
  and keeps its id, so nothing after it moves. The airship lands on either
  cell; "Not yet" leaves the party standing there and the action button
  takes off, as it always does out there.
* **Getting out**: Map 42's door marks the question answered and puts the
  party on whichever castle cell the airship is on (`places.PREMISES_LAND`;
  `PREMISES_STEP` is the east cell, if she is somehow on neither). Both
  destinations carry `<airreturn>` and `validate.py` asserts each is
  airship-landable. **`Game_Vehicle.pos()` is false off the vehicle's own
  map**, so from the hall the check compares `x` and `y`; the first draft
  used `pos` and always put the party on the east cell.
* **The mountain door** is reached from outside only across the chapel's
  door now, choosing "Press on" (Mike: that, or from inside Hithermost), as
  (31,21) is mountain.
* **Looked at**: the island with the question up (`premises_door.png`) and
  after coming out (`premises_out.png`) - the parked airship is under the
  party, which is how the engine draws it.
* **Scenarios**: `premises` rewritten for the island - both cells landable
  and nothing round them; land east, asked, the hall as before, out east
  and not asked; off, land west, asked, Not yet and not asked again, off
  and down again, asked, in, and out west - 37 checks, all pass. `hithermost`'s
  last leg walks onto the chapel's door, presses on, and steps up onto the
  mountain door: all pass. Nothing else lands at the Premises or walks the
  pass (`q_spa1_letters` goes straight to Map 42 by `goto`).

**P2, part two - the early maps, done** (7 Oct 2026). The six items left after
part one, in the order given, one commit each. **P2 is finished.**

* **Door holes** (`build_game.door_holes`, a pass after every module like
  `shape_wall_tops`). A `!Door1` sprite's open frames are see-through, so an
  opened door showed the wall it was painted on. Every door sprite set in an
  A3 wall now has the sheet's doorway under it on layer 3, as the sample lays
  it under all of its own: Outside_B 132 (`mapkit.DOORWAY_DARK`) and
  SF_Outside_B's `Entrance A`. The Safety Valve's canopy already has layer 3,
  so its doorway is on 2, under the star. 36 doors on 15 maps, one cell each;
  the Churchyard Gate, in a fence, is left opening onto grass. The doorway is
  open ground, so the player's step forward after the door opens now really
  steps into it before the transfer - one more step, the same destination.
* **Shadows** (`build_game.cast_shadows`): there were none in the game. The
  sample's rule, `ROOMGEN2-CORPUS.md` 1.20 - the left half of a cell whose
  west and north-west neighbours are A4 wall - which reproduces 83 of its 99
  interiors exactly. Layer 4 only, on all 47 maps on tilesets 3, 4 and 6.
* **The forest rings.** `TREE_DARK` is not a darker tree but the sheet's
  forest canopy, a block that only tiles with itself; alternated with `TREE`
  it was a whole tree, then four quarter-trees cut off square. Six towns had
  it (Thistlewick, Nether Sopping, Firstfield, Penultima, Restwell, Little
  Gore); they are all `TREE` now, as Gladhollow already was. The Gloamwood's
  outer wood mixed the two over the whole map and is all canopy now, like
  its Deep. The sample never lays the canopy on Outside at all; `mapkit.py`
  says so at the constant. A whole tree's crown is a star, so the ring's
  crown cells are walkable behind the leaves, as Gladhollow's always were;
  Map 9's region layer loses the 232 crown cells the canopy now covers.
* **Invisible walls** - a new `validate.py` check (the workspace's): a page
  at "same as characters", not through, with no picture, on open ground the
  flood reaches, with nothing on layers 1-3 and no other event drawn on the
  cell. BasicSample: none. Here it found four props and the Guild's mat:
  the **Obligatory Tower's basin** and the **Pit's hamper** were text on bare
  floor - the Dungeon sheets have neither, so tileset 4 borrows Inside_C into
  its empty E slot (tileset 3's flags, as SF Inside and Outside already do)
  for `Large Basin` and `Basket A` (`mapkit.DGE_BASIN`, `DGE_HAMPER`); the
  **lighthouse's ledger** and **Penultima's parish notice** were each one
  cell above the desk and the barrel they describe, and moved onto them.
  The Worm (decided in ROL-2: never drawn) and Mr Pocock (a voice in the
  dark) are meant, and say `<unseen>` in their notes. Thistlewick's anvil
  is one event and Beatrice another on the same cell, which is why a
  picture on any event on the cell counts. **`build_tilesets` now runs
  first**: `paint_regions` reads the flags on disk, and run last, a
  tileset change took two builds to settle.
* **The Guild** (Map 15), relaid as a registry office: Pell behind a
  five-table counter (he is at (9,5) now and talked to across it), the
  register and a scroll on it and the world map behind him; the bounty
  board three posted notices on the wall where it was one under crossed
  swords; the Filing a long bookcase, a tall one and a chest of drawers,
  where it was a **shield** - which is what "a shield standing in for a
  sign" was taken to mean, the thing you read being a shield - and the
  "cabinet" beside it was a bread shelf; a bench for the queue; a table for
  filling the forms in at; the Charter a stone tablet by the door; a sword
  rack and a barrel in the corner. **The mat is drawn** - a one-cell rug on
  the floor-art layer, in the doorway - and is "below characters", searched
  by standing on it, where it was an invisible wall at (8,10). Outside, the
  Guild's second sign was the **eatery's plate**; it is `Shop Sign (Crest)`.
  Positions are `south.GUILD_*`. Cropped with `propsheet.py` after: twenty
  tiles, each what it is named. **If Mike meant the shield as something
  else** - the crest sign outside is a shield-like badge too - it is one line.
* **Bram's sword** was never drawn: event 4 sits on the hearth because
  nobody can stand next to the wall. **Map 2 event 7** is the picture, Inside_C
  `Sword A` on the wall above the mantel at (10,2). Event 4's take page
  switches it off as its first command, so the sword leaves the wall as "The
  sword comes off the wall" appears - one non-dialogue command added to that
  page, no line changed - and event 7's parallel page watches event 4's
  switch A for a save made after the sword was taken, then retires.
* **Not touched**: `TREE_DARK` elsewhere (only the Deep and the Gloamwood use
  it now), and the buff/debuff `value1`/`value2` question from P1, which is
  Mike's.
* **Scenarios**, chosen by what each change reaches. Shadows are layer 4
  and change nothing a walk can meet. The door holes add a step into the
  doorway after any town door opens; the rings change what is walkable at a
  town's edge and inside the Gloamwood; the Guild and Bram's house changed
  under two scenarios each. So: everything that walks Maps 1, 2, 13, 15, 28
  or 31 by key (`reachable_home`, `reachable_village`, `q_hob2`, `q_hob3`,
  `q_wre5`, `reachable_sopping`, `q_mer2`, `guild`, `firstfield_graduation`,
  `q_spa1_letters`), `opening` and `q_nix3` for the sword and the Guild, and
  the door walks of `reachable_clanging` (the canopy door), `restwell`,
  `hamlets`, and `ashcombe` and `dunnage_company` for the two doors that
  refuse. Nothing walks Map 9 by key. `guild` now walks onto the mat and
  presses Enter instead of starting the event. RESULTS

---

## Restart prompt

**Start with P3, Olde Evermore's elves** (Part G, "Before G: the playtest
round", 7 Oct 2026), not G1. **P1 and P2 are done**: P1 the NIX-5 Mothballs
and PIP-3 solo; P2 the early maps in two parts - Mike's Door and island,
then the door holes, interior shadows, the forest rings, `validate.py`'s
invisible-wall check and the four props it found, the Guild relaid, and
Bram's sword on the wall (the last two Done paragraphs in section 3). P1
found a game-wide buff bug that waits on Mike's word. What is left of Mike's
playtest list, in order: P3 Olde Evermore needs more elves about doing
things (Maps 38-39, `evermore.py` - read `SITES.md` step 4's Done paragraph
and `evermore.py`'s docstring, which says what it may not contradict);
then P4 the post-game with the Door into the Mountain and G1's ending
lines. G0, the quest log, follows its plugin (`../QUESTLOG.md` Q0-Q7, a
parallel effort in `trial-chamber`). Last come G1's counter re-cuts, the
one full suite, Mike's playthrough, and the push. Read Part G's playtest
round and the step's own bullet; the paragraph below is still the plan for
G1's ending lines, which are written in P4.

Continue Thistlewick's **companion quests** in
`/home/mike/Projects/rpgmaker-mz/thistlewick` with **step G1, the ending**
(`QUESTS.md` Part G). **Parts A-F are done** (F4, SPA-2 Ninety Tubes, 6 Oct
2026): every companion quest in this effort is built.

G1 is one `if_then` block per companion on `SW_<NAME>_STORY` (and Spare's,
110) in `journey.finale_event`'s tally before THE END, each choosing **one**
line from that companion's candidate ending lines - every step's Done
paragraph in section 3 names its candidates - and one closing line on
`VAR_COMPANION_STORIES`; `finale_ending` extended to assert them. Then both
counters re-cut against the finished totals (below), the comments above both
branches updated, and `CLAUDE.md` "The ending" amended. Nothing may settle
Spare's baby (SPA-3 is owed, past the ending). **Then the full suite, once**,
`../tools/scenarios.sh .` in the background, budgeted at eight hours. Then
Mike plays it; nothing is pushed until he has.

Read section 0, Part G, and **only the candidate-line bullets** of the Done
paragraphs (grep "Candidate ending line"), once, at the start. Read
`journey.finale_event` by dumping the finale's event, not by opening the
module first.

Per step, exactly as before: `build_game.py`, then a `git diff --stat data/`
that touches only what the step meant to - and compare old pages byte for
byte. `validate.py`, and `apidigest.py . --write`. The finale's own scenario,
then the suite.

Where things stand: tropes **+50 fixed** and 2-9 from PIP-2; blushes **+13
fixed** and 0-1 from PIP-2 - the totals G1 re-cuts against. Next free: switch
214, variable 33 (`build_game.py` sizes the list at 33, so **the next
variable needs it grown**), item 75, weapon 44, armour 49, armour type 15,
weapon type 14, element 11, class 13, common event 7, state 45 (past the
40-44 block, which P1 filled), enemy 60,
troop 55, skill 185, map 71, `Gen_People15` 4. Spare is actor 11; his story
switch is 110 and is on after F2. Cotter (Map 61 event 12) has six pages now;
Map 70 is the culvert.

Things learned that will bite again:

* **`R.script` takes a list of lines.** Handed a string, it writes one
  character per line and the event hangs where the script was (D1).
* **One quest module per companion holds several quests**; prefix private
  helpers per quest (`_cor1_`), and treat a data diff on a map the step never
  meant to touch as a bug.
* **"Afterwards" is the person's own last page plus one line**, on a page
  above the quest's, conditioned on their ladder's terminal and the done
  switch. Avoid an owner another quest already gave an afterwards page
  (Mrs Ash, Mr Weir, Mrs Dimmock and the Ashcombe notice are taken).
* **A published first page that is wrong with the companion standing in
  it** is skipped by setting the owner's terminal self switch by script from
  the step before (ALD-4, COR-1), and the quest page carries what of it is
  still true.
* **A published reaction shot stays the first visit, word for word**: start
  the quest on a second look (WRE-1's shelf, COR-1's Roll).
* **A map in no place** is drawn in the quest module, registered in
  `build_game.MAP_NAMES` with a `build()` call beside the place modules',
  and its id goes in `places.py` (COR-2, Map 66).
* **The Outside sheets' `Dirt` reads as beach sand.** For wet ground, lay
  `Soil` (A2 kind 31, an overlay) over it on layer 1; `!Chest` 5 is the iron
  box, 0-3 are treasure chests.
* **A long speaker name eats the first line.** Check every line at once with
  `story._check_width` patched to collect.
* **Waiting on a background run:** wait on the log's last line ("all checks
  passed" / "N FAILURE(S)"), never on a `pgrep -f` that matches itself. A
  killed run leaves its Chromium: kill the browser whose parent is 1. And
  never `pkill -f` a pattern that is in your own command line: it kills the
  shell running it (E4).
* **`advance` budgets run short on published first pages**, which are often
  long: Mordaunt's took more than twenty presses. "still busy" then a `goto`
  that never arrives is the budget, not the page (E1, E4).
* **A new `db` constant can rebind an old one.** `EN_WISP` and `SK_LULLABY`
  were already taken, and the build silently moved two troops and a class
  learning to the new ids. Grep `db.py` for a name before using it; the
  data diff is what caught it (E7).
* **An appended page that would shadow another quest's page can carry it**:
  `q_piper._pip4_carry(pages)` rebuilds the engine's page choice as a chain
  of script conditions, so the new page shows what would have shown and then
  its own part (E12).
* **A turn-count fight can be fought for real in a scenario**: wrap
  `Game_BattlerBase.isAutoBattle` true for actors and `advance` through it
  (q_ald2). Kill the party only after any screenshot, and press through
  the defeat message.
* **An old scenario can be stale against a later step's design**: `q_hob3`
  (A8) asserted nothing runs in the smithy, and HOB-2 (A13) made that the
  autorun where Beatrice goes quiet; nobody reran it until E13-E15. When a
  step adds an autorun or a page to a room, rerun the older scenarios that
  stand in that room.
* **`$gameParty.numArmors` is not an engine method**; `numItems` takes an
  armour or a weapon too (E14).
* **A splice inside somebody else's command list is found by a line, and
  asserts the line is there**: `q_roland._rol2_sword_at` finds Roland's "Take
  it up there" and puts the drawn sword before it, at that command's indent
  (`R.shift`). A page that needs two such additions on two switches is two
  more pages, one per switch and one for both (E17, E18).
* **A fight in a scenario needs a long `advance`**: at headless battle speed
  sixty presses ran out while the battle was still up, and every check after
  it cascaded. Kill the troop at about frame 60 and give `advance` 250 (E18).
* **A room shrunk after it was drawn can lose its doorway**: the corridor was
  a fixed range and the smaller room left a row of rock across it;
  `validate.py` said the Worm could not be reached. Derive a corridor from the
  rooms it joins (E18).
* **Seal Equip (trait 54) is not "cannot be changed"; Lock Equip (53) is.**
  Seal takes the slot away, so `setup()` silently drops the weapon and every
  skill with a required weapon type goes dark - the actor fights bare-handed
  and nothing says so. Assert the kit at the start of a scripted fight (F1).
* **`BattleManager.abort()` only sets a phase**: with a message window open
  in the battle, it waits. A scenario that ends a battle it started itself
  should clear the message and call `processAbort()` (F1).
* **The end-of-part rerun by map id is the whole suite** once Maps 1, 8, 13
  or 14 are touched. Choose by what each change can reach and write the
  reasoning down (the E1-E6 rerun paragraph).
* **A `pgrep -f` waiter matches its own command line**, every time the
  pattern is in it - and a log from an earlier run already says "all checks
  passed". Wait on the background task's own notification, or on a log you
  truncated first (F2).
* **A transfer out of Upper Clanging by an event, not a door, keeps the
  rain**: weather lives on `$gameScreen`. Dry it before the transfer, the way
  `north.door` does (F2).
* **`validate.py` cannot see a sealed corner whose event is read from
  beside**: F3's maze had its only corridor walled across, and the stump at
  its centre - an action-button event on a blocked tile - checked clean.
  Flood from the arrival and ask about the cells you stand on to read things.
* **`K.HEDGE` is an overlay** (A2 `Bush`, flags `0xe40`): on layer 0 it draws
  with black round it, and it is wadeable, not a wall. Put it on layer 1 over
  grass (F3).
* **Two presses to leave an interior is one too many**: the second lands
  on the street after the transfer and walks a step (F3's scenario).
* **A party set aside across a transfer belongs in a variable, not
  `$gameTemp`**: `$gameTemp` is not saved, and a map the player walks about
  on has a menu with Save in it. A variable holds the array and is (F4).
* **A transfer re-rolls the encounter count** (`Game_Player.locate`), so
  anything that adds to `_encounterCount` is gone at the next map. P1's
  Repel is a state with Encounter None, walked off (P1).
* **Three scenarios count a shop's stock** - `lighthouse` (Wick & Barrow),
  `audit_fixes` (the Chandler's), `clanging_cast` (the Parish Rooms). A
  goods line added to one of those shops is a count to change (P1).
* **A new box before an old choice outruns old `advance` budgets**: q_nix5's
  first night needed 45 presses once Bagshawe mentioned the mothballs (P1).
* **`Game_Vehicle.pos()` is false off the vehicle's own map**: ask an
  airship where she is from an interior with `.x`, `.y` and `._mapId` (P2).
* **A choice that opens the moment something lands** has its default fixed
  when it opens, so `window._pick` goes on *before* the landing, not after
  (P2's `premises`).
* **To reach a choice in a scenario, set `window._pick`** (the hook in the
  setup eval wraps `setChoices`' default) and `advance` through: no counting
  presses to the choice window (F1's idiom, F4).
* **A tileset change took two builds to settle**: `paint_regions` reads
  `Tilesets.json` off disk, and `build_tilesets` ran last. It runs first now;
  after any flag or slot change, build twice and `cmp` anyway (P2).
* **A searchable thing with no picture is an invisible wall** unless a tile
  draws it on its own cell - and twice the tile was one cell away.
  `validate.py` reports it now; `<unseen>` in the note says it is meant (P2).
* **`TREE_DARK` is forest canopy**, only for a solid wood; a ring of trees is
  all `TREE` (P2).
* **An event can be a picture with a parallel watcher** when the thing taken
  is on a cell nobody can stand beside: the take page switches the picture's
  self switch, and the watcher covers saves from before the picture (Bram's
  sword, P2).
