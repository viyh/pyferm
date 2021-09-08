import requests
from pyferm.controls import brewcontrol


class ifttt(brewcontrol):
    def __init__(self, name, parent, webhooks={}):
        self.webhooks = webhooks
        super().__init__(name, parent)

    def on(self):
        self.log("Triggered on")
        return self.trigger(True)

    def off(self):
        self.log("Triggered off")
        return self.trigger(False)

    def trigger(self, state):
        if state not in self.webhooks:
            self.log(f"No '{state}' webhook configured for control {self.name}")
            return None
        if self.post_request(**self.webhooks[state]):
            self.state = True if state == "on" else False
            return True
        else:
            return False

    def post_request(self, webhook_event, secret_key):
        url = f"https://maker.ifttt.com/trigger/{webhook_event}/with/key/{secret_key}"
        response = requests.post(url)
        if response.status_code == 200:
            self.log(f"Posted event {webhook_event}")
            return True
        else:
            self.log(
                "Received unsuccessful response. HTTP Error Code: "
                f"{response.status_code}"
            )
            return False
