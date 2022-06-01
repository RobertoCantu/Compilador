# from msilib.schema import Error
from ast import arg
from asyncio import constants
from calendar import c
import sys
import virtualAddress
# from Directory import addFunc, createVarTable, addVar
import ply.yacc as yacc
from lexer import tokens
import Directory as dc
from cube import SEMANTIC
from Quadruples import Quadruple
from Directory import ConstantsTable
import pickle
import subprocess
from error import SemanticError


# Dict
dirFunc = {}
globalVars = {}

# Global vars
currentType = "" 		# current type being asigned to variable
programName = ""		# 
currentFunction = ""	# current function
currentVarsTable = ""

# Array utils
arr_dim = 1
arr_r = 1
curr_id = "" # Current ID of array variable

# Quads
quadruple = Quadruple()

#Constants Table
constantsTable = ConstantsTable()

# Functions calls and params
funcCalled = None
funcCalledStack = []
paramCounter = None
currentParamTable = None
tempFunc = None
auxFunc = None

# Dimensions
DIM = 1
curr_node = None

def p_program(p):
	'''
	program 		: PROGRAM ID create_main_func SEMICOLON program2 program3 program4 MAIN start_main LBRACKET bloque RBRACKET SEMICOLON
	'''
	# Count globals vars
	globals = virtualAddress.getGlobalUsed()
	dirFunc["globalsUsed"] = {}
	dirFunc["globalsUsed"]["int"] = globals[0]
	dirFunc["globalsUsed"]["float"] = globals[1]
	dirFunc["globalsUsed"]["char"] = globals[2]
	dirFunc["globalsUsed"]["bool"] = globals[3]

	# Count globals temp
	globals = virtualAddress.getGlobalTempUsed()
	dirFunc["globalsTempUsed"] = {}
	dirFunc["globalsTempUsed"]["int"] = globals[0]
	dirFunc["globalsTempUsed"]["float"] = globals[1]
	dirFunc["globalsTempUsed"]["char"] = globals[2]
	dirFunc["globalsTempUsed"]["bool"] = globals[3]
	dirFunc["globalsTempUsed"]["pointer"] = globals[4]

	quadruple.generateQuad('END', None, None, None) # END OF FILE
	p[0] = 'Code compiled successfully'

	print("Diccionario de funciones", dirFunc)
	for key in dirFunc.keys():
		print(dirFunc[key])
		print()

	print("Pila de operandos", quadruple.pilaO)
	print("Pila de tipos", quadruple.pTypes)
	print("Pila de operadores", quadruple.poper)
	print("Pila Saltos", quadruple.pSaltos)
	print("Pila arrays", quadruple.pilaDIM)
	print("Size of quads list", quadruple.quad_counter)
	print("Lista de cuadruplos: ")
	i = 0
	for quad in quadruple.get_quads_list():
		print(f"{i}", quad)
		i = i + 1
	
	print('========================================')
	subprocess.call(['python', 'VirtualMachine.py'])
	print('========================================')
		
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
	vars_s			: ID id_seen vars_options
					| ID id_seen LSQRBRACKET is_array CTEI RSQRBRACKET array_calcs vars_matrix vars_options
	'''

def p_vars_options(p):
	'''
	vars_options	: SEMICOLON vars_end
					| COMMA vars_s
	'''

def p_vars_end(p):
	'''
	vars_end		: vars_
					| empty
	'''

def p_vars_matrix(p):
	'''
	vars_matrix		: LSQRBRACKET CTEI RSQRBRACKET array_calcs array_end
					| array_end empty
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
					|  FUNCTION VOID ID add_func LPAREN create_var_table param RPAREN LBRACKET vars_ count_parameters count_locals count_quads count_function_elements bloque RBRACKET end_of_func funciones2
					| empty
	'''

# <EXP>
def p_exp(p):
	'''
	exp				: t_exp check_and_or exp_2
	'''

def p_exp_2(p):
	'''
	exp_2			: OR add_poper exp
					| empty
	'''

# <T_EXP>
def p_t_exp(p):
	'''
	t_exp			: g_exp check_and_or t_exp_2
	'''

def p_t_exp_2(p):
	'''
	t_exp_2			: AND add_poper t_exp
					| empty
	'''
  
# <G_EXP>
def p_g_exp(p):
	'''
	g_exp			: m_exp check_comparator g_exp_2
	'''
	global currentFunction, programName
	location = 'Global' if programName == currentFunction else 'Local'

	if(quadruple.poper_top() == ">" or quadruple.poper_top() == ">=" or quadruple.poper_top() == "<" or quadruple.poper_top() == "<=" or quadruple.poper_top() == "!=" or quadruple.poper_top() == "=="):
		quadruple.found_operator(quadruple.poper_top(), location)

def p_g_exp_2(p):
	'''
	g_exp_2			: GREATER add_comparator m_exp
					| GREATEROREQUAL add_comparator m_exp
					| LESS add_comparator m_exp
					| LESSOREQUAL add_comparator m_exp
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
	f			: CTEI add_int
				| CTEF add_float
				| CTESTRING add_str
				| llamada
				| variable
				| LPAREN add_fake_bottom exp pop_fake_bottom RPAREN
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
	llamada			: ID LPAREN func_exists_create_era add_fake_bottom llamada2 RPAREN verify_params_coherency pop_fake_bottom
					| ID LPAREN func_exists_create_era  RPAREN gosub_no_params
	'''

def p_llamada2(p):
	'''
	llamada2		: add_fake_bottom exp pop_fake_bottom verify_param
					| add_fake_bottom exp pop_fake_bottom verify_param COMMA next_param llamada2
	'''

def p_llamada_void(p):
	'''
	llamada_void	: ID LPAREN func_exists_create_era llamada_void2 RPAREN verify_params_coherency SEMICOLON
					| ID LPAREN func_exists_create_era RPAREN gosub_no_params SEMICOLON
	'''

def p_llamada_void2(p):
	'''
	llamada_void2	: add_fake_bottom exp pop_fake_bottom verify_param
					| add_fake_bottom exp pop_fake_bottom verify_param COMMA next_param llamada_void2
	'''

def p_asignacion(p):
	'''
	asignacion	: variable EQUALS add_equals exp SEMICOLON
	'''
	quadruple.found_equal()

def p_variable(p):
	'''
	variable	: ID  add_id variable2
					
	'''

def p_variable2(p):
	'''
	variable2	: DOT ID
				| LSQRBRACKET verify_dim add_fake_bottom exp pop_fake_bottom add_verify RSQRBRACKET variable_array_2
				| empty
	'''

def p_variable_array_2(p):
	'''
	variable_array_2	: incr_dim LSQRBRACKET add_fake_bottom exp pop_fake_bottom add_verify RSQRBRACKET end_arr_access
						| end_arr_access empty
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
	write		:	WRITE LPAREN write_2 RPAREN SEMICOLON
	'''

def p_write_2(p):
	'''
	write_2		: exp add_write write_3 
				| CTESTRING add_write
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
	
	programName = p[-1]
	currentFunction = p[-1]

	# GENERATE QUAD FOR GOTO MAIN FUNCTION
	quadruple.generateQuad('GOTO', None, None, None)
	quadruple.pSaltos.append(quadruple.quad_counter-1)


