import ply.lex as lex

# reserved words
reserved = {
    'if' : 'IF',
    'var': 'VAR',
    'else' : 'ELSE',
    'program' : 'PROGRAM',
    'int' : 'INT',
    'float': 'FLOAT',
    'class': 'CLASS',
    'string': 'STRING',
    'char': 'CHAR',
    'main': 'MAIN',
    'void': 'VOID',
    'inherits': 'INHERITS',
    'return': 'RETURN',
    'write': 'WRITE',
    'read': 'READ',
    'while': 'WHILE',
    'for': 'FOR',
    'open': 'OPEN',
    'close': 'CLOSE',
    'file': 'FILE',
    'to': 'TO',
    'function': 'FUNCTION',
    'functions': 'FUNCTIONS',
    'do': 'DO',
}

# List of token names.   This is always required
tokens = [
    'ID',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'GREATER',
    'GREATEROREQUAL',
    'LESSOREQUAL',
    'LESS',
    'NOTEQUAL',
    'LBRACKET',
    'RBRACKET',
    'LSQRBRACKET',
    'RSQRBRACKET',
    'LPAREN',
    'RPAREN',
    'SEMICOLON',
    'COLON',
    'EQUALS',
    'EQUAL',
    'COMMA',
    'AND',
    'OR',
    'DOT',
    'CTEI',
    'CTEF',
    'CTESTRING'
] + list(reserved.values())

# Regular expression rules for simple tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_GREATER = r'>'
t_GREATEROREQUAL = r'>='
t_LESS = r'<'
t_LESSOREQUAL = r'<='
t_LBRACKET = r'\{'
t_RBRACKET = r'\}'
t_LSQRBRACKET = r'\['
t_RSQRBRACKET = r'\]'
t_SEMICOLON = r'\;'
t_COLON = r'\:'
t_EQUALS = r'\='
t_COMMA = r'\,'
t_CTESTRING = r'\".*\"'
t_EQUAL = r'\=='
t_NOTEQUAL = r'\!='
t_AND = r'\&&'
t_OR = r'\|\|'
t_DOT = r'\.'

# REGEX

#Define an ID
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# Define a constant float
def t_CTEF(t):
    r'[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t

# Define a constant int
def t_CTEI(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t


# # Define a constant string
# def t_CTESTRING(t):
#     r'\"([^\\\"]|\\.)*\"'
#     return t

# Define a rule so we can track line numbers
def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()