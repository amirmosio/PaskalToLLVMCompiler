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
        self.current_token = []

        #### address allocated memory for array and variables ####
        # self.adrc = 0

    def get_pre_current_token(self):
        return self.current_token[0]

    def get_last_token(self):
        return self.current_token[-1]

    def set_next_token(self, token):
        if len(self.current_token) == 2:
            del self.current_token[0]
            self.current_token.append(token)
        else:
            self.current_token.append(token)

    def proceed_conceptual_routines(self, conceptual_routines):
        if conceptual_routines == "push":
            self.push()
        elif conceptual_routines == "pushconst":
            self.pushconst()
        elif conceptual_routines == "switch":
            self.switch()
        elif conceptual_routines == "beginblock":
            self.begin_block()
        elif conceptual_routines == "endblock":
            self.end_block()
        elif conceptual_routines == "sdscp":
            self.sdscp()
        elif conceptual_routines == "adscp":
            self.adscp()
        elif conceptual_routines == "ub":
            self.ub()
        elif conceptual_routines == "cadscp":
            self.cadscp()
        elif conceptual_routines == "funcdscp":
            self.funcdscp()
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
        elif conceptual_routines == "not":
            self.c_not()
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
        self.semantic_stack.append(self.get_last_token().value)
        self.stp = self.get_last_token().value

    def pushconst(self):
        temp_name_id = self.symbol_table.declare_new_variable()
        self.semantic_stack.append(temp_name_id)
        temp_var = self.symbol_table.get_variable(temp_name_id)
        const_value = self.get_pre_current_token().value

        #### assign constant code ####
        code_index = self.result_code.add_code_line()
        code_line = self.result_code.get_line_code(code_index=code_index)
        code_line.result = "%" + temp_name_id
        code_line.operation = "="
        code_line.op1 = str(const_value)
        #### end assign constant code ####

    def switch(self):
        self.in_dcls_flag = not self.in_dcls_flag

    def begin_block(self):
        code_index = self.result_code.add_code_line()
        code_line = self.result_code.get_line_code(code_index=code_index)
        code_line.result = "{"

    def end_block(self):
        code_index = self.result_code.add_code_line()
        code_line = self.result_code.get_line_code()
        code_line.result = "}"

    def funcdscp(self):
        # argumentlist = self.semantic_stack.pop()
        argumentlist = '????'
        func_name_id = self.semantic_stack.pop()
        fdscp = Models.FunctionVariableDSC()
        fdscp.type = self.get_pre_current_token().value
        fdscp.argument_list = argumentlist

        func_name_id = self.symbol_table.declare_variable(func_name_id)
        func_var = self.symbol_table.get_variable(func_name_id)
        func_var.dsc = fdscp

        #### declare new function code ####
        code_index = self.result_code.add_code_line()
        code_line = self.result_code.get_line_code(code_index=code_index)

        code_line.result = 'define'
        code_line.optype = self.convert_var_type(fdscp.type)
        code_line.op1 = func_name_id
        code_line.op2 = "(" + self.convert_arguments(fdscp.argument_list) + " ) "
        #### end declare new function code ####

    def sdscp(self):
        simple_dsc = Models.SimpleVariableDSC()
        # simpleDSC.type = self.symbol_table.get_variable(self.stp).type # TODO recheck later
        var_type = self.get_pre_current_token().value
        simple_dsc.type = var_type
        name_id = self.semantic_stack[-1]
        name_id = self.symbol_table.declare_variable(name_id=name_id)
        var = self.symbol_table.get_variable(name_id)
        var.dsc = simple_dsc

        #### declare code ####
        code_index = self.result_code.add_code_line()
        code_line = self.result_code.get_line_code(code_index=code_index)
        code_line.result = '%' + name_id
        code_line.operation = '='
        code_line.optype = ' alloca '
        code_line.op1 = self.convert_var_type(var_type)
        #### end declare code ####

    def pop_declare_name_id(self):
        name_id = self.semantic_stack.pop()

    def adscp(self):
        array_dsc = Models.ArrayVariableDSC
        # array_dsc.address = self.adrc
        self.semantic_stack.append(array_dsc)

    def ub(self):
        ub_name_id = self.semantic_stack.pop()
        array_dsc = self.semantic_stack[-1]
        array_dsc.size = int(ub_name_id)

    def cadscp(self):
        # TODO
        array_dsc = self.semantic_stack.pop()
        array_dsc.type = self.current_token.value
        array_dsc.type_size = self.symbol_table.get_variable(self.current_token.value).dsc.size
        # self.adrc += array_dsc.size * array_dsc.type_size
        array_name_id = self.semantic_stack[-1]
        self.symbol_table.get_variable(array_name_id).dsc = array_dsc

        #### array declare code ####
        code_index = self.result_code.add_code_line()
        code_line = self.result_code.get_line_code(code_index=code_index)
        code_line.result = '%' + array_name_id
        code_line.operation = "alloca"
        code_line.op1 = '[' + array_dsc.size + ' * ' + self.convert_var_type(array_dsc.type) + ']'
        #### end array declare code ####

    def add(self):
        name_id_op1 = self.semantic_stack.pop()
        var_op1 = self.symbol_table.get_variable(name_id_op1)
        name_id_op2 = self.semantic_stack.pop()
        var_op2 = self.symbol_table.get_variable(name_id_op2)

        #### add code ####
        code_index = self.result_code.add_code_line()
        code_line = self.result_code.get_line_code(code_index=code_index)

        temp_name_id = self.symbol_table.declare_new_variable()
        temp_var = self.symbol_table.get_variable(temp_name_id)
        code_line.result = '%' + temp_var.id

        code_line.operation = 'add'
        code_line.optype = var_op1.dsc.type
        code_line.op1 = '%' + var_op1.id
        code_line.op2 = '%' + var_op2.id

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

        temp_name_id = self.symbol_table.declare_new_variable()
        temp_var = self.symbol_table.get_variable(temp_name_id)
        code_line.result = '%' + temp_var.id

        code_line.operation = "sub"
        code_line.optype = var_op1.dsc.type
        code_line.op1 = '%' + var_op2.id
        code_line.op2 = '%' + var_op1.id

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

        temp_name_id = self.symbol_table.declare_new_variable()
        temp_var = self.symbol_table.get_variable(temp_name_id)
        code_line.result = '%' + temp_var.id

        code_line.operation = 'mul'
        code_line.optype = var_op1.dsc.type
        code_line.op1 = '%' + var_op1.id
        code_line.op2 = '%' + var_op2.id

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

        temp_name_id = self.symbol_table.declare_new_variable()
        temp_var = self.symbol_table.get_variable(temp_name_id)
        code_line.res = '%' + temp_var.id

        code_line.operation = 'div'
        code_line.optype = var_op1.dsc.type
        code_line.op1 = '%' + var_op2.id
        code_line.op2 = '%' + var_op1.id

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

        temp_name_id = self.symbol_table.declare_new_variable()
        temp_var = self.symbol_table.get_variable(temp_name_id)
        code_line.result = '%' + temp_var.id

        code_line.operation = "&&"  # TODO
        code_line.optype = var_op1.dsc.type
        code_line.op1 = '%' + var_op1.id
        code_line.op2 = '%' + var_op2.id
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

        temp_name_id = self.symbol_table.declare_new_variable()
        temp_var = self.symbol_table.get_variable(temp_name_id)
        code_line.result = '%' + temp_var.id

        code_line.operation = "||"  # TODO
        code_line.optype = var_op1.dsc.type
        code_line.op1 = var_op1.id
        code_line.op2 = var_op2.id
        #### end and code ####

        self.semantic_stack.append(temp_name_id)

    def c_not(self):
        # TODO
        pass

    def assign(self):
        res_name_id = self.semantic_stack.pop()
        name_id = self.semantic_stack.pop()

        #### assign code ####
        code_index = self.result_code.add_code_line()
        code_line = self.result_code.get_line_code(code_index=code_index)
        code_line.result = '%' + name_id
        code_line.operation = "="
        code_line.op1 = '%' + res_name_id
        #### end assign code ####

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

    def convert_var_type(self, var_type):
        if var_type == "integer":
            return "i32"
        elif var_type == "long":
            return 'i1000'
        elif var_type == "float":
            return 'float'
        # TODO

    def convert_arguments(self, argument_list):
        # TODO
        return ""
