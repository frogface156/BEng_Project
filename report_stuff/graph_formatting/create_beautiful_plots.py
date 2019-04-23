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
lidar_coords_name = "lidar_coords.csv"

#odo_file_path = "/home/pi/BEng_Project/sensor_tests/data/odometry/"
odo_file_path = "/home/pi/BEng_Project/sensor_tests/data/kalman/"
#odo_file_name = "sample_encoder_data.csv"
odo_file_name = "raw_data_imu_odo.csv"
kalman_file = "/home/pi/BEng_Project/sensor_tests/data/kalman/kalman_data.csv"
#state_file = "/home/pi/BEng_Project/sensor_tests/analysis/odometry/odometry_test.csv"
state_file = "/home/pi/BEng_Project/sensor_tests/analysis/imu/imu_test.csv"
odo_pos_file_path = "/home/pi/BEng_Project/sensor_tests/analysis/odometry/"
odo_pos_file_name = "odometry_test.csv"


file = file_path + file_name
lidar_file = lidar_file_path + lidar_file_name
lidar_coords_file = lidar_file_path + lidar_coords_name
odo_file = odo_file_path + odo_file_name
odo_pos_file = odo_pos_file_path + odo_pos_file_name

x_vals = []
y_vals = []
z_vals = []
theta_a_vals = []
theta_b_vals = []
theta_c_vals = []
time_vals = []
lidar_vals = []
l_vals = []
r_vals = []
x_vals_2 = []
y_vals_2 = []
x_vals_3 = []
y_vals_3 = []
odo_time_vals = []
dt_imu = 1 / 32
dt_odo = 1 / 50
counter = 0


with open(file, "r") as f:
	reader = csv.reader(f)
	for row in reader:
		x_vals.append(float(row[0])*1000) # mm/s^2 rather than m/s^2
		y_vals.append(float(row[1])*1000)
		z_vals.append(float(row[2])*1000)
		theta_a_vals.append(float(row[3]))
		theta_b_vals.append(float(row[4]))
		theta_c_vals.append(float(row[5]))
		time_vals.append(dt_imu * counter)
		counter += 1



with open(lidar_file, "r") as f:
	reader = csv.reader(f)
	for x, row in enumerate(reader):
		lidar_vals.append([])
		for i in range(360):
			lidar_vals[x].append(float(row[i]))

lidar_x = []
lidar_y = []
with open(lidar_coords_file, "r") as f:
	reader = csv.reader(f)
	for row in reader:
		lidar_x.append(float(row[0]))
		lidar_y.append(float(row[1]))


with open(state_file, "r") as f:
	reader = csv.reader(f)
	for row in reader:
		x_vals_2.append(row[0])
		y_vals_2.append(row[2])


with open(odo_file, "r") as f:
	reader = csv.reader(f)
	for row in reader:
		l_vals.append(int(row[0]))
		r_vals.append(int(row[1]))

with open(odo_pos_file, "r") as f:
	reader = csv.reader(f)
	for row in reader:
		x_vals_3.append(float(row[0]))
		y_vals_3.append(float(row[2]))


'''
x_pred = []
x_odo = []
x_imu = []
x_corr = []
y_pred = []
y_odo = []
y_imu = []
y_corr = []
theta_pred = []
theta_odo = []
theta_imu = []
theta_corr = []
with open(kalman_file, "r") as f:
	reader = csv.reader(f)
	for row in reader:
		x_odo.append(row[0])
		y_odo.append(row[1])
		theta_odo.append(row[2])
		x_imu.append(row[3])
		y_imu.append(row[4])
		theta_imu.append(row[5])
		x_pred.append(row[6])
		y_pred.append(row[7])
		theta_pred.append(row[8])
		x_corr.append(row[9])
		y_corr.append(row[10])
		theta_corr.append(row[11])
'''


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

def imu_time_plot(time_vals, data_vals, title, color='#d62728'):
	fig, ax1 = plt.subplots(1, 1, figsize=set_size(width, subplot=[1, 1]))
	ax1.plot(time_vals, data_vals, color=color)
	ax1.set_xlabel(r'Time $(s)$')
	ax1.set_ylabel(r'Orientation $(deg)$')
	ax1.set_title(title)
	plt.savefig('/home/pi/BEng_Project/report_stuff/graph_formatting/imu_plot_{}.pdf'.format(title), format='pdf', bbox_inches='tight')

def imu_time_plot_multiple(time_vals, x_vals, y_vals, z_vals):
	fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=set_size(width, subplot=[1, 3]))
	ax1.plot(time_vals, x_vals, color='#1f77b4')
	ax1.set_xlabel(r'Time $(s)$')
	ax1.set_ylabel(r'Acceleration $(m/{s^2})$')
	ax1.set_title(r'x-axis')
	ax2.plot(time_vals, y_vals, color='#ff7f0e')
	ax2.set_xlabel(r'Time $(s)$')
	ax2.set_title(r'y-axis')
	ax3.plot(time_vals, z_vals, color='#2ca02c')
	ax3.set_xlabel(r'Time $(s)$')
	ax3.set_title(r'z-axis')
	plt.savefig('/home/pi/BEng_Project/report_stuff/graph_formatting/imu_plot_multiple.pdf', format='pdf', bbox_inches='tight')

