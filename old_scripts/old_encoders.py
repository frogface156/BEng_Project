import RPi.GPIO as gpio
import time

class encoder_handler(object):

	def __init__(self):
#		self.la_pin = 36 # BOARD
#		self.lb_pin = 38
#		self.ra_pin = 32
#		self.rb_pin = 26
		self.la_pin = 16 # BCM
		self.lb_pin = 20
		self.ra_pin = 12
		self.rb_pin = 7
		self.ticks = [0, 0]
		self.ticks_last = [0, 0]
		self.dt_ticks = [0, 0]
		self.gpio_setup()
		self.read_pins()
		self.init_states()

	def gpio_setup(self):
#		gpio.setmode(gpio.BOARD) # Already set mode to BCM in IMU code?
		gpio.setup(self.la_pin, gpio.IN, pull_up_down = gpio.PUD_DOWN)
		gpio.setup(self.lb_pin, gpio.IN, pull_up_down = gpio.PUD_DOWN)
		gpio.setup(self.ra_pin, gpio.IN, pull_up_down = gpio.PUD_DOWN)
		gpio.setup(self.rb_pin, gpio.IN, pull_up_down = gpio.PUD_DOWN)

	def init_states(self):
		self.la_old = gpio.input(self.la_pin)
		self.lb_old = gpio.input(self.lb_pin)
		self.ra_old = gpio.input(self.ra_pin)
		self.rb_old = gpio.input(self.rb_pin)

	def read_pins(self):
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

	def display_tick_count(self):
		print("Ticks: {}".format(self.ticks))

	def return_motor_info(self):
		self.read_pins()
		self.update_ticks()
		return self.ticks
