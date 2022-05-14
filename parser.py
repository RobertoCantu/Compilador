# from msilib.schema import Error
from asyncio import constants
from calendar import c
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

#quadruple.generateQuad('plus', 2, 3, 4)

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
	print("Diccionario de funciones", dirFunc)
	print("Pila de operandos", quadruple.pilaO)
	print("Pila de tipos", quadruple.pTypes)
	print("Pila de operadores", quadruple.poper)
	print("Pila Saltos", quadruple.pSaltos)
	print("Size of quads list", quadruple.quad_counter)
	print("Lista de cuadruplos: ")
	i = 0
	for quad in quadruple.get_quads_list():
		print(f"{i}", quad)
		i = i + 1
		
def p_program2(p):
	'''
	program2		: vars_ add_to_global_vars
					| empty
	'''

def p_program3(p):
	'''
	program3		: funciones
					| empty
	'''

def p_program4(p):
	'''
	program4		: class_
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
					| empty
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
	funciones2		:  FUNCTION tipo_simple ID add_func func_add_return LPAREN create_var_table param RPAREN LBRACKET vars_ count_function_elements bloque RETURN LPAREN exp RPAREN func_return SEMICOLON RBRACKET end_of_func funciones2
					|  FUNCTION VOID ID add_func LPAREN create_var_table param RPAREN LBRACKET vars_ count_parameters count_locals count_quads bloque RBRACKET end_of_func funciones2
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
	g_exp			: m_exp check_comparator g_exp_2
	'''
	if(quadruple.poper_top() == ">" or quadruple.poper_top() == "<" or quadruple.poper_top() == "!=" or quadruple.poper_top() == "=="):
		quadruple.found_operator(quadruple.poper_top())

def p_g_exp_2(p):
	'''
	g_exp_2			: GREATER add_comparator m_exp
					| LESS add_comparator m_exp
					| NOTEQUAL add_comparator m_exp
					| EQUAL add_comparator m_exp
					| empty
	'''

# <M_EXP>
# Calls to + (SUM) or - (SUB)
# WHERE EXPs IN FOR LOOP STARTS m_exp
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
	f			: LPAREN add_fake_bottom exp pop_fake_bottom RPAREN
				| CTEI add_int
				| CTEF add_float
				| CTESTRING
				| variable
				| llamada
	'''
	
def p_param(p):
	'''
	param			: tipo_simple ID add_param param2
						| empty
	'''

def p_param2(p):
	'''
	param2			: COMMA tipo_simple ID add_param param2
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
	condicion	: IF LPAREN exp if_cond RPAREN LBRACKET bloque RBRACKET if_end condicion2 SEMICOLON
	'''

def p_condicion2(p):
	'''
	condicion2	: ELSE LBRACKET bloque end_of_else RBRACKET
				| end_of_else empty
	'''

# <READ>
def p_read(p):
	'''
	read		: READ LPAREN variable add_read RPAREN SEMICOLON
	'''

# <WRITE>
def p_write(p):
	'''
	write		:	WRITE LPAREN write_2
	'''

def p_write_2(p):
	'''
	write_2		: exp add_write write_3
						| CTESTRING write_3 
	'''

def p_write_3(p):
	'''
	write_3		: COMMA write_2
						| RPAREN SEMICOLON
	'''

def p_var_cte(p):
	'''
	var_cte		: ID
				| CTEI
				| CTEF
				| CTESTRING
	'''

# <WHILE LOOP>
def p_while_loop(p):
	'''
	while_loop	: WHILE while_jump LPAREN exp RPAREN while_eval_exp LBRACKET bloque RBRACKET while_return SEMICOLON
	'''

# <FOR LOOP>
def p_for_loop(p):
	'''
	for_loop	: FOR ID for_store_id EQUALS exp for_exp_equal_id TO exp for_comparison DO LBRACKET bloque RBRACKET for_end SEMICOLON
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
		
	dirFunc[p[-1]] = {"name": p[-1], "type": "global", "table": None, "paramsTable": None}
	
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
	dirFunc[p[-1]] = {"name": p[-1], "type": p[-3], "table": None, "paramsTable": None }
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
	global dirFunc

	dirFunc[currentFunction]['table'] = None # Delete function's var table at the end. 

	currentFunction = programName

