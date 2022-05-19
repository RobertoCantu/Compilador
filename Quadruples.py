from collections import deque
from cube import SEMANTIC
import virtualAddress
from Directory import ConstantsTable

class Quadruple:

    def __init__(self):
        self.quadruples = []
        self.poper = deque()    # poper = PILA OPERADORES
        self.pilaO = deque()    # pilaO = PILA DE OPERANDOS
        self.pTypes = deque()   # pTypes = PILA DE TIPOS
        self.pSaltos = deque()  # pSaltos = PILA DE SALTOS
        self.counter = 666      # 
        self.quad_counter = 0   # CONT. PARA LISTA DE CUADRUPLOS

    
    def increment_counter(self):
        self.counter = self.counter + 1

    # ADD TO STACKS 
    def push_poper(self, value):
        self.poper.append(value)

    def push_pilaO(self, value):
        self.pilaO.append(value)

    def push_pTypes(self, value):
        self.pTypes.append(value)

    def push_pSaltos(self, value):
        self.pSaltos.append(value)

    # Get stacks
    def get_poper_stack(self):
        return self.poper

    def get_pilaO_stack(self):
        return self.pilaO

    def get_pilaTypes_stack(self):
        return self.pTypes

    def get_pilaSaltos_stack(self):
        return self.pSaltos

    def get_quads_list(self):
        return self.quadruples


    # Get TOP from stacks
    def poper_top(self):
        if(len(self.poper) > 0):
            return self.poper[len(self.poper)-1]
        else:
            return None

    def pilaO_top(self):
        if(len(self.pilaO) > 0):
            return self.pilaO[len(self.pilaO)-1]
        else:
            return None

    def pTypes_top(self):
        if(len(self.pTypes) > 0):
            return self.pTypes[len(self.pTypes)-1]
        else:
            return None
    
    def pSaltos_top(self):
        if(len(self.pSaltos) > 0):
            return self.pSaltos[len(self.pSaltos)-1]
        else:
            return None

    # When an operator is found it creates the quadruple
    def found_operator(self, operator, location):
        operator = self.poper.pop()

        r_type = self.pTypes.pop()
        l_type = self.pTypes.pop()

        try:
            res_type = SEMANTIC[l_type][r_type][operator]

            self.pTypes.append(res_type)

            r_operand = self.pilaO.pop()
            l_operand = self.pilaO.pop()

            va = virtualAddress.setAddress(res_type, f'temp{location}')

            # print(f"{operator}, {l_operand}, {r_operand}, t{self.counter}")
            # self.generateQuad(operator, l_operand, r_operand, self.counter)
            # self.pilaO.append(self.counter)
            # self.increment_counter()

            self.generateQuad(operator, l_operand, r_operand, va)
            self.pilaO.append(va)

        except:
            print('Error in operator')
            exit()
    
    # When the call is returned, it creates an quadruple with equal. 
    def found_equal(self):
        operator = self.poper.pop()

        r_type = self.pTypes.pop()
        l_type = self.pTypes.pop()

        try:
            res_type = SEMANTIC[l_type][r_type][operator]

            r_operand = self.pilaO.pop()
            l_operand = self.pilaO.pop()

            # print(f"{operator}, t{r_operand}, null, {l_operand}")
            self.generateQuad(operator, r_operand, 'empty', l_operand)
        except:
            print('Error in equal')
            exit()

    # QUADRUPLE GENERATION AND FILL FUNCTIONS (GOTOs)
    def generateQuad(self, operator, left_operand, right_operand, result):
        self.quadruples.append([operator, left_operand, right_operand, result])
        self.quad_counter = self.quad_counter + 1

    def fillQuad(self, index, val):
        self.quadruples[index][3] = val

    
    # FUNCTIONS FOR IF, ELSE 
    def createIf(self, tag):
        print(self.pTypes)
        if(self.pTypes.pop() != "bool"): 
            print('Expected boolean exp')
            exit()

        oper = self.pilaO.pop()
        
        self.pSaltos.append(self.quad_counter)
        self.generateQuad(tag, oper, None, None)

    def if_end(self):
        # 1 - Pop pSaltos
        jump = self.pSaltos.pop()
        # 2 - Guarda contador actual en pSaltos
        self.pSaltos.append(self.quad_counter)
        # 3 - Genera GOTO para el else
        self.generateQuad('GOTO', None, None, None)
        # 4 - Rellena jump: GOTOF original con valor del contador actual
        self.fillQuad(jump, self.quad_counter)
    
    def else_end(self):
        jump = self.pSaltos.pop()
        self.fillQuad(jump, self.quad_counter)

    
    # FOR FUNCTIONS
    def for_equal_exp(self):
        exp_type = self.pTypes.pop()
        exp_res = self.pilaO.pop()

        # Debe ser solo entera
        if not ( numerical(exp_type) ):
            print(f"Variable \"{exp_type}\" no numerica ")
            exit()
	
        v_control = self.pilaO_top()
        v_control_type = self.pTypes_top()

        # NO SEGURO SI DEJAR O BORRAR
        self.pilaO.append(v_control) # Para poder luego incrementarla
        self.pTypes.append(v_control_type) # Para poder luego incrementarla

        res_type = SEMANTIC[v_control_type][exp_type]["="] # Error if result not found

        self.generateQuad("=", exp_res, None, v_control)
    
    # < comparison 
    def for_comparison(self, location):
        exp_type = self.pTypes.pop()
        exp_res = self.pilaO.pop()

        if not(numerical(exp_type)):
            print(f"Variable \"{exp_type}\" no numerica ")
            exit()
        
        # CREATE v_final
        v_final_va = virtualAddress.setAddress(exp_type, f'temp{location}')
        self.generateQuad('=', exp_res, None, v_final_va)

        # COMPARE v_control with v_final
        v_control = self.pilaO_top()
        va = virtualAddress.setAddress('bool', f'temp{location}')

        # self.generateQuad('<', v_control, 'v_final', self.counter)
        # self.increment_counter()
        self.generateQuad('<', v_control, v_final_va, va)

        self.pSaltos.append(self.quad_counter-1)
        # self.generateQuad('GOTOF', self.counter - 1, None, None)
        self.generateQuad('GOTOF', va , None, None)
        
        self.pSaltos.append(self.quad_counter-1)
    
    # for loop end
    def for_end(self, location, address_one):
        v_control = self.pilaO.pop()
        v_control_type = self.pTypes.pop()

        # USING COUNTER
        # self.generateQuad('+', v_control, 1, self.counter) 
        # self.generateQuad('=', self.counter, None, v_control)
        # self.generateQuad('=', self.counter, None, self.pilaO_top())
        # self.increment_counter()

        va = virtualAddress.setAddress('bool', f'temp{location}')

        # USING VIRTUAL ADDRESS
        self.generateQuad('+', v_control, address_one, va) 
        self.generateQuad('=', va, None, v_control)
        self.generateQuad('=', va, None, self.pilaO_top())

        end = self.pSaltos.pop()
        ret = self.pSaltos.pop()

        self.generateQuad('GOTO', None, None, ret)
        self.fillQuad(end, self.quad_counter)

        # ELIM COUNTER
        self.pilaO.pop()
        self.pTypes.pop()


        

################ AUX FUNCTIONS ################
def numerical(val):
	if (val != "int" and val != "float"):
			return False
	else:
		return True

################ END OF AUX FUNCTIONS ################