from numpy.random import choice
from ai.base import BasicAI
from gameplay import BattleData


class RandomAI(BasicAI):

    def get_next_target(self, battle: BattleData) -> int:
        return choice(BasicAI.get_valid_targets(battle))
