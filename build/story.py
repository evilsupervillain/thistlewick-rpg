"""Shared event-building helpers: how people talk, how doors work, and the
running gag that counts clichés.

The point of `say` is that dialogue in the map scripts reads as dialogue -
a speaker, a face, and the lines - instead of as a pile of command dicts.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import db
import mapkit as K
import rmmzdata as R

# Faces, by the person they belong to, so nobody has to remember that the
# blacksmith is Actor2 index 4.
FACES = {
    # Party members share their face sheet with their walking sprite.
    "Bram": ("Actor1", 0), "Merribell": ("Actor1", 7), "Hob": ("Actor2", 4),
    "Zephyrine": ("Actor1", 5), "Nix": ("Actor3", 4), "Aldric": ("Actor3", 6),
    "Piper": ("Actor2", 3),
    # Villagers. The stock People sheets are typecast harder than you would
    # expect - People3 is entirely royalty, so nobody in Thistlewick uses it.
    "Gatekeeper": ("People1", 2),
    "Elder Wispel": ("People1", 6),
    "Clerk": ("People2", 0),
    "Mother": ("People1", 5),
    "Villager": ("People1", 0),
    "Neighbour": ("People1", 1),
    "Councillor": ("People1", 3),
    "Councillor Fenn": ("People4", 2),
    "Old Man": ("People4", 4),
    "Farmer": ("People2", 6),
    "Fisher": ("People1", 4),
    "Child": ("People2", 2),
    "Innkeeper": ("People2", 3),
    "Merchant": ("People2", 4),
    "Apprentice": ("People2", 7),
    "Shopkeeper": ("People4", 3),
    "Regular": ("People4", 6),
    # Grimspite gets the horned, red-caped Dark Lord off the Evil sheet.
    # The Prophecy deliberately has no face: it is a document, not a person.
    "Grimspite": ("Evil", 6),
}


# A message window shows four lines. RPG Maker's own editor enforces that, and
# nothing enforces it here, so `say` and `narrate` do: anything longer is split
# into consecutive windows rather than being quietly drawn off the bottom.
MESSAGE_LINES = 4


def _pages(lines):
    lines = list(lines)
    return [lines[i:i + MESSAGE_LINES]
            for i in range(0, len(lines), MESSAGE_LINES)] or [[]]


def say(speaker, lines, *, face=True, indent=0, position=2):
    """One person saying something, over as many windows as it takes."""
    if speaker is None:
        return narrate(lines, indent=indent)
    name, index = FACES.get(speaker, ("", 0)) if face else ("", 0)
    out = []
    for page in _pages(list(lines)):
        # The speaker's name leads every window, not just the first: a long
        # speech runs over several of them and the player should not have to
        # remember who started talking four windows ago.
        page = ["\\C[6]%s:\\C[0] %s" % (speaker, page[0])] + page[1:]
        out += R.text(page, face_name=name, face_index=index,
                      position=position, indent=indent)
    return out


def narrate(lines, indent=0):
    """Screen text with nobody speaking - descriptions, and the narrator."""
    out = []
    for page in _pages(lines):
        out += R.text(page, indent=indent)
    return out


def trope(indent=0):
    """Bump the cliché counter. The ending reads the total back to the player,
    so every joke that lands on a well-worn RPG convention calls this exactly
    once - and, because it usually sits behind a self switch, only once per
    playthrough."""
    return R.control_variable_add(db.VAR_TROPES, 1, indent=indent)


def got(lines, indent=0):
    """The 'you found a thing' message, in the colour things are found in."""
    return narrate(lines, indent=indent)


# ------------------------------------------------------------------ doors ---
def door_page(target_map, tx, ty, direction=2, se="Open1"):
    """The commands behind a door sprite: open it, step through, transfer."""
    cmds = [R.play_se(se)]
    cmds += R.move_route(0, K.door_animation(), repeat=False, wait_flag=True)
    cmds += R.move_route(-1, [{"code": 12}], repeat=False, skippable=True,
                         wait_flag=True)
    cmds += [R.play_se("Move1"),
             R.transfer(target_map, tx, ty, direction, 0)]
    return cmds


def door(event_id, name, x, y, target_map, tx, ty, direction=2, sheet="!Door1",
         index=0):
    """An outward-facing door on a house wall. Player-touch, because a door
    that needs a button press on an impassable tile is fiddly."""
    return R.event(event_id, name, x, y, [R.page(
        door_page(target_map, tx, ty, direction),
        img=R.image(sheet, index, direction=2), trigger=1, priority=1)])


def exit_tile(event_id, name, x, y, target_map, tx, ty, direction=2):
    """An invisible way out of an interior - stand on it and you are outside."""
    return R.event(event_id, name, x, y, [R.page(
        [R.play_se("Move1"), R.transfer(target_map, tx, ty, direction, 0)],
        img=R.image(""), trigger=1, priority=1, through=True)])


def sign(event_id, name, x, y, lines, sheet="", index=0):
    """Something you read. No sprite by default - the scenery tile is the
    sign, and the event just sits on it."""
    return R.event(event_id, name, x, y, [R.page(
        narrate(lines), img=R.image(sheet, index, direction=2),
        trigger=0, priority=1, direction_fix=True, through=True)])


def npc(event_id, name, x, y, commands, sheet, index, direction=2,
        move_type=0, trigger=0, priority=1, step_anime=False, pages=None,
        move_speed=3, move_frequency=3):
    """A person who says something when you talk to them."""
    first = R.page(commands, img=R.image(sheet, index, direction=direction),
                   trigger=trigger, priority=priority, move_type=move_type,
                   step_anime=step_anime, move_speed=move_speed,
                   move_frequency=move_frequency)
    return R.event(event_id, name, x, y, [first] + list(pages or []))


def prop(event_id, name, x, y, lines, sheet, index, direction=2, pattern=1,
         extra=()):
    """A searchable object - a barrel, a bookshelf, a scarecrow."""
    return R.event(event_id, name, x, y, [R.page(
        narrate(lines) + list(extra),
        img=R.image(sheet, index, direction=direction, pattern=pattern),
        trigger=0, priority=1, direction_fix=True)])


def chest(event_id, name, x, y, contents, lines):
    """A treasure chest: page one gives you the thing, page two is empty."""
    open_it = [R.play_se("Open1")] + list(contents)
    open_it += got(lines)
    open_it.append(R.self_switch("A", True))
    return R.event(event_id, name, x, y, [
        R.page(open_it, img=R.image("!Chest", 0, direction=2, pattern=1),
               trigger=0, priority=1, direction_fix=True),
        R.page(narrate(["Empty. You were thorough."]),
               img=R.image("!Chest", 0, direction=2, pattern=2),
               trigger=0, priority=1, direction_fix=True,
               conditions={"selfSwitchValid": True, "selfSwitchCh": "A"}),
    ])


# -------------------------------------------------------------- recruiting ---
PARTY_LIMIT = 4      # Bram plus three


def recruit(event_id, actor_id, name, x, y, sheet, index, *, pitch, accept,
            decline, full, direction=2, move_type=0, extra_pages=(), after=()):
    """One of the six.

    The 'already joined' page is keyed on a global switch rather than a self
    switch, because the Prophecy Hall clerk can amend the roster - and a self
    switch can only be set by its own event, so nothing else could ever put
    this person back on the map."""
    sw = db.SW_RECRUIT[actor_id]

    joins = list(accept) + [
        R.change_party(actor_id, add=True, initialize=True),
        R.play_me("Item"),
    ]
    joins += R.text(["\\C[3]%s\\C[0] joined the party!" % name])
    joins += [R.control_switch(sw, True),
              R.control_variable_add(db.VAR_COMPANIONS, 1)]
    joins += list(after)

    # Whether there is room changes while the player is standing here, so this
    # is a branch inside the choice rather than a condition on the page.
    take_them = R.if_then(
        R.condition_script("$gameParty.size() < %d" % PARTY_LIMIT),
        joins, list(full))

    cmds = list(pitch) + R.choice_block(
        ["Come with me", "Not right now"], [take_them, list(decline)])

    # Once they are following you around, the copy of them standing in their
    # own kitchen has to go away - invisible, and walk-through so it stops
    # being a wall in the middle of a room.
    gone = R.page([], img=R.image(""), trigger=0, priority=1, through=True,
                  conditions={"switch1Valid": True, "switch1Id": sw})
    return R.event(event_id, name, x, y, [
        R.page(cmds, img=R.image(sheet, index, direction=direction),
               trigger=0, priority=1, move_type=move_type),
        gone] + list(extra_pages))


# ------------------------------------------------------- who is with you ----
COMPANIONS = [
    (db.MERRI, "Merribell"), (db.HOB, "Hob"), (db.ZEPH, "Zephyrine"),
    (db.NIX, "Nix"), (db.ALDRIC, "Aldric"), (db.PIPER, "Piper"),
]


def roster_amendment():
    """The Committee clerk's dismissal form. Lets the player swap a companion
    out without restarting, which matters because the whole of the first act
    is a choice of three from six."""
    branches = []
    for actor_id, nm in COMPANIONS:
        remove = [R.change_party(actor_id, add=False),
                  R.control_switch(db.SW_RECRUIT[actor_id], False),
                  R.control_variable_add(db.VAR_COMPANIONS, -1),
                  R.play_se("Cancel1")]
        remove += R.text(["\\C[3]%s\\C[0] has been struck from the roster" % nm,
                          "and has gone home to think about it."])
        not_here = say("Clerk", ["%s is not on the roster." % nm,
                                 "I cannot remove someone who is not on the",
                                 "roster. That would create a negative person."])
        branches.append(R.if_then(R.condition_actor_in_party(actor_id),
                                  remove, not_here))
    return R.choice_block([nm for _, nm in COMPANIONS], branches,
                          cancel=say("Clerk", ["Filed under 'no change'."]))
