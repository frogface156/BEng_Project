import models_all_values
import numpy as np
from Config import Config
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

graph_path = Config['logging']['graph_file_path']
extension = Config['logging']['graph_extension']

init_s = Config['test']['initial_state']
x = np.array([[init_s['x_0'], init_s['vx_0'], init_s['y_0'], init_s['vy_0'], init_s['theta_0']]]).T

oss = models_all_values.OdometryStateSpace()

folder_path = "/home/pi/BEng_Project/sensor_tests/data/odometry/"
read_file_name = "supplemented_encoder_data"
write_file = "/home/pi/BEng_Project/sensor_tests/data/odometry/test_1/output.csv"
extension = ".csv"

read_file_path = folder_path + read_file_name + extension


ticks = []
states = []

def clear_file(file):
	with open(file, "w") as f:
		writer = csv.writer(f)

def log_data(file, data):
	with open(file, "a") as f:
		writer = csv.writer(f)
		writer.writerow(data)

with open(read_file_path, "r") as f:
	reader = csv.reader(f)
	for row in reader:
		ticks.append((int(row[0]), int(row[1]), float(row[2])))

clear_file(write_file)
for (l, r, theta) in ticks:
	x, values = oss.measure_state(x, l, r)
	x[4][0] = theta
	states.append(x)
	values.append(theta)
	log_data(write_file, values)

