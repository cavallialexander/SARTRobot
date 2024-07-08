from servo_wrapper import ServoWrapper, ServoModel
import HiWonderFirmata as HiWonder
import logging
from SerialFirmata import string_to_port, Leonardo


class HiWonderConnection(ServoWrapper):
    type_ = 'hiwonder'

    def __init__(self, config):
        ServoWrapper.__init__(self, config)
        self.firmata = None
        try:
            self.logger.info("Initialising Firmata")
            firmataConf = config['firmata']
            self.logger.info("Got Firmata conf")
            self.logger.info(firmataConf)
            self.firmata = Leonardo(firmataConf['port'], baudrate=firmataConf['baudrate'], timeout=5)
            self.logger.info("Firmata created")
        except Exception as error:
            self.logger.error("No Firmata config found or it could not be connected to")
            self.logger.error(error)

        if self.firmata is None:
            raise Exception("no firmata provided")

        self.port = string_to_port(config.get('port'))
        self.baudrate = config.get('baudrate')
        self.tx = config.get('tx')
        self.rx = config.get('rx')
        self.firmata.serialConfig(self.port, self.baudrate, self.rx, self.tx)
        self.controller = HiWonder.SBS_Controller(self.firmata, self.port)

    def go_to(self, channel, pos, time=None):
        safe_pos = min(1000, max(0, pos))
        self.logger.info(f"Trying to moving channel {channel} to position {safe_pos}")
        self.controller.cmd_servo_move(channel, safe_pos, 1000 if time is None else time)
        return safe_pos

    def stop(self, channel=None):
        pass

    def close(self):
        pass
