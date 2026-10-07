"""The whole database of The Obligatory Quest.

Seven playable characters, one class each, and enough skills that who you take
with you changes how a fight goes. Every record is upserted by id, so this file
can be re-run over an existing project without duplicating anything.

Balance notes, so the numbers are not a mystery later:
  * Physical damage is `a.atk * K - b.def * 2` with K from 3 (a cheap skill) to
    8 (a level-10 finisher). Magic is `a.mat * K - b.mdf * 2`.
  * Ordinary enemies sit at 150-500 HP and 8-30 DEF, so a party at the level the
    area expects kills a mook in one or two actions and a boss in a dozen.
  * Everyone learns their opener at level 1 and their finisher by level 10, and
    the game is paced to end around level 11-13.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mapkit as K  # noqa: F401  (sets up the path to rmmzdata)
import rmmzdata as R

# ------------------------------------------------------------------- ids ----
BRAM, MERRI, HOB, ZEPH, NIX, ALDRIC, PIPER = 1, 2, 3, 4, 5, 6, 7
CORVIN, WREN, ROLAND = 8, 9, 10          # the three found in the south
CLASSES = {BRAM: 1, MERRI: 2, HOB: 3, ZEPH: 4, NIX: 5, ALDRIC: 6, PIPER: 7,
           CORVIN: 8, WREN: 9, ROLAND: 10}

SK_ATTACK, SK_GUARD = 1, 2
# Bram
SK_TURNIP, SK_PLOT_ARMOR, SK_SECOND_WIND, SK_FRIENDSHIP, SK_DESTINED = 10, 11, 12, 13, 14
# Merribell
SK_BEDSIDE, SK_HYDRATION, SK_STERN, SK_GET_UP, SK_REST, SK_HOMILY = 20, 21, 22, 23, 24, 25
# Hob
SK_ANVIL, SK_PERCUSSIVE, SK_FULL_SWING, SK_QUENCH, SK_REFORGE = 30, 31, 32, 33, 34
# Zephyrine
SK_KINDLE, SK_FROSTBITE, SK_STATIC, SK_CONFLAGRATE, SK_METEOR, SK_MANA_SIP = 40, 41, 42, 43, 44, 45
# Nix
SK_BACKSTAB, SK_REALLOCATE, SK_TWELVE, SK_VANISH, SK_COUP = 50, 51, 52, 53, 54
# Aldric
SK_INTERPOSE, SK_OATH, SK_CHARGE, SK_RALLY, SK_CHIVALRIC = 60, 61, 62, 63, 64
# Piper
SK_BALLAD, SK_DISCORD, SK_RECAP, SK_LULLABY, SK_FINALE, SK_FORESHADOW = 70, 71, 72, 73, 74, 75
# monsters
SK_NIBBLE, SK_ROOT_GRAB, SK_SHRIEK, SK_EMBER, SK_DRAIN = 90, 91, 92, 93, 94
SK_DOOM_MONOLOGUE, SK_INEVITABILITY, SK_CLAUSE_TWELVE, SK_ERRATUM = 95, 96, 97, 98
SK_SMALL_PRINT = 99
# Corvin
SK_BROOD, SK_BLACK_EDGE, SK_OLD_WOUND, SK_OMINOUS = 100, 101, 102, 103
SK_RIVAL, SK_ALL_AT_ONCE = 104, 105
# Wren
SK_SNAP_SHOT, SK_FIELD_NOTES, SK_PIN_DOWN, SK_SPECIMEN = 110, 111, 112, 113
SK_VOLLEY, SK_DEFINITIVE = 114, 115
# Roland
SK_GUEST_APPEARANCE, SK_ENCOURAGEMENT, SK_FLOURISH, SK_PRIOR = 120, 121, 122, 123
# more monsters
SK_PINCH, SK_SWOOP, SK_GRAVE_DUTY, SK_WHATS_DONE = 130, 131, 132, 133
SK_RUMMAGE, SK_OPINION, SK_TRIBUTE = 134, 135, 136

# The north's bestiary. 137-139 are left as a gap, per NORTH.md section 9.
SK_SCALD, SK_STILL_TRYING, SK_SHED_A_PART = 140, 141, 142
SK_OVERPRESSURE, SK_DUE_NORTH, SK_MAKE_GOOD = 143, 144, 145

# items
IT_POTION, IT_HI_POTION, IT_ETHER, IT_FEATHER, IT_ANTIDOTE = 1, 2, 3, 4, 5
IT_TURNIP, IT_ELIXIR, IT_SMELLING_SALTS, IT_TONIC = 6, 7, 8, 9
IT_BISCUIT, IT_CHOWDER, IT_PALE = 10, 11, 12
IT_PROPHECY, IT_TOWER_KEY, IT_RECEIPT = 20, 21, 22
IT_JAR, IT_REPLY, IT_REFERENCE, IT_LAMP_OIL = 23, 24, 25, 26
IT_GUILD_CARD, IT_HISTORY, IT_BENCH = 27, 28, 29
# The north. Section 9 of NORTH.md allots Items 13-19, Weapons 32-36 and
# Armors 23-28 to Upper Clanging; what is taken here is the Parish Rooms
# counter, and the rest of each range is left for the works' gear and for
# whatever ITEM 1 renders down into.
IT_DRIPPING, IT_STEWED_TEA, IT_LINIMENT = 13, 14, 15
# The 20-29 key-item block is full, so the north's key items start at 30.
IT_OILSKIN_BOLTS, IT_PLATE = 30, 31
IT_ITEM_ONE = 32                # off the works inventory, and never ticked off

# weapons, roughly by class
WP_HOE, WP_SWORD, WP_BROADSWORD, WP_DESTINY = 1, 2, 3, 4
WP_CENSER, WP_STAFF, WP_HOLY_ROD = 5, 6, 7
WP_HAMMER, WP_SLEDGE, WP_WORLDBREAKER = 8, 9, 10
WP_TWIG, WP_WAND, WP_STARFALL = 11, 12, 13
WP_KNIFE, WP_DIRK, WP_LAST_WORD = 14, 15, 16
WP_LANCE, WP_HALBERD, WP_OATHKEEPER = 17, 18, 19
WP_LUTE, WP_FIDDLE, WP_LEGEND = 20, 21, 22
WP_NOTCHED, WP_GRUDGE, WP_FORETOLD = 23, 24, 25
WP_CROSSBOW, WP_RECURVE, WP_CITATION = 26, 27, 28
WP_PRACTICE, WP_FAIRWEATHER, WP_FORTY_FOURTH = 29, 30, 31
WP_WRENCH = 32
WP_NUMBER_ONE = 33              # what Ott renders ITEM 1 down into

AR_SMOCK, AR_LEATHER, AR_CHAIN, AR_PLATE, AR_ROBE, AR_SILK = 1, 2, 3, 4, 5, 6
AR_BUCKLER, AR_KITE_SHIELD, AR_HAT, AR_HELM, AR_CIRCLET = 7, 8, 9, 10, 11
AR_RING_LUCK, AR_RING_SPEED, AR_AMULET, AR_BOOTS = 12, 13, 14, 15
AR_OILSKIN, AR_A_HAT, AR_LAMP, AR_LOCKET = 16, 17, 18, 19
AR_FOOTNOTE, AR_SIGNET, AR_KIT = 20, 21, 22
AR_TROUSERS, AR_WORKS_CAP = 23, 24
AR_FUSE, AR_GOVERNOR = 25, 26   # ITEM 1's other half, and Eighty-Four's

# enemies
EN_TURNIP, EN_CROW, EN_GOBLIN, EN_BANDIT, EN_TREANT, EN_WISP = 1, 2, 3, 4, 5, 6
EN_SKELETON, EN_GARGOYLE, EN_MIMIC, EN_BAT, EN_SLIME_ISH = 7, 8, 9, 10, 11
EN_CRAB, EN_GULL, EN_SANDTHING, EN_OCCUPANT = 12, 13, 14, 15
EN_LOST_PROPERTY, EN_HOUND, EN_GRAVE_GOODS = 16, 17, 18
EN_THING, EN_GRIMSPITE, EN_PROPHECY = 20, 21, 22
EN_BADGER, EN_BIG_CRAB, EN_CROOKE, EN_FORTY_FOURTH = 23, 24, 25, 26
EN_84 = 27                      # Attempt Eighty-Four, the north's optional boss
# The 1-19 ordinary block is full, so northern encounters continue at 30.
EN_PRESSURE, EN_UNNUMBERED, EN_SALVAGE = 30, 31, 32

TR_TURNIPS, TR_CROWS, TR_GOBLINS, TR_BANDITS, TR_WOOD_MIX = 1, 2, 3, 4, 5
TR_WISPS, TR_TOWER_MIX, TR_SKELETONS, TR_GARGOYLES, TR_FIELD_MIX = 6, 7, 8, 9, 10
TR_CRABS, TR_GULLS, TR_COAST_MIX, TR_PIT_MIX = 11, 12, 13, 14
TR_BARROW_MIX, TR_WRAITHS, TR_GRAVE_GOODS = 15, 16, 17
TR_THING, TR_MIMIC, TR_GRIMSPITE, TR_PROPHECY = 20, 21, 22, 23
TR_BADGER, TR_BIG_CRAB, TR_CROOKE, TR_FORTY_FOURTH = 24, 25, 26, 27
TR_84 = 28
# The 1-19 encounter block is full, so northern groups continue at 30.
TR_PRESSURE, TR_UNNUMBERED, TR_SALVAGE, TR_CRAG_MIX = 30, 31, 32, 33

# states we add on top of the stock list
ST_DEAD, ST_SLEEP, ST_POISON = 1, 10, 4
ST_INTERPOSING, ST_INSPIRED, ST_NARRATED = 31, 32, 33
ST_BROODING, ST_CATALOGUED, ST_SLOWED = 34, 35, 36

# common events
CE_STEAL_GOLD, CE_TURNIP_EATEN = 1, 2
CE_FIT_TO_TRAVEL = 3             # MER-2's examination, run from the blank form

# switches / variables (also written down in CLAUDE.md)
SW_QUEST, SW_LEFT_VILLAGE, SW_GLOAMWOOD, SW_GRIMSPITE, SW_WON, SW_TOWER_OPEN = 1, 2, 3, 4, 5, 6
SW_RECRUIT = {MERRI: 11, HOB: 12, ZEPH: 13, NIX: 14, ALDRIC: 15, PIPER: 16,
              CORVIN: 17, WREN: 18, ROLAND: 19}
SW_MIMIC = 20

# The south. Everything from here down is optional content, and every one of
# these is a thing the player may simply never do.
SW_ROLAND_GONE = 21             # the guest star had a prior engagement
SW_FEUD_JAR, SW_FEUD_REPLY, SW_FEUD_DONE = 22, 23, 24
SW_GUILD_ASKED, SW_GUILD_FORM, SW_GUILD_MEMBER = 25, 26, 27
SW_BOUNTY_CRAB, SW_BOUNTY_CROOKE = 28, 29
SW_CRAB_PAID, SW_CROOKE_PAID = 30, 31
SW_LAMP_ASKED, SW_LAMP_LIT = 32, 33
SW_PIT_ASKED, SW_PIT_CLEARED, SW_PIT_PAID = 34, 35, 36
SW_BARROW_OPEN, SW_BARROW_BEATEN = 37, 38
SW_BENCH_ASKED, SW_BENCH_DONE = 39, 40
SW_HISTORY_ASKED, SW_HISTORY_DONE = 41, 42
SW_MET_QUY = 43                 # #45 told Bram what to ask Grimspite
SW_MET_46 = 44                  # met the man on the log in the Gloamwood
SW_SOUTH = 45                   # has been to Nether Sopping
SW_WYVERN = 46                  # knows about the goose

# The north. Upper Clanging, the Two Hundred, and the Register A retrofit
# threaded back through the rest of the game.
SW_NORTH = 47                   # has been to Upper Clanging
SW_TWO_HUNDRED_ASKED = 48       # Ott has explained what she needs
SW_OILSKIN_ASKED, SW_OILSKIN_GOT = 49, 50
SW_SPAR_ASKED, SW_SPAR_DONE = 51, 52
SW_AIRSHIP = 53                 # the Two Hundred flies; the vehicle is placed
SW_ITEM_ONE_ASKED, SW_ITEM_ONE_DOWN = 54, 55
SW_84_BEATEN, SW_84_REBUILT = 56, 57
SW_HOB_BRYD = 58                # they went for a drink. That is all
# 59 was drafted as the ask half of an ask-then-done pair and never got a
# job: NORTH.md 3.3 specifies the fete minutes as a *readable board*, and a
# board is a document and not a conversation, so there is nothing to ask and
# SW_BALLAD_DONE does all of it. It is never set and never read. Ids are not
# renumbered here, so it stays reserved; it is named as unused in System.json
# so that the next person to open the editor does not go looking for the
# event that sets it.
SW_BALLAD_ASKED, SW_BALLAD_DONE = 59, 60
SW_CENSUS = 61                  # heard about the Cold Winter
SW_COTTERILL = 62               # met the family
SW_SPARE_ASKED = 63             # the nine-year-old has applied
SW_LONG_FIELD = 64              # walked the field
SW_CLAUSE_SEVEN = 65            # Ott showed you the log; changes the finale
SW_ROOM_FOUR = 66               # room four at the Wyvern
SW_GERALD = 67                  # that is all that is being said about Gerald
# Appended after NORTH.md section 10 was written, for the reason recorded at
# the Clause Seven event in `field.py`: the log entry in 5.4 says REACHED THE
# TOWER, and nothing else in the game knows whether the Two Hundred ever did.
SW_TWO_HUNDRED_FLEW = 68        # set down beside the tower, out of the air
# The retrofit of NORTH.md section 3. Two Very Ordinary Travellers are one
# joke with two mouths, and either of them can be asked first, so the bump
# cannot hang off a self switch the way every other guarded blush does - a
# self switch is keyed on (map, event id, letter) and these are two events.
SW_TRAVELLERS = 69              # they have been asked how long they have known
                                # each other, by whichever of them you asked
# Ott's last beat before you go north asks you to carry a question to the
# only other person alive who has had four thousand years to look at that
# tower. It has to be its own switch: the beat sits six deep in her flying
# chain, so `SW_AIRSHIP` says the ship exists and says nothing at all about
# whether she got round to asking.
SW_OTT_MATERIALS = 70           # Ott asked you to ask him what it is made of
# NORTH.md 7, the stretch goal. The crate is the one thing in the game a
# player can spend two ways - Ott renders it down into the north's best gear,
# or you carry it up the tower and light it - and the ending is the only place
# that ever mentions which. `SW_ITEM_ONE_DOWN` says it came off the crag and
# says nothing about where it went.
SW_ITEM_ONE_USED = 71           # it was set down in front of the throne
# The roster is amendable, so a companion can be recruited, sent home from a
# form desk, and taken on again - and three different things need to know
# which of those has happened. `SW_RECRUIT` means "is walking behind you right
# now" and is switched off the moment the clerk strikes them off. These mean
# "has walked behind you at some point", and are never switched off again.
#
# They pay for two fixes and one joke. Change Party Member's *initialise* flag
# calls `Game_Actor.setup()`, which puts the actor back to their database level
# with their database equipment - so re-hiring somebody used to throw away
# every level they had earned and every thing you had ever given them. The
# rejoin branch only initialises on a first join, and this is how it knows.
# And an event page keyed on one of these is a person who does not introduce
# themselves to somebody they have already been north with.
SW_KNOWN = {MERRI: 72, HOB: 73, ZEPH: 74, NIX: 75, ALDRIC: 76, PIPER: 77,
            CORVIN: 78, WREN: 79, ROLAND: 80}

VAR_COMPANIONS, VAR_TROPES, VAR_TURNIPS = 1, 2, 3
VAR_TALES, VAR_BOUNTIES = 4, 5
VAR_PLAQUES = 6                 # wreck plaques read; Ott opens up at twelve
VAR_BLUSHES = 7                 # "things nobody quite said" - see story.blush
VAR_OTT_ORDER, VAR_OTT_FLYING = 8, 9    # Ott's stage-2 and stage-3 beat chains
# 10 is a scratch variable owned by build_game.py, not a counter.

# ------------------------------------------------------ Firstfield Meadow ----
# Map 28, the optional tutorial west of the village, in `meadow.py`. It takes
# fresh blocks rather than the free ends of the north's, because SPARE.md has
# already spoken for those (Enemy 28, Troop 29, Weapon 34, Armor 27, Items
# 33-34, Skills 146-155).
SW_FF_ARRIVED = 81              # Fizz has said HEY
SW_FF_STICK = 82                # Old Hollis has handed over a stick
SW_FF_SHEEP_ASKED = 83          # Dilys has lost her sheep, officially
SW_FF_SHEEP_DONE = 84           # and they have been found, where they were
SW_FF_CHEST = 85                # the most-opened chest in the world
SW_FF_NORBERT = 86              # Norbert has lost, as contracted
SW_FF_GRADUATED = 87            # the first completed tutorial on record
VAR_FF_STATIONS = 11            # stations done, of four; Fizz graduates you at four
VAR_FF_SHEEP = 12               # sheep found, of three
VAR_FF_SIGNS = 13               # signs read, which is how Fizz varies her line
VAR_TOBY = 14                   # which of his fourteen Toby did last; see gladhollow.py
# The Former Premises, SITES.md step 6. Set on Map 42 and read by a page on
# Grimspite at the top of the tower, Map 12, so it cannot be a self switch.
SW_VISITORS_BOOK = 88           # Hollowell has asked for the incumbent's signature

# ------------------------------------------------------- companion quests ----
# COMPANIONS.md is the design and QUESTS.md the queue; its 0.6 reserves these
# blocks, and each step takes the next free id in them. The quests' events
# are in `build/q_<name>.py`, one module per companion.
#
# One story switch per companion, set by whichever of their quests is finished
# first and never cleared - the ending reads one block per companion off
# these, not one per quest (COMPANIONS.md 1.4). Same last digit as SW_RECRUIT
# and SW_KNOWN. Set them with `story.companion_story` and nowhere else: it is
# also what counts VAR_COMPANION_STORIES.
SW_STORY = {MERRI: 101, HOB: 102, ZEPH: 103, NIX: 104, ALDRIC: 105,
            PIPER: 106, CORVIN: 107, WREN: 108, ROLAND: 109}
VAR_COMPANION_STORIES = 15      # how many of SW_STORY are on
# WRE-2, the second plaque (QUESTS.md A1, q_wren.py)
SW_WRE2_ASKED = 111             # Dorcas has agreed to brass, read by her first
SW_WRE2_UP = 112                # and it is up, on the other side of the fire
IT_BRASS_PLATE = 40
# WRE-5, Bramus (QUESTS.md A2, q_wren.py). Its own switch as well as
# SW_STORY[WREN], so the ending can tell which of her quests was done.
SW_WRE5_NAMED = 113             # the thing in the turnips has a name
# PIP-2, a rhyme for turnip (QUESTS.md A3, q_piper.py)
SW_PIP2_DONE = 114              # the ballad has its last verse
# MER-2, fit to travel (QUESTS.md A4, q_merribell.py). The lamp is SW_LAMP_LIT.
SW_MER2_ASKED = 115             # clause eleven found; the blank form taken
SW_MER2_SCALES = 116            # the fish stall has lent its scales
SW_MER2_DONE = 117              # certified
VAR_MER2_WITNESS = 16           # actor id of whoever witnessed it
IT_FITNESS_FORM, IT_SCALES, IT_CERTIFICATE = 41, 42, 43
# ROL-4, the maker's mark (QUESTS.md A5, q_roland.py)
SW_ROL4_SEEN = 118              # Hob has seen the mark on Roland's sword
SW_ROL4_REFIT = 119             # and put the blade on a haft of his own
WP_REHAFTED = 40                # Fairweather's Own, as an axe
# HOB-5, two smiths, one forge (QUESTS.md A6, q_hob.py)
SW_HOB5_FORGED = 120            # the tube plate is made, and is being carried
SW_HOB5_DONE = 121              # Ott has said it will do
IT_TUBE_PLATE = 44
# ZEPH-5, the lay-by (QUESTS.md A7, q_zephyrine.py)
SW_ZEPH5_DONE = 122             # the association has shown her page 23
SK_PAGE_23 = 46                 # Kindle, as worked out without the page
# MER-4, the man who cannot stay down (QUESTS.md A7, q_merribell.py)
SW_MER4_TOLD = 123              # she has refused him, and he has paid
SW_MER4_DONE = 124              # and they have left, which is the cure
# HOB-3, the anvil (QUESTS.md A8, q_hob.py)
SW_HOB3_GONE = 125              # the anvil is out on the grass; off again after
SW_HOB3_DONE = 126              # and back, to the inch
IT_APOLOGY = 45
# NIX-4, the longest loan (QUESTS.md A9, q_nix.py)
SW_NIX4_BEGUN = 127             # the eleven are out of the Emporium
SW_NIX4_DONE = 128              # and back, and the ledger ruled off
VAR_NIX4_RETURNED = 17          # how many of the eleven have gone home
IT_RETURNS, IT_PARCEL = 46, 47
# NIX-5, half an encounter (QUESTS.md A10, q_nix.py)
SW_NIX5_ON = 129                # Mr Bagshawe is being taken through; ends
SW_NIX5_DONE = 130              # and he was, without a fight
VAR_NIX5_BATTLES = 18           # battleCount() when the escort set out
# WRE-3, the thing in the Gloamwood (QUESTS.md A11, q_wren.py)
SW_WRE3_WALK = 131              # the society is out on its walk; ends
SW_WRE3_DONE = 132              # and the Thing is proved not to exist
AR_SOCIETY_BADGE = 40           # Wren's gear (QUESTS.md 0.5): only she wears it
AT_BADGE = 7                    # an armour type of its own, for that
# PIP-5, the struck verses (QUESTS.md A12, q_piper.py)
SW_PIP5_ASKED = 133             # Piper knows there is a box
SW_PIP5_SIGNED = 134            # Form S-7, countersigned on the wording
SW_PIP5_KEY = 135               # the key, lifted while Fenn was listened to
SW_PIP5_DONE = 136              # and the box opened, and shut again
VAR_PIP5_DECOY = 19             # actor id of whoever asked Fenn about clause 12
IT_FORM_S7, IT_ARCHIVE_KEY = 48, 49
# HOB-2, the grave he has not made (QUESTS.md A13, q_hob.py)
SW_HOB2_ON = 137                # Beatrice has gone quiet; off again after
SW_HOB2_CARRYING = 138          # an attempt is on its way to the churchyard
SW_HOB2_DONE = 139              # the gate is hung, and she has views on it
VAR_HOB2_TRY = 20               # attempts made, of four
WP_SOMETHING_TO_SAY = 41        # Hob's gear (QUESTS.md 0.5)
# ROL-3, the alumni (QUESTS.md A14, q_roland.py)
SW_ROL3_DINNER = 140            # the eleven are in the Slain Wyvern; ends
SW_ROL3_DONE = 141              # and have drunk to him
VAR_ROL3_HEARD = 21             # how many of the eleven have been spoken to
# HOB-1, the Assize of Hammers (QUESTS.md B1, q_hob.py)
SW_HOB1_ON = 142                # the retrieval tour is on
SW_HOB1_PICKS = 143             # Nix has been asked for the lockpicks
SW_HOB1_DONE = 144              # Beatrice examined, and disqualified
VAR_HOB1_ASKED = 22             # owners asked, of eleven
IT_WARDENS_NOTES = 50
# ALD-4, the horse (QUESTS.md B2, q_aldric.py)
SW_ALD4_DONE = 145              # Duchess and her knight; she stays
# PIP-3, the contest at the Sign of the Bell (QUESTS.md B3, q_piper.py)
SW_PIP3_ON = 146                # entered; the rival acts are in the Bell; ends
SW_PIP3_DONE = 147              # second place, framed
AR_ROSETTE = 41                 # Piper's gear (QUESTS.md 0.5): only she wears it
AT_ROSETTE = 8                  # an armour type of its own, as AT_BADGE is
EN_DRAY, EN_MOON, EN_BACK_TABLE = 41, 42, 43
TR_CONTEST = 41
SK_HECKLE, SK_TALK_THROUGH, SK_SERPENT, SK_SAD_VERSE, SK_ENCORE = (
    170, 171, 172, 173, 174)
# COR-5, the appraisal (QUESTS.md B4, q_corvin.py)
SW_COR5_DONE = 148              # no curse on it; the form is on offer
ST_CURSED = 40                  # Cursed (Elective): optional, and comes off
# NIX-1, the client identifies themselves (QUESTS.md B5, q_nix.py)
SW_NIX1_LETTER = 149            # the parcel opened: the client is Nix at fifteen
SW_NIX1_DONE = 150              # the coat out of bond, and it fits
IT_BOND_TICKET = 51
AR_GRANS_COAT = 42              # Nix's gear (QUESTS.md 0.5): only Nix wears it
AT_COAT = 9                     # an armour type of its own, as AT_BADGE is
# NIX-2, the sealed counting house (QUESTS.md B6, q_nix.py)
SW_NIX2_OPEN = 151              # the Door is open, informally; Form L is not
SW_NIX2_DONE = 152              # the chair, the note, and the change
# ROL-1, the appointment (QUESTS.md B7, q_roland.py)
SW_ROL1_ON = 153                # the review meeting is sitting in the Bell; ends
SW_ROL1_DONE = 154              # and has sat: the minutes
IT_MINUTES = 52
# ZEPH-1, the fines (QUESTS.md C1, q_zephyrine.py)
SW_ZEPH1_ON = 155               # the eleventh notice has been read
SW_ZEPH1_TOLD = 156             # there was no expulsion; purse, or draft
SW_ZEPH1_PAID = 157             # the purse turned out: in good standing
SW_ZEPH1_EXPELLED = 158         # the draft filed, at her own request
SW_ZEPH1_DONE = 159             # either of those two
VAR_ZEPH1_PAID = 23             # crowns turned out on the Library desk
IT_FINES_NOTICE = 53
AR_COLLEGIUM_ROBE = 43          # Zephyrine's gear (QUESTS.md 0.5): hers alone
AT_ROBE = 10                    # an armour type of its own, as AT_BADGE is
# ZEPH-3, Dean Fenwold is fine (QUESTS.md C2, q_zephyrine.py)
SW_ZEPH3_DONE = 160             # the demonstration; the room was wrong
# ZEPH-2, the duck (QUESTS.md C3, q_zephyrine.py)
SW_ZEPH2_ON = 161               # inquorate: the twelfth Fellow is a duck
SW_ZEPH2_WALKING = 162          # the duck is out of its pond; ends
SW_ZEPH2_DONE = 163             # quorate; carried; the proxy is hers
IT_DUCK, IT_PROXY = 54, 55
# WRE-1, the monograph (QUESTS.md C4, q_wren.py)
SW_WRE1_ON = 164                # the Library's rules for a monograph, read
SW_WRE1_MOTT = 165              # reviewed: Professor Mott
SW_WRE1_FURZE = 166             # reviewed: Dr Furze
SW_WRE1_DUCK_DUE = 167          # two reviews in; the duck's is due; ends
SW_WRE1_DUCK = 168              # reviewed: the Honorary Fellow
SW_WRE1_DONE = 169              # published, in the inch-wide gap
VAR_WRE1_SPECIMENS = 24         # type specimens measured, of eleven
IT_SUBSCRIPTIONS = list(range(56, 64))   # eight names on the list
IT_MONOGRAPH = 64
CL_WREN_PUBLISHED = 11          # her class, plus the upgrade (see below)
EN_SPECIMENS = list(range(44, 55))       # the eleven type specimens
TR_SPECIMENS = list(range(42, 53))       # one troop each
SK_STARTLE, SK_BOLT, SK_BITE_NOTES, SK_NOT_THERE = 175, 176, 177, 178
# COR-1, Ashcombe (New) (QUESTS.md D1, q_corvin.py)
SW_COR1_ON = 170                # his name on the Roll: Away. Today, then
SW_COR1_HOME = 171              # through his mother's door, and the tea
SW_COR1_DONE = 172              # the speech, which went well; the scarf
IT_INVITATION = 65              # the eleventh, never posted
AR_SCARF = 44                   # Corvin's gear (QUESTS.md 0.5): his alone
AT_SCARF = 11                   # an armour type of its own, as AT_BADGE is
# COR-2, Ashcombe (Old) (QUESTS.md D2, q_corvin.py)
SW_COR2_STEP = 173              # sat on the doorstep; the sword's name read
SW_COR2_DONE = 174              # the report card, out of the strongbox
IT_REPORT_CARD = 66
# MER-5, The Well at Sump (QUESTS.md E1, q_merribell.py)
SW_MER5_ON = 175                # the Water Committee re-formed; wasps
SW_MER5_DONE = 176              # the curse lifted; item three carried
IT_JAM = 67                     # Mrs Pardew's gran's gooseberry, 1931
# MER-1, The Sisterhouse (QUESTS.md E2, q_merribell.py)
SW_MER1_ON = 177                # the queue instead of the symposium
SW_MER1_DONE = 178              # Whatever Works, on points; the Pamphlet
VAR_MER1_POINTS = 25            # Whatever Works' score, of twenty
AR_PAMPHLET = 45                # Merribell's gear (QUESTS.md 0.5): hers alone
AT_PAMPHLET = 12                # an armour type of its own, as AT_BADGE is
# MER-3, The Healers' Table (QUESTS.md E3, q_merribell.py)
SW_MER3_ON = 179                # the Table is sitting; she is on the list
SW_MER3_DONE = 180              # write it down; the Table's Kit
AR_TABLE_KIT = 46               # anybody's: an accessory of the general type
# ALD-3, The Chapter House (QUESTS.md E4, q_aldric.py)
SW_ALD3_DONE = 181              # the pin goes with the knight: At Large
# ALD-1, The Errand (QUESTS.md E5, q_aldric.py)
SW_ALD1_DONE = 182              # the letter delivered, nine years late
IT_ALD1_LETTER = 68             # TO THE PARISH OF LITTLE GORE. BY HAND.
# ALD-5, Pemberton-Gore the Fourth (QUESTS.md E6, q_aldric.py)
SW_ALD5_DONE = 183              # three paces behind; and the gate, found
# ALD-2, The Vigil (QUESTS.md E7, q_aldric.py, db.build_vigil)
SW_ALD2_DONE = 184              # dusk to dawn, in the right chapel: confirmed
AR_REGARDANT = 47               # Aldric's gear (QUESTS.md 0.5): his alone
AT_ESCUTCHEON = 13              # an armour type of its own, as AT_BADGE is
ST_VIGIL = 41                   # keeping vigil: does not move, draws everything
EN_DAMP, EN_SMALL_HOURS, EN_TEMPTATION, EN_LIGHT = 55, 56, 57, 58
TR_VIGIL = 53
SK_SEEPS_IN, SK_SIT_DOWN, SK_HOW_LATE, SK_THIS_WAY = 179, 180, 181, 182
VIGIL_DAWN = 5                  # the turn at whose end it is light
# ALD-6, The Wrong Dragon (QUESTS.md E8, q_aldric.py)
SW_ALD6_DONE = 185              # the cave lit; read to; the commission reported
# WRE-4, The Cabinet (QUESTS.md E9, q_wren.py)
SW_WRE4_ON = 186                # engaged to authenticate the collection
SW_WRE4_JOINS = 187             # Mr Ottershaw has shown her every join
SW_WRE4_DONE = 188              # written up, honestly; the fee
WRE4_FEE = 600                  # crowns, the family's, for the write-up
# COR-3, The Rivals' Retreat (QUESTS.md E10, q_corvin.py)
SW_COR3_ON = 189                # seventeenth, of seventeen; he sat down
SW_COR3_DONE = 190              # the meeting; second; his chair is kept
# COR-4, Mother Selvidge (QUESTS.md E11, q_corvin.py)
SW_COR4_DONE = 191              # three readings; four young men a year
# PIP-4, The Elegy (QUESTS.md E12, q_piper.py)
SW_PIP4_ON = 192                # commissioned; the interviews; ends
SW_PIP4_DONE = 193              # nine lines, pinned up, not performed
VAR_PIP4_HEARD = 26             # accounts of Abel Thrush, of eleven
IT_ELEGY = 69                   # Piper's copy
# PIP-1, The Authorised Version (QUESTS.md E13, q_piper.py)
SW_PIP1_ON = 194                # Ambrosine has read it to us; the choice
SW_PIP1_GOOD = 195              # ending: it is very good; one footnote
SW_PIP1_FIXED = 196             # ending: fixed, in metre; A. & P. Quill
SW_PIP1_DONE = 197              # either ending
IT_AUTHORISED = 70              # the Authorised Version, a copy
# NIX-3, Professional Courtesy (QUESTS.md E14, q_nix.py)
SW_NIX3_ON = 198                # Lorrimer's challenge; the list; ends
SW_NIX3_DONE = 199              # won on paperwork; a Dark Lord signed for
VAR_NIX3_LOCATED = 27           # the list's three things, with receipts
AR_LORRIMER_TOOLS = 48          # anybody's: left on a barrel, in a huff
# HOB-4, The Sky Anvil (QUESTS.md E15, q_hob.py)
SW_HOB4_TRADED = 200            # a gate out of eleven; the gatepost traded
SW_HOB4_DONE = 201              # one sword, and he will not say who for
IT_STAR_IRON = 71               # the Sky Anvil, under one arm
WP_STAR_IRON = 42               # the one thing it makes; not for Hob
# ZEPH-4, The Cinder Fen (QUESTS.md E16, q_zephyrine.py)
SW_ZEPH4_DONE = 202             # nine hundred acres, sanctioned; the road dry
IT_FEN_CERTIFICATE = 72         # the Commissioner's; countersigned by scorch
# ROL-5, The Understudy (QUESTS.md E17, q_roland.py)
SW_ROL5_ON = 203                # met her; he is deciding whether to tell her
SW_ROL5_DONE = 204              # told; she asked whose; she has gone north
# ROL-2, Roland's Own Quest (QUESTS.md E18, q_roland.py)
SW_ROL2_ON = 205                # going to see: the card says GONE TO SEE
SW_ROL2_DRAWN = 206             # the sword is out of the stone
SW_ROL2_DONE = 207              # the Worm of Carn Drey is ended; discharged
WP_DRAWN = 43                   # out of the stone; he leaves it at the door
EN_WORM = 59
TR_WORM = 54
SK_COILS, SK_LOOKS_AT_HIM = 183, 184

# --------------------------------------------------------------- Spare ----
# The tenth companion and the secret one (SPARE.md; QUESTS.md F1, q_spare.py,
# db.build_spare). His ids are the ones SPARE.md reserved, except the class -
# WRE-1 took 11 - and the switches, which SW_KNOWN took (QUESTS.md 0.3).
SPARE = 11
CLASSES[SPARE] = 12             # The Ninth
SW_SPARE_FORM = 89              # Gudgeon has issued Form P-9
SW_SPARE_JOINED = SW_RECRUIT[SPARE] = 90        # he is coming
SW_SPARE_REFUSED = 91           # the argument has been lost at least once
SW_SPARE_KNOWN = SW_KNOWN[SPARE] = 92           # never goes off
SW_SPARE_STORY = SW_STORY[SPARE] = 110          # story.companion_story's
# He is in those three tables for their names and for companion_story, and
# deliberately **not** in story.COMPANIONS: no form desk can strike him off,
# because he was never on the roster (SPARE.md 7).
IT_FORM_P9, IT_WASHER = 33, 34
WP_BAG = 34                     # A Bag, Packed
AR_WASHER = 27                  # A Washer, Off Shim, once he is wearing it
WT_BAG = 13                     # a weapon type of his own
AT_WASHER = 14                  # an armour type of his own, as AT_BADGE is
SK_YOU_ARE_NINE, SK_ASK_YOUR_FATHER, SK_NOT_THE_POINT, SK_SAID_NO = (
    146, 147, 148, 149)
SK_SMALL_ENOUGH, SK_TANTRUM, SK_HAVE_A_BAG = 150, 151, 152
SK_NEVER_HIT_ME, SK_NINETY_TUBES, SK_THE_DRAWING = 153, 154, 155
ST_NEVER_HIT, ST_BRUSHED = 42, 43
EN_MAM = 28
TR_MAM = 29                     # A Discussion With Mam
CE_TANTRUM = 4                  # what Temper Tantrum costs him
# SPA-1, The Letters (QUESTS.md F2, q_spare.py)
SW_SPA1_DONE = 208              # read out at the dinner hour; no dragon
SW_SPA1_DINNER = 209            # the dinner hour, while it is on
VAR_SPA1_POSTED = 28            # letters posted, of eight
VAR_SPA1_ORDER = 29             # digit i: which letter went from town i
IT_SPA1_COPIES = 73             # his copies, in pencil
CE_SPA1_COPIES = 5              # reading them, from the menu
# SPA-4, The Pen Pal (QUESTS.md F3, q_spare.py; the village is pottering.py)
SW_SPA4_DONE = 210              # met, shown round, and written to by hand
VAR_SPA4_TOUR = 30              # Effie's tour: 1 volcano, 2 serpent, 3 post
# SPA-2, Ninety Tubes (QUESTS.md F4, q_spare.py; Cotter is dunnage.py's)
SW_SPA2_ASKED = 211             # Cotter has asked; the short ask from now on
SW_SPA2_CLEARED = 212           # the paddle is clear; out by the ladder
SW_SPA2_DONE = 213              # out, and everybody was there
VAR_SPA2_PARTY = 31             # the party, set aside while he is in alone
# P1, the playtest round (QUESTS.md Part G): NIX-5's escort is care, not luck
IT_MOTHBALLS = 74               # a twist of them; sold in shops
ST_MOTHBALLS = 44               # Encounter None, for so many steps
CE_MOTHBALLS = 6                # using one: the state, or still airing
VAR_MOTHBALLS = 32              # $gameParty.steps() when one was last used
MOTHBALL_STEPS = 50             # see build_mothballs for the arithmetic
MOTHBALL_AIRING = 25            # steps after it wears off before another
SPARE_ARGUING_LEVEL = 12        # fixed, so the argument is tuned once

AR_STICK, AR_STRAIGHTER_STICK, AR_CERTIFICATE = 30, 31, 32
SK_TELEGRAPH, SK_ENORMOUS_SWING = 160, 161
EN_NORBERT = 40
TR_NORBERT = 40

# element ids, from System.json
EL_PHYSICAL, EL_FIRE, EL_ICE, EL_THUNDER, EL_WATER = 1, 2, 3, 4, 5
EL_EARTH, EL_WIND, EL_LIGHT, EL_DARK = 6, 7, 8, 9
EL_TEMPER = 10                  # Spare's tantrum; his mother is immune

# skill types / equip types / armor types, also from System.json
STYPE_MAGIC, STYPE_SPECIAL = 1, 2
ET_WEAPON, ET_SHIELD, ET_HEAD, ET_BODY, ET_ACCESSORY = 1, 2, 3, 4, 5
AT_GENERAL, AT_MAGIC, AT_LIGHT, AT_HEAVY, AT_SMALL_SHIELD, AT_LARGE_SHIELD = 1, 2, 3, 4, 5, 6
WT_DAGGER, WT_SWORD, WT_FLAIL, WT_AXE, WT_WHIP, WT_STAFF = 1, 2, 3, 4, 5, 6
WT_BOW, WT_CROSSBOW, WT_GUN, WT_CLAW, WT_GLOVE, WT_SPEAR = 7, 8, 9, 10, 11, 12


# ------------------------------------------------------------- utilities ----
def upsert(records, entry):
    """Put a record at its own id, padding the list if it has to.

    The id ranges here are deliberately gappy - skills 20-29 are Merribell's
    whether or not she has ten of them - so the gaps get filled with the same
    empty records the editor writes when you raise a list's maximum. A `null`
    in the middle of a list crashes the editor and the validator; an empty
    record is just an unused row."""
    while len(records) <= entry["id"]:
        records.append(None)
    records[entry["id"]] = entry
    return records


BLANKS = {
    "Skills.json": lambda i: {
        "id": i, "animationId": 0, "description": "", "effects": [],
        "damage": {"critical": False, "elementId": 0, "formula": "0",
                   "type": 0, "variance": 20},
        "hitType": 0, "iconIndex": 0, "message1": "", "message2": "",
        "messageType": 1, "mpCost": 0, "name": "", "note": "", "occasion": 0,
        "repeats": 1, "requiredWtypeId1": 0, "requiredWtypeId2": 0, "scope": 1,
        "speed": 0, "stypeId": 1, "successRate": 100, "tpCost": 0, "tpGain": 0},
    "Items.json": lambda i: {
        "id": i, "animationId": 0, "consumable": True, "description": "",
        "damage": {"critical": False, "elementId": 0, "formula": "0",
                   "type": 0, "variance": 20},
        "effects": [], "hitType": 0, "iconIndex": 0, "itypeId": 1, "name": "",
        "note": "", "occasion": 0, "price": 0, "repeats": 1, "scope": 7,
        "speed": 0, "successRate": 100, "tpGain": 0},
    "States.json": lambda i: {
        "id": i, "autoRemovalTiming": 0, "chanceByDamage": 100, "traits": [],
        "iconIndex": 0, "maxTurns": 1, "message1": "", "message2": "",
        "message3": "", "message4": "", "messageType": 1, "minTurns": 1,
        "motion": 0, "name": "", "note": "", "overlay": 0, "priority": 50,
        "removeAtBattleEnd": False, "removeByDamage": False,
        "removeByRestriction": False, "removeByWalking": False,
        "restriction": 0, "stepsToRemove": 100},
    "Enemies.json": lambda i: {
        "id": i, "actions": [], "battlerHue": 0, "battlerName": "",
        "dropItems": [], "exp": 0, "traits": [], "gold": 0, "name": "",
        "note": "", "params": [1, 0, 1, 1, 1, 1, 1, 1]},
    "Troops.json": lambda i: {
        "id": i, "members": [], "name": "",
        "pages": [{"conditions": dict(BLANK_TROOP_CONDITIONS),
                   "list": [{"code": 0, "indent": 0, "parameters": []}],
                   "span": 0}]},
    "Weapons.json": lambda i: {
        "id": i, "animationId": 0, "description": "", "etypeId": 1,
        "traits": [], "iconIndex": 0, "name": "", "note": "",
        "params": [0] * 8, "price": 0, "wtypeId": 0},
    "Armors.json": lambda i: {
        "id": i, "atypeId": 0, "description": "", "etypeId": 1, "traits": [],
        "iconIndex": 0, "name": "", "note": "", "params": [0] * 8, "price": 0},
    "CommonEvents.json": lambda i: {
        "id": i, "list": [{"code": 0, "indent": 0, "parameters": []}],
        "name": "", "switchId": 1, "trigger": 0},
}


def save(name, records):
    """Write a list file, replacing any hole left by a gappy id range with the
    empty record the editor would have put there."""
    blank = BLANKS.get(name)
    if blank:
        records = [r if r is not None or i == 0 else blank(i)
                   for i, r in enumerate(records)]
    R.save_list(name, records)


def curve(base, growth, accel=1.0):
    """One value per level, index 0 unused, 100 entries - the shape MZ stores.
    `accel` bends the curve upward at high level so late levels still feel
    like something."""
    out = [0]
    for lv in range(1, 100):
        t = (lv - 1) / 98.0
        out.append(int(round(base + growth * (lv - 1) * (1.0 + accel * t))))
    return out


def params(hp, mp, atk, dfn, mat, mdf, agi, luk, accel=0.9):
    """Eight curves from eight (base, growth) pairs."""
    return [curve(b, g, accel) for b, g in
            (hp, mp, atk, dfn, mat, mdf, agi, luk)]


def trait(code, data_id, value):
    return {"code": code, "dataId": data_id, "value": value}


def effect(code, data_id=0, value1=0, value2=0):
    return {"code": code, "dataId": data_id, "value1": value1, "value2": value2}


def described(text):
    """Break a description across the two lines the help window shows.

    Window_Help draws each line at the window's full width and clips whatever
    runs past it, so a description written as one long string quietly loses its
    ending. Descriptions are prose, so a machine may break them; dialogue is
    not wrapped this way, because there the line breaks are the timing."""
    lines = R.wrap(text, R.HELP_WIDTH)
    if len(lines) > 2:
        raise ValueError("description needs %d lines and the help window shows "
                         "2: %r" % (len(lines), text))
    return "\n".join(lines)


def skill(sid, name, desc, formula, *, stype=STYPE_SPECIAL, scope=1, mp=0, tp=0,
          tp_gain=8, animation=1, icon=76, element=-1, hit_type=1, dmg_type=1,
          effects=(), critical=False, variance=20, message="%1 uses %2!",
          occasion=1, repeats=1, success=100, speed=0):
    return {
        "id": sid, "name": name, "note": "", "description": described(desc),
        "animationId": animation, "iconIndex": icon, "stypeId": stype,
        "scope": scope, "occasion": occasion, "hitType": hit_type,
        "mpCost": mp, "tpCost": tp, "tpGain": tp_gain, "speed": speed,
        "successRate": success, "repeats": repeats,
        "requiredWtypeId1": 0, "requiredWtypeId2": 0,
        "message1": message, "message2": "", "messageType": 1,
        "damage": {"critical": critical, "elementId": element, "type": dmg_type,
                   "variance": variance, "formula": formula},
        "effects": list(effects),
    }


def item(iid, name, desc, *, price=0, icon=176, itype=1, scope=7, consumable=True,
         effects=(), animation=41, occasion=0, formula="0", dmg_type=0,
         element=0, hit_type=0):
    return {
        "id": iid, "name": name, "note": "", "description": described(desc),
        "animationId": animation, "iconIndex": icon, "itypeId": itype,
        "price": price, "consumable": consumable, "scope": scope,
        "occasion": occasion, "hitType": hit_type, "speed": 0,
        "successRate": 100, "repeats": 1, "tpGain": 0,
        "damage": {"critical": False, "elementId": element, "formula": formula,
                   "type": dmg_type, "variance": 20},
        "effects": list(effects),
    }


def weapon(wid, name, desc, wtype, price, stats, traits=(), icon=97, animation=6):
    return {"id": wid, "name": name, "note": "", "description": described(desc),
            "animationId": animation, "iconIndex": icon, "etypeId": ET_WEAPON,
            "wtypeId": wtype, "price": price, "params": list(stats),
            "traits": list(traits)}


def armor(aid, name, desc, etype, atype, price, stats, traits=(), icon=131):
    return {"id": aid, "name": name, "note": "", "description": described(desc),
            "iconIndex": icon, "etypeId": etype, "atypeId": atype,
            "price": price, "params": list(stats), "traits": list(traits)}


def action(skill_id, rating=5, condition=0, p1=0, p2=0):
    return {"skillId": skill_id, "rating": rating, "conditionType": condition,
            "conditionParam1": p1, "conditionParam2": p2}


def drop(kind=0, data_id=0, denominator=1):
    return {"kind": kind, "dataId": data_id, "denominator": denominator}


NO_DROP = drop()


def enemy(eid, name, battler, hue, stats, exp, gold, actions, traits=(),
          drops=(), note=""):
    ds = list(drops) + [NO_DROP, NO_DROP, NO_DROP]
    return {"id": eid, "name": name, "note": note, "battlerName": battler,
            "battlerHue": hue, "params": list(stats), "exp": exp, "gold": gold,
            "actions": list(actions), "dropItems": ds[:3], "traits": list(traits)}


BLANK_TROOP_CONDITIONS = {
    "actorHp": 50, "actorId": 1, "actorValid": False, "enemyHp": 50,
    "enemyIndex": 0, "enemyValid": False, "switchId": 1, "switchValid": False,
    "turnA": 0, "turnB": 0, "turnEnding": False, "turnValid": False,
}


def troop(tid, name, members, pages=None):
    """`members` is a list of (enemyId, x, y) - x across the 816-wide battle
    field, y down it, both in pixels the way the editor stores them."""
    return {
        "id": tid, "name": name,
        "members": [{"enemyId": e, "x": x, "y": y, "hidden": False}
                    for e, x, y in members],
        "pages": pages or [{"conditions": dict(BLANK_TROOP_CONDITIONS),
                            "list": [{"code": 0, "indent": 0, "parameters": []}],
                            "span": 0}],
    }


def state(sid, name, icon, *, traits=(), restriction=0, max_turns=3, min_turns=3,
          auto_removal=1, message1="", message4="", priority=50, motion=0,
          overlay=0, remove_at_battle_end=True):
    return {
        "id": sid, "autoRemovalTiming": auto_removal, "chanceByDamage": 100,
        "iconIndex": icon, "maxTurns": max_turns, "minTurns": min_turns,
        "message1": message1, "message2": message1, "message3": "",
        "message4": message4, "messageType": 1, "motion": motion,
        "overlay": overlay, "name": name, "note": "", "priority": priority,
        "releaseByDamage": False, "removeAtBattleEnd": remove_at_battle_end,
        "removeByDamage": False, "removeByRestriction": False,
        "removeByWalking": False, "restriction": restriction,
        "stepsToRemove": 100, "traits": list(traits),
    }


# ============================================================== classes =====
def build_classes():
    """Each class's traits say what it is allowed to do; its param curves say
    what it is good at. The two together are the whole of a character's
    mechanical identity, so they live next to each other."""
    cl = R.load("Classes.json")

    def cls(cid, name, exp_params, curves, learnings, traits):
        return {"id": cid, "name": name, "note": "", "expParams": exp_params,
                "params": curves, "traits": list(traits),
                "learnings": [{"level": lv, "skillId": s, "note": ""}
                              for lv, s in learnings]}

    # A gentle curve - the game is short and should not need grinding.
    EXP = [25, 18, 30, 30]
    hit = lambda v: trait(22, 0, v)          # xparam 0: hit rate
    eva = lambda v: trait(22, 1, v)          # xparam 1: evasion
    crit = lambda v: trait(22, 2, v)         # xparam 2: critical rate

    upsert(cl, cls(
        CLASSES[BRAM], "Chosen One", EXP,
        params((400, 44), (60, 7), (18, 3.4), (16, 3.0), (14, 2.6),
               (15, 2.8), (17, 3.0), (32, 4.2)),
        [(1, SK_TURNIP), (1, SK_PLOT_ARMOR), (3, SK_SECOND_WIND),
         (6, SK_FRIENDSHIP), (9, SK_DESTINED)],
        [trait(23, 0, 1), hit(0.95), eva(0.06), crit(0.06),
         trait(41, STYPE_SPECIAL, 1),
         trait(51, WT_SWORD, 1), trait(51, WT_FLAIL, 1),
         trait(52, AT_LIGHT, 1), trait(52, AT_SMALL_SHIELD, 1),
         trait(52, AT_GENERAL, 1)]))

    upsert(cl, cls(
        CLASSES[MERRI], "Field Medic", EXP,
        params((360, 36), (120, 15), (11, 1.8), (13, 2.4), (23, 4.4),
               (25, 4.6), (15, 2.7), (18, 2.6)),
        [(1, SK_BEDSIDE), (1, SK_STERN), (2, SK_HYDRATION), (4, SK_REST),
         (5, SK_GET_UP), (10, SK_HOMILY)],
        [trait(23, 0, 0.9), hit(0.92), eva(0.05),
         trait(41, STYPE_MAGIC, 1), trait(41, STYPE_SPECIAL, 1),
         trait(11, EL_LIGHT, 0.5), trait(11, EL_DARK, 0.7),
         trait(23, 2, 1.5),                 # sparam 2: her healing lands harder
         trait(51, WT_STAFF, 1), trait(51, WT_FLAIL, 1),
         trait(52, AT_MAGIC, 1), trait(52, AT_GENERAL, 1)]))

    upsert(cl, cls(
        CLASSES[HOB], "Blacksmith", EXP,
        params((560, 60), (30, 3), (27, 4.8), (25, 4.4), (6, 1.0),
               (12, 2.0), (9, 1.6), (12, 1.8)),
        [(1, SK_ANVIL), (1, SK_PERCUSSIVE), (3, SK_FULL_SWING),
         (6, SK_QUENCH), (10, SK_REFORGE)],
        [trait(23, 0, 1.3),                 # sparam 0: enemies aim at him
         hit(0.9), eva(0.01), crit(0.04),
         trait(23, 6, 0.85),                # takes less physical damage
         trait(23, 7, 1.2),                 # and more magical
         trait(41, STYPE_SPECIAL, 1),
         trait(51, WT_FLAIL, 1), trait(51, WT_AXE, 1), trait(51, WT_GLOVE, 1),
         trait(52, AT_HEAVY, 1), trait(52, AT_GENERAL, 1),
         trait(52, AT_LARGE_SHIELD, 1)]))

    upsert(cl, cls(
        CLASSES[ZEPH], "Hedge Mage", EXP,
        params((300, 30), (140, 18), (9, 1.4), (10, 1.8), (29, 5.4),
               (18, 3.4), (16, 2.9), (15, 2.4)),
        [(1, SK_KINDLE), (1, SK_MANA_SIP), (2, SK_FROSTBITE), (3, SK_STATIC),
         (6, SK_CONFLAGRATE), (9, SK_METEOR)],
        [trait(23, 0, 0.8), hit(0.9), eva(0.04),
         trait(23, 4, 0.85),                # sparam 4: her spells cost less
         trait(23, 7, 1.25),                # but magic hurts her more
         trait(41, STYPE_MAGIC, 1),
         trait(51, WT_STAFF, 1), trait(51, WT_DAGGER, 1),
         trait(52, AT_MAGIC, 1), trait(52, AT_GENERAL, 1)]))

    upsert(cl, cls(
        CLASSES[NIX], "Acquisitions", EXP,
        params((350, 38), (55, 6), (20, 3.6), (12, 2.2), (12, 2.0),
               (13, 2.2), (30, 5.4), (28, 4.0)),
        [(1, SK_BACKSTAB), (1, SK_REALLOCATE), (3, SK_TWELVE),
         (5, SK_VANISH), (9, SK_COUP)],
        [trait(23, 0, 0.7),                 # hard to target
         hit(0.97), eva(0.22), crit(0.16),
         trait(64, 0, 1),                   # party ability: half encounters
         trait(41, STYPE_SPECIAL, 1),
         trait(51, WT_DAGGER, 1), trait(51, WT_CLAW, 1), trait(51, WT_BOW, 1),
         trait(52, AT_LIGHT, 1), trait(52, AT_GENERAL, 1)]))

    upsert(cl, cls(
        CLASSES[ALDRIC], "Knight Errant", EXP,
        params((500, 54), (45, 5), (19, 3.2), (32, 5.6), (8, 1.4),
               (21, 3.8), (10, 1.8), (14, 2.0)),
        [(1, SK_INTERPOSE), (1, SK_OATH), (3, SK_CHARGE), (6, SK_RALLY),
         (10, SK_CHIVALRIC)],
        [trait(23, 0, 1.4), hit(0.9), eva(0.03),
         trait(23, 1, 2.0),                 # sparam 1: guarding is worth it
         trait(23, 6, 0.8),
         trait(41, STYPE_SPECIAL, 1),
         trait(51, WT_SPEAR, 1), trait(51, WT_SWORD, 1),
         trait(52, AT_HEAVY, 1), trait(52, AT_LARGE_SHIELD, 1),
         trait(52, AT_GENERAL, 1)]))

    upsert(cl, cls(
        CLASSES[PIPER], "Bard", EXP,
        params((340, 36), (95, 12), (14, 2.4), (16, 2.8), (19, 3.6),
               (20, 3.6), (21, 3.8), (24, 3.4)),
        [(1, SK_BALLAD), (1, SK_DISCORD), (3, SK_RECAP), (5, SK_FORESHADOW),
         (6, SK_LULLABY), (9, SK_FINALE)],
        [trait(23, 0, 0.9), hit(0.93), eva(0.1), crit(0.05),
         trait(61, 0, 1),                   # action plus: sometimes acts twice
         trait(41, STYPE_MAGIC, 1), trait(41, STYPE_SPECIAL, 1),
         trait(51, WT_DAGGER, 1), trait(51, WT_WHIP, 1), trait(51, WT_STAFF, 1),
         trait(52, AT_LIGHT, 1), trait(52, AT_GENERAL, 1)]))

    # -- the three you can find in the south --------------------------------
    # Corvin is the first party member who is actively bad for you: enormous
    # damage, no defence, the worst luck in the game, and a finisher that only
    # pays out when he is nearly dead.
    upsert(cl, cls(
        CLASSES[CORVIN], "Doomed Rival", EXP,
        params((330, 34), (50, 6), (22, 4.0), (11, 1.9), (14, 2.4),
               (12, 2.0), (24, 4.4), (8, 1.2)),
        [(1, SK_BROOD), (1, SK_BLACK_EDGE), (2, SK_OMINOUS),
         (4, SK_OLD_WOUND), (6, SK_RIVAL), (9, SK_ALL_AT_ONCE)],
        [trait(23, 0, 0.9), hit(0.94), eva(0.10), crit(0.20),
         trait(23, 6, 1.2),                 # everything hurts him more
         trait(11, EL_DARK, 0.3), trait(11, EL_LIGHT, 1.3),
         trait(41, STYPE_SPECIAL, 1),
         trait(51, WT_SWORD, 1), trait(51, WT_DAGGER, 1),
         trait(52, AT_LIGHT, 1), trait(52, AT_GENERAL, 1)]))

    upsert(cl, cls(
        CLASSES[WREN], "Cataloguer", EXP,
        params((340, 36), (80, 9), (18, 3.2), (14, 2.5), (16, 2.8),
               (17, 3.0), (26, 4.6), (22, 3.2)),
        [(1, SK_SNAP_SHOT), (1, SK_FIELD_NOTES), (3, SK_PIN_DOWN),
         (5, SK_SPECIMEN), (6, SK_VOLLEY), (10, SK_DEFINITIVE)],
        [trait(23, 0, 0.8), hit(0.98), eva(0.12), crit(0.10),
         trait(64, 5, 1),                   # party ability: double drops -
                                            # she is collecting specimens
         trait(41, STYPE_SPECIAL, 1),
         trait(51, WT_BOW, 1), trait(51, WT_CROSSBOW, 1),
         trait(51, WT_DAGGER, 1),
         trait(52, AT_LIGHT, 1), trait(52, AT_GENERAL, 1)]))

    # Roland is deliberately better than everyone at everything. He is also
    # contractually unavailable for the last dungeon, which is the price.
    upsert(cl, cls(
        CLASSES[ROLAND], "Guest Star", EXP,
        params((480, 50), (100, 12), (22, 3.8), (24, 4.2), (22, 4.0),
               (22, 4.0), (22, 4.0), (26, 3.6)),
        [(1, SK_GUEST_APPEARANCE), (1, SK_ENCOURAGEMENT), (1, SK_FLOURISH),
         (9, SK_PRIOR)],
        [trait(23, 0, 1.0), hit(0.95), eva(0.08), crit(0.08),
         trait(41, STYPE_MAGIC, 1), trait(41, STYPE_SPECIAL, 1),
         trait(11, EL_LIGHT, 0.6),
         trait(51, WT_SWORD, 1), trait(51, WT_SPEAR, 1),
         trait(52, AT_HEAVY, 1), trait(52, AT_LIGHT, 1),
         trait(52, AT_GENERAL, 1), trait(52, AT_LARGE_SHIELD, 1)]))

    # WRE-1: the upgrade, which she earns by publishing. Her class exactly,
    # double drops and all, and two more party abilities: nothing the
    # monograph describes takes the party by surprise (cancel surprise), and
    # the party tends to see it first (raise preemptive). A class of its own,
    # reached by Change Class with her experience kept, so the Cataloguer
    # record and everybody's published data stay as they were.
    published = dict(next(c for c in cl if c and c["id"] == CLASSES[WREN]))
    published.update(id=CL_WREN_PUBLISHED, name="Cataloguer (Published)",
                     traits=list(published["traits"]) + [
                         trait(64, 2, 1), trait(64, 3, 1)])
    upsert(cl, published)
    R.save_list("Classes.json", cl)


# =============================================================== actors =====
def build_actors():
    """Sprite/face/battler indices are the stock MZ sets; the sv battler name
    must match a file in img/sv_actors, which only exists for Actor1 1-8,
    Actor2 1-8 and Actor3 5-8."""
    ac = R.load("Actors.json")

    def actor(aid, name, nickname, profile, sheet, index, level, equips,
              face=None):
        face_name, face_index = face or (sheet, index)
        return {"id": aid, "name": name, "nickname": nickname, "note": "",
                "profile": profile, "classId": CLASSES[aid],
                "initialLevel": level, "maxLevel": 99,
                "characterName": sheet, "characterIndex": index,
                "faceName": face_name, "faceIndex": face_index,
                "battlerName": "%s_%d" % (sheet, index + 1),
                "equips": list(equips), "traits": []}

    upsert(ac, actor(
        BRAM, "Bram", "Chosen One #48",
        "A turnip farmer. Was asleep during the vote and so did not object to "
        "being the subject of a prophecy. Owns one hoe and a great deal of "
        "unearned confidence.",
        "Actor1", 0, 4, [WP_HOE, AR_BUCKLER, 0, AR_SMOCK, 0]))

    upsert(ac, actor(
        MERRI, "Merribell", "Sister of Whatever Works",
        "Village healer. Her order holds that theology is a distraction from "
        "the actual problem, which is usually that you have not had any water "
        "today.",
        "Actor1", 7, 4, [WP_CENSER, 0, 0, AR_ROBE, 0]))

    upsert(ac, actor(
        HOB, "Hob", "Grumnir the Smith",
        "Blacksmith. Talks to his hammers. Two of the hammers have names, and "
        "one of them, he insists, talks back.",
        "Actor2", 4, 4, [WP_HAMMER, 0, 0, AR_CHAIN, 0]))

    upsert(ac, actor(
        ZEPH, "Zephyrine", "Formerly of the College",
        "Hedge mage. Expelled from the Collegium Arcanum over an incident "
        "involving the Dean, a duck, and what the enquiry called 'an "
        "unsanctioned quantity of fire'.",
        "Actor1", 5, 4, [WP_TWIG, 0, AR_HAT, AR_SILK, 0]))

    upsert(ac, actor(
        NIX, "Nix", "Acquisitions",
        "Runs the back room of the general store. Does not steal things. "
        "Locates them, ahead of schedule, on behalf of a client who has not "
        "yet been identified.",
        "Actor3", 4, 4, [WP_KNIFE, 0, 0, AR_LEATHER, 0],
        face=("Supplied", 0)))          # Mike's; NORTH.md 8.1e

    upsert(ac, actor(
        ALDRIC, "Aldric", "Pemberton-Gore III",
        "A knight errant who arrived in Thistlewick six years ago and has been "
        "trying to leave ever since. Has never once found the north gate.",
        "Actor3", 6, 4, [WP_LANCE, AR_KITE_SHIELD, AR_HELM, AR_PLATE, 0]))

    upsert(ac, actor(
        PIPER, "Piper", "Quill, Chronicler",
        "A bard who narrates events as they happen, in the third person, at "
        "volume, whether or not this is convenient.",
        "Actor2", 3, 4, [WP_LUTE, 0, 0, AR_LEATHER, 0]))

    upsert(ac, actor(
        CORVIN, "Corvin", "The Brooding One",
        "Has been waiting in the corner of a tavern for a destiny since he was "
        "nineteen. His village was destroyed by flooding, in his absence, and "
        "everyone was fine, and he cannot make anyone understand.",
        "Actor1", 4, 6, [WP_NOTCHED, 0, 0, AR_LEATHER, 0]))

    upsert(ac, actor(
        WREN, "Wren", "Cataloguer",
        "Does not fight monsters. Documents them. The fighting is a "
        "regrettable step in the methodology. Carries seventeen specimen jars "
        "and a monograph in progress.",
        "Actor2", 7, 6, [WP_CROSSBOW, 0, AR_A_HAT, AR_LEATHER, 0]))
    # WRE-3: the Gloamwood Society's badge is hers and nobody else's
    # (QUESTS.md 0.5) - an armour type no class has, allowed on her alone.
    # On the actor rather than the Cataloguer class, so no published class
    # changes and the rule reads as what it is.
    ac[WREN]["traits"] = [trait(52, AT_BADGE, 1)]
    # PIP-3: the rosette for second place is hers alone, the same way.
    ac[PIPER]["traits"] = [trait(52, AT_ROSETTE, 1)]
    # NIX-1: gran's coat, which fits now, and fits nobody else.
    ac[NIX]["traits"] = [trait(52, AT_COAT, 1)]
    # ZEPH-1: the Collegium's robe, with her name sewn in.
    ac[ZEPH]["traits"] = [trait(52, AT_ROBE, 1)]
    # COR-1: the scarf his mother knitted, in the wrong colour.
    ac[CORVIN]["traits"] = [trait(52, AT_SCARF, 1)]
    # MER-1: the founder's own copy of the Pamphlet, four lines and soup.
    ac[MERRI]["traits"] = [trait(52, AT_PAMPHLET, 1)]
    # ALD-2: the shield over the chapel door, thirty years waiting for him.
    ac[ALDRIC]["traits"] = [trait(52, AT_ESCUTCHEON, 1)]

    upsert(ac, actor(
        ROLAND, "Roland", "Guest Star",
        "Magnificent, glowing, extremely good at everything, and the "
        "protagonist of a much more expensive story. Contractually unavailable "
        "for the final dungeon. He is very sorry. He is always very sorry.",
        "Actor2", 2, 9, [WP_PRACTICE, AR_KITE_SHIELD, 0, AR_CHAIN, 0]))

    R.save_list("Actors.json", ac)


# =============================================================== skills =====
def build_skills():
    sk = R.load("Skills.json")

    # -- Bram: buffs the party and gets better the more friends he has -------
    upsert(sk, skill(
        SK_TURNIP, "Turnip Toss",
        "Throws a turnip very hard at one enemy. It is what he has.",
        "a.atk * 3 - b.def * 2", mp=0, tp=0, animation=1, icon=176,
        message="%1 throws a turnip!"))
    upsert(sk, skill(
        SK_PLOT_ARMOR, "Plot Armor",
        "The party is briefly too important to the story to be hurt properly.",
        "0", dmg_type=0, scope=8, mp=10, animation=53, icon=81, hit_type=0,
        effects=[effect(31, 3, 0, 3), effect(31, 5, 0, 3)],
        message="%1 is clearly the main character!"))
    upsert(sk, skill(
        SK_SECOND_WIND, "Heroic Second Wind",
        "Stands back up, dusts himself off, and gets on with it.",
        "a.mhp / 3 + 60", dmg_type=3, scope=11, tp=35, animation=41, icon=72,
        hit_type=0, effects=[effect(22, ST_POISON, 1.0)],
        message="%1 gets a second wind!"))
    upsert(sk, skill(
        SK_FRIENDSHIP, "The Power of Friendship",
        "Damages every enemy. Scales with how many people came along, which is "
        "the entire moral of most of these stories.",
        "(a.atk + a.mat) * 2 * $gameParty.aliveMembers().length - b.def",
        scope=2, mp=22, animation=100, icon=84, hit_type=0, element=EL_LIGHT,
        message="%1 believes in everyone!"))
    upsert(sk, skill(
        SK_DESTINED, "Destined Strike",
        "The blow the prophecy specifically mentions. Always finds its mark.",
        "a.atk * 6 - b.def * 2", tp=60, animation=25, icon=80, critical=True,
        message="%1 strikes as foretold!"))

    # -- Merribell: the only real healer, and the only Light damage ----------
    upsert(sk, skill(
        SK_BEDSIDE, "Bedside Manner",
        "Restores an ally's HP while explaining what they did wrong.",
        "a.mat * 3 + 70", dmg_type=3, scope=7, mp=8, animation=41, icon=72,
        hit_type=0, stype=STYPE_MAGIC, message="%1 sees to %2."))
    upsert(sk, skill(
        SK_HYDRATION, "Aggressive Hydration",
        "Restores HP to the whole party, whether or not they asked.",
        "a.mat * 2 + 45", dmg_type=3, scope=8, mp=22, animation=43, icon=72,
        hit_type=0, stype=STYPE_MAGIC, message="%1 insists everyone drinks!"))
    upsert(sk, skill(
        SK_STERN, "Stern Word",
        "Light damage to one enemy, delivered in the tone of a disappointed "
        "aunt.",
        "a.mat * 3 - b.mdf * 2", scope=1, mp=6, animation=96, icon=79,
        hit_type=2, element=EL_LIGHT, stype=STYPE_MAGIC,
        message="%1 has a word with %2."))
    upsert(sk, skill(
        SK_REST, "Prescribed Rest",
        "Clears an ally's afflictions and tells them to sit down.",
        "0", dmg_type=0, scope=7, mp=10, animation=45, icon=73, hit_type=0,
        stype=STYPE_MAGIC,
        effects=[effect(22, ST_POISON, 1.0), effect(22, 5, 1.0),
                 effect(22, 6, 1.0), effect(22, 7, 1.0), effect(22, 8, 1.0),
                 effect(22, ST_SLEEP, 1.0), effect(22, 12, 1.0)],
        message="%1 prescribes rest."))
    upsert(sk, skill(
        SK_GET_UP, "Get Up",
        "Revives a fallen ally. The dying is, she says, mostly attitude.",
        "0", dmg_type=0, scope=9, mp=28, animation=49, icon=72, hit_type=0,
        stype=STYPE_MAGIC,
        effects=[effect(22, ST_DEAD, 1.0), effect(11, 0, 0.5, 0)],
        message="%1 tells %2 to get up."))
    upsert(sk, skill(
        SK_HOMILY, "Homily",
        "Light damage to every enemy. Runs slightly long.",
        "a.mat * 4 - b.mdf * 2", scope=2, mp=30, animation=100, icon=79,
        hit_type=2, element=EL_LIGHT, stype=STYPE_MAGIC,
        message="%1 begins the homily."))

    # -- Hob: one enormous number, and healing by hitting people -------------
    upsert(sk, skill(
        SK_ANVIL, "Anvil Drop",
        "Hits one enemy with an anvil. Where the anvil comes from is his "
        "business.",
        "a.atk * 5 - b.def * 2", tp=30, animation=21, icon=100,
        message="%1 drops an anvil on %2!"))
    upsert(sk, skill(
        SK_PERCUSSIVE, "Percussive Maintenance",
        "Restores an ally's HP by striking them in a knowledgeable place.",
        "a.atk * 2 + 40", dmg_type=3, scope=7, mp=10, animation=1, icon=76,
        hit_type=0, message="%1 fixes %2 with a hammer."))
    upsert(sk, skill(
        SK_FULL_SWING, "Full Swing",
        "Swings at everything in front of him. Accuracy is not the point.",
        "a.atk * 3 - b.def * 2", scope=2, mp=14, animation=38, icon=100,
        success=85, message="%1 swings wide!"))
    upsert(sk, skill(
        SK_QUENCH, "Quench",
        "Braces up. Raises his own defence sharply and steadies him.",
        "0", dmg_type=0, scope=11, tp=25, animation=51, icon=81, hit_type=0,
        effects=[effect(31, 3, 0, 4), effect(21, 15, 1.0)],
        message="%1 quenches the blade."))
    upsert(sk, skill(
        SK_REFORGE, "Reforge The Moment",
        "The single hardest thing anyone in this village can do.",
        "a.atk * 8 - b.def * 3", tp=80, animation=22, icon=100, critical=True,
        variance=10, message="%1 brings the hammer down!"))

    # -- Zephyrine: elements, and one spell that is a gamble -----------------
    for sid, nm, el, anim, desc in (
            (SK_KINDLE, "Kindle", EL_FIRE, 66, "A modest fire, aimed carefully."),
            (SK_FROSTBITE, "Frostbite", EL_ICE, 71, "Ice, in one specific place."),
            (SK_STATIC, "Static", EL_THUNDER, 76, "A great deal of static.")):
        upsert(sk, skill(sid, nm, desc, "a.mat * 4 - b.mdf * 2", scope=1, mp=6,
                         animation=anim, icon=64 + el, hit_type=2, element=el,
                         stype=STYPE_MAGIC))
    upsert(sk, skill(
        SK_MANA_SIP, "Mana Sip",
        "Takes a little magic back off an enemy who was not using it well.",
        "12 + a.mat", dmg_type=6, scope=1, mp=0, tp_gain=12, animation=58,
        icon=163, hit_type=2, stype=STYPE_MAGIC, message="%1 sips."))
    upsert(sk, skill(
        SK_CONFLAGRATE, "Conflagrate",
        "Fire, to every enemy, all at once. This is the one she was expelled "
        "for.",
        "a.mat * 4 - b.mdf * 2", scope=2, mp=20, animation=70, icon=66,
        hit_type=2, element=EL_FIRE, stype=STYPE_MAGIC,
        message="%1 conflagrates!"))
    # ZEPH-5 (q_zephyrine.py). Taught at the Lay-By, off a page Dunnock
    # never saw: weaker than Kindle, cheaper, and at three enemies at random.
    upsert(sk, skill(
        SK_PAGE_23, "Page Twenty-Three",
        "Kindle, as worked out by a man whose book was missing the page. "
        "You mean it at everything. It should not work.",
        "a.mat * 3 - b.mdf * 2", scope=5, mp=5, animation=66, icon=66,
        hit_type=2, element=EL_FIRE, stype=STYPE_MAGIC,
        message="%1 means it at everything."))
    upsert(sk, skill(
        SK_METEOR, "Extremely Unstable Meteor",
        "Enormous damage to every enemy, give or take. Mostly give. Sometimes "
        "take.",
        "a.mat * 7 - b.mdf", scope=2, mp=45, animation=110, icon=67,
        hit_type=2, variance=60, stype=STYPE_MAGIC,
        message="%1 calls down something unstable!"))

    # -- Nix: speed, multi-hits, and taking things ---------------------------
    upsert(sk, skill(
        SK_BACKSTAB, "Backstab",
        "One precise hit from a direction nobody was watching.",
        "a.atk * 4 - b.def", tp=20, animation=11, icon=91, critical=True,
        message="%1 finds an opening!"))
    upsert(sk, skill(
        SK_REALLOCATE, "Reallocate",
        "Relieves an enemy of funds it was not going to spend anyway.",
        "0", dmg_type=0, scope=1, tp=10, animation=58, icon=314, hit_type=0,
        effects=[effect(44, CE_STEAL_GOLD)], message="%1 reallocates!"))
    upsert(sk, skill(
        SK_TWELVE, "Twelve Fingers",
        "Four quick strikes, at whatever happens to be nearest.",
        "a.atk * 2 - b.def", scope=4, mp=12, animation=16, icon=91,
        message="%1 is briefly everywhere!"))
    upsert(sk, skill(
        SK_VANISH, "Vanish",
        "Becomes markedly harder to hit and slightly harder to find.",
        "0", dmg_type=0, scope=11, tp=30, animation=52, icon=82, hit_type=0,
        effects=[effect(31, 6, 0, 4), effect(21, 21, 1.0)],
        message="%1 is suddenly not there."))
    upsert(sk, skill(
        SK_COUP, "Coup de Grace",
        "Hits harder the worse the target is already doing.",
        "a.atk * 3 * (2 - b.hp / b.mhp) - b.def", mp=18, animation=26,
        icon=91, critical=True, message="%1 finishes it!"))

    # -- Aldric: the reason anyone else survives -----------------------------
    upsert(sk, skill(
        SK_INTERPOSE, "Interpose",
        "Stands in front. Takes hits meant for the others, on principle.",
        "0", dmg_type=0, scope=11, mp=8, animation=51, icon=81, hit_type=0,
        effects=[effect(21, ST_INTERPOSING, 1.0)],
        message="%1 steps in front!"))
    upsert(sk, skill(
        SK_OATH, "Oath of Nearly-Certain Victory",
        "Raises the party's defence, at some length.",
        "0", dmg_type=0, scope=8, mp=14, animation=53, icon=81, hit_type=0,
        effects=[effect(31, 3, 0, 4)], message="%1 swears an oath!"))
    upsert(sk, skill(
        SK_CHARGE, "Righteous Charge",
        "A charge, in a direction that is at least approximately correct.",
        "a.atk * 4 - b.def", tp=25, animation=26, icon=93,
        message="%1 charges!"))
    upsert(sk, skill(
        SK_RALLY, "Rally",
        "Raises the party's attack with a short and very sincere speech.",
        "0", dmg_type=0, scope=8, mp=16, animation=51, icon=80, hit_type=0,
        effects=[effect(31, 2, 0, 4), effect(21, ST_INSPIRED, 1.0)],
        message="%1 rallies the party!"))
    upsert(sk, skill(
        SK_CHIVALRIC, "Chivalric Finisher",
        "Everything he has been holding back, plus his armour.",
        "a.atk * 5 + a.def * 2 - b.def * 2", tp=70, animation=27, icon=93,
        critical=True, variance=10, message="%1 finishes it properly!"))

    # -- Piper: makes everyone else better -----------------------------------
    upsert(sk, skill(
        SK_BALLAD, "Ballad of Adequacy",
        "Raises the party's attack. The lyrics are honest about the odds.",
        "0", dmg_type=0, scope=8, mp=10, animation=36, icon=80, hit_type=0,
        stype=STYPE_MAGIC, effects=[effect(31, 2, 0, 4)],
        message="%1 strikes up a ballad!"))
    upsert(sk, skill(
        SK_DISCORD, "Discordant Note",
        "One truly awful chord. Every enemy's defence suffers for it.",
        "a.mat - b.mdf", scope=2, mp=8, animation=34, icon=85, hit_type=2,
        stype=STYPE_MAGIC, effects=[effect(32, 3, 1.0, 4)],
        message="%1 plays something unforgivable."))
    upsert(sk, skill(
        SK_RECAP, "Previously, On This Quest",
        "Recaps events so far. The party is restored by the reminder that they "
        "have survived worse.",
        "a.mat + 60", dmg_type=3, scope=8, mp=0, tp=40, animation=44, icon=72,
        hit_type=0, stype=STYPE_MAGIC,
        effects=[effect(12, 0, 0, 20)], message="%1 recaps!"))
    upsert(sk, skill(
        SK_FORESHADOW, "Foreshadowing",
        "Hints ominously at what is coming. The party braces accordingly.",
        "0", dmg_type=0, scope=8, mp=12, animation=53, icon=81, hit_type=0,
        stype=STYPE_MAGIC, effects=[effect(31, 5, 0, 4), effect(31, 6, 0, 4)],
        message="%1 foreshadows!"))
    upsert(sk, skill(
        SK_LULLABY, "Lullaby of Mild Tedium",
        "A song about crop rotation. One enemy falls asleep.",
        "0", dmg_type=0, scope=1, mp=12, animation=62, icon=85, hit_type=2,
        stype=STYPE_MAGIC, success=80,
        effects=[effect(21, ST_SLEEP, 0.85)], message="%1 sings about turnips."))
    upsert(sk, skill(
        SK_FINALE, "Epic Finale",
        "The last verse, at volume, to every enemy present.",
        "a.mat * 4 + a.agi * 2 - b.mdf * 2", scope=2, mp=30, animation=110,
        icon=85, hit_type=2, element=EL_WIND, stype=STYPE_MAGIC,
        message="%1 reaches the finale!"))

    # -- Corvin: better the worse it is going ---------------------------------
    upsert(sk, skill(
        SK_BROOD, "Brood",
        "Says nothing, meaningfully. His attack rises, his guard drops, and "
        "the moment finds him ready.",
        "0", dmg_type=0, scope=11, mp=0, animation=52, icon=82, hit_type=0,
        effects=[effect(31, 2, 0, 4), effect(32, 3, 0, 4),
                 effect(21, ST_BROODING, 1.0), effect(13, 0, 30)],
        message="%1 broods."))
    upsert(sk, skill(
        SK_BLACK_EDGE, "Black Edge",
        "A dark, unhurried cut. He has practised this alone for eleven years "
        "and it shows, which is the sad part.",
        "a.atk * 4 - b.def * 2", mp=8, animation=24, icon=91, element=EL_DARK,
        message="%1 cuts once."))
    upsert(sk, skill(
        SK_OMINOUS, "Ominous Remark",
        "Says something about the coming dark to nobody in particular. Every "
        "enemy attacks worse for a while.",
        "0", dmg_type=0, scope=2, mp=6, animation=34, icon=85, hit_type=2,
        effects=[effect(32, 2, 0, 3), effect(32, 4, 0, 3)],
        message="%1 says something about the coming dark."))
    upsert(sk, skill(
        SK_OLD_WOUND, "Old Wound",
        "Opens the scar on purpose: costs him a sixth of his health and fills "
        "his resolve. A terrible way to run a person.",
        "Math.min(a.mhp / 6, a.hp - 1)", scope=11, dmg_type=1, variance=0,
        tp_gain=60, animation=1, icon=91, hit_type=0,
        message="%1 opens an old wound."))
    upsert(sk, skill(
        SK_RIVAL, "Prophesied Rival",
        "The blow he has been saving. Hits hardest when he is nearly finished, "
        "which he considers correct.",
        "a.atk * 4 * (2 - a.hp / a.mhp) - b.def * 2", tp=50, animation=25,
        icon=91, element=EL_DARK, critical=True, variance=10,
        message="%1 has been waiting for this."))
    upsert(sk, skill(
        SK_ALL_AT_ONCE, "Everything At Once",
        "Stops holding back. Dark damage to every enemy, and a slightly "
        "embarrassing amount of shouting.",
        "a.atk * 3 - b.def * 2", scope=2, mp=26, animation=103, icon=91,
        element=EL_DARK, message="%1 stops holding back!"))

    # -- Wren: two arrows, a debuff, and a monograph --------------------------
    upsert(sk, skill(
        SK_SNAP_SHOT, "Snap Shot",
        "Two bolts, quickly, at one specimen. Costs nothing, which she "
        "considers good practice.",
        "a.atk * 2 - b.def", mp=0, repeats=2, animation=111, icon=89,
        tp_gain=12, message="%1 looses two bolts."))
    upsert(sk, skill(
        SK_FIELD_NOTES, "Field Notes",
        "Writes one enemy up properly. Being described accurately does "
        "measurable harm to a creature's defences.",
        "0", dmg_type=0, scope=1, mp=10, animation=54, icon=83, hit_type=2,
        effects=[effect(32, 3, 0, 5), effect(32, 5, 0, 5),
                 effect(21, ST_CATALOGUED, 1.0)],
        message="%1 takes notes on %2."))
    upsert(sk, skill(
        SK_PIN_DOWN, "Pin It Down",
        "A bolt through something structural. Damage, and the specimen is "
        "markedly slower about everything afterwards.",
        "a.atk * 3 - b.def * 2", mp=12, animation=29, icon=89,
        effects=[effect(21, ST_SLOWED, 0.9)],
        message="%1 pins %2 down."))
    upsert(sk, skill(
        SK_SPECIMEN, "Preserve A Specimen",
        "Applies the preserving fluid early, on the grounds that it saves time "
        "later. Poisons one enemy.",
        "a.atk * 2 - b.def", mp=14, animation=59, icon=89, element=EL_WATER,
        effects=[effect(21, ST_POISON, 0.9)],
        message="%1 applies the preserving fluid."))
    upsert(sk, skill(
        SK_VOLLEY, "Volley",
        "Empties the quiver across the whole field. Wasteful. She retrieves "
        "every bolt afterwards and will say so.",
        "a.atk * 3 - b.def * 2", scope=2, mp=22, animation=113, icon=89,
        message="%1 empties the quiver!"))
    upsert(sk, skill(
        SK_DEFINITIVE, "The Definitive Entry",
        "The last word on a species, delivered at range. Nothing survives being "
        "described this thoroughly.",
        "a.atk * 6 - b.def * 2", tp=60, animation=114, icon=89, critical=True,
        variance=10, message="%1 closes the entry on %2."))

    # -- Roland: annoyingly good at all of it ---------------------------------
    upsert(sk, skill(
        SK_GUEST_APPEARANCE, "Guest Appearance",
        "Arrives in the fight properly, with light behind him. It is a lot to "
        "watch and it does a lot of damage.",
        "a.atk * 4 - b.def * 2", mp=10, animation=25, icon=96,
        element=EL_LIGHT, message="%1 makes an entrance!"))
    upsert(sk, skill(
        SK_ENCOURAGEMENT, "Heroic Encouragement",
        "Heals the whole party and means every word of it. Guest characters "
        "always have one of these.",
        "a.mat * 2 + 80", dmg_type=3, scope=8, mp=24, animation=43, icon=72,
        hit_type=0, stype=STYPE_MAGIC, effects=[effect(31, 2, 0, 3)],
        message="%1 tells everyone they are doing well."))
    upsert(sk, skill(
        SK_FLOURISH, "Unnecessary Flourish",
        "Hits every enemy in a way that is objectively more elaborate than the "
        "situation calls for.",
        "a.atk * 3 - b.def", scope=2, mp=20, animation=38, icon=96,
        element=EL_LIGHT, message="%1 flourishes, unnecessarily."))
    upsert(sk, skill(
        SK_PRIOR, "Prior Engagement",
        "Everything he has, at once, quickly, because he has to be somewhere.",
        "a.atk * 5 + a.mat * 2 - b.def * 2", tp=70, animation=117, icon=96,
        element=EL_LIGHT, critical=True, variance=10,
        message="%1 checks the time, and finishes it."))

    # -- what the monsters do ------------------------------------------------
    upsert(sk, skill(SK_NIBBLE, "Nibble", "", "a.atk * 2 - b.def",
                     animation=16, message="%1 nibbles %2."))
    upsert(sk, skill(SK_ROOT_GRAB, "Root Grab", "",
                     "a.atk * 3 - b.def * 2", scope=2, animation=88,
                     element=EL_EARTH, message="%1 grabs at everyone!"))
    upsert(sk, skill(SK_SHRIEK, "Portentous Shriek", "", "0", dmg_type=0,
                     scope=2, animation=34, hit_type=2,
                     effects=[effect(32, 2, 0.6, 3)],
                     message="%1 shrieks something about doom."))
    upsert(sk, skill(SK_EMBER, "Ember", "", "a.mat * 3 - b.mdf * 2",
                     animation=66, hit_type=2, element=EL_FIRE,
                     message="%1 spits an ember."))
    upsert(sk, skill(SK_DRAIN, "Drain", "", "a.mat * 2 - b.mdf", dmg_type=5,
                     animation=58, hit_type=2, element=EL_DARK,
                     message="%1 drains %2."))
    upsert(sk, skill(SK_DOOM_MONOLOGUE, "Doom Monologue", "",
                     "a.mat * 2 - b.mdf", scope=2, animation=104, hit_type=2,
                     element=EL_DARK,
                     effects=[effect(32, 3, 0.5, 3)],
                     message="%1 explains the plan at length."))
    upsert(sk, skill(SK_INEVITABILITY, "Inevitability", "",
                     "a.atk * 4 - b.def * 2", scope=2, animation=39,
                     message="%1 does the inevitable."))
    upsert(sk, skill(SK_CLAUSE_TWELVE, "Clause Twelve", "",
                     "a.mat * 3 - b.mdf", scope=2, animation=105,
                     hit_type=2, element=EL_DARK,
                     message="%1 invokes CLAUSE TWELVE."))
    upsert(sk, skill(SK_ERRATUM, "Erratum", "", "a.mat * 4 - b.mdf",
                     scope=1, animation=101, hit_type=2, element=EL_DARK,
                     effects=[effect(21, 6, 0.5)],
                     message="%1 issues an erratum."))
    upsert(sk, skill(SK_SMALL_PRINT, "The Small Print", "", "0", dmg_type=0,
                     scope=11, animation=51, hit_type=0,
                     effects=[effect(31, 2, 0, 5), effect(31, 3, 0, 5)],
                     message="%1 refers to the small print."))

    upsert(sk, skill(SK_PINCH, "Pinch", "", "a.atk * 3 - b.def * 2",
                     animation=16, message="%1 pinches %2. It is a lot."))
    upsert(sk, skill(SK_SWOOP, "Swoop", "", "a.atk * 2 - b.def", scope=2,
                     animation=38, element=EL_WIND,
                     message="%1 goes for the food."))
    upsert(sk, skill(SK_GRAVE_DUTY, "Grave Duty", "", "a.mat * 3 - b.mdf",
                     dmg_type=5, animation=58, hit_type=2, element=EL_DARK,
                     message="%1 takes something owed."))
    upsert(sk, skill(SK_WHATS_DONE, "It Is What Is Done", "",
                     "a.atk * 4 - b.def * 2", scope=2, animation=25,
                     effects=[effect(32, 3, 0, 3)],
                     message="%1 does what is done."))
    upsert(sk, skill(SK_RUMMAGE, "Rummage", "", "a.atk * 2 - b.def",
                     animation=21, message="%1 rummages through %2."))
    upsert(sk, skill(SK_OPINION, "A Strong Opinion", "",
                     "a.atk * 5 - b.def * 2", animation=39, critical=True,
                     message="%1 has a strong opinion about this."))
    upsert(sk, skill(SK_TRIBUTE, "Demand Tribute", "", "a.atk * 2 - b.def",
                     scope=2, animation=37,
                     effects=[effect(32, 2, 0, 3)],
                     message="%1 demands tribute, with a syllabus."))

    # -- the north -----------------------------------------------------------
    # Everything up here is a machine, and every skill is something a machine
    # does rather than something a monster does: it lets go of its pressure, it
    # tries to leave the ground, it takes a part off its neighbour. Attempt
    # Eighty-Four's last one is the whole character - a hundred and forty years
    # of repairing herself out of the wrecks either side of her, done once more
    # in front of you, in the middle of a fight.
    upsert(sk, skill(SK_SCALD, "Let Go", "", "a.atk * 3 - b.def",
                     animation=67, element=EL_FIRE,
                     message="%1 lets go of it all at once."))
    upsert(sk, skill(SK_STILL_TRYING, "Still Trying", "",
                     "a.atk * 3 - b.def * 2", animation=39,
                     message="%1 gets a foot off the ground."))
    upsert(sk, skill(SK_SHED_A_PART, "Take A Part Off", "",
                     "a.atk * 2 - b.def", animation=21,
                     effects=[effect(32, 3, 0, 3), effect(21, ST_SLOWED, 0.6)],
                     message="%1 takes a part off %2."))
    upsert(sk, skill(SK_OVERPRESSURE, "Overpressure", "",
                     "a.atk * 3 - b.def", scope=2, animation=68,
                     element=EL_FIRE,
                     message="%1 goes over the mark on the gauge."))
    upsert(sk, skill(SK_DUE_NORTH, "Due North", "", "a.atk * 5 - b.def * 2",
                     animation=39, critical=True, variance=10,
                     message="%1 sets off north again."))
    upsert(sk, skill(SK_MAKE_GOOD, "Make Good", "", "700 + a.atk * 6",
                     dmg_type=3, scope=11, animation=42, hit_type=0,
                     message="%1 makes good out of the neighbours."))

    save("Skills.json", sk)


# =============================================================== states =====
def build_states():
    st = R.load("States.json")
    upsert(st, state(
        ST_INTERPOSING, "Interposing", 81,
        traits=[trait(62, 1, 0), trait(23, 0, 6), trait(23, 6, 0.75)],
        max_turns=3, min_turns=3,
        message1="%1 is guarding the others!",
        message4="%1 stands down."))
    upsert(st, state(
        ST_INSPIRED, "Inspired", 80,
        traits=[trait(22, 2, 0.15), trait(22, 0, 0.05)],
        max_turns=4, min_turns=4,
        message1="%1 is inspired!", message4="%1 is no longer inspired."))
    upsert(st, state(
        ST_NARRATED, "Narrated", 87,
        traits=[trait(22, 1, 0.15), trait(23, 0, 1.4)],
        max_turns=4, min_turns=4,
        message1="%1 is being described in detail!",
        message4="%1 is out of the narration."))
    upsert(st, state(
        ST_BROODING, "Brooding", 82,
        traits=[trait(22, 2, 0.25), trait(23, 6, 1.25)],
        max_turns=4, min_turns=4,
        message1="%1 is brooding!", message4="%1 stops brooding. Mostly."))
    upsert(st, state(
        ST_CATALOGUED, "Catalogued", 83,
        traits=[trait(22, 1, -0.15), trait(23, 6, 1.2), trait(23, 7, 1.2)],
        max_turns=5, min_turns=5,
        message1="%1 has been written up.",
        message4="%1 is no longer of scholarly interest."))
    upsert(st, state(
        ST_SLOWED, "Pinned", 87,
        traits=[trait(21, 6, 0.5), trait(22, 0, -0.1)],
        max_turns=4, min_turns=4,
        message1="%1 is pinned down!", message4="%1 works itself free."))
    # COR-5: the curse Corvin pays to have put on (QUESTS.md B4). Bad for
    # him on purpose: half luck, drawn fire, a slow bleed. It lasts out of
    # battle and until something clears it - Miss Fettle, or a proper bed.
    upsert(st, state(
        ST_CURSED, "Cursed (Elective)", 17,
        traits=[trait(21, 7, 0.5), trait(23, 0, 1.5), trait(22, 7, -0.03)],
        auto_removal=0, max_turns=1, min_turns=1, remove_at_battle_end=False,
        message1="%1 is cursed, electively.",
        message4="%1's curse wears off.", priority=40))
    save("States.json", st)


# ============================================================ inventory =====
def build_items():
    it = R.load("Items.json")
    upsert(it, item(IT_POTION, "Potion", "Restores 300 HP to one ally.",
                    price=60, icon=176,
                    effects=[effect(11, 0, 0, 300)]))
    upsert(it, item(IT_HI_POTION, "Hi-Potion", "Restores 900 HP to one ally.",
                    price=280, icon=176,
                    effects=[effect(11, 0, 0, 900)]))
    upsert(it, item(IT_TONIC, "Field Tonic",
                    "Restores 400 HP to the whole party. Tastes of turnip.",
                    price=420, icon=180, scope=8, animation=43,
                    effects=[effect(11, 0, 0, 400)]))
    upsert(it, item(IT_ETHER, "Ether", "Restores 60 MP to one ally.",
                    price=200, icon=178,
                    effects=[effect(12, 0, 0, 60)]))
    upsert(it, item(IT_ELIXIR, "Elixir",
                    "Restores an ally completely. There are four in the world "
                    "and everyone is saving them for later.",
                    price=1500, icon=179, animation=42,
                    effects=[effect(11, 0, 1.0, 0), effect(12, 0, 1.0, 0)]))
    upsert(it, item(IT_FEATHER, "Slightly Singed Feather",
                    "Revives one fallen ally at half health. Smells of a "
                    "bonfire.",
                    price=500, icon=185, scope=9, animation=49,
                    effects=[effect(22, ST_DEAD, 1.0), effect(11, 0, 0.5, 0)]))
    upsert(it, item(IT_ANTIDOTE, "Antidote", "Cures poison.",
                    price=40, icon=177, animation=45,
                    effects=[effect(22, ST_POISON, 1.0)]))
    upsert(it, item(IT_SMELLING_SALTS, "Smelling Salts",
                    "Wakes an ally who is asleep, stunned or confused.",
                    price=80, icon=181, animation=45,
                    effects=[effect(22, ST_SLEEP, 1.0), effect(22, 8, 1.0),
                             effect(22, 13, 1.0)]))
    upsert(it, item(IT_TURNIP, "Turnip",
                    "A turnip. Restores 1 HP. Bram grew it and would prefer "
                    "you did not throw it away.",
                    price=2, icon=257,
                    effects=[effect(11, 0, 0, 1), effect(44, CE_TURNIP_EATEN)]))

    # -- what they eat in the south -----------------------------------------
    upsert(it, item(IT_BISCUIT, "Ship's Biscuit",
                    "Restores 250 HP. Older than some of the people selling "
                    "it. Must be soaked, struck, or both.",
                    price=90, icon=266, effects=[effect(11, 0, 0, 250)]))
    upsert(it, item(IT_CHOWDER, "Sopping Chowder",
                    "Restores 350 HP to the whole party. Nobody has ever "
                    "asked what is in it and Nether Sopping is glad of that.",
                    price=380, icon=236, scope=8, animation=43,
                    effects=[effect(11, 0, 0, 350)]))
    upsert(it, item(IT_PALE, "Bottle of Sopping Pale",
                    "Restores 45 MP and 25 TP to one ally. Tastes of the "
                    "harbour, which is either a fault or the point.",
                    price=240, icon=226,
                    effects=[effect(12, 0, 0, 45), effect(13, 0, 25)]))

    # -- what they eat in the north -----------------------------------------
    # The counter in the Parish Rooms, because in a town this size the
    # registrar also sells things. Nothing here is magic; it is a works town
    # and what a works town sells you is fat, tea and something for the hands.
    upsert(it, item(IT_DRIPPING, "Bread and Dripping",
                    "Restores 320 HP. The north's answer to ship's biscuit, "
                    "and it is not close, and the north knows it.",
                    price=120, icon=269, effects=[effect(11, 0, 0, 320)]))
    upsert(it, item(IT_STEWED_TEA, "Stewed Tea",
                    "Restores 55 MP and 20 TP. It has been on the stove since "
                    "six. That is not a complaint about the tea.",
                    price=250, icon=208,
                    effects=[effect(12, 0, 0, 55), effect(13, 0, 20)]))
    upsert(it, item(IT_LINIMENT, "Works Liniment",
                    "Cures poison, sleep and blindness. Mrs Tunnicliffe will "
                    "tell you twice that it is not to go near the eyes.",
                    price=160, icon=178, animation=45,
                    effects=[effect(22, ST_POISON, 1.0), effect(22, ST_SLEEP, 1.0),
                             effect(22, 13, 1.0)]))

    # key items: itypeId 2, not consumable, no use in battle
    upsert(it, item(IT_PROPHECY, "The Prophecy",
                    "The Forty-Eighth Prophecy of Thistlewick, in triplicate. "
                    "Clause twelve has been underlined by somebody worried.",
                    itype=2, consumable=False, scope=0, occasion=3, icon=193))
    upsert(it, item(IT_TOWER_KEY, "Tower Key",
                    "Opens the Obligatory Tower. Labelled 'SPARE - DO NOT LOSE "
                    "AGAIN'.",
                    itype=2, consumable=False, scope=0, occasion=3, icon=195))
    upsert(it, item(IT_RECEIPT, "A Receipt",
                    "Proof of purchase for one (1) Dark Lord, renewable. "
                    "Signed, in a hand that has clearly been at this a while.",
                    itype=2, consumable=False, scope=0, occasion=3, icon=188))

    # -- the southern key items ---------------------------------------------
    upsert(it, item(IT_JAR, "A Jar Of Something",
                    "Sealed, weighty, and warm on one side. For Mrs Thrupp of "
                    "Nether Sopping, from her sister, with love.",
                    itype=2, consumable=False, scope=0, occasion=3, icon=228))
    upsert(it, item(IT_REPLY, "A Reply, Sealed",
                    "Heavier than the jar. Do not open it. Thirty years of "
                    "sisterly regard are in there under pressure.",
                    itype=2, consumable=False, scope=0, occasion=3, icon=192))
    upsert(it, item(IT_REFERENCE, "A Character Reference",
                    "Elder Wispel confirms that Bram Thistle is the Chosen "
                    "One, is of good character, and grows a decent turnip.",
                    itype=2, consumable=False, scope=0, occasion=3, icon=193))
    upsert(it, item(IT_LAMP_OIL, "Lamp Oil",
                    "One gallon, for a lighthouse that has been dark since "
                    "the spring. Sold by Mrs Barrow, who marks it up.",
                    price=120, itype=2, consumable=False, scope=0, occasion=3,
                    icon=275))
    upsert(it, item(IT_GUILD_CARD, "Guild Card (Provisional)",
                    "Certifies the holder as an adventurer. Provisional. The "
                    "Guild has been provisional for forty years.",
                    itype=2, consumable=False, scope=0, occasion=3, icon=194))
    upsert(it, item(IT_HISTORY, "A Complete And Accurate History",
                    "Hosea Bellwether's life's work, bound in boards. It is "
                    "complete. Accuracy was always going to be harder.",
                    itype=2, consumable=False, scope=0, occasion=3, icon=229))
    upsert(it, item(IT_BENCH, "A Bench (Flat-Packed)",
                    "One bench, in eleven pieces, with a mallet and a diagram "
                    "that is wrong. Somebody wanted somewhere to sit.",
                    price=400, itype=2, consumable=False, scope=0, occasion=3,
                    icon=223))

    # -- the northern key items ---------------------------------------------
    # Two things the Two Hundred needs that will fit in a pack. The third
    # thing she needs is the party, and there is no icon for that.
    upsert(it, item(IT_OILSKIN_BOLTS, "Forty Bolts of Oilskin",
                    "Forty. Mrs Barrow counted them twice, out loud, and made "
                    "somebody else count them again after her.",
                    itype=2, consumable=False, scope=0, occasion=3, icon=227))
    upsert(it, item(IT_PLATE, "Number-Plate, 112",
                    "A brass oval off an airship, stamped HOYLE WORKS 112. It "
                    "has been out in the weather for a hundred years.",
                    itype=2, consumable=False, scope=0, occasion=3, icon=188))
    # The description does not say what it is, because nothing in the works
    # says what it is either. That is the whole of the joke and the ledger is
    # in on it: one off, reissued a hundred and ninety-nine times, returned a
    # hundred and ninety-eight, described in the column headed DESCRIPTION as
    # "ITEM 1".
    # -- the companion quests' ----------------------------------------------
    upsert(it, item(IT_BRASS_PLATE, "A Brass Plate",
                    "Four lines about a goose, at a crown a letter, with no "
                    "name on it. For the Slain Wyvern, if Dorcas will have it.",
                    itype=2, consumable=False, scope=0, occasion=3, icon=188))
    upsert(it, item(IT_FITNESS_FORM, "Certificate of Fitness (Blank)",
                    "Clause eleven: scales, a good light, a clean surface and "
                    "a witness. Use it when Merribell has all four.",
                    itype=2, consumable=False, scope=0, occasion=2, icon=186,
                    effects=[effect(44, CE_FIT_TO_TRAVEL)]))
    upsert(it, item(IT_SCALES, "The Fishmonger's Scales",
                    "Stamped, to twenty stone, and wrapped in sacking. They "
                    "have never once lied. They smell of haddock.",
                    itype=2, consumable=False, scope=0, occasion=3, icon=208))
    upsert(it, item(IT_CERTIFICATE, "Certificate of Fitness",
                    "Bram, certified fit to travel under clause eleven. Signed, "
                    "witnessed, blotted. Does nothing. Enormously official.",
                    itype=2, consumable=False, scope=0, occasion=3, icon=191))
    upsert(it, item(IT_TUBE_PLATE, "A Boiler Tube Plate",
                    "For the Two Hundred's refit: forty-one holes, one heat, "
                    "four hands. Still warm. For Miss Hoyle, up the hill.",
                    itype=2, consumable=False, scope=0, occasion=3, icon=196))
    upsert(it, item(IT_APOLOGY, "A Written Apology",
                    "From I. Scrope, week four, on the back of a syllabus. "
                    "Very sorry, in a very good hand. Hob keeps it.",
                    itype=2, consumable=False, scope=0, occasion=3, icon=193))
    upsert(it, item(IT_RETURNS, "Previously Owned Goods",
                    "Eleven things, labelled for their owners in Nix's hand: "
                    "four in Thistlewick, four in Nether Sopping, three up north.",
                    itype=2, consumable=False, scope=0, occasion=3, icon=209))
    upsert(it, item(IT_PARCEL, "A Parcel, Unaddressed",
                    "Brown paper and string. The last of Hulda Bole's four "
                    "hundred and six jobs. The client had moved.",
                    itype=2, consumable=False, scope=0, occasion=3, icon=208))
    upsert(it, item(IT_FORM_S7, "Form S-7",
                    "Application to Consult Struck Material (Verse). In "
                    "triplicate, in Piper's hand, which scans.",
                    itype=2, consumable=False, scope=0, occasion=3, icon=193))
    upsert(it, item(IT_ARCHIVE_KEY, "A Key Marked STRUCK",
                    "Off Councillor Fenn's hook, while he was explaining "
                    "clause twelve. It goes back on the way out.",
                    itype=2, consumable=False, scope=0, occasion=3, icon=195))
    upsert(it, item(IT_WARDENS_NOTES, "The Wardens' Notes",
                    "BEATRICE. A hammer. DISQUALIFIED (clause one). With the "
                    "Company's mark. Remarks: right about everything.",
                    itype=2, consumable=False, scope=0, occasion=3, icon=191))
    upsert(it, item(IT_BOND_TICKET, "Bond No. 1 (Ticket)",
                    "A luggage ticket for the Bonded Warehouse, Great Dunnage. "
                    "Enclosed by the client, aged fifteen.",
                    itype=2, consumable=False, scope=0, occasion=3, icon=195))
    upsert(it, item(IT_MINUTES, "The Minutes (141st)",
                    "Apologies: the sorcerer. Readiness: not. Lineage: "
                    "present. Asset: available. Thanked. Eleven minutes.",
                    itype=2, consumable=False, scope=0, occasion=3, icon=193))
    upsert(it, item(IT_DUCK, "The Honorary Fellow",
                    "A duck, with the Collegium's silver medal on a ribbon. "
                    "Four hit points. Walks into everything.",
                    itype=2, consumable=False, scope=0, occasion=3, icon=298))
    upsert(it, item(IT_PROXY, "The Duck's Proxy",
                    "Congregation's minutes, an extract: PROXY - Z. VANCE. "
                    "PERMANENTLY. One vote, and it has a feather on it.",
                    itype=2, consumable=False, scope=0, occasion=3, icon=195))
    upsert(it, item(IT_FINES_NOTICE, "Notice of Fines (Eleventh)",
                    "The Collegium Library, to Miss Z. Vance, on study leave. "
                    "Folded very small, and kept in her hat.",
                    itype=2, consumable=False, scope=0, occasion=3, icon=192))
    upsert(it, item(IT_INVITATION, "Invitation (Eleventh)",
                    "The Flood Dinner Committee requests the pleasure of Mr "
                    "C. Ash as Speaker. Saturday. It has no stamp on it.",
                    itype=2, consumable=False, scope=0, occasion=3, icon=192))
    upsert(it, item(IT_REPORT_CARD, "Report Card (Ashcombe School)",
                    "Pupil: Corvin. The surname has run. \"He will go far, if "
                    "he ever gets up.\" Kept dry, in oilcloth.",
                    itype=2, consumable=False, scope=0, occasion=3, icon=193))
    upsert(it, item(IT_JAM, "Mrs Pardew's Jam",
                    "Gooseberry, 1931, her gran's, and the last jar. The label "
                    "says (BETTER). Wasps would like it very much.",
                    itype=2, consumable=False, scope=0, occasion=3, icon=179))
    upsert(it, item(IT_ALD1_LETTER, "The Letter (Nine Years Late)",
                    "TO THE PARISH OF LITTLE GORE. BY HAND. P-G. Soft at the "
                    "folds. His first errand, four miles.",
                    itype=2, consumable=False, scope=0, occasion=3, icon=192))
    upsert(it, item(IT_ELEGY, "Elegy (Nine Lines)",
                    "Abel Thrush, carrier, Little Gore - Fenmarch - Sump. "
                    "Piper's copy. She has not performed it.",
                    itype=2, consumable=False, scope=0, occasion=3, icon=193))
    upsert(it, item(IT_AUTHORISED, "The Authorised Version",
                    "The Lay of the Forty-Eighth, by the Quills, chroniclers "
                    "to the Committee. Properly metred. A very good middle.",
                    itype=2, consumable=False, scope=0, occasion=3, icon=189))
    upsert(it, item(IT_STAR_IRON, "Star-Iron",
                    "The Sky Anvil. Fell in 1749, on a Tuesday, and was a "
                    "gatepost. Very heavy. Hob does not mention this.",
                    itype=2, consumable=False, scope=0, occasion=3, icon=313))
    upsert(it, item(IT_FEN_CERTIFICATE, "Certificate of Burning",
                    "The Cinder Fen, 900 acres. Fire person: Z. Vance. "
                    "Quantity: sanctioned. Countersigned, in scorch, by the Fen.",
                    itype=2, consumable=False, scope=0, occasion=3, icon=193))
    upsert(it, item(IT_ITEM_ONE, "ITEM 1",
                    "Heavier than it looks. Stencilled, on all six faces, "
                    "ITEM 1. Ott would like it out of a field.",
                    itype=2, consumable=False, scope=0, occasion=3, icon=218))
    save("Items.json", it)


def build_weapons():
    wp = R.load("Weapons.json")
    atk_el = lambda e: trait(31, e, 0)

    # Bram - sword class, sensible numbers all the way up
    upsert(wp, weapon(WP_HOE, "Turnip Hoe",
                      "[Sword] A hoe. It has done more honest work than most "
                      "legendary blades.", WT_SWORD, 40,
                      [0, 0, 10, 2, 0, 0, 0, 2], icon=122))
    upsert(wp, weapon(WP_SWORD, "Village Sword",
                      "[Sword] Kept above the fireplace for exactly this "
                      "occasion.", WT_SWORD, 340,
                      [0, 0, 22, 3, 0, 0, 2, 2], icon=97))
    upsert(wp, weapon(WP_BROADSWORD, "Broadsword",
                      "[Sword] Heavier. Simpler. Works.", WT_SWORD, 950,
                      [0, 0, 38, 5, 0, 2, 0, 2], icon=123))
    upsert(wp, weapon(WP_DESTINY, "Blade of Some Destiny",
                      "[Sword] Prophesied, though the prophecy is vague about "
                      "which one.", WT_SWORD, 2600,
                      [0, 0, 58, 8, 6, 6, 4, 12], icon=113, animation=25,
                      traits=[atk_el(EL_LIGHT), trait(22, 2, 0.08)]))

    # Merribell - staff/flail
    upsert(wp, weapon(WP_CENSER, "Censer",
                      "[Flail] Swung on a chain. Doubles as a weapon, which is "
                      "not what it was for.", WT_FLAIL, 60,
                      [0, 0, 6, 0, 8, 4, 0, 0], icon=98))
    upsert(wp, weapon(WP_STAFF, "Wellwater Staff",
                      "[Staff] Its healing is 30% better and its jokes are "
                      "not.", WT_STAFF, 420,
                      [0, 0, 8, 2, 20, 8, 0, 0], icon=101))
    upsert(wp, weapon(WP_HOLY_ROD, "Rod of Whatever Works",
                      "[Staff] Whatever works.", WT_STAFF, 1800,
                      [0, 0, 12, 4, 40, 16, 2, 4], icon=109,
                      traits=[atk_el(EL_LIGHT), trait(23, 2, 0.25)]))

    # Hob - flail/axe/glove
    upsert(wp, weapon(WP_HAMMER, "Shop Hammer",
                      "[Flail] Named Beatrice. Hob will tell you why.",
                      WT_FLAIL, 90, [0, 0, 16, 2, 0, 0, -2, 0], icon=110))
    upsert(wp, weapon(WP_SLEDGE, "Two-Handed Sledge",
                      "[Axe] Requires both hands and a certain outlook.",
                      WT_AXE, 780, [0, 0, 40, 4, 0, 0, -4, 0], icon=99))
    upsert(wp, weapon(WP_WORLDBREAKER, "Beatrice II",
                      "[Axe] Hob made this one himself, and it shows, in a "
                      "good way.", WT_AXE, 2400,
                      [0, 0, 68, 10, 0, 4, -4, 4], icon=99, animation=22,
                      traits=[trait(22, 2, 0.1)]))

    # Zephyrine - staff/dagger
    upsert(wp, weapon(WP_TWIG, "A Good Twig",
                      "[Staff] Structurally, a stick. Magically, a slightly "
                      "better stick.", WT_STAFF, 30,
                      [0, 0, 3, 0, 10, 2, 0, 0], icon=101))
    upsert(wp, weapon(WP_WAND, "Secondhand Wand",
                      "[Staff] Still has the College's property stamp on it.",
                      WT_STAFF, 460, [0, 0, 5, 0, 26, 6, 2, 0], icon=109))
    upsert(wp, weapon(WP_STARFALL, "Unlicensed Starfall",
                      "[Staff] The College would like a word about this.",
                      WT_STAFF, 2500, [0, 0, 8, 2, 52, 12, 4, 0], icon=118,
                      animation=110, traits=[trait(23, 4, -0.15)]))

    # Nix - dagger/claw
    upsert(wp, weapon(WP_KNIFE, "Borrowed Knife",
                      "[Dagger] Nix means to give it back.", WT_DAGGER, 50,
                      [0, 0, 9, 0, 0, 0, 4, 2], icon=96))
    upsert(wp, weapon(WP_DIRK, "Quiet Dirk",
                      "[Dagger] Makes no noise at all, which is the expensive "
                      "part.", WT_DAGGER, 500,
                      [0, 0, 24, 2, 0, 0, 8, 6], icon=96,
                      traits=[trait(22, 2, 0.08)]))
    upsert(wp, weapon(WP_LAST_WORD, "Last Word",
                      "[Dagger] Ends discussions.", WT_DAGGER, 2300,
                      [0, 0, 44, 4, 0, 0, 14, 14], icon=112, animation=26,
                      traits=[trait(22, 2, 0.18), trait(22, 1, 0.06)]))

    # Aldric - spear
    upsert(wp, weapon(WP_LANCE, "Ancestral Lance",
                      "[Spear] Three generations of Pemberton-Gores have "
                      "carried this and none of them found the exit either.",
                      WT_SPEAR, 120, [0, 0, 14, 4, 0, 2, -2, 0], icon=107))
    upsert(wp, weapon(WP_HALBERD, "Halberd",
                      "[Spear] Reach, and a great deal of it.", WT_SPEAR, 700,
                      [0, 0, 32, 8, 0, 4, -2, 0], icon=107))
    upsert(wp, weapon(WP_OATHKEEPER, "Oathkeeper",
                      "[Spear] Sir Aldric swore on it once and has been "
                      "extremely careful with it since.", WT_SPEAR, 2400,
                      [0, 0, 54, 16, 0, 10, 0, 4], icon=119, animation=27,
                      traits=[atk_el(EL_LIGHT)]))

    # Piper - whip/dagger, but the numbers live in her support
    upsert(wp, weapon(WP_LUTE, "Dented Lute",
                      "[Whip] Swung by the neck. The strings survive this "
                      "better than you would think.", WT_WHIP, 70,
                      [0, 0, 8, 0, 8, 4, 4, 4], icon=199))
    upsert(wp, weapon(WP_FIDDLE, "Road Fiddle",
                      "[Whip] Loud enough to be heard over a battle, which is "
                      "the point.", WT_WHIP, 480,
                      [0, 0, 18, 2, 20, 10, 8, 8], icon=200))
    upsert(wp, weapon(WP_LEGEND, "The Instrument of Legend",
                      "[Whip] Piper wrote the legend first and then had the "
                      "instrument made to match.", WT_WHIP, 2400,
                      [0, 0, 34, 6, 40, 20, 14, 16], icon=200, animation=36,
                      traits=[atk_el(EL_WIND), trait(22, 1, 0.08)]))

    # Corvin - a sword he has been sharpening alone for eleven years
    upsert(wp, weapon(WP_NOTCHED, "Notched Black Sword",
                      "[Sword] Black, notched, and carried since he was "
                      "nineteen. He will not say where the notches came from.",
                      WT_SWORD, 300, [0, 0, 24, 0, 0, 0, 4, -4], icon=112,
                      traits=[atk_el(EL_DARK)]))
    upsert(wp, weapon(WP_GRUDGE, "Grudge",
                      "[Sword] Mrs Barrow has had it on the wall for years. "
                      "It is exactly one person's sort of thing.",
                      WT_SWORD, 1100, [0, 0, 46, 2, 0, 0, 8, -6], icon=97,
                      traits=[atk_el(EL_DARK), trait(22, 2, 0.1)]))
    upsert(wp, weapon(WP_FORETOLD, "The Foretold Blade",
                      "[Sword] Somebody's destiny, certainly. The label in the "
                      "cupboard says RIVAL and does not elaborate.",
                      WT_SWORD, 2600, [0, 0, 72, 4, 0, 0, 14, -8], icon=120,
                      animation=25,
                      traits=[atk_el(EL_DARK), trait(22, 2, 0.22)]))

    # Wren - bows, and one of them is a filing system
    upsert(wp, weapon(WP_CROSSBOW, "Field Crossbow",
                      "[Crossbow] Light, accurate, and fitted with a small "
                      "shelf for note-taking.", WT_CROSSBOW, 280,
                      [0, 0, 20, 2, 0, 2, 4, 4], icon=103))
    upsert(wp, weapon(WP_RECURVE, "Recurve Bow",
                      "[Bow] Draws further. She will explain why that matters "
                      "for longer than you want.", WT_BOW, 1000,
                      [0, 0, 40, 4, 0, 4, 10, 6], icon=102))
    upsert(wp, weapon(WP_CITATION, "The Final Citation",
                      "[Bow] The last word on a species, at ninety paces. "
                      "Labelled CATALOGUER in a very neat hand.",
                      WT_BOW, 2500, [0, 0, 62, 6, 0, 8, 18, 10], icon=102,
                      animation=114, traits=[trait(22, 2, 0.15)]))

    # Roland - one he practises with, and one he leaves behind
    upsert(wp, weapon(WP_PRACTICE, "Fairweather's Practice Sword",
                      "[Sword] The one he trains with. It is better than most "
                      "people's best sword and he is sorry about that.",
                      WT_SWORD, 900, [0, 0, 34, 6, 6, 6, 4, 6], icon=97))
    upsert(wp, weapon(WP_FAIRWEATHER, "Fairweather's Own",
                      "[Sword] Given away at the door of the tower by a man "
                      "with somewhere else to be. It is a very good sword.",
                      WT_SWORD, 3000, [0, 0, 64, 12, 10, 10, 8, 14], icon=113,
                      animation=25,
                      traits=[atk_el(EL_LIGHT), trait(22, 2, 0.12),
                              trait(22, 0, 0.05)]))
    upsert(wp, weapon(WP_FORTY_FOURTH, "The Forty-Fourth's Sword",
                      "[Sword] Grave goods. He was buried with it by a village "
                      "that had not written to him in forty years.",
                      WT_SWORD, 2800, [0, 0, 60, 10, 0, 8, 2, 8], icon=123,
                      animation=24, traits=[trait(22, 2, 0.1)]))

    # -- the north ----------------------------------------------------------
    # Icon 114 is the only spanner on the sheet: row 7, column 2, two nuts and
    # a jaw. Counted, not guessed.
    upsert(wp, weapon(WP_WRENCH, "Stillson Wrench",
                      "[Flail] Eighteen inches of works property. Miss Hoyle "
                      "wants it back and has said so in writing.",
                      WT_FLAIL, 1150, [0, 0, 44, 8, 0, 4, -2, 0], icon=114))
    # ITEM 1, rendered down. A flail, because that is what Bram can hold and
    # because eighteen pounds of casing on a shaft is not a sword; and the
    # best weapon in the north, because it was built to end the argument in
    # one go and in a sense it now does.
    upsert(wp, weapon(WP_NUMBER_ONE, "Number One",
                      "[Flail] The casing of ITEM 1, on a shaft. Miss Hoyle "
                      "stamped it 1 out of habit and then went very quiet.",
                      WT_FLAIL, 3400, [0, 0, 68, 14, 0, 10, 4, 6], icon=117,
                      animation=21,
                      traits=[trait(22, 2, 0.12), trait(22, 0, 0.05)]))
    # -- the companion quests' ----------------------------------------------
    # ROL-4: the same blade on an ash haft. An axe, because Hob's class takes
    # axes and nobody else's does - so it is his without a class being edited.
    upsert(wp, weapon(WP_REHAFTED, "Fairweather's Own, Rehafted",
                      "[Axe] A very good blade on an ash haft. Made in "
                      "Thistlewick forty years ago, and again last week.",
                      WT_AXE, 3000, [0, 0, 66, 12, 0, 8, 2, 10], icon=99,
                      animation=25,
                      traits=[atk_el(EL_LIGHT), trait(22, 2, 0.1)]))
    # HOB-2: the three markers he made for her and would not put up, melted
    # down. His best (QUESTS.md 0.5), and slower than it need be, on purpose.
    # An axe, as Beatrice II is: the one weapon type that is Hob's alone.
    upsert(wp, weapon(WP_SOMETHING_TO_SAY, "Something To Say",
                      "[Axe] Three grave markers, melted. The haft a shade "
                      "long, the face left rough: so she'd have something to say.",
                      WT_AXE, 0, [0, 0, 78, 12, 0, 6, -6, 12], icon=99,
                      animation=22,
                      traits=[trait(22, 2, 0.15)]))
    # HOB-4: the one thing the star-iron makes. A sword, which Hob's class
    # cannot hold - he made it knowing - and he will not say who it is for.
    upsert(wp, weapon(WP_STAR_IRON, "Star-Iron Sword",
                      "[Sword] A gatepost that fell out of the sky. Takes the "
                      "light like frost on a window. Hob won't say who for.",
                      WT_SWORD, 0, [0, 0, 66, 6, 8, 8, 6, 14], icon=119,
                      animation=6, traits=[trait(22, 2, 0.06)]))
    save("Weapons.json", wp)


def build_armors():
    ar = R.load("Armors.json")
    upsert(ar, armor(AR_SMOCK, "Farming Smock",
                     "[Light Armor] Sturdy, practical, covered in soil.",
                     ET_BODY, AT_LIGHT, 50, [0, 0, 0, 6, 0, 2, 0, 0], icon=135))
    upsert(ar, armor(AR_LEATHER, "Leather Jerkin",
                     "[Light Armor] Boiled leather. Quiet, cheap, adequate.",
                     ET_BODY, AT_LIGHT, 260, [0, 0, 0, 16, 0, 6, 2, 0],
                     icon=152))
    upsert(ar, armor(AR_CHAIN, "Chain Shirt",
                     "[Heavy Armor] Heavy, and worth it.",
                     ET_BODY, AT_HEAVY, 620, [30, 0, 0, 30, 0, 10, -2, 0],
                     icon=137))
    upsert(ar, armor(AR_PLATE, "Family Plate",
                     "[Heavy Armor] Polished daily by someone with time.",
                     ET_BODY, AT_HEAVY, 1600, [80, 0, 0, 52, 0, 20, -4, 0],
                     icon=137))
    upsert(ar, armor(AR_ROBE, "Sister's Habit",
                     "[Magic Armor] Practical, washable, deceptively warm.",
                     ET_BODY, AT_MAGIC, 240, [0, 20, 0, 10, 8, 18, 0, 0],
                     icon=136))
    upsert(ar, armor(AR_SILK, "Travelling Robe",
                     "[Magic Armor] Has more pockets than it appears to.",
                     ET_BODY, AT_MAGIC, 900, [0, 40, 0, 18, 20, 32, 2, 0],
                     icon=154))
    upsert(ar, armor(AR_BUCKLER, "Buckler",
                     "[Small Shield] A small round shield.",
                     ET_SHIELD, AT_SMALL_SHIELD, 180, [0, 0, 0, 10, 0, 4, 0, 0],
                     icon=128))
    upsert(ar, armor(AR_KITE_SHIELD, "Kite Shield",
                     "[Large Shield] Enough to stand behind.",
                     ET_SHIELD, AT_LARGE_SHIELD, 700,
                     [20, 0, 0, 26, 0, 10, -2, 0], icon=129,
                     traits=[trait(23, 1, 0.3)]))
    upsert(ar, armor(AR_HAT, "Wide Hat",
                     "[Magic Armor] Keeps the rain and the questions off.",
                     ET_HEAD, AT_MAGIC, 200, [0, 15, 0, 6, 8, 12, 0, 0],
                     icon=133))
    upsert(ar, armor(AR_HELM, "Great Helm",
                     "[Heavy Armor] Excellent protection, no peripheral "
                     "vision. This may explain a lot about Sir Aldric.",
                     ET_HEAD, AT_HEAVY, 640, [0, 0, 0, 24, 0, 8, -2, 0],
                     icon=132, traits=[trait(14, 5, 1)]))
    upsert(ar, armor(AR_CIRCLET, "Plain Circlet",
                     "[General Armor] Unassuming. Steadies the mind.",
                     ET_HEAD, AT_GENERAL, 800, [0, 25, 0, 12, 14, 20, 2, 4],
                     icon=148))
    upsert(ar, armor(AR_RING_LUCK, "Ring of Mild Fortune",
                     "[Accessory] Things go slightly your way.",
                     ET_ACCESSORY, AT_GENERAL, 900, [0, 0, 0, 0, 0, 0, 0, 24],
                     icon=145, traits=[trait(22, 2, 0.06)]))
    upsert(ar, armor(AR_RING_SPEED, "Hasty Ring",
                     "[Accessory] You arrive before you have decided to.",
                     ET_ACCESSORY, AT_GENERAL, 1100, [0, 0, 0, 0, 0, 0, 20, 0],
                     icon=147, traits=[trait(22, 1, 0.08)]))
    upsert(ar, armor(AR_AMULET, "Amulet of the Committee",
                     "[Accessory] Resists darkness, and most forms of "
                     "paperwork.",
                     ET_ACCESSORY, AT_GENERAL, 1400, [0, 20, 0, 8, 0, 20, 0, 0],
                     icon=146, traits=[trait(11, EL_DARK, 0.6),
                                       trait(14, 6, 1)]))
    upsert(ar, armor(AR_BOOTS, "Walking Boots",
                     "[Accessory] Broken in by somebody who walked a long way "
                     "in them and came back with opinions.",
                     ET_ACCESSORY, AT_GENERAL, 500, [20, 0, 0, 4, 0, 4, 12, 0],
                     icon=140))

    # -- the south ----------------------------------------------------------
    upsert(ar, armor(AR_OILSKIN, "Oilskin Coat",
                     "[Light Armor] Nether Sopping's answer to Nether "
                     "Sopping. Sheds water, weather and most opinions.",
                     ET_BODY, AT_LIGHT, 700, [20, 0, 0, 24, 0, 14, 0, 0],
                     icon=153, traits=[trait(11, EL_WATER, 0.6)]))
    upsert(ar, armor(AR_A_HAT, "A Hat",
                     "[General Armor] A hat. Form A-1 requires a hat and does "
                     "not say which, so Mrs Barrow sells this one.",
                     ET_HEAD, AT_GENERAL, 30, [0, 0, 0, 2, 0, 2, 0, 2],
                     icon=130))
    upsert(ar, armor(AR_LAMP, "Keeper's Lamp",
                     "[Accessory] A small lamp off a large lighthouse. It is "
                     "what the ones who come back walk home by.",
                     ET_ACCESSORY, AT_GENERAL, 1200, [0, 0, 0, 6, 0, 18, 0, 16],
                     icon=212, traits=[trait(11, EL_DARK, 0.6),
                                       trait(14, 13, 1)]))
    upsert(ar, armor(AR_LOCKET, "Feud Locket",
                     "[Accessory] Two sisters, one portrait each, facing "
                     "resolutely away. Thirty years of this.",
                     ET_ACCESSORY, AT_GENERAL, 1000,
                     [60, 0, 0, 8, 0, 12, 0, 8], icon=146,
                     traits=[trait(22, 7, 0.03)]))
    upsert(ar, armor(AR_FOOTNOTE, "Footnote",
                     "[Accessory] Hosea Bellwether has written you into the "
                     "history. Small type, bottom of the page, but there.",
                     ET_ACCESSORY, AT_GENERAL, 1300,
                     [0, 30, 0, 6, 16, 14, 4, 12], icon=224,
                     traits=[trait(22, 2, 0.05)]))
    upsert(ar, armor(AR_SIGNET, "The Forty-Fourth's Signet",
                     "[Accessory] Grave goods, given rather than taken, which "
                     "he was very particular about.",
                     ET_ACCESSORY, AT_GENERAL, 1800,
                     [80, 0, 0, 16, 0, 16, 4, 10], icon=145,
                     traits=[trait(11, EL_DARK, 0.5), trait(14, ST_SLEEP, 1),
                             trait(22, 2, 0.08)]))
    upsert(ar, armor(AR_KIT, "Ysolde's Kit",
                     "[Accessory] Forty years of field medicine in one canvas "
                     "roll. She does not need it any more. You will.",
                     ET_ACCESSORY, AT_GENERAL, 2200,
                     [120, 20, 0, 14, 0, 18, 6, 6], icon=187,
                     traits=[trait(22, 7, 0.06), trait(14, ST_POISON, 1),
                             trait(14, 7, 1)]))

    # -- the north ----------------------------------------------------------
    # There is no trousers icon on the sheet - row 8 and row 9 were counted
    # cell by cell and the wardrobe runs smock, robe, dress, coat, jacket. 152
    # is the long coat, and it is the garment icon nothing else is using.
    #
    # The description is the joke and it is a straight one: every set of body
    # armour in this game is a smock, a jerkin or a shirt of mail, and the
    # party has walked through a wood, a coast, a bog and a barrow in them.
    upsert(ar, armor(AR_TROUSERS, "Sensible Trousers",
                     "[General Armor] Nobody in this story is dressed for the "
                     "weather. These are. That is the whole of the pitch.",
                     ET_BODY, AT_GENERAL, 880, [0, 0, 0, 40, 0, 8, -2, 0],
                     icon=152, traits=[trait(11, EL_ICE, 0.7),
                                       trait(11, EL_WATER, 0.7)]))
    upsert(ar, armor(AR_WORKS_CAP, "Works Cap",
                     "[General Armor] The hooter sounds at six. A cap does "
                     "not help with that and everybody wears one anyway.",
                     ET_HEAD, AT_GENERAL, 240, [0, 0, 0, 10, 0, 6, 0, 2],
                     icon=150))
    # The other half of ITEM 1. She takes the fuse out first, before anything
    # else, and hands it over, and does not let go of it for a moment.
    upsert(ar, armor(AR_FUSE, "The Fuse (Removed)",
                     "[Accessory] Taken out first, before anything else was "
                     "touched. Carry it and you will not be surprised again.",
                     ET_ACCESSORY, AT_GENERAL, 2600,
                     [100, 20, 0, 12, 0, 14, 12, 16], icon=215,
                     traits=[trait(22, 1, 0.08), trait(22, 2, 0.06),
                             trait(14, 13, 1)]))
    # Given rather than taken, which is the Barrow's rhyme in a different key:
    # nobody strips Attempt Eighty-Four. Ott takes it off her while rebuilding
    # her, and says it is coming off anyway.
    upsert(ar, armor(AR_GOVERNOR, "Governor",
                     "[Accessory] A brass ball governor off Attempt Eighty-"
                     "Four. It kept her from running away with herself.",
                     ET_ACCESSORY, AT_GENERAL, 2200,
                     [60, 0, 0, 14, 0, 14, 18, 4], icon=163,
                     traits=[trait(23, 6, 0.92), trait(14, 8, 1)]))
    save("Armors.json", ar)


# ============================================================== bestiary ====
def build_enemies():
    en = R.load("Enemies.json")
    base = [trait(22, 0, 0.95), trait(22, 1, 0.05)]

    upsert(en, enemy(
        EN_TURNIP, "Militant Turnip", "Matango", 60,
        [420, 0, 30, 12, 8, 8, 10, 5], 45, 60,
        [action(SK_ATTACK, 6), action(SK_NIBBLE, 4)],
        traits=base + [trait(11, EL_FIRE, 1.5)],
        drops=[drop(0, IT_TURNIP, 1)],
        note="A turnip that has had enough. Bram takes this personally."))

    upsert(en, enemy(
        EN_CROW, "Crow of Foreshadowing", "Crow", 0,
        [380, 20, 28, 8, 18, 12, 26, 12], 65, 80,
        [action(SK_ATTACK, 5), action(SK_SHRIEK, 3)],
        traits=base + [trait(22, 1, 0.2), trait(11, EL_WIND, 1.5)],
        drops=[drop(0, IT_POTION, 4)],
        note="Caws exactly three times whenever anything important is about "
             "to happen, which is exhausting for everyone."))

    upsert(en, enemy(
        EN_GOBLIN, "Disgruntled Goblin", "Goblin", 0,
        [560, 0, 34, 18, 8, 12, 16, 8], 75, 110,
        [action(SK_ATTACK, 6)],
        traits=base + [trait(31, EL_PHYSICAL, 0)],
        drops=[drop(0, IT_POTION, 3)],
        note="Has a list of grievances and will read from it."))

    upsert(en, enemy(
        EN_BANDIT, "Bandit (Trainee)", "Mercenary", 0,
        [700, 20, 38, 22, 10, 14, 22, 14], 90, 170,
        [action(SK_ATTACK, 6), action(SK_NIBBLE, 2)],
        traits=base + [trait(22, 1, 0.12)],
        drops=[drop(0, IT_POTION, 2), drop(1, WP_KNIFE, 12)],
        note="On the fourth week of a six-week banditry apprenticeship."))

    upsert(en, enemy(
        EN_WISP, "Wisp of Mild Concern", "Plasma", 210,
        [460, 60, 20, 10, 40, 30, 30, 10], 60, 95,
        [action(SK_EMBER, 5), action(SK_DRAIN, 3)],
        traits=base + [trait(11, EL_PHYSICAL, 0.4), trait(11, EL_LIGHT, 2.0),
                       trait(22, 1, 0.25)],
        drops=[drop(0, IT_ETHER, 5)],
        note="Hovers nearby looking worried. Attacks anyway."))

    upsert(en, enemy(
        EN_TREANT, "Grumblewood Treant", "Treant", 0,
        [1300, 40, 44, 34, 20, 24, 8, 10], 180, 280,
        [action(SK_ATTACK, 5), action(SK_ROOT_GRAB, 4)],
        traits=base + [trait(11, EL_FIRE, 2.0), trait(11, EL_EARTH, 0.3),
                       trait(23, 6, 0.8)],
        drops=[drop(0, IT_HI_POTION, 4)],
        note="Objects to being walked past."))

    upsert(en, enemy(
        EN_BAT, "Tower Bat", "Crow", 180,
        [420, 0, 32, 10, 10, 10, 34, 10], 60, 80,
        [action(SK_ATTACK, 6)],
        traits=base + [trait(22, 1, 0.3)],
        note="There are always bats. It is in the contract."))

    upsert(en, enemy(
        EN_SKELETON, "Skeleton (Intern)", "Zombie", 40,
        [800, 30, 44, 26, 16, 18, 14, 6], 130, 190,
        [action(SK_ATTACK, 6), action(SK_DRAIN, 2)],
        traits=base + [trait(11, EL_LIGHT, 2.0), trait(11, EL_DARK, 0.2),
                       trait(11, EL_FIRE, 1.3)],
        drops=[drop(0, IT_POTION, 3)],
        note="Unpaid. Six months, 'for the experience'."))

    upsert(en, enemy(
        EN_GARGOYLE, "Load-Bearing Gargoyle", "Stoneknight", 0,
        [1400, 40, 52, 44, 22, 30, 12, 10], 220, 320,
        [action(SK_ATTACK, 5), action(SK_INEVITABILITY, 2)],
        traits=base + [trait(11, EL_PHYSICAL, 0.6), trait(11, EL_EARTH, 0.5),
                       trait(11, EL_THUNDER, 1.6), trait(23, 6, 0.7)],
        drops=[drop(0, IT_HI_POTION, 3)],
        note="Structurally important. Attacks anyway, which raises questions "
             "about the tower."))

    upsert(en, enemy(
        EN_MIMIC, "Chest (Definitely A Chest)", "Mimic", 0,
        [1800, 40, 58, 30, 40, 26, 26, 30], 320, 900,
        [action(SK_ATTACK, 6), action(SK_NIBBLE, 3)],
        traits=base + [trait(11, EL_FIRE, 1.4)],
        drops=[drop(0, IT_ELIXIR, 1), drop(2, AR_RING_LUCK, 2)],
        note="It was going to be a chest. It is not a chest."))

    # -- the south coast, the pit and the barrow -----------------------------
    upsert(en, enemy(
        EN_CRAB, "Territorial Crab", "Crab", 0,
        [480, 0, 30, 22, 6, 14, 12, 8], 70, 100,
        [action(SK_ATTACK, 5), action(SK_PINCH, 4)],
        traits=base + [trait(11, EL_PHYSICAL, 0.6), trait(11, EL_THUNDER, 1.8),
                       trait(23, 6, 0.8)],
        drops=[drop(0, IT_CHOWDER, 8)],
        note="The beach is its beach. It has held this position, without "
             "documentation, since before the village."))

    upsert(en, enemy(
        EN_GULL, "Gull With Ambitions", "Harpy", 30,
        [340, 20, 26, 10, 14, 12, 34, 14], 60, 85,
        [action(SK_ATTACK, 5), action(SK_SWOOP, 4)],
        traits=base + [trait(22, 1, 0.28), trait(11, EL_WIND, 0.5)],
        drops=[drop(0, IT_BISCUIT, 5)],
        note="Has worked out that adventurers carry food and that "
             "adventurers are, as a class, slow."))

    upsert(en, enemy(
        EN_SANDTHING, "Something In The Sand", "Sandworm", 0,
        [760, 30, 36, 20, 12, 18, 16, 6], 110, 170,
        [action(SK_ATTACK, 5), action(SK_ROOT_GRAB, 3)],
        traits=base + [trait(11, EL_EARTH, 0.4), trait(11, EL_ICE, 1.5)],
        drops=[drop(0, IT_POTION, 3)],
        note="Nether Sopping does not swim off this beach and has never "
             "written down why."))

    upsert(en, enemy(
        EN_LOST_PROPERTY, "Lost Property", "Demonpot", 0,
        [560, 20, 32, 24, 14, 16, 14, 10], 85, 140,
        [action(SK_ATTACK, 5), action(SK_RUMMAGE, 4)],
        traits=base + [trait(11, EL_PHYSICAL, 0.7), trait(11, EL_FIRE, 1.4)],
        drops=[drop(0, IT_POTION, 3)],
        note="Two hundred years at the bottom of a pit will do this to "
             "anything, apparently, including an urn."))

    upsert(en, enemy(
        EN_HOUND, "Barrow Hound", "Wolfman", 200,
        [740, 0, 46, 20, 10, 16, 32, 10], 140, 160,
        [action(SK_ATTACK, 6), action(SK_NIBBLE, 3)],
        traits=base + [trait(22, 1, 0.18), trait(11, EL_LIGHT, 1.5),
                       trait(11, EL_DARK, 0.4)],
        drops=[drop(0, IT_HI_POTION, 5)],
        note="Buried with him, which nobody asked the hound about."))

    upsert(en, enemy(
        EN_OCCUPANT, "Previous Occupant", "Wraith", 0,
        [880, 80, 40, 24, 38, 30, 24, 12], 170, 210,
        [action(SK_ATTACK, 4), action(SK_GRAVE_DUTY, 5),
         action(SK_DRAIN, 3)],
        traits=base + [trait(11, EL_PHYSICAL, 0.5), trait(11, EL_LIGHT, 2.0),
                       trait(11, EL_DARK, 0.1), trait(22, 1, 0.2)],
        drops=[drop(0, IT_ETHER, 4)],
        note="Was in the mound first. Has views about the extension."))

    upsert(en, enemy(
        EN_GRAVE_GOODS, "Grave Goods (Animated)", "Blackknight", 0,
        [1500, 40, 54, 42, 20, 30, 16, 10], 230, 300,
        [action(SK_ATTACK, 5), action(SK_WHATS_DONE, 3)],
        traits=base + [trait(11, EL_PHYSICAL, 0.6), trait(11, EL_THUNDER, 1.6),
                       trait(23, 6, 0.75)],
        drops=[drop(0, IT_HI_POTION, 3)],
        note="A full suit of armour, buried with a man who would have "
             "preferred the money."))

    # -- bosses --------------------------------------------------------------
    upsert(en, enemy(
        EN_THING, "The Thing In The Woods", "Hydra", 0,
        [3600, 200, 44, 36, 34, 34, 24, 20], 900, 1400,
        [action(SK_ATTACK, 5), action(SK_ROOT_GRAB, 4),
         action(SK_SHRIEK, 3, condition=1, p1=50)],
        traits=base + [trait(11, EL_FIRE, 1.6), trait(11, EL_LIGHT, 1.3),
                       trait(23, 6, 0.85), trait(14, ST_SLEEP, 1),
                       trait(62, 3, 0)],
        drops=[drop(0, IT_ELIXIR, 1)],
        note="Nobody in Thistlewick has ever agreed on what it is, only that "
             "it is in the woods and it is a thing."))

    upsert(en, enemy(
        EN_GRIMSPITE, "Grimspite the Inevitable", "Demoncount", 0,
        [7000, 400, 58, 48, 52, 48, 34, 24], 2000, 3000,
        [action(SK_ATTACK, 5), action(SK_INEVITABILITY, 4),
         action(SK_DOOM_MONOLOGUE, 4),
         action(SK_SMALL_PRINT, 3, condition=1, p1=40)],
        traits=base + [trait(11, EL_DARK, 0.2), trait(11, EL_LIGHT, 1.5),
                       trait(14, ST_SLEEP, 1), trait(14, 6, 1),
                       trait(62, 3, 0), trait(23, 6, 0.9)],
        note="Four thousand eight hundred years into a renewable engagement. "
             "Tired in a way that does not show up on a stat block."))

    upsert(en, enemy(
        EN_PROPHECY, "THE PROPHECY", "Evilbook", 0,
        [9000, 999, 50, 52, 72, 58, 40, 30], 2500, 4000,
        [action(SK_CLAUSE_TWELVE, 5), action(SK_ERRATUM, 4),
         action(SK_DOOM_MONOLOGUE, 3),
         action(SK_SMALL_PRINT, 4, condition=1, p1=50)],
        traits=base + [trait(11, EL_PHYSICAL, 0.7), trait(11, EL_DARK, 0.1),
                       trait(11, EL_LIGHT, 1.4), trait(11, EL_FIRE, 1.6),
                       trait(14, ST_SLEEP, 1), trait(14, 6, 1), trait(14, 5, 1),
                       trait(62, 3, 0), trait(61, 0, 1)],
        note="Clause twelve enforces itself. That is the whole problem."))
    # -- the four optional ones ----------------------------------------------
    upsert(en, enemy(
        EN_BADGER, "The Thing At The Bottom", "SF_Brownbear", 0,
        [3000, 60, 48, 34, 16, 22, 26, 14], 560, 900,
        [action(SK_ATTACK, 6), action(SK_OPINION, 4),
         action(SK_RUMMAGE, 3)],
        traits=base + [trait(11, EL_EARTH, 0.5), trait(11, EL_FIRE, 1.4),
                       trait(23, 6, 0.85), trait(62, 3, 0)],
        drops=[drop(0, IT_ELIXIR, 3)],
        note="A badger. An enormous one, admittedly, and it has been eating "
             "two centuries of lost property, which cannot have helped."))

    upsert(en, enemy(
        EN_BIG_CRAB, "The Crab Of Unusual Size", "Crab", 220,
        [3000, 0, 52, 46, 10, 26, 18, 12], 620, 1100,
        [action(SK_ATTACK, 5), action(SK_PINCH, 5),
         action(SK_INEVITABILITY, 3, condition=1, p1=50)],
        traits=base + [trait(11, EL_PHYSICAL, 0.5), trait(11, EL_THUNDER, 1.8),
                       trait(23, 6, 0.75), trait(62, 3, 0)],
        drops=[drop(2, AR_OILSKIN, 1)],
        note="The bounty says 'unusual'. Everyone in Nether Sopping wants it "
             "on record that they said 'unusual' and not 'large'."))

    upsert(en, enemy(
        EN_CROOKE, "Meredith Crooke", "Actor3_2", 0,
        [3200, 120, 56, 38, 24, 28, 34, 20], 700, 1400,
        [action(SK_ATTACK, 5), action(SK_TRIBUTE, 4),
         action(SK_INEVITABILITY, 3, condition=1, p1=40)],
        traits=base + [trait(22, 1, 0.14), trait(61, 0, 1), trait(62, 3, 0)],
        drops=[drop(1, WP_GRUDGE, 2), drop(0, IT_HI_POTION, 1)],
        note="Runs the six-week banditry apprenticeship. Has a syllabus, a "
             "marking rubric, and an unusually loyal cohort."))

    upsert(en, enemy(
        EN_FORTY_FOURTH, "The Forty-Fourth", "Highking", 0,
        [6400, 300, 62, 48, 36, 42, 30, 22], 1800, 2400,
        [action(SK_ATTACK, 5), action(SK_WHATS_DONE, 4),
         action(SK_GRAVE_DUTY, 3),
         action(SK_INEVITABILITY, 4, condition=1, p1=40)],
        traits=base + [trait(11, EL_DARK, 0.3), trait(11, EL_LIGHT, 1.4),
                       trait(14, ST_SLEEP, 1), trait(62, 3, 0),
                       trait(23, 6, 0.85)],
        drops=[drop(1, WP_FORTY_FOURTH, 1), drop(2, AR_SIGNET, 1)],
        note="Chosen One #44. Came home, was pensioned south, died old and "
             "unwritten-to, and was then given a barrow with a curse on it "
             "because that is what you do with a hero."))

    # -- the north ------------------------------------------------------------
    # Everything in the Long Field is a machine that has not been told it has
    # stopped, and everything aboard Attempt 199 is a system that is still
    # sound. Nothing up here is a monster and nothing up here is angry: they
    # are all doing the job they were built for, in a place where the job no
    # longer applies, which is also what the town is doing.
    upsert(en, enemy(
        EN_PRESSURE, "Loose Pressure", "Plasma", 40,
        [900, 0, 44, 20, 30, 24, 62, 8], 200, 160,
        [action(SK_ATTACK, 4), action(SK_SCALD, 6)],
        traits=base + [trait(11, EL_FIRE, 0.2), trait(11, EL_ICE, 1.6),
                       trait(11, EL_WATER, 1.5), trait(11, EL_PHYSICAL, 0.6),
                       trait(14, ST_POISON, 1), trait(14, ST_SLEEP, 1),
                       trait(22, 1, 0.2)],
        drops=[drop(0, IT_ETHER, 5)],
        note="A hundred and forty years of stored steam, finding the way out "
             "all at once. It is not attacking anybody. It is just leaving."))

    upsert(en, enemy(
        EN_UNNUMBERED, "Attempt (Unnumbered)", "Machinerybee", 0,
        [1150, 0, 56, 36, 12, 26, 54, 18], 240, 220,
        [action(SK_ATTACK, 5), action(SK_STILL_TRYING, 5)],
        traits=base + [trait(11, EL_THUNDER, 1.4), trait(11, EL_EARTH, 0.6),
                       trait(14, ST_POISON, 1), trait(14, ST_SLEEP, 1),
                       trait(22, 1, 0.15)],
        drops=[drop(0, IT_POTION, 3)],
        note="Too early to have been given a number. It has been getting one "
             "foot off the ground since before anybody now alive was born."))

    upsert(en, enemy(
        EN_SALVAGE, "Ambulant Salvage", "Mechascorpion", 25,
        [1600, 0, 62, 52, 10, 34, 30, 12], 300, 300,
        [action(SK_ATTACK, 5), action(SK_SHED_A_PART, 4),
         action(SK_SCALD, 3, condition=1, p1=40)],
        traits=base + [trait(11, EL_PHYSICAL, 0.7), trait(11, EL_ICE, 1.4),
                       trait(11, EL_FIRE, 0.6),
                       trait(14, ST_POISON, 1), trait(14, ST_SLEEP, 1),
                       trait(23, 6, 0.85)],
        drops=[drop(0, IT_HI_POTION, 4)],
        note="Parts of nine different attempts, walking. Nobody assembled it "
             "and nobody can prove it was not assembled."))

    upsert(en, enemy(
        EN_84, "Attempt Eighty-Four", "SF_Slaughterrobot", 0,
        [7600, 400, 70, 64, 16, 44, 26, 10], 2200, 3000,
        [action(SK_ATTACK, 5), action(SK_DUE_NORTH, 5),
         action(SK_OVERPRESSURE, 4),
         action(SK_MAKE_GOOD, 4, condition=1, p1=45),
         action(SK_SHED_A_PART, 3)],
        traits=base + [trait(11, EL_PHYSICAL, 0.7), trait(11, EL_FIRE, 0.4),
                       trait(11, EL_ICE, 1.5), trait(11, EL_WATER, 1.3),
                       trait(11, EL_DARK, 0.6), trait(11, EL_LIGHT, 0.8),
                       trait(14, ST_POISON, 1), trait(14, ST_SLEEP, 1),
                       trait(14, 8, 1), trait(62, 3, 0),
                       trait(23, 6, 0.75), trait(23, 7, 1.15)],
        note="Came down in the Long Field in 1860 and has been repairing "
             "herself out of her neighbours ever since. Still has pressure. "
             "Still, faintly, trying to go north."))
    save("Enemies.json", en)


def build_troops():
    tr = R.load("Troops.json")
    upsert(tr, troop(TR_TURNIPS, "Militant Turnip*3",
                     [(EN_TURNIP, 200, 340), (EN_TURNIP, 380, 400),
                      (EN_TURNIP, 560, 350)]))
    upsert(tr, troop(TR_CROWS, "Crow*2",
                     [(EN_CROW, 250, 320), (EN_CROW, 520, 380)]))
    upsert(tr, troop(TR_FIELD_MIX, "Turnip*2, Crow",
                     [(EN_TURNIP, 200, 380), (EN_TURNIP, 400, 340),
                      (EN_CROW, 580, 360)]))
    upsert(tr, troop(TR_GOBLINS, "Goblin*2",
                     [(EN_GOBLIN, 260, 370), (EN_GOBLIN, 520, 400)]))
    upsert(tr, troop(TR_BANDITS, "Bandit*2, Goblin",
                     [(EN_BANDIT, 220, 350), (EN_GOBLIN, 400, 400),
                      (EN_BANDIT, 580, 360)]))
    upsert(tr, troop(TR_WOOD_MIX, "Treant, Wisp*2",
                     [(EN_WISP, 200, 330), (EN_TREANT, 400, 400),
                      (EN_WISP, 600, 340)]))
    upsert(tr, troop(TR_WISPS, "Wisp*3",
                     [(EN_WISP, 220, 340), (EN_WISP, 400, 390),
                      (EN_WISP, 580, 330)]))
    upsert(tr, troop(TR_SKELETONS, "Skeleton*2, Bat",
                     [(EN_SKELETON, 240, 370), (EN_BAT, 410, 300),
                      (EN_SKELETON, 570, 390)]))
    upsert(tr, troop(TR_GARGOYLES, "Gargoyle, Skeleton",
                     [(EN_GARGOYLE, 300, 390), (EN_SKELETON, 540, 360)]))
    upsert(tr, troop(TR_TOWER_MIX, "Gargoyle, Bat*2",
                     [(EN_BAT, 210, 300), (EN_GARGOYLE, 400, 400),
                      (EN_BAT, 590, 310)]))
    upsert(tr, troop(TR_MIMIC, "Chest (Definitely A Chest)",
                     [(EN_MIMIC, 400, 380)]))
    upsert(tr, troop(TR_THING, "The Thing In The Woods",
                     [(EN_THING, 400, 400)]))
    upsert(tr, troop(TR_GRIMSPITE, "Grimspite the Inevitable",
                     [(EN_GRIMSPITE, 400, 400)]))
    upsert(tr, troop(TR_PROPHECY, "THE PROPHECY",
                     [(EN_PROPHECY, 400, 380)]))
    # -- the south ------------------------------------------------------------
    upsert(tr, troop(TR_CRABS, "Territorial Crab*2",
                     [(EN_CRAB, 260, 380), (EN_CRAB, 540, 400)]))
    upsert(tr, troop(TR_GULLS, "Gull*3",
                     [(EN_GULL, 210, 330), (EN_GULL, 400, 380),
                      (EN_GULL, 590, 320)]))
    upsert(tr, troop(TR_COAST_MIX, "Something In The Sand, Gull*2",
                     [(EN_GULL, 220, 330), (EN_SANDTHING, 410, 400),
                      (EN_GULL, 600, 340)]))
    upsert(tr, troop(TR_PIT_MIX, "Lost Property*2, Bat",
                     [(EN_LOST_PROPERTY, 240, 380), (EN_BAT, 410, 300),
                      (EN_LOST_PROPERTY, 570, 400)]))
    upsert(tr, troop(TR_BARROW_MIX, "Grave Goods, Barrow Hound",
                     [(EN_GRAVE_GOODS, 300, 400), (EN_HOUND, 550, 370)]))
    upsert(tr, troop(TR_WRAITHS, "Previous Occupant*2",
                     [(EN_OCCUPANT, 270, 360), (EN_OCCUPANT, 540, 390)]))
    upsert(tr, troop(TR_GRAVE_GOODS, "Barrow Hound*2, Occupant",
                     [(EN_HOUND, 220, 350), (EN_OCCUPANT, 400, 390),
                      (EN_HOUND, 590, 360)]))

    upsert(tr, troop(TR_BADGER, "The Thing At The Bottom",
                     [(EN_BADGER, 400, 400)]))
    upsert(tr, troop(TR_BIG_CRAB, "The Crab Of Unusual Size",
                     [(EN_BIG_CRAB, 400, 400), (EN_CRAB, 180, 350),
                      (EN_CRAB, 620, 360)]))
    upsert(tr, troop(TR_CROOKE, "Meredith Crooke and the Fourth Week",
                     [(EN_CROOKE, 400, 400), (EN_BANDIT, 190, 350),
                      (EN_BANDIT, 610, 360)]))
    upsert(tr, troop(TR_FORTY_FOURTH, "The Forty-Fourth",
                     [(EN_FORTY_FOURTH, 400, 400)]))

    # -- the north ------------------------------------------------------------
    upsert(tr, troop(TR_PRESSURE, "Loose Pressure*3",
                     [(EN_PRESSURE, 220, 340), (EN_PRESSURE, 400, 390),
                      (EN_PRESSURE, 580, 330)]))
    upsert(tr, troop(TR_UNNUMBERED, "Attempt (Unnumbered)*2",
                     [(EN_UNNUMBERED, 260, 350), (EN_UNNUMBERED, 540, 390)]))
    upsert(tr, troop(TR_SALVAGE, "Ambulant Salvage, Loose Pressure",
                     [(EN_PRESSURE, 210, 330), (EN_SALVAGE, 450, 400)]))
    upsert(tr, troop(TR_CRAG_MIX, "Ambulant Salvage, Attempt*2",
                     [(EN_UNNUMBERED, 200, 330), (EN_SALVAGE, 410, 400),
                      (EN_UNNUMBERED, 600, 340)]))
    upsert(tr, troop(TR_84, "Attempt Eighty-Four",
                     [(EN_84, 400, 400)]))
    save("Troops.json", tr)


def build_common_events():
    """Two small ones. `Reallocate` needs script because Change Gold cannot
    read the enemy it was used on, and eating a turnip is a running joke that
    has to count itself."""
    ce = R.load("CommonEvents.json")

    steal = R.script([
        "const g = 30 + Math.floor(Math.random() * 120);",
        "$gameParty.gainGold(g);",
        "$gameVariables.setValue(%d, g);" % 10,
    ])
    steal += R.text(["Nix reallocates \\C[3]\\V[10]\\C[0]\\G."])
    upsert(ce, {"id": CE_STEAL_GOLD, "name": "Reallocate: gold",
                "switchId": 1, "trigger": 0,
                "list": steal + [{"code": 0, "indent": 0, "parameters": []}]})

    eaten = [R.control_variable_add(VAR_TURNIPS, 1)]
    upsert(ce, {"id": CE_TURNIP_EATEN, "name": "Turnip eaten",
                "switchId": 1, "trigger": 0,
                "list": eaten + [{"code": 0, "indent": 0, "parameters": []}]})
    # MER-2's examination. Its dialogue lives with the quest; imported here,
    # not at the top, because q_merribell imports this module.
    import q_merribell
    upsert(ce, {"id": CE_FIT_TO_TRAVEL, "name": "Fit To Travel (MER-2)",
                "switchId": 1, "trigger": 0,
                "list": q_merribell.examination() +
                [{"code": 0, "indent": 0, "parameters": []}]})
    save("CommonEvents.json", ce)


# ===================================================== Firstfield Meadow =====
def build_firstfield():
    """The tutorial's whole database: two sticks, a certificate, and a man
    who loses for a living.

    Norbert's fight is written to be won. His turns alternate between saying
    what he is about to do and doing one point of damage, and his HP is set so
    that a party of the level that can reach the meadow at all - anybody who
    has walked out of the village gate - takes him down in two or three turns.
    The battle is started with "can lose" on anyway, because a tutorial that
    can end the game is the one cliche this one is not doing."""
    sk = R.load("Skills.json")
    upsert(sk, skill(SK_TELEGRAPH, "Telegraph", "",
                     "0", dmg_type=0, scope=11, animation=0, hit_type=0,
                     message="%1 winds up. Next turn: an ENORMOUS swing."))
    upsert(sk, skill(SK_ENORMOUS_SWING, "Enormous Swing", "",
                     "1", scope=1, animation=1, variance=0,
                     message="%1 lands the ENORMOUS swing, as promised!"))
    save("Skills.json", sk)

    ar = R.load("Armors.json")
    upsert(ar, armor(AR_STICK, "A Stick",
                     "[Accessory] It is dangerous to go alone. Carried, "
                     "rather than wielded. Nobody knows why.",
                     ET_ACCESSORY, AT_GENERAL, 1, [0, 0, 1, 0, 0, 0, 0, 0],
                     icon=292))
    upsert(ar, armor(AR_STRAIGHTER_STICK, "A Straighter Stick",
                     "[Accessory] Nell picked this one out specially. It is "
                     "noticeably straighter.",
                     ET_ACCESSORY, AT_GENERAL, 2, [0, 0, 2, 0, 0, 0, 0, 1],
                     icon=292))
    upsert(ar, armor(AR_CERTIFICATE, "Certificate of Completion",
                     "[Accessory] For walking, talking, opening and hitting. "
                     "The first one the Guild of Guides has issued.",
                     ET_ACCESSORY, AT_GENERAL, 0, [0, 0, 0, 0, 0, 0, 0, 5],
                     icon=191))
    # -- the companion quests' (40-59) -------------------------------------
    # WRE-3: honorary membership. Wren only (AT_BADGE). A small sharp eye and
    # a great deal of luck, which is what forty years of looking comes to.
    upsert(ar, armor(AR_SOCIETY_BADGE, "Gloamwood Society Badge",
                     "[Accessory] Honorary member. Enamel: a Thing with nine "
                     "heads, all of them busy. The only one ever given away.",
                     ET_ACCESSORY, AT_BADGE, 0, [0, 0, 0, 0, 0, 0, 4, 12],
                     icon=146, traits=[trait(22, 0, 0.05)]))
    # MER-1: Merribell's gear. An accessory of a type only her actor has: the
    # Order's founding document, Mother Ursula Pym's own copy. Healing +, as
    # COMPANIONS.md has it - pharmacology x1.25, so what she gives out does a
    # quarter more, and a little MAT for what she casts.
    upsert(ar, armor(AR_PAMPHLET, "The Pamphlet",
                     "[Pamphlet] Mother Ursula Pym, 1702. Four pages, stitched, "
                     "damp at the corners. The Rule of Life is on the first.",
                     ET_ACCESSORY, AT_PAMPHLET, 0, [0, 20, 0, 0, 12, 8, 0, 0],
                     icon=189, traits=[trait(23, 3, 1.25)]))
    # MER-3: the Table's Kit - a candle-end, a coil of gut string, a splint
    # and a very good sash, in canvas. Anybody's; it goes to the youngest.
    upsert(ar, armor(AR_TABLE_KIT, "The Table's Kit",
                     "[Accessory] A candle-end, a coil of gut string, a splint "
                     "and a very good sash, rolled up in canvas.",
                     ET_ACCESSORY, AT_GENERAL, 0,
                     [60, 10, 0, 10, 0, 10, 0, 0], icon=187,
                     traits=[trait(23, 2, 1.15), trait(22, 7, 0.04)]))
    upsert(ar, armor(AR_LORRIMER_TOOLS, "Lorrimer's Tools",
                     "[Accessory] Picks, a jemmy, a hood-pin and a list of "
                     "things he meant to take. Left in a huff; located.",
                     ET_ACCESSORY, AT_GENERAL, 0,
                     [0, 0, 6, 0, 0, 0, 14, 10], icon=208,
                     traits=[trait(22, 2, 0.05), trait(22, 1, 0.03)]))
    save("Armors.json", ar)

    en = R.load("Enemies.json")
    upsert(en, enemy(
        EN_NORBERT, "Norbert", "Norbert_Pelling", 0,
        [260, 0, 12, 4, 1, 4, 1, 1], 5, 12,
        # Turn 0 and every even turn he announces; every odd turn he delivers.
        # `meetsTurnCondition` with a span of 0 is "exactly this turn", and
        # with a span it needs n > 0, which is why turn 0 has its own entry.
        [action(SK_TELEGRAPH, 5, condition=1, p1=0, p2=0),
         action(SK_TELEGRAPH, 5, condition=1, p1=2, p2=2),
         action(SK_ENORMOUS_SWING, 5, condition=1, p1=1, p2=2)],
        drops=[drop(0, IT_POTION, 1)],
        note="Guild of Guides contractor. Three thousand, one hundred and four "
             "professional losses and no wins, which is the job."))
    save("Enemies.json", en)

    tr = R.load("Troops.json")
    fizz = lambda lines: R.text(lines, face_name="Gen_People1", face_index=0)
    norbert = lambda lines: R.text(lines, face_name="Gen_People1", face_index=1)
    # His hit points are sized at the start of the fight, to the party that
    # turned up: about two and a half turns of it. A fixed number is either a
    # formality for four people at level twelve or a slog for two at level
    # four, and either way the swing he has been announcing never lands.
    size_him = R.script([
        "const e = $gameTroop.members()[0];",
        "const want = 90 * $gameParty.highestLevel() * "
        "$gameParty.battleMembers().length;",
        "e.addParam(0, Math.max(0, want - e.mhp));",
        "e.setHp(e.mhp);",
    ])
    turn0 = size_him + (fizz(["\\C[6]Fizz:\\C[0] This is a BATTLE!",
                   "Pick ATTACK to ATTACK!",
                   "Pick GUARD to GUARD!",
                   "Pick RUN to... he'd understand."]) +
             norbert(["\\C[6]Norbert:\\C[0] Take your time.",
                      "No rush. I'm on till four."]))
    halfway = norbert(["\\C[6]Norbert:\\C[0] Oof! Good one!",
                       "Textbook, that. Textbook."])
    pages = [
        {"conditions": dict(BLANK_TROOP_CONDITIONS, turnValid=True,
                            turnA=0, turnB=0),
         "list": turn0 + [{"code": 0, "indent": 0, "parameters": []}],
         "span": 0},
        {"conditions": dict(BLANK_TROOP_CONDITIONS, enemyValid=True,
                            enemyIndex=0, enemyHp=50),
         "list": halfway + [{"code": 0, "indent": 0, "parameters": []}],
         "span": 0},
    ]
    upsert(tr, troop(TR_NORBERT, "Norbert (Tutorial)",
                     [(EN_NORBERT, 400, 400)], pages=pages))
    save("Troops.json", tr)


def build():
    build_classes()
    build_actors()
    build_skills()
    build_states()
    build_items()
    build_weapons()
    build_armors()
    build_enemies()
    build_troops()
    build_common_events()
    build_firstfield()
    build_contest()
    build_monograph()
    build_vigil()
    build_worm()
    build_spare()
    build_mothballs()


# ================================================= the companion quests ======
def build_contest():
    """PIP-3, the Contest at the Sign of the Bell (QUESTS.md B3): a fight in
    which the damage type is heckling. Two rival acts and the back table, and
    Piper's buffs and debuffs are the whole of her kit - which they already
    were. Their hit points are the room's patience with them; and it is
    started with "can lose" on, because losing the room is a thing that
    happens to a bard. Piper fights it alone (P1): the party is the floor."""
    sk = R.load("Skills.json")
    upsert(sk, skill(SK_HECKLE, "Heckle", "", "a.atk * 2 - b.mdf",
                     hit_type=2, animation=0,
                     message="%1 shouts GET OFF at %2!"))
    upsert(sk, skill(SK_TALK_THROUGH, "Talks Through It", "", "0",
                     dmg_type=0, hit_type=2, animation=0,
                     effects=[effect(32, 4, 3)],
                     message="%1 talks loudly through the quiet bit."))
    upsert(sk, skill(SK_SERPENT, "Serpent Solo", "", "a.mat * 2 - b.mdf",
                     scope=2, hit_type=2, animation=0,
                     message="%1 plays the serpent, which is a sort of "
                             "bassoon that has given up."))
    upsert(sk, skill(SK_SAD_VERSE, "A Very Sad Verse", "", "a.mat * 2",
                     scope=2, dmg_type=2, hit_type=2, animation=0,
                     message="%1 sings a verse in which everybody dies, "
                             "including the narrator."))
    upsert(sk, skill(SK_ENCORE, "Encore", "", "a.mat * 3", scope=11,
                     dmg_type=3, hit_type=0, animation=0,
                     message="%1 does an encore nobody asked for."))
    save("Skills.json", sk)

    ar = R.load("Armors.json")
    upsert(ar, armor(AR_ROSETTE, "Rosette, Second Place",
                     "[Accessory] Blue silk, Great Dunnage, the Contest at the "
                     "Sign of the Bell. The certificate is framed.",
                     ET_ACCESSORY, AT_ROSETTE, 0, [0, 20, 0, 0, 8, 4, 0, 6],
                     icon=149, traits=[trait(22, 8, 0.05)]))
    # NIX-1: Nix's gear. Body armour, and only Nix's actor has the type.
    upsert(ar, armor(AR_GRANS_COAT, "Gran's Coat",
                     "[Coat] Long, dark, well made and much mended. Eleven "
                     "years in bond. It fits.",
                     ET_BODY, AT_COAT, 0, [0, 0, 0, 30, 0, 18, 10, 8],
                     icon=152, traits=[trait(22, 2, 0.05)]))
    # ZEPH-1: Zephyrine's gear, if the purse is turned out. Body armour of a
    # type only her actor has. The white-and-purple; eleven years in the
    # Registrar's cupboard. MP cost rate 0.9: the right equipment, at last.
    upsert(ar, armor(AR_COLLEGIUM_ROBE, "Collegium Robe (Vance)",
                     "[Robe] White and purple, eleven years in the "
                     "Registrar's cupboard. Her name is sewn in the collar.",
                     ET_BODY, AT_ROBE, 0, [0, 60, 0, 20, 30, 40, 4, 0],
                     icon=154, traits=[trait(23, 4, 0.9)]))
    # COR-1: Corvin's gear. An accessory of a type only his actor has. It
    # keeps out the cold (ice x0.5) and, by a slow three per cent, about
    # cancels the elective curse's bleed, which nobody planned.
    upsert(ar, armor(AR_SCARF, "Scarf (Wrong Colour)",
                     "[Scarf] Very long, very warm and bright yellow, like the "
                     "new roofs. For somebody who feels the cold.",
                     ET_ACCESSORY, AT_SCARF, 0, [80, 0, 0, 8, 0, 12, 0, 6],
                     icon=139, traits=[trait(11, EL_ICE, 0.5),
                                       trait(22, 7, 0.03)]))
    save("Armors.json", ar)

    en = R.load("Enemies.json")
    upsert(en, enemy(
        EN_DRAY, "Mr Dray (Other Wind)", "Septimus_Dray", 0,
        [300, 60, 20, 14, 26, 16, 10, 10], 40, 0,
        [action(SK_SERPENT, 5), action(SK_ENCORE, 3, condition=2, p1=0,
                                       p2=0.5)],
        note="Instrumental (Other Wind). The serpent. Second place, twice."))
    upsert(en, enemy(
        EN_MOON, "Miss Moon (Ballad, Sad)", "Lettice_Moon", 0,
        [280, 80, 16, 12, 28, 18, 12, 10], 40, 0,
        [action(SK_SAD_VERSE, 5), action(SK_ENCORE, 3, condition=2, p1=0,
                                         p2=0.5)],
        note="Ballad (Sad). Every ballad she has written ends with the same "
             "number of survivors."))
    upsert(en, enemy(
        EN_BACK_TABLE, "The Back Table", "Sailor", 0,
        [240, 0, 24, 12, 8, 10, 14, 10], 30, 0,
        [action(SK_HECKLE, 5), action(SK_TALK_THROUGH, 4)],
        note="Regulars at the Bell. They have heard all of it before, and "
             "say so."))
    save("Enemies.json", en)

    tr = R.load("Troops.json")
    harbottle = lambda lines: R.text(lines, face_name="Gen_People6",
                                     face_index=3)
    # Sized to one performer (P1, QUESTS.md Part G): Piper fights it alone,
    # so everything is read off her at the start and it is the same fight at
    # any level. The room's patience is so many of her Epic Finales (`ef`,
    # its formula less the defence); a heckle or a serpent solo is about 14%
    # of her HP; a sad verse about 6% of her MP. Simulated over levels 9-15:
    # a player who never heals wins 61-90% in about seven turns, and one who
    # drinks a potion or two at a third of her HP wins 93-99% in nine or ten.
    size_them = R.script([
        "const p = $gameParty.battleMembers()[0];",
        "const ef = 4 * p.mat + 2 * p.agi;",
        "const heckle = Math.ceil((0.14 * p.mhp + p.mdf) / 2);",
        "for (const e of $gameTroop.members()) {",
        "  const id = e.enemyId();",
        "  const k = id === %d ? 4 : 3.5;" % EN_DRAY,
        "  e.addParam(0, Math.floor(k * ef) - e.mhp);",
        "  e.setHp(e.mhp);",
        "  if (id === %d) e.addParam(2, heckle - e.atk);" % EN_BACK_TABLE,
        "  if (id === %d) e.addParam(4, heckle - e.mat);" % EN_DRAY,
        "  if (id === %d) e.addParam(4, Math.ceil(0.06 * p.mmp / 2) - e.mat);"
        % EN_MOON,
        "}",
    ])
    turn0 = size_them + harbottle([
        "\\C[6]Mrs Harbottle:\\C[0] Ballad (Not Sad).",
        "Miss Piper Quill. Of Thistlewick.",
        "The room will give her its attention."])
    pages = [{"conditions": dict(BLANK_TROOP_CONDITIONS, turnValid=True,
                                 turnA=0, turnB=0),
              "list": turn0 + [{"code": 0, "indent": 0, "parameters": []}],
              "span": 0}]
    upsert(tr, troop(TR_CONTEST, "The Contest at the Sign of the Bell",
                     [(EN_BACK_TABLE, 130, 350), (EN_DRAY, 270, 330),
                      (EN_MOON, 410, 300)], pages=pages))
    save("Troops.json", tr)


# WRE-1's eleven type specimens: (Wren's name, battler, hue, mhp, atk, def,
# agi, Rowbotham's name for it, the second skill). Named after what they are;
# the note keeps what he called them.
SPECIMENS = [
    ("Common Hedge Egg", "Oddegg", 0, 1500, 46, 44, 18,
     "Rowbotham's Breakfast", SK_NOT_THERE),
    ("Frilled Wall Lizard", "Frilledlizard", 0, 1700, 54, 34, 34,
     "Rowbotham's Magnificent", SK_STARTLE),
    ("Hearth Salamander", "Salamander", 0, 1900, 58, 36, 28,
     "Rowbotham's Comfort", SK_BITE_NOTES),
    ("Turnip Gnome", "Gnome", 0, 1500, 50, 40, 22,
     "Mrs Rowbotham", SK_NOT_THERE),
    ("Barn Cait", "Caitsith", 0, 1600, 56, 30, 44,
     "Biscuit (his dog)", SK_BOLT),
    ("Striped Warren Hare", "Tigerbunny", 0, 1600, 54, 30, 46,
     "Rowbotham's Tiger", SK_BOLT),
    ("Upright Fox", "Foxman", 0, 1800, 60, 34, 38,
     "Pelham-Rudd's Fox (a subscriber)", SK_STARTLE),
    ("Many-Eyed Grazer", "Hakutaku", 0, 2400, 52, 46, 20,
     "Rowbotham's Ox", SK_NOT_THERE),
    ("Draught Sylph", "Sylph", 0, 1600, 48, 30, 48,
     "Lady Amberley (a subscriber)", SK_BOLT),
    ("Tall Marsh Wader", "Birdman", 0, 2000, 60, 36, 36,
     "Rowbotham's Self-Portrait", SK_BITE_NOTES),
    ("Pond Kappa", "SF_Kappa", 0, 2200, 58, 42, 26,
     "Captain (his other dog)", SK_BITE_NOTES),
]

# WRE-1's subscription list, which is a shop with names in it: one copy, bound,
# for each of these, paid for by the party because that is how a subscription
# list works when you are the one holding it.
SUBSCRIBERS = [
    "Dorcas Thrupp", "the Gloamwood Society", "Mr Ottershaw", "Bram",
    "Dr Hapgood", "Mr Gedge, the Lodge", "Prewitt, the Library",
    "Edith Pellow",
]
SUBSCRIPTION_PRICE = 150
SUBSCRIBERS_NEEDED = 6


def build_monograph():
    """WRE-1, the monograph (QUESTS.md C4): eleven type specimens to measure,
    each one a fight she objects to and conducts anyway, and the list."""
    sk = R.load("Skills.json")
    upsert(sk, skill(SK_STARTLE, "Startle", "", "0", dmg_type=0, hit_type=2,
                     animation=0, effects=[effect(32, 2, 0, 3)],
                     message="%1 does something sudden at %2."))
    upsert(sk, skill(SK_BOLT, "Bolts For Cover", "", "0", scope=11,
                     dmg_type=0, hit_type=0, animation=0,
                     effects=[effect(31, 6, 0, 3)],
                     message="%1 bolts for cover, and is somewhere else."))
    upsert(sk, skill(SK_BITE_NOTES, "Bites The Note-Taker", "",
                     "a.atk * 5 - b.def * 2", animation=0,
                     message="%1 bites %2, who was writing."))
    upsert(sk, skill(SK_NOT_THERE, "Is Not Where You Measured It", "",
                     "a.atk * 2 - b.def", scope=2, animation=0,
                     message="%1 is not where anybody measured it."))
    save("Skills.json", sk)

    en = R.load("Enemies.json")
    tr = R.load("Troops.json")
    base = [trait(22, 0, 0.95), trait(22, 1, 0.08)]
    for eid, tid, (name, battler, hue, mhp, atk, df, agi, his, extra) in zip(
            EN_SPECIMENS, TR_SPECIMENS, SPECIMENS):
        upsert(en, enemy(
            eid, name, battler, hue,
            [mhp, 40, atk, df, 30, 30, agi, 14], 340, 0,
            [action(SK_ATTACK, 5), action(extra, 4)], traits=base,
            note="A type specimen (WRE-1). Measured, not killed. "
                 "Rowbotham's name for it: %s." % his))
        upsert(tr, troop(tid, "Type Specimen: " + name, [(eid, 400, 330)]))
    save("Enemies.json", en)
    save("Troops.json", tr)

    it = R.load("Items.json")
    for iid, who in zip(IT_SUBSCRIPTIONS, SUBSCRIBERS):
        upsert(it, item(iid, "Subscription: " + who,
                        "One copy of Wren's monograph, bound, for %s. "
                        "Paid for; put down on the list." % who,
                        price=SUBSCRIPTION_PRICE, itype=2, consumable=False,
                        scope=0, occasion=3, icon=192))
    upsert(it, item(IT_MONOGRAPH, "The Monograph",
                    "The Fauna of the Valley, by What They Are. W. Halloway. "
                    "Eleven type specimens. One of them is a goose.",
                    itype=2, consumable=False, scope=0, occasion=3, icon=189))
    save("Items.json", it)



def build_vigil():
    """ALD-2, the vigil (QUESTS.md E7): a defence battle in which Aldric is
    present, cannot act and cannot be commanded, and draws everything that
    comes at the party - his whole class, as the boss condition.

    * **He keeps vigil** (state 41): restriction 4, so he is never given a
      turn, and a target rate of ten, so nearly everything aimed at the
      party is aimed at him. Substitute would be the literal reading, but
      the engine only lets a battler who can move substitute, so the cover
      is the targeting.
    * **The things that come hit for a share of the target's hit points**,
      so the fight is the same fight at any level: the party keeps him up
      and thins out what it can. The Small Hours cannot be fought, only got
      through, so the only way to win is the dawn - a troop page at the end
      of turn `VIGIL_DAWN` that kills everything still in the chapel.
    * **If he falls, the vigil is broken**: a troop page aborts the battle,
      which Battle Processing reports as an escape. The party cannot run."""
    sk = R.load("Skills.json")
    upsert(sk, skill(SK_SEEPS_IN, "Seeps In", "", "b.mhp * 0.08",
                     hit_type=0, animation=0,
                     message="%1 seeps into %2's armour."))
    upsert(sk, skill(SK_SIT_DOWN, "Suggests Sitting Down", "",
                     "b.mhp * 0.06", hit_type=0, animation=0,
                     message="%1 suggests to %2, very reasonably, that "
                             "they sit down."))
    upsert(sk, skill(SK_HOW_LATE, "How Late It Is", "", "0", dmg_type=0, hit_type=0,
                     animation=0, effects=[effect(21, 10, 0.4)],
                     message="%1 hums something about how late it is."))
    upsert(sk, skill(SK_THIS_WAY, "THIS WAY", "", "b.mhp * 0.12",
                     hit_type=0, animation=0,
                     message="%1 says THIS WAY to %2, very brightly."))
    save("Skills.json", sk)

    st = R.load("States.json")
    upsert(st, state(
        ST_VIGIL, "Keeping Vigil", 81, restriction=4,
        traits=[trait(23, 0, 10)], auto_removal=0, max_turns=1, min_turns=1,
        message1="%1 is keeping vigil.", message4="%1 may move.",
        priority=90))
    save("States.json", st)

    ar = R.load("Armors.json")
    upsert(ar, armor(AR_REGARDANT, "Shield (Regardant)",
                     "[Escutcheon] Argent, a knight rampant regardant: "
                     "looking back, to see who is behind him.",
                     ET_SHIELD, AT_ESCUTCHEON, 0, [60, 0, 0, 40, 0, 24, 0, 6],
                     icon=129, traits=[trait(62, 1, 1), trait(23, 1, 0.3)]))
    save("Armors.json", ar)

    en = R.load("Enemies.json")
    upsert(en, enemy(
        EN_DAMP, "The Damp", "Undine", 0, [260, 0, 30, 20, 20, 30, 12, 10],
        60, 0, [action(SK_SEEPS_IN, 5)],
        note="ALD-2. It comes in under the chapel door at Weeping Bottom "
             "every night. It always has."))
    upsert(en, enemy(
        EN_SMALL_HOURS, "The Small Hours", "Siren", 0,
        [999999, 0, 20, 999, 20, 999, 8, 10], 200, 0,
        [action(SK_HOW_LATE, 5)],
        note="ALD-2. Cannot be fought, only got through. Gone at dawn."))
    upsert(en, enemy(
        EN_TEMPTATION, "A Small Temptation", "Petitdevil", 0,
        [240, 0, 24, 16, 24, 20, 30, 10], 80, 0, [action(SK_SIT_DOWN, 5)],
        note="ALD-2. Sits on the end of the altar rail. Very reasonable."))
    upsert(en, enemy(
        EN_LIGHT, "A Light Going Away", "SF_Will_o_the_wisp", 0,
        [260, 0, 36, 18, 30, 24, 24, 10], 100, 0, [action(SK_THIS_WAY, 5)],
        note="ALD-2. Bobs off down the valley, saying THIS WAY. He has "
             "followed every light in the valley but this one."))
    save("Enemies.json", en)

    end = {"code": 0, "indent": 0, "parameters": []}

    def page(lines_or_cmds, span=0, **cond):
        cmds = (R.text(lines_or_cmds) if isinstance(lines_or_cmds[0], str)
                else lines_or_cmds)
        return {"conditions": dict(BLANK_TROOP_CONDITIONS, **cond),
                "list": cmds + [end], "span": span}

    # The killable three are sized to the party, as the contest's acts are.
    size_them = R.script([
        "for (const e of $gameTroop.members()) {",
        "  if (e.mhp > 99999) continue;",
        "  const want = 30 * $gameParty.highestLevel() *",
        "    $gameParty.battleMembers().length;",
        "  e.addParam(0, Math.max(0, want - e.mhp));",
        "  e.setHp(e.mhp);",
        "}",
    ])
    # Change Actor State: fixed actor, add.
    kneel = [{"code": 313, "indent": 0, "parameters": [0, ALDRIC, 0, ST_VIGIL]}]
    turn0 = size_them + kneel + R.text([
        "Sir Aldric kneels at the altar rail. He will not move",
        "until it is light, or speak, and whatever comes for any",
        "of you will have to come past him."]) + R.text([
        "The damp comes in under the door, as it always has.",
        "The small hours come in after it, and sit down. They",
        "cannot be fought. They can only be got through."])
    appear = lambda i: [{"code": 335, "indent": 0, "parameters": [i]}]
    temptation = appear(2) + R.text([
        "Something small sits down on the end of the altar rail,",
        "and asks Sir Aldric, very reasonably, whether he would",
        "not like to sit down."])
    wisp = appear(3) + R.text([
        "A light at the window, bobbing away down the valley,",
        "says THIS WAY. Sir Aldric has followed every light in",
        "the valley. He does not follow this one."])
    fallen = R.text([
        "Sir Aldric goes down, and gets straight up again, which",
        "is not allowed, and he knows it.",
        "The vigil is broken."]) + [
        {"code": 340, "indent": 0, "parameters": []}]
    # Change Enemy State: the entire troop, add Dead.
    dawn = R.text([
        "Grey at the east window. Then light, all down the",
        "chapel, and everything that came in the night is",
        "suddenly not there."]) + [
        {"code": 333, "indent": 0, "parameters": [-1, 0, 1]}]
    pages = [
        page(turn0, turnValid=True, turnA=0, turnB=0),
        page(fallen, actorValid=True, actorId=ALDRIC, actorHp=0),
        page(dawn, turnEnding=True, turnValid=True, turnA=VIGIL_DAWN,
             turnB=0),
        page(temptation, turnValid=True, turnA=2, turnB=0),
        page(wisp, turnValid=True, turnA=3, turnB=0),
    ]
    tr = R.load("Troops.json")
    t = troop(TR_VIGIL, "The Vigil",
              [(EN_DAMP, 200, 300), (EN_SMALL_HOURS, 400, 250),
               (EN_TEMPTATION, 560, 330), (EN_LIGHT, 330, 380),
               (EN_DAMP, 620, 240)], pages=pages)
    t["members"][2]["hidden"] = t["members"][3]["hidden"] = True
    upsert(tr, t)
    save("Troops.json", tr)


def build_worm():
    """ROL-2, the Worm of Carn Drey (QUESTS.md E18): the thing Roland's
    prophecy names, scaled for a hero of nineteen and met by a man of
    thirty-four with friends. A real fight and a short one - it is over before
    Piper has got a verse out - so its numbers are fixed, not sized to the
    party, and an over-levelled party is the point. And the sword out of the
    stone, which is strictly better than Fairweather's Own, and which he
    leaves at the tower door beside it."""
    sk = R.load("Skills.json")
    upsert(sk, skill(SK_COILS, "Coils", "", "a.atk * 4 - b.def * 2",
                     animation=1, message="%1 coils round %2."))
    upsert(sk, skill(SK_LOOKS_AT_HIM, "Looks At Roland", "", "0", dmg_type=0,
                     hit_type=0, scope=11, animation=0,
                     message="%1 looks at Roland for a long time. It was "
                             "expecting somebody younger."))
    save("Skills.json", sk)

    wp = R.load("Weapons.json")
    upsert(wp, weapon(WP_DRAWN, "The Drawn Sword",
                      "[Sword] Out of a stone under Carn Drey, in an afternoon, "
                      "with help. It has had one afternoon. It would like another.",
                      WT_SWORD, 0, [0, 0, 72, 14, 12, 12, 10, 16], icon=120,
                      animation=25,
                      traits=[trait(31, EL_LIGHT, 0), trait(22, 2, 0.15),
                              trait(22, 0, 0.06)]))
    save("Weapons.json", wp)

    en = R.load("Enemies.json")
    upsert(en, enemy(
        EN_WORM, "The Worm of Carn Drey", "SF_Anaconda", 0,
        [1600, 0, 70, 40, 30, 30, 28, 10], 600, 0,
        [action(SK_COILS, 5), action(SK_LOOKS_AT_HIM, 3)],
        note="ROL-2. Asleep under Carn Drey since before Roland was born, "
             "waiting for a hero of nineteen."))
    save("Enemies.json", en)

    tr = R.load("Troops.json")
    upsert(tr, troop(TR_WORM, "The Worm of Carn Drey",
                     [(EN_WORM, 408, 300)]))
    save("Troops.json", tr)


def build_spare():
    """Spare Cotterill, aged nine, and his mother (SPARE.md 3-5; QUESTS.md F1).

    * **The best skill list in the party on the worst stat line in it**:
      about half Bram's HP, the lowest DEF and an ATK that is a joke, the
      highest AGI, and every one of his skills runs off AGI with no DEF term
      at all. He is the only one who fits.
    * **The bag is the joke.** Every skill but one is a thing he takes out of
      it, so all but one need it in his hand - and it is sealed there. The
      exception is Temper Tantrum, for which he puts it down. It hurts him
      (a common event, so the formula stays one `balance.py` can read), and
      it is of an element his mother is immune to: it has never once worked
      on her. Fighting her with his real skills is SPARE.md 3's point - every
      one of them is a thing he tried on her first.
    * **The Drawing is not learned at a level.** The scene gives it him,
      because it is what she found in the bag.
    * **She is not a damage race.** A share of his HP when she says he is
      nine, a heal when she defers, every buff and guard he put up taken off
      in one sentence, and below half the quiet one, which costs him his TP.
      Tuned with a simulation at level 12: a player who heals when low and
      spends TP on Ninety Tubes wins about six in seven, in eleven turns or
      so; one who tries Temper Tantrum on her loses rather more often.
      The troop aborts at a quarter, which Battle Processing reports as an
      escape and the scene reads as "she stopped" (SPARE.md 4). She never
      reaches 0; collapse type 3 says she would not fall over if she did."""
    cl = R.load("Classes.json")
    hit = lambda v: trait(22, 0, v)
    eva = lambda v: trait(22, 1, v)
    crit = lambda v: trait(22, 2, v)
    upsert(cl, {
        "id": CLASSES[SPARE], "name": "The Ninth", "note": "",
        "expParams": [25, 18, 30, 30],
        "params": params((210, 24), (40, 4.5), (8, 1.2), (6, 1.0), (8, 1.2),
                         (12, 2.2), (34, 6.2), (30, 4.2)),
        "learnings": [{"level": lv, "skillId": s, "note": ""} for lv, s in
                      [(1, SK_SMALL_ENOUGH), (1, SK_TANTRUM),
                       (3, SK_HAVE_A_BAG), (5, SK_NEVER_HIT_ME),
                       (8, SK_NINETY_TUBES)]],
        "traits": [trait(23, 0, 0.45),      # nobody can quite bring themselves
                   hit(0.95), eva(0.25), crit(0.08),
                   trait(64, 4, 1),         # party ability: double gold
                   trait(41, STYPE_SPECIAL, 1),
                   trait(51, WT_BAG, 1), trait(52, AT_GENERAL, 1)]})
    R.save_list("Classes.json", cl)

    ac = R.load("Actors.json")
    upsert(ac, {
        "id": SPARE, "name": "Spare", "nickname": "Aged Nine", "note": "",
        "profile": "The ninth Cotterill, and nine in a useful way: the only "
                   "person in Upper Clanging small enough to get inside a "
                   "boiler. Has had a bag packed for two years.",
        "classId": CLASSES[SPARE], "initialLevel": SPARE_ARGUING_LEVEL,
        "maxLevel": 99, "characterName": "Gen_People14", "characterIndex": 4,
        "faceName": "Gen_People14", "faceIndex": 4,
        "battlerName": "Gen_People14_5",
        "equips": [WP_BAG, 0, 0, 0, 0],
        # The washer is his alone, and the bag does not come out of his hand:
        # Lock Equip (53). Not Seal Equip (54), which takes the slot away, so
        # `setup()` drops the bag and every skill that needs it goes dark.
        "traits": [trait(52, AT_WASHER, 1), trait(53, ET_WEAPON, 1)]})
    R.save_list("Actors.json", ac)

    st = R.load("States.json")
    upsert(st, state(
        ST_NEVER_HIT, "They Never Hit Me", 135, traits=[trait(23, 0, 0)],
        auto_removal=2, max_turns=3, min_turns=3,
        message1="%1 is wearing the jumper his mam knitted.",
        message4="%1 has taken the jumper off. It was warm."))
    upsert(st, state(
        ST_BRUSHED, "Brushed Through", 224, traits=[trait(21, 3, 0.6)],
        auto_removal=0, max_turns=1, min_turns=1,
        message1="%1 has been gone through with a brush."))
    save("States.json", st)

    sk = R.load("Skills.json")
    bag = []
    bag.append(skill(
        SK_SMALL_ENOUGH, "Small Enough",
        "There is a way in. There is always a way in, and he is the only "
        "one who fits. Ignores defence.",
        "a.agi * 2", mp=6, icon=214, animation=11,
        message="%1 takes out a candle end, and finds the way in."))
    upsert(sk, skill(
        SK_TANTRUM, "Temper Tantrum",
        "Enormous, and it hurts him too. It has never once worked on his "
        "mother.",
        "a.agi * 4.5 - b.def", tp=20, icon=218, animation=26,
        element=EL_TEMPER,
        effects=[effect(44, CE_TANTRUM)],
        message="%1 puts the bag down."))
    sk[SK_TANTRUM]["message2"] = "It is a very thorough tantrum."
    bag.append(skill(
        SK_HAVE_A_BAG, "I Have A Bag",
        "It has been packed for two years. There is something in it for "
        "everything. Heals the party; clears every ailment.",
        "a.agi + 80", dmg_type=3, scope=8, mp=14, icon=208, animation=41,
        hit_type=0, effects=[effect(22, s, 1.0)
                             for s in (4, 5, 6, 7, 8, 9, 10, 12, 13)],
        message="%1 takes out plasters, a hanky and a boiled sweet each."))
    bag.append(skill(
        SK_NEVER_HIT_ME, "They Never Hit Me",
        "Three turns in which nobody can make themselves swing at him.",
        "0", dmg_type=0, scope=11, tp=25, icon=135, animation=52,
        hit_type=0, effects=[effect(21, ST_NEVER_HIT, 1.0)],
        message="%1 takes out the jumper, and puts it on."))
    bag.append(skill(
        SK_NINETY_TUBES, "Ninety Tubes",
        "Ignores defence, and leaves it lower for good. He has done worse, "
        "in the dark, for buns.",
        "a.agi * 3", tp=40, icon=224, animation=16,
        effects=[effect(21, ST_BRUSHED, 1.0)],
        message="%1 takes out a flue brush. It is longer than the bag."))
    bag.append(skill(
        SK_THE_DRAWING, "The Drawing",
        "Revives and heals everybody, and raises attack and agility. He "
        "does not show it to just anybody.",
        "a.agi * 3 + 200", dmg_type=3, scope=13, tp=100, icon=196,
        animation=45, hit_type=0,
        effects=[effect(22, ST_DEAD, 1.0), effect(31, 2, 0, 4),
                 effect(31, 6, 0, 4), effect(13, 0, 100)],
        message="%1 takes out the drawing, and shows everybody."))
    for s in bag:
        s["requiredWtypeId1"] = WT_BAG
        upsert(sk, s)

    # Mrs Cotterill's four. Mothers do not miss: every one is a certain hit.
    upsert(sk, skill(SK_YOU_ARE_NINE, "You Are Nine", "", "b.mhp * 0.34",
                     hit_type=0, animation=0, message='%1 says, "You are nine."'))
    upsert(sk, skill(SK_ASK_YOUR_FATHER, "Ask Your Father", "", "a.mhp * 0.06",
                     dmg_type=3, scope=11, hit_type=0, animation=0,
                     message='%1 says, "Ask your father."'))
    sk[SK_ASK_YOUR_FATHER]["message2"] = "Mr Cotterill looks at the sky."
    upsert(sk, skill(SK_NOT_THE_POINT, "That Is Not The Point", "", "0",
                     dmg_type=0, hit_type=0, animation=0,
                     effects=[effect(33, p) for p in range(2, 8)] +
                     [effect(22, ST_NEVER_HIT, 1.0)],
                     message='%1 says, "That is not the point."'))
    sk[SK_NOT_THE_POINT]["message2"] = "He was doing so well."
    upsert(sk, skill(SK_SAID_NO, "I Have Said No", "", "b.mhp * 0.18",
                     hit_type=0, animation=0, effects=[effect(13, 0, -100)],
                     message='%1 says, "I have said no."'))
    sk[SK_SAID_NO]["message2"] = "It is not louder. It is quieter."
    save("Skills.json", sk)

    ce = R.load("CommonEvents.json")
    upsert(ce, {"id": CE_TANTRUM, "name": "Temper Tantrum (Spare)",
                "switchId": 1, "trigger": 0,
                "list": R.script([
                    "const s = $gameActors.actor(%d);" % SPARE,
                    "const d = Math.min(Math.floor(s.mhp / 5), s.hp - 1);",
                    "if (d > 0) { s.gainHp(-d); s.startDamagePopup(); }",
                ]) + [{"code": 0, "indent": 0, "parameters": []}]})
    save("CommonEvents.json", ce)

    it = R.load("Items.json")
    upsert(it, item(IT_FORM_P9, "Form P-9",
                    "Application by a Minor to Accompany a Chosen One (Parish "
                    "of Upper Clanging). Wants a parent's signature.",
                    itype=2, consumable=False, scope=0, occasion=3, icon=193))
    upsert(it, item(IT_WASHER, "A Washer, Off Shim",
                    "Out of Shim's tin. Not the bearing. Flat the whole time, "
                    "which is why it is a good one.",
                    itype=2, consumable=False, scope=0, occasion=3, icon=145))
    # SPA-1's copies: used from the menu, they read every letter he has
    # posted, in the order they went (q_spare.copies).
    upsert(it, item(IT_SPA1_COPIES, "Spare's Copies",
                    "Everything he has posted home, copied out in pencil "
                    "first, in case. None of it is true.",
                    itype=2, consumable=False, scope=0, occasion=2, icon=192,
                    effects=[effect(44, CE_SPA1_COPIES)]))
    save("Items.json", it)
    import q_spare                  # it imports this module
    ce = R.load("CommonEvents.json")
    upsert(ce, {"id": CE_SPA1_COPIES, "name": "Spare's Copies (SPA-1)",
                "switchId": 1, "trigger": 0,
                "list": q_spare.copies() +
                [{"code": 0, "indent": 0, "parameters": []}]})
    save("CommonEvents.json", ce)

    wp = R.load("Weapons.json")
    upsert(wp, weapon(WP_BAG, "A Bag, Packed",
                      "[Bag] Packed two years ago. Contents: yes.",
                      WT_BAG, 0, [0, 0, 6, 0, 0, 0, 10, 10], icon=209,
                      animation=1))
    save("Weapons.json", wp)

    ar = R.load("Armors.json")
    upsert(ar, armor(AR_WASHER, "A Washer, Off Shim",
                     "[Accessory] Shim's second-best. Flat the whole time. "
                     "He wears it on a bootlace.",
                     ET_ACCESSORY, AT_WASHER, 0, [0, 0, 0, 0, 0, 4, 4, 12],
                     icon=145))
    save("Armors.json", ar)

    en = R.load("Enemies.json")
    upsert(en, enemy(
        EN_MAM, "Mrs Cotterill", "Mrs_Cotterill", 0,
        [2600, 0, 55, 30, 30, 30, 40, 30], 0, 0,
        [action(SK_YOU_ARE_NINE, 9, condition=1, p1=0, p2=0),
         action(SK_YOU_ARE_NINE, 4), action(SK_ATTACK, 5),
         action(SK_ASK_YOUR_FATHER, 4, condition=2, p1=0, p2=0.75),
         action(SK_NOT_THE_POINT, 4),
         action(SK_SAID_NO, 6, condition=2, p1=0, p2=0.5)],
        traits=[trait(63, 3, 0), trait(11, EL_TEMPER, 0)],
        note="SPARE.md 3. She is right. She loses to the one thing she cannot "
             "argue with, which is that he is exactly like her."))
    save("Enemies.json", en)

    end = {"code": 0, "indent": 0, "parameters": []}
    folds = R.text(["Mrs Cotterill folds her arms.",
                    "Mr Cotterill finds somewhere else to stand."])
    stops = R.text(["Mrs Cotterill stops."]) + [
        {"code": 340, "indent": 0, "parameters": []}]
    pages = [
        {"conditions": dict(BLANK_TROOP_CONDITIONS, turnValid=True),
         "list": folds + [end], "span": 0},
        {"conditions": dict(BLANK_TROOP_CONDITIONS, enemyValid=True,
                            enemyIndex=0, enemyHp=25),
         "list": stops + [end], "span": 0},
    ]
    tr = R.load("Troops.json")
    upsert(tr, troop(TR_MAM, "A Discussion With Mam", [(EN_MAM, 408, 380)],
                     pages=pages))
    save("Troops.json", tr)


def build_mothballs():
    """P1 (QUESTS.md Part G): a Repel, for NIX-5 and anywhere else. The engine
    rolls a fresh encounter count on every transfer (`Game_Player.locate`), so
    adding to the count would be lost at the Gloamwood's map change. A state
    is not: Encounter None while it lasts freezes the count, and it is removed
    by walking, with a message. So the next encounter is pushed back a fixed
    number of steps, and Nix's half applies to every step after it - the two
    stack, which an Encounter Half trait would not.

    **And then it wants airing** (Mike, 7 Oct 2026): without a cooldown, a
    twist used every time the last wore off covered any walk, and Nix's half
    did nothing. So using one runs a common event, which goes by the party's
    step count in `VAR_MOTHBALLS`: inside 50 + 25 steps of the last twist the
    new one goes back in the bag with a line, and nothing is spent. Party
    steps, so another member's coat is no way round it.

    The walk through the Gloamwood is 92 steps on Map 9 and 28 on Map 10 at
    the shortest, all of it in the encounter region. With Nix alone it is got
    through about one night in fifty. A twist covers 49 steps outright (the
    fiftieth, which walks it off, already counts at Nix's half), and the
    next can be had 25 steps after: twisted at the mouth and again the moment
    it may be, 87% with Nix (85% for a party that wanders a tenth further)
    and 48% without - which is what Nix is for. One twist alone, 56%."""
    st = R.load("States.json")
    upsert(st, dict(state(
        ST_MOTHBALLS, "Mothballs", 208, traits=[trait(64, 1, 0)],
        auto_removal=0, max_turns=1, min_turns=1, remove_at_battle_end=False,
        message4="%1 no longer smells of mothballs.", priority=10),
        removeByWalking=True, stepsToRemove=MOTHBALL_STEPS))
    save("States.json", st)
    it = R.load("Items.json")
    upsert(it, item(IT_MOTHBALLS, "Mothballs",
                    "A twist of paper, very strong. Nothing will come near "
                    "you for %d steps. Then it wants airing." %
                    MOTHBALL_STEPS,
                    price=30, icon=208, scope=0, occasion=2, animation=0,
                    effects=[effect(44, CE_MOTHBALLS)]))
    save("Items.json", it)
    since = "$gameParty.steps() - $gameVariables.value(%d)" % VAR_MOTHBALLS
    airing = R.if_then(
        R.condition_script("$gameVariables.value(%d) > 0 && %s < %d" % (
            VAR_MOTHBALLS, since, MOTHBALL_STEPS + MOTHBALL_AIRING)),
        [R.gain_item(IT_MOTHBALLS, 1)] +
        R.text(["The last lot is still airing. Give it a while."]),
        R.script([
            "$gameVariables.setValue(%d, Math.max(1, $gameParty.steps()));"
            % VAR_MOTHBALLS,
            "const a = $gameParty.battleMembers().find(m => m.isAlive());",
            "if (a) a.addState(%d);" % ST_MOTHBALLS,
        ]) + [R.play_se("Equip1", 60)] +
        R.text(["The smell is extraordinary."]))
    ce = R.load("CommonEvents.json")
    upsert(ce, {"id": CE_MOTHBALLS, "name": "Mothballs (P1)",
                "switchId": 1, "trigger": 0,
                "list": airing + [{"code": 0, "indent": 0, "parameters": []}]})
    save("CommonEvents.json", ce)
