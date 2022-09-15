import sys
import machine
import time
import gc
from umodbus.uModBusSerial import uModBusSerial
from renogy import RenogyRover
from Engine import Engine
from Device import REMOTE_TIME_URL, RS232_UART_ID, RS232_SLAVE_ADDR
from utils import execute_timer, log_error, read_json_file, read_time, sync_time_from_remote

led = machine.Pin('LED', machine.Pin.OUT)

engine  = Engine()
engine.display.log_event("Initing Modules...")
modbus_obj = uModBusSerial(RS232_UART_ID, pins=(machine.Pin(0), machine.Pin(1)))
rover = RenogyRover(modbus_obj, RS232_SLAVE_ADDR)
engine.secrets = secrets = read_json_file('secrets.json')
wifi_status = engine.wifi.connect(secrets['wifi_ssid'], secrets['wifi_password'])
sync_time_from_remote(engine, REMOTE_TIME_URL)
counter = 0

try:
    while True:
        time.sleep(2)
        led.value(1)
        display_values = {}
        year, month, date, hour, minute, second = read_time()
        engine.time = "{}:{}{}".format(hour % 12, "{:02d}".format(minute), 'am' if hour < 12 else 'pm')
        page = counter % 7

        if page == 0:
            display_values = { 'label': rover.model().strip(), 'value': '', 'icon': '' }
        elif page == 1:
            display_values = { 'type': 'battery', 'value': f"{rover.battery_voltage()}v", 'icon': 'battery' }
        elif page == 2:
            display_values = { 'type': 'battery', 'value': f"{rover.battery_percentage()}%", 'icon': 'battery' }
        elif page == 3:
            display_values = { 'type': 'solar', 'value': f"{rover.solar_power()}w", 'icon': 'sun' }
        elif page == 4:
            display_values = { 'type': 'solar', 'value': f"{rover.solar_current()}a", 'icon': 'sun' }
        elif page == 5:
            display_values = { 'label': 'Load', 'value': f"{rover.load_power()}w", 'icon': 'bulb' }
        elif page == 6:
            wifi = secrets['wifi_ssid'] if engine.wifi.is_connected() else 'Not connected'
            display_values = { 'label': f"WiFi: {wifi}", 'value': '', 'icon': '' }

        engine.display.display_status(display_values, f"{engine.time}:{second}")
        time.sleep(1)
        led.value(0)
        counter  = counter + 1

        if second >= 57:
            gc.collect()
            engine.logger.log_pvoutput(f"d={year}{month:02d}{date:02d}&t={hour:02d}:{minute:02d}&v2={rover.solar_power()}")
            counter = 0
            
except Exception as err:
    execute_timer(machine.reset, 20)
    sys.print_exception(err)
    log_error(err)
    engine.display.display_event(f"Error: {str(err)}")
finally:
    execute_timer(engine.cleanup, 18)
    execute_timer(machine.reset, 20)