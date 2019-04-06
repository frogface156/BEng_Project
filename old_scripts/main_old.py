# First edit to this file was on 23rd March 2019

from pygame.time import Clock
import encoders
import imu_sensor
import threading
import time
from Config import Config
import kalman
import numpy as np
import imu_state_space as iss

# Initial IMU conditions and Matrix Setup
dt = 0;
C = iss.C
x = iss.x
P = iss.P
B = iss.B
u = iss.get_u(0, 0)
theta = 0

# Initial Encoder conditions and Matrix Setup
sr2 = Config['encoders']['sr2']
R = sr2 * np.eye(z.shape[0])
z = np.array([[0, 0], [1, 0]])

def fast_loop(print_lock, state_vector_lock, path_planning_lock, imu, enc, freq):
	clock = Clock()
	dt = 0
	while True:
		start = time.time()
		A = iss.get_A(dt) # update state transition matrix
		Q = iss.get_Q(dt) # update covariance matrix
		a_x = imu.linear_acceleration[0]
		a_y = imu.linear_acceleration[1]
		theta = imu.euler[0]
		u = iss.get_u(a_x, a_y) # get control vector (actually this is for the next loop, but this was the best way of handling the state...)
		with state_vector_lock: # required so we lidar doesn't write at the same time
			x, P = kalman.predict(x, P, A, B, u, Q) # predict state from imu
		ticks_l, ticks_r = enc.get_ticks() # get 'measured' position
		with state_vector_lock:
			x, P = kalman.correct(x, C, z, P, R)
		with path_planning_lock:
			# run control code based on position estimate and current planned path
		with print_lock:
			print("This is dummy text")

	# read imu data (to give starting acceleration)
	# while True:
	# time since clock began = clock.time()?
	# state space model to estimate position from previous imu data (with time)
	# WITH STATE_VECTOR_LOCK:
		# predict belief of position vector, with covariance vector in KF
	# read imu data for this moment
	# read encoder ticks
	# state space model to estimate position, with covariance vector
	# WITH STATE_VECTOR_LOCK:
		# update belief of position vector in KF
	# WITH PATH_PLANNING_LOCK:
		# run control code based on current position estimate and planned path
	# actuate motors based on the control code
		time.sleep(0.01)
		clock.tick(freq) # limits the loop to "freq" fps - stops unnecessary processing power being used
		dt = time.time() - start # make sure this doesn't break / clash with clock.tick()

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

	fast_loop_freq = Config['pygame']['fast_loop_freq'] # 60 Hz loop speed
	print_lock = threading.Lock()
	state_vector_lock = threading.Lock()
	path_planning_lock = threading.Lock()
	fast_thread = threading.Thread(target=fast_loop, args=(print_lock, state_vector_lock, path_planning_lock, imu, enc, fast_loop_freq), name="fast_loop")
	fast_thread.start()
	slow_thread = threading.Thread(target=slow_loop, args=(print_lock, 'dummy_text'), name="slow_loop")
	slow_thread.start()


if __name__ == "__main__":
	main()