# FILL GOTO MAIN FUNCTION
def p_start_main(p):
    '''
    start_main          : empty
    '''
    quadruple.fillQuad(quadruple.pSaltos.pop(), quadruple.quad_counter)

	
def p_add_func(p):
	'''
	add_func		: empty
	'''

	global dirFunc
	global currentFunction
	
	# dirFunc = dc.DirFunc()
	# dirFunc.addFunc({"name": p[-1], "type": p[-3], "table": None })
	dirFunc[p[-1]] = {"name": p[-1], "type": p[-2], "table": None, "paramsTable": None }
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
	global programName

	varID = p[-1]

	if(varID in dirFunc[currentFunction]["table"]):
		raise SemanticError("Naming collisions multiple declaration of variable ")
	else:
		if(currentFunction == programName):
			dirFunc[currentFunction]['table'][varID] = {'name': varID, 'type': currentType, 'address': virtualAddress.setAddress(currentType, 'global')}
		else:
			dirFunc[currentFunction]['table'][varID] = {'name': varID, 'type': currentType, 'address': virtualAddress.setAddress(currentType, 'local')} # Don't know

def p_class_seen(p):
	'''
	class_seen		: empty
	'''
	global currentFunction
	global dirFunc
	global currentType
	currentFunction = p[-1]
	dirFunc[p[-1]] = {"name": p[-1], "type": "class", "table": None }

