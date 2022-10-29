import datetime
import logging
import time
from enum import Enum

from pyferm.conditions import condition

logger = logging.getLogger(__name__)


class step_status(Enum):
    NOT_RUNNING = 0
    STARTING = 1
    RUNNING = 2
    COMPLETED = 3
    FAILED = 4
    UNKNOWN = 5


class step:
    def __init__(self, name, parent, actions=[], triggers=[], conditions=[]):
        self.name = name
        self.parent = parent
        self.start_time = None
        self.end_time = None
        self.elapsed = None
        self.interval = 10
        self.actions_config = actions
        self.conditions = self.load_conditions(conditions)
        self.status = step_status.NOT_RUNNING
        logger.debug("init")

    def run(self):
        logger.debug(f"status: {self.get_status()}")
        # if not running, begin
        if self.status == step_status.NOT_RUNNING:
            self.start_time = datetime.datetime.utcnow()
            self.start()
        if self.status == step_status.RUNNING:
            self.run_conditions()
        if self.status == step_status.COMPLETED:
            self._is_running = False
            return True
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
        logger.debug("run_conditions")
        if self.check_conditions(self.conditions):
            self.stop()

    def start(self):
        self.status = step_status.STARTING
        self.actions = self.load_actions(self.actions_config)
        for action in self.actions:
            action.start()
        self.status = step_status.RUNNING
        logger.info("start")

    def stop(self):
        self.status = step_status.COMPLETED
        self.end_time = datetime.datetime.utcnow()
        logger.info("stop")
        logger.info(f"start time: {self.time_string(self.start_time)}")
        logger.info(f"end time: {self.time_string(self.end_time)}")
        logger.info(f"elapsed time: {self.elapsed} seconds")
        self.actions = None

    def get_status(self):
        return step_status(self.status).name

    def time_string(self, dt):
        return dt.strftime("%Y-%m-%d %H:%M:%S")
