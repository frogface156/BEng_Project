import time
import busio
import board
import adafruit_bno055
from i2c_class import I2C

def IMU():
        i2c = busio.I2C(board.SCL, board.SDA)
        time.sleep(1)
        sensor = adafruit_bno055.BNO055(i2c)
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

