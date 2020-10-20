import threading
import logging
from Library.Entity import VirtualPosition
from cv2 import cv2 as cv


view_exit = False
view_items = []


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
        self.pt1 = (virtual_position.x - virtual_position.height / 2, virtual_position.y - virtual_position.width / 2)
        self.pt2 = (virtual_position.x + virtual_position.height / 2, virtual_position.y + virtual_position.width / 2)

    def draw(self, frame):
        cv.rectangle(frame, self.pt1, self.pt2, (0, 0, 255))
        cv.addText(frame, self.name, self.pt2, cv.FONT_HERSHEY_DUPLEX, (0, 255, 255))


class Point(ViewItem):
    def __init__(self, x, y, name):
        super().__init__(name)
        self.x = x
        self.y = y

    def draw(self, frame):
        cv.circle(frame, (x, y), 1, (0, 0, 255))
        cv.addText(frame, self.name, (x + 5, y + 5), cv.FONT_HERSHEY_DUPLEX, (0, 255, 255))


class ViewThread(threading.Thread):
    def __init__(self, name, camera):
        threading.Thread.__init__(self)
        self.name = name
        self.camera = camera

    def run(self) -> None:
        logging.debug("Start view thread")
        while True:
            ret, frame = self.camera.read()

            for item in view_items:
                if type(item) is ViewItem:
                    item.draw(frame)

            cv.imshow('Object', frame)
            if view_exit is True:
                logging.info("View stop")
                break
