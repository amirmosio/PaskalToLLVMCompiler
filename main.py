import lex as scanner
import parser

#################### test Strings ###################
file = open("input/in1.txt", "r")
input_code = ""
for line in file:
    input_code += line

file.close()


############### end Test Strings ####################


def get_parse_table_detail():
    actions = {0: "error", 1: "shift", 2: "goto", 3: "goto_push", 4: "reduce", 5: "accept"}
    file = open("ParseTable.npt", "r")
    n, m = file.readline().split()
    n = int(n)
    m = int(m)
    parse_table = []
    tokens = file.readline().split()
    parse_table.append(tokens)
    for i in range(n):
        row = file.readline().split()
        grammars_row = [None] * (len(row) // 3)
        for i in range(0, len(row), 3):
            grammar = []
            index = i // 3
            grammar.append(row[i])
            grammar.append(row[i + 1])
            grammar.append(row[i + 2])
            grammars_row[index] = grammar
        parse_table.append(grammars_row)
    return tokens, actions, parse_table


# Build the lexer and try it out


tokens = scanner.test(input_code)  # Test it
Syntactic_and_Linguistic, actions, parse_table = get_parse_table_detail()
parser = parser.Parser(Syntactic_and_Linguistic, actions, parse_table, tokens=tokens)
parser.parse_tokens()
print(parser.code_generator.get_code())  # this is the output code
