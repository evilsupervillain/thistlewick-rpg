# The Companions

*A proposal, not a specification. Nothing below is built.*

`EXPANSION.md` was the intent for the south and `NORTH.md` for the north. This
is the intent for the **fourth quarter**: the nine people who can walk beside
Bram, who they are, and the quests that exist only because one of them is
standing there.

**`NORTH.md` section 1 is still the law for every line of it.** Register A is
the innocent double meaning; Register B is adult experience; the comedy is
embarrassment and never resentment; marriages are good; nobody is diminished by
their own punchline; and section 1.7's additive rule holds without exception -
not one existing line is re-voiced. Several ideas below started life as
rewrites of finished content and have all been redone as appended pages, which
made two of them better and is the usual result.

---

## 0. What this is, and what it is not

The game has ten actors and a party of four. Which three the player takes
already changes how combat works. It changes nothing else, and that is the gap
this document fills:

> **A companion quest is content that does not exist unless that person is in
> the party.** Not a special line inside a quest everybody can do. A different
> errand, in a place the other players never saw, that ends with a thing only
> they could have got you.

Three consequences fall straight out of that and are worth accepting up front:

* **A single playthrough can see at most three of them.** That is a feature.
  Nine companion quests across three-companion parties is the first real reason
  this game has ever had to be played twice.
* **They belong after the airship.** The map is full - Thistlewick, Nether
  Sopping and Upper Clanging are crowded, and every road on the island has
  something on it. The Two Hundred is the game's answer to "where does new
  content go", and it is already flying and currently only takes you to three
  rocks and a joke. Companion quests are what the airship is *for*.
* **None of them is on the way to anything.** Same contract as the south: the
  road north is the plot, and everything here is the world the plot is
  happening in.

**Bram is out of scope.** He is always in the party, so a quest that requires
him is just a quest. He is in the table below for completeness and because two
other people's quests are about him.

---

## 1. The shape of a companion quest

### 1.1 The gate is an engine feature, not a switch

MZ page conditions have **`actorValid` / `actorId`** natively -
`Game_Event.meetsConditions` checks `$gameParty.members().includes(actor)` and
refuses the page otherwise. `db.py`'s page template already carries both fields
(`"actorId": 1, "actorValid": False`). So:

* A person in a town has an ordinary page and an appended page conditioned on
  `actorValid`. Walk up with Zephyrine and you get a different conversation.
  Nothing is switched, nothing is spent, and a player without her sees today's
  game byte for byte. **This is pattern 1 and pattern 2 of 1.7 at the same
  time and it is free.**
* Two traps. `Game_Party.members()` is `battleMembers()` in battle and
  `allMembers()` on the map - irrelevant here only because this game caps the
  roster at four, and *that* is the assumption to write down rather than
  rediscover. And a page condition takes exactly **one** actor, so "Hob or
  Bryd" is two pages and "Hob **and** Roland" is a conditional branch inside
  one.
* The roster clerks can **dismiss** a companion mid-quest. Every quest below
  must therefore be re-enterable and must never park state that only that
  person can spend. Rule: **the quest giver keeps the quest.** If the player
  walks off with somebody else, the errand waits.

### 1.2 What a companion quest owes the player

| owes | why |
| --- | --- |
| One place the other eight never see | the reward for the choice is *content*, not a stat |
| One fight or trial that uses their mechanic | Nix opens a thing, Wren identifies a thing, Aldric is hit instead of you |
| One piece of gear only they can wear | so the reward is not wasted on a party that lacks them |
| One cliche, walked into face first | `story.trope()`. This game's running gag pays the rent |
| One line in the ending | see 1.4 |

### 1.3 What they must not do

* **Not undo an established fact.** Roland leaves at the tower door. That is
  contractual, it is the best thing in the south, and no quest here may soften
  it into a stay. Roland's quests may only change *what he leaves you with*.
* **Not require a companion the player cannot have.** Nothing here gates on two
  named people at once except where it is explicitly a two-companion quest and
  is flagged as such - there are three, they are the best ideas in the
  document, and they are optional twice over.
* **Not re-voice anybody.** Corvin's village is fine, everyone is fine, and
  every joke here is still the one where nobody is unhappy.

### 1.4 The ending, and the counters

Fourteen `if_then` blocks already hang off the finale's tally and this document
could trivially make it forty. Do not.

* **One switch per companion**, `SW_<NAME>_STORY`, set by whichever of their
  quests the player finished. One block each in the tally, nine total, and the
  Prophecy has one opinion per person rather than one per errand.
* Plus **one counter**, `VAR_COMPANION_STORIES`, and one closing line that
  reads it back: *"Three of them got something out of it as well."*
* **`VAR_TROPES` drift.** Every quest here adds sites, and the ending's tiers
  are 40 / 20 against about sixty reachable. Fifty new clichés moves both
  thresholds and `CLAUDE.md` says to come back and check. Come back and check.
* **`VAR_BLUSHES` is the dangerous one.** The tier is 20 against 25 reachable,
  cut at four fifths. Merribell and Wren are two of the game's four natural
  Register A delivery systems and their quests will produce more moments
  without trying. Every one added moves the threshold. The comment above the
  branch in `journey.py` is where whoever adds the twenty-sixth is standing;
  this document is the warning that it will be a whole handful at once.

---

## 2. The nine, and the tenth

Bios below are expansions of what the game already says, not replacements for
it. Nothing here contradicts a line that has shipped; where the finished game is
silent, this fills it in.

### Bram - Chosen One #48 *(out of scope, listed for completeness)*

A turnip farmer, asleep during the vote, selected by a committee, in possession
of one hoe and a quantity of unearned confidence that has never once been
audited. He is the straight man and he is free of charge: the narration voice is
already naive, he asks the polite question, and somebody else answers it
honestly. Two of the quests below are about him and he is not invited to either.

---

## Merribell - Sister of Whatever Works

### Who she is

Village healer, Thistlewick, and the only member of her order for eleven miles.
The Order of Whatever Works holds that theology is a distraction from the actual
problem, and that the actual problem is usually that you have not had any water
today. Its founding document is a pamphlet. Its rule of life is four lines long
and one of them is about socks.

She trained at the **Sisterhouse at Weeping Bottom**, in a wet valley chosen by
a founder who believed damp air was good for the chest and was wrong, and left
at twenty-two because the Sisterhouse had begun holding symposia. She keeps the
most complete medical record in the county - every ailment of every soul in
Thistlewick, dated, in a good hand - and the Prophecy Committee has never once
asked to see it, preferring the Prophecy.

She is a professional, and professionals have vocabularies. She says anatomical
words the way you would say "elbow", entirely without incident, in mixed
company, at volume, and Bram has learned to look at the ceiling. This is already
in the game (`village.py`, "Then say ankle! Oh, thank goodness") and it is the
seam her quests mine.

The thing she does not say: she has never lost anybody. She is twenty-six. She
knows exactly what that means and she knows it is not a virtue, it is an
average, and she is aware the average is about to be tested by a tower.

### Quests

