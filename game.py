import numpy as np
from itertools import combinations_with_replacement
from ai import *
from data import ships
from gameplay import Battle, Ship


def play(attacker: Targeter, defender: Targeter) -> str:
    # set up the battle with random ships
    battle = Battle()
    ship_types = list(ships.keys())
    for i in range(3):
        opp = np.random.choice(ship_types)
        battle.add_defender(Ship(opp, ships[opp]), i)
    defender_level: float = sum([s.level for s in battle.defenders])
    # examine possible lineups
    legal_lineups = []
    for lineup in combinations_with_replacement(ship_types, 3):
        if defender_level * .9 < sum([ships[s]['level'] for s in lineup]) < defender_level * 1.1:
            legal_lineups.append(lineup)
    # Pick a legal lineup at random
    final_lineup = legal_lineups[np.random.randint(len(legal_lineups))]
    for i in range(3):
        atk = str(final_lineup[i])
        battle.add_attacker(Ship(atk, ships[atk]), i)
    battle.print_state()

    # play out the battle until done
    while not battle.winner:
        # advance battle to the next volley
        data = battle.proceed_to_next_volley(verbose=True)
        # query the AI what to do next
        target = attacker.get_next_target(data) if data.active < 3 \
            else defender.get_next_target(data)
        # fire the volley
        battle.fire_volley(data.active, target, verbose=True)

    return battle.winner


if __name__ == '__main__':
    ATK = MinimaxTargeter(level=15)
    DEF = UtilityBasedTargeter()
    _ = play(ATK, DEF)
