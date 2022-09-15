from lib.Display import Display
from lib.WiFi import WiFi
from lib.Logger import Logger

class Engine():
    def __init__(self):
        print("Engine init")
        self.display = Display(self)
        self.wifi = WiFi(self)
        self.logger = Logger(self)

    def cleanup(self):
        self.display.poweroff()
        