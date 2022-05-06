from collections import deque
from cube import SEMANTIC

'''
deque = stack 

s.append(x) --> pushes into top of stack
s.pop() --> pops top of


QUADRUPLES --> LIST

Pila de Operadores
poper

Pila de Operandos
pilaO

Pila de tipos
pTypes

Pila de Saltos
pSaltos 

'''

class Quadruple:

    def __init__(self):
        self.quadruples = []
        self.poper = deque()
        self.pilaO = deque()
        self.pTypes = deque()
        self.pSaltos = deque()
        self.counter = 666


    # FUNCTIONS ADD TO STACKS 
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
    def found_operator(self, operator):
        operator = self.poper.pop()

        r_type = self.pTypes.pop()
        l_type = self.pTypes.pop()

        try:
            res_type = SEMANTIC[l_type][r_type][operator]

            # print(res_type)

            self.pTypes.append(res_type)

            r_operand = self.pilaO.pop()
            l_operand = self.pilaO.pop()


            # print(f"{operator}, {l_operand}, {r_operand}, t{self.counter}")
            self.quadruples.append([operator, l_operand, r_operand, self.counter])
            self.pilaO.append(self.counter)
            self.counter = self.counter + 1

        except:
            print('Error')
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
            self.quadruples.append([operator, 'empty', r_operand, l_operand])


        except:
            print('Error')
            exit()


    # VALUES = { _ , _ , _ , _ }
    # IF NO VALUE SEND IT AS "NULL"

    def generateQuad(self, operator, left_operand, right_operand, result):
        # print(values)
        self.quadruples.append([operator, left_operand, right_operand, result])

    def fillQuad(self, index, val):
        self.quadruples[index][3] = val
