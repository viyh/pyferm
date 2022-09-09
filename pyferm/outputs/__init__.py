import csv
import os
import datetime
import time
from pyferm import threader


class output(threader):
    def __init__(self, name, parent, interval=60):
        self.name = name
        self.parent = parent
        self.logprefix = f"output - {self.name}"
        self.interval = interval

    def run(self):
        self.start_time = datetime.datetime.utcnow()
        while self._is_running:
            if not self.push():
                self.log("metric push failed. Retrying in 60 seconds.", "error")
                time.sleep(60)
            else:
                self.log(f"sleeping {self.interval} seconds")
                time.sleep(self.interval)

    def start(self):
        self.log("thread start")
        self._is_running = True
        self.start_thread()

    def stop(self):
        self.log("thread stop")
        self._is_running = False

    def push(self):
        self.log(f"output - {self.name}")

    def get_metrics(self):
        metrics = {}
        for metric_config in self.metrics:
            sensor = self.parent.get_sensor_by_name(metric_config["sensor"])
            metric = sensor.get_metric_by_name(metric_config["metric"])
            metrics[
                f'{metric_config["sensor"]} - {metric_config["metric"]}'
            ] = metric.get_value()
        return metrics


class output_csv(output):
    def __init__(self, name, parent, interval=60, filename=None, metrics=[]):
        self.metrics = metrics
        self.filename = filename
        self.logprefix = f"output - csv - {name}"
        self.init_csv()
        super().__init__(name, parent, interval)

    def push(self):
        self.log(f"push output to filename: {self.filename}", "debug")
        row = [
            datetime.datetime.utcnow().strftime("%Y-%m-%d"),
            datetime.datetime.utcnow().strftime("%H:%M:%S"),
        ]
        for metric_name, metric_value in self.get_metrics().items():
            row.append(f"{metric_value}")
        self.writerow(row)
        return True

    def init_csv(self):
        if os.path.exists(self.filename):
            self.log(f"{self.filename} already exists.")
            return True
        header = ["date", "time"]
        for source in self.sources:
            header.append(f"{source['sensor']} - {source['metric']}")
        self.writerow(header)

    def writerow(self, row):
        with open(self.filename, mode="a") as csvfile:
            csvwriter = csv.writer(
                csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )
            csvwriter.writerow(row)
