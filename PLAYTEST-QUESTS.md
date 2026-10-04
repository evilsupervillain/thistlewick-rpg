# Playing through the companion quests

A walkthrough of the forty-six companion quests built in `QUESTS.md` Parts A-E
(30 September - 3 October 2026), for playing every one of them before the push.
Spare's four (F1-F4) are not built and are not here.

Each entry says **who** has to be in the party, **when** it opens, **where** to
go, and **how** to finish it, then what to look at **afterwards** and the
**switches** to check or set if you want to jump ahead in a test save. The
scripted version of each is `build/scenarios/q_<quest>.json`; its steps
are the same route, with exact coordinates.

---

## How these quests behave

* **A "second look"** is the commonest start. Talk to the person (or read the
  thing) once with anybody - that is the published scene, word for word, even
  with the companion standing there - then talk to them **again** with the
  companion in the party. Most quests below start that way, and an entry that
  says "second look" means exactly this.
* **World-map sites ask first.** Walking onto a site cell gives "Stop a while /
  Press on" (or "Look in", "Call in"); the first stop is the published one, and
  the quest is on a later stop.
* **A dismissed companion's errand waits.** All quest state is global, so you
  can swap people at the roster desk mid-quest; the person who needs them says
  so and waits. Only the beats marked "needs X" need them present.
* **One companion per page.** Where a quest needs two companions (ROL-4: Roland
  and Hob) both must be in the party at once.
* **Afterwards** is usually the person's own last line plus one new line, for
  everybody, with or without the companion. Worth checking on a second pass
  without them.
* **Counters.** Most quests add one to the tropes counter (variable 2); a few
  add a blush (variable 7). Each quest's finish turns on that companion's story
  switch (101-109) and counts variable 15 the first time.

### Story progress that opens quests

| switch | meaning | what it opens |
| --- | --- | --- |
| 2 | left Thistlewick | PIP-2, PIP-1, HOB-3 (and so HOB-2, HOB-4) |
| 3 | the Gloamwood cleared | NIX-5, WRE-3 |
| 32-33 | the lighthouse lit (`SW_LAMP_LIT` is 33) | MER-2's last fetch |
| 47 | been to Upper Clanging | NIX-4 (and so NIX-1) |
| 58 + 70 | Hob and Bryd's drink; Ott's flying chain finished | HOB-5 |
| 21 | Roland has left at the tower door | **closes every Roland quest**; opens ROL-4's refit |

### Where the companions are recruited

| who | where |
| --- | --- |
| Merribell | the Chapel of Whatever Works, Thistlewick (Map 5) |
| Hob | Grumnir's Smithy, Thistlewick (Map 6) |
| Zephyrine | the Gilded Turnip, Thistlewick (Map 4) |
| Piper | the Gilded Turnip (Map 4) |
| Nix | Nix's Emporium, Thistlewick (Map 7) |
| Sir Aldric | Thistlewick's street (Map 1, by (22,16)) |
| Corvin, Wren, Roland | the Slain Wyvern, Nether Sopping (Map 14) |

### Chains: what has to come first

| quest | needs first |
| --- | --- |
| HOB-2 | HOB-3 (the anvil back) |
| HOB-4 | HOB-2 |
| NIX-1 | NIX-4 |
| ZEPH-3 | ZEPH-1 (either ending) |
| ZEPH-2 | ZEPH-3 |
| WRE-1's third reviewer | the duck at its pond, so not while ZEPH-2 has it out walking |
| ALD-5 | ALD-1 |
| COR-2 | COR-1 |
| ROL-5, ROL-2 | ROL-1 |
| every ROL quest except ROL-4's refit | Roland still in the party, so **before the tower door** |
| ROL-4's refit | Roland gone (the tower door), and the mark seen first |

### World-map places used

Thistlewick (60,79); Nether Sopping (71,84); Upper Clanging (44,47);
Gloamwood mouth (52,62); the Tower (66,43); Tobias Frayne (66,82); the Lay-By
(11,88); the Sky Anvil (76,26); the Cinder Fen (47,118); the Wrong Dragon
(110,114); the Fair (67,115); Ashcombe Lake (104,54); the Duck's Pond
(115,40); Coldbarrow (50,19); the Sable Hart (24,75); Little Gore (97,101);
Sump (78,102); Ashcombe (102,55); Weeping Bottom (58,99); Fenmarch Hall
(86,114); the Collegium Arcanum (112,38); Great Dunnage (31,52); Carn Drey
(39,55, appears during ROL-2).

