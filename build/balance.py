"""A quick read on whether the fights are winnable, without running the game.

    python3 build/balance.py [level]

Reads the real Classes/Actors/Weapons/Armors/Skills/Enemies out of `data/` and
evaluates the damage formulas the same way `Game_Action` does, so the numbers
here are the numbers the engine will produce, minus variance and criticals.

It answers two questions per matchup: how many party turns it takes to kill the
enemy, and how many enemy turns it takes to kill the party. If the first number
is not comfortably smaller than the second, the fight is wrong.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import db  # noqa: E402
import rmmzdata as R  # noqa: E402

GAME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R.use_project(GAME)

PARAM_NAMES = ["mhp", "mmp", "atk", "def", "mat", "mdf", "agi", "luk"]


class Battler:
    """Just enough of Game_BattlerBase for the formulas to evaluate."""

    def __init__(self, name, params, level=1):
        self.name = name
        self.level = level
        self._params = list(params)
        self.hp = self._params[0]
        self.mp = self._params[1]

    def __getattr__(self, item):
        if item == "df":
            item = "def"
        if item in PARAM_NAMES:
            return self._params[PARAM_NAMES.index(item)]
        raise AttributeError(item)


def actor_battler(actor, classes, weapons, armors, level):
    cls = classes[actor["classId"]]
    params = [cls["params"][i][level] for i in range(8)]
    for slot, eid in enumerate(actor["equips"]):
        if not eid:
            continue
        table = weapons if slot == 0 else armors
        gear = table[eid]
        if gear and gear.get("name"):
            for i in range(8):
                params[i] += gear["params"][i]
    b = Battler(actor["name"], params, level)
    b.cls = cls["name"]
    b.known = [l["skillId"] for l in cls["learnings"] if l["level"] <= level]
    return b


class _Math:
    floor = staticmethod(lambda v: int(v // 1))
    ceil = staticmethod(lambda v: -int(-v // 1))
    round = staticmethod(lambda v: int(v + 0.5))
    max = staticmethod(max)
    min = staticmethod(min)
    random = staticmethod(lambda: 0.5)
    abs = staticmethod(abs)


def evaluate(formula, a, b):
    """Damage formulas are JavaScript. The only thing that is not also valid
    Python is `.def`, which is a keyword here, so it is rewritten to `.df` and
    the battlers answer to both."""
    expr = formula.replace(".def", ".df")
    expr = expr.replace("$gameParty.aliveMembers().length", "4")
    try:
        return max(0, int(eval(expr, {"__builtins__": {}},
                               {"a": a, "b": b, "v": lambda i: 0,
                                "Math": _Math, "item": None})))
    except Exception:
        return None


def party_damage(actor, skills, target, level):
    """Best single-target and best all-target damage this character can do,
    using only the skills their class has actually learned by this level."""
    best_single = ("Attack", max(0, actor.atk * 4 - target.df * 2))
    best_all = ("-", 0)
    for sid in actor.known:
        s = skills[sid]
        if not s or not s.get("name") or s["damage"]["type"] != 1:
            continue
        dmg = evaluate(s["damage"]["formula"], actor, target)
        if dmg is None:
            print("      (could not evaluate %s: %s)"
                  % (s["name"], s["damage"]["formula"]))
            continue
        n = dmg * (4 if s["scope"] == 4 else 1)
        if s["scope"] in (2, 3, 4, 5, 6):
            if n > best_all[1]:
                best_all = (s["name"], n)
        elif n > best_single[1]:
            best_single = (s["name"], n)
    return best_single, best_all


def enemy_damage(enemy, skills, target):
    out = []
    for act in enemy["actions"]:
        s = skills[act["skillId"]]
        if not s or s["damage"]["type"] not in (1, 5):
            continue
        f = s["damage"]["formula"]
        eb = Battler(enemy["name"], enemy["params"])
        dmg = evaluate(f, eb, target)
        if dmg is not None:
            out.append((s["name"] or "Attack", dmg, s["scope"]))
    plain = max(0, enemy["params"][2] * 4 - target.df * 2)
    out.append(("Attack", plain, 1))
    return out


def main():
    level = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    actors = R.load("Actors.json")
    classes = R.load("Classes.json")
    weapons = R.load("Weapons.json")
    armors = R.load("Armors.json")
    skills = R.load("Skills.json")
    enemies = R.load("Enemies.json")

    print("=== party at level %d (starting equipment) ===" % level)
    party = []
    for a in actors[1:]:
        if not a or not a.get("name"):
            continue
        b = actor_battler(a, classes, weapons, armors, level)
        party.append(b)
        print("  %-11s %-16s hp %4d mp %3d atk %3d def %3d mat %3d mdf %3d "
              "agi %3d luk %3d" % (b.name, b.cls, b.mhp, b.mmp, b.atk,
                                   getattr(b, "def"), b.mat, b.mdf, b.agi,
                                   b.luk))

    print("\n=== matchups (no variance, no criticals, no buffs) ===")
    for e in enemies[1:]:
        if not e or not e.get("name"):
            continue
        target = Battler(e["name"], e["params"])
        print("\n%-28s hp %5d def %3d mdf %3d" %
              (e["name"], e["params"][0], e["params"][3], e["params"][5]))

        total_single = 0
        for b in party:
            single, all_ = party_damage(b, skills, target, level)
            total_single += single[1]
            print("    %-11s best hit %-26s %5d   best sweep %-24s %5d"
                  % (b.name, single[0], single[1], all_[0], all_[1]))
        # A four-person party of the four best hitters, as a rough ceiling.
        best4 = sorted((party_damage(b, skills, target, level)[0][1]
                        for b in party), reverse=True)[:4]
        dps = sum(best4)
        turns = (e["params"][0] + dps - 1) // max(1, dps)
        print("    -> a strong party of four does about %d a turn: %d turns"
              % (dps, turns))

        squishiest = min(party, key=lambda b: b.mhp)
        hits = enemy_damage(e, skills, squishiest)
        worst = max(hits, key=lambda h: h[1])
        survives = squishiest.mhp // max(1, worst[1])
        print("    -> worst hit on %s (%d hp) is %s for %d: %d hits to drop"
              % (squishiest.name, squishiest.mhp, worst[0], worst[1], survives))


if __name__ == "__main__":
    main()
