"""Roland Fairweather's companion quests - `COMPANIONS.md`, his section, and
`QUESTS.md` for the order they are built in.

Nothing here draws a map, and this module imports no place module: the place
modules call in here for pages.

ROL-4, The Maker's Mark (`QUESTS.md` A5)
----------------------------------------
The sword he leaves you at the door has a mark on it. Hob knows the mark. It
is his aunt's. It was made at the forge in Thistlewick forty years ago, and
sold, and travelled, and came back.

* **It happens at the anvil in Hob's smithy** - Map 6, event 4, the hammer
  called Beatrice. One page, no switches, so the pages below it wait on no
  ladder. The forge the sword was made at is the right place to look at it.
* **Before the door.** Roland never *equips* Fairweather's Own - he wears his
  practice sword and carries the other one, and `journey.roland_departure`
  hands it over from what he is carrying. So the look is Roland's page, with
  him taking it out to show; Hob is a branch inside it (one actor to a page).
* **Nobody explains the hammer** (`COMPANIONS.md`, twice). Hob says his aunt
  made the sword and that she did good work. Beatrice says nothing. What the
  player makes of a hammer with a name on it is theirs.
* **The refit is after he has gone**, on Hob's page: the blade on an ash
  haft, as an axe, because Hob's class takes axes and not swords, and a class
  is published. `WP_REHAFTED` is an axe nobody else can hold. The sword is
  found carried *or* equipped - Bram can wield it - so the check and the
  taking are both script, with `includeEquip`.
"""
import copy

import db
import rmmzdata as R
import story as S

HAS_SWORD = "$gameParty.hasItem($dataWeapons[%d], true)" % db.WP_FAIRWEATHER


def _like(page0, cmds, conditions):
    """A page in exactly another page's dress, with its own commands and
    conditions."""
    shaped = R.page(cmds, conditions=conditions)
    page = copy.deepcopy(page0)
    page["list"] = shaped["list"]
    page["conditions"] = shaped["conditions"]
    return page


def _the_mark():
    """Roland and Hob at the anvil. The whole of ROL-4 that matters."""
    c = S.narrate([
        "Roland stops at the anvil. He has been quiet since",
        "you came in."])
    c += S.say("Roland", [
        "Hob. Would you look at something",
        "for me? Professionally."])
    c += S.narrate([
        "He unbuckles the sword he carries and never uses -",
        "not the one on his hip, the other one - and lays it",
        "across the anvil."])
    c += S.say("Roland", [
        "I leave it at a door. Every time.",
        "And every time, somehow, it finds",
        "its way back to me."])
    c += S.say("Roland", [
        "I've never known who made it.",
        "There's a mark by the hilt."])
    c += S.narrate([
        "Hob picks it up. He turns it to the light from the",
        "forge, and looks at the mark by the hilt, and does",
        "not say anything for a while."])
    c += S.narrate([
        "It is a small mark, struck with a punch: a B and a G",
        "run together, the way somebody signs a thing they",
        "are not ashamed of."])
    c += [R.wait(40)]
    c += S.say("Hob", ["That's my aunt's."])
    c += S.say("Hob", [
        "She made this here. On this.",
        "Forty years back, near enough.",
        "Sold it to a man going south."])
    c += S.narrate([
        "Roland looks at the sword, and at the forge, and at",
        "Hob, and for once he does not say anything clever."])
    c += [R.wait(30)]
    c += S.say("Hob", ["She did good work."])
    c += [R.wait(40)]
    c += S.narrate([
        "Beatrice, on the anvil, for once, says nothing at",
        "all."])
    c += S.narrate([
        "Roland buckles the sword on again, carefully, the",
        "way you would carry a thing back to where it lives."])
    c += [R.control_switch(db.SW_ROL4_SEEN, True)]
    c += S.companion_story(db.ROLAND)
    return c


def anvil_pages(page0):
    """Pages 2 and 3 of Beatrice (Map 6, event 4). `page0` is the prop's own
    page: a party without Roland or Hob sees only that, and either of them
    alone still reads it first where nothing else is happening."""
    looked = page0["list"][:-1]

    # -- 2: Roland, before the door. Hob is a branch.
    alone = looked + S.narrate([
        "Roland looks at the anvil for a moment, the way a",
        "swordsman looks at any forge he is standing in, and",
        "his hand goes to the sword he never uses."])
    again = S.say("Hob", [
        "Mind the edge on that. She'd",
        "want it minded."])
    with_hob = R.if_then(R.condition_switch(db.SW_ROL4_SEEN), again,
                         _the_mark())
    roland = R.if_then(R.condition_actor_in_party(db.HOB), with_hob, alone)

    # -- 3: Hob, after the door, with the sword.
    refit = S.narrate([
        "He takes the grip off. He fits the tang to a long",
        "ash haft out of the rack, and wedges it, and pins it.",
        "It takes the whole of an afternoon, and he does not",
        "talk to anybody, including the hammers."])
    refit += [R.play_se("Hammer"), R.wait(30), R.play_se("Hammer"),
              R.wait(30), R.play_se("Hammer", pitch=90), R.wait(40)]
    refit += R.script(["$gameParty.loseItem($dataWeapons[%d], 1, true);"
                       % db.WP_FAIRWEATHER])
    refit += [R.gain_weapon(db.WP_REHAFTED, 1), R.play_me("Item"),
              R.control_switch(db.SW_ROL4_REFIT, True)]
    refit += S.got(["Got \\I[99]\\C[3]Fairweather's Own, Rehafted\\C[0].",
                    "Her blade. His haft. Hob's to swing."])
    refit += S.say("Hob", ["There. Still hers. Handle's mine."])
    keep = S.say("Hob", [
        "Fair enough. It's a good sword",
        "as it is. She'd say so."])

    ask = S.narrate([
        "Hob stands at the anvil with Roland's sword across",
        "his two hands, which is where it started."])
    ask += S.say("Hob", [
        "He said take it up there. It's",
        "never been in a last room."])
    ask += S.say("Hob", [
        "I'm not a sword man. But it's",
        "hers, and it should go up with",
        "one of us."])
    ask += R.choice_block(["Let Hob refit it", "Leave it a sword"],
                          [refit, keep], cancel=1)

    swung = S.say("Hob", [
        "It swings right. She always made",
        "them to swing right."])
    no_sword = looked + S.say("Hob", [
        "He'll have left you that sword.",
        "Bring it here when you're ready."])

    hob = R.if_then(
        R.condition_switch(db.SW_ROL4_REFIT), swung,
        R.if_then(R.condition_script(HAS_SWORD), ask, no_sword))

    return [
        _like(page0, roland, {"actorValid": True, "actorId": db.ROLAND}),
        _like(page0, hob, {"actorValid": True, "actorId": db.HOB,
                           "switch1Valid": True,
                           "switch1Id": db.SW_ROLAND_GONE,
                           "switch2Valid": True,
                           "switch2Id": db.SW_ROL4_SEEN}),
    ]
