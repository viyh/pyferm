import datetime
import logging
import time

from pyferm.actions import action

logger = logging.getLogger(__name__ + '.actions.ramp')


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
        self.action_step_start_time = datetime.datetime.utcnow()

        while self._is_running:
            self.action_step_elapsed = (
                datetime.datetime.utcnow() - self.action_step_start_time
            ).seconds
            logger.info(f"elapsed: {self.action_step_elapsed}")

            if (
                self.action_step_elapsed > self.step_interval
                and self.current_value < self.end_value
            ):
                self.action_step_start_time = datetime.datetime.utcnow()
                self.current_value += self.step_size
                logger.info(f"next step, value: {self.current_value}")
            else:
                logger.info(f"set value: {self.current_value}")
                sensor = self.parent.get_sensor_by_name(self.metric["sensor"])
                metric = sensor.get_metric_by_name(self.metric["metric"])
                metric_value = metric.get_value()
                if metric_value:
                    logger.info(f"metric value: {metric_value}")
                    if metric_value < self.current_value - self.low["threshold"]:
                        logger.info(f"low threshold, triggering {self.low['control']}")
                        self.low_on()
                    if (
                        metric_value >= self.current_value - self.low["threshold"]
                        and metric_value
                    ):
                        logger.info(
                            f"low threshold met, turning off {self.low['control']}"
                        )
                        self.low_off()
                    if metric_value > self.current_value + self.high["threshold"]:
                        logger.info(f"high threshold, triggering {self.high['control']}")
                        self.high_on()
                    if metric_value <= self.current_value - self.high["threshold"]:
                        logger.info(
                            f"high threshold met, turning off {self.high['control']}"
                        )
                        self.high_off()
                else:
                    logger.info(
                        f'no metric value for {self.metric["sensor"]} - '
                        f'{self.metric["metric"]}'
                    )

            logger.info(f"sleeping {self.interval} seconds")
            time.sleep(self.interval)
