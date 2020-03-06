from StateMachine.drone_states import IdleState, TakeOffState, LandState
from djitellopy import Tello
import time
import sys


class DroneObject:


    def __init__(self):
        self.state = IdleState()
        self.tello = Tello()
        self.coordinate = (0, 0)
        self.FPS = 30
        self.distance = 30 #pre defined, to be changed later


    def on_event(self, event):

        self.state = self.state.on_event(event)

    def set_parameter (self, x,y, dist):
        self.coordinate = (x,y)
        self.distance = dist

    def take_off(self):
        self.tello.takeoff()
        for i in range (0,5):
            print("taking off %d /5" % (i+1))
            time.sleep(1)
        self.on_event("track")

    def land(self):
        self.tello.land()
        for i in range (0,5):
            print("landing %d / 5" % (i+1))
            time.sleep(1)
        self.on_event("idle")


    def track(self):
        if (self.distance > 70):
            self.tello.move_forward(20)
            time.sleep(0.05)
        elif (self.distance < 50):
            self.tello.move_back(20)
            time.sleep(0.05)

        if (self.coordinate[0] < 200 and self.coordinate[0]> 0):
            self.tello.rotate_counter_clockwise(10)
            time.sleep(0.05)
        elif(self.coordinate[0] < 400 and self.coordinate[0]>=200):
            self.tello.move_left(20)
            time.sleep(0.05)

        if (self.coordinate[0] < 759 and self.coordinate[0]>= 559):
            self.tello.move_right(20)
            time.sleep(0.05)
        elif(self.coordinate[0]< 959 and self.coordinate[0]>= 759):
            self.tello.rotate_clockwise(10)
            time.sleep(0.05)

        if (self.coordinate[1] > 0 and self.coordinate[1]<=200):
            self.tello.move_up(20)
            time.sleep(0.05)
        elif (self.coordinate[1]>=519 and self.coordinate[1] <719):
            self.tello.move_down(20)
            time.sleep(0.05)
        return


    def setup(self):
        if not self.tello.connect():
            print("Tello not connected")
            sys.exit()

        # In case streaming is on. This happens when we quit this program without the escape key.
        if not self.tello.streamoff():
            print("Could not stop video stream")
            sys.exit()

        if not self.tello.streamon():
            print("Could not start video stream")
            sys.exit()

        print("Current battery is " + self.tello.get_battery())
        self.tello.streamon()
        frame_read = self.tello.get_frame_read()

    def action(self):
        print("current state is" , self.state)
        print(str(self.state))
        if (str(self.state) == "TakeOffState"):
            print("take off!")
            self.take_off()
        elif (str(self.state) == "LandState"):
            print("land")
            self.land()
        if (str(self.state)== "TrackState"):
            self.track()

        else:
            return #idle state or undefined state do nothing
        return
