import random
import math

MAXIMIZE, MINIMIZE = 11, 22

class Individual(object):
	alleles = (0,1)
	length = 6
	seperator = ''
	left = -20
	right = 20
	x=0.0
	optimization = MINIMIZE
	
	# TODO - vise varijabli (lista varijabli pa pretvorba za svaki po broju bitova koje zauzima)

	def __init__(self, chromosome=None):
		self.chromosome = chromosome or self.makechromosome()
		self.fitness = None

	def function(self, x):
		#return 0.5*(x+2)*(x-10)+math.cos(2*x-8)
		return -pow(x,2)

		#Funkcija f1(x) = (1/2) * (x+2) * (x-10)
		#Funkcija f2(x) = (1/2) * (x+2) * (x-10) + cos(2x-8)
		#Funkcija f3(x) = x^2 + y^2 +3xy -2x -3y

	def makechromosome(self):
		return [random.choice(self.alleles) for gene in range(self.length)]

	def evaluate(self, optimum=None):
		nmb = 0
		for i in range(self.length):
			nmb *= 2
			if (self.chromosome[i] == 1):
				nmb += 1
		maxnmb = 1 << self.length
		self.x = float(nmb) / maxnmb * (self.right - self.left) + self.left
		self.fitness = self.function(self.x)

	def crossover(self, other):
		left, right = self._pickpivots()
		def mate(p0, p1):
			chromosome = p0.chromosome[:]
			chromosome[left:right] = p1.chromosome[left:right]
			child = p0.__class__(chromosome)
			return child
		return mate(self, other), mate(other, self)
	
	def mutate(self, mutation_rate):
		for gene in range(self.length):
			if random.random() < mutation_rate:
				self.chromosome[gene] = random.choice(self.alleles)

	# crossover helper
	def _pickpivots(self):
		left = random.randrange(1, self.length-2)
		right = random.randrange(left, self.length-1)
		return left, right

	# other
	def __repr__(self):
		return '<%s chromosome="%s" fitness=%s>' % (self.__class__.__name__, self.seperator.join(map(str,self.chromosome)), self.fitness)

	def __cmp__(self, other):
		if self.optimization == MINIMIZE: 
			return cmp(self.fitness, other.fitness)
		else: # MAXIMIZE
			return cmp(other.fitness, self.fitness)

	def copy(self):
		twin = self.__class__(self.chromosome[:])
		twin.fitness = self.fitness
		return twin


class Environment(object):
	def __init__(self, kind, population=None, size=100, maxgenerations=100, 
		crossover_rate=0.75, mutation_rate=0.01, optimum=None):
		self.kind = kind
		self.size = size
		self.optimum = optimum
		self.population = population or self.makepopulation()
		for individual in self.population:
			individual.evaluate(self.optimum)
		self.crossover_rate = crossover_rate
		self.mutation_rate = mutation_rate
		self.maxgenerations = maxgenerations
		self.generation = 0
		self.report()

	def makepopulation(self):
		return [self.kind() for individual in range(self.size)]
    
	def run(self):
		while not self.goal():
			self.step()
    
	def goal(self):
		return self.generation >= self.maxgenerations or self.best.fitness == self.optimum
    
	def step(self):
		self.population.sort()
		self.breed()
		self.generation += 1
		self.report()
    
    	def breed(self):
 		next_population = [self.best.copy()]
		while len(next_population) < self.size:
            		mate1, mate2 = self.select()
		  	if random.random() < self.crossover_rate:
		      		offspring = mate1.crossover(mate2)
		  	else:
		      		offspring = [mate1.copy(), mate2.copy()]
		  	for individual in offspring:
			      	individual.mutate(self.mutation_rate)
				individual.evaluate(self.optimum)
				next_population.append(individual)
        		self.population = next_population[:self.size]
        
	def select(self, competitors=3): # tournament
		competitors = [random.choice(self.population) for i in range(competitors)]
		competitors.sort()
		return competitors[0:2]
		
    
    	# helpers...
	def best():
		def fget(self):
			return self.population[0]
		return locals()
	best = property(**best())
    
    	def avg_fitness(self):
		return sum([individual.fitness for individual in self.population])/self.size

	def report(self):
		print "generation:       ", self.generation
		print "best:             ", self.best
		print "average fitness:  ", self.avg_fitness()
        
        # print "min f(x):  ", self.best.function(self.best.x)
        # print "population: ", self.population

env = Environment(Individual, maxgenerations=10)
env.run()

