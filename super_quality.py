import matplotlib.pyplot as plt
import numpy as np

'''
print "Loading quality..."

quality = []
with open('quality.txt') as fp:
    for num in fp:
    	quality.append(float(num))

print "Loading supers..."

supers = []
with open('supers.txt') as fp:
    for num in fp:
    	supers.append(int(num))

print supers
'''
def getSupQual(quality,supers):
	supQual = []
	for i in range(len(supers)-1):
		supQual.append(np.average(quality[supers[i]:supers[i+1]]))
	return supQual

'''
f = open("sup-quality.txt","w")
for q in supQual:
	f.write(str(q) + '\n')
f.close()

plt.plot(supQual)
plt.show()
'''