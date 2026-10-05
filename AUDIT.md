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

**The living, and the promises - 26 September 2026.** Done by reading the
whole of the built text end to end (`audit_text.py '.'`, about 85,000 tokens
once the padding is stripped), and by cross-referencing every speaker's name
against every other event that mentions it. Nothing in it is a plain Free
contradiction, so nothing was changed for this half; what it found is below,
for Mike.

**Checked, and consistent** - do not re-check:

* **Where people are said to be.** Ysolde at the table by the bar; Tom in the
  gardens at Fenmarch, home at five; Walt on the bottom stair; Cotter at the
  Iron Company, home Saturdays; Sir Dunstable at a quarter past four, with
  Hithermost's lamp, and his apologies at Fairholme "(in a mountain)"; Mr
  Pilbeam at the council table; Rosamund up the hill on Thursdays, in her card,
  the minutes and Mrs Emberthwaite's tablet; Mr Gedge lifting the Register on
  Mondays; Corvin in the Wyvern, on his mother's dresser and in the Sable
  Hart's apologies; Hob "south twenty year ago" in Bryd's mouth; Nib and
  Tappet's four years; the Sable Hart's rota, table and five for four corners;
  the Vanes' wedding, banns and three births; Frostwick's twelfth, forty
  festivals and forty winters; Fairholme's eleven rescues and the
  two-thousand-and-forty-eighth; the Dean's eleven years and Zephyrine's.
* **Directions and prices.** Mr Gedge's "Hall's on the left, Library's on the
  right" against Map 58; Mrs Barrow "across the way" from the Guild. Every
  price a line quotes against what its event charges or its shop sells: the
  six inns (20, 25, 30, 10, 11, 15), the hat at 30, the bench at 400, the oil
  at 120, the Pit and the fair at 2.
* **Soft, and read the kind way.** Wick went north forty-one years ago and
  Mrs Barrow has been thirty-nine years in the trade: she opened the shop with
  his name on it. Fizz's "forty-seven skipped it" against Old Hollis's
  forty-one years: Fizz counts the way Thistlewick does. Ysolde's duke's son
  "runs a shipping concern" ninety-one years after the last ship passed
  Bother's point: not past that point. Pargeter's "nine years, renewed"
  against forty winters: a nine-year term. Mirabel's ninth of March and
  Penultima's twelfth of November: the game has no one date. Wat Pardle is
  not by the Standing Stones because the plaque says he was asked to stop
  coming.
* **Hooks, not promises.** Lines that invite something the game does not yet
  do are companion-quest set-ups and are meant to be open: the Cinder Fen's
  fire person, Meech's gate, Tobias Frayne's jar, Miss Fettle's card, Bond No.
  1, Form L, the Contest's categories, the Schedule, Duchess, the Wrong
  Dragon's knight. The Ferryman's tide is a published joke that never turns.
* **Sops** is never given a pronoun in anything the player reads - "the
  Potboy" is only the event's name - so the face reads as either and is not an
  item 4 finding. Nor are Clevis and Ferrule (`NORTH.md` 4.6), Tibb, Child,
  Dunnock or Warden Crabbe.

**Found, for Mike** - each needs a decision before anything changes:

* **D3 - the Chandler's never opens (P).** Nether Sopping's shut shop gives its
  hours as "when the light is on at the point. The light has been out since
  spring." The player lights it, and the card still says so, for ever.
  Additive fix, no Repair: a page on `SW_LAMP_LIT` (pattern 2). Either it
  opens - a small chandlery, lamp oil and ship's biscuit and rope - or it stays
  shut under a new card. Which?
* **D4 - Bother's stipend (P against P).** "The Guild stopped my stipend when
  the shipping stopped ... Ninety-one years ago", and the Adventurers' Guild
  (Provisional) was founded forty years ago - the Charter, the Guild Card and
  Pell all say so. Readable as another, older guild. Proposed: leave it. The
  Repair would be one word in Bother's line.
