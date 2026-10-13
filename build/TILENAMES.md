# What `mapkit`'s tile constants actually are

**Generated - `python3 ../../tools/tileaudit.py . --write`.** Do not
edit by hand; edit `mapkit.py` and regenerate.

The left column is what this game calls the tile. The right column is
what the people who drew the sheet call it, read out of the `.txt`
table beside the `.png`. **Where those two disagree, the right column
is the fact and the left column is somebody's first impression at
forty-eight pixels** - which is how `INC_BELL` came to be a `Globe`.

A disagreement is not automatically a bug. Several are deliberate and
are load-bearing in maps that have shipped; `../../TILES-AND-ASSETS.md`
lists those, with what to use instead. What this file is for is seeing
the disagreement *before* building a room out of it.

Multi-cell constants list their cells in drawing order, top row first,
with consecutive repeats collapsed - so a 2x2 tree is one name and a
dresser is `Closet / Sundries Shelf A`.


## Outside_A2 ground  (tileset 2)

| constant | tiles | what the sheet calls it |
| --- | --- | --- |
| `GRASS` | A2 k16 | Meadow |
| `PATH` | A2 k17 | Dirt (Meadow) |
| `COBBLE` | A2 k18 | Road (Meadow) |
| `PAVING` | A2 k19 | Cobblestones A |
| `HEDGE` | A2 k20 | Bush |
| `DECKING` | A2 k22 | Fencepost A (Wood) |
| `SAND` | A2 k24 | Dirt |
| `WHEAT` | A2 k28 | Bush (Dead) |
| `SOIL` | A2 k32 | Sand |
| `DARK_GRASS` | A2 k39 | Moss |
| `WATER` | A1 k1 | Pond |

## Outside_A4 cliffs  (tileset 2)

| constant | tiles | what the sheet calls it |
| --- | --- | --- |
| `CLIFF_TOP` | A4 k116 | Ledge A (Meadow) |
| `CLIFF_FACE` | A4 k124 | Ledge A (Meadow) |

## Outside_A3 house walls  (tileset 2)

| constant | tiles | what the sheet calls it |
| --- | --- | --- |
| `WALL_SHINGLE` | A3 k52 | Roof E (Wood) |
| `WALL_THATCH` | A3 k53 | Roof F (Wood, Ruins) |
| `WALL_LOG` | A3 k54 | Roof G (Log) |
| `WALL_BLUE_TILE` | A3 k55 | Roof H (Dark Blue Tile) |
| `WALL_SANDBRICK` | A3 k56 | Outer Wall A (Rock Wall) |
| `WALL_PLASTER` | A3 k57 | Outer Wall B (Plaster) |
| `WALL_BRICK_RED` | A3 k58 | Outer Wall C (Brick) |
| `WALL_ICE` | A3 k59 | Outer Wall D (Plaster) |
| `WALL_PLANK` | A3 k60 | Outer Wall E (Wood) |
| `WALL_PLANK_LIGHT` | A3 k61 | Outer Wall F (Wood) |
| `WALL_TIMBER` | A3 k62 | Outer Wall G (Log) |
| `WALL_BRICK_PURPLE` | A3 k63 | Outer Wall H (Demon Castle) |
| `WALL_BRICK_GREEN` | A3 k64 | Roof I (Green Tile) |
| `WALL_COLUMNS` | A3 k65 | Roof J (Temple) |
| `WALL_CONCRETE` | A3 k66 | Roof K (Stone) |
| `WALL_MOSSY` | A3 k67 | Roof L (Thatched) |
| `WALL_STONE` | A3 k72 | Outer Wall I (Rock Wall) |
| `WALL_STONE_WHITE` | A3 k73 | Outer Wall J (Temple) |
| `WALL_STONE_DARK` | A3 k74 | Outer Wall K (Rock Wall) |
| `WALL_MOSS_STONE` | A3 k75 | Outer Wall L (Moss) |

## Outside_B scenery  (tileset 2)

