# Global address range
intGlobalAddress = 1000
floatGlobalAddress = 2000
charGlobalAddress = 3000
boolGlobalAddress = 4000

# Local address range
intLocalAddress = 5000
floatLocalAddress = 6000
charLocalAddress = 7000
boolLocalAddress = 8000

# Global temporal address range
intTempGlobalAddress = 9000
floatTempGlobalAddress = 10000
charTempGlobalAddress = 11000
boolTempGlobalAddress = 12000

# Local temporal address range
intTempLocalAddress = 13000
floatTempLocalAddress = 14000
charTempLocalAddress = 15000
boolTempLocalAddress = 16000

# Constant address range
intConstAddress = 17000
floatConstAddress = 18000
charConstAddress = 19000
boolConstAddress = 20000

# RESET TEMPORALS FOR RE-USE
def resetLocalTemporals():
  global intGlobalAddress, floatGlobalAddress, charGlobalAddress, intLocalAddress, floatLocalAddress, charLocalAddress, intTempGlobalAddress, floatTempGlobalAddress, charTempGlobalAddress, intTempLocalAddress, floatTempLocalAddress, charTempLocalAddress, intConstAddress, floatConstAddress, charConstAddress
  global boolGlobalAddress, boolLocalAddress, boolTempGlobalAddress, boolTempLocalAddress, boolConstAddress
  intLocalAddress = 5000
  floatLocalAddress = 6000
  charLocalAddress = 7000
  boolLocalAddress = 8000
  intTempLocalAddress = 13000
  floatTempLocalAddress = 14000
  charTempLocalAddress = 15000
  boolTempLocalAddress = 16000

def getLocalTempUsed():
  ints = intTempLocalAddress - 13000
  floats = floatTempLocalAddress - 14000
  chars  = charTempLocalAddress - 15000
  bools = boolTempLocalAddress - 16000

  return (ints, floats, chars, bools)

def getLocalUsed():
  ints = intLocalAddress - 5000
  floats = floatLocalAddress - 6000
  chars  = charLocalAddress - 7000
  bools = boolLocalAddress - 8000
  
  return (ints, floats, chars, bools)

def getGlobalUsed():
  ints = intGlobalAddress - 1000
  floats = floatGlobalAddress - 2000
  chars  = charGlobalAddress - 3000
  bools = boolGlobalAddress - 4000
    
  return (ints, floats, chars, bools)

def getGlobalTempUsed():
  ints = intTempGlobalAddress - 9000
  floats = floatTempGlobalAddress - 10000
  chars  = charTempGlobalAddress - 11000
  bools = boolTempGlobalAddress - 12000
    
  return (ints, floats, chars, bools)

