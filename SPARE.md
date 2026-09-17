# Spare

*A proposal, not a specification. Nothing below is built. `NORTH.md` section 1
is still the law for every line of it.*

The tenth companion, and the only secret one: **Spare Cotterill, aged nine**,
who has had a bag packed for two years and has been told he cannot come by
every Chosen One who has walked up that street. He can come. It takes work, it
takes a free seat, and it takes getting past his mother, who is right.

---

## 0. The shape of it

1. Hear everything Spare has to say (his four beats).
2. Meet all nine Cotterills, who are scattered across five maps.
3. Have the airship, because that is the only answer to "he would be walking".
4. Get **Form P-9** out of Gudgeon at the Parish Rooms - the parish has a form
   for this, because the parish has a form for everything.
5. Come back with a seat free. Ask him again, and this time he answers.
6. Say yes, and then argue with his mother, which the engine renders as a
   fight because a fight is the only verb this world has.
7. Win, and he joins - late, over-powered, and permanent. He does not leave at
   the tower door. That is Roland's job and Roland is contractually obliged.

Everything here is additive under 1.7: new events, appended pages, and one new
`if_then` block in the ending's tally. **Not one existing line is touched.**

---

## 1. Unlocking him

### The seven candidates

**A. His own ladder, heard out.** He has four beats and the fourth repeats
forever. `ladder()` chains self switches A-B-C, so `$gameSelfSwitches.value(
[MAP_CLANGING, 13, "C"])` is true exactly when the first three have been heard
and the fourth is what he says now. **Costs nothing and edits nothing** - the
state is already being recorded, it has simply never been read by anybody else.

**B. All nine Cotterills met.** Mrs Cotterill, Mr Cotterill, Spare, Ferrule,
Clevis, Shim and Bessie on the street; Rivet in the Safety Valve; Gudgeon at
the Parish Rooms; Tappet in the works; Grommet at the forge. Every one of them
is a `talker()`, and a `talker()` sets self switch A the first time it is heard,
so this too is nine script reads and zero edits. The argument for it is the
whole point of the thing: **you do not take a child out of a family you have
not met.**

**C. The airship flies** (`SW_AIRSHIP`), or better, **has flown somewhere real**
(`SW_TWO_HUNDRED_FLEW`). This is the answer to the only objection his mother
cannot be talked out of. A nine-year-old does not walk to the Obligatory Tower
through the Gloamwood. A nine-year-old can be *flown* there and flown back.
It also puts him where he belongs in the game's shape: after the north's main
quest, as its last reward.

**D. Form P-9, issued by Gudgeon.** This game's own machinery - Form A-1 at the
Guild, Form C-12 with the clerk, Form C-12(S) with Pell. Gudgeon is twenty, she
clerks at the Parish Rooms, and she is Spare's sister. She has never issued one.
She knows exactly where it is. *Application by a Minor to Accompany a Chosen One
(Parish of Upper Clanging).* It needs a signature from a parent or guardian,
which is the joke and also the plot: the form is why there has to be a fight.
**This is the criterion that turns a checklist into an errand**, and it is where
conditions A and B are actually tested - Gudgeon will not go and look for it
until you have met her family and heard her brother out.

**E. Attempt Eighty-Four rebuilt** (`SW_84_REBUILT`). Thematically the best of
the lot: you are the sort of person who does not scrap a thing that still wants
to go. It is also an optional side quest, so requiring it gates a secret
character behind another secret. **Recommended as a soft extra**, not a hard
gate - see below.

**F. Shim's washer.** Shim, eleven, has a tin, and said "I said he can have a
washer." A new appended page on Shim once `SW_SPARE_ASKED` lets you ask for it,
and you carry it. It is a key item that does nothing. It is in the bag at the
end of the conversation, and it is on the character sheet forever after as an
accessory. **Recommended, as flavour rather than as a gate.**

**G. A level requirement.** Cheap, mechanical, says nothing about anybody.
**Not recommended.** Every other condition on this list is a sentence about who
Bram has become; this one is a number.

