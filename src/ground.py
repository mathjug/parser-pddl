from custom_types import Proposition, Action
from collections import deque

def store_initial_queue(initial_state: list[int], propositions: list[Proposition]):
    frontier_queue = deque([])
    for i in range(len(initial_state)):
        if initial_state[i] == 1:
            frontier_queue.appendleft(propositions[i])
    return frontier_queue

def run_ground(initial_state: list[int], propositions: list[Proposition],
           actions: dict[str, Action]):
    frontier_queue = store_initial_queue(initial_state, propositions)
    reached = []
    
    while(len(frontier_queue) > 0):
        reached.append(frontier_queue.pop())
        