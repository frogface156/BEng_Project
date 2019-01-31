#!/usr/bin/python3

# MUST RUN AS ROOT!!

# adds left stick movement functionality

import RPi.GPIO as gpio
import time
import os
import pygame
import sys

# Debug mode - display joystick data verbosely
debug_mode = True
# Verbose mode - outputs pwm duty cycles and direction
verbose_mode = True
# Alert mode - buzzer to alert user of errors / issues / notifications
alert_mode = False

# pin references
in_1 = 12
in_2 = 13
in_3 = 7
in_4 = 11
en_a = 21
en_b = 15

trig = 18
echo = 22

servo_pin = 16

enc_La = 36
enc_Lb = 38
enc_Ra = 32
enc_Rb = 26

headlight_r = 29
headlight_l = 31


# Pygame init stuff
os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.init()
# Dummy screen init (required by pygame...)
#screen = pygame.display.set_mode((1,1))
# Loop until the user clicks the PS (or another?) button.
done = False
# Initialize the joysticks
pygame.joystick.init()

# Button debounce time
debounce_time = 0.25

# Direction values
forwards = ["forwards", False, True, True, False]
backwards = ["backwards", True, False, False, True]
spin_left = ["spin left", True, False, True, False]
spin_right = ["spin right", False, True, False, True]