def imu_hist_plot_multiple(x_vals, y_vals, z_vals):
	fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=set_size(width, subplot=[1, 3]))
	ax1.hist(np.array(x_vals), bins=280, edgecolor = 'black', color='#2ca02c')
	ax1.set_xlabel(r'Acceleration $(mm/{s^2})$')
	ax1.set_ylabel(r'Frequency')
	ax1.set_title(r'${a_x}_i$')
	ax1.set_xlim(-250.0, 250.0)
	ax2.hist(np.array(y_vals), bins=280, edgecolor = 'black', color='#ff7f0e')
	ax2.set_xlabel(r'Acceleration $(mm/{s^2})$')
	ax2.set_title(r'${a_y}_i$')
	ax2.set_xlim(-250.0, 250.0)
#	ax2.set_ylabel(r'Frequency')
	ax3.hist(np.array(z_vals), bins=800, edgecolor = 'black', color='#d62728')
	ax3.set_xlabel(r'Orientation $(deg)$')
	ax3.set_title(r'$\theta_i$')
	ax3.set_xlim(335, 385)
#	ax3.set_ylabel(r'Frequency')
	plt.subplots_adjust(wspace=0.5)
	plt.savefig('/home/pi/BEng_Project/report_stuff/graph_formatting/imu_hist_multiple.pdf', format='pdf', bbox_inches='tight')

def imu_hist_plot(data_vals, title, x_axis_limits=None, color='#1f77b4'):
	fig, ax1 = plt.subplots(1, 1, figsize=set_size(width, subplot=[1, 1]))
	ax1.hist(np.array(data_vals), bins=700, edgecolor = 'black', color=color)
	if x_axis_limits:
		ax1.set_xlim(x_axis_limits[0], x_axis_limits[1])
	ax1.set_xlabel(r'Orientation $(deg)$')
	ax1.set_ylabel(r'Frequency')
	ax1.set_title(r'\theta_i')
	#plt.subplots_adjust(wspace = 0.4)
	plt.savefig('/home/pi/BEng_Project/report_stuff/graph_formatting/imu_hist_{}.pdf'.format(title), format='pdf', bbox_inches='tight')

def lidar_plots(data_scan, title):
	fig, (ax1, ax2) = plt.subplots(2, 1, figsize=set_size(width, subplot=[2, 1]))
	ax1.plot(data_scan, color='#1f77b4')
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
	ax2.scatter(x_pos, y_pos, c='#1f77b4')
	for i in range(360):
		radians = (i * np.pi / 180)
		x_lim.append(max_range * np.cos(radians))
		y_lim.append(max_range * np.sin(radians))
	ax2.scatter(x_lim, y_lim, c='#ff7f0e')
	ax2.set_xlabel(r'X (mm)')
	ax2.set_ylabel(r'Y (mm)')
	ax2.axis('equal')
	ax2.set_xlim(-2000, 2000)
	ax2.set_xlim(-2000, 2000)
	ax2.set_title(r'Lidar Scan - Real World Coordinates')
	plt.savefig('/home/pi/BEng_Project/report_stuff/graph_formatting/lidar_plot_{}.pdf'.format(title), format='pdf', bbox_inches='tight')

def lidar_plot_coords(x, y):
	fig, ax1 = plt.subplots(1, 1, figsize=set_size(width, subplot=[1, 1]))
	ax1.scatter(x, y, c='#1f77b4')
	ax1.scatter(0, 0, c='#2ca02c')
	ax1.arrow(0, 0, 100, 0)
	max_range = 1792
	x_lim = []
	y_lim = []
	for i in range(360):
                radians = (i * np.pi / 180)
                x_lim.append(max_range * np.cos(radians))
                y_lim.append(max_range * np.sin(radians))
	ax1.scatter(x_lim, y_lim, c='#ff7f0e')
	ax1.set_xlabel(r'X (mm)')
	ax1.set_ylabel(r'Y (mm)')
	ax1.axis('equal')
	ax1.set_xlim(-2000, 2000)
	ax1.set_xlim(-2000, 2000)
	ax1.set_title(r'Lidar Scan - Real World Coordinates')
	plt.savefig('/home/pi/BEng_Project/report_stuff/graph_formatting/lidar_coords_plot.pdf', format='pdf', bbox_inches='tight')

