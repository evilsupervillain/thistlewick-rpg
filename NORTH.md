# The North

A design for the third and last quarter of *The Obligatory Quest*: an
industrial town at the top of the island, an airship that arrives too late to
be useful, and a pass over the whole existing game to add a kind of joke it has
so far had none of.

`CLAUDE.md` is the reference. `EXPANSION.md` was the intent for the south, and
this is the intent for the north. Read both first. Section 1 of this document is
not optional colour - it is the specification for every line of dialogue below
it, and a session that skips it will write the wrong jokes with great confidence.

---

## 0. What this adds, in one paragraph

Thistlewick believes the Prophecy. Nether Sopping has been discarded by it.
**Upper Clanging intends to solve it** - with infrastructure, on an industrial
scale, at the fourth generation of trying. Two hundred years ago somebody up
there read "every hundred years the Dark Lord rises" and correctly identified a
recurring problem, and recurring problems are an engineering matter. They have
built one hundred and ninety-nine flying machines. None has reached the tower.
The two hundredth is in the shed, and it is only missing one part, and the part
is you.

Alongside that, a retrofit: **Register A humour** - the innocent double meaning -
threaded through the whole game, which currently has none.

---

## 1. The doctrine

### 1.1 Two registers, and which one this is

There are two things "an adult joke in a family film" can mean.

**Register B - adult experience.** A joke that goes over children's heads
because they have not lived it: a long marriage, a career you cannot leave, the
specific exhaustion of a parish council, the fact that grief and admin arrive
together. **This game is already very good at Register B and needs no more of
it.** Ysolde's "you keep someone alive, and then they go and live, and you don't
get to see much of it" is the standard to keep clearing.

**Register A - the innocent double meaning.** A line that is entirely innocent
on the page and lands somewhere else in an adult ear. The game has none of this
and the north is where it goes.

The model is Bilbo and Mrs Bracegirdle: he says "you have been productive," she
smiles and nods, and *nothing improper has been said by anybody*. It works
because the surface reading is **a compliment** and the marriage is **good**.

### 1.2 The rule

> **The comedy is embarrassment, never resentment.** Somebody goes red. Nobody
> is unhappy. Every one of these is a joke about people who like each other very
> much, overheard by somebody who was not supposed to be listening.
>
> **And the game never says the thing.** The player's own head says it. Every
> line must be defensible as literal - a compliment, a repair, a census entry,
> a child reporting the news.

Corollary: if a joke needs the game to confirm it, it is a wink, and it is out.
Winks make parents wince. A closed subject makes them laugh.

### 1.3 The six mechanisms

1. **The innocent superlative.** A word that means one thing and lands as
   another, offered as praise.
2. **The leaky child.** A child reports household news verbatim, uncomprehending,
   at volume, in company. The parents go scarlet. The child is unharmed and
   thinks the subject is buns.
3. **The professional register.** *The party already contains three people whose
   ordinary working vocabulary is somebody else's blush.* **Merribell** is a
   field medic and says anatomical words the way you would say "elbow."
   **Wren** is a taxonomist, and taxonomy is largely the study of how things
   reproduce. **Ottoline Hoyle** makes three, because steam engineering's real
   terminology is filthy-sounding and completely innocent. Meanwhile **Piper**
   is a bard and the bawdy verse is *literally the job*. Four of eleven speaking
   professionals are natural delivery systems and none of them has to be crude -
   they only have to be good at their work while Bram is in the room.
4. **The accidental record.** A parish register, an inn ledger, a works log. A
   document does not know what it is saying.
5. **The refusal.** A closed subject is funnier and safer than an open one.
6. **The reaction shot.** Nobody says anything; the room says it. The game
   already does this beautifully - the whole tavern staring at the ceiling for
   Perpetua. Reuse that machinery.

### 1.4 Bram is the straight man, free of charge

A turnip farmer with parish-council manners, in a narration voice that is
already naive ("You ask whether…"). Two towns of writing have produced the
perfect innocent without needing him for it. Use him. He asks the polite
question; somebody answers it honestly; the joke happens in the gap.

### 1.5 The tone tests

Apply all four to every line:

* **Would it still be a good line if the second reading did not exist?** Ott's
  "it's a box, you stuff it, that is what it is called" is funny as pure
  exasperation. If a line is only funny with the second reading, cut it.
* **Is anybody in it unhappy?** If yes, it is the wrong joke. Rewrite until the
  couple in it are fond of each other.
* **Could you read it aloud at a village fete?** (See 3.3. This is a live
  question inside the game now.)
* **Does the game explain it?** If yes, delete the explanation.

### 1.6 Out of bounds

These were considered and rejected. They must not drift back in:

* **Any "I hate my wife" construction.** Not funny, and not what children should
  absorb about marriage. The working assumption for this game is that **most
  marriages are healthy and wholesome**, and the humour comes from that, not in
  spite of it.
* Affairs, or anything implying one. No "she is NOT his sister." No landlady's
  list of who cannot be roomed next to whom.
* Divorce played for comedy. The Hermit is not separated. Halbert Quy is not
  hiding from anybody. There is no amicably-divorced adventuring party running a
  business.
* Grimspite and the Prophecy are **an employment contract**, not a marriage. He
  has a renewal clause and a non-compete and no idea what Tuesday is. Do not
  reach for the spouse reading; the job reading is stronger and it is the one
  the finished game already implies.
* Anything sexual *about* the child characters. Sops and Spare are reporters
  only, and the joke is always their innocence.
* Drunkenness as a punchline. Sopping Pale is texture, not a gag.
* Nobody is diminished by their own punchline. Especially not Ysolde, Merrow,
  Ambrose or Ott, who are carrying the emotional weight of two expansions.

---

### 1.7 The additive rule

**Nothing already in the game is removed, rewritten or re-voiced.** Not a line,
not a page, not a face. A player who has finished this game must be able to
replay it and find every conversation exactly where they left it.

That is a constraint, not a preference, and it has teeth: several ideas in the
first draft of this document were rewrites, and every one of them has been
redone as an addition. It also turned out to make two of them better, which is
worth knowing before arguing with it.

Three legal patterns, in order of preference:

**1. A new event.** A new person in an existing room, a new thing to look at, a
new noticeboard next to an old one. Always allowed, always the first thing to
try. The player gets more to click on and the old content is untouched.

**2. An appended page.** `Game_Event.refresh()` selects the **last** page whose
conditions are satisfied, so a page appended to the end of an existing event's
page list, guarded by a switch or a variable, adds a layer without editing a
single existing command. `story.npc()` already takes `pages=` for exactly this,
and `talker()` builds a two-page event whose third page is free.

This is the workhorse. It means an existing character can acquire something new
to say **without losing what they said before** - a player who never trips the
condition sees today's game, byte for byte.

**3. A conditional branch appended to an existing command list.** Legal but
last-resort, because it edits a list somebody else wrote. Only where a page
cannot work - chiefly the ending, whose tally is one long command list and where
new `if_then` blocks before THE END take nothing away.

**Never:** change an existing line's text, change a character's face, delete an
event, or renumber anything. If a joke seems to need one of those, it is the
wrong joke and pattern 1 will produce a better one.

**One sanctioned exception, and it is a repair rather than a revision.** Where
the finished game contradicts *itself* - a character drawn as one thing and
rendered as another - fixing it is not re-voicing anybody, and the rule does not
protect it. There is exactly one such case and it is specified in 8.1. Any
further ones must be argued for in writing and listed there too; "it would be
better if" is not a contradiction.

## 2. The counters

### 2.1 What the existing ones actually do

Checked against the build rather than assumed, because the answer is not what
the variable names imply:

**Re-audited 2026-08-25** out of the built `data/` rather than the source -
every code-122 write, every code-111 branch, every page condition and every
`\V[n]` in a message. The first version of this table was wrong about two of
them, so the numbers below are the ones to trust:

| var | writes | branch | page cond. | printed | what it does today |
| --- | ---: | ---: | ---: | ---: | --- |
| 2 `VAR_TROPES` | 72 | 2 | - | 1 | The ending prints the number, then picks one of **three** closing paragraphs at 40 / 20 / below. |
| 4 `VAR_TALES` | 6 | - | **1** | 1 | A real gate: Hosea Bellwether's payout page needs `>= 6`. Was the only variable page-condition in the game until the Long Field. |
| 1 `VAR_COMPANIONS` | 18 | - | - | 1 | **Already printed in the ending** - "with `\V[1]` companions." |
| 3 `VAR_TURNIPS` | 1 | - | - | 1 | **Already printed in the ending** - "...and ate `\V[3]` turnips." |
| 5 `VAR_BOUNTIES` | 2 | - | - | - | **Write-only. The only genuinely dead one.** |
| 6 `VAR_PLAQUES` | 12 | - | **1** | - | **A real gate**, and the second variable page-condition in the game: Ott's clause-seven page needs `>= 12`. Twelve writes, one per plate, each behind its own self switch. The thirteenth plaque does not write to it. |
| 7 `VAR_BLUSHES` | 24 sites, **20 reachable** | - | - | - | Write-only until step 8 puts its line in the ending. Nine moments came with the north and eleven with the retrofit of section 3. Sites over-count moments for the reason at the end of 2.3, and 3.6 adds a second reason: the two travellers are one moment with two mouths, guarded by a global switch. |

So **one** of the five is write-only, not three. Do not add a counter to that
pile without giving it a job.

### 2.2 Cash the one dead one

**This section originally read "cash the three dead ones" and was wrong.** The
companions line and the turnip line are already in the ending and have been
since before the north - `git show HEAD:build/journey.py` has both. The turnip
joke is not a free win waiting to be taken; it has already been taken.

What is left is `VAR_BOUNTIES`, and it is one appended `if_then` on the ending's
tally (pattern 3 in 1.7 - nothing is removed).

### 2.3 The new one, and its job

    VAR_BLUSHES = 7    # "things nobody quite said"

Every Register A moment bumps it, once, on first sight. Bump it with
**`story.blush()` and nowhere else**, exactly as `VAR_TROPES` is handled, so the
tally can be audited by grep. `story.blush()` is a bare variable-add with no
message, so it can be appended to any command list without disturbing pacing.

Its job is **Piper's ballad** (3.3). Piper has been taking notes all game, and
the Prophecy Committee strikes the verses it cannot have read aloud at the fete.
So the ending prints, under the existing cliché line:

    Clichés walked into: 34
    Verses struck by the Committee: 11

...if the ballad happened, and the flatter `Things nobody quite said: 11` if it
did not. Same number, wearing a joke, and it retroactively explains why there
was ever a verse seven.

**This is the most important small feature in the document.** The joke only
exists **in aggregate** - which is exactly what keeps every individual instance
deniable, the entire design constraint solving itself. If the schedule collapses,
ship the counter and four blushes rather than twenty blushes and no counter.

**Count the sites, not the writes.** A moment written with `talker(..., pages=)`
lands in the data **twice** - once on the first-visit page and once on the
repeat page - and a grep of `data/` will therefore over-count it. Mrs
Tunnicliffe's census is the town's one example: two code-122 writes, both
guarded by `condition_switch(SW_CENSUS, False)`, one reachable moment. Guard
every appended blush the same way, and prove it the way `clanging_cast` does -
ask the same question a second time and assert the counter has not moved.

**Measured on the finished build, 2026-08-26: twenty-five.** Counted off
`data/` and then corrected, which is the only way to get it right - 28 code-122
writes to variable 7, less three known duplicates: the two travellers are one
joke with two mouths and one `SW_TRAVELLERS`; Mrs Tunnicliffe's census is the
first-visit page and the repeat page, both guarded on `SW_CENSUS` being false;
and Bryd's spar page holds a with-Hob branch and a without-Hob branch that
cannot both run. Nineteen events carry one, and six of the twenty-five are
Ott's.

The total was **20** when the ending's threshold was cut at 16 - the town's
nine (4.6) and the retrofit's eleven (3) - and it has grown since by Ott's
three flying-chain beats and by Bessie and Gudgeon, neither of whom existed
when 4.6 was written. **The threshold moved to 20 to match**, because four
fifths is what "very nearly all of them" was ever supposed to mean and 16 out
of 25 congratulates a player who missed nine. Anything appended to this counter
later has to move it again; that instruction is in the comment above the branch
in `journey.py`, where whoever adds the twenty-sixth will actually be standing.

---

## 3. Part one: the retrofit

Register A, threaded back through the finished game. **Every item here is an
addition** under 1.7 - a new event, or a page appended to an existing one. No
existing line changes. Each bumps `VAR_BLUSHES` once, on first sight.

Order of implementation: build the north first. These read far better written by
somebody who already has Ott's voice in their ear, and several of them are
guarded by switches the north sets.

### 3.1 The Slain Wyvern (Map 14) - room four

**New event.** A door, or the stairs, or Dorcas's board - something new to click
on near the bar. Dorcas is *delighted*; she is not being arch.

    Dorcas: Room four's not been down since Tuesday.
    Dorcas: Best guests I've ever had.
            No trouble, no noise to speak of.
    Dorcas: I leave the tray on the mat.
            Lovely to see young people happy.

Sets `SW_ROOM_FOUR`, which two later additions read.

### 3.2 The Slain Wyvern - the ledger, and Sops

**New prop.** The register, on the bar, with a column headed **PURPOSE OF
VISIT**. Forty entries. Thirty-nine say "business." One says something else,
neatly crossed out in a different hand, with "business" written above it.

**Appended page on Sops** (event 17), conditioned on `SW_ROOM_FOUR`. `talker()`
gives him two pages; this is his third, and MZ will prefer it once the switch is
on. His existing lines stay exactly where they are and a player who never finds
room four never sees this.

    Sops: The Forty-Second and his wife are in.
          They come every year for the anniversary.
    Sops: They're SIXTY.
    Sops: Mrs Thrupp says good for them, and I
          said good for what, and got a bun.

Note the shape: the child asks the correct question, is answered with pastry, and
is entirely satisfied. **Never let Sops work it out.**

### 3.3 Prophecy Hall (Map 3) - verse seven

**New event: the minutes of the Fete Sub-Committee**, a readable board on the
wall. Nobody's dialogue is touched; the joke is a document, which is the most
Thistlewick delivery available and fits 1.3's fourth mechanism exactly.

