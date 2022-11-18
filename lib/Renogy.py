"""
Driver for the Renogy Rover Solar Controller using the Modbus RTU protocol
"""
from time import sleep
import machine
from umodbus.uModBusFunctions import bytes_to_int, bytes_to_string
from umodbus.uModBusSerial import uModBusSerial


BATTERY_TYPE = {
    1: 'open',
    2: 'sealed',
    3: 'gel',
    4: 'lithium',
    5: 'custom'
}

CHARGING_STATE = {
    0: 'deactivated',
    1: 'activated',
    2: 'mppt',
    3: 'equalizing',
    4: 'boost',
    5: 'floating',
    6: 'current limiting'
}

DATA_TYPE = {
    'INT': 0,
    'INT_HIGHER': 1,
    'INT_LOWER': 2,
    'STRING': 3
}

class RenogyRover():
    """
    Communicates using the Modbus RTU protocol (need RS232 chip)
    """

    def __init__(self, slave_addr, uart_id, uart_tx, uart_rx):
        self.uModBusSerial = uModBusSerial(uart_id, pins=(machine.Pin(uart_tx), machine.Pin(uart_rx)))
        self.slave_addr = slave_addr
        self.device_busy = False

    def read_register(self, starting_address, number_of_registers = 1, type = DATA_TYPE['INT']):
        if (self.device_busy): sleep(0.2)
        self.device_busy = True
        bytes = self.uModBusSerial.read_holding_registers(self.slave_addr, starting_address, number_of_registers, True)
        value = None
        if type == DATA_TYPE['INT']:
            value = bytes_to_int(bytes)
        elif type == DATA_TYPE['INT_HIGHER']:
            value = bytes_to_int(bytes, 0, 1)
        elif type == DATA_TYPE['INT_LOWER']:
            value = bytes_to_int(bytes, 1, 1)
        elif type == DATA_TYPE['STRING']:
            value = bytes_to_string(bytes)
        self.device_busy = False
        return value

    def write_register(self, address, value):
        if (self.device_busy): sleep(0.2)
        self.device_busy = True
        values = self.uModBusSerial.write_single_register(self.slave_addr, address, value, False)
        self.device_busy = False
        return values
 
    def model(self):
        """ Read the controller's model information """
        return self.read_register(12, number_of_registers=8, type = DATA_TYPE['STRING'])

    def system_voltage_current(self):
        """
        Read the controler's system voltage and current
        Returns a tuple of (voltage, current)
        """
        amps = self.read_register(10, DATA_TYPE['INT_LOWER'])
        voltage = amps >> 8
        return (voltage, amps)

    def battery_percentage(self):
        return self.read_register(256, DATA_TYPE['INT_LOWER'])

    def battery_voltage(self):
        return self.read_register(257, number_of_registers=1) * 0.1

    def battery_temperature(self):
        """ Read the battery surface temperature """
        register = self.read_register(259)
        battery_temp_bits = register & 0x00ff
        temp_value = battery_temp_bits & 0x0ff
        sign = battery_temp_bits >> 7
        battery_temp = -(temp_value - 128) if sign == 1 else temp_value
        return battery_temp

    def controller_temperature(self):
        """ Read the controller temperature """
        register = self.read_register(259)
        controller_temp_bits = register >> 8
        temp_value = controller_temp_bits & 0x0ff
        sign = controller_temp_bits >> 7
        controller_temp = -(temp_value - 128) if sign == 1 else temp_value
        return controller_temp

    def load_voltage(self):
        return self.read_register(260, number_of_registers=1) * 0.1

    def load_current(self):
        return self.read_register(261, number_of_registers=1) * 0.01

    def load_power(self):
        return self.read_register(262)

    def solar_voltage(self):
        return self.read_register(263, number_of_registers=1) * 0.1

    def solar_current(self):
        return self.read_register(264, number_of_registers=1) * 0.01

    def solar_power(self):
        return self.read_register(265)

    def charging_amp_hours_today(self):
        return self.read_register(273)

    def discharging_amp_hours_today(self):
        return self.read_register(274)

    def power_generation_today(self):
        return self.read_register(275)

    def charging_status(self):
        return self.read_register(288, DATA_TYPE['INT_LOWER'])

    def charging_status_label(self):
        return CHARGING_STATE.get(self.charging_status() )

    def battery_capacity(self):
        return self.read_register(57346)

    def voltage_setting(self):
        register = self.read_register(57347)
        setting = register >> 8
        recognized_voltage = register & 0x00ff
        return (setting, recognized_voltage)

    def battery_type(self):
        register = self.read_register(57348)
        return BATTERY_TYPE.get(register)

    def load_status(self):
        return  self.read_register(288, 1, DATA_TYPE['INT_HIGHER']) >> 7

    def load_on(self):
        return self.write_register(266, 1)

    def load_off(self):
        return self.write_register(266, 0)

    def get_info(self):
        print('Model: ', self.model())
        print('Battery %: ', self.battery_percentage())
        print('Battery Type: ', self.battery_type())
        print('Battery Capacity: ', self.battery_capacity())
        print('Battery Voltage: ', self.battery_voltage())
        battery_temp = self.battery_temperature()
        print('Battery Temperature: ', battery_temp, battery_temp * 1.8 + 32)
        controller_temp = self.controller_temperature()
        print('Controller Temperature: ', controller_temp, controller_temp * 1.8 + 32)
        print('Load Status: ', self.load_status())
        print('Load Voltage: ', self.load_voltage())
        print('Load Current: ', self.load_current())
        print('Load Power: ', self.load_power())
        print('Charging Status: ', self.charging_status_label())
        print('Solar Voltage: ', self.solar_voltage())
        print('Solar Current: ', self.solar_current())
        print('Solar Power: ', self.solar_power())
        print('Power Generated Today (kilowatt hours): ', self.power_generation_today())
        print('Charging Amp/Hours Today: ', self.charging_amp_hours_today())
        print('Discharging Amp/Hours Today: ', self.discharging_amp_hours_today())
