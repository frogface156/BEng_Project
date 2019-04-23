import numpy as np
from Config import Config

freq = Config['pygame']['fast_loop_freq']
dt = 1 / freq

class IMUStateSpace(object):
	def __init__(self):
		self.sig_x2 = Config['imu']['sig_z2'] # using the z-axis (more reliable)
		self.sig_y2 = Config['imu']['sig_y2']
		self.sig_theta2 = np.radians(Config['imu']['sig_theta2'])

		self.x_bias = Config['imu']['z_bias'] # using the z-axis (more reliable)
		self.y_bias = Config['imu']['y_bias']
		self.theta_bias = Config['imu']['theta_bias'] # degrees (processed before radians conversion)

		self.x_thresh = Config['imu']['x_thresh']
		self.y_thresh = Config['imu']['y_thresh']
		self.theta_thresh = Config['imu']['theta_thresh']

		self.a_xi_prev = 0
		self.a_yi_prev = 0
		self.theta_i_prev = 0

		self.A = np.array([[1, dt, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, dt, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 0]])
		self.B = np.array([[0.5*dt**2, 0, 0], [dt, 0, 0], [0, 0.5*dt**2, 0], [0, dt, 0], [0, 0, 1]])

		self.W = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]) # World Frame transition matrix

		self.H = np.array([[1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]])
#		self.R = np.array([[0.5*(dt**2)*self.sig_x2, 0, 0, 0, 0], [0, dt*self.sig_x2, 0, 0, 0], [0, 0, 0.5*(dt**2)*self.sig_y2, 0, 0], [0, 0, 0, dt*self.sig_y2, 0], [0, 0, 0, 0, self.sig_theta2]])
		self.R = np.array([[999, 0, 0, 0, 0], [0, 999, 0, 0, 0], [0, 0, 999, 0, 0], [0, 0, 0, 999, 0], [0, 0, 0, 0, self.sig_theta2]]) # artificial values, from educated guess

	def clean_input(self, a_xi, a_yi, theta_i):
		if abs(theta_i - self.theta_i_prev) > self.theta_thresh:
			theta_i = self.theta_i_prev
		else:
			self.theta_i_prev = theta_i
		if abs(a_xi - self.a_xi_prev) > self.x_thresh:
			a_xi = self.a_xi_prev
		else:
			self.a_xi_prev = a_xi
		if abs(a_yi - self.a_yi_prev) > self.y_thresh:
			a_yi = self.a_yi_prev
		else:
			self.a_yi_prev = a_yi

		return a_xi, a_yi, theta_i

	def measure_state(self, x, a_xi, a_yi, theta_i):
		# Raw values - removing bias, converting to correct units and convention directions
		a_xi = (a_xi - self.x_bias) * 1000 # Acc in IMU frame in mm/s^2
		a_yi = -1 * (a_yi - self.y_bias) * 1000 # Acc in decided IMU frame y +ve is left, x +ve is forwards
		theta_i = (-1 * np.radians(theta_i - self.theta_bias)) % (2*np.pi) # converted to radians and converted to world frame i.e. anticlockwise is +ve

		u_i = np.array([[a_xi, a_yi, theta_i]]).T # acceleration and theta in IMU frame

		cos_ti = np.cos(theta_i)
		sin_ti = np.sin(theta_i)

		self.W[0, 0] = cos_ti # update World transition matrix with new values
		self.W[0, 1] = -sin_ti
		self.W[1, 0] = sin_ti
		self.W[1, 1] = cos_ti

#		self.R[0, 0] = 0.5*(dt**2) * ((self.sig_x2 * cos_ti) - (self.sig_y2 * sin_ti))
#		self.R[1, 1] = dt * ((self.sig_x2 * cos_ti) - (self.sig_y2 * sin_ti))
#		self.R[2, 2] = 0.5*(dt**2) * ((self.sig_x2 * sin_ti) + (self.sig_y2 * cos_ti))
#		self.R[3, 3] = dt * ((self.sig_x2 * sin_ti) + (self.sig_y2 * cos_ti))

		u_w = np.dot(self.W, u_i) # Put acceleration and theta in world frame
		#u_w = u_i
		z = np.dot(self.A, x) + np.dot(self.B, u_w)

		return z


class OdometryStateSpace(object):
	def __init__(self):
		self.sig_position2 = Config['odometry']['sig_position2']
		self.sig_velocity2 = Config['odometry']['sig_velocity2']
		self.sig_theta2 = Config['odometry']['sig_theta2']
		self.b = Config['odometry']['wheel_base']
		self.ticks_to_mm_l = Config['odometry']['ticks_to_mm']
		self.ticks_to_mm_r = Config['odometry']['ticks_to_mm']

		self.l_prev = 0
		self.r_prev = 0
		self.thresh = Config['odometry']['thresh']

		self.H = np.array([[1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]])
		self.R = np.array([[self.sig_position2, 0, 0, 0, 0], [0, self.sig_velocity2, 0, 0, 0], [0, 0, self.sig_position2, 0, 0], [0, 0, 0, self.sig_velocity2, 0], [0, 0, 0, 0, self.sig_theta2]])

	def clean_input(self, l, r):
		if l > self.thresh:
			l = self.l_prev
		else:
			self.l_prev = l
		if r > self.thresh:
			r = self.r_prev
		else:
			self.r_prev = r

		return l, r

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

	def get_obstacles(self, scan, heading): # returns array of obstacles with their widths
		obstacles = []
		for theta, dist in enumerate(scan):
			if dist != 0:
				theta_w = ((heading + np.pi) - np.radians(theta)) % (2*np.pi)
				x_w = dist * np.cos(theta_w)
				y_w = dist * np.sin(theta_w)
				width = np.radians(1) * dist # width = angular resolution * distance
				obstacles.append((x_w, y_w, width))

		return obstacles

class RobotStateSpace(object):
	def __init__(self):
		self.sig_trans2 = Config['robot']['sig_trans2']
		self.Q = self.sig_trans2*np.eye(5) # DUMMY MATRIX - will need to get values from testing
		self.A = np.array([[1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]])
