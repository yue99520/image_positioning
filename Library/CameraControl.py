from cv2 import cv2 as cv
from Config import CAM_XY_PORT, CAM_Z_PORT


def access_camera_xy():
    return cv.VideoCapture(CAM_XY_PORT)


def access_camera_z():
    return cv.VideoCapture(CAM_Z_PORT)