| constant | tiles | what the sheet calls it |
| --- | --- | --- |
| `TREE` | B 176, B 177, B 184, B 185 | Large Tree |
| `TREE_DARK` | B 178, B 179, B 186, B 187 | Large Tree |
| `STALL` | B 180, B 181, B 188, B 189 | Large Crate / Crate A / Large Crate / Crate D |
| `STALL_FRUIT` | B 182, B 183, B 190, B 191 | Crate B / Crate C / Crate E / Crate F |
| `TENT` | B 29, B 30, B 31, B 37, B 38, B 39, B 45, B 46, B 47 | Tent B / Tent B (Entrance, Snow) / Tent B |
| `PALM` | B 236, B 244 | Palm Tree |
| `BUSH` | B 152 | Grass A |
| `BUSH2` | B 153 | Grass B |
| `BUSH3` | B 154 | Grass C |
| `FLOWERS` | B 160 | Flowers A |
| `FLOWERS2` | B 161 | Flowers B |
| `FLOWERS3` | B 162 | Flowers C |
| `ROCK` | B 159 | Boulder A |
| `ROCK2` | B 167 | Boulder B |
| `LOGS` | B 164 | Fallen Log |
| `TUB` | B 139 | Well |
| `BARREL` | B 141 | Barrel |
| `CRATE` | B 149 | Barricade (H) |
| `POT` | B 144 | Pot |
| `BUCKET` | B 145 | Basin A |
| `SIGNPOST` | B 137 | Sign A |
| `GRAVE_A` | B 142 | Grave A |
| `GRAVE_B` | B 143 | Grave B |
| `FENCE_PANEL` | B 138 | Sign B |
| `STOVEPIPE` | B 136 | Chimney |
| `LILYPAD` | B 255 | Lotus Pads C |
| `MUSHROOMS` | B 235 | Mushrooms B |
| `BURROW` | B 169 | Hole |
| `BRAMBLES` | B 49 | Wall Vines A |
| `DEAD_BUSH` | B 251 | Susuki Grass |
| `DEAD_TREE` | B 232 | Dead Tree |
| `DEAD_ROOTS` | B 224 | Dead Beanstalk |
| `LADDER` | B 18 | Wood Ladder |
| `REEDS` | A1 k11 | Waterfall D (Boulder) |
| `LAMP` | B 8, B 16 | Streetlight A |
| `SIGN_BLADE` | B 65 | Shop Sign (Sword) |
| `SIGN_ORB` | B 66 | Shop Sign (Sword & Shield) |
| `SIGN_ARMOR` | B 67 | Shop Sign (Armor) |
| `SIGN_RING` | B 68 | Shop Sign (Sack) |
| `SIGN_POTION` | B 69 | Shop Sign (Teapot) |
| `SIGN_INN` | B 70 | Shop Sign (Inn) |
| `SIGN_MUG` | B 71 | Shop Sign (Pub) |
| `SIGN_PLATE` | B 72 | Shop Sign (Eatery) |
| `SIGN_WAND` | B 74 | Shop Sign (Staves) |
| `SIGN_COIN` | B 75 | Shop Sign (Coin) |
| `SIGN_HAMMER` | B 77 | Shop Sign (Hammer) |
| `SIGN_SUN` | B 78 | Shop Sign (Crest) |
| `DOORWAY_DARK` | B 132 | Entrance A (Extend) |
| `DOOR_SHUT` | B 114, B 122 | Large Window C |
| `DOORWAY_ARCH` | B 116, B 124 | Large Window D |
| `WINDOW` | B 96 | Window A |
| `WINDOW_GLASS` | B 115, B 123 | Stained Glass Window / Stained Glass Window B |
| `DOOR_DOUBLE` | B 114, B 122 | Large Window C |

## Inside tileset (id = 3)  (tileset 3)

