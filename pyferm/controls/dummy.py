# pybrew - sensor - Dummy

from pyferm.controls import control

from random import randint
import time


class dummy(control):
    def __init__(self, name="Dummy", parent=None):
        super().__init__(name, parent)

    def on(self):
        if self.state is None or self.state == False:
            self.state = True
            self.log("TRIGGERED ON")
            return True

    def off(self):
        if self.state is None or self.state == True:
            self.state = False
            self.log("TRIGGERED OFF")
            return True