def p_create_var_table(p):
	'''
	create_var_table	: empty
	'''

	global currentFunction, programName
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
	global programName

	varID = p[-1]

	# Look in locals
	if (varID in dirFunc[currentFunction]['table']):
		address = dirFunc[currentFunction]['table'][varID]["address"]
		var_type = dirFunc[currentFunction]['table'][varID]["type"]
		quadruple.push_pTypes(var_type) # Add type of id to type stack
		quadruple.push_pilaO(address) # Add address to operands stack
	# If not look in global
	elif (varID in dirFunc[programName]['table']):
		address = dirFunc[programName]['table'][varID]["address"]
		var_type = dirFunc[programName]['table'][varID]["type"]
		quadruple.push_pTypes(var_type) # Add type of id to type stack
		quadruple.push_pilaO(address) # Add address to operands stack

	else:
		raise SemanticError("Undeclared variable")

def p_add_param(p):
	'''
	add_param	: empty
	'''
	global currentFunction
	global dirFunc

	param = p[-1]
	paramType = p[-2]

	if ( param not in dirFunc[currentFunction]['table']):
		dirFunc[currentFunction]['table'][param] = {'name': param, 'type': paramType, 'address': virtualAddress.setAddress(paramType, 'local')}
		# Add signature
		dirFunc[currentFunction]['paramsTable'].append(paramType)
	else:
		raise SemanticError("Naming collisions multiple declaration of variable ")

def p_add_int(p):
	"""
	add_int : empty
	"""
	cint = p[-1] # INT VALUE
	# Check if constant already exist
	if (constantsTable.getConstantByValue(cint) == None):
		constantsTable.addConstant(cint, virtualAddress.setAddress('int', 'constant'))

	address_int = constantsTable.getConstantByValue(cint)['address']
	quadruple.push_pTypes("int")
	quadruple.push_pilaO(address_int)

def p_add_str(p):
	"""
	add_str : empty
	"""
	cstr = p[-1] # INT VALUE
	# Check if constant already exist
	if (constantsTable.getConstantByValue(cstr) == None):
		constantsTable.addConstant(cstr, virtualAddress.setAddress('char', 'constant'))

	address_str = constantsTable.getConstantByValue(cstr)['address']
	quadruple.push_pTypes("char")
	quadruple.push_pilaO(address_str)

def p_add_float(p):
	"""
	add_float : empty
	"""
	cfloat = p[-1]

	# Check if constant already exist
	if (constantsTable.getConstantByValue(cfloat) == None):
		constantsTable.addConstant(cfloat, virtualAddress.setAddress('float', 'constant'))

	address_int = constantsTable.getConstantByValue(cfloat)['address']
	quadruple.push_pTypes("float")
	quadruple.push_pilaO(address_int)

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

def p_check_and_or(p):
	'''
	check_and_or	: empty
	'''
	global currentFunction, programName
	location = 'Global' if programName == currentFunction else 'Local'

	if(quadruple.poper_top() == "&&" or quadruple.poper_top() == "||"):
		quadruple.found_operator(quadruple.poper_top(), location)

def p_check_sum_sub(p):
	'''
	check_sum_sub	: empty
	'''
	global currentFunction, programName
	location = 'Global' if programName == currentFunction else 'Local'

	if(quadruple.poper_top() == "+" or quadruple.poper_top() == "-"):
		quadruple.found_operator(quadruple.poper_top(), location)


def p_check_mul_div(p):
	'''
	check_mul_div	: empty
	'''
	global currentFunction, programName
	location = 'Global' if programName == currentFunction else 'Local'

	if(quadruple.poper_top() == "*" or quadruple.poper_top() == "/"):
		quadruple.found_operator(quadruple.poper_top(), location)

def p_check_comparator(p):
	'''
	check_comparator	: empty
	'''
	global currentFunction, programName
	location = 'Global' if programName == currentFunction else 'Local'

	if(quadruple.poper_top() == ">" or quadruple.poper_top() == "<" or quadruple.poper_top() == "!=" or quadruple.poper_top() == "=="):
		quadruple.found_operator(quadruple.poper_top(), location)

