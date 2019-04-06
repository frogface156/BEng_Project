import csv
import sensors
import models
from Config import Config
import numpy as np
from pygame.time import Clock

file_path = "/home/pi/BEng_Project/sensor_tests/data/odometry/"
save_file = "sample_encoder_data"
extension = ".csv"
log_file_path = file_path + save_file + extension

freq = Config['pygame']['fast_loop_freq']

def log_data(data):
	with open(log_file_path, "a") as f:
		writer = csv.writer(f)
		writer.writerow(data)

def main():
	clock = Clock()
	enc = sensors.Encoders()
	enc.get_ticks() # clears previous stored values
	while True:
		l, r = enc.get_ticks()
		data = [l, r]
		log_data(data)
		print(data)
		clock.tick(freq)

if __name__ == "__main__":
	main()
