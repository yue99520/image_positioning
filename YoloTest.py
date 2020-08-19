from Library.ImageRecognition import Darknet
from Library.CameraControl import access_camera_xy
import cv2.cv2 as cv
import time

net = Darknet()

cam = access_camera_xy()
count = 0
while True:
    ret, frame = cam.read()
    virtual_positions = net.detect(frame)

    for p in virtual_positions:
        p.draw(frame)
        print(str(p.id) + ' x:' + str(p.x) + ' y:' + str(p.y))
    cv.imshow('test', frame)
    cv.waitKey(1)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
