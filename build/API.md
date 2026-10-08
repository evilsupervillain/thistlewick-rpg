# Build-script API

**Generated - `python3 ../../tools/apidigest.py . --write`.** Do not
edit by hand. `--check` exits non-zero when it is stale.

Signatures and the first line of each docstring, for the modules
that are *libraries*. The content modules - every other
`build/*.py`, one per region or site - are deliberately not here:
their functions are used once each, and `CLAUDE.md` already says in
a line what each file holds.

**Read this instead of opening a module to find out what it does.**
Open one when you are *changing* it, and then open only that one.

It is long enough to be worth not reading whole: it is laid out one
`##` section per module so a single section can be read on its own,
and the constant blocks are there to be **grepped** - `grep -n
SW_ build/API.md` for a switch, `grep -n Ashbury build/API.md` for
who has a face - rather than scrolled.


## `rmmzdata` — tools/rmmzdata.py

Toolkit for reading/writing RPG Maker MZ data files by hand.

### `class MapGrid`

Six-layer tile grid: 0/1 = ground layers, 2/3 = upper layers,

```
idx(x, y, z)
get(x, y, z=0)
set(x, y, z, tile)
fill(x1, y1, x2, y2, z, tile)
rect(x1, y1, x2, y2, z, tile)
stamp(src_map, sx, sy, w, h, dx, dy, layers=(0, 1, 2, 3, 4, 5)) Copy a rectangle of tiles out of another map, the way you would
autotile(z=0, kinds=None)                            Recompute autotile shapes on layer z from tile adjacency, the way
```

### functions

```
find_project(start=None)                             A project is a directory containing data/System.json. Looks at the given
use_project(path=None)                               Point the module at a project. Called automatically on first access.
autotile_kind(tile_id)
autotile_shape(tile_id)
make_autotile(kind, shape)
is_autotile(tile_id)
is_waterfall_autotile(tile_id)                       A1's odd kinds from 4 up are waterfalls, and the engine looks their
is_wall_autotile(tile_id)                            A3 tiles, and the odd kind-rows of A4, are 16-shape 'wall' autotiles;
load(name)
save_object(name, obj)                               System.json-style: a single line.
save_list(name, items)                               Actors.json-style: one element per line between brackets.
map_text(m)                                          A map file's exact text, the way the editor writes one.
save_map(map_id, m)
load_map(map_id)
message_width(face=False)                            How many pixels of a message line the player will actually see.
text_width(text, font_size=FONT_SIZE, currency='G', digits=4) Pixels the engine will draw `text` in, following processEscapeCharacter.
fits(text, width, **kw)
wrap(text, width, **kw)                              Break `text` into lines that fit in `width` pixels, on word boundaries.
image(character_name='', character_index=0, direction=2, pattern=1, tile_id=0)
page(commands, img=None, trigger=0, priority=1, conditions=None, through=False, walk_anime=True, step_anime=False, direction_fix=False, move_type=0, move_speed=3, move_frequency=3) trigger: 0 action button, 1 player touch, 2 event touch, 3 autorun, 4 parallel
event(event_id, name, x, y, pages, note='')
text(lines, face_name='', face_index=0, background=0, position=2, indent=0) Show Text. background: 0 window 1 dim 2 transparent; position: 0 top 1 middle 2 bottom
comment(lines, indent=0)                             Comment: 108 for the first line and 408 for every one after it.
choices(options, cancel_type=-1, default=0, position=2, background=0, indent=0)
when(index, label, indent=0)
when_cancel(indent=0)
branch_end(indent=0)                                 Terminator RPG Maker puts at the end of every branch body.
choices_end(indent=0)
transfer(map_id, x, y, direction=0, fade=0, indent=0) direction 0=retain, 2 down, 4 left, 6 right, 8 up; fade 0=black 1=white 2=none
set_vehicle_location(vehicle, map_id, x, y, indent=0) Park a vehicle somewhere. `vehicle` is BOAT, SHIP or AIRSHIP.
play_se(name, volume=90, pitch=100, pan=0, indent=0)
play_me(name, volume=90, pitch=100, pan=0, indent=0)
gain_item(item_id, amount=1, indent=0)
gain_weapon(weapon_id, amount=1, indent=0)
gain_armor(armor_id, amount=1, indent=0)
gain_gold(amount, indent=0)
lose_gold(amount, indent=0)                          Change Gold has a separate 'decrease' operation - a negative amount on
learn_skill(actor_id, skill_id, learn=True, indent=0) Change Skill for one actor, by id. `learn=False` forgets it.
self_switch(ch, on=True, indent=0)
control_switch(switch_id, on=True, indent=0)
battle(troop_id, can_escape=True, can_lose=False, indent=0)
shop(goods, purchase_only=False, indent=0)           goods: list of (kind, id, price_type, price); kind 0 item 1 weapon 2 armor
recover_all(actor_id=0, indent=0)                    Recover All. `actor_id` 0 is the whole party, which is what an inn
change_party(actor_id, add=True, initialize=False, indent=0)
wait(frames, indent=0)
script(lines, indent=0)
move_route(target, steps, repeat=True, skippable=False, wait_flag=False, indent=0) target: -1 player, 0 this event, >0 event id. steps: list of route codes.
condition_self_switch(ch, on=True, indent=0)
condition_switch(switch_id, on=True, indent=0)
else_branch(indent=0)
end_branch(indent=0)
control_variable(variable_id, value, operation=0, indent=0)
control_variable_add(variable_id, amount=1, indent=0)
control_variable_script(variable_id, expression, operation=0, indent=0)
condition_variable(variable_id, value, comparison=0, indent=0) comparison: 0 ==, 1 >=, 2 <=, 3 >, 4 <, 5 !=
condition_script(expression, indent=0)
condition_item(item_id, indent=0)
condition_actor_in_party(actor_id, indent=0)
call_common_event(common_event_id, indent=0)
label(name, indent=0)
jump_to_label(name, indent=0)
exit_event(indent=0)
erase_event(indent=0)
game_over(indent=0)
return_to_title(indent=0)
fadeout_screen(indent=0)
fadein_screen(indent=0)
tint_screen(tone, duration=60, wait_flag=True, indent=0) tone: [red, green, blue, grey], each -255..255.
flash_screen(colour, duration=30, wait_flag=True, indent=0) colour: [red, green, blue, intensity], each 0..255.
shake_screen(power=5, speed=5, duration=60, wait_flag=True, indent=0)
set_weather(kind='none', power=5, duration=60, wait_flag=False, indent=0) kind: one of WEATHER; power 1-9; duration in frames, 0 for instant.
show_animation(target, animation_id, wait_flag=True, indent=0) target: -1 player, 0 this event, >0 event id.
show_balloon(target, balloon_id, wait_flag=False, indent=0) balloon_id: 1 exclamation, 2 question, 3 music note, 4 heart, 5 anger,
set_transparency(transparent=True, indent=0)
scroll_map(direction, distance, speed=4, wait_flag=True, indent=0) direction: 2 down, 4 left, 6 right, 8 up.
play_bgm(name, volume=90, pitch=100, pan=0, indent=0)
fadeout_bgm(seconds=3, indent=0)
save_bgm(indent=0)
replay_bgm(indent=0)
change_hp(actor_spec, value, allow_death=False, indent=0) actor_spec: (0, actorId) for a fixed actor, or (1, variableId).
change_exp(actor_spec, amount, show_level_up=True, indent=0)
change_level(actor_spec, amount, show_level_up=True, indent=0)
open_save_screen(indent=0)
open_menu(indent=0)
name_input(actor_id, max_chars=8, indent=0)
shift(commands, base)                                Re-indent a command list so its outermost commands sit at `base`.
if_then(condition, then_commands, else_commands=None, indent=0) Conditional Branch. `condition` is one of the condition_* commands;
choice_block(options, branches, cancel=None, default=0, position=2, background=0, indent=0) Show Choices with one body per option, each written at indent 0.
```


## `mapkit` — build/mapkit.py

Tile vocabulary and drawing helpers for The Obligatory Quest.

**Tile constants (356)** - names only. What each one actually is, off the sheet's own `.txt`, is in `build/TILENAMES.md`; regenerate it with `tools/tileaudit.py`. The `SF_*` constants are not among them because they are not written as numbers: they look their tile up by the sheet's own name at import time, so they cannot be wrong and the definition below is already the answer.

