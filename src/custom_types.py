class Object:
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __str__(self):
        return self.name

class Predicate:
    def __init__(self, name, variable_types = []):
        self.name = name
        self.variable_types = variable_types[:]

    def __str__(self):
        output = self.name + " " + str(self.variable_types)
        return output