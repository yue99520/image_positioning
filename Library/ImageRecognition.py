import logging

from pydarknet import Detector, Image
from Config import CFG_PATH, WEIGHTS_PATH, DATA_PATH, COORD_ORIGIN_ID, COORD_X_ID, COORD_Y_ID
from ImagePositioning import CONFIDENCE_THRESHOLD
from Library.Entity import VirtualPosition, Coordinate


class Darknet:
    def __init__(self):
        logging.debug('Connect Yolov3 darknet.')
        self.net = Detector(bytes(CFG_PATH, encoding="utf-8"),
                            bytes(WEIGHTS_PATH, encoding="utf-8"), 0,
                            bytes(DATA_PATH, encoding="utf-8"))

    def detect(self, image):
        results = self.net.detect(Image(image))
        virtual_positions = []
        for cat, score, bounds in results:
            if score >= CONFIDENCE_THRESHOLD:
                x, y, w, h = bounds
                virtual_position = VirtualPosition()
                virtual_position.id = cat.decode("utf-8") # 注意cat是物品在names檔案中的名稱，並非數字
                virtual_position.x = x
                virtual_position.y = y
                virtual_position.width = w
                virtual_position.height = h
                virtual_position.confidence = score
                virtual_positions.append(virtual_position)
        return virtual_positions


"""
取得影像中座標與物品的虛擬位置
return coord: Coordinate, item: VirtualPosition
"""


def recognize_from_xy(net: Darknet, image):
    virtual_positions = net.detect(image)
    coord = Coordinate()
    highest_conf = 0
    item = None
    for position in virtual_positions:
        pos_id = position.id

        if pos_id is COORD_ORIGIN_ID:
            coord.origin = position
        elif pos_id is COORD_X_ID:
            coord.x = position
        elif pos_id is COORD_Y_ID:
            coord.y = position
        elif position.confidence > highest_conf:
            item = position

    return coord, item


def recognize_from_z(net: Darknet, image, find_id):
    virtual_positions = net.detect(image)
    highest_conf = 0
    item = None
    for position in virtual_positions:
        pos_id = position.id
        if position.confidence > highest_conf and pos_id is find_id:
            item = position
    return item
