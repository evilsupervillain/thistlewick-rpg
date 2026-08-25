"""Builds the whole of The Obligatory Quest from scratch.

    python3 build/build_game.py

Re-runnable: every record is written at its own id, so running it again
rewrites the game rather than piling up duplicates. This, and the modules it
calls, is the only place the game's content is authored - `data/*.json` is
output, not source.
"""
import os
import sys

GAME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GAME, "build"))

import mapkit  # noqa: E402,F401  puts the workspace's tools/ on the path
import rmmzdata as R  # noqa: E402

R.use_project(GAME)

import db  # noqa: E402
import field  # noqa: E402
import journey  # noqa: E402
import north  # noqa: E402
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


def build_tilesets():
    """`Tilesets.json` is the one data file this game inherits rather than
    authors, so the edits it needs are written here, by id, and OR-ed in - the
    build stays re-runnable and the diff stays one number wide."""
    tilesets = R.load("Tilesets.json")
    for tid, flags in TILESET_FLAGS.items():
        for tile_id, bits in flags.items():
            tilesets[tid]["flags"][tile_id] |= bits
    R.save_list("Tilesets.json", tilesets)


def build_system():
    system = R.load("System.json")

    switches = [""] * 72
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
            (db.SW_BALLAD_ASKED, "the Fete Sub-Committee has met"),
            (db.SW_BALLAD_DONE, "verse seven was struck"),
            (db.SW_CENSUS, "heard about the Cold Winter"),
            (db.SW_COTTERILL, "met the Cotterills"),
            (db.SW_SPARE_ASKED, "Spare has applied to come along"),
            (db.SW_LONG_FIELD, "walked the Long Field"),
            (db.SW_CLAUSE_SEVEN, "Ott showed you clause seven"),
            (db.SW_ROOM_FOUR, "room four has not been down since Tuesday"),
            (db.SW_GERALD, "there was a Gerald"),
            (db.SW_TWO_HUNDRED_FLEW, "the Two Hundred set down by the tower")]:
        switches[sid] = name
    for actor_id, sid in db.SW_RECRUIT.items():
        switches[sid] = "recruited actor %d" % actor_id

    variables = [""] * 32
    variables[db.VAR_COMPANIONS] = "companions recruited"
    variables[db.VAR_TROPES] = "tropes encountered"
    variables[db.VAR_TURNIPS] = "turnips eaten"
    variables[db.VAR_TALES] = "tales heard in the Slain Wyvern"
    variables[db.VAR_BOUNTIES] = "bounties claimed"
    variables[db.VAR_PLAQUES] = "wreck plaques read"
    variables[db.VAR_BLUSHES] = "things nobody quite said"
    variables[10] = "scratch: gold reallocated"

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
    field.build()
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
