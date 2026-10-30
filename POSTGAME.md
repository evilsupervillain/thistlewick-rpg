# The post-game - P4, a design to agree before anything is built

`QUESTS.md` P4: **the Prophecy's defeat stops being the end.** The finale's
tally plays, and then the party is back in the world, with unfinished quests
still finishable. This page settles what that world looks like, writes G1's
ending lines into the same pass (they live in the event that now hands back),
and designs the one piece of new content Mike has already placed after the
ending: **the Door into the Mountain**.

**Status: agreed by Mike, 8 Oct 2026**, with the recommendation taken on every
open question (section 11). Building starts at P4a (section 10).
Quoted lines are drafts of the *idea*. Wording is Mike's to change, and every
line gets measured against the 47/60 widths when it is built.

**Why a file of its own.** `QUESTS.md` is 4,400 lines and is read every session.
This is a design that the steps in section 9 read once each, the same split
`COMPANIONS.md` and `SITES.md` made. `QUESTS.md` P4 gets a one-line pointer here.

---

## 1. What does not move

* **No published line changes.** The finale keeps every word it has. The one
  command that has to go is the last one, **Return to Title** (command 354) after THE END. That
  is a command, not a line, and it is the whole of what "stops being the
  end" means.
* **THE END stays on screen.** It is still the end of *the Prophecy's* story.
  What follows it is the next morning.
