from _collections import deque
import code_generator


class Parser:
    def __init__(self, syntactic_and_linguistic, actions, parse_table):
        self.code_generator = code_generator.Code_Generator()

        self.syntactic_and_linguistic = syntactic_and_linguistic
        self.actions = actions
        self.parse_table = parse_table

        self.grammar_right_left_hand_side_size = []
        self.parse_stack = deque()

    def get_code_generated(self):
        return self.code_generator.get_code()

    def get_parse_table_grammar(self, word):
        parse_stack_top = self.parse_stack.top()
        column_index = -1
        for i in range(len(self.syntactic_and_linguistic)):
            if self.syntactic_and_linguistic[i] == word:
                column_index = i
        return self.parse_table[parse_stack_top][column_index].split()

    def parse_tokens(self, tokens):
        self.parse_table.push(1)
        for token in tokens:
            grammar = self.get_parse_table_grammar(token.value)
