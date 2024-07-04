import logging


# Motor handlers inherit this class
class MotorWrapper:
    def __init__(self, config, firmata=None):
        # Setup logger
        self.logger = logging.getLogger(__name__)
        self.firmata = firmata

    def move_raw(self, left=None, right=None):
        pass

    def stop(self):
        pass

    def close(self):
        pass
