from src import Proposition, Action, Predicate, Object
from collections import deque
from typing import Union
import itertools

def create_reached_list(initial_state: list[int]) -> list[int]:
    """ Creates the list of reached propositions at the initial state.
    
    Args:
        initial_state (list[int]): A bitmask representing the initial truth values of propositions (1 for true, 0 for false).

    Returns:
        list[int]: A list indicating whether a proposition is reached or not; for those reached, the value is 0; otherwise, value is -1.

    Note:
        Each proposition P has an index i; the i-th entry of the returned list correspond to the tuple (P, True), and the (n + i)-th entry to the tuple (P, False).
    """
    n = len(initial_state)
    reached = [-1 for _ in range(2 * n)]
    for i in range(n):
        if initial_state[i] == 0:
            reached[i + n] = 0
        elif initial_state[i] == 1:
            reached[i] = 0
    return reached

def store_initial_queue(initial_state: list[int], propositions: list[Proposition]) -> deque[tuple[Proposition, int]]:
    """
    
    Args:

    Returns:

    Note:
    """
    frontier_queue = deque([])
    for i in range(len(initial_state)):
        frontier_queue.appendleft((propositions[i], initial_state[i]))
    return frontier_queue

def get_element_from_frontier(frontier_queue: deque[tuple[Proposition, int]]) -> tuple[Proposition, int, int]:
    """
    
    Args:

    Returns:

    Note:
    """
    reached_tuple = frontier_queue.pop()
    proposition = reached_tuple[0]
    value = reached_tuple[1]
    index = proposition.get_index()
    return (proposition, value, index)

def add_proposition_to_reached(reached_list: list[int], proposition_value: int, 
                                proposition_index: int, num_propositions: int) -> None:
    """
    
    Args:

    Returns:

    Note:
    """
    if proposition_value == 0:
        reached_list[num_propositions + proposition_index] = 1
    else:
        reached_list[proposition_index] = 1

def find_reached_predicate_in_preconditions(preconditions: list[tuple[Proposition, int]], 
                                            predicate: Predicate, value: int) -> Union[tuple[Proposition, int], None]:
    """
    
    Args:

    Returns:

    Note:
    """
    for precondition in preconditions:
        if predicate == precondition[0].get_predicate() and value == precondition[1]:
            return precondition
    return None

def get_action_parameters_and_preconditions(action: Action) -> tuple[list[tuple[Proposition, bool]], list[Object]]:
    """
    
    Args:

    Returns:

    Note:
    """
    preconditions = action.get_preconditions()
    parameters = action.get_parameters()
    return (preconditions, parameters)

def get_parameters_combinations(parameters: list[Object], fixed_object: dict[Object, list[Object]], 
                                dict_objects: dict[str, list[Object]]) -> list[tuple[Object]]:
    """
    
    Args:

    Returns:

    Note:
    """
    parameters_list = []
    for object in parameters:
        if object in fixed_object:
            parameters_list.append([fixed_object[object]])
        else:
            parameters_list.append(dict_objects[object.get_type()])

    all_combinations = itertools.product(*parameters_list)
    unique_combinations = [tup for tup in all_combinations if len(tup) == len(set(tup))]
    return unique_combinations

def find_proposition(generic_proposition, object_combination, propositions, parameters):
    """
    
    Args:

    Returns:

    Note:
    """
    proposition_objects = []
    for object in generic_proposition.get_objects():
        for index, parameter in enumerate(parameters):
            if object == parameter:
                proposition_objects.append(object_combination[index])

    predicate = generic_proposition.get_predicate()
    name = predicate.get_name()
    for object in proposition_objects:
        name += "_" + object.get_name()
    proposition = propositions[name]
    return proposition

def enqueue_effects(frontier_queue: deque[tuple[Proposition, int]], action: Action, 
                    object_combination: tuple[Object], propositions: dict[str, Proposition], 
                    parameters: list[Object], reached: list[int]) -> None:
    """
    
    Args:

    Returns:

    Note:
    """
    for effect_scenario in action.get_effects():
        for effect_generic_proposition, effect_value in effect_scenario:
            proposition = find_proposition(effect_generic_proposition, object_combination, propositions, parameters)
            index = proposition.get_index()

            num_propositions = len(reached) // 2
            if not effect_value:
                index += num_propositions

            if reached[index] == -1:
                reached[index] = 0 
                frontier_queue.appendleft((proposition, effect_value))

def run_ground(initial_state: list[int], list_propositions: list[Proposition], 
                dict_propositions: dict[str, Proposition],
                pred_to_actions: dict[Predicate, list[Action]],
                dict_objects: dict[str, list[Object]]) -> list[tuple[Action, tuple[Object]]]:
    """
    
    Args:

    Returns:

    Note:
    """
    frontier_queue = store_initial_queue(initial_state, list_propositions)
    reached = create_reached_list(initial_state)
    actions = []
    num_propositions = len(initial_state)

    while(len(frontier_queue) > 0):
        reached_proposition, value, index = get_element_from_frontier(frontier_queue)
        add_proposition_to_reached(reached, value, index, num_propositions)
        reached_predicate = reached_proposition.get_predicate()

        for action in pred_to_actions[reached_predicate]:
            preconditions, parameters = get_action_parameters_and_preconditions(action)

            reached_precondition = find_reached_predicate_in_preconditions(preconditions,
                                                                           reached_predicate,
                                                                           value)
            if reached_precondition is None:
                continue
            reached_precondition_proposition, _ = reached_precondition
            
            fixed = {}
            for i, object in enumerate(reached_precondition_proposition.get_objects()):
                fixed[object] = reached_proposition.get_objects()[i]

            parameters_combinations = get_parameters_combinations(parameters, fixed, dict_objects)

            for object_combination in parameters_combinations:
                all_propositions_reachable = True
                for precondition in preconditions:
                    generic_precondition_proposition, precondition_value = precondition
                    builded_precondition_proposition = find_proposition(generic_precondition_proposition, object_combination,
                                                                    dict_propositions, parameters)
                    builded_precondition_proposition_index = builded_precondition_proposition.get_index()
                    if not precondition_value:
                        builded_precondition_proposition_index += num_propositions
                        
                    if reached[builded_precondition_proposition_index] != 1:
                        all_propositions_reachable = False
                        break
                    
                if all_propositions_reachable == True:
                    enqueue_effects(frontier_queue, action, object_combination, dict_propositions, parameters, reached)
                    actions.append((action, object_combination))

    return (actions, reached)