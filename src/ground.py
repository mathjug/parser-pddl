from src import Proposition, Action, Predicate, Object
from collections import deque
import itertools

def create_reached_list(initial_state):
    n = len(initial_state)
    reached = [-1 for _ in range(2 * n)]
    for i in range(n):
        if initial_state[i] == 0:
            reached[i + n] = 0
        elif initial_state[i] == 1:
            reached[i] = 0
    return reached

def store_initial_queue(initial_state: list[int], propositions: list[Proposition]):
    frontier_queue = deque([])
    for i in range(len(initial_state)):
        frontier_queue.appendleft((propositions[i], initial_state[i]))
    return frontier_queue

def get_element_from_frontier(frontier_queue):
    reached_tuple = frontier_queue.pop()
    proposition = reached_tuple[0]
    value = reached_tuple[1]
    index = proposition.get_index()
    return (proposition, value, index)

def add_proposition_to_reached(reached_list, proposition_value, proposition_index,
                               num_propositions):
    if proposition_value == 0:
        reached_list[num_propositions + proposition_index] = 1
    else:
        reached_list[proposition_index] = 1

def find_reached_predicate_in_preconditions(preconditions, predicate, value):
    for precondition in preconditions:
        if predicate == precondition[0].get_predicate() and value == precondition[1]:
            return precondition
    return None

def get_action_parameters_and_preconditions(action):
    preconditions = action.get_preconditions()
    parameters = action.get_parameters()
    return (preconditions, parameters)

def get_parameters_combinations(parameters, fixed_object, dict_objects) -> list[tuple[Object]]:
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

def enqueue_effects(frontier_queue, action, object_combination, propositions, parameters, reached):
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
                dict_objects: dict[str, list[Object]]):
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

    return actions