### The recommendation

Hard conditions, all four: **A + B + C + D.** Free seat checked at the moment of
asking, exactly as `story.recruit` already does it - because whether there is
room changes while the player is standing there.

`SW_84_REBUILT` (E) does not gate the conversation; it changes **one window
inside it**. If you rebuilt Eighty-Four, Mrs Cotterill has heard about it before
you open your mouth, and the argument starts one notch further along. That is
better than a gate: it rewards the player who did it and costs the player who
did not exactly nothing.

Shim's washer (F) is carried, not required, and is what she takes out of the bag.

### What it costs

| new | what |
| --- | --- |
| Switch 72 | `SW_SPARE_FORM` - Gudgeon has issued Form P-9 |
| Switch 73 | `SW_SPARE_JOINED` - he is coming. Also `SW_RECRUIT[SPARE]` |
| Switch 74 | `SW_SPARE_REFUSED` - the argument has been lost at least once |
| Item 33 | Form P-9 (key item) |
| Item 34 | A Washer, Off Shim (key item, until it becomes armour 27) |
| pages | one appended to Gudgeon, one to Shim, two appended to Spare |
| events | none. Every condition is read off state that already exists |

---

## 2. The conversation

Appended page on Spare Cotterill (Map 21, event 13), conditioned on
`SW_SPARE_FORM`. Every line below has been through `story.say`'s width check
and fits the window.

### He asks again, and this time he has an answer ready

    Spare: Can I come yet?

    He asks it the way he has asked it every day.
    Then he does something he has not done before.
    He puts the bag down.

    Spare: I have thought about your reasons.
           You said I am nine. I said I am nine in a
           useful way. You did not ask what that means.

    You ask what it means.

    Spare: The boiler has ninety tubes in it.
           They have to be brushed. A man does not fit.
           I fit.

    Spare: I have been going in since I was six.
           Miss Hoyle pays me in buns.
           I have never once been frightened.

    He considers this.

    Spare: I have been frightened. Not of the dark.
           Of coming out and nobody being there.
           There is always somebody there.

    Spare: In the spring there will be ten of us.
           I will not be the littlest one any more.

    Spare: I am not sad about it. I have had nine
           years of being the littlest and it is a
           very good job.

    Spare: I would just like to have done one thing
           first.

    You ask what is in the bag.

    Spare: A jumper. A tin. A washer off Shim.
           There was bread. There is not now.

    Spare: And a drawing of the Two Hundred.
           With me on it.

    He does not show you the drawing.
    He tells you the drawing is in there, which is
    not the same thing, and is worse.

**Why it works.** He never asks to be a hero and he is never once unhappy - 1.5's
second test. "Nine in a useful way" has been sitting unexplained in the finished
game since the town was built, and this is the game paying it off: he is nine in
a useful way because he is the only person in Upper Clanging small enough to get
inside a boiler, which is true, is period, and is why every one of his skills
later is a thing a small person can do that a large one cannot. And the turn is
not the boiler. The turn is a drawing he will not show you.

*(Optional window, only with `SW_84_REBUILT`, inserted before the bag:*

    Spare: You mended the one in the field.
           Everyone said scrap her.
           You did not say scrap her.

*)*

### The choice

    > Come with me
    > Not yet

**Not yet** - and this is the one that must not be sad:

    Spare: Right.

    He takes it extremely well.
    He picks the bag back up.

**No room** - the `$gameParty.size() < 4` branch, in his voice rather than the
game's:

    Spare: You have got three already.
    Spare: I will wait. I am extremely good at it.

### Mam

    Mrs Cotterill has been standing behind you.
    You do not know for how long.

    Mrs Cotterill: No.

    Mrs Cotterill: I have had him out of a boiler.
                   Nine times. And out of a flue, and a
                   culvert, and a drain we do not discuss.

    Mrs Cotterill: Every time, he came out.
                   Every time, I was there.

    Mrs Cotterill: You are going to a tower that
                   eats the people who go to it.
                   I would not be there.

    Spare: Mam.

    Mrs Cotterill: No, love.

    Spare: Then I will have to change your mind.

    You have seen this before. Somebody wants a
    thing, somebody else says no, and a fight
    starts. It is the only way anyone in this
    world has ever settled anything.

                                        [story.trope()]

    Nobody raises a hand to anybody.
    It is an argument. It is simply that up here
    an argument is a serious piece of work.

