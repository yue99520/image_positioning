import logging
import Config
from cv2 import cv2 as cv
from Library.ArmControl import convert_arm_coordinate, move
from Library.CameraControl import access_camera_xy, access_camera_z
from Library.Coordinate import find_real_position
from Library.ImageRecognition import recognize_from_xy, Darknet, recognize_from_z
from Library.ItemHigh import calculate_item_high

"""
    系統流程：
    
    取得物品實際位置：
          影像辨識：取得座標虛擬位置
          影像辨識：取得物品虛擬位置與種類
          計算物品真實位置：
                計算物品虛擬座標（多少數量個座標單位）
                轉換物品虛擬座標，取得以公分為單位的真實位置
    取得物品實際高度：
          將真實座標加上Z軸攝影機的固定距離，經過誤差校正，取得實際距離
          轉換物品離攝影機的實際距離，取得物品實際高度
    依照物品實際高度與位置，計算機械手臂如何到達目的地
    操作機械手臂：
          得知物品位置後，將物品吸取
          移動物品至目的地
"""

logging.basicConfig(level=Config.LOGGING_LEVEL, format=Config.LOGGING_FORMAT)
logging.debug('App started.')

z_queue = {'a': 1}

"""
取得物品實際位置
"""
# 存取攝影機
cam_xy = access_camera_xy()
cam_z = access_camera_z()

# XY軸攝影機拍照
ret, frame = cam_xy.read()
image_xy = frame.copy()

# 取得座標位置
# 取得物品位置
net = Darknet()
coord, virtual_position = recognize_from_xy(net, image_xy)

if coord.x is None or coord.y is None or coord.origin is None:
    logging.warning('Can not detect coordinate - ' +
                    'Origin: ' + str(coord.origin is not None) +
                    ', X axis: ' + str(coord.x is not None) +
                    ', Y axis: ' + str(coord.y is not None))
    exit()
elif virtual_position is None:
    logging.warning('Can not detect any items.(XY cam)')
    exit()

logging.debug('Item Detected: ' + virtual_position.id)

# 計算真實座標
x, y = find_real_position(coord, virtual_position)
real_xy = {'x': x, 'y': y}
logging.debug('[Real Position] x: ' + real_xy['x'] + ' cm, y: ' + real_xy['y'] + ' cm.')

"""
取得物品實際高度
"""

# Z軸攝影機拍照
ret, frame = cam_z.read()
image_z = frame.copy()

# 取得物品位置與虛擬高度
virtual_position_from_z = recognize_from_z(net, image_z, virtual_position.id)

if virtual_position is None:
    logging.warning('Can not detect any items.(Z cam)')
    exit()

# 取得真實距離
real_distance = real_xy[Config.CAM_Z_DIRECTION] + Config.CAM_Z_FIXED_DISTANCE

# 用畢氏定理校正物品與Z軸攝影機的距離誤差
pass

# 計算真實高度
real_z = calculate_item_high(real_distance, virtual_position_from_z.height)
logging.debug('[Real Position] z: ' + real_z + ' cm.')

"""
進行移動
"""

# 找出物品相對應的目的地
arm_from = convert_arm_coordinate(coord, real_xy[x], real_xy[y], real_z)

arm_to = Config.DESTINATION.copy()

# 計算目的地堆疊高度
if virtual_position.id in z_queue:
    arm_to['z'] = z_queue.get(virtual_position.id)
    z_queue[virtual_position.id] += arm_from['z']
else:
    arm_to['z'] = arm_from['z']
    z_queue[virtual_position.id] = arm_from['z']

# move
logging.debug('Ready to move item - From x: {fx}, y: {fy}, z: {fz} To x: {tx}, y: {ty}, z:{tz}'
              .format(fx=arm_from['x'], fy=arm_from['y'], fz=arm_from['z'],
                      tx=arm_to['x'], ty=arm_to['y'], tz=arm_to['z']))

# draw every thing
coord.draw(image_xy)
virtual_position.draw(image_xy)
virtual_position_from_z(image_z)
cv.imshow('Cam XY', image_xy)
cv.imshow('Cam Z', image_z)
