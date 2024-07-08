from pyfirmata import Board
from time import sleep 
from serial import Serial


HW_SERIAL0 = 0x00
HW_SERIAL1 = 0x01
HW_SERIAL2 = 0x02
HW_SERIAL3 = 0x03
HW_SERIAL4 = 0x04
HW_SERIAL5 = 0x05
HW_SERIAL6 = 0x06
HW_SERIAL7 = 0x07
SW_SERIAL0 = 0x08
SW_SERIAL1 = 0x09
SW_SERIAL2 = 0x0A
SW_SERIAL3 = 0x0B
SW_SERIAL4 = 0x0C
SW_SERIAL5 = 0x0D
SW_SERIAL6 = 0x0E
SW_SERIAL7 = 0x0F


SERIAL_DATA = 0x60
SERIAL_CONFIG = 0x10
SERIAL_WRITE = 0x20
SERIAL_CLOSE = 0x50
SERIAL_READ = 0x30
SERIAL_FLUSH = 0x60
SERIAL_REPLY = 0x40


START_SYSEX = 0xF0
END_SYSEX = 0xF7

SERIAL_READ_CONTINUOSLY = 0x00
SERIAL_STOP_READING = 0x01


def string_to_port(string):
    if string.startswith("HW"):
        return int(string[-1])
    elif string.startswith("SW"):
        return int(string[-1]) + 8
    else:
        raise Exception("Firmata Serial Port out of range")

class InvalidPortError(Exception):
	pass
	
LeonardoConfig = {
	'digital': tuple(x for x in range(14)),
	'analog': tuple(x for x in range(6)),
	'pwm': (3, 5, 6, 9, 10, 11),
	'use_ports': True,
	'disabled': (),  # no disabled as Serial0 is not on pins
	'hardwareSerial': (1,),
}

class SerialBoard(Board):
	
	def __init__(self, *args, **kwargs):
		super(SerialBoard, self).__init__(*args, **kwargs)
		
	
	def serialConfig(self, portId, baud = 57600, rx = None, tx = None):
		if portId > SW_SERIAL7:
			raise InvalidPortError("Serial Ports must be less than '0x0F'")
		
		if portId > HW_SERIAL7 and (rx == None or tx == None):
			raise InvalidPortError("Software Serial Ports must define a tx and rx pin")
		
		msg = bytearray([SERIAL_CONFIG | portId])
		msg.extend([(baud >> x) & 0x7f for x in range(0, 15, 7)])
		if(portId > HW_SERIAL7):
			msg.extend([rx, tx])
		
		self.send_sysex(SERIAL_DATA, msg)
	
	def serialWriteRaw(self, portId, data):
		if portId > SW_SERIAL7:
			raise InvalidPortError("Serial Ports must be less than '0x0F'")
		msg = bytearray([SERIAL_WRITE | portId])
		for byte in data:
			msg.extend([(byte >> x) & 0x7f for x in range(0, 8, 7)])
		
		self.send_sysex(SERIAL_DATA, msg)
		
		
	def serialStopRead(self, portId):
		msg = bytearray([SERIAL_READ |portId])
		msg.extend([SERIAL_STOP_READING])
		self.send_sysex(SERIAL_DATA, msg)
		
	def serialRead(self, portId, length = 0):
		msg = bytearray([SERIAL_READ |portId])
		msg.extend([SERIAL_READ_CONTINUOSLY])
		if length > 0:
			msg.extend([(length >> x) & 0x7f for x in range(0, 8, 7)])
		self.send_sysex(SERIAL_DATA, msg)
			
	def serialFlush(self, portId):
		msg = bytearray([SERIAL_FLUSH |portId])
		self.send_sysex(SERIAL_DATA, msg)
		
	def serialWriteString(self, portId, string):
		data = map(ord, string)
		self.serialWriteRaw(portId, data);
	
	def serialClose(self, portId):
		self.send_sysex(SERIAL_DATA, [SERIAL_CLOSE | portId])
	
class Leonardo(SerialBoard):
	def __init__(self, *args, **kwargs):
		args = list(args)
		args.append(LeonardoConfig)
		super(Leonardo, self).__init__(*args, **kwargs)
	
	def __str__(self):
		return "Arduino Leonardo {0.name} on {0.sp.port}".format(self)
