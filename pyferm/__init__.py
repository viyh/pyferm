import yaml
import logging
from pyferm.steps import brewstep_runner
from pyferm.utils import class_loader


class pyferm:
    def __init__(self):
        self.load_config()

    def start(self):
        self.load_sensors()
        self.load_steps()
        self.load_outputs()
        self.step_runner.start()

    def load_config(self, config_filename="pyferm.yaml"):
        with open(config_filename, "r") as config_file:
            try:
                self.config = yaml.safe_load(config_file)
            except yaml.YAMLError as exc:
                logging.error(exc)

    def load_sensors(self):
        self.sensors = []
        for sensor in self.config.get("sensors", {}):
            self.sensors.append(
                class_loader(
                    sensor["class"],
                    sensor["name"],
                    parent=self,
                    **sensor.get("params", {})
                )
            )

    def load_outputs(self):
        self.outputs = []
        for output in self.config.get("outputs", {}):
            self.outputs.append(
                class_loader(
                    output["class"],
                    output["name"],
                    parent=self,
                    **output.get("params", {})
                )
            )

    def load_steps(self):
        self.step_runner = brewstep_runner(parent=self, config=self.config)

    def get_sensor_by_name(self, name):
        return next((s for s in self.sensors if s.name == name), None)
