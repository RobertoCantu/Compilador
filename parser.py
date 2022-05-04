# from msilib.schema import Error
import sys
# from Directory import addFunc, createVarTable, addVar
import ply.yacc as yacc
from lexer import tokens
import Directory as dc
from cube import SEMANTIC
from Quadruples import Quadruple

# Dict
dirFunc = {}
globalVars = {}

# Global vars
currentType = "" 		# current type being asigned to variable
programName = ""		# 
currentFunction = ""	# 
currentVarsTable = ""

# Quads
quadruple = Quadruple()

quadruple.generateQuad('plus', 2, 3, 4)

# print(quadruple.quadruples)



def p_program(p):
	'''
	program 		: PROGRAM ID create_main_func SEMICOLON program2 program3 program4 MAIN LBRACKET bloque RBRACKET SEMICOLON
	'''
	p[0] = 'Code compiled successfully'
	
	keys = dirFunc.keys()

	# for key in keys: 
	# 	print(key)
	# 	print(dirFunc[key]['table'])
	# 	print('--------')
	print(quadruple.pilaO)
	print(quadruple.pTypes)
	print(quadruple.poper)
		
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
	class_			: CLASS ID class_seen class1_ 
	'''
def p_class1_(p):
	'''
	class1_			: INHERITS ID
					| class2_
	'''

def p_class2_(p):
	'''
	class2_			: LBRACKET class3_ RBRACKET end_of_func SEMICOLON
	'''

def p_class3_(p):
	'''
	class3_			: vars_
					| funciones
					| empty
	'''

# <VARS>

def p_vars_(p):
	'''
	vars_ 			: VAR create_var_table vars_type
	'''


def p_vars_type(p):
	'''
	vars_type		: tipo_simple type_seen vars_s
					| tipo_compuesto type_seen vars_c
	'''

def p_vars_c(p):
	'''
	vars_c			: ID id_seen COMMA
					| ID id_seen SEMICOLON vars_end
	'''

def p_vars_s(p):
	'''
	vars_s			: ID id_seen SEMICOLON vars_end
					| ID id_seen LSQRBRACKET CTEI RSQRBRACKET vars_array
					| ID id_seen COMMA vars_s
	'''

def p_vars_array(p):
	'''
	vars_array		: SEMICOLON vars_end
					| COMMA vars_s
	'''


def p_vars_end(p):
	'''
	vars_end		: vars_
					| empty
	'''


# <FUNCIONES>
def p_funciones(p):
	'''
	funciones		: FUNCTIONS funciones2
					| empty
	'''
def p_funciones2(p):
	'''
	funciones2		:  tipo_simple FUNCTION ID add_func LPAREN param RPAREN LBRACKET vars_ estatutos RETURN LPAREN exp RPAREN RBRACKET end_of_func funciones2
					|  VOID FUNCTION ID add_func LPAREN param RPAREN LBRACKET vars_ estatutos RBRACKET end_of_func funciones2
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
# Calls to + (SUM) or - (SUB)
def p_m_exp(p):
	'''
	m_exp			: t check_sum_sub m_exp_2
	'''

def p_m_exp_2(p):
	'''
	m_exp_2			: PLUS add_poper  m_exp
					| MINUS add_poper m_exp
					| empty
	'''


# <T>
# Calls to * (MUL) or / (DIV)
def p_t(p):
	'''
	t				: f check_mul_div t_2 
	'''

def p_t_2(p):
	'''
	t_2				: TIMES add_poper t
					| DIVIDE add_poper t
					| empty
	'''

# <F>
def p_f(p):
	'''
	f			: LPAREN exp RPAREN
				| CTEI add_int
				| CTEF add_float
				| CTESTRING
				| variable
				| llamada
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
	asignacion	: variable EQUALS add_equals exp SEMICOLON
	'''
	# When the call returns it creates the equal quadruple
	quadruple.found_equal()

