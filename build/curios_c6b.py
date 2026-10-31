"""CURIOS.md wave C6b: quiet curios for the places the jokes were kept out
of - the Long Field, the Wreck, Old Ashcombe, Under Carn Drey, Fitch's
cottage and the Stair (Mike, 31 Oct: "can you add anything to it that would
match the tone?").

No jokes here, or only the place's own: these are observations in the voice
the map already uses - the plaques, the log, the chalk. Two or three to a
map, so the quiet stays quiet. Nothing here settles whether Sir Dunstable
is alive, or says what happened to the crew of the Hundred and
Ninety-Ninth, or anything of Ambrose's that his own events do not."""

from curios import curio as C

# ------------------------------------------------------ Map 26, the Long Field --
LONG_FIELD = [
    C("A Piece of Brass", (24, 14), "Waste", [
        "A twist of brass in the grass, too small to have a plate of its "
        "own.",
        "Somebody has tied a paper tag to it with string anyway: ONE OF "
        "THEM. KEPT."]),
    C("A Propeller Blade", (13, 9), "Waste", [
        "A propeller blade, half sunk in the turf. The side that faces "
        "the sky has been polished. The side in the ground has been left "
        "to the field."]),
    C("Envelope Cloth", (28, 19), "Waste", [
        "A strip of envelope cloth caught on a bush, faded to the colour "
        "of the grass. It lifts in the wind, the way it was made to."]),
    C("A Rivet", (8, 13), "Waste", [
        "A single rivet in the grass, with a ring of small white stones "
        "laid round it so that nobody treads on it."]),
]

# ------------------------------------------- Map 27, the Hundred and Ninety-Ninth --
WRECK = [
    C("Valve", (16, 4), "Valve", [
        "A valve on the bulkhead, tagged DO NOT TOUCH. The handle is worn "
        "bright where a hand used to rest on it, and has dulled a little "
        "since."]),
    C("An Almanac", (15, 7), "Book A", [
        "A pocket almanac, open at the week of the flight. One day is "
        "ringed in pencil, and beside it, very small: SHE'LL GO."]),
    C("Stores", [(3, 9), (4, 9)], "Steel Shelf", [
        "The stores rack, packed once for a flight of fourteen miles as if for "
        "a fortnight. It is bare now, and wiped down, and nothing else has been"
        " put on it."]),
    C("Gauge", (17, 9), "Machine C", [
        "A gauge, its needle resting exactly where it ought to. It has "
        "been resting there, quite correctly, for eleven years."]),
    C("A Berth", (8, 18), "Pipe Frame Bed", [
        "A berth with the blanket folded at the foot. Under the pillow, a "
        "letter, sealed, addressed in the steadier of the two hands from "
        "the log:",
        "TO BE POSTED ON ARRIVAL."]),
    C("Sweet Tin", (3, 21), "Side Desk B (Metal)", [
        "A tin of boiled sweets on a small desk. One is gone. The lid has "
        "been put back on carefully, so the rest would keep."]),
    C("A Web", (23, 22), "Spider Web", [
        "A spider has spun a web across a corner of the hold. It is the "
        "only thing aboard that has started anything new in eleven years, "
        "and it is a very good web."]),
]

# ---------------------------------------------------- Map 66, Old Ashcombe --
OLD_ASHCOMBE = [
    C("Gatepost", (7, 5), "Broken Stone Pillar B (Moss)", [
        "A stone gatepost, mossed over. There is still a hinge on it, and "
        "the hinge still turns."]),
    C("Garden Wall", (12, 3), "Broken Stone Pillar B (Moss)", [
        "Part of a garden wall. A rose has got through the gap where the "
        "gate was, and is flowering on the lake side."]),
    C("Lily Pads", (4, 11), "Lotus Pads A", [
        "Lily pads over what was the green. A coot has built a nest on "
        "the old maypole stump and is sitting on it, very seriously."]),
    C("A Beam", (8, 10), "Fallen Log", [
        "A beam, washed out of the lake and bleached white. There is "
        "still a coat hook in it."]),
    C("Stump", (13, 10), "Stump (Moss)", [
        "A stump, with a ring of shells pressed into the mud round it by "
        "somebody who comes down here sometimes, and sits."]),
]

# --------------------------------------------------- Map 67, Under Carn Drey --
CARN_DREY = [
    C("Cracked Wall", (14, 11), "Crumbling Wall", [
        "A wall, cracked across, and at about shoulder height a smooth "
        "place where somebody once leaned to get their breath before "
        "going on down."]),
    C("Tall Rock", (14, 5), "Tall Rock A (Dirt Cave)", [
        "A tall rock. Something very long has slid past it so often, "
        "going down and coming back, that one side of it is polished "
        "like a banister."]),
]

# -------------------------------------------------- Map 71, Fitch's cottage --
FITCH = [
    C("The Window", (6, 3), "Large Window A", [
        "From the window you can see the sea, and the end of the north "
        "road where it comes over the hill.",
        "The glass is clean. Mrs Pimm does the windows on Tuesdays, "
        "inside and out."]),
    C("A Stool", (8, 8), "Stool A", [
        "A stool pulled up to the table, for a visitor. There was only "
        "ever the one, and it was always pulled up, in case."]),
]

# --------------------------------------------------- Maps 73-77, the Stair --
# Sir Dunstable's chalk, in his cheerful hand, with no numbers on it: the
# D. markers are the count, and these are only the things he sat on.
STAIR_TOP = [
    C("Boulder", (21, 3), "Boulder B (Rock Cave)", [
        "A boulder near the top of the stair. Chalked on it, in the "
        "cheerful hand: 'Good boulder. Sat on it.'"]),
    C("Boulder", (32, 23), "Boulder B (Rock Cave)", [
        "A boulder with a smooth dip on top. Chalked beside the dip: "
        "'Second-best boulder.'"]),
]
STAIR_FURTHER = [
    C("Boulder", (26, 6), "Boulder B (Rock Cave)", [
        "A boulder, and chalked beside it an arrow, pointing down, and "
        "under the arrow: 'That way, I expect.'"]),
]
STAIR_HALF = [
    C("Boulder", (18, 6), "Boulder B (Rock Cave)", [
        "A boulder with TEA chalked on it, and an arrow, and under the "
        "arrow, smaller: 'If there is any.'"]),
]
STAIR_STILL = [
    C("Boulder", (36, 16), "Boulder B (Rock Cave)", [
        "A boulder. Chalked on it, in the cheerful hand, rather bigger "
        "than usual: 'STILL GOING.'"]),
]
STAIR_212 = [
    C("Boulder", (22, 20), "Boulder B (Rock Cave)", [
        "Chalked on a boulder, in the cheerful hand: a little drawing of "
        "the sun, with rays. Under it: 'For later.'"]),
]

ALL = {26: LONG_FIELD, 27: WRECK, 66: OLD_ASHCOMBE, 67: CARN_DREY,
       71: FITCH, 73: STAIR_TOP, 74: STAIR_FURTHER, 75: STAIR_HALF,
       76: STAIR_STILL, 77: STAIR_212}
