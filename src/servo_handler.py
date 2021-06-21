#!/usr/bin/env python3
import logging
import serial
import os
import traceback
import asyncio as aio
from plugin_system import PluginManager
from servo_wrapper import ServoWrapper, ServoModel
from motors.virtual import VirtualConnection
from typing import List, Optional


class ServoBackgroundService:
    def __init__(self, connection, servos: List[ServoModel]):
        self.moving_servos = dict()
        self.servos = dict([(s.channel, s) for s in servos])
        self.connection = connection
        self.task = aio.create_task(self.servo_update())

    def set_speed(self, channel, vel):
        if vel == 0:
            self.stop([channel])
        else:
            self.moving_servos[channel] = vel*self.servos[channel].speed

    def stop(self, channels=None):
        if channels is None:
            self.moving_servos = dict()
        else:
            for channel in channels:
                self.moving_servos.pop(channel, None)

    def close(self):
        if self.task is not None:
            self.task.cancel()

    async def servo_update(self):
        for channel, vel in self.moving_servos.items():
            self.servos[channel].pos = self.connection.go_to(self.servos[channel].pos +
                                                             vel)
        await aio.sleep(0.01)
        self.task = aio.create_task(self.servo_update())


class ServoHandler:
    def __init__(self, config):
        # Setup logger
        self.logger = logging.getLogger(__name__)
        # Create new plugin manager looking for subclasses of MotorWrapper in "src/motors/"
        self.pm = PluginManager(ServoWrapper, os.getcwd() + "/src/servos")
        # Load values from configuration file
        self.type = config['servos']['type'].lower()
        # Log loaded type
        self.logger.info(f"Opening servo connection of type '{self.type}'")
        try:
            # Create servo connection (from a list loaded by the plugin manager) using
            # class specified in the config
            self.connection: ServoWrapper = self.pm.wrappers[self.type](config['servos'])
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
            self.connection = VirtualConnection(config['servos'])
            self.type = 'virtual'
        # Ensure Connection class has access to logging capabilities
        self.connection.logger = self.logger
        Servos = []
        for servo, conf in config['servos']['channels'].items():
            Servos.append(self.connection.create_servo_model(servo, conf))
        self.background_service = ServoBackgroundService(self.connection, Servos)
    
    def go_to_pos(self, channel, angle):
        pass
    
    def move(self, channel, speed):
        self.background_service.set_speed(channel, max(-1, min(1, speed)))
    
    def stop(self, channel=None):
        if channel is None:
            # stop all servos
            self.background_service.stop()
            self.connection.stop()
        else:
            self.background_service.stop(channel)
            self.connection.stop(channel)


    def close(self):
        self.logger.info("Closing servo connection")
        # Set all servos to 0 and close connection
        self.stop()
        self.background_service.close()
        self.connection.close()