* **The spine** (`evermore.py`'s docstring): nothing after the ending says who
  or what the villain is, connects the two horses, or says where the original
  Prophecy is or who signed it. Grimspite is still there to ask, and he does
  not know. He has never once wondered (the materials branch says so).
* **The calendar** (`TIMELINE.md` 1): Thistlewick still notices nothing. The
  post-game is the same season, a few days on. **It never reaches spring**, so
  SPA-3 and Spare's baby stay unsettled. Mrs Cotterill's "Ten in the spring"
  is still the last word on it.
  *Amended 30 Oct 2026 (Mike):* **it reaches spring for the Cotterills** -
  SPA-3 is `QUESTS.md` P4f. Spring comes when everything of Spare's is done
  and the party next wakes; only the Cotterills mark it, and Thistlewick
  still notices nothing. The ending itself still settles nothing.
* **Roland leaves at the tower door, and comes back after the ending** (Mike,
  8 Oct 2026). Before the tower he cannot be hired again, as `journey.
  guest_leaves` says: "a guest star you can re-hire after he has made his
  exit is not a guest star." Once the tower is done, the show is over and he
  is between engagements, so he can be hired again and **his unfinished quests
  can be finished**. Section 3a has the details.

## 2. The hand-back

After THE END and its wait, in place of Return to Title:

> *(fade)* The next morning there are still turnips.

The party is moved to Bram's house (Map 2) and keeps its line-up, kit and
levels. Two things change on that move. `SW_WON` is already on, so every
post-game page below can key on it. And **the player can save from here on**,
which no save file has ever been able to do.

**All four finale pages get this.** Pages 0 and 1 are the finale (with and
without ITEM 1's scene), and pages 3 and 4 are the same two with the Former
Premises' signature spliced in. The tally is built four times, so the G1 lines
(section 7) and the hand-back go into all four, from one function. Pages 2 and 5
stay empty. A new **page 6** on `SW_WON` beats them both and is Grimspite
afterwards (section 3). That puts `finale_ending` and `premises` both in scope.

## 3. The tower afterwards

**The tower stays exactly as it is, and Grimspite stays in it.** He has lived
there for four thousand eight hundred years and has nowhere else in the
world. Nothing renews him now, so he sits down. Page 6 is him in the chair
with the book open at the bookmark:

> **Grimspite:** Forty-eight. Nobody's ever come back up.
> There's a kettle on, if you want one.
> *[Have a cup / Not just now]*
> *Have a cup* - It is just tea. / **Grimspite:** There. Now somebody has.
> *Not just now* - **Grimspite:** Halbert said that. It's all right. The
> kettle's always on now.

That is the tea Halbert Quy turned down thirty years ago, offered to the next
man up the stairs. The wall keeps its forty-seven carvings, and one look says
so: *"There is room for a forty-eighth. Nobody is going to need it."* The
monsters on the way up stay where they are, because the tower has always had
them.

**Maud** (ROL-5) said she would wait at the door and then "go and tell him how
it ends". In the post-game she has gone, so her splice at the tower door gets
a `SW_WON` guard and the door shows nothing.

## 3a. Roland, between engagements

He is back at his table in the Slain Wyvern. A new top page on `SW_WON` sits
above the "gone" page and leaves it as it is. His recruit pitch is new, because
the published one is about being asked a twelfth time:

> **Roland:** Finished? Marvellous. I've never been
> in the bit after. Is it nice?

If ROL-5 is done, he has heard how it ends from Maud, and her question still
goes unanswered.

* **The recruit is the same `story.recruit` shape, keyed on `SW_KNOWN`**, so
  there is no second initialise. He comes back at the level he left at.
  `guest_leaves` handed his gear to the party at the door, so **he rejoins
  carrying whatever he had on when he was removed**. The build checks what that
  is. If it is nothing, his page puts his armour back on by script, and the
  swords stay with whoever has them now.
* **`SW_ROLAND_GONE` stays on.** The tally reads it, and so does Hob's ROL-4
  refit page. The switch records that he left at the door, not that he is
  away now. Before building, every Roland quest page is checked for anything
  that assumes "gone" means "not in the party". Those pages already gate on
  `actorValid`, so most will simply work.
* **His departure scene cannot run again.** It is gated on him being in the
  party at the tower door, and `SW_ROLAND_GONE` is already on. The build adds
  a guard on that switch, so that walking back up the tower with him rehired
  does not make him leave a second time.
* The roster desks can strike him off and take him back like anybody else.

## 4. Thistlewick's lines

The gradient decides the tone (`TIMELINE.md` 1, "Who notices"). Thistlewick
holds both at once and never notices, so it is **delighted, proud, and very
keen that Bram should enjoy the coast.** It is the oldest habit in the
expansion: a returning hero is an awkward thing to have about the place
(`EXPANSION.md` 1). Nobody says so. Everybody is lovely about it.

* **The letter on the mat** (the first post-game event, in Map 2):
  > PROPHECY OF THISTLEWICK - CLAUSE NINETEEN
  > With the Committee's congratulations on your return.
  > Enclosed: your pension, and the key to a cottage at
  > Nether Sopping, at such distance as is mutually agreeable.
  > We trust Friday will suit.

  "Ready by the Friday" is what happened to Quy. A player who has met him gets
  the joke, and one who hasn't still gets a perfectly good letter.
* **About six villagers get an appended page each**, keyed on `SW_WON`. Each
  is one short exchange in which they ask after his health, admire the Receipt
  and mention the sea air. **The rule in `QUESTS.md` 0.2 still applies**: a
  page goes only on someone whose ladder has a terminal switch the post-game
  can wait on. Anyone else gets a new event or goes without. The Committee
  Chair, the Gilded Turnip and the Old Man are the obvious three. Mike has
  the last word on the Old Man, whose boy was the Forty-Seventh, and the safe
  version of his page is a short one.
* **The Wall of the Forty-Seven** gets a forty-eighth portrait frame, empty,
  with a card: *"Portrait to follow. Sitter at the coast."*
* **"SEE BRAM"** is in the tally, so the clause-twelve note exists. Anyone who
  checks the Committee's records reads it in the minute book, on a new page.

## 5. The pension and the place in Nether Sopping

**Both happen.** Clause nineteen is still in force in the post-game. The tally
says Thistlewick struck it six months later, and only if Bram met Quy, so for
now it simply applies.

* **The pension** comes with the letter: one quarter in advance, as gold,
  paid once. A payment that kept coming would be an income in a game whose
  shops are tuned for the main quest.
* **The cottage is Ambrose Fitch's.** Fitch was pensioned south, died about
  1999 (`TIMELINE.md` 3), and Nether Sopping already has a shut door that
  fits: *"Somebody's front door. There is a boot scraper, and a pot with a dead
  thing in it, and no answer."* (`south.py`, shut door 15). The published page
  stays first. A new page on the key opens it onto a new one-room interior
  (map 71), with a bed that rests the party for free, Fitch's chair facing the
  window, and the dead thing in the pot, which Bram can water. Nothing grows.
  Nothing says it will. Ysolde can get one appended line once Bram has been in.
* **The old woman behind that door** (Mike, 8 Oct 2026). NIX-3 already has her
  open it an inch and give Nix the pot ("Keep the dead thing an' all"). She is
  **Mrs Pimm, who has the other key**: she has aired Fitch's place since he
  died and was in it when Nix knocked. The cottage is empty; she never
  appears; her note on the table says so. Not "next door": the house to the
  west is Number Forty-Five's, Halbert Quy's.
* **Bram does not have to live there.** His own house is still his, and the
  letter says "mutually". The cottage is a free inn in the south and a door
  the town finally opens. It is not a relocation.

## 6. Is the Prophecy really over?

**Yes. The post-game must not reopen it.** The ending's last line is "There
isn't a forty-nine", and the whole game has been building to that. A successor
prophecy, a surviving clause or a sting in the tail would turn Grimspite's
"admin problem" into a cliffhanger, and would invite somebody to explain the
horse. What the post-game *can* show is the people the contract used to own:

* **Grimspite**, retired, with a kettle (section 3).
* **Hollowell**, the contract's own staff at the Former Premises. He is the one
  person in the world who would notice it ending, and noticing is what he does.
  He gets one airship-only page: the notice of termination came in the post,
  and he has filed it, and he has nothing else to file. Optional; Mike's call.
* **Halbert Quy** (on `SW_MET_QUY` and `SW_WON`). The tally already says what
  happens: "He had walked down and told him what Grimspite said, all of it, in
  order, including the part about the tea. It took most of an afternoon." So
  the post-game lets the player do exactly that, and the scene is one fade:
  *"You tell him all of it. It takes most of an afternoon."* If Bram had the
  cup (section 3), Quy asks one question, *"What was it like?"*, and is told
  it was just tea. **This is the one post-game scene that has to agree with
  the tally word for word**, because the tally has already narrated it.

## 7. G1's ending lines

The plan stays the same: one block per companion and one closing count. **One
change is needed to make it work.** Each candidate line belongs to one quest,
so a block keyed on `SW_<NAME>_STORY` alone cannot know which line to print.
Each companion's block is therefore an `if/else` chain over that companion's
quest switches, best line first. The first one done prints, and exactly one
line per companion ever appears. The headline picks:

| who | chain, headline first | the headline |
| --- | --- | --- |
| Merribell | MER-1, MER-4, MER-5, MER-3, MER-2 | The Order of Whatever Works... It is four lines long. |
| Hob | HOB-1, HOB-4, HOB-2, HOB-5, HOB-3 | ...a hammer called Beatrice... she is right about everything. |
| Zephyrine | ZEPH-2, ZEPH-1 (paid / expelled), ZEPH-4, ZEPH-3, ZEPH-5 | ...the duck... She has not yet used it. She is saving it. |
| Nix | NIX-1, NIX-4, NIX-3, NIX-5, NIX-2 | The client has been identified... and the coat fits. |
| Aldric | ALD-2, ALD-5, ALD-4, ALD-3, ALD-1, ALD-6 | ...looking back, to see who is behind him. Somebody always is. |
| Piper | PIP-4, PIP-1 (good / fixed), PIP-3, PIP-2, PIP-5 | ...nine lines by Piper Quill... He walks it still. |
| Corvin | COR-1, COR-2, COR-4, COR-3, COR-5 | ...a scarf in the wrong colour, and he wears it. |
| Wren | WRE-1, WRE-5, WRE-3, WRE-4 | ...three reviewers, one of them a duck. Page four hundred says goose. |
| Roland | ROL-2, ROL-4, ROL-3, ROL-1 | ...He asked to be surprised. Everybody was. |
| Spare | SPA-2, SPA-4, SPA-1 | ...Somebody was there when he came out. |

The full texts are the Done paragraphs' "Candidate ending line" bullets, used
as written.

* **PIP-5 goes last in Piper's chain** because its `\V[7]` repeats the struck
  verses count, which the tally already prints two blocks earlier.
* **ROL-5 is not in Roland's chain.** It is a splice after "...who thinks about
  this one" inside the `SW_ROLAND_GONE` block, which is where its candidate
  says it goes. It puts a second Roland line into an ending that has room for
  one, so **Mike: keep it or drop it.** I would keep it. It is the reason Maud
  exists.
* **Placement.** The companion lines go after the Firstfield block and before
  "Thistlewick struck clause twelve...". Clause twelve and the walk to Quy stay
  the last words. It is an insertion, and no published line moves its wording.
* **The closing count** on `VAR_COMPANION_STORIES`, after the ten. Nothing
  prints at 0. At 1: "One of them got something out of it as well." At 2-9:
  "\V[15] of them got something out of it as well." At 10: "All ten of them
  got something out of it as well."

## 8. Does an ending tally still make sense?

**Yes, as the account of the day it was written.** The tally is a flash-forward
in the past tense, "six months later" and "Nobody has needed to yet", so it
reads as the record made at the end of the Prophecy and not as a final score.
Two things keep it honest once the game goes on:

* **The official account can be read again.** Prophecy Hall gets a lectern
  with *"THE OBLIGATORY QUEST, as amended"*. Reading it plays the tally against
  the current state, so a quest finished in the post-game shows up there.
  **It is built by the same Python function as the finale's tally**, so the two
  cannot drift. PIP-1's "official account" is already set in Prophecy Hall,
  which makes this the natural place for it.
* **The counter thresholds are about the finale moment.** G1 re-cuts them
  against what can be reached *before* the ending. Tropes and blushes found in
  the post-game count only in the amended account. The comment above both
  branches says so.

## 9. The Door into the Mountain

The game has already fixed what goes in (`COMPANIONS.md` 8): the board says NO
ADMITTANCE WITHOUT A LAMP, the hook is empty, and Sir Dunstable borrowed the
lamp ("Back directly. - D."). He comes in at a quarter past four, and the Book
is his name all the way down. **It stays unsettled whether he is alive.**

**The lamp.** Dunstable gets a post-game page on `SW_WON`. He would never have
offered before: a man with an appointment is not to be detained.

> **Sir Dunstable:** The Forty-Eighth! Free afternoon now, I
> expect? Then you'll want the lamp.
> Wouldn't have dreamt of it before. Man with an
> appointment. Not done.
> Back directly, there's a good fellow. I go in at
> a quarter past four.

The gate is natural: what kept the door shut was always manners, and the
ending is when the manners stop applying. The lamp is item 75, a key item.
**The door gets a new page on the item and transfers.** The published refusal
stays exactly as it is for everyone without the lamp.

**Behind the door: the Stair.** "A stair going down into a dark that does not
stop." The proposal:

* **A descent of about five maps** (ids from 71, after the cottage). Outside
  the lamp's light it is dark, done the way SPA-2's culvert and ROL-2's cave
  already do it. The party walks inside a small circle of light. These are
  the hardest regular fights in the game, tuned with `balance.py` above
  Fitch's barrow, which is currently the hardest optional fight.
* **Dunstable's chalk marks.** Down the walls run "D." marks, each one a little
  further down than the last, a hundred-odd of them. The deepest is
  **"D. 212"**. Past it, nobody has been.
* **Continuance, mechanically** (agreed with Mike, 8 Oct 2026: allowed
  because the plot expects it). If the party falls in the mountain, there is
  no Game Over. They come back in through the chapel porch, with the Book open,
  and Brother Quillon says nothing with enormous tact. That is the chapel's
  name, the Book's purpose and Dunstable's whole story, done to the player.
  It still settles nothing about Dunstable, because the player also "comes
  back" and the game never says the player died.
  * **Why only here.** The world ties this to one place. The chapel stands
    beside the only door into the mountain, and the people who come back in
    through its porch are the people who went through that door. Nowhere else
    in the game makes that promise, so a defeat anywhere else is still Game
    Over.
  * **Whether or not the party signed the Book** (Mike, 8 Oct 2026, on the
    fence and for now). The promise belongs to the door and the porch, not to
    the signature. If only people who signed came back, the Book would be the
    mechanism, and the game would have explained what it was careful to leave
    open: the bio only says that people sign "in case of misfortune" and
    "quite often" come back. It would also hide a Game Over behind an
    optional save point. Dunstable's "Signed the Book? Just in case." stays,
    as character and not as a rule. A party that never signed comes in
    through the porch to Quillon's first-visit page, and he does not react to
    them arriving from the wrong side. Requiring the signature was considered
    and set aside. To change it later, put a switch on the Book's "write"
    choice and test it in the override.
  * **What it costs.** The party comes back fully restored, as at the Vigil and
    the Worm, and keeps the lamp, its items and its gold. The price is the walk
    back down. Quillon's reaction is whichever of his published pages is due,
    reused unchanged, plus at most one new silent beat. Nothing about it
    explains.
  * **Scripted fights** in the mountain, the bottom included, use the pattern
    the game already has: "can lose" on, and a lose branch that sends the
    party back through the porch. That is the same as the Vigil, the Worm and
    Norbert, and needs no engine change.
  * **Random encounters** have no event to put a lose branch in, so they need
    a small plugin override of the defeat path, active only while a switch is
    on, and the switch is on only in the mountain maps. It is the first random encounter anywhere in the game that
    does not end in Game Over. A scenario tests it both ways: a defeat on the
    stair comes back through the porch, and a defeat on the world map is still
    Game Over.
* **At the bottom, the dark stops.** That is the punchline the line has always
  had. **What is there is the decision for Mike.** Three options:
  * **(a) Something Unscheduled** - *my recommendation.* The only monster in the
    world that is in no prophecy, contract, clause or form. Nobody was ever
    obliged to come down for it, so nobody did. It is thrilled to see them. It
    is the post-game's superboss and is very hard. Afterwards it says thank
    you, and means it differently from Grimspite. It is a fight with no
    paperwork, in a game where every fight had some. It touches no part of the
    spine.
  * **(b) The far side.** The stair comes out in daylight on the other side of
    the mountain. Dunstable has been having his tea there at a quarter past
    four, every day, for two hundred and twelve days, because nothing ever
    happens. That is gentler and funnier, and has no fight at the end.
  * **(c) Something older than the Third Age.** The mountain is the obvious
    place for it. `TIMELINE.md` 6 says only Mike may decide what began the
    Age, so I am listing it only to say I won't propose it.
* **Art.** The superboss under (a) is a stock monster first and goes on
  `AUDIT.md` item 1 for real art, the same as every other enemy without its
  own picture.

## 10. Build order, once agreed

Each step follows `QUESTS.md` 0.1: build, `git diff --stat data/`, old pages
compared byte for byte, `validate.py`, `apidigest.py`, screenshots, and only
the scenarios the step reaches.

* **P4a - the hand-back and G1's lines** (**done**, 8 Oct 2026; `QUESTS.md`
  section 3). Pages 0, 1, 3 and 4: the companion
  chains, the closing count, the ROL-5 splice, and "The next morning..." with
  the transfer in place of Return to Title. Then page 6, Grimspite and the kettle,
  and Maud's guard. Scenarios: `finale_ending` (extended to assert each chain
  and the hand-back) and `premises`. Their old endings assert the title
  scene and will change. The new tropes are counted here, and the counter
  re-cut stays in G1.
