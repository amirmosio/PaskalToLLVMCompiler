from _collections import deque

import Models


class CodeGenerator:
    def __init__(self):
        self.Code = []

        #### semantic stack stuff ####
        self.semantic_stack = deque()

        #### symbol table stuff ####
        self.symbol_table = Models.SymbolTable()
        self.stp = None

        #### DCLS flag ####
        self.in_dcls_flag = True

        #### current token ####
        self.current_token = None

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
        # there should be a lot if else here to call conceptual_routines functions
        pass

    def get_code(self):
        return self.Code

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
        simple_dsc.type = self.symbol_table.get_variable(self.current_token.value).type
        self.symbol_table.get_variable(self.stp).dsc = simple_dsc
        self.semantic_stack.pop()

    def adscp(self):
        # TODO
        pass

    def ub(self):
        # TODO
        pass

    def cadscp(self):
        # TODO
        pass

    def add(self):
        # TODO
        pass

    def multi(self):
        # TODO
        pass
    def

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
