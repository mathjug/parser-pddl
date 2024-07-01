from pddl import parse_problem
from src.custom_types import Object

class Problem:
    def __init__(self, parsed_problem):
        self.name = parsed_problem.name
        self.objects = self.__store_objects(parsed_problem)

    def __store_objects(self, parsed_problem):
        dict_obj = {}
        for parsed_object in parsed_problem.objects:
            object_type = str(next(iter(parsed_object.type_tags)))
            if object_type not in dict_obj:
                dict_obj[object_type] = []
            object_name = parsed_object.name
            object = Object(object_name, object_type)
            dict_obj[object_type].append(object)
        return dict_obj

    def get_name(self):
        return self.name

    def get_objects(self):
        return self.objects