---

## Merribell

### MER-2 Fit To Travel (A4)
* **Party:** Merribell, plus **a third member** (the witness - whoever is first
  in the party after Bram and Merribell).
* **Opens:** any time you can reach Upper Clanging; the last fetch needs the
  lighthouse lit.
* **Start:** Upper Clanging, the **Parish Notices** (Map 21) with Merribell -
  clause eleven, and a pad of blank fitness forms (item 41).
* **Do:**
  1. Nether Sopping's **fish stall**: it lends its stamped scales (item 42) -
     anybody can collect them once the form is in the bag.
  2. Have the **lighthouse lit** (the lighthouse quest).
  3. Anywhere, with Merribell and a witness: **use the blank form from the Key
     Items menu.** It names whatever is still missing, in order. The
     examination plays out with the witness reacting; it can only happen once.
* **Get:** Certificate of Fitness (item 43). One trope, three blushes.
* **Try:** a different witness each time you replay it - eight branches (Sir
  Aldric shields Bram with his cloak, facing the wrong way).
* **Switches:** 115 asked, 116 scales, 117 done; variable 16 the witness.
  Scenario `q_mer2` (long).

### MER-4 The Man Who Cannot Stay Down (A7)
* **Party:** Merribell.
* **Start:** Tobias Frayne's cottage (66,82). **Second look** at Tobias with
  her.
* **Do:** he refuses a twelfth revival - there is nothing wrong with him, which
  is the trouble - and the jar pays out **1,100 crowns**. Then simply **walk
  out of the cottage**: leaving is the cure.
* **Afterwards:** Tobias has had the parish to tea; the mended rung; the empty
  jar; the twelfth line of his book left blank. The door, ladder, book and jar
  each have a page. One trope, one blush (the coccyx).
* **Switches:** 123 told, 124 done. Scenario `q_zeph5_mer4`.

### MER-5 The Well at Sump (E1)
* **Party:** Merribell (for the start and the cure).
* **Start:** Sump (78,102). **Second look** at Mr Thurle with her - she
  re-forms the Water Committee (one member). A blush.
* **Do:**
  1. **Mrs Pardew** (anybody, once the Committee sits): her gran's last jar of
     gooseberry jam (item 67).
  2. **The well**, with Merribell and the jam: the Standing Orders for the
     Lifting of the Curse, clause by clause, and the Rule of Life (item
     three: water, sit down, dry socks, see how you feel).
* **Afterwards:** Thurle, Gammage, Pardew, the well, the minutes and the sign
  all change.
* **Switches:** 175 on, 176 done. Scenario `q_mer5`.

### MER-1 The Sisterhouse (E2)
* **Party:** Merribell.
* **Start:** Weeping Bottom (58,99), the ward. **Second look** at the Prioress
  with her - the queue proposal, Sister Bewick's eleven clauses.
* **Do:** in the same conversation, "Begin" (or "Not yet"). Four patients,
  each asking for one of the Rule's four answers (water, sit down, dry socks,
  have you eaten?). The right answer scores a point; the queue of six stands
  outside in the rain. Then Bewick is examined on the Pamphlet, and passes. A
  blush.
* **Get:** The Pamphlet (armour 45, Merribell's own gear).
* **Switches:** 177 on, 178 done; variable 25 the points. Scenario `q_mer1`.

### MER-3 The Healers' Table (E3)
* **Party:** Merribell.
* **Start:** the Slain Wyvern (Map 14). With her, a **door appears** in the
  bar's north wall at (15,3), between the bookcase and the red curtain; Ysolde
  calls her in.
* **Do:** through the door to the back room; talk to **Ysolde in the chair** -
  the four visiting healers' stories, then Merribell's.
* **Get:** the Table's Kit (armour 46, anybody's).
* **Afterwards:** the back room empty, and the card: NEXT YEAR. SISTER M.
  (THISTLEWICK) TO SPEAK.
* **Switches:** 179 on, 180 done. Scenario `q_mer3`.

---

## Hob

### HOB-5 Two Smiths, One Forge (A6)
* **Party:** Hob (for the forging only).
* **Opens:** after the Two Hundred's spar, Hob and Bryd's drink (58), and **Ott's
  flying chain** finished (70).
