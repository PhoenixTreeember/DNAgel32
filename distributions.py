from pylab import *
import networkx
from scipy.misc import factorial
from scipy import pi
import random
from numpy.random import choice


class Distribution(object):
    def __init__(self, bins=9, tokens=100):
        # self.base = zeros(bins)
        self.amounts = zeros(bins)
        self.filtered = []
        self.bins = bins
        # self.type =""
        self.tokens = tokens
        print " * New empty distribution generator created with", bins, "bins"

    def resize(self, dictionary, prop=1E6, fix=False):
        self.amounts /= sum(self.amounts)
        self.amounts *= prop
        self.amounts = map(int, self.amounts)

        if fix:
            while (sum(self.amounts) != self.tokens):
                if self.tokens > sum(self.amounts):
                    destination = random.sample(dictionary.keys(), 1)[0]
                    self.amounts[destination - 1] += 1
                if self.tokens < sum(self.amounts):
                    destination = choice(dictionary.keys(), 1)
                    if self.amounts[destination - 1] > 0:
                        self.amounts[destination - 1] -= 1

        print self.amounts, sum(self.amounts)


    def initialize_uniform(self):
        min_amount = self.tokens / self.bins
        print " * Minimum amount for", self.tokens, "tokens in", self.bins, "bins:", min_amount
        for b in xrange(self.bins):
            self.amounts[b] = min_amount
        rem_amount = self.tokens - min_amount * self.bins
        print " * Stochastically assigning", rem_amount, "remaining tokens"
        for b in random.sample(range(self.bins), rem_amount):
            self.amounts[b] += 1
        print " * Uniform distribution initialized"

    def filter_bins(self, dictionary):
        print " * Filtering arities"
        self.filtered = range(1, self.bins + 1)
        self.filtered = filter(lambda x: x not in dictionary.keys(), self.filtered)
        # print "Filtered:", self.filtered
        for b in xrange(1, self.bins + 1):
            if b in self.filtered:
                # print b, "not in keys, removing tokens..."
                destination = choice(dictionary.keys(), self.amounts[b - 1])
                for db in destination:
                    self.amounts[db - 1] += 1
                self.amounts[b - 1] = 0

    def perturb(self, prob_bin=.1, sigma=.1):

        elenco = range(self.bins)
        random.shuffle(elenco)

        for b in elenco:
            if prob_bin > random.random():
                while (True):
                    am = int(random.gauss(self.amounts[b], sigma))
                    if am > 0: break
                diff = am - self.amounts[b]
                if diff > 0:
                    while (diff > 0):
                        rnd_bin = random.randint(0, self.bins - 1)
                        if rnd_bin == b: continue
                        if rnd_bin + 1 in self.filtered: continue
                        if self.amounts[rnd_bin] > 0:
                            self.amounts[rnd_bin] -= 1
                            diff -= 1
                else:
                    while (diff < 0):
                        rnd_bin = random.randint(0, self.bins - 1)
                        if rnd_bin == b: continue
                        if rnd_bin + 1 in self.filtered: continue
                        if self.amounts[rnd_bin] > 0:
                            self.amounts[rnd_bin] += 1
                            diff += 1
                self.amounts[b] = am


