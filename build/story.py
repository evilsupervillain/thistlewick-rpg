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
    "Corvin": ("Actor1", 4), "Wren": ("Actor2", 7), "Roland": ("Actor2", 2),
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
    # Nether Sopping. People3 is the royalty sheet, which is why the amnesiac
    # who does not know she is a princess is drawn from it, and why the two
    # "very ordinary travellers" in the corner are as well.
    "Dorcas": ("People4", 5),
    "Prudence": ("People2", 3),
    "Hosea": ("People4", 0),
    "Ysolde": ("People1", 7),
    "Hulda": ("People2", 1),
    "Nabb": ("People4", 7),
    "Tolly": ("People2", 5),
    "Merrow": ("People3", 6),
    "Dree": ("People3", 5),
    "Perpetua": ("People3", 3),
    "Pell": ("People3", 7),
    "Mrs Barrow": ("People4", 1),
    "Bother": ("People3", 4),
    # #45 is written as a man in his seventies, four stone heavier than his
    # portrait in Prophecy Hall. Every old man on the People sheets is spoken
    # for, so he shares one: People4:4, with the old man in Thistlewick square
    # forty miles north, who is the least likely of the five to be next to him
    # in a player's memory. The Hermit gave the face up to him.
    "Halbert Quy": ("People4", 4),
    "Splint": ("People2", 6),
    "Ferryman": ("People1", 4),
    "Sops": ("People2", 2),
    "Tibb": ("People1", 0),
    "Traveller": ("People3", 0),
    "Also A Traveller": ("People3", 1),
    "Hermit": ("People2", 0),
    # Meredith Crooke is drawn and fought as the same person: face
    # Actor3:1 and battler Actor3_2, which is that face in armour on the
    # side-view sheet. She used to share People2:7 with the Apprentice
    # while being fought as `Captain`, who is a man.
    "Crooke": ("Actor3", 1),
    # Ambrose Fitch and Ferrety Bother share a face: two grey-bearded old
    # men who are never in the same room, one of them being dead.
    "Ambrose": ("People3", 4),
    # Grimspite gets the horned, red-caped Dark Lord off the Evil sheet.
    # The Prophecy deliberately has no face: it is a document, not a person.
    "Grimspite": ("Evil", 6),
    # ----------------------------------------------------------- the north --
    # The People sheets are spent: People1, People2 and People4 are fully
    # allocated and People3 has one cell left. So Upper Clanging is cast out
    # of `SF_People1` and `SF_Actor3`, which between them hold thirty-two
    # faces that nothing in this game has ever used.
    #
    # Ott is the exception and is worth the share. `People2:7` has **brass
    # goggles pushed up on her head** and is the only engineer's face in the
    # entire stock library, which is not a thing you pass up for a chief
    # engineer. It is shared with the Thistlewick smithy's Apprentice, forty
    # miles and two acts away, who has one line about a hammer.
    "Ott": ("People2", 7),
    "Mrs Tunnicliffe": ("SF_People1", 7),      # white hair, spectacles, scarf
    "Mrs Cotterill": ("SF_People1", 5),        # dark braid, unbothered
    "Mr Cotterill": ("SF_People1", 4),         # moustache, work jacket
    "Spare": ("SF_People1", 0),                # a lad of nine, blue shirt
    "Sowerby": ("SF_People1", 6),              # knit cap, white beard
    "Nib": ("SF_People1", 1),                  # ponytail, red cardigan
    "Mr Kell": ("SF_People1", 2),              # black hair, blue jacket
    # The only face in either SF set with the mass to stand next to Hob.
    "Bryd": ("SF_Actor3", 0),
    # Winnie Marsden is sixty and was drawn as twenty-five. Mrs Tunnicliffe is
    # white-haired and was **born in June of the same year**, so Class of
    # 'Nineteen is sixty years back and every one of the two hundred and forty
    # is a pensioner - which is the funnier reading anyway, and the one the
    # census actually says. Nothing Winnie says implies youth, so this is a
    # recast and not a re-voicing: the lines are untouched.
    #
    # There are exactly two old women in the entire face library and both were
    # already spoken for. So she shares Ysolde's, on the Halbert Quy precedent
    # above: Nether Sopping is forty miles and an act away, and the two of them
    # will never be next to each other in a player's memory.
    "Winnie": ("People1", 7),                  # grey, and sixty, and certain
    # ---------------------------------------------------------------------
    # The Cotterills. Nine children over fifteen years and then nine years of
    # nothing, which is why the name list ran out, why the ninth is called
    # Spare, and why the tenth in the spring is a surprise. Seven of them are
    # placed around the town; Cotter, the eldest, is down the valley at the
    # big foundry and is represented here by his wife.
    #
    # `SF_People1` was spent, and Winnie's move frees exactly the face this
    # wants: Bessie is Winnie's granddaughter, so the resemblance is meant.
    # The other seven come off `SF_Actor1` and `SF_Actor2`, which nothing in
    # this game has ever used.
    "Bessie": ("SF_People1", 3),               # her grandmother, forty years on
    # Rivet was SF_Actor2:2, which is maroon hair and a soft blue shirt and
    # reads as a girl at both sizes - which makes "I have shared a bed my
    # whole life and one of them is Grommet" a different line entirely. He
    # takes SF_Actor1:0 instead: brown hair, a plain white work jacket, and
    # unmistakably a young man. It is also his brothers' and sisters' sheet,
    # so the four of them off SF_Actor1 read as related. He is the only one
    # of the nine indoors at the Safety Valve with Mr Kell, who is black hair
    # and a blue jacket, so brown-and-white is the legible choice there too.
    "Rivet": ("SF_Actor1", 0),                 # 22, day shift, Da's shadow
    "Gudgeon": ("SF_Actor1", 7),               # 20, braid and spectacles, clerk
    "Tappet": ("SF_Actor2", 3),                # 18, blue cap, drives the cart
    "Ferrule": ("SF_Actor1", 1),               # 16, long braid, in charge
    "Grommet": ("SF_Actor2", 6),               # 15, apprentice, put-upon
    "Clevis": ("SF_Actor1", 2),                # 13, red spikes, running a book
    "Shim": ("SF_Actor1", 5),                  # 11, beret and spectacles, tin
}


