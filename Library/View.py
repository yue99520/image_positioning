import threading
import logging
import Config
from Library.Entity import Coordinate
from ImagePositioning import PositioningThread
from Library.Entity import VirtualPosition
from cv2 import cv2 as cv


class ViewItem:
    def __init__(self, name=""):
        self.name = name

    def get_name(self):
        return self.name

    def draw(self, frame):
        pass


class Rectangle(ViewItem):
    def __init__(self, virtual_position: VirtualPosition, name):
        super().__init__(name)
        self.pt1 = (int(virtual_position.x - virtual_position.width / 2), int(virtual_position.y - virtual_position.height / 2))
        self.pt2 = (int(virtual_position.x + virtual_position.width / 2), int(virtual_position.y + virtual_position.height / 2))

    def draw(self, frame):
        cv.rectangle(frame, self.pt1, self.pt2, (0, 0, 255))
        # cv.addText(frame, self.name, self.pt2, cv.FONT_HERSHEY_DUPLEX, color=(0, 255, 255))
        cv.putText(frame, self.name, self.pt2, cv.FONT_HERSHEY_DUPLEX, 1, color=(0, 255, 255))


class Point(ViewItem):
    def __init__(self, x, y, name):
        super().__init__(name)
        self.x = x
        self.y = y

    def draw(self, frame):
        cv.circle(frame, (int(self.x), int(self.y)), 1, (0, 0, 255))
        # cv.addText(frame, self.name, (int(self.x + 5), int(self.y + 5)), cv.FONT_HERSHEY_DUPLEX, color=(0, 255, 255))
        cv.putText(frame, self.name, (int(self.x + 5), int(self.y + 5)), cv.FONT_HERSHEY_DUPLEX, 1, color=(0, 255, 255))


class ViewPresenter:
    def __init__(self, camera, coord: Coordinate, info_source: PositioningThread):
        self._camera = camera
        self._info_source = info_source
        self._view_items = []
        self._exit = False
        self._window_name = 'Image Positioning'
        self.x = coord.x
        self.y = coord.y
        self.o = coord.origin

    def show(self):
        logging.debug("Start view thread")
        while True:
            ret, frame = self._camera.read()
            info = self._info_source.get_info_copy()

            self.draw_coordinate(frame)

            if info is not None:
                Point(int(info.obj.x), int(info.obj.y), "Target Center").draw(frame)
                Rectangle(info.obj, "").draw(frame)

            cv.imshow(self._window_name, frame)
            cv.waitKey(1)
            if self._exit is True:
                cv.destroyWindow(self._window_name)
                break
        logging.info("View stop")

    def draw_coordinate(self, frame):
        cv.line(frame, self.o.to_tuple(), self.x.to_tuple(), (255, 255, 0), 3)
        cv.line(frame, self.o.to_tuple(), self.y.to_tuple(), (255, 255, 0), 3)
        cv.circle(frame, self.x.to_tuple(), 5, (0, 255, 255), 2)
        cv.circle(frame, self.y.to_tuple(), 5, (0, 255, 255), 2)
        cv.circle(frame, self.o.to_tuple(), 5, (0, 255, 255), 2)

    def stop(self):
        self._exit = True
