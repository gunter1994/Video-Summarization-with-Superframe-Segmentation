#based on open cv tutorial https://docs.opencv.org/3.3.1/d7/d8b/tutorial_py_lucas_kanade.html
import sys
import numpy as np
import cv2

'''
supers = []
with open('supers.txt') as fp:
	for num in fp:
		supers.append(int(num))

motion = []
with open('motion.txt') as fp:
	for num in fp:
		motion.append(float(num))
'''

def Track(frames,j,motion):
	i = 0
	# params for ShiTomasi corner detection
	feature_params = dict( maxCorners = 100,
						   qualityLevel = 0.3,
						   minDistance = 7,
						   blockSize = 7 )
	# Parameters for lucas kanade optical flow
	lk_params = dict( winSize  = (15,15),
					  maxLevel = 2,
					  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
	# Take first frame and find corners in it
	old_frame = frames[i]
	old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
	p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)

	score = 0
	while(1):
		i += 1
		if i >= len(frames):
			break
		frame = frames[i]
		frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		# calculate optical flow
		try:
			p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
		except:
			return score
		# Select good points
		if p1 is None:
			return score
		good_new = p1[st==1]
		good_old = p0[st==1]

		#if object is being tracked it should always be moving slower than background
		s = 0
		for k in range(len(p1)):
			temp = motion[j+i] - np.linalg.norm(p1[k]-p0[k])
			if temp > 0:
				s += temp
		score += s
		# Now update the previous frame and previous points
		old_gray = frame_gray.copy()
		p0 = good_new.reshape(-1,1,2)

	cv2.destroyAllWindows()
	return score

def getTrack(supers,motion,videofile,supQual):
	scores = []
	cap = cv2.VideoCapture(videofile)
	for i in range(len(supers)-1):
		#print "Super: " + str(i)
		if supQual[i] > 0.3:
			frames = []
			for j in range(supers[i+1]-supers[i]):
				ret, frame = cap.read()
				frame = cv2.resize(frame, (640, 480)) 
				if(ret):
					frames.append(frame)
				else:
					break
			scores.append(Track(frames,supers[i],motion))
		else:
			scores.append(0)
	cap.release()
	return scores

'''
f = open("sup-track.txt","w")
for s in scores:
	f.write(str(s) + '\n')
f.close()
'''