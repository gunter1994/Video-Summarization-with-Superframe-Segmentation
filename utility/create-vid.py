import cv2
import argparse
import numpy as np
import h5py
import sys

parser = argparse.ArgumentParser(description='Thesis video generator')
parser.add_argument('vidn', help='video number in interest database')
parser.add_argument('frameLoc', help='location of folder holding frames')

args = parser.parse_args()

'''
ints = np.sort(np.array(ints))

maxLen = int(0.3*len(ints))
sumLen = 0
'''
f = h5py.File('interest.hdf5')

ints = f['vid_' + str(args.vidn)]

imgs = []
for i in range(len(ints)):
	if ints[i] == 1:
		imgs.append(cv2.imread(args.frameLoc + "/frame" + str(i+1) + ".jpg"))
	#cost = 
	#	imgs.append(cv2.imread(args.frameLoc + "/frame" + str(i+1) + ".jpg"))

height , width , layers =  imgs[0].shape

video = cv2.VideoWriter('sum.avi',cv2.VideoWriter_fourcc(*'DIVX'),30,(width,height))

for f in imgs:
	video.write(f)

cv2.destroyAllWindows()
video.release()