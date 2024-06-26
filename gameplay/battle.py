from dataclasses import dataclass
from numpy.random import uniform as randf
from gameplay.ship import Ship, ShipData


@dataclass
class BattleData:
    ships: list[ShipData]
    active: int


class Battle:
    attackers: list[Ship] = [None, None, None]
    defenders: list[Ship] = [None, None, None]

    volley_count: int = 0
    winner: str = ""

    @property
    def all_ships(self) -> list[Ship]:
        return self.attackers + self.defenders

    def add_attacker(self, ship: Ship):
        ship.cooldown *= randf(.95, .999)
        for i in range(3):
            if self.attackers[i] is None:
                self.attackers[i] = ship
                return

    def add_defender(self, ship: Ship):
        ship.cooldown *= randf(.95, .999)
        for i in range(3):
            if self.defenders[i] is None:
                self.defenders[i] = ship
                return

    def print_state(self):
        print('~' * 64)
        for i in range(3):
            print(" {0:<31}{1:>31}".format(str(self.attackers[i]), str(self.defenders[i])))
        print('~' * 64)

    def proceed_to_next_volley(self, verbose: bool = False) -> BattleData:
        self.volley_count += 1
        if verbose:
            print("                            VOLLEY", self.volley_count)
        next_ship_id, steps = self.next_position_to_fire
        for s in [s for s in self.all_ships if s is not None]:
            s.cool(steps)
        if verbose:
            self.print_state()
        return BattleData([s.data if s else None for s in self.all_ships], next_ship_id)

    def fire_volley(self, attacker_id: int, target_id: int, verbose: bool = False):
        attacker = self.all_ships[attacker_id]
        target = self.all_ships[target_id]

        # inflict damage and reset cooldown
        if verbose:
            print(attacker, "fires at", target)
        attacker.fire(target)
        attacker.reset_cooldown()

        # check if the target is sunk
        if target.is_sunk:
            if target_id < 3:
                self.attackers[target_id] = None
            else:
                self.defenders[target_id - 3] = None
        if verbose:
            self.print_state()

        # check if either side has won
        if target.is_sunk and all(s is None for s in self.defenders):
            if verbose:
                print("The Attackers have won the battle!")
            self.winner = "ATK"
        elif target.is_sunk and all(s is None for s in self.attackers):
            if verbose:
                print("The Defenders have won the battle!")
            self.winner = "DEF"

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
