from math import sin, cos, pi, atan2
import numpy as np

class ExtendedKalmanFilter():
	def __init__(self, state, covariance,
			robot_width, scanner_displacement,
			control_motion_factor, control_turn_factor,
			measurement_distance_stddev, measurement_angle_stddev):
		# State
		self.state = state
		self.covariance = covariance

		# Constants
		self.robot_width = robot_width
		self.scanner_displacement = scanner_displacement
		self.control_motion_factor = control_motion_factor
		self.control_turn_factor = control_turn_factor
		self.measurement_distance_stddev = measurement_distance_stddev
		self.measurement_angle_stddev = measurement_angle_stddev

	@staticmethod
	def g(state, control, w):
		x, y, theta = state
		l, r = control
		if l != r:
			alpha = (r - l) / w
			rad = 1 / alpha
			g1 = x + (rad + w/2.) * (sin(theta + alpha) - sin(theta))
			g2 = y + (rad + w/2.) * (-cos(theta + alpha) + cos(theta))
			g3 = (theta + alpha + pi) % (2*pi) - pi
		else: # l == r
			g1 = x + l * cos(theta)
			g2 = y + l * sin(theta)
			g3 = theta

		return np.array([g1, g2, g3])

	@staticmethod
	def dg_dstate(state, control, w): # partial derivative wrt state

		return np.array([1, 2, 3], [4, 5, 6], [7, 8, 9])

	@staticmethod
	def dg_dcontrol(state, control, w): # partial derivative wrt control

		return np.array([1, 2], [3, 4], [5, 6])

	@staticmethod
	def get_error_ellipse(covariance):
		eigenvals, eigenvects = linalg.eig(covariance[0:2, 0:2])
		angle = atan2(eigenvects[1, 0], eigenvects[0, 0])
		return (angle, sqrt(eigenvals[0]), sqrt(eigenvals[1]))

	def predict(self, control):
		# Write code
		pass

	@staticmethod
	def h(state, landmark, scanner_displacement):
		dx = landmark[0] - (state[0] + scanner_displacement * cos(state[2]))
		dy = landmark[1] - (state[1] + scanner_displacement * sin(state[2]))
		r = sqrt(dx * dx + dy * dy)
		alpha = (atan2(dy, dx) - state[2] + pi) % (2*pi) - pi

		return np.array([r, alpha])

	@staticmethod
	def dh_dstate(state, landmark, scanner_displacement):
		# Write code
		pass

	def correct(self, measurement, landmark):
		# Write code
		pass

if __name__ == "__main__":
	# Robot constants
	scanner_displacement = 30 # distance from scanner (being tracked by overhead camera)
	ticks_to_mm = 0.349 # determine this experimentally
	robot_width = 155.0 # determine this experimentally

	# Filter constants
	control_motion_factor = 0.35 # error in motion control - determine experimentally
	control_turn_factor = 0.6 # additional error due to slip when turning - determine experimentally
	measurement_distance_stddev = 200.0 # Distance measurement error of cylinders
	measurement_angle_stddev = 15.0 / 180.0 * pi # Angle measurement error


	# Measured start position - uncomment / edit the following lines when ready
	# start_x, start_y = camera.get_coords()
	# start_theta = IMU.euler[0]
	# state = np.array([start_x, start_y, start_theta])
	initial_state = np.array([0, 0, 0])
	# Covariance at start position - standard deviation of camera coords and IMU angle
	initial_covariance = diag([100.0**2, 100.0**2, (10.0 / 180.0 * pi) ** 2])

	# Instantiate Filter
	kf = ExtendedKalmanFilter(initial_state, initial_covariance,
				robot_width, scanner_displacement,
				control_motion_factor, control_turn_factor,
				measurement_distance_stddev,
				measurement_angle_stddev)

	# Log File Version
	# logfile = logfile.read("motor_count.csv")
	states = []
	covariances = []
	for ticks in logfile: # or ticks = enc.get_ticks()
		# Prediction
		control = np.array(ticks) * ticks_to_mm
		kf.predict(control)

		# Log state
		states.append(kf.state)
		covariances.append(kf.covariance)
