from pddl import parse_problem
from src import Object

class Problem:
    """Represents a PDDL problem.

    Attributes:
        name (str): A descriptive name for the planning problem.
        objects (dict[str, list[Object]]): A map from object types (strings) to lists of instances of the 'Object' class.

    Examples:
        >>> parsed_problem = pddl.parse_problem("tests/examples/gripper3_3_balls.pddl")
        >>> problem = Problem(parsed_problem)
    """

    def __init__(self, parsed_problem) -> None:
        """Initializes a Problem object.

        Args:
            parsed_problem: The parsed problem description, as returned by 'pddl.parse_problem'.

        Note:
            This method assumes that the 'parsed_problem' object contains the following information:
                - 'name': The AI planning problem name.
                - 'objects': a list of objects valid for the problem domain.
        """
        self.name = parsed_problem.name
        self.objects = self.__store_objects(parsed_problem)

    def __store_objects(self, parsed_problem) -> dict[str, list[Object]]:
        """Stores objects corresponding to the instantiated problem.

        Args:
            parsed_problem: The parsed problem description.

        Returns:
            dict[str, list[Object]]: A map from object types (strings) to lists of instances of the 'Object' class.
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

    def get_name(self) -> str:
        """Gets problem name."""
        return self.name

    def get_objects(self) -> dict[str, list[Object]]:
        """Gets type-to-Object mapping for problem objects."""
        return self.objects