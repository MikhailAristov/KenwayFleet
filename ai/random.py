import numpy as np
from numpy.random import choice
from ai import Targeter
from gameplay import BattleData


class RandomTargeter(Targeter):
    weighted_by: str

    weight_calc = {
        'none': lambda t, _: np.ones(len(t), dtype=float),
        'level_inv': lambda t, s: np.array([1. / s[i].level for i in t], dtype=float),
    }

    def __init__(self, weighted_by='none'):
        if weighted_by in self.weight_calc.keys():
            self.weighted_by = weighted_by

    def get_next_target(self, battle: BattleData) -> int:
        targets = Targeter.get_valid_targets(battle)
        weights = self.weight_calc[self.weighted_by](targets, battle.ships)
        return choice(targets, p=weights/sum(weights))
