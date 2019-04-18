import models
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

oss = models.OdometryStateSpace()

folder_path = "/home/pi/BEng_Project/sensor_tests/data/odometry/"
read_file_name = "sample_encoder_data"
write_file_name = "state_data_from_sample"
extension = ".csv"

read_file_path = folder_path + read_file_name + extension
write_file_path = folder_path + write_file_name + extension

ticks = []
states = []

with open(read_file_path, "r") as f:
	reader = csv.reader(f)
	for row in reader:
		ticks.append((int(row[0]), int(row[1])))

for (l, r) in ticks:
	x = oss.measure_state(x, l, r)
	states.append(x)


def clear_file(file_path):
	with open(file_path, "w") as f:
		writer = csv.writer(f)
		writer.writerow([])

def log_data(file_path, data):
	with open(file_path, "a") as f:
		writer = csv.writer(f)
		writer.writerow(data)

clear_file(write_file_path)
for i in range(len(states)):
	data = [ticks[i][0], ticks[i][1], states[i][0][0], states[i][1][0], states[i][2][0], states[i][3][0], states[i][4][0]]
	log_data(write_file_path, data)


