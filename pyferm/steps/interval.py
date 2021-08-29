from . import brewstep
import logging
import datetime


class interval(brewstep):
    def __init__(self, name, duration, triggers):
        self.name = name
        self.duration = duration
        self.start_time = None
        self.end_time = None
        self.elapsed = None
        self.triggers = triggers
        super().__init__(self.name, self.triggers)

    def start(self):
        if self.status != 2:
            logging.info(
                f"step - {self.name} cannot start, status currently {self.get_status()}"
            )
            return False
        self.status = 3
        self.start_time = datetime.datetime.utcnow()
        logging.debug(
            f"step - {self.name} start, interval duration: {self.duration} seconds"
        )

    def stop(self):
        self.status = 4
        self.end_time = datetime.datetime.utcnow()
        logging.debug(
            f"step - {self.name} stop - start time: {self.time_string(self.start_time)}"
        )
        logging.debug(
            f"step - {self.name} stop - end time: {self.time_string(self.end_time)}"
        )
        logging.debug(f"step - {self.name} stop - elapsed time: {self.elapsed} seconds")

    def time_string(self, dt):
        return dt.strftime("%Y-%d-%m %H:%M:%S")

    def check(self):
        self.elapsed = (datetime.datetime.utcnow() - self.start_time).seconds
        logging.debug(
            f"step - {self.name} - status: {self.get_status()}, "
            f"elapsed time: {self.elapsed} seconds"
        )
        if self.elapsed >= self.duration and self.duration != 0:
            self.stop()


# steps:
#   - name: hold temp
#     class: pyferm.steps.interval.interval
#     params:
#       duration: 3600
#     triggers:
#       - input: my_tilt.metric[0]
#         value: 70
#         threshold: 1, 1

#   - name: pause to dry hop
#     class: pyferm.steps.interval.interval
#     params:
#       duration: 0
#     triggers:
#       - input: my_tilt.metric[0]
#         value: 70
#         threshold: 1, 1
