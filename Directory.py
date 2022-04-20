# dirFun = {
# 	{
# 		'name': '',
# 		'type': '',
# 		'vars': {}
# 	},
# 	{
# 		'name': '',
# 		'type': '',
# 		'vars': {}
# 	}
# }

dirFun = {'correr': {'type': 'void', 'vars': {}}}
# devBio = {
# 	"name": "Ihechikara",
# 	"age": 120,
# 	"language": "JavaScript"
# }

# devBio["age"] = 1

# print(devBio)


def createDic():
	dirFun = {}
	return dirFun


def addFunc(dir, name, type):
	dir[f"{name}"] = {
			'type': type
			#Mas campos en el futuro
	}
	return dir


def createVarTable(dir, funcName):
	dir[f"{funcName}"]['vars'] = {}
	#Mas campos en el futuro
	return dir


def addVar(dir, funcName, varName, varType):
	dir[f"{funcName}"]['vars'][f"{varName}"] = {
		'type': varType
	}
	return dir


# test = createDic()
# test = addFunc(test, "pato", "void")

# test = createVarTable(test, "pato")
# test = addVar(test, "pato", "var1", "int")

# print(test)