class robot():
	def __init__(self): # potentially take in the controller as a parameter and use for the joystick stuff...

		# General variables (joystick, speed, freq, states etc.)
		self.joy_x_l = 0 # initializes joystick variables
		self.joy_y_l = 0
		self.joy_x_r = 0
		self.headlights_on = False # headlights off
		self.top_speed = 100 # max PWM duty cycle
		self.motor_freq = 100 # PWM frequency for motors (value obtained from youtube video)
		self.last_time_loop = 0
		self.last_time_headlights = 0
		self.triangle_button = 0 # initializing button state

		# Servo duty values - specific to this robot / servo
		self.servo_0 = 11.9
		self.servo_180 = 3.7
		self.servo_90 = 7.8
		self.duty_per_degree = (self.servo_180 - self.servo_0) / 180
		self.wait_time = 0.6

		# Movement variables
		self.period = 0.1 # Time on for motor control (plan to replace with dt at some point...)
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
		gpio_setup()
		self.en_a_pwm = gpio.PWM(en_a, self.motor_freq)
		self.en_b_pwm = gpio.PWM(en_b, self.motor_freq)
		self.move_servo(0)
		self.move_servo(180)
		self.move_servo(90) # centers servo

	def help(self):
		print()
		print("TANK CONTROLS")
		print("Left Analogue - Move Tank")
		print("Right Analogue - Spin Tank")
		print("Left Arrow - Servo Left")
		print("Right Arrow - Servo Right")
		print("Up Arrow - Servo Forward")
		print("Triangle - Toggle Headlights")
		print("Options - Displays this help menu")
		print()

	def toggle_headlights(self):
		if (time.time() - tank.last_time_headlights) > debounce_time:
			tank.last_time_headlights = time.time()
			if self.headlights_on:
				gpio.output(headlight_r, gpio.LOW)
				gpio.output(headlight_l, gpio.LOW)
				self.headlights_on = False
			elif self.headlights_on == False:
				gpio.output(headlight_r, gpio.HIGH)
				gpio.output(headlight_l, gpio.HIGH)
				self.headlights_on = True

	def get_loop_time(self):
		self.dt = time.time() - self.last_time_loop
		self.last_time_loop = time.time()
		return("Loop time: {}s".format(self.dt))

	def move_servo(self, angle):
		duty = self.servo_0 + (angle * self.duty_per_degree)
		self.servo_pwm = gpio.PWM(servo_pin, 50) # servo freq = 50Hz (from youtube video)
		self.servo_pwm.start(duty)
		time.sleep(self.wait_time)
		self.servo_pwm.stop()

	def process_input(self): # decides whether to move or spin or do nothing
		if (abs(self.joy_x_l) > 0) or (abs(self.joy_y_l) > 0):
			# left stick is away from origin -> regular movement
			# regular movement code...
			self.move()
			self.last_movement = "move" # might want to move this to the move method...
			# left stick is at origin -> check if right stick has moved
		elif abs(self.joy_x_r) > 0:
			# right stick is away from origin -> spin movement
			# spin movement code...
			self.spin()
			self.last_movement = "spin"
		else:
			self.pwm_a = 0
			self.pwm_b = 0
			self.move(stopped=True) # Stopped indicates pwm override (updates system to stopped state)


	def move(self, stopped=False):
		if not stopped:
			self.pwm_a, self.pwm_b = self.joy_2_pwm_move()
		# get general direction from joystick
		if self.joy_y_l < 0:
			move_direction = self.forwards
			self.pwm_a = abs(self.pwm_a)
			self.pwm_b = abs(self.pwm_b)
		elif self.joy_y_l > 0:
			move_direction = self.backwards
			self.pwm_a = abs(self.pwm_a)
			self.pwm_b = abs(self.pwm_b)
		else:
			move_direction = self.stopped # shouldn't be necessary.
		if verbose_mode:
			print("")
			print("Direction: {}".format(move_direction[0]))
			print("Motor mix A: {}".format(self.pwm_a))
			print("Motor mix B: {}".format(self.pwm_b))
			print("")
		if (self.last_movement == "move") and (move_direction == self.last_move_direction):
			self.en_a_pwm.ChangeDutyCycle(self.pwm_a)
			self.en_b_pwm.ChangeDutyCycle(self.pwm_b)
		elif move_direction != 0:
			self.en_a_pwm.start(self.pwm_a)
			self.en_b_pwm.start(self.pwm_b)
			gpio.output(in_1, move_direction[1])
			gpio.output(in_2, move_direction[2])
			gpio.output(in_3, move_direction[3])
			gpio.output(in_4, move_direction[4])
			self.last_move_direction = move_direction
		time.sleep(self.period)

	def joy_2_pwm_move(self):
		if self.joy_y_l < 0: # y-axis is inverted so negative value is forward
			if self.joy_x_l >= 0:
				mot_premix_l = 1.0 # 1.0 is max joystick value
				mot_premix_r = 1.0 - self.joy_x_l
			else:
				mot_premix_l = 1.0 + self.joy_x_l
				mot_premix_r = 1.0
		elif self.joy_y_l > 0: # backwards
			if self.joy_x_l >= 0:
				mot_premix_l = 1.0 - self.joy_x_l
				mot_premix_r = 1.0
			else:
				mot_premix_l = 1.0
				mot_premix_r = 1.0 + self.joy_x_l
		else:
			mot_premix_l = 0
			mot_premix_r = 0

		# Scale drive output due to joystick y (throttle)
		mot_premix_l = mot_premix_l * (self.joy_y_l / 1.0)
		mot_premix_r = mot_premix_r * (self.joy_y_l / 1.0)

		# Calculate pivot amount
		# - Strength of pivot (piv_speed) due to joystick x
		# - Blending of pivot vs drive (piv_scale) due to joystick y
		piv_speed = abs(self.joy_x_l)
		if abs(self.joy_y_l) > self.piv_y_limit: # might change to a piv_x_limit instead - could give smoother results...
			piv_scale = 0.0
		else:
			piv_scale = (1.0 - (abs(self.joy_y_l)/self.piv_y_limit))

		# Calculate final mix of drive and pivot
		mot_mix_l = ((1.0 - piv_scale) * mot_premix_l) + (piv_scale * piv_speed)
		mot_mix_r = ((1.0 - piv_scale) * mot_premix_r) + (piv_scale * piv_speed)

		mot_mix_l = mot_mix_l * self.top_speed
		mot_mix_r = mot_mix_r * self.top_speed

		return mot_mix_l, mot_mix_r

	def spin(self):
		self.pwm_a, self.pwm_b = self.joy_2_pwm_spin()
		if self.joy_x_r > 0:
			spin_direction = self.spin_right
		elif self.joy_x_r < 0:
			spin_direction = self.spin_left
		else:
			spin_direction = self.stopped
		if verbose_mode:
			print("")
			print("Direction: {}".format(spin_direction[0]))
			print("Motor mix A: {}".format(self.pwm_a))
			print("Motor mix B: {}".format(self.pwm_b))
			print("")
		if  (self.last_movement == "spin") and (spin_direction == self.last_spin_direction):
			self.en_a_pwm.ChangeDutyCycle(self.pwm_a)
			self.en_b_pwm.ChangeDutyCycle(self.pwm_b)
		elif spin_direction != 0:
			self.en_a_pwm.start(self.pwm_a)
			self.en_b_pwm.start(self.pwm_b)
			gpio.output(in_1, spin_direction[1])
			gpio.output(in_2, spin_direction[2])
			gpio.output(in_3, spin_direction[3])
			gpio.output(in_4, spin_direction[4])
			self.last_spin_direction = spin_direction
		time.sleep(self.period/2)

	def joy_2_pwm_spin(self):
		speed_factor = abs(self.joy_x_r)
		mot_mix_l = speed_factor * self.top_speed
		mot_mix_r = speed_factor * self.top_speed

		return  mot_mix_l, mot_mix_r


