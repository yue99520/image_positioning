from pydobot import Dobot

from Library import Coordinate
from serial.tools import list_ports
from pydobot import *
#
port = list_ports.comports()[0].device

"""
轉換座標
return 手臂座標{x, y, z}
"""
finx,finy,finz = 0


def convert_arm_coordinate(coord: Coordinate, x, y, z):
    global finx,finy,finz
    finx = 300-(y*10)
    finy = (x*10)-180
    finz = (z-10)-60


"""
移動物品到目的地
"""


def move(from_x, from_y, from_z, to_x, to_y, to_z):
    convert_arm_coordinate(from_x,from_y,from_z)
    bot = Dobot(port=port, verbose=True)
    bot.move_to(finx,finy,finz)
    convert_arm_coordinate(to_x, to_y, to_z)
    bot.move_to(finx,finy,finz)

