class Variable:
    def __init__(self):
        self.id = None
        self.idk = None  # simple array type
        self.dsc = None  # a descriptor for more detail of variables one of below DSC


class SimpleVariableDSC:
    def __init__(self):
        self.am = None  # immediate ...
        self.type = None  # integer real float ....


class ArrayVariableDSC:
    def __init__(self):
        self.am = None  # immediate ...
        self.address = None  # address location in memory
        self.size = None  # n element size
        self.type = None  # integer real float element
        self.type_size = None  # n bytes


class FunctionVariableDSC:
    def __init__(self):
        self.pc_address = None
        self.argument_list = None
        self.call_pc_address = []


class TypeDSC:
    def __init__(self):
        self.type = None
        self.size = None


class SymbolTable:
    def __init__(self):
        self.variables = {}
        self.variable_counter = 0

    def declare_variable(self, name_id):
        old_value = self.variables.get(name_id, "undefined")
        if old_value == "undefined":
            var = Variable()
            var.id = name_id
            self.variables[name_id] = var
            return name_id
        else:
            return -1

    def get_variable(self, name_id):
        return self.variables.get(name_id, "undefined")

    def get_variable(self, variable_address):
        return self.variables[variable_address]

    def declare_new_variable(self):
        name_id = "compiler_temp_variable" + str(self.variable_counter)
        self.variable_counter += 1
        return self.declare_variable(name_id=name_id)


class ResultCode:
    def __init__(self):
        self.code = []

    def add_code_line(self):
        code_line = CodeLine()
        self.code.append(code_line)
        return len(self.code) - 1

    def get_line_code(self, code_index):
        if code_index >= len(self.code):
            raise Exception("Line Code Index Error Occurred")
        else:
            return self.code[code_index]

    def set_opcode(self, code_index, opcode):
        self.code.opcode = opcode

    def set_op1(self, code_index, op1):
        self.code.op1 = op1

    def set_op2(self, code_index, op2):
        self.code.op2 = op2

    def set_result(self, code_index, res):
        self.code.res = res


class Grammar:
    def __init__(self):
        self.rhsl
        self.lhs


class CodeLine:
    def __init__(self):
        self.result = ""
        self.operation = ""
        self.optype = ""
        self.op1 = ""
        self.op2 = ""

    def __str__(self):
        return self.result + " " + self.operation + " " + self.optype + " " + self.op1 + " " + self.op2