def p_variable(p):
	'''
	variable	: ID  variable2 add_id
	'''

def p_variable2(p):
	'''
	variable2	: DOT ID
				| LSQRBRACKET CTEI RSQRBRACKET
				| empty
	'''

def p_condicion(p):
	'''
	condicion	: IF LPAREN exp RPAREN LBRACKET bloque RBRACKET condicion2 SEMICOLON
	'''

def p_condicion2(p):
	'''
	condicion2	: ELSE LBRACKET bloque RBRACKET
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


################ NEURAL POINTS ################

def p_create_main_func(p):
	'''
	create_main_func : empty
	'''

	global dirFunc
	global programName
	global currentFunction
		
	dirFunc[p[-1]] = {"name": p[-1], "type": "global", "table": None}
	
	# = dc.DirFunc()
	# dirFunc.addFunc({"name": p[-1], "type": "global", "table": None })
	programName = p[-1]
	currentFunction = p[-1]
	
def p_add_func(p):
	'''
	add_func		: empty
	'''

	global dirFunc
	global currentFunction
	
	# dirFunc = dc.DirFunc()
	# dirFunc.addFunc({"name": p[-1], "type": p[-3], "table": None })
	dirFunc[p[-1]] = {"name": p[-1], "type": p[-3], "table": None }
	currentFunction = p[-1]


def p_type_seen(p):
	'''
	type_seen		: empty
	'''
	global currentType
	currentType = p[-1]

def p_id_seen(p):
	'''
	id_seen			: empty
	'''
	global currentFunction
	global dirFunc
	global currentType
	dirFunc[currentFunction]['table'][p[-1]] = {'name': p[-1], 'type': currentType}
	
def p_class_seen(p):
	'''
	class_seen		: empty
	'''
	global currentFunction
	global dirFunc
	global currentType
	currentFunction = p[-1]
	dirFunc[p[-1]] = {"name": p[-1], "type": "class", "table": None }



def p_end_of_func(p):
	'''
	end_of_func		: empty
	'''
	global currentFunction
	global programName
	currentFunction = programName

def p_create_var_table(p):
	'''
	create_var_table	: empty
	'''

	global currentFunction
	global dirFunc

	if not (dirFunc[currentFunction]["table"]):
		dirFunc[currentFunction]["table"] = {}



def p_add_id(p):
	'''
	add_id : empty

	'''

	global currentFunction
	global globalVars
	global dirFunc

	if (p[-2] in dirFunc[currentFunction]['table']):

		var_type = dirFunc[currentFunction]['table'][p[-2]]["type"]
		quadruple.push_pTypes(var_type)
		quadruple.push_pilaO(p[-2])
	else:
		print(f"Variable \"{p[-2]}\" no declarada ")
		exit()

def p_add_int(p):
	"""
	add_int : empty
	"""
	quadruple.push_pTypes("int")
	quadruple.push_pilaO(p[-1])

def p_add_float(p):
	"""
	add_float : empty
	"""
	quadruple.push_pTypes("float")
	quadruple.push_pilaO(p[-1])

# Adds equal to poper
def p_add_equals(p):
	'''
	add_equals	: empty
	'''
	quadruple.poper.append("=")


def p_add_poper(p):
	'''
	add_poper	: empty
	'''
	quadruple.push_poper(p[-1])

def p_check_sum_sub(p):
	'''
	check_sum_sub	: empty
	'''
	if(quadruple.poper_top() == "+" or quadruple.poper_top() == "-"):
		quadruple.found_operator(quadruple.poper_top())


def p_check_mul_div(p):
	'''
	check_mul_div	: empty
	'''
	if(quadruple.poper_top() == "*" or quadruple.poper_top() == "/"):
		quadruple.found_operator(quadruple.poper_top())


# Error rule for syntax errors
def p_error(p):
	print ("Line %s, illegal token %s" % (p.lineno, p.value))


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