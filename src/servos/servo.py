# coding: utf-8
#based off of code by aakmsk at https://github.com/aakmsk/serial_bus_servo_controller_python_module
import serial
import time
from SerialFirmata import Leonardo, HW_SERIAL1

FRAME_HEADER         =0x55
MOVE_TIME_WRITE      =1
MOVE_TIME_READ       =2
MOVE_TIME_WAIT_WRITE =7
MOVE_TIME_WAIT_READ  =8
MOVE_START           =11
MOVE_STOP            =12
ID_WRITE             =13
ID_READ              =14
ANGLE_OFFSET_ADJUST  =17
ANGLE_OFFSET_WRITE   =18
ANGLE_OFFSET_READ    =19
ANGLE_LIMIT_WRITE    =20
ANGLE_LIMIT_READ     =21
VIN_LIMIT_WRITE      =22
VIN_LIMIT_READ       =23
TEMP_MAX_LIMIT_WRITE =24
TEMP_MAX_LIMIT_READ  =25
TEMP_READ            =26
VIN_READ             =27
POS_READ             =28
OR_MOTOR_MODE_WRITE  =29
OR_MOTOR_MODE_READ   =30
LOAD_OR_UNLOAD_WRITE =31
LOAD_OR_UNLOAD_READ  =32
LED_CTRL_WRITE       =33
LED_CTRL_READ        =34
LED_ERROR_WRITE      =35
LED_ERROR_READ       =36

class SBS_Controller:
    def __init__(self, arduino, port):
        
        self.arduino = arduino
        self.port = port

    def cmd_servo_move(self, servo_id, angle_position, time):
        """
        Description: Control the rotation of any servo.
                     The rotation time of all servos commanded by this function will be the same.
        Parameters: 
            servo_id: list
                e.g. servo_id = [1, 2, 3, 4]   
            angle_position: list
                e.g. angle_position = [1000, 2000, 1000, 2000]  
                (note. The number of elements must be the same as servo_id)
            time: int (ms)
                e.g. time = 1000    
        return:
        """
        buf = bytearray()
        buf.extend([0x55,0x55])        
        buf.extend([0xff & (len(servo_id)*3+5)])    # length (the number of control servo * 3 + 5)
        buf.extend([0x03])                          # command value

        buf.extend([0xff & len(servo_id)])          # The number of servos to be controlled
        
        time = 0xffff & time
        buf.extend([(0xff & time), (0xff & (time >> 8))])   # Lower and Higher 8 bits of time value

        for i in range(len(servo_id)):
            p_val = 0xffff & angle_position[i]
            buf.extend([0xff & servo_id[i]])    # servo id
            buf.extend([(0xff & p_val), (0xff & (p_val >> 8))])   # Lower and Higher 8 bits of angle posiotion value

        self.arduino.serialWriteRaw(self.port, buf)

    # def cmd_get_battery_voltage(self):
        # """
        # Description: Get the servo controller's battery voltage in unit millivolts.
        # return: 
            # battery_voltage: float (V)
        # """
        # # transmit
        # buf = bytearray(b'\x55\x55')    # header 
        # buf.extend([0x02])              # length
        # buf.extend([0x0F])              # command value
        # # Empty the contents of the cache in preparation for receiving data.
        # count = self.ser.inWaiting()    # Check receive cache.
        # if count != 0:
            # _ = self.ser.read(count)    # Read out data
        # # Send command.
        # self.ser.write(buf)

        # # Receive
        # count = 0
        # recv_cmd_len = 6
        # while count != recv_cmd_len:        # Waiting for reception to finish.
            # count = self.ser.inWaiting()
        # recv_data = self.ser.read(count)    # Read the received byte data.
        # if count == recv_cmd_len:                      # Check if the number of bytes of data received is correct as a response to this command.
            # if recv_data[0] == 0x55 and recv_data[1] == 0x55 and recv_data[3] == 0x0F : # Check if the received data is a response to a command.
                # battery_voltage = 0xffff & (recv_data[4] | (0xff00 & (recv_data[5] << 8))) # Read battery  voltage
                # battery_voltage = battery_voltage / 1000.0

        # return battery_voltage

    # def cmd_mult_servo_unload(self, servo_id):
        # """
        # Description: Power off multiple servos and its motors, after sending this command.
        # Parameters: 
            # servo_id: list
                # e.g. servo_id = [1, 2, 3, 4]     
        # return:
        # """
        # buf = bytearray(b'\x55\x55')                # header 
        # buf.extend([0xff & (len(servo_id)+3)])      # length (the number of control servo + 3)
        # buf.extend([0x14])                          # command value

        # buf.extend([0xff & len(servo_id)])          # The number of servo to be controlled.

        # for i in range(len(servo_id)):
            # buf.extend([0xff & servo_id[i]])    # servo id

        # self.ser.write(buf)      

    def cmd_mult_servo_pos_read(self, servo_id):
        """
        Description: Read a angle position values of multiple servos.
        Parameters: 
            servo_id: list
                e.g. servo_id = [1, 2, 3, 4]   
        return: 
            angle_pos_values: list 
                note. The list size is the same as the number of servos you want to get values.
        """
        # transmit
        buf = bytearray(b'\x55\x55')            # header 
        buf.extend([0xff & (len(servo_id)+3)])  # length (the number of control servo + 3)
        buf.extend([0x15])                      # command value
        buf.extend([0xff & len(servo_id)])          # The number of servo to be controlled.

        for i in range(len(servo_id)):
            buf.extend([0xff & servo_id[i]])    # servo id

        #flush port
        self.arduino.serialFlush(self.port)
        
        # Send command.
        self.arduino.serialWriteRaw(self.port, buf)

        # Receive
        count = 0
        recv_cmd_len = len(servo_id) * 3 + 5
        
        self.arduino.serialRead(self.port, recv_cmd_len)
        
        
        
        if count == recv_cmd_len:           # Check if the number of bytes of data received is correct as a response to this command.
            if recv_data[0] == 0x55 and recv_data[1] == 0x55 and recv_data[3] == 0x15:  # Check if the received data is a response to a command.
                for i in range(len(servo_id)):
                    angle_pos_values[i] = 0xffff & (recv_data[6+3*i] | (0xff00 & (recv_data[7+3*i] << 8))) # Read battery  voltage

        return angle_pos_values