| constant | tiles | what the sheet calls it |
| --- | --- | --- |
| `IN_WOOD_FLOOR` | A2 k16 | Ground A (Wood Floor Stripe) |
| `IN_COBBLE` | A2 k17 | Ground B (Stone Floor Tile) |
| `IN_DARK_WOOD` | A2 k24 | Ground E (Wood Floor Border) |
| `IN_RED_CARPET` | A2 k26 | Rug A (Red Flower) |
| `IN_SANDSTONE` | A2 k37 | Raised Stone B (Yellow) |
| `IN_DIAMOND_TILE` | A2 k41 | Ground L (Stone Floor X Tile) |
| `IN_PARQUET` | A2 k32 | Ground H (Wood Floor Lattice) |
| `IN_BRICK_FLOOR` | A2 k25 | Ground F (Stone Floor Brick) |
| `IN_PURPLE_RUG` | A2 k35 | Rug D (Oriental Redpink) |
| `IN_GREEN_RUG` | A2 k27 | Rug B (Oriental Green) |
| `IN_BLUE_RUG` | A2 k34 | Rug C (Oriental Blue) |
| `IN_RED_RUG` | A2 k42 | Rug E (Oriental Red) |
| `IN_DOOR_OPENING` | B 17 | Entrance A (Extend) |
| `IN_WALL_TOP` | A4 k98 | Wall J (Wood) |
| `IN_WALL_FACE` | A4 k104 | Wall H (Wood) |
| `IN_WALL_TOP_PLANK` | A4 k97 | Wall I (Log) |
| `IN_WALL_FACE_PLANK` | A4 k105 | Wall I (Log) |
| `IN_WALL_TOP_STONE` | A4 k80 | Wall A (Stone) |
| `IN_WALL_FACE_STONE` | A4 k88 | Wall A (Stone) |
| `IN_WALL_TOP_TAN` | A4 k81 | Wall B (Castle) |
| `IN_WALL_FACE_TAN` | A4 k89 | Wall B (Castle) |
| `IN_WALL_TOP_WHITE` | A4 k101 | Wall K (Stone) |
| `IN_WALL_FACE_WHITE` | A4 k109 | Wall K (Stone) |
| `IN_WALL_TOP_RED` | A4 k85 | Wall F (Brick) |
| `IN_WALL_FACE_RED` | A4 k93 | Wall F (Brick) |
| `IN_WALL_TOP_GOLD` | A4 k86 | Wall G (Stone) |
| `IN_WALL_FACE_GOLD` | A4 k94 | Wall G (Stone) |
| `IN_WALL_TOP_PURPLE` | A4 k116 | Wall N (Tent) |
| `IN_WALL_FACE_PURPLE` | A4 k124 | Wall N (Tent) |
| `IN_VOID` | A5 0 | Darkness |
| `IN_BED` | B 168, B 176 | Bed |
| `IN_BED_ORANGE` | B 169, B 177 | Large Bed |
| `IN_BED_BROWN` | B 171, B 179 | Cheap Bed A |
| `IN_BOOKCASE` | B 158, B 166 | Bookshelf B |
| `IN_BOOKCASE2` | B 159, B 167 | Bookshelf B |
| `IN_CURTAIN_GREEN` | B 66, B 74 | Middle Window B |
| `IN_SHELF_JARS` | B 153, B 161 | Sundries Shelf A |
| `IN_SHELF_BOTTLES` | B 155, B 163 | Sundries Shelf B |
| `IN_SHELF_FRUIT` | B 154, B 162 | Sundries Shelf A |
| `IN_SUNDRIES_CABINET` | B 154, B 162, B 155, B 163 | Sundries Shelf A / Sundries Shelf B |
| `IN_BOTTLE_CABINET` | B 142, B 150, B 143, B 151 | Bottle Shelf A / Bottle Shelf B |
| `WIDE_PIECES` | B 154, B 162, B 155, B 163, B 142, B 150, B 143, B 151 | Sundries Shelf A / Sundries Shelf B / Bottle Shelf A / Bottle Shelf B |
| `IN_SHELF_GOODS` | B 152, B 160 | Bread Shelf |
| `IN_CABINET` | B 144, B 152 | Chest B / Bread Shelf |
| `IN_DRESSER` | B 146, B 154 | Closet / Sundries Shelf A |
| `IN_COUNTER` | B 153 | Sundries Shelf A |
| `IN_PILLAR` | B 24, B 32, B 40 | Stone Pillar A / Broken Stone Pillar A |
| `IN_FIREPLACE` | B 189, B 190, B 191, B 197, B 198, B 199 | Large Fireplace |
| `IN_PIANO` | B 205, B 206, B 207 | Piano |
| `IN_ORGAN` | B 213, B 214, B 215, B 221, B 222, B 223, B 229, B 230, B 231 | Piano / Pipe Organ |
| `IN_TABLE_ROUND` | B 238 | Table A (Ruins) |
| `IN_TABLE_SMALL` | B 239 | Stool (Ruins) |
| `IN_POT` | B 237 | Barrel (Ruins) |
| `IN_CRATE` | B 224 | Crate A |
| `IN_CRATE2` | B 225 | Crate B |
| `IN_BARREL` | B 210 | Pot B |
| `IN_BARREL2` | B 211 | Basin |
| `IN_SACK` | B 208 | Simple Shelf E |
| `IN_SACK2` | B 209 | Pot A |
| `IN_SOFA` | B 96, B 97, B 98, B 99, B 104, B 105, B 106, B 107 | Sofa (Castle) |
| `IN_CURTAIN_RED` | B 49, B 57 | Curtains B |
| `IN_WINDOW` | B 68, B 76 | Large Window A |
| `IN_STAINED_GLASS` | B 71, B 79 | Stained Glass Window |
| `IN_SWORD_RACK` | B 82, B 90 | Swords A / Shield |
| `IN_NOTICE_BOARD` | B 83, B 91 | Swords B / Posted Notice |
| `IN_CLOCK` | B 116, B 124 | Table D / Table F |
| `IN_MIRROR` | B 118, B 126 | Mirror |
| `IN_THRONE` | B 103, B 111 | Throne (Demon Castle) |
| `IN_RAILING` | B 244 | Jail Bar |
| `IN_STOVE` | B 186, B 194 | Fireplace A (Stone) |
| `IN_KITCHEN_COUNTER` | B 202 | Kitchen Counter A |
| `IN_TABLE` | B 112, B 113 | Table A |
| `IN_TABLE_ONE` | B 114 | Table B |
| `IN_STOOL` | B 120 | Stool A |
| `IN_TABLE_PLAIN` | B 115 | Table C |
| `IN_BOOKSHELF` | B 157, B 165 | Bookshelf A |
| `IN_WINE_RACK` | B 141, B 149 | Wine Rack |
| `IN_KITCHEN` | B 192, B 200 | Simple Shelf C (Sacks) / Oven |
| `INC_BOOK` | C 320 | Closed Book A (V) |
| `INC_BOOK2` | C 324 | Open Book A (V) |
| `INC_SCROLL` | C 328 | Note A (V) |
| `INC_SCROLL2` | C 333 | Map B (H) |
| `INC_CANDLES` | C 338 | Scrolls A |
| `INC_PLANT` | C 340 | Planter A |
| `INC_PLANT2` | C 342 | Potted Plant A |
| `INC_CHEST_PROP` | C 344 | Case A |
| `INC_POTION_BLUE` | C 356 | Potion A |
| `INC_POTION_GREEN` | C 357 | Potion B |
| `INC_POTION_RED` | C 358 | Potion C |
| `INC_FRUIT` | C 360 | Basket A |
| `INC_BASKET` | C 362 | Basket C |
| `INC_BOTTLE` | C 280 | Bottle C |
| `INC_BOTTLES` | C 282 | Bottle D |
| `INC_GOBLET` | C 265 | Bottle B |
| `INC_MEAL` | C 296 | Dinner Set A (Bottom) |
| `INC_MEAL2` | C 298 | Dinner Set C (Left) |
| `INC_ARMOR_STAND` | C 372 | Doll B |
| `INC_LAMP` | C 366 | Rugs C |
| `INC_BELL` | C 376 | Globe |
| `INC_DESK_BELL` | C 377 | Bell |
| `INC_SWORD_STAND` | C 400 | Sword Rack A |
| `INC_CASE` | C 344 | Case A |
| `INC_OPEN_BOOK` | C 324 | Open Book A (V) |

