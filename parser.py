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
        self.current_token = None

    def read_next_token(self):
        token = self.tokens[self.token_index]
        self.current_token = token
        self.token_index += 1
        return token

    def parse_tokens(self):
        self.parse_table.push(1)
        self.read_next_token()

        grammar = self.get_parse_table_grammar(token_value=self.current_token.value)
        action = grammar[0]
        number = grammar[1]
        while action != "5":
            if action == "0":  # error
                pass
            elif action == "1":  # shift
                self.parse_stack.push(number)
                self.read_next_token()
            elif action == "2":  # goto ????
                self.parse_stack.push(number)
            elif action == "3":  # goto_push
                pass
            elif action == "4":  # reduce
                # doubt about 0 or 1 for left or right hand side
                self.code_generator.proceed_conceptual_routines(grammar[2])
                for i in range(self.grammar_right_left_hand_side_size[number][0]):
                    self.parse_stack.pop()
                # self.parse_stack.push(self.get_parse_table_grammar())
            elif action == "5":  # accept
                pass

    def get_parse_table_grammar(self, token_value):
        parse_stack_top = self.parse_stack.top()
        column_index = -1
        for i in range(len(self.syntactic_and_linguistic)):
            if self.syntactic_and_linguistic[i] == token_value:
                column_index = i
        return self.parse_table[parse_stack_top][column_index].split()