**MER-1. The Sisterhouse.** *(cliche: the return to the monastery / the
master's disappointment)* The mother house has split. The Order of Whatever
Works has been schism'd by the **Order of What Ought To Work**, which is losing
patients and winning every argument, on the grounds that Whatever Works has no
doctrine and cannot be examined on it. The dispute is settled the way this world
settles things: a queue. Two orders, one ward, forty patients, and whoever gets
through their half first is right. What Ought To Work insists on the correct
treatment for a disease the patient does not have. Merribell asks people
whether they have eaten. *Needs:* Sisterhouse (map), Prioress Aveline Stope,
Sister Bewick. *Gives:* the Pamphlet (accessory, healing +), and the ending
learns her order won on points.

**MER-2. Fit To Travel.** *(cliche: the prologue medical / the paperwork
before the adventure)* She discovers, somewhere around Upper Clanging, that a
Chosen One is required by clause eleven to be certified fit before departure,
that this has been done forty-seven times, and that Bram's is blank, because
he was asleep. She will now do it. Properly. It requires a set of scales from
Nether Sopping, a lamp from the lighthouse, a clean surface, and a witness, and
it is conducted wherever the party happens to be standing. **Register A carries
the entire middle of this quest and not one line of it is improper**: she is a
medic, she is thorough, she narrates what she is doing because that is what a
professional does, and the witness is whoever is third in the party. *Needs:*
no new map; three fetches across existing towns; one witness page per companion
- and **the witness page is the joke**, because nine people react to the same
examination nine different ways and Sir Aldric's is the funniest thing in this
document. *Gives:* Certificate of Fitness (key item, does nothing, is
enormously official), several blushes, and a line in the ending in which the
Prophecy notes that this is the first properly documented attempt in four
thousand years.

**MER-3. The Healers' Table.** *(cliche: the veterans' reunion)* Every surviving
party medic within forty miles meets once a year in a back room of the Slain
Wyvern and compares the worst thing they have ever had to improvise with. **Ysolde
Marrow** chairs. Merribell is the youngest by thirty-eight years and is asked to
speak, and has nothing, because nobody has died on her. The room does not
console her and does not mock her. They tell her to write it down, all of it,
now, while she still thinks it is boring. *Needs:* one appended interior page
(Map 14) and four visiting healers. *Gives:* the Table's Kit, and this game's
second-best Register B moment after Ysolde's original one, which is fitting,
because it is Ysolde who says it.

**MER-4. The Man Who Cannot Stay Down.** *(cliche: the healer NPC as a vending
machine)* **Tobias Frayne**, of a hamlet on the coast road, has been revived by
passing adventurers eleven times in thirty years, on the grounds that they were
going that way anyway. He has developed a professional relationship with
mortality and now walks into things on purpose, because it always works out and
the attention is lovely. Merribell will not raise him a twelfth time and instead
has to cure him of adventurers, which is done by leaving. *Needs:* one world-map
cottage, one bad ladder. *Gives:* gold he insists on paying, out of a jar.

**MER-5. The Well at Sump.** *(cliche: the cursed village and its ancient
affliction)* A village has been cursed for six generations. The symptoms are
headache, irritability, poor sleep and a general sense that things used to be
better. Merribell diagnoses it in nine seconds. Nobody has had any water since
1794 because the well has a wasps' nest in it and the parish has been unable to
agree whose job the wasps are. The curse is real, in the sense that a thing that
has ruined six generations is real. *Needs:* Sump (small map or a world-map
event with a well), Parish Clerk. *Gives:* the founder's four-line rule made
literal, and the biggest single `story.trope()` payload in the document.

---

## Hob Grumnir - the Smith

### Who he is

Blacksmith, Thistlewick, third of that forge and second of that name. Talks to
his hammers. Two of them have names and one of them, he insists, answers.

The one that answers is **Beatrice**. Beatrice is right about everything and has
never once said anything anybody wanted to hear. She told him the forty-seventh
came in for a sword and got a good one and it did not help. She tells him a
sword is no use on its own. She tells him whose fault the gate is.

There is a headstone in Thistlewick churchyard that says **BEATRICE GRUMNIR**,
and she was his aunt, and she trained him from nine, and everything the hammer
says is a thing she said first, and the entire village has quietly agreed for
eleven years not to mention this to Hob. That is the joke and it should never be
explained by the game. If a line ever has a character say "the hammer is your
aunt", cut the line. Somebody should say instead that Beatrice was always
right, and let the player do the rest.

He has made a great many things and owns almost none of them, because his
pricing model is "take it" and his invoicing is a shelf. He is an enormous man
who is frightened of exactly two things: getting a thing wrong in a way that
someone else has to live with, and Bryd Ollerenshaw's forearms - the second of
which the game has already established and must continue never to say.

### Quests

**HOB-1. The Assize of Hammers.** *(cliche: the tournament arc)* The Worshipful
Company of Smiths judges work every three years at **Great Dunnage**, and Hob
has never entered, because entry requires a submitted piece and he does not own
anything he has made. So the quest is a retrieval tour: eleven things he made
are in eleven hands across the whole island - a hinge, a trivet, a ploughshare,
Nix's lockpicks, a hook on a boat in Nether Sopping - and every owner is glad to
see you and none of them will give it back, and each has a better reason than
the last. He submits Beatrice, which is not his work, and is disqualified, and
is entirely satisfied. *Needs:* Great Dunnage + the Company's hall; eleven
appended pages on existing NPCs, which is the cheapest big quest here. *Gives:*
a Company mark, and one line in the ending in which the Prophecy has read the
judges' notes.

