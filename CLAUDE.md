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
| Items 1-19 | consumables (10-12 are southern) |
| Items 20-29 | key items (23-29 are southern) |
| Weapons 1-31 | roughly three per class, in class order |
| Armors 1-22 | shared body/head/accessory; 16-22 are southern |
| Enemies 1-19 | ordinary encounters (12-18 are southern) |
| Enemies 20-29 | bosses (23-26 are the optional ones) |
| Troops 1-19 | encounter groups (11-17 are southern) |
| Troops 20-29 | set-piece fights (24-27 are southern) |
| Maps 1-7 | Thistlewick and interiors |
| Maps 8-12 | the journey |
| Maps 13-18 | Nether Sopping and its interiors, and the lighthouse |
| Maps 19-20 | the Bottomless Pit, the Barrow of the Forty-Fourth |
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

| id | variable |
| --- | --- |
| 1 | companions recruited |
| 2 | **tropes encountered** - the running gag. Every cliche the player walks
     into bumps it, and the ending reads the total back to them. Bump it with
     `story.trope()` and nowhere else. |
| 3 | turnips eaten |
| 4 | tales heard in the Slain Wyvern - Hosea pays out at six |
| 5 | bounties claimed |

## Verifying

Nothing here is judged by reading the data back. Maps are judged from
screenshots, fights from numbers, and events from a scripted playthrough.

    node ../tools/serve.js . 8766                # background it, then
    node ../tools/scenario.js build/scenarios/opening.json

Headless runs at about twelve frames a second on a map and three in a battle,
so playing a boss fight through a scenario takes the better part of an hour and
mostly tests the renderer. `finale_ending` sidesteps that: it feeds the finale's
own command list to the interpreter with the Battle Processing, Show Text and
Show Choices commands filtered out, so every switch, item and screen effect
still runs, in about a minute, with no key presses at all. Use the same trick
for any long cutscene.

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
| `finale_ending` | the ending itself: switches, the receipt, the trope
  tally and the return to the title, with the battles and the message
  windows stripped out of the command list so it runs without input |
| `reachable_home` | the bed, the sword and the front door of Bram's house,
  walked to with the arrow keys and triggered with the action button |
| `reachable_village` | the Fisher on the pond bank, Prophecy Hall's door, the
  Wall of the Forty-Seven, the Creed and the Organ, the same way |
| `south_road` | the coast road east is walkable end to end, the shingle is
  its own encounter region, and the town door opens |
| `reachable_sopping` | all four doors of Nether Sopping, walked to with the
  arrow keys from the north road |
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
