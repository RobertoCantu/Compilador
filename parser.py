import sys
from Directory import addFunc, createVarTable, addVar
import ply.yacc as yacc
from lexer import tokens

# Dict
dirFunc = {}
globalVars = {}


def p_program(p):
	'''
	program 		: PROGRAM ID SEMICOLON program2 program3 program4 MAIN LBRACKET bloque RBRACKET SEMICOLON
	'''
	addFunc(dirFunc, p[2], "void");
	print(dirFunc)
	p[0] = 'Code compiled successfully'

	# while True:
	# 	print("hola222")
	

def p_program2(p):
	'''
	program2		: class_
					| empty
	'''

def p_program3(p):
	'''
	program3		: funciones
					| empty
	'''

def p_program4(p):
	'''
	program4		: vars_
					| empty
	'''

def p_bloque(p):
	'''
	bloque			: estatutos bloque1
					| empty
	'''

def p_bloque1(p):
	'''
	bloque1			: estatutos bloque1
					| empty
	'''

def p_tipo_simple(p):
	'''
	tipo_simple		: INT
					| FLOAT
					| STRING
					| CHAR
	'''
	p[0] = p[1]
def p_tipo_compuesto(p):
	'''
	tipo_compuesto	: FILE
					| ID
	'''
	p[0] = p[1]

def p_class_(p):
	'''
	class_			: CLASS ID class1_ 
	'''
def p_class1_(p):
	'''
	class1_			: INHERITS ID
					| class2_
	'''

def p_class2_(p):
	'''
	class2_			: LBRACKET class3_ RBRACKET SEMICOLON
	'''

def p_class3_(p):
	'''
	class3_			: vars_
					| funciones
					| empty
	'''

# <VARS>

def p_vars_(p):
	'''
	vars_			: VAR tipo_simple vars_2
					| VAR tipo_compuesto vars_2
					| empty
	'''

	if(len(p) == 4):
		p[0] = p[2]
		print(p[0])
		# p[2].append(p[3])
		# p[0] = p[2]
	# print(p[2])
	# print("hola")

def p_vars_2(p):
	'''
	vars_2			: ID vars_3
	'''

def p_vars_3(p):
	'''
	vars_3			: SEMICOLON vars_
					| vars_4
	'''

def p_vars_4(p):
	'''
	vars_4			: COMMA ID vars_4
					| LSQRBRACKET CTEI RSQRBRACKET vars_5
					| SEMICOLON vars_
	'''

def p_vars_5(p):
	'''
	vars_5			: COMMA vars_2
					| SEMICOLON vars_
	'''

# <FUNCIONES>
def p_funciones(p):
	'''
	funciones		: FUNCTIONS funciones2
					| empty
	'''
def p_funciones2(p):
	'''
	funciones2		:  tipo_simple FUNCTION ID LPAREN param RPAREN LBRACKET vars_ estatutos RETURN LPAREN exp RPAREN RBRACKET funciones2
					|  VOID FUNCTION ID LPAREN param RPAREN LBRACKET vars_ estatutos RBRACKET funciones2
					| empty
	'''

# <EXP>
def p_exp(p):
	'''
	exp				: t_exp exp_2
	'''

def p_exp_2(p):
	'''
	exp_2			: OR exp
					| empty
	'''

# <T_EXP>
def p_t_exp(p):
	'''
	t_exp			: g_exp t_exp_2
	'''

def p_t_exp_2(p):
	'''
	t_exp_2			: AND t_exp
					| empty
	'''
  
# <G_EXP>
def p_g_exp(p):
	'''
	g_exp			: m_exp g_exp_2
	'''

def p_g_exp_2(p):
	'''
	g_exp_2			:	GREATER m_exp
					| LESS m_exp
					| NOTEQUAL m_exp
					| EQUAL m_exp
					| empty
	'''

# <M_EXP>
def p_m_exp(p):
	'''
	m_exp			: t m_exp_2
	'''

def p_m_exp_2(p):
	'''
	m_exp_2			: PLUS  m_exp
					| MINUS m_exp
					| empty
	'''
# <T>
def p_t(p):
	'''
	t				: f t_2
	'''

def p_t_2(p):
	'''
	t_2				: TIMES t
					| DIVIDE t
					| empty
	'''

# <F>
def p_f(p):
	'''
	f			: LPAREN exp RPAREN f_2
				| CTEI f_2
				| CTEF f_2
				| CTESTRING f_2
				| variable f_2
				| llamada f_2
				| ID DOT ID f_2
	'''

