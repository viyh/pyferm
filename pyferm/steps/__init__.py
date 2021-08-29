import logging
import time
from pyferm.utils import class_loader

STEP_STATUS = {
    0: "NOT RUNNING",
    1: "WAITING FOR TRIGGER",
    2: "TRIGGERS COMPLETE",
    3: "RUNNING",
    4: "COMPLETED",
    5: "FAILED",
    6: "UNKNOWN",
}


class brewstep:
    def __init__(self, name, triggers=[]):
        self.triggers = triggers
        self.status = 0
        logging.debug(f"step - {self.name} init")

    def run(self):
        # if not running, begin
        if self.status == 0:
            self.status = 1
        # if waiting for triggers, run triggers
        if self.status == 1:
            self.run_triggers()
        if self.status == 2:
            self.run()
        if self.status == 3:
            self.check()
        else:
            return

    def run_triggers(self):
        if not self.triggers:
            self.status = 2

        for trigger in self.triggers:
            logging.debug(f"step - {self.name} trigger - {trigger}")
            # if trigger.get("status", 0) != 3:
            #     self.check_trigger()
        self.status = 2

        if self.status == 2:
            self.start()

    def start(self):
        self.status = 3
        logging.debug(f"step - {self.name} start")

    def stop(self):
        self.status = 4
        logging.debug(f"step - {self.name} stop")
        pass

    def check(self):
        logging.debug(f"step - {self.name} - status: {self.get_status()}")
        pass

    def get_status(self):
        return STEP_STATUS[self.status]

    def time_string(self, dt):
        return dt.strftime("%Y-%d-%m %H:%M:%S")


class brewstep_runner:
    def __init__(self, config={}):
        logging.debug("step_runner - init")
        self.config = config
        self.interval = self.config["vars"]["step_runner_interval"]
        self.load_steps()
        self.current_step = 0

    def load_steps(self):
        self.steps = []
        for step in self.config.get("steps", {}):
            self.steps.append(
                class_loader(step["class"], step["name"], **step.get("params", {}))
            )

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
        if self.steps[self.current_step].status == 4:
            self.current_step += 1
            self.run()
