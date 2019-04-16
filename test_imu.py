import csv
import numpy as np

import models
from Config import Config

read_file = "/home/pi/BEng_Project/sensor_tests/data/kalman/raw_data_imu_odo.csv"
write_file = "/home/pi/BEng_Project/sensor_tests/analysis/imu/imu_test.csv"

with open(write_file, 'w') as f:
	writer = csv.writer(f)

init = Config['test']['initial_state']
x = np.array([[init['x_0'], init['vx_0'], init['y_0'], init['vy_0'], init['theta_0']]]).T

iss = models.IMUStateSpace()

imu_input = []


with open(read_file, 'r') as f:
	reader = csv.reader(f)
	for row in reader:
		imu_input.append((float(row[2]), float(row[3]), float(row[4])))

def log_data(file, row):
	with open(file, 'a') as f:
		writer = csv.writer(f)
		writer.writerow(row)

for a_xi, a_yi, theta_i in imu_input:
	a_xi, a_yi, theta_i = iss.clean_input(a_xi, a_yi, theta_i)
	x = iss.measure_state(x, a_xi, a_yi, theta_i)
	data = [x[0][0], x[1][0], x[2][0], x[3][0], x[4][0]]
	log_data(write_file, data)
