class Object:
    """Represents a PDDL object.

    Attributes:
        name (str): A descriptive name for the object.
        type (str): The type of the object.

    Examples:
        >>> rooma = Object("rooma", "room")
        >>> ball1 = Object("ball1", "ball")
    """

    def __init__(self, name: str, type: str) -> None:
        """Initializes an 'Object' object.

        Args:
            name (str): The name of the object.
            type (str): The type of the object.
        """
        self.name = name
        self.type = type

    def __str__(self) -> str:
        """Provides a string representation for the object (its name).

        Returns:
            str: The standard string representation for 'Object' instances.
        """
        return self.name

    def __lt__(self, other) -> bool:
        """Compares this object to another lexicographically, based on name.

        Args:
            other (Object): The object to compare to.

        Returns:
            bool: True if this object is lexicographically less than 'other'; False otherwise.
        """
        return self.name < other.name

    def get_name(self) -> str:
        """Gets object's name."""
        return self.name

    def get_type(self) -> str:
        """Gets object's type."""
        return self.type

class Predicate:
    """Represents a PDDL Predicate.

    Attributes:
        name (str): A descriptive name for the predicate.
        variable_types (list[str]): The list of variable types of the predicate.

    Examples:
        >>> at_robby = Predicate("at-robby", [ "room" ])
        >>> at_ball = Predicate("at-ball", [ "ball", "room" ])
    """

    def __init__(self, name: str, variable_types: list[str] = []) -> None:
        """Initiliazes a 'Predicate' object.

        Args:
            name (str): The name of the predicate.
            variable_types (list[str]): The list of variable types.
        """
        self.name = name
        self.variable_types = variable_types[:]

    def __str__(self) -> str:
        """Provides a string representation for the predicates.

        Returns:
            str: The name of the predicate besides its variable types list.
        """
        output = self.name + " " + str(self.variable_types)
        return output

    def __eq__(self, other) -> bool:
        """Compares this predicate to another lexicographically, based on name.

        Args:
            other (Predicate): The predicate to compare to.

        Returns:
            bool: True if 'other' is an instance of 'Predicate', and its name is equal to this predicate's name; False otherwise.
        """
        if isinstance(other, Predicate):
            return self.name == other.name
        return False

    def __hash__(self) -> int:
        """Calculates the hash value of this predicate, based on name.

        Returns:
            int: A hash value for this predicate.
        """
        return hash(self.name)

    def get_name(self) -> str:
        """Gets the predicate's name."""
        return self.name

    def get_variable_types(self) -> list[str]:
        """Gets the variable types"""
        return self.variable_types

class Proposition:
    """Represents a PDDL Proposition, which is an instantiated predicate.

    Attributes:
        name (str): A descriptive name for the proposition.
        predicate (Predicate): The predicate corresponding to the proposition.
        objects (list[Object]): The list of (instantiated) objects corresponding to the proposition.
        index (int): An index associated with the proposition.

    Examples:
        >>> at_ball = Predicate("at-ball", [ "ball", "room" ])
        >>> objects = [ Object("ball1", "ball"), Object("rooma", "room") ]
        >>> at_ball_ball1_rooma = Proposition(at_ball, objects, 0)
    """
    def __init__(self, predicate: Predicate, objects: list[Object], index: int = -1) -> None:
        """Initializes a 'Proposition' object

        Args:
            predicate (Predicate): The predicate corresponding to the proposition.
            objects (list[Objects]): The list of (instantiated) objects.
            index (int): An index associated with the proposition.
        """
        self.predicate = predicate
        self.objects = objects[:]
        self.name = self.__build_proposition_name()
        self.index = index

    def __str__(self) -> str:
        """Provides a string representation for propositions.

        Returns:
            str: The name of the proposition.
        """
        return self.name

    def __repr__(self) -> str:
        """Provides a standard representation for propositions.

        Returns:
            str: The name of the proposition.
        """
        return self.name

    def __eq__(self, other: 'Proposition') -> bool:
        """Compares this proposition to another lexicographically, based on name.

        Args:
            other (Proposition): The proposition to compare to.

        Returns:
            bool: True if 'other' is an instance of 'Proposition', and its name is equal to this proposition's name; False otherwise.
        """
        if isinstance(other, Proposition):
            return self.name == other.name
        return False

    def __build_proposition_name(self) -> str:
        """Builds a proposition name by combining the predicate name and object names."""
        names = ""
        for object in self.objects:
            names += "_" + object.get_name()
        names = self.predicate.get_name() + names
        return names

    def compare_names(self, prop_name: str) -> bool:
        """Compare the name of the proposition with the strings 'prop_name'.

        Args:
            prop_name (str): The string to be compared to the proposition name.

        Returns:
            bool: True if the name of the proposition is equal to 'prop_name'; False otherwise.
        """
        if prop_name == self.name:
            return True
        return False

    def get_predicate(self) -> Predicate:
        """Gets predicate."""
        return self.predicate

    def get_objects(self) -> list[Object]:
        """Gets objects."""
        return self.objects

    def get_index(self) -> int:
        """Gets proposition index."""
        return self.index

class Action:
    """Represents a PDDL Action.

    Attributes:
        name (str): A descriptive name for the action.
        arguments (list[Objects]): The list of arguments of the action.
        preconditions (list[(Proposition, bool)]): A list of tuples, with a proposition and its corresponding (boolean) value.
        effects (list[list[(Proposition, bool)]]): A list of effects; each effect is a list of propositions and their corresponding values.
    """
    def __init__(self, name: str, arguments: list[Object], preconditions: list[tuple[Proposition, bool]],
                    effects: list[list[tuple[Proposition, bool]]]) -> None:
        """Initializes an 'Action' object.

        Attributes:
            name (str): A descriptive name for the action.
            arguments (list[Objects]): The list of arguments of the action.
            preconditions (list[(Proposition, bool)]): The list of preconditions for the action.
            effects (list[list[(Proposition, bool)]]): The list of effects of the action.
        """
        self.name = name
        self.arguments = arguments
        self.preconditions = preconditions[:]
        self.effects = effects[:]

    def get_name(self) -> str:
        """Gets action's name."""
        return self.name

    def get_arguments(self) -> list[Object]:
        """Gets action's arguments list."""
        return self.arguments

    def get_preconditions(self) -> list[tuple[Proposition, bool]]:
        """Gets action's preconditions' list."""
        return self.preconditions

    def get_effects(self) -> list[list[tuple[Proposition, bool]]]:
        """Gets action's effects' list."""
        return self.effects