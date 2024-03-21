import numpy as np
from ai import *
from data import ships
from gameplay import Battle, Ship


def play(attacker: BasicAI, defender: BasicAI):
    battle = Battle()
    ship_types = list(ships.keys())
    for i in range(3):
        atk = np.random.choice(ship_types)
        battle.add_attacker(Ship(atk, ships[atk]), i)
        opp = np.random.choice(ship_types)
        battle.add_defender(Ship(opp, ships[opp]), i)
    print(battle)

    turn = 1
    while not battle.victor:
        next_ship = battle.wait_for_next_ship()
        print("                             TURN", turn)
        print(battle)
        pos = attacker.get_next_target(battle.data)
        target: Ship = battle.get_ship_at_position(pos)
        print("{0} fires at {1}!".format(next_ship, target))
        next_ship.fire(target)
        if target.is_sunk:
            battle.remove_ship(target)
        next_ship.reset_cooldown()
        print(battle)
        turn += 1

    print("{0} win the battle!".format(battle.victor))


if __name__ == '__main__':
    AI = RandomAI()
    play(AI, AI)