Gated on Piper being recruited (`SW_RECRUIT[PIPER]`). Sets `SW_BALLAD_DONE`,
which the ending reads (2.3).

    Verses one to six: approved.
    Verse seven: struck.
    Verse eight: struck, and we would like a word.
    Verse nine was read aloud at the fete. In error.
    By Mrs Wispel.
    There were children present. There were
    GRANDPARENTS present.

And **an appended page on Piper**, or a new event beside the board if Piper is
not in the party:

    Piper: It scans.
    Piper: That is all I will say for it. It scans,
           and it is true, and if they wanted a
           different verse they should have asked
           for a different verse.

**The content of verse seven is never given.** Not in dialogue, not in a prop,
not in the ending. It only ever accrues consequences. Anyone who writes verse
seven down has misunderstood the assignment.

### 3.4 Wren, on the road

**New props** in existing dungeons - a nest, a shed skin, a carcass - each with a
page conditioned on Wren being in the party, exactly as the wyvern event already
checks party membership. Clinical, correct, relentless, never once aware.

    Wren: The crest isn't for fighting.
          It's a display structure.
    Wren: It is for attracting a mate. It works.
          That is why there are nine of them.

    Wren: That one is gravid.
    Bram: Is that bad?
    Wren: It is the single most normal thing
          in this cave.

    Wren: Everything we have killed this week
          was in the middle of courting.
    Wren: I don't say that to upset you.
          I say it because it goes in the monograph.

### 3.5 Merribell, being a professional

**New event**, best placed at an inn or after a set-piece. She has no
embarrassment reflex, because medics do not. Pitch her as *kind* and Bram as
unable to cope.

    Merribell: Where does it hurt? Be specific.
               "Down there" is four separate systems
               and I will guess wrong.
    Bram: It's my ankle.
    Merribell: Then say ankle! Oh, thank goodness.

### 3.6 The Two Very Ordinary Travellers (Map 14, events 15-16)

The first draft rewrote these two from "royalty in disguise" to "newlyweds."
**That is not allowed and the additive version is better:** they are royalty in
disguise *and* newlyweds, and the second only surfaces on a later visit.

**Appended page on each**, conditioned on `SW_ROOM_FOUR`. Every existing line -
the peasant crowns, the small farm, the beans - stays exactly as it is and is
still what a first-time player meets.

    Traveller: We are peasants, and we are
               unacquainted.
    Also A Traveller: We met on the road.
    Traveller: Yesterday.
    Also A Traveller: Yesterday.
    (They are holding hands. They have been holding
     hands the entire time.)

Keep the beans. The beans are load-bearing.

### 3.7 Perpetua Small (Map 14, event 10)

**Appended page on Dorcas**, conditioned on Perpetua's tale having been heard,
using the ceiling-staring machinery already built into that room:

    Dorcas: There was a Gerald.
    Dorcas: We handled it.
    Dorcas: That is all that is being said
            about Gerald.

### 3.8 The Standing Stones (Map 8, event 13)

The first draft added a seventh line to the plaque. **Do not edit the plaque.**
Put a **second, newer, smaller notice** next to it - the parish correcting its
own sign, which is funnier than the sign being longer:

    THEORY SEVEN HAS BEEN REMOVED AT THE
    REQUEST OF THE PARISH AND THE FAMILY.

This also does useful work: the stones are the turn onto the west road (4.3), so
a second sign there is the last thing a player reads before the town of people
who will not accept the obvious explanation.

---

## 4. Upper Clanging

### 4.1 The thesis

The third answer to the Prophecy, and the only cheerful one.

| town | answer | comedy |
| --- | --- | --- |
| Thistlewick | believe it | rural bureaucracy |
| Nether Sopping | be discarded by it | the adventuring industry |
| **Upper Clanging** | **solve it** | **engineering optimism** |

Faith, cynicism, and then a woman with a slide rule who has looked at a
four-thousand-year-old curse and seen a load case. The north is the funniest of
the three and also the most likeable, and it must never be played as stupid.
Ott Hoyle is not a fool. She is running an experiment.

### 4.2 The name and the sign

**UPPER CLANGING.** Upper/Nether is a real English toponymic pair - Nether
Wallop and Over Wallop are two actual villages in Hampshire - so it reads as a
deliberate sibling to Nether Sopping rather than as a second unrelated joke.

The sign, in the established format (`NETHER SOPPING - 'THE SEA IS RIGHT THERE'`):

    UPPER CLANGING
    'IT WILL BE QUIETER SOON'

### 4.3 Where it goes on Map 8

Map 8 is 50x50, tileset 1. The island's north tip is currently around y=5 and
the **entire north-west quadrant (x < 9, y < 18) is open sea.** The south-east
bulge precedent from `wilds.py` applies: grow the continent.

* **Grow a north-west lobe**, roughly x 3-13, y 6-18, following the existing
  coastline diagonal.
* **Upper Clanging** at **(9, 12)**.
* **The Long Field** at **(12, 15)** - walkable, its own map.
* **The wreck crag** at **(6, 8)** - walkable, its own map.
* **A west road**: leaves the existing north road near the Gloamwood north mouth
  (17, 20), runs west past **the Standing Stones (11, 18)**, then north to the
  town.

The Standing Stones being the turn is not an accident and should be leaned on.
Six competing theories on a plaque, the sixth from a man who was standing there
when they went up and is being ignored on principle - that is the northern
temperament in miniature, and it is the last thing you pass before the town of
people who will not accept the obvious explanation. Put the parish's correction
notice beside it - see 3.8, and note that it is a *second sign*, not an edit to
the first.

A junction signpost at (14, 19):

    UPPER CLANGING .......... 9 miles
    THE OBLIGATORY TOWER .... 14 miles
    (The second figure has been crossed out and
     rewritten four times, in four hands, each
     more confident than the last.)

### 4.4 The look

Not brass-and-goggles steampunk - the assets do not have brass, cogs or
goggles, and it would be the wrong register anyway. **Soot, brick and rust,
under a permanent chimney haze.** Rain would sell it and is free.

Tileset **5, "SF Outside"**, which already exists in `Tilesets.json` and whose
A1/A2 are the *ordinary* Outside water and grass - so an industrial town sits on
the same earth as the rest of the world, which is exactly right.

**Use:** Wall O (Brick), Wall G (Metal, Red Rust), Wall H (Metal, Patina), Walls
K/L/M (Factory), Walls I/J (Barracks), Wall T/U (Wood, Dirty); Chimney A/B/C on
every roofline; Small Fuel Tank, Air Vent A/B, Vent, Machine A/B/C, Machine
Device, Large Machine, Sphere Machinery, Pillar C (Machine), Broken Pillar C;
Iron Fence A/B, Metal Fence; Crate, Stacked Crates, Barrel; the **Clock Tower**
as the one civic building; Waste Land and Metal Floor A (Factory) for the yard.

**Never place:** the Neon Shop Signs, Traffic Lights (Car/Pedestrian), Vending
Machine, asphalt and white lines, or the tile helpfully labelled "Tank" (戦車 -
it is a literal military tank). Interiors likewise: use Pipe (H)/(V), Control
Panel A/B/C, Machine A/B/C, Broken Machine; avoid Server Machine, Monitor A/B,
Large Monitor and the ECG Monitor.

The whole SF set skews cyberpunk in about a third of its tiles. The rule is:
**anything that implies electricity is out; anything that implies pressure is
in.**

### 4.5 The maps

| id | map | what |
| --- | --- | --- |
| 21 | **Upper Clanging** | one long street on a slope, chimneys, the Clock Tower, the sign, four doors |
| 22 | **The Hoyle Works** | the shed, the drawing office, and the Two Hundred |
| 23 | **The Safety Valve** | the inn. Framed on the wall: THINGS THAT ARE NOT TO HAPPEN AGAIN, numbered to sixty-three, most entries redacted to a single word. Number 61 is just "OLLERENSHAW." |
| 24 | **Ollerenshaw's** | the forge. Bryd, and the spar. |
| 25 | **The Parish Rooms** | Mrs Tunnicliffe, the register, the census, the shop counter |
| 26 | **The Long Field** | one hundred and ninety-nine wrecks, in rows, with plaques |
| 27 | **The Wreck of the One Hundred and Ninety-Ninth** | a crag, a dungeon, and ITEM 1 |

Deliberately no bounty board and no guild. The north's institutions are a works
and a parish register, and repeating Nether Sopping's shape would be the worst
thing this expansion could do.

The **shop** lives in the Parish Rooms because in a town this size the registrar
also sells things, which is both true to life and one fewer door. It sells
industrial goods: oilskins, a wrench, a lamp, ship's biscuit's northern
equivalent, and **Sensible Trousers** (high DEF, low everything else, and a
description that is a small essay about how nobody in this game is dressed for
the weather).

### 4.6 The cast

#### How to read a face reference

Two numbering schemes are in play and they are off by one from each other:

* **`story.py`'s `FACES`, and MZ's `faceIndex`, are 0-based.** A sheet is a 4x2
  grid of 144px cells, read left to right, top row then bottom: indices 0-7.
* **`img/pictures/` holds MZ's pre-split single faces and they are 1-based.**
  `People2_8.png` is face **index 7**.

So `("People2", 7)` in code is the file `img/pictures/People2_8.png` on disk.
**Every reference in this document gives the filename**, because that is the one
a human can actually look at. The code index is always the number in the
filename minus one.

#### What is left

The People sheets are **exhausted**: People1, People2 and People4 are fully
allocated and People3 has exactly one free cell (`People3_3.png`). That is not a
warning, it is the reason the north is drawn from the SF sheets, and it is why
`SF_People1` and `SF_Actor1-3` - thirty-two faces, none used - matter.

Doubling up is established practice here and is fine when the two are far apart
in a player's memory: the game already shares `People1_5` (Fisher / Ferryman),
`People3_5` (Bother / Ambrose - with a written justification in `story.py`),
`People4_5` (Old Man / Halbert Quy) and `People2_8` (Apprentice / Crooke -
which becomes Apprentice / Ott, see 8.1).

#### The northern cast

| who | file | code | what they look like |
| --- | --- | --- | --- |
| **Ottoline "Ott" Hoyle** | `People2_8.png` | `("People2", 7)` | **brass goggles pushed up on her head**, pink-plum hair, fur-trimmed shoulder, green amulet. The only steampunk face in the entire stock library. |
| **Mrs Tunnicliffe**, registrar | `SF_People1_8.png` | `("SF_People1", 7)` | white hair, spectacles, green scarf, cardigan. A gift of a face for a woman who keeps a register. |
| **Mrs Cotterill** | `SF_People1_6.png` | `("SF_People1", 5)` | dark green-black hair in a long side braid, mustard cardigan, entirely unbothered |
| **Mr Cotterill** | `SF_People1_5.png` | `("SF_People1", 4)` | moustache, weathered, olive work jacket |
| **Spare Cotterill**, aged 9 | `SF_People1_1.png` | `("SF_People1", 0)` | dark-haired lad in a blue shirt |
| **Bryd Ollerenshaw**, smith | `SF_Actor3_1.png` | `("SF_Actor3", 0)` | broad, square-jawed, dark hair, thick neck. The only face in the SF sets with the mass to stand next to Hob. |
| **Old Sowerby**, sixty years at the works | `SF_People1_7.png` | `("SF_People1", 6)` | old man, olive knit cap, white beard, tan coat |
| **Nib**, Ott's apprentice, the fortieth | `SF_People1_2.png` | `("SF_People1", 1)` | young, brown ponytail, red cardigan. The one doing the face. **She**, which the game establishes once and only in Ott's mouth - "I have told her nine times that it is not a question with an answer" - so do not write the line that says it again. |
| **Mr Kell**, the Safety Valve | `SF_People1_3.png` | `("SF_People1", 2)` | young man, black hair, blue jacket |
| **Winnie Marsden**, Cold Winter cohort | `People1_8.png` | `("People1", 7)` | **grey, and sixty, and certain.** Insufferable about the dinner. **Recast after this table was written.** She was `SF_People1_4.png`, a strawberry-blonde of about twenty-five, and Mrs Tunnicliffe - white-haired - was **born in June of the same year**. Class of 'Nineteen is sixty years back and all two hundred and forty of them are pensioners, which is the funnier reading and the one the census actually says. Nothing Winnie says implies youth, so it is a recast and not a re-voicing: not a line was touched. There are exactly two old women in the whole face library and both were spoken for, so she shares Ysolde's on the Halbert Quy precedent - Nether Sopping is forty miles and an act away. |

Everything above was looked at this session, not inferred from a filename. Still
confirm in a rendered screenshot before committing, per house rules.

#### The rest of the Cotterills

Appended after the table above, and the reason Winnie had to move: nine children
over fifteen years and then nine years of nothing, which is why the name list ran
out, why the ninth is called Spare, and why the tenth in the spring is a
surprise. Seven of them are placed around the town; **Cotter**, the eldest, is
down the valley at the big foundry and is represented here by his wife.

| who | file | code | where | what they look like, and what they are doing |
| --- | --- | --- | --- | --- |
| **Bessie Marsden**, Cotterill now | `SF_People1_4.png` | `("SF_People1", 3)` | Map 21 (5, 40) | Winnie's face, forty years earlier, because Bessie is **Winnie's granddaughter** and the resemblance is meant. Winnie's move off this cell freed exactly the face this wanted. She does four jobs in one event: she is where Cotter is, she is the Marsden marriage, and she is the reason Winnie has an opinion about the seating. |
| **Rivet**, 22 | `SF_Actor1_1.png` | `("SF_Actor1", 0)` | Map 23 (8, 10) | brown hair, plain white work jacket, unmistakably a young man. Day shift; Da's shadow. **He was drafted onto `SF_Actor2_3.png`** - maroon hair and a soft blue shirt, which reads as a girl at both sizes, and that makes "I have shared a bed my whole life and one of them is Grommet" a different line entirely. He is also the only one of the nine indoors at the Safety Valve with Mr Kell, who is black hair and a blue jacket, so brown-and-white is the legible choice twice over. |
| **Gudgeon**, 20 | `SF_Actor1_8.png` | `("SF_Actor1", 7)` | Map 25 (11, 6) | braid and spectacles; clerks at the Parish Rooms. **She.** |
| **Tappet**, 18 | `SF_Actor2_4.png` | `("SF_Actor2", 3)` | Map 22 (14, 13) | blue cap; brings the castings up on Tuesdays and has watched that thing not fly for four years. **She**, and she would still get in it. |
| **Ferrule**, 16 | `SF_Actor1_2.png` | `("SF_Actor1", 1)` | Map 21 (11, 40) | long braid; in charge until six, when Da wakes up and she gets to sit down. |
| **Grommet**, 15 | `SF_Actor2_7.png` | `("SF_Actor2", 6)` | Map 24 (7, 11) | apprenticed to Bryd and put upon. **He.** |
| **Clevis**, 13 | `SF_Actor1_3.png` | `("SF_Actor1", 2)` | Map 21 (8, 41) | red spikes; running a book on the tenth one's name, which is the fastener gag handed to somebody who thinks it is a market. |
| **Shim**, 11 | `SF_Actor1_6.png` | `("SF_Actor1", 5)` | Map 21 (7, 41) | beret and spectacles, and a tin of washers, three bolts, a doorknob and a bearing. **She**, and the bearing is the best one. |