* **D5 - Aldric's father (F against P).** Published: "I wrote to my father. I
  have not sent it." Free: the Fourth, his nephew - "Grandfather came over the
  wall. Until he was eighty." - which is Aldric's father, and reads as either
  retired from the wall or dead. If he is dead, the unsent letter becomes a
  sad beat nobody chose (`NORTH.md` 1.5, test two). Proposed, Free: make him
  plainly alive and still at it ("Grandfather still comes over the wall. He
  is eighty-one ..."), one line in `fenmarch.py`. Or leave it open for ALD-5.
* **D6 - the Door into the Mountain says "Not yet" (F).** "You have no lamp.
  You do not go in. Not yet." There is no lamp to get: Sir Dunstable has it,
  and nothing lets you in. Keep it as a hook (and write it into
  `COMPANIONS.md` or `SITES.md` section 4, so it is owed), or drop "Not yet."
  and let it be a door that says no, which is what `hithermost.py`'s docstring
  calls it.
* **D7 - the same name twice (not contradictions).** Nell is Old Hollis's wife
  (P) and the smallest Vane (F); Kit is a Fairholme hero (F), Kit Blackwood (F)
  and Ysolde's Kit (P); Budge is the Barrow's hound (P) and Mr and Mrs Budge
  (F); Tolly (P) and the Tolleys in the Chapel's Book (F). Vance is Zephyrine
  and Halloran, both published, and may as well be family. Rename the Free
  doubles, or leave them - real villages repeat names.

**Done, 26 September 2026 - the wider dialogue audit.** Every line of built
text has been read: the facts two speakers share (D1, D2, fixed), the dead,
distances, marriages, days, the living, and the promises. Two Free fixes were
made (the currency); five findings (D3-D7) are Mike's to decide and are listed
above, with a proposal each; everything else was consistent, and the lists
above say what, so it is not checked again. Characters described unlike their
face or sprite went to item 4, below.

**Done, 26 September 2026 - Mike's decisions on D3-D7, and what was made:**

* **D3 - the Chandler's opens.** A page appended to Map 13 event 16 on
  `SW_LAMP_LIT` (`NORTH.md` 1.7 pattern 2; page 0 is byte for byte as
  published): the card has been turned round, OPEN, "everything has been
  dusted since spring. Twice." - and a shop of lamp oil, ship's biscuit,
  antidote and smelling salts. No rope: there is no rope item, and the free
  item ids are `SPARE.md`'s. `south.py`, F. The new `audit_fixes` scenario
  walks up to it both ways.
* **D4 - left.** Bother's Guild is another, older guild.
* **D5 - left open for ALD-5.** Whether Aldric's father is alive is ALD-5's
  to settle; nothing changed.
* **D6 - kept as a hook.** "Not yet." stays, and is now owed: `COMPANIONS.md`
  section 8 (new) writes down what the game has already fixed about the way
  in - the lamp, from Sir Dunstable, at a quarter past four - and
  `hithermost.py`'s docstring points there.
* **D7 - left.** Real villages repeat names.

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

#### Started, 26 September 2026

**The tool is `build/facesheet.py OUT_DIR`**: every name in `story.FACES`,
its face cropped beside the walking sprite of the event that speaks with it,
and a he/she count off that event's narration (a hint, not a verdict - a scene
with two people in it counts both), as `sheet-NN.png` montages of 24 and a
`faces.tsv`. 135 faces, six sheets. Items 3 and 2 start from the same sheets.

Two things it established that nobody needs to check again:

* **Face and sprite always agree.** Every speaking event's page graphic is the
  same sheet and index as its speaker's face - stock faces pair with their own
  stock sprites, and `Gen_*` faces with the sprite drawn from the same
  settings. So the only question is face against text.
* **The faceless speakers' sprites were checked too** (they are what item 1
  will draw faces to match): one wrong, below; the rest agree with their text.

**Fixed, Free:**

* **G1 - Restwell's guest** "shoulders his pack" and had the Neighbour's face,
  the girl with the pigtails (`People1` 1). He shares the Merchant's now,
  `People2` 4, face and sprite. `restwell.py`, `story.FACES`.
* **G2 - Little Gore's Nell** - "She is, too" - walked about as the
  spiky-haired boy, `People1` 0. She is the pigtailed girl, `People1` 1.
  `hamlets.py`.

**For Mike:**

* **G3 - Thistlewick's gossip (P, Repair).** Map 1's `Gossip` - "They chose
  you at the meeting ... She lets that sit" - has the `Villager` face and
  sprite, `People1` 0, which is a boy. Published, and a contradiction on its
  face, so a Repair in `NORTH.md` 8.1 is allowed: recast the event onto a
  woman (`People1` 3, the red-haired Councillor, or `People1` 5, Mother, who
  are both in Thistlewick already, or an unused cell). The Hithermost villager
  shares `Villager` and is never given a pronoun, so it can stay.
* **G4 - Wren (P).** Written as a woman; `Actor2` 7, face and battler, can read
  as a young man - a slight ranger with short grey hair. A judgement by eye,
  and a companion's recast touches the face, the sprite, the battler and
  every scene she is in.
* **G5 - Nix (P).** Written as she; `Actor3` 4 is masked and hooded, and the
  brows read male to some eyes. Same judgement.

**Not gender, for items 1 and 2:** Tom (F) walks about as the old man with
the headband, `People4` 4, and is nine years married with three small
children - decide his age before item 1 draws his face. Bess (F), "a small
girl", walks as an adult, `People2` 3 (the white headscarf passes for a
bride's veil). Dree (P), "an elderly gentleman", has a middle-aged face, and
Mrs Harbottle (F, drawn), "formidable", a young one.

**Done, 26 September 2026 - Mike's answers to G3-G5:**

* **G3 - recast, a Repair, `NORTH.md` 8.1c.** Mike's rule: a new stock face
  if one is free, else a generated one. The only unused stock woman in the
  game is `Actor3` 5, a child in a red riding hood, so the gossip is drawn:
  `Gen_People6` 5, a kerchief and a print dress
  (`build/characters/thistlewick-gossip.json`). Her label still reads
  "Villager:", so `story.say` takes `face=` naming another `FACES` key -
  `"Gossip"` - and Hithermost's pronounless villager keeps `People1` 0. Not a
  word changed. `audit_fixes` asserts her sprite and face off the live game.
