# pybrew - sensor - Dummy

import logging

from pyferm.controls import control

logger = logging.getLogger(__name__ + '.controls.dummy')


class dummy(control):
    def __init__(self, name="Dummy", parent=None):
        super().__init__(name, parent)

    def on(self):
        if self.state is None or self.state is False:
            self.state = True
            logger.info("TRIGGERED ON")
            return True

    def off(self):
        if self.state is None or self.state is True:
            self.state = False
            logger.info("TRIGGERED OFF")
            return True
