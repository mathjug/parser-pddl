class Object:
    def __init__(self, name: str, type: str):
        self.name = name
        self.type = type

    def __str__(self):
        return self.name
    
    def get_name(self):
        return self.name

    def get_type(self):
        return self.type
    
    def __lt__(self, other):
        return self.name < other.name

class Predicate:
    def __init__(self, name: str, variable_types: list = []):
        self.name = name
        self.variable_types = variable_types[:]

    def __str__(self):
        output = self.name + " " + str(self.variable_types)
        return output
    
    def get_name(self):
        return self.name
    
    def get_variable_types(self):
        return self.variable_types

class Proposition:
    '''
    Implementation of a proposition, which is an instantiation of a predicate with the
    objects involved.
    '''
    def __init__(self, predicate: Predicate, objects: list):
        self.predicate = predicate
        self.objects = objects

    def __str__(self):
        output = self.__get_object_names()
        return output
    
    def __get_object_names(self):
        names = ""
        for object in self.objects:
            names += "_" + object.get_name()
        names = self.predicate.get_name() + names
        return names
    
    def compare_names(self, prop_names: str):
        if prop_names == self.__get_object_names():
            return True
        return False

    def get_predicate(self):
        return self.predicate

    def get_objects(self):
        return self.objects