import sys
from machine import ADC, Timer, UART

temp_sensor = ADC(4)
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

def deep_get(d, keys):
    if not keys or d is None:
        return d
    return deep_get(d.get(keys[0]), keys[1:])

def read_temperature():
    reading =  temp_sensor.read_u16() * conversion_factor
    return  "{:.2f}".format(27 - (reading - 0.706)/0.001721)
