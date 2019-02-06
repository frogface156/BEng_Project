import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

file_path = "sensor_tests/log1.csv"

x_vals = []
y_vals = []
z_vals = []

with open(file_path, 'r') as file:
	reader = csv.reader(file)
	for row in reader:
		x_vals.append(row[0])
		y_vals.append(row[1])
		z_vals.append(row[2])

plt.plot(x_vals, label='X')
plt.plot(y_vals, label='Y')
plt.plot(z_vals, label='Z')
plt.legend()
plt.title('IMU - Linear Acceleration')

#plt.show()
plt.savefig("sensor_tests/imu_plot3.png")
