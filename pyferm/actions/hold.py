import logging
import time

from pyferm.actions import action

logger = logging.getLogger(__name__)


class hold(action):
    def __init__(self, name, parent, **kwargs):
        super().__init__(name, parent, **kwargs)

    def run(self):
        self.value = self.params["value"]
        self.low = self.params["controls"]["low"]
        self.high = self.params["controls"]["high"]
        self.metric = self.params["metric"]

        while self._is_running:
            if getattr(self, "value"):
                logger.info(f"set value: {self.value}")
                sensor = self.parent.get_sensor_by_name(self.metric["sensor"])
                metric = sensor.get_metric_by_name(self.metric["metric"])
                metric_value = metric.get_value()
                if metric_value:
                    logger.info(f"metric value: {metric_value}")
                    if metric_value < self.value - self.low["threshold"]:
                        logger.info(f"low threshold, triggering {self.low['control']}")
                        self.low_on()
                    if (
                        metric_value >= self.value - self.low["threshold"]
                        and metric_value
                    ):
                        logger.info(
                            f"low threshold met, turning off {self.low['control']}"
                        )
                        self.low_off()
                    if metric_value > self.value + self.high["threshold"]:
                        logger.info(
                            f"high threshold, triggering {self.high['control']}"
                        )
                        self.high_on()
                    if metric_value <= self.value - self.high["threshold"]:
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
