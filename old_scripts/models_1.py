import numpy as np
from Config import Config

freq = Config['pygame']['fast_loop_freq']
dt = 1 / freq

class IMUStateSpace(object):
	def __init__(self):
		self.sig_x2 = Config['imu']['sig_x2']
		self.sig_y2 = Config['imu']['sig_y2']
		self.sig_theta2 = Config['imu']['sig_theta2']

		self.x_bias = Config['imu']['x_bias']
		self.y_bias = Config['imu']['y_bias']
		self.theta_bias = Config['imu']['theta_bias']

		self.A = np.array([[1, dt, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, dt, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]])
		self.B = np.array([[0.5*dt**2, 0, 0], [dt, 0, 0], [0, 0.5*dt**2, 0], [0, dt, 0], [0, 0, 1]])

		self.H = np.array([[1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]])
		self.R = np.array([[0.5*(dt**2)*self.sig_x2, 0, 0, 0, 0], [0, dt*self.sig_x2, 0, 0, 0], [0, 0, 0.5*(dt**2)*self.sig_y2, 0, 0], [0, 0, 0, dt*self.sig_y2, 0], [0, 0, 0, 0, self.sig_theta2]])

	def measure_state(self, x, a_x, a_y, theta):
		a_x = (a_x - self.x_bias) / 1000 # in mm/s^2
		a_y = (a_y - self.y_bias) / 1000
		theta = np.radians(theta - self.theta_bias) % 2*np.pi # radians
		u = np.array([[a_x, a_y, theta]]).T

		z = np.dot(self.A, x) + np.dot(self.B, u)

		return z


class OdometryStateSpace(object):
	def __init__(self):
		self.sig_position2 = Config['odometry']['sig_position2']
		self.sig_theta2 = Config['odometry']['sig_theta2']
		self.b = Config['odometry']['wheel_base']
		self.ticks_to_mm_l = Config['odometry']['ticks_to_mm']
		self.ticks_to_mm_r = Config['odometry']['ticks_to_mm']

		self.H = np.array([[1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]])
		self.R = np.array([[self.sig_position2, 0, 0, 0, 0], [0, self.sig_position2, 0, 0, 0], [0, 0, self.sig_position2, 0, 0], [0, 0, 0, self.sig_position2, 0], [0, 0, 0, 0, self.sig_theta2]])

	def ticks_to_mm(self, l_ticks, r_ticks):
		l_mm = l_ticks * self.ticks_to_mm_l
		r_mm = r_ticks * self.ticks_to_mm_r

		return l_mm, r_mm

	def get_alpha(self, l, r):
		alpha = (r - l) / self.b

		return alpha

	def get_radius(self, alpha, l):
		rad = l / alpha # "L" not "One"

		return rad

	def measure_state(self, x, l, r):
		l, r = self.ticks_to_mm(l, r)
		theta = x[4][0] # [[x, vx, y, vy, theta]]
		x_old = x[0][0]
		y_old = x[2][0]
		if l == r:
			x_p = x_old + l * np.cos(theta) # theta_prime = theta (so save computation...)
			y_p = y_old + l * np.sin(theta)
			vx_p = (x_p - x_old) / dt
			vy_p = (y_p - y_old) / dt
			z = np.array([[x_p, vx_p, y_p, vy_p, theta]]).T

			return z

		else: # l != r
			alpha = self.get_alpha(l, r)
			rad = self.get_radius(alpha, l)
			theta_p = (theta + alpha) % 2*np.pi
			transposition = rad + (self.b / 2)
			x_p = x_old + transposition * (np.sin(theta_p) - np.sin(theta))
			y_p = y_old - transposition * (np.cos(theta_p) - np.cos(theta))
			vx_p = (x_p - x_old) / dt
			vy_p = (y_p - y_old) / dt
			z = np.array([[x_p, vx_p, y_p, vy_p, theta_p]]).T

			return z

class LidarStateSpace(object):
	def __init__(self):
		self.sig_position2 = Config['lidar']['sig_position2']
		self.H = np.array([[1, 0, 0, 0, 0], [0, 0, 1, 0, 0]])
		self.R = np.array([[self.sig_position2, 0], [0, self.sig_position2]])
		self.radians = self.get_radians_array() # don't want to compute this each time...

	def get_point_coords(self, scan):
		point_coords = []
		for i, dist in enumerate(scan):
			x = -1 * dist * np.sin(self.radians[i])
			y = -1 * dist * np.cos(self.radians[i])
			point_coords.append((x, y))

		return point_coords # list of (x, y) tuples

	def get_obstacles(self, scan): # similar to get_point_coords() but includes obstacle width based on angle and distance
		obstacles = []
		for i, dist in enumerate(scan):
			x = -1 * dist * np.sin(self.radians[i])
			y = -1 * dist * np.cos(self.radians[i])
			width = np.radians(1) * dist # l*theta (theta = resolution = 1 deg)
			obstacles.append((x, y, width))

		return obstacles # list of (x, y, width) tuples

	@staticmethod
	def get_radians_array():
		radians = []
		for i in range(360):
			radians.append(np.radians(i))

		return radians

class RobotStateSpace(object):
	def __init__(self):
		self.sig_trans2 = Config['robot']['sig_trans2']
		self.Q = self.sig_trans2*np.eye(5) # DUMMY MATRIX - will need to get values from testing
		self.A = np.array([[1, dt, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, dt, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]])