class OldDistribution(object):
    def __init__(self, bins=100):
        self.base = zeros(bins)
        self.amounts = zeros(bins)
        self.cumulative = zeros(bins)
        self.bins = bins
        self.type = ""
        print " * New empty distribution generator created with", bins, "bins"

    def normalize(self):
        self.cumulative /= sum(self.cumulative)
        self.amounts /= sum(self.amounts)
        print "Values normalized"

    def resample(self, groups=100):
        print " * Resample from", self.bins, "to", groups
        if groups > self.bins:
            print "ERROR: wrong number of groups specified"
            exit(-1)
        new_dist = zeros(groups)
        total = 0
        for i in xrange(groups):
            for j in xrange(i * self.bins / groups, (i + 1) * self.bins / groups):
                new_dist[i] += self.amounts[j]
        self.amounts = new_dist
        self.bins = groups
        self.cumulative = zeros(groups)
        for i in xrange(1, groups + 1):
            total += self.amounts[i - 1]
            self.cumulative[i - 1] = total


    def generate(self, distrib, mu=10, sigma=5, lam=10, scaletoone=True, sf=100):
        if distrib == "uniform":
            self.generate_uniform()
        elif distrib == "normal":
            self.generate_normal(mu=mu, sigma=sigma)
        elif distrib == "poisson":
            self.generate_poisson(lam=lam)
        elif distrib == "power_law":
            self.generate_power_law(lam=lam, sf=sf)

        if scaletoone: self.normalize()
        self.type = distrib


    """ Returns a list of N random numbers distributed according to the distribution """

    def array_of_samples(self, N):
        a = map(int, list(x for x in self.sample_distribution(N)))
        return a


    """ Generates N random numbers distributed according to the distribution,
		resampled according to #groups subdivisions (#groups must be =< #bins) """

    def sample_distribution(self, N):
        for i in xrange(N):
            x = random.random() * self.cumulative[-1]
            for n, j in enumerate(self.cumulative):
                if x < j:
                    yield n
                    break


    """ Closed-form formula of gaussian distribution """

    def gaussian(self, x, mu, sig):
        fact = 1. / (sig * sqrt(2 * pi))
        fact *= exp(-( (x - mu) * (x - mu) / (2 * sig * sig)))
        return fact

    # return 1./(sig*sqrt(2*pi)) * exp(-power(x-mu, 2.) / (2*power(sig, 2.)) )


    """ Generates a uniform distribution """

    def generate_uniform(self):
        total = 0
        for i in xrange(1, self.bins + 1):
            self.amounts[i - 1] = 1. / self.bins
            total += self.amounts[i - 1]
            self.cumulative[i - 1] = total
        self.base = self.amounts[:]


    """ Generates a normal distribution with specified average and standard deviation """

    def generate_normal(self, mu=10, sigma=5):
        total = 0
        for i in xrange(1, self.bins + 1):
            self.amounts[i - 1] = self.gaussian(i, mu, sigma)
            total += self.amounts[i - 1]
            self.cumulative[i - 1] = total
        self.base = self.amounts[:]


    """ Generates a power-law distribution with specified exponent and scaling coefficient.
		The distribution can be scaled to sum to 1. """

    def generate_power_law(self, lam=2.1, sf=100):
        total = 0
        for i in xrange(1, self.bins + 1):
            self.amounts[i - 1] = sf * pow(i, -lam)
            total += self.amounts[i - 1]
            self.cumulative[i - 1] = total
        # if scaletoone: self.amounts /= sum(self.amounts)
        self.base = self.amounts[:]


    """ Generates a Poisson distribution with specified lambda """

    def generate_poisson(self, lam=10):
        total = 0
        for i in xrange(1, self.bins + 1):
            self.amounts[i - 1] = exp(-lam) * (pow(lam, i) / factorial(i))
            total += self.amounts[i - 1]
            self.cumulative[i - 1] = total
        self.base = self.amounts[:]


def myownhistogram(data, bins=100, Normed=True):
    alloc = zeros(bins)
    for d in data:
        alloc[d] += 1
    if Normed:
        alloc /= sum(alloc)
    return alloc


