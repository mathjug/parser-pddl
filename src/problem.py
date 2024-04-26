from pddl import parse_problem

class Problem:
    def __init__(self, problem_path):
        parsed_problem = parse_problem(problem_path)
        self.objects = self.__store_objects(parsed_problem)

    def __store_objects(self, parsed_problem, dict_obj = {}):
        for object in parsed_problem.objects:
            key = str(next(iter(object.type_tags)))
            if key not in dict_obj:
                dict_obj[key] = []
            dict_obj[key].append(repr(object)[9:-1])
        return dict_obj

def main():
    problem_path = "../tests/examples/gripper3_2_balls.pddl"
    problem = Problem(problem_path)
    print(problem.objects)

if __name__ == "__main__":
    main()