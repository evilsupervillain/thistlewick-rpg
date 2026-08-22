# The Obligatory Quest

A short comic fantasy RPG, built for RPG Maker MZ 1.10.0.

Every hundred years the Dark Lord rises in the Obligatory Tower, and the village
of Thistlewick sends a Chosen One north to deal with him. It has worked
forty-seven times. You are Bram, a turnip farmer, and you are number forty-eight
— selected by the Prophecy Committee while you were asleep and therefore unable
to object.

You wake up at home, wander Thistlewick, talk to everyone, and persuade up to
three of six villagers to come with you: a field medic who cannot hit anything,
a blacksmith who can hit one thing extremely hard, a hedge mage with no hit
points, a shopkeeper with sticky fingers, a knight who is mostly armour, and a
bard who is writing all of this down. Who you take changes how the fights work.
Then you walk out of the gate, cross the world, get lost in a wood, climb a
tower, and discover that the Prophecy is a contract - and that the Dark Lord has
been trying to get out of it for four thousand years.

Roughly an hour to finish. There is a counter for how many clichés you walk
into, and the ending reads it back to you.

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