* **G4 - Wren: left.**
* **G5 - Nix: Mike will supply a female version of the face.** `Actor3` 4
  reads male; the walking sprite and battler stay. It is the first entry in
  **the list of faces Mike supplies**, item 1 below. The game writes her as
  she ("She does not hand it over", "like a woman with somewhere to be");
  `COMPANIONS.md` alone heads her section "Who they are", which is a doc and
  is left for Mike.

Item 4 is finished, bar installing Nix's face when it comes (a Repair of a
published face - write it up in `NORTH.md` 8.1 then).
**Nix's face is installed, 29 September 2026** - Mike's portrait,
`NORTH.md` 8.1e. Item 4 is finished.

### 3. Elves without pointed ears

Olde Evermore's elves above all - Elder Faelan (`Actor3` 0), Elder Lirien
(`Nature` 6) and Mirabel (`Gen_People2` 4, drawn) - and anybody else written
as an elf. Check `CHARGEN.md` for how the generator does ears: `ears` is its
own part in the settings, and every settings file here sets `ears: p01`.
Mirabel is a kid-body drawing, so check what ear parts the kid body has.
Stock faces with human ears on elves are recast or redrawn.

**Done, 26 September 2026.** Who is an elf: `audit_text.py` for
elf/elves/elven/ears finds only Olde Evermore - its sign, the raker, and the
Archive's three - plus Tobias Frayne's book, whose "Two elves. Sang to me."
is a memory, not somebody on a map. Nobody else is written as one. All Free.

* **Elder Faelan** was `Actor3` 0, a round-eared human swordsman; **Elder
  Lirien** `Nature` 6, a young spirit whose hair covers her ears, under "every
  one of them visibly older than she looks". Both are drawn now, on
  `Gen_People6` 6 and 7, old and with `ears: p02` showing: Faelan long and
  silver with a gold bead in a green robe, Lirien lilac with a circlet in a
  cream one, which keeps the note her stock face struck. `story.FACES` and
  both sprites in `evermore.py` read the same entry now, so they cannot
  drift. `Actor3` 0 and `Nature` 6 are free again.
* **Mirabel** always had `ears: p02` - her sprite shows them - but her
  fringe, `fronthair p17`, covered the point in the portrait. `p04` keeps the
  bob and shows the ear; redrawn with `art.py --replace 4`. The lesson is in
  `CHARGEN.md`: setting the part is not the same as seeing it.
* **The raker** (`Elf`, faceless) walks as `People2` 1, whose hair covers the
  ears at 48 pixels, so the sprite contradicts nothing. Whether it gets a face
  is item 1's question, and the raker is on its list of the deliberately
  faceless; if it does, draw it as an elf, face and sprite together.

`evermore` scenario re-run after the recast.

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

**Done, 26 September 2026.** Measured first: the five candidates rendered
with `beard: ""` show **exactly the same nose** as with it - Beard is
stacked over Nose, but no moustache here reaches the tip, so it hides none
of it; the stacking is not at fault
and `chargen.LAYER_ORDER` is untouched. The cause is the part itself:
every one of the 49 settings files but Dorothy's had `nose p01`, and male
`p01` is a single pale highlight on the tip - no line, no shadow. Without
a moustache it reads as the house style of the young stock faces; with a
moustache sitting right under it, the eye takes the moustache for where
the face ends. The stock faces with moustaches - Fisher/Ferryman
(`People1` 4), Dree, the Merchant, Bother, Mr Budge, Dunnock - all have
hand-drawn noses, so **nothing stock is recast**.

* **Eighteen generated faces** with beards or moustaches get a nose that
  shows, picked on each face from a trial of `p03`, `p07`, `p12`, `p19`
  and `p23`, and varied so the cast does not share one: `p12` (a shaded
  tip) for Weir, Gedge, Walt Ashbury, King Aldous, Hollowell, Crake,
  Ottershaw and Tibbs; `p23` (a softer tip) for Gideon, Perce, Quillon,
  Meech, Rook and the Mayor; `p19` (a long bridge) for the three severe old
  men, Dean Fenwold, Sir Dunstable and Mordaunt; `p03` (a line) for Tobias,
  the youngest. Redrawn with `art.py --replace 0 1 2 3 4 5 6 7`; the rest
  came back `unchanged`. Only faces and bust pictures changed - the walking
  sprites and battlers do not draw the nose differently.
* **All Free.** Gideon is `Gen_People1` 4, which is in `live-rpg`'s image,
  but no published map or troop shows cells 4-7 of it or their busts; cells
  0-3 were checked pixel-identical to `live-rpg` after the redraw.
* **Not changed: Norbert Pelling and Old Hollis** (`Gen_People1` 1 and 2),
  both bearded, both on `nose p01`, both shown on published Map 28 (and
  Norbert in `Troops`). A small nose contradicts nothing, so a redraw
  would be "better if", not a Repair - **put to Mike**; if he wants them,
  it is the same one-line change and a `NORTH.md` 8.1 entry.
* Beardless generated faces keep `p01`; they read like the stock faces
  beside them. No scenario asserts a redrawn face (only the gossip's, in
  `audit_fixes`), and the build changed nothing in `data/`.

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