# A message window shows four lines. RPG Maker's own editor enforces that, and
# nothing enforces it here, so `say` and `narrate` do: anything longer is split
# into consecutive windows rather than being quietly drawn off the bottom.
MESSAGE_LINES = 4

CURRENCY = "cr"          # matches System.json, for the width of \G


def _pages(lines):
    lines = list(lines)
    return [lines[i:i + MESSAGE_LINES]
            for i in range(0, len(lines), MESSAGE_LINES)] or [[]]


def _check_width(line, face, speaker):
    """The window has no wrap and no ellipsis: a line too wide for it is drawn
    off the edge and the player never sees the end of the sentence. A face
    takes 164 of the 784 pixels, which is why a line that is fine over a
    narrator's window is not fine over a speaker's.

    This refuses to build rather than wrapping the line, because where a line
    of dialogue breaks is a decision about timing and belongs to whoever wrote
    it. `rmmzdata.wrap` is there for prose."""
    limit = R.message_width(bool(face))
    width = R.text_width(line, currency=CURRENCY)
    if width > limit:
        over = int((width - limit) / (R.FONT_SIZE / 2.0) + 0.999)
        raise ValueError(
            "%s's line is %d character(s) too wide for the message window "
            "(%d of %d px, and a face costs 164 of them). Break it earlier:\n"
            "  %r" % (speaker or "the narrator", over, width, limit, line))


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
        #
        # It leads the message rather than sitting in Show Text's `speakerName`
        # box, which would cost the line nothing. That is a decision about how
        # the game looks and not an oversight - see CLAUDE.md. When a line is
        # too wide, break the line.
        page = ["\\C[6]%s:\\C[0] %s" % (speaker, page[0])] + page[1:]
        for line in page:
            _check_width(line, name, speaker)
        out += R.text(page, face_name=name, face_index=index,
                      position=position, indent=indent)
    return out


def narrate(lines, indent=0):
    """Screen text with nobody speaking - descriptions, and the narrator."""
    out = []
    for page in _pages(lines):
        for line in page:
            _check_width(line, "", None)
        out += R.text(page, indent=indent)
    return out


def trope(indent=0):
    """Bump the cliché counter. The ending reads the total back to the player,
    so every joke that lands on a well-worn RPG convention calls this exactly
    once - and, because it usually sits behind a self switch, only once per
    playthrough."""
    return R.control_variable_add(db.VAR_TROPES, 1, indent=indent)


