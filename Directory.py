
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

dic = DirFunc()

dic.addFunc({"name": "hola", "type": "void", "table": None})
dic.addVarsTable('hola', {"name": "perro", "type": "int"} )
dic.addVarsTable('hola', {"name": "gato", "type": "float"} )

print(dic.dirFunc)