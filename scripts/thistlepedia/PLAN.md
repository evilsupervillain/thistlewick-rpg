# The Thistle-pedia: the plan, and the notes it is built to

What is still to write, and the decisions taken with Mike that shape it.
`README.md` is how to maintain the wiki; `AFTERWARDS.md` is what became of
everybody. This file is the order of work and the rules that only matter
while writing it.

## The units

Each one ends with the checks in `README.md`, a commit, a push to
`thistlepedia`, and a pause for review.

1. **The scaffold and Hosea's front page.** Done.
2. **History**: The Prophecy of Thistlewick (its clauses), the Chosen Ones
   (#1-#48), the Quest of the Forty-Eighth, Two Reckonings, a Timeline. Done.
3. **The company**: Bram, the nine companions, Spare, Grimspite and Hosea,
   each with an infobox portrait and an Afterwards section that agrees with
   `AFTERWARDS.md`. Done.
4. **Places I**: Thistlewick, the road north and the Tower, and the south.
5. **Places II**: the north, and the world-map sites.
6. **Notable people**: the major characters who are not in the party.
7. **Institutions, the Bestiary, Arms and Artefacts, and the Glossary of
   Cliches.**
8. **The final pass**: cross-links, the search index, and a browser check of
   every page.

## Other hands

The wiki is Hosea's book, but he is a historian and knows when somebody else
knows better. **Where a section is better told by somebody in the game, it is
given to them**, as a contribution that Hosea has commissioned and printed
whole. He introduces it in a hatnote and may add his own `marginalia` at the
foot. He does not correct the contributor in the text, only beside it. A
contributor writes in their own voice from the game, keeps to the canon as
strictly as he does, and dates the piece on or before 21 March 2002.

The page shows who wrote it: a byline under the title, *Contributed by W.
Halloway*, and Hosea's introduction. The wiki needs two new content classes
for this, `.contributor` (the byline) and `.verse` (a song or poem, set as
verse), These go into `style.css` in the unit that first uses
them.

Who writes what. These are suggestions, and the rule above decides:

| hand | what | how it sounds |
| --- | --- | --- |
| **Wren Halloway** | **The Bestiary**, the whole volume: its index and every entry | a monograph. Each creature under what it *is*, with what people call it after. A method step where the fight was. Rowbotham's names given as synonyms and quietly demolished. The goose. `data/Enemies.json` notes are the facts |
| **Ott Hoyle** | **The technical articles**: the Two Hundred and every attempt in the Long Field, the airship, the works, ITEM 1 | a works memorandum. Numbered paragraphs, tolerances, CAUSE: UNDER REVIEW, ITEM numbers. The plaques and the attempt log are the source |
| **Piper Quill** | **Songs and tales**: excerpts set through the History and People volumes, and a page of her own, *From the Notebooks of P. Quill* | the third person, at volume, in metre, and true. Where the game already has lines of hers (the ballad, PIP-2's rhyme for turnip, the fingerpost at Little Gore), quote them exactly, and write new verse only around them. **Verse seven is never quoted, paraphrased or hinted at**, because the game must never say what is in it (`COMPANIONS.md`) |
| **Nix** | the provenance notes in **Arms and Artefacts** | ledger entries: item, got how, from whom, on behalf of the party of the second part |
| **Merribell** | a medical note or two (fitness to travel, adventurers' complaints) | the clinical words said plainly, and water |
| **Prosper Hollowell** | the Former Premises | the tour, as he gives it |
| **Grimspite** | letters to Hosea correcting dates, as `marginalia` or a short exchange | a beautiful hand, very tired, very polite. Never his age |
| **Spare Cotterill** | excerpts of his letters | four lines, untrue. Hosea files them under Fiction |

Ambrosine Quill's official account (if it is the edition with the wolf), the
Committee's minutes, Pargeter's reading of clause two and the Sable Hart's
newsletter are good for **quotation**, not for whole pages.

## Sir Dunstable: alive, or not

**Never settled.** `COMPANIONS.md` 8, `POSTGAME.md` 9 and `CURIOS.md` C6 all
say so, and the wiki keeps it so. His article (and Hithermost's, and the
Stair's) says that **there are competing theories in the world**, and gives
the evidence for both sides fairly and with a straight face. Hosea does not
decide. He asked Sir Dunstable directly and was told "Just in case."

Evidence that he is alive, all from the game:

* he takes the tea. Brother Quillon pours it at ten past four, and Sir
  Dunstable is delighted by it every time ("The fellow's a mind-reader");
* he borrowed the village's lamp ("Back directly. - D."), and after the
  ending he **lends it to Bram**, in person, with lovely manners. Bram
  carried it down the Stair, and it was a perfectly solid lamp;
* he is a shareholder in the Kingdom of Fairholme, with a chair and a place
  card. The council minutes list him under *apologies* ("in a mountain"),
  not under deceased, and the council minutes everything;
* he says nothing happened, with some warmth, and he is "very slightly more
  singed" each time, and the singeing is cumulative, which is a living thing's
  habit;
* the party also came back in through the porch, and nobody suggests that
  Bram is dead.

Evidence that he is not, all from the game:

* the Book is his name all the way down the page, *Just in case*, two
  hundred and twelve times;
* he comes in **through the porch**, the way people come back who went
  through the Door and did not come out of it;
* the chalk marks down the Stair, each one D. and a number and a little
  deeper than the last, stop at **D. 212**, and nobody has been past it;
* Brother Quillon's vows forbid him exactly one thing, saying that he
  remembers, and he says under his breath a number in the low two hundreds;
* something on the Stair is on its way up, in the dark, and the party meets
  it as Somebody Coming Up (P4d, Enemy 63), and nobody can see who;
* a quarter past four, every day, to the minute.

The wiki may add evidence of its own on either side, from witnesses who have
theories (the Hithermost villagers, the Fairholme council, the Guild, Quillon's
silence, the Wyvern's regulars taking bets), as long as **no piece of it
settles the question** and every piece has an answer from the other side.
Good ground: his laundry, his post, whether his tea goes cold, whether he
casts a shadow by lamplight and whose lamp it is. The Fairholme minutes
deferring the matter is a joke the game has made already and can stand
another outing. Hosea marks the whole section `disputed`, and ends it with
his own view, which is that the knight is a man of excellent manners and the
question is none of his business, and then with the betting at the Wyvern.
