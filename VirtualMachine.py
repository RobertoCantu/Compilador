from audioop import add
from glob import glob
from locale import currency
# from msilib.schema import Error
from operator import le
import pickle
from collections import deque
from tabnanny import check
from threading import local
from error import RuntimeError

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
  def __init__(self, intSize = 0, floatSize = 0, charSize = 0, boolSize = 0, pointerSize = 0):
    self.data = [[None] * intSize,[None] * floatSize,[None] * charSize,[None] * boolSize, [None] * pointerSize]

  def insert(self, address, value, type):
    if(type == 'int'):
      self.data[0][address] = value

    elif(type == 'float'):
      self.data[1][address] = value

    elif(type == 'char'):
      self.data[2][address] = value

    elif(type == 'bool'):
      self.data[3][address] = value

    elif(type == 'pointer'):
      self.data[4][address] = value

  def get_value_by_address(self, address):
    if (address in self.data):
      return self.data[address]

    else:
      print("Runtime error")
      # exit()
  
  def return_memory_space(self, type):
    if(type == 'int'):
      return self.data[0]

    elif(type == 'float'):
      return self.data[1]

    elif(type == 'char'):
      return self.data[2]

    elif(type == 'bool'):
      return self.data[3]

    elif(type == 'pointer'):
      return self.data[4]
  
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

# Count total of globals vars
int_global_size = dirFunc['globalsUsed']['int']
float_global_size = dirFunc['globalsUsed']['float']
char_global_size = dirFunc['globalsUsed']['char']
bool_global_size = dirFunc['globalsUsed']['bool']

# Create global memory
global_memory = Memory(int_global_size, float_global_size, char_global_size, bool_global_size)

# Stack Segment for local scopes
local_memory = []

#[   [Mem1,Mem2]]
curr_local_memory = []

# Extra Segment Definition for global temp and constants Position 0 equals to constants and Position 1 equals to temp globals
extra_memory = []
const_mem = Memory()

# Create constant Memory
for key, value in constantsTable.items():
  #Add it to list of constants ints
  if(value['address'] >= 17000 and value['address'] <= 17999):
    const_mem.return_memory_space("int").append(value['name'])

  #Add it to list of constants floats
  elif(value['address'] >= 18000 and value['address'] <= 18999):
    const_mem.return_memory_space("float").append(value['name'])

  #Add it to list of constants chars
  elif(value['address'] >= 19000 and value['address'] <= 19999):
   const_mem.return_memory_space("char").append(value['name'])

  #Add it to list of constants bools
  elif(value['address'] >= 20000 and value['address'] <= 20999):
    const_mem.return_memory_space("bool").append(value['name'])

# Count temp globals
int_global_temp_size = dirFunc['globalsTempUsed']['int']
float_global_temp_size = dirFunc['globalsTempUsed']['float']
char_global_temp_size = dirFunc['globalsTempUsed']['char']
bool_global_temp_size = dirFunc['globalsTempUsed']['bool']
pointer_global_temp_size = dirFunc['globalsTempUsed']['pointer']

# Create global temp Memory
temp_global_mem = Memory(int_global_temp_size, float_global_temp_size, char_global_temp_size, bool_global_temp_size, pointer_global_temp_size)
# Create extra Memory 
extra_memory.append(const_mem)
extra_memory.append(temp_global_mem)

##################################################################
def get_quad(quads, index):
  return quads[index]

##################################################################
def insert_to_memory(address,value):
  # Globals logic
  # Insert global int
  if(address >= 1000 and address <= 1999):
    global_memory.insert(address-1000, value, 'int')
    
  # Insert global float
  elif(address >= 2000 and address <= 2999):
    global_memory.insert(address-2000, value, 'float')

  # Insert global char
  elif(address >= 3000 and address <= 3999):
    global_memory.insert(address-3000, value, 'char')

  # Insert global bool
  elif(address >= 4000 and address <= 4999):
    global_memory.insert(address-3000, value, 'bool')
###############################################################
  # Local - Local Memory
  # Insert Local temp int
  if(address >= 5000 and address <= 5999):
    curr_local_memory[0].insert(address - 5000, value, "int")

  # Insert Local temp float
  elif(address >= 6000 and address <= 6999):
    curr_local_memory[0].insert(address - 6000, value, "float")

  # Insert Local temp char
  elif(address >= 7000 and address <= 7999):
    curr_local_memory[0].insert(address - 7000, value, "char")

  # Insert Local temp bool
  elif(address >= 8000 and address <= 8999):
    curr_local_memory[0].insert(address - 8000, value, "bool")
