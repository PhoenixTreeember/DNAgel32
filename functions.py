import random
import re, string
pattern = re.compile('[\W_]+')

import derivation_tree

random.seed(3)
global IDS; IDS = 0		# singleton
global IDE; IDE = 0		# singleton


class SafeFloat(float):
	def __div__(self, other):
		if other==0:
			return self
		else:
			return SafeFloat(float(self)/float(other))


def basic_func(p):
	return p.upper() not in ["OR", "AND", "NOT", "^", "+", "*", "-"]
def identify_variables(string):
	string = pattern.sub(' ', string)
	return filter(basic_func, string.split())

def get_new_node(nodes):
	global IDS; IDS += 1
	return "A"+str(IDS)

def build_random_expression(list_operators=[('and',2), ('or',2), ('not',1), ('^',2)], max_depth=2):
	global IDE; IDE += 1
	ret, ret_dt = build_random_expression_worker(list_operators=list_operators, depth=0, max_depth=max_depth)
	if not isinstance(ret, list):
		ret = [ret]
	# 	ret_inv_pol = [ret_inv_pol]
	# print "Produced:", ret
	global IDS; IDS = 0
	return ret, "Exp"+str(IDE),  convert_to_expression(ret), ret_dt

def build_random_expression_worker(list_operators=[('and',2), ('or',2), ('not',1)], depth=0, max_depth=2):

	solution = []
	# sol_inv_pol = []
	nodes = 0

	if random.random()>.5 or depth>=max_depth:
		node = get_new_node(nodes)
		dt_node = derivation_tree.TreeNode(node)
		return node, dt_node
	else:
		operator, arity = random.sample(list_operators,1)[0]	
		if arity == 2:	
			left, left_dt   = build_random_expression_worker(list_operators=list_operators, depth=depth+1, max_depth=max_depth)
			right, right_dt = build_random_expression_worker(list_operators=list_operators, depth=depth+1, max_depth=max_depth)
			solution.append( [left, operator, right] )
			dt_tree = derivation_tree.Tree(operator)
			dt_tree.add(left_dt)
			dt_tree.add(right_dt)
		else:
			left, left_dt   = build_random_expression_worker( list_operators=list_operators, depth=depth+1, max_depth=max_depth)
			solution.append( [operator, left] )
			dt_tree = derivation_tree.Tree(operator)
			dt_tree.add(left_dt)
		return solution[0], dt_tree

def convert_to_expression(tree):
	ret_str = ""	
	for st in tree:
		if not isinstance(st, list):
			ret_str += " "+st+" "
		else:
			ret_str += "(" + convert_to_expression(st) + ")"
	return ret_str


class CustomFunction(object):

	def __init__(self, name, implementation):
		self.function_name = name
		self.implementation = implementation
		self.arity = len(identify_variables(implementation))
		self.DT = None


	def __repr__(self):
		return self.function_name

	def apply(self,attr_list):
		
		symbols = identify_variables(self.implementation)		
		"""
		print self.implementation
		print symbols
		print attr_list
		print
		"""

		for n,a in enumerate(attr_list):						
			# exec ( symbols[n] + "=" + str(a) ) in locals(), locals()
			exec ( symbols[n] + "=" + str(a) ) 
		try:	
			return eval(self.implementation)
		except ZeroDivisionError:
			return 0
		except Exception as ex:
			print self.implementation
			print type(ex).__name__, ex.args
			exit()

	def convert_from_dt(self):
		self.implementation = self.DT.convert_to_string()

	def mutate(self, max_depth=3):		
		nodes = self.DT.count_nodes()
		# print "Total nodes:", nodes
		node_mut = random.randint(0, nodes)
		# print "Will mutate node:", node_mut
		self.DT.depth_subtree(node_mut)
		# print "Depth of node:", self.DT.temp_depth
		max_subtree = max_depth-self.DT.temp_depth
		# print "Maximum height of mutated subtree", max_subtree
		x, expr_name, x_str, ret_dt =  build_random_expression(max_depth=max_subtree)
		# print "Inserting", ret_dt.convert_to_string()
		self.DT.mutate_subtree(ret_dt, seek=node_mut)
		

		# self.convert_from_dt()

"""
	def mutate(self, list_operators=[('and',2), ('or',2), ('not',1), ('^',2)], max_depth=3):
		# rand_expr, expr_name, x_str, x_inv =  build_random_expression(list_operators=[("and", 2), ("or", 2), ("not", 1)], max_depth=max_depth-1)		
		# step 1: randomly navigate tree
		dtl = derivation_tree_length(self.sol_inv_pol)
		pos = random.randint(0,dtl-1)
		pos = 1
		x, expr_name, x_str, x_inv = build_random_expression(max_depth=2)
		if len(x_inv)==1:
			x_inv = x_inv[0]
		print "Will substitute node in position", pos, "with", x_inv

		#dep = depth(self.sol_inv_pol)
		#print "Depth of tree:", dep
		#print "Max height of random subtree:", max_depth - dep
	
		for i in xrange(dtl):
			print "scanning", i
			rebuild(self.sol_inv_pol, "[Z]", pos=0, seek=i)
		r = Rebuilder()
		print r.rebuild(self.sol_inv_pol, x_inv, pos=pos, seek=pos)[1]
		print "Elemento:", r.answer	
			
		exit()
"""
	


			
		




if __name__ == '__main__':
	
	
	x, expr_name, x_str, ret_dt =  build_random_expression(max_depth=3)
	cf = CustomFunction("AND", x_str )
	print cf.implementation
	cf.DT = ret_dt
	cf.convert_from_dt()
	print cf.implementation

	#cf.mutate()
	