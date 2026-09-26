# The audit

Mike's list of things found by playing - faces that do not match, dialogue
that disagrees with itself - to be worked through **before** the companion
quests and **before** `SITES.md` section 4. It is a queue like `SITES.md`: one
item or part of one per session, a "Done" paragraph under each item as it is
finished, and a restart prompt in `AUDIT-NEXT.md` (untracked, like
`SITES-NEXT.md`) rewritten by each session for the next.

**Why now and not later** (decided 26 September 2026):

* **The editing window closes at the push.** Mike's rule for this audit is
  that `NORTH.md` 1.7's "nothing already in the game is changed" protects only
  what is **published** - what is on the `live-rpg` branch. Everything newer
  is free to change. Once section 4 pushes, all of it becomes published and a
  fix becomes a sanctioned repair that has to be argued in `NORTH.md` 8.1.
* **The quests stand on these characters.** Nearly every companion quest is
  an appended page on somebody who already exists, and several are about the
  Prophecy. Fix the faces, the genders and the timeline first, and no quest
  is written on top of a mistake.
* **One suite run.** Section 4's full suite, and its re-cut of the two
  counter thresholds, then cover the audit's changes too. The audit can move
  the trope and blush totals, and the thresholds are cut against them.

---

## 0. What is published, and therefore what may be changed

Measured on 26 September 2026:

