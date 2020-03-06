import numpy as np
import cv2
import cv2.aruco as aruco
import sys, time, math
'''
    drawMarker(...)
        drawMarker(dictionary, id, sidePixels[, img[, borderBits]]) -> img
'''

# second parameter is id number
# last parameter is total image size

def DistancetoCamera(coordinates, knownWidth, focalLength):
    pixel_width = abs(coordinates[0][0][0]-coordinates[0][1][0])**2 + abs(coordinates[0][0][1]-coordinates[0][1][1])**2
    pixel_width = pixel_width**0.5
    return (knownWidth*focalLength)/pixel_width


def orientation (RedCenter, BlueCenter):
    dy = -(RedCenter[1] - BlueCenter[1])
    dx = (RedCenter[0] - BlueCenter[0])
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


cap = cv2.VideoCapture(0)
angle = 0

while (True):
    ret, frame = cap.read();
    #print(frame.shape)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters =  aruco.DetectorParameters_create()


    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)


    if (len(corners)!=0):
        aruco.drawDetectedMarkers(frame, corners, ids, (0,0,0))
        coordinates = tuple(corners[0])

        centerY = int((coordinates[0][0][1] + coordinates[0][2][1]) / 2)
        centerX = int((coordinates[0][0][0] + coordinates[0][2][0]) / 2)
        Center = (centerX,centerY)
        angle = orientation((int(coordinates[0][3][0]),int(coordinates[0][3][1])),(int(coordinates[0][0][0]), int(coordinates[0][0][1])) )
        Distance = DistancetoCamera(coordinates, 12.6, 660)
        cv2.putText (gray, ('Distance %d' % Distance), (10, 95), cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 255),
                    2, cv2.LINE_AA)
        cv2.circle(gray, Center, 2, (255,0,0), thickness=1)
        cv2.circle(gray, (int(coordinates[0][0][0]),int(coordinates[0][0][1])), 4, (255,0,0), thickness=-1)
        cv2.circle(gray, (int(coordinates[0][1][0]), int(coordinates[0][1][1])), 4, (255, 0, 0), thickness=-1)
        cv2.putText(gray, ('Orientation %d' % angle), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, .5, (0,0,0),
                    2,
                    cv2.LINE_AA)
        cv2.putText(gray, ('Center %d,%d' % Center), (10, 15), cv2.FONT_HERSHEY_SIMPLEX, .5, (0,0,0), 2,
                    cv2.LINE_AA)
        cv2.putText(gray, ('id %s' % ids), (10, 35), cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 255), 2,
                    cv2.LINE_AA)
        aruco.drawDetectedMarkers(gray, corners, borderColor=(255,255,255))
        print (coordinates)
    """
    if ids != None:
        ret = aruco.estimatePoseSingleMarkers(corners, marker_size)
        gray = aruco.drawDetectedMarkers(gray, corners)
        rvec,tvec = ret[0][0,0,:], ret[1][0,0,:]
        aruco.drawDetectedMarkers(frame,corners)
        aruco.drawAxis(frame, rvec, tvec, 10)
  """
        # print(rejectedImgPoints)

    # Display the resulting frame
    cv2.imshow('frame', gray)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    time.sleep(1/30)
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()