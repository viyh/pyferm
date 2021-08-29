import logging
import time
import datetime
from pyferm.utils import class_loader
from pyferm.conditions import condition
from enum import Enum


class step_status(Enum):
    NOT_RUNNING = 0
    WAITING_FOR_TRIGGERS = 1
    TRIGGERS_COMPLETE = 2
    RUNNING = 3
    COMPLETED = 4
    FAILED = 5
    UNKNOWN = 6


class brewstep:
    def __init__(self, name, parent, triggers=[], conditions=[]):
        self.name = name
        self.start_time = None
        self.end_time = None
        self.elapsed = None
        self.triggers = self.load_conditions(triggers)
        self.conditions = self.load_conditions(conditions)
        self.status = step_status.NOT_RUNNING
        self.parent = parent
        logging.debug(f"step - {self.name} init")

    def run(self):
        # if not running, begin
        if self.status == step_status.NOT_RUNNING:
            self.start_time = datetime.datetime.utcnow()
            self.status = step_status.WAITING_FOR_TRIGGERS
        # if waiting for triggers, run triggers
        if self.status == step_status.WAITING_FOR_TRIGGERS:
            self.run_triggers()
        if self.status == step_status.TRIGGERS_COMPLETE:
            self.start()
        if self.status == step_status.RUNNING:
            self.run_conditions()
        else:
            return False

    def load_conditions(self, conditions):
        condition_objs = []
        for c in conditions:
            condition_objs.append(condition(parent=self, **c))
        return condition_objs

    def check_conditions(self, conditions):
        self.elapsed = (datetime.datetime.utcnow() - self.start_time).seconds
        for c in conditions:
            if c.status != step_status.COMPLETED.value:
                c.check()
        if all([c.status == step_status.COMPLETED.value for c in conditions]):
            return True
        else:
            return False

    def run_conditions(self):
        logging.debug("run_conditions")
        if self.check_conditions(self.conditions):
            self.stop()

    def run_triggers(self):
        logging.debug("run_triggers")
        if self.check_conditions(self.triggers):
            self.status = step_status.TRIGGERS_COMPLETE

    def start(self):
        if self.status != step_status.TRIGGERS_COMPLETE:
            logging.info(
                f"condition - cannot start, status currently {self.get_status()}"
            )
            return False
        self.status = step_status.RUNNING
        logging.debug(f"step - {self.name} start")

    def stop(self):
        self.status = step_status.COMPLETED
        self.end_time = datetime.datetime.utcnow()
        logging.debug(f"step - {self.name} stop")
        logging.debug(
            f"step - {self.name} - start time: {self.time_string(self.start_time)}"
        )
        logging.debug(
            f"step - {self.name} - end time: {self.time_string(self.end_time)}"
        )
        logging.debug(f"step - {self.name} - elapsed time: {self.elapsed} seconds")

    def get_status(self):
        return step_status(self.status).name

    def time_string(self, dt):
        return dt.strftime("%Y-%m-%d %H:%M:%S")


class brewstep_runner:
    def __init__(self, parent, config={}):
        logging.debug("step_runner - init")
        self.config = config
        self.interval = self.config["vars"]["step_runner_interval"]
        self.load_steps()
        self.current_step = 0
        self.parent = parent

    def load_steps(self):
        self.steps = []
        for step in self.config.get("steps", {}):
            s = class_loader(
                step["class"], step["name"], parent=self, **step.get("params", {})
            )
            self.steps.append(s)

    def start(self):
        while True:
            logging.info("step_runner - start")
            self.run()
            logging.info(f"step_runner - sleeping {self.interval} seconds.")
            time.sleep(self.config["vars"]["step_runner_interval"])

    def stop(self):
        pass

    def run(self):
        self.steps[self.current_step].run()
        if self.steps[self.current_step].status == step_status.COMPLETED:
            self.current_step += 1
            self.run()
