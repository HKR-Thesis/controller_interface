from robot_controller import RobotController
from input_controller import InputController
from scipy.integrate import solve_ivp
import numpy as np
import time

ANGLE_RATIO = 9152.8
POSITION_RATIO = 65534

def test():
    rc = RobotController(32)
    ic = InputController()
    position, angle = ic.read_angle_and_position()
    current_time = time.time()
    current_state = [angle/ANGLE_RATIO, 0, position/POSITION_RATIO, 0, current_time]

    while True:
        rc.move(0)
        current_state = f(ic, current_state)
        time.sleep(0.105)
        rc.move(1)
        current_state = f(ic, current_state)
        time.sleep(0.008)

def quotient(param_1, param_2, time_1, time_2):
    return (param_2 - param_1)/(time_2 - time_1)

def f(ic: InputController, state):
    x, theta = ic.read_angle_and_position()
    x = x/POSITION_RATIO
    theta = theta/ANGLE_RATIO
    new_time = time.time()

    theta_dot = quotient(theta, state[0], new_time, state[4])
    x_dot = quotient(x, state[2], new_time, state[4])
    print(f'Angle: {theta}\nCart Position: {x}\nAngular velocity: {theta_dot}\nCart velocity: {x_dot}')
    return [theta, theta_dot, x, x_dot, new_time]

if __name__ == '__main__':
    test()