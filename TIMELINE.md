# The timeline

The reference every dated or aged line in this game is checked against.
Decided with Mike on 26 September 2026, out of `AUDIT.md` item 6, which has the
contradictions it settled and the fixes that followed.

**The rule:** a new line that names a year, an age or a span of years is
checked against this page before it is written, and a new date goes into this
page in the same commit as the line. Where a line and this page disagree, the
line is wrong - or, if it is on `live-rpg`, the page has a problem to take to
Mike (`AUDIT.md` section 0).

---

## 1. Two reckonings

**The calendar** is the elves' **Third Age**. Olde Evermore counts in Ages - the
village is "since the First Age", Mirabel has been doing the biscuit prophecy
"since the Second Age" - and every year this game prints (1702, 1802, 1886) is a
year of the Third Age. **Whatever actually began the Third Age, it was not
Thistlewick.** Thistlewick signed the Prophecy in its first year, on purpose, so
that it could say the Age began with the Prophecy, and it has said so ever
since. The elves know better and have never been asked. **Nothing in the game
says any of this yet**; it is the canon a line would have to agree with.

**The contract** counts in its own years. Clause two defines "a hundred years"
as *such period as the Committee shall find convenient* - Pargeter reads it out
in Frostwick's cold room (`frostwick.cold_room_events`), and that is the only
place it is said. Every figure that comes from the Prophecy's side of things is
in contract years:

* Wispel's "every hundred years" and the Cache's "RESTOCKED EVERY CENTURY";
* Grimspite's **4,800 years**, the Tower's "Est. approx. 4,800 years ago", and
  the rounded "four thousand years" the Tower and Grimspite also use;
* the Obelisk's forty-seven dated RENEWED entries, and the wayshrine's visitors'
  book, whose last entry is "dated a hundred years ago" because it is dated the
  Prophecy's way;
* Hollowell's everything - "two thousand years of Dark Lords", "four thousand
  eight hundred years" since the move, 19,200 quarterly reports - because he is
  the contract's own staff.

**Everybody else uses the calendar and means it**: the south's forty years and
sixty years, the Hoyle Works' two hundred, every site's founding date, every
age. So the Tower is **2,000 calendar years old and 4,800 contract years old**,
and both are true. That is the whole answer to "how can #45 be alive and the
cycle be a hundred years": the Committee has lately found ten convenient.

### Who notices - a gradient, and it has to stay consistent

Mike, 26 September 2026: **the nearer Thistlewick's committees, the less
anybody sees the discrepancy; the further away, the more people take notice;
and the elves will simply tell you, correctly.**

* **Thistlewick itself holds both at once and never notices.** Forty-seven went
  "a hundred years" apart, and the Old Man's boy was the Forty-Seventh, and the
  regular's cousin was the Thirty-Ninth, and nobody in the village is over a
  hundred - and nobody in the village remarks on any of it. That cognitive
  dissonance is the joke and it must be left strong: **no one in Maps 1-7, the
  wayshrine or anything else in Thistlewick's orbit may notice, count, or
  explain.** The wayshrine book is dated the Committee's way ("a hundred years
  ago") for the same reason.
* **Nether Sopping, forty miles off, has the people who noticed** - and were
  pensioned for it. Halbert Quy asked "if it works every hundred years, why is
  there always a next one?" at a meeting, and the cottage was ready by the
  Friday. Everybody there speaks in plain years (sixty, forty, thirty) without
  making a point of it.
* **Upper Clanging believes the text** - it read "every hundred years" two
  hundred years ago and made an engineering programme of it - and does not
  count. That is allowed: noticing grows with distance, it is not guaranteed by
  it, and engineers who take a document literally are their own joke.
* **Frostwick, far north, has the one person who reads the contract**:
  Pargeter finds clause two. She reads it; she does not do the arithmetic for
  you.
