"""Builds the whole of The Obligatory Quest from scratch.

    python3 build/build_game.py

Re-runnable: every record is written at its own id, so running it again
rewrites the game rather than piling up duplicates. This, and the modules it
calls, is the only place the game's content is authored - `data/*.json` is
output, not source.
"""
import copy
import os
import sys

GAME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GAME, "build"))

import mapkit  # noqa: E402  puts the workspace's tools/ on the path
import rmmzdata as R  # noqa: E402

R.use_project(GAME)

import db  # noqa: E402
import field  # noqa: E402
import meadow  # noqa: E402
import journey  # noqa: E402
import north  # noqa: E402
import penultima  # noqa: E402
import restwell  # noqa: E402
import hithermost  # noqa: E402
import fairholme  # noqa: E402
import evermore  # noqa: E402
import gladhollow  # noqa: E402
import premises  # noqa: E402
import frayne  # noqa: E402
import frostwick  # noqa: E402
import coldbarrow  # noqa: E402
import sable_hart  # noqa: E402
import hamlets  # noqa: E402
import ashcombe  # noqa: E402
import weeping_bottom  # noqa: E402
import fenmarch  # noqa: E402
import collegium  # noqa: E402
import dunnage  # noqa: E402
import pottering  # noqa: E402
import nomap  # noqa: E402,F401  world-map events only; journey reads SITES
import places  # noqa: E402
import q_corvin  # noqa: E402  draws COR-2's drowned street, Map 66
import q_roland  # noqa: E402  draws ROL-2's dungeon, Map 67
import q_spare  # noqa: E402  checks F1's gate against the built town
import south  # noqa: E402
import village  # noqa: E402
import wilds  # noqa: E402


