import lex as scanner

#################### test Strings ###################
data_test1 = '''
 3 + 4 * 10
   + -20 *2
 '''
data_test2 = "5*24"
data_test3 = "a:array[12 :10] int"
############### end Test Strings ####################

# Build the lexer and try it out
tokens = scanner.test(data_test3)  # Test it
