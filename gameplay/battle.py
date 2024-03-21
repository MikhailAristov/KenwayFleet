from dataclasses import dataclass
from numpy.random import uniform as randf
from typing import List
from gameplay.ship import Ship, ShipData


@dataclass
class BattleData:
    attacker1: ShipData
    attacker2: ShipData
    attacker3: ShipData
    defender1: ShipData
    defender2: ShipData
    defender3: ShipData
    active: int


class Battle:
    attackers: List[Ship] = [None, None, None]
    defenders: List[Ship] = [None, None, None]

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
        format_str: str = " A{0:d}. {1:<" + str(width // 2 - 5) + "}{2:>" + str(width // 2 - 5) + "} D{0:d}."
        rows = [separator]
        for i in range(3):
            rows.append(format_str.format(i + 1, str(self.attackers[i]), str(self.defenders[i])))
        rows.append(separator)
        return '\r\n'.join(rows)

    @property
    def next_position_to_fire(self) -> (int, float):
        all_ships: List[Ship] = self.attackers + self.defenders
        fastest = -1
        for i in range(len(all_ships)):
            if all_ships[i] is not None:
                if fastest < 0 or all_ships[i].remaining_steps < all_ships[fastest].remaining_steps:
                    fastest = i
        return fastest, all_ships[fastest].remaining_steps

    def wait_for_next_ship(self) -> Ship:
        next_ship_id, steps = self.next_position_to_fire
        result = (self.attackers + self.defenders)[next_ship_id]
        for s in [s for s in (self.attackers + self.defenders) if s is not None]:
            s.cool(steps)
        return result

    def get_valid_targets(self, for_ship: Ship) -> List[Ship]:
        assert for_ship is not None
        if for_ship in self.attackers:
            return [s for s in self.defenders if s is not None and not s.is_sunk]
        elif for_ship in self.defenders:
            return [s for s in self.attackers if s is not None and not s.is_sunk]
        raise "Invalid ship!"

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
        return BattleData(Ship.get_data(self.attackers[0]), Ship.get_data(self.attackers[1]),
                          Ship.get_data(self.attackers[2]), Ship.get_data(self.defenders[0]),
                          Ship.get_data(self.defenders[1]), Ship.get_data(self.defenders[2]), active)
