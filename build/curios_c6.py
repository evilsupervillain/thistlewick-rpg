"""CURIOS.md wave C6: Much Pottering and the Gotobeds' cottage (Maps 68-69).

The Bottom Lock (70) is a culvert, Ambrose Fitch's cottage (71) is a
house nobody lives in any more, and the Stair (73-78) is the post-game's
long walk down with Sir Dunstable's markers on it; all three are left
alone on purpose (CURIOS.md 6, C6)."""

import db
from curios import curio as C

# --------------------------------------------------- Map 68, Much Pottering --
POTTERING = [
    C("Window", (4, 11), "Window A", [
        "Through the window: a front room in which nothing is happening, "
        "very contentedly, and has been all morning."]),
    C("Window", (8, 11), "Window A", [
        "Through the window: a cat asleep on the sill, and a card propped "
        "beside it: CAT, ASLEEP. NO ADVENTURES, PLEASE."]),
    C("Window", (16, 11), "Window A", [
        "Through the window: a table laid for a quiet afternoon. It has "
        "been laid since about eleven. The quiet afternoon is coming "
        "along nicely."]),
    C("Window", (36, 11), "Window A", [
        "Through the window: a very comfortable armchair, and in it, the "
        "pig's owner, also asleep."]),
    C("Scarecrow", (29, 20), "Scarecrow", [
        "A scarecrow on Mr Dibble's allotment, with a card on a string "
        "round its neck: PLEASE DO NOT DISTURB.",
        "The crows have read it, and are respecting it."]),
    C("Haystack", (36, 20), "Hay", [
        "A haystack. You search it for a needle, out of habit.",
        "There is no needle. There is a card: NO NEEDLE. THIS IS MUCH "
        "POTTERING."],
      trope="needle_haystack"),
]

# ------------------------------------------------- Map 69, the Gotobeds' --
GOTOBEDS = [
    C("Window", (6, 3), "Large Window A", [
        "Through the window: the garden gate, worn smooth along the top "
        "bar where somebody small leans to watch for the post."]),
    C("Clock", (7, 3), "Clock", [
        "A clock, and a card under it in Mr Gotobed's hand: NOTHING "
        "HAPPENS AT ANY OF THESE TIMES."]),
    C("Best Plates", (8, 4), "Dish Cabinet", [
        "The best plates, and among them, kept with the best ones, a "
        "plate with a crayon volcano on it."]),
    C("Teapot", (6, 7), "Teapot A", [
        "A teapot, and beside it two cosies: one for an ordinary afternoon, and"
        " one to go on top of the first, for a really quiet one."]),
    C("Potted Plant", (9, 10), "Potted Plant A", [
        "A potted plant with a little flag stuck in the soil: VOLCANO "
        "(DORMANT). Effie's work."]),
    C("Effie's Books", (27, 8), "Simple Shelf B (Books)", [
        "Effie's books: an atlas with Upper Clanging circled in red, and "
        "LETTERS, AND HOW TO WRITE THEM, with every page turned down at "
        "the corner."]),
    C("Effie's Bed", (26, 10), "Cheap Bed B", [
        "A small bed, made, with a picture pinned up over it of a very "
        "tall chimney, drawn by somebody who has heard about chimneys "
        "and is excited."]),
    C("Drawers", (29, 9), "Chest of Drawers", [
        "A chest of drawers. Taped to the top drawer, in a child's "
        "writing: STAMPS. DO NOT.",
        "You do not."],
      trope="rummage"),
    C("Jewellery Box", (33, 7), "Case A", [
        "A jewellery box on the dresser. You do not so much as look at "
        "it. It is Mrs Gotobed's, she is downstairs, and you were "
        "brought up properly."]),
    C("Mr Gotobed's Swords", (29, 4), "Swords B", [
        "Two swords crossed on the wall, very well kept. A brass plate "
        "under them: H. GOTOBED - ADVENTURER (RETIRED).",
        "Tucked behind one hilt, a card in Mrs Gotobed's hand: HE CAME "
        "THROUGH ON A QUEST TO RESCUE SOMEBODY ELSE. HE STAYED FOR TEA. "
        "THE OTHER ONE WAS FINE."],
      again=["The swords are oiled every Sunday and put back exactly "
             "crossed. Nothing in Much Pottering has needed slaying since. "
             "He puts this down to the swords."],
      trope="retired_hero", hung=1),
    C("Map Over the Drawers", (30, 4), "Chest of Drawers", [
        "Over the drawers, a map of the world, with a dotted red line "
        "on it: every road Mr Gotobed ever took. It goes to every edge "
        "of the map, and then comes back, quite straight, to here.",
        "Much Pottering is circled twice, and beside it, in the same red "
        "ink: FOUND IT."],
      trope="world_map"),
]

ALL = {68: POTTERING, 69: GOTOBEDS}
