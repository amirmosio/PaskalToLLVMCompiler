from _collections import deque

import Models
import code_generator


class Parser:
    def __init__(self, syntactic_and_linguistic, actions, parse_table):
        self.code_generator = code_generator.Code_Generator()

        #### parse table stuff ####
        self.syntactic_and_linguistic = syntactic_and_linguistic
        self.actions = actions
        self.parse_table = parse_table

        #### parse stack stuff ####
        self.grammar_right_left_hand_side_size = []
        self.parse_stack = deque()

        #### semantic stack stuff ####
        self.semantic_stack = deque

        #### symbol table stuff ####
        self.symbol_table = Models.SymbolTable

    def parse_tokens(self, tokens):
        self.parse_table.push(1)
        for token in tokens:
            grammar = self.get_parse_table_grammar(word=token.value)
            action_type = grammar[0]
            grammar_number = grammar[1]
            self.proceed_next_parse_state(action_type=action_type, grammar_number=grammar_number)
            conceptual_routines = None
            if len(grammar) == 3:
                conceptual_routines = grammar[2]
                self.proceed_conceptual_routines(conceptual_routines=conceptual_routines)

    def get_parse_table_grammar(self, word):
        parse_stack_top = self.parse_stack.top()
        column_index = -1
        for i in range(len(self.syntactic_and_linguistic)):
            if self.syntactic_and_linguistic[i] == word:
                column_index = i
        return self.parse_table[parse_stack_top][column_index].split()

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

    def proceed_next_parse_state(self, action_type, grammar_number):
        if action_type == "0":  # error
            pass
        elif action_type == "1":  # shift
            self.parse_stack.push(grammar_number)
        elif action_type == "2":  # goto
            pass
        elif action_type == "3":  # goto_push
            pass
        elif action_type == "4":  # reduce
            # doubt about 0 or 1 for left or right hand side
            for i in range(self.grammar_right_left_hand_side_size[grammar_number][0]):
                self.parse_stack.pop()
        elif action_type == "5":  # accept
            pass

    def push(self):
        pass
