#!/usr/bin/env python3
import logging
from time import perf_counter
import serial
import os
import traceback
from multiprocessing import Pipe
import multiprocessing
from websocket_process import WebSocketProcess
import asyncio as aio
from plugin_system import PluginManager
from servo_wrapper import ServoWrapper, ServoModel
from servos.virtual import VirtualConnection
from typing import List, Optional


_INCREMENT = 10


class ServoHandler:
    def __init__(self, config, pipe, firmata=None):
        # Setup logger
        self.logger = logging.getLogger(__name__)
        self.pipe = pipe
        self.config = config
        # Create new plugin manager looking for subclasses of MotorWrapper in "src/motors/"
        self.pm = PluginManager(ServoWrapper, os.getcwd() + "/src/servos")
        # Load values from configuration file
        self.type = config['servos']['type'].lower()
        # Log loaded type
        self.logger.info(f"Opening servo connection of type '{self.type}'")
        try:
            # Create servo connection (from a list loaded by the plugin manager) using
            # class specified in the config
            self.connection: ServoWrapper = self.pm.wrappers[self.type](config['servos']['controller'])
        except Exception as e:
            if isinstance(e, KeyError):
                self.logger.error(f"Could not determine servo connection type "
                                  f"'{self.type}'")
            elif isinstance(e, serial.serialutil.SerialException):
                self.logger.error(f"Could not open servo connection of type '{self.type}'")
            else:
                traceback.print_exc()
            # Fall back to virtual connection common to all servo connection errors
            self.logger.warning("Falling back to virtual connection")
            self.connection = VirtualConnection(config['servos']['controller'])
            self.type = 'virtual'
        self.logger.info(f"Debug message 3")
        # Ensure Connection class has access to logging capabilities
        # self.connection.logger = self.logger
        self.Servos = {}
        self.logger.info(f"Debug message 4")
        for _id in config['servos']['ids']:
            self.Servos[_id] = 500
        self.logger.info(f"Debug message 5")

    def get_initial_messages(self):
        msg = []
        for _id in self.config['servos']['ids']:
            msg.append([_id, self.Servos[_id]])
        return {"SERVO_POS": msg}

    def go_to_pos(self, channel, pos):
        self.logger.debug("Moving servo {} to {}".format(channel, pos))
        self.Servos[channel] = self.connection.go_to(channel, pos)
        self.logger.debug("Sending updated servo pos of {}".format(self.Servos[channel]))
        self.pipe.send(["SERVO_POS", self.Servos[channel], pos])

    def increment_angle(self, channel, positive):
        self.go_to_pos(channel, self.Servos[channel] + (_INCREMENT if positive else -_INCREMENT))
    
    def move(self, channel, speed):
        pass
    
    def stop(self):
        self.connection.stop()

    def close(self):
        self.logger.info("Closing servo connection")
        # Set all servos to 0 and close connection
        self.stop()
        self.connection.close()
