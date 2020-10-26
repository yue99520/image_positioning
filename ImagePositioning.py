import logging
import Config
import threading
import copy
import Library.View as View
from pydobot.dobot import Dobot
from cv2 import cv2 as cv
from serial.tools import list_ports
from Library.CameraControl import init_camera, access_camera_z
from Library.Coordinate import find_real_position
from Library.ItemHigh import calculate_item_high
from Library.Entity import VirtualPosition, Coordinate
from Library.ImageRecognition import DarknetProxy


class ImageLocator:
    class PointRecord:
        def __init__(self, point):
            self.point = point
            self.count = 1

        def add_count(self):
            self.count += 1

    def __init__(self, cam):
        logging.debug('Initializing ImageLocator...')
        self._cam = cam
        self._darknet = DarknetProxy(Config.CFG_OBJECT_PATH,
                                     Config.WEIGHTS_OBJECT_PATH,
                                     Config.DATA_OBJECT_PATH)
        logging.info('Environment correcting...')
        self._coord = Coordinate()
        self._coord.origin, self._coord.x, self._coord.y = self._environment_correction(Config.COORD_O, Config.COORD_X, Config.COORD_Y)
        logging.info('Correction done.')
        logging.debug('ImageLocator has been initialized.')

    def convert_real_position(self, obj):
        return find_real_position(self._coord, obj)

    def _environment_correction(self, o, x, y):
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
            ret, frame = self._cam.read()
            cv.line(frame, o, x, (255, 255, 0), 1)
            cv.line(frame, o, y, (255, 255, 0), 1)
            # cv.circle(frame, x, 5, (0, 255, 255), 2)
            # cv.circle(frame, y, 5, (0, 255, 255), 2)
            # cv.circle(frame, o, 5, (0, 255, 255), 2)
            # cv.circle(frame, (0, 100), 10, (0, 255, 255), 3)
            cv.imshow('Correction', frame)
            if cv.waitKey(1) & 0xFF == ord('q'):
                cv.destroyWindow('Correction')
                break
        return po, px, py

    def object_detection(self):
        point_records = []
        nothing_detected_notice = True
        while True:
            ret, frame = self._cam.read()
            virtual_positions = self._darknet.detect(frame)

            if len(virtual_positions) == 0 and nothing_detected_notice is True:
                logging.info("Nothing detected...")
                nothing_detected_notice = False
                continue

            best_p = self._get_single_frame_best_detection(virtual_positions)

            if best_p is not None:
                is_best, point = self._get_best_detection_overall(point_records, best_p)
                if is_best:
                    return point

    def _get_best_detection_overall(self, records, best_p):
        new_record = True
        for p in records:
            if int(p.point.x) == int(best_p.x) and int(p.point.y) == int(best_p.y):
                p.add_count()
                if p.count >= 10:
                    return True, p.point
                new_record = False
        if new_record is True:
            records.append(self.PointRecord(best_p))
        return False, None

    @staticmethod
    def _get_single_frame_best_detection(virtual_positions):
        best_p = VirtualPosition()
        for p in virtual_positions:
            if p.width >= best_p.width and p.height >= best_p.height:
                best_p = p
        if best_p.x <= 10 or best_p.y <= 10:
            best_p = None
        return best_p


class DobotProxy:
    def __init__(self, set_home=True):
        logging.debug("Initializing DobotProxy...")
        self._dobot = Dobot(list_ports.comports()[1].device)
        self._home_cmd_id = None
        if set_home:
            logging.debug('Setting home...')
            self._home_cmd_id = self._dobot.home()

    def wait_for_initialized(self):
        if self._home_cmd_id is not None:
            self._dobot.wait_for_cmd(self._home_cmd_id)
            logging.debug('Resetting done.')

    def move_object(self, x, y, wait=True):
        horizon = 125
        straight = -27

        self._dobot.move_to(x * 10 + straight, y * 10 + horizon, 20)
        self._dobot.suck(True)
        self._dobot.move_to(x * 10 + straight, y * 10 + horizon, -50)

        self._dobot.move_to(x * 10 + straight, y * 10 + horizon, 20)
        self._dobot.move_to(120, -150, -20)
        self._dobot.suck(False)
        cmd_id = self._dobot.move_to(120, 0, 0)
        if wait:
            self._dobot.wait_for_cmd(cmd_id)


class PositioningThread(threading.Thread):

    class Info:
        def __init__(self, obj, real_position):
            self.obj = obj
            self.real_position = real_position

    def __init__(self, name, image_locator, dobot_proxy, lock: threading.Lock):
        threading.Thread.__init__(self)
        self.name = name
        self._image_locator = image_locator
        self._dobot_proxy = dobot_proxy
        self._lock = lock
        self._info = None

    def get_info_copy(self) -> Info:
        self._lock.acquire()
        info_copy = copy.deepcopy(self._info)
        self._lock.release()
        return info_copy

    def run(self) -> None:
        while True:
            obj = self._image_locator.object_detection()

            # 計算真實座標
            x, y = image_locator.convert_real_position(obj)
            real_position = {'x': x, 'y': y}
            logging.debug('Real Position --- [x: ' + str(round(real_position['x'], 2)) + ' cm], [y: ' +
                          str(round(real_position['y'], 2)) + ' cm]')
            info = self.Info(obj, real_position)

            self._lock.acquire()
            self._info = info
            self._lock.release()

            self._dobot_proxy.move_object(real_position['x'], real_position['y'], True)

            self._lock.acquire()
            self._info = None
            self._lock.release()


class CameraProxy:
    def __init__(self, camera, lock: threading.Lock):
        self._camera = camera
        self._lock = lock

    def read(self):
        self._lock.acquire()
        ret, frame = self._camera.read()
        self._lock.release()
        return ret, frame


if __name__ == '__main__':
    logging.basicConfig(level=Config.LOGGING_LEVEL, format=Config.LOGGING_FORMAT)

    logging.info('Application initializing...')

    reset_dobot = input('Do you need to reset dobot(n)?[y/n]:')

    reset_dobot = reset_dobot == "y"

    dobot_proxy = DobotProxy(reset_dobot)

    cam_lock = threading.Lock()
    camera = init_camera()
    camera = CameraProxy(camera, cam_lock)

    image_locator = ImageLocator(camera)

    dobot_proxy.wait_for_initialized()

    logging.info('-----Application start-----|')

    info_lock = threading.Lock()
    positioning = PositioningThread("Positioning Thread", image_locator, dobot_proxy, info_lock)
    view = View.ViewPresenter(camera, positioning)
    positioning.start()
    view.show()

    # view = View.ViewThread("Application View", camera)
    # view.start()

    # while True:
    #     ret, frame = camera.read()
    #     obj.draw(frame)
    #     cv.imshow('Object', frame)
    #     if cv.waitKey(1) & 0xFF == ord('q'):
    #         break
