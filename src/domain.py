from pddl import parse_domain

class Domain:
    def __init__(self, domain_path):
        parsed_domain = parse_domain(domain_path)
        self.constants = self.__store_constants(parsed_domain)
        self.predicates = self.__store_predicates(parsed_domain)

    def __store_constants(self, parsed_domain, dict_const = {}):
        for constant in parsed_domain.constants:
            key = str(next(iter(constant.type_tags)))
            if key not in dict_const:
                dict_const[key] = []
            dict_const[key].append(repr(constant)[9:-1])
        return dict_const

    def __store_predicates(self, parsed_domain, dict_predicates = {}):
        for predicate in parsed_domain.predicates:
            dict_predicates[predicate.name] = []
            for object in predicate.terms:
                dict_predicates[predicate.name].append(str(next(iter(object.type_tags))))
        return dict_predicates

def main():
    domain_path = "../tests/examples/gripper3.pddl"
    domain = Domain(domain_path)
    print("Constants:", domain.constants)
    print("\nPredicates:", domain.predicates)

if __name__ == "__main__":
    main()