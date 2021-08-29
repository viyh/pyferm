# from pyferm.utils import class_loader
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
        self.interval = interval
        self.thread = threading.Thread(name=self.name, target=self.run, args=())
        self.thread.daemon = True
        if not self.thread.is_alive():
            self.thread.start()

    def run(self):
        while True:
            self.push()
            time.sleep(self.interval)

    def push(self):
        self.log(f"output - {self.name}")

    def log(self, message, level="info"):
        logger = getattr(logging, level)
        logger(f"output - {self.name} - {message}")


class brewoutput_csv(brewoutput):
    def __init__(self, name, parent, interval=60, filename=None, sources=[]):
        self.sources = sources
        self.filename = filename
        self.init_csv()
        super().__init__(name, parent, interval)

    def push(self):
        self.log(f"push output to filename: {self.filename}", "debug")
        row = [
            datetime.datetime.utcnow().strftime("%Y-%m-%d"),
            datetime.datetime.utcnow().strftime("%H:%M:%S"),
        ]
        for source in self.sources:
            sensor = self.parent.get_sensor_by_name(source["source"]["sensor"])
            metric = sensor.get_metric_by_name(source["source"]["metric"])
            row.append(f"{metric.get_value()}")
        self.writerow(row)

    def init_csv(self):
        if os.path.exists(self.filename):
            self.log(f"{self.filename} already exists.")
            return True
        header = ["date", "time"]
        for source in self.sources:
            header.append(
                f"{source['source']['sensor']} - {source['source']['metric']}"
            )
        self.writerow(header)

    def writerow(self, row):
        with open(self.filename, mode="a") as csvfile:
            csvwriter = csv.writer(
                csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )
            csvwriter.writerow(row)

    def log(self, message, level="info"):
        logger = getattr(logging, level)
        logger(f"output - csv - {self.name} - {message}")


# def brewoutput_loader(config):
#     for output in config.get('outputs', {}):