def setAddress(type, scope):
  global intGlobalAddress, floatGlobalAddress, charGlobalAddress, intLocalAddress, floatLocalAddress, charLocalAddress, intTempGlobalAddress, floatTempGlobalAddress, charTempGlobalAddress, intTempLocalAddress, floatTempLocalAddress, charTempLocalAddress, intConstAddress, floatConstAddress, charConstAddress
  global boolGlobalAddress, boolLocalAddress, boolTempGlobalAddress, boolTempLocalAddress, boolConstAddress
  if(type == "int" and scope == "global"):
    if(intGlobalAddress >= 1000 and intGlobalAddress <= 1999):
      aux = intGlobalAddress
      intGlobalAddress += 1
      return aux
    else:
      print("Addresing Overflow")
      exit()

  if(type == "float" and scope == "global"):
    if(floatGlobalAddress >= 2000 and floatGlobalAddress <= 2999):
      aux = floatGlobalAddress
      floatGlobalAddress += 1
      return aux
    else:
      print("Addresing Overflow")
      exit()

  if(type == "char" and scope == "global"):
    if(charGlobalAddress >= 3000 and charGlobalAddress <= 3999):
      aux = charGlobalAddress
      charGlobalAddress += 1
      return aux
    else:
      print("Addresing Overflow")
      exit()
  
  if(type == "bool" and scope == "global"):
    if(boolGlobalAddress >= 4000 and boolGlobalAddress <= 4999):
      aux = boolGlobalAddress
      boolGlobalAddress += 1
      return aux
    else:
      print("Addresing Overflow")
      exit()

  if(type == "int" and scope == "local"):
    if(intLocalAddress >= 5000 and intLocalAddress <= 5999):
      aux = intLocalAddress
      intLocalAddress += 1
      return aux
    else:
      print("Addresing Overflow")
      exit()

  if(type == "float" and scope == "local"):
    if(floatLocalAddress >= 6000 and floatLocalAddress <= 6999):
      aux = floatLocalAddress
      floatLocalAddress += 1
      return aux
    else:
      print("Addresing Overflow")
      exit()

  if(type == "char" and scope == "local"):
    if(charLocalAddress >= 7000 and charLocalAddress <= 7999):
      aux = charLocalAddress
      charLocalAddress += 1
      return aux
    else:
      print("Addresing Overflow")
      exit()

  if(type == "bool" and scope == "local"):
    if(boolLocalAddress >= 8000 and boolLocalAddress <= 8999):
      aux = boolLocalAddress
      boolLocalAddress += 1
      return aux
    else:
      print("Addresing Overflow")
      exit()
  
  if(type == "int" and scope == "tempGlobal"):
    if(intTempGlobalAddress >= 9000 and intTempGlobalAddress <= 9999):
      aux = intTempGlobalAddress
      intTempGlobalAddress += 1
      return aux
    else:
      print("Addresing Overflow")
      exit()

  if(type == "float" and scope == "tempGlobal"):
    if(floatTempGlobalAddress >= 10000 and floatTempGlobalAddress <= 10999):
      aux = floatTempGlobalAddress
      floatTempGlobalAddress += 1
      return aux
    else:
      print("Addresing Overflow")
      exit()

  if(type == "char" and scope == "tempGlobal"):
    if(charTempGlobalAddress >= 11000 and charTempGlobalAddress <= 11999):
      aux = charTempGlobalAddress
      charTempGlobalAddress += 1
      return aux
    else:
      print("Addresing Overflow")
      exit()

  if(type == "bool" and scope == "tempGlobal"):
    if(boolTempGlobalAddress >= 12000 and boolTempGlobalAddress <= 12999):
      aux = boolTempGlobalAddress
      boolTempGlobalAddress += 1
      return aux
    else:
      print("Addresing Overflow")
      exit()

  if(type == "int" and scope == "tempLocal"):
    if(intTempLocalAddress >= 13000 and intTempLocalAddress <= 13999):
      aux = intTempLocalAddress
      intTempLocalAddress += 1
      return aux
    else:
      print("Addresing Overflow")
      exit()

  if(type == "float" and scope == "tempLocal"):
    if(floatTempLocalAddress >= 14000 and floatTempLocalAddress <= 14999):
      aux = floatTempLocalAddress
      floatTempLocalAddress += 1
      return aux
    else:
      print("Addresing Overflow")
      exit()

  if(type == "char" and scope == "tempLocal"):
    if(charTempLocalAddress >= 15000 and charTempLocalAddress <= 15999):
      aux = charTempLocalAddress
      charTempLocalAddress += 1
      return aux
    else:
      print("Addresing Overflow")
      exit()

  if(type == "bool" and scope == "tempLocal"):
    if(boolTempLocalAddress >= 16000 and boolTempLocalAddress <= 16999):
      aux = boolTempLocalAddress
      boolTempLocalAddress += 1
      return aux
    else:
      print("Addresing Overflow")
      exit()

  if(type == "int" and scope == "constant"):
    if(intConstAddress >= 17000 and intConstAddress <= 17999):
      aux = intConstAddress
      intConstAddress += 1
      return aux
    else:
      print("Addresing Overflow")
      exit()

  if(type == "float" and scope == "constant"):
    if(floatConstAddress >= 18000 and floatConstAddress <= 18999):
      aux = floatConstAddress
      floatConstAddress += 1
      return aux
    else:
      print("Addresing Overflow")
      exit()

  if(type == "char" and scope == "constant"):
    if(charConstAddress >= 19000 and charConstAddress <= 19999):
      aux = charConstAddress
      charConstAddress += 1
      return aux
    else:
      print("Addresing Overflow")
      exit()

  if(type == "bool" and scope == "constant"):
    if(boolConstAddress >= 20000 and boolConstAddress <= 20999):
      aux = boolConstAddress
      boolConstAddress += 1
      return aux
    else:
      print("Addresing Overflow")
      exit()