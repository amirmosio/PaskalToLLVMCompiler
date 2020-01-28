class Variable:
    def __init__(self):
        self.id = None
        self.idk = None  # simple array type
        self.dsc = None  # a descriptor for more detail of variables one of below DSC


class SimpleVariableDSC:
    def __init__(self):
        self.am = None  # immediate ...
        self.address = None  # address location in memory
        self.type = None  # integer real float ....
        self.size = None  # n bytes


class ArrayVariableDSC:
    def __init__(self):
        self.am = None  # immediate ...
        self.address = None  # address location in memory
        self.size = None  # n element size
        self.type = None  # integer real float element
        self.type_size = None  # n bytes


class TypeDSC:
    def __init__(self):
        self.type = None
        self.size = None


class SymbolTable:
    def __init__(self):
        self.variables = {}

    def declare_variable(self, id):
        self.variables.push(id, Variable())
        return id

    def get_variable(self, variable_address):
        return self.variables[variable_address]


class Grammar:
    def __init__(self):
        self.rhsl
        self.lhs
