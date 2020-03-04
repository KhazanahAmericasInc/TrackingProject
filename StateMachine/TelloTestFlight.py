from StateMachine.DroneObject import DroneObject
import time
import cv2
from djitellopy import Tello
import sys

tello = Tello()
FPS = 30
if not tello.connect():
    print("Tello not connected")
    sys.exit()

time.sleep(1)
# In case streaming is on. This happens when we quit this program without the escape key.
if not tello.streamoff():
    print("Could not stop video stream")
    sys.exit()

if not tello.streamon():
    print("Could not start video stream")
    sys.exit()

print ("Current battery is " + tello.get_battery())

tello.takeoff()
time.sleep(1)

tello.streamon()
cv2.namedWindow("drone")
#vidcap =cv2.VideoCapture(tello.get_udp_video_address())
#image =vidcap.read()
frame_read = tello.get_frame_read()

while True:
    #vidcap.set(cv2.CAP_PROP_POS_MSEC, (count*1000))
    frame = frame_read.frame
    #frame = vidcap.read()
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow("drone", frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

    time.sleep(1 / FPS)

tello.land()
tello.streamoff()
cv2.destroyAllWindows()

"""

FPS = 30
drone = DroneObject()

drone.setup()
frame_read = drone.tello.get_frame_read()

while True:
    frame = frame_read.frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow("gray", gray)
    cv2.imshow("video", frame)
    drone.take_off()

    time.sleep(5)

    drone.land()
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    time.sleep = (1/FPS)
drone.tello.streamoff()

"""