* **Start:** Upper Clanging, Ollerenshaw's forge (Map 24): Bryd, with Hob.
* **Do:**
  1. The forging - nobody finishes a sentence. You get the tube plate (item
     44).
  2. Carry it up to **Ott** at the works (Map 22) - anybody can. She tries each
     hole with her little finger (a blush).
  3. Back to **Bryd** for the telling.
* **Switches:** 120 forged, 121 done. Scenario `q_hob5`.

### HOB-3 The Anvil (A8)
* **Party:** Hob.
* **Opens:** after leaving Thistlewick (2).
* **Start:** walk into Grumnir's Smithy with Hob - **an autorun**: the anvil is
  gone.
* **Do:** outside, three squares south-east of the smithy door (Map 1, (9,33)):
  the anvil face down on the grass with two apprentices flat either side. Talk
  to the anvil with Hob. Meredith Crooke runs the course (her line changes if
  you beat her bounty).
* **Get:** the apology (item 45). The anvil goes home.
* **Note:** with Roland too, this comes before ROL-4's mark at the anvil.
* **Switches:** 125 gone (ends), 126 done. Scenario `q_hob3`.

### HOB-2 The Grave He Has Not Made (A13)
* **Party:** Hob.
* **Opens:** HOB-3 done.
* **Start:** walk into the smithy with Hob - **an autorun** at the forge;
  Beatrice goes quiet.
* **Do:** four attempts. Each time: make it at **the forge** (Map 6, by the
  hearth), carry it to **Beatrice Grumnir's grave** in the new churchyard east
  of the chapel (Map 1, (35,4)). Roses, a cross, a plate - "No." The fourth is
  **a gate**, hung at the churchyard gate as you walk through it.