**Her objection has to be the right one and it has to be unanswerable**, or the
scene is about a woman being wrong for ten minutes. Hers is: *I have always been
the one who was there when he came out.* You cannot argue with that. Spare does
not argue with it. He changes it.

### She concedes

Played on the map after the fight, not in the battle scene, because the faces
and the doorstep are here and only her battler is there.

    She stops. Not because she is tired.
    Because he has not.

    Mrs Cotterill: Nine years, and you have never
                   once let a thing go.
                   I do not know where you get it.

    Mr Cotterill: Mam.

    Mrs Cotterill: I know.

    She picks the bag up and looks in it.
    She takes out the drawing and looks at that,
    for rather longer, and puts it back.

    Mrs Cotterill: Right. Terms.

    Mrs Cotterill: Jumper on.
                   You do not go in first.
                   You write. It does not have to be long,
                   and it does not have to be true.

    Spare: Yes, Mam.

    Mrs Cotterill: And you.

    She hands you the bag.

    Mrs Cotterill: Bring him back.

                                    Spare joined the party!

**"I do not know where you get it"** is the whole scene, and it is a joke about a
marriage told without one word about the marriage - she knows exactly where he
gets it, and so does Mr Cotterill, which is why he says "Mam" and she says "I
know". It is Register B and it is not a blush; it does not bump the counter.

### She does not

    It is not close.

    Spare: I nearly had you.

    Mrs Cotterill: You did not.

    Mrs Cotterill: Tea is at six. Wash your hands.

    He takes it extremely well.
    He does not put the bag down.

`SW_SPARE_REFUSED` goes on, no self switch is set, and you can come back and try
again tomorrow, which is what a nine-year-old would do.

---

## 3. The fight: whose fight is it

**Recommendation: Spare fights alone.** The other version - your party of four
beating up a pregnant woman on her own doorstep for custody of her son - is
twenty minutes of work and is the wrong scene in every register the document
has. Spare alone is the funnier answer, the truer one, and it is the one where
the player is not doing anything they would be embarrassed to explain.

It is also **entirely achievable**, and here is exactly how, all of it checked
against `js/rmmz_*.js` in this project:

* `Game_Party.allMembers()` maps `this._actors`, and `battleMembers()` is
  `allMembers().slice(0, 4)`. **Everything the battle scene knows about who is
  fighting comes from that one array.** So: stash it in `$gameTemp`, set it to
  `[SPARE]`, `$gamePlayer.refresh()`, fight, restore, refresh again. Six lines
  of Script command and no plugin.
* He must be set up first - `$gameActors.actor(SPARE).setup(SPARE)` - and
  levelled to a **fixed** level for the argument rather than to the party's, so
  the fight can be tuned once with `balance.py` and stay tuned. He is levelled
  up to the party when he actually joins.
* Restore the party **after** the win/lose branches, not inside them, so it
  happens on every path.
* He is not a party member while this is happening, so losing costs nothing and
  leaves nothing behind to clean up.

**And the joke pays forward.** Do not write a separate set of persuasion skills
for the argument. Write his **real** skills, and fight the argument with them.
Every skill Spare has for the rest of the game is a thing he tried on his
mother, which means every time he uses one in a real fight the player remembers
where he learned it. Temper Tantrum is in his list at level 99. It has never
worked on her. It works alarmingly well on a skeleton.

### Her side of it

Enemy 28, `Mrs Cotterill`. Skills 146-149, which is the free end of the northern
boss block:

