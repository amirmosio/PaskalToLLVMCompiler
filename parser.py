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
        self.grammar_right_left_hand_side_size = {'67': 2, '57': 2, '60': 2, '54': 4, '71': 3, '68': 5, '56': 8,
                                                  '65': 2, '64': 2, '58': 3, '66': 3, '62': 3}
        # 58 is 2 for declare without assignment but 3 for decignment:)))
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
        self.code_generator.set_next_token(token)
        self.token_index += 1
        return token

    def parse_tokens(self):
        self.parse_stack.append(0)
        self.read_next_token()

        while True:
            grammar = self.get_parse_table_grammar(token=self.code_generator.get_last_token())
            action = grammar[0]
            number = int(grammar[1])

            if grammar[2] != "NoSem":
                self.code_generator.proceed_conceptual_routines(grammar[2][1:])
            if action == "0":  # error
                raise Exception("Syntax Error Occurred")
            elif action == "1":  # shift
                self.parse_stack.append(number)
                self.read_next_token()
            elif action == "2":  # goto ????
                self.parse_stack.append(number)
            elif action == "3":  # goto_push
                self.parse_stack.append(number)
                # self.read_next_token()
            elif action == "4":  # reduce
                # doubt about 0 or 1 for left or right hand side
                if number == 68:
                    while 59 >= self.parse_stack[-1] >= 56:
                        self.parse_stack.pop()
                else:
                    for i in range(self.grammar_right_left_hand_side_size[str(number)]):
                        self.parse_stack.pop()
                grammar = self.reduce_from_table(number)
                # action = grammar[0]
                number = int(grammar[1])
                self.parse_stack.append(number)
                if grammar[2] != "NoSem":
                    self.code_generator.proceed_conceptual_routines(grammar[2][1:])
            elif action == "5":  # accept
                break

    def get_parse_table_grammar(self, token):
        parse_stack_top = self.parse_stack[-1]
        column_index = -1
        for i in range(len(self.syntactic_and_linguistic)):
            if self.syntactic_and_linguistic[i] == token.value:
                column_index = i
                break
        if column_index == -1 or self.parse_table[parse_stack_top][column_index][0] == '-1':
            for i in range(len(self.syntactic_and_linguistic)):
                if self.syntactic_and_linguistic[i] == token.type:
                    column_index = i
                    break
        if column_index == -1:
            column_index = 21
        return self.parse_table[parse_stack_top][column_index]

    def reduce_from_table(self, reduced_index):
        parse_stack_top = self.parse_stack[-1]
        return self.parse_table[parse_stack_top][reduced_index]
