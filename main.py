import lex as scanner

#################### test Strings ###################
data_test1 = '''
 3 + 4 * 10
   + -20 *2
 '''
data_test2 = "5*24"
data_test3 = "a:array[ 12     :10] integer"


############### end Test Strings ####################


def get_parse_table_detail():
    actions = {0: "error", 1: "shift", 2: "goto", 3: "goto_push", 4: "reduce", 5: "accept"}
    file = open("/media/amir/Program/Documentwork/ProjectCode/Python Project/PaskalToLLVMCompiler/ParseTable.npt", "r")
    n, m = file.readline().split()
    n = int(n)
    m = int(m)
    toekns = file.readline().split()
    parse_table = []
    for i in range(n):
        row = file.readline().split("NoSem")
        parse_table.append(row)
    return toekns, actions, parse_table


# Build the lexer and try it out
tokens = scanner.test(data_test3)  # Test it
Syntactic_and_Linguistic, actions, parse_table = get_parse_table_detail()
