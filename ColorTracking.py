import argparse
import time
import cv2
import numpy as np
import math
from numpy import mean
def tupleAverage (tuple1, tuple2):
    x = int((tuple1[0] + tuple2[0]) / 2)
    y = int((tuple1[1] + tuple2[1]) / 2)

    return (x, y)

def isValid (redRect, blueRect):
    if(redRect[2] < 30 or redRect[3] < 30): #if individual edge is too small
        print("Red edge length too small")
        return False
    if(blueRect[2]< 30 or blueRect[3] < 30):
        print("Blue edge length too small")
        return False
    if(redRect[2] * redRect[3] < 1500): #if total area is too small
        print("Red area too small")
        return False
    if(blueRect[2] * blueRect[3] < 1500):
        print("Blue area too small")
        return False
    distance = (abs(RedCenter[0] - BlueCenter[0])**2 + abs(RedCenter[1] - BlueCenter[1])**2)**0.5
    print('distance between centers are %d' % (distance) )

    if (redRect[2]< redRect[3]): #if width is shorter than height
        if (distance < (redRect[2]+blueRect[2])/4): #should be half of the average
            print ("distance too close")
            return False
        if (distance > (redRect[2] + blueRect[2])):
            print ("distance too far")
            return False
    else:
        if (distance < (redRect[3]+blueRect[3])/4):  #should be half of the average
            print ("distance too close")
            return False
        if (distance > (redRect[3] + blueRect[3])):
            print ("distance too far")
            return False

    return True

def orientation (RedCenter, BlueCenter):
    dy = (RedCenter[1] - BlueCenter[1])
    dx = (RedCenter[0] - BlueCenter[0])
    if (dx ==0): #special case, don't want to divide by 0!
        if (dy>0):
            return 90
        else:
            return 270

    if (dy ==0):
        if (dx>=0):
            return 0
        else:
            return 180
    angle = int(math.degrees(math.atan(dy/dx)))
    return angle

#define the upper and lower bound of blue taht we want to track

blueLower= np.array([82,42,0], dtype = "uint8")
blueUpper = np.array([255,147,67], dtype = "uint8")
redLower = np.array([15,15,135], dtype = "uint8")
redUpper = np.array([115,115,255], dtype = "uint8")
RedCenter = (0,0) #(x,y)
BlueCenter = (0,0) #(x,y)
redRect = (0,0,0,0) #x,y,w,h
blueRect = (0,0,0,0) #x,y,w,h
valid = False #intialize this flag as false, and if any point it becomes false, the program will restart photo capture process

if __name__ == "__main__":
    camera = cv2.VideoCapture(0)

    while True:
        (grabbed, frame) = camera.read()

        blue = cv2.inRange(frame, blueLower, blueUpper)
        blue = cv2.GaussianBlur(blue, (3,3), 0)

        (cnts, _) = cv2.findContours(blue.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #find the largest contour. must use the copy otherwise will destroy the original

        red = cv2.inRange(frame, redLower, redUpper)
        red = cv2.GaussianBlur(red, (3, 3), 0)
        (redcnts, _) = cv2.findContours(red.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


        if len(cnts)> 0:
            cnt = sorted(cnts, key = cv2.contourArea, reverse = True)[0] #sort in reverse order, so 0th is the largest

            blueRect = cv2.boundingRect(cnt)
            BlueCenter = (blueRect[0]+ int(blueRect[2]/2), blueRect[1]+ int(blueRect[3]/2))

            print('Blue:  X: %d, Y: %d, W:%d, H:%d' % (blueRect))

        if len(redcnts)> 0:
            redcnt = sorted(redcnts, key = cv2.contourArea, reverse = True)[0] #sort in reverse order, so 0th is the largest
            redRect = cv2.boundingRect(redcnt)
            print('Red:  X: %d, Y: %d, W:%d, H:%d' % (redRect))

            RedCenter = (redRect[0]+ int(redRect[2]/2), redRect[1]+ int(redRect[3]/2))


        if (isValid(redRect, blueRect)):
            Center = tupleAverage(RedCenter,BlueCenter)
            Angle = orientation(RedCenter, BlueCenter)

            cv2.circle(frame, RedCenter, 10, (0, 0, 255), -1)
            cv2.circle(frame, Center, 10, (0,255,0), -1)
            cv2.circle(frame, BlueCenter, 10, (255, 0, 0), -1)
            cv2.putText(frame, ('Center %d,%d' % Center), (10, 15), cv2.FONT_HERSHEY_SIMPLEX, .5, (255,255,255), 2, cv2.LINE_AA)
            cv2.putText(frame, ('Orientation %d' % Angle), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 255), 2,
                        cv2.LINE_AA)
        cv2.imshow("tracking", frame)
        cv2.imshow("blue", blue)
        cv2.imshow("red", red)



        time.sleep(0.025)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    camera.release()
    cv2.destroyAllWindows()
