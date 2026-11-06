//=============================================================================
// TOQ_Offset.js - an event drawn a few pixels off its cell
//=============================================================================
// Thistlewick's own plugin. It is written here, in the game, and registered
// in js/plugins.js by build/build_game.py.

/*:
 * @target MZ
 * @plugindesc An event's picture nudged by pixels, from a tag in its note.
 * @author The Obligatory Quest
 *
 * @help TOQ_Offset.js
 *
 * An event is drawn on the grid. This lets its note move the picture:
 *
 *   <offset:-1,-14>
 *
 * is one pixel left and fourteen up - a dead plant in the mouth of the pot
 * on the cell, rather than lying on the pot's side. Only the picture moves:
 * the event still stands on, collides on and is triggered from its own
 * cell, and its balloons and animations are drawn over the picture.
 */

(() => {
    "use strict";

    const TAG = /<offset:\s*(-?\d+)\s*,\s*(-?\d+)\s*>/i;

    const offset = event => {
        if (event._toqOffset === undefined) {
            const m = TAG.exec(event.event().note || "");
            event._toqOffset = m ? [Number(m[1]), Number(m[2])] : null;
        }
        return event._toqOffset;
    };

    const _screenX = Game_Event.prototype.screenX;
    Game_Event.prototype.screenX = function() {
        const o = offset(this);
        return _screenX.call(this) + (o ? o[0] : 0);
    };

    const _screenY = Game_Event.prototype.screenY;
    Game_Event.prototype.screenY = function() {
        const o = offset(this);
        return _screenY.call(this) + (o ? o[1] : 0);
    };
})();
