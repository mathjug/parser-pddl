from pddl import parse_domain, parse_problem
from src.problem import Problem
from src.domain import Domain
from src.custom_types import Proposition
import itertools

class Parser:
    def __init__(self, domain_path, problem_path):
        parsed_problem = parse_problem(problem_path)
        parsed_domain = parse_domain(domain_path)
        self.problem = Problem(parsed_problem)
        self.domain = Domain(parsed_domain)
        self.__store_basic_elements(parsed_problem)
        self.actions = self.domain.get_actions()

    def __print_problem_name(self, output_file):
        output_file.write("begin_problem_name\n")
        output_file.write(self.problem.get_name() + "\n")
        output_file.write("end_problem_name\n")

    def __print_propositions(self, output_file):
        output_file.write("begin_propositions\n")
        output_file.write(str(len(self.propositions)) + "\n")
        for i, proposition in enumerate(self.propositions):
            output_file.write(str(proposition) + " " + str(i) + "\n")
        output_file.write("end_propositions\n")

    def __print_initial_state(self, output_file):
        output_file.write("begin_initial_state\n")
        output_file.write(str(len(self.initial_state)) + "\n")
        for i, proposition in enumerate(self.initial_state):
            output_file.write(str(i) + " " + str(proposition) + "\n")
        output_file.write("end_initial_state\n")

    def __print_goal_state(self, output_file):
        output_file.write("begin_goal_state\n")
        for i, proposition in enumerate(self.goal_state):
            if(self.goal_state[i] != -1):
                output_file.write(str(i) + " " + str(self.goal_state[i]) +  "\n")
        output_file.write("end_goal_state\n")

    def __store_basic_elements(self, parsed_problem):
        self.objects = self.__merge_obj_const()
        self.propositions, self.dict_propositions = self.__store_propositions()
        self.initial_state = self.__process_state(parsed_problem.init, 0)
        self.goal_state = self.__process_state(parsed_problem.goal, -1)

    def __merge_obj_const(self):
        objects = self.problem.get_objects()
        constants = self.domain.get_constants()
        objects.update(constants)

        return objects

    def __store_propositions(self):
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

    def __is_proposition_negated(self, parsed_prop):
        return (str(type(parsed_prop)) == "<class 'pddl.logic.base.Not'>")

    def __build_proposition_names(self, parsed_prop, is_negated):
        low = 1
        high = -1
        if is_negated:
            low = 6
            high = -2

        return '_'.join(str(parsed_prop)[low:high].split())

    def __process_state(self, parsed_state, default_value):
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

    def __get_object_combinations(self, predicate):
        variable_types = predicate.get_variable_types()

        object_combinations = []
        for variable_type in variable_types:
            objects_of_type = self.objects.get(variable_type, [])
            object_combinations.append(objects_of_type)

        all_products = itertools.product(*object_combinations)

        unique_products = [tup for tup in all_products if len(tup) == len(set(tup))]
    
        return unique_products

    def get_propositions(self):
        return self.propositions
    
    def get_dict_propositions(self):
        return self.dict_propositions

    def get_initial_state(self):
        return self.initial_state

    def get_goal_state(self):
        return self.goal_state
    
    def get_actions(self):
        return self.actions

    def print_bdds(self, output_file):
        with open(output_file, 'w') as output_file:
            self.__print_problem_name(output_file)
            self.__print_propositions(output_file)
            self.__print_initial_state(output_file)
            self.__print_goal_state(output_file)