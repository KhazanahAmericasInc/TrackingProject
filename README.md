# TrackingProject
The goal of this project is to control robots or drones using a coloured marker or Aruco Marker
To Run: 

##To Run
_Please use Linux OS, this will not work with Windows._ 
1. Turn on Tello Drone
2. Connect to Tello Wifi
3. Open terminal on Ubuntu 18.04 LTS, go to the main directory of TrackingProject
To run color marker tracking version, run:
`python3 ColorTracking.py`
- use 14.5cm side length large color marker

To run aruco marker edge tracking version, run:
`python3 TrackTelloAruco.py`
- use 9.5cm aruco marker with white border

To run aruco marker with pose detection, type:
`cd ArucoMarkerTests`
`python3 TrackTelloArucoPose.py`
- use 9.5cm aruco marker with white border

##Checkout Evernote Documentation
Tello Drone Project
https://www.evernote.com/shard/s507/sh/32ab84e8-bef7-4793-beba-94545d6bd723/7b9949a631ed8c73bd018e94cba1a207

Tracking Project
https://www.evernote.com/shard/s507/sh/7a42b570-f74c-41a8-8217-cfc419e9396d/06ebf63103f6d2166e7529c967fb90ea