MAP_NAMES = [
    (village.MAP_VILLAGE, "Thistlewick", 0),
    (village.MAP_HOME, "Bram's House", village.MAP_VILLAGE),
    (village.MAP_HALL, "Prophecy Hall", village.MAP_VILLAGE),
    (village.MAP_INN, "The Gilded Turnip", village.MAP_VILLAGE),
    (village.MAP_CHAPEL, "Chapel of Whatever Works", village.MAP_VILLAGE),
    (village.MAP_SMITHY, "Grumnir's Smithy", village.MAP_VILLAGE),
    (village.MAP_STORE, "Nix's Emporium", village.MAP_VILLAGE),
    (journey.MAP_WORLD, "The World, Roughly", 0),
    (journey.MAP_GLOAMWOOD, "The Gloamwood", journey.MAP_WORLD),
    (journey.MAP_GLOAM_DEEP, "Gloamwood - The Bit With The Thing", journey.MAP_WORLD),
    (journey.MAP_TOWER, "The Obligatory Tower", journey.MAP_WORLD),
    (journey.MAP_SUMMIT, "The Obligatory Tower - Summit", journey.MAP_WORLD),
    (south.MAP_SOPPING, "Nether Sopping", 0),
    (south.MAP_WYVERN, "The Slain Wyvern", south.MAP_SOPPING),
    (south.MAP_GUILD, "The Adventurers' Guild (Provisional)",
     south.MAP_SOPPING),
    (south.MAP_OUTFIT, "Wick & Barrow, Outfitters", south.MAP_SOPPING),
    (south.MAP_COTTAGE, "Number Forty-Five's Cottage", south.MAP_SOPPING),
    (south.MAP_LIGHTHOUSE, "The Lighthouse of Saint Bother", journey.MAP_WORLD),
    (wilds.MAP_PIT, "The Bottomless Pit", journey.MAP_WORLD),
    (wilds.MAP_BARROW, "The Barrow of the Forty-Fourth", journey.MAP_WORLD),
    (north.MAP_CLANGING, "Upper Clanging", 0),
    (north.MAP_WORKS, "The Hoyle Works", north.MAP_CLANGING),
    (north.MAP_VALVE, "The Safety Valve", north.MAP_CLANGING),
    (north.MAP_FORGE, "Ollerenshaw's", north.MAP_CLANGING),
    (north.MAP_PARISH, "The Parish Rooms", north.MAP_CLANGING),
    (field.MAP_LONG_FIELD, "The Long Field", journey.MAP_WORLD),
    (field.MAP_CRAG, "The Wreck of the One Hundred and Ninety-Ninth",
     journey.MAP_WORLD),
    (meadow.MAP_MEADOW, "Firstfield Meadow", journey.MAP_WORLD),
    (penultima.MAP_PENULTIMA, "Penultima", journey.MAP_WORLD),
    (penultima.MAP_SHOPPE, "Ye Final Shoppe",
     penultima.MAP_PENULTIMA),
    (restwell.MAP_RESTWELL, "Restwell", journey.MAP_WORLD),
    (restwell.MAP_EIGHT_HOURS, "The Eight Hours", restwell.MAP_RESTWELL),
    (hithermost.MAP_HITHERMOST, "Hithermost", journey.MAP_WORLD),
    (hithermost.MAP_CONTINUANCE, "Chapel of Continuance",
     hithermost.MAP_HITHERMOST),
    (fairholme.MAP_FAIRHOLME, "Fairholme", journey.MAP_WORLD),
    (fairholme.MAP_ROSAMUND, "Rosamund's Tower", fairholme.MAP_FAIRHOLME),
    (fairholme.MAP_LAIR, "Mrs Emberthwaite's Lair", journey.MAP_WORLD),
    (evermore.MAP_EVERMORE, "Olde Evermore", journey.MAP_WORLD),
    (evermore.MAP_ARCHIVE, "The Forbidden Archive", evermore.MAP_EVERMORE),
    (gladhollow.MAP_GLADHOLLOW, "Gladhollow", journey.MAP_WORLD),
    (gladhollow.MAP_MAYORS, "The Mayor's House", gladhollow.MAP_GLADHOLLOW),
    (premises.MAP_PREMISES, "The Former Premises", journey.MAP_WORLD),
    (frayne.MAP_FRAYNE, "Tobias Frayne's Cottage", journey.MAP_WORLD),
    (frostwick.MAP_FROSTWICK, "Frostwick", journey.MAP_WORLD),
    (frostwick.MAP_ELEVEN_DAYS, "The Eleven Days", frostwick.MAP_FROSTWICK),
    (frostwick.MAP_WORKING_GROUP, "The Working Group",
     frostwick.MAP_FROSTWICK),
    (frostwick.MAP_COLD_ROOM, "The Cold Room", frostwick.MAP_FROSTWICK),
    (coldbarrow.MAP_COLDBARROW, "The Chapter House", journey.MAP_WORLD),
    (sable_hart.MAP_SABLE_HART, "The Sable Hart", journey.MAP_WORLD),
    (hamlets.MAP_LITTLE_GORE, "Little Gore", journey.MAP_WORLD),
    (hamlets.MAP_SUMP, "Sump", journey.MAP_WORLD),
    (ashcombe.MAP_ASHCOMBE, "Ashcombe", journey.MAP_WORLD),
    (ashcombe.MAP_ASHCOMBE_IN, "Ashcombe, Indoors", ashcombe.MAP_ASHCOMBE),
    (weeping_bottom.MAP_WEEPING_BOTTOM, "Weeping Bottom", journey.MAP_WORLD),
    (weeping_bottom.MAP_WARD, "The Sisterhouse",
     weeping_bottom.MAP_WEEPING_BOTTOM),
    (fenmarch.MAP_FENMARCH, "Fenmarch Hall", journey.MAP_WORLD),
    (fenmarch.MAP_GALLERY, "The Long Gallery", fenmarch.MAP_FENMARCH),
    (collegium.MAP_COLLEGIUM, "The Great Court", journey.MAP_WORLD),
    (collegium.MAP_COLLEGIUM_LIBRARY, "The Library", collegium.MAP_COLLEGIUM),
    (collegium.MAP_COLLEGIUM_HALL, "The Hall", collegium.MAP_COLLEGIUM),
    (dunnage.MAP_DUNNAGE, "Great Dunnage", journey.MAP_WORLD),
    (dunnage.MAP_SMITHS_HALL, "The Smiths' Hall", dunnage.MAP_DUNNAGE),
    (dunnage.MAP_COUNTING_HOUSE, "The Counting House", dunnage.MAP_DUNNAGE),
    (dunnage.MAP_BONDED, "The Bonded Warehouse", dunnage.MAP_DUNNAGE),
    (dunnage.MAP_BELL, "The Bell", dunnage.MAP_DUNNAGE),
    (places.MAP_DROWNED_STREET, "Old Ashcombe", journey.MAP_WORLD),
    (places.MAP_CARN_DREY, "Under Carn Drey", journey.MAP_WORLD),
    (places.MAP_POTTERING, "Much Pottering", journey.MAP_WORLD),
    (places.MAP_POTTERING_IN, "The Gotobeds' Cottage", places.MAP_POTTERING),
    (places.MAP_CULVERT, "The Bottom Lock", dunnage.MAP_DUNNAGE),
]


