from StateMachine.drone_states import IdleState, TakeOffState, LandState
from djitellopy import Tello
import time
import sys

#This class is to interact with djitellopy API to control the drone. 
#It is also responsible to generates events for state transition

class DroneObject:

    #initialize the object
    #Set default state to IdleState()
    #Create Tello object from the API
    #set default values for coordinate, FPS, distance, and tilt
    def __init__(self):
        self.state = IdleState()
        self.tello = Tello()
        self.coordinate = (0, 0)
        self.FPS = 30
        self.distance = 30 #pre defined, to be changed later
        self.tilt = 0

    #Generates pass events to tellodrone class
    def on_event(self, event):

        self.state = self.state.on_event(event)
    
    #setter for member variables
    def set_parameter (self, x,y, dist, tilt):
        self.coordinate = (x,y)
        self.distance = dist
        self.tilt = tilt

    #for take off the drone, called when the drone is in takeoff state
    #when take off is complete, trigger event for track
    def take_off(self):
        self.tello.takeoff()
        for i in range (0,3):
            print("taking off %d /3" % (i+1))
            time.sleep(1)
        self.on_event("track")

        
    #for landing the drone, called when the drone is in landingstate
    #when landing is complete, trigger event for idle

    def land(self):
        self.tello.land()
        for i in range (0,3):
            print("landing %d / 3" % (i+1))
            time.sleep(1)
        self.on_event("idle")

    #for tracking the drone, called when the drone is in track state
    #when tilt is active, it will prioritize the turning motion over the other motions
    #controls shifting, moving up and down, forward backwards, and turning
    def track(self):
        if(self.tilt <= 0.95 and self.tilt != 0):
            self.tello.rotate_clockwise(int((1-self.tilt)*100))
            time.sleep(0.05)
        elif(self.tilt >= 1.05):
            self.tello.rotate_counter_clockwise(int((self.tilt-1)*100))
            time.sleep(0.05)
        else:
            if (self.distance > 60):
                forward = int((self.distance - 60))
                if ((forward < 20)):
                    self.tello.move_forward(20)
                else:
                    self.tello.move_forward(forward)
                time.sleep(0.05)
            elif (self.distance < 50):
                backward = int(abs(self.distance - 50))
                if ((backward < 20)):
                    self.tello.move_back(20)
                else:
                    self.tello.move_back(backward)
                time.sleep(0.05)

            if (self.coordinate[0] < 400 and self.coordinate[0] >= 0):
                self.tello.move_left(20)
                time.sleep(0.05)

            elif (self.coordinate[0] < 959 and self.coordinate[0] >= 559):
                self.tello.move_right(20)
                time.sleep(0.05)

            if (self.coordinate[1] > 0 and self.coordinate[1] <= 200):
                self.tello.move_up(20)
                time.sleep(0.05)
            elif (self.coordinate[1] >= 519 and self.coordinate[1] < 719):
                self.tello.move_down(20)
                time.sleep(0.05)
    
    #For setting up the drone
        #Establish connection
        #Initialize streamming
        #Display battery
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

        
    #For calling corresponding functions based on their state
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
