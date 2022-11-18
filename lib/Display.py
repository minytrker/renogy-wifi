from time import sleep
from machine import Pin, I2C
import framebuf
from ssd1306 import SSD1306_I2C
from utils import execute_timer
from writer import Writer
from fonts import font6, freesans30
from Device import DISPLAY_I2C_SDA, DISPLAY_I2C_SCL, DISPLAY_I2C_PORT, DISPLAY_SSD1306_RES_X, DISPLAY_SSD1306_RES_Y

class Display():
    def __init__(self, engine):
        print("LoggerDisplay init")
        self.engine = engine
        self.pix_res_x  = DISPLAY_SSD1306_RES_X
        self.pix_res_y = DISPLAY_SSD1306_RES_Y
        self.i2c_dev = I2C(DISPLAY_I2C_PORT, scl=Pin(DISPLAY_I2C_SCL), sda=Pin(DISPLAY_I2C_SDA), freq=200000)  # start I2C on I2C0
        self.i2c_addr = [hex(ii) for ii in self.i2c_dev.scan()]
        if self.i2c_addr==[]:
            print('No I2C Display Found') 
        else:
            self.oled = SSD1306_I2C(self.pix_res_x, self.pix_res_y, self.i2c_dev) # oled controller
            self.writer =  Writer(self.oled, font6)
            self.writer_big =  Writer(self.oled, freesans30)
            self.icons = {
                'sun': self.load_image('fonts/sun.pbm'),
                'bulb': self.load_image('fonts/bulb.pbm'),
                'battery': self.load_image('fonts/battery.pbm')
            }
        self.counter = 0
        self.power_save_mode = False
        self.is_display_busy = False

    def log_event(self, event, remote_logging = False, log_data = {}):
        print(event)
        self.display_event(event)
        if (remote_logging): self.log_remote(event, log_data)

    def display_event(self, message):
        if self.i2c_addr==[] or self.power_save_mode:
            return
        if self.is_display_busy: sleep(0.1)
        self.lock_display()
        self.oled.fill(0)
        Writer.set_textpos(self.oled, 0, 0) 
        self.writer.printstring(message)
        self.oled.show()
        execute_timer(self.unlock_display, 0.1)

    def display_status(self, status, key):
        main_value = str(status['value'])
        print (f"{key}: {status}")

        if self.i2c_addr!=[] and not self.power_save_mode:
            if self.is_display_busy: sleep(0.1)
            self.lock_display()
            self.oled.fill(0)
            if status['icon'] is not None and status['icon'] != '' and self.icons[status['icon']] is not None:
                self.draw_image(self.icons[status['icon']])
            elif status['label'] is not None:
                label_pos_y = 0 if self.writer.stringlen(status['label']) > DISPLAY_SSD1306_RES_X else 12
                Writer.set_textpos(self.oled, label_pos_y, 0)
                self.writer.printstring(status['label'])
            value_pos = min(128 - self.writer_big.stringlen(main_value), 127)
            Writer.set_textpos(self.oled, 2, value_pos)
            self.writer_big.printstring(main_value)
            self.oled.show()
            execute_timer(self.unlock_display, 0.1)
            
        self.counter = self.counter + 1

    def load_image(self, file):
        with open(file, 'rb') as f:
            f.readline() # Magic number
            f.readline() # Dimensions
            data =  bytearray(f.read())
            f.close()
            return data

    def draw_image(self, icon, width = 32, height = 32, x=0, y=0):
        fbuf = framebuf.FrameBuffer(icon, width, height, framebuf.MONO_HLSB)
        self.oled.blit(fbuf, x, y)

    def poweroff(self):
        self.power_save_mode = True
        if self.i2c_addr==[]: return
        self.oled.fill(0)
        self.oled.poweroff()
        print("power off display")

    def poweron(self):
        self.power_save_mode = False
        if self.i2c_addr==[]: return
        self.oled.poweron()
        print("power on display")

    def lock_display(self):
        self.is_display_busy = True

    def unlock_display(self):
        self.is_display_busy = False
