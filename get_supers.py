import matplotlib.pyplot as plt

motion = []
'''
with open('motion-gaus.txt') as fp:
    for num in fp:
    	motion.append(float(num))
'''

def getSupers(motion,fps):
	r = fps*5 #multiply by the number of seconds you want each superframe to take up on average
	supers = []
	minimas = []
	#default to spacing of 50
	for m in range(len(motion)):
		if m%r == 0:
			supers.append(m)
	if (len(motion)-1)%r != 0:
		supers.append(len(motion)-1)

	for i in range(1,len(motion)-1):
		if motion[i-1] > motion[i] and motion[i+1] > motion[i]:
			minimas.append(i)
	#print minimas

	space = int(fps/10)
	if space < 3:
		space = 3

	for i in range(1,len(supers)-1):
		minimum = supers[i]-(fps-space)
		maximum = supers[i]+(fps-space)
		options = []
		for m in minimas:
			if minimum < m < maximum:
				options.append(m)
		lowest = motion[supers[i]]
		for o in options:
			if motion[o] < lowest:
				lowest = motion[o]
				supers[i] = o
	return supers

'''
plt.plot(motion)
for s in supers:
    plt.axvline(x=s, color='r')
plt.show()

f = open("supers.txt","w")
for s in supers:
	f.write(str(s) + '\n')
f.close()
'''