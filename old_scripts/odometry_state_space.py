import numpy as np
from Config import Config


# how does the error in the encoders propogate?
sig_position2 = Config['odometry']['sig_position2']
sig_theta2 = Config['odometry']['sig_theta2']
width = Config['odometry']['width']
ticks_to_mm_factor = Config['odometry']['ticks_to_mm']

freq = Config['pygame']['fast_loop_freq']
dt = 1 / freq

H = np.array([[1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]]) # x, y, theta - look at deriving x', y'
R = np.array([[sig_position2, 0, 0, 0, 0], [0, sig_position2, 0, 0, 0], [0, 0, sig_position2, 0, 0], [0, 0, 0, sig_position2, 0], [0, 0, 0, 0, sig_theta2]])

def get_alpha(l, r):
	alpha = (r - l) / width

	return alpha

def get_radius(alpha, l):
	rad = l / alpha # "L" not "One"

	return rad

def measure_state(x, l, r): # return z (i.e. x, y, theta) and maybe derive x', y'
	if l == r:
		l, r = ticks_to_mm(l, r)
		theta = x[4][0]
		x_old = x[0][0]
		y_old = x[2][0]
		new_theta = theta
		x_prime = x_old + l * np.cos(new_theta)
		y_prime = y_old + l * np.sin(new_theta)
		vx_prime = (x_prime - x_old) / dt
		vy_prime = (y_prime - y_old) / dt
		z = np.array([[x_prime, vx_prime, y_prime, vy_prime, new_theta]]).T

		return z
	else:
		l, r = ticks_to_mm(l, r)
		theta = x[4][0]
		x_old = x[0][0]
		y_old = x[2][0]
		alpha = get_alpha(l, r)
		rad = get_radius(alpha, l)
		new_theta = (theta + alpha) % 2*np.pi
		transposition = rad + (width / 2)
		x_prime = x_old + transposition * (np.sin(new_theta) - np.sin(theta))
		y_prime = y_old + transposition * (np.cos(theta) - np.cos(new_theta))
		vx_prime = (x_prime - x_old) / dt
		vy_prime = (y_prime - y_old) / dt
		z = np.array([[x_prime, vx_prime, y_prime, vy_prime, new_theta]]).T

		return z

def ticks_to_mm(l_ticks, r_ticks):
	l_mm = l_ticks * ticks_to_mm_factor
	r_mm = r_ticks * ticks_to_mm_factor

	return l_mm, r_mm
