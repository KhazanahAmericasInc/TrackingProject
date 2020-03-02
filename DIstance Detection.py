# import the necessary packages
from imutils import paths
import numpy as np
import imutils
import cv2
def find_marker(image):
	# convert the image to grayscale, blur it, and detect edges
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (5, 5), 0)
	edged = cv2.Canny(gray, 35, 125)
	# find the contours in the edged image and keep the largest one;
	# we'll assume that this is our piece of paper in the image
	cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	c = max(cnts, key = cv2.contourArea)
	# compute the bounding box of the of the paper region and return it
	return cv2.minAreaRect(c)

def distance_to_camera(knownWidth, focalLength, perWidth):
	# compute and return the distance from the maker to the camera
	return (knownWidth * focalLength) / perWidth


KNOWN_DISTANCE = 15 #marker is set to 20cm apart from teh camera
KNOWN_WIDTH = 8

image = cv2.imread("Calibration15cm.jpg")
marker = find_marker(image)
color = (255,0,0)
print(marker[0])
print(marker[1])
image = cv2.rectangle(image,(700,191), (500,195), color, -1)
cv2.imshow("picture", image)
focalLength = (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH
print(focalLength)
cv2.waitKey(0)