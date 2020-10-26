import cv2 as cv

"""
每一個影像辨識偵測到的物品單位
this xy system is as same as numpy.
x axis is bigger when right, y axis is bigger when low
"""


class VirtualPosition:
    def __init__(self):
        self.id = None  # id 是 .names 檔中的名稱而非該名稱的 index
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.confidence = 0

    # 方框加上文字，預設為紅色（0, 0, 255）
    def draw(self, image, color=(0, 0, 255)):
        cv.rectangle(image,
                     (int(self.x - self.width / 2), int(self.y - self.height / 2)),
                     (int(self.x + self.width / 2), int(self.y + self.height / 2)), (255, 0, 0),
                     thickness=2)
        cv.putText(image, str(self.id), (int(self.x), int(self.y)), cv.FONT_HERSHEY_DUPLEX, 1, color)


"""
代表座標系統於影像中的虛擬位置，座標系統為原點，其他物品會被轉為相對於原點的真實位置，而座標本身不會。
origin: VirtualPosition
x: VirtualPosition
y: VirtualPosition
"""


class Coordinate:
    def __init__(self):
        self.origin = None
        self.x = None
        self.y = None

    # 畫出座標，
    def draw(self, image):
        black = (0, 0, 0)
        green = (0, 255, 0)
        blue = (255, 0, 0)
        self.origin.draw(image, black)
        self.x.draw(image, green)
        self.y.draw(image, blue)
        Coordinate._draw_axis(image, self.origin, self.x, black, 4)
        Coordinate._draw_axis(image, self.origin, self.y, black, 4)

    @staticmethod
    def _draw_axis(image, pt1, pt2, color, len_multiple=1):
        vector = (int(pt2.x - pt1.x), int(pt2.y - pt1.y))
        startpoint = (int(pt1.x), int(pt1.y))
        # 延伸軸線
        endpoint = (startpoint[0] + vector[0] * len_multiple, startpoint[1] + vector[1] * len_multiple)
        cv.line(image, startpoint, endpoint, color, 2)
