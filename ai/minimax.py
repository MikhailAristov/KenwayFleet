from copy import deepcopy
from ai import Targeter
from gameplay import BattleData, ShipData


class MinimaxTargeter(Targeter):
    sup_score: float
    inf_score: float
    level: int

    def __init__(self, **kwargs):
        self.level = kwargs['level'] if 'level' in kwargs else 6

    def get_next_target(self, battle: BattleData) -> int:
        self.sup_score = sum([s.hp for s in battle.ships[0:3] if s is not None])
        self.inf_score = -sum([s.hp for s in battle.ships[3:6] if s is not None])
        _, result = self.minimax(battle, self.level, self.inf_score, self.sup_score)
        return result

    def minimax(self, state: BattleData, depth: int, alpha: float, beta: float) -> (float, int):
        if depth < 1 or MinimaxTargeter.is_over(state):
            return MinimaxTargeter.evaluate(state) + (1 - 2 * MinimaxTargeter.get_winner(state)) * depth, -1

        best_move = -1
        if state.active < 3:  # maximizing player
            max_score: float = self.inf_score
            for tgt in Targeter.get_valid_targets(state):
                score, _ = self.minimax(MinimaxTargeter.simulate(state, tgt), depth - 1, alpha, beta)
                if score > max_score:
                    best_move = tgt
                    max_score = score
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            return max_score, best_move
        else:  # minimizing player
            min_score: float = self.sup_score
            for tgt in Targeter.get_valid_targets(state):
                score, _ = self.minimax(MinimaxTargeter.simulate(state, tgt), depth - 1, alpha, beta)
                if score < min_score:
                    best_move = tgt
                    min_score = score
                beta = min(beta, score)
                if beta <= alpha:
                    break
            return min_score, best_move

    @staticmethod
    def is_over(state: BattleData):
        return all([s is None for s in state.ships[0:3]]) or all([s is None for s in state.ships[3:6]])

    @staticmethod
    def get_winner(state: BattleData):  # 0 = attacker, 1 = defender
        return 1 if all([s is None for s in state.ships[0:3]]) else 0

    @staticmethod
    def simulate(state: BattleData, tgt: int) -> BattleData:
        # copy old state
        new_state = deepcopy(state)
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
            if s is not None:
                s.cooldown -= s.speed / 1000 * steps
        return new_state

    @staticmethod
    def get_steps_in_cooldown(ship: ShipData) -> float:
        return ship.cooldown * 1000 / ship.speed

    @staticmethod
    def evaluate(state: BattleData) -> float:
        return sum([state.ships[i].hp * (1. if i < 3 else -1.) for i in range(6) if state.ships[i]])
