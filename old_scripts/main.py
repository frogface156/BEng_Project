# First edit to this file was on 23rd March 2019

# General Libaries
import threading
import time
import numpy as np
from pygame.time import Clock

# My Libraries
from Config import Config
import imu_sensor
import encoders
import robot_state_space as rss
import imu_state_space as iss
import odometry_state_space as oss
import lidar_state_space as lss
import kalman

# Initial Conditions Matrix Setup
init = Config['test']['initial_state'] # dictionary of initial positions

# can populate theta_0 from IMU reading
x = np.array([[init['x_0'], init['vx_0'], init['y_0'], init['vy_0'], init['theta_0']]]).T
# can populate this with sigma variables from the lidar (at least for x and y)...
# can populate the theta probability with the sigma for the IMU orientation...
P = np.array([[0.1, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0.1, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]) # P(v) can be 0 as  we're pretty confident v_0 = 0 for x and y

# General Variables
fast_loop_freq = Config['pygame']['fast_loop_freq']
dt = 1 / freq

# Robot
Q = rss.Q
A = rss.A
# B = A # 1. Is this right? Probs not... 2. Are you gonna use control matrix? Do you need to?
# u = np.array([[0, 2, 0, 2, 0]]).transpose()

# IMU
H_i = iss.H
R_i = iss.R

# Odometry
H_o = oss.H
R_o = oss.R

# Lidar
H_l = lss.H
R_l = lss.R


def fast_loop(print_lock, state_vector_lock, path_planning_lock, imu, enc, freq):
	clock = Clock()
	dt = 1 / freq
	# might be worth having an "initial" loop to sort out accleration / dt issues?
	imu_a_x = 0 # first time, shouldn't be measured before the prediction because it hasn't been any time yet!
	imu_a_y = 0
	while True:
		# get imu measurements
		# consider the fact that acceleration should really predict state (except
		# theta) for the NEXT timestep...
		imu_theta = imu.euler[0]
		z_i = iss.measure_state(x, imu_a_x, imu_a_y, imu_theta) # get control vector (actually this is for the next loop, but this was the best way of handling the state...)
		imu_a_x = imu.linear_acceleration[0] # measured AFTER KF so it can be used for the NEXT timestep
		imu_a_y = imu.linear_acceleration[1]

		# get odometry measurements
		enc_l, enc_r = enc.get_ticks()
		z_o = oss.measure_state(x, enc_l, enc_r)

		# get lidar measurements
		# z_l = lss.measure_state(x, scan) # update this whenever you have done lidar stuff...

		#Kalman Filter
		# State Propagation (Prediction) - based on previous state and any control signal (don't have one atm...)
		with state_vector_lock:
			x, P = kalman.predict(x, P, A, Q) # can pass B, u as if you want...

		# IMU Update
		with state_vector_lock:
			x, P = kalman.update(x, P, z_i, H_i, R_i)
		# Odometry Update
		with state_vector_lock:
			x, P = kalman.update(x, P, z_o, H_o, R_o)


		# Path correction control code
		#with path_planning_lock:
			# run control code based on position estimate and current planned path
			# does this need to run every loop?

		# Actuate motors
		#rc_robot.actuate(args)

		#time.sleep(0.01) # is this required? Probably not...
		clock.tick(freq) # limits the loop to "freq" fps - stops unnecessary processing power being used

def slow_loop(print_lock, text):
	freq = 10
	clock = Clock()
	while True:
		with print_lock:
			print("This {} will be taken by the Lidar scanning and Path Planning".format(text))
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

def main():
	imu = imu_sensor.IMU()
	enc = encoders.Encoders()
	# lidar = lidar.Lidar() # add when written...

	print_lock = threading.Lock()
	state_vector_lock = threading.Lock()
	path_planning_lock = threading.Lock()
	fast_thread = threading.Thread(target=fast_loop, args=(print_lock, state_vector_lock, path_planning_lock, imu, enc, fast_loop_freq), name="fast_loop")
	fast_thread.start()
	slow_thread = threading.Thread(target=slow_loop, args=(print_lock, 'dummy_text'), name="slow_loop")
	slow_thread.start()


if __name__ == "__main__":
	main()
