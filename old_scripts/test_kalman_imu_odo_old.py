import kalman
import numpy as np
import sensors
import models
from Config import Config
from pygame.time import Clock
import csv

graph_path = Config['logging']['graph_file_path']
extension = Config['logging']['graph_extension']
data_path = "/home/pi/BEng_Project/sensor_tests/data/kalman/"
data_file_name = "kalman_data.csv"
data_file = data_path + data_file_name

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

N = 300

imu_a_x = 0
imu_a_y = 0

def log_data(file, data):
	with open(file, "a") as f:
		writer = csv.writer(f)
		writer.writerow(data)


clock = Clock()
print("Starting...")
for i in range(N):
	data = []
	enc_l, enc_r = enc.get_ticks()
	z_o = oss.measure_state(x, enc_l, enc_r)
	data.append(z_o[0][0])
	data.append(z_o[2][0])
	data.append(z_o[4][0])
	imu_theta = imu.euler[0]
	z_i = iss.measure_state(x, imu_a_x, imu_a_y, imu_theta) # acc provided in m/s^2, theta provided in degrees (model converts these)
	imu_a_x = imu.linear_acceleration[2] # using the z-axis because x-axis is faulty...
	imu_a_y = imu.linear_acceleration[1] 
	data.append(z_i[0][0])
	data.append(z_i[2][0])
	data.append(z_i[4][0])
	x, P = kalman.predict(x, P, rss.A, rss.Q)
	data.append(x[0][0])
	data.append(x[2][0])
	data.append(x[4][0])
	x, P = kalman.update(x, P, z_i, iss.H, iss.R)
	x, P = kalman.update(x, P, z_o, oss.H, oss.R)
	data.append(x[0][0])
	data.append(x[2][0])
	data.append(x[4][0])

	log_data(data_file, data)

	clock.tick(freq)

print("Final Estimated State: {}".format(x))
print("Final State Covariance: {}".format(P))

