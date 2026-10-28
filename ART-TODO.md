# Art to do

Pictures the game needs that no stock sheet has. Mike draws them and I put them in.
**Keep this file current**: add a row when a map edit or a line of text asks for
a picture that does not exist, and move it to *Done* when the picture is in.

Last updated 27 October 2026.

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
| 6 | **The bench on the Barrow** | the world map (Map 8), on top of the Barrow of the Forty-Fourth at (77, 55); event 12 | 48x48 at world-map scale, more cells if it needs them | a plain bench facing the sea. It appears only once the flat-packed bench has been built there (switch `SW_BENCH_DONE`), so before that the cell stays as it is | nothing: no World tile is a bench |
| 8 | **The bench on the Middle Distance** | the world map (Map 8), the Hermit's little hill island south of the Barrow, reached by airship; event 23 at (82, 65) | 48x48 at world-map scale, like item 6 | a plain bench facing the sea, **older** than the Barrow's, with no plaque. It is always there | nothing: no World tile is a bench |
| 7 | **A heap of odd socks** | The Bottomless Pit (Map 19), on the floor at (10, 9); event 6 | 48x48, or more cells for a bigger drift | "a drift of odd socks four feet deep", two hundred years of them, none matching | bare floor |

Item 7 wasn't on your list on 23 October. It was on round 7's, so I've kept it.
Items 6 and 8 are the two overworld benches. Everything the game says about them,
and where it is wrong about the map, is in *The two benches* below.

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
| The Barrow is "**the mound in the east**", seen from the Middle Distance | the Middle Distance | **no**: the Barrow is north of it, a little west. This is a text error, not a map one |
| The Barrow bench is "**a long way south**" of the Middle Distance | the Middle Distance, after sitting | **no**: it is north, about 11 cells away. Also a text error |
| "a mound in the **eastern hills**" | the ending | the Barrow is at x 68 of 120, a little east of centre, in hills. It's true enough |
| "a mound out **east**" | Ysolde, in the Slain Wyvern | it's true from the Slain Wyvern |

I haven't changed the two text errors: those lines are finished content. Tell me
which way round you want them once the map is settled, and I'll fix just those
words.

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
> There is a bench on it. / It is older than the one on the mound in the / east. It has no plaque. Nobody remembers who / put it up.

*sitting on it* (choice: Sit on it / Stand about):
> You sit on it. / Nothing happens. / The sea does what the sea does.

*and, only if the Barrow bench was built:*
> There is another one of these a long way / south, facing the same water.

**What this means for the drawing:**
- It's a bench on a grassy hill, looking out to sea.
- It has no plaque, and it is clearly old and weathered, older than the Barrow's.
- It's of the same kind as the Barrow's ("another one of these").
- The Hermit sees it from seven cells west, so it faces away from him, towards the sea. If it is
  to face "the same water" as the Barrow's, that is north, up the channel towards the mound.

Note that the Middle Distance's "older than the one on the mound" is said even
before the Barrow bench exists. It's a small slip in the text too; I can make it
conditional when I fix the directions.

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