def build_map_infos():
    """Writes the map list, and drops anything not on it.

    Throwaway maps - the tile sampler, mostly - are written straight into
    `data/` while working, and would otherwise ship with the game. The build
    owns the map list, so it deletes any map it did not author."""
    infos = R.load("MapInfos.json")
    for order, (map_id, name, parent) in enumerate(MAP_NAMES, start=1):
        while len(infos) <= map_id:
            infos.append(None)
        infos[map_id] = {"id": map_id, "expanded": True, "name": name,
                         "order": order, "parentId": parent,
                         "scrollX": 0, "scrollY": 0}

    ours = {map_id for map_id, _, _ in MAP_NAMES}
    for map_id, info in enumerate(infos):
        if not info or map_id in ours:
            continue
        infos[map_id] = None
        stray = os.path.join(GAME, "data", "Map%03d.json" % map_id)
        if os.path.exists(stray):
            os.remove(stray)
            print("  dropped stray %s (%s)" % (os.path.basename(stray),
                                               info["name"]))
    while len(infos) > 1 and infos[-1] is None:
        infos.pop()
    R.save_list("MapInfos.json", infos)


# The one number that makes clause seven a rule of the engine rather than a
# line of dialogue. See NORTH.md 5.2, which was verified against the built
# data before this was written.
#
# `Game_Map.isAirshipLandOk` is `checkPassage(x, y, 0x0800) && checkPassage(x,
# y, 0x0f)`, and `checkPassage` reads the layers top down, skips star tiles,
# and **returns on the first tile it does not skip**. The Obligatory Tower's
# door is a B-sheet tile on layer 3 of Map 8 at (31, 8): tile 88, flagged
# 0x0600, which does not set 0x0800 - so it is consulted before the impassable
# castle wall underneath it, and it says yes. As the blank project ships it,
# **the airship can land on the front step of the tower.**
#
# Tile 88 is used exactly once in the whole 50x50 world map and Map 8 is the
# only map on tileset 1, so this is surgical. The approach tiles cannot be
# done and do not need doing: they are plain world grass, which is *the*
# landable ground for the entire island, and the road beside them already
# carries 0x0800 in its own flags. So the Two Hundred sets down on the grass
# two squares short and the party walks in, which is clause seven, enforced by
# the collision map.
TILESET_FLAGS = {
    1: {88: 0x0800},            # Overworld: the Obligatory Tower's door tile
}


# The tilesets whose A4 sheet is the walls of a room. On the outdoor ones A4
# is roofs and town walls, placed with deliberate shapes, so they are left out.
INTERIOR_TILESETS = {mapkit.TS_INSIDE, mapkit.TS_DUNGEON, mapkit.TS_CLANGING_IN}


def shape_wall_tops():
    """Gives every interior's wall tops their edge shapes. Runs after every
    module, so it is the one place it happens.

    `mapkit.interior()` writes the ring round a room as `A(98)` - the A4
    wall-top autotile in shape 0, the middle of a solid block of wall - and
    no room builder re-shapes layer 0, because autotiling all of it would
    outline every square of a two-tone floor. Shape 0 is `0xe00` and blocks
    nothing; it is the edge shapes that carry the direction bit for their
    edge, so a ring left in shape 0 is a ring the player can walk round the
    top of. Only the A4 wall-top kinds are re-shaped: the faces already are,
    and the floor is not touched. Maps built another way are unchanged by
    it, because their tops are already in the shapes this computes."""
    for map_id, _, _ in MAP_NAMES:
        m = R.load_map(map_id)
        if m["tilesetId"] not in INTERIOR_TILESETS:
            continue
        w, h = m["width"], m["height"]
        kinds = {R.autotile_kind(t) for t in m["data"][:w * h]
                 if t >= R.TILE_ID_A4 and not R.is_wall_autotile(t)}
        if not kinds:
            continue
        g = R.MapGrid(w, h, list(m["data"]))
        g.autotile(0, kinds=kinds)
        if g.data != m["data"]:
            m["data"] = g.data
            R.save_map(map_id, m)


