# pybrew - sensor - Tilt Hydrometer

import time
import datetime
import threading
from random import randint
from pyferm import singleton
from pyferm.sensors import sensor, metric
from beacontools import BeaconScanner, IBeaconFilter

TILTS = {
    "a495bb10-c5b1-4b44-b512-1370f02d74de": "Red",
    "a495bb20-c5b1-4b44-b512-1370f02d74de": "Green",
    "a495bb30-c5b1-4b44-b512-1370f02d74de": "Black",
    "a495bb40-c5b1-4b44-b512-1370f02d74de": "Purple",
    "a495bb50-c5b1-4b44-b512-1370f02d74de": "Orange",
    "a495bb60-c5b1-4b44-b512-1370f02d74de": "Blue",
    "a495bb70-c5b1-4b44-b512-1370f02d74de": "Yellow",
    "a495bb80-c5b1-4b44-b512-1370f02d74de": "Pink",
}


class tilt_scanner(singleton):
    def __init__(self, scantime=5, interval=15):
        self.filters = [IBeaconFilter(uuid=t) for t in TILTS.keys()]
        self.cache = {}
        self.random = randint(0, 10000)
        self.interval = interval
        self.scantime = scantime
        thread = threading.Thread(name="tilt_scanner", target=self.run, args=())
        thread.daemon = True
        if not thread.is_alive():
            thread.start()

    def callback(self, bt_addr, rssi, packet, additional_info):
        self.cache[additional_info["uuid"]] = {
            "temperature": additional_info["major"],
            "gravity": additional_info["minor"] / 1000,
            "last_seen": datetime.datetime.utcnow(),
        }

    def run(self):
        while True:
            self.get_data()
            time.sleep(self.interval)

    def get_data(self):
        self.scanner = BeaconScanner(self.callback, device_filter=self.filters)
        self.scanner.start()
        time.sleep(self.scantime)
        self.scanner.stop()


class tilt(sensor):
    def __init__(self, name="Tilt", parent=None, color=None):
        if color:
            self.uuid = [u for u, c in TILTS.items() if c.lower() == color.lower()][0]
            if name == "Tilt":
                f"Tilt ({TILTS[self.uuid]})"
        else:
            self.uuid = None
        self.metrics = [
            metric("temperature", metric_type="temperature"),
            metric("gravity", metric_type="gravity"),
        ]
        self.tilt_scanner = tilt_scanner()
        super().__init__(name, parent)

    def get_metrics(self):
        # pick the first Tilt if color/uuid is not set
        cached_uuids = list(self.tilt_scanner.cache.keys())
        if not self.uuid and len(cached_uuids) > 0:
            self.uuid = cached_uuids[0]
            self.name = f"Tilt ({TILTS[self.uuid]})"
        if self.uuid and self.uuid in self.tilt_scanner.cache:
            self.last_seen = self.tilt_scanner.cache[self.uuid]["last_seen"]
            self.log(
                f'last seen: {self.last_seen.strftime("%Y-%m-%d %H:%M:%S")}',
                "debug",
            )
            self.get_metric_by_name("temperature").set_value(
                self.tilt_scanner.cache[self.uuid]["temperature"]
            )
            self.get_metric_by_name("gravity").set_value(
                self.tilt_scanner.cache[self.uuid]["gravity"]
            )
        else:
            time.sleep(10)