def p_add_comparator(p):
	'''
	add_comparator	: empty
	'''
	quadruple.push_poper(p[-1])

def p_add_fake_bottom(p):
	'''
	add_fake_bottom 	: empty
	'''
	quadruple.push_poper("(")

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
		raise SemanticError("Type mismatched expected a boolean exp")
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
		v_control_va =  dirFunc[currentFunction]['table'][v_control]['address']

	elif(v_control in dirFunc[programName]['table']):

		v_type = dirFunc[programName]['table'][v_control]['type']
		v_control_va =  dirFunc[currentFunction]['table'][v_control]['address']

	else:
		raise SemanticError(f"Undeclared variable {v_control}")

		print(f"Semantic Error: Type mismatch, Variable \"{v_control}\" no existe")
		exit()

	# Check it's type
	if not (numerical(v_type)):
		raise SemanticError("Type mismatched expected a numeric variable")

		print(f"Semantic Error: Type missmatch, Variable \"{v_control}\" no numerica ")
		exit()

	# PUSH pilaO & pTypes
	quadruple.pilaO.append(v_control_va)
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
	global currentFunction, programName
	location = 'Global' if programName == currentFunction else 'Local'
	quadruple.for_comparison(location)


def p_for_end(p):
	'''
	for_end				: empty
	'''
	global currentFunction, programName
	location = 'Global' if programName == currentFunction else 'Local'

	address_one = constantsTable.getConstantByValue(1)['address']
	quadruple.for_end(location, address_one)

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

	# Count locals vars
	locals = virtualAddress.getLocalUsed()
	dirFunc[currentFunction]["localsUsed"] = {}
	dirFunc[currentFunction]["localsUsed"]["int"] = locals[0]
	dirFunc[currentFunction]["localsUsed"]["float"] = locals[1]
	dirFunc[currentFunction]["localsUsed"]["char"] = locals[2]
	dirFunc[currentFunction]["localsUsed"]["bool"] = locals[3]

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
		raise SemanticError("Naming collisions multiple declaration of variable ")
		print(f'error {varName} already exists')
		exit()
	else:
		# ADD VALUE AND TYPE TO GLOBAL VARS
		globalVars[varName] = {'name': varName, 'type': varType, 'address': virtualAddress.setAddress(varType, 'global')}

def p_func_return(p):
	'''
	func_return			: empty
	'''
	global currentFunction, programName
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
		# quadruple.get_pilaTypes_stack().append(retType)
		# GENERATE QUAD, ASIGN RETURN TO FUNCTION'S RETURN VAR
		# temp = quadruple.counter
		# quadruple.counter += 1
		va = virtualAddress.setAddress(retVarType, 'tempLocal')

		# ASIGN EXP TO FUNCTION'S VAR 
		func_return_va = globalVars[currentFunction]['address']
		quadruple.generateQuad('=', retVar, None, func_return_va)

		quadruple.generateQuad('RETURN', None, None, va) # NOT SURE IF NEEDED!!!

	except:
		raise SemanticError("Type mismatched return value is incorrect")

		print(f'Comp. error: in function: {currentFunction}, return value not correct')
		exit()

def p_end_of_func(p):
	'''
	end_of_func		: empty
	'''
	global currentFunction
	global programName
	global dirFunc

	# dirFunc[currentFunction]['table'] = None # Delete function's var table at the end.
	quadruple.generateQuad('ENDFUNC', None, None, None)

	# Count local temporals and add it to dirFunc (int,float, char, bool)
	locals_temp_used = virtualAddress.getLocalTempUsed()
	dirFunc[currentFunction]['usedTemp'] = {}
	dirFunc[currentFunction]['usedTemp']['int'] = locals_temp_used[0]
	dirFunc[currentFunction]['usedTemp']['float'] = locals_temp_used[1]
	dirFunc[currentFunction]['usedTemp']['char'] = locals_temp_used[2]
	dirFunc[currentFunction]['usedTemp']['bool'] = locals_temp_used[3]
	dirFunc[currentFunction]['usedTemp']['pointer'] = locals_temp_used[4]

	print(locals_temp_used)

	virtualAddress.resetLocalTemporals() # RESETS LOCAL TEMPORALS FOR FUNCTIONS
	# Set currFunc to main
	currentFunction = programName


