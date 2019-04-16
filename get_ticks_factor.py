import sensors
import time
from Config import Config
enc = sensors.Encoders()
enc.get_ticks() # clear arduino

ticks = [0, 0]

freq = Config['pygame']['fast_loop_freq']
dt = 1 / freq

while True:
	l, r = enc.get_ticks()
	ticks_new = [(ticks[0] + l), (ticks[1] + r)]
	if ticks_new != ticks:
		print(ticks_new)
	ticks = ticks_new
	time.sleep(dt)
