from collections import deque

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



    # VALUES = { _ , _ , _ , _ }
    # IF NO VALUE SEND IT AS "NULL"

    def generateQuad(self, operator, left_operand, right_operand, result):
        # print(values)
        self.quadruples.append([operator, left_operand, right_operand, result])

    def fillQuad(self, index, val):
        self.quadruples[index][3] = val
