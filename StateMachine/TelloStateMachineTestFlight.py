from StateMachine.DroneObject import DroneObject
import time
import cv2



drone = DroneObject()


drone.setup()
frame_read = drone.tello.get_frame_read()
frame = frame_read.frame
cv2.imshow("frame", frame)
time.sleep(1)

drone.on_event("take_off")
drone.action()
time.sleep(5)

drone.on_event("land")
drone.action()

