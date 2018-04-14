#!/usr/bin/env python
'''
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Demo for the evaluation of video summaries
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% This script takes a random video, selects a random summary
% Then, it evaluates the summary and plots the performance compared to the human summaries
%
%%%%%%%%
% publication: Gygli et al. - Creating Summaries from User Videos, ECCV 2014
% author:      Michael Gygli, PhD student, ETH Zurich,
% mail:        gygli@vision.ee.ethz.ch
% date:        05-16-2014
'''
import os 
from summe import *
import numpy as np
import random
import h5py
import matplotlib.pyplot as plt
''' PATHS ''' 
HOMEDATA='GT/';
HOMEVIDEOS='videos/';

if __name__ == "__main__":
    # Take a random video and create a random summary for it
    included_extenstions=['mp4']
    videoList=[fn for fn in os.listdir(HOMEVIDEOS) if any([fn.endswith(ext) for ext in included_extenstions])]
    fs = []
    lens = []
    hFs = []
    hLens = []
    for i in range(len(videoList)):
        videoName = videoList[i]
        videoName=videoName.split('.')[0]                                    
        
        #In this example we need to do this to now how long the summary selection needs to be
        gt_file=HOMEDATA+'/'+videoName+'.mat'
        print videoName
        gt_data = scipy.io.loadmat(gt_file)
        user_score=gt_data.get('user_score')
        nFrames=user_score.shape[0];
        nbOfUsers=user_score.shape[1];  

        human_f_measures=np.zeros(nbOfUsers)
        human_summary_length=np.zeros(nbOfUsers)
        for userIdx in range(0, nbOfUsers):
            human_f_measures[userIdx], human_summary_length[userIdx] = evaluateSummary(user_score[:,userIdx],videoName,HOMEDATA);

        hFs.append(np.mean(human_f_measures)*100)
        hLens.append(np.mean(human_summary_length)*100)
    
        f = h5py.File('interest.hdf5')
        vid = f['vid_'+str(i)]
        if len(vid) < nFrames:
            for j in range(nFrames - len(vid)):
                vid = np.append(vid,0)
        summary_selections={}
        summary_selections[0]=vid
        '''Evaluate'''
        #get f-measure at 15% summary length
        [f_measure,summary_length]=evaluateSummary(summary_selections[0],videoName,HOMEDATA)
        print('F-measure : %.3f at length %.2f' % (f_measure, summary_length))
        fs.append(f_measure*100)
        lens.append(summary_length*100)

    colours = np.random.rand(len(videoList))
    for i in range(len(lens)):
        plt.plot([lens[i],hLens[i]], [fs[i],hFs[i]], 'r-')
    alg = plt.scatter(lens,fs,c=colours,marker='^', label='Superframe Segmentation')
    human = plt.scatter(hLens,hFs,c=colours,marker='o', label='Average Human Editing')
    plt.xlabel('summary length[%]')
    plt.ylabel('f-measure')
    plt.title('f-measure for SumMe benchmark')
    plt.legend(handles=[alg,human])
    plt.ylim([0,85])
    plt.xlim([0,20])
    plt.plot([5, 5],[0, 100],'--k')
    plt.plot([15.1, 15.1],[ 0, 100],'--k')
    plt.show()
    print "Average F-measure: " + str(np.mean(fs))
    print "Average F-measure (human): " + str(np.mean(hFs))