from audioop import add
from glob import glob
from locale import currency
from operator import le
import pickle
from collections import deque
from tabnanny import check
from threading import local

# Define same memory bases as the compiler
int_local_base = 5000
float_local_base = 6000
char_local_base = 7000
bool_local_base = 8000

int_local_temp_base = 13000
float_local_temp_base = 14000
char_local_temp_base = 15000
bool_local_temp_base = 16000

class Memory():
  def __init__(self):
    self.data = {}

  def insert(self, address, value):
    self.data[address] = value

  def get_value_by_address(self, address):
    if (address in self.data):
      return self.data[address]

    else:
      print("Runtime error")
      # exit()
  
  def get_all_memory(self):
    return self.data
  
  def printMemory(self):
    print(self.data)

    
# Loads code
objectCodeData = None
with open('object.p', 'rb') as handle:
  objectCodeData = pickle.load(handle)

quads = objectCodeData['quadruples']
dirFunc = objectCodeData['dirFunc']
constantsTable = objectCodeData['constantsTable']

# Global memory definition, Data segment
global_memory = Memory()

# Stack Segment for local scopes
local_memory = []
curr_local_memory = None

# Extra Segment for global temp and constants
extra_memory = Memory()

# Load extra segment with constants
for key, value in constantsTable.items():
  extra_memory.insert(value['address'], value['name'])


def get_quad(quads, index):
  return quads[index]

def insert_to_memory(address,value):
  # Global address range
  if(address >= 1000 and address <=4999):
    global_memory.insert(address,value)

  # Local - Local Memory
  if(address >= 5000 and address <=8999):
    # Get top of stack
    curr_local_memory.insert(address, value)

  # Local temp - Local Memory
  if(address >= 13000 and address <=16999):
    # Get top of stack
    curr_local_memory.insert(address, value)

  # Constant address range
  if(address >= 17000 and address <= 20999):
    extra_memory.insert(address, value)

  # Global temporal
  if(address >= 9000 and address <= 12999):
    extra_memory.insert(address, value)

def get_val_from_memory(address, get_just_address= False):
  # Global address range
  # Hay que corregir esto, es un parche bien feo mientras
  if(get_just_address):
    return address
  # Global memory
  if(address >= 1000 and address <=4999):
    return global_memory.get_value_by_address(address)

  # Local - Local Memory
  if(address >= 5000 and address <=8999):
    return curr_local_memory.get_value_by_address(address)

  # Local temp - Local Memory
  if(address >= 13000 and address <=16999):
    return curr_local_memory.get_value_by_address(address)

  # Constant address range - Extra memory
  if(address >= 17000 and address <= 20999):
    return extra_memory.get_value_by_address(address)

  # Global temporal - Extra memory
  if(address >= 9000 and address <= 12999):
    return extra_memory.get_value_by_address(address)

ip = 0
i = 0
checkpoint = []

curr_quad = get_quad(quads,ip)
saltos = deque() # STACK FOR JUMPS WITH FUNCTIONS

