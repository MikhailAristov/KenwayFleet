from numpy.random import uniform as randf
from typing import List
from gameplay.ship import Ship


class Sea:
    all_ships: List[Ship] = []
    attackers: List[Ship] = [None, None, None]
    defenders: List[Ship] = [None, None, None]

    def add_attacker(self, ship: Ship, pos: int):
        ship.cooldown *= randf(.95, .999)
        self.attackers[pos] = ship
        self.all_ships.append(ship)

    def add_defender(self, ship: Ship, pos: int):
        ship.cooldown *= randf(.95, .999)
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

    def wait_for_next_ship(self) -> Ship:
        next_ship: Ship = min(self.all_ships, key=lambda x: x.remaining_steps)
        steps = next_ship.remaining_steps
        for s in self.all_ships:
            s.cool(steps)
        return next_ship

    def get_valid_targets(self, for_ship: Ship) -> List[Ship]:
        assert for_ship is not None
        if for_ship in self.attackers:
            return [s for s in self.defenders if s is not None and not s.is_sunk]
        elif for_ship in self.defenders:
            return [s for s in self.attackers if s is not None and not s.is_sunk]
        raise "Invalid ship!"

    def remove_ship(self, ship: Ship):
        if ship in self.all_ships:
            self.attackers = [None if s == ship else s for s in self.attackers]
            self.defenders = [None if s == ship else s for s in self.defenders]
            self.all_ships.remove(ship)

    @property
    def victor(self) -> str:
        if all(s is None for s in self.defenders):
            return "Attackers"
        elif all(s is None for s in self.attackers):
            return "Defenders"
        else:
            return ""
