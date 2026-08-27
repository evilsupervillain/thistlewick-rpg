# The Obligatory Quest

An RPG Maker MZ 1.10.0 game. The game is data, not code: everything lives in
`data/*.json`, the unmodified engine is in `js/rmmz_*.js`, and the art, audio
and effects are in `img/`, `audio/` and `effects/`.

This project is built with the harness in the parent workspace. Read
`../CLAUDE.md` and `../MZ-DATA-FORMAT.md` first; they cover the data format and
the tools. Everything below is specific to this game.

    python3 build/build_game.py                 regenerate every data file
    python3 ../tools/validate.py .              check the data after every change
    node ../tools/serve.js . 8766               serve this game (background it)
    node ../tools/shots.js /tmp/s 1:20:24       screenshot places in it

## Premise

Every hundred years the Dark Lord rises in the Obligatory Tower, and the village
of Thistlewick sends a Chosen One north to put him down. It has worked
forty-seven times. Bram, a turnip farmer, is Chosen One number forty-eight,
selected by the Prophecy Committee while he was asleep and therefore unable to
object.

The joke the game is built around is that the Prophecy is a *contract*. Grimspite
the Inevitable does not want to be the Dark Lord; he is four thousand years into
a renewable engagement he cannot get out of. Beat him and the Prophecy itself
unrolls to enforce clause twelve, and *that* is the real last boss.

Bram can take up to three of nine companions. Each is a different answer to the
same fight, so who you pick changes how combat plays:

| who | class | good at | bad at |
| --- | --- | --- | --- |
| Bram | Chosen One | everything, slightly; enormous luck | nothing, impressively |
| Merribell | Field Medic | healing, reviving, Light | hitting things |
| Hob Grumnir | Blacksmith | HP, ATK, DEF, one huge hit | speed, magic, being subtle |
| Zephyrine | Hedge Mage | elemental nukes, MAT | HP, DEF, MP economy |
| Nix | Acquisitions | speed, evasion, multi-hits, stealing | taking a hit |
| Sir Aldric | Knight Errant | DEF, covering allies, party buffs | damage, speed |
| Piper Quill | Bard | buffs, debuffs, party utility | raw numbers |
| Corvin Ash | Doomed Rival | dark damage, and more of it the worse things get | DEF, luck, being told the school is very good |
| Wren Halloway | Cataloguer | multi-hit range, poison, armour-shredding, double drops | raw damage |
| Roland Fairweather | Guest Star | everything, genuinely | being there at the end |

The last three are found in a tavern in the south, and the last of them
**leaves at the door of the Obligatory Tower**, which is deliberate. See
`EXPANSION.md` - it is the design document for the whole southern half and is
worth reading before touching any of it.

`NORTH.md` is the design document for what comes next: Upper Clanging, the
airship, and a pass over the whole game adding a kind of joke it currently has
none of. Its section 1 is the specification for every line of dialogue in it,
including what is deliberately out of bounds; read that before writing any of
this game's humour, not just the north's.

## The ending

`journey.finale_event` is the longest command list in the game and most of it is
optional. It is worth knowing its shape before adding to it, because the two
halves are built differently on purpose.

**Inside the Grimspite scene**, before the fight, are two branches on
`SW_CLAUSE_SEVEN` and `SW_OTT_MATERIALS` - the two questions Ott can send the
player up here with. They are separate switches on separate branches so that
either can be asked without the other, and the finale is the only place either
is ever answered. He is never told the airship flew.

