import numpy as np
from ai import *
from data import ships
from gameplay import Battle, Ship


def play(attacker: BasicAI, defender: BasicAI):
    # set up the battle with random ships
    battle = Battle()
    ship_types = list(ships.keys())
    for i in range(3):
        atk = np.random.choice(ship_types)
        battle.add_attacker(Ship(atk, ships[atk]), i)
        opp = np.random.choice(ship_types)
        battle.add_defender(Ship(opp, ships[opp]), i)
    battle.print_state()

    # play out the battle until done
    while not battle.finished:
        # advance battle to the next volley
        data = battle.proceed_to_next_volley()
        # query the AI what to do next
        target = attacker.get_next_target(data) if data.active < 3 else defender.get_next_target(data)
        # fire the volley
        battle.fire_volley(data.active, target)


if __name__ == '__main__':
    play(RandomAI(), RandomAI())
