import logging
from pyferm import threader


class action(threader):
    def __init__(self, name, parent, **kwargs):
        self.name = name
        self.parent = parent
        self.logprefix = f"action - {self.name}"
        self.state = None
        self.params = kwargs
        self.load_controls(self.params["controls"])

    def log(self, message, level="info"):
        logger = getattr(logging, level)
        logger(f"{self.logprefix:40s} {message}")

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
            self.log(f"Setting param [{p}] = {params[p]}", "debug")
            self.params[p] = params[p]

    def load_controls(self, controls):
        self.controls = {}
        for k in controls:
            self.controls[k] = self.parent.load_control(controls[k]["control"])
