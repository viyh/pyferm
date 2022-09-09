import yaml
import logging
import threading
import time
from pyferm.steps import step_status
from pyferm.utils import class_loader


class singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, "_instance"):
            orig = super(singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance


class threader:
    def start_thread(self):
        if not hasattr(self, "interval"):
            self.interval = 30
        self.thread = threading.Thread(name=self.name, target=self.run)
        self.thread.daemon = True
        if not self.thread.is_alive():
            self.thread.start()

    def log(self, message, level="info"):
        logger = getattr(logging, level)
        logger(f"{self.logprefix:50s} {message}")

    def start(self):
        self.log("thread start")
        self._is_running = True
        self.start_thread()

    def stop(self):
        self.log("thread stop")
        self._is_running = False

    def run(self):
        while self._is_running:
            self.log("thread sleeper")
            time.sleep(60)


class pyferm:
    def __init__(self):
        self.load_config()
        self.current_step = 0
        self.logprefix = "pyferm"

    def log(self, message, level="info"):
        logger = getattr(logging, level)
        logger(f"{self.logprefix:50s} {message}")

    def start(self):
        self.load_sensors()
        self.load_steps()
        self.load_outputs()
        self.interval = self.config["vars"]["step_runner_interval"]
        self.step_runner()

    def load_config(self, config_filenames=["pyferm.defaults.yaml", "pyferm.yaml"]):
        self.config = {}
        for config_filename in config_filenames:
            with open(config_filename, "r") as config_file:
                try:
                    self.config.update(yaml.safe_load(config_file))
                except yaml.YAMLError as exc:
                    self.log(exc, "error")

    def load_sensors(self):
        self.sensors = []
        for sensor in self.config.get("sensors", {}):
            self.sensors.append(
                class_loader(
                    sensor["class"],
                    sensor["name"],
                    parent=self,
                    **sensor.get("params", {}),
                )
            )

    def load_control(self, name):
        for control in self.config.get("controls", {}):
            if control["name"] != name:
                continue
            return class_loader(
                control["class"],
                control["name"],
                parent=self,
                **control.get("params", {}),
            )

    def load_action(self, name):
        for action in self.config.get("actions", {}):
            if action["name"] != name:
                continue
            return class_loader(
                action["class"],
                action["name"],
                parent=self,
                **action.get("params", {}),
            )

    def load_outputs(self):
        self.outputs = []
        for output in self.config.get("outputs", {}):
            self.log(f"Loading output: {output['class']} - {output['name']}")
            output = class_loader(
                output["class"],
                output["name"],
                parent=self,
                **output.get("params", {}),
            )
            output.start()
            self.outputs.append(output)

    def load_steps(self):
        self.steps = []
        for step in self.config.get("steps", {}):
            self.steps.append(
                class_loader(
                    step["class"], step["name"], parent=self, **step.get("params", {})
                )
            )

    def step_runner(self):
        self.log("step_runner - start")
        self._is_running = True
        while self._is_running:
            if self.steps:
                self.steps[self.current_step].run()
                if self.steps[self.current_step].status == step_status.COMPLETED:
                    self.log(f"step_runner - step {self.current_step + 1} complete.")
                    self.current_step += 1
            if self.steps and self.current_step >= len(self.steps):
                self._is_running = False
            else:
                self.log(f"step_runner - sleeping {self.interval} seconds.")
                time.sleep(self.interval)
        self.log("step_runner - end")

    def get_sensor_by_name(self, name):
        return next((s for s in self.sensors if s.name == name), None)

    def get_action_by_name(self, name):
        return next((a for a in self.actions if a.name == name), None)
