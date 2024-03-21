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


if __name__ == '__main__':
    play()
