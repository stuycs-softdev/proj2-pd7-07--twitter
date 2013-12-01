#this will be the python code that will manage the tree datastructure
#Shaan Sheikh

class node(object):

	def __init__(self, value, numchildren, level):
		self.value = value
		self.level = level
		self.numchildren = numchildren
		self.children = [0] * numchildren

	def setvalue(self, val):
		self.value = val

	def getvalue(self):
		return self.value

	def setchild(self, pos,insert):
		if isinstance(insert,node) and pos > 0 and pos < numchildren:
			self.children[pos] = insert

	def createchild(self, pos, value):
		self.children[pos] = node(value, self.numchildren, self.level + 1)

	def getchild(self, pos):
		return self.children[pos]

	def __str__(self):
		return self.value
	
class  tree(object):



	def __init__(self, rootvalue, branchespernode):
		self.numberofnodes = 1
		self.root = node(rootvalue, branchespernode, 0)
		self.childnodelist = []
		self.branchespernode = branchespernode

	def getroot(self):
		return self.root

	#pos has range [0,(branchespernode^level)-1]
	def addnode(self,level, pos, value):
		self.numberofnodes += 1
		path = [0] * level
		for x in xrange(level,0,-1):
			path[x-1] = pos/self.branchespernode
			pos /= self.branchespernode

		parent = self.root

		print path[1:]


		for x in path[1:]:
			otherparent = parent.getchild(x)
			parent = otherparent

		print parent
		parent.createchild(pos,value)

	def getnode(pos):
		pass

	def getnumnodes():
		return numberofnodes

cat = tree('#start',3)

#cat.addnode(1,0,'#asdf')
cat.addnode(1,1,'#b')
#cat.addnode(1,2,'#c')


#cat.addnode(2,0,'#d')
#cat.addnode(2,1,'#e')
#cat.addnode(2,2,'#f')
cat.addnode(2,3,'#g')
#cat.addnode(2,4,'#h')
#cat.addnode(2,5,'#i')
#cat.addnode(2,6,'#j')
#cat.addnode(2,7,'#k')
#cat.addnode(2,8,'#l')
