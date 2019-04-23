import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import csv

from my_plot import set_size
import sensors
import models

raw_scan_file = "/home/pi/BEng_Project/sensor_tests/data/lidar/lidar_scan.csv"
lidar_coords_file = "/home/pi/BEng_Project/sensor_tests/data/lidar/lidar_coords.csv"

def clear_file(file):
	with open(file, "w") as f:
		writer = csv.writer(f)

def log_data(file, data):
	with open(file, "a") as f:
		writer = csv.writer(f)
		writer.writerow(data)

imu = sensors.IMU()
lidar = sensors.Lidar()
lss = models.LidarStateSpace()
iss = models.IMUStateSpace()

obstacles = []

clear_file(raw_scan_file)
clear_file(lidar_coords_file)
for i in range(1):
	heading = (-1 * np.radians(imu.euler[0] - iss.theta_bias)) % (2*np.pi)
	scan = lidar.get_scan(200, 0.04)
	log_data(raw_scan_file, scan)
	obstacles = lss.get_obstacles(scan, heading)
	print(obstacles)

x_vals = []
y_vals = []

for point in obstacles:
	x_vals.append(point[0])
	y_vals.append(point[1])
	data = [point[0], point[1]]
	log_data(lidar_coords_file, data)

width = 452.9679
fig, ax1 = plt.subplots(1, 1, figsize=set_size(width, subplot=[1, 1]))
ax1.scatter(x_vals, y_vals)
ax1.set_title("Lidar - Detected Obstacles")
plt.savefig('/home/pi/BEng_Project/report_stuff/graph_formatting/lidar_scan.pdf', format='pdf', bbox_inches='tight')
