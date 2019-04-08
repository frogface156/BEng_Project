import RPi.GPIO as gpio
import time
import os

# change the code later so you can easily adjust the OUT1,2,3,4 and modify in code (because $
in_1 = 7
in_2 = 11
in_3 = 12
in_4 = 13
en_a = 15
en_b = 21

enc_La = 36
enc_Lb = 38
enc_Ra = 32
enc_Rb = 26

# Direction values
forwards = ["forwards", False, True, True, False]
backwards = ["backwards", True, False, False, True]
spin_left = ["spin left", True, False, True, False]
spin_right = ["spin right", False, True, False, True]

class robot(object):
	def __init__(self):

		# Movement variables
		self.top_speed = 60 # max PWM duty cycle (100 max)
		self.motor_freq = 100 # PWM frequency for motors
		self.period = 0.1 # time on for motor control
		self.pwm_a = 0
		self.pwm_b = 0
		self.last_move_direction = 0
		self.last_spin_direction = 0
		self.last_movement = ""
		self.piv_y_limit = 0.25
		self.forwards = ["forwards", False, True, True, False]
		self.backwards = ["backwards", True, False, False, True]
		self.spin_left = ["spin left", True, False, True, False]
		self.spin_right = ["spin right", False, True, False, True]
		self.stopped = ["stopped", False, False, False, False]

		# Init stuff
		self.gpio_setup()
		self.en_a_pwm = gpio.PWM(en_a, self.motor_freq)
		self.en_b_pwm = gpio.PWM(en_b, self.motor_freq)

	@staticmethod
	def control2pwm():
		

	@staticmethod
	def gpio_setup()
		gpio.setmode(gpio.BOARD)
		gpio.setup(in_1, gpio.OUT)
		gpio.setup(in_2, gpio.OUT)
		gpio.setup(in_3, gpio.OUT)
		gpio.setup(in_4, gpio.OUT)
		gpio.setup(en_a, gpio.OUT)
		gpio.setup(en_b, gpio.OUT)

		gpio.setup(enc_La, gpio.IN, pull_up_down = gpio.PUD_DOWN)
		gpio.setup(enc_Lb, gpio.IN, pull_up_down = gpio.PUD_DOWN)
		gpio.setup(enc_Ra, gpio.IN, pull_up_down = gpio.PUD_DOWN)
		gpio.setup(enc_Rb, gpio.IN, pull_up_down = gpio.PUD_DOWN)