## Dungeon tileset (id = 4)  (tileset 4)

| constant | tiles | what the sheet calls it |
| --- | --- | --- |
| `DG_FLOOR` | A2 k16 | Ground A (Dirt Cave) |
| `DG_FLOOR2` | A2 k18 | Dark Ground A (Dirt Cave) |
| `DG_WALL_TOP` | A4 k80 | Wall A (Dirt Cave) |
| `DG_WALL_FACE` | A4 k88 | Wall A (Dirt Cave) |
| `DG_VOID` | A5 0 | Darkness |
| `DGB_GATE` | B 2, B 3, B 10, B 11, B 18, B 19, B 26, B 27 | Stairs A (Up) / Stairs B (Up) / Stairs A (Down) / Stairs B (Down) / Stairs C (Up) / Stairs D (Up) / Stairs C (Down) / Stairs D (Down) |
| `DGB_PORTAL` | B 67, B 75 | Large Monument |
| `DGB_OBELISK` | B 64, B 72 | Monument A |
| `DGB_MONUMENT` | B 65, B 73 | Monument B / Monument C |
| `DGB_STATUE_ANGEL` | B 80, B 88 | Statue |
| `DGB_STATUE_DEMON` | B 86, B 94 | Dragon Statue |
| `DGB_PILLAR` | B 96, B 104 | Obelisk |
| `DGB_PILLAR_WHITE` | B 99, B 107 | Stone Pillar B (Moss) |
| `DGB_LADDER` | B 12 | Metal Ladder |
| `DGB_ROCK` | B 32 | Gravel A (Dirt Cave) |
| `DGB_RUBBLE` | B 120 | Rubble |
| `DGB_BONES` | B 122 | Rubble (Ice) |
| `DGB_SKULLS` | B 121 | Rubble (Moss) |
| `DGB_CRYSTAL_PURPLE` | B 45, B 53, B 61 | Crystal / Large Crystal |
| `DGB_BARRICADE` | B 126 | Barricade A (H) |