def p_f_2(p):
	'''
	f_2				: empty
	'''

def p_param(p):
	'''
	param			: tipo_simple ID param2
	'''

def p_param2(p):
	'''
	param2			: COMMA tipo_simple ID param2
					| empty
'''

def p_estatutos(p):
	'''
	estatutos		: asignacion
					| condicion
					| read
					| write
					| for_loop
					| while_loop
					| llamada_void
	'''

def p_llamada(p):
	'''
	llamada			: ID LPAREN exp RPAREN llamada2
'''

def p_llamada2(p):
	'''
	llamada2		: COMMA LPAREN exp RPAREN llamada2
					| empty
	'''

def p_llamada_void(p):
	'''
	llamada_void	: ID LPAREN var_cte llamada_void2 RPAREN SEMICOLON
	'''

def p_llamada_void2(p):
	'''
	llamada_void2	: COMMA var_cte llamada_void2
					| empty
	'''

def p_asignacion(p):
	'''
	asignacion	: variable EQUALS exp SEMICOLON
	'''

def p_variable(p):
	'''
	variable	: ID variable2
	'''

def p_variable2(p):
	'''
	variable2	: DOT ID
				| LSQRBRACKET CTEI RSQRBRACKET
				| empty
	'''

def p_condicion(p):
	'''
	condicion	: IF LPAREN exp RPAREN bloque condicion2 SEMICOLON
	'''

def p_condicion2(p):
	'''
	condicion2	: ELSE bloque
				| empty
	'''

def p_read(p):
	'''
	read		: READ LPAREN ID read2 RPAREN SEMICOLON
	'''

def p_read2(p):
	'''
	read2		: DOT ID
				| COMMA ID read2
				| empty
	'''

# <WRITE>
def p_write(p):
	'''
	write		:	WRITE LPAREN write_2
	'''

def p_write_2(p):
	'''
	write_2		: exp  RPAREN write_3 SEMICOLON
				| CTESTRING RPAREN write_3 SEMICOLON
	'''

def p_write_3(p):
	'''
	write_3		: COMMA write_2
				| empty
	'''

def p_var_cte(p):
	'''
	var_cte		: ID
				| CTEI
				| CTEF
				| CTESTRING
	'''

def p_while_loop(p):
	'''
	while_loop	: WHILE LPAREN loop_cond RPAREN LBRACKET exp RBRACKET
	'''
# <LOOP_COND>
def p_loop_cond(p):
	'''
	loop_cond	:	l_1 loop_cond_2
	'''

def p_loop_cond_2(p):
	'''
	loop_cond_2	: OR loop_cond
				| empty
	'''

# <L_1>
def p_l_1(p):
	'''
	l_1			: l_2 l_1_2
	'''

def p_l_1_2(p):
	'''
	l_1_2		: AND l_1
				| empty
	'''

# <L_2>
def p_l_2(p):
	'''
	l_2			: l_3 l_2_2
	'''

def p_l_2_2(p):
	'''
	l_2_2		: GREATER l_3
				| LESS l_3
				| NOTEQUAL l_3
				| EQUAL l_3
				| empty
	'''

def p_l_3(p):
	'''
	l_3			:	CTEI empty
				| LPAREN loop_cond RPAREN empty
	'''

def p_for_loop(p):
	'''
	for_loop	: FOR LPAREN ID EQUALS CTEI TO CTEI RPAREN LBRACKET exp RBRACKET
	'''

def p_open_file(p):
	'''
	open_file	: ID DOT OPEN LPAREN CTESTRING RPAREN SEMICOLON
	'''

def p_close_file(p):
	'''
	close_file	: ID DOT CLOSE LPAREN RPAREN SEMICOLON
	'''

def p_empty(p):
	'''
	empty	:
	'''
	pass

# Error rule for syntax errors
def p_error(p):
	print ("Line %s, illegal token %s" % (p.lineno, p.value))


# DirFunc
# name: [type, varTable]

# VarTables
# id_name: [type, value]

dirFunc = {}

# dirFunc = {
#	'global': ['void', { 'i': ['int', #], }],
# }

parser = yacc.yacc()

if __name__ == '__main__':

	if len(sys.argv) > 1:
		file = sys.argv[1]
		try:
			f = open(file, 'r')
			data = f.read()
			f.close()
			result = parser.parse(data)
			print(result)
		except EOFError:
			print(EOFError)
	else:
		print("No file to read")