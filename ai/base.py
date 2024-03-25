from abc import ABC, abstractmethod
from itertools import combinations_with_replacement
from gameplay import BattleData, Ship


class Targeter(ABC):

    @abstractmethod
    def get_attacking_flotilla(self, ships: dict, defenders: list[Ship]) -> list[Ship]:
        pass

    @abstractmethod
    def get_next_target(self, battle: BattleData) -> int:
        pass

    @staticmethod
    def get_all_lineups(ships: dict, total_level: float) -> list[tuple[str]]:
        result: list[tuple[str]] = []
        lineup: tuple[str]
        for lineup in combinations_with_replacement(ships.keys(), 3):
            if total_level * .9 <= sum([ships[s]['level'] for s in lineup]) <= total_level * 1.1:
                result.append(lineup)
        return result

    @staticmethod
    def get_valid_targets(battle: BattleData) -> list[int]:
        side = [0, 1, 2] if battle.active >= 3 else [3, 4, 5]
        return [i for i in side if battle.ships[i] is not None]
