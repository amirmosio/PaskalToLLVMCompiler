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

        #### parse stack stuff ####
        self.grammar_right_left_hand_side_size = {'67': 2, '57': 2, '60': 2, '54': 4, '71': 3, '68': 5, '56': 8,
                                                  '65': 1, '64': 2, '58': 3, '66': 3, '62': 3, '70': 2, '74': 5}
        # 58 is 2 for declare without assignment but 3 for decignment:)))

        #### current token ####
        self.current_token = []

        #### arg counter ####
        self.arg_count = 0

        #### address allocated memory for array and variables ####
        # self.adrc = 0

    def declare_printf_to_result_code(self):
        code_index = self.result_code.add_top_code_line()
        code_line = self.result_code.get_line_code(code_index=code_index)
        code_line.result = "declare"
        code_line.optype = "i32"
        code_line.op1 = "@printf"
        code_line.op2 = "(" + "i32* , ..." + ")"

    def declare_scanf_to_result_code(self):
        code_index = self.result_code.add_top_code_line()
        code_line = self.result_code.get_line_code(code_index=code_index)
        code_line.result = "declare"
        code_line.optype = "i32"
        code_line.op1 = "@scanf"
        code_line.op2 = "(" + "i32* , ..." + ")"

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
            self.grammar_right_left_hand_side_size['70'] += 2
            self.ub()
        elif conceptual_routines == "cadscp":
            self.grammar_right_left_hand_side_size['70'] = 2
            self.cadscp()
        elif conceptual_routines == "funcdscp":
            self.grammar_right_left_hand_side_size['65'] += 1
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
            self.array()
        elif conceptual_routines == "jz":
            self.jz()
        elif conceptual_routines == "compjz":
            self.compjz()
        elif conceptual_routines == "jpcompjz":
            self.jpcompjz()
        elif conceptual_routines == "compjp":
            self.compjp()
        elif conceptual_routines == "pusharg":
            self.pusharg()
        elif conceptual_routines == 'callfunc':
            self.callfunc()
        elif conceptual_routines == 'retfunc':
            self.retfunc()
        elif conceptual_routines == "retdscp":
            self.retdscp()
        # there should be a lot if else here to call conceptual_routines functions

    def get_code(self):
        return self.result_code.code

    ####################################
    ######## conceptual_routines #######
    ###################################
    def push(self):
        self.semantic_stack.append(self.get_last_token().value)
        self.stp = self.get_last_token().value

    def retfunc(self):
        #### add return func code ####
        code_index = self.result_code.add_code_line()
        code_line = self.result_code.get_line_code(code_index=code_index)
        code_line.result = "ret"
        #### end code return ####

    def retdscp(self):
        ret_name_id = self.semantic_stack.pop()
        ret_value = None
        try:
            ret_value = int(ret_name_id)
        except:
            pass
        code_index = len(self.result_code.code) - 1
        code_line = self.result_code.get_line_code(code_index=code_index)
        if ret_value is None:
            code_line.op1 = "@" + ret_name_id
        else:
            code_line.op1 = ret_name_id

    def pusharg(self):
        # temp_name_id = self.symbol_table.declare_new_variable()
        # self.semantic_stack.append(temp_name_id)
        # temp_var = self.symbol_table.get_variable(temp_name_id)
        # const_value = self.get_pre_current_token().value
        #
        # #### assign constant code ####
        # code_index = self.result_code.add_code_line()
        # code_line = self.result_code.get_line_code(code_index=code_index)
        # code_line.result = "%" + temp_name_id
        # code_line.operation = "="
        # code_line.op1 = str(const_value)
        # #### end assign constant code ####

        self.arg_count += 1

    def callfunc(self):
        args = self.get_call_func_arg()
        self.arg_count = 0

        func_name = self.semantic_stack.pop()

        post_code_line, func_args = self.get_post_line_and_args_of_function(func_name=func_name, args=args)

        #### call func ####
        code_index = self.result_code.add_code_line()
        code_line = self.result_code.get_line_code(code_index)
        code_line.result = ""
        code_line.operation = "call"
        code_line.optype = ""
        code_line.op1 = self.convert_defined_function(func_name)
        code_line.op2 = "(" + func_args + ")"
        #### end call func ####
        if post_code_line is not None:
            self.result_code.add_code_line_object_with_index(post_code_line, False)

        pass

    def pushconst(self):
        temp_name_id = self.symbol_table.declare_new_variable()
        self.semantic_stack.append(temp_name_id)
        temp_var = self.symbol_table.get_variable(temp_name_id)
        temp_var.global_flag = True
        token = self.get_pre_current_token()
        temp_var.dsc = Models.SimpleVariableDSC()
        temp_var.dsc.type = self.convert_var_type(self.get_type_with_token_type(token))

        temp_var.dsc.size = len(str(token.value)) - 2

        #### assign constant code ####
        code_index = self.result_code.add_top_code_line()
        code_line = self.result_code.get_line_code(code_index=code_index)
        code_line.result = "@." + temp_name_id
        code_line.operation = "="
        code_line.op1 = self.convert_to_declare_token_value(token, temp_name_id)
        #### end assign constant code ####

    def switch(self):
        self.in_dcls_flag = not self.in_dcls_flag

    def begin_block(self):
        code_index = self.result_code.add_code_line()
        code_line = self.result_code.get_line_code(code_index=code_index)
        code_line.result = "{"

    def end_block(self):
        code_index = self.result_code.add_code_line()
        code_line = self.result_code.get_line_code(code_index=code_index)
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
        code_line.op1 = "@" + func_name_id
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
        code_line.op2 = ",align 4"
        #### end declare code ####

        if self.get_last_token().value == ";":
            self.grammar_right_left_hand_side_size['58'] = 2
            self.semantic_stack.pop()
        else:
            self.grammar_right_left_hand_side_size['58'] = 3

    def pop_declare_name_id(self):
        name_id = self.semantic_stack.pop()

    def adscp(self):
        array_dsc = Models.ArrayVariableDSC()
        # array_dsc.address = self.adrc
        self.semantic_stack.append(array_dsc)

    def ub(self):
        ub_name_id = self.get_last_token().value
        array_dsc = self.semantic_stack[-1]
        array_dsc.size.append(int(ub_name_id))

    def cadscp(self):
        array_dsc = self.semantic_stack.pop()
        array_dsc.type = self.get_pre_current_token().value
        # self.adrc += array_dsc.size * array_dsc.type_size
        array_name_id = self.semantic_stack[-1]
        array_name_id = self.symbol_table.declare_variable(array_name_id)
        array_var = self.symbol_table.get_variable(array_name_id)
        array_var.dsc = array_dsc

        #### array declare code ####
        code_index = self.result_code.add_code_line()
        code_line = self.result_code.get_line_code(code_index=code_index)
        code_line.result = array_var.get_name_id_in_llvm()
        code_line.operation = "="
        code_line.optype = "alloca"
        code_line.op1 = '[' + str(array_dsc.size[-1]) + ' x ' + self.convert_var_type(array_dsc.type) + ']'
        for i in range(len(array_dsc.size) - 2, -1, -1):
            code_line.op1 = "[" + str(array_dsc.size[i]) + "x" + code_line.op1 + "]"
        code_line.op1 += ","
        code_line.op2 = "align 16"
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
        code_line.result = '%' + temp_var.id

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
        var_res = self.symbol_table.get_variable(res_name_id)

        #### assign code ####
        code_index = self.result_code.add_code_line()
        code_line = self.result_code.get_line_code(code_index=code_index)
        code_line.result = '%' + name_id
        code_line.operation = "= add "
        code_line.optype = var_res.dsc.type
        code_line.op1 = '@' + res_name_id
        code_line.op2 = "," + str(0)
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

    def convert_defined_function(self, func_name):
        if func_name == "write":
            self.declare_printf_to_result_code()
            return "i32 (i8*,...)" + " @" + "printf"
        elif func_name == "read":
            self.declare_scanf_to_result_code()
            return "i32 (i8*,...)" + " @" + "scanf"
        else:
            return "@" + func_name

    def get_call_func_arg(self):
        result = ""
        for i in range(self.arg_count):
            arg = self.semantic_stack.pop()
            arg_var = self.symbol_table.get_variable(arg)
            result += arg_var.get_name_id_in_llvm() + ","
        if self.arg_count != 0:
            result = result[0:len(result) - 1]
        return result

    def get_type_with_token_type(self, token):
        token_type = None
        try:
            a = float(str(token.value))
            token_type = "cREAL"
        except:
            pass
        try:
            a = int(str(token.value))
            token_type = "cINTEGER"
        except:
            pass

        if token_type is None:
            token_type = "cSTRING"

        if token_type == "cINTEGER":
            return "integer"
        elif token_type == "cREAL":
            return "float"

    def convert_to_declare_token_value(self, token, temp_name):
        token_type = None
        try:
            a = float(str(token.value))
            token_type = "cREAL"
        except:
            pass
        try:
            a = int(str(token.value))
            token_type = "cINTEGER"
        except:
            pass

        if token_type is None:
            token_type = "cSTRING"

        if token_type == "cSTRING":
            return "private constant [" + str(len(token.value) - 1) + " x " + "i8" + "]" + " c " + str(
                token.value)[0:len(str(token.value)) - 1] + "\\00'"
        elif token_type == "cINTEGER":
            return "alloca i32, align 4" + "\n" + "store i32 " + str(token.value) + ", i32* @" + temp_name + ", align 4"
        elif token_type == "cREAL":
            return "alloca float, align 4" + "\n" + "store float " + str(
                token.value) + ",float* @" + temp_name + ",align 4"

    def get_post_line_and_args_of_function(self, func_name, args):
        if func_name == "write":
            string_temp_name = args[1:]
            string_temp_var = self.symbol_table.get_variable(string_temp_name)

            temp_name_id1 = self.symbol_table.declare_new_variable()
            temp_var1 = self.symbol_table.get_variable(temp_name_id1)
            temp_var1.global_flag = True
            code_line1 = Models.CodeLine()
            code_line1.result = "@" + "." + temp_name_id1
            code_line1.operation = "="
            code_line1.optype = "private constant"
            code_line1.op1 = " [3 x i8]"
            code_line1.op2 = "c\'%s\\00\'"

            temp_name_id2 = self.symbol_table.declare_new_variable()
            temp_var2 = self.symbol_table.get_variable(temp_name_id2)
            code_line2 = Models.CodeLine()
            code_line2.result = "%" + temp_name_id2
            code_line2.operation = "="
            code_line2.optype = "getelementptr inbounds [" + str(string_temp_var.dsc.size + 1) + " x i8],"
            code_line2.op1 = "[" + str(string_temp_var.dsc.size + 1) + " x i8]* " + args
            code_line2.op2 = ", i32 0, i32 0"

            temp_name_id3 = self.symbol_table.declare_new_variable()
            temp_var3 = self.symbol_table.get_variable(temp_name_id3)
            code_line3 = Models.CodeLine()
            code_line3.result = "%" + temp_name_id3
            code_line3.operation = "="
            code_line3.optype = "getelementptr inbounds [3 x i8],"
            code_line3.op1 = "[3 x i8]* " + "@" + temp_name_id1
            code_line3.op2 = ", i32 0, i32 0"

            self.result_code.add_code_line_object_with_index(code_line1, True)
            self.result_code.add_code_line_object_with_index(code_line2, False)
            self.result_code.add_code_line_object_with_index(code_line3, False)
            return None, "i8* " + "%" + temp_name_id3 + ", i8* " + "%" + temp_name_id1
        elif func_name == "read":
            temp_name_id1 = self.symbol_table.declare_new_variable()
            temp_var1 = self.symbol_table.get_variable(temp_name_id1)
            temp_var1.global_flag = True
            code_line1 = Models.CodeLine()
            code_line1.result = "@" + "." + temp_name_id1
            code_line1.operation = "="
            code_line1.optype = "private constant"
            code_line1.op1 = " [3 x i8]"
            code_line1.op2 = "c\"%d\\00\""

            temp_name_id2 = self.symbol_table.declare_new_variable()
            temp_var2 = self.symbol_table.get_variable(temp_name_id2)
            code_line2 = Models.CodeLine()
            code_line2.result = "%" + temp_name_id2
            code_line2.operation = "="
            code_line2.op1 = "alloca i32,"
            code_line2.op2 = "align 4"

            temp_name_id3 = self.symbol_table.declare_new_variable()
            temp_var3 = self.symbol_table.get_variable(temp_name_id3)
            code_line3 = Models.CodeLine()
            code_line3.result = "%" + temp_name_id3
            code_line3.operation = "="
            code_line3.optype = "getelementptr inbounds [3 x i8],"
            code_line3.op1 = "[3 x i8]* " + "@" + temp_name_id1
            code_line3.op2 = ", i32 0, i32 0"

            self.result_code.add_code_line_object_with_index(code_line1, True)
            self.result_code.add_code_line_object_with_index(code_line2, False)
            self.result_code.add_code_line_object_with_index(code_line3, False)

            temp_name_id4 = self.symbol_table.declare_new_variable()
            temp_var4 = self.symbol_table.get_variable(temp_name_id4)
            code_line4 = Models.CodeLine()
            code_line4.result = args
            code_line4.operation = "="
            code_line4.optype = "load"
            code_line4.op1 = "i32,i32* "
            code_line4.op2 = "%" + temp_name_id2
            return code_line4, "i8*" + temp_name_id3 + ",i32* " + args
        else:
            return None, args
