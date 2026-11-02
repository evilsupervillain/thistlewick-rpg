# The Thistle-pedia: how to maintain it

`thistlepedia/` is an in-world encyclopedia of the game, written as Volume
Three of Hosea Bellwether's *A Complete And Accurate History Of The Obligatory
Quest*, some time after the ending. It is a [Static-Pedia](https://github.com/evilsupervillain/staticpedia)
wiki: `thistlepedia/index.html` is the whole program (never edit it), every
`.md` under the folder is a page, and it can be served on its own, apart from
the game. The skill that says how is `.claude/skills/staticpedia/SKILL.md`.

## The voice

* Everything is Hosea's, in the first person where he has an opinion. He is a
  Nether Sopping man: he counts in plain calendar years, he notices what
  Thistlewick does not (see `TIMELINE.md` section 1, the gradient), and he is
  wry about the Committee. He has never been on a quest. Complete is going
  well; accurate is the problem.
* **Never contradict the game.** Dialogue, the design docs and `TIMELINE.md`
  are canon. Where the game leaves a gap Hosea may fill it, but as *his*
  account, and a guess is marked as one (`<div class="marginalia">`). Where
  `TIMELINE.md` section 6 says something is undecided on purpose (what began
  the Third Age, Grimspite's own age), he does not decide it.
* **Where the player chooses, he is vague.** Who climbed the Tower with Bram
  varies; everybody he asked says it was them. Every optional quest is
  resolved - the wiki is written as if all of it happened.
* **He writes on the twenty-first of March, Third Age 2002**, two years after
  the Quest. "Now" means that date and ages are 2002's. What became of
  everybody in between is decided once, in `AFTERWARDS.md` next to this file,
  which keeps the game's canon and the wiki's inventions in separate columns;
  every bio ends with an "Afterwards" section that agrees with it.
* The humour rules are `NORTH.md` 1.2-1.6, and they hold here too: clean,
  embarrassment never resentment, nobody diminished by their punchline.

## The tools

    python3 scripts/thistlepedia/portraits.py     # refresh the portrait copies
    python3 scripts/thistlepedia/redlinks.py      # red <-> blue links, and what is still owed
    node scripts/staticpedia/build-index.mjs thistlepedia
    node scripts/staticpedia/check-links.mjs thistlepedia
    python3 -m http.server 8011                   # then /thistlepedia/

**Portraits.** `portraits.json` names each portrait after its page and says
which speaker in `build/story.py`'s `FACES` it is, so the casting comes from
the game. The script copies `img/pictures/<sheet>_<index+1>.png` (the full
bust), or cuts the face cell out of `img/faces/` where there is no bust, or
uses `scripts/thistlepedia/art/<Name>.png` if a portrait was drawn for the wiki.
When final art lands in `img/` under the same names, rerun it; `--check` says
whether any copy is stale.

**Red links.** Write links to articles as ordinary links whether or not the
article exists yet; `redlinks.py` turns the missing ones red and turns them
back when the article is written, and prints the list of articles still owed.
Run it, then the index generator, then the link checker, after every batch.
