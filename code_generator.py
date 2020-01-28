from _collections import deque


class Code_Generator:
    def __init__(self):
        self.Code = []

        #### semantic stack stuff ####
        self.semantic_stack = deque()

    def proceed_conceptual_routines(self, conceptual_routines):
        if conceptual_routines == "push":
            self.push()
        elif conceptual_routines == "switch":
            pass
        elif conceptual_routines == "sdscp":
            pass
        elif conceptual_routines == "adscp":
            pass
        elif conceptual_routines == "ub":
            pass
        elif conceptual_routines == "cadscp":
            pass
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
        pass

    def switch(self):
        pass

    def sdscp(self):
        pass

    def adscp(self):
        pass

    def ub(self):
        pass

    def cadscp(self):
        pass