def build_tilesets():
    """`Tilesets.json` is the one data file this game inherits rather than
    authors, so the edits it needs are written here, by id, and OR-ed in - the
    build stays re-runnable and the diff stays one number wide."""
    tilesets = R.load("Tilesets.json")
    for tid, flags in TILESET_FLAGS.items():
        for tile_id, bits in flags.items():
            tilesets[tid]["flags"][tile_id] |= bits
    # SF Inside has no D or E sheet, and no anvil, hearth or coal anywhere on
    # the two it has - so Ollerenshaw's was a forge with a marble mantelpiece
    # in it. The stock Inside_B and Inside_C go into those empty slots with
    # tileset 3's flags for them, which changes nothing any existing map has
    # drawn; `mapkit.borrowed` names a tile on them.
    # Outside (tileset 2) takes `Inside_C` into its E slot the same way, for
    # the smithy's anvil out on the grass (HOB-3), so an `Inside_C` tile has
    # the same E id on both and `mapkit.borrowed` serves either. This runs
    # before the copies below, so the Collegium's copy of 2 has it too, on
    # the first build as on every other.
    inside = tilesets[mapkit.TS_INSIDE]
    for tid, slot, sheet, src, dst in (
            (mapkit.TS_CLANGING_IN, 7, "Inside_B", R.TILE_ID_B, R.TILE_ID_D),
            (mapkit.TS_CLANGING_IN, 8, "Inside_C", R.TILE_ID_C, R.TILE_ID_E),
            (mapkit.TS_OUTSIDE, 8, "Inside_C", R.TILE_ID_C, R.TILE_ID_E)):
        tilesets[tid]["tilesetNames"][slot] = sheet
        tilesets[tid]["flags"][dst:dst + 256] = inside["flags"][src:src + 256]
    # Two copies of stock tilesets with one sheet swapped for a recoloured
    # one, rewritten whole each build after the flags above, so the flags
    # follow: the Collegium's purple roofs (`mapkit.TS_COLLEGIUM`) and the
    # world map with Fenmarch Hall's green ones (`mapkit.TS_OVERWORLD`).
    for tid, base, name, slot, sheet in [
            (mapkit.TS_COLLEGIUM, mapkit.TS_OUTSIDE, "Outside (Collegium)",
             6, "Outside_C_Collegium"),
            (mapkit.TS_OVERWORLD, mapkit.TS_WORLD, "Overworld (Thistlewick)",
             5, "World_B_Fenmarch")]:
        ts = copy.deepcopy(tilesets[base])
        ts.update(id=tid, name=name)
        ts["tilesetNames"][slot] = sheet
        tilesets[tid:tid + 1] = [ts]
    # Mike's floating island (P2; `worldmap/run_finish.ISLAND`), on the world
    # map's own copy only, so after the copy. The castle row, 240-241, is
    # ground: open and not a star, so the party stands on it and an airship
    # lands on it. The shadow row, 250-251, is drawn on the sea and was open
    # and not a star on the stock sheet - two cells of water a party could
    # set down on and walk about - so it becomes a star, and the sea decides.
    flags = tilesets[mapkit.TS_OVERWORLD]["flags"]
    for tile_id in (240, 241):
        flags[tile_id] &= ~0x10
    for tile_id in (250, 251):
        flags[tile_id] |= 0x10
    R.save_list("Tilesets.json", tilesets)


