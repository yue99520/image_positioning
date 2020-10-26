import math

from Config import CM_PER_X_UNIT, CM_PER_Y_UNIT
from Library.Entity import Coordinate


class Equation:
    def __init__(self, a, b):
        self.a = a
        self.b = b


def _axis_equation(pt1, pt2):
    a = (pt2['y'] - pt1['y']) / (pt2['x'] - pt1['x'])
    b = pt1['y'] - a * pt1['x']
    return Equation(round(a, 4), round(b, 4))


def _normal_equation(a, over_pt):
    normal_a = -1 / a
    normal_b = over_pt['y'] - normal_a * over_pt['x']
    return Equation(round(normal_a, 4), round(normal_b, 4))


def _simultaneous_equations(equation1, equation2):
    x = (-equation1.b + equation2.b) / (equation1.a - equation2.a)
    y = equation1.a * x + equation1.b
    return {'x': round(x, 4), 'y': round(y, 4)}


def _pixel_distance(pt1, pt2):
    return math.sqrt((pt1['x'] - pt2['x'])**2 + (pt1['y'] - pt2['y'])**2)


def _real_x_distance(origin, pt_axis, virtual_position):
    line_axis = _axis_equation(origin, pt_axis)
    line_normal_axis = _normal_equation(line_axis.a, virtual_position)

    # 法線與軸線交點
    point_axis_cross_normal = _simultaneous_equations(line_axis, line_normal_axis)

    pixel_dis = _pixel_distance(virtual_position, point_axis_cross_normal)
    pixels_per_unit = _pixel_distance(origin, pt_axis)
    real_dis = pixel_dis / pixels_per_unit
    real_dis = real_dis * CM_PER_X_UNIT
    return real_dis


def _real_y_distance(origin, pt_axis, virtual_position):
    line_axis = _axis_equation(origin, pt_axis)
    line_normal_axis = _normal_equation(line_axis.a, virtual_position)

    # 法線與軸線交點
    point_axis_cross_normal = _simultaneous_equations(line_axis, line_normal_axis)

    pixel_dis = _pixel_distance(virtual_position, point_axis_cross_normal)
    pixels_per_unit = _pixel_distance(origin, pt_axis)
    real_dis = pixel_dis / pixels_per_unit
    real_dis = real_dis * CM_PER_Y_UNIT
    return real_dis


"""
依據座標系統計算物品的真實座標
coord: 座標系統物件
virtualPosition: 物品虛擬位置
return x, y 單位公分
"""


def find_real_position(coord: Coordinate, virtual_position):
    origin = {'x': coord.origin.x, 'y': coord.origin.y}
    ptx = {'x': coord.x.x, 'y': coord.x.y}
    pty = {'x': coord.y.x, 'y': coord.y.y}
    pto = {'x': virtual_position.x, 'y': virtual_position.y}

    obj_real_x = _real_x_distance(origin, ptx, pto)
    obj_real_y = _real_y_distance(origin, pty, pto)

    return obj_real_x, obj_real_y
