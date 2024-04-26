from pddl import parse_problem

def  store_objects(problem, dict_obj = {}):
    for object in problem.objects:
        key = str(next(iter(object.type_tags)))
        if key not in dict_obj:
            dict_obj[key] = []
        dict_obj[key].append(repr(object)[9:-1])
    return dict_obj

def main():
    problem = parse_problem("../tests/gripper3_2_balls.pddl")
    dict_obj = store_objects(problem)
    print(dict_obj)

if __name__ == "__main__":
    main()