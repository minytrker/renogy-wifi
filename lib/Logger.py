from Device import DEVICE_ID, DEVICE_VERSION, PVOUTPUT_URL, REMOTE_LOG_URL

class Logger():
    def __init__(self, engine):
        print("Logger init")
        self.engine = engine
        self.counter = 0

    def log_remote(self, event, log_data = {}):
        api_url = (REMOTE_LOG_URL or '').strip()
        if api_url:
            self.engine.wifi.post_request(self.engine.config['log_url'], json = {
                'message': event,
                'data': log_data,
                'device_id': DEVICE_ID,
                'device_version': DEVICE_VERSION
            }, headers = { "Authorization": f"Bearer {self.engine.secrets['auth_header']}"})

    def log_pvoutput(self, data):
        api_url = (PVOUTPUT_URL or '').strip()
        if api_url:
            self.engine.display.log_event(f"pvoutput {data}")
            response = self.engine.wifi.post_request(api_url, data = data, headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-Pvoutput-Apikey": self.engine.secrets['pvoutput_apikey'],
                "X-Pvoutput-SystemId":  self.engine.secrets['pvoutput_systemid']
            })
            self.engine.display.log_event(f"pvoutput {response}")