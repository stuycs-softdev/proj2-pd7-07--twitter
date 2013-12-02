#Shaan Sheikh

#read the comments for the ranges carfully. I didn't code in error correction (yet)
#misusing something will lead to an error
#addnode() in tree is buggy

#Node Class
class node(object):

	#python's equivalent of the main class. Initialize by node(value,numchildren,level)
	#where:
	#value is the contents of the node
	#numchildren is the number of childred the node will have. This will be 10 in our case
	#level is which level of the tree the node is on, with the root being 0
	def __init__(self, value, numchildren, level):
		self.value = value
		self.level = level
		self.numchildren = numchildren
		self.children = [0] * numchildren

	#changes the value of the node
	def setvalue(self, val):
		self.value = val

	#returns the value of the node
	def getvalue(self):
		return self.value

	#if you have 2 node and want to set one as a child of the other, use this function
	#node1.setchild(pos,node2)
	#where pos is which of the children you want node2 to be
	#pos has a range of [0,numchildren-1]
	def setchild(self, pos,insert):
		if isinstance(insert,node) and pos > 0 and pos < numchildren:
			self.children[pos] = insert

	#Node spawns a new child node with a value of 'value'
	#pos has range [0,numchildren-1]
	def createchild(self, pos, value):
		self.children[pos] = node(value, self.numchildren, self.level + 1)

	#returns a node that's in 'pos' position
	#returns 0 if there is none
	#pos has range [0,numchildren-1]
	def getchild(self, pos):
		return self.children[pos]

	#overrides print functionality
	#returns the value of the node
	def __str__(self):
		return self.value
	


class  tree(object):


	#main class
	#arguements should be self explanitory
	def __init__(self, rootvalue, branchespernode):
		self.numberofnodes = 1
		self.root = node(rootvalue, branchespernode, 0)
		self.childnodelist = []
		self.branchespernode = branchespernode

	#The tree object returns the node at it's root
	def getroot(self):
		return self.root

	#adds a new node into the tree
	#this is kinda buggy
	#When it's done, the only prerequisite to run is that the node above it is set
	#usage: treeobject.addnode(level, position, value)
	#for level, 0 is thre root, with each subsequent level below it is one higher
	#pos has range [0,(branchespernode^level)-1] - be careful with this, an out of range value will crash the program
	#the left-most node has a pos of 0 in each level
	#so a tree with the pos values of each node looks like:
	#			0
	#		   / \
	#		  0   1
	#        / \ / \
	#       0  1 2  3
	#value is the contents of the new node
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

	#return the total number of nodes in the tree
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