**After the fight** the Prophecy's tally is fourteen appended `if_then` blocks
reading `SW_ROLAND_GONE`, `SW_SOUTH`, `VAR_BOUNTIES` (two tiers, the lower
nested in the higher's else), `SW_HISTORY_DONE`, `SW_LAMP_LIT`,
`SW_BENCH_DONE`, `SW_TWO_HUNDRED_FLEW`, `SW_84_REBUILT`, `SW_ITEM_ONE_USED`,
`SW_HOB_BRYD`, `VAR_TROPES` (40 / 20 / else), `SW_BALLAD_DONE`, `VAR_BLUSHES`
and `SW_MET_QUY`. Every one is additive: a new line here is a new block, and
nothing that is already in the tally comes out or gets re-voiced.

**Two counter thresholds are cut against totals that keep moving**, so anything
that adds a `story.trope()` or a `story.blush()` site has to come back here.
`VAR_TROPES` is 40 / 20 against about sixty reachable; `VAR_BLUSHES` is 20
against **twenty-five** reachable, measured off the data in August 2026. Keep
the blush tier at four fifths of the true total - `NORTH.md` 2.3 has the count
and, more importantly, why counting it by grep gives 28 and is wrong.

**ITEM 1 is a page, not a branch.** The crate is a whole scene rather than a
question, so page 1 of the event is `c[:split] + item_one_scene() + c[split:]`
with an `itemValid` condition, and page 0 rebuilds byte for byte. The splice is
after the Shock2 sting and before the battle, which is the only placement that
does not make him a liar: he has just said he has heard all of them, and four
windows later he says this one is new.

`finale_ending` covers all of it in eight passes; see Verifying.

## Layout

    build/
      mapkit.py      tile vocabulary and drawing helpers; names are what
                     things look like, and were confirmed in screenshots
      db.py          the whole database
      village.py     Maps 1-7: Thistlewick and its interiors
      journey.py     Maps 8-12: overworld, Gloamwood, the Obligatory Tower
      south.py       Maps 13-18: Nether Sopping, the Slain Wyvern, the Guild,
                     the outfitters, #45's cottage, the lighthouse
      wilds.py       Maps 19-20: the Bottomless Pit and the Barrow, plus the
                     southern half of the world map - `journey.py` still owns
                     Map 8 and calls four hooks in here while drawing it
      north.py       Maps 21-25: Upper Clanging and its four interiors
      field.py       Maps 26-27: the Long Field, Attempt Eighty-Four, the
                     wreck of the 199th and ITEM 1, plus the north-west of the
                     world map - the same arrangement, five `north_*` hooks
                     called from `journey.py` - and the three places out at sea
                     that only the airship can reach. It also holds the three
                     pages `north.py` appends to Ott and the works stores
                     ledger, because those are the field's payoff and the
                     crag's
      places.py      map ids, and the coordinates two modules have to agree on
      story.py       shared dialogue helpers and the endgame
      build_game.py  runs all of the above, then System.json and MapInfos
      scenarios/     scripted playthroughs for `tools/scenario.js`
      balance.py     offline damage report: evaluates the real formulas
      sampler.py     throwaway tile sampler; writes Map099. `build_game.py`
                     deletes any map that is not on its own list, so the
                     sampler cannot ship by accident - run it *after* a build,
                     never before one you intend to keep

## Ids

Nothing here is ever renumbered - saves and cross-references point at ids.
Append instead.

| range | what |
| --- | --- |
| Actors 1-10 | Bram, Merribell, Hob, Zephyrine, Nix, Aldric, Piper, Corvin, Wren, Roland |
| Classes 1-10 | one per actor, same order |
| Skills 1-2 | engine-reserved Attack and Guard |
| Skills 10-19 | Bram |
| Skills 20-29 | Merribell |
| Skills 30-39 | Hob |
| Skills 40-49 | Zephyrine |
| Skills 50-59 | Nix |
| Skills 60-69 | Aldric |
| Skills 70-79 | Piper |
| Skills 90-99 | enemy and boss skills |
| Skills 100-109 | Corvin |
| Skills 110-119 | Wren |
| Skills 120-129 | Roland |
| Skills 130-139 | southern enemy and boss skills |
| Skills 140-149 | northern enemy and boss skills |
| Items 1-19 | consumables (10-12 are southern, 13-15 northern) |
| Items 20-29 | key items (23-29 are southern) |
| Items 30-32 | northern key items - the 20-29 block is full. 30 is the
  oilskin, 31 is Attempt 112's number-plate, 32 is ITEM 1. The range was
  reserved to 36 and three were enough |
| Weapons 1-33 | roughly three per class, in class order; 32-33 are the north's |
| Armors 1-26 | shared body/head/accessory; 16-22 are southern, 23-26 northern
  - Sensible Trousers, Works Cap, The Fuse (Removed) and the Governor |
| Enemies 1-19 | ordinary encounters (12-18 are southern). **Full**: northern
  ordinary encounters continue at 30 |
| Enemies 20-29 | bosses (23-26 are the optional ones, 27 is Attempt
  Eighty-Four) |
| Enemies 30-32 | northern encounters: Loose Pressure, Attempt (Unnumbered),
  Ambulant Salvage. Reserved to 35 |
| Troops 1-19 | encounter groups (11-17 are southern). **Full**: northern
  groups continue at 30 |
| Troops 20-29 | set-piece fights (24-27 are southern, 28 is Eighty-Four) |
| Troops 30-33 | northern encounter groups |
| Maps 1-7 | Thistlewick and interiors |
| Maps 8-12 | the journey |
| Maps 13-18 | Nether Sopping and its interiors, and the lighthouse |
| Maps 19-20 | the Bottomless Pit, the Barrow of the Forty-Fourth |
| Maps 21-25 | Upper Clanging and its interiors: the works, the inn, the forge,
  the Parish Rooms. `north.py` |
| Maps 26-27 | the Long Field, and the wreck of Attempt 199 on her crag.
  `field.py` |
| Map 99 | the tile sampler, not part of the game |

Icon indices in `db.py` and in the `\I[n]` codes in dialogue were re-checked
against `img/system/IconSet.png` cell by cell when the south was added; several
of the original ones pointed at the wrong cell (rings that were orbs, a
prophecy that was a glove). The sheet is 16 icons to a row: row 6 is weapons in
`wtypeId` order from 96, row 8 is armour from 128, row 11 is consumables from
176, row 12 is tools and instruments from 192, and the food is at 256-280.

## Switches and variables

| id | switch |
| --- | --- |
| 1 | quest accepted (the Elder has said the words) |
| 2 | the party has left the village |
| 3 | Gloamwood cleared |
| 4 | Grimspite defeated |
| 5 | the Prophecy annulled - the game is won |
| 6 | the tower door is unbarred |
| 11-19 | recruited: Merribell, Hob, Zephyrine, Nix, Aldric, Piper, Corvin, Wren, Roland |
| 20 | the mimic has been met |
| 21 | Roland has left at the tower door |
| 22-24 | the Feud: jar going south, reply going north, done |
| 25-27 | the Guild: asked, Form A-1 found, registered |
| 28-31 | bounties: crab beaten, Crooke beaten, and each one paid |
| 32-33 | the lighthouse: asked for oil, lit |
| 34-36 | the Pit: asked, badger gone, Splint has paid |
| 37-38 | the Barrow: entered, the Forty-Fourth has stopped |
| 39-40 | the bench: asked for, built |
| 41-42 | Hosea's history: asked, complete |
| 43 | #45 told Bram what to ask Grimspite - this changes the finale |
| 44 | met #46 on his log |
| 45 | has been to Nether Sopping |
| 46 | knows the wyvern is a goose |
| 47-67 | the north. Named in `db.py` and specified in `NORTH.md` section 10:
  47 been to Upper Clanging, 48 Ott has explained what she needs, 49-50 the
  oilskin, 51-52 the spar, 53 the airship flies, 54-55 ITEM 1, 56-57 Attempt
  Eighty-Four, 58 Hob and Bryd went for a drink, 59-60 the ballad, 61 the
  Cold Winter, 62 met the Cotterills, 63 the nine-year-old has applied,
  64 walked the Long Field, 65 clause seven, 66 room four, 67 Gerald,
  68 the Two Hundred set down beside the tower, 69 the two travellers
  have been asked how long, exactly - the retrofit's one global switch,
  because the joke is one moment across two events and a self switch is
  keyed on (map, event id, letter), 70 Ott asked you to ask what the tower
  is made of, which is also the last thing her flying chain sets and so the
  one switch that means "Ott has nothing left owing", 71 the crate was set
  down in front of the throne. **59 is reserved and unused** - it was
  drafted as the ask half of an ask-then-done pair and the fete minutes
  turned out to be a board rather than a conversation. It is never set and
  never read, and `System.json` names it as unused so nobody goes looking
  for the event |

| id | variable |
| --- | --- |
| 1 | companions recruited |
| 2 | **tropes encountered** - the running gag. Every cliche the player walks
     into bumps it, and the ending reads the total back to them. Bump it with
     `story.trope()` and nowhere else. |
| 3 | turnips eaten |
| 4 | tales heard in the Slain Wyvern - Hosea pays out at six |
| 5 | bounties claimed |
| 6 | wreck plaques read - Ott opens up at twelve. The thirteenth plaque
     deliberately does not count: there are twelve readable plates in the
     Long Field and the thirteenth is one you make |
| 7 | **things nobody quite said** - the north's running gag, and the
     companion to variable 2. Every Register A moment bumps it once, on first
     sight, and the ending prints the total. Bump it with `story.blush()` and
     nowhere else. `NORTH.md` 2.3 is the specification and it matters: the
     joke exists only in aggregate, which is exactly what keeps every
     individual instance deniable. **Twenty-five reachable moments**; a grep
     of `data/` says 28 and over-counts, for the three reasons in 2.3 |
| 8 | Ott's beat while the oilskin-and-spar order is outstanding - a nine-beat
     chain. A variable and not a run of self switches because a page
     condition can name exactly one self switch, and four letters do not
     reach nine |
| 9 | the same for the seven beats after the Two Hundred flies. Its last write
     is the one that sets switch 70, which is what makes that switch usable as
     "Ott has nothing left owing" - and anything appended to Ott below her
     ladders has to require it, or it shadows them. `NORTH.md` 16 step 6 is
     the write-up of the lockout that taught us so |

## Verifying

Nothing here is judged by reading the data back. Maps are judged from
screenshots, fights from numbers, and events from a scripted playthrough.

    node ../tools/serve.js . 8766                # background it, then
    node ../tools/scenario.js build/scenarios/opening.json
    ../tools/scenarios.sh .                      # or all thirty-three

The whole suite is a little over an hour, so background it and read
`build/scenarios/logs/` afterwards rather than watching it. `scenarios.sh`
checks before it starts that 8766 is serving *this* game and that no Chromium
has been orphaned by an earlier killed run, because both of those turn an hour
of machine time into an hour of confusing output.

Headless runs at about twelve frames a second on a map and three in a battle,
so playing a boss fight through a scenario takes the better part of an hour and
mostly tests the renderer. `finale_ending` sidesteps that: it feeds the finale's
own command list straight to the interpreter with Battle Processing filtered
out, so every switch, item and screen effect still runs, with no key presses at
all. Use the same trick for any long cutscene.

**Filtering the Show Texts out as well is the version of that trick to avoid,
and it is what this scenario used to do.** An optional ending is *made of*
Show Text inside a Conditional Branch, so a scenario that deletes the messages
before running the list can assert nothing whatever about which branch it took
- and four shipped endings sat behind checks that would have passed with every
one of them deleted. The fix is to take the blocking out of the messages
instead of taking the messages out of the list:

    Game_Message.prototype.add = function (t) { window._lines.push(t); };
    Game_Message.prototype.isBusy = function () { return false; };

The interpreter then runs the whole cutscene without ever opening a window -
`hasText()` is false, so `Window_Message` does not try - and what comes back is
every line the player would have read, in order, ready to assert against. Two
things go with it. A choice must be answered by a shim on `setupChoices`,
because a choice left unanswered takes *neither* branch: `command402` compares
against a `_branch` entry nothing ever wrote, and the run silently loses
everything under both halves. And if the pass is only about what was printed,
filter the waits and screen effects (`230`, `221`, `222`, `223`, `225`) as
well - the interpreter will run a hundred thousand commands in a frame before
it decides it has frozen, so the entire finale executes in one. That is what
makes eight passes over it cost less than the single pass did before.

| scenario | what it proves |
| --- | --- |
| `opening` | the house scene, the sword, the turnips, walking out the door |
| `village` | the gate refuses a Chosen One with no quest; the Elder gives it; Merribell joins |
| `gate` | a lone hero is still turned back; two of them get onto the world map |
| `journey` | Gloamwood, the Thing that blocks the way, and the tower door |
| `tower_door` | a party without Nix finds the key under the mat; the Cache arms all seven |
| `nix_door` | Nix opens the same door without it |
| `battle_mook` | a random encounter at level 6 is a fight, not a formality |
| `finale` | the throne-room scene runs and the Grimspite fight starts |
| `finale_ending` | the ending, in eight passes over the same command list.
  Seven fast ones capture the narration and assert which optional endings
  printed: clause seven and the materials question independently and together,
  the two `VAR_BOUNTIES` tiers each with the other's line asserted *absent*,
  and the ITEM 1 stores-book line. Pass D is the one worth having - it is the
  only state in which Grimspite saying she will never get one off the ground
  and the attempt log reporting that she did are both on screen, which is the
  game's central joke and had nothing standing behind it. The eighth runs at
  full length with the waits intact for the switches, the receipt and the
  return to the title |
| `reachable_home` | the bed, the sword and the front door of Bram's house,
  walked to with the arrow keys and triggered with the action button |
| `reachable_village` | the Fisher on the pond bank, Prophecy Hall's door, the
  Wall of the Forty-Seven, the Creed and the Organ, the same way |
| `south_road` | the coast road east is walkable end to end, the shingle is
  its own encounter region, and the town door opens |
| `north_road` | the west road is walked end to end with the arrow keys, from
  the Gloamwood's north mouth to the door of Upper Clanging, plus both spurs;
  and the Standing Stones are proved to be *beside* the road rather than on it |
| `reachable_sopping` | all four doors of Nether Sopping, walked to with the
  arrow keys from the north road |
| `reachable_clanging` | walking into Upper Clanging off the world map, up the
  whole street and both flights of steps, and through all four doors - and
  that the rain stops indoors and does not follow the player home |
| `clanging_cast` | the town's dialogue: Ott's four steam beats arrive one per
  conversation and then stop, Spare's three, the whole Cotterill doorstep, the
  Cold Winter, Gudgeon over the parish ledger, the Parish Rooms counter opening
  as a real shop, and Hob and Bryd - with `VAR_BLUSHES` asserted after every one
  of them, because a counter nobody checks is a counter that silently reads zero
  in the ending. It is also where Ott's first rung is proved **with** Merribell
  in the party: that moment is a conditional branch, and a conditional blush
  that has only ever been run one way is indistinguishable from one somebody
  deleted. `two_hundred` runs the same four rungs without her and asserts the
  counter does not move |
| `clanging_faces` | each of the eighteen northern faces read off the **live
  message window** rather than off the data, and screenshotted. It is the check
  that catches an off-by-one between `story.FACES` (0-based, like MZ's
  `faceIndex`) and `img/pictures/` (1-based), which is a mistake that builds,
  validates and looks like somebody else answering - and the only thing standing
  behind two casting decisions with reasons: Winnie on `People1` 7 because she
  is sixty, and Rivet off `SF_Actor2` 2 because that face reads as a girl at
  both sizes |
| `two_hundred` | Ott's quest end to end without Hob: the ask amidships, the
  spar in a day, forty bolts of oilskin on account, and the airship placed on
  the world map at (10, 13). It also walks **both of Ott's beat chains** - five
  conversations of the order chain and all seven of the flying chain - because
  five of her six Register A moments live in them and nothing else in the suite
  executes one. The last beat of the flying chain is what sets
  `SW_OTT_MATERIALS`, so this is also the check that the ladders can be finished
  at all |
| `hob_and_bryd` | the same spar with Hob in the party - forged in an
  afternoon, and then they go for a drink, and `SW_HOB_BRYD` |
| `airship_lands` | the one that protects the joke. It asserts
  `isAirshipLandOk` out of the flags, then **flies over the tower door and
  presses the button**, and the engine refuses; then lands on the grass beside
  it and walks in. Then all three of the air-only rocks |
| `tavern` | all six tales count, and each one counts as a cliche |
| `tavern_history` | Hosea asks for six, pays out at six, and the wyvern turns
  out to be a goose |
| `recruit_south` | Corvin and Wren join; a full party is turned down |
| `guest_leaves` | Roland joins over-levelled and is gone - with his gear
  handed back - by the time the party reaches the tower door |
| `feud` | the jar goes south, the reply comes north, the locket arrives |
| `guild` | reference plus hat plus the mat equals a Guild Card |
| `barrow` | the card opens the mound, the Forty-Fourth stops and asks for a
  bench, the bench is built, and Ysolde answers |
| `lighthouse` | Mrs Barrow's shelf is stocked and Lamp Oil can be *bought*
  through the shop windows, not granted - then Bother, the climb and the lamp |
| `long_field` | the gate off the spur road, the twelve plaques counting once
  each, `VAR_PLAQUES` landing on twelve, clause seven out of Ott, and the
  thirteenth plaque made out of Attempt 112's number-plate - which does *not*
  count, because twelve is twelve. Also the guard: twelve plaques on their own
  must **not** change which page Ott is on, because those pages sit below both
  of her beat chains and would delete them |
| `eighty_four` | the furrow is walkable from her empty plot to the top of the
  field, the action button reaches her, "Stop her" starts the right fight
  against the right enemy, and the stop, the rebuild and the governor |
| `item_one` | the stores ledger, the crag, the log with seven minutes missing
  out of it, ITEM 1 off the crag for the first time since 1802, and Ott
  rendering it down into a weapon and an accessory |
| `item_one_throne` | the stretch goal: carrying ITEM 1 to the throne room
  instead. Both branches of the choice - "Draw your weapon" keeps the crate
  and sets nothing, "Set the crate down" lights it - plus the page mechanism
  itself, which is that `findProperPageIndex()` returns the crate page while
  the crate is held and drops back to the ordinary finale the moment it is
  spent. The crate block is found in the command list **by its label**: the
  finale opens with a choice of its own, and slicing from the first code 102
  on the page runs the whole introduction and takes the wrong branch while
  reporting a pass |
| `blushes` | the whole of `NORTH.md` section 3, in one walk: room four, the
  house register, Sops, both travellers, Perpetua and Gerald, the fete
  minutes, the washstand, Wren's three specimens and the second notice at the
  Standing Stones. Every one of them is asked a second time and `VAR_BLUSHES`
  asserted not to have moved, and the last check is that the retrofit came to
  eleven - the number 2.3 asked for |

The two `reachable` scenarios exist because every other scenario here starts
its events with `$gameMap.event(n).start()`, which proves what an event does
and nothing at all about whether the player can get to it. They walk instead,
and check `$gameMap._interpreter.eventId()` to see which event the button
press actually reached. `validate.py` catches the same class of bug statically
now, so these are the confirmation rather than the search.

    python3 build/balance.py 8

prints, for every enemy, what each character's best hit does to it and what its
best hit does to the squishiest party member. Use it before touching a stat: the
fights were tuned so a four-person party kills a mook in two or three turns and
survives five or six of its turns.

## Conventions

* Every event is named for what it is, and the recruitable six are named after
  the character so `Merribell` is findable by grep.
* **A page appended below a ladder must require that ladder's terminal
  switch.** `Game_Event.refresh` takes the *last* page whose conditions hold,
  so appending is not the same as sequencing: a new page whose condition can be
  true while a page above it still owes the player a beat does not follow that
  page, it deletes it - silently, permanently, with no symptom but the
  character saying the wrong thing forever. Ott's three field pages were
  appended on a plaque count that is reachable on foot long before the works is
  asked for an airship, which shadowed her fabric page, her handover page and
  both of her beat chains and made the whole questline unreachable for anyone
  who read the field first. The fix is to name the switch that means "this
  character has nothing left owing" - for Ott, `SW_OTT_MATERIALS`, the last
  thing the flying chain sets - and require it on every appended page.
  Reordering is not a fix; it only chooses which ladder dies.
* Dialogue lives in `village.py` / `journey.py` next to the event that says it,
  not in a strings table - it is read far more often than it is reused.
* Colour codes in text: `\C[6]` for a speaker's name, `\C[3]` for a thing you
  just got, `\C[2]` for something ominous.
* **The speaker's name goes inside the message, not in a name box.** MZ's Show
  Text has a fifth parameter, `speakerName`, which draws the name in its own
  little window above the message and costs the line nothing - it is the
  engine's own answer to the width problem, and it is deliberately not used
  here. `\C[6]Speaker:\C[0] ` in front of the first line of each window is the
  look this game has settled on, and the eight-to-seventeen characters it costs
  are a price worth paying. Do not "fix" a long line by moving the name out of
  it; break the line.
* A line of dialogue is at most **47 characters** including the `Speaker: `
  that `say()` puts in front of the first line of every window - so a line by
  Councillor Fenn has thirty characters to play with and one by Hob has
  forty-two. Narration, which has no face beside it, gets 60. `say()` and
  `narrate()` measure every line and refuse to build one that would be drawn
  off the edge of the window, naming the speaker and how much is over; break
  it earlier rather than letting anything wrap it, because where a line breaks
  is the joke landing or not. Item and skill descriptions are prose, so
  `db.described()` wraps those onto the two lines the help window shows.
