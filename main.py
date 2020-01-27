import lex as scanner

#################### test Strings ###################
data_test1 = '''
 3 + 4 * 10
   + -20 *2
 '''
data_test2 = "5*24"
data_test3 = "a:array[ 12     :10] integer"
############### end Test Strings ####################

# Build the lexer and try it out
tokens = scanner.test(data_test3)  # Test it


def get_parse_table():
    file = open()
    n, m = file.readline().split()
    n = int(n)
    m = int(m)
    toekns = file.readline().split()
    parse_table = []
    for i in range(n):
        row = file.readline().split("noSem")
        parse_table.
