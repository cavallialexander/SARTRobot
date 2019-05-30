# SARTRobot Mark IV DEVELOPMENT BRANCH

ALL CODE IN THIS REPOSITORY IS MOST LIKELY UNTESTED DUE TO LACK OF ACCESS TO THE SART ROBOT

The scripts and programs written by the Semi-Autonomous Rescue Team for the S.A.R.T. Mark IV rescue robot.

Configuration files for camera-streaming software _Motion_ can be found in the **_Motion_** directory. Arduino code for sensor data can be found in **_Arduino_**

## Scripts

### _servo_party.py_
The servo_party script contains a single class which utilises the PyPot library. This class is reusable in other scripts for all movement based purposes such as Autonomy and Manual Control

### _control_gamepad.py_
This script handles movement based on the data fetched from the SARTInterface once a button is pressed or the thumb sticks and triggers are moved. The data is recieved in a JSON format. From this information, the script sets the corresponding speeds and direction.

### _sensor_stream.py_
This script grabs the data from the Arduino's and the mainboard(UDOO, Raspberry Pi, NanoPi, Jetson) and streams it to the control interface through a WebSocket server.

Sensor data sent includes:
- Distance
- Temperature
- Gas
- CPU Usage
- CPU Temperature
- Total RAM and used RAM

### _stop_servos.py_
When the python script exits unexpectedly, this script is used as the last resort. Once run, all motors will stop spinning.

### _auto_pid.py_
This script allows the robot to run in autonomous mode. It’s in very early stages currently but in the future, it will allow the robot to navigate any of the main courses autonomously.

### SARTInterface
The robot code in this repository is used in tandom with the [SARTInterface](https://github.com/brucbr/SARTInterface/) code.

###Libraries

- [PyPot](https://github.com/poppy-project/pypot/)
- [WebSockets](https://github.com/aaugustin/websockets)

If a library that doesn't come with Python as a standard is not listed here, please open an issue and let us know! S.A.R.T likes to give credit where it's due.
