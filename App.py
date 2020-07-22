from Config import CAM_Z_DIRECTION, CAM_Z_FIXED_DISTANCE, DESTINATION
from Library.ArmControl import convert_arm_coordinate, move
from Library.CameraControl import access_camera_xy, access_camera_z
from Library.Coordinate import find_real_position
from Library.Entity import Coordinate
from Library.ImageRecognition import recognize_coordinate, recognize_item
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

z_queue = {'a': 1}

"""
取得物品實際位置
"""
# 存取攝影機
cam_xy = access_camera_xy()
cam_z = access_camera_z()

# XY軸攝影機拍照
ret, frame = cam_xy.read()
image = frame.copy()

# 取得座標位置
coord = Coordinate()
coord.origin, coord.x, coord.y = recognize_coordinate(image)

# 取得物品位置
virtual_position = recognize_item(image)

# 計算真實座標
x, y = find_real_position(coord, virtual_position)
real_xy = {'x': x, 'y': y}

"""
取得物品實際高度
"""

# Z軸攝影機拍照
ret, frame = cam_z.read()
image = frame.copy()

# 取得物品位置與虛擬高度
virtual_position_from_z = recognize_item(image)

# 取得真實距離
distance = real_xy[CAM_Z_DIRECTION] + CAM_Z_FIXED_DISTANCE

# 用畢氏定理校正物品與Z軸攝影機的距離誤差
pass

# 計算真實高度
real_z = calculate_item_high(distance, virtual_position_from_z.height)

# 找出物品相對應的目的地
arm_from = convert_arm_coordinate(coord, real_xy[x], real_xy[y], real_z)

arm_to = DESTINATION.copy()

# 計算目的地堆疊高度
if virtual_position.id in z_queue:
    arm_to['z'] = z_queue.get(virtual_position.id)
    z_queue[virtual_position.id] += arm_from['z']
else:
    arm_to['z'] = arm_from['z']
    z_queue[virtual_position.id] = arm_from['z']

# move
# move(arm_from['x'], arm_from['y'], arm_from['z'], arm_to['x'], arm_to['y'], arm_to['z'])
print('Result \n From x: {fx}, y: {fy}, z: {fz} \n To x: {tx}, y: {ty}, z:{tz}'
      .format(fx=arm_from['x'], fy=arm_from['y'], fz=arm_from['z'],
              tx=arm_to['x'], ty=arm_to['y'], tz=arm_to['z']))

# 下一個循環
pass
