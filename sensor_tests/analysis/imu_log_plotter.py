import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

file = input("File name: ")

file_path = "/home/pi/BEng_Project/sensor_tests/{}.csv".format(file)

x_vals = []
y_vals = []
z_vals = []
theta_vals = []

with open(file_path, 'r') as file:
	reader = csv.reader(file)
	for row in reader:
		x_vals.append(float(row[0]))
		y_vals.append(float(row[1]))
		z_vals.append(float(row[2]))
		theta_vals.append(float(row[3]))

graph_path = "/home/pi/BEng_Project/sensor_tests/graphs/"
'''
plt.legend()
plt.plot(x_vals, label='X')
plt.title('IMU - Linear Acceleration - X Axis')
plt.savefig(graph_path + "IMU_noise_plot_x.png")

plt.clf()
plt.legend()
plt.plot(y_vals, label='Y')
plt.title('IMU - Linear Acceleration - Y Axis')
plt.savefig(graph_path + "IMU_noise_plot_y.png")

plt.clf()
plt.legend()
plt.plot(z_vals, label='Z')
plt.title('IMU - Linear Acceleration - Z Axis')
plt.savefig(graph_path + "IMU_noise_plot_z.png")

plt.clf()
plt.legend()
plt.plot(theta_vals, label='Theta')
plt.title('IMU - Euler Vector - XY plane')
plt.savefig(graph_path + "IMU_noise_plot_theta.png")
'''

x_sample = pd.Series(x_vals)
y_sample = pd.Series(y_vals)
z_sample = pd.Series(z_vals)
theta_sample = pd.Series(theta_vals)

def get_info(sample):
	mean = sample.mean()
	median = sample.median()
	sd_est = sample.std()
	sd_meas = sample.std(ddof=0)
	var = sample.var
	return [mean, median, sd_est, sd_meas, var]

x_info = get_info(x_sample)
y_info = get_info(y_sample)
z_info = get_info(z_sample)
theta_info = get_info(theta_sample)

print("Mean of x sample: {}".format(x_info[0]))
print("Standard Deviation of x sample: {}".format(x_info[3]))
print("Mean of y sample: {}".format(y_info[0]))
print("Standard Deviation of y sample: {}".format(y_info[3]))
print("Mean of z sample: {}".format(z_info[0]))
print("Standard Deviation of z sample: {}".format(z_info[3]))
print("Mean of theta sample: {}".format(theta_info[0]))
print("Standard Deviation of theta sample: {}".format(theta_info[3]))
