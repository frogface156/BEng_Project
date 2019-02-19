import numpy as np
import time

x_0 = 0
y_0 = 0
theta = 0
alpha = 0
w = 200 # cm

ticks_to_mm_factor = 0.9044025

def compute_alpha(r, l):
	alpha = (r - l)/w
	return alpha

def compute_radius(alpha):
	rad = 1/alpha
	return rad

def compute_sin_and_cos(theta, alpha):
	new_theta = (theta + alpha)%2*np.pi
	sin_theta = np.sin(theta)
	cos_theta = np.cos(theta)
	sin_new_theta = np.sin(new_theta)
	cos_new_theta = np.cos(new_theta)
	return sin_theta, cos_theta, sin_new_theta, cos_new_theta, new_theta

def return_new_pose(X, theta, l, r): # takes l and r in mm NOT ticks
	if l == r:
		l, r = ticks_to_mm(l, r)
		new_theta = theta
		X = X + l*np.array([np.cos(new_theta), np.sin(new_theta)])
		return X, new_theta
	else:
		l, r = ticks_to_mm(l, r)
		alpha = compute_alpha(r, l)
		rad = compute_radius(alpha)
		sin_theta, cos_theta, sin_new_theta, cos_new_theta, new_theta = compute_sin_and_cos(theta, alpha)
		transposition = rad + (w/2)
		C = X - transposition*np.array([sin_theta, -1*cos_theta])
		X = C + transposition*np.array([sin_new_theta, -cos_new_theta])
		return X, new_theta

def ticks_to_mm(l_ticks, r_ticks):
	l_mm = l_ticks * ticks_to_mm_factor
	r_mm = r_ticks * ticks_to_mm_factor
	return l_mm, r_mm

if __name__ == "__main__":
	dr = 2*random.random()
	dl = 2*random.random()
	dt = 1

	X = np.array([x_0, y_0])

	old_time = time.time()

	for x in range(10):
		X, theta = return_new_pose(X, theta, dr, dl)
		print("Loop took {} seconds".format(time.time() - old_time))
		old_time = time.time()
		print("X: {}, Y: {}, Heading: {}".format(X[0], X[1], theta))
		dr = 2*random.random()
		dl = 2*random.random()
