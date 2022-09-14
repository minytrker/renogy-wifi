# from lib.ConfigManager import ConfigManager
# from lib.LED import LED
from lib.DisplayLogger import DisplayLogger
from lib.WiFi import WiFi

class Engine():
    def __init__(self):
        print("Engine init")
        self.display_logger = DisplayLogger(self)
        # self.led = LED(self)
        self.wifi = WiFi(self)

    def cleanup(self):
        self.display_logger.poweroff()
        