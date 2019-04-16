import RPi.GPIO as GPIO
from pygame.time import Clock
import time

from Config import Config

class Control(object):
	def __init__(self):
		self.top_speed = Config['control']['top_speed']
		self.motor_freq = Config['control']['motor_freq']
		self.pin_refs = Config['control']['pin_refs']
		self.move_directions = Config['control']['move_directions']
		self.hs = Config['control']['high_speed']
		self.ls = Config['control']['low_speed']
		self.l_boost = Config['control']['left_boost_factor']

		self.gpio_setup()
		self.en_a_pwm = GPIO.PWM(self.pin_refs['en_a'], self.motor_freq)
		self.en_b_pwm = GPIO.PWM(self.pin_refs['en_b'], self.motor_freq)

		self.moves = {
			'f': (self.hs, self.hs, 'forwards'),
			'fl': (self.hs, self.ls, 'forwards'),
			'fr': (self.ls, self.hs, 'forwards'),
			'b': (self.hs, self.hs, 'backwards'),
			'bl': (self.hs, self.ls, 'backwards'),
			'br': (self.ls, self.hs, 'backwards'),
			'stop': (0, 0, 'stopped')
		}

	def gpio_setup(self):
		GPIO.setmode(GPIO.BOARD)
		for pin in self.pin_refs:
			GPIO.setup(self.pin_refs[pin], GPIO.OUT)

	def actuate_motors(self, pwm_a, pwm_b, direction):
		self.en_a_pwm.start(pwm_a)
		self.en_b_pwm.start(pwm_b)
		GPIO.output(self.pin_refs['in_1'], self.move_directions[direction]['in_1'])
		GPIO.output(self.pin_refs['in_2'], self.move_directions[direction]['in_2'])
		GPIO.output(self.pin_refs['in_3'], self.move_directions[direction]['in_3'])
		GPIO.output(self.pin_refs['in_4'], self.move_directions[direction]['in_4'])

	def norm_speed(self, pwm_a, pwm_b):
		max_pwm = max(pwm_a, pwm_b)
		pwm_a = (pwm_a * self.top_speed) / max_pwm
		pwm_b = (pwm_b * self.top_speed) / max_pwm

		return pwm_a, pwm_b

	def move(self, dir, count=1):
		pwm_a = self.moves[dir][0]
		pwm_b = self.moves[dir][1]
		direction = self.moves[dir][2]
		for i in range(count):
			if dir != 'stop':
				pwm_a, pwm_b = self.norm_speed(pwm_a, pwm_b)
			self.actuate_motors(pwm_a, pwm_b, direction)
			time.sleep(0.1)

def main():
	ctrl = Control()

	ctrl.move('f', 5)

	ctrl.move('stop')
	GPIO.cleanup()


if __name__ == "__main__":
	main()
