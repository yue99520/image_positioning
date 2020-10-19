import logging
import Config
from pydobot.dobot import Dobot
from cv2 import cv2 as cv
from serial.tools import list_ports
from Library.CameraControl import access_camera_xy, access_camera_z
from Library.Coordinate import find_real_position
from Library.ItemHigh import calculate_item_high
from Library.Entity import VirtualPosition, Coordinate
from Library.ImageRecognition import DarknetProxy


point_records = []


class PointRecord:
    def __init__(self, point):
        self.point = point
        self.count = 1

    def add_count(self):
        self.count += 1


def init_obj_net():
    object_net = DarknetProxy(Config.CFG_OBJECT_PATH,
                              Config.WEIGHTS_OBJECT_PATH,
                              Config.DATA_OBJECT_PATH)
    return object_net


def init_darknet():
    coord_origin_net = DarknetProxy(Config.CFG_COORDINATE_ORIGIN_PATH,
                                    Config.WEIGHTS_COORDINATE_ORIGIN_PATH,
                                    Config.DATA_COORDINATE_ORIGIN_PATH)
    coord_x_net = DarknetProxy(Config.CFG_COORDINATE_X_PATH,
                               Config.WEIGHTS_COORDINATE_X_PATH,
                               Config.DATA_COORDINATE_X_PATH)
    coord_y_net = DarknetProxy(Config.CFG_COORDINATE_Y_PATH,
                               Config.WEIGHTS_COORDINATE_Y_PATH,
                               Config.DATA_COORDINATE_Y_PATH)

    return coord_origin_net, coord_x_net, coord_y_net


def detect_coordinate(cam_xy, net_o, net_x, net_y):
    count = 1
    while True:
        logging.info('Start fetching coordinate...')
        frame = cam_xy.read()
        po = net_o.detect(frame)
        px = net_x.detect(frame)
        py = net_y.detect(frame)
        if len(py) != 1 or len(px) != 1 or len(po) != 1:
            logging.debug('Trying to fetch(' + str(count) + ') --- fail')
            count += 1
            if count >= 100:
                logging.error('Cannot fetch coordinates.')
                exit(-1)
        else:
            logging.info('Trying to fetch(' + str(count) + ') --- success')
            return po[0], px[0], py[0]


def detect_object(cam_xy, net_obj):
    count = 1
    while True:
        logging.info('Start fetching objects...')
        frame = cam_xy.read()
        p = net_obj.detect(frame)
        if len(p) >= 1:
            logging.debug('Trying to fetch(' + str(count) + ') --- fail')
            count += 1
            if count >= 100:
                logging.error('Cannot fetch any objects.')
                exit(-1)
        else:
            logging.info('Trying to fetch(' + str(count) + ') --- success')
            return p[0]


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


def correction(cam_xy):
    y = (90, 375)
    x = (561, 30)
    o = (70, 46)
    po = VirtualPosition()
    px = VirtualPosition()
    py = VirtualPosition()
    po.x = o[0]
    po.y = o[1]
    px.x = x[0]
    px.y = x[1]
    py.x = y[0]
    py.y = y[1]
    while True:
        ret, frame = cam_xy.read()
        cv.circle(frame, x, 1, (0, 0, 255), -1)
        cv.circle(frame, y, 1, (0, 0, 255), -1)
        cv.circle(frame, o, 1, (0, 0, 255), -1)
        cv.line(frame, o, x, (255, 255, 0))
        cv.line(frame, o, y, (255, 255, 0))
        cv.imshow('Correction', frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    return po, px, py


def dobot_operate(dobot, x, y):
    fix = 120

    dobot.wait_for_cmd(dobot.move_to(x * 10, y * 10 + fix, 20))
    dobot.wait_for_cmd(dobot.suck(True))
    dobot.wait_for_cmd(dobot.move_to(x * 10, y * 10 + fix, -50))
    dobot.wait_for_cmd(dobot.move_to(x * 10, y * 10 + fix, 20))
    dobot.wait_for_cmd(dobot.move_to(120, -150, -20))
    # dobot.wait_for_cmd(dobot.move_to(120, -150, -45))
    dobot.wait_for_cmd(dobot.suck(False))
    # dobot.wait_for_cmd(dobot.move_to(120, 0, 50))


if __name__ == '__main__':
    logging.basicConfig(level=Config.LOGGING_LEVEL, format=Config.LOGGING_FORMAT)
    logging.debug('App started.')

    dobot = Dobot(list_ports.comports()[1].device)
    # dobot.wait_for_cmd(dobot.home())

    # net_o, net_x, net_y = init_darknet()
    net_obj = init_obj_net()
    cam_xy = access_camera_xy()
    coord = Coordinate()
    coord.origin, coord.x, coord.y = correction(cam_xy)
    # coord.origin, coord.x, coord.y = detect_coordinate(cam_xy, net_o, net_x, net_y)
    obj = get_actual_point(cam_xy, net_obj)

    # 計算真實座標
    x, y = find_real_position(coord, obj)
    real_xy = {'x': x, 'y': y}
    logging.debug('[Real Position] x: ' + str(real_xy['x']) + ' cm, y: ' + str(real_xy['y']) + ' cm.')

    dobot_operate(dobot, real_xy['x'], real_xy['y'])

    while True:
        ret, frame = cam_xy.read()
        obj.draw(frame)
        cv.imshow('Object', frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
