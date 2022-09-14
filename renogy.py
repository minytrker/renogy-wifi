"""
Driver for the Renogy Rover Solar Controller using the Modbus RTU protocol
"""

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

class RenogyRover():
    """
    Communicates using the Modbus RTU protocol (via provided USB<->RS232 cable)
    """

    def __init__(self, uModBusSerial, slave_addr):
        self.uModBusSerial = uModBusSerial
        self.slave_addr = slave_addr

    def read_register(self, starting_address, numberOfRegisters = 1):
        values = self.uModBusSerial.read_holding_registers(self.slave_addr, starting_address, numberOfRegisters, True)
        return values
        
    def read_string(self, starting_address, numberOfRegisters = 1):
        values = self.uModBusSerial.read_holding_registers(self.slave_addr, starting_address, numberOfRegisters, True)
        return values

    def model(self):
        """
        Read the controller's model information
        """
        return self.read_string(12, numberOfRegisters=8)

    def system_voltage_current(self):
        """
        Read the controler's system voltage and current
        Returns a tuple of (voltage, current)
        """
        register = self.read_register(10)
        amps = register & 0x00ff
        voltage = register >> 8
        return (voltage, amps)

    def battery_percentage(self):
        """
        Read the battery percentage
        """
        return self.read_register(256) & 0x00ff

    def battery_voltage(self):
        """
        Read the battery voltage
        """
        return self.read_register(257, numberOfRegisters=1) * 0.1

    def battery_temperature(self):
        """
        Read the battery surface temperature
        """
        register = self.read_register(259)
        battery_temp_bits = register & 0x00ff
        temp_value = battery_temp_bits & 0x0ff
        sign = battery_temp_bits >> 7
        battery_temp = -(temp_value - 128) if sign == 1 else temp_value
        return battery_temp

    def controller_temperature(self):
        """
        Read the controller temperature
        """
        register = self.read_register(259)
        controller_temp_bits = register >> 8
        temp_value = controller_temp_bits & 0x0ff
        sign = controller_temp_bits >> 7
        controller_temp = -(temp_value - 128) if sign == 1 else temp_value
        return controller_temp

    def load_voltage(self):
        """
        Read load voltage
        """
        return self.read_register(260, numberOfRegisters=1) * 0.1

    def load_current(self):
        """
        Read load current
        """
        return self.read_register(261, numberOfRegisters=1) * 0.01

    def load_power(self):
        """
        Read load power
        """
        return self.read_register(262)

    def solar_voltage(self):
        """
        Read solar voltage
        """
        return self.read_register(263, numberOfRegisters=1) * 0.1

    def solar_current(self):
        """
        Read solar current
        """
        return self.read_register(264, numberOfRegisters=1) * 0.01

    def solar_power(self):
        """
        Read solar power
        """
        return self.read_register(265)

    def charging_amp_hours_today(self):
        """
        Read charging amp hours for the current day
        """
        return self.read_register(273)

    def discharging_amp_hours_today(self):
        """
        Read discharging amp hours for the current day
        """
        return self.read_register(274)

    def power_generation_today(self):
        return self.read_register(275)

    def charging_status(self):
        return self.read_register(288) & 0x00ff

    def charging_status_label(self):
        return CHARGING_STATE.get(self.charging_status())

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