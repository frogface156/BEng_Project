import sensors
from Config import Config

ticks_to_mm_factor = Config['odometry']['ticks_to_mm']

l_ticks = []
r_ticks = []

input("Enter a key to start: ")

enc = sensors.Encoders()
enc.get_ticks()

print("Ready!")

while True:
	try:
		l, r = enc.get_ticks()
		l_ticks.append(l)
		r_ticks.append(r)
	except KeyboardInterrupt:
		break
avg = (sum(l_ticks) + sum(r_ticks)) / 2

position = avg * ticks_to_mm_factor
print("Rough final position (mm): {}".format(position))
