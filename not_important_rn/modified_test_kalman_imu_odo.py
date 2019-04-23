import kalman
import numpy as np
import sensors
import models
import random
from Config import Config
from pygame.time import Clock
import imu_sensor
import encoders
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

# Sensors
imu = sensors.IMU()
enc = sensors.Encoders()

# Models
rss = models.RobotStateSpace()
iss = models.IMUStateSpace()
oss = models.OdometryStateSpace()

x_predictions, x_corrections, x_imu_measurements, x_odo_measurements = [], [], [], []
y_predictions, y_corrections, y_imu_measurements, y_odo_measurements = [], [], [], []
theta_predictions, theta_corrections, theta_imu_measurements, theta_odo_measurements = [], [], [], []

N = 500

imu_a_x = 0
imu_a_y = 0

clock = Clock()
print("Starting...")
for i in range(N):
	enc_l, enc_r = enc.get_ticks()
	z_o = oss.measure_state(x, enc_l, enc_r)
	x_odo_measurements.append(z_o[0][0])
	y_odo_measurements.append(z_o[2][0])
	theta_odo_measurements.append(z_o[4][0])
	imu_theta = imu.euler[0]
	z_i = iss.measure_state(x, imu_a_x, imu_a_y, imu_theta) # acc provided in m/s^2, theta provided in degrees (model converts these)
	x_imu_measurements.append(z_i[0][0])
	y_imu_measurements.append(z_i[2][0])
	theta_imu_measurements.append(z_i[4][0])
	imu_a_x = imu.linear_acceleration[2] # using the z-axis because x-axis is faulty...
	imu_a_y = imu.linear_acceleration[1] 
	x, P = kalman.predict(x, P, A, Q)
	x_predictions.append(x[0][0])
	y_predictions.append(x[2][0])
	theta_predictions.append(x[4][0])
	x, P = kalman.update(x, P, z_i, H_i, R_i)
	x, P = kalman.update(x, P, z_o, H_o, R_o)
	x_corrections.append(x[0][0])
	y_corrections.append(x[2][0])
	theta_corrections.append(x[4][0])

	clock.tick(freq)

print("Final Estimated State: {}".format(x))
print("Final State Covariance: {}".format(P))


def draw_plot(predictions, odo_meas, imu_meas, corrections, state='x'):
	plt.plot(predictions, label='{} State Prediction'.format(state))
	plt.plot(odo_meas, label='{} Odometry Measurement'.format(state))
	plt.plot(imu_meas, label='{} IMU Measurement'.format(state))
	plt.plot(corrections, label='{} Correction'.format(state))
	plt.legend()
	plt.title("Kalman Filter - IMU and Odometry - {}".format(state))

	save_name = "KF_IMU_odo_test_{}".format(state)
	plt.savefig(graph_path + save_name + extension)

def draw_scatter(x, y):
	plt.scatter(x, y)
	plt.title("Kalman Filter - IMU and Odometry - Optimally Estimated Position")
	save_name = "KF_IMU_odo_scatter"
	plt.savefig(graph_path + save_name + extension)

draw_plot(x_predictions, x_odo_measurements, x_imu_measurements, x_corrections, state='x') # should be able to spot any clear errors here...
draw_plot(y_predictions, y_odo_measurements, y_imu_measurements, y_corrections, state='y') # should be able to spot any clear errors here...
draw_plot(theta__predictions, theta_odo_measurements, theta_imu_measurements, theta_corrections, state='theta') # should be able to spot any clear errors here...
draw_scatter(x_corrections, y_corrections) # estimated position over time,  play with the covariances