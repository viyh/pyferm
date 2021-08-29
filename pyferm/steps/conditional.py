from pyferm.steps import brewstep
import logging
import datetime


class conditional(brewstep):
    def __init__(self, name, triggers, conditions):
        self.elapsed = None
        super().__init__(name, triggers, conditions)

    def start(self):
        if self.status != 2:
            logging.info(
                f"condition - cannot start, status currently {self.get_status()}"
            )
            return False
        self.status = 3
        self.start_time = datetime.datetime.utcnow()
        logging.debug(f"step - {self.name} start, conditional")
        self.run_conditions()

    def stop(self):
        self.status = 4
        self.end_time = datetime.datetime.utcnow()
        logging.debug(
            f"condition - stop - start time: {self.time_string(self.start_time)}"
        )
        logging.debug(f"condition - stop - end time: {self.time_string(self.end_time)}")
        logging.debug(f"condition - stop - elapsed time: {self.elapsed} seconds")
