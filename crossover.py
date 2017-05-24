from distributions import *
from nodes import *
import random

random.seed(3)


def crossover_distributions(d1, d2, n1, n2, e1, e2):

	d1.tokens = n1
	d1.resize(e1)	
	d1.filter_bins(e1)
	d2.tokens = n2
	d2.resize(e2)	
	d2.filter_bins(e2)
	
	return d1, d2

if __name__ == '__main__':

	net1 = Network()
	net2 = Network()
	net1.generate_random_functions(10, max_depth=3)
	net2.generate_random_functions(10, max_depth=3)
	print net1.nodes_arities
	print net2.nodes_arities
	
	d1 = Distribution(tokens=100, bins=5)
	d1.initialize_uniform()
	d2 = Distribution(tokens=10, bins=6)
	d2.initialize_uniform()

	n1 = 13
	n2 = 100

	d1, d2 = crossover_distributions(d1, d2, n1, n2, net1.nodes_arities, net2.nodes_arities)