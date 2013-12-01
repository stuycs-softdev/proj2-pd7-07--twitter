#this will be the python code that will manage the tree datastructure
#Shaan Sheikh

class node(object):

	def __init__(self, value, level):
		self.value = value
		self.level = level
		children = [0] * maxvalue

	def setvalue(self, val):
		self.value = val

	def getvalue(self):
		return self.value

	def setchild(self, pos,insert):
		if isinstance(insert,node) and pos > 0 and pos < maxvalue:
			children[pos] = insert

	def createchild(self, pos, value):
		children[pos] = node(value, self.level + 1)

	def getchild(self, pos):
		return children[pos]
	
class  tree(object):

	def __init__(self, rootvalue, branchespernode):
		self.numberofnodes = 1
		self.root = node(rootvalue, branchespernode, 0)
		self.childnodelist = []
		self.branchespernode = branchespernode


	#pos has range [0,(branchespernode^level)-1]
	def addnode(self,level, pos):
		self.numberofnodes += 1
		path = [0] * level
		for x in xrange(level,0,-1):
			print pos/self.branchespernode
			path[x-1] = pos/self.branchespernode
			pos /= self.branchespernode

		
		



	def getnode(pos):
		pass

	def getnumnodes():
		return numberofnodes

cat = tree(0,3)
cat.addnode(4,28)