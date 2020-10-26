import logging
import Config
import Library.View as View
from pydobot.dobot import Dobot
from cv2 import cv2 as cv
from serial.tools import list_ports
from Library.CameraControl import init_camera, access_camera_z
from Library.Coordinate import find_real_position
from Library.ItemHigh import calculate_item_high
from Library.Entity import VirtualPosition, Coordinate
from Library.ImageRecognition import DarknetProxy


class PointRecord:
    def __init__(self, point):
        self.point = point
        self.count = 1

    def add_count(self):
        self.count += 1


def init_log():
    logging.basicConfig(level=Config.LOGGING_LEVEL, format=Config.LOGGING_FORMAT)


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


def init_dobot():
    dobot = Dobot(list_ports.comports()[1].device)
    return dobot.home(), dobot
    # return None, dobot


# def detect_coordinate(cam_xy, net_o, net_x, net_y):
#     count = 1
#     while True:
#         logging.info('Start fetching coordinate...')
#         frame = cam_xy.read()
#         po = net_o.detect(frame)
#         px = net_x.detect(frame)
#         py = net_y.detect(frame)
#         if len(py) != 1 or len(px) != 1 or len(po) != 1:
#             logging.debug('Trying to fetch(' + str(count) + ') --- fail')
#             count += 1
#             if count >= 100:
#                 logging.error('Cannot fetch coordinates.')
#                 exit(-1)
#         else:
#             logging.info('Trying to fetch(' + str(count) + ') --- success')
#             return po[0], px[0], py[0]


# def detect_object(cam_xy, net_obj):
#     count = 1
#     while True:
#         logging.info('Start fetching objects...')
#         frame = cam_xy.read()
#         p = net_obj.detect(frame)
#         if len(p) >= 1:
#             logging.debug('Trying to fetch(' + str(count) + ') --- fail')
#             count += 1
#             if count >= 100:
#                 logging.error('Cannot fetch any objects.')
#                 exit(-1)
#         else:
#             logging.info('Trying to fetch(' + str(count) + ') --- success')
#             return p[0]


def object_detection(cam, net):
    point_records = []
    nothing_detected_notice = True
    while True:
        ret, frame = cam.read()
        virtual_positions = net.detect(frame)

        if len(virtual_positions) is 0 and nothing_detected_notice is True:
            logging.info("Nothing detected...")
            nothing_detected_notice = False
            continue

        best_p = get_single_frame_best_detection(virtual_positions)

        if best_p is not None:
            is_best, point = get_best_detection_overall(point_records, best_p)
            if is_best:
                return point


def get_best_detection_overall(records, best_p):
    new_record = True
    for p in records:
        if int(p.point.x) == int(best_p.x) and int(p.point.y) == int(best_p.y):
            p.add_count()
            if p.count >= 10:
                return True, p.point
            new_record = False
    if new_record is True:
        records.append(PointRecord(best_p))
    return False, None


def get_single_frame_best_detection(virtual_positions):
    best_p = VirtualPosition()
    for p in virtual_positions:
        if p.width >= best_p.width and p.height >= best_p.height:
            best_p = p
    if best_p.x <= 10 or best_p.y <= 10:
        best_p = None
    return best_p


def environment_correction(cam_xy):
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
            cv.destroyWindow('Correction')
            break
    return po, px, py


def move_object(dobot, x, y):
    fix = 120

    dobot.move_to(x * 10, y * 10 + fix, 20)
    dobot.suck(True)
    dobot.move_to(x * 10, y * 10 + fix, -50)

    dobot.move_to(x * 10, y * 10 + fix, 20)
    dobot.move_to(120, -150, -20)
    dobot.suck(False)
    return dobot.move_to(120, 0, 0)


if __name__ == '__main__':
    init_log()
    logging.info('Application initializing...')

    logging.info('Start dobot resetting')
    cmd_reset, dobot = init_dobot()
    # net_o, net_x, net_y = init_darknet()
    net_obj = init_obj_net()
    camera = init_camera()

    """
    Environment correction
    """
    logging.info('Start environment correcting')
    coord = Coordinate()
    coord.origin, coord.x, coord.y = environment_correction(camera)

    """
    Waiting for dobot initialize
    """
    logging.info('Wait for dobot reset to complete...')
    # dobot.wait_for_cmd(cmd_reset)
    logging.info('Dobot reset complete')

    logging.info('-----Application start-----|')

    # view = View.ViewThread("Application View", camera)
    # view.start()

    while True:
        # coord.origin, coord.x, coord.y = detect_coordinate(cam_xy, net_o, net_x, net_y)
        obj = object_detection(camera, net_obj)

        # 計算真實座標
        x, y = find_real_position(coord, obj)
        real_xy = {'x': x, 'y': y}
        logging.debug('Real Position --- [x: ' + str(round(real_xy['x'], 2)) + ' cm], [y: ' + str(round(real_xy['y'], 2)) + ' cm]')

        View.view_items.clear()
        View.view_items.append(View.Point(int(real_xy['x']), int(real_xy['y']), "Target Center"))
        View.view_items.append(View.Rectangle(obj, ""))

        cmd_moving = move_object(dobot, real_xy['x'], real_xy['y'])
        dobot.wait_for_cmd(cmd_moving)

        # while True:
        #     ret, frame = camera.read()
        #     obj.draw(frame)
        #     cv.imshow('Object', frame)
        #     if cv.waitKey(1) & 0xFF == ord('q'):
        #         break
