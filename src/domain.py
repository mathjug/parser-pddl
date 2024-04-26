from pddl import parse_domain

def store_constants(domain, dict_const = {}):
    for constant in domain.constants:
        key = str(next(iter(constant.type_tags)))
        if key not in dict_const:
            dict_const[key] = []
        dict_const[key].append(repr(constant)[9:-1])
    return dict_const

def store_predicates(domain, dict_predicates = {}):
    for predicate in domain.predicates:
        dict_predicates[predicate.name] = []
        for object in predicate.terms:
            dict_predicates[predicate.name].append(str(next(iter(object.type_tags))))
    return dict_predicates

def main():
    domain = parse_domain("../tests/gripper3.pddl")
    dict_obj = store_constants(domain)
    print("Objetos:", dict_obj)
    dict_predicates = store_predicates(domain)
    print("\nPredicados:", dict_predicates)

if __name__ == "__main__":
    main()