# pybrew - sensor - Dummy

from . import sensor, metric
from random import randint
import time


class dummy(sensor):
    def __init__(self, name="Dummy", parent=None):
        super().__init__(name, parent)
        self.metrics = [
            metric(name="temperature", metric_type="temperature"),
            metric(name="gravity", metric_type="gravity"),
        ]

    def get_metrics(self):
        time.sleep(2)
        self.get_metric_by_name("temperature").set_value(randint(50, 80))
        self.get_metric_by_name("gravity").set_value(randint(1000, 1070) / 1000.0)
