import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from my_plot import set_size
import numpy as np
import csv
import time

#plt.style.use("seaborn") # Default style is better I think...
width = 452.9679 # obtained from LaTeX text width in my dissertation

nice_fonts = {
	# Use LaTex to write all text
	"text.usetex": True,
	"font.family": "serif",
	# Use 11pt (10 is standard but due to file conversions, I use 11) font in plots, to match 11 pt font in document
	"axes.labelsize": 11,
	"font.size": 11,
	# Make the legend/label fonts a little smaller
	"legend.fontsize": 9,
	"xtick.labelsize": 9,
	"ytick.labelsize": 9,
}

matplotlib.rcParams.update(nice_fonts) # LaTeX fonts and sizes for graphs!


###################################################################

file_path = "/home/pi/BEng_Project/sensor_tests/data/imu/"
#file_name = "10_minutes_imu.csv"
file_name = "40_minutes_imu.csv" # beefy (2.8MB of imu data...)
lidar_file_path = "/home/pi/BEng_Project/sensor_tests/data/lidar/"
lidar_file_name = "lidar_scan.csv"

file = file_path + file_name
lidar_file = lidar_file_path + lidar_file_name

x_vals = []
y_vals = []
z_vals = []
theta_a_vals = []
theta_b_vals = []
theta_c_vals = []
time_vals = []
lidar_vals = []
dt = 1 / 32
counter = 0

'''
with open(file, "r") as f:
	reader = csv.reader(f)
	for row in reader:
		x_vals.append(float(row[0]))
		y_vals.append(float(row[1]))
		z_vals.append(float(row[2]))
		theta_a_vals.append(float(row[3]))
		theta_b_vals.append(float(row[4]))
		theta_c_vals.append(float(row[5]))
		time_vals.append(dt * counter)
		counter += 1
'''

with open(lidar_file, "r") as f:
	reader = csv.reader(f)
	for x, row in enumerate(reader):
		lidar_vals.append([])
		for i in range(360):
			lidar_vals[x].append(float(row[i]))

# x = np.linspace(0, 2*np.pi, 100) # from example...

# Initialise figure instance
#fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=set_size(width, subplot=[1, 3]))
#fig, ax1 = plt.subplots(1, 1, figsize=set_size(width, subplot=[1, 1]))

# Plot
#ax1.plot(time_vals, z_vals)
#ax2.plot(time_vals, y_vals)
#ax3.plot(time_vals, z_vals)

# Hist
#ax1.hist(np.array(x_vals), bins=280, edgecolor = 'black')
#ax2.hist(np.array(y_vals), bins=280, edgecolor = 'black')
#ax3.hist(np.array(z_vals), bins=280, edgecolor = 'black')

# Uncomment to turn off axis scale / ticks
#ax1.set_yticklabels([])
#ax2.set_yticklabels([])
#ax3.set_yticklabels([])

# Manual axis limits
#ax1.set_xlim(-0.25, 1.50)
#ax2.set_xlim(-0.25, 0.25)
#ax3.set_xlim(-0.25, 0.25)

#ax1.set_ylim(0, 21000)
#ax2.set_ylim(0, 21000)
#ax3.set_ylim(0, 21000)

# Axis labels
#ax1.set_xlabel(r'Time $(s)$')
#ax2.set_xlabel(r'Acceleration $(m/{s^2})$')
#ax3.set_xlabel(r'Acceleration $(m/{s^2})$')
#ax1.set_ylabel(r'Acceleration $(m/{s^2})$')
#ax2.set_ylabel(r'Frequency')
#ax3.set_ylabel(r'Frequency')

# Subplot titles
#ax1.set_title(r'z-axis')
#ax2.set_title(r'y-axis')
#ax3.set_title(r'z-axis')

#ax.legend()
#fig.suptitle(r'IMU Linear Acceleration')


# Save as PDF (no rasterising) and remove excess whitespace
#plt.savefig('/home/pi/BEng_Project/report_stuff/graph_formatting/imu_plot_z_06-04-19.pdf', format='pdf', bbox_inches='tight')

def imu_time_plot(time_vals, data_vals, title):
	fig, ax1 = plt.subplots(1, 1, figsize=set_size(width, subplot=[1, 1]))
	ax1.plot(time_vals, data_vals)
	ax1.set_xlabel(r'Time $(s)$')
	ax1.set_ylabel(r'Acceleration $(m/{s^2})$')
	ax1.set_title(title)
	plt.savefig('/home/pi/BEng_Project/report_stuff/graph_formatting/imu_plot_{}.pdf'.format(title), format='pdf', bbox_inches='tight')

def imu_hist_plot(data_vals, title, x_axis_limits=None):
	fig, ax1 = plt.subplots(1, 1, figsize=set_size(width, subplot=[1, 1]))
	ax1.hist(np.array(data_vals), bins=280, edgecolor = 'black')
	if x_axis_limits:
		ax1.set_xlim(x_axis_limits[0], x_axis_limits[1])
	ax1.set_xlabel(r'Acceleration $(m/{s^2})$')
	ax1.set_ylabel(r'Frequency')
	ax1.set_title(title)
	plt.savefig('/home/pi/BEng_Project/report_stuff/graph_formatting/imu_hist_{}.pdf'.format(title), format='pdf', bbox_inches='tight')

def lidar_plots(data_scan, title):
	fig, (ax1, ax2) = plt.subplots(2, 1, figsize=set_size(width, subplot=[2, 1]))
	ax1.plot(data_scan)
	ax1.set_xlabel(r'Angle $(deg)$')
	ax1.set_ylabel(r'Distance $(mm)$')
	ax1.set_title(r'Lidar Scan - Distance vs. Angle')
	x_pos = []
	y_pos = []
	x_lim = []
	y_lim = []
	max_range = 1792
	for i, dist in enumerate(data_scan):
		radians = (i * np.pi / 180)
		x_pos.append(-1 * dist * np.sin(radians))
		y_pos.append(-1 * dist * np.cos(radians))
	ax2.scatter(x_pos, y_pos)
	for i in range(360):
		radians = (i * np.pi / 180)
		x_lim.append(max_range * np.cos(radians))
		y_lim.append(max_range * np.sin(radians))
	ax2.scatter(x_lim, y_lim, c='g')
	ax2.set_xlabel(r'X (mm)')
	ax2.set_ylabel(r'Y (mm)')
	ax2.axis('equal')
	ax2.set_xlim(-2000, 2000)
	ax2.set_xlim(-2000, 2000)
	ax2.set_title(r'Lidar Scan - Real World Coordinates')
	plt.savefig('/home/pi/BEng_Project/report_stuff/graph_formatting/lidar_plot_{}.pdf'.format(title), format='pdf', bbox_inches='tight')

def main():
	start = time.time()
#	imu_time_plot(time_vals, x_vals, r'x-axis')
#	imu_time_plot(time_vals, y_vals, r'y-axis')
#	imu_time_plot(time_vals, z_vals, r'z-axis')

#	imu_hist_plot(x_vals, r'x-axis', (-0.5, 1.50))
#	imu_hist_plot(y_vals, r'y-axis', (-0.25, 0.25))
#	imu_hist_plot(z_vals, r'z-axis', (-0.25, 0.25))
	for i, scan in enumerate(lidar_vals):
		lidar_plots(scan, i)

	period = time.time() - start
	print("Took {} seconds".format(period))

if __name__ == "__main__":
	main()
