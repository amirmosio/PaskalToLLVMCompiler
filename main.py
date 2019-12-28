import lex as scanner

#################### test Strings ###################
data_test1 = '''
 3 + 4 * 10
   + -20 *2
 '''
data_test2 = "5*24"
############### end Test Strings ####################

# Build the lexer and try it out
scanner.test(data_test2)  # Test it