# Functions call
def p_func_exists_create_era(p):
	'''
	func_exists_create_era : empty
	'''
	global funcCalled
	global dirFunc
	global paramCounter
	global currentParamTable

	funcName = p[-2]

	if(funcName in dirFunc):
		funcCalled = funcName
	
	else:
		raise SemanticError(f"Undeclared variable {funcName}")

		print(f'Semantic Error: Funcion {funcName}, no declarada')
		exit()
	
	quadruple.generateQuad("ERA", funcCalled, None, None)
	paramCounter = 1
	currentParamTable = dirFunc[funcCalled]["paramsTable"]

def p_verify_param(p):
	'''
	verify_param	: empty
	'''
	argument = quadruple.get_pilaO_stack().pop()
	argument_type = quadruple.get_pilaTypes_stack().pop()
	# print(argument)

	# Verify types
	real_param_type = currentParamTable[paramCounter - 1]
	if(argument_type == real_param_type):
		quadruple.generateQuad("PARAMETER", argument, None, paramCounter)
	
	else:
		raise SemanticError(f"Type mismatched argument {paramCounter} is not of type {real_param_type}")

		print(f"Semantic error: Firma incorrecta, arugmento {paramCounter} no es de tipo {real_param_type}")
		exit()

def p_next_param(p):
	'''
	next_param	: empty
	'''
	global paramCounter
	paramCounter += 1

def p_verify_params_coherency(p):
	'''
	verify_params_coherency	: empty
	'''
	global funcCalled, programName, globalVars
	global dirFunc
	global programName, currentFunctionxw
	
	# Check if table of params is empty
	paramsTable = dirFunc[funcCalled]['paramsTable']
	if(len(paramsTable) != paramCounter):
		raise SemanticError(f"Type mismatched incorrect number of params for {funcCalled}")

		print("Semantic Error: Numero de parametros incorrecto")
		exit()
		
	else:
		quadruple.generateQuad("GOSUB", funcCalled, None, dirFunc[funcCalled]['startAtQuad'])
		funcCalledType = dirFunc[funcCalled]["type"]
		# Parche guadulupano
		if(funcCalledType != 'void'):
			if (programName == currentFunction):
				va = virtualAddress.setAddress(funcCalledType, 'tempGlobal')
			else:
				va = virtualAddress.setAddress(funcCalledType, 'tempLocal') # FUNCTION CALLS INSIDE FUNCTIONS
			# Get address of function
			func_return_va = globalVars[funcCalled]['address']

			quadruple.generateQuad("=", func_return_va, None, va)
			quadruple.push_pilaO(va)
			quadruple.push_pTypes(funcCalledType)
			quadruple.counter += 1

def p_gosub_no_params(p):
	'''
	gosub_no_params	: empty
	'''
	quadruple.generateQuad("GOSUB", funcCalled, None, dirFunc[funcCalled]['startAtQuad'])
	funcCalledType = dirFunc[funcCalled]["type"]
	# Parche guadulupano
	if(funcCalledType != 'void'):

		if (programName == currentFunction):
			va = virtualAddress.setAddress(funcCalledType, 'tempGlobal')
		else:
			va = virtualAddress.setAddress(funcCalledType, 'tempLocal') # FUNCTION CALLS INSIDE FUNCTIONS
		# Get address of function
		func_return_va = globalVars[funcCalled]['address']

		quadruple.generateQuad("=", func_return_va, None, va)
		quadruple.push_pilaO(va)
		quadruple.push_pTypes(funcCalledType)
		quadruple.counter += 1

	
def p_add_to_global_vars(p):
	'''
	add_to_global_vars 		: empty
	'''
	global currentFunction
	global dirFunc
	global globalVars

	globalVars = dirFunc[currentFunction]['table']

def p_is_array(p):
	'''
	is_array		: empty
	'''
	global currentFunction
	global dirFunc, globalVars
	global arr_dim, arr_r, curr_id

	location = 'Global' if programName == currentFunction else 'Local'
	varName = p[-3]
	curr_id = varName
	dirFunc[currentFunction]['table'][varName]['dim'] = []

