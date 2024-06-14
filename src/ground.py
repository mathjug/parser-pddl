from custom_types import Proposition, Action
from collections import deque

def store_initial_queue(initial_state: list[int], propositions: list[Proposition]):
    frontier_queue = deque([])
    for i in range(len(initial_state)):
        frontier_queue.appendleft((propositions[i], initial_state[i]))
    return frontier_queue

def run_ground(initial_state: list[int], propositions: list[Proposition],
                actions: dict[str, Action]):
    frontier_queue = store_initial_queue(initial_state, propositions)
    reached = {}
    
    while(len(frontier_queue) > 0):
        reached_tuple = frontier_queue.pop()
        reached_predicate = reached_tuple[0].get_predicate()
        if reached_predicate not in reached:
            reached[reached_predicate] = []
        reached[reached_predicate].append(reached_tuple)
        