Four of the seven are off `SF_Actor1`, deliberately, so that they read as
related. **Neither Ferrule nor Clevis is ever given a pronoun** in the finished
text - every "he" and "she" in their two events is about Da or Mam - and that is
not something to tidy up: nothing in either scene needs one, and a line added to
supply one would be a line added to say something the scene was not saying.

#### Three casting decisions worth knowing the reasons for

**Ott gets the goggles, and Meredith Crooke is moved off them - as a repair.**
`People2_8.png` was shared by the Thistlewick smithy's Apprentice (a shop vendor
with one line) and Meredith Crooke. Crooke moves to `Actor3_2.png`, for a reason
that has nothing to do with Ott: **the finished game already contradicts itself
about her.** Her face is a woman and her battler is `Captain`, which is a man in
armour, so the person you talk to and the person you fight are visibly two
different people. That is the 1.7 exception, and it is specified in 8.1.

`Actor3_2.png` is a better Crooke than the goggles ever were - long braided
auburn hair, a purple scarf, pauldrons over a blue-and-white jacket, entirely
composed - and it reads as a woman who runs a training programme, which is what
she is. It also carries `img/enemies/Actor3_2.png` **and**
`img/sv_enemies/Actor3_2.png`, and this game is side-view (`optSideView: true`),
so the fight finally shows the person from the conversation.

That leaves `People2_8.png` shared by the Apprentice and Ott, which is one fewer
share than the game runs today. There is a quiet symmetry in it that should
**not** be pointed at: the Apprentice is an apprentice, and Ott has had "every
apprentice I have ever had."

**Mrs Tunnicliffe is a woman, and was drafted as a man.** Pell, Bother, Splint,
the Thistlewick clerk and Hosea are all men; the north's registrar was the
cheapest place to fix that, and `SF_People1_8.png` is a better face for the part
than anything else available.

**Bryd Ollerenshaw is a man**, and he and Hob Grumnir are a twenty-year slow
burn between two enormous blacksmiths. This is deliberate and it is written
under 1.2: **the game never says the thing.** Nobody announces anything, nobody
has a Moment, the two of them cannot finish a sentence in the same room, a child
says "they do this every time," and the payoff is that they go for a drink.
A child reads two grown-ups being strange at each other. An adult reads twenty
years. Anyone who writes a coming-out scene, a declaration, or a kiss has
misread the entire document - it is the same discipline as verse seven, applied
to a relationship instead of a joke.

**Ottoline Hoyle**, chief engineer, fourth generation. Deadpan, precise, and with
no capacity for embarrassment whatsoever. She has an opinion about Bram and
gives it immediately:

    Ott: Two hundred years I have been at this.
         Four generations of us.
    Ott: And they have sent a lad.
    Ott: No offence intended. Some given,
         I will grant you. But none intended.

### 4.7 The Register A payload

**Ott, and the vocabulary.** This is the cleanest joke in the whole document,
because **every one of these is a genuine steam-engineering term.** Nobody has
written a dirty line. Somebody has written a repair, accurately. If the
implementer is unsure of a term, look it up rather than inventing one - the
authenticity is the defence.

    Ott: She's blowing off at the drain cock,
         the gland has gone on the big end,
         and she primes if you heat her too fast.
    Ott: Otherwise she is sound.
    (Merribell nods along. Merribell is a field medic
     and this is a Tuesday.)
    (Bram has found something to look at.)

    Ott: Get on the stuffing box with the packing,
         and do not be shy with it.
    Bram: ...
    Ott: It is a box. You stuff it.
         That is what it is called.

    Ott: Nipples want doing every forty hours.
         There are thirty-one of them.
         You will want the small can.

    Ott: That is a male thread, that is a female,
         and they do not go together.
    Ott: I have had this conversation with every
         apprentice I have ever had and they
         all do the face.
    Ott: You are doing the face.

That last beat is deliberately built on Sops's "You're doing the standing again,"
so it lands as this game's joke rather than as an import. **Use the vocabulary
four times across the whole town, at intervals.** The moment it becomes The Bit,
it stops being a repair.

**The Cotterills.** Foundry family. Every child named after a fastener: Cotter,
Rivet, Gudgeon, Tappet, Ferrule, Grommet, Clevis, Shim, and **Spare**. They ran
out around the seventh.

    Bram: ...Are all of these yours?
    Mrs Cotterill: Nine. And one in the oven.
    Bram: Nine!
    Mrs Cotterill: Mr Cotterill does the night shift.
    Mrs Cotterill: He is always very glad to get home.

She is **proud**. She is not complaining and she is not confessing - she is
answering a polite question from a polite young man, and the joke is entirely in
Bram's face and the player's. On the naming:

    Mrs Cotterill: We had run out. He said "call it
                   Spare," and I was tired.

Then the double-tap, from Spare, unprompted, thirty seconds later:

    Spare: We are not to knock on Sunday mornings.
    Spare: Da says Sunday mornings is why
           there is ten of us.
    (Mrs Cotterill has gone the colour of the forge.)

And the sweetest one, which is the endearment version and should be the last
thing you get from that house:

    Spare: Da calls Mam "the Two Hundred."
    Bram: ...The airship?
    Spare: He says she is the one that is finally
           going to work.
    (Mr Cotterill has left the room.)

**A running gag, free of ids:** Spare, aged nine, wants to come with you. Asks
every time you enter the town. Is refused. Has a packed bag. Never becomes an
actor; the joke is entirely that he is nine and completely serious.

**Mrs Tunnicliffe and the register.** The accidental-record mechanism, and the
one to fight hardest for, because it is a *census entry* - the most innocent
object imaginable - and it does the whole job by itself.

    Tunnicliffe: Class of 'Nineteen. The Cold Winter lot.
    Tunnicliffe: Foundry was banked down six weeks that
                 January. No work. No heat in the whole
                 town but what was in the houses.
    Tunnicliffe: Two hundred and forty of them.
                 All born the same autumn, near enough.
    Tunnicliffe: They have a dinner every year.
                 I am not invited. I was born in June.

The punchline for a child is a woman being sulky about a dinner. The punchline
for an adult is the arithmetic. Nothing has been said.

