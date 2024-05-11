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
        self.__store_basic_elements(parsed_problem)
        with open("../output.txt", "x") as output_file:
            self.__print_problem_name(output_file)
            self.__print_propositions(output_file)
            self.__print_initial_state(output_file)

    def __print_problem_name(self, output_file):
        output_file.write("begin_problem_name\n")
        output_file.write(self.problem.get_name() + "\n")
        output_file.write("end_problem_name\n\n")
    
    def __print_propositions(self, output_file):
        output_file.write("begin_propositions\n")
        output_file.write(str(len(self.propositions)) + "\n")
        for i, proposition in enumerate(self.propositions):
            output_file.write(str(proposition) + " " + str(i) + "\n")
        output_file.write("end_propositions\n\n")

    def __print_initial_state(self, output_file):
        output_file.write("begin_initial_state\n")
        output_file.write(str(len(self.initial_state)) + "\n")
        for i, proposition in enumerate(self.initial_state):
            output_file.write(str(i) + " " + str(proposition) + "\n")
        output_file.write("end_initial_state\n\n")
    
    def __store_basic_elements(self, parsed_problem):
        self.objects = self.__merge_obj_const()
        self.propositions = self.__store_propositions()
        self.initial_state = self.__process_initial_state(parsed_problem.init)
                
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
    
    def __process_initial_state(self, parsed_initial):
        initial_state = [0 for i in range(len(self.propositions))]
        for parsed_prop in parsed_initial:
            prop_name = parsed_prop.name
            obj_names = []
            for object in parsed_prop.terms:
                obj_names.append(str(object.name))
            for i, proposition in enumerate(self.propositions):
                if proposition.compare_names(prop_name, obj_names):
                    initial_state[i] = 1
        return initial_state
    
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

if __name__ == "__main__":
    main()