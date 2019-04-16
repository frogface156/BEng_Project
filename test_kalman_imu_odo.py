import numpy as np
import csv

import models
from Config import Config
import kalman

read_file = "/home/pi/BEng_Project/sensor_tests/data/kalman/raw_data_imu_odo.csv"
write_file = "/home/pi/BEng_Project/sensor_tests/analysis/kalman/kalman_test.csv"

with open(write_file, 'w') as f:
	writer = csv.writer(f)

imu_input = []
odo_input = []

with open(read_file, 'r') as f:
	reader = csv.reader(f)
	for row in reader:
		imu_input.append((float(row[2]), float(row[3]), float(row[4])))

with open(read_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
                odo_input.append((int(row[0]), int(row[1])))

init_s = Config['test']['initial_state']
init_p = Config['test']['initial_probabilities']
x = np.array([[init_s['x_0'], init_s['vx_0'], init_s['y_0'], init_s['vy_0'], init_s['theta_0']]]).T
P = np.array([[init_p['p0_x'], 0, 0, 0, 0], [0, init_p['p0_vx'], 0, 0, 0], [0, 0, init_p['p0_y'], 0, 0], [0, 0, 0, init_p['p0_vy'], 0], [0, 0, 0, 0, init_p['p0_theta']]])

# Models
rss = models.RobotStateSpace()
iss = models.IMUStateSpace()
oss = models.OdometryStateSpace()

imu_a_x = 0
imu_a_y = 0

def log_data(file, data):
	with open(file, "a") as f:
		writer = csv.writer(f)
		writer.writerow(data)


for i in range(len(imu_input)):
	data = []
	l = odo_input[i][0]
	r = odo_input[i][1]
	z_o = oss.measure_state(x, l, r)
	data.append(z_o[0][0])
	data.append(z_o[2][0])
	data.append(z_o[4][0])
	imu_theta = imu_input[i][2]
	z_i = iss.measure_state(x, imu_a_x, imu_a_y, imu_theta)
	imu_a_x = imu_input[i][0]
	imu_a_y = imu_input[i][1]
	data.append(z_i[0][0])
	data.append(z_i[2][0])
	data.append(z_i[4][0])
#	x, P = kalman.predict(x, P, rss.A, rss.Q)
	data.append(x[0][0])
	data.append(x[2][0])
	data.append(x[4][0])
#	x, P = kalman.update(x, P, z_i, iss.H, iss.R)
	x, P = kalman.update(x, P, z_o, oss.H, oss.R)
	data.append(x[0][0])
	data.append(x[2][0])
	data.append(x[4][0])

	log_data(write_file, data)

print("Final Estimated State: {}".format(x))
print("Final State Covariance: {}".format(P))

