class DirFunc:
	def __init__(self):
		self.dirFunc = {}

	def addFunc(self,item):
		self.dirFunc[item["name"]] = item

	def getFuncByName(self,name):
		if(name in self.dirFunc):
			return self.dirFunc[name]
		else:
			return None

	def addVarsTable(self,name, item):
		if (name in self.dirFunc):
			self.dirFunc[name]["table"] = item
			return self.dirFunc[name]["table"]
		else:
			return None

	def addParamsTable(self,name, item):
		if (name in self.dirFunc):
			self.dirFunc[name]["paramsTable"] = item
			return self.dirFunc[name]["paramsTable"]
		else:
			return None
	
	def addVar(self, name, type):
		print('Add var')

class Vars:
	def __init__(self):
		self.data = {}

	def addVar(self,item):
		self.data[item["name"]] = item

	def getVarByName(self,name):
		if(name in self.data):
			return self.data[name]
		else:
			return None

class ConstantsTable:
	def __init__(self):
		self.constants = {}

	def addConstant(self, value, address):
		self.constants[value] = {'name': value, 'address': address}

	def getConstants(self):
		return self.constants

	def getConstantByValue(self,value):
		if(value in self.constants):
			return self.constants[value]
		else:
			return None