import numpy as np
from data import ships
from gameplay import Battle, Ship


def play():
    battle = Battle()
    ship_types = list(ships.keys())
    for i in range(3):
        atk = np.random.choice(ship_types)
        battle.add_attacker(Ship(atk, ships[atk]), i)
        opp = np.random.choice(ship_types)
        battle.add_defender(Ship(opp, ships[opp]), i)
    print(battle)

    for t in range(100):
        next_ship = battle.wait_for_next_ship()
        print("                             TURN", t + 1)
        print(battle)
        target: Ship = np.random.choice(battle.get_valid_targets(next_ship))
        print("{0} fires at {1}!".format(next_ship, target))
        next_ship.fire(target)
        if target.is_sunk:
            battle.remove_ship(target)
        next_ship.reset_cooldown()
        print(battle)
        print(battle.data)
        if battle.victor:
            print("{0} win the battle!".format(battle.victor))
            break


if __name__ == '__main__':
    play()
