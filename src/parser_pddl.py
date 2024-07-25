from pddl import parse_domain, parse_problem
from .custom_types import Action, Object, Proposition, Predicate
from .domain import Domain
from .problem import Problem
from .ground import run_ground, find_proposition
from typing import TextIO
import itertools

class Parser:
    """Represents the Parser, the central unit for domain and problem analysis.

    Attributes:
        domain (Domain): The parsed representation of the planning domain.
        problem (Problem): The parsed representation of the specific planning problem.
        actions (list[Action]): The list of actions defined in the domain.
        objects (dict[str, list[Object]]): A dictionary mapping object types (str) to lists of corresponding objects.
        propositions (list[Proposition]): The list of all possible propositions in the domain.
        dict_propositions (dict[str, Proposition]): A dictionary mapping proposition names (str) to Proposition objects.
        initial_state (list[int]): The bitmask representing the initial truth values of propositions (1 for true, 0 for false).
        goal_state (list[int]): The bitmask representing the goal truth values of propositions (1 for true, 0 for false, -1 for don't care).

    Examples:
        >>> parser1 = Parser("tests/examples/gripper3.pddl", "tests/examples/gripper3_3_balls.pddl")
        >>> parser2 = Parser("tests/examples/triangle-tire.pddl", "tests/examples/triangle-tire-1.pddl")
    """

    def __init__(self, domain_path: str, problem_path: str) -> None:
        """Initializes the 'Parser' object by parsing PDDL domain and problem files.

        Args:
            domain_path (str): The file path to the PDDL domain definition.
            problem_path (str): The file path to the PDDL problem definition.

        Note:
            The initialization process assumes a valid and coherent relationship between the problem and domain definitions.
        """
        parsed_problem = parse_problem(problem_path)
        parsed_domain = parse_domain(domain_path)
        self.problem = Problem(parsed_problem)
        self.domain = Domain(parsed_domain)
        self.__store_basic_elements(parsed_problem)
        self.actions = self.domain.get_actions()
        self.reachable_actions, self.reachable_propositions = self.__instantiate_reachable_actions()

    def __print_problem_name(self, output_file: TextIO) -> None:
        """Writes the problem name, enclosed in 'begin_problem_name' and 'end_problem_name' tags, to the specified output stream.

        Args:
            output_file (TextIO): The text stream where the formatted problem name should be written.
        """
        output_file.write("begin_problem_name\n")
        output_file.write(self.problem.get_name() + "\n")
        output_file.write("end_problem_name\n")

    def __print_propositions(self, output_file: TextIO) -> None:
        """Writes propositions and their indices, enclosed in 'begin_propositions' and 'end_propositions' tags, to the specified output stream.

        Args:
            output_file (TextIO): The text stream where the formatted propositions should be written.
        """
        output_file.write("begin_propositions\n")
        output_file.write(str(len(self.propositions)) + "\n")
        for i, proposition in enumerate(self.propositions):
            output_file.write(str(proposition) + " " + str(i) + "\n")
        output_file.write("end_propositions\n")

    def __print_initial_state(self, output_file: TextIO) -> None:
        """Writes the initial state, enclosed in 'begin_initial_state' and 'end_initial_state' tags, to the specified output stream.

        Args:
            output_file (TextIO): The text stream where the formatted initial state should be written.
        """
        output_file.write("begin_initial_state\n")
        output_file.write(str(len(self.initial_state)) + "\n")
        for i, proposition in enumerate(self.initial_state):
            output_file.write(str(i) + " " + str(proposition) + "\n")
        output_file.write("end_initial_state\n")

    def __print_goal_state(self, output_file: TextIO) -> None:
        """Writes the goal state, enclosed in 'begin_goal_state' and 'end_goal_state' tags, to the specified output stream.

        Args:
            output_file (TextIO): The text stream (file or similar) where the formatted goal state should be written.

        Note:
            Propositions with an indeterminate goal value (-1) are omitted from the output.
        """
        output_file.write("begin_goal_state\n")
        for i, proposition in enumerate(self.goal_state):
            if(self.goal_state[i] != -1):
                output_file.write(str(i) + " " + str(self.goal_state[i]) +  "\n")
        output_file.write("end_goal_state\n")

    def __store_basic_elements(self, parsed_problem) -> None:
        """Pre-proccess and store some complementary attributes.

        Args:
            parsed_problem: The parsed problem description.
        """
        self.objects = self.__merge_obj_const()
        self.propositions, self.dict_propositions = self.__store_propositions()
        self.initial_state = self.__process_state(parsed_problem.init, 0)
        self.goal_state = self.__process_state(parsed_problem.goal, -1)

    def __merge_obj_const(self) -> dict[str, list[Object]]:
        """Combines domain constants and problem objects into a unified object dictionary.

        Returns:
            dict[str, list[Object]]: A map from types to a list of 'Object' objects.

        Note:
            This method assumes that object types are consistent between the domain and problem definitions.
        """
        objects = self.problem.get_objects()
        constants = self.domain.get_constants()
        objects.update(constants)
        return objects

    def __store_propositions(self) -> tuple[list[Proposition], dict[str, Proposition]]:
        """Builds a list of propositions, along with a map from the names to the 'Proposition' objects.

        Returns:
            list[Proposition]: The list of propositions of the corresponding PDDL domain.
            dict[str, Proposition]): A map from the proposition names to the 'Proposition' objects.
        """
        propositions = []
        dict_propositions = {}
        predicates = self.domain.get_predicates()

        for _, predicate in predicates.items():
            object_combinations = self.__get_object_combinations(predicate)
            for obj_combination in object_combinations:
                proposition = Proposition(predicate, list(obj_combination), len(propositions))
                propositions.append(proposition)
                dict_propositions[str(proposition)] = proposition

        return propositions, dict_propositions

    def __is_proposition_negated(self, parsed_prop) -> bool:
        """Determines whether a parsed proposition is negated.

        Args:
            parsed_prop: The parsed proposition description.

        Returns:
            bool: True if the proposition is negated; False otherwise.
        """
        return (str(type(parsed_prop)) == "<class 'pddl.logic.base.Not'>")

    def __build_proposition_names(self, parsed_prop, is_negated: bool) -> str:
        """Constructs a standardized proposition name string from a parsed proposition.

        Args:
            parsed_prop: The parsed proposition description.
            is_negated (bool): Indicates whether the proposition is negated.

        Returns:
            str: The standardized proposition name
        """
        low = 1
        high = -1
        if is_negated:
            low = 6
            high = -2

        return '_'.join(str(parsed_prop)[low:high].split())

    def __process_state(self, parsed_state, default_value: int) -> list[int]:
        """Converts a parsed PDDL state into the list of truth values for propositions.

        Args:
            parsed_state: The parsed state object from the PDDL problem.
            default_value (int, optional): The default value to use for propositions not explicitly mentioned in the state. Defaults to 'default_value'.

        Returns:
            list[int]: The list of truth values (1 for true, 0 for false, 'default_value' for don't care) corresponding to the propositions defined in the domain. The list's length matches the number of propositions.
        """
        if (str(type(parsed_state)) == "<class 'pddl.logic.base.And'>" ):
            parsed_state = parsed_state.operands
        elif (str(type(parsed_state)) == "<class 'pddl.logic.predicates.Predicate'>"):
            parsed_state = (parsed_state,)
        state = [default_value for i in range(len(self.propositions))]
        for parsed_prop in parsed_state:
            prop_is_negated = self.__is_proposition_negated(parsed_prop)
            prop_names = self.__build_proposition_names(parsed_prop, prop_is_negated)
            for i, proposition in enumerate(self.propositions):
                if proposition.compare_names(prop_names):
                    state[i] = 0 if prop_is_negated else 1
        return state

    def __get_object_combinations(self, predicate: Predicate) -> tuple[Object]:
        """Generates unique combinations of objects that satisfy a given predicate's variable types.

        This method takes a predicate and identifies the types of variables it expects. It then retrieves all objects of those types and creates unique combinations where each object in a combination is of the required type.

        Args:
            predicate (Predicate): The predicate for which object combinations are to be generated.

        Returns:
            list[tuple[Object, ...]]: The list of tuples, where each tuple represents a unique combination of objects that can satisfy the predicate's variable types.
        """
        variable_types = predicate.get_variable_types()

        object_combinations = []
        for variable_type in variable_types:
            objects_of_type = self.objects.get(variable_type, [])
            object_combinations.append(objects_of_type)

        all_products = itertools.product(*object_combinations)

        unique_products = [tup for tup in all_products if len(tup) == len(set(tup))]

        return unique_products

    def __instantiate_reachable_actions(self) -> tuple[list[tuple[Action, tuple[Object]]], list[int]]:
        """Calls the function run_ground and returns the tuple returned by the call."""
        reachable_actions, reachable_propositions = run_ground(self.initial_state, self.propositions,
                                       self.dict_propositions,
                                       self.domain.get_pred_to_actions(),
                                       self.problem.get_objects())
        return (reachable_actions, reachable_propositions)

    def __build_instantiated_action_name(self, action: Action, parameters: tuple[Object]) -> str:
        """Builds an instantiated action name by combining the action name and the parameters names."""
        name = str(action)
        for parameter in parameters:
            name += "_" + str(parameter)
        return name

    def __print_preconditions_reachable_action(self, action: Action, parameters: tuple[Object], output_file: TextIO) -> None:
        """Writes the preconditions of a reachable action to the specified output stream.

        Args:
            action (Action): The instantiated action.
            parameters (tuple[Object]): The parameters of the instantiated action.
            output_file (TextIO): The text stream where the formatted effects of the reachable action should be written.
        """
        preconditions = action.get_preconditions()

        output_file.write(str(len(preconditions)) + "\n")
        for precondition in preconditions:
            generic_proposition, value = precondition
            proposition = find_proposition(generic_proposition, parameters,
                                            self.dict_propositions, action.get_parameters())
            proposition_index = proposition.get_index()
            output_file.write(str(proposition_index) + " " + str(int(value))  + "\n")

    def __print_effects_reachable_action(self, action: Action, parameters: tuple[Object], output_file: TextIO) -> None:
        """Writes the effects of a reachable action, enclosed in 'begin_nd_effects' and 'end_nd_effects' tags, to the specified output stream.

        Args:
            output_file (TextIO): The text stream where the formatted effects of the reachable action should be written.
        """
        effects = action.get_effects()
        output_file.write("begin_nd_effects\n")

        if len(effects) == 0:
            output_file.write("1\n")
            output_file.write("effects\n")
            self.__print_preconditions_reachable_action(action, parameters, output_file)
        else:
            output_file.write(str(len(effects)) + "\n")
            for effect_scenario in effects:
                output_file.write("effects\n")
                if len(effect_scenario) == 0:
                    self.__print_preconditions_reachable_action(action, parameters, output_file)
                else:
                    output_file.write(str(len(effect_scenario)) + "\n")
                    for effect_tuple in effect_scenario:
                        generic_proposition, value = effect_tuple
                        proposition = find_proposition(generic_proposition, parameters,
                                                        self.dict_propositions, action.get_parameters())
                        output_file.write(str(proposition.get_index()) + " " + str(int(value)) + "\n")
        output_file.write("end_nd_effects\n")

    def __print_reachable_actions(self, output_file: TextIO) -> None:
        """Writes the reachable actions, enclosed in 'begin_actions' and 'end_actions' tags, to the specified output stream.

        Args:
            output_file (TextIO): The text stream where the formatted reachable actions should be written.
        """
        output_file.write("begin_actions\n")
        output_file.write(str(len(self.reachable_actions)) + "\n")
        for action_tup in self.reachable_actions:
            action, parameters = action_tup
            output_file.write("begin_action\n")
            action_name = self.__build_instantiated_action_name(action, parameters)
            output_file.write(action_name + "\n")
            output_file.write("preconditions\n")
            self.__print_preconditions_reachable_action(action, parameters, output_file)
            self.__print_effects_reachable_action(action, parameters, output_file)
            output_file.write("end_action\n")
        output_file.write("end_actions\n")
        return

    def __print_reachable_propositions(self, output_file: TextIO) -> None:
        """Writes the reachable propositions, enclosed in 'begin_reachable_propositions' and 'end_reachable_propositions' tags, to the specified output stream.

        Args:
            output_file (TextIO): The text stream where the formatted reachable proposition should be written.
        """
        output_file.write("begin_reachable_propositions\n")
        reachable_propositions = []
        for i in range(len(self.reachable_propositions) // 2):
            if self.reachable_propositions[i] == 1:
                reachable_propositions.append(i)
        output_file.write(str(len(reachable_propositions)) + "\n")
        for i in reachable_propositions:
            output_file.write(str(i) + "\n")
        output_file.write("end_reachable_propositions")

    def get_propositions(self) -> list[Proposition]:
        """Gets domain propositions list."""
        return self.propositions

    def get_dict_propositions(self) -> dict[str, Proposition]:
        """Gets name-to-Proposition mapping."""
        return self.dict_propositions

    def get_initial_state(self) -> list[int]:
        """Gets problem initial state bitmap."""
        return self.initial_state

    def get_goal_state(self) -> list[int]:
        """Gets problem goal state mapping."""
        return self.goal_state

    def get_actions(self) -> list[Action]:
        """Gets domain action list."""
        return self.actions

    def get_reachable_actions(self):
        """Gets the list of reachable actions, which is a list of pairs composed by the action and its respective parameters."""
        return self.reachable_actions

    def print_bdds(self, output_file: TextIO) -> None:
        """Writes the problem definition, propositions, initial state, and goal state in a structured format to a file.

        This method generates a file containing a structured representation of the planning problem, including:

        - Problem Name: Enclosed in 'begin_problem_name' and 'end_problem_name' tags.
        - Propositions: Enclosed in 'begin_propositions' and 'end_propositions' tags, along with their indices.
        - Initial State: Enclosed in 'begin_initial_state' and 'end_initial_state' tags, with truth values for each proposition.
        - Goal State: Enclosed in 'begin_goal_state' and 'end_goal_state' tags, with truth values for defined goal propositions.
        - Reachable Actions: Enclosed in 'begin_actions' and 'end_actions' tags, with their respective preconditions and effects.
        - Reachable Propositions: Enclosed in 'begin_reachable_propositions' and 'end_reachable_propositions' tags, with the indices of the reachable propositions.

        Args:
            output_file_path (str): The path to the file where the output should be written.
        """
        with open(output_file, 'w') as output_file:
            self.__print_problem_name(output_file)
            self.__print_propositions(output_file)
            self.__print_initial_state(output_file)
            self.__print_goal_state(output_file)
            self.__print_reachable_actions(output_file)
            self.__print_reachable_propositions(output_file)