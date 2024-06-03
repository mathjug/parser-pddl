from pddl import parse_domain
from custom_types import Object, Predicate

class Domain:
    def __init__(self, parsed_domain):
        self.constants = self.__store_constants(parsed_domain)
        self.predicates = self.__store_predicates(parsed_domain)
        self.actions = self.__store_actions(parsed_domain)

    def __store_constants(self, parsed_domain):
        dict_const = {}
        for constant in parsed_domain.constants:
            constant_type = str(next(iter(constant.type_tags)))
            if constant_type not in dict_const:
                dict_const[constant_type] = []

            constant_name = repr(constant)[9:-1]
            constant = Object(constant_name, constant_type)
            dict_const[constant_type].append(constant)

        return dict_const

    def __store_predicates(self, parsed_domain):
        predicates = []
        for predicate in parsed_domain.predicates:
            variable_types = []
            for object in predicate.terms:
                variable_types.append(str(next(iter(object.type_tags))))

            instantiated_predicate = Predicate(predicate.name, variable_types)
            predicates.append(instantiated_predicate)

        return predicates

    def get_constants(self):
        return self.constants

    def get_predicates(self):
        return self.predicates

    def get_actions(self):
        return self.actions

def main():
    domain_path = "../tests/examples/gripper3.pddl"
    parsed_domain = parse_domain(domain_path)
    domain = Domain(parsed_domain)

    print("CONSTANTS")
    constant_dict = domain.constants
    for constant_type in constant_dict:
        print(constant_type, end = ':')
        constants = constant_dict[constant_type]
        for constant in constants:
            print(f" {constant}", end = '')
        print("\n")

    print("PREDICATES")
    predicates = domain.predicates
    for predicate in predicates:
        print(predicate)

if __name__ == "__main__":
    main()