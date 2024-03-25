from time import perf_counter
from ai import Targeter
from gameplay import BattleData, ShipData, Ship


class MinimaxTargeter(Targeter):
    sup_score: float
    inf_score: float
    level: int

    target_calls: int = 0
    target_call_time: float = 0

    state_cache: list[BattleData] = []
    ship_cache: list[ShipData] = []

    def __init__(self, **kwargs):
        self.level = int(kwargs['level']) if 'level' in kwargs else 6
        self.eval_ship = kwargs['eval_ship'] if 'eval_ship' in kwargs else lambda s: s.hp * s.fire * s.speed

    def get_attacking_flotilla(self, ships: dict, defenders: list[Ship]) -> list[Ship]:
        print("Evaluating starting lineups...")
        lineups = Targeter.get_all_lineups(ships, sum([s.level for s in defenders]))
        count = len(lineups)

        base_state = BattleData([None, None, None] + [s.data for s in defenders], -1)

        best_lineup: tuple[str] = lineups[0]
        best_eval = -1e6
        for j in range(count):
            # display progress
            print("\r|{0:<62}|".format("~" * int(62. * (j + 1) / count)), end='' if j < count - 1 else "\n")
            # create a new state
            lineup = lineups[j]
            state = self.duplicate_battle(base_state)
            # set attacking ships
            for i in range(3):
                state.ships[i] = self.get_ship_data(ships[lineup[i]])
            # simulate to first volley
            MinimaxTargeter.simulate_to_next_volley(state)
            # evaluate the performance of the lineup
            self.set_inf_and_sup_scores(state)
            val, _ = self.minimax(state, self.level, self.inf_score, self.sup_score)
            # print(lineup, val)
            if val > best_eval:
                best_lineup = lineup
                best_eval = val
            self.state_cache.append(state)

        print("Chosen attacker lineup:", best_lineup)
        return [Ship(a, ships[a]) for a in best_lineup]

    def get_next_target(self, battle: BattleData) -> int:
        self.set_inf_and_sup_scores(battle)
        start_time: float = perf_counter()
        _, result = self.minimax(battle, self.level, self.inf_score, self.sup_score)
        self.target_call_time += perf_counter() - start_time
        self.target_calls += 1
        assert result >= 0
        return result

    def set_inf_and_sup_scores(self, battle: BattleData):
        self.sup_score = sum([self.eval_ship(s) for s in battle.ships[0:3] if s is not None])
        self.inf_score = -sum([self.eval_ship(s) for s in battle.ships[3:6] if s is not None])

    def minimax(self, state: BattleData, depth: int, alpha: float, beta: float) -> (float, int):
        if depth < 1 or MinimaxTargeter.get_winner(state) != 0:
            return self.evaluate(state) + depth * MinimaxTargeter.get_winner(state), 7

        best_move = 7
        valid_targets: list[int] = Targeter.get_valid_targets(state)
        if state.active < 3:  # maximizing player
            max_score: float = self.inf_score
            for tgt in valid_targets:
                next_state = self.simulate(state, tgt)
                score, _ = self.minimax(next_state, depth - 1, alpha, beta)
                if score > max_score:
                    best_move = tgt
                    max_score = score
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
                self.state_cache.append(next_state)
            return max_score, best_move
        else:  # minimizing player
            min_score: float = self.sup_score
            for tgt in valid_targets:
                next_state = self.simulate(state, tgt)
                score, _ = self.minimax(next_state, depth - 1, alpha, beta)
                if score < min_score:
                    best_move = tgt
                    min_score = score
                beta = min(beta, score)
                if beta <= alpha:
                    break
                self.state_cache.append(next_state)
            return min_score, best_move

    @staticmethod
    def get_winner(state: BattleData) -> int:  # 1 = attacker, -1 = defender, 0 = none yet
        return all([s is None for s in state.ships[3:6]]) - all([s is None for s in state.ships[0:3]])

    def simulate(self, state: BattleData, tgt: int) -> BattleData:
        # copy old state
        new_state = self.duplicate_battle(state)
        # inflict damage
        new_state.ships[tgt].hp -= new_state.ships[new_state.active].fire
        # check for sinking
        if new_state.ships[tgt].hp <= 0.:
            self.ship_cache.append(new_state.ships[tgt])
            new_state.ships[tgt] = None
        # reset the attackers cooldown
        new_state.ships[new_state.active].cooldown = 1.
        # compute time to the volley
        MinimaxTargeter.simulate_to_next_volley(new_state)
        return new_state

    def duplicate_battle(self, state: BattleData) -> BattleData:
        if not len(self.state_cache):
            return BattleData([None if s is None else self.duplicate_ship(s) for s in state.ships], state.active)
        else:
            result = self.state_cache.pop()
            result.active = state.active
            for i in range(6):
                if result.ships[i] is None:
                    if state.ships[i] is not None:
                        result.ships[i] = self.duplicate_ship(state.ships[i])
                else:
                    if state.ships[i] is not None:
                        result.ships[i].copy_values(state.ships[i])
                    else:
                        self.ship_cache.append(result.ships[i])
                        result.ships[i] = None
            return result

    def duplicate_ship(self, ship: ShipData) -> ShipData:
        if len(self.ship_cache):
            result = self.ship_cache.pop()
            result.copy_values(ship)
            return result
        else:
            return ShipData(ship.level, ship.speed, ship.fire, ship.hp, ship.cooldown)

    def get_ship_data(self, raw: dict) -> ShipData:
        if len(self.ship_cache):
            result = self.ship_cache.pop()
            result.level = raw['level']
            result.speed = raw['speed']
            result.fire = raw['fire']
            result.hp = raw['maxhp']
            result.cooldown = 1.
            return result
        else:
            return ShipData(raw['level'], raw['speed'], raw['fire'], raw['maxhp'], 1.)

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

    def evaluate(self, state: BattleData) -> float:
        return sum([self.eval_ship(state.ships[i]) * (1. if i < 3 else -1.)
                    for i in range(6) if state.ships[i]])
