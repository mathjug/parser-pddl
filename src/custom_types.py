class Object:
    def __init__(self, name: str, type: str):
        self.name = name
        self.type = type

    def __str__(self):
        return self.name

    def __lt__(self, other):
        return self.name < other.name

    def get_name(self):
        return self.name

    def get_type(self):
        return self.type

class Predicate:
    def __init__(self, name: str, variable_types: list[str] = []):
        self.name = name
        self.variable_types = variable_types[:]

    def __str__(self):
        output = self.name + " " + str(self.variable_types)
        return output

    def __eq__(self, other):
        if isinstance(other, Predicate):
            return self.name == other.name
        return False

    def __hash__(self):
        return hash(self.name)

    def get_name(self):
        return self.name

    def get_variable_types(self):
        return self.variable_types

class Proposition:
    '''
    Implementation of a proposition, which is an instantiation of a predicate with the
    objects involved.
    '''
    def __init__(self, predicate: Predicate, objects: list[Object], index=-1):
        self.predicate = predicate
        self.objects = objects[:]
        self.name = self.__build_proposition_name()
        self.index = index

    def __str__(self):
        return self.name
    
    def __repr__(self) -> str:
        return self.name
    
    def __eq__(self, other):
        if isinstance(other, Proposition):
            return self.name == other.name
        return False

    def __build_proposition_name(self):
        names = ""
        for object in self.objects:
            names += "_" + object.get_name()
        names = self.predicate.get_name() + names
        return names

    def compare_names(self, prop_name: str):
        if prop_name == self.name:
            return True
        return False

    def get_predicate(self):
        return self.predicate

    def get_objects(self):
        return self.objects
    
    def get_index(self):
        return self.index
    
    def __lt__(self, other):
        return self.name < other.name

class Action:
    def __init__(self, name: str,
                 arguments: list[Object],
                 preconditions: list[(Proposition, bool)],
                 effects: list[list[(Proposition, bool)]]) -> None:
        self.name = name
        self.arguments = arguments
        self.preconditions = preconditions[:]
        self.effects = effects[:]

    def __str__(self):
        return self.name
    
    def get_name(self) -> str:
        return self.name
    
    def get_arguments(self) -> list[Object]:
        return self.arguments

    def get_preconditions(self) -> list[(Proposition, bool)]:
        return self.preconditions

    def get_effects(self) -> list[list[(Proposition, bool)]]:
        return self.effects