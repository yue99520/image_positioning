from Library.ImageRecognition import Darknet
from Library.CameraControl import access_camera_xy
import cv2.cv2 as cv
import time

net = Darknet()

cam = access_camera_xy()
count = 0
current_x = 0
current_y = 0
while True:
    ret, frame = cam.read()
    virtual_positions = net.detect(frame)

    if len(virtual_positions) is 0:
        print("------------------------------------------")

    for p in virtual_positions:
        p.draw(frame)
        if current_x != p.x or current_y != p.y:
            print(str(p.id) + ' x:' + str(p.x) + ' y:' + str(p.y))
            current_x = p.x
            current_y = p.y
    cv.imshow('test', frame)
    cv.waitKey(1)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
