import datetime
import logging

from pyferm import threader

logger = logging.getLogger(__name__)


class action(threader):
    def __init__(self, name, parent, **kwargs):
        self.name = name
        self.parent = parent
        self.state = None
        self.params = kwargs
        self.load_controls(self.params["controls"])
        self.action_start_time = datetime.datetime.utcnow()

    def low_on(self):
        self.controls["low"].on()

    def low_off(self):
        self.controls["low"].off()

    def high_on(self):
        self.controls["high"].on()

    def high_off(self):
        self.controls["high"].off()

    def set_params(self, action, **params):
        for p in params:
            logger.debug(f"setting param [{p}] = {params[p]}")
            self.params[p] = params[p]

    def load_controls(self, controls):
        self.controls = {}
        for k in controls:
            self.controls[k] = self.parent.load_control(controls[k]["control"])