* **`live-rpg` is `6168832`** (17 September 2026, "Say that Norbert's battler
  is drawn now"). `master` is 29 commits ahead of it.
* `live-rpg` has **28 maps** - Maps 1-28, Thistlewick to Firstfield Meadow -
  and **the old 50x50 world map**. The 120x120 world map, every world-map site
  and **Maps 29-65 are all unpublished**, and so is everything `SITES.md`
  built.

So there are two kinds of fix, and every item below has to say which:

* **Free:** content that is not in `live-rpg`. Change it; no argument needed.
  Check with `git show live-rpg:<path>` or `git diff live-rpg..master --
  <path>` before assuming.
* **Repair:** content that *is* in `live-rpg`. Allowed only where the game
  contradicts itself (`NORTH.md` 1.7's one sanctioned exception), and each one
  is written up in `NORTH.md` 8.1 with its reason. Where an appended page or a
  new line can explain the mismatch instead, prefer that.

A change to published content that is neither - "it would be better if" - is
out, and belongs in a conversation with Mike, not in a commit.

---

## 1. The order

Item 6 goes first, because it may rewrite lines, and faces should be checked
against the text that will ship. Then the fixes to existing faces, then the
new faces, then the look of the places.

| # | item | order | notes |
| --- | --- | --- | --- |
| 6 | the timeline, and every contradiction in the dialogue | **first** | may be two or three sessions |
| 4 | portraits whose gender is wrong, mostly children | second | existing faces |
| 3 | elves without pointed ears | second | existing faces |
| 2 | portraits that look noseless, mostly with moustaches | second | existing faces |
| 1 | speakers with no portrait at all | third | new faces, and a list for Mike |
| 5 | the Collegium's green roofs, and other visual contradictions | last | places |

---

## 2. The items

### 6. The timeline, and dialogue that contradicts itself

Mike's words: the biggest inconsistencies are **in the timeline, most
specifically regarding the Prophecy, and changes made to the timeline
regarding the Former Premises**.

* **First, print the timeline of the world as established so far**, into this
  file under this heading, as a table: year or relative date, event, and
  **where it is said** (module and function, or document and section) - every
  claim sourced, because the point is to find where two sources disagree. The
  spine it has to hold: the Prophecy and its clause twelve, the Dark Lord
  rising every hundred years, the forty-seven Chosen Ones before Bram (so
  roughly 4,700 years), Grimspite's "four thousand years" in the
  `CLAUDE.md` premise, the Former Premises and when the Dark Lord moved out of
  them, the Collegium's six hundred years, Fenmarch's generations, the Sky
  Anvil's 1749 meteorite, the Counting House sealed in 1802, ITEM 1's 1802 off
  the crag, the 199 attempts at flight, Weeping Bottom founded in 1702, Sump's
  1794, Ashcombe's flood, the Order of the Errant's pins, and the ages of
  everybody whose age is stated. **Note that "1802" appears twice** - Great
  Dunnage's Counting House and ITEM 1 - which is either a coincidence to keep
  or a collision to fix.
* **Then show it to Mike before changing anything.** The timeline is a
  judgement about which source wins, and he has views about the Prophecy.
  Propose the fixes as a list - what changes, where, and whether it is Free or
  a Repair - and make them once he agrees.
* **Then the rest of the dialogue**: facts that disagree between two
  speakers (names, places, who is married to whom, who is dead, distances,
  prices), a character described as something their sprite or portrait is
  not, and a line that promises something the game does not have. Each
  finding gets the same Free / Repair label.
* Where to look for the lore, in roughly this order: `CLAUDE.md`'s premise and
  "The ending"; `journey.finale_event` and the Prophecy item in `db.py`;
  `EXPANSION.md` and `NORTH.md` for what the south and the north established;
  `WORLDMAP.md` section 7 (7.4 is the Former Premises) and `SITES.md`'s Done
  paragraphs for what the sites added; `premises.py`, `evermore.py`,
  `coldbarrow.py` and `frostwick.py`, which each touch the spine. Their
  docstrings say what each module was told it must not contradict - start
  there before reading any dialogue.

#### The timeline, as the game states it (built 26 September 2026)

Measured off the built text, not the source: every Show Text, choice and
database description in `data/` on `master`, and the same off `live-rpg`, so a
line is **P** (published) only if the identical line is on `live-rpg`, and
**F** (free) otherwise. `C1`-`C10` are the contradictions, listed after the
table. Relative dates are "years before Bram sets out".

| when | what | where it is said | P/F | |
| --- | --- | --- | --- | --- |
| before the engagement | "Two thousand years of Dark Lords" in the castle on the cloud, "so that no hero could ever reach it. And no hero ever did." | `premises.hollowell_pages`; `WORLDMAP.md` 7.4 | F | C2 |
| ~4,800 years | the engagement begins; the Tower "Est. approx. 4,800 years ago - UNDER THE SAME MANAGEMENT"; "Four thousand eight hundred years, this job" | `journey.tower_events` (plaque), `journey.finale_event` (x2), `journey.item_one_scene`, `db.build_enemies` (Grimspite's note); `EXPANSION.md` 1 | P | C1 C4 |
| "four thousand years" | the same span, rounded: the mat, the Cache's hooks, "leaned on that wall every day of four thousand years", "Four thousand years, and she is the only one", Ott's "Four thousand years in the weather" | `journey.tower_events` (x2), `journey.finale_event` (x2), `north.ott_the_two_hundred`; `CLAUDE.md`'s premise | P | C4 |
| | "in four thousand years that wasn't binding" | `journey.visitors_book_pages` | F | C4 |
| 4,112 years | Mirabel born; "I was there when they signed it" - the Prophecy, signed three times each, and a horse beside clause twelve | `evermore.mirabel_pages`, `evermore` Archive copy; `BIOS.md` | F | C5 |
| "since the First Age" | Olde Evermore | `evermore` village sign | F | |
| every 100 years, 47 times | "Every hundred years the Dark Lord rises ... It has worked forty-seven times"; the Obelisk's 47 RENEWED; "renewed me forty-seven times"; the Cache "RESTOCKED EVERY CENTURY" | `village.hall_events` (Wispel), `journey.tower_events`, `journey.finale_event`; `CLAUDE.md`, `README.md` | P | C1 |
| ~600 years | the Collegium founded, by the Founder, in one afternoon | `collegium.arms_pages`, Founder | F | |
| ~500 years | the First Dean's portrait "pending for five hundred years" | `collegium.portrait_pages` | F | |
| 400 years | the Premises vacated for the Tower; the visitors' book empty since; 1,600 quarterly reports | `premises.hollowell_pages` (x3), `premises.hall_events` (x2), `journey.visitors_book_pages` (x2); `WORLDMAP.md` 7.4 (x2) | F | C2 |
| 1702 | Weeping Bottom founded by Mother Ursula Pym, for the sea air | `weeping_bottom.stone_pages` | F | |
| 1749, 1750 | the Sky Anvil falls, becomes Meech's great-great-grandad's gatepost; shrine built round it | `nomap._sky_anvil` | F | C9 |
| 1794, 1795 | Sump: wasps, the Water Committee wound up; "Cursed 1794"; "six generations" without sleep | `hamlets.thurle_pages`, `hamlets.sump_events` | F | |
| 1802 | the Hoyle Works' stores ledger begins; ITEM 1 | `field.stores_ledger`, `journey.item_one_scene` | P | C6 |
| 1802 | Great Dunnage's Counting House sealed, "when the key was lost"; the memorandum | `dunnage.mayor_pages`, `door_pages`, `memorandum_pages`; `COMPANIONS.md` NIX-2 | F | C6 |
| 1804 | an apprentice at the works since; Nib is the fortieth | `north.works_events` | P | |
| ~200 years | "Two hundred years I have been at this. Four generations of us"; 199 attempts; the Pit's lost property | `north.works_events`, `field`, `wilds` | P | |
| 1811, 1840 | Dame Honoria's portrait; Rollo the dog | `fenmarch.portrait_pages` | F | |
| 1819, 1838, 1852 | the unicorn bred; the Marsh Bear "taken by Sir Aldric the Second"; the phoenix | `fenmarch` case table (module level) | F | C7 |
| 1841 | the Clanging clock four minutes fast since - "and has been for sixty years" | `north.clanging_events` | P | C10 |
| 1886 | Attempt Eighty-Four comes down; her bay empty "for a hundred and forty years" | `field.eighty_four` (x2), `db.build_enemies` (x2), `journey.finale_event` tally | P | C3 |
| 198 years | ITEM 1 "has spent a hundred and ninety-eight years strapped down" since 1802 | `journey.item_one_scene` | P | C3 |
| ~100 years | the wayshrine's last entry, "Feeling good about this one!", "dated a hundred years ago" - i.e. #47 | `journey.world_events` | P | C1 |
| ~100 years | Attempt 112, "a hundred years dead" | `field` | P | |
| 91 years | the shipping stopped; the light kept since for "the ones coming back" | `south` (Bother) | P | |
| ~70 years | Mr Ottershaw, "ninety in March", has composed the animals for "seventy years. Three generations" | `fenmarch.ottershaw_pages` | F | C7 |
| 60 years | #41 Halloran Vance's goose "a wyvern in my house for sixty years" | `south.the_wyvern` | P | C1 |
| 41 years | Wick "went north. Same as they all do." | `south.outfit_events` | P | C1 |
| 40 years | #44 Ambrose Fitch home and "ignored for forty years", since dead; Ysolde (78) forty years a medic | `wilds.forty_fourth`, `south.ysolde_event`, Weapons 31 | P | C1 |
| 40 years | Perce breaks Frostwick's winter - "Everybody went north, that year"; the Eleven Days' book, two Chosen Ones "a century apart" and P. Stagg | `frostwick.frostwick_events`, `eleven_days_events` | F | C1 |
| 30 years | #45 Halbert Quy, "in his seventies", has "thought about a cup of tea for thirty years" | `south.quy_event`, `journey.finale_event` | P | C1 |
| 31 years | Gideon prices the Sword of Ultimate Ending | `penultima` | F | |
| 14 / 11 years | Sir Hamo at Weeping Bottom; Dame Winifred at Little Gore | `weeping_bottom.hamo_pages`, `hamlets.cope_pages` | F | |
| 12 years | a young knight with a dragon commission at the Wrong Dragon's - Aldric, ALD-6 | `nomap._wrong_dragon`; `COMPANIONS.md` ALD-6 | F | C8 |
| 11 years | Corvin in his corner, since nineteen; the flood was while he was away | `south`, `ashcombe` | P/F | |
| 9 years | Aldric "went out errant nine years ago and never came back"; the flowers under his portrait; Tom and Mrs Vane married at Fenmarch | `fenmarch.fourth_pages`, `portrait_pages`, `tom_pages`; `hamlets.vane_pages` | F | C8 |
| 6 years | Aldric arrives in Thistlewick and cannot find the north gate; Perpetua wakes on the beach | `db.build_actors`, `village.aldric_event`, notice board; `coldbarrow` | P | |
| recent | #46 alive on his log, his party writing monthly; #47 was the Old Man's boy | `journey.gloamwood_events`, `south`, `village.village_events` | P | C1 |
| 4 years | Mr Pilbeam and the eagle | `fairholme` | F | |
| now | Bram, #48. The calendar: 1802 + 198 = **2000**; 1886 + 140 = **2026** | | | C3 |

Consistent, and worth knowing so nobody "fixes" them: Aldric's **nine** years
out and **six** in Thistlewick (three on the road first); Ott's "Forty-six of
them have gone up that road" against forty-seven (#46 stopped in the
Gloamwood); Mrs Emberthwaite is seventy; the Fourth found the gate at ten.

#### The contradictions, and the proposed fixes

**C1 - the Prophecy's clock (P against P, the big one).** Thistlewick, the
Tower and Grimspite run on a hundred-year cycle: 47 renewals, 4,800 years, the
wayshrine's last entry a hundred years ago. The whole published south runs on
a clock about ten times faster: #41 sixty years ago, #44 forty, #45 thirty and
alive, #46 alive with his party, #47's father alive, Ysolde and Wick in living
memory. Frostwick (F) sits on the fast clock too - "everybody went north, that
year" was forty years ago, which is #44's year. Both halves are published and
neither can be repaired without re-voicing dozens of lines. Proposed:

* **(a) recommended - "a hundred years" is a defined term.** One new line, F:
  Pargeter reads the whole Prophecy (she is the one person who ever has) and
  finds that clause two defines "a hundred years" as *such period as the
  Committee shall find convenient*. Every published line then stays true as
  written - Wispel, the wayshrine, the Cache, and Grimspite's 4,800, which are
  the contract's years - and Halbert's published "if it works every hundred
  years, why is there always a next one?" becomes the question that got him
  pensioned. Nothing is repaired. `frostwick.py`, Pargeter's `prophecy` pages;
  optionally the same clause visible on the Archive copy at Olde Evermore.
* (b) leave it: a comic world where nobody counts. Costs nothing; the audit
  exists because Mike counted.
* (c) repair either clock: dozens of published lines. Not proposed.

**C2 - the Former Premises (F against P).** Hollowell has the venue moved
**four hundred** years ago after **two thousand** years in which "no hero ever
reached it". Published: the Tower is 4,800 years old, and Grimspite has been
reached, renewed and has said "so you have come at last" forty-seven times -
and, in the Premises' own page, he has "never been" to the old place. So the
move must predate him. Proposed, F: the move was **4,800 years ago**, just
before the present incumbent - the first hero ever to arrive was the one who
got the job, which the Tower's "UNDER THE SAME MANAGEMENT" already allows.
`premises.hollowell_pages` ("That was four hundred years ago" -> four thousand
eight hundred; "Four hundred years and nobody in it"), `premises.hall_events`
(the book's "four hundred years"; "sixteen hundred" reports -> nineteen
thousand two hundred), `journey.visitors_book_pages` (two lines), and
`WORLDMAP.md` 7.4 and the module docstring. Hollowell is then nearly five
thousand years old and retained, which the game should not explain - Mirabel
is four thousand and nobody explains her either.

**C3 - the present year (P against P, minor).** ITEM 1's "a hundred and
ninety-eight years" since 1802 makes it 2000; Attempt Eighty-Four's "a hundred
and forty years" since 1886 makes it 2026, in four published lines to ITEM 1's
one. Proposed, Repair of one line in `journey.item_one_scene`: "a hundred and
ninety-eight years" -> "two hundred years and more", which "Two hundred years
I have been at this" already rounds to. Or leave it.

**C4 - four thousand and four thousand eight hundred (P, soft).** Grimspite
says both in one scene. Read as a tired man rounding, it is not a
contradiction. Proposed: leave the game; correct `CLAUDE.md`'s premise ("four
thousand years into") to 4,800, which is a doc.

**C5 - Mirabel at the signing (F, soft).** She is 4,112; the engagement is
4,800 (or 6,800 with the castle). It only contradicts if there was one signing
- and the published Prophecy is "the Forty-Eighth Prophecy of Thistlewick, in
triplicate", so there have been forty-eight, and she signed three times at one
of them. Proposed: leave it. If Mike reads the Prophecy as signed once, raise
her to "five thousand one hundred and twelve" (F, one line and `BIOS.md`).

**C6 - 1802 twice (F against P).** Great Dunnage sealed its Counting House in
the year ITEM 1 went into the Hoyle Works' ledger, a valley apart. Nothing
connects them. Proposed, F: move Dunnage to **1788** - no other date in the
game - in `dunnage.mayor_pages`, `door_pages`, `memorandum_pages` and
`COMPANIONS.md` NIX-2. Or keep it and let NIX-2 make it a connection.

**C7 - Fenmarch's dates (F against F, and against P).** Mr Ottershaw has
composed every animal in seventy years, but three cases are dated 1819, 1838
and 1852 - and the Marsh Bear's "Sir Aldric the Second, 1838" would make the
published Sir Aldric **the Third** the grandson of a man active a century and
a half ago. Proposed, F: take the years off the three cases and keep them on
the two portraits, which are older than Ottershaw's work and can be. The
`fenmarch` case table.

**C8 - Aldric and the Wrong Dragon (F against F).** The young knight "oh,
twelve years ago" is Aldric, who left home nine years ago. Proposed, F: "oh,
eight years ago" - after he left Fenmarch and before Thistlewick -
`nomap._wrong_dragon` and `COMPANIONS.md` ALD-6.

**C9 - Meech's great-great-grandad in 1749 (F, minor).** Four generations in
about 250 years. Proposed: leave it.

**C10 - the Clanging clock (P, minor).** Fast "since eighteen forty-one" and
the town early "for sixty years". Readable as the town having trusted it for
sixty. Proposed: leave it.

**Done, 26 September 2026 - the timeline, and its fixes.** Mike's decisions,
and what was changed for each:

* **C1: the defined term.** Pargeter now reads clause two out after "Somebody's
  worried": *'A hundred years' is a defined term. 'Such period as the Committee
  shall find convenient.'* `frostwick.cold_room_events`, F. Not added to the
  Archive copy.
* **C2: the move was 4,800 years ago.** Hollowell, the visitors' book, the
  quarterly reports (19,200) and Grimspite's visitors'-book pages 3 and 4 say
  four thousand eight hundred years; `WORLDMAP.md` 7.4 and `SITES.md` step 6
  follow. F.
* **C3: repaired - the other way from the one proposed.** Mike asked why
  the present was not a round year, and it should be: the Committee finds
  round years convenient, so Bram sets out in **2000**, which is what ITEM 1's
  published "hundred and ninety-eight years" since 1802 already said. So
  ITEM 1 stands and Attempt Eighty-Four came down in **1860** instead of 1886
  - three published lines, `NORTH.md` 8.1b. (The 224 repair made earlier the
  same session was undone; ITEM 1's lines are byte for byte as published.)
* **Who notices** (Mike's rule, `TIMELINE.md` 1): Thistlewick never notices,
  the further from its committees the more people do, and the elves say it
  outright. Checked: nobody in Maps 1-7 notices. Added, F: **Elder Faelan**
  tells you the Forty-Seventh came off the ledge ten years ago, that the
  Committee counts "the way the Prophecy does. We count the way the sun
  does", and that the Age "began with a great many things. The Prophecy was
  the one with a clerk present." `evermore.py`, event 4, page 0.
* **C4:** `CLAUDE.md`'s premise says 4,800. The game is unchanged.
* **C5, C9, C10:** left.
* **C6:** Great Dunnage sealed its Counting House in **1788**. `dunnage.py`
  x3, `COMPANIONS.md` NIX-2, `SITES.md` step 18. F.
* **C7:** the three dated cases at Fenmarch have no dates; the two portraits
  keep theirs. F.
* **C8:** the Wrong Dragon's knight was "oh, eight years" ago; `COMPANIONS.md`
  ALD-6 and `SITES.md` follow. F.
* **Mike's question - what is the calendar?** - is answered in the new
  **`TIMELINE.md`**, which is now the reference every dated line is checked
  against. The calendar is the elves' **Third Age**, which Thistlewick claims
  began with its Prophecy because it signed it in year 1 on purpose; the
  present is **2000**, and recent Chosen Ones go in round years; the Prophecy's figures are contract years. Mike's idea,
  and nothing in the game says it yet.

Rebuilt and `validate.py` clean. The built text was diffed before and after:
the only lines that moved are the ones above. No scenario asserted any of
them except `finale_ending`'s label.

#### The wider dialogue audit - started 26 September 2026

**The tool is `build/audit_text.py`**: a regex over every line of text in the
built `data/`, each marked P or F against `live-rpg`, with map, event, page
and speaker. `--event 'Map042 ev2 '` prints one event's whole script. It is
how the timeline above was built, and it is much cheaper than reading
modules.

**Checked, and consistent** - do not re-check:

* **Distances.** Little Gore to Fenmarch is four miles in all four places
  (Mrs Vane twice, Tom, the fingerpost). Ashcombe's "eight miles inland" is
  Mr Weir's "by the road". Cotter's eleven miles, the charts' fourteen, the
  west road signpost's 9 and 14, the Coast Road's 4 leagues to Sopping and
  Halbert's forty miles are all measured from different places, and nothing
  says otherwise. Thistlewick's "200 leagues" to the Tower is crossed out
  on the sign itself.
* **Marriages and families.** The Cotterills: Gudgeon's register of ages
  agrees with every child who states one (Rivet 22, Ferrule 16, Spare 9), and
  Bessie's "down the valley at the big foundry until the spring" is the Cotter
  that Great Dunnage has, home on Saturdays. Tom and Mrs Vane, nine years.
  Mrs Emberthwaite a widow in both places. Dorcas and Prudence sisters.
* **Sir Dunstable**: a quarter past four at Hithermost and at Fairholme.
* **Days of the week**: Thursdays are Rosamund's walk, the Order's committee
  and Nabb's post, and none of them collide.

**Found and fixed, Free:**

* **D1 - Restwell charged in gold.** The game's money is crowns (`System.json`
  says `cr`; Prudence says "20 crowns", Splint "two crowns"). Mrs Ashbury said
  "Ten gold" three times; she says "Ten crowns" now. `restwell.py`.
* **D2 - Penultima priced in gold.** The Sword's card said "9,999,999 gold"
  and Dorothy "One gold"; both say crowns now. Dorothy's line was re-broken
  to fit - the same words. `penultima.py`.

* **The dead.** Ambrose Fitch is the only person who is dead and speaks,
  and that is the Barrow's point. The Hoyle attempts agree with the calendar:
  84 in 1886, 199 "eleven years dead" in both the log and on her crag.

**Still to do**, next session: the living - anybody said to be somewhere, or
doing something, by a second speaker who is contradicted by the first;
characters described as something their sprite or face is not (overlaps item
4 - do it with the contact sheet item 4 builds, not separately); and lines
that promise something the game does not have - a place, a shop, a person
somebody says is "up the road".

### 4. Portraits of the wrong gender

Most often children: a character written as a boy with a girl's face, or the
reverse. Not only children.

* Build the list from `story.FACES` and the `Gen_*` settings in
  `build/characters/`: every face, cropped - the `clanging_faces` scenario's
  idiom, or a contact sheet of `img/faces/` cells - beside the name, and
  compared against what the dialogue and `BIOS.md` say the character is.
  Look at the sprite too: the face and the walking sprite should agree.
* `NORTH.md` 4.6 has a worked example: Rivet was moved off `SF_Actor2` 2
  because it "reads as a girl at both sizes". Read that before recasting.
* A stock face that is wrong can be **recast** onto another stock face or a
  generated one; a generated face can be redrawn with `art.py --replace`.
  Recasting a *published* character's face is a Repair.

### 3. Elves without pointed ears

Olde Evermore's elves above all - Elder Faelan (`Actor3` 0), Elder Lirien
(`Nature` 6) and Mirabel (`Gen_People2` 4, drawn) - and anybody else written
as an elf. Check `CHARGEN.md` for how the generator does ears: `ears` is its
own part in the settings, and every settings file here sets `ears: p01`.
Mirabel is a kid-body drawing, so check what ear parts the kid body has.
Stock faces with human ears on elves are recast or redrawn.

### 2. Portraits that look as if they have no nose

Mostly faces with a moustache; others have only a very small nose. Mike
suspects the nose is set and hidden rather than missing. **Measure before
fixing**: render one of them (Gideon Markup, Hubert Weir, Dean Fenwold, Perce
Stagg and Mr Gedge are candidates) with the beard removed and see whether the
nose appears. If it is being drawn under the beard, the stacking order in
`tools/chargen` is the place to look - `CHARGEN.md` has the per-view stacking
and it was calibrated against editor exports, so compare against a reference
export with a moustache before changing it, because the editor itself may do
the same. If the editor does it too, pick a different `nose` or `beard`
pattern per face instead of changing the stacking.

### 1. Speakers with no portrait

**Draw a face for every human or elf who speaks without one**, and give Mike
**a list, with criteria, of those that cannot be drawn** with the Character
Generator because they are not human or elf.

**Thirty-eight names** are spoken through `say()` with no `story.FACES`
entry, found by `say("<literal>")` against `FACES` on 26 September 2026:

    Alfie, Bess, Nell, Mr Gammage, Mrs Pardew, Dame Winifred   hamlets
    Commissioner, Somebody Large                                nomap
    Dr Hapgood, Reader, Undergraduate                           collegium
    Elf                                                         evermore
    Granny Wendle, Ned                                          gladhollow
    Miss Quayle, Mr Ambler, Mr Plummer, Mr Tweddle,
      Mrs Dewhirst, Mrs Poskitt, Town Clerk, Warden Crabbe,
      Watchman                                                  dunnage
    Mr Crouch, Mr Dace, Mr Nuttall, Mr Oakes, Mrs Liddy,
      Sir Hamo, Sister Lamb, Sister Pim                         weeping_bottom
    Mrs Dimmock, Wilf                                           ashcombe
    Mrs Emberthwaite                                            fairholme
    Mrs Garrow                                                  sable_hart
    Mrs Puddifoot, Tom                                          fenmarch
    The Prophecy                                                journey

**The list is not complete**: speakers whose name reaches `say()` through a
variable or a helper (`talker`, `npc`, `recruit`) are not in it. Extend the
search to those before calling it done.

Things to decide per name:

* **A face drawn for a speaker must match their walking sprite**, which is
  usually a stock `People*` sprite. Draw the face to agree with the sprite -
  hair, clothes, age - or change both, in which case the event's image
  changes too.
* **Adding a face costs line width.** A faceless line has 60 characters and a
  faced one 47, so every line those speakers say has to be re-broken: `say()`
  refuses the over-long ones, so the build lists them. Moving a line break is
  not re-voicing; changing the words is.
* **Some were left faceless on purpose, and Mike should see those rather than
  have them drawn unasked.** `The Prophecy` has no face because "it is a
  document, not a person" (`story.FACES`'s comment). `Somebody Large` is
  deliberately unseen. `Elf` is a nameless raker. Put these to him as a list.
* **The non-human ones go to Mike as a list with criteria**, since he supplies
  full-body art: at least Mrs Emberthwaite (a dragon, `$BigMonster2` 0, kindly,
  a widow, plays whist), the Wrong Dragon (elderly, well read, delightful, "a
  dragon in the sense that the map says so", has a blanket over what you think
  are its knees), the Duck (honorary Fellow, four hit points, a medal),
  Duchess the horse (a grey mare in harness, effectively a partner), and
  anything else the search finds. For each: size (144x144 face, matching the
  `Gen_*` sheets), what it must show, and what it must *not* show - e.g. the
  Wrong Dragon's face must not settle what it is.
* New faces continue on **`Gen_People6`**, cells 5-7, then `Gen_People7`.
  Skin swatch 2; `lineup.py` for every one; `art.py` installs.

### 5. The Collegium's roofs, and other visual contradictions

The world-map stamp and the text say **purple spires**; every roof on Map 58
is `ROOF_GREEN`.

* `mapkit`'s nine-slice roofs on the Outside C sheet are only four - green,
  white, gold and brown (`mapkit.py`'s comment above `ROOF_GREEN`). So look
  for purple elsewhere before settling: **Outside_A3's roof autotiles**
  (`Roof A` to `Roof L` by their `.txt` names - `WALL_BLUE_TILE` is `Roof H
  (Dark Blue Tile)`, for instance), the `Outside_C` towers, or **a recoloured
  copy of the green roof** drawn by running the module, the way
  `collegium.draw_art()` and `fenmarch.draw_art()` make what no sheet has.
  Crop candidates with `../tools/mapgen/contact.py`.
* **Then look for others of the same kind**: every place whose text describes
  its look (a colour, a material, a thing on the wall) against a screenshot of
  it and against the world-map stamp it sits behind. `SITES.md`'s steps each
  recorded what their stamp looked like when shot.

---

## 3. Not in this audit

* **The walkable wall ring** on every `K.interior` room (`SITES.md` step 18,
  last bullet). Mike is raising it separately with other build issues.
* **Village 1**, the counter thresholds, the full suite and the push -
  `SITES.md` section 4, which comes after this, with `SITES-NEXT.md` as its
  restart prompt.
* **The companion quests**, which come after that.
