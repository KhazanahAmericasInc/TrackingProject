import numpy as np
import cv2
import cv2.aruco as aruco
import sys, time, math
'''
    drawMarker(...)
        drawMarker(dictionary, id, sidePixels[, img[, borderBits]]) -> img
'''
marker_size = 6
id_to_find = 1

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
print(aruco_dict)
# second parameter is id number
# last parameter is total image size
img = aruco.drawMarker(aruco_dict, 1, 700)
cv2.imwrite("test_marker.jpg", img)

cap = cv2.VideoCapture(0)
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
        TL = (int(coordinates[0][0][0]), int(coordinates[0][0][1]))
        BR = (int(coordinates[0][2][0]), int(coordinates[0][2][1]))
        gray = cv2.rectangle(gray, TL, BR, (255,255,0), 1)
        centerY = int((coordinates[0][0][1] + coordinates[0][2][1]) / 2)
        centerX = int((coordinates[0][0][0] + coordinates[0][2][0]) / 2)
        Center = (centerX,centerY)
        cv2.circle(gray, Center, 2, (255,0,0), thickness=1)
        cv2.putText(gray, ('Center %d,%d' % Center), (10, 15), cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 255), 2,
                    cv2.LINE_AA)

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

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()