def build_system():
    system = R.load("System.json")

    # 251: QUESTS.md 0.6 reserves up to 250 for the companion quests.
    switches = [""] * 251
    for sid, name in [
            (db.SW_QUEST, "quest accepted"),
            (db.SW_LEFT_VILLAGE, "left the village"),
            (db.SW_GLOAMWOOD, "Gloamwood cleared"),
            (db.SW_GRIMSPITE, "Grimspite defeated"),
            (db.SW_WON, "the Prophecy annulled"),
            (db.SW_TOWER_OPEN, "tower door unbarred"),
            (db.SW_MIMIC, "met the mimic"),
            (db.SW_ROLAND_GONE, "the guest star had a prior engagement"),
            (db.SW_FEUD_JAR, "carrying the jar south"),
            (db.SW_FEUD_REPLY, "carrying the reply north"),
            (db.SW_FEUD_DONE, "the Thrupp sisters are speaking"),
            (db.SW_GUILD_ASKED, "Pell has explained Form A-1"),
            (db.SW_GUILD_FORM, "Form A-1 was under the mat"),
            (db.SW_GUILD_MEMBER, "registered adventurer"),
            (db.SW_BOUNTY_CRAB, "the crab is dealt with"),
            (db.SW_BOUNTY_CROOKE, "Crooke is dealt with"),
            (db.SW_CRAB_PAID, "crab bounty claimed"),
            (db.SW_CROOKE_PAID, "Crooke bounty claimed"),
            (db.SW_LAMP_ASKED, "Bother has asked for oil"),
            (db.SW_LAMP_LIT, "the lighthouse is lit"),
            (db.SW_PIT_ASKED, "Splint has explained the badger"),
            (db.SW_PIT_CLEARED, "the badger has left"),
            (db.SW_PIT_PAID, "Splint has paid up"),
            (db.SW_BARROW_OPEN, "the barrow has been entered"),
            (db.SW_BARROW_BEATEN, "the Forty-Fourth has stopped"),
            (db.SW_BENCH_ASKED, "he asked for a bench"),
            (db.SW_BENCH_DONE, "there is a bench on the mound"),
            (db.SW_HISTORY_ASKED, "Hosea wants six tales"),
            (db.SW_HISTORY_DONE, "the history is complete"),
            (db.SW_MET_QUY, "#45 said what to ask"),
            (db.SW_MET_46, "met #46 on his log"),
            (db.SW_SOUTH, "has been to Nether Sopping"),
            (db.SW_WYVERN, "knows about the goose"),
            (db.SW_NORTH, "has been to Upper Clanging"),
            (db.SW_TWO_HUNDRED_ASKED, "Ott has said what she needs"),
            (db.SW_OILSKIN_ASKED, "Ott wants forty bolts of oilskin"),
            (db.SW_OILSKIN_GOT, "the oilskin is bought"),
            (db.SW_SPAR_ASKED, "the main spar wants forging"),
            (db.SW_SPAR_DONE, "the main spar is forged"),
            (db.SW_AIRSHIP, "the Two Hundred flies"),
            (db.SW_ITEM_ONE_ASKED, "Ott has mentioned ITEM 1"),
            (db.SW_ITEM_ONE_DOWN, "ITEM 1 is off the crag"),
            (db.SW_84_BEATEN, "Attempt Eighty-Four has stopped"),
            (db.SW_84_REBUILT, "Attempt Eighty-Four is being rebuilt"),
            (db.SW_HOB_BRYD, "they went for a drink"),
            (db.SW_BALLAD_ASKED, "(unused - reserved, see NORTH.md 10)"),
            (db.SW_BALLAD_DONE, "verse seven was struck"),
            (db.SW_CENSUS, "heard about the Cold Winter"),
            (db.SW_COTTERILL, "met the Cotterills"),
            (db.SW_SPARE_ASKED, "Spare has applied to come along"),
            (db.SW_LONG_FIELD, "walked the Long Field"),
            (db.SW_CLAUSE_SEVEN, "Ott showed you clause seven"),
            (db.SW_ROOM_FOUR, "room four has not been down since Tuesday"),
            (db.SW_GERALD, "there was a Gerald"),
            (db.SW_TWO_HUNDRED_FLEW, "the Two Hundred set down by the tower"),
            (db.SW_TRAVELLERS, "the travellers said how long, exactly"),
            (db.SW_OTT_MATERIALS, "Ott asked you to ask about materials"),
            (db.SW_ITEM_ONE_USED, "ITEM 1 was used on the Dark Lord"),
            (db.SW_FF_ARRIVED, "Fizz has said HEY"),
            (db.SW_FF_STICK, "Firstfield: got a stick"),
            (db.SW_FF_SHEEP_ASKED, "Firstfield: the sheep are lost"),
            (db.SW_FF_SHEEP_DONE, "Firstfield: the sheep are found"),
            (db.SW_FF_CHEST, "Firstfield: opened the chest"),
            (db.SW_FF_NORBERT, "Firstfield: Norbert has lost"),
            (db.SW_FF_GRADUATED, "Firstfield: tutorial completed"),
            (db.SW_VISITORS_BOOK, "Hollowell wants the visitors' book signed"),
            (db.SW_SPARE_FORM, "Gudgeon has issued Form P-9"),
            (db.SW_SPARE_REFUSED, "Spare has lost the argument at least once")]:
        switches[sid] = name
    for actor_id, sid in db.SW_RECRUIT.items():
        switches[sid] = "recruited actor %d" % actor_id
    for actor_id, sid in db.SW_KNOWN.items():
        switches[sid] = "actor %d has been in the party before" % actor_id
    for actor_id, sid in db.SW_STORY.items():
        switches[sid] = "actor %d has had a story of their own" % actor_id
    for sid, name in [
            (db.SW_WRE2_ASKED, "WRE-2: Dorcas will read a second plaque"),
            (db.SW_WRE2_UP, "WRE-2: the second plaque is up"),
            (db.SW_WRE5_NAMED, "WRE-5: Bramus is named"),
            (db.SW_PIP2_DONE, "PIP-2: the ballad has its last verse"),
            (db.SW_MER2_ASKED, "MER-2: clause eleven, the blank form"),
            (db.SW_MER2_SCALES, "MER-2: the fish stall's scales lent"),
            (db.SW_MER2_DONE, "MER-2: Bram certified fit to travel"),
            (db.SW_ROL4_SEEN, "ROL-4: Hob has seen the maker's mark"),
            (db.SW_ROL4_REFIT, "ROL-4: the sword rehafted for Hob"),
            (db.SW_HOB5_FORGED, "HOB-5: the tube plate is made"),
            (db.SW_HOB5_DONE, "HOB-5: Ott says it will do"),
            (db.SW_ZEPH5_DONE, "ZEPH-5: page twenty-three"),
            (db.SW_MER4_TOLD, "MER-4: no twelfth time; the jar paid"),
            (db.SW_MER4_DONE, "MER-4: left, which is the cure"),
            (db.SW_HOB3_GONE, "HOB-3: the anvil is outside"),
            (db.SW_HOB3_DONE, "HOB-3: the anvil is back"),
            (db.SW_NIX4_BEGUN, "NIX-4: the eleven are out"),
            (db.SW_NIX4_DONE, "NIX-4: the ledger is ruled off"),
            (db.SW_NIX5_ON, "NIX-5: the escort is on (ends)"),
            (db.SW_NIX5_DONE, "NIX-5: through without a fight"),
            (db.SW_WRE3_WALK, "WRE-3: the society's walk is on (ends)"),
            (db.SW_WRE3_DONE, "WRE-3: the Thing proved not to exist"),
            (db.SW_PIP5_ASKED, "PIP-5: there is a box"),
            (db.SW_PIP5_SIGNED, "PIP-5: Form S-7 countersigned"),
            (db.SW_PIP5_KEY, "PIP-5: the key, while Fenn was listened to"),
            (db.SW_PIP5_DONE, "PIP-5: the box opened and shut"),
            (db.SW_HOB2_ON, "HOB-2: Beatrice is quiet (ends)"),
            (db.SW_HOB2_CARRYING, "HOB-2: an attempt is being carried (ends)"),
            (db.SW_HOB2_DONE, "HOB-2: the gate is hung"),
            (db.SW_ROL3_DINNER, "ROL-3: the alumni dinner is on (ends)"),
            (db.SW_ROL3_DONE, "ROL-3: the toast"),
            (db.SW_HOB1_ON, "HOB-1: the retrieval tour is on"),
            (db.SW_HOB1_PICKS, "HOB-1: Nix asked for the picks"),
            (db.SW_HOB1_DONE, "HOB-1: Beatrice disqualified"),
            (db.SW_ALD4_DONE, "ALD-4: Duchess found, and stays"),
            (db.SW_PIP3_ON, "PIP-3: the contest is on (ends)"),
            (db.SW_PIP3_DONE, "PIP-3: second place"),
            (db.SW_COR5_DONE, "COR-5: appraised; no curse"),
            (db.SW_NIX1_LETTER, "NIX-1: the client's letter opened"),
            (db.SW_NIX1_DONE, "NIX-1: the coat collected"),
            (db.SW_NIX2_OPEN, "NIX-2: the Door open, informally"),
            (db.SW_NIX2_DONE, "NIX-2: we spent it"),
            (db.SW_ROL1_ON, "ROL-1: the review meeting is on (ends)"),
            (db.SW_ROL1_DONE, "ROL-1: the minutes"),
            (db.SW_ZEPH1_ON, "ZEPH-1: the eleventh notice read"),
            (db.SW_ZEPH1_TOLD, "ZEPH-1: no expulsion; purse or draft"),
            (db.SW_ZEPH1_PAID, "ZEPH-1: the purse turned out"),
            (db.SW_ZEPH1_EXPELLED, "ZEPH-1: expelled, at her own request"),
            (db.SW_ZEPH1_DONE, "ZEPH-1: decided, either way"),
            (db.SW_ZEPH3_DONE, "ZEPH-3: the demonstration; everyone fine"),
            (db.SW_ZEPH2_ON, "ZEPH-2: inquorate; fetch the duck"),
            (db.SW_ZEPH2_WALKING, "ZEPH-2: the duck is walking (ends)"),
            (db.SW_ZEPH2_DONE, "ZEPH-2: quorate; the proxy"),
            (db.SW_WRE1_ON, "WRE-1: the monograph is on"),
            (db.SW_WRE1_MOTT, "WRE-1: reviewed by Mott"),
            (db.SW_WRE1_FURZE, "WRE-1: reviewed by Furze"),
            (db.SW_WRE1_DUCK_DUE, "WRE-1: the duck's review is due (ends)"),
            (db.SW_WRE1_DUCK, "WRE-1: reviewed by the duck"),
            (db.SW_WRE1_DONE, "WRE-1: published"),
            (db.SW_COR1_ON, "COR-1: on the Roll; today, then"),
            (db.SW_COR1_HOME, "COR-1: home, and the tea"),
            (db.SW_COR1_DONE, "COR-1: the speech; the scarf"),
            (db.SW_COR2_STEP, "COR-2: the doorstep; the sword's name"),
            (db.SW_COR2_DONE, "COR-2: the report card"),
            (db.SW_MER5_ON, "MER-5: the Water Committee re-formed"),
            (db.SW_MER5_DONE, "MER-5: the curse lifted; item three"),
            (db.SW_MER1_ON, "MER-1: the queue instead of the symposium"),
            (db.SW_MER1_DONE, "MER-1: on points; the Pamphlet"),
            (db.SW_MER3_ON, "MER-3: the Table is sitting"),
            (db.SW_MER3_DONE, "MER-3: write it down; the Table's Kit"),
            (db.SW_ALD3_DONE, "ALD-3: Knight Errant, At Large"),
            (db.SW_ALD1_DONE, "ALD-1: the letter delivered"),
            (db.SW_ALD5_DONE, "ALD-5: the Fourth squires for him"),
            (db.SW_ALD2_DONE, "ALD-2: the vigil kept; confirmed"),
            (db.SW_ALD6_DONE, "ALD-6: the Wrong Dragon, read to"),
            (db.SW_WRE4_ON, "WRE-4: engaged to authenticate"),
            (db.SW_WRE4_JOINS, "WRE-4: shown every join"),
            (db.SW_WRE4_DONE, "WRE-4: written up; the fee"),
            (db.SW_COR3_ON, "COR-3: seventeenth"),
            (db.SW_COR3_DONE, "COR-3: the meeting; his chair kept"),
            (db.SW_COR4_DONE, "COR-4: the third reading"),
            (db.SW_PIP4_ON, "PIP-4: the interviews (ends)"),
            (db.SW_PIP4_DONE, "PIP-4: the elegy, nine lines"),
            (db.SW_PIP1_ON, "PIP-1: the Authorised Version, read"),
            (db.SW_PIP1_GOOD, "PIP-1: very good; one footnote"),
            (db.SW_PIP1_FIXED, "PIP-1: fixed, A. & P. Quill"),
            (db.SW_PIP1_DONE, "PIP-1: the official account settled"),
            (db.SW_NIX3_ON, "NIX-3: Lorrimer's list (ends)"),
            (db.SW_NIX3_DONE, "NIX-3: won on paperwork"),
            (db.SW_HOB4_TRADED, "HOB-4: a gate for the gatepost"),
            (db.SW_HOB4_DONE, "HOB-4: one sword, not for Hob"),
            (db.SW_ZEPH4_DONE, "ZEPH-4: the Fen burnt; the road open"),
            (db.SW_ROL5_ON, "ROL-5: met the understudy; to tell her?"),
            (db.SW_ROL5_DONE, "ROL-5: told; she is at the tower door"),
            (db.SW_ROL2_ON, "ROL-2: gone to see, under Carn Drey"),
            (db.SW_ROL2_DRAWN, "ROL-2: the sword out of the stone"),
            (db.SW_ROL2_DONE, "ROL-2: the Worm ended; discharged"),
            (db.SW_SPA1_DONE, "SPA-1: read out at the dinner hour"),
            (db.SW_SPA1_DINNER, "SPA-1: the dinner hour (scene)"),
            (db.SW_SPA4_DONE, "SPA-4: met, and written to by hand"),
            (db.SW_SPA2_ASKED, "SPA-2: Cotter has asked"),
            (db.SW_SPA2_CLEARED, "SPA-2: the paddle is clear"),
            (db.SW_SPA2_DONE, "SPA-2: out, and everybody there")]:
        switches[sid] = name

    variables = [""] * 33
    variables[db.VAR_COMPANIONS] = "companions recruited"
    variables[db.VAR_TROPES] = "tropes encountered"
    variables[db.VAR_TURNIPS] = "turnips eaten"
    variables[db.VAR_TALES] = "tales heard in the Slain Wyvern"
    variables[db.VAR_BOUNTIES] = "bounties claimed"
    variables[db.VAR_PLAQUES] = "wreck plaques read"
    variables[db.VAR_BLUSHES] = "things nobody quite said"
    variables[db.VAR_OTT_ORDER] = "Ott's beat, while the order is outstanding"
    variables[db.VAR_OTT_FLYING] = "Ott's beat, once the Two Hundred flies"
    variables[10] = "scratch: gold reallocated"
    variables[db.VAR_FF_STATIONS] = "Firstfield stations done"
    variables[db.VAR_FF_SHEEP] = "Firstfield sheep found"
    variables[db.VAR_FF_SIGNS] = "Firstfield signs read"
    variables[db.VAR_TOBY] = "Toby's delivery"
    variables[db.VAR_COMPANION_STORIES] = "companions with a story of their own"
    variables[db.VAR_MER2_WITNESS] = "MER-2: who witnessed it"
    variables[db.VAR_NIX4_RETURNED] = "NIX-4: returned, of eleven"
    variables[db.VAR_NIX5_BATTLES] = "NIX-5: battles when the escort set out"
    variables[db.VAR_PIP5_DECOY] = "PIP-5: who asked Fenn about clause twelve"
    variables[db.VAR_HOB2_TRY] = "HOB-2: attempts, of four"
    variables[db.VAR_ROL3_HEARD] = "ROL-3: alumni spoken to, of eleven"
    variables[db.VAR_HOB1_ASKED] = "HOB-1: owners asked, of eleven"
    variables[db.VAR_ZEPH1_PAID] = "ZEPH-1: crowns turned out in the Library"
    variables[db.VAR_WRE1_SPECIMENS] = "WRE-1: type specimens, of eleven"
    variables[db.VAR_MER1_POINTS] = "MER-1: Whatever Works' points"
    variables[db.VAR_PIP4_HEARD] = "PIP-4: accounts of Abel Thrush, of eleven"
    variables[db.VAR_NIX3_LOCATED] = "NIX-3: located with receipts, of three"
    variables[db.VAR_SPA1_POSTED] = "SPA-1: letters posted, of eight"
    variables[db.VAR_SPA1_ORDER] = "SPA-1: which went from where (digits)"
    variables[db.VAR_SPA4_TOUR] = "SPA-4: Effie's tour (4 is done)"
    variables[db.VAR_SPA2_PARTY] = "SPA-2: the party, set aside"
    variables[db.VAR_MOTHBALLS] = "P1: party steps when mothballs last used"

    system.update({
        "gameTitle": "The Obligatory Quest",
        "startMapId": village.MAP_HOME,
        "startX": village.HOME_START[0], "startY": village.HOME_START[1],
        "editMapId": village.MAP_VILLAGE,
        "partyMembers": [db.BRAM],
        "testBattlers": [], "testTroopId": db.TR_TURNIPS,
        "optFollowers": True, "optSideView": True, "optDisplayTp": True,
        "optAutosave": False, "optDrawTitle": True,
        "switches": switches, "variables": variables,
        # WRE-3's badge is Wren's alone: a type of its own (QUESTS.md 0.5).
        "armorTypes": system["armorTypes"][:db.AT_BADGE] + ["Badge", "Rosette", "Coat", "Robe", "Scarf", "Pamphlet", "Escutcheon", "Washer"],
        # Spare's bag is a weapon type of its own, and his tantrum an element
        # his mother is immune to (QUESTS.md F1).
        "weaponTypes": system["weaponTypes"][:db.WT_BAG] + ["Bag"],
        "elements": system["elements"][:db.EL_TEMPER] + ["Temper"],
        # The blank project ships all three vehicles parked on map 1 at
        # coordinates from a tutorial map that is not in this game - the
        # airship at (154, 70), which is a hundred tiles off the east edge of
        # Thistlewick. That is inherited junk, not setup. The Two Hundred is
        # earned, so it starts on map 0, which is nowhere, and an event puts
        # it on the world map the day Ott hands it over.
        #
        # The *ship* carries the same junk (map 1, 142x69) and is left alone:
        # it is unreachable, unreferenced and invisible, and NORTH.md 8.2
        # sanctions the airship only.
        "airship": {"bgm": {"name": "Ship3", "pan": 0, "pitch": 100,
                            "volume": 90},
                    "characterName": "Vehicle", "characterIndex": 3,
                    "startMapId": 0, "startX": 0, "startY": 0},
        "title1Name": "Bigtree", "title2Name": "",
        "titleBgm": {"name": "Theme3", "pan": 0, "pitch": 100, "volume": 80},
        "battleBgm": {"name": "Battle2", "pan": 0, "pitch": 100, "volume": 85},
        "victoryMe": {"name": "Victory1", "pan": 0, "pitch": 100, "volume": 85},
        "defeatMe": {"name": "Defeat1", "pan": 0, "pitch": 100, "volume": 85},
        "gameoverMe": {"name": "Gameover1", "pan": 0, "pitch": 100, "volume": 85},
        "battleback1Name": "Grassland", "battleback2Name": "Grassland",
        "currencyUnit": "cr",
    })
    system["terms"]["basic"][8] = "EXP"
    R.save_object("System.json", system)


