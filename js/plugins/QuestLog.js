//=============================================================================
// QuestLog.js - a quest log read from the game's own switches and variables
//=============================================================================
// The master copy is tools/questlog/QuestLog.js in the rpgmaker-mz workspace.
// A game carries a copy in its own js/plugins/, installed by questlog.py, and
// check.py reports a copy that has drifted from the master. Edit the master.

/*:
 * @target MZ
 * @plugindesc A quest log that reads quest state from switches, variables and self switches.
 * @author rpgmaker-mz workspace
 *
 * @help QuestLog.js
 *
 * Quests are defined in data/Quests.json, which a build script writes. Each
 * quest's status - unknown, active, completed or failed - and each objective
 * is a condition over the game's existing state: switches, variables, self
 * switches, items and party members. The game sets the switches it was
 * already setting and the log follows; a banner is shown whenever a quest
 * starts, changes, completes or fails, once no message or event is running.
 *
 * A quest with nothing to read can be driven by the plugin commands instead,
 * and the two can be mixed. Completed and failed are remembered once seen,
 * even if the switch behind them later goes off.
 *
 * Script calls, for a Conditional Branch:
 *   QuestLog.status("key")      "unknown", "active", "completed" or "failed"
 *   QuestLog.isActive("key")    also isCompleted, isFailed, isKnown
 *   QuestLog.objectiveDone("key", "objective")
 *   QuestLog.tracked()          the tracked quest's key, or null
 *   QuestLog.refresh()          recompute now rather than on the next frame
 *
 * The full description of the data file is QUESTLOG.md in the workspace.
 *
 * @param menuName
 * @text Menu command
 * @desc The label of the menu command that opens the log.
 * @default Quests
 *
 * @param menuSwitch
 * @text Menu switch
 * @type switch
 * @desc If set, the menu command is shown only while this switch is on.
 * @default 0
 *
 * @param banner
 * @text Banners
 * @type boolean
 * @desc Show a banner on the map when a quest starts, changes or ends.
 * @default true
 *
 * @param bannerFrames
 * @text Banner frames
 * @parent banner
 * @type number
 * @min 30
 * @desc How long one banner stays up, in frames.
 * @default 120
 *
 * @param newText
 * @text New quest text
 * @parent banner
 * @default New quest:
 *
 * @param updateText
 * @text Updated text
 * @parent banner
 * @default Quest updated:
 *
 * @param completeText
 * @text Completed text
 * @parent banner
 * @default Quest complete:
 *
 * @param failText
 * @text Failed text
 * @parent banner
 * @default Quest failed:
 *
 * @param newSe
 * @text New quest sound
 * @parent banner
 * @type file
 * @dir audio/se/
 * @desc Empty for silence.
 * @default Item3
 *
 * @param updateSe
 * @text Updated sound
 * @parent banner
 * @type file
 * @dir audio/se/
 * @default Book1
 *
 * @param completeSe
 * @text Completed sound
 * @parent banner
 * @type file
 * @dir audio/se/
 * @default Chime2
 *
 * @param failSe
 * @text Failed sound
 * @parent banner
 * @type file
 * @dir audio/se/
 * @default Down2
 *
 * @param tracker
 * @text Tracker
 * @type boolean
 * @desc Offer the map tracker: the tracked quest's current objective in a corner of the map.
 * @default false
 *
 * @param trackerOption
 * @text Tracker option name
 * @parent tracker
 * @desc The Options entry that shows or hides the tracker.
 * @default Quest Tracker
 *
 * @param trackerPosition
 * @text Tracker position
 * @parent tracker
 * @type select
 * @option top-right
 * @option top-left
 * @option bottom-right
 * @option bottom-left
 * @default top-right
 *
 * @param tabNames
 * @text Tab names
 * @desc The three tabs of the log, comma separated.
 * @default Active, Completed, Failed
 *
 * @param emptyText
 * @text Empty tab text
 * @default Nothing here yet.
 *
 * @param maskText
 * @text Hidden objective text
 * @desc Drawn in place of an objective whose "hidden" is "mask".
 * @default ???
 *
 * @param rewardLabel
 * @text Reward label
 * @desc Drawn before a quest's reward. Empty hides the reward line.
 * @default Reward:
 *
 * @command Start
 * @text Start quest
 * @desc Sets the quest's explicit "started" flag.
 * @arg quest
 * @text Quest
 * @desc The quest's key.
 * @arg silent
 * @text Silent
 * @type boolean
 * @desc Change the quest without a banner.
 * @default false
 *
 * @command Complete
 * @text Complete quest
 * @desc Sets the quest's explicit "completed" flag.
 * @arg quest
 * @text Quest
 * @desc The quest's key.
 * @arg silent
 * @text Silent
 * @type boolean
 * @default false
 *
 * @command Fail
 * @text Fail quest
 * @desc Sets the quest's explicit "failed" flag.
 * @arg quest
 * @text Quest
 * @desc The quest's key.
 * @arg silent
 * @text Silent
 * @type boolean
 * @default false
 *
 * @command CompleteObjective
 * @text Complete objective
 * @desc Sets an objective's explicit "done" flag.
 * @arg quest
 * @text Quest
 * @desc The quest's key.
 * @arg objective
 * @text Objective
 * @desc The objective's key.
 * @arg silent
 * @text Silent
 * @type boolean
 * @default false
 *
 * @command RevealObjective
 * @text Reveal objective
 * @desc Shows an objective whose "visible" condition does not hold.
 * @arg quest
 * @text Quest
 * @desc The quest's key.
 * @arg objective
 * @text Objective
 * @desc The objective's key.
 * @arg silent
 * @text Silent
 * @type boolean
 * @default false
 *
 * @command SetProgress
 * @text Set progress
 * @desc Sets an objective's explicit progress counter.
 * @arg quest
 * @text Quest
 * @desc The quest's key.
 * @arg objective
 * @text Objective
 * @desc The objective's key.
 * @arg value
 * @text Value
 * @type number
 * @default 0
 * @arg silent
 * @text Silent
 * @type boolean
 * @default false
 *
 * @command AddProgress
 * @text Add progress
 * @desc Adds to an objective's explicit progress counter.
 * @arg quest
 * @text Quest
 * @desc The quest's key.
 * @arg objective
 * @text Objective
 * @desc The objective's key.
 * @arg value
 * @text Amount
 * @type number
 * @min -9999
 * @default 1
 * @arg silent
 * @text Silent
 * @type boolean
 * @default false
 *
 * @command Track
 * @text Track quest
 * @desc Tracks a quest; an empty key stops tracking.
 * @arg quest
 * @text Quest
 * @desc The quest's key, or empty.
 *
 * @command Open
 * @text Open quest log
 * @desc Opens the quest log screen.
 */

