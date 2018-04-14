import cv2
import argparse
import numpy as np
import h5py
import sys

parser = argparse.ArgumentParser(description='Thesis video generator')
parser.add_argument('--t', help='int threshold', default=0.20)

args = parser.parse_args()

f = h5py.File('features.hdf5')
sums = []

for i in range(25):
	temp = f['fea_'+str(i)]
	vidLen = len(f['mot_'+str(i)])
	maxLen = int(args.t*vidLen)
	sumLen = 0
	fea = np.array(temp)
	inters = []
	for sup in fea:
		inters.append(sup[0] + 0.4*sup[1] + sup[2])
	inters = np.array(inters)/max(inters)
	sums.append([])
	while True: #q,t,u,l
		minCost = 0
		loc = -1
		for sup in range(len(fea)):
			if sup in sums[i]:
				continue
			else:
				newLen = sumLen + fea[sup][3]
				cost = newLen/maxLen - inters[sup]
				if cost < minCost:
					minCost = cost
					loc = sup
		if loc == -1:
			break
		else:
			sums[i].append(loc)
			sumLen += fea[loc][3]
#now select all frames so they may be used for comparison
f2 = h5py.File('interest.hdf5', 'w')
sums = np.array(sums)
for s in range(len(sums)):
	sums[s] = np.sort(sums[s])
	vidLen = len(f['mot_'+str(s)])
	frames = np.zeros(vidLen)
	fea = f['fea_'+str(s)]
	i = 0
	sup = 0
	for j in fea:
		for k in range(int(j[3])):
			if sup in sums[s]:
				frames[i] = 1
			i += 1
		sup += 1
	f2.create_dataset("vid_" + str(s), data=frames)

f2.close()