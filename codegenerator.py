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
        elif conceptual_routines == "minus":
            self.minus()
        elif conceptual_routines == "mult":
            self.mult()
        elif conceptual_routines == "divide":
            self.divide()
        elif conceptual_routines == "and":
            self.c_and()
        elif conceptual_routines == "or":
            self.c_or()
        elif conceptual_routines == "assign":
            self.assign()
        elif conceptual_routines == "array":
            self.assign()
        elif conceptual_routines == "jz":
            self.jz()
        elif conceptual_routines == "compjz":
            self.compjz()
        elif conceptual_routines == "jpcompjz":
            self.jpcompjz()
        elif conceptual_routines == "compjp":
            self.compjp()
        # there should be a lot if else here to call conceptual_routines functions
        pass

    def get_code(self):
        return self.result_code.code

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
        name_id_op1 = self.semantic_stack.pop()
        var_op1 = self.symbol_table.get_variable(name_id_op1)
        name_id_op2 = self.semantic_stack.pop()
        var_op2 = self.symbol_table.get_variable(name_id_op2)

        #### add code ####
        code_index = self.result_code.add_code_line()
        code_line = self.result_code.get_line_code(code_index=code_index)
        code_line.opcode = "+"
        code_line.op1 = var_op1.dsc.address
        code_line.op2 = var_op2.dsc.address
        temp_name_id = self.symbol_table.declare_new_variable()
        temp_var = self.symbol_table.get_variable(temp_name_id)
        code_line.res = temp_var.dsc.address
        #### end add code ####

        self.semantic_stack.append(temp_name_id)

    def minus(self):
        name_id_op1 = self.semantic_stack.pop()
        var_op1 = self.symbol_table.get_variable(name_id_op1)
        name_id_op2 = self.semantic_stack.pop()
        var_op2 = self.symbol_table.get_variable(name_id_op2)

        #### minus code ####
        code_index = self.result_code.add_code_line()
        code_line = self.result_code.get_line_code(code_index=code_index)
        code_line.opcode = "-"
        code_line.op1 = var_op2.dsc.address
        code_line.op2 = var_op1.dsc.address
        temp_name_id = self.symbol_table.declare_new_variable()
        temp_var = self.symbol_table.get_variable(temp_name_id)
        code_line.res = temp_var.dsc.address
        #### end minus code ####

        self.semantic_stack.append(temp_name_id)

    def mult(self):
        name_id_op1 = self.semantic_stack.pop()
        var_op1 = self.symbol_table.get_variable(name_id_op1)
        name_id_op2 = self.semantic_stack.pop()
        var_op2 = self.symbol_table.get_variable(name_id_op2)

        #### mult code ####
        code_index = self.result_code.add_code_line()
        code_line = self.result_code.get_line_code(code_index=code_index)
        code_line.opcode = "*"
        code_line.op1 = var_op1.dsc.address
        code_line.op2 = var_op2.dsc.address
        temp_name_id = self.symbol_table.declare_new_variable()
        temp_var = self.symbol_table.get_variable(temp_name_id)
        code_line.res = temp_var.dsc.address
        #### end mult code ####

        self.semantic_stack.append(temp_name_id)

    def divide(self):
        name_id_op1 = self.semantic_stack.pop()
        var_op1 = self.symbol_table.get_variable(name_id_op1)
        name_id_op2 = self.semantic_stack.pop()
        var_op2 = self.symbol_table.get_variable(name_id_op2)

        #### div code ####
        code_index = self.result_code.add_code_line()
        code_line = self.result_code.get_line_code(code_index=code_index)
        code_line.opcode = "/"
        code_line.op1 = var_op2.dsc.address
        code_line.op2 = var_op1.dsc.address
        temp_name_id = self.symbol_table.declare_new_variable()
        temp_var = self.symbol_table.get_variable(temp_name_id)
        code_line.res = temp_var.dsc.address
        #### end div code ####

        self.semantic_stack.append(temp_name_id)

    def c_and(self):
        name_id_op1 = self.semantic_stack.pop()
        var_op1 = self.symbol_table.get_variable(name_id_op1)
        name_id_op2 = self.semantic_stack.pop()
        var_op2 = self.symbol_table.get_variable(name_id_op2)

        #### and code ####
        code_index = self.result_code.add_code_line()
        code_line = self.result_code.get_line_code(code_index=code_index)
        code_line.opcode = "&&"  # TODO
        code_line.op1 = var_op1.dsc.address
        code_line.op2 = var_op2.dsc.address
        temp_name_id = self.symbol_table.declare_new_variable()
        temp_var = self.symbol_table.get_variable(temp_name_id)
        code_line.res = temp_var.dsc.address
        #### end and code ####

        self.semantic_stack.append(temp_name_id)

    def c_or(self):
        name_id_op1 = self.semantic_stack.pop()
        var_op1 = self.symbol_table.get_variable(name_id_op1)
        name_id_op2 = self.semantic_stack.pop()
        var_op2 = self.symbol_table.get_variable(name_id_op2)

        #### and code ####
        code_index = self.result_code.add_code_line()
        code_line = self.result_code.get_line_code(code_index=code_index)
        code_line.opcode = "||"  # TODO
        code_line.op1 = var_op1.dsc.address
        code_line.op2 = var_op2.dsc.address
        temp_name_id = self.symbol_table.declare_new_variable()
        temp_var = self.symbol_table.get_variable(temp_name_id)
        code_line.res = temp_var.dsc.address
        #### end and code ####

        self.semantic_stack.append(temp_name_id)

    def assign(self):
        # TODO
        pass

    def array(self):
        index_name_id = self.semantic_stack.pop()
        index_var = self.symbol_table.get_variable(index_name_id)
        index_var_address = index_var.dsc.address

        array_name_id = self.semantic_stack.pop()
        array_var = self.symbol_table.get_variable(array_name_id)
        type_size = array_var.dsc.type_size
        array_length = array_var.dsc.size
        array_first_address = array_var.dsc.address

        #### check array index out of rage ####
        code_index = self.result_code.add_code_line()
        code_line = self.result_code.get_line_code(code_index=code_index)
        code_line.opcode = "<"
        code_line.op1 = index_var_address
        code_line.op2 = "#" + str(array_length)
        code_line.res = "index_out_of_range"

        #### end checking index range ####

        #########################
        #### element_address ####
        code_index = self.result_code.add_code_line()
        code_line = self.result_code.get_line_code(code_index=code_index)
        code_line.opcode = "*"
        code_line.op1 = index_var_address
        code_line.op2 = "#" + str(type_size)
        temp_name_id = self.symbol_table.declare_new_variable()
        temp_var = self.symbol_table.get_variable(temp_name_id)
        code_line.res = temp_var.dsc.address

        code_index = self.result_code.add_code_line()
        code_line = self.result_code.get_line_code(code_index=code_index)
        code_line.opcode = "+"
        code_line.op1 = temp_var.dsc.address
        code_line.op2 = array_first_address
        code_line.res = temp_var.dsc.address
        self.semantic_stack.append(temp_name_id)
        #### end element address ####
        #############################
        pass

    def jz(self):
        boolean_name_id = self.semantic_stack.pop()
        boolean_var = self.symbol_table.get_variable(boolean_name_id)

        #### jz jump #####
        code_index = self.result_code.add_code_line()
        code_line = self.result_code.get_line_code(code_index=code_index)
        code_line.opcode = "jz"
        code_line.op1 = boolean_var.dsc.address
        #### end jz jump ####

        self.semantic_stack.append(code_index)

    def compjz(self):
        code_index = self.semantic_stack.pop()
        jz_code_line = self.result_code.get_line_code(code_index=code_index)
        jz_code_line.op2 = len(self.result_code.code)

    def jpcompjz(self):
        jump_code_index = self.result_code.add_code_line()
        jump_code_line = self.result_code.get_line_code(jump_code_index)
        jump_code_line.opcode = "jp"

        code_index = self.semantic_stack.pop()
        jz_code_line = self.result_code.get_line_code(code_index=code_index)
        jz_code_line.op2 = len(self.result_code.code)

        self.semantic_stack.append(jump_code_index)

    def compjp(self):
        jump_code_index = self.semantic_stack.pop()
        jump_code_line = self.result_code.get_line_code(code_index=jump_code_index)
        jump_code_line.op1 = len(self.result_code.code)

    #####################################
    ###### end conceptual routines ######
    #####################################

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
