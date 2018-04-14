import cv2
import h5py
import numpy as np
import sys
import matplotlib.pyplot as plt
import argparse
import get_supers
import super_quality
import object_track

#helper functions
def getContrast(f):
	gray = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
	return np.std(gray) + (0.3 * np.mean(gray)),np.mean(gray)

def getColour(f):
	#based on example from the following link
	#https://www.pyimagesearch.com/2017/06/05/computing-image-colorfulness-with-opencv-and-python/
	(B, G, R) = cv2.split(f.astype("float"))
	rg = abs(R - G)
	yb = abs(0.5*(R + G) - B)
	stdRoot = np.sqrt((np.std(rg) ** 2) + (np.std(yb) ** 2))
	meanRoot = np.sqrt((np.mean(rg) ** 2) + (np.mean(yb) ** 2))
	return stdRoot + (0.3 * meanRoot),(np.mean(B),np.mean(G),np.mean(R))

def getEdge(f):
	lap = cv2.Laplacian(f, cv2.CV_64F)
	return np.std(lap)**2,np.mean(lap)

def process(videofile):

	cap = cv2.VideoCapture(videofile)

	fps = int(cap.get(5))

	motion = []
	camMot = []
	edges = []
	uEdges = []
	colours = []
	uColours = []
	contrasts = []
	uContrasts = []
	unique = np.array([0,0,0])

	print "Calculating motion, and quality..."

	#calculate motion
	motion.append(0)
	flow = None
	#grab first frame since missing form loop
	ret, old = cap.read()
	while True:
		if old.shape[0] > 480 and old.shape[1] > 640:
			old = cv2.pyrDown(old)
		else:
			break
	#old = cv2.resize(old,(640, 480),interpolation=0)
	t1,t2 = getEdge(old) #creates temp variables
	edges.append(t1)
	uEdges.append(t2)
	t1,t2 = getColour(old)
	colours.append(t1)
	uColours.append(t2)
	t1,t2 = getContrast(old)
	contrasts.append(t1)
	uContrasts.append(t2)
	i = 1
	while(True):
		ret, new = cap.read()
		if not ret:
			break
		while True:
			if new.shape[0] > 480 and new.shape[1] > 640:
				new = cv2.pyrDown(new)
			else:
				break
		#new = cv2.resize(new,(640, 480),interpolation=2)
		t1,t2 = getEdge(new) #creates temp variables
		edges.append(t1)
		uEdges.append(t2)
		t1,t2 = getColour(new)
		colours.append(t1)
		uColours.append(t2)
		t1,t2 = getContrast(new)
		contrasts.append(t1)
		uContrasts.append(t2)

		gray1 = cv2.cvtColor(new, cv2.COLOR_BGR2GRAY)
		gray2 = cv2.cvtColor(old, cv2.COLOR_BGR2GRAY)
		flow = cv2.calcOpticalFlowFarneback(gray2,gray1,flow, 0.5, 2, 15, 2, 5, 1.1, 1) #calculate the optical flow of entire frame
		mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
		mag = np.ma.masked_invalid(mag) #prevent errors from inf values
		motion.append(np.mean(mag))
		camMot.append(np.median(mag))
		'''
		if i%50 == 0:
			print "Frame " + str(i) + ": " + str(motion[i])
		'''
		old = new
		i+=1

	cap.release()
	#normalize motion
	motion = np.array(motion)
	motion = motion/max(motion)

	#normalize quality
	mEdge = np.mean(edges)
	mCol = np.mean(colours)
	mCon = np.mean(contrasts)
	quality = []
	for i in range(len(edges)):
		quality.append(edges[i]/mEdge + colours[i]/mCol + contrasts[i]/mCon)

	#added motion smoothing here instead of having seperate file
	motion = np.convolve(motion,[0.05,0.05,0.1,0.2,0.2,0.2,0.1,0.05,0.05],"same") #seudo gaussian

	print "Calculating superframes..."

	supers = get_supers.getSupers(motion,fps)

	print "Calculating superframe quality..."

	supQual = super_quality.getSupQual(quality,supers)
	#calculate uniqueness, edges colours contrasts
	unique = []
	uMEdge = np.mean(uEdges)
	uMCol = np.mean(uColours)
	uMCon = np.mean(uContrasts)
	for i in range(len(supers)-1):
		unique.append(abs(np.mean(uEdges[supers[i]:supers[i+1]])-uMEdge) + 
						abs(np.linalg.norm(np.mean(uColours[supers[i]:supers[i+1]])-uMCol)) +
						abs(np.mean(uContrasts[supers[i]:supers[i+1]])-uMCon))
	unique = np.array(unique)/max(unique)

	print "Calculating object tracking..."

	supQual = np.array(supQual)
	supQual = supQual/max(supQual)

	scores = object_track.getTrack(supers,camMot,videofile,supQual)

	#normalizing
	scores = np.array(scores)
	scores = scores/max(scores)
	lens = []
	for i in range(len(supers)-1):
		lens.append(supers[i+1]-supers[i])

	return supQual,scores,lens,motion,unique

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Thesis motion generator')
	parser.add_argument('videofile', help='video file')
	parser.add_argument('--out', help='output text file where interest is stored', default='interest.txt')
	parser.add_argument('-p', help='plot motion graph, before and after smoothing', action='store_true')

	args = parser.parse_args()

	supQual,scores,supers,motion,unique = process(args.videofile)

	if (args.p):
		plt.plot(motion, 'r-')
		plt.plot(motion2, 'b-')
		plt.ylabel('Normalized Motion')
		plt.xlabel('Frame')
		plt.show()
		plt.plot(quality)
		plt.ylabel('Quality')
		plt.xlabel('Frame')
		plt.show()

	#save all information for examination
	with h5py.File("test.hdf5",'w') as f:
		q = np.array(supQual)
		t = np.array(scores)
		l = np.array(supers)
		m = np.array(motion)
		u = np.array(unique)
		f.create_dataset("qual", data=q)
		f.create_dataset("track", data=t)
		f.create_dataset("length", data=l)
		f.create_dataset("motion", data=m)
		f.create_dataset("unique", data=u)