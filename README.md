# Video Summarization with Superframe Segmentation

Hi, I'm Hunter Thompson, and welcome to my github!

Here I will going off the basis of using my undergrad thesis project based in video-summarization with superframe segmentation

## Setup

First obviously, your going to need to clone the githubs current master branch.

Once that is done make sure you have a few key things to run my code

- Python 2.7
- opencv (cv2)
- numpy
- h5py (used for feature and interest data)

If you wish to run my demo, you will need my static folder.

Simply download from [here](https://drive.google.com/file/d/1v0dfi3dqkh4L7lYXfoI3nT-K4l4K9T5p/view?usp=sharing), and place in flask/app so that its flask/app/static. You will also need an additional python library.

- flask

### Creating your own Demo
- create static folder within flask/app
- Move current interest.hdf5 and features.py inside
- create a folder for each video (name will need to be added as an option inside of index.html)
- Place the video, and summarization inside of the folder
- Summarization can be generated using "create-vid.py" inside utility
- using "get-frames.py" (also in utility) extract the frames of the entire video to the folder

You will also need jquery inside of the static folder, just confirm the version number matches mine inside of index.html

## What to run
In order to generate feature data, you will need the video dataset for SumMe, you can find everything about them on their [website](https://people.ee.ethz.ch/~gyglim/vsum/)

Any other videos you would like to test just need to be placed inside the videos folder.

- "process_vid.py"

Generates feature data for just one selected video

- "get_dataset.py"

Generates feature data for every video inside the videos folder

- "get_int.py"

Generates interest ratings at a per frame level, than decides if a frame is selected or not, and saves 1 for yes or 0 for no to "interest.hdf5".

- "demo.py"

Runs a wrapper I build with for SumMes evaluation demo, generates an image displaying F-Measure over every video and comparing it to the human average.

Other files are simply contain helper functions.
