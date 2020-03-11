from StateMachine.drone_states import IdleState, TakeOffState, LandState
import tellopy
import time
import sys


def __init__(self):
    self.state = IdleState()
    self.tello = tellopy.Tello()
    self.init_drone()



    self.coordinate = (0, 0)
    self.FPS = 30
    self.distance = 30  # pre defined, to be changed later
    self.tilt = 0



def init_drone(self):
    """Connect, uneable streaming and subscribe to events"""
    # self.drone.log.set_level(2)
    self.drone.connect()
    self.drone.start_video()
    self.drone.subscribe(self.drone.EVENT_FLIGHT_DATA,
                         self.flight_data_handler)
    self.drone.subscribe(self.drone.EVENT_FILE_RECEIVED,
                         self.handle_flight_received)

