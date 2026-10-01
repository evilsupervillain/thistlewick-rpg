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
  Courting." / "...All at once?" / "It's the only way they know how."
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
  the TANG" - and Corvin looks at the ceiling (**one blush**). **No curse**:
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

* **The start is the shelf** (Map 59 event 5, which has one page with her
  reaction shot in it). Page 2 is hers - that reaction, kept, and then one
  of the Library's cards tucked into the inch-wide gap: A MONOGRAPH OF THE
  COLLEGIUM REQUIRES (I) A TYPE SPECIMEN FOR EVERY ENTRY; (II) THREE FELLOWS
  TO REVIEW IT; (III) A LIST OF SUBSCRIBERS. "Rowbotham named three hundred
  species and never had a type specimen for one of them. He named them after
  his dogs." `SW_WRE1_ON`. **One trope** (the collect-them-all). The same
  page counts what is left (`\V[24]` of eleven, three reviewers, six
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
* **Scenario** `q_wre1`: passes (44 checks): two specimens fought (one
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

---

## Restart prompt

Continue Thistlewick's **companion quests** in
`/home/mike/Projects/rpgmaker-mz/thistlewick` with **step D1, COR-1
Ashcombe (New)** - the first of Part D, Ashcombe (Maps 52-53,
`ashcombe.py`). Part C, the Collegium, is done (C1-C4, 1 Oct 2026). One
step per session again (0.1): Part C's override was for Part C only.

Read section 0, the Part D entries and the Done paragraphs from B1 on,
once, at the start; then **Corvin's** section of `COMPANIONS.md`, and no
other companion's. Read what the step needs by dumping Maps 52-53's events
and their text, not by opening a module. Ashcombe has **never been swept**:
crop Maps 52-53 with `propsheet.py` before judging, and screenshot before
and after anything changed (0.1).

Per step, exactly as before: `build_game.py`, then a `git diff --stat data/`
that touches only what the step meant to - and compare old pages byte for
byte: every existing page identical, only appended pages and new events.
`validate.py`, and `apidigest.py . --write` / `tileaudit.py . --write` if a
signature or constant moved. Screenshots of anything drawn, looked at. The
step's own scenario, `build/scenarios/q_cor1.json`, run in the background,
one browser at a time. Then the Done paragraph (ids taken, tropes and
blushes, running tally, candidate ending line, rooms fixed), a commit, and
this prompt moved on to D2. Nothing is pushed. No full suite until G1.

Where things stand: tropes +24 fixed and 2-9 from PIP-2; blushes +11 fixed
and 0-1 from PIP-2. Next free: switch 170, variable 25, item 65, weapon 42,
armour 44, armour type 11, class 12, common event 4, state 41, enemy 55,
troop 53, skill 179, `Gen_People13` 5. Corvin's gear is **the scarf, the
wrong colour** (0.5): an accessory of a new armour type 11 plus one trait on
his actor, the badge pattern (types 7-10 are Wren's, Piper's, Nix's and
Zephyrine's). He already has the elective curse, state 40, from COR-5, and
the name on the tang belongs to COR-2, not here.

What D1 will need deciding, so make the call, say why in the Done
paragraph, and keep going:

* **The door.** Event 3 on Map 52 carries Corvin's refusal at pages 1-2;
  COR-1's page goes after them, the way ZEPH-1's went after Zephyrine's on
  the Collegium's world-map doors (`q_zephyrine.door_pages`) - check what
  the refusal pages need first, and decide what sends him back (ZEPH-1 used
  a letter at her old table; something of his own is better than a copy).
* **The study** - "the bedroom that is a study" - was **not built**. A new
  room in a built place is drawn by that place's module on its own map where
  it can be (0.4); NIX-2 widened Map 63 into its black east for the vault,
  which is the precedent if Map 53 has room.
* **The Flood Dinner's speaker, TO BE CONFIRMED** (event 9), and Mrs Ash
  knitting something long (event 2, Map 53): read both ladders before
  appending, and remember the terminal-switch rule.
* **New face?** Only if somebody new speaks; generate (`Gen_People13` 5).

Things learned in A6-C4 that will bite again:

* **One quest module per companion holds several quests**; prefix private
  helpers per quest (`_hob1_`, `_z1_`), and treat a data diff on a map the
  step never meant to touch as a bug. `q_corvin.py` exists (COR-5).
* **"Afterwards" is the person's own last page plus one line**, on a page
  above the quest's, conditioned on their ladder's terminal and the done
  switch. `q_zephyrine._afterwards` / `_plus` and `q_nix.returned` do it;
  avoid an owner another quest already gave an afterwards page, since two
  of them on one event shadow each other - and if you must, make the later
  page carry both lines (Hapgood's two in C2-C3).
* **A quest with two endings** (ZEPH-1: paid or expelled) sets a switch per
  end and one done switch, and every later page that cares branches with
  one `if_then` on the end switch. Test both ends in one scenario by putting
  the switches back between them.
* **A page with a companion that replaces somebody's own page must carry
  that page's list** - and on a second visit, only the part that is still
  true (WRE-1's shelf replayed Wren's whole reaction shot on every visit
  until it was cut back to the count; a scenario's `advance` ran out of
  presses on it and the next `goto` never arrived).
* **New events on a busy map go after everything else** so no existing id
  moves: `journey.world_map` appends WRE-1's eleven specimens after the
  placeholder doors.
* **A long speaker name eats the first line.** Check every line of a new
  section at once with `story._check_width` patched to collect rather than
  raise, instead of one build per error; `narrate` pages in fours.
* **Mapkit constants lie**; crop before using one somewhere new.
* **Gear only one companion can use**: a new armour type plus one trait on
  the actor (`db.build_actors`), and the type's name appended in
  `build_game` (`["Badge", "Rosette", "Coat", "Robe"]`). A **party ability**
  lives on a class; WRE-1 upgraded Wren's additively with a copied class (11)
  and Change Class (code 321) keeping experience.
* **Change Items' decrease is its own operation** (parameter 1), as Change
  Gold's is; `rmmzdata.gain_item` only increases, so set `parameters` to
  `[id, 1, 0, n]` (see `q_zephyrine._z2_vote`).
* **New faces**: `tools/chargen` settings in `build/characters/` (colour
  indices are in `CHARGEN.md`'s swatch list), a slot in `art.py`'s `SHEETS`,
  `python3 build/art.py` in the background, and a `story.FACES` entry; look
  at a `lineup.py` sheet first - `catalogue.py --base` to pick a part.
* **A fight in a scenario**: hook `Scene_Battle.prototype.start/update` to
  kill the troop 200 frames in (`q_wre1.json`); look at the battle once with
  `BattleManager.setup` and a shot. **A choice in a scenario**: hook
  `Game_Message.prototype.setChoices` so the default is `window._pick`, and
  `advance` then takes the branch you want (`q_zeph1.json`).
* **A shop in a scenario**: Enter through the text with long frame waits,
  assert `Scene_Shop`, buy with three Enters, out with two Escapes, and
  assert `Scene_Map` (`q_wre1.json`).
* **Waiting on a background run:** never wait with `pgrep -f` on a pattern
  that is in your own command line - it matches itself and the wait never
  ends. Wait on the log's last line instead, or on a pid. A killed run leaves
  its Chromium: kill the browser whose parent is 1.
