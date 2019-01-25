import imu_sensor
import matplotlib.pyplot as plt
import numpy as np

IMU = imu_sensor.IMU()

count = 2000
x_1 = np.zeros(count)
x_2 = np.zeros(count)
x_3 = np.zeros(count)

for i in range(count):
	x_1[i] = IMU.linear_acceleration[0]
	x_2[i] = IMU.linear_acceleration[1]
	x_3[i] = IMU.linear_acceleration[2]

plt.figure(1)

plt.subplot(221)
plt.hist(x_1, bins='auto', color='#0504aa')
plt.grid(True)
plt.title('x direction')

plt.subplot(222)
plt.hist(x_2, bins='auto', color='#0504aa')
plt.grid(True)
plt.title('y direction')

plt.subplot(223)
plt.hist(x_3, bins='auto', color='#0504aa')
plt.grid(True)
plt.title('z direction')

plt.show()