def blush(indent=0):
    """Bump the count of things nobody quite said.

    The companion to `trope()`, and the same discipline: bump it here and
    nowhere else, so the total can be audited with one grep. Every Register A
    moment in the game calls this exactly once, on first sight, and because it
    is a bare variable-add with no message it can be appended to any command
    list without disturbing the pacing of what is already there.

    The joke only exists in aggregate. No single line of dialogue admits to
    anything - each one is a compliment, a repair, or a census entry - and the
    ending prints the total, which is the first and only time the game lets on
    that it was counting."""
    return R.control_variable_add(db.VAR_BLUSHES, 1, indent=indent)


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
    """An invisible way out of an interior - stand on it and you are outside.

    Below characters, not same as characters: `checkEventTriggerHere` only
    starts events whose priority is *not* normal, so a player-touch tile at
    "same as characters" is one the player walks straight over. It would still
    answer the action button from the tile next to it, which is exactly what a
    door that has stopped working looks like."""
    return R.event(event_id, name, x, y, [R.page(
        [R.play_se("Move1"), R.transfer(target_map, tx, ty, direction, 0)],
        img=R.image(""), trigger=1, priority=0, through=True)])


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


def specimen(event_id, name, x, y, lines, wren_says, again,
             sheet="", index=0):
    """One of NORTH.md 3.4's three things on the road, for Wren to be correct
    about.

    Taxonomy is largely the study of how things reproduce, so a taxonomist
    doing her job out loud is a delivery system that needs no crudeness in it
    at all - she is describing a display structure, or a gravid female, and
    every word of it is the right word. She is never once aware. Bram is the
    one who cannot cope, and Bram does not speak: he is the narrator.

    The shape is the wyvern's, in a different room. The thing on the branch is
    the same thing either way, and the cataloguer is standing behind you or
    she is not - so a party without her loses nothing and is told nothing.
    `VAR_BLUSHES` counts moments, so the bump is behind a self switch and the
    second page is what you get afterwards."""
    look = narrate(lines)
    said = list(wren_says) + [blush(), R.self_switch("A", True)]
    page = dict(img=R.image(sheet, index, direction=2), trigger=0,
                priority=1, direction_fix=True, through=(sheet == ""))
    return R.event(event_id, name, x, y, [
        R.page(look + R.if_then(R.condition_actor_in_party(db.WREN), said),
               **page),
        R.page(narrate(again), conditions={"selfSwitchValid": True,
                                           "selfSwitchCh": "A"}, **page),
    ])


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
            decline, full, direction=2, move_type=0, extra_pages=(), after=(),
            again=None):
    """One of the nine.

    Three pages, because there are three states and only the middle one is
    obvious: never met, met and sent home, and currently following you around.
    The last of those is keyed on a global switch rather than a self switch,
    because a form desk can amend the roster - and a self switch can only be
    set by its own event, so nothing else could ever put this person back on
    the map.

    `again` is a dict of the same four command lists - pitch, accept, decline,
    full - for somebody who has already walked north with you and is now back
    in their own kitchen explaining it to the neighbours. Any key it leaves
    out falls back to the first-meeting version."""
    sw = db.SW_RECRUIT[actor_id]
    known = db.SW_KNOWN[actor_id]

    def joining(accept_cmds, first_time):
        """The join itself.

        `initialize` is Change Party Member's flag for `Game_Actor.setup()`,
        which puts the actor back to their database level with their database
        equipment. That is right exactly once. On a rejoin it silently deletes
        every level they earned walking north with you and every piece of kit
        you ever handed them, which is why it is set on the first join and
        never again - the actor sits in `$gameActors` the whole time they are
        at home, with everything still on it."""
        cmds = list(accept_cmds)
        cmds += [R.change_party(actor_id, add=True, initialize=first_time),
                 R.control_switch(known, True)]
        if not first_time:
            # They have had a month at home, so they come back rested. A first
            # join does not need this - `setup()` has just given them full HP
            # - but a rejoin otherwise hands you back exactly the three hit
            # points they were struck off on, and a companion who has been
            # sitting in their own kitchen since Tuesday being quietly bleeding
            # is a bug the player has no way to read as anything else. Recover
            # All on one actor works whether or not they are in the party, and
            # it clears Death, so somebody struck off unconscious wakes up.
            cmds.append(R.recover_all(actor_id))
        cmds.append(R.play_me("Item"))
        cmds += R.text(["\\C[3]%s\\C[0] %s the party!"
                        % (name, "joined" if first_time else "rejoined")])
        cmds += [R.control_switch(sw, True),
                 R.control_variable_add(db.VAR_COMPANIONS, 1)]
        cmds += list(after)
        return cmds

    def conversation(pitch_cmds, accept_cmds, decline_cmds, full_cmds,
                     first_time):
        # Whether there is room changes while the player is standing here, so
        # this is a branch inside the choice rather than a condition on the
        # page.
        take_them = R.if_then(
            R.condition_script("$gameParty.size() < %d" % PARTY_LIMIT),
            joining(accept_cmds, first_time), list(full_cmds))
        yes = "Come with me" if first_time else "Come back with me"
        return list(pitch_cmds) + R.choice_block(
            [yes, "Not right now"], [take_them, list(decline_cmds)])

    look = dict(img=R.image(sheet, index, direction=direction), trigger=0,
                priority=1, move_type=move_type)
    a = dict(again or {})

    first = R.page(conversation(pitch, accept, decline, full, True), **look)
    # Struck off the roster and back home. Everything they earned is still on
    # them, and so is everything they know about you.
    returning = R.page(
        conversation(a.get("pitch", pitch), a.get("accept", accept),
                     a.get("decline", decline), a.get("full", full), False),
        conditions={"switch1Valid": True, "switch1Id": known}, **look)

    # Once they are following you around, the copy of them standing in their
    # own kitchen has to go away - invisible, and walk-through so it stops
    # being a wall in the middle of a room. It is the last page of the three,
    # because MZ takes the highest-numbered page whose conditions hold and
    # anyone who is with you has also, necessarily, been met.
    gone = R.page([], img=R.image(""), trigger=0, priority=1, through=True,
                  conditions={"switch1Valid": True, "switch1Id": sw})
    return R.event(event_id, name, x, y,
                   [first, returning, gone] + list(extra_pages))


