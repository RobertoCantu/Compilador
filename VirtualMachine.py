import pickle
from error import RuntimeError

class Memory():
  def __init__(self, intSize = 0, floatSize = 0, stringSize = 0, boolSize = 0, pointerSize = 0):
    self.data = [[None] * intSize,[None] * floatSize,[None] * stringSize,[None] * boolSize, [None] * pointerSize]

  def insert(self, address, value, type):
    if(type == 'int'):
      self.data[0][address] = value

    elif(type == 'float'):
      self.data[1][address] = value

    elif(type == 'string'):
      self.data[2][address] = value

    elif(type == 'bool'):
      self.data[3][address] = value

    elif(type == 'pointer'):
      # print(self.data)
      self.data[4][address] = value

  def return_memory_space(self, type):
    if(type == 'int'):
      return self.data[0]

    elif(type == 'float'):
      return self.data[1]

    elif(type == 'string'):
      return self.data[2]

    elif(type == 'bool'):
      return self.data[3]

    elif(type == 'pointer'):
      return self.data[4]
  
  def printMemory(self):
    print(self.data)

class VirtualMachine():
  def __init__(self):
    self.global_memory = None # Data segment
    self.local_memory = [] # Stack Segment
    self.curr_local_memory = []
    self.extra_memory = [] # Extra Memory

  # Parameters for this function are total global int, float, string, bool used in compilation
  # Creates the global memory in the virtual machine
  def create_global_memory(self, int_size, float_size, string_size, bool_size):
    self.global_memory = Memory(int_size, float_size, string_size, bool_size )

  # Parameters for this function are the directoy of constants from compilation and the total int, float, bool , string temporal global used in compilation
  # Creates the extra memory in the virtual machine
  def create_extra_segment_memory(self, constant_table, int_global_temp_size, float_global_temp_size, string_global_temp_size, bool_global_temp_size, pointer_global_temp_size):
    const_mem = Memory()
    for key, value in constant_table.items():
      #Add it to list of constants ints
      if(value['address'] >= 17000 and value['address'] <= 17999):
        const_mem.return_memory_space("int").append(value['name'])

      #Add it to list of constants floats
      elif(value['address'] >= 18000 and value['address'] <= 18999):
        const_mem.return_memory_space("float").append(value['name'])

      #Add it to list of constants strings
      elif(value['address'] >= 19000 and value['address'] <= 19999):
        const_mem.return_memory_space("string").append(value['name'])

      #Add it to list of constants bools
      elif(value['address'] >= 20000 and value['address'] <= 20999):
        const_mem.return_memory_space("bool").append(value['name'])

    temp_global_mem = Memory(int_global_temp_size, float_global_temp_size, string_global_temp_size, bool_global_temp_size, pointer_global_temp_size)
    
    # Extra memory is now created
    self.extra_memory.append(const_mem)
    self.extra_memory.append(temp_global_mem)
  
  # This function receive as parameter the memory address and the value to insert
  # This funcion insert the value to the correct space memory base on address range
  # It does not return any value
  def insert_to_memory(self, address,value):
    # Globals logic
    # Insert global int
    if(address >= 1000 and address <= 1999):
      self.global_memory.insert(address-1000, value, 'int')
    # Insert global float
    elif(address >= 2000 and address <= 2999):
      self.global_memory.insert(address-2000, value, 'float')

    # Insert global string
    elif(address >= 3000 and address <= 3999):
      self.global_memory.insert(address-3000, value, 'string')

    # Insert global bool
    elif(address >= 4000 and address <= 4999):
      self.global_memory.insert(address-3000, value, 'bool')
  ###############################################################
    # Local - Local Memory
    # Insert Local temp int
    if(address >= 5000 and address <= 5999):
      # print(self.curr_local_memory)
      self.curr_local_memory[0].insert(address - 5000, value, "int")

    # Insert Local temp float
    elif(address >= 6000 and address <= 6999):
      self.curr_local_memory[0].insert(address - 6000, value, "float")

    # Insert Local temp string
    elif(address >= 7000 and address <= 7999):
      self.curr_local_memory[0].insert(address - 7000, value, "string")

    # Insert Local temp bool
    elif(address >= 8000 and address <= 8999):
      self.curr_local_memory[0].insert(address - 8000, value, "bool")
  ####################################################################
    # Local temp - Local Memory
    # Insert Local temp int
    if(address >= 13000 and address <= 13999):
      self.curr_local_memory[1].insert(address - 13000, value, "int")

    # Insert Local temp float
    elif(address >= 14000 and address <= 14999):
      self.curr_local_memory[1].insert(address - 14000, value, "float")

    # Insert Local temp string
    elif(address >= 15000 and address <= 15999):
      self.curr_local_memory[1].insert(address - 15000, value, "string")

    # Insert Local temp bool
    elif(address >= 16000 and address <= 16999):
      self.curr_local_memory[1].insert(address - 16000, value, "bool")
    
    # Insert local temp pointer
    elif(address >= 71000 and address <= 71999):
      # print(address-71000)
      self.curr_local_memory[1].insert(address - 71000, value, "pointer")  

  ######################################################################
    # Insert global temp int
    if(address >= 9000 and address <= 9999):
      self.extra_memory[1].insert(address - 9000, value, "int")

    # Insert global temp float
    elif(address >= 10000 and address <= 10999):
      self.extra_memory[1].insert(address - 10000, value, "float")

    # Insert global temp string
    elif(address >= 11000 and address <= 11999):
      self.extra_memory[1].insert(address - 11000, value, "string")

    # Insert global temp bool
    elif(address >= 12000 and address <= 12999):
      self.extra_memory[1].insert(address - 12000, value, "bool")

    # Insert global temp pointer
    elif(address >= 70000 and address <= 70999):
      self.extra_memory[1].insert(address - 70000, value, "pointer")

  # Parameters for this function is the memory adress
  # Base on memory ranges it finds the correct memory where the value is located
  # This function returns the value extracted from the correct memory space
  def get_val_from_memory(self, address):
    # Global address range
    # Globals logic
    # Return global int
    if(address >= 1000 and address <= 1999):
      return self.global_memory.return_memory_space("int")[address - 1000]

    # Return global float
    elif(address >= 2000 and address <= 2999):
      return  self.global_memory.return_memory_space("float")[address - 2000]

    # Return global string
    elif(address >= 3000 and address <= 3999):
      return  self.global_memory.return_memory_space("string")[address - 3000]

    # Return global bool
    elif(address >= 4000 and address <= 4999):
      return  self.global_memory.return_memory_space("bool")[address - 3000]

    # Local - Local Memory
    # Local  logic
    # Return Local int
    if(address >= 5000 and address <= 5999):
      # print(address)
      index = address - 5000
      if 0 <= index < len(self.curr_local_memory[0].return_memory_space("int")):
        value =  self.curr_local_memory[0].return_memory_space("int")[address - 5000] 
        if(value == None):
          # Look one space of memory behind
          last_call_memory = self.local_memory[len(self.local_memory) - 2]
          value =  last_call_memory[0].return_memory_space("int")[address - 5000]
          return value
        else:
          return value
      else:
        # Look one space of memory behind
        last_call_memory = self.local_memory[len(self.local_memory) - 2]
        value =  last_call_memory[0].return_memory_space("int")[address - 5000]
        return value
    # Return Local float
    elif(address >= 6000 and address <= 6999):
      index = address - 6000
      if 0 <= index < len(self.curr_local_memory[0].return_memory_space("float")):
        value =  self.curr_local_memory[0].return_memory_space("float")[address - 6000] 
        if(value == None):
          # Look one space of memory behind
          last_call_memory = self.local_memory[len(self.local_memory) - 2]
          value =  last_call_memory[0].return_memory_space("float")[address - 6000]
          return value
        else:
          return value
      else:
        # Look one space of memory behind
        last_call_memory = self.local_memory[len(self.local_memory) - 2]
        value =  last_call_memory[0].return_memory_space("float")[address - 5000]
        return value
    # Return Local string
    elif(address >= 7000 and address <= 7999):
      index = address - 7000
      if 0 <= index < len(self.curr_local_memory[0].return_memory_space("string")):
        value =  self.curr_local_memory[0].return_memory_space("string")[address - 7000] 
        if(value == None):
          # Look one space of memory behind
          last_call_memory = self.local_memory[len(self.local_memory) - 2]
          value =  last_call_memory[0].return_memory_space("string")[address - 7000]
          return value
        else:
          return value
      else:
        # Look one space of memory behind
        last_call_memory = self.local_memory[len(self.local_memory) - 2]
        value =  last_call_memory[0].return_memory_space("string")[address - 7000]
        return value
    # Return Local bool
    elif(address >= 8000 and address <= 8999):
      index = address - 8000
      if 0 <= index < len(self.curr_local_memory[0].return_memory_space("bool")):
        value =  self.curr_local_memory[0].return_memory_space("bool")[address - 8000] 
        if(value == None):
          # Look one space of memory behind
          last_call_memory = self.local_memory[len(self.local_memory) - 2]
          value =  last_call_memory[0].return_memory_space("bool")[address - 8000]
          return value
        else:
          return value
      else:
        # Look one space of memory behind
        last_call_memory = self.local_memory[len(self.local_memory) - 2]
        value =  last_call_memory[0].return_memory_space("bool")[address - 8000]
        return value   
    # Local temp logic - Local Memory
    # Return Local temp  int
    if(address >= 13000 and address <= 13999):
      return  self.curr_local_memory[1].return_memory_space("int")[address - 13000]

    # Return Local temp  float
    elif(address >= 14000 and address <= 14999):
      return  self.curr_local_memory[1].return_memory_space("float")[address - 14000]

    # Return Local temp  string
    elif(address >= 15000 and address <= 15999):
      return  self.curr_local_memory[1].return_memory_space("string")[address - 15000]

    # Return Local temp  bool
    elif(address >= 16000 and address <= 16999):
      return  self.curr_local_memory[1].return_memory_space("bool")[address - 16000]
      
    # Return Local temp pointer
    elif(address >= 71000 and address <= 71999):
      return  self.curr_local_memory[1].return_memory_space("pointer")[address - 71000]

    # Constans logic -- Extra memory
    # Return constant int
    if(address >= 17000 and address <= 17999):
      return  self.extra_memory[0].return_memory_space("int")[address - 17000]

    # Return constant float
    elif(address >= 18000 and address <= 18999):
      return  self.extra_memory[0].return_memory_space("float")[address - 18000]

    # Return constant string
    elif(address >= 19000 and address <= 19999):
      return  self.extra_memory[0].return_memory_space("string")[address - 19000]

    # Return constant bool
    elif(address >= 20000 and address <= 20999):
      return  self.extra_memory[0].return_memory_space("bool")[address - 20000]

    # Globals temporal logic -- Extra memory
    # Return global temp  int
    if(address >= 9000 and address <= 9999):
      return  self.extra_memory[1].return_memory_space("int")[address - 9000]

    # Return global temp float
    elif(address >= 10000 and address <= 10999):
      return  self.extra_memory[1].return_memory_space("float")[address - 10000]

    # Return global temp  string
    elif(address >= 11000 and address <= 11999):
      return  self.extra_memory[1].return_memory_space("string")[address - 11000]

    # Return global temp  bool
    elif(address >= 12000 and address <= 12999):
      return  self.extra_memory[1].return_memory_space("bool")[address - 12000]

    # Return global temp pointer
    elif(address >= 70000 and address <= 70999):
      return  self.extra_memory[1].return_memory_space("pointer")[address - 70000]

  # This function received as parameters the memory address and a boolean flag
  # If the flag is turn on the function return the address, this is useful
  # in cases such as in assigment operation
  # This function is very useful for pointers because it allows double indexing
  # If the flag is turn off it returns the value from the correct space memory
  def get_val(self, address, get_just_address= False):
    if(get_just_address):
      if(address >= 70000):
        address = self.get_val_from_memory(address)
      return address

    if(address >= 70000):
        address = self.get_val_from_memory(address)

    ret_value = self.get_val_from_memory(address)

    return ret_value

  # This function receive as parameter all que quadruples created in compilation
  # All the logic of opearation code is hanlde in ths function
  def start_machine(self, quads):
    ip = 0
    checkpoint = []

    def get_quad(quads, index):
      return quads[index]

    curr_quad = get_quad(quads, ip)

    while(curr_quad[0] != 'END'):
      curr_quad = get_quad(quads, ip)

      # Big Switch
      # Assign
      if(curr_quad[0] == '='):
        val_to_assign = self.get_val(curr_quad[1]) 
        res_dir = curr_quad[3]    
        self.insert_to_memory(self.get_val(res_dir, True), val_to_assign)
        ip +=1

      # Arithmetic operations
      elif(curr_quad[0] == '+'):

        left_value = self.get_val(curr_quad[1])
        right_value = self.get_val(curr_quad[2])
        temp_address = curr_quad[3]
        try:
          self.insert_to_memory(temp_address, left_value + right_value)
        except:
          raise RuntimeError("Variable without value")
        ip +=1

      elif(curr_quad[0] == '-'):
        # print(curr_quad)
        left_value = self.get_val(curr_quad[1])
        right_value = self.get_val(curr_quad[2])
        temp_address = curr_quad[3]
        try:
          self.insert_to_memory(temp_address, left_value - right_value)
        except:
          raise RuntimeError("Variable without value")
        ip +=1

      elif(curr_quad[0] == '*'):
        left_value = self.get_val(curr_quad[1])
        right_value = self.get_val(curr_quad[2])
        temp_address = curr_quad[3]
        try:
          self.insert_to_memory(temp_address, left_value * right_value)
        except:
          raise RuntimeError("Variable without value")
        ip +=1

      elif(curr_quad[0] == '/'):
        left_value = self.get_val(curr_quad[1])
        right_value = self.get_val(curr_quad[2])
        temp_address = curr_quad[3]
        try:
          self.insert_to_memory(temp_address, int(left_value / right_value))
        except ZeroDivisionError:
          raise ZeroDivisionError("RuntimeError: Division by 0")
        except:
          raise RuntimeError("Variable without value")
        ip +=1
        
      # Comparison operations
      elif(curr_quad[0] == '=='):
        left_value = self.get_val(curr_quad[1])
        right_value = self.get_val(curr_quad[2])
        temp_address = curr_quad[3]
        self.insert_to_memory(temp_address, left_value == right_value)
        ip += 1

      elif(curr_quad[0] == '!='):
        left_value = self.get_val(curr_quad[1])
        right_value = self.get_val(curr_quad[2])
        temp_address = curr_quad[3]
        self.insert_to_memory(temp_address, left_value != right_value)
        ip += 1

      elif(curr_quad[0] == '<'):
        left_value = self.get_val(curr_quad[1])
        right_value = self.get_val(curr_quad[2])
        temp_address = curr_quad[3]
        self.insert_to_memory(temp_address, left_value < right_value)
        ip += 1

      elif(curr_quad[0] == '<='):
        left_value = self.get_val(curr_quad[1])
        right_value = self.get_val(curr_quad[2])
        temp_address = curr_quad[3]
        self.insert_to_memory(temp_address, left_value <= right_value)
        ip += 1

      elif(curr_quad[0] == '>='):
        left_value = self.get_val(curr_quad[1])
        right_value = self.get_val(curr_quad[2])
        temp_address = curr_quad[3]
        self.insert_to_memory(temp_address, left_value >= right_value)
        ip += 1
        
      elif(curr_quad[0] == '>'):
        left_value = self.get_val(curr_quad[1])
        right_value = self.get_val(curr_quad[2])
        temp_address = curr_quad[3]
        self.insert_to_memory(temp_address, left_value > right_value)
        ip += 1

      # Logical operator
      elif(curr_quad[0] == '&&'):
        left_value = self.get_val(curr_quad[1])
        right_value = self.get_val(curr_quad[2])
        temp_address = curr_quad[3]
        res_bool = None
        if(left_value == True and right_value == True):
          res_bool = True
        else:
          res_bool = False
        self.insert_to_memory(temp_address, res_bool)
        ip += 1

      elif(curr_quad[0] == '||'):
        left_value = self.get_val(curr_quad[1])
        right_value = self.get_val(curr_quad[2])
        temp_address = curr_quad[3]
        res_bool = None
        if(left_value == True or right_value == True):
          res_bool = True
        else:
          res_bool = False
        self.insert_to_memory(temp_address, res_bool)
        ip += 1

      # Console operations
      elif(curr_quad[0] == 'WRITE'):
        if(curr_quad[3] >= 70000):
          real_address = self.get_val_from_memory(curr_quad[3])
          val = self.get_val_from_memory(real_address)
        else:
          val = self.get_val_from_memory(curr_quad[3])
        new_string=str(val).replace('"','')

        if(new_string == '\\n'):
          print('\n',end='')
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
        self.insert_to_memory(self.get_val(address, True), res)
        ip += 1

      # Goto's
      elif(curr_quad[0] == 'GOTO'):
        ip = curr_quad[3]
        
      elif(curr_quad[0] == 'GOTOF'):
        cond = self.get_val_from_memory(curr_quad[1])

        if cond == False:
          ip = curr_quad[3]
        elif cond == True:
          ip += 1
        
      elif(curr_quad[0] == 'ERA'):
        # StackOverflow error
        if(len(self.local_memory) > 500):
          raise RuntimeError("StackOverflow")
        self.curr_local_memory = []
          
        # Obtain name of function
        function_name = curr_quad[1]

        # Look if function is global or inside a class
        if(curr_quad[3] != None):
          class_name = curr_quad[3]
          curr_func = dirFunc[class_name]['functions'][function_name]
        else:
          curr_func = dirFunc[function_name]
        # Obtain required locals
        locals = curr_func['localsUsed']
        ints = locals['int']
        floats = locals['float']
        strings = locals['string']
        bools = locals['bool']

        # Obtain required temp locals
        temp_locals = curr_func['usedTemp']
        ints_temp = temp_locals['int']
        floats_temp = temp_locals['float']
        strings_temp = temp_locals['string']
        bools_temp = temp_locals['bool']
        pointer_temp = temp_locals['pointer']

        # Create space memory
        new_local_memory = Memory(ints, floats, strings, bools)
        new_local_temp_memory = Memory(ints_temp, floats_temp, strings_temp, bools_temp, pointer_temp)

        # Points to new space of memory
        self.curr_local_memory.append(new_local_memory)
        self.curr_local_memory.append(new_local_temp_memory)

        # Add new space to stack
        self.local_memory.append(self.curr_local_memory)

        # Create counters useful for managing parameters
        int_count = 0
        float_count = 0
        string_count = 0
        bool_count = 0
        ip += 1
        
      elif(curr_quad[0] == 'PARAMETER'):
        # Check if it is an object
        if(curr_quad[2] != None):
          class_name = curr_quad[2]
          # Signature
          params_table = dirFunc[class_name]['functions'][function_name]['paramsTable']
        else:
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

        elif(argument_type == 'string'):
          address = 7000 + string_count
          string_count += 1

        elif(argument_type == 'bool'):
          address = 8000 + bool_count
          bool_count += 1

        # Obtain value from memory
        argument_value = self.get_val_from_memory(curr_quad[1])
        # Insert argument to formal param
        self.insert_to_memory(address, argument_value)
        ip += 1
        
      elif(curr_quad[0] == 'GOSUB'):
        # Reset counter of params
        int_count   = 0
        float_count = 0
        string_count  = 0
        bool_count  = 0
        # Save the current IP
        checkpoint.append(ip)
        ip = curr_quad[3]

      elif(curr_quad[0] == 'ENDFUNC'):   
        # Erase local memory
        self.local_memory.pop()
        # Update current memory
        if(len(self.local_memory) > 0):
          self.curr_local_memory = self.local_memory[-1]
        else:
          self.curr_local_memory = None

        ip =  checkpoint.pop() + 1
        
      elif(curr_quad[0] == 'RETURN'):
        ip += 1
        
      elif(curr_quad[0] == 'VERIFY'):
        check_value = self.get_val(curr_quad[1])
        upper_limit = self.get_val(curr_quad[3])

        if (check_value >= 0 and check_value < upper_limit):
          ip += 1
        else:
          raise RuntimeError("Out of bounds")

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
string_global_size = dirFunc['globalsUsed']['string']
bool_global_size = dirFunc['globalsUsed']['bool']


# Count temp globals
int_global_temp_size = dirFunc['globalsTempUsed']['int']
float_global_temp_size = dirFunc['globalsTempUsed']['float']
string_global_temp_size = dirFunc['globalsTempUsed']['string']
bool_global_temp_size = dirFunc['globalsTempUsed']['bool']
pointer_global_temp_size = dirFunc['globalsTempUsed']['pointer']

virtual_machine = VirtualMachine()

# Create global memory
virtual_machine.create_global_memory(int_global_size, float_global_size, string_global_size, bool_global_size)

# Create extra segment memory
virtual_machine.create_extra_segment_memory(constantsTable,int_global_temp_size, float_global_temp_size, string_global_temp_size, bool_global_temp_size, pointer_global_temp_size)

# Start the virtual machine
virtual_machine.start_machine(quads)
