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
| Piper | *nothing in her five gives gear* - decide in her first step (A3) | | |
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

---

## Restart prompt

Continue Thistlewick's **companion quests** in
`/home/mike/Projects/rpgmaker-mz/thistlewick`. `QUESTS.md` is the queue: read
its section 0 and the Done paragraphs, then build the **next step** - A3,
PIP-2 A Rhyme For Turnip - reading only Piper's section of `COMPANIONS.md`. Nothing is
pushed in this effort (0.1). Per step: `build_game.py`, a `git diff --stat
data/` that touches only what the step meant to, `validate.py`, screenshots
of anything drawn, and the step's own scenario - run it under `stdbuf -oL`
or it prints nothing until it ends. No full suite until G1. Write the step's
Done paragraph and move this prompt on by one.
