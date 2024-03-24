from copy import deepcopy

from ai import Targeter
from gameplay import BattleData, ShipData, Ship


class MinimaxTargeter(Targeter):
    sup_score: float
    inf_score: float
    level: int

    def __init__(self, **kwargs):
        self.level = kwargs['level'] if 'level' in kwargs else 6

    def get_attacking_flotilla(self, ships: dict, defenders: list[Ship]) -> list[Ship]:
        lineups = Targeter.get_all_lineups(ships, sum([s.level for s in defenders]))

        base_state = BattleData([None, None, None] + [s.data for s in defenders], -1)

        best_lineup: tuple[str] = lineups[0]
        best_eval = -1000
        for lineup in lineups:
            state = deepcopy(base_state)
            # set attacking ships
            for i in range(3):
                t: dict = ships[lineup[i]]
                state.ships[i] = ShipData(t['level'], t['speed'], t['fire'], t['maxhp'], 1.)
            # simulate to first volley
            MinimaxTargeter.simulate_to_next_volley(state)
            # evaluate the performance of the lineup
            self.set_inf_and_sup_scores(state)
            val, _ = self.minimax(state, self.level, self.inf_score, self.sup_score)
            # print(lineup, val)
            if val > best_eval:
                best_lineup = lineup
                best_eval = val

        return [Ship(a, ships[a]) for a in best_lineup]

    def get_next_target(self, battle: BattleData) -> int:
        self.set_inf_and_sup_scores(battle)
        _, result = self.minimax(battle, self.level, self.inf_score, self.sup_score)
        return result

    def set_inf_and_sup_scores(self, battle: BattleData):
        self.sup_score = sum([s.hp for s in battle.ships[0:3] if s is not None])
        self.inf_score = -sum([s.hp for s in battle.ships[3:6] if s is not None])

    def minimax(self, state: BattleData, depth: int, alpha: float, beta: float) -> (float, int):
        if depth < 1 or MinimaxTargeter.is_over(state):
            return MinimaxTargeter.evaluate(state) + depth * MinimaxTargeter.get_winner(state), -1

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
    def get_winner(state: BattleData):  # 1 = attacker, -1 = defender, 0 = none yet
        if all([s is None for s in state.ships[0:3]]):
            return 1
        elif all([s is None for s in state.ships[3:6]]):
            return -1
        else:
            return 0

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
        MinimaxTargeter.simulate_to_next_volley(new_state)
        return new_state

    @staticmethod
    def simulate_to_next_volley(state: BattleData):
        state.active = min(range(6),
                           key=lambda x: MinimaxTargeter.get_steps_in_cooldown(state.ships[x])
                           if state.ships[x] else 1000)
        steps = MinimaxTargeter.get_steps_in_cooldown(state.ships[state.active])
        # subtract the time elapsed from everyone's cooldown
        for s in state.ships:
            if s is not None:
                s.cooldown -= s.speed / 1000 * steps

    @staticmethod
    def get_steps_in_cooldown(ship: ShipData) -> float:
        return ship.cooldown * 1000 / ship.speed

    @staticmethod
    def evaluate(state: BattleData) -> float:
        return sum([state.ships[i].hp * (1. if i < 3 else -1.) for i in range(6) if state.ships[i]])
