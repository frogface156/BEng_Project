import smbus
import time


class I2C(object):

	def __init__(self, addr):
		self.address = addr # Arduino: 0x08, IM: 0x40
		self.delay = 0.5
		self.bus = smbus.SMBus(1)

	def write_number(self, number):
		self.bus.write_byte(self.address, number)
		return -1

	def read_number(self):
		number = self.bus.read_byte(self.address) # Change params to better suit your application (LIDAR vs encoder data)
		return number

	def read_block(self, bytes=2):
		block = self.bus.read_i2c_block_data(self.address, 0, bytes)
		return block

# test code
if __name__ == "__main__":
	addr = 0x08
	i2c = I2C(addr)
	while True:
		#send_data = int(input("Send some data: "))
		#print("Writing {} to I2C bus".format(send_data))
		#i2c.write_number(send_data)

		i2c.write_number(5)
		time.sleep(0.01)
		#I2Cdata = i2c.read_number()
		I2Cdata = i2c.read_block()
		print("Left Ticks: {}, Right Ticks {}".format(I2Cdata[0], I2Cdata[1]))