```
GRASS                   PATH                    COBBLE                  PAVING
HEDGE                   DECKING                 SAND                    WHEAT
SOIL                    DARK_GRASS              WATER                   CLIFF_TOP
CLIFF_FACE              WALL_SHINGLE            WALL_THATCH             WALL_LOG
WALL_BLUE_TILE          WALL_SANDBRICK          WALL_PLASTER            WALL_BRICK_RED
WALL_ICE                WALL_PLANK              WALL_PLANK_LIGHT        WALL_TIMBER
WALL_BRICK_PURPLE       WALL_BRICK_GREEN        WALL_COLUMNS            WALL_CONCRETE
WALL_MOSSY              WALL_STONE              WALL_STONE_WHITE        WALL_STONE_DARK
WALL_MOSS_STONE         TREE                    TREE_DARK               STALL
STALL_FRUIT             TENT                    PALM                    BUSH
BUSH2                   BUSH3                   FLOWERS                 FLOWERS2
FLOWERS3                ROCK                    ROCK2                   LOGS
TUB                     BARREL                  CRATE                   POT
BUCKET                  SIGNPOST                GRAVE_A                 GRAVE_B
FENCE_PANEL             STOVEPIPE               LILYPAD                 MUSHROOMS
BURROW                  BRAMBLES                DEAD_BUSH               DEAD_TREE
DEAD_ROOTS              LADDER                  REEDS                   LAMP
SIGN_BLADE              SIGN_ORB                SIGN_ARMOR              SIGN_RING
SIGN_POTION             SIGN_INN                SIGN_MUG                SIGN_PLATE
SIGN_WAND               SIGN_COIN               SIGN_HAMMER             SIGN_SUN
DOORWAY_DARK            DOOR_SHUT               DOORWAY_ARCH            WINDOW
WINDOW_GLASS            DOOR_DOUBLE             IN_WOOD_FLOOR           IN_COBBLE
IN_DARK_WOOD            IN_RED_CARPET           IN_SANDSTONE            IN_DIAMOND_TILE
IN_PARQUET              IN_BRICK_FLOOR          IN_PURPLE_RUG           IN_GREEN_RUG
IN_BLUE_RUG             IN_RED_RUG              IN_WALL_TOP             IN_WALL_FACE
IN_WALL_TOP_PLANK       IN_WALL_FACE_PLANK      IN_WALL_TOP_STONE       IN_WALL_FACE_STONE
IN_WALL_TOP_TAN         IN_WALL_FACE_TAN        IN_WALL_TOP_WHITE       IN_WALL_FACE_WHITE
IN_WALL_TOP_RED         IN_WALL_FACE_RED        IN_WALL_TOP_GOLD        IN_WALL_FACE_GOLD
IN_WALL_TOP_PURPLE      IN_WALL_FACE_PURPLE     IN_VOID                 IN_BED
IN_BED_ORANGE           IN_BED_BROWN            IN_BOOKCASE             IN_BOOKCASE2
IN_CURTAIN_GREEN        IN_SHELF_JARS           IN_SHELF_BOTTLES        IN_SHELF_FRUIT
IN_SHELF_GOODS          IN_CABINET              IN_DRESSER              IN_COUNTER
IN_PILLAR               IN_FIREPLACE            IN_PIANO                IN_ORGAN
IN_TABLE_ROUND          IN_TABLE_SMALL          IN_POT                  IN_CRATE
IN_CRATE2               IN_BARREL               IN_BARREL2              IN_SACK
IN_SACK2                IN_SOFA                 IN_CURTAIN_RED          IN_WINDOW
IN_STAINED_GLASS        IN_SWORD_RACK           IN_NOTICE_BOARD         IN_CLOCK
IN_MIRROR               IN_THRONE               IN_RAILING              IN_STOVE
IN_KITCHEN_COUNTER      IN_TABLE                IN_TABLE_ONE            IN_STOOL
IN_TABLE_PLAIN          IN_BOOKSHELF            IN_WINE_RACK            IN_KITCHEN
INC_BOOK                INC_BOOK2               INC_SCROLL              INC_SCROLL2
INC_CANDLES             INC_PLANT               INC_PLANT2              INC_CHEST_PROP
INC_POTION_BLUE         INC_POTION_GREEN        INC_POTION_RED          INC_FRUIT
INC_BASKET              INC_BOTTLE              INC_BOTTLES             INC_GOBLET
INC_MEAL                INC_MEAL2               INC_ARMOR_STAND         INC_LAMP
INC_BELL                INC_DESK_BELL           INC_SWORD_STAND         INC_CASE
INC_OPEN_BOOK           DG_FLOOR                DG_FLOOR2               DG_WALL_TOP
DG_WALL_FACE            DG_VOID                 DGB_GATE                DGB_PORTAL
DGB_OBELISK             DGB_MONUMENT            DGB_STATUE_ANGEL        DGB_STATUE_DEMON
DGB_PILLAR              DGB_PILLAR_WHITE        DGB_LADDER              DGB_ROCK
DGB_RUBBLE              DGB_BONES               DGB_SKULLS              DGB_CRYSTAL_PURPLE
DGB_BARRICADE           W_SEA                   W_GRASS                 W_GRASS_DARK
W_SAND                  W_SNOW                  W_WASTE                 W_FOREST
W_CONIFER               W_HILLS                 W_HILLS_BROWN           W_MOUNTAIN
W_VOLCANO               W_ROAD                  W_DUNES                 W_JUNGLE
WB_VILLAGE              WB_TOWN                 WB_DARK_CASTLE          WB_STONE_CASTLE
WB_TOWER                WB_TOWER_WHITE          WB_CAVE                 WB_CAVE_DARK
WB_SIGN                 WB_TREE                 WB_HUT                  WB_ROCK
SF_UPPER_BRICK          SF_UPPER_FACTORY        SF_UPPER_RUST           SF_UPPER_BARRACKS
SF_UPPER_IVY            SF_WALL_STONE           SF_WALL_FACTORY         SF_WALL_RUST
SF_WALL_BARRACKS_A      SF_WALL_BARRACKS_B      SF_WALL_FACTORY_B       SF_WALL_IVY
SF_UPPER_PATINA         SF_UPPER_WOOD           SF_WALL_TILE            SF_WALL_BRICK_MOSSY
SF_WALL_MORTAR          SF_WALL_WOOD            SF_WALL_BRICK           SF_WALL_WOOD_LIGHT
SF_YARD_RUST_TOP        SF_YARD_RUST            SF_YARD_PATINA_TOP      SF_YARD_PATINA
SF_YARD_BARRACKS_TOP    SF_YARD_BARRACKS        SF_YARD_BARRACKS2_TOP   SF_YARD_BARRACKS2
SF_YARD_FACTORY_TOP     SF_YARD_FACTORY         SF_YARD_FACTORY_L_TOP   SF_YARD_FACTORY_L
SF_YARD_FACTORY_M_TOP   SF_YARD_FACTORY_M       SF_YARD_BRICK_TOP       SF_YARD_BRICK
SF_YARD_WOOD_TOP        SF_YARD_WOOD            SF_YARD_WOOD_DIRTY_TOP  SF_YARD_WOOD_DIRTY
SF_WASTE                SF_METAL_FLOOR          SF_METAL_FLOOR_RUINS    SF_CONCRETE
SF_CONCRETE_RUINS       SF_GRID_FLOOR           SF_DIRTY_FLOOR          SF_COBBLE_A
SF_COBBLE_B             SF_COBBLE_C             SF_MECHA_FLOOR          SF_WOOD_FLOOR
SF_HOLE                 SF_STAIRS_METAL         SF_STAIRS_WOOD          SF_CHIMNEY_A
SF_CHIMNEY_B            SF_CHIMNEY_C            SF_CRATE                SF_BARREL
SF_STACKED_CRATES       SF_MACHINE_A            SF_MACHINE_B            SF_MACHINE_C
SF_MACHINE_DEVICE       SF_AIR_VENT_A           SF_AIR_VENT_B           SF_VENT
SF_SMALL_FUEL_TANK      SF_PILLAR_MACHINE       SF_PILLAR_METAL         SF_PILLAR_BRICK
SF_BROKEN_PILLAR_MACHINE  SF_BROKEN_PILLAR_BRICK  SF_IRON_FENCE_A         SF_IRON_FENCE_B
SF_METAL_FENCE          SF_SPHERE_MACHINERY     SF_WATER_TANK           SF_ROUND_CLOCK
SF_SIGN_POST            SF_WARNING_PLATE        SF_CANOPY               SF_PUMP
SF_POSTBOX              SF_BENCH                SF_BENCH_B              SF_DUMPSTER
SF_WEEDS                SF_WEEDS_B              SF_RUBBLE               SF_RAILING
SF_RAILING_PIER         SF_GATE_LEAF            SF_IN_WALL_CONCRETE     SF_IN_FACE_CONCRETE
SF_IN_WALL_HOUSE        SF_IN_FACE_HOUSE        SF_IN_WALL_METAL        SF_IN_FACE_METAL
SF_IN_WALL_RUST         SF_IN_FACE_RUST         SF_IN_WALL_BARRACKS     SF_IN_FACE_BARRACKS
SF_IN_WALL_FACTORY      SF_IN_FACE_FACTORY      SF_IN_WALL_FACTORY_B    SF_IN_FACE_FACTORY_B
SF_IN_WALL_PATTERN      SF_IN_FACE_PATTERN      SF_IN_WALL_PATTERN_B    SF_IN_FACE_PATTERN_B
SF_IN_WALL_BRICK        SF_IN_FACE_BRICK        SF_IN_WALL_WOOD         SF_IN_FACE_WOOD
SF_FLOOR_RESIN          SF_FLOOR_TILE           SF_FLOOR_DECO           SF_FLOOR_WOOD
SF_FLOOR_CARPET         SF_FLOOR_MARBLE         SF_FLOOR_LINO           SF_THRESHOLD
```

