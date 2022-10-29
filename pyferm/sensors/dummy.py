# pybrew - sensor - Dummy

import logging
import time
from random import randint

from . import metric, sensor

logger = logging.getLogger(__name__)


class dummy(sensor):
    def __init__(self, name="Dummy", parent=None):
        logger.debug("init")
        super().__init__(name, parent)
        self.metrics = [
            metric(name="temperature", metric_type="temperature"),
            metric(name="gravity", metric_type="gravity"),
        ]
        logger.debug("init complete")

    def get_metrics(self):
        logger.debug("get metric")
        time.sleep(2)
        self.get_metric_by_name("temperature").set_value(randint(50, 80))
        self.get_metric_by_name("gravity").set_value(randint(1000, 1070) / 1000.0)
        logger.debug("get metric complete")