* **P4b - Thistlewick and the pension** (**done**, 8 Oct 2026; `QUESTS.md`
  section 3). The letter, the villagers' pages, the
  empty frame, the minute book, the cottage (map 71) and Fitch's door, and
  Ysolde's line. Roland's page in the Slain Wyvern and the guard on his
  departure (section 3a), with a new `pg_roland` that rehires him, walks him
  up the tower, and starts one of his undone quests. Scenarios: whatever already walks Maps 1-7 and 13,
  chosen as `QUESTS.md` 0.1 says, plus a new `pg_home`.
* **P4c - the amended account, Quy and Hollowell** (**done**, 28 Oct 2026;
  `QUESTS.md` section 3). The lectern in Prophecy
  Hall, built from the tally's function. Quy's afternoon and Hollowell's notice.
  Scenarios: a new `pg_account`, plus `premises` again for Hollowell.
* **P4d - the lamp, the Door, the Stair and continuance** (**done**, 28 Oct
  2026; `QUESTS.md` section 3). Dunstable's lamp, the Door's pages, Maps 73-77
  with the chalk marks, the schedule and the warden, the lamplight and the
  continuance plugin (`js/plugins/TOQ_Mountain.js`, keyed by map-note tags
  rather than a switch). Scenarios: a new `pg_mountain`, and `hithermost`.