def p_array_calcs(p):
	'''
	array_calcs			: empty
	'''
	global currentFunction, programName
	global dirFunc, globalVars
	global arr_dim, arr_r, curr_id

	location = 'Global' if programName == currentFunction else 'Local'
	varName = curr_id

	l_sup = p[-2]

	# R = (L_sup - L_inf + 1) * R
	arr_r = (l_sup) * arr_r

	dirFunc[currentFunction]['table'][varName]['dim'].append({'l_sup': l_sup, 'm': 0})

	arr_dim += 1

def p_array_end(p):
	'''
	array_end			: empty
	'''
	global currentFunction, programName
	global dirFunc, globalVars
	global arr_dim, arr_r, curr_id, currentType

	location = 'global' if programName == currentFunction else 'local'
	varName = curr_id
	
	arr_list = dirFunc[currentFunction]['table'][varName]['dim']

	indx = 0
	size = int(arr_r)

	virtualAddress.setArrayAddresses(currentType, location, size)

	for elem in arr_list:
		# R = R / (L_sup_dim - L_inf_dim + 1)
		l_sup = int(elem["l_sup"])

		arr_r = arr_r / (l_sup)

		# Stores m in DIM table
		dirFunc[currentFunction]['table'][varName]['dim'][indx]['m'] = int(arr_r)
		indx += 1

	curr_id = ""

# Array Access
def p_verify_dim(p):
	'''
	verify_dim	: empty
	'''
	global dirFunc
	global currentFunction
	global DIM
	global curr_node, curr_id
	global programName
	global tempFunc
	global auxFunc

	arr_id_address = quadruple.get_pilaO_stack().pop()
	arr_id = p[-3]
	# curr_id = arr_id

	# Check if local
	arr_type = quadruple.get_pilaTypes_stack().pop()

	# Check if id is an array local
	if(arr_id in dirFunc[currentFunction]['table']):
		if('dim' in dirFunc[currentFunction]['table'][arr_id]):
			DIM = 1
			quadruple.pilaDIM.append({
				'id': arr_id,
				'dim': DIM
			})
			curr_node = dirFunc[currentFunction]['table'][arr_id]['dim'][0]

		else:
			raise SemanticError(f"Type mismatched {arr_id} is not an array")

			print(f"Semantic Error: {arr_id} is not an array")
			exit()
	# Check global
	elif(arr_id in dirFunc[programName]['table']):
		if('dim' in dirFunc[programName]['table'][arr_id]):
			DIM = 1
			quadruple.pilaDIM.append({
				'id': arr_id,
				'dim': DIM
			})
			curr_node = dirFunc[programName]['table'][arr_id]['dim'][0]

		else:
			raise SemanticError(f"Type mismatched {arr_id} is not an array")
			print(f"Semantic Error: {arr_id} is not an array")
			exit()

	else:
		raise SemanticError(f"Undeclared variable {arr_id}")
		print(f"Semantic Error: Variable {arr_id} no declarada")
		exit()



