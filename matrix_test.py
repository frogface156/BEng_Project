import numpy as np
import random
import time

x1_0 = 0
x2_0 = 0
x3_0 = 0
y1_0 = 0
y2_0 = 0
y3_0 = 0
dt = 1
dax = 2*random.random()
day = 2*random.random()

A = np.array([[1, dt, 0.5*dt**2, 0, 0, 0], [0, 1, dt, 0, 0, 0], [0, 0, 1, 0, 0, 0], [0, 0, 0, 1, dt, 0.5*dt**2], [0, 0, 0, 0, 1, dt], [0, 0, 0, 0, 0, 1]])
X = np.array([x1_0, x2_0, x3_0, y1_0, y2_0, y3_0])

print("Test: {}".format(np.dot(A, X)))

B = np.array([[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1]])
u = np.array([0, 0, dax, 0, 0, day])

Y = [1, 0, 0, 1, 0, 0]

old_time = time.time()

for x in range(10):
	X = np.dot(A, X) + np.dot(B, u)
	print("Loop took {} seconds".format(time.time() - old_time))
	old_time = time.time()
	#print("Position, Velocity, Acceleration is: {}".format(X))
	print(X)
