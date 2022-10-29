import logging

logger = logging.getLogger(__name__)


class control:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.state = None

    def on(self):
        pass

    def off(self):
        pass
