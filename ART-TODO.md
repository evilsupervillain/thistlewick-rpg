# Art to do

Pictures the game needs that no stock sheet has. Mike draws them and I put them in.
**Keep this file current**: add a row when a map edit or a line of text asks for
a picture that does not exist, and move it to *Done* when the picture is in.

Last updated 29 October 2026.

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

Nothing. Everything asked for so far is in; see *Done*.

The notes on the two benches below are kept for when either drawing is
changed.

## The two benches: everything the game says

Collected on 24 October so the map and the drawings can match the text. Each
line is quoted exactly as the player reads it; `/` is a line break.

**Where things are on the world map (Map 8)**, after your round of 27 October:
the Barrow's door is at (76, 54), and its top, where the bench goes, is at
(77, 55). The Hermit's hut is at (75, 64). The Middle Distance is the little
island at (82-84, 65-67), hills at (83, 65) and (84, 66), with its bench event
at (82, 65), its top-left corner. The Obligatory Tower is at (66, 43). So the
Middle Distance is **6 cells east and 10 south of the Barrow**, and the Tower is
11 north and 10 west of it. The Barrow now stands on the north shore of the
channel that runs down to the Middle Distance.

### What the text needs from the map

| claim | said by | true on the map now? |
| --- | --- | --- |
| From the top of the Barrow you can see the **sea** | the Barrow top (before, during and after building); Ambrose; Ysolde | **yes**, since 27 Oct: the channel is right below it, and it opens into the sea |
| From the top of the Barrow you can see the **north road** and **the tower at the end of it** | the Barrow top; Ambrose | the road passes just west and north of the mound. The Tower is 11 north and 10 west |
| The north road has "nowhere for them to sit down for **four miles**" | Ambrose | there's nothing to check, as long as the road passes near the mound |
| The Barrow bench **faces the sea** | Ambrose; the build text; the empty chamber; Ysolde | yes: it faces south, down the channel |
| The Middle Distance bench faces "**the same water**" as the Barrow's | the Middle Distance, after sitting, if the Barrow bench is built | **yes**: both look on to the same channel |
| The Barrow is "**the mound to the north**", seen from the Middle Distance | the Middle Distance, once the Barrow bench is built | **yes**: fixed 28 Oct (it said "in the east") |
| The Barrow bench is "**to the north**" of the Middle Distance | the Middle Distance, after sitting | **yes**: fixed 28 Oct (it said "a long way south") |
| "a mound in the **eastern hills**" | the ending | the Barrow is at x 68 of 120, a little east of centre, in hills. It's true enough |
| "a mound out **east**" | Ysolde, in the Slain Wyvern | **loosely**: from the village at (60, 79) the Barrow is 16 east and 25 north, so it is north-east. Not a bench line, so unchanged |

The two text errors were fixed on 28 October, at your request, by changing only
the direction words, and the comparison now waits for the Barrow bench.

### The Barrow bench (item 6): the text

*Ambrose Fitch, after the fight* (`wilds.py`, the Barrow, Map 20):
> I didn't ask for any of it. / I asked for a bench.

> A bench.

*(narration)* You wait. That is the whole request.
> Top of the mound. Facing the sea. / You can see the north road from up there. / People walk that road tired and there's / nowhere for them to sit down for four miles.

> Forty years of standing in a circle / and that's what I want. A bench. / Anyone's bench. Not mine. Anyone's.

*Ambrose, until it is built:*
> Still no bench. / I'm not going anywhere. That's rather / the difficulty.

*The empty chamber, after it is built:*
> The burial chamber is empty. / The circle somebody drew on the floor has / gone unswept for the first time in forty / years, and there is nobody standing in it.
>
> If you want him, he is on the top of the / mound, on a bench, facing the sea.

*The top of the Barrow* (world map event 12), before you meet him:
> The top of the mound. Long grass, and a view. / You can see the sea from here, and the north / road, and the tower at the end of it. / There is nowhere at all to sit.

*after he asks:*
> The top of the mound. The sea one way, the / tower the other. / This is the spot. He was quite clear about / the spot.

*with the bench in your bag:*
> The top of the mound, and a bench in eleven / pieces under your arm.

*building it* (choice: Put the bench together / Not yet):
> The diagram is wrong. You work it out. / It takes an hour and a half and one piece / is left over, which is traditional.
>
> A bench, on the top of the Barrow of the / Forty-Fourth, facing the sea. / Anyone may sit on it. That was the point; / he was very clear that that was the point.

*once it is there:*
> The bench on the top of the mound. / Somebody has already been sitting on it: the / grass is flat in front of it, and there is a / cup, and the cup is not yours.

*Ysolde, in the Slain Wyvern, after it is built:*
> You've been out to the mound.

*(narration)* You tell her what he asked for. / You tell her that it is there now, on the / top, facing the sea.
> They wanted a hero in a mound. / He wanted somewhere to put his legs up.

*The ending, if it was built* (`journey.py`):
> And on the top of a mound in the eastern / hills there is a bench, facing the sea, / which anybody may sit on, and which is what / Ambrose Fitch asked for and did not get.

*The flat pack itself*: the Wick & Barrow shop and the item description.
> A bench, in eleven pieces, leaning against / the wall under a hand-lettered card: / 'BENCH. 400. NOBODY HAS EVER BOUGHT THIS.' / The card is not wrong and knows it.

> One bench, in eleven pieces, with a mallet and a diagram that is wrong. Somebody wanted somewhere to sit.

