from pypot.robot import from_json
import time

class ServoParty():
	def __init__(self):
		self.robot = from_json('my_robot.json')
		for m in self.robot.motors: # Note that we always provide an alias for all motors.
			m.compliant = False
			m.goal_position = 0
	def move(self, left, right):
		self.robot.front_left.moving_speed = left;
		self.robot.back_left.moving_speed = left;
		self.robot.front_right.moving_speed = right;
		self.robot.back_right.moving_speed = right;
	def stop(self):
		self.robot.front_left.moving_speed = 0;
		self.robot.back_left.moving_speed = 0;
		self.robot.front_right.moving_speed = 0;
		self.robot.back_right.moving_speed = 0;
