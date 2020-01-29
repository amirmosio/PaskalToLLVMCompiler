from _collections import deque

import codegenerator


class Parser:
    def __init__(self, syntactic_and_linguistic, actions, parse_table, tokens):
        self.code_generator = codegenerator.CodeGenerator()

        #### parse table stuff ####
        self.syntactic_and_linguistic = syntactic_and_linguistic
        self.actions = actions
        self.parse_table = parse_table

        #### parse stack stuff ####
        self.grammar_right_left_hand_side_size = []
        self.parse_stack = deque()

        #### next token ####
        self.tokens = tokens
        self.token_index = 0
        self.declare_all_variables()

    def declare_all_variables(self):
        for token in self.tokens:
            if token.value == "function":
                break
            if token.value == ":":
                self.code_generator.in_dcls_flag = False
            if self.code_generator.in_dcls_flag:
                status = self.code_generator.symbol_table.declare_variable(name_id=token.value)
                if status == -1:
                    raise Exception("Variable has been defined before.")

            if token.value == ";":
                self.code_generator.in_dcls_flag = True

    def read_next_token(self):
        token = self.tokens[self.token_index]
        self.code_generator.current_token = token
        self.token_index += 1
        return token

    def parse_tokens(self):
        self.parse_stack.append(1)
        self.read_next_token()

        while True:

            grammar = self.get_parse_table_grammar(token_type=self.code_generator.current_token.type)
            action = grammar[0]
            number = int(grammar[1])

            if action == "0":  # error
                raise Exception("Syntax Error Occurred")
            elif action == "1":  # shift
                self.parse_stack.append(number)
                self.read_next_token()
            elif action == "2":  # goto ????
                self.parse_stack.append(number)
            elif action == "3":  # goto_push
                pass
            elif action == "4":  # reduce
                # doubt about 0 or 1 for left or right hand side
                self.code_generator.proceed_conceptual_routines(grammar[2])
                for i in range(self.grammar_right_left_hand_side_size[number][0]):
                    self.parse_stack.pop()
                # self.parse_stack.append(self.get_parse_table_grammar())
            elif action == "5":  # accept
                break

    def get_parse_table_grammar(self, token_type):
        parse_stack_top = self.parse_stack[-1]
        column_index = -1
        for i in range(len(self.syntactic_and_linguistic)):
            if self.syntactic_and_linguistic[i] == token_type:
                column_index = i
        if column_index == -1:
            raise Exception("Syntax Error Occurred")
        return self.parse_table[parse_stack_top][column_index]
