import network
import time
import lib.urequests as urequests
from utils import log_error

class WiFi():
    def __init__(self, engine):
        print("WiFi init")
        self.engine = engine
        self.wlan = network.WLAN(network.STA_IF)
        self.ssid = None
        self.password = None
        self.status_code = None
        self.wifi_networks = []
        self.connection_attempt = 0
        self.timeout = 30

    def connect(self, ssid, password):
        self.ssid = ssid
        self.password = password
        self.wlan.active(True)
        self.wlan.connect(self.ssid, self.password)

        self.engine.display.log_event("Connecting to {}...".format(self.ssid))
        timeout = 30
        while timeout > 0:
            if self.wlan.status() < 0 or self.wlan.status() >= 3:
                break
            timeout -= 1
            time.sleep(0.5)

        if self.wlan.status() == 3:
            self.engine.display.log_event("Connected to {}".format(self.ssid))
        else:
            self.engine.display.log_event('Network connection failed')
        self.status_code = self.wlan.status()
        return self.status_code

    def disconnect(self):
        self.wlan.disconnect()

    def is_connected(self):
        return self.wlan.status() == 3 and self.wlan.isconnected()

    def reconnect(self, ssid, password):
        if (self.is_connected() == False and self.connection_attempt < 5):
            self.connection_attempt = self.connection_attempt + 1
            self.connect(ssid, password)

    def get_request(self, url):
        if (not self.is_connected()):
            print ("not connected")
            return None
        try:
            return urequests.request('GET', url, timeout=self.timeout)
        except Exception as err:
            print(f"request failed {url} {str(err)}")
            return None

    def fetch_json_data(self, url):
        try:
            response = self.get_request(url)
            json =  response.json()
            response.close()
            return json
        except:
            return None

    def post_request(self, url, json = None, data = None, headers = {}):
        if (not self.is_connected()):
            return None
        try:
            response = urequests.request('POST', url, json=json, data = data, headers=headers, timeout=self.timeout)
            content =  response.text
            response.close()
            return content
        except Exception as err:
            print(f"request failed {url} {err}")
            log_error(err)
            return None
