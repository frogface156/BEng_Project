import numpy as np
import random
import time

x1 = 0 # x_pos
x2 = 0 # x_vel
x3 = 0 # x_acc
y1 = 0 # y_pos
y2 = 0 # y_vel
y3 = 0 # y_acc
theta = 0
dt = 1

def generate_acceleration_and_theta(theta):
	new_theta = (theta + random.uniform(-(np.pi)/60, (np.pi)/60))%2*np.pi
	a = 2*random.random()
	a_x = a*np.cos(new_theta)
	a_y = a*np.sin(new_theta)
	return a_x, a_y, new_theta

x3, y3, theta = generate_acceleration_and_theta(theta)

A = np.array([[1, dt, 0.5*dt**2, 0, 0, 0], [0, 1, dt, 0, 0, 0], [0, 0, 1, 0, 0, 0], [0, 0, 0, 1, dt, 0.5*dt**2], [0, 0, 0, 0, 1, dt], [0, 0, 0, 0, 0, 1]])
X = np.array([x1, x2, x3, y1, y2, y3])

B = np.array([[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1]])
#u = np.array([0, 0, x3, 0, 0, y3])
u = np.array([0, 0, 0, 0, 0, 0])

old_time = time.time()

for x in range(10):
	X = np.dot(A, X) + np.dot(B, u)
	print("Loop took {} seconds".format(time.time() - old_time))
	old_time = time.time()
	#print("Position, Velocity, Acceleration is: {}".format(X))
	print(X, theta)
	x3, y3, theta = generate_acceleration_and_theta(theta)
