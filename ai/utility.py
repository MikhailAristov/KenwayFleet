from numpy.random import randint
from ai import Targeter
from gameplay import BattleData, Ship


class UtilityBasedTargeter(Targeter):

    def get_attacking_flotilla(self, ships: dict, defenders: list[Ship]) -> list[Ship]:
        lineups = Targeter.get_all_lineups(ships, sum([s.level for s in defenders]))
        return [Ship(t, ships[t]) for t in lineups[randint(len(lineups))]]

    def get_next_target(self, battle: BattleData) -> int:
        targets = Targeter.get_valid_targets(battle)

        # sort the targets by firepower (inverse)
        targets.sort(key=lambda i: 1. / battle.ships[i].fire)
        # see if I can sink any of them
        for t in targets:
            if battle.ships[t].hp <= battle.ships[battle.active].fire:
                return t

        # otherwise, fire at the ship with the least remaining HP
        return min(targets, key=lambda i: battle.ships[i].hp)
