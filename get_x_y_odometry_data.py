import sensors
import models
import csv
from Config import Config
import numpy as np
from pygame.time import Clock

file_path = "/home/pi/BEng_Project/sensor_tests/data/odometry/"
save_file = "x_y_predicted_position_data"
extension = ".csv"
log_file_path = file_path + save_file + extension

init = Config['test']['initial_state']
theta_bias = Config['imu']['theta_bias']

freq = Config['pygame']['fast_loop_freq']

oss = models.OdometryStateSpace()

def log_data(data):
	with open(log_file_path, "a") as f:
		writer = csv.writer(f)
		writer.writerow(data)

def get_heading(imu): # shouldn't really be here... but cba to organise rn
	heading = imu.euler[0] - theta_bias
	heading = (heading * np.pi / 180) % 2*np.pi # radians

	return heading

def predict_state_test():
	input("Enter key when in position: ")
	enc = sensors.Encoders()
	imu = sensors.IMU() # reinstantiate each time to avoid errors due to drift in IMU
	l, r = enc.get_ticks() # clears arduino in case there was prior movement
	theta_0 = get_heading(imu) # should = 0 (I think...) It might initialise it to the Earth's Magnetic field but I can't remember. Either way it's fine...
	x = np.array([[init['x_0'], init['vx_0'], init['y_0'], init['vy_0'], theta_0]]).T
	num_steps = 0
	print("Ready to start!")
	clock = Clock()
	while True:
		try:
			l, r = enc.get_ticks()
			x = oss.measure_state(x, l, r)
			num_steps += 1
			clock.tick(freq)
		except KeyboardInterrupt:
			break
	print()
	theta_t = get_heading(imu) # get true final heading
	x_t = int(input("Enter true x position (mm): "))
	y_t = int(input("Enter true y position (mm): "))

	# data = [x_pred, y_pred, theta_pred, x_t, y_t, theta_t, num_steps, freq]
	data = [x[0][0], x[1][0], x[4][0], x_t, y_t, theta_t, num_steps, freq]
	log_data(data)
	print()
	print(data)
	print()

if __name__ == "__main__":
	while True:
		predict_state_test()
