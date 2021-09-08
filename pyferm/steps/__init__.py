import logging
import time
import datetime
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
    def __init__(self, name, parent, actions=[], triggers=[], conditions=[]):
        self.name = name
        self.parent = parent
        self.logprefix = f"step - {self.name}"
        self.start_time = None
        self.end_time = None
        self.elapsed = None
        self.interval = 10
        self.actions_config = actions
        self.triggers = self.load_conditions(triggers)
        self.conditions = self.load_conditions(conditions)
        self.status = step_status.NOT_RUNNING
        self.log("init")

    def log(self, message, level="info"):
        logger = getattr(logging, level)
        logger(f"{self.logprefix:40s} {message}")

    def run(self):
        self.log(f"status: {self.get_status()}")
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

        time.sleep(self.interval)

    def load_actions(self, actions):
        action_objs = []
        for a in actions:
            action_obj = self.parent.load_action(a["action"])
            action_obj.set_params(parent=self, **a)
            action_objs.append(action_obj)
        return action_objs

    def load_conditions(self, conditions):
        condition_objs = []
        for c in conditions:
            condition_objs.append(condition(parent=self, **c))
        return condition_objs

    def check_conditions(self, conditions):
        self.elapsed = (datetime.datetime.utcnow() - self.start_time).seconds
        if not conditions:
            return True
        for c in conditions:
            if c.status != step_status.COMPLETED.value:
                c.check()
        if all([c.status == step_status.COMPLETED.value for c in conditions]):
            return True
        else:
            return False

    def run_conditions(self):
        self.log("run_conditions", "debug")
        if self.check_conditions(self.conditions):
            self.stop()

    def run_triggers(self):
        self.log("run_triggers", "debug")
        if self.check_conditions(self.triggers):
            self.status = step_status.TRIGGERS_COMPLETE

    def start(self):
        if self.status != step_status.TRIGGERS_COMPLETE:
            self.log(f"cannot start, status currently {self.get_status()}")
            return False
        self.status = step_status.RUNNING
        self.actions = self.load_actions(self.actions_config)
        for action in self.actions:
            action.start()
        self.log("start")

    def stop(self):
        self.status = step_status.COMPLETED
        self.end_time = datetime.datetime.utcnow()
        self.log("stop")
        self.log(f"start time: {self.time_string(self.start_time)}")
        self.log(f"end time: {self.time_string(self.end_time)}")
        self.log(f"elapsed time: {self.elapsed} seconds")
        self.actions = []
        # for action in self.actions:
        #     action.stop()

    def get_status(self):
        return step_status(self.status).name

    def time_string(self, dt):
        return dt.strftime("%Y-%m-%d %H:%M:%S")
