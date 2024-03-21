from dataclasses import dataclass
from numpy.random import uniform as randf
from typing import List
from gameplay.ship import Ship, ShipData


@dataclass
class BattleData:
    ships: List[ShipData]
    active: int


class Battle:
    attackers: List[Ship] = [None, None, None]
    defenders: List[Ship] = [None, None, None]

    @property
    def all_ships(self) -> List[Ship]:
        return self.attackers + self.defenders

    def add_attacker(self, ship: Ship, pos: int):
        ship.cooldown *= randf(.95, .999)
        self.attackers[pos] = ship

    def add_defender(self, ship: Ship, pos: int):
        ship.cooldown *= randf(.95, .999)
        ship.hit_points *= randf(.85, 1.)
        self.defenders[pos] = ship

    def __str__(self) -> str:
        width = 64
        separator = '~' * width
        format_str: str = " {1:<" + str(width // 2) + "}{2:>" + str(width // 2) + "} "
        rows = [separator]
        for i in range(3):
            rows.append(format_str.format(i + 1, str(self.attackers[i]), str(self.defenders[i])))
        rows.append(separator)
        return '\r\n'.join(rows)

    @property
    def next_position_to_fire(self) -> (int, float):
        fastest = -1
        for i in range(6):
            if self.all_ships[i] is not None:
                if fastest < 0 or self.all_ships[i].remaining_steps < self.all_ships[fastest].remaining_steps:
                    fastest = i
        return fastest, self.all_ships[fastest].remaining_steps

    def wait_for_next_ship(self) -> Ship:
        next_ship_id, steps = self.next_position_to_fire
        result = self.all_ships[next_ship_id]
        for s in [s for s in self.all_ships if s is not None]:
            s.cool(steps)
        return result

    def remove_ship(self, ship: Ship):
        assert ship is not None
        for i in range(3):
            if self.attackers[i] == ship:
                self.attackers[i] = None
            elif self.defenders[i] == ship:
                self.defenders[i] = None

    @property
    def victor(self) -> str:
        if all(s is None for s in self.defenders):
            return "Attackers"
        elif all(s is None for s in self.attackers):
            return "Defenders"
        else:
            return ""

    @property
    def data(self) -> BattleData:
        active, _ = self.next_position_to_fire
        return BattleData([s.data if s else None for s in self.all_ships], active)

    def get_ship_at_position(self, pos: int) -> Ship:
        return self.all_ships[pos]
