chromosome = [1,1,0,1,1,0,0,0,1,0]
nmb = 0
for i in range(10):
	nmb *= 2
	if (chromosome[i] == 1):
		nmb += 1

print nmb
maxnmb = 1 << 10
print maxnmb

x = float(nmb) / float(maxnmb)
print x
