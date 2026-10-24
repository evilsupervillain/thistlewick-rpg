# Art to do

Pictures the game needs that no stock sheet has. Mike draws them and I put them in.
**Keep this file current**: add a row when a map edit or a line of text asks for
a picture that does not exist, and move it to *Done* when the picture is in.

Last updated 23 October 2026.

## How to hand them over

* Put each PNG in `build/supplied/` and name it after its row, e.g.
  `goose_trophy.png`. They are kept there as delivered, like the portraits.
* Make them 48 pixels a cell on a transparent background. Draw at the cell
  sizes given below; if you need a different size, say so and I'll fit
  the event to it.
* Each picture becomes an event's sprite (a `!$` object sheet), so it is drawn
  standing on its cell: anything taller than 48 pixels goes **upwards** from
  the cell.
* No animation is needed. Send one frame and I'll fill the sheet.
* If a picture needs a second state (before and after), send two files.

## Wanted

| # | what | where | size | must show (the text the player reads) | now |
| --- | --- | --- | --- | --- | --- |
| 1 | **The Thistle family portrait** | Bram's House (Map 2), on the wall at (8, 2); event 6 at (8, 3) | 48x48, or 48x96 for a tall frame | **six generations** of Thistles in one frame, all holding turnips, "not one of them is holding a sword" | a stock one-person portrait |
| 2 | **The "wyvern"** | The Slain Wyvern (Map 14), over the fireplace at (13-15, 2-3); event 14 at (14, 3) | 48x48, up to 144x96 across the chimney breast | a goose mounted as a trophy, "wings out, jaws open", with sixty years of everybody agreeing it is a wyvern | nothing: only the fireplace shows |
| 3 | **Two small brass plaques** | either side of the goose, on the fireplace's lower row; events 18 at (13, 3) and 21 at (15, 3) | 48x48 each, the plate small inside the cell | plain small brass plates. The second only appears once Wren's quest (WRE-2) has it engraved | nothing |
| 4 | **Pencil height marks** | Ashcombe indoors, Corvin's study (Map 53), "the new wall by the window"; event 16 at (44, 3) | 48x48, or 48x96 up the wall | pencil lines up the wall with ages beside them: *C., 6. C., 9. C., 12. C., 16. C., 19.*, each a little too tall for a boy that age. They appear only after Corvin has been home | a plain wall |
| 5 | **The painted board** | The Bottomless Pit (Map 19), lying flat on the floor at (15, 19); event 2 | 48x48 | a painted board lying face up: **BOTTOMLESS (APPROX.)**, with *YOU ARE STANDING ON IT* added by another hand | a plain pale note (`Notes B (V)`) |
| 6 | **The bench on the Barrow** | the world map (Map 8), on top of the Barrow of the Forty-Fourth at (69, 57); event 12 | 48x48 at world-map scale, more cells if it needs them | a plain bench facing the sea. It appears only once the flat-packed bench has been built there (switch `SW_BENCH_DONE`), so before that the cell stays as it is | nothing: no World tile is a bench |
| 8 | **The bench on the Middle Distance** | the world map (Map 8), the Hermit's little hill island east of the Barrow, reached by airship; event 23 at (82, 67) | 48x48 at world-map scale, like item 6 | a plain bench facing the sea, **older** than the Barrow's, with no plaque. It is always there | nothing: no World tile is a bench |
| 7 | **A heap of odd socks** | The Bottomless Pit (Map 19), on the floor at (10, 9); event 6 | 48x48, or more cells for a bigger drift | "a drift of odd socks four feet deep", two hundred years of them, none matching | bare floor |

Item 7 wasn't on your list on 23 October. It was on round 7's, so I've kept it.
Items 6 and 8 are the two overworld benches; they face the same sea, and the
Middle Distance's text says the Barrow's is the newer of the two.

## Would be better, if you feel like it

The game uses stand-ins for these, and the stand-ins are acceptable.

| what | where | the text says | stand-in |
| --- | --- | --- | --- |
| the flat-packed bench | Wick & Barrow, Outfitters (Map 16), against the wall at (7, 4) | a bench in a flat pack, for sale | `Simple Shelf E` |
| a collar in the hound's alcove | the Barrow (Map 20), with the dish in your alcove at (21, 12) | "a dish in it, and a collar, and a name: BUDGE" | the dish only (`Beef Stew`) |
| a bird's nest in a tree fork | the Gloamwood (Map 9) | a nest | `Wall Fern` |
| an arrow carved in a trunk | the Gloamwood (Map 9) | a carved arrow | `Wall Vines` |
| a shed snakeskin | the deep wood (Map 10) | a shed skin | `Wall Vines` |

## Done

| what | where | how | when |
| --- | --- | --- | --- |
| the bell rope by the church door | Ashcombe (Map 52), (6, 12) | Mike: Outside_B `Rope` down from a bell box, with a real door beside it (locked: "SERVICE AT SIX. KEY WITH THE BELL.") | 23 Oct |
| the hound's alcove | the Barrow (Map 20), (21, 12) | Mike: `Entrance A` over `Entrance D` set back into the wall, with Inside_C `Beef Stew` as the dish | 23 Oct |
| the splintered chest | the Gloamwood (Map 9), the mimic at (12, 12) | Dungeon_B `Scrap Wood`, cut out to `img/characters/!$Splinters.png` by `journey.draw_art()` | 23 Oct |
| the crack in the pit wall | the Bottomless Pit (Map 19), (19, 2) | Mike: Dungeon_B `Fissures D` | 23 Oct |
