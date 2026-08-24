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
import journey  # noqa: E402
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


def build_system():
    system = R.load("System.json")

    switches = [""] * 64
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
            (db.SW_WYVERN, "knows about the goose")]:
        switches[sid] = name
    for actor_id, sid in db.SW_RECRUIT.items():
        switches[sid] = "recruited actor %d" % actor_id

    variables = [""] * 32
    variables[db.VAR_COMPANIONS] = "companions recruited"
    variables[db.VAR_TROPES] = "tropes encountered"
    variables[db.VAR_TURNIPS] = "turnips eaten"
    variables[db.VAR_TALES] = "tales heard in the Slain Wyvern"
    variables[db.VAR_BOUNTIES] = "bounties claimed"
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
    build_map_infos()
    build_system()

    print("built The Obligatory Quest")
    print("  %d maps, %d playable characters, %d skills"
          % (len(MAP_NAMES), len(db.CLASSES), len(R.load("Skills.json")) - 1))
    print("  start: Map%03d '%s' at %s"
          % (village.MAP_HOME, "Bram's House", village.HOME_START))


if __name__ == "__main__":
    main()
