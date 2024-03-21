from ai.base import Targeter
from gameplay import BattleData


class LevelBasedTargeter(Targeter):

    def get_next_target(self, battle: BattleData) -> int:
        targets = Targeter.get_valid_targets(battle)
        result = targets[0]
        for t in targets:
            if battle.ships[t].level > battle.ships[result].level:
                result = t
        return result


class OpportunisticTargeter(Targeter):

    def get_next_target(self, battle: BattleData) -> int:
        targets = Targeter.get_valid_targets(battle)
        result = targets[0]
        for t in targets:
            if 1. / battle.ships[t].hp > 1. / battle.ships[result].hp:
                result = t
        return result


class FirepowerBasedTargeter(Targeter):

    def get_next_target(self, battle: BattleData) -> int:
        targets = Targeter.get_valid_targets(battle)
        result = targets[0]
        for t in targets:
            if battle.ships[t].fire > battle.ships[result].fire:
                result = t
        return result


class UtilityBasedTargeter(Targeter):

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
