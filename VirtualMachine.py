from audioop import add
from glob import glob
from locale import currency
import pickle

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

  if(address >= 1000 and address <=4999):
    return global_memory.get_value_by_address(address)

  # Constant address range
  if(address >= 17000 and address <= 20999):
    return extra_memory.get_value_by_address(address)

  # Global temporal
  if(address >= 9000 and address <= 12999):
    return extra_memory.get_value_by_address(address)

ip = 0
i=0

curr_quad = get_quad(quads,ip)

while(i < len(quads)):

  curr_quad = get_quad(quads,ip)

  # Switch
  if(curr_quad[0] == '='):
    val_to_assign = get_val_from_memory(curr_quad[1])
    res_dir = get_val_from_memory(curr_quad[3], get_just_address = True)
    insert_to_memory(res_dir, val_to_assign)
    ip +=1


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


  elif(curr_quad[0] == 'WRITE'):
    val = get_val_from_memory(curr_quad[3])
    print(val)
    ip +=1


  elif(curr_quad[0] == 'GOTO'):
    ip = curr_quad[3]

  i += 1
print('Memoria global')
global_memory.printMemory()

