//=============================================================================
// TOQ_Mountain.js - the Stair under the mountain: the lamp, and continuance
//=============================================================================
// Thistlewick's own plugin (POSTGAME.md 9, QUESTS.md P4d). It is written here,
// in the game, and registered in js/plugins.js by build/build_game.py.

/*:
 * @target MZ
 * @plugindesc The Stair under the mountain: a circle of lamplight, and no Game Over.
 * @author The Obligatory Quest
 *
 * @help TOQ_Mountain.js
 *
 * Two things, each switched on by a tag in a map's note, so that nothing has
 * to be remembered to be switched off again on the way out:
 *
 *   <lamplight>     The map is dark except for a small circle of light round
 *                   the player, which is the lamp Sir Dunstable lent them.
 *
 *   <continuance>   A random encounter lost on this map is not Game Over. The
 *                   party is revived and comes back in through the chapel
 *                   porch, by the common event in the parameters, which
 *                   restores them and says so. It is the one place in the
 *                   game this happens, because the chapel stands beside the
 *                   only door into the mountain (POSTGAME.md 9).
 *
 * A scripted battle on such a map is left alone: it has its own lose branch,
 * and that branch calls the same common event.
 *
 * @param commonEvent
 * @text Hand-back common event
 * @desc Run after a lost battle on a <continuance> map.
 * @type common_event
 * @default 7
 *
 * @param mapId
 * @text Porch map
 * @type number
 * @default 34
 *
 * @param x
 * @text Porch x
 * @type number
 * @default 7
 *
 * @param y
 * @text Porch y
 * @type number
 * @default 13
 */

(() => {
    "use strict";
    const params = PluginManager.parameters("TOQ_Mountain");
    const COMMON_EVENT = Number(params.commonEvent || 7);
    const PORCH = [Number(params.mapId || 34), Number(params.x || 7),
                   Number(params.y || 13)];

    const tagged = tag => !!($dataMap && $dataMap.meta && $dataMap.meta[tag]);

    // ------------------------------------------------------- continuance ---
    // Sent back through the porch: the transfer is reserved now, so the map
    // the battle returns to is the chapel and the mountain is never seen
    // again in between; the common event does the rest once it is up.
    const comeBack = () => {
        $gamePlayer.reserveTransfer(PORCH[0], PORCH[1], PORCH[2], 8, 2);
        $gameTemp.reserveCommonEvent(COMMON_EVENT);
    };

    // The common event is reserved *after* the original has run, because
    // processDefeat ends in endBattle, and endBattle clears every common
    // event reservation - one made before it is silently thrown away.
    const _processDefeat = BattleManager.processDefeat;
    BattleManager.processDefeat = function() {
        const ours = !this._canLose && !this._eventCallback &&
            tagged("continuance");
        if (ours) {
            this._canLose = true;
        }
        _processDefeat.call(this);
        if (ours) {
            comeBack();
        }
    };

    // Nothing on the Stair kills on the map itself today (slip and floor
    // death are both off), but if anything ever does, it is the same rule.
    const _checkGameover = Scene_Map.prototype.checkGameover;
    Scene_Map.prototype.checkGameover = function() {
        if ($gameParty.isAllDead() && tagged("continuance") &&
                !$gamePlayer.isTransferring()) {
            $gameParty.reviveBattleMembers();
            comeBack();
            return;
        }
        _checkGameover.call(this);
    };

    // --------------------------------------------------------- the lamp ---
    // A screen of dark, twice the size of the screen, with a soft hole in the
    // middle of it, kept centred on the player. It sits above the characters
    // and the weather and under the pictures and the windows.
    const DARK = 0.94, INNER = 84, OUTER = 210;

    function Sprite_Lamplight() {
        this.initialize(...arguments);
    }

    Sprite_Lamplight.prototype = Object.create(Sprite.prototype);
    Sprite_Lamplight.prototype.constructor = Sprite_Lamplight;

    Sprite_Lamplight.prototype.initialize = function() {
        Sprite.prototype.initialize.call(this);
        const w = Graphics.width, h = Graphics.height;
        this.bitmap = new Bitmap(w * 2, h * 2);
        const ctx = this.bitmap.context;
        ctx.fillStyle = "rgba(8, 5, 0, " + DARK + ")";
        ctx.fillRect(0, 0, w * 2, h * 2);
        ctx.globalCompositeOperation = "destination-out";
        const g = ctx.createRadialGradient(w, h, INNER, w, h, OUTER);
        g.addColorStop(0, "rgba(0, 0, 0, 1)");
        g.addColorStop(0.55, "rgba(0, 0, 0, 0.55)");
        g.addColorStop(1, "rgba(0, 0, 0, 0)");
        ctx.fillStyle = g;
        ctx.beginPath();
        ctx.arc(w, h, OUTER, 0, Math.PI * 2);
        ctx.fill();
        ctx.globalCompositeOperation = "source-over";
        this.bitmap.baseTexture.update();
        this.anchor.x = 0.5;
        this.anchor.y = 0.5;
        this._tick = 0;
        this.update();
    };

    Sprite_Lamplight.prototype.update = function() {
        Sprite.prototype.update.call(this);
        this.visible = tagged("lamplight");
        this.x = $gamePlayer.screenX();
        this.y = $gamePlayer.screenY() - $gameMap.tileHeight() / 2;
        // A flame, not a bulb: never still, never much.
        this._tick++;
        const s = 1 + 0.018 * Math.sin(this._tick / 7) +
                  0.01 * Math.sin(this._tick / 2.3);
        this.scale.x = this.scale.y = s;
    };

    const _createLowerLayer = Spriteset_Map.prototype.createLowerLayer;
    Spriteset_Map.prototype.createLowerLayer = function() {
        _createLowerLayer.call(this);
        this._lamplight = new Sprite_Lamplight();
        this.addChild(this._lamplight);
    };

    window.Sprite_Lamplight = Sprite_Lamplight;
})();
