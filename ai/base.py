from abc import ABC, abstractmethod
from typing import List
from gameplay import BattleData


class Targeter(ABC):

    @staticmethod
    def get_valid_targets(battle: BattleData) -> List[int]:
        side = [0, 1, 2] if battle.active >= 3 else [3, 4, 5]
        return [i for i in side if battle.ships[i] is not None]

    @abstractmethod
    def get_next_target(self, battle: BattleData) -> int:
        pass