**Hob and Bryd.** If Hob Grumnir is in the party, a twenty-year slow burn
resumes exactly where it left off, which is to say nowhere, in a very warm room,
in front of everybody. They were apprenticed together.

    Hob: ...Ollerenshaw.
    Bryd: ...Grumnir.
    (Neither of them says anything for a while.)
    (Somewhere behind you a child says "they do this
     every time" and is removed.)

The side-quest payoff must be **small and undramatic**: they go for a drink.
That is all. The town loses its mind. Hob currently has the least interiority of
the original six and this costs him none of his dignity - which is the test from
1.5, applied to the character who can least afford to fail it.

Sets `SW_HOB_BRYD`; the ending mentions it in one line and does not elaborate.

---

## 5. The Two Hundred

### 5.1 The quest

Ott needs three things, and the third is the point.

1. **Envelope fabric** - forty bolts of oilskin from **Mrs Barrow** in Nether
   Sopping. She has never sold forty of anything in her life and is
   *incandescent* with commercial joy. This deliberately ties the two expansions
   together and means the north cannot be finished before the south is open.
2. **A main spar that will not fracture** - forged at Ollerenshaw's. If Hob is
   in the party he does it himself and 4.7's scene fires. If not, Bryd does it
   and it takes a day, and you get a shorter version of the same scene.
3. **A pilot who has been to the tower and come back.**

The third is where the town stops being funny for a moment:

    Ott: Lift has never been the problem.
         I want you clear on that.
    Ott: We can get anything off the ground.
         We have had a shed off the ground.
    Ott: They come down. That is all they do.
         They come down in sight of the tower,
         and I have one variable left that I have
         never once been able to get hold of.
    Ott: And it walked into my works this morning
         and asked whether we had a gift shop.

She has considered the Prophecy. Privately. For years. She will not say so, and
she has designed the experiment anyway, and Bram is the missing part - which
inverts "they have sent a lad" and is the single best beat in the north.

### 5.2 The engine facts - read this before writing a line of it

Verified this session against `js/rmmz_objects.js` and the project data:

* **The airship already exists in `System.json`**: `characterName: "Vehicle"`,
  `characterIndex: 3`, currently parked at `startMapId: 1, (154, 70)`. That is
  dead default junk inherited from the blank project - map 1 is Thistlewick and
  is nowhere near 154 tiles wide. Set `startMapId: 0` so it is genuinely
  nowhere, and place it from an event when it is earned.
* **Placing it is event command 202**, "Set Vehicle Location", params
  `[vehicleIndex, mode, mapId, x, y]` with `vehicleIndex: 2` for the airship and
  `mode: 0` for direct designation. **`rmmzdata.py` has no helper for this** -
  add `set_vehicle_location(vehicle, map_id, x, y, indent=0)`.
* **Landing rule**:
  `Game_Map.isAirshipLandOk(x, y) = checkPassage(x, y, 0x0800) && checkPassage(x, y, 0x0f)`.
  `checkPassage` walks `layeredTiles` **top down (z3, z2, z1, z0)**, skips any
  tile flagged `0x10` ("[*] no effect on passage"), and **returns on the first
  tile it does not skip**. So the topmost non-star tile decides, and everything
  underneath it is irrelevant.
* Plain world grass (tile 2816, flags `0x0600`) **is** landable. Sea (tile 2048,
  flags `0x080f`) is not. Both correct and both free.
* **The joke does not work out of the box, and this is the most important line
  in this document.** The Tower Door tile (31, 8) carries a top-layer B-sheet
  tile, id 88, flags `0x0600` - which does *not* set `0x0800`, and which is
  consulted *before* the impassable 3915 beneath it. **As the data stands today
  the airship can land on the front step of the Obligatory Tower.** Setting
  `0x0800` on the tower's top tile in `Tilesets.json[1].flags` fixes it, and
  then the engine itself refuses, and clause seven and the collision map become
  the same sentence.

  **Correction, verified against the built data: flag tile 88 and stop there.**
  The rest of the original plan - "flag the tower approach tiles too" - cannot
  be done and does not need doing.

  * Tile 88 is used **exactly once in the whole 50x50 world map**, at (31, 8, 3),
    the tower door itself. Setting `0x0800` on it is surgical and costs nothing
    anywhere else.
  * The approach tiles are plain world grass (2816), which is *the* landable
    ground for the entire island. There is no way to flag them by tile id
    without making the whole world unlandable, and no way to flag them by
    position at all - `Tilesets.json` flags are per tile, not per square.
  * The road does not need flagging either - but **not for the reason this
    document gave**, and the reason it gave is wrong. Corrected 2026-08-25 out
    of the built map: the world road is autotile kind 29, and the shapes Map 8
    actually lays down are 3472-3485, all flagged `0x0600`. **The road beside
    the tower is airship-landable**, and tile 3008 is not road at all - it is
    the forest autotile, which is where `0xe40` came from.

    That costs the joke nothing, because the only square that matters is the
    door. A party that flies here can set down on the road at (31, 9) and walk
    one square, or on the grass at (30, 8) and walk two. Either way they arrive
    at the door on foot, which is what clause seven says.

  So the airship sets down on the grass a couple of squares from the door and
  the party walks in, which is the joke exactly as specified. The only edit is
  one number.

### 5.3 The handover

The airship arrives **when the map is finished**, which is the joke, and the
game says so out loud:

    Ott: She is yours. Where will you take her first?
    Bram: ...I have been everywhere.
    Ott: Ah. Yes.
    Ott: I am told that is traditional.
         I did ask.

Bump `story.trope()`. Then let the engine deliver the real punchline unassisted:
it will fly the party over the Obligatory Tower all day and set them down beside
it, on the grass, **on foot**, exactly as clause seven specifies. Two hundred
years of engineering and one sentence of a contract arrive at the same result,
and the machine works perfectly.

### 5.4 The log entry

In the works, afterwards, readable:

    ATTEMPT 200. REACHED THE TOWER.
    LANDED ADJACENT.
    CAUSE: UNDER REVIEW.

The same three words as 199. She still will not write it down. That is the whole
town in one plaque and it should be the last thing you can read in the north.

### 5.5 The plaques, and clause seven

The Long Field (Map 26): one hundred and ninety-nine wrecks in rows, twelve of
them with readable plaques. Every cause is mechanical, specific and plausible.
Not one says "the Prophecy."

    ATTEMPT 137. LOST OVER THE GLOAMWOOD.
    CAUSE: FRACTURE, MAIN SPAR.

    ATTEMPT 138. LOST OVER THE GLOAMWOOD.
    CAUSE: FRACTURE, MAIN SPAR (DIFFERENT SPAR).

    ATTEMPT 199. LOST IN SIGHT OF THE TOWER.
    CAUSE: UNDER REVIEW.
    (This plaque has said UNDER REVIEW for eleven years.)

Count them in `VAR_PLAQUES`. **The reward for all twelve is not gold** - Hosea
already does gold-for-collectibles and repeating it would be lazy. Read all
twelve and Ott stops working:

    Ott: Twelve of them you have read.
    Ott: Go on, then. Ask me.

She shows you the works' log with **clause seven** annotated in four
generations of handwriting, and sets `SW_CLAUSE_SEVEN`, which changes a line in
the finale - the exact parallel to `SW_MET_QUY`.

And the Register B beat, which under 1.6 must be **warm**, not bitter:

    Ott: Great-grandmother started it to stop
         the Dark Lord.
    Ott: Grandmother kept it on because the town
         needed the work.
    Ott: Mother kept it on out of spite.
    Ott: I keep it on because I like it.
         I would rather be honest with you.
    Ott: Two hundred years, and we have arrived at
         "I like it," and I think that is fine.

---

### 5.6 What the airship is actually for

Two separate jokes live on this airship and they must not be confused.

The **timing** joke - you are handed it once the map is already walked - is free.
It needs no flags, no code and no engine cooperation, only that the quest ends
where it ends. The **clause seven** joke in 5.2 is a different, optional joke
about the Prophecy out-cheating two hundred years of engineering, and *that* is
the one needing a tileset flag. Nothing breaks if it is cut: the tower door is a
transfer event, the Barrow and the Guild are gated by items rather than terrain,
and there is no sequence in this game that an airship can break.

But an airship that only revisits places you have already been is a fast-travel
toy, and the north deserves better than that. **Put things in the sea and on top
of things.** These should be the last three jokes in the game a player finds,
and none of them is reachable on foot.

**The Isle of Uncertain Ownership.** A rock in the sea between Thistlewick and
Nether Sopping. Both have claimed it for two hundred years. It carries a
flagpole with two flags on it, one above the other, and the order has been
reversed nine times by parties who could not get ashore and were shouting from
boats. A plaque reads THIS ISLAND IS THE PROPERTY OF and then a great deal of
scratching out.

On it, one sheep. Belonging to nobody, and therefore never once sheared, and now
roughly spherical. The sheep is the joke: two parish councils, two hundred years
of correspondence, and a sheep that has done extremely well out of the dispute.

**Attempt 112.** Not in the Long Field, because it came down on a sea stack and
nobody could get to it. Its plaque was never written, and it is the only gap in
a hundred and ninety-nine. Bring its number-plate back and Ott writes the
thirteenth plaque, and it is the only one in the field whose cause reads simply
LOST. She would rather have an unwritten plaque than a wrong one, which is the
most engineer thing about her.

**The Hermit's middle distance.** Fly to the thing he has been gazing at
meaningfully for thirty years. It is a hill. An ordinary hill of no distinction
whatever, with a good view of the sea.

There is a bench on it.

It is not the Forty-Fourth's bench - that one is on the mound in the east, if
the player put it there. This one is older, weathered, has no plaque, was put up
by nobody anybody remembers, and faces the same water. Sit on it. Nothing
happens. That is the entire event, and it should be the last thing in the game
the player finds.

If `SW_BENCH_DONE` is set, allow one extra line of narration. One.

**Implementation notes.** Each of these wants its top tile airship-landable
(`0x0800` clear) with impassable water around it, so the airship is the only way
in - and `validate.py`'s flood fill should be extended to *assert* they are
unreachable on foot, because an air-only joke that turns out to be walkable is a
joke nobody will ever notice was one.

## 6. Attempt Eighty-Four

The north's optional boss, and a deliberate structural rhyme with the Barrow of
the Forty-Fourth - in a different key, which is the point of writing it at all.

In the Long Field, a machine that has been slowly repairing itself for a hundred
and forty years out of parts taken from its neighbours. It still has pressure.
It is still, faintly, trying to go north.

The difference from the Forty-Fourth is the whole reason it exists: **Ambrose
Fitch could ask for what he wanted. Eighty-Four cannot.** It can only keep
trying. So the payoff is not a bench and it is not a conversation. You stop it,
and it stops, and Ott comes out and looks at it for a long time.

    Ott: She got further than any of them.
    Ott: Nobody has ever been able to work out
         how she was still doing it.
    Ott: I have not tried very hard.

And then the ending line - `Attempt two hundred and one: begun` - is
**Eighty-Four, rebuilt**, if `SW_84_REBUILT` is set. That is worth the whole
subplot on its own.

Hardest fight in the north, entirely optional, comparable to the Forty-Fourth.
Run `balance.py` before committing a stat.

---

## 7. ITEM 1

Attempt 199 came down eleven years ago and is on a crag (Map 27). Everything
aboard is intact. Every system sound. She came down because she **stopped
flying**, in sight of the tower, and started again about four hundred feet
lower, and the crew walked home, and none of them will discuss it.

Still aboard is the thing they meant to drop on the tower. On the works
inventory since 1802 it is **ITEM 1**, and nobody has ever ticked it off.

Recovering it is the dungeon. Ott renders it down into the north's best gear -
one weapon and one accessory - and is visibly relieved to have it out of a
field.

**Stretch goal, flag it and cut it first if the schedule bites:** keep ITEM 1
intact instead, carry it to the throne room, and use it on Grimspite. The
Prophecy has a clause about that too. It produces the funniest failure in the
game, counts as a trope, and Grimspite is **genuinely delighted** - it is the
first new thing in four thousand years and he says so.

**Built 2026-08-25.** Map 27 is in, the stores ledger is in, and Ott renders
ITEM 1 down on a page appended to her. She only takes it **when you talk to
her**, which is what left the crate available to be carried anywhere else.

**The stretch goal was built 2026-08-26, and it is a page on the Grimspite
event guarded by `itemValid` on Item 32**, exactly as this section guessed it
would have to be. Three things about how it went in that are worth knowing
before touching it again:

* A page **replaces** page 1 rather than adding to it, so the crate page has
  to contain the whole finale. It is not written twice. `finale_event` records
  `split = len(c)` after the battle sting, and the page is built as
  `c[:split] + item_one_scene() + c[split:]` - one list, spliced. The existing
  finale rebuilds command for command; the only change to page 1 anywhere is
  the new ending paragraph, which is an ordinary appended `if_then`.
* The splice point is **after** `Shock2` and **before** `R.battle`, and that is
  the only placement that works. He has just said he has heard all of them;
  four windows later he says this one is new. Put the crate down before the
  line and he is a liar.
* It is **offered, not triggered**. `["Draw your weapon", "Set the crate
  down"]`, weapon first so a confirm pressed out of habit keeps the crate. A
  player can reach the summit carrying it on the way to Ott - the ledger sends
  you to the crag, not to the tower - and a page that lit it unasked would cost
  them Weapon 33 and Armor 25 without ever putting the question.

`SW_ITEM_ONE_USED` (71) carries it to the ending, which prints the stores book
line ruled through at last. `build/scenarios/item_one_throne.json` runs both
branches.

---

## 8. Additions to what already exists

Everything in this section is an addition under 1.7 except 8.1, which is a
repair, and the two tileset/system flags, which are noted as edits.

### 8.1 The Meredith Crooke repair - **DONE, do not redo**

The one sanctioned exception in 1.7, and the only part of this document that has
been built. Applied on 2026-08-24, rebuilt, and `validate.py` clean. It is
recorded here because it explains why 4.6 reads as it does, not because anything
is outstanding.

Crooke's face is `People2_8.png`, a woman. Her `battlerName` is `Captain`, which
is a man in armour. The player talks to one person and fights another.

    build/story.py:71   "Crooke": ("People2", 7)   ->  ("Actor3", 1)
    build/db.py:1638    EN_CROOKE, ..., "Captain"  ->  "Actor3_2"

Verified before proposing:

* `Actor3` index 1 is **unused** - the sheet carries only Nix (4) and Aldric (6).
* `Actor3_2` is **unused** as a battler; no enemy in the game uses any `Actor*`
  battler today, and `Captain` has exactly one user, which is Crooke.
* Both `img/enemies/Actor3_2.png` and `img/sv_enemies/Actor3_2.png` exist, and
  `System.json` has `optSideView: true`, so the side-view sheet is the one that
  renders. The battler and the face are the same character: braided auburn hair,
  blue cape, pauldrons.
* Crooke's world-map event builds its image as `R.image("")` - she has no
  walking sprite to keep in step. Nothing else to change.

Not one word she says is touched. Confirmed after the rebuild: her camp event
now draws `("Actor3", 1)` on all five of her speaking windows, `Enemies.json`
carries `battlerName: "Actor3_2"`, and `validate.py` reports no problems.

The only files that moved were `build/story.py`, `build/db.py`, and the two
generated files that follow from them (`data/Enemies.json`, `data/Map008.json`).

### 8.1a The state of the tree at handoff

**Updated 2026-08-25, after step 5 of section 16.** Everything is uncommitted
and deliberately so. A fresh session's first move is still the same - `python3
build/build_game.py && python3 ../tools/validate.py .` - and it should rebuild
clean with no diff beyond the files listed here.

In `thistlewick/` (its own repo):

| file | why |
| --- | --- |
| `build/story.py` | the Crooke face (8.1), `blush()` (2.3), and the ten northern faces (4.6) |
| `build/db.py` | the Crooke battler (8.1), switches 47-67 / variables 6-7, and the Parish Rooms counter: Items 13-15, Weapon 32, Armors 23-24 |
| `build/build_game.py` | those switch and variable names into `System.json`; airship `startMapId: 0` |
| `build/south.py` | `talker(..., pages=)`, additive, defaulting to nothing |
| `build/mapkit.py` | the SF vocabulary, `tile_names()`, `SF_FORBIDDEN`, `Canvas(tileset=)`, `Canvas.clock_tower()`; and the SF **Inside** furniture, `sf_grid()`, and an inside forbidden list grown from 11 names to 191 tiles |
| `build/sampler.py` | eight SF modes: `sf_walls`, `sf_yard`, `sf_ground`, `sf_props`, `sf_fronts`, and `sf_inside` / `sf_parlour` / `sf_floors` / `sf_in_walls` for the interiors |
| `data/Enemies.json` | generated - Crooke's battler |
| `data/System.json` | generated - the airship, and the new switch/variable names |
| `build/places.py` | map ids 21-27, the northern world coordinates, `CLANGING_GATE` |
| `build/field.py` | **new** - the five `north_*` hooks (step 2), the town's destination event (step 3), and 5.6's three rocks plus the Clause Seven parallel (step 5) |
| `build/journey.py` | the five calls to them, `REG_CLANG` on the three northern encounter troops, and `<noairship>` on the Tower Door event - a note `validate.py` reads, and not a line of anybody's dialogue |
| `build/north.py` | **new** - Maps 21-25 (step 3), furnished and cast (step 4); Ott's four appended pages, the chalk line, the attempt log's second page and Bryd's spar (step 5) |
| `build/scenarios/north_road.json` | **new** - the west road, walked |
| `build/scenarios/reachable_clanging.json` | **new** - the town, walked |
| `build/scenarios/clanging_cast.json` | **new** - the dialogue, and `VAR_BLUSHES` asserted after every beat of it |
| `build/scenarios/clanging_faces.json` | **new** - the ten new faces, asserted off the live message window and screenshotted |
| `build/scenarios/two_hundred.json` | **new** - the whole quest end to end, Hobless |
| `build/scenarios/hob_and_bryd.json` | **new** - the same spar with Hob along, and the drink |
| `build/scenarios/airship_lands.json` | **new** - the one that protects the joke: it flies over the tower door and presses the button |
| `data/Map008.json` | generated - Crooke's face, the whole north-west, and the town's door |
| `data/Map021.json` - `data/Map025.json` | **new** - generated |
| `data/MapInfos.json` | generated - the five new maps |
| `data/Map016.json` | generated - Mrs Barrow's appended page, and nothing else in Nether Sopping |
| `data/Tilesets.json` | generated **for the first time** - `build_tilesets()`, and the diff is one number: tile 88 of tileset 1, `0x600` to `0xe00` |
| `data/Items.json`, `data/Weapons.json`, `data/Armors.json` | generated - the counter's stock, appended; no existing record moves |
| `CLAUDE.md` | a pointer to this file; `field.py`, `north.py`; the four new scenarios; switches 47-67 and variables 6-7 |
| `NORTH.md` | this file, still untracked |

In the workspace repo (one level up):

| file | why |
| --- | --- |
| `tools/rmmzdata.py` | `set_vehicle_location()`, `set_weather()` |
| `TILES-AND-ASSETS.md` | the SF tilesets, the `.txt` name tables, the SF fronts and SF Inside, the star-flag drawing order; and SF Inside's walls, floors and furniture, all looked at |
| `CLAUDE.md` | the note about turning encounters off in a walking scenario; never piping a scenario through `tail`; the orphaned-Chromium leak; the labelled contact sheet for judging prop tiles; and why `{"advance"}` must not be used on a choice that opens a shop |

**The other eighteen maps still rebuild byte-identical.** Map 8 and Map 16 are
the only *existing* generated maps that move, and Map 16 moves by one appended
page on Mrs Barrow, which is the check that matters: every
tooling change is inert for content that was already there. The three database
files that now move do so by having empty slots filled in - Items 13-15 were
already blank records, and Weapon 32 and Armors 23-24 are appended - so no id
in the finished game has changed meaning.

Upper Clanging is furnished and cast, and the Two Hundred flies. Nothing in
sections 3, 6 or 7 is built: no Long Field, no Attempt Eighty-Four, no crag, no
retrofit, and 5.5's plaques wait for the field they are in. Section 5 turned
out to need one thing this table did not predict - the ask could not be a page
on Ott, for the reason written up in 16 step 5 - and nothing else in step 4 was
edited to make room for any of it.

### 8.2 Everything else

* **Map 8 (world)**: the north-west lobe, the west road, the Standing Stones
  junction and signpost, three new destination events (town, Long Field, crag),
  and the northern encounter region. Owned by a new module, called from
  `journey.py` the way `wilds.py` already is.
* **Tilesets.json[1].flags** *(edit, not addition)*: `0x0800` on the tower tile
  and its approach. See 5.2 and 5.6. Nothing breaks without it - it buys the
  clause-seven joke and nothing else, so it is the first thing to cut if it
  causes trouble. It changes no dialogue and no behaviour a player has seen.
* **System.json** *(edit, not addition)*: `airship.startMapId` to 0. This is
  cleaning dead default junk inherited from the blank project, not changing
  anything the game has ever done. `airship.bgm` is already `Ship3` and is fine.
* **Map 16 (Wick & Barrow)**: forty bolts of oilskin, on a new page appended to
  Mrs Barrow, guarded by `SW_OILSKIN_ASKED`. Her existing shop and lines are
  untouched; a player who never goes north never sees the largest order of her
  life.
* **Map 3 (Prophecy Hall)**: verse seven and the fete - a new noticeboard event
  plus an appended page on Piper. See 3.3.
* **Map 14 (Slain Wyvern)**: room four (new event), the ledger (new prop),
  Sops's third page, an appended page on each of the two travellers, and Gerald
  on an appended page of Dorcas's. See 3.1, 3.2, 3.6, 3.7. **No existing line in
  that room changes.**
* **Map 12 (the finale)**: Grimspite answers clause seven if `SW_CLAUSE_SEVEN`.
  This is the north's payoff and it should be written last, when the town's
  voice is established. The shape of it:

      Grimspite: Clause seven. On foot.
      Grimspite: Do you know why?
      Grimspite: Because a thing that flies over and
                 drops something is not a story.
                 It is a Tuesday.
      Grimspite: She will never get one off the ground
                 in sight of this place, and it has
                 nothing whatever to do with her spars.

  And then the kind turn, because he is not cruel:

      Grimspite: Tell her the work was good.
      Grimspite: Four thousand years, and she is the
                 only one who ever came at me with a
                 question about materials.

  He is wrong, of course, and neither of them will ever find out: the Two
  Hundred *did* get there, because it had a Chosen One aboard, which means Ott
  succeeded by accidentally putting a story on her airship. Her log says UNDER
  REVIEW. **Do not have anybody in the game notice this.** It is for the player.
* **The ending tally** *(pattern 3: appended branches, nothing removed)*: the
  blush/verses line (2.3), the three dead counters finally cashed (2.2), whether
  the Two Hundred flew, whether Eighty-Four was rebuilt, and whether Hob and
  Bryd went for a drink.
* **`story.py`**: add `blush()`; extend `FACES` with the SF cast.
* **`mapkit.py`**: **extend, do not fork.** Add an SF tile-vocabulary section to
  the existing file so `Canvas.building()` footprint protection is inherited for
  free. Forking mapkit is exactly how you lose the guarantee that found seven
  scenery-on-roof mistakes in Nether Sopping. Add the northern wall-mounted
  props (Air Vent A/B, Vent, Machine Device) to `WALL_MOUNTED`.

---

## 9. Ids

The original decade blocks have run out in three places. The rule from here on
is stated per type; append, never renumber.

| range | what |
| --- | --- |
| Actors / Classes | **none.** Ten is already more than a four-slot party can use, and the north's contribution is a vehicle and a town, not another body. Ott stays an NPC. |
| Skills 140-149 | northern enemy and boss skills (137-139 left as a gap) |
| Items 13-19 | northern consumables |
| **Items 30-36** | northern key items. **The 20-29 key-item block is full** (max item id is 29); key items continue at 30. **30** Forty Bolts of Oilskin, **31** Number-Plate 112, **32** ITEM 1; 33-36 free. |
| Weapons 32-36 | northern weapons. **32** Stillson Wrench, **33** Number One (ITEM 1, rendered down); 34-36 free. |
| Armors 23-28 | northern armour. **23** Sensible Trousers, **24** Works Cap, **25** The Fuse (Removed), **26** Governor; 27-28 free. |
| **Enemies 30-35** | northern encounters. **The 1-19 ordinary block is full** (only 19 free); ordinary enemies continue at 30. **30** Loose Pressure, **31** Attempt (Unnumbered), **32** Ambulant Salvage; 33-35 free. |
| Enemies 27-29 | northern bosses - the last of the 20-29 boss block. **27** Attempt Eighty-Four; 28-29 free. |
| **Troops 30-33** | northern encounter groups. **The 1-19 block is full** (18-19 free only); encounter groups continue at 30. **30** Loose Pressure*3, **31** Attempt (Unnumbered)*2, **32** Salvage + Pressure, **33** Salvage + Attempt*2. |
| Troops 28-29 | northern set-pieces - the last of the 20-29 block. **28** Attempt Eighty-Four; 29 free. |
| Skills 140-149 | northern enemy and boss skills. **140** Let Go, **141** Still Trying, **142** Take A Part Off, **143** Overpressure, **144** Due North, **145** Make Good; 146-149 free. |
| Maps 21-27 | Upper Clanging, its four interiors, the Long Field, the crag |

Current maxima at time of writing: Actors 10, Classes 10, Skills 136, Items 29,
Weapons 31, Armors 22, Enemies 26, Troops 27, States 36, CommonEvents 2,
Animations 120, Maps 20, switches 46, variables 5.

## 10. Switches and variables

| id | switch |
| --- | --- |
| 47 | `SW_NORTH` - has been to Upper Clanging |
| 48 | `SW_TWO_HUNDRED_ASKED` - Ott has explained what she needs |
| 49 / 50 | `SW_OILSKIN_ASKED` / `SW_OILSKIN_GOT` |
| 51 / 52 | `SW_SPAR_ASKED` / `SW_SPAR_DONE` |
| 53 | `SW_AIRSHIP` - the Two Hundred flies; the vehicle has been placed |
| 54 / 55 | `SW_ITEM_ONE_ASKED` / `SW_ITEM_ONE_DOWN` |
| 56 / 57 | `SW_84_BEATEN` / `SW_84_REBUILT` |
| 58 | `SW_HOB_BRYD` - they went for a drink |
| ~~59~~ | `SW_BALLAD_ASKED` - **reserved and unused.** Drafted as the ask half of an ask-then-done pair; 3.3 then specified the fete minutes as a readable *board*, and a board is a document rather than a conversation, so there was never anything to ask and `SW_BALLAD_DONE` does the whole job. Never set, never read, so it gates nothing and orphans no page. Ids are not renumbered here, so it stays reserved; `build_game.py` names it `(unused - reserved, see NORTH.md 10)` in `System.json` so that the next person to open the editor does not go hunting for the event that sets it. |
| 60 | `SW_BALLAD_DONE` - verse seven was struck at the fete |
| 61 | `SW_CENSUS` - heard the Cold Winter |
| 62 | `SW_COTTERILL` - met the family |
| 63 | `SW_SPARE_ASKED` - the nine-year-old has applied |
| 64 | `SW_LONG_FIELD` - has been in the field. Set by an **autorun** in the corner of Map 26 that erases itself, exactly like Upper Clanging's weather, and not by a player-touch tile inside the gate: the path up the field is two tiles wide and a player who walks up the other one never touches it. |
| 65 | `SW_CLAUSE_SEVEN` - Ott showed you the log; changes the finale |
| 66 | `SW_ROOM_FOUR` - room four at the Wyvern |
| 67 | `SW_GERALD` - that is all that is being said about Gerald |
| **68** | `SW_TWO_HUNDRED_FLEW` - set down beside the tower, out of the air. Appended after this table was written; 5.4's log entry says REACHED THE TOWER and nothing else in the game knew whether she had. Set by the Clause Seven event on Map 8 - see 13. |
| **69** | `SW_TRAVELLERS` - the Two Very Ordinary Travellers have been asked how long, exactly. A switch and not a self switch because they are one joke with two mouths and either can be asked first, and a self switch is keyed on (map, event, letter). |
| **70** | `SW_OTT_MATERIALS` - Ott asked you to ask him what the tower is made of. Its own switch because the beat sits six deep in her flying chain, and `SW_AIRSHIP` says the ship exists and nothing about whether she got round to asking. It has a second job it was not designed for and is now the only switch that can do: being the *last* thing that chain sets, it is Ott's "nothing left owing" marker, and all three of her appended field pages require it so that they cannot shadow the chains they sit below. |
| **71** | `SW_ITEM_ONE_USED` - the crate was set down in front of the throne. The stretch goal in 7. `SW_ITEM_ONE_DOWN` says ITEM 1 came off the crag and says nothing about where it went; this is the only thing in the game that knows, and the ending is the only place that says. |

| id | variable |
| --- | --- |
| 6 | `VAR_PLAQUES` - wreck plaques read; Ott opens up at twelve. The **thirteenth** plaque does not bump it: twelve is twelve, and the thirteenth is one you make. |
| 7 | **`VAR_BLUSHES`** - "things nobody quite said". Bump with `story.blush()` **and nowhere else**, exactly as `VAR_TROPES` is handled. **Twenty-five reachable moments in the finished build** - see 2.3 for how that is counted and why a grep says 28. |
| **8** | `VAR_OTT_ORDER` - which beat Ott is on while the oilskin-and-spar order is outstanding. Appended after this table was written. A variable and not four self switches because a page condition can name exactly one self switch, and this chain is nine beats long. |
| **9** | `VAR_OTT_FLYING` - the same thing for the seven beats after the Two Hundred flies. Its last write is the one that sets `SW_OTT_MATERIALS`, which is what makes that switch mean "Ott has nothing left owing" - see 70, and see 16 step 6 for the lockout that fact fixes. |

## 11. Build modules

    build/north.py     Maps 21-25: Upper Clanging and its interiors
    build/field.py     Maps 26-27: the Long Field, the crag, Attempt
                       Eighty-Four, ITEM 1, and the north-west of the world map
                       - `journey.py` keeps Map 8 and calls hooks in here,
                       exactly as it does for `wilds.py`. It also holds the
                       three pages `north.py` appends to Ott and the works
                       stores ledger, because those are the field's payoff and
                       the crag's, and 11 says the field's writing lives here

The Register A retrofit in section 3 is edits inside `village.py` and
`south.py`, next to the events it belongs to, per the existing convention that
dialogue lives beside its event and not in a strings table.

## 12. Verification

Same as everything else: screenshots for maps, `balance.py` for the fights,
`validate.py` after every build, scenarios for anything with state.

| scenario | what it proves |
| --- | --- |
| `north_road` | the west road is walkable end to end from the Gloamwood junction, the Standing Stones sit on it, and the town door opens |
| `reachable_clanging` | all four doors of Upper Clanging, walked with the arrow keys from the road |
| `two_hundred` | oilskin bought in the south, spar forged in the north, and the airship is *placed* - assert `$gameMap.airship()._mapId` and coordinates |
| `airship_lands` | **done, and it does more than this row asked.** It asserts `isAirshipLandOk` out of the flags on the tower door, the grass beside it and all three rocks; then it boards, flies the Two Hundred over the door, **presses the button, and asserts she is still in the air**; then lands one square west and walks in. Then all three air-only rocks, in turn. The note about the road in the original row is wrong - see 5.2 - and the coordinates it gives are right anyway. |
| `hob_and_bryd` | the same spar with Hob in the party: the meeting runs first if it has not, the forge takes an afternoon instead of a day, `SW_HOB_BRYD` is set, and `VAR_BLUSHES` counts the two moments once each |
| `long_field` | **done.** Walks in off the spur road, reads all twelve, proves a plate cannot be read twice for two, and that the twelfth opens Ott up and sets `SW_CLAUSE_SEVEN` and that the speech happens exactly once. Then the thirteenth, on `itemValid`, and that it does **not** move the counter |
| `eighty_four` | **done.** The furrow is walked from her empty plot to the top of the field, the action button reaches her, "Stop her" starts the right fight against the right enemy (asserted off `$gameTroop`), and then `BattleManager.abort()` hands the interpreter back the way a win does, so the stop, the rebuild and the governor all run for real. The numbers are `balance.py`'s job, the same as `battle_mook` |
| `item_one` | **done, and it was not in this table.** The stores ledger, the crag off the world map, the log, ITEM 1 off the crag, and Ott rendering it down into Weapon 33 and Armor 25 - including that the crate in the party beats every other page she has, and stops beating them the moment she takes it |
| `blushes` | walk the Register A retrofit and assert `VAR_BLUSHES` lands on the expected total. A counter nobody checks is a counter that silently reads zero in the ending. |
| `finale_clause_seven` | **done, folded into `finale_ending` rather than written as its own file, and it needed the trick rebuilding first.** Filtering Show Text out of the command list is exactly what makes a branch untestable - the branch *is* Show Text - so the messages are now captured instead of deleted, and the finale runs eight times over: clause seven off, on, the materials question on its own, both together with the Two Hundred flown, both bounty tiers with the other tier's line asserted absent, `SW_ITEM_ONE_USED`, and then one full-length pass for the switches, the receipt and the title. Twenty-six checks. See `CLAUDE.md` under Verifying for the harness and the two things that go wrong without it |

**New `validate.py` checks - all in as of 2026-08-25**, because they are a
genuinely new class of bug that nothing else catches:

* `checkPassage` is now faithful to the engine, including the clause that makes
  a *partial* answer to a multi-bit question fall through to the layer below.
  That only matters for `0x0f`, and `0x0f` is half of `isAirshipLandOk`.
* every command 202 that places the airship, and `System.json`'s own start
  position, must name a real map and a square that is actually airship-landable
  - the difference between "parked" and "left over from the blank project".
* a map with an airship on it is flooded from its **landable squares** as well
  as its transfers, so an event only an airship can reach no longer reads as
  unreachable. Squares with an event standing on them are excluded, because
  `Game_Vehicle.isLandOk` excludes them.
* two notes read off the finished data. `<aironly>` on an event asserts it
  cannot be walked to *and* that there is an airship on the map at all;
  `<noairship>` on an event asserts its square is not landable. The Tower Door
  carries the second one, which is 5.2 asserted rather than remembered.

Both were checked by breaking them on purpose: clearing `0x0800` off tile 88
makes the Tower Door fail, and laying a line of grass from the Isle to the
beach makes the Isle and the Sheep fail.

## 13. Things that will cost time to rediscover

* **Tilesets 5 (SF Outside) and 6 (SF Inside) already exist** in
  `Tilesets.json`. No new tileset records are needed. SF Outside's A1/A2 are the
  *ordinary* Outside water and grass, which is why an industrial town can sit on
  the same ground as everything else.
* `checkPassage` decides from the **topmost** non-`0x10` tile and ignores
  everything beneath it. Every passability surprise in this expansion will be
  that sentence.
* The airship in `System.json` is pre-declared with junk coordinates from the
  blank project. It is not evidence that anybody set it up.
* Command 202 has no `rmmzdata` helper yet. Write one; do not hand-build the
  dict.
* **A scenario that walks the world map has to turn encounters off first.**
  `north_road` failed three checks, passed on a re-run, and failed again: a
  random battle had eaten the key presses. Nothing in the transcript said so -
  the player simply stopped moving. `{"eval": "$gameSystem.disableEncounter()"}`
  as the first step, and it is deterministic. Every walking scenario the game
  had before this one was indoors, which is why it had never come up.
* **`Canvas.blob` does not know where the coast is.** `journey.py` plants a
  conifer wood at (11, 11) that is eleven tiles wide, and until this session
  the coastline only reached the eastern third of it: eight tiles of pine have
  been standing in open sea, visible from the north road, for the whole of the
  game so far. The lobe puts ground under all of them. `field._upland()` is a
  blob that stops at the water's edge and everything on layer 1 up here goes
  through it.
* **The Standing Stones are a player-touch event with no self switch**, so
  every step onto (11, 18) re-reads all four windows *and* bumps `VAR_TROPES`,
  which is the number the ending prints. The west road was drawn straight
  through them first - it looked wonderful and it would have inflated the
  cliche tally by one per journey. It now passes them on two sides instead.
  Anything else routed through an existing world-map landmark wants the same
  check: `trope()` is only "once per playthrough" when something guards it.
* Headless runs at about twelve frames a second on a map, so a flight across a
  50x50 world map in a scenario is slow. Assert on `$gameMap.airship()` state
  and `isAirshipLandOk()` rather than flying anywhere you do not have to.
* Message widths are still 47 characters beside a face and 60 without. Every
  sample line in this document is **indicative and unchecked**; `say()` will
  refuse to build the long ones. Break them earlier rather than moving a name
  into `speakerName`, per the house convention.
* `TILES-AND-ASSETS.md` has nothing about the SF sheets. Add what you identify
  as you go, so the session after this one does not repeat the lookup.
  **Done** - it now has a section on tilesets 5 and 6, and on the tile name
  tables below.
* **Every stock tileset ships a `.txt` name table** beside its `.png`, one
  `English|Japanese` line per tile in tile id order, and it is the editor's own
  palette text. It is by a wide margin the fastest way to identify an SF tile,
  and it is the only practical way to find the ones that must *not* be used.
  `mapkit.tile_names(sheet)` parses one.
* **A roof anchor is a (column, row) on the C sheet, and the C sheet changes
  with the tileset.** `ROOF_BROWN` is (13, 3), which on SF Outside is the middle
  of the Clock Tower - so an Outside roof on a northern map builds, validates,
  and draws a three-storey clock face on a cottage. The same goes for every
  A-sheet `kind`: 116 is a grass plateau on tileset 2 and a wooden wall on
  tileset 5. `Canvas` now takes `tileset=` and refuses anchors and forbidden
  tiles accordingly, but nothing in the *data* distinguishes them.
* **The Clock Tower is not a nine-slice.** Cap, clock face, brick shaft - nine-
  slicing it four tall repeats the middle row and it grows a second clock. Use
  `Canvas.clock_tower`.
* **Weather is global and survives a map transfer.** `$gameScreen.clear()` runs
  on a new game and nowhere else, so rain started in Upper Clanging is still
  falling in Thistlewick, and indoors. Every way *out* of a wet map has to set
  it back to "none". `rmmzdata.set_weather` documents this at the call site.
* `talker()` lives in **`build/south.py`**, not `story.py`, and did not take a
  `pages=` argument - 1.7's appended-page pattern needed it added. It has been,
  additively, defaulting to no extra pages, so every existing call is unchanged.
* **Three engine rules about a landed airship, and they only bite where an
  airship is the only way in.** All three were found by playing
  `airship_lands`, and none of them shows in the data:
  1. `Game_Player.triggerButtonAction` offers the **vehicle before the event**:
     `if (this.getOnOffVehicle()) return true;` comes first, and only then
     `checkEventTriggerHere` / `checkEventTriggerThere`. So the action button
     pressed while standing on a landed airship *always* takes off again. On a
     rock with one square to stand on, every "same as characters" event on it
     is unusable, and the symptom is an event that starts nothing.
  2. `Game_Vehicle.isLandOk` refuses a square that has **an event** on it, not
     just a square with the wrong flags. A rock with a prop on every tile of it
     has no way in at all.
  3. Together those two say how to build an air-only place: props are
     **player-touch, below characters** - the idiom this world map already uses
     for the Standing Stones, the Hermit and the top of the Barrow - and every
     rock keeps one bare square in the middle for the airship. That is why the
     Isle is four tiles and not three.
* **A landed airship is drawn below characters** (`Game_Vehicle.refresh` sets
  priority 2 while driving and 0 when parked), so a screenshot taken with the
  party standing on it shows no airship at all. Step one square off before
  shooting.
* **An isolated grass tile on the world map draws as all edge and no middle**,
  which is to say a sandbank. That is exactly right for a rock in the sea and
  it is worth knowing before you go looking for a beach autotile.
* `mapkit`'s world-map names are not the sheet's names, and two are actively
  misleading: `W_HILLS` is World_A2's **Mountain (Grass)** and `W_DUNES` is its
  **Hill (Dirt)**. The usage is fine everywhere it is used; the names are not
  evidence.
* Variable **10** is already in use (`build_game.py`, "scratch: gold
  reallocated"), so section 9's "variables 5" maximum is wrong. 6 and 7 were
  free and are now `VAR_PLAQUES` and `VAR_BLUSHES` as planned; there is no
  conflict, but do not trust that line for the next free id.
* **`Canvas.set` checked the forbidden list on every layer, including the
  region layer.** Region ids and shadow bits live on layers 5 and 4 and are
  numbers, not tiles - and region 1 is the number 1, and tile 1 on
  SF_Outside_B is a neon shop sign. The first SF map to want random encounters
  went through `paint_regions` and was refused at (0, 0). Fixed: the check is
  `z < 4` now. Every SF map with encounters on it would have hit this.
* **A downed airship, seen from directly overhead, has no tile**, and the two
  obvious ways of drawing one are both wrong in a way no amount of reasoning
  shows: two rows of A3 outer wall is a **garden wall** and two rows of SF roof
  over one of A3 wall is a **garden shed**. The A4 free-standing pairs, which
  are the right tool on paper, have *gravel* tops. A heap is what works. See
  `TILES-AND-ASSETS.md`.
* **On a carved map the wall *top* is the map.** `dungeon_walls` fills every
  square that is not a room with it, so on Map 27 that single choice is two
  thirds of the screen. Wall D (Metal)'s top is green-grey mould and the
  airship came out as a flooded cellar.
* **The contact sheet catches things this document recommends.** 4.4's use
  list includes `Sphere Machinery`, which has coloured wiring and a console
  lit cyan bolted to its right-hand cell and cannot be cropped without it. Run
  the labelled contact sheet on any new map before calling it done, including
  when every tile on it came off a list somebody already checked.
* **`BattleManager.abort()` hands the interpreter back the way a win does**, so
  a scenario can prove a boss fight starts, look at what turned up, and then
  run the whole aftermath for real without playing seven thousand hit points at
  three frames a second. `endBattle(1)` fires the event callback; with no
  escape or lose branch on the Battle Processing command, execution simply
  continues.

## 14. Decisions already taken

These were open questions at the end of the design session and were settled
rather than left. They are recorded with reasons so a fresh session can disagree
knowingly rather than by accident.

**The retrofit ships, and it is strictly additive.** Section 3 touches
Thistlewick and Nether Sopping, which are finished and which people have played.
Rule 1.7 is what makes that safe: new events, appended pages, and not one
existing line re-voiced. Two ideas got *better* under the constraint - the
travellers are now royalty **and** newlyweds discovered on a second visit, and
the Standing Stones get a second sign correcting the first instead of a longer
first sign.

**Mrs Cotterill's night shift and the Cold Winter cohort both stay.** They are
the most legible of the Register A set, and both pass all four tests in 1.5:
literal on the page, warm, about people who like each other, and unexplained.

**Hob and Bryd stay, and nothing is ever said.** See 4.6. It is the doctrine of
1.2 applied to a relationship, and the payoff is a drink, not a scene.

**Full scope.** Seven maps, the vehicle, the optional boss, the air-only
content, and the retrofit. If it has to shrink, the cut line is the Long Field
and Attempt Eighty-Four; keep the town, the airship, section 5.6 and the
counters.

**Upper Clanging has rain.** Decided 2026-08-24. It is what sells "soot, brick
and rust under a permanent chimney haze" for the price of one event command,
and the engine has had `Set Weather Effect` all along. The cost is not the
weather, it is the bookkeeping: weather is global and survives a transfer (see
13), so every road, door and stair out of the north has to set it back to
"none" or the player carries the rain home. `rmmzdata.set_weather` exists and
refuses a misspelled type.

**Blushes get a job.** See 2.3 - a counter that only reports is a fourth
write-only variable, and this game already has three.

**No eleventh party member.** Ten is already more than four slots can use, and
the north's contribution is a vehicle and a town, not another body.

**Clause seven waits for the airship.** Decided 2026-08-26, and it is a
decision rather than an accident of the fix in 16 step 6. Ott's two clause-seven
pages require `SW_OTT_MATERIALS` as well as twelve plaques, and that switch is
the last thing her flying chain sets - so the player has to have finished the
Two Hundred before she will get the works ledger out, even though the Long Field
is walkable on foot long before that. The lockout fix needed *some* terminal
switch on those pages or they would shadow the ladder above them; requiring this
one also happens to be right on its own terms. Clause seven is the works'
founding grievance and she has been carrying it for four generations. She does
not hand it to a stranger who has read some plaques; she hands it to somebody
who has built the thing with her. And the alternative order is worse in the
finale: Grimspite answers a question about a document the player was shown
before they had any reason to care about it.

**Meredith Crooke is repaired, not merely re-cast.** See 8.1. The face swap was
first rejected under 1.7 and then reinstated once it turned out she is drawn as
a woman and fought as a man in armour - which is a contradiction the game
already ships, not a preference of this expansion's. It is two lines and it
stands alone; build it first, or build it even if nothing else here happens.

## 15. Genuinely open

Short list, and none of it blocks a start:

* ~~**Northern encounter design**~~ - **settled 2026-08-25**, and along the
  seam this section proposed. Three enemies and four groups, and nothing up
  here is a monster and nothing up here is angry: **Loose Pressure** (a hundred
  and forty years of stored steam finding the way out all at once - it is not
  attacking anybody, it is leaving), **Attempt (Unnumbered)** (too early to
  have been given a number; it has been getting one foot off the ground since
  before anybody now alive was born) and **Ambulant Salvage** (parts of nine
  different attempts, walking; nobody assembled it and nobody can prove it was
  not assembled). Ambulant Salvage at 1600/52 is the toughest ordinary enemy in
  the game, which is right for the last region, and `balance.py` was run before
  a stat was written.
* ~~**Whether the north is gated**~~ - **settled**, and it shipped as the
  recommendation: no hard gate. It is soft-gated by the oilskin, which needs
  the south, and by encounters that hurt. Nether Sopping's precedent held.
* ~~**The ITEM 1 stretch goal** (7)~~ - **built**, not cut, and it reaches all
  the way through: the crate comes off the crag, Ott takes the fuse out of it
  first, and if it is set down in front of the throne instead then
  `SW_ITEM_ONE_USED` is the only thing in the game that knows and the ending is
  the only place that says. `item_one`, `item_one_throne` and pass G of
  `finale_ending` cover it end to end.

Which leaves this section empty. Anything that lands in it from here is new
work, not unfinished work.

## 16. Where to start

The order matters more than usual here, because three things in this document
are cheap to get right early and expensive to retrofit.

**0. Confirm the tree.** `python3 build/build_game.py && python3
../tools/validate.py .` Clean, and no diff beyond the four files in 8.1a. If
that is not true, stop and find out why before adding anything.

**1. Tooling, before any content. - DONE 2026-08-24.** Everything below leans
on these, and all of them are in and rebuild the existing twenty maps
byte-identical:
   * `rmmzdata.set_vehicle_location()` - command 202, verified against
     `Game_Interpreter.command202`. See 5.2.
   * `rmmzdata.set_weather()` - command 236, for the rain (14). Refuses a type
     that is not one of the engine's four, and documents the persistence trap.
   * `story.blush()` - the bare variable-add, shaped exactly like `trope()`.
     See 2.3.
   * `db.py` carries switches 47-67 and variables 6-7 by name, and
     `build_game.py` writes all of them into `System.json` - the switch array
     had to grow from 64 to 72 to hold them.
   * `System.json`'s airship moved to `startMapId: 0`. The *ship* carries the
     same inherited junk and was deliberately left alone; 8.2 sanctions the
     airship only.
   * `talker(..., pages=)` in `south.py`, which 1.7's appended-page pattern
     needs and did not have.
   * The SF tile vocabulary **appended to `mapkit.py`**, ~80 names with an
     `SF_` prefix, confirmed in four new `sampler.py` modes (`sf_walls`,
     `sf_yard`, `sf_ground`, `sf_props`) and written up in
     `TILES-AND-ASSETS.md`.
   * `Canvas(tileset=...)`, which is new and load-bearing: it selects the roof
     anchors and the forbidden-tile set for the sheet the map is actually
     drawn on. The first SF sampler put a clock tower on every cottage because
     `ROOF_BROWN` means something else on tileset 5 - see 13.
   * `Canvas.clock_tower()`, because the Clock Tower is not a nine-slice.
   * `SF_FORBIDDEN`, written as **names** and resolved through the sheets'
     `.txt` tables. 92 tiles, against the 19 that hand-picking coordinates
     found - it caught a second vending machine that is called an ATM.

**2. The world map before the town. - DONE 2026-08-24.** `build/field.py`
holds the five `north_*` hooks and `journey.py` calls them where it calls
`wilds.py`'s. What is on Map 8 now:

   * the north-west lobe, x 3-15 by y 5-19, merged into the existing coast so
     that the conifer wood finally has ground under it (see 13);
   * the west road: west from the Gloamwood's north mouth (17, 20) along the
     top of the wood to (9, 20), then north to the town's door at (9, 13);
   * two spurs - (9, 15) east to the Long Field, and (9, 13) west and north to
     the crag at (6, 8);
   * the Standing Stones sitting in the elbow of that corner, **beside** the
     road and not on it, for the reason in 13;
   * the junction signpost at (14, 19), and the town, field and crag icons;
   * `REG_CLANG` (region 4) over the lobe, pointed at the same three troops as
     the rest of the north, so it is inert today and ready later.

   The three destination events are **not** written: a Transfer Player wants a
   map to transfer to, so the town's event belongs with step 3 and the Long
   Field's and the crag's with step 6. `WORLD_CLANGING_STEP` is (9, 13).
   `gate`, `south_road` and `journey` still pass; `north_road` is new and walks
   the whole thing with the arrow keys.

**3. Upper Clanging's shell, then its interiors. - DONE 2026-08-24.**
`build/north.py` holds Maps 21-25 and `build_game.py` carries them. What is
there:

   * **Map 21** is one street straight up a hill, 34x44. The hill is three
     terraces separated by two-row brick retaining walls with three-tile
     flights of iron steps cut through them where the road goes; the stair
     tiles are flagged blocked-left and blocked-right, so a flight is a
     channel. The **Hoyle Works** stands across the head of the street with
     its way in on the centre line - an open arch rather than a door leaf,
     because the opening is sized for an airship - the **Clock Tower** beside
     it, and the works yard behind and around it. Below: **Ollerenshaw's** and **the Safety
     Valve** facing each other across the middle terrace, and **the Parish
     Rooms** on the bottom one, with the gate at (17, 42) and the sign beside
     it. Three more buildings have shutters instead of doors.
   * **Maps 22-25** are real rooms - walls, floor, an exit door, nobody home.
     Tileset 6, whose A1/A2 are the ordinary Inside ones and whose A5 is the
     street's own, so only its A4 walls were new.
   * **The rain** is one autorun on Map 21 that sets it and erases itself, so
     it also rains in a screenshot warped straight in. Every way *out* dries
     the player off, and that is in the `door()` helper rather than in each
     event, because forgetting it once sends the player home in the rain and
     nothing in the data would show it. `reachable_clanging` asserts it at
     every door and at the gate.
   * **`places.CLANGING_GATE`** is (17, 42); the town's destination event is in
     `field.north_events` and sets `SW_NORTH`.

   Four things the Canvas caught that would otherwise have shipped: windows
   drawn on roof rows rather than wall rows, an oil drum and a crate on two
   different roofs, and a chimney on a roof crest, which is invisible for the
   reason now written up in `TILES-AND-ASSETS.md`. Two more were found by
   looking: a ladder used as decoration is a climbable route over a retaining
   wall, and `interior`'s `floor_alt` checkerboard turns two unlike textures
   into a chessboard forty feet across.

   Read the roof note in `TILES-AND-ASSETS.md` before adding a building: the
   SF roof is a flat grey slab, so northern buildings are drawn shallow and
   given their height in storeys of A3 wall instead.

**4. The cast and the dialogue. - DONE 2026-08-24.** All four rooms are
furnished and there are thirteen people and eight readable things in the town.
What is there:

   * **Ott** has five pages on a new `north.ladder()` helper - one beat per
     conversation, because a page condition can name exactly one self switch
     and `Game_Event.refresh` takes the *last* page that qualifies, so A sets
     B sets C sets D is the only way to say "next time". Page one is the
     introduction and the drain cock; pages two to four are the stuffing box,
     the nipples and the threads; page five is what she says for the rest of
     the game. That is 4.7's "four times, at intervals" - one visit is the
     interval, and the fifth page exists so the bit stops rather than loops.
   * **Nine blushes** in the town, asserted one at a time by
     `clanging_cast`: Ott's four, Spare's two, Mrs Cotterill's one, the Cold
     Winter, and Hob and Bryd. Mr Cotterill, Winnie Marsden and Old Sowerby
     deliberately bump nothing - they are the reaction shots, and counting a
     joke three times is the game explaining it.
   * **Hob and Bryd meet**, and the meeting is all of it. `SW_HOB_BRYD` is
     still unset and the drink belongs with the spar in step 5. The state is
     in one page rather than in page conditions so that it fires the moment
     Hob walks in, including on a second visit after Bryd has already
     introduced himself to a Hobless party.
   * **The shop is in**, at the Parish Rooms counter, as Mrs Tunnicliffe's
     second option: Items 13-15 (Bread and Dripping, Stewed Tea, Works
     Liniment), Weapon 32 (Stillson Wrench) and Armors 23-24 (Sensible
     Trousers, Works Cap), plus potions and Mrs Barrow's oilskin. The rest of
     each range in section 9 is untouched, for the works' gear and ITEM 1.
   * **SF Inside's B and C sheets are identified** - about seventy names in
     `mapkit.py`, four new sampler modes, and the inside forbidden list grown
     from eleven names to **191 tiles**, because a modern *room* is far easier
     to build by accident than a modern street. Written up in
     `TILES-AND-ASSETS.md`, including which wall pairs are warm: the answer is
     that what you see of an interior wall is mostly its **top**, and Wall K
     (Brick) and Wall E (Metal, Red Rust) both have grey ones.
   * **The furnishing was then judged again, tile by tile.** The rooms read
     well in a screenshot and still had a fire extinguisher with a flame
     pictogram on the wall, an ISO warning triangle, a rack of LEDs called
     `Meters`, a console bank lit cyan called `Large Machine`, two heaps of
     modern litter, a teal plastic bin, a black three-seater sofa and a wall
     planner lettered in katakana - none of which survives 4.4's rule, and
     none of which a map-scale screenshot makes obvious. What found them was a
     labelled contact sheet of **every one of the eighty-two prop tiles the
     four interiors had laid down**, at one tile per cell. That is the check
     to repeat before any new interior is called done; the table of what it
     rejected and what replaces it is in `TILES-AND-ASSETS.md`.
   * The inn's bar and the Parish Rooms' counter are `Large Desk B`, a
     two-tile counter with a dark top. The bar had been a row of `Side Table`,
     which reads as four little round tables in a line - the Slain Wyvern's
     trick, and this town is not that town.
   * **`clanging_cast` is 27 checks and they all pass**, `clanging_faces`
     ten, `reachable_clanging` twenty-three - the last re-run after the
     furnishing changed, because a counter and a furnace are solid tiles
     and a room can be sealed by decorating it.
   * `clanging_faces` asserts each of the ten new faces off the live message
     window and screenshots it, which is the check that catches 4.6's
     off-by-one rather than trusting it.

   Two things worth knowing before adding to it. `validate.py` caught a solid
   waste-pile drawn on the forge's arrival tile, which sealed the whole room -
   run it, do not reason about it. And `interior`'s `floor_alt` claimed
   another victim: tile and lino sound like a matched pair and came out as a
   public convenience forty feet across.

**5. The Two Hundred. - DONE 2026-08-25.** 5.1-5.4 and 5.6 are in, the tileset
flag is in, and `airship_lands` passes. What is there:

   * **The one number.** `build_game.TILESET_FLAGS` ORs `0x0800` onto tile 88
     of tileset 1 and `build_tilesets()` writes it, so the edit is authored
     rather than hand-made and the diff is one number wide. The engine now
     refuses to set the Two Hundred down on the tower's step, and
     `airship_lands` flies her over it and presses the button to prove it.
   * **The ask is a new event, not one of Ott's pages**, and 5.1's speech is on
     it. A page condition is a set of ANDs with no NOT in it, so "she has
     finished the ladder and has not yet asked" is *the same condition* as the
     last rung of the ladder - a page written for it wins and deletes the rung.
     So the ask went on the chalk line amidships (pattern 1), gated by a script
     branch on Ott's own self switch D, and the quest opens on the fourth
     conversation. That is the right answer and not a compromise: 5.6's timing
     joke wants the map walked before she hands it over, and four conversations
     with the chief engineer is the cheapest honest way to spend that time.
   * **Ott has four appended pages** - the standing order, the same thing with
     forty bolts in the party's hands, the handover, and afterwards - each
     one's condition strictly harder than the last, all four also requiring
     self switch D so nothing can fire before the ladder is finished. Her five
     existing pages are untouched and page five is still reachable.
   * **Mrs Barrow invoices the works.** A page appended to her, guarded by
     `SW_OILSKIN_ASKED`, which runs the forty-bolt scene once and is her own
     shop page every time after. She takes no money: a works order means nobody
     can arrive here too poor to finish the airship, and "on account" is a
     better joke than a price.
   * **Bryd has three appended pages**, and `SW_HOB_BRYD` is finally set - on
     the Hob path only, because they cannot go for a drink if one of them is
     four days' walk south. Without Hob it is a day's work and the shorter
     version of the same scene, and Grumnir is named and not present and it
     costs Bryd nothing to be glad about it. If the party reaches the spar
     errand without ever having spoken to him, page one's own openings run
     first rather than instead - handed in, not rewritten.
   * **5.4's log entry** is a page appended to the attempt log, guarded by
     `SW_TWO_HUNDRED_FLEW`, which the Clause Seven parallel on Map 8 sets when
     the party is on foot within two squares of the door with the Two Hundred
     parked within four. A player-touch tile would not do: the airship keeps
     the party on its own square when it lands, so anybody who set down on the
     trigger square would miss it.
   * **5.6's three rocks are all in** - the Isle of Uncertain Ownership with
     its plaque and its spherical sheep, Attempt 112 on its stack with the
     number-plate, and the Hermit's middle distance with the hill and the
     bench - and `validate.py` now asserts out of the tileset flags that none
     of them can be walked to. See 13 for the three engine rules that decide
     how they are laid out.

   **What is deferred, deliberately, to step 6.** The plaques of 5.5,
   `VAR_PLAQUES` and `SW_CLAUSE_SEVEN` are Long Field content and belong with
   the Long Field. So is Ott's thirteenth plaque: the number-plate is a key
   item the party **keeps**, so the field can read it with an `itemValid` page
   condition the way the Barrow already reads the flat-packed bench, and Ott's
   reaction to it is written there rather than here.

**6. The Long Field, Attempt Eighty-Four, the crag. - DONE 2026-08-25.** Maps
26 and 27 are in `build/field.py` and `build_game.py` carries them; 5.5, 6 and
7 are all built, and `long_field`, `eighty_four` and `item_one` pass. What is
there:

   * **Map 26 is a war cemetery for machines and nothing in it says so.**
     Wrought-iron railings on a stone plinth, a double gate, and five rows of
     wrecks in numerical order with a plaque in front of each. Nobody remarks
     on it and no line of dialogue uses the word. The rows age as you walk
     them, oldest at the gate.
   * **The twelve plaques**, counted in `VAR_PLAQUES`, each behind its own self
     switch so a plate cannot be read twice for two. The joke is the sequence
     and only the sequence: the gate end names a broken part every time -
     ENVELOPE, SEAM; BALLAST, RELEASED IN ERROR; FRACTURE, MAIN SPAR; FRACTURE,
     MAIN SPAR (DIFFERENT SPAR) - and by the top of the field every plate says
     IN SIGHT OF THE TOWER and every cause says UNDER REVIEW. Nothing in the
     game points at that. Ott will, once, if you have read all twelve.
   * **Attempt 84's plate is one of the twelve and its cause line is blank** -
     the only blank one in the field - because she never stopped. Her plot is
     empty and there is a gouge three feet deep going north out of the back of
     it, through four rows of her own kind, to where she actually is. That
     costs nothing and it is the whole character.
   * **The thirteenth**, on `itemValid` with Attempt 112's number-plate, and it
     deliberately **does not** bump `VAR_PLAQUES`: twelve is twelve, and the
     thirteenth is one you make. Ott is not in the scene. The card behind the
     plate has been ready for years - correct, eleven words, and nowhere to put
     it - which says what she thinks about a wrong plaque better than she would.
   * **Clause seven** is two pages appended to Ott (1.7 pattern two, on the
     `pages=` argument `north.py` already built her with), guarded by a
     variable page condition at twelve. She copies the sentence into the works
     ledger and four generations annotate it: *does this apply to us* / *it
     does not say it applies to us* / *it does not say it does not* / and the
     fourth, in pencil, recent, is one word, and the word is **quite.**
   * **Fixed 2026-08-26: those pages have to require `SW_OTT_MATERIALS` as
     well, and leaving it out was a silent content lockout.** They are appended
     *below* everything `north.py` built on that event, and `refresh` takes the
     last page whose conditions hold, so a condition that can be true while a
     page above still owes a beat does not follow that page - it deletes it.
     Twelve plaques is reachable on foot before the works has been asked for a
     ship at all, so reading the field early shadowed the fabric page, the
     handover page, the nine beats of the order chain and the seven of the
     flying chain: no airship, no `SW_OTT_MATERIALS`, no way back, and no
     symptom except Ott saying the wrong thing for the rest of the game.
     Reordering only chooses which ladder dies. `SW_OTT_MATERIALS` is the last
     switch the flying chain sets, so it is the one switch that means "Ott has
     nothing left owing", and requiring it on all three appended pages makes
     the order the player does things in stop mattering - read the field first
     and she simply holds clause seven until the ship is finished. **General
     rule for anything appended to a character later: a page appended below a
     ladder must require that ladder's terminal switch.** An exhaustive sweep
     of all 1520 reachable states of that event is in the commit; `long_field`
     asserts both halves - twelve plaques alone changes nothing, and the moment
     switch 70 is set she has clause seven ready.
   * **Attempt Eighty-Four** is Enemy 27 / Troop 28, `SF_Slaughterrobot`, 7600
     hp, and strictly harder than the Forty-Fourth on both axes at every level
     `balance.py` was run at. `Make Good` heals her out of the neighbours at
     45%, which is the thing she has been doing for a hundred and forty years,
     done once more in front of you. Stopping her is a **choice**, because
     Ambrose could ask and she cannot, so the player has to decide with nothing
     to go on. The governor is **given** afterwards rather than dropped, which
     is the Barrow's rhyme in a different key.
   * **Map 27 is a working airship with nobody on it.** Nothing aboard is
     broken except the hole the crew came out of. The log is the best thing on
     her and it is seven minutes long: 0938 TOWER IN SIGHT. ALL WELL. / 0939
     ALL WELL. / 0940. / 0947 ON THE CRAG. ALL HANDS. NO INJURIES. / 0947
     NOTHING TO REPORT BETWEEN 0940 AND 0947 - and then, in a steadier hand,
     WE ARE WALKING HOME.
   * **The works stores ledger** is a new event in the works (pattern one) and
     is the only thing in the game that says what is on the crag, which it does
     by arithmetic: ITEM 1, one off, 1802, issued 199 times, returned 198.
     Nothing anywhere says what it is. The icon is a bomb.
   * **ITEM 1 renders down** on a third appended page of Ott's, into Weapon 33
     (Number One) and Armor 25 (The Fuse (Removed)) - which she takes out
     first, before anything else on it is touched.
   * **Both destination events on Map 8** are appended at the end of
     `field.north_events`, ids 25 and 26. Never inserted: a self switch is
     keyed on (map, event id, letter), so putting one in the middle would move
     every id after it and silently reset the Isle, the sheep, Attempt 112, the
     bench and Clause Seven in every existing save.

   **No new blushes.** `VAR_BLUSHES` is still the town's nine. Nothing in the
   Long Field or the crag produced a Register A line that passed all four of
   1.5's tests, and 1.5's first test is the one that matters here: the field is
   Register B and forcing an A into it would have failed "would it still be a
   good line if the second reading did not exist". Section 3 is where the rest
   of the count comes from.

   Three things that cost time, written up in `TILES-AND-ASSETS.md` at length:
   a downed airship seen from directly overhead has **no tile**, and the two
   obvious ways of drawing one are a garden wall and a garden shed; a carved
   map's wall *top* is two thirds of the screen and Wall D's is green mould;
   and the contact sheet caught four more wrong-century props, two of which
   **4.4 recommends** - `Sphere Machinery` has a cyan console bolted to its
   right-hand cell, and `Broken Pillar B (Metal)` is a heap of gold blocks that
   was standing in all thirty wrecks.

   **Step 6 closed out, 2026-08-25.** The verification is done and the north is
   committed:

   * The tree rebuilds at 27 maps, `validate.py` is clean, and
     `git diff --name-only HEAD -- data/ | grep Map0` is `Map008.json` and
     `Map016.json` and nothing else - Maps 21-27 being new files rather than
     diffs.
   * **All ten northern scenarios pass** on the finished build: `clanging_cast`,
     `clanging_faces`, `hob_and_bryd`, `two_hundred`, `airship_lands`,
     `eighty_four`, `item_one`, `long_field`, `north_road` and
     `reachable_clanging`.
   * `north_road` **broke, and it is the one this document predicted.** Step 2
     wrote it to walk the Long Field spur to (12, 15) and check it got there;
     step 6 then put the field's own door on that exact square, and a
     player-touch Show Choices that nobody answers leaves the interpreter
     running, so `$gamePlayer.canMove()` is false and every later step reports
     the coordinates of wherever the walk stopped. It answers the door now.
     Fixing it needed the trap now written up in `CLAUDE.md`: `{"choose": i}`
     does nothing until the text has finished printing, a four-line window
     takes about two hundred frames to print, and an arrow press before that is
     discarded while the confirm after it silently takes option **0**.
   * **The prop contact sheet is a tool now** - `tools/propsheet.py` - and was
     run over Maps 21-27 rather than only over the two new ones. It found four
     more things, three of which had already survived the step 4 sheet because
     that sheet was of the maps they were not the odd thing on: `Document
     Shelf` is a backlit teal display cabinet, `Medicine Shelf` is a pharmacy
     fridge, `Locker A` has a card reader on the door, and one free-standing
     `Stacked Crates` in the Long Field reads as a door left in the grass. All
     three cupboards are on the inside forbidden list now. The lesson worth
     keeping: **run the sheet over every map an expansion touches, not only the
     new ones**, and look at what is painted *into* a tile before moving it -
     the galley dresser that replaced the pharmacy fridge had a living pot
     plant on it, aboard a wreck nobody has been on for two hundred years.
   * Maps 26 and 27 were screenshotted again afterwards. The Long Field reads
     as what it is and no line in it says so; the wreck reads as being inside
     something. One note for whoever shoots them next: a shot taken immediately
     after a warp catches the fade and comes out black. Put a `wait:120` in
     front of it.

**7. The retrofit (section 3) last. - DONE 2026-08-25.** All eight items are
in, `blushes` walks every one of them, and 1.7 held: **not one existing line
was edited.** Four items are new events (Dorcas's board, the house register,
the fete minutes, the second notice at the Standing Stones), three are pages
appended to people who already had pages (Sops, both travellers, Dorcas), one
is a new prop with a party check in it repeated three times (Wren), and one is
a new prop in the Gilded Turnip (Merribell). The only edits to existing code
are the `extra=` parameter `tale()` grew so that Perpetua's list could have a
command added to the *end* of it, and three tile placements.

**Eleven moments, twelve writes**, which is 2.3's target exactly, and the
count is 20 with the north's nine. What is worth knowing:

   * **The two travellers are one joke with two mouths**, and either can be
     asked first, so the guard cannot be a self switch - those are keyed on
     (map, event id, letter) and this is two events. `SW_TRAVELLERS` (69) is
     a global switch and the only one of its kind in the game. `blushes` asks
     both of them and asserts the counter moved once.
   * **Dorcas's fifth page turns its own condition off on the way out**, and
     it is the only page in the game that does. `Game_Event.refresh` takes the
     *last* qualifying page, so a fifth page on her would otherwise shadow the
     jar handover and the reply - a thirty-year quest - for the rest of the
     game. It fires once, clears `SW_GERALD`, and the feud is exactly where it
     was. Ask her again and she is back to selling beds at 25.
   * **The fete minutes have no qualifying page until Piper is recruited.**
     That is MZ's own way of saying "not yet": `_pageIndex` stays at -1, the
     board is not drawn and cannot be read, and there is no ballad to strike
     verses out of before she joins. In a scenario, **assert `_pageIndex` is
     -1 rather than calling `start()`** - `start()` on a page-less event throws
     on an undefined list.
   * **Bram does not speak, and 3.5 and 3.4's scripts give him lines.** In two
     towns of writing he never has once: he is the narrator's "You ask
     whether...", which 1.4 is right to call the perfect innocent. The
     finished game's convention beat the script, in both places, and the flat
     narration is funnier than the line would have been. Do not "fix" this
     back.

Two props were wrong and a **contact sheet over rooms nobody had changed the
tileset work in** found them, which is the third time that check has paid for
itself:

   * the washstand was `IN_DRESSER`, whose lower cell is `Sundries Shelf A` -
     **two teddy bears and a pink rabbit** - which is the wrong object outright
     and especially wrong beside that scene. It is a `Pot B` ewer over a
     `Basin` now, and those are the sheet's own names for them;
   * the house register was `INC_BOOK`, which the `.txt` calls **Closed Book
     A**, under four lines of narration about forty entries down an open page.
     `INC_BOOK2` is Open Book A.

And two scenario-harness facts, both of which cost a run to find:

   * **A stray `{"key": "Escape"}` on an idle map opens the menu**, and every
     `goto` after it then waits forever for a transfer `Scene_Menu` will never
     perform. `blushes` asserts `SceneManager._scene.constructor.name` instead,
     so the same mistake fails a check rather than hanging the run.
   * **`{"advance": n}` has to come before the counter check, not after it**,
     for a player-touch event. Walking on starts the list and stops with the
     text on the screen; `story.blush()` is the last command in it. Check
     first and you read the value from before the notice was finished.

**8. The ending. - DONE 2026-08-26.** 2.2, 2.3, the clause-seven branch and the
tally additions are all in, and 1.7 held to the letter: `git diff --stat
build/journey.py` is **325 insertions and not one deletion**. Nothing that was
in the ending before the north came out of it, and not a line of it was
re-voiced. What is there:

   * **Two branches inside the Grimspite scene**, before the fight, on
     `SW_CLAUSE_SEVEN` and `SW_OTT_MATERIALS` - the two questions Ott can send
     you up here with, and they are independent because they are two switches
     on two branches. Clause seven he answers straight: the Prophecy walks its
     Chosen One because a thing that flies over is not a story, and *it is a
     Tuesday*. The materials question stops him: nobody has ever asked him
     that, in four thousand years, and he sends the compliment back down the
     hill. **He is never told she managed it**, and he never finds out.
   * **The tally is fourteen appended `if_then` blocks**, in order:
     `SW_ROLAND_GONE`, `SW_SOUTH`, `VAR_BOUNTIES` (two tiers, the second
     nested in the first's else), `SW_HISTORY_DONE`, `SW_LAMP_LIT`,
     `SW_BENCH_DONE`, `SW_TWO_HUNDRED_FLEW`, `SW_84_REBUILT`,
     `SW_ITEM_ONE_USED`, `SW_HOB_BRYD`, `VAR_TROPES` (40 / 20 / else),
     `SW_BALLAD_DONE`, `VAR_BLUSHES`, `SW_MET_QUY`.
   * **2.2 is cashed**: `VAR_BOUNTIES` was the one genuinely dead counter and
     it now has the two-tier line. The companions and turnip lines were
     already there and were left exactly as they were - see 2.2, which was
     wrong about that until it was checked.
   * **2.3 is the payoff.** `SW_BALLAD_DONE` chooses between "Verses struck by
     the Committee" and the flatter "Things nobody quite said", same number
     wearing a joke, and the extra line above four fifths admits there was a
     pattern without ever saying what it was.
   * **The blush threshold moved from 16 to 20** on 2026-08-26, because the
     total moved from 20 to 25 - Ott's flying chain, Bessie and Gudgeon - and
     nothing had gone back to look. See 2.3. The count is now written down
     where the branch is, not only here.
   * **The central irony is two branches that do not know about each other.**
     Grimspite says she will never get one off the ground in sight of this
     place; four hundred lines later the attempt log reads REACHED THE TOWER.
     LANDED ADJACENT. Nobody in the game reconciles them and nobody should.

   **`finale_ending` was rebuilt before any of this could be trusted, and that
   is the part worth reading.** It ran four checks and every one of them would
   have passed with all four ending branches deleted from the game, because it
   tested the finale by *filtering Show Text out of the command list* - and an
   optional ending is made of Show Text inside a Conditional Branch. It now
   **captures** the messages instead of deleting them: `Game_Message.add`
   records the line, `isBusy` always answers false, and the interpreter runs
   the whole cutscene with no key presses and never opens a window. Eight
   passes, **26 checks**, and the passes are their own mutation test - the same
   assertion reads true in one and false in another against real data. Two
   traps, both of which cost a run: an **unanswered choice takes neither
   branch** (`command402` compares against a `_branch` entry nothing wrote, so
   both halves are skipped and a hundred lines vanish silently), and stripping
   the waits collapses the whole finale into a single frame, which is what
   makes eight passes cheaper than the old one. The harness is written up in
   `CLAUDE.md` under Verifying.

**9. Re-run every scenario, not only the new ones. - DONE 2026-08-27.** The
southern expansion broke exactly one old scenario and nothing else noticed.
That is the argument, and it was right again: **30 of 33 passed in 120m22s**,
and all three failures were in scenarios written before this session's work.
None of them was a broken game. All three were a stale assertion about
something step 7 and step 8 had deliberately changed, and the entry worth
keeping is *how you tell those apart*:

   * **`clanging_cast` expected Ott's ladder to yield four blushes.** Step 7
     rewrote that ladder - the stuffing box, the nipples and the threads are
     gone, and the surviving drain-cock moment sits inside a conditional
     branch on Merribell being in the room. Every later check in the scenario
     was low by exactly four with **every delta correct**, which is the shape
     of a stale baseline and not of a broken event: a game that had stopped
     counting would have drifted, not offset.
   * **`clanging_faces` expected Winnie on `SF_People1` 3**, which is now her
     granddaughter's. She is sixty and was drawn as twenty-five, and the
     recast is written up in `story.FACES` with its reason.
   * **`two_hundred` expected the same four blushes** and is correct at
     **nought**: that party has no Merribell. Which is the point - the same
     data, asserted from two states, and only one of them is wrong.

   Two real gaps came out of fixing them, and neither was a failing check:

   * **Five of Ott's six Register A moments were executed by no scenario at
     all** - two in the order chain, three in the flying chain. 2.3's own
     warning is that a counter nobody checks reads zero in the ending, and the
     ending's threshold is cut against that total, so five twenty-fifths of it
     had never once been run. `two_hundred` now walks five beats of the order
     chain and all seven of the flying chain, and asserts that the seventh
     sets `SW_OTT_MATERIALS` - which makes it the check that both ladders can
     be finished at all.
   * **A conditional blush that has only ever been run one way is
     indistinguishable from one somebody deleted.** `clanging_cast` runs Ott's
     first rung with Merribell and counts one; `two_hundred` runs it without
     her and asserts nought. Dropping the condition now fails a check in both
     directions, which is what the four-blush assertion should have been from
     the start.

   `clanging_faces` also went from ten faces to eighteen, because the town's
   cast grew by seven Cotterills and a recast and the scenario that exists to
   catch a face off-by-one was checking none of them. It is the only thing
   standing behind Rivet being moved off `SF_Actor2` 2, which reads as a girl
   at both sizes and makes what he says about sharing a bed a different line.

   Re-run: **3 of 3 in 45m04s** - `clanging_cast` 38 checks, `clanging_faces`
   18, `two_hundred` 37. The tree rebuilds byte-identical and `validate.py` is
   clean at 27 maps. **Nothing in `data/` was touched to fix any of this**;
   the three files that changed are scenarios, plus the table in `CLAUDE.md`
   that describes them.

   `../tools/scenarios.sh .` runs all thirty-three, sequentially, one line
   each, with the transcripts kept in `build/scenarios/logs/`. It was written
   for this step, and what it is really guarding is the hour: a suite run is a
   little over one, and the three ways that hour gets thrown away are all
   mechanical rather than interesting - a server on 8766 left over from another
   game, a Chromium orphaned by an earlier killed run making everything after
   it three times slower, and node's block-buffered stdout meaning a suite you
   interrupt prints nothing at all about the twenty scenarios that had already
   passed. It refuses to start on the first two and runs everything under
   `stdbuf -oL` for the third. Background it and read the logs afterwards.

   Expect any breakage to be in the **old** scenarios. Every new one here has
   been run at least once, so the interesting failure is the one in something
   nobody thought was related - which is precisely what the southern precedent
   was.

