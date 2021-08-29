# pybrew - sensor - Dummy

from . import brewsensor, brewmetric
from random import randint
import time


class dummy(brewsensor):
    def __init__(self, name="Dummy"):
        self.name = name
        self.metrics = [
            brewmetric(name="Temperature", metric_type="temperature"),
            brewmetric(name="Gravity", metric_type="gravity"),
        ]
        super().__init__(self.name)

    def get_metrics(self):
        time.sleep(2)
        self.get_metric_by_name("Temperature").set_value(randint(0, 10))
        self.get_metric_by_name("Gravity").set_value(randint(0, 10))
