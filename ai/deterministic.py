from ai import Targeter
from gameplay import BattleData


class DeterministicTargeter(Targeter):
    attribute: str

    selectors = {
        'max_level': lambda t, s: max(t, key=lambda i: s[i].level),
        'max_fire': lambda t, s: max(t, key=lambda i: s[i].fire),
        'min_hp': lambda t, s: min(t, key=lambda i: s[i].hp),
    }

    def __init__(self, attribute = 'max_level'):
        if attribute in self.selectors.keys():
            self.attribute = attribute

    def get_next_target(self, battle: BattleData) -> int:
        targets = Targeter.get_valid_targets(battle)
        return self.selectors[self.attribute](targets, battle.ships)
