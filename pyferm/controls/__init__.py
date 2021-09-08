import logging


class brewcontrol:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.logprefix = f"control - {self.name}"
        self.state = None

    def log(self, message, level="info"):
        logger = getattr(logging, level)
        logger(f"{self.logprefix:40s} {message}")

    def on(self):
        pass

    def off(self):
        pass
