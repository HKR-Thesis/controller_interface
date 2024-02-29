import Jetson.GPIO as GPIO

class RobotController:
    """
    A class representing a robot controller.

    Attributes:
        pin (int): The pin number for controlling the robot.
        pwm (PWM): The PWM object for controlling the duty cycle of the pin.

    Methods:
        __init__(self, pin): Initializes the RobotController object.
        move(self, direction): Moves the robot in the specified direction with max duty cycle.
        __del__(self): Cleans up the GPIO resources when the object is deleted.
    """

    def __init__(self, pin=32):
        """
        Initializes the RobotController object with a specified pin.

        Args:
            pin (int): The pin number for controlling the robot.
        """
        if pin not in [33, 32]:
            raise ValueError("Invalid pin number. Only pin numbers 33 and 32 are accepted.")
        self.pin = pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 1000)
        self.pwm.start(0)

    def move(self, direction):
        """
        Moves the robot in the specified direction with a max duty cycle.

        Args:
            direction (int): The direction of movement, either 'left' (0) or 'right' (1).

        Raises:
            ValueError: If an invalid direction is provided.
        """
        if direction == "left":
            self.pwm.ChangeDutyCycle(0)
        elif direction == "right":
            self.pwm.ChangeDutyCycle(100)
        else:
            raise ValueError(f"Invalid direction: {direction}")

    def __del__(self):
        """
        Cleans up the GPIO resources when the object is deleted.
        """
        self.pwm.stop()
        GPIO.cleanup()
