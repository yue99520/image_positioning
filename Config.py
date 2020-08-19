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
CAM_XY_PORT = 1

# Z軸平視攝影機
# port id
CAM_Z_PORT = 1

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

# PATH
CFG_PATH = "./Yolov3TestModel/cfg/yolov3.cfg"
WEIGHTS_PATH = "./Yolov3TestModel/weights/yolov3.weights"
DATA_PATH = "./Yolov3TestModel/cfg/coco.data"

"""
    物件與比例尺
"""

# XY平面真實長度cm：虛擬長度pixel
LENGTH_SCALE = None

# XY平面使用的單位比例尺
CM_PER_UNIT = 1

"""
    機械手臂
"""

# 機械手臂原點於座標軸中位置
# {x, y}
ARM_POSITION = {'x': 0, 'y': 0}

# 物品各自的目的地
# {id: {x, y}, ...}
DESTINATION = {0: {0, 0}}
