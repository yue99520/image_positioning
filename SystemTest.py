import logging
import Config
from os import path
from cv2 import cv2 as cv

logging.basicConfig(level=logging.INFO, format=Config.LOGGING_FORMAT)


def generate_log(test_what, result, value):
    if result:
        logging.info('Test ' + str(test_what) + ': OK (' + str(value) + ')')
    else:
        logging.error('Test ' + str(test_what) + ': ERROR (' + str(value) + ')')

# CAM XY
cam = cv.VideoCapture(Config.CAM_XY_PORT)
r = cam.isOpened()
generate_log('[CAM_XY_PORT]', r, Config.CAM_XY_PORT)

ret, frame = cam.read()
cv.imshow('Test Camera XY (Press "ENTER" to continue)', frame)

# CAM Z
cam = cv.VideoCapture(Config.CAM_Z_PORT)
r = cam.isOpened()
generate_log('[CAM_Z_PORT]', r, Config.CAM_Z_PORT)

ret, frame = cam.read()
cv.imshow('Test Camera Z (Press "ENTER" to continue)', frame)

# yolo
r = path.exists(Config.CFG_PATH)
generate_log('[CFG_PATH](yolo)', r, Config.CFG_PATH)

r = path.exists(Config.WEIGHTS_PATH)
generate_log('[WEIGHTS_PATH](yolo)', r, Config.WEIGHTS_PATH)

r = path.exists(Config.DATA_PATH)
generate_log('[DATA_PATH](yolo)', r, Config.DATA_PATH)

cv.waitKey(0)
cv.destroyAllWindows()