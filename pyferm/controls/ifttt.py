import logging

import requests
from pyferm.controls import control

logger = logging.getLogger(__name__ + '.controls.ifttt')


class ifttt(control):
    def __init__(self, name, parent, webhooks={}):
        self.webhooks = webhooks
        super().__init__(name, parent)

    def on(self):
        if self.state is False:
            logger.info("TRIGGERED ON")
            return self.trigger(True)

    def off(self):
        if self.state is True:
            logger.info("TRIGGERED OFF")
            return self.trigger(False)

    def trigger(self, state):
        if state not in self.webhooks:
            logger.info(f"no '{state}' webhook configured for control {self.name}")
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
            logger.info(f"posted event {webhook_event}")
            return True
        else:
            logger.info(
                "received unsuccessful response. HTTP Error Code: "
                f"{response.status_code}"
            )
            return False