def lidar_plot_raw_data(data_scan):
	fig, ax1 = plt.subplots(1, 1, figsize=set_size(width, subplot=[1, 1]))
	ax1.plot(data_scan, color='#1f77b4')
	ax1.set_xlabel(r'Angle $(deg)$')
	ax1.set_ylabel(r'Distance $(mm)$')
	ax1.set_title(r'Lidar Scan - Distance vs. Angle')
	plt.savefig('/home/pi/BEng_Project/report_stuff/graph_formatting/lidar_plot_raw_data.pdf', format='pdf', bbox_inches='tight')

def encoder_plot_lr(l_vals, r_vals):
	fig, ax1 = plt.subplots(1, 1, figsize=set_size(width, subplot=[1, 1]))
	ax1.plot(l_vals, label='Left Encoder')
	ax1.plot(r_vals, label='Right Encoder')
	ax1.set_xlabel(r'Samples')
	ax1.set_ylabel(r'Encoder Counts')
	ax1.legend()
	ax1.set_title(r'Quadrature Encoder Sample Data')
	plt.savefig('/home/pi/BEng_Project/report_stuff/graph_formatting/encoder_plot_lr.pdf', format='pdf', bbox_inches='tight')

def lr_odometry_pos_plot(l_vals, r_vals, x_vals, y_vals):
	fig, (ax1, ax2) = plt.subplots(1, 2, figsize=set_size(width, subplot=[1, 2]))
	ax1.plot(l_vals, label='Left Encoder')
	ax1.plot(r_vals, label='Right Encoder')
	ax1.set_xlabel(r'Samples')
	ax1.set_ylabel(r'Encoder Counts')
	ax1.legend()
	ax1.set_title(r'Quadrature Encoder Data')
	ax2.scatter(x_vals, y_vals)
	ax2.set_title(r'Odometry Model')
	ax2.set_xlabel(r'x-axis $(mm)$')
	ax2.set_ylabel(r'y-axis $(mm)$')
	plt.subplots_adjust(wspace=0.4)
	plt.savefig('/home/pi/BEng_Project/report_stuff/graph_formatting/lr_odometry_pos_plot.pdf', format='pdf', bbox_inches='tight')


def position_plot(x_vals, y_vals, title):
	fig, ax1 = plt.subplots(1, 1, figsize=set_size(width, subplot=[1, 1]))
	ax1.scatter(x_vals, y_vals)
	ax1.set_title(r'Position Plot')
	plt.savefig('/home/pi/BEng_Project/report_stuff/graph_formatting/position_{}.pdf'.format(title), format='pdf', bbox_inches='tight')

def compare_plots(title, *args):
	fig, ax1 = plt.subplots(1, 1, figsize=set_size(width, subplot=[1, 1]))
	for i, data in enumerate(args):
		ax1.plot(data, label=i)
	ax1.legend()
	ax1.set_title(r'Kalman Filter - Comparison')
	ax1.set_xlabel(r'Samples')
	ax1.set_ylabel(r'Displacement (mm)')
	plt.savefig('/home/pi/BEng_Project/report_stuff/graph_formatting/compare_{}.pdf'.format(title), format='pdf', bbox_inches='tight')

def main():
	start = time.time()
#	imu_time_plot(time_vals, x_vals, r'x-axis', color='#1f77b4')
#	imu_time_plot(time_vals, y_vals, r'y-axis', color='#ff7f0e')
#	imu_time_plot(time_vals, z_vals, r'z-axis', color='#2ca02c')
#	imu_time_plot(time_vals, theta_a_vals, r'\theta_i', color='#d62728')

#	imu_time_plot_multiple(time_vals, x_vals, y_vals, z_vals)
#	imu_hist_plot_multiple(z_vals, y_vals, theta_a_vals)


#	imu_hist_plot(x_vals, r'x-axis', (-0.5, 1.50), color='#1f77b4')
#	imu_hist_plot(y_vals, r'y-axis', (-0.25, 0.25), color='#ff7f0e')
#	imu_hist_plot(z_vals, r'z-axis', (-0.25, 0.25), color='#2ca02c')
	imu_hist_plot(theta_a_vals, r'\theta_i', (335, 385), color='#d62728')

#	for scan in enumerate(lidar_vals):
#		lidar_plots(scan, i)
#		lidar_plot_raw_data(scan)
#	lidar_plot_coords(lidar_x, lidar_y)

#	encoder_plot_lr(l_vals, r_vals)
#	lr_odometry_pos_plot(l_vals, r_vals, x_vals_3, y_vals_3)

#	position_plot(x_vals, y_vals, "200_1082")
#	compare_plots("x_position", x_pred, x_imu, x_odo, x_corr)
#	compare_plots("y_position", y_pred, y_imu, y_odo, y_corr)
#	compare_plots("theta", theta_pred, theta_imu, theta_odo, theta_corr)

	period = time.time() - start
	print("Took {} seconds".format(period))

if __name__ == "__main__":
	main()
