# Video-Summarization-with-Superframe-Segmentation

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

Simply download from [here](notyetsetup.com), and place in flask/app so that its flask/app/static.

### Creating your own Demo
- create static folder within flask/app
- Move current interest.hdf5 and features.py inside
- create a folder for each video (name will need to be added as an option inside of index.html)
- Place the video, and summarization inside of the folder
- Summarization can be generated using "create-vid.py" inside utility
- using "get-frames.py" (also in utility) extract the frames of the entire video to the folder

## What to run
In order to generate feature data, you will need the video dataset for SumMe, you can find everything about them on their [website](https://people.ee.ethz.ch/~gyglim/vsum/)

Any other videos you would like to test just need to be placed inside the videos folder.

- "process_vid.py"

Generates feature data for just one selected video
- "get_dataset.py"

Generates feature data for every video inside the videos folder
- "get_int.py"

Generates interest ratings at a per frame level, than decides if a frame is selected or not, and saves 1 for yes or 0 for no to "interest.hdf5".

Other files are simply contain helper functions.
