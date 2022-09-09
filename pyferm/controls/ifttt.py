import requests
from pyferm.controls import control


class ifttt(control):
    def __init__(self, name, parent, webhooks={}):
        self.webhooks = webhooks
        super().__init__(name, parent)

    def on(self):
        if self.state == False:
            self.log("TRIGGERED ON")
            return self.trigger(True)

    def off(self):
        if self.state == True:
            self.log("TRIGGERED OFF")
            return self.trigger(False)

    def trigger(self, state):
        if state not in self.webhooks:
            self.log(f"no '{state}' webhook configured for control {self.name}")
            return None
        if self.post_request(**self.webhooks[state]):
            self.state = state
            return True
        else:
            return False

    def post_request(self, webhook_event, secret_key):
        url = f"https://maker.ifttt.com/trigger/{webhook_event}/with/key/{secret_key}"
        response = requests.post(url)
        if response.status_code == 200:
            self.log(f"posted event {webhook_event}")
            return True
        else:
            self.log(
                "received unsuccessful response. HTTP Error Code: "
                f"{response.status_code}"
            )
            return False