**The search, extended - 28 September 2026, and now complete.** Rather
than chase every helper through the source, it was re-run off the **built
`data/`**: every Show Text whose `faceName` is empty and whose first line
opens with the `\C[6]Name:\C[0]` label `say()` writes, however the name got
there - `say`, `npc`, `talker`, `recruit`, a site's own helper or a loop over
a table. It checked the other ways a name could reach the screen as well: no
Show Text anywhere uses the engine's `speakerName`, and every other first line
with a colon in it is a notice, a sign or narration ("CAUSE: UNDER REVIEW.",
"STATION ONE: ITEMS"). It found the thirty-eight above and **one more**:

    Dog                                                         village (P)

and two signposts that print a direction as a label (`NORTH`, `EAST`), which
are not speakers. **The Duck and Duchess never speak** - both are narrated
("The duck inclines its head"; "She is considering the Tuesdays") - so
neither needs a face unless a quest gives them lines. **`Somebody Large` is
the Wrong Dragon**: the label under which it speaks, in its cave on Map 8.

Every one of the thirty-eight is **Free**; Dog and The Prophecy are
**Published**. Where each speaker walks, which is what a face has to agree
with (`People*` are stock; the Commissioner, Somebody Large and The Prophecy
have no sprite):

| who | P/F | map, event | sprite | | who | P/F | map, event | sprite |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Dog | P | 1, ev14 | `Nature` 0 | | Sister Pim | F | 54, ev8 | `People4` 1 |
| Commissioner | F | 8, ev52 Cinder Fen | none | | Mr Crouch | F | 54, ev9 | `People3` 4 |
| Somebody Large | F | 8, ev53 Wrong Dragon | none | | Mrs Liddy | F | 54, ev10 | `People1` 7 |
| The Prophecy | P | 12, ev2 Grimspite | none | | Mr Oakes | F | 54, ev11 | `People1` 6 |
| Mrs Emberthwaite | F | 37, ev5 and ev6 | `$BigMonster2` 0 | | Sir Hamo | F | 55, ev4 | `People2` 0 |
| Elf | F | 38, ev7 the Raker | `People2` 1 | | Sister Lamb | F | 55, ev5 | `People4` 1 |
| Ned | F | 40, ev9 | `People1` 0 | | Mr Nuttall | F | 55, ev6 | `People1` 4 |
| Granny Wendle | F | 40, ev10 | `People1` 7 | | Mr Dace | F | 55, ev7 | `People4` 4 |
| Mrs Garrow | F | 49, ev7 | `People4` 5 | | Tom | F | 56, ev7 | `People4` 4 |
| Dame Winifred | F | 50, ev4 | `Actor2` 1 | | Mrs Puddifoot | F | 57, ev3 | `People4` 1 |
| Bess | F | 50, ev5 | `People2` 3 | | Dr Hapgood | F | 58, ev11 | `People3` 4 |
| Alfie | F | 50, ev6 | `People1` 2 | | Reader | F | 59, ev6 | `People1` 2 |
| Nell | F | 50, ev7 | `People1` 1 | | Undergraduate | F | 60, ev7 | `People2` 2 |
| Mr Gammage | F | 51, ev4 | `People4` 4 | | Watchman | F | 61, ev8 | `People4` 2 |
| Mrs Pardew | F | 51, ev5 | `People4` 5 | | Mrs Poskitt | F | 61, ev13 | `People1` 5 |
| Wilf | F | 52, ev10 | `People1` 2 | | Mr Plummer | F | 61, ev14 | `People1` 4 |
| Mrs Dimmock | F | 52, ev11 | `People1` 5 | | Warden Crabbe | F | 62, ev3 | `Actor3` 2 |
| | | | | | Town Clerk | F | 63, ev5 | `People4` 6 |
| | | | | | Mrs Dewhirst | F | 65, ev2 | `People2` 3 |
| | | | | | Mr Ambler | F | 65, ev4 | `People2` 0 |
| | | | | | Miss Quayle | F | 65, ev5 | `People1` 1 |
| | | | | | Mr Tweddle | F | 65, ev6 | `People4` 0 |

So **thirty-five are to be drawn** - every speaker above except the four
non-human ones (Dog, Somebody Large, Mrs Emberthwaite, The Prophecy). The
raker `Elf` was put to Mike as deliberately faceless and he said draw it.
Five sheets: `Gen_People7` to `Gen_People11`, eight, eight, eight, eight and
three.

**How they are drawn.** Many of the stock sprites are shared (Sister Pim,
Sister Lamb and Mrs Puddifoot are all `People4` 1; Tom and two others are
`People4` 4, the old man in the headband) and several contradict the text
(Tom, nine years married with small children; Bess, "a small girl", an
adult). So each speaker is drawn whole - **face and walking sprite from one
settings file** - and the event reads its sprite from the same `story.FACES`
entry as its face, the way `evermore.py` does for the Elders. A face and a
sprite that come from one entry cannot drift apart.

**The batches**, one sheet each, grouped by site so each batch re-runs as
few scenarios as possible:

