import numpy as np
import cv2
import cv2.aruco as aruco
import sys, time, math
from StateMachine.DroneObject import DroneObject




#Find Distance
#Param: coordinates: np.array of 4 coordinates of the detected marker, from top left corner going clockwise
        #knownWidth: predefined width of teh marker
        #focalLength: predefined focalLength of camera (different for each camera)
#return: distance (int)

def DistancetoCamera(coordinates, knownWidth, focalLength):
    pixel_width = abs(coordinates[0][0][0]-coordinates[0][1][0])**2 + abs(coordinates[0][0][1]-coordinates[0][1][1])**2
    pixel_width = pixel_width**0.5
    return (knownWidth*focalLength)/pixel_width

#Determine Orientation
#Param: TopPoint: Tuple for top point
        #BottomPoint: Tuple for bottom point
#return: number between 0 to 360
def orientation (TopPoint, BottomPoint):
    dy = -(TopPoint[1] - BottomPoint[1])
    dx = (TopPoint[0] - BottomPoint[0])
    if (dx ==0): #special case, don't want to divide by 0!
        if (dy>0):
            return 90
        else:
            return 270


    angle = int(math.degrees(math.atan(dy/dx)))

    if (dy>0):
        if (dx < 0):
            angle = 180 + angle
        else:
            return angle
    else:
        if (dx < 0):
            angle += 180
        else:
            angle += 360


    return angle

#Determine command based on orientation of the marker
#Param: orientation, a number between 360
#return: null

def StateTransition(orientation):
    if (orientation > 360 or orientation < 0):
        print("invalid orientation, orientation should be between 0 adn 360")
        return

    if (orientation < 100 and orientation > 80):
        drone.on_event("take_off")


    elif (orientation < 280 and orientation > 260):
        drone.on_event("land")
    return

#Draw HUD information on the screen for human operator
#Param: frame: frame to write on
        #Distance: distance to camera
        #coordinates: 4 corners of the marker
        #angle: orientation of marker
        #center: center of marker
        #ids: ids of marker
        #corners: a list of coordinates for aruco.drawDectedMarkers
#return: nothing


def Draw (frame, Distance, coordinates, angle, Center, ids, corners):

    cv2.putText(frame, ('Distance %d' % Distance), (10, 95), cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 255),
                2, cv2.LINE_AA)
    cv2.circle(frame, Center, 2, (255, 0, 0), thickness=1)
    cv2.circle(frame, (int(coordinates[0][0][0]), int(coordinates[0][0][1])), 4, (255, 0, 0), thickness=-1)
    cv2.circle(frame, (int(coordinates[0][1][0]), int(coordinates[0][1][1])), 4, (255, 0, 0), thickness=-1)
    cv2.putText(frame, ('Orientation %d' % angle), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 0),
                2,
                cv2.LINE_AA)
    cv2.putText(frame, ('Center %d,%d' % Center), (10, 15), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 0), 2,
                cv2.LINE_AA)
    cv2.putText(frame, ('id %s' % ids), (10, 35), cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 255), 2,
                cv2.LINE_AA)
    aruco.drawDetectedMarkers(frame, corners, borderColor=(255, 255, 255))
    return

#Determines the amount of tilt of the marker
#Param: state: state of the drone
        #frame: frame to draw on
        #coordinates: coordinates of the detected marker
        #orientation: orientation of the marker
#Returns: ratio of the right side length over the left side length, 0 if nothing is detected
def Tilt(state, frame, coordinates, orientation):
    Ratio = 0
    if (str(state) != "TrackState"):
        return Ratio
    if (orientation > 140 and orientation < 220):
        LeftSide = ((coordinates[0][1][0] - coordinates[0][0][0]) ** 2 + (
                    coordinates[0][1][1] - coordinates[0][0][1]) ** 2) ** 0.5
        RightSide = ((coordinates[0][2][0] - coordinates[0][3][0]) ** 2 + (
                    coordinates[0][2][1] - coordinates[0][3][1]) ** 2) ** 0.5
        Ratio = (1.0* RightSide / LeftSide)
        cv2.putText(frame, ("Ratio is %s " % Ratio), (400, 15), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 0), 2, cv2.LINE_AA)

    elif ((orientation > 310 and orientation <= 360) or (orientation >= 0 and orientation <= 30)):
        RightSide = ((coordinates[0][1][0] - coordinates[0][0][0]) ** 2 + (
                coordinates[0][1][1] - coordinates[0][0][1]) ** 2) ** 0.5
        LeftSide = ((coordinates[0][2][0] - coordinates[0][3][0]) ** 2 + (
                coordinates[0][2][1] - coordinates[0][3][1]) ** 2) ** 0.5
        Ratio = (1.0 * RightSide / LeftSide)
        cv2.putText(frame, ("Ratio is %s" % Ratio), (400, 15), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 0), 2, cv2.LINE_AA)
    return Ratio

if __name__ == "__main__":
    #Create drone object and set up communication
    drone = DroneObject()
    drone.setup()
    frame_read = drone.tello.get_frame_read()
    time.sleep(5)

    angle = 0
    KNOWN_WIDTH = 9.7
    FOCAL_LENGTH = 630
    tilt = 0

    while (True):
        #retrieve frame and convert to black and white
        frame = frame_read.frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #Detect 6X6 marker
        aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
        parameters =  aruco.DetectorParameters_create()
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

        #if markers are detected
        if (len(corners)!=0):
            aruco.drawDetectedMarkers(frame, corners, ids, (0,0,0))

            #determine center of the marker
            coordinates = tuple(corners[0])
            centerY = int((coordinates[0][0][1] + coordinates[0][2][1]) / 2)
            centerX = int((coordinates[0][0][0] + coordinates[0][2][0]) / 2)
            Center = (centerX,centerY)

            #determine angle, distance, state command, and pass in drone command
            angle = orientation((int(coordinates[0][3][0]),int(coordinates[0][3][1])),(int(coordinates[0][0][0]), int(coordinates[0][0][1])) )
            Distance = DistancetoCamera(coordinates, KNOWN_WIDTH, FOCAL_LENGTH)
            StateTransition(angle)
            tilt = Tilt(drone.state, frame, coordinates, angle)
            drone.set_parameter(Center[0], Center[1], Distance, tilt)

            print (coordinates)
            #draw HUD for BGR and gray screen
            Draw(gray, Distance, coordinates, angle, Center, ids, corners )
            Draw(frame, Distance, coordinates, angle, Center, ids, corners)
            #send command to the drone
            drone.action()

        #print state info on the drone
        cv2.putText(frame, ("Drone state: %s" % drone.state), (600, 15), cv2.FONT_HERSHEY_SIMPLEX, .5,
                    (255, 255, 255),
                    2, cv2.LINE_AA)
        cv2.putText(gray, ("Drone state: %s" % drone.state), (600, 15), cv2.FONT_HERSHEY_SIMPLEX, .5,
                    (255, 255, 255),
                    2, cv2.LINE_AA)

        #show screen
        cv2.imshow('frame', frame)
        cv2.imshow('gray', gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        time.sleep(1/30)
    # When everything done, release the capture

    cv2.destroyAllWindows()
    sys.exit()
