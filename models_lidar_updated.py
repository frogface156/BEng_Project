import numpy as np
from Config import Config

freq = Config['pygame']['fast_loop_freq']
dt = 1 / freq

class IMUStateSpace(object):
	def __init__(self):
		self.sig_x2 = Config['imu']['sig_x2'] # sig^2 of IMU 'x'_axis accel -> needs converting to world coords and update R for each loop...
		self.sig_y2 = Config['imu']['sig_y2']
		self.sig_theta2 = np.radians(Config['imu']['sig_theta2'])

		self.x_bias = Config['imu']['x_bias']
		self.y_bias = Config['imu']['y_bias']
		self.theta_bias = Config['imu']['theta_bias'] # degrees (processed before radians conversion)

		self.A = np.array([[1, dt, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, dt, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 0]])
		self.B = np.array([[0.5*dt**2, 0, 0], [dt, 0, 0], [0, 0.5*dt**2, 0], [0, dt, 0], [0, 0, 1]])

		self.H = np.array([[1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]])
		self.R = np.array([[0.5*(dt**2)*self.sig_x2, 0, 0, 0, 0], [0, dt*self.sig_x2, 0, 0, 0], [0, 0, 0.5*(dt**2)*self.sig_y2, 0, 0], [0, 0, 0, dt*self.sig_y2, 0], [0, 0, 0, 0, self.sig_theta2]])

	def measure_state(self, x, a_xi, a_yi, theta):
		# Raw values - removing bias, converting to correct units and convention directions
		a_xi = (a_xi - self.x_bias) / 1000 # Acc in IMU frame in mm/s^2
		a_yi = -1 * (a_yi - self.y_bias) / 1000 # Acc in decided IMU frame y +ve is left, x +ve is forwards
		theta_w = (-1 * np.radians(theta - self.theta_bias)) % (2*np.pi) # converted to radians and converted to world frame i.e. anticlockwise is +ve

		cos_tw = np.cos(theta_w)
		sin_tw = np.sin(theta_w)

		self.R[0, 0] = 0.5*(dt**2) * ((self.sig_x2 * cos_tw) - (self.sig_y2 * sin_tw))
		self.R[1, 1] = dt * ((self.sig_x2 * cos_tw) - (self.sig_y2 * sin_tw))
		self.R[2, 2] = 0.5*(dt**2) * ((self.sig_x2 * sin_tw) + (self.sig_y2 * cos_tw))
		self.R[3, 3] = dt * ((self.sig_x2 * sin_tw) + (self.sig_y2 * cos_tw))

		a_xw = (a_xi * cos_tw) - (a_yi * sin_tw))  # Acc in World Frame
		a_yw = (a_xi * sin_tw) + (a_yi * cos_tw)
		u = np.array([[a_xw, a_yw, theta_w]]).T

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

	def get_radius(self, l, alpha):
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
			rad = self.get_radius(l, alpha)
			theta_p = (theta + alpha) % (2*np.pi)
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

	def get_obstacles(self, scan, heading): # returns array of obstacles with their widths
		obstacles = []
		for theta, dist in enumerate(scan):
			theta_w = ((heading + np.pi) - np.radians(angle)) % (2*np.pi)
			x_w = dist * np.cos(theta_w)
			y_w = dist * np.sin(theta_w)
			width = np.radians(1) * dist # width = angular resolution * distance
			obstacles.append((x, y, width))

		return obstacles
	
class RobotStateSpace(object):
	def __init__(self):
		self.sig_trans2 = Config['robot']['sig_trans2']
		self.Q = self.sig_trans2*np.eye(5) # DUMMY MATRIX - will need to get values from testing
		self.A = np.array([[1, dt, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, dt, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]])