* **Get:** Something To Say (weapon 41, an axe, Hob's best).
* **Switches:** 137 on (ends), 138 carrying (ends), 139 done; variable 20 the
  try. Scenario `q_hob2`.

### HOB-1 The Assize of Hammers (B1)
* **Party:** Hob; **Nix** once, for the eleventh.
* **Start:** Great Dunnage, the Smiths' Hall (Map 62). **Second look** at the
  Prime Warden with Hob. The tally is eleven pieces of Hob's work, counted on
  his fingers.
* **Do:** with Hob, ask each owner for their piece back (each says no, with a
  reason - that is the count): the Farmer and the Gossip (Thistlewick), the Man
  Having A Day Off (Nether Sopping), Hithermost's villager, Perce Stagg
  (Frostwick), King Aldous (Fairholme), Mrs Dimmock (Ashcombe), Dame Winifred
  (Little Gore), Cotter (Great Dunnage, the Iron Company's gate), Warden
  Crabbe (the Smiths' Hall). **Nix's lockpicks** are asked at the Prime
  Warden's table with Nix and Hob in the party together. At eleven, back to
  the Prime Warden: the submission, Beatrice on the table, **disqualified**.
* **Get:** the Wardens' notes (item 50). The Prize gets a second card.
* **Switches:** 142 on, 143 picks, 144 done; variable 22 asked. Scenario
  `q_hob1` (long).

### HOB-4 The Sky Anvil (E15)
* **Party:** Hob.
* **Opens:** HOB-2 done.
* **Start:** the Sky Anvil (76,26). Stop once (the published scene), then stop
  again with Hob.
* **Do:** he makes Elias Meech a gate out of the eleven old gates, with the
  spring for the latch, and lifts out the star-iron (item 71). Take it to
  **the forge** in the smithy with Hob.
* **Get:** Star-Iron Sword (weapon 42) - Hob can't hold it; he won't say who it
  is for. Bram can.
* **Switches:** 200 traded, 201 done. Scenario `q_hob4`.

---

## Zephyrine

### ZEPH-5 The Lay-By (A7)
* **Party:** Zephyrine.
* **Start:** the Lay-By (11,88). Stop once, then stop again with her.
* **Do:** the hedge mages' admission: Dunnock's Kindle from the book with four
  pages missing.
* **Get:** skill Page Twenty-Three (46). One trope.
* **Switches:** 122 done. Scenario `q_zeph5_mer4`.

### ZEPH-1 The Fines (C1) - two endings
* **Party:** Zephyrine (for the letter and the decision).
* **Start:** the Gilded Turnip, her old table at (12,6): with her, a letter
  (item 53, the eleventh notice of fines).
* **Do:**
  1. The Collegium (112,38): the gate lets her in now. Mr Gedge in the Lodge
     knew.
  2. The **Library** (Map 59): Mr Pennock, at the east end of Prewitt's desk,
     with her. There was never an expulsion; she owes **4,117,206 crowns and
     ninepence**.
  3. Choose: **turn out the purse** (takes **every crown you have**; her name
     back, the robe, a slide on the IN and OUT board), **file the expulsion**
     herself (free), or **not today**.
* **Get:** on the paid ending, Collegium Robe (Vance) (armour 43).
* **Test both:** save before Pennock. Later Collegium quests read which.
* **Switches:** 155 on, 156 told, 157 paid, 158 expelled, 159 done; variable 23
  what was paid. Scenario `q_zeph1`.

### ZEPH-3 Dean Fenwold Is Fine (C2)
* **Party:** Zephyrine.
* **Opens:** ZEPH-1 done.
* **Start:** the Collegium Hall (Map 60). **Second look** at the Dean with her.
* **Do:** "No." then "On terms." The rehearsal - the undergraduate's bucket,
  the room is wrong, and the biggest fire in the game. No consequences.
* **Afterwards:** the Dean's talk, his portrait's second card, Dr Hapgood's
  offprint, the undergraduate kept the bucket.
* **Switches:** 160 done. Scenario `q_zeph3`.

### ZEPH-2 The Duck (C3)
* **Party:** Zephyrine.
* **Opens:** ZEPH-3 done.
* **Start:** the Great Court (Map 58), Congregation's notice: INQUORATE. Read it
  with her.
* **Do:**
  1. The Duck's Pond (115,40): stop with her - the duck comes (item 54).
  2. Back to the Collegium - the duck walks into Mr Gedge.
  3. The Hall: the **Honorary Fellow's chair** (read it once first), with her:
     the vote, quorate for the first time in eleven years.
* **Get:** the Duck's Proxy (item 55, replaces the duck).
* **Switches:** 161 on, 162 walking (ends), 163 done. Scenario `q_zeph2`.

### ZEPH-4 The Cinder Fen (E16)
* **Party:** Zephyrine.
* **Start:** the Cinder Fen (47,118). Stop once (the Commissioner: "Are you a
  fire person?"), then stop again with her.
* **Do:** the form in triplicate, QUANTITY OF FIRE, SANCTIONED, and the Fen
  burns all night. (The fire line differs if ZEPH-5 is done.)
* **Get:** Certificate of Burning (item 72). **The road:** the Fen now offers
  "Take the causeway" to Great Dunnage's gate, and a new signpost beside
  Great Dunnage (33,53), read from beside, takes you back to the Fen.
* **Switches:** 202 done. Scenario `q_zeph4`.

---

## Nix

### NIX-4 The Longest Loan (A9)
* **Party:** Nix.
* **Opens:** after Upper Clanging (47).
* **Start:** Nix's Emporium (Map 7), the **ledger**, with her: eleven things
  that were never sold (item 46, eleven of them).
* **Do:** give each back, with Nix. Most owners need to have been spoken to
  once first. Thistlewick: Bram's mother, the Old Man, the Fisher, the
  Gatekeeper. Nether Sopping: the Ferryman (pays a penny), Councillor Dree,
  Tolly, **Hulda Bole** (gives Nix a parcel, item 47). Upper Clanging: Old
  Sowerby, Nib, Bessie Marsden (a blush). Then back to the ledger.
* **Switches:** 127 begun, 128 done; variable 17 returned. Scenario `q_nix4`
  (about 25 minutes).

### NIX-5 Half An Encounter (A10)
* **Party:** Nix.
* **Opens:** the Gloamwood cleared (3).
* **Start:** the Gloamwood mouth (52,62): Enoch Bagshawe on the milestone, with
  Nix (a blush, once).
* **Do:** cross the whole wood, south to north, **without a single battle** -
  running away counts as one. Leaving by the south end abandons it; a battle
  fails it. Either way he waits for another night.
* **Get:** 300 crowns and a receipt.
* **Switches:** 129 on (ends), 130 done; variable 18. Scenario `q_nix5`.

### NIX-1 The Client Identifies Themselves (B5)
* **Party:** Nix.
* **Opens:** NIX-4 done.
* **Start:** the Emporium ledger, with her: the letter (from herself, aged
  fifteen) and Bond No. 1's ticket (item 51).
* **Do:** Great Dunnage: the **Bonded Warehouse door** (it refused her before)
  with Nix and the ticket; inside, **Mr Tibbs** (second look) with Nix.
* **Get:** Gran's Coat (armour 42, Nix's gear).
* **Switches:** 149 letter, 150 done. Scenario `q_nix1`.

### NIX-2 The Sealed Counting House (B6)
* **Party:** Nix (for the opening only).
* **Start:** Great Dunnage, the Counting House (Map 63). **Second look** at the
  Mayor with her: nine seconds, two clicks.
* **Do:** go through the Door into the room behind it; the chair.
* **Get:** 1,788 crowns (WE SPENT IT).
* **Switches:** 151 open, 152 done. Scenario `q_nix2`.

### NIX-3 Professional Courtesy (E14)
* **Party:** Nix.
* **Start:** Nether Sopping, the Adventurers' Guild (Map 15): Cobb Lorrimer,
  with her.
* **Do:** the children's list. With Nix, at three of the town's shut doors: the
  **Net Loft** (the rope), the **front door nobody answers** (wait an hour: a
  helmet), the **boat shed** (the Ferryman's oar). Then Lorrimer on the
  front by Sops and Tibb (26,19): the judging, and the Dark Lord post.
* **Get:** Lorrimer's Tools (armour 48).
* **Switches:** 198 on (ends), 199 done; variable 27. Scenario `q_nix3`.

---

## Sir Aldric

### ALD-4 The Horse (B2)
* **Party:** Aldric.
* **Start:** Great Dunnage, the haulage yard (north-west): **second look** at Mr
  Plummer with him. Duchess, wordless.
* **Get:** nothing, on purpose.
* **Switches:** 145 done. Scenario `q_ald4`.

### ALD-3 The Chapter House (E4)
* **Party:** Aldric.
* **Start:** Coldbarrow (50,19). **Second look** at Mordaunt with him.
* **Do:** the committee, the offer, the refusal, the pin.
* **Get:** his nickname becomes **Knight Errant, At Large** (status screen). The
  great map loses his red pins.
* **Switches:** 181 done. Scenario `q_ald3`.

### ALD-1 The Errand (E5)
* **Party:** Aldric (for the delivery).
* **Start:** Little Gore (97,101), **the banns** board, with him: the letter
  nine years late (item 68).
* **Do:** choose the route ("Follow him" - the long way - or the short way).
  Then **Mrs Vane** (second look) with Aldric and the letter.
* **Switches:** 182 done. Scenario `q_ald1`.

### ALD-5 Pemberton-Gore the Fourth (E6)
* **Party:** Aldric.
* **Opens:** ALD-1 done.
* **Start:** Little Gore: the Fourth by the road (14,16).
* **Do:** meet him with Aldric. Then Fenmarch Hall's world-map door lets
  Aldric in; the Third's portrait in the gallery.
* **Check:** with Aldric in the party, the Fourth follows him at six places
  (Thistlewick, Nether Sopping, Coldbarrow, Little Gore, Weeping Bottom, Great
  Dunnage).
* **Switches:** 183 done. Scenario `q_ald5`.

### ALD-2 The Vigil (E7)
* **Party:** Aldric.
* **Start:** Weeping Bottom ward. **Second look** at Sir Hamo with him -
  "Tonight / Not yet".
* **Do:** the vigil in the chapel: a defence battle. Aldric kneels and cannot
  act, and draws nearly every attack. **Keep him alive until the end of turn
  five** (dawn). If he falls the vigil breaks; if everybody falls it's lost;
  either way it waits for another night.
* **Get:** Shield (Regardant) (armour 47, Aldric's gear).
* **Switches:** 184 done. Scenario `q_ald2`.

### ALD-6 The Wrong Dragon (E8)
* **Party:** Aldric.
* **Start:** the Wrong Dragon's cave (110,114). Stop once, then "Call in" again
  with him.
* **Do:** Horace was the horse; the lamp; the Odes. The line about Horace
  changes if ALD-4 is done.
* **Switches:** 185 done. Scenario `q_ald6`.

---

## Piper

### PIP-2 A Rhyme For Turnip (A3)
* **Party:** Piper, plus whoever else - **each companion present gives a
  suggestion** (and a trope); Merribell's is a blush.
* **Opens:** after leaving Thistlewick (2).
* **Start:** the Gilded Turnip, the **gilded turnip** on its plinth, with her.
* **Test:** replay with different parties to hear all eight companions.
* **Switches:** 114 done. Scenario `q_pip2`.

### PIP-5 The Struck Verses (A12)
* **Party:** Piper, plus **a third member** (the decoy).
* **Start:** Prophecy Hall (Map 3): the fete minutes, second look with her.
* **Do:**
  1. Form S-7 from the **Committee Records**.
  2. Countersigned by **the Councillor on the wording**.
  3. **Councillor Fenn** - nobody listens to him; your third member does, and
     the key comes off his hook.
  4. The curtained window on the north wall (16,4) is a door marked STRUCK:
     the archive, and **the box**, with Piper. A blush.
* **Switches:** 133-136; variable 19 the decoy. Scenario `q_pip5`.

### PIP-3 The Contest at the Sign of the Bell (B3)
* **Party:** Piper.
* **Start:** Great Dunnage, the Bell (Map 65). **Second look** at Mrs Harbottle
  with her.
* **Do:** talk to her again: "Begin". Two acts, the thrush, then Piper's set -
  a fight against the hecklers (can be lost; she finishes anyway). Second
  place by one point.
* **Get:** Rosette, Second Place (armour 41, Piper's gear).
* **Switches:** 146 on (ends), 147 done. Scenario `q_pip3`.

### PIP-4 The Elegy (E12)
* **Party:** Piper.
* **Start:** Little Gore, the **fingerpost** (the back of it), with her.
* **Do:** interview eleven people about Abel Thrush, with Piper (those with a
  ladder need speaking to once first). Little Gore: Mrs Vane, Dame Winifred,
  Bess, Alfie, Nell. Fenmarch: Tom, Mrs Puddifoot, Mr Ottershaw, the Fourth.
  Sump: Mr Gammage, Mrs Pardew. Then back to the fingerpost.
* **Get:** Elegy (Nine Lines) (item 69).
* **Switches:** 192 on (ends), 193 done; variable 26 heard. Scenario `q_pip4`.

### PIP-1 The Authorised Version (E13) - two endings
* **Party:** Piper.
* **Opens:** after leaving Thistlewick.
* **Start:** Prophecy Hall: **Ambrosine Quill** at the table by the door (7,12).
* **Do:** the four cantos (Merribell in the party changes canto nine). Then:
  **Fight it** (filed under no change; asked again next time), **It's very
  good** (one footnote), or **Fix it** (a goat where the wolf was).
* **Get:** the Authorised Version (item 70). The Wall of the Forty-Seven gets a
  card either way.
* **Test both:** save before choosing.
* **Switches:** 194 on, 195 good, 196 fixed, 197 done. Scenario `q_pip1`.

---

## Corvin

### COR-5 The Appraisal (B4)
* **Party:** Corvin.
* **Start:** Great Dunnage, the Smiths' Hall: **second look** at Miss Fettle
  with him. The tang. A blush.
* **Do:** optional: "Have it cursed" for 30 crowns - Cursed (Elective). She
  takes it off for nothing; any inn's night clears it.
* **Switches:** 148 done; state 40. Scenario `q_cor5`.

### COR-1 Ashcombe (New) (D1)
* **Party:** Corvin.
* **Start:** Ashcombe (102,55), the Drainage Museum: **the Roll** - the first
  read with him is the published one; read it **again**.
* **Do:**
  1. **Mrs Ash's door** (it always refused him) with Corvin.
  2. **Mrs Ash** in the kitchen with him.
  3. Up the new stair in the kitchen's north wall (6,3) to the study: **the
     Committee's desk** - this year's invitation (item 65). The height marks.
  4. **The Flood Dinner notice** in the street, with Corvin and the
     invitation: "Confirm the speaker" - the speech.
* **Get:** Scarf (Wrong Colour) (armour 44, Corvin's gear).
* **Switches:** 170 on, 171 home, 172 done. Scenario `q_cor1`.

### COR-2 Ashcombe (Old) (D2)
* **Party:** Corvin.
* **Opens:** COR-1 done.
* **Start:** Ashcombe Lake (104,54), with him, after a first stop: the lake is
  down - "Walk down".
* **Do:** the drowned street (Map 66): **the doorstep** first, then **the
  strongbox** (the report card, item 66). The pub sign and the church are
  extra. Out by the slope.
* **Switches:** 173 step, 174 done. Scenario `q_cor2`.

### COR-3 The Rivals' Retreat (E10)
* **Party:** Corvin.
* **Start:** the Sable Hart (24,75): **the league table** with him -
  seventeenth.
* **Do:** **second look** at Crake with him: the meeting. Second, behind the
  scar.
* **Switches:** 189 on, 190 done. Scenario `q_cor3`.

### COR-4 Mother Selvidge (E11)
* **Party:** Corvin.
* **Opens:** you have paid her once (as anybody), at the Fair.
* **Start:** the Fair (67,115). Stop again with him.
* **Do:** three readings for two crowns.
* **Switches:** 191 done. Scenario `q_cor4`.

---

## Wren

### WRE-2 The Second Plaque (A1)
* **Party:** Wren (for the ask and the handover).
* **Start:** the Slain Wyvern, **the goose** (second look) with her.
* **Do:** Wick & Barrow's (Map 16): **the engraving card** in the basket by Mrs
  Barrow, with Wren; then pay **128 crowns** (anybody). Back to the goose with
  Wren and the plate (item 40).
* **Afterwards:** the second plaque, right of the fireplace.
* **Switches:** 111 asked, 112 up. Scenario `q_wre2`.

### WRE-5 Bramus (A2)
* **Party:** Wren.
* **Start:** Bram's field (Map 1), a burrow in the fourth soil row (15,27),
  with her.
* **Switches:** 113 named. A trope and a blush. Scenario `q_wre5`.

### WRE-3 The Thing In The Gloamwood (A11)
* **Party:** Wren.
* **Opens:** the Gloamwood cleared (3).
* **Start:** the Gilded Turnip: the Gloamwood Society's table - **Mrs Lumb**,
  with Wren.
* **Do:** the society walks to the deep clearing in the Gloamwood (Map 10);
  meet them there and talk to Mrs Lumb with Wren. Nine snakes, courting. A
  blush.
* **Get:** Gloamwood Society Badge (armour 40, Wren's gear).
* **Switches:** 131 walk (ends), 132 done. Scenario `q_wre3`.

### WRE-1 The Monograph (C4)
* **Party:** Wren.
* **Start:** the Collegium Library: **the monographs shelf** - the first look
  with her is the published one; look **again** (the card in the gap).
* **Do:**
  1. **Eleven type specimens** - tracks on the world map, each 3-4 steps off a
     place. With Wren: "Measure it", and a fight with no escape. Firstfield
     (52,74), Restwell (40,81), the Cinder Fen (44,118), Thistlewick (57,79),
     Fairholme (105,76), the Sable Hart (21,75), Gladhollow (30,111),
     Frostwick (58,21), the Sky Anvil (73,26), Weeping Bottom (56,98),
     Ashcombe Lake (103,56).
  2. **Two reviewers** at the Library's reading table, after the specimens:
     Professor Mott and Dr Furze. The second names the third:
  3. **The duck**, at its pond (115,40) - not while ZEPH-2 has it out.
  4. **The subscription list** on Prewitt's desk: a shop. Buy **six** at 150
     crowns each.
  5. Back to the shelf: publication.
* **Get:** the Monograph (item 64); Wren's class becomes Cataloguer
  (Published) - fewer surprises, more pre-emptive attacks.
* **Switches:** 164 on, 165 Mott, 166 Furze, 167 duck due (ends), 168 duck, 169
  done; variable 24 specimens. Scenario `q_wre1`.

### WRE-4 The Cabinet (E9)
* **Party:** Wren.
* **Start:** Fenmarch Hall, the gallery (Map 57): **second look** at Mrs
  Puddifoot with her.
* **Do:** **Mr Ottershaw** with Wren - the joins, and case forty. Back to **Mrs
  Puddifoot** for the write-up.
* **Get:** 600 crowns.
* **Switches:** 186 on, 187 joins, 188 done. Scenario `q_wre4`.

---

## Roland - all before the tower door

### ROL-4 The Maker's Mark (A5)
* **Party:** **Roland and Hob together** for the mark; **Hob** for the refit.
* **Start:** Grumnir's Smithy, **the anvil** (Beatrice), with both. "She did
  good work."
* **Then, after the tower door** (Roland has left Fairweather's Own): Hob at the
  anvil with the sword - the refit, if you accept.
* **Get:** the refit is Rehafted (weapon 40, an axe, Hob's).
* **Switches:** 118 seen, 119 refit. Scenario `q_rol4`.

### ROL-3 The Alumni (A14)
* **Party:** Roland.
* **Start:** the Slain Wyvern, **Dorcas's Board** (second look) with him: the
  dinner card.
* **Do:** eleven of his old parties fill the room. Talk to all eleven, then
  Dame Florence with Roland: the toast.
* **Get:** eleven small gifts (consumables).
* **Switches:** 140 dinner (ends), 141 done; variable 21 heard. Scenario
  `q_rol3`.

### ROL-1 The Appointment (B7)
* **Party:** Roland.
* **Start:** Great Dunnage, the Bell: **second look** at Mrs Dewhirst with him.
* **Do:** the snug: **the Convenor**, with Roland - the 141st meeting.
* **Get:** the Minutes (141st) (item 52).
* **Switches:** 153 on (ends), 154 done. Scenario `q_rol1`.

### ROL-5 The Understudy (E17)
* **Party:** Roland.
* **Opens:** ROL-1 done.
* **Start:** the Bell: **Maud Penhallow** at the snug table (south of it).
* **Do:** talk to her with Roland (he doesn't tell her); talk to her **again**
  (he does). Whose prophecy is it? Nobody answers.
* **Then, at the tower door:** she is standing beside it, and after Roland
  leaves there is a short scene with her (once).
* **Switches:** 203 on, 204 done. Scenario `q_rol5`.

### ROL-2 Roland's Own Quest (E18)
* **Party:** Roland (Piper for the best line).
* **Opens:** ROL-1 done.
* **Start:** the Bell: **the card** on the snug table, read from beside (from
  the seat north of it) with Roland. "Today".
* **Do:**
  1. A cave appears in the hill east of Great Dunnage (39,55): with Roland, "Go
     down".
  2. **The stone** at the foot of the stairs: draw the sword.
  3. **The Worm**, at the bottom of the room beyond, in the dark: a fight. It
     can be lost and retried.
* **Get:** at the tower door, Roland leaves **The Drawn Sword** (weapon 43)
  beside Fairweather's Own.
* **Afterwards:** the card and the cave's plate both say DONE.
* **Switches:** 205 on, 206 drawn, 207 done. Scenario `q_rol2`.

---

## A route through all of it

One way to order a full playthrough, keeping the chains and the tower door in
mind:

1. **Thistlewick** has nothing to start before you leave (switch 2).
2. **The south (Nether Sopping):** recruit Corvin, Wren and Roland; MER-3,
   WRE-2, ROL-3, NIX-3; then back to Thistlewick for WRE-5, PIP-2, PIP-1, PIP-5,
   HOB-3 and HOB-2.
3. **The Gloamwood cleared:** NIX-5, WRE-3.
4. **Upper Clanging:** MER-2 (after the lighthouse), NIX-4, then NIX-1; HOB-5
   once Ott has flown.
5. **The sites, by airship or on foot:** Great Dunnage (HOB-1, ALD-4, PIP-3,
   COR-5, NIX-1's warehouse, NIX-2, ROL-1, ROL-5, ROL-2), the Collegium
   (ZEPH-1, -3, -2, WRE-1 - start the specimens early), Ashcombe (COR-1,
   COR-2), Weeping Bottom (MER-1, ALD-2), Little Gore and Sump (ALD-1, ALD-5,
   PIP-4, MER-5), Fenmarch (WRE-4), Coldbarrow (ALD-3), the Sable Hart
   (COR-3), Tobias Frayne (MER-4), and the no-map sites (ZEPH-5, ZEPH-4,
   HOB-4, ALD-6, COR-4).
6. **ROL-4's mark, then the tower door** with Roland: he leaves (with ROL-5's
   scene and ROL-2's sword), then ROL-4's refit with Hob.
7. **The ending** - not yet extended for these (that is G1).

Save before the two-ending quests (ZEPH-1, PIP-1) and before ZEPH-1's purse,
which takes all your gold.
