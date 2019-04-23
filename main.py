# First edit to this file was on 23rd March 2019

# General Libaries
import threading
import time
import numpy as np
from pygame.time import Clock
from math import sqrt
import csv

# My Libraries
from Config import Config
import sensors
import temp_models as models
import kalman
import prop_control as control
import kastar

# Initial Conditions Matrix Setup
init = Config['test']['initial_state'] # dictionary of initial positions

# can populate theta_0 from IMU reading
x = np.array([[init['x_0'], init['vx_0'], init['y_0'], init['vy_0'], init['theta_0']]]).T
P = np.array([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])

# General Variables
freq = Config['pygame']['fast_loop_freq']
dt = 1 / freq

# Path planning scale factor
d = Config['path_planning']['scale']
dist_thresh = Config['control']['distance_threshold']

write_file = "/home/pi/BEng_Project/kalman_test_vals.csv"
path_file = "/home/pi/BEng_Project/path.csv"
with open(write_file, "w") as f:
	writer = csv.writer(f)
with open(path_file, "w") as f:
	writer = csv.writer(f)


def main():
	# Sensor init
	imu = sensors.IMU()
	enc = sensors.Encoders()
	lidar = sensors.Lidar()

	# State Space Models
	rss = models.RobotStateSpace()
	iss = models.IMUStateSpace()
	oss = models.OdometryStateSpace()
	lss = models.LidarStateSpace()

	# Control init
	ctrl = control.Control()

	# Path Planning init
	#extents = input("Enter world extents: e.g. 3000 2200")
	#start = input("Enter start pose: e.g. 500 200 0").split()
	#goal = input("Enter goal pose: e.g. 2800 0 0")

	extents = Config['path_planning']['test_params']['extents']
	start = Config['path_planning']['test_params']['start']
	goal = Config['path_planning']['test_params']['goal']

	# Obstacle Detection
	obstacles_lidar = []
	heading = (-1 * np.radians(imu.euler[0] - iss.theta_bias)) % (2*np.pi)
	scan = lidar.get_scan(100, 0.04) # add more updates to improve initial scan
	obstacles_lidar = lss.get_obstacles(scan, heading)
	print(obstacles_lidar)

	# Scaling down
	extents = (int(extents[0]/d), int(extents[1]/d))
	start = (start[0]/d, (start[1]/d) + (extents[1]/2), np.radians(start[2]))
	goal = (goal[0]/d, (goal[1]/d) + (extents[1]/2), np.radians(goal[2]))
	obstacles = []
	for point in obstacles_lidar:
		obstacles.append((int(point[0]/20 + start[0]), (int(point[1]/20 + start[1]))))

	pp = kastar.KinematicAStar(extents)
	path_scaled_down, moves, visited, obstacles_array = pp.plan_path(start, goal, obstacles)
	# scaling path coords back to real scale
	path = []
	for a, b in path_scaled_down:
		log_data(path_file, [a*d, b*d])
		path.append((a * d, b * d))

	print(path)
	print(moves)

	input("Ready? ")
	print(3)
	time.sleep(1)
	print(2)
	time.sleep(1)
	print(1)
	time.sleep(1)
	print("GO!")

	# Threading init
	print_lock = threading.Lock()
	state_vector_lock = threading.Lock()
	fast_thread = threading.Thread(target=fast_loop, args=(print_lock, state_vector_lock, imu, enc, iss, oss, rss, path, ctrl), name="fast_loop")
	fast_thread.start()
#	slow_thread = threading.Thread(target=slow_loop, args=(print_lock, 'dummy_text'), name="slow_loop")
#	slow_thread.start()

def fast_loop(print_lock, state_vector_lock, imu, enc, iss, oss, rss, path, ctrl):
	clock = Clock()
	imu_a_x = 0
	imu_a_y = 0
	p = path.pop(0)
	with print_lock:
		print(p)
	start = time.time()
	global x
	global P

	while True:
		period = time.time() - start
		actual_freq = 1 / period
#		with print_lock:
#			print("{}Hz".format(actual_freq))
		start = time.time()

		dist_to_point = sqrt((x[0][0] - p[0])**2 + (x[2][0] - p[1])**2)
		if dist_to_point < dist_thresh:
			if path:
				p = path.pop(0) # get the next point on the path
				with print_lock:
					print(p)
			else:
				with print_lock:
					print("Reached Goal")
					ctrl.move('stop')
					break

		phi = ctrl.get_phi(x, p)
#		with print_lock:
#			print(np.degrees(phi))
		a, b =	ctrl.p_control(phi)
#		with print_lock:
#			print("A: {}, B: {}".format(a, b))

		# State Estimation Code
#		imu_theta = imu.euler[0]
#		z_i = iss.measure_state(x, imu_a_x, imu_a_y, imu_theta)
#		imu_a_x = imu.linear_acceleration[2]
#		imu_a_y = imu.linear_acceleration[1]

		l_ticks, r_ticks = enc.get_ticks() # ticks = encoder counts
		l_ticks, r_ticks = oss.clean_input(l_ticks, r_ticks) # removes noise if present
		z_o = oss.measure_state(x, l_ticks, r_ticks)

		#Kalman Filter
		# State Propagation
		with state_vector_lock:
			x, P = kalman.predict(x, P, rss.A, rss.Q) # can pass B, u as if you want...

		# IMU Update
#		with state_vector_lock:
#			x, P = kalman.update(x, P, z_i, iss.H, iss.R)

		# Odometry Update
		with state_vector_lock:
			x, P = kalman.update(x, P, z_o, oss.H, oss.R)
#			with print_lock:
#				print(x)
			xx = x[0][0]
			xy = x[2][0]
			xt = x[4][0]
			log_data(write_file, [xx, xy, xt])


		# Path correction control code
		#with path_planning_lock:
			# run control code based on position estimate and current planned path
			# does this need to run every loop?

		# Actuate motors
		#rc_robot.actuate(args)

		clock.tick(freq) # limits the loop to "freq" fps - stops unnecessary processing power being used

def slow_loop(print_lock, text):
	freq = 10
	clock = Clock()
	while True:
#		with print_lock:
#			print("This {} will be taken by the Lidar scanning and Path Planning".format(text))
		time.sleep(0.01)
		clock.tick(freq)
	# while True:
		# listen for Lidar scan from arduino
		# if lidar_scan:
			# infer_position using one of the methods you know
			# WITH STATE_VECTOR_LOCK:
				# update belief of position vector in KF
			# run path planning code
			# WITH PATH_PLANNING_LOCK (and maybe state_vector_lock?):
				# update path plan based on current position and end goal

def log_data(file, data):
	with open(file, "a") as f:
		writer = csv.writer(f)
		writer.writerow(data)


if __name__ == "__main__":
	main()
