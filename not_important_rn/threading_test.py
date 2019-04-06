# First edit to this file was on 23rd March 2019

from pygame.time import Clock
import encoders
import imu
import threading
import time

def fast_loop(print_lock):
	freq = 60
	clock = Clock()
	while True:
		start = time.time()
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
			print(time.time() - start)
		time.sleep(0.01)
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
	fast_loop_freq = 60 # 60 Hz loop speed

	print_lock = threading.Lock()
	state_vector_lock = threading.Lock()
	path_planning_lock = threading.Lock()
	fast_thread = threading.Thread(target=fast_loop, args=(print_lock,), name="fast_loop")
	fast_thread.start()
	slow_thread = threading.Thread(target=slow_loop, args=(print_lock, 'dummy_text'), name="slow_loop")
	slow_thread.start()


if __name__ == "__main__":
	main()
