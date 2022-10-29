import logging
import operator

logger = logging.getLogger(__name__)


class condition:
    def __init__(self, parent, target_type, target, value, operator):
        self.parent = parent
        self.target_type = target_type
        self.target = target
        self.value = value
        self.operator = operator
        self.status = 0

    def check(self):
        logger.debug(f"{self.target_type} {self.operator} {self.value}")
        if self.target_type == "time" and self.target == "duration":
            self.check_duration()
        elif self.target_type == "metric":
            self.check_metric()

    def check_metric(self):
        sensor = self.parent.parent.get_sensor_by_name(self.target["sensor"])
        metric = sensor.get_metric_by_name(self.target["metric"])
        logger.debug(
            f"check metric [{self.target['sensor']} - {self.target['metric']}] - "
            f"current value: {metric.get_value()}"
        )
        self.check_condition(metric.get_value(), self.value)

    def check_duration(self):
        logger.debug(f"check duration [elapsed: {self.parent.elapsed}]")
        self.check_condition(self.parent.elapsed, self.value)

    def check_condition(self, a, b):
        op = self.get_operator_func()
        if not a or not b:
            return False
        if op(a, b):
            self.status = 3

    def get_operator_func(self):
        try:
            return getattr(operator, self.operator)
        except AttributeError:
            logger.error(f"not a valid operator [{self.operator}]")
            return False
