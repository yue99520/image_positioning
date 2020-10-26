import logging

import cv2 as cv
"""
APP
"""
LOGGING_LEVEL = logging.DEBUG
LOGGING_FORMAT = '%(asctime)s | %(levelname)10s | %(filename)10s | %(message)s'

"""
    攝影機
"""

# XY軸俯視攝影機
# port id
CAM_XY_PORT = 0

# Z軸平視攝影機
# port id
CAM_Z_PORT = 5

# Z軸攝影機焦距
# 單位：pixels
CAM_Z_FOCAL_LENGTH = 570

# Z軸攝影機拍攝方向
# 若方向平行於Y軸則填'y'
CAM_Z_DIRECTION = 'y'

# Z軸攝影機與座標系統之固定距離
# 單位：cm
CAM_Z_FIXED_DISTANCE = 0

"""
    影像辨識
"""


# 信心閥值
CONFIDENT_THRESHOLD = 0.7

# 影像辨識座標ID
COORD_ORIGIN_ID = "origin"
COORD_X_ID = "x_axis"
COORD_Y_ID = "y_axis"

CFG_PATH = "../darknet/test/cfg/circle/circle.cfg"
WEIGHTS_PATH = "../darknet/backup/circle/circle_10000.weights"
DATA_PATH = "../darknet/test/cfg/circle/obj.data"

CFG_COORDINATE_ORIGIN_PATH = "../darknet/test/cfg/red_circle.cfg"
DATA_COORDINATE_ORIGIN_PATH = "../darknet/test/cfg/obj.data"
WEIGHTS_COORDINATE_ORIGIN_PATH = "../darknet/backup/blue_circle_70000.weights"

CFG_COORDINATE_X_PATH = "../darknet/test/cfg/red_circle.cfg"
DATA_COORDINATE_X_PATH = "../darknet/test/cfg/obj.data"
WEIGHTS_COORDINATE_X_PATH = "../darknet/backup/blue_circle_70000.weights"

CFG_COORDINATE_Y_PATH = "../darknet/test/cfg/red_circle.cfg"
DATA_COORDINATE_Y_PATH = "../darknet/test/cfg/obj.data"
WEIGHTS_COORDINATE_Y_PATH = "../darknet/backup/blue_circle_70000.weights"

CFG_OBJECT_PATH = "../darknet/test/cfg/candybox/yolov3-tiny.cfg"
DATA_OBJECT_PATH = "../darknet/test/cfg/candybox/candybox.data"
WEIGHTS_OBJECT_PATH = "../darknet/test/cfg/candybox/yolov3-tiny_final.weights"

"""
    物件與比例尺
"""

# XY平面真實長度cm：虛擬長度pixel
LENGTH_SCALE = None

# XY平面使用的單位比例尺
CM_PER_X_UNIT = 20
CM_PER_Y_UNIT = 20

"""
    機械手臂
"""

# 機械手臂原點於座標軸中位置
# {x, y}
ARM_POSITION = {'x': 0, 'y': 0}

# 物品各自的目的地
# {id: {x, y}, ...}
DESTINATION = {0: {0, 0}}

# COORD_O = (70, 46)
# COORD_X = (561, 30)
# COORD_Y = (90, 375)

COORD_O = (300, 40)
COORD_X = (628, 41)
COORD_Y = (299, 368)
