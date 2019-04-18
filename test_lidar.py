import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from my_plot import set_size

import numpy as np
import sensors
import models

imu = sensors.IMU()
lidar = sensors.Lidar()
lss = models.LidarStateSpace()
iss = models.IMUStateSpace()

obstacles = []

for i in range(1):
	heading = (-1 * np.radians(imu.euler[0] - iss.theta_bias)) % (2*np.pi)
	scan = lidar.get_scan(100, 0.04)
	obstacles = lss.get_obstacles(scan, heading)
	print(obstacles)

x_vals = []
y_vals = []

for point in obstacles:
	x_vals.append(point[0])
	y_vals.append(point[1])

width = 452.9679
fig, ax1 = plt.subplots(1, 1, figsize=set_size(width, subplot=[1, 1]))
ax1.scatter(x_vals, y_vals)
ax1.set_title("Lidar - Detected Obstacles")
plt.savefig('/home/pi/BEng_Project/report_stuff/graph_formatting/lidar_scan.pdf', format='pdf', bbox_inches='tight')
