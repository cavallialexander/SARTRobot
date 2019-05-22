#!/usr/bin/env python3
class ServoParty():
	def __init__(self):
		# Import desired libraries when initialised.
		# Initialise the motors by using the mkIV configuration
		# Set all 
		# Set shortname aliases
		from pypot.robot import from_json
		from contextlib import closing
		self.robot = from_json('mkiv.json')
		for m in self.robot.motors:
			m.compliant = False
			m.goal_position = 0
		self.fr = self.robot.front_right
		self.fl = self.robot.front_left
		self.br = self.robot.back_right
		self.bl = self.robot.back_left
		self.last_left = 0;
		self.last_right = 0;
		self.speed_factor = 5;
		
	def move(self, left, right):
		# Move motors with designated speed, set last left and right (For compatibility, will be removed)
		self.fl.moving_speed = left;
		self.bl.moving_speed = left;
		self.fr.moving_speed = right;
		self.br.moving_speed = right;
		self.last_left = left;
		self.last_right = right;
		
	def move_left(self, left):
		# Move left motors with designated speed
		self.fl.moving_speed = left;
		self.bl.moving_speed = left;
		self.last_left = left;
		
	def move_right(self, right):
		# Move right motors with designated speed
		self.fr.moving_speed = right;
		self.br.moving_speed = right;
		self.last_right = right;
		
	def stop(self):
		# Stop all motors
		self.fl.moving_speed = 0;
		self.bl.moving_speed = 0;
		self.fr.moving_speed = 0;
		self.br.moving_speed = 0;
		
	def close(self):
		# Cleanly close program (PyPot) DOES NOT WORK
		with closing(from_json('mkiv.json')) as my_robot:
			self.robot.close()
			pass
