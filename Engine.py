from Device import RS232_SLAVE_ADDR, RS232_UART_ID, RS232_UART_RX, RS232_UART_TX
from lib.Display import Display
from lib.WiFi import WiFi
from lib.Logger import Logger
from lib.Renogy import RenogyRover

class Engine():
    def __init__(self):
        print("Engine init")
        self.display = Display(self) # DisplayDummy()
        self.wifi = WiFi(self) # WiFiDummy(self) 
        self.logger = Logger(self)
        self.rover = RenogyRover(RS232_SLAVE_ADDR, RS232_UART_ID, RS232_UART_TX, RS232_UART_RX) # RenogyDummy() #  

    def cleanup(self):
        self.display.poweroff()

class WiFiDummy(WiFi):
    # def fetch_json_data(self, url): print(url)
    # def get_request(self, url): print(url)
    def post_request(self, url, json = None, data = None, headers = {}): print(url)

class RenogyDummy():
    def model(self): return "RNG-WANDERER"
    def battery_percentage(self): return 100
    def battery_voltage(self): return 13.2
    def controller_temperature(self): return 32.2
    def load_voltage(self): return 13.2
    def load_current(self): return 0.1
    def load_power(self): return 2
    def solar_voltage(self): return 14.2
    def solar_current(self): return 0.5
    def solar_power(self): return 8
    def power_generation_today(self): return 39
    def load_status(self): return 1
    def load_on(self): print ("load_on")
    def load_off(self): print ("load_off")

class DisplayDummy():
    def log_event(self, message): print(message)
    def display_event(self, message): print(message)
    def display_status(self, message, key): print(f"{key}{message}")
    def poweroff(self): print('poweroff')
    def power_save_on(self): print('power_save_on')
    def power_save_off(self): print('power_save_off')
    