import numpy as np
from data import ships
from gameplay import Sea, Ship


def play():
    sea = Sea()
    ship_types = list(ships.keys())
    for i in range(3):
        atk = np.random.choice(ship_types)
        sea.add_attacker(Ship(atk, ships[atk]), i)
        opp = np.random.choice(ship_types)
        sea.add_defender(Ship(opp, ships[opp]), i)
    print(sea)

    for t in range(100):
        next_ship = sea.wait_for_next_ship()
        print("                             TURN", t + 1)
        print(sea)
        target: Ship = np.random.choice(sea.get_valid_targets(next_ship))
        print("{0} fires at {1}!".format(next_ship, target))
        next_ship.fire(target)
        if target.is_sunk:
            sea.remove_ship(target)
        next_ship.reset_cooldown()
        print(sea)
        if sea.victor:
            print("{0} win the battle!".format(sea.victor))
            break


if __name__ == '__main__':
    play()
