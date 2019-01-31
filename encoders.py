import RPi.GPIO as gpio
import time

class encoder_handler(object):

	def __init__(self):
		self.la_pin = 36
		self.lb_pin = 38
		self.ra_pin = 32
		self.rb_pin = 26
		self.period = 0.25
		self.freq = 60
		self.l_ticks_last = 0
		self.r_ticks_last = 0
		self.l_diff = 0
		self.r_diff = 0
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

	def init_ticks(self):
		self.l_ticks = 0
		self.r_ticks = 0

	def init_states(self):
		self.la_old = gpio.input(self.la_pin)
		self.lb_old = gpio.input(self.lb_pin)
		self.ra_old = gpio.input(self.ra_pin)
		self.rb_old = gpio.input(self.rb_pin)

	def update_states(self):
		self.la = gpio.input(self.la_pin)
		self.lb = gpio.input(self.lb_pin)
		self.ra = gpio.input(self.ra_pin)
		self.rb = gpio.input(self.rb_pin)

	def update_ticks(self):
		if self.la == self.la_old:
			pass
		else:
			if self.la == 1:
				if self.lb == 1:
					self.l_ticks += 1
				else:
					self.l_ticks -= 1
			else:
				if self.lb == 1:
					self.l_ticks -= 1
				else:
					self.l_ticks += 1
		if self.lb == self.lb_old:
			pass
		else:
			if self.lb == 0:
				if self.la == 1:
					self.l_ticks += 1
				else:
					self.l_ticks -= 1
			else:
				if self.la == 1:
					self.l_ticks -= 1
				else:
					self.l_ticks += 1
		if self.ra == self.ra_old:
			pass
		else:
			if self.ra == 1:
				if self.rb == 1:
					self.r_ticks -= 1
				else:
					self.r_ticks += 1
			else:
				if self.rb == 1:
					self.r_ticks += 1
				else:
					self.r_ticks -= 1
		if self.rb == self.rb_old:
			pass
		else:
			if self.rb == 0:
				if self.ra == 1:
					self.r_ticks -= 1
				else:
					self.r_ticks += 1
			else:
				if self.ra == 1:
					self.r_ticks += 1
				else:
					self.r_ticks -= 1
		self.l_diff = self.l_ticks - self.l_ticks_last
		self.r_diff = self.r_ticks - self.r_ticks_last
		self.l_ticks_last = self.l_ticks
		self.r_ticks_last = self.r_ticks
		self.la_old = self.la
		self.lb_old = self.lb
		self.ra_old = self.ra
		self.rb_old = self.rb

	def print_states(self):
		print("LA: {}\tLB: {}\t RA: {}\tRB: {}".format(self.la, self.lb, self.ra, self.rb))

	def print_ticks(self):
		print("L_ticks: {}\tR_ticks: {}".format(self.l_ticks, self.r_ticks))
