from Library.ImageRecognition import DarknetProxy
from Library.CameraControl import access_camera_xy
from Library.Entity import VirtualPosition
import Config
import cv2.cv2 as cv
import time


point_records = []


class PointRecord:
    def __init__(self, point):
        self.point = point
        self.count = 1

    def add_count(self):
        self.count += 1


def get_best_point(virtual_positions):
    best_p = VirtualPosition()
    for p in virtual_positions:
        if p.width >= best_p.width and p.height >= best_p.height:
            best_p = p
    return best_p


def get_actual_point(cam, net):
    while True:
        ret, frame = cam.read()
        virtual_positions = net.detect(frame)

        if len(virtual_positions) is 0:
            print("------------------------------------------")
            continue

        best_p = get_best_point(virtual_positions)

        new_record = True
        for p in point_records:
            if int(p.point.x) == int(best_p.x) and int(p.point.y) == int(best_p.y):
                p.add_count()
                if p.count >= 10:
                    return p.point
                new_record = False
        if new_record is True:
            point_records.append(PointRecord(best_p))


if __name__ == '__main__':
    net = DarknetProxy(Config.CFG_COORDINATE_ORIGIN_PATH, Config.WEIGHTS_COORDINATE_ORIGIN_PATH, Config.DATA_COORDINATE_ORIGIN_PATH)

    cam = access_camera_xy()
    count = 0
    ret, base_frame = cam.read()

    actual_p = get_actual_point(cam, net)

    print('conf: ' + str(round(actual_p.confidence, 2) * 100) + '% | id: ' + str(actual_p.id) + ' | x:' + str(actual_p.x) + ' | y:' + str(actual_p.y))
    cv.circle(base_frame, (int(actual_p.x), int(actual_p.y)), 1, (0, 0, 255), -1)
    cv.imshow('test', base_frame)
    cv.waitKey(0)

    # if cv.waitKey(1) & 0xFF == ord('q'):
    #     break
    # cam.release()
    # cv.destroyWindow('test')
