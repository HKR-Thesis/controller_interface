from robot_controller import RobotController

def run():
    rc = RobotController()

    while True:
        rc.move(0)
        rc.update_state()
        rc.move(1)
        rc.update_state()

if __name__ == '__main__':
    run()