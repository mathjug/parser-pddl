from custom_types import Proposition, Action, Predicate
from collections import deque

def store_initial_queue(initial_state: list[int], propositions: list[Proposition]):
    frontier_queue = deque([])
    for i in range(len(initial_state)):
        frontier_queue.appendleft((propositions[i], initial_state[i]))
    return frontier_queue

def run_ground(initial_state: list[int], propositions: list[Proposition],
                pred_to_actions: dict[Predicate, list[Action]]):
    frontier_queue = store_initial_queue(initial_state, propositions)
    reached = {}
    used_prop = [False for prop in propositions]
    
    while(len(frontier_queue) > 0):
        reached_tuple = frontier_queue.pop()
        reached_predicate = reached_tuple[0].get_predicate()
        if reached_predicate not in reached:
            reached[reached_predicate] = []
        reached[reached_predicate].append(reached_tuple)

        for action in pred_to_actions[reached_predicate]:
            # excluir as proposições nas pré-condições que são inválidas devido
            # à utilização da mesma variável que a proposição que acabou de ser
            # retirada da fronteira
            continue




        # quando entrar no frontier
        #used_prop[effects[i].get_index()] = True
        