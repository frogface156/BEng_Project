import time
import busio
import board
import adafruit_bno055

def IMU():
	i2c = busio.I2C(board.SCL, board.SDA)
	time.sleep(1)
	sensor = adafruit_bno055.BNO055(i2c)
	return sensor
