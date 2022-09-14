import machine
import time
from umodbus.uModBusSerial import uModBusSerial
from renogy import RenogyRover
from Engine import Engine
from Device import RS232_UART_ID, RS232_SLAVE_ADDR

led = machine.Pin('LED', machine.Pin.OUT)

engine  = Engine()
engine.display_logger.log_event("Initing Module...")
modbus_obj = uModBusSerial(RS232_UART_ID, pins=(machine.Pin(0), machine.Pin(1)))
rover = RenogyRover(modbus_obj, RS232_SLAVE_ADDR)
counter = 0

while True:
    time.sleep(2)
    led.value(1)
    display_values = {}
    page = counter % 6

    if page == 0:
        display_values = {
            'label': rover.model().strip(),
            'value': '',
            'icon': ''
        }
    elif page == 1:
        display_values = {
            'type': 'battery',
            'value': f"{rover.battery_voltage()}v",
            'icon': 'battery'
        }
    elif page == 2:
        display_values = {
            'type': 'battery',
            'value': f"{rover.battery_percentage()}%",
            'icon': 'battery'
        }
    elif page == 3:
        display_values = {
            'type': 'solar',
            'value': f"{rover.solar_power()}w",
            'icon': 'sun'
        }
    elif page == 4:
        display_values = {
            'type': 'solar',
            'value': f"{rover.solar_current()}a",
            'icon': 'sun'
        }
    elif page == 5:
        display_values = {
            'label': 'Load',
            'value': f"{rover.load_power()}w",
            'icon': 'bulb'
        }

    engine.display_logger.display_status(display_values)
    time.sleep(1)
    led.value(0)
    counter = counter + 1