**What this means for the drawing:**
- It's a plain, new, flat-pack bench, put together by an amateur from a wrong diagram.
- It's on long grass, facing the sea (south, down the channel), with the grass flattened in front of it.
- A cup that isn't yours appears once it's built, so the cup can be part of the picture.
- No plaque is mentioned on it. The Middle Distance text implies it has one, by saying that bench has none.
- Ambrose is said to sit on it, but nothing in the game draws him there.

### The Middle Distance bench (item 8): the text

*The Hermit*, at his hut (75, 64), the first time:
> A hut, a rock, and a man looking at the / middle distance with great authority.

*after his shopping:*
> The middle distance is very fine today. / Also I am nearly out of candles again, / but I shan't mention it.

*The Middle Distance* (world map event 23, reached by airship):
> The middle distance. / It is a hill. Grass, a view of the sea, and / nothing else of any description whatever.
>
*before the Barrow bench is built:*
> There is a bench on it. / It is very old. It has no plaque. Nobody / remembers who put it up.

*after it is built:*
> There is a bench on it. / It is older than the one on the mound to the / north. It has no plaque. Nobody remembers who / put it up.

*sitting on it* (choice: Sit on it / Stand about):
> You sit on it. / Nothing happens. / The sea does what the sea does.

*and, only if the Barrow bench was built:*
> There is another one of these to the / north, facing the same water.

**What this means for the drawing:**
- It's a bench on a grassy hill, looking out to sea.
- It has no plaque, and it is clearly old and weathered, older than the Barrow's.
- It's of the same kind as the Barrow's ("another one of these").
- The Hermit sees it from seven cells west, so it faces away from him, towards the sea. If it is
  to face "the same water" as the Barrow's, that is north, up the channel towards the mound.

Until 28 October the Middle Distance said "older than the one on the mound"
before the Barrow bench existed. That comparison now waits for `SW_BENCH_DONE`.

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
| the pencil height marks (item 4) | Corvin's study (Map 53), event 16 at (44, 3) | Mike: `height_marks.png`, `!$HeightMarks`, on the wall face's lower row, on the two pages that need `SW_COR1_HOME`; nothing before he has been home | 29 Oct |
| the Thistle family portrait (item 1) | Bram's House (Map 2), (8, 2) | Mike: `thistle_portrait_small.png`, a 40x40 frame in its cell (his smaller second go; the first, full-cell, is `thistle_portrait.png`), made into `!$ThistlePortrait` lifted 48 pixels, so event 6 at (8, 3) shows it on the wall above. The stock `Portrait B` tile it replaces is gone from the frozen map | 29 Oct |
| the "wyvern" (item 2) | the Slain Wyvern (Map 14), on the mantel shelf; event 14 at (14, 3) | Mike: `goose_trophy.png`, 48x48, made into `!$GooseTrophy` lifted 69 pixels, which sets it just into the shelf (72 sat it on top; Mike asked for it 3 pixels lower). On all five of the goose's pages | 29 Oct |
| the two brass plaques (item 3) | the Slain Wyvern (Map 14), events 18 at (13, 3) and 21 at (15, 3) | Mike: `plaque_left_shadow.png` and `plaque_right_shadow.png` (his third go, with a shadow so they stand off the stone; the earlier are `plaque_left.png`/`plaque_right.png` and the `_small` pair), `!$PlaqueLeft` and `!$PlaqueRight`, each on the fire's side of its cell. The right one shows only once WRE-2 has put it up | 29 Oct |
| the painted board (item 5) | the Bottomless Pit (Map 19), event 2 at (15, 19) | Mike: `bottomless_board.png`, `!$BottomlessBoard`, replacing `Notes B (V)` | 29 Oct |
| the bench on the Barrow (item 6) | the world map (Map 8), event 12 at (77, 55) | Mike: `barrow_bench.png`, `!$BarrowBench`, on the page for `SW_BENCH_DONE` only. A faint frame round the cell's edge is dropped by `supplied.py` (`clean`) | 29 Oct |
| the heap of odd socks (item 7) | the Bottomless Pit (Map 19), event 6 at (10, 9) | Mike sent two: `socks_outlined.png` (in use, `!$SocksOutlined`) and `socks_plain.png` (`!$SocksPlain`). `wilds.SOCKS_SHEET` picks one. The heap now blocks its cell | 29 Oct |
| the bench on the Middle Distance (item 8) | the world map (Map 8), event 23 at (82, 65) | Mike: `middle_distance_bench.png`, `!$MiddleBench`, facing north up the channel; always there. Cleaned like the Barrow's | 29 Oct |
| the bell rope by the church door | Ashcombe (Map 52), (6, 12) | Mike: Outside_B `Rope` down from a bell box, with a real door beside it (locked: "SERVICE AT SIX. KEY WITH THE BELL.") | 23 Oct |
| the hound's alcove | the Barrow (Map 20), (21, 12) | Mike: `Entrance A` over `Entrance D` set back into the wall, with Inside_C `Beef Stew` as the dish | 23 Oct |
| the splintered chest | the Gloamwood (Map 9), the mimic at (12, 12) | Dungeon_B `Scrap Wood`, cut out to `img/characters/!$Splinters.png` by `journey.draw_art()` | 23 Oct |
| the Two Hundred's shadow over the Works floor | the Hoyle Works (Map 22), event 13 at (12, 16) | Mike: `airship-shadow-big.png`, 816x624, kept as `build/supplied/airship_shadow.png` and made into `img/characters/!$AirshipShadow.png` by `build/supplied.py`. Below characters and through; gone once `SW_AIRSHIP` is on | 28 Oct |
| the crack in the pit wall | the Bottomless Pit (Map 19), (19, 2) | Mike: Dungeon_B `Fissures D` | 23 Oct |
