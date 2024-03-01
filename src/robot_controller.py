import Jetson.GPIO as GPIO, numpy as np
from ADS1x15 import ADS1115
import time

class RobotController:
    """
    A class representing a robot controller.

    Attributes:
        pin (int): The pin number for controlling the robot.
        pwm (PWM): The PWM object for controlling the duty cycle of the pin.
        angle_ratio (float): The ratio between analog value to an angle in radians.
        position_ratio (float): The ratio between analog value to a position in meters.
        loop_delay_left (float): The delay applied after a move to the left.
        loop_delay_right (float): The delay applied aftera move to the right.
        ads (ADS1115): Class for reading from the ADS1115 AD converter.

    Methods:
        __init__(self, pin): Initializes the RobotController object.
        setup_pwm(self): Initializes the PWM output.
        setup_ads1115(self): Initializes the ADS1115.
        update_state(self): Updates the state of the robot.
        read(self): Reads analog values for position and angle.
        calculate_reward(self): Calculates the reward based on current angle.
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

        self.setup_ads1115()
        self.pin = pin
        self.angle_ratio = 9152.8
        self.position_ratio = 65534
        self.loop_delay_left = 0.135
        self.loop_delay_right = 0.008

        self.setup_pwm()
        position, angle = self.read()
        self.state = np.array([angle, 0, position, 0, time.time()])

    def setup_pwm(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 1000)
        self.pwm.start(0)

    def setup_ads1115(self, bus_number=1, address=0x48):
        """
        Initializes ADC converter with 4.096V gain and appropriate
        data rate.
        """
        self.ads = ADS1115(bus_number, address)
        self.ads.setGain(self.ads.PGA_4_096V)
        self.ads.setDataRate(self.ads.DR_ADS111X_860)

    def update_state(self):
        """
        Updates the state of the robot.
        """
        new_cart_position, new_angle = self.read()
        last_time = self.state[4]
        new_time = time.time()
        delta_time = new_time - last_time

        new_angular_velocity = (new_angle - self.state[0]) / delta_time
        new_cart_velocity = (new_cart_position - self.state[2]) / delta_time

        self.state = np.array([
            new_angle, 
            new_angular_velocity, 
            new_cart_position, 
            new_cart_velocity, 
            new_time
        ])

    def read(self):
        """
        Reads analog values from channels A0 and A1 on the ADS1115.

        Returns:
            tuple: The normalized values from A0 and A1 - angle and position, respectively.
        """
        position = self.ads.readADC(0) / self.position_ratio
        angle = self.ads.readADC(1) / self.angle_ratio
        return (position, angle)

    def move(self, direction):
        """
        Moves the robot in the specified direction with a max duty cycle.

        Args:
            direction (int): The direction of movement, either 'left' (0) or 'right' (1).

        Raises:
            ValueError: If an invalid direction is provided.
        """
        if direction == 0:
            self.pwm.ChangeDutyCycle(0)
            time.sleep(self.loop_delay_left)
        elif direction == 1:
            self.pwm.ChangeDutyCycle(100)
            time.sleep(self.loop_delay_right)
        else:
            raise ValueError(f"Invalid direction: {direction}")
        

    def calculate_reward(self):
        """
        Calculate the reward based on the current state.

        Args:
            state (List[float]): Current state of the pendulum [theta, omega, x, x_dot].

        Returns:
            float: Reward value.
        """
        angle, _, _, _, _ = self.state
        target_angle = np.pi

        angle_difference = np.abs(angle - target_angle)
        reward = 1.0 / (1.0 + angle_difference)

        return reward

    def __del__(self):
        """
        Cleans up the GPIO resources when the object is deleted.
        """
        self.pwm.stop()
        self.ads
        GPIO.cleanup()