**Everything else.**

```
GAME                         os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKSPACE                    os.path.dirname(GAME)
TS_WORLD                     1
TS_OUTSIDE                   2
TS_INSIDE                    3
TS_DUNGEON                   4
TS_COLLEGIUM                 7
TS_OVERWORLD                 8
ROOF_GREEN                   (8, 0)
ROOF_WHITE                   (13, 0)
ROOF_GOLD                    (8, 3)
ROOF_BROWN                   (13, 3)
ROOF_PURPLE                  ROOF_GREEN
TOWER_STONE                  (8, 6)
TOWER_WHITE                  (10, 6)
TS_CLANGING                  5
TS_CLANGING_IN               6
SF_CLOCK_TOWER               (12, 3)
SF_ROOF                      (13, 12)
DGE_BASIN                    borrowed('Inside_C', 'Large Basin')
DGE_HAMPER                   borrowed('Inside_C', 'Basket A')
IN_TABLE_WOOD                sf_tile('Inside_B', 'Table D')
IN_STOOL_SQUARE              sf_tile('Inside_B', 'Stool C')
IN_BARREL_WOOD               sf_tile('Inside_B', 'Barrel')
IN_STONE_PILLAR              sf_block('Inside_B', 'Stone Pillar A')
IN_LONGCASE_CLOCK            sf_block('Inside_B', 'Clock')
IN_PIANO_WHOLE               _rows(sf_block('Inside_B', 'Piano'), 3)
IN_PIPE_ORGAN                _rows(sf_block('Inside_B', 'Pipe Organ'), 3)
INC_SCROLLS                  sf_tile('Inside_C', 'Scrolls A')
INC_ALTAR                    _rows(sf_block('Inside_C', 'Church Table'), 3)
INC_ARMOUR_STEEL             sf_tile('Inside_C', 'Armor B (Stand)')
INC_COAT_STAND               sf_tile('Inside_C', "Women's Clothing C (Stand)")
SF_SIGN_BLANK                sf_tile('SF_Outside_B', 'Metal Shop Sign (Blank)')
SF_SIGN_WEAPON               sf_tile('SF_Outside_B', 'Metal Shop Sign (Weapon)')
SF_SIGN_ARMOR                sf_tile('SF_Outside_B', 'Metal Shop Sign (Armor)')
SF_SIGN_ITEM                 sf_tile('SF_Outside_B', 'Metal Shop Sign (Item)')
SF_SIGN_PHARMACY             sf_tile('SF_Outside_B', 'Metal Shop Sign (Pharmacy)')
SF_SIGN_CAFE                 sf_tile('SF_Outside_B', 'Metal Shop Sign (Cafe)')
SF_SIGN_INN                  sf_tile('SF_Outside_B', 'Metal Shop Sign (Inn)')
SF_WINDOWS                   ...
SF_WINDOWS_TALL              ...
SF_WINDOW                    SF_WINDOWS[0]
SF_WINDOW_LOUVRE             SF_WINDOWS[2]
SF_WINDOW_TALL               SF_WINDOWS_TALL[0]
SF_ENTRANCE_A                sf_tile('SF_Outside_B', 'Entrance A')
SF_ENTRANCE_B                sf_tile('SF_Outside_B', 'Entrance B')
SF_SHUTTER                   sf_tile('SF_Outside_B', 'Shutter')
SF_EXHAUST_WALL              sf_tile('SF_Outside_B', 'Exhaust Port Wall')
SF_WALL_POSTER               sf_tile('SF_Outside_B', 'Wall Poster')
SF_AIR_INTAKE                sf_tile('SF_Outside_B', 'Outdoor Air Intake Unit')
SF_OIL_DRUM                  sf_tile('SF_Outside_B', 'Oil Drum')
SF_OIL_DRUM_LEAK             sf_tile('SF_Outside_B', 'Oil Drum (Leak)')
SF_LADDER                    sf_block('SF_Outside_B', 'Metal Ladder')
SF_FIRE_ESCAPE               sf_block('SF_Outside_B', 'Metal Stairs')
SF_PLAQUE                    sf_tile('SF_Outside_B', 'Tombstone (Plaque)')
SF_SCRAP                     sf_tile('SF_Outside_B', 'Scrap Metal')
SF_IRONWORK                  sf_tile('SF_Outside_B', 'Iron Materials')
SF_SPOIL                     sf_tile('SF_Outside_B', 'Waste')
SF_ROPE                      sf_block('SF_Outside_B', 'Rope')
SF_NETTING                   sf_block('SF_Outside_B', 'Net')
SF_BROKEN_PILLAR_METAL       sf_tile('SF_Outside_C', 'Broken Pillar B (Metal)')
SF_FISSURE                   sf_block('SF_Outside_B', 'Fissures A')
SF_IN_MACHINE_C              sf_tile('SF_Inside_C', 'Machine C')
SF_IN_AIR_VENT               sf_tile('SF_Inside_C', 'Air Vent A')
SF_IN_RUBBLE                 sf_tile('SF_Inside_C', 'Rubble')
SF_IN_PIPE_H                 sf_tile('SF_Inside_C', 'Pipe (H)')
SF_IN_PIPE_V                 sf_block('SF_Inside_C', 'Pipe (V)')
SF_IN_PLUMBING               ...
SF_IN_VALVE                  sf_tile('SF_Inside_C', 'Valve')
SF_IN_DUCT                   sf_block('SF_Inside_C', 'Duct')
SF_IN_MECH_DEVICE            sf_block('SF_Inside_C', 'Mechanical Device')
SF_IN_BELT_H                 sf_block('SF_Inside_C', 'Belt Conveyor (H)')
SF_IN_BELT_V                 sf_block('SF_Inside_C', 'Belt Conveyor (V)')
SF_IN_AIR_VENT_A             sf_tile('SF_Inside_C', 'Air Vent A')
SF_IN_AIR_VENT_B             sf_tile('SF_Inside_C', 'Air Vent B')
SF_IN_VENT                   sf_tile('SF_Inside_C', 'Vent')
SF_IN_DRAIN                  sf_tile('SF_Inside_C', 'Drain')
SF_IN_PAPERS                 sf_tile('SF_Inside_C', 'Scattered Papers')
SF_IN_RUBBLE                 sf_tile('SF_Inside_C', 'Rubble')
SF_IN_RUBBLE_PILE            sf_grid('SF_Inside_C', 'Pile of Rubble', 2)
SF_IN_HANDRAIL               sf_block('SF_Inside_C', 'Handrail')[:3]
SF_IN_GIRDER                 ...
SF_IN_WARNING                sf_tile('SF_Inside_B', 'Warning Plate B')
SF_IN_METAL_RUBBLE           sf_tile('SF_Inside_B', 'Rubble B (Metal)')
SF_IN_STEEL_SHELF            sf_block('SF_Inside_B', 'Steel Shelf')
SF_IN_DOC_SHELF              sf_block('SF_Inside_B', 'Document Shelf')
SF_IN_BOOKSHELF              sf_block('SF_Inside_B', 'Bookshelf A')
SF_IN_DRAWERS                sf_block('SF_Inside_B', 'Chest of Drawers A')
SF_IN_ODDMENTS               sf_block('SF_Inside_B', 'Miscellaneous Item Shelf')
SF_IN_LOCKER                 sf_block('SF_Inside_B', 'Locker A')
SF_IN_MEDICINE_SHELF         sf_block('SF_Inside_B', 'Medicine Shelf')
SF_IN_STACKED_CRATES         sf_block('SF_Inside_B', 'Stacked Crates')
SF_IN_CHEST_WOOD             sf_tile('SF_Inside_B', 'Chest A (Wood)')
SF_IN_CHEST_METAL            sf_tile('SF_Inside_B', 'Chest B (Metal)')
SF_IN_DESK_LARGE             sf_block('SF_Inside_B', 'Large Desk A')
SF_IN_DESK_LARGE_B           sf_block('SF_Inside_B', 'Large Desk B')
SF_IN_DESK                   sf_tile('SF_Inside_B', 'Desk')
SF_IN_SIDE_DESK              sf_tile('SF_Inside_B', 'Side Desk A (Wood)')
SF_IN_SIDE_DESK_METAL        sf_tile('SF_Inside_B', 'Side Desk B (Metal)')
SF_IN_BOOK_STAND             sf_tile('SF_Inside_B', 'Book Stand')
SF_IN_DOCUMENT               sf_tile('SF_Inside_B', 'Document')
SF_IN_BULLETIN               sf_tile('SF_Inside_C', 'Bulletin Board')
SF_IN_WALL_CLOCK             sf_block('SF_Inside_C', 'Wall Clock')
SF_IN_PARTITION              sf_block('SF_Inside_C', 'Partition A')
SF_IN_FIREPLACE              sf_grid('SF_Inside_C', 'Fireplace', 3)
SF_IN_ARMCHAIR               sf_block('SF_Inside_C', 'Armchair')
SF_IN_STOOL                  sf_tile('SF_Inside_C', 'Stool')
SF_IN_TABLE                  sf_tile('SF_Inside_C', 'Side Table')
SF_IN_BED                    sf_block('SF_Inside_B', 'Bed')
SF_IN_BED_IRON               sf_block('SF_Inside_B', 'Pipe Frame Bed')
SF_IN_CURTAINS               sf_block('SF_Inside_C', 'Curtains A')
SF_IN_CURTAINS_B             sf_block('SF_Inside_C', 'Curtains B')
SF_IN_WINDOW                 sf_block('SF_Inside_B', 'Midsize Window A')
SF_IN_LAMP                   sf_tile('SF_Inside_C', 'Lamp')
SF_IN_PICTURE                sf_tile('SF_Inside_C', 'Picture Frame')
SF_IN_PAINTING_A             sf_tile('SF_Inside_C', 'Painting A')
SF_IN_PAINTING_B             sf_tile('SF_Inside_C', 'Painting B')
SF_IN_PLANT                  sf_block('SF_Inside_C', 'Plant A')
SF_IN_POTTED_PLANT           sf_tile('SF_Inside_C', 'Potted Plant')
SF_IN_SINK                   sf_tile('SF_Inside_B', 'Sink')
SF_IN_MATTRESS               sf_tile('SF_Inside_B', 'Mattress')
SF_IN_SPIDER_WEB             sf_tile('SF_Inside_C', 'Spider Web')
SF_IN_DRIPPING               sf_tile('SF_Inside_C', 'Dripping')
SF_IN_MUG                    sf_tile('SF_Inside_C', 'Beer Mug')
SF_IN_WINE                   sf_tile('SF_Inside_C', 'Wine & Glass')
SF_IN_BREAD                  sf_tile('SF_Inside_C', 'Bread')
SF_IN_MEAT                   sf_tile('SF_Inside_C', 'Meat Dish')
SF_IN_CHICKEN                sf_tile('SF_Inside_C', 'Roast Chicken')
SF_IN_PLATE                  sf_tile('SF_Inside_C', 'Plate A')
SF_IN_PLATE_B                sf_tile('SF_Inside_C', 'Plate B')
SF_IN_TEAPOT                 sf_tile('SF_Inside_C', 'Teapot & Cup')
SF_IN_FRUIT                  sf_tile('SF_Inside_C', 'Fruit Bowl')
SF_IN_BOOK                   sf_tile('SF_Inside_C', 'Book A')
SF_IN_VASE                   sf_tile('SF_Inside_C', 'Vase')
SF_FORBIDDEN_NAMES           ...
SF_INSIDE_FORBIDDEN_NAMES    ...
SF_FORBIDDEN                 _forbidden(SF_FORBIDDEN_NAMES)
SF_INSIDE_FORBIDDEN          _forbidden(SF_INSIDE_FORBIDDEN_NAMES)
TILESET_ROOFS                ...
TILESET_FORBIDDEN            ...
BANNER_PURPLE                sf_block('Outside_C', 'Tapestry B')
WALL_MOUNTED                 ...
CHIMNEY_STACK                sf_block('Outside_C', 'Chimney')
ROOF_MOUNTED                 ...
```

