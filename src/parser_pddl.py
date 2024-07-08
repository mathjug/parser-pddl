from pddl import parse_domain, parse_problem
from src import Action, Domain, Object, Problem, Proposition, Predicate
from typing import TextIO
import itertools

class Parser:
    """Represents the Parser, the central unit for domain and problem analysis.

    This class encapsulates the parsing and representation of PDDL (Planning Domain Definition Language)
    files, enabling the extraction and manipulation of domain elements and problem specifics for planning.

    Attributes:
        domain (Domain): The parsed representation of the planning domain.
        problem (Problem): The parsed representation of the specific planning problem.
        actions (list[Action]): A list of actions defined in the domain.
        objects (dict[str, list[Object]]): A dictionary mapping object types (str) to lists of
            corresponding objects.
        propositions (list[Proposition]): A list of all possible propositions in the domain.
        dict_propositions (dict[str, Proposition]): A dictionary mapping proposition names (str)
            to Proposition objects.
        initial_state (list[int]): A bitmask representing the initial truth values of propositions
            (1 for true, 0 for false).
        goal_state (list[int]): A bitmask representing the goal truth values of propositions
            (1 for true, 0 for false, -1 for don't care).

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
            The initialization process assumes a valid and coherent relationship between the problem
                and domain definitions.
        """
        parsed_problem = parse_problem(problem_path)
        parsed_domain = parse_domain(domain_path)
        self.problem = Problem(parsed_problem)
        self.domain = Domain(parsed_domain)
        self.__store_basic_elements(parsed_problem)
        self.actions = self.domain.get_actions()

    def __print_problem_name(self, output_file: TextIO) -> None:
        """Writes the problem name, enclosed in 'begin_problem_name' and 'end_problem_name' tags,
            to the specified output stream.

        Args:
            output_file (TextIO): The text stream where the formatted problem name should be written.
        """
        output_file.write("begin_problem_name\n")
        output_file.write(self.problem.get_name() + "\n")
        output_file.write("end_problem_name\n")

    def __print_propositions(self, output_file: TextIO) -> None:
        """Writes propositions and their indices, enclosed in 'begin_propositions' and 'end_propositions' tags,
            to the specified output stream.

        Args:
            output_file (TextIO): The text stream where the formatted propositions should be written.
        """
        output_file.write("begin_propositions\n")
        output_file.write(str(len(self.propositions)) + "\n")
        for i, proposition in enumerate(self.propositions):
            output_file.write(str(proposition) + " " + str(i) + "\n")
        output_file.write("end_propositions\n")

    def __print_initial_state(self, output_file: TextIO) -> None:
        """Writes the initial state, enclosed in 'begin_initial_state' and 'end_initial_state' tags,
            to the specified output stream.

        Args:
            output_file (TextIO): The text stream where the formatted initial state should be written.
        """
        output_file.write("begin_initial_state\n")
        output_file.write(str(len(self.initial_state)) + "\n")
        for i, proposition in enumerate(self.initial_state):
            output_file.write(str(i) + " " + str(proposition) + "\n")
        output_file.write("end_initial_state\n")

    def __print_goal_state(self, output_file: TextIO) -> None:
        """Writes the goal state, enclosed in 'begin_goal_state' and 'end_goal_state' tags,
            to the specified output stream.

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
        """Converts a parsed PDDL state into a list of truth values for propositions.

        Args:
            parsed_state: The parsed state object from the PDDL problem.
            default_value (int, optional): The default value to use for propositions not explicitly
                mentioned in the state. Defaults to 'default_value'.

        Returns:
            list[int]: A list of truth values (1 for true, 0 for false, 'default_value' for don't care)
                corresponding to the propositions defined in the domain. The list's length matches the number
                of propositions.
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

    def __get_object_combinations(self, predicate: Predicate):
        """Generates unique combinations of objects that satisfy a given predicate's variable types.

        This method takes a predicate and identifies the types of variables it expects.
        It then retrieves all objects of those types and creates unique combinations
        where each object in a combination is of the required type.

        Args:
            predicate (Predicate): The predicate for which object combinations are to be generated.

        Returns:
            list[tuple[Object, ...]]: A list of tuples, where each tuple represents a unique combination of objects
                that can satisfy the predicate's variable types.
        """
        variable_types = predicate.get_variable_types()

        object_combinations = []
        for variable_type in variable_types:
            objects_of_type = self.objects.get(variable_type, [])
            object_combinations.append(objects_of_type)

        all_products = itertools.product(*object_combinations)

        unique_products = [tup for tup in all_products if len(tup) == len(set(tup))]

        return unique_products

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

    def print_bdds(self, output_file: TextIO) -> None:
        """Writes the problem definition, propositions, initial state, and goal state in a structured format to a file.

        This method generates a file containing a structured representation of the planning problem, including:

        - Problem Name: Encased in `begin_problem_name` and `end_problem_name` tags.
        - Propositions:  Encased in `begin_propositions` and `end_propositions` tags, along with their indices.
        - Initial State: Encased in `begin_initial_state` and `end_initial_state` tags, with truth values for each proposition.
        - Goal State:   Encased in `begin_goal_state` and `end_goal_state` tags, with truth values for defined goal propositions.

        Args:
            output_file_path (str): The path to the file where the output should be written.
        """
        with open(output_file, 'w') as output_file:
            self.__print_problem_name(output_file)
            self.__print_propositions(output_file)
            self.__print_initial_state(output_file)
            self.__print_goal_state(output_file)