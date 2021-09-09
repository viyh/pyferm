import logging
import operator


class condition:
    def __init__(self, parent, target_type, target, value, operator):
        self.parent = parent
        self.logprefix = "condition"
        self.target_type = target_type
        self.target = target
        self.value = value
        self.operator = operator
        self.status = 0

    def log(self, message, level="info"):
        logger = getattr(logging, level)
        logger(f"{self.logprefix:50s} {message}")

    def check(self):
        self.log(f"{self.target_type} {self.operator} {self.value}", "debug")
        if self.target_type == "time" and self.target == "duration":
            self.check_duration()
        elif self.target_type == "metric":
            self.check_metric()

    def check_metric(self):
        sensor = self.parent.parent.get_sensor_by_name(self.target["sensor"])
        metric = sensor.get_metric_by_name(self.target["metric"])
        self.log(
            f"check metric [{self.target['sensor']} - {self.target['metric']}] - "
            f"current value: {metric.get_value()}",
            "debug",
        )
        self.check_condition(metric.get_value(), self.value)

    def check_duration(self):
        self.log(f"check duration [elapsed: {self.parent.elapsed}]")
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
            self.log(f"not a valid operator [{self.operator}]", "error")
            return False
