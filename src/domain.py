from pddl import parse_domain

def store_constants(domain, dict_const = {}):
    for constant in domain.constants:
        key = next(iter(constant.type_tags))
        if key not in dict_const:
            dict_const[key] = []
        dict_const[key].append(repr(constant)[9:-1])
    return dict_const

def main():
    domain = parse_domain("../tests/gripper3.pddl")
    dict_obj = store_constants(domain)
    print(dict_obj)

if __name__ == "__main__":
    main()