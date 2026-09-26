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
