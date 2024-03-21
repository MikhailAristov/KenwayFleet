import numpy as np
from numpy.random import choice
from ai.base import Targeter
from gameplay import BattleData


class RandomTargeter(Targeter):

    def get_next_target(self, battle: BattleData) -> int:
        return choice(Targeter.get_valid_targets(battle))


class WeightedRandomTargeter(Targeter):

    def get_next_target(self, battle: BattleData) -> int:
        targets = Targeter.get_valid_targets(battle)
        weights = np.array([1. / battle.ships[t].level for t in targets])
        return choice(targets, p=weights/sum(weights))
