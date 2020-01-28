class Variable:
    def __init__(self):
        self.name_id = None
        self.type = None


class SingleVariable(Variable):
    def __init__(self):
        self.value = None


class ArrayVariable(Variable):
    def __init__(self):
        self.array_address = None
        self.array_size = None


class SymbolTable:
    def __init__(self):
        self.variables = []

    def declare_variable(self):
        self.variables.append(Variable())
        return len(self.variable) - 1

    def get_variable(self, variable_address):
        return self.variables[variable_address]
