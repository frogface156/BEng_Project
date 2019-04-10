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

N = 200

imu_a_x = 0
imu_a_y = 0

clock = Clock()
print("Starting...")
for i in range(N):
	enc_l, enc_r = enc.get_ticks()
	z_o = oss.measure_state(x, enc_l, enc_r)
	x_odo_measurements.append(z_o[0][0])
	y_odo_measurements.append(z_o[2][0])
	imu_theta = imu.euler[0]
	z_i = iss.measure_state(x, imu_a_x, imu_a_y, imu_theta)
	x_imu_measurements.append(z_i[0][0])
	y_imu_measurements.append(z_i[2][0])
	x, P = kalman.predict(x, P, A, Q)
	x_predictions.append(x[0][0])
	y_predictions.append(x[2][0])
	x, P = kalman.update(x, P, z_i, H_i, R_i)
	x, P = kalman.update(x, P, z_o, H_o, R_o)
	x_corrections.append(x[0][0])
	y_corrections.append(x[2][0])

	imu_a_x = imu.linear_acceleration[0]
	imu_a_y = imu.linear_acceleration[1]

	clock.tick(freq)

plt.plot(x_predictions, label='X State Prediction')
plt.plot(x_odo_measurements, label='X Odometry Measurement')
plt.plot(x_imu_measurements, label='X IMU Measurement')
plt.plot(x_corrections, label='X Correction')
plt.legend()
plt.title("Kalman Filter - IMU and Odometry Test - X")

save_name_x = "KF_IMU_Odo_test_x"
plt.savefig(graph_path + save_name_x + extension)

plt.plot(y_predictions, label='Y State Prediction')
plt.plot(y_odo_measurements, label='Y Odometry Measurement')
plt.plot(y_imu_measurements, label='Y IMU Measurement')
plt.plot(y_corrections, label='Y Correction')
plt.legend()
plt.title("Kalman Filter - IMU and Odometry Test - Y")

save_name_y = "KF_IMU_Odo_test_y"
plt.savefig(graph_path + save_name_y + extension)
