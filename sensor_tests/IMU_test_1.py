import time
import busio
import board
import adafruit_bno055

i2c = busio.I2C(board.SCL, board.SDA)
time.sleep(1) # required or else smbus fails and you spend years debugging code and googling
sensor = adafruit_bno055.BNO055(i2c)

while True:
	print(sensor.linear_acceleration)
	time.sleep(1)