| sheet | who | scenarios |
| --- | --- | --- |
| `Gen_People7` | **done**: Weeping Bottom's eight | `weeping_bottom` |
| `Gen_People8` | **done**: Great Dunnage: Watchman, Mrs Poskitt, Mr Plummer, Warden Crabbe, Town Clerk, Mrs Dewhirst, Mr Ambler, Miss Quayle | `dunnage`, `dunnage_company` |
| `Gen_People9` | **done**: Mr Tweddle (Dunnage's ninth, the Bell); Little Gore's Dame Winifred, Bess, Alfie, Nell; Sump's Mr Gammage, Mrs Pardew; the Sable Hart's Mrs Garrow | `dunnage`, `hamlets`, `sable_hart` |
| `Gen_People10` | **done**: the Collegium's Dr Hapgood, Reader, Undergraduate; Gladhollow's Granny Wendle, Ned; Ashcombe's Mrs Dimmock, Wilf; the Commissioner (face only, no sprite) | `collegium`, `ashcombe`; Gladhollow has none, the Cinder Fen none |
| `Gen_People11` | **done**: Fenmarch's Mrs Puddifoot and Tom, and Olde Evermore's raker `Elf` - drawn as an elf, `ears: p02` showing, face and sprite (Mike, 28 September) | `fenmarch`, `evermore` |

Things to decide on the way, already found: **Tom** is nine years married
with three small children and walks as an old man - draw him about thirty.
**Bess** is "a small girl" and walks as an adult - the kid body. Read each
speaker's lines with `audit_text.py --event` for everything else they are
said to be, before picking parts.

**Done, 28 September 2026 - batch 1, `Gen_People7`: Weeping Bottom.** Sister
Pim, Sister Lamb, Mrs Liddy, Mr Crouch, Mr Oakes, Sir Hamo, Mr Nuttall and
Mr Dace, all Free. The two Sisters of Whatever Works share a uniform - the
white kerchief cap (`accb p07`) and dress `p13` in blue with its white
collar, which reads as a nursing order where the drawn `p09` read as a party
frock - and are a young woman and a grey one in it. Sir Hamo is the oldest
male face with a long white beard, in `p05`'s white surcoat. Mr Dace was
first drawn in a blue suit and grey hair and came out Mr Thurle's twin
(`Gen_People4` 6), which only the facesheet showed; he is fair and
spectacled in a ward shirt now. Adult men got noses from item 2's list
(`p23`, `p03`, `p19`, `p12`) and a rear hair - **a male settings file with
no `rearhair` is bald from behind**, in every view but the portrait.
`weeping_bottom.py` had passed `face=False` to all twenty of their `say()`
calls, and the lines were already broken to 47, so nothing had to be
re-broken; the events read their sprites from `story.FACES`. Built,
`validate.py` clean, the data diff is those eight events' faces and
sprites and nothing else, and `weeping_bottom` passes.

**Done, 28 September 2026 - batch 2, `Gen_People8`: Great Dunnage.** The
Watchman, Mrs Poskitt, Mr Plummer, Warden Crabbe, the Town Clerk, Mrs
Dewhirst, Mr Ambler and Miss Quayle, all Free. Mr Plummer is "a broad man in
a brown coat, with a moustache": the brown coat is `p26`'s fur-collared one
in swatch 7, since `p12` will not go brown in any swatch. Mr Ambler was drawn
twice more after his first draft came out Dean Fenwold's twin (white hair
swept back, white moustache) and his second the Mayor's (red coat, brown
beard); he is grey-bearded in a mustard scarf now. **Look for twins against
the whole cast, not only the batch** - `facesheet.py` puts the new faces
beside everybody drawn before them, and that is the only place it shows.
`dunnage.py` had 33 `face=False` calls for these eight (and a 34th through
a variable, `S.say("Mrs Dewhirst", lines, face=False)`); Mr Tweddle's two
stay until his batch. Nothing needed re-breaking. Built, `validate.py` clean,
the data diff is those eight events, and `dunnage` and `dunnage_company`
pass.

**Done, 28 September 2026 - batch 3, `Gen_People9`.** Mr Tweddle (Dunnage's
ninth), Dame Winifred, Bess, Alfie and Nell at Little Gore, Mr Gammage and
Mrs Pardew at Sump, and Mrs Garrow at the Sable Hart, all Free. **The three
Vanes are children now**, on the kid body with their mother Hester's brown
hair and blue eyes - Bess, "a small girl", had walked as an adult in a white
headscarf, and Alfie and Nell as stock children shared with half the game;
the kid body has no daisy chain, so Bess's is left to the narration. Dame
Winifred wears the female `accb p05` helmet over `p05` armour. Mrs Garrow
first came out Mrs Dewhirst's twin - two landladies who say "love", in the
same bun - and is black ringlets now.

**The first re-breaking.** These lines had been written for 60 characters,
and eleven first lines were too wide with a face: Dame Winifred's five (her
label leaves her 32), Mrs Pardew's three, Mrs Garrow's two, Mr Gammage's
one. `build_game.py` stops at the first, so the whole list came from one
build with `story._check_width` patched to report rather than raise (then
`git checkout data/`). Each was re-broken by hand, at a sentence end where
there was one ("It doesn't say. / That's the worst of it."), every window
still four lines or fewer; the edit script asserted the text identical but
for where the lines end, and the built text of every changed event, joined
up, is identical to `HEAD`'s. **One scenario did assert a re-broken
line**, and a grep for double-quoted strings missed it: `hamlets` checks
`includes('pin in me at')`, single-quoted, and "pin" now ends a line. It
checks `'in me at Coldbarrow'` now. **After re-breaking, grep the scenarios
for `includes(` in both quote styles** and check every phrase against the
new lines. Built, `validate.py` clean; `hamlets`, `sable_hart` and `dunnage`
pass.