### `class ForbiddenTile`

A tile from the wrong century was drawn on a northern map.

### `class BuildingOverlap`

Something was drawn on top of a house.

### `class Canvas`

A MapGrid that knows how to draw the things above.

```
set(x, y, z, tile)
autotile(*args, **kwargs)
blit(x, y, z, block)                                 Draw a tuple-of-rows block of raw tile ids with its top-left at x,y.
column(x, y, z, tiles)                               Draw a vertical run of tiles - a lamp post, a window, a doorway.
scatter(spots, z, tile)
roof(x, y, w, h, roof, z=3)                          Nine-slice a roof over a w x h rectangle. Needs w >= 2 and h >= 2.
chimney(x, y, tile)                                  A chimney on a roof, drawn so that it is actually visible.
crest(x, y, w, wall)                                 Block the top row of a roof before the building is drawn.
clock_tower(x, y, h=5, z=3)                          The Clock Tower, three tiles wide and `h` tall, with its base at
building(x, y, w, h, wall=WALL_PLANK, roof=ROOF_BROWN, wall_rows=2, register=True) A house: `wall_rows` rows of A3 wall along the bottom on layer 0,
dungeon_walls(top, face, z=0)                        Turn solid rock into a cave wall: the two rows of rock directly
path_h(x1, x2, y, tile=PATH, thickness=1, z=0)
path_v(x, y1, y2, tile=PATH, thickness=1, z=0)
blob(cx, cy, rx, ry, z, tile)                        A rough ellipse of tiles - a pond, a copse, a patch of flowers.
```

### functions

```
b_tile(col, row)                                     A tile on the B sheet, by its (column, row) on the 16x16 grid.
c_tile(col, row)
a5(n)                                                A plain, non-autotiling A5 tile by its index on that sheet.
A(kind)                                              An autotile in its default shape; `MapGrid.autotile` fixes the shape up.
tile_names(sheet)                                    `{name: [tile id, ...]}` for a B/C/D/E sheet, from the editor's own tile
sf_tile(sheet, name, index=0)                        One tile, by the name the editor's palette gives it. Safer than counting
sf_block(sheet, name)                                Every tile of a multi-tile prop, in reading order - so a three-tile
borrowed(sheet, name)                                Every tile of a stock Inside_B/Inside_C prop, by name, as it is
sf_grid(sheet, name, w)                              A rectangular prop as a tuple of rows, ready for `Canvas.blit`.
recolour_sheet(sheet, out, cells, hues, hue, sat, renames=()) Writes `img/tilesets/<out>.png`, a copy of `<sheet>.png` with some cells
paint_regions(g, tileset_id, value=1, layer=5)       Region-tag every tile the player can actually stand on.
new_map(width, height, tileset, name='', bgm='Town1', bgm_volume=70, encounters=(), encounter_step=30, battleback=None, scroll_type=0, parallax='', disable_dashing=False) A map record with everything the editor expects, and nothing surprising.
interior(width, height, x1, y1, x2, y2, door_x=None, floor=IN_WOOD_FLOOR, floor_alt=None, wall_top=IN_WALL_TOP, wall_face=IN_WALL_FACE, void=IN_VOID, threshold=None, outside=None, tileset=TS_INSIDE) A room in black space, tiled the way the stock interiors are.
door_animation()                                     Open a door sprite, hold, close it, then make it transparent - the
```


