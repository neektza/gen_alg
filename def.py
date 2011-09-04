def decodechromosome(self):
		self.nmb = 0
    	for i in range(self.length):
    		self.nmb *= 2
    		if (self.chromosome[i] == 1):
    			self.nmb += 1
		maxnmb = 1 << self.length
		self.x = self.nmb / maxnmb * (self.right - self.left) + self.left
    	return self.x
