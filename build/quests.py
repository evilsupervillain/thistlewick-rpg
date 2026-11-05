"""The quest log's contents: `data/Quests.json`, written through the
workspace's `tools/questlog` (`../../QUESTLOG.md`). `QUESTS.md` G0 is the
step that built it.

The log keeps no state of its own. Every quest below is bound to switches,
variables and self switches the game already sets, so nothing here changes an
event - the log reads, and the plugin works out the rest (2.3 of the plugin's
document). Three rules decide every binding:

* **Never `SW_RECRUIT`.** A form desk turns those off. `SW_KNOWN` and the
  quests' own switches never go off, and those are what is read here.
* **A switch that ends is never a quest's only start.** Several "on" switches
  go off again (`(ends)` in `db.py`). Where one goes off at the finish, the
  start is `any(on, done)` and the plugin's latch holds the completion. Where
  one goes off on a *failure* (NIX-5's escort), the start also reads
  something that stays on, so a failed night does not drop the quest.
* **Where the offer leaves nothing behind, the quest arrives complete.** A
  scene that offers and finishes in one sitting - ALD-4's reunion, the
  Lay-By, a dragon read to - sets only its done switch, so the quest starts
  and finishes on it and the banner says "Quest complete". That is the honest
  reading, and it is exactly what `QUESTS.md` G0 asks for "We haven't got a
  quest log".

The self switches read are listed in `SELF_BINDINGS`, because `check.py`
cannot see who sets one.

Titles are 22 characters at most and objectives about 33, because the list
and the tracker are that wide (`check.py` enforces it). Descriptions carry the
game's voice; every one is new writing, for Mike's eye. A finished quest says
what happened, in an entry keyed on its done switch.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)),
                                "tools", "questlog"))

import questlog as Q  # noqa: E402
import db  # noqa: E402
from places import (MAP_HOME, MAP_COTTAGE, MAP_WORLD)  # noqa: E402

sw, var, self_sw, item, armor = Q.sw, Q.var, Q.self_sw, Q.item, Q.armor
any_, all_, not_ = Q.any_, Q.all_, Q.not_
obj, desc = Q.objective, Q.desc

# The self switches the log reads, and what each one means.
MOUTH = self_sw(MAP_WORLD, 2)           # Bagshawe has told his tale at the mouth
LETTER = self_sw(MAP_HOME, 8)           # clause nineteen's letter, read
QUY_A = self_sw(MAP_COTTAGE, 2, "A")    # Quy met after the ending
QUY_B = self_sw(MAP_COTTAGE, 2, "B")    # the afternoon the tally promised
SELF_BINDINGS = [
    ("Map %03d event 2 A" % MAP_WORLD, "NIX-5: Mr Bagshawe's tale told, "
     "so a failed night keeps the quest"),
    ("Map %03d event 8 A" % MAP_HOME, "clause nineteen: the letter on the mat, read"),
    ("Map %03d event 2 B" % MAP_COTTAGE, "Halbert Quy told what Grimspite said"),
]


def done_only(key, title, done, giver, location, text, category="companion"):
    """A quest that is offered and finished in one scene: it starts and ends
    on the same switch."""
    return Q.quest(key, title, start=done, complete=done, category=category,
                   giver=giver, location=location, description=[desc(text)])


def started(*switches):
    """Start on any of these: the ask, the "on" that may end, and the done."""
    return any_(*[sw(s) for s in switches])


# ================================================================ the main ==
def main_quests():
    return [
        Q.quest(
            "obligatory", "The Obligatory Quest", category="main",
            giver="Elder Wispel", location="Thistlewick",
            start=sw(db.SW_QUEST), complete=sw(db.SW_WON),
            description=[
                desc("Every hundred years the Dark Lord rises in the "
                     "Obligatory Tower, and Thistlewick sends somebody north "
                     "to put him down. It has worked forty-seven times. You "
                     "are the Forty-Eighth, selected while you were asleep "
                     "and therefore unable to object."),
                desc("The tower door is open. At the top of the stairs is a "
                     "Dark Lord, and the Prophecy is very clear about what "
                     "happens next. It has been clear about it forty-seven "
                     "times.", when=sw(db.SW_TOWER_OPEN)),
                desc("The Dark Lord was never the problem. The Prophecy was, "
                     "and it has been annulled. Clause twelve has been struck "
                     "from the records and replaced with a note reading SEE "
                     "BRAM.", when=sw(db.SW_WON)),
            ],
            objectives=[
                obj("party", "Take companions, up to three", optional=True,
                    done=var(db.VAR_COMPANIONS, ">=", 1)),
                obj("leave", "Leave Thistlewick", done=sw(db.SW_LEFT_VILLAGE)),
                obj("wood", "Get through the Gloamwood",
                    done=sw(db.SW_GLOAMWOOD)),
                obj("tower", "Get into the Obligatory Tower",
                    done=sw(db.SW_TOWER_OPEN)),
                obj("lord", "Kill the Dark Lord", done=sw(db.SW_GRIMSPITE)),
                obj("home", "Come home", done=sw(db.SW_WON)),
            ]),
    ]


# ============================================================= the south ==
def south_quests():
    return [
        Q.quest(
            "feud", "The Thrupp Sisters",
            giver="Prudence Thrupp", location="Thistlewick",
            start=started(db.SW_FEUD_JAR, db.SW_FEUD_REPLY, db.SW_FEUD_DONE),
            complete=sw(db.SW_FEUD_DONE),
            description=[
                desc("Prudence Thrupp and her sister Dorcas have not spoken "
                     "for thirty years. It is not a falling-out. They stopped "
                     "one day and neither of them started again, so they send "
                     "each other things instead. This one is a jar. Do not "
                     "shake it. Do not ask what is in it."),
                desc("Dorcas has sent something back. It is heavier than the "
                     "jar was. Considerably heavier. Do not open it, do not "
                     "shake it, and do not let it near a fire.",
                     when=sw(db.SW_FEUD_REPLY)),
                desc("Dorcas sent back something worse than the jar, "
                     "deliberately, and Prudence laughed. Thirty years, and "
                     "her sister has still got it. She is going to write to "
                     "her at the weekend. Do not tell Dorcas.",
                     when=sw(db.SW_FEUD_DONE)),
            ],
            objectives=[
                obj("jar", "Take the jar to Dorcas",
                    done=any_(sw(db.SW_FEUD_REPLY), sw(db.SW_FEUD_DONE))),
                obj("reply", "Take the reply to Prudence",
                    done=sw(db.SW_FEUD_DONE),
                    visible=any_(sw(db.SW_FEUD_REPLY), sw(db.SW_FEUD_DONE))),
            ]),
        Q.quest(
            "guild", "Form A-1",
            giver="Registrar Pell", location="Nether Sopping",
            start=sw(db.SW_GUILD_ASKED), complete=sw(db.SW_GUILD_MEMBER),
            description=[
                desc("You cannot be an adventurer in this district "
                     "unregistered. You can do the adventuring. You just "
                     "cannot be one. Registration takes Form A-1, which "
                     "requires a character reference, a hat, and Form A-1. "
                     "Form A-1 has been mislaid for eleven years."),
                desc("Registered: a Guild Card (Provisional). In forty years "
                     "nobody had brought Registrar Pell all three at once. "
                     "The board is open to you, and so, administratively, is "
                     "a mound with a curse on it.",
                     when=sw(db.SW_GUILD_MEMBER)),
            ],
            objectives=[
                obj("reference", "Get a character reference",
                    done=any_(item(db.IT_REFERENCE), sw(db.SW_GUILD_MEMBER))),
                obj("hat", "Get a hat",
                    done=any_(armor(db.AR_A_HAT), sw(db.SW_GUILD_MEMBER))),
                obj("form", "Find Form A-1", done=sw(db.SW_GUILD_FORM)),
                obj("register", "Take all three to Pell",
                    done=sw(db.SW_GUILD_MEMBER)),
            ]),
        Q.quest(
            "bounty_crab", "Bounty: The Crab",
            giver="The Guild's board", location="Nether Sopping",
            start=any_(sw(db.SW_GUILD_MEMBER), sw(db.SW_BOUNTY_CRAB)),
            complete=sw(db.SW_CRAB_PAID),
            description=[
                desc("THE CRAB OF UNUSUAL SIZE. Holds the west beach. Will "
                     "not be reasoned with. Has been there longer than the "
                     "town. Everyone in Nether Sopping is very careful to say "
                     "'unusual'."),
                desc("The Crab of Unusual Size no longer holds the west "
                     "beach. Four smaller crabs hold it now, between them, "
                     "badly. Its card says DISCHARGED, in Pell's hand.",
                     when=sw(db.SW_CRAB_PAID)),
            ],
            objectives=[
                obj("crab", "Deal with the crab", done=sw(db.SW_BOUNTY_CRAB)),
                obj("claim", "Claim the bounty", done=sw(db.SW_CRAB_PAID)),
            ],
            reward="900 crowns, and chowder"),
        Q.quest(
            "bounty_crooke", "Bounty: M. Crooke",
            giver="The Guild's board", location="Nether Sopping",
            start=any_(sw(db.SW_GUILD_MEMBER), sw(db.SW_BOUNTY_CROOKE)),
            complete=sw(db.SW_CROOKE_PAID),
            description=[
                desc("M. CROOKE, BANDIT CHIEF. Camp in the western hills. "
                     "Runs a six-week banditry apprenticeship with a "
                     "syllabus."),
                desc("Meredith Crooke's bounty is discharged, and somebody "
                     "has pinned her syllabus up next to the card as a "
                     "curiosity. Her pass rate this year was ninety per "
                     "cent.", when=sw(db.SW_CROOKE_PAID)),
            ],
            objectives=[
                obj("camp", "Deal with Crooke", done=sw(db.SW_BOUNTY_CROOKE)),
                obj("claim", "Claim the bounty", done=sw(db.SW_CROOKE_PAID)),
            ],
            reward="1200 crowns, and a coat"),
        Q.quest(
            "lighthouse", "The Lighthouse",
            giver="Ferrety Bother", location="Nether Sopping",
            start=sw(db.SW_LAMP_ASKED), complete=sw(db.SW_LAMP_LIT),
            description=[
                desc("The light has been out since the spring, for want of "
                     "oil. It is not for the ships. There have been no ships "
                     "for ninety-one years. It is for the ones coming back "
                     "down the north road at night: you can see it from the "
                     "crossroads, and it is what you walk home by."),
                desc("The lighthouse at Nether Sopping is lit. Out on the "
                     "north road, at the crossroads, there is a light in the "
                     "south again when you turn round.",
                     when=sw(db.SW_LAMP_LIT)),
            ],
            objectives=[
                obj("oil", "Get a gallon of lamp oil",
                    done=any_(item(db.IT_LAMP_OIL), sw(db.SW_LAMP_LIT))),
                obj("light", "Light the lamp", done=sw(db.SW_LAMP_LIT)),
            ]),
        Q.quest(
            "pit", "The Bottomless Pit",
            giver="Fenwick Splint", location="The Bottomless Pit",
            start=sw(db.SW_PIT_ASKED), complete=sw(db.SW_PIT_PAID),
            description=[
                desc("Two crowns to look into the Bottomless Pit, a wonder of "
                     "the district, which is four feet deep. Something has "
                     "moved in down the far end and has been eating the lost "
                     "property: two hundred years of it."),
                desc("It was a badger. Fenwick Splint told the Guild for "
                     "forty years, and they never came and saw the badger. "
                     "Admission is free for you now. Forever.",
                     when=sw(db.SW_PIT_PAID)),
            ],
            objectives=[
                obj("far_end", "Deal with the far end",
                    done=sw(db.SW_PIT_CLEARED)),
                obj("splint", "Tell Mr Splint", done=sw(db.SW_PIT_PAID)),
            ]),
        Q.quest(
            "barrow", "The Forty-Fourth",
            location="The Barrow of the Forty-Fourth",
            start=sw(db.SW_BARROW_OPEN), complete=sw(db.SW_BARROW_BEATEN),
            description=[
                desc("A Scheduled Monument of the district, entry restricted "
                     "to registered adventurers. Underneath, in chalk, in a "
                     "much older hand: THERE IS A CURSE ON IT AS WELL."),
                desc("Ambrose Fitch, the Forty-Fourth, waited forty years to "
                     "have that fight, and it took four minutes. He gave you "
                     "the grave goods, rather than letting you take them, "
                     "which he was particular about.",
                     when=sw(db.SW_BARROW_BEATEN)),
            ]),
        Q.quest(
            "bench", "A Bench",
            giver="Ambrose Fitch", location="The Barrow of the Forty-Fourth",
            start=sw(db.SW_BENCH_ASKED), complete=sw(db.SW_BENCH_DONE),
            description=[
                desc("Forty years of standing in a circle, and what he wants "
                     "is a bench. Top of the mound, facing the sea, where "
                     "people walking the north road tired can sit down. "
                     "Anyone's bench. Not his. Anyone's."),
                desc("A bench on the top of the barrow, facing the sea. "
                     "Anyone may sit on it, which was the point. One piece "
                     "was left over, which is traditional.",
                     when=sw(db.SW_BENCH_DONE)),
            ],
            objectives=[
                obj("bench", "Put a bench on the mound",
                    done=sw(db.SW_BENCH_DONE)),
            ]),
        Q.quest(
            "history", "A Complete History",
            giver="Hosea Bellwether", location="The Slain Wyvern",
            start=sw(db.SW_HISTORY_ASKED), complete=sw(db.SW_HISTORY_DONE),
            description=[
                desc("Hosea is compiling A Complete And Accurate History Of "
                     "The Obligatory Quest. Complete is going well. Accurate "
                     "is the problem. Everyone in the Slain Wyvern has been "
                     "on one, and not one of them will tell a historian. "
                     "They will tell you."),
                desc("Complete. Not accurate - two of the tales cannot both "
                     "be true on a Tuesday - but complete. The Footnote on "
                     "page four hundred and one is you. It says you "
                     "listened.", when=sw(db.SW_HISTORY_DONE)),
            ],
            objectives=[
                obj("tales", "Hear six tales, to the end",
                    progress=(db.VAR_TALES, 6)),
                obj("hosea", "Go back to Hosea", done=sw(db.SW_HISTORY_DONE),
                    visible=var(db.VAR_TALES, ">=", 6)),
            ]),
        Q.quest(
            "forty_five", "Number Forty-Five",
            giver="Halbert Quy", location="Nether Sopping",
            start=sw(db.SW_MET_QUY), complete=QUY_B,
            description=[
                desc("Halbert Quy went north thirty years ago, and came back, "
                     "and asked a question at the next meeting. His cottage "
                     "was ready by the Friday. Forty-seven Chosen Ones did "
                     "the sword, he says, and not one of them ever asked the "
                     "man why he doesn't stop. Ask him why. Then listen to "
                     "the whole answer."),
                desc("You told him what Grimspite said, all of it, in order, "
                     "including the part about the tea. It took most of an "
                     "afternoon.", when=QUY_B),
            ],
            objectives=[
                obj("ask", "Ask the Dark Lord why",
                    done=sw(db.SW_GRIMSPITE)),
                obj("tell", "Tell Halbert what he said", done=QUY_B,
                    visible=sw(db.SW_WON)),
            ]),
    ]


# ============================================================= the north ==
def north_quests():
    return [
        Q.quest(
            "two_hundred", "The Two Hundred",
            giver="Ott Hoyle", location="Upper Clanging",
            start=sw(db.SW_TWO_HUNDRED_ASKED), complete=sw(db.SW_AIRSHIP),
            description=[
                desc("Lift has never been the problem. The Hoyle Works can "
                     "get anything off the ground; they have had a shed off "
                     "the ground. They come down, in sight of the tower. Ott "
                     "Hoyle has one variable left she has never been able to "
                     "get hold of, and it walked into her works this morning "
                     "and asked whether they had a gift shop."),
                desc("Attempt Two Hundred flies. She is outside the gate. "
                     "Do not set her down on anything with a roof on it.",
                     when=sw(db.SW_AIRSHIP)),
            ],
            objectives=[
                obj("oilskin", "Forty bolts of oilskin",
                    done=sw(db.SW_OILSKIN_GOT)),
                obj("spar", "A spar from Ollerenshaw's",
                    done=sw(db.SW_SPAR_DONE)),
                obj("ott", "Go back to Ott", done=sw(db.SW_AIRSHIP),
                    visible=all_(sw(db.SW_OILSKIN_GOT), sw(db.SW_SPAR_DONE))),
            ]),
        Q.quest(
            "item_one", "ITEM 1",
            giver="The Stores Book", location="The Hoyle Works",
            start=sw(db.SW_ITEM_ONE_ASKED),
            complete=any_(sw(db.SW_ITEM_ONE_USED),
                          all_(sw(db.SW_ITEM_ONE_DOWN),
                               not_(item(db.IT_ITEM_ONE)))),
            description=[
                desc("The works stores book has been kept honestly since "
                     "1802, and everything ever issued has a line through "
                     "it but one: ITEM 1, issued 199 times, returned 198. "
                     "Attempt 199 is on a crag in sight of the tower, and "
                     "everything aboard her is intact."),
                desc("ITEM 1 is off the crag, in a crate, and is not light.",
                     when=sw(db.SW_ITEM_ONE_DOWN)),
                desc("Ott rendered ITEM 1 down, and was visibly relieved to "
                     "have it out of a field. Nobody has yet ticked it off.",
                     when=all_(sw(db.SW_ITEM_ONE_DOWN),
                               not_(item(db.IT_ITEM_ONE)))),
                desc("ITEM 1 was set down in front of the throne, and the "
                     "Dark Lord was delighted. It was the first new thing in "
                     "four thousand years.", when=sw(db.SW_ITEM_ONE_USED)),
            ],
            objectives=[
                obj("crag", "Get ITEM 1 off the crag",
                    done=sw(db.SW_ITEM_ONE_DOWN)),
            ]),
        done_only(
            "eighty_four", "Attempt Eighty-Four", sw(db.SW_84_BEATEN),
            None, "The Long Field",
            "A machine that spent a hundred and forty years repairing itself "
            "out of its neighbours, still faintly trying to go north, has "
            "stopped. She got further than any of them, Ott says. There is a "
            "bay in the shed with her number over it, and she is coming up "
            "the hill.", category="side"),
        Q.quest(
            "spare", "Form P-9",
            giver="Spare Cotterill", location="Upper Clanging",
            start=sw(db.SW_SPARE_ASKED), complete=sw(db.SW_SPARE_KNOWN),
            description=[
                desc("Spare Cotterill, aged nine, would like to come. He has "
                     "asked every Chosen One who ever walked up that street, "
                     "and been told he cannot. The Parish Office issues the "
                     "form, and his mother signs it, or nobody does."),
                desc("Spare Cotterill, aged nine: Form P-9, countersigned by "
                     "his mother. He is coming. He has to write.", when=sw(db.SW_SPARE_KNOWN)),
            ],
            objectives=[
                obj("form", "Get Form P-9 from Gudgeon",
                    done=sw(db.SW_SPARE_FORM)),
                obj("mam", "Get it past his mother",
                    done=sw(db.SW_SPARE_KNOWN), visible=sw(db.SW_SPARE_FORM)),
            ]),
    ]


# ========================================== Firstfield and the Premises ==
def meadow_quests():
    return [
        Q.quest(
            "firstfield", "Firstfield Meadow",
            giver="Fizz", location="Firstfield Meadow",
            start=sw(db.SW_FF_ARRIVED), complete=sw(db.SW_FF_GRADUATED),
            description=[
                desc("A tutorial, in a meadow, run by Fizz, who is extremely "
                     "pleased to see you. There are four stations. "
                     "Everything is explained, at least twice, in capitals."),
                desc("Graduated: the first completed tutorial on record. "
                     "Fizz said so, several times, in capitals.",
                     when=sw(db.SW_FF_GRADUATED)),
            ],
            objectives=[
                obj("stick", "Get a stick from Old Hollis",
                    done=sw(db.SW_FF_STICK)),
                obj("chest", "Open the chest", done=sw(db.SW_FF_CHEST)),
                obj("sheep", "Find Mrs Fenwick's sheep",
                    done=sw(db.SW_FF_SHEEP_DONE)),
                obj("norbert", "Fight Norbert", done=sw(db.SW_FF_NORBERT)),
                obj("graduate", "Go back to Fizz",
                    done=sw(db.SW_FF_GRADUATED),
                    visible=var(db.VAR_FF_STATIONS, ">=", 4)),
            ]),
        Q.quest(
            "ff_sheep", "Mrs Fenwick's Sheep",
            giver="Dilys Fenwick", location="Firstfield Meadow",
            start=sw(db.SW_FF_SHEEP_ASKED), complete=sw(db.SW_FF_SHEEP_DONE),
            description=[
                desc("The Guild says a meadow has to have a fetch quest, so "
                     "Dilys Fenwick's sheep are lost. A bit. They are just "
                     "there. They are pigs. They have been practising their "
                     "baa."),
                desc("Dilys Fenwick's sheep, which are pigs, have been found, "
                     "where they were. They look extremely found.",
                     when=sw(db.SW_FF_SHEEP_DONE)),
            ],
            objectives=[
                obj("sheep", "Find the sheep", progress=(db.VAR_FF_SHEEP, 3)),
            ]),
        # QUESTS.md G0 names this one "We haven't got a quest log.", which is
        # 27 characters against the list's 22; this is Fizz's next line.
        done_only(
            "ff_quest_log", "Remember Really Hard",
            sw(db.SW_FF_SHEEP_ASKED), "Fizz", "Firstfield Meadow",
            "Check your quest log so that you don't have to remember really "
            "hard.", category="side"),
        Q.quest(
            "visitors_book", "The Visitors' Book",
            giver="Mr Hollowell", location="The Former Premises",
            start=sw(db.SW_VISITORS_BOOK),
            complete=all_(sw(db.SW_VISITORS_BOOK), sw(db.SW_GRIMSPITE)),
            description=[
                desc("Mr Hollowell keeps the Former Premises, and its "
                     "visitors' book, which has never had a visitor in it. "
                     "He would very much like the incumbent's signature. The "
                     "book never leaves its lectern, so he has given you a "
                     "slip, ruled to match."),
                desc("NAME: GRIMSPITE THE INEVITABLE. FROM: HERE. REMARKS: "
                     "Never been. Heard marvellous things about the lift.",
                     when=sw(db.SW_GRIMSPITE)),
            ],
            objectives=[
                obj("sign", "Get the incumbent to sign",
                    done=sw(db.SW_GRIMSPITE)),
            ]),
    ]


# ====================================================== companion quests ==
def merribell():
    who = "Merribell"
    return [
        Q.quest(
            "mer2", "Fit to Travel", category="companion",
            giver=who, location="Upper Clanging",
            start=sw(db.SW_MER2_ASKED), complete=sw(db.SW_MER2_DONE),
            description=[
                desc("Clause eleven: a Chosen One is certified fit before "
                     "departure. It has been done forty-seven times. Bram's "
                     "form is blank, because he was asleep. Merribell will "
                     "now do it. Properly. She needs the form, a pair of "
                     "stamped scales, a good light and a witness."),
                desc("Bram is certified fit to travel under clause eleven, "
                     "properly, with a witness. The Certificate of Fitness "
                     "does nothing. It is very properly filled in.", when=sw(db.SW_MER2_DONE)),
            ],
            objectives=[
                obj("scales", "Borrow the fish stall's scales",
                    done=any_(sw(db.SW_MER2_SCALES), sw(db.SW_MER2_DONE))),
                obj("light", "Get a good light",
                    done=any_(sw(db.SW_LAMP_LIT), sw(db.SW_MER2_DONE))),
                obj("exam", "Use the form, with a witness",
                    done=sw(db.SW_MER2_DONE)),
            ]),
        Q.quest(
            "mer4", "Tobias Frayne", category="companion",
            giver=who, location="Tobias Frayne's cottage",
            start=started(db.SW_MER4_TOLD, db.SW_MER4_DONE),
            complete=sw(db.SW_MER4_DONE),
            description=[
                desc("Tobias Frayne has been brought back eleven times. "
                     "Merribell will not make it twelve. There is nothing "
                     "wrong with him, which is the trouble, and the cure is "
                     "to leave."),
                desc("Tobias Frayne has had the parish to tea, twice, and "
                     "nobody fell off anything. The twelfth line in his book "
                     "is empty.", when=sw(db.SW_MER4_DONE)),
            ],
            objectives=[
                obj("leave", "Leave, which is the cure",
                    done=sw(db.SW_MER4_DONE)),
            ]),
        Q.quest(
            "mer5", "The Well at Sump", category="companion",
            giver=who, location="Sump",
            start=started(db.SW_MER5_ON, db.SW_MER5_DONE),
            complete=sw(db.SW_MER5_DONE),
            description=[
                desc("Sump has been under a curse since 1794. Nobody there "
                     "has drunk a glass of water since. Mr Thurle says it is "
                     "a very thorough curse. Merribell says it is a very "
                     "thorough thirst, and has re-formed the Water Committee "
                     "to deal with it."),
                desc("The curse on Sump is lifted, on a motion of the Water "
                     "Committee, re-formed. Sump has had a glass of water.",
                     when=sw(db.SW_MER5_DONE)),
            ]),
        Q.quest(
            "mer1", "The Sisterhouse", category="companion",
            giver=who, location="Weeping Bottom",
            start=started(db.SW_MER1_ON, db.SW_MER1_DONE),
            complete=sw(db.SW_MER1_DONE),
            description=[
                desc("Instead of the eleventh symposium - Whether Anything "
                     "Works, at three - Merribell has proposed the queue at "
                     "the gate: twenty patients each half, and whoever is "
                     "through first is right. Sister Bewick wants it in "
                     "writing."),
                desc("The question was settled by the queue at the gate "
                     "instead of by the eleventh symposium, and Whatever "
                     "Works won, on points. Sister Bewick has it in "
                     "writing.",
                     when=sw(db.SW_MER1_DONE)),
            ],
            objectives=[
                obj("queue", "See the queue through",
                    done=sw(db.SW_MER1_DONE)),
            ]),
        Q.quest(
            "mer3", "The Healers' Table", category="companion",
            giver=who, location="The Slain Wyvern",
            start=started(db.SW_MER3_ON, db.SW_MER3_DONE),
            complete=sw(db.SW_MER3_DONE),
            description=[
                desc("The Table sits in the back room of the Slain Wyvern: "
                     "medics only, who have kept the parties alive and have "
                     "stories about it. Merribell is on the list."),
                desc("The Healers' Table sat, with Merribell on the list, "
                     "and she told them to write it down. They have given "
                     "her the Table's Kit.", when=sw(db.SW_MER3_DONE)),
            ]),
    ]


def hob():
    who = "Hob Grumnir"
    return [
        Q.quest(
            "hob5", "Two Smiths, One Forge", category="companion",
            giver=who, location="Upper Clanging",
            start=started(db.SW_HOB5_FORGED, db.SW_HOB5_DONE),
            complete=sw(db.SW_HOB5_DONE),
            description=[
                desc("A tube plate for the Two Hundred's refit, forty-one "
                     "holes, made at Ollerenshaw's in one heat, by four "
                     "hands. Neither smith finished a sentence. It wants "
                     "carrying up the hill to Ott."),
                desc("The Two Hundred's tube plate was made in one heat, by "
                     "four hands, and Ott tried every hole with a gauge pin. "
                     "True, every one. That will do, she says. They will "
                     "know what she means by it.", when=sw(db.SW_HOB5_DONE)),
            ],
            objectives=[
                obj("ott", "Take the plate up to Ott",
                    done=sw(db.SW_HOB5_DONE)),
            ]),
        Q.quest(
            "hob3", "The Anvil", category="companion",
            giver=who, location="Thistlewick",
            start=started(db.SW_HOB3_GONE, db.SW_HOB3_DONE),
            complete=sw(db.SW_HOB3_DONE),
            description=[
                desc("Somebody has stolen the anvil out of Hob's smithy. "
                     "They will not have got far."),
                desc("The anvil is back in Hob's smithy, to the inch. Two "
                     "apprentices failed module seven, acquisition of a "
                     "heavy object, by eleven feet. The apology is on the "
                     "back of a syllabus, in a very good hand.",
                     when=sw(db.SW_HOB3_DONE)),
            ],
            objectives=[
                obj("anvil", "Find the anvil", done=sw(db.SW_HOB3_DONE)),
            ]),
        Q.quest(
            "hob2", "A Marker", category="companion",
            giver=who, location="Thistlewick churchyard",
            start=started(db.SW_HOB2_ON, db.SW_HOB2_DONE),
            complete=sw(db.SW_HOB2_DONE),
            description=[
                desc("Beatrice Grumnir's grave has no marker of Hob's making. "
                     "He is very large at being at a loss. He will make one "
                     "at the forge, and carry it over, and see."),
                desc("Thistlewick churchyard has a new gate, with a good "
                     "latch. Somebody says the latch wants a spring.",
                     when=sw(db.SW_HOB2_DONE)),
            ],
            objectives=[
                obj("marker", "Make something that is right",
                    done=sw(db.SW_HOB2_DONE)),
            ]),
        Q.quest(
            "hob1", "The Assize of Hammers", category="companion",
            giver=who, location="Great Dunnage",
            start=started(db.SW_HOB1_ON, db.SW_HOB1_DONE),
            complete=sw(db.SW_HOB1_DONE),
            description=[
                desc("The Worshipful Company of Smiths will examine a smith's "
                     "best work, if it is his own work, under clause one, and "
                     "his own property, under clause two. Hob has made a "
                     "great deal, and given all of it away: ten owners, in "
                     "eight places, and Nix."),
                desc("The Worshipful Company of Smiths disqualified Beatrice "
                     "under clause one, and Hob beamed. The Wardens' notes "
                     "say she is right about everything.",
                     when=sw(db.SW_HOB1_DONE)),
            ],
            objectives=[
                obj("owners", "Ask the owners", progress=(db.VAR_HOB1_ASKED, 11)),
                obj("submit", "Go back to the Prime Warden",
                    done=sw(db.SW_HOB1_DONE),
                    visible=var(db.VAR_HOB1_ASKED, ">=", 11)),
            ]),
        Q.quest(
            "hob4", "The Sky Anvil", category="companion",
            giver=who, location="The Sky Anvil",
            start=started(db.SW_HOB4_TRADED, db.SW_HOB4_DONE),
            complete=sw(db.SW_HOB4_DONE),
            description=[
                desc("The Sky Anvil is star-iron. Hob made Meech a gate for "
                     "it, out of the eleven gates in the hedge-bottom, and "
                     "the gate is a very good gate. The star-iron wants "
                     "taking home to the forge."),
                desc("Hob made one sword out of the Sky Anvil's star-iron, "
                     "and he will not say who it is for.", when=sw(db.SW_HOB4_DONE)),
            ],
            objectives=[
                obj("forge", "Take it home to the forge",
                    done=sw(db.SW_HOB4_DONE)),
            ]),
    ]


def zephyrine():
    who = "Zephyrine"
    return [
        done_only(
            "zeph5", "The Lay-By", sw(db.SW_ZEPH5_DONE), who,
            "The west road",
            "Three hedge mages, nine years without a name, in an igloo in a "
            "lay-by. Dunnock taught himself out of a book with four pages "
            "missing, and is better than the Collegium at exactly those "
            "four. He taught Zephyrine page twenty-three, badly, and it "
            "works."),
        Q.quest(
            "zeph1", "The Fines", category="companion",
            giver=who, location="The Collegium Arcanum",
            start=started(db.SW_ZEPH1_ON, db.SW_ZEPH1_DONE),
            complete=sw(db.SW_ZEPH1_DONE),
            description=[
                desc("NOTICE OF OUTSTANDING FINES (ELEVENTH), Miss Z. Vance, "
                     "on study leave. The first ten went to her pigeonhole. "
                     "She was not on study leave. She was EXPELLED."),
                desc("There was never an expulsion: only a draft, referred "
                     "to a committee that has never met.",
                     when=sw(db.SW_ZEPH1_TOLD)),
                desc("There was never an expulsion, and the fines are paid. "
                     "Zephyrine Vance is a member of the Collegium in good "
                     "standing.",
                     when=sw(db.SW_ZEPH1_PAID)),
                desc("There was never an expulsion, so she asked for one. "
                     "The draft is filed, at her own request, and she is "
                     "expelled at last, properly.", when=sw(db.SW_ZEPH1_EXPELLED)),
            ],
            objectives=[
                obj("collegium", "See the Registrar's clerk",
                    done=sw(db.SW_ZEPH1_TOLD)),
                obj("decide", "Settle it, one way or another",
                    done=sw(db.SW_ZEPH1_DONE), visible=sw(db.SW_ZEPH1_TOLD)),
            ]),
        done_only(
            "zeph3", "Dean Fenwold Is Fine", sw(db.SW_ZEPH3_DONE), who,
            "The Collegium Arcanum",
            "On the Kindling of Damp Materials, by Dr Hapgood, went out "
            "under the Master's name, and the Master is a committee. "
            "Zephyrine said so at High Table, once. She has now demonstrated "
            "it. Everybody is fine. The room was wrong."),
        Q.quest(
            "zeph2", "The Duck", category="companion",
            giver=who, location="The Collegium Arcanum",
            start=started(db.SW_ZEPH2_ON, db.SW_ZEPH2_DONE),
            complete=sw(db.SW_ZEPH2_DONE),
            description=[
                desc("Congregation is quorate at twelve: eleven Fellows who "
                     "come to things, and one who is a duck. Every meeting "
                     "for eleven years has been inquorate. The duck is on a "
                     "pond, some way off."),
                desc("Congregation was quorate for the first time in eleven "
                     "years, with all twelve Fellows present, one of them a "
                     "duck. Carried. The duck's proxy is hers.",
                     when=sw(db.SW_ZEPH2_DONE)),
            ],
            objectives=[
                obj("duck", "Fetch the twelfth Fellow",
                    done=any_(sw(db.SW_ZEPH2_WALKING),
                              item(db.IT_DUCK), sw(db.SW_ZEPH2_DONE))),
                obj("vote", "Get it to Congregation",
                    done=sw(db.SW_ZEPH2_DONE)),
            ]),
        done_only(
            "zeph4", "The Cinder Fen", sw(db.SW_ZEPH4_DONE), who,
            "The Cinder Fen",
            "She was expelled for an unsanctioned quantity of fire. The "
            "Commissioner had a form. QUANTITY OF FIRE: nine hundred acres. "
            "SANCTIONED, three times. It burned all afternoon and all "
            "night, and the road is dry."),
    ]


def nix():
    who = "Nix"
    return [
        Q.quest(
            "nix4", "The Longest Loan", category="companion",
            giver=who, location="The Emporium",
            start=started(db.SW_NIX4_BEGUN, db.SW_NIX4_DONE),
            complete=sw(db.SW_NIX4_DONE),
            description=[
                desc("Eleven things have been in Nix's ledger since the "
                     "beginning with nothing in the RETURNED column. This is "
                     "the afternoon they go back: three towns, eleven owners, "
                     "and none of them aware it had gone."),
                desc("The ledger is ruled off. Hulda Bole gave Nix something "
                     "better: a parcel, for a client not yet identified.",
                     when=sw(db.SW_NIX4_DONE)),
            ],
            objectives=[
                obj("returns", "Return the eleven",
                    progress=(db.VAR_NIX4_RETURNED, 11)),
            ]),
        Q.quest(
            "nix5", "Half An Encounter", category="companion",
            giver=who, location="The Gloamwood",
            start=any_(MOUTH, sw(db.SW_NIX5_ON), sw(db.SW_NIX5_DONE)),
            complete=sw(db.SW_NIX5_DONE),
            description=[
                desc("Enoch Bagshawe, first bassoon to the Upper Clanging "
                     "Works Band, has one reed that took three weeks, and "
                     "it goes the moment anything looks at him. He would "
                     "like to cross the Gloamwood by night. Nix halves "
                     "encounters. Half an encounter is still an encounter."),
                desc("Enoch Bagshawe crossed the Gloamwood by night without "
                     "a single encounter, or half of one. The Works Band has "
                     "a bassoon.",
                     when=sw(db.SW_NIX5_DONE)),
            ],
            objectives=[
                obj("through", "Take Mr Bagshawe through",
                    done=sw(db.SW_NIX5_DONE)),
            ]),
        Q.quest(
            "nix1", "The Client", category="companion",
            giver=who, location="Great Dunnage",
            start=started(db.SW_NIX1_LETTER, db.SW_NIX1_DONE),
            complete=sw(db.SW_NIX1_DONE),
            description=[
                desc("The parcel was a letter in Nix's own hand: NOT TO BE "
                     "OPENED UNTIL I AM TWENTY-SIX. The client is Nix, aged "
                     "fifteen, and there is a ticket for Bond No. 1, in "
                     "Great Dunnage."),
                desc("Bond No. 1 was her gran's coat, too long for her at "
                     "fifteen, not to be worn until it fitted. It fits.",
                     when=sw(db.SW_NIX1_DONE)),
            ],
            objectives=[
                obj("bond", "Collect Bond No. 1", done=sw(db.SW_NIX1_DONE)),
            ]),
        Q.quest(
            "nix2", "The Counting House", category="companion",
            giver=who, location="Great Dunnage",
            start=started(db.SW_NIX2_OPEN, db.SW_NIX2_DONE),
            complete=sw(db.SW_NIX2_DONE),
            description=[
                desc("The Door of the Sealed Counting House is open, "
                     "informally. Form L is not completed. The Opening "
                     "proper will follow on its completion. The Mayor has "
                     "gone in at something close to a run."),
                desc("Behind the Door of the Sealed Counting House there is "
                     "one chair, and a note: WE SPENT IT. J. Pocklington, "
                     "Clerk to the Corporation, 1788. It is a very good "
                     "chair.",
                     when=sw(db.SW_NIX2_DONE)),
            ],
            objectives=[
                obj("vault", "See what is inside", done=sw(db.SW_NIX2_DONE)),
            ]),
        Q.quest(
            "nix3", "Professional Courtesy", category="companion",
            giver=who, location="Nether Sopping",
            start=started(db.SW_NIX3_ON, db.SW_NIX3_DONE),
            complete=sw(db.SW_NIX3_DONE),
            description=[
                desc("Cobb Lorrimer, registered under T, says locating is "
                     "stealing with a waistcoat on. The challenge is a "
                     "client, a list and an afternoon. The client is Sops "
                     "and Tibb. The list is in a child's hand: ONE ROPE. ONE "
                     "HELMIT. ONE SWORD. ONE DARK LORD (WHO LOSES)."),
                desc("Nix won Cobb Lorrimer's challenge on paperwork: the "
                     "whole list located, with permission, and receipts.", when=sw(db.SW_NIX3_DONE)),
            ],
            objectives=[
                obj("list", "Locate the list", progress=(db.VAR_NIX3_LOCATED, 3)),
            ]),
    ]


def aldric():
    who = "Sir Aldric"
    return [
        done_only(
            "ald4", "The Horse", sw(db.SW_ALD4_DONE), who, "Great Dunnage",
            "Nobody had asked Sir Aldric about his horse in six years, "
            "including Sir Aldric. She walked into Plummer's yard one winter "
            "with a good saddle on and nobody in it, and she is a partner in "
            "the haulage business now. She is doing so well. He may visit "
            "any day but a Tuesday."),
        done_only(
            "ald3", "The Chapter House", sw(db.SW_ALD3_DONE), who,
            "Coldbarrow",
            "The committee could not fault his nine pins, and so had to "
            "fault the knight, and offered him a desk and a pin that does "
            "not move. He said it was the finest thing he had been offered "
            "in nine years, and no. Knight Errant, At Large: they made it up "
            "for him, on a Thursday."),
        Q.quest(
            "ald1", "The Errand", category="companion",
            giver=who, location="Little Gore",
            start=any_(item(db.IT_ALD1_LETTER), sw(db.SW_ALD1_DONE)),
            complete=sw(db.SW_ALD1_DONE),
            description=[
                desc("TO THE PARISH OF LITTLE GORE. BY HAND. P-G. His father "
                     "gave it him the morning he rode out: four miles, your "
                     "first errand, deliver it and then you may go errant. "
                     "He has been errant for nine years."),
                desc("The letter to the Parish of Little Gore is delivered, "
                     "by hand, nine years late. He may now go errant.",
                     when=sw(db.SW_ALD1_DONE)),
            ],
            objectives=[
                obj("deliver", "Deliver the letter", done=sw(db.SW_ALD1_DONE)),
            ]),
        done_only(
            "ald5", "The Fourth", sw(db.SW_ALD5_DONE), who, "Little Gore",
            "Pemberton-Gore the Fourth found Little Gore first time, and "
            "would like to squire. He can find gates. Every other "
            "Pemberton-Gore came over the wall; his uncle went OUT. He walks "
            "three paces behind now, and says if his uncle is facing the "
            "wrong way. He always is. It's on the arms."),
        done_only(
            "ald2", "The Vigil", sw(db.SW_ALD2_DONE), who, "Weeping Bottom",
            "Dusk to dawn, in the right chapel at last - he had kept vigil in "
            "eleven wrong ones. Sir Hamo Tench sat at the back and coughed. "
            "Confirmed: the first in thirty years."),
        done_only(
            "ald6", "The Wrong Dragon", sw(db.SW_ALD6_DONE), who,
            "The Wrong Dragon's cave",
            "Eight years ago he was sent to slay a dragon and arrived at a "
            "different one, and they talked about Horace for four hours. "
            "Horace was a poet. He was talking about his horse. The right "
            "dragon was slain by somebody else. This one was read to, and "
            "the commission reported on, on its back."),
    ]


def piper():
    who = "Piper Quill"
    return [
        done_only(
            "pip2", "A Rhyme for Turnip", sw(db.SW_PIP2_DONE), who,
            "The Gilded Turnip",
            "There is no rhyme for turnip. Everybody had a go, and every "
            "suggestion was worse than the last. Piper changed the other "
            "line, in nine seconds, and everybody who spent the afternoon on "
            "it is furious."),
        Q.quest(
            "pip5", "The Struck Verses", category="companion",
            giver=who, location="Prophecy Hall",
            start=sw(db.SW_PIP5_ASKED), complete=sw(db.SW_PIP5_DONE),
            description=[
                desc("The Committee keeps a box of verses it struck and "
                     "never printed. To consult it takes Form S-7, "
                     "countersigned, and the key on Councillor Fenn's hook. "
                     "Nobody is listening to Councillor Fenn. Remember him."),
                desc("The box was opened, and shut again, and the key went "
                     "back on the hook. Piper has read every verse in it, "
                     "and printed none.", when=sw(db.SW_PIP5_DONE)),
            ],
            objectives=[
                obj("form", "Get Form S-7 countersigned",
                    done=any_(sw(db.SW_PIP5_SIGNED), sw(db.SW_PIP5_DONE))),
                obj("key", "Get the key off Fenn's hook",
                    done=any_(sw(db.SW_PIP5_KEY), sw(db.SW_PIP5_DONE))),
                obj("box", "Open the box", done=sw(db.SW_PIP5_DONE)),
            ]),
        Q.quest(
            "pip3", "Contest at the Bell", category="companion",
            giver=who, location="Great Dunnage",
            start=started(db.SW_PIP3_ON, db.SW_PIP3_DONE),
            complete=sw(db.SW_PIP3_DONE),
            description=[
                desc("The Contest at the Sign of the Bell is always tonight; "
                     "they have simply not had the entries. Nobody has ever "
                     "entered Ballad (Not Sad). Piper Quill is aware of "
                     "that."),
                desc("Second place in Ballad (Not Sad), by one point, to a "
                     "thrush. The certificate is framed.", when=sw(db.SW_PIP3_DONE)),
            ],
            objectives=[
                obj("set", "Perform her set", done=sw(db.SW_PIP3_DONE)),
            ]),
        Q.quest(
            "pip4", "The Elegy", category="companion",
            giver=who, location="Little Gore",
            start=started(db.SW_PIP4_ON, db.SW_PIP4_DONE),
            complete=sw(db.SW_PIP4_DONE),
            description=[
                desc("Abel Thrush carried the post between Little Gore, "
                     "Fenmarch and Sump every day for fifty years. Somebody "
                     "has nailed a card to the back of the fingerpost, where "
                     "nobody reads but a chronicler. Everybody knew him, and "
                     "each of them knew him differently."),
                desc("An elegy for Abel Thrush, the carrier: nine lines, "
                     "pinned up, and not performed.",
                     when=sw(db.SW_PIP4_DONE)),
            ],
            objectives=[
                obj("accounts", "Hear about Abel Thrush",
                    progress=(db.VAR_PIP4_HEARD, 11)),
                obj("elegy", "Write the elegy", done=sw(db.SW_PIP4_DONE)),
            ]),
        Q.quest(
            "pip1", "The Authorised Version", category="companion",
            giver=who, location="Prophecy Hall",
            start=started(db.SW_PIP1_ON, db.SW_PIP1_DONE),
            complete=sw(db.SW_PIP1_DONE),
            description=[
                desc("Ambrosine Quill, Chronicler to the Committee, has "
                     "finished THE LAY OF THE FORTY-EIGHTH. The Committee "
                     "approved it on Tuesday. Bram has not finished yet. The "
                     "shape has. It is in twelve cantos, and there is "
                     "no turnip in any of them."),
                desc("Piper read it again, and found it very good. One "
                     "footnote, in small type: None of this happened. It is "
                     "very good. - P.Q.", when=sw(db.SW_PIP1_GOOD)),
                desc("THE LAY OF THE FORTY-EIGHTH, fixed, in metre, in an "
                     "afternoon, by A. & P. Quill.",
                     when=sw(db.SW_PIP1_FIXED)),
            ]),
    ]


def corvin():
    who = "Corvin Ash"
    return [
        done_only(
            "cor5", "The Appraisal", sw(db.SW_COR5_DONE), who,
            "Great Dunnage",
            "No curse. A very good sword in very poor condition, with a name "
            "on the tang nobody has used for a while. He asked what a curse "
            "would cost to have put on. It is not expensive. There is a "
            "form."),
        Q.quest(
            "cor1", "Ashcombe (New)", category="companion",
            giver=who, location="Ashcombe",
            start=started(db.SW_COR1_ON, db.SW_COR1_DONE),
            complete=sw(db.SW_COR1_DONE),
            description=[
                desc("One name on Ashcombe's Roll is marked Away. (Written "
                     "to.) Two hundred and six people stood on a hill in the "
                     "rain and counted him anyway. Today, then."),
                desc("His mother has a new kitchen, his room is a study, and "
                     "the speech at the Flood Dinner went well. Nothing went "
                     "wrong. There is a scarf.", when=sw(db.SW_COR1_DONE)),
            ],
            objectives=[
                obj("home", "Go home", done=sw(db.SW_COR1_HOME)),
                obj("dinner", "Speak at the Flood Dinner",
                    done=sw(db.SW_COR1_DONE), visible=sw(db.SW_COR1_HOME)),
            ]),
        Q.quest(
            "cor2", "Ashcombe (Old)", category="companion",
            giver=who, location="Ashcombe Lake",
            start=started(db.SW_COR2_STEP, db.SW_COR2_DONE),
            complete=sw(db.SW_COR2_DONE),
            description=[
                desc("The lake is let down once a year, for the sluices, and "
                     "that week you can walk the street at the bottom. His "
                     "grandfather made the sword. It was the doorstop."),
                desc("Under the lake, in a strongbox in the schoolroom, the "
                     "schoolmistress kept everybody's reports. His says he "
                     "will go far, if he ever gets up.",
                     when=sw(db.SW_COR2_DONE)),
            ],
            objectives=[
                obj("school", "Look in the schoolroom",
                    done=sw(db.SW_COR2_DONE)),
            ]),
        Q.quest(
            "cor3", "The Rivals' Retreat", category="companion",
            giver=who, location="The Sable Hart",
            start=started(db.SW_COR3_ON, db.SW_COR3_DONE),
            complete=sw(db.SW_COR3_DONE),
            description=[
                desc("The league table: 17. C. ASH 0 (no meetings attended). "
                     "Seventeenth, of seventeen, behind Blackwood, and "
                     "Blackwood is NEW. Points are scored at meetings."),
                desc("Corvin Ash has attended a meeting, and is second in "
                     "the league table. His chair is kept.",
                     when=sw(db.SW_COR3_DONE)),
            ],
            objectives=[
                obj("meeting", "Attend a meeting", done=sw(db.SW_COR3_DONE)),
            ]),
        done_only(
            "cor4", "Mother Selvidge", sw(db.SW_COR4_DONE), who, "The Fair",
            "Eleven years ago, for two crowns, she told him he was the rival "
            "of a great hero. She tells about four young men a year, because "
            "it is the reading that makes them stand up straight, and it has "
            "never once been wrong. They all went and did something."),
    ]


def wren():
    who = "Wren Halloway"
    return [
        Q.quest(
            "wre2", "The Second Plaque", category="companion",
            giver=who, location="The Slain Wyvern",
            start=sw(db.SW_WRE2_ASKED), complete=sw(db.SW_WRE2_UP),
            description=[
                desc("Wren was asked to leave the Slain Wyvern for saying "
                     "that the wyvern is a goose. It is a goose. She would "
                     "like a retraction. Dorcas will read a second plaque. "
                     "Engraving is a crown a letter."),
                desc("A second plaque, on the other side of the fire. It "
                     "neither corrects the first nor repeats it.",
                     when=sw(db.SW_WRE2_UP)),
            ],
            objectives=[
                obj("plate", "Have a plate engraved",
                    done=any_(item(db.IT_BRASS_PLATE), sw(db.SW_WRE2_UP))),
                obj("up", "Put it up, with Wren there",
                    done=sw(db.SW_WRE2_UP)),
            ]),
        done_only(
            "wre5", "Bramus", sw(db.SW_WRE5_NAMED), who, "Bram's field",
            "Wren has named a small brown thing in Bram's turnip field after "
            "him, and then explained why. It is statistically indefensible. "
            "It has a labelled stick."),
        Q.quest(
            "wre3", "The Gloamwood Society", category="companion",
            giver=who, location="The Gilded Turnip",
            start=started(db.SW_WRE3_WALK, db.SW_WRE3_DONE),
            complete=sw(db.SW_WRE3_DONE),
            description=[
                desc("The Gloamwood Society has discussed The Sighting four "
                     "times a year since 1960, and once a year it goes for a "
                     "walk. Wren is going with them, and would like a proper "
                     "look."),
                desc("The Thing in the Gloamwood is proved not to exist. Miss "
                     "Pellow counted nine, in 1971. She was right.",
                     when=sw(db.SW_WRE3_DONE)),
            ],
            objectives=[
                obj("walk", "Walk to the deep clearing",
                    done=sw(db.SW_WRE3_DONE)),
            ]),
        Q.quest(
            "wre1", "The Monograph", category="companion",
            giver=who, location="The Collegium Arcanum",
            start=sw(db.SW_WRE1_ON), complete=sw(db.SW_WRE1_DONE),
            description=[
                desc("A monograph of the Collegium requires a type specimen "
                     "for every entry, three Fellows to review it, and a list "
                     "of subscribers. Rowbotham named three hundred species "
                     "and never had a type specimen for one of them. He "
                     "named them after his dogs."),
                desc("Wren Halloway's monograph of the Collegium is "
                     "published, and on the shelf, in the inch-wide gap.",
                     when=sw(db.SW_WRE1_DONE)),
            ],
            objectives=[
                obj("specimens", "Measure type specimens",
                    progress=(db.VAR_WRE1_SPECIMENS, 11)),
                obj("mott", "A review: Professor Mott",
                    done=sw(db.SW_WRE1_MOTT)),
                obj("furze", "A review: Dr Furze", done=sw(db.SW_WRE1_FURZE)),
                obj("duck", "A review: the Honorary Fellow",
                    done=sw(db.SW_WRE1_DUCK), hidden="mask",
                    visible=any_(sw(db.SW_WRE1_DUCK_DUE), sw(db.SW_WRE1_DUCK))),
            ]),
        Q.quest(
            "wre4", "The Cabinet", category="companion",
            giver=who, location="Fenmarch Hall",
            start=started(db.SW_WRE4_ON, db.SW_WRE4_DONE),
            complete=sw(db.SW_WRE4_DONE),
            description=[
                desc("Mrs Puddifoot dusts all eighty specimens, Friday to "
                     "Wednesday, and has asked a proper naturalist, with the "
                     "jars, to authenticate them. Dr Rowbotham named "
                     "everything. That was the problem."),
                desc("Fenmarch's cabinet of eighty specimens is written up, "
                     "honestly, every join of it, and the family has paid "
                     "the fee.",
                     when=sw(db.SW_WRE4_DONE)),
            ],
            objectives=[
                obj("joins", "See Mr Ottershaw's joins",
                    done=any_(sw(db.SW_WRE4_JOINS), sw(db.SW_WRE4_DONE))),
                obj("write", "Write it up, honestly",
                    done=sw(db.SW_WRE4_DONE)),
            ]),
    ]


def roland():
    who = "Roland"
    return [
        Q.quest(
            "rol4", "The Maker's Mark", category="companion",
            giver=who, location="Thistlewick",
            start=sw(db.SW_ROL4_SEEN), complete=sw(db.SW_ROL4_SEEN),
            description=[
                desc("The sword Roland carries has a mark on it, and Hob "
                     "knows the mark. It was made at the forge in "
                     "Thistlewick forty years ago, and sold, and travelled, "
                     "and came back. She did good work, Hob says."),
                desc("The sword was made at the forge in Thistlewick forty "
                     "years ago. It is back, on an ash haft, as an axe, in "
                     "a Thistlewick hand.", when=sw(db.SW_ROL4_REFIT)),
            ]),
        Q.quest(
            "rol3", "The Alumni", category="companion",
            giver=who, location="The Slain Wyvern",
            start=started(db.SW_ROL3_DINNER, db.SW_ROL3_DONE),
            complete=sw(db.SW_ROL3_DONE),
            description=[
                desc("THE FAIRWEATHER ALUMNI: eleven parties who finished "
                     "their quests without him, at dinner, in the Slain "
                     "Wyvern, at capacity. Every one of them says 'our "
                     "Roland'."),
                desc("Eleven parties drank to Roland Fairweather, who got "
                     "them all to the door. The card on the board is signed "
                     "eleven times.",
                     when=sw(db.SW_ROL3_DONE)),
            ],
            objectives=[
                obj("guests", "Speak to the eleven",
                    progress=(db.VAR_ROL3_HEARD, 11)),
            ]),
        Q.quest(
            "rol1", "The Appointment", category="companion",
            giver=who, location="Great Dunnage",
            start=started(db.SW_ROL1_ON, db.SW_ROL1_DONE),
            complete=sw(db.SW_ROL1_DONE),
            description=[
                desc("The snug at the Bell is booked in his name. The usual. "
                     "Roland went slightly pink, and asked you not to say "
                     "anything."),
                desc("The hundred and forty-first meeting. The stone is not "
                     "ready. The asset is available. Noted, with thanks. "
                     "Eleven minutes.", when=sw(db.SW_ROL1_DONE)),
            ],
            objectives=[
                obj("meeting", "Sit the meeting", done=sw(db.SW_ROL1_DONE)),
            ]),
        Q.quest(
            "rol5", "The Understudy", category="companion",
            giver=who, location="Great Dunnage",
            start=started(db.SW_ROL5_ON, db.SW_ROL5_DONE),
            complete=sw(db.SW_ROL5_DONE),
            description=[
                desc("Maud Penhallow, sixteen, has been in Fellow Blunt's "
                     "yard since she was nine: sword, horse, lineage, the "
                     "lot. She has been told it is nearly ready. Roland was "
                     "told that when he was twelve. He does not know whether "
                     "to tell her."),
                desc("He told her. She asked whose. She has gone north.",
                     when=sw(db.SW_ROL5_DONE)),
            ],
            objectives=[
                obj("tell", "Decide whether to tell her",
                    done=sw(db.SW_ROL5_DONE)),
            ]),
        Q.quest(
            "rol2", "Roland's Own Quest", category="companion",
            giver=who, location="Carn Drey",
            start=started(db.SW_ROL2_ON, db.SW_ROL2_DONE),
            complete=sw(db.SW_ROL2_DONE),
            description=[
                desc("WHEN THE STONE IS READY, ONE OF THE LINE SHALL DRAW THE "
                     "SWORD THEREFROM, AND GO DOWN UNDER CARN DREY. He knows "
                     "it by heart. Fellow Blunt checks the stone quarterly, "
                     "from the gate. Nobody has gone down the stairs to look. "
                     "GONE TO SEE."),
                desc("The sword is out of the stone, and the Worm of Carn "
                     "Drey is ended. Discharged.",
                     when=sw(db.SW_ROL2_DONE)),
            ],
            objectives=[
                obj("stone", "Go down and look", done=sw(db.SW_ROL2_DRAWN)),
                obj("worm", "Go further down", done=sw(db.SW_ROL2_DONE),
                    visible=sw(db.SW_ROL2_DRAWN)),
            ]),
    ]


def spare():
    who = "Spare Cotterill"
    return [
        Q.quest(
            "spa1", "The Letters", category="companion",
            giver=who, location="Upper Clanging",
            start=sw(db.SW_SPARE_KNOWN), complete=sw(db.SW_SPA1_DONE),
            description=[
                desc("His mother's third term was: you write. The post is a "
                     "courier in a red coat, who is already standing in "
                     "every town when you get there and never explains. "
                     "Spare writes the letters. They do not have to be "
                     "true."),
                desc("Read out to the shift at the dinner hour. There was no "
                     "dragon. His mother did more potatoes anyway.",
                     when=sw(db.SW_SPA1_DONE)),
            ],
            objectives=[
                obj("post", "Post a letter home",
                    progress=(db.VAR_SPA1_POSTED, 8)),
                obj("dinner", "Go home for the dinner hour",
                    done=sw(db.SW_SPA1_DONE),
                    visible=var(db.VAR_SPA1_POSTED, ">=", 8)),
            ]),
        Q.quest(
            "spa4", "The Pen Pal", category="companion",
            giver=who, location="Much Pottering",
            start=any_(var(db.VAR_SPA4_TOUR, ">=", 1), sw(db.SW_SPA4_DONE)),
            complete=sw(db.SW_SPA4_DONE),
            description=[
                desc("Effie Gotobed of Much Pottering has been his pen pal "
                     "since he was six. She told him about a volcano and a "
                     "sea serpent. He told her he drives the Two Hundred. "
                     "They knew each other at once, and they are both "
                     "furious about it."),
                desc("Effie showed Spare round Much Pottering, and they each "
                     "wrote one letter on the spot. The courier carried them "
                     "four steps.",
                     when=sw(db.SW_SPA4_DONE)),
            ],
            objectives=[
                obj("tour", "Let Effie show him round",
                    done=sw(db.SW_SPA4_DONE)),
            ]),
        Q.quest(
            "spa2", "Ninety Tubes", category="companion",
            giver=who, location="Great Dunnage",
            start=started(db.SW_SPA2_ASKED, db.SW_SPA2_CLEARED,
                          db.SW_SPA2_DONE),
            complete=sw(db.SW_SPA2_DONE),
            description=[
                desc("Something is on the paddle of the bottom lock, thirty "
                     "boats are sat on the cut, and the Canal Company's "
                     "smallest man went in at eleven and has not come out. "
                     "A man does not fit. Spare fits."),
                desc("Spare went into the bottom lock alone, in the dark, "
                     "and came out by the ladder, and everybody was there. "
                     "Thirty boats went down the cut.", when=sw(db.SW_SPA2_DONE)),
            ],
            objectives=[
                obj("paddle", "Clear the paddle",
                    done=any_(sw(db.SW_SPA2_CLEARED), sw(db.SW_SPA2_DONE))),
                obj("out", "Come back up the ladder",
                    done=sw(db.SW_SPA2_DONE)),
            ]),
        Q.quest(
            "spa3", "The Tenth", category="postgame",
            giver=who, location="Upper Clanging",
            start=sw(db.SW_SPA3_LETTER), complete=sw(db.SW_SPA3_DONE),
            description=[
                desc("Dear Mam. Is it spring yet? Spare. He asks every "
                     "morning as well."),
                desc("Dear Mam. Is it spring yet? It is. Spare cannot miss "
                     "this.",
                     when=sw(db.SW_SPA3_SPRING)),
                desc("It is spring, and every Cotterill in Upper Clanging is "
                     "indoors today.",
                     when=sw(db.SW_SPA3_INSIDE)),
                desc("Ten Cotterills. The new one is a girl, called Washer. "
                     "Clevis had it at twenty to one, and has had to pay "
                     "out.",
                     when=sw(db.SW_SPA3_DONE)),
            ],
            objectives=[
                obj("spring", "Wait for spring", done=sw(db.SW_SPA3_SPRING)),
                obj("home", "Take him home",
                    done=any_(sw(db.SW_SPA3_INSIDE), sw(db.SW_SPA3_DONE)),
                    visible=sw(db.SW_SPA3_SPRING)),
                obj("morning", "Wait for the morning",
                    done=sw(db.SW_SPA3_DONE), visible=sw(db.SW_SPA3_INSIDE)),
            ]),
    ]


# ========================================================== the post-game ==
def postgame_quests():
    return [
        Q.quest(
            "clause_nineteen", "Clause Nineteen", category="postgame",
            giver="The Committee", location="Nether Sopping",
            start=any_(LETTER, sw(db.SW_COTTAGE_SEEN)),
            complete=sw(db.SW_COTTAGE_SEEN),
            description=[
                desc("With the Committee's congratulations on your return: "
                     "your pension, and the key to a cottage at Nether "
                     "Sopping, at such distance as is mutually agreeable. "
                     "They trust Friday will suit."),
                desc("The cottage was Ambrose Fitch's. There is a chair "
                     "facing the window, a bed you may use, and a pot with a "
                     "dead thing in it. You do not have to live there.",
                     when=sw(db.SW_COTTAGE_SEEN)),
            ],
            objectives=[
                obj("cottage", "Find the cottage",
                    done=sw(db.SW_COTTAGE_SEEN)),
            ]),
        Q.quest(
            "the_stair", "The Door", category="postgame",
            giver="Sir Dunstable", location="The Door into the Mountain",
            start=any_(item(db.IT_LAMP), sw(db.SW_STAIR_IN)),
            complete=sw(db.SW_UNSCHEDULED),
            description=[
                desc("NO ADMITTANCE WITHOUT A LAMP. Sir Dunstable has lent "
                     "you the lamp off the hook. Behind the Door into the "
                     "Mountain is a stair going down into a dark that does "
                     "not stop."),
                desc("His chalk marks go down the walls, D. 1 at the Door, "
                     "each a little further down than the last.",
                     when=sw(db.SW_STAIR_IN)),
                desc("At the bottom of the Stair, past the last of Sir "
                     "Dunstable's marks, was something nobody had "
                     "anticipated. It has been met.",
                     when=sw(db.SW_UNSCHEDULED)),
            ],
            objectives=[
                obj("door", "Go through the Door", done=sw(db.SW_STAIR_IN)),
                obj("bottom", "Find the bottom", done=sw(db.SW_UNSCHEDULED),
                    visible=sw(db.SW_STAIR_IN)),
            ]),
        Q.quest(
            "form_z", "Form Z", category="postgame",
            giver="Something Unscheduled", location="Nether Sopping",
            start=any_(item(db.IT_BOUNTY_CARD), sw(db.SW_FORM_Z)),
            complete=sw(db.SW_FORM_Z),
            description=[
                desc("It wrote a bounty on itself, and wanted it stamped. A "
                     "bounty is claimed by a member, in person, at the "
                     "Guild's desk. The card has no authority and no number, "
                     "and a drawing of an octopus on the back."),
                desc("Form Z, Matters Not Anticipated. Registrar Pell had "
                     "kept it forty years, in case. DISCHARGED.",
                     when=sw(db.SW_FORM_Z)),
            ],
            objectives=[
                obj("pell", "Take the card to the Guild",
                    done=sw(db.SW_FORM_Z)),
            ]),
    ]


def quests():
    out = (main_quests() + south_quests() + north_quests() + meadow_quests()
           + merribell() + hob() + zephyrine() + nix() + aldric() + piper()
           + corvin() + wren() + roland() + spare() + postgame_quests())
    return out


def build(game):
    """Install the plugin and write `data/Quests.json`. The menu entry is
    there from the first screen (Mike, 7 Oct 2026), so no `menuSwitch`."""
    Q.install(game)
    Q.write(game, quests())


if __name__ == "__main__":
    for q in quests():
        print("%-16s %s" % (q["key"], q["title"]))
