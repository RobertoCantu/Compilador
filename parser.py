import sys
import ply.yacc as yacc
from lexer import tokens

def p_program(p):
	'''
	program : PROGRAM ID SEMICOLON program2 program3 program4 MAIN LBRACKET block RBRACKET SEMICOLON
	'''
p[0] = 'Code compiled successfully'

def p_program2(p):
	'''
	program2	: class_
						| empty
	'''

def p_program3(p):
	'''
	program3	: funciones
						| empty
	'''

def p_program4(p):
	'''
	program4	: vars
						| empty
	'''

def bloque(p):
	'''
	bloque	: estatuto bloque1
	'''

def bloque1(p):
	'''
	bloque1	: estatuto bloque1
					| empty
	'''

def tipo_simple(p):
	'''
	tipo_simple	: INT
							| FLOAT
							| STRING
							| CHAR
	'''

def tipo_compuesto(p):
	'''
	tipo_compuesto	: FILE
									| ID
	'''

def class_(p):
	'''
	class_	: CLASS ID class1_ 
	'''
def class1_(p):
	'''
	class1_	: INHERITS ID
					| class2_
	'''

def class2_(p):
	'''
	class2_	: LBRACKET class3_ RBRACKET SEMICOLON
	'''

def class3_(p):
	'''
	class3_	: vars
					| funciuones
					| empty
	'''

def vars_(p):
	'''
	vars_	: tipo_simple vars2_
				| tipo_compuesto vars2_
	'''

def vars2_(p):
	'''
	vars2_	: ID s
	'''







def param(p):
	'''
	param	: tipo_simple ID param2
	'''

def param2(p):
	'''
	param2	: COMMA tipo_simple ID param2
					| empty
'''

def estatutos(p):
	'''
	estatutos	: asignacion
						| condicion
						| read
						| write
						| for_loop
						| while_loop
						| llamada_void
	'''

def llamada(p):
	'''
	llamada	: ID LPAREN exp RPAREN llamada2
'''

def llamada2(p):
	'''
	llamada2	: COMMA LPAREN exp RPAREN llamada2
						| empty
	'''

def llamada_void(p):
	'''
	llamada_void	: ID LPAREN var_cte llamada_void2 RPAREN SEMICOLON
	'''

def llamada_void2(p):
	'''
	llamada_void2	: COMMA var_cte llamada_void2
								| empty
	'''

def asignacion(p):
	'''
	asignacion	: variable EQUALS exp SEMICOLON
	'''

def variable(p):
	'''
	variable	: ID variable2
	'''

def variable2(p):
	'''
	variable2	: DOT ID
						| LSQRBRACKET CTE_I RSQRBRACKET
						| empty
	'''

def condicion(p):
	'''
	condicion	: IF LPAREN exp RPAREN bloque condicion2 SEMICOLON
	'''

def condicion2(p):
	'''
	condicion2	: ELSE bloque
							| empty
	'''

def read(p):
	'''
	read	:	READ LPAREN ID read2 RPAREN SEMICOLON
	'''

def read2(p):
	'''
	read2	: DOT ID
				| COMMA ID read2
				| empty
	'''

# Esta no se que onda
def write(p):
	'''
	write	: WRITE LPAREN 
	'''

def var_cte(p):
	'''
	var_cte	: ID
					| CTE_I
					| CTE_F
					| CTE_STRING
	'''

def while_loop(p):
	'''
	while_loop	: WHILE LPAREN loop_cond RPAREN LBRACKET exp RBRACKET
	'''
def loop_cond(p):
	'''
	loop_cond	: 
	'''

def for_loop(p):
	'''
	for_loop	: FOR LPAREN ID EQUALS CTE_I TO CTE_I RPAREN LBRACKET exp RBRACKET
	'''

def open_file(p):
	'''
	open_file	: ID DOT OPEN LPAREN CTE_STRING RPAREN SEMICOLON
	'''

def close_file(p):
	'''
	close_file	: ID DOT CLOSE LPAREN RPAREN SEMICOLON
	'''