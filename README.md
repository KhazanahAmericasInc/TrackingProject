# TrackingProject
The goal of this project is to control robots or drones using a coloured marker or Aruco Marker

# Libraries
Tested on Ubuntu 18.04 LTS, should be able to run on Ubuntu 16.04 LTS, 17.04, and 19.04, 
python 3.6.x,3.7.x,3.8.x (any variation)

Tested on:
opencv-python 4.2.0.32
aruco 3.1.2.0
numpy 1.18.1
djitellopy 1.5


To install the required libraires: 

`pip install aruco` 

`pip install opencv-python` 

`pip install numpy` 

`pip install djytellopy` 

# To Run
Please use Linux OS, this will not work with Windows._ 
1. Turn on Tello Drone
2. Connect to Tello Wifi
3. Open terminal on Ubuntu 18.04 LTS, go to the main directory of this project
To run color marker tracking version, run:
`python3 TrackTello.py`
- use 14.5cm side length large color marker
- Note: color tracking is inconsistent, please tune the color parameter from line 10 - 13 in that file
- Note2: turn control for color tracking is different from the rest. This will send a turn signal when the marker is near the edge, not when the marker is tilted


To run aruco marker edge tracking version, run:
`python3 TrackTelloAruco.py`
- use 9.5cm aruco marker with white border

To run aruco marker with pose detection, type:
`python3 TrackTelloArucoPose.py`
- use 9.5cm aruco marker with white border

# Control
The drone will always attempt the center the marker in the field of view at a distance of 50cm. The drone will also turn to align its orientation with the orientation of the marker

# Documentation
Tello Drone Project
https://www.evernote.com/shard/s507/sh/32ab84e8-bef7-4793-beba-94545d6bd723/7b9949a631ed8c73bd018e94cba1a207

Tracking Project
https://www.evernote.com/shard/s507/sh/7a42b570-f74c-41a8-8217-cfc419e9396d/06ebf63103f6d2166e7529c967fb90ea

