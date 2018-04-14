import cv2
import argparse

parser = argparse.ArgumentParser(description='Gets frames of video as jpgs')
parser.add_argument('file', help='the video to convert to frames')
parser.add_argument('folder', help='the folder to put the frames')

args = parser.parse_args()

vid = cv2.VideoCapture(args.file)

ret,frame = vid.read()
i = 0
while ret:
	cv2.imwrite(args.folder + "/frame" + str(i) + '.jpg',frame)
	ret,frame = vid.read()
	i += 1