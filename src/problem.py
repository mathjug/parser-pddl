from pddl import parse_problem
from src import Object

class Problem:
    """Represents an AI planning problem.

    Attributes:
        name (str): A descriptive name for the planning problem.
        objects (dict): A dictionary whose keys are object types (strings) and the values are instances of the 'Object' class.
            For example:
            '''python
            objects = {
                "ball": [Object("ball1", "ball"), Object("ball2", "ball"), Object("ball3", "ball")],
                "room": [Object("rooma", "room"), Object("roomb", "room")]
            }
            '''
    """

    def __init__(self, parsed_problem):
        """Initializes a Problem object.

        Args:
            parsed_problem (pddl.Problem): The parsed problem description, as returned by 'pddl.parse_problem'.

        Note:
            This method assumes that the 'parsed_problem' object contains the following informations:
                - 'name': The AI planning problem name.
                - 'objects': a list of objects valid for the problem domain.
        """
        self.name = parsed_problem.name
        self.objects = self.__store_objects(parsed_problem)

    def __store_objects(self, parsed_problem):
        """Stores objects corresponding to the instantiated problem.

        Args:
            parsed_problem (pddl.Problem): The parsed problem description, as returned by 'pddl.parse_problem'.

        Returns:
            dict: A dictionary whose keys are object types (strings) and the values are instances of the 'Object' class.
        """
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
        """Gets the AI problem name.
        """
        return self.name

    def get_objects(self):
        """Gets the object dictionary, whose keys are the object types (strings) and the values are instances of the 'Object' class.
        """
        return self.objects