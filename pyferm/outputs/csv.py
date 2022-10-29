import csv
import datetime
import logging
import os

from pyferm.outputs import output

logger = logging.getLogger(__name__ + '.outputs.csv')


class output_csv(output):
    def __init__(self, name, parent, interval=60, filename=None, metrics=[]):
        self.metrics = metrics
        self.filename = filename
        self.init_csv()
        super().__init__(name, parent, interval)

    def push(self):
        logger.debug(f"push output to filename: {self.filename}")
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
            logger.info(f"{self.filename} already exists.")
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
