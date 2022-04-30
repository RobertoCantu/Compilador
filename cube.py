'''

INT INT     --> INT
INT FLOAT   --> FLOAT
INT CHAR    --> ERROR
INT STRING  --> ERROR

FLOAT INT     --> FLOAT
FLOAT FLOAT   --> FLOAT
FLOAT CHAR    --> ERROR
FLOAT STRING  --> ERROR

CHAR INT     --> ERROR
CHAR FLOAT   --> ERROR
CHAR CHAR    --> CHAR
CHAR STRING  --> STRING

STRING INT     --> ERROR
STRING FLOAT   --> ERROR
STRING CHAR    --> STRING
STRING STRING  --> STRING


{
    'INT': {
        'INT': {
            'PLUS': {

            },
            'MINUS': {

            },
            'MULT':{

            },
            'DIVIDE': {
                
            }

        },
        'FLOAT': {

        },
        'CHAR': {

        }
    }
}

'''