| id | skill | what it does |
| --- | --- | --- |
| 146 | **You Are Nine** | The unanswerable one. Heavy, and she opens with it. |
| 147 | **Ask Your Father** | She defers. Does nothing to him at all and restores her position, because a deferred question is a question you have not lost. |
| 148 | **That Is Not The Point** | Strips every buff and state he has put up. He was doing so well. |
| 149 | **I Have Said No** | Her last resort, below half. It is not louder. It is quieter. |

She should **not** be a damage race. She should be a war of attrition that he
wins by still being there, because that is what the concession says about him.

---

## 4. Nobody dies, and nobody gets a Game Over

Both are stock engine features. Verified in this project's `js/`:

**No Game Over.** Battle Processing's fourth parameter is `canLose`.
`BattleManager.processDefeat` skips the audio kill when it is set, and
`updateBattleEnd` calls `$gameParty.reviveBattleMembers()` and `SceneManager.pop()`
instead of `SceneManager.goto(Scene_Gameover)`. The event resumes on the **If
Lose** branch. `rmmzdata.battle(troop, can_escape=False, can_lose=True)` already
takes it; nothing in this game has ever used it, and this is what it is for.

**Nobody dies.** She never reaches 0 HP. A **troop battle event page** with the
condition *enemy HP ≤ 25%* shows one line and calls **Abort Battle** (command
340). `BattleManager.abort()` → `processAbort()` → `endBattle(1)`, so:

* no death, no collapse animation, no `SoundManager.playEnemyCollapse()`;
* no victory fanfare and no rewards, which is correct - the reward is a person;
* the event resumes on the **If Escape** branch.

Set `can_escape=False` so that the escape branch is unreachable by any other
route and means exactly one thing: *she stopped*.

Belt and braces, if she should ever somehow reach zero: `trait(63, 3, 0)` sets
collapse type 3, and `Game_Enemy.performCollapse` has cases for 0, 1 and 2 only -
so no effect is requested, `_appeared` stays true, and she simply remains
standing. Not needed with the abort, but it is one trait and it costs nothing.

**The battle log**. Give the troop a name nobody sees but the next reader:
`A Discussion With Mam`.

---

## 5. Spare, in the party

### Ids

| range | what |
| --- | --- |
| Actor 11 / Class 11 | Spare Cotterill / **The Ninth** |
| Skills 150-155 | his |
| Skills 146-149 | Mrs Cotterill's |
| Enemy 28 | Mrs Cotterill |
| Troop 29 | A Discussion With Mam |
| Weapon 34 | A Bag, Packed |
| Armor 27 | A Washer, Off Shim (accessory) |
| Items 33-34 | Form P-9, the washer before it is worn |
| Switches 72-74 | as above |

**This reverses `NORTH.md` 9**, which says *Actors / Classes: none*, in as many
words, and gives the reason. That decision was right when the north was a
vehicle and a town. It is being overturned deliberately and it needs writing
down in 9 as an amendment rather than quietly edited out.

### What he is

Not a small fighter. **The best-designed skill list in the party, on the worst
stat line in the party.** He has the highest AGI and the lowest DEF in the game,
about half of Bram's HP, and an ATK that is a joke. He is one of the strongest
characters in the game and none of it comes from a number.

Class traits:

* **Target rate 0.45.** Nobody can quite bring themselves to be the one who hit
  the nine-year-old. Literal, defensible, and mechanically enormous.
* Evasion 0.25, the highest in the game. He is small and he is quick and he has
  eight older siblings.
* **Party ability: double gold.** Wren has double drops and Nix has half
  encounters; Spare is the youngest of nine and there has never once been money
  down the back of anything that he did not find first.
* Special skills only. No magic. He is nine.

### The six

