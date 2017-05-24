class Tree(object):

	def __init__(self, operator):
		self.children = []
		self.operator = operator
		self.temp_depth = 0

	def __repr__(self):
		return "Function "+self.operator

	def add(self, child):
		self.children.append(child)

	def remove(self, n):
		self.chilren.remove(self.children[n])


	def print_tree(self):
		print self.operator, "(", 
		for c in self.children:
			if isinstance(c, TreeNode):
				print c.value, 
			else:
				c.print_tree(), 
		print ")", 


	def count_nodes(self, n=0):
		n += 1
		for c in self.children:
			if isinstance(c, TreeNode):
				n += 1
			else:
				n = c.count_nodes(n=n)				
		return n 

	def depth_subtree(self, seek=0):
		return self.depth_subtree_worker(seek=seek, root=self) + 1

	def depth_subtree_worker(self, pos=0, seek=0, depth=0, root=None):
		if seek==0:
			self.temp_depth = 0
			return pos
		pos += 1
		for n, c in enumerate(self.children):
			if isinstance(c, TreeNode):				
				# identified leaf
				if pos==seek: 				
					root.temp_depth = depth+1
				pos += 1
			else:
				# identified subtree
				if pos == seek:
					root.temp_depth = depth+1
				pos = c.depth_subtree_worker(pos=pos, seek=seek, depth=depth+1, root=root) 
		return pos


	def depth(self, d=0):
		ret = [0]
		for c in self.children:
			if isinstance(c, TreeNode):
				ret.append(d+1)
			else:
				ret.append(c.depth(d+1))
		return max(ret)


	def mutate_subtree(self, subtree, pos=0, seek=0):

		"""
		if (seek==0):
			print "Tutto l'albero"
			self = subtree
			return 0
		"""

		# print "pos=",pos, self.operator
		pos += 1
		for n, c in enumerate(self.children):
			if isinstance(c, TreeNode):				
				# identified leaf
				if pos==seek: 
					self.children[n] = subtree				
					# c.value = 1000
				pos += 1
			else:
				# identified subtree
				if pos == seek:
					self.children[n] = subtree
				pos = c.mutate_subtree(subtree, pos=pos, seek=seek) 
		return pos


	def convert_to_string(self):

		arity = len(self.children)
		if arity==1:
			if isinstance(self.children[0], TreeNode):
				sub = self.children[0].value
			else:
				sub = self.children[0].convert_to_string()
			return "("+self.operator+" "+str(sub)+")"
		if arity==2:
			if isinstance(self.children[0], TreeNode):
				subleft = self.children[0].value
			else:
				subleft = self.children[0].convert_to_string()
			if isinstance(self.children[1], TreeNode):
				subright = self.children[1].value
			else:
				subright = self.children[1].convert_to_string()
			return "( "+str(subleft)+" "+self.operator+" "+str(subright) +" )"


class TreeNode(object):
	def __init__(self, value):
		self.value = value
		self.precalculated_depth = 0
		self.temp_depth = 0

	def __repr__(self):
		return "Node "+str(self.value)

	
	def count_nodes(self):
		return 1

	def depth_subtree(self, seek=0):
		return 0

	def mutate_subtree(self, subtree, pos=0, seek=0):
		self = subtree

	def convert_to_string(self):
		return str(self.value)


if __name__ == '__main__':
	
	tree = Tree("+")
	subtree = Tree("-")
	tree.add(subtree)

	subsubtree = Tree("*")
	subtree.add(subsubtree)
	node1 = TreeNode(1)
	node2 = TreeNode(2)
	node3 = TreeNode(3)
	node4 = TreeNode(4)
	subsubtree.add(node1)
	subsubtree.add(node2)	
	subtree.add(node3)
	tree.add(node4)
	
	mutsub=Tree("sqrt")
	mutsubleaf=TreeNode("9")
	mutsub.add(mutsubleaf)

	tree.print_tree()
	print
	print tree.convert_to_string()

	tree.mutate_subtree(mutsub, seek=6)

	tree.print_tree()
	print
	print tree.convert_to_string()

	"""
	tree.print_tree()
	print 
	st = 3
	print "Looking for subtree", st
	tree.depth_subtree(seek=st)
	print "Depth:", tree.temp_depth
	"""