def p_add_verify(p):
	'''
	add_verify	: empty
	'''
	# Create Verify quad
	global curr_node, DIM, curr_id
	global currentFunction, dirFunc, programName


	curr_arr = quadruple.pDim_top()
	curr_id = curr_arr['id']
	curr_dim = curr_arr['dim']

	if(curr_id in dirFunc[currentFunction]['table']):
		if(curr_dim > 1 and len(dirFunc[currentFunction]['table'][curr_id]['dim']) == 2):
			curr_node = dirFunc[currentFunction]['table'][curr_id]['dim'][1]

		elif(curr_dim > 1 and len(dirFunc[currentFunction]['table'][curr_id]['dim']) != 2 ):
			raise SemanticError(f"Type mismatched {curr_id} is not a matrix")

			print(f"Semantic Error: accesando indice de arreglo no existente")
			exit()

	elif(curr_id in dirFunc[programName]['table']):
		if(curr_dim > 1 and len(dirFunc[programName]['table'][curr_id]['dim']) == 2):
			curr_node = dirFunc[programName]['table'][curr_id]['dim'][1]

		elif(curr_dim > 1 and len(dirFunc[programName]['table'][curr_id]['dim']) != 2 ):
			raise SemanticError(f"Type mismatched {curr_id} is not a matrix")
			print(f"Semantic Error: accesando indice de arreglo no existente")
			exit()

	access_value = quadruple.pilaO_top()
	l_sup = curr_node['l_sup']

	# Check if constant already exist
	address_l_sup = getConstant(l_sup, 'int')

	quadruple.generateQuad("VERIFY", access_value, None, address_l_sup)

	# # Formula
	aux = quadruple.get_pilaO_stack().pop()
	aux_type = quadruple.pTypes.pop()

	m = curr_node['m']
	address_m = getConstant(m, 'int')

	# Create quad
	location = 'tempGlobal' if programName == currentFunction else 'tempLocal'

	va = virtualAddress.setAddress("int", location)
	quadruple.generateQuad("*", aux, address_m, va)
	quadruple.push_pilaO(va)

	if(curr_id in dirFunc[currentFunction]['table']):
		quadruple.push_pTypes(dirFunc[currentFunction]['table'][curr_id]['type']) # ARRAY type


	elif(curr_id in dirFunc[programName]['table']):
		quadruple.push_pTypes(dirFunc[programName]['table'][curr_id]['type']) # ARRAY type



	if (curr_dim > 1):
		aux2 = quadruple.pilaO.pop()
		aux1 = quadruple.pilaO.pop()
		
		t1 = quadruple.pTypes.pop()
		t2 = quadruple.pTypes.pop()

		retType = SEMANTIC[t1][t2]['+']

		va = virtualAddress.setAddress("int", location )
		quadruple.generateQuad("+", aux1, aux2, va)

		quadruple.push_pilaO(va)
		quadruple.push_pTypes(retType)

def p_incr_dim(p):
	'''
	incr_dim	: empty
	'''
	global DIM, curr_id

	curr_arr = quadruple.pDim_top()
	dim = curr_arr['dim']

	dim += 1
	
	quadruple.pilaDIM.append({"id": curr_id, "dim": dim})

def p_end_arr_access(p):
	'''
	end_arr_access	: empty
	'''
	global DIM, curr_id, curr_node
	global programName, currentFunction

	aux1 = quadruple.pilaO.pop()
	if(curr_id in dirFunc[currentFunction]['table']):
		addrs = dirFunc[currentFunction]['table'][curr_id]['address']


	elif(curr_id in dirFunc[programName]['table']):
		addrs = dirFunc[programName]['table'][curr_id]['address']

	addrs = getConstant(addrs, 'int')

	location = 'global' if programName == currentFunction else 'local'

	va = virtualAddress.setAddress("pointer", location)
	quadruple.generateQuad("+", aux1, addrs, va)

	quadruple.pilaO.append(va)
	quadruple.pilaDIM.pop()

	if(len(quadruple.pilaDIM) > 0):
		curr_arr = quadruple.pDim_top()
		id_arr = curr_arr['id']
		if(curr_id in dirFunc[currentFunction]['table']):
			curr_node = dirFunc[currentFunction]['table'][id_arr]['dim'][0]

		elif(curr_id in dirFunc[programName]['table']):
			curr_node = dirFunc[programName]['table'][id_arr]['dim'][0]




################ END OF NEURAL POINTS ################


################ AUX FUNCTIONS ################
def numerical(val):
	if (val != "int" and val != "float"):
			return False
	else:
		return True

def getConstant(val, val_type):
	ret = 0
	if (constantsTable.getConstantByValue(val) == None):
		constantsTable.addConstant(val, virtualAddress.setAddress(val_type, 'constant'))
	ret = constantsTable.getConstantByValue(val)['address']

	return ret

################ END OF AUX FUNCTIONS ################

# Error rule for syntax errors
def p_error(p):
	print ("Syntax Error in line %s, illegal token %s" % (p.lineno, p.value))


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

	# Generate ovejota
	with open('object.p', 'wb') as handle:
		pickle.dump(
			{
				"quadruples": quadruple.quadruples,
				"dirFunc": dirFunc,
				"constantsTable": constantsTable.getConstants()
			}, handle
		)