if __name__ == '__main__':
    D = Distribution(bins=9, tokens=111)
    D.initialize_uniform()
    example = {1: [], 2: [], 4: [], 9: []}
    D.filter_bins(example)

    """
	PRECISION = 100
	NODES = 100
	d = Distribution(bins=PRECISION)
	
	d_pl = Distribution(bins=PRECISION)
	d_pl.generate_power_law()
	# d.generate_uniform()
	# d.generate_poisson()
	# d.generate_normal(mu=10, sigma=1)
	G_pl = networkx.Graph()

	list_of_nodes = d_pl.array_of_samples(NODES)

	for m, n in enumerate(list_of_nodes):
		G.add_node(m)

	for m, n in enumerate(list_of_nodes):
		X = random.sample(range(NODES), n)
		for p in X:
			G.add_edge(m, p)

	print "*"*100
	print " Graph type        | Average degree (N/K) |  "
	print "*"*100
	
	# networkx.draw(G)
	# show()
	f, axarr = subplots(2,2, sharey='row')

	# d.generate_uniform()
	d.generate("uniform", scaletoone=True)
	axarr[0,0].plot(range(d.bins), d.amounts, "-o", color=(0,0,1), label="uniform")
	sampled_uniform = list (x for x in d.sample_distribution(10000))
	hist_uniform = histogram(sampled_uniform, bins=PRECISION, density=True)
	axarr[0,0].plot(range(d.bins), hist_uniform[0], "-o",  color=(0.5,0.5,1), label="sampled uniform")
	axarr[0,0].legend(prop={'size':6})	
	axarr[0,0].set_xlim(0,PRECISION)
	axarr[0,0].set_ylim(0,1)
	axarr[0,0].set_xlabel("Degree of nodes (K)")
	axarr[0,0].set_ylabel("Ratio of degree (K/N)")

	d.generate("normal", mu=PRECISION/2, sigma=1.5, scaletoone=True)
	axarr[0,1].plot(range(d.bins), d.amounts, "-o",  color=(0,1,0), label="normal")
	sampled_normal = list (x for x in d.sample_distribution(100000))
	# hist_normal = histogram(sampled_normal, bins=PRECISION, density=True)
	hist_normal = myownhistogram(sampled_normal, bins=PRECISION, Normed=True)
	# axarr[0,1].plot(range(d.bins), hist_normal[0], "-o",  color=(0.5,1,0.5), label="sampled normal")
	axarr[0,1].plot(range(d.bins), hist_normal, "-o",  color=(0.5,1,0.5), label="sampled normal")
	axarr[0,1].legend(prop={'size':6})
	axarr[0,1].set_xlim(0,PRECISION)
	axarr[0,1].set_ylim(0,1)
	axarr[0,1].set_xlabel("Degree of nodes (K)")
	axarr[0,1].set_ylabel("Ratio of degree (K/N)")
	
	d.generate("power_law", lam=2.1, sf=100, scaletoone=True)
	axarr[1,0].plot(range(d.bins), d.amounts, "-o", color='r', label="power-law")
	sampled_powerlaw = list (x for x in d.sample_distribution(100000))
	hist_powerlaw = histogram(sampled_powerlaw, bins=PRECISION, density=True)
	# hist_powerlaw = myownhistogram(sampled_powerlaw, bins=PRECISION, Normed=True)
	axarr[1,0].plot(range(d.bins), hist_powerlaw[0], "-o",  color=(1.0,0.5,0.5), label="sampled power law")
	# axarr[1,0].plot(range(d.bins), hist_powerlaw, "-o",  color=(1.0,0.5,0.5), label="sampled power law")
	axarr[1,0].legend(prop={'size':6})
	axarr[1,0].set_xlim(0,PRECISION)
	axarr[1,0].set_ylim(0,1)
	axarr[1,0].set_xlabel("Degree of nodes (K)")
	axarr[1,0].set_ylabel("Ratio of degree (K/N)")

	d.generate("poisson", lam=10, scaletoone=True)
	axarr[1,1].plot(range(d.bins), d.amounts, "-o", color='k', label="poisson")
	sampled_poisson = list (x for x in d.sample_distribution(100000))
	# hist_poisson = histogram(sampled_poisson, bins=PRECISION, density=True)
	hist_poisson = myownhistogram(sampled_poisson, bins=PRECISION, Normed=True)
	# axarr[1,1].plot(range(d.bins), hist_poisson[0], "-o",  color=(0.5,0.5,0.5), label="sampled poisson")
	axarr[1,1].plot(range(d.bins), hist_poisson, "-o",  color=(0.5,0.5,0.5), label="sampled poisson")
	axarr[1,1].legend(prop={'size':6})
	axarr[1,1].set_xlim(0,PRECISION)
	axarr[1,1].set_ylim(0,1)
	axarr[1,1].set_xlabel("Degree of nodes (K)")
	axarr[1,1].set_ylabel("Ratio of degree (K/N)")

	show()
	"""
