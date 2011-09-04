#
# genetic.py
#

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
    optimization = MAXIMIZE
    
    #todo
    #vise varijabli (lista varijabli pa pretvorba za svaki po broju bitova koje zauzima)

    def __init__(self, chromosome=None):
        self.chromosome = chromosome or self._makechromosome()
        self.fitness = None
       	return None
    	
    def function(self, x):
    	return 0.5*(x+2)*(x-10)+math.cos(2*x-8)
    	
    	#Funkcija f1(x) = (1/2) * (x+2) * (x-10)
		#Funkcija f2(x) = (1/2) * (x+2) * (x-10) + cos(2x-8)
		#Funkcija f3(x) = x^2 + y^2 +3xy -2x -3y
    	
    def _makechromosome(self):
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
    	
    def pie_part(self, avg_fit):
    
    	
    
    def crossover(self, other):
        left, right = self._pickpivots()
        def mate(p0, p1):
            chromosome = p0.chromosome[:]
            chromosome[left:right] = p1.chromosome[left:right]
            child = p0.__class__(chromosome)
            return child
        return mate(self, other), mate(other, self)
    
    def mutate(self, gene):
        self.chromosome[gene] = random.choice(self.alleles)

	#crossover helper
    def _pickpivots(self):
        left = random.randrange(1, self.length-2)
        right = random.randrange(left, self.length-1)
        return left, right

	#other
    def __repr__(self):
        "returns string representation of self"
        return '<%s chromosome="%s" fitness=%s>' % \
               (self.__class__.__name__,
                self.seperator.join(map(str,self.chromosome)), self.fitness)

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
    def __init__(self, kind, population=None, size=5, maxgenerations=100, 
                 crossover_rate=0.75, mutation_rate=0.01, optimum=None):
        self.kind = kind
        self.size = size
        self.optimum = optimum
        self.population = population or self._makepopulation()
        for individual in self.population:
            individual.evaluate(self.optimum)
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.maxgenerations = maxgenerations
        self.generation = 0
        self.report()

    def _makepopulation(self):
        return [self.kind() for individual in range(self.size)]
    
    def run(self):
        while not self._goal():
            self.step()
    
    def _goal(self):
        return self.generation > self.maxgenerations or \
               self.best.fitness == self.optimum
    
    def step(self):
        self.population.sort()
        self._crossover()
        self.generation += 1
        self.report()
    
    def _crossover(self):
        next_population = [self.best.copy()]
        while len(next_population) < self.size:
            mate1 = self._select()
            if random.random() < self.crossover_rate:
                mate2 = self._select()
                offspring = mate1.crossover(mate2)
            else:
                offspring = [mate1.copy()]
            for individual in offspring:
                self._mutate(individual)
                individual.evaluate(self.optimum)
                next_population.append(individual)
        self.population = next_population[:self.size]

    def _select(self):
        "override this to use your preferred selection method"
        return self._tournament()
    
    def _mutate(self, individual):
        for gene in range(individual.length):
            if random.random() < self.mutation_rate:
                individual.mutate(gene)

    #
    # sample selection method
    #
    def _tournament(self, size=8, choosebest=0.90):
        competitors = [random.choice(self.population) for i in range(size)]
        competitors.sort()
        if random.random() < choosebest:
            return competitors[0]
        else:
            return random.choice(competitors[1:])
    
    def best():
        doc = "individual with best fitness fitness in population."
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

env = Environment(Individual, maxgenerations=10000, optimum=0)
env.run()