var QuestLog = (() => {
    "use strict";
    const QuestLog = { version: 1 };

    //=========================================================================
    // The model. Nothing in this part touches the engine, so node can load
    // the file and test it (test_conditions.js). It sees the game through a
    // reader:
    //
    //   switch(n), variable(n), self(mapId, eventId, ch), count(kind, id),
    //   inParty(actorId), script(expr), flags(questKey), latched(questKey),
    //   wasKnown(questKey)
    //
    // where kind is "item", "weapon" or "armor", flags() returns the quest's
    // explicit flags {started, completed, failed, objectives: {key: {done,
    // revealed, progress}}} or null, and latched() returns "completed",
    // "failed" or null, and wasKnown() is whether the quest has ever been in
    // the log.
    //=========================================================================

    const OPS = {
        "==": (a, b) => a === b,
        "!=": (a, b) => a !== b,
        "<": (a, b) => a < b,
        "<=": (a, b) => a <= b,
        ">": (a, b) => a > b,
        ">=": (a, b) => a >= b
    };

    const STATUSES = ["unknown", "active", "completed", "failed"];

    class Model {
        // quests: the Quests.json array, element 0 null.
        constructor(quests, reader) {
            this.quests = (quests || []).filter(q => q);
            this.byKey = {};
            for (const q of this.quests) this.byKey[q.key] = q;
            this.reader = reader;
            this.invalidate();
        }

        invalidate() {
            this._status = {};
            this._view = {};
        }

        quest(key) {
            return this.byKey[key] || null;
        }

        keys() {
            return this.quests.map(q => q.key);
        }

        //---------------------------------------------------- conditions ----
        // `quest` is the key that {"flag": ...} refers to.
        test(cond, quest) {
            if (cond === true) return true;
            if (cond === false || cond === null || cond === undefined) return false;
            if (typeof cond !== "object") {
                throw new Error("QuestLog: bad condition " + JSON.stringify(cond));
            }
            const r = this.reader;
            if ("all" in cond) return cond.all.every(c => this.test(c, quest));
            if ("any" in cond) return cond.any.some(c => this.test(c, quest));
            if ("not" in cond) return !this.test(cond.not, quest);
            if ("switch" in cond) return !!r.switch(cond.switch);
            if ("var" in cond) {
                const value = r.variable(cond.var);
                if (cond.op === undefined && cond.value === undefined) return value !== 0;
                const op = OPS[cond.op || "=="];
                if (!op) throw new Error("QuestLog: bad op " + cond.op);
                return op(value, cond.value);
            }
            if ("self" in cond) return !!r.self(cond.self[0], cond.self[1], cond.self[2] || "A");
            for (const kind of ["item", "weapon", "armor"]) {
                if (kind in cond) {
                    return r.count(kind, cond[kind]) >= (cond.count === undefined ? 1 : cond.count);
                }
            }
            if ("actor" in cond) return !!r.inParty(cond.actor);
            if ("quest" in cond) {
                const status = this.status(cond.quest);
                const is = cond.is || "known";
                return is === "known" ? status !== "unknown" : status === is;
            }
            if ("flag" in cond) return this.flag(quest, cond.flag, cond.objective);
            if ("script" in cond) return !!r.script(cond.script);
            throw new Error("QuestLog: bad condition " + JSON.stringify(cond));
        }

        flag(quest, name, objective) {
            const flags = this.reader.flags(quest);
            if (!flags) return false;
            if (objective === undefined) return !!flags[name];
            const o = flags.objectives && flags.objectives[objective];
            return !!(o && o[name]);
        }

        //-------------------------------------------------------- status ----
        // Latched beats everything; then failed, completed, active. Each
        // condition is ORed with the explicit flag of the same name, and an
        // omitted condition is the flag alone. A quest can only fail once it
        // has started, or been in the log: one the player was never offered
        // has nothing to fail, and is not announced as failing.
        status(key) {
            if (key in this._status) {
                // A quest whose status depends on itself, through other
                // quests, reads as unknown at the point of the cycle;
                // check.py reports cycles, so this is only a guard.
                return this._status[key] === null ? "unknown" : this._status[key];
            }
            const q = this.quest(key);
            if (!q) return "unknown";
            this._status[key] = null;
            let status = this.reader.latched(key);
            if (!status) {
                const started = this.holds(q, "start", "started");
                const known = started || this.reader.wasKnown(key);
                if (known && this.holds(q, "fail", "failed")) status = "failed";
                else if (this.holds(q, "complete", "completed")) status = "completed";
                else if (started) status = "active";
                else status = "unknown";
            }
            this._status[key] = status;
            return status;
        }

        holds(q, field, flag) {
            return this.flag(q.key, flag) || (field in q && this.test(q[field], q.key));
        }

        //---------------------------------------------------------- view ----
        // Everything the log draws for one quest, or null while unknown.
        view(key) {
            if (key in this._view) return this._view[key];
            const q = this.quest(key);
            const status = this.status(key);
            let result = null;
            if (q && status !== "unknown") {
                const finished = status !== "active";
                const objectives = [];
                let current = null;
                for (const o of q.objectives || []) {
                    const v = this.objective(q, o, status);
                    if (!v.shown && (finished || v.hidden === "omit")) continue;
                    if (!current && status === "active" && v.shown && !v.done && !v.optional) {
                        current = v;
                        v.current = true;
                    }
                    objectives.push(v);
                }
                result = {
                    key: key,
                    status: status,
                    title: q.title || key,
                    category: q.category || "side",
                    giver: q.giver || "",
                    location: q.location || "",
                    description: this.description(q),
                    objectives: objectives,
                    current: current,
                    reward: q.reward || ""
                };
            }
            this._view[key] = result;
            return result;
        }

        objective(q, o, status) {
            const flags = this.reader.flags(q.key);
            const f = (flags && flags.objectives && flags.objectives[o.key]) || {};
            let progress = null;
            let of = null;
            if (o.progress) {
                of = o.progress.of;
                const raw = o.progress.var ? this.reader.variable(o.progress.var) : (f.progress || 0);
                progress = Math.max(0, Math.min(of, Number(raw) || 0));
            }
            let done = !!f.done;
            if (!done) {
                if ("done" in o) done = this.test(o.done, q.key);
                else if (o.progress) done = progress >= of;
            }
            const visible = !("visible" in o) || this.test(o.visible, q.key);
            const shown = visible || !!f.revealed || done;
            // A completed quest ticks what the player could see, whatever the
            // game's state says: a step it skipped is not a step left undone.
            if (status === "completed" && shown && !o.optional) done = true;
            return {
                key: o.key,
                text: o.text || "",
                optional: !!o.optional,
                hidden: o.hidden || "omit",
                shown: shown,
                done: done,
                progress: progress,
                of: of,
                current: false
            };
        }

        description(q) {
            let entries = q.description;
            if (entries === undefined || entries === null) return "";
            if (typeof entries === "string") return entries;
            let text = "";
            for (const e of entries) {
                if (typeof e === "string") text = e;
                else if (!("when" in e) || this.test(e.when, q.key)) text = e.text;
            }
            return text;
        }

        //------------------------------------------------------ snapshot ----
        // What the change detector compares. Two snapshots that differ mean
        // the player has something new to read.
        snapshot(key) {
            const v = this.view(key);
            if (!v) return { status: "unknown" };
            return {
                status: v.status,
                def: hash(JSON.stringify(this.quest(key))),
                shown: v.objectives.filter(o => o.shown).map(o => o.key),
                done: v.objectives.filter(o => o.done).map(o => o.key),
                progress: v.objectives.filter(o => o.of !== null).map(o => o.progress),
                description: v.description
            };
        }
    }

    // A short fingerprint of a quest's definition, so that a game update
    // which rewords a quest is not announced as news in every save.
    function hash(text) {
        let h = 5381;
        for (let i = 0; i < text.length; i++) h = ((h * 33) ^ text.charCodeAt(i)) >>> 0;
        return h.toString(36);
    }

    // The kind of change between two snapshots: "start", "update",
    // "complete", "fail", "drop" (active to unknown, which is not announced)
    // or null for none.
    function change(before, after) {
        const was = before ? before.status : "unknown";
        const now = after.status;
        if (was === now) {
            if (now !== "active" || before.def !== after.def) return null;
            return JSON.stringify(before) === JSON.stringify(after) ? null : "update";
        }
        if (now === "completed") return "complete";
        if (now === "failed") return "fail";
        if (now === "active") return was === "unknown" ? "start" : "update";
        return "drop";
    }

    QuestLog.Model = Model;
    QuestLog.change = change;
    QuestLog.OPS = OPS;
    QuestLog.STATUSES = STATUSES;

    if (typeof PluginManager === "undefined") {
        return QuestLog;            // loaded by node, for the model alone
    }

    //=========================================================================
    // The engine side.
    //=========================================================================

    const PLUGIN = "QuestLog";
    const params = PluginManager.parameters(PLUGIN);
    const P = {
        menuName: String(params.menuName || "Quests"),
        menuSwitch: Number(params.menuSwitch || 0),
        banner: params.banner !== "false",
        bannerFrames: Number(params.bannerFrames || 120),
        tracker: params.tracker === "true",
        trackerOption: String(params.trackerOption || "Quest Tracker"),
        trackerPosition: String(params.trackerPosition || "top-right"),
        tabNames: String(params.tabNames || "Active, Completed, Failed")
            .split(",").map(t => t.trim()),
        emptyText: String(params.emptyText === undefined ? "Nothing here yet." : params.emptyText),
        maskText: String(params.maskText === undefined ? "???" : params.maskText),
        rewardLabel: String(params.rewardLabel === undefined ? "Reward:" : params.rewardLabel),
        bannerText: {
            start: String(params.newText || "New quest:"),
            update: String(params.updateText || "Quest updated:"),
            complete: String(params.completeText || "Quest complete:"),
            fail: String(params.failText || "Quest failed:")
        },
        bannerSe: {
            start: String(params.newSe === undefined ? "Item3" : params.newSe),
            update: String(params.updateSe === undefined ? "Book1" : params.updateSe),
            complete: String(params.completeSe === undefined ? "Chime2" : params.completeSe),
            fail: String(params.failSe === undefined ? "Down2" : params.failSe)
        }
    };
    QuestLog.parameters = P;

    DataManager._databaseFiles.push({ name: "$dataQuests", src: "Quests.json" });

    //------------------------------------------------------------- the save --
    // Everything kept lives on $gameSystem, so it rides in the save. It is
    // made on first use, which is how a save from before the plugin was
    // installed comes to have one.
    function newStore() {
        return {
            version: 1,
            flags: {},          // key -> {started, completed, failed, objectives}
            snapshot: null,     // key -> Model.snapshot(); null until first taken
            latched: {},        // key -> "completed" | "failed"
            seen: {},           // key -> true once read in the log since its last change
            order: {},          // key -> the order it became known in
            nextOrder: 1,
            tracked: null
        };
    }

    function store() {
        if (!window.$gameSystem) return null;
        if (!$gameSystem._questLog) $gameSystem._questLog = newStore();
        return $gameSystem._questLog;
    }

    function questFlags(key, create) {
        const s = store();
        if (!s) return null;
        if (!s.flags[key] && create) s.flags[key] = { objectives: {} };
        return s.flags[key] || null;
    }

    //------------------------------------------------------------ the reader --
    const scripts = {};
    const KINDS = { item: () => $dataItems, weapon: () => $dataWeapons, armor: () => $dataArmors };

    const reader = {
        switch: n => $gameSwitches.value(n),
        variable: n => $gameVariables.value(n),
        self: (m, e, ch) => $gameSelfSwitches.value([m, e, ch]),
        count: (kind, id) => {
            const data = KINDS[kind] && KINDS[kind]();
            const item = data && data[id];
            if (!item) return 0;
            let n = $gameParty.numItems(item);
            if (kind !== "item") {
                for (const actor of $gameParty.allMembers()) {
                    n += actor.equips().filter(e => e === item).length;
                }
            }
            return n;
        },
        inParty: id => $gameParty._actors.includes(id),
        script: expr => {
            scripts[expr] = scripts[expr] || new Function("return (" + expr + ");");
            return scripts[expr]();
        },
        flags: key => questFlags(key, false),
        latched: key => {
            const s = store();
            return (s && s.latched[key]) || null;
        },
        wasKnown: key => {
            const s = store();
            return !!(s && key in s.order);
        }
    };

    let model = null;

    function theModel() {
        if (!model || model.source !== window.$dataQuests) {
            model = new Model(window.$dataQuests || [null], reader);
            model.source = window.$dataQuests;
        }
        return model;
    }

    // Something a condition can read has changed.
    function markDirty() {
        QuestLog._dirty = true;
        if (model) model.invalidate();
    }
    QuestLog._dirty = true;
    QuestLog.markDirty = markDirty;
    QuestLog.model = theModel;

    //----------------------------------------------------------- dirtying --
    // Every way the game changes something a condition can read. A script
    // condition can read anything; the model is also invalidated once a
    // frame on the map, which covers it.
    for (const cls of [Game_Switches, Game_Variables, Game_SelfSwitches]) {
        const onChange = cls.prototype.onChange;
        cls.prototype.onChange = function() {
            onChange.apply(this, arguments);
            markDirty();
        };
    }
    for (const method of ["gainItem", "addActor", "removeActor"]) {
        const original = Game_Party.prototype[method];
        Game_Party.prototype[method] = function() {
            original.apply(this, arguments);
            markDirty();
        };
    }

    //---------------------------------------------------- change detection --
    // Recompute every quest, compare with the snapshot in the save, and queue
    // one banner per change. The first snapshot a save ever gets is taken
    // silently - a new game, or a save from before the plugin was installed -
    // and so is a quest whose definition changed in a game update, unless its
    // status changed too. Returns the changes queued.
    QuestLog._queue = [];
    const silenced = new Set();

    function detect() {
        const s = store();
        if (!s || !window.$dataQuests) return [];
        const m = theModel();
        m.invalidate();
        QuestLog._dirty = false;
        const first = !s.snapshot;
        const snapshot = s.snapshot || {};
        const changes = [];
        for (const key of m.keys()) {
            const before = snapshot[key];
            const after = m.snapshot(key);
            let kind = null;
            if (!first) {
                // A quest new to Quests.json is news only if it is under way.
                kind = before ? change(before, after) : (after.status === "active" ? "start" : null);
            }
            if (after.status !== "unknown" && !(key in s.order)) s.order[key] = s.nextOrder++;
            if (after.status === "completed" || after.status === "failed") {
                s.latched[key] = after.status;
            }
            if (first || !before) {
                s.seen[key] = true;
            }
            if (kind) {
                delete s.seen[key];
                if (kind === "start" && !s.tracked) s.tracked = key;
                if (kind !== "drop" && !silenced.has(key)) {
                    changes.push({ kind: kind, key: key, title: m.quest(key).title || key });
                }
            }
            if (s.tracked === key && after.status !== "active") s.tracked = null;
            snapshot[key] = after;
        }
        s.snapshot = snapshot;
        silenced.clear();
        // With banners off nothing is ever shown, so nothing should wait.
        if (P.banner) QuestLog._queue.push(...changes);
        return changes;
    }

    function isIdle(scene) {
        return scene.isActive() && !SceneManager.isSceneChanging() &&
            !$gameMessage.isBusy() && !$gameMap.isEventRunning() &&
            !$gamePlayer.isTransferring();
    }

    // A script condition can read anything, so a game that has one is also
    // looked at once a second, dirty or not.
    function hasScripts() {
        return !!window.$dataQuests && JSON.stringify(window.$dataQuests).includes('"script"');
    }

    const _Scene_Map_updateMain = Scene_Map.prototype.updateMain;
    Scene_Map.prototype.updateMain = function() {
        _Scene_Map_updateMain.call(this);
        if (model) model.invalidate();
        if (model && model.hasScripts === undefined) model.hasScripts = hasScripts();
        const tick = model && model.hasScripts && Graphics.frameCount % 60 === 0;
        if ((QuestLog._dirty || tick) && isIdle(this)) detect();
    };

    // A new game's snapshot is taken at once, before any autorun can start a
    // quest, so that the opening quest is announced rather than swallowed.
    const _DataManager_setupNewGame = DataManager.setupNewGame;
    DataManager.setupNewGame = function() {
        _DataManager_setupNewGame.call(this);
        QuestLog._queue = [];
        silenced.clear();
        markDirty();
        detect();
    };

    const _Game_System_onAfterLoad = Game_System.prototype.onAfterLoad;
    Game_System.prototype.onAfterLoad = function() {
        _Game_System_onAfterLoad.call(this);
        QuestLog._queue = [];
        silenced.clear();
        markDirty();
        if (!store().snapshot) detect();
    };

    //------------------------------------------------------- plugin commands --
    function knownQuest(key) {
        if (theModel().quest(key)) return true;
        console.warn("QuestLog: no quest with the key " + JSON.stringify(key));
        return false;
    }

    function objectiveFlags(args) {
        const key = String(args.quest || "");
        const objective = String(args.objective || "");
        if (!knownQuest(key)) return null;
        const q = theModel().quest(key);
        if (!(q.objectives || []).some(o => o.key === objective)) {
            console.warn("QuestLog: " + key + " has no objective " + JSON.stringify(objective));
            return null;
        }
        const flags = questFlags(key, true);
        flags.objectives = flags.objectives || {};
        flags.objectives[objective] = flags.objectives[objective] || {};
        return flags.objectives[objective];
    }

    function changed(args) {
        if (args.silent === "true") silenced.add(String(args.quest));
        markDirty();
    }

    for (const [command, flag] of [["Start", "started"], ["Complete", "completed"], ["Fail", "failed"]]) {
        PluginManager.registerCommand(PLUGIN, command, args => {
            const key = String(args.quest || "");
            if (!knownQuest(key)) return;
            questFlags(key, true)[flag] = true;
            changed(args);
        });
    }

    PluginManager.registerCommand(PLUGIN, "CompleteObjective", args => {
        const o = objectiveFlags(args);
        if (!o) return;
        o.done = true;
        changed(args);
    });

    PluginManager.registerCommand(PLUGIN, "RevealObjective", args => {
        const o = objectiveFlags(args);
        if (!o) return;
        o.revealed = true;
        changed(args);
    });

    PluginManager.registerCommand(PLUGIN, "SetProgress", args => {
        const o = objectiveFlags(args);
        if (!o) return;
        o.progress = Number(args.value) || 0;
        changed(args);
    });

    PluginManager.registerCommand(PLUGIN, "AddProgress", args => {
        const o = objectiveFlags(args);
        if (!o) return;
        o.progress = (o.progress || 0) + (Number(args.value) || 0);
        changed(args);
    });

    PluginManager.registerCommand(PLUGIN, "Track", args => {
        const key = String(args.quest || "");
        if (key && !knownQuest(key)) return;
        store().tracked = key || null;
    });

    //-------------------------------------------------------- the script API --
    QuestLog.status = key => theModel().status(key);
    QuestLog.isActive = key => QuestLog.status(key) === "active";
    QuestLog.isCompleted = key => QuestLog.status(key) === "completed";
    QuestLog.isFailed = key => QuestLog.status(key) === "failed";
    QuestLog.isKnown = key => QuestLog.status(key) !== "unknown";
    QuestLog.objectiveDone = (key, objective) => {
        const v = theModel().view(key);
        const o = v && v.objectives.find(x => x.key === objective);
        return !!(o && o.done);
    };
    QuestLog.view = key => theModel().view(key);
    QuestLog.refresh = () => {
        markDirty();
        return detect();
    };
    QuestLog.pending = () => QuestLog._queue.slice();
    QuestLog.tracked = () => {
        const s = store();
        return (s && s.tracked) || null;
    };

    //=========================================================================
    // The log screen: three tabs, a list, and a detail pane that follows the
    // cursor. Left and right change tab, confirm tracks the selected quest,
    // page up and page down (and the wheel, and dragging) scroll the detail.
    //=========================================================================

    const TABS = ["active", "completed", "failed"];

    // The quests with a status, main first and then in the order they became
    // known.
    QuestLog.listed = status => {
        const m = theModel();
        const s = store();
        const order = k => (s && s.order[k]) || 1e9;
        const main = k => ((m.quest(k).category || "side") === "main" ? 0 : 1);
        return m.keys().filter(k => m.status(k) === status)
            .sort((a, b) => main(a) - main(b) || order(a) - order(b));
    };

    function markSeen(key) {
        const s = store();
        if (s && key) s.seen[key] = true;
    }

    // Font sizes the screen draws in, relative to the game's own.
    const bodyFontSize = () => Math.max(16, $gameSystem.mainFontSize() - 4);
    const bodyLineHeight = () => bodyFontSize() + 10;

    function drawStar(bitmap, cx, cy, r, color) {
        const ctx = bitmap.context;
        ctx.save();
        ctx.fillStyle = color;
        ctx.strokeStyle = ColorManager.outlineColor();
        ctx.lineWidth = 2;
        ctx.beginPath();
        for (let i = 0; i < 10; i++) {
            const a = -Math.PI / 2 + (i * Math.PI) / 5;
            const rr = i % 2 === 0 ? r : r * 0.45;
            ctx.lineTo(cx + Math.cos(a) * rr, cy + Math.sin(a) * rr);
        }
        ctx.closePath();
        ctx.stroke();
        ctx.fill();
        ctx.restore();
        bitmap._baseTexture.update();
    }

    function drawBox(bitmap, x, y, size, done, color, alpha) {
        const ctx = bitmap.context;
        ctx.save();
        ctx.globalAlpha = alpha;
        ctx.lineJoin = "round";
        ctx.lineCap = "round";
        ctx.strokeStyle = ColorManager.outlineColor();
        ctx.lineWidth = 4;
        ctx.strokeRect(x + 1, y + 1, size - 2, size - 2);
        ctx.strokeStyle = color;
        ctx.lineWidth = 2;
        ctx.strokeRect(x + 1, y + 1, size - 2, size - 2);
        if (done) {
            const tick = () => {
                ctx.beginPath();
                ctx.moveTo(x + size * 0.2, y + size * 0.5);
                ctx.lineTo(x + size * 0.42, y + size * 0.75);
                ctx.lineTo(x + size * 0.85, y + size * 0.15);
                ctx.stroke();
            };
            ctx.strokeStyle = ColorManager.outlineColor();
            ctx.lineWidth = 6;
            tick();
            ctx.strokeStyle = color;
            ctx.lineWidth = 3;
            tick();
        }
        ctx.restore();
        bitmap._baseTexture.update();
    }

    //------------------------------------------------------------ the tabs --
    // Never active: the list owns the keyboard, and a click on a tab is
    // handled here directly.
    function Window_QuestTabs() {
        this.initialize(...arguments);
    }

    Window_QuestTabs.prototype = Object.create(Window_HorzCommand.prototype);
    Window_QuestTabs.prototype.constructor = Window_QuestTabs;

    Window_QuestTabs.prototype.maxCols = function() {
        return TABS.length;
    };

    Window_QuestTabs.prototype.makeCommandList = function() {
        TABS.forEach((status, i) => {
            const name = P.tabNames[i] || status;
            this.addCommand(name + " (" + QuestLog.listed(status).length + ")", status);
        });
    };

    Window_QuestTabs.prototype.update = function() {
        Window_HorzCommand.prototype.update.call(this);
        if (this.isOpen() && !this.active && TouchInput.isTriggered()) {
            const i = this.hitIndex();
            if (i >= 0 && i !== this.index()) {
                this.playCursorSound();
                if (this._onTab) this._onTab(i);
            }
        }
    };

    //------------------------------------------------------------ the list --
    function Window_QuestList() {
        this.initialize(...arguments);
    }

    Window_QuestList.prototype = Object.create(Window_Selectable.prototype);
    Window_QuestList.prototype.constructor = Window_QuestList;

    Window_QuestList.prototype.initialize = function(rect) {
        Window_Selectable.prototype.initialize.call(this, rect);
        this._keys = [];
    };

    Window_QuestList.prototype.setKeys = function(keys) {
        this._keys = keys;
        this.refresh();
    };

    Window_QuestList.prototype.maxItems = function() {
        return this._keys.length;
    };

    Window_QuestList.prototype.item = function() {
        return this._keys[this.index()] || null;
    };

    Window_QuestList.prototype.isCurrentItemEnabled = function() {
        return !!this.item() && QuestLog.status(this.item()) === "active";
    };

    // Left and right change tab, even on an empty tab with no cursor.
    Window_QuestList.prototype.isCursorMovable = function() {
        return this.isOpenAndActive();
    };

    Window_QuestList.prototype.cursorRight = function() {
        if (this._onTabStep) this._onTabStep(1);
    };

    Window_QuestList.prototype.cursorLeft = function() {
        if (this._onTabStep) this._onTabStep(-1);
    };

    Window_QuestList.prototype.cursorDown = function(wrap) {
        if (this.maxItems() > 0) Window_Selectable.prototype.cursorDown.call(this, wrap);
    };

    Window_QuestList.prototype.cursorUp = function(wrap) {
        if (this.maxItems() > 0) Window_Selectable.prototype.cursorUp.call(this, wrap);
    };

    Window_QuestList.prototype.resetFontSettings = function() {
        Window_Selectable.prototype.resetFontSettings.call(this);
        this.contents.fontSize = bodyFontSize();
    };

    Window_QuestList.prototype.refresh = function() {
        Window_Selectable.prototype.refresh.call(this);
        if (this.maxItems() === 0) {
            const rect = this.itemLineRect(0);
            this.changePaintOpacity(false);
            this.drawText(P.emptyText, rect.x, rect.y, rect.width, "center");
            this.changePaintOpacity(true);
        }
    };

    Window_QuestList.prototype.markerWidth = function() {
        return bodyFontSize() + 6;
    };

    Window_QuestList.prototype.drawItem = function(index) {
        const key = this._keys[index];
        const q = theModel().quest(key);
        const s = store();
        const rect = this.itemLineRect(index);
        const mw = this.markerWidth();
        const cx = rect.x + mw / 2 - 2;
        const cy = rect.y + rect.height / 2;
        if (s.tracked === key) {
            drawStar(this.contents, cx, cy, bodyFontSize() * 0.42, ColorManager.textColor(17));
        } else if (!s.seen[key]) {
            this.contents.drawCircle(cx, cy, 4, ColorManager.textColor(24));
        }
        this.resetTextColor();
        if ((q.category || "side") === "main") this.changeTextColor(ColorManager.systemColor());
        this.drawText(q.title || key, rect.x + mw, rect.y, rect.width - mw);
    };

    Window_QuestList.prototype.updateHelp = function() {
        const key = this.item();
        if (this._helpWindow) this._helpWindow.setQuest(key);
        if (key && !store().seen[key]) {
            markSeen(key);
            this.redrawItem(this.index());
        }
    };

    //---------------------------------------------------------- the detail --
    // A window whose contents bitmap is as tall as the quest needs; scrolling
    // moves the origin over it rather than redrawing.
    function Window_QuestDetail() {
        this.initialize(...arguments);
    }

    Window_QuestDetail.prototype = Object.create(Window_Scrollable.prototype);
    Window_QuestDetail.prototype.constructor = Window_QuestDetail;

    Window_QuestDetail.prototype.initialize = function(rect) {
        this._overallHeight = 0;
        this._key = null;
        this._fontSize = 0;
        Window_Scrollable.prototype.initialize.call(this, rect);
    };

    Window_QuestDetail.prototype.overallHeight = function() {
        return Math.max(this._overallHeight, this.innerHeight);
    };

    Window_QuestDetail.prototype.contentsHeight = function() {
        return this.overallHeight();
    };

    Window_QuestDetail.prototype.scrollBlockWidth = function() {
        return 1e6;
    };

    Window_QuestDetail.prototype.scrollBlockHeight = function() {
        return 1e6;
    };

    Window_QuestDetail.prototype.itemHeight = function() {
        return bodyLineHeight();
    };

    Window_QuestDetail.prototype.paint = function() {
        //
    };

    Window_QuestDetail.prototype.resetFontSettings = function() {
        Window_Scrollable.prototype.resetFontSettings.call(this);
        if (this._fontSize) this.contents.fontSize = this._fontSize;
    };

    Window_QuestDetail.prototype.setQuest = function(key) {
        if (this._key !== key) {
            this._key = key;
            this.refresh();
        }
    };

    Window_QuestDetail.prototype.scrollPage = function(direction) {
        this.smoothScrollBy(0, direction * (this.innerHeight - bodyLineHeight()));
    };

    // Lay the quest out as a list of drawing steps, so the height is known
    // before the bitmap is made.
    Window_QuestDetail.prototype.layout = function(v) {
        const steps = [];
        const width = this.innerWidth;
        const body = bodyFontSize();
        const lh = bodyLineHeight();
        let y = 0;
        steps.push({ kind: "title", y: y, text: v.title, main: v.category === "main" });
        y += this.lineHeight();
        const where = [v.giver, v.location].filter(t => t).join("  \u00b7  ");
        if (where) {
            steps.push({ kind: "dim", y: y, text: where });
            y += lh;
        }
        y += lh / 2;
        if (v.description) {
            this._fontSize = body;
            for (const line of this.wrap(v.description, width)) {
                steps.push({ kind: "text", y: y, text: line });
                y += lh;
            }
            y += lh / 2;
        }
        for (const o of v.objectives) {
            steps.push({ kind: "objective", y: y, o: o });
            y += lh;
        }
        if (v.reward && P.rewardLabel) {
            y += lh / 2;
            steps.push({ kind: "reward", y: y, text: v.reward });
            y += lh;
        }
        return { steps: steps, height: Math.ceil(y) };
    };

    // Greedy word wrap, measured with the engine's own text measure so that
    // control codes cost what they draw. A newline in the text is a break.
    Window_QuestDetail.prototype.wrap = function(text, width) {
        const lines = [];
        for (const paragraph of String(text).split("\n")) {
            let line = "";
            for (const word of paragraph.split(" ")) {
                const trial = line ? line + " " + word : word;
                if (line && this.textSizeEx(trial).width > width) {
                    lines.push(line);
                    line = word;
                } else {
                    line = trial;
                }
            }
            lines.push(line);
        }
        return lines;
    };

    Window_QuestDetail.prototype.refresh = function() {
        const v = this._key ? QuestLog.view(this._key) : null;
        this._fontSize = 0;
        if (!this.contents) this.createContents();
        const plan = v ? this.layout(v) : { steps: [], height: 0 };
        this._overallHeight = plan.height;
        this.createContents();
        this._scrollY = 0;
        this._scrollBaseY = 0;
        this.clearScrollStatus();
        this.origin.y = 0;
        for (const step of plan.steps) this.drawStep(step);
    };

    Window_QuestDetail.prototype.drawStep = function(step) {
        const width = this.innerWidth;
        const lh = bodyLineHeight();
        const body = bodyFontSize();
        this._fontSize = step.kind === "title" ? 0 : body;
        this.resetFontSettings();
        switch (step.kind) {
            case "title":
                if (step.main) this.changeTextColor(ColorManager.systemColor());
                this.drawText(step.text, 0, step.y, width);
                break;
            case "dim":
                this.changePaintOpacity(false);
                this.drawText(step.text, 0, step.y, width, "left");
                this.changePaintOpacity(true);
                break;
            case "text":
                this.drawTextEx(step.text, 0, step.y, width);
                break;
            case "objective":
                this.drawObjective(step.o, step.y, width, lh, body);
                break;
            case "reward": {
                this.changeTextColor(ColorManager.systemColor());
                this.contents.drawText(P.rewardLabel, 0, step.y, width, lh);
                const lw = this.textWidth(P.rewardLabel + " ");
                this.drawTextEx(step.text, lw, step.y, width - lw);
                break;
            }
        }
    };

    Window_QuestDetail.prototype.drawObjective = function(o, y, width, lh, body) {
        const box = Math.round(body * 0.8);
        const tx = box + 12;
        const masked = !o.shown;
        const dim = o.done || masked;
        drawBox(this.contents, 2, y + (lh - box) / 2, box, o.done && !masked,
                ColorManager.normalColor(), dim ? 0.55 : 1);
        let right = "";
        if (o.of !== null && !masked) right = o.progress + "/" + o.of;
        else if (o.optional && !masked) right = "optional";
        const rw = right ? this.textWidth(right) + 8 : 0;
        if (right) {
            this.changePaintOpacity(false);
            this.contents.drawText(right, tx, y, width - tx, lh, "right");
        }
        // drawTextEx resets the colour and font but not the paint opacity,
        // so a done objective draws translucent.
        this.changePaintOpacity(!dim);
        if (masked) {
            this.contents.drawText(P.maskText, tx, y, width - tx - rw, lh);
        } else {
            this.drawTextEx(o.text, tx, y, width - tx - rw);
        }
        this.changePaintOpacity(true);
    };

    //----------------------------------------------------------- the scene --
    function Scene_Quest() {
        this.initialize(...arguments);
    }

    Scene_Quest.prototype = Object.create(Scene_MenuBase.prototype);
    Scene_Quest.prototype.constructor = Scene_Quest;

    Scene_Quest.prototype.helpAreaHeight = function() {
        return 0;
    };

    Scene_Quest.prototype.needsPageButtons = function() {
        return false;
    };

    Scene_Quest.prototype.create = function() {
        Scene_MenuBase.prototype.create.call(this);
        detect();
        this.createTabWindow();
        this.createDetailWindow();
        this.createListWindow();
        this.openTab(this.initialTab(), QuestLog.tracked());
    };

    // The tab holding the tracked quest, or the first with anything in it.
    Scene_Quest.prototype.initialTab = function() {
        const tracked = QuestLog.tracked();
        if (tracked) {
            const i = TABS.indexOf(QuestLog.status(tracked));
            if (i >= 0) return i;
        }
        const i = TABS.findIndex(t => QuestLog.listed(t).length > 0);
        return Math.max(0, i);
    };

    Scene_Quest.prototype.tabWindowRect = function() {
        return new Rectangle(0, this.mainAreaTop(), Graphics.boxWidth, this.calcWindowHeight(1, true));
    };

    Scene_Quest.prototype.listWidth = function() {
        return Math.floor(Graphics.boxWidth * 0.4);
    };

    Scene_Quest.prototype.paneRect = function(x, width) {
        const top = this._tabWindow.y + this._tabWindow.height;
        return new Rectangle(x, top, width, this.mainAreaBottom() - top);
    };

    Scene_Quest.prototype.createTabWindow = function() {
        this._tabWindow = new Window_QuestTabs(this.tabWindowRect());
        this._tabWindow.deactivate();
        this._tabWindow._onTab = i => this.openTab(i);
        this.addWindow(this._tabWindow);
    };

    Scene_Quest.prototype.createDetailWindow = function() {
        const lw = this.listWidth();
        this._detailWindow = new Window_QuestDetail(this.paneRect(lw, Graphics.boxWidth - lw));
        this.addWindow(this._detailWindow);
    };

    Scene_Quest.prototype.createListWindow = function() {
        const list = new Window_QuestList(this.paneRect(0, this.listWidth()));
        list.setHelpWindow(this._detailWindow);
        list.setHandler("ok", this.onTrack.bind(this));
        list.setHandler("cancel", this.popScene.bind(this));
        list.setHandler("pagedown", this.onPage.bind(this, 1));
        list.setHandler("pageup", this.onPage.bind(this, -1));
        list._onTabStep = step => {
            SoundManager.playCursor();
            this.openTab((this._tab + step + TABS.length) % TABS.length);
        };
        this.addWindow(list);
        this._listWindow = list;
    };

    Scene_Quest.prototype.openTab = function(index, key) {
        this._tab = index;
        this._tabWindow.select(index);
        const keys = QuestLog.listed(TABS[index]);
        this._listWindow.setKeys(keys);
        this._listWindow.select(Math.max(0, keys.indexOf(key)));
        if (keys.length === 0) this._listWindow.select(-1);
        this._listWindow.activate();
        this._listWindow.callUpdateHelp();
        if (keys.length === 0) this._detailWindow.setQuest(null);
    };

    Scene_Quest.prototype.onTrack = function() {
        const key = this._listWindow.item();
        const s = store();
        s.tracked = s.tracked === key ? null : key;
        this._listWindow.refresh();
        this._listWindow.activate();
    };

    Scene_Quest.prototype.onPage = function(direction) {
        this._detailWindow.scrollPage(direction);
        this._listWindow.activate();
    };

    //=========================================================================
    // Banners: one line at the top of the map per change, in the order they
    // were queued, each with its sound. A banner leaves the queue only once
    // it has been shown, so one cut short by a scene change is shown again.
    //=========================================================================

    function Window_QuestBanner() {
        this.initialize(...arguments);
    }

    Window_QuestBanner.prototype = Object.create(Window_Base.prototype);
    Window_QuestBanner.prototype.constructor = Window_QuestBanner;

    // A window that is visible stamps the window layer's stencil even when
    // it draws nothing, and every window added before it is then clipped
    // out of that rectangle. So the banner and the tracker are invisible,
    // not merely transparent, whenever they have nothing to show.
    Window_QuestBanner.prototype.initialize = function(rect) {
        Window_Base.prototype.initialize.call(this, rect);
        this.opacity = 0;
        this.contentsOpacity = 0;
        this.visible = false;
        this._baseY = rect.y;
        this._current = null;
        this._count = 0;
    };

    Window_QuestBanner.SLIDE = 12;

    Window_QuestBanner.prototype.update = function() {
        Window_Base.prototype.update.call(this);
        if (!this._current) {
            if (this._canStart && this._canStart() && QuestLog._queue.length > 0) this.start();
            return;
        }
        const total = P.bannerFrames;
        const fade = 16;
        this._count++;
        if (this._count <= fade) {
            this.contentsOpacity = (255 * this._count) / fade;
            this.y = this._baseY - Window_QuestBanner.SLIDE * (1 - this._count / fade);
        } else if (this._count > total - fade) {
            this.contentsOpacity = (255 * (total - this._count)) / fade;
        }
        if (this._count >= total) {
            this.contentsOpacity = 0;
            this.visible = false;
            // Remove this banner, not whatever is first: the queue may have
            // been emptied under it by a load or a new game.
            const i = QuestLog._queue.indexOf(this._current);
            if (i >= 0) QuestLog._queue.splice(i, 1);
            this._current = null;
        }
    };

    Window_QuestBanner.prototype.start = function() {
        this._current = QuestLog._queue[0];
        this._count = 0;
        this.visible = true;
        this.refresh();
        const se = P.bannerSe[this._current.kind];
        if (se) AudioManager.playSe({ name: se, volume: 90, pitch: 100, pan: 0 });
    };

    Window_QuestBanner.prototype.isShowing = function() {
        return !!this._current;
    };

    Window_QuestBanner.prototype.refresh = function() {
        this.contents.clear();
        const c = this._current;
        if (!c) return;
        const width = this.innerWidth;
        const lh = this.lineHeight();
        const half = width / 2;
        this.contents.gradientFillRect(0, 0, half, lh, ColorManager.dimColor2(), ColorManager.dimColor1());
        this.contents.gradientFillRect(half, 0, half, lh, ColorManager.dimColor1(), ColorManager.dimColor2());
        const label = P.bannerText[c.kind] + " ";
        const title = c.title;
        const lw = this.textWidth(label);
        const tw = this.textWidth(title);
        const x = Math.max(0, (width - lw - tw) / 2);
        this.changeTextColor(ColorManager.systemColor());
        this.drawText(label, x, 0, lw);
        this.resetTextColor();
        this.drawText(title, x + lw, 0, width - x - lw);
    };

    const _Scene_Map_createAllWindows = Scene_Map.prototype.createAllWindows;
    Scene_Map.prototype.createAllWindows = function() {
        _Scene_Map_createAllWindows.call(this);
        this.createQuestBannerWindow();
        if (P.tracker) this.createQuestTrackerWindow();
    };

    Scene_Map.prototype.createQuestBannerWindow = function() {
        const ww = Math.min(Graphics.boxWidth, 600);
        const wh = this.calcWindowHeight(1, false);
        const rect = new Rectangle((Graphics.boxWidth - ww) / 2, Window_QuestBanner.SLIDE, ww, wh);
        const banner = new Window_QuestBanner(rect);
        // Never over a message, an event, or the map's own name.
        banner._canStart = () => P.banner && isIdle(this) &&
            !(this._mapNameWindow && (this._mapNameWindow._showCount > 0 ||
                                      this._mapNameWindow.contentsOpacity > 0));
        this.addWindow(banner);
        this._questBannerWindow = banner;
    };

    //=========================================================================
    // The tracker: the tracked quest's title and current objective in a
    // corner of the map. Hidden during messages and events, and absent from
    // every other scene; switched off in Options. It never points anywhere.
    //=========================================================================

    function Window_QuestTracker() {
        this.initialize(...arguments);
    }

    Window_QuestTracker.prototype = Object.create(Window_Base.prototype);
    Window_QuestTracker.prototype.constructor = Window_QuestTracker;

    Window_QuestTracker.prototype.initialize = function(rect) {
        Window_Base.prototype.initialize.call(this, rect);
        this.opacity = 0;
        this.contentsOpacity = 0;
        this.visible = false;
        this._signature = "";
        this._wanted = false;
    };

    Window_QuestTracker.prototype.resetFontSettings = function() {
        Window_Base.prototype.resetFontSettings.call(this);
        this.contents.fontSize = bodyFontSize();
    };

    Window_QuestTracker.prototype.lineHeight = function() {
        return bodyLineHeight();
    };

    // What it would show now, or null for nothing.
    Window_QuestTracker.prototype.subject = function() {
        if (!P.tracker || !ConfigManager.questTracker) return null;
        const key = QuestLog.tracked();
        const v = key ? QuestLog.view(key) : null;
        return v && v.status === "active" ? v : null;
    };

    Window_QuestTracker.prototype.update = function() {
        Window_Base.prototype.update.call(this);
        const v = this.subject();
        const o = v && v.current;
        const signature = v ? [v.key, v.title, o && o.text, o && o.progress].join("\u0001") : "";
        if (signature !== this._signature) {
            this._signature = signature;
            if (v) this.refresh(v);
        }
        this._wanted = !!v && !(this._isBusy && this._isBusy());
        this.contentsOpacity += this._wanted ? 24 : -24;
        this.visible = this.contentsOpacity > 0;
    };

    Window_QuestTracker.prototype.isShowing = function() {
        return this._wanted;
    };

    Window_QuestTracker.prototype.refresh = function(v) {
        this.contents.clear();
        const width = this.innerWidth;
        const lh = this.lineHeight();
        const lines = v.current ? 2 : 1;
        const color = ColorManager.dimColor1();
        this.contents.fillRect(0, 0, width, lh * lines, color);
        this.resetFontSettings();
        this.changeTextColor(ColorManager.systemColor());
        this.drawText(v.title, 6, 0, width - 12);
        const o = v.current;
        if (o) {
            this.resetFontSettings();
            let rw = 0;
            if (o.of !== null) {
                const right = o.progress + "/" + o.of;
                rw = this.textWidth(right) + 8;
                this.drawText(right, 6, lh, width - 12, "right");
            }
            this.drawTextEx(o.text, 6, lh, width - 12 - rw);
        }
    };

    Scene_Map.prototype.questTrackerRect = function() {
        const ww = Math.min(420, Graphics.boxWidth / 2);
        const wh = bodyLineHeight() * 2 + $gameSystem.windowPadding() * 2;
        const pos = P.trackerPosition;
        const wx = pos.includes("left") ? 0 : Graphics.boxWidth - ww;
        // Below the touch-UI menu button rather than under it.
        const top = ConfigManager.touchUI && pos === "top-right" ? this.buttonAreaHeight() : 0;
        const wy = pos.includes("bottom") ? Graphics.boxHeight - wh : top;
        return new Rectangle(wx, wy, ww, wh);
    };

    Scene_Map.prototype.createQuestTrackerWindow = function() {
        const tracker = new Window_QuestTracker(this.questTrackerRect());
        // Out of the way of anything the player is reading or watching, and
        // of the map's name if they share a corner.
        tracker._isBusy = () => $gameMessage.isBusy() || $gameMap.isEventRunning() ||
            this._questBannerWindow.isShowing() ||
            (P.trackerPosition === "top-left" && this._mapNameWindow &&
             this._mapNameWindow.contentsOpacity > 0);
        this.addWindow(tracker);
        this._questTrackerWindow = tracker;
    };

    //------------------------------------------------- the Options toggle --
    ConfigManager.questTracker = true;

    const _makeData = ConfigManager.makeData;
    ConfigManager.makeData = function() {
        const config = _makeData.call(this);
        config.questTracker = this.questTracker;
        return config;
    };

    const _applyData = ConfigManager.applyData;
    ConfigManager.applyData = function(config) {
        _applyData.call(this, config);
        this.questTracker = this.readFlag(config, "questTracker", true);
    };

    const _addGeneralOptions = Window_Options.prototype.addGeneralOptions;
    Window_Options.prototype.addGeneralOptions = function() {
        _addGeneralOptions.call(this);
        if (P.tracker) this.addCommand(P.trackerOption, "questTracker");
    };

    const _maxCommands = Scene_Options.prototype.maxCommands;
    Scene_Options.prototype.maxCommands = function() {
        return _maxCommands.call(this) + (P.tracker ? 1 : 0);
    };

    window.Scene_Quest = Scene_Quest;
    window.Window_QuestTracker = Window_QuestTracker;
    window.Window_QuestBanner = Window_QuestBanner;
    window.Window_QuestTabs = Window_QuestTabs;
    window.Window_QuestList = Window_QuestList;
    window.Window_QuestDetail = Window_QuestDetail;

    PluginManager.registerCommand(PLUGIN, "Open", () => {
        SceneManager.push(Scene_Quest);
    });

    //------------------------------------------------------- the menu entry --
    const _addOriginalCommands = Window_MenuCommand.prototype.addOriginalCommands;
    Window_MenuCommand.prototype.addOriginalCommands = function() {
        _addOriginalCommands.call(this);
        if (!P.menuSwitch || $gameSwitches.value(P.menuSwitch)) {
            this.addCommand(P.menuName, "questLog", true);
        }
    };

    const _createCommandWindow = Scene_Menu.prototype.createCommandWindow;
    Scene_Menu.prototype.createCommandWindow = function() {
        _createCommandWindow.call(this);
        this._commandWindow.setHandler("questLog", () => SceneManager.push(Scene_Quest));
    };

    return QuestLog;
})();

if (typeof module !== "undefined") {
    module.exports = QuestLog;
}