####################################################################
  # Local temp - Local Memory
  # Insert Local temp int
  if(address >= 13000 and address <= 13999):
    curr_local_memory[1].insert(address - 13000, value, "int")

  # Insert Local temp float
  elif(address >= 14000 and address <= 14999):
    curr_local_memory[1].insert(address - 14000, value, "float")

  # Insert Local temp char
  elif(address >= 15000 and address <= 15999):
    curr_local_memory[1].insert(address - 15000, value, "char")

  # Insert Local temp bool
  elif(address >= 16000 and address <= 16999):
    curr_local_memory[1].insert(address - 16000, value, "bool")
######################################################################
  # Insert global temp int
  if(address >= 9000 and address <= 9999):
    extra_memory[1].insert(address - 9000, value, "int")

  # Insert global temp float
  elif(address >= 10000 and address <= 10999):
    extra_memory[1].insert(address - 10000, value, "float")

  # Insert global temp char
  elif(address >= 11000 and address <= 11999):
    extra_memory[1].insert(address - 11000, value, "char")

  # Insert global temp bool
  elif(address >= 12000 and address <= 12999):
    extra_memory[1].insert(address - 12000, value, "bool")

  # Insert global temp pointer
  elif(address >= 70000 and address <= 70999):
    extra_memory[1].insert(address - 70000, value, "pointer")    

################################################################
def get_val_from_memory(address, get_just_address= False):
  # Global address range
  # Hay que corregir esto, es un parche bien feo mientras
  if(get_just_address):
    return address

  # Globals logic
  # Return global int
  if(address >= 1000 and address <= 1999):
    return global_memory.return_memory_space("int")[address - 1000]

  # Return global float
  elif(address >= 2000 and address <= 2999):
    return global_memory.return_memory_space("float")[address - 2000]

  # Return global char
  elif(address >= 3000 and address <= 3999):
    return global_memory.return_memory_space("char")[address - 3000]

  # Return global bool
  elif(address >= 4000 and address <= 4999):
    return global_memory.return_memory_space("bool")[address - 3000]

  # Local - Local Memory
  # Local  logic
  # Return Local int
  if(address >= 5000 and address <= 5999):
    value = curr_local_memory[0].return_memory_space("int")[address - 5000]
    if(value == None):
      # Look one space of memory behind
      last_call_memory = local_memory[len(local_memory) - 2]
      value = last_call_memory[0].return_memory_space("int")[address - 5000]
      return value
    return value
  # Return Local float
  elif(address >= 6000 and address <= 6999):
    value = curr_local_memory[0].return_memory_space("float")[address - 6000]
    if(value == None):
      # Look one space of memory behind
      last_call_memory = local_memory[len(local_memory) - 2]
      value = last_call_memory[0].return_memory_space("float")[address - 6000]
      return value
    return value
  # Return Local char
  elif(address >= 7000 and address <= 7999):
    value = curr_local_memory[0].return_memory_space("char")[address - 7000]
    if(value == None):
      # Look one space of memory behind
      last_call_memory = local_memory[len(local_memory) - 2]
      value = last_call_memory[0].return_memory_space("char")[address - 7000]
      return value
    return value
  # Return Local bool
  elif(address >= 8000 and address <= 8999):
    value = curr_local_memory[0].return_memory_space("bool")[address - 8000]
    if(value == None):
      # Look one space of memory behind
      last_call_memory = local_memory[len(local_memory) - 2]
      value = last_call_memory[0].return_memory_space("bool")[address - 8000]
      return value
    return value
  
  # Local temp logic - Local Memory
  # Return Local temp  int
  if(address >= 13000 and address <= 13999):
    return curr_local_memory[1].return_memory_space("int")[address - 13000]

  # Return Local temp  float
  elif(address >= 14000 and address <= 14999):
    return curr_local_memory[1].return_memory_space("float")[address - 14000]

  # Return Local temp  char
  elif(address >= 15000 and address <= 15999):
    return curr_local_memory[1].return_memory_space("char")[address - 15000]

  # Return Local temp  bool
  elif(address >= 16000 and address <= 16999):
    return curr_local_memory[1].return_memory_space("bool")[address - 16000]

  # Constans logic -- Extra memory
  # Return constant int
  if(address >= 17000 and address <= 17999):
    return extra_memory[0].return_memory_space("int")[address - 17000]

  # Return constant float
  elif(address >= 18000 and address <= 18999):
    return extra_memory[0].return_memory_space("float")[address - 18000]

  # Return constant char
  elif(address >= 19000 and address <= 19999):
    return extra_memory[0].return_memory_space("char")[address - 19000]

  # Return constant bool
  elif(address >= 20000 and address <= 20999):
    return extra_memory[0].return_memory_space("bool")[address - 20000]

  # Globals temporal logic -- Extra memory
  # Return global temp  int
  if(address >= 9000 and address <= 9999):
    return extra_memory[1].return_memory_space("int")[address - 9000]

  # Return global temp float
  elif(address >= 10000 and address <= 10999):
    return extra_memory[1].return_memory_space("float")[address - 10000]

  # Return global temp  char
  elif(address >= 11000 and address <= 11999):
    return extra_memory[1].return_memory_space("char")[address - 11000]

  # Return global temp  bool
  elif(address >= 12000 and address <= 12999):
    return extra_memory[1].return_memory_space("bool")[address - 12000]

  # !!!!!!!!!!!!!!!! This is a global temp pointer
  elif(address >= 70000 and address <= 70999):
    return extra_memory[1].return_memory_space("pointer")[address - 70000]
  

