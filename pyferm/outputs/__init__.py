import logging
import csv
import os
import datetime
import threading
import time


class brewoutput:
    def __init__(self, name, parent, interval=60):
        self.name = name
        self.parent = parent
        self.logprefix = f"output - {self.name}"
        self.interval = interval
        self.thread = threading.Thread(name=self.name, target=self.run, args=())
        self.thread.daemon = True
        if not self.thread.is_alive():
            self.thread.start()

    def log(self, message, level="info"):
        logger = getattr(logging, level)
        logger(f"{self.logprefix:40s} {message}")

    def run(self):
        while True:
            if not self.push():
                self.log("Metric push failed. Retrying in 60 seconds.", "warn")
                time.sleep(60)
            else:
                self.log(f"Sleeping {self.interval} seconds")
                time.sleep(self.interval)

    def get_metrics(self):
        metrics = {}
        for metric_config in self.metrics:
            sensor = self.parent.get_sensor_by_name(metric_config["sensor"])
            metric = sensor.get_metric_by_name(metric_config["metric"])
            metrics[
                f'{metric_config["sensor"]} - {metric_config["metric"]}'
            ] = metric.get_value()
        return metrics

    def push(self):
        self.log(f"output - {self.name}")


class brewoutput_csv(brewoutput):
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
