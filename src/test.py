from robot_controller import RobotController
from input_controller import InputController

def test():
    # rc = RobotController()
    ic = InputController()
    while True:
        print_sensors(ic)

def print_sensors(ic: InputController):
    angle, position = ic.read_angle_and_position()
    print(f'Angle: {angle}\nPosition: {position}\n')

if __name__ == '__main__':
    test()