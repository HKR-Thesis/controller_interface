from ADS1x15 import ADS1115

class InputController:
    """
    This class represents an input interface for reading analog values from encoders
    on an inverted pendulum system, using the ADS1115 ADC.
    """

    def __init__(self, bus_number=1, address=0x48) -> None:
        """
        Initializes an instance of the InputController class.

        Parameters:
        - bus_number (int): The I2C bus number to use for communication.
        - address (int): The I2C address of the ADS1115 device.
        """
        self.ads = ADS1115(bus_number, address)
        self.ads.setGain(self.ads.PGA_4_096V)
        self.ads.setDataRate(self.ads.DR_ADS111X_860)

    def read_angle_and_position(self):
        """
        Reads analog values from channels A0 and A1 on the ADS1115.

        Returns:
        tuple: The analog values from A0 and A1 - angle and position, respectively.
        """
        position_value = self.ads.readADC(0)
        angle_value = self.ads.readADC(1)
        return position_value, angle_value