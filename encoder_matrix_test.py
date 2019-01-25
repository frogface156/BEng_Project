import numpy as np
import random
import time

x_0 = 0
y_0 = 0
theta = 0
dt = 1
dl = 2*random.random()
dr = 2*random.random()
alpha = 0
w = 20 # cm

def compute_alpha_and_R(r, l):
	alpha = (r - l)/w
	R = l/alpha
	return alpha, R

def compute_sin_and_cos(theta, alpha):
	new_theta = (theta + alpha)%2*np.pi
	sin_theta = np.sin(theta)
	cos_theta = np.cos(theta)
	sin_new_theta = np.sin(new_theta)
	cos_new_theta = np.cos(new_theta)
	return sin_theta, cos_theta, sin_new_theta, cos_new_theta, new_theta

def return_new_pose(X, theta, r, l):
	alpha, R = compute_alpha_and_R(r, l)
	sin_theta, cos_theta, sin_new_theta, cos_new_theta, new_theta = compute_sin_and_cos(theta, alpha)
	transposition = R + (w/2)
	C = X - transposition*np.array([sin_theta, -1*cos_theta])
	X = C + transposition*np.array([sin_new_theta, -cos_new_theta])
	return X, new_theta

X = np.array([x_0, y_0])

old_time = time.time()

for x in range(10):
	X, theta = return_new_pose(X, theta, dr, dl)
	print("Loop took {} seconds".format(time.time() - old_time))
	old_time = time.time()
	print("X: {}, Y: {}, Heading: {}".format(X[0], X[1], theta))
	dr = 2*random.random()
	dl = 2*random.random()