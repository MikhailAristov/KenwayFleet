import copy

from ai.base import Targeter
from gameplay import BattleData, ShipData


class MinimaxTargeter(Targeter):

    def get_next_target(self, battle: BattleData) -> int:
        targets = Targeter.get_valid_targets(battle)



        result = targets[0]
        for t in targets:
            if battle.ships[t].level > battle.ships[result].level:
                result = t
        return result

    @staticmethod
    def simulate(state: BattleData, tgt: int) -> BattleData:
        # copy old state
        new_state = copy.deepcopy(state)
        # inflict damage
        new_state.ships[tgt].hp -= new_state.ships[new_state.active].fire
        # check for sinking
        if new_state.ships[tgt].hp <= 0.:
            new_state.ships[tgt] = None
        # reset the attackers cooldown
        new_state.ships[new_state.active].cooldown = 1.
        # compute time to the volley
        new_state.active = min(range(6),
                               key=lambda x: MinimaxTargeter.get_steps_in_cooldown(new_state.ships[x])
                               if new_state.ships[x] else 1000)
        steps = MinimaxTargeter.get_steps_in_cooldown(new_state.ships[new_state.active])
        # subtract the time elapsed from everyone's cooldown
        for s in new_state.ships:
            s.cooldown -= s.speed / 1000 * steps
        return new_state

    @staticmethod
    def get_steps_in_cooldown(ship: ShipData) -> float:
        return ship.cooldown * 1000 / ship.speed

    @staticmethod
    def evaluate(state: BattleData) -> float:
        return sum([state.ships[i].hp * (1. if i < 3 else -1.) for i in range(6) if state.ships[i]])
