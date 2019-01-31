#import imu_sensor
#import i2c_class
import encoders
import encoder_matrix_test as emt
import numpy as np
import time
import datetime
import csv

# define variables
x_0 = 0
y_0 = 0
theta = 0
X = np.array([x_0, y_0])
dt_start = time.time()
dt_end = time.time()
freq = 2
dt = 1/freq # only logging every dt seconds (so log isn't full of repeated info!)

date = datetime.datetime.now().strftime("%H-%M-%S-%B-%d-%Y")
path = "sensor_tests/"
file = "ticks_pose_log_"
extension = ".csv"
file_num = 1
log_file_path = path + file + date + extension
counter = 1

# initiate classes (i2c - LIDAR and Encoders, IMU) - perhaps not in this main script actually... rather in sub-scripts
enc = encoders.encoder_handler()

# arduino = i2c_class.I2C(0x08)
# imu = i2c_class.I2C(0x40)


def log_vals(log_file_path, X, theta, tick_change):
	with open(log_file_path, 'a') as log_file:
		writer = csv.writer(log_file)
		writer.writerow([counter, X[0], X[1], theta, tick_change[0], tick_change[1]])

while True:
	if (dt_end - dt_start) >= dt:
		tick_change = [sum_ticks_l, sum_ticks_r]
		log_vals(log_file_path, X, theta, tick_change)
		counter += 1
		X, theta = emt.return_new_pose(X, theta, enc.l_diff, enc.r_diff)
		print("L_diff: {}\tR_diff: {}".format(enc.l_diff, enc.r_diff))
		print("Pose: {}\t Theta: {}".format(X, theta))
		dt_start = time.time()

	# get raw encoder data
	enc.update_states()
	enc.update_ticks()

	dt_end = time.time()

	# compute position from IMU linear acceleration data (and other data e.g. orientation, rotation etc.?) + save values
	# compute optimal estimate for position based on encoders and IMU + save values

