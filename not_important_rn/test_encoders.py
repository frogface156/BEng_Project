import encoders
import odometry_state_space as oss
import numpy as np
from pygame.time import Clock
from Config import Config

freq = Config['pygame']['fast_loop_freq']
dt = 1 / freq

init = Config['test']['initial_state']

x = np.array([[init['x_0'], init['vx_0'], init['y_0'], init['vy_0'], init['theta_0']]]).T

enc = encoders.Encoders()
l, r = enc.get_ticks() # clears arduino
clock = Clock()
while True:
	l, r = enc.get_ticks()
	print("L: {}, R: {}".format(l, r))
	z = oss.measure_state(x, l, r)
	print(z)
#	print("x: {:.2f}, vx: {:.2f}, y: {:.2f}, vy: {:.2f}, theta: {:.2f}").format(z[0][0], z[1][0], z[2][0], z[3][0], z[4][0])
	print()
	x = z
	clock.tick(freq)
