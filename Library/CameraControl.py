import logging

from cv2 import cv2 as cv
from Config import CAM_XY_PORT, CAM_Z_PORT


def access_camera_xy():
    logging.debug('Access camera XY, port = ' + CAM_XY_PORT)
    cam = cv.VideoCapture(CAM_XY_PORT)
    if cam.isOpened():
        logging.debug('Camera XY is opened.')
    else:
        logging.error('Camera XY is not opened.')
    return cam


def access_camera_z():
    logging.debug('Access camera Z, port = ' + CAM_Z_PORT)
    cam = cv.VideoCapture(CAM_Z_PORT)
    if cam.isOpened():
        logging.debug('Camera Z is opened.')
    else:
        logging.error('Camera Z is not opened.')
    return cam
