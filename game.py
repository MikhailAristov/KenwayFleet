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

    for t in range(3):
        print(sea)
        next_ship = sea.wait_for_next_ship()
        print(str(next_ship), "fires!")
        next_ship.reset_cooldown()


if __name__ == '__main__':
    play()