def p_create_var_table(p):
	'''
	create_var_table	: empty
	'''

	global currentFunction
	global dirFunc

	if not (dirFunc[currentFunction]["table"]):
		dirFunc[currentFunction]["table"] = {}
		# dirFunc[currentFunction]["paramsTable"] = []
	if(currentFunction != programName):
		if not (dirFunc[currentFunction]["paramsTable"]):
			dirFunc[currentFunction]["paramsTable"] = []

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

def p_add_param(p):
	'''
	add_param	: empty
	'''
	global currentFunction
	global dirFunc

	if ( p[-1] not in dirFunc[currentFunction]['table']):
		dirFunc[currentFunction]['table'][p[-1]] = {'name': p[-1], 'type': p[-2]}
		# Add signature
		dirFunc[currentFunction]['paramsTable'].append(p[-2])

	else:
		print(f"Variable \"{p[-1]}\" ya declarada ")
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

def p_check_comparator(p):
	'''
	check_comparator	: empty
	'''
	if(quadruple.poper_top() == ">" or quadruple.poper_top() == "<" or quadruple.poper_top() == "!=" or quadruple.poper_top() == "=="):
		quadruple.found_operator(quadruple.poper_top())

def p_add_comparator(p):
	'''
	add_comparator	: empty
	'''
	quadruple.push_poper(p[-1])

def p_add_fake_bottom(p):
	'''
	add_fake_bottom 	: empty
	'''
	quadruple.push_poper(p[-1])

def p_pop_fake_bottom(p):
	'''
	pop_fake_bottom 	: empty
	'''
	quadruple.get_poper_stack().pop()

def p_add_write(p):
	'''
	add_write	: empty
	'''
	quadruple.push_poper('write')
	res = quadruple.pilaO_top()
	quadruple.get_pilaO_stack().pop()
	quadruple.generateQuad('WRITE', 'empty', 'empty', res)
	quadruple.get_poper_stack().pop()
	quadruple.get_pilaTypes_stack().pop()

def p_add_read(p):
	'''
	add_read	: empty
	'''
	quadruple.push_poper('read')
	res = quadruple.pilaO_top()
	quadruple.get_pilaO_stack().pop()
	quadruple.generateQuad('READ', 'empty', 'empty', res)
	quadruple.get_poper_stack().pop()
	quadruple.get_pilaTypes_stack().pop()

# IF
def p_if_cond(p):
	'''
	if_cond		: empty
	'''
	quadruple.createIf('GOTOF')
	

# END OF IF, START OF ELSE (IF ANY)
def p_if_end(p):
	'''
	if_end	: empty
	'''
	quadruple.if_end()


# ELSE 
def p_end_of_else(p):
	'''
	end_of_else	: empty
	'''
	quadruple.else_end()

# WHILE Points
def p_while_jump(p):
	'''
	while_jump	: empty
	'''
	count = quadruple.quad_counter
	quadruple.push_pSaltos(count)

def p_while_eval_exp(p):
	'''
	while_eval_exp 	: empty
	'''
	cond = quadruple.get_pilaO_stack().pop()
	type_condition = quadruple.get_pilaTypes_stack().pop()
	if (type_condition != 'bool'):
		print('Expected boolean exp')
		exit()
	else:
		quadruple.generateQuad('GOTOF', cond, 'empty', 'empty')
		quadruple.push_pSaltos(quadruple.quad_counter - 1)

def p_while_return(p):
	'''
	while_return	: empty
	'''
	false_quad = quadruple.get_pilaSaltos_stack().pop()
	return_quad = quadruple.get_pilaSaltos_stack().pop()
	quadruple.generateQuad('GOTO', None, None, return_quad)
	quadruple.fillQuad(false_quad, quadruple.quad_counter)


