import h5py
import numpy as np
import matplotlib.pyplot as plt
import sys
from process_vid import process
import glob

vids = glob.glob('videos/*.mp4')

with h5py.File("features.hdf5") as f:
	i = 0
	for v in vids:
		qual,track,leng,mot,uni = process(v)
		q = np.array(qual)
		t = np.array(track)
		l = np.array(leng)
		m = np.array(mot)
		u = np.array(uni)
		feature = np.stack((q,t,u,l),axis=-1)
		f.create_dataset("fea_" + str(i), data=feature)
		f.create_dataset("mot_" + str(i), data=m)
		i += 1