from .custom_types import Proposition, Action, Predicate, Object
from collections import deque
from typing import Union
import itertools

def create_reached_list(initial_state: list[int]) -> list[int]:
    """Creates the list of reached propositions at the initial state.

    Args:
        initial_state (list[int]): The bitmask representing the initial truth values of propositions (1 for true, 0 for false).

    Returns:
        list[int]: The list indicating whether a proposition is reached or not; for those reached, the value is 0; otherwise, value is -1.

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
    """Enqueue the pairs composed by the propositions and their respective truth values at the initial state.

    Args:
        initial_state (list[int]): The bitmask representing the initial truth values of propositions (1 for true, 0 for false).
        propositions (list[Proposition]): The list of all possible propositions in the domain.

    Returns:
        deque[tuple[Proposition, int]]: A queue with the tuples corresponding to the initial state.
    """
    frontier_queue = deque([])
    for i in range(len(initial_state)):
        frontier_queue.appendleft((propositions[i], initial_state[i]))
    return frontier_queue

def get_element_from_frontier(frontier_queue: deque[tuple[Proposition, int]]) -> tuple[Proposition, int, int]:
    """Pops and returns the front element from the frontier queue along with its proposition's index.

    Args:
        frontier_queue (deque[tuple[Proposition, int]]): A queue of (proposition, truth value) pairs representing propositions at the frontier. A proposition reaches the frontier if it lies in the effects list of a reachable action (see definition elsewhere).

    Returns:
        tuple[Proposition, int, int]: A tuple containing:
            - The popped proposition
            - Its corresponding truth value (1 for true, 0 for false)
            - The index associated with the proposition
    """
    reached_tuple = frontier_queue.pop()
    proposition = reached_tuple[0]
    value = reached_tuple[1]
    index = proposition.get_index()
    return (proposition, value, index)

def add_proposition_to_reached(reached_list: list[int], proposition_value: int,
                                proposition_index: int, num_propositions: int) -> None:
    """Assigns value 1 to the entry of the list of reached (valued) propositions corresponding to the valued proposition.

    Args:
        reached_list (list[int]): The list reached propositions.
        proposition_value (int): The truth value of the proposition (1 for true, 0 for false).
        proposition_index (int): The index corresponding to the proposition.
        num_propositions (int): The total number of propositions.

    Note:
        If a proposition P has an index i, the i-th entry of the returned list correspond to the tuple (P, True), and the (n + i)-th entry to the tuple (P, False).
    """
    if proposition_value == 0:
        reached_list[num_propositions + proposition_index] = 1
    else:
        reached_list[proposition_index] = 1

def find_reached_predicate_in_preconditions(preconditions: list[tuple[Proposition, int]],
                                            predicate: Predicate, value: int) -> Union[tuple[Proposition, int], None]:
    """Among all the preconditions of an action, finds the one (if one exists) that has a proposition whose predicate is the desired one.

    Args:
        preconditions (list[tuple[Proposition, int]]): The list of preconditions of an action.
        predicate (Predicate): The predicate we're looking for in the propositions of the preconditions.
        value (int): The truth value of the proposition (1 for true, 0 for false).

    Returns:
        Union[tuple[Proposition, int], None]: returns the matching precondition, or None if not found.
    """
    for precondition in preconditions:
        if predicate == precondition[0].get_predicate() and value == precondition[1]:
            return precondition
    return None

def get_action_parameters_and_preconditions(action: Action) -> tuple[list[tuple[Proposition, bool]], list[Object]]:
    """Retrieves the preconditions and parameters of an action.

    Args:
        action (Action): The action object.

    Returns:
        tuple[list[tuple[Proposition, bool]], list[Object]]: A tuple containing:
            - A list of preconditions, where each precondition is a tuple of a Proposition and its truth value (True or False).
            - A list of objects representing the parameters required for the action.
    """
    preconditions = action.get_preconditions()
    parameters = action.get_parameters()
    return (preconditions, parameters)

def get_parameters_combinations(parameters: list[Object], fixed_object: dict[Object, list[Object]],
                                dict_objects: dict[str, list[Object]]) -> list[tuple[Object]]:
    """Generates all unique combinations of objects that can be assigned to a set of parameters.

    Args:
        parameters (list[Object]): A list of parameter objects for which combinations need to be generated.
        fixed_object (dict[Object, list[Object]]): A dictionary mapping parameter objects to their fixed values. If a parameter is not in this dictionary, it is considered variable.
        dict_objects (dict[str, list[Object]]): A dictionary mapping object types (as strings) to lists of objects of that type.

    Returns:
        list[tuple[Object]]: A list of tuples, where each tuple represents a unique combination of objects that can be assigned to the parameters.
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

def find_proposition(generic_proposition: Proposition, object_combination: tuple[Object],
                     propositions: dict[str, Proposition], parameters: list[Object]) -> Proposition:
    """Finds a specific proposition within a dictionary given a generic proposition and an object combination.

    Args:
        generic_proposition (Proposition): The generic proposition (template) to match.
        object_combination (tuple[Object]): The objects to substitute into the generic proposition.
        propositions (dict[str, Proposition]): A dictionary mapping proposition names to Proposition objects.
        parameters (list[Object]): The list of parameters (objects) used in the propositions.

    Returns:
        Proposition: The matching proposition from the dictionary, or None if not found.
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
    """Enqueues propositions and their respective truth values onto a frontier queue based on an action's effects.

    Args:
        frontier_queue (deque[tuple[Proposition, int]]): A queue of (proposition, truth value) pairs representing propositions at the frontier.
        action (Action): The action whose effects are being processed.
        object_combination (tuple[Object]): The combination of objects for which the action's effects are being evaluated.
        propositions (dict[str, Proposition]): A dictionary mapping proposition names to Proposition objects.
        parameters (list[Object]): The list of parameters (objects) of the action.
        reached (list[int]): A list indicating which propositions have already been reached.

    Note:
        The function updates the 'reached' list to mark new propositions as reached, and appends the corresponding (proposition, truth value) pairs to the 'frontier_queue'.
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
                dict_objects: dict[str, list[Object]]) -> tuple[list[tuple[Action, tuple[Object]]], list[int]]:
    """Given an initial state, computes the list of reachable actions, along with the list of reachable propositions.

    Args:
        initial_state (list[int]): The initial state represented as a bitmask (1 for true, 0 for false) for each proposition.
        list_propositions (list[Proposition]): The list of all propositions in the domain.
        dict_propositions (dict[str, Proposition]): A dictionary mapping proposition names to Proposition objects.
        pred_to_actions (dict[Predicate, list[Action]]): A dictionary mapping predicates to lists of actions that have those predicates in their preconditions.
        dict_objects (dict[str, list[Object]]): A dictionary mapping object types (as strings) to lists of objects of that type.

    Returns:
        tuple[list[tuple[Action, tuple[Object]]], list[int]]: A tuple containing:
            - A list of tuples where each tuple represents a reachable action and its corresponding object combination.
            - A list indicating whether each proposition (and its negation) is reachable (1) or not (-1).

    Note:
        The algorithm iteratively explores the state space by adding reached propositions to a frontier queue.
        It checks if actions' preconditions are satisfied by the reached propositions and their combinations.
        If so, the action's effects are enqueued, expanding the frontier.
        The process continues until all reachable propositions and actions are found.
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