* **P4e - the bottom** (**done**, 29 Oct 2026; `QUESTS.md` section 3). Past
  D. 212 on Map 77: Something Unscheduled, item six on the schedule, and its
  line in the account. Map 78. **Agreed in full, section 12** (29 Oct 2026):
  the build brief. Built from it as written, but with two deviations: 30,000 HP
  where the brief said about 36,000 (the Monte Carlo is in the Done
  paragraph), and the chamber's size.
* **G0, the quest log**, adds the post-game quests (the letter, the cottage,
  Quy, the lamp, the Stair, and the bottom with Form Z) to `quests.py`. **G1** then does only the re-cut,
  the suite, Mike's playthrough, and the push.

**Ids** (next free): switches from 214, item 75 (lamp) and 76 (cottage key),
maps from 71, common event 7 (the continuance hand-back, if it is one). No new
variable is needed, so `build_game.py`'s list stays at 33.

## 11. Decided (Mike, 8 Oct 2026)

Mike agreed the draft as written, so each question below took the
recommendation:

1. **The shape** in sections 2-6, as written.
2. **Roland** leaves at the door and can be hired again after the tower
   (section 3a). Mike asked for this. His first post-game line is a draft.
3. **ROL-5's line** stays, as a second Roland line, spliced into the
   `SW_ROLAND_GONE` block.
