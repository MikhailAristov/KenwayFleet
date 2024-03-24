from numpy.random import choice
from ai import *
from data import ships
from gameplay import Battle, Ship


def play(attacker: Targeter, defender: Targeter) -> str:
    # set up the battle with random defending ships
    battle = Battle()
    for def_ship in choice(list(ships.keys()), 3):
        battle.add_defender(Ship(def_ship, ships[def_ship]))
    # Pick a legal lineup at random
    for atk_ship in attacker.get_attacking_flotilla(ships, battle.defenders):
        battle.add_attacker(atk_ship)
    battle.print_state()

    # play out the battle until done
    while not battle.winner:
        # advance battle to the next volley
        data = battle.proceed_to_next_volley(verbose=True)
        # query the AI what to do next
        target = attacker.get_next_target(data) if data.active < 3 \
            else defender.get_next_target(data)
        # fire the volley
        battle.fire_volley(data.active, target, verbose=True)

    return battle.winner


if __name__ == '__main__':
    ATK = MinimaxTargeter(level=15)
    DEF = UtilityBasedTargeter()
    _ = play(ATK, DEF)