# FOR LOOP
def p_for_store_id(p):
	'''
	for_store_id		: empty
	'''
	global currentFunction
	global dirFunc
	global programName

	v_control = p[-1]

	# Check it exists in local function if not checks in global and is a numerical var
	if ( v_control in dirFunc[currentFunction]['table']):

		v_type = dirFunc[currentFunction]['table'][v_control]['type']

	elif(v_control in dirFunc[programName]['table']):
		v_type = dirFunc[programName]['table'][v_control]['type']

	else:
		print(f"Semantic Error: Type mismatch, Variable \"{v_control}\" no existe")
		exit()

	# Check it's type
	if not (numerical(v_type)):
		print(f"Semantic Error: Type missmatch, Variable \"{v_control}\" no numerica ")
		exit()

	# PUSH pilaO & pTypes
	quadruple.pilaO.append(v_control)
	quadruple.pTypes.append(v_type)
	


def p_for_exp_equal_id(p):
	'''
	for_exp_equal_id	: empty
	'''
	quadruple.for_equal_exp()


def p_for_comparison(p):
	'''
	for_comparison		: empty
	'''
	quadruple.for_comparison()


def p_for_end(p):
	'''
	for_end				: empty
	'''
	quadruple.for_end()

# Functions 
def p_count_parameters(p):
	'''
	count_parameters	: empty
	'''
	global currentFunction
	global dirFunc

	totalParams = len(dirFunc[currentFunction]["paramsTable"])
	dirFunc[currentFunction]["totalParams"] = totalParams

def p_count_locals(p):
	'''
	count_locals	: empty
	'''
	global currentFunction
	global dirFunc

	totalLocals = len(dirFunc[currentFunction]["table"])
	dirFunc[currentFunction]["totalLocals"] = totalLocals - dirFunc[currentFunction]["totalParams"]

def p_count_quads(p):
	'''
	count_quads : empty
	'''
	dirFunc[currentFunction]["startAtQuad"] = quadruple.quad_counter


def p_count_function_elements(p):
	'''
	count_function_elements	: empty
	'''
	global currentFunction
	global dirFunc

	totalParams = len(dirFunc[currentFunction]["paramsTable"])
	dirFunc[currentFunction]["totalParams"] = totalParams

	totalLocals = len(dirFunc[currentFunction]["table"])
	dirFunc[currentFunction]["totalLocals"] = totalLocals - dirFunc[currentFunction]["totalParams"]

	dirFunc[currentFunction]["startAtQuad"] = quadruple.quad_counter

def p_func_add_return(p):
	'''
	func_add_return			: empty
	'''
	global currentFunction
	global dirFunc
	global globalVars

	varName = p[-2]
	varType = p[-3]

	# CHECK GLOBAL VARS
	if (varName in globalVars):
		print(f'error {varName} already exists')
		exit()
	else:
		# ADD VALUE AND TYPE TO GLOBAL VARS
		globalVars[varName] = {'name': varName, 'type': varType}

def p_func_return(p):
	'''
	func_return			: empty
	'''
	global currentFunction
	global dirFunc
	global globalVars

	# GET FUNCTION'S TYPE AND RETURN VAR
	funcVar = globalVars[currentFunction]['name']
	funcVarType = globalVars[currentFunction]['type']

	# CHECK RETURN VALUE IS EQUAL TO TYPE OF FUNCTION
	retVar = quadruple.pilaO.pop()
	retVarType = quadruple.pTypes.pop()

	try:
		retType = SEMANTIC[funcVarType][retVarType]['=']
		# GENERATE QUAD, ASIGN RETURN TO FUNCTION'S RETURN VAR
		quadruple.generateQuad('=', retVar, None, funcVar)
	except:
		print(f'Comp. error: in function: {currentFunction}, return value not correct')
		exit()
	
def p_add_to_global_vars(p):
	'''
	add_to_global_vars 		: empty
	'''
	global currentFunction
	global dirFunc
	global globalVars

	globalVars = dirFunc[currentFunction]["table"]


################ END OF NEURAL POINTS ################


################ AUX FUNCTIONS ################
def numerical(val):
	if (val != "int" and val != "float"):
			return False
	else:
		return True

################ END OF AUX FUNCTIONS ################

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