from _collections import deque

import Models


class CodeGenerator:
    def __init__(self):
        self.result_code = Models.ResultCode()

        #### semantic stack stuff ####
        self.semantic_stack = deque()

        #### symbol table stuff ####
        self.symbol_table = Models.SymbolTable()
        self.stp = None

        #### DCLS flag ####
        self.in_dcls_flag = True

        #### current token ####
        self.current_token = None

        #### address allocated memory for array and variables ####
        self.adrc = 0

    def proceed_conceptual_routines(self, conceptual_routines):
        if conceptual_routines == "push":
            self.push()
        elif conceptual_routines == "switch":
            self.switch()
        elif conceptual_routines == "sdscp":
            self.sdscp()
        elif conceptual_routines == "adscp":
            self.adscp()
        elif conceptual_routines == "ub":
            self.ub()
        elif conceptual_routines == "cadscp":
            self.cadscp()
        elif conceptual_routines == "add":
            self.add()
        elif conceptual_routines == "mult":
            self.mult()
        elif conceptual_routines == "assign":
            self.assign()
        elif conceptual_routines == "array":
            self.assign()
        # there should be a lot if else here to call conceptual_routines functions
        pass

    def get_code(self):
        return self.result_code.code

    def add_code(self, code_line):
        self.Code.append(code_line)

    ####################################
    ######## conceptual_routines #######
    ###################################
    def push(self):
        self.semantic_stack.append(self.stp)

    def switch(self):
        self.in_dcls_flag = not self.in_dcls_flag

    def sdscp(self):
        simple_dsc = Models.SimpleVariableDSC
        # simpleDSC.type = self.symbol_table.get_variable(self.stp).type # TODO recheck later
        var_type = self.symbol_table.get_variable(self.current_token.value)
        simple_dsc.type = var_type.dsc.type
        simple_dsc.address = self.adrc
        simple_dsc.size = var_type.dsc.size
        self.adrc += simple_dsc.size
        name_id = self.semantic_stack.pop()
        self.symbol_table.get_variable(name_id=name_id).dsc = simple_dsc

    def adscp(self):
        array_dsc = Models.ArrayVariableDSC
        array_dsc.address = self.adrc
        self.semantic_stack.append(array_dsc)

    def ub(self):
        if int(self.current_token.value) < 1:
            raise Exception("Array Size Error Occurred")
        else:
            array_dsc = self.semantic_stack[-1]
            array_dsc.size = int(self.current_token.value)

    def cadscp(self):
        array_dsc = self.semantic_stack.pop()
        array_dsc.type = self.current_token.value
        array_dsc.type_size = self.symbol_table.get_variable(self.current_token.value).dsc.size
        self.adrc += array_dsc.size * array_dsc.type_size
        array_name_id = self.semantic_stack.pop()
        self.symbol_table.get_variable(array_name_id).dsc = array_dsc

    def add(self):
        # TODO
        pass

    def mult(self):
        # TODO
        pass

    def assign(self):
        # TODO
        pass

    def array(self):
        index_name_id = self.semantic_stack.pop()
        array_name_id = self.semantic_stack.pop()
        # var =
        pass

    def fkw(self, string):
        var = self.symbol_table.get_variable(string)
        if var.idk != "reservedword":  # TODO
            if self.in_dcls_flag:
                if self.symbol_table.get_variable(string) == "undefined":
                    self.stp = self.symbol_table.declare_variable(string)
                else:
                    raise Exception("Error Occurred")
            else:
                if self.symbol_table.get_variable(string) == "undefined":
                    raise Exception("Error Occurred")
                else:
                    self.stp = string
