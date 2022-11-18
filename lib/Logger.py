from Device import AUTH_HEADER, PVOUTPUT_APIKEY, PVOUTPUT_SYSTEMID, PVOUTPUT_URL, REMOTE_LOG_URL

class Logger():
    def __init__(self, engine):
        print("Logger init")
        self.engine = engine
        self.counter = 0

    def log_remote(self, data):
        api_url = (REMOTE_LOG_URL or '').strip()
        if api_url:
            self.engine.wifi.post_request(REMOTE_LOG_URL, data = data, headers = { 
                "Authorization": f"Bearer {AUTH_HEADER}"
            })

    def log_pvoutput(self, data):
        api_url = (PVOUTPUT_URL or '').strip()
        if api_url:
            self.engine.display.log_event(f"pvoutput {data}")
            response = self.engine.wifi.post_request(api_url, data = data, headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-Pvoutput-Apikey": PVOUTPUT_APIKEY,
                "X-Pvoutput-SystemId":  PVOUTPUT_SYSTEMID
            })
            self.engine.display.log_event(f"pvoutput {response}")