## World tileset (id = 1)  (tileset 1)

| constant | tiles | what the sheet calls it |
| --- | --- | --- |
| `W_SEA` | A1 k0 | Sea |
| `W_GRASS` | A2 k16 | Grassland A |
| `W_GRASS_DARK` | A2 k17 | Grassland A (Dark) |
| `W_SAND` | A2 k26 | Dirt Field A |
| `W_SNOW` | A2 k40 | Snowfield |
| `W_WASTE` | A2 k32 | Desert A |
| `W_FOREST` | A2 k20 | Forest |
| `W_CONIFER` | A2 k21 | Forest (Conifer) |
| `W_HILLS` | A2 k22 | Mountain (Grass) |
| `W_HILLS_BROWN` | A2 k23 | Mountain (Dirt) |
| `W_MOUNTAIN` | A2 k38 | Mountain (Rock) |
| `W_VOLCANO` | A2 k39 | Mountain (Lava) |
| `W_ROAD` | A2 k29 | Road (Dirt) |
| `W_DUNES` | A2 k30 | Hill (Dirt) |
| `W_JUNGLE` | A2 k36 | Forest (Palm Trees) |
| `WB_VILLAGE` | B 96, B 97, B 104, B 105 | Fortress City |
| `WB_TOWN` | B 98, B 99, B 106, B 107 | Fortress City (Snow) |
| `WB_DARK_CASTLE` | B 26, B 27, B 34, B 35 | Collapsed Bridge (H) / Collapsed Bridge (V) / Castle B |
| `WB_STONE_CASTLE` | B 28, B 29, B 36, B 37 | Snow Bridge (H) / Snow Bridge (V) / Fort A |
| `WB_TOWER` | B 80, B 88 | Tower A |
| `WB_TOWER_WHITE` | B 84, B 92 | Tower A (Snow) |
| `WB_CAVE` | B 16 | Cave A |
| `WB_CAVE_DARK` | B 19 | Mine |
| `WB_SIGN` | B 1 | Sign |
| `WB_TREE` | B 11 | Giant Tree |
| `WB_HUT` | B 8 | Tent |
| `WB_ROCK` | B 13 | Dirt |

## SF_Outside_A3: the fronts of buildings (16-shape wall autotiles)  (tileset 5)

