import csv
import numpy as np

import models
from Config import Config

read_file = "/home/pi/BEng_Project/sensor_tests/data/kalman/raw_data_imu_odo.csv"
write_file = "/home/pi/BEng_Project/sensor_tests/analysis/odometry/odometry_supp_test.csv"

with open(write_file, 'w') as f:
	writer = csv.writer(f)

init = Config['test']['initial_state']
x = np.array([[init['x_0'], init['vx_0'], init['y_0'], init['vy_0'], init['theta_0']]]).T

oss = models.OdometryStateSpace()
iss = models.IMUStateSpace()

odo_supp_input = []

with open(read_file, 'r') as f:
	reader = csv.reader(f)
	for row in reader:
		odo_supp_input.append((int(row[0]), int(row[1]), float(row[4])))

def log_data(file, row):
	with open(file, 'a') as f:
		writer = csv.writer(f)
		writer.writerow(row)

a_xi = 0
a_yi = 0

for l, r, theta_i in odo_supp_input:
	l, r = oss.clean_input(l, r)
	theta_i = (-1 * np.radians(theta_i - iss.theta_bias)) % (2*np.pi)
	x = oss.measure_state(x, l, r)
	x[4][0] = theta_i
	data = [x[0][0], x[1][0], x[2][0], x[3][0], x[4][0]]
	log_data(write_file, data)
