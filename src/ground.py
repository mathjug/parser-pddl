from custom_types import Proposition, Action, Predicate
from collections import deque

def store_initial_queue(initial_state: list[int], propositions: list[Proposition]):
    frontier_queue = deque([])
    for i in range(len(initial_state)):
        frontier_queue.appendleft((propositions[i], initial_state[i]))
    return frontier_queue

def run_ground(initial_state: list[int], propositions: dict[str, Proposition],
                pred_to_actions: dict[Predicate, list[Action]]):
    frontier_queue = store_initial_queue(initial_state, propositions)

    n = len(initial_state)
    reached = [-1 for _ in range(2 * n)]
    for i in range(n):
        if initial_state[i] == 0:
            reached[i + n] = 0
        elif initial_state[i] == 1:
            reached[i] = 0

    while(len(frontier_queue) > 0):
        reached_tuple = frontier_queue.pop()
        reached_proposition = reached_tuple[0]
        value = reached_tuple[1]

        index = reached_proposition.get_index()
        if value == 0:
            reached[n + index] = 1
        else:
            reached[index] = 1

        reached_predicate = reached_proposition.get_predicate()
        for action in pred_to_actions[reached_predicate]:
            preconditions = action.get_precondition()
            for precondition in preconditions:
                precondition_predicate = precondition[0].get_predicate()
                precondition_value = precondition[1]
                if precondition_predicate == reached_predicate \
                                and precondition_value == value:
                    continue
        # quando entrar no frontier
        #used_prop[effects[i].get_index()] = True
