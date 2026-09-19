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
2. **Map ids continue upward from 31.** Penultima took 29 and 30. Never
   renumber.
3. **The door is claimed by name, not by coordinate.** The module exports
   `SITE = "<the name worldmap.json's door events carry>"` and
   `world_doors(base_id, cells)`; `journey.world_map` drops the placeholders
   carrying that name and hands the module *their* cells. **Never copy a site's
   world-map coordinate into `places.py`** - only the square the player is put
   back on coming out.
4. **`placeholder_doors.json`'s count goes down by the number of cells you
   claimed**, and you edit that number on purpose. It is 39 now. That scenario
   is the check that notices a half-wired site.
5. **A scenario that walks in from the world map and back out.** Not
   `$gameMap.event(n).start()` - walking is the only thing that proves the door
   swap landed on the right squares.
6. **Faces.** `build/art.py`, `Gen_People1` slots 6 and 7 are free and then it
   is a new sheet. Six `BIOS.md` characters already have settings files in
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
| 1 | Restwell | 1 | 2 | 2 | `BIOS.md` |
| 2 | Hithermost cluster | **3** | 2-3 | 1 | `BIOS.md` |
| 3 | Fairholme and the lair | **2** | 3 | 1-2 | `BIOS.md` |
| 4 | Olde Evermore | 1 | 2 | 1-2 | `BIOS.md` |
| 5 | Gladhollow | 1 | 1-2 | 0 | `BIOS.md` |
| 6 | The Former Premises | 1 | 1 | 1 | `WORLDMAP.md` 7.4 |
| 7 | The seven with no map | **7** | **0** | 3-5 | `COMPANIONS.md` 3 |
| 8 | Tobias Frayne | 1 | 1 | 1 | `COMPANIONS.md` 4 |
| 9 | Village 1 | 1 | 0 | 0 | `WORLDMAP.md` 8 |
| 10 | Frostwick | 1 | 4 | 6 | `WORLDMAP.md` 7.3 |
| 11 | Coldbarrow | 1 | 1 | 1 | `COMPANIONS.md` L6 |
| 12 | The Sable Hart | 1 | 1 | 5 | `COMPANIONS.md` L7 |
| 13 | Little Gore and Sump | **2** | 2 | 2 | `COMPANIONS.md` L8 |
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

### 2. The Hithermost cluster — (30,23), (30,22), (30,21)

**Three doors, one module, one face**, which is the best ratio on the list.
`Village A` at (30,23), **Chapel of Continuance** `Temple C` at (30,22), and
**The Door into the Mountain** `Tunnel` at (30,21), stacked up the pass.

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

### 3. Fairholme and Mrs Emberthwaite's lair — (104,73) `Castle A`, (111,69) `Cave A`

Two doors, one module: they are one bio.

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

### 5. Gladhollow — (33,111), `Village B`

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
* **`COMPANIONS.md` contradicts itself about Ashcombe Lake** - it is in this
  table as one event and in L3 as "the drawn-down street (1 small map)". Build
  the event here; the small map, if it is ever wanted, belongs to step 14.

### 8. Tobias Frayne — (66,82), `House (Town)`

`COMPANIONS.md` 4: a cottage on the coast road, four cells from Thistlewick.
**Revived eleven times, and has developed a relationship with mortality.**
Merribell's MER-4.

* **Build:** the cottage (1). One face.
* Cheap, close to country the player already walks, and it is a good one to do
  while the pattern is fresh.

### 9. Village 1 — (60,61), `Village B`

**A decision, not a build.** `WORLDMAP.md` 8: worldgen placed it itself as an
extra beyond the anchors, it has no backstory in any document, and two
candidates were measured against it and both refused. It is being kept surplus
on purpose rather than filled with the first idea that fits.

* **Name it or remove it**, and either is a few lines. If it is removed, the
  placeholder count drops by two and `placeholder_doors` needs editing; if it is
  named, it joins this list as a step of its own.
* It is here at number nine so that the decision is taken while the list is
  still short, not left to the end.

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

### 11. Coldbarrow — (50,19), `Temple A (Snow)`

`COMPANIONS.md` L6, "the single cheapest location here and the one with the best
sight gag". One room, one enormous map of the island with pins in it, one
clerk - **Chapter Clerk Mordaunt**. Nine pins, one knight, a committee, a
review. Serves ALD-3, and ALD-2 if the chapel is here rather than at the
Sisterhouse.

* **Build:** 1 map, 1 face.

### 12. The Sable Hart — (24,75), `House (Town)`

`COMPANIONS.md` L7. An inn on a moor where every corner is taken: **five hooded
men being scrupulously fair to each other about seating**, with a rota for the
darkest corner, a newsletter and a league table. Corvin's COR-3, and where
COR-4's fair should be pitched if the fair does not get its own map — it does,
at step 7.

* **Build:** 1 map. **Five faces**, which is the whole joke and is why a cheap
  map is not a cheap step. They can be five variations on one look; doubling up
  is established practice.

### 13. Little Gore and Sump — (97,101) `House (Village)`, (78,102) `House (Desert)`

`COMPANIONS.md` L8. Two hamlets, one map each, both essentially one street and a
reason. **Little Gore** is four miles from Fenmarch and is where the letter was
always going - **Hester Vane**, married nine years ago, keeps the invitation.
**Sump** has not had any water since 1794 and has a wasp problem the parish
cannot allocate. Either can host PIP-4's eleven interviews. Serves ALD-1,
MER-5, PIP-4.

* **Build:** 2 maps, 2 faces, one module.

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
   total. It is already at 77% after Penultima's one moment. **This is the one
   thing on this list that genuinely cannot be done incrementally**, because it
   is a judgement about a total that is not known until the total stops moving.
6. Then, and only then, push `master` to **`live-rpg`**.
