from problem import Problem
from domain import Domain
from custom_types import Proposition
import itertools

class Parser:
    def __init__(self, domain_path, problem_path):
        self.problem = Problem(problem_path)
        self.domain = Domain(domain_path)
        self.objects = self.__merge_obj_const()
        self.propositions = self.__store_propositions()
    
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

def main():
    domain_path = "../tests/examples/gripper3.pddl"
    problem_path = "../tests/examples/gripper3_2_balls.pddl"
    parser = Parser(domain_path, problem_path)
    propositions = parser.get_propositions()
    for proposition in propositions:
        print(proposition)

if __name__ == "__main__":
    main()