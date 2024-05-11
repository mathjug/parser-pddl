from pddl import parse_problem
from custom_types import Object

class Problem:
    def __init__(self, parsed_problem):
        self.name = parsed_problem.name
        self.objects = self.__store_objects(parsed_problem)

    def __store_objects(self, parsed_problem):
        dict_obj = {}
        for object in parsed_problem.objects:
            object_type = str(next(iter(object.type_tags)))
            if object_type not in dict_obj:
                dict_obj[object_type] = []

            object_name = repr(object)[9:-1]
            instantiated_object = Object(object_name, object_type)
            dict_obj[object_type].append(instantiated_object)
        return dict_obj
    
    def get_name(self):
        return self.name

    def get_objects(self):
        return self.objects

def main():
    problem_path = "../tests/examples/gripper3_2_balls.pddl"
    problem = Problem(problem_path)

    object_dict = problem.objects
    for object_type in object_dict:
        print(object_type)
        objects = object_dict[object_type]
        for object in objects:
            print(f"\t{object}")
        print()

if __name__ == "__main__":
    main()