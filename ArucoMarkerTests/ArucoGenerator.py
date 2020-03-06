import numpy as np
import cv2, PIL
from cv2 import aruco
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd


if __name__=='__main__':

    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    fig = plt.figure()
    ax = fig.add_subplot (1,1,1)
    img = aruco.drawMarker(aruco_dict,1, 700)
    plt.imshow(img, cmap=mpl.cm.gray, interpolation= "nearest")
    ax.axis("off")

    plt.savefig("_data/markers.png")
    plt.show()
