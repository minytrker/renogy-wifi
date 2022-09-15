# Contains hardware build config info

# Device Info
DEVICE_ID = "sjc"
DEVICE_VERSION = "1.0"
PVOUTPUT_URL = 'http://pvoutput.org/service/r2/addstatus.jsp'
REMOTE_TIME_URL = 'http://worldtimeapi.org/api/ip'

# MAX32232 IC
RS232_UART_ID = 0X00
RS232_SLAVE_ADDR=0XFF

# SD1306 0.91" I2C OLED Display
DISPLAY_I2C_PORT = 1
DISPLAY_I2C_SDA = 10
DISPLAY_I2C_SCL = 11
DISPLAY_SSD1306_RES_X = 128
DISPLAY_SSD1306_RES_Y = 32