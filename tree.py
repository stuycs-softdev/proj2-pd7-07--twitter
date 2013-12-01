#this will be the python code that will manage the tree datastructure
#Shaan Sheikh

class node(object):

	def __init__(self, value, maxvalue):
		self.value = value
		self.maxvalue = maxvalue
		children = [0] * maxvalue

	def setvalue(val):
		self.value = val

	def getvalue():
		return self.value

	def setchild(pos):
		




class  tree(object):
	numberofnodes = 0

	def __init__(self, value, branchespernode, level):
		numberofnodes = numberofnodes + 1
		self.value = value
		self.childnodelist = []
		self.branchespernode = branchespernode


	#pos represents the branch number and has a range of [0, branchespernode - 1]
	def addnode(pos):
		pass

	def setvalue(value):
		pass

	def getvalue():
		pass

	def getnode(pos):
		pass