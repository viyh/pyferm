import time
import datetime
from pyferm.actions import action


class ramp(action):
    def __init__(self, name, parent, **kwargs):
        super().__init__(name, parent, **kwargs)

    def run(self):
        self.start_value = self.params["start_value"]
        self.end_value = self.params["end_value"]
        self.step_interval = self.params["step_interval"]
        self.step_size = self.params["step_size"]

        self.low = self.params["controls"]["low"]
        self.high = self.params["controls"]["high"]
        self.metric = self.params["metric"]

        self.current_value = self.start_value

        while self._is_running:
            self.action_elapsed = (
                datetime.datetime.utcnow() - self.action_start_time
            ).seconds
            self.log(f"elapsed: {self.action_elapsed}")
            if self.action_elapsed > self.step_interval:
                self.log(f"Next step, value: {self.current_value}")
                self.action_start_time = datetime.datetime.utcnow()
                self.current_value += self.step_size
            if self.current_value > self.end_value:
                self._is_running = False
                break
            elif getattr(self, "current_value"):
                self.log(f"Set value: {self.current_value}")
                sensor = self.parent.get_sensor_by_name(self.metric["sensor"])
                metric = sensor.get_metric_by_name(self.metric["metric"])
                metric_value = metric.get_value()
                if metric_value:
                    self.log(f"Metric value: {metric_value}")
                    if metric_value < self.value - self.low["threshold"]:
                        self.log(f"Low threshold, triggering {self.low['control']}")
                        self.low_on()
                    if (
                        metric_value >= self.value - self.low["threshold"]
                        and metric_value
                    ):
                        self.log(
                            f"Low threshold met, turning off {self.low['control']}"
                        )
                        self.low_off()
                    if metric_value > self.value + self.high["threshold"]:
                        self.log(f"High threshold, triggering {self.high['control']}")
                        self.high_on()
                    if metric_value <= self.value - self.high["threshold"]:
                        self.log(
                            f"High threshold met, turning off {self.high['control']}"
                        )
                        self.high_off()
                else:
                    self.log(
                        f'No metric value for {self.metric["sensor"]} - '
                        f'{self.metric["metric"]}'
                    )

            self.log(f"Sleeping {self.interval} seconds")
            time.sleep(self.interval)
