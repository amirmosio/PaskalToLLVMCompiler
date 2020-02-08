# # ------------------------------------------------------------
# # calclex.py
# #
# # tokenizer for a simple expression evaluator for
# # numbers and +,-,*,/
# # ------------------------------------------------------------
import re

import ply.lex as lex
from ply.lex import TOKEN

rsv_sys_function = ["main", "read", "write", "strlen"]
rsv_sys_type = ["array", "boolean", "string", "char", "integer", "real"]
rsv_sys_con = ["false", "true"]
rsv_other = ["assign", "break", "begin", "continue", "do", "else", "end", "function", "procedure", "if", "of",
             "return",
             "while", "var"]

reserved = {}
reserved_type = {}
for w in rsv_sys_function:
    reserved[w] = 'SYS_FUNCT'
    # reserved_type[w]='f'+w.upper()
    reserved_type[w] = 'SYS_FUNCT'

for w in rsv_sys_con:
    reserved[w] = 'SYS_CON'
    # reserved_type[w]='c'+w.upper()
    reserved_type[w] = 'cSYS_CON'

for w in rsv_sys_type:
    reserved[w] = 'SYS_TYPE'
    # reserved_type[w]='c'+w.upper()
    reserved_type[w] = 'c' + 'SYS_TYPE'

for w in rsv_other:
    reserved[w] = 'k' + w.upper()
    reserved_type[w] = 'k' + w.upper()

tokens = (
    'cCHAR', 'cINTEGER', 'cREAL', 'cBOO', 'cSTRING', 'oLP', 'oRP', 'oLB', 'oRB', 'oPLUS', 'oMINUS',
    'oMUL', 'oDIV', 'oASSIGN', 'oEQUAL', 'oLT', 'oGT', 'oLE', 'oGE', 'oUN_EQU', 'oCOMMA', 'oSEMI',
    'oCOLON', 'oQUOTE', 'oDOT_DOT', 'oDOT', 'id', 'oAND', 'oOR', 'oXOR', 'oLOGICAL_AND', 'oLOGICAL_OR', 'oMOD',
    "oLOGICAL_NOT", "oUNARY_MINUS"
)
tokens += tuple(list(set(reserved_type.values())))

############ Rules ###############
letter = r"[a-zA-Z_]"
alnum = r"[_a-zA-Z0-9]"
dec = r"[0-9]"
hex = r"[0-9a-fA-F]"


# c_INTEGER
@TOKEN(r'[1-9]' + dec + r'*')
def t_cINTEGER_10(t):
    t.value = int(t.value, 10)
    t.type = 'cINTEGER'
    return t


@TOKEN(r'0(x|X)' + hex + r'+')
def t_cINTEGER_16(t):
    t.value = int(t.value, 16)
    t.type = 'cINTEGER'
    return t


@TOKEN(dec + r'+(\.' + dec + r'+)?([E|e][+\-]?' + dec + r'+)?')
def t_cREAL(t):
    return t


t_cCHAR = r"'([^']|\")'"
# t_cSTRING = r"\'(\\.|[^\'])(\\.|[^\'])+\'"
t_cSTRING = r"\'[^']*\'"

# bitwise
t_oAND = re.escape(r'&')
t_oOR = re.escape(r'|')
t_oXOR = re.escape(r'^')
# logic
t_oLOGICAL_AND = re.escape(r'and')
t_oLOGICAL_OR = re.escape(r'or')
# arithmetic
t_oPLUS = re.escape(r'+')
t_oMINUS = re.escape(r'-')
t_oMUL = re.escape(r'*')
t_oDIV = re.escape(r'/')
t_oMOD = re.escape(r'%')
# compare
t_oEQUAL = re.escape(r'=')
t_oLT = re.escape(r'<')
t_oGT = re.escape(r'>')
t_oLE = re.escape(r'<=')
t_oGE = re.escape(r'>=')
t_oUN_EQU = re.escape(r'<>')
# unary
t_oUNARY_MINUS = re.escape(r'-')
t_oLOGICAL_NOT = re.escape(r'~')

t_oLP = re.escape(r'(')
t_oRP = re.escape(r')')
t_oLB = re.escape(r'[')
t_oRB = re.escape(r']')

t_oASSIGN = re.escape(r':=')
t_oCOMMA = re.escape(r',')
t_oSEMI = re.escape(r';')
t_oCOLON = re.escape(r':')
t_oQUOTE = re.escape(r"'")
t_oDOT_DOT = re.escape(r'..')
t_oDOT = re.escape(r'.')


@TOKEN(letter + alnum + r'*')
def t_ID_or_KEYWORD(t):
    global reserved
    if t.value in reserved.keys():
        t.type = reserved_type[t.value]
        return t
    t.type = 'id'
    return t


#######################

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


###########Action Rules##############
#####################################
# A regular expression rule with some action code

# Note addition of self parameter since we're in a class
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


#####################################
#####################################
# Build the lexer
lexer = lex.lex()


# Test it output
def test(data):
    result = []
    global lexer
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        result.append(tok)
        # print(tok)
    return result
