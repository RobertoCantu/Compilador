'''

TYPE
+ 
-
*
/
=

BOOLEAN
== 
&& 
<
<=
>
>=
!=
||

response = cubo[int][int][*]

'''


SEMANTIC = {
    # INT
    'int': {
        'int': {
            '+': 'int',
            '-': 'int',
            '*': 'int',
            '/': 'int',
            '=': 'int',
            '==': 'bool',
            '!=': 'bool',
            '>': 'bool',
            '>=': 'bool',
            '<': 'bool',
            '<=': 'bool',
        },
        'float': {
            '+': 'float',
            '-': 'float',
            '*': 'float',
            '/': 'float',
            '==': 'bool',
            '!=': 'bool',
            '>': 'bool',
            '>=': 'bool',
            '<': 'bool',
            '<=': 'bool',
        },
    },
    # FLOAT
    'float': {
        'int': {
            '+': 'float',
            '-': 'float',
            '*': 'float',
            '/': 'float',
            '=': 'float',
            '==': 'bool',
            '!=': 'bool',
            '>': 'bool',
            '>=': 'bool',
            '<': 'bool',
            '<=': 'bool',
        },
        'float': {
            '+': 'float',
            '-': 'float',
            '*': 'float',
            '/': 'float',
            '=': 'float',
            '==': 'bool',
            '!=': 'bool',
            '>': 'bool',
            '>=': 'bool',
            '<': 'bool',
            '<=': 'bool',
        },
    },
    # CHAR
    'char': {
        'char': {
            '=': ' char',
            '==': 'bool',
            '!=': 'bool',
        },
    },
    # STRING
    'string': {
        'string': {
            '=': 'string',
            '==': 'bool',
            '!=': 'bool',
        },
    },
    # BOOL
    'bool': {
        'bool': {
            '&&': 'bool',
            '||': 'bool', 
        },
    },
}