4. **The G1 chains** in section 7, as tabled.
5. **Hollowell's page** is in.
6. **The bottom of the Stair** is (a), Something Unscheduled.
7. **Continuance replaces Game Over** in the mountain, because the plot
   expects it, whether or not the party signed the Book (section 9).
8. **This file** stays `POSTGAME.md`, and `QUESTS.md` P4 points here.

Still open from before and not part of P4 unless Mike says so: the value1/value2
turn count on every buff and debuff in `db.py`, and whether P2's "shield
standing in for a sign" meant the crest sign outside the Guild.

## 12. P4e, the bottom - agreed (Mike, 29 Oct 2026)

Option (a) of section 9, with its open questions answered. This section is
the whole brief for P4e; the draft lines below are approved as written
(Mike: "they work"), and anything new beyond them is still new writing.

**Map 78, the Bottom** (`mountain.py`, `places.MAP_STAIR` stays the five;
add `MAP_BOTTOM = 78`). Map 77's "d" (28, 48) stops being "You turn back.
Not yet." and becomes a way down, the same `_way` the other maps use; the
old page's text is P4d's and was never pushed, so it can go. One more flight
down, then a chamber that is **lit**: lamps on every ledge, dozens, all
burning, because it has been getting ready for company. The note is
`<continuance>` only - no `<lamplight>` - so the dark stops, and a lost
fight still goes to the porch. Same rock-cave family and `_plan` idiom as
73-77 (it can be a plan in `PLANS`'s style but outside the list, or the list
grown with care: `stair_map`, `ENCOUNTERS`, `BGS`, `NAMES` and `_ways` all
index by it). No random encounters on Map 78. Register the map in
`build_game.MAP_NAMES` and the build, as P4d did.

