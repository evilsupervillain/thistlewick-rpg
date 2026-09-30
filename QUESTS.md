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
| Hob | the best weapon for him, forged badly on purpose | HOB-2 | A13 |
| Zephyrine | a robe with a stat line | ZEPH-1 | C1 |
| Nix | the coat (armour, and it fits) | NIX-1 | B5 |
| Aldric | the shield | ALD-2 | E7 |
| Piper | the rosette for second place (accessory) - she frames the certificate and wears the rosette; decided in A3 | PIP-3 | B3 |
| Corvin | the scarf, the wrong colour (accessory) | COR-1 | D1 |
| Wren | *nothing in her five gives gear* - decide in her first step (A1) | | |
| Roland | the better sword he leaves at the door | ROL-2 | E18 |

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
| E18 | ROL-2 Roland's Own Quest | nothing | a small dungeon (66+), the thing, the better sword |

### Part F - Spare (`SPARE.md`, `q_spare.py`)

**F1. Spare joins.** `SPARE.md` whole, with its switches renumbered to 89-92
first. **Blocked on art** (section 1): his side-view battler and Mrs
Cotterill's enemy image. Build everything else, and ask Mike for the two
images when this step is reached rather than at the very end, because
`validate.py` fails without the battler. **F2. SPA-1 The Letters**, **F3.
SPA-3 The Tenth**, **F4. SPA-2 Ninety Tubes** (a confined map, 66+).

### Part G - the ending, last

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
  "Breeds March to October, and is enthusiastic about it", written down under
  Bram's name. Running tally for the effort: **tropes +2, blushes +1**.
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
* **No trope** (the quest has no cliche, like ROL-4). **One blush**: Ott
  tries each of the forty-one holes with her little finger - "Tight. All the
  way round." Running tally for the effort: **tropes +3 fixed and 2-9 from
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
  (`build_game.build_tilesets`); `mapkit.clanging_in(sheet, name)` names a
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

---

## Restart prompt

Continue Thistlewick's **companion quests** in
`/home/mike/Projects/rpgmaker-mz/thistlewick`. `QUESTS.md` is the queue: read
its section 0 and the Done paragraphs, then build the **next step** - A8,
HOB-3 The Anvil - reading only Hob's section of `COMPANIONS.md`.
Nothing is pushed in this effort (0.1). Per step: `build_game.py`, a `git
diff --stat data/` that touches only what the step meant to, `validate.py`,
screenshots of anything drawn, and the step's own scenario - run it under
`stdbuf -oL`, and in the background if it is long, or it prints nothing until
it ends. No full suite until G1. **Any old room a step works in that looks
wrong is fixed in that step** (0.1, "Fix the room you are standing in"): crop
its props before judging them, and run the scenarios that walk it. Write the
step's Done paragraph and move this prompt on by one.
