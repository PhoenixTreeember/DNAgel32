import random
import re, string
pattern = re.compile('[\W_]+')

random.seed(7)
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
	ret, ret_inv_pol = build_random_expression_worker(list_operators=list_operators, depth=0, max_depth=max_depth)
	if not isinstance(ret, list):
		ret = [ret]
		ret_inv_pol = [ret_inv_pol]
	# print "Produced:", ret
	global IDS; IDS = 0
	return ret, "Exp"+str(IDE),  convert_to_expression(ret), ret_inv_pol

def build_random_expression_worker(list_operators=[('and',2), ('or',2), ('not',1)], depth=0, max_depth=2):

	solution = []
	sol_inv_pol = []
	nodes = 0

	if random.random()>.5 or depth>=max_depth:
		node = get_new_node(nodes)
		return node, node
	else:
		operator, arity = random.sample(list_operators,1)[0]	
		if arity == 2:	
			left, left_inv_pol   = build_random_expression_worker(list_operators=list_operators, depth=depth+1, max_depth=max_depth)
			right, right_inv_pol = build_random_expression_worker(list_operators=list_operators, depth=depth+1, max_depth=max_depth)
			solution.append( [left, operator, right] )
			sol_inv_pol.append( [operator, left_inv_pol, right_inv_pol] )
			# solution.append( [build_random_expression_worker(list_operators=list_operators, depth=depth+1, max_depth=max_depth), operator, build_random_expression_worker(list_operators=list_operators, depth=depth+1, max_depth=max_depth)] )
		else:
			left, left_inv_pol   = build_random_expression_worker( list_operators=list_operators, depth=depth+1, max_depth=max_depth)
			solution.append( [operator, left] )
			sol_inv_pol.append( [operator, left_inv_pol] )
			# solution.append( [operator, ] )
		return solution[0], sol_inv_pol[0]

def convert_to_expression(tree):
	ret_str = ""	
	for st in tree:
		if not isinstance(st, list):
			ret_str += " "+st+" "
		else:
			ret_str += "(" + convert_to_expression(st) + ")"
	return ret_str

"""
def convert_to_expression_inv(tree):
	if len(tree)==1:
		return tree[0]
	if not isinstance(tree, list):
		return str(tree)
	if tree==[]: return ""
	op = tree[0]
	rest = tree[1:]		
	left  = convert_to_expression_inv(rest[0])
	if len(rest)==2:		
		right = convert_to_expression_inv(rest[1])
	if len(rest)==2:
		return "( " + left + " " + op + " " + right + ")"
	else:
		return "( " + op + " " + left + " )"

class Rebuilder(object): 

	def __init__(self):
		self.answer = None		
		# self.rebuilt_expression = []

	def rebuild(self, tree, newtree, pos=0, seek=0):
		print tree, pos
		if tree==[]: return pos, []
		if isinstance(tree, list):
			car = tree[0]
			cons = tree[1:]
			pos, left  = self.rebuild(car,newtree,pos,seek)
			pos, right = self.rebuild(cons,newtree,pos,seek)
			if right == []:
				return pos, left
			else:				
				if right == None: return pos, [left]
				return pos, [left].extend(right)
		else:
			if pos==seek: 
				self.answer = tree
				return pos + 1, newtree				
			else:
				return pos + 1, tree
				
def derivation_tree_length(tree):
	if tree ==[]: return 0
	if not isinstance(tree, list):	return 1
	car = tree[0]
	cons = tree[1:]
	return derivation_tree_length(car) + derivation_tree_length(cons)


def derivation_tree_height(tree):
	if tree ==[]: return 0
	if not isinstance(tree, list):	return 0
	car = tree[0]
	cons = tree[1:]
	val = max(derivation_tree_height(car), derivation_tree_height(cons))+1
	return val

from collections import Sequence
from itertools import chain, count

def depth(seq):
    d  = lambda L: isinstance(L, list) and max(map(depth, L))+1
    return d(seq)
"""


class CustomFunction(object):

	def __init__(self, name, implementation, inv_pol = None):
		self.function_name = name
		self.implementation = implementation
		self.arity = len(identify_variables(implementation))
		self.sol_inv_pol = inv_pol


	def __repr__(self):
		return self.function_name

	def apply(self,attr_list):
		symbols = identify_variables(self.implementation)		
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

"""	
	def convert_from_inv(self):
		self.implementation = convert_to_expression_inv(self.sol_inv_pol)	
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
	
		"""
		for i in xrange(dtl):
			print "scanning", i
			rebuild(self.sol_inv_pol, "[Z]", pos=0, seek=i)
		"""
		r = Rebuilder()
		print r.rebuild(self.sol_inv_pol, x_inv, pos=pos, seek=pos)[1]
		print "Elemento:", r.answer
			
			
		exit()
	


			
		




if __name__ == '__main__':
	
	
	x, expr_name, x_str, x_inv =  build_random_expression(max_depth=3)
	# cf = CustomFunction("AND", convert_to_expression_inv(x_inv) )
	cf.sol_inv_pol = x_inv
	print "Expression:", x_inv
	cf.mutate()

	#cf.mutate()
	