**Something Unscheduled.** Stock `Kraken` battler (big-eyed octopus; looks
pleased to see you). Map sprite: whatever stock character reads as large and
friendly, or `Monster`; check with a shot. Enemy 65, troop 61, skills from
191: three or four with eager names, heavy hits spread across the party so
the healer is busy. About **36,000 HP**, roughly ten turns for
`balance.py`'s strong four at level 25 (Prophecy 9,000, Grimspite 7,000,
warden 4,400); tune with a Monte Carlo of the engine's rules as PIP-3's was
(`QUESTS.md`, the P1 Done paragraph), not by `balance.py` alone. Can lose;
the lose branch calls `CE_CONTINUANCE`, exactly as `mountain._warden` does.
Can't escape.

**The draft lines** (approved):

> The stair ends. The dark stops all at once, like a door shutting behind
> you. Lamps, dozens of them, on every ledge, and every one is lit.
> **Something Unscheduled:** OH. Oh! Visitors! Come in, come in!
> I'm not on anything. I asked. Not in the Prophecy, not on the board.
> Item six.
> Nobody is obliged to fight me. So nobody ever has. ...Would you? Only if
> you've got the afternoon.
> *(Fight / Not today)*
> After winning: ...Thank you. That was the best afternoon I've ever had.
> Nobody made you.

Break them to the 47/60-character widths with `S.say`; a trope on the first
meeting (self switch, once). Its thank-you is for a *visit*, Grimspite's
(`journey.py`, "...Thank you.") was for an *ending*; keep them apart.

**Rematch: yes** (Mike). After a win, every later visit it asks "Again?"
(Fight / Not today). No second bounty card.

**The way home: it takes you up** (Mike). After every win - and on "Not
today" too is a sensible choice, decide when writing - it sees the party up:
fade, transfer to Hithermost's `mountain.DOOR_STEP` (17, 6) on Map 33.