## `story` — build/story.py

Shared event-building helpers: how people talk, how doors work, and the

### functions

```
say(speaker, lines, *, face=True, indent=0, position=2) One person saying something, over as many windows as it takes.
narrate(lines, indent=0)                             Screen text with nobody speaking - descriptions, and the narrator.
trope(indent=0)                                      Bump the cliché counter. The ending reads the total back to the player,
blush(indent=0)                                      Bump the count of things nobody quite said.
companion_story(actor_id, indent=0)                  A companion quest is finished: turn on that companion's story switch,
got(lines, indent=0)                                 The 'you found a thing' message, in the colour things are found in.
door_page(target_map, tx, ty, direction=2, se='Open1') The commands behind a door sprite: open it, step through, transfer.
door(event_id, name, x, y, target_map, tx, ty, direction=2, sheet='!Door1', index=0) An outward-facing door on a house wall. Player-touch, because a door
exit_tile(event_id, name, x, y, target_map, tx, ty, direction=2) An invisible way out of an interior - stand on it and you are outside.
sign(event_id, name, x, y, lines, sheet='', index=0) Something you read. No sprite by default - the scenery tile is the
npc(event_id, name, x, y, commands, sheet, index, direction=2, move_type=0, trigger=0, priority=1, step_anime=False, pages=None, move_speed=3, move_frequency=3) A person who says something when you talk to them.
prop(event_id, name, x, y, lines, sheet, index, direction=2, pattern=1, extra=()) A searchable object - a barrel, a bookshelf, a scarecrow.
specimen(event_id, name, x, y, lines, wren_says, again, sheet='', index=0) One of NORTH.md 3.4's three things on the road, for Wren to be correct
chest(event_id, name, x, y, contents, lines)         A treasure chest: page one gives you the thing, page two is empty.
recruit(event_id, actor_id, name, x, y, sheet, index, *, pitch, accept, decline, full, direction=2, move_type=0, extra_pages=(), after=(), again=None) One of the nine.
roster_amendment(companions=None, clerk='Clerk')     A dismissal form. Lets the player swap a companion out without
```

### `FACES` — who already has a face (212)

The key is what `say()` prints as the speaker's name. Adding somebody here is how a new character gets a portrait; sharing an existing sheet and index is normal and the reasons are commented in the module.

```
Bram                  Merribell             Hob                   Zephyrine
Nix                   Aldric                Piper                 Corvin
Wren                  Roland                Gatekeeper            Elder Wispel
Clerk                 Mother                Villager              Gossip
Neighbour             Councillor            Councillor Fenn       Old Man
Farmer                Fisher                Child                 Innkeeper
Merchant              Apprentice            Shopkeeper            Regular
Dorcas                Prudence              Hosea                 Ysolde
Hulda                 Nabb                  Tolly                 Merrow
Dree                  Perpetua              Pell                  Mrs Barrow
Bother                Halbert Quy           Splint                Ferryman
Sops                  Tibb                  Traveller             Also A Traveller
Hermit                Crooke                Ambrose               Grimspite
Ott                   Mrs Tunnicliffe       Mrs Cotterill         Mr Cotterill
Spare                 Sowerby               Nib                   Mr Kell
Bryd                  Winnie                Bessie                Rivet
Gudgeon               Tappet                Ferrule               Grommet
Clevis                Shim                  Fizz                  Norbert
Hollis                Dilys                 Gideon                Dorothy
Mrs Ashbury           Walt                  Dr Pike               Guest
Quillon               Sir Dunstable         King Aldous           Mrs Emberthwaite
Rosamund              Tamsin                Brannoc               Kit
Osric                 Aurel                 Hild                  Morwen
Leof                  Valen                 Mr Budge              Mrs Budge
Mr Pilbeam            Mirabel               Elder Faelan          Elder Lirien
Toby                  Hollowell             Somebody Large        Meech
Mother Selvidge       Dunnock               Miss Privet           Mrs Quickset
Tobias                Perce                 Ida                   Clem
Mrs Blagg             Pargeter              Mrs Marchpane         Mordaunt
Crake                 Morrow                Rook                  Veyle
Blackwood             Mrs Vane              Mr Thurle             Mrs Ash
Mr Weir               Prioress              Sister Bewick         Sister Pim
Sister Lamb           Mrs Liddy             Mr Crouch             Mr Oakes
Sir Hamo              Mr Nuttall            Mr Dace               Watchman
Mrs Poskitt           Mr Plummer            Warden Crabbe         Town Clerk
Mrs Dewhirst          Mr Ambler             Miss Quayle           Mr Tweddle
Dame Winifred         Bess                  Alfie                 Nell
Mr Gammage            Mrs Pardew            Mrs Garrow            Dr Hapgood
Reader                Undergraduate         Ned                   Granny Wendle
Wilf                  Mrs Dimmock           Commissioner          Mrs Puddifoot
Tom                   Elf                   Ivy                   Hodge
Bagshawe              Mrs Lumb              Mr Dunmore            Miss Pellow
Dame Florence         Brother Anselm        Mags                  Pim
Odile                 Old Jory              Hettie                Lord Tobin
Ned                   Saul                  Major Royce           The Fourth
Mr Ottershaw          Mr Gedge              Prewitt               Dean Fenwold
The Mayor             Prime Warden          Mr Tibbs              Mrs Harbottle
Mr Dray               Miss Moon             The Convenor          Fellow Grice
Fellow Amory          Fellow Blunt          Mr Pennock            Professor Mott
Dr Furze              Mother Grizel         Dr Hobday             Nan Gilly
Mr Spence             Ambrosine             Lorrimer              Maud
Miss Fettle           Cotter                Courier               Effie
Mrs Gotobed           Mr Dibble             Mrs Throssell         Mr Cobley
```


## `places` — build/places.py

Map ids and the handful of coordinates that two maps have to agree on.

155 constants.