* **The elves say it outright.** Elder Faelan (`evermore`, event 4): the
  Forty-Seventh "came off the ledge ten years ago"; the Committee "counts the
  way the Prophecy does. We count the way the sun does"; and the Age "began
  with a great many things. The Prophecy was the one with a clerk present."
* **The Prophecy's own side** - Grimspite, the Tower, Hollowell - speaks in
  contract years and does not notice either, because to them there is nothing
  to notice.

A new line that touches the clock is placed on this gradient first: somebody
in Thistlewick who notices, or an elf who is coy about it, is a
contradiction.

## 2. The present

**Third Age 2000**, Bram's year. Mike's decision: **the Committee finds round
years convenient**, so every Chosen One of living memory set out in a year
ending in nought, and the forty-eighth in the two-thousandth year of the Age
Thistlewick claims. The published text agrees:

* ITEM 1 was written into the stores book in **1802** and has waited "a
  hundred and ninety-eight years" (`journey.item_one_scene`, the tally).
* Attempt Eighty-Four came down in **1860** and her bay has been empty "a
  hundred and forty years" (`field.eighty_four`, `db.build_enemies`, the
  tally). The year was 1886 until `NORTH.md` 8.1b repaired it.
* The south's spans are round too: sixty years, forty, thirty.

"N years ago" in any line means 2000 minus N.

## 3. The Prophecy and the Chosen Ones

| year | what | where |
| --- | --- | --- |
| before year 1 | the Former Premises: the engagement's venue is the castle on the cloud, "two thousand years of Dark Lords" (the old engagement's years) and **no hero ever reaches it** | `premises.hollowell_pages`, `WORLDMAP.md` 7.4 |
| **1** | **the Prophecy of Thistlewick is signed**, three times by everybody, with a horse in the margin beside clause twelve (Mirabel, aged about 2,113, was bored). The engagement moves to the Obligatory Tower - "Ground floor. Door at the bottom" - and the first hero ever to arrive is the one who gets the job: **Grimspite**. Hollowell is retained. 4,800 contract years ago | `evermore.mirabel_pages`, `journey.finale_event` ("That's how I got the job"), `journey.tower_events` (plaque), `premises` |
| 100-900 | #1-#9, a real century apart, in the hundreds - the Committee found a hundred years convenient at first | |
| ~900 | about #9: Thistlewick finds a returning hero awkward and writes clause nineteen, the Resettlement Clause | `EXPANSION.md` 1 |
| 900-1930s | #10-#40, closer and closer together, always in a round year | |
| ~1930 | #39, the cousin of a regular in the Gilded Turnip | `village` |
| 1940 | **#41 Halloran Vance**; the goose has been a wyvern in the Slain Wyvern "for sixty years" - and the second plaque (WRE-2) says 1940, "in two days, with wire" | `south.the_wyvern`, `q_wren.PLATE` |
| 1940s-50s | #42 and #43; the Forty-Second and his wife still drink in the Wyvern | `south` (Sops) |
| 1959 | Wick goes north "forty-one years ago this spring" - a year ahead of the Chosen One; everybody goes north, and not all of them together | `south.outfit_events` |
| 1960 | **#44 Ambrose Fitch**, home and "ignored for forty years"; Ysolde's forty years of field medicine; Beatrice Grumnir makes the sword that becomes Fairweather's Own, at the Thistlewick forge, and sells it to a man going south ("forty years back, near enough", `q_roland`, ROL-4); Perce Stagg, walking north with everybody else, breaks Frostwick's winter "forty years ago this spring"; the Guild founded, provisionally | `wilds.forty_fourth`, `south.ysolde_event`, `frostwick.frostwick_events`, `south` (the Charter) |
| 1970 | **#45 Halbert Quy** declines Grimspite's tea, "thirty years" ago; he is in his seventies now | `south.quy_event`, `journey.finale_event` |
| 1980 | **#46** stops in the Gloamwood and says the woods are enough; his party write monthly. He is the one who did not go "up that road" - Ott counts forty-six | `journey.gloamwood_events`, `south`, `north` |
| 1990 | **#47**, the Old Man's boy; the last name in the wayshrine book | `village.village_events`, `journey.world_events` |
| ~1999 | Ambrose Fitch dies; the masons come within a fortnight | `wilds.forty_fourth` |
| **2000** | **#48 Bram Thistle** | |

