# The Obligatory Quest

A short comic fantasy RPG, built for RPG Maker MZ 1.10.0.

Every hundred years the Dark Lord rises in the Obligatory Tower, and the village
of Thistlewick sends a Chosen One north to deal with him. It has worked
forty-seven times. You are Bram, a turnip farmer, and you are number forty-eight
— selected by the Prophecy Committee while you were asleep and therefore unable
to object.

You wake up at home, wander Thistlewick, talk to everyone, and persuade up to
three villagers to come with you: a field medic who cannot hit anything, a
blacksmith who can hit one thing extremely hard, a hedge mage with no hit
points, a shopkeeper with sticky fingers, a knight who is mostly armour, and a
bard who is writing all of this down. Who you take changes how the fights work.
Then you walk out of the gate, cross the world, get lost in a wood, climb a
tower, and discover that the Prophecy is a contract - and that the Dark Lord has
been trying to get out of it for four thousand years.

## The south

None of the above is the whole map. Turn left out of the gate instead of right
and there is a coast road, and at the end of it a wet fishing town called
**Nether Sopping**, which is where the forty-seven Chosen Ones who *came back*
were quietly resettled by a village that found them awkward to have about.

They are all in a tavern called the Slain Wyvern, and they will all tell you
what happened to them, and every one of those stories is a genre cliché that
happened to somebody who is still annoyed about it: the escort mission, the
fetch-quest chain, the unwinnable scripted fight, the party that quit, the
kindly old advisor everyone accused of being the villain, and the amnesiac in a
tiara who is going to work it out any day now.

Three of the people in there will come with you. One of them is contractually
unavailable for the final dungeon and tells you so twice.

Out in the world there is also a lighthouse kept for a sea nobody sails, a
tourist attraction four feet deep with something living in it, a barrow with a
hero in it who only ever wanted somewhere to sit down, a hermit whose cryptic
wisdom is a shopping list, and a delivery job between two sisters who have not
spoken in thirty years and communicate entirely by parcel.

Roughly an hour for the quest, two or three if you go south. There is a counter
for how many clichés you walk into, and the ending reads it back to you along
with what you did about the bench.

## Playing it

RPG Maker MZ loads its data over XHR, so the game has to be served rather than
opened from disk:

    ../tools/play.sh .

Or serve it and point a browser at <http://127.0.0.1:8766/>:

    node ../tools/serve.js . 8766

Arrow keys to move, Z or Enter to confirm, X or Escape for the menu, Shift to
dash.

## Building it

`data/*.json` is generated. The source is `build/`, and it is re-runnable:

    python3 build/build_game.py
    python3 ../tools/validate.py .

`CLAUDE.md` documents the structure, the id ranges and how to verify changes.
`EXPANSION.md` is the design document for the southern half - the lore it hangs
on, the places, the people and the seven side-quests.
