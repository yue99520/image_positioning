from Library.ImageRecognition import DarknetProxy
from Library.CameraControl import init_camera
from pydobot.dobot import Dobot
from serial.tools import list_ports
import Config
import cv2.cv2 as cv
import time


def test_yolo():
    # net = DarknetProxy(Config.CFG_COORDINATE_ORIGIN_PATH,
    #                    Config.WEIGHTS_COORDINATE_ORIGIN_PATH,
    #                    Config.DATA_COORDINATE_ORIGIN_PATH)
    net = DarknetProxy(Config.CFG_COORDINATE_Y_PATH,
                       Config.WEIGHTS_COORDINATE_Y_PATH,
                       Config.DATA_COORDINATE_Y_PATH)

    cam = init_camera()
    count = 0
    current_x = 0
    current_y = 0

    while True:
        ret, frame = cam.read()
        # frame = cv.imread('/home/pulab509/Documents/darknet/IMG_1589.JPG')
        virtual_positions = net.detect(frame)

        if len(virtual_positions) == 0:
            print("------------------------------------------")

        for p in virtual_positions:
            p.draw(frame)
            if current_x != p.x or current_y != p.y:
                print(str(p.id) + ' x:' + str(p.x) + ' y:' + str(p.y))
                current_x = p.x
                current_y = p.y
        cv.imshow('test', frame)
        # cv.resizeWindow('test', 512)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break


def test_arm():
    port = list_ports.comports()[1].device
    dobot = Dobot(port=port)
    dobot.home()
    cmd_id = dobot.move_to(100, 150, -50)
    dobot.wait_for_cmd(cmd_id)
    dobot.close()
    print("finish")


if __name__ == "__main__":
    # test_yolo()
    test_arm()
