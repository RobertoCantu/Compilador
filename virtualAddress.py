# Global address range
intGlobalAddress = 1000
floatGlobalAddress = 2000
charGlobalAddress = 3000

# Local address range
intLocalAddress = 4000
floatLocalAddress = 5000
charLocalAddress = 6000

# Global temporal address range
intTempGlobalAdress = 7000
floatTempGlobalAdress = 8000
charTempGlobalAdress = 9000
intTempLocalAdress = 10000
floatTempLocalAdress = 11000
charTempLocalAdress = 12000

# Constant address range
intConstAddress = 13000
floatConstAddress = 14000
charConstAddress = 15000

def setAdress(type, scope):
  global intGlobalAddress, floatGlobalAddress, charGlobalAddress, intLocalAddress, floatLocalAddress, charLocalAddress, intTempGlobalAdress, floatTempGlobalAdress, charTempGlobalAdress, intTempLocalAdress, floatTempLocalAdress, charTempLocalAdress, intConstAddress, floatConstAddress, charConstAddress
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

  if(type == "int" and scope == "local"):
    if(intLocalAddress >= 4000 and intLocalAddress <= 4999):
      aux = intLocalAddress
      intLocalAddress += 1
      return aux
    else:
      print("Addresing Overflow")
      exit()

  if(type == "float" and scope == "local"):
    if(floatLocalAddress >= 5000 and floatLocalAddress <= 5999):
      aux = floatLocalAddress
      floatLocalAddress += 1
      return aux
    else:
      print("Addresing Overflow")
      exit()

  if(type == "char" and scope == "local"):
    if(charLocalAddress >= 6000 and charLocalAddress <= 6999):
      aux = charLocalAddress
      charLocalAddress += 1
      return aux
    else:
      print("Addresing Overflow")
      exit()

  if(type == "int" and scope == "tempGlobal"):
    if(intTempGlobalAdress >= 7000 and intTempGlobalAdress <= 7999):
      aux = intTempGlobalAdress
      intTempGlobalAdress += 1
      return aux
    else:
      print("Addresing Overflow")
      exit()

  if(type == "float" and scope == "tempGlobal"):
    if(floatTempGlobalAdress >= 8000 and floatTempGlobalAdress <= 8999):
      aux = floatTempGlobalAdress
      floatTempGlobalAdress += 1
      return aux
    else:
      print("Addresing Overflow")
      exit()

  if(type == "char" and scope == "tempGlobal"):
    if(charTempGlobalAdress >= 9000 and charTempGlobalAdress <= 9999):
      aux = charTempGlobalAdress
      charTempGlobalAdress += 1
      return aux
    else:
      print("Addresing Overflow")
      exit()

  if(type == "int" and scope == "tempLocal"):
    if(intTempLocalAdress >= 10000 and intTempLocalAdress <= 10999):
      aux = intTempLocalAdress
      intTempLocalAdress += 1
      return aux
    else:
      print("Addresing Overflow")
      exit()

  if(type == "float" and scope == "tempLocal"):
    if(floatTempLocalAdress >= 11000 and floatTempLocalAdress <= 11999):
      aux = floatTempLocalAdress
      floatTempLocalAdress += 1
      return aux
    else:
      print("Addresing Overflow")
      exit()

  if(type == "char" and scope == "tempLocal"):
    if(charTempLocalAdress >= 12000 and charTempLocalAdress <= 12999):
      aux = charTempLocalAdress
      charTempLocalAdress += 1
      return aux
    else:
      print("Addresing Overflow")
      exit()

  if(type == "int" and scope == "constant"):
    if(intConstAddress >= 13000 and intConstAddress <= 13999):
      aux = intConstAddress
      intConstAddress += 1
      return aux
    else:
      print("Addresing Overflow")
      exit()

  if(type == "float" and scope == "constant"):
    if(floatConstAddress >= 14000 and floatConstAddress <= 14999):
      aux = floatConstAddress
      floatConstAddress += 1
      return aux
    else:
      print("Addresing Overflow")
      exit()

  if(type == "char" and scope == "constant"):
    if(charConstAddress >= 15000 and charConstAddress <= 15999):
      aux = charConstAddress
      charConstAddress += 1
      return aux
    else:
      print("Addresing Overflow")
      exit()