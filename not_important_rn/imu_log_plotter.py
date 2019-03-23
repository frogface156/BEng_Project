import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

file = input("File name: ")

file_path = "sensor_tests/{}.csv".format(file)

x_vals = []
y_vals = []
z_vals = []

with open(file_path, 'r') as file:
	reader = csv.reader(file)
	for row in reader:
		x_vals.append(row[2])
		y_vals.append(row[3])
		z_vals.append(row[4])

plt.plot(x_vals, label='X')
plt.plot(y_vals, label='Y')
plt.plot(z_vals, label='Z')
plt.legend()
plt.title('IMU - Linear Acceleration')

#plt.show()
plt.savefig("sensor_tests/graphs/IMU_noise_plot.png")
