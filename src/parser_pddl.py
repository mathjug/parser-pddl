from pddl import parse_domain, parse_problem
from problem import Problem
from domain import Domain
from custom_types import Proposition
import itertools

class Parser:
    def __init__(self, domain_path, problem_path):
        parsed_problem = parse_problem(problem_path)
        parsed_domain = parse_domain(domain_path)
        self.problem = Problem(parsed_problem)
        self.domain = Domain(parsed_domain)
        self.objects = self.__merge_obj_const()
        self.propositions = self.__store_propositions()
        self.initial_state = self.process_initial_state(parsed_problem.init)

    def process_initial_state(self, parsed_initial):
        initial_state = []
        for parsed_prop in parsed_initial:
            prop_name = parsed_prop.name
            obj_names = []
            for object in parsed_prop.terms:
                obj_names.append(str(object.name))
            for proposition in self.propositions:
                if proposition.compare_names(prop_name, obj_names):
                    initial_state.append(proposition)
        return initial_state
                
    def __merge_obj_const(self):
        objects = self.problem.get_objects()
        constants = self.domain.get_constants()
        objects.update(constants)
        return objects
    
    def __store_propositions(self):
        propositions = []
        predicates = self.domain.get_predicates()

        for predicate in predicates:
            object_combinations = self.__get_object_combinations(predicate)
            for obj_combination in object_combinations:
                proposition = Proposition(predicate, list(obj_combination))
                propositions.append(proposition)

        return propositions
    
    def __get_object_combinations(self, predicate):
        variable_types = predicate.get_variable_types()

        object_combinations = []
        for variable_type in variable_types:
            objects_of_type = self.objects.get(variable_type, [])
            object_combinations.append(objects_of_type)

        return itertools.product(*object_combinations)

    def get_propositions(self):
        return self.propositions

    def get_initial_state(self):
        return self.initial_state

def main():
    domain_path = "../tests/examples/gripper3.pddl"
    problem_path = "../tests/examples/gripper3_2_balls.pddl"
    parser = Parser(domain_path, problem_path)
    initial_state = parser.get_initial_state()
    for proposition in initial_state:
        print(proposition)

if __name__ == "__main__":
    main()