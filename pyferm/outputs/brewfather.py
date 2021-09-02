# from pyferm.utils import class_loader
# import csv
# import os
# import threading
# import time
# import datetime
from pyferm.outputs import brewoutput
import requests

allowed_metrics = ["temp", "gravity", "pressure", "ph", "bpm"]

unit_map = {
    "Celcius": "C",
    "Fahrenheit": "F",
    "Kelvin": "K",
    "Specific Gravity": "G",
    "Plato": "P",
    "PSI": "PSI",
    "Bar": "BAR",
    "Kilopascal": "KPA",
}


class brewfather(brewoutput):
    def __init__(self, name, parent, interval=900, api_key=None, metrics={}):
        self.api_key = api_key
        if not self.api_key:
            self.log("api_key param must be set to post data to brewfather.")
            return False
        self.metrics_config = metrics
        super().__init__(name, parent, interval)

    def push(self):
        self.log("Push output to brewfather", "debug")
        self.get_metrics()
        if not self.metrics:
            self.log("No metrics to submit (either not configured of no values yet).")
            return False
        data = self.create_request()
        return self.post_request(json=data)

    def post_request(self, url="https://log.brewfather.net/stream", json=None):
        params = {"id": self.api_key}
        self.log(f"json: {json}", "debug")
        response = requests.post(url, params=params, json=json)
        if response.status_code == 200:
            self.log(f"Submitted data: {json}")
            return True
        else:
            self.log(
                "Received unsuccessful response. HTTP Error Code: "
                f"{response.status_code}"
            )
            return False

    def get_metrics(self):
        self.metrics = {}
        for metric_name, metric_config in self.metrics_config.items():
            if metric_name not in allowed_metrics:
                self.log(
                    f"Metric {metric_name} is not a known Brewfather metric.", "warn"
                )
                continue
            sensor = self.parent.get_sensor_by_name(metric_config["sensor"])
            metric = sensor.get_metric_by_name(metric_config["metric"])
            if metric.get_value():
                self.metrics[metric_name] = float(metric.get_value())
                self.metrics[f"{metric_name}_unit"] = unit_map[metric.unit["name"]]

    def create_request(self):
        data = {"name": "pyferm"}
        for key, value in self.metrics.items():
            data[key] = value
        return data
