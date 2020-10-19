from pydobot import Dobot

from Library import Coordinate
from serial.tools import list_ports
from pydobot import *
#
port = list_ports.comports()[0].device

"""
轉換座標 cm to arm coordinate
return 手臂座標{x, y, z}
"""


def convert_arm_coordinate(x, y, z):
    pass


"""
移動物品到目的地
"""


def move(from_x, from_y, from_z, to_x, to_y, to_z):
    convert_arm_coordinate(from_x,from_y,from_z)
    bot = Dobot(port=port, verbose=True)
    bot.move_to(finx,finy,finz)
    bot._set_end_effector_suction_cup(True)
    bot.move_to(finx, finy, 60)
    convert_arm_coordinate(to_x, to_y, to_z)
    bot.move_to(finx, finy, 60)
    bot.move_to(finx,finy,finz)
    bot.suck(False)

