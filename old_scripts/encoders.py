from i2c_class import I2C
import time

class Encoders(object):
	def __init__(self, addr=0x08):
		self.i2c = I2C(addr)
		self.delay = 0.01 # to allow hardware to keep up with software

	def get_ticks(self):
		self.i2c.write_number(5) # need to write a byte to call the response
		time.sleep(self.delay) # need to delay to allow hardware to keep up with software
		ticks = self.i2c.read_block(2) # 2 bytes of data to read (we are assuming that the ticks won't go above 255)
		ticks[0] -= 128
		ticks[1] -= 128
		return ticks[0], ticks[1] # left and right ticks since last call

def main():
	enc = Encoders()
	print("This is a test...")
	l, r = enc.get_ticks() # clears arduino
	print("Spin the motors, I'll print the results in a few seconds!!")
	time.sleep(3)
	l, r = enc.get_ticks()
	print("L: {}, R: {}".format(l, r))

if __name__ == "__main__":
	main()

# PPR = 300
