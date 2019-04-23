import csv
import numpy as np

import models
from Config import Config

read_file = "/home/pi/BEng_Project/sensor_tests/data/raw_sensor_data/straight/raw_data_imu_odo_1.csv"
write_file = "/home/pi/BEng_Project/sensor_tests/analysis/odometry/odometry_test.csv"

with open(write_file, 'w') as f:
	writer = csv.writer(f)

init = Config['test']['initial_state']
x = np.array([[init['x_0'], init['vx_0'], init['y_0'], init['vy_0'], init['theta_0']]]).T

oss = models.OdometryStateSpace()

ticks = []


with open(read_file, 'r') as f:
	reader = csv.reader(f)
	for row in reader:
		ticks.append((int(row[0]), int(row[1])))

def log_data(file, row):
	with open(file, 'a') as f:
		writer = csv.writer(f)
		writer.writerow(row)

for l, r in ticks:
	l, r = oss.clean_input(l, r)
	x = oss.measure_state(x, l, r)
	data = [x[0][0], x[1][0], x[2][0], x[3][0], x[4][0]]
	log_data(write_file, data)