def gpio_setup(): # might change this to use the same gpio mode as OLED... (could include an optional parameter for this!)
	gpio.setmode(gpio.BOARD)
	gpio.setup(in_1, gpio.OUT)
	gpio.setup(in_2, gpio.OUT)
	gpio.setup(in_3, gpio.OUT)
	gpio.setup(in_4, gpio.OUT)
	gpio.setup(en_a, gpio.OUT)
	gpio.setup(en_b, gpio.OUT)
	gpio.setup(trig, gpio.OUT)
	gpio.setup(echo, gpio.IN)
	gpio.setup(servo_pin, gpio.OUT)
	gpio.setup(enc_La, gpio.IN, pull_up_down = gpio.PUD_DOWN)
	gpio.setup(enc_Lb, gpio.IN, pull_up_down = gpio.PUD_DOWN)
	gpio.setup(enc_Ra, gpio.IN, pull_up_down = gpio.PUD_DOWN)
	gpio.setup(enc_Rb, gpio.IN, pull_up_down = gpio.PUD_DOWN)
	gpio.setup(headlight_l, gpio.OUT)
	gpio.setup(headlight_r, gpio.OUT)

def joystick_values(joystick):
	print("")
	# Get the name from the OS for the controller/joystick
	name = joystick.get_name()
	print("Joystick name: {}".format(name))

	axes = joystick.get_numaxes()
	print("Number of axes: {}".format(axes))

	for i in range(axes):
		axis = joystick.get_axis(i)
		print("Axis {} value: {:>6.3f}".format(i, axis))

	buttons = joystick.get_numbuttons()
	print("Number of buttons: {}".format(buttons))

	for i in range(buttons):
		button = joystick.get_button(i)
		print("Button {:>2} value: {}".format(i, button))
	# Hat switch. All or nothing for direction, not like joysticks.
	# Value comes back in an array.
	hats = joystick.get_numhats()
	print("Number of hats: {}".format(hats))

	for i in range(hats):
		hat = joystick.get_hat(i)
		print("Hat {} value: {}".format(i, str(hat)))
	print("")

if __name__ == '__main__':
	tank = robot()
	while done==False: # CONTROL LOOP
		try:
			# EVENT PROCESSING STEP
			for event in pygame.event.get(): # User did something
				if event.type == pygame.QUIT: # If user clicked close
					done=True # Flag that we are done so we exit this loop (not really used in this code atm...)

				# Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBU$
				if event.type == pygame.JOYBUTTONDOWN:
					print("Joystick button pressed.")
				if event.type == pygame.JOYBUTTONUP:
					print("Joystick button released.")


			# Get count of joysticks
			joystick_count = pygame.joystick.get_count()

			# For each joystick:
			for i in range(joystick_count):
				joystick = pygame.joystick.Joystick(i)
				joystick.init()
				if debug_mode:
					joystick_values(joystick)

				tank.joy_x_l = joystick.get_axis(0) # get horizontal data for left analogue
				tank.joy_y_l = joystick.get_axis(1) # get vertical data for left analogue
				tank.joy_x_r = joystick.get_axis(2) # get horizontal data for right analogue

		
				# act on these joystick and button values
				tank.process_input()

				servo_hats = joystick.get_hat(0)
				if servo_hats == (-1,0):
					tank.move_servo(0)
				elif servo_hats == (1,0):
					tank.move_servo(180)
				elif servo_hats == (0,1):
					tank.move_servo(90)

				tank.triangle_button = joystick.get_button(3)
				if tank.triangle_button == 1:
					tank.toggle_headlights() # includes debounce code in method

				print(tank.get_loop_time())

			# ALL CODE IN CONTROL LOOP SHOULD GO ABOVE THIS COMMENT

			#time.sleep(1) # for debugging purposes

		except KeyboardInterrupt as e:
			gpio.cleanup()
			pygame.quit()
			sys.exit(1)

	gpio.cleanup() # just in case pygame quits
