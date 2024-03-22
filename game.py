import numpy as np
from ai import *
from data import ships
from gameplay import Battle, Ship


def play(attacker: Targeter, defender: Targeter) -> str:
    # set up the battle with random ships
    battle = Battle()
    ship_types = list(ships.keys())
    ship_weights = np.array([1. / ships[t]['level'] for t in ship_types])
    ship_weights /= sum(ship_weights)
    for i in range(3):
        atk = np.random.choice(ship_types, p=ship_weights)
        battle.add_attacker(Ship(atk, ships[atk]), i)
        opp = np.random.choice(ship_types, p=ship_weights)
        battle.add_defender(Ship(opp, ships[opp]), i)
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