```
MAP_VILLAGE                  1
MAP_HOME                     2
MAP_HALL                     3
MAP_INN                      4
MAP_CHAPEL                   5
MAP_SMITHY                   6
MAP_STORE                    7
MAP_WORLD                    8
MAP_GLOAMWOOD                9
MAP_GLOAM_DEEP               10
MAP_TOWER                    11
MAP_SUMMIT                   12
MAP_SOPPING                  13
MAP_WYVERN                   14
MAP_GUILD                    15
MAP_OUTFIT                   16
MAP_COTTAGE                  17
MAP_LIGHTHOUSE               18
MAP_PIT                      19
MAP_BARROW                   20
REG_SOUTH                    1
REG_NORTH                    2
REG_COAST                    3
REG_CLANG                    4
REG_SNOW                     5
REG_DESERT                   6
VILLAGE_GATE                 (19, 2)
WORLD_VILLAGE                (60, 79)
WORLD_VILLAGE_STEP           (60, 78)
WORLD_GLOAMWOOD              (52, 62)
WORLD_TOWER                  (66, 43)
SOPPING_GATE                 (20, 2)
WORLD_SOPPING                (71, 84)
WORLD_SOPPING_STEP           (71, 83)
WORLD_LIGHTHOUSE             (79, 80)
WORLD_LIGHTHOUSE_STEP        (78, 80)
WORLD_PIT                    (43, 70)
WORLD_BARROW                 (68, 56)
WORLD_STONES                 (46, 53)
WORLD_HERMIT                 (75, 65)
WORLD_CRAB                   (55, 81)
WORLD_CAMP                   (47, 67)
MAP_CLANGING                 21
MAP_WORKS                    22
MAP_VALVE                    23
MAP_FORGE                    24
MAP_PARISH                   25
MAP_LONG_FIELD               26
MAP_CRAG                     27
CLANGING_GATE                (17, 42)
WORLD_CLANGING               (44, 47)
WORLD_CLANGING_STEP          (44, 48)
WORLD_LONG_FIELD             (47, 50)
WORLD_LONG_FIELD_STEP        (46, 50)
WORLD_CRAG                   (41, 43)
WORLD_CRAG_STEP              (41, 44)
WORLD_JUNCTION               (49, 54)
WORLD_AIRSHIP                (45, 48)
WORLD_ISLE                   (55, 83)
WORLD_ISLE_PAD               (57, 83)
WORLD_STACK                  (37, 40)
WORLD_STACK_PAD              (39, 40)
WORLD_MIDDLE                 (82, 65)
WORLD_MIDDLE_PAD             (83, 66)
MAP_MEADOW                   28
WORLD_MEADOW                 (55, 74)
WORLD_MEADOW_STEP            (56, 74)
MAP_PENULTIMA                29
MAP_SHOPPE                   30
PENULTIMA_STEP               (63, 48)
MAP_RESTWELL                 31
MAP_EIGHT_HOURS              32
RESTWELL_STEP                (42, 81)
MAP_HITHERMOST               33
MAP_CONTINUANCE              34
HITHERMOST_STEP              (30, 24)
MAP_FAIRHOLME                35
MAP_ROSAMUND                 36
MAP_LAIR                     37
FAIRHOLME_STEP               (104, 74)
LAIR_STEP                    (111, 70)
MAP_EVERMORE                 38
MAP_ARCHIVE                  39
EVERMORE_STEP                (30, 94)
MAP_GLADHOLLOW               40
MAP_MAYORS                   41
GLADHOLLOW_STEP              (33, 112)
MAP_PREMISES                 42
PREMISES_LAND                ((79, 88), (80, 88))
PREMISES_STEP                PREMISES_LAND[1]
MAP_FRAYNE                   43
FRAYNE_STEP                  (66, 83)
MAP_FROSTWICK                44
MAP_ELEVEN_DAYS              45
MAP_WORKING_GROUP            46
MAP_COLD_ROOM                47
FROSTWICK_STEP               (61, 22)
MAP_COLDBARROW               48
COLDBARROW_STEP              (50, 20)
MAP_SABLE_HART               49
SABLE_HART_STEP              (24, 76)
MAP_LITTLE_GORE              50
MAP_SUMP                     51
LITTLE_GORE_STEP             (97, 102)
SUMP_STEP                    (78, 103)
MAP_ASHCOMBE                 52
MAP_ASHCOMBE_IN              53
ASHCOMBE_STEP                (102, 56)
MAP_WEEPING_BOTTOM           54
MAP_WARD                     55
WEEPING_BOTTOM_STEP          (58, 100)
MAP_FENMARCH                 56
MAP_GALLERY                  57
FENMARCH_STEP                (86, 115)
MAP_COLLEGIUM                58
MAP_COLLEGIUM_LIBRARY        59
MAP_COLLEGIUM_HALL           60
COLLEGIUM_STEP               (112, 39)
MAP_DUNNAGE                  61
MAP_SMITHS_HALL              62
MAP_COUNTING_HOUSE           63
MAP_BONDED                   64
MAP_BELL                     65
DUNNAGE_STEP                 (31, 53)
WORLD_SIGN_SOUTH             (58, 73)
WORLD_SIGN_NORTH             (64, 46)
WORLD_SIGN_COAST             (63, 80)
FEN_ROAD_SIGN                (33, 53)
FEN_ROAD_END                 (47, 117)
UNDERSTUDY_BELL              (4, 9)
UNDERSTUDY_DOOR              (65, 43)
VAULT                        (23, 5, 25, 7, 24)
VAULT_CHAIR                  (24, 5)
COUNTING_BEFORE_DOOR         (8, 5)
STUDY                        (28, 4, 33, 8, 30)
STUDY_DOOR                   (6, 3)
STUDY_DESK                   (31, 6)
STUDY_MARKS                  (30, 3)
MAP_DROWNED_STREET           66
MAP_CARN_DREY                67
CARN_DREY                    (39, 55)
CARN_DREY_STEP               (40, 55)
SNUG_CARD                    (4, 8)
WYVERN_BACK                  (28, 4, 34, 9, 31)
WYVERN_BACK_DOOR             (15, 3)
WYVERN_BACK_TABLE            (29, 6, 33)
COLDBARROW_MAP_AT_LARGE      'Coldbarrow_Map_AtLarge'
FOURTH_FOLLOWS               ...
ASHCOMBE_LAKE                (104, 54)
LAKE_SHORE_STEP              (104, 55)
MAP_POTTERING                68
MAP_POTTERING_IN             69
POTTERING_STEP               (60, 62)
MAP_CULVERT                  70
CULVERT_STEP                 (33, 20)
```


## `db` — build/db.py

The whole database of The Obligatory Quest.

615 constants.

