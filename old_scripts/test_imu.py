import imu_sensor
import imu_state_space as iss
from Config import Config
from pygame.time import Clock
import numpy as np
from Config import Config

freq = Config['pygame']['fast_loop_freq']
dt = 1 / freq

init = Config['test']['initial_state']

x = np.array([[init['x_0'], init['vx_0'], init['y_0'], init['vy_0'], init['theta_0']]]).T
A = np.array([[1, dt, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, dt, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]])
B = np.array([[0.5*dt**2, 0, 0], [dt, 0, 0], [0, 0.5*dt**2, 0], [0, dt, 0], [0, 0, 1]])


imu = imu_sensor.IMU()

clock = Clock()

print("Start Coords - X: {}, Y: {}".format(x[0], x[3]))
input("Enter a key to start loop...")

while True:
	a_x = imu.linear_acceleration[0]
	a_y = imu.linear_acceleration[1]
	theta = imu.euler[0]

	u = np.array([[a_x, a_y, theta]]).T

	z = np.dot(A, x) + np.dot(B, u)

	#z = iss.measure_state(x, a_x, a_y, theta)
	print("X: {:.2f}, Y: {:.2f}, v_x: {:.2f}, v_y: {:.2f}, a_x: {:.2f}, a_y: {:.2f}".format(x[0], x[3], x[1], x[4], x[2], x[5]))

	clock.tick(freq)