**Done, 28 September 2026 - batches 4 and 5, `Gen_People10` and
`Gen_People11`, and item 1 is finished bar the faces Mike supplies.** Dr
Hapgood, the Reader and the Undergraduate at the Collegium; Ned and Granny
Wendle at Gladhollow; Wilf and Mrs Dimmock at Ashcombe; the Drainage
Commissioner on the Cinder Fen; Mrs Puddifoot and Tom at Fenmarch; and the
raker `Elf` at Olde Evermore. All Free.

* **Two speakers the text never gives a pronoun** - the Undergraduate and the
  Commissioner ("a person with a clipboard") - are drawn as women, which
  says nothing the text contradicts and evens a cast that was running to
  men. The Undergraduate was a stock sprite that could be either.
* **Gladhollow and the Cinder Fen had never passed `face=False`**: Ned,
  Granny Wendle and the Commissioner were faceless only because `FACES` had
  no entry, on a "one short scene" and a "the raker's precedent" in its
  comments - both comments are corrected. The Commissioner is a face only;
  the Fen's event has no sprite, so the sprite drawn for her is unused.
* **Tom is about thirty**, keeping his sprite's headband as a green bandana;
  **the raker is an elf**, with `ears: p02` showing in the portrait and the
  sprite, as Mike asked. Ned has his brother Toby's hair and eyes.
* Twins caught on the facesheet: Hapgood as Mr Dace (fair, spectacled -
  he is dark auburn now), and Mrs Puddifoot as Sister Lamb (grey, the same
  white cap - she is chestnut under it). Tom's first waistcoat and the
  raker's first coat were armour or Mr Dace's in the sprite.
* **Re-breaking.** Ten first lines were too wide: the Commissioner's eight
  and Granny Wendle's two. Nine were re-broken inside their windows. The
  Commissioner's "Ah. It wants burning" speech could not be: at about 176
  characters it is more than four faced lines hold, so it is now **two
  windows of the same words**, split after "Everybody agrees." - which
  `say()` does to any speech over four lines anyway, name and all. It is the
  one window count item 1 changed. The joined built text of every changed
  event is identical to `HEAD`'s, and no scenario asserts a re-broken line.
* Built, `validate.py` clean; `collegium`, `ashcombe`, `fenmarch` and
  `evermore` pass.

**Item 1 is done**, except the faces Mike supplies at the end of the audit
(the running list below): thirty-five speakers drawn on five sheets, the
Dog and The Prophecy left faceless, and Somebody Large waiting on his
silhouette.

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
* New faces continue on **`Gen_People7`** - `Gen_People6` is full (the
  gossip, and the two Elders, took 5-7). Skin swatch 2; `lineup.py` for
  every one; `art.py` installs.

#### The faces Mike supplies - the list, started 26 September 2026

Mike's instruction (with G5): keep a list of every face that cannot be made
with the Character Generator, and **tell him when it is complete**; he will
supply them. Each entry: where it goes, the size, what it must show and what
it must not.

**Mike's answer, 28 September 2026: he supplies every image on this list
at the end of the portrait audit, not piecemeal - so this is a running list,
kept current by every session, of everything he will be asked for.** Add to
it whenever something is found that the Character Generator cannot make, and
leave its rows alone otherwise.

**Complete, 28 September 2026**, now that the search has been run off the
built data (above), and Mike was told. The search added no non-human
speaker to be drawn: its one new name is Thistlewick's Dog, which is
published and goes on the faceless list below. The Duck and Duchess never
speak, so their rows are there only in case a quest ever gives them lines.
The Wrong Dragon is on both lists, because it speaks as `Somebody Large`, the
label item 1 calls "deliberately unseen" - which of the two is Mike's call.