def main():
    db.build()
    village.build()
    journey.build()
    south.build()
    wilds.build()
    north.build()
    q_spare.check_family()             # F1's gate names north.py's ids
    field.build()
    meadow.build()
    penultima.build()
    restwell.build()
    hithermost.build()
    fairholme.build()
    evermore.build()
    gladhollow.build()
    premises.build()
    frayne.build()
    frostwick.build()
    coldbarrow.build()
    sable_hart.build()
    hamlets.build()
    ashcombe.build()
    weeping_bottom.build()
    fenmarch.build()
    collegium.build()
    dunnage.build()
    q_corvin.build()                    # COR-2's drowned street
    q_roland.build()                    # ROL-2's dungeon under Carn Drey
    pottering.build()                   # SPA-4's village, Maps 68-69
    q_spare.build()                     # SPA-2's culvert, Map 70
    q_spare.check_couriers()            # F2's courier ids are the towns'
    shape_wall_tops()
    build_map_infos()
    build_tilesets()
    build_system()

    print("built The Obligatory Quest")
    print("  %d maps, %d playable characters, %d skills"
          % (len(MAP_NAMES), len(db.CLASSES), len(R.load("Skills.json")) - 1))
    print("  start: Map%03d '%s' at %s"
          % (village.MAP_HOME, "Bram's House", village.HOME_START))


if __name__ == "__main__":
    main()
