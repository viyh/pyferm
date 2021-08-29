# pybrew - sensor - Dummy

from . import brewsensor, brewmetric
from random import randint
import time


class dummy(brewsensor):
    def __init__(self, name="Dummy"):
        self.name = name
        super().__init__(self.name)
        self.metrics = [
            brewmetric(name="Temperature", metric_type="temperature"),
            brewmetric(name="Gravity", metric_type="gravity"),
        ]
        self.metrics[0].set_value(66)
        self.metrics[1].set_value(1.040)

    def get_metrics(self):
        time.sleep(5)
        self.metrics[0].set_value(randint(0, 10))
        self.metrics[1].set_value(randint(0, 10))
