from robot_controller import RobotController
from input_controller import InputController
import time

def test():
    ic = InputController()

    while True:
        start = time.time()
        print_sensors(ic)
        end = time.time()
        print(f"{end - start}")

def print_sensors(ic: InputController):
    position, angle = ic.read_angle_and_position()
    print(f'Angle: {angle}\nPosition: {position}\n')

if __name__ == '__main__':
    test()

# difference 0.009