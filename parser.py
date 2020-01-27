class Parser:
    def __init__(self, syntactic_and_linguistic, actions, parse_table):
        self.Syntactic_and_Linguistic = syntactic_and_linguistic
        self.actions = actions
        self.parse_table = parse_table

    def parse_tokens(self, tokens):
        for token in tokens:
            token_string = token
