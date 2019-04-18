import csv
import sensors
import models
from Config import Config
import numpy as np
from pygame.time import Clock
import time

file_path = "/home/pi/BEng_Project/sensor_tests/data/odometry/"
save_file = "sample_encoder_data_50Hz"
extension = ".csv"
log_file_path = file_path + save_file + extension

freq = Config['pygame']['fast_loop_freq']

def clear_file(file):
	with open(file, "w") as f:
		writer = csv.writer(f)

def log_data(file, data):
	with open(file, "a") as f:
		writer = csv.writer(f)
		writer.writerow(data)

def main():
	clock = Clock()
	clear_file(log_file_path)
	enc = sensors.Encoders()
	enc.get_ticks() # clears previous stored values
	start = time.time()
	while True:
		end = time.time()
		period = end - start
		actual_freq = 1 / period
		print("{}Hz".format(actual_freq))
		start = end
		l, r = enc.get_ticks()
		data = [l, r]
		log_data(log_file_path, data)
		print(data)
		clock.tick(freq)

if __name__ == "__main__":
	main()
