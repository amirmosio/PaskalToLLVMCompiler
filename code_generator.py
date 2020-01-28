class Code_Generator:
    def __init__(self):
        self.Code = []

    def get_code(self):
        return self.Code

    def add_code(self, code_line):
        self.Code.append(code_line)
