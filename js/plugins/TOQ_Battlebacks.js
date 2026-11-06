//=============================================================================
// TOQ_Battlebacks.js - a battle background by where the party is standing
//=============================================================================
// Thistlewick's own plugin. It is written here, in the game, and registered
// in js/plugins.js by build/build_game.py.

/*:
 * @target MZ
 * @plugindesc A battle background chosen by region, terrain or column, from tags in a map's note.
 * @author The Obligatory Quest
 *
 * @help TOQ_Battlebacks.js
 *
 * A map has one battle background in the editor. This lets a map's note
 * give it others, for the parts of the map that are somewhere else:
 *
 *   <battleback region 3: Sand/Desert>
 *   <battleback terrain 40,41: Snowfield/Snowfield>
 *   <battleback x 97-185: Fort2/Tower>
 *
 * `region` is the region id under the player, `terrain` the autotile kind
 * under them on tile layer 1 or 0 (the number the engine's own overworld
 * table switches on), and `x` the column they are standing in. Numbers are
 * a list, and a-b is a range. The first tag that matches wins; with none,
 * the map's own background stands. A scripted fight on a touch event starts
 * with the party standing on that event, so it is matched like any other.
 *
 * Change Battle Back (a command in an event) still wins over all of it,
 * until the map is entered again.
 */

(() => {
    "use strict";

    const TAG = /<battleback\s+(region|terrain|x)\s+([\d,\s-]+):\s*(\w*)\s*\/\s*(\w*)\s*>/gi;

    const numbers = text => {
        const set = new Set();
        for (const part of text.split(",")) {
            const [a, b] = part.trim().split("-").map(Number);
            for (let n = a; n <= (isNaN(b) ? a : b); n++) {
                set.add(n);
            }
        }
        return set;
    };

    let rulesFor = null;
    let rules = [];
    const mapRules = () => {
        if (rulesFor !== $dataMap) {
            rulesFor = $dataMap;
            rules = [];
            for (const m of ($dataMap && $dataMap.note || "").matchAll(TAG)) {
                rules.push({ kind: m[1].toLowerCase(), set: numbers(m[2]),
                             names: [m[3], m[4]] });
            }
        }
        return rules;
    };

    const matching = () => {
        const x = $gamePlayer.x;
        const y = $gamePlayer.y;
        for (const r of mapRules()) {
            if ((r.kind === "region" && r.set.has($gameMap.regionId(x, y))) ||
                (r.kind === "x" && r.set.has(x)) ||
                (r.kind === "terrain" &&
                 (r.set.has($gameMap.autotileType(x, y, 1)) ||
                  r.set.has($gameMap.autotileType(x, y, 0))))) {
                return r.names;
            }
        }
        return null;
    };

    // Change Battle Back writes straight over the map's own pair, so this is
    // the one place to tell an event's choice from the map's.
    const _setupBattleback = Game_Map.prototype.setupBattleback;
    Game_Map.prototype.setupBattleback = function() {
        _setupBattleback.call(this);
        this._toqBattlebackChanged = false;
    };

    const _changeBattleback = Game_Map.prototype.changeBattleback;
    Game_Map.prototype.changeBattleback = function(name1, name2) {
        _changeBattleback.call(this, name1, name2);
        this._toqBattlebackChanged = true;
    };

    const chosen = () =>
        BattleManager.isBattleTest() || $gameMap._toqBattlebackChanged
            ? null : matching();

    const _battleback1Name = Sprite_Battleback.prototype.battleback1Name;
    Sprite_Battleback.prototype.battleback1Name = function() {
        const names = chosen();
        return names ? names[0] : _battleback1Name.call(this);
    };

    const _battleback2Name = Sprite_Battleback.prototype.battleback2Name;
    Sprite_Battleback.prototype.battleback2Name = function() {
        const names = chosen();
        return names ? names[1] : _battleback2Name.call(this);
    };
})();
