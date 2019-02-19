from math import sin, cos, pi
import numpy as np

class ExtendedKalmanFilter():

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

if __name__ == "__main__":
	ticks_to_mm = 0.349 # determine this experimentally
	robot_width = 155.0 # determine this experimentally

	# Measured start position - uncomment / edit the following lines when ready
	# start_x, start_y = camera.get_coords()
	# start_theta = IMU.euler[0]
	# state = np.array([start_x, start_y, start_theta])
	state = np.array([0, 0, 0])

	# Log File Version
	# logfile = logfile.read("motor_count.csv")
	# states = []
	# for ticks in logfile: # or ticks = enc.get_ticks()
		# Prediction
		# control = np.array(ticks) * ticks_to_mm
		# state = ExtendedKalmanFilter.g(state, control, robot_width)

		# Log state
		# states.append(state)