**HOB-2. The Grave He Has Not Made.** *(cliche: the smith's masterwork)* Beatrice
goes quiet. Not broken - quiet. Hob is bereft, and unbearable, and after a while
admits what she last told him to do, eleven years ago, which was to make her a
marker, and which he has been unable to start because he cannot get the words
right. The quest is four attempts. He rejects the first three, all of which are
magnificent, and settles on the fourth, which is a churchyard gate with a good
latch, because the gate was sticking and she would have hated the fuss. **Nobody
in the scene says she is the hammer.** Beatrice starts talking again on the walk
home and immediately criticises the latch. *Needs:* no new map - Thistlewick's
churchyard, which does not exist yet and is one appended corner of Map 1.
*Gives:* the game's best weapon for him, forged badly on purpose.

**HOB-3. The Anvil.** *(cliche: the stolen sacred object)* The anvil has been
stolen. It weighs three hundredweight. Hob is incandescent for nine seconds and
then thoughtful, because they cannot have got far. They did not get far. They
are eleven feet outside the door, under it, and have been for some hours, and
are apprentice bandits on the six-week syllabus, and one of them is very
apologetic. Rescue your own burglars. **Meredith Crooke** turns up to collect
them and marks the module a fail. *Needs:* nothing new. Crooke's camp already
exists and the syllabus is already a joke this game has made. *Gives:* two
bandits, briefly, as a joke, and a written apology in a good hand.

**HOB-4. The Sky Anvil.** *(cliche: the star-metal blade)* The one wholly
mythic thing in the document, undercut immediately: a meteorite fell in 1749 and
has been a farm gatepost ever since. **Elias Meech** will not sell his gatepost,
because it is a very good gatepost, but will trade it for a gate. Hob has
recently become quite good at gates (see HOB-2, and require it - this is the one
place a quest chain earns the dependency). *Needs:* a world-map field; airship
or the west road. *Gives:* star-iron, which makes exactly one weapon, which is
not for Hob, and he will not say who it is for, and the player can guess.

**HOB-5. Two Smiths, One Forge.** *(two-companion: Hob + nobody, but requires
`SW_HOB_BRYD`)* They went for a drink. That happened, it is in the game, and
this is what comes of it and no more: Bryd sends up a job neither of them can do
alone - a boiler tube plate for the Two Hundred's refit, which needs four hands
and one heat and a person small enough to get inside afterwards. They do not
finish a sentence in the same room for the whole quest. A child says they do
this every time. *Needs:* Map 24, appended; Grommet, who is already there and
already put upon. *Gives:* the plate, Ott's approval, and nothing whatsoever
said out loud.

---

## Zephyrine Vance - Formerly of the College

### Who she is

Hedge mage. Eleven years "just passing through" Thistlewick, which is a
Collegium term of art meaning a leave of absence that nobody has processed.
Expelled from the **Collegium Arcanum** over an incident involving the Dean, a
duck, and what the enquiry twice called "an unsanctioned quantity of fire". The
Dean is fine. The duck is fine. Everyone is fine.

What the game has never said is *why*, and the answer is worth building a quest
on: she did it over a footnote. A junior fellow's paper had been quietly
attributed to somebody senior, she said so at a faculty dinner, was told to let
it go, and did not let it go. The quantity of fire was unsanctioned. The
argument was correct. Both those things have been true for eleven years and only
one of them is in the file.

She was the best student of her year and has not cast anything indoors since,
because hedge magic is the discipline of doing the same work with worse
equipment in somebody's garden, and she is very good at it and it is not what
she trained for. She drinks at the Gilded Turnip in the manner of a person
waiting for a letter.

### Quests

**ZEPH-1. The Fines.** *(cliche: the return to the wizard school)* She goes back
to appeal. There is no appeal, because there was no expulsion: the paperwork was
drafted, initialled, and never filed, and she has therefore been on unpaid study
leave for eleven years, and is in good standing, and owes eleven years of
library fines. The fines are the largest number in the game. **This is where the
bounty money goes** - it is the only gold sink the design has ever had that is
funny. The Sub-Librarian is immovable, courteous, and correct. *Needs:*
Collegium (2-3 maps), Sub-Librarian Prewitt, Registrar's clerk. *Gives:* her
name back, a robe with a stat line, and the option to simply refuse to pay and
remain expelled forever, which is a real choice and should be.

**ZEPH-2. The Duck.** *(cliche: the escort mission)* The duck survived the
incident, and the Collegium, unable to think what else to do with a bird that
had been present at a formal enquiry, made it an honorary Fellow. That was
eleven years ago and it now holds a chair, votes in Congregation, and has an
opinion on the endowment. There is a vote. The vote needs a quorum. The quorum
needs the duck, and the duck is on a pond four miles off, and it must be walked.
It has four hit points and walks into everything, exactly as Ysolde's duke's son
did, and Ysolde's tale in the Slain Wyvern is the setup this pays off nine hours
later. *Needs:* Collegium + a pond; the duck as an escortable event. *Gives:*
the duck's proxy vote, permanently, which is worth precisely one joke and it is
in the ending.

**ZEPH-3. Dean Fenwold Is Fine.** *(cliche: the mentor who was secretly the
villain - denied)* The Dean has built a second career on being the man who was
fine. He does an after-dinner talk. He would like her to do the fire again, for
the lecture demonstration, controlled, small, in a hall, with buckets. She
refuses. She then agrees, on terms. It goes wrong in precisely the way it went
wrong the first time, for precisely the same reason, which is that the room is
wrong and she said so in 1794 as well. Everyone is fine. **He is not a villain
and must never become one** - he is a nice, vain, slightly silly man who did not
back her up once, eleven years ago, and knows it, and this is his apology, and
it is a bad apology, and it is sincere. *Needs:* Collegium Hall; Dean Fenwold.
*Gives:* the biggest fire in the game and no consequences.

**ZEPH-4. The Cinder Fen.** *(cliche: the elemental hazard only one member can
solve)* Something needs burning and everybody agrees. Nine hundred acres of
sodden fen have been slowly drowning the road to Great Dunnage, and the
traditional remedy is fire, and the parish has not had anyone able to do it
since the last one retired. This is the pure ability quest: an unsanctioned
quantity of fire, sanctioned, in writing, in triplicate, by a parish that
requires the form back afterwards. *Needs:* a fen on the world map; Drainage
Commissioner. *Gives:* opens a road, which is a real reward, and a certificate.

**ZEPH-5. The Lay-By.** *(cliche: the secret order of mages)* The hedge mages
have an association. It has three members, meets in a lay-by on the west road
because none of them will host, and has been trying to agree a name for nine
years. They are all excellent. One of them taught himself out of a book with
four pages missing and is therefore better than the Collegium at exactly four
things. *Needs:* one world-map event, no map. *Gives:* one skill, taught badly,
that works.

---

## Nix - Acquisitions

### Who they are

Runs the back room of the general store. Does not steal things. **Locates**
them, ahead of schedule, on behalf of a client who has not yet been identified.
Everyone asks eventually; Nix likes to get ahead of it, same as everything else.

The client has been unidentified for eleven years, and here is what that is: at
fifteen, Nix worked out that "I wanted it" was not a sentence that got you
anywhere in a village where everybody knows your mother, and invented a ledger
instead. Every item in, every item out, every provenance, dated, in a hand that
got better with practice, all of it done on behalf of a client who is described
in the front of the book only as *the party of the second part*. Eleven years
of scrupulous double entry later, the ledger is the most honest document in the
county and the client has, in a real sense that Nix would refuse to discuss,
begun to exist.

They are not a thief and the distinction is not a joke to them. Every single
thing in that shop was got somehow, and Nix can tell you how, and the telling is
always fine, and is occasionally magnificent. There is one entry near the back
with no provenance and no date, and it is the only unfinished line in eleven
years, and it is what NIX-1 is about.

### Quests

**NIX-1. The Client Identifies Themselves.** *(cliche: the mysterious patron)*
A letter arrives, correctly addressed, in Nix's own hand, which Nix did not
write, or wrote and does not remember writing, and neither reading is the one
you want - the true one is worse and funnier, which is that Nix wrote it at
fifteen, to be delivered on a date, and has been beaten to the joke by a
teenager. The client wants one item, and it is the entry with no provenance, and
it is a coat, and it belonged to somebody, and getting it back requires going to
a bonded warehouse in Great Dunnage that Nix has been avoiding for eleven years
for a reason that turns out to be embarrassment rather than crime. *Needs:*
Great Dunnage; the Bonded Warehouse; Wharfinger Tibbs. *Gives:* the coat, which
is armour, and which fits.

**NIX-2. The Sealed Counting House.** *(cliche: the vault nobody can open)*
Great Dunnage sealed its counting house in 1802 when the key was lost, and has
run its entire municipal finance on faith and a memorandum ever since. The
Corporation would like it opened, formally, by a licensed person, and Nix is
not one, and the licence is a form. Nix opens it in nine seconds while the
Mayor is still reading the preamble. Inside is a note in a clerk's hand reading
*we spent it*, dated 1802, and one chair. *Needs:* Great Dunnage; the Mayor;
the counting house interior (one small room, one enormous door). *Gives:* gold,
which the Corporation insists you keep, because it is not theirs, because
apparently nothing is.

**NIX-3. Professional Courtesy.** *(cliche: the rival thief)* **Cobb Lorrimer**
steals things. He says so. He is enormously proud of it, has a hooded cloak, and
finds Nix's entire vocabulary insulting - "locates", "ahead of schedule", "the
client" - because it makes what he does sound like a job somebody has failed to
apply for. He challenges Nix. The contest is not a fight: it is a client, a
list, and an afternoon, and Nix wins on **paperwork**, having got every item
with permission, and Lorrimer cannot bear it. *Needs:* one map, or a room in an
existing town. *Gives:* Lorrimer's tools, which he leaves behind, in a huff,
which means they were located.

**NIX-4. The Longest Loan.** *(cliche: the fetch chain)* Everything in the
Emporium of Previously Owned Goods was previously owned by somebody Nix can
name. Return eleven items to eleven owners in one afternoon. Every owner is
delighted. None of them knew it was gone. Two of them try to pay. One of them
gives Nix something better and the whole thing starts again, which is how the
shop got its stock in the first place and is stated nowhere. *Needs:* nothing
new; eleven appended pages spread over three towns. *Gives:* the ledger's last
page, closed out.

**NIX-5. Half An Encounter.** *(cliche: the stealth section)* Nix's party
ability halves encounters, and this is the quest that is entirely about it:
somebody has to be got through the Gloamwood at night without a single fight,
because he is a witness, or a bailiff, or a bassoonist, and any of those is
funny. A fight fails the quest outright. *Needs:* nothing new - the Gloamwood
exists and is under-used. *Gives:* the only no-combat dungeon run in the game.

---

## Sir Aldric Pemberton-Gore III - Knight Errant

### Who he is

A real knight of a real house, which is small, and moated, and damp, and eleven
miles from anywhere in a direction he could not indicate. He arrived in
Thistlewick six years ago and has been trying to leave ever since, and has never
found the north gate, which is nineteen tiles from where he is standing and has
a sign.

He has left successfully many times. He has also arrived in Thistlewick many
times, believing it to be a different village, and the village has decided
without ever discussing it that this is fine and that somebody should keep an
eye on his laundry. Errantry is a formal programme with a syllabus and a
reporting requirement, and he is nine years overdue on an errand whose details
he no longer has, and he has never once written to say so, because the letter
would have to be posted, and the post is in the direction of the gate.

The family arms are, in blazon, *a knight rampant regardant* - facing the wrong
way - and this was assumed for two centuries to be a pun about vigilance. He is
the third of that name. The first and second were also lost. He is the kindest
person in the party by a distance that is not close, he covers whoever is
bleeding without being asked, and if there is one companion the player should
feel bad about leaving behind it is this one, and every quest below should be
built so that finishing it makes that worse.

### Quests

**ALD-1. The Errand.** *(cliche: the quest that started it all)* He still has
the letter. It has been in his tabard for nine years and is soft at the folds.
It must go to the next village, which is four miles away, and he insists on
leading, and the route he proposes is a hundred and ten miles and passes a
coast he has been told about. The party may correct him at any point and should
not. The letter is an invitation to a wedding, nine years ago, which everybody
attended anyway, and the bride is now a mother of three and delighted to see
him, and keeps the letter, and puts it on the mantelpiece. *Needs:* one hamlet
(**Little Gore**, four miles from the seat and mapped as a single small map);
the bride, **Hester Vane**. *Gives:* the errand, discharged, and the first time
in six years that anything he is carrying has got where it was going.

**ALD-2. The Vigil.** *(cliche: the night watch)* A knight is confirmed by
keeping vigil in a chapel. He has kept eleven and every one of them was in the
wrong chapel, including one that was a barn. The party keeps the twelfth with
him, in the right one, and the rules of the vigil forbid him to move or speak
until dawn - and things come. **Mechanically this is the best fight in the
document**: a defence battle in which Aldric is present, cannot act, cannot be
commanded, and automatically covers whoever is about to be hit, so his entire
class identity is the boss condition. He does not move. He does not speak. He
takes everything. *Needs:* a chapel (small map, could be an interior at
Coldbarrow or the Sisterhouse); a troop with a turn-count victory condition.
*Gives:* confirmation, thirty years late, and the shield.

**ALD-3. The Chapter House.** *(cliche: the guild that has lost your file)* The
Order of the Errant keeps a great map with a pin for every knight in the field.
Aldric has nine pins. Six of them are correct on different dates and three of
them are the same week. The Order is not embarrassed; the Order regards this as
a data problem, has formed a committee, and would like him to stay put for the
duration of the review, which is the one thing he cannot do and the one thing he
has always wanted to be asked. He is offered a promotion contingent on remaining
in one place. He refuses it beautifully. *Needs:* the Chapter House at
Coldbarrow (one interior); Chapter Clerk Mordaunt. *Gives:* a proper rank, and
the Prophecy notices in the ending that somebody in this party finally got
promoted.

**ALD-4. The Horse.** *(cliche: the loyal steed)* He had a horse. Nobody has
asked about the horse in six years. **The horse is fine.** The horse walked
home, was taken in at a haulage yard in Great Dunnage, has been in steady work
ever since, is well thought of, and has, in the way of a good horse in a good
yard, effectively become a partner in the business. The reunion is genuinely
touching and the horse does not want to leave, and the yard is very tactful
about it, and Aldric says of course, and means it. **She is doing so well.**
*Needs:* Great Dunnage; the haulage yard; the horse. *Gives:* nothing
mechanical. This is the one quest in the document whose reward is a scene, and
it should stay that way.

**ALD-5. Pemberton-Gore the Fourth.** *(cliche: the prodigy successor)* His
nephew turns up. Nineteen, magnificent, courteous, found the north gate
unassisted on the first attempt, and worships his uncle without a trace of
irony, having been raised on the story of the knight who went out and never came
back, which is the family's most treasured tale and is not how Aldric would
describe the last six years. The lad wants to squire for him. The comedy is
entirely Aldric's face; the warmth is that the lad is right. *Needs:* one NPC,
placeable anywhere. *Gives:* an appended page on Aldric everywhere afterwards
in which somebody is following him.

**ALD-6. The Wrong Dragon.** *(cliche: the dragon)* He was sent, twelve years
ago, to slay a dragon. He arrived at a different one. The different one is
delightful, elderly, has read a great deal, and is not remotely a dragon in the
sense the commission meant. The correct dragon has since been slain by somebody
else who is now insufferable about it in the Slain Wyvern. *Needs:* a lair on
the world map; one large friendly NPC. *Gives:* the game's only dragon,
uneaten.

---

## Piper Quill - Chronicler

### Who she is

A bard who narrates events as they happen, in the third person, at volume,
whether or not this is convenient. Stands on tables. Does the songs; you do the
sword bit; it is a good system.

The Quills are the **official chroniclers** and have been for four
generations - the text under all forty-seven portraits on the Wall of the
Forty-Seven was written by somebody in her family, and her grandmother did
numbers forty through forty-three and is quoted in the Prophecy's own preamble.
The house style is one line long: *never let the truth spoil the metre.* Piper's
entire professional rebellion is that she writes down what actually happened,
which is why she is standing on a table in a village pub at twenty-four instead
of being paid.

She has been taking notes on Bram since the day he woke up, and the Prophecy
Committee strikes the verses it cannot have read aloud at the fete, which the
game already counts. Verse seven is already struck. She has never told anybody
what is in verse seven and the game must never say.

### Quests

**PIP-1. The Authorised Version.** *(cliche: the rival chronicler)* Her aunt
**Ambrosine Quill** is writing the official account of Bram's quest and has
already finished it, having started before he left, because the shape is known.
It is better than what happened. It is properly metred, it has a good middle,
and in it Bram is orphaned, which he is not, and Merribell dies, which she has
not, and there is a bit with a wolf. The Committee has approved it. The player
can help Piper fight it, or help Piper *fix* it, or - the choice worth building
- read it, and find it very good, and say so. *Needs:* Prophecy Hall, appended;
Ambrosine. *Gives:* two endings' worth of one block, and the funniest single
document in the game.

**PIP-2. A Rhyme For Turnip.** *(cliche: the running gag that pays off)* She has
been looking for one since the recruit scene. This is the quest where the party
helps. Every companion offers one and every one is worse than the last: Hob
offers "burnip" without embarrassment, Wren rules the whole class of words
inadmissible on taxonomic grounds, Corvin's scans perfectly and is about
drowning, Aldric's is in another language and does not rhyme in that one either,
and Nix locates one, ahead of schedule, on behalf of a client. The answer is
that no such rhyme exists and any competent poet would have changed the other
line in week one, which she does, in nine seconds, and everyone who spent the
afternoon on it is furious. *Needs:* nothing new; one appended page per
companion, which is the same cheap pattern as MER-2 and just as good. *Gives:*
the ballad's last verse, and a `story.trope()` per suggestion.

**PIP-3. The Contest at the Sign of the Bell.** *(cliche: the tournament, again,
but with instruments)* A bardic competition at Great Dunnage with categories
nobody can defend, judged by a panel that includes a man who cannot hear.
**Mechanically a boss fight where the damage type is heckling**: her buffs and
debuffs are the whole kit, the enemy is a rival act, and HP is the room's
patience. She loses to a man who does birdcalls. The birdcalls are, in fairness,
extraordinary. *Needs:* Great Dunnage; the Bell; three rival acts. *Gives:*
second place, which she frames.

**PIP-4. The Elegy.** *(cliche: the tragic backstory of the NPC you never met)*
She is commissioned to write an elegy for a man she never met, by a village that
loved him, and the only way to do it is to interview eleven people who all
describe somebody different. The quest is the interviews. The payoff is that she
writes it out of the contradictions rather than resolving them, and it is the
best thing she has ever done, and it is nine lines long, and she does not
perform it. **This is the Register B one and it must not have a punchline at
anyone's expense.** The joke, and there is one, is that the village had asked
for something with a bit more of a tune. *Needs:* one village (reuse Sump or
Little Gore); eleven appended pages. *Gives:* the song, and one of the game's
two best lines.

**PIP-5. The Struck Verses.** *(cliche: the redacted archive)* The Committee
keeps what it strikes. Of course it does. In a box. The box is in Prophecy Hall,
behind the same institutional caution that produced verse seven, and getting at
it is a form, a key and a distraction, and the last of those is what a party of
four is for. **What is in the box is never printed.** The player sees the
count - which is a number the game is already keeping - and Piper's face, and
one line of verse forty-one, which is about a hedge. *Needs:* Prophecy Hall,
appended; the archive room. *Gives:* the blush counter its second job, and
requires the threshold in `journey.py` to be recut. See 1.4.

---

## Corvin Ash - the Brooding One

### Who he is

Has been waiting in the corner of a tavern for a destiny since he was nineteen,
which is eleven years, which is longer than most careers. His village was
destroyed by flooding, in his absence, and everyone was fine, and they moved
eight miles inland, and there is a school now, and it is very good, and he
cannot make anybody understand.

The village was called **Ashcombe** and he took its name when it went under, as
a memorial, in a gesture he had thought about for some weeks. The village also
took its name when it moved, because it was their name and they were still
using it, and the new one is **Ashcombe** as well, and has a post office. You
cannot mourn a place that is answering its correspondence.

The destiny came from a fortune-teller at a fair when he was nineteen, and it
said he was the rival of a great hero, and he has organised his entire adult
life around a sentence he paid twopence for. What the game must never do is tell
him he is nothing. He is not nothing. He is a genuinely dangerous man with a
black sword who has been sitting still for a decade because somebody once
suggested he was important, and the sad-funny thing is that the sitting still
was the only bit that was ever a waste.

### Quests

**COR-1. Ashcombe (New).** *(cliche: going home)* Everyone is delighted to see
him. His mother is fine and has a new kitchen. His childhood bedroom has been
rebuilt, larger, with better light, and is currently a study. There is a plaque
about the flood and it is *upbeat*: the village is proud of the drainage, holds
an annual dinner about it, and has a small museum. He is invited to speak at the
dinner. He does. **It goes well.** Nothing in this quest goes wrong for him,
which is the joke and also the point. *Needs:* Ashcombe (map, one interior);
his mother, **Mrs Ash**; the Drainage Museum. *Gives:* a scarf she has knitted,
which is an accessory, and which is the wrong colour.

**COR-2. Ashcombe (Old).** *(cliche: the sunken ruin)* The drowned one is
under a lake, and the lake is drawn down once a year for the sluices, and if you
are there that week you can walk in. There is one street. What survives is a pub
sign, a doorstep, and - in a strongbox in what was the schoolroom - his own
report card, which is bad, and which the schoolmistress had kept because she
kept everybody's. **The one moment in his story that is allowed to be simply
sad**, immediately undercut by the report card, which is in the ending. *Needs:*
Ashcombe Lake (world map) and the drowned street (one small map, drawn as a
draw-down). *Gives:* the sword's real name, which was written on the doorstep,
because his grandfather made it and it was a doorstop.

**COR-3. The Rivals' Retreat.** *(cliche: the dark mirror)* There is an inn on
a moor where doomed rivals brood professionally. Every corner is occupied. There
is a **waiting list for the darkest one**, administered fairly, with a rota.
They have a newsletter. They are, individually, lovely, and collectively a
support group that has never once used the word. Corvin is a member and has
never attended, because attending would be admitting there is a category, and
the category is the only thing that has ever made him feel better. *Needs:* the
Sable Hart (one interior on the moor); five rivals with names and hoods.
*Gives:* the ranking, which is a real league table, on which Corvin is
seventeenth, and which he takes very hard, and which is fixable by quest.

**COR-4. Mother Selvidge.** *(cliche: the prophecy that made him)* The
fortune-teller is still working the fairs, and remembers nothing, and reads him
again for twopence, and gets something completely different: a long life, a
useful trade, and no destiny whatsoever. He asks her to do it again. She does it
again. Same answer. The third reading is where the quest is: she puts the cards
down and tells him, kindly and without a shred of mysticism, that she says the
rival thing to about four young men a year because it is the reading that makes
them stand up straight, and it has never once been wrong, in the sense that they
all went and did something. *Needs:* a fair (world-map event or one small map);
Mother Selvidge. *Gives:* nothing. He keeps the coat.

**COR-5. The Appraisal.** *(cliche: the cursed blade)* He takes the black sword
to be appraised, expecting a curse. There is no curse. It is a very good sword
in poor condition with a name he cannot pronounce, and the appraiser is
enthusiastic about the tang. He asks how much a curse would cost to have put on.
It is not expensive. The appraiser has a form. *Needs:* Great Dunnage or the
Collegium; **Appraiser Fettle**. *Gives:* an optional curse, which is a real
trait, which is bad for him, which he takes.

---

## Wren Halloway - Cataloguer

### Who she is

Green cloak, crossbow, seventeen specimen jars, four hundred pages of the only
honest monograph on the monsters of this region, and every page has cost her a
fight she resented. She does not hunt them, she **documents** them; the fighting
is a step in the methodology; you cannot measure a wing that is actively in use.
Taxonomy is a moral position. Everyone else names them after how they died. She
names them after what they are.

The discipline she is trying to fix is in ruins for one reason: the previous
authority, **Doctor Amias Rowbotham FRS**, spent forty years naming three
hundred species after himself, his subscribers and his dogs, and the standard
work is therefore a monument to a man rather than a description of a landscape,
and every correction she publishes reads to the field as a personal attack on a
dead man they were all rather fond of. She published once, at twenty-three, and
was reviewed by three of his students.

She was thrown out of the Slain Wyvern for saying the wyvern is a goose. It is a
goose. She was right, and she was right at length, and being asked to leave for
being correct is the closest this game comes to being unfair to a party member,
which is deliberate, and which WRE-2 is the answer to.

### Quests

**WRE-1. The Monograph.** *(cliche: the collect-them-all)* Publication requires
a type specimen for every entry, which means an intact example of eleven things,
which means eleven fights she objects to and conducts anyway with a very bad
grace. It also requires three fellows to review it and a subscription list, and
one of the three fellows is a duck (see ZEPH-2 - **these two quests share a
map and should be built together**). *Needs:* the Collegium; Rowbotham's
students; the subscription list, which is a shop interface with names in it.
*Gives:* the monograph, published, with her name on it, and a party ability
upgrade that is entirely earned.

**WRE-2. The Second Plaque.** *(cliche: the retcon)* She wants a retraction from
the Slain Wyvern. Dorcas Thrupp will not give one, because #41 was a good man
and brought back what he could and the tone that ends the conversation is not
negotiable. The compromise is a second plaque, beside the first, which does not
correct it and does not repeat it: it records what the bird is, and where it was
got, and by whom, and why. Both plaques stay up. Dorcas reads it twice and says
nothing and puts it up herself. **Additive, in a document about being additive**,
which is the joke for anyone who has read `NORTH.md` 1.7. *Needs:* Map 14,
appended; a brass plate. *Gives:* readmission to the Slain Wyvern, which she
affects not to care about.

**WRE-3. The Thing In The Gloamwood.** *(cliche: the cryptid)* There is a
society. It has a newsletter, a membership of nine, an annual walk, and forty
years of sightings, and Wren proves comprehensively that the Thing does not
exist and never has. The society is **delighted**. They have been trying to
prove it for forty years and the walk is the point and the newsletter now has
its best-ever issue. The one member who is quietly devastated is handled with
enormous care by everybody else and is fine by the end of the walk. *Needs:*
the Gloamwood, appended; the society, meeting in an existing inn. *Gives:*
honorary membership and a badge.

**WRE-4. The Cabinet.** *(cliche: the nobleman's collection)* A manor holds
eighty impossible animals in glass cases and she is engaged to authenticate
them. All eighty are two animals sewn together. The taxidermist is alive, is
ninety, is unrepentant, and is *an artist* - he did not forge them, he composed
them, and the joins are magnificent and he will show you. The owner's family has
been proud of these for three generations. She writes it up honestly and
truthfully, which requires her to say that the workmanship is the finest she has
seen, which she means. *Needs:* the manor (one interior - reuse Fenmarch Hall
from Aldric's line and save a map); **Mr Ottershaw**, taxidermist. *Gives:*
a fee, and one composite creature that is real, which she does not mention.

**WRE-5. Bramus.** *(cliche: the honour that is an insult)* She names a new
species after Bram. It is a small brown thing that lives in turnip fields, is
of no consequence, and is remarkable for exactly one attribute: it survives
things it has no business surviving, by luck, repeatedly, in a manner she calls
in print "statistically indefensible". He is deeply touched until she explains
the naming rationale, and then he is deeply touched anyway, because it is
accurate, and because being described accurately is a thing that has never
happened to him before. *Needs:* nothing new. *Gives:* a line in the ending in
which the Prophecy, which does not read journals, has read this one.

---

## Roland Fairweather - Guest Star

### Who he is

Magnificent, glowing, extremely good at everything, and the protagonist of a
much more expensive story. Joins at level nine when the party is around six,
carries more than his share, likes you, warns you twice with genuine regret, and
**leaves at the door of the Obligatory Tower** and gives you his sword.

Eleven times. Eleven parties, eleven doors, eleven appointments. What the game
has never explained is what the appointment *is*, and the answer that fits this
world is not a curse and is not cowardice: **Roland has a prophecy of his own.**
It is a very good one - a proper one, with a lineage and a sword in a stone and
an actual sorcerer - and it has been in preparation for twenty-two years and has
never been ready. He is not waiting for it in a tavern like Corvin. He fills the
time, extremely well, on other people's, and every time somebody else's story
reaches its last door his own story's people send for him to check whether he is
still available, because he is the asset and the asset must be accounted for.

He is thirty-four. He has been the finest swordsman on the island since he was
nineteen. He has never finished anything.

**Nothing below may keep him at the tower door.** It is the best thing in the
south, it is contractual, and it is the joke. What these quests may change is
what he leaves you with, and what he knows about himself while he goes.

### Quests

**ROL-1. The Appointment.** *(cliche: the summons that takes the ally away)*
Follow him. He is embarrassed and permits it. The appointment is a **review
meeting**, in a room, with an agenda, at which four people confirm that the
prophecy is still not ready, note his continued availability, and thank him for
his patience. It takes eleven minutes. He has attended one hundred and forty of
them. The comedy is that it is exactly the same instrument as Grimspite's, seen
from the other end, and the game should let the player notice that on their own
and never say it. *Needs:* one interior anywhere (the Collegium or Great Dunnage
both work); **the Convenor**; three fellows of no importance. *Gives:* the
minutes, as a key item, which are dry and devastating.

**ROL-2. Roland's Own Quest.** *(cliche: the epic)* His prophecy names a thing
in a place. The party goes and does it. It takes an afternoon, because he is
over-levelled and the thing was scaled for a hero at nineteen and he is
thirty-four, and it is over before Piper has got a verse out. He asks the party,
carefully and without much hope, to be surprised. They are. **It is kind, and
it is not sad, and it should be played completely straight** - his life's work,
finished, in an afternoon, by four people who were glad to help. *Needs:* one
small dungeon (three maps, or one good one); the thing. *Gives:* his prophecy,
discharged, and a strictly better sword to leave you at the door - which is the
only mechanical reward in this document that changes the last act.

**ROL-3. The Alumni.** *(cliche: the party reunion)* Eleven previous parties.
They hold a dinner. They all finished their quests **without** him, all of them
say so warmly, and every single one of them thinks of him as *their* Roland and
is slightly hurt to find that there are ten other tables. It is a wholly happy
room full of people who are all quietly working something out at the same time,
and the working-out is the entire quest, and it resolves into a toast. Nobody
says the word. *Needs:* one large interior (the Slain Wyvern at capacity works
and is free); eleven cameo NPCs, several of whom already exist in this game.
*Gives:* a great many small gifts, and one line in the ending.

**ROL-4. The Maker's Mark.** *(two-companion: Roland + Hob)* The sword he leaves
you at the door has a mark on it. Hob knows the mark. It is his aunt's. The best
weapon in the game was made in a village smithy forty years ago by the woman
whose name is on his hammer, and was sold, and travelled, and came back. **Do
not have anybody explain the hammer.** Hob looks at the mark for a while and
says she did good work, and Beatrice, for once, says nothing at all. *Needs:*
nothing new. *Gives:* the sword's provenance, a refit that makes it wieldable by
Hob after Roland has gone, and the single best cross-companion moment available
to this game.

**ROL-5. The Understudy.** *(cliche: the successor)* Somebody is being trained to
replace him against the day the prophecy is ready. She is sixteen, she is
extraordinary, and she has been told nothing about the review meetings. Roland's
entire moral position for the length of the quest is whether to tell her. He
tells her. She takes it well, thinks about it, and asks a question none of the
grown-ups have thought of in twenty-two years, which is *whose prophecy is it,
exactly?* - and that question is dropped and never answered and is the seed of
whatever comes after this document. *Needs:* one NPC. *Gives:* an appended page
in the finale in which somebody is at the tower door after all, and it is not
him.

---

## Spare Cotterill - the Ninth *(see `SPARE.md` - not yet built)*

The tenth companion and the only secret one, aged nine, with a bag packed for
two years. `SPARE.md` is his specification and is not superseded by anything
here; these are what a party *with* him could then go and do.

**SPA-1. The Letters.** *(cliche: the collectible)* His mother's terms were:
jumper on, do not go in first, and **you write - it does not have to be long,
and it does not have to be true**. So he writes, from every town, and the
letters are a collectible the player posts. They are four lines each and they
are increasingly untrue. The payoff is at the works, where his mother has kept
every one and has been reading them out at the dinner hour, and the entire
shift knows about the dragon, and there was no dragon. *Needs:* a post box in
each town; one appended page on Mrs Cotterill. *Gives:* the whole set, readable
from the menu, and a very short line in the ending.

**SPA-2. Ninety Tubes.** *(cliche: the solo section)* Somewhere only he fits.
A jammed lock gate on the Dunnage cut, or a flue, or the sunken street at
Ashcombe. The party waits outside and the player plays a nine-year-old alone in
the dark for four minutes. `SPARE.md` section 3 already documents the party-swap
that makes this trivial to build. He is not frightened of the dark. He has said
what he is frightened of and it is not this. *Needs:* one confined map; the
swap. *Gives:* the best use of an established mechanic in the document.

**SPA-3. The Tenth.** *(cliche: the deadline)* It arrives in the spring, and
he would like to be there, and the tower does not care what month it is. A soft
timer, or a single window, or - better and funnier - **no timer at all**, and
the entire quest is him asking the party every few maps whether it is spring
yet, and the answer being no, and then one day being yes. *Needs:* one switch,
one appended page on Map 21. *Gives:* a tenth Cotterill, unnamed, because Clevis
is still running the book.

---

## 3. New locations

Numbered for cross-reference. **The airship is the delivery mechanism for all of
them** - anything that needs a road needs a road built, and the Two Hundred is
already flying and currently visits three rocks.

### L1. Great Dunnage - the foundry town *(the big one)*

Down the valley from Upper Clanging, where Cotter Cotterill already works -
`NORTH.md` 4.6 says so in a table and this is the town collecting on it. Upper
Clanging is a works with a town round it; **Great Dunnage is a town with nine
works in it**, and it is to Upper Clanging what Upper Clanging is to
Thistlewick: bigger, richer, louder, and completely uninterested in the
Prophecy, which it regards as a Thistlewick matter.

The joke of the place is **municipal self-regard**. It has a Corporation, a
Mayor, a motto, a crest, an anthem, and a counting house it cannot open. It
has opinions about Upper Clanging, which it considers charming. Nobody in Great
Dunnage has ever heard of Bram.

* Maps: the town (1), the Company of Smiths' hall (1), the Sealed Counting House
  (1, mostly door), the Bonded Warehouse (1), the Bell inn (1), the haulage yard
  (world-map or a corner of the town map). **Five maps.** It is the most
  expensive thing here and it carries six quests across four companions.
* Serves: HOB-1, HOB-4 (approach), NIX-1, NIX-2, ALD-4, PIP-3, COR-5, ROL-1.

### L2. The Collegium Arcanum *(the second big one)*

A university that is entirely committee. Zephyrine's expulsion, Wren's
publication and a duck with a chair all live here, which is three companions'
worth of quest on one set of maps and makes it the best value in the document.

Its comedy is **institutional courtesy**: nobody is ever rude, nothing is ever
refused, everything is referred. The Porter's Lodge holds the real power and
knows it. The Library is where money goes to die.

* Maps: the Great Court (1), the Library (1), the Hall (1), the pond (world-map
  event). **Three maps.**
* Serves: ZEPH-1, ZEPH-2, ZEPH-3, WRE-1, COR-5 (alternative), ROL-1
  (alternative).

### L3. Ashcombe - the village that is fine

Prosperous, cheerful, superbly drained, with a small museum about the flood and
an annual dinner. Every building is newer and better than what it replaced. The
plaque is upbeat. This is one map, one interior, and possibly the funniest
single location in the document, and it exists to be pleasant at somebody.

* Maps: the village (1), Mrs Ash's kitchen (1). Plus **Ashcombe Lake** and the
  drawn-down street (1 small map) for COR-2.
* Serves: COR-1, COR-2.

### L4. The Sisterhouse at Weeping Bottom

The Order of Whatever Works' mother house, in a damp valley chosen on medical
grounds that were wrong. Half hospital, half argument. A ward, a cloister, and a
chapel that will do for ALD-2 if Coldbarrow is cut.

* Maps: the Sisterhouse (1), the ward (1). **Two maps.**
* Serves: MER-1, MER-3 (alternative venue), ALD-2 (if the chapel is here).

### L5. Fenmarch Hall - the Pemberton-Gore seat

Moated, damp, and hung with eighty impossible animals in glass cases, which is
how Aldric's family home also becomes Wren's cabinet of curiosities and saves a
map. Small household, enormous portrait gallery, all of them facing the wrong
way.

* Maps: the hall (1), the long gallery (1). **Two maps.**
* Serves: ALD-1 (departure point), ALD-5, WRE-4.

### L6. The Chapter House at Coldbarrow

One room, one enormous map of the island with pins in it, one clerk. The single
cheapest location here and the one with the best sight gag: nine pins, one
knight.

* Maps: 1. Serves: ALD-3, ALD-2 (the chapel, if not at the Sisterhouse).

### L7. The Sable Hart - the Rivals' Retreat

An inn on a moor where every corner is taken. A rota for the darkest one. A
newsletter. Five hooded men being scrupulously fair to each other about seating.

* Maps: 1. Serves: COR-3, and it is where COR-4's fair should be pitched if the
  fair does not get its own map.

### L8. Little Gore, and Sump

Two hamlets, one map each, both essentially one street and a reason.
**Little Gore** is four miles from Fenmarch and is where the letter was always
going. **Sump** has not had any water since 1794 and has a wasp problem the
parish cannot allocate. Either can host PIP-4's eleven interviews.

* Maps: 1 each. Serves: ALD-1, MER-5, PIP-4.

### World-map-only sites (no maps, one event each)

| site | for |
| --- | --- |
| **The Sky Anvil** - a meteorite used as a gatepost since 1749 | HOB-4 |
| **The Lay-By** - three hedge mages, nine years, no name | ZEPH-5 |
| **The Cinder Fen** - nine hundred acres, needs burning, forms required | ZEPH-4 |
| **The Wrong Dragon's lair** - elderly, well read, not a dragon | ALD-6 |
| **The Fair** - Mother Selvidge, twopence | COR-4 |
| **Ashcombe Lake** - drawn down one week a year | COR-2 |
| **The Duck's pond** - four miles from the Collegium | ZEPH-2 |

---

## 4. New NPCs

| who | where | what they are | quests |
| --- | --- | --- | --- |
| **Prioress Aveline Stope** | Sisterhouse (L4) | runs Whatever Works; has begun holding symposia and knows it is a bad sign | MER-1 |
| **Sister Bewick** | Sisterhouse (L4) | Order of What Ought To Work; losing patients, winning arguments, entirely sincere | MER-1 |
| **Tobias Frayne** | coast road cottage | revived eleven times; has developed a relationship with mortality | MER-4 |
| **The Parish Clerk of Sump** | Sump (L8) | cannot allocate the wasps | MER-5 |
| **Elias Meech** | the Sky Anvil | will not sell a very good gatepost; will trade for a gate | HOB-4 |
| **The Wardens of the Company of Smiths** | Great Dunnage (L1) | judge work triennially; have a schedule of what constitutes a piece | HOB-1 |
| **Sub-Librarian Prewitt** | Collegium (L2) | immovable, courteous, correct; holds the largest number in the game | ZEPH-1 |
| **Dean Fenwold** | Collegium (L2) | is fine, has a talk about it, did not back her up once | ZEPH-3 |
| **The Duck** | Collegium (L2) | honorary Fellow, holds a chair, votes, four hit points | ZEPH-2, WRE-1 |
| **The Drainage Commissioner** | Cinder Fen | wants nine hundred acres burnt, in triplicate | ZEPH-4 |
| **Wharfinger Tibbs** | Bonded Warehouse (L1) | has held a coat for eleven years and never asked why | NIX-1 |
| **The Mayor of Great Dunnage** | Great Dunnage (L1) | reading the preamble | NIX-2 |
| **Cobb Lorrimer** | anywhere | steals things, says so, is insulted by vocabulary | NIX-3 |
| **Hester Vane** | Little Gore (L8) | was married nine years ago; keeps the invitation | ALD-1 |
| **Chapter Clerk Mordaunt** | Coldbarrow (L6) | nine pins, one knight, a committee, a review | ALD-3 |
| **The horse** | haulage yard (L1) | fine. Doing well. Effectively a partner | ALD-4 |
| **Pemberton-Gore IV** | mobile | nineteen, magnificent, found the gate first time | ALD-5 |
| **The Wrong Dragon** | its lair | elderly, well read, delightful, not a dragon | ALD-6 |
| **Ambrosine Quill** | Prophecy Hall | wrote the authorised version before he left; it is better | PIP-1 |
| **The Bell's judges** | Great Dunnage (L1) | one of them cannot hear; the birdcall man wins | PIP-3 |
| **Mrs Ash** | Ashcombe (L3) | fine; new kitchen; knits | COR-1 |
| **The Ashcombe Drainage Museum curator** | Ashcombe (L3) | proud | COR-1 |
| **Five doomed rivals** | Sable Hart (L7) | a rota, a newsletter, a league table | COR-3 |
| **Mother Selvidge** | the Fair | twopence; four young men a year; never wrong | COR-4 |
| **Appraiser Fettle** | L1 or L2 | enthusiastic about the tang; has a form for curses | COR-5 |
| **Rowbotham's three students** | Collegium (L2) | reviewed her once, at twenty-three | WRE-1 |
| **The Gloamwood Thing Appreciation Society** | an inn | nine members, forty years, an annual walk | WRE-3 |
| **Mr Ottershaw** | Fenmarch (L5) | ninety, unrepentant, an artist, will show you the joins | WRE-4 |
| **The Convenor** | L1 or L2 | chairs the review; thanks him for his patience | ROL-1 |
| **Eleven previous parties** | Slain Wyvern | all finished without him; all slightly hurt | ROL-3 |
| **The understudy** | mobile | sixteen, extraordinary, asks the question | ROL-5 |

---

## 5. What depends on what

| location | quests that need it | companions unlocked |
| --- | --- | --- |
| **L1 Great Dunnage** | HOB-1, NIX-1, NIX-2, ALD-4, PIP-3, COR-5, ROL-1 | Hob, Nix, Aldric, Piper, Corvin, Roland - **six** |
| **L2 Collegium** | ZEPH-1/2/3, WRE-1, ROL-1 alt | Zephyrine, Wren, Roland - **three** |
| **L3 Ashcombe** | COR-1, COR-2 | Corvin |
| **L4 Sisterhouse** | MER-1, MER-3 alt, ALD-2 alt | Merribell, Aldric |
| **L5 Fenmarch** | ALD-1, ALD-5, WRE-4 | Aldric, Wren |
| **L6 Coldbarrow** | ALD-3, ALD-2 | Aldric |
| **L7 Sable Hart** | COR-3, COR-4 alt | Corvin |
| **L8 Little Gore / Sump** | ALD-1, MER-5, PIP-4 | Aldric, Merribell, Piper |
| **no new map at all** | MER-2, MER-4, HOB-2, HOB-3, HOB-5, ZEPH-5, NIX-4, NIX-5, PIP-2, PIP-5, WRE-2, WRE-3, WRE-5, ROL-3, ROL-4, SPA-1 | **all nine** |

That last row is the important one. **Sixteen of the forty-nine quests here need
no new map**, and four of the best - MER-2, PIP-2, ROL-4 and WRE-2 - need
nothing but appended pages on people who already exist. If the schedule
collapses, that row is the shippable game.

---

## 6. If only some of it gets built

**Build in this order.**

1. **The no-map row.** Sixteen quests, appended pages, no new art, no new
   terrain, and it gives every one of the nine companions something. MER-2's
   nine witness pages and PIP-2's nine terrible rhymes are the same cheap
   pattern and are both funnier than anything a new town will produce.
2. **L1 Great Dunnage.** Six companions off one town, and it is the location the
   finished game is already pointing at - Cotter is down the valley at the big
   foundry, and has been since the north was written.
3. **L2 The Collegium.** Three companions, one set of maps, and it holds the
   duck, which is the best single joke in the document.
4. **L3 Ashcombe**, for Corvin, because his is the only bio in the game that has
   a whole town implied by it and no town.
5. Everything else, in whatever order somebody feels like.

**One per companion, if it has to be one per companion:** MER-2, HOB-2, ZEPH-1,
NIX-1, ALD-4, PIP-2, COR-1, WRE-2, ROL-4. Four of those nine need no new map.

---

## 7. What it would cost

Sketched, not specified. Nothing below is reserved yet.

| new | rough size |
| --- | --- |
| Maps | 5 (Dunnage) + 3 (Collegium) + 3 (Ashcombe) + 2 (Sisterhouse) + 2 (Fenmarch) + 1 (Coldbarrow) + 1 (Sable Hart) + 2 (hamlets) = **19**, and a companion-quest tier that ships half of them is not a failure |
| Switches | 9 x `SW_<NAME>_STORY` + roughly 3 per quest built |
| Variables | 1 (`VAR_COMPANION_STORIES`) |
| Enemies / Troops | the vigil troop (ALD-2), the heckling troop (PIP-3), eleven type specimens (WRE-1), Roland's afternoon (ROL-2) |
| Weapons / Armors | one per companion minimum, per 1.2 |
| Build modules | one per location cluster: `dunnage.py`, `collegium.py`, `outlands.py` for the small sites, and a `companions.py` for the sixteen map-less ones, which will be the largest of them |
| Faces | **the blocker, exactly as it was for the north.** People1-4 are exhausted and the SF sets carried the north. Thirty-one new speaking NPCs is more faces than remain. Doubling up is established practice and Halbert Quy is the precedent, but this needs auditing before a line is written, not after |

Three risks worth writing down now:

* **The ending's tally.** 1.4 exists because this document could put fifty
  blocks in it. Nine, plus a counter, or the finale stops being funny.
* **The blush threshold.** Merribell and Wren will generate Register A moments
  the way Ott did. Every one moves the tier. `journey.py`'s comment is where
  this gets settled.
* **The party of four.** Nine companion stories in a game that shows you three
  is either the best thing in the design or a great deal of work nobody sees.
  It is the former **only if the game tells the player it happened** - so the
  ending's line about how many of them got something out of it is not a
  flourish, it is the feature that makes the other eight exist.
