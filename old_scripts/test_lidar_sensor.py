import time
import i2c_class
import math
import csv

class lidarScanner(object):
	def __init__(self):
		self.delay = 0.04
		self.addr = 0x08
		self.i2c = i2c_class.I2C(self.addr)
		self.lidar_scan = [0]*360

	def update_scan(self):
#		self.i2c.write_number(5)
		time.sleep(self.delay)
		data = self.i2c.read_block(32) # read 32 bytes of data (16 data points - angle, distance)
		for i in range(16):
			angle = math.ceil((data[0] * 360 / 256))
			distance = int((data[1] * 7))
			self.lidar_scan[angle] = distance
			data.pop(0)
			data.pop(0)

file_path = "/home/pi/BEng_Project/sensor_tests/data/lidar/"
file_name = "lidar_scan"
extension = ".csv"
log_file_path = file_path + file_name + extension


def log_data(data):
	with open(log_file_path, "a") as f:
		writer = csv.writer(f)
		writer.writerow(data)

def clear_file(file):
	with open(file, "w") as f:
		writer = csv.writer(f)
#		writer.writerow()

def main():
	lidar = lidarScanner()
	clear_file(log_file_path)
	counter = 0
	start = time.time()
	while True:
		try:
			counter += 1
			lidar.update_scan()
			print(lidar.lidar_scan)
#			time.sleep(lidar.delay)
			if counter >= 50:
				period = time.time() - start
				counter = 0
				start = time.time()
				print("Time: {}".format(period))
				log_data(lidar.lidar_scan)
				lidar.lidar_scan = [0]*360
		except KeyboardInterrupt:
			log_data(lidar.lidar_scan)
			break

if __name__ == "__main__":
	main()