# def insert_to_memory_pointer(address, value):
#   real_address = get_val_from_memory(address)
#   insert_to_memory(real_address, value)

def get_val(address, get_just_address= False):
  
  if(get_just_address):
    if(address >= 70000):
      address = get_val_from_memory(address)
    return address

  if(address >= 70000):
      address = get_val_from_memory(address)

  ret_value = get_val_from_memory(address)

  return ret_value

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

    # val_to_assign = get_val_from_memory(curr_quad[1])
    val_to_assign = get_val(curr_quad[1])
    
    res_dir = curr_quad[3]

    # Careful this is a pointer
    # if(res_dir >= 70000):
      # real_address= get_val_from_memory(res_dir)
      # insert_to_memory(real_address, val_to_assign)
    # else:
      # insert_to_memory(res_dir, val_to_assign)
    
    insert_to_memory(get_val(res_dir, True), val_to_assign)
    ip +=1

  # Arithmetic operations
  elif(curr_quad[0] == '+'):

    left_value = get_val(curr_quad[1])
    right_value = get_val(curr_quad[2])
    
    temp_address = curr_quad[3]

    try:
      insert_to_memory(temp_address, left_value + right_value)
    except:
      raise RuntimeError("Variable sin valor asignado")
    ip +=1


  elif(curr_quad[0] == '-'):
    # print(curr_quad)
    left_value = get_val(curr_quad[1])
    right_value = get_val(curr_quad[2])
    temp_address = curr_quad[3]
    try:
      insert_to_memory(temp_address, left_value - right_value)
    except:
      raise RuntimeError("Variable sin valor asignado")
    ip +=1


  elif(curr_quad[0] == '*'):
    left_value = get_val(curr_quad[1])
    right_value = get_val(curr_quad[2])
    temp_address = curr_quad[3]
    try:
      insert_to_memory(temp_address, left_value * right_value)
    except:
      raise RuntimeError("Variable sin valor asignado")
    ip +=1

  elif(curr_quad[0] == '/'):
    left_value = get_val(curr_quad[1])
    right_value = get_val(curr_quad[2])
    temp_address = curr_quad[3]
    try:
      insert_to_memory(temp_address, left_value / right_value)
    except ZeroDivisionError:
      raise ZeroDivisionError("Semantic Error: Division entre 0")
    except:
      raise RuntimeError("Variable sin valor asignado")
    ip +=1
  
  # Comparison operations
  elif(curr_quad[0] == '=='):
    left_value = get_val(curr_quad[1])
    right_value = get_val(curr_quad[2])
    temp_address = curr_quad[3]
    insert_to_memory(temp_address, left_value == right_value)
    ip += 1

  elif(curr_quad[0] == '!='):
    left_value = get_val(curr_quad[1])
    right_value = get_val(curr_quad[2])
    temp_address = curr_quad[3]
    insert_to_memory(temp_address, left_value != right_value)
    ip += 1

  elif(curr_quad[0] == '<'):
    left_value = get_val(curr_quad[1])
    right_value = get_val(curr_quad[2])
    temp_address = curr_quad[3]
    insert_to_memory(temp_address, left_value < right_value)
    ip += 1

  elif(curr_quad[0] == '<='):
    left_value = get_val(curr_quad[1])
    right_value = get_val(curr_quad[2])
    temp_address = curr_quad[3]
    insert_to_memory(temp_address, left_value <= right_value)
    ip += 1

  elif(curr_quad[0] == '>='):
    left_value = get_val(curr_quad[1])
    right_value = get_val(curr_quad[2])
    temp_address = curr_quad[3]
    insert_to_memory(temp_address, left_value >= right_value)
    ip += 1
  
  elif(curr_quad[0] == '>'):
    left_value = get_val(curr_quad[1])
    right_value = get_val(curr_quad[2])
    temp_address = curr_quad[3]
    insert_to_memory(temp_address, left_value > right_value)
    ip += 1

  # Logical operator
  elif(curr_quad[0] == '&&'):
    left_value = get_val(curr_quad[1])
    right_value = get_val(curr_quad[2])
    temp_address = curr_quad[3]
    res_bool = None
    if(left_value == True and right_value == True):
      res_bool = True
    else:
      res_bool = False
    insert_to_memory(temp_address, res_bool)
    ip += 1

  elif(curr_quad[0] == '||'):
    left_value = get_val(curr_quad[1])
    right_value = get_val(curr_quad[2])
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
    if(curr_quad[3] >= 70000):
      real_address = get_val_from_memory(curr_quad[3])
      val = get_val_from_memory(real_address)
    else:
      val = get_val_from_memory(curr_quad[3])
    new_string=str(val).replace('"','')

    if(new_string == '\\n'):
      print('\n')
    else:
      print((new_string), end=' ')
    ip += 1

  elif(curr_quad[0] == 'READ'):
    res = input()
    address = curr_quad[3]
    # Check flavor of memory
    if(address >= 1000 and address <=1999 or address >= 5000 and address <=5999 or address >= 70000):
      res = int(res)
    elif(address >= 2000 and address <=2999 or address >= 6000 and address <=6999):
      res = float(res)
    elif(address >= 3000 and address <=3999 or address >= 7000 and address <=7999):
      res = str(res)
    insert_to_memory(get_val(address, True), res)
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
    curr_local_memory = []
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

    # Create space memory
    new_local_memory = Memory(ints, floats, chars, bools)
    new_local_temp_memory = Memory(ints_temp, floats_temp, chars_temp, bools_temp)
    # Points to new space of memory
    curr_local_memory.append(new_local_memory)
    curr_local_memory.append(new_local_temp_memory)
    # Add new space to stack
    local_memory.append(curr_local_memory)

    # Create counters useful for managing parameters
    int_count = 0
    float_count = 0
    char_count = 0
    bool_count = 0
    ip += 1
  
  elif(curr_quad[0] == 'PARAMETER'):
    # Signature
    params_table = dirFunc[function_name]["paramsTable"]
    # Obtain paramater index
    paramIndex = curr_quad[3] - 1
    argument_type = params_table[paramIndex]
    # Get address of formal param
    if(argument_type == 'int'):
      address = 5000 + int_count
      int_count += 1

    elif(argument_type == 'float'):
      address = 6000 + float_count
      float_count += 1

    elif(argument_type == 'char'):
      address = 7000 + char_count
      char_count += 1

    elif(argument_type == 'bool'):
      address = 8000 + bool_count
      bool_count += 1

    # Obtain value from memory
    argument_value = get_val_from_memory(curr_quad[1])
    # Insert argument to formal param
    insert_to_memory(address, argument_value)
    ip += 1
  
  elif(curr_quad[0] == 'GOSUB'): # Need to asign ARGUMENTS  to PARAMETERS
    # Reset counter of params
    int_count   = 0
    float_count = 0
    char_count  = 0
    bool_count  = 0
    # Save the current IP
    checkpoint.append(ip)
    ip = curr_quad[3]

  elif(curr_quad[0] == 'ENDFUNC'):
    # Print before erasing local memory
    # print("Memoria local antes de destruirse")
    # curr_local_memory.printMemory()
    
    # Erase local memory
    local_memory.pop()
    # Update current memory
    if(len(local_memory) > 0):
      curr_local_memory = local_memory[-1]
    else:
      curr_local_memory = None

    ip =  checkpoint.pop() + 1
  
  elif(curr_quad[0] == 'RETURN'):
    ip += 1
  
  elif(curr_quad[0] == 'VERIFY'):
    check_value = get_val(curr_quad[1])
    upper_limit = get_val(curr_quad[3])

    if (check_value >= 0 and check_value < upper_limit):
      ip += 1
    else:
      raise RuntimeError("Fuera de rangos")

  
  i += 1


# print('Memoria global')
# global_memory.printMemory()