```
BRAM                         1
MERRI                        2
HOB                          3
ZEPH                         4
NIX                          5
ALDRIC                       6
PIPER                        7
CORVIN                       8
WREN                         9
ROLAND                       10
CLASSES                      ...
SK_ATTACK                    1
SK_GUARD                     2
SK_TURNIP                    10
SK_PLOT_ARMOR                11
SK_SECOND_WIND               12
SK_FRIENDSHIP                13
SK_DESTINED                  14
SK_BEDSIDE                   20
SK_HYDRATION                 21
SK_STERN                     22
SK_GET_UP                    23
SK_REST                      24
SK_HOMILY                    25
SK_ANVIL                     30
SK_PERCUSSIVE                31
SK_FULL_SWING                32
SK_QUENCH                    33
SK_REFORGE                   34
SK_KINDLE                    40
SK_FROSTBITE                 41
SK_STATIC                    42
SK_CONFLAGRATE               43
SK_METEOR                    44
SK_MANA_SIP                  45
SK_BACKSTAB                  50
SK_REALLOCATE                51
SK_TWELVE                    52
SK_VANISH                    53
SK_COUP                      54
SK_INTERPOSE                 60
SK_OATH                      61
SK_CHARGE                    62
SK_RALLY                     63
SK_CHIVALRIC                 64
SK_BALLAD                    70
SK_DISCORD                   71
SK_RECAP                     72
SK_LULLABY                   73
SK_FINALE                    74
SK_FORESHADOW                75
SK_NIBBLE                    90
SK_ROOT_GRAB                 91
SK_SHRIEK                    92
SK_EMBER                     93
SK_DRAIN                     94
SK_DOOM_MONOLOGUE            95
SK_INEVITABILITY             96
SK_CLAUSE_TWELVE             97
SK_ERRATUM                   98
SK_SMALL_PRINT               99
SK_BROOD                     100
SK_BLACK_EDGE                101
SK_OLD_WOUND                 102
SK_OMINOUS                   103
SK_RIVAL                     104
SK_ALL_AT_ONCE               105
SK_SNAP_SHOT                 110
SK_FIELD_NOTES               111
SK_PIN_DOWN                  112
SK_SPECIMEN                  113
SK_VOLLEY                    114
SK_DEFINITIVE                115
SK_GUEST_APPEARANCE          120
SK_ENCOURAGEMENT             121
SK_FLOURISH                  122
SK_PRIOR                     123
SK_PINCH                     130
SK_SWOOP                     131
SK_GRAVE_DUTY                132
SK_WHATS_DONE                133
SK_RUMMAGE                   134
SK_OPINION                   135
SK_TRIBUTE                   136
SK_SCALD                     140
SK_STILL_TRYING              141
SK_SHED_A_PART               142
SK_OVERPRESSURE              143
SK_DUE_NORTH                 144
SK_MAKE_GOOD                 145
IT_POTION                    1
IT_HI_POTION                 2
IT_ETHER                     3
IT_FEATHER                   4
IT_ANTIDOTE                  5
IT_TURNIP                    6
IT_ELIXIR                    7
IT_SMELLING_SALTS            8
IT_TONIC                     9
IT_BISCUIT                   10
IT_CHOWDER                   11
IT_PALE                      12
IT_PROPHECY                  20
IT_TOWER_KEY                 21
IT_RECEIPT                   22
IT_JAR                       23
IT_REPLY                     24
IT_REFERENCE                 25
IT_LAMP_OIL                  26
IT_GUILD_CARD                27
IT_HISTORY                   28
IT_BENCH                     29
IT_DRIPPING                  13
IT_STEWED_TEA                14
IT_LINIMENT                  15
IT_OILSKIN_BOLTS             30
IT_PLATE                     31
IT_ITEM_ONE                  32
WP_HOE                       1
WP_SWORD                     2
WP_BROADSWORD                3
WP_DESTINY                   4
WP_CENSER                    5
WP_STAFF                     6
WP_HOLY_ROD                  7
WP_HAMMER                    8
WP_SLEDGE                    9
WP_WORLDBREAKER              10
WP_TWIG                      11
WP_WAND                      12
WP_STARFALL                  13
WP_KNIFE                     14
WP_DIRK                      15
WP_LAST_WORD                 16
WP_LANCE                     17
WP_HALBERD                   18
WP_OATHKEEPER                19
WP_LUTE                      20
WP_FIDDLE                    21
WP_LEGEND                    22
WP_NOTCHED                   23
WP_GRUDGE                    24
WP_FORETOLD                  25
WP_CROSSBOW                  26
WP_RECURVE                   27
WP_CITATION                  28
WP_PRACTICE                  29
WP_FAIRWEATHER               30
WP_FORTY_FOURTH              31
WP_WRENCH                    32
WP_NUMBER_ONE                33
AR_SMOCK                     1
AR_LEATHER                   2
AR_CHAIN                     3
AR_PLATE                     4
AR_ROBE                      5
AR_SILK                      6
AR_BUCKLER                   7
AR_KITE_SHIELD               8
AR_HAT                       9
AR_HELM                      10
AR_CIRCLET                   11
AR_RING_LUCK                 12
AR_RING_SPEED                13
AR_AMULET                    14
AR_BOOTS                     15
AR_OILSKIN                   16
AR_A_HAT                     17
AR_LAMP                      18
AR_LOCKET                    19
AR_FOOTNOTE                  20
AR_SIGNET                    21
AR_KIT                       22
AR_TROUSERS                  23
AR_WORKS_CAP                 24
AR_FUSE                      25
AR_GOVERNOR                  26
EN_TURNIP                    1
EN_CROW                      2
EN_GOBLIN                    3
EN_BANDIT                    4
EN_TREANT                    5
EN_WISP                      6
EN_SKELETON                  7
EN_GARGOYLE                  8
EN_MIMIC                     9
EN_BAT                       10
EN_SLIME_ISH                 11
EN_CRAB                      12
EN_GULL                      13
EN_SANDTHING                 14
EN_OCCUPANT                  15
EN_LOST_PROPERTY             16
EN_HOUND                     17
EN_GRAVE_GOODS               18
EN_THING                     20
EN_GRIMSPITE                 21
EN_PROPHECY                  22
EN_BADGER                    23
EN_BIG_CRAB                  24
EN_CROOKE                    25
EN_FORTY_FOURTH              26
EN_84                        27
EN_PRESSURE                  30
EN_UNNUMBERED                31
EN_SALVAGE                   32
TR_TURNIPS                   1
TR_CROWS                     2
TR_GOBLINS                   3
TR_BANDITS                   4
TR_WOOD_MIX                  5
TR_WISPS                     6
TR_TOWER_MIX                 7
TR_SKELETONS                 8
TR_GARGOYLES                 9
TR_FIELD_MIX                 10
TR_CRABS                     11
TR_GULLS                     12
TR_COAST_MIX                 13
TR_PIT_MIX                   14
TR_BARROW_MIX                15
TR_WRAITHS                   16
TR_GRAVE_GOODS               17
TR_THING                     20
TR_MIMIC                     21
TR_GRIMSPITE                 22
TR_PROPHECY                  23
TR_BADGER                    24
TR_BIG_CRAB                  25
TR_CROOKE                    26
TR_FORTY_FOURTH              27
TR_84                        28
TR_PRESSURE                  30
TR_UNNUMBERED                31
TR_SALVAGE                   32
TR_CRAG_MIX                  33
ST_DEAD                      1
ST_SLEEP                     10
ST_POISON                    4
ST_INTERPOSING               31
ST_INSPIRED                  32
ST_NARRATED                  33
ST_BROODING                  34
ST_CATALOGUED                35
ST_SLOWED                    36
CE_STEAL_GOLD                1
CE_TURNIP_EATEN              2
CE_FIT_TO_TRAVEL             3
SW_QUEST                     1
SW_LEFT_VILLAGE              2
SW_GLOAMWOOD                 3
SW_GRIMSPITE                 4
SW_WON                       5
SW_TOWER_OPEN                6
SW_RECRUIT                   ...
SW_MIMIC                     20
SW_ROLAND_GONE               21
SW_FEUD_JAR                  22
SW_FEUD_REPLY                23
SW_FEUD_DONE                 24
SW_GUILD_ASKED               25
SW_GUILD_FORM                26
SW_GUILD_MEMBER              27
SW_BOUNTY_CRAB               28
SW_BOUNTY_CROOKE             29
SW_CRAB_PAID                 30
SW_CROOKE_PAID               31
SW_LAMP_ASKED                32
SW_LAMP_LIT                  33
SW_PIT_ASKED                 34
SW_PIT_CLEARED               35
SW_PIT_PAID                  36
SW_BARROW_OPEN               37
SW_BARROW_BEATEN             38
SW_BENCH_ASKED               39
SW_BENCH_DONE                40
SW_HISTORY_ASKED             41
SW_HISTORY_DONE              42
SW_MET_QUY                   43
SW_MET_46                    44
SW_SOUTH                     45
SW_WYVERN                    46
SW_NORTH                     47
SW_TWO_HUNDRED_ASKED         48
SW_OILSKIN_ASKED             49
SW_OILSKIN_GOT               50
SW_SPAR_ASKED                51
SW_SPAR_DONE                 52
SW_AIRSHIP                   53
SW_ITEM_ONE_ASKED            54
SW_ITEM_ONE_DOWN             55
SW_84_BEATEN                 56
SW_84_REBUILT                57
SW_HOB_BRYD                  58
SW_BALLAD_ASKED              59
SW_BALLAD_DONE               60
SW_CENSUS                    61
SW_COTTERILL                 62
SW_SPARE_ASKED               63
SW_LONG_FIELD                64
SW_CLAUSE_SEVEN              65
SW_ROOM_FOUR                 66
SW_GERALD                    67
SW_TWO_HUNDRED_FLEW          68
SW_TRAVELLERS                69
SW_OTT_MATERIALS             70
SW_ITEM_ONE_USED             71
SW_KNOWN                     ...
VAR_COMPANIONS               1
VAR_TROPES                   2
VAR_TURNIPS                  3
VAR_TALES                    4
VAR_BOUNTIES                 5
VAR_PLAQUES                  6
VAR_BLUSHES                  7
VAR_OTT_ORDER                8
VAR_OTT_FLYING               9
SW_FF_ARRIVED                81
SW_FF_STICK                  82
SW_FF_SHEEP_ASKED            83
SW_FF_SHEEP_DONE             84
SW_FF_CHEST                  85
SW_FF_NORBERT                86
SW_FF_GRADUATED              87
VAR_FF_STATIONS              11
VAR_FF_SHEEP                 12
VAR_FF_SIGNS                 13
VAR_TOBY                     14
SW_VISITORS_BOOK             88
SW_STORY                     ...
VAR_COMPANION_STORIES        15
SW_WRE2_ASKED                111
SW_WRE2_UP                   112
IT_BRASS_PLATE               40
SW_WRE5_NAMED                113
SW_PIP2_DONE                 114
SW_MER2_ASKED                115
SW_MER2_SCALES               116
SW_MER2_DONE                 117
VAR_MER2_WITNESS             16
IT_FITNESS_FORM              41
IT_SCALES                    42
IT_CERTIFICATE               43
SW_ROL4_SEEN                 118
SW_ROL4_REFIT                119
WP_REHAFTED                  40
SW_HOB5_FORGED               120
SW_HOB5_DONE                 121
IT_TUBE_PLATE                44
SW_ZEPH5_DONE                122
SK_PAGE_23                   46
SW_MER4_TOLD                 123
SW_MER4_DONE                 124
SW_HOB3_GONE                 125
SW_HOB3_DONE                 126
IT_APOLOGY                   45
SW_NIX4_BEGUN                127
SW_NIX4_DONE                 128
VAR_NIX4_RETURNED            17
IT_RETURNS                   46
IT_PARCEL                    47
SW_NIX5_ON                   129
SW_NIX5_DONE                 130
VAR_NIX5_BATTLES             18
SW_WRE3_WALK                 131
SW_WRE3_DONE                 132
AR_SOCIETY_BADGE             40
AT_BADGE                     7
SW_PIP5_ASKED                133
SW_PIP5_SIGNED               134
SW_PIP5_KEY                  135
SW_PIP5_DONE                 136
VAR_PIP5_DECOY               19
IT_FORM_S7                   48
IT_ARCHIVE_KEY               49
SW_HOB2_ON                   137
SW_HOB2_CARRYING             138
SW_HOB2_DONE                 139
VAR_HOB2_TRY                 20
WP_SOMETHING_TO_SAY          41
SW_ROL3_DINNER               140
SW_ROL3_DONE                 141
VAR_ROL3_HEARD               21
SW_HOB1_ON                   142
SW_HOB1_PICKS                143
SW_HOB1_DONE                 144
VAR_HOB1_ASKED               22
IT_WARDENS_NOTES             50
SW_ALD4_DONE                 145
SW_PIP3_ON                   146
SW_PIP3_DONE                 147
AR_ROSETTE                   41
AT_ROSETTE                   8
EN_DRAY                      41
EN_MOON                      42
EN_BACK_TABLE                43
TR_CONTEST                   41
SK_HECKLE                    170
SK_TALK_THROUGH              171
SK_SERPENT                   172
SK_SAD_VERSE                 173
SK_ENCORE                    174
SW_COR5_DONE                 148
ST_CURSED                    40
SW_NIX1_LETTER               149
SW_NIX1_DONE                 150
IT_BOND_TICKET               51
AR_GRANS_COAT                42
AT_COAT                      9
SW_NIX2_OPEN                 151
SW_NIX2_DONE                 152
SW_ROL1_ON                   153
SW_ROL1_DONE                 154
IT_MINUTES                   52
SW_ZEPH1_ON                  155
SW_ZEPH1_TOLD                156
SW_ZEPH1_PAID                157
SW_ZEPH1_EXPELLED            158
SW_ZEPH1_DONE                159
VAR_ZEPH1_PAID               23
IT_FINES_NOTICE              53
AR_COLLEGIUM_ROBE            43
AT_ROBE                      10
SW_ZEPH3_DONE                160
SW_ZEPH2_ON                  161
SW_ZEPH2_WALKING             162
SW_ZEPH2_DONE                163
IT_DUCK                      54
IT_PROXY                     55
SW_WRE1_ON                   164
SW_WRE1_MOTT                 165
SW_WRE1_FURZE                166
SW_WRE1_DUCK_DUE             167
SW_WRE1_DUCK                 168
SW_WRE1_DONE                 169
VAR_WRE1_SPECIMENS           24
IT_SUBSCRIPTIONS             list(range(56, 64))
IT_MONOGRAPH                 64
CL_WREN_PUBLISHED            11
EN_SPECIMENS                 list(range(44, 55))
TR_SPECIMENS                 list(range(42, 53))
SK_STARTLE                   175
SK_BOLT                      176
SK_BITE_NOTES                177
SK_NOT_THERE                 178
SW_COR1_ON                   170
SW_COR1_HOME                 171
SW_COR1_DONE                 172
IT_INVITATION                65
AR_SCARF                     44
AT_SCARF                     11
SW_COR2_STEP                 173
SW_COR2_DONE                 174
IT_REPORT_CARD               66
SW_MER5_ON                   175
SW_MER5_DONE                 176
IT_JAM                       67
SW_MER1_ON                   177
SW_MER1_DONE                 178
VAR_MER1_POINTS              25
AR_PAMPHLET                  45
AT_PAMPHLET                  12
SW_MER3_ON                   179
SW_MER3_DONE                 180
AR_TABLE_KIT                 46
SW_ALD3_DONE                 181
SW_ALD1_DONE                 182
IT_ALD1_LETTER               68
SW_ALD5_DONE                 183
SW_ALD2_DONE                 184
AR_REGARDANT                 47
AT_ESCUTCHEON                13
ST_VIGIL                     41
EN_DAMP                      55
EN_SMALL_HOURS               56
EN_TEMPTATION                57
EN_LIGHT                     58
TR_VIGIL                     53
SK_SEEPS_IN                  179
SK_SIT_DOWN                  180
SK_HOW_LATE                  181
SK_THIS_WAY                  182
VIGIL_DAWN                   5
SW_ALD6_DONE                 185
SW_WRE4_ON                   186
SW_WRE4_JOINS                187
SW_WRE4_DONE                 188
WRE4_FEE                     600
SW_COR3_ON                   189
SW_COR3_DONE                 190
SW_COR4_DONE                 191
SW_PIP4_ON                   192
SW_PIP4_DONE                 193
VAR_PIP4_HEARD               26
IT_ELEGY                     69
SW_PIP1_ON                   194
SW_PIP1_GOOD                 195
SW_PIP1_FIXED                196
SW_PIP1_DONE                 197
IT_AUTHORISED                70
SW_NIX3_ON                   198
SW_NIX3_DONE                 199
VAR_NIX3_LOCATED             27
AR_LORRIMER_TOOLS            48
SW_HOB4_TRADED               200
SW_HOB4_DONE                 201
IT_STAR_IRON                 71
WP_STAR_IRON                 42
SW_ZEPH4_DONE                202
IT_FEN_CERTIFICATE           72
SW_ROL5_ON                   203
SW_ROL5_DONE                 204
SW_ROL2_ON                   205
SW_ROL2_DRAWN                206
SW_ROL2_DONE                 207
WP_DRAWN                     43
EN_WORM                      59
TR_WORM                      54
SK_COILS                     183
SK_LOOKS_AT_HIM              184
SPARE                        11
SW_SPARE_FORM                89
SW_SPARE_JOINED              90
SW_SPARE_REFUSED             91
SW_SPARE_KNOWN               92
SW_SPARE_STORY               110
IT_FORM_P9                   33
IT_WASHER                    34
WP_BAG                       34
AR_WASHER                    27
WT_BAG                       13
AT_WASHER                    14
SK_YOU_ARE_NINE              146
SK_ASK_YOUR_FATHER           147
SK_NOT_THE_POINT             148
SK_SAID_NO                   149
SK_SMALL_ENOUGH              150
SK_TANTRUM                   151
SK_HAVE_A_BAG                152
SK_NEVER_HIT_ME              153
SK_NINETY_TUBES              154
SK_THE_DRAWING               155
ST_NEVER_HIT                 42
ST_BRUSHED                   43
EN_MAM                       28
TR_MAM                       29
CE_TANTRUM                   4
SW_SPA1_DONE                 208
SW_SPA1_DINNER               209
VAR_SPA1_POSTED              28
VAR_SPA1_ORDER               29
IT_SPA1_COPIES               73
CE_SPA1_COPIES               5
SW_SPA4_DONE                 210
VAR_SPA4_TOUR                30
SW_SPA2_ASKED                211
SW_SPA2_CLEARED              212
SW_SPA2_DONE                 213
VAR_SPA2_PARTY               31
IT_MOTHBALLS                 74
ST_MOTHBALLS                 44
CE_MOTHBALLS                 6
VAR_MOTHBALLS                32
MOTHBALL_STEPS               50
MOTHBALL_AIRING              25
SPARE_ARGUING_LEVEL          12
AR_STICK                     30
AR_STRAIGHTER_STICK          31
AR_CERTIFICATE               32
SK_TELEGRAPH                 160
SK_ENORMOUS_SWING            161
EN_NORBERT                   40
TR_NORBERT                   40
EL_PHYSICAL                  1
EL_FIRE                      2
EL_ICE                       3
EL_THUNDER                   4
EL_WATER                     5
EL_EARTH                     6
EL_WIND                      7
EL_LIGHT                     8
EL_DARK                      9
EL_TEMPER                    10
STYPE_MAGIC                  1
STYPE_SPECIAL                2
ET_WEAPON                    1
ET_SHIELD                    2
ET_HEAD                      3
ET_BODY                      4
ET_ACCESSORY                 5
AT_GENERAL                   1
AT_MAGIC                     2
AT_LIGHT                     3
AT_HEAVY                     4
AT_SMALL_SHIELD              5
AT_LARGE_SHIELD              6
WT_DAGGER                    1
WT_SWORD                     2
WT_FLAIL                     3
WT_AXE                       4
WT_WHIP                      5
WT_STAFF                     6
WT_BOW                       7
WT_CROSSBOW                  8
WT_GUN                       9
WT_CLAW                      10
WT_GLOVE                     11
WT_SPEAR                     12
BLANKS                       ...
NO_DROP                      drop()
BLANK_TROOP_CONDITIONS       ...
SPECIMENS                    ...
SUBSCRIBERS                  ...
SUBSCRIPTION_PRICE           150
SUBSCRIBERS_NEEDED           6
```
