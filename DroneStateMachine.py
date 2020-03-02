
class DroneState(object):
    idle = True
    takeoff = False
    track = False
    Land = False
    command_ = 0
        #0 -- idle
        #1 -- take off
        #2 -- Land
        #3 -- track
    def __init__(self):
        print("Processing current state")
        idle = True
        takeoff = False
        track = False
        land = False

    def command (self, orientation):
        if (orientation < 100 and orientation > 80):
            print("take off")
            command_ = 1
            return command_
        elif (orientation < 280 and orientation > 260):
            print("landing")
            command_ = 2
            return command_
        else:
            if (self.track):
                print("track")
                command_ = 3
                return command_
            else:
                command_ = 4
                return command_

    def state_transition(self):
        if (self.idle):# if we are at idle state
                if (self.command_==0):
                    print("drone")
                    return
                elif(self.command ==1):
                    print("drone action: take off")




