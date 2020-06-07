from pydobot import Dobot
import TerminalColor


class CustomDobot:

    def __init__(self, port):
        self.device = Dobot(port=port, verbose=True)
        self.home_x = 200
        self.home_y = 0
        self.home_z = 135

    def speed(self, speed: float):
        self.device.speed(speed)

    def set_home(self, x: float, y: float, z: float):
        self.home_x = x
        self.home_y = y
        self.home_z = z

    def relocate(self):
        self.device.home()
        self._move_home()

    def move_and_suck(self, from_x: float, from_y: float, from_z: float, to_x: float, to_y: float, to_z: float):

        self._move_home()

        (now_x, now_y, now_z, now_r, now_j1, now_j2, now_j3, now_j4) = self.device.pose()
        # move to object location
        self.device.move_to(from_x, from_y, now_z)
        self.device.move_to(from_x, from_y, from_z)

        # suck object
        self.device.suck(True)

        # move to target location
        self.device.move_to(now_x, now_y, self.home_z)
        self.device.move_to(to_x, to_y, self.home_z)
        self.device.move_to(to_x, to_y, to_z)

        self.device.suck(False)

    def move_to(self, x=None, y=None, z=None):
        if x is None:
            x = self.pose()[0]
        if y is None:
            y = self.pose()[1]
        if z is None:
            z = self.pose()[2]

        self.device.move_to(x, y, z)
        self.show_position()

    def _move_home(self):
        (now_x, now_y, now_z, now_r, now_j1, now_j2, now_j3, now_j4) = self.device.pose()
        self.device.move_to(now_x, now_y, self.home_z)
        self.device.move_to(self.home_x, self.home_y, self.home_z)

    def suck(self, suck):
        self.suck(suck)

    def pose(self):
        return self.device.pose()

    def show_position(self):
        (x, y, z, r, j1, j2, j3, j4) = self.device.pose()
        print()
        print(TerminalColor.Green + "CUSTOM_DOBOT at position:")
        print(TerminalColor.Green + 'x:{', x, '}\ny:{', y, '}\nz:{', z, '}')
        print(TerminalColor.ResetAll)

    def close(self):
        self.device.close()