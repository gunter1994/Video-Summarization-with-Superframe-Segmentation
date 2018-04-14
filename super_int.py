import matplotlib.pyplot as plt
import numpy as np
import h5py

f = h5py.File("info.hdf5")

qual = np.array(f["qual"])
track = np.array(f["track"])
supers = np.array(f["length"])
unique = np.array(f["unique"])

supInt = []
for i in range(len(supers)):
	for j in range(supers[i]):
		supInt.append(qual[i] + track[i]/4 + unique[i]/4)

supInt = np.array(supInt)/max(supInt)

f = open("sup-int.txt","w")
for i in supInt:
	f.write(str(i) + '\n')
f.close()

plt.plot(supInt)
plt.show()