| constant | tiles | what the sheet calls it |
| --- | --- | --- |
| `SF_UPPER_BRICK` | A3 k48 | Roof A (Brick) |
| `SF_UPPER_FACTORY` | A3 k49 | Roof B (Factory) |
| `SF_UPPER_RUST` | A3 k50 | Roof C (Metal, Red Rust) |
| `SF_UPPER_BARRACKS` | A3 k51 | Roof D (Barracks) |
| `SF_UPPER_IVY` | A3 k54 | Roor G (Ivy) |
| `SF_WALL_STONE` | A3 k56 | Outer Wall A (Stone) |
| `SF_WALL_FACTORY` | A3 k57 | Outer Wall B (Factory) |
| `SF_WALL_RUST` | A3 k58 | Outer Wall C (Metal, Red Rust) |
| `SF_WALL_BARRACKS_A` | A3 k59 | Outer Wall D (Barracks) |
| `SF_WALL_BARRACKS_B` | A3 k60 | Outer Wall E (Barracks) |
| `SF_WALL_FACTORY_B` | A3 k61 | Outer Wall F (Factory) |
| `SF_WALL_IVY` | A3 k62 | Outer Wall G (Ivy) |
| `SF_UPPER_PATINA` | A3 k66 | Roof K (Metal, Patina) |
| `SF_UPPER_WOOD` | A3 k69 | Roof N (Wood) |
| `SF_WALL_TILE` | A3 k72 | Outer Wall I (Tile) |
| `SF_WALL_BRICK_MOSSY` | A3 k73 | Outer Wall J (Brick) |
| `SF_WALL_MORTAR` | A3 k74 | Outer Wall K (Mortar) |
| `SF_WALL_WOOD` | A3 k77 | Outer Wall N (Wood) |
| `SF_WALL_BRICK` | A3 k78 | Outer Wall O (Brick) |
| `SF_WALL_WOOD_LIGHT` | A3 k79 | Outer Wall P (Wood) |

## SF_Outside_A4: free-standing walls  (tileset 5)

| constant | tiles | what the sheet calls it |
| --- | --- | --- |
| `SF_YARD_RUST_TOP` | A4 k86 | Wall G (Metal, Red Rust) |
| `SF_YARD_RUST` | A4 k94 | Wall G (Metal, Red Rust) |
| `SF_YARD_PATINA_TOP` | A4 k87 | Wall H (Metal, Patina) |
| `SF_YARD_PATINA` | A4 k95 | Wall H (Metal, Patina) |
| `SF_YARD_BARRACKS_TOP` | A4 k96 | Wall I (Barracks) |
| `SF_YARD_BARRACKS` | A4 k104 | Wall I (Barracks) |
| `SF_YARD_BARRACKS2_TOP` | A4 k97 | Wall J (Barracks) |
| `SF_YARD_BARRACKS2` | A4 k105 | Wall J (Barracks) |
| `SF_YARD_FACTORY_TOP` | A4 k98 | Wall K (Factory) |
| `SF_YARD_FACTORY` | A4 k106 | Wall K (Factory) |
| `SF_YARD_FACTORY_L_TOP` | A4 k100 | Wall L (Factory) |
| `SF_YARD_FACTORY_L` | A4 k108 | Wall L (Factory) |
| `SF_YARD_FACTORY_M_TOP` | A4 k101 | Wall M (Factory) |
| `SF_YARD_FACTORY_M` | A4 k109 | Wall M (Factory) |
| `SF_YARD_BRICK_TOP` | A4 k103 | Wall O (Brick) |
| `SF_YARD_BRICK` | A4 k111 | Wall O (Brick) |
| `SF_YARD_WOOD_TOP` | A4 k116 | Wall T (Wood) |
| `SF_YARD_WOOD` | A4 k124 | Wall T (Wood) |
| `SF_YARD_WOOD_DIRTY_TOP` | A4 k117 | Wall U (Wood, Dirty) |
| `SF_YARD_WOOD_DIRTY` | A4 k125 | Wall U (Wood, Dirty) |

## SF_Outside_A5: the ground of the yard  (tileset 5)

