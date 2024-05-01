class Object:
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __str__(self):
        return self.name

class Predicate:
    def __init__(self, name, type_variables = []):
        self.name = name
        self.type_variables = type_variables[:]

    def __str__(self):
        return self.name