import kalman
import numpy as np
import random
from Config import Config
import robot_state_space as rss
import imu_state_space as iss
from pygame.time import Clock
import imu_sensor
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


graph_path = Config['logging']['graph_file_path']
extension = Config['logging']['graph_extension']

freq = Config['pygame']['fast_loop_freq']
dt = 1 / freq

init_s = Config['test']['initial_state']
init_p = Config['test']['initial_probabilities']
x = np.array([[init_s['x_0'], init_s['vx_0'], init_s['y_0'], init_s['vy_0'], init_s['theta_0']]]).T
P = np.array([[init_p['p0_x'], 0, 0, 0, 0], [0, init_p['p0_vx'], 0, 0, 0], [0, 0, init_p['p0_y'], 0, 0], [0, 0, 0, init_p['p0_vy'], 0], [0, 0, 0, 0, init_p['p0_theta']]])

# Robot
Q = rss.Q
A = rss.A

# IMU
H_i = iss.H
R_i = iss.R

imu = imu_sensor.IMU()

x_predictions, x_corrections, x_measurements = [], [], []
y_predictions, y_corrections, y_measurements = [], [], []

N = 200

imu_a_x = 0
imu_a_y = 0

clock = Clock()
print("Starting...")
for i in range(N):
	imu_theta = imu.euler[0]
	z_i = iss.measure_state(x, imu_a_x, imu_a_y, imu_theta)
	x_measurements.append(z_i[0][0])
	y_measurements.append(z_i[2][0])
	x, P = kalman.predict(x, P, A, Q)
	x_predictions.append(x[0][0])
	y_predictions.append(x[2][0])
	x, P = kalman.update(x, P, z_i, H_i, R_i)
	x_corrections.append(x[0][0])
	y_corrections.append(x[2][0])

	imu_a_x = imu.linear_acceleration[0]
	imu_a_y = imu.linear_acceleration[1]

	clock.tick(freq)

plt.plot(x_predictions, label='State Prediction')
plt.plot(x_measurements, label='Odometry Measurement')
plt.plot(x_corrections, label='Odometry Correction')
plt.legend()
plt.title("Kalman Filter - Odometry Test")

save_name = "KF_IMU_test"
plt.savefig(graph_path + save_name + extension)
