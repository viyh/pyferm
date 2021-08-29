import logging
import operator


class condition:
    def __init__(self, parent, target_type, target, value, operator):
        self.target_type = target_type
        self.target = target
        self.value = value
        self.operator = operator
        self.status = 0
        self.parent = parent

    def check(self):
        logging.debug(f"condition - {self.target_type} {self.operator} {self.value}")
        if self.target_type == "time" and self.target == "duration":
            self.check_duration()
        elif self.target_type == "metric":
            self.check_metric()

    def check_metric(self):
        sensor = self.parent.parent.parent.get_sensor_by_name(self.target["sensor"])
        metric = sensor.get_metric_by_name(self.target["metric"])
        logging.debug(
            f"condition - check metric [{self.target['metric']}] - "
            f"current value: {metric.get_value()}"
        )
        self.check_condition(metric.get_value(), self.value)

    def check_duration(self):
        logging.debug(f"condition - check duration [elapsed: {self.parent.elapsed}]")
        self.check_condition(self.parent.elapsed, self.value)

    def check_condition(self, a, b):
        op = self.get_operator_func()
        if not a or not b:
            return False
        if op(a, b):
            self.status = 4

    def get_operator_func(self):
        try:
            return getattr(operator, self.operator)
        except AttributeError:
            logging.error("Not a valid operator.")
            return False