**The schedule board** inside the Door (Map 73, `mountain.schedule()`): once
it is beaten, a new page above the old shows the same board with a chalk
line beside item six in the party's hand - "Anticipated." (not "- D.":
Dunstable never got this far, and nothing may settle him). P4d is unpushed,
so this is free to change.

**The keepsake is paperwork** (Mike's idea, the design below agreed):

* After the first win it shyly hands over a card it has kept ready a very
  long time - a bounty it wrote on itself:
  `BOUNTY: SOMETHING UNSCHEDULED / Lives at the bottom of the Stair. Would
  love to meet you. / Reward: on production of a witness.`
* The contradiction is the joke. Narrated, the game's idiom for the party:
  "You point out that it said it wasn't on anything." It: "I'm not! Nobody
  would put me on anything. So I did it myself." / "It isn't official. It
  wants a stamp. ...I didn't know where you'd get one." It is still in no
  prophecy, contract or schedule; needing to write its own card is the proof.
* **Registrar Pell** at the Guild (Map 15, `south.pell_event`, event 2;
  pages: intro, unregistered on `SW_GUILD_ASKED`, member on
  `SW_GUILD_MEMBER`). A new page appended on the member switch **and** the
  card item: he examines it, for some time. Nobody issued it; no authority;
  there is no form for this. Then, after a pause: there is. He has kept it
  forty years in case - **Form Z, Matters Not Anticipated** (item six of the
  Stair's schedule, at the other end of the paperwork). Never used. He is
  quietly as thrilled as the monster was. He stamps the card DISCHARGED and
  gives it back, and takes the Guild Card (Provisional) and hands back one
  without "(Provisional)". That is the whole reward - every other bounty
  paid gold; this one pays in status, which Pell regards as the larger sum.
  The page must still offer the member page's roster amendment afterwards
  (or be followed by a page that does), because it shadows that page.
* **Unregistered party**: the unregistered page is untouched, so the card
  waits; Pell, if it needs a line, says a bounty is claimed by a member.
* **The bounty board** (Map 15 event 3, `south.bounty_board`): published
  page 2 reads "Two cards. There are usually two cards." A page appended on
  the stamped switch: "Three cards. There are usually two." The third is a
  copy, pinned up, stamped DISCHARGED; the crab and Crooke choices as before.
* `VAR_BOUNTIES` is **not** bumped: the finale's numbers are the ending
  moment's (section 8).
* The Guild Card (item 27, `db.IT_GUILD_CARD`) is checked nowhere but its own
  gain in `pell_event` - membership is `SW_GUILD_MEMBER` - so swapping it for
  a new item is safe; grep again before doing it.

**The account** (`mountain.account_lines()`, after the Stair's three): on
the beaten switch, "Something Unscheduled was met at the bottom of the
Stair, and fought, because nobody had to." and, on the stamped switch, "Its
bounty was discharged on Form Z." (wrap to width; extend `pg_account`).

**Ids:** switch 222 `SW_UNSCHEDULED` (beaten), 223 `SW_FORM_Z` (stamped);
first meeting is a self switch. Items: 77 the card as handed over
("Bounty (Something Unscheduled)"), 78 the same card stamped ("Bounty,
Discharged"), swapped by Pell - an item's description cannot change, so it
is two items - and 79 "Guild Card", swapped for 27. All key items. Enemy 65,
troop 61, skills 191+, map 78. Grep `db.py` for every new constant name
before using it. Variables: none needed.

**Also in P4e:** `AUDIT.md` item 1 (enemy art) gains the six mountain
enemies - P4d's five (The Dark, The Draught, The Echo, Somebody Coming Up,
the Half-Way Warden) were meant to go on it and did not - and Something
Unscheduled.

**Scenario `pg_bottom`:** from Map 77 down to 78; the meeting (trope once);
"Not today"; the fight won (set the troop dead as `q_ald2`/E18 do) - the
switch, the card, the ride up to (17, 6) on Map 33; a rematch offered with
no second card; a fight lost going to the porch (Map 34, wait on "You come
back in through the porch."); the schedule's new page; Pell stamping
(card swapped, Guild Card swapped, switch 223); the board's third card; the
account's two lines. Rerun `pg_mountain` (Map 77 changed), `pg_account`,
and whatever walks the Guild (`guild` and any scenario touching Map 15:
grep `scenarios/` for `15,`).