while(curr_quad[0] != 'END'):
  # print("Memoria local array: ", local_memory)
  curr_quad = get_quad(quads, ip)

  # print(f'{ip}: {curr_quad}')

  # Switch
  # Assign
  if(curr_quad[0] == '='):
    val_to_assign = get_val_from_memory(curr_quad[1])
    res_dir = get_val_from_memory(curr_quad[3], get_just_address = True)
    insert_to_memory(res_dir, val_to_assign)
    ip +=1

  # Arithmetic operations
  elif(curr_quad[0] == '+'):
    left_value = get_val_from_memory(curr_quad[1])
    right_value = get_val_from_memory(curr_quad[2])
    temp_address = curr_quad[3]
    insert_to_memory(temp_address, left_value + right_value)
    ip +=1


  elif(curr_quad[0] == '-'):
    left_value = get_val_from_memory(curr_quad[1])
    right_value = get_val_from_memory(curr_quad[2])
    temp_address = curr_quad[3]
    insert_to_memory(temp_address, left_value - right_value)
    ip +=1


  elif(curr_quad[0] == '*'):
    left_value = get_val_from_memory(curr_quad[1])
    right_value = get_val_from_memory(curr_quad[2])
    temp_address = curr_quad[3]
    insert_to_memory(temp_address, left_value * right_value)
    ip +=1

  elif(curr_quad[0] == '/'):
    left_value = get_val_from_memory(curr_quad[1])
    right_value = get_val_from_memory(curr_quad[2])
    temp_address = curr_quad[3]
    insert_to_memory(temp_address, left_value / right_value)
    ip +=1
  
  # Comparison operations
  elif(curr_quad[0] == '=='):
    left_value = get_val_from_memory(curr_quad[1])
    right_value = get_val_from_memory(curr_quad[2])
    temp_address = curr_quad[3]
    insert_to_memory(temp_address, left_value == right_value)
    ip += 1

  elif(curr_quad[0] == '!='):
    left_value = get_val_from_memory(curr_quad[1])
    right_value = get_val_from_memory(curr_quad[2])
    temp_address = curr_quad[3]
    insert_to_memory(temp_address, left_value != right_value)
    ip += 1

  elif(curr_quad[0] == '<'):
    left_value = get_val_from_memory(curr_quad[1])
    right_value = get_val_from_memory(curr_quad[2])
    temp_address = curr_quad[3]
    insert_to_memory(temp_address, left_value < right_value)
    ip += 1

  elif(curr_quad[0] == '<='):
    left_value = get_val_from_memory(curr_quad[1])
    right_value = get_val_from_memory(curr_quad[2])
    temp_address = curr_quad[3]
    insert_to_memory(temp_address, left_value <= right_value)
    ip += 1

  elif(curr_quad[0] == '>='):
    left_value = get_val_from_memory(curr_quad[1])
    right_value = get_val_from_memory(curr_quad[2])
    temp_address = curr_quad[3]
    insert_to_memory(temp_address, left_value >= right_value)
    ip += 1
  
  elif(curr_quad[0] == '>'):
    left_value = get_val_from_memory(curr_quad[1])
    right_value = get_val_from_memory(curr_quad[2])
    temp_address = curr_quad[3]
    insert_to_memory(temp_address, left_value > right_value)
    ip += 1

  # Logical operator
  elif(curr_quad[0] == '&&'):
    left_value = get_val_from_memory(curr_quad[1])
    right_value = get_val_from_memory(curr_quad[2])
    temp_address = curr_quad[3]
    res_bool = None
    if(left_value == True and right_value == True):
      res_bool = True
    else:
      res_bool = False
    insert_to_memory(temp_address, res_bool)
    ip += 1

  elif(curr_quad[0] == '||'):
    left_value = get_val_from_memory(curr_quad[1])
    right_value = get_val_from_memory(curr_quad[2])
    temp_address = curr_quad[3]
    res_bool = None
    if(left_value == True or right_value == True):
      res_bool = True
    else:
      res_bool = False
    insert_to_memory(temp_address, res_bool)
    ip += 1

  # Console operations
  elif(curr_quad[0] == 'WRITE'):
    val = get_val_from_memory(curr_quad[3])
    print(val)
    ip += 1

  elif(curr_quad[0] == 'READ'):
    res = input()
    address = get_val_from_memory(curr_quad[3], get_just_address = True)
    # Check flavor of memory
    if(address >= 1000 and address <=1999 or address >= 5000 and address <=5999):
      res = int(res)
    elif(address >= 2000 and address <=2999 or address >= 6000 and address <=6999):
      res = float(res)
    elif(address >= 3000 and address <=3999 or address >= 7000 and address <=7999):
      res = str(res)
    insert_to_memory(address, res)
    ip += 1

  # Goto's
  elif(curr_quad[0] == 'GOTO'):
    ip = curr_quad[3]
  
  elif(curr_quad[0] == 'GOTOF'):
    cond = get_val_from_memory(curr_quad[1])

    if cond == False:
      ip = curr_quad[3]
    elif cond == True:
      ip += 1
  
  elif(curr_quad[0] == 'ERA'):
    # Create space memory
    new_space = Memory()
    # Points to new space of memory
    curr_local_memory = new_space
    # Add new space to stack
    local_memory.append(new_space)
    # Obtain name of function
    function_name = curr_quad[1]
    # Obtain required locals
    locals = dirFunc[function_name]['localsUsed']
    ints = locals['int']
    floats = locals['float']
    chars = locals['char']
    bools = locals['bool']
    # Obtain required temp locals
    temp_locals = dirFunc[function_name]['usedTemp']
    ints_temp = temp_locals['int']
    floats_temp = temp_locals['float']
    chars_temp = temp_locals['char']
    bools_temp = temp_locals['bool']

    # Set space base on size
    for i in range(ints):
      new_space.get_all_memory()[int_local_base + i] = None
      
    for i in range(floats):
      new_space.get_all_memory()[float_local_base + i] = None
      
    for i in range(chars):
      new_space.get_all_memory()[char_local_base + i] = None

    for i in range(bools):
      new_space.get_all_memory()[bool_local_base + i] = None

    for i in range(ints_temp):
     new_space.get_all_memory()[int_local_temp_base + i] = None

    for i in range(floats_temp):
      new_space.get_all_memory()[float_local_temp_base + i] = None

    for i in range(chars_temp):
      new_space.get_all_memory()[char_local_temp_base + i] = None

    for i in range(bools_temp):
      new_space.get_all_memory()[bool_local_temp_base + i] = None
    
    print("Memoria Local Inicial")
    new_space.printMemory()
    ip += 1
  
  elif(curr_quad[0] == 'PARAMETER'):
    # Obtain paramater index
    paramIndex = curr_quad[3] - 1
    # Convert dict to list of keys
    adress_keys = list(curr_local_memory.get_all_memory())
    # Get  address of formal param
    address = adress_keys[paramIndex]
    # Obtain value from extra memory
    argument_value = extra_memory.get_value_by_address(curr_quad[1])
    # Insert argument to formal param
    insert_to_memory(address, argument_value)
    ip += 1
  
  elif(curr_quad[0] == 'GOSUB'): # Need to asign ARGUMENTS  to PARAMETERS
    # Save the current IP
    checkpoint.append(ip)
    # saltos.append(ip+1)
    ip = curr_quad[3]

  elif(curr_quad[0] == 'ENDFUNC'):
    # Print before erasing local memory
    print("Memoria local antes de destruirse")
    curr_local_memory.printMemory()
    # Erase local memory
    local_memory.pop()
    # Update current memory
    if(len(local_memory) > 0):
      curr_local_memory = local_memory[-1]
    else:
      curr_local_memory = None

    ip =  checkpoint.pop() + 1
    # ip = saltos.pop()
  
  elif(curr_quad[0] == 'RETURN'):
    ip += 1
  
  i += 1
print('Memoria global')
global_memory.printMemory()


