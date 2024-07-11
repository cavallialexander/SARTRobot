# Wrapper for simple serial motor controllers.
#
# Tested on Cytron SmartDriveDuo-30 MDDS30.
# Will also work with:
#  * Sabertooth motor controllers
#  * Any serial (not packetised) motor controller using the following schema:
# +---------------------------------------------+---------+----------------------------+
# |                    Binary                   |         |                            |
# +---------+-----------+-----------------------+         |                            |
# | Channel | Direction |         Speed         | Decimal |                            |
# +---------+-----------+---+---+---+---+---+---+         |                            |
# |    7    |     6     | 5 | 4 | 3 | 2 | 1 | 0 |         |                            |
# +---------+-----------+---+---+---+---+---+---+---------+----------------------------+
# |    0    |     0     | 0 | 0 | 0 | 0 | 0 | 0 |    0    | motor LEFT stop            |
# +---------+-----------+---+---+---+---+---+---+---------+----------------------------+
# |    0    |     0     | 1 | 1 | 1 | 1 | 1 | 1 |    63   | motor LEFT full speed CW   |
# +---------+-----------+---+---+---+---+---+---+---------+----------------------------+
# |    0    |     1     | 0 | 0 | 0 | 0 | 0 | 0 |    64   | motor LEFT stop            |
# +---------+-----------+---+---+---+---+---+---+---------+----------------------------+
# |    0    |     1     | 1 | 1 | 1 | 1 | 1 | 1 |   127   | motor LEFT full speed CCW  |
# +---------+-----------+---+---+---+---+---+---+---------+----------------------------+
# |    1    |     0     | 0 | 0 | 0 | 0 | 0 | 0 |   128   | motor RIGHT stop           |
# +---------+-----------+---+---+---+---+---+---+---------+----------------------------+
# |    1    |     0     | 1 | 1 | 1 | 1 | 1 | 1 |   191   | motor RIGHT full speed CW  |
# +---------+-----------+---+---+---+---+---+---+---------+----------------------------+
# |    1    |     1     | 0 | 0 | 0 | 0 | 0 | 0 |   192   | motor RIGHT stop           |
# +---------+-----------+---+---+---+---+---+---+---------+----------------------------+
# |    1    |     1     | 1 | 1 | 1 | 1 | 1 | 1 |   255   | motor RIGHT full speed CCW |
# +---------+-----------+---+---+---+---+---+---+---------+----------------------------+

from motor_wrapper import MotorWrapper
from SerialFirmata import Leonardo, string_to_port


class SimpleSerialConnection(MotorWrapper):
    # What type of motor this wrapper handles
    type_ = 'simpleserialfirmata'

    def __init__(self, config, **kwargs):
        MotorWrapper.__init__(self, config)
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
        self.logger.info("Setup Firmata Serial connection to sabertooths")
        self.logger.info("port: %s baudrate: %d rx: %d tx: %d", self.port, self.baudrate, self.rx, self.tx)
        self.firmata.serialConfig(self.port, self.baudrate, self.rx, self.tx)
        self.logger.info("Finish Firmata Serial connection to sabertooths")
        self.channels = config.get('channels')
        try:
            self.channels.get('left')
            self.channels.get('right')
        except AttributeError:
            self.channels['left'] = 1
            self.channels['right'] = 0
        
        self.logger.info("Finish init")

    def move_raw(self, left=None, right=None):
        # Left side
        if left is not None:
            offset = 64  # if left > 0 else 0
            msg = offset + (round(62 / 1000 * left))
            self.logger.info(f"moving left motor {msg}")
            self.firmata.serialWriteRaw(self.port, bytes([msg]))
        # Right side
        if right is not None:
            offset = 64  # if right > 0 else 0
            msg = offset + 128 + (round(62 / 1000 * right))
            self.logger.info(f"moving right motor {msg}")
            self.firmata.serialWriteRaw(self.port, bytes([msg]))

    def stop(self):
        self.firmata.serialWriteRaw(self.port, bytes([0]))

    def close(self):
        pass
