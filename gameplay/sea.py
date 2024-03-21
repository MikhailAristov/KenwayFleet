from numpy.random import uniform as randf
from typing import List
from gameplay.ship import Ship


class Sea:

    all_ships: List[Ship] = []
    attackers: List[Ship] = [None, None, None]
    defenders: List[Ship] = [None, None, None]

    def add_attacker(self, ship: Ship, pos: int):
        self.attackers[pos] = ship
        self.all_ships.append(ship)

    def add_defender(self, ship: Ship, pos: int):
        ship.hit_points *= randf(.85, 1.)
        self.defenders[pos] = ship
        self.all_ships.append(ship)

    def __str__(self) -> str:
        width = 64
        separator = '~' * width
        format_str: str = " A{0:d}. {1:<" + str(width // 2 - 5) + "}{2:>" + str(width // 2 - 5) + "} D{0:d}."
        rows = [separator]
        for i in range(3):
            rows.append(format_str.format(i + 1, str(self.attackers[i]), str(self.defenders[i])))
        rows.append(separator)
        return '\r\n'.join(rows)
