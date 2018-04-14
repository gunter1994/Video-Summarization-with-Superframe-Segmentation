from flask import Flask, render_template, Response, jsonify, request
import time
import h5py
import numpy as np

# creates a Flask application, named app
app = Flask(__name__)
f = h5py.File('static/features.hdf5') #qual,track,unique,length
fea = np.array(f['fea_12'])
motion = np.array(f['mot_12'])
vid = "Jumps"
num = '12'

# a route where we will display a welcome message via an HTML template
@app.route("/")
def index():
	global motion,fea
	l = len(motion)
	return render_template('index.html',length=l,motion=int(100*motion[0]),qual=int(100*fea[0][0]),track=int(100*fea[0][1]),unique=int(100*fea[0][2]))

@app.route('/_get_frame_info')
def get_frame_info():
	val = request.args.get('i', 0, type=int)
	j = 0
	for i in range(len(fea)):
		j += fea[i][3]
		if val < j:
			m = int(100*motion[val])
			q = int(100*fea[i][0])
			t = int(100*fea[i][1])
			u = int(100*fea[i][2])
			break
	return jsonify(motion=m,qual=q,track=t,unique=u,img="/static/" + vid + "/frame" + str(val) + ".jpg")

@app.route('/_change_video')
def change_video():
	global motion,fea,f,vid,num
	vid = request.args.get('vid', 'Jumps', type=None)
	num = request.args.get('num', '12', type=None)
	motion = np.array(f['mot_' + num])
	fea = np.array(f['fea_' + num])
	l = len(motion)
	img = "/static/" + vid + "/frame0.jpg"
	orVid = "/static/" + vid + "/" + vid + ".ogg"
	sumVid = "/static/" + vid + "/sum.ogg"
	return jsonify(length=l,motion=int(motion[0]*100),qual=int(fea[0][0]*100),track=int(fea[0][1]*100),unique=int(fea[0][2]*100),img=img,orVid=orVid,sumVid=sumVid)

# run the application
if __name__ == "__main__":  
	app.run(threaded=True)