| constant | tiles | what the sheet calls it |
| --- | --- | --- |
| `SF_WASTE` | A5 16 | Waste Land |
| `SF_METAL_FLOOR` | A5 17 | Metal Floor A (Factory) |
| `SF_METAL_FLOOR_RUINS` | A5 23 | Metal Floor A (Factory, Ruins) |
| `SF_CONCRETE` | A5 18 | Concrete Floor |
| `SF_CONCRETE_RUINS` | A5 19 | Concrete Floor (Ruins) |
| `SF_GRID_FLOOR` | A5 1 | Grid floor |
| `SF_DIRTY_FLOOR` | A5 32 | Dirty Floor |
| `SF_COBBLE_A` | A5 64 | Cobblestones A |
| `SF_COBBLE_B` | A5 65 | Cobblestones B |
| `SF_COBBLE_C` | A5 66 | Cobblestones C |
| `SF_MECHA_FLOOR` | A5 27 | Mecha Floor |
| `SF_WOOD_FLOOR` | A5 38 | Wood Floor A |
| `SF_HOLE` | A5 20 | Hole |
| `SF_STAIRS_METAL` | A5 44, A5 45, A5 46, A5 47 | Stairs B (Metal, Left) / Stairs B (Metal, Center) / Stairs B (Metal, Right) / Stairs B (Metal) |
| `SF_STAIRS_WOOD` | A5 60, A5 61, A5 62, A5 63 | Stairs D (Wood, Left) / Stairs D (Wood, Center) / Stairs D (Wood, Right) / Stairs D (Wood) |

## SF_Outside_B: what stands in the street  (tileset 5)

| constant | tiles | what the sheet calls it |
| --- | --- | --- |
| `SF_CHIMNEY_A` | B 104 | Chimney A |
| `SF_CHIMNEY_B` | B 105 | Chimney B |
| `SF_CHIMNEY_C` | B 106 | Chimney C |
| `SF_CRATE` | B 128 | Crate |
| `SF_BARREL` | B 131 | Barrel |
| `SF_STACKED_CRATES` | B 101, B 109 | Stacked Crates |
| `SF_MACHINE_A` | B 162 | Machine A |
| `SF_MACHINE_B` | B 163 | Machine B |
| `SF_MACHINE_C` | B 164 | Machine C |
| `SF_MACHINE_DEVICE` | B 153 | Machine Device |
| `SF_AIR_VENT_A` | B 178 | Air Vent A |
| `SF_AIR_VENT_B` | B 179 | Air Vent B |
| `SF_VENT` | B 199 | Vent |
| `SF_SMALL_FUEL_TANK` | B 188 | Small Fuel Tank |

## SF_Outside_C: the bigger structures  (tileset 5)

| constant | tiles | what the sheet calls it |
| --- | --- | --- |
| `SF_PILLAR_MACHINE` | C 331, C 339 | Pillar C (Machine) |
| `SF_PILLAR_METAL` | C 330, C 338 | Pillar B (Metal) |
| `SF_PILLAR_BRICK` | C 334, C 342 | Pillar F (Brick) |
| `SF_BROKEN_PILLAR_MACHINE` | C 347 | Broken Pillar C (Machine) |
| `SF_BROKEN_PILLAR_BRICK` | C 350 | Broken Pillar F (Brick) |
| `SF_IRON_FENCE_A` | C 459, C 467, C 475 | Iron Fence A |
| `SF_IRON_FENCE_B` | C 439 | Iron Fence B |
| `SF_METAL_FENCE` | C 306, C 307, C 308 | Metal Fence |
| `SF_SPHERE_MACHINERY` | C 370, C 371, C 372, C 378, C 379, C 380 | Sphere Machinery |
| `SF_WATER_TANK` | C 492, C 500 | Water Storage Tank |
| `SF_ROUND_CLOCK` | C 465 | Round Clock |
| `SF_SIGN_POST` | C 336, C 344 | Warning Plate |
| `SF_WARNING_PLATE` | C 315 | Warning Plate |
| `SF_CANOPY` | C 278, C 286 | Shop Canopy |
| `SF_PUMP` | C 270 | Water Well Pump |
| `SF_POSTBOX` | C 318 | Postal Box |
| `SF_BENCH` | C 275, C 276 | Bench A |
| `SF_BENCH_B` | C 283, C 284 | Bench B |
| `SF_DUMPSTER` | C 271 | Garbage Dumpster |
| `SF_WEEDS` | C 288 | Grass A |
| `SF_WEEDS_B` | C 289 | Grass B |
| `SF_RUBBLE` | C 291 | Small Stones |

