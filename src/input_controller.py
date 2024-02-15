from smbus2 import SMBus

class InputController:
    """
    This class represents an input interface for reading analog values from encoders
    on an inverted pendulum system.
    """

    def __init__(self, address, bus_number, config_reg) -> None:
        """
        Initializes an instance of the InputInterface class.

        Parameters:
        - address (int): The I2C address of the device.
        - bus_number (int): The bus number to use for communication.
        - config_reg (int): The configuration register address.

        Returns:
        None
        """
        self.address = address
        self.config_reg = config_reg
        self.bus = SMBus(bus_number)

    def configure_continuous_mode(self, channel):
        """
        Configures the input interface for continuous mode.

        Parameters:
        - channel (str): The channel to configure. Valid values are 'A0' and 'A1'.

        Returns:
        None

        Raises:
        - ValueError: If an invalid channel is provided.
        """
        if channel == 'A0':
            config_data = [0xC4, 0x83]
        elif channel == 'A1':
            config_data = [0xD4, 0x83]
        else:
            raise ValueError("Invalid channel. Choose 'A0' or 'A1'.")
        
        self.bus.write_i2c_block_data(self.address, self.config_reg, config_data)

    def read_conversion_result(self):
        """
        Reads the conversion result from the input interface.

        Returns:
        int: The conversion result.
        """
        data = self.bus.read_i2c_block_data(self.address, 0, 2)
        return (data[0] << 8) | data[1]

    def read_angle_continuous(self):
        """
        Reads the continuous angle from the input interface.

        Returns:
        int: The continuous angle value.
        """
        self.configure_continuous_mode('A1')
        return self.read_conversion_result()

    def read_position_continuous(self):
        """
        Reads the continuous position from the input interface.

        Returns:
        int: The continuous position value.
        """
        self.configure_continuous_mode('A0')
        return self.read_conversion_result()
