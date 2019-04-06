import numpy as np
from Config import Config

sig_x2 = Config['imu']['sig_x2']
sig_y2 = Config['imu']['sig_y2']
sig_theta2 = Config['imu']['sig_theta2']

x_bias = Config['imu']['x_bias']
y_bias = Config['imu']['y_bias']
theta_bias = Config['imu']['theta_bias']

freq = Config['pygame']['fast_loop_freq']
dt = 1 / freq


A = np.array([[1, dt, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, dt, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]])
B = np.array([[0.5*dt**2, 0, 0], [dt, 0, 0], [0, 0.5*dt**2, 0], [0, dt, 0], [0, 0, 1]])

# All states measured
H = np.array([[1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]])
# For R, you need to integrate the error to get velocity error, then again to get position error
R = np.array([[0.5*(dt**2)*sig_x2, 0, 0, 0, 0], [0, dt*sig_x2, 0, 0, 0], [0, 0, 0.5*(dt**2)*sig_y2, 0, 0], [0, 0, 0, dt*sig_y2, 0], [0, 0, 0, 0, sig_theta2]])

def measure_state(x, a_x, a_y, theta):
	a_x = (a_x - x_bias) / 1000 # in mm/s^2
	a_y = (a_y - y_bias) / 1000 # in mm/s^2
	theta = ((theta - theta_bias) * np.pi / 180) % 2*np.pi # in radians (0 <= theta < 2pi)

	u = np.array([[a_x, a_y, theta]]).T

	z = np.dot(A, x) + np.dot(B, u)

	return z
