import RPi.GPIO as GPIO
from pygame.time import Clock
import time
from math import sqrt, atan2, pi

from Config import Config

class Control(object):
	def __init__(self):
		self.top_speed = Config['control']['top_speed']
		self.bottom_speed = Config['control']['bottom_speed']
		self.motor_freq = Config['control']['motor_freq']
		self.pin_refs = Config['control']['bcm_pin_refs']
		self.move_directions = Config['control']['move_directions']
		self.pulse_time = Config['control']['motors_on_time']

		self.phi_max = pi / 4
		self.phi_min = 0

		self.gpio_setup()
		self.en_a_pwm = GPIO.PWM(self.pin_refs['en_a'], self.motor_freq)
		self.en_b_pwm = GPIO.PWM(self.pin_refs['en_b'], self.motor_freq)

		self.ll = Config['control']['pwm_limits']['l_left']
		self.ls = Config['control']['pwm_limits']['l_straight']
		self.lr = Config['control']['pwm_limits']['l_right']
		self.rl = Config['control']['pwm_limits']['r_left']
		self.rs = Config['control']['pwm_limits']['r_straight']
		self.rr = Config['control']['pwm_limits']['r_right']

		self.moves = {
			'f': (self.ls, self.rs, 'forwards'),
			'fl': (self.ll, self.rl, 'forwards'),
			'fr': (self.lr, self.rr, 'forwards'),
			'stop': (0, 0, 'stopped')
		}

	def gpio_setup(self):
		GPIO.setmode(GPIO.BCM)
		for pin in self.pin_refs:
			GPIO.setup(self.pin_refs[pin], GPIO.OUT)

	def actuate_motors(self, pwm_a, pwm_b, direction):
		try:
			self.en_a_pwm.start(pwm_a)
			self.en_b_pwm.start(pwm_b)
		except ValueError as e:
			print(e)
			print("Attempted PWM: {}".format((pwm_a, pwm_b)))
		GPIO.output(self.pin_refs['in_1'], self.move_directions[direction]['in_1'])
		GPIO.output(self.pin_refs['in_2'], self.move_directions[direction]['in_2'])
		GPIO.output(self.pin_refs['in_3'], self.move_directions[direction]['in_3'])
		GPIO.output(self.pin_refs['in_4'], self.move_directions[direction]['in_4'])
		time.sleep(self.pulse_time)

	def normalise_speed(self, input_a, input_b):
		r_max = 100
		r_min = 0
		t_max = self.top_speed
		t_min = self.bottom_speed
		pwm_a = (((input_a - r_min)/(r_max - r_min))*(t_max - t_min)) + t_min
		pwm_b = (((input_a - r_min)/(r_max - r_min))*(t_max - t_min)) + t_min

		return pwm_a, pwm_b

	def move(self, dir, count=1):
		pwm_a = self.moves[dir][0]
		pwm_b = self.moves[dir][1]
		direction = self.moves[dir][2]
		for i in range(count):
			#if dir != 'stop':
			#	pwm_a, pwm_b = self.normalise_speed(pwm_a, pwm_b)
			self.actuate_motors(pwm_a, pwm_b, direction)

	def p_control(self, phi):
		if 0 <= phi < pi: # right turn
			pwm_l = self.ls + (phi * (self.lr - self.ls)) / (self.phi_max - self.phi_min)
			pwm_r = self.rs + (phi * (self.rr - self.rs)) / (self.phi_max - self.phi_min)
		else: # left turn
			phi = (-phi) % (2*pi)
			pwm_l = self.ls + (phi * (self.ll - self.rs)) / (self.phi_max - self.phi_min)
			pwm_r = self.rs + (phi * (self.rl - self.rs)) / (self.phi_max - self.phi_min)

		pwm_l, pwm_r = self.normalise_speed(pwm_l, pwm_r)
		self.actuate_motors(pwm_l, pwm_r, 'forwards')

		return pwm_l, pwm_r

	def stop(self):
		self.move('stop')
		GPIO.cleanup()

	def get_phi(self, x, p):
		xr = x[0][0] # x, y theta robot
		yr = x[2][0]
		tr = x[4][0]
		alpha = atan2((p[1] - yr), (p[0] - xr))
		phi = ((tr - alpha) % (2*pi))

		return phi

def main():
	ctrl = Control()

	ctrl.move('f', 10)

	ctrl.move('stop')
	GPIO.cleanup()

if __name__ == "__main__":
	main()