| who | P/F | goes | must show | must not |
| --- | --- | --- | --- | --- |
| **Nix** (G5) | P | replaces the face of `Actor3` 4 only - the walking sprite and the `Actor3_5` battler stay, so match them: masked, hooded, the same colours | a woman; the mask and hood | anything the sprite does not have |
| **Mrs Emberthwaite** | F | a new face, 144x144, `FACES["Mrs Emberthwaite"]`; ten windows, Map 37 ev5 and ev6 (she speaks from Mr Emberthwaite's chair too). Her sprite is `$BigMonster2` 0 and stays | a dragon, kindly, seventy, a widow who plays whist | menace |
| **The Wrong Dragon** | F | a new face, 144x144, `FACES["Somebody Large"]`; seven windows, Map 8 ev53, its cave by the water - no map of its own yet (ALD-6), no sprite. **Mike will supply a silhouette of a dragon**, which is right: every line it has is spoken in the dark of the cave | a dragon-shaped silhouette - enormous, in an armchair among books, a blanket over what you think are its knees | detail - "a dragon in the sense that the map says so". **If ALD-6 or any later scene shows it in the light, a clearer image goes on this list then** |
| **The Duck** | F | not needed now: it never speaks. A face only if a quest gives it lines | an honorary Fellow of the Collegium: four hit points, a medal on a ribbon | |
| **Duchess** | F | not needed now: she never speaks - ALD-4 (`QUESTS.md` B2) made the reunion wordless. A face only if a quest gives her lines; her sprite is `Vehicle` 4 | a grey mare in harness, effectively a partner | |
| **Mr Dray** (B3) | F | real enemy art for `img/sv_enemies/Septimus_Dray.png`, one still image facing right, replacing `art.py`'s stand-in (it is never overwritten once real art is there). Enemy 41, troop 41, Map 65 | his generated face and sprite, `Gen_People12` 7: grey hair and beard, brown coat - and a serpent, the S-shaped bass horn | a modern instrument |
| **Miss Moon** (B3) | F | real enemy art for `img/sv_enemies/Lettice_Moon.png`, the same way. Enemy 42 | `Gen_People13` 0: long black hair, black dress, a sheaf of verses, a handkerchief | cheerfulness |

Installing a supplied face: a sheet of its own in `img/faces/` (8 cells of
144x144, or one), `story.FACES` pointed at it, and - for a speaker with a
sprite - the sprite left alone. Nix's is a Repair of a published face and
gets a `NORTH.md` 8.1 entry; the rest are Free.

**Delivered and installed, 29 September 2026.** Mike sent three 144x144
portraits: Nix, Mrs Emberthwaite and the Wrong Dragon's silhouette. They are
kept as given in `build/supplied/`, and `build/supplied.py` composes them into
one face sheet, `img/faces/Supplied.png`, cells 0-2, in that order. Append to
its list and never move anybody. `story.FACES` points `Nix`, `Mrs
Emberthwaite` and `Somebody Large` at it, and Nix's actor record takes it via
a new `face=` on `db.actor()` - her sprite and battler are still `Actor3` 4.
Nix is a Repair, `NORTH.md` 8.1e; the two dragons are Free. A face costs a
line 13 characters, so both dragons' speeches were re-broken for 47 - no
word changed - and the Wrong Dragon's knight is now two windows instead of
one. `supplied_faces`, a new scenario, reads all three off the live message
window and checks Nix's actor. `fairholme` and `nomap` walk the two dragons
and were run for the line breaks. **The list is done.** The Duck and
Duchess stay unasked unless a quest gives them lines.

**Put to Mike separately, not on this list** - deliberately faceless, and
left faceless unless he says otherwise:

| who | P/F | why faceless | if Mike wants one |
| --- | --- | --- | --- |
| `The Prophecy` | P | "a document, not a person" (`story.FACES`'s comment) - eight windows in the finale | his to supply; published, so a Repair it is not: it would be "better if" |
| `Somebody Large` | F | unseen in the dark of the cave, which the narration is careful about | **answered**: a silhouette, supplied by Mike - the Wrong Dragon row above |
| `Elf`, the raker at Olde Evermore | F | a nameless extra with three windows; its sprite `People2` 1 hides the ears (item 3) | **answered: draw it** - `Gen_People11`, as an elf, face and sprite together |
| `Dog`, Thistlewick | P | says "Woof."; `Nature` 0 | his to supply, and a published face, so it needs a `NORTH.md` 8.1 argument this would not win: a faceless dog contradicts nothing |

#### Provisional, for the companion quests - added 30 September 2026

`QUESTS.md` section 1 audited the faces the companion quests need before any
were built. Every human is the generator's; what is not is below. **Rows
become real only when a step gives the subject lines or a fight**, and that
step moves the row into the table above. Spare's two are not provisional.

| who | P/F | goes | must show | must not |
| --- | --- | --- | --- | --- |
| **Spare** (F1) | F | a side-view battler, `img/sv_actors/`, 576x384, 9x6 cells of 64x64 - `SPARE.md` 6. **Blocks F1**: `validate.py` fails a side-view actor without one | the lad on `SF_People1` 0: blue-black hair, brown eyes, blue jacket over a pale blue shirt | an adult |
| **Mrs Cotterill** (F1) | F | an enemy image, `img/sv_enemies/` and `img/enemies/`, facing right, like the stock enemies (the party is on the right) - `SPARE.md` 6 | `SF_People1` 5: long dark green-black side braid, mustard cardigan, expecting in the spring, unmovable | anger |
| **The Duck** (C3, C4) | F | the row above, if it speaks as a reviewer or a Fellow | | |
| **The Wrong Dragon, lit** (E8) | F | **answered, 2 Oct 2026: no new image.** ALD-6 lights the lamp and the narration shows the books, a blanket with ducks on it and a pair of spectacles the size of cartwheels, and declines the rest; its face stays the silhouette (`Supplied` 2), so what it is stays closed | | |
| **Enemy art** (C4, E7, E18) | F | eleven type specimens, the vigil, Roland's thing - stock monster art first; a generated person gets `art.py`'s stand-in and a row in the table above, as B3's two rival acts have (its hecklers are the stock `Sailor`) | | |

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

#### Done, 29 September 2026

**The Collegium (Free).** No roof on any Outside sheet is purple
(`TILES-AND-ASSETS.md` has the survey), so it is drawn: `collegium.draw_art()`
now also writes `img/tilesets/Outside_C_Collegium.png`, `Outside_C` with the
green roof, its hip and valley pieces, its roof detail and the green `Castle's
Spire` turned the lavender of the world-map stamp, and tileset 7 (`mapkit.
TS_COLLEGIUM`, "Outside (Collegium)") is tileset 2 with that one sheet
swapped. Map 58 is drawn on it with `ROOF_PURPLE`. The door said two other
things the court did not show, and both are fixed with it: the walls were
white ashlar and are now `WALL_SANDBRICK`, "cream-coloured stone"; and the
three towers were flat-topped, and are now the sheet's spire on the tower's
lower three rows - "all towers and purple spires". The recolour is
`mapkit.recolour_sheet`, which the Collegium and Fenmarch both call; it
reproduced the first sheet byte for byte.

**Then everything else whose text describes its look**, found with
`audit_text.py` over colour and material words: twenty-six people's clothes
against their sprites in one labelled montage, eleven world-map stamps, and
thirteen described things by the tiles under their events.

| where | the text | what was there | P/F | fix |
| --- | --- | --- | --- | --- |
| Fenmarch Hall's stamp, Map 8 (86,113) | "its roofs gone green" - and Map 56's are | `Large Mansion`, blue roofs; the only country house on either World sheet | F | `World_B_Fenmarch`, the stamp's four cells gone verdigris (`fenmarch.draw_stamp()`), and **Map 8 on tileset 8**, `TS_OVERWORLD`, tileset 1 with that sheet swapped. Map 8's diff is its `tilesetId`; `worldmap.json` stays on tileset 1, and `coords.py`, `decor.py` and `validate.py` all pass |
| Fenmarch's gate, Map 56 | "Two stone gateposts, green with damp" | the stone fence simply stops either side of the gap | F | `Stone Pillar B (Moss)` over the last fencepost each side |
| **The Gilded Turnip, Map 4 ev6** | "A single turnip on a plinth, painted gold" | an empty `Stool (Ruins)`: the event never had a graphic | **P** | **Repair, `NORTH.md` 8.1d**: the Turnip item's icon cut out and gilded, `!Gilded_Turnip`, stood on the stool. No word changed |
| King Aldous, Map 35 | "a small man in a brown coat" | `art.py` drew him, on purpose, in the red robe, cape and gold circlet | F | the line: "a small man in a red robe / and a crown waves, weakly" |
| The Founder's Stone, Map 54 | "green to the waist with moss" | `Monument A`, clean; no sheet has a mossy standing stone | F | the line: "beaded all over with the damp" |
| Penultima's sign, Map 29 | "in gold on green" | `Sign A`, a bare brown board; no green board exists | F | "in gold" - the `\C[14]` lettering is |

**Checked and fine**, so nobody repeats them: Prophecy Hall is `ROOF_GOLD`,
"the gold one"; the Sable Hart's stamp is a lone green-roofed house on the
waste; Coldbarrow's a white temple in the snow; the Sky Anvil's a stone shrine
with a round stone on top; Frostwick's roofs are snow; Sump has its palm and
its blue pool, on the stamp and on Map 51; Weeping Bottom's `Temple B` and its
Sisterhouse are white and grey (step 15 measured the stamp the same way);
Ashcombe's church is pale stone with a green roof and stained glass, and its
roofs are new; Great Dunnage is walled; Fenmarch's house on Map 56 is grey
moss-stone with a green roof and a moat; the cap is blue with white piping
(`Hat A (Stand)`); the ribbon's case is gilt (`Case A`); the Smiths' banners
are red and gold; the arms over Dunnage's gate are small and gold. Every
described person matched their sprite - Wren's green cloak, Mrs Emberthwaite
very red, Perce's red coat, Pargeter's pale blue and spectacles, Mordaunt,
Blackwood's hood, Weir's frogging, Pim's and Puddifoot's white caps, the three
Sisters' whites, the Fourth's blue and silver, Ottershaw and Tweddle in green,
Fenwold's white and purple, the watchman's blue coat, Cotter's white jacket,
Plummer, Duchess, the Prime Warden, the Mayor's scarlet and hat, Mrs
Harbottle's gold - with one published exception that is not a contradiction:
**Corvin** is "hood up" in the Slain Wyvern and `Actor1` 4 has no hood. A man
can put his hood down, the face is stock art, and it is published - left.

**Nothing item 5 found needs art from Mike**; the one thing no sheet had, the
turnip, was drawn from the game's own icon. The faces list above is unchanged.

Scenarios run for it: `collegium`, `fenmarch` and `airship_lands` (Map 8's
tileset changed under its landing checks). The three re-worded lines keep their
line counts and no scenario asserts them, and no scenario visits Map 4's turnip.

---

## 3. Not in this audit

* **The walkable wall ring** on every `K.interior` room (`SITES.md` step 18,
  last bullet). Mike is raising it separately with other build issues.
* **Village 1**, the counter thresholds, the full suite and the push -
  `SITES.md` section 4, which comes after this, with `SITES-NEXT.md` as its
  restart prompt.
* **The companion quests**, which come after that.