Only #41, #44, #45, #46 and #47 are pinned by a line, and only by a span back
from 2000. The rest are "about", and a new line may pin one - add it here
when it does, in a round year.

## 4. Everything else, in calendar years

| year | what | where | P/F |
| --- | --- | --- | --- |
| Second Age, ~2,113 before year 1 | Mirabel born; 4,112 now | `evermore.mirabel_pages` | F |
| 1400 | the Collegium Arcanum founded, by the Founder, in one afternoon ("six hundred years") | `collegium.arms_pages` | F |
| 1500 | the First Dean's portrait hung, pending the Hanging Committee ("five hundred years") | `collegium.portrait_pages` | F |
| 1702 | Weeping Bottom founded by Mother Ursula Pym, for the sea air | `weeping_bottom.stone_pages` | F |
| 1749 | the Sky Anvil falls into Meech's top field; his great-great-grandad makes it a gatepost | `nomap._sky_anvil` | F |
| 1750 | the pilgrims build the shrine round it | `nomap._sky_anvil` | F |
| 1788 | Great Dunnage seals its Counting House, "when the key was lost" | `dunnage` (Mayor, Door, Memorandum) | F |
| 1794 | Sump: wasps in the well; the Water Committee wound up. "Cursed 1794" | `hamlets` | F |
| 1795 | Sump: "a general sense that things used to be better" | `hamlets` | F |
| 1802 | the Hoyle Works' stores book begins; ITEM 1 | `field.stores_ledger` | P |
| 1804 | an apprentice at the works since; Nib is the fortieth | `north.works_events` | P |
| 1811 | Dame Honoria Pemberton-Gore's portrait | `fenmarch.portrait_pages` | F |
| ~1800 | Nether Sopping starts throwing things down the Pit ("two hundred years") | `wilds` | P |
| 1840 | Rollo, a dog, painted | `fenmarch.portrait_pages` | F |
| 1841 | the Clanging clock goes four minutes fast | `north.clanging_events` | P |
| 1860 | Attempt Eighty-Four comes down in the Long Field (1886 until `NORTH.md` 8.1b) | `field.eighty_four`, `db.build_enemies` | P, repaired |
| ~1900 | Attempt 112, "a hundred years dead", on her rock | `field` | P |
| 1909 | the shipping stops; Bother's light is for the ones coming home | `south` (Bother) | P |
| 1919 | Beatrice Grumnir born (the headstone) | `village.churchyard` | P |
| 1930 | Mr Ottershaw (born 1910, "ninety in March") begins the animals: "seventy years. Three generations." Every case in the gallery is his, which is why none of them has a date on it | `fenmarch.ottershaw_pages` | F |
| 1940 | the Clanging clock's town has been early "for sixty years" | `north.clanging_events` | P |
| 1960 | the Gloamwood Society founded to prove the Thing in the Woods is not there; nine members, a walk a year, The Sighting four times a year (issue 160 in 2000) | `q_wren` (WRE-3) | F |
| 1969 | Gideon Markup prices the Sword of Ultimate Ending | `penultima` | F |
| 1970 | Tobias Frayne's first revival of eleven, "in thirty years" | `frayne` | F |
| 1971 | Edith Pellow sees the Thing, and counts nine heads; The Sighting, issue forty-four | `q_wren` (WRE-3) | F |
| 1974 | Walt Ashbury, twenty-six years at the Eight Hours | `restwell` | F |
| 1977 | Roland Fairweather, eleven, page to Dame Florence Ickworth: the Wyrm of Ickworth, the first of his eleven parties ("since I was eleven", and thirty-four now) | `q_roland` (ROL-3) | P |
| 1986 | Sir Hamo Tench comes to Weeping Bottom for the sea air | `weeping_bottom.hamo_pages` | F |
| 1989 | Corvin, nineteen, sits down in the corner of the Slain Wyvern; Ashcombe floods "in his absence". Dame Winifred at Little Gore. Wat Pardle puts up the Standing Stones, if theory six is right, which it is. Bond No. 1 in the Bonded Warehouse: Nix, fifteen, puts gran's coat in bond till it fits, makes a speech from a crate, and pays the rent by post for eleven years sooner than come back (NIX-1). The same year Nix gives Hulda Bole her first job, a parcel to be delivered at twenty-six, which is also her last. Dr Pike takes a room | `south`, `ashcombe`, `hamlets`, `journey`, `dunnage`, `restwell`, `q_nix` | P/F |
| 1989 | Beatrice Grumnir dies; the parish's plain headstone in the new churchyard, "1919 - 1989"; she has told Hob to make her a marker, and the village stops mentioning it ("eleven years") | `q_hob` (HOB-2), `village.churchyard` | P |
| 1989 | Nix, fifteen, starts the ledger; the first page's eleven things are never sold, and go home in NIX-4 ("eleven years" for every one of them: Bram's mother's pie dish, the Old Man's chair, Hulda Bole's good boots). Hulda takes her first fetching job the same year, and Tolly buys a sheet of stamps | `q_nix`, `south` | P |
| 1989 | Attempt 199 lost in sight of the Tower, "eleven years dead" on her crag; the last entry in the attempt log | `field`, `north` | P |
| 1991 | Sir Aldric Pemberton-Gore the Third goes out errant, "nine years ago"; the flowers under his portrait start. Tom marries Mrs Vane at Fenmarch, in the rain | `fenmarch.fourth_pages`, `portrait_pages`, `tom_pages`; `hamlets.vane_pages` | F |
| 1992 | Aldric, with a commission that says "dragon", talks about Horace with the Wrong Dragon until dark ("eight years ago") | `nomap._wrong_dragon` | F |
| 1994 | Aldric reaches Thistlewick and cannot find the north gate; Perpetua Small wakes on the beach. That winter his horse walks into Plummer's yard at Great Dunnage on her own, saddled ("six years", ALD-4) | `db.build_actors`, `village`; `dunnage.plummer_pages`, `q_aldric` | P |
| 1996 | Mr Pilbeam rescues Rosamund from the eagle | `fairholme` | F |

