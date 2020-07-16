# from DobotAdapter.CustomDobot import CustomDobot
from serial.tools import list_ports
from pydobot import *
import TerminalColor

#
port = list_ports.comports()[0].device
# custom_dobot = CustomDobot(port)
# # custom_dobot.relocate()
# custom_dobot.move_and_suck(150,60,-57,100,60,80)


def our_home():
    bot.move_to(206, 0, 134)


bot = Dobot(port=port, verbose=True)
bot.move_to(156,0,134)
bot.home()
bot.speed(10)
bot.move_to(156,0,134)
bot.move_to(156,0,-45,)
bot._set_end_effector_suction_cup(True)
bot.move_to(156,0,134)
bot.move_to(156,140,134)
bot.move_to(156,140,-45)
bot.suck(False)
bot.move_to(156,0,134)
bot.move_to(156,140,134)
bot.move_to(156,140,-45)
bot._set_end_effector_suction_cup(True)
bot.move_to(156,140,134)
bot.move_to(156,-140,134)
bot.move_to(156,-140,-45)
bot.suck(False)
our_home()



# bot.suck(True)

