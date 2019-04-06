import csv
import sensors
import models
from Config import Config
import numpy as np
from pygame.time import Clock

imu_theta_bias = Config['imu']['theta_bias']

file_path = "/home/pi/BEng_Project/sensor_tests/data/odometry/"
save_file = "supplemented_encoder_data"
extension = ".csv"
log_file_path = file_path + save_file + extension

freq = Config['pygame']['fast_loop_freq']

def log_data(data):
	with open(log_file_path, "a") as f:
		writer = csv.writer(f)
		writer.writerow(data)

def clear_file(file_path):
	with open(file_path, "w") as f:
		writer = csv.writer(f)
		writer.writerow([0, 0, 0.0])

def main():
	clock = Clock()
	imu = sensors.IMU()
	enc = sensors.Encoders()
	enc.get_ticks() # clears previous stored values
	clear_file(log_file_path)
	while True:
		l, r = enc.get_ticks()
		theta = ((imu.euler[0] - imu_theta_bias) * np.pi / 180) % 2*np.pi # radians
		data = [l, r, theta]
		log_data(data)
		print(data)
		clock.tick(freq)

if __name__ == "__main__":
	main()