## 5. Ages stated

| who | age in 2000 | where |
| --- | --- | --- |
| Mirabel | 4,112 ("eight and a QUARTER") | `evermore` |
| Mr Ottershaw | ninety in March | `fenmarch` |
| Thaddeus Rook's rival | ninety-one | `sable_hart` |
| Ysolde Marrow | seventy-eight | `south` |
| Halbert Quy | in his seventies | `south` |
| Mrs Emberthwaite | seventy (Rosamund's word) | `fairholme` |
| Corvin Ash | thirty (nineteen, and eleven years in the corner) | `south` |
| the Cotterills | Cotter 24, Rivet 22, Gudgeon 20, Tappet 18, Ferrule 16, Grommet 15, Clevis 13, Shim 11, Spare 9, and one due in the spring | `north` (Gudgeon's register) |
| Pemberton-Gore IV | nineteen; found the gate at ten | `fenmarch` |
| Toby Wendle | ten | `gladhollow` |
| Clem Blagg | seven | `frostwick` |

## 6. Not decided, on purpose

* **What began the Third Age.** Only the elves know, and nothing may say it
  without Mike.
* **The dates of #2-#40**, beyond the shape in section 3.
* **Grimspite's own age.** He has had the job for 4,800 contract years; how old
  he was when he got it, and in whose years, is his.
