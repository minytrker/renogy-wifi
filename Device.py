# Device Info
DEVICE_ID = "rng-wifi-01"
DEVICE_VERSION = "1.0"
LED_PIN = 'LED'

# WiFi settings 
WIFI_SSID = "WIFI_SSID"
WIFI_PASSWORD = "WIFI_PASSWORD"

# Settings for PVOutput
PVOUTPUT_APIKEY = "PVOUTPUT_APIKEY"
PVOUTPUT_SYSTEMID = "PVOUTPUT_SYSTEMID"
PVOUTPUT_URL = 'http://pvoutput.org/service/r2/addstatus.jsp' # Leave URL empty '' to disable

# Settings for custom logging to your server
REMOTE_LOG_URL = 'REMOTE_LOG_URL' #Leave URL empty '' to disable.
AUTH_HEADER = "AUTH_HEADER" # Sent as "Authorization: Bearer {AUTH_HEADER}"

# For time syncing
REMOTE_TIME_URL = 'http://worldtimeapi.org/api/ip'

# --- DO NOT TOUCH BELOW CONFIG --

# MAX32232 IC
RS232_UART_ID = 0
RS232_UART_TX = 0 #10
RS232_UART_RX = 1 #9
RS232_SLAVE_ADDR=0XFF

# SD1306 0.91" I2C OLED Display
DISPLAY_I2C_PORT = 1
DISPLAY_I2C_SDA = 10
DISPLAY_I2C_SCL = 11
DISPLAY_SSD1306_RES_X = 128
DISPLAY_SSD1306_RES_Y = 32
