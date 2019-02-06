import RPi.GPIO as gpio
import time

class encoder_handler(object):

	def __init__(self):
		self.la_pin = 36
		self.lb_pin = 38
		self.ra_pin = 32
		self.rb_pin = 26
		self.locked = False
		self.gpio_setup()
		self.init_states()
		self.init_ticks()

	def gpio_setup(self):
		gpio.setmode(gpio.BOARD)
		gpio.setup(self.la_pin, gpio.IN, pull_up_down = gpio.PUD_DOWN)
		gpio.setup(self.lb_pin, gpio.IN, pull_up_down = gpio.PUD_DOWN)
		gpio.setup(self.ra_pin, gpio.IN, pull_up_down = gpio.PUD_DOWN)
		gpio.setup(self.rb_pin, gpio.IN, pull_up_down = gpio.PUD_DOWN)

	def cleanup(self):
		gpio.cleanup()

	def init_states(self):
		self.la_old = gpio.input(self.la_pin)
		self.lb_old = gpio.input(self.lb_pin)
		self.ra_old = gpio.input(self.ra_pin)
		self.rb_old = gpio.input(self.rb_pin)

	def init_ticks(self):
		self.ticks = [0, 0]
		self.ticks_last = [0, 0]
		self.dt_ticks = [0, 0]

	def update(self):
		#if self.reset_motor_ticks:
		#	print("Code executed...")
		#	self.reset_motor_ticks()
		self.read_pins()
		self.update_ticks()
		self.update_dt_ticks()
		return self.ticks

	def read_pins(self):
		self.la = gpio.input(self.la_pin)
		self.lb = gpio.input(self.lb_pin)
		self.ra = gpio.input(self.ra_pin)
		self.rb = gpio.input(self.rb_pin)

	def reset_motor_ticks(self):
		self.ticks_last = self.ticks
		self.dt_ticks = [0, 0]

	def update_dt_ticks(self):
		self.dt_ticks[0] = (self.ticks[0] - self.ticks_last[0])
		self.dt_ticks[1] = (self.ticks[1] - self.ticks_last[1])

	def update_ticks(self):
		if self.la == self.la_old:
			pass
		else:
			if self.la == 1:
				if self.lb == 1:
					self.ticks[0] += 1
				else:
					self.ticks[0] -= 1
			else:
				if self.lb == 1:
					self.ticks[0] -= 1
				else:
					self.ticks[0] += 1
		if self.lb == self.lb_old:
			pass
		else:
			if self.lb == 0:
				if self.la == 1:
					self.ticks[0] += 1
				else:
					self.ticks[0] -= 1
			else:
				if self.la == 1:
					self.ticks[0] -= 1
				else:
					self.ticks[0] += 1
		if self.ra == self.ra_old:
			pass
		else:
			if self.ra == 1:
				if self.rb == 1:
					self.ticks[1] -= 1
				else:
					self.ticks[1] += 1
			else:
				if self.rb == 1:
					self.ticks[1] += 1
				else:
					self.ticks[1] -= 1
		if self.rb == self.rb_old:
			pass
		else:
			if self.rb == 0:
				if self.ra == 1:
					self.ticks[1] -= 1
				else:
					self.ticks[1] += 1
			else:
				if self.ra == 1:
					self.ticks[1] += 1
				else:
					self.ticks[1] -= 1
		self.la_old = self.la
		self.lb_old = self.lb
		self.ra_old = self.ra
		self.rb_old = self.rb


	def print_states(self):
		print("LA: {}\tLB: {}\t RA: {}\tRB: {}".format(self.la, self.lb, self.ra, self.rb))

	def print_ticks(self):
		print("Ticks: {}\tLast ticks: {}\tDt ticks: {}".format(self.ticks, self.ticks_last, self.dt_ticks))