## Inside furniture, by name  (tileset 3)

| constant | tiles | what the sheet calls it |
| --- | --- | --- |
| `IN_TABLE_TOP` | A2 k23 | Table A (Wood) |
| `IN_TABLE_DARK` | A2 k31 | Table B (Dark Wood) |
| `IN_BOOKCASE_WIDE` | B 158, B 159, B 166, B 167 | Bookshelf B |

## the Long Field  (tileset 5)

| constant | tiles | what the sheet calls it |
| --- | --- | --- |
| `SF_RAILING` | C 439 | Iron Fence B |
| `SF_RAILING_PIER` | C 459, C 467, C 475 | Iron Fence A |
| `SF_GATE_LEAF` | C 447, C 455 | Gate |

## SF Inside (tileset id = 6)  (tileset 6)

| constant | tiles | what the sheet calls it |
| --- | --- | --- |
| `SF_IN_WALL_CONCRETE` | A4 k80 | Wall A (Concrete) |
| `SF_IN_FACE_CONCRETE` | A4 k88 | Wall A (Concrete) |
| `SF_IN_WALL_HOUSE` | A4 k82 | Wall C (House) |
| `SF_IN_FACE_HOUSE` | A4 k90 | Wall C (House) |
| `SF_IN_WALL_METAL` | A4 k83 | Wall D (Metal) |
| `SF_IN_FACE_METAL` | A4 k91 | Wall D (Metal) |
| `SF_IN_WALL_RUST` | A4 k84 | Wall E (Metal, Red Rust) |
| `SF_IN_FACE_RUST` | A4 k92 | Wall E (Metal, Red Rust) |
| `SF_IN_WALL_BARRACKS` | A4 k86 | Wall G (Barracks) |
| `SF_IN_FACE_BARRACKS` | A4 k94 | Wall G (Barracks) |
| `SF_IN_WALL_FACTORY` | A4 k96 | Wall I (Factory) |
| `SF_IN_FACE_FACTORY` | A4 k104 | Wall I (Factory) |
| `SF_IN_WALL_FACTORY_B` | A4 k97 | Wall J (Factory) |
| `SF_IN_FACE_FACTORY_B` | A4 k105 | Wall J (Factory) |
| `SF_IN_WALL_PATTERN` | A4 k98 | Interior Wall A (Pattern) |
| `SF_IN_FACE_PATTERN` | A4 k106 | Interior Wall A (Pattern) |
| `SF_IN_WALL_PATTERN_B` | A4 k99 | Interior Wall B (Pattern) |
| `SF_IN_FACE_PATTERN_B` | A4 k107 | Interior Wall B (Pattern) |
| `SF_IN_WALL_BRICK` | A4 k103 | Wall K (Brick) |
| `SF_IN_FACE_BRICK` | A4 k111 | Wall K (Brick) |
| `SF_IN_WALL_WOOD` | A4 k112 | Wall L (Wood) |
| `SF_IN_FACE_WOOD` | A4 k120 | Wall L (Wood) |
| `SF_FLOOR_RESIN` | A5 48 | Interior Floor A (Green Resin) |
| `SF_FLOOR_TILE` | A5 49 | Interior Floor B (Tile) |
| `SF_FLOOR_DECO` | A5 51 | Interior Floor C (Decoration) |
| `SF_FLOOR_WOOD` | A5 54 | Wood Floor B |
| `SF_FLOOR_CARPET` | A5 89 | Interior Floor F (Tile Carpet) |
| `SF_FLOOR_MARBLE` | A5 96 | Marble Floor |
| `SF_FLOOR_LINO` | A5 97 | Interior Floor G (Linoleum) |
| `SF_THRESHOLD` | A5 47 | Stairs B (Metal) |

## drawing  (tileset 6)

| constant | tiles | what the sheet calls it |
| --- | --- | --- |
| `IN_FLIGHT` | A5 88, A5 90 | Neon Floor / Interior Floor F (Tile Carpet, Ruins) |
| `IN_STEP` | A5 91 | Ledge (Demonic Ground) |