| id | skill | what |
| --- | --- | --- |
| 150 | **Small Enough** | One enemy, and **ignores DEF entirely** - `a.agi` based, no `b.def` term. There is a way in. There is always a way in. He is the only one who fits. This is the answer to Ambulant Salvage at 52 DEF, and it is his bread and butter from level one. |
| 151 | **Temper Tantrum** | One enemy, enormous, and **he hurts himself doing it**. It has never once worked on his mother. Keep it in the list for the whole game. |
| 152 | **I Have A Bag** | Whole party: a modest heal and **every state removed**. It has been packed for two years. There is something in it for everything. |
| 153 | **They Never Hit Me** | Self, three turns: **target rate 0**. For that long nobody in the fight can make themselves swing at him. A state with `trait(23, 0, 0)`. |
| 154 | **Ninety Tubes** | One enemy: DEF-ignoring damage and **a permanent DEF break** on the target. He has done worse, in the dark, for buns. |
| 155 | **The Drawing** | The ultimate. Party-wide: revives the fallen, a substantial heal, ATK and AGI up, and full TP. He does not show it to just anybody. **He does not know this skill during the argument** - it is what he learns from it, because it is what his mother found in the bag, and it is granted at the end of the scene rather than at a level. |

That is a character who ignores armour, cannot be targeted on demand, carries a
full-party revive, and doubles the party's income - which is what "one of the
most powerful players in the game" has to mean in a game where the numbers were
tuned two expansions ago. Run `balance.py` before a stat is committed.

---

## 6. The art, and it is a blocker

`validate.py` line 86: a side-view game with an actor whose `battlerName` is not
in `img/sv_actors/` is a **hard validation failure**, not a cosmetic one.

* **Spare needs `img/sv_actors/<name>.png`.** There is no sv battler for
  `SF_People1` at all - the sheet does not exist in that folder. The format is
  **576 x 384**, a 9 x 6 grid of 64 x 64 pose cells, matching every other file
  in there. His face and walking sprite are already right and do not change:
  `SF_People1` index 0, dark blue-black hair, brown eyes, a blue jacket over a
  pale blue shirt. The only stock alternative is to borrow one of the
  `SF_Actor*` battlers, all of which are grown adults, and it would be visibly
  the wrong person.
* **Mrs Cotterill needs `img/sv_enemies/<name>.png`** (and conventionally the
  same file in `img/enemies/`). No grid, no fixed size - stock enemies run from
  146 x 218 to 192 x 192 - transparent PNG, standing, drawn facing left. She is
  `SF_People1` index 5 in conversation: dark green-black hair in a long side
  braid, mustard cardigan, entirely unbothered, and **expecting her tenth in the
  spring**. She should look like somebody who is not going to move rather than
  somebody who is angry.

---

## 7. What else has to be touched

* **The ending tally.** One new appended `if_then` on `SW_SPARE_JOINED` in
  `journey.finale_event`, after the fight, alongside the other fourteen. The
  Prophecy has an opinion about the paperwork.
* **`VAR_TROPES`.** Two new sites: the argument itself, and one for the secret
  tenth companion. The tiers are 40 / 20 against about sixty reachable, so two
  more does not move a threshold - but it is exactly the kind of drift
  `CLAUDE.md` says to come back and check, so check it.
* **`VAR_BLUSHES` is untouched.** Nothing in this is Register A. The count
  stays at twenty-five reachable and the tier stays at twenty. Resist the urge.
* **`story.COMPANIONS`.** He is deliberately **not** added to either roster
  form. The Committee cannot strike him off, because he was never on it. If the
  player takes him to a clerk, the clerk's existing line does the whole joke on
  its own: *"I cannot remove someone who is not on the roster. That would create
  a negative person."*
* **He does not leave at the tower door.** That is Roland's, and Roland's is
  about a contract.
* **Scenarios.** `spare_joins` (the conditions, the conversation, both branches
  of the choice, the no-room branch), `spare_argument` (the fight: the party
  swap, the abort at threshold, the concession, and a deliberate loss proving
  there is no Game Over and that it can be retried), and a `clanging_faces`-style
  check that his face in the message window is the same lad who is standing on
  the doorstep.

---

## 8. The one thing to get wrong

She is right. He is nine, the tower eats people, and she has been the one there
every time he came out of a hole. If the scene is ever written so that she is an
obstacle, or shrill, or a joke, it has gone wrong, and 1.6's last line covers it:
nobody is diminished by their own punchline. She loses the argument to the one
thing she cannot argue with, which is that he is exactly like her.
