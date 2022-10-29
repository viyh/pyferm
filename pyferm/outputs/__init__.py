import datetime
import logging
import time

from pyferm import threader

logger = logging.getLogger(__name__ + '.outputs')


class output(threader):
    def __init__(self, name, parent, interval=60):
        self.name = name
        self.parent = parent
        self.interval = interval

    def run(self):
        self.start_time = datetime.datetime.utcnow()
        while self._is_running:
            if not self.push():
                logger.error("metric push failed. Retrying in 60 seconds.")
                time.sleep(60)
            else:
                logger.info(f"sleeping {self.interval} seconds")
                time.sleep(self.interval)

    def start(self):
        logger.info("thread start")
        self._is_running = True
        self.start_thread()

    def stop(self):
        logger.info("thread stop")
        self._is_running = False

    def push(self):
        logger.info(f"output - {self.name}")

    def get_metrics(self):
        metrics = {}
        for metric_config in self.metrics:
            sensor = self.parent.get_sensor_by_name(metric_config["sensor"])
            metric = sensor.get_metric_by_name(metric_config["metric"])
            metrics[
                f'{metric_config["sensor"]} - {metric_config["metric"]}'
            ] = metric.get_value()
        return metrics
