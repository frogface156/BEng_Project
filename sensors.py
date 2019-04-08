import time
import busio
import board
import adafruit_bno055
from i2c_class import I2C
import math

def IMU():
	i2c = busio.I2C(board.SCL, board.SDA)
	time.sleep(1)
	sensor = adafruit_bno055.BNO055(i2c)
	sensor.euler[0] # initialise euler vectors
	sensor.euler[1]
	sensor.euler[2]

	return sensor

class Encoders(object):
	def __init__(self, addr=0x48):
		self.i2c = I2C(addr)
		self.delay = 0.01 # to allow hardware to keep up with software

	def get_ticks(self):
		#self.i2c.write_number(5) # need to write a byte to call the response
		#time.sleep(self.delay) # need to delay to allow hardware to keep up with software
		ticks = self.i2c.read_block(2) # 2 bytes of data to read (we are assuming that t$
		ticks[0] -= 128
		ticks[1] -= 128

		return ticks[0], ticks[1] # left and right ticks since last call

class LidarScanner(object):
	def __init__(self, addr=0x08):
		self.i2c=I2C(addr)
		self.delay = 0.01
		self.lidar_scan = [0]*360

	def update_scan(self):
		data = self.i2c.read_block(32) # read 32 bytes (16 data points - angle and distance)
		for i in range(16):
			angle = math.ceil((data[0] * 360 / 256))
			distance = int((data[1] * 7))
			self.lidar_scan[angle] = distance
			data.pop(0)
			data.pop(0)

	def get_scan(self, updates=30, delay=0.04):
		self.lidar_scan = [0]*360
		for i in range(updates):
			self.update_scan()
			time.sleep(delay)

		return self.lidar_scan # 360 point list
