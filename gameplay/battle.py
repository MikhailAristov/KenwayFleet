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

    volley_count: int = 1
    finished: bool = False

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

    def print_state(self):
        print('~' * 64)
        for i in range(3):
            print(" {1:<31}{2:>31}".format(i + 1, str(self.attackers[i]), str(self.defenders[i])))
        print('~' * 64)

    def proceed_to_next_volley(self) -> BattleData:
        print("                            VOLLEY", self.volley_count)
        next_ship_id, steps = self.next_position_to_fire
        for s in [s for s in self.all_ships if s is not None]:
            s.cool(steps)
        self.print_state()
        return BattleData([s.data if s else None for s in self.all_ships], next_ship_id)

    def fire_volley(self, attacker_id: int, target_id: int):
        attacker = self.all_ships[attacker_id]
        target = self.all_ships[target_id]

        # inflict damage and reset cooldown
        attacker.fire(target)
        attacker.reset_cooldown()

        # check if the target is sunk
        if target.is_sunk:
            if target_id < 3:
                self.attackers[target_id] = None
            else:
                self.defenders[target_id - 3] = None
        self.print_state()

        # check if either side has won
        if target.is_sunk and all(s is None for s in self.defenders):
            print("The Attackers have won the battle!")
            self.finished = True
        elif target.is_sunk and all(s is None for s in self.attackers):
            print("The Defenders have won the battle!")
            self.finished = True

        self.volley_count += 1

    @property
    def next_position_to_fire(self) -> (int, float):
        fastest = -1
        for i in range(6):
            if self.all_ships[i] is not None:
                if fastest < 0 or self.all_ships[i].remaining_steps < self.all_ships[fastest].remaining_steps:
                    fastest = i
        return fastest, self.all_ships[fastest].remaining_steps

    @property
    def data(self) -> BattleData:
        active, _ = self.next_position_to_fire
        return BattleData([s.data if s else None for s in self.all_ships], active)
