import sys
import re
from machine import ADC, Timer, RTC

utc_regex = re.compile("-|T|:|\.")
temp_sensor = ADC(4)
rtc = RTC()
conversion_factor = 3.3/65536

def save_file(file, data):
    f = open(file, 'w')
    f.write(data)
    f.close()

def log_error(err: Exception):
    f = open('error.log', 'w')
    sys.print_exception(err, f)
    f.close()

def execute_timer(callback, delay):
    Timer().init(mode=Timer.ONE_SHOT, period=int(delay * 1000), callback=lambda t: callback())

# def execute_timer(callback, delay):
#     Timer().init(mode=Timer.PERIODIC, period=int(delay * 1000), callback=lambda t: callback())

def read_temperature():
    reading =  temp_sensor.read_u16() * conversion_factor
    return  "{:.2f}".format(27 - (reading - 0.706)/0.001721)

def sync_time_from_remote(engine, time_url):
    engine.display.log_event('Syncing time from server...')
    remote_time = engine.wifi.fetch_json_data(time_url)
    if (remote_time is None):
        engine.display.log_event('Fetching remote time failed')
        return
    try:
        print (remote_time)
        items = utc_regex.split(remote_time['datetime'])
        day_of_week = int(remote_time['day_of_week'])
        rtc.datetime((int(items[0]), int(items[1]), int(items[2]), day_of_week, int(items[3]), int(items[4]), int(items[5]), 0))
    except Exception as err:
        engine.display.log_event(f"Time sync failed{str(err)}")

def read_time():
    items = rtc.datetime()
    return [int(items[0]), int(items[1]), int(items[2]), int(items[4]), int(items[5]), int(items[6])]
