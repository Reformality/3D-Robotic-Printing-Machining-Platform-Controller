from dorna import Dorna


class Robot:
    def __init__(self):
        self.robot = Dorna()

    def update_firmware(self):
        self.robot.update_firmware()

    def connect(self):
        self.robot.connect()

    def homing(self):
        print("###### START HOMING ######")
        print("Homing j0")
        self.robot.home("j0")
        print("Homing j1")
        self.robot.home("j1")
        print("Homing j2")
        self.robot.home("j2")
        print("Homing j3")
        self.robot.home("j3")
        print("Homing j4")
        self.robot.home("j4")


# robot = Dorna()
# print(robot.port_list())
# robot.update_firmware()
# robot.connect()
# print(robot.homed())
# robot.home("j0")
# robot.home("j1")
# robot.home("j2")
# robot.home("j3")
# robot.home("j4")
#
# robot.terminate()

if __name__ == '__main__':
    arm = Robot()
    arm.connect()
    arm.update_firmware()
    arm.homing()

    arm.robot.terminate()
