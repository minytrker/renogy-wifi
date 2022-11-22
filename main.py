import json
import sys
import machine
import time
import gc
from Engine import Engine
from Device import LED_PIN, REMOTE_TIME_URL, WIFI_PASSWORD, WIFI_SSID
from utils import log_error, read_time, sync_time_from_remote

led = machine.Pin(LED_PIN, machine.Pin.OUT)
engine  = Engine()
engine.display.log_event("Initing Modules...")
counter = 0
rover = engine.rover
led.value(1)
engine.wifi.connect(WIFI_SSID, WIFI_PASSWORD)
if engine.wifi.is_connected():
    sync_time_from_remote(engine, REMOTE_TIME_URL)
led.value(0)

try:
    while True:
        time.sleep(2)
        led.value(1)
        display_values = {}
        year, month, date, hour, minute, second = read_time()
        engine.time = "{}:{}{}".format(hour % 12, "{:02d}".format(minute), 'am' if hour < 12 else 'pm')
        page = counter % 10

        if page == 0:
            display_values = { 'label': rover.model().strip(), 'value': '', 'icon': '' }
        elif page == 1:
            display_values = { 'type': 'battery', 'value': f"{rover.battery_voltage()}v", 'icon': 'battery' }
        elif page == 2:
            display_values = { 'type': 'battery', 'value': f"{rover.battery_percentage()}%", 'icon': 'battery' }
        elif page == 3:
            display_values = { 'type': 'solar', 'value': f"{rover.solar_power()}w", 'icon': 'sun' }
        elif page == 4:
            display_values = { 'type': 'solar', 'value': f"{rover.solar_current()}A", 'icon': 'sun' }
        elif page == 5:
            display_values = { 'label': 'Load', 'value': 'On' if rover.load_status() else 'Off', 'icon': 'bulb' }
        elif page == 6:
            display_values = { 'label': 'Load', 'value': f"{rover.load_power()}w", 'icon': 'bulb' }
        elif page == 7:
            wifi = WIFI_SSID if engine.wifi.is_connected() else ('Waiting..' if engine.wifi.connection_attempt == 0 else 'Not connected')
            display_values = { 'label': f"WiFi: {wifi}", 'value': '', 'icon': '' }
        elif page == 8:
            ip = engine.wifi.wlan.ifconfig()[0]
            display_values = { 'label': f"IP: {ip}", 'value': '', 'icon': '' }
        elif page == 9:
            display_values = { 'label': '', 'value': engine.time, 'icon': '' }

        engine.display.display_status(display_values, f"{engine.time}:{second}")
        time.sleep(1)
        led.value(0)
        counter  = counter + 1

        if second >= 57:
            gc.collect()
            counter = 0
            if engine.wifi.is_connected() and year > 2021 and hour > 6 and hour < 19:
                engine.logger.log_pvoutput(f"d={year}{month:02d}{date:02d}&t={hour:02d}:{minute:02d}&v2={rover.solar_power()}")
            if engine.wifi.is_connected() and year > 2021 and hour > 6 and hour < 19 and minute % 5 == 0:
                engine.logger.log_remote(json.dumps({
                    'pv_voltage': rover.solar_voltage(),
                    'pv_current': rover.solar_current(),
                    'battery_voltage': rover.battery_voltage(),
                    'battery_percentage': rover.battery_percentage(),
                    'pv_power': rover.solar_power(),
                    'power_generation_today': rover.power_generation_today()
                }))
            if not engine.wifi.is_connected():
                engine.wifi.reconnect(WIFI_SSID, WIFI_PASSWORD)
            if engine.wifi.is_connected() and year < 2022:
                sync_time_from_remote(engine, REMOTE_TIME_URL)

except KeyboardInterrupt:
    pass
except Exception as err:
    sys.print_exception(err)
    log_error(err)
    engine.display.display_event(f"Error: {str(err)}")
 
engine.cleanup()