# ------------------------------------------------------- who is with you ----
# Two lists, because Show Choices tops out at six options in the editor and
# nine companions do not fit in one form. The Committee clerk in Thistlewick
# holds Form C-12 and can only strike off Thistlewick people; Registrar Pell in
# Nether Sopping holds Form C-12(S) and can only strike off southern ones.
# This is funnier than a submenu and it is exactly how the Committee would in
# fact have arranged it.
COMPANIONS = [
    (db.MERRI, "Merribell"), (db.HOB, "Hob"), (db.ZEPH, "Zephyrine"),
    (db.NIX, "Nix"), (db.ALDRIC, "Aldric"), (db.PIPER, "Piper"),
]

COMPANIONS_SOUTH = [
    (db.CORVIN, "Corvin"), (db.WREN, "Wren"), (db.ROLAND, "Roland"),
]


def roster_amendment(companions=None, clerk="Clerk"):
    """A dismissal form. Lets the player swap a companion out without
    restarting, which matters because the whole of the first act is a choice of
    three from what is now nine."""
    branches = []
    for actor_id, nm in (companions or COMPANIONS):
        # `SW_KNOWN` is set here as well as at the join, and the redundancy is
        # the point: anybody standing at this desk to be struck off has, by
        # definition, been in the party. `story.recruit` sets it too, but a
        # save made before these switches existed has it clear for somebody who
        # is demonstrably a companion - and a clear switch sends them back to
        # page 0, which introduces them to you all over again and re-initialises
        # them down to their database level. One command here migrates every
        # such save at the only moment it matters, without a migration.
        remove = [R.control_switch(db.SW_KNOWN[actor_id], True),
                  R.change_party(actor_id, add=False),
                  R.control_switch(db.SW_RECRUIT[actor_id], False),
                  R.control_variable_add(db.VAR_COMPANIONS, -1),
                  R.play_se("Cancel1")]
        remove += R.text(["\\C[3]%s\\C[0] has been struck from the roster" % nm,
                          "and has gone home to think about it."])
        # Said out loud because the player cannot see it in the menu: a struck
        # companion keeps their level and their kit, and gets both back the
        # moment they are re-hired. Nothing is lost by trying somebody else.
        remove += say(clerk, [
            "They keep the kit and the experience.",
            "Both are theirs. It was tried the other way",
            "once. There is a form about why not."])
        not_here = say(clerk, ["%s is not on the roster." % nm,
                               "I cannot remove someone who is not on the",
                               "roster. That would create a negative person."])
        branches.append(R.if_then(R.condition_actor_in_party(actor_id),
                                  remove, not_here))
    return R.choice_block([nm for _, nm in (companions or COMPANIONS)],
                          branches,
                          cancel=say(clerk, ["Filed under 'no change'."]))
