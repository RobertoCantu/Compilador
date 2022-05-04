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



    # VALUES = { _ , _ , _ , _ }
    # IF NO VALUE SEND IT AS "NULL"

    def generate(self, values):
        print(values)
        self.quadruples.append(values)
