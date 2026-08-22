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

Bram can take up to three of six companions. Each is a different answer to the
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

## Layout

    build/
      mapkit.py      tile vocabulary and drawing helpers; names are what
                     things look like, and were confirmed in screenshots
      db.py          the whole database
      village.py     Maps 1-7: Thistlewick and its interiors
      journey.py     Maps 8-12: overworld, Gloamwood, the Obligatory Tower
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
| Actors 1-7 | Bram, Merribell, Hob, Zephyrine, Nix, Aldric, Piper |
| Classes 1-7 | one per actor, same order |
| Skills 1-2 | engine-reserved Attack and Guard |
| Skills 10-19 | Bram |
| Skills 20-29 | Merribell |
| Skills 30-39 | Hob |
| Skills 40-49 | Zephyrine |
| Skills 50-59 | Nix |
| Skills 60-69 | Aldric |
| Skills 70-79 | Piper |
| Skills 90-99 | enemy and boss skills |
| Items 1-19 | consumables |
| Items 20-29 | key items |
| Weapons 1-29 | roughly four per class, in class order |
| Armors 1-29 | shared body/head/accessory |
| Enemies 1-19 | ordinary encounters |
| Enemies 20-29 | bosses |
| Troops 1-19 | encounter groups |
| Troops 20-29 | set-piece fights |
| Maps 1-7 | Thistlewick and interiors |
| Maps 8-12 | the journey |
| Map 99 | the tile sampler, not part of the game |

## Switches and variables

| id | switch |
| --- | --- |
| 1 | quest accepted (the Elder has said the words) |
| 2 | the party has left the village |
| 3 | Gloamwood cleared |
| 4 | Grimspite defeated |
| 5 | the Prophecy annulled - the game is won |
| 6 | the tower door is unbarred |
| 11-16 | recruited: Merribell, Hob, Zephyrine, Nix, Aldric, Piper |
| 20 | the mimic has been met |

| id | variable |
| --- | --- |
| 1 | companions recruited |
| 2 | **tropes encountered** - the running gag. Every cliche the player walks
     into bumps it, and the ending reads the total back to them. Bump it with
     `story.trope()` and nowhere else. |
| 3 | turnips eaten |

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
