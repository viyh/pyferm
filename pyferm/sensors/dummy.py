# pybrew - sensor - Dummy

from . import brewsensor, brewmetric
from random import randint
import time


class dummy(brewsensor):
    def __init__(self, name="Dummy", parent=None):
        super().__init__(name, parent)
        self.metrics = [
            brewmetric(name="Temperature", metric_type="temperature"),
            brewmetric(name="Gravity", metric_type="gravity"),
        ]

    def get_metrics(self):
        time.sleep(2)
        self.get_metric_by_name("Temperature").set_value(randint(50, 80))
        self.get_metric_by_name("Gravity").set_value(randint(1000, 1070) / 1000.0)
