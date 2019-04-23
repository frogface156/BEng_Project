import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from my_plot import set_size
import numpy as np
import csv

import sensors
import models
from my_plot import set_size
import kastar
from Config import Config

write_file = "/home/pi/BEng_Project/output_path.csv"

start = (700, 0, 0)
goal = (2200, 0, 0)
extents = (3000, 2200)
#start = (0, 31, np.radians(0))
#goal = (90, 31, np.radians(0))
#extents = (100, 70)
d = 20
extents = (int(extents[0]/d), int(extents[1]/d))
start = (start[0]/d, (start[1]/d) + (extents[1]/2), np.radians(start[2]))
goal = (goal[0]/d, (goal[1]/d) + (extents[1]/2), np.radians(goal[2]))


width = 452.9679 # obtained from LaTeX text width in my dissertation
#width /= 2

nice_fonts = {
	# Use LaTex to write all text
	"text.usetex": True,
	"font.family": "serif",
	# Use 11pt (10 is standard but due to file conversions, I use 11) font in plots, to $
	"axes.labelsize": 11,
	"font.size": 11,
	# Make the legend/label fonts a little smaller
	"legend.fontsize": 9,
	"xtick.labelsize": 9,
	"ytick.labelsize": 9,
}

matplotlib.rcParams.update(nice_fonts) # LaTeX fonts and sizes for graphs!


imu = sensors.IMU()
lidar = sensors.Lidar()
lss = models.LidarStateSpace()
iss = models.IMUStateSpace()

obstacles_lidar = []

for i in range(1):
	heading = (-1 * np.radians(imu.euler[0] - iss.theta_bias)) % (2*np.pi)
	scan = lidar.get_scan(100, 0.04)
	obstacles_lidar = lss.get_obstacles(scan, heading)
	print(obstacles_lidar)

obstacles = []

for point in obstacles_lidar:
	#obstacles.append((int(point[0]/20), (int(point[1]/20 + extents[1]/2))))
	obstacles.append((int(point[0]/20 + start[0]), (int(point[1]/20 + start[1]))))

pp = kastar.KinematicAStar(extents)
#start = (randint(0, 10), randint(0, 10), np.radians(randint(0, 20)))
#goal = (randint(40, 50), randint(40, 50), np.radians(randint(30, 50)))
#path, moves, visited, obstacles_array = pp.plan_path(start, goal, obstacles)
path, moves, visited, obstacles_array = pp.plan_path(start, goal, obstacles)
print(path)
print(moves)

x_vals = []
y_vals = []

for node in path:
	x_vals.append(node[0])
	y_vals.append(node[1])

fig, ax1 = plt.subplots(1, 1, figsize=set_size(width, subplot=[1, 1]))
ax1.scatter(x_vals, y_vals, c='#ff7f0e')
ax1.scatter(x_vals[0], y_vals[0], c='#2ca02c')
ax1.scatter(x_vals[-1], y_vals[-1], c='#d62728')

scalar = 3
dx_start = scalar * np.cos(start[2])
dy_start = scalar * np.sin(start[2])
dx_goal = scalar * np.cos(goal[2])
dy_goal = scalar * np.sin(goal[2])

ax1.arrow(x_vals[0], y_vals[0], dx_start, dy_start)
ax1.arrow(x_vals[-1], y_vals[-1], dx_goal, dy_goal)
ax1.set_xlabel(r'x-axis')
ax1.set_xlim(0, extents[0])
ax1.set_ylim(0, extents[1])
ax1.set_ylabel(r'y-axis')
ax1.matshow(obstacles_array.T, cmap='Blues')
plt.savefig('/home/pi/BEng_Project/report_stuff/graph_formatting/lidar_path_planning.pdf', format='pdf', bbox_inches='tight')

with open(write_file, "w") as f:
	writer = csv.writer(f)
	for point in path:
		writer.writerow(point)
