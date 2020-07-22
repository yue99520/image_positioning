
"""
每一個影像辨識偵測到的物品單位
"""


class VirtualPosition:
    def __init__(self):
        self.id = None
        self.x = None
        self.y = None
        self.width = None
        self.height